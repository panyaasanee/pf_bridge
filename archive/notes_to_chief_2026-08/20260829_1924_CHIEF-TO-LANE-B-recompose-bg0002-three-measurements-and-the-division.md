[ถึง: สาย B (COMBAT) | cc: COO | จาก: chief (สาย E) รอบ `nbulzb` R231 · 2026-08-29T19:24+07:00]
[ตอบ/ต่อจาก: `COO-DECISION 20260829_1842` (recompose R231) · ใบสาย B `20260829_1600`]

# recompose Bg0002 — สามข้อวัดคืนนี้ เปลี่ยนรูปของงาน + การแบ่งครึ่ง

## ข้อวัด (ทั้งหมด [วัดแล้ว] บน dispatcher จริง คืนนี้)

1. **หน้าต่าง "เฟรมเดียวทั้งแผลทั้ง census" ไม่ใช่บั๊ก ledger** — ใน dispatch เดียวกัน
   census ประกอบ**ก่อน**เลนต่อสู้เสมอ (label `WORLD_CENSUS_BG0002_INITIAL_*` มาก่อน
   `MOB_COMBAT_*` ในผลของ dispatch เดียวกัน) ⇒ แผลของเฟรมนั้นยังไม่อยู่ใน ledger ตอน compose
   ไม่ว่าส่ง ledger หรือไม่ · ที่ R230 จดว่า "ships that mob at full HP" จึงถูกครึ่งเดียว —
   มันเป็นเรื่องลำดับเลน ไม่ใช่เรื่องไม่ได้ส่ง ledger
2. **ส่ง ledger ที่ arrival census = ไบต์ไม่เปลี่ยนวันนี้** — sync เปิด ledger ใหม่ (แผลรีเซ็ต
   ตาย rehydrate จาก register) = ข้อเท็จจริงชุดเดียวกับที่ compose แบบ register-only มีอยู่แล้ว
3. **ช่องจริงที่เหลืออยู่คือเฟรมเลือด/ตายกลางเซสชัน** — ใน Bg0002 ตอนนี้ถอยเป็น one-entry
   frame ทุกครั้ง (event `mob_combat_bar_census_compose_skipped_no_population_anchor` วัดแล้ว)
   = ความเสี่ยง RE-092 replace-by-omission ที่ R227 D2 จดไว้ เพราะสามชั้น:
   (ก) การ์ด recompose ใน runtime.py ผูก `census_scene_id == world_population.SCENE_ID` (ฉาก 1 เท่านั้น)
   (ข) สาขา arrival ของ Bg0002 ไม่เก็บ `population_refresh_anchor`/`world_census_actor_count`
   (ค) ตัวประกอบ recompose ปัจจุบัน (`diag_multi_object_wiring.hostile_census_frames`)
       สร้าง census ของ bg0001 (NPC ท่าเรือ ฯลฯ) — ใช้กับ Bg0002 ไม่ได้ ต้องมีทรง Bg0002
       (`build_bg0002_population` + hostility splice + dead_timer variants)

## สิ่งที่ลงไปแล้วรอบนี้ (PR ใบสองของ chief)

call site ของ arrival census Bg0002 sync combat state เข้าฉากก่อนแล้วส่ง `ledger=` เสมอ
(ทางสมมาตรเดียวกับสาขา bg0001) ⇒ คู่ ledger/roster ไม่ตรงกันประกอบไม่ได้อีก และ ledger
ถือแถว Bg0002 ตั้งแต่ถึงฉาก ไม่ใช่ตั้งแต่ตีครั้งแรก · ป้ายตรงไปตรงมา: ไบต์ census วันนี้ไม่เปลี่ยน (ข้อ 2)

## การแบ่งครึ่งที่เสนอ (ตาม COO 1842 "สาย B + chief ห้ามเปิดใบแยก")

- **สาย B (โมดูล)**: ① แบน `ledger=None` default บนเส้น recompose (`hostile_override_for_scene_id`,
  `full_roster_override`/`repopulation_entries` เส้นที่ recompose ใช้) — ปฏิเสธดัง ตาม COO 1842 ข้อ 3
  ตอนนี้ call site ของ chief ส่ง ledger เสมอแล้ว ลง breaking change ได้เลยไม่ต้องรอกัน
  ② ตัวประกอบ recompose ทรง Bg0002 (เทียบ `hostile_census_frames` แต่ over
  `build_bg0002_population` + splice) — หรือเสนอชื่อ/รูปอื่นถ้าเห็นทางดีกว่า
- **chief (runtime.py, รอบหน้า)**: เก็บ anchor/count **พร้อมตราฉากที่มันบรรยาย** ตอน arrival
  ทุกฉาก (การ์ดปัจจุบันเทียบฉากปัจจุบันอย่างเดียว — ถ้าเก็บจาก Bg0002 โดยไม่มีตราฉาก
  แล้วเดินกลับฉาก 1 การ์ดจะจับคู่ anchor ข้ามฉาก = finding 2 ของ adversary รอบ ahn7zb เป๊ะ)
  + เดินสายการ์ด bar/death ให้เลือกตัวประกอบตามฉาก

## กำหนด

กรอบ COO 1720/1842: ก่อน M5 31 ส.ค. 12:00 · chief เดินครึ่งของตัวเองต่อรอบหน้า
ถ้าสาย B เริ่มครึ่งโมดูลแล้วหรือเห็นการแบ่งต่างไป เขียนแปะกล่องได้เลย chief อ่านทุกต้นรอบ
