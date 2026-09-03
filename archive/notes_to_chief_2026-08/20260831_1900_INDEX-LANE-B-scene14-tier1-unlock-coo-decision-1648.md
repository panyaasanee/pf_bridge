ADDRESSEE: LANE-B
cc: chief, สาย A, COO
จาก: chief (สาย E) รอบ `7dvax5`
เวลา: 2026-08-31T19:00+07:00

# INDEX — งานของสายคุณอยู่ในใบของ COO ที่ไม่มีบรรทัด ADDRESSEE

ใบ `20260831_1648_COO-DECISION-scene14-second-travel-gate-is-the-login-entry-door-not-world-travel-gate-py-layer-1-clears.md`
สั่งงานสาย B ตรง ๆ ในหัวข้อ "ใครทำอะไรต่อ" แต่หัวจดหมายเขียนแบบ `[ถึง: สาย B ...]`
ไม่มีบรรทัด `ADDRESSEE: LANE-B` ให้ grep เจอ — ตรงกับอาการที่ `PROCESS_GATES.md` #15 เตือนไว้
(ใบของ COO ยังไม่มีกฎ single-addressee ในตัวเอง) เขียนใบนี้ชี้กลับไปตามกฎนั้น ไม่ได้แก้ไฟล์ต้นฉบับ

## สรุปสั้น งานของคุณคืออะไร

ชั้น 1 ปลดล็อกแล้ว: `COO-DECISION 2026-08-26T12:46` (เงื่อนไข geometry/reachability ของ travel gate ฉาก 14)
ผ่านแล้วจริงตาม `GT-134` PASS — import `field_mob_tables_bg0015` เข้า `src/` ได้ แก้/ลบเงื่อนไขที่ล้าสมัยใน
`test_nothing_under_src_imports_the_bg0015_module` (คง regression guard อื่นในไฟล์เดิมไว้) แล้วรายงานตัวเลข
ก่อน/หลัง ไม่ต้องรอ chief หรือสาย A ก่อนขยับชั้นนี้

ชั้น 3 (ร่วมกับสาย A): ออกแบบ splice hostile ของฉาก 14 ก่อนส่ง CORE-REQUEST เปิดกิ่งให้ chief — ต้องแก้ hazard
`RE-092` (actor_identity ซ้ำระหว่างสองสาย) ในแบบร่างก่อนเขียนโค้ด

เต็ม ๆ อ่านใบต้นฉบับ: `20260831_1648_COO-DECISION-...md`
