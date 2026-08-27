[ถึง: **สาย A (WORLD)** — งานรอบ 05:21 · cc สาย B · chief · COO · RE runner · Panya | จาก: Panya (เจ้าของ) ผ่านเซสชัน attended กะ1 — คำสั่ง 04:5x (+07:00) | เขียน 05:00 (+07:00) | ภาคผนวก 3 ของ 0310 ข้อ ① · แทนที่ "ทางเดียวที่เหลือ = attended" ใน 0415]

# PANYA-RULE + ANCHOR — **ห้าม brute-force วาง NPC ทีละตัวให้เจ้าของดู** · หาความเชื่อมโยงจากไฟล์เกมก่อน · จุดยึดแรก: **placement index 1 (`Mob_Set_02`, XYZ −8013.5 / −2780.0 / 223.3) = Columbus – Marine Transport Station**

บล็อกนี้ลงชื่อ "จาก Panya" (prompt chief §14 ข้อ 9)

## ① คำสั่งเจ้าของ (คำต่อคำ 04:5x)

> "ฉันสามารถช่วยยืนยัน npc ที่ถูกต้องได้แค่บางตัว ไม่ใช่ทุกตัว เพราะฉะนั้นหาความเชื่อมโยงที่เป็นไปได้จากไฟล์เกมก่อนดีกว่า อย่าเพิ่ง bruteforce วางตำแหน่งเช็คทีละตัว ฉันจำได้ไม่หมดหรอก รู้แค่ว่า ตำแหน่งของ n_ID 2 Sebastian ในตอนนี้ มันต้องเป็น Columbus - Marine Transport Station"

⇒ **ยกเลิก**ข้อเสนอ "ใบ attended ยิงทีละตัวให้ Panya ดู" ใน 0310/0415 · ใบ attended จะมีได้ก็ต่อเมื่อมีตารางเสนอที่มาจากไฟล์ก่อน แล้วให้ Panya ยืนยันเฉพาะตัวที่เธอจำได้

## ② หลักฐานใหม่จากเจ้าของ — ภาพเซิร์ฟเวอร์เดิม #2 (ท่าเรือ Port Royal)

`evidence_screens/REF_ORIGINAL_SERVER_PortRoyal_harbor_Columbus_Lisa_Loie_20260827.jpg` (ย่อจาก PNG 3 MB → JPG 378 KB ให้ผ่าน guard · ต้นฉบับอยู่กับ Panya) — client 1.41 เดิม, เห็นในภาพ:
- NPC **"Marine Transport Station / Columbus"** ยืนหน้าเรือใหญ่ริมท่า (ป้ายสองบรรทัด title ฟ้าเหนือชื่อเหลือง)
- NPC **"Navy Engineer / Loie"** มุมซ้ายล่าง (`MOBS.n_ID 802` "Royal Navy Engineer")
- target bar บนสุด = **"Lisa"** (`n_ID 177` Navy Transport Officer) — ผู้เล่นเลือกเป้าอยู่ ⇒ Lisa อยู่ใกล้ท่าเรือเช่นกัน
- minimap "Port Royal" อ่านพิกัดได้ประมาณ **X 7,7xx · Y 2,5xx** (เบลอ) ขณะผู้เล่นยืนห่าง Columbus ไม่กี่เมตร
- **สัญญาณ:** ถ้า HUD = −XYZ ของไฟล์ฉาก (sign flip) จุด (−7722,−2546) ห่างจาก placement index 1 เพียง 374 หน่วย และห่าง index 0 (`Mob_Set_01`, −9140/−2780) 1,437 หน่วย — สอดคล้องกับคำเจ้าของว่า index 1 = Columbus · **แต่** จุดลาน REF #1 (HUD 11,510/6,951) flip แล้วไม่มี placement ใกล้เลย (ใกล้สุด 4,800) ⇒ transform HUD↔XYZ **ยังไม่นิ่ง** สาย A ที่รู้ transform ของ GT-078 ต้องเป็นคนตัดสิน (อย่าเชื่อ sign flip ของผม)

## ③ ความเชื่อมโยงจริงในไฟล์เกมที่เพิ่งพบ (ตรวจสด 04:4x–05:00 · ทั้งหมด grep ได้จาก `gamedata/tables/`)

**(ก) `CONSTDATA_TH__MOBS.s_QUEST_BEGIN` / `s_QUEST_END` → `QUESTDATA_TH__QUEST.n_ID` → `QUEST.n_SCENE`** — นี่คือ crosswalk field จริงตัวแรกที่ผูก NPC เข้ากับฉาก
- NPC ที่มีเควสเริ่ม/จบในฉาก 1 (Port Royal) = **119 ตัว** (รายชื่อเต็มให้สาย A รันซ้ำเอง 20 บรรทัด python) · ตัวอย่างที่เกณฑ์ M1 ต้องการ: `159 Hields` ✓ · `796 Sase` ✓ (9 เควส) · `177 Lisa` ✓ · `801 Adam` / `802 Loie` ✓ · `164 Nayar Skill Trainer` (13) · `165 Tim Dungeon Keeper` · `163 Mackie Royal Exchange Manager` · `162 Joshua Appraisers` · `161 Locher Finance` · `160 Frank Port Royal Congressman` · `166 Grace Beer Promoter` · `167 Jensen Shipyard Engineer` · `168–170 Nelson/Bismarck/Yamamoto Admirals` · `171 Drunkard Captain` · `172 Mo Yuzi` · `183 Columbus "Dream Voyager"` (เควส, ไม่ใช่สถานีขนส่ง) · `638 Port Royal Bulletin Board` (66 เควส)
- **Columbus สถานีขนส่งของ Port Royal = `n_ID 156`** (เควส 3 ใบในฉาก 1 · lv 10) — **ไม่ใช่ 196** ที่ผมเดาจากลำดับบล็อกเมื่อ 04:2x · Columbus ตัวอื่น (36/67/105/196/835) เควสอยู่ฉาก 0/3/126 = ของเกาะอื่น
- `2 Sebastian` → เควสฉาก 2 (4 ใบ) · `5 Pike` → ฉาก 2 (3 ใบ) · `1 Navy Transfer` → ฉาก 0 ⇒ ตัวที่ตารางแช่แข็งวางในเมืองตอนนี้ **มี field ยืนยันแล้วว่าเป็นของ Prison Exile** (ก่อนหน้านี้ผมอนุมานจากบทพูดแล้วถอนไป — ตอนนี้กลับมาได้ด้วยหลักฐานจริง)

**(ข) โครงบล็อกของตาราง MOBS** (วัดจากชื่อ/title เรียงตาม n_ID): แต่ละเกาะเป็นบล็อกต่อกัน และบล็อกเริ่มด้วยคู่ `Port transportation` + `Columbus Marine Transport Station`: `36/37` → Spice Paradise (38 Reyna Spice Merchant…) · `66/67` → Slave Market (70 slave buyers…) · `104/105` → Evil Port (106 Old Tom Pirate Dad…) · **`155/156` → Port Royal (157 Love Millie Antique Store … 183)** · `195/196` → เกาะถัดไป · บล็อก `1..35` = Prison Exile (2 Sebastian Warden, 11 Mystery Prisoner, 15 Old Prisoner, มอนสเตอร์ 27–35) — **ยังเป็นการอ่านรูปแบบ ไม่ใช่ field** แต่สอดคล้องกับ (ก) ทุกจุดที่ตรวจ

**(ค) `CONSTDATA_TH__SCENE_AREA` (ไอคอนบน minimap ของฉาก 1 · 26 แถว · พิกัดพิกเซล n_MAP_X/n_MAP_Y):** `Icon_Map_Sail (151,213)` · `Icon_Map_Shop (214,206) (248,161) (232,208)` · `Icon_Map_Warehouse (221,267)` · `Icon_Map_Auction (273,224)` · `Icon_Map_Skilllearn (267,165)` · `Icon_Map_Instance (267,184)` · `Icon_Map_Army (290,173)` · `Icon_Map_Wine (314,109)` · Chest ×5 · CollectMap ×5 · ไม่มีไอคอน ×6 — **นี่คือ "หน้าที่ ↔ ตำแหน่ง" ของเมือง**: Sail = Columbus · Skilllearn = Nayar 164 · Instance = Tim 165 · Auction = Mackie 163? · Warehouse = ? · Army = Navy HQ (168–170/174) · Wine = Grace 166 / Drunkard Captain 171 · Shop = Melody 903 Grocer / Keleita 934 / Vera 918 …
⇒ ถ้า fit พิกเซล→XYZ ได้ (ใช้ Sail↔index 1 Columbus เป็นจุดยึดแรก + Auction/Skilllearn/Army ที่ NPC มีตัวเดียว) จะได้ placement ของ NPC บทบาทเหล่านี้ **จากไฟล์ล้วน**

**(ง) `CONSTDATA_TH__MARKER` (391 แถว · `n_SCENE, n_X, n_Y, n_Z, n_DIRECTION` · ฉาก 1 มี 29 จุด · พิกัดเป็น u32 ที่ค่าลบ wrap เช่น 4294956974 = −10322)** — เป็นพิกัดโลกในระบบเดียวกับ HUD/ไฟล์ฉาก (Z 930/931 ตรงกับ "Port Royal ground Z=931" ที่ v141 ใช้) · marker `n_ID 1` ฉาก 1 = (−10322, −726, 671) · ใครอ้าง marker (quest? teleport? spawn point?) ยังไม่รู้ — **ใช้เป็นชุดพิกัดสอบเทียบ transform ได้ทันที**

**(จ) ตัดออก (ตรวจแล้วไม่ใช่):** `MOBS.n_ID_MAP` มีค่า 0–5 เท่านั้น (ไม่ใช่ marker/scene) · `QUESTTALK.n_NPC_*` ค่า 1–22 (ไม่ใช่ MOBS id) · `MAP_SCENE_LIST` 15 แถว = ปุ่มแผนที่โลก · `STANDARD_MOB` = stat ตามเลเวล · `bg0001.gsa.scene.settings` = viewport ของ editor · `bg0001.tgr` = trigger (RE-057 ทำไปแล้ว)

## ④ งานที่สั่งสาย A รอบนี้ (ลำดับบังคับ — ไม่ต้องรอ COO)

1. **สร้าง Port Royal roster จาก (ก)** — NPC ทุกตัวที่มีเควสในฉาก 1 + บล็อก 156–183 + ส่วนเพิ่มทีหลัง (356–359, 796–802, 833–834, 871, 902–934 ฯลฯ) · ติดคอลัมน์: n_ID, ชื่อ, title, outfit, lv, จำนวนเควสฉาก 1, n_MOB_APPEAR, s_ROLE_GRAPHIC · **เทียบจำนวนกับ 116 placements ที่ version2_byte=1** และ 149 ทั้งหมด — ถ้า roster ~60–120 ตัว นั่นคือคำตอบว่า "เมืองมี NPC มากเกินจริง" เพราะอะไร
2. **fit transform** พิกเซล minimap (ค) ↔ XYZ ไฟล์ฉาก ↔ HUD: จุดยึด = `Icon_Map_Sail (151,213)` ↔ index 1 (−8013.5, −2780.0) [คำเจ้าของ] + MARKER 29 จุด + REF #1 (ลาน, HUD 11,510/6,951) + REF #2 (ท่า, HUD ~7,7xx/2,5xx) · ให้ระบุ residual ทุกจุดยึด
3. **เสนอตาราง "placement index → n_ID" เฉพาะตัวที่ไฟล์ชี้ได้** (ไอคอนบทบาทที่มี NPC ตัวเดียว: Sail/Skilllearn/Instance/Auction/Army/Wine + Hields/Sase จาก REF #1 + Lisa/Loie ใกล้ Columbus จาก REF #2) · ทุกแถวมีคอลัมน์ "หลักฐาน" และ "ความมั่นใจ" · **ส่วนที่ไฟล์ไม่ชี้ ให้เว้นว่าง อย่าเดา**
4. ส่ง Panya **รายการสั้น ≤ 10 ตัวที่ต้องการให้เธอยืนยัน** (ตัวที่คนเล่นเกมจำได้แน่ ๆ: Columbus, Lisa, Hields, Sase, Nayar, Tim, Mackie, admirals) — เธอบอกแล้วว่ายืนยันได้แค่บางตัว
5. เพิ่มข้อ (ก)–(ง) เข้า `00_SEARCH_HERE_FIRST.md` หมวด "ตารางที่มีค่าที่สุด" (เขตของสาย A/chief ตามกติกา) เพื่อไม่ให้ใครเปิดใบหาอีก

สาย B: ข้อ (ก) ใช้กับสนามได้เหมือนกัน — NPC/มอนสเตอร์ที่เควสชี้ฉาก 2/3/15 = roster ของเกาะนั้น เอาไปประกบชุด 1..N vs 101+ ของ Bg0002/Bg0015 ได้

— Panya (ผ่านเซสชัน attended กะ1) · ไม่แตะโค้ด · ไฟล์ใหม่ที่วาง = ภาพ REF #2 ใน evidence_screens/ เท่านั้น
