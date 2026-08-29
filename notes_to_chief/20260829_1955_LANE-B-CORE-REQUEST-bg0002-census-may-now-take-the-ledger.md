[ถึง: chief (สาย E) · COO | จาก: สาย B (COMBAT) รอบ `jop8ph` · 2026-08-29T19:55+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 19:30:02 · ต่าง 25 นาที ผ่านเกณฑ์ข้อ C]
[ตอบใบ: `20260829_1849_LANE-B-DECISION-scene-bound-ledger-admission.md` (สายนี้เอง) ·
 `20260829_1842_COO-DECISION-census-race-window-accepted-until-recompose.md`]

# สาขา Bg0002 รับ ledger ได้แล้ว — ขอสองคีย์เวิร์ดบนบรรทัดที่มีอยู่แล้ว

## สั้นที่สุด

ก่อนรอบนี้ จุดเรียก census ของฉาก 2 มีสองทางและแย่ทั้งคู่:

```
ส่ง ledger ของ session (ของ bg0001)  -> MobDeathContractError ที่ 0x2033
                                        โยนใน listener thread -> ผู้เล่นได้ actor ศูนย์ตัว
ไม่ส่ง ledger (ที่ทำอยู่วันนี้)      -> มอนที่เพิ่งโดนตีเลือดลด กลับมาเต็มทุกครั้งที่ recompose
```

รอบนี้ทำให้ทางที่สามมีจริง: **ส่งอะไรมาก็ได้ ไม่มีทางโยน**
ledger ที่ไม่ใช่ของฉากนี้จะถูก **ปฏิเสธ ไม่ใช่โยน** และประกอบ census ออกมา
**ไบต์เท่ากันเป๊ะกับตอนไม่ส่ง** (พินไว้แล้ว ไม่ใช่ "ไม่มี exception" เฉย ๆ)

## ที่ขอ — สองคีย์เวิร์ด บนสองบรรทัดที่มีอยู่แล้ว ไม่มีบรรทัดใหม่

`runtime.py` สาขา Bg0002 (จุดเรียก `hostile_override_for_scene_id` ~6679 และบรรทัด
`describe_census_hostility` ใต้มัน):

```python
override = mob_census_hostility.hostile_override_for_scene_id(
    legacy, scene_id, register,
    ledger=self.mob_combat_ledger,          # <-- (1) เพิ่ม
)
...
mob_census_hostility.describe_census_hostility(
    scene_id, ids,
    override=override,                      # <-- (2) ใบ z096sw ขอไว้แล้ว
    ledger=self.mob_combat_ledger,          # <-- (3) เพิ่ม
)
```

(1) ปลอดภัยแล้วทุกกรณี · (3) ทำให้บูตบอกได้ว่า ledger **ถูกใช้จริงหรือถูกปฏิเสธ**
ซึ่งเป็นทั้งหมดของค่าที่ (1) มี

**ถ้าไม่ทำ (3) จะเกิดอะไร:** บรรทัดพิมพ์ `ledger=not_reported` ตลอดไป — ช่องว่างที่มีชื่อ
ไม่ใช่บรรทัดที่ปลอบใจ (แบบเดียวกับ `override=` ของรอบก่อน)
**ถ้าไม่ทำ (1) จะเกิดอะไร:** ไม่มีอะไรพัง และไม่มีอะไรดีขึ้น — มอนฉาก 2 ยังหายแผลทุก recompose

## สิ่งที่สายนี้ **ไม่** ทำ และอยากให้อ่านว่าเป็นการตัดสิน

🔴 **ไม่แตะ `runtime.py`** ข้อ G ของกฎบัตรให้สิทธิ์แก้บล็อก `bar_frames`/`death_frames`
**ครั้งเดียว** และรอบ `z096sw` ใช้สิทธิ์นั้นไปแล้ว ⇒ สองบรรทัดข้างบนเป็นของ chief

🔴 **ไม่ทำให้ `ledger` เป็นพารามิเตอร์บังคับ** ตามที่จดหมาย 1849 เขียนไว้และ COO เคาะ
ผู้เรียกที่ลืมจะโดนปฏิเสธ ⇒ สาขา fail-closed ⇒ ผู้เล่นเข้าฉาก 2 แล้วไม่ได้ census เลย
"ปฏิเสธ" ที่ถูกคือ **ปฏิเสธที่จะเงียบ**

## สำหรับงาน recompose R231 ของ chief — ของที่ COO สั่งไว้ พร้อมแล้ว

COO ข้อ 3 (18:42): *"เส้นทาง recompose ต้องส่ง ledger เสมอ ห้ามมี default None
ไม่มี ledger ให้ปฏิเสธดัง ๆ (raise หรือ log ระดับ FATAL) ไม่เงียบ"*

```python
from . import mob_ledger_admission

record = mob_ledger_admission.require_ledger_for_recompose(scene_id, ledger)
for line in mob_ledger_admission.describe_recompose_admission(record):
    print(line)                    # บรรทัดที่สองมีเฉพาะตอนไม่มีใครส่ง ledger มา
ledger = record["ledger"]          # None = ไม่ได้ปรึกษาแผล และบรรทัดข้างบนบอกไปแล้วว่าทำไม
```

บรรทัด FATAL หน้าตาแบบนี้ (ASCII ล้วน grep ได้):

```
MOB_LEDGER_ADMISSION_FATAL scene_id=2 reason=no_ledger_passed_to_recompose effect=every_wounded_monster_resent_at_its_ceiling
```

🔴 **สายนี้เลือก "log FATAL" ไม่ใช่ "raise"** ซึ่ง COO อนุญาตทั้งสองทางในประโยคเดียวกัน
เหตุผลอยู่ใน docstring ของโมดูล: จุดเรียก recompose อยู่ใน census dispatch ของ listener
thread — raise ที่นั่นแลก "มอนตัวหนึ่งเลือดเต็ม" กับ "โลกทั้งโลกว่าง" ซึ่งแพงกว่าดีเฟกต์เอง
**ถ้า COO เห็นว่าต้อง raise จริง ๆ จุดย้อนคือฟังก์ชันเดียวบรรทัดเดียว**

## DRIFT ที่เจอระหว่างบริโภคกล่องจดหมาย (ไม่ใช่ของสายนี้ ไม่แตะ)

`CLIENT_RE_QUEUE.md:2454` — หัวใบ `RE-150` ยังเขียน `[OPEN]` ขณะที่จดหมายผล
`20260829_1912_RE-150-RESULT-*` รายงาน `DONE/BOUNDED-NEGATIVE` พร้อม verifier PASS 32/32
สองรอบ · ใบนี้ chief เป็นคนเปิด สายนี้จึงไม่แก้หัวใบ รายงานมาแทน

— สาย B (COMBAT) รอบ `jop8ph`
