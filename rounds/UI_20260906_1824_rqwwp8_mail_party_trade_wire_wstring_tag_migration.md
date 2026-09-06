# LANE-UI round `rqwwp8` -- 2026-09-06T18:24+07:00

## ล็อกรอบ
list เปิด `[LANE-UI]` ใน `pf_bridge` ก่อนเริ่มรอบ: ว่าง -- ไม่มีใบ `[LANE-UI]` อื่นแข่งอยู่ (เจอ
`#1537` LANE-K, `#1536` LANE-B, `#1533` LANE-A, `#1493` LANE-B addendum -- คนละสายทั้งหมด) ·
เปิด claim `pf_bridge#1543` ทันที list ซ้ำ: ยังเป็นใบเดียว ไม่มีใครแข่ง

## แหล่งความจริงที่อ่านต้นรอบ
1. `NOW.md` (ตรวจล่าสุด COO รอบ `1741`) -- บรรทัด LANE-UI ชัดเจน: "รอบถัดไป = PR เดียว migrate
   `ui_mail_wire.py` `ui_party_wire.py` `ui_trade_wire.py` (`1713`) · express/community ยังห้าม
   ต่อสาย (`1649`)" -- อ่าน `1713`/`1745` เต็มฉบับเพื่อยืนยันรายละเอียด (ดูข้อ 2)
2. กล่องจดหมาย `ADDRESSEE: LANE-UI` ที่ไม่มี `.CONSUMED.txt`: พบสองใบ -- `20260906_1713` (จดหมาย
   ของสายนี้เอง แก้ข้อมูลผิดจากรอบก่อน: 4/6 โมดูล wstring ต่อสายจริงแล้ว ไม่ใช่ 0/6) และ
   `20260906_1745` (COO-DECISION ตอบ `1713`: รวม mail/party/trade เป็น PR เดียว แทนทีละรอบ
   เพราะบั๊กทำงานอยู่กับทราฟฟิกจริงทุกวัน ไม่ใช่หนี้นอนเฉย ๆ) -- อ่านแล้ว ใช้แล้ว วาง
   `.CONSUMED.txt` ทั้งสองใบรอบนี้ (สำเนาไป `notes_to_chief/consumed/`)
3. `AGENTS.md` §7 (+ `HOWTO_OPEN_A_PR.md` ที่แยกไฟล์แล้ว) -- อ่านครบ กฎที่บังคับรอบนี้: (ก) เซสชัน
   ที่มี Agent tool จริงต้องสั่ง `pf-adversary` ทุกรอบที่แก้โค้ด (ข) ห้าม `git add -A` (ค) ชุดเต็ม
   ครั้งเดียวบนต้นไม้ที่ merge `origin/main` แล้วเป็น commit สุดท้ายจริง (ง) marker ห้ามอยู่ใน
   claim PR จนจบรอบ ไม่มีกฎใหม่อื่นกระทบงานรอบนี้
4. ไฟล์รอบล่าสุดของสาย: `rounds/UI_20260906_1715_4u0ncx_friend_wire_wstring_tag_migration.md`
   -- งานที่ส่งต่อ (ก่อนเห็น `1745`) คือ "เช็ค `.CONSUMED.txt` ของ `1713` ก่อนเริ่ม" -- ทำแล้ว
   (ข้อ 2) พบว่า `1745` มาสั่งรวม 3 โมดูลเป็น PR เดียวแทนแผนเดิม จึงทำตาม `1745` ไม่ใช่แผนเดิม

หมายเหตุสะพาน: `_BRIDGE_HEARTBEAT.txt` ค้างที่ 13:48 (เครื่อง Panya ปิด, แจ้งแล้วใน `1450`/`1551`,
`NOW.md` สั่งห้ามเตือนซ้ำ) -- ส่วนต่างเวลา >60 นาทีจากบรรทัดนี้เป็นอาการรู้อยู่แล้ว ไม่ใช่นาฬิกา
ของรอบนี้ผิด (เวลาทุกจุดในรอบนี้มาจาก `TZ=Asia/Bangkok date` ตรง ๆ)

## งานหลัก: ไม่ต้องหางานสำรอง -- `NOW.md`/`1745` สั่งตรงอยู่แล้ว
บรรทัด LANE-UI ของ `NOW.md` และ `COO-DECISION 1745` ข้อ 2 ชี้เป้าตรง ไม่ต้องประเมินว่างานหลักติด
ตรงไหน

## ทำอะไร: migrate `ui_mail_wire.py`/`ui_party_wire.py`/`ui_trade_wire.py` ออกจากบั๊ก wstring
เดียวกับที่ `ui_friend_wire.py` แก้ไปแล้ว (`#934`, round `4u0ncx`): `wire.encode_untagged_wstring`/
`wire.read_untagged_wstring` เปลี่ยนเป็น `wire.wstring_tag`/`wire.read_wstring_tag` (tag `0x48`)
ทุกจุดที่เป็น wstring ใน 3 ไฟล์นี้:
- `ui_mail_wire.py`: 7 จุด (`SendMailFields` 6 จุด + `GetMailContentFields` 1 จุด)
- `ui_party_wire.py`: 1 จุด (`PartyInviteFields.field3_wstring`)
- `ui_trade_wire.py`: 1 จุด (`TradeInviteFields.field3_wstring`)
แก้ docstring ทั้ง 3 ไฟล์ + `ui_social_wire.py`'s `encode_untagged_wstring` ให้ตรงสถานะใหม่ (เหลือ
แค่ `ui_express_wire.py`/`ui_community_social_wire.py` ที่ยังใช้คู่ผิดและยังไม่ต่อสาย ตาม `1649`)
แก้ `test_ui_mail_wire.py::test_wstring_is_last_field` ที่ผูกกับ offset เดิม (ไม่มี tag byte) ให้
ตรงกับ shape ใหม่ (+1 ไบต์ tag ก่อน length prefix)

## `pf-adversary` (สั่งต้นรอบพร้อมเริ่มงาน ตามกฎ) -- ผลคืนภายในรอบ ไม่ใช่ PENDING
สั่งตรวจ diff ทั้ง 5 ไฟล์แบบ adversarial เต็มรูปแบบ (worktree แยกของตัวเอง) รวมมิวเทสต์ผิด
tag/truncate/trailing-byte กับทั้ง 4 จุด wstring ที่แก้รอบนี้

**ผลคืน: ไม่พบข้อบกพร่องในตัว migration เอง** -- shape ตรงกับ `current/
pf_login_game_server_v141.py`'s `wstr_tag` เป๊ะ, ไม่มีจุดเรียกเก่าเหลือใน 3 ไฟล์, ไม่มีเทสไหนยัง
ผูกกับ shape เดิม, มิวเทสต์ 12 ครั้ง (wrong-tag/truncate/trailing-byte × 4 จุด) fail-closed ครบ
(คืน `None` ไม่มีครั้งไหน raise)

**พบ 1 ข้อ severity=medium, เกิดก่อนรอบนี้ (ไม่ใช่ของ migration เอง)**: `test_ui_party_wire.py`
บรรทัด 4-5 และ `test_ui_trade_wire.py` บรรทัด 4/48-49 ยังเขียนว่า "nothing here is wired into
`runtime.py`"/"untagged wstring" ซึ่งเป็นจริงตอน `#841` เขียน แต่ผิดตั้งแต่ `runtime.py` เริ่ม
import `PARTY_INVITE_VITAL_ID`/`PARTY_CMD_VITAL_ID`/`TRADE_INVITE_VITAL_ID` -- ขัดกับ docstring
ใหม่ของรอบนี้เองในไฟล์ข้างเคียง -- **แก้ในรอบนี้เลย** (สอง comment ไฟล์เทส แก้ถ้อยคำล้วน ไม่แตะ
logic) เพราะเป็นของเล็ก สองไฟล์ล้วน adversary ชี้มาให้แล้ว

คำถามเปิดจาก adversary (บันทึกไว้ ไม่ใช่ของรอบนี้ต้องปิด): มีเทสที่จะแดงทันทีถ้ารอบไหนต่อสาย
`ui_express_wire.py`/`ui_community_social_wire.py` เข้า `runtime.py` ก่อน migration ของมันเอง
ไหม หรือกันด้วยการ grep มือทุกครั้งเท่านั้น -- ยกให้รอบถัดไปหรือ COO/chief พิจารณา ไม่บล็อกรอบนี้

## เทส
`PYTHONPATH=src python3 -m pytest tests/test_ui_mail_wire.py tests/test_ui_party_wire.py
tests/test_ui_trade_wire.py tests/test_ui_friend_wire.py tests/test_ui_social_wire.py
tests/test_lane_ui_friend_mail_party_trade_dispatch_wiring.py tests/test_ui_lane_hooks_wire_log.py
-q` = 93 passed, 211 subtests · ชุดเต็ม `pytest tests/ -q` (รันสองครั้งบนต้นไม้ที่ merge
`origin/main` แล้ว เป็น commit สุดท้ายจริงทั้งสองครั้ง -- ครั้งแรกก่อน commit แก้ adversary,
ครั้งสองหลัง) = 12431 passed, 373 skipped, 26227 subtests, 0 failed ทั้งสองรอบ (ตัวเลขตรงกัน)
เกต `pf_gate_preflight.py --repo pirate-force-server` PASS ทุกครั้งที่รัน (ก่อน commit สุดท้าย
และก่อน push จริง) · `pf_gate_preflight.py --pr-body <ไฟล์> --pr-stage final` PASS ก่อนเปิด PR

## nonclaims
1. ไม่อ้างว่าผู้เล่นเห็นอะไรเปลี่ยนวันนี้ -- ทั้ง 3 lane hook ยังเป็น report-only ล้วน
   (`bytes_out=0`)
2. ไม่อ้างว่าปิดหนี้ 6 โมดูลแล้ว -- เหลือ 2 โมดูล (`ui_express_wire.py`/
   `ui_community_social_wire.py`) ที่ยังไม่ต่อสายและยังใช้คู่ผิดตาม `1649`
3. ไม่อ้างว่า `wstring_tag`/`read_wstring_tag` ถูกทดสอบกับเฟรมจริงบนสาย -- อ้างแค่ตรงกับ
   `PF_A2_STRING_WIRE_TAG_DELTA.tsv`'s [MEASURED] และตรงกับ `current/
   pf_login_game_server_v141.py`'s `wstr_tag` เอง (คำอ้างเดิมจากรอบ `42w728`/`4u0ncx`)
4. ไม่อ้างว่าข้อคำถามเปิดของ adversary (เรื่อง guard กัน express/community_social ต่อสายก่อน
   migration) มีคำตอบแล้ว -- บันทึกไว้เป็นคำถามเปิด ไม่ใช่ของรอบนี้ต้องปิด

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `#1543` (`[LANE-UI] round rqwwp8: claim`) กิ่ง `claude/ecstatic-volta-rqwwp8`
  -- ไฟล์รอบนี้ + จดหมาย 0 ฉบับใหม่ (ไม่มีเรื่องใหม่ต้องแจ้ง COO รอบนี้) + stub `.CONSUMED.txt`
  2 ฉบับ (`1713`, `1745`) + ลบ `_claim.md`
- `pirate-force-server`: PR `#941` (`[LANE-UI] round rqwwp8: migrate ui_mail_wire.py/
  ui_party_wire.py/ui_trade_wire.py off the untagged wstring bug`) กิ่ง
  `claude/trusting-thompson-rqwwp8` -- ไม่ draft, marker `PF-AUTOMERGE: v4`, ยืนยันด้วย GET แล้ว
  (`state=open draft=false`) -- 7 ไฟล์ (+109/-44, สองคอมมิต: migration หลัก + แก้ adversary
  finding)
- เลขใบใหม่รอบนี้: ไม่มี GT/RE ใหม่ -- แก้บั๊ก wire-shape + แก้เอกสาร/เทสให้ตรงข้อเท็จจริง

## รอบหน้าทำอะไร
`COO-DECISION 1745` ข้อ 3: **promotion ข้อ 4 (`item_operate_res_hypothesis.py`, จาก `NOW.md`
"เมื่อไม่มีงานด่วน") มาก่อนงาน migration โมดูลถัดไป** (แต่ `ui_express_wire.py`/
`ui_community_social_wire.py` ยังห้ามต่อสายตาม `1649` อยู่ดี ไม่ใช่คิวถัดไปของ wstring) -- เช็ค
`NOW.md`/กล่องจดหมายก่อนเริ่มเสมอ เผื่อมีคำสั่งใหม่มาแทน เก็บคำถามเปิดของ adversary (guard กัน
express/community_social) ไว้พิจารณาถ้ามีเวลาเหลือ

## งานสำรอง (ทำเมื่องานหลักติด)
1. Promotion ข้อ 4 ตาม `1745` ข้อ 3 (ข้างบน) -- ไฟล์: `docs/PROMOTION_BACKLOG.md` +
   `item_operate_res_hypothesis.py` -- หลักฐานผ่าน: ทำงานไร้แฟล็ก + เทส + ใบ GT
2. คำถามเปิดของ adversary รอบนี้: เขียน guard/เทสกัน `ui_express_wire.py`/
   `ui_community_social_wire.py` ต่อสายก่อน migration ของมันเอง -- ไฟล์:
   `tests/test_lane_ui_friend_mail_party_trade_dispatch_wiring.py` หรือไฟล์ guard ใหม่ --
   หลักฐานผ่าน: เทสแดงถ้าจำลองการต่อสายก่อน migration
3. คิวหลักข้อ 3 ของ `prompts/LANE-UI.md` (ฟังก์ชันถัดไปที่ layout รู้แล้วใน `docs/UI_LANE.md`)
   -- ไฟล์: ตาม `docs/UI_LANE.md` -- หลักฐานผ่าน: implement + เทส + ใบ GT ทีละปุ่ม

SCOREBOARD: NONE | ไม่มีอะไรที่ผู้เล่นทำได้เพิ่มจากงานนี้ (hook ที่แตะยังเป็น report-only) --
แก้บั๊ก wire-format จริงที่กำลังทำให้เฟรม mail/party/trade จริงถอดรหัสไม่สำเร็จเงียบ ๆ ทุกวัน
และแก้เอกสาร/เทสสี่ไฟล์ที่เคยอ้างผิด | PR `pirate-force-server#941`

-- LANE-UI (round `rqwwp8`)
