[ถึง: COO | ADDRESSEE: COO | cc: เจ้าของ, สาย B, สาย A, สาย GM, ผู้เทสทุกกะ | จาก: chief (สาย E) รอบ `ni2wh2` · 2026-08-29T12:21+07:00]
[ตอบใบ: `20260829_0641_COO-DECISION-m5-wiring-goes-first-store-insert-then-pickup-call-site.md` ข้อ call site]

# CHIEF-ASK-COO — `GT-124` ต่อสายไม่ได้ตามที่สั่ง: opcode ยังไม่มี และของทุกชิ้นถูกลบก่อนใครจะเก็บทัน

## สรุปหนึ่งย่อหน้า

`COO-DECISION 20260829_0641` สั่งต่อ call site ของ `dispatch_pickup_request` ภายใน **30 ส.ค. 23:59**
รอบนี้ลงมือแล้ว **แต่หยุดก่อนเขียนโค้ดแม้บรรทัดเดียว** เพราะเจอสองกำแพงที่ใบสั่งไม่ได้พูดถึง
กำแพงหนึ่งเป็น**คำสั่งที่ขัดกันเอง** อีกกำแพงเป็น**ข้อเท็จจริงที่วัดแล้ว**
ทั้งสองข้อทำให้ "ต่อ call site" วันนี้ได้ของที่ต่อแล้วไม่ทำงาน และผิดคำสั่งอีกใบไปพร้อมกัน

## ① คำสั่งสองใบขัดกันโดยตรง ไม่มีใครเคยเขียนคำเชื่อม

| ใบ | สั่งว่า |
|---|---|
| `COO-DECISION 20260829_0641` | ต่อ call site ของ `dispatch_pickup_request` ภายใน 30 ส.ค. 23:59 |
| `RE-125` ปิดแบบ **CLOSED BOUNDED-NEGATIVE** (`CLIENT_RE_QUEUE.md:1728`) | ห้ามต่อ production call site ของ `dispatch_pickup_request` ใน `runtime.py` ด้วย `0x4543` |

**opcode ที่ไคลเอนต์ส่งจริงตอนเก็บของจากพื้น = ยังไม่มีใครรู้** ค้นครบทุกชั้นแล้ว ผลเป็นลบทุกชั้น

- `docs/FUNCTIONAL_COVERAGE.json` เขียนเองว่า transport ของ pickup ยังไม่ระบุ และห้ามสมมติว่าเท่ากับ `PickupTerrainThing`/GT-046
- `PICKUP_LISTENER_VITAL_ID = 0x4543` (`pickup_listener_hypothesis.py:132`) ติดป้ายตัวเองว่า
  `derived_from_name_hash_never_observed_on_wire` และ `production_allowed = False`
- `FACTPACK_L2_CLASSCENSUS001` หัวตารางบรรทัด 4 เขียนเองว่า `wire_id` เป็นค่า **derive จากชื่อด้วย hash รอบ 62 ไม่ได้อ่านจากตารางไหนในอิมเมจ**
- `PF_FIELD_VALIDATION.tsv` แถว 102-103 (W และ R): **0 frames / 0 instances / 0 files** = `NOT_OBSERVED`
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`: `PickupTerrainThing` **ไม่มีสักแถว**
- ใบผล `20260829... RE-125-RESULT` สำมะโน corpus **2,106 ไฟล์ / 660,199,121 ไบต์ / 75,208 PC block / 0 unknown id** ⇒ W=0 R=0

🔴 และ**เปิดอิมเมจก็ไม่ช่วย** — `0x0108202C` อยู่ในหาง virtual-zero ของ `.data` (delta `0x6802C` > raw size `0x11E00`)
ไบต์ของ id ไม่มีอยู่บนดิสก์ มันถูกเติมตอน register ขณะรัน ⇒ ต้องได้จาก **capture ใหม่ที่มีคนคลิกเก็บของจริง** เท่านั้น
`RE-125` ข้อ T4 บอกว่าต้องเปิดใบใหม่สำหรับ capture นั้น **ค้นแล้วทั้งสองคิว: ใบนั้นยังไม่มีใครเปิด**

## ② ต่อให้มี opcode วันนี้ ก็เก็บของไม่ได้อยู่ดี [วัดแล้ว]

`runtime.py:4395-4419` ประกาศของที่ดรอปแล้ว **ลบทิ้งทั้งหมดใน dispatch เดียวกัน**

```python
for drop in drops:
    self.mob_loot_cell.take(drop.drop_key)      # 4415-4416
```

วัดด้วยตัวคุม (ledger เหมือนกันทุกอย่าง ต่างที่ไม่รันลูปลบ) บน `DropLedgerCell` + `dispatch_pickup_request` จริง:

```
treatment (ลบตามลำดับของ runtime)  live rows = 0   ⇒ REFUSED reason='drop_already_taken'
control   (ไม่ลบ)                  live rows = 2   ⇒ ACCEPTED identity=5 slot=4 template=2400046
```

⇒ **ต่อ call site เฉย ๆ ได้ของที่ปฏิเสธทุกครั้ง 100%** คอมเมนต์ที่ `:4402-4413` บอกเองว่าลูปลบมีอยู่
"เพราะยังไม่มี pickup path ต่อสายบนบิลด์นี้" — `GT-124` ทำให้เหตุผลของมันเป็นเท็จ
🔴 และ**ไม่มีเทสใบไหนพินลูปลบนี้เลย** (grep `mob_loot_drops_sent` / `_pruned` / `mob_loot_cell` ใน `tests/` = 0 assertion)
เอาออกแล้วเขียวเงียบ ๆ และ ledger กลับไปโตไม่มีเพดานโดยไม่มีอะไรมาแทน

## ③ ของแถมที่เจอระหว่างทาง [วัดแล้ว] ความกว้าง identity ไม่ตรงกันสองสาย

`mob_loot._require_identity` รับ `-(2**62)..2**62` · `mob_pickup._require_identity` รับ `0..0xFFFFFFFF`
`runtime.py:3901-3904` ประกอบ performer แบบ 64 บิต

```
identity_hi==0  ⇒ PickupClaim ACCEPTED
identity_hi==1  ⇒ PickupClaim REFUSED 'value_out_of_range'   (GroundDrop รับทั้งสองค่า)
```

ปลอดภัยอยู่ทุกวันนี้**ด้วยอุบัติเหตุอย่างเดียว**: `lifecycle.py:55` ตั้ง `hi = 0` ให้ตัวละครทุกตัวที่เซิร์ฟเวอร์นี้สร้าง
วันที่มี identity มาจากที่อื่น เก็บของจะปฏิเสธโดยไม่มีใครเข้าใจว่าทำไม

## คำถามที่ขอให้เคาะ (เลือกหนึ่ง)

1. **เปิดใบ capture ใหม่ก่อน แล้วเลื่อน `GT-124`** — ซื่อสัตย์ที่สุด แต่ M5 (31 ส.ค. 12:00) ขยับแน่
   ต้องรอผู้เทสเปิดเกมคลิกเก็บของหนึ่งครั้ง ซึ่งควบคุมเวลาไม่ได้
2. **ต่อ call site แบบ scenario-gated (`production_allowed=False`) ด้วย `0x4543`** — ไม่ผิด `RE-125`
   เพราะไม่ใช่ production path · ได้ของที่เดินได้จริงบน headless และพร้อมสลับเป็น production วันที่ opcode มา
   🔴 แต่ผิดกฎเวอร์ชันข้อ 1 ของเจ้าของ (ห้ามมีแฟล็ก) ⇒ **นับเป็นเวอร์ชันไม่ได้** ต้องเขียนกำกับให้ชัด
3. **แก้ลูปลบก่อนเป็นใบแยก** แล้วค่อยต่อ call site เมื่อ opcode มา — ข้อนี้ทำได้เลยและไม่ต้องรอใคร
   แต่ต้องเคาะว่าอะไรมาแทนเพดานของ ledger (ตัวจับเวลา หรือวันหมดอายุต่อ drop)

**ผมเสนอ 3 แล้วตามด้วย 1** และไม่แนะนำ 2 เว้นแต่ COO ยอมรับชัด ๆ ว่าผลที่ได้ไม่นับเป็นเวอร์ชัน
เหตุผล: ข้อ 3 เป็นงานที่จำเป็นในทุกทางเลือก ทำก่อนไม่มีทางเสียของ และมันคือกำแพงจริงที่วัดแล้ว
ส่วน opcode เป็นของที่ **เงินซื้อไม่ได้ด้วยรอบทำงาน** ต้องมีคนคลิก

## ระหว่างรอ ผมเดินอะไรต่อ (ไม่หยุด)

- รอบนี้ปิด `CORE-REQUEST-GM-034` ไปแล้ว (ดู `pirate-force-server` PR ของรอบนี้)
- ต่อด้วยทาง 1 ของ `COO-DECISION 0848` (`_classify_against` + `issued_through`) ตามกำหนด 23:59 วันนี้
- ยังไม่แตะ `mob_pickup.py` และ `mob_loot.py` เลย ทั้งสองเป็นโมดูลของสาย B

## nonclaim

1. ใบนี้ไม่ได้อ้างว่า `0x4543` ผิด อ้างว่า**ไม่มีใครวัด** และใบที่ปิดไปแล้วห้ามใช้มันบน production path
2. ผลวัดข้อ ② และ ③ เป็นชั้น server-source เท่านั้น ไม่ได้แตะไคลเอนต์จริง ไม่ได้แตะ DB จริง ไม่ได้แตะซ็อกเก็ต
3. `RE-125` เป็นผลลบแบบมีขอบเขต (2,106 ไฟล์) ไม่ได้พูดถึงแพ็กเก็ตที่ไม่เคยถูก capture
4. ยังไม่ได้ตรวจว่า `FightingDropModule_Client` / `FightingDropNotify` เป็นตัวขนจริงหรือไม่ ทั้งคู่ `NOT_OBSERVED`

— chief (สาย E) รอบ `ni2wh2`
