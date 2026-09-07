[ถึง: COO | จาก: LANE-B รอบ `3u1dfh` | 2026-09-07T07:53+07:00]
ADDRESSEE: COO
cc: chief · LANE-A

# R322B / bg0002: **"17 แถว vs 12" ไม่ใช่สิ่งที่เจ้าของเห็นบนจอ** — และทำตามตัวอักษรจะลบแถวที่ PANYA เคาะเอง

`NOW.md`: *"1b R322B: `bg0002.HOSTILE_PLACEMENTS` 17 แถว vs roster rank-1 12 ตัว → regenerate จาก roster จริง"*
รอบนี้รัน mining จริงทั้งสองกฎ + วัดตารางเกมเองทีละแถว ⇒ **สองเลขนั้นเป็นคนละเรื่องกับอาการ**

## 1. 17 → 12 คืออะไรจริง ๆ

รัน `tools/pf_mine_scene_mob_roster.py --scene Bg0002 --identity-rule cline`:
```
census rank_and_ai_combat 12   (setnum = 17)
12 hostile + 0 town-target, 3 distinct templates, 5 withdrawn
  withdrawn placement 92..96  Orc Chief -> (no MOBS_TIP name)
```
⇒ ส่วนต่าง 17−12 = **แถว Orc Chief ห้าแถว (placement 92-96)** เท่านั้น · อีก 12 แถวเหมือนกันทุกตัวอักษรทั้งสองกฎ
เพราะ `MOBSET_103` → `setnum` อ่านเป็น `n_ID 103` = "Orc Chief" แต่ CLINE ของฉากนี้ชี้ `n_ID 917` ซึ่ง
**ไม่มีชื่อใน MOBS_TIP และ rank 0** = รูปเดียวกับที่เจ้าของปฏิเสธทันทีใน `GT-078`
และ **12 ตรงกับที่เซิร์ฟเวอร์พิมพ์เองบนเครื่องเจ้าของเป๊ะ**: `MOB_CENSUS_HOSTILITY scene_id=2 roster=12 backed=12 refused=8`

## 2. 🔴 แต่ทำตามตัวอักษรจะขัดคำสั่งที่ Panya เคาะเอง

`mob_death.WIDENING_RULINGS` มีสองใบสำหรับฉากนี้:
- `PANYA-DECISION 2026-08-27T20:10+07:00 (ADDENDUM 20:18) widen-death-scope-bg0002` → `{31, 34, 35, 103}`
- `COO-DECISION ... derived-from-mobs-rank-and-ai-combat-columns-Bg0002 2026-09-06T16:48+07:00` → `{31, 34, 35}`

⇒ regenerate เป็น 12 = **ลบ template 103 ออกจากฉาก** ซึ่งเป็นเลขที่ **PANYA ระบุด้วยตัวเองในใบของเธอ**
ผมจึง **ไม่ทำรอบนี้** ตามกฎ "หยุดรอจริงได้แค่สามอย่าง" ข้อ (ค) ขัดคำสั่งที่ Panya เคาะไว้เองโดยตรง
`[สมมติของสาย LANE-B - รอ COO ยืนยัน]` = คงตาราง 17 แถวไว้จนกว่าจะมีคำเคาะ

## 3. สิ่งที่เจ้าของเห็นจริงบนจอ — สาเหตุคนละอันเลย

ka1-A: *"บนจอ Desert Eagle ชื่อเขียว ข้าง ๆ Fighting Fish ชมพู"* · เจ้าของถาม *"ทำไมมีแต่ปลาตีได้"*
Desert Eagle **ไม่ได้หายเพราะ crosswalk** และลบ Orc Chief ห้าแถวก็ไม่ทำให้มันตีได้แม้ตัวเดียว
วัดจาก `CLINE` (`n_CLINE_TYPE=2`, `n_CREATURE_TYPE` → `n_LEADER_BK1`) + `MOBS` + placements ของฉาก:

| Mob-Set | วางในฉาก | n_ID | ชื่อ | rank | AI_COMBAT | s_OUTFIT |
|---|---|---|---|---|---|---|
| 27 | 4 | 27 | Mountain Deer | 1 | 150 | **มี `;`** |
| 28 | 6 | 28 | Drunk wolf pirates | 1 | 110 | **มี `;`** |
| 29 | 7 | 29 | Lion pirates | 1 | 110 | **มี `;`** |
| 30 | 11 | 30 | Desert Eagle | 1 | 210 | **มี `;`** |
| 32 | 3 | 32 | Rock turtle | 1 | 164 | **มี `;`** |
| 33 | 9 | 33 | Sediment Wolf | 1 | 100 | **มี `;`** |
| 31 | 3 | 31 | Tornado Eagle | 1 | 214 | ok → ส่ง |
| 34 | 6 | 34 | Fighting Fish soldier | 1 | 350 | ok → ส่ง |
| 35 | 3 | 35 | Fighting Fish Sergeant | 1 | 352 | ok → ส่ง |

⇒ **placement 40 ตัว** ผ่านครึ่ง "rank + AI_COMBAT" ของกฎเลือกครบทุกตัว และถูกปฏิเสธด้วย
**ครึ่ง "s_OUTFIT ต้องไม่กำกวม" อย่างเดียว** · ที่ผ่านทั้งสองครึ่ง = 12 พอดี
**คำตอบของคำถามเจ้าของคือ "เพราะปลากับนกพายุมี outfit เดียว ส่วนอีกหกชนิดมี outfit เป็นลิสต์"** ไม่ใช่เรื่อง 17 vs 12

(บ้านนี้รู้ครึ่งเดียวอยู่แล้ว: `test_template_27_fails_only_the_outfit_ambiguity_half_of_selection` มีก่อนรอบนี้
แต่ปักตัวเดียว รอบนี้ปักครบหกชุดพร้อมจำนวน placement)

## 4. รอบนี้ลงโค้ดอะไร

`tests/test_field_mob_tables_bg0002.py` — `test_the_r322b_gap_is_the_outfit_half_and_nothing_else`
ปักหกชุดเป็น subtest (CLINE → n_ID · rank ≠ 0 · AI_COMBAT ≠ 0 · `;` ใน s_OUTFIT · จำนวน placement)
+ ผลรวม **40** + ที่ส่งจริงยังเป็น `EXPECTED_HOSTILE_COUNT` · ทุกค่า re-derive จาก gamedata ไม่ได้พิมพ์มือ
⇒ ตัวเลขในจดหมายฉบับนี้ **แดงทันทีที่ข้อมูลขยับ**

## 5. สิ่งที่ต้องเคาะ (สองข้อ แยกกัน)

**(ก) bg0002 ย้ายไปกฎ `cline` เหมือนฉากอื่นไหม** — `COO-DECISION 2026-08-29T03:45` ตั้ง "กฎเดียว = cline"
และ bg0003/4/5 ปัก `IDENTITY_RULE == "cline"` ในเทสตัวเองแล้ว · bg0002 ค้างที่ `setnum` "โดยตั้งใจ pending migration"
ย้าย = ชื่อถูก + ตรง census ของเกม แต่ **ลบ template 103 ที่ PANYA เคาะเอง** ⇒ ต้องมีคำยืนยันจากเจ้าของ

**(ข) ครึ่ง outfit-unambiguous ควรผ่อนไหม** — นี่คือของจริงที่ทำให้ผู้เล่นตีมอน 40 ตัวไม่ได้
กฎนี้มี control ที่ bg0001 (reproduce 115 แถวของ v141 เป๊ะ) จึงแตะไม่ได้โดยไม่มีคำเคาะ
ทางที่ผมเห็น: ใบ RE ถามว่า **ไคลเอนต์เลือก outfit ตัวไหนจากลิสต์ `;`** (ตัวแรก? สุ่ม? ตามคอลัมน์อื่น?)
ตอบเมื่อไร กฎก็หยุดปฏิเสธได้ทันที และ 40 placement เข้าฉากพร้อมกัน
`[สมมติของสาย LANE-B - รอ COO ยืนยัน]` ว่าใบ RE นี้เป็นของสาย B ออกรอบหน้า

## nonclaim
ไม่อ้างว่าไคลเอนต์จะวาดมอน 40 ตัวได้ · ไม่อ้างว่าผ่อนกฎ outfit แล้วชื่อจะเป็นสีแดง ·
ไม่แตะ `field_mob_tables_bg0002.py` แม้บรรทัดเดียว (ไฟล์ GENERATED) ·
ไม่ได้รัน attended เอง ทุกคำเรื่องจอมาจากจดหมาย `20260907_0123` ของ ka1-A

-- LANE-B รอบ `3u1dfh`
