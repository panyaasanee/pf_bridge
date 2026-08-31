# รอบ `k0w291` -- 2026-09-01T03:18+07:00

## หนึ่งบรรทัด

บริโภคใบ `GT-172 RESULT` (PASS ทั้งสองชั้น, ADDRESSEE: LANE-GM) ปิดหัวใบ GT-172 ใน
`GAME_TEST_QUEUE.md` เป็น PASS แล้วเปิดสามใบแยกตามที่ใบขอ (`CORE-REQUEST-GM-045`,
`CORE-REQUEST-GM-046`, FINDING F-3) จากสามข้อสังเกตใหม่ที่พบระหว่างเทส

## round-lock

ไม่มี PR `[LANE-GM]` เปิดค้างก่อนเริ่ม (ตรวจด้วย `list_pull_requests(state=open)` ทั้งสอง repo --
เจอเฉพาะ `[LANE-E]` ของ chief ซึ่งไม่ใช่ล็อกของสายนี้) รอบก่อน (`kv02mn`) merged จริงทั้งสอง repo
(`pf_bridge#653` `merged=true` @2026-08-31T19:19:12Z, `pirate-force-server#429` `merged=true`
@2026-08-31T19:29:52Z -- ยืนยันด้วย `pull_request_read(method=get)`)

## กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-GM" notes_to_chief/*.md` แล้วเช็คคู่ `.CONSUMED.txt` ทีละไฟล์ พบหนึ่งใบ
ค้างจริง (อีกสองไฟล์ที่ grep ติดเป็น STATUS letter ของสายนี้เองที่อ้างถึงคำว่า "ADDRESSEE: LANE-GM"
ในเนื้อหา ไม่ใช่หัวใบของตัวเอง -- ตรวจ header แล้วทั้งคู่เป็น `ADDRESSEE: chief`):

`20260901_0225_GT172-RESULT-PASS-live-cross-scene-warp-works-plus-three-new-findings.md`
(ADDRESSEE: LANE-GM, จากผู้เทส attended) -- บริโภคแล้ว วางสตับ + สำเนาต้นฉบับไว้ `consumed/`

## ทำไมได้งานจริงรอบนี้ (ต่างจาก 10 รอบ verify-only ก่อนหน้า)

ใบนี้เป็นผลเทส attended ใหม่ (GT-172 ยิงจริงโดยเจ้าของ) ไม่ใช่จดหมายที่ค้างวนซ้ำเหมือนบล็อก A/B
เดิม -- priority-1 ของลำดับงาน (จดหมายที่จ่าหน้าถึง LANE-GM ยังไม่มี `.CONSUMED.txt`) มีของจริง
ให้ทำเป็นครั้งแรกในรอบนี้

## รายละเอียดสามข้อสังเกต

**F-1 -- สำมะโนใช้ทะเบียนฉากเก่าหลัง live warp.** `/warp 278 100 200` ทำให้คอนโซลพิมพ์
`WORLD_CENSUS ... scene=bg0001` (ฉากต้นทาง) แต่ anchor เป็นพิกัดปลายทาง และไม่มีบรรทัดสำมะโนของ
ฉาก 278 เลย ตรวจซอร์สยืนยัน (ไม่ใช่การเดา): `gm/chat_command_action.py::_warp_teleport_action`
docstring บอกตรง ๆ ว่า "No new call site in `runtime.py` was needed to land this" -- เส้นทาง GM
ไม่แตะ session state ของ runtime.py เลย ในขณะที่บล็อก `WORLD-CENSUS-001` (`runtime.py:7385`
เป็นต้นไป) อ่าน `self.foundation.selected.position.scene_id` เป็น scene ของสำมะโน ⇒ อยู่นอกเขต
เขียนของสายนี้ (`runtime.py` เป็นของ chief) เปิด `CORE-REQUEST-GM-045` แทนการแก้เอง

**F-2 -- ไม่มีจุดเกิดปลอดภัยที่ปลายทาง วาร์ปแล้วลอย/ติดโครงสร้าง.** `gm/warp_executor.py`'s
docstring จงใจไม่เดา z (`z` ต้องมาจาก caller) เพราะไม่มีข้อมูล ground/spawn ต่อฉากในเขต `gm/`
เลย -- ตรวจ `gm/scene_catalog.py` แล้วไม่มีฟิลด์ spawn และค้น `external/00_SEARCH_HERE_FIRST.md`
+ `gamedata/00_SEARCH_HERE_FIRST.md` ด้วยคำ "spawn"/"จุดเกิด"/"respawn" แล้ว **ไม่เจอ** (grep exit
1, ยืนยันจริงก่อนเขียนใบ) ⇒ นี่คือใบขอข้อมูลจาก chief (`CORE-REQUEST-GM-046`) ไม่ใช่ใบขอจุดเสียบ
โค้ด -- และตรงกับความต้องการ GM-A ที่เจ้าของเพิ่งสั่ง (ใบ `20260901_0215`) พอดี

**F-3 -- live warp ไม่ sync กับค่า stage สำหรับ relog.** ไม่ใช่บั๊ก (สองโมดูลออกแบบแยกกันโดยเจตนา
ตั้งแต่แรก) แต่ขัดสัญชาตญาณและเกี่ยวกับ GM-A โดยตรง จึงบันทึกเป็น FINDING ให้คนที่รับ GM-A อ่าน
ก่อนออกแบบ

## ที่ไม่ทำในรอบนี้ (เจตนา ไม่ใช่ลืม)

- **ไม่รับงาน GM-A/GM-B เอง** แม้ชื่อจะขึ้นต้นด้วย GM -- ใบ `20260901_0215_PANYA-ORDER-*` (มาถึง
  หลังรอบ `kv02mn`) ขอให้ chief เป็นคนประกาศมอบหมายสายให้ P-1/P-2/P-3/GM-A/GM-B/UI-A/UI-B
  ทีละสายชัดเจน ("หนึ่งเรื่องหนึ่งสาย") -- ตรวจ `FROM_CHIEF_R277` (ล่าสุด, 02:00, ก่อนใบ 0215
  ที่ 02:15) แล้ว **ยังไม่มีการประกาศมอบหมาย** รับงานเองตอนนี้จะเสี่ยงชนกับสายอื่นถ้า chief มอบ
  GM-A ให้สายอื่น -- ตามกฎ 🔴 เรื่องใบสั่งงานที่ยังไม่ระบุผู้ทำสายเดียว ต้องรอ chief มอบหมายหรือ
  ประกาศจองก่อน สายนี้ยังไม่จอง เพราะยังไม่เห็นสัญญาณว่าใครแย่งคิว
- ไม่แตะ `runtime.py`/`gm/login_scene_stage.py`/`gm/chat_command_action.py`/
  `gm/warp_executor.py` -- ไม่มีโค้ดที่ต้องแก้ในเขตเขียนของสายนี้รอบนี้ (สามข้อสังเกตทั้งหมดต้องการ
  ข้อมูล/จุดเสียบจาก chief ก่อน)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** (ยังไม่มี call site/ข้อมูลใหม่ให้ทดสอบ) แต่ **GT-172 ปิดเป็น PASS แล้วอย่างเป็นทางการ** ใน
คิว (เมื่อวานเป็น READY ยังไม่ยิง) และมีสามใบใหม่รอ chief ตอบซึ่งจะปลดล็อกงานถัดไปถ้าตอบเร็ว

## nonclaims

1. ไม่อ้างว่า F-1/F-2 คือบั๊กเดียวกับที่ addendum G มอบให้สาย B (`runtime.py:3828-3835`) -- คนละจุด
   ในไฟล์เดียวกัน อาการคล้ายกัน ตั้งข้อสังเกตให้ chief ตัดสินเอง
2. ไม่อ้างว่า GM-A/GM-B เป็นของสายนี้ -- รอ chief ประกาศ
3. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`gm_accounts.json`/
   `scenarios/world_*.json`/`scenarios/combat_*.json`
4. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json` ไม่ประกาศ milestone ใด ๆ (milestone พักอยู่แล้ว
   ตามใบ 0215 ข้อ 2)
5. ไม่ลบประวัติ/จดหมายเดิม -- สตับใหม่เท่านั้น ต้นฉบับสำเนาไว้ที่ `consumed/` ครบ
6. src/scenarios/tests ไม่มีการแก้รอบนี้ (เฉพาะจดหมาย/คิว/round notes/docs) -- ไม่เรียก pf-adversary
   ตามบรรทัดฐานรอบ `dgyakk`/`bmedw1`/`kv02mn`

## PR

`pf_bridge` และ `pirate-force-server` (เลขจะเติมหลังเปิด PR รอบนี้)

— สาย GM รอบ `k0w291`
