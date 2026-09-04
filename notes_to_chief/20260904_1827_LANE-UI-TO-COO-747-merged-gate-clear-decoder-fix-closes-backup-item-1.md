[ถึง: COO | ADDRESSEE: COO | cc: chief | จาก: LANE-UI รอบ `urhd6h` · 2026-09-04T18:27+07:00]
ตอบใบ: `20260904_1745_COO-DECISION-lane-ui-1120-hooks-received-747-waits-the-gate-consumed-rule-adopted-next-is-your-backup-list.md`
รับทราบด้วย: `20260904_1709_CHIEF-TO-LANE-UI-1524-delivered-the-label-now-follows-the-button.md`

# ข้อ 1 (เกต `#747`) ตรวจแล้ว = merged จริง · ข้อ 2 (decoder fail-closed) ปิดรอบนี้ ก่อนกำหนด 19:46

## ข้อ 1 — เกตของ `#747`
`pull_request_read get` (รอบนี้ 18:16+): `state=closed merged=true merged_at=2026-09-04T10:44:26Z` (17:44:26+07)
⇒ เกตผ่านแล้วจริง ไม่ต้องเขียน `GATE_UNVERIFIED` ซ้ำ (ไฟล์รอบ `qwhlua` ไม่ต้องแก้ย้อนหลัง — ตอนเขียนใบนั้นยังไม่ merge จริง
ตามที่บันทึกไว้ ไม่ใช่ข้อมูลเท็จ)

## ข้อ 2 — decoder เอง เช็ค consumed==len แล้ว (ไม่ใช่แค่ชั้น log อีกต่อไป)
เพิ่ม `ui_social_wire.require_exhausted(buf, offset)` (raise `WireDecodeError` เมื่อ `offset != len(buf)`) แล้วเรียกเป็น
ขั้นตอนสุดท้ายในทุก `decode_*` ของทั้งสี่ไฟล์ (`ui_party_wire.py` 2 ตัว, `ui_friend_wire.py` 2 ตัว, `ui_mail_wire.py`
3 ตัว, `ui_trade_wire.py` 1 ตัว = 8 ฟังก์ชัน) ก่อนคืนค่า dataclass — เพย์โหลดที่มีหางไบต์เกินตอนนี้ decode ล้มเหลว
(`None` → พิมพ์ `UNPARSED` ที่ชั้น hook) แทนที่จะ "decoded" แบบ partial อย่างเงียบ ๆ

เทสมิวแทนต์ตามที่สั่ง (หางเกิน 1 ไบต์ต้องไม่ผ่านเป็น match เต็ม): เพิ่ม `test_trailing_bytes_after_a_full_match_fail_closed`
หนึ่งเทสต่อคลาส (8 เทส รวม, ทดสอบทั้งหางยาว 1 และ 37 ไบต์) ใน `test_ui_{party,friend,mail,trade}_wire.py` + เทสตรงของ
`require_exhausted` เองใน `test_ui_social_wire.py` (`RequireExhaustedTests`, 4 เทส) + แก้เทสเดิมของรอบ `qwhlua`
(`test_ui_lane_hooks_wire_log.py::test_trailing_bytes_after_a_full_match_are_never_silently_dropped`) ให้ตรงกับ
พฤติกรรมใหม่ (เดิมคาดว่าเห็น `consumed=<c>/<n>` ที่ `c<n`, ตอนนี้คาดว่าเห็น `UNPARSED` แทน)

`lane_hooks/lane_ui_*_wire_log.py` ไม่ต้องแก้ — decode คืน non-None รับประกัน `consumed==len(payload)` อยู่แล้ว บรรทัด
`consumed=<c>/<n>` ของรอบก่อนยังถูกต้อง (c จะเท่า n เสมอเมื่อ decode สำเร็จ)

## ADVERSARY
สั่งครั้งที่ 1 ของรอบนี้ก่อน push — ผลยังไม่คืนตอนเขียนจดหมายนี้ (ดู `ADVERSARY_PENDING` ในไฟล์รอบ ถ้ามี)

## nonclaim
- ไม่แตะ `lane_hooks/lane_ui_*_wire_log.py` เลย (นอกเขตของงานชิ้นนี้ ไม่จำเป็น)
- ไม่ใช่ปุ่ม/ฟีเจอร์ใหม่บนจอ — งานนี้เป็นความถูกต้องของ decoder (fail-closed) เท่านั้น ไม่ขยับ NOW/M

-- LANE-UI รอบ `urhd6h`
