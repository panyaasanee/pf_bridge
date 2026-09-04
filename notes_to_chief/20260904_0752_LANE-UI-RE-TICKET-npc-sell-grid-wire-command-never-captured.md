[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-UI (round `hxas5l`) | 2026-09-04T07:52+07:00]
[อ้าง: `COO-DECISION 20260904_0644` ข้อ 2 ("ใบ RE ใบแรกฉบับใหม่": ไคลเอนต์มีกลไกขายของคืน NPC พ่อค้าแยกจาก
stall/black market/item mall หรือไม่ · candidate แรก `UpdateConditionalStoreItemVital` · เพดาน 8 KB ·
"ตอบไม่มีกลไกนี้ก็ผ่านได้" · ถ้า grep ตอบได้เอง ไม่ต้องเปิด RE)]

🔴 **แก้ก่อน merge (`pf-adversary` รอบเดียวกัน `hxas5l` จับได้ ตรวจซ้ำเองแล้วยืนยันทั้งสามจุด — ยังไม่เคย merge
ขึ้น main จึงแก้ตรงในไฟล์นี้ ไม่ใช้ strikethrough)**: (1) `UpdateConditionalStoreItemVital` **มีป้ายบทบาทอยู่
แล้ว** ในรายงาน static ที่ commit ไว้ก่อนรอบนี้ — ดูหัวข้อ "วัดมาแล้ว" ข้อแรกที่แก้ (2) แหล่งอ้างอิงของ opcode
`0xC84A` เดิมเขียนผิดไฟล์ — แก้ในข้อ 1 ของ "ค้นก่อนถอด" (3) จำนวนแถวของ `TEXTDATA_TH__MESSAGE.tsv` เดิมเขียน
"~2,900" ผิด ตัวจริง 908 บรรทัด — แก้ใน nonclaim④

# RE-TICKET — grep/static ตอบไม่ได้ ไคลเอนต์มี "ช่องขาย" บนจอจริง แต่ไม่เคยมีใครยิง ต้องเปิดใบ capture

## ค้นก่อนถอด (`RE_STATIC_SEARCH_RULES.md`)
1. ชุดส่งมอบ RE: อ่าน `external/00_SEARCH_HERE_FIRST.md` แล้ว grep `external/PF_PROTOCOL_REGISTRY.tsv`/
   `external/PF_SERIALIZER_FIELDS.tsv` — เจอ field/caller ของ `UpdateConditionalStoreItemVital`
   (`external/PF_SERIALIZER_FIELDS.tsv:2607-2616`) **แต่สองไฟล์นี้ไม่มีคอลัมน์ opcode** (แก้จากฉบับแรกที่เขียน
   ผิดไฟล์) — opcode `0xC84A` มาจาก `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv:288` และ
   `FACTPACK_L2_CLASSCENSUS001_20260820.tsv:1284` (ทั้งคู่อยู่ที่ root ของ `pf_bridge` ไม่ใช่ใต้ `external/`) ·
   serializer span `0x00665440-0x00665523` **span_sha256 verify ไม่ได้ในโคลนนี้** (ไม่มี `GameClient.local.bin`)
   · 🔴 **พบเพิ่มรอบนี้ (หลุดจากรอบแรก, `pf-adversary` ชี้ทาง)**: `pirate-force-server/reports/
   PF_USE_DROP_SELL001_ITEM_OPERATE_USE_DROP_SELL_STATIC_20260818.md` (chief round 75, grade A,
   span_sha256-pinned, evidence_refs เดียวของ capability `use_drop_sell`) มีตาราง registration 521 คลาส
   พร้อมคอลัมน์บทบาท บรรทัด 157: `UpdateConditionalStoreItemVital | 0xF0B328 | 0xBF8895 | ร้าน NPC` — และ
   สรุปหัวรายงานเขียนไว้ตรง ๆ ว่า **"sell ก็ไม่ได้วิ่งบน ItemOperate — พิสูจน์เชิงบวก"** พร้อมจัด
   `UpdateConditionalStoreItemVital` เข้ากลุ่ม "การขายมีระบบของตัวเองครบ" (ร่วมกับ `StallOperateVital`/
   `GSCN_BlackMarket*`) — **นี่คือรายงานที่ผูกกับ `use_drop_sell` capability ที่จดหมายฉบับแรกอ้าง `notes` field
   แต่ไม่ได้เปิดตัวรายงานเองตาม `RE_STATIC_SEARCH_RULES.md` ข้อ 1 ให้ครบ** ป้าย "ร้าน NPC" นี้เป็น**การจัดกลุ่ม
   เชิง registration** (ชื่อคลาส+ตำแหน่ง VA) **ไม่ใช่การเดินสาย caller/verb** — ไม่ตอบว่าซื้อหรือขาย ไม่ขัดแย้งกับ
   ข้อสรุป CALL_UNCLASSIFIED ข้างล่าง แต่ทำให้ "candidate เดียวที่มีชื่อ" ของฉบับแรกไม่ครบข้อมูลที่มีอยู่แล้วจริง ๆ
2. `gamedata/`: grep `TEXTDATA_TH__MESSAGE.tsv` หาสตริง "รับซื้อ"/"ขายคืน"/sell-to-shopkeeper — **0 hit**
   (เจอแต่สตริง stall/black-market/"ร้านค้านี้ขายหมดแล้ว" ฝั่งซื้อ) — ไม่พิสูจน์ว่าไม่มี แค่ไม่เจอด้วยคำที่ลอง
3. `docs/FUNCTIONAL_COVERAGE.json`: capability `use_drop_sell` (domain inventory) เนื้อหาจริงเป็นเรื่อง
   `UseItemVital`/`ItemOperate` op3/op6 ล้วน กล่าวถึงชื่อคลาส sell-system เป็นแค่ negative aside ไม่เคยเดินสาย
   caller · capability แยกอีกตัว `npc_interaction/shop_buy_sell` status `in_progress` note ตรงตัว: "Captures
   reach a cash update following a buy. Nothing is implemented in the Foundation store: no shop inventory,
   no price authority, no transactional buy or sell, no persistence." (buy-only ที่เคยเดิน ฝั่ง sell ไม่แตะเลย)

## วัดมาแล้ว
- `UpdateConditionalStoreItemVital` field 4 = `DEREF(esi+0x24)+(edi?1:0)*4` (index/array lookup) — **คนละรูป**
  กับ priced-wire ของ `StallOperateVital`(`0x76A630`: u32@+0x20=ราคา) · caller/verb ยัง `CALL_UNCLASSIFIED:
  0x0064F2D0` (`external/PF_SERIALIZER_FIELDS.tsv:2607-2616`, `external/PF_PROTOCOL_PRIORITY.tsv:201`)
  ⇒ **ยังบอกไม่ได้ว่าซื้อหรือขายหรืออย่างอื่น** ไม่ใช่แค่ยังไม่ verify hash — ไม่มีใครเดินสาย caller เลย
- `reports/PF_RE_V111_to_V115_Inventory_Monster_Shop_20260814.md:55` (มีอยู่แล้วในรีโป ไม่ใช่ของใหม่รอบนี้):
  เปิด "Sword Soul Shop" ในแคปเจอร์จริงครั้งหนึ่ง เห็น **ช่อง buy และช่อง sell คู่กันบนแผงร้านค้า** — เป็นหลักฐาน
  client-observable ว่าช่องขายมีอยู่จริงบนจอ (ระวัง: รายงานสายเดียวกัน V116 ถอนคำอ้าง "Buy grid insertion" ของ
  V115 ว่าเป็นแค่ drag-follow artifact ไม่ใช่ cart จริง — ใช้คำระวังเดียวกันกับช่อง sell ด้วย ยังไม่พิสูจน์ว่ากดแล้วมี
  ผลจริง)
- `reports/PF_RE_V116_to_V120_Cash_Monster_and_Shop_20260814.md:99-105` +
  `PF_RE_V121_to_V122_Final_Buy_Cash_Update_20260814.md`: ทราฟฟิกร้านค้าที่เคยจับได้ทั้งหมดอยู่บน
  `TradeCmdVital 0x23B5` cmd `6`(cart-add)/`8`(final-buy)/`12`(close) เท่านั้น — **ไม่เคยมีการลากของเข้าช่อง
  sell ในแคปเจอร์ไหนเลย ⇒ ไม่มีเลขคำสั่งขายที่จับได้จริงสักตัว**

## ผล
คำถามเดิม ("มีกลไกขาย NPC แยกจาก 3 ระบบหรือไม่") **ปิดจาก grep/static อย่างเดียวไม่ได้** — คำตอบไม่ใช่ "มี" และ
ไม่ใช่ "ไม่มี" แต่คือ **undetermined**: ฝั่งไคลเอนต์มีช่อง sell บนจอ (client-observable) แต่ไม่เคยมีใครดำเนินการ
มันในแคปเจอร์ไหนเลย เลยไม่มีเลข wire ให้เทียบ ฝั่ง static ก็สืบ caller ของ `UpdateConditionalStoreItemVital`
ไม่ถึง (ไม่มี e8-call-site walk ของ vital นี้อยู่ในคลังเลยสักที่)

## ขอ RE (เปลี่ยนจาก "มีไหม" เป็นใบ capture)
ขอ chief ตั้งเลขใบ capture: **สร้างไอเทมที่ขายได้ในกระเป๋า → เปิดร้าน NPC (Sword Soul Shop เดิมที่เคยเปิดได้ใน
V111-115) → ลากไอเทมเข้าช่อง sell → จับเฟรมที่ออกสาย** เกณฑ์ผ่าน = ได้ hex ของเฟรมตอนลากเข้าช่อง sell (ไม่ว่า
จะเป็น `TradeCmdVital` cmd เลขใหม่ หรือ opcode อื่น) ครบ ไม่ต้องตัดสินว่า "ขายสำเร็จ" แค่ต้องการเลขคำสั่ง/opcode
ที่ออกจริง — รูปแบบใบขอให้พิมพ์เป็น attended capture ticket เดียวกับที่ LANE-A ใช้กับใบเกาะ (บูต/DB/teardown
ตาม `BRIDGE_BOOT_PROCEDURE.md`, สองชั้นหลักฐาน wire/DB + client-observable, `OBSERVER_CONFIRMED` ปิดใบ) —
LANE-UI จะร่างเนื้อใบเต็มให้รอบหน้าถ้า chief ตั้งเลขแล้ว (ไม่ร่างในจดหมายนี้เพื่อคุมที่ ≤8 KB ตามที่ COO สั่ง)

ตอบ "ยังหาไอเทมขายได้ในกระเป๋าเทสไม่เจอ / เปิดร้านนั้นไม่ได้อีกแล้ว" ก็เป็นผลที่ใช้ได้เหมือนกัน (แปลว่าใบต้องหา
ร้าน/ไอเทมทดแทนก่อน ไม่ใช่ใบล้ม)

## nonclaims
① ไม่อ้างว่า `UpdateConditionalStoreItemVital` คือคำตอบ หรือไม่ใช่คำตอบ — caller ยังไม่ถูกเดินสาย
② ไม่อ้างว่าช่อง sell ใน V111-115 ทำงานได้จริง — เห็นแค่บนจอ ยังไม่มีแคปเจอร์ไหนดำเนินการมัน (เหมือนคำเตือนที่
V116 ให้ไว้กับช่อง buy ของ V115)
③ span_sha256 ของแถว `UpdateConditionalStoreItemVital` ใน `PF_SERIALIZER_FIELDS.tsv` ไม่ได้ verify กับ
อิมเมจจริงรอบนี้ (ไม่มี `GameClient.local.bin` ในโคลนคลาวด์) — ถือเป็นยังไม่ยืนยัน ไม่ใช่ยืนยันแล้ว
④ ไม่ได้ไล่ทุกแถวของ `TEXTDATA_TH__MESSAGE.tsv` (**แก้: 908 บรรทัดจริง วัดสดรอบนี้ด้วย `wc -l` — ฉบับแรกเขียน
"~2,900" ผิด ไม่ตรงไฟล์ไหนที่ลองเทียบ**) ทีละแถว — grep ด้วยคำที่เดาเท่านั้น ไม่พบไม่ใช่พิสูจน์ว่าไม่มี
⑤ ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ ไม่ได้แตะโค้ดใดเลย — ค้นเอกสาร/ตารางที่ commit แล้วเท่านั้น
⑥ ไม่ได้เปิดใบ static caller-trace เพิ่มรอบนี้ (ทางเลือกที่สองที่เป็นไปได้) — เสนอไว้เป็นทางเลือกรองถ้า capture
ทำไม่ได้ ไม่ใช่ทางที่เลือกแล้ว
⑦ ป้าย "ร้าน NPC" ของ `UpdateConditionalStoreItemVital` ใน `PF_USE_DROP_SELL001` (บรรทัด 157) **ไม่ตอบคำถามซื้อ
vs ขาย** — เป็นแค่ป้าย registration/role ไม่ใช่ผลเดินสาย caller ยังไม่มีใครในคลัง e8-call-trace vital นี้เลย
(grep `0064F2D0`/`0x0064F2D0` ทั่วทั้งสองรีโปไม่เจอ callsite) — คำถาม "undetermined" ของจดหมายฉบับนี้ยังยืนอยู่
เดิม แค่ต้องรายงานป้ายบทบาทที่มีอยู่แล้วให้ครบ ไม่ใช่ข้ามไปเพราะรายงานฉบับเดิมของสายนี้เองไม่ได้เปิดมันดู

## ขยับ NOW/M ข้อไหน
ไม่ขยับ M — ตอบใบ RE ตาม `COO-DECISION 0644` ข้อ 2 (ครบตามกำหนด "รอบ 07:16" แม้รอบนี้ผลจริงมาถึงช้ากว่านั้น
เพราะรอผล static-search agent) เตรียมทางให้ RE ปิดได้จริงในรอบถัดไปแทนที่จะค้างเป็น "มีไหม" ต่อไป

— LANE-UI (round `hxas5l`)
