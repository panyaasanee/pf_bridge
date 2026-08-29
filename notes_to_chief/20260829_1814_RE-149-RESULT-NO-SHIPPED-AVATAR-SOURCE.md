[ถึง: LANE-A (ผู้เปิดใบ) · chief · COO · cc Panya | จาก: RE runner local · 2026-08-29T18:14+07:00]

# RE-149 RESULT — DONE / BOUNDED-NEGATIVE · ไม่พบ avatar source ของ 155/819/937/942/9107 ในชุด shipped PC+Lua+NPC

- ใบ: `RE-149 PORT-ROYAL-FIVE-COSTUMELESS-LEADERS-001 [STATIC-ON-BRIDGE]`
- START: `2026-08-29T18:02:08.734+07:00`
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, source, queue หรือ git
- verdict: **bounded-negative ที่ static method ceiling ของ corpus ปัจจุบัน** — ทั้งห้า id มี named crosswalk จริงจาก `CLINE.n_LEADER_BK1` ไปยัง MOBS-id space แต่ไม่มีแถว `MOBS` และไม่พบแหล่ง shipped อื่นที่ให้ world-avatar/model/outfit แก่ id เหล่านั้น

## T0 — input pins และช่องค้นบังคับ

- shared input manifest ก่อนเริ่ม:
  - `external/`: 30 ไฟล์ / 29,900,221 ไบต์ / manifest `3b742370873829347ec7827e610c96e8091b0400fde70ceae9965c6f3664e811`
  - `gamedata/`: 1,109 ไฟล์ / 15,319,585 ไบต์ / manifest `e8e44669b2e7b7b06a8722be9c622ee988ab5c169a4b170ad8956751d9428e5b`
  - raw shipped `*.pc_/*.lu_/*.npc`: 909 ไฟล์ / 2,338,723 ไบต์ / manifest `b9ff3e6f4d98a91d7a34f1a4c2e7ab063bd38ef7e4132954cb285e070eafc904`
- **ค้นใน `pf_bridge\external\` แล้ว: ไม่เจอ.** ค้นครบทั้ง 30 ไฟล์ด้วย `CLINE|MOBS|s_OUTFIT|CHANGE_MODEL|Port transportation|Tuna|Mengsk|Jack`; ไม่มี avatar/crosswalk source. ชุดนี้เป็น protocol/client-binary handoff ไม่ใช่ PC table corpus.
- **ค้น `gamedata\` แล้ว: เจอ identity/name แต่ไม่เจอ avatar ของทั้งห้า.** เจอ `CLINE` outputs + `MOBS_TIP` names; ตรวจครบ 188 tables/2,365 columns, Lua 616 ไฟล์ และ scene `.npc` 289 ไฟล์. ขอบเขตผลลบของ avatar อยู่ที่ raw PC/Lua/NPC ชุดนี้เท่านั้น.
- SHA หลัก: `MOBS` `3c0d33d6...b3916b`; `MOBS_TIP` `e25ac667...53ce38f`; `CLINE` `aa4a55b8...b2dc40`; `CHANGE_MODEL` `f74000f7...c40454`; `bg0001.npc` `026bbe32...c2070`; placements `2e5b4115...4cfc5f`; raw `B_CONSTDATA_TH.pc_` `496b5c7b...c9c3f8`; decoded bytes `496dfb2e...f0d2d`.

## T1 — named crosswalk ยืนยันว่าห้าค่านี้อยู่ใน MOBS-id space

`CONSTDATA_TH__CLINE.tsv` ให้คู่ named fields โดยตรง ไม่ใช่จับคู่เพราะเลขเท่ากัน:

- line 202: `(n_CLINE_TYPE=1,n_CREATURE_TYPE=1) -> n_LEADER_BK1=155`
- line 277: type 1 / creature 76 -> `819`
- line 311: type 1 / creature 110 -> `9107`
- line 313: type 1 / creature 112 -> `937`
- line 314: type 1 / creature 113 -> `942`

ผลเดิม RE-128 SHA `f6bb419e...49a89` ยังตรง และ verifier เดิม SHA `bf1048e...88900` ผ่าน 41/41: client CLINE helper require `MOBS` row ก่อนเพิ่ม output. จึงใช้ `n_ID` ของตารางอื่นที่เลขซ้ำแทนไม่ได้.

## T2 — PC tables: ไม่มี world-avatar row สำรอง

1. เครื่องมี raw PC table เพียง 4 ไฟล์และทั้งหมดเป็น locale `TH`: `B_CONSTDATA_TH`, `B_TEXTDATA_TH`, `B_QUESTDATA_TH`, `B_QUESTTEXT_TH`; **ไม่มี MOBS locale อื่นใน shipped tree**.
2. re-parse จาก raw compressed bytes ในหน่วยความจำสำเร็จทั้งหมดโดยไม่ stop: CONSTDATA 120 tables (trailing 146 bytes), TEXTDATA 65 (78), QUESTDATA 2 (76), QUESTTEXT 1 (76). Decoded SHA/size ตรง `_meta.json` ทุกไฟล์.
3. raw `MOBS` มี 3,210 rows x 54 columns; target `{155,819,937,942,9107}` = 0 rows. `MOBS_TIP` มีครบห้าชื่อที่ lines 156/820/933/938/3051 แต่ linked data row ที่ถือ `s_ID_MODEL_CLASS`, `n_ID_MODEL`, `s_OUTFIT` ไม่มี.
4. enumerated ทุก table ที่มี named column `s_OUTFIT`: `MOBS`, `SAILING_RESULT`, `SHIP`, `GET_SHIPCORPSE`. ทั้งสี่ไม่มี target-id row; และไม่มี secondary field ชื่อ `n_MOBS_ID`/`n_NPC_ID` ที่ชี้ถึง target ใด.
5. `CHANGE_MODEL.tsv:156` มี `n_ID=155` จริง แต่แถวนั้นคือ `s_ID_MODEL_PARTS=FIREARM`, `n_ID_MODEL=1`, `n_ID_MAP=5`, equip slots 8/24; ตารางไม่มี MOBS/NPC crosswalk field. นี่คือ **เลขชนข้าม id-space** ไม่ใช่ avatar ของ Port transportation.
6. same-name candidates ก็ใช้แทนไม่ได้: `Tuna` มี MOBS row ที่ id `8529`, `Jack` มีที่ id `855`; display-name เท่ากันไม่ใช่ crosswalk และ target `819/9107` ยังไม่มี row ของตนเอง.

## T3 — Lua และ `.npc`

- Lua decompressed ครบ 616/616: exact numeric token `155|819|937|942|9107` = 0 hit. API surface ที่ชื่อเกี่ยวกับ model มีเพียง `Trigger.HideModel` และ `Trigger.HideTriggerModel`; ไม่มี call สำหรับ set/change avatar/outfit/model.
- raw `bg0001.npc` parse ถึง EOF เป๊ะ 27,607/27,607 bytes: 113 definitions + 149 placements. P0 ใช้ `Mob_Set_01 -> local template_id 1`; definition payload ทั้ง 113 ไม่มี target ใดในรูป direct little-endian u32. ไฟล์ให้ local definition/placement/XYZ แต่ไม่มี named world-avatar field หรือ MOBS replacement crosswalk.

## T4 — verifier / checkpoint

- verifier ใหม่ `staged/re149_costumeless_leaders_static.py` SHA `c676131179f3dcc2d329e513e162a6e3436216f53b14eeeb4a4fe2079e5b01af`: **PASS 51 checks / failed 0**.
- มัน pin source SHA, manifests, re-decode/re-parse raw PC ทั้งสี่, enumerate outfit providers/named crosswalk fields, scan Lua ทั้ง corpus, parse NPC exact EOF และตรวจ source SHA หลังงาน.
- checkpoint: `T0 DONE · T1 DONE · T2 DONE/BOUNDED-NEGATIVE · T3 DONE/BOUNDED-NEGATIVE · T4 PASS`.
- **method ceiling:** ห้ามรัน RE-149 ซ้ำกับ PC/Lua/NPC corpus/objective เดิม. เปิดใหม่ได้เมื่อมี locale/data pack ใหม่, named MOBS-id→avatar crosswalk ใหม่ หรือ chief แก้ objective/jobs อย่างมีสาระ.

## nonclaims

1. ไม่ claim ว่าไฟล์ client จาก build/locale อื่นไม่มีห้าตัวนี้; วัดเฉพาะ shipped tree ที่ตรึง SHA ข้างบน.
2. ไม่ claim ว่า opaque bytes อื่นใน `.npc` มี semantic อะไร; พิสูจน์ได้เพียงไม่มี direct target u32/named avatar field และ path ที่ pin แล้วใช้ local template id เข้า CLINE.
3. ไม่ยก outfit ของ `Tuna 8529`, `Jack 855`, หรือเลข `CHANGE_MODEL 155` มาแทน target เพราะไม่มี named crosswalk.
4. ไม่ claim client-observable ว่า actor ทั้งห้า “วาดไม่ได้” จากการมองจอ; ใบนี้ตั้งใจไม่เปิด visual test. ข้อสรุปคือไม่มี buildable avatar source ใน static corpus ปัจจุบัน.
5. ไม่ claim ข้อเท็จจริงของ original server; `108` เป็นเพดานของ census ที่ **ข้อมูล client ชุดนี้รองรับอย่างมี provenance**.

## BUILD_IMPACT

**BUILD_IMPACT:** BUILD-001 ใช้ **108/115 เป็นเพดานที่ปลอดภัยของ shipped client data ชุดนี้** ได้; ห้ามสร้าง/แต่งตัวห้า absent-MOBS leaders ด้วยเลขชนหรือชื่อซ้ำ. ถ้า M2 ยังต้องการ `Port transportation 155` ให้เปิดงานหา data pack/source ใหม่หรือกำหนด actor ใหม่ด้วยคำตัดสินเจ้าของ — ผลนี้ไม่ให้วัตถุดิบสำหรับ wire มันเอง.

`BUILD_IMPACT_NONE: 0/1`

สถานะที่ควรกรอก: `RE-149 DONE/BOUNDED-NEGATIVE — NO SHIPPED AVATAR SOURCE FOR FIVE CLINE LEADERS`.
