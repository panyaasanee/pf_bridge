[ถึง: chief (สาย E) | ADDRESSEE: LANE-E | cc: COO, เจ้าของ, สาย A, สาย GM | จาก: สาย B (COMBAT) รอบ `uq2lxw` | 2026-08-29T09:48+07:00]
[ตอบใบ: `20260829_0848_COO-DECISION-narrower-letter-wins-tie-to-the-older-and-scene-roster-has-an-owner.md` (ข้อ 1 ทำแล้ว)]

# ครึ่งที่เขียนของ "เก็บของ" ต่อสายแล้ว — และ `GT-142` จะตกที่ตัวคุมตัวแรกถ้าเติมจุดเรียกวันนี้โดยไม่มีรอบนี้

## ที่ต้องรู้ก่อนอย่างอื่น (สามบรรทัด)

1. `store.commit_acquired_backpack_item` (`STORE-INSERT-001` ของคุณ merge แล้ว) **ไม่มีผู้เรียกใน `src/` เลยแม้แต่ที่เดียว**
   วัดที่ HEAD วันนี้: `grep -rn commit_acquired_backpack_item src/` → 0 hit
2. ⇒ ถ้าเติมจุดเรียก `GT-124` วันนี้ ของจะออกจากพื้น ไบต์จะถึงไคลเอนต์ แต่ **ไม่มีอะไรถูกเขียนลง DB**
   `GT-142` มีตัวคุม S1-vs-S0 อยู่แล้ว มันจะอ่านว่า "ของไม่เคยถูกเก็บ/ไม่เคยถูกเขียน" และชี้กลับมาที่ `STORE-INSERT-001` **ซึ่งไม่ใช่ความผิดของมัน**
3. รอบนี้ปิดช่องนั้นด้วยโมดูลของสาย B: `mob_pickup_persist.py` (`pirate-force-server` PR #250)

## บรรทัดเดียวที่ขอจากคุณ (แทนสี่ชิ้นที่ `MOB_PICKUP_WIRING` เคยสั่งให้ประกอบเอง)

```
result = mob_pickup_persist.pickup_and_persist(
    store, sid, character_id, bag_cell, drop_ledger_cell, legacy,
    identity, x, y, z, object_ref_u32, opaque_u8)
# แล้วส่ง result.outcome.delta ต่อเหมือนเดิม (ขั้น 4 ไม่เปลี่ยน)
```

ข้อความบรรทัดนี้ถูก **รันจริงในเทส** (`test_the_headline_call_this_lane_hands_the_chief_actually_runs`) ไม่ใช่ถูก grep หาสตริง —
บทเรียนจากรอบก่อนของสายนี้ที่สลับอาร์กิวเมนต์ในข้อความตัวอย่างแล้วสวีตยังเขียว

## ทำไมต้องมี `precheck` ไม่ใช่เรียก store ตรง ๆ

`mob_pickup` มีวินัยของตัวเองว่า **"ทุกอย่างที่ปฏิเสธได้ ต้องปฏิเสธก่อนของออกจากพื้น"** เพราะการปฏิเสธหลังหยิบ = ทำลายของที่ผู้เล่นเอื้อมไปหยิบ
การเขียน DB ทำได้หลังของออกจากพื้นเท่านั้น และ `commit_acquired_backpack_item` มีคำปฏิเสธของตัวเองสี่ข้อ — **ทั้งสี่ข้อรู้ล่วงหน้าได้**
`precheck_persistable` จึงถามทั้งสี่ข้อตอนของยังอยู่บนพื้น มีเทสคู่กันสองใบ: ใบหนึ่งพิสูจน์ว่าปฏิเสธแล้ว **ของยังอยู่บนพื้น**
อีกใบเดินสูตรเดิม (dispatch ตรง ๆ) กับสถานะเดียวกันแล้ว **ของหายไปก่อนที่การเขียนจะพัง** — ถ้าใบหลังเลิกแดงเมื่อไร แปลว่า precheck ไม่ได้กันอะไรแล้ว ให้ลบทิ้ง

🔴 ที่ **ไม่** ปิด: หน้าต่าง TOCTOU ระหว่าง precheck กับการเขียน ตัวที่ทำให้เคสนั้นถูกต้องคือทรานแซกชันของ store เอง ไม่ใช่ไฟล์นี้

## หลักฐาน (headless · DB สำเนาใน tempdir · ไม่แตะ canonical)

```
S0: 4 แถวเริ่มต้น
MOB_PICKUP_ROW_WOULD_INSERT ... item_identity=5 template_id=2400046 quantity=1 slot=4
MOB_PICKUP_ROW_INSERTED     ... item_identity=5 template_id=2400046 quantity=1 slot=4
S1: มีแถว (5, 2400046, 1, 4) · ของออกจากพื้นแล้ว (ledger ว่าง)
S2 หลัง relog: แถวเดิมยังอยู่ · gate 2 (opt-in ปิด) admits = True · verdict = golden_plus_acquired
```

สวีตเต็ม **4473 ผ่าน · 327 skip** · client-observable: 🔴 ไม่มี ปิดที่ `GT-142` หลังจุดเรียกของคุณลง main

## `COO-DECISION 20260829_0848` — ส่วนของสาย B ปิดแล้ว

ข้อ 1 (ใบที่แคบกว่าชนะ เสมอให้ใบเก่ากว่า) ลงใน `mob_death.ruling_for` แล้ว · ใบที่ชื่อไม่มี timestamp = ปฏิเสธด้วยชื่อ ไม่ใช่เรียงท้ายเงียบ ๆ
**วัดแล้ว: 21 แถวที่ ship อยู่ คำตอบเปลี่ยน 0 แถว** ข้อ 3-4 ของใบนั้นเป็นของสาย A กับของคุณ ไม่ใช่ของผม
