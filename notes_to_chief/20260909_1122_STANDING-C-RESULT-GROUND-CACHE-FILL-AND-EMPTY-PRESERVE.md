งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B, LANE-A/CORE, LANE-GM, LANE-K, chief และ Panya · จาก Codex static RE
C1b · ปิด 2026-09-09T11:22:58.137240+07:00 · IMAGE A / composition D · PARTIAL: ปิด cache-fill ของสีของตก; ยังไม่มี native pixels

**ผลที่เพิ่มจาก C1a:** gate/seed ที่ไม่ได้ส่งสามารถสืบค่าจาก ground collection ก่อนหน้าได้. แต่ **PRESERVE ที่ส่ง collection ว่างรักษาของบนพื้น ไม่ได้รักษาแคช Attr**. ดังนั้นต้องแยกค่าหลัง decode, หลัง fill และค่าที่ผู้เล่นเห็น

เชน IMAGE:
- RuntimeRes handler5E4060 เรียก5DCB40ก่อนนำ ground ไปใช้. getter5DC9B0 คืน incoming+20. ถ้า app+158 และ incoming+20 มีค่า:5DCC4E→5F8490(incoming,&old).
- 5F8490 เดินรายการใหม่ ค้น old ด้วย key32 ที่ TerrainThing+10 ผ่าน5F8400. พบแล้ว5F8581→5F81E0(new,old). ไม่เทียบ item+14 จึงเป็น identity key ของของตก ไม่ใช่ไอเทม template.
- 5F81E0 ตรวจ type node1082578 แล้วอ่าน new.mask+28: ขาด08→คัด gate+1B จาก old ที่5F8230; ขาด20→คัด seed+1A ที่5F8250.
- app+158 ถูกแทนด้วย incoming+20 ที่5DCC8D. ไม่มีฐานสะสมราย key ข้ามทุกเฟรม; cache ว่าง/null/key ขาดย่อมไม่ช่วยเติมเฟรมถัดไป.
field_key: `TerrainThing@0x1B.1#R:b0x08`, `TerrainThing@0x1A.1#R:b0x20`; mask+28 แยกจากฟิลด์

**null ต่างจาก empty อย่างไร (เมื่อ local player/world/component type gates ผ่าน):**
1. derived bit08 ไม่มีบน fresh RuntimeRes → ground pointer20=null. เส้น5E40D5→5F53A0→6AF970 ยังส่ง null เข้าไป. 6AF9AE→6B024F เข้าทางล้างรายการของตก: 6B034F→B0EE40,6B0368→5E0D40,6B0398→5E0560 และ6B03A6 ตั้ง map size0. ไม่อ้าง pixels.
2. bit08 มี + count tag12/u16=0 → pool objectมีจริงแต่ map count+2C=0. 6AF9B4/6AF9BF กระโดด6B03BC ออกจาก reconcile ก่อนเดินลบ/อัปเดต. **app158 ถูกแทนด้วย empty object แล้ว** แม้ของและรูปแบบสีเดิมยังไม่ได้รับการอัปเดตจากฟังก์ชันนี้.
3. collectionไม่ว่าง → reconcileตาม key set; keyที่ขาดยังเสี่ยงถูกลบตาม C1a/RE-130. ฟิลด์ delta ไม่อนุญาตตัด keyของผู้เล่นคนอื่นออก

ตัวอย่าง D ที่ reconstruct จาก gates (item n_QUALITY2, model/label/world gates ผ่าน; incoming XYZ ตรงกับ reference actor จึง distance=0):
| ลำดับ | ฐานสีหลัง fill | ผลแบบมีเงื่อนไข |
|---|---|---|
| key7 explicit mask3E gate1 seed2 → key7 mask16 | สืบ1/2 | คง style94; fieldsเท่ากันอาจไม่เรียก update |
| key7 explicit → present-empty PRESERVE → key7 mask16 | ไม่มี old key; default0/1 | style52 แดงอุ่น |
| key7 explicit → key7 mask3E gate0 seed2 | บิต08ระบุ0จริง | style52 |
| key7 explicit → keyใหม่ mask16 | ไม่มีฐาน keyใหม่ | style52 |
| keyเดิม เปลี่ยน item template โดยไม่ส่ง gate/seed | สืบจาก old key แม้ itemต่าง | updateยังใช้ n_QUALITYของ itemใหม่เมื่อ seed>0 |
style/RGB/create-update: C1a; static only

**ผูกกับโค้ดที่มีอยู่:** `mob_loot.py:5245` preserve_ground_heartbeat_pc ประกอบ derived08 + count0 จริง (ตรวจ AST โดยไม่รันโมดูล). เป็นรูปที่ตรงข้อ2 จึงไม่ใช่ฐานเก็บสีสำหรับ sparse update ถัดไป. ข้อเสนอเพิ่ม rarity ต้องส่ง gate/seed ชัดในทุก generation ที่อาจตามหลัง PRESERVE ไม่ใช่ส่งครั้งแรกแล้วพึ่ง inheritance. สอง encoderเดิมใช้12/16 ไม่ส่งสองบิตนี้; staticผลนี้ไม่พิสูจน์ว่าเป็นสาเหตุของสีส้มใน footageเจ้าของ

แก้เพดาน C1a: ประโยค freshly decoded omission retains0 ใช้ได้ **ก่อน5F81E0**; ผลหลังmergeอาจเป็น1. คำเตือนอย่าสันนิษฐานว่าค่าเดิมรอดยังถูก แต่ไม่ใช่ข้อพิสูจน์ว่ามันไม่มีทางรอด. null/emptyเป็นฐานเก่า RE-082/130; ใหม่คือgate/seed/cache. D1a ก็มีข้อควรระวังร่วม: RuntimeRes bit08-only นี้ไม่มี actorcollection จึงทำให้ app154=null ด้วย

Search: staged/standing_c1b_search.log (five domains; QME-IMG-011 shape only). V141 frozen.
Distance gate: 6AF9F7→432510(0) false + distance squared >[1086B0C] at6AFBC8→6AFBCE→6AFBF5 removes before style. Scene must hold XYZ at reference actor. Unchanged gate/seed/key/item/XYZ skips update via6AFC5D..6AFD74.

IMAGE SHA 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623. spans end-exclusive:
- TerrainThing.fill: VA 005F81E0..005F8258, file 001F75E0, SHA `61ff4fee022056130a1f04e47edb585bb7277832979287407267d46f88a51e52`
- ground.reconcile: VA 006AF970..006B03E3, file 002AED70, SHA `e5eb9e1fdae15544773c7e94fa6ff6aaa6990650cbb05f20e39a009941575663`
20spansครบใน staged/standing_c1b_manifest.json SHA 287a75b09f26432b0af3291a3c26430090e1d2d6dca78d3a6444156c3b7d1451
verifier SHA a3193ffdac4f29023634efc19da012d9ea242246dd7dd1d864ebf739824cabf0; verify.log SHA b44a0f71a432e6217142b3d2398935d3ebeacd73d5cd72cd256b55e2b5bfd3f4
PASS20 spans/17 ranges/2355 instructions/6 inputs/22 calls/90 pins/1 vslot/6 style IDs/1 AST shape/16 fill cases/6 sequence controls/4 reconcile gates. Reconstruction ไม่ใช่ native replay
Frozen review: P2 distance/equality gates corrected; offline verifier rerun exit0. No native pass.
BUILD_IMPACT: generation ที่ตาม PRESERVE ต้องพกสีเอง; emptyไม่ควรถูกเข้าใจว่าเก็บฐานfield-delta
BUILD_PROPOSED: เติม gate08/seed20 ทุก ground generation ที่ต้องการrarity พร้อมคง full key set | LANE-B + CORE | explicit→sparse เทียบ explicit→PRESERVE→sparse แล้ว explicit→PRESERVE→explicit; XYZตรงreference actor; ownerยืนยันสีหลังrefreshและไอเทมอีกคนไม่หาย
nonclaims: ไม่อ้าง original frame/policy, native color/removal, arbitrary aliases, item quality persistence หรือ reconnect. ไม่แก้ src/DB/lease/Git/คิว; ไม่รัน client/server; job9xxไม่ใช้
SCOREBOARD: NONE | Standing C IMAGE evidence | no runtime promotion
