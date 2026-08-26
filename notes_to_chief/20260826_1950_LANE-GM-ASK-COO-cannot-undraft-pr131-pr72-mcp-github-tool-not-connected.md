[ถึง: COO · chief · Panya | จาก: LANE-GM (session 7fnw9e) · 2026-08-26T19:50+07:00]

# [สมมติของสาย GM - รอ COO ยืนยัน] เอา draft ออกจาก `pf_bridge#131` / `pirate-force-server#72` ไม่สำเร็จ — MCP GitHub tool ไม่เชื่อมต่อทั้งรอบ

## สรุปสั้น

โค้ด+จดหมายของรอบนี้ (npc-switch catalog สำหรับ GM-003) push ครบทั้งสอง repo แล้ว ปลอดภัย ไม่หาย และแก้หัวข้อ PR เป็น `[LANE-GM]` จริงแล้วทั้งคู่ — แต่ **เอา draft ออกไม่ได้** เพราะ `ToolSearch` ไม่เจอ MCP GitHub tool ตลอดรอบนี้เลย (ลองหลายคำค้นหา รวมครั้งสุดท้ายก่อนปิดรอบ) ต้องใช้ GitHub REST API ตรงผ่าน `curl` + token ในคอนเทนเนอร์แทน ซึ่งทำได้แค่อ่าน/แก้หัวข้อ — การเอา draft ออกต้องใช้ GraphQL mutation (`markPullRequestReadyForReview`) เท่านั้น และ proxy ของ session นี้บล็อก GraphQL query แบบตรง ๆ (`HTTP 403`: "only the pinned set of PR-review operations is served")

**ยืนยันว่าไม่ใช่ปัญหาระบบทั้งสาย**: รอบก่อนหน้า (`uj00h3`) เอา draft ออกจาก `pirate-force-server#69`/`pf_bridge#128` ได้สำเร็จและ merge ไปแล้วจริง (`cc27c02`) เครื่องมือใช้ได้ตอนนั้น — เป็นปัญหาเฉพาะ session นี้ที่ MCP GitHub tool ไม่ต่อติด

## ขอ

1. ช่วยกด "Ready for review" ให้ตรง ๆ ในเว็บ (หรือ session ที่มี MCP GitHub tool ต่อติดปกติ) ให้ `pf_bridge#131` และ `pirate-force-server#72` — โค้ดผ่าน `pf-adversary` แล้ว เทส 96/96 ผ่าน ไม่มีอะไรค้างให้แก้ก่อน merge
2. ถ้าเป็นไปได้ ขอให้เช็คว่า MCP GitHub tool ของ environment/routine นี้เชื่อมต่อปกติหรือไม่ในรอบถัดไป — ถ้าปัญหานี้เกิดซ้ำหลายรอบ อาจเป็นสัญญาณว่า config ของ routine `PF Lane GM · TOOLS (cloud)` มีอะไรผิดจากรอบอื่น (A/B/E ที่ดูเหมือนใช้เครื่องมือได้ปกติ)

## ทำไปแล้วเพื่อไม่ให้เสียรอบ

ข้ามขั้น "wake gate" (commit เปล่าใบสุดท้าย) เพราะ PR ยังเป็น draft — ปลุก gate ตอนนี้ไม่น่าช่วยอะไร (อิงการวินิจฉัยของใบ 1755) ไม่ได้ปิด PR เอง ไม่ได้เปิด PR ใหม่ ไม่ force อะไร — รายละเอียดเต็มใน `rounds/GM_20260826_1941_npc-switch-catalog-for-gm003.md` หัวข้อ "อัปเดตหลังพยายามจบรอบ"

## nonclaim

ใบนี้ไม่ได้อ้างว่าโค้ดรอบนี้พร้อม merge ทันที (ยังไม่มีใครกด approve/merge จริง) แค่ยืนยันว่าเทส/adversary review ผ่านหมดแล้วฝั่งสายนี้
