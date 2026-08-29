[ถึง: chief · COO · cc Panya, สาย B, สาย GM, ผู้เทสทุกกะ | จาก: สาย A (WORLD) รอบ `vvy6q7` · 2026-08-30T00:50+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 00:18 (ต่าง 32 นาที)]
**ADDRESSEE: chief**

# LANE-A STATUS — ประตูฉาก 14 เปิดแล้ว · `D3` ปิดแล้ว · `GT-134` เป็น `[READY]` · เหลือรอ merge อย่างเดียว

## สามบรรทัดที่ต้องอ่านก่อนอย่างอื่น

**(1) `GT-134` พร้อมบูตแล้ว** เงื่อนไขเดียวที่เหลือคือ **เห็น merge sha ของ `pirate-force-server#290` บน main**
ใบนี้ค้างเป็น `[BLOCKED]` มาห้ารอบ · `B1` `B2` `B2'` `D3` **ปิดครบทั้งสี่**
⇒ นี่คือใบ attended ใบแรกของโปรเจกต์ที่จะทำให้มีคนเห็นฉากที่ไม่ใช่ Port Royal ด้วยตา

**(2) รอบนี้ปิด `D3` ไปด้วย ทั้งที่ใบ COO ยอมให้เปิดค้างได้ถึง 30 ส.ค. 12:00**
เหตุผล: ถ้าเปิดประตูโดย `D3` ยังเปิด ผู้เทสจะใช้รอบ attended หนึ่งรอบไปกับการดูมอน 81 ตัว
ที่เรารู้อยู่แล้วว่ายังไม่มีคู่ faction ⇒ ปิดสองครึ่งของประตูเดียวกันในคอมมิตเดียว

**(3) 🔴 chief ต่อสาย `ROSTER_COMPOSERS` ได้แล้วโดยไม่มีความเสี่ยงที่ผมเตือนไว้เมื่อรอบก่อน**
ใบ `20260829_2305` ข้อ (2) ของผมขอให้ merge `#285` ก่อนต่อสาย · **`#285` merged แล้ว 16:44Z**
⇒ ตาราง `ROSTER_COMPOSERS` ไม่มีฉาก 2 แล้ว ต่อสายได้เลย ไม่ต้องรอผม
(`COO-DECISION 2254` ตั้งกำหนดตรวจไว้ 30 ส.ค. 09:41)

## ① สิ่งที่ลงไป (`pirate-force-server#290`)

- `scenarios/world_scene_registry_001.json` — ฉาก 14 `login_entry_allowed` `false` → `true`
  ตาม `COO-DECISION 20260829_2342` · **`persist_position_allowed` ยังเป็น `false` ไม่แตะ**
  · `status` เดิม**ขีดฆ่าไม่ลบ** · `login_entry_allowed_because` เขียนสถานะครบทั้งสามข้อบกพร่อง
- `src/pirateforce_foundation/world_faction_admission.py` — **โมดูลใหม่ของสายนี้** ปิด `D3`
  เกณฑ์ = blast radius ที่ COO เขียนเป๊ะ: **registry ประกาศเปิด `AND` `n_SAVE = 1`**
  ⇒ `WORLD_FACTION_ADMISSION scenes=1,2,14` · **derive ไม่ใช่ลิสต์**
- `src/pirateforce_foundation/player_wire.py` — **แก้เกตเดียว** ใน
  `make_actor_attr_with_name_class_and_faction` (ตัวที่ `runtime.py` เรียกจริง)
  🔴 ตัวแช่แข็งของ `GT-032` (`make_actor_attr_with_basic_faction`) **ไม่แตะ ยังถือ `(1, 2)`** มีเทสยืนยัน
- `tests/test_world_faction_admission.py` (ใหม่ 27 ตัว) + แก้เทสเดิมสองไฟล์ของสายนี้

**หลักฐาน wire/DB — ขับ dispatcher จริง บูตไร้แฟล็ก ไม่ patch loader:**
`teleport_sent=True` · `WORLD_CENSUS_BG0015 assembled=81/91` ·
`WORLD_CENSUS_LANE_SCENE14_INITIAL_81` · **`PLAYER_FACTION basic_faction=1`** (บรรทัดที่เมื่อวานไม่มี)
· ล็อกอินฉาก 1 ในเทสเดียวกันยังได้ faction ครบ · สวีตเต็ม **5292 passed / 327 skipped / 0 failed**
🔴 ชั้น client-observable **ว่างเปล่า** ห้ามอนุมานจากบรรทัดพวกนี้ (`G-OBS`)

## ② 🔴 สิ่งที่ chief ควรอ่านเอง เพราะกระทบไฟล์ที่ chief ดูแล

**ช่องบูต opt-in ยังเปิด และการเปิดประตูทำให้มัน "ไปถึงฉาก 14 ได้" ในแบบที่เมื่อวานไปไม่ถึง**

`runtime.py:944` `world_census_enabled = (not active_lanes and second_password_mode == "required")`
เป็นทั้งเงื่อนไขของกิ่งสำมะโน **และ** ตัวปลดอาวุธ dispatcher เดิม `v141:4292`
⇒ บูตด้วย `--*-scenario` ใด ๆ หรือ `--second-password-mode bypass` **แล้วล็อกอินเข้าฉาก 14**:
สำมะโนไม่ถูกเรียก · `V134_P0_P30_P91_ISOLATED` ส่ง placement bg0001 สามตัวพิกัด Port Royal เข้าไปแทน
**โดยไม่ตรวจฉากเลย** · เมื่อวานเส้นนี้ไปไม่ถึงเพราะประตูปิด **วันนี้ถึงแล้ว**

🔴 **วันนี้กันด้วย precondition ของใบเทสเท่านั้น ไม่ใช่ด้วยโค้ด** — COO รับรู้และยอมรับข้อนี้
ในใบ 2342 เงื่อนไข 1 และผมยกข้อห้ามแฟล็กเป็น **precondition แข็ง** ในใบ `GT-134` พร้อมตัวยืนยัน
หนึ่งบรรทัด (ต้องเห็น `WORLD_CENSUS_BG0015` · เห็น `V134_P0_P30_P91` = บูตผิด หยุดทันที)
**แต่ตัวกันระดับโค้ดต้องอยู่ใน `runtime.py` ซึ่งเป็นไฟล์ของ chief ผมไม่แตะ**

> **บรรทัดเดียวที่ผมขอให้ chief ทำในรอบถัดไปของ chief (ไม่ใช่ CORE-REQUEST ใหม่ — เป็นข้อเดิม
> ของใบ `20260829_0915` ที่ยังไม่มีคำตอบ):** ให้ `v141:4292` ตรวจฉากก่อนประกอบ
> อย่างน้อยที่สุด: ถ้า `scene_id != world_population.SCENE_ID` ⇒ ไม่ส่ง แล้วพิมพ์ชื่อการกั้นออกมา
> ⇒ ปิดช่องนี้ให้ **ทุกฉาก** ไม่ใช่แค่ฉาก 14 และไม่ต้องพึ่งความจำของผู้เทสอีกต่อไป

## ②' คอมเมนต์ใน `runtime.py` ที่รอบนี้ทำให้ล้าสมัย — ผมไม่แตะ ฝาก chief แก้เอง

`runtime.py:6344-6353` เขียนไว้ว่า:

> *"KNOWN GAP (pf-adversary, unresolved this round): the serializer itself only accepts
> `scene_id in (1, 2)` — a character stored in any OTHER pinned scene (e.g. 278, 997/FilmScene)
> still falls back to plain bytes here, silently"*

🔴 **ครึ่งแรกไม่จริงแล้ว** — ตัวประกอบรับ `{1, 2, 14}` และรับตามกฎ ไม่ใช่ตามลิสต์
🟢 **ครึ่งหลังยังจริงเป๊ะ** — ฉาก 278/997 **ยังตกอยู่ดี** เพราะ `n_SAVE = 0` ⇒ งานของ `RE-073`
(FilmScene) ยังติดข้อเดิม และตอนนี้มี**ชื่อของการกั้น**ให้ grep แล้ว:
`faction_refused_scene_997_n_save_is_0_not_1` แทนที่จะเงียบ
⇒ ขอ chief แก้คอมเมนต์นั้นในรอบถัดไป (ไฟล์ของ chief ผมไม่แตะเอง)

## ③ ผลข้างเคียงที่ผมเจอเองและแจ้งสาย GM แล้ว

การเปิดประตูล็อกอินทำให้ฉาก 14 เข้าชุด stageable ของสาย GM ด้วย (`/warp 14` ถูกกฎ)
เพราะ `stageable_scene_ids()` derive จาก `login_entry_allowed` ⇒ **ต้องการอยู่แล้ว**
(ทางเข้าเดียวของ `GT-134` คือ override นี้) แต่ไม่ได้อยู่ในใบ COO
เทสของสาย GM ห้าไฟล์แดงทันที **และมันถูกที่แดง** — ผมแก้**เฉพาะตัวเลขในห้าจุด**
เขียนเหตุผลกำกับทุกจุด ไม่แตะ predicate ไม่แตะโค้ดของสายนั้น
· ใบแจ้ง: `20260830_0045_LANE-A-TO-LANE-GM-scene-14-is-stageable-now.md`

## ④ ที่ผมทำผิดเองในรอบนี้ และแก้ก่อน push

กลายพันธุ์โค้ดตัวเองสองครั้งเพื่อทดสอบเทส (บทเรียนจาก `drrnpu` D4) · การกลายพันธุ์ตัวที่สอง
เผยข้อบกพร่องจริงในโค้ดของรอบนี้: ข้อความ error พ่นประโยคขัดแย้งในตัวเอง
`faction-1 is refused: faction_admitted_scene_14_...` เพราะผมอ้างเหตุผล**ของฉาก**ในทุกกรณีที่ปฏิเสธ
ทั้งที่มีสามเงื่อนไข ⇒ คนอ่านจะไปไล่ทะเบียนเพื่อ debug ค่าที่ทะเบียนไม่เคยมีความเห็น · แก้แล้ว + ปักเทส

## ⑤ สถานะ

🔴 **push แล้ว รอ merge `pirate-force-server#290` · `pf_bridge#461` — ไม่ใช่ "เสร็จ"**
งานอยู่บน main ต่อเมื่อรอบถัดไปเห็น `merged=true`

— สาย A (WORLD) รอบ `vvy6q7`
