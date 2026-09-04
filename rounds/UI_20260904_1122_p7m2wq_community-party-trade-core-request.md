# LANE-UI round p7m2wq — CORE-REQUEST: 8 community/party/trade vitals fully resolved, wire them

เวลา: 2026-09-04 11:22 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ M — รอบนี้เป็น CORE-REQUEST (ต่อคิวข้อ 5 ของสารบัญ 15 แถว: เพื่อน/เมล/ปาร์ตี้/เทรด P2P/กิลด์คลัง) ไม่ใช่
โค้ดที่ผู้เล่นเห็นบนจอ — งานเตรียมทางให้ chief ต่อ dispatch ก่อน ตามกติกาภารกิจ (จุดเสียบ = CORE-REQUEST ใบเดียว
ต่อจุด) LANE-UI เองยืนยันแล้วว่าไม่มีจุดเสียบที่ต่อเองได้จาก `lane_hooks/`/`ui_*.py` อย่างเดียว

## ทำอะไร
1. `git fetch origin main` · ยืนยันรอบก่อน (`fx9k2p` #1113) merge แล้วจริง · ไม่มีใบ `[LANE-UI]` เปิดค้าง (นอกจาก
   claim ของรอบนี้) · กล่องจดหมายเจอแค่ false-positive เดิม (`0332`)
2. รอบก่อนไม่มี `ADVERSARY_PENDING` ค้าง — verification pass ของ `fx9k2p` คืนผลแล้ว **สะอาด ไม่มี defect ยืนยัน**
   (มีข้อสังเกตเล็ก ๆ สองจุดที่ไม่ใช่ของรอบ `fx9k2p` เอง อยู่ในเนื้อจดหมายเดิมตั้งแต่ก่อนแก้ — "519 vs 520" จาก
   คำสั่ง grep ที่ elide header row กับ "~85 vs 83" ที่ hedge ด้วย `~` ไว้แล้ว ไม่ใช่ defect ที่ต้องแก้ ปิดเรื่องนี้
   ที่นี่ ไม่เปิดรอบแก้เพิ่ม)
3. Explore agent สอบถามกลไก dispatch ของ `runtime.py` — ยืนยันว่าไม่มีจุดเสียบสำเร็จรูปสำหรับ vital ใหม่: ทุก
   `lane_hooks.fire()` วางอยู่ *ข้างใน* `if nested_id == <ค่าคงที่>:` ที่ chief เขียนไว้แล้วเท่านั้น — vital ใหม่
   ต้องถูก chief เพิ่ม branch ก่อนเสมอ (เหมือนปัญหาเดียวกับ `TARGET_VITAL`/`CHOOSE_NPC` ที่ `CORE-REQUEST 0453`
   เปิดค้างไว้)
4. `pf-static-re` agent เดินสาย opcode+ฟิลด์ของทุกคลาสในแถวเพื่อน/เมล/ปาร์ตี้/เทรด/กิลด์คลังของสารบัญ `0400` เทียบ
   กับ `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (ไฟล์ที่ round `c2a7nc` ไม่เคยเปิด) — พบ **8 คลาส opcode+
   ฟิลด์ resolved ครบ 100%** (`PartyInviteVital`, `PartyCmdVital`, `Community_RequestBeFriendVital`,
   `Community_RemoveFriendVital`, `Community_SendMailVital`, `Community_GetMailContentVital`,
   `Community_DeleteMailVital`, `TradeInviteVital` — ตัวหลังมีหลักฐานชั้น PROVEN เพิ่ม) และคลาสพี่น้องอีกจำนวนมาก
   ที่ opcode รู้แต่ฟิลด์ไม่ครบ (สถานะ "แก้แค่ id" ไม่ใช่ "แก้ทั้งแถว") · ตลาดมืด/หน้าต่างเรือยืนยันซ้ำว่ายังไม่มี
   opcode จริง (grep ว่างจริง)
5. เขียนจดหมาย `ADDRESSEE: chief` `notes_to_chief/20260904_1120_LANE-UI-CORE-REQUEST-eight-community-party-trade-
   vitals-are-fully-resolved-wire-them.md` (6,816 อักขระ / 12,668 ไบต์ — ต่ำกว่าเพดาน 12,000 อักขระ) แก้คำสรุปเดิม
   ของ `0400` ไว้ที่หัวจดหมายฉบับใหม่ตามธรรมเนียม ไม่แก้ไฟล์เก่า
6. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานเขียนจดหมาย — รีวิวตัวเลข opcode/ฟิลด์ทุกคลาส + เช็คหลักฐานชั้น PROVEN
   ของ `TradeInviteVital` + เช็คว่าไม่มีจุดเสียบ self-serve จริง + honesty ของ nonclaims — ผลยังไม่คืนตอน push
   ⇒ **`ADVERSARY_PENDING pf_bridge#1114`**

## ส่งอะไร (SHA/PR)
- `pf_bridge` PR `#1114` (`[LANE-UI] round p7m2wq: claim` → เติมไฟล์รอบนี้ + จดหมาย CORE-REQUEST) กิ่ง
  `claude/lane-ui-round-p7m2wq`
- ไม่มี PR เซิร์ฟเวอร์ — ไม่แตะโค้ดเลย (รอ chief ต่อ dispatch ก่อน)
- ไม่มี GT/RE ใหม่ · เปิด CORE-REQUEST ใหม่ 1 ใบ (สอง CORE-REQUEST เดิม `0453`/`0621` ยังไม่มีคำตอบ ณ ตอนเขียนนี้
  — ยังไม่ถึงรอบเร่งรัดตามที่บันทึกไว้ในรอบ `fx9k2p`)

## nonclaims
① opcode ของ 7/8 คลาส (ยกเว้น `TradeInviteVital`) มาจาก hash validate แล้ว ไม่ใช่ค่าที่อ่านจากไบต์ในภาพตรง ๆ และ
ไม่มีคลาสไหนถูกสังเกตบนสายจริงเลย (`NOT_OBSERVED` ทั้ง 8) ② ฟิลด์ resolved ครบ = รู้แค่รูปเฟรม ไม่รู้ความหมาย/
caller ของฟิลด์เลย — ไม่มีคลาสไหนมีหลักฐานว่า handler จริงทำอะไร ③ ไม่ยืนยันว่ารายชื่อ 8 คลาสครบทุกคลาสที่ resolved
จริงในสี่ระบบนี้ ④ ไม่ได้ไล่ `docs/FUNCTIONAL_COVERAGE.json` ว่าควรสร้างจริงหรือยัง ⑤ ไม่มีไบต์ออกไปไคลเอนต์เครื่อง
ไหนเลยรอบนี้ ไม่แตะโค้ด

## ADVERSARY_PENDING
`pf_bridge#1114` — pf-adversary รีวิวจดหมาย `20260904_1120_LANE-UI-CORE-REQUEST-*` (ตัวเลข opcode/ฟิลด์ทุกคลาส +
หลักฐาน PROVEN ของ `TradeInviteVital` + เช็คจุดเสียบ self-serve + nonclaims) เริ่มต้นรอบพร้อมงาน ยังไม่คืนผลตอน
push · ห้ามเขียนว่า "ผ่าน adversary" จนกว่าจะมีผลจริง · รอบถัดไปของ LANE-UI หยิบผลเป็นงานแรกก่อน claim ใหม่

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
- หยิบผล `pf-adversary` ก่อน (ADVERSARY_PENDING ข้างบน) — แก้ถ้ามีจุดจริง
- คิวถัดไป: RE ตลาดมืด/หน้าต่างเรือ (ยังไม่มี opcode จริง) หรือมินิแมป (ยังไม่รู้แม้แต่ชื่อ class) — เลือกตามลำดับ
  ตาราง `0400`
- ติดตามว่า chief ตอบ CORE-REQUEST ไหนก่อน (`0453`/`0621`/`1120` ใบใหม่นี้) — ถ้าตอบแล้วให้ข้ามไปเขียนโค้ดจริง
  ทันที (สูงกว่าคิว RE letter ต่อไป)

— LANE-UI รอบ `p7m2wq`
