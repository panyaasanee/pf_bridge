# CODEX CHECKPOINT — P0-1 Attr scope / A2 / manifest V4

วันที่ 31 สิงหาคม 2026 เวลาโดยประมาณ 16:05 +07:00

## สรุปผลที่ต้องรู้ก่อน

P0-1 ปิดได้ในชั้น static IMAGE: ข้อกังวลเดิมว่า `BasicAttr +0x54` ของ `CNetNPC` เป็น `f_SCALE` ถูกหักล้าง หลักฐานแยก consumer ยืนยันว่าเส้น `CNetNPC` รับ `MOBS.n_SPEED_WALK` ไปเป็นค่าเริ่มต้นของการเคลื่อนที่แนวนอน ส่วนอีกเส้นเป็น input ของสูตร run speed แต่ concrete owner ยังไม่ทราบ ดังนั้นการส่ง `speed_walk` เป็น movement speed ในโค้ดที่รันอยู่ **ยังไม่ถูกพิสูจน์ว่าผิดจากประเด็นนี้** และไม่มีจดหมายด่วนให้แก้ runtime

IMAGE ที่ใช้: `GameClient.local.bin`, 14,759,424 ไบต์, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` ตรวจซ้ำหลังจบรอบแล้วตรงค่าบังคับ

## ทำอะไรไป

- ตรวจ directional field ทั้ง 480 แถวใหม่โดยแยกแกน `semantic_status` ออกจาก `scope_status` และเพิ่มหลักฐาน concrete-class แบบ fail-closed
- พิสูจน์ typed scope 46 แถวด้วย descriptor/span/pointer/call-edge/instruction chain ที่ผูก hash ครบ; scope รวมเป็น EXACT 270 / UNKNOWN 210
- ทำ A2 ใหม่จาก current scoped evidence ไม่ใช้ origin key เก่าตัดสิน publication; 196 แถว เชื่อม field ปัจจุบันครบทุกคอลัมน์, `server_safe=YES` 26 / `NO` 170
- รวม unresolved เป็น ledger เดียว 963 แถว โดยแยก active claim 453 ออกจาก conflict-only work item 510 เพื่อไม่เรียกงาน conflict ว่า UNKNOWN field
- ตรวจ conflict 1,274 แถว: OPEN 635 / non-OPEN 639; OPEN ทุก key ปรากฏใน unresolved exactly once
- ทดสอบ quarantine แบบฉีด blank/malformed evidence: แถวเสียถูกกักและไม่รั่วเข้า delta, conflict หรือ A2; generation จริงมี quarantine 0 แถว
- ออก manifest V4 ที่ผูก publication rule เข้ากับ generation ID, ตรวจย้อนหลัง V3 22 generation และ V2 1 generation ได้
- ออกคู่มือ server จาก predicate เดียวกับ TSV และแจกแจงครบ 480 แถว: SAFE 93 / WITHHELD 387

## ฟิลด์ที่เปลี่ยนสถานะ

- Semantic/scope delta รวม 290 แถว: existing row เปลี่ยน semantic และ/หรือ scope/evidence 284 แถว และเพิ่ม scoped row ใหม่ 6 แถว
- ใน 284 แถวเดิม มี 68 แถวที่ semantic status เปลี่ยนจริง; อีก 216 แถวคง semantic label เดิมแต่แก้ scope/evidence/provenance ให้ fail-closed
- สถานะสะสมปัจจุบัน: `PROVEN_EXACT` 223, `PROVEN_ROLE_ONLY` 188, `PARTIAL` 27, `UNKNOWN` 42 จาก 480 แถว
- ใช้ต่อสายได้ตามกฎสามแกน (`semantic exact + scope exact + ไม่มี OPEN conflict`) 93 แถว; กันไว้ 387 แถว

## Conflict ที่กระทบการต่อสายจริง (เรียงตามผลกระทบ; ไม่เกิน 10 บรรทัด)

1. `BasicAttr +0x54`: false premise ถูกหักล้าง—เส้น `CNetNPC` คือ `n_SPEED_WALK`; ห้ามเปลี่ยน runtime เป็น scale จากข้อกังวลเดิม
2. เส้น Fight ของ `BasicAttr +0x54` รู้บทบาท run-speed formula แต่ concrete owner ยัง UNKNOWN; ห้ามยก mapping ของ `CNetNPC` ไปใช้กับ actor subtype อื่น
3. มี 16 แถวที่ semantic และ scope เป็น EXACT ทั้งคู่แต่ยังมี OPEN conflict; จึงต้อง WITHHOLD แม้ชื่อ field ดูพร้อมใช้
4. `CSkillAttr` ปลอดภัยเฉพาะฝั่ง R ของ count carrier `CSkillAttr.entry_count#R`; อีก 7 directional rows ยัง WITHHELD ห้ามตีความเป็น layout ของ skill ทั้งก้อน
5. `MOBS.f_SCALE` มี IMAGE/DATA cross-source mismatch 2 แถวที่เก็บแยก source; ห้ามรวมเป็นข้อเท็จจริงชั้นเดียวหรือแก้ให้เข้ากันเอง
6. Artifact ชุดนี้เป็น local-only และไม่ถูก ServerProject Git ติดตาม; หากต้องส่งข้ามเครื่องต้องอนุมัติ packaging/ingest ที่เก็บ manifest, generator snapshot, reader และ generation directory เป็นชุดเดียว

## ตัวเลขงานเปิด

- Unresolved 963 แถว = active claims 453 + standalone conflict work items 510
- Active claims 453 = field 387 + runtime 7 + container 32 + class-link/codec 10 + empty-codec closure 17
- OPEN conflicts 635 = rederived IMAGE 616 + ต้องวัด NOT_WIRE 17 + cross-source 2
- Probe requests 0 แถว เพราะยังไม่มี proposal ผ่าน intake contract ครบ ไม่ได้หมายความว่าไม่มี unresolved work

## ผลลัพธ์และขนาดไฟล์

Generation ID: `0e9cb92bb01b6b2255dc2284ae582347cd0f97765ac6128675d01e82aad376bd`

Generation directory:
`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\.pf_attr_generations\0e9cb92bb01b6b2255dc2284ae582347cd0f97765ac6128675d01e82aad376bd\`

- 39 artifact ที่ manifest ผูก hash; 13,756,444 ไบต์ ไม่รวม `manifest.json`
- 40 ไฟล์รวม `manifest.json`; 13,763,338 ไบต์
- `manifest.json` — 6,894 ไบต์ (มีรายการ/hash/size ของ artifact ทั้ง 39 ไฟล์)
- `PF_ATTR_FIELD_SEMANTICS.tsv` — 1,309,380 ไบต์
- `PF_ATTR_CONFLICTS.tsv` — 3,520,750 ไบต์
- `PF_ATTR_UNRESOLVED.tsv` — 2,344,168 ไบต์
- `PF_A2_ATTR_FIELD_DELTA.tsv` — 448,710 ไบต์
- `PF_ATTR_FOR_SERVER.md` — 118,976 ไบต์
- `PF_ATTR_SEMANTIC_REPORT.md` — 32,044 ไบต์
- `PF_ATTR_QUARANTINE.tsv` — 343 ไบต์ (header, 0 data row)
- `PF_ATTR_PROBE_REQUESTS.tsv` — 151 ไบต์ (header, 0 data row)

ไฟล์ re-derive/verify ที่ต้องเก็บคู่กัน:

- `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\pf_rederive_attr_semantics.py` — 1,069,745 ไบต์
- `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\pf_attr_checkpoint_reader.py` — 26,393 ไบต์
- `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_GENERATION_MANIFEST.json` — 6,894 ไบต์

รายงาน audit ที่อัปเดตไฟล์เดิมและยังคง `HOLD FOR PANYA`:

- `C:\Users\Panya\Desktop\Pirate Force\Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md` — 53,509 ไบต์

## การตรวจรับ

- authoritative reader ผ่าน: generation ID และ artifact count ตรง
- สร้างซ้ำสองรอบได้ generation ID เดิม
- cross-file key/source/schema/hash/size และ A2 current-linkage ผ่าน
- fault test ของ quarantine, publication rule tamper, path ที่มีช่องว่าง และ atomic lock ผ่าน
- adversarial review รอบสุดท้ายไม่พบ concrete blocker

ข้อที่ยังต้องให้เจ้าของตัดสินในอนาคตมีเพียงด้านการส่งมอบถาวรข้ามเครื่อง เพราะข้อจำกัดรอบนี้ห้ามแตะ ServerProject/Git; รอบแกะถัดไปเดินต่อ P0-2 selector สีชื่อ NPC/มอนสเตอร์ได้ทันที
