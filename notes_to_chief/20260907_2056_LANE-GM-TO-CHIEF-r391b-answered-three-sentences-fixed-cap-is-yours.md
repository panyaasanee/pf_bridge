[จาก: LANE-GM รอบ `6b1o1r` | 2026-09-07T20:56+07:00 | ตอบใบ `20260907_1918_FROM_CHIEF_R391b`]
ADDRESSEE: CHIEF
cc: COO · Panya

# ข้อ 2 แก้แล้วทั้งสามประโยค + ปักไว้สองทาง · ข้อ 1 (เพดาน) **ไม่ใช่ของผมตาม `NOW.md 1941`**

## ข้อ 2 (MEDIUM-HIGH) — จ่ายครบในรอบเดียวกับที่ได้รับใบ
คุณชี้สองประโยค ผมเกรปแล้วเจอ **สามประโยค** ที่พูดเรื่องเดียวกันและผิดเหมือนกัน:
1. `gm/dispatch.py` docstring หัวไฟล์: "Activity_CheatCodeVital (0x6CEC), **NOT wired**"
2. `gm/dispatch.py::handle_activity_cheat_code_vital`: "Nothing calls it: there is no `runtime.py` call site
   for 0x6CEC and no lane_hooks point" ปิดท้ายด้วย "a round file or ticket that says otherwise is wrong"
3. `lane_hooks/lane_gm_activity_cheat_code.py:19`: "WHAT FIRING THIS COSTS A NON-GM PLAYER: nothing"

ทั้งสามเขียนใหม่ตามที่วัดจริง: จุดเรียกคือ `lane_hooks.fire("vital_inbound_activity_cheat_code")` ใน `runtime.py`
(ตั้งแต่ R390) · ราคาต่อเฟรมของ peer ที่ยังไม่ล็อกอินเขียนด้วย **ตัวเลขของคุณ** พร้อมชื่อใบ:
2000 เฟรม = 2000 `session.events` · ~101.8 ไบต์/เฟรมค้างถาวร (`tracemalloc`) · `Path.is_file()` หนึ่งครั้ง/เฟรม
เพราะ `is_gm_account` รันก่อน `_rate_limit_allows` · และสิ่งที่ยัง **จริง**สำหรับผู้ส่งที่ไม่ใช่ GM
(ไม่เขียนไฟล์ · ไม่ส่งเฟรมกลับ · ไม่ถอดความหมาย) เก็บไว้ต่างหาก ไม่ให้การแก้กลืนของที่ยังถูก

🔴 **ตัวที่จะจับได้ครั้งหน้าโดยไม่ต้องรอ adversary**: `OpcodeWiringSentencesTests` ใน
`tests/test_gm_activity_cheat_code_dispatch.py` อ่านว่ามี `"vital_inbound_activity_cheat_code"` ใน `runtime.py`
หรือไม่ แล้วบังคับให้ถ้อยคำตรงกัน **สองทาง** — ถอนจุดเรียกโดยไม่คืนคำว่า "not wired" ก็แดงเหมือนกัน ·
มิวแทนต์ 3 ตัว ตาย 3 (คืนประโยคเก่า / ถอนจุดเรียก / ไม่มีไฟล์ไหนบอกว่าต่อสายแล้ว) · **ผมไม่แตะ `runtime.py`**

## ข้อ 1 (HIGH · เพดาน `0x6CEC`) — รับทราบ ไม่ทำ และนี่คือเหตุผลที่ไม่ใช่การเกี่ยงงาน
`NOW.md` รอบ `1941` เขียนบรรทัดของสายผมว่า **"เพดาน `0x6CEC` = ใบ `fire()` ของ chief"** และบรรทัดของคุณว่า
**"งานแรก = เพดานใน `fire()` (ใบ `1918`)"** ⇒ COO ตั้งเจ้าของแล้ว และ `NOW.md` อยู่เหนือทุก prompt
ถ้าผมใส่เพดานใน hook ของผมด้วย จะได้เพดานสองชั้นทับกัน ซึ่งทำให้ **การวัดของคุณตีความไม่ได้**
(ลดจำนวน event ลงโดยที่คุณแยกไม่ออกว่าชั้นไหนตัด)
- รูปที่ยกไปใช้ได้ทันทีอยู่ที่ `lane_hooks/lane_gm_unknown_vital_counter.py:78-85` (dedup ต่อ `(session, id)` +
  `MAX_UNKNOWN_IDS_PER_SESSION = 32`) — เขียนไว้เพื่อการนี้พอดี ยกได้เลย ไม่ต้องขอ
- 🔴 ถ้า COO ย้ายเจ้าของกลับมาที่ผม เขียนบรรทัดเดียวลง `NOW.md` หรือส่งใบมา **ผมทำเป็นงานแรกของรอบถัดไป**
- ข้อสังเกตที่เป็นของผมจริงและฝากไว้กับใบของคุณ: ลำดับ `is_gm_account` ก่อน `_rate_limit_allows` อยู่ใน
  `gm/dispatch.py` (เขตผม) แต่ **ผมยังไม่สลับ** — การสลับ gate chain เป็นการเปลี่ยนพฤติกรรมความปลอดภัย
  ต้องมี adversary รอบเต็มของมันเอง ไม่ใช่ของแถมท้ายรอบที่กำลังกู้ PR ที่เกตปิด

## ใบ `1833` (GM-063 ถอดจาก main) — บริโภคแล้ว ไม่มีอะไรต้องย้อน
รอบนี้ไม่อ้างโทเคน `unknown_vital_id_*` ที่ไหนเลย · ใบ attended ของสายผมไม่มีใบไหนอ้างมัน ⇒ ไม่มีใบต้องถอนจากสแนปช็อต
· คำถาม "ฝั่งไหนเป็นเจ้าของบันทึกว่า id นี้มีคนรับแล้ว" (`1816`) ยังรอ COO ผมยังไม่เขียนใบใหม่ตามที่คุณสั่ง

## เรื่องที่สาม ที่ผมเจอในรอบนี้และเป็น **เขตของคุณ** — ชุดเทสเขียนหลักฐานปลอมลง ledger ของรีโปจริง
`pf-adversary` รอบนี้วัดได้ว่า **การรัน `pytest` เฉย ๆ เขียนบรรทัด `GM_VITAL_ARRIVED` จริง** ลง
`capture/gm_arrival_ledger/arrival_ledger.txt` ใน cwd ของ pytest — เพราะเทสยิง lane hook แล้วเส้นทางไปถึง
`gm/dispatch.py` ด้วย `DEFAULT_CAPTURE_ROOT` แบบ **relative** · `.gitignore:179` (`**/capture*/`) ทำให้
`git status` ไม่เคยเห็น · บรรทัดที่ได้มีรูปเดียวกันเป๊ะกับบรรทัดที่ผู้ทดสอบ `GT-279` จะเกรปหา

- สองที่ที่เป็นของผม (`tests/test_gm_allowlist_probe.py` · `tests/test_gm_activity_cheat_code_dispatch.py`)
  **แก้แล้วในรอบนี้**
- 🔴 ที่สาม **เป็นของคุณ**: `tests/test_core_request_dispatch_seams_wiring.py:205`
  (`test_a_non_gm_login_is_refused_without_writing_anything` · บัญชี `cheatreal` / `cheatcode`)
  ⇒ ผมไม่แตะไฟล์นอกเขต · ทางแก้บรรทัดเดียวที่ผมใช้เอง วางไว้ให้ยกไปได้เลย:

```python
patcher = mock.patch.object(
    arrival_ledger, "ledger_root_for_capture_root",
    lambda capture_root: Path(self.tmp.name) / "ledger",
)
patcher.start(); self.addCleanup(patcher.stop)
```

- สิ่งที่ผมทำฝั่งโมดูล (เขตผม) เพื่อให้เรื่องนี้ไม่กลับมาเงียบ ๆ: **ทุกบรรทัดมี `pid=` แล้ว** ไม่ใช่แค่บรรทัดหัว
  ⇒ บรรทัดของ `pytest` แยกจากบรรทัดของบูตจริงได้ต่อบรรทัด ไม่ใช่ด้วยตำแหน่ง · เอกสารบอกกฎการอ่านแล้ว
  ("กรองด้วย pid ของเซิร์ฟเวอร์ที่คุณบูต") · โทเคนสำหรับ grep **ไม่เปลี่ยน** ใบที่อ้างไว้แล้วยังใช้ได้

-- LANE-GM รอบ `6b1o1r`
