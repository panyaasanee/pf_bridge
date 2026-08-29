[ถึง: chief · สาย A · RE runner | cc COO · Panya | จาก: เซสชัน attended กะ1 | 2026-08-27 03:35 (+07:00) | ภาคผนวกของ `20260827_0310_PANYA-DECISION-*` ข้อ ①]

# ADDENDUM — เบาะแสสำหรับใบ RE ใหม่ต่อจาก `RE-093`: "Navy Transfer ที่ P0" มาจาก join ด้วยเลขเท่ากันในตารางแช่แข็งของเรา ไม่ได้มาจากไคลเอนต์

Panya ถาม 03:2x: "อะไรตอนนี้ที่ทำให้ต้องเป็น Navy Transfer มาเกิดที่ xyz นี้ ไม่ใช่ตัวอื่น" — ตรวจสดแล้ว คำตอบวัดได้:

1. `current/pf_login_game_server_v141.py:1323` `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` แถว 0 = `(0, 1, -9139.96, -2780.05, 223.29, 'P_MALE_002_000_SP1', 'Navy Transfer')` — คอลัมน์ที่ 2 คือ `template_id = 1`
2. `template_id` มาจาก `gamedata/pf_decode_lua_npc.py:439`: อ่าน u32 ที่ offset +1 ของ payload 16 ไบต์ของ definition `Mob_Set_01` ⇒ ได้ `1` (และ `Mob_Set_NN` ⇒ `NN` ทุกตัว 1..113 เรียงตามลำดับ)
3. ตารางแช่แข็งเอาเลขนั้นไปเปิด `CONSTDATA_TH__MOBS.n_ID = 1` ⇒ 海軍傳送兵 / outfit `P_MALE_002_000_SP1` / TIP "Navy Transfer" · `world_population._entry()` ส่ง `source_name` นี้เป็น `basic_name` (amendment 26 ส.ค.)

⇒ **นี่คือ join-by-equal-number ที่กฎ GT-044 ห้าม** ไม่มีหลักฐานเลยว่า u32 ตัวนั้นคือ `MOBS.n_ID` — มันเรียง 1..113 ตรงกับ ordinal ของ definition พอดี ซึ่งเป็นสิ่งที่คาดจาก "เลขลำดับ" มากกว่า "id ของ NPC ที่เมืองนี้ใช้"

**หลักฐานเสริมว่า join ผิดจริง (จากตาราง MOBS/TIP เอง):** `n_ID 2` Sebastian = *Warden* (ผู้คุมคุก) · `n_ID 5` Pike = *Unemployed Sailor* บทพูด "ข้าทำกุญแจหาย ผู้คุมต้องลงโทษข้าแน่" · `n_ID 4` Mo Yuzi = Naval Communications Bureau — สามตัวนี้คือ NPC ของ **Prison Exile Island (ฉากเริ่มเกม)** แต่ตารางแช่แข็งวางไว้ใน Port Royal เพราะเลข 2/4/5 · และ "Unemployed Sailor" คือตัวที่ Panya เห็นยืนแทน Hields ใน GT-078 พอดี

## เบาะแสที่ใบใหม่ควรไล่ (เรียงตามต้นทุน)

- **T0 — payload 16 ไบต์ของ definition ยังถอดแค่ 4 ไบต์** (`u32@+1`): เหลือ 12 ไบต์ (`+0`, `+5..+15`) ที่ไม่มีใครดู — dump payload ทั้ง 113 definitions ออกมาเทียบกัน ดูว่ามี field ไหนไม่เรียง 1..113 (ถ้ามี นั่นคือผู้สมัคร `MOBS.n_ID` ตัวจริง) · positive control: definition ใดมีค่า `159` หรือ `796`
- **T1 — จับคู่พิกัด**: แปลง XYZ ของ 149 placements เป็น HUD (transform เดียวกับที่ GT-078 ใช้แล้วตำแหน่งถูก) หา record ที่ใกล้ HUD `X 11,510 Y 6,951` ของภาพ REF ที่สุด แล้วดู definition/payload ของ record นั้น
- **T2 — ค้นสองที่**: `MOBS.n_ID_MAP` (คอลัมน์ 5) และตาราง `STANDARD_MOB` / `NPC_VOICE` / quest ว่ามีคอลัมน์ผูก scene 1 ↔ n_ID ไหม (Panya บอกไว้ว่าเมืองจริงมี "NPC มาตรฐานประจำเมือง" — `CONSTDATA_TH__STANDARD_MOB.tsv` ชื่อตรงเกินไปที่จะไม่เปิดดู)
- ถ้า T0–T2 ล้มทั้งหมด ⇒ ใบ attended ตามข้อ ① ของจดหมาย 0310

ไม่แตะโค้ด ไม่เปิดเกม — ใบนี้เป็นเบาะแสให้คนเปิดใบ ไม่ใช่ผล RE

— เซสชัน attended กะ1
