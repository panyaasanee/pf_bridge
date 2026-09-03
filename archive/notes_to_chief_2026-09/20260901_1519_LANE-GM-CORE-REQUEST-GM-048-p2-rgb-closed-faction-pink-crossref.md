[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: สาย GM รอบ `r2jfjm` · 2026-09-01T15:19+07:00]

# CORE-REQUEST-GM-048 -- P-2 RGB ปิดแล้ว แต่พบเส้นทางสีที่สองที่เคยเรนเดอร์ "ชมพู" จริง ต้องแยกให้ชัดก่อนสายไหนเขียนโค้ด

## ที่มา

`notes_to_chief/20260901_1439_CODEX-RE191-RESULT-FONTSTYLE63-RGBA.md` (ถึง chief, LANE-GM จาก
Codex static RE, ยังไม่มีคนบริโภค) ตอบข้อเดียวที่ค้างของ P-2 ตาม `COO-DECISION 20260901_1241`:
RGBA จริงของ `fontstyle_id` 61/62/63 ผ่าน DATA+IMAGE cross-reference (`PF_MONSTER_COLOR_GATE.tsv`,
sha256 ระบุในใบ):

| FontStyleID | FontColor RGBA | คำบรรยาย |
|---:|---|---|
| 61 | (255,100,100,255) | แดง/แดงอมชมพู |
| 62 | (255,159,113,255) | ส้ม/แซลมอน |
| 63 | (179,179,179,255) | เทา |

ตรงกับเกณฑ์เจ้าของ (ปกติ=ส้ม, สู้=แดง, ตาย=เทา) และ**ไม่มีตัวไหนเป็นชมพู** -- ปิดคำถาม RGB ที่ COO
สั่งไว้ได้จริง สายนี้บริโภคใบแล้วรอบนี้ (สตับ + สำเนาไป `consumed/`)

## แต่ใบนี้เองเขียนเพดานไว้ชัด (ไม่ใช่การอ่านเกินของสายนี้)

> "นี่ไม่แปลว่า style63 = death ในทุกบริบท และไม่พิสูจน์ว่า live actor ผ่าน gate นั้น ... อย่า
> hardcode สีหรือส่ง style ID ตรง ๆ; client เลือกจาก identity/relationship/death path"

ตาราง `PF_ATTR_NAME_COLOR_SELECTOR.tsv` (มีอยู่แล้วใน `notes_to_chief/reference_codex_attr/`,
ไม่ใช่ของใหม่รอบนี้) ยืนยันคำนี้: selector เป็นโค้ด**ฝั่งไคลเอนต์**ล้วน (function VA เดียว
`0x00443F50`, path entry หลายจุด) ที่อ่าน identity/relationship ของ actor สองตัว -- ไม่มีฟิลด์ wire
ชื่อ FontStyleID ที่เซิร์ฟเวอร์ส่งตรง ๆ เท่าที่ค้นในทั้งสอง repo (`grep -rn FontStyle` = 0 ผลนอก
เอกสารนี้เอง)

## สิ่งที่พบใหม่รอบนี้ (ยังไม่มีรอบ GM ก่อนหน้าไหนอ้างถึง) -- คนละเส้นทางสีที่เคยเรนเดอร์ชมพูจริง

`src/pirateforce_foundation/npc_hostile_hypothesis.py:11-30` (docstring, GT-032 attended PASS,
ไม่ใช่ของสาย GM -- อ่านอย่างเดียว) บันทึกไว้ว่า faction เป็น **BasicAttr bit `0x0400`, u32 ที่
offset `+0x68`** และเมื่อผู้เล่น faction 1 เจอ NPC faction 6 ไคลเอนต์จริงเรนเดอร์ **"pink/red name,
red outline, red target panel"** -- นี่คือกลไกสีคนละตัวกับตาราง FontStyleID ข้างบน (relation/faction
comparator `0x4A1D50` ไม่ใช่ `UILabel_FontStyleID_parser_setter`) แต่ผลลัพธ์ที่เคยวัดได้ **ตรงกับคำว่า
"ชมพู" ที่เจ้าของสั่งห้ามเป๊ะ** (`NOW.md` P-2: "ห้ามชมพู")

## ทำไมเรื่องนี้สำคัญก่อนใครเขียนโค้ด P-2

ถ้าโมดูล/สายไหนก็ตามที่ได้รับมอบให้ทำ P-2 ต่อ (ไม่ว่าจะเป็นสายนี้หรือสายอื่น) ไปแตะ faction field
ของ NPC เพื่อให้ระบบ hostility ทำงาน (เช่นต่อยอดจาก `npc_hostile_hypothesis.py`) โดยไม่รู้ตัวว่า
faction pairing บางคู่เรนเดอร์ชมพู ⇒ เสี่ยงเขียนโค้ดที่ขัด "ห้ามชมพู" ของเจ้าของโดยตรงและไม่มีใคร
ตรวจจับจนกว่าจะเทสจริง สายนี้เห็นแค่ครึ่งเดียว (ตาราง FontStyleID, เขตของสายนี้) ไม่มีสิทธิ์อ่าน/แตะ
`npc_hostile_hypothesis.py` ในรายละเอียด (นอก `gm/`) จึงไม่มีทางยืนยันเองว่า faction pairing ไหน
ปลอดภัย

## ขอจาก chief

1. ยืนยัน/หักล้าง: สองเส้นทางสี (FontStyleID selector vs faction/relation comparator `0x4A1D50`)
   เป็นกลไกเดียวกันหรือคนละกลไกจริงในไคลเอนต์ -- ถ้าเป็นคนละกลไก ต้องตัดสินว่า P-2 "ปกติ/สู้/ตาย"
   ควรผูกกับกลไกไหน (FontStyleID ดูใกล้เคียงกับ requirement มากกว่า เพราะมี 3 ระดับสีตรงกับ 3
   สถานะ ส่วน faction ดูเหมือนออกแบบมาสำหรับ friend/foe ไบนารี ไม่ใช่ 3-state)
2. ถ้าเลือก FontStyleID: ขอยืนยันว่ามี/ไม่มีวิถีที่เซิร์ฟเวอร์ส่ง FontStyleID (หรือฟิลด์ที่ไคลเอนต์แปล
   เป็น FontStyleID ผ่าน embedded-style branch ที่ใบ RE-191 อ้างถึง) อยู่แล้ววันนี้ -- ถ้าไม่มี นี่คือ
   ช่องว่างข้อมูลที่ต้องส่งให้สาย RE ต่อ ไม่ใช่จุดเสียบโค้ดที่พร้อมให้สายไหนเขียนได้เลย
3. ถ้าเลือก faction/relation: ขอรายชื่อ faction pairing ที่เคยวัดว่าเรนเดอร์ชมพู (ไม่ใช่แค่ (1,6))
   ให้เป็น block-list ก่อนสายไหนแตะ NPC faction field ของมอนสเตอร์

## เทสที่พิสูจน์คำตอบ

ไม่มีทางวัดจาก static ต่อ -- ต้องเป็น attended: ยิง identity pair ที่ระบบ hostility ปัจจุบันสร้าง
(ถ้ามี call site จริงแล้ว) แล้วเทียบ FontStyleID ที่ requested/applied กับพิกเซลจริงบนจอ ตามที่ใบ
RE-191 เขียนไว้เอง ("ยังต้องเห็น live registry node, requested/applied ID และ pixels ของ actor ตัว
เดียวกันก่อนปิด")

## nonclaims

1. ไม่อ้างว่า faction comparator กับ FontStyleID selector เป็นกลไกเดียวกัน -- แค่ตั้งข้อสังเกตว่า
   ผลลัพธ์ที่เคยวัด (ชมพู) ตรงกับคำห้ามของเจ้าของ ให้ chief ตัดสิน
2. ไม่อ้างว่า RE-191 ปิด P-2 ทั้งใบ -- ปิดเฉพาะคำถาม RGB ที่ COO สั่งไว้ ยังต้องมี live wiring +
   คำตอบข้อ 1-3 ข้างบนก่อนใครเขียนโค้ดสีได้จริง
3. ไม่แตะ `npc_hostile_hypothesis.py`/`runtime.py`/`app.py`/`pf_login_game_server_v141.py`/
   canonical DB/`scenarios/world_*.json`/`scenarios/combat_*.json` -- อยู่นอกเขตเขียนของสายนี้ทั้งหมด
   นี่คือใบขอ ไม่ใช่การแก้
4. ไม่เขียนโค้ดสีมอนสเตอร์ใด ๆ รอบนี้ -- ยังไม่มีจุดเสียบและยังไม่รู้ว่าเป็นกลไกไหน เขียนตอนนี้ =
   การเดา

ค้นแล้ว: ค้น `external/00_SEARCH_HERE_FIRST.md` และ `gamedata/00_SEARCH_HERE_FIRST.md` ด้วยคำ
"faction"/"pink"/"ชมพู"/"fontstyle" แล้ว -- ไม่เจอรายการที่ตรงประเด็นนี้โดยตรง (มีแต่ตารางที่อ้างถึง
ในใบนี้เองซึ่งรู้อยู่แล้ว)

— สาย GM รอบ `r2jfjm`
