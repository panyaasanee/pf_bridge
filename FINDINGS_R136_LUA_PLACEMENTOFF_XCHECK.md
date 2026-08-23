# FINDINGS R136 — cross-check `Scene.PlacementOFF` กับ `.npc` placement index: **สมมติฐานสะพานตรง ๆ ถูกหักล้าง**

**ผู้เขียน:** chief (cloud R136 · session zkhuuy) · **วันที่:** 2026-08-24 (+07:00)
**ขุดโดย:** ลูกมือ `pf-static-re` จาก artifact ที่ commit แล้วล้วน (`gamedata/` @ commit `0801541`) — ไม่มี binary ไม่มี capture
**ชั้นหลักฐาน:** [STATIC · extracted game-data] ทั้งไฟล์ — ไม่มีอะไรในนี้เป็น wire/DB หรือ client-observable

---

## คำถามที่ตั้ง

จดหมาย `notes_to_chief/20260824_0124_*` ชี้ว่า `Scene.PlacementOFF` 173 จุดใช้ "เลข index ตรง ๆ"
และเสนอว่าใบเชื่อมเลน Lua ↔ เลน placement (GT-053: Bg0002 = 106 placement · band `0x2000+idx+1`) น่าจะคุ้มที่สุด
⇒ ก่อนเปิดใบ ต้องตอบก่อนว่า **เลขใน PlacementOFF(n) คือ placement index ของ `.npc` จริงไหม**

## คำตอบ: ไม่ใช่ (ในรูปแบบที่ ship มากับ build นี้) — และรูปประโยคตั้งต้นก็คลาดด้วย

### ① สัดส่วนรูปอาร์กิวเมนต์จริง — แก้คำในจดหมาย 0124

| รูป | จำนวน | ที่อยู่ |
|---|---:|---|
| literal number | **112** | 4 ไฟล์เท่านั้น: `t_clsplc_t1_for_bg3001.lua:3-28` (26 จุด) · `..._bg3002.lua:3-40` (38) · `..._bg3003.lua:3-19` (17) · `..._bg3004.lua:3-33` (31) |
| `Trigger.VarN` (N=1..16) | **61** | 15 ไฟล์ · ไม่มีรูปอื่นเลย |

รวม 173 ตรง census (`PF_GAMEDATA_LUA_API.tsv:12`) ✓ — แต่ประโยค "173 จุดเป็นเลขตรง" **ผิด 61/173**
literal ทั้งหมดอยู่ในช่วง 13..61 (49 ค่า ไม่มีรู)

### ② การ map ไฟล์ lua → ฉาก มีหลักฐานแค่ 4 ไฟล์

- `PF_GAMEDATA_LUA_INDEX.tsv` **ไม่มีคอลัมน์ scene** (header: `rel_path src_path src_sha256 src_bytes out_bytes lines status`)
- หลักฐานเดียว: ชื่อไฟล์ `_for_bg300N` (index rows 373-376) + คอมเมนต์ `--# Var1 = BG3001...` ใน `t_clsplc_t1_for_bg3001.lua:1`
- อีก 15 ไฟล์ (สาย `Trigger.VarN`): **ไม่มี binding ฉากใน clone นี้เลย** — trigger→scene กับค่าของ VarN
  อยู่ใน trigger data ของฉาก/อิมเมจ client ⇒ **ต้องใช้เครื่องสะพาน** [UNKNOWN]

### ③ 🔴 counterexample — literal เกินช่วง placement index ของฉากตัวเอง

(row count re-derive จาก `gamedata/scene/*/*.placements.tsv` ตรง `placement_count` ใน `PF_GAMEDATA_SCENE_INDEX.tsv:262-265` · คอลัมน์ `index` เป็น 0-based ต่อเนื่องทุกไฟล์ที่ตรวจ)

| ฉาก | placements (idx) | def_count | literals ในสคริปต์ | คำตัดสิน |
|---|---|---:|---|---|
| Bg3001 | 38 (0..37) | 56 | 26-28, 34-56 | 🔴 **19 จุด (38..56) เกิน 0-based · 18 จุดเกิน 1-based** |
| Bg3002 | 39 (0..38) | 58 | 24..61 | 🔴 **23 จุดเกิน 0-based · 22 จุดเกิน 1-based · 59-61 เกินแม้แต่ def_count** |
| Bg3003 | 42 (0..41) | 36 | 13-20, 25-33 | พอดีทั้งสองแบบ |
| Bg3004 | 46 (0..45) | 46 | 15..45 | พอดี · max 45 = count-1 เป๊ะ (เอียงอ่อน ๆ ไปทาง 0-based) |

**ไม่มี convention ไหนทำให้ literal ทุกตัว valid: 42/112 หลุดช่วงแบบ 0-based · 40/112 แบบ 1-based**
ทางเลือกที่ลองแล้ว (กับข้อมูล Bg3002 · แก้ตาม adversary R136 — ระบุคอลัมน์ให้ถูก):
- `u16_6` เซตคือ {1-9,12-40,62} — **ไม่มี 59/60/61**
- `template_ids` เซตคือ {1-2,11-31,33,55-58} — **ทับ literal ที่ 55-58** (ไม่ตัดออกด้วยเหตุ "ไม่มีในช่วง") แต่ **ไม่มี 59/60/61**
- definition index แบบ 1-based เพดาน 58 แต่ literal ถึง 61
**ไม่มีคอลัมน์ไหนใน artifact ที่ commit แล้วอธิบายค่า 59/60/61 ได้** (จุดตัดสินคือ 59/60/61 ที่ไม่มีที่มา ไม่ใช่การอ้างว่าทั้งช่วงว่าง)

ที่เป็นไปได้แต่ยังไม่พิสูจน์: สคริปต์เขียนกับ revision ฉากที่เก่ากว่า/ใหญ่กว่า หรือกับ namespace placement อีกชุด
(trigger/event placements) ที่ตัวถอด `.npc` ไม่ครอบ ⇒ **ชี้ขาดต้องใช้เครื่องสะพาน (อิมเมจ/runtime)**

### ④ Bg0002 (ฉากของ GT-053) — เทียบข้ามไม่ได้เลย

ไม่มีไฟล์ lua ไหนอ้าง Bg0002 (grep ทั้ง `gamedata/lua/` = 0) · re-derive อิสระ: `Bg0002.placements.tsv`
106 แถว idx 0..105 ตรง `PF_GAMEDATA_SCENE_INDEX.tsv:9` และตรงเลข GT-053 ✓ — แต่ **ฝั่ง Lua ไม่มีอะไรให้เชื่อม**

### ⑤ ครอบครัว API placement (จาก `PF_GAMEDATA_LUA_API.tsv`)

`PlacementOFF` 173/19 (บรรทัด 12) · `PlacementON` 96/46 `var` (21) · `CheckPlacementAlive` 65/36 `var` (26) ·
`PlacementCancel` 32/15 `var` (46) · `CheckPlacementCombat` 1/1 (159) — **PlacementOFF เป็นตัวเดียวในครอบครัวที่
arg เด่นเป็น literal** ที่เหลือขับด้วยตัวแปรทั้งหมด

## ผลต่อแผน

1. 🔴 **อย่าเปิดใบ "เชื่อม PlacementOFF เข้า band GT-053" บนสมมติฐาน idx ตรง ๆ** — ถูกหักล้างแล้วด้วย 42/112
2. คำถามเปิดที่เหลือ (บันทึกไว้ ไม่เปิดใบรอบนี้ — ต้องรอเครื่องสะพาน): literal ของ PlacementOFF ชี้ namespace ไหน
   (ตัวเทียบที่ดีคือ Bg3002: ค่า 59/60/61 ที่ไม่มีอะไรรองรับ) — ถ้าจะเปิดใบภายหลัง จ็อบแรกต้องเป็นการหา
   namespace นั้นในอิมเมจ ไม่ใช่การ assume index
3. schema ของ `placements.tsv` (24 คอลัมน์ รวม xyz/template_ids/set_names) พร้อมใช้อ้างในใบอนาคต — ตัวอย่างใน sec ⑤ ของรายงานลูกมือ

## nonclaims

- ไม่ได้พิสูจน์ว่า runtime ตีความ arg ของ PlacementOFF อย่างไร — counterexample บอกแค่ว่า "ไม่ใช่ .npc index ตามที่ ship"
- 🔴 **caveat ของ counterexample เอง (adversary R136):** "42/112 หลุดช่วง" นับกับ denominator = จำนวนแถวที่ตัวถอด `.npc`
  ตัวเดียวมองเห็น · findings นี้ยอมรับเองว่า trigger/event placements อาจอยู่ใน namespace ที่ตัวถอดไม่ครอบ (sec ③)
  ⇒ ถ้า namespace จริงใหญ่กว่านั้น "หลุดช่วง" อาจกลายเป็น "อยู่ในช่วงของ denominator ที่ครบกว่า" — **ข้อสรุปจึงเป็น
  "ไม่ใช่ index ของ .npc ที่เราถอดได้" ไม่ใช่ "ไม่ใช่ index ของ placement เลย"** · ชี้ขาดต้องเครื่องสะพาน
- ไม่แตะ wire/DB/หน้าจอ · ไม่ได้ re-verify band `0x2000+idx+1` ของ GT-053 (ใช้แค่เลข 106 เป็น input)
- ไม่รู้ว่า 15 ไฟล์สาย `Trigger.VarN` ผูกฉากไหน และ VarN รับค่าอะไร
- ชื่อไฟล์ `_for_bg300N` คือเจตนาของ dev ไม่ใช่ binding ที่พิสูจน์แล้ว
