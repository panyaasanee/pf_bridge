[ถึง: LANE-A (ผู้เปิดใบ) · chief · COO · cc Panya | จาก: RE runner local · 2026-09-01T09:49:00.718+07:00]

# RE-188 RESULT — DONE / CONFIRMED-NO-CHANGE · CLINE เป็น map-NPC/GO crosswalk ไม่ใช่ world-actor-at-placement rule

- ใบ: `RE-188 PRISON-EXILE-BULLETIN-BOARD-CROSSWALK-CONTRADICTION-001 [STATIC-ON-BRIDGE]`
- START: `2026-09-01T09:33:14.289+07:00`
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB/source/queue/external/gamedata/git
- verdict: **CLINE ทั้งสี่แถวเป็นข้อมูลจริง แต่ห้าม generalize เป็น identity ของ world actor ที่ placement นั้น**. คง placement 64/67/68/91 เป็น `38/39/40/41`; ไม่แทนด้วย `231/742/743/914`.
- input manifest 15 ไฟล์ SHA-256 `3564daefc8813bed0860d3bbfa5f23d82fc0fdffe5886773cfc4e2bc7f2a8650`.

## Job 1 — ปิด semantic boundary ของ CLINE

raw inputs ตรงกันครบ:

- `Bg0002.placements.tsv` SHA `e57841a7018b46ff50d31972e5ba0846612548288446fe8514d819a99be92f8f`: placement 64/67/68/91 ใช้ local sets 38/39/40/41.
- `SCENE_NAME.tsv` SHA `e38114a802576266ce37b2abcf8ebce3f105d7d5abaf4bc5ca066e7848c5d60b`: BG0002 ใช้ CLINE type 2.
- `CLINE.tsv` SHA `aa4a55b8db882eb965d0b7e186cd7bc7b5a81da8f057fee24586a27c94b2dc40`: `(2,38/39/40/41) -> 231/742/743/914`; ช่อง BK2/BK3/crew ทั้งหมดเป็นศูนย์.

แต่ native proof ของ RE-128 SHA `f6bb419e0838e6d61bb9045ae1df45a91a7f0acff5fabceed6d0edea17649a89` ปักสายนี้ไว้ใน **client map-NPC/GO list consumer**: local definition id + scene CLINE type -> CLINE -> candidate IDs. nonclaim ของผลเดิมระบุชัดว่าไม่พิสูจน์ runtime spawn/visibility/original-server population. RE-115 SHA `7e1ce18a2ef1c400d4d683161361f0b0d50e31adf959968bd2d5539b9d7bec63` ยืนยันเพิ่มว่า list/GO นี้สร้าง client-local จาก `.npc`+tables และแยกจาก world census.

counterexample ที่ปิดข้อสงสัยคือ local set 37: CLINE `(2,37)->230` แต่ RE-123 SHA `35c1df1c06d85e6871428966ec581856ca13acf921c5be7131cc7d206cc8f8cd` ตรวจทุก extracted placement แล้วไม่มี template 230, ไม่มี authoritative XYZ/lifecycle และปัก hard guard ว่า Mirage Reel 230 เป็น server-owned quest/service population ห้ามใส่เป็น static placement. ดังนั้นสมการ `CLINE output == world actor at placement XYZ` ใช้ทั่วไปไม่ได้.

อีก control: set numbers เป็น scene-local namespace ไม่ใช่ global MOBS ids. BG0003 ใช้ local sets 3/4/5/6 (placement SHA `5a03747a6cb3c6766fe335863032008c30f82c67dfdc52c701ec44223056ac46`) และ CLINE type 3 จึง map เป็น MOBS 38/39/40/41. เลขเดียวกันข้าม scene/consumer จึงชน namespace ได้โดยไม่ทำให้ CLINE เสีย.

**Job 1: CLOSED — mixed consumer semantics confirmed.** ความขัดแย้งเกิดจากนำ map/list crosswalk ไปตีความเป็น world-placement identity ไม่ใช่จาก CLINE row corrupt.

## Job 2 — หลักฐานราย placement / candidate

1. placement 64: **คง Reyna 38**. Candidate 231 คือ Navy Bulletin Board จริง แต่ไม่มี quest/XYZ/screenshot/note ที่ผูก 231 กับ placement 64. ผลเป็น bounded-negative เฉพาะแถวนี้.
2. placement 67: **คง Mo Yuzi 39**. ภาพ local และ original-server ที่เต็นท์ Prison Exile (`M1P...mo_yuzi_tent.png` SHA `25391844c701021ff29a564bc25ddbd44873b5228e8cee16383840036d6aee95`; reference SHA `4dcfd4a7498809dfbc6753708e5465c4407836dacd130d063d3fa2618c778419`) แสดง Mo Yuzi/Naval Communications Bureau; RE-123 ผูก anchor นี้กับ index 67 / exact XYZ. Candidate 742 Odyssey มี quest 722 ใน scene 2 แต่ไม่มี crosswalk ไป placement 67; scene 2 มี Odyssey ID 13 ที่ placement 17 อยู่แล้ว.
3. placement 68: **คง Carle 40**. attended result SHA `042462792ee7477ccd22ba45964d53fd3b54b21d598772c2d6b32850dd5c1d1e` ผูก exact XYZ `(17542.941,5782.644,950.594)` กับ wire n_ID 40 และเจ้าของเห็น Carle/Nautilus Leader ณ จุดนั้น. Candidate 743 เป็น Prison Exile quest target จริง แต่ไม่มีหลักฐานว่าแทน Carle ที่ placement 68.
4. placement 91: **คง Martin 41**. Candidate 914 Waite ไม่มี scene-2 quest/XYZ/screenshot/note anchor; MOBS quest 3238 ของ 914 อยู่ scene 1. ผลเป็น bounded-negative เฉพาะแถวนี้.

MOBS SHA `3c0d33d68f832eefda56c845495008338dcef56f4277584b9ca479b7e1b3916b`; MOBS_TIP SHA `e25ac667c9029e07752fbfd5d13b548d2e62ea439936884f30187c0c553ce38f`; QUEST SHA `cc9927286def2bda166c320a2dddd16f5457eb4579ce5207a3d76758707527bd`; TEXT_QUEST SHA `e192903071cfba24f882fd120dd230e512b068b67bb956316ffce871b53bb427`.

**Job 2: CLOSED — ไม่มี candidate ใดมี placement-specific support; 39/40 มี positive client-observable anchors, 38/41 คงเดิมแบบ fail-closed.**

## Job 3 — mandatory search / disposition / BUILD_IMPACT

- **ค้น `pf_bridge\external\` แล้ว:** ทั้ง tree 2,443 files / 758,848,182 bytes; deterministic manifest SHA `7c6647ebf4738b168e168f4d44776dc2409ff78845194061d3a9f4f225af5b21`. ค้น exact names/outfits/IDs และ placement terms แบบ binary-safe. เจอเพียง presentation/metadata artifacts; ไม่มีหลักฐานเลือก runtime identity หรือผูก 231/742/743/914 กับสี่ placement. `PF_MONSTER_PRESENTATION.tsv` เป็น descriptor metadata เท่านั้น; `PF_ATTR_SEMANTIC_REPORT.md` พูดถึง outfit ของ Pike ID5 ไม่ใช่ Waite 914.
- **ค้น `pf_bridge\gamedata\` แล้ว:** ทั้ง tree 1,109 files / 15,319,585 bytes; deterministic manifest SHA `f06b5d02854f10e50222c8326b6e7038d7a49a4ffdff142e9c5f2cceecf4dead`. เจอ placement/SCENE_NAME/CLINE/MOBS/TIP/QUEST/TEXT_QUEST exact rows ตามด้านบน; ไม่พบ named field ที่ผูก candidate ทั้งสี่กับ XYZ ของ placement 64/67/68/91.
- ค้น `evidence_screens` 513 files / 251,342,249 bytes, notes root+consumed+archive+rounds และ `**/reports/**`: เจอ Mo Yuzi anchors และ GT-143 Carle result; report tree ไม่มี relevant hit และไม่มี placement-labelled evidence ของ Reyna/Martin หรือ candidates 231/742/743/914.

**BUILD_IMPACT:** `NONE` ต่อ world-census rows — LANE-A คง `38/39/40/41`. ถ้าต้องเก็บ 231/742/743/914 ให้เก็บเป็น client map/quest catalog candidates คนละชั้น; การเพิ่ม server-owned actor ต้องมี lifecycle/visibility + world XYZ evidence แบบเดียวกับ RE-123. RE-173 ไม่ต้อง revert เพราะ set36->360 มี independent name/outfit/route corroboration ซึ่งสี่แถวนี้ไม่มี.

`BUILD_IMPACT_NONE: 1/1`

**Job 3: CLOSED — ticket DONE / CONFIRMED-NO-CHANGE.**

## nonclaims

1. ไม่อ้างว่า CLINE row 231/742/743/914 ผิด; อ้างเฉพาะว่า consumer ที่พิสูจน์ได้ไม่ให้สิทธิ์เอาไปแทน world actor ณ XYZ.
2. ไม่อ้างว่า 742/743 ไม่เคยเป็น actor ใน scene 2; quest data สนับสนุน scene/catalog membership แต่ไม่ให้ placement/lifecycle join.
3. ไม่อ้างว่า Reyna/Martin ถูกยืนยันด้วยภาพเฉพาะจุด; สองแถวนี้คงเดิมแบบ bounded-negative ตามข้อห้ามของใบ.
4. แยกหลักฐาน wire กับ client-observable: wire ของ replacement server พิสูจน์สิ่งที่ server ส่ง; ภาพ/คำเจ้าของพิสูจน์สิ่งที่ client แสดง. ไม่ใช้ชั้นหนึ่งแทนอีกชั้น.
5. ผลลบจำกัดตาม corpus/scopes ที่ระบุ; ไม่ใช้ linear disassembler/string absence เป็นหลักฐานผลลบ.
6. ไม่มีเกม/server boot, capture ใหม่, `LOCK_GAME`, canonical DB, source/table/queue/external/gamedata/git mutation.
