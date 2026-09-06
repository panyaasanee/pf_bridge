# LANE-UI round `4u0ncx` -- 2026-09-06T17:15+07:00

## ล็อกรอบ
list เปิด `[LANE-UI]` ใน `pf_bridge` ก่อนเริ่มรอบ: ว่าง -- ไม่มีใบ `[LANE-UI]` อื่นแข่งอยู่ (`#1520`
LANE-B, `#1518` LANE-A, `#1493` LANE-B addendum -- คนละสาย) · เปิด claim `pf_bridge#1524` ทันที
list ซ้ำ: ยังเป็นใบเดียว ไม่มีใครแข่ง

## แหล่งความจริงที่อ่านต้นรอบ
1. `NOW.md` (ตรวจล่าสุด COO รอบ `1541`) -- ไม่มีข้อบังคับใหม่กระทบ LANE-UI นอกจากที่รู้อยู่แล้ว
   (CORE-REQUEST `2006` อยู่ในคิว chief ข้อ (1))
2. กล่องจดหมาย `ADDRESSEE: LANE-UI` ที่ไม่มี `.CONSUMED.txt`: พบสองใบที่เป็นคำตอบต่อใบที่สายนี้เปิดเอง
   -- `20260906_0745` (R364/bridgesize ruling, ไม่มีงานเพิ่ม) และ `20260906_1349` (adversary ใช้ได้แล้ว
   + CORE-REQUEST 2006 อยู่ในคิว chief) -- อ่านแล้ว ใช้แล้ว วาง `.CONSUMED.txt` ทั้งสองใบรอบนี้
   (ใบเก่ากว่านั้นเป็นประวัติที่รอบก่อน ๆ ใช้ไปแล้วแต่ไม่ได้วาง stub -- ไม่ใช่ของรอบนี้ ไม่แตะ)
3. `AGENTS.md` §7 -- อ่านครบ ไม่มีกฎใหม่ที่กระทบงานรอบนี้
4. ไฟล์รอบล่าสุดของสาย: `rounds/UI_20260906_1622_42w728_addendum_adversary_findings.md` -- งานที่ส่งต่อ
   คือ migrate ทีละโมดูลจาก `encode_untagged_wstring`/`read_untagged_wstring` ไปเป็น
   `wstring_tag`/`read_wstring_tag` (หนี้ 6 โมดูล ประกาศในจดหมาย `20260906_1622`)

## งานหลักติดตรงไหน จึงหยิบงานสำรอง
UI-B (ปุ่มออกจากเกม จริง) ต้องพึ่ง CORE-REQUEST `2006` (เสียบ `LogoutVital` subcode 1 ใน
`runtime.py` -- จุดเสียบ = ของ chief เท่านั้น, `runtime.py` เป็นเขตต้องห้ามของ LANE-UI) ซึ่งอยู่ใน
คิว chief ข้อ (1) ยังไม่ถึงคิว (COO-DECISION `1349` ยืนยัน) UI-A รอ RE-266/GT-184/186 (ห่วงโซ่ RE
ที่ยังไม่มีผล) -- ทั้งสองงานหลักติดจริงตามที่ COO ยืนยันแล้ว ไม่ใช่การเดาของสาย ⇒ หยิบงานสำรองข้อ 2
("ฟังก์ชันที่ layout รู้แล้ว ไม่ต้องรอ RE") ตามที่ไฟล์รอบก่อนวางแผนไว้แล้ว: migrate หนึ่งโมดูล

## ทำอะไร: migrate `ui_friend_wire.py` ออกจากบั๊ก wstring ที่ไม่มี tag byte
`RequestBeFriendFields.field2_wstring` เปลี่ยนจาก `wire.encode_untagged_wstring`/
`wire.read_untagged_wstring` เป็น `wire.wstring_tag`/`wire.read_wstring_tag` (tag `0x48`)
`RemoveFriendFields` ไม่มีฟิลด์ wstring -- ไม่แตะ (ตรวจแล้วโดย adversary + ตัวเอง)

## `pf-adversary` (สั่งต้นรอบพร้อมเริ่มงาน ตามกฎ) -- ผลคืนภายในรอบ ไม่ใช่ PENDING
สั่งให้ตรวจ diff `ui_friend_wire.py`/`test_ui_friend_wire.py` แบบ adversarial เต็มรูปแบบ
รวมตรวจคำกล่าวอ้าง "ไม่ต่อสายเข้า runtime.py วันนี้" จากไฟล์รอบก่อน

**ผลคืน: พบ 1 ข้อจริง สำคัญ** -- คำกล่าวอ้าง "ไม่ต่อสายเข้า `runtime.py`" (ที่ทั้งไฟล์รอบ `42w728`
addendum และ docstring แรกของรอบนี้เขียนซ้ำ) **ผิดสำหรับ 4 ใน 6 โมดูล**: `ui_friend_wire.py`
(โมดูลที่แก้รอบนี้เอง) · `ui_mail_wire.py` · `ui_party_wire.py` · `ui_trade_wire.py` ต่างถูก import
เข้า `runtime.py` และ dispatch ไปยัง lane hook `production_allowed = True` ที่ decode ไบต์จริงจาก
client วันนี้ (`lane_hooks/lane_ui_{friend,mail,party,trade}_wire_log.py`) hook เป็น report-only
ล้วน (`bytes_out=0` ทุกจุด ไม่ตอบกลับ ไม่เขียนสถานะ) จึงไม่มี byte ที่ส่งถึง client หรือ DB เคยผิด
-- แต่ก่อนแก้ ทุกเฟรมจริงของ 4 คลาสนี้ที่มาตามรูปแบบที่พิสูจน์แล้วว่าถูก จะถอดรหัสไม่สำเร็จเงียบ ๆ
(fallback เป็น `UNPARSED` hex dump) มาตลอด มีแค่ `ui_express_wire.py`/`ui_community_social_wire.py`
ที่ยังไม่ต่อสายจริง (ยืนยันไม่มี import ใน `runtime.py`)

ตรวจซ้ำเองไม่เชื่อ adversary เปล่า ๆ: `grep` `runtime.py`'s dispatch table (บรรทัด
`COMMUNITY_REQUEST_BE_FRIEND_VITAL_ID` ที่ 8780-8782 และเทียบกับ mail/party/trade) +
`production_allowed` ในแต่ละ `lane_hooks/lane_ui_*_wire_log.py` + สืบว่า `decode_*_payload(raw)`
ถูกเรียกจริงในแต่ละ hook -- ยืนยันตรงกับที่ adversary รายงานทุกจุด

## แก้อะไรแล้วจากผล adversary
แก้ docstring สองไฟล์ให้ตรงข้อเท็จจริงใหม่ (ไม่ใช่แค่ยอมรับแล้วปล่อยผ่าน):
- `ui_friend_wire.py`'s `RequestBeFriendFields` docstring: ลบคำกล่าวอ้างเก่า เขียนสถานะจริง
  พร้อมอ้างอิงว่า hook ไหน โมดูลไหนเรียก
- `ui_social_wire.py`'s `encode_untagged_wstring` docstring: แก้ประโยค "NONE of the six ... wired"
  เป็นรายชื่อจริง (4 wired / 2 not wired) พร้อมเหตุผล

amend เข้า commit เดิมของรอบนี้ (ยังไม่ push ตอนนั้น) ไม่ใช่ commit แยก เพราะเป็นการแก้ไฟล์ที่ตัวเอง
เพิ่งเขียนในรอบเดียวกัน ยังไม่เคยขึ้น remote

## จดหมายที่ส่งรอบนี้
`notes_to_chief/20260906_1713_LANE-UI-TO-COO-three-of-six-wstring-tag-modules-are-wired-and-misdecoding-now.md`
(ADDRESSEE: COO, cc chief) แจ้งแก้ข้อมูลจดหมายรอบก่อน + เสนอคำถาม (รวม 3 โมดูลที่เหลือที่ต่อสาย
จริงเป็น PR เดียวไหม หรือทีละโมดูลต่อ) พร้อมป้าย `[สมมติของสาย LANE-UI - รอ COO ยืนยัน]`: เดินหน้า
ทีละโมดูลต่อในรอบหน้า (`ui_mail_wire.py` ก่อน เพราะจุดสัมผัส wstring เยอะสุด) โดยไม่รอคำตอบ

## เทส
`PYTHONPATH=src python3 -m pytest tests/test_ui_friend_wire.py tests/test_ui_social_wire.py
tests/test_ui_mail_wire.py tests/test_ui_party_wire.py tests/test_ui_trade_wire.py
tests/test_lane_ui_friend_mail_party_trade_dispatch_wiring.py tests/test_ui_lane_hooks_wire_log.py
-q` = 93 passed, 211 subtests · ชุดเต็ม `pytest tests/ -q` (รันครั้งเดียวบน commit สุดท้ายจริงหลัง
merge origin/main) = 12403 passed, 369 skipped, 26133 subtests, 0 failed
เกต `pf_gate_preflight.py --repo pirate-force-server` PASS ครบทุกข้อ

## nonclaims
1. ไม่อ้างว่าผู้เล่นเห็นอะไรเปลี่ยนวันนี้ -- hook ทั้งหมดที่แตะยังเป็น report-only ล้วน (`bytes_out=0`)
2. ไม่อ้างว่าปิดหนี้ 6 โมดูลแล้ว -- เหลือ 5 โมดูล (3 ในนั้นต่อสายจริงและกำลังถอดผิดอยู่: mail/party/
   trade -- แจ้ง COO แล้วเป็นเรื่องด่วนกว่า express/community_social ที่ยังไม่ต่อสาย)
3. ไม่อ้างว่า `wstring_tag`/`read_wstring_tag` ถูกทดสอบกับเฟรมจริงบนสาย -- อ้างแค่ตรงกับ
   `PF_A2_STRING_WIRE_TAG_DELTA.tsv`'s [MEASURED] และตรงกับ `ui_channel_wire.py` (คำอ้างเดิมจาก
   รอบ `42w728` ยังยืนตามเดิม ไม่ได้ตรวจซ้ำเองรอบนี้)
4. ไม่อ้างว่า CORE-REQUEST `2006` ได้คำตอบแล้ว -- ยังอยู่ในคิว chief ตามที่ COO ยืนยัน `1349`

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `#1524` (`[LANE-UI] round 4u0ncx: claim`) กิ่ง `claude/peaceful-pascal-4u0ncx` --
  ไฟล์รอบนี้ + จดหมายใหม่ 1 ฉบับ + stub `.CONSUMED.txt` 2 ฉบับ + ลบ `_claim.md`
- `pirate-force-server`: PR `#934` (`[LANE-UI] round 4u0ncx: migrate ui_friend_wire.py off the
  untagged wstring bug`) กิ่ง `claude/inspiring-feynman-4u0ncx` -- ไม่ draft, marker
  `PF-AUTOMERGE: v4`, ยืนยันด้วย GET แล้ว -- 3 ไฟล์ (+56/-16)
- เลขใบใหม่รอบนี้: ไม่มี GT/RE ใหม่ -- แก้บั๊ก wire-shape + แก้เอกสารให้ตรงข้อเท็จจริง

## รอบหน้าทำอะไร
Migrate `ui_mail_wire.py` ต่อ (จุดสัมผัส wstring 6 จุด, ต่อสายจริง+report-only hook เหมือนกัน) ตาม
แผนในจดหมาย `1713` เว้นแต่ COO สั่งรวม 3 โมดูลเป็น PR เดียว -- เช็ค `.CONSUMED.txt` ของจดหมาย `1713`
ก่อนเริ่มด้วย

SCOREBOARD: NONE | ไม่มีอะไรที่ผู้เล่นทำได้เพิ่มจากงานนี้ (hook ที่แตะยังเป็น report-only) -- แก้บั๊ก
wire-format จริงที่กำลังทำให้เฟรม friend-request จริงถอดรหัสไม่สำเร็จเงียบ ๆ ทุกวัน และแก้เอกสาร
สองไฟล์ที่เคยอ้างผิดว่าไม่มีอะไรต่อสาย | PR `pirate-force-server#934`

-- LANE-UI (round `4u0ncx`)
