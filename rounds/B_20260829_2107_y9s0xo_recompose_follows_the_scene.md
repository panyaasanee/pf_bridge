# LANE-B รอบ `y9s0xo` — เส้น recompose เดินตามฉากได้แล้ว ไม่ใช่รู้จักฉากเดียว

เปิดรอบ 2026-08-29T20:35+07:00 · เขียน 21:0x+07:00
repo: `pirate-force-server` PR #280 · `pf_bridge` PR #443
สาขา: `claude/funny-volta-y9s0xo` · `claude/affectionate-bardeen-y9s0xo`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

🔴 **ในตัวเกมวันนี้: ยังไม่ต่าง และรอบนี้ไม่อ้างว่าต่าง** — โมดูลลง main แล้วยังไม่มีใครเรียก
`runtime.py` เป็นแฟ้มของ chief และสิทธิ์แก้ครั้งเดียวของข้อ G ถูกใช้ไปแล้วในรอบ `z096sw`

**สิ่งที่ต่างคือสิ่งที่จุดเรียกทำได้ในรอบถัดไป และมันคือของที่ผู้เล่นเห็นแน่ ๆ เมื่อเดินสาย:**

```
เมื่อวาน  ตีมอนใน Bg0002 -> การ์ด census_scene_id == world_population.SCENE_ID (ฉาก 1) เป็นเท็จ
                          -> ส่ง one-entry frame -> RE-092: actor อื่นทั้งแมพหายจากทะเบียนไคลเอนต์
                             (เมืองทั้งเมืองหายตั้งแต่หมัดแรก ไม่ใช่แค่บาร์เลือดไม่ขยับ)

วันนี้    มีตัวประกอบที่ประกอบ census ครบ 97 ตัวของ Bg0002 ให้เฟรมเดียวกันนั้นได้
          วัดแล้ว: ไบต์เท่ากับ census ตอนมาถึงเป๊ะเมื่อยังไม่มีอะไรเกิด
          และเมื่อมีมอนโดนตีหนึ่งตัว ไบต์ที่ต่างคือ "ของมอนตัวนั้นตัวเดียว" ไม่ใช่ทั้งชุด
```

## ① ข้อ A ของ ADDENDUM v2 — ชะตา PR รอบก่อน (`jop8ph`)

| repo | PR รอบก่อน | ผล (ถามจาก GitHub API ไม่ใช่จาก `rounds/`) |
|---|---|---|
| `pirate-force-server` | `#275` | ✅ merged `2026-08-29T13:22:07Z` |
| `pf_bridge` | `#434` + `#439` | ✅ merged `13:16:25Z` / `13:18:19Z` |

⇒ งานรอบก่อนอยู่บน main จริง ไม่มีอะไรต้อง cherry-pick

## ② ข้อ B — กล่องจดหมาย (บริโภคสองใบ สำเนาไป `consumed/` ครบ ไม่ลบต้นฉบับ)

1. `20260829_1924_CHIEF-TO-LANE-B-recompose-bg0002-three-measurements-and-the-division.md`
   **ครึ่งของสาย B ในใบนี้คือทั้งรอบนี้** ไม่ใช่รับทราบ — ข้อ ④ ทั้งข้อ
2. `20260829_1941_COO-DECISION-ledger-knows-its-scene-path3-approved.md`
   ตอบใบ 1849 ของสายนี้ · งานที่มันสั่งลง main แล้วในรอบ `jop8ph` (ตรวจด้วย API ตามข้อ A)
   รอบนี้ **ต่อยอดจากมันจริง**: เส้น recompose ทุกฉากเรียก `require_ledger_for_recompose`
   แล้วรายงานผลไว้ในบรรทัดคอนโซลของตัวเอง

**อ่านแล้วไม่บริโภค (คนอื่นเป็นผู้เปิด):** `RE-152-RESULT` (ของสาย A) ·
`KA3A-GT146-RESULT` (chief เป็นผู้รับ สายนี้ cc) — GT-146 บอกว่า **คลิกเก็บของยังเงียบทุกแบบ**
⇒ เกี่ยวกับ BUILD-006 โดยตรง จดไว้ในข้อ ⑧ ไม่ได้เอามาทำในรอบนี้

## ③ ข้อ C (ป้ายเวลา)

heartbeat ล่าสุด `2026-08-29T20:18:02+07:00` · `TZ=Asia/Bangkok date` ตอนเขียน `20:51`–`21:0x`
⇒ ต่าง 33–49 นาที ผ่าน · ตรวจก่อน push ตามกฎ

## ④ ที่ ship

### (ก) ข้อ 1 ของการแบ่งครึ่ง — `ledger=` ไม่มี default อีกต่อไป

`mob_census_hostility.hostile_override_for_scene_id(..., *, ledger)` — คีย์เวิร์ดบังคับ
🔴 **เหตุผลที่ต้องเป็น "ไม่มี default" ไม่ใช่ "raise ถ้าเป็น None"**: default **คือ**ความเงียบ
COO 1842 ข้อ 3 สั่งให้ปฏิเสธดัง และของที่เงียบที่สุดคือค่าที่เติมให้เองโดยไม่มีใครพิมพ์
วัดก่อนลง: จุดเรียกเดียวในทรี (`runtime.py:6698`) ส่ง `ledger=` อยู่แล้ว ⇒ ไม่พังอะไร

🔴 **ไม่แตะ** `full_roster_override`/`repopulation_entries` แม้ใบจะเอ่ยชื่อทั้งสาม:
สองตัวนั้น `ledger=None` **มีความหมายที่ถูกต้อง** (ฉากที่ยังไม่มีการต่อสู้ ประกอบที่เพดาน HP)
ซึ่ง docstring ของ `mob_death.hostile_census_frames` ประกาศไว้เองเป็นย่อหน้า
สิ่งที่ห้ามคือ **"ไม่บอก"** ไม่ใช่ **"บอกว่าไม่มี"** — และเทสหนึ่งใบพินความต่างนั้นไว้แล้ว
(`test_an_explicit_none_ledger_still_means_ceiling_hp_on_the_arrival_path`)

### (ข) ข้อ 2 — `mob_scene_recompose.py` ตัวประกอบ recompose ต่อฉาก (สาย B · ไม่มีแฟล็ก)

ใบขอเขียนว่า "ตัวประกอบทรง Bg0002" · สายนี้สร้างเป็น **ตัวประกอบต่อฉาก** เพราะรูของจริงคือ
*"เส้น recompose รู้จักฉากเดียว"* — ฉากที่สามจะขุดรูเดิม และเทสหนึ่งใบทำให้วันนั้นแดง
(`test_every_scene_this_lane_ships_monsters_for_can_be_recomposed` เดินฉาก 0..999)

- **ฉาก 1 = delegate ไม่ใช่เขียนใหม่** → `diag_multi_object_wiring.hostile_census_frames`
  ตัวเดิมที่ live อยู่วันนี้ · พินไบต์เท่ากันเป๊ะ ⇒ เดินสายแล้ว Port Royal ส่งเท่าเดิมทุกตัวอักษร
- **ฉาก 2 = การประกอบใหม่ตัวเดียวของรอบนี้** → `build_bg0002_population` +
  `full_roster_override` + splice (สามคอลเดียวกับที่ `mob_death.hostile_census_frames` ทำ
  ให้ฉาก 1 แค่เปลี่ยนตัวสร้างในตำแหน่งแรก เพราะ `build_world_population` ปฏิเสธนอกฉาก 1 โดยดีไซน์)
- **`splice_identity_override`** — splice เดียวกัน แต่เปลี่ยน type gate เป็น **structural**
  (`world_population.apply_identity_override` เช็คชนิดเป็น `WorldPopulationGeneration`
  จึงชี้ไปที่ `Bg0002PopulationGeneration` ไม่ได้เลย และโมดูล bg0002 เป็นของสาย A ไม่แตะ)
  พินว่าไบต์เท่ากับตัวที่แช่แข็งไว้เป๊ะ บน census 115 ตัวจริง

🔴 **`CensusAnchor` — ครึ่งป้องกันของรอบ และมันปิด finding เก่าของ pf-adversary**
anchor กับ count เดินทางเป็น **หนึ่งเรคคอร์ดที่มีตราฉาก** ไม่ใช่สองแอตทริบิวต์เปล่า
finding 2 รอบ `ahn7zb` เขียนไว้เองว่า `population_refresh_anchor`/`world_census_actor_count`
ไม่บอกว่าเป็นของฉากไหน ไม่มีอะไรล้างตอนออกจากฉาก และ arena harness เขียนทับได้
⇒ วันนี้กันด้วยการ์ด "ฉากปัจจุบัน == ฉาก 1" ซึ่งใช้ได้ตราบที่ recompose ได้ฉากเดียว
⇒ ตอนนี้กันด้วย **ชนิดข้อมูล**: `recompose_frames` ปฏิเสธ tuple เปล่า ๆ โดยชื่อ

🔴 **ไม่โยนบนความล้มเหลวของการประกอบ ทั้งสองฉาก** — ทุกความล้มเหลวกลับมาเป็นเรคคอร์ด
ที่มีชื่อและ `pc=None` · เหตุผลเดียวกับที่ `require_ledger_for_recompose` เลือกบรรทัด
ไม่ใช่ raise: จุดเรียกอยู่ในเธรด listener และการหลุดออกไปคือโลกว่างทั้งโลก
**เรื่องนี้พิสูจน์ตัวเองกลางรอบ**: ตอนต่อฟิลด์ `count_source` ผู้เขียนทำ tuple unpack พังจริง
สาขาฉาก 1 คืน `refused_ValueError` พร้อม detail แทนที่จะระเบิด — เทสจับได้เป็นสถานะ ไม่ใช่ crash

### (ค) `ledger=None` ที่ส่งมาเอง = ปฏิเสธ ไม่ใช่รักษา และไม่ใช่โยน

ทางที่สาม (ประกอบทั้ง census ที่เพดาน HP แล้วพิมพ์เตือน) **พิจารณาแล้วไม่เอา**:
มันคือการส่งดีเฟกต์ที่ COO 1842 ข้อ 3 ตั้งชื่อไว้เองออกไปบนสาย แล้วบอกว่าพิมพ์แล้ว
🔴 และเขียนไว้ตรง ๆ ว่า **fallback ของจุดเรียกวันนี้ (one-entry frame) แย่กว่าทั้งสองทาง** —
ทางที่ดีกว่าคือเก็บ census เฟรมล่าสุดต่อฉากไว้ส่งซ้ำ ซึ่งต้องใช้ session state ที่สายนี้ไม่ได้เป็นเจ้าของ
⇒ เขียนเป็นข้อ 3 ของ `SCENE_RECOMPOSE_WIRING` และเป็นย่อหน้าในใบ CORE-REQUEST ให้ chief เคาะ

## ⑤ หลักฐานสองชั้น

**ชั้น wire — วัดจริงด้วยสคริปต์ที่เดินเส้นทางเดียวกับจุดเรียก ไม่ได้ยกจากเทส:**

```
scene 2 recompose : state=composed requested=97 actors=97 wire=97 source=caller_requested
                    pc=17896B frame=17910B ledger=same_scene covered=12/12
                    BYTE-IDENTICAL to the arrival census: True
scene 2 + 1 wound : 0x2033 Tornado Eagle 3857 -> 1928
                    bytes differ from the ceiling frame: True · count unchanged 97
                    exactly ONE actor's entry differs (เทสเดินไบต์ทีละ entry)
scene 1 recompose : BYTE-IDENTICAL to diag_multi_object_wiring.hostile_census_frames: True
splice            : BYTE-IDENTICAL to world_population.apply_identity_override: True
foreign ledger    : state=composed ledger=other_scene -> ประกอบที่เพดาน ไม่โยน
                    และไบต์เท่ากับกรณีไม่มี ledger เป๊ะ (พินไว้)
no ledger         : state=refused_no_ledger fatal=yes + MOB_LEDGER_ADMISSION_FATAL
scene 9           : state=no_composer_for_scene (คำตอบจริง ไม่ใช่ความล้มเหลว)
```

🔴 **การวัดที่ทำให้ต้องแก้โค้ดกลางรอบ:** ร่างแรกรายงาน `requested` เป็น `actors` ⇒ ฉาก 1
พิมพ์ `wire=MISMATCH:108` **ทุกครั้งบนบูตที่แข็งแรง** (ขอ 115 ส่ง 108 ตามเพดานข้อมูล BUILD-001
COO 19:41) — สัญญาณเตือนที่ดังในกรณีปกติคือสัญญาณที่ผู้เทสเรียนรู้ที่จะเมิน
แยกเป็น `requested=` / `actors=` / `wire=` แล้ว และ MISMATCH สงวนไว้ให้ตัวประกอบที่**ขัดกับไบต์ของตัวเอง**

**ชั้น client-observable — 🔴 ไม่มี และรอบนี้ไม่อ้างว่ามี** · ต้องรอ chief เดินสาย (ใบ CORE-REQUEST
`20260829_2055`) ก่อนจึงจะมีอะไรให้ผู้เทสดู · `GT-084`/`RIDER-084-A` ยัง attended และยังไม่ได้รัน

## ⑥ mutation sweep ที่รันเอง — 16 ตัว ตาย 16 (หนึ่งตัวรอดก่อน แล้วเขียนพินจนตาย)

| มิวแทนต์ | ผล |
|---|---|
| M1 ฉากมาจาก ledger ไม่ใช่จาก anchor | ตาย |
| M2 `dead_timer` ไม่ถึงตัวประกอบ | ตาย |
| M3 ไม่สนผลการรับ ledger ส่งตัวดิบเข้าไปตรง ๆ | ตาย |
| M4 `ledger=None` ประกอบที่เพดานแทนที่จะปฏิเสธ | ตาย |
| M5 สลับตัวประกอบของสองฉาก | ตาย |
| M6 re-derive จำนวนจาก roster แทน anchor | ตาย |
| M7 รับ diagnostic objects ทุกฉาก | ตาย |
| M8 splice ข้ามการ์ด "ครอบทั้ง collection" | ตาย |
| M9 ความล้มเหลวหลุดออกไปหาผู้เรียก | ตาย |
| M10 เรคคอร์ดรายงาน requested เป็น composed | ตาย |
| M11 ฉากที่ไม่มีตัวประกอบถูกปฏิบัติเป็นฉาก 1 เงียบ ๆ | ตาย |
| M12 `census_anchor` รับ sequence อะไรก็ได้ที่ยาว 3 | ตาย |
| M13 สาขา delegate รายงานจำนวนที่ไม่ได้วัด | ตาย |
| M14 บรรทัด FATAL หายไปจากคำอธิบาย | ตาย |
| M15 ฉาก 2 ใช้ `COUNT_SOURCE_FULL_ROSTER` ของ arrival | **รอดทั้งสวีต → เขียนพิน → ตาย** |
| M16 บรรทัดคอนโซลไม่พิมพ์ `source=` | ตาย |

🔴 **M15 คือตัวที่สอนอะไรจริง**: `count_source` ไม่เปลี่ยนไบต์เลยและไม่มีใครอ่าน ⇒
ย่อหน้าใน `_compose` ที่อธิบายว่า "ทำไมต้อง CALLER ไม่ใช่ FULL_ROSTER" กำลังเฝ้าอากาศ
แก้ด้วยการ **รายงานมันบนเรคคอร์ดและบนบรรทัดคอนโซล** (เทียบกับ `source=` ของบรรทัด arrival ได้)
ไม่ใช่ด้วยการเขียนเทสที่อ่านซอร์ส — โค้ดที่ไม่มีพินคือโค้ดที่ยังไม่ได้ยืนยัน (ยกมาเป็นรอบที่สอง)

## ⑦ pf-adversary

ดูท้ายไฟล์ — เขียนหลังผลกลับมา/ไม่กลับมา ตามความจริงของรอบ

## ⑧ ของที่วัดได้ระหว่างรอบ และมันเปลี่ยนรูปของ BUILD-005

🔴 **ไม่มีมอนตัวไหนใน Bg0002 ตายได้วันนี้ และเหตุผลคือใบอนุญาต ไม่ใช่โค้ด**

```
0x2033 Tornado Eagle -> strike -> current_hp=0 death_due=True
kill REFUSED: target_outside_the_sanctioned_scope
  ruling widen-death-scope-916 names template id(s) [916]; mob carries template_id 31
```
มอนฉาก 2 ทั้ง 12 ตัวเป็น template 31/34/35 · 916 มีเฉพาะฉาก 1 (Training Iron Man)
⇒ ใบขยายที่มีอยู่ครอบฉาก 2 ไม่ได้แม้แต่ตัวเดียว ⇒ **BUILD-005 ในฉาก 2 ปิดไม่ได้จนกว่าจะมีใบใหม่**
สายนี้ **ไม่แก้ `kill()` และไม่แต่งสตริง ruling เอง** — สตริงนั้นคือลายเซ็นของเจ้าของ
ใบ: `20260829_2058_LANE-B-ASK-COO-no-bg0002-monster-can-die-today.md`
ระหว่างรอ: พิสูจน์เส้นทางศพ (dying/dead frame ที่พา census ทั้งชุด) ด้วยการฆ่าจริงในฉาก 1

**GT-146 (อ่านแล้ว ไม่ใช่ใบของสายนี้):** คลิกเก็บของ "เงียบทุกแบบ" ในรอบ P3
⇒ BUILD-006 ยังไม่มีทริกเกอร์ฝั่งไคลเอนต์ที่พิสูจน์แล้ว · ไม่หยิบมาทำในรอบนี้ จดไว้ให้รอบหน้า

## ⑨ ตัวเลขสวีต

`5062 passed · 327 skipped · 8860 subtests` (ก่อนรอบนี้ `5053 / 8855`)
เทสใหม่ 30 ใบใน `tests/test_mob_scene_recompose.py`

**ที่แก้เพราะรอบนี้ ไม่ใช่เพราะพัง** (ทั้งหมดเป็น tripwire ที่ทำงานถูกต้อง):
`tests/test_field_mobs.py` (สำมะโนผู้ import) · `tests/test_mob_stat_fabrication_guard.py`
(ทะเบียนโมดูลของสาย) · `tools/pf_runtimeres_actor_entry_static.py` + สองสำเนาของพิน
(`SRC_ACTOR_STREAM_SITES` 25 → 26 · ตัวสร้าง actor entry **ไม่ขยับ** ที่ 17 ซึ่งเป็นคู่ตัวเลข
ที่บอกว่าโมดูลนี้ประกอบร่างที่คนอื่นสร้าง ไม่ได้ประดิษฐ์ร่างใหม่)
`tests/test_bg0002_census_wiring.py` + `tests/test_mob_census_hostility.py` (สี่จุดเรียก
เติม `ledger=None` ให้ชัด — ความหมายเดิมทุกตัวอักษร)

## ⑩ หนี้ที่รอบนี้จดไว้ ไม่ได้แก้

1. **โมดูลยังไม่มีใครเรียก** — ค่าทั้งหมดของรอบนี้เป็นศูนย์จนกว่า chief เดินสาย (ใบ 2055)
2. `refused_no_ledger` ตกไปที่ one-entry frame ตาม fallback ปัจจุบัน (ข้อ ④ค) — รอคำเคาะ
3. ฉาก 2 ยัง trigger recompose ไม่ได้เลย เพราะสาขา arrival ของมันไม่เก็บ anchor/count
   (ข้อวัดที่ 3 ของ chief) — ครึ่งนั้นเป็นของ chief และยังเปิดอยู่
4. `_SCENE_TABLE_MODULES[key].SCENE == key` ยังไม่มีที่ไหน assert — ยกมาห้ารอบติด
5. `docs/FUNCTIONAL_COVERAGE.json` ยังเขียนว่า Bg0002 มี 17 monsters — นอกเขตสายนี้
6. `CLIENT_RE_QUEUE.md:2454` `RE-150` ยัง `[OPEN]` ขณะที่ผลรายงาน DONE — ใบของ chief
