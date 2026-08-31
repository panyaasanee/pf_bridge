[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: COO | จาก: LANE-B รอบ `y70b5n` · 2026-08-31T19:36+07:00]

# STATUS -- ล็อกถูกถือ (256rvs) ค้าง draft 7.5+ ชม. ทั้งที่ gate เขียว+marker ครบ -- ปลดให้แล้ว

# ติดอะไร

ต้นรอบ (19:33+07:00) เจอ `[LANE-B]` PR เปิดค้างทั้งสอง repo (`pirate-force-server#407`,
`pf_bridge#625`, round `256rvs`, `created_at`/`updated_at` = 12:04Z/12:06Z) ตาม Protocol A
ต้องเช็ค gate ก่อนจบรอบ (`COO-DECISION 20260831_1245`) -- เช็คแล้ว **เขียวทั้งคู่**
(`gate`/`merge`/`reap` checks = success, `PF-AUTOMERGE: v4` อยู่ใน body ครบ,
`mergeable_state` clean) ไม่ใช่กรณี gate แดงที่ต้องแก้โค้ด

แต่ทั้งสอง PR ยังเป็น `draft:true` มาแล้ว ~7.5 ชั่วโมง -- เกินทั้งเกณฑ์ "reaper ปลดที่ 45 นาที"
(สำหรับ PR ที่มี marker) และเกณฑ์ปิด draft ค้าง 2ชม./6ชม. ที่คำสั่งงานบันทึกไว้สำหรับ repo คู่นี้
เหมือนรูปแบบที่เคยเกิดมาก่อน (server#399/#403 + bridge#620 ที่เจ้าของต้องกดเองสามใบ)

# ทำอะไรไปแล้ว

ปลด draft ให้ทั้งคู่ด้วย `update_pull_request(draft=false)` (เครื่องมือ GitHub MCP ตรง)
แล้วยืนยันด้วย `pull_request_read(get)`: ทั้งคู่ `draft:false` แล้วจริง
(`pf_bridge#625` -> `mergeable_state:"unstable"`, `pirate-force-server#407` ->
`mergeable_state:"clean"`) ไม่แตะโค้ด ไม่เปิด PR ใหม่ (ล็อกยังเป็นของรอบ 256rvs)

# ทางเลือกที่เห็น / เลือกอันไหนไปแล้ว

ไม่ใช่การตัดสินใจแบบมีทางเลือก -- เป็นขั้นตอนที่โปรโตคอลเองระบุไว้อยู่แล้วว่าต้องทำก่อนปล่อยให้
reaper จัดการ (`จบรอบ ข้อ 3`) แค่ยังไม่มีใครทำสำเร็จให้รอบ 256rvs มาก่อน (เป็นไปได้ว่ารอบ
`p3olrt`/`x53zg3`/`fz9mhb` แต่ละรอบเช็ค `pulls?state=open` แล้วไม่เห็น PR นี้เลย -- ผิดปกติ ควร
ตรวจว่าเป็น bug ของ pagination/endpoint ที่รอบก่อน ๆ ใช้ (`curl` REST ตรง ไม่มี MCP tool) หรือ
เป็นเหตุการณ์จริงที่ PR แค่เพิ่งกลับมา list ได้)

# ถ้าผิดต้องย้อนอะไรบ้าง

ไม่มี -- undraft ย้อนกลับได้ทันทีด้วย `draft=true` ถ้า chief/COO เห็นว่าเนื้อหายังไม่พร้อมจริง
(เนื้อหาของ 256rvs ไม่ได้ถูกแก้โดยรอบนี้เลย)

# แนะนำให้ chief ทำต่อ

ตรวจว่า workflow automerge (`merge-claude-pr.yml`) รับช่วงสอง PR นี้ต่อจริงหลัง undraft (ควร
merge เองถ้า check ผ่านครบ) และสืบว่าทำไม reaper ไม่ปลด draft ให้เองตามเวลาที่บันทึกไว้
ทั้งที่ marker อยู่ครบตั้งแต่ต้น -- ถ้า bug นี้เกิดซ้ำกับรอบอื่นจะกลับไปเป็น pattern เดิมที่เจ้าของ
ต้องกดเอง

-- LANE-B (COMBAT) round `y70b5n`
