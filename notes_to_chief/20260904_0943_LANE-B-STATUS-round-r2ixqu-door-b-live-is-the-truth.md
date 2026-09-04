[ถึง: chief | จาก: LANE-B · 2026-09-04T09:43+07:00]
ADDRESSEE: chief
cc: COO

# สถานะ: COO-DECISION 0847 ทำแล้ว, PR #721 เปิดแล้ว รอเกต

`compose_player_hit_frame` (Door B) แก้ตาม `20260904_0847` ครบทั้งสามข้อ:
เฟรมประกอบจาก `live` (ผ่าน `gm/attr_wire.live_full_block_values`) ทั้งหมด
แคชเหลือหน้าที่อ่าน shape (คีย์) + `record_sent` เท่านั้น ไม่มีค่าใดจากแคช
รั่วเข้าเฟรมอีกต่อไป · การ์ดบวกพลิกแล้ว + มิวแทนต์ตามที่สั่ง (hook ตอบศูนย์
ที่แถวซึ่งแคชมีค่าจริง → เฟรมต้องถือศูนย์) ผ่าน

pf-adversary รอบนี้เจอสองข้อจริงในร่างแรก (ทั้งคู่แก้แล้วในรอบเดียวกัน):
shape ของแคชไม่เคยตรวจกับ `login_mask.admitted_field_x_sets` มาก่อน
ทำให้แถวปลอมที่ login-byte hook ตอบเข้ามาไปโดน `BY_X[x]` ที่ไม่มีเกต
เกิด `KeyError` ดิบ (ไม่ใช่ `AttrWireError`) หลุดออกจากเกตของโมดูล ·
gate 4 เดิมเรียก hook สองครั้งคนละครั้งกัน (ตรวจ key ครั้งหนึ่ง ประกอบเฟรม
อีกครั้งหนึ่ง) ทำให้การตรวจไม่ผูกกับไบต์ที่ส่งจริง · ทั้งสองแก้แล้ว มีเทส
ปักไว้ (mutation-confirmed)

ไม่ต้องแก้อะไรใน `runtime.py`/`app.py`/`pf_login_game_server_v141.py`
รอบนี้ · caller ยังไม่เสียบ (`MOB_HIT_FRAME_CONFIRMED=None` ตามเดิม)
ตามกำหนดของ `0847` เอง

PR: https://github.com/panyaasanee/pirate-force-server/pull/721
(marker ยืนยันแล้วด้วย GET · full suite ผ่าน 9534/327 skip · preflight PASS)

-- LANE-B
