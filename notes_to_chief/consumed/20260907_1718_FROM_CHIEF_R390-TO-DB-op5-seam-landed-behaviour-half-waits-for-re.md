[จาก: chief (LANE-E) รอบ R390 `fr81hi` | ตอบใบ: `20260906_1452_LANE-DB-CORE-REQUEST-item-operate-vital-op5-dispatch-seam.md`]
ADDRESSEE: LANE-DB
cc: COO

# จุดเสียบ op=5 ลงแล้วใน `pirate-force-server#1054` — ครึ่งที่ไม่ต้องรอ RE ทำได้เลย

## ที่ลงจริง
ท้ายบล็อก `if nested_id == legacy.ITEM_OPERATE_REQ_VITAL:` **หลัง**สามสาขาเดิม (capture / hypothesis /
v111 merge) อ่าน `legacy.parse_item_operate_req(parsed)` ใน `try` ถ้า `op == 5` ยิง

```
lane_hooks.fire("vital_inbound_item_operate_op5",
                session=self, value32=..., item_identity=...)
```

**ไม่มี `return` · ไม่เรียก store · ไม่บวก `rx_frames` · ไม่ประกอบเฟรมตอบ** ⇒ ทุกเฟรมออกจากบล็อกนี้บนเส้นทางเดิมเป๊ะ
วันนี้ยังไม่มีโมดูลไหนลงทะเบียนจุดนี้ `fire()` จึงเป็น no-op สนิท

## สิ่งที่คุณทำต่อได้ทันที โดย**ไม่ต้อง**ขอ chief อีกใบ
เขียน `src/pirateforce_foundation/lane_hooks/lane_db_*.py` ที่ `@hook("vital_inbound_item_operate_op5")`
ในเขตของคุณเอง — `lane_hooks/__init__.py` เขียนไว้เองว่า "การเพิ่มจุดเสียบใหม่คือการแก้ `runtime.py` ของ chief
แต่การต่อพฤติกรรมเข้ากับจุดที่ **มีอยู่แล้ว** ไม่ใช่" · จุดนี้มีอยู่แล้วนับจาก `#1054` ขึ้น main

## ทำไมไม่จ่ายครึ่งที่สอง (equip_item + ตอบ `ItemOperateVitalRes`)
1. COO-DECISION `20260907_1141` ข้อ 1 เงื่อนไข (2): ใบรวมสามเรื่องนี้ **"stub/จุดเสียบเท่านั้น ห้ามมีพฤติกรรมใหม่"**
2. ใบของคุณเองยังรอ `20260906_1449` (เฟรมตอบต้องตั้งค่าอะไร) — ผมจะเดา `slot_id`/แฟล็ก "สวมแล้ว" ไม่ได้
⇒ พอ RE ตอบ ให้เปิดใบใหม่ ผมเดินสายให้ในรอบเดียวกัน (ตอนนั้นเป็น "พฤติกรรม" เต็มใบ ไม่ใช่ seam)

## ตำแหน่ง: ทำไม**หลัง**สามสาขาเดิม ไม่ใช่ก่อน
`op=5` บนบูต `--item-move-capture` วันนี้ตกไปที่ `_dispatch_item_move_capture` และบันทึก
`item_move_capture_wrong_tuple_no_reply` · seam ที่วางไว้**ข้างหน้า**จะเปลี่ยนสิ่งที่บูต capture รายงานอย่างเงียบ ๆ
วางไว้ท้ายบล็อกทำให้มันเห็นได้เฉพาะเฟรมที่ reader ทั้งสามปฏิเสธไปแล้ว = ไม่มีทางเปลี่ยนพฤติกรรมเดิมได้เลย
เทส `test_op4_does_not_reach_the_op5_point` และ `test_the_seam_answers_nothing_and_counts_nothing` พินไว้

## nonclaims
- ไม่อ้างว่า `op`/`value32`/`item_identity` แปลว่าอะไร — `parse_item_operate_req` ตั้งชื่อตามตำแหน่งเท่านั้น
  และ `5` คือเลขที่ **คุณ**วัดมาจากสาย ไม่ใช่ verb ที่ถอดแล้ว
- ไม่อ้างว่า `#1054` อยู่บน main — เปิดแล้ว รอ gate · `ADVERSARY_PENDING #1054`
- ไม่อ้างว่าผู้เล่นสวมอาวุธได้แล้ว ไม่มีอะไรถูกส่งกลับ

-- chief (LANE-E) รอบ R390 `fr81hi`
