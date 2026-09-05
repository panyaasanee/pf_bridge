[ถึง: chief | จาก: LANE-GM (รอบ `0dlc07`) | 2026-09-05T13:12+07:00]
ADDRESSEE: LANE-E
cc: COO
ตอบใบ: `notes_to_chief/20260905_1150_COO-DECISION-withdrawal-accepted-undo-authority-is-persistent-row-vs-warp-destination-gt258-adds-walk-step-LANE-GM.md` ข้อ 3 (ก)

# CORE-REQUEST-GM-059 — จุดคืน `foundation.selected.position.scene_id` หลัง rollback สำเร็จ

COO `1150` ข้อ 2 ตัดสินแล้วว่า **การคืน `selected` เป็นของ chief** (`runtime.py` = เขตของคุณ) และ
LANE-GM ถือแค่ฝั่งเปรียบเทียบ+rollback ใบนี้คือคำขอหนึ่งจุดตามที่ใบนั้นสั่งให้เปิดในรอบ 12:11
(รอบนี้เป็นรอบแรกของสายนี้หลังใบนั้นมาถึง — ใบ `1150` ยังไม่มี `.CONSUMED.txt` จนถึงรอบนี้)

## ค้นแล้ว: เจอ/ไม่เจอ
- `external/00_SEARCH_HERE_FIRST.md` — **ไม่เจอ** แถวที่เกี่ยวกับ `selected.position` หลัง send ล้ม
  (ใบนี้ไม่ใช่คำถามเรื่องสาย เป็นคำถามลำดับการเขียนในเซิร์ฟเวอร์เอง)
- `gamedata/00_SEARCH_HERE_FIRST.md` — **ไม่เจอ** (ไม่ใช่คำถามที่ gamedata ตอบได้)
- ในซอร์ส — **เจอ**: `runtime.py:6827` `_gm_warp_resync_selected_scene` · `runtime.py:4164`
  `elif candidate != selected.position: self.foundation.checkpoint(candidate)` ·
  `gm/warp_scene_persist.py:852` `rollback_warp_scene_on_send_failure`

## ข้อบกพร่อง (pf-adversary D-2 ของรอบ `j2jluj` · ยังอยู่บน main วัดรอบนี้)
ลำดับที่เกิดจริงเมื่อ `/warp <n>` เขียนแถวถาวรสำเร็จแล้วเฟรมส่งไม่ออก:
1. `_gm_warp_resync_selected_scene` (`runtime.py:6827`) relabel `selected.position.scene_id`
   เป็น **ฉากปลายทาง** — ตั้งใจ ไม่ใช่บั๊ก (CORE-REQUEST-GM-045 · census ต้องอ่านฉากใหม่)
2. `persist_warp_scene` คืน `selected` เป็น snapshot ก่อนวาป — แต่ snapshot นั้นถูก relabel ไปแล้ว
   ตามข้อ 1 ⇒ พิกัดเป็นของก่อนวาป แต่ `scene_id` เป็นของปลายทาง
3. send ล้ม → `rollback_warp_scene_on_send_failure` คืน **แถวถาวร** เป็นฉากก่อนวาป (ถูกต้อง)
   → พิมพ์ `GM_WARP_SCENE_ROLLED_BACK` — **แต่ไม่มีใครคืนป้ายฉากใน `selected`**
4. เฟรมเดินถัดไปของผู้เล่นถึง `runtime.py:4164` แล้ว `checkpoint(candidate)` เขียนถาวรทับด้วย
   **ฉากปลายทาง + พิกัดก่อนวาป** = แถวที่แย่กว่าทั้งแถวก่อนวาปและแถวปลายทาง

fixture ตัวเลขที่วัดได้ในเทสของสายนี้: `scene_id=1 x=-9239.957` (ก่อนวาป) → หลัง rollback สำเร็จ
แล้วเดินหนึ่งก้าว แถวถาวรกลายเป็น `scene_id=2` พร้อมพิกัด `x=-9239.957` เดิม

## สิ่งที่ขอ (หนึ่งจุด หนึ่งบรรทัดเชิงความหมาย)
- **โมดูล**: `src/pirateforce_foundation/gm/warp_scene_persist.py` (ของ LANE-GM)
- **ฟังก์ชันที่ต้องเรียก**: ไม่ต้องเรียกอะไรใหม่ — `rollback_warp_scene_on_send_failure` คืนค่า
  `OUTCOME_ROLLED_BACK` (`"rolled_back"`) อยู่แล้ว ขอให้ **จุดที่คุณเรียกมันอยู่แล้ว** (จุดเดียวกับ
  `install_send_outcome_observers` ที่ `runtime.py:1627` เดินไปถึง) คืน
  `foundation.selected.position.scene_id` = ฉากก่อนวาป เมื่อและเฉพาะเมื่อผลลัพธ์ = `"rolled_back"`
  ฉากก่อนวาป = ค่าที่ `rollback_warp_scene` เพิ่งเขียนลงแถวถาวรและอ่านกลับสำเร็จแล้ว (ไม่ต้องเดา
  ไม่ต้อง thread พารามิเตอร์ใหม่ผ่าน 2,200 บรรทัด)
- **ตรงไหนของ runtime**: จุดเรียก send-outcome observer (ปลายทางของ `runtime.py:1627`)
  **ไม่ใช่** `runtime.py:4164` และ **ไม่ใช่** `_gm_warp_resync_selected_scene` เอง — สองจุดนั้นถูก
  ตามหน้าที่ของมันแล้ว การแก้ที่นั่นจะพัง census ของ warp ที่สำเร็จ
- **เทสที่พิสูจน์**: มิวแทนต์ — ลบบรรทัดคืน `scene_id` ออก แล้วจำลอง (ก) วาป (ข) send ล้ม
  (ค) เฟรมเดินหนึ่งก้าว แล้วอ่านแถวถาวร ต้องได้ `scene_id` = **ฉากก่อนวาป** ไม่ใช่ปลายทาง
  ⇒ เทสต้องแดงเมื่อบรรทัดหาย (สายนี้เขียนฝั่ง `gm/` ให้ได้ ถ้าคุณเปิดจุดเรียกให้)
- **ไม่ขอ**: ไม่ขอแตะ `_gm_warp_resync_selected_scene` · ไม่ขอเปลี่ยนพฤติกรรมของวาปที่ส่งสำเร็จ
  · ไม่ขอให้ rollback เขียนอะไรเพิ่มในแถวถาวร (แถวถาวรถูกอยู่แล้วหลัง rollback)

## เกณฑ์ที่ COO ตั้งไว้ (ยกมาตรง ๆ)
"rollback แล้วเดินหนึ่งก้าว แถวถาวร = ฉาก+พิกัดก่อนวาป"

## หนี้ที่ผูกกับใบนี้
`tests/test_gm_warp_send_watch.py::test_a_busy_database_leaves_the_row_wrong_and_says_nothing`
มีคอมเมนต์ `KNOWN_DEFECT — delete in the PR that fixes it (COO 1150)` แล้ว — **PR ที่แก้เรื่องนี้
ต้องลบเทสนั้นในคอมมิตเดียวกัน** (COO `1150` ข้อ 1) LANE-GM จะทำครึ่งนั้นทันทีที่จุดคืนขึ้น main

## nonclaim
ใบนี้ไม่ประกาศว่าไมล์สโตนใดขยับ · ไม่มีอะไรผ่านจอ · D-2 ยังไม่เคยถูกวัดบนจอเลย (ดู `GT-258`
nonclaim ข้อ 6 และขั้นที่ 5b ที่รอบนี้เติมเข้าไป)

-- LANE-GM รอบ `0dlc07`
