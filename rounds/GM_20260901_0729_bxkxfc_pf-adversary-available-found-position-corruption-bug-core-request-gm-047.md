# รอบ `bxkxfc` -- 2026-09-01T07:29+07:00

## หนึ่งบรรทัด

Agent tool (pf-adversary) ใช้ได้จริงรอบนี้ (ต่างจากทุกรอบก่อน) -- รีวิวย้อนหลัง GM-A ที่ merge
ด้วย self-review เท่านั้น พบบั๊กจริงระดับสูง: `runtime.py:5304` เช็ค label ผิด ทำให้
CORE-REQUEST-GM-045's resync ไม่เคยทำงานกับ cross-scene warp จริงเลย ตำแหน่งผู้เล่นเพี้ยนซ้ำ
GT-106 -- เปิด CORE-REQUEST-GM-047 ถึง chief ไม่มี src diff รอบนี้ (ไม่ใช่เขตเขียนของสายนี้)

## round-lock

`list_pull_requests(state=open)` ทั้งสอง repo ก่อนแตะไฟล์ใด ๆ: ไม่มี `[LANE-GM]` ค้าง (มีแต่
`[LANE-E]` #675/#448 และ `[LANE-A]` #674/#447 ของสายอื่น ไม่แตะ) ตรวจชะตา PR รอบก่อน (`vsopwk`)
ด้วย `pull_request_read(method=get)` โดยตรง -- `list_pull_requests` คืนค่า `merged:false` ผิดสำหรับ
ทั้ง `pf_bridge#673` และ `pirate-force-server#446` (แต่ `get` ตรงยืนยัน `merged:true` จริงทั้งคู่
`merged_at` ตรงกับที่รอบ `vsopwk` อ้าง) -- บันทึกไว้เป็นข้อสังเกต: `list_pull_requests` field
`merged` ไม่น่าเชื่อถือสำหรับ PR ปิดแล้ว ต้อง `get` ตรงเสมอก่อนสรุปว่างานหายจาก main

`git fetch origin main` + `git reset --hard origin/main` ทั้งสอง repo (local branch ตามหลัง 1-2
commit) แล้วเปิด lock: empty commit `round claim: bxkxfc` ทั้งสอง repo, เปิด draft PR ก่อนแตะไฟล์ใด ๆ
(`pf_bridge` #677, `pirate-force-server` #450)

## กล่องจดหมาย

Grep `ADDRESSEE: LANE-GM` ไม่มี `.CONSUMED.txt` คู่ = ว่าง ไม่มีใบใหม่ให้บริโภครอบนี้ (Codex letters
ล่าสุด `0419`/`0432`/`0443` บริโภคไปแล้วโดยรอบ `jd4jqp`/chief ก่อนหน้า)

## Baseline

`pytest tests/` = 6153 passed, 327 skipped, 0 failed เขียว(cloud sanity) ก่อนเริ่มตรวจ

## pf-adversary -- ใช้ได้แล้ว (เปลี่ยนจากทุกรอบก่อนหน้า)

`ToolSearch`/`Agent` มี `subagent_type: pf-adversary` ให้เรียกจริงในสภาพแวดล้อมของรอบนี้ ต่างจาก
ทุกรอบ LANE-GM ก่อนหน้า (`vsopwk`, `jd4jqp`, `3g2w5z`, ฯลฯ) ที่ค้นแล้วไม่เจอ ต้องแทนด้วย self-review
เสมอ **บันทึกไว้ว่าตัวแปรนี้ผันแปรตามสภาพแวดล้อมของแต่ละเซสชัน ไม่ใช่ค่าคงที่ของโปรเจกต์ -- สายอื่น
ควรเช็ค ToolSearch ทุกรอบเองด้วย**

ใช้โอกาสนี้รีวิวย้อนหลัง GM-A (`pirate-force-server#440`, merge แล้วด้วย self-review 12 ข้อรอบ
`jd4jqp`) เพราะเป็น wire change ที่ blast radius สูงสุดในบรรดาที่ merge ไปโดยไม่มี pf-adversary จริง

## ผล -- พบบั๊กจริง (ไม่ใช่ style nit)

**`runtime.py:5304`**: `if action and action[0] == chat_command_action.WARP_ACTION_LABEL:` --
`WARP_ACTION_LABEL` (`chat_command_action.py:355`) คือ label ของ ForcePos **ฉากเดียวกันเท่านั้น**
(`warp_executor.py:286-291` ปฏิเสธ cross-scene เอง) label cross-scene ทั้งสองตัว
(`chat_command_action.py:378,399`) ไม่ปรากฏใน `runtime.py` เลย (grep ยืนยัน 0 hit ด้วยตัวเอง ไม่เชื่อ
agent เฉย ๆ)

ผล: `_gm_warp_resync_selected_scene` (CORE-REQUEST-GM-045, `runtime.py:5336-5408` -- ฟังก์ชันเอง
ถูกต้อง มี early-return จัดการ same-scene ไว้แล้วที่บรรทัด 5398-5401) **ไม่เคยถูกเรียกสำหรับ
cross-scene warp จริงสักครั้ง** ทั้งแบบมีพิกัดและแบบ GM-A ไม่มีพิกัด `self.foundation.selected
.position.scene_id` ค้างเป็นฉากต้นทางหลัง live warp ทุกครั้ง -- `TargetPos` ถัดไปจากฉากปลายทางจริง
ถูก `_checkpoint_exact_target` (`runtime.py:3698+`) ประกอบเป็นแถวผิด (`scene_id` เก่า + พิกัดใหม่)
แล้วเขียนลง DB จริงผ่าน `lifecycle.checkpoint` -- ซ้ำอาการ `GT-106` ทุกประการ

**หลักฐานว่าไม่ใช่แค่ทฤษฎี**: `GT-172` finding F-1 (`CORE-REQUEST-GM-045` เดิม) สังเกตอาการนี้จาก
เซสชัน attended จริงเมื่อเช้านี้ (~02:25 น.) แล้ว -- สำมะโนยิงด้วยทะเบียนฉากเก่าหลัง warp 4 ครั้งซ้อน
เซสชันนั้นมีโอกาสสูงเขียนแถวตำแหน่งผิดลง DB ไปแล้ว (ยังไม่ยืนยัน ไม่มีสิทธิ์เข้า DB เอง)

**ทำไมเทสเขียว**: `tests/test_gm_warp_position_confirmed.py::GmWarpSelectedSceneResyncTests`
(บรรทัด 219-238, 613-622) monkeypatch dispatch ให้คืน `WARP_ACTION_LABEL` เสมอ แม้เทสตั้งชื่อว่า
ทดสอบ cross-scene -- คู่ผสมนั้นเป็นไปไม่ได้จริงในโปรดักชัน (ForcePos ปฏิเสธ cross-scene เอง)
`test_gm_warp_executor.py`/`test_gm_chat_command_action.py` ที่ใช้ label จริงไม่เคยพา flow ไปถึง
`runtime.py`

**ทำไม self-review ของรอบ `jd4jqp` พลาด**: ข้อที่อ้างว่า "census-resync ครอบคลุม GM-A ให้ฟรี" อ่าน
แค่ว่าฟังก์ชัน resync มีอยู่และ logic ถูก ไม่ได้ไล่ตาม caller ว่าเรียกด้วย label ไหนจริง -- บทเรียน:
การอ้าง "ครอบคลุมให้ฟรี" ต้องไล่ label/เงื่อนไข dispatch จริงเสมอ ไม่พอแค่อ่านว่าฟังก์ชันดูถูก

## สี่ข้อที่ตรวจแล้วไม่พบปัญหา (บันทึกกันขุดซ้ำ)

1. GM authorization gate ที่ `handle_local_talk_chat` -- บังคับถูกจุดเดียว ไม่มีทาง bypass
2. Scene validation ของ path ไม่มีพิกัด -- fallback เป็น stage สำหรับฉากไม่รู้จัก ไม่มี mismatch
3. เทส kill-switch `WARP_CROSS_SCENE_LIVE_TELEPORT_AUTHORIZED = False` ทุกจุด -- ถูกต้อง ไม่บัง
4. `warp_executor.*` ไม่มี auth check ในตัวเอง -- ตรง pattern เดิมทั้งโมดูล ไม่ใช่ช่องโหว่ใหม่
   (แต่เป็น landmine ถ้ามี direct caller ในอนาคต -- บันทึกไว้เฉย ๆ)

## CORE-REQUEST-GM-047

เปิดถึง chief แล้ว (`runtime.py:5304` เป็นเขตของ chief) ระบุจุดแก้บรรทัดเดียว (เปลี่ยนจากเช็ค label
เดียวเป็นเช็คสมาชิกเซตสาม label GM-warp) พร้อมเทสที่พิสูจน์ ทำเครื่องหมายเร่งด่วน: `GT-182` ยังอยู่
ในคิว attended รอ merge -- ถ้าทดสอบก่อนแก้จะเพี้ยนตำแหน่งลง DB จริงอีกรอบ

## GM-B -- ยังบล็อกถูกต้อง

`RE-172` ตอบลบแล้ว ใบถามเจ้าของ (`2327`) ยังไม่มีคำตอบ -- เข้าเงื่อนไข (ข) ไม่เดาทางเอง

## ที่ไม่ทำในรอบนี้ (เจตนา)

- ไม่แก้ `runtime.py:5304` เอง -- นอกเขตเขียนของสายนี้ เปิด CORE-REQUEST แทน
- ไม่แตะ canonical DB เพื่อตรวจแถวเสีย -- ไม่มีสิทธิ์
- ไม่แก้หัวใบ `GT-182` -- chief เป็นผู้เปิด
- ไม่แตะ `gm/attr_wire.py`/GM-B (ล็อกเดิม)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** -- รอบนี้คือรีวิว/พบบั๊ก/CORE-REQUEST ล้วน ไม่มี wire ใหม่ 🔴 คำเตือน: อย่าเพิ่งรัน
`GT-182` จนกว่า `GM-047` จะแก้

## nonclaims

1. ไม่อ้างว่าแถว DB เสียแน่นอน -- หลักฐานทางอ้อมสูง (`GT-172` F-1) แต่ไม่มีสิทธิ์ยืนยันเอง
2. `_gm_warp_resync_selected_scene` เองไม่มีบั๊ก -- ปัญหาที่ caller เท่านั้น
3. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone, ไม่แตะ
   `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
   `scenarios/combat_*.json`
4. ไม่ลบประวัติ
5. GM-B ไม่มีความคืบหน้า

## PR

`pf_bridge` #677, `pirate-force-server` #450

— สาย GM รอบ `bxkxfc`
