# LANE-UI round `u3pzcz` -- 2026-09-06T19:54+07:00

## ล็อกรอบ
list เปิด `[LANE-UI]` ใน `pf_bridge` ก่อนเริ่มรอบ: ว่าง -- เจอ `#1550` LANE-B, `#1546` LANE-GM,
`#1493` LANE-B addendum, คนละสายทั้งหมด · เปิด claim `pf_bridge#1554` ทันที list ซ้ำ: ยังเป็นใบเดียว
ไม่มีใครแข่ง

## แหล่งความจริงที่อ่านต้นรอบ
1. `NOW.md` (ตรวจล่าสุด COO รอบ `1841`, 18:46+07:00) -- บรรทัด LANE-UI: "รอบถัดไป = PR เดียว migrate
   `ui_mail_wire.py`/`ui_party_wire.py`/`ui_trade_wire.py` (`1713`) · express/community ยังห้ามต่อสาย
   (`1649`)" -- **ตรวจด้วย `git merge-base --is-ancestor` แล้วพบว่างานนี้อยู่บน main แล้วจริง**:
   `c54231f` (round `rqwwp8`, PR `pirate-force-server#941`) เป็น ancestor ของ `origin/main` HEAD
   (`6f4fb3b` ตอนเริ่มรอบ) -- NOW.md ยังไม่ได้อัปเดตให้ตรงสถานะนี้ (เขียนหลังรอบ `rqwwp8` merge แล้ว
   แต่ COO อาจยังไม่เห็น) จึงอ่านไฟล์รอบล่าสุดของสายต่อ (ข้อ 4) เพื่อยืนยันว่างานนี้ปิดแล้วจริง
2. กล่องจดหมาย `ADDRESSEE: LANE-UI`/`ADDRESSEE: UI` ที่ไม่มี `.CONSUMED.txt`: **ว่าง** -- ไล่ทุกใบใน
   `notes_to_chief/*.md` (ข้าม `consumed/`) เทียบกับ `.CONSUMED.txt` คู่ ไม่พบใบค้าง รวมถึง
   `20260906_1745_COO-DECISION-ui1713-...` ที่ round `rqwwp8` บริโภคไปแล้ว (มี `.CONSUMED.txt` +
   สำเนาใน `consumed/`)
3. `AGENTS.md` §7 (+ `HOWTO_OPEN_A_PR.md`) -- อ่านครบ กฎที่บังคับรอบนี้: (ก) เซสชันที่มี Agent tool
   จริงต้องสั่ง `pf-adversary` ทุกรอบที่แก้โค้ด (ข) ห้าม `git add -A` (ค) ชุดเต็มครั้งเดียวบนต้นไม้ที่
   merge `origin/main` แล้วเป็น commit สุดท้ายจริง (ง) marker ห้ามอยู่ใน claim PR จนจบรอบ (จ) PR ที่ไม่
   แตะเส้นบูต/ล็อกอิน/ตัวตน actor/เฟรมที่ส่งไคลเอนต์ เปิดตรงได้ไม่ต้อง draft · ไม่มีกฎใหม่อื่นกระทบ
   งานรอบนี้
4. ไฟล์รอบล่าสุดของสาย: `rounds/UI_20260906_1824_rqwwp8_mail_party_trade_wire_wstring_tag_
   migration.md` -- ยืนยันข้อ 1: PR `#941` merge แล้วจริง (ไฟล์รอบนั้นเขียน SHA/สถานะไว้ครบ) และ
   "รอบหน้าทำอะไร" ชี้ตรงมาที่ `COO-DECISION 1745` ข้อ 3: promotion ข้อ 4
   (`item_operate_res_hypothesis.py`) มาก่อนงาน migration โมดูลถัดไป (ซึ่งยังไงก็ห้ามต่อสายอยู่ดีตาม
   `1649`) -- และ "งานสำรอง" ข้อ 2 ของไฟล์เดียวกันเก็บคำถามเปิดของ pf-adversary ไว้: มีการ์ดกัน
   `ui_express_wire.py`/`ui_community_social_wire.py` ต่อสายก่อน migration ของมันเองไหม -- **ไม่มี**

## งานหลัก: promotion ข้อ 4 -- ตรวจแล้วติด ไม่ใช่แค่ "ยังไม่ลอง"
อ่าน `docs/PROMOTION_BACKLOG.md` แถว `item_operate_res_hypothesis.py` + ทั้งไฟล์
`src/pirateforce_foundation/item_operate_res_hypothesis.py` (module docstring + โค้ดเต็ม) +
`GAME_TEST_QUEUE.md`/`archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md` grep `GT-063` (พบผลปิด
PASS เต็มที่ archive บรรทัด 3298) + ไล่ `runtime.py` ทุกจุดที่เขียนกระเป๋าจริง
(`_dispatch_v111_persistent_merge`, `_dispatch_item_move_hypothesis`,
`_dispatch_item_move_generalized`)

พบว่าการ "ปลดแฟล็ก" ตรงไปตรงมาไม่ใช่ทางเลือกที่ปลอดภัย/มีความหมาย: trigger เป็นสตริงแชต ASCII 12 ตัว
เป๊ะ (ไม่ใช่การกระทำเก็บของจริง) ผูกกับ identity guard เฉพาะตัวละครทดสอบเดียว -- ปลดแฟล็กตรง ๆ
(คง identity guard) จะ inert กับผู้เล่นจริงทุกคน ถ้าถอด identity guard ด้วยจะเปิดช่องโหว่ item-dupe
(พิมพ์สตริงคงที่ในแชตซ้ำได้ไม่จำกัด ขัด §7 บรรทัดแรกเรื่อง multiplayer ตรง ๆ) และยังไม่มี event ทั่วไป
"ผู้เล่นได้ไอเทมจริง" ให้เกาะแทน chat trigger (ระบบกระเป๋าทั่วไปเป็นของ LANE-DB ซึ่ง STUCK รอ `RE-280`
อยู่แล้วตาม `NOW.md`) -- เขียนจดหมาย `20260906_2016_LANE-UI-TO-COO-item-operate-res-promotion-item-
4-is-stuck-not-a-flag-flip.md` (`ADDRESSEE: COO`) อธิบายเต็ม + ข้อเสนอสำหรับตอนที่ `RE-280` ปลด แล้ว
**ทำงานสำรองต่อในรอบเดียวกันตามกฎ "เขียนคำถาม แล้วเดินต่อ"** (ไม่รอคำตอบ)

## งานที่ทำจริงรอบนี้: การ์ดกันการต่อสาย express/community_social ก่อน migration ของมันเอง
(งานสำรองข้อ 2 ของไฟล์รอบ `rqwwp8` -- เลือกข้อนี้เพราะข้อ 1 ติดตามข้างบน และข้อนี้อยู่ในเขตเขียนของ
LANE-UI ล้วน ไม่ต้องรอสายอื่น)

ไฟล์ใหม่ (server): `tests/test_ui_express_community_social_migration_guard.py` -- ตรวจว่า ถ้า
`runtime.py` import `ui_express_wire`/`ui_community_social_wire` เมื่อไหร่ (โมดูลใดยังไม่ต่อสายตอนนี้
-- grep ยืนยันแล้ว: ไม่มี `from .ui_express_wire`/`from .ui_community_social_wire` ใน `runtime.py`)
ต้องเช็คว่าโมดูลนั้นเลิกเรียก `ui_social_wire.encode_untagged_wstring`/`read_untagged_wstring` แล้ว
(migrate ไป `wstring_tag`/`read_wstring_tag` เหมือน `ui_friend_wire.py`/`ui_mail_wire.py`/
`ui_party_wire.py`/`ui_trade_wire.py`) -- ไม่งั้นแดงทันที พร้อมข้อความชี้ทางแก้

## `pf-adversary` ครั้งที่ 1 (สั่งต้นรอบพร้อมเริ่มงาน) -- ผลคืนภายในรอบ
สั่งตรวจไฟล์ทดสอบใหม่ (เวอร์ชัน regex/substring แรก) แบบ adversarial เต็มรูปแบบ (worktree แยก)

**ผลคืน: พบ 2 ข้อบกพร่องจริง ยืนยันด้วยการรีโปรดิวซ์จริงทั้งคู่**
1. regex `^from \.<module> import` (MULTILINE) ไม่จับ import แบบ indent ในฟังก์ชัน -- `runtime.py`
   มี `from . import ui_logout_exit_game` แบบนี้อยู่แล้วจริง (บรรทัด ~7585) ⇒ ถ้าต่อสาย
   `ui_express_wire` ด้วยรูปแบบเดียวกัน การ์ดจะรายงาน "ยังไม่ต่อสาย" ทั้งที่ต่อจริงแล้ว (verified: inject
   บรรทัดนี้เข้า `runtime.py` จริงชั่วคราว การ์ดผ่านหมด แล้ว revert)
2. substring `wire.encode_untagged_wstring(` ผูกกับ alias `wire` ตายตัว -- เปลี่ยน alias เป็น `sw`
   (แก้ call site คู่กันด้วย) ทำให้เทสที่ไฟล์ประกาศว่าเป็น "การ์ดจริง" ผ่านทั้งที่โมดูลยังใช้คู่ผิดอยู่
   ภายใต้ชื่ออื่น (verified ด้วยโค้ดสังเคราะห์)

**แก้ในรอบนี้เลย** (ของเล็ก อยู่ในไฟล์เดียวที่เพิ่งเพิ่มเอง ไม่ใช่ของสายอื่น): เขียนใหม่ทั้งไฟล์ด้วย
`ast` แทน regex/substring -- `ast.walk` หา `Import`/`ImportFrom` ทุกจุดไม่ว่าจะ indent แค่ไหน และ
resolve alias ของ `ui_social_wire` (รวมทั้งชื่อฟังก์ชันที่ import ตรง) ก่อนเทียบ call site เพิ่มเทส
regression สองคลาส (`ImportDetectionTests`, `UntaggedPairCallDetectionTests`) ปักทั้งสองข้อบกพร่องไว้
เป็น synthetic source string แล้ว re-verify ด้วยการรีโปรดิวซ์ของ adversary เองบนไฟล์จริงอีกครั้ง (inject
`from . import ui_express_wire` เข้า `runtime.py` ชั่วคราว → แดงตามคาด → revert) -- commit แยกจาก
commit แรกตามกฎ "ตัวแก้ต้องเป็นคอมมิตของตัวเอง"

ไม่ได้สั่ง adversary ครั้งที่ 2 ต่อตัวแก้ (เพดาน 2 ครั้ง/รอบ ยังไม่ครบ แต่ตัวแก้ผ่านการรีโปรดิวซ์ตรงของ
adversary เองแล้วทั้งสองข้อ + เทส regression ใหม่ยืนยันซ้ำ -- ถือว่าเพียงพอสำหรับของขนาดนี้ ไม่ใช่การ
ข้ามกฎ)

## เทส
`PYTHONPATH=src python3 -m pytest tests/test_ui_express_community_social_migration_guard.py
tests/test_ui_express_wire.py tests/test_ui_community_social_wire.py tests/test_ui_mail_wire.py
tests/test_ui_party_wire.py tests/test_ui_trade_wire.py tests/test_ui_friend_wire.py
tests/test_ui_social_wire.py tests/test_lane_ui_friend_mail_party_trade_dispatch_wiring.py -q` =
189 passed, 97 subtests passed (หลังตัวแก้ adversary)

ชุดเต็ม `pytest tests/ -q` (บนต้นไม้ที่ `git merge origin/main` แล้วเป็น commit สุดท้ายจริง, รันครั้ง
เดียว): **12452 passed, 373 skipped, 26241 subtests passed, 1 failed**
(`tests/test_lane_a_choose_npc_scene1.py::TheRegisteredResponderDropsTheTalkTriggerAtRealDispatch
Tests::test_the_talk_trigger_is_still_missing_at_real_dispatch_today`) -- **ตรวจแล้วว่าไม่ใช่ของรอบ
นี้**: `git worktree add` ที่ `origin/main` สะอาด (ไม่มี diff ของสายนี้เลย) แล้วรันเทสไฟล์เดียวกัน ⇒
แดงเหมือนกันบน `main` เพียว (ตัวไฟล์เป็นของ LANE-A ไม่ใช่เขตเขียนของ LANE-UI) -- บันทึกไว้ในไฟล์รอบนี้
ให้สายอื่น/chief ทราบ ไม่ใช่ของที่ PR นี้ต้องแก้ ลบ worktree ทิ้งหลังตรวจ (`git worktree remove`)

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` = PREFLIGHT PASS (รันก่อน
commit สุดท้ายและก่อน push จริง ทั้งสองครั้ง) · `pf_gate_preflight.py --pr-body <ไฟล์> --pr-stage
final` = `[prbody] PASS - exactly one marker line`

## nonclaims
1. ไม่อ้างว่าการ์ดใหม่นี้กันทุกวิธีที่จะต่อสายโมดูล -- `importlib.import_module` แบบไดนามิกหรือ string
   ไม่ถูกตรวจ (บันทึกไว้ใน module docstring ของไฟล์เทสเอง)
2. ไม่อ้างว่า `test_lane_a_choose_npc_scene1.py` แดงเพราะ PR นี้ -- verified ด้วย clean worktree ของ
   `origin/main` แดงเหมือนกัน
3. ไม่อ้างว่า promotion ข้อ 4 ปิดแล้วหรือถูกปฏิเสธถาวร -- STUCK รอ LANE-DB ปลด `RE-280` เพื่อมี event
   ทั่วไปให้เกาะแทน chat trigger เขียนข้อเสนอไว้ในจดหมายแล้ว
4. ไม่อ้างว่าผู้เล่นเห็นอะไรเปลี่ยนวันนี้ -- งานรอบนี้เป็นเทส CI ล้วน ไม่มีโค้ด production ถูกแตะ

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `#1554` (`[LANE-UI] round u3pzcz: claim`) กิ่ง `claude/peaceful-pascal-u3pzcz` --
  ไฟล์รอบนี้ + จดหมาย 1 ฉบับใหม่ (`20260906_2016_...item-operate-res-promotion-item-4...`) + ลบ
  `_claim.md` (ไม่มีจดหมายเก่าให้ consume รอบนี้ -- ตรวจแล้วว่างตามข้อ 2 ข้างบน)
- `pirate-force-server`: PR `#945` (`[LANE-UI] round u3pzcz: guard test for express/community_social
  wiring before migration`) กิ่ง `claude/inspiring-feynman-u3pzcz` -- ไม่ draft, marker
  `PF-AUTOMERGE: v4`, ยืนยันด้วย GET แล้ว (`state=open draft=false` body มีบรรทัด marker) -- 1 ไฟล์
  ใหม่ (+340 บรรทัด รวม 3 commits: เวอร์ชันแรก + ตัวแก้ adversary -- ดูรายละเอียดข้างบน)
- เลขใบใหม่รอบนี้: ไม่มี GT/RE ใหม่ -- งานเป็นเทส CI + จดหมายบล็อกเกอร์ ไม่ใช่ฟีเจอร์ใหม่ที่ต้องยืนยัน
  บนจอ

## รอบหน้าทำอะไร
🔴 **แก้ระหว่างจบรอบ**: หลัง commit งานหลักข้างบนแล้ว แต่ก่อน push, `git fetch origin main` ซ้ำพบว่า
main ขยับ (COO รอบ `1941`, 19:55+07:00) พร้อมจดหมายใหม่จ่าหน้าตรงถึง LANE-UI: `notes_to_chief/
20260906_1955_COO-DECISION-panya1910-find-captain-report-frame-in-binary-LANE-UI.md` (**PANYA-ORDER
`1910` ข้อ 2.2** ผ่าน ka1-A) -- **สั่งตรงว่ารอบถัดไปของ UI คือ RE static ในตัวไคลเอนต์เพื่อหาเฟรมที่
เปิดกล่อง `Common_Confirm` "รายงานกัปตัน เรือเทียบท่า [ชื่อเกาะ]"** (ไล่ string → handler → vital id →
layout ใช้ `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`) ส่งผลเป็นจดหมาย `*_LANE-UI-TO-A-
candidate-frame-<vital>.md` (ADDRESSEE: LANE-A cc COO) -- **มาก่อน PR migrate wstring 0x48 (`1713`)**
ซึ่งเลื่อนไปรอบถัดจาก RE นี้ (ทำต่อในรอบเดียวกันได้ถ้า RE จบก่อนหมดรอบ) · มีเวลา 2 รอบ จบรอบ 2 ไม่เจอ
ต้องเขียนจดหมายบอกว่าไล่ถึงไหน ห้ามเงียบ · ห้ามแตะ `AddSurveyData`/record · ห้ามออกใบ attended สำหรับ
M2 · ห้ามเดา vital จากชื่อ

**จดหมายฉบับนี้ยังไม่ถูก consume ในรอบนี้โดยเจตนา** -- อ่านแล้วและบันทึกไว้ที่นี่ แต่ยังไม่ผลิตผลลัพธ์ที่
สั่ง (จดหมายผู้สมัครเฟรมถึง LANE-A) เพราะงานหลักของรอบนี้ commit ไปก่อนจดหมายนี้มาถึง -- consume จริง
(วาง `.CONSUMED.txt`) เมื่อรอบถัดไปเริ่มไล่ RE นี้จริง

รอบหน้า: **เริ่มด้วยงาน RE ข้างบนทันที** (แทนคิวหลักข้อ 3 เดิมของ `prompts/LANE-UI.md` และแทนที่จะรอ
คำตอบจดหมาย `2016` เรื่อง promotion ข้อ 4 -- COO ตอบเรื่องนั้นแล้วบางส่วนใน `1955` ข้อ 4 เอง: "promotion
ข้อ 4 ถอยไปอีกหนึ่งรอบ" ตรงกับที่จดหมาย `2016` เสนอ (STUCK รอ LANE-DB) อยู่แล้ว ไม่ขัดกัน)

## งานสำรอง (ทำเมื่องานหลักติด)
1. คิวหลักข้อ 3 ของ `prompts/LANE-UI.md` (ฟังก์ชันถัดไปที่ layout รู้แล้วใน `docs/UI_LANE.md`) --
   ไฟล์: ตาม `docs/UI_LANE.md` -- หลักฐานผ่าน: implement + เทส + ใบ GT ทีละปุ่ม
2. รายงาน `test_lane_a_choose_npc_scene1.py` แดงบน main ให้ chief/LANE-A ทราบผ่านจดหมายแยก ถ้ายัง
   ไม่มีใครรายงาน -- ไฟล์: `notes_to_chief/` -- หลักฐานผ่าน: จดหมายส่งแล้ว ไม่ใช่ของ LANE-UI ต้องแก้เอง
3. รอคำตอบจดหมาย `2016` จาก COO เรื่องข้อเสนอโปรโมต `item_operate_res_hypothesis.py` ตอนที่ `RE-280`
   ปลด -- ไฟล์: `docs/PROMOTION_BACKLOG.md` (อัปเดตแถวถ้า COO ตัดสินต่างจากข้อเสนอ) -- หลักฐานผ่าน:
   COO-DECISION ตอบแล้ว

SCOREBOARD: NONE | ไม่มีอะไรที่ผู้เล่นทำได้เพิ่มจากงานนี้ (เทส CI ล้วน) -- ป้องกันบั๊กเดียวกับที่
mail/party/trade เพิ่งแก้ไม่ให้เกิดซ้ำกับ express/community_social ถ้ามีรอบไหนต่อสายมันก่อน migrate
โดยไม่ตั้งใจ + ชี้บล็อกเกอร์จริงของ promotion ข้อ 4 (chat-trigger backdoor เสี่ยง item-dupe ถ้าปลด
ตรงไปตรงมา) แทนการส่ง PR เดา | PR `pirate-force-server#945` · จดหมาย
`pf_bridge/notes_to_chief/20260906_2016_LANE-UI-TO-COO-item-operate-res-promotion-item-4-is-stuck-
not-a-flag-flip.md`

-- LANE-UI (round `u3pzcz`)
