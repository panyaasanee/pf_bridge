[ถึง: chief / COO / สาย A · cc Panya | จาก: RE runner LOCAL | 2026-08-27T03:10+07:00]

# RE-095 RESULT — PASS/DONE: Columbus marine-transport crosswalk ใช้ quest 3023; descriptor byte 0 เป็นค่า default ที่ปลอดภัยสำหรับ type 20

## คำตอบสั้น

crosswalk จริงในข้อมูลไคลเอนต์ชี้ว่า **Columbus แถว `MOBS.n_ID=36` ใช้ quest `3023`** สำหรับทางไปทะเล ไม่ใช่ `3020` หรือ `3301..3303`:

`MOBS 36 (Columbus / Marine Transport Station)` → `s_QUEST_BEGIN` และ `s_QUEST_END` มี `3023` → `QUEST 3023` เป็น `n_TYPE=20`, `s_LUASCRIPT=Q_TELEPORT1`, `n_VARI_2=19` → `QUESTTALK 3023.s_ROLE_TALK=COLUMBUS_0` → ข้อความเควสต์ชื่อ “Atlantic Ocean: Rising Sun Sea”. `SCENE_NAME 19` เป็น `Bg1003`, `n_SCENE_TYPE=4`, ชื่อ `Ship in the Sea` จึงสอดคล้องกับขั้น “ย้ายไปแมพทะเลแล้วเป็นเรือ”.

ค่าที่ใส่ใน nested descriptor ได้จาก static คือ:

- `u16 +0x10 = 3023`
- `u8 +0x12 = 0` เป็น **constructor default ที่ปลอดภัย**: factory `0x00622130` zero ทั้ง `+0x10/+0x12` ในสอง allocation paths และ router `0x0061CA50` อ่าน `QUEST.n_TYPE`; เมื่อ type เป็น `20` จะกระโดดจาก `0x0061CB5E` ไป common path `0x0061CBC7` โดยข้าม selector-byte read ที่ `0x0061CB6F` ทั้งหมด

🔴 ค่า byte `0` นี้เป็นคำตอบระดับ client-compatible/default; **ไม่ได้สังเกต byte จริงจากเซิร์ฟเวอร์ต้นฉบับ** และไม่ได้ตั้งชื่อ semantic ให้ `+0x12`.

## T0/T1 — crosswalk ที่ใช้จริง

`QUESTDATA_TH__QUEST.tsv` ไม่มีคอลัมน์ giver NPC โดยตรง แต่ตาราง `MOBS` มี crosswalk ชื่อฟิลด์ตรง ๆ คือ `s_QUEST_BEGIN`/`s_QUEST_END`; `PF_GAMEDATA_INDEX.tsv` ยังประกาศ `MOBS -> MOBS_TIP` ทำให้ระบุตัว NPC ได้โดยไม่ join จากเลขบังเอิญ:

- `MOBS 36`: `s_QUEST_BEGIN=121;3023;3207`, `s_QUEST_END=121;919;3023;3207`
- `MOBS_TIP 36`: `s_NAME=Columbus`, `s_TITLE=Marine Transport Station`
- `QUEST 3023`: `n_TYPE=20`, `Q_TELEPORT1`, `n_VARI_2=19`
- `QUESTTALK 3023`: `s_ROLE_TALK=1;COLUMBUS_0...`
- `TEXT_QUEST 3023`: ชื่อเควสต์ไป `Atlantic Ocean: Rising Sun Sea`
- `SCENE_NAME 19`: `Bg1003`, type `4`; `SCENE_NAME_TIP 19`: `Ship in the Sea`

ตัวควบคุมที่หักล้าง candidate เดิม:

- `3020` ผูกกับ `MOBS 1`, ชื่อ `Navy Transfer`, ไม่ใช่ Columbus; ข้อความคือ “เดินทางไป Port Royal”
- `3301..3303` ไม่อยู่ใน `MOBS 36.s_QUEST_BEGIN/END`, ไม่มี `COLUMBUS_*` ใน `QUESTTALK`, และข้อความเป็น Poseidon warp gate ไป scene 1/2/3
- ดังนั้น candidate `{3020,3301,3302,3303}` ทั้งหมดไม่ใช่ Columbus marine-transport crosswalk ที่ข้อมูลชุดนี้ชี้

## Wire / image verification

- `NPCConversation` registry: serializer `0x00622F10`, nested serializer `0x00606890`; external fields ยืนยัน `u16 +0x10` และ `u8 +0x12`
- span `[0x00622F10,0x00623083)` SHA `3678aab6...e50c3b40`
- nested serializer `[0x00606890,0x006068E3)` SHA `7f43e91b...0f1e8bb4`
- descriptor factory `[0x00622130,0x0062221A)` SHA `b5ba1e25...1023e739`
- quest router `[0x0061CA50,0x0061CD38)` SHA `bc2c22d7...99225cc4`

## ค้นสองที่ (บังคับ)

- **ค้นใน `pf_bridge\external\` แล้ว:** เจอ registry/serializer/validation ของ `NPCConversation` และ `QuestOperateVital`, รวม field `+0x10/+0x12`; ไม่เจอ Columbus/3023→NPC crosswalk ในชุด external เพราะตารางนี้เป็นชั้นโค้ด/wire ไม่ใช่ข้อมูล quest/NPC
- **ค้น gamedata แล้ว:** เจอ crosswalk ครบใน `MOBS 36.s_QUEST_BEGIN/END`, `MOBS_TIP 36`, `QUEST/QUESTTALK/TEXT_QUEST 3023`, และ scene 19 ตามรายละเอียดด้านบน

## Verifier / integrity

- verifier ใหม่ read-only: `pf_bridge\staged\re095_columbus_quest_crosswalk.py`, SHA256 `a9203ec5cb877de6182fe0f5f219c0bd163ab2bd3f39f1cc8965920142a4aa12`
- รันหลังแก้ verifier สุดท้ายสองรอบ: `SUMMARY guards=45 failed=0`, exit `0` ทั้งสองรอบ
- `GameClient.local.bin` ก่อน/หลัง `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- external ก่อน/หลัง: registry `27daac0c...16cfb4d`, fields `99282bdf...b5c123`, validation `080a5f32...e0941c3`
- gamedata ก่อน/หลัง: index `a9ab5efd...110b5bc`, MOBS `3c0d33d6...1b3916b`, MOBS_TIP `e25ac667...53ce38f`, QUEST `cc992728...7527bd`, QUESTTALK `e6f8cb7a...f421e`, TEXT_QUEST `e1929030...bb427`, SCENE_NAME `e38114a8...5d60b`, SCENE_NAME_TIP `f9076cfc...1bfa3a`
- server source `current/pf_login_game_server_v141.py` ก่อน/หลัง `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`; ไม่ได้แก้ source
- ระหว่างรัน queue ถูก sync โดย chief ที่ `03:04:03+07:00` (ปิดหัว `RE-085`); reread แล้ว `RE-095/096` ไม่เปลี่ยนและ `RE-095` ยังไม่มีผลเดิมก่อนเขียนฉบับนี้

## BUILD_IMPACT

สาย A มี data-backed descriptor สำหรับ Columbus lane แล้ว: ใช้ **Columbus actor context + qid 3023 + byte 0** แทน singleton `P0/0x2001 + qid 3020` เพื่อสร้าง probe/implementation ของขั้น Port Royal→sea โดยไม่ clone ความหมายผิดจาก Navy Transfer/Poseidon gate. ยังต้องแก้ actor placement identity และพิสูจน์ runtime sequence แยกก่อนประกาศ M2 ผ่าน.

## Nonclaims

- ยังไม่พิสูจน์ว่า Columbus ใน `bg0001` placement block คือ template/actor identity ใด; `RE-093` ปิดเพียงสมมติฐาน block ที่สอง ไม่ได้ให้ identity crosswalk
- ยังไม่พิสูจน์ byte `+0x12` จริงของเซิร์ฟเวอร์ต้นฉบับ; พิสูจน์เพียงว่า zero คือ constructor default และ type-20 path ไม่อ่าน selector นี้
- ยังไม่พิสูจน์ว่า q3023 เพียงตัวเดียวทำให้เกิด scene transition, vehicle binding, dock trigger หรือ captain-report UI ครบสาย
- `n_VARI_2=19` + scene 19 เป็นหลักฐานสอดคล้องกับขั้น sea-map แต่ไม่ถูกใช้ยืนยัน whole runtime sequence; ต้อง wire/attended แยก
- ไม่ได้ใช้ linear disassembler เป็นหลักฐานของผลลบ และไม่แก้ source/queue/DB ใด
