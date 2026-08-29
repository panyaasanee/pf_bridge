[ถึง: chief (ผู้เปิดใบ) · LANE-B · COO · cc Panya | จาก: RE runner local · 2026-08-29T19:12+07:00]

# RE-150 RESULT — DONE / BOUNDED-NEGATIVE · ไม่มีมอน aggro นอกบล็อกที่เจ้าของปฏิเสธใน bg0001/Bg0002

- ใบ: `RE-150 AGGRO-PLACEMENT-OUTSIDE-REFUSED-BLOCKS-001 [STATIC-ON-BRIDGE]`
- START: `2026-08-29T19:01:30.632+07:00`
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, source, queue หรือ git
- verdict: **bounded-negative ของ committed corpus + identity/hostility predicate ปัจจุบัน** — placement ที่เป็นมอน (`n_RANK>0` และ `n_AI_COMBAT>0`) และเริ่มหาเป้าเอง (`n_OFFESIVE=1`, `n_AGGRO>0`) มีเพียง Bg0002 placement 92–96, Mob-Set/n_ID 103, `AI_WANDER=11`; ทั้งห้าอยู่ในชุด 101–104 ที่เจ้าของปฏิเสธทั้งหมด จึงไม่มีตัวเลือกนอกบล็อกสำหรับ M6

## T0 — input pins และช่องค้นบังคับ

- shared input manifest ก่อนเริ่ม:
  - `external/`: 30 ไฟล์ / 29,900,221 ไบต์ / manifest `adde783103731a02d03fe937cc4c203689011ae88f684f64c8fd910fff41e51a`
  - `gamedata/`: 1,109 ไฟล์ / 15,319,585 ไบต์ / manifest `a99978af7990524948808d33f82f8543bffed949d6efdd1b31381e292da5c227`
- **ค้นใน `pf_bridge\external\` แล้ว: ไม่เจอ.** ค้นครบทั้ง 30 ไฟล์ด้วย `ai_wander|aggro|aggressive|OWNER_REFUSED_PLACEMENTS|Mob-Set 101-104`; ไม่มี placement/AI crosswalk — tree นี้เป็น protocol/client-binary handoff ไม่ใช่ scene/table corpus
- **ค้น `gamedata` แล้ว: เจอคำตอบในตาราง/placement; ไม่เจอทางเลือกใน Lua.**
  - `PF_GAMEDATA_INDEX.tsv:26` และ `PF_GAMEDATA_COLUMNS.tsv:323-327,392` พิน `AI_WANDER.(n_ID,n_OFFESIVE,n_AGGRO)` และ `MOBS.n_AI_WANDER`
  - อ่าน `CONSTDATA_TH__AI_WANDER.tsv`, `MOBS.tsv`, `CLINE.tsv`, `SCENE_NAME.tsv`, placement ของทั้งสองฉาก และ Lua 616/616 ไฟล์; Lua ไม่มี `AI_WANDER|n_OFFESIVE|n_AGGRO|OWNER_REFUSED_PLACEMENTS`
- SHA หลัก: `AI_WANDER` `0b3f1eb8...01a23`; `MOBS` `3c0d33d6...3916b`; `CLINE` `aa4a55b8...dc40`; `SCENE_NAME` `e38114a8...5d60b`; bg0001 placements `2e5b4115...4cfc5f`; Bg0002 placements `e57841a7...92f8f`

## T1 — ความหมาย aggro ผ่าน G1 สองชั้น

1. ชั้นตาราง: `AI_WANDER.tsv:12` แถว 11 ให้ `n_OFFESIVE=1`, `n_AGGRO=1200`; `MOBS.tsv` ผูกผ่าน named field `n_AI_WANDER` จึงไม่ใช่การจับคู่เพราะเลขเท่ากัน
2. ชั้นอิสระ: `FACTPACK_R102_HOSTILE13_ROSTER.md:13,24-30,53` พาร์สตาราง 024 สดจาก client offset `0x329A46` แล้วได้การแบ่งเดียวกัน (`AI_WANDER 11 -> 6/1/1200`); `tools/pf_mine_mob_ai_rows.py:22-31` บันทึกว่าการพาร์สคนละทิศทาง corroborate กัน
3. artifact ที่ commit แล้ว `field_mob_ai_tables.py:11-14,38-43` ระบุ `n_OFFESIVE` = acquire เป้าที่ไม่เคยตีมัน และ `n_AGGRO` = รัศมี; SHA `928b3130...ab675d`

ข้อสรุปนี้ใช้เงื่อนไขทิศเดียวที่ข้อมูลรองรับ: `OFFESIVE=1` พร้อมรัศมีบวก. ไม่อ่าน `n_AGGRO>0` ตัวเดียวเป็น offensive เพราะมีแถว non-offensive ที่ยังมีรัศมีอยู่จริง

## T2 — join placement → identity → MOBS → AI

ใช้ rule ที่ artifact ปัจจุบันประกาศเองและ source digest ตรงกับ gamedata ทุกตัว:

- bg0001: `cline` — `SCENE_NAME.n_CLINE_TYPE=1` + `(type,Mob-Set)` เข้า `CLINE`, ใช้ `n_LEADER_BK1` เป็น production identity; สแกนเพิ่มครบทั้ง 9 ช่อง leader/crew ตาม consumer ของ RE-128 เพื่อกัน candidate ซ่อนใน crew
- Bg0002: `setnum` — Mob-Set เป็น `MOBS.n_ID` ตาม artifact ปัจจุบัน
- monster predicate ที่ artifact ประกาศ: `n_RANK>0` และ `n_AI_COMBAT>0`

ผลที่เป็นมอนและ offensive มีเพียงห้าแถว:

| ฉาก | placement | placement file:line | Mob-Set | n_ID | MOBS:line | AI_WANDER | AI:line | off/aggro | rank/combat |
|---|---:|---|---:|---:|---|---:|---|---|---|
| Bg0002 | 92 | `Bg0002.placements.tsv:94` | 103 | 103 | `MOBS.tsv:102` | 11 | `AI_WANDER.tsv:12` | 1 / 1200 | 1 / 332 |
| Bg0002 | 93 | `Bg0002.placements.tsv:95` | 103 | 103 | `MOBS.tsv:102` | 11 | `AI_WANDER.tsv:12` | 1 / 1200 | 1 / 332 |
| Bg0002 | 94 | `Bg0002.placements.tsv:96` | 103 | 103 | `MOBS.tsv:102` | 11 | `AI_WANDER.tsv:12` | 1 / 1200 | 1 / 332 |
| Bg0002 | 95 | `Bg0002.placements.tsv:97` | 103 | 103 | `MOBS.tsv:102` | 11 | `AI_WANDER.tsv:12` | 1 / 1200 | 1 / 332 |
| Bg0002 | 96 | `Bg0002.placements.tsv:98` | 103 | 103 | `MOBS.tsv:102` | 11 | `AI_WANDER.tsv:12` | 1 / 1200 | 1 / 332 |

บล็อก 101–104 ในไฟล์ฉาก derive เป็น placement `{89,90,92,93,94,95,96,97}` ครบแปดตัว; จึงกิน candidate ทั้งห้าพอดี และ candidate นอกชุดนี้ = 0

## T3 — ค่า offensive อื่นที่พบ แต่ห้ามยกเป็นมอน

พบ 13 placement นอกบล็อกที่แถว AI เป็น offensive แต่ไม่ผ่าน monster predicate:

- bg0001 placement `103/105/107/109`: n_ID 916 Training Iron Man, `AI_WANDER=21`, off/aggro `1/3000`, แต่ rank 0 และ combat AI 0
- bg0001 placement `2/96/131/133-138`: n_ID `157/918/634`, `AI_WANDER=33`, off/aggro `1/700`, มี combat AI แต่ rank 0 — artifact ปัจจุบันจัดเป็น NPC/rank-zero ไม่ใช่มอน

ผล all-slot scan ของ `CLINE` ทั้ง leader+crew ในสองฉากไม่พบ actor ที่ครบ `offensive + rank>0 + combat>0` เพิ่มอีก. จึงห้ามหยิบ rank-zero NPC หรือเป้าซ้อมมาเติม M6 เพียงเพราะค่า AI ดูดุ

## T4 — verifier / checkpoint

- `staged/re150_aggro_placement_static.py` SHA `77e0af7a29794977ab96c2634ef50ae8597393c701ccda28da8c4c46e4e3d55f`: **PASS 32/32 สองรอบ**
- artifact `staged/re150_aggro_candidates.tsv` SHA `21956d9d924dfafdc8c73e9a97c3ba1d81b3a5cc2560d96895c7d5f6ab23d156`: 18 แถว (5 refused monsters + 13 non-monster offensive rows) พร้อม file line/SHA provenance
- checkpoint: `T0 DONE · T1 DONE/G1 · T2 DONE/BOUNDED-NEGATIVE · T3 DONE/NONCLAIM · T4 PASS`
- method ceiling: ห้ามรัน RE-150 ซ้ำกับ corpus/rule/owner-refusal เดิม; เปิดใหม่ได้เมื่อมี placement/data pack ใหม่, identity/monster predicate เปลี่ยนอย่างมีหลักฐาน หรือเจ้าของเคาะบล็อก 101–104 ใหม่

## nonclaims

1. ไม่ claim ว่า rank-zero NPC/Training Iron Man จะไม่ acquire target ใน client; บอกเพียงว่าไม่ใช่ **มอน M6** ตาม predicate ที่ commit อยู่
2. ไม่ claim ว่า AI_WANDER เป็นพฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ; เป็นข้อมูลที่ ship มากับ client + การอ่านที่โปรเจกต์/COO รับไว้
3. ไม่ claim client-observable ว่า Orc Chief ทั้งห้าเริ่มตีจริง; ใบนี้ตั้งใจไม่มีชั้นตา และยังต้องเปิดใบ “ยืนใกล้แล้วโดนตีไหม” หลังมีตัวที่อนุญาตให้วาง
4. ไม่ claim ว่าฉาก/locale/data pack อื่นไม่มี candidate; ขอบเขตคือ bg0001/Bg0002 ใน committed corpus ที่ตรึง SHA ด้านบน
5. สูตร/monster predicate/การเลือกว่าจะส่ง actor ใดเป็นดีไซน์ของโปรเจกต์ ไม่ใช่ข้อเท็จจริงของ original server

## BUILD_IMPACT

**BUILD_IMPACT:** M6 ยังเพิ่ม “มอนที่เริ่มตีเอง” จาก bg0001/Bg0002 corpus ปัจจุบันไม่ได้โดยไม่ขัดคำสั่งเจ้าของ. ทางเปิดที่มี provenance คือ (ก) ขอเจ้าของทบทวน Bg0002 placement 92–96 / Mob-Set 103 พร้อมหลักฐานนี้ หรือ (ข) เพิ่มฉาก/data source ใหม่; ห้าม promote rank-zero NPC/เป้าซ้อมเป็นมอนแทน

`BUILD_IMPACT_NONE: 0/1`

สถานะที่ควรกรอก: `RE-150 DONE/BOUNDED-NEGATIVE — NO ELIGIBLE AGGRO MONSTER OUTSIDE OWNER-REFUSED BLOCK`.
