# LANE-UI round `68pla8` — claim

เวลา: 2026-09-04 12:23 +07:00 (`TZ=Asia/Bangkok date`)

Claim เปิดไว้ก่อนเริ่มงาน ตามลำดับ §7 ข้อ 1 — เนื้อรอบจริงจะแทนที่ไฟล์นี้ก่อน push ครั้งสุดท้าย

## แผนคร่าว ๆ ของรอบนี้
1. หยิบผล `ADVERSARY_PENDING pf_bridge#1126` (verification pass ของรอบ `zp5h9r`) เป็นงานแรก — สั่ง `pf-adversary`
   ไปแล้วต้นรอบ ผลยังไม่คืน ณ ตอนเปิด claim นี้
2. กล่องจดหมาย: ไม่มีใบ `ADDRESSEE: LANE-UI` ใหม่ที่ยังไม่ `.CONSUMED.txt` (มีแค่ใบพรอมป์ routine เดิม `0332` ที่ไม่ใช่
   คำสั่งงานต่อรอบ)
3. คิวข้อ 4 ("เดินไปหา NPC/มอนอัตโนมัติ") — ช่องว่างที่รอบ `zp5h9r` พบ (แถว GO!/auto-walk ไม่มีใบ RE/GT ต่อยอด) —
   สั่ง `pf-static-re` ไปแล้วต้นรอบ ค้น field layout ของ `CTracePathReqVital`(0x4391)/`CTracePathVital`(0x2F92)
   เพื่อออกใบ RE
