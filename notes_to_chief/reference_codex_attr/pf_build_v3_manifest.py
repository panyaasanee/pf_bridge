#!/usr/bin/env python3
"""Build and verify the duplicate-safe PF V3 local checkpoint.

The manifest is the commit marker, not an assertion that a partial directory is
valid. One O_EXCL lock covers snapshot, component checks, staging, CAS,
publication, full re-derivation and backup disposal. A crash leaves a lock or
transaction directory which ordinary checks reject rather than taking over.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Iterator, Mapping, Sequence


# Before any local-component import. Child checks also receive -B and the env
# switch. A pre-existing cache is rejected, never silently ignored or deleted.
sys.dont_write_bytecode = True

OUT_DIR = Path(__file__).resolve().parent
INDEX_PATH = OUT_DIR / "00_SEARCH_HERE_FIRST.md"
MANIFEST_PATH = OUT_DIR / "PF_V3_MANIFEST.md"
V2_MANIFEST_PATH = OUT_DIR / "PF_V2_MANIFEST.md"
LOCK_PATH = OUT_DIR / ".PF_V3_MANIFEST_PUBLISH.lock"
TRANSACTION_PREFIX = ".PF_V3_MANIFEST_TXN."
IMAGE_PATH = OUT_DIR.parent.parent / "GameClient" / "GameClient.local.bin"
IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
V2_MANIFEST_SHA256 = "e43d0c73323de0c69ec14ae6a3fb4717458f8a3896be25e4054da68590ea2f06"
V2_INDEX_SOURCE_SHA256 = "d3638942030a6aa5a8be20e13cec56b2a9e85eefbed5414068a949cb0fc63d56"
V2_INDEX_TAIL_SHA256 = "3e799aa845521a44f7fe47ca00536e46abaa3463aa022c82fea83d6cfdae3181"
CANONICAL_A5_TSV = "PF_V2_FIELD_VALIDATION.tsv"
CANONICAL_A5_SHA256 = "10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806"
FORBIDDEN_DUPLICATE_A5_TSV = "PF_V3_FIELD_VALIDATION.tsv"
ALLOWED_SOURCES = {"IMAGE", "DUMP", "CAPTURE", "DATA"}
KEY_COLUMNS = ("delta_key", "dedup_key", "root_key", "status_key", "validation_key")
# References may repeat. They do not assert new owned identities; the component
# checks bind A2/status references to their exact predecessor lines and keys.
REFERENCE_KEY_COLUMNS = {"base_row_key", "base_delta_key", "effective_schema_key"}
DERIVED_STATUS_SEMANTICS = "DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW"
ALLOWED_STATUS_REFERENCE_FILES = {"PF_V2_P1_OPEN.tsv", "PF_V3_P1_OPEN.tsv"}
EXPECTED_INHERITED_STATUS_KEYS = 95
V2_TABLE_RE = re.compile(
    r"^\| `([^`]+)` \| (\d+) \| `([0-9A-F]{64})` \|", re.MULTILINE
)
NEW_A2_COUNTS = {
    "PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv": 48,
    "PF_A2_TARGETS_6564E0_656C50_6FDB40_NONWIRE_DELTA.tsv": 32,
    "PF_A2_TARGET_656690_NONWIRE_DELTA.tsv": 4,
    "PF_A2_ITERATOR_HELPERS_NONWIRE_DELTA.tsv": 40,
}
V3_FILES = {
    "pf_build_compiler_runtime_target_6564_closure.py", *NEW_A2_COUNTS,
    "PF_PRIORITY_COMPILER_TARGET_6564_DELTA.tsv",
    "PF_COMPILER_RUNTIME_TARGET_6564_CLOSURE.md",
    "pf_build_iterator_helpers_nonwire.py", "PF_ITERATOR_HELPERS_NONWIRE.md",
    "pf_build_v3_effective_status.py", "PF_V3_P1_OPEN.tsv", "PF_V3_EFFECTIVE_STATUS.md",
    "pf_validate_v3_effective_capture.py", "PF_V3_FIELD_VALIDATION.md",
    "PF_V3_HANDOFF.md", "pf_build_v3_manifest.py", "PF_V3_MANIFEST.md",
}
COMPONENT_CHECKS = (
    "pf_build_compiler_runtime_target_6564_closure.py",
    "pf_build_iterator_helpers_nonwire.py",
    "pf_build_v3_effective_status.py",
    "pf_validate_v3_effective_capture.py",
)
REVIEWED_V3_PINS = {
    "pf_build_compiler_runtime_target_6564_closure.py": "bf7dd51598eef0d1c5db15c600af17265d3eda651dafa79cdde70059795b103f",
    "pf_build_iterator_helpers_nonwire.py": "cc9e73047fd2442961a59be5885740e7a40010cd3c4a1e0a40b85360127d2b22",
    "pf_build_v3_effective_status.py": "aff946ac806826b5516203d582672d88577c9f99c3e96c72fc191232bda000b9",
    "pf_validate_v3_effective_capture.py": "3d145407c9a6e4236eefe829c9fb9eb0757bf53cce9ac9cb136f201f594a360b",
    "PF_V3_HANDOFF.md": "2a1534a64b98e31d3b9574e89a47ce3584586c33dd41e90103d9faa37b3ec43a",
}
EXPECTED_CANDIDATES = {
    ("ItemAttr", "R", "VTABLE_0x00F0EBB0"): 13,
    ("ItemAttr", "W", "VTABLE_0x00F0EBB0"): 13,
    ("ItemAttr", "R", "VTABLE_0x00F4A188"): 15,
    ("ItemAttr", "W", "VTABLE_0x00F4A188"): 15,
}
EXPECTED_CANDIDATE_TOTALS = {"VTABLE_0x00F0EBB0": 8697, "VTABLE_0x00F4A188": 8701}
EXPECTED_PLAN_CENSUS = {"APPLICABLE": 620, "SCHEMA_NOT_APPLIED": 46, "STATIC_OPEN": 372}
# Measured V3 replay, not targets. Identical TSV bytes remain canonical in V2.
EXPECTED_A5 = {
    "rows": 66, "parse_success": 22965, "static_open": 78532,
    "schema_not_applied": 0, "mismatch": 386, "mismatch_points": 4,
    "field_locations": 3,
}
A2_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line", "base_row_key",
    "base_delta_key", "message", "direction(W/R)", "old_order", "old_tag",
    "old_field_offset", "old_len", "new_wire_order", "new_tag", "new_field_offset",
    "new_len", "new_gate_condition", "resolution", "evidence_ticket",
    "evidence_span_start", "evidence_span_end", "evidence_span_sha256",
    "evidence_file_off", "source",
)
PRIORITY_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key", "base_delta_key",
    "message", "priority", "old_registry_identity_status", "new_registry_identity_status",
    "old_registry_identity_missing", "new_registry_identity_missing",
    "old_serializer_status", "new_serializer_status", "old_serializer_blockers",
    "new_serializer_blockers", "old_structural_status", "new_structural_status",
    "old_blocker", "new_blocker", "evidence_ticket", "closure_scope", "source",
)
STATUS_COLUMNS = (
    "status_key", "message", "priority", "matched_groups", "matched_keywords",
    "base_line", "base_registry_identity_status", "effective_registry_identity_status",
    "effective_registry_identity_missing", "base_serializer_status",
    "effective_serializer_status", "base_structural_status", "effective_structural_status",
    "primary_blocker_group", "effective_blocker", "applied_overlay_chain", "row_semantics", "source",
)
A5_COLUMNS = (
    "validation_key", "message", "direction(W/R)", "schema_variant", "effective_schema_key",
    "observed_frames", "observed_instances", "baseline_observed_instances",
    "new_observed_instances", "parse_success_frames", "parse_success_instances",
    "baseline_parse_success_instances", "new_parse_success_instances", "static_open_frames",
    "static_open_instances", "baseline_static_open_instances", "new_static_open_instances",
    "static_open_reason_count", "schema_not_applied_frames", "schema_not_applied_instances",
    "baseline_schema_not_applied_instances", "new_schema_not_applied_instances",
    "schema_not_applied_reason_count", "mismatch_frames", "mismatch_instances",
    "baseline_mismatch_instances", "new_mismatch_instances",
    "mismatch_field_identity_reason_count", "record_instances_observed",
    "record_branch_coverage", "capture_file_count", "status", "content_dedup_scope", "source",
)
EXACT_SCHEMAS = {
    **{name: A2_COLUMNS for name in NEW_A2_COUNTS},
    "PF_PRIORITY_COMPILER_TARGET_6564_DELTA.tsv": PRIORITY_COLUMNS,
    "PF_V3_P1_OPEN.tsv": STATUS_COLUMNS, CANONICAL_A5_TSV: A5_COLUMNS,
}
EXACT_SOURCE_SETS = {
    **{name: {"IMAGE"} for name in NEW_A2_COUNTS},
    "PF_PRIORITY_COMPILER_TARGET_6564_DELTA.tsv": {"IMAGE"},
    "PF_V3_P1_OPEN.tsv": {"IMAGE"}, CANONICAL_A5_TSV: {"CAPTURE"},
}
RAW_BYTE_PATTERNS = (
    re.compile(r"(?:^|\s)(?:[0-9A-Fa-f]{2}\s+){7,}[0-9A-Fa-f]{2}(?:\s|$)"),
    re.compile(r"(?:\\x[0-9A-Fa-f]{2}){4,}"),
    re.compile(r"(?:0x[0-9A-Fa-f]{2}\s*,\s*){7,}0x[0-9A-Fa-f]{2}\b"),
    re.compile(r"data:[^\s]*;base64,", re.IGNORECASE),
    re.compile(r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{96,}={0,2}(?![A-Za-z0-9+/])"),
)

# Literal from the complete V2-index SHA pin above. Never inherit mutable tail
# text from the current index and thereby let its edits authenticate themselves.
V2_INDEX_TAIL_TEXT = r"""> ### 🔴 โฟลเดอร์ไหนเก็บอะไร — กฎตัดสินประโยคเดียว (2026-08-24)
> **ถอดมาจากอิมเมจ `GameClient.local.bin` (โค้ดที่เกม *รัน*) → `pf_bridge\external\`**
> **ถอดมาจากไฟล์ข้อมูลเกม `.pc_` / `.lu_` / `.npc` (เนื้อหาที่เกม *อ่าน*) → `pf_bridge\gamedata\`**
> 🔴 `.pc_` และ `.lu_` ใช้ `$pcz`+LZMA · **`.npc` ไม่ถูกบีบอัด** เป็นไบนารีเปล่า
> โครง: `u16 version` → `u16 **definition_count**` → นิยาม NPC set → `u16 **placement_count**` → เรกคอร์ด `NPCPlacement` (มี XYZ)
> ⚠️ `u16` ตัวที่สอง **ไม่ใช่** placement count (ผู้ช่วยเคยอ่านผิดจุดนี้ 2026-08-24) · placement จริงรวม 6,248 · definition รวม 3,745
> ตัวเลขต่อฉากอ่านจาก `gamedata\PF_GAMEDATA_SCENE_INDEX.tsv`
> เกณฑ์แบ่งบ้านคือ **ถอดมาจากไหน** ไม่ใช่ **บีบอัดด้วยอะไร**
> ⚠️ ชื่อ `external\` บอกว่า *ใครทำ* ไม่ได้บอกว่า *มันคืออะไร* — ชื่อที่ตรงคือ `clientbin\`
> **ห้ามเปลี่ยนชื่อจนกว่า GT-054 จะผ่าน** (`tools\pf_external_registry.py` ฮาร์ดโค้ด `pf_bridge\external` ไว้)


**V1 core ของโฟลเดอร์นี้มี 8 ตาราง รวม 17,626 แถว; ผลล่าสุด V2 อยู่ในรูป additive overlays + derived indexes + manifest ตามรายการด้านบน**
มันแกะไคลเอนต์ไปแล้วเป็นวัน ๆ และ **คำตอบของคำถามหลายข้อที่เรากำลังจะเปิดใบใหม่ อยู่ในนี้แล้ว**

## กติกาข้อเดียวที่ต้องทำทุกครั้ง

> **ก่อนเริ่มงาน static ใด ๆ: `grep` หาชื่อ message / ชื่อคลาส / VA ที่สนใจในโฟลเดอร์นี้ก่อนเสมอ**
> แล้วเขียนในจดหมายว่า **"ค้นชุดส่งมอบแล้ว เจอ / ไม่เจอ"** — บังคับทุกใบ

**ทำไมกฎนี้ถึงเกิด (เรื่องจริง 2026-08-23):** ผู้ช่วยร่างใบ GT-050 ว่า *"ให้ไปถอด serializer ของ `TriggerCastSkillVital`"*
แล้วอีก 20 นาทีต่อมาเปิดไฟล์ในโฟลเดอร์นี้ **พบว่ามันถอดไว้ครบแล้ว** ทั้ง VA · span · sha256 · ฟิลด์ทั้งสามช่อง
⇒ เกือบสั่งให้คนไปทำงานซ้ำที่ทำเสร็จแล้ว **ถ้าคุณเริ่มเซสชันใหม่และไม่รู้เรื่องนี้ คุณจะพลาดแบบเดียวกัน**

---

## มีอะไรอยู่ในนี้บ้าง

| ไฟล์ | แถว | ใช้ตอบคำถามอะไร |
|---|---|---|
| **`PF_PROTOCOL_REGISTRY.tsv`** | **519** | **ทุก message ในเกม** — ชื่อ + `vtable_va` + `serializer_va` + `handler_va` + `getter_va` + file offset ครบ ⇒ *"ข้อความชื่อนี้อยู่ที่ VA ไหน"* |
| **`PF_SERIALIZER_FIELDS.tsv`** | **6,931** | **ฟิลด์ของทุก message** — `tag` · `field_offset` · `len` · ทิศทาง W/R · `span_start/end` · `span_sha256` ⇒ *"ข้อความนี้มีกี่ฟิลด์ อยู่ออฟเซ็ตไหน ยาวเท่าไร"* |
| `PF_PROTOCOL_PRIORITY.tsv` | 519 | สถานะความพร้อมของแต่ละ message — อันไหนถอดครบ อันไหนติดอะไร |
| `PF_FIELD_VALIDATION.tsv` | 1,038 | เอา schema ไปทาบ capture จริงแล้วผ่านกี่เฟรม · `mismatch` · `A2_STATIC_OPEN` |
| `PF_RUNTIME_CLASSMAP.tsv` | 6,244 | vtable -> ชื่อคลาส (จาก dump) · 🔴 `class_name` เป็น UNKNOWN เกือบ 100% |
| `PF_INPUT_INVENTORY.tsv` | 2,066 | บัญชีไฟล์ input ที่แช่แข็งไว้ (capture 1,772 ไฟล์) + sha256 |
| `PF_DATA_EVIDENCE.tsv` | 290 | ไฟล์ข้อมูลในเกมที่ parse แล้ว |
| `PF_TAG_CENSUS.tsv` | 11 | ความหมายของ `tag` แต่ละตัว + ความถี่ + ตัวอย่าง |

**ไฟล์ `.md` ชื่อเดียวกัน = คำอธิบายของตารางนั้น** · `PF_HANDOFF_V1.md` (32 KB) และ `PF_EXTERNAL_REPORT.md` (49 KB) = รายงานเต็ม
**สคริปต์ `pf_*.py` ในโฟลเดอร์นี้ = ตัวที่สร้างตารางพวกนี้** ⇒ **re-derive ได้เอง** (GT-042 พิสูจน์แล้วว่าออกมาไบต์ต่อไบต์เท่าเดิม)

---

## ท่าค้นที่ใช้ได้เลย

```powershell
# 1) message ชื่อนี้มีอยู่ไหม อยู่ VA ไหน
Select-String -Path PF_PROTOCOL_REGISTRY.tsv -Pattern "Skill"

# 2) ฟิลด์ของ message ตัวนี้มีอะไรบ้าง
Select-String -Path PF_SERIALIZER_FIELDS.tsv -Pattern "^TriggerCastSkillVital"

# 3) เคยเอาไปทาบ capture แล้วผลเป็นยังไง
Select-String -Path PF_FIELD_VALIDATION.tsv -Pattern "TriggerCastSkill"

# 4) tag ตัวนี้แปลว่าอะไร
Get-Content PF_TAG_CENSUS.tsv
```

**ตัวอย่างผลจริง** — `TriggerCastSkillVital` ค้นเจอทันทีโดยไม่ต้องเปิด disassembler:
```
serializer_va 0x00600A60 · handler_va 0x00601810 · vtable_va 0x00F3175C
span [0x00600A60,0x00600AD7) sha 396200629ab4082b8eef730dda809124f5df8eca6f0ced5419d7a2ac7e3500ec
  #1 tag 0x0F @ +0x14 len 2
  #2 tag 0x08 @ +0x16 len 1
  #3 tag 0x14 @ +0x18 len 4
```

---

## 🔴 สิ่งที่ตารางพวกนี้ **ไม่ได้** บอก — อย่าเข้าใจผิด

1. **ไม่บอกทิศทางจริง** — มีทั้งแถว `W` และ `R` เพราะ serializer ตัวเดียวทำสองทาง
   **ไม่ได้แปลว่าไคลเอนต์ส่งจริง** ⇒ ต้องไล่ผู้เรียกเองว่าเข้าสตรีมผ่าน `0x0089A600` (W) หรือ `0x0089A640` (R) — แบบที่ GT-046 ทำ
2. **ไม่บอกตัวจุดชนวน** — ว่าอะไรทำให้ข้อความถูกส่ง (คลิกเมาส์? timer? entity update?) ต้องไล่เอง
3. **ไม่บอกความหมายของฟิลด์** — รู้ว่า `tag 0x0F len 2` แต่ไม่รู้ว่ามันคือ skill id หรืออะไร **ห้ามเดา**
4. **`PF_RUNTIME_CLASSMAP` แทบไม่มีชื่อคลาส** — 6,244 แถว `class_name` เป็น `UNKNOWN` เกือบหมด
5. **ยังต้อง verify ก่อนพึ่งเสมอ** — เทียบ `span_sha256` กับอิมเมจจริงก่อน ถ้าไม่ตรงแม้ตัวเดียว **หยุดแล้วรายงาน**
   *(ตารางนี้เป็นงานของคนอื่น ต้องผ่านปฏิปักษ์ก่อน — GT-042 ผ่านแล้วครั้งหนึ่ง แต่กติกายังบังคับให้เช็คทุกครั้งที่พึ่ง)*

## สถานะการใช้งาน ณ 2026-08-23

- ✅ ผ่าน re-derive ปฏิปักษ์แล้ว (GT-042 · ไบต์ต่อไบต์)
- 🟡 `pf_validate_capture_fields.py` **มีช่องโหว่** — มันยอมรับการกลายพันธุ์ `field_offset` (GT-047) ⇒ **ห้ามใช้ผล validator ตัวเดียวเป็นเหตุผลเลื่อนขั้น schema**
- 🔴 **ยังไม่มีโค้ดใน `src/` `tools/` `tests/` อ่านไฟล์พวกนี้เลยแม้แต่บรรทัดเดียว** — ข้อห้าม "ห้ามเขียนโมดูล/encoder" เพิ่งปลดเมื่อ 2026-08-23 02:03
"""


class ManifestError(RuntimeError):
    pass


@dataclass(frozen=True)
class Snapshot:
    expected: frozenset[str]
    files: Mapping[str, bytes]
    v2_hashes: Mapping[str, tuple[int, str]]
    image_fingerprint: tuple[int, str]

    def text(self, name: str) -> str:
        try:
            text = self.files[name].decode("utf-8")
        except (KeyError, UnicodeDecodeError) as exc:
            raise ManifestError(f"missing/non-UTF-8 snapshot artifact: {name}") from exc
        if "\x00" in text:
            raise ManifestError(f"NUL in textual artifact: {name}")
        return text


@dataclass
class HeldLock:
    descriptor: int
    payload: bytes
    retain: bool = False


@dataclass(frozen=True)
class Audit:
    snapshot: Snapshot
    census: Mapping[str, tuple[int, Counter[str]]]
    a5: Mapping[str, int]
    effective: Mapping[str, int]
    inherited_status_keys: int
    final_index: str


def assert_held_lock(held: HeldLock) -> None:
    if not LOCK_PATH.exists() or LOCK_PATH.read_bytes() != held.payload:
        held.retain = True
        raise ManifestError("publication lock identity changed while held")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def image_fingerprint() -> tuple[int, str]:
    data = IMAGE_PATH.read_bytes()
    return len(data), sha256_bytes(data)  # Same read supplies both size and hash.


@contextmanager
def exclusive_lock() -> Iterator[HeldLock]:
    try:
        descriptor = os.open(LOCK_PATH, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise ManifestError(
            f"active/stale publication lock exists: {LOCK_PATH.name}; no automatic takeover"
        ) from exc
    payload = json.dumps(
        {"pid": os.getpid(), "token": os.urandom(16).hex(), "scope": "PF_V3_MANIFEST"},
        sort_keys=True,
    ).encode("utf-8") + b"\n"
    held = HeldLock(descriptor, payload)
    try:
        with os.fdopen(os.dup(descriptor), "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        yield held
    finally:
        os.close(descriptor)
        if not held.retain:
            if not LOCK_PATH.exists() or LOCK_PATH.read_bytes() != payload:
                raise ManifestError("publication lock was removed/replaced while held")
            LOCK_PATH.unlink()


def parse_v2_hashes(data: bytes) -> dict[str, tuple[int, str]]:
    if sha256_bytes(data) != V2_MANIFEST_SHA256:
        raise ManifestError("frozen V2 manifest changed")
    found = V2_TABLE_RE.findall(data.decode("utf-8"))
    if len(found) != 82 or len({name for name, _size, _digest in found}) != 82:
        raise ManifestError(f"V2 manifest table census/uniqueness changed: {len(found)}")
    rows = {name: (int(size), digest.lower()) for name, size, digest in found}
    if rows.get(INDEX_PATH.name) != (11504, V2_INDEX_SOURCE_SHA256):
        raise ManifestError("frozen V2 index source pin changed")
    for name in rows:
        if Path(name).name != name or "/" in name or "\\" in name:
            raise ManifestError(f"non-local manifest member: {name}")
    return rows


def expected_files(v2_hashes: Mapping[str, tuple[int, str]]) -> set[str]:
    expected = set(v2_hashes) | {V2_MANIFEST_PATH.name} | V3_FILES
    if FORBIDDEN_DUPLICATE_A5_TSV in expected:
        raise ManifestError("V3 cannot publish an unchanged copy of the canonical A5 TSV")
    if len(expected) != len({name.casefold() for name in expected}):
        raise ManifestError("case-insensitive namespace collision")
    return expected


def verify_namespace(
    expected: set[str] | frozenset[str], *, manifest_may_be_absent: bool,
    transients: frozenset[str],
) -> None:
    # Only this locked operation's exact paths may be transient. Existing
    # caches/other locks/stale journals/transaction directories fail closed.
    if LOCK_PATH.name not in transients:
        raise ManifestError("namespace audit requires the held publication lock")
    for name in transients - {LOCK_PATH.name}:
        if not name.startswith(TRANSACTION_PREFIX) or Path(name).name != name:
            raise ManifestError(f"invalid active transaction namespace: {name}")
    entries = list(OUT_DIR.iterdir())
    actual = {path.name for path in entries}
    if len(actual) != len({name.casefold() for name in actual}):
        raise ManifestError("case-insensitive output namespace collision")
    for path in entries:
        if path.is_symlink() or path.resolve().parent != OUT_DIR:
            raise ManifestError(f"symlink/reparse/nonlocal output: {path.name}")
        if path.name in transients - {LOCK_PATH.name}:
            if not path.is_dir():
                raise ManifestError(f"transaction path is not a directory: {path.name}")
        elif not path.is_file():
            raise ManifestError(f"unexpected directory/non-file: {path.name}")
    accepted = {frozenset(expected | transients)}
    if manifest_may_be_absent:
        accepted.add(frozenset((expected - {MANIFEST_PATH.name}) | transients))
    if frozenset(actual) not in accepted:
        wanted = expected | transients
        raise ManifestError(
            f"namespace mismatch: missing={sorted(wanted - actual)} extra={sorted(actual - wanted)}"
        )


def take_snapshot(*, manifest_may_be_absent: bool, transients: frozenset[str]) -> Snapshot:
    v2_bytes = V2_MANIFEST_PATH.read_bytes()
    v2_hashes = parse_v2_hashes(v2_bytes)
    expected = frozenset(expected_files(v2_hashes))
    verify_namespace(expected, manifest_may_be_absent=manifest_may_be_absent, transients=transients)
    contents = {V2_MANIFEST_PATH.name: v2_bytes}
    for name in sorted(expected - {V2_MANIFEST_PATH.name}):
        path = OUT_DIR / name
        if name == MANIFEST_PATH.name and manifest_may_be_absent and not path.exists():
            continue
        contents[name] = path.read_bytes()
    snapshot = Snapshot(
        expected, MappingProxyType(contents), MappingProxyType(v2_hashes), image_fingerprint()
    )
    assert_snapshot_current(snapshot, transients=transients)
    return snapshot


def assert_snapshot_current(snapshot: Snapshot, *, transients: frozenset[str]) -> None:
    verify_namespace(
        snapshot.expected, manifest_may_be_absent=MANIFEST_PATH.name not in snapshot.files,
        transients=transients,
    )
    for name in sorted(snapshot.expected):
        path = OUT_DIR / name
        if name not in snapshot.files:
            if path.exists():
                raise ManifestError(f"CAS absent artifact appeared: {name}")
        elif path.read_bytes() != snapshot.files[name]:
            raise ManifestError(f"CAS artifact bytes changed: {name}")
    if image_fingerprint() != snapshot.image_fingerprint:
        raise ManifestError("CAS pinned image changed")


def verify_inputs(snapshot: Snapshot) -> None:
    if snapshot.image_fingerprint != (IMAGE_SIZE, IMAGE_SHA256):
        raise ManifestError("pinned client image changed")
    for name, (size, digest) in snapshot.v2_hashes.items():
        if name == INDEX_PATH.name:
            continue
        data = snapshot.files[name]
        if (len(data), sha256_bytes(data)) != (size, digest):
            raise ManifestError(f"pre-V3 artifact changed: {name}")
    for name, digest in REVIEWED_V3_PINS.items():
        if sha256_bytes(snapshot.files[name]) != digest:
            raise ManifestError(f"reviewed V3 component/handoff changed: {name}")
    if sha256_bytes(V2_INDEX_TAIL_TEXT.encode("utf-8")) != V2_INDEX_TAIL_SHA256:
        raise ManifestError("embedded immutable V2 index tail changed")


def read_tsv(snapshot: Snapshot, name: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        reader = csv.reader(io.StringIO(snapshot.text(name), newline=""), delimiter="\t", strict=True)
        fields = next(reader)
        if not fields or any(not field for field in fields) or len(fields) != len(set(fields)):
            raise ManifestError(f"empty/duplicate TSV header: {name}")
        rows: list[dict[str, str]] = []
        for line, cells in enumerate(reader, start=2):
            # DictReader would silently turn missing/extra cells into None
            # values/keys. Reject both before constructing any row dictionary.
            if len(cells) != len(fields) or any(cell is None for cell in cells):
                raise ManifestError(f"missing/extra TSV cells: {name}:{line}")
            rows.append(dict(zip(fields, cells, strict=True)))
    except (StopIteration, csv.Error) as exc:
        raise ManifestError(f"empty/malformed TSV: {name}") from exc
    return fields, rows


def require_text(snapshot: Snapshot, name: str, snippets: Sequence[str]) -> str:
    text = snapshot.text(name)
    for snippet in snippets:
        if snippet not in text:
            raise ManifestError(f"missing expected text in {name}: {snippet}")
    return text


def normalise_status_reference(row: Mapping[str, str]) -> dict[str, str]:
    normalised = dict(row)
    if "applied_overlay" in normalised:
        normalised["applied_overlay_chain"] = normalised.pop("applied_overlay")
    return normalised


def audit_tsvs(snapshot: Snapshot) -> tuple[dict[str, tuple[int, Counter[str]]], int]:
    census: dict[str, tuple[int, Counter[str]]] = {}
    owners: dict[tuple[str, str], list[tuple[str, dict[str, str]]]] = defaultdict(list)
    cross_namespace: dict[str, str] = {}
    for name in sorted(item for item in snapshot.expected if item.endswith(".tsv")):
        fields, rows = read_tsv(snapshot, name)
        if "source" not in fields:
            raise ManifestError(f"TSV missing source column: {name}")
        if name in EXACT_SCHEMAS and tuple(fields) != EXACT_SCHEMAS[name]:
            raise ManifestError(f"exact TSV schema changed: {name}")
        unknown_keys = {
            field for field in fields if field.endswith("_key")
        } - set(KEY_COLUMNS) - REFERENCE_KEY_COLUMNS
        if unknown_keys:
            raise ManifestError(f"unclassified key namespace: {name}: {sorted(unknown_keys)}")
        sources = Counter(row["source"] for row in rows)
        if not sources or not set(sources).issubset(ALLOWED_SOURCES):
            raise ManifestError(f"invalid/empty TSV sources: {name}: {sources}")
        if name in EXACT_SOURCE_SETS and set(sources) != EXACT_SOURCE_SETS[name]:
            raise ManifestError(f"exact evidence layer changed: {name}: {sources}")
        tuples = [tuple(row[field] for field in fields) for row in rows]
        if len(tuples) != len(set(tuples)):
            raise ManifestError(f"exact duplicate TSV row: {name}")
        for key in KEY_COLUMNS:
            if key not in fields:
                continue
            values = [row[key] for row in rows]
            if any(not value or value == "N/A" for value in values) or len(values) != len(set(values)):
                raise ManifestError(f"invalid/duplicate local {key}: {name}")
            for row in rows:
                value = row[key]
                previous_namespace = cross_namespace.setdefault(value, key)
                if previous_namespace != key:
                    raise ManifestError(f"cross-namespace owned-key collision: {previous_namespace}/{key}")
                owners[(key, value)].append((name, row))
        for action_column in ("action", "delta_action"):
            if action_column in fields:
                for row in rows:
                    if any(token in row[action_column].upper() for token in ("UNCHANGED", "COPIED")):
                        raise ManifestError(f"duplicative delta action: {name}:{row[action_column]}")
        census[name] = (len(rows), sources)
    inherited_status_keys = 0
    for (key, value), occurrences in owners.items():
        if len(occurrences) == 1:
            continue
        if (
            key == "status_key" and len(occurrences) == 2
            and {name for name, _row in occurrences} == ALLOWED_STATUS_REFERENCE_FILES
            and all(
                row.get("row_semantics") == DERIVED_STATUS_SEMANTICS
                and row.get("source") == "IMAGE" for _name, row in occurrences
            )
            and normalise_status_reference(occurrences[0][1])
            == normalise_status_reference(occurrences[1][1])
        ):
            inherited_status_keys += 1
            continue
        raise ManifestError(
            f"unauthorised global {key} duplicate: {value}: {[name for name, _row in occurrences]}"
        )
    if inherited_status_keys != EXPECTED_INHERITED_STATUS_KEYS:
        raise ManifestError(f"inherited derived status-key census changed: {inherited_status_keys}")
    return census, inherited_status_keys


def raw_byte_guard(name: str, text: str) -> None:
    if any(pattern.search(text) for pattern in RAW_BYTE_PATTERNS):
        raise ManifestError(f"raw/opaque byte representation in output: {name}")


def audit_no_raw_proprietary(snapshot: Snapshot) -> None:
    forbidden_columns = {
        "raw_bytes", "payload", "payload_hex", "packet_hex", "hexdump",
        "field_value", "byte_value", "raw_base64", "payload_base64",
    }
    guarded = {CANONICAL_A5_TSV}
    for name in sorted(item for item in snapshot.expected if item.endswith(".tsv")):
        fields, rows = read_tsv(snapshot, name)
        if {row["source"] for row in rows} & {"CAPTURE", "DUMP"}:
            overlap = forbidden_columns & {field.lower() for field in fields}
            if overlap:
                raise ManifestError(f"raw proprietary output column: {name}: {sorted(overlap)}")
            guarded.add(name)
            companion = name.removesuffix(".tsv") + ".md"
            if companion in V3_FILES:
                guarded.add(companion)
    # All V3 prose is guarded, including handoff prose, so renaming a report
    # cannot evade the CAPTURE/DUMP text guard.
    guarded.update(name for name in V3_FILES if name.endswith(".md") and name in snapshot.files)
    for name in sorted(guarded):
        raw_byte_guard(name, snapshot.text(name))
    forbidden_suffixes = {".dmp", ".bin", ".cap", ".pcap", ".pcapng"}
    if {Path(name).suffix.lower() for name in snapshot.expected} & forbidden_suffixes:
        raise ManifestError("proprietary binary included in output namespace")


def audit_duplicate_history(snapshot: Snapshot) -> None:
    _fields, base = read_tsv(snapshot, "PF_SERIALIZER_FIELDS.tsv")
    direct_lines = {
        line: row for line, row in enumerate(base, start=2)
        if row["tag"] == "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL"
    }
    if len(direct_lines) != 638:
        raise ManifestError(f"raw V1 invalid-parameter census changed: {len(direct_lines)}")
    _fields, prior = read_tsv(snapshot, "PF_A2_POST_V1_STATIC_DELTA.tsv")
    prior_direct = [
        row for row in prior if row.get("action", "").startswith("REMOVE")
        and row.get("old_tag") == "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL"
    ]
    if {(row["message"], int(row["base_line"])) for row in prior_direct} != {
        ("CTracePathVital", 5493), ("CTracePathVital", 5494), ("CTracePathVital", 5495),
    } or len(prior_direct) != 3:
        raise ManifestError("the three prior CTracePathVital removals changed")
    _fields, slot = read_tsv(snapshot, "PF_A2_SERIALIZER_SLOT34_DELTA.tsv")
    slot_direct = [
        row for row in slot if row["action"] == "ADD_CORRECTED_SLOT34_ROW"
        and row["new_tag"] == "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL"
    ]
    if len(slot_direct) != 296:
        raise ManifestError(f"slot34 invalid-parameter census changed: {len(slot_direct)}")
    _fields, new = read_tsv(snapshot, "PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv")
    if len(new) != 48 or any(row["old_tag"] != "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL" for row in new):
        raise ManifestError("narrow V3 invalid-parameter set changed")
    split = Counter(row["base_file"] for row in new)
    if split != {"PF_SERIALIZER_FIELDS.tsv": 24, "PF_A2_SERIALIZER_SLOT34_DELTA.tsv": 24}:
        raise ManifestError(f"narrow V3 invalid split changed: {dict(split)}")
    prior_targets = {
        (row["base_file"], row["base_line"], row["base_row_key"])
        for row in prior if row.get("base_row_key") not in {None, "", "N/A"}
    }
    new_targets = {(row["base_file"], row["base_line"], row["base_row_key"]) for row in new}
    if prior_targets & new_targets:
        raise ManifestError("V3 invalid set repeats prior output")
    # 883 is measured from FINAL effective fields below, not historical sums.


def run_component_checks() -> None:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    for name in COMPONENT_CHECKS:
        result = subprocess.run(
            [sys.executable, "-B", str(OUT_DIR / name), "--check"], cwd=OUT_DIR,
            env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="strict", check=False,
        )
        if result.returncode != 0:
            raise ManifestError(f"required component --check failed: {name}:\n{result.stdout[-12000:]}")
        print(f"component integrity PASS: {name}", flush=True)
    # --fail-on-mismatch is separately a red conformance gate, NOT a
    # publication-success requirement. Its measured failure is reported below.


def audit_effective_outputs(snapshot: Snapshot) -> dict[str, int]:
    import pf_build_v3_effective_status as status_v3
    import pf_validate_v3_effective_capture as field_v3

    registry, effective, candidates, counts, per_file = field_v3.apply_v3_removals(OUT_DIR)
    measured_count = sum(len(rows) for rows in effective.values())
    if (
        counts.get("v3_new_removed") != 124 or counts.get("effective_rows") != 8671
        or measured_count != 8671 or counts.get("v3_new_slot34_removed") != 40
        or counts.get("v3_new_v1_removed") != 84 or per_file != NEW_A2_COUNTS
    ):
        raise ManifestError(f"effective V3 A2 census changed: {counts}; per_file={per_file}")
    candidate_counts = {key: len(rows) for key, rows in candidates.items()}
    if candidate_counts != EXPECTED_CANDIDATES:
        raise ManifestError(f"explicit candidate identities/counts changed: {candidate_counts}")
    candidate_totals = {
        variant: measured_count + sum(
            len(rows) for (_message, _direction, candidate_variant), rows in candidates.items()
            if candidate_variant == variant
        ) for variant in EXPECTED_CANDIDATE_TOTALS
    }
    if candidate_totals != EXPECTED_CANDIDATE_TOTALS:
        raise ManifestError(f"effective candidate alternatives changed: {candidate_totals}")
    _id_to_name, plans = field_v3.v2.build_schema_plans(registry, effective, candidates)
    plan_census = dict(Counter(plan.state for plan in plans.values()))
    if plan_census != EXPECTED_PLAN_CENSUS:
        raise ManifestError(f"schema-plan census changed: {plan_census}")
    remaining = [
        field for fields in effective.values() for field in fields
        if field.tag == "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL"
    ]
    if len(remaining) != 883 or any("UNKNOWN(" not in field.field_offset for field in remaining):
        raise ManifestError(f"final effective retained-invalid census/ceiling changed: {len(remaining)}")
    status_rows, report, _pins = status_v3.build(False)
    derived_status = status_v3.format_tsv(status_v3.OPEN_COLUMNS, status_rows).encode("utf-8")
    if snapshot.files["PF_V3_P1_OPEN.tsv"] != derived_status:
        raise ManifestError("actual P1 OPEN TSV differs byte-for-byte from re-derived rows")
    if snapshot.files["PF_V3_EFFECTIVE_STATUS.md"] != report.encode("utf-8"):
        raise ManifestError("actual status MD differs byte-for-byte from re-derived report")
    if len(status_rows) != 111 or len({row["message"] for row in status_rows}) != 111:
        raise ManifestError("V3 Priority-1 OPEN index changed")
    if any(
        row["source"] != "IMAGE" or row["effective_structural_status"] != "OPEN"
        or row["row_semantics"] != DERIVED_STATUS_SEMANTICS for row in status_rows
    ):
        raise ManifestError("invalid V3 Priority-1 derived row")
    require_text(snapshot, "PF_V3_EFFECTIVE_STATUS.md", (
        "Priority 1: **254/365 CLOSED**", "Priority 2: **8/16 CLOSED**",
        "Priority 3: **70/138 CLOSED**", "Overall: **332/519 CLOSED**",
        "Net-new A2 removal targets: 124", "duplicate/cross-file base-row target: 0",
    ))
    return {"rows": measured_count, "new_removals": 124, "remaining_invalid": len(remaining)}


def audit_a5(snapshot: Snapshot) -> dict[str, int]:
    if FORBIDDEN_DUPLICATE_A5_TSV in snapshot.files:
        raise ManifestError("unchanged A5 output was duplicated instead of referenced")
    if sha256_bytes(snapshot.files[CANONICAL_A5_TSV]) != CANONICAL_A5_SHA256:
        raise ManifestError("canonical A5 TSV identity changed")
    _fields, rows = read_tsv(snapshot, CANONICAL_A5_TSV)
    points: set[tuple[str, str, str, str]] = set()
    locations: set[tuple[str, str, str]] = set()
    for row in rows:
        for item in row["mismatch_field_identity_reason_count"].split(" | "):
            if not item or item == "NONE":
                continue
            parts = item.rsplit("~", 2)
            if len(parts) != 3 or not parts[2].isdigit() or int(parts[2]) <= 0:
                raise ManifestError("malformed A5 mismatch identity/reason/count")
            identity, reason, _count = parts
            location = (row["message"], row["direction(W/R)"], identity)
            if (*location, reason) in points:
                raise ManifestError("duplicate A5 mismatch identity/reason")
            locations.add(location)
            points.add((*location, reason))
    measured = {
        "rows": len(rows),
        "parse_success": sum(int(row["parse_success_instances"]) for row in rows),
        "static_open": sum(int(row["static_open_instances"]) for row in rows),
        "schema_not_applied": sum(int(row["schema_not_applied_instances"]) for row in rows),
        "mismatch": sum(int(row["mismatch_instances"]) for row in rows),
        "mismatch_points": len(points), "field_locations": len(locations),
    }
    if measured != EXPECTED_A5:
        raise ManifestError(f"V3 A5 measured census changed: {measured}")
    require_text(snapshot, "PF_V3_FIELD_VALIDATION.md", (
        "# 🔴 A5 V3 พบ static/capture mismatch",
        "exact-content duplicate paths rejected before claim counting: 645",
        "canonical non-text contents skipped by the packet-text parser: 561", CANONICAL_A5_TSV,
    ))
    # Required validator --check replays CAPTURE and compares generated UTF-8
    # bytes to this exact canonical TSV and actual V3 MD. Hash/census supplement
    # that byte comparison; they do not substitute for the component gate.
    return measured


def build_index(a5: Mapping[str, int], inherited_status_keys: int) -> str:
    if sha256_bytes(V2_INDEX_TAIL_TEXT.encode("utf-8")) != V2_INDEX_TAIL_SHA256:
        raise ManifestError("immutable V2 index tail changed")
    return "\n".join((
        '# 🔴 อ่านไฟล์นี้ก่อนจะ "ไปถอด" อะไรใหม่จากไบนารี', "",
        "## 🔴 V3 checkpoint ปัจจุบัน — duplicate-safe additive overlay", "",
        f"**A5 ยังพบ IMAGE/CAPTURE mismatch {a5['mismatch']} instances ที่ {a5['mismatch_points']} field+reason points ({a5['field_locations']} field locations)**; ตาราง IMAGE ไม่ถูกแก้ให้เข้ากับ CAPTURE", "",
        "ลำดับอ่าน:", "",
        "1. `PF_V3_MANIFEST.md` — commit marker, exact namespace, hashes และ duplicate audit ข้ามทุกรอบ",
        "2. `PF_V3_HANDOFF.md` — วิธีประกอบ V1 → V2 → V3 โดยไม่ append แถวซ้ำ",
        "3. `PF_V3_FIELD_VALIDATION.md` + canonical `PF_V2_FIELD_VALIDATION.tsv` — V3 replay ได้ TSV เดิมทุกไบต์ จึงไม่ปล่อยสำเนาซ้ำ",
        "4. `PF_V3_EFFECTIVE_STATUS.md` / `PF_V3_P1_OPEN.tsv` — P1 254/365 CLOSED, OPEN 111",
        "5. `PF_V2_MANIFEST.md` / `PF_HANDOFF_V1.md` — checkpoint ฐานแบบ immutable", "",
        "⚠️ ห้าม append TSV ทุกไฟล์เข้าด้วยกันตรง ๆ: `CHANGED` แทนที่, `REMOVE*` ลบ, `ADD*` เพิ่ม และ status index ไม่ใช่ evidence table อีกชุด", "",
        f"V3 ตัดแถวเดิมที่รอบก่อนทำแล้วออกจากชุดใหม่: `CTracePathVital` 3 แถวไม่ถูกปล่อยซ้ำ; cross-overlay base target ซ้ำ 0; owned evidence keys ซ้ำ 0; status key เดิม {inherited_status_keys} ตัวเป็น reference ใน derived index เท่านั้น", "",
        "[DECLARED-SCOPE] V3 เป็น local-only ใต้ `pf_bridge\\external`; ไม่มี client/server runtime, server code, workflow หรือ queue ถูกแก้หรือรัน", "",
        "ข้อความประวัติด้านล่างเป็น immutable V2 index tail ไม่ใช่สถานะปัจจุบันของ V3:", "",
        V2_INDEX_TAIL_TEXT,
    ))


def audit_all(
    *, manifest_may_be_absent: bool, require_final_index: bool, transients: frozenset[str],
) -> Audit:
    snapshot = take_snapshot(manifest_may_be_absent=manifest_may_be_absent, transients=transients)
    verify_inputs(snapshot)
    for name in sorted(snapshot.files):
        snapshot.text(name)
    census, inherited_status_keys = audit_tsvs(snapshot)
    audit_no_raw_proprietary(snapshot)
    audit_duplicate_history(snapshot)
    run_component_checks()
    effective = audit_effective_outputs(snapshot)
    a5 = audit_a5(snapshot)
    require_text(snapshot, "PF_V3_HANDOFF.md", (
        "3 แถวของ `CTracePathVital`", "Net-new A2 removal targets: **124**",
        "Priority 1: **254/365 CLOSED**", "effective canonical A2: **8,671 rows**", CANONICAL_A5_TSV,
    ))
    final_index = build_index(a5, inherited_status_keys)
    raw_byte_guard(INDEX_PATH.name, final_index)
    if require_final_index and snapshot.files[INDEX_PATH.name] != final_index.encode("utf-8"):
        raise ManifestError("current index differs byte-for-byte from derived V3 index")
    if (
        not require_final_index
        and sha256_bytes(snapshot.files[INDEX_PATH.name]) != V2_INDEX_SOURCE_SHA256
        and snapshot.files[INDEX_PATH.name] != final_index.encode("utf-8")
    ):
        raise ManifestError("current index is neither frozen V2 nor exact derived V3; refusing overwrite")
    # Bind every derivation/gate to the SAME bytes supplying manifest hashes/CAS.
    assert_snapshot_current(snapshot, transients=transients)
    return Audit(snapshot, census, a5, effective, inherited_status_keys, final_index)


def build_manifest(audit: Audit) -> str:
    a5, effective, snapshot = audit.a5, audit.effective, audit.snapshot
    lines = [
        "# PF V3 final local manifest and duplicate audit", "",
        f"🔴 **A5 V3 พบ mismatch {a5['mismatch']} instances / {a5['mismatch_points']} field+reason points / {a5['field_locations']} field locations**; IMAGE และ CAPTURE คงแยกชั้นหลักฐาน", "",
        "## Measured integrity and duplicate audit", "",
        "- [MEASURED] artifact integrity/reproduction: `PASS`; capture conformance: `FAIL` (the frozen red result is preserved)",
        "- [MEASURED] all four component `--check` gates passed; status and A5 outputs were re-derived and compared byte-for-byte, not merely by totals",
        "- [MEASURED] one exact artifact-byte snapshot supplies both manifest hashes and precommit compare-and-swap",
        "- [MEASURED] exclusive O_EXCL lock spans audit, stage, journal-before-replace, commit, final re-derivation and backup disposal; manifest replaced last",
        "- [MEASURED] pinned V2 manifest and all prior artifacts except the superseded search index: `PASS`",
        "- [MEASURED] exact namespace / UTF-8 / strict TSV cell counts / schema allowlists / exact V3 evidence-source sets: `PASS`",
        "- [MEASURED] exact duplicate rows within each TSV: `0`; unauthorised owned-key collisions in every key namespace: `0`",
        f"- [MEASURED] allowed inherited `status_key` references: `{audit.inherited_status_keys}`; only identical V2/V3 derived-index rows labelled NOT_A_NEW_EVIDENCE_ROW",
        "- [MEASURED] base_row_key/base_delta_key/effective_schema_key are explicitly classified references, not new owned-key namespaces",
        "- [MEASURED] cross-overlay A2 base-target duplicates / UNCHANGED or COPIED delta rows: `0`",
        "- [MEASURED] CAPTURE/DUMP schema and raw/opaque-byte-text guards passed; proprietary binary output files: `0`",
        "- [MEASURED] prior CTracePathVital invalid-parameter removals excluded from V3: `3`",
        f"- [MEASURED] retained invalid-parameter rows counted directly from FINAL effective A2: `{effective['remaining_invalid']}` (remain UNKNOWN)",
        "- [MEASURED] A5 generated TSV equals canonical PF_V2_FIELD_VALIDATION.tsv byte-for-byte; PF_V3_FIELD_VALIDATION.tsv is forbidden, not copied", "",
        "## Effective checkpoint", "",
        "| measured item | result |", "|---|---:|",
        "| Priority 1 IMAGE-static | 254/365 CLOSED; 111 OPEN |",
        "| Priority 2 IMAGE-static | 8/16 CLOSED; 8 OPEN |",
        "| Priority 3 IMAGE-static | 70/138 CLOSED; 68 OPEN |",
        "| Overall IMAGE-static | 332/519 CLOSED; 187 OPEN |",
        f"| effective canonical A2 | {effective['rows']:,} rows |",
        f"| net-new A2 removals | {effective['new_removals']} (84 V1 + 40 slot34) |",
        "| ItemAttr VTABLE_0x00F0EBB0 alternative | 13 R + 13 W = 26; total 8,697 |",
        "| ItemAttr VTABLE_0x00F4A188 alternative | 15 R + 15 W = 30; total 8,701 |",
        "| candidate composition | exactly those four identities; alternatives never merged |",
        "| schema plans | 620 applicable / 372 static-open / 46 not applied |",
        f"| A5 parse / static-open / schema-not-applied / mismatch | {a5['parse_success']:,} / {a5['static_open']:,} / {a5['schema_not_applied']:,} / {a5['mismatch']:,} |", "",
        "## Delivery scope (declared, not a historical-process measurement)", "",
        "[DECLARED-SCOPE] Local-only under pf_bridge/external. No client/server runtime, server code, workflow, or queue was changed or run. No dump/capture raw bytes may be emitted. This builder measures the artifact guards above; it does not infer historical process activity from file hashes.", "",
        "## Artifact hashes", "",
        "PF_V3_MANIFEST.md does not hash itself. The index hash is computed from staged final V3 UTF-8 bytes; every other hash is computed from the one audited snapshot. The historical index tail is literal immutable V2 text, not read from the mutable current index.", "",
        f"- V2 index source SHA-256: `{V2_INDEX_SOURCE_SHA256}`",
        f"- immutable V2 index tail SHA-256: `{V2_INDEX_TAIL_SHA256}`", "",
        "| file | bytes | SHA-256 | TSV rows | source counts |", "|---|---:|---|---:|---|",
    ]
    for name in sorted(snapshot.expected - {MANIFEST_PATH.name}):
        data = audit.final_index.encode("utf-8") if name == INDEX_PATH.name else snapshot.files[name]
        if name in audit.census:
            row_count, sources = audit.census[name]
            row_text = str(row_count)
            source_text = ", ".join(f"{source}={sources[source]}" for source in sorted(sources))
        else:
            row_text, source_text = "—", "—"
        lines.append(
            f"| `{name}` | {len(data)} | `{sha256_bytes(data).upper()}` | {row_text} | `{source_text}` |"
        )
    lines.extend((
        "", "## Reproduction and red conformance gate", "",
        "Run `py -3 -B pf_build_v3_manifest.py --check`; it itself requires all four component --check gates. A consumer must reject V3 if this fails, including a stale lock/cache/journal/transaction directory.", "",
        f"A5 ordinary --check is an integrity gate. `py -3 -B pf_validate_v3_effective_capture.py --check --fail-on-mismatch` is separately expected to exit nonzero for the measured {a5['mismatch']} mismatches / {a5['mismatch_points']} field+reason points; that expected conformance failure must not be hidden or treated as a publication failure.", "",
    ))
    result = "\n".join(lines)
    raw_byte_guard(MANIFEST_PATH.name, result)
    return result


def write_exclusive(path: Path, data: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def append_journal(path: Path, event: Mapping[str, object]) -> None:
    with path.open("ab") as handle:
        handle.write(json.dumps(event, sort_keys=True).encode("utf-8") + b"\n")
        handle.flush()
        os.fsync(handle.fileno())  # Intent is durable before destination changes.


def cleanup_transaction(directory: Path, known_paths: Sequence[Path]) -> None:
    if directory.resolve().parent != OUT_DIR or not directory.name.startswith(TRANSACTION_PREFIX):
        raise ManifestError("refusing cleanup outside the exact transaction directory")
    actual, allowed = set(directory.iterdir()), set(known_paths)
    if actual - allowed or any(path.is_symlink() or not path.is_file() for path in actual):
        raise ManifestError("unknown transaction content retained for manual inspection")
    for path in known_paths:
        if path.exists():
            path.unlink()
    directory.rmdir()  # Never recursive; unknown contents cannot be erased.


def publish_index_and_manifest(audit: Audit, manifest_text: str, held: HeldLock) -> None:
    before = audit.snapshot
    outputs = {
        INDEX_PATH.name: audit.final_index.encode("utf-8"),
        MANIFEST_PATH.name: manifest_text.encode("utf-8"),
    }
    transaction = Path(tempfile.mkdtemp(prefix=TRANSACTION_PREFIX, dir=OUT_DIR))
    if transaction.resolve().parent != OUT_DIR:
        held.retain = True
        raise ManifestError("transaction directory escaped the allowed output root")
    transients = frozenset({LOCK_PATH.name, transaction.name})
    journal = transaction / "journal.jsonl"
    staged = {name: transaction / f"{ordinal}.new" for ordinal, name in enumerate(outputs)}
    backups = {name: transaction / f"{ordinal}.old" for ordinal, name in enumerate(outputs)}
    known_paths = [*staged.values(), *backups.values(), journal]
    attempted: list[str] = []
    try:
        for name, data in outputs.items():
            write_exclusive(staged[name], data)
            if name in before.files:
                write_exclusive(backups[name], before.files[name])
        write_exclusive(journal, b"")
        append_journal(journal, {
            "event": "PREPARED", "manifest_last": MANIFEST_PATH.name,
            "destinations": [
                {"name": name, "existed": name in before.files,
                 "old_sha256": sha256_bytes(before.files[name]) if name in before.files else None,
                 "new_sha256": sha256_bytes(data), "backup": backups[name].name,
                 "staged": staged[name].name} for name, data in outputs.items()
            ],
        })
        # Compare against the original AUDITED snapshot, never a second hash
        # set taken after audit/build and accidentally made authoritative.
        assert_held_lock(held)
        assert_snapshot_current(before, transients=transients)
        for name in (INDEX_PATH.name, MANIFEST_PATH.name):
            append_journal(journal, {"event": "REPLACE_INTENT", "name": name})
            attempted.append(name)
            os.replace(staged[name], OUT_DIR / name)
            append_journal(journal, {"event": "REPLACE_DONE", "name": name})
        # Keep backups/journal throughout final checks and complete derivation.
        after = audit_all(manifest_may_be_absent=False, require_final_index=True, transients=transients)
        for name in before.expected - {INDEX_PATH.name, MANIFEST_PATH.name}:
            if after.snapshot.files[name] != before.files[name]:
                raise ManifestError(f"nonpublished artifact changed across commit: {name}")
        if after.snapshot.image_fingerprint != before.image_fingerprint:
            raise ManifestError("image changed across commit")
        rederived_manifest = build_manifest(after).encode("utf-8")
        if rederived_manifest != outputs[MANIFEST_PATH.name]:
            raise ManifestError("postcommit re-derived manifest differs from staged manifest")
        for name, data in outputs.items():
            if after.snapshot.files[name] != data:
                raise ManifestError(f"postcommit exact-byte readback mismatch: {name}")
        assert_snapshot_current(after.snapshot, transients=transients)
        assert_held_lock(held)
        append_journal(journal, {"event": "FINAL_REDERIVATION_PASS", "sha256": sha256_bytes(rederived_manifest)})
    except BaseException as original_error:
        try:
            for name in reversed(attempted):
                append_journal(journal, {"event": "ROLLBACK_INTENT", "name": name})
                destination = OUT_DIR / name
                if name in before.files:
                    if not backups[name].exists():
                        raise ManifestError(f"rollback backup missing: {name}")
                    os.replace(backups[name], destination)
                    if destination.read_bytes() != before.files[name]:
                        raise ManifestError(f"rollback byte verification failed: {name}")
                elif destination.exists():
                    destination.unlink()
            cleanup_transaction(transaction, known_paths)
        except BaseException as rollback_error:
            held.retain = True
            raise ManifestError(
                f"publication failed; rollback/cleanup incomplete; retained {transaction.name} "
                f"and {LOCK_PATH.name}: {rollback_error}"
            ) from original_error
        raise
    else:
        # Only the completely re-derived checkpoint reaches backup deletion.
        # A cleanup interruption must not roll back using partial backup sets.
        try:
            assert_held_lock(held)
            cleanup_transaction(transaction, known_paths)
        except BaseException as cleanup_error:
            held.retain = True
            raise ManifestError(
                f"checkpoint re-derived successfully but transaction cleanup failed; "
                f"retained lock/remaining journal: {transaction.name}"
            ) from cleanup_error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    success_message = ""
    with exclusive_lock() as held:
        transients = frozenset({LOCK_PATH.name})
        audit = audit_all(
            manifest_may_be_absent=not args.check, require_final_index=args.check,
            transients=transients,
        )
        assert_held_lock(held)
        manifest = build_manifest(audit)
        if args.check:
            if audit.snapshot.files.get(MANIFEST_PATH.name) != manifest.encode("utf-8"):
                raise ManifestError("PF_V3_MANIFEST.md differs byte-for-byte from re-derived manifest")
            assert_snapshot_current(audit.snapshot, transients=transients)
            success_message = (
                "check ok: P1=254/365 A2=8671 new_removals=124 prior_duplicate_excluded=3 "
                "remaining_invalid=883 unauthorized_key_collisions=0 inherited_status_refs=95 "
                "A5=canonical_V2_BYTES_IDENTICAL conformance=FAIL_386_4"
            )
        else:
            publish_index_and_manifest(audit, manifest, held)
            verify_namespace(audit.snapshot.expected, manifest_may_be_absent=False, transients=transients)
            success_message = f"PF_V3_MANIFEST.md {sha256_bytes(manifest.encode('utf-8'))}"
    # Lock identity/close/unlink must succeed before a global success is visible.
    print(success_message)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ManifestError as exc:
        raise SystemExit(f"ERROR: {exc}")
