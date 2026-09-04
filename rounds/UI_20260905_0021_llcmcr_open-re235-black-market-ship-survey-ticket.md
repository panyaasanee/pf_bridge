# LANE-UI round `llcmcr` — เขียนเนื้อใบ RE-235 (ตลาดมืด/หน้าต่างเรือ) ลง CLIENT_RE_QUEUE.md

เวลา: 2026-09-05 00:21 +07:00 (`TZ=Asia/Bangkok date`)

## รอบนี้ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
**ไม่ขยับ M-ladder** (M2 คงเดิม — ตัวบล็อกเดียวที่เหลือคือ chief แก้หัวใบ `GT-233` ซึ่งไม่ใช่ของสายนี้) · รอบนี้เดินคิว
ข้อ 1 ของ LANE-UI ต่อ (สารบัญปุ่ม/ฟังก์ชันนอกระบบหลัก) — ปิดช่องว่างที่ chief จองเลขไว้ตั้งแต่รอบ `wjqykr`/R338
(`RE-235`) ด้วยเนื้อใบจริง ไม่ใช่โค้ดที่แก้บันไดไมล์สโตนโดยตรง

## ลำดับตาม §7
1. `git fetch origin main` ทั้งสองรีโป (bridge `2eaecf8` · server `bc65818`) · `checkout -B claude/wizardly-knuth-llcmcr`
   จาก `origin/main` · list PR เปิดหัว `[LANE-UI]` ทั้งสองรีโป (`mcp__github__search_pull_requests`) — **ไม่มี** ⇒
   ไม่ต้องถอย · claim ที่ `pf_bridge` เท่านั้น: PR `#1230` หัว `[LANE-UI] round llcmcr: claim`
2. รอบก่อน (`5u9bio3`) ปิด `ADVERSARY_PENDING` ของตัวเองแล้วในไฟล์รอบ (`pf_bridge#1221` รอบสอง — สะอาด) — **ไม่มีอะไรค้าง
   ให้หยิบเป็นงานแรกรอบนี้**
3. กล่องจดหมาย `grep -l "ADDRESSEE: LANE-UI" notes_to_chief/*.md` ข้าม `.CONSUMED.txt` — พบสองใบ:
   - `0332` (LANE-PROMPT ต้นทาง — ยืนยันซ้ำเป็นครั้งที่ห้าแล้วว่าไม่ใช่จดหมายจริงถึง LANE-UI ตามที่รอบ
     `md7pjz`/`qwhlua`/`urhd6h`/`n4vqwx` วินิจฉัยไว้แล้วทุกรอบ ไม่สร้าง `.CONSUMED.txt` ตามเดิม)
   - **`2304`** (chief อนุมัติ exemption 4 symbol ของ `lane_ui_trade_wire_log.py` ตามที่ขอในใบ `2121` ของรอบ `yarohy`
     เอง — จดหมายเขียนตรงว่า "คุณไม่ต้องทำอะไรต่อ และไม่ต้องเปลี่ยนชื่อ" การขยายการ์ดให้ recursive เป็นงานของ chief เอง)
     ⇒ ไม่มีโค้ดให้แก้ สร้าง `.CONSUMED.txt` ทันที
4. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงาน (ครั้งที่ 1 ของเพดาน `1428` ≤2 ครั้ง) — ให้รีวิวเนื้อใบ `RE-235` ที่กำลัง
   จะเขียน (ข้อเท็จจริงที่อ้าง + การไม่ชนใบซ้ำ) ก่อน push จริง — ดูหัวข้อ ADVERSARY ด้านล่าง

## ทำอะไร
### เขียนเนื้อใบ `RE-235 BLACK-MARKET-AND-SHIP-SURVEY-WINDOW-OPCODES-001`
chief จองเลขไว้ตั้งแต่รอบ `wjqykr`/R338 ระบุตรงว่า "เนื้อใบเป็นของ LANE-UI ให้เขียนทับทั้งก้อนในรอบถัดไปของสายนั้น"
(`CLIENT_RE_QUEUE.md:4901-4904` เดิม) — บทสรุปของคำถามนี้มีอยู่แล้วจากใบต้นทาง `notes_to_chief/20260904_1137_*.md`
(วัดสามรอบติดมาก่อนแล้ว: `c2a7nc`/`p7m2wq`/`h4wnbz`) แต่ยังไม่เคยลงเป็นเนื้อใบจริงในไฟล์คิว — รอบนี้ re-derive ข้อเท็จ
จริงหลักสองข้อซ้ำเอง (ไม่ก๊อปเลขเก่ามาโดยไม่เช็ค ตามบทเรียนของโปรเจกต์):
- `grep -in "blackmarket"` และ `grep -in "requestsurvey"` บน `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — ยัง
  **0 hit ทั้งคู่** (ไม่เปลี่ยนจากที่วัดไว้ก่อนหน้า)
- `grep -n "^GSCN_BlackMarket\|^NavigationEx_RequestSurveyVtial" external/PF_SERIALIZER_FIELDS.tsv` — **104 บรรทัด**
  (แถวฟิลด์ของทั้ง 7 คลาสยังอยู่ครบ)

เขียนเนื้อใบเต็มทับบล็อกจองที่ `CLIENT_RE_QUEUE.md` (คำถาม · กันสับสนกับ M2 · ค้นก่อนถอด 4 ข้อ · ตารางฟิลด์/opcode
7 คลาส · สรุป · ลำดับความสำคัญของ capture · route/ห้ามอ้าง/ลิงก์ · ช่อง `result:` ว่างรอ) — เปลี่ยนหัวใบจาก
`PENDING (RESERVED)` เป็น `OPEN` พร้อมป้ายเส้นทาง `[NEEDS-ATTENDED-CAPTURE]` ตาม §18 (เพิ่มจาก `[OPEN — assigned
LANE-UI]` ไม่ใช่แทนที่ — รูปแบบเดียวกับ `RE-234`)

รันเครื่องมือบังคับตาม `PROCESS_GATES.md` §18/R298 หลังแก้ไฟล์นี้: `python3 tools_bridge/pf_re_queue_taglint.py`
→ **`RESULT: 0 ticket(s) the RE runner cannot select`** (RE-235 ไม่อยู่ใน 13 หัวใบเก่าที่ตัวเครื่องเตือนแยกต่างหาก
ว่า "ตอบแล้วแต่หัวยังไม่ปิด" — ใบเหล่านั้นไม่ใช่ของ LANE-UI และไม่ใช่ของรอบนี้)

## ADVERSARY
`pf-adversary` ครั้งที่ 1 ของเพดาน `1428` สั่งต้นรอบพร้อมเริ่มงาน ให้ตรวจ: (1) re-derive ตัวเลข/ผล grep ที่อ้างเอง
ไม่เชื่อของที่ให้มา (2) เช็คว่าเนื้อใบไม่ชนใบเปิดอื่นที่ซ้ำ (3) เช็คว่าไม่ทับเนื้อหาอื่นที่ไม่ควรทับรอบ `CLIENT_RE_QUEUE.md`
(4) ประโยคปฏิเสธทุกประโยคมี grep กำกับ — **ผลยังไม่คืนตอน push** ⇒ บันทึก `ADVERSARY_PENDING <PR#>` ด้านล่าง ตาม
กติกา `1428`/`0903_2345` (push ตามเดิม ห้ามถือล็อกรอ ห้ามเขียนว่า "ผ่าน adversary" ก่อนผลคืน)

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `#1230` (`[LANE-UI] round llcmcr: claim`, กิ่ง `claude/wizardly-knuth-llcmcr`) — แก้
  `CLIENT_RE_QUEUE.md` (เนื้อใบ `RE-235`) + `.CONSUMED.txt` ของใบ `2304` + ไฟล์รอบนี้ (แทน `_claim.md`)
- **ไม่มี PR เซิร์ฟเวอร์รอบนี้** — ไม่แตะโค้ด `src/`/`tests/` เลย (งานรอบนี้เป็นเนื้อใบคิวล้วน)
- ไม่มี GT ใหม่ · RE-235 คือใบที่เปิดเนื้อจริงรอบนี้ (เลขตั้งไว้ก่อนแล้วโดย chief) · ไม่มีเลข CORE-REQUEST ใหม่

## nonclaims
① ไม่ยืนยันว่า `NavigationEx_RequestSurveyVtial` ฟิลด์ครบ = แปลว่ารู้ semantic ของฟิลด์นั้นแล้ว — รู้แค่ shape/
ค่าคงที่ (`RE-086`/`RE-087`) ไม่รู้ว่าคำสั่งทำอะไรจริงในเกม
② ไม่ยืนยันว่า `GSCN_BlackMarketSearchMyItem` ที่ field `EMPTY` ทั้งคู่เป็นคลาสที่ยังใช้งานจริงในบิลด์นี้ — อาจเป็น
dead code หรือ derive ค่าจากที่อื่น ไม่มีข้อมูลพอสรุป (ยกมาจากใบต้นทาง `1137` nonclaim①)
③ ไม่ได้ประเมินว่า chief/ทีม static ควรรัน string-extraction รอบใหม่ครอบคลุม 519 คลาสไหม — เสนอไว้เป็นทางเลือกใน
เนื้อใบเฉย ๆ ไม่ใช่คำขอ
④ ไม่มีไบต์ใหม่ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ ไม่แตะโค้ด ไม่เดา opcode แล้วส่ง

## งานสำรอง (พร้อมเริ่มได้ทันทีรอบถัดไปถ้างานหลักติด — ตาม `PANYA 1450` ข้อ 6)
1. เขียนเนื้อใบ `RE-237 OPTIONS-APPLY-SERVER-SETTING-VITAL-FIELDS-001` (`CLIENT_RE_QUEUE.md:4987`, ยัง
   `PENDING (RESERVED)`, เจ้าของ/ผู้เขียน = LANE-UI เหมือน `RE-235`) — บทสรุปมีอยู่แล้วในใบต้นทาง
   `notes_to_chief/20260904_1054_LANE-UI-RE-TICKET-options-apply-server-setting-vital-fields-need-dynamic-capture.md`
   (5/6 ฟิลด์ resolved จาก static, ฟิลด์ 3 + ทิศตรงข้ามของ 1/2/6 ต้อง dynamic capture) — หลักฐานผ่าน: หัวใบ
   `RE-237` เปลี่ยนจาก `PENDING (RESERVED)` เป็น `OPEN` พร้อมป้าย `NEEDS-ATTENDED-CAPTURE`
2. เช็คว่า ka1-A รันกิ่งทิ้ง `HYP-PF-040` (`pirate-force-server` commit `e678a376a274f5ba3d1f3e30e86bf1c43df1047c`,
   push โดยรอบ `yarohy`) แล้วหรือยัง — `grep -l "KA1A" notes_to_chief/*.md` ใหม่ที่พูดถึง `GT-184`/`GT-186`/
   `HYP-PF-040` — หลักฐานผ่าน: มีจดหมายผลใหม่ ⇒ รายงาน COO ตามข้อ 4 ของ `2047` ทันที (ไม่ว่าผลจะเป็นบวกหรือลบ)
3. เช็ค CORE-REQUEST `0621` (LANE-DB เงิน/กระเป๋าสำหรับร้านค้า NPC ซื้อ) มีอินเทอร์เฟซใหม่จาก LANE-DB หรือยัง —
   `grep -l "LANE-DB"` ใหม่ล่าสุดใน `notes_to_chief/` (ล่าสุดที่เช็คแล้ว: งาน piece 3-5 ของ PLAYER/CHARACTER +
   scene-select fix ยังไม่ถึงคิวร้านค้า) — หลักฐานผ่าน: มี interface ใหม่ ⇒ กลับมาต่อสาย `TradeCmdVital` ทันที

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
1. เปิด PR `#1230` ดูผล `pf-adversary` ที่ค้าง (`ADVERSARY_PENDING`) เป็นงานแรกก่อน claim ใหม่ใด ๆ
2. เช็คงานสำรองข้อ 1-3 ข้างบนตามลำดับ
3. ถ้า `RE-235`/`RE-237` ทั้งคู่มีผล capture กลับมาแล้ว กลับไปไล่ RE ที่เหลือของสารบัญ (stall/guild storage/
   black-market สองคลาสฟิลด์ยังไม่ครบ) ทีละใบ

— LANE-UI รอบ `llcmcr`
