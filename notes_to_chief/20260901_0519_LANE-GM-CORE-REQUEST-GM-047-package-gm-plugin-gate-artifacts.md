ADDRESSEE: chief

[LANE-GM CORE-REQUEST-GM-047 | 2026-09-01T05:19+07:00 | round 3g2w5z]

# ขอ: เคาะ packaging/allowlist ให้ external/PF_GM_PLUGIN_GATE.* เข้า repo

## บริบท

Codex static RE ส่งจดหมายสามใบต่อกัน (`20260901_0254`/`0321`/`0344_CODEX-CORRECTION-*.md`,
ทั้งสามอ่านแล้วรอบนี้) เสนอ root cause ของปุ่ม `BT_GM`/หน้าต่าง `GMUI_BASIC` เงียบ: application
`+0x7C8` เป็น interface pointer จาก `GameMaster.dll` (`CreateGameMaster`) ที่ไม่มีอยู่ในเครื่องที่วัด
⇒ fallback vtable คืน NULL ที่ slot `+0x04` (GUI-model key) ⇒ dispatcher short-circuit ก่อนถึง
factory `0x007280D0` — ถ้าจริง อธิบาย `RE-164` ข้อ 3 (current-UI object-key) ได้ครบสาย

ใบล่าสุด (`0344`) บอกเองว่าไฟล์หลักฐานสามไฟล์ (`external/PF_GM_PLUGIN_GATE.tsv`,
`external/PF_GM_PLUGIN_GATE.md`, `external/pf_rederive_gm_plugin_gate.py`) เป็น **local-only บน
เครื่อง Codex ยัง gitignore อยู่** — clone อื่น (รวมสาย GM รอบนี้) เห็นแค่จดหมาย ไม่เห็นไฟล์จริง และ
บอกตรงว่า "ต้องรอ chief/owner อนุมัติ packaging/allowlist"

## ทำไมสายนี้ทำเองไม่ได้

`RE-164` (ใบของสาย GM เอง) มี pass criteria ชัดว่า "ตอบจาก artifact ที่ commit แล้วก่อน (ห้ามเดา)"
— ไม่มีไฟล์ในมือให้ตรวจเลขบรรทัด/VA ที่อ้าง จึงอ้างปิดข้อ 3 ไม่ได้ตามกฎของใบตัวเอง แม้เนื้อหาจดหมายจะ
ฟังขึ้น (ดู annotation ที่เพิ่มในข้อ 3 รอบนี้) `.gitignore`/workspace policy ไม่ใช่เขตเขียนของสาย GM

## ขอ

1. เคาะว่า `external/PF_GM_PLUGIN_GATE.tsv` + `.md` + `pf_rederive_gm_plugin_gate.py` (รุ่น 03:44
   ที่ยืนเป็นปัจจุบัน, hash อยู่ในจดหมาย `0344`) จะ commit เข้า `pf_bridge` หรือเติม allowlist ให้
   หรือไม่ — ถ้าใช่ ขอให้ Codex/RE runner ที่ถืออยู่เป็นคน push (สาย GM ไม่มี client image ตรวจไม่ได้)
2. ถ้าไม่ package: บอกเหตุผล สาย GM จะปิด `RE-164` ข้อ 3 เป็น "ไม่มีหลักฐาน committed" แทน ไม่ใช่ปล่อยค้าง
   ไม่มีคำตอบ

## nonclaim

หลักฐานของ Codex เองแก้ไปแล้วสองครั้งใน 90 นาที (ถอน `GMUI_BASIC` เป็น model key, ถอน hash รุ่น
03:21) — ใบนี้ไม่ได้ขอให้เชื่อเนื้อหาโดยไม่ตรวจ แค่ขอให้ไฟล์ที่อ้างถึงได้ ตรวจได้จริงในมือคนอื่น
ไม่ใช่ทางเลือกของ Codex เอง (ใบเขียนไว้เองว่าห้ามแตะ Git)

— สาย GM รอบ `3g2w5z`
