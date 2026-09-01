[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ | จาก: LANE-B (COMBAT) รอบ `jqxe6v`
(scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-08-31T21:05+07:00]

# ADDENDUM -- PR ทั้งสองใบค้าง draft (ไม่มี MCP tool ให้ undraft รอบนี้ เหมือนรอบ `256rvs`)

Function list ของเซสชันนี้มีแค่ Read/Grep/Glob/Bash/Edit/Write ไม่มี `mcp__github__*` tool ใด ๆ
ให้เรียก (ตรวจ `env` เจอ `CLAUDE_CODE_DISABLE_BUILTIN_ANTMCP=1` ตั้งไว้ในเซสชันนี้ -- ยืนยันว่า
ไม่ใช่แค่ "ไม่ถูกส่งมาให้" แต่ปิดไว้ตรง ๆ) ตามคำสั่งงาน **ไม่ลอง** raw REST
`PATCH {"draft": false}` (คำสั่งงานเตือนไว้ว่าคืน 200 แต่ไม่เปลี่ยนค่าจริง) และ**ไม่ลอง**
GraphQL `markPullRequestReadyForReview` (proxy ปฏิเสธเสมอตามที่บันทึกไว้สามคืนก่อน)

ทำตามลำดับที่ถูกต้องแล้ว: push ครบ (ข้อ 1) -> แก้หัวข้อ+body ให้มี `PF-AUTOMERGE: v4` และ GET
ยืนยันว่า marker อยู่จริงทั้งสองใบ (ข้อ 2, ทำก่อนข้อ 3 เสมอ) -> พยายามปลด draft (ข้อ 3) แต่ไม่มี
เครื่องมือให้ทำจริง

**PR ที่ค้าง draft ณ ตอนจบรอบ**:
- `pirate-force-server#412` -- title/body อัปเดตแล้ว, `PF-AUTOMERGE: v4` ยืนยันด้วย GET
- `pf_bridge#630` -- title/body อัปเดตแล้ว, `PF-AUTOMERGE: v4` ยืนยันด้วย GET

หลักฐานจากรอบก่อน (`pirate-force-server#407`/`pf_bridge#625`, ทั้งคู่ merged แล้ว): timeline
แสดงว่า `ready_for_review` ถูกยิงโดย `github-actions[bot]` เอง ไม่ใช่สาย B แล้ว merge ตามทันที --
คาดว่า `merge-claude-pr.yml` จะทำแบบเดียวกันกับสองใบนี้เองเมื่อ CI เขียว + marker ครบ (มีแล้ว)
ไม่ต้องมีคนกดเอง ถ้าไม่ขยับภายใน 2 ชม. (pf_bridge) / 6 ชม. (server) ควรมีคนเข้าไปดู

-- LANE-B (COMBAT) รอบ `jqxe6v`
