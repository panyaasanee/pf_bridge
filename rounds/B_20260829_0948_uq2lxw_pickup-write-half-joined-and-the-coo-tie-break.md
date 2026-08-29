# LANE-B รอบ `uq2lxw` — ครึ่งที่เขียนลง DB ของการเก็บของ ต่อสายแล้ว · และกฎเลือกใบตามที่ COO เคาะ

เปิดรอบ 2026-08-29T09:33+07:00 · เขียน 2026-08-29T09:48+07:00 · repo: `pirate-force-server` PR #250 · `pf_bridge` PR #390

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่เห็น และรอบนี้ไม่อ้างว่าเห็น** — `runtime.py` ยังไม่มีจุดเรียกของ opcode "เก็บของ" (`GT-124`) ซึ่งเป็นไฟล์ของ chief
สิ่งที่รอบนี้เปลี่ยนคือ **วันที่บรรทัดนั้นถูกเติม ของที่เก็บจะถูกเขียนลง DB จริง** ซึ่งก่อนรอบนี้จะ**ไม่ถูกเขียน**แม้บรรทัดนั้นมีแล้ว

## ① ตัวบล็อกที่วัดเจอ: สองครึ่งของ M5 อยู่บน main แล้ว แต่ไม่เคยรู้จักกัน

- `mob_pickup.dispatch_pickup_request` — เอาของออกจากพื้น ประกอบไบต์ให้ไคลเอนต์ แล้ว **log อย่างเดียว** (`MOB_PICKUP_ROW_WOULD_INSERT`)
- `store.commit_acquired_backpack_item` — `STORE-INSERT-001` ของ chief (merge แล้ว `#244`) เขียนแถวจริงและเดินตัวนับในทรานแซกชันเดียวกัน

วัดที่ HEAD ของรอบนี้: `grep -rn commit_acquired_backpack_item src/` = **0 hit** (มีแต่ใน `tests/` กับในข้อความคอมเมนต์)
⇒ **ถ้า chief เติมบรรทัด `GT-124` วันนี้ `GT-142` จะตกที่ตัวคุม S1-vs-S0 ทันที** ("ของไม่เคยถูกเขียน") ทั้งที่ทั้งสองครึ่งเขียวอยู่บน main

## ② ที่ ship: `src/pirateforce_foundation/mob_pickup_persist.py` (โมดูลใหม่ของสายนี้ · ไม่มีแฟล็ก `production_allowed = True`)

- `precheck_persistable(store, sid, character_id, bag_cell)` — **ถามทุกคำถามที่ store จะปฏิเสธ ตั้งแต่ตอนของยังอยู่บนพื้น**
  นี่คือกฎเดียวที่โมดูลนี้เพิ่มเอง และมันเป็นเรื่อง**ลำดับ** ไม่ใช่เรื่องไอเทม: `mob_pickup` ประกาศวินัยของตัวเองว่า
  "ทุกอย่างที่ปฏิเสธได้ ต้องปฏิเสธก่อนหยิบ" แต่การเขียน DB ทำได้หลังของออกจากพื้นเท่านั้น ⇒ คำปฏิเสธของ store สี่ข้อ
  (เซสชันไม่ได้เลือกตัวละครนี้ · identity ไม่ตรงคอลัมน์ · ช่องไม่ว่าง · แถวผิดรูป) จะมาถึง**หลัง**ของหายไปแล้ว
  ⇒ ย้ายมาถามก่อน **ของที่ผู้เล่นเอื้อมไปหยิบจะไม่ถูกทำลายด้วย error ของฐานข้อมูล**
- `persist_pickup(...)` — ส่ง `outcome.item` **ตัวเดิม** (ตัวที่ identity อยู่บนสายไปแล้วใน `outcome.delta`) ให้ store ไม่ประกอบใหม่
- `pickup_and_persist(...)` — **บรรทัดเดียวสำหรับ chief** (`MOB_PICKUP_PERSIST_HEADLINE_CALL`) precheck → dispatch → persist
- โทเคนคอนโซล `MOB_PICKUP_ROW_INSERTED` **รูปเดียวกับ** `MOB_PICKUP_ROW_WOULD_INSERT` เป๊ะ เพื่อให้วางเทียบกันแล้วอ่านออกทันที (G-OBS)
- `mob_pickup.BagCell.issued_through` — property อ่านอย่างเดียว (อ่านใต้ล็อกเดียวกับ `.bag`) ที่ precheck ต้องใช้

## ③ กฎเลือกใบตาม `COO-DECISION 2026-08-29T08:48+07:00` ข้อ 1 (บริโภคใบแล้ว)

`mob_death.ruling_for` เปลี่ยนตัวตัดสินเสมอจาก **ชื่อเรียงตัวอักษร** → **ใบที่ลงทะเบียนก่อน** (`ruling_registered_at` อ่าน timestamp จากชื่อใบ)
เสมอจริง ๆ ค่อยเรียงชื่อ · ใบที่ชื่อไม่มี timestamp = **ปฏิเสธด้วยชื่อ** (`REFUSE_RULING_NAME_HAS_NO_TIMESTAMP`) ไม่ใช่ถูกเรียงไปท้ายเงียบ ๆ

🔴 **วัดแล้วว่าไม่ขยับของที่ ship อยู่แม้แถวเดียว**: 21 แถวที่มีใบครอบ · **คำตอบเปลี่ยน 0 แถว** · `PIN_WIDENING_RULING` เท่าเดิม
สิ่งที่เปลี่ยนคือ**ใบในอนาคต**: ใบใหม่ที่ชื่อเรียงมาก่อน (`AAA...`) เคยแย่ง provenance ของการฆ่าที่เกิดไปแล้ว ตอนนี้แย่งไม่ได้
เทสที่ตรึงข้ออ้างเดิมไว้ **ไม่ถูกลบ** เปลี่ยนข้ออ้างเป็น "ใบใหม่ไม่ย้ายของเก่า" ตามที่ใบสั่ง

## ④ หลักฐานสองชั้น

**wire/DB** (รันจริง headless บน DB สำเนาใน tempdir ไม่แตะ canonical):

```
S0 rows: [(1,2600001,1,0), (2,2400901,1,1), (3,2600001,1,2), (4,2200002,1,3)]
MOB_PICKUP_ROW_WOULD_INSERT table=character_backpack_items claimant=0x750059 character_id=1 item_identity=5 template_id=2400046 quantity=1 slot=4 raw_u8_38=0 raw_u8_39=255 detail_present=0
MOB_PICKUP_ROW_INSERTED   table=character_backpack_items claimant=0x750059 character_id=1 item_identity=5 template_id=2400046 quantity=1 slot=4
S1 rows: [... (5,2400046,1,4)] | ground now: ()
S2 rows (หลัง relog): [... (5,2400046,1,4)]
gate2 admits after relog: True | verdict: golden_plus_acquired
```

สวีตเต็ม: **4473 ผ่าน · 327 skip** (ก่อนรอบนี้ 4472 · เพิ่มไฟล์เทสใหม่หนึ่งไฟล์ 15 เทส)

**client-observable** — 🔴 **ไม่มี และไม่อ้างว่ามี** relog ในหลักฐานข้างบนคือปิด-เปิดเซสชันกับ store ไม่ใช่ไคลเอนต์ล็อกอิน
ชั้นนี้ปิดที่ `GT-142` (attended) หลัง chief เติมจุดเรียก `GT-124`

## ⑤ บรรทัดที่ขอจาก chief (ไฟล์ของคุณ ผมไม่แตะ)

1. จุดเรียก opcode เก็บของ (`GT-124`) ให้เรียก **บรรทัดเดียว**:
   `mob_pickup_persist.pickup_and_persist(store, sid, character_id, bag_cell, drop_ledger_cell, legacy, identity, x, y, z, object_ref_u32, opaque_u8)`
   แล้วส่ง `result.outcome.delta` ต่อ (ขั้น 4 เดิมของ `MOB_PICKUP_WIRING` ไม่เปลี่ยน)
2. (ค้างจากรอบก่อน ยังไม่ลง) `widened=mob_death.ruling_for(mob)` ที่ roster kill site · `describe_widening_coverage()` ตอนบูต ·
   roster/ledger ตามฉาก (`3911` + `1119`) ตาม `COO-DECISION 20260829_0848` ข้อ 3

## nonclaims

- ไม่มีบรรทัดไหนในรอบนี้อยู่บนเส้นทางที่ผู้เล่นเดินได้วันนี้ — ไม่มีจุดเรียกใน `runtime.py`
- `precheck_persistable` **ไม่**ปิดหน้าต่าง TOCTOU: ถ้ามีผู้เขียนรายที่สองแทรกระหว่าง precheck กับ write การเขียนก็ยังพัง
  ตัวที่ทำให้เคสนั้นถูกต้องคือทรานแซกชันของ store เอง (rollback) ไม่ใช่ไฟล์นี้ · เขียนไว้ใน docstring ตรงนั้นด้วย
- รอบนี้ไม่แตะ `runtime.py` `app.py` `pf_login_game_server_v141.py` และไม่แตะเขตสาย A
