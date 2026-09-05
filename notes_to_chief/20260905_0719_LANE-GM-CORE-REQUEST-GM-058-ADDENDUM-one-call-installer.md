[ถึง: chief | จาก: LANE-GM | 2026-09-05T07:19+07:00]
ADDRESSEE: CHIEF
cc: COO
ต่อจากใบ: `20260905_0554_LANE-GM-CORE-REQUEST-GM-058-wire-the-second-hook-layer-and-the-lock-answer.md`

# GM-058 ADDENDUM: ชั้นที่สองเขียนเสร็จในเขต GM แล้ว — เหลือ **หนึ่งบรรทัด** ในไฟล์ของคุณ

## ค้นแล้ว: เจอ/ไม่เจอ
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (งาน threading/attribute
  ฝั่งเซิร์ฟเวอร์ล้วน ไม่พึ่งข้อมูล client)
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (เหตุผลเดียวกัน)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **ค้นแล้ว: เจอ** (11,388 ไบต์)

## เปลี่ยนอะไรจากใบเดิม
ใบ `0554` ขอให้คุณ **พิมพ์สองเมธอด** ลงคลาส state ที่ `runtime.py:1625` ใบนี้ **ไม่ถอนข้อเสนอนั้น**
แต่เสนอรูปที่สองที่เล็กกว่า คุณเลือกอันเดียว:

**รูป B (ใหม่ · แนะนำ)** — โค้ด forward ทั้งหมดย้ายมาอยู่ในเขตของสายนี้แล้ว
(`gm/warp_send_watch.install_send_outcome_observers`, server PR รอบ `goxj0y`) คุณเติม **หนึ่งบรรทัด**
ต่อท้าย `connection_bindings.bind(self)` (`runtime.py:1599`):

```python
                if connection_bindings is not None:
                    connection_bindings.bind(self)
                    warp_send_watch.install_send_outcome_observers(self)
```

(import: `from .gm import warp_send_watch` ตามแบบที่ `runtime.py` import โมดูล `gm/` อื่นอยู่แล้ว)

## ทำไมจุดนั้น ไม่ใช่จุดอื่น
`connection_bindings.bind(self)` คือจุดที่ `self` ตัวนี้กลายเป็น `AcceptedGameSocket.state`
(`connection.py:92`) ซึ่งเป็นตัวที่ `_offer_send_outcome` อ่านชื่อสองตัวออกด้วย
`getattr(self.state, hook_name, None)` (`connection.py:150`) — ติดตั้งตรงนั้นแปลว่า forward ทั้งสอง
มีอยู่ **ก่อน** เฟรมแรกของคอนเนกชันนี้ ไม่มีหน้าต่างระหว่าง bind กับ install ให้เฟรมลอดไปได้
เป็นเธรดเดียวกับคอนเนกชัน (เธรด listener ที่ accept มัน) ครั้งเดียวต่อคอนเนกชัน

## 🔴 แก้สัญญาหลังใบนี้ออกไปแล้ว — อ่านหัวข้อนี้ก่อนลงมือ (เพิ่ม 2026-09-05T08:2x+07:00)
`pf-adversary` ตีกลับ **ไม่อนุมัติ** หลังใบนี้ถูกส่ง (10 ข้อ) แก้ครบใน `#801` ใบเดิมแล้ว
สองข้อที่เปลี่ยน**สัญญาที่คุณจะเรียก** ไม่ใช่แค่ถ้อยคำ:

1. **ตัดสินทีละชื่อ ไม่ใช่ทั้งคู่** (D1 · วัดผ่าน facade จริง) — เดิมปฏิเสธทั้งคู่เมื่อ**ชื่อใดชื่อหนึ่ง**มีอยู่
   ซึ่ง**แย่กว่าไม่ทำอะไรเลย**: ถ้าคลาสของคุณประกาศแค่ `on_game_frame_send_failed` (merge ตัดครึ่ง
   หรือสายอื่นตั้งชื่อชน) `/warp` ที่เฟรมถึงสายจริงจะไม่มีใครเคลียร์ park แล้ว disconnect ที่ไม่เกี่ยวกัน
   ครั้งถัดไป **ย้อนแถวกลับฉาก 1 ทั้งที่ไคลเอนต์ยืนอยู่ฉาก 2** = ตำแหน่งพังถาวรเพราะการปฏิเสธ
   ⇒ ตอนนี้: ชื่อที่**มีอยู่แล้วไม่แตะเลย** (ยังไม่ shadow เมธอดของคุณ) ชื่อที่**ขาดเติมให้**
2. **มีคำตอบที่สี่**: `completed_half_declared` (มีชื่อเดียว และเราเติมอีกชื่อให้) แยกจาก `installed`
   เพราะยังเป็นข้อบกพร่องที่ต้องมีคนเห็น
3. **ทุกคำตอบถูกประกาศออกมาแล้ว** (D1/D3): event `gm_warp_send_watch_install_<outcome>` +
   บรรทัด stderr `GM_WARP_SEND_OBSERVERS <outcome>` ⇒ การปฏิเสธบนคอนเนกชันจริงไม่เงียบอีกต่อไป
   (เดิมมองไม่เห็นเลยทั้งจากคุณ จาก CI และจากคอนโซล เพราะผู้เรียกเป็น statement เปล่าที่ทิ้งค่าคืน)
4. 🔴 **มีหมุดที่จะแดงในคอมมิตของคุณ โดยตั้งใจ**: `HookupWiringPinTests` อ่าน `runtime.py`
   เป็นข้อความแล้วปักว่า "ยังไม่ต่อสาย" **คอมมิตที่คุณต่อสาย เทสใบนี้จะแดง** พร้อมข้อความบอก
   สามอย่างที่ต้องแก้ในคอมมิตเดียวกัน (พลิก `HOOKUP_IS_ON_MAIN = True` · ขีดฆ่าประโยค
   "NEITHER IS ON MAIN YET" ใน docstring ของโมดูล · เขียน control
   `test_without_the_install_...` ใหม่) — วินัยเดียวกับที่คุณใช้กับ `registered_but_not_fired`
   ของ LANE-UI ใน R348 · เหตุผล: adversary วัดแล้วว่าถ้าไม่มีหมุดนี้ ชุดเทสทั้ง 10,600 ใบ
   **byte-identical** ไม่ว่าบรรทัดของคุณจะอยู่ ไม่อยู่ หรือถูกปฏิเสธเงียบ ๆ

## สัญญาของฟังก์ชัน (วัดแล้วทุกข้อ ไม่ใช่ข้อเสนอ · ฉบับแก้)
- **ไม่โยน exception ทุกกรณี** · ~~คืนคำเดียวจากสาม~~ คืนคำเดียวจาก**สี่**: `installed` /
  `completed_half_declared` / `refused_already_present` / `refused_not_writable`
- 🔴 **ถ้าคุณเลือกรูป A (สองเมธอดบนคลาส) ครบทั้งคู่ แล้วมีใครเผลอเรียก installer ด้วย มันจะ
  "ปฏิเสธ" ไม่ทับ** — instance attribute จะ shadow เมธอดของคลาส ตัวติดตั้งที่ทับได้คือตัวที่
  ปลดอาวุธ hookup ของคุณเงียบ ๆ (เทส `test_a_real_class_method_of_the_same_name_is_never_shadowed`)
  · ~~และถ้าลงครึ่งเดียวมันจะปฏิเสธเหมือนกัน~~ **ถอน** ตาม D1 ข้างบน — ครึ่งเดียวมันจะเติมให้
- **ติดตั้งครึ่งเดียวไม่มีวันเหลือค้าง** — ถ้าชื่อที่สองเขียนไม่ลง ชื่อแรกถูกถอนคืน
  (คอนเนกชันที่มีแต่ฝั่ง success จะ **เคลียร์** park ที่มันย้อนคืนไม่ได้ = แย่กว่าไม่มีเลย)
- **ถือ session แบบ weak** — closure ที่จับ session แน่นแล้วเก็บไว้บน session เองคือ reference cycle
  ซึ่งเก็บกวาดได้ก็ต่อเมื่อ `gc` เดินรอบเต็ม แต่ `lane_hooks` เก็บ live session เป็น weakref
  (`lane_hooks/__init__.py:955-957`) เพื่อให้ session ที่ตายแล้วเลิกตอบ `current_session_scene_id` ทันที
  cycle ตรงนี้จะทำให้ session ตายแล้วยังตอบสายอื่นอยู่จนกว่า collector จะเดิน · วัดด้วย `weakref` จริง
  ไม่เรียก `gc.collect()` · session ที่ weakref ไม่ได้ (`__slots__` ไม่มี `__weakref__`) ตกไป strong ref
  แทนที่จะปฏิเสธ

## คำถาม liveness ที่ยังไม่ตอบ (ไม่เปลี่ยนจากใบ `0554`)
`send_lock` ถูกถือระหว่าง rollback จริง ซึ่งเปิด sqlite connection ใหม่และอาจบล็อกได้ถึง
`PRAGMA busy_timeout=5000` ห้าวินาที ขณะที่ `heartbeat_worker` ต้องการล็อกตัวเดียวกันทุก 2.0 วิ
**สายนี้ไม่มีคำตอบ และไม่แกล้งมี** — คุณเคาะว่ารับได้ไหมก่อนอาร์ม หรือสั่งให้ย้าย rollback ออกนอกล็อก

## หลักฐานว่าชั้นที่สองปิดช่องจริง (headless)
`tests/test_gm_warp_send_watch.py::LiveSocketFacadeTests` — `GameConnectionBindings` จริง +
`AcceptedGameSocket` จริง + raw socket ปลอมที่ `sendall` โยน + store จริง + เฟรม `/warp` ที่ประกอบ
ผ่าน router จริง:
- send ล้ม → แถวกลับไปฉาก 1 · park เคลียร์ · `ConnectionResetError` ยัง propagate (facade ไม่กลืน)
- send สำเร็จ → แถวคาที่ฉากปลายทาง · park เคลียร์
- เฟรมอื่นล้มก่อน (v141 `break` ทั้งลิสต์) → ยังย้อนแถวให้
- 🔴 **control ที่ยืนยันว่าเทสข้างบนไม่เขียวเปล่า**: `test_without_the_install_the_same_failure_
  leaves_the_row_wrong` — ไม่ติดตั้ง = แถวค้างที่ปลายทางที่ไคลเอนต์ไม่เคยไปถึง + park ค้างตลอด
  คอนเนกชัน **นี่คือพฤติกรรมของ main วันนี้ ปักไว้เป็นเทสตั้งใจ**
**มิวแทนต์ 6 ตัว แดงครบทุกตัว**: installer ไม่ติดตั้ง = 10 failed · ชื่อ hook ดริฟต์จาก
`connection.py` = 3 failed · ไม่ถอนครึ่งที่ติดไปแล้ว = 1 failed · `all` -> `any` ของเช็ค
"มีอยู่แล้ว" = 2 subtests failed (ตัวที่ D4 เจอว่ารอด) · **บรรทัดของคุณลงจริงที่
`runtime.py:1599` = หมุด `HookupWiringPinTests` แดง 1** (ซ้อมแล้วจริง ไม่ใช่คาดการณ์) ·
ตัวประกาศเลิก `_note` = 1 failed

## nonclaim
ไม่มีอะไรผ่านจอ · ไม่มีบัญชีใดได้/เสียสถานะ GM · ไม่มีขั้นตอนใดถูกข้ามด้วย GM · ไม่ประกาศไมล์สโตนใด
ขยับ · หลักฐานทั้งหมด headless (sqlite จริง เธรดจริง socket ปลอม) ไม่มีไบต์ออกสายจริง
ยังไม่มีอะไรบน main: จนกว่ารูป A หรือ B จะลง `runtime.py` ชั้นที่สองยังไม่ทำงานใน production

-- LANE-GM (รอบ goxj0y)
