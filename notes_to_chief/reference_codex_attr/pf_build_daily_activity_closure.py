#!/usr/bin/env python3
"""Build the IMAGE-only DailyActivityState non-wire closure.

The builder starts from the hash-pinned effective V3 A2, proves six physical
non-wire sites in the complete DailyActivityState serializer CFG, and removes
only their twelve path-insensitive W/R analysis rows.  Frozen inputs are never
modified.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import re
import struct
import sys
import tempfile
from collections import Counter
from dataclasses import replace
from io import StringIO
from pathlib import Path
from typing import Iterable, Mapping, Sequence


IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
DECODER_SHA256 = "0bb792bb6b0561e11592ab7f8c93c65cd1e0fba0210e2a6bf40c9e5a8579112e"
V2_VALIDATOR_SHA256 = "7a9c08014974ef41273971a0e451701cc1d8fa9381d80f69a943f86c5a53c8c9"
V3_VALIDATOR_SHA256 = "3d145407c9a6e4236eefe829c9fb9eb0757bf53cce9ac9cb136f201f594a360b"
V3_MANIFEST_SHA256 = "dc87eedc65ed5e07ce4673742b6a0d20304140bb177e617c6af8b3846bd0b50e"
SLOT34_A2_SHA256 = "1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334"
SLOT34_PRIORITY_SHA256 = "00ef0f3cb632b40ba168ce79bbd656fc7a6936a55f3b3e185c6e63b32c39ec5d"
TARGET_652A30_SHA256 = "217f7f9854df7412ca942d755c0ed858130954f93c8384185af9719415720592"

DECODER_NAME = "pf_extract_protocol.py"
V2_VALIDATOR_NAME = "pf_validate_v2_effective_capture.py"
V3_VALIDATOR_NAME = "pf_validate_v3_effective_capture.py"
V3_MANIFEST_NAME = "PF_V3_MANIFEST.md"
SLOT34_A2_NAME = "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"
SLOT34_PRIORITY_NAME = "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv"
TARGET_652A30_NAME = "PF_TARGET_652A30_A2_DELTA.tsv"

A2_OUTPUT_NAME = "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv"
PRIORITY_OUTPUT_NAME = "PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv"
REPORT_NAME = "PF_DAILY_ACTIVITY_CLOSURE.md"
OWN_OUTPUTS = {A2_OUTPUT_NAME, PRIORITY_OUTPUT_NAME, REPORT_NAME}
PUBLISH_LOCK_NAME = ".PF_DAILY_ACTIVITY_PUBLISH.lock"
EVIDENCE_TICKET = "STATIC-DAILY-ACTIVITY-NONWIRE"

SERIALIZER_START = 0x0069CB20
SERIALIZER_END = 0x0069CC63
SERIALIZER_OFF = 0x0029BF20
SERIALIZER_SHA256 = "28f27bb1158748030e9876e896e729d3b6fe1d18a988f7e90ed1d7b0745e31ca"
HELPER_START = 0x00B0BF70
HELPER_END = 0x00B0BFDC
HELPER_OFF = 0x0070B370
HELPER_SHA256 = "4e1374fd126457c82d11bf3e6efa0fda845bb85e2c2a985ed67c4eff3f4eb7e6"
INVALID_IAT = 0x00C3B4C0
WIRE_WRITE = 0x0089A600
WIRE_READ = 0x0089A640

DIRECT_INVALID_SITE = 0x0069CB82
REGISTER_INVALID_SITES = (0x0069CB9A, 0x0069CBA3, 0x0069CBB8, 0x0069CBBF)
REGISTER_IAT_DEF = 0x0069CB90
HELPER_CALL_SITE = 0x0069CBD4
HELPER_RECEIVER_SITE = 0x0069CBD0
NEUTRAL_STACK_IDENTITY_SITE = 0x0069CB6C
TARGET_SITES = (DIRECT_INVALID_SITE, *REGISTER_INVALID_SITES, HELPER_CALL_SITE)

# line, source delta key, direction, order, tag, blocker, physical site
EXPECTED_ROWS = (
    (986, "c975f2a41acbee4c90da1e556d1b5e5c850024e17b12b3a4a1c006208d1f2de7", "R", "4", "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL", "UNKNOWN(invalid_parameter_import_call_wire_effect_unproved)", 0x0069CB82),
    (987, "5b2db97c41b1ff2e6545358f9eccff40df39cbddd5941ea101f68ac4f8287ae2", "W", "5", "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL", "UNKNOWN(invalid_parameter_import_call_wire_effect_unproved)", 0x0069CB82),
    (988, "d71337a06fb09d2a88aa43f0bdc9c4a4a1128bd27e138df80999394ebee24538", "R", "5", "PE_IMPORT_INVALID_PARAMETER_NOINFO_SINGLETON_REGISTER_CALL", "UNKNOWN(invalid_parameter_singleton_register_call_wire_effect_unproved)", 0x0069CB9A),
    (989, "98b900b14a49ea0fe4523cfc52b018dfe0e69da5e1e6c175a3a285463f466cd0", "W", "6", "PE_IMPORT_INVALID_PARAMETER_NOINFO_SINGLETON_REGISTER_CALL", "UNKNOWN(invalid_parameter_singleton_register_call_wire_effect_unproved)", 0x0069CB9A),
    (990, "5a88d810ceabc46e1bf1361db5ad857ebcd3f2df84f47197ada1ad5670df3c42", "R", "6", "PE_IMPORT_INVALID_PARAMETER_NOINFO_SINGLETON_REGISTER_CALL", "UNKNOWN(invalid_parameter_singleton_register_call_wire_effect_unproved)", 0x0069CBA3),
    (991, "b139e22eb7ba502153ead25d747687fe77b9f6e72877094d6398b85aee857ffe", "W", "7", "PE_IMPORT_INVALID_PARAMETER_NOINFO_SINGLETON_REGISTER_CALL", "UNKNOWN(invalid_parameter_singleton_register_call_wire_effect_unproved)", 0x0069CBA3),
    (993, "06b62262816a3cf302c503fb0b052fe8afc4a599f0cf641c8aed1ce63aba6985", "R", "7", "PE_IMPORT_INVALID_PARAMETER_NOINFO_SINGLETON_REGISTER_CALL", "UNKNOWN(invalid_parameter_singleton_register_call_wire_effect_unproved)", 0x0069CBB8),
    (994, "7f5fa406a9ade5d2d77c4d6aaba4b1b67b2e320a5eca802f4509783b619c9035", "W", "9", "PE_IMPORT_INVALID_PARAMETER_NOINFO_SINGLETON_REGISTER_CALL", "UNKNOWN(invalid_parameter_singleton_register_call_wire_effect_unproved)", 0x0069CBB8),
    (995, "5aff5a1340677fb2cb3939fbee6c82af7718682697448f182f023f1b81b74f17", "R", "8", "PE_IMPORT_INVALID_PARAMETER_NOINFO_SINGLETON_REGISTER_CALL", "UNKNOWN(invalid_parameter_singleton_register_call_wire_effect_unproved)", 0x0069CBBF),
    (996, "a5663d2a5825ab8677f76ee7a7e1d788039a2d760fe50a2a7aa5e5831c52ac95", "W", "10", "PE_IMPORT_INVALID_PARAMETER_NOINFO_SINGLETON_REGISTER_CALL", "UNKNOWN(invalid_parameter_singleton_register_call_wire_effect_unproved)", 0x0069CBBF),
    (998, "0fe6457c8be546387faa0e07823ecc194d8cbb9c1389d286103ae05ef9c3de42", "R", "9", "MUTATING_CHAIN_PLUS_04_HELPER", "UNKNOWN(mutable_chain_target_object_alias_unproved)", 0x0069CBD4),
    (999, "4fd665398d0630f65cf047d091fbd4fa865fd322dda5556e76e59b5847b872fa", "W", "12", "MUTATING_CHAIN_PLUS_04_HELPER", "UNKNOWN(mutable_chain_target_object_alias_unproved)", 0x0069CBD4),
)

# Independent immutable oracles for the complete predecessor row and its large
# gate/proof cell.  The canonical row key covers every column; the gate digest
# makes the high-risk semantic cell explicit rather than relying on a subset
# comparison or on report prose.
EXPECTED_ROW_KEYS = {
    986: "1179b702b5ff44837695529e716e266de21d659dec6407742b99b371e815aa1e",
    987: "fe76e08e9c12f7b8344ffb56a78ed6b697d138a06abe229b9df09130022076ca",
    988: "a0fbcac4364a8755c76be57424a3825980ad0248d0a4f644486398909d25dd5c",
    989: "348bfd8d68193a45c9fa4ef7a25f1aa780b1ba5979363713ee3f56f91cf14af3",
    990: "de89064a2ed47351c5f5a8a9ab1dcd32f7fa5daa3be78018169aec0637e37c86",
    991: "97cd50dc942b9c1a88593f35bdf7e7e60be1f7405df81b71c0ce7a33d225345b",
    993: "16f0374e9b18a640cafffe1ff32048b904cd9c7df039bc78f5a1d2c83f271576",
    994: "aa5dc305336c5102dbe87f3df2b8437e64084fe85521e6dec2d1907ada97d06a",
    995: "9b344f70ce61da2080ec36eaffb31e102e18ee1145d7da8b84c553758e5dadd2",
    996: "bdba7df88a4e71e6e9a0d1357c87cb023f6ffa29aa5e6bed39c6aaa5c02d5bf6",
    998: "0f640de4d1acf77775aa19eb44a3ec0dddf67f919884b77e3a113a8b67556453",
    999: "45a3c931dba00af66c63c8e978fe764dd935a5e7ceb9746f0b92909ffcbca4e9",
}
EXPECTED_GATE_SHA256 = {
    986: "932cb01e6cb2acb6cc84b05d6da8da33dcd04e56b712156a6c7e2d4e15f40d79",
    987: "932cb01e6cb2acb6cc84b05d6da8da33dcd04e56b712156a6c7e2d4e15f40d79",
    988: "1b1cfc44a200ddead7c8c6317653d71f3b4fda3c5202bf1433f60acb68df3d8e",
    989: "1b1cfc44a200ddead7c8c6317653d71f3b4fda3c5202bf1433f60acb68df3d8e",
    990: "f04d72b3ed617f50cac80ba0acb8cac07a11aaf5118a9c1fe14a498359ecee0b",
    991: "f04d72b3ed617f50cac80ba0acb8cac07a11aaf5118a9c1fe14a498359ecee0b",
    993: "a29c9ee071e69f73be170fb57cd7fcc6675057120c3fe95578dfd514a204ad1c",
    994: "a29c9ee071e69f73be170fb57cd7fcc6675057120c3fe95578dfd514a204ad1c",
    995: "d981f7e3777c69262d74f25e568b6e0d91c51c25c1b15d9652054ac77bb2fdfb",
    996: "d981f7e3777c69262d74f25e568b6e0d91c51c25c1b15d9652054ac77bb2fdfb",
    998: "dc5b6841baa68980fdd141cf4e3a3d4f9bb43a41cac7aeb25e0275088a09c117",
    999: "dc5b6841baa68980fdd141cf4e3a3d4f9bb43a41cac7aeb25e0275088a09c117",
}

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


class BuildError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_hash(path: Path, expected: str, label: str) -> None:
    actual = sha256_path(path)
    if actual != expected:
        raise BuildError(f"{label} SHA-256 mismatch: expected {expected}, got {actual}")


def canonical_row_key(fields: Sequence[str], row: Mapping[str, str]) -> str:
    payload = json.dumps(
        [row[name] for name in fields], ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(payload)


def make_delta_key(parts: Iterable[str]) -> str:
    return sha256_bytes("\x1f".join(parts).encode("utf-8"))


def parse_tsv_text(
    text: str, label: str
) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    reader = csv.reader(StringIO(text, newline=""), delimiter="\t")
    physical = list(reader)
    if not physical:
        raise BuildError(f"missing TSV header: {label}")
    fields = list(physical[0])
    if not fields or any(not field for field in fields):
        raise BuildError(f"empty TSV header cell: {label}")
    if len(fields) != len(set(fields)):
        raise BuildError(f"duplicate TSV header: {label}")
    rows: list[tuple[int, dict[str, str]]] = []
    for line, values in enumerate(physical[1:], start=2):
        if len(values) != len(fields):
            kind = "missing" if len(values) < len(fields) else "extra"
            raise BuildError(
                f"{kind} TSV cells: {label}:{line}: {len(values)} != {len(fields)}"
            )
        rows.append((line, dict(zip(fields, values, strict=True))))
    return fields, rows


def read_tsv_with_lines(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    return parse_tsv_text(path.read_text(encoding="utf-8"), path.name)


def verify_strict_tsv_mutation_controls() -> None:
    malformed = (
        ("a\ta\n1\t2\n", "duplicate TSV header"),
        ("a\tb\n1\n", "missing TSV cells"),
        ("a\tb\n1\t2\t3\n", "extra TSV cells"),
    )
    for text, expected in malformed:
        try:
            parse_tsv_text(text, "MUTATION_CONTROL")
        except BuildError as exc:
            if expected not in str(exc):
                raise BuildError(f"strict TSV control failed with wrong reason: {exc}") from exc
        else:
            raise BuildError(f"strict TSV mutation escaped: {expected}")


def tsv_bytes(columns: Sequence[str], rows: Sequence[Mapping[str, str]]) -> bytes:
    handle = StringIO(newline="")
    writer = csv.DictWriter(
        handle, fieldnames=list(columns), delimiter="\t", lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue().encode("utf-8")


def load_module(name: str, path: Path, expected_hash: str) -> object:
    require_hash(path, expected_hash, path.name)
    if name in sys.modules:
        raise BuildError(f"module-name collision: {name}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise BuildError(f"cannot load module: {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


def function_span(decoder: object, image: object, start: int, end: int, digest: str) -> object:
    off = image.va_to_off(start)
    if off is None:
        raise BuildError(f"unmapped function start: 0x{start:08X}")
    return decoder.FunctionSpan(start, end, off, off + end - start, digest)


def require_full_decode(decoded: object, start: int, end: int, nodes: int, edges: int) -> None:
    if decoded.errors:
        raise BuildError(f"decoder errors in 0x{start:08X}: {decoded.errors}")
    actual_edges = sum(len(values) for values in decoded.successors.values())
    if len(decoded.instructions) != nodes or actual_edges != edges:
        raise BuildError(
            f"CFG census drift 0x{start:08X}: "
            f"{len(decoded.instructions)}/{actual_edges} != {nodes}/{edges}"
        )
    coverage = [0] * (end - start)
    for instruction in decoded.instructions.values():
        begin = instruction.va - start
        for index in range(begin, begin + instruction.size):
            if not 0 <= index < len(coverage) or coverage[index]:
                raise BuildError(f"CFG overlap/outside at 0x{instruction.va:08X}")
            coverage[index] = 1
    if not all(coverage):
        raise BuildError(f"CFG uncovered bytes at 0x{start:08X}")


def is_reg(operand: object | None, name: str) -> bool:
    return bool(
        operand is not None
        and operand.kind == "reg"
        and decoder_base_reg(operand.reg) == name
    )


def decoder_base_reg(name: str | None) -> str | None:
    aliases = {
        "al": "eax", "ah": "eax", "cl": "ecx", "ch": "ecx",
        "dl": "edx", "dh": "edx", "bl": "ebx", "bh": "ebx",
    }
    return aliases.get(name, name)


def verify_serializer(decoder: object, image: object) -> tuple[object, dict[int, int]]:
    body = image.data[SERIALIZER_OFF:SERIALIZER_OFF + SERIALIZER_END - SERIALIZER_START]
    if sha256_bytes(body) != SERIALIZER_SHA256:
        raise BuildError("DailyActivityState serializer span drift")
    span = function_span(decoder, image, SERIALIZER_START, SERIALIZER_END, SERIALIZER_SHA256)
    decoded = decoder.decode_function(image, span)
    require_full_decode(decoded, SERIALIZER_START, SERIALIZER_END, 117, 126)

    calls = {
        va: (instruction.kind, instruction.target, instruction.src)
        for va, instruction in decoded.instructions.items()
        if instruction.kind in {"call", "call_indirect"}
    }
    expected_call_sites = {
        0x0069CB37, 0x0069CB57, 0x0069CB82, 0x0069CB9A,
        0x0069CBA3, 0x0069CBAF, 0x0069CBB8, 0x0069CBBF,
        0x0069CBCB, 0x0069CBD4, 0x0069CBFE, 0x0069CC1B,
        0x0069CC2B, 0x0069CC4C,
    }
    if set(calls) != expected_call_sites:
        raise BuildError(f"serializer call-site census drift: {sorted(calls)}")
    direct_targets = {
        0x0069CB37: 0x00467790, 0x0069CB57: WIRE_WRITE,
        0x0069CBAF: WIRE_WRITE, 0x0069CBCB: WIRE_WRITE,
        0x0069CBD4: HELPER_START, 0x0069CBFE: WIRE_READ,
        0x0069CC1B: WIRE_READ, 0x0069CC2B: WIRE_READ,
        0x0069CC4C: 0x00652A30,
    }
    for site, target in direct_targets.items():
        instruction = decoded.instructions[site]
        if instruction.kind != "call" or instruction.target != target:
            raise BuildError(f"direct-call target drift at 0x{site:08X}")
    direct_invalid = decoded.instructions[DIRECT_INVALID_SITE]
    if not (
        direct_invalid.kind == "call_indirect"
        and direct_invalid.src.kind == "mem"
        and direct_invalid.src.absolute == INVALID_IAT
        and direct_invalid.raw == bytes.fromhex("FF15C0B4C300")
    ):
        raise BuildError("direct invalid-parameter call drift")
    definition = decoded.instructions[REGISTER_IAT_DEF]
    if not (
        definition.kind == "mov" and is_reg(definition.dst, "ebp")
        and definition.src.kind == "mem" and definition.src.absolute == INVALID_IAT
        and definition.raw == bytes.fromhex("8B2DC0B4C300")
    ):
        raise BuildError("EBP invalid-parameter IAT definition drift")
    for site in REGISTER_INVALID_SITES:
        instruction = decoded.instructions[site]
        if not (
            instruction.kind == "call_indirect" and instruction.src.kind == "reg"
            and instruction.src.reg == "ebp" and instruction.raw == bytes.fromhex("FFD5")
        ):
            raise BuildError(f"register invalid-parameter call drift at 0x{site:08X}")

    # Positive singleton EBP reaching-definition proof at all four register calls.
    # ENTRY_UNDEFINED is carried explicitly, so a bypass path cannot disappear
    # when predecessor definition sets are unioned.
    entry_undefined = -1
    dom = dominators(decoded, SERIALIZER_START)
    ebp_in: dict[int, frozenset[int]] = {va: frozenset() for va in decoded.instructions}
    ebp_out: dict[int, frozenset[int]] = {va: frozenset() for va in decoded.instructions}
    changed = True
    while changed:
        changed = False
        for va in sorted(decoded.instructions):
            incoming = (
                frozenset({entry_undefined})
                if va == SERIALIZER_START
                else frozenset(
                    value for pred in decoded.predecessors[va] for value in ebp_out[pred]
                )
            )
            instruction = decoded.instructions[va]
            defines = is_reg(instruction.dst, "ebp")
            outgoing = frozenset({va}) if defines else incoming
            if incoming != ebp_in[va] or outgoing != ebp_out[va]:
                ebp_in[va], ebp_out[va] = incoming, outgoing
                changed = True
    if any(
        ebp_in[site] != frozenset({REGISTER_IAT_DEF})
        or entry_undefined in ebp_in[site]
        or REGISTER_IAT_DEF not in dom[site]
        for site in REGISTER_INVALID_SITES
    ):
        raise BuildError("register invalid-parameter singleton reaching definition failed")

    # Unique entry-relative stack depth.  Depth D means ESP == entry_SP - D.
    cleanup = {
        0x00467790: 8, WIRE_WRITE: 12, WIRE_READ: 12,
        HELPER_START: 0, 0x00652A30: 8,
    }
    depth_in: dict[int, set[int]] = {SERIALIZER_START: {0}}
    pending = [SERIALIZER_START]
    while pending:
        va = pending.pop()
        instruction = decoded.instructions[va]
        delta = 0
        if instruction.kind == "push":
            delta = 4
        elif instruction.kind == "pop":
            delta = -4
        elif instruction.kind in {"sub", "add"} and is_reg(instruction.dst, "esp"):
            if instruction.src is None or instruction.src.kind != "imm":
                raise BuildError(f"non-immediate ESP arithmetic at 0x{va:08X}")
            delta = instruction.src.imm if instruction.kind == "sub" else -instruction.src.imm
        elif instruction.kind == "lea" and is_reg(instruction.dst, "esp"):
            if not (
                va == NEUTRAL_STACK_IDENTITY_SITE
                and instruction.raw == bytes.fromhex("8D642400")
                and instruction.src.kind == "mem" and instruction.src.base == "esp"
                and instruction.src.disp == 0 and instruction.src.index is None
            ):
                raise BuildError(f"unapproved ESP LEA at 0x{va:08X}")
        elif instruction.kind == "call":
            if instruction.target not in cleanup:
                raise BuildError(f"unknown direct-call cleanup at 0x{va:08X}")
            delta = -cleanup[instruction.target]
        elif instruction.kind == "call_indirect":
            if va not in {DIRECT_INVALID_SITE, *REGISTER_INVALID_SITES}:
                raise BuildError(f"unknown indirect-call cleanup at 0x{va:08X}")
            delta = 0
        outgoing = {value + delta for value in depth_in[va]}
        if any(value < 0 for value in outgoing):
            raise BuildError(f"negative stack depth after 0x{va:08X}")
        for successor in decoded.successors[va]:
            merged = depth_in.get(successor, set()) | outgoing
            if merged != depth_in.get(successor, set()):
                depth_in[successor] = merged
                pending.append(successor)
    if set(depth_in) != set(decoded.instructions):
        raise BuildError("stack analysis did not reach complete serializer CFG")
    ambiguous = {va: values for va, values in depth_in.items() if len(values) != 1}
    if ambiguous:
        raise BuildError(f"non-unique serializer stack depths: {ambiguous}")
    depths = {va: next(iter(values)) for va, values in depth_in.items()}
    if any(depths[site] != 40 for site in TARGET_SITES):
        raise BuildError(f"target stack-depth drift: {[(hex(s), depths[s]) for s in TARGET_SITES]}")
    if depths[0x0069CC60] != 0:
        raise BuildError("serializer exit stack depth is not zero")

    receiver = decoded.instructions[HELPER_RECEIVER_SITE]
    if not (
        receiver.kind == "lea" and is_reg(receiver.dst, "ecx")
        and receiver.src.kind == "mem" and receiver.src.base == "esp"
        and receiver.src.index is None and receiver.src.disp == 0x14
        and receiver.raw == bytes.fromhex("8D4C2414")
        and receiver.next_va == HELPER_CALL_SITE
    ):
        raise BuildError("helper receiver definition drift")
    # depth 0x28 and disp +0x14 => receiver entry_SP-0x14; +4 write => -0x10.
    if depths[HELPER_RECEIVER_SITE] - receiver.src.disp != 0x14:
        raise BuildError("helper receiver entry-relative address drift")
    return decoded, depths


def dominators(decoded: object, start: int) -> dict[int, set[int]]:
    nodes = set(decoded.instructions)
    result = {va: ({start} if va == start else set(nodes)) for va in nodes}
    changed = True
    while changed:
        changed = False
        for va in sorted(nodes):
            if va == start:
                continue
            preds = decoded.predecessors[va]
            if not preds:
                raise BuildError(f"non-entry CFG node lacks predecessor: 0x{va:08X}")
            updated = {va} | set.intersection(*(result[pred] for pred in preds))
            if updated != result[va]:
                result[va] = updated
                changed = True
    return result


def verify_helper(decoder: object, image: object) -> tuple[object, int, int]:
    body = image.data[HELPER_OFF:HELPER_OFF + HELPER_END - HELPER_START]
    if len(body) != 108 or sha256_bytes(body) != HELPER_SHA256:
        raise BuildError("0x00B0BF70 helper span drift")
    span = function_span(decoder, image, HELPER_START, HELPER_END, HELPER_SHA256)
    decoded = decoder.decode_function(image, span)
    require_full_decode(decoded, HELPER_START, HELPER_END, 44, 49)
    dom = dominators(decoded, HELPER_START)

    iat_load = 0x00B0BF77
    guard_calls = (0x00B0BF7F, 0x00B0BF8A)
    writes = (0x00B0BFAB, 0x00B0BFC8, 0x00B0BFD7)
    load = decoded.instructions[iat_load]
    if not (
        load.kind == "mov" and is_reg(load.dst, "edi")
        and load.src.kind == "mem" and load.src.absolute == INVALID_IAT
    ):
        raise BuildError("helper invalid-parameter IAT load drift")
    explicit_writes = tuple(sorted(
        va for va, instruction in decoded.instructions.items()
        if instruction.dst is not None and instruction.dst.kind == "mem"
        and instruction.kind in {"mov", "unknown_write"}
    ))
    if explicit_writes != writes:
        raise BuildError(f"helper explicit-write census drift: {explicit_writes}")
    if any(
        decoded.instructions[site].dst.base != "esi"
        or decoded.instructions[site].dst.disp != 4
        or decoded.instructions[site].dst.index is not None
        for site in writes
    ):
        raise BuildError("helper write shape is not exactly [ESI+4]")
    if decoded.instructions[HELPER_START + 1].raw != bytes.fromhex("8BF1"):
        raise BuildError("helper receiver ECX-to-ESI copy drift")
    if any(HELPER_START + 1 not in dom[site] for site in writes):
        raise BuildError("helper receiver definition does not dominate all writes")

    edi_in: dict[int, frozenset[int]] = {va: frozenset() for va in decoded.instructions}
    edi_out: dict[int, frozenset[int]] = {va: frozenset() for va in decoded.instructions}
    changed = True
    while changed:
        changed = False
        for va in sorted(decoded.instructions):
            incoming = frozenset(
                value for pred in decoded.predecessors[va] for value in edi_out[pred]
            )
            instruction = decoded.instructions[va]
            outgoing = frozenset({va}) if is_reg(instruction.dst, "edi") else incoming
            if incoming != edi_in[va] or outgoing != edi_out[va]:
                edi_in[va], edi_out[va] = incoming, outgoing
                changed = True
    for site in guard_calls:
        instruction = decoded.instructions[site]
        if not (
            instruction.kind == "call_indirect" and instruction.src.kind == "reg"
            and instruction.src.reg == "edi" and iat_load in dom[site]
            and edi_in[site] == frozenset({iat_load})
        ):
            raise BuildError(f"helper guard-call proof failed at 0x{site:08X}")

    direct_wire_intersections = sum(
        instruction.kind == "call" and instruction.target in {WIRE_WRITE, WIRE_READ}
        for instruction in decoded.instructions.values()
    )
    literal_hits = sum(body.count(struct.pack("<I", target)) for target in (WIRE_WRITE, WIRE_READ))
    if direct_wire_intersections != 0 or literal_hits != 0:
        raise BuildError("wire primitive intersects helper graph/literals")
    return decoded, direct_wire_intersections, literal_hits


def whole_image_e8_census(image: object) -> dict[int, int]:
    counts = {WIRE_WRITE: 0, WIRE_READ: 0}
    data = image.data
    for off in range(len(data) - 4):
        if data[off] != 0xE8:
            continue
        va = image.off_to_va(off)
        if va is None:
            continue
        target = (va + 5 + struct.unpack_from("<i", data, off + 1)[0]) & 0xFFFFFFFF
        if target in counts:
            counts[target] += 1
    if counts != {WIRE_WRITE: 1350, WIRE_READ: 1350}:
        raise BuildError(f"whole-image E8 wire census drift: {counts}")
    return counts


def prior_keys_and_targets(external: Path) -> tuple[dict[str, str], dict[tuple[str, str, str], str]]:
    keys: dict[str, str] = {}
    targets: dict[tuple[str, str, str], str] = {}
    for path in sorted(external.glob("*.tsv")):
        if path.name in {A2_OUTPUT_NAME, PRIORITY_OUTPUT_NAME}:
            continue
        fields, rows = read_tsv_with_lines(path)
        for line, row in rows:
            for column in ("delta_key", "dedup_key"):
                value = row.get(column, "")
                if value and value != "N/A":
                    owner = f"{path.name}:{line}"
                    if value in keys:
                        raise BuildError(f"pre-existing provenance collision: {value}: {keys[value]}/{owner}")
                    keys[value] = owner
            if (
                path.name.startswith(("PF_A2_", "PF_TARGET"))
                and {"base_file", "base_line", "base_row_key"}.issubset(fields)
                and row.get("base_file") not in {"", "N/A"}
                and row.get("base_row_key") not in {"", "N/A"}
            ):
                identity = (row["base_file"], row["base_line"], row["base_row_key"])
                owner = f"{path.name}:{line}"
                if identity in targets:
                    raise BuildError(f"pre-existing A2 target collision: {identity}")
                targets[identity] = owner
    return keys, targets


def subcall_is_flattened_machine(field: object, fields: Sequence[object]) -> bool:
    target = str(field.tag).split(":", 1)[1]
    for candidate in fields:
        if candidate.sequence <= field.sequence:
            continue
        searchable = " ".join(
            (
                str(candidate.field_offset), str(candidate.origin_field_offset),
                str(candidate.gate_condition), str(candidate.origin_gate_condition),
            )
        )
        if target in searchable and not str(candidate.tag).startswith("SUBCALL:"):
            return True
    return False


def effective_field_unknown_reasons(
    field: object, fields: Sequence[object], v2: object
) -> tuple[str, ...]:
    """One executable closure predicate over every schema-bearing dimension."""
    reasons: set[str] = set()
    tag = str(field.tag)
    offset = str(field.field_offset)
    length = str(field.length)
    order = str(field.wire_order)
    gate = str(field.gate_condition)

    def unknown(value: str) -> bool:
        return not value or value == "UNKNOWN" or "UNKNOWN(" in value

    if unknown(tag):
        reasons.add("UNKNOWN_TAG")
    elif not (
        v2.NUMERIC_TAG_RE.fullmatch(tag)
        or tag in v2.ZERO_LENGTH_TAGS
        or tag in v2.STRING_TAGS
        or tag.startswith("SUBCALL:")
    ):
        reasons.add("UNSUPPORTED_TAG")
    if unknown(offset):
        reasons.add("UNKNOWN_OFFSET")
    if unknown(length):
        reasons.add("UNKNOWN_LENGTH")
    elif v2.NUMERIC_TAG_RE.fullmatch(tag) and not length.isdigit():
        reasons.add("INVALID_NUMERIC_LENGTH")
    if not (order.isdigit() or v2.ALT_ORDER_RE.fullmatch(order)):
        reasons.add("UNKNOWN_OR_UNSUPPORTED_ORDER")
    if unknown(gate):
        reasons.add("UNKNOWN_GATE")
    kind_gate = v2.KIND_GATE_RE.fullmatch(gate)
    if kind_gate is not None:
        reasons.add("KIND_GATE_OUTSIDE_CTRACE")
    if gate.startswith("test@") and " mask=" in gate:
        reasons.add("UNEXECUTED_MASK_GATE")
    if ("!=NULL" in gate or "DECODED_" in gate) and tag.startswith("SUBCALL:"):
        reasons.add("UNEXECUTED_PRESENCE_GATE")
    if tag.startswith("SUBCALL:") and not subcall_is_flattened_machine(field, fields):
        reasons.add("UNFLATTENED_SUBCALL")
    return tuple(sorted(reasons))


def verify_closure_predicate_mutation_controls(
    residual: Mapping[str, Sequence[object]], v2: object
) -> None:
    all_fields = [field for direction in ("W", "R") for field in residual[direction]]
    if any(effective_field_unknown_reasons(field, residual[direction], v2)
           for direction in ("W", "R") for field in residual[direction]):
        raise BuildError("unmutated Daily residual fails closure predicate")
    numeric = next(field for field in all_fields if v2.NUMERIC_TAG_RE.fullmatch(str(field.tag)))
    mutations = (
        replace(numeric, tag="UNKNOWN(test_mutation)"),
        replace(numeric, field_offset="UNKNOWN(test_mutation)"),
        replace(numeric, length="UNKNOWN(test_mutation)"),
        replace(numeric, wire_order="UNKNOWN(test_mutation)"),
        replace(numeric, gate_condition="UNKNOWN(test_mutation)"),
    )
    if any(not effective_field_unknown_reasons(value, (value,), v2) for value in mutations):
        raise BuildError("closure predicate mutation escaped")
    marker = next(field for field in all_fields if str(field.tag).startswith("SUBCALL:"))
    if "UNFLATTENED_SUBCALL" not in effective_field_unknown_reasons(marker, (marker,), v2):
        raise BuildError("unflattened-subcall mutation control escaped")


def build_a2_delta(external: Path, v3: object) -> tuple[list[dict[str, str]], dict[str, int]]:
    fields, rows = read_tsv_with_lines(external / SLOT34_A2_NAME)
    by_line = {line: row for line, row in rows}
    _registry, effective, _candidates, counts, _per_file = v3.apply_v3_removals(external)
    if counts.get("effective_rows") != 8671:
        raise BuildError(f"effective V3 A2 census drift: {counts}")
    effective_index = {
        (message, direction, value.evidence_key): value
        for (message, direction), values in effective.items()
        for value in values
    }
    prior_keys, prior_targets = prior_keys_and_targets(external)
    output: list[dict[str, str]] = []
    for line, source_key, direction, order, tag, blocker, site in EXPECTED_ROWS:
        row = by_line.get(line)
        if row is None:
            raise BuildError(f"missing slot34 base line: {line}")
        expected = {
            "delta_key": source_key, "action": "ADD_CORRECTED_SLOT34_ROW",
            "message": "DailyActivityState", "schema_variant": "SINGLETON_SLOT34",
            "direction(W/R)": direction, "new_order": order, "new_tag": tag,
            "new_field_offset": blocker, "new_len": "N/A",
            "new_span_start": "0x0069CB20", "new_span_end": "0x0069CC63",
            "new_span_sha256": SERIALIZER_SHA256,
            "new_file_off_claim": f"0x{site - 0x00400C00:08X}", "source": "IMAGE",
        }
        if any(row.get(name) != value for name, value in expected.items()):
            raise BuildError(f"slot34 Daily base-row drift at line {line}")
        row_key = canonical_row_key(fields, row)
        if row_key != EXPECTED_ROW_KEYS[line]:
            raise BuildError(f"complete slot34 predecessor row oracle drift at line {line}")
        if sha256_bytes(row["new_gate_condition"].encode("utf-8")) != EXPECTED_GATE_SHA256[line]:
            raise BuildError(f"slot34 predecessor gate oracle drift at line {line}")
        identity = (SLOT34_A2_NAME, str(line), row_key)
        if identity in prior_targets:
            raise BuildError(f"Daily A2 target already delivered by {prior_targets[identity]}")
        field = effective_index.get(("DailyActivityState", direction, source_key))
        if field is None:
            raise BuildError(f"Daily row is not effective in V3: {line}")
        actual = (field.wire_order, field.tag, field.field_offset, field.length)
        if actual != (order, tag, blocker, "N/A"):
            raise BuildError(f"effective V3 Daily row contract drift at line {line}: {actual}")
        if site == HELPER_CALL_SITE:
            change_type = "NONWIRE_STACK_LOCAL_LINK_STATE_HELPER"
            resolution = (
                "EXECUTED_CFG_UNIQUE_DEPTH_0x28;STACK_LOCAL_RECEIVER_ENTRY_SP_MINUS_0x14;"
                "HELPER_WRITE_ENTRY_SP_MINUS_0x10;NO_STREAM_FORMAL"
            )
        elif site == DIRECT_INVALID_SITE:
            change_type = "NONWIRE_STACK_NEUTRAL_INVALID_PARAMETER_GUARD"
            resolution = (
                "EXACT_PE_IMPORT;EXECUTED_CFG_UNIQUE_DEPTH_0x28;"
                "STACK_NEUTRAL_INVALID_PARAMETER_GUARD"
            )
        else:
            change_type = "NONWIRE_STACK_NEUTRAL_INVALID_PARAMETER_GUARD"
            resolution = (
                "EXACT_PE_IMPORT;SINGLETON_EBP_IAT_REACHING_DEFINITION;"
                "EXECUTED_CFG_UNIQUE_DEPTH_0x28;STACK_NEUTRAL_INVALID_PARAMETER_GUARD"
            )
        values = {
            "action": "REMOVE_OVERLAY_NONWIRE_ROW",
            "change_type": change_type,
            "base_file": SLOT34_A2_NAME, "base_line": str(line),
            "base_row_key": row_key, "base_delta_key": source_key,
            "message": "DailyActivityState", "direction(W/R)": direction,
            "old_order": order, "old_tag": tag, "old_field_offset": blocker,
            "old_len": "N/A", "new_wire_order": "N/A", "new_tag": "N/A",
            "new_field_offset": "N/A", "new_len": "N/A",
            "new_gate_condition": "N/A", "resolution": resolution,
            "evidence_ticket": EVIDENCE_TICKET,
            "evidence_span_start": "0x0069CB20", "evidence_span_end": "0x0069CC63",
            "evidence_span_sha256": SERIALIZER_SHA256,
            "evidence_file_off": f"0x{site - 0x00400C00:08X}", "source": "IMAGE",
        }
        values["delta_key"] = make_delta_key(
            ("A2", values["action"], values["base_file"], values["base_line"], row_key)
        )
        output.append(values)

    if len(output) != 12 or Counter(row["direction(W/R)"] for row in output) != Counter({"W": 6, "R": 6}):
        raise BuildError("Daily A2 removal census drift")
    if len({row["delta_key"] for row in output}) != 12:
        raise BuildError("duplicate Daily A2 delta_key")
    if any(row["delta_key"] in prior_keys for row in output):
        raise BuildError("Daily A2 delta_key collides with prior provenance")

    selected_keys = {row["base_delta_key"] for row in output}
    residual = {
        direction: [
            value for value in effective[("DailyActivityState", direction)]
            if value.evidence_key not in selected_keys
        ]
        for direction in ("W", "R")
    }
    if {direction: len(values) for direction, values in residual.items()} != {"W": 6, "R": 6}:
        raise BuildError("Daily residual field census drift")
    residual_reasons = {
        direction: {
            value.evidence_key: effective_field_unknown_reasons(value, residual[direction], v3.v2)
            for value in residual[direction]
        }
        for direction in ("W", "R")
    }
    if any(reasons for direction in residual_reasons.values() for reasons in direction.values()):
        raise BuildError(f"Daily residual effective schema remains OPEN: {residual_reasons}")
    verify_closure_predicate_mutation_controls(residual, v3.v2)
    if any(all(value.tag == "EMPTY" for value in values) for values in residual.values()):
        raise BuildError("Daily residual direction lacks a non-empty field")

    # The two 0x00652A30 rows were already delivered; they must not be repeated.
    _old_fields, old_rows = read_tsv_with_lines(external / TARGET_652A30_NAME)
    old_daily = [row for _line, row in old_rows if row.get("message") == "DailyActivityState"]
    if len(old_daily) != 2 or {row["base_line"] for row in old_daily} != {"1003", "1004"}:
        raise BuildError("older Daily 0x00652A30 removal census drift")
    if selected_keys & {row["base_delta_key"] for row in old_daily}:
        raise BuildError("new Daily removal repeats older 0x00652A30 work")
    return output, {"W": len(residual["W"]), "R": len(residual["R"])}


def build_priority_delta(external: Path, a2_rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    fields, rows = read_tsv_with_lines(external / SLOT34_PRIORITY_NAME)
    hits = [(line, row) for line, row in rows if row.get("message") == "DailyActivityState"]
    if len(hits) != 1:
        raise BuildError("Daily slot34 Priority predecessor census drift")
    line, row = hits[0]
    row_key = canonical_row_key(fields, row)
    expected = {
        "delta_key": "c4d24d899578ad584b3b13e3f81f4aa051f77f9380ea0c893929080434f8e017",
        "action": "CHANGED", "message": "DailyActivityState", "priority": "3",
        "new_registry_identity_status": "KNOWN", "new_registry_identity_missing": "N/A",
        "new_serializer_status": "OPEN",
        "new_serializer_blockers": "direct_call_not_proven_serializer | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | mutable_chain_target_object_alias_unproved",
        "new_structural_status": "OPEN",
        "new_blocker": "direct_call_not_proven_serializer | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | mutable_chain_target_object_alias_unproved",
        "source": "IMAGE",
    }
    if line != 15 or row_key != "c18d6d65a771b97b112ca8f1d7062c4d204bf8cb9bb87a6a22794737a8b6af13":
        raise BuildError("Daily slot34 Priority line/key drift")
    if any(row.get(name) != value for name, value in expected.items()):
        raise BuildError("Daily slot34 Priority predecessor content drift")
    # No later pre-existing Priority overlay may already touch DailyActivityState.
    occurrences = []
    for path in sorted(external.glob("PF_PRIORITY_*_DELTA.tsv")):
        if path.name == PRIORITY_OUTPUT_NAME:
            continue
        _headers, candidate_rows = read_tsv_with_lines(path)
        for candidate_line, candidate in candidate_rows:
            if candidate.get("message") == "DailyActivityState":
                occurrences.append((path.name, candidate_line))
    if occurrences != [(SLOT34_PRIORITY_NAME, 15)]:
        raise BuildError(f"Daily Priority predecessor is not current/unique: {occurrences}")
    if len(a2_rows) != 12:
        raise BuildError("Priority close lacks exact 12-row A2 proof")
    values = {
        "action": "CHANGED", "base_file": SLOT34_PRIORITY_NAME,
        "base_line": str(line), "base_row_key": row_key,
        "base_delta_key": row["delta_key"], "message": "DailyActivityState",
        "priority": "3", "old_registry_identity_status": "KNOWN",
        "new_registry_identity_status": "KNOWN", "old_registry_identity_missing": "N/A",
        "new_registry_identity_missing": "N/A", "old_serializer_status": "OPEN",
        "new_serializer_status": "CLOSED", "old_serializer_blockers": row["new_serializer_blockers"],
        "new_serializer_blockers": "N/A", "old_structural_status": "OPEN",
        "new_structural_status": "CLOSED", "old_blocker": row["new_blocker"],
        "new_blocker": "N/A", "evidence_ticket": EVIDENCE_TICKET,
        "closure_scope": (
            "STATIC_WIRE_STRUCTURE_ONLY;EXECUTED_CFG_STACK_DEPTH;"
            "STACK_LOCAL_NONALIAS;SLOT34_CHAINED;V1_IMMUTABLE"
        ),
        "source": "IMAGE",
    }
    values["delta_key"] = make_delta_key(
        ("PRIORITY", values["action"], values["base_file"], values["base_line"], row_key)
    )
    prior_keys, _targets = prior_keys_and_targets(external)
    if values["delta_key"] in prior_keys:
        raise BuildError("Daily Priority delta_key collides with prior provenance")
    return [values]


def report_text(
    a2_rows: Sequence[Mapping[str, str]], priority_rows: Sequence[Mapping[str, str]],
    residual: Mapping[str, int], wire_counts: Mapping[int, int],
) -> str:
    physical = sorted({int(row["evidence_file_off"], 16) + 0x00400C00 for row in a2_rows})
    lines = [
        "# PF IMAGE closure: DailyActivityState non-wire rows",
        "",
        "[MEASURED] IMAGE-only additive correction built from the exact effective V3 A2.",
        "",
        "## Outcome",
        "",
        "- Removed 12 effective UNKNOWN analysis rows: 6 W + 6 R over exactly 6 physical sites.",
        "- DailyActivityState Priority 3 changes OPEN -> CLOSED for serializer and structural status.",
        "- Residual effective schema has 6 W + 6 R rows, zero UNKNOWN reasons, and non-empty fields in both directions.",
        "- Closure is gated by one executable predicate over tag, offset, length, order, gate, and subcall flattening; built-in mutations of all six dimensions are rejected.",
        "- source=IMAGE on every emitted TSV row; no capture, dump, data, runtime, or server claim is mixed in.",
        "- Duplicate accounting: 0 repeated base targets, 0 prior provenance-key collisions, and 0 unchanged/copied rows.",
        "",
        "## Exact proof boundary",
        "",
        "| role | VA span | bytes | file offset | SHA-256 | executed CFG |",
        "|---|---|---:|---:|---|---|",
        f"| DailyActivityState serializer | `0x{SERIALIZER_START:08X}-0x{SERIALIZER_END:08X}` | {SERIALIZER_END-SERIALIZER_START} | `0x{SERIALIZER_OFF:08X}` | `{SERIALIZER_SHA256}` | 117 nodes / 126 edges / 0 errors |",
        f"| stack-local link-state helper | `0x{HELPER_START:08X}-0x{HELPER_END:08X}` | {HELPER_END-HELPER_START} | `0x{HELPER_OFF:08X}` | `{HELPER_SHA256}` | 44 nodes / 49 edges / 0 errors |",
        "",
        "The complete serializer stack fixed point has one entry-relative depth at every decoded node. All six reviewed sites have depth 0x28. The only semantic ESP-LEA override is exact bytes `8D642400` at `0x0069CB6C`, which is the identity `ESP := ESP+0`. The EBP proof carries an explicit entry-undefined sentinel and separately requires `0x0069CB90` to dominate all four register-indirect calls, so a bypass path cannot disappear at a set union.",
        "",
        "| physical site | classification | entry-relative stack depth | rows removed |",
        "|---:|---|---:|---:|",
        "| `0x0069CB82` | direct PE import `MSVCR90.dll!_invalid_parameter_noinfo` | `0x28` | 2 |",
        "| `0x0069CB9A` | EBP call; singleton IAT definition `0x0069CB90` | `0x28` | 2 |",
        "| `0x0069CBA3` | EBP call; singleton IAT definition `0x0069CB90` | `0x28` | 2 |",
        "| `0x0069CBB8` | EBP call; singleton IAT definition `0x0069CB90` | `0x28` | 2 |",
        "| `0x0069CBBF` | EBP call; singleton IAT definition `0x0069CB90` | `0x28` | 2 |",
        "| `0x0069CBD4` | stack-local receiver into helper `0x00B0BF70` | `0x28` | 2 |",
        "",
        "At `0x0069CBD0`, `lea ecx,[esp+0x14]` at depth 0x28 proves receiver `entry_SP-0x14`. The helper copies entry ECX to ESI, and its exact three explicit writes (`0x00B0BFAB`, `0x00B0BFC8`, `0x00B0BFD7`) are all `[ESI+4]`, therefore target `entry_SP-0x10`. The helper receives no stack argument or stream formal; this local target is structurally distinct from the stream formal slot at `entry_SP+0x04` and the entry object receiver.",
        "",
        "Both helper guard calls have the singleton reaching EDI definition from `[0x00C3B4C0]`, which PE metadata resolves to `_invalid_parameter_noinfo`. The helper graph has 0 direct wire-primitive intersections and 0 wire-address literal hits.",
        "",
        f"Whole-image raw E8 destination census remains `{wire_counts[WIRE_WRITE]}` calls to `0x{WIRE_WRITE:08X}` and `{wire_counts[WIRE_READ]}` calls to `0x{WIRE_READ:08X}`. This census is a negative-control boundary, not a reason to remove unrelated rows.",
        "",
        "## Prior result not duplicated",
        "",
        "The two DailyActivityState rows at physical call `0x0069CC4C -> 0x00652A30` (slot34 lines 1003/1004) were already removed by `PF_TARGET_652A30_A2_DELTA.tsv`. They are verified as prior effective removals and are not emitted again. This artifact covers only lines 986-999 listed in its TSV.",
        "",
        "## Priority predecessor",
        "",
        "The single Priority row chains from `PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv:15`, canonical row key `c18d6d65a771b97b112ca8f1d7062c4d204bf8cb9bb87a6a22794737a8b6af13`, predecessor delta key `c4d24d899578ad584b3b13e3f81f4aa051f77f9380ea0c893929080434f8e017`. No base-V1 CLOSED row is reused as the predecessor.",
        "",
        "## Nonclaims and stop rule",
        "",
        "- No field meaning, gameplay behavior, runtime state, capture agreement, or server behavior is claimed.",
        "- No other invalid-parameter or mutable-helper row is generalized from this serializer.",
        "- Resume only if the pinned IMAGE/V3 effective inputs change or independent evidence identifies another exact still-effective DailyActivityState blocker.",
        "",
    ]
    if physical != list(TARGET_SITES) or len(priority_rows) != 1 or residual != {"W": 6, "R": 6}:
        raise BuildError("report input census drift")
    return "\n".join(lines)


def atomic_write_bytes(path: Path, data: bytes) -> None:
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp",
            delete=False,
        ) as handle:
            temp_name = handle.name
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name is not None and os.path.exists(temp_name):
            os.unlink(temp_name)


def acquire_lock(parent: Path) -> tuple[Path, bytes]:
    path = parent / PUBLISH_LOCK_NAME
    token = f"pid={os.getpid()};owner={Path(__file__).name}\n".encode("ascii")
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise BuildError(
            f"publisher lock exists (active or stale): {path.name}; resolve ownership before publishing"
        ) from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(token)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        if path.exists():
            path.unlink()
        raise
    if path.read_bytes() != token:
        raise BuildError("publisher lock read-back drift")
    return path, token


def release_lock(path: Path, token: bytes) -> None:
    if not path.exists() or path.read_bytes() != token:
        raise BuildError("publisher lock ownership changed; lock retained")
    path.unlink()


def publish_transaction(outputs: Mapping[Path, bytes]) -> None:
    ordered = list(outputs.items())
    names = [path.name for path, _data in ordered]
    if set(names) != OWN_OUTPUTS or names[-1] != REPORT_NAME:
        raise BuildError(f"owned output set/order drift: {names}")
    parent = ordered[0][0].parent.resolve()
    if any(path.resolve().parent != parent for path, _data in ordered):
        raise BuildError("publish path escapes external directory")
    staged: dict[Path, Path] = {}
    old: dict[Path, bytes | None] = {}
    replaced: list[Path] = []
    lock_path, token = acquire_lock(parent)
    try:
        for path, data in ordered:
            old[path] = path.read_bytes() if path.exists() else None
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=parent, prefix=f".{path.name}.stage.", suffix=".tmp",
                delete=False,
            ) as handle:
                stage = Path(handle.name)
                staged[path] = stage
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            if stage.read_bytes() != data:
                raise BuildError(f"staged output drift: {path.name}")
        for path, _data in ordered:
            replaced.append(path)
            os.replace(staged[path], path)
        for path, data in ordered:
            if path.read_bytes() != data:
                raise BuildError(f"published output drift: {path.name}")
    except BaseException as exc:
        rollback_errors = []
        for path in reversed(replaced):
            try:
                previous = old[path]
                if previous is None:
                    if path.exists():
                        path.unlink()
                else:
                    atomic_write_bytes(path, previous)
            except BaseException as rollback_exc:
                rollback_errors.append(f"{path.name}:{rollback_exc}")
        if rollback_errors:
            raise BuildError(f"publish failed ({exc}); rollback failed: {rollback_errors}") from exc
        raise
    finally:
        for stage in staged.values():
            if stage.exists():
                stage.unlink()
        release_lock(lock_path, token)


def build(external: Path) -> tuple[dict[Path, bytes], str]:
    image_path = external.parent.parent / "GameClient" / "GameClient.local.bin"
    pinned = {
        image_path: IMAGE_SHA256,
        external / DECODER_NAME: DECODER_SHA256,
        external / V2_VALIDATOR_NAME: V2_VALIDATOR_SHA256,
        external / V3_VALIDATOR_NAME: V3_VALIDATOR_SHA256,
        external / V3_MANIFEST_NAME: V3_MANIFEST_SHA256,
        external / SLOT34_A2_NAME: SLOT34_A2_SHA256,
        external / SLOT34_PRIORITY_NAME: SLOT34_PRIORITY_SHA256,
        external / TARGET_652A30_NAME: TARGET_652A30_SHA256,
    }
    before = {path: sha256_path(path) for path in pinned}
    for path, expected in pinned.items():
        if before[path] != expected:
            raise BuildError(f"pinned input changed: {path.name}")
    verify_strict_tsv_mutation_controls()
    v2 = load_module("pf_validate_v2_effective_capture", external / V2_VALIDATOR_NAME, V2_VALIDATOR_SHA256)
    v3 = load_module("pf_daily_v3_validator", external / V3_VALIDATOR_NAME, V3_VALIDATOR_SHA256)
    decoder = load_module("pf_daily_decoder", external / DECODER_NAME, DECODER_SHA256)
    if sha256_path(Path(v3.v2.__file__).resolve()) != V2_VALIDATOR_SHA256:
        raise BuildError("V3 validator dependency is not the pinned V2 module")
    v2.verify_pinned_inputs(external, False)
    v3.verify_v2_module()
    v3.verify_new_inputs(external, False)
    image = decoder.Image(image_path)
    symbol = image.imports_by_iat.get(INVALID_IAT)
    if symbol is None or (
        symbol.dll, symbol.name, symbol.iat_off, symbol.descriptor_off,
        symbol.lookup_off, symbol.dll_name_off, symbol.symbol_name_off,
    ) != (
        "MSVCR90.dll", "_invalid_parameter_noinfo", 0x008398C0,
        0x00C112DC, 0x00C118B4, 0x00C1647C, 0x00C15C62,
    ):
        raise BuildError("invalid-parameter PE import provenance drift")
    if (symbol.dll, symbol.name) not in decoder.STACK_NEUTRAL_IMPORTS:
        raise BuildError("invalid-parameter import lost stack-neutral classification")
    _serializer, _depths = verify_serializer(decoder, image)
    _helper, graph_intersections, literal_hits = verify_helper(decoder, image)
    if graph_intersections or literal_hits:
        raise BuildError("helper wire negative controls failed")
    wire_counts = whole_image_e8_census(image)
    a2_rows, residual = build_a2_delta(external, v3)
    priority_rows = build_priority_delta(external, a2_rows)
    all_keys = [row["delta_key"] for row in (*a2_rows, *priority_rows)]
    if len(all_keys) != len(set(all_keys)):
        raise BuildError("new Daily A2/Priority key collision")
    report = report_text(a2_rows, priority_rows, residual, wire_counts).encode("utf-8")
    after = {path: sha256_path(path) for path in pinned}
    if after != before:
        raise BuildError("pinned IMAGE/input changed during build")
    outputs = {
        external / A2_OUTPUT_NAME: tsv_bytes(A2_COLUMNS, a2_rows),
        external / PRIORITY_OUTPUT_NAME: tsv_bytes(PRIORITY_COLUMNS, priority_rows),
        external / REPORT_NAME: report,
    }
    return outputs, before[image_path]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify existing outputs byte-for-byte")
    parser.add_argument("--audit-only", action="store_true", help="run every proof without publishing")
    parser.add_argument("--external", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    if args.check and args.audit_only:
        raise BuildError("--check and --audit-only are mutually exclusive")
    external = args.external.resolve()
    outputs, image_hash = build(external)
    if args.audit_only:
        print("PASS audit-only DailyActivityState: 12 removals; 6 sites; Priority P3 CLOSED; writes 0")
        return 0
    if args.check:
        for path, expected in outputs.items():
            if not path.exists() or path.read_bytes() != expected:
                raise BuildError(f"byte output drift: {path.name}")
        if sha256_path(external.parent.parent / "GameClient" / "GameClient.local.bin") != image_hash:
            raise BuildError("IMAGE changed during check")
        print("PASS DailyActivityState: 12 removals; duplicate 0; Priority P3 CLOSED")
        return 0
    publish_transaction(outputs)
    if sha256_path(external.parent.parent / "GameClient" / "GameClient.local.bin") != image_hash:
        raise BuildError("IMAGE changed during publication")
    print("WROTE DailyActivityState: 12 removals; duplicate 0; Priority P3 CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
