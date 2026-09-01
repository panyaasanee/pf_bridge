[LANE-A (WORLD) round `7ste68` -- 2026-09-02T01:55+07:00]

# census ปกติส่ง level แล้ว 12 ฉาก: บิต BasicAttr 0x0002 ที่ไม่เคยถูกส่งเลยตั้งแต่ต้นโปรเจกต์

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

วาปเข้าฉากไหนก็ตามใน 12 ฉากที่ต่อสายแล้ว ป้ายเหนือหัว NPC จะขึ้น **เลเวลจริงของตัวนั้น**
(ฉาก 6 = 71-105 · ฉาก 14 = 1-115 · ฉาก 130 = 10/150) แทน `LV 1` เหมือนกันหมดทุกตัวอย่างที่
`GT-192` เห็นเมื่อวาน · ไม่ต้องเปิดแฟล็ก ติดทุกบูต

## 1. NOW.md (อ่านก่อนทุกอย่าง)

หัวข้อ "งานด่วนตอนนี้" มี P-1/P-2/P-3 และคิว GM-A/UI-A/GM-B/UI-B/census-latch
**รอบนี้ขยับ GM-A** (`/warp <เลขแมพ>` ต้องเจอ NPC ปกติทุกแมพ) — ไม่ใช่ตัว warp เอง แต่เป็นอาการที่
`GT-192` บันทึกไว้บนจอเดียวกัน: NPC ขึ้นครบแต่ **ทุกตัวเป็น `LV 1`** ซึ่งเป็นข้อที่ Codex ชี้ว่าเป็น
ของฝั่งเซิร์ฟเวอร์ล้วน ๆ และ chief มอบให้สายนี้ในใบ `20260901_2358`
ไม่แตะ P-1/P-2/P-3 (คนละเขต และ P-2 สีถูก Codex ระบุ `NOT_READY_FOR_POLICY_CHANGE`)

## 2. Section A (addendum v2) — ชะตา PR รอบก่อน

- `pf_bridge#771` (`[LANE-A] round n8v2qk`) — `merged_at 2026-09-01T16:35:15Z` ⇒ อยู่บน main
- `pirate-force-server#515` (`[LANE-A] ground-check API + HYP-PF-042`) — `merged_at
  2026-09-01T16:08:00Z` ⇒ อยู่บน main
- ไม่มีงานรอบก่อนหายจาก main ⇒ ไม่ต้อง cherry-pick · branch รอบนี้ตั้งจาก `origin/main` สด ๆ ทั้งสอง repo

## 3. Section B — mailbox (บริโภคครบสามใบ)

ตรวจสองแพทเทิร์นตาม `CHIEF-DECISION 20260901_2357` (`<ชื่อเต็ม.md>.CONSUMED.txt` และ
`<ชื่อตัด .md>.CONSUMED.txt`) พบใบที่ `ADDRESSEE: LANE-A` ยังไม่บริโภคสามใบ บริโภคครบในรอบนี้:

1. `20260901_2321_CHIEF-REPLY-core-request-2007-wired-gt194-ready.md` — CORE-REQUEST 2007 ต่อสายแล้ว
   (option ก) `GT-194` เป็น READY · ไม่มีงานโค้ดค้างฝั่งนี้ รอ attended
2. `20260901_2357_CHIEF-DECISION-consumed-stub-naming-check-both-patterns.md` — ตอบใบ ASK-COO ของ
   สายนี้เอง เลือกทางที่ 2 · รอบนี้ทำตามแล้วทั้งการเช็คและการเขียน stub ใหม่
3. `20260901_2358_CHIEF-TO-LANE-A-codex-gt192-lv1-census-level-encode-assigned.md` — **งานหลักของรอบนี้**

## 4. งานหลัก: ทำไม `LV 1` ไม่ใช่ "ไคลเอนต์ถอดได้ครึ่งเดียว"

`current/pf_login_game_server_v141.py:1139-1195` (frozen, เขตของ chief, **ไม่แตะ**) รับ
name/HP/speed/scene/seq แต่ **ไม่มีพารามิเตอร์ level** และ BasicAttr mask ที่มันเขียนคือ
`0x0004|0x0008|0x0100|0x0200` บวก optional `0x0001` (name) / `0x0040` (speed) — **ไม่มีบิต
`0x0002` เลย** ⇒ ไคลเอนต์วาด default ของตัวเอง · HP ถูกเข้ารหัสจริงจึงแสดงถูกบนจอเดียวกัน
นี่คือเหตุที่อาการ "ดูเหมือน" partial decode แต่ไม่ใช่ (Codex urgent `20260901_2340`)

### สิ่งที่สร้าง

`src/pirateforce_foundation/world_census_level.py` (Foundation-owned additive, ไม่แตะ v141 /
`runtime.py` / `app.py`):

- `with_level(legacy, baseline, *, actor_identity, basic_name, level)` — splice บิต `0x0002`
  และ `u16tag(0x12, level)` เข้าบอดี้แช่แข็ง ตำแหน่ง **คำนวณจากบอดี้เอง** (mask offset จาก head
  ที่ประกอบใหม่จาก `legacy` เอง, level อยู่หลัง optional name ก่อน HP ตามลำดับบิต) ไม่ได้เขียน
  offset คงที่ไว้ · หลัง splice **ถอดกลับ**เป็นบอดี้เดิมแล้วเทียบ ไม่เท่ากันเป๊ะ = refuse
- `leveled_npc_attr(...)` — keyword-only wrapper ที่ composer เรียกแทน `legacy.make_npc_attr`
  (keyword-only จงใจ: พารามิเตอร์แรกของ helper แช่แข็งคือ template u16 ที่ต้องเป็น `MOBS.n_ID`
  จริง ไม่ใช่ Mob-Set number — ความผิดพลาดเดิมของ `GT-078`)
- `read_level(legacy, body, actor_identity)` — อ่านค่ากลับ **ออกจากไบต์** คืน `None` ถ้าไม่มีบิต
  (นี่คือชั้น wire ของกติกาหลักฐานสองชั้น: เทสอ่านจาก `generation.pc` ไม่ใช่จาก roster)

ที่มาของฟิลด์: `RE-117` (NPCAttr serializer `0x00466EB0` เรียก BasicAttr `0x004656F0` เสมอ ⇒
บิต `0x0002`, object `+0x5E`, u16 tag `0x12`, W `0x00465736..0x0046574A`) — แพทเทิร์นเดียวกับที่
hostile encoder ของ lane B ส่งมาตั้งแต่ RE นั้นลง ไม่ได้อนุมานใหม่

### ที่ต่อสาย (12 ฉาก)

`world_population_bg0002` (ฉาก 2) · `bg0003` · `bg0004` · `bg0005` · `bg0006` · `bg0007` ·
`bg0008` · `bg0009` · `bg0010` · `bg0011` · `bg0015` (ฉาก 14) · `bg4001` (ฉาก 130)
ค่าที่ส่ง = `MOBS.n_LEVEL_MIN` ที่ mine ไว้แล้วในโมดูล identity ของฉากนั้นเอง ไม่ใช่ค่าที่คิดขึ้น
ช่วงจริงรายฉาก: 2 (มี range ต่อแถว, ส่ง min) · 3 = 10..105 · 4 = 46..105 · 5 = 61..105 ·
6 = 71..105 · 7 = 81..105 · 8 = 87..105 · 9 = 93/98 · 10 = 99..104 · 11 = 99..105 ·
14 = 1..115 · 130 = 10/150

### 🔴 ขยายขอบเขตจาก 3 เป็น 12 ฉาก — ประกาศไว้ ไม่ได้ทำเงียบ

ใบสั่งระบุสามไฟล์ (`bg0006`/`bg0009`/`bg0015`) เพราะ Codex ตรวจสามไฟล์นั้น · วัดแล้วว่า composer
อีกเก้าตัวเป็นสำเนาโครงเดียวกัน (call shape เหมือนกันทุกตัวอักษร 11 ตัว, `bg0002` ต่างแค่ชื่อค่าคงที่)
และทุกตัวมีคอลัมน์ level อยู่แล้ว · เกณฑ์ GM-A ของเจ้าของคือ "ทุกแมพ" ⇒ แก้ 3 จาก 12 แปลว่าเธอวาป
ครั้งที่สี่แล้วเจอ `LV 1` อีก ซึ่งจะอ่านเป็น "ยังไม่หาย" · ย้อนออกได้ทีละไฟล์ถ้า COO ไม่เห็นด้วย
เขียนไว้ในจดหมายถึง chief (`notes_to_chief/20260902_0158_LANE-A-REPORT-*.md`) ด้วย

### ฉากที่ต่อไม่ได้: ฉาก 1 (Port Royal)

`world_port_royal_identity` ไม่มีคอลัมน์ level ที่ mine ไว้เลย · **ไม่เดา ไม่ใส่ default** —
โมดูลใหม่ไม่มี default ของ `level` เลย และมีเทสบังคับว่าห้ามมี ⇒ เปิด **`RE-199`** ให้สาย RE
(สายเดียว ไม่ใช่ "RE หรือ chief") ขุด `MOBS.n_LEVEL_MIN` ของแถวที่ฉากนี้ชิปจริง

## 5. หลักฐานสองชั้น

- **wire/DB (ทำแล้ว)**: `tests/test_world_census_level.py` (14 เทส) + เทสรายฉากใน
  `test_world_population_bg0006/0009/0015.py` — อ่านค่ากลับออกจาก `generation.pc` รายตัว
  ครบทุกฉากที่ต่อสาย · พินไว้ด้วยว่า `make_npc_attr` เปล่า ๆ **ยังไม่ส่ง level** (กัน revert เงียบ)
  · full suite **6624 passed / 327 skipped / 14112 subtests**
- **client-observable (ยังไม่ทำ ต้องมีคนหน้าจอ)**: เปิด **`GT-200`** (ท้าย `GAME_TEST_QUEUE.md`,
  8,150 B < 8 KB ตาม ADDENDUM H) สถานะ `PENDING` จนกว่า PR #524 จะขึ้น main

## 6. pf-adversary

รันก่อน commit ตามกติกา ผลและสิ่งที่แก้ตามผล อยู่ในหัวข้อนี้ของไฟล์ฉบับที่ push (ดู PR body ประกอบ)

## 7. nonclaim

1. ไม่แตะสี/ป้าย/faction/ชนิด actor/identity เลย — P0-2 ยังไม่ปิด และ Codex ระบุสถานะสีเป็น
   `NOT_READY_FOR_POLICY_CHANGE` · รอบนี้ไม่ได้พูดอะไรเกี่ยวกับสีทั้งสิ้น
2. ไม่ได้พิสูจน์ว่าไคลเอนต์ **วาด** เลเวลที่ส่งไป — ชั้น wire พิสูจน์แค่ว่าไบต์ออกจากเซิร์ฟเวอร์
   (`GT-200` เท่านั้นที่ตัดสิน) · ถ้ายังเห็น `LV 1` ทั้งที่ไบต์ออกไปแล้ว = หลักฐานใหม่ ไม่ใช่ FAIL ของรอบนี้
3. `n_LEVEL_MIN` เป็นค่า min ไม่ใช่เลเวลที่เซิร์ฟเวอร์เดิมสุ่มต่อ spawn — ฉาก 2 มี `level_max`
   ต่างจาก `level` จริง รอบนี้เลือกส่ง min อย่างเปิดเผยเพราะไม่มีหลักฐานเรื่องการสุ่ม
4. ตรวจเส้นทางที่ประกอบ census ซ้ำแล้วหนึ่งเส้น: `mob_scene_recompose` ใช้
   `world_population_bg0002` เป็น composer ของฉาก 2 ตรง ๆ (`_COMPOSERS`) ⇒ สืบทอดการแก้นี้เอง
   ไม่มีทางเกิดฉากที่ census แรกมี level แต่ recompose ไม่มี · **ยังไม่ได้ไล่** diagnostic modules
   และเส้นทางอื่นที่เรียก `make_npc_attr` เอง (`mob_diag_multi_object`, `npc_*_hypothesis`,
   `remote_player_hypothesis` ฯลฯ) — พวกนั้นไม่ใช่ census ปกติและไม่อยู่ในใบสั่งนี้

## 8. จบรอบ

push ทั้งสอง repo -> แก้หัวข้อ/body ให้มี `PF-AUTOMERGE: v4` (GET ยืนยัน) -> ปลด draft ด้วย
`update_pull_request(draft=false)` -> ยืนยัน `draft:false` -> **wake gate commit เปล่าเฉพาะ
`pirate-force-server`** ตามข้อ 4 ของพรอมป์

**รอบนี้ขยับ NOW ข้อไหน: GM-A** (ส่วน "วาปแล้วต้องเจอ NPC ปกติทุกแมพ" — ปิดอาการ `LV 1` ที่
`GT-192` เห็น) · ยังไม่ติ๊กได้ ต้องรอ Panya รัน `GT-200`

-- LANE-A (WORLD) round `7ste68`
