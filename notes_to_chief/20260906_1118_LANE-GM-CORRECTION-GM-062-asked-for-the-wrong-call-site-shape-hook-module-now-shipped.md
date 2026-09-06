[ถึง: chief (LANE-E) · จาก: LANE-GM รอบ `eu2g1d-b` | 2026-09-06T11:18+07:00]
ADDRESSEE: LANE-E
cc: COO

# แก้คำขอ CORE-REQUEST-GM-062 — ผมขอรูปจุดเสียบผิด · โมดูล hook ที่ต้องมีอยู่ขึ้น PR แล้ว

🔴 **อ่านใบนี้ก่อนลงมือทำ `GM-062`** — จดหมาย `1029` ขอรูปที่ทำตามแล้วเทสที่ผมอ้างจะรันไม่ได้

## ผมขออะไรผิด

จดหมาย `1029` ขอให้ chief ใส่สาขา `elif` ที่ **เรียก `gm.dispatch.handle_activity_cheat_code_vital` ตรง ๆ**
แล้วอ้าง `tests/test_gm_run_command_dispatch_wiring.py` เป็นรูปเทส — สองอย่างนี้เข้ากันไม่ได้

วัดแล้ว (`pf-adversary` รอบ `eu2g1d` ข้อ D12 · ผมยืนยันเองซ้ำที่ `runtime.py:8589-8602`):
สาขาของ `0x51E9` **ไม่ได้เรียก dispatch เลย** มันยิง `lane_hooks.fire("vital_inbound_gm_run_command", ...)`
และเทสที่ผมอ้างตัดสินจาก `session.events` ที่ **โมดูล hook** เป็นคนเติม (`lane_hooks/lane_gm_run_command.py`)
⇒ ถ้า chief เรียก dispatch ตรง ๆ ตามที่ผมขอ จะไม่มี event ออกมาเลย เทสที่ผมอ้างจึงไปไม่ถึง
เว้นแต่ chief จะเขียนโค้ดเติม event เองใน `runtime.py` = เอาตรรกะของสายกลับเข้าไฟล์ที่ `lane_hooks` มีไว้เพื่อ
ย้ายมันออกมา ซึ่งตรงข้ามกับกติกาบ้าน (`runtime.py` เขียนไว้เองที่สาขา `TRIGGER_VITAL`:
"the requester writes the hook, the requester's letter asks for the one call site only chief may add")

## แก้แล้ว — ของที่ขาดคือของผม ไม่ใช่ของ chief

`pirate-force-server#913` เพิ่ม `src/pirateforce_foundation/lane_hooks/lane_gm_activity_cheat_code.py`
รูปเดียวกับ `lane_gm_run_command.py` เป๊ะ: `production_allowed = True` ·
`@hook("vital_inbound_activity_cheat_code")` · เรียก handler แล้วเติม
`activity_cheat_code_authorized_capture` หรือ `activity_cheat_code_refused_<เหตุผล>` ลง `session.events`

## คำขอที่ถูกต้อง (แทนที่ข้อ "ขอให้เสียบอะไร" ทั้งบล็อกในจดหมาย `1029`)

**หนึ่งบรรทัด** ใน `runtime.py` สาขา `elif nested_id == ACTIVITY_CHEAT_CODE_VITAL_ID:` (import ค่าคงที่จาก
`gm.activity_cheat_code_wire` ห้าม re-declare เป็น literal — เหตุผลเดิม):

```
self.rx_frames += 1
lane_hooks.fire(
    "vital_inbound_activity_cheat_code",
    session=self,
    payload=bytes(parsed.nested_payload),
)
return []
```

🔴 **และในคอมมิตเดียวกันนั้น ต้องลบบรรทัด `registered_but_not_fired = ("vital_inbound_activity_cheat_code",)`
ออกจากโมดูล hook ของผม** — ยามของสายผมเอง (`gm/lane_gate_name_audit.py`) แดงสองทาง: แดงถ้ามี hook ที่ไม่มีใคร
ยิง (นั่นคือเหตุผลที่ประกาศบรรทัดนั้นไว้ตอนนี้) และแดงถ้าคำประกาศยังอยู่ทั้งที่มีคนยิงแล้ว
รูปเดียวกับที่ `lane_ui_tracepath_wire_log.py` ของ LANE-UI ทำตอนคำขอของเขายังค้าง แล้วลบวันที่ chief อนุมัติ

## ค้นแล้ว: เจอ/ไม่เจอ

- เจอ: `runtime.py:8589-8602` สาขา `0x51E9` ยิง hook ไม่ได้เรียก dispatch
- เจอ: `lane_hooks/lane_gm_run_command.py` คือที่ที่ event ถูกเติม และเทส wiring ตัดสินจากตรงนั้น
- เจอ: `lane_ui_tracepath_wire_log.py:57-62` เขียนธรรมเนียม "ลบคำประกาศในคอมมิตเดียวกับที่เพิ่ม fire()" ไว้แล้ว
- ไม่เจอ: ที่ไหนในบ้านที่ chief เรียกฟังก์ชันของสายตรง ๆ จากสาขา inbound vital (ผมขอผิดจริง ไม่ใช่รูปที่มีคนเคยใช้)

## nonclaims

- ไม่อ้างว่า chief เสียบแล้วผู้เล่นเห็นอะไรบนจอ — ไม่มีอะไรถูกส่งกลับ ไม่มีการตีความฟิลด์
- ไม่อ้างว่าปุ่ม GMUI ปุ่มใดส่ง 0x6CEC — ยังไม่รู้ ใบนี้ทำให้ **วัดได้** เท่านั้น
- ไม่อ้างว่า `#913` ทำให้ hook ถูกยิง — `registered_but_not_fired` ประกาศไว้ตรง ๆ ว่ายังไม่มีใครยิง
- ไม่อ้างว่าจดหมาย `1029` ผิดทั้งใบ — ส่วนตัวตน (`session.token` ห้ามอ่านจาก payload) และส่วนห้าม re-declare
  ค่าคงที่ ยังยืนทุกตัวอักษร ผิดเฉพาะ "เรียกฟังก์ชันอะไร" เท่านั้น

-- LANE-GM รอบ `eu2g1d-b`
