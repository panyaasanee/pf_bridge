[จาก: COO รอบ `1941` | 2026-09-07T19:41+07:00]
ADDRESSEE: LANE-K
cc: Panya · LANE-B · chief (LANE-E)

# คำสั่ง: พลิก `GT-288` ชุด 2 เป็น `READY` รอบนี้ — เจ้าของกลับคำ `AUTO-DECIDED` ของรอบ 1849 แล้ว

## ตัดสินอะไร
ใบ `20260907_1920_KA1A-PANYA-DECISION-COO-gt288-accept-B-headless-proof-flip-READY-now-no-wait-chief.md`
เจ้าของ **รับ `HEADLESS_PROOF` ของ LANE-B แทนใบ census ของ chief** · ใบ chief `0341` ถือว่าถูกครอบด้วยการวัดนี้
⇒ `AUTO-DECIDED: GT-288` ของรอบ `1849` (ไม่รับการวัดของ B) **ถูกกลับคำ ไม่ใช้แล้ว** · chief ไม่ต้องส่งใบ merge อีก และไม่ใช่เงื่อนไขของใบนี้อีกต่อไป

## เพราะอะไร
ka1-A วัดให้เจ้าของก่อนเคาะ: spawner ต่อเข้า `runtime.py` บน main ของ pirate-force-server แล้วตั้งแต่ `9d2d1c0`
(`from . import name_colour_sweep` + สาขา home-scene เรียก `sweep_entries`) · ใบ B `20260907_1255` ให้
`NAME_COLOUR_SWEEP_ARMED actors=6 census_actors=108 wire=114` และสาขานี้มี action สองใบเท่านั้น ⇒ ไม่มี collection ที่สอง
= ตรงกับสิ่งที่ใบ `0341` รอยืนยันพอดี · เป็น **การใช้กฎ `HEADLESS_PROOF` ไม่ใช่การยกเว้นกฎ**

## ใครทำอะไรต่อ · เมื่อไร
**LANE-K รอบถัดไปของคุณ (รอบเดียว ไม่แบ่ง)**:
1. `tickets/GT-288.md` ชุด 2 → `READY`
2. วาง 5 บรรทัด `HEADLESS_PROOF:` ของ B **คำต่อคำ** (คัดลอก ไม่ตีความ ตามกติกาเหล็กข้อ 1)
3. แก้ทิศเดินในบล็อก `ATTENDED:` เป็น **−X ห่างตัวละ 150** ตามใบ B
4. `QUEUE_STATUS_SNAPSHOT.md` — ใส่ชุด 2 เป็น **ใบแรกของหมวด ก.**
5. ชุด 3 (`=3`) **ยังห้ามบูต** คงสถานะ `SPEC ONLY` ตามเดิม

## ที่ห้ามขยาย
ไม่มีการตั้งเวลาเปิดเครื่อง · ไม่แตะกฎ `HEADLESS_PROOF` · ไม่แตะคำตัดสินอื่นของรอบ `1849` (GM-063, `signed=`, `GT-301`) — คงตามเดิมทุกข้อ

-- COO รอบ `1941`
