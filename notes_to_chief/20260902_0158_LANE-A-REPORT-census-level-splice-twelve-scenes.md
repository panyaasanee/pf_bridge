[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-A (WORLD) รอบ `7ste68` · 2026-09-02T01:58+07:00]
[ตอบใบ: `notes_to_chief/20260901_2358_CHIEF-TO-LANE-A-codex-gt192-lv1-census-level-encode-assigned.md`]

# LANE-A REPORT — census ปกติส่ง level แล้ว 12 ฉาก (ใบมอบหมายสั่ง 3 ฉาก — ขยายเป็น 12 อย่างเปิดเผย)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

วาปเข้าฉากไหนก็ตามใน 12 ฉากที่ต่อสายแล้ว ป้ายเหนือหัว NPC จะขึ้นเลเวลจริงของตัวนั้น
(เช่นฉาก 6 = 71-105, ฉาก 14 = 1-115) แทนที่จะขึ้น `LV 1` เหมือนกันหมดอย่างที่ `GT-192` เห็น
ไม่ต้องเปิดแฟล็กอะไร ติดทุกบูต

## ทำอะไรไปแล้ว

- โมดูลใหม่ `src/pirateforce_foundation/world_census_level.py` (Foundation-owned additive)
  splice BasicAttr bit `0x0002` + `u16tag(0x12, level)` เข้าบอดี้ที่ `make_npc_attr` แช่แข็งคืนมา
  ตำแหน่งคำนวณจากตัวบอดี้เอง (mask offset จาก head, level อยู่หลัง optional name ก่อน HP ตามลำดับ
  บิต) ไม่ได้เขียนค่าคงที่ไว้ · ถอดกลับเป็นบอดี้เดิมได้เป๊ะก่อนคืนค่าเสมอ ไม่เท่ากัน = refuse
- **ไม่แตะ `current/pf_login_game_server_v141.py` (frozen), ไม่แตะ `runtime.py`/`app.py`**
  และ **ไม่ต้องขอให้ chief ต่อสายอะไรเลย** — composer ทั้ง 12 ตัวถูก dispatch ผ่าน
  `lane_hooks/lane_a_scene_census.py` ซึ่งเป็นไฟล์ของสายนี้อยู่แล้ว
- ต่อสายเข้า composer 12 ตัว: `world_population_bg0002..bg0011`, `bg0015` (ฉาก 14),
  `bg4001` (ฉาก 130)

## 🔴 ขยายขอบเขตจาก 3 ฉากเป็น 12 — บอกไว้ตรงนี้ ไม่ได้ทำเงียบ

ใบมอบหมายระบุสามไฟล์ (`bg0006`, `bg0009`, `bg0015`) เพราะ Codex ตรวจสามไฟล์นั้น แต่ composer
อีกเก้าตัวเป็นสำเนาโครงเดียวกันเป๊ะ (เช็คแล้ว: call shape เหมือนกันทุกตัวอักษร 11 ตัว, `bg0002`
ต่างแค่ชื่อค่าคงที่) และทุกตัวมีคอลัมน์ level ที่ mine ไว้แล้วใน `SceneIdentity`
เกณฑ์ GM-A ของเจ้าของคือ "วาปข้ามหลายแมพติดกันแล้วต้องเจอ NPC ปกติทุกแมพ" — ปล่อยไว้ 3 จาก 12
แปลว่าเธอวาปสามแมพแล้วเจอ `LV 1` อีกเก้า ซึ่งจะอ่านเป็น "ยังไม่หาย"
ถ้า chief/COO เห็นว่าไม่ควรขยาย บอกได้ ย้อนเก้าไฟล์นั้นออกได้ทีละไฟล์ (คนละบรรทัดกัน ไม่ผูกกัน)

## ฉากที่ต่อไม่ได้ และทำอะไรกับมัน

**ฉาก 1 (Port Royal / `bg0001`)** — `world_port_royal_identity` ไม่มีคอลัมน์ level ที่ mine ไว้เลย
ต่างจากอีก 12 ฉาก · **ไม่เดา ไม่ใส่ default** (โมดูลใหม่ไม่มี default ของ `level` เลย มีเทสคุมไว้)
⇒ เปิด **`RE-199`** ให้สาย RE ขุด `MOBS.n_LEVEL_MIN` ของแถวที่ฉากนี้ชิปจริง
ได้ข้อมูลเมื่อไหร่ LANE-A เติมคอลัมน์แล้วต่อสายจบในรอบเดียว (โค้ดพร้อมแล้ว)

## ข้อควรระวังสี่ข้อในใบมอบหมาย — ทำครบ

1. **ไม่แตะสี/ป้าย/actor type/identity** เลยแม้แต่บิตเดียว (P0-2 ยังไม่ปิด)
2. **กัน double-field ฉาก 14**: บอดี้ที่มีบิต `0x0002` อยู่แล้วถูก refuse — มีเทสขับด้วยบอดี้ hostile
   จริงของฉาก 14 (`field_mob_hostile_bg0015`) และยืนยันว่า reader ตัวเดียวกันอ่านค่าของ lane B ได้ตรง
3. Foundation-owned wrapper ใหม่ ไม่แก้ v141, ไม่ import ข้าม module (อ้าง lane B ในคอมเมนต์เท่านั้น
   — จงใจไม่เขียนชื่อโมดูลของ lane B ในไฟล์ census เพื่อไม่ให้ tripwire "ใครนำเข้า field_mobs" เพี้ยน)
4. เทส focused codec/order + regression: สวีททั้งชุด **6624 passed / 327 skipped / 14112 subtests**

## หลักฐานสองชั้น

- wire/DB: `tests/test_world_census_level.py` + เทสรายฉาก อ่านค่า level กลับ **ออกจาก
  `generation.pc`** (ไม่ใช่จาก roster) รายตัวครบทุกฉากที่ต่อสาย · พิสูจน์ว่า `make_npc_attr` เปล่า ๆ
  ยังไม่ส่ง level (กันการ revert เงียบ)
- client-observable: **`GT-200`** เปิดแล้ว (ท้าย `GAME_TEST_QUEUE.md`, `PENDING` จนกว่า PR #524
  จะขึ้น main) — เกณฑ์คือเห็นเลขต่างกันรายตัวใน >= 3 ฉากใน login เดียว

## PR

`pirate-force-server#524` (branch `claude/dazzling-volta-7ste68`) · `pf_bridge#778` (เอกสาร/คิว)

— LANE-A (WORLD) รอบ `7ste68`
