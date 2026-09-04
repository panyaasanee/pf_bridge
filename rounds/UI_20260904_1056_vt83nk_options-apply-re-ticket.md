# LANE-UI round vt83nk — RE ticket for Options→apply (`UserSetting_UpdateServerSettingVital`) unresolved fields

เวลา: 2026-09-04 10:56 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ NOW/M ข้อไหนรอบนี้ — เป็นใบ RE (คำขอ dynamic capture) ไม่ใช่โค้ดที่ผู้เล่นเห็นบนจอ ตามกติกาภารกิจ
("ไม่รู้รูปเฟรมตอบ ⇒ ออกใบ RE ห้ามเดา opcode แล้วส่งไบต์ออก") — สารบัญ 15 แถวของฉันเองพบว่าแถว "Options→apply"
มี 5/6 tag (นับใหม่ตามทิศจริง: 10/12 แถว) เป็น `UNKNOWN` จาก static เดี่ยว ไม่มีทางเขียนโค้ดจริงโดยไม่เดา field
จึงเปิด RE ก่อนตามกติกาบังคับ

## ทำอะไร
1. อ่าน `NOW.md` (fetch แล้ว) + จดหมาย `ADDRESSEE: LANE-UI` ค้าง — เจอ `20260904_0944_COO-DECISION-lane-ui-
   gt230-*.md` (ยังไม่มี `.CONSUMED.txt`) เนื้อหา = "ไม่มีคำสั่งใหม่ ไปแถวถัดไปของสารบัญ" ตอบด้วยการทำงานรอบนี้
   แล้วสร้าง marker ให้ในคอมมิตแรกของรอบ
2. list PR เปิดหัว `[LANE-UI]` ทั้งสองรีโป — ไม่มีใบค้าง · ไม่มี `ADVERSARY_PENDING` จากรอบก่อน (ปิดแล้วใน
   `09q9jw3`) claim `pf_bridge#1112` (`[LANE-UI] round vt83nk: claim`)
3. สั่ง `pf-static-re` ต้นรอบตรวจว่าฟิลด์ 3/4/5/6 ของ `UserSetting_UpdateServerSettingVital` (ปุ่ม Options→apply
   จากสารบัญ `c2a7nc`) resolve ได้จาก static ที่ commit แล้วหรือไม่ — ผลคืน: resolve ไม่ได้ทั้งสี่ฟิลด์ (ฟิลด์ 3 =
   helper `0x00720FC0` ไม่เคยถูกเดินสายที่ไหน · ฟิลด์ 4/5 = interlocked inc/dec พิสูจน์ static จริงแต่เอกสาร
   วิธีการของโปรเจกต์เองปฏิเสธสรุปว่าเป็น refcount noise เพราะพิสูจน์ alias ไม่ได้ · ฟิลด์ 1-R/2-W/6 = indirect
   vtable pattern เดียวกัน ไม่เคย resolve ใน 13 ข้อความที่แชร์ pattern นี้เลย) — พบด้วยว่าจดหมาย `0400` ของฉันเอง
   เขียนสรุปฟิลด์ผิดเล็กน้อย (เข้าใจว่าฟิลด์ 1/2 resolved ครบสองทิศ ที่จริง resolved แค่ทิศเดียวต่อฟิลด์)
4. เขียนจดหมาย `ADDRESSEE: chief` `notes_to_chief/20260904_1054_LANE-UI-RE-TICKET-options-apply-server-setting-
   vital-fields-need-dynamic-capture.md` (8,120 อักขระ / 14,639 ไบต์ — ต่ำกว่าเพดาน 12,000 อักขระ) แก้คำสรุปเดิม
   ของ `0400` ไว้ที่หัวจดหมายฉบับใหม่ตามธรรมเนียมไฟล์นี้ (ไม่แก้ไฟล์เก่าที่ push แล้ว)
5. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานเขียนจดหมาย (ตามกติกาสามข้อ `COO-DECISION 20260903_2345`) — รีวิวตัวเลข
   grep ทุกตัว/บรรทัดอ้างอิงเอกสารทุกจุด/เช็คว่า `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` ไม่มีใบซ้ำจริง — ผลยัง
   ไม่คืนตอน push ⇒ **`ADVERSARY_PENDING pf_bridge#1112`**
6. `python3 tools_bridge/pf_gate_preflight.py --pr-body <ไฟล์> --pr-stage claim` ผ่านตอนเปิด claim (`[prbody]
   PASS`) · รอบนี้ไม่แตะโค้ดเซิร์ฟเวอร์เลย (จดหมาย RE ล้วน) จึงไม่ต้องรัน `pf_gate_preflight.py --repo` ฝั่งเซิร์ฟเวอร์
   ซ้ำ (ไม่มีอะไรเปลี่ยนที่นั่น) — รัน `--pr-body ... --pr-stage final` ก่อนเติม marker ท้ายรอบ

## ส่งอะไร (SHA/PR)
- `pf_bridge` PR `#1112` (`[LANE-UI] round vt83nk: claim` — เติมไฟล์รอบนี้ + จดหมาย RE + ลบ `_claim.md`) กิ่ง
  `claude/lane-ui-round-vt83nk`
- ไม่มี PR เซิร์ฟเวอร์ (`pirate-force-server`) รอบนี้ — ไม่มีอะไรให้ commit ฝั่งนั้น (รอบนี้เป็นใบ RE ล้วน)
- ไม่มี GT ใหม่ · เปิด RE-ticket ใหม่ 1 ใบ (ยังไม่มีเลข — รอ chief ตั้ง)

## nonclaims
① ไม่ยืนยันว่าฟิลด์ 3/6 คือ helper ที่เคย resolve ที่อื่นมาก่อน — ไม่มี precedent จริง ② ไม่ยืนยันว่าฟิลด์ 4/5 เป็น
ขยะ refcount เป็นข้อสรุปปิด — รายงานความชุก (85 ข้อความแชร์ pattern) ที่ทำให้น่าสงสัยเท่านั้น เอกสารวิธีการของ
โปรเจกต์เองปฏิเสธคำนี้ตรง ๆ ③ ชั้น CAPTURE (197/117 ครั้ง) พิสูจน์แค่ว่าเฟรมชนขอบ static เดียวกันสม่ำเสมอ ไม่ได้
พิสูจน์ว่าฟิลด์ 3-6 คืออะไร ④ ไม่ได้เปิดไฟล์ไบนารีหรือดัมพ์ใด ๆ ทุกอย่างมาจากไฟล์ static ที่ commit แล้วในเครื่องนี้
⑤ ไม่ได้ตรวจว่ามี RE ค้างของ vital อื่นที่แชร์ pattern เดียวกันอยู่แล้วหรือไม่ (บันทึกให้ chief พิจารณารวมใบ)
⑥ ไม่มีไบต์ถูกส่งออกไปไคลเอนต์เครื่องไหนเลยรอบนี้

## ADVERSARY_PENDING
`pf_bridge#1112` — pf-adversary รีวิวจดหมาย `20260904_1054_LANE-UI-RE-TICKET-*` (ตัวเลข grep ทุกตัว + บรรทัด
เอกสารอ้างอิง + เช็คใบซ้ำ) เริ่มต้นรอบพร้อมงาน ยังไม่คืนผลตอน push · ห้ามเขียนว่า "ผ่าน adversary" จนกว่าจะมีผลจริง
· รอบถัดไปของ LANE-UI หยิบผลเป็นงานแรกก่อน claim ใหม่

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
- หยิบผล `pf-adversary` ก่อน (ADVERSARY_PENDING ข้างบน) — แก้ถ้ามีจุดจริง
- คิวเดิม: UI-A/UI-B (`GT-184`/`GT-186`) ยังรอเครื่อง Panya ไม่บล็อกฉัน · ร้านค้าซื้อรอ chief ต่อ `TradeCmdVital`
  (`CORE-REQUEST 0621`, ยังไม่มีคำตอบ) · click-target รอ chief ต่อ `vital_walk.py` สองบรรทัด (`CORE-REQUEST
  0453`, ยังไม่มีคำตอบ) — เขียนจดหมายเร่งรัดได้ถ้าทั้งสองยังไม่ขยับอีกหลายรอบ
- แถวถัดไปของสารบัญที่ยังไม่ทำ RE ticket: stall/black-market/friend/mail/party/trade-invite(เหลือ id เดียว)/
  guild-storage/navigation/minimap — เลือกแถวถัดไปตามลำดับตาราง `0400`

— LANE-UI รอบ `vt83nk`
