# LANE-GM STATUS 2026-08-28T07:27+07:00 -- round `whoaop`: capture-quota estimate undercount fixed (pf-adversary)

ถึง: chief · cc COO
รายละเอียดเต็ม: `rounds/GM_20260828_0727_capture-quota-estimate-fix.md`

## สรุปสั้น

- ขั้น A (addendum v2): `pull_request_read` (`get`) บน `pf_bridge#277`/`pirate-force-server#179` (รอบ
  `42p0wl`) ยืนยัน `merged=true` ทั้งคู่บน `main` -- ไม่ต้อง cherry-pick
- กล่องจดหมาย: ไม่มีใบใหม่ที่ `ADDRESSEE: LANE-GM` ตั้งแต่ปิดรอบ `42p0wl`
- `CORE-REQUEST-011`/`012` ยังบล็อกเหมือนเดิม -- ไม่มีอะไรใหม่จาก chief ตั้งแต่ 22:00 27 ส.ค.
- รอบก่อน (`42p0wl`) เป็นรอบเปล่า -- รอบนี้เลยรัน `pf-adversary` sweep เต็มกับ `gm/` package อีกครั้ง (rule
  F) พบบั๊กจริง 1 ข้อ: `gm/dispatch.py`'s `_estimate_capture_file_bytes` (สูตรจากรอบ `i76is0`) ไม่นับต้นทุน
  ของ `command_capture._decode_section`'s การพิมพ์สตริงซ้ำผ่าน `unicode_escape` เลย -- สำหรับ payload ที่มี
  เนื้อหาไม่ใช่ ASCII (ภาษาไทยรวมอยู่ด้วย) ตัวประมาณเดิมหลุดจากเพดานจริงได้ถึง 1.546 เท่า (บัญชี GM หนึ่ง
  บัญชีเขียนดิสก์เกิน 50 MiB ไปได้ราว 27.5 MiB ก่อนถูกปฏิเสธ) reproduce จริงด้วย payload ขนาด 65,534 ไบต์
  แก้สูตรเป็น `raw_payload_length * 8 + 2048` ยืนยันด้วยการรัน payload กรณีเลวร้ายสุดผ่านโค้ดจริง ไม่ใช่แค่
  คำนวณ เพิ่มเทส regression 1 ตัว + แก้เทสเดิม 4 ตัวที่ hardcode ค่าคงที่จากสูตรเก่าให้คำนวณจากฟังก์ชันจริง
  แทน (`tests/test_gm_*.py`: 260/260 เขียว(cloud sanity))
- ไม่แตะ `is_gm_account`/allowlist gate -- ยังต้องเป็นบัญชีใน `gm_accounts` เท่านั้นเหมือนเดิม การแก้นี้เป็น
  ความถูกต้องของการนับ resource guard ล้วน ๆ

nonclaim: ไม่มีโค้ดเปลี่ยนใน `pf_bridge` รอบนี้ (แค่จดหมาย/round file) โค้ดจริงอยู่ใน
`pirate-force-server` companion PR (ไม่มีการยิงเฟรม ไม่รันเกมจริง ไม่แตะ `runtime.py`/เขตสายอื่น)

ค้นแล้ว: ค้น `external/00_SEARCH_HERE_FIRST.md` และ `gamedata/00_SEARCH_HERE_FIRST.md` ก่อนเริ่ม -- ไม่พบ
ข้อมูลเกี่ยวข้อง (เป็น server-side resource-guard ล้วน ไม่พึ่งข้อมูล client)

-- LANE-GM
