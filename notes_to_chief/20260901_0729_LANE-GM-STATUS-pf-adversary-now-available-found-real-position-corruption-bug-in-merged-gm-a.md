[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: สาย GM รอบ `bxkxfc` · 2026-09-01T07:29+07:00]

# LANE-GM-STATUS -- Agent tool (pf-adversary) ใช้ได้แล้วรอบนี้ พบบั๊กจริง: GM-045's resync ไม่เคยทำงาน
ตำแหน่งผู้เล่นเพี้ยนซ้ำ GT-106 ทุกครั้งที่ warp ข้ามฉากแบบ live -- เปิด CORE-REQUEST-GM-047

## round-lock

`list_pull_requests(state=open)` ทั้งสอง repo ก่อนแตะไฟล์ใด ๆ: ไม่มี `[LANE-GM]` ค้าง (มีแต่
`[LANE-E]` #675/#448 และ `[LANE-A]` #674/#447 ของสายอื่น ไม่แตะ) ตรวจ PR รอบก่อน (`vsopwk`,
`pf_bridge#673`/`pirate-force-server#446`) ด้วย `pull_request_read(method=get)` ตรง ๆ (ไม่เชื่อ field
`merged` จาก `list_pull_requests` เฉย ๆ เพราะ list มา `false` ผิดของทั้งคู่ -- `get` ตรงยืนยัน
`merged:true` จริงทั้งสอง) งานรอบก่อนอยู่บน `main` แล้ว `git fetch origin main` + `reset --hard` ทั้ง
สอง repo ก่อน เปิด lock: empty commit `round claim: bxkxfc` ทั้งสอง repo แล้วเปิด draft PR ก่อนแตะ
โค้ดใด ๆ (`pf_bridge` #677, `pirate-force-server` #450)

## กล่องจดหมาย

ไม่มีใบใหม่ addressed ถึง `LANE-GM` ที่ยังไม่มีสตับ (grep `ADDRESSEE: LANE-GM` ไม่มี `.CONSUMED.txt`
คู่ = ว่าง) เช็คโค้ดัค (Codex) รายการล่าสุด (`0419`/`0432`/`0443`) ก็บริโภคไปแล้วโดยรอบ `jd4jqp`/chief
ก่อนรอบนี้ทั้งหมด ไม่มีอะไรใหม่ให้บริโภค

## สิ่งที่ทำรอบนี้: รัน pf-adversary ย้อนหลังกับ GM-A ที่ merge ไปแล้วด้วยแค่ self-review

Agent tool (subagent_type `pf-adversary`) **ใช้ได้จริงในสภาพแวดล้อมของรอบนี้** -- ต่างจากทุกรอบก่อน
หน้า (`vsopwk`, `jd4jqp`, `3g2w5z`, ...) ที่ค้น ToolSearch แล้วไม่เจอ ต้องแทนที่ด้วย self-review
ทั้งหมดแล้วแปะ `[สมมติของสาย GM - รอ COO ยืนยัน]` ไว้รอ COO confirm ความเพียงพอ -- **ตัวแปรสภาพแวดล้อม
นี้ไม่คงที่ระหว่างรอบ สายอื่นควรเช็ค ToolSearch ทุกรอบเองด้วย ไม่ใช่เชื่อรอบก่อนของตัวเอง**

ใช้โอกาสนี้รีวิวย้อนหลัง GM-A (`pirate-force-server#440`, merge แล้ว, ตอนนั้น self-review 12 ข้อ)
เพราะเป็นการเปลี่ยน wire ที่มี blast radius สูงสุดในบรรดาที่ merge ไปโดยไม่มี pf-adversary จริง

**ผล: self-review ตอนนั้นพลาดจริง** -- พบข้อบกพร่องระดับสูง 1 ข้อ ตรวจซ้ำด้วยตัวเอง (grep ตรงจาก
source ไม่เชื่อ agent เฉย ๆ) ยืนยันตรงกันทุกจุด รายละเอียดเต็ม/บรรทัดอ้างอิง/ข้อเสนอแก้ อยู่ใน
`20260901_0729_LANE-GM-CORE-REQUEST-GM-047-*.md` (ใบนี้แค่สรุปหัวข้อ):

`runtime.py:5304` เช็ค label การ warp ด้วย `== WARP_ACTION_LABEL` เดียว (ป้าย ForcePos ฉากเดียวกัน
เท่านั้น) แทนที่จะเช็คสาม label GM-warp ทั้งหมด -- ผลคือ `_gm_warp_resync_selected_scene`
(CORE-REQUEST-GM-045 ที่จดหมาย `0403` เคยตอบว่า "wired" แล้ว) **ไม่เคยถูกเรียกสำหรับ cross-scene warp
จริงสักครั้ง** ทั้งแบบมีพิกัดและแบบ GM-A ไม่มีพิกัด `self.foundation.selected.position.scene_id` เลย
ค้างเป็นฉากต้นทางตลอดเซสชัน หลัง live warp ทุกครั้ง -- `TargetPos` ถัดไปที่มาจากฉากปลายทางจริงจึงถูก
`_checkpoint_exact_target` ประกอบเป็นแถว `scene_id` ผิด + พิกัดข้ามฉาก แล้วเขียนลง DB จริง (ผ่าน
`lifecycle.checkpoint`) ซ้ำอาการ `GT-106` ทุกประการ

**นี่ไม่ใช่แค่ทฤษฎี**: `GT-172` ที่เพิ่ง PASS วันนี้ (ผู้เทส attended จริง ~02:25 น.) มี finding F-1
ของตัวเอง (`CORE-REQUEST-GM-045`) ที่สังเกตอาการนี้ตรง ๆ อยู่แล้ว (สำมะโนยิงด้วยทะเบียนฉากเก่าหลัง
warp) -- แปลว่าเซสชันเทสจริงเมื่อเช้านี้มีโอกาสสูงที่จะเขียนแถวตำแหน่งผิดลง DB ไปแล้ว (ยังไม่ยืนยัน
ไม่มีสิทธิ์เข้า DB เอง ไม่ใช่ขอบเขตใบนี้ -- ระบุไว้ให้ chief/COO ตรวจ)

## ทำไม self-review 12 ข้อของรอบ `jd4jqp` ถึงพลาด

ข้อที่เกี่ยวข้องที่สุด ("census-resync ครอบคลุม GM-A ให้ฟรีโดยไม่ต้องขอจุดเสียบเพิ่ม") **อ่านแค่ว่า
`_gm_warp_resync_selected_scene` มีอยู่และดูถูกต้อง ไม่ได้ไล่ตามว่า caller เรียกมันด้วย label ไหนจริง**
-- ตรงกับที่ pf-adversary เรียกว่า "อ่านหลักฐานของตัวเองแค่ครึ่งเดียว" เป็นบทเรียนที่ต้องจำ: การยืนยัน
"ฟังก์ชันมีอยู่และ logic ดูถูก" ไม่พอ ต้องไล่ label/เงื่อนไข dispatch จริงด้วยเสมอเวลาอ้างว่า
"ครอบคลุมให้ฟรี"

## CORE-REQUEST-GM-047

เปิดถึง chief แล้ว (`runtime.py:5304` เป็นเขตของ chief ไม่ใช่ของสายนี้) ระบุจุดแก้เดียว บรรทัดเดียว
(เปลี่ยนจากเช็ค label เดียวเป็นเช็คสมาชิกเซตสาม label) พร้อมเทสที่พิสูจน์ **เร่งด่วน**: `GT-182`
(GM-A) ยังนั่งอยู่ในคิว attended สถานะ `BLOCKED-ON-WIRING` -- ถ้ามีคนกด PASS ก่อนแก้ข้อนี้ ตำแหน่ง
จะเพี้ยนลง DB จริงอีกรอบ ขอให้ chief/COO พิจารณาแปะคำเตือนที่หัวใบก่อน (สายนี้ไม่มีสิทธิ์แก้หัวใบที่
chief เปิด)

## สี่ข้อที่ pf-adversary ตรวจแล้วไม่พบปัญหา (เพื่อบันทึกไว้ ไม่ต้องขุดซ้ำ)

1. GM authorization gate: บังคับถูกจุดเดียวที่ `handle_local_talk_chat` ก่อน parse ใด ๆ ไม่มีทาง
   bypass บน production call path
2. Scene validation ของ path ไม่มีพิกัด: `world_scene_travel.destination` โยน
   `KeyError`/`ValueError` แล้ว fallback เป็น stage สำหรับฉากที่ไม่รู้จัก ไม่มีทาง mismatch scene id
3. `WARP_CROSS_SCENE_LIVE_TELEPORT_AUTHORIZED = False` ในเทสต่าง ๆ เป็น regression test ของ
   kill-switch ที่ตั้งชื่อ/ยืนยันถูกต้องทุกจุด ไม่ได้บังพฤติกรรมจริง
4. `warp_executor.*` ไม่มี auth check ในตัวเอง (auth อยู่ที่ caller เท่านั้น) -- ตรงกับ pattern เดิม
   ของทุก wire-builder ในโมดูลนี้ ไม่ใช่ช่องโหว่ใหม่ แต่เป็น landmine ถ้ามี direct caller ในอนาคต
   (บันทึกไว้เฉย ๆ ไม่ใช่ของที่ต้องแก้ตอนนี้)

## GM-B -- ยังบล็อกถูกต้อง ไม่แตะ

`RE-172` ตอบลบแล้ว ใบถามเจ้าของ (`2327`) ยังไม่มีคำตอบ -- เข้าเงื่อนไข (ข) ไม่เดาทางเอง

## เทสที่พิสูจน์

Baseline ก่อนเขียนจดหมายใด ๆ: `pytest tests/` = 6153 passed, 327 skipped, 0 failed เขียว(cloud
sanity) (ไม่มีการแก้โค้ดรอบนี้ -- CORE-REQUEST-GM-047 ขอให้ chief แก้ ไม่ใช่สายนี้)

## ที่ไม่ทำในรอบนี้ (เจตนา)

- ไม่แก้ `runtime.py:5304` เอง -- นอกเขตเขียนของสายนี้ เปิด CORE-REQUEST แทน
- ไม่แตะ canonical DB เพื่อตรวจว่ามีแถวเสียจริงหรือยัง -- ไม่มีสิทธิ์ ให้ chief/COO ตรวจ
- ไม่แก้หัวใบ `GT-182` -- chief เป็นผู้เปิด ไม่ใช่เขตแก้ของสายนี้
- ไม่แตะ `gm/attr_wire.py`/GM-B (ล็อกเดิม รอเจ้าของ)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** -- รอบนี้เป็นการรีวิว/พบบั๊ก/เขียน CORE-REQUEST ล้วน ไม่มี wire ใหม่ ไม่มี chat command ใหม่
🔴 **คำเตือนตรงข้าม**: อย่าเพิ่งรัน `GT-182` จนกว่า `CORE-REQUEST-GM-047` จะแก้ -- เสี่ยงตำแหน่งเพี้ยน
ลง DB จริง

## nonclaims

1. ไม่อ้างว่าแถว DB เสียไปแล้วแน่นอน -- มีหลักฐานทางอ้อมสูง (`GT-172`'s F-1) แต่ไม่มีสิทธิ์เข้า DB
   ยืนยันเอง
2. ไม่อ้างว่า `_gm_warp_resync_selected_scene` เองมีบั๊ก -- ฟังก์ชันถูกต้อง ปัญหาที่ caller เท่านั้น
3. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone, ไม่แตะ
   `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
   `scenarios/combat_*.json`
4. ไม่ลบประวัติ -- ใบนี้/`GM-047` เป็นใบใหม่ ไม่ทับใบเดิม
5. GM-B ไม่มีความคืบหน้า -- รอเจ้าของเคาะทาง 1/2 เหมือนเดิม

## PR

`pf_bridge` #677, `pirate-force-server` #450 (จดหมาย/round file เท่านั้น ไม่มี src diff รอบนี้)

— สาย GM รอบ `bxkxfc`
