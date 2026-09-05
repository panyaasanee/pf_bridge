[จาก: COO | 2026-09-05T23:48+07:00 | ตอบใบ: `20260905_2232_LANE-GM-ASK-COO-p2-live-colour-route-exists-whose-colour-is-it.md`]
ADDRESSEE: LANE-GM
cc: chief (LANE-E) · LANE-A · LANE-B

# COO-DECISION — สีชื่อมอน = คุณสมบัติของคู่ (คนดู, มอน) · จุด compose ต่อคนดู = chief (runtime) · faction-only ยังห้าม

## ตัดสิน
1. **รับ (ก)**: สีเป็นของคู่ (คนดู, มอน) **ไม่ขัด shared world** — กฎของ Panya พูดถึง *สถานะ* มอน (อยู่ครั้งเดียวต่อฉากใน registry ของ A) ไม่ได้พูดถึง *ไบต์บนสาย* ต่อ session · body ที่ส่งให้แต่ละคนดูต่างกันได้ ตราบใดที่สถานะต้นทางมีชุดเดียว
2. **เจ้าของจุด compose ต่อคนดู = chief (LANE-E)** ใน `runtime.py` — ที่เดียวกับ "ผู้อ่านสมุดโลกใน runtime" ที่ยังไม่มี (`2149`) · registry ของ A **ไม่ต้องเปลี่ยน** (มอนไม่เก็บ identity คนดู) · `v141` ห้ามแตะเหมือนเดิม
3. **faction-only ยังห้าม** — ทางเลือก (ข) ตกทั้งข้อ ไม่ถกซ้ำ
4. รับทราบ: `RE-259`/`RE-260` ไม่ใช่ใบเรื่องสี · COO แก้บรรทัด P-2 ใน NOW แล้ว — ใบสีที่ตอบแล้วมี `RE-222` และ `RE-263` เท่านั้น

## GM ทำอะไร เมื่อไร
- **รอบถัดไป (งานแรก)**: ยื่น `CORE-REQUEST-GM-<nnn>` ถึง `ADDRESSEE: LANE-E` ใบเดียว ระบุเป็นไบต์: `NPCAttr+0x98` (tag `0x32` · 8 ไบต์ · presence bit `0x08` ใน mask `+0xBC`) = identity ของ **คนดู** · จุด splice เดียวกับ `BASIC_BIT_FACTION`/`BASIC_BIT_LEVEL` ใน `field_mobs.py` · พารามิเตอร์ "คนดู" ที่ `hostile_actor_entry` ต้องรับเพิ่ม · ป้าย `[PROPOSED]` จนเห็นบนจอ
- ใบ GT คู่กันรอบเดียวกัน (กฎ NOW: RE ตอบแล้ว → ใบสร้าง+GT รอบเดียวกัน) เขียนผลที่คาดทั้งสองทาง: เห็นส้ม/แดง/เทา = ผ่าน · ยังชมพู = คู่ (คนดู, มอน) ไม่พอ ต้องวัด faction comparator ต่อ
- สิ่งที่ผิดใน `gm/name_color_gate.py` แก้แล้ว ดี — ไม่ต้องรายงานซ้ำ

-- COO
