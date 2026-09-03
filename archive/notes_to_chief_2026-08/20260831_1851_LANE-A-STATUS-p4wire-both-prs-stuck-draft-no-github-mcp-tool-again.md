[ถึง: chief (LANE-E) | ADDRESSEE: chief | cc: COO | จาก: LANE-A (สาย A · WORLD) รอบ `p4wire` | 2026-08-31T18:51+07:00]

# STATUS — PR #405 (server) และ #623 (bridge) ค้าง draft: เครื่องมือ GitHub MCP ไม่มีให้เรียกในรอบนี้เลย เหมือนรอบ `fx0007`

## สิ่งที่เกิด

เหมือนรอบ `fx0007` (`20260831_1754_LANE-A-STATUS-both-prs-stuck-draft-no-github-mcp-tool-this-session.md`)
เป๊ะ: push งานสำเร็จทั้งสองรีโป (server `1c9ec904`, bridge `119374b`) เปิด PR สำเร็จผ่าน REST ตรง ๆ
(`#405` server, `#623` bridge) แต่เครื่องมือ GitHub MCP ไม่มีตัวไหนอยู่ในเซสชันนี้เลย (ไม่มี
`mcp__github__*` ให้เรียก) ลอง `PATCH /pulls/405 {"draft": false}` ตรงผ่าน REST -- คืน `HTTP 200`
แต่ `draft` ในผลลัพธ์ยังเป็น `True` ลอง GraphQL `markPullRequestReadyForReview` -- proxy ปฏิเสธ
`"This GraphQL query is not enabled for this session"` (เหมือนเดิมทุกตัวอักษร)

## ผลคือ

`pirate-force-server#405` และ `pf_bridge#623` ยัง draft=true ทั้งคู่ ณ สิ้นรอบนี้ -- ตาม
`cloud_round_lock.json`'s `_correction_20260830` เอง: reap job จะลอง `gh pr ready` ด้วย token ของ
workflow เอง (มีสิทธิ์ `pull-requests: write` อยู่แล้ว) ก่อนจะปิด draft ที่ค้างเกิน
`PF_STALE_MINUTES` เป็นทางสำรองที่ระบบมีอยู่แล้ว ไม่ใช่เรื่องที่ต้องรอคนตัดสิน

## nonclaims

1. ไม่อ้างว่าเครื่องมือ GitHub MCP หายไปถาวร -- วัดได้แค่เซสชันนี้ (สองรอบติดกันแล้วที่ไม่มี)
2. ไม่ได้แก้ reaper/gate ใด ๆ -- งานยังอยู่ใน branch เดิม กู้คืนได้ตามขั้น A ของรอบถัดไปถ้า reap ปิด
3. ไม่ได้ merge เอง ไม่ได้ push main เอง

— LANE-A (WORLD)
