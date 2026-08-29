[ถึง: chief / COO / สาย A · cc Panya | จาก: RE runner LOCAL | 2026-08-27T04:15+07:00]

# RE-097 RESULT — PASS/DONE (mixed evidence): Columbus อยู่ placement index 0 ตาม client+คำเจ้าของ; raw scene ไม่มี MOBS crosswalk

## คำตอบสั้น

ปิดใบได้สองชั้นโดยไม่ join เลขเอาเอง:

- **static / gamedata:** `bg0001.npc` และ `bg0001.placements.tsv` **ไม่มี field ที่ผูกไป `MOBS.n_ID`, `M055`, model หรือชื่อ NPC**. `template_ids` คือเลข local set ของฉาก ไม่ใช่ MOBS id. ดังนั้น static T0/T2 เป็น bounded negative.
- **client-observable + owner-stated:** Columbus ตรงกับ **placement index `0`**, raw XYZ `(-9139.95703125, -2780.045166015625, 223.29209899902344)`. เหตุผลไม่ใช่เลข `1`: ตาราง frozen ของเรานำ XYZ นี้ไปฉายเป็น P0 `Navy Transfer`; GT-030 วัดจาก HUD `(-8876,-2715)` ว่า P0 อยู่ใกล้สุด `271.9` หน่วยและไม่มีตัวเลือกอื่น; Panya ระบุใน GT-078 และคำตัดสิน 16:00 ว่า Columbus / Marine Transport Station ต้องอยู่แทนตำแหน่ง Navy Transfer ปัจจุบัน.

raw placement index 0 อ้าง definition local ชื่อ `Mob_Set_01`. **ห้ามเปลี่ยนประโยคนี้เป็น “definition/MOBS 1 คือ Columbus”** — semantics ของ local definition ยังไม่พิสูจน์ และ MOBS 1 คือ Navy Transfer.

## T0/T1 — crosswalk ใน raw ไม่มี; join `36→36` ถูกหักล้าง

`MOBS 36` คือ Columbus (`M055`, outfit `M055_000_000_N`, title `Marine Transport Station`) จริง แต่เลข `36` ใน raw มีที่เดียวที่ payload `u32/u16 +1` ของ local definition `Mob_Set_36`. Derived TSV จึงวาง `template_ids=36` ที่ **placement index 35**, XYZ `(12558.9072265625, -5593.716796875, 2210.97265625)` — คนละตำแหน่งกับ P0 ที่เจ้าของระบุให้เป็น Columbus.

payload 16 ไบต์ทั้ง 113 definitions ของ bg0001 วัดครบ:

- `+0 = 0` ทุกแถว
- `u32 +1` เท่ากับเลขท้ายชื่อ local `Mob_Set_NN` ทุกแถว
- `+5 ∈ {0,1,2}`; `+6..+10 = 0`; `u32 +11 = 100`; `+15` เป็นเลขเล็ก `0..12`
- ไม่มี `159` หรือ `796` ในทุก unaligned u16/u32 window

จึงไม่มี field ที่ใช้ผูก `Mob_Set_01`/`Mob_Set_36` ไป MOBS 1/36 อย่างสุจริต. คอลัมน์ `template_ids` ของ decoder เป็นชื่อที่แรงกว่าหลักฐานจริง; provenance ของมันคือ payload `u32@+1` + local set-name lookup เท่านั้น.

## T2/T3 — metadata และ Hields/Sase

- schema 24 คอลัมน์ของ placements มี XYZ, u16 fields, set names และ local set ids; ไม่มี model/MOBS/name/comment crosswalk
- `MOBS 36.n_ID_MAP=0`; `STANDARD_MOB` และ `NPC_VOICE` ไม่มี scene/placement field
- census ครบ `gamedata/scene/**/*.placements.tsv` **289 ไฟล์**: ไม่มี local set id `159` หรือ `796`
- ดังนั้นใบนี้ไม่ assign placement ของ Hields/Sase; ทางนั้นยังต้องใช้ภาพ/attended ตาม addendum 04:15

## Correction ต่อ addendum 04:15 (ข้อสรุปหลักยังถูก)

verify raw หกฉากพบว่าข้อสรุป “เลขเป็น local set ต่อฉาก ไม่ใช่ MOBS id” ถูก แต่ตารางนับใน `20260827_0415_ATTENDED-ADDENDUM2-*` มีตัวเลขตกหล่น:

- Bg0002 = 46 definitions จริง: `1..41, 99, 101..104` (addendum ลืม `99`)
- Bg0003 = **52**, ไม่ใช่ 51: `1..40, 99, 101..111`
- Bg0007 = **57**, ไม่ใช่ 56: `1..45, 99, 101..111`
- Bg1001 = **6 definitions** แต่ 5 unique ids: `[1,2,2,4,5,6]`

ทุก raw sample เดิน exact EOF และข้อแก้นี้ไม่เปลี่ยนคำตอบ RE-097.

## ค้นสองที่ (บังคับ)

- **ค้นใน `pf_bridge\external\` แล้ว:** ไม่เจอ `Columbus`, `M055`, `Mob_Set_36` ใน TSV ทั้ง 8 ชุด; `bg0001` เจอเพียง 2 ancillary rows ของ `Sector_0_0/surfaces.xml` ใน INPUT_INVENTORY/DATA_EVIDENCE ซึ่งไม่ใช่ NPC crosswalk.
- **ค้น gamedata แล้ว:** เจอ `MOBS 36`/`MOBS_TIP 36` ยืนยัน Columbus+M055+title, เจอ raw/scene index/placements และ `STANDARD_MOB`/`NPC_VOICE`; ไม่เจอ field ใดผูก identity นั้นเข้ากับ placement. Census 289 scene TSV ไม่พบ local id 159/796.

## BUILD_IMPACT

สาย A ใช้ **placement index 0 + XYZ ข้างบน** เป็นจุด Columbus ได้โดยอ้าง provenance ว่าเป็น **owner/client policy crosswalk** แล้วประกอบกับผล RE-095 (`MOBS 36`, quest 3023). ห้ามอ้างว่า raw scene decode บอก Columbus และห้ามใช้ `template_ids=36` เพราะมันชี้ placement index 35 ซึ่งขัดกับจุดที่เจ้าของระบุ.

## Verifier / integrity

- verifier ใหม่ read-only: `pf_bridge\staged\re097_columbus_placement_identity.py`, SHA256 `71001a3d861f758014acf0bca2005b5cd1542372ec90178e738aa843ca66893b`
- final run สองรอบ: `SUMMARY guards=106 failed=0`, exit `0` ทั้งสองรอบ
- raw bg0001 SHA ก่อน/หลัง `026bbe32...dc2070`; decoder `6ab38fd5...cccf9e`; derived TSV `2e5b4115...cfc5f`; scene index `c4016cf6...652d`
- MOBS `3c0d33d6...b3916b`; MOBS_TIP `e25ac667...ce38f`; server v141 source `2eb05ed2...a4c22`; ภาพ Navy P0 `64af9e6e...ef4fe`; ทุกไฟล์ก่อน/หลังตรง
- external tree manifest ก่อน/หลัง `3b742370...e811`; gamedata tree manifest ก่อน/หลัง `e8e44669...8e5b`
- queue SHA คงที่ `dc1c3e1e...46b86`; addendum 04:15 โผล่ระหว่างรอบ จึงอ่านและ verify แล้วก่อนเขียนผล

## Nonclaims

- ไม่พิสูจน์ actor identity ของ Columbus บนเซิร์ฟเวอร์ต้นฉบับ; `0x2001/P0` เป็น identity ฝั่ง emulator ปัจจุบันเท่านั้น
- ไม่มีภาพ Columbus จากเซิร์ฟเวอร์ต้นฉบับใน evidence ชุดนี้; mapping “Columbus แทน Navy Transfer” เป็นคำยืนยันของ Panya ไม่ใช่ pixel ในภาพ REF Hields/Sase
- ไม่อ้างว่า `Mob_Set_01` หรือ payload id `1` มี semantic เป็น Columbus/Navy Transfer
- ไม่ assign Hields/Sase และไม่ตัดสินโครงสร้าง `world_population.py`
- ไม่ใช้ linear disassembler และไม่เปิดเกม/server ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB/source/queue/git
