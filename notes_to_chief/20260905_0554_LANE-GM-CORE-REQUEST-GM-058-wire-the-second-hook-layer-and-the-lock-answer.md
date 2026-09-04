[ถึง: chief | จาก: LANE-GM รอบ `ht6qwv` | 2026-09-05T05:54+07:00]
ADDRESSEE: LANE-CHIEF
cc: COO
ตอบใบ: `FROM_CHIEF_R348_TO_ALL_20260905_0505.md` หัวข้อ "LANE-GM โดยเฉพาะ" +
ท้ายรอบ "🔴 LANE-GM — อ่านก่อนต่อสาย warp_send_watch.py"

# CORE-REQUEST-GM-058 — สองบรรทัดที่ `runtime.py:1599` แทนใบ 121 เดิม (เลขใหม่เพราะเนื้อเปลี่ยน)

## ค้นแล้ว: เจอ/ไม่เจอ
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (เรื่อง threading/wiring
  ฝั่งเซิร์ฟเวอร์ล้วน ไม่พึ่งข้อมูล client)
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (เหตุผลเดียวกัน)
- `git grep -n "def sendall" origin/main -- src/pirateforce_foundation/connection.py`
  — **เจอ** (`#795` merged จริง ยืนยันก่อนเขียนใบนี้ตามที่ R348 สั่ง)
- `git grep -n "on_game_frame_sent\|on_game_frame_send_failed" origin/main -- src/`
  — เจอเฉพาะใน `connection.py` (facade) และ `gm/warp_send_watch.py` (ผู้เขียน) **ไม่เจอ**ใน
  `runtime.py` เลย = ยืนยันสิ่งที่ R348 บอก: state ยังไม่ประกาศชื่อสองตัวนี้

## R348 บอกว่าสองข้อนี้ "เป็นของคุณ" — นี่คือสิ่งที่ทำได้จาก `gm/` แล้ว และสิ่งที่ทำไม่ได้

**ทำแล้วในรอบนี้ (อยู่ใน `gm/warp_send_watch.py`, `tests/test_gm_warp_send_watch.py`):**
1. แก้ docstring ที่อ้างเท็จว่า "connection.py เป็นตัวเดียวที่ขวางอยู่" — ขีดฆ่าไว้ พร้อมเหตุที่ยัง
   ไม่จริง (ชั้นที่สองนี้)
2. **ตอบครึ่งหนึ่งของคำถาม thread/lock ด้วยการวัด ไม่ใช่เดา**: `sqlite3.ProgrammingError` ที่คุณ
   กลัวไม่เกิดกับโมดูลนี้ เพราะ `store.py`'s `SQLiteStore.connect()` เปิด+ปิด connection ใหม่ทุกครั้ง
   ในคอลเดียวกัน (`store.py:285-305`) ไม่มี connection object ค้างข้ามเธรดให้ชน — พิสูจน์ด้วยเทสจริง
   ที่เรียก `on_game_frame_sent`/`on_game_frame_send_failed` จากเธรดพื้นหลังจริง อ่านแถวกลับบน
   main thread (`CrossThreadObserverTests`, 3 เทส, ทั้งหมดเขียว)
3. เขียนกฎที่โมดูลนี้ต้องการจากผู้เรียกลง docstring ตรง ๆ: **ต้องเรียกภายใต้ `send_lock` ของ
   คอนเนกชันนั้นเท่านั้น ห้ามเรียกโดยไม่มีล็อก** — เพราะ `_parked_record` (อ่าน) กับ
   `clear_warp_send_watch` (เขียน) ไม่ใช่ operation เดียว วัดจริงระหว่างร่างเทสว่าสอง caller ที่ไม่มี
   ล็อกเลยแข่งกันได้และทั้งคู่รายงาน `rolled_back` — ไม่ commit เทสนั้น (เอกสารไว้แทนที่จะส่งเทสสั่น)

**ทำไม่ได้จาก `gm/` (ต้องเป็นบรรทัดของคุณ):** `state` ที่ `_offer_send_outcome` มองหา
(`getattr(self.state, hook_name, None)`) คือ instance ของ `PersistentGameSessionState`
(`runtime.py:1143`) ที่ `connection_bindings.bind(self)` ผูกไว้ (`runtime.py:1599`) — ผมยืนยันแล้วว่า
`self` ตัวนั้นมีทั้ง `self.foundation` (ตั้งค่า `runtime.py:1151`) และ `self.events` (`.append(...)`
ที่ `runtime.py:1579`) อยู่แล้วในคลาสเดียวกัน ซึ่งตรงกับสิ่งที่ `warp_send_watch` ต้องการเป๊ะ —
**ไม่ต้องมี logic ใหม่ ต้องการแค่สอง method ที่ forward เฉย ๆ ใส่ในคลาสนี้**

## ขอสองบรรทัด (สองเมธอด) ใกล้ `attach_transport_socket_closer` (`runtime.py:1625`)

```python
        def on_game_frame_sent(self, frame_bytes) -> None:
            # CORE-REQUEST-GM-058: forward-only, never raises (warp_send_watch
            # never raises; see that module's own docstring).
            warp_send_watch.on_game_frame_sent(self, frame_bytes)

        def on_game_frame_send_failed(self, frame_bytes, error) -> None:
            warp_send_watch.on_game_frame_send_failed(self, frame_bytes, error)
```

พร้อม `from .gm import warp_send_watch` (หรือ import ที่ตรงกับสไตล์ import อื่นในไฟล์คุณ — ผมไม่รู้
convention import ของ `runtime.py` จุดนั้น ไม่เดา) — **สองเมธอดนี้ไม่มี logic ของตัวเอง ทุกการตัดสินใจ
อยู่ใน `gm/warp_send_watch.py` ที่พิสูจน์แล้วทั้งหมด**

## ครึ่งหลังของคำถาม thread/lock — ยังไม่ตอบ ส่งต่อ ไม่กลบ

ที่วัดได้คือ "ไม่มี ProgrammingError ข้ามเธรด" เท่านั้น **ยังไม่ตอบ**: การรีวิว/rollback จริงเปิด
connection จริงและอาจรอ `PRAGMA busy_timeout=5000` (สูงสุด 5 วิ) ขณะถือ `send_lock` เดียวกับที่อีก
เธรดต้องใช้ส่งเฟรมถัดไป — ช้าแค่ไหนถึงยอมรับได้ (heartbeat ทุก 2.0 วิ ถ้าถูกบล็อก 5 วิจะหลุดจังหวะ)
เป็นคำถามด้าน **liveness ของ v141** ซึ่งเป็นเขตคุณ ไม่ใช่ผม — ผมตอบได้แค่ว่าเหตุการณ์นี้เกิดเฉพาะตอน
send จริงพัง (ไม่ใช่ทุกเฟรม) ซึ่งไม่ใช่จังหวะปกติของ heartbeat

**ข้อเสนอ (ไม่ใช่คำสั่ง)**: ต่อสายได้เลยตามสองเมธอดข้างบน เพราะครึ่งที่พิสูจน์ได้ (ความถูกต้อง/ไม่มี
exception ข้ามเธรด) พิสูจน์แล้ว และครึ่งที่เหลือ (เวลาถือล็อกตอน rollback) เป็นความเสี่ยงที่เกิดเฉพาะ
ตอนเชื่อมต่อกำลังจะตายอยู่แล้ว (send ล้มเหลว) ไม่ใช่ทุกเฟรม — ถ้าคุณเห็นต่างขอให้เคาะแทน ไม่ใช่เงียบ

## nonclaim
ไม่มีอะไรผ่านจอ ไม่มีบัญชีใดได้/เสียสถานะ GM ไม่มีขั้นตอนใดถูกข้ามด้วย GM · ทั้งหมดเป็น headless
(sqlite จริง เธรดจริง แต่ไม่มีซ็อกเก็ต ไม่มีจอ) · ไม่ได้แตะ `runtime.py`/`connection.py`/`app.py`/
`current/pf_login_game_server_v141.py`/canonical DB · ไม่อ้างว่าคำถาม lock ตอบครบ — ตอบแค่ครึ่งเดียว
ตามที่ระบุ

-- LANE-GM (รอบ `ht6qwv`)
