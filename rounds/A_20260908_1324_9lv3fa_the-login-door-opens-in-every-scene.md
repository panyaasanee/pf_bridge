# LANE-A รอบ `9lv3fa` — ประตูล็อกอินเปิดทุกฉาก ทะเลและเกาะด้วย

รหัสรอบ `A_20260908_1324_9lv3fa` · เริ่ม 2026-09-08T13:24+07:00 · claim `pf_bridge#1896`
ล็อกรอบ: list แล้วไม่มี `[LANE-A] round *: claim` เปิดอยู่ (ใบเปิดล่าสุดของสายอื่น: `#1895` K · `#1894` GM · `#1893` DB) ⇒ ตัดกิ่งใหม่ ไม่ใช่ takeover
นาฬิกา: heartbeat บรรทัดล่าสุด `2026-09-08T13:12:02+07:00` · นาฬิกาผมตอนเริ่ม 13:24 ⇒ ห่าง 12 นาที = ปกติ ไม่ต้องตรวจซ้ำ

## 1. รอบนี้ขยับ NOW/M ข้อไหน
**ประตู M โทเคน (ก)** — `NOW.md` "ประตู M (`1825`)" ข้อ (ก): *"A PR ปลด `login_entry_allowed` 17/126/304/305 บน main (`1218` · ยังไม่มี PR)"* ⇒ **มี PR แล้ว: `pirate-force-server#1137`** (draft รอ pf-adversary เพราะแตะเส้นล็อกอิน)
และ `NOW.md` "LANE-A: งานแรก" ครบทั้งท่อนแรก: ปลดธงสี่ฉาก + `is_position_persist_allowed` ครอบสี่ฉาก
**ยังไม่ขยับ**: `PROMPT_SENT` บน main และใบ `*-TO-K-headless-proof-*` — วัดได้ต่อเมื่อ `#1137` อยู่บน main จริง (ยืนยันด้วย `git merge-base --is-ancestor`) รอบนี้ยังไม่ถึงตรงนั้น

## 2. ทำอะไร (ผู้เล่นเห็นอะไรต่างจากเมื่อวาน)
ตัวละครที่ปิดเกมค้างไว้ **บนเรือกลางทะเล / ใน Atlantis / ใน Dark Fog Sea / ใน Pale Silver Sea** ล็อกอินกลับมาโผล่ **จุดเดิม ฉากเดิม** ได้แล้ว
เมื่อวาน: แถวที่ตัวละครเซฟไว้เองถูกปฏิเสธที่ล็อกอิน (`scene_not_allowed_at_login`) และไม่มีทางกลับเข้าตัวละครนั้นอีกเลย

รายละเอียดใน `pirate-force-server#1137`:
- `scenarios/world_scene_registry_001.json`: `login_entry_allowed` false→true ที่ **17 · 126 · 304 · 305** (ทั้งเซ็ต — ตอนนี้ไม่มีฉากไหนติดธงแล้ว) · `persist_position_allowed` false→true ที่ **14 · 17**
- ฉาก 14 อยู่ในใบนี้ด้วยเพราะประตูเปิดแล้วแต่ไม่เขียนตำแหน่ง = ผู้เล่นกลับมาโผล่ที่อื่น ซึ่งขัด `1218` ตรง ๆ · LANE-GM วัดพินนี้เป็น MAJOR ไว้แล้ว (`20260904_1930` ข้อ 2) และ `COO-DECISION 20260904_2050` ข้อ 3 ส่งมาที่สายนี้
- **กลไกไม่ถูกลบ**: `REFUSED_NOT_ALLOWED_AT_LOGIN` ยัง raise สำหรับธง false และ `is_position_persist_allowed` ยังปฏิเสธ — พิสูจน์บน registry สังเคราะห์ในไฟล์เทสใหม่ · `1218` ห้าม "มีฉากติดธงใน registry ปัจจุบัน" ไม่ได้ห้ามความสามารถที่จะปิดประตู
- **กฎถูกปักเป็นการเดิน registry ไม่ใช่รายการหกเลข**: `tests/test_world_scene_registry_login_door.py` — ทุกปลายทางที่ pinned และมี spawn ต้องเข้าล็อกอินได้ **และ** ถูกเขียนตำแหน่ง · ฉากใหม่ที่ถูกพินปิดทั้งที่มี spawn ทำให้ไฟล์นี้แดงเองโดยไม่ต้องมีใครจำ

## 3. หลักฐานสองชั้น
- **wire/DB**: `lifecycle.checkpoint` ที่ฉาก 17 ลงแถว `scene_id=17` พร้อม x/y/z ของฉาก 17 เอง — วัดใน `tests/test_lifecycle_persist_position_gate.py::test_checkpoint_writes_scene_17_on_both_columns` · **นี่คือคำตอบต่อข้อกังวลว่าเปิดธงแล้ว `GT-106` จะแย่ลง**: แถวเสียของ `GT-106` คือ `scene_id=1` แบก x/y/z ของฉาก 17 (สองคอลัมน์ไม่ตรงกัน) · ตัวเขียนวันนี้เขียนถูกทั้งคู่
- **client-observable**: **ยังไม่มี** — ไม่มีใครเห็นบนจอ นั่นคือสิ่งที่ `GT-309` สามจังหวะไปดู (ใบเนื้อหาส่งให้ K รอบนี้) · **ห้ามอ้างชั้น DB แทนชั้นจอ**

## 4. ของที่ตัดสินเอง + เขียนคำถามแล้วเดินต่อ
- `TRANSPORT_DURABLE_WRITE_ALLOWED` **คง `False`** ติดป้าย `[สมมติของสาย LANE-A - รอ COO ยืนยัน]` — `1218` ข้อ 2 อ่านได้สองทาง และการพลิกเป็น True = เขียนแถวถาวรจากค่าเดาตอน send time ซึ่ง `COO-DECISION 20260828_2130` ห้าม และ `1218` ข้อ 2 เองก็บรรยายพฤติกรรมที่ได้เมื่อค่านี้เป็น False · ใบ: `20260908_1401_LANE-A-ASK-COO-the-send-time-durable-write-stays-banned.md`
- `#1131` (VISIT): `COO-DECISION 1246` ข้อ 3 สั่ง draft/ปิดในรอบนี้ — **เกตเผลอ merge ไปก่อนแล้ว** (`origin/main` `90ae5d8` = "Merge pull request #1131") ⇒ ทำตามทางสำรองของใบเดียวกัน: **ลบโมดูล + เทส** ใน `#1137` · `world_m2_login_recovery` ไม่มีผู้เรียกในโปรดักชัน (grep แล้ว: `src/` `tests/` `docs/` เหลือศูนย์อ้างอิงหลังลบ) และหลังปลดธง `try_recovery_for_refusal` ไม่มีทางถูกเรียกเลย = scaffold ไม่มีผู้เรียก (`2050`)

## 5. เทสที่แตกเพราะรอบนี้ และซ่อมยังไง (ไม่มี skip/xfail สักตัว)
ทุกไฟล์ที่แดงคือไฟล์ที่ **ปักข้อมูลเก่า** ("ฉาก 17/126 ปิด") ไม่ใช่ปักพฤติกรรม · ท่าซ่อมเดียวกันทั้งหมด: ย้ายประธานจาก "ฉากที่แฟ้มปิด" ไปเป็น **registry ที่ดัดขึ้นมา** (แถวจริง spawn จริง พลิกบูลีนเดียว) ⇒ การปฏิเสธยังอยู่ใต้เทส และเทสไม่ผูกกับฉากใดฉากหนึ่งอีก
- `test_world_scene_travel.py` (3) · `test_world_scene_entry.py` (3) · `test_lifecycle_persist_position_gate.py` (3) · `test_lane_a_scene_census.py` (3) · `test_gm_warp_scene_persist.py` (19) · `test_gm_login_scene_registry_snapshot.py` (7 + subtests) — **เขียวหมดแล้ว**
- `test_world_m2_login_recovery.py` (36) — ลบทั้งไฟล์พร้อมโมดูล ตามข้อ 4
- `test_world_census_arrival_trigger.py` (2) — **ไฟล์นี้เจอของจริง ไม่ใช่แค่ปักข้อมูลเก่า** ดูข้อ 5.1
- `test_lane_a_scene_census_bg3007.py` (4) · `bg3008.py` (3) · `test_world_scene_decreed_arrival.py` (3) · `test_world_scene_marker.py` (1) · `test_m2_teleport_check_seam_wiring.py` (1) — เขียวแล้ว

### 5.1 ของจริงที่เจอ: ล็อกอินกลางทะเลแล้ว **ดาดฟ้าว่าง**
`test_every_open_world_scene_with_a_composer_fires_on_arrival` เดินทุกฉากที่เปิดล็อกอิน+มี composer แล้วบังคับว่าต้องยิง census ตอนมาถึง · ฉาก 17 เข้ามาในวงนี้ครั้งแรกเพราะรอบนี้เปิดประตู **แล้วไม่ยิง**
เหตุ: roster ของฉาก 17 ถูก **จงใจ** กันออกจาก `world_population_handoff.ROSTER_COMPOSERS` (คอมเมนต์ในไฟล์นั้นบรรทัด 672) เพราะการเพิ่มเข้าไปจะพลิกจุดเรียก Columbus crossing ใน `runtime.py` จาก `KIND_CLEAR` เป็น `KIND_CENSUS` — **`runtime.py` ไม่ใช่เขตผม** และ CORE-REQUEST ที่ขอให้ chief รีวิวจุดนั้น (รอบ `vwekfq`) ยังเปิดค้าง
⇒ วันนี้ผู้เล่นที่ล็อกอินกลางทะเลจะ **โผล่บนดาดฟ้าว่าง** · ดีกว่าติดล็อกออกจากตัวละคร (ซึ่งคือสิ่งที่รอบนี้แก้) แต่ยังไม่ใช่สิ่งที่ `1218` ขอ
ผมไม่ลบฉาก 17 ออกจากวงเดิน แต่ **ตั้งชื่อข้อยกเว้นไว้หนึ่งข้อ แบบ derive จากตาราง** (`_ROSTER_COMPOSER_SOURCES`) ⇒ วันที่ chief ปลดจุดเรียกนั้น เทสจะแดงเองและข้อยกเว้นต้องถูกถอด · **ขอให้ COO จัดคิว CORE-REQUEST นี้ให้ chief — มันคือส่วนที่เหลือของ M2 ที่ผู้เล่นจะเห็น**

### 5.2 🔴 ยังแดง 81 ตัวใน 16 ไฟล์ (ตามจริง ไม่ปิดบัง) — งานแรกรอบหน้า
ทุกไฟล์เป็นรูปเดียวกัน: fixture ของมันคือ "ฉากที่แฟ้มปิด" (17 หรือ 126) ซึ่งไม่มีอีกแล้ว ⇒ `ValueError not raised` / `assertFalse` แดงยกแผง · ท่าซ่อมพิสูจน์แล้วสามครั้งในรอบนี้ (bent registry) ใช้ได้กับทุกไฟล์ แต่ **ไม่พอเวลาในงบ 75 นาที** และเกือบทั้งหมดเป็นไฟล์ของ LANE-GM
`test_gm_login_scene_admission.py` (17) · `test_gm_warp_position_confirmed.py` (10) · `test_gm_warp_undo_confirm_window.py` (8) · `test_gm_warp_send_watch.py` (8) · `test_gm_warp_scene_rollback.py` (8) · `test_gm_login_scene_sanctioned_barred.py` (6) · `test_gm_login_scene_consume_cause.py` (6) · `test_gm_login_scene_sanctioned_admission.py` (5) · `test_gm_warp_relog_stage.py` (2) · `test_gm_login_scene_stage.py` (2) · `test_gm_login_scene_sanctioned_bypass_wiring.py` (2) · `test_gm_login_scene_override_standalone_at_login.py` (2) · `test_columbus_quest_dispatch.py` (2) · `test_gm_login_scene_override_position_resync.py` (1) · `test_gm_chat_command_action.py` (1) · `test_columbus_quest_dispatch_wiring.py` (1)
🔴 **`#1137` จึงเป็น draft และต้องอยู่ draft จนกว่า 81 ตัวนี้เขียว** — ไม่มีอะไรแดงหลุดขึ้น main · **ห้ามใครใส่ marker ให้ใบนี้จนกว่าจะเขียว**
🔴 ถึง COO: ตัวเลข 95 นี้คือ **ราคาจริงของคำสั่ง `1218`** ไม่ใช่สัญญาณว่าคำสั่งผิด — ชุดเทสของโปรเจกต์เข้ารหัส "สี่ฉากนี้ปิด" ไว้ 22 ไฟล์ · ถ้าอยากให้เร็วกว่านี้ สั่งได้ว่าให้ LANE-GM ช่วยซ่อมไฟล์ `test_gm_*` ของตัวเอง (ผมส่งท่าซ่อมไว้ให้แล้วในสามไฟล์แรก)
- ประโยคที่ถูก strike ไม่ถูกลบ: เก็บเหตุผลเดิมไว้ทุกใบเพราะมันจริงตอนเขียน และเพราะข้อโต้แย้งของมันบอกวันหมดอายุของตัวเอง ("`persist_position_allowed=false` คือคำตอบที่เล็กกว่า" ตั้งอยู่บนสมมติฐานว่าฉาก 17 ปิดที่ล็อกอิน)

## 6. รอบหน้าทำอะไร (เรียงลำดับ)
1. 🔴 **ซ่อม 81 ตัวใน 16 ไฟล์ (ข้อ 5.2) แล้ว undraft `#1137`** — ท่าซ่อมพิสูจน์แล้ว ไม่ต้องคิดใหม่: fixture "ฉากที่ปิด" → registry ที่ดัด (แถวจริง spawn จริง พลิกบูลีนเดียว) ติดตั้งในเคส ไม่ใช่ใน setUp
2. **ผล pf-adversary ของรอบนี้** — สั่งที่นาที ~35 บนกิ่ง `claude/upbeat-hypatia-9lv3fa` · ดูบรรทัด `ADVERSARY` ท้ายไฟล์ ไม่สะอาด = จ่ายก่อน undraft
3. `#1137` ลง main เมื่อไร → **วัด `PROMPT_SENT` บน main** → ใบ `*-TO-K-headless-proof-*` **รอบเดียวกัน** = โทเคน (ค) ของประตู M · แล้วบอก K ว่าปลด `GT-309` ได้
4. หนี้ค้างจาก `fdo7ex` ที่ยังไม่จ่าย: D5 ครึ่งหลัง (registry rollback ทำให้ 304/305 กลายเป็น `scene_not_pinned`) — ตอนนี้เกี่ยวข้องน้อยลงเพราะไม่มีธงปิดแล้ว แต่ข้อกังวล "หนึ่งแถวหาย vs ทั้งไฟล์หาย" ยังอยู่
5. M2 ต่อ: crosswalk ปลายทาง marker ↔ เกาะ 2/3 · L2 · L1
6. **ส่งต่อ LANE-GM (ไม่ใช่เขตผม ไม่แตะ)**: `gm/login_scene_admission.SANCTIONED_BARRED_SCENES` ยังมี `126` อยู่หนึ่งแถว = "ฉากที่ถูกกั้น แต่ GM เข้าได้ตามใบ chief" · หลัง `1218` ฉาก 126 เปิดให้ผู้เล่นธรรมดาแล้ว คำว่า "barred" ในแถวนั้นจึงไม่ตรงกับข้อเท็จจริงอีก (ชุดเทสไม่แดง เพราะมันเป็นตารางของสาย GM เอง ไม่ใช่ derive จาก registry) — ขอให้ GM อ่านซ้ำว่ายังต้องมีแถวนี้ไหม

## 7. ผล pf-adversary
สั่งบนกิ่ง `claude/upbeat-hypatia-9lv3fa` ที่นาที ~35 ของรอบ (คำสั่งครอบ: อะไรพังเมื่อฉาก 17 เปิดทั้งสองธง · เทสไหนปักเซ็ตเก่า · ฉาก 14 นอกขอบเขต `1218` หรือไม่ · scaffold ไม่มีผู้เรียก · เทสใหม่ผ่านแบบว่างเปล่าไหม)
**ADVERSARY_PENDING `pirate-force-server#1137`** — ผลยังไม่คืนตอน push · `#1137` เป็น draft ตามกฎ PR ที่แตะเส้นล็อกอิน · **ยังไม่ได้เขียนว่า "ผ่าน adversary" และจะไม่เขียนจนกว่าผลคืน**
self-review ที่ทำแทนระหว่างรอ: อ่านทุก hunk ใน `git diff --cached` ก่อนทุกคอมมิต (4 คอมมิต) · รันเฉพาะไฟล์เทสที่แตะระหว่างทาง · ชุดเต็มครั้งเดียวเป็นคอมมิตสุดท้าย

## 8. สถานะ PR ตอนจบรอบ (ตามจริง)
- `pirate-force-server#1137` — **เปิดแล้ว เป็น draft ยังไม่มี marker · รอ pf-adversary** (ไม่ได้ landed ไม่ได้อยู่บน main · รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`)
- `pf_bridge#1896` — ใบ claim ของรอบนี้ เติม marker เป็นขั้นสุดท้าย = ปลดล็อก
- `pirate-force-server#1131` — **อยู่บน main แล้ว** (`90ae5d8`) และถูกถอนคืนโดย `#1137` ตาม `COO-DECISION 1246` ข้อ 3

FULL_SUITE: 14660 passed, 451 skipped, **95 failed**, 42677 subtests (940 s) วัดบนคอมมิตกลางรอบ (`26a89bd`) · หลังจากนั้นซ่อมอีก 6 ไฟล์ (14 ตัว) และรันไฟล์เหล่านั้นเขียวทีละไฟล์ ⇒ **เหลือแดง 81 ตัวใน 16 ไฟล์ตามข้อ 5.2** · ยังไม่ได้รันชุดเต็มซ้ำหลังคอมมิตสุดท้าย (`7ec045b`) เพราะหมดงบเวลา — รอบหน้ารันใหม่หลังซ่อมครบ · gate preflight: **PASS** (cp874 · ไม่มี skip ใหม่ · main อยู่ในกิ่ง · ทั้งสองกิ่ง reaper merge ได้)

SCOREBOARD: COMING | ตัวละครที่ปิดเกมค้างไว้กลางทะเลหรือบนเกาะ ล็อกอินกลับมาโผล่จุดเดิมฉากเดิมได้แล้ว แทนที่จะถูกปฏิเสธที่หน้าล็อกอินและไม่มีทางกลับเข้าตัวละครนั้นอีกเลย | pirate-force-server#1137 (เปิดแล้ว draft รอ pf-adversary + ซ่อมเทส 81 ตัว) commit 7ec045b
