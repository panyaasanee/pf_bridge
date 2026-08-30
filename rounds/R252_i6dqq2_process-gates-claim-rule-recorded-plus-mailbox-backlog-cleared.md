# R252 (i6dqq2) — 2026-08-31T~00:5x+07:00 — chief

## รอบนี้ทำอะไร

- Round-lock guard: ยืนยัน R251 ทั้งสอง repo `merged=true` ด้วย `pull_request_read get`
  (`pf_bridge#543` sha `b22adad`..., `pirate-force-server#344`) ก่อนแตะอะไร — ไม่มีของหาย
- ทำตามสั่งของ `20260831_0044_COO-DECISION-claim-before-work-rule-recorded-in-process-gates.md` ครบสองข้อ:
  1. บันทึกกฎ "จองก่อนลงมือ + จ่าหน้าสายเดียว" ลง `PROCESS_GATES.md` เป็น section 12 ใหม่
     (ที่มา: `20260830_2356_PANYA-DECISION-...` รับรองโดย `20260831_0044_COO-DECISION-...`
     ไม่คัดลอกเหตุผลยาวมา ลิงก์กลับสองใบตามที่สั่ง)
  2. ไล่ตรวจ `GAME_TEST_QUEUE.md` และ `CLIENT_RE_QUEUE.md` หาใบที่ระบุผู้ทำแบบ "สาย X หรือ chief/สาย Y"
     — grep ตรงและกว้างสองรอบ ไม่พบใบค้างที่ผิดกติกาแม้แต่ใบเดียว (ทั้งสองไฟล์อยู่ในเขตเขียนที่ถูกต้องแล้ว)
- CORE-REQUEST audit: ใบล่าสุด (`20260830_2148_LANE-A-CORE-REQUEST-columbus-crossing-...`) ถูกต่อสายไปแล้วใน R250
  (`world_m2_crossing_handoff.crossing_handoff()`) ไม่มีใบใหม่ค้าง
- Mailbox: consume 11 ใบที่จ่าหน้าถึง chief/ทุกคนจริง (PANYA-ANNOUNCE 2315, LANE-B-STATUS 2343, LANE-GM-STATUS 2345,
  PANYA-DECISION 2356, LANE-B-REPLY 2248 (superseded ด้วยตัวเอง), LANE-A-STATUS 2259, KA1A-ADDENDUM 0011,
  LANE-GM-STATUS 0025, LANE-A-STATUS 0033, KA1A-PROMPTS-PATCHED 0039, COO-DECISION 0044) พร้อม stub ครบทุกใบ
  · ข้ามสองใบที่จ่าหน้าไม่ใช่ chief โดยตรง (LANE-B-REPLY-PANYA-ANNOUNCE 2343 ADDRESSEE: PANYA,
  PANYA-ADDENDUM 2355 ADDRESSEE: ทุกสาย A/B/GM cc chief เท่านั้น) — ปล่อยให้เจ้าของ/สายที่ถูกจ่าหน้าอ่านเอง
- ledger: `python3 tools/verify_hypothesis_ledger.py` → `HYPOTHESIS_LEDGER PASS entries=47` ไม่มี drift ก่อน commit

## ไฟล์ที่แตะ (pf_bridge, ไม่นับ rounds/ และจดหมาย)

`PROCESS_GATES.md` (1 ไฟล์)

## ไม่ได้พิสูจน์ / ยกไปรอบหน้า

- ไม่มีการเปลี่ยน src ฝั่ง `pirate-force-server` รอบนี้ ⇒ ไม่มี gameplay ใหม่ให้เทส
  (`GAME_TEST_QUEUE.md` ไม่แก้เนื้อในรอบนี้ ตามกติกาหัวข้อ 11 — ไม่มีอะไรใหม่ให้เพิ่ม)
- หมายเหตุที่ยังไม่ได้ลงมือ (แจ้งไว้ในจดหมายท้ายรอบ ไม่ใช่ของ chief แก้เอง): prompt สาย A/B/GM หัวข้อ E
  ยังเขียนเลข reap เก่า (2ชม./6ชม.) ไม่ตรงค่าจริง `PF_STALE_MINUTES=45` ตาม `20260831_0039_KA1A-PROMPTS-PATCHED-*`
- `CORE-REQUEST-GM-042` ยังเลื่อนตามเดิม (ตัดสินใจรอบ R248) ไม่มีข้อมูลใหม่ให้ทบทวนรอบนี้

push แล้ว รอ merge PR pf_bridge#547 / server#347
