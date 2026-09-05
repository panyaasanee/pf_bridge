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
(`connection.py:87`) ซึ่งเป็นตัวที่ `_offer_send_outcome` อ่านชื่อสองตัวออกด้วย
`getattr(self.state, hook_name, None)` (`connection.py:150`) — ติดตั้งตรงนั้นแปลว่า forward ทั้งสอง
มีอยู่ **ก่อน** เฟรมแรกของคอนเนกชันนี้ ไม่มีหน้าต่างระหว่าง bind กับ install ให้เฟรมลอดไปได้
เป็นเธรดเดียวกับคอนเนกชัน (เธรด listener ที่ accept มัน) ครั้งเดียวต่อคอนเนกชัน

## สัญญาของฟังก์ชัน (วัดแล้วทุกข้อ ไม่ใช่ข้อเสนอ)
- **ไม่โยน exception ทุกกรณี** · คืนคำเดียวจากสาม: `installed` / `refused_already_present` /
  `refused_not_writable`
- 🔴 **ถ้าคุณเลือกรูป A (สองเมธอดบนคลาส) แล้วมีใครเผลอเรียก installer ด้วย มันจะ "ปฏิเสธ" ไม่ทับ**
  — instance attribute จะ shadow เมธอดของคลาส ตัวติดตั้งที่ทับได้คือตัวที่ปลดอาวุธ hookup ของคุณเงียบ ๆ
  (เทส `test_a_real_class_method_of_the_same_name_is_never_shadowed`)
- **ติดตั้งครึ่งเดียวไม่มีวันเหลือค้าง** — ถ้าชื่อที่สองเขียนไม่ลง ชื่อแรกถูกถอนคืน
  (คอนเนกชันที่มีแต่ฝั่ง success จะ **เคลียร์** park ที่มันย้อนคืนไม่ได้ = แย่กว่าไม่มีเลย)
- **ถือ session แบบ weak** — closure ที่จับ session แน่นแล้วเก็บไว้บน session เองคือ reference cycle
  ซึ่งเก็บกวาดได้ก็ต่อเมื่อ `gc` เดินรอบเต็ม แต่ `lane_hooks` เก็บ live session เป็น weakref
  (`lane_hooks/__init__.py:945`) เพื่อให้ session ที่ตายแล้วเลิกตอบ `current_session_scene_id` ทันที
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
มิวแทนต์ 3 ตัวแดงครบ (installer ไม่ติดตั้ง = 10 failed · ชื่อ hook ดริฟต์จาก `connection.py` = 3 failed
· ไม่ถอนครึ่งที่ติดไปแล้ว = 1 failed)

## nonclaim
ไม่มีอะไรผ่านจอ · ไม่มีบัญชีใดได้/เสียสถานะ GM · ไม่มีขั้นตอนใดถูกข้ามด้วย GM · ไม่ประกาศไมล์สโตนใด
ขยับ · หลักฐานทั้งหมด headless (sqlite จริง เธรดจริง socket ปลอม) ไม่มีไบต์ออกสายจริง
ยังไม่มีอะไรบน main: จนกว่ารูป A หรือ B จะลง `runtime.py` ชั้นที่สองยังไม่ทำงานใน production

-- LANE-GM (รอบ goxj0y)
