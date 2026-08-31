# LANE-GM round `bmedw1` -- 2026-09-01T01:22+07:00

## เช็คทั้งสี่ช่องตามลำดับที่กำหนด

1. **จดหมาย ADDRESSEE: LANE-GM ที่ยังไม่มี `.CONSUMED.txt`**: พบหนึ่งใบ --
   `notes_to_chief/20260901_0043_COO-DECISION-attr-wire-unlock-criteria-replaced-shelve-
   stays-locked.md`. บริโภคแล้ว (รายละเอียดด้านล่าง).
2. **CORE-REQUEST / คำตอบของ chief ที่อ้างหมายเลข GM-0xx**: grep แล้ว ไม่พบใบใหม่ที่ยังไม่บริโภค
   นอกจากใบข้อ 1.
3. **ใบ GT ในคิว (อ่านอย่างเดียว)**: ไม่มีหัวใบ GT ใหม่ที่ระบุว่าเป็นของสาย GM รอบนี้ `GT-172`
   (READY จากรอบก่อน) ยังเป็นสถานะเดิม ไม่มีอะไรให้แก้.
4. **`rounds/GM_*.md` backlog ของตัวเอง**: รอบก่อน (`dgyakk`) บันทึกว่าบล็อกอยู่ที่ (ก) RE-164
   #1/#3 รอ RE runner (ของ chief) (ข) `attr_wire.py` shelved รอคำตอบเจ้าของ (ใบ `2327`).
   ทั้งสองยังไม่เปลี่ยนสถานะรอบนี้.

## งานที่ทำ

`COO-DECISION 0043` (ADDRESSEE: LANE-GM) แจ้งว่าเงื่อนไขปลดล็อก attr-wire แก้เป็น 3 ข้อใหม่:
(ก) encoder ครอบทุกฟิลด์ที่มีชื่อแล้ว (ข) ฟิลด์ไม่รู้จักต้อง lossless preserve ไม่ใช่ zero
(ค) ต้องมี version-confirmation constant แบบเดียวกับ `warp`/`say`.

ร่างแรกของ docstring เขียนว่าใบนี้ "confirmed this module already satisfies all three" --
**pf-adversary จับได้ว่าเกินจริงและขัดกันเองในย่อหน้าเดียวกัน**: ใบ `0043` ไม่ได้ตรวจโค้ดโมดูลนี้
เลย (ไม่มีคำว่า `attr_wire.py`/`FIELDS`/`RawBlockCache` ในใบ) และข้อ (ข) จริง ๆ ยังไม่เป็นจริง
ระดับผลลัพธ์ -- docstring ส่วน "The open part" ของไฟล์เดียวกันบอกเองว่าการส่ง named-field ครั้งแรก
จะทำให้ฟิลด์ unnamed ที่ไม่ใช่ศูนย์อยู่ตอนนี้กลายเป็นศูนย์ เพราะยังไม่มี raw-block source ให้ preserve
จากอะไรเลย นั่นคือเหตุผลที่ทาง 1 vs ทาง 2 ยังเป็นคำถามเปิด -- ถ้า (ข) เป็นจริงแล้ว คำถามนี้ก็ไม่ต้อง
มีอยู่ แก้ตามที่ pf-adversary ชี้: (ก)/(ค) จริงระดับโค้ด (`FIELDS` ครอบทุกแถวมีชื่อ,
`UPDATE_ATTR_VITAL_VERSION_CONFIRMED: int | None = None` เป็น gate แบบเดียวกับ
`teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED`/`say_wire.GM_GLOBAL_MESSAGE_VITAL_VERSION_
CONFIRMED`) แต่ (ข) ยังไม่จริงจนกว่าทาง 1/ทาง 2 จะถูกตอบ ระบุไว้ตรง ๆ ในย่อหน้าที่แก้แล้ว
ไม่อ้างว่าใบ `0043` ตรวจ/ยืนยันโมดูลนี้

แก้เฉพาะ docstring หัวไฟล์ `gm/attr_wire.py` (บรรทัด ~28-32 เดิม) เพิ่มพารากราฟอ้างอิง
`COO-DECISION 0043` แบบที่แก้แล้ว (ตรงกับสิ่งที่ตรวจได้จริง ไม่เกินขอบเขตของใบเอง) และย้ำจุดที่ยัง
รอเจ้าของ ไม่แก้ logic/ไม่แก้ gate/ไม่แก้เทส

รัน `python3 -m pytest tests/test_gm_*.py -q` ยืนยัน 1164 passed, 537 subtests (ไม่มี
regression -- คาดไว้แล้วเพราะเป็น docstring เท่านั้น)

ส่งผ่าน pf-adversary ก่อน commit (agent เดียวกับที่โปรเจกต์ใช้ทุกรอบที่ไม่ใช่แก้คำผิด) -- จับ
ประเด็นเกินจริงข้างบนได้ แก้แล้วก่อน commit จริง

## หลักฐานสองชั้น

client-observable: ไม่มีในรอบนี้ (ไม่มีการเปลี่ยนพฤติกรรมที่ผู้เทสสัมผัสได้)
wire/DB: ไม่มีการเปลี่ยน -- `UPDATE_ATTR_VITAL_VERSION_CONFIRMED` ยัง `None` เหมือนก่อนรอบนี้

## nonclaim

1. ไม่อ้างว่า attr-wire ปลดล็อกแล้ว หรือ `/lv` ส่งได้จริง -- ยัง shelved
2. ไม่อ้างว่าทาง 1 หรือทาง 2 ถูกเลือกแล้ว -- ยังเป็นคำถามเปิดถึงเจ้าของ
3. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/
   `gm_accounts.json`/`scenarios/world_*.json`/`scenarios/combat_*.json`
4. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone ใด ๆ รอบนี้
5. ไม่ลบประวัติ/จดหมายเดิม -- สตับที่เพิ่มเป็นไฟล์ใหม่ ต้นฉบับยังอยู่ครบ

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** -- รอบนี้เป็นการบริโภคจดหมาย + แก้ docstring เท่านั้น `GT-172` (READY จากรอบก่อน)
ยังเป็นทางเดียวที่ผู้เทส attended ทำได้เพิ่มจากเมื่อวาน

PR: `pf_bridge#649`, `pirate-force-server#426`
