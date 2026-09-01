# [MEASURED][CAPTURE] 🔴 A5 ยัง mismatch 386 instances / 3 field locations / 4 field+reason points

[MEASURED][IMAGE] V4 เป็น local IMAGE-static overlay ต่อจาก V3; full pinned V1→V2→V3→V4 overlay replay ถูก derive ใหม่ครบและเทียบผลลัพธ์แบบ byte-exact.

[MEASURED][CAPTURE] CAPTURE replay ยังคงจุดแดงเดิมและไม่ถูก rewrite เป็น IMAGE fact; conformance strict gate ยังต้องล้มเหลวที่ mismatch ชุดนี้.

## [MEASURED][IMAGE] V3 → V4 ที่เปลี่ยนจริง

- [MEASURED][IMAGE] DailyActivityState ลบ non-wire UNKNOWN 12 แถว (6 R + 6 W); Priority 3 ปิดเพิ่ม 1 message.
- [MEASURED][IMAGE] embedded-child composition ปล่อย 4 reference rows และ 2 removals เท่านั้น; ไม่ copy 64 logical child rows ลง A2. ActorActivity_UpdateDailyActivityStateVital ปิดเพิ่ม 1 P1; DBSS_GuildStorageInitialVital ยัง OPEN.
- [MEASURED][IMAGE] static type identity ยืนยัน ItemAttr/VitalData base vtable และ retained derived class แต่เพิ่ม A2 = 0, closure = 0; serializer selection ของทั้งคู่ยัง withheld ตามขอบเขตด้านล่าง.
- [MEASURED][IMAGE] Full pinned overlay replay วัด P1 255/365 CLOSED, P2 8/16, P3 71/138, overall 334/519; P1 OPEN 110.
- [MEASURED][IMAGE] canonical stored/reference A2 = 8,657; logical validation-only expansion = 8,721. expanded child fields อยู่ในหน่วยความจำเท่านั้น.

## [MEASURED][OUTPUT-AUDIT] Duplicate accounting — อะไรซ้ำได้และซ้ำไม่ได้

- [MEASURED][OUTPUT-AUDIT] Full namespace census = 121 files / 46 TSV / 21,918 TSV data rows; exact duplicate files = 0; exact duplicate rows ภายใน TSV = 0.
- [MEASURED][OUTPUT-AUDIT] `delta_key` + `dedup_key` = 3,404 occurrences / 3,404 unique; full `(base_file,base_line,base_row_key)` = 576 / 576 unique; non-N/A `base_delta_key` references = 69 / 69 unique; classmap keys = 4.
- [MEASURED][OUTPUT-AUDIT] raw row ที่ซ้ำข้ามไฟล์มีเฉพาะ derived status snapshots: 110 distinct / 312 occurrences / 202 extras. V2∩V3=95, V3∩V4=107, V2∩V4=92; ทุกแถวติด `NOT_A_NEW_EVIDENCE_ROW` จึงเป็น historical reference ไม่ใช่ fact row ใหม่.
- [MEASURED][OUTPUT-AUDIT] Bounded A2 ADD semantic census ใช้ tuple `(message,schema_variant,direction,new_order,new_tag,new_field_offset,new_len,new_gate_condition)`: 2,194/2,194 unique, duplicate groups 0. ขอบเขตนี้ครอบเฉพาะ `PF_A2_SERIALIZER_SLOT34_DELTA.tsv` และไม่สร้าง universal semantic identity ให้ TSV schema อื่น; CHANGED/REMOVE overlays ยังใช้ full base-target uniqueness ด้านบน.
- [MEASURED][OUTPUT-AUDIT] A5 TSV มี canonical singleton เดียวคือ `PF_V2_FIELD_VALIDATION.tsv`; V3/V4 มีรายงาน MD แต่ไม่มี TSV สำเนา.

## [MEASURED][IMAGE] Composition และ schema boundary

- [MEASURED][IMAGE] composition = 4 CHANGED references + 2 directionally-impossible removals; `ADD`, `UNCHANGED`, `COPIED` = 0 และ materialized child fields = 0.
- [MEASURED][IMAGE] ItemAttr alternatives คงแยก: `0x00F0EBB0` = 13 R + 13 W และ `0x00F4A188` = 15 R + 15 W. `canonical_a2_action=NO_CHANGE`; ไม่มีการเลือก/merge 26-row กับ 30-row schema.
- [MEASURED][IMAGE] VitalData base `0x00F0B930` และ Channel_MessageVtial derived `0x00F375FC` เป็น identity proof เท่านั้น; serializer ยัง UNKNOWN/WITHHELD และไม่ activate A2/A5 schema.
- [MEASURED][IMAGE] A5 logical plan = 624 APPLICABLE / 368 STATIC_OPEN / 46 SCHEMA_NOT_APPLIED.
- [MEASURED][CAPTURE] 8 V4-touched message+direction keys มี capture observations = 0 ตาม pinned corpus; ผลศูนย์นี้ไม่ขยายไปยัง session อื่น.

## [PROPOSED][LOCAL] ลำดับใช้ไฟล์

1. [PROPOSED][LOCAL] อ่าน `PF_V4_MANIFEST.md` สำหรับ commit marker, exact namespace/hashes และ executable guards.
2. [PROPOSED][LOCAL] อ่าน `PF_V4_EFFECTIVE_STATUS.md` + `PF_V4_P1_OPEN.tsv` สำหรับ current IMAGE-static derived status.
3. [PROPOSED][LOCAL] อ่าน `PF_V4_FIELD_VALIDATION.md` + canonical `PF_V2_FIELD_VALIDATION.tsv` สำหรับ CAPTURE replay และ red mismatch.
4. [PROPOSED][LOCAL] Compose Daily/composition/classmap outputs ตาม action/reference; ห้าม append TSV ตรง ๆ.
5. [PROPOSED][LOCAL] ใช้ V3 เป็น immutable predecessor; V4 index ฝัง V3 index เดิมครบทุกไบต์หลัง marker.

[PROPOSED][LOCAL] Reproduce ด้วย `py -3 -B pf_build_v4_manifest.py --check`; คำสั่งนี้เรียก component `--check` ทั้ง 5 ตัวและตรวจ image hash ก่อน/หลัง, exact bytes, duplicate topology, A2 ADD semantic tuple และ canonical A5 singleton.

[DECLARED-SCOPE] Local-only ใต้ `pf_bridge\external`; ไม่มี server/client runtime, workflow, queue, lease, Git หรือ GameClient file ถูกแก้หรือรัน และไม่มี raw dump/capture bytes ถูกเผยแพร่.
