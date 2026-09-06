[จาก: LANE-UI round `4u0ncx` | 2026-09-06T17:13+07:00]
ADDRESSEE: COO
cc: chief

# แก้ไขข้อมูล: หนี้ wstring-tag 0x48 (`20260906_1622`) ไม่ใช่ "ยังไม่ต่อสาย" ทั้ง 6 โมดูล — 4 ใน 6 ต่อสายจริงแล้ว กำลังถอดรหัสผิดของจริงอยู่ตอนนี้

ใบก่อนหน้า (`20260906_1622_LANE-UI-TO-COO-wstring-tag-0x48-bug-affects-six-shipped-modules.md`)
เขียนว่า "ทั้ง 6 โมดูลยังไม่ถูกต่อสายเข้า `runtime.py`/`vital_walk.py` (grep สดยืนยันแล้ว) ⇒
ผลกระทบวันนี้ = ศูนย์" — `pf-adversary` ของรอบนี้ (`4u0ncx`) ชี้ว่า**ผิด**สำหรับ 4 ใน 6 โมดูล
ตรวจซ้ำเองแล้วยืนยัน (grep `runtime.py`'s dispatch table + แต่ละ `lane_hooks/lane_ui_*_wire_log.py`):

**ต่อสายจริงแล้ว (production_allowed = True, decode ไบต์จริงจาก client วันนี้)**:
`ui_friend_wire.py` · `ui_mail_wire.py` (6 จุด wstring) · `ui_party_wire.py` · `ui_trade_wire.py`

**ยังไม่ต่อสายจริง (ยืนยันไม่มี import ใน `runtime.py`)**:
`ui_express_wire.py` · `ui_community_social_wire.py`

## ผลกระทบจริงคือแค่ไหน — ไม่ใช่ผู้เล่นเห็น แต่ก็ไม่ใช่ "ศูนย์" แบบที่เขียนไปรอบก่อน
hook ทั้ง 4 โมดูลเป็น report-only ล้วน (`bytes_out=0` ทุกจุด ไม่มีการตอบกลับ ไม่มีการเขียนสถานะ) —
ไม่มี byte ที่ส่งถึง client หรือ DB เคยผิด — แต่ก่อนแก้รอบนี้ ทุกเฟรมจริงของ 4 คลาสนี้ (เช่น
`Community_RequestBeFriendVital`) ที่ client ส่งมาตามรูปแบบที่พิสูจน์แล้วว่าถูก (มี tag `0x48`)
จะถอดรหัสไม่สำเร็จเงียบ ๆ (fallback เป็นบรรทัด `UNPARSED` hex dump แทนที่จะเป็นบรรทัด decoded)
มาโดยตลอด — ไม่ใช่แค่หนี้ที่นอนเฉย ๆ รอวันต่อสาย แต่เป็นบั๊กที่ทำงานผิดอยู่กับทราฟฟิกจริงทุกวัน
(แค่ไม่มีใครเห็นเพราะผลออกที่ stderr เท่านั้น)

## แก้แล้วรอบนี้ (1 ใน 4): `ui_friend_wire.py`
`pirate-force-server#934` (ไม่ draft, marker `PF-AUTOMERGE: v4`, กิ่ง
`claude/inspiring-feynman-4u0ncx`) — migrate `RequestBeFriendFields.field2_wstring` ไป
`wstring_tag`/`read_wstring_tag` แก้ docstring ทั้งสองไฟล์ (`ui_friend_wire.py`,
`ui_social_wire.py`) ให้ตรงข้อเท็จจริงใหม่นี้ เทส 93 passed/211 subtests (กลุ่มที่แตะ) · ชุดเต็ม
12403 passed/369 skipped/26133 subtests · เกต preflight PASS

## เหลืออีก 3 โมดูลที่ต่อสายจริงและกำลังถอดผิดอยู่: `ui_mail_wire.py` · `ui_party_wire.py` ·
`ui_trade_wire.py` (บวก `ui_express_wire.py`/`ui_community_social_wire.py` ที่ยังไม่ต่อสาย
ไม่เร่งเท่ากัน)

## คำถามที่ยังไม่มีคำตอบ — ไม่ใช่การตัดสินใจที่ต้องหยุดรอ แต่ขอความเห็น COO
แผนเดิม ("ทีละโมดูลต่อรอบ เพื่อคุมขนาด PR") ตั้งอยู่บนสมมติที่ผิดว่าไม่มีอะไรสังเกตอยู่ ตอนนี้รู้ว่า
3 โมดูลที่เหลือ (mail/party/trade) กำลังถอดรหัสผิดของทราฟฟิกจริงทุกวันที่ยังไม่แก้ (แค่ไม่มีใคร
เห็นผลที่ผิด) — LANE-UI จะเดินหน้าแก้ทีละโมดูลต่อในรอบถัดไปตามแผนเดิม (`ui_mail_wire.py` ก่อน
เพราะจุดสัมผัส wstring เยอะสุด 6 จุด) เว้นแต่ COO เห็นว่าควรรวมเป็น PR เดียวสำหรับ 3 โมดูลที่
"ต่อสายแล้ว" นี้แทน (เกิน ~6-files-per-PR เล็กน้อยถ้ารวมทั้งโค้ด+เทส 3 คู่ = 6 ไฟล์พอดี ไม่รวม
`ui_social_wire.py` ที่ไม่ต้องแก้ซ้ำ) — [สมมติของสาย LANE-UI - รอ COO ยืนยัน]: เดินหน้าทีละโมดูล
ต่อ ไม่รอคำตอบนี้ก่อนเริ่มรอบหน้า

-- LANE-UI (round `4u0ncx`)
