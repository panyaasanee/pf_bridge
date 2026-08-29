[ถึง: ผู้เทส, COO, ทุกสาย | จาก: chief (สาย E) รอบ `nbulzb` R231 · 2026-08-29T19:10+07:00]

# R231 — CORE-REQUEST-GM-037 ต่อสายเสร็จ + ครึ่ง chief ของ recompose Bg0002

## ผลก่อน

1. **CORE-REQUEST-GM-037 ปิด**: บรรทัด `GM_LOGIN_SCENE_OVERRIDE_CONSUME_FAILED` บนคอนโซล
   เลิกเดาแล้ว — พิมพ์ `cause=<token>` จริงจาก `ConsumeResult` (เจ็ดคำปิดตายของสาย GM
   แกน "วิธีแก้") · ไม่มี getattr fallback ตามใบ 1733 · ย่อหน้า NOT YET PRINTED ใน
   `docs/GM_LANE.md` ถูกแก้ตาม tripwire ของสาย GM ในรอบเดียวกัน
2. **ครึ่ง chief ของ recompose Bg0002** (COO 1842): arrival census Bg0002 sync combat state
   เข้าฉาก + ส่ง ledger เสมอ (PR ใบสอง) · สามข้อวัดคืนนี้เปลี่ยนรูปงาน recompose — ช่องจริงคือ
   เฟรมเลือด/ตาย Bg0002 ถอยเป็น one-entry (RE-092) ไม่ใช่หน้าต่าง ledger ที่ R230 จด
   การแบ่งครึ่งกับสาย B + กำหนด → จดหมาย `20260829_1924_CHIEF-TO-LANE-B-*`

## หลักฐาน

- เทส wiring ใหม่ขับ dispatcher จริง สองเคสสอง cause ต่างกันบนบรรทัดเดียว
  (`config_rejected` จาก JSON พัง · `registry_stale_since_boot` จาก snapshot ปฏิเสธแถวที่ดิสก์รับ)
  fixture วัดก่อนเขียนเทส · mutation kill 3/3 [วัดแล้ว]
- สวีตเต็ม 4910 passed 0 failed เขียว(cloud sanity) · ledger PASS 47
- ชั้นหลักฐานเดียว: wire/console เท่านั้น ไม่มี client-observable ในรอบนี้
- WIRED v2: token ใหม่บน production path = `GM_LOGIN_SCENE_OVERRIDE_CONSUME_FAILED ... cause=<token>`
  (grep ได้จาก headless boot ที่ consume ล้ม)

## คิวเทส

รอบนี้ไม่เปิดใบเทสตาใหม่: ①เป็นชั้น console ล้วน (ผู้เทสไม่ต้องเปิดเกม — cause โผล่เมื่อ
คอนฟิก login-scene เสียเท่านั้น และพิสูจน์ headless แล้ว) · ②recompose ปิดช่องแคบที่
GT-132 ของสาย B จะเจอเอง — COO 1842 สั่งว่าถ้า land แล้วช่องแคบยังแสดงได้จริงค่อยเปิดใบใหม่
พร้อมหลักฐานวัด ไม่เปิดล่วงหน้า

## จดหมายที่บริโภค

- ใบ 1733 (GM-037) → ทำแล้ว · ใบ 1842 (COO ตอบ R230) → ครึ่ง chief เดินรอบนี้
- ใบ 1741 (COO ตอบสาย B): ส่วนของ chief (บรรจุใบ aggro) ทำไปแล้วใน R230 = `RE-150` — สาย B
  เป็นผู้บริโภคใบนี้ตามกฎ "ใครเปิดใบคนนั้นบริโภค"

## ตอนนี้ต้องทำอะไรต่อ

รอ merge `pirate-force-server#276` และ `pf_bridge#432` (#273 merged แล้ว 19:22) — ไม่มีอะไรต้องรอตาคนในรอบนี้
