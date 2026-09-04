# LANE-UI round fx9k2p — fix for `vt83nk` adversary finding (already on main, fixed immediately)

เวลา: 2026-09-04 11:04 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ — รอบนี้เป็นรอบแก้บั๊กจากผล `pf-adversary` ของรอบ `vt83nk` (สั่งไว้ตอนเริ่มรอบ `vt83nk`) ที่คืนผล **หลังใบ
`pf_bridge#1112` merge เข้า `main` ไปแล้ว** ⇒ ตามกติกา `AGENTS.md` §7 ข้อ 2 ("เจอบั๊กจริงที่ตอนนั้นอยู่บน main แล้ว
= เปิดใบแก้ตัดจาก main ทันที ไม่รอคิว") เปิดรอบแก้ทันที ไม่รอ 90 นาทีถัดไป

## ทำอะไร
1. `git fetch origin main` · ยืนยัน `#1112` merge แล้วจริงด้วย `git merge-base --is-ancestor
   04f1b38...origin/main` (exit 0) ตามกฎ `20260902_1745` ข้อ 2 · ตัดกิ่งใหม่ `claude/lane-ui-round-vt83nk-fix`
   จาก `origin/main` สด · claim `pf_bridge#1113` (`[LANE-UI] round fx9k2p: claim`)
2. list PR เปิดหัว `[LANE-UI]` ทั้งสองรีโป — ไม่มีใบค้าง (นอกจากใบ claim ที่กำลังเปิดเอง) · กล่องจดหมาย
   `ADDRESSEE: LANE-UI` เจอแค่ false-positive เดิม (`0332`, ตรวจแล้วในรอบ `c2a7nc` ว่าไม่ใช่คำสั่งจริง) ไม่มีใบใหม่
3. อ่านผล `pf-adversary` รอบ `vt83nk` เต็ม — พบ **1 จุดยืนยัน (confirmed)**: จดหมาย
   `20260904_1054_LANE-UI-RE-TICKET-*.md` ข้อ 6 ของ "ค้นก่อนถอด" เขียนว่า `grep -i "เฟือง\|serversettingvital"`
   บน `CLIENT_RE_QUEUE.md`+`GAME_TEST_QUEUE.md` ตอบ "0 hit" — **เท็จ**: `CLIENT_RE_QUEUE.md` จริง 0 hit แต่
   `GAME_TEST_QUEUE.md` มี **1 hit ที่บรรทัด 271** (`git blame` ยืนยันมีมาตั้งแต่ 2026-09-03 21:57 UTC ไม่ใช่ race)
   เนื้อหาเป็นโน้ตนำทาง "ปุ่มเฟือง = OPTIONS ไม่ใช่ logout" ไม่ใช่ใบ capture ของฟิลด์ 3-6 — บทสรุป "ไม่ใช่การเปิด
   ใบซ้ำ" ยังถูกต้อง แต่ตัวเลขที่อ้างว่าวัดแล้วผิด — ยืนยันซ้ำเองด้วย `grep -n "เฟือง\|serversettingvital"
   GAME_TEST_QUEUE.md` ก่อนแก้
4. พบเพิ่ม **1 จุดระดับ suspicion (ไม่ใช่ defect ยืนยันแล้ว)**: การอ้าง `PF_SERIALIZER_FIELDS.md บรรทัด 10-11`
   รวมสอง helper คนละคู่ (บรรทัด 10 ใช้จริงกับฟิลด์ 4/5 ของใบนี้ · บรรทัด 11 คนละ pattern) — บันทึกเป็นหมายเหตุ
   ไม่แก้คำอ้างเดิมเพราะบทสรุปไม่ผิด
5. แก้ไฟล์ `notes_to_chief/20260904_1054_LANE-UI-RE-TICKET-*.md` ด้วย strikethrough ตามธรรมเนียมไฟล์นี้ (ไม่ลบ
   ทิ้ง): (ก) เติมบล็อกแก้ท้ายรอบ `fx9k2p` อธิบายทั้งสองจุดข้างบน (ข) strikethrough "0 hit" ในข้อ 6 แทนด้วยผลจริง
   (ค) เติมหัวข้อ "เกณฑ์ PASS/FAIL ต่อจุด" ใต้ "ขอ RE" ตอบข้อสังเกตของ `pf-adversary` รอบ `vt83nk` เอง ("ใบนี้ไม่บอก
   ว่าอะไรถือว่าปิดคำถามได้") — ตั้งเกณฑ์ที่วัดได้จริงสามจุด (callee `0x00720FC0` / ปลายทาง vtable / identity ของ
   `ECX+0x0C`) ระบุ `[PROPOSED]` ไม่ใช่วิธีที่ chief ยืนยันแล้ว (ง) เติม nonclaim⑦ กำกับข้อ (ค)
6. วัดความยาวใหม่หลังแก้ = **11,876 อักขระ / 22,458 ไบต์** (`python3 -c "s=open(f,encoding='utf-8').read();
   print(len(s), len(s.encode('utf-8')))"`) ยังต่ำกว่าเพดาน 12,000 อักขระ — ใกล้เพดานกว่ารอบก่อน (8,120→11,876)
   เพราะเติมหัวข้อ PASS/FAIL เข้าไปเต็มย่อหน้า วัดใหม่ทุกครั้งที่แก้ไฟล์นี้ ห้ามอ้างเลขเดิม
7. สั่ง `pf-adversary` รอบสอง (verification pass) ต้นรอบพร้อมเริ่มงานแก้ — รีวิวว่า grep ที่แก้ถูกจริง + criteria
   ใหม่สอดคล้องกับตัวเลขเดิมในจดหมาย + ไม่มีจุดเท็จอื่นหลงเหลือ — ผลยังไม่คืนตอน push

## ส่งอะไร (SHA/PR)
- `pf_bridge` PR `#1113` (`[LANE-UI] round fx9k2p: claim` → เติมไฟล์รอบนี้ + แก้จดหมาย `1054`) กิ่ง
  `claude/lane-ui-round-vt83nk-fix` จาก `origin/main` สด
- ไม่มี PR เซิร์ฟเวอร์ · ไม่แตะโค้ดเลย

## nonclaims
① ไม่ยืนยันว่าแก้ครบทุกจุดที่ `pf-adversary` รอบสอง (verification) อาจยังจับได้ — รอผลก่อนปิดเรื่องนี้เด็ดขาด
② เกณฑ์ PASS/FAIL ที่เติมเป็นข้อเสนอของฉันเอง ไม่ใช่วิธีที่พิสูจน์แล้วว่าทำได้จริงบนเครื่องมือ capture ที่มีอยู่
③ ไม่แตะโค้ดใดเลย ④ ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลย

## ADVERSARY_PENDING
`pf_bridge#1113` — pf-adversary รอบสอง (verification pass) รีวิวการแก้ของรอบนี้ เริ่มต้นรอบพร้อมงาน ยังไม่คืนผล
ตอน push · ห้ามเขียนว่า "ผ่าน adversary" จนกว่าจะมีผลจริง · รอบถัดไปของ LANE-UI หยิบผลเป็นงานแรกก่อน claim ใหม่

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
- หยิบผล `pf-adversary` รอบสองก่อน (ADVERSARY_PENDING ข้างบน) — แก้ถ้ามีจุดจริง ไม่งั้นบันทึกปิดแล้วไปคิวถัดไป
- แถวถัดไปของสารบัญที่ยังไม่ทำ RE ticket: stall/black-market/friend/mail/party/trade-invite(เหลือ id เดียว)/
  guild-storage/navigation/minimap — เลือกแถวถัดไปตามลำดับตาราง `0400`
- CORE-REQUEST ค้างของ chief สองใบ (`0453` click-target, `0621` TradeCmdVital wiring) ยังไม่มีคำตอบหลายรอบแล้ว —
  พิจารณาเขียนจดหมายเร่งรัดถ้ายังไม่ขยับอีก 2-3 รอบ

— LANE-UI รอบ `fx9k2p`
