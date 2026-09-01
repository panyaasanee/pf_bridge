# 🔴 A5 V2 พบ 3 field locations / 4 field+reason points / 386 instances

นี่คือ checkpoint ส่งมอบผลถอด GameClient V2 แบบ additive overlay ต่อจาก V1 โดยรักษาชั้นหลักฐาน `IMAGE`, `DUMP`, `CAPTURE`, `DATA` แยกจากกันทุกแถว และไม่แก้ static table ให้เข้ากับสายจริงเมื่อพบความไม่ตรง

[MEASURED] ตัวเลข census, hash, duplicate count และ validation outcome ในรายงานนี้มาจาก generator/checkpoint ที่ re-derive ได้ ส่วนสิ่งที่ยังพิสูจน์ไม่ได้คงสถานะ OPEN/UNKNOWN และไม่ถูกเดา

## 1. ข่าวใหญ่จาก A5

| message | dir | field | reason | instances |
|---|:---:|---|---|---:|
| `TeleportVital` | R | wire order 20 | `STRING_TAG` | 190 |
| `TeleportVital` | W | order 4 | `TAG` | 188 |
| `TradeCmdVital` | W | order 5 | `TAG` | 6 |
| `TradeCmdVital` | W | order 5 | `TRUNCATED_TAG` | 2 |

- รวม 386 mismatch instances ที่ 3 ตำแหน่งฟิลด์ / 4 คู่ field+reason (`TradeCmdVital W order 5` มีทั้ง `TAG` และ `TRUNCATED_TAG` ที่ตำแหน่งเดียวกัน)
- parse ผ่าน 22,965 instances; IMAGE static-open 78,532 instances
- ไม่มี schema-not-applied ใน corpus ที่นำมานับชุดนี้
- ตาราง IMAGE ไม่ถูกแก้หรือเดาให้เข้ากับ CAPTURE
- รายละเอียดและตัวระบุ field ที่แน่นอนอยู่ใน `PF_V2_FIELD_VALIDATION.tsv`
- `--check` ที่ออก 0 หมายถึง freeze/reproduction ผ่าน ไม่ได้หมายถึง schema conformance ผ่าน; ใช้ `--check --fail-on-mismatch` เมื่อต้องการ gate ที่ออก nonzero เมื่อมี mismatch

## 2. สถานะ IMAGE-static หลังใช้ overlay ทั้งหมด

| priority | CLOSED | OPEN | CLOSED % |
|---:|---:|---:|---:|
| 1 | 250/365 | 115 | 68.49% |
| 2 | 7/16 | 9 | 43.75% |
| 3 | 68/138 | 70 | 49.28% |
| รวม | 325/519 | 194 | 62.62% |

ตัวเลขนี้เป็นผลโครงสร้างจาก `source=IMAGE` เท่านั้น ไม่ได้หมายความว่า 250 ตัวใน Priority 1 ผ่านสายจริงครบทุก branch แล้ว รายชื่อ Priority 1 ที่ยังเปิดและเหตุผลเต็มอยู่ใน `PF_V2_P1_OPEN.tsv`

กลุ่มเหตุผลของ Priority 1 ที่ยังเปิด:

| blocker group | messages |
|---|---:|
| call effect / stream provenance | 15 |
| dynamic dispatch / subcall | 77 |
| indirect jump target | 2 |
| object alias / mutable graph | 10 |
| registry identity | 11 |

## 3. กฎป้องกัน duplicated output

V2 ไม่สร้างสำเนา A1/A2/A3 เต็มชุดใหม่ แต่ส่งเฉพาะ delta และ derived index:

- `CHANGED` = แทนที่แถวฐานที่ระบุด้วย `base_row_key` ห้ามเก็บทั้งเก่าและใหม่
- `REMOVE*` = ลบแถวฐานหรือแถว overlay ที่ระบุ ห้ามคงแถวเดิมไว้
- `ADD*` = เพิ่มเฉพาะแถวใหม่ที่ไม่มีในฐาน
- ItemAttr base/derived เป็น **candidate alternatives** ห้ามรวมสองแบบเข้าด้วยกัน
- `PF_V2_P1_OPEN.tsv` เป็น derived status index ไม่ใช่ evidence table เพิ่มอีกชุด

การตรวจปัจจุบันพบ:

- exact duplicate rows ในผล V2: 0
- duplicate primary/delta/status/validation keys: 0
- priority message ซ้ำข้าม overlay: 0 จาก 52 status changes
- แถว `UNCHANGED` หรือ `COPIED` ที่ถูกส่งซ้ำเป็น delta: 0
- base-row target ซ้ำระหว่าง overlay ที่ต้องใช้ร่วมกัน: 0
- capture 2,154 paths เหลือ 1,509 unique contents; 645 duplicate paths ถูกตัดออกก่อนนับ claim
- ใน 1,509 unique contents: 561 non-text ไม่เข้า packet-text parser, 948 text ถูกตรวจ, 556 text ไม่มี recognized packet block และ 392 text ส่ง block เข้า parser
- message instances จาก duplicate capture paths 8 instances ถูกเก็บเป็น audit count เท่านั้น ไม่ถูกรวมในผล canonical

ดังนั้นอย่านำ TSV ทุกไฟล์มาต่อท้ายกันตรง ๆ ให้ใช้ลำดับและ action ด้านล่าง

## 4. ลำดับประกอบ effective A2

เริ่มจาก V1 `PF_SERIALIZER_FIELDS.tsv` 6,931 แถว แล้วใช้ตามลำดับ:

1. `PF_A2_STRING_WIRE_TAG_DELTA.tsv`
2. `PF_A2_POST_V1_STATIC_DELTA.tsv`
3. `PF_A2_SERIALIZER_SLOT34_DELTA.tsv`
4. `PF_A2_POOL_638690_DELTA.tsv`
5. `PF_A2_POOL_661FA0_DELTA.tsv`
6. `PF_A2_POOL_46F4D0_DELTA.tsv`
7. `PF_A2_POOL_46BAA0_READER_DELTA.tsv`
8. `PF_TARGET_652A30_A2_DELTA.tsv`
9. `PF_TARGETS_694790_6B3440_A2_DELTA.tsv`

ข้อควรระวัง: target-removal สองไฟล์ท้ายอาจอ้างถึงแถวที่เพิ่ง `ADD` จาก slot+0x34 overlay ดังนั้นต้องประมวลผล action ตามตัวระบุ ไม่ใช่ sort แล้ว append

ผล canonical ที่ไม่เลือก ItemAttr candidate = **8,795 A2 rows**. ถ้าเลือก ItemAttr base candidate จะเป็น 8,821; ถ้าเลือก derived candidate จะเป็น 8,825. สองจำนวนหลังเป็นทางเลือกคนละชุด ห้ามรวมเป็น 8,851

## 5. A1 และ A3

- A1 ยังคงมี logical message registry 519 ตัว; `PF_A1_SERIALIZER_SLOT34_DELTA.tsv` มี correction 59 แถว ไม่ได้ทำให้กลายเป็น 578 messages
- correction 59 แถวประกอบด้วย target correction 56, provenance-only 2 และ ItemAttr ambiguity 1
- A3 string correction เพิ่ม tag 0x44/0x48
- effective tag-frequency total เมื่อใช้ singleton slot+0x34 = 4,081
- ถ้าเลือก ItemAttr base candidate = 4,095; derived candidate = 4,097; เป็นทางเลือกคนละชุดและห้ามบวกเข้าด้วยกัน

## 6. A5 content de-duplication และการเทียบ V1/V2

- V1 inventory เดิม 1,772 paths มี 1,189 unique contents และ 583 duplicate paths
- capture เพิ่ม 382 paths มี 320 unique new contents และ 62 duplicate paths
- รวม 2,154 paths มี 1,509 unique contents และ 645 duplicate paths
- ถ้าใช้ V1 schema เดิมกับ unique corpus ทั้งหมด: pass 22,963; static-open 78,920; mismatch 0
- เมื่อใช้ effective V2 schema: pass 22,965; static-open 78,532; mismatch 386
- reconciliation ตรงกัน 101,883 claims: formerly-open 388 instances เปลี่ยนเป็น pass 2 + mismatch 386 โดยไม่มี claim หายหรือเพิ่ม

นี่อธิบายว่าทำไมรอบเก่ารายงาน mismatch 0 แต่รอบนี้พบ mismatch: รอบเก่าทาบเฉพาะ schema V1; รอบนี้ทาบ correction/overlay V2 จริง

## 7. A6 runtime identity

- V1 dump inventory มี 6,244 aggregate rows แต่ strict RTTI class/vtable mapping ที่พิสูจน์ได้ = 0
- V2 ตรวจ candidate เพิ่ม 134 รายการและปฏิเสธทั้งหมดเป็น `REJECTED_NOT_VTABLE`
- ไม่มีการเดาชื่อคลาสจากสตริงใกล้เคียง
- ผลจาก dump เป็น snapshot ณ crash และติด `source=DUMP`; ไม่เขียนย้อนเข้า IMAGE table

## 8. สรุป delta ที่เพิ่มจาก V1

- string-wire corrections: 408 `CHANGED`; A3 เพิ่ม 2 tags
- post-V1 static: A2 42 directives และปิด Priority 1 ได้ 3 messages
- serializer slot+0x34: A1 59, A2 2,308, A3 23, priority 37 directives
- proven pools `0x638690`, `0x661FA0`, `0x46F4D0`: ปิดเพิ่มรวม 12 messages
- pool `0x46BAA0`: แก้ reader 3 แถว แต่ writer identity ยัง dynamic จึงไม่ปิด status
- non-wire removals: target `0x652A30` 16 directives; targets `0x694790/0x6B3440` 30 directives; ไม่มี status change
- capture branch shapes: 67 shapes ใหม่แบบ `source=CAPTURE`
- A6 candidate rejection audit: 134 แถวแบบ `source=DUMP`

## 9. V1 report errata ที่ต้องรู้

V1 artifacts คงสภาพเดิมเพื่อ audit แต่มี census prose ที่ห้ามนำไปใช้โดยไม่แก้ความหมาย:

- รายงาน V1 ระบุ `indirect_subserializer=7` แต่ A2 V1 ที่วัดจริงมี 0 แถวประเภทนี้
- รายงาน V1 ไม่แจกแจง `call_clobber` ของ 5 messages: `GSCN_RunTimeProtocolReq`, `GSCN_RunTimeProtocolRes`, `GSCN_LoginProtocol`, `LSCN_Protocol`, `VitalProtocol`

Errata นี้ไม่แก้ไฟล์ V1 และไม่เปลี่ยน provenance ของแถวเดิม

## 10. ขอบเขตและการส่งมอบ

- อ่าน GameClient เท่านั้น; ไม่มีการรัน client/server
- ไม่มีการเขียนหรือแก้ server code, workflow หรือ game-test queue
- เขียนผลเฉพาะ `pf_bridge/external`
- ไม่มี raw dump bytes, capture bytes, payload, field value, hexdump หรือ proprietary input ถูกคัดลอกลงผลลัพธ์
- `GameClient.local.bin` ที่ pin: size 14,759,424; SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

🔴 ไฟล์ V2 ใน `pf_bridge/external` เป็น local-only และถูกกฎ ignore ของ repository กันไว้อยู่ ผู้ออกใบสั่งที่เข้าถึงเครื่อง/โฟลเดอร์นี้อ่านได้ครบ แต่ clean clone หรือ remote จะไม่ได้ V2 อัตโนมัติ ต้องขออนุมัติช่องทางส่งมอบแบบ sanitized แยกต่างหากก่อนนำออกจากเครื่อง

## 11. ลำดับอ่าน

1. `PF_V2_MANIFEST.md` — checkpoint, namespace และ hash ทั้งชุด
2. `PF_V2_FIELD_VALIDATION.md` / `.tsv` — A5 mismatch
3. `PF_V2_EFFECTIVE_STATUS.md` / `PF_V2_P1_OPEN.tsv` — สถานะ IMAGE-static และสิ่งที่ยังเปิด
4. ไฟล์ correction/closure/blocker `.md` ของแต่ละ overlay
5. V1 `PF_HANDOFF_V1.md` และ `PF_V1_MANIFEST.md` สำหรับฐาน immutable

การตรวจซ้ำทุกครั้งให้ใช้ generator `--check`; manifest เป็นตัวปิด checkpoint และต้องสร้างเป็นขั้นสุดท้ายหลังไฟล์อื่นนิ่งแล้ว
