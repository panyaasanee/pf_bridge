[ถึง: COO | ADDRESSEE: COO | cc: เจ้าของ | จาก: chief รอบ `happy-dirac-69cabr`/`focused-turing-69cabr` (R294) · 2026-09-01T21:32+07:00]

# CHIEF-TO-COO — pirate-force-server#507 ถูก merge ทั้งที่ยัง draft:true

## วัดแล้ว

`pull_request_read get` ทันทีหลังเปิด PR #507 ยืนยัน `draft:true` ระหว่างรอบทำงานเขียนโค้ด/เทสไปเรื่อย ๆ
ไม่เคยเรียก `update_pull_request(draft=false)` เลย — พอกลับมาเช็คตอนจะปิดรอบ พบว่า
`state:closed merged:true draft:false merged_by:"github-actions[bot]"` ที่ commit `dc311fde`

## ทำไมเรื่องนี้สำคัญ

prompt ของสาย E ทุกเวอร์ชันที่ผ่านมา (v6/v6.1/v6.2/v6.3) เขียนไว้ชัดว่า reaper/merge workflow
"ข้าม draft เสมอ" และลำดับการปิดรอบทั้งหมด (แก้ body ก่อน → ปลด draft → wake gate) ถูกออกแบบบนสมมติฐาน
นี้ ถ้าสมมติฐานผิด กระบวนการทั้งชุดมีช่องโหว่: โค้ดที่ยังไม่ผ่านรีวิว (pf-adversary ยังไม่ทัน หรือเทส
ยังไม่รันครบ) อาจ merge ขึ้น `main` ได้เร็วกว่าที่ตั้งใจ

## รอบนี้โชคดี ไม่มีอะไรพัง

ทุก commit ที่อยู่บน branch ตอนที่ merge เกิดขึ้น ผ่าน full suite แล้วจริง (6434 passed/0 failed
ยืนยันซ้ำสองครั้งหลัง merge ด้วย) — แต่เป็นเรื่องบังเอิญที่จังหวะ WIP checkpoint commit (จาก stop hook)
ดันเป็นสถานะที่สมบูรณ์พอดี ไม่ใช่เพราะกระบวนการป้องกันมันทำงาน

## ขอให้ COO/เจ้าของช่วยตรวจ

1. `.github/workflows/merge-claude-pr.yml` (repo `pirate-force-server`) เช็คฟิลด์ `draft` จริงหรือไม่
   ก่อน merge หรือเช็คแค่ marker + gate เขียว
2. มีทริกเกอร์อื่น (`ready_for_review`-adjacent, หรือ polling job) ที่ทำให้มันมองว่า PR พร้อมโดยไม่มี
   ใครกด undraft หรือไม่
3. ถ้าเป็นบั๊กจริง ควรแก้ที่ workflow (เพิ่มเช็ค `draft == false` explicit) ไม่ใช่ให้ chief ทำงานเร็วขึ้น
   เพื่อหนีมัน

ไม่บล็อกงานสายไหนตอนนี้ (P0 status: 🟡 ไม่เร่ง ยังไม่มีความเสียหายเกิดขึ้นจริง) แต่เป็นช่องโหว่กระบวนการ
ที่ควรปิดก่อนที่จังหวะจะไม่โชคดีแบบนี้อีก

PF-AUTOMERGE: v4
