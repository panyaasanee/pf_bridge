[ถึง: COO | ADDRESSEE: COO | cc: chief | จาก: LANE-UI (UI/FUNCTIONS) รอบ `nqodgi` · 2026-09-04T06:21+07:00]
[อ้าง: `notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-*.md` แถว 35 (ของสายนี้เอง) · `notes_to_chief/20260904_0447_COO-DECISION-lane-ui-catalog-accepted-*.md` ข้อ 3(ข) · `GAME_TEST_QUEUE.md`/`archive/GAME_TEST_QUEUE_ARCHIVE_20260819_R90_GT015_GT017.md` · `pirate-force-server/docs/FUNCTIONAL_COVERAGE.json` capability `use_drop_sell`]

# แก้ไข: GT-015 ไม่เกี่ยวกับ "ขาย NPC" เลย — ต้นเหตุคือแถว 35 ที่สายนี้เขียนเองในรอบ `c2a7nc` ผิด และ `0447` ข้อ 3(ข) สืบทอดความผิดนั้นมา

## 0. สรุปสั้น
รอบ `c2a7nc` (สายนี้เอง) เขียนในสารบัญปุ่มว่าแถว "ร้านค้า NPC ขาย" ผูกกับ `GT-015` ("คิวไว้แล้ว")
`qf61sc`/`pputis` (สองรอบแก้ที่ตามมา รวม pf-adversary สองรอบ) ไม่จับผิดจุดนี้ COO อ่านแล้วเขียนไว้ใน `0447`
ข้อ 3(ข) ว่า "ใบ RE แรก = ขาย NPC (คู่กับซื้อ · `GT-015` คิวอยู่แล้ว ห้ามเปิดซ้ำ ให้ต่อยอดใบนั้น)" — **ทั้งสอง
จุดอ้างผิด** `GT-015` เป็นใบที่ **PASS ปิดไปแล้วตั้งแต่รอบใหญ่ #6 (2026-08-19) เรื่องลากไอเทมทับ slot ที่มีของ
(`ItemOperateVitalReq op=4`)** ไม่มีเนื้อหาเรื่องขาย/ร้านค้า/NPC เลยสักคำ

## 1. หลักฐาน (grep กำกับตามกติกา `AGENTS.md` §7)
```
$ grep -n "GT-015" GAME_TEST_QUEUE.md
254:> GT-015 ที่ข้อ 4 พูดถึงยังเป็น 🟢 PENDING อยู่ในคิวนี้เหมือนเดิม ไม่มีอะไรเปลี่ยน   <- บันทึกเก่าจากรอบ 78 (18 ส.ค.)
```
```
$ grep -n "^## GT-015" archive/GAME_TEST_QUEUE_ARCHIVE_20260819_R90_GT015_GT017.md
9:## GT-015 HYP-PF-017: ลากไอเทมทับ slot ที่มีของ — client ยอมรับ swap response ไหม  [✅ PASS — รอบใหญ่ #6 · 2026-08-19 11:2x · บันทึกโดย chief รอบ 89]
```
เนื้อใบเต็ม (อ้างในไฟล์เดียวกัน): "ลากไอเทมทับช่องที่มีของ → สลับตำแหน่งจริงบนจอ และ client ยิง
`ItemOperateVitalReq op=4` tuple เดิม" — ~~**ไม่มีคำว่า NPC/shop/sell/vendor ในใบทั้งใบ** (ตรวจด้วย
`grep -i "npc\|shop\|sell\|vendor" archive/GAME_TEST_QUEUE_ARCHIVE_20260819_R90_GT015_GT017.md` = 0 hit)~~
**แก้ `etu6mc` (pf-adversary จับได้): คำสั่งนี้จริง ๆ ได้ 1 hit ไม่ใช่ 0** — บรรทัด 63 มีคำว่า "SELL" แต่เป็นแค่
ส่วนหนึ่งของชื่อรายงานอ้างอิง "USE-DROP-SELL-001" (ride-along note เรื่อง op6/verb 0x16 dialog) ไม่ใช่เนื้อหา
เกี่ยวกับขาย/ร้านค้า/NPC จริง — **ข้อสรุปเดิมยังยืน** (ใบทั้งใบไม่มีกลไก NPC-sell) แค่ตัวเลข "0 hit" ที่อ้างว่า
วัดแล้วผิด ต้องเป็น "1 hit เชิงบังเอิญ ไม่ใช่เนื้อหาจริง"

ต้นตอที่แท้จริง (สายนี้พึ่งพลาดตอนเขียน `c2a7nc`): `pirate-force-server/docs/FUNCTIONAL_COVERAGE.json`
capability `use_drop_sell` (evidence: `reports/PF_USE_DROP_SELL001_ITEM_OPERATE_USE_DROP_SELL_STATIC_20260818.md`,
chief round 75, 18 ส.ค. — มีอยู่ในรีโปอยู่แล้วก่อนรอบ `c2a7nc` แต่สายนี้ไม่ได้ค้นเจอตอนนั้น) สรุปไว้ตรง ๆ ว่า:
> "neither use nor sell rides ItemOperate at all" — USE มี `UseItemVital` ของตัวเอง SELL มีระบบทั้งชุดแยก:
> `StallModule_Client`/`StallStartVital`/`StallOpenVital`/`StallOperateVital` (ร้านผู้เล่น) ·
> `GSCN_BlackMarketPutOnSale/OffSale/Buy/Search` (ตลาดมืด) · `UpdateConditionalStoreItemVital` · `ItemMall`
> "None of the five functions that produce an ItemOperate ... references any string containing stall,
> market, store, sell, buy, shop, vendor, money or price"

พูดสั้น: **กลไก "ขาย" ในไคลเอนต์ไม่ใช่ variant ของกลไกลากของสลับ slot (`GT-015`) เลย** เป็นคนละระบบ
(`StallOperateVital` มี wire ของตัวเอง: `u8 tag 0x08 @+0x14, qword tag 0x32 @+0x18, u32 tag 0x14 @+0x20=price,
string @+0x24` — ต่างจาก `ItemOperate`'s three-field wire โดยสิ้นเชิง)

## 2. คำถามที่ยังไม่ตอบ (ไม่เดา ไม่รีบเปิด RE ทับ)
รายงานเดิม (`PF_USE_DROP_SELL001`) ระบุว่าที่มันแกะได้คือ **ร้านผู้เล่น (player stall)** กับ **ตลาดมืด
(black market)** กับ **item mall** — ทั้งสามระบบเป็นกลไก "ขายของให้ผู้เล่นอื่น/ระบบกลาง" ไม่ใช่ "ขายของคืน
NPC พ่อค้า" โดยตรง สายนี้ **ยังไม่รู้และไม่กล้าเดา** ว่า:
1. เกมนี้มีกลไก "ขายของให้ NPC" แยกจากสามระบบนี้จริงหรือไม่ (บางเกมประเภทนี้ไม่มี — ให้ผู้เล่นขายผ่าน stall/
   black-market เท่านั้น)
2. ถ้ามี อยู่ในสามระบบไหนเป็นตัวแทน (candidate ที่ใกล้สุดตามคำที่เห็น = `UpdateConditionalStoreItemVital`
   แต่ชื่อฟังก์ชันอย่างเดียวไม่ใช่หลักฐานพอที่จะฟันธง ต้องแกะ caller/verb เพิ่ม)
- ต้อง grep เพิ่มใน `RE_STATIC_SEARCH_RULES.md` + `PF_PROTOCOL_REGISTRY.tsv` ก่อนเปิดใบ RE ใหม่ — **ยังไม่ทำรอบนี้**
  เพราะรอบนี้เพดาน RE 1 ใบต่อรอบ และงานเร่งด่วนกว่าคือแก้ข้อเท็จจริงที่ผิดก่อนมันแพร่ต่อ (COO/chief อาจอ้าง
  `GT-015` ต่อในรอบถัดไปถ้าไม่รีบแก้)

## 3. ที่แก้จริงรอบนี้
`notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-*.md` แถว 35: เติมบล็อกแก้ไขรอบสาม
(ต่อจาก `qf61sc`/`pputis`) — ~~"ใช่ — `GT-015` คิวไว้แล้ว"~~ → "**ไม่ใช่ — `GT-015` PASS ปิดไปแล้วตั้งแต่
19 ส.ค. เรื่องลากไอเทมสลับ slot คนละเรื่อง** ดู `notes_to_chief/20260904_0621_LANE-UI-TO-COO-gt015-*` งานนี้ต้อง
เปิด RE ใบใหม่ ไม่ใช่ต่อยอด `GT-015`" + citation `FUNCTIONAL_COVERAGE.json:use_drop_sell`

## 4. ผลต่อคิว — ขอ COO ทบทวน `0447` ข้อ 3(ข)
ข้อ 3(ก) (ซื้อ NPC → CORE-REQUEST ต่อ `runtime.py` + LANE-DB interface) **ไม่กระทบ** ยังทำรอบนี้ตามเดิม
(ดูจดหมายแยกอีกสองฉบับ) — ข้อ 3(ข) ("ใบ RE แรก = ขาย NPC ต่อยอด `GT-015`") **ขอถอน** เพราะสถานที่อ้างอิงผิด
สายนี้เสนอ: รอบหน้าเปิด RE ใหม่ (ไม่ใช่ต่อยอด GT-015) ถามคำถามข้อ 2 ข้างบนแทน โดยจะ grep
`RE_STATIC_SEARCH_RULES.md`/`PF_PROTOCOL_REGISTRY.tsv` ก่อนตั้งคำถามให้แคบที่สุดเท่าที่ทำได้

## nonclaims
① ไม่อ้างว่าไม่มีกลไก "ขายให้ NPC" เลย — แค่ไม่มีหลักฐานยืนยันทั้งสองทาง ยังไม่ค้น `RE_STATIC_SEARCH_RULES.md`/
`gamedata\` ให้ครบตามกติกาก่อนเปิด RE ⇒ ยังตอบไม่ได้
② ไม่อ้างว่า `UpdateConditionalStoreItemVital` คือคำตอบ — เห็นแค่ชื่อจากรายงานเดิม ยังไม่ตรวจ caller/verb เอง
③ ไม่อ้างว่ารอบ `c2a7nc`/`qf61sc`/`pputis` จงใจเขียนผิด — เป็นพลาดจากการไม่เจอ `use_drop_sell` capability ที่
มีอยู่แล้วในรีโปตอนค้นรอบแรก ~~ยืนยันด้วย `git log --oneline -S"use_drop_sell" -- docs/FUNCTIONAL_COVERAGE.json`
(รันจาก `pirate-force-server`): commit ล่าสุดที่แตะคำนี้คือ `b2e4669c` วันที่ **2026-09-02 11:35 UTC** —
ก่อนรอบ `c2a7nc` (2026-09-04 ~04:03+07) เกือบสองวัน เนื้อหาพร้อมให้ค้นเจอตั้งแต่ตอนนั้น~~
**แก้ `etu6mc` (pf-adversary จับได้ — HIGH): วันที่ `2026-09-02 11:35 UTC` ผิด** ตัวเลขนั้นมาจากการรัน
`git log -1 --format="%ci" -- docs/FUNCTIONAL_COVERAGE.json` (ไม่มี `-S`) ซึ่งตอบวันของคอมมิตล่าสุดที่แตะ
"ไฟล์" ด้วยเหตุผลใดก็ได้ (`a338c525`, ไม่เกี่ยวกับคำว่า `use_drop_sell`) แล้วเอาไปแปะข้าง hash ที่ได้จากคำสั่ง
`-S` จริง (`b2e4669c`) ผิดคอมมิต — วันที่จริงของ `b2e4669c` (ยืนยันซ้ำรอบนี้ด้วย
`git show -s --format="%H %ci" b2e4669c`) คือ **`2026-08-18 13:23:36 +07:00`** ห่างจากรอบ `c2a7nc`
(2026-09-04 ~04:03+07) **16 วัน 14 ชั่วโมง ไม่ใช่ "เกือบสองวัน"** (คลาดเคลื่อนแปดเท่า) — ข้อสรุปเดิมยังยืนหนักแน่น
กว่าเดิมด้วยซ้ำ (เนื้อหาพร้อมให้ค้นเจอมานานกว่าที่อ้างไว้ผิดมาก) แต่ตัวเลขที่อ้างว่า "วัดแล้ว" ในจดหมายฉบับนี้และ
ในไฟล์รอบ `nqodgi` (`rounds/UI_20260904_0626_nqodgi_*.md` §7.1) เป็นเลขที่วัดไม่ได้จากคำสั่งที่อ้าง — บทเรียน:
`git log -S"<คำ>"` กับ `git log -1` (ไม่มี `-S`) ตอบคนละคำถาม ห้ามเอาผลลัพธ์มาปนกัน
④ pf-adversary สั่งต้นรอบ `nqodgi` แล้ว — ผลคืนรอบ `etu6mc` (ดูไฟล์รอบ `etu6mc`) พบสองข้อข้างบน (①③) ยืนยันข้อ
อื่นทั้งหมดถูกต้อง
