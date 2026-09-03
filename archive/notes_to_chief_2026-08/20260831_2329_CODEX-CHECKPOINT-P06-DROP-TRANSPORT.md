[ถึง: Panya / ผู้ออกใบสั่ง / chief · จาก: OpenAI Codex]

# CODEX CHECKPOINT P0-6 — DROP TRANSPORT · PARTIAL

- เวลา checkpoint: `2026-08-31 23:29 +07:00`
- generation: `3578f2aa13fcf22e4e47ca80f4acbfe38a82b38ca5a636798fdfd40995ced6ff`
- image: `GameClient.local.bin`, 14,759,424 ไบต์, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- สถานะรวม P0-6: `PARTIAL` — ปิดขา pickup request แบบ static ถึง buffer encoding; persistent server-to-client ground object ยังเปิด
- รอบนี้ไม่แก้/รัน ServerProject, server, เกม, dump หรือ capture และไม่ commit/push

## ทำอะไรไป

1. พิสูจน์สาย IMAGE แบบ bounded: click producer สร้าง `PickupTerrainThing` → เก็บในคิว `session/controller+0x150` → ห่อใน outer protocol → ผ่าน ready branch ของ transport queue → pump ภายหลัง → outer/nested buffer encoder
2. ปิด `PickupTerrainThing` assigned runtime type ID เป็น `0x4543` บน successful 519-stub registration path: 519 ชื่อ / 519 ID ไม่ซ้ำ / collision 0
3. แยก outer สองทาง: gameplay `GSCN_RunTimeProtocolReq=0x6E6F`; login alternative `GSCN_LoginProtocol=0x453A`
4. ยืนยันว่าค่าทั้งสามเป็น **runtime type ID**; `wire_opcode=UNKNOWN` และห้ามใช้ `0x4543` เป็น top-level opcode
5. ปิด custom-reflection parent/metadata: `FightingDropModule_Client -> ClientModule`, size `0x34`; `FightingDropNotify -> VitalData`, size `0x50`; descriptor vtable เป็น metadata ไม่ใช่ wire vtable
6. ปฏิเสธ false lead `TreasurePointAttr`/`ActorTreasureHuntExcavatingInfoAttr`; ไม่ยืม codec ใกล้สตริงไปตั้ง payload ของ FightingDrop
7. เพิ่ม `PF_GROUND_DROP_TRANSPORT.tsv/.md` เข้า content-addressed generation และแก้ RE-125 แบบไม่ย้อนแก้ไฟล์ประวัติ

## สถานะที่เปลี่ยนจาก P0-5

- Attr field semantic/status/scope: **0 แถวเปลี่ยน**; `PF_ATTR_FIELD_SEMANTICS.tsv` ยัง 490 แถวและ SHA-256 `1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f`
- Class parent: **1 คลาสเปลี่ยน** — `FightingDropModule_Client` จาก `UNKNOWN` เป็น `PROVEN_EXACT / ClientModule`; parent exact รวม 130→131, unknown 10→9
- ความรู้ P0-6 เปลี่ยน **3 กลุ่ม**: assigned Pickup ID, outer/envelope+encoder สอง path, FightingDrop hierarchy/size
- Artifact count: **44→46**
- Conflict rows: **1,285→1,286**; OPEN คง **640**, non-OPEN **645→646**
- Unresolved ledger: **976 คงเดิม** — parent ปิดแล้วแต่ concrete FightingDrop codec/transport blocker ยังอยู่
- Quarantine: **0 data rows**

## Conflict ที่กระทบการต่อสายจริง (5 ข้อ)

1. RE-125 ส่วนที่ว่า `0x4543` เป็นเพียงค่าจากชื่อและ static ไปไม่ถึง assigned ID ถูกถอนด้วย conflict `c49b824a…`; ผล CAPTURE เดิมว่า corpus ไม่พบยังคงอยู่และแยกชั้นหลักฐาน
2. `0x4543` เป็น nested runtime ID; gameplay/login outer runtime IDs คือ `0x6E6F`/`0x453A`. การนำค่าใดค่าหนึ่งไปลงทะเบียนเป็น top-level opcode จะผิดชั้น
3. `A8D500` enqueue เฉพาะ ready branch; refusal branch release object. ทั้งสองคืน 0 และ caller ที่ตรวจไม่อ่าน EAX จึงห้ามอ้างว่า live request ถูกยอมรับทุกครั้ง
4. Exact A1 getter/vtable/slot census “ไม่พบ canonical surface” ของ `FightingDrop*` เป็น bounded negative ไม่ใช่ข้อพิสูจน์ว่า transport ไม่มี
5. รอบนี้ไม่พบ production server defect ใหม่; open server-code semantic conflicts เดิมยัง 5 รายการ และไม่มี `CODEX_URGENT_` ใหม่

## หลักฐานและการสร้างซ้ำ

- `PF_GROUND_DROP_TRANSPORT.tsv`: 19 IMAGE rows = canonical reference 9 + new evidence 10
- canonical targets 9/9 unique; new evidence keys 10/10 unique; primary span tuples 10/10 unique; exported IMAGE spans 39 จุด re-hash ผ่าน
- opcode/status pairs มีเพียง `UNKNOWN -> NOT_ESTABLISHED_BY_IMAGE` 17 แถว และ `N/A -> NOT_APPLICABLE` 2 แถว
- ไม่มี CAPTURE/DUMP/DATA ปนใน P0-6 TSV
- generator รันสองรอบได้ generation ID เดิม; independent adversarial/read-only review ตรวจ manifest, 46/46 hashes/sizes/mirrors, generator snapshot, canonical digests, conflict/parent linkage และ checkpoint reader ผ่าน
- generation ระหว่างทาง `a62db354…` และ `d01e7f6f…` ถูก supersede; authoritative top manifest ชี้ `3578f2aa…` เท่านั้น

## สิ่งที่ยังเปิดและทางเดินต่อ

คำถามเดียวที่ P0-6 ยังตอบไม่ได้คือ original server-to-client producer/class ใดสร้าง persistent clickable ground object ที่ป้อน element ให้ click branch และ state ใดเป็นผู้ถอดมันออก. ต้องการ exact concrete wire getter/vtable/serializer/receiver/producer chain หรือหลักฐาน wire แยก source ที่มี issuance/lifetime/remove/claim จริง. ห้ามเดา payload และห้ามเสนอ resend ซ้ำ

ตาม stop rule งาน P0-6 ปล่อยเป็น `PARTIAL` พร้อม blocker แล้วเดิน P0-7 ต่อ: แยก `f_SCALE`, dimensions (`n_BOUNDARY`/`n_HEIGHT`) และ outfit/initial-action selection; ห้ามย้อนผูก scale กลับ `BasicAttr+0x54`

## ไฟล์ผล local-authoritative

- `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_GENERATION_MANIFEST.json` — 7,913 ไบต์ — SHA-256 `41204f5bf3e106020a8ed947564f7b25f268cf8cf60d15229fd100928b05ae18`
- `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\pf_rederive_attr_semantics.py` — 1,388,594 ไบต์ — SHA-256 `26226adfe8da34b5a38c91a29ed32ca03c5f6f37dfd331f3826c4694f9ccb947`
- generation `...\.pf_attr_generations\3578f2aa13fcf22e4e47ca80f4acbfe38a82b38ca5a636798fdfd40995ced6ff\PF_GROUND_DROP_TRANSPORT.tsv` — 26,924 ไบต์ — SHA-256 `9e2396795ee32287f1f9b82f22fb8f394464d2b0a25375d07108ee138c73907b`
- generation `...\PF_GROUND_DROP_TRANSPORT.md` — 2,779 ไบต์ — SHA-256 `e2b1b90efcd63cfb6878f47937a466424d872809599a04718c75e6d7940c38c5`
- generation `...\PF_ATTR_CLASS_CENSUS.tsv` — 120,388 ไบต์ — SHA-256 `82b02f402005ba7b1d51a97e0eaba2bc89dcfdf884d91ecd61bd3542972efa11`
- generation `...\PF_ATTR_REMAINING_CODEC_CENSUS.tsv` — 135,056 ไบต์ — SHA-256 `3b5584002e4f87289f491576789c423779ea2756ca932cc7d0d1f3e8c1ff34e1`
- generation `...\PF_ATTR_CONFLICTS.tsv` — 3,531,496 ไบต์ — SHA-256 `d7cf844d1c61afec1c1b7a15411a77b5c21dd3afd55c0e7db0b73f9d8f9654dc`
- `C:\Users\Panya\Desktop\Pirate Force\Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md` — 92,551 ไบต์ก่อนเขียน checkpoint นี้ — SHA-256 `7bcbef60e9d058d38bb74f86802e4cb691c5b54fd295f2c867582af4040bc83c`
- snapshot ก่อนแก้ `C:\Users\Panya\Desktop\Pirate Force\audit_history\Pirate_Force_Codex_Audit_Recommendations.105cc7692579_20260831_2257.md` — 86,734 ไบต์ — SHA-256 `2d5241220c4a4b15528906e3e840edadbf1ff6bc25150bd613a3173afeeae4f4`

ไฟล์ทั้งหมดข้างต้นยังเป็น local external/audit artifacts ไม่ใช่ committed/released package. รายงานหลักคงสถานะ `HOLD FOR PANYA`
