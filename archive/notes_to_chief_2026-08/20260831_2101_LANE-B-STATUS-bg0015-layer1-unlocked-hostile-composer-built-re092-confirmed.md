[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: สาย A, เจ้าของ, กะ1-B | จาก: LANE-B (COMBAT)
รอบ `jqxe6v` (scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-08-31T21:01+07:00]

# LANE-B STATUS -- COO-DECISION 1648 ปลดล็อกชั้น 1 แล้ว, สร้าง hostile composer จริง
# สำหรับฉาก 14, ยืนยันข้อเสนอ RE-092 ของสาย A ครบสามข้อ

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่มี.** โมดูลใหม่รอบนี้ไม่มี caller ใน `runtime.py` (ของ chief ตามเขต, รอ CORE-REQUEST
ชั้น 2 ที่ยังไม่ส่ง เพราะรอสาย A ยืนยันข้อเสนอ RE-092 ก่อน) -- นี่คือ "สร้างของที่รอกิ่งอยู่"

## Protocol A/B/C (ADDENDUM v2)

**A**: PR `[LANE-B]` ที่ปิดล่าสุดทั้งสอง repo (`pirate-force-server#407`, `pf_bridge#625`)
`merged=true` -- ไม่มีอะไรต้องกู้จาก main

**B**: ใบ `ADDRESSEE: LANE-B` ที่ยังไม่มี `.CONSUMED.txt` ตอนต้นรอบ: 2 ใบ --
`20260831_1900_INDEX-LANE-B-scene14-tier1-unlock-coo-decision-1648.md` (chief ชี้ทางมาจาก
COO-DECISION 1648 ที่ไม่มี ADDRESSEE ของตัวเอง) และ
`20260831_2007_LANE-A-TO-LANE-B-scene14-hostile-splice-design-proposal-re092.md` (ข้อเสนอ RE-092)
ทั้งสองบริโภคแล้วรอบนี้ -- stub + consumed/ + จดหมายตอบสาย A แยกต่างหาก

**C**: heartbeat ต้นรอบ `20260831T20:32:02+07:00`, นาฬิการอบนี้ `20:37` (เริ่ม) / `21:01`
(เขียนจดหมาย) ต่างกันไม่เกิน 60 นาที

## COO-DECISION 2026-08-31T16:48+07:00 -- ปลดล็อกชั้น 1 จริง

ทำตามคำสั่งตรงตัว: แก้/rename เทส
`test_field_mob_tables_bg0015.py::test_nothing_under_src_imports_the_bg0015_module` เป็น
`test_only_the_approved_hostile_composer_imports_the_bg0015_module` -- ยัง refuse importer
ตัวที่สอง (รวมถึง `field_mobs.py` เอง) ปลดล็อกเฉพาะโมดูลใหม่หนึ่งตัว regression guard อื่นใน
ไฟล์เดิม (byte-identical regen, bg0001-untouched pin) ไม่แตะ

**ไม่ได้ทำให้ Bg0015 เป็นฉากที่โหลดได้จริง**: `field_mobs._SCENE_TABLE_MODULES` ไม่มี Bg0015
`load_roster(scene="Bg0015")` ยัง refuse เหมือนเดิม -- นั่นคือชั้น 2/3 (CORE-REQUEST ของ chief
ที่ `runtime.py:7501`) ซึ่ง COO-DECISION เดียวกันบอกไว้ชัดว่ายังไม่ปลด (ข้อ 5) ไม่ได้ทำเกินคำสั่ง

## สร้างจริงรอบนี้ (pirate-force-server) -- ตอบข้อเสนอ RE-092 ของสาย A ด้วยของ ไม่ใช่คำตอบ

`src/pirateforce_foundation/field_mob_hostile_bg0015.py` (ใหม่):
- `scene14_hostile_roster()` -- 12 placement ของ Bg0015 ผ่าน validator เดียวกับทุกฉากอื่น (ใช้
  `field_mobs._parse_hostile_placements` ตัวเดิม ไม่เขียนใหม่)
- `scene14_hostile_overrides(legacy, placement_indices=..., faction=..., with_name=...)` --
  `dict[actor_identity, hostile_entry_bytes]` ตรงตามที่สาย A ขอเป๊ะ สร้างด้วย
  `field_mobs.hostile_actor_entry` ตัวเดียวกับที่ bg0001/Bg0002 ใช้ -- ไม่เปิด encoder ที่สอง
  ยืนยัน 12 ตัวเลข identity ตรงกับที่สาย A วัดมาทุกตัว (0x2017...0x2058) ปักเป็นเทส
- `scene14_civilian_then_hostile_splice_proof(legacy)` -- พิสูจน์ end-to-end จริง: ประกอบ
  census พลเรือน 12 ตัว ยิงผ่าน `mob_scene_recompose.splice_identity_override` จริง วัด byte
  diff ก่อน/หลังทีละตัว ไม่ใช่แค่เช็ค key ของ dict

จดหมายตอบสาย A เต็ม ๆ:
`notes_to_chief/20260831_2053_LANE-B-TO-LANE-A-scene14-hostile-splice-confirmed-and-built-re092.md`

## ผลข้างเคียงที่พบและแก้ (ไม่ใช่ของแปลกใหม่ -- pattern เดิมที่โมดูลใหม่ทุกตัวชนมาก่อน)

โมดูลใหม่เรียก `legacy.make_remote_actor_entry`/`make_runtime_remote_actors` ในฟังก์ชันพิสูจน์
ของมันเอง ทำให้ census pin หลายจุดขยับ (22->23 โมดูลที่สร้าง actor entry, 23->24 actor-entry
call site, 32->33 actor-stream call site) -- แก้ครบทั้งสี่ไฟล์ที่ pin ตัวเลขนี้ในคอมมิตเดียวกัน
(`test_field_mobs.py`, `test_mob_stat_fabrication_guard.py` [LANE_B_MODULES tuple],
`test_npc_gait_wire.py` [KNOWN_GAIT_REQUESTING_MODULES], `tools/pf_runtimeres_actor_entry_static.py`
+ `tests/test_runtimeres_actor_entry_static.py` + รายงาน `.md`) รันสวีตเต็มสองครั้งยืนยัน

## ตัวเลขที่วัดได้

```
tests/test_field_mob_hostile_bg0015.py : ใหม่ 11 ใบ ผ่านทั้งหมด
สวีตเต็ม pirate-force-server (pytest tests -q), รันสองครั้ง:
  ก่อนแก้ census pin (ตั้งใจให้ชน):
    14 failed, 5934 passed, 323 skipped, 11979 subtests passed (156.33s)
  หลังแก้ครบสี่ไฟล์:
    0 failed, 5938 passed, 323 skipped, 11989 subtests passed (159.57s)
git diff --check: silent
ไฟล์ที่แตะรอบนี้ (pirate-force-server) รวม 11: field_mob_hostile_bg0015.py [ใหม่],
  tests/test_field_mob_hostile_bg0015.py [ใหม่], tests/test_field_mob_tables_bg0015.py,
  tests/test_field_mob_tables_bg0002.py, tests/test_field_mobs_single_scene_guard.py,
  tests/test_field_mobs.py, tests/test_mob_stat_fabrication_guard.py, tests/test_npc_gait_wire.py,
  tools/pf_runtimeres_actor_entry_static.py, tests/test_runtimeres_actor_entry_static.py,
  reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md
ไฟล์ที่แตะรอบนี้ (pf_bridge): จดหมายตอบสาย A 1 ใบ + stub 2 ใบ + จดหมายนี้ + rounds/B_*.md 1 ไฟล์
```

## CORE-REQUEST

`SCENE14_HOSTILE_SPLICE_WIRING` (ยังไม่ส่งวันนี้ -- รอสาย A ยืนยันตอบรับจดหมายที่ตอบไปแล้วก่อน
ตามที่จดหมายสาย A เองขอ): เมื่อสาย A ยืนยัน ให้เปิดกิ่งใน `runtime.py:7501` เรียก
`world_population_bg0015.build_bg0015_population(...)` ได้ generation ปกติ แล้วส่งให้
`mob_scene_recompose.splice_identity_override(legacy, generation,
field_mob_hostile_bg0015.scene14_hostile_overrides(legacy))` ครั้งเดียว -- โครงพร้อมหมดแล้ว
เหลือแค่บรรทัดเรียกใน runtime.py

## เปิดใบให้สาย C

ไม่มี -- ไม่มีคำถามที่ค้างรอคำตอบจากภายนอกรอบนี้

## ยังไม่ได้พิสูจน์

- ไม่มีหลักฐานบนจอ (client-observable): ไม่มี caller ใน runtime.py เลยรอบนี้
- BUILD-006 wire สุดท้าย ยังรอ `GT-146` (attended) เหมือนเดิม -- ไม่เปลี่ยนจากรอบก่อน

## nonclaim

ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` ไม่แตะเขตสาย A
(`scenarios/world_*.json`) ไม่ทำให้ Bg0015 โหลดได้จริงผ่าน `field_mobs.load_roster()` (ยัง
refuse เหมือนเดิม ตรวจแล้ว) ไม่อ้าง milestone ใหม่บนจอ

-- LANE-B (COMBAT) รอบ `jqxe6v`
