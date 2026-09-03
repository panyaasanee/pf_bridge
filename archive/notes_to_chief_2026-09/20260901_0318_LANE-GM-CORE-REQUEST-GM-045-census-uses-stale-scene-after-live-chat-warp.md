[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: สาย GM รอบ `k0w291` · 2026-09-01T03:18+07:00]

# CORE-REQUEST-GM-045 -- WORLD-CENSUS-001 ยิงด้วยทะเบียนฉากเก่าหลัง live warp ของสาย GM

## ที่มา

`pf_bridge/notes_to_chief/20260901_0225_GT172-RESULT-*.md` (ADDRESSEE: LANE-GM, ผู้เทส attended)
ระบุ finding F-1 ว่า `/warp 278 100 200` (แชท, `gm/chat_command_action.py::_warp_teleport_action`)
ทำให้ไคลเอนต์เห็นฉาก 278 จริง แต่คอนโซลพิมพ์:

```
WORLD_CENSUS ... scene=bg0001 ... anchor=(111.044, 216.844, 186.000)
[G>] WORLD_CENSUS_INITIAL_108  (20112 bytes)
[G>] WORLD_CENSUS_REAPPLY_108  (20112 bytes)
```

ทะเบียนเป็นของ bg0001 (Port Royal) แต่ actor 108 ตัวถูกวางรอบพิกัดปลายทางในฉาก 278 -- และไม่มี
บรรทัดสำมะโนของฉาก 278 เลยสักบรรทัด (grep = 0) ยิง 4 ครั้งในรอบ ผลเหมือนกันทุกครั้ง

## โมดูล / ฟังก์ชันที่เกี่ยว

- สาย GM: `gm/chat_command_action.py::_warp_teleport_action` เรียก
  `gm/warp_executor.make_warp_teleport_frame_with_target` แล้วคืนเฟรมให้ dispatch ทั่วไปส่ง --
  โมดูลนี้ (และ `warp_executor.py`) **ไม่แตะ session state ของ runtime.py เลย** ตามที่ docstring
  ของ `_warp_teleport_action` เขียนไว้เอง: *"NO SEND MECHANISM IS NEW HERE ... No new call site in
  `runtime.py` was needed to land this (checked before writing this function: chief's zone was not
  touched)"* -- นี่คือหลักฐานในซอร์ส ไม่ใช่การเดา
- ฝั่ง runtime.py: บล็อก `WORLD-CENSUS-001` (คอมเมนต์ `runtime.py:7385` เป็นต้นไป) อ่าน
  `self.foundation.selected.position.scene_id` (`runtime.py:7420`) เป็น `scene_id` ของสำมะโน และ
  `self.last_target_pos` เป็น anchor -- ทั้งสองตัวเป็น session state ที่สาย GM เรียกไม่ถึง

## สมมติฐาน (ยังไม่ยืนยัน ขอให้ chief ยืนยันหรือหักล้าง)

`self.foundation.selected.position.scene_id` และ `self.last_target_pos` ไม่ถูกอัปเดตเมื่อสาย GM
ส่ง `TeleportVital` แบบ live เพราะเส้นทางนี้จงใจไม่แตะ runtime.py (ตามหลักฐาน docstring ข้างบน) --
สำมะโนที่ยิงในเฟรมถัดไปจึงยังอ่าน scene_id เดิม (bg0001) ในขณะที่ anchor/พิกัดที่ log แสดงมาจากค่าที่
ผู้เล่นขยับหลังวาร์ป (ผ่าน `TargetPosVital` ต่อมา) ไม่ใช่จาก scene_id ที่วาร์ปไป -- ตรงข้ามกับเส้นทาง
`departure.confirmed_fields()`/`_dispatch_columbus_quest3021` ที่ chief เขียนเอง ซึ่งอัปเดต
checkpoint/census ให้สอดคล้องกันก่อนส่งเฟรม (ดู `runtime.py:7236-7384`)

## ตรงไหนของ runtime (login / dispatch vital id)

ระหว่าง dispatch ทั่วไปของ `GSCN_RunTimeProtocolReq` (บล็อกเดียวกับที่ `WORLD-CENSUS-001` อยู่,
`runtime.py:7405-7420`) -- ไม่ใช่ login path

## ขอจาก chief

1. ยืนยันว่า `self.foundation.selected.position` (และ `last_target_pos` ถ้าเกี่ยว) จริง ๆ ไม่ถูกอัปเดต
   เมื่อเฟรมที่ dispatch ทั่วไปส่งออกเป็น `TeleportVital` จากสาย GM (ต่างจากเส้นทาง checkpoint ของ
   world-travel-gate) -- ยิงจริงหนึ่งครั้งแล้วรายงานค่า ไม่อ่านโค้ดอย่างเดียว
2. ถ้าใช่จริง ขอ call site หนึ่งจุด (ที่ไหนก็ได้ที่ chief เห็นว่าถูกต้องใน `runtime.py`) ที่อัปเดต
   `position.scene_id` (และ/หรือ `last_target_pos`) ให้ตรงกับ target ที่ `_warp_teleport_action` คืนมา
   ก่อนสำมะโนถัดไปจะยิง -- สาย GM พร้อมส่ง `WarpTarget` (มี `scene_id`, `x`, `y`, `z` อยู่แล้ว,
   `gm/warp_executor.py`) ให้ runtime.py ใช้ได้ทันทีถ้ามีจุดเสียบ
3. ถ้า chief เห็นว่าไม่ใช่บั๊กที่ควรแก้ตอนนี้ (เช่นเพราะ F-1 เป็นบั๊กพี่น้องของ `GT-148` ที่สาย B
   กำลังแก้อยู่ตาม addendum G) ขอคำตอบสั้น ๆ ว่า "รอสาย B" หรือ "แก้แยก" เพื่อไม่ให้สองสายชนกัน

## เทสที่พิสูจน์

`/warp <ฉาก> x y` แบบ live หนึ่งครั้ง -> เฟรม `RuntimeReq` ถัดไปที่ทำให้สำมะโนยิง -> คอนโซลต้องพิมพ์
`WORLD_CENSUS ... scene=<ฉากปลายทาง>` (ไม่ใช่ฉากต้นทาง) และต้องมี actor ของฉากปลายทางจริง (ไม่ใช่ของ
ฉากต้นทางที่ลากพิกัดปลายทางมาใช้) -- เทียบกับ evidence_video ของ GT-172
(`evidence_video/1400_gt172_FULLROUND_20260901_011801.mkv`) เป็นเส้นฐาน negative

## nonclaims

1. ไม่อ้างว่ารู้ค่าจริงของ `position.scene_id`/`last_target_pos` หลังวาร์ป -- ไม่มีทางอ่าน session
   state สดจากอิมเมจ clone นี้ (ไม่มี `gh`/หน้าจอ/DB) อาศัยหลักฐานคอนโซลจากใบ GT-172 เท่านั้น
2. ไม่อ้างว่า F-1 เหมือนกับบั๊กที่ addendum G มอบให้สาย B (`runtime.py:3828-3835`
   bar_frames/death_frames) ทุกประการ -- เป็นบั๊กคนละจุดในไฟล์เดียวกัน มีอาการคล้ายกัน
   ("สำมะโนประกอบหลังเฟรม จึงใช้ทะเบียนเก่า") จึงตั้งข้อสังเกตให้ chief ตัดสินว่าควรแก้พร้อมกันหรือแยก
3. ไม่แตะ `runtime.py` เอง -- อยู่นอกเขตเขียนของสายนี้ นี่คือใบขอ ไม่ใช่การแก้

ค้นแล้ว: ค้น `external/00_SEARCH_HERE_FIRST.md` และ `gamedata/00_SEARCH_HERE_FIRST.md` แล้ว --
ไม่เกี่ยว (นี่เป็นบั๊ก runtime session-state ไม่ใช่ข้อมูล client)

— สาย GM รอบ `k0w291`
