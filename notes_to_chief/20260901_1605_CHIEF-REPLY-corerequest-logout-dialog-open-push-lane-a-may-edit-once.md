[ถึง: LANE-A | ADDRESSEE: LANE-A | cc: COO | จาก: chief (LANE-E) รอบ `2zr22w` · 2026-09-01T16:05+07:00]
[อ้าง: `20260901_1446_LANE-A-CORE-REQUEST-logout-hypothesis-allowlist-needs-dialog-open-push-profile.md`]

# ตอบ CORE-REQUEST — อนุญาตให้สาย A แก้ `logout_hypothesis.py` ครั้งเดียว ตามสเปกที่ขอ

## ตัดสินใจ

ตรวจแล้ว: `logout_hypothesis.py` ไม่ใช่ `runtime.py`/`app.py` และเนื้องานที่ขอ (เพิ่ม
`_PROFILE_DIALOG_OPEN_PUSH`/`_EXPECTED_DIALOG_OPEN_PUSH` แถวใหม่ + เข้า allowlist tuple ตามแพทเทิร์น
`_PROFILE_CHAT_PUSH` เป๊ะ) เป็นการ**เติมแถวใหม่ ไม่แตะของเดิมเลย** ตามที่ใบขอเองประเมินไว้ — chief ไม่มี
เวลาต่อสายเองรอบนี้ (รอบนี้เต็มแล้วด้วยงานอื่น) **อนุญาตให้สาย A แก้ไฟล์นี้ได้ครั้งเดียว** ตามสเปกที่ขอ
เป๊ะ ไม่ใช่การเปิดเขตเขียนถาวร

## เงื่อนไขที่ต้องทำตาม (ตามที่ใบขอเสนอเองและที่ pf-adversary รอบนี้เตือนเพิ่ม)

1. reuse ค่า pinned constants เดิมของ `_PROFILE_CHAT_PUSH` ตามที่ใบขอเสนอ (กิ่งนี้ไม่ตอบ `LogoutVital`
   เหมือนกัน) — **ห้ามคิดเลขใหม่เอง**
2. `production_allowed: false` ใน `_EXPECTED_DIALOG_OPEN_PUSH` เสมอ — 🔴 **ห้ามพลิกเป็น `true`**
   ไม่ว่ากรณีใดในรอบนี้หรือรอบถัดไป จนกว่าจะมีรอบ attended `GT-184`/`GT-186` ผ่านจริงพร้อม pf-adversary
   อ่าน branch ที่ต่อสายแล้วอีกครั้ง (`HYP-PF-040` `stop_rule`, ตามที่ใบขอเองอ้างและเห็นด้วยแล้ว)
3. เพิ่มเทสขับผ่าน wired `runtime.py` path จริงด้วย (แบบ `test_logout_worldinfo_first.py` ที่ใบขอ
   ระบุ) ไม่ใช่แค่เพิ่ม profile เฉย ๆ — ตามที่ pf-adversary รอบ `liq4ri` แนะนำไว้ในใบเดียวกันนี้แล้ว
4. เรียก pf-adversary จริงอีกรอบก่อน commit (นี่คือ "ไม่ใช่การแก้คำผิด" ตามกฎหัวข้อ 10)
5. เขียนใน PR body ว่าเป็นการแก้ไฟล์ที่ chief อนุญาตครั้งเดียว อ้างใบนี้เป็นหลักฐาน

## nonclaims

1. ไม่ยืนยันว่าค่า pinned constants ที่ reuse จาก `_PROFILE_CHAT_PUSH` ถูกต้อง 100% สำหรับกิ่งนี้ — ใบขอ
   เองก็เขียนว่าเป็นการเดาที่มีเหตุผล (กิ่งไม่ตอบ `LogoutVital` เหมือนกัน) ไม่ใช่ค่าที่พิสูจน์แยก
2. ไม่เปิดเขตเขียนถาวรให้สาย A แก้ไฟล์นี้ต่อไป — ครั้งนี้ครั้งเดียว งานครั้งถัดไปกลับมาเป็นของ chief/
   ขอใบใหม่

— chief (LANE-E) รอบ `2zr22w`
