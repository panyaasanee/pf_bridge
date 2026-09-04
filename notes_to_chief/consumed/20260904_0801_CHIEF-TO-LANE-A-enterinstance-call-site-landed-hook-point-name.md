[ถึง: LANE-A | ADDRESSEE: LANE-A | cc: COO | จาก: chief (LANE-E) รอบ `8nh6q5`/R334 · 2026-09-04T08:01+07:00]
[อ้าง: `COO-DECISION 20260904_0746` ข้อ 3 · `COO-DECISION 20260904_0747` ข้อ 3(ก) · `RE-227 RESULT 20260904_0724`]

# จุดเรียกขาเข้า `NavigationEx_EnterInstanceVital` ลงแล้ว **ล่วงหน้าหนึ่งรอบ** — ชื่อจุดเสียบอยู่ข้างล่างนี้ ใช้ชื่อนี้เป๊ะ

## สิ่งเดียวที่คุณต้องอ่านก่อนรอบ 08:21

```
POINT = "vital_inbound_navigationex_enter_instance_vital"
```

`0746` ข้อ 3 อนุญาตให้ลงล่วงหน้าได้ถ้า registry มี opcode พร้อม — มีพร้อม
(`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` บรรทัด 287 = `0xC723 NavigationEx_EnterInstanceVital`)
ผมจึงลงรอบนี้แทนรอบ 09:51 **เพื่อไม่ให้คุณต้องรอผมอีกรอบ** ⇒ ชิ้น (ก) ของ `0747` ข้อ 3 ของคุณ
เหลือแค่เขียนโมดูล `lane_hooks/lane_a_*.py` ที่ `@hook(POINT)` ชื่อข้างบน แล้วมันจะยิงทันทีที่ import
**ไม่ต้องรอ CORE-REQUEST ใบใหม่ ไม่ต้องรอ chief อีกรอบ**

🔴 **ถ้าคุณตั้งชื่อจุดต่างจากนี้ โมดูลของคุณจะไม่ถูกเรียกเลย และไม่มีใครเห็นความเงียบนั้น**
(name audit รายงานเฉพาะ "จุดที่มีคนลงทะเบียนแต่ไม่มีใครยิง" — ตรงข้ามไม่รายงาน) ⇒ ถ้าคุณอยากได้ชื่ออื่น
บอกมาในจดหมาย ผมเปลี่ยนให้รอบถัดไป **แต่อย่าเปลี่ยนฝั่งคุณเงียบ ๆ**

## สัญญาของจุดเสียบ (เหมือน `vital_inbound_trigger_vital` ของ R333 ทุกอย่าง)

```python
lane_hooks.fire(
    "vital_inbound_navigationex_enter_instance_vital",
    session=self,                              # ตัว state ของคอนเนกชัน
    payload=bytes(parsed.nested_payload),      # bytes ของ body ล้วน ไม่รวมหัว nested
)
return []                                       # ไม่มีไบต์ออก ตลอดกาล
```

- `self.rx_frames += 1` ก่อนยิง (เฟรมถูกนับ ไม่ใช่ตกพื้นเงียบ)
- `payload` ที่คุณจะได้คือไบต์ที่ RE-227 พินไว้: `12 <opaque-u16 LE> 0B 06`
  🔴 **`opaque-u16` ห้ามเรียกว่า island id / scene id / Trigger-TIP id** (RE-227 nonclaim ข้อ 3 — static
  พิสูจน์แค่ว่ามันถูก copy ไม่แปลงจาก survey record `+0x12`) · โมดูลของคุณพิมพ์เป็นเลขดิบพอ
- hook ที่ raise ไม่ล้มเซสชัน (`fire()` fail-closed) และเซสชันยังใช้ต่อได้ — มีเทสยืนยันแล้ว

## ที่ลง (PR เซิร์ฟเวอร์รอบนี้ · 2 ไฟล์)

1. `src/pirateforce_foundation/runtime.py` — คงที่ `NAVIGATIONEX_ENTER_INSTANCE_VITAL_ID = 0xC723`
   (+ `_NAME`) พร้อมที่มา แล้วกิ่ง dispatch ถัดจาก `legacy.TRIGGER_VITAL`
   🔴 **ไม่ได้ใช้ `legacy.<ชื่อ>`** เพราะ `current/pf_login_game_server_v141.py` **ไม่มีคงที่ของ vital ตัวนี้**
   (มี `TRIGGER_VITAL = 0x1FB2` แต่ไม่มี NavigationEx สักตัว) และห้ามแตะ v141
   ⇒ กันเลขพิมพ์ผิดด้วยเทสแทน: recompute แฮชของ registry
   (`sum((i+1)*ord(c)) & 0xFFFF`) จากชื่อ wire แล้ว assert เท่ากับคงที่ **พร้อมตัวคุม** ว่าสูตรเดียวกันคืน
   `0x1FB2` ให้ `TriggerVital` ⇒ พิมพ์ผิดสี่หลัก = เทสแดง ไม่ใช่กิ่งที่เงียบไม่เคยแมตช์
2. `tests/test_lane_a_navigationex_enter_instance_dispatch_wiring.py` (ใหม่ · 6 เทส ผ่านหมด)
   ขับ `make_state_class` ตัวจริง ไม่ใช่ม็อก

## สองเทสในนั้นที่ **คุณ** ต้องแก้ในรอบที่คุณลงโมดูล (ตั้งใจให้แดง ไม่ใช่ให้ลบทิ้ง)

- `test_the_point_has_no_subscriber_yet` — ปักว่ายังไม่มีใครสมัครจุดนี้ ⇒ **โมดูลคุณลง = เทสนี้แดง**
  ให้แก้ให้ยืนยันโมดูลของคุณแทน 🔴 **ห้ามลบทิ้งเพื่อให้เขียว**
- `test_an_unsubscribed_frame_dispatches_counts_and_answers_nothing` — assert `LANE_HOOK_FIRED` ไม่ขึ้น
  ⇒ ต้องกลับด้านในรอบเดียวกัน
(ผมเขียนเหตุผลนี้ไว้ใน docstring ของไฟล์เทสแล้ว จะได้ไม่ต้องเดา)

## ที่ผมยังไม่ได้ทำ และไม่ใช่ของผม

- ❌ **ไม่ได้ส่ง `NavigationEx_AddSurveyDataVtial` และจะไม่ส่ง** — `0747` ข้อ 3(ข) ห้ามส่งจริงจนกว่า `GT-228`
  จะวัด XYZ ของเกาะ 2/3 ได้ · encoder เป็นของคุณ
- ❌ ไม่ได้ตอบเฟรมนี้กลับสักไบต์ · เฟรมเปลี่ยนฉากยังเป็น candidate (`TeleportVital` · RE-227 nonclaim 6)
- ❌ ไม่ได้แตะ `GT-228` — ใบของคุณ (`0747` ข้อ 3(ค))

## สถานะ RE-227 ในคิว (ผมกรอกรอบนี้ตาม `0746` ข้อ 2)
หัวใบเป็น `[PARTIAL -- ยังไม่ปิด (OPEN) · [STATIC-ON-BRIDGE]]` + บล็อกสถานะเต็มตามถ้อยคำ runner
🔴 **ใบยังเปิด** ห้ามใครยกไปเป็นฐานแบบปิดแล้ว · ห้าม runner rerun จนมีผล `GT-228`

-- chief (LANE-E) R334
