# 🔴 A5 V3 ยังพบ 386 mismatch instances ที่ 3 field locations / 4 field+reason points

[MEASURED][CAPTURE] Replay ด้วย effective V3 A2 แล้วผล aggregate ไม่เปลี่ยนจาก V2: parse ผ่าน 22,965 instances, static-open 78,532, schema-not-applied 0, mismatch 386. ตาราง IMAGE ไม่ถูกแก้ให้เข้ากับ CAPTURE

**ไม่สร้าง `PF_V3_FIELD_VALIDATION.tsv`** เพราะผลที่ re-derive ได้เหมือน `PF_V2_FIELD_VALIDATION.tsv` แบบไบต์ต่อไบต์ SHA-256 `10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806`. ใช้ตาราง V2 นี้เป็น canonical ต่อไป และอ่าน `PF_V3_FIELD_VALIDATION.md` สำหรับ input hashes, effective A2 ใหม่ และผล replay รอบนี้

## 1. ความคืบหน้า V2 → V3

[MEASURED][IMAGE] ตัวเลขนี้เป็นการปิดโครงสร้างจากภาพไบนารี ไม่ใช่เปอร์เซ็นต์ gameplay หรือการผ่านสายจริงครบทุก branch

| ตัววัด | V2 | V3 | เปลี่ยนแปลง |
|---|---:|---:|---:|
| Priority 1 CLOSED | 250/365 (68.49%) | 254/365 (69.59%) | +4 |
| Priority 1 OPEN | 115 | 111 | -4 |
| Priority 2 CLOSED | 7/16 | 8/16 | +1 |
| Priority 3 CLOSED | 68/138 | 70/138 | +2 |
| รวม CLOSED | 325/519 | 332/519 | +7 |
| รวม OPEN | 194 | 187 | -7 |
| effective canonical A2 | 8,795 | 8,671 | -124 non-wire analysis rows |
| A2 rows ที่ยังมี UNKNOWN | 4,105 | 3,981 | -124 |
| generic CALL/JUMP UNKNOWN rows | 1,354 | 1,318 | -36 |
| direct invalid-parameter UNKNOWN rows | 931 | 883 | -48 |

Priority 1: **254/365 CLOSED**; OPEN 111

effective canonical A2: **8,671 rows**

แถว UNKNOWN ไม่ใช่จำนวนฟังก์ชันไม่ซ้ำ: ฟังก์ชันเดียวอาจถูกอ้างหลาย message, หลาย order และทั้ง W/R. ห้ามนำจำนวนแถวไปอ้างว่าเป็นจำนวนฟังก์ชันที่ปิดแล้ว

## 2. ผลใหม่และการป้องกัน duplicated output

Net-new A2 removal targets: **124** — ทุกแถว `source=IMAGE`

| delta | แถวที่ลบจาก effective A2 | physical sites ไม่ซ้ำ |
|---|---:|---:|
| guarded invalid-parameter | 48 | 18 |
| targets `0x6564E0/0x656C50/0x6FDB40` | 32 | 12 |
| target `0x656690` | 4 | 2 |
| stack-local link-state helpers | 40 | 12 |
| รวม | 124 | 44 |

- พบ 3 แถวของ `CTracePathVital` ที่รอบก่อนลบแล้ว: V1 lines 5493–5495. ชุดใหม่ไม่ส่งสามแถวนี้ซ้ำ และตัวตรวจปฏิเสธการอ้าง base-line/key เดิม
- A2 `delta_key` ใหม่ไม่ซ้ำ 124/124; base targets ไม่ซ้ำ 124/124; ไม่ชน target ของ overlay เก่า
- จำนวน 124 rows กับ 44 physical sites เป็นคนละมิติ การอ้าง site เดียวผ่าน message/direction/order ต่างกันถูกแจกแจง ไม่ถูกนับเป็น 124 ฟังก์ชัน
- Priority changes ใหม่มี 7 แถว; 4 แถวต้องอ้าง predecessor จาก `PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv` ไม่ใช่อ้าง V1 ที่ล้าสมัย
- ไม่มีแถว `UNCHANGED` หรือ `COPIED` ถูกส่งเป็น delta
- A5 aggregate TSV ที่เหมือน V2 ถูก reuse โดยอ้าง hash ไม่คัดลอกเป็นไฟล์ V3 อีกชุด
- `PF_V3_P1_OPEN.tsv` เป็น **derived index** สำหรับค้น 111 messages ที่ยังเปิด ไม่ใช่ evidence table ใหม่. ความหมายสถานะคงเดิม 103 messages (ในนี้ 95 มี `status_key` เดิมตรงกัน; อีก 8 เปลี่ยนรูปการอ้าง chain), อีก 8 messages คำนวณ blocker metadata ใหม่จาก effective A2; 4 P1 messages ที่ปิดแล้วไม่อยู่ใน index

เจ็ด structural closures ใหม่:

- Priority 1: `ActorLearnedPetsSkillData`, `CollectionObj_UpdateCollectEffectVital`, `NPCAppearAttr`, `Winemaking_UpdateLearnedFormulaVital`
- Priority 2: `CBuffConditionState`
- Priority 3: `CollectionEffectData`, `WineFormulaLearningAttr`

ทุก closure ผ่านการประกอบ effective A2 จริง, UNKNOWN คงเหลือ 0 และมี non-EMPTY field อย่างน้อยหนึ่งแถว. ไม่ใช้แค่ข้อความ blocker เก่าหรือจำนวนแถวที่ลดลงเป็นเหตุผลปิด

## 3. ลำดับประกอบ effective A2

เริ่มจาก V1 `PF_SERIALIZER_FIELDS.tsv` แล้วใช้เก้า overlay ตาม `PF_V2_HANDOFF.md` ก่อน จากนั้นใช้ V3 ตามลำดับ:

1. `PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv`
2. `PF_A2_TARGETS_6564E0_656C50_6FDB40_NONWIRE_DELTA.tsv`
3. `PF_A2_TARGET_656690_NONWIRE_DELTA.tsv`
4. `PF_A2_ITERATOR_HELPERS_NONWIRE_DELTA.tsv`

`REMOVE_NONWIRE_ROW` ลบแถว V1 ที่ระบุ; `REMOVE_OVERLAY_NONWIRE_ROW` ลบแถว slot+0x34 ที่ระบุด้วยทั้ง canonical row key และ predecessor delta key. **ห้าม append ทุก TSV เข้าด้วยกันตรง ๆ**

ผล canonical = 8,671 rows. ItemAttr ยังเป็นทางเลือกแยกกัน:

- base candidate `VTABLE_0x00F0EBB0`: เพิ่ม 26 → 8,697 rows
- derived candidate `VTABLE_0x00F4A188`: เพิ่ม 30 → 8,701 rows

ห้ามรวมสอง candidate เข้าด้วยกัน. A1 ยังคง 519 logical messages และ effective A3 frequency คง 4,081 (candidate alternatives 4,095 หรือ 4,097)

## 4. A5 และสิ่งที่ไม่ได้เปลี่ยน

| message | direction | field | reason | instances |
|---|:---:|---|---|---:|
| `TeleportVital` | R | wire order 20 | `STRING_TAG` | 190 |
| `TeleportVital` | W | order 4 | `TAG` | 188 |
| `TradeCmdVital` | W | order 5 | `TAG` | 6 |
| `TradeCmdVital` | W | order 5 | `TRUNCATED_TAG` | 2 |

- capture 2,154 paths → 1,509 unique full-file contents; 645 duplicate paths ถูกตัดก่อนนับ claims
- schema plans เปลี่ยนจาก applicable 606/static-open 386 เป็น applicable 620/static-open 372; schema-not-applied คง 46
- แต่ observed aggregate ทั้ง 66 rows เหมือนเดิมทุกไบต์: corpus นี้ไม่ได้ให้ผลใหม่จาก 14 direction plans ที่เพิ่งปิด
- `--check` exit 0 หมายถึง integrity/reproduction ผ่าน ไม่ใช่ conformance ผ่าน
- `--check --fail-on-mismatch` รันแล้วออก 1 ตามจริง: mismatch 386 / field+reason points 4

## 5. Priority 1 ที่ยังเปิด

| กลุ่ม blocker หลัก | messages |
|---|---:|
| call effect / stream provenance | 14 |
| dynamic dispatch / subcall | 77 |
| indirect jump target | 2 |
| object alias / mutable graph | 7 |
| registry identity | 11 |
| รวม | 111 |

ชื่อและเหตุผลเต็มอยู่ใน `PF_V3_P1_OPEN.tsv`. เป้าหมายยังไม่ครบ 100% และไม่เปลี่ยนเป้าหมายเป็นไล่ UNKNOWN ทุกกลุ่มให้เหลือศูนย์

ข้อที่ตั้งใจยังไม่รับ:

- global invalid-parameter cleanup 931 แถวถูกปฏิเสธ; รับเฉพาะ 48 แถวที่มี per-call proof และคงอีก 883 แถวเป็น UNKNOWN
- callsite `0x0049FAD4` และ 6 แถวที่เกี่ยวข้องยังไม่ถูกลบ เพราะ entry-relative stack depth ยัง UNKNOWN
- คำว่า iterator เป็นเพียง `[PROPOSED]`; หลักฐานรับรองเฉพาะ stack-local link-state helper ไม่ได้ยืนยัน RTTI/container identity
- A6 ไม่มีผลใหม่ใน V3; strict runtime class/vtable mapping ที่พิสูจน์ได้ยังเป็น 0 ตาม checkpoint เดิม

## 6. Checkpoint และขอบเขตส่งมอบ

`PF_V3_MANIFEST.md` เป็น acceptance marker และต้องเขียนเป็นลำดับสุดท้าย. ถ้าไม่มี manifest, hash ไม่ตรง, namespace ไม่ครบ หรือ component `--check` ไม่ผ่าน ให้ปฏิเสธ V3 ทั้งชุด ไม่ใช้ไฟล์ที่เขียนค้างครึ่งทาง

ลำดับอ่าน:

1. `PF_V3_MANIFEST.md`
2. `PF_V3_FIELD_VALIDATION.md` + canonical `PF_V2_FIELD_VALIDATION.tsv`
3. `PF_V3_EFFECTIVE_STATUS.md` + `PF_V3_P1_OPEN.tsv`
4. รายงาน compiler/container และ link-state helper ของ V3
5. `PF_V2_HANDOFF.md` และ V1/V2 manifests สำหรับฐาน immutable

[DECLARED SCOPE] รอบนี้ทำเฉพาะ client reverse engineering แบบอ่านอย่างเดียว; ไม่มีการรัน client/server และไม่มีการเขียน/แก้ server code, workflow หรือ queue. ผลทั้งหมดอยู่ใต้ `pf_bridge/external` แบบ local-only. ผู้ออกใบสั่งที่เข้าถึงโฟลเดอร์นี้อ่านได้ครบ แต่ clean clone/remote ไม่ได้รับไฟล์โดยอัตโนมัติ

Pinned `GameClient.local.bin`: 14,759,424 bytes; SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

ทุก TSV row มี `source` แยก IMAGE/CAPTURE/DUMP/DATA; ไม่มี raw dump/capture bytes ถูกคัดลอกลงผลลัพธ์
