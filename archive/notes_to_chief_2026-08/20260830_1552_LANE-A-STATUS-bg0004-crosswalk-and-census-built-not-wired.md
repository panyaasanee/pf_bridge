[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ, สาย B | จาก: LANE-A (WORLD) รอบ `6p22bu` · 2026-08-30T15:52+07:00]

# LANE-A STATUS — รอบ `6p22bu`: crosswalk + census ของฉาก 4 (Slave Market Island) สร้างเสร็จ ยังไม่ต่อสาย

## สรุปหนึ่งบรรทัด

ทำตาม `COO-DECISION 2026-08-30T14:41+07:00` สร้าง crosswalk CLINE->MOBS + ตัวประกอบ census ให้ฉาก 4
เสร็จสมบูรณ์ (109/116 placement ขึ้นตัวได้ มีเทสคุมทุกด้าน รันจริงผ่าน encoder ตัวจริงแล้ว) แต่**ยังไม่ต่อสาย
เข้า path ที่ผู้เล่นเข้าถึงได้** ตามคำสั่ง COO เอง (ห้ามเปิด `login_entry_allowed` จนกว่าตัวประกอบพร้อมจริง) —
**ผู้เล่นจะไม่เห็นอะไรต่างจากเมื่อวานเลย**

## ทำอะไรไปบ้าง

1. **อ่านตารางเองจากไฟล์ต้นทางในเครื่องนี้ ไม่ได้ copy จากโมดูลพี่น้อง** — `CONSTDATA_TH__SCENE_NAME.tsv`
   (ฉาก 4: `n_CLINE_TYPE=4`, `n_SCENE_LV=45`), `CONSTDATA_TH__CLINE.tsv` (type 4 มี 61 แถว),
   `CONSTDATA_TH__MOBS.tsv`, `TEXTDATA_TH__MOBS_TIP.tsv`, `CONSTDATA_TH__STANDARD_MOB.tsv`,
   `gamedata/scene/bg0004/bg0004.placements.tsv` (116 แถว) — digest ทั้งห้าตารางที่ใช้ร่วมกับโมดูลอื่น
   ตรงกับที่โมดูลอื่นปักไว้ทุกตัว
2. **วัดได้ (ไม่ใช่เดา):** placement ทั้งหมด 116 → Mob-Set เลขต่างกัน 55 เลข → resolve ได้ 48 เลข
   (109 placement ขึ้นตัวได้) → resolve ไม่ได้ 7 เลข (7 placement ตกหล่น มีเหตุผลกำกับทุกตัวบน console)
3. หนึ่งตัว (leader 917, outfit `INVISIBLE`, ไม่มีชื่อใน MOBS_TIP) ขึ้นแบบไม่มีชื่อ — **แบบเดียวกับที่
   `world_port_royal_identity.py` ขึ้น leader ตัวเดียวกันที่ฉาก 1 อยู่แล้ว** ตัวนี้ตัวเดียวคิดเป็น 25 ใน 109
   placement ที่ขึ้นได้ (Mob-Set 107, instance 01-25)
4. พบความไม่ตรงกันในข้อมูลดิบสองแถว (82, 83): คอลัมน์ชื่อ free-text บอก "Mob_Set_34" แต่คอลัมน์
   `template_ids` ที่ parse มาแล้วบอก 45/46 — ใช้ `template_ids` เป็นหลัก (คอลัมน์เดียวกับที่
   `field_mob_tables_bg0002.py` ของสาย B ใช้เป็นหลักอยู่แล้ว) บันทึกความไม่ตรงกันนี้ไว้ ไม่ได้เงียบ ๆ เลือกเอง
5. สร้างและ**ทดสอบจริงกับ encoder ตัวจริง (`v141`)** แล้ว: `world_bg0004_identity.py` (ตาราง crosswalk)
   + `world_population_bg0004.py` (ตัวประกอบ census — ใช้ encoder ชุดเดียวกับทุกฉากพี่น้อง ไม่สร้างใหม่)
   ผลจริง: ประกอบ actor ได้ 109 ตัว จำนวนใน wire header ตรงกับ body 109 ตัวเป๊ะ ทุก console line
   เข้ารหัส cp874 ได้หมด
6. เพิ่มเทส `tests/test_world_bg0004_identity.py` (15 เทส/64 subtest) และ
   `tests/test_world_population_bg0004.py` (14 เทส/355 subtest) รวมเทสตรวจ regression GT-078 บน
   bytes จริงบน wire (ต้องเป็น `MOBS.n_ID` จริง ห้ามเป็นเลข Mob-Set ดิบ)

## ยังไม่ต่อสาย (ตามคำสั่ง COO)

`world_scene_travel.CENSUS_SOURCES`, `world_population_handoff.ROSTER_COMPOSERS`,
`lane_hooks/lane_a_scene_census.py` — ไม่แตะทั้งสามจุดรอบนี้ และ `login_entry_allowed` ของฉาก 4 ใน
`scenarios/world_scene_registry_001.json` ยังเป็น `false` เหมือนเดิม ตามที่ COO สั่งไว้ตรง ๆ
(`world_bg0015_identity.py`/`world_population_bg0015.py` ก็ผ่านแบบนี้มาก่อน — สร้างรอบ `w0pu2i` ต่อสาย
รอบ `ga91m5-r2` ห่างกันหลายรอบ — รอบนี้ทำครึ่งแรกแบบเดียวกันให้ฉาก 4)

## ผลข้างเคียงที่แก้ในรอบเดียวกัน (นอกเขตเขียนที่ระบุไว้ 4 จุด แต่เป็นหน้าที่ซ้ำที่ทุกสายต้องทำ)

โมดูลใหม่สร้าง actor entry เพิ่ม 1 จุด ทำให้ `tools/pf_runtimeres_actor_entry_static.py` ที่ปักเลขจาก
เนื้อหา `src/` เองต้องขยับ 3 ตัวเลข (17→18, 26→27, 16→17) — เป็นหน้าที่ที่ทุกสายก่อนหน้านี้ที่เพิ่ม actor
entry site ต้องทำเหมือนกันในคอมมิตเดียวกัน (`w0pu2i`, `y9s0xo`, `7ptoku` ทำแบบนี้มาก่อนทั้งหมด) —
`tests/test_static_verifier_pins_cloud.py` มีไว้จับสายที่ลืมขั้นตอนนี้พอดี แก้ครบ 3 จุดในคอมมิตนี้: ตัว
verifier เอง, สำเนาปักเลขใน `tests/test_runtimeres_actor_entry_static.py`, และ block JSON
`RUNTIMERES_COUNTS` ในรายงาน (เพิ่ม NOTE ต่อท้าย ไม่แก้ข้อความเดิม ตามธรรมเนียมไฟล์นั้น)

## ตัวเลขที่วัดได้

Placement: 116 ทั้งหมด / 109 ขึ้นตัวได้ / 7 ตกหล่น · Mob-Set: 55 ที่ใช้ / 48 resolve / 7 ไม่ resolve ·
multi-variant outfit: 9 เลข กระทบ 44 ใน 109 placement · เทสทั้ง repo server
(`python3 -m pytest tests -q`): **ผ่าน 5431 · skip 383 · subtest ผ่าน 9540 · ล้มเหลว 0** (118 วินาที) —
ก่อนแก้ pin ทั้งสามจุดข้างต้น รันเดียวกันล้มเหลว 11 (ทั้งหมดมาจากตัวเลข 3 ตัวที่โมดูลใหม่รอบนี้ทำให้ขยับเอง
ไม่มีอะไรอื่น) · จำนวน skip 383 เท่าเดิมก่อนรอบนี้ (ช่องว่าง capstone/image ที่รู้อยู่แล้ว)

## ยังไม่ได้พิสูจน์

การจับคู่ (Mob-Set เลขไหน = leader ตัวไหน) เป็น table inference ล้วน — ยังไม่มีมนุษย์ยืนอยู่ในฉากนี้เลย
(`status: never_sent_to_any_client_by_this_project` ในตาราง registry) ยังไม่เปิดใบเทสเพราะยังไม่มี path
เข้าถึงผู้เล่น · ว่า placement ที่หน้าตาเป็นมอนสเตอร์ (Scythe Beetle, Orc Chief, Dragon Gladiator ฯลฯ)
ควรเป็นฝ่ายศัตรูหรือไม่ เป็นการตัดสินใจของสาย B ไม่ได้ทำที่นี่ — เหมือนที่ PANYA-DECISION 2026-08-27
20:10 แบ่งงานไว้สำหรับฉาก 2

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี** — ประตูฉาก 4 ปิดเหมือนเดิม ไม่มี path ที่ผู้เล่นเข้าถึงได้เปลี่ยนพฤติกรรมรอบนี้

## CORE-REQUEST

ไม่มีรอบนี้

## ASK-COO ใหม่

ไม่มี (คำสั่ง COO รอบนี้ตอบคำถามที่ค้างจากรอบ `12lyda` ไปแล้ว)

## เปิดใบให้สาย C

ไม่มี

— LANE-A (WORLD)
