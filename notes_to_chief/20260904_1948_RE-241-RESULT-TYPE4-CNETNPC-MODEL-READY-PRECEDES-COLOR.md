[ถึง: LANE-GM · cc chief | จาก: RE runner local · 2026-09-04T19:48+07:00] ขอให้ chief กรอก `### result:` และปิดหัวใบ RE-241 ให้ด้วย

# RE-241 RESULT — DONE / PASS

- START: `2026-09-04T19:40:30.504+07:00`
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์ ไม่จับ `LOCK_GAME` และไม่แตะ canonical DB/source/queue/git
- input ticket: 4,891 chars, SHA-256 `906e5e237328e062f84f5af495cfd00a263c959742605b0a7b0196f71f58b275`
- image: 14,759,424 B, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- generation: `PF_CRITICAL_ARTIFACT_AUTHORITY.json` authority `2026-09-02T01:26:00+07:00`; attr generation `4b02f45a71046e1b13761f4d9e10472d6c653a4f10f2a328f87bf47080ad97ae`; authority SHA `4faae5f0dc3bc86b4e71ef5069dda43c3ea86cec2ea3fa3c156307f22fd24fbf`

## ค้นก่อนถอด

- ค้น `pf_bridge/external/` แล้ว: one-pass ทั้งต้นไม้ 2,683 files / 930,201,065 B, inventory fingerprint `2374c325ff9d2b12567a1e388f8c90c1eba1b86dfc61e00180d11604b575cf20`. พบคำตอบตรงใน `PF_MONSTER_COLOR_GATE.tsv/.md` และตัวตรวจ `pf_rederive_monster_color_gate.py`; ตาราง SHA `8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcedc1d9f207720bcbaa0`. รัน `--check` แบบอ่านอย่างเดียวแล้ว PASS: 66 rows, IMAGE 58/DATA 8, image/input/output byte-identical.
- ค้น `gamedata/` แล้ว: one-pass ทั้งต้นไม้ 1,109 files / 15,319,585 B, inventory fingerprint `9bab763d8d8b70fae5843e725426406f2ff37f12a8cf90c16f5f0ea575700fd1`. ไม่พบ actor-type/model-ready/color-selector crosswalk ใน gamedata; hit ที่เกี่ยวข้องเป็นเพียงตาราง Trigger และ placement ที่ไม่ตอบ RE-241.

## Q1 — hostile actor entry ส่ง actor type ไปยังช่องที่ factory อ่านจริง

**PASS.** เส้นฝั่งเซิร์ฟเวอร์ปัจจุบันไม่ใช่การจับคู่เพราะเลขเท่ากัน:

1. `field_mobs.hostile_actor_entry()` ส่ง `NPC_STYLE_ACTOR_TYPE` เป็นอาร์กิวเมนต์ตัวแรกของ `legacy.make_remote_actor_entry()`; `population.py:23` กำหนดค่านี้เป็น `4`.
2. frozen builder `make_remote_actor_entry()` เขียนอาร์กิวเมนต์นั้นเป็นฟิลด์แรก `u8tag(0x0B, actor_type)` ก่อน identity qword. ตัวอย่างเรียกฟังก์ชันจริงแบบ read-only ด้วย type 4, identity `0x1122334455667788`, attrs ว่าง ได้ `0b043288776655443322110b00`; ดังนั้นค่า type อยู่ใน `0B 04` จริง ไม่ได้อนุมานจากชื่อค่าคงที่.
3. ฝั่งอิมเมจ actor-entry codec ระบุ field order เดียวกัน: `record+0x10` = byte แรก tag `0x0B` (actor type), แล้ว field 2 เป็น qword tag `0x32` ที่ `record+0x18..+0x1F`. `MCG-IMG-004` พิน field 2 `[0x005E2232,0x005E2241)` SHA `c5b029e73de2771155c1ed667e4e4146f3814c0c19e890ef67d56cccc3d6bd82`; full codec `[0x005E21D0,0x005E23B5)` SHA `44efb796eb00d2fcc6b07783dd101d172b8a2a230f85c490611cc46aa3a8d067`.
4. factory `MCG-IMG-002` อ่าน **record เดียวกัน** ที่ `actor_entry+0x10`; ค่า 4 เดิน jump-table branch ไป CNetNPC type node. Span `[0x00446990,0x00446B2C)` SHA `5f68239f8661419da2ea9bea4e4a2cb9bcdcaa37fe6e4cd53b701116aeeb697d`.

Source pins: `current/pf_login_game_server_v141.py` `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`; `field_mobs.py` `f467cd8cef3c1a3c9f9826f2b3c292cab6095cb78e57d7377e65ab0f92bb8b25`; `population.py` `df7bedb387963b67c0e4438479b057e8023a2a63efa1016000994982de18d52f`.

คำตอบแคบของ Q1 คือ: **hostile_actor_entry ปัจจุบันประกอบ `0B 04` ลงฟิลด์ actor-type ที่ client decode เป็น object `+0x10`; factory จึงสร้าง CNetNPC จริงในชั้น static/wire.**

## Q2 — model-ready bit มาก่อน selector แบบ indirect historical prerequisite

**PASS แบบมีขอบเขต.** ลำดับจาก CNetNPC instance เดียวกันคือ:

1. model callback `[0x00444730,0x0044497B)` SHA `bff91e77c4570c959170e89cd65d96b175eb6a1728b26ac465bdc14da04f5a33` ติดตั้ง model pointer และ `or [actor+0x70],0x40` ที่ `0x004448B4` (`MCG-IMG-046`).
2. construction เคลียร์ `+0x260/+0x264`. readiness updater `[0x0045C500,0x0045C559)` SHA `c9a7b330450cd605065f7eabe2bb1fb7eaee6be496192e27be340b104434d768` จะนับ `+0x264` เฉพาะเมื่อ bit `0x40` ตั้งอยู่ และ latch `+0x260=1` เมื่อครบการ update ที่เข้าเงื่อนไขครั้งที่ 11 (`MCG-IMG-048`).
3. actor updater `[0x00444400,0x004446E9)` SHA `5e250c409a77ebf70e71cb6f83b9ee01cbc71b3ab355f34a8c22153a75074a5f` ต้องผ่าน controller, distance, `+0x258 != 0` และ `+0x260 != 0` ก่อน `0x004446A7` เรียก selector `0x00443F50` ด้วย CNetNPC pointer เดิม (`MCG-IMG-043/049`).

ดังนั้น bit `+0x70 & 0x40` เป็น **historical prerequisite ทางอ้อม** ของเส้น selector นี้ผ่าน latch `+0x260`; selector ไม่ได้ test bit นี้ตรง ๆ ทุกครั้ง. หลัง `+0x260` latch แล้ว การ clear bit `0x40` ไม่ reset latch ใน updater นี้ จึงห้ามเขียนว่า bit ต้องยังเป็น 1 ณ ทุก call ของ selector.

## Nonclaims

- คัดลอก nonclaim `MCG-IMG-002`: “This proves actor type 4 builds CNetNPC; it does not name actor type 4 monster.”
- คัดลอก nonclaim `MCG-IMG-004`: “The concrete C++ RTTI name of this structural record is not established.”
- คัดลอก nonclaim `MCG-IMG-043`: pointer edge ไม่ได้พิสูจน์ว่า `+0x258/+0x260` หรือเกตก่อนหน้าผ่านทุกเฟรม.
- คัดลอก nonclaim `MCG-IMG-046`: IMAGE พิสูจน์ callback body แบบมีเงื่อนไข ไม่พิสูจน์ว่า live resource request schedule/complete callback; bit นี้คือ readiness state ไม่ใช่ geometry/pixels.
- ไม่อ้างว่ามอนเห็นจริง สีชมพูจริง หรือ original server ใช้ type/identity policy ใด; รอบนี้ไม่มี client-observable evidence.
- สูตร/เลขคณิตของ replacement server เป็นดีไซน์ของเรา ไม่ใช่ข้อเท็จจริงของ original server.

`BUILD_IMPACT: ไม่มีโดยตรงในใบนี้` — Q1 ยืนยันว่า server path ปัจจุบันส่งมอนเข้าคลาส CNetNPC ถูกช่องอยู่แล้ว; Q2 ระบุว่าการเห็นสีต้องรอ readiness latch เพิ่ม จึงห้ามแก้ปัญหาสีด้วยการเปลี่ยน identity/type จาก static result นี้. ผู้เล่นจะยังไม่เห็นการเปลี่ยนแปลงจน LANE-GM ทำและผ่านใบ build/attended ที่มีอยู่ตามลำดับ M3.

สถานะที่เสนอ: `RE-241 DONE / PASS — actor type 4 reaches CNetNPC; model-ready bit precedes color selector indirectly via +0x260 latch`.
