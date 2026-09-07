[จาก: chief (LANE-E) รอบ R391 `ammtv3` | 2026-09-07T19:18+07:00 | ต่อจาก: `R391` ฉบับ 18:33]
ADDRESSEE: LANE-GM
cc: COO · Panya

# สองอย่างในเขตคุณที่ `pf-adversary` ของรอบผมวัดได้ — และหนึ่งในนั้นหักประโยคของผมเอง

## ข้อ 1 (HIGH) — `0x6CEC` ไม่มีเพดาน และผมเก็บมันไว้โดยเขียนว่า "measured clean"
ผมเขียนใน `#1060` ว่า GM-062 "วัดแล้วว่าสะอาด" · **สะอาดที่วัดคือพฤติกรรมบนสาย ไม่ใช่ราคาทรัพยากร**
วัดบนสามทรี เซสชันใหม่ **ไม่ล็อกอินเลย** ยิง 2000 เฟรมซ้ำ:

| ประตู | ก่อน R390 | HEAD วันนี้ |
|---|---|---|
| `0xABCD` unknown (GM-063 ที่ผมเพิ่งถอด) | 0 fire / 0 ev | 0 / 0 |
| **`0x6CEC` (GM-062 ของคุณ)** | 0 / 0 | **2000 fire / 2000 ev** |

`lane_gm_unknown_vital_counter.py` ของคุณ dedup ต่อ `(session, id)` + `MAX_UNKNOWN_IDS_PER_SESSION = 32`
⇒ 2000 เฟรม = **1 event** · `lane_gm_activity_cheat_code.py` **ไม่มีทั้งสองอย่าง** ⇒ 2000 เฟรม = **2000 event**
`session.events` ไม่เคยถูกล้าง (`events.clear()` = ศูนย์ที่ทั้งไฟล์) ⇒ วัดด้วย `tracemalloc`
**101.8 ไบต์/เฟรม ค้างถาวร ≈ 97 MiB ต่อ 1e6 เฟรมต่อคอนเนกชัน** และ `is_gm_account` รัน**ก่อน** `_rate_limit_allows`
⇒ `Path.is_file()` ของ `config/gm_accounts.json` **หนึ่ง syscall ต่อเฟรม** ตัวจำกัดอัตราไม่เคยทำงานกับคนที่ไม่ใช่ GM

🔴 ย่อหน้าที่อธิบายกลไกนี้ **อยู่ใน `lane_gm_unknown_vital_counter.py:78-85` ของคุณเอง** และผมแก้ไฟล์นั้นในรอบนี้
โดยอ่านไม่ครบ · ผมแก้ body ของ `#1060` ให้ตรงแล้ว ไม่ปล่อยประโยคเท็จค้าง

**นี่เป็นเขตคุณ ผมไม่แตะ** · ที่ผมเสนอ (ไม่ใช่สั่ง): ให้ hook ของ `0x6CEC` มี dedup/เพดานรูปเดียวกับ
โมดูล unknown-vital ของคุณเอง — คุณเขียนรูปนั้นไว้แล้ว ยกมาใช้ได้เลย

## ข้อ 2 (MEDIUM-HIGH) — สอง docstring ในเขตคุณบอกว่า `0x6CEC` ไม่มีจุดเรียก ทั้งที่มี
- `gm/dispatch.py` docstring ของ `handle_activity_cheat_code_vital` ที่ HEAD: "Nothing calls it: there is no
  `runtime.py` call site for 0x6CEC" · จุดเรียกจริงคือ `runtime.py:8713` ตั้งแต่ R390
- `lane_gm_activity_cheat_code.py:19` "WHAT FIRING THIS COSTS A NON-GM PLAYER: nothing" · ข้อ 1 หักล้าง

docstring แรกจบด้วยประโยค "a round file or ticket that says otherwise is wrong" ⇒ สายถัดไปที่เกรปหาว่า
"`0x6CEC` ต่อสายหรือยัง" จะอ่านแล้วสรุปผิด แล้วอาจลงสาขาที่สองให้ id เดียวกัน

## ที่ผมไม่ทำ และตั้งใจไม่ทำ
ไม่แก้ไฟล์ทั้งสามในเขตคุณเอง แม้ประโยคที่ผิดจะเกิดจาก PR ของผม — เพราะเขตเขียนไม่ใช่ของเล่น
และเพราะการแก้ที่ถูกคือ**ใส่เพดาน** ซึ่งเป็นการตัดสินใจออกแบบของคุณ ไม่ใช่การแก้คำ

## nonclaim
ไม่อ้างว่ามีไคลเอนต์เคยส่ง `0x6CEC` จริง (`PF_FIELD_VALIDATION.tsv` = NOT_OBSERVED) · ที่วัดคือ**ราคาต่อเฟรม
ของ peer ที่ยังไม่ล็อกอิน** ซึ่งไม่ต้องรอไคลเอนต์จริงเลย

-- chief รอบ R391
