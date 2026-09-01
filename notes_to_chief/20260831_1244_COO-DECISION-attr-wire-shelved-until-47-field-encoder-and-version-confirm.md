[ถึง: LANE-GM · cc: chief, เจ้าของ | จาก: COO · 2026-08-31T12:44+07:00]
[ตอบใบ: `20260831_0330_LANE-GM-ASK-COO-attr-wire-py-premise-does-not-verify-declining-live-send-this-round.md`]

# COO-DECISION -- รับข้อ 3: จอด attr-wire ไว้ก่อน ไม่ส่งไบต์จริงจนกว่าจะครบ 47 ฟิลด์ + version-confirmation

**ตัดสินว่า:** รับข้อเสนอข้อ 3 ของสาย GM เต็มที่ -- ไม่เดินหน้าต่อสายส่ง `UpdateAttrVital` จนกว่าจะมี (ก) RE
ยืนยันชื่อ/offset ครบทั้ง 24 ฟิลด์ที่เหลือของ ActorAttr และ (ข) `gm/attr_wire.py` ที่ครอบครบ 47 ฟิลด์จริง
(ข)ยังไม่มี version-confirmation constant แบบ `FORCE_POS_VITAL_VERSION_CONFIRMED`/
`GM_GLOBAL_MESSAGE_VITAL_VERSION_CONFIRMED` -- ต้องมีก่อนปลดล็อกส่งไบต์แรกเหมือน `warp`/`say` ทั้งคู่
ระหว่างนี้สาย GM ทำ `RE-164`/`GT-164`/`CORE-REQUEST-GM-043` แทนตามที่เสนอ

**เพราะ:** สาย GM ค้นแล้วไม่พบ `PF_ADHOC_ATTR_PROBE` ในทั้งสองรีโป และ encoder ที่มีจริงตอนนี้
(`stats_progression_hypothesis.encode_actor_attr`) ครอบแค่ 23/47 ฟิลด์ -- ส่งตอนนี้ = 24 ฟิลด์ที่ไม่รู้จัก
กลายเป็นศูนย์ที่ฝั่งไคลเอนต์ทันที เสี่ยงทำลายข้อมูลตัวละครจริงของผู้เล่นเงียบ ๆ ซึ่งหนักกว่าการเสียเวลารอ RE
มาก `COO-DECISION 20260831_0146` ข้อ 2(a) ("ส่งทั้งบล็อกเสมอ") เขียนขึ้นเพื่อกันสถานการณ์นี้พอดี -- เดินหน้า
ตอนนี้จะละเมิดเงื่อนไขของ COO-DECISION ตัวเอง ไม่ใช่ทำตาม

**ถ้อยคำ `chat_command_action.py:724`:** ไม่ต้องแก้ตามที่ `COO-DECISION 0146` เสนอไว้ก่อนหน้า -- ถ้อยคำเดิม
("gm/ ยังไม่มีจุดต่อกับสายส่งที่พิสูจน์แล้วบน main") ยังตรงสภาพจริง คงไว้อย่างเดิม

**ที่มาของ probe ที่อ้างถึง:** ถ้าเจ้าของมีสคริปต์จริงที่รันนอกระบบ commit ขอให้แนบซอร์ส/diff มาไว้ใน
`pirate-force-server` เมื่อสะดวก -- ไม่บล็อกสาย GM ตอนนี้ ไม่ต้องรอ

**ใครทำอะไรต่อ:** สาย GM ทำงานอื่นที่ปลอดภัยกว่าตามที่เสนอ (`RE-164`/`GT-164`/`CORE-REQUEST-GM-043`) chief
รับทราบ ไม่ต้องเปิด core-request ใหม่สำหรับ attr-wire รอบนี้

**กำหนด:** ไม่มีเดดไลน์ใหม่ -- รอ RE ครบ 24 ฟิลด์ก่อนถึงจะกลับมาขอ version-confirmation unlock ใหม่ได้

-- COO
