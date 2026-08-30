[ถึง: chief · COO | ADDRESSEE: LANE-E, COO | cc: สาย B, สาย GM, เจ้าของ | จาก: LANE-A | 2026-08-30T13:5x+07:00, แก้ไขจากฉบับ 13:27]

# LANE-A STATUS -- `RE-156` ตอบแล้ว, แก้ไขหลัง `pf-adversary` จับข้อผิดพลาด CRITICAL ในฉบับร่างแรก; `GT-158` เปิดใหม่; `GT-134`/`RE-155` ยังรออยู่ที่เดิม

## สรุปหนึ่งบรรทัด

ฉบับร่างแรกของ `RE-156` ผิด (อ้างว่า "ไม่มี client->server byte พกเลขฉากเลย") `pf-adversary` จับได้ก่อนคอมมิต
แก้เป็นคำตอบเชิงบวกที่ถูกต้อง พร้อมเปิดใบใหม่ `GT-158` สำหรับคำถามที่ยังตอบไม่ได้จาก static

## สิ่งที่ผิดในฉบับร่างแรก และแก้อย่างไร

**อ้างผิด:** "0/14 `parse_*` functions มีฟิลด์เกี่ยวกับฉาก ⇒ ไม่มี byte แบบนี้เลย"
**วิธีที่ผิด:** grep คำว่า "scene" ในตัวฟังก์ชัน `parse_*` แต่ละตัวเอง -- จุดบอดคือฟิลด์อาจถูกตั้งชื่อว่า
scene โดยไฟล์อื่นที่*ใช้*ผลของ parse_ ไม่ใช่ตัว parse_ เอง

**ข้อเท็จจริงที่ถูกต้อง:** `current/pf_login_game_server_v141.py:3250-3284` `parse_action_vital`
return field `field_u16_4a` (offset `0x12`) ซึ่งถูก `src/pirateforce_foundation/action_ack.py:8-11,63`
ตั้งชื่อ/ใช้เป็น `scene_id` ตรงๆ และเดินสายจริงใน `src/pirateforce_foundation/runtime.py:247,6483-6501`
(หลัง flag `--scene-load-scenario`, `app.py:98,287-288`) แคปเจอร์จริงสองชุดเห็นค่าต่างกันตรงกับฉากจริง
ที่ต่างกัน (`PF_SCENE006...` = ฉาก 2, `PF_SCENE007...` = ฉาก 1) **แต่เป็นคนละ session** ⇒ ยังแยกไม่ออก
ว่าไคลเอนต์ติดตามฉากแบบสดจริง หรือค่าถูก bake ต่อการทดลอง

รายละเอียดเต็มพร้อมเลขบรรทัด/sha256 ทุกไฟล์ อยู่ในใบผลฉบับแก้:
`20260830_1327_RE-156-RESULT-no-scene-carrying-client-byte-teleport-check-echo-is-the-nearest-proxy.md`
(เขียนใหม่ทั้งฉบับ ไม่ใช่แค่แพตช์ประโยคที่ผิด)

**ขอให้ chief (ผู้เปิดใบ) ปิดหัวใบ `RE-156` ใน `CLIENT_RE_QUEUE.md`** ด้วยข้อความที่แก้แล้ว:
`RE-156 DONE (wire/DB layer) / POSITIVE-CANDIDATE-OUT-OF-DOMAIN-AND-UNVERIFIED-LIVE-TRACKING`
(ไม่ใช่ `DONE/BOUNDED-NEGATIVE` ตามที่ฉบับแรกเสนอผิด)

## ใบใหม่ที่เปิดรอบนี้: `GT-158`

เปิดใน `GAME_TEST_QUEUE.md` โดยตรง (แบบเดียวกับที่ `RE-155` เปิดโดยรอบ `lg1dvz`) เพื่อแยกคำถาม
client-observable ที่ static ตอบไม่ได้: `field_u16_4a` ติดตามฉากปัจจุบันแบบสดจริงหรือเป็นค่า bake
ต่อการทดลอง ต้องการ attended session ที่เดินข้ามฉากในหนึ่ง session แล้วเทียบค่า

## เรื่องแฟล็ก/โดเมน -- ทำไมสายนี้ไม่แก้เอง และไม่มี CORE-REQUEST

`action_ack.py`/กิ่ง `runtime.py:6483-6501` เป็นกลไกจริงที่เดินสายแล้ว แต่ (1) อยู่หลัง
`--scene-load-scenario` เท่านั้น ไม่ใช่บูตปกติ ตรงกับกฎ "ทำงานโดยไม่ต้องมีแฟล็ก" ของสายนี้เป๊ะ
แต่ (2) โมดูลนี้เป็นของโดเมน **combat** (`docs/FUNCTIONAL_COVERAGE.json`'s `combat` domain อ้างมันใน
`attack_command_producer`/`action_acknowledgement`) ไม่ใช่โดเมน world/travel ที่สายนี้ดูแล และ (3)
ปักไว้เป็น `HYP-PF-002 frozen` ⇒ **สายนี้ (WORLD) ไม่มีสิทธิ์และไม่มีแผนจะแก้/พลิกแฟล็กนี้เอง**
ไม่ยื่น `CORE-REQUEST` เรื่องนี้ เพราะ (ก) ไม่ใช่ไฟล์ `runtime.py`/`app.py` ล้วนๆ ที่ขอเป็นบรรทัดเดียวได้
โดยไม่เข้าใจ combat semantics ก่อน (ข) `GT-158` ยังไม่ตอบว่าค่านี้มีความหมายจริงหรือไม่ พลิกแฟล็ก
ก่อนรู้คำตอบนั้นเสี่ยงเป็น "แถวที่กุขึ้นเอง" ตามกฎของโปรเจกต์เอง **ส่งต่อให้ COO/chief พิจารณาว่าจะ
ให้สาย/ทีมที่ดูแล combat + `HYP-PF-002` รับไปพิจารณาต่อหรือไม่ หลัง `GT-158` มีคำตอบ**

## สองเรื่องที่ยังไม่ขยับ (เหมือนฉบับร่างแรก)

1. `GT-134` (Bg0015 first-eyes) -- precondition เคลียร์แล้ว (`#290` merge sha บน main ยืนยันแล้ว)
   ใบยัง `[READY]` รอ attended session เท่านั้น
2. `RE-155` (สี NPC/mob) -- ยัง `NEEDS-ATTENDED-CAPTURE`

## CORE-REQUEST

none.

## เปิดใบให้สาย C

`GT-158 ACTIONVITAL-FIELD-U16-4A-LIVE-SCENE-TRACKING-001` (`GAME_TEST_QUEUE.md`, เปิดโดยสายนี้)

— LANE-A (WORLD)
