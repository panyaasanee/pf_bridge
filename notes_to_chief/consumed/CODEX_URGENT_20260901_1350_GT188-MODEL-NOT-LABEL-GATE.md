[ถึง: chief, LANE-B · cc: Panya, COO · จาก: OpenAI Codex static RE]

# URGENT — GT-188 ต้องห้ามผ่านด้วย label อย่างเดียว

พบจุดที่อาจทำให้ P-1 ได้ผลเขียวผิดเป้าหมาย: `GAME_TEST_QUEUE.md:9425` เขียนว่าให้ผ่านเมื่อ “drop/label” ยังอยู่ที่ STEP-B/C ซึ่งอนุญาตให้ **ป้ายตัวหนังสืออย่างเดียว** ผ่านได้ แต่คำสั่งเจ้าของต้องการ item model ถูกวาดบนพื้นและมองเห็นนานพอเดินไปเก็บ.

- **[ORIGINAL EVIDENCE: DATA]** `PF_GROUND_DROP_LIFETIME.tsv` แถว `GDL-DATA-003` decode+parse asset `.ni_` 13 ชุดแบบ deterministic: root `NiNode` 13/13 และ root graphถึง `NiMesh` 13/13. Packaged filesมี geometryจริง ไม่ใช่มีเพียงชื่อ.
- **[ORIGINAL EVIDENCE: IMAGE]** `GDL-IMG-022` ปิด `wrapper+0x84`→retain→world registration→recursive NiNode activationแบบ static แต่ยังไม่พิสูจน์ actual runtime load/renderer/pixels.
- **ผลกระทบ:** ถ้า STEP-A/B/C เห็นแต่ label แล้วติ๊ก PASS ทีมจะปิด milestoneคนละเรื่องกับที่ Panya สั่ง และจะซ่อนคอขวด actual resource→scene→renderer.
- **ข้อเสนอให้เจ้าของคิวแก้เอง:** PASS ชั้นจอต้องเห็น **non-text item geometry/model** แยกจาก labelที่ STEP-A, STEP-B และ STEP-C พร้อมยืนยัน same object. ถ้า STEP-A ไม่มี model ให้ลง `NO-RESULT` สำหรับคำถาม lifetimeของ model และบันทึก label lifetimeแยก ห้ามนับฝุ่น เงา หรือข้อความเป็น model.

หลักฐาน canonical: `pf_bridge\external\PF_GROUND_DROP_LIFETIME.tsv` 59,965 B SHA-256 `d889460b8d4c1c4f69b1df349f59ac2dae950c6373ee170915e5f5f2fa94e059`; report 18,946 B SHA-256 `266067b57fae3b5cb742eb7c1565210d31e11cfb7ed3586f9ef5f2fa033ecc32`.

Codexไม่ได้แก้ `GAME_TEST_QUEUE.md`, ServerProject หรือ runtime; ใบนี้เป็นคำเตือนให้ chief/LANE-B แก้เกณฑ์ในเขตของตน.
