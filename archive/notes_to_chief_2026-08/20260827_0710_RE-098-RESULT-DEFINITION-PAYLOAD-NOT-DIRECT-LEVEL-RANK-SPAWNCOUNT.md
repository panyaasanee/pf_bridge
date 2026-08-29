[ถึง: chief cloud (cc), สาย B (COMBAT), COO และ Panya · จาก: RE runner LOCAL · 2026-08-27T07:10+07:00]

# RE-098 RESULT — DONE / BOUNDED-NEGATIVE: `b5`/`b15`/`u32@11` ไม่ใช่ level/rank/placement-count แบบตรง และยังไม่มี global definition→MOBS crosswalk

สถานะที่เสนอ: **`RE-098 [DONE / BOUNDED-NEGATIVE]`** — T0-T3 ปิดครบตามเกณฑ์จบใบ งานทั้งรอบเป็น static/read-only; ไม่เปิดเกม/server, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ source/queue/git

## ด่านค้นก่อนถอด (สองช่องบังคับ)

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** `00_SEARCH_HERE_FIRST.md` ระบุโครง `.npc` และแยก definition/placement count ไว้แล้ว; แต่ TSV ทั้ง 8 ชุด **ไม่เจอ** `Mob_Set`/`MOBSET`/`n_LEVEL_MIN`/`n_LEVEL_MAX`/`n_RANK`/`spawn_rate` หรือ scene-definition→MOBS crosswalk (คำว่า `definition_count` ที่เจอใน serializer trace เป็นจำนวน reaching definitions ของ disassembly คนละความหมาย)
- **ค้น gamedata แล้ว: เจอ** parser ที่มีอยู่แล้ว `gamedata/pf_decode_lua_npc.py` SHA `6ab38fd...f9e`, scene index 288 ไฟล์ใต้ `Data/Scene/Save`, placement TSV ที่มี `set_names`/`template_ids`, และ `CONSTDATA_TH__MOBS.tsv` ที่มี `n_LEVEL_MIN`/`n_LEVEL_MAX`/`n_RANK`; **ไม่เจอ** field ชื่อ/สัญญาณ `spawn_rate` และ placement TSV ไม่มี level/rank/spawn field

ดังนั้นใบเปลี่ยนจาก “เขียน parser ใหม่” เป็น **verify SHA + ใช้ parser เดิม + เขียน verifier เฉพาะ RE-098** ตามกฎคิว

## T0 — parser และ crosswalk ที่ใช้จริง

parser เดิมอ่าน `.npc` ทั้ง 288 ไฟล์ใต้ `Data/Scene/Save` แบบ exact-EOF ผ่านครบ: **3,745 definitions / 6,248 placements**; definition payload ทุกแถวยาว 16 ไบต์

crosswalk ที่อนุญาตให้เทียบกับ level/rank ได้มีขอบเขตเพียงสองฉากที่สาย B ทำ curated roster ไว้แล้ว (`field_mob_tables.py` และ `field_mob_tables_bg0015.py`):

`raw definition.name` ↔ `placements.tsv.set_names` (ข้อความตรงกัน) → `placement index + XYZ` ตรงกับ curated `HOSTILE_PLACEMENTS` → revalidate level/rank ของ curated MOBS id กับ `CONSTDATA_TH__MOBS.tsv`

เส้นนี้ให้ **30 hostile placements / 14 scene-scoped definitions** โดยไม่เปิด join ใหม่จากเลข local set id เท่ากับ MOBS id เฉย ๆ:

| scene/set | MOBS | level min-max | rank | b5 | b15 | u32@11 | placements/set |
|---|---:|---:|---:|---:|---:|---:|---:|
| Bg0015/MOBSET_31 | 31 | 27-27 | 1 | 0 | 0 | 100 | 4 |
| Bg0015/MOBSET_34 | 34 | 25-27 | 1 | 0 | 0 | 100 | 11 |
| Bg0015/MOBSET_35 | 35 | 27-27 | 1 | 0 | 0 | 100 | 1 |
| Bg0015/MOBSET_103 | 103 | 58-60 | 1 | 2 | 0 | 100 | 1 |
| bg0001/Mob_Set_31 | 31 | 27-27 | 1 | 2 | 2 | 100 | 1 |
| bg0001/Mob_Set_34 | 34 | 25-27 | 1 | 2 | 12 | 100 | 1 |
| bg0001/Mob_Set_35 | 35 | 27-27 | 1 | 2 | 6 | 100 | 1 |
| bg0001/Mob_Set_60 | 60 | 37-39 | 1 | 2 | 6 | 100 | 1 |
| bg0001/Mob_Set_61 | 61 | 38-40 | 1 | 2 | 3 | 100 | 1 |
| bg0001/Mob_Set_62 | 62 | 39-41 | 1 | 2 | 12 | 100 | 1 |
| bg0001/Mob_Set_65 | 65 | 43-45 | 1 | 0 | 0 | 100 | 1 |
| bg0001/Mob_Set_94 | 94 | 47-49 | 1 | 2 | 1 | 100 | 1 |
| bg0001/Mob_Set_97 | 97 | 51-53 | 1 | 2 | 0 | 100 | 4 |
| bg0001/Mob_Set_103 | 103 | 58-60 | 1 | 2 | 0 | 100 | 1 |

## T1 — `b5` เทียบ level

- `b5 == n_LEVEL_MIN`: **0/30 placements**
- `b5 == n_LEVEL_MAX`: **0/30 placements**
- positive control ข้ามฉาก: MOBS 31/34/35/103 มี level/rank เดิม แต่ `b5` เปลี่ยนตามฉากได้ (เช่น MOBS 31: Bg0015 `b5=0`, bg0001 `b5=2`)

สรุปจำกัดขอบเขต: `b5` **ไม่ใช่ level min/max แบบค่าตรง** ใน crosswalk ที่วัดได้; ยังไม่ตั้งชื่อ semantic อื่น

## T2 — `b15` เทียบ rank

`b15 == n_RANK` เพียง **1/30 placements** (bg0001/Mob_Set_94: 1==1); อีก 29/30 ไม่ตรง และ MOBS เดียวกันข้ามฉากมี `b15` ต่างกันได้ เช่น MOBS 31: `0` กับ `2`, MOBS 34: `0` กับ `12`

สรุปจำกัดขอบเขต: `b15` **ไม่ใช่ rank แบบค่าตรง**; 1 จุดที่เท่ากันไม่พอเป็น crosswalk

## T3 — `u32@11` เทียบสัญญาณ spawn-rate ที่วัดได้

สัญญาณเดียวในข้อมูลชุดนี้ที่วัดตรงได้คือจำนวน placement ต่อ set. ทั้ง 14 definition ที่ crosswalk ได้มี `u32@11=100` เหมือนกันหมด ขณะที่จำนวน placement ต่อ set เป็น **1, 4, 11** จึงไม่ใช่ direct placement count และไม่มี variance ฝั่ง `u32` ให้คำนวณความสัมพันธ์

bounded global census ของ raw 3,745 definitions:

- `u32@11`: `50×16, 100×3723, 200×1, 400×2, 500×2, 800×1`
- `b5`: `0×2158, 1×119, 2×1456, 3×12`
- `b15`: `0×3146, 1×15, 2×66, 3×71, 4×27, 5×45, 6×97, 7×30, 8×23, 9×77, 10×45, 11×21, 12×82`

แถว raw ที่ `u32` ไม่เท่ากับ 100 ยังเอาไปเทียบ monster level/rank/spawn-rate ไม่ได้ เพราะไม่มี global definition→MOBS crosswalk; ห้าม join จากเลข local id เท่ากันเอง

## verifier / integrity

- verifier ใหม่ (เขียนเฉพาะเขต `staged`): `pf_bridge/staged/re098_definition_payload_level_rank_static.py`
- SHA256: `e00594bbc407a1f1e94a24cb7cb823a01ff9f4c7dedcb6740c90e55faf3790b4`
- รันด้วย `python -B` **สองครั้ง**: `SUMMARY guards=523 failed=0` ทั้งสองครั้ง; ไม่มี `__pycache__`
- SHA รายตัวก่อน/หลังตรงกันทั้งหมดสำหรับ AGENTS, queue, NEW_ORDERS, search guides, parser, scene index, MOBS, raw/placement สองฉาก, curated roster สองไฟล์, AI table และ roster generator
- tree manifest ก่อน/หลังตรงกัน: external `30 files / cd917747...f483`; gamedata `1109 / 81c087df...54a`; raw Save NPC `288 / 3f4a0486...07f3`

## nonclaims

1. ไม่อ้างว่า `b5`/`b15`/`u32@11` ไม่มีความหมายหรือไม่มีความสัมพันธ์เชิงหมวดหมู่ทุกแบบ; ผลนี้ตัดเฉพาะ direct level/rank/count mapping ที่วัดได้
2. ไม่อ้าง global scene-definition→MOBS identity crosswalk; สองฉากนี้ยืนบน curated Lane-B roster + placement index/XYZ/text-name เท่านั้น
3. ไม่อ้าง original-server spawn-rate field หรือ runtime behavior; รอบนี้ไม่มี wire/client-observable evidence
4. ไม่สั่งให้สาย B แก้ `field_mob_tables*`; การตัดสิน production อยู่ในเขตสาย B

`BUILD_IMPACT: ไม่มี — ผล bounded negative นี้หยุดการนำ b5/b15/u32@11 ไปใช้เป็น level/rank/spawn-count โดยไม่มี crosswalk; production ควรใช้ MOBS/placement fields ที่พิสูจน์อยู่แล้วจนกว่าจะมีหลักฐานใหม่`

`BUILD_IMPACT_NONE: 1/1`

