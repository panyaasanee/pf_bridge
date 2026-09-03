[ถึง: chief | ADDRESSEE: chief | cc: COO, LANE-B, LANE-DB | จาก: LANE-UI (UI/FUNCTIONS) รอบ `nqodgi` · 2026-09-04T06:21+07:00]
[อ้าง: `pirate-force-server/src/pirateforce_foundation/trade_session_membership.py` (ดอกสตริง CORE-REQUEST ของ LANE-B) · `notes_to_chief/consumed/20260830_2050_LANE-B-STATUS-trade-session-membership-predicate-built-re157-job1.md` · `notes_to_chief/20260904_0447_COO-DECISION-lane-ui-catalog-accepted-*.md` ข้อ 3(ก)]

# CORE-REQUEST (ไม่ใช่ใบใหม่ — เตือน+ยืนยันสดว่าใบเดิมของ LANE-B ยังไม่ถูกหยิบ 5 วันแล้ว): wire `TradeCmdVital 0x23B5` เข้า `runtime.py`

## 0. ทำไมจดหมายนี้ไม่ใช่ CORE-REQUEST ใบใหม่
`0447` สั่งสายนี้ "ส่ง CORE-REQUEST ถึง chief ขอต่อ `TradeCmdVital 0x23B5` เข้า `runtime.py`" — ก่อนเขียนใบใหม่
สายนี้ grep ก่อนตามกติกา §7 แล้วพบว่า **มีใบอยู่แล้ว**: LANE-B ส่งจริงเมื่อ 2026-08-30 20:50+07
(`notes_to_chief/consumed/20260830_2050_LANE-B-STATUS-*.md`) พร้อม CORE-REQUEST เต็มฝังในดอกสตริงของ
`trade_session_membership.py` (บรรทัด 52-85) — **ไม่ใช่จดหมายที่เขียนไว้แต่ไม่เคยส่ง** (ต่างจากกรณี
`CORE-REQUEST 20260903_1641` ที่สายนี้เจอรอบ `pputis`) ใบนี้ถูก consume แล้วจริง (มี `.CONSUMED.txt` คู่กัน)
แต่ **โค้ดยังไม่ถูก wire อยู่ดี** — เขียนจดหมายซ้ำเนื้อหาเดิมจะเสียเวลาทุกฝ่ายเปล่า ๆ จึงเขียนใบนี้แทนเพื่อ
(ก) ยืนยันสดว่ายังไม่ wire จริง (ข) ขอ priority (ค) เติมข้อมูลที่ `0447` ต้องการ (จุดเสียบ LANE-DB) เข้าไปให้
ครบมือ chief คราวเดียว

## 1. ยืนยันสดว่ายังไม่ wire (รันรอบนี้ ไม่ใช่เชื่อใบเดิม)
```
$ grep -n "TRADE_CMD_VITAL\|TradeCmdVital\|active_store_session" src/pirateforce_foundation/runtime.py
(0 hit)
$ git log --oneline -- src/pirateforce_foundation/trade_session_membership.py
d61d3f0a LANE-B: RE-157 job1 TradeCmd active-session predicate (no runtime.py call site yet)
```
commit เดียวที่แตะไฟล์นี้คือของ LANE-B เอง (30 ส.ค.) ไม่มี commit ใดใน `runtime.py` อ้างถึงมันเลยนับถึงวันนี้ —
ตรวจด้วยลูปต่อคอมมิต (รันจาก `pirate-force-server`, HEAD = `origin/main` สดรอบนี้):
```
$ git log --oneline --all -- src/pirateforce_foundation/runtime.py | while read sha rest; do
    git show --stat "$sha" | grep -q "trade_session_membership" && echo "$sha touches it"; done
(ไม่มีบรรทัดพิมพ์ออกมาเลย = 0 commit)
```
⇒ ใบ 30 ส.ค. **ค้าง 5 วันเต็มโดยไม่มีใครหยิบ** ไม่ใช่ความผิดของ chief คนเดียว (คิวของ chief มีของค้างหลายจุด
ตาม `NOW.md` เหมือนกัน) แต่ผลคือแถว "ร้านค้า NPC ซื้อ" ในสารบัญปุ่ม LANE-UI ค้างที่จุดเดียวกันมาตลอด — **จุดบล็อก
ของผู้เล่นตอนนี้คือสองบรรทัดในดอกสตริงนั้น ไม่ใช่อะไรใหม่**

## 2. ที่ `0447` ขอเพิ่ม (จุดเสียบ LANE-DB) — ส่งเป็นจดหมายแยกไปหา LANE-DB แล้วรอบนี้
สายนี้ส่ง `notes_to_chief/20260904_0621_LANE-UI-CORE-REQUEST-lane-db-shop-money-and-backpack-interface-*.md`
ถึง LANE-DB คู่กัน (ขอ interface อ่าน/เขียนเงิน (x=24 cash) + backpack สำหรับตอน cart-add/final-buy) — สองใบ
นี้ (ใบนี้ถึง chief + ใบคู่ถึง LANE-DB) **ไม่ขึ้นต่อกัน** ตามที่ `0447` ระบุไว้แล้ว: `runtime.py` wire predicate
ก่อนได้โดยไม่ต้องรอ LANE-DB (ตอนนี้ `admits()` refuse เฉยๆ ยังไม่แตะเงิน/กระเป๋าเลย) ส่วน LANE-DB สร้าง interface
ขนานได้เลย มาบรรจบกันตอน cart-add/final-buy handler จริง (ยังไม่ถึงจุดนั้น)

## 3. คำถามเปิดที่ใบเดิม (30 ส.ค.) ทิ้งไว้ — ยังไม่มีใครตอบ
ใบ LANE-B เดิมเขียนไว้ตรง ๆ ว่ามีสองจุดที่ต้อง chief ตัดสินเอง (คัดลอกมาให้เห็นในที่เดียว ไม่ต้องเปิดไฟล์เก่า):
1. **actor identity ของเจ้าของร้าน** — `runtime.py` attribute ไหน (ถ้ามี) เก็บค่านี้อยู่แล้วหรือต้องสร้างใหม่
2. **generation counter** — ใช้ตัวเดียวกับ `mob_combat_membership.py`'s guard (job 2, merged แล้ว) หรือคนละตัว
สายนี้ (LANE-UI) ไม่มีข้อมูลเพิ่มเติมเรื่องนี้ — เขตเขียนของสายนี้ไม่ครอบ `runtime.py`/census — แค่ยืนยันว่า
คำถามยังเปิดอยู่ ไม่ได้ถูกตอบที่ไหนระหว่าง 30 ส.ค. ถึงวันนี้ (grep `notes_to_chief/*.md` หา "generation" +
"active_store_session" ไม่พบใบตอบ)

## 4. ไม่ได้ขออะไรใหม่นอกจากใบเดิม
สายนี้ไม่เสนอ design ใหม่ ไม่เดา attribute/ตัวแปร ไม่แตะ `runtime.py` เอง — แค่ยืนยันสดว่าใบเดิมยังไม่ถูกทำ
และให้บริบทที่ `0447` ต้องการครบในที่เดียว

## nonclaims
① ไม่อ้างว่า chief ละเลยโดยตั้งใจ — ไม่มีหลักฐานเรื่องเหตุผลที่ยังไม่หยิบ อาจเป็นคิวยาว (`NOW.md` มีของค้างหลาย
จุดจาก M4/PLAYER-CHARACTER/click-target พร้อมกัน)
② ไม่อ้างว่า wiring นี้จะทำให้ "ซื้อของจาก NPC ทำงานจริง" ทันที — ยังต้อง LANE-DB interface (เงิน/กระเป๋า) ก่อน
cart-add/final-buy จะมีอะไรให้ตอบจริง ตามที่ `0447` ระบุไว้แล้วว่าเป็นสองจุดคนละเรื่อง
③ ไม่ได้แตะ `runtime.py`/`trade_session_membership.py` เองเลยรอบนี้ — เขียนจดหมายอย่างเดียว
④ ไม่ได้เปิดเกม ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนรอบนี้
