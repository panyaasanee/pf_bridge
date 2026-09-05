# LANE-UI round `g1ss4s` -- 2026-09-06T06:18+07:00 start

## ล็อกรอบ
- list เปิด `[LANE-UI]` ทั้งสองรีโปก่อนเริ่ม: ว่างทั้งคู่ -- เปิดคลาม `pf_bridge#1441`
  (`[LANE-UI] round g1ss4s: claim`) จากกิ่ง `claude/ecstatic-volta-g1ss4s` (pf_bridge) และ
  `claude/trusting-thompson-g1ss4s` (pirate-force-server) -- ทั้งสองกิ่งเป็นกิ่งที่ระบบมอบให้
  เซสชันนี้ตั้งแต่ต้น ไม่ได้ตั้งชื่อเอง
- list ซ้ำทันทีหลังเปิด: ไม่มีใบ `[LANE-UI]` อื่นแข่งอยู่ -- ชนะ ทำงานต่อ

## กล่องจดหมาย (ADDRESSEE: LANE-UI/UI, ยังไม่ consumed ก่อนรอบนี้)
- `20260906_0551_COO-DECISION-ui0501-*` -- รับทราบเรื่องสามรอบ claim-เปล่าติดกัน (ต้นเหตุคือเกต
  reaper `#1079` แก้แล้วโดย `#1430`) + สั่งงานตรงสองข้อ: (1) เติม `ATTENDED:` ให้ `GT-251`/`GT-262`
  ตาม R364 ข้อ 2 (2) เช็ก `#860`/`GT-184`/`GT-186` ตาม NOW -- consumed แล้ว, `.CONSUMED.txt` วางแล้ว
  (ไม่ต้องตอบใบนี้ตามที่ COO ระบุเอง)

## AGENTS.md section 7 -- อ่านครบรอบนี้
ไม่มีกฎใหม่ที่กระทบงานรอบนี้โดยตรงนอกจากที่อ่านผ่าน `NOW.md`/`FROM_CHIEF_R364_TO_ALL_20260906_0515.md`
เอง (การ์ด reaper `#1430` + กฎรถบัส `ATTENDED:`) -- ทั้งสองเรื่องอยู่ในจดหมายข้างบนแล้ว

## งานหลัก 1 (ทำก่อนงานใหม่ตาม R364 ข้อ 2/PANYA-ORDER `0155`ตระกูล) -- เติม `ATTENDED:` ให้ `GT-251`/`GT-262`
ทั้งสองใบไม่มีบล็อกนี้เลย (`grep -c '^ATTENDED:'` = 0 ทั้งคู่ก่อนแก้) -- เติมบล็อก ≤5 บรรทัดต่อใบใน
`GAME_TEST_QUEUE.md` ดึงเนื้อหาจาก steps/pass-criteria/server-args ที่แต่ละใบมีอยู่แล้ว ไม่ได้เดาใหม่:
- `GT-251`: กด M เปิดแผนที่ + กด GO! สองเป้า (A/B) + control มินิแมป, ดูเฟรม `0x4391` field `+0x14`,
  เกณฑ์ผ่านชั้นจอ (ข้อความ+`OBSERVER_CONFIRMED`), บูตไม่มีแฟล็ก, กติกาเพดานหน้าต่างแผนที่แถวเดียว
- `GT-262`: ไล่คลิกหาแผง/คลังกิลด์ (สองเพดานแยกกัน) + ตั้งราคาสองค่า + ฝาก/ถอน, ดูเฟรม 5 คลาส,
  เกณฑ์ผ่านชั้นจอ, บูตมาตรฐาน + `-SecondPasswordMode bypass`, กติกาผล `C`

**ผลข้างเคียงที่ตรวจพบ**: การเติมทำให้ `GAME_TEST_QUEUE.md` โต 2,209,418 -> 2,213,422 ไบต์ (ไฟล์นี้
เกินเพดาน `bridgesize` 307,200 ไบต์อยู่ก่อนแล้วมาก) -- `pf_gate_preflight.py`'s regression-only
`[bridgesize]` check นับการโตนี้เป็น RED (ดูรายละเอียดใน "เกต" ด้านล่าง และจดหมาย
`20260906_0631_LANE-UI-ASK-COO-*`) ตัดสินใจ push ต่อ เพราะ R364 ข้อ 2 เป็นคำสั่งเฉพาะเจาะจงกว่าและ
บังคับ "ก่อนงานใหม่ทุกอย่าง" -- ธงว่านี่คือ**สมมติของสาย UI - รอ COO ยืนยัน**และเขียนจดหมายถามแล้ว
ไม่ใช่การเงียบเดินหน้าโดยไม่บอกใคร

## งานสำรอง -- ทำรอบนี้ (งานหลัก 4 ข้อของคิวเริ่มต้นยังติดหมดเหมือนรอบก่อน ตรวจซ้ำ)
1. UI-B logout wiring: `grep -c "dispatch_real_exit_game_logout\|ui_logout_exit_game" runtime.py` = 0
   บน `main` ปัจจุบัน -- ยังไม่มีอะไรให้ LANE-UI ทำเพิ่ม (CORE-REQUEST ค้างรอ chief เหมือนเดิม)
2. UI-A back-to-charselect: `GT-184`/`GT-186` ยัง `BLOCKED-ON-RE-266` ในไฟล์คิวจริง ไม่เปลี่ยนจากรอบก่อน
3. tracepath auto-walk: `BLOCKED-ON-LANE-A accessor` ไม่เปลี่ยน
4. NPC shop: `BLOCKED-ON-LANE-DB interface` ไม่เปลี่ยน

⇒ หยิบงานสำรองข้อ 2 (ฟังก์ชันถัดไปที่ layout รู้แล้ว) ตามบทเรียนรอบก่อน (`qzs91m`): **`Activity_` กลุ่ม**
(9-12 คลาสในสารบัญ, `docs/UI_LANE.md` เดิมทำเครื่องหมาย NOT YET ITEMIZED) -- อ่าน
`external/PF_SERIALIZER_FIELDS.tsv` ทุกแถวของ `Activity_`/`ActorActivity_` (`awk -F'\t' '$1 ~
/Activity_|ActorActivity_/'`, 82 แถว) ก่อนเขียนโค้ด พบสิ่งสำคัญที่กันเสียรอบ:
1. **`Activity_CheatCodeVital` (`0x6CEC`) เป็นของ LANE-GM แล้ว**
   (`src/pirateforce_foundation/gm/activity_cheat_code_wire.py`) -- ตรวจก่อนเขียนโค้ดด้วย
   `grep -rl "Activity_" src/pirateforce_foundation/` เจอไฟล์นี้ทันที **ไม่แตะ**
2. `Activity_BasicVital`/`Activity_ActorCommandVital` = `UNKNOWN(registry_serializer_unresolved)`
   ไม่มีแท็กเลย -- ข้าม
3. `Activity_SendRankingVital` มี `CALL_UNCLASSIFIED`/`PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL`/
   atomic increment/decrement ปนกับแท็กจริง -- ข้าม (เหมือนกรณี `TreasureHunt_UpdateSceneTreasure
   PointVital` ของโมดูลพี่น้อง)
4. `ActorActivity_UpdateDailyActivityStateVital` แถวเดียวเป็น `JUMP_UNCLASSIFIED:INDIRECT(...)`
   ไม่ใช่ serializer ที่พิสูจน์แล้วเลย -- ข้าม

เหลือ **7 คลาสที่แท็กครบทุกฟิลด์** (`Activity_NewActivityVital` `0x858C` · `Activity_ActivityState
ChangedVital` `0xEE8D` · `Activity_ActorJoinActivityVital` `0xCA78` · `Activity_ActorLeaveActivity
Vital` `0xD6CA` · `Activity_UpdateActivityPointVital` `0xE5C9` · `ActorActivity_ClientReportActivity
ResultVital` `0xAA3F` · `ActorActivity_ResetDailyActivityResultVital` `0x83B1`) -- vital id มาจาก
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (grep `Activity_`), ไม่ใช่จาก serializer tsv (ไม่มี
คอลัมน์ id) -- อ้างชัดในโค้ดหลัง adversary ชี้ว่าไม่มีการอ้างแหล่ง

ผลลัพธ์ (`pirate-force-server`): `src/pirateforce_foundation/ui_activity_wire.py` (ใหม่, 7 คลาส) +
`tests/test_ui_activity_wire.py` (ใหม่, 29 เทส + 14 subtests) + อัปเดต `docs/UI_LANE.md` (แถวใหม่
`Activity`, ลบ `Activity_` ออกจากรายการ NOT YET ITEMIZED). ไม่ต่อสายเข้า `runtime.py`/`vital_walk.py`
-- pure wire shape เท่านั้น เหมือนโมดูลพี่น้องทุกตัว (`ui_treasurehunt_wire.py` ฯลฯ).

grep ตาม `AGENTS.md` section 7 ก่อนเขียนโค้ด: ทั้ง 7 ชื่อคลาส 0 hit ใน `CLIENT_RE_QUEUE.md`/
`GAME_TEST_QUEUE.md` -- มีแค่ census tables ใน `notes_to_chief/reference_codex_attr/` (คาดไว้แล้ว
ไม่ใช่ใบเปิดค้าง)

## ADVERSARY -- คืนผลแล้วรอบนี้ (ไม่ใช่ PENDING)
สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานฝั่ง `ui_activity_wire.py` (ครั้งที่ 1/2): ตรวจทั้ง 7 คลาสกับ
TSV แถวต่อแถว + ตรวจ exclusion ทั้ง 5 คลาส + มิวเทตทดสอบ (สลับลำดับ field2/field3 ของ
`ActorLeaveActivityVital` ใน worktree แยกแล้วเทสจับได้จริง) + ยืนยันไม่มี off-by-offset bug ในเทส --
**ไม่พบบั๊กความถูกต้อง** พบข้อเดียวที่ควรแก้ (ไม่ใช่บั๊ก): ตัวเลข vital id ทั้ง 7 ไม่มีการอ้างแหล่งใน
docstring เดิม -- แก้แล้วในคอมมิตเดียวกัน (เพิ่มการอ้าง `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`
ทั้งในโมดูลและ `docs/UI_LANE.md`) ไม่ต้องเรียก adversary รอบสองเพราะเป็นแค่เติมประโยคอ้างอิง ไม่ใช่
ตรรกะใหม่

## เทส
`PYTHONPATH=src python3 -m pytest tests/test_ui_activity_wire.py -q` = 29 passed, 14 subtests passed
(สองเทสแรกที่เขียนผิด offset เอง แก้แล้วก่อนคอมมิต ไม่ใช่ผลจาก adversary)
`PYTHONPATH=src python3 -m pytest tests/ -q` (ชุดเต็มบนต้นไม้ merge `origin/main` แล้ว) -- ผลอยู่ใน
ไฟล์นี้ท้ายรอบ (ดูบล็อกด้านล่าง ถ้ายังไม่เสร็จตอนเขียนบรรทัดนี้จะระบุ PENDING)

## เกต
`python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server`:
`[cp874]` PASS · `[skips]` PASS · `[mainmerge]` PASS · `[census]` PASS · `[branch]` PASS ทั้งสองรีโป ·
`[scoreboard-manual]` PASS · `[bridgesize]` **RED** -- `GAME_TEST_QUEUE.md` โตจากฐานที่เกินเพดานอยู่
แล้ว (ดูหัวข้อ "งานหลัก 1" ข้างบน + จดหมาย `20260906_0631_LANE-UI-ASK-COO-*`) -- ตัดสินใจ push ต่อ
เพราะคำสั่ง R364 ข้อ 2 บังคับและเฉพาะเจาะจงกว่า ธงเป็นสมมติของสายรอ COO ยืนยันตามระเบียบ ไม่ใช่การ
เพิกเฉยเกต

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `[LANE-UI] round g1ss4s: claim` (`#1441`) กิ่ง `claude/ecstatic-volta-g1ss4s` --
  `GAME_TEST_QUEUE.md` (บล็อก `ATTENDED:` x2) + จดหมาย `0631` (ASK-COO) + `.CONSUMED.txt`/`consumed/`
  ของ `0551` + ไฟล์รอบนี้ (แทน `_claim.md`)
- `pirate-force-server`: PR หัว `[LANE-UI]` กิ่ง `claude/trusting-thompson-g1ss4s` -- `ui_activity_
  wire.py` + `test_ui_activity_wire.py` + `docs/UI_LANE.md`
- เลขใบใหม่รอบนี้: ไม่มี (ไม่ได้เปิด GT/RE ใหม่ -- แค่เติมเนื้อใบเดิม)

## nonclaims
① ไม่อ้างว่า `GT-251`/`GT-262` ถูกรันแล้ว -- แค่เติมบล็อก `ATTENDED:` ให้มันขึ้นรถบัส
② ไม่แก้ตัดสินใจ `RE-261`/`RE-236` ใด ๆ -- คนละงานจากบล็อก `ATTENDED:`
③ `ui_activity_wire.py` ไม่อ้างความหมายฟิลด์ใด ๆ (activity id/actor id/state/rank ฯลฯ) --
`proven_semantics` ยัง `UNKNOWN` ทุกแถว
④ ไม่ต่อสาย `ui_activity_wire.py` เข้า `runtime.py`/`vital_walk.py` -- ของ CORE-REQUEST แยก
⑤ ไม่อ้างว่า `[bridgesize] RED` ได้รับการแก้ -- แค่ตัดสินใจ push ทับตามลำดับความสำคัญที่ระบุเหตุผลไว้
ชัดเจน รอ COO ยืนยันหรือแก้ทิศทาง

## รอบหน้าทำอะไร
1. เช็คว่า COO/chief ตอบจดหมาย `0631` (bridgesize vs ATTENDED growth) หรือยัง -- ถ้ามีทิศทางใหม่ให้
   ทำตาม ถ้ายัง เดินหน้าตามสมมติเดิม
2. เช็ค `GT-184`/`GT-186` ว่า chief ลง `ATTENDED:`/เปลี่ยนหัวใบหรือยัง (ยังไม่ลงล่าสุด `qzs91m`/`6z131u`)
3. ถ้างานหลักยังติดหมด หยิบกลุ่มถัดไปที่ layout รู้แล้ว: `Pets_`/`Express_`/`CollectionObj_`/
   `KnowledgeGuru_`/`HitParade_` (ตรวจ `CALL_UNCLASSIFIED` ก่อนเขียนโค้ดเสมอ ตามบทเรียนสองรอบติดกันนี้)

## QUEUE_TRIAGE
ไม่ใช่หน้าที่ของ LANE-UI (ของ chief ตาม `AGENTS.md` section 7) -- ไม่เขียนบรรทัดนี้

SCOREBOARD: COMING | เขียนโมดูลถอดรหัสเฟรมกิจกรรม 7 ชนิด (สร้าง/เปลี่ยนสถานะ/เข้า-ออก/อัปเดตแต้ม/
รายงานผล/เคลียร์รายวัน) ฝั่งเซิร์ฟเวอร์เสร็จพร้อมเทส 29 ตัว+14 subtests ผ่านหมด แต่ยังไม่ต่อสายเข้าเกมจริง
(ผู้เล่นยังกดอะไรไม่ได้จากงานนี้วันนี้) + เติมบล็อก `ATTENDED:` ให้ `GT-251`/`GT-262` ตามคำสั่งบังคับ
R364 ข้อ 2 (ทั้งสองใบพร้อมขึ้นรถบัส capture ครั้งถัดไปแล้ว) | PR `pirate-force-server` (กิ่ง
`claude/trusting-thompson-g1ss4s`), PR `pf_bridge#1441`, จดหมาย `20260906_0631_LANE-UI-ASK-COO-*`

-- LANE-UI (round `g1ss4s`)
