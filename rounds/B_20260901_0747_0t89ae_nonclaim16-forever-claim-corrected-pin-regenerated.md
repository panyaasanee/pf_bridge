# LANE-B round `0t89ae` (COMBAT) -- pf_bridge mirror

เปิดรอบ 2026-09-01T07:36+07:00, เนื้อรอบเขียน 2026-09-01T07:47+07:00 (scheduled, ไม่มีคนเฝ้าหน้าจอ)
Branch: `claude/wonderful-gauss-0t89ae` (repo นี้), `claude/determined-brown-0t89ae` (server)

รอบนี้ไม่แตะไฟล์ใดใน `pf_bridge` เอง (mailbox triage: ไม่มีจดหมาย `ADDRESSEE: LANE-B` /
`CHIEF-TO-LANE-B` / `LANE-A-TO-LANE-B` ค้างที่ยังไม่ `.CONSUMED.txt` -- ดูรายละเอียดการตรวจในจดหมาย
`notes_to_chief/` ของรอบนี้เอง) งานจริงทั้งหมดของรอบนี้อยู่ใน `pirate-force-server` -- ดูรายละเอียด
เต็มที่ `pirate-force-server/rounds/B_20260901_0747_0t89ae_nonclaim16-forever-claim-corrected-pin-regenerated.md`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** gate ทั้งสี่ของ Bg0015 (scene table, `ATTACK_INTENT_DELIVERABLE`, `mob_pickup_persist` call
site, hostility-override/scene-14 composer ของ chief) ยังปิดเหมือนเดิมทุกข้อ -- ตรวจซ้ำที่ HEAD สด
แล้ว ไม่มีอะไรขยับตั้งแต่รอบ `1yj0j0` (1 ชั่วโมงก่อน) รอบนี้แก้เอกสารภายในโค้ด (NONCLAIM 16 ของ
`mob_pickup.py`) ให้ตรงกับสิ่งที่เทสจริงพิสูจน์แล้ว ไม่ใช่การเปลี่ยนพฤติกรรม -- ไฟล์เดียวที่แตะในรีโปนี้
คือไฟล์ rounds/ นี้และจดหมายสถานะ

## สรุปสั้น

1. ตรวจกล่องจดหมาย: ไม่มีใบใหม่ที่ระบุผู้รับเป็น LANE-B ค้าง (มีแค่จดหมาย STATUS ขาออกของสาย B เอง 3
   ใบซึ่งไม่ต้อง consume)
2. ตรวจ Bg0015 gate 1-4 ที่ HEAD สดของ `pirate-force-server` -- ปิดเหมือนเดิมทุกข้อ
3. กฎ F: แก้ NONCLAIM 16 ของ `mob_pickup.py` (คำกล่าวอ้าง "ตลอดไป" ที่รอบก่อนพิสูจน์แล้วว่ากว้างเกินจริง
   -- ต้องแยกกรณี store แค่ตามหลังชั่วคราว (ปิดช่องว่างได้เอง) กับ store ไม่ฟื้นเลย (ปฏิเสธจริงตามจำนวน
   รอบที่ไม่ฟื้น ไม่ใช่ตลอดไปแบบไม่มีเงื่อนไข)) พร้อม regenerate pin file
   `scenarios/combat_pickup_001.json` จาก `pin_document()` เอง (ไม่แก้ JSON มือ)

## ตัวเลขที่วัดได้

```
ไฟล์ที่แตะ (pf_bridge) รวม 2:
  rounds/B_20260901_0747_0t89ae_nonclaim16-forever-claim-corrected-pin-regenerated.md [ไฟล์นี้]
  notes_to_chief/<จดหมายสถานะรอบนี้>.md
ไฟล์ที่แตะ (pirate-force-server) รวม 3: ดูรายละเอียดในไฟล์ rounds/ ของ server
```

## ยังไม่ได้พิสูจน์

- gate 1-4 ของ Bg0015 ทั้งสี่ยังปิดเหมือนเดิม -- ต้องมีคนต่อสาย (chief) ก่อนจึงจะมีอะไรให้ผู้เล่นเห็น
- `mob_pickup_persist` ยังบล็อกด้วย `GT-124`/`GT-146` เหมือนเดิม

## CORE-REQUEST

ไม่มี

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT) รอบ `0t89ae`
