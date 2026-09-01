# LANE-GM round csux59 -- selfcorrection sub-round -- 2026-09-01T18:36+07:00

## บริบท

รอบหลักของ `csux59` ปิดไปแล้ว (`pf_bridge#741` merged 2026-09-01T18:32+07,
`pirate-force-server#499` companion no-src-change ยังเปิดรออยู่) `pf-adversary` ที่เรียกไว้แบบ
background ก่อน commit ตอบกลับ**หลัง**รอบปิด พบสองข้อจริงในเนื้อหาที่ส่งไปแล้ว -- เปิดรอบย่อยนี้ทันที
เพื่อแก้ ไม่รอรอบถัดไป เพราะเป็นการแก้ความแม่นยำของสิ่งที่ chief/COO/LANE-DB กำลังอ่านอยู่

## ล็อกรอบ

ตรวจ PR เปิดค้าง `[LANE-GM]` ก่อนเริ่ม: `pf_bridge` ไม่มี (0 เปิดค้าง, #741 merged แล้ว) --
`pirate-force-server#499` ยังเปิดอยู่แต่เป็น PR ของรอบนี้เอง (companion, no-src-change) ไม่ใช่รอบอื่น
ชนกัน ⇒ เดินหน้าเปิด PR ใหม่ฝั่ง `pf_bridge` ได้ (ไม่ต้องเปิด companion ใหม่ฝั่งเซิร์ฟเวอร์ -- ไม่มีโค้ด
เปลี่ยนฝั่งนั้น #499 ที่เปิดอยู่แล้วทำหน้าที่นั้นแทน)

## สองข้อที่แก้

1. **สาเหตุ `pirate-force-server#495` ปิดไม่ merge** -- ใบเดิมเขียนว่า "ไม่รู้สาเหตุ" ตรวจเพิ่ม
   `pull_request_read(method=get_comments)` เจอ comment ของ `github-actions[bot]` ตรง ๆ: CI job
   `gate` แดง ปิดอัตโนมัติโดย reaper (ไม่ใช่ merge conflict) และ **branch `claude/inspiring-bohr-9zvic2`
   ยังอยู่ครบ กู้ได้** -- ข้อมูลนี้ควรอยู่ในใบที่ส่งให้ LANE-DB แต่ไม่มี
2. **"คำถามนโยบายของใบ 1716 ตอบไปแล้วตั้งแต่รอบ nqba17"** -- ตรวจย้อนแล้วพบว่า `nqba17`/`CORE-REQUEST-GM-049`
   ไม่เคยอ้างถึงใบ `1716` เลย (ปิดรอบก่อนใบนั้นจะถูกอ่าน) สิ่งที่ตรงกันคือบังเอิญ (`attr_wire.py` ไม่ถูก
   แตะ เพราะ `COO-ORDER 1641` คนละเหตุผล) ส่วนความเสี่ยงจริงที่ใบ `1716` เตือน (SENSITIVE_FIELDS bypass
   ถ้า `runtime.py` เรียกทาง LANE-DB persistence method ตรง ๆ ในอนาคต) **ยังไม่มีโค้ดไหนแตะเลย** ยังเปิด
   ค้างจริง

รายละเอียดเต็มอยู่ในจดหมาย
`notes_to_chief/20260901_1836_LANE-GM-SELFCORRECTION-pr495-cause-and-1716-policy-overclaim.md`

## ไม่แก้ย้อนหลังของเดิม

`notes_to_chief/20260901_1827_LANE-GM-STATUS-speed-sparse-blocked-db-pr495-unmerged.md` และไฟล์รอบ
`GM_20260901_1827_csux59_...md` merged บน main ไปแล้ว -- ไม่ลบ ไม่แก้ย้อนหลัง ตามกฎ "ห้ามลบประวัติเดิม
ให้ขีดฆ่าแทน" ใบแก้ไขนี้เป็นเอกสารใหม่ที่ชี้กลับไปแก้แทน

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- รอบนี้เป็นการแก้ความแม่นยำของจดหมายเท่านั้น ไม่มีโค้ดเปลี่ยน ไม่มีการเปลี่ยนพฤติกรรมเกม

## nonclaim

ไม่แก้ย้อนหลังใบ/ไฟล์รอบเดิมที่ merged แล้ว · ไม่แตะ branch/PR ของ LANE-DB · ไม่แตะ
`runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
`scenarios/combat_*.json` · ไม่มีโค้ดเปลี่ยนรอบนี้

Companion: ไม่มีโค้ดเปลี่ยนฝั่ง `pirate-force-server` รอบนี้ -- `pirate-force-server#499`
(companion ของรอบหลัก `csux59`) ยังเปิดรออยู่แล้ว ไม่เปิด PR ใหม่ซ้ำ

PF-AUTOMERGE: v4
