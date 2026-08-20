# FINDINGS R40 — payload 248B ของ `GetWorldInfoVital` (0x3D4B) parse ครบทุกไบต์ (headless, read-only)

รอบ 40 (scheduled, 2026-08-17 18:18–18:3x) · งานตาม next ของ LOCK รอบ 39 (ทางเลือก optional
เพราะ HYP-PF-012 ยังไม่ถูกเคาะ) · ไม่แตะ src · ไม่เปิดเกม · ไม่ request_access · corpus read-only

## Claim เดียวของ finding นี้ (เกรด B)

**payload 248B ของ `GetWorldInfoVital` (client→server) parse ได้ครบ 248/248 ไบต์ภายใต้
tag grammar ของ v141 โดยไม่มี tag แปลกปลอมเลย** — โครงคือ vital collection 3 record:
record เต็ม 123B ที่ **byte-identical กันเอง 2 ชุดติดกัน** + record ว่าง (`0B 00`) ปิดท้าย ·
skeleton คงที่ทุกไบต์ข้ามเซสชัน มีเพียง **float32 สี่ค่า** ที่เปลี่ยนต่อเซสชัน
(ค่าแชร์ A ซ้ำ 3 ตำแหน่ง + ค่าเรียงลง B1>B2>B3) และภายในเซสชันเดียวกัน payload
**เหมือนกันทุกไบต์ทุกครั้งที่ยิง**

## แหล่งข้อมูล (ทั้งหมดที่มีใน corpus)

สแกน structural id `15691` ทั้ง 181 ไฟล์ที่มี STRUCTURAL_IDS annotation → พบใน **3 เซสชันเท่านั้น**:

| เซสชัน | ครั้ง | รูปแบบ | หมายเหตุ |
|---|---|---|---|
| `capture_v141` (2026-08-15 08:01:39) | 1 | **ว่าง 2B** `0B00` (count=1) | กลางเกมเพลย์ ไม่มี LogoutVital ตาม |
| `capture_item_move_hyp001` (00:38:10–24) | 3 | เต็ม 248B (count=3) | ทุกครั้งตามด้วย `0x1B40` ใน 2–6 วิ |
| `capture_gt002` (16:44–16:52) | 4 | เต็ม 248B (count=3) | ทุกครั้งตามด้วย `0x1B40` ใน 4–14 วิ |

→ **correlation 7/7**: รูปแบบเต็มยิงตอนเปิด dialog system-settings/logout (สอดคล้อง handler
strings ใน R38) แล้วตามด้วย `LogoutVital` เสมอ · รูปแบบว่างยิงกลางเกมเพลย์ได้โดยไม่เกี่ยว logout

## วิธี (ทำซ้ำได้ทุกขั้น)

1. payload hex จาก `GAME_EVENTS_LIVE.txt` ของ 3 เซสชัน (7 เต็ม + 1 ว่าง)
2. **oracle อิสระ**: parse raw `GAME_20260817_164015_*.txt` frame #187 ด้วย
   `pf_bridge\replay\pf_capture_frames.py` → container 268B = envelope 20B + payload 248B
   ตรงกับ events logger เป๊ะ · envelope decode ได้เอง: `u16 28271 (GSCN_RunTimeProtocolReq) ·
   u32 0 · u8 0 · u8 2 (mask) · u16 3 (count) · u16 0x3D4B · u8 0 (version)`
   = ตรง STRUCTURAL_IDS ทุก field
3. tag grammar อ่านจาก v141 เอง (ไม่ได้เดา): `u8tag` 0x05/0x08/0x0B · `u16tag` 0x0F/0x12 ·
   `u32tag` 0x14/0x26 · `qwordtag` 0x32 · `f32tag` 0x2A → sequential walk กิน 123/123 ไบต์พอดี

## โครง record เต็ม 123B (offset · tag · ค่า gt002 | hyp001)

```
+  0 u8 [0B] 0 (record version)      +  55 u8 [08] 1   ← record-index 1
+  2 u16[12] 0x0F01 (3841)           + 57 f32[2A] A     0.750817 | 0.693813  ★
+  5 u8 [0B] 0                       + 62 f32[2A] B1    0.950000 | 0.896632  ★
+  7 u8 [0B] 1                       + 67 u8 [0B] 2 · +69 u8 4 · +71 u8 0
+  9 u8 [0B] 0xFF                    + 73 u64[32] 111
+ 11 u64[32] 0                       + 82 u8 [0B] 4 · +84 u8 1
+ 20 u32[26] 0xFFFFFFFF              + 86 u64[32] 110
+ 25 u8 [0B] 0x19 (25)               + 95 u8 [08] 2   ← record-index 2
+ 27 u8 [0B] 0 · +29 u8 0            + 97 f32[2A] A (ซ้ำ)                    ★
+ 31 u8 [05] 1                       +102 f32[2A] B2    0.922426 | 0.847851  ★
+ 33 u64[32] 0                       +107 u8 [0B] 0
+ 42 u32[26] 1                       +109 u8 [08] 3   ← record-index 3
+ 47 u8 [0B] 12 · 12 · 12            +111 f32[2A] A (ซ้ำ)                    ★
+ 53 u8 [0B] 3                       +116 f32[2A] B3    0.863188 | 0.799071  ★
                                     +121 u8 [0B] 0
```

★ = ไบต์ที่ต่างระหว่างเซสชัน (ตำแหน่ง 58-60,63-65,98-100,103-105,112-114,117-119 —
ทั้งหมดคือเนื้อ float 4 ค่า ไม่มีไบต์อื่นต่างเลย)

## พฤติกรรม server (สังเกตจาก console GT-002)

Foundation log `[G<` ครบ 4 ครั้ง **ไม่ส่ง response ใด ๆ** — dialog ฝั่ง client ยังเปิด/ทำงานปกติ
(ตัวที่ค้างคือ `LogoutVital` ตาม R38 ไม่ใช่เฟรมนี้)

## Nonclaims

1. **ไม่ claim ความหมายของ float ทั้งสี่** — candidate ที่เข้าเค้า (ค่า normalized [0,1],
   A แชร์ทั้ง 3 record, B เรียงลง) มีหลายทาง (UI/volume/ตำแหน่ง normalized) แต่มีแค่ 2
   เซสชันรูปแบบเต็ม ไม่มี ground truth ที่สามให้ correlate → ยังพิสูจน์ไม่ได้
2. ไม่ claim ความหมายค่าคงที่ (0x0F01 · 25 · 12,12,12,3 · u64 111/110 · u32 -1/1) —
   111/110 อยู่ในตำแหน่งที่ v141 ใช้ qword identity แต่การตีความว่าเป็น identity ยังไม่พิสูจน์
3. ไม่ claim เหตุที่ record เต็มถูกส่งซ้ำ 2 ชุด identical — ไม่ตีความว่าเป็นบั๊กหรือตั้งใจ
4. ไม่ claim ว่า original server ตอบเฟรมนี้อย่างไร — corpus ไม่มี golden response (ตรวจแล้ว)
5. ไม่ claim ว่า client ต้องการ response — แค่สังเกตว่า dialog ทำงานได้โดยไม่มี (ขอบเขต
   เฉพาะเซสชันที่มี)
6. ชื่อ `GetWorldInfoVital` เป็น wire name จาก registry R38 — เนื้อหาที่ client "ขอ" จริง
   อนุมานจากชื่ออย่างเดียวไม่ได้

## ผลต่อคิวงาน

- **ไม่บล็อก/ไม่เปลี่ยนคำถาม HYP-PF-012** — เสริมบริบทตัวเลือก (ก): เฟรมเปิด dialog
  เข้าใจครบแล้วและ ignore ได้ปลอดภัย การออกแบบ logout ไม่ต้องแตะ 0x3D4B
- unknown id ที่เหลือใน GT captures = หมดแล้ว (0x1B40 → R38, 0x3D4B → R40, 0xAC52 →
  candidate R38) — เครื่องมือ: `/tmp` scripts สร้างซ้ำได้จากขั้นตอนข้างบน
