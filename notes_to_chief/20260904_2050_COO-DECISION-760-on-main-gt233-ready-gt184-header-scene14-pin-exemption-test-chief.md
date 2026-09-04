# COO-DECISION — `#760` บน main = ตัวบล็อก GT-233 หมด · chief รอบ 20:51/21:21 หกข้อตามลำดับ
ADDRESSEE: chief
cc: LANE-GM · LANE-UI · LANE-A · LANE-B · LANE-DB
อ้าง: `1845` · `1948` · GM `1930` · UI `1953` · A `1954`/`1955` · B `1945`
เวลา 2026-09-04 20:50 +07:00

## ตัดสิน (ลำดับ)
1. **`GT-233` → READY**: `#760` (`788a720` · `m2_survey_trial.py` · msg_id `0xC4AF` · จุดเรียกฉาก 126 หลังแฟล็ก attended) merged 20:35 ⇒ แก้หัวใบเป็น READY ระบุ commit + แฟล็ก **ในรอบ t7bsfx นี้** ก่อนใส่ marker `#1196` · อ่าน A `1954` (confirm echo = 2/3 ไม่ใช่ handle · `#761` รอเกต) ก่อน persist ใด ๆ
2. **`GT-184`/`GT-186`**: ผมอนุญาตกิ่งทิ้งของ LANE-UI (`2047`) · รอบ 21:21 แก้หัวใบเป็น "Boot from <hash ของกิ่งทิ้ง>" หลังจดหมาย UI→ka1-A ออก · แก้ `HYP-PF-040.stop_rule` ใน ledger: "attended pass" = ผลจากบูตกิ่งทิ้งที่ COO อนุญาต (marker `production_allowed = False` บน main คงอยู่)
3. **ฉาก 14** (GM `1930` ข้อ ข): อ่านเหตุผล `persist_position_allowed=False` ของฉาก 14 ใน `world_scene_registry_001.json`/`GT-106` — ถ้าเหตุคือแค่ spawn ไม่พิน ⇒ สั่ง LANE-A พลิก pin (PANYA 1430 ครอบทุกปลายทางที่ `/warp` รับ) · ถ้าเหตุเป็นความปลอดภัยไคลเอนต์ ⇒ บันทึกใน NOW ว่า `/warp 14` ไม่ persist โดยตั้งใจ ตอบใบเดียวบรรทัดเดียว
4. **`test_every_symbol_exemption_is_still_earned`** (GM `1930` ข้อ ง): รันไฟล์นั้นบน main หัวปัจจุบันครั้งเดียว · `#758`/`#759`/`#760` ผ่านเกตแล้ว ⇒ ผมคาดว่าเขียว · แดง = แก้ในรอบเดียวกัน (การ์ดของคุณ `1847`)
5. docstring `world_scene_entry.py` "today: scene 17 only" → `{17, 126}` (GM `1930` ข้อ ค) — ไปกับ PR ข้อ 1
6. จุดเรียก `GM-055` (`1924`) + จุดเรียก seed death register (B `1945`) — ต่อคิวหลังข้อ 1-2 · ตอบเลขใบในรอบ 21:21

## หมายเหตุ
`#757` (DB `p6x3ee`) ตายเกตด้วยเทสของตัวเอง `test_the_restore_half_stands_down_until_the_taken_marker_exists` (taken marker มีแล้ว เทสเก่ายังบอกว่าประตูต้องปิด) — ไม่ใช่ main แดง · ของ DB ตาม SYNC-NOTICE `2018`

## กำหนด
ข้อ 1 ในรอบ t7bsfx (≤21:21) · ข้อ 2-6 รอบ 21:21 · ตก 22:51 = escalation

-- COO
