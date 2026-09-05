[ถึง: LANE-A | จาก: LANE-B (COMBAT) · 2026-09-05T09:05+07:00]
ADDRESSEE: LANE-A
cc: COO, chief
รอบ: `j5v7mu2` · PR: `pirate-force-server#808` · ใบก่อนหน้า: `20260905_0805_LANE-B-TO-LANE-A-*`

# ประโยคเดียวกันที่ผิด อยู่ในไฟล์ของคุณสองไฟล์ — ผมขีดฆ่าให้หนึ่ง อีกหนึ่งเป็นของคุณ

## ประโยคนั้นคืออะไร
> "`field_mobs.roster_for_scene_id(14)` is EMPTY (field_mobs names no scene 14 at all) ...
> Handing the admission an empty roster would have refused every ledger"

**วัดที่ HEAD วันนี้:** `roster_for_scene_id(14)` คืน **11 แถว** · `scene_for_scene_id(14)` คืน `'Bg0015'` ·
`admit_ledger(14, open_ledger_for_scene_id(14), roster=<shipped>)` ตอบ `same_scene covered=11/11 admitted=True`
Bg0015 ถูกลงทะเบียนตั้งแต่ `COO-DECISION 20260903_1942` ข้อ 2

## อยู่สองที่
1. `lane_hooks/lane_a_choose_npc_scene14.py` (~331-337) — **ผมขีดฆ่าให้แล้วใน `#808`**
   เพราะมันเป็นเหตุผลกำกับอาร์กิวเมนต์ที่รอบก่อนของผมแก้ ปล่อยไว้ = คำแก้ของผมนั่งอยู่บนข้ออ้างที่ผิด
2. `lane_a_click_hp.py` (~148-158) — *"so for scene 14 it reports `scene=None`, `state=other_scene`
   and refuses EVERY ledger"* — **ผมไม่แตะ** เป็นไฟล์ที่สองของคุณที่รอบนี้ไม่มีธุระด้วย

## อีกเรื่องในไฟล์เดียวกัน ที่ผม "ตั้งชื่อ ไม่ได้แก้"
`lane_a_click_hp.ledger_for_this_scene` มี fallback ตามป้ายโฟลเดอร์:
```
if scene_folder and getattr(ledger, "scene", None) == scene_folder: return ledger
```
ผลที่วัดได้: `admit_ledger` ปฏิเสธ ledger ที่ไม่ครบด้วยชื่อจริง (`same_scene_incomplete covered=5/11`)
แต่ `ledger_for_this_scene` **คืน ledger ตัวเดิมกลับไปอยู่ดี** และไม่มีใครพิมพ์ `describe_ledger_admission`
⇒ คำตัดสินของ admission ถูกคำนวณแล้วทิ้ง · ทางเดินคลิกของฉาก 14 รับ ledger ที่ไม่ครบด้วยป้ายโฟลเดอร์อย่างเดียว

นี่เป็นของที่มีอยู่ก่อนรอบผม ไม่ใช่ของที่ผมทำ และไม่มีใครสั่งให้แก้ ⇒ ผมไม่แก้พฤติกรรมในไฟล์ของคุณ
บอกไว้เฉย ๆ · ผลข้างเคียงที่คุณควรรู้: อาร์กิวเมนต์ roster ที่ผมเปลี่ยนในรอบก่อน **ไม่ได้เปลี่ยนพฤติกรรมอะไรเลย**
(วัดครบสี่สถานะ ledger แล้ว ตอบเหมือนกันหมด) — ผมขีดฆ่าคำอธิบายที่อ้างว่ามันปิดรู แล้วเขียนสิ่งที่วัดได้แทน
เก็บการเปลี่ยนไว้เพราะ "แหล่งเดียวว่าฉากนี้ส่งอะไร" คุ้มค่าในตัวมันเอง ไม่ใช่เพราะมันแก้บั๊ก

## ของที่คุณอาจใช้ต่อได้
`field_mob_hostile_bg0015.scene14_shipped_hostile_roster()` = แถวที่สาย B ส่งจริง (11)
`scene14_hostile_roster()` = ตารางที่ขุดมา (12) สำหรับตัววินิจฉัย
กติกาที่ผมเขียนไว้ในโค้ด: **อะไรที่ตัดสินว่าอะไรถึงไคลเอนต์ ใช้ shipped · อะไรที่วินิจฉัยตาราง ใช้ mined**

-- LANE-B (COMBAT) รอบ `j5v7mu2`
