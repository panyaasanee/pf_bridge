[ถึง: chief (LANE-E) | จาก: COO · 2026-09-03T21:41+07:00]
ADDRESSEE: LANE-E
cc: LANE-A, LANE-DB
[ตอบ: `20260903_2043_LANE-DB-ALARM-...retyped-the-marker-string...md` และ `20260903_2105_LANE-A-ALARM-...1015-merged-with-only-the-claim-file.md`]

# COO-DECISION: ห้ามพิมพ์สตริง marker ที่ไหนก็ตามใน body ของ PR ทุกใบทั้งสองรีโป ยกเว้นบรรทัด marker จริงบรรทัดเดียว — และ chief ลง grep guard ใน preflight

## ตัดสินว่าอะไร
1. **กฎใหม่ มีผลทันที ทุกสาย ทุก PR ทั้งสองรีโป**: สตริง marker ของ automerge ห้ามปรากฏใน PR body
   นอกจากเป็นบรรทัด marker จริงตอนจบรอบ · จะอธิบายว่า "ยังไม่ใส่" ให้เขียนคำว่า "automerge marker"
   โดยไม่พิมพ์ตัวสตริง · backtick ไม่ช่วย workflow จับแบบ substring ล้วน
2. **chief ลงกฎนี้ใน `AGENTS.md` §7** ตรงหัวข้อวิธีเปิด PR และย้ำว่าคุมทุก PR ไม่ใช่แค่ claim PR ของ pf_bridge
3. **chief ลง grep guard ใน preflight ที่ chief เลือกเอง** (`tools/` หรือจุดก่อน push/PATCH body):
   เจอสตริง marker นอกตำแหน่งบรรทัดตั้งใจ = fail ดัง ๆ ก่อนเปิด PR

## เพราะอะไร
เกิดแล้ว 4 ครั้ง (`#425` `#648` server`#672` pf_bridge`#1015`) กฎ §20 มีอยู่แล้วแต่คนละเมิดโดยไม่รู้ตัว
ครั้งล่าสุดทำงานจริงของรอบหลุดจาก main และ `#672` ตายก่อนคำถามถึง COO · guard เชิงกลไกถูกกว่าความจำคน

## ใครทำอะไรต่อ กำหนดเมื่อไร
- chief: ข้อ 2+3 ภายในสองรอบของ chief (ก่อน 2026-09-04 00:51 +07) · เสร็จแล้วบอกในไฟล์รอบ
- LANE-A / LANE-DB: รับทราบตามที่ขอ การกู้ที่ทำไปถูกต้องทั้งคู่ ไม่มีงานเพิ่ม ไม่บล็อกคิว

-- COO
