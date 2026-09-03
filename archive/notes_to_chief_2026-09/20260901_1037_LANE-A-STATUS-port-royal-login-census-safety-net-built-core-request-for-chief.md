[ถึง: chief | ADDRESSEE: CHIEF | cc: COO, เจ้าของ | จาก: LANE-A รอบ `yv3k9x` · 2026-09-01T10:37+07:00]

# LANE-A STATUS -- Port Royal login census: safety net built, runtime.py CORE-REQUEST attached

## บริบท

`PANYA-ORDER 20260901_0955` (`pf_bridge/notes_to_chief/20260901_0955_PANYA-ORDER-login-
path-must-ship-the-census-eagerly-like-the-warp-path-now-does.md`): "ตอนเข้าเกมมา port
royal ยังไม่เจอ npc ใดๆ เพราะไม่เดิน ทำไมไม่ทำอันนี้ด้วยล่ะ เว้นไว้ทำไม" -- login ไม่ส่งสำมะโน
Port Royal จนกว่าผู้เล่นจะขยับ (ต่างจากเส้นทางวาร์ปที่ส่งทันทีตอน `after_teleport`) จองหัวข้อไว้
แล้วที่ `20260901_1037_CLAIM-LANE-A-*` (ไม่มีสายไหนจองก่อน ไม่มีจดหมายมอบหมายจาก chief ก่อนต้น
รอบนี้ 10:24)

## ทำไมงานนี้ต้องแบ่งเป็นสองครึ่ง

วัดจากคอมเมนต์ที่มีอยู่แล้วใน `runtime.py` เอง (ไม่ใช่การเดาของสายนี้): เงื่อนไข trigger ของ
สำมะโน scene 1 (`runtime.py:7578-7582`) ต้องมี `self.last_target_pos is not None` เพราะ
`self.population_indices` ถูกตั้งแบบไม่มีเงื่อนไข (`runtime.py:8266`) และ dispatcher เดิม
(`current/pf_login_game_server_v141.py:4395-4416`) unpack `self.last_target_pos` โดยไม่
เช็ค `None` เลย -- ถ้าคลิก NPC ก่อนเดินก้าวแรก จะ `TypeError` กลาง listener thread (ไม่มี
`except` ที่ v141:7440) = การเชื่อมต่อหลุด ไม่ใช่แค่ช้า **นี่คือ MEASURED crash ที่คอมเมนต์เดิม
ของ runtime.py เองระบุไว้แล้ว ไม่ใช่สมมติของสายนี้**

ครึ่งที่ 1 (ทำแล้วรอบนี้ อยู่ในเขต LANE-A ทั้งหมด): responder ที่ตอบคลิก NPC ของ scene 1 แทน
dispatcher เดิม (กลไกเดียวกับที่ scene 14 ใช้อยู่แล้ว -- guard ของ `runtime.py:7088-7160`
เป็น scene-agnostic อยู่แล้ว ไม่ต้องแก้ runtime.py เพิ่มเพื่อให้คลุม scene ใหม่) เมื่อไม่รู้ตำแหน่ง
ผู้เล่น (`last_target_pos is None`) responder หันหน้า NPC ไปทิศทางเดียวกับที่สำมะโนตอน arrival
กำหนดไว้แล้ว (`world_population.HEADINGS`) แทนที่จะเดาทิศไปหาผู้เล่น -- ไม่มีอะไรถูก invent
ไฟล์: `src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene1.py` (ใหม่, 232 บรรทัด)
`tests/test_lane_a_choose_npc_scene1.py` (ใหม่, 15 เทส, เขียวหมด)

**`production_allowed = False` ในรอบนี้โดยตั้งใจ** -- สองเหตุผลอิสระกัน (ดู docstring ของไฟล์
เต็ม ๆ ที่หัวข้อ "WHY THE GATE STAYS CLOSED THIS ROUND"): (1) วันนี้ trigger ยังไม่กว้างพอให้
`population_indices` ถูกตั้งก่อนเดิน ⇒ ยังไม่มี crash ให้ป้องกัน (2) เปิดแล้ว responder นี้จะ
ตอบ**ทุก**คลิกของ scene 1 แทน dispatcher เดิม รวมถึงคลิกหลังเดินที่ dispatcher เดิมตอบถูกอยู่แล้ว
วันนี้ -- สลับ path ที่ใช้งานจริงมานานโดยไม่มี pf-adversary รีวิว (เครื่องมือ subagent ไม่มีให้
เรียกในเซสชันนี้ เหมือนที่ LANE-GM รายงานไว้ที่ `20260901_1018_LANE-GM-STATUS-*`) ในรอบเดียว
กับที่เขียนโค้ดถือว่าเสี่ยงเกิน จะขอปลด flag เองในรอบถัดไปหลังมี adversary หรือ attended click
parity อย่างน้อยหนึ่งครั้ง

## CORE-REQUEST -- runtime.py (บรรทัดเดียวตามกฎ)

**กว้างเงื่อนไขที่ `runtime.py:7578-7582`: ตัด `self.last_target_pos is not None or` ออก
สำหรับ scene 1 เหมือนที่ทุก scene อื่นทำอยู่แล้ว (เงื่อนไขเหลือแค่ตรวจว่า arm แล้วหรือยัง ไม่ต้อง
รอ `last_target_pos`) -- แต่ 🔴 ห้ามทำ CORE-REQUEST นี้จนกว่าจะเห็นจดหมาย LANE-A ยืนยันว่า
`lane_a_choose_npc_scene1.production_allowed` เป็น `True` บน `main` แล้ว -- ถ้าเดินสาย
runtime.py นี้ก่อน จะเปิด crash เดิมที่ responder ตัวนี้ตั้งใจปิดกลับมาใหม่ทันที (population_indices
จะถูกตั้งก่อนเดิน ในขณะที่ dispatcher เดิมยังเป็นคนตอบคลิกอยู่)**

## เปิดใบให้สาย C

ไม่มี -- ข้อมูลที่ต้องรู้ (ตำแหน่ง trigger, กลไก crash) วัดจากซอร์สที่มีอยู่แล้วครบ ไม่ต้องพึ่ง
ไบนารีไคลเอนต์เพิ่ม

## ยังไม่ได้พิสูจน์

Attended click parity ระหว่าง responder ใหม่กับ dispatcher เดิมสำหรับคลิกหลังเดิน (ยังไม่มี
ใครลองคลิก NPC ใน Port Royal ผ่าน responder ใหม่บนจอจริง) -- นี่คือเหตุผลข้อ (2) ที่ flag ยังปิด

-- LANE-A (WORLD) รอบ `yv3k9x`
