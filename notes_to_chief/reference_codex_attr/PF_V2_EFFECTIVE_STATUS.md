# PF v2 effective IMAGE-static priority status

[MEASURED][IMAGE] ดัชนีนี้คำนวณจาก V1 และ IMAGE overlay ที่ pin hash แล้ว ไม่ใช่ตารางหลักฐานใหม่ และไม่คัดลอก field row เดิม

🔴 ผล CAPTURE เป็นคนละชั้นหลักฐาน: `PF_V2_FIELD_VALIDATION.tsv` พบ mismatch 386 instances ที่ 3 field locations / 4 field+reason points; ห้ามตีความ 250 CLOSED ด้านล่างว่าได้รับการยืนยันจากสายจริงทั้งหมด

## Effective IMAGE-static structural result

- Priority 1: **250/365 CLOSED** (68.49%); OPEN 115
- Priority 2: **7/16 CLOSED** (43.75%); OPEN 9
- Priority 3: **68/138 CLOSED** (49.28%); OPEN 70
- Overall: **325/519 CLOSED** (62.62%); OPEN 194

## Overlay accounting

| overlay | changed status rows |
|---|---:|
| `PF_POST_V1_PRIORITY_DELTA.tsv` | 3 |
| `PF_PRIORITY_POOL_638690_DELTA.tsv` | 4 |
| `PF_PRIORITY_POOL_661FA0_DELTA.tsv` | 4 |
| `PF_PRIORITY_POOL_46F4D0_DELTA.tsv` | 4 |
| `PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv` | 37 |

- V1 structural CLOSED: 337/519.
- post-V1 plus three proven pools: +15 CLOSED.
- serializer-slot +0x34 truth correction: -27 structural CLOSED.
- effective structural CLOSED: 325/519.
- `PF_A2_POOL_46BAA0_READER_DELTA.tsv` changes three reader rows only; its dynamic writer identities remain OPEN, so it changes no priority status.
- `PF_TARGET_652A30_A2_DELTA.tsv` and `PF_TARGETS_694790_6B3440_A2_DELTA.tsv` remove non-wire A2 rows only; they change no priority status.

## Priority-1 OPEN primary blocker groups

| primary group | messages |
|---|---:|
| `CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED` | 15 |
| `DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED` | 77 |
| `INDIRECT_JUMP_TARGET_UNRESOLVED` | 2 |
| `OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED` | 10 |
| `REGISTRY_IDENTITY_UNRESOLVED` | 11 |

Exact names and complete blocker strings are in `PF_V2_P1_OPEN.tsv`.

## Duplicate-control contract

- Base messages: 519 unique.
- Priority overlay rows: 52; duplicate messages within/across overlays: 0.
- `delta_key` and `base_row_key` duplicates within each overlay: 0.
- Every overlay base line/hash/status matches the immutable V1 row.
- Output rows: 115 OPEN-only derived status rows; CLOSED rows and A1/A2/A3 fields are not copied.
- `row_semantics=DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW` prevents this view from being counted as another evidence table.
- Every TSV row in this derived status view remains `source=IMAGE`; no DUMP, CAPTURE, or DATA layer is joined.
- CAPTURE mismatch counts are reported separately and never used to overwrite IMAGE status rows.

## Reproduction

Run `py -3 -B pf_build_v2_effective_status.py --check` to re-hash every input, re-apply all status deltas, and compare both outputs byte-for-byte.
