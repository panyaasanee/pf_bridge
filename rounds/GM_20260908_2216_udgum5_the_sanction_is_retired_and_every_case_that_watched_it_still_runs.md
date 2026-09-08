# LANE-GM รอบ `udgum5` — แถว 126 ถูกถอน และทุกเคสที่เฝ้ามันอยู่ยังวิ่งครบ

รหัสรอบ: `GM_20260908_2216_udgum5` · เริ่ม 2026-09-08T22:16+07:00 · ล็อก `pf_bridge#1965`
ป้ายเวลาทั้งไฟล์มาจาก `TZ=Asia/Bangkok date` · `_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุด `22:02` ห่างจากเวลาเริ่มรอบ **14 นาที** (ต่ำกว่า 60 ⇒ สะพานไม่ค้าง)

## รอบนี้ขยับ NOW/M ข้อไหน
`## งานด่วนตอนนี้` → **LANE-GM: "งานแรก = ถอนแถว 126 + คืน tripwire"** — ทำจนจบในรอบเดียว
กระทบ **ประตู M (`1825`)** ทางอ้อมและตรงจุดที่ NOW เขียนไว้เอง: บล็อก (1) ของโทเคน `#1181` คือ "GM ถอนแถว 126 เงื่อนไขครบแล้ว" — บล็อกนั้นถูกปลดในรอบนี้ ⇒ LANE-A rebase `#1181` ได้ทันทีที่ PR นี้ลง main (แจ้งเขาแล้ว)

## ลำดับความจริงที่เดินตาม (COMMON ข้อ 1-5)
1. `NOW.md` (fetch สด `b77ad57`) → LANE-GM งานแรก = ถอนแถว 126 · 🔴 ห้ามรอ ancestor-of-main
2. กล่องจดหมาย: `2141_COO-DECISION-retire-scene-126-now` · `2141_COO-BLOCKER-SWEEP-3` · `2055_COO-DECISION-bound-to-the-token` · `2330_LANE-A-TO-LANE-GM` — **บริโภคครบทั้งสี่ใบ** (stub `.CONSUMED.txt` + สำเนาไป `consumed/`)
3. ไฟล์รอบก่อน (`2042_ve2zs4`) ตั้ง "ถอนแถว 126" ไว้เป็นข้อ 2 ของรอบหน้า · COO ย้ายขึ้นเป็นข้อ 1 ⇒ ทำข้อนี้ก่อน

## ล็อกรอบ
list `[LANE-GM] round *: claim` ที่ open = **ไม่มี** ⇒ ตัดกิ่งจาก `origin/main` เปิด `pf_bridge#1965` (ไม่ draft, body ไม่มีสตริง marker ตลอดรอบ) · ไม่มี takeover ไม่มี yield

## สิ่งที่ทำ (หนึ่งชิ้น จบในรอบเดียว)
### ก. ถอนแถว
`SANCTIONED_BARRED_SCENES` **ว่าง** · โทเคนของ COO ทั้งสอง: `retirable_sanctioned_scene_ids()` = `()` · ไม่เหลือแถว sanction ของ 126 ในไฟล์
เขียนบันทึกการถอนไว้ที่แผนที่เอง: ใบที่สั่ง (`2141` DECISION + BLOCKER-SWEEP ข้อ 5) · เงื่อนไขที่ผูกไว้ (`2055` = `retirable_...() != ()` ซึ่ง LANE-A วัดได้ `(126,)` บน `#1181`) · **ต้นทุนของหน้าต่าง วัดบน `origin/main` ก่อนลบ** · และวิธีเพิ่มแถวใหม่ในอนาคต

### ข. ต้นทุนของหน้าต่าง — วัดก่อนลบ ไม่ได้เดา (`origin/main` = `c5820e8`)
    retirable_sanctioned_scene_ids()  -> ()            <- ยังไม่ (126,) บน main; LANE-A วัดบนกิ่งเขา
    login_entry_is_pinned(126)        -> False
    sanctioned_barred_blocker(126)    -> login_path_bars_it_needs_core_request_gm_038
    single_use_stageable_scene_ids()  -> (..., 126, ...)   <- 126 อยู่ได้เพราะแถว sanction เท่านั้น
⇒ ถอนแล้ว 126 หลุด single-use map: **(ก)** `warp_relog_stage` ตอบ `reason=scene_not_sanctioned` (GM วาร์ป 126 แล้ว relog กลับแถวเดิม — `PANYA 1430` ปิดชั่วคราว) **(ข)** census ฉาก 126 ผ่าน arm 2 ของ LANE-A ดับ
**ไม่กระทบ**: วาร์ปสด (`PANYA 1329`) อ่าน decreed arrival ไม่ได้อ่านแผนที่นี้ · ประตูล็อกอินผู้เล่นทั่วไป · `runtime.py` (`gm_sanctioned_bypass` กลายเป็น False ⇒ `via_login=True` = ปฏิเสธตามปกติ fail-closed)
หน้าต่างปิดเองเมื่อแถวล็อกอินของ LANE-A ลง main (ตอนนั้น arm 1 คลุม 126 ไม่ต้องมี sanction) — ไม่ต้องมีใครกลับมาแก้

### ค. 33 เคส 6 ไฟล์ พลิกเนื้อใน ไม่ skip ไม่ xfail ไม่ลบ (`2050`)
🔴 **"25 เคส/5 ไฟล์" ที่ COO นับ ไม่ใช่เคสแดง — มันคือ skip ที่กำลังจะเกิด** และนี่คือข้อค้นพบของรอบนี้:
`tests/test_gm_login_scene_sanctioned_admission.py` มี `unittest.skipIf(SANCTIONED is None, ...)` ระดับคลาส 6 จุด ⇒ ถอนแถวปุ๊บ ไฟล์ทั้งไฟล์ = **25 skipped 0 failed** เกตไม่แดง ชุดเต็มเขียว และ 25 เคสที่พินการขยาย single-use **หยุดวิ่งบนทรีเดียวกับที่การขยายนั้นเปลี่ยนสถานะ**
แทนที่ด้วย class decorator `with_a_sanctioned_scene` ที่ **ติดตั้งแถวสังเคราะห์หนึ่งแถว** ⇒ 25 เคสวิ่งครบและเขียว · `skipIf` เดิมถูก **ขีดฆ่าไว้ในไฟล์พร้อมเหตุผลว่าทำไมมันผิด** ไม่ได้ลบ
หลักการที่ใช้ทุกไฟล์ เขียนไว้ครั้งเดียวใน `_install_a_sanction`: **แผนที่คือข้อมูล กลไกคือโค้ด** — เคสที่พิน "สายนี้ส่งอะไร" อ่านแผนที่จริง (มีใบเดียว) · เคสที่ทดสอบกลไกติดตั้งแถวของตัวเอง
- `test_gm_login_scene_sanctioned_barred.py` (16 เคส): แผนที่ = `{}` แบบเท่ากันเป๊ะ (ไม่ลดเป็น `assertNotIn` ⇒ ใส่แถวคืนโดยไม่มีใบ = แดง) · `test_the_sanction_is_still_load_bearing_on_this_tree` → **พลิกเป็น** `test_what_the_retirement_cost_is_measured_not_argued` (ชื่อเดิมขีดฆ่าไว้)
- `test_gm_login_scene_sanctioned_admission.py` (25 เคส): ตามข้อบน
- `test_gm_login_scene_sanctioned_bypass_wiring.py` (1) · `test_gm_warp_relog_stage.py` (5) · `test_lane_a_scene_census.py` (7+1 subtest) · `test_lane_a_scene_census_bg3007.py` (2)

### ง. ทริปไวร์ที่ COO สั่งให้ "คืน" — คืนแบบที่ **ยิงได้จริง**
`test_every_sanctioned_scene_is_one_the_predicate_refuses_today` วนบนแผนที่ว่าง = ลูปไม่ทำงาน = เขียวที่แดงไม่เป็น (ข้อบกพร่องที่คลาสนี้ตั้งขึ้นมากันเอง)
เพิ่มครึ่งที่สองในเคสเดิม: ติดตั้ง sanction ให้ฉากที่ predicate รับอยู่แล้ว แล้วพินว่า `retirable_sanctioned_scene_ids()` ต้องชี้ฉากนั้น ⇒ ลบกฎ retirement ออกจาก `sanction_is_retirable` = แดงทันที
เจอและปิดเคสไร้ฟันอีกใบระหว่างทาง: `test_the_pinning_holds_when_the_fix_is_reverted` — สตับคืน `scene_not_sanctioned` ซึ่งเป็นสิ่งที่เกิดอยู่แล้วบนแผนที่ว่าง ⇒ เคสนี้แดงไม่เป็นอีกต่อไป · แก้โดยพิสูจน์ก่อนว่าเส้นทางที่ไม่ถูกสตับ **stage จริง** แล้วค่อยสตับ

### จ. ประโยคที่เป็นเท็จหลังการถอน — ขีดฆ่าพร้อมเหตุผล ไม่ได้ลบ
`login_scene_admission.py` (docstring ของ `sanction_is_retirable` ที่เขียนว่าแถวยัง load-bearing · บรรทัด `BLOCKER_NO_REGISTRY_ROW` ที่อ้าง "the only id in the map") · `warp_relog_stage.py` (module docstring "which today holds exactly one id" · คอมเมนต์ที่เขียนว่าทริกเกอร์ยังไม่ยิง)
**ไม่แตะ `src/` ของ LANE-A**: `world_bg3001_identity.py:17` และ `world_scene_travel.py:387` ยังเขียนว่าแผนที่ตั้งชื่อ 126 (เท็จหลัง PR นี้) — ส่งเป็น **การวัด** ให้เจ้าของในใบ `2228` ตามใบ `1742` ข้อ 4 (ห้ามส่งบิลข้ามสาย)

## เขตที่แตะ
`gm/login_scene_admission.py` · `gm/warp_relog_stage.py` · `tests/test_gm_*` (4 ไฟล์) · `tests/test_lane_a_scene_census*.py` (2 ไฟล์ **ตามคำสั่งตรงของ COO ใบ `2141`: "25 เคส/5 ไฟล์"** — แตะเฉพาะเทส ไม่แตะ `src/` ของเขา)
**ไม่แตะ** `runtime.py` · `app.py` · `v141` · canonical DB · `world_*.json` · `combat_*.json` · `migrations/`

## `TWO_SESSIONS_SAME_SCENE:` (บังคับทุก PR)
**ไม่เกี่ยว และตรวจได้**: รอบนี้ลบ **หนึ่งแถวในตารางค่าคงที่ระดับโมดูล** ไม่มีสถานะต่อเซสชัน ไม่มีการเขียน registry ของ LANE-A ไม่มีเฟรมออกไปหาไคลเอนต์ ไม่มี mob/HP/ศพ/ของตกพื้น
สองเซสชันในฉากเดียวกันอ่านตารางเดียวกันทั้งก่อนและหลัง — สิ่งที่เปลี่ยนคือ **คำตอบเดียวกันสำหรับทุกเซสชัน** (126 ไม่อยู่ในแผนที่ single-use อีกต่อไป) ไม่ใช่คำตอบที่ต่างกันต่อคน
ข้อจำกัด multiplayer ที่ยังอยู่คือของเดิม (`GM-058` · `session.token` ระดับโปรเซส) ไม่ใช่ของรอบนี้

## หลักฐานสองชั้น (แยกกัน ไม่อ้างชั้นเดียวกันสองรอบ)
- **client-observable**: คอนโซลของผู้ปฏิบัติหลัง `/warp 126` — `GM_WARP_SCENE_PERSIST_FAILED scene=126 reason=login_would_refuse` ตามด้วย `GM_WARP_RELOG_ENTRY_NOT_STAGED scene=126 reason=scene_not_sanctioned` (เดิมเป็น `..._STAGED scene=126 previous=none single_use=1`) — พินใน `test_warp_126_still_sends_the_frame_and_leaves_the_row_with_no_relog` ผ่านเส้นทาง `/warp` จริง (store จริง lifecycle จริง session จริง)
- **wire/DB**: แถวตัวละครใน SQLite **ไม่ขยับ** (`scene_id` = 1 ทั้งก่อนและหลัง) และ **ไม่มีไฟล์ entry ถูกเขียน** (`config/gm_login_scene.json` ไม่มีอยู่) — เป็นการอ่านฐานและระบบไฟล์ ไม่ใช่การอ่านคอนโซล

## nonclaims (สิ่งที่รอบนี้ **ไม่** พิสูจน์)
- ไม่ได้พิสูจน์ว่าฉาก 126 เข้าได้ · ไม่ได้เปิดประตูล็อกอินใด ๆ · ไม่ได้แตะ `login_entry_allowed`
- **ไม่ได้ใช้ GM ข้ามขั้นเพื่ออ้างว่าฟีเจอร์ผ่าน** — รอบนี้ *ถอน* ความสามารถ GM หนึ่งอย่างชั่วคราว ไม่ได้ใช้มันอ้างอะไร
- ไม่ได้พิสูจน์ว่า `#1181` ของ LANE-A จะเขียว — พิสูจน์เฉพาะว่าสองเคสในไฟล์ของสายนี้ที่แดงบนกิ่งเขา ไม่แดงอีกแล้ว
- ไม่ได้วัดบนเครื่องจริง/ไคลเอนต์จริง ทั้งหมดเป็น headless บน cloud clone
- "ยังไม่อยู่บน main" — PR เปิดแล้ว รอเกต ยืนยัน ancestor ในรอบถัดไป

## เทส
ไฟล์ที่แตะ ทีละไฟล์: `sanctioned_barred` 36 · `sanctioned_admission` 25 (เดิม 25 skipped) · `bypass_wiring` 6 · `warp_relog_stage` 20 · `lane_a_scene_census` 69 · `lane_a_scene_census_bg3007` 21 — **เขียวทั้งหมด**
`python3 tools_bridge/pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS** (รวมบรรทัด **no new skips** ซึ่งเป็นหัวใจของข้อ ค.)
ชุดเต็ม `pytest tests/` รันครั้งเดียวหลัง `git merge origin/main` เป็นขั้นสุดท้าย — ผลอยู่ในหัวข้อสถานะท้ายไฟล์

## รอบหน้าทำอะไร
1. **จ่าย adversary D6-D10 ที่ค้างจากรอบ `ve2zs4`** (D7/D10 แตะบรรทัดที่เจ้าของ grep จึงมาก่อน D8/D9) + ผล adversary ของรอบนี้ถ้าคืนหลังปลดล็อก
2. **ยืนยัน `#1176` และ PR ของรอบนี้เป็น ancestor ของ main** ด้วย `git merge-base --is-ancestor` แล้วปลด hold บูต `/skill all` (NOW ข้อ "บูต `/skill all` HELD จน `#1176` ลง main")
3. **เทสสองคอนเนกชันบน listener เดียว** (`CORE-REQUEST-GM-058` · ใบ chief `20260908_1843`) — เขียนเป็นเทสที่วัดสภาพปัจจุบันตามจริง ชื่อบอกว่ากำลังวัดรู
4. ถ้า LANE-A rebase แล้วแถวล็อกอิน 126 ลง main: **ลบ `_install_a_sanction` ที่ไม่จำเป็นแล้วออกจากเคสที่ arm 1 คลุมแทน** และปิดหัวข้อ "หน้าต่าง" ในโค้ด

## สถานะตอนจบรอบ (เขียนตามจริง ห้ามเขียนว่า landed)
