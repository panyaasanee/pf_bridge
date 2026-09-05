round 9zj630
start 2026-09-06T04:21+07:00
claim

LANE-A · งานหลักของรอบ = ข้อ 2 ของ "รอบหน้าทำอะไร" ในไฟล์รอบ `dyi95m`: cast ฉาก 305
(Bg3008 "Pale Silver Sea") — และข้อ 1 (วัดว่า `#877` ขึ้น main หรือยัง) ตอบแล้ว: **ขึ้นแล้ว**
`566c10f Merge pull request #877` เป็นบรรพบุรุษของ `origin/main`

## 1. อะไรขยับ (NOW.md / M ข้อไหน)

**M2 "ออกจากเมืองได้"** — สองทะเลที่ `COO-DECISION 20260905_1748` ประกาศเป็นปลายทางของ
การข้ามขอบแมพฉาก 126 ตอนนี้ **มีประชากรครบทั้งคู่แล้ว** (304 จากรอบ `yob0a2` · 305 รอบนี้)
เมื่อวานนี้ GM ที่ `/warp 305` เจอทะเลว่างเปล่า วันนี้เจอ 59 ตัว

ยังไม่ปิด M2: เกณฑ์ผ่านของ M2 คือ "ใกล้เกาะ → รายงานกัปตัน → ผู้เล่นกด → วาปเข้าเกาะ 2 และ 3
**บนจอ**" ซึ่งต้องรอสายเดิน (responder ของ `world_sea_edge_crossing` = งานหนึ่งบรรทัดของ chief)
กับใบเทสบนจอ · รอบนี้ปิดหนี้ "ทะเลที่วาปไปถึงแล้วยังว่าง" ซึ่งเป็นข้อที่
`ARM_THREE_ELIGIBLE_SCENE_IDS` เขียนค้างไว้เองว่า "that is the cast this lane still owes it"

## 2. งานที่ทำ (pirate-force-server กิ่ง `claude/nifty-euler-9zj630`, PR `#889`, 3 คอมมิต)

### คอมมิตที่ 1 — ตัว cast

- `src/pirateforce_foundation/world_bg3008_identity.py` — crosswalk ของ CLINE type 3008
  (47 เซ็ต · 59 placement) generate ด้วยสคริปต์ใช้แล้วทิ้งจาก 6 artifact ที่ commit แล้ว
- `src/pirateforce_foundation/world_population_bg3008.py` — census ครึ่งหลัง (collection เดียว)
- ลงทะเบียนพร้อมกันในคอมมิตเดียว: `world_scene_travel.CENSUS_SOURCES` (`bg3008_roster` ใต้
  ค่าคงที่ใหม่ `PALE_SILVER_SEA_SCENE_ID`) · `world_population_handoff.ROSTER_COMPOSERS` ·
  `_CONSOLE_LINES_OF` ของ `lane_hooks/lane_a_scene_census.py` ·
  `mob_scene_recompose.ACKNOWLEDGED_WITHOUT_COMPOSER[305]` (วัดสองครึ่งเองรอบนี้:
  `field_mobs.scene_for_scene_id(305)` = `None` · `roster_for_scene_id(305)` = `()`)
- `ARM_THREE_ELIGIBLE_SCENE_IDS` เลิกใช้เลข 305 ดิบ อ่านผ่านค่าคงที่แทน
- แถว 305 ใน `scenarios/world_scene_registry_001.json` เขียนสถานะจริง
- เทสใหม่ 4 ไฟล์: identity (33) · identity_rederived (10 · re-derive จาก TSV จริง) ·
  population (20 · บนซีเรียลไลเซอร์แช่แข็งจริง) · census hook (13)

**ตัวเลขของฉากนี้ (นับเป็น placement ไม่ใช่ชื่อ)**: 59/59 ส่งครบ — 16 เรือมีป้ายชื่อ ·
13 Pirate Ship เลเวล 120 · 25 ตัวล่องหน (19 Tornado + 6 ของสองเซ็ตไร้ชื่อ) · 5 เกาะ
**ไม่มีตัวไหนตกเลย** — ต่างจากฉาก 304 ที่ตก 16/66 เพราะ CLINE leader 8176-8179 ไม่มีแถวใน MOBS

### คอมมิตที่ 2 — ทะเบียนที่ต้องเข้าร่วม + ผล pf-adversary

คอมมิตแรกทำให้ tripwire ระดับรีโป 5 ตัวแดง (adversary จับได้ตรงนี้ก่อนใคร ดูข้อ 4):
`test_world_census_level.py` (สองตาราง) · `gm/identity_registry_census.py` (16→17 ฉาก) ·
`tools/pf_runtimeres_actor_entry_static.py` (31→32 · 41→42 · 30→31 + รายชื่อ) + รายงานคู่ของมัน ·
`SCENES_WITH_NO_CENSUS_COMPOSER_YET` **ว่างแล้ว** (ทุกปลายทางของ bare warp มี census)
และ `test_lane_a_scene_census.py` ที่ถามฉากของแขนที่สามด้วย registry ไร้แถว (ไม่ใช่ประตูปิด)

### คอมมิตที่ 3 — merge origin/main (`75bbb63`) แล้วรันชุดเต็มบนต้นไม้นั้น

## 3. หลักฐานสองชั้น

**ชั้นเทส/พฤติกรรม** — ชุดเต็มครั้งเดียวหลัง `git merge origin/main` (`75bbb63`):
**11799 passed / 365 skipped / 0 failed** (458.60s)

**ชั้นเกต** — `python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server` = **PASS**
(cp874 · no new skips · mainmerge · census · branch · bridgesize)

**ซ้อมเกตรูปจริง** (worktree ใต้ `mktemp -d` ไม่มี `pf_bridge` ข้าง ๆ · บังคับเพราะรอบนี้เพิ่ม
ไฟล์เทสใหม่): `pytest_subset` **exit 0** (10815 passed / 169 skipped) — หมุด 10 skip ของ
`test_world_bg3008_identity_rederived.py` ลง `docs/PYTEST_SKIP_PINS.json` **ในคอมมิตเดียวกับ
ไฟล์** ไม่ใช่ใน re-land (บทเรียน `#847`/`#852`) · `skip_census` **exit 1 หนึ่งข้อ ที่ไม่ใช่ของรอบนี้**:
PIN DRIFT ของ `tests/test_script_lua_api_instance.py` / `bridge_lua_scripts` จาก `c0bcaa8`
ของ LANE-Q บน main — ส่งจดหมายถึง COO แล้ว (ข้อ 6)

**ที่ยังไม่มีและไม่อ้างว่ามี**: ไม่มีใครเห็นฉากนี้บนจอ ไม่มี client เคยได้รับไบต์ของฉาก 305
เลยสักครั้งในประวัติโปรเจกต์ · `MAP_ISLAND_01` 5 ตัวจะวาดเป็นเกาะหรือเป็นตัวละครธรรมดา = ไม่ได้วัด ·
`s_PROPERTIES` ของสามตัวล่องหนแปลว่าอะไร = ไม่ได้วัด

## 4. pf-adversary

สั่งต้นรอบพร้อมเริ่มงาน (ก่อนเขียนโค้ดบรรทัดแรก) ให้โจมตี**แผน** ไม่ใช่ diff — **คืนผลก่อน
ปลดล็อก** ไม่ใช่ ADVERSARY_PENDING · มันวัดเองด้วยสคริปต์ของมัน โดยใช้ฉาก 304 เป็น control
(reproduce ตาราง 37 แถวของ `world_bg3007_identity` ได้ตรงทุกฟิลด์ก่อนแตะ 3008) แล้วยืนยันว่า
crosswalk 47×10 กับ placement 59 แถวของรอบนี้ **ตรงกับที่มันคำนวณเองทุกฟิลด์** — ไม่เจอเลข
ผิดสักตัว แต่**ไม่ผ่านรวด** เจอ 7 ข้อ แก้ครบในคอมมิตที่สอง:

1. **D1 (สูงสุด)** คอมมิตแรกแดง — tripwire 5 ตัวข้างบน (control: `HEAD~1` เขียว) แก้แล้ว
2. **D2 (HIGH)** ประโยค "สองขาต่างกันแค่ MOBS id" **ผิด** — 8167 กับ 8171 ต่างกัน 4 คอลัมน์
   (`s_NAME` พายุ/ทะเลสงบ · `s_PROPERTIES` 8 ตัวเทียบ 1 · ความเร็ว 600 เทียบ 200) และ
   **ไฟล์ฉาก 304 เขียนประโยคเดียวกันผิดเหมือนกัน** — แก้ทั้งสองไฟล์ + ยกเป็นคำถามออกแบบถึง COO
3. **D3 (HIGH)** `unshippable_placements()` ของฉากนี้ลูปไม่เคยทำงาน (ไม่มีตัวตก) แต่ docstring
   ของเทสอ้างว่า "ลูปวิ่งครบ 59 แถวแล้วไม่เจอ" — adversary พิสูจน์ด้วย mutant `return ()`
   ที่ผ่าน 75 เทส/886 subtest · เพิ่มเทสที่ถอดเซ็ต 11 ออกแล้วบังคับให้ตัวรายงานพูด · รัน mutant
   ซ้ำเอง: **แดงแล้ว**
4. **D4** โทเคน `Mob_Set_57|Mob_Set_58` เป็นการสะกดของฉากพี่ ของจริงคือ `MobSet_57|MobSet_58`
   — แก้ + เทส re-derivation อ่านคอลัมน์ `set_names` จริงเป็นครั้งแรกในรีโปนี้
5. **D6** ชื่อ `MOBS.s_NAME` ของสามตัวไร้ชื่อเป็นจีนตัวเต็ม **cp874 เข้ารหัสไม่ได้เลย** → ไม่มีหมุด
   `NAME_CP874_HEX` ที่รับมันได้ — เขียนกำกับไว้ (คนถัดไปที่อยากตั้งชื่อให้มันจะเจอ `UnicodeEncodeError`)
6. **D7** สูตร re-verify ในแถว registry สั่ง `sha256sum` ของ `.tsv` ไปเทียบ `src_sha256` ซึ่งเป็น
   sha ของ `.npc` — รันแล้วไม่มีวันตรง · แก้ทั้งแถว 304 และ 305
7. **D9** docstring ของ `identity_for` อ่านตรงตัวแล้วแปลว่า "ไม่เคยคืน None" ทั้งที่คืน None ให้
   11 เซ็ตที่ CLINE 3008 นิยามแต่ฉากไม่วาง — หนึ่งในนั้นคือ **เซ็ต 55 `Pirate Flagship` rank 64**
   บอสตัวเดียวของ type นี้ ที่ผู้ออกแบบฉากไม่ได้วางไว้ที่จุดไหนเลย — เขียนกำกับ

ที่มันลองแล้วพังไม่ได้: mutant 6 แบบที่ `_self_check` จับได้หมด (หมุดไร้ชื่อค้าง · UNRESOLVED
ปลอม · second leg ว่าง · instance count สลับ · placement หาย · MOBS id สลับ)
ที่มันบอกว่ายัง**รอด**และรอบนี้ไม่ได้แก้: `SOURCE_SHA256` ไม่มีใครตรวจบนเส้นทางเซิร์ฟเวอร์
(ตัวที่ตรวจคือเทส bridge-only ที่ skip บนเครื่องเกต — ไฟล์เขียนบอกไว้เองอยู่แล้ว)

## 5. `TWO_SESSIONS_SAME_SCENE:`

ผ่าน — ไม่มี state ต่อ session เพิ่มเลยในรอบนี้: crosswalk เป็นข้อมูลโมดูลแช่แข็ง และ composer
เป็นฟังก์ชันบริสุทธิ์ของ (anchor, count) · สอง session ที่ยืนในฉาก 305 ได้ 59 ตัวชุดเดียวกันจาก
ตารางเดียวกัน ต่างกันแค่ลำดับ ซึ่งคือความหมายของ nearest-first

## 6. จดหมายรอบนี้

- **บริโภค**: `20260906_0347_COO-DECISION-a0315-option-a-confirmed-...-LANE-A.md`
  — ข้อ 1 ถอดป้าย `[สมมติ]` (ตรวจแล้ว: โค้ดบน main ไม่มีป้ายนี้ค้างอยู่แล้ว ตั้งแต่รอบ `dyi95m`) ·
  ข้อ 3 **เงื่อนไข AND ยืนยันด้วยการอ่านโค้ดจริง**: `ARM_THREE_ELIGIBLE_SCENE_IDS` เช็คก่อน
  แล้วยัง**คง**การหลบให้ `is_sanctioned_barred_scene` ไว้ครบ (ฉากที่อยู่ใน allowlist แต่ GM ถอนแถว
  = ปิด) และรอบนี้เติมคอมเมนต์อ้างใบ decree ให้ทุกแถวตามที่ข้อ 3 สั่ง ·
  ข้อ 4 `#877` ขึ้น main แล้ว (`566c10f`) · stub วางแล้ว
- **ส่ง** สองใบ:
  1. `20260906_0522_LANE-A-ASK-COO-which-mobs-columns-a-legs-are-interchangeable-gate-must-read.md`
     — คำถามออกแบบจาก D2 ตัดสินไปแล้วด้วย (ก) ติดป้าย `[สมมติของสาย LANE-A - รอ COO ยืนยัน]`
  2. `20260906_0522_LANE-A-TO-COO-skip-census-is-red-on-main-and-it-is-lane-q-pin-drift-not-a-lane.md`
     — ช่อง `skip_census` แดงบน main ด้วยหมุดของ LANE-Q ไม่ใช่ของสายไหนที่เปิด PR
- **ยังไม่บริโภค ยกไปรอบหน้า** (รอบนี้เวลาหมดไปกับ cast + 7 ข้อของ adversary):
  `0805_LANE-B-TO-LANE-A-scene14-responder` · `1152_COO-DECISION-world-registry` ·
  `1506_SYNC-NOTICE-pf_bridge-pr1319` · `2056_COO-DECISION-lane-q-needs-world-registry-interface`

## 7. ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

GM ที่พิมพ์ `/warp 305` เมื่อวานลงไปยืนในทะเลว่างเปล่า — ไม่มีอะไรบนจอเลยนอกจากน้ำ
วันนี้ลงไปเจอ **59 ตัว**: เรือพ่อค้า 9 ลำ เรือโจรสลัดเลเวล 120 สิบสามลำ เรือชื่อ Viking Princess /
Santa Maria / Skull Phantom / Utopia และ **เกาะห้าเกาะ** (Ice · Turtle · Dragon Turtle ·
Guawa · Snow) กับพายุล่องหนอีก 25 จุด · ประตูล็อกอินยังปิดสนิท ผู้เล่นธรรมดายังเข้าไม่ได้
(เข้าได้เมื่อ chief ต่อสายข้ามขอบแมพหนึ่งบรรทัด) และ**ยังไม่มีใครเห็นด้วยตา** — ใบเทสบนจอ
คือสิ่งที่จะเปลี่ยนประโยคนี้เป็นการวัด

## 8. รอบหน้าทำอะไร

1. วัดว่า `#889` ขึ้น `main` หรือยัง (`git merge-base --is-ancestor`)
2. **ใบ GT บนจอของทะเลทั้งสอง**: ฉาก 304 มีใบค้างอยู่แล้ว (`GT-268` รอ `ATTENDED:` + census 304)
   — เขียนใบของ 305 ให้เข้ารถบัส capture คันเดียวกัน (บล็อก `ATTENDED:` ≤5 บรรทัด: `/warp 305`
   แล้วดูว่ามีตัวบนจอกี่ตัว/เห็นเกาะไหม) ผ่าน pf-queue-author — **รอบนี้ทำไม่ทันในงบ 75 นาที**
3. บริโภคจดหมายสี่ใบที่ยกมาในข้อ 6
4. ถ้า COO ตอบใบ `0522` ด้วย (ข) หรือ (ค): แก้ `MULTI_SET_GATE` ให้เทียบคอลัมน์ที่ตกลงกัน

## 9. กำหนดเวลา

เริ่ม 04:21 · เพดาน 75 นาที = 05:36 · เวลาหลักหมดไปกับการอ่านคู่ไฟล์ของฉาก 304 ให้เข้าใจกลไก
ก่อนเขียน (854 + 430 บรรทัด) · ชุดเต็มสองรอบ (8 นาทีต่อรอบ) · ซ้อมเกตรูปจริงอีก 7 นาที ·
และ 7 ข้อของ adversary ที่คืนมาก่อนปลดล็อก

SCOREBOARD: COMING | GM ที่ `/warp 305` (Pale Silver Sea) เห็นเรือ เกาะ และพายุรวม 59 ตัวแทนทะเลว่างเปล่า — ทะเลปลายทางทั้งสองของการข้ามขอบแมพฉาก 126 มีประชากรครบแล้วทั้งคู่ | PR: pirate-force-server#889 (ไม่ draft · marker ยืนยันด้วย GET · 3 คอมมิต) · claim pf_bridge#1425 · ชุดเต็ม 11799 passed / 0 failed · preflight PASS · ซ้อมเกต pytest_subset exit 0 · ADVERSARY: returned in-round, 7 findings addressed
