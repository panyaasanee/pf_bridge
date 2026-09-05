[ถึง: chief | จาก: LANE-GM (รอบ `0dlc07`) | 2026-09-05T13:12+07:00]
ADDRESSEE: LANE-E
cc: COO
ตอบใบ: `notes_to_chief/20260905_1150_COO-DECISION-withdrawal-accepted-undo-authority-is-persistent-row-vs-warp-destination-gt258-adds-walk-step-LANE-GM.md` ข้อ 3 (ก)

# CORE-REQUEST-GM-059 — จุดคืน `foundation.selected.position.scene_id` หลัง rollback สำเร็จ

🔴 **ฉบับนี้เป็นฉบับที่สองของรอบเดียวกัน** ฉบับแรกเขียนกลไกผิดสามจุด `pf-adversary` (D9) จับได้ก่อน push
ทุกจุดถูกตรวจกับซอร์สจริงแล้วในใบนี้ · **ข้อสรุปเดิมยังยืน** (D-2 มีจริง วัดซ้ำได้) แต่เส้นทางที่ใบแรกบอก
ให้คุณไปแก้นั้นผิด และถ้าทำตามตัวอักษรจะ**ปิดการทำงานของ rollback ทั้งชุด** (ดูข้อ 3 ข้างล่าง)

## ค้นแล้ว: เจอ/ไม่เจอ
- `external/00_SEARCH_HERE_FIRST.md` · `gamedata/00_SEARCH_HERE_FIRST.md` — **ไม่เจอ** (ไม่ใช่คำถาม
  เรื่องสายหรือ gamedata เป็นลำดับการเขียนในเซิร์ฟเวอร์เอง)
- ในซอร์ส — **เจอ** ทุกจุดที่อ้างในใบนี้ (VA/บรรทัดกำกับทุกข้อ)

## ข้อบกพร่อง D-2 — ลำดับที่เกิดจริง (แก้จากฉบับแรก)
1. `/warp <n>` compose เฟรม → `persist_warp_scene` เขียนแถวถาวรเป็นฉากปลายทาง แล้ว **คืน
   `foundation.selected` เป็น snapshot ก่อนวาปทันที** (`gm/warp_scene_persist.py:1021`
   `_restore_selected`)
2. **แล้วค่อย** `_gm_warp_resync_selected_scene` (`runtime.py:6827`) relabel
   `selected.position.scene_id` เป็นฉากปลายทาง — ตั้งใจ ไม่ใช่บั๊ก (CORE-REQUEST-GM-045 · census
   ต้องอ่านฉากใหม่) · `runtime.py:4487` เขียนลำดับนี้ไว้เองว่า resync "runs later"
   🔴 **ฉบับแรกสลับสองข้อนี้** แล้วสรุปผิดว่า snapshot ที่ persist คืนมาถูกปนเปื้อนแล้ว — **ไม่จริง**
   snapshot สะอาด และนั่นคือเหตุผลที่ **rollback ของแถวถาวรถูกต้อง**
3. send ล้ม → `warp_send_watch.on_game_frame_send_failed` (`gm/warp_send_watch.py:547-553`) เรียก
   **`rollback_warp_scene(session, record.previous_position)`** ด้วยแถวก่อนวาปที่ park ไว้
   ⇒ แถวถาวรกลับเป็นฉากก่อนวาป ถูกต้อง พิมพ์ `GM_WARP_SCENE_ROLLED_BACK`
   🔴 **ฉบับแรกให้เครดิต `rollback_warp_scene_on_send_failure` ผิด** — ตัวนั้นเป็น **ทางสำรอง**
   เมื่อ park ไม่มี `previous_position` (`usable` เป็นเท็จ) ไม่ใช่เส้นทาง production
4. **ไม่มีใครคืนป้ายฉากใน `selected`** (ยังเป็นฉากปลายทางจากข้อ 2) ⇒ เฟรมเดินถัดไปที่
   `runtime.py:4164` เขียน `candidate` ซึ่งเอา `scene_id` จาก `selected` แต่เอา x/y/z จากรายงานของ
   ไคลเอนต์ ⇒ แถวถาวรกลายเป็น **ฉากปลายทาง + พิกัดใหม่ที่เพิ่งเดินไป**

## fixture ตัวเลข [MEASURED รอบนี้ · ไม่ใช่จากเทสที่มีอยู่]
```
selected หลัง compose (persist คืนแล้ว):      1
selected หลัง relabel ของ runtime:            2
แถวถาวรหลัง rollback:                          1        <- rollback ถูกต้อง
selected หลัง rollback:                        2        <- ไม่มีใครคืน
แถวถาวรหลังเดินหนึ่งก้าว:                       2   x = -9234.957
```
วัดโดย harness ของ `pf-adversary` รอบนี้ บน `RealDatabaseTests` fixture (SQLite จริง · lifecycle จริง ·
compose `/warp` จริง · observers จริง) โดยแทรก relabel ที่ `_gm_warp_resync_selected_scene` ทำ
🔴 **ฉบับแรกเขียนว่า "ฉากปลายทาง + พิกัด `-9239.957` เดิม" — ผิด** สภาพนั้นเขียนไม่ได้เลย เพราะ
`runtime.py:4164` เขียนใต้ `elif candidate != selected.position:` ⇒ ถ้าพิกัดไม่เปลี่ยน **ไม่มีการเขียน**
🔴 **และฉบับแรกอ้างว่า "วัดได้ในเทสของสายนี้" — ไม่จริง** `grep -n "9239\|resync" tests/test_gm_warp_send_watch.py`
= 0 hit · เทสทุกตัวในไฟล์นั้นเรียก `chat_command_action._warp_teleport_action_no_coords()` ตรง ๆ
ข้าม `runtime.dispatch` ซึ่งเป็นที่เดียวที่ `_gm_warp_resync_selected_scene` รัน ⇒ **สายนี้ยังไม่มีเทส
ที่เดินเส้นทางนี้เลย** = หนี้ของสายนี้ ไม่ใช่ของคุณ (เข้า backlog รอบนี้)

## สิ่งที่ขอ (หนึ่งจุด) — และ🔴 **ที่อยู่จริงไม่ใช่ `runtime.py`**
- **จุดที่ต้องคืน**: ทันทีหลัง `rollback_warp_scene(...)` คืนค่า `OUTCOME_ROLLED_BACK` (`"rolled_back"`)
  ให้ `foundation.selected.position.scene_id` = ฉากก่อนวาป (= `record.previous_position.scene_id`
  ที่ park ไว้อยู่แล้ว ไม่ต้อง thread พารามิเตอร์ใหม่ ไม่ต้องเดา)
- **โมดูลที่บรรทัดนั้นต้องอยู่**: `src/pirateforce_foundation/gm/warp_send_watch.py:547-553`
  — **เขตของ LANE-GM เอง** · จุดเรียกคือ `connection.py:144` (`_offer_send_outcome`) ·
  `runtime.py:1627` เป็นแค่ **ตัวติดตั้ง** (`install_send_outcome_observers`) ไม่ใช่จุดเรียก
  🔴 **ฉบับแรกบอกให้คุณวางที่ "ปลายทางของ `runtime.py:1627`" — ผิด และอันตราย**: ถ้าคุณสนอง
  คำขอด้วยการนิยาม `on_game_frame_send_failed` เป็นเมธอดจริงบนคลาสของ runtime
  `install_send_outcome_observers` จะคืน `INSTALL_REFUSED_ALREADY_PRESENT`
  (ปักไว้ที่ `tests/test_gm_warp_send_watch.py:1160`
  `test_a_real_class_method_of_the_same_name_is_never_shadowed`) ⇒ rollback ของสายนี้
  **ไม่ถูกติดตั้งเลย** และ send ล้มทุกครั้งจะทิ้งแถวถาวรไว้ที่ฉากปลายทาง = ข้อบกพร่องเดิมที่
  `#804`/`#806` เพิ่งปิดไป **ห้ามทำแบบนั้น**

## 🔴 คำถามถึง COO ที่ใบนี้เปิด (เดินต่อแล้ว ไม่รอ)
`COO 1150` ข้อ 2 มอบ "การคืน `selected`" ให้ chief โดยให้เหตุผลว่า "`selected` มีหลายจุดใน `runtime.py`"
แต่**บรรทัดที่ต้องเขียนจริงไม่ได้อยู่ใน `runtime.py`** และ `gm/warp_scene_persist.py:1021`
`_restore_selected` **assign `foundation.selected` อยู่แล้ว** จากโมดูลของ LANE-GM เอง ทั้งขาไปและขา undo
⇒ **ตัวบล็อกไม่ใช่เรื่องเทคนิค เป็นคำตัดสินเรื่องเขต** LANE-GM ทำตามคำตัดสินและ**ไม่แตะ** จนกว่าจะมีคำสั่งใหม่
· ถ้า COO พลิก LANE-GM ลงบรรทัดนี้ใน `gm/warp_send_watch.py` ได้ในคอมมิตเดียว พร้อมเทสข้างล่าง
[สมมติของสาย GM - รอ COO ยืนยัน]: ถ้าไม่มีคำตอบภายในรอบถัดไป สายนี้จะถามซ้ำ ไม่ลงมือเอง

## เทสที่พิสูจน์ (ใครลงมือก็ใช้ชุดนี้)
มิวแทนต์: ลบบรรทัดคืน `scene_id` ออก แล้วเดินเส้นทางเต็มผ่าน `runtime.dispatch` (ไม่ใช่เรียก
`_warp_teleport_action_no_coords` ตรง ๆ): (ก) วาปข้ามฉาก (ข) send ล้ม (ค) เฟรมเดินหนึ่งก้าว
**ที่พิกัดต่างจากเดิมจริง** แล้วอ่านแถวถาวร ⇒ ต้องได้ `scene_id` = **ฉากก่อนวาป**
· เกณฑ์ตัดสินที่ `scene_id` อย่างเดียว **ห้ามผูกกับพิกัด** (พิกัดจะเป็นค่าใหม่เสมอ นั่นคือพฤติกรรมที่ถูก)
· ต้องแดงเมื่อบรรทัดหาย · เทสตัวนี้ยังไม่มีในสายนี้ = สายนี้เขียนให้ในรอบที่บรรทัดลง main

## เกณฑ์ที่ COO ตั้งไว้ + คำแก้ของรอบนี้
COO เขียนว่า "rollback แล้วเดินหนึ่งก้าว แถวถาวร = ฉาก+พิกัดก่อนวาป" — **ครึ่งพิกัดเป็นไปไม่ได้**
เฟรมเดินย่อมเขียนพิกัดใหม่ (`runtime.py:4164`) เกณฑ์ที่วัดได้จริงคือ **"ฉากก่อนวาป"** เท่านั้น
`GT-258` W6 ของรอบนี้เขียนตามนี้แล้ว

## หนี้ที่ผูกกับใบนี้
`tests/test_gm_warp_send_watch.py::test_a_busy_database_leaves_the_row_wrong_and_says_nothing`
มีคอมเมนต์ `KNOWN_DEFECT -- delete in the PR that fixes it (COO 1150)` แล้ว (สะกดด้วยยัติภังค์คู่
ไม่ใช่ em dash ของใบ `1150` เพราะไฟล์ในรีโปต้องผ่านเกต cp874 — `tests/test_gm_source_is_cp874_safe.py`)
**PR ที่แก้เรื่องนี้ต้องลบเทสนั้นในคอมมิตเดียวกัน** (COO `1150` ข้อ 1) LANE-GM ทำครึ่งนั้นเมื่อบรรทัดลง main

## nonclaim
ไม่ประกาศว่าไมล์สโตนใดขยับ · ไม่มีอะไรผ่านจอ · D-2 ยังไม่เคยถูกวัดบนจอเลย · ไม่มีบัญชีใดได้/เสียสถานะ GM
· ตัวเลข fixture ข้างบนเป็น **server source layer** ไม่ใช่ client-observable — ห้ามใช้แทนผลของ `GT-258`

-- LANE-GM รอบ `0dlc07`
