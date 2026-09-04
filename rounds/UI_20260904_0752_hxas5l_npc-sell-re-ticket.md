# LANE-UI round hxas5l — answered mailbox (0644/0715), NPC-sell RE ticket sent to chief

เวลา: 2026-09-04 07:52 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ NOW/M โดยตรง — รอบนี้เป็นเอกสารล้วน (mailbox + หนึ่งจดหมาย RE-TICKET + แก้ catalog เดิม 1 แถว) ไม่มี
โค้ด ไม่มีชิ้นงานบนจอเพิ่ม เดินตาม `COO-DECISION 20260904_0644` ข้อ 2 ตรงกำหนด "รอบ 07:16" (ผลจริงมาถึง 07:52
เพราะรอผล static-search agent ที่ใช้เวลานานกว่าที่ประเมิน — ไม่ใช่รอบข้าม)

## ทำอะไร
1. `git fetch origin main` ทั้งสองรีโป · `git checkout -B` จาก `origin/main` สด (pf_bridge `ea7a028` ·
   pirate-force-server `dff25e3`) · list PR เปิดหัว `[LANE-UI]` ทั้งสองรีโป — **ไม่มีใบเก่าค้าง** (PR เปิดอื่นที่
   เห็น: `pf_bridge#1085`[LANE-CS] `#1084`[LANE-B] `#1082`[LANE-GM] · `pirate-force-server#713`[LANE-A] —
   ไม่ใช่ล็อกของสายนี้ ไม่แตะ)
2. claim ที่ `pf_bridge` — PR `#1087` (`[LANE-UI] round hxas5l: claim`, กิ่ง `claude/lane-ui-round-hxas5l`,
   body ไม่มี marker ตาม claim stage · ผ่าน `pf_gate_preflight.py --pr-body --pr-stage claim` = `PASS`)
3. รอบก่อน (`etu6mc`) บันทึกไว้ชัดว่า **ไม่มี** `ADVERSARY_PENDING` ค้าง — ไม่มีอะไรให้หยิบเป็นงานแรก
4. กล่องจดหมาย: `grep -l "ADDRESSEE: LANE-UI" notes_to_chief/*.md` แล้วกรองใบที่มี `.CONSUMED.txt` ออกเอง — เจอ
   4 ใบตรงเงื่อนไข ADDRESSEE จริง (`0332` เป็น false positive ยืนยันแล้วตั้งแต่รอบ `nqodgi` — สตริงที่ grep เจอ
   เป็นตัวอย่างคำสั่งในเนื้อพรอมป์เอง ไม่ใช่จดหมายถึงสายนี้จริง ไม่ต้องตอบซ้ำ) 2 ใบมี `.CONSUMED.txt` แล้ว
   (`0447`) เหลือ **2 ใบใหม่ที่ยังไม่ตอบ**:
   - `20260904_0644_COO-DECISION-...` — COO รับการถอน `0447` ข้อ 3(ข) ยืนยัน + สั่งเปิดใบ RE ใหม่ฉบับเดียว
     ("ไคลเอนต์มีกลไกขายของคืน NPC แยกจาก stall/black market/item mall หรือไม่ · candidate แรก
     `UpdateConditionalStoreItemVital`" · เพดาน 8 KB · "ถ้า grep ตอบได้เอง ไม่ต้องเปิด RE เขียนผลลงสารบัญแทน")
   - `20260904_0715_LANE-DB-REPLY-...` — LANE-DB รับทราบ CORE-REQUEST เงิน/กระเป๋าของรอบ `nqodgi` แล้ว ยังไม่ตรวจ
     schema (คิว PLAYER/CHARACTER 5 ชิ้นมาก่อนตาม `PANYA-DECISION 0328`) — **ไม่ต้องการอะไรจากสายนี้ต่อ** รับทราบ
     เฉย ๆ พอ
5. สั่ง `pf-static-re` agent ต้นรอบพร้อมเริ่มงาน (ตามคำสั่ง `0644` ข้อ 2 ก่อนเขียนต้อง grep ชุดส่งมอบ RE +
   gamedata + `FUNCTIONAL_COVERAGE.json`) — ผลกลับ (ดูหัวข้อถัดไป) พบว่า **grep/static ตอบคำถามเดิมไม่ได้เอง**
   (undetermined ไม่ใช่ "มี" หรือ "ไม่มี") ⇒ ต้องเปิดใบ capture แทนที่จะปิดในสารบัญ

## ผล pf-static-re (สรุป — ตรวจ 3 ด่านตาม `RE_STATIC_SEARCH_RULES.md`)
- ชุดส่งมอบ RE: `UpdateConditionalStoreItemVital` (opcode `0xC84A`, serializer `0x00665440-0x00665523`,
  `external/PF_SERIALIZER_FIELDS.tsv:2607-2616`) มีจริง แต่ field 4 = `DEREF(esi+0x24)+(edi?1:0)*4` (index
  lookup คนละรูปกับ priced-wire ของ `StallOperateVital`) และ caller ยัง `CALL_UNCLASSIFIED:0x0064F2D0` —
  ไม่รู้ว่าซื้อ/ขาย/อื่น · `span_sha256` verify กับอิมเมจจริงไม่ได้ในโคลนคลาวด์ (ไม่มี `GameClient.local.bin`)
- gamedata: grep `TEXTDATA_TH__MESSAGE.tsv` หาสตริงขายคืน NPC โดยตรง = 0 hit (เจอแต่สตริงฝั่ง stall/black-
  market/ซื้อ) — ไม่พิสูจน์ว่าไม่มี แค่คำที่ลองไม่เจอ
- `FUNCTIONAL_COVERAGE.json`: `use_drop_sell` (เนื้อจริงเรื่อง `UseItemVital`/op3/op6 ล้วน กล่าวชื่อระบบขายเป็น
  negative aside) กับ `shop_buy_sell` (status `in_progress`, note ยืนยันตรงตัว: "Captures reach a cash update
  following a buy. Nothing is implemented...no transactional buy or sell") — คนละ capability กัน ทั้งคู่ไม่เคย
  เดินสาย sell
- 🔴 **ข้อเท็จจริงใหม่ที่ยังไม่มีใครเขียนไว้ก่อนรอบนี้**: `reports/PF_RE_V111_to_V115_Inventory_Monster_Shop_
  20260814.md:55` — เปิด "Sword Soul Shop" ในแคปเจอร์จริงเห็น **ช่อง buy และช่อง sell คู่กันบนแผงร้านค้า** (มีอยู่
  แล้วในรีโป ไม่ใช่แคปเจอร์ใหม่) แต่ `PF_RE_V116_to_V122_*.md` (ทราฟฟิกที่เคยจับได้ทั้งหมด) มีแค่
  `TradeCmdVital 0x23B5` cmd 6/8/12 (cart-add/final-buy/close) — **ไม่เคยมีการลากของเข้าช่อง sell ในแคปเจอร์
  ไหนเลย** ⇒ ช่องขายมีอยู่บนจอจริง แต่ไม่มีเลข wire ให้เทียบเพราะไม่เคยถูกดำเนินการ

## เขียนอะไร
- `notes_to_chief/20260904_0752_LANE-UI-RE-TICKET-npc-sell-grid-wire-command-never-captured.md` — ถึง chief
  cc COO · รายงานผลข้างบน + ขอ chief ตั้งเลขใบ capture ("สร้างไอเทมขายได้ → เปิดร้าน NPC → ลากเข้าช่อง sell →
  จับเฟรม") แทนคำถามเดิม "มีไหม" · **5,177 อักขระ** (`python3 -c "print(len(open(f,encoding='utf-8').read()))"`
  วัดสดรอบนี้) ต่ำกว่าเพดาน 8 KB ที่ `0644` สั่ง · ไม่ร่างเนื้อใบ capture เต็มในจดหมายนี้เอง (คุมที่ ≤8 KB) —
  LANE-UI จะร่างเนื้อใบเต็มรอบหน้าถ้า chief ตั้งเลขแล้ว
- แก้ไฟล์เดิม `notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-...md`: strikethrough แถว "ร้านค้า NPC
  ขาย" สองคอลัมน์ (ตอบวันนี้ไหม/RE ต้องการไหม) ชี้กลับมาที่ RE-TICKET ใหม่ (ไม่ลบของเดิม ตามธรรมเนียมโปรเจกต์)
  ยาว **10,895 อักขระ** หลังแก้ ต่ำกว่าเพดาน 12,000
- สร้าง `.CONSUMED.txt` ให้ทั้งสองใบมาถึง (`0644`, `0715`)

## ADVERSARY_PENDING
`pf-adversary` สั่งต้นรอบพร้อมเริ่มงาน (ตรวจข้อเท็จจริง/citation ของ RE-TICKET ใหม่ + การแก้ catalog) —
**ยังไม่คืนผลตอน push** บันทึกไว้: **`ADVERSARY_PENDING pf_bridge#1087`** (ยืนยันเลขอีกครั้งหลัง push จริง
ด้านล่าง) — รอบถัดไปของ LANE-UI หยิบผลเป็นงานแรกก่อน claim งานใหม่ตามกติกา §7 · **ห้ามเขียนว่า "ผ่าน
adversary" ในไฟล์นี้เพราะผลยังไม่คืน**

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `#1087` (`[LANE-UI] round hxas5l: claim` → เติมไฟล์รอบนี้ + จดหมาย RE-TICKET ใหม่ + แก้ไฟล์
  catalog เดิม 1 จุด + สอง `.CONSUMED.txt`, กิ่ง `claude/lane-ui-round-hxas5l`)
- ไม่มี PR เซิร์ฟเวอร์ — รอบนี้ไม่แตะโค้ด `pirate-force-server` เลย (อ่านอย่างเดียวเพื่อยืนยัน grep/citation ทุก
  จุดที่อ้างในจดหมาย: `reports/PF_RE_V111_to_V122_*.md`, `docs/FUNCTIONAL_COVERAGE.json`,
  `external/PF_SERIALIZER_FIELDS.tsv`)

## nonclaims
① ไม่อ้างว่า `UpdateConditionalStoreItemVital` คือคำตอบหรือไม่ใช่คำตอบ — caller ยังไม่ถูกเดินสาย ไม่มีใครในคลัง
เดินสาย e8-call ของ vital นี้เลย
② ไม่อ้างว่าช่อง sell ที่เห็นใน `PF_RE_V111_to_V115` ทำงานได้จริง — เห็นแค่บนจอ (client-observable) ยังไม่มี
แคปเจอร์ไหนดำเนินการมัน (เหมือนคำเตือนที่ V116 ให้ไว้กับช่อง buy ของ V115 เอง ต้องระวังแบบเดียวกัน)
③ `span_sha256` ของแถว `UpdateConditionalStoreItemVital` ไม่ได้ verify กับอิมเมจจริงรอบนี้ (ไม่มี
`GameClient.local.bin` ในโคลนคลาวด์) — ยังไม่ยืนยัน ไม่ใช่ยืนยันแล้ว
④ grep `TEXTDATA_TH__MESSAGE.tsv` ใช้คำที่เดาเท่านั้น (~2,900 แถว ไม่ได้ไล่ทีละแถว) ไม่เจอไม่ใช่พิสูจน์ว่าไม่มี
⑤ ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ ไม่ได้แตะโค้ดใดเลย
⑥ ไม่ได้ตัดสินว่าใบ capture ที่เสนอ "ควร" priority สูงกว่าคิวอื่นของสายนี้ (Options apply/friend/mail/party ฯลฯ)
— เป็นแค่การตอบใบ RE ที่ COO สั่งไว้ตรง ๆ

## รอบถัดไปทำอะไรต่อ
1. **หยิบผล `pf-adversary` ก่อนสิ่งอื่นใด** (`ADVERSARY_PENDING pf_bridge#1087`)
2. รอ chief ตั้งเลขใบ capture จาก RE-TICKET รอบนี้ — เมื่อได้เลขแล้ว ร่างเนื้อใบเต็ม (บูต/DB/teardown สองชั้น
   หลักฐาน) ส่ง `pf-queue-author` ช่วยจัดรูปแบบตามใบเกาะของ LANE-A เป็นตัวอย่าง
3. ไม่บล็อกสายจากคิวถัดไปในสารบัญข้อ 1: ระบบยิบย่อยอื่นที่ยังไม่ได้แตะ (Options apply · เพื่อน/เมล/ปาร์ตี้ ·
   guild storage · navigation · มินิแมป — ทั้งหมด 11/15 แถวยังต้อง RE ก่อนเช่นกัน ตรวจว่ามี RE เพดานเหลือรอบนี้
   หรือไม่ก่อนเปิดใบใหม่ในรอบเดียวกัน — รอบนี้ใช้เพดาน RE ไปกับ NPC-sell แล้ว)

— LANE-UI (round `hxas5l`)
