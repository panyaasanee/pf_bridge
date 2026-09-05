# LANE-A round `yob0a2` — the Dark Fog Sea gets its cast, and the arrival path is allowed to say so

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** GM ที่พิมพ์ `/warp 304` แล้วขยับตัว
เมื่อวานยืนอยู่ในทะเลว่างเปล่า **วันนี้ทะเลนั้นมีของอยู่ 50 ตัว** — เรือสินค้า 9 ลำ
เรือโจรสลัดเลเวล 120 อีก 9 ลำ เรือชื่อ Ulysses / Bismarck / Yamato / Black beard /
Red beard / Smuggling Ship เกาะสองเกาะ (Mad Sand Island, Pirate Lair) และพายุ
Tornado อีกสิบสี่ลูก · เฟรมจริง 8,684 ไบต์ ไม่มีแฟล็ก ไม่ต้องเปิดอะไร
(ยังไม่มีใครเห็นบนจอ — ใบเทส attended ของรอบนี้คือสิ่งที่จะพิสูจน์ชั้นที่สอง)

## NOW.md — รอบนี้ขยับข้อไหน

อ่าน `pf_bridge/NOW.md` เป็นไฟล์แรก (ตรวจล่าสุด 18:47 โดย COO) ไม่มีบรรทัด
"งานด่วน" ที่จ่าหน้า LANE-A ค้างอยู่ในรอบนี้: `/warp 126` วาปสด (`#838`) ปิดแล้ว
และข้ามขอบทะเล 304/305 (`1748`) จ่ายไปแล้วรอบก่อน (`#843` **merge แล้ว** — ดูข้อ A)

รอบนี้ขยับ **บันไดไมล์สโตน M2 "ออกจากเมืองได้"** ในครึ่งที่ไม่ต้องรอใคร: ปลายทางของ
การข้ามขอบทะเลเลิกเป็นห้องว่าง · และขยับ **`## งานด่วนตอนนี้` ข้อ GM-A `/warp <เลขแมพ>`**
โดยทำให้ฉากที่ `/warp` สดไปถึงแล้วมีอะไรให้เห็นจริง

**ที่ไม่ขยับ และเพราะอะไร**: `TWO_SESSIONS_SAME_SCENE` / world registry
(`COO 1152` ข้อ 2(2)) — โมดูล `world_scene_registry.py` อยู่บน main ตั้งแต่รอบ
`tz2rgc` แต่ทั้งสองครึ่งที่เหลือ**ไม่ใช่ของสายนี้**: (ก) seed ตอนล็อกอินอยู่ใน
`runtime.py` = CORE-REQUEST ค้างที่ chief (`WORLD_REGISTRY_SEED_WIRING`) และ
(ข) ผู้เขียน combat state คือ LANE-B ผ่าน API ของสายนี้ · วัดที่ HEAD รอบนี้:
`note_balance`/`seed_the_session_ledger` **ยังไม่มีผู้เรียกใน production เลยแม้แต่ราย
เดียว** ⇒ สายนี้ไม่ยืนรอ (กฎ "เขียนคำถาม แล้วเดินต่อ") ไปหยิบงานที่ผู้เล่นเห็นได้จริง
ในรอบเดียวแทน

## Round-start checks

- **ล็อกรอบ**: `pf_bridge` ไม่มี `[LANE-A]` เปิดค้าง · `pirate-force-server` มี `#843`
  ([LANE-A] รอบ `n4vqxc`) เปิดอยู่ตอนต้นรอบ แต่รอบนั้น**จบแล้ว** (claim merge แล้ว
  ไฟล์รอบ `A_20260905_1754_n4vqxc_*.md` อยู่บน main) ⇒ ตามหัวข้อจบรอบ PR เซิร์ฟเวอร์
  ที่รอเกตไม่ใช่ล็อกที่มีชีวิต · เปิด claim ของตัวเอง `pf_bridge#1365` แล้ว list ซ้ำ:
  ไม่มีใบ `[LANE-A]` ที่เก่ากว่าและยังมีชีวิต
- **ชะตา PR รอบก่อน (ADDENDUM A)**: `pirate-force-server#843` **merged=true**
  (`58209ef` บน main) · `pf_bridge` claim ของรอบ `n4vqxc` merge แล้วเช่นกัน
  ⇒ ไม่มีอะไรหายจาก main ไม่ต้อง cherry-pick
- **กล่องจดหมาย (ADDENDUM B)**: บริโภค `20260905_1812` (chief R356 → LANE-A,
  `COMPANION_BYTES_PER_PUNCH: 390 B`) — stub เขียนแล้ว ต้นฉบับสำเนาเข้า `consumed/`
  ไม่มีใบอื่นที่ `ADDRESSEE: LANE-A` ค้าง · ใบ RE/GT ที่สายนี้เปิดไว้ยังไม่มีผลใหม่กลับมา
  · `SYNC-ALARM 1856` เรียกสองใบที่ไม่ใช่ของสายนี้ (LANE-GM `0558`, LANE-DB `0612`)
- `KNOWN_RED_MAIN:` ไม่มี (NOW.md 17:55 บันทึกว่า `test_combat_pose` เขียวแล้วบน main)
- `BYTECODE_PURGED:` ทั้งรอบรันด้วย `PYTHONDONTWRITEBYTECODE=1` + `python3 -B`
  ไม่มีการคืนค่ามิวแทนต์นอก process ของเทสเอง

## สิ่งที่รอบนี้ทำ

### 1. ทำไมเป็นฉาก 304 และทำไมตอนนี้

รอบก่อน (`n4vqxc`) ปักจุดมาถึงของ 304/305 และเขียนไว้เองในหัวข้อ "What is NOT proven"
ว่า **"No cast"** — และ pf-adversary ของรอบนั้นวัดได้ว่าการปักหมุดทำให้
`gm.warp_executor.warp_no_coords_live_target(304)` คืนค่า ⇒ `/warp 304` **วาปสดได้
ตั้งแต่ตอนนั้น** เข้าไปยืนในฉากที่ไม่มีอะไรเลย นี่คือช่องว่างที่ปิดได้ในรอบเดียว
ด้วยของที่มีอยู่แล้วในสะพาน ไม่ต้องรอ RE ไม่ต้องรอ chief ไม่ต้องรอเครื่องเจ้าของ

### 2. `world_bg3007_identity.py` — ตารางไขว้ของ CLINE 3007

join เดียวกับที่ `world_bg3001_identity` (ฉาก 126) ใช้ ไล่จากตารางที่คอมมิตไว้จริง
ด้วยสคริปต์ใช้แล้วทิ้ง ไม่ใช่พิมพ์มือ:

```
CLINE[n_CLINE_TYPE==3007][n_CREATURE_TYPE==<Mob-Set>] -> n_LEADER_BK1
  -> MOBS -> MOBS_TIP (ชื่อ/ฉายา) + STANDARD_MOB[n_LEVEL_MIN].n_HPMAX
```

- **41 Mob-Set ที่ placement ของฉากใช้ → resolve 37 · placement 66 → ส่งได้ 50**
- **16 placement ที่ตกทั้งหมดมีเหตุผลเดียว และเป็นรูปแบบใหม่ของสายนี้**: set
  55/56/57/58 ชี้ leader 8176/8178/8177/8179 ซึ่ง `TEXTDATA_TH__MOBS_TIP` **มีชื่อให้**
  (Ulysses, Pirate Follow Ship, Yamato, Navy Follow Ship) แต่ `CONSTDATA_TH__MOBS`
  **ไม่มีแถวเลย** — ป้ายชื่อไม่ใช่ร่าง ไม่มี `s_OUTFIT` ไม่มีเลเวล ไม่มี HP จะส่ง
  ทุกฉากก่อนหน้านี้ตกด้วย leader 0 หรือ outfit ว่าง อันนี้ไม่ใช่ทั้งสองอย่าง
  🔴 กับดักที่เขียนลงใบเทสด้วย: ชื่อ "Ulysses" และ "Yamato" **โผล่ทั้งสองฝั่ง** —
  set 1/set 4 ส่งจริง ส่วน set 55/57 ตก ผู้เทสต้องแยกด้วย `placement=` ไม่ใช่ด้วยชื่อ
- **`53|54` หกแถว**: ส่ง leg แรกตาม `COO-DECISION 20260902_2146` shape 2 และ
  **ตรวจ ไม่ใช่สมมติ** — `multi_set_placement_refusals()` เทียบสองขาทีละคอลัมน์
  (ทั้งคู่ `INVISIBLE` ไม่มีชื่อ ไม่มีฉายา lv110 rank 0 hp 260787 usage 7 ต่างกันแค่
  เลข MOBS 8167/8171) และทั้งสองขา**ไม่มีแถว MOBS_TIP** = ไม่มีป้ายชื่อให้ผู้เล่นแยก
- ชื่อทุกตัวในฉากนี้เป็น ASCII ⇒ `NAME_CP874_HEX` ว่าง (กลไก cp874 คงไว้ ไม่ลบ:
  มันคือด่านสมาชิกของ `2146` shape 1 และเทสยิงตรงเข้าฟังก์ชัน)
- ตัวเลขอื่นที่วัดเอง: extra spawn triple 656 จุดใน 18 จาก 66 แถว (ไม่ส่งสักจุด) ·
  `n_SAVE=0` (ไม่มีเฟรม faction เหมือน 126) · `n_SCENE_LV=30` (126 เป็น 0) ·
  CLINE 3007 ทั้ง 58 แถวไม่มี `n_CREW` เลย · มีแถวเดียวที่มี BK2/BK3 คือ 61410
  (set 11) ซึ่ง crosswalk นี้ดรอปตามกติกา `n_LEADER_BK1` เท่านั้น

### 3. `world_population_bg3007.py` — ครึ่ง census

รูปเดียวกับพี่น้องทุกฉาก serializer แช่แข็งตัวเดิม (`world_census_level.leveled_npc_attr`
/ `make_remote_movement_attr` / `make_remote_actor_entry` / `make_runtime_remote_actors`)
ปฏิเสธทุกฉากที่ไม่ใช่ 304 · เรียงใกล้ก่อน · HP มาจากตารางจริง ส่ง current == max

### 4. แขนรับที่สาม (`scene_arrival_was_decreed_and_is_gm_reachable`)

ปัญหา: ด่านรับของ hook มีสองแขน (ทะเบียน `login_entry_allowed` / เพรดิเคต GM ที่รับ
เฉพาะฉากที่ chief sanction) และ**ไม่มีแขนไหนรับฉาก 304** ⇒ cast ที่สร้างจะเป็น
"ลงทะเบียนแล้วไม่เคยยิง" = รอบกระดาษ

แขนที่สามรับฉากที่ **(i)** แถวทะเบียนมี `decreed_arrival` ที่ผ่านการตรวจของ loader
(ใส่ได้เฉพาะ PANYA-DECISION / COO-DECISION) **และ (ii)** `warp_no_coords_live_target`
คืนค่า (เกตของสาย GM เอง ไม่ได้เขียนใหม่)

- **ขอบเขตวัดแล้วทั้งทะเบียน 19 แถว = 126, 304, 305 เท่านั้น** และเทสไล่ทุกแถว
  ไม่ใช่ assert สามตัว · 16 ฉากที่ `/warp` สดถึง มี 13 ฉากที่ `login_entry_allowed`
  เป็น true อยู่แล้ว (แขนแรกรับไปแล้ว) ⇒ แขน "กว้าง" แบบ /warp อย่างเดียว
  ไม่ได้เพิ่มอะไรวันนี้ แต่จะกลายเป็นกฎยืนที่รอบก่อน ๆ ตั้งใจเลี่ยง จึงไม่เอา
- **ไม่ใช่ประตู**: `login_entry_allowed` ของทั้งสามฉากไม่ถูกแตะ · เทสยิง
  `resolve_entry(..., via_login=True)` จริงและได้ `REFUSED_NOT_ALLOWED_AT_LOGIN`
- **ติดป้าย `[ASSUMPTION OF LANE A - AWAITING COO CONFIRMATION]` ในตัวฟังก์ชัน**
  พร้อมจดหมายถึง COO (`1946`) — ถ้า COO ตอบว่าไม่ ลบฟังก์ชันเดียวกับบรรทัด `or`
  กลับเป็นพฤติกรรมวันนี้เป๊ะ
- **ผลข้างเคียงที่ประกาศเอง**: ฉาก 126 เดิมรับด้วยแขน GM อย่างเดียว ตอนนี้แขนที่สาม
  รับด้วย ⇒ เทสของรอบ `4uztfj` ที่ปักว่า "ปิดแขน GM แล้ว 126 ดับ" ถูกแก้ให้พูดความจริง
  ใหม่ (ต้องปิดทั้งสองแขน GM) ไม่ใช่เลี่ยง
- **"GM-only" หมายถึงอะไร**: เพรดิเคตถามถึง**ฉาก** ไม่ใช่บัญชี วันนี้ทางเดียวที่ไปถึง
  ฉากคือ `/warp` ของ GM · วันที่ chief เสียบบรรทัดข้ามขอบทะเล ผู้เล่นธรรมดาที่แล่นข้าม
  ขอบฉาก 126 จะได้ cast ชุดเดียวกันนี้ — ตั้งใจ และเขียนไว้ในเอกสารของฟังก์ชันแล้ว

### 5. การลงทะเบียนสองตาราง + ตารางที่สาม

`world_scene_travel.CENSUS_SOURCES` (`bg3007_roster`) ·
`lane_hooks/lane_a_scene_census._CONSOLE_LINES_OF` · และ
`world_population_handoff.ROSTER_COMPOSERS` (ไม่มีตัวนี้ seam จะตอบ CLEAR แล้ว
composer จะ decline เงียบ ๆ) · เพิ่มค่าคงที่ `DARK_FOG_SEA_SCENE_ID = 304`
· แก้ข้อความ `status` ของแถว 304 ในทะเบียนให้ตรงกับความจริงใหม่

## pf-adversary

<!-- ADVERSARY -->

## เทส

`BYTECODE_PURGED: PYTHONDONTWRITEBYTECODE=1 + python3 -B ทั้งรอบ`
(ไม่ได้ลบ `__pycache__` — ไม่เคยเขียน)

ระหว่างทาง (เฉพาะไฟล์ที่รอบนี้แตะ):
`tests/test_world_bg3007_identity.py` (ใหม่) ·
`tests/test_world_bg3007_identity_rederived.py` (ใหม่ · ไล่ไขว้กับตารางของสะพานจริง
ทีละฟิลด์ — **skip บนเกต Windows** เพราะที่นั่นไม่มี `pf_bridge` วางข้าง ๆ เขียนไว้
ในหัวไฟล์ว่าเป็นรูโหว่ที่รู้ตัว) · `tests/test_world_population_bg3007.py` (ใหม่ ·
บน serializer แช่แข็งจริง) · `tests/test_lane_a_scene_census_bg3007.py` (ใหม่ ·
แขนที่สามทั้งชุด) · `tests/test_lane_a_scene_census.py` ·
`tests/test_gm_warp_chain_census_shipped.py` · `tests/test_world_scene_travel.py` ·
`tests/test_world_population_handoff.py` · `tests/test_field_mobs.py` ·
`tests/test_gm_warp_chain_preflight.py` · `tests/test_world_scene_folder.py` ·
`tests/test_world_m2_sea_scene_cast.py` · `tests/test_world_scene_entry.py`
แล้วกวาดด้วย `-k "world or lane_a or warp or census or scene"`

🔴 เทสที่เป็นหลักฐานชั้น wire ของประโยคหัวเรื่อง:
`tests/test_gm_warp_chain_census_shipped.py::test_every_map_a_bare_warp_can_reach_ships_one_on_arrival`
บูตไร้แฟล็กจริง `/warp 304` แล้ว poll — ตอนนี้**บังคับ**ให้มี census 50 ตัว
(`SCENES_WITH_NO_CENSUS_COMPOSER_YET` เหลือ `(305,)`)

ชุดเต็ม: <!-- FULLSUITE -->

## จดหมายรอบนี้

- `20260905_1946_LANE-A-ASK-COO-third-admission-arm-*.md` — ขอ COO เคาะแขนที่สาม
  (ตัดสินไปแล้ว เดินต่อแล้ว ระบุสิ่งที่ต้องย้อนถ้าผิด)
- `20260905_1950_LANE-A-TO-CHIEF-scene-304-has-a-cast-*.md` — ปลายทางของ
  บรรทัดที่ chief จะเสียบ (ใบ `1834`) มีของแล้ว + ขอเลข GT
- `20260905_1953_LANE-A-GT-TICKET-BODY-scene-304-cast-first-eyes.md` — เนื้อใบเทส attended
- บริโภคแล้ว: `20260905_1812` (stub + สำเนาใน `consumed/`)

## สิ่งที่ยังไม่พิสูจน์

- **ไม่มีใครเห็นฉาก 304 บนจอ** ทั้งโปรเจกต์ · 20 จาก 50 ตัวเป็นร่าง `INVISIBLE`
  และอีก 2 เป็น `MAP_ISLAND_01` ซึ่งไม่เคยมีใครดูว่าไคลเอนต์วาดยังไง ⇒ "เห็นน้อยกว่า
  50 ตัวบนจอ" **ไม่ใช่** ความล้มเหลวโดยอัตโนมัติ ใบเทสเขียนวิธีแยกไว้
- **จุดมาถึง (6918, -792, 90) ยังเป็น `decreed_provisional`** — เจ้าของยังไม่เคาะ
  ผู้เทสต้อง *บันทึก* ว่าเรือโผล่ตรงไหนจริง ไม่ใช่ตัดสินว่าถูกหรือผิด
- **ฉาก 305 (Bg3008) ยังไม่มี cast** — 59 placement, join เดียวกันให้ 55/59
  (วัดแล้วรอบนี้ ยังไม่สร้าง) = งานจริงของรอบถัดไป
- **ทางของผู้เล่นธรรมดายังไม่มี** — ข้ามขอบทะเลยังรอบรรทัดเดียวของ chief (`1834`)
- **ประตูล็อกอิน 304 ยังปิด · ไม่มี ground bounds · ไม่มี hostility ของฉากนี้**
  (`mob_census_hostility` พิมพ์ `roster=0 unbacked=none` ตามจริง)
- **`SOURCE_SHA256` ถูกแฮชจริงเฉพาะบนเครื่องที่มี `pf_bridge` วางข้าง ๆ** บนเกต
  Windows เทสนั้น skip — รูโหว่เดิมของทั้ง 12 ตารางไขว้ ไม่ได้ปิดในรอบนี้

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว — รอบนี้ไม่เพิ่มสถานะโลกต่อฉากที่แก้ไขได้เลย
(ไม่มี roster ที่เขียนได้ ไม่มีมอน ไม่มีของบนพื้น) มีแต่ตารางนิ่งกับฟังก์ชันอ่านอย่างเดียว
สอง session ที่ยืนในฉาก 304 พร้อมกันได้ census ชุดเดียวกันจากตารางเดียวกัน

## งานสำรอง 3 ข้อ (ถือไว้ทุกรอบตามคำสั่ง Panya 0904_14:4x)

1. **cast ของฉาก 305 (Bg3008)** — คู่แฝดของรอบนี้ 55/59 placement resolve แล้ว
2. **`world_scene_registry` ครึ่งที่สายนี้ทำเองได้**: อ่าน remembered vitals เข้ามา
   ประกอบ census ตอน arrival (ครึ่ง read ผ่าน hook ของสายนี้เอง ไม่ต้องรอ runtime.py)
   — ทำได้แต่ยังไม่มีคนเขียน ⇒ ตัวเลขจะเป็นศูนย์จนกว่า LANE-B หรือ chief จะขยับ
3. **ฉาก 127/128** (Bermuda / Bg3002) ocean panel อีกสองฉากที่ `world_m2_sea_scene_cast`
   นับไว้แล้ว ยังไม่มีทั้งจุดมาถึงและ cast

## Status

<!-- STATUS -->
