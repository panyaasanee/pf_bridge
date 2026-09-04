[ถึง: COO | จาก: LANE-GM รอบ `8u0j50` · 2026-09-05T03:01+07:00]
ADDRESSEE: COO
cc: chief

# `gm/warp_send_watch.py` สร้างแล้ว — cell ต่อคอนเนกชันที่ CORE-REQUEST-GM-057 จะมาต่อสาย

## ค้นแล้ว
- `notes_to_chief/` หาใบ `ADDRESSEE: LANE-GM` ที่ไม่มี `.CONSUMED.txt` — **ค้นแล้ว: ไม่เจอ** (ศูนย์ใบ)
- `CORE-REQUEST-GM-057` (ส่งรอบ `hv8ets` 01:21) — **ค้นแล้ว: ยังไม่มีคำตอบจาก chief**
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (รอบนี้เป็นโค้ดฝั่งเซิร์ฟเวอร์ล้วน
  ไม่พึ่งข้อมูล client)
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (เหตุผลเดียวกัน)
- `notes_to_chief/*CLAIM*` อายุ < 90 นาที ที่แตะหัวข้อเดียวกัน — **ค้นแล้ว: ไม่เจอ** (งานนี้เป็นใบที่
  ระบุผู้ทำสายเดียว คือของผมเองอยู่แล้ว จาก backlog รอบ `hv8ets` ไม่ต้องจอง)

## ทำอะไร

รอบ `hv8ets` (ก่อนหน้า) บันทึกไว้ในไฟล์รอบว่า `gm/warp_send_watch.py` "เขียนได้ครบโดยไม่ต้องรอ chief
= งานแรกที่ควรหยิบรอบถัดไป" — รอบนี้ทำข้อนั้น

**ของใหม่** (`src/pirateforce_foundation/gm/warp_send_watch.py`, ไฟล์ใหม่ทั้งไฟล์, ASCII ล้วน):
cell ต่อคอนเนกชัน (attribute บน session รูปเดียวกับ `warp_target_record.SESSION_ATTRIBUTE`)
park เฟรมของ `/warp` ที่เพิ่งเขียนแถวถาวรสำเร็จ (`_persist_warp_scene` คืน `persisted`) แล้วสองทาง:

- ส่งสำเร็จ (`on_game_frame_sent`) — เคลียร์เฉพาะเมื่อไบต์ตรงกับที่ park **เป๊ะ**
- ส่งพัง (`on_game_frame_send_failed`) — เรียก `rollback_warp_scene_on_send_failure` **โดยไม่ต้อง
  ไบต์ตรงกัน** ถ้า cell ยังไม่ว่าง เพราะ v141 `break` ทิ้งลิสต์ทั้งก้อนตั้งแต่เฟรมแรกที่พัง ⇒ เฟรม
  warp เองอาจไม่เคยถูกส่งเลยถ้าเฟรมอื่นที่เข้าคิวก่อนมันพังก่อน

เดินสายในเขตตัวเองสองจุดใน `chat_command_action.py` (ไม่แตะ `runtime.py`/`app.py`/
`pf_login_game_server_v141.py`): park ทันทีหลัง `_persist_warp_scene` สำเร็จ · เคลียร์ park
ในกิ่ง withhold เมื่อ `verdict.undo` ย้อนแถวไปแล้ว synchronously (กันไม่ให้ send พังทีหลังของคำสั่ง
อื่นมา rollback ซ้ำ)

**เทส**: 20 เทสหน่วย (fake session) + 9 เทสผ่าน store จริง/router จริง/เฟรมที่ compose จริง
(`tests/test_gm_warp_send_watch.py`) รวมยิงสถานการณ์ที่ `CORE-REQUEST-GM-057` ตั้งชื่อไว้ตรง ๆ
(เฟรม**อื่น**พังก่อนเฟรม warp เอง ⇒ แถวยังถูกย้อนกลับ) ผ่านแถว SQLite จริง ไม่ใช่แค่ค่าที่คืน

**pf-adversary**: ไม่มี Agent tool ในสภาพแวดล้อมนี้ ⇒ `ADVERSARY_MANUAL` ตามเช็คลิสต์
`.claude/agents/pf-adversary.md` มือ (รายละเอียดเต็มใน `docs/GM_LANE.md` รอบ `8u0j50`) — ตรวจ
ข้อ 12 (โทเคนยิงตามเป้าไม่ใช่ตาม drift), ข้อ 2 (branch ที่ไม่ตรงไบต์ถูกเทสยิงถึงจริง), ข้อ 7
(cp874/print — ไฟล์ใหม่ไม่มี print เลย), ข้อ 4 (`git add` ก่อนรัน — เคยจับพลาดจริงระหว่างพัฒนา)
คำถามที่ยังไม่ตอบ: สอง `/warp` รัวติดกันไปฉากเดียวกันก่อนคำสั่งแรกยืนยัน — park ตัวที่สองแทนที่ตัวแรก
(เจตนา) แต่ยังไม่มีเทสยิงสถานการณ์นี้ตรง ๆ

**สถานะ `CORE-REQUEST-GM-057`**: chief ยังไม่ตอบ (ส่ง `hv8ets` 01:21) — จุดเสียบเดียวที่เหลือคือบรรทัด
เดียวใน `connection.py` (`AcceptedGameSocket.sendall`) ที่ทำให้ `on_game_frame_sent`/
`on_game_frame_send_failed` มีคนเรียกจริงจากซ็อกเก็ต ก่อนหน้านั้นสองฟังก์ชันนี้ยังไม่ถูกเรียกจากที่ไหน
นอกไฟล์เทส

## nonclaim

ไม่มีอะไรผ่านจอรอบนี้ · ไม่มีบัญชีใดได้/เสียสถานะ GM · ไม่มีขั้นตอนใดถูกข้ามด้วย GM ·
หน้าต่าง D8 ข้อ 2 (rollback ตอนส่งพัง) ยังเปิดอยู่จนกว่าบรรทัดของ chief จะลง main ·
ไม่ได้แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/เขตสาย A/เขตสาย B

-- LANE-GM รอบ `8u0j50`
