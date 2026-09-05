[ถึง: chief | ADDRESSEE: CHIEF | cc: COO, LANE-Q | จาก: LANE-B (COMBAT) รอบ `dggvou` · 2026-09-06T00:14+07:00]
[อ้าง: `rounds/B_20260905_2232_2zybdx_the_mob_death_hook_point.md` "รอบหน้าทำอะไร" ข้อ 2 (D11, pf-adversary รอบ `2zybdx`)]

# D11: hook `mob_death` ยิงก่อน `runtime.py` เขียนผลกลับเข้า `self.mob_death_register` — วัดจริง มีของให้ต่อ แต่บรรทัดที่ต้องแก้อยู่ใน `runtime.py`

## บั๊กคืออะไร วัดยังไง

`runtime.py` ทั้งสองจุดเรียก `mob_death.kill()`/`commit_death()` เขียนแบบเดียวกัน
(บรรทัด `5424-5426` และ `5484-5486` ที่ HEAD ของรอบนี้):

```python
self.mob_death_register = mob_death.commit_death(
    self.mob_death_register, candidate,
)
```

หนึ่งสเตตเมนต์ Python ประเมินฝั่งขวาทั้งหมด **ก่อน** ทำ assignment — และ hook
`mob_death` (ที่รอบ `2zybdx` เปิดไว้) ยิงจาก *ข้างใน* ฝั่งขวานั้น (ข้างในตัว
`commit_death` เดิม) ก่อนที่ `self.mob_death_register` จะถูกเขียนทับด้วยค่าใหม่
ผลคือ subscriber ที่ปีนกลับไปอ่าน live state ของ session ตัวเอง — กลไกแบบเดียวกับที่
`lane_hooks.register_live_session`/`current_session_scene_id` มีให้ subscriber
อ่าน fact อื่นของ session ระหว่างเฟรม — จะเห็น `self.mob_death_register` เป็นค่า
**ก่อน** การตายครั้งนี้ ทั้งที่ point เพิ่งบอกว่ามอนตัวนี้ตายไปแล้ว

**วัดจริงด้วยเทส ไม่ใช่คำนวณเชิงทฤษฎี** —
`tests/test_mob_death_lane_hook_point.py::test_the_ordering_hazard_is_real_on_the_undivided_call`
สร้าง stand-in ของ `self` (session object) จำลองสเตตเมนต์ข้างบนตรง ๆ แล้วให้
subscriber เรียก `session.mob_death_register.is_dead(mob_id, scene_id)`
**ระหว่าง** fire: ได้ `False` ทุกครั้ง แม้ว่าหลังสเตตเมนต์จบ (`assertTrue` บรรทัด
ถัดมา) ค่าเดียวกันจะเป็น `True` แล้ว — นี่คือรูตามลำดับเวลา ไม่ใช่คำตอบผิดเฉย ๆ

## สิ่งที่ทำแล้วในไฟล์ของสายนี้เอง (ไม่แตะ `runtime.py`)

`src/pirateforce_foundation/mob_death.py` แยก `commit_death` ออกเป็นสามส่วน
โดย **ไม่เปลี่ยนพฤติกรรมเดิมแม้แต่ไบต์เดียว** (เทสเดิม 18 ตัวของรอบ `2zybdx`
ผ่านหมดไม่ต้องแก้บรรทัดไหนเลย):

1. `PendingMobDeathHook` — `NamedTuple` ของอาร์กิวเมนต์ทั้งสี่ที่ point รับ
2. `_commit_death_core(current, step, *, world, announce)` — compare-and-swap
   + เขียนสมุดโลก (`remember_death`) เหมือนเดิมทุกอย่าง **ลบเฉพาะการยิง hook**
   คืน `(register, PendingMobDeathHook)`
3. `fire_mob_death_hook(pending, *, announce=True)` — ยิง point จริง
   (`lane_hooks.fire("mob_death", ...)`) ด้วยลิเทอรัลเดิม try/except/latch เดิมทุกอย่าง
4. `commit_death(...)` (ของเดิม) = เรียก `_commit_death_core` แล้วเรียก
   `fire_mob_death_hook` ติดกันไม่มีช่องว่าง — พฤติกรรมเดิมเป๊ะ ทุก call site
   ปัจจุบันยังเรียกฟังก์ชันนี้เหมือนเดิม ไม่ต้องแก้อะไร
5. `commit_death_and_prepare_hook(...)` — ของใหม่ ทำแค่ข้อ (2) คืน
   `(register, pending)` ให้ผู้เรียกไปยิง `fire_mob_death_hook` เองทีหลัง

เทสยืนยันของใหม่ (`test_the_split_call_lets_a_caller_close_the_gap`): เขียน
`self.mob_death_register` **ก่อน** เรียก `fire_mob_death_hook` แล้ว subscriber
เห็น `is_dead(...)` เป็น `True` ระหว่าง fire ทันที — ปิดช่องว่างได้จริงเมื่อลำดับถูก

## ทำไมไม่แก้เอง — บรรทัดที่ต้องแก้อยู่ใน `runtime.py` ทั้งคู่

การปิดช่องว่างจริงต้องเปลี่ยน**ลำดับสามบรรทัด**ที่ call site ทั้งสองใน
`runtime.py` (ไฟล์ของ chief สายนี้ห้ามแตะ):

**บรรทัด `5424-5426`** (กิ่ง diag) และ **`5484-5486`** (กิ่ง roster ปกติ) จาก:
```python
self.mob_death_register = mob_death.commit_death(
    self.mob_death_register, candidate,   # หรือ dispatch.step
)
```
เป็น:
```python
new_register, pending = mob_death.commit_death_and_prepare_hook(
    self.mob_death_register, candidate,   # หรือ dispatch.step
)
self.mob_death_register = new_register        # เขียนกลับก่อน
mob_death.fire_mob_death_hook(pending)        # แล้วค่อยยิง
```

การ `except mob_death.MobDeathContractError` ที่ครอบอยู่เดิมยังทำงานเหมือนเดิม —
`commit_death_and_prepare_hook` โยน error ตัวเดียวกัน ที่จุดเดียวกัน
(`REFUSE_REGISTER_STALE` ฯลฯ) ก่อนจะถึงบรรทัด `fire_mob_death_hook` เสมอ

## ขอ

CORE-REQUEST: สลับสามบรรทัดที่ `runtime.py:5424-5426` และ `:5484-5486` ตามด้านบน
(ใช้ `commit_death_and_prepare_hook` + เขียนกลับก่อนยิง) เมื่อสะดวก — ไม่ใช่
บล็อกเกอร์ของสายไหนตอนนี้ (ยังไม่มีใครลงทะเบียนบน point นี้จริง) แต่ถ้าไม่แก้
ไว้เป็นความเสี่ยงที่รอ subscriber ตัวแรกไปเจอเอง

-- LANE-B
