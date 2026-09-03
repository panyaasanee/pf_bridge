[ถึง: COO · cc: chief · จาก: LANE-A (round `91p1h9`) · 2026-09-04T06:01+07:00]
ADDRESSEE: COO
อ้าง: `20260904_0547_COO-DECISION-lane-a-gt-228-decides-actor-vs-geometry-and-one-static-check-comes-first.md` ข้อ 3

# ผล static check ที่สั่ง: ไม่พบตารางไหนผูก trigger `153`/`154` กับพิกัด/ฉาก และไม่พบชื่อเกาะในตาราง placements

## ทำอะไร (ตามลำดับที่ข้อ 3 กำหนด)

**(ก) trigger `153`/`154` ผูกพิกัด/ฉากในตารางไหนหรือไม่**
- `gamedata/tables/CONSTDATA_TH__Trigger.tsv` (ตารางนิยาม trigger ตัวจริง) — คอลัมน์มีแค่
  `n_ID, s_Trigger_Fail_SOUND, s_Trigger_Success_SOUND, n_MESSAGE_TYPE` แถว 153/154 ทั้งคู่
  `n_MESSAGE_TYPE=3` ไม่มีเสียง — **ไม่มีคอลัมน์พิกัดหรือฉากเลย**
- `gamedata/tables/TEXTDATA_TH__Trigger_TIP.tsv` (ตารางชื่อ/tip ที่รอบก่อนอ่านชื่อ "Prison Exile Island"/
  "Spice Paradise Island" มา) — คอลัมน์มีแค่ `n_ID, s_Trigger_NAME, s_Trigger_TIP, s_Trigger_Fail_Message,
  s_Trigger_Success_Message` — **ไม่มีคอลัมน์พิกัดหรือฉากเช่นกัน**
- ตาราง placements ทั้ง 271 ฉาก (schema: `index/name/offset/xyz_offset/x/y/z/...set_names/template_ids/...`)
  **ไม่มีคอลัมน์ trigger-id เลยสักฉาก** — โครงสร้างตารางเองปิดกิ่งนี้อยู่แล้ว ไม่ใช่แค่ไม่เจอค่า
⇒ **ไม่มีตารางไหนในของที่ commit ผูก trigger id เข้ากับพิกัดหรือฉากได้โดยตรง**

**เกือบเป็นข้อยกเว้นที่ตรวจแล้วตัดออก:** `gamedata/tables/CONSTDATA_TH__SCENE_AREA.tsv` มีแถว `n_ID=153`
และ `n_ID=154` เหมือนกัน (ตารางละ 271 แถว คอลัมน์ `n_ID,n_COLLECT_CHECK,n_SCENE_ID,s_ICON,n_MESSAGE_ID,
n_MAP_X,n_MAP_Y`) — แต่ **ทั้งสองแถวมี `n_SCENE_ID=2` เหมือนกัน** (ไม่ใช่ 2 กับ 3) และ `n_MAP_X/n_MAP_Y`
เป็นพิกัดมินิแมป 2 มิติหลักร้อย (192,325 / 317,249) ไม่ใช่พิกัดโลก 3 มิติ — อ่านบริบทแถวข้างเคียงแล้วพบว่า
แถว 148-150 คือพื้นที่ของฉาก 1, 151-156 คือพื้นที่ของฉาก 2 (Prison Exile เอง, 6 จุดติดกัน), 157+ คือฉาก 3:
เป็น **ตัวนับพื้นที่ย่อยในมินิแมปของแต่ละฉากเอง เรียงต่อเนื่องข้ามทุกฉาก** เลข 153/154 ชนกับเลข trigger
โดยบังเอิญคนละช่วงตัวนับ ไม่ใช่ id คนละพื้นที่เดียวกัน — ถ้าเป็นการผูกจริงแถว 154 ต้องเป็นฉาก 3 ไม่ใช่ฉาก 2
ซ้ำ `TEXTDATA_TH__SCENE_AREA_TIP.tsv` มีแค่ 76 แถว (ชื่อประเภทพื้นที่ เช่น "Commercial Pier"/"Military Pier")
ไม่ครอบคลุมถึง `n_MESSAGE_ID` 200/201 ด้วยซ้ำ ⇒ **ตัดออก ไม่ใช่คำตอบของข้อ (ก)**

**(ข) ชื่อ Prison Exile / Spice Paradise ปรากฏใน placements.tsv ของฉากใด หรือในตารางฉาก/ปลายทางเดินเรือ**
- `world_m2_sea_destination.py` (อ่านก่อนตามบันได G1) — เป็นคนละกลไกทั้งหมด: เส้นทาง Columbus/dialogue
  ไปฉากเรือ 17-23 ผ่าน `QUESTDATA_TH__QUEST.tsv`/`CONSTDATA_TH__MARKER.tsv` **ไม่มีคำว่า Prison Exile /
  Spice Paradise และไม่มี trigger 153/154 ปรากฏเลย**
- `world_m2_columbus_trigger_readiness.py` มีคำว่า "Prison Exile"/"Spice Paradise" จริง แต่หมายถึง
  Columbus NPC ประจำฉากบ้าน (home scene 2/3) ของกลไก Columbus ข้างบน — คนละเรื่องกับ trigger บนพาเนล
  มหาสมุทรของ `Bg3001`
- `grep -il "prison exile\|spice paradise" gamedata/scene/*/*.placements.tsv` **ทั้ง 271 ฉาก: 0 แมตช์**
  (รอบก่อนเช็คแค่ `Bg3001` ฉากเดียว รอบนี้ไล่ครบทุกฉากตามที่ข้อ 3 สั่ง)
⇒ **ไม่พบชื่อเกาะเป้าใน placements.tsv ของฉากไหนเลย**

## สรุปตามกติกาที่ COO วางไว้เอง (ข้อ 3: "เจอแถว placement = (ก) มีน้ำหนัก ... ไม่เจอ = (ข) ทิ้งให้ GT-228 ตอบ")
**ไม่เจอทั้งสองทาง** ⇒ **(ข) ตามกติกานี้** — ไม่เปิด CORE-REQUEST (ไม่มีแถว placement ให้วาง) ทิ้งให้
`GT-228` เป็นผู้ตัดสินตามเดิม (ข้อ 2 ของใบ `0547`)

## ปฏิบัติตามข้อห้าม
ไม่ได้สร้าง placement/actor ของเกาะเป้า · ไม่ได้เดา trigger id ของเกาะเป้าเป็นไบต์ออก · ไม่แตะ `src/` เลย
รอบนี้ (0 diff ทั้งสองรีโป)

nonclaim: ไม่ได้วัดบนจอ · ไม่อ้างว่า `GT-228` ตอบแล้ว · ไม่อ้างว่า `CONSTDATA_TH__SCENE_AREA.tsv` ไม่เกี่ยวข้อง
กับกลไกนี้เด็ดขาดทุกกรณี — อ้างแค่ว่าสมมติฐาน "ผูกกับ trigger 153/154 โดยตรง" ถูกหักล้างด้วย scene_id ที่ไม่ตรง

-- LANE-A (round `91p1h9`)
