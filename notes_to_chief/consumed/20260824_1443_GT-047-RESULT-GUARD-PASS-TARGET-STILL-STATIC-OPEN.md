ถึง chief — ผล GT-047 รอบ unattended/static บนสะพาน

# GT-047 — DONE / GUARD PATCH PASS / F2 STILL OPEN

เวลา: 2026-08-24 14:38–14:43 +07:00

สรุปชี้ขาด: patch guard ที่ chief ส่งมาทำงานถูกต้องบน Windows สะพาน (`ALL 8 CHECKS PASS`) และ mutation บังคับ `TargetPosVital:W:1 field_offset +0x14 -> +0x99` แดงจริง แต่เมื่อรัน patched validator กับ frozen corpus 1,772 ไฟล์ ข้อความเป้าหมายทั้งสองยังไม่ถูก parse แม้แต่เฟรมเดียว จึง **คง `A2_STATIC_OPEN`; F2 ยังไม่ปิด** ไม่ promote เป็น `VALIDATED`

ตามข้อห้ามของรอบ runner ว่าอย่าแก้ไฟล์ต้นทางใน `external\` ผมไม่ได้สำเนาทับ validator เดิม แต่รันไฟล์ patch ที่พินตรงไบต์ (`CAFA…011B`) จาก `patches\gt047\` และ staged mirror ที่มี TSV/input inventory เหมือนต้นทางทุกไบต์ ผลทดสอบ guard/corpus จึงใช้ตัว patch เดียวกับที่ใบสั่งระบุ โดย `external\pf_validate_capture_fields.py` ยังมี SHA เดิม `0166337C…B793D8C8`

## ช่องค้นบังคับ

- ค้นใน `pf_bridge\external\` แล้ว: เจอชื่อ `GSCN_RunTimeProtocolReq` ใน `PF_PROTOCOL_REGISTRY.tsv`, `PF_SERIALIZER_FIELDS.tsv`, `PF_TAG_CENSUS.tsv`, `PF_PROTOCOL_PRIORITY.tsv`, `PF_FIELD_VALIDATION.tsv` และเจอ validator รุ่นก่อน patch
- ค้น gamedata แล้ว: ไม่เจอชื่อ `GSCN_RunTimeProtocolReq` หรือ `GSCN_RunTimeProtocolRes` ใน `pf_bridge\gamedata\`

## จ็อบ 0/การ์ด — PASS 8/8

บรรทัดพินตัวที่โหลดจริง:

```text
validator sha256=cafa5f69401eaf152f7ae4e646ce76eb3016c3d6b71e76c494819a029877011b bytes=58656
```

ผล `verify_gt047_guard_patch.py`: pristine PASS (`messages=519 static_open=181`); mutation จ็อบ 3, static-open flip, one-leg embedded-VA edit, span hash tamper และ membership swap ถูก reject; parser/schema mutation self-tests PASS; self-test แดงเมื่อปิด guard; จบด้วย `ALL 8 CHECKS PASS` exit 0

## จ็อบ 1 — frozen corpus 1,772 ไฟล์

patched validator exit 0:

```text
capture_files=1772 blocks=51894 nested_declared=13220 nested_reached=12785 pass=11904 static_open=52775 mismatch=0 unresolved_after_open=435
```

ผลสองข้อความเป้าหมาย:

| message/leg | observed | parse success | A2 static open | mismatch | files | status |
|---|---:|---:|---:|---:|---:|---|
| `GSCN_RunTimeProtocolReq` W | 40,747 | 0 | 40,747 | 0 | 126 | `A2_STATIC_OPEN` |
| `GSCN_RunTimeProtocolRes` R | 10,073 | 0 | 10,073 | 0 | 134 | `A2_STATIC_OPEN` |

ขา Req/R และ Res/W เป็น `NOT_OBSERVED` (0 เฟรม) ตาม output. ตัวเลข `mismatch=0` รอบนี้ **ไม่ใช่หลักฐาน schema ของสองข้อความ** เพราะทั้ง 50,820 เฟรมถูกจัดเป็น static-open ก่อนเกิด parse; จึงไม่มี mismatch รายฟิลด์ให้รายงาน

validator ตรวจ path/size/SHA ตาม `PF_INPUT_INVENTORY.tsv` ก่อนและหลังรันครบ 1,772 ไฟล์และ exit 0; inventory SHA `729B5E73383DE8FD6E0008875D4B9B685DE2AD8D72A55118AA862093F10259D1`

## จ็อบ 2 — re-derive สดจาก image

รันสำเนา `pf_extract_protocol.py` ใน staged directory ใหม่ ผล exit 0 และตรง byte-for-byte ครบสามไฟล์:

- `PF_PROTOCOL_REGISTRY.tsv` = `27DAAC0C6FBBC45D88281C31B98E3A8B56F421BD1E8BC16F970FDFF5716CFB4D`
- `PF_SERIALIZER_FIELDS.tsv` = `99282BDF3F492EAEBDBAB4918AECC0E37BF8EFB42B904B18E1BA306767B5C123`
- `PF_TAG_CENSUS.tsv` = `63BC9A039B5B35E5B2E1F08CE99E91B05DA6E6959B5B4F173EAC66B88AEA337A`
- image ก่อน/หลัง = `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`

## จ็อบ 3 — mutation ต้องแดง

baseline patched validator เขียวตามจ็อบ 1. จากนั้นรัน patch เดียวกันกับ mirror ที่กลาย `TargetPosVital:W:1 field_offset +0x14 -> +0x99`: exit 1 ทันทีด้วย

```text
ERROR: W/R field_offset mirror broken for TargetPosVital order 1
```

ดังนั้นช่องโหว่เดิมที่ยอมรับ field-offset corruption ถูกปิดแล้ว

## หลักฐานที่สร้างใหม่

โฟลเดอร์: `pf_bridge\staged\gt047_patch_run_20260824_1438\`

- `guard_verifier.log` SHA `37D5B0010BEC91706C4E9A6CF00C71E38EB77A227C853CF4973D8A8381E4832B`
- `frozen_corpus_baseline.log` SHA `789E186F9DF0B6DAF7EBA764F11BB9F74BF5C97B0EC320225C21C3A3AE66F2B4`
- `fieldoffset_mutation_red.log` SHA `C27FD94CD74493C08C593C54610A178F370A170411C2D7323F0FBD70D8189E6E`
- `rederive_exact.log` SHA `1DA0E2686A36FC68E1E1FAE6EC6ABBC94CA12356F9A6E16C7A3B496A8674C13F`
- generated `PF_FIELD_VALIDATION.tsv` SHA `080A5F32580DF575632FEE69D3F8FAA6E2E745AD1775D05DAF3E272E4E0941C3`
- generated `PF_FIELD_VALIDATION.md` SHA `39C8FA913316B674636AE684CDE2FC1B4D77A7BC1DD57016A1E4636E03636FF1`

## Nonclaims บังคับ

- F1: `pass=11,904` ถูกแบกด้วย `CheckSecondPwdVital` R 9,166 (77%) + หางบาง 34 คู่; ห้ามอ่านว่าตารางโปรโตคอลถูกยืนยันกว้าง ๆ
- F2: ผลนี้ยกได้เฉพาะ Req/W และ Res/R และทั้งคู่ยัง `A2_STATIC_OPEN`; F2 ยังเปิด
- F3: 980 คู่ (95%) `NOT_OBSERVED`, 37 คู่ (3.6%) `VALIDATED`; `mismatch=0` ไม่กล่าวถึง 980 คู่นั้น
- เฉพาะแถว `VALIDATED` เท่านั้นเป็นหลักฐาน capture; ผลนี้เป็น static/capture analysis ไม่ใช่ client-observable
- ไม่ claim ความหมาย tag เกินขนาดที่พินไว้, ไม่ใช้ `PF_RUNTIME_CLASSMAP.tsv` เป็นชื่อคลาส และไม่ claim ว่าเป็นการประกอบของเซิร์ฟเวอร์ต้นฉบับ
- guard ใหม่ไม่ครอบ mutation สมมาตรพร้อมกันสองขา; embedded VA ในคู่ pinned 40 คู่ยังพึ่ง span SHA/GT-054; ไม่ครอบ `gate_condition` หรือ `file_off_claim`

ไม่มีการบูต server/client, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ capture/TSV/image/external/gamedata หรือ queue ใด ๆ

ข้อเสนอให้ chief ลง ledger: ปิด GT-047 ในฐานะ `DONE / GUARD-GAP FIXED / METHOD-RUN COMPLETE` แต่คง claim F2 เป็น `OPEN — TARGET A2_STATIC_OPEN 50,820/50,820` จนกว่าจะมี parser ที่เข้าถึง body ของสองข้อความจริง
