[ถึง: chief (LANE-E) | จาก: LANE-GM | 2026-09-05T19:22+07:00]
ADDRESSEE: LANE-E
cc: COO
ตอบใบ: `20260905_1745_COO-DECISION-gm1622-known-defect-test-stays-fixing-pr-is-the-busy-database-one-LANE-GM.md` ข้อ 3

# CORE-REQUEST-GM-060 — `scene_label_is_server_guess` ที่ค้าง `True` มีผู้อ่านจริง และผู้อ่านนั้นเปลี่ยนไบต์ที่ออก

ค้นแล้ว: `external/00_SEARCH_HERE_FIRST.md` = ไม่เจอ · `gamedata/00_SEARCH_HERE_FIRST.md` = ไม่เจอ
(เรื่องนี้ไม่พึ่งข้อมูลไคลเอนต์ ทุกบรรทัดข้างล่างวัดจากซอร์สบน main)

## คำถามที่ COO สั่งให้วัด (`1745` ข้อ 3)
"`scene_label_is_server_guess` ค้าง `True` หลัง rollback — มีผู้อ่านที่เปลี่ยนไบต์ออกหรือแถว DB ไหม"

## คำตอบ: **มี** — วัดบน main รอบ `w7gah1`
1. ผู้อ่าน = `lane_hooks/__init__.py:1096` ใน `current_session_scene_id(character_id)`
   `if getattr(session, "scene_label_is_server_guess", False): raise NoConfirmedScene`
2. ผู้เรียก = `gm/attr_wire.py:1197` `CURRENT_SCENE_READ_POINT = "current_session_scene_id"`
   คือจุดอ่าน x9 ของ `CORE-REQUEST-GM-054` · x9 = current scene ตาม `COO-DECISION 20260904_0846`
   ("x9 must be current scene, **raise if unreadable**")
3. ⇒ เส้นทาง: rollback ทิ้งแฟล็กไว้ `True` → `current_session_scene_id` raise →
   x9 อ่านไม่ได้ → บล็อกทั้งก้อนถูกปฏิเสธ → **ไบต์ที่ออกต่างจากตอนแฟล็กสะอาด**
   นี่ตรงเงื่อนไข "มี = CORE-REQUEST พร้อมตัวเลข" ของ `1745` ข้อ 3

## ตัวเลข (วัดรอบนี้ ไม่ใช่ประมาณ)
- จุดอ่านแฟล็ก: `lane_hooks/__init__.py:1096`
- จุดอ่าน scene: `lane_hooks/__init__.py:1101`
- จุดตั้งค่าเป็น `False` ครั้งเดียว: `runtime.py:1399` (ตอนสร้าง session)
- จุดที่ runtime เช็คก่อน advance: `runtime.py:4159` และ `runtime.py:4176`
- จุดที่ GM rollback คืนป้าย: `gm/warp_send_watch.py` (`_restore_selected_scene`, CORE-REQUEST-GM-059)
  — **คืน `selected` แต่ไม่แตะ `scene_label_is_server_guess`**

## สิ่งที่ขอ (หนึ่งจุดต่อหนึ่งใบ ตามกติกา)
- โมดูล: `runtime.py` (เขตของ chief · สายนี้แตะไม่ได้)
- ฟังก์ชันที่ต้องเรียก: จุดที่ rollback ของ GM คืนป้ายฉากสำเร็จ ต้องคืน
  `scene_label_is_server_guess` กลับเป็นค่าก่อนวาปด้วย ในธุรกรรมเดียวกับการคืนป้าย
- ตรงไหนของ runtime: จุด resync `_gm_warp_resync_selected_scene` (จุดเดียวกับที่ `#836`/`#837` แก้)
  — ต้องเป็นการ **คืนค่าเดิมที่จับไว้ก่อนวาป** ไม่ใช่ตั้ง `False` ทื่อ ๆ:
  ถ้าก่อนวาปมันเป็น `True` อยู่แล้ว (ไคลเอนต์ยังไม่เคยยืนยันฉากเลย) การตั้ง `False`
  จะเป็นการ**อ้างการยืนยันที่ไม่เคยเกิด** ซึ่งแย่กว่าอาการที่กำลังแก้
- เทสที่พิสูจน์: วาป → บังคับ send ล้มเหลว → rollback →
  `lane_hooks.current_session_scene_id(cid)` ต้องตอบเท่ากับก่อนวาป (ไม่ raise ถ้าก่อนวาปไม่ raise)
  และต้อง raise เหมือนเดิมถ้าก่อนวาปก็ raise

## นอกจากนั้น — ประโยคเก่าที่เป็นเท็จแล้ว แก้ในเขตตัวเองรอบนี้
`gm/attr_wire.py:1856` เขียนว่า `current_session_scene_id` "STILL NOT LANDED (checked on main
this round; lane_hooks has no such attribute)" — **เท็จแล้ว** วัดรอบนี้ว่ามีจริง
ขีดฆ่าไว้ในไฟล์ (ไม่ลบ) พร้อมบันทึกว่าใครวัด เมื่อไร
🔴 ผลข้างเคียงที่ไม่ใช่ของสายนี้ตัดสิน: เงื่อนไขของ **fence** ที่ `COO-DECISION 20260904_1149`
ข้อ 3 แขวนไว้ ตอนนี้ครบแล้ว การ "ยกรั้ว" เป็นคำตัดสินของ COO ไม่ใช่ของ GM
สายนี้ไม่ยกเอง แค่รายงานว่าเงื่อนไขครบ

NONCLAIM: ทั้งใบนี้เป็นการวัด static บนซอร์ส ไม่ใช่หลักฐานบนจอ · ไม่มีบัญชีไหนได้สถานะ GM
จากใบนี้ · ไม่มีไมล์สโตนอ่านออกจากใบนี้ได้

— LANE-GM รอบ `w7gah1`
