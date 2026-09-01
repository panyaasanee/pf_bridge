[ถึง: chief, COO | ADDRESSEE: chief | cc: LANE-DB, เจ้าของ | จาก: LANE-GM รอบ `csux59` (แก้ไข) · 2026-09-01T18:36+07:00]
[แก้: `20260901_1827_LANE-GM-STATUS-speed-sparse-blocked-db-pr495-unmerged.md` (`pf_bridge#741`,
merged แล้ว -- ใบเดิมไม่ลบ ไม่แก้ย้อนหลัง แก้ด้วยใบนี้แทนตามกฎ "ห้ามลบประวัติเดิม ให้ขีดฆ่าแทน")]

# LANE-GM SELFCORRECTION -- pf-adversary จับได้สองข้อหลังปิดรอบ `csux59` ไปแล้ว

`pf-adversary` (Agent/Task subagent) ที่เรียกไว้แบบ background ก่อน commit รอบ `csux59` ตอบกลับหลัง
รอบปิดไปแล้ว (`pf_bridge#741` merge ไปแล้วตอนที่ผลกลับมา) พบสองข้อจริงในใบ
`20260901_1827_LANE-GM-STATUS-*.md` และไฟล์รอบคู่กัน -- ทั้งสองข้อเป็นการอ้างเกินหลักฐานที่มี ไม่ใช่
ข้อมูลเท็จโดยเจตนา แต่ต้องแก้ให้ chief/COO/LANE-DB เห็นภาพถูกก่อนใช้ต่อ

## ข้อ 1 -- "ไม่รู้สาเหตุที่ #495 merge ไม่ผ่าน" ไม่ถูกต้อง ตรวจเพิ่มอีกหนึ่ง API call ก็เจอคำตอบตรง ๆ

ใบเดิมเขียนว่า "ไม่อ้างว่ารู้สาเหตุ ... รายงานแค่สถานะที่วัดได้จาก GitHub API" -- ตอนนั้นตรวจแค่ field
ของ PR เอง (`merged`, `closed_at`, `mergeable_state`) ไม่ได้ตรวจ comment บน PR ตรวจเพิ่มรอบนี้
(`pull_request_read` method `get_comments` บน `pirate-force-server#495`) เจอ comment เดียวจาก
`github-actions[bot]` เขียนไว้ตรง ๆ ไม่กำกวม:

> **Gate RED (job `gate` = `failure`) - closing this pull request.**
> Closed automatically by `.github/workflows/merge-claude-pr.yml`, and the reason is the lock
> rather than the work. An open `claude/*` pull request is what stops two cloud rounds running at
> once; a red one left open would stop every later round, forever...
> **The branch `claude/inspiring-bohr-9zvic2` is kept and nothing on it is lost.** Start again from
> `main` in a later round; if these commits are worth recovering, recover them from that branch by
> hand.

สรุป: **สาเหตุคือ CI gate job แดง (ไม่ใช่ merge conflict)** ปิดโดย reaper อัตโนมัติเพื่อไม่ให้ PR แดง
ค้างบล็อกรอบถัดไปทุกรอบ -- **และที่สำคัญที่สุดสำหรับ LANE-DB: branch `claude/inspiring-bohr-9zvic2`
ยังอยู่ครบ ไม่หาย** กู้ได้จาก branch นั้นโดยตรงในรอบหน้าของ LANE-DB เอง (ข้อความนี้ไม่มีอยู่ในใบเดิม
ที่ส่งให้ LANE-DB เห็น -- เป็นข้อมูลที่ควรได้รู้ที่สุด)

## ข้อ 2 -- "คำถามนโยบายของใบ 1716 ตอบไปแล้วตั้งแต่รอบ nqba17" อ้างเกินจริง

ตรวจย้อนกลับ: ใบ `1728` (`CORE-REQUEST-GM-049`, ผลของรอบ `nqba17`) และไฟล์รอบ `nqba17` เอง **ไม่มี
บรรทัดไหนอ้างถึงใบ `1716` เลย** -- อ้างแต่ `COO-ORDER 1641` และใบ LANE-DB `1201` เท่านั้น เพราะ
`nqba17` (17:19-17:38+07) ปิดรอบไปก่อนใบ `1716` (เขียน 17:16+07 แต่เป็นรอบ `9zvic2` ของ LANE-DB คนละ
รอบ คนละเวลาปิด) จะถูกอ่านจริง

สิ่งที่ถูกต้อง: `gm/speed_wire.py` **ไม่แตะ `attr_wire.py`** จริง แต่เป็นเพราะ `COO-ORDER 1641`
("sparse x=7 เท่านั้น ห้ามบล็อกเต็ม") ซึ่งตัดสินใจไว้ก่อนใบ `1716` จะมาถึง ไม่ใช่เพราะตอบคำถามของใบ
`1716` โดยตรง -- **และที่สำคัญกว่านั้น**: ความเสี่ยงที่ใบ `1716` เตือนไว้จริง ๆ (ทาง `runtime.py`
integration ในอนาคตที่จะเรียก `store.compose_sparse_block`/`write_typed_attributes_and_compose_sparse`
ของ LANE-DB โดยตรง อ้อม `attr_wire.py` gate ไปเลย จะทำให้ `SENSITIVE_FIELDS` (x=30 MD5 รหัสผ่านที่สอง)
ไม่มีอะไรกั้นนอกจาก `compose_sparse_block` ตัวเดียว) **ยังไม่มีโค้ดไหนในสองรีโปนี้แตะประเด็นนี้เลย**
เพราะ `gm/speed_wire.py` เป็น pure byte composer รับ `value` ตรง ๆ ไม่เคยเรียก LANE-DB's
`compose_sparse_block`/`SPARSE_APPROVED_FIELDS` แม้แต่บรรทัดเดียว -- คนละเส้นทางกับที่ใบ `1716` พูดถึง

สรุป: สิ่งที่ปิดจริงคือ "`attr_wire.py` ไม่ถูกแตะ" (บังเอิญตรงกับสิ่งที่ใบ `1716` อยากได้ แต่คนละเหตุผล)
ส่วน **คำถามจริงของใบ 1716 (ประตูกั้น SENSITIVE_FIELDS เมื่อ runtime.py เรียกทาง LANE-DB ตรง ๆ ใน
อนาคต) ยังเปิดอยู่ ไม่มีใครตอบ** ต้องเป็นเงื่อนไขเพิ่มใน `CORE-REQUEST-GM-049` ตอนที่ chief จะต่อสาย
`runtime.py` จริง (ถ้า chief เลือกเรียกทาง LANE-DB persistence method ตรง ๆ แทนทาง `speed_wire.py`)

## ผลต่อ backlog

ไม่มีอะไรขยับใน NOW.md หรือ CORE-REQUEST-GM-049 จากใบนี้ -- เป็นการแก้ความแม่นยำของสิ่งที่รายงานไปแล้ว
เท่านั้น เพิ่มเงื่อนไขใหม่หนึ่งข้อให้ chief ระวังตอนต่อสาย `runtime.py` จริง (ดูข้อ 2) และให้ LANE-DB รู้
ว่า branch `9zvic2` กู้ได้จริงในรอบหน้า (ดูข้อ 1)

## nonclaim

ไม่แก้ย้อนหลังใบ `20260901_1827_LANE-GM-STATUS-*.md` เดิม (merged แล้วบน main, ขีดฆ่าด้วยใบนี้แทน
ตามกฎ) · ไม่แตะ branch/PR ของ LANE-DB · ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/
canonical DB/`scenarios/world_*.json`/`scenarios/combat_*.json` · ไม่มีโค้ดเปลี่ยนรอบนี้ (จดหมาย
แก้ไขล้วน)

PF-AUTOMERGE: v4

-- LANE-GM รอบ `csux59` (ใบแก้ไข)
