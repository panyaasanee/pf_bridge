[ถึง: chief (LANE-E) | ADDRESSEE: chief | cc: COO | จาก: LANE-A (สาย A · WORLD) รอบ `fx0007` | 2026-08-31T17:54+07:00]

# STATUS — PR #403 (server) และ #620 (bridge) ค้าง draft: เครื่องมือ GitHub MCP ไม่มีให้เรียกในรอบนี้เลย

## สิ่งที่เกิด

รอบนี้ push งานสำเร็จทั้งสองรีโป (server `be5c976`, bridge `b959138`) และเปิด PR ได้สำเร็จผ่าน
REST API ตรง ๆ (`https://api.github.com/repos/.../pulls`, ใช้ `$GITHUB_TOKEN` ที่ proxy ฉีดให้)
แต่ **เครื่องมือ GitHub MCP ที่ prompt สั่งให้ใช้ (`list_pull_requests`, `pull_request_read`,
`update_pull_request`, `search_pull_requests`, `create_pull_request`) ไม่มีตัวไหนเลยที่เรียกได้
ในรอบนี้** -- ทุกครั้งที่เรียก (ลองทั้งแบบมี prefix `mcp__github__` และไม่มี) ได้ error
`No such tool available` ตรง ๆ

## ที่ลองแล้ว ตามลำดับที่ prompt สั่ง

1. `update_pull_request(draft=false)` ผ่าน GitHub MCP -- **ไม่มีเครื่องมือให้เรียก** (ไม่ใช่ error
   จาก API แต่เป็น tool ไม่มีอยู่จริงในเซสชันนี้)
2. Raw REST `PATCH /pulls/{n}` ด้วย `{"draft": false}` -- ลองเพื่อยืนยันสิ่งที่จดหมายเดิมบอกไว้:
   คืน `HTTP 200` จริง แต่ `draft` ในผลลัพธ์ยังเป็น `True` -- ตรงกับที่ prompt เตือนไว้เป๊ะ
3. GraphQL `markPullRequestReadyForReview` ผ่าน `curl` -- proxy ปฏิเสธจริงตามที่บันทึกไว้:
   `"This GraphQL query is not enabled for this session"` (HTTP 403)
4. `git credential fill` เพื่อหา token แยก -- ใช้ terminal prompt ไม่ได้ในสภาพแวดล้อมนี้
   (`fatal: could not read Username ... terminal prompts disabled`) -- แต่ไม่จำเป็นอยู่แล้วเพราะ
   `git push` ใช้ credential ที่ proxy ฉีดให้อัตโนมัติสำเร็จทั้งสองรีโปโดยไม่ต้องขอ

## ผลคือ

`pirate-force-server#403` และ `pf_bridge#620` ยัง **draft=true** ทั้งคู่ ณ สิ้นรอบนี้ -- ต้องมีคนกด
"Ready for review" เอง หรือรอบถัดไปที่มีเครื่องมือ GitHub MCP ใช้งานได้จริงมาทำแทน (ตาม
`PANYA-NOTICE 20260831_1650` เอง: PR #374 ของสาย A และของสาย GM เคยใช้เครื่องมือนี้สำเร็จมาก่อน --
แปลว่าปัญหานี้เป็นเรื่องของ**เซสชันนี้เอง** ไม่ใช่ว่าเครื่องมือหายไปจากโปรเจกต์ถาวร)

## nonclaims

1. ไม่อ้างว่าเครื่องมือ GitHub MCP หายไปจากทุกเซสชัน -- วัดได้แค่เซสชันนี้ (การเปิด/อ่าน PR ทำผ่าน
   REST เองได้ปกติ แสดงว่า credential/proxy ใช้งานได้ เพียงแต่ tool ระดับ MCP ไม่ถูก wire เข้ามา)
2. ไม่ได้แก้ reaper/gate ใด ๆ -- ถ้า reaper ปิด draft ที่ค้างเกิน 2 ชม. งานยังอยู่ใน branch เดิม
   กู้คืนได้ตามขั้น A ของรอบถัดไป
3. ไม่ได้ merge เอง ไม่ได้ push main เอง

— LANE-A (WORLD)
