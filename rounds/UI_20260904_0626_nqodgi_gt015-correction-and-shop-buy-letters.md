# LANE-UI round nqodgi — GT-015/NPC-sell correction + shop-buy CORE-REQUEST pair (chief + LANE-DB)

เวลา: 2026-09-04 06:26 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ NOW/M โดยตรง — รอบนี้เป็นเอกสารล้วน (สามจดหมาย + แก้ไฟล์เดิมหนึ่งจุด) ไม่มีโค้ด ไม่มีชิ้นงานบนจอ
เตรียมพื้นให้คิว "ร้านค้า NPC ซื้อ" ของ `NOW.md` (บรรทัด "UI-A ปุ่มออกไปหน้าเลือกตัวละคร · UI-B ... —
เจ้าของใหม่ LANE-UI" และ `COO-DECISION 0447` ข้อ 3) เดินต่อได้จริง แทนที่จะเดินตามสมมติฐานที่ผิด (`GT-015`)

## ทำอะไร
1. `git fetch origin main` ทั้งสองรีโป · `git checkout -B` จาก `origin/main` ทั้งคู่ (ไม่มีดริฟต์)
2. List PR เปิดหัว `[LANE-UI]` ทั้งสองรีโป — ไม่มีใบเก่าค้าง (PR อื่นที่เห็นเป็นของสายอื่น: `pf_bridge#1074`
   `[LANE-B]`, `pirate-force-server#707` `[LANE-DB]` — ไม่ใช่ล็อกของสายนี้ ไม่แตะ)
3. claim ที่ `pf_bridge` — PR `#1076` (`[LANE-UI] round nqodgi: claim`) · body ผ่าน
   `pf_gate_preflight.py --pr-body --pr-stage claim` (`[prbody] PASS`) ก่อนเปิด
4. กล่องจดหมาย: `grep -l "ADDRESSEE: LANE-UI" notes_to_chief/*.md` แล้วกรองใบที่มี `.CONSUMED.txt` ออกเอง (ไม่ใช้
   ผล grep ดิบ) เจอ 2 ใบ: `20260904_0447_COO-DECISION-*` — **consumed แล้วจริง** (มี `.CONSUMED.txt`,
   ตอบครบในรอบ `pputis`) กับ `20260904_0332_LANE-PROMPT-*` — **false positive**: จ่าหน้าจริงคือ `ADDRESSEE:
   COO` (บรรทัด 1) สตริง "ADDRESSEE: LANE-UI" ที่ grep เจอเป็นแค่ตัวอย่างคำสั่งอยู่ในเนื้อพรอมป์เอง (บรรทัด 27:
   `grep -l "ADDRESSEE: LANE-UI" ...`) ไม่ใช่จดหมายถึงสายนี้จริง ⇒ ไม่ต้องตอบ ไม่สร้าง `.CONSUMED.txt`
5. รอบก่อน (`pputis`) บันทึกไว้ชัดว่า **ไม่มี** `ADVERSARY_PENDING` ค้าง — ไม่มีอะไรให้หยิบเป็นงานแรก
6. เริ่มงานคิวใหม่ตาม `0447` ข้อ 3 — ก่อนเขียนจดหมาย CORE-REQUEST ตรวจ `GT-015` (ที่แถว "ร้านค้า NPC ขาย" ของ
   catalog รอบ `c2a7nc` อ้างไว้) ตามกติกา grep-กำกับ พบว่า **อ้างผิด** (รายละเอียดเต็มในจดหมายข้อ 7.1)
7. เขียนจดหมายสามฉบับ (สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานตามกติกา — ดู `ADVERSARY_PENDING` ท้ายไฟล์):

### 7.1 `notes_to_chief/20260904_0621_LANE-UI-TO-COO-gt015-has-nothing-to-do-with-npc-sell-*.md`
ถึง COO cc chief — retract: `GT-015` (PASS ปิดแล้ว 19 ส.ค., เรื่องลากไอเทมสลับ slot `ItemOperateVitalReq op=4`)
ไม่เกี่ยวกับ "ขาย NPC" เลย ต้นเหตุคือ catalog รอบ `c2a7nc` ของสายนี้เองเขียนผิด (พลาดไม่เจอ
`FUNCTIONAL_COVERAGE.json:use_drop_sell` capability ที่มีอยู่แล้วในรีโปตั้งแต่ commit `b2e4669c`
2026-09-02 — ก่อนรอบ `c2a7nc` เกือบสองวัน) ผลคือ `COO-DECISION 0447` ข้อ 3(ข) ("ใบ RE แรก = ขาย NPC ต่อยอด
`GT-015`") สืบทอดความผิดมา — ขอ COO ทบทวนข้อนั้น เสนอเปิด RE ใหม่รอบหน้าแทนแทนที่จะต่อยอดใบผิด (คำถามเปิด:
กลไก "ขายให้ NPC" แยกจาก Stall/BlackMarket/ItemMall หรือไม่ — ยังไม่ตรวจ ไม่เดา)

แก้ไฟล์เดิมคู่กัน: `notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-*.md` — เติมบล็อกแก้ไขรอบสามที่หัว
จดหมาย + strikethrough แถว "ร้านค้า NPC ขาย" (ไม่ลบของเดิม ตามธรรมเนียมโปรเจกต์) ยาว 10,463 อักขระหลังแก้
(ต่ำกว่าเพดาน 12,000)

### 7.2 `notes_to_chief/20260904_0621_LANE-UI-CORE-REQUEST-wire-tradecmdvital-*.md`
ถึง chief cc COO/LANE-B/LANE-DB — **ไม่ใช่ CORE-REQUEST ใบใหม่**: grep ก่อนเขียนตามกติกา §7 พบว่า LANE-B
ส่งคำขอเดียวกันไปแล้วจริงตั้งแต่ 2026-08-30 20:50+07 (`notes_to_chief/consumed/20260830_2050_LANE-B-STATUS-*.md`,
ฝัง CORE-REQUEST เต็มในดอกสตริง `trade_session_membership.py`) — ยืนยันสดรอบนี้ว่า **ยังไม่ wire** (`grep -n
"TRADE_CMD_VITAL\|TradeCmdVital\|active_store_session" src/pirateforce_foundation/runtime.py` = 0 hit ·
คอมมิตเดียวที่แตะไฟล์ predicate คือของ LANE-B เอง `d61d3f0a`, ไม่มี commit ใน `runtime.py` อ้างถึงมันเลย) —
ค้างมา 5 วัน จดหมายนี้ขอ priority + เติมบริบทที่ `0447` ต้องการ (จุดเสียบ LANE-DB, ดู 7.3) ให้ครบมือ chief
คราวเดียว แทนเขียนซ้ำเนื้อหาเดิม พร้อมย้ำสองคำถามเปิดเดิมที่ยังไม่มีใครตอบ (actor identity attribute /
generation counter ใช้ร่วมกับ `mob_combat_membership.py` หรือไม่)

### 7.3 `notes_to_chief/20260904_0621_LANE-UI-CORE-REQUEST-lane-db-shop-money-and-backpack-interface-*.md`
ถึง LANE-DB cc chief/COO — ขอ interface อ่าน/เขียนเงิน (x=24 cash) + backpack สำหรับ cart-add/final-buy ในอนาคต
(ยังไม่มีใครสร้างทั้งสองฝั่ง — `grep -n -i "gold\|money\|currency" src/pirateforce_foundation/store.py` เจอแค่
สองบรรทัดไม่เกี่ยวกัน) อ้างบริบทเดิมที่มีอยู่แล้ว (`live_named_attr_values.py:90-103`: x=24 คงตัว 10000 vs DB
NULL vs HUD "1 gold" — ความขัดแย้งที่ยังไม่คลี่) ระบุชัดว่า **ไม่บล็อกคิว PLAYER/CHARACTER 5 ชิ้นของ LANE-DB**
(`PANYA-DECISION 0328` ข้อ 1 มาก่อนเสมอ) แค่ลงคำขอไว้ล่วงหน้า

## ADVERSARY_PENDING
`pf-adversary` สั่งต้นรอบพร้อมเริ่มงานจดหมาย (ตรวจข้อเท็จจริง/grep ทั้งสามฉบับข้างบน) — **ยังไม่คืนผลตอน push**
บันทึกไว้: **`ADVERSARY_PENDING pf_bridge#1076`** (เลข PR หลัง push จริงจะยืนยันอีกครั้งด้านล่าง) — รอบถัดไปของ
LANE-UI หยิบผลเป็นงานแรกก่อน claim งานใหม่ตามกติกา §7 · **ห้ามเขียนว่า "ผ่าน adversary" ในไฟล์นี้เพราะผลยังไม่คืน**

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `#1076` (`[LANE-UI] round nqodgi: claim` → เติมไฟล์รอบนี้ + สามจดหมายใหม่ + แก้ไฟล์ catalog
  เดิม 1 จุด, กิ่ง `claude/wizardly-knuth-1mxas0`)
- ไม่มี PR เซิร์ฟเวอร์ — รอบนี้ไม่แตะโค้ด `pirate-force-server` เลย (อ่านอย่างเดียวเพื่อยืนยัน grep ทุกจุดที่อ้าง
  ในจดหมาย, ยืนยันด้วย `pf_gate_preflight.py` ที่รันสำเร็จ `PREFLIGHT PASS` ระหว่างตรวจ claim body)

## nonclaims
① การแก้ `GT-015` อาศัยการอ่าน `archive/GAME_TEST_QUEUE_ARCHIVE_20260819_R90_GT015_GT017.md` เต็มใบ +
`FUNCTIONAL_COVERAGE.json:use_drop_sell` เต็มข้อความ — ยืนยันสองแหล่งตรงกัน ไม่ใช่แหล่งเดียว
② ไม่อ้างว่ากลไก "ขายให้ NPC" มีหรือไม่มีจริง — เปิดเป็นคำถามให้ RE รอบหน้า ไม่เดา ไม่เปิด RE ทับรอบนี้
(เพดาน 1 ใบต่อรอบ + ยังไม่ค้น `RE_STATIC_SEARCH_RULES.md`/`gamedata\` ให้ครบตามกติกาก่อนตั้งคำถามแคบพอ)
③ จดหมายถึง chief (7.2) ไม่ได้ยืนยันว่า chief ละเลยโดยตั้งใจ — แค่รายงานสถานะสดว่ายังไม่ wire
④ จดหมายถึง LANE-DB (7.3) ไม่ได้ตรวจ DB schema จริงว่ามีคอลัมน์เงินหรือยัง — นอกเขตอ่าน/เขียนที่มั่นใจของสายนี้
⑤ ไม่ได้เปิดเกม ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ · ไม่ได้แตะ `runtime.py`/`store.py`/
`trade_session_membership.py`/`inventory.py` เอง — เขียนจดหมายอย่างเดียวทั้งรอบ
⑥ pf-adversary ยังไม่คืนผล ณ เวลา push — ดูหัวข้อ `ADVERSARY_PENDING` ข้างบน

## รอบถัดไปทำอะไรต่อ
1. **หยิบผล `pf-adversary` ก่อนสิ่งอื่นใด** (`ADVERSARY_PENDING pf_bridge#1076`) — เจอบั๊กจริงที่อยู่บน `main`
   แล้วให้เปิดใบแก้ทันที ไม่รอคิว
2. รอผล COO ทบทวน `0447` ข้อ 3(ข) (จดหมาย 7.1) — ถ้ายืนยันถอนแล้ว เปิด RE ใหม่ (ไม่ใช่ต่อยอด `GT-015`) ถาม
   คำถามเปิดข้อ 2 ของ nonclaims ข้างบน โดย grep `RE_STATIC_SEARCH_RULES.md`/`gamedata\` ก่อนตั้งคำถาม
3. รอ chief ตอบจดหมาย 7.2 (wire `TradeCmdVital`) และ LANE-DB ตอบจดหมาย 7.3 (interface เงิน/กระเป๋า) — ไม่บล็อก
   สายนี้จากการทำคิวถัดไปในสารบัญข้อ 1 (ระบบยิบย่อยอื่นที่ยังไม่ได้แตะ: Options apply, เพื่อน/เมล/ปาร์ตี้ ฯลฯ)
