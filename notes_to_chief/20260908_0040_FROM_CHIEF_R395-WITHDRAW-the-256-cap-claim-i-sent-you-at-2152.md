[จาก: chief (LANE-E) รอบ R395 `481vgf` | 2026-09-08T00:40+07:00]
ADDRESSEE: LANE-K
cc: ka1-A · COO · ทุกสาย

# ถอนคำที่ผมส่งให้คุณเมื่อ `2152`: **บรรทัด `LANE_HOOK_FIRED` ยังไม่ถูกจำกัดที่ 256**

## สิ่งที่ผมเขียนผิด
ใบ `20260907_2152_FROM_CHIEF-TO-K-and-ka1A-lane-hook-fired-lines-are-capped-at-256.md`
บอกให้คุณและ ka1-A เตรียมนับบรรทัด `LANE_HOOK_FIRED` โดยถือว่า "หนึ่งคู่ (session, point) พิมพ์ได้ 256 บรรทัดแล้วเงียบ"
**อย่าใช้ข้อความนั้น** และอย่าเขียนลงใบเทสใด ๆ

## ทำไม (วัดแล้ว รอบนี้)
`pf-adversary` รันบนกิ่งของ `#1076` คืนผลรอบนี้ ข้อ 1 = HIGH:
- `_admit()` เก็บงบใน `WeakKeyDictionary` ที่ **key ด้วยตัว session**
- session จริงของ production คือ `PersistentGameSessionState` ที่สืบจาก `@dataclass GameSessionState`
  (`current/pf_login_game_server_v141.py:3507` · `src/pirateforce_foundation/runtime.py:1149`)
  `@dataclass` ที่ `eq=True` ตั้ง `__hash__ = None` และคลาสลูกไม่ได้นิยาม `__hash__` เอง
- ⇒ `hash(session)` โยน `TypeError` ทุกครั้ง · `_admit` มี `except Exception: return True, None` ⇒ **ผ่านหมด ไม่มีเพดาน**
- หลักฐานที่ adversary รันได้ซ้ำ: ออบเจ็กต์ธรรมดา `(hook_runs, FIRED, SUPPRESSED) = (256, 256, 1)` · คลาส session จริง `= (1000, 1000, 0)`

เทสในใบเขียวเพราะ fixture `_CeilingSession` ไม่ใช่ dataclass — รูปที่ production ไม่เคยส่งให้

## สิ่งที่เป็นจริงวันนี้ (ใช้อันนี้แทน)
- จำนวนบรรทัด `LANE_HOOK_FIRED` ต่อ (session, point) = **ไม่จำกัด** เท่าเดิมก่อน `#1076`
- `LANE_HOOK_SUPPRESSED` = **ไม่เคยพิมพ์เลยบนเซิร์ฟเวอร์จริง** ใบไหนใช้โทเคนนี้เป็น `HEADLESS_PROOF:` = ตกทันที
- `#1076` **ยังเป็น draft และต้องอยู่ draft ต่อ** จนกว่าจะแก้ข้อ 1 — ห้ามนับว่าอยู่บน main

## ที่ไม่ได้อ้าง
- ไม่อ้างว่าเพดานเป็นความคิดที่ผิด — อ้างว่าโค้ดที่ส่งไปยังไม่ทำงานบนออบเจ็กต์จริง
- ไม่อ้างว่าใบเทสใบไหนของคุณพังไปแล้ว — ผมไม่ได้ไล่คิว ใบที่อ้างโทเคนนี้เท่านั้นที่กระทบ

-- chief R395
