ถึง: chief (cloud) / COO / cc Panya | จาก: LANE-B (COMBAT) | 2026-08-27T19:57+07:00 (ปิดจดหมาย ~20:2x)
ADDRESSEE: LANE-B (สถานะของตัวเอง), chief (CORE-REQUEST ท้ายจดหมาย), COO (cc)

🔴 **สำคัญ อ่านก่อน:** ระหว่างที่เขียนรอบนี้ เจ้าของออก **ADDENDUM 20:18** ต่อ PANYA-ORDER 18:55 เลือกมอนเอง
เป็น **Mountain Deer (n_ID 27)** แทน — คนละตัวกับ Jungle Big Tiger ที่รอบนี้ใช้ Mountain Deer ไม่อยู่ใน roster
ที่ mine ไว้แล้วของ bg0001 (ต้อง mine ใหม่จาก MOBS/MOBS_TIP/STANDARD_MOB) และ template 27 ไม่อยู่ใน
`WIDENING_RULINGS` เดิม (ต้องขอ ruling ใหม่) — **สองอย่างนี้เป็นงานรอบหน้า ยังไม่ทำในรอบนี้** โค้ดรอบนี้ตอบ
เกณฑ์เดิมของ ADDENDUM 19:05 (aggro+EXP) ถูกต้องสำหรับตัวที่มันเลือก แต่เจ้าของเคาะเองมาทีหลังและเจาะจงกว่า
จึงทับคำตอบนี้ ไม่ใช่ตรรกะผิด — ดูรายละเอียดที่หัวไฟล์ `mob_diag_multi_object.py`

# LANE-B STATUS — GT-DIAG-MULTI-OBJECT-001 ชั้น composition สร้างเสร็จ (ยังไม่ wire) · RE-110/RE-111 บริโภคแล้ว

## ต้นรอบ (addendum v2 A/B)

- Heartbeat ก่อนเริ่ม: `2026-08-27T19:42:03+07:00` เทียบตอนเขียนจดหมาย `19:57` → ต่าง 15 นาที ผ่านกฎ 60 นาที
- PR ก่อนหน้าของสาย B: `pirate-force-server#135` และ `pf_bridge#226` ทั้งคู่ `merged=true` บน main แล้ว (ตรวจผ่าน
  `pull_request_read`) — งานรอบก่อนอยู่บน main จริง ไม่ต้องกู้อะไร
- Lock check: `search_pull_requests is:open in:title [LANE-B]` = 0 ผลทั้งสอง repo ก่อนเริ่มรอบ (ตรวจซ้ำอีกครั้งก่อน
  push ท้ายรอบเหมือนกัน เพราะ repo นี้ยุ่งมาก — ดูหมายเหตุด้านล่าง)
- Mailbox ที่ยังไม่บริโภคซึ่งถึง LANE-B ตอนต้นรอบ: `RE-110-RESULT` (18:32), `RE-111-RESULT` (18:39), และ
  `PANYA-ORDER-diag-multi-object-boot` (18:55, ADDENDUM 19:05) — ทั้งสามบริโภคในรอบนี้ (ดูด้านล่าง)

## หมายเหตุความเร็วของ repo รอบนี้ (ไม่ใช่ปัญหา แต่ต้องบันทึกไว้)

`origin/main` ขยับ 3 ครั้งระหว่างที่ทำรอบนี้ (จาก `3c58c9f` → `d0285f9` → อีกหลาย sync commit) รวมถึงรอบของ
สาย LANE-GM ที่เปิด `RE-113` และ chief ที่ **ต่อสาย `mob_combat`/`mob_death` เข้า `runtime.py` จริงแล้ว**
(`_dispatch_mob_combat` มีอยู่จริง, `tests/test_field_mobs.py`'s tripwire เปลี่ยนไปคาด `runtime.py` มี
`field_mobs`/`mob_combat`/`mob_death` แล้ว) และเพิ่มโมดูลใหม่ `player_hostile_pairing.py` — ทั้งหมดนี้ merge
เข้า main ระหว่างที่ผมทำงาน ผม `git fetch` + rebase สองครั้งกลางรอบเพื่อตามให้ทัน (conflict เดียวที่เจอคือ
`tests/test_field_mobs.py`'s tripwire list ซึ่ง resolve โดยเก็บทั้งสองฝั่ง: ของจริงจาก main (runtime.py มี
`field_mobs`/`mob_combat`/`mob_death` แล้ว) + เพิ่ม `mob_diag_multi_object.py` ของรอบนี้เข้าไปในลิสต์)
**BUILD-005 (M4 ตีได้ตายได้) ดูเหมือนจะ wire เข้า production จริงแล้วตอนนี้** — เป็นข่าวดีที่ผมเจอเป็นผลพลอยได้
ระหว่างรีเบส ไม่ใช่สิ่งที่ผมทำเอง; SERVER_VERSIONS.md ยังไม่มีใครยืนยัน attended จึงยังไม่แตะบรรทัดนั้น

## บริโภคแล้ว: RE-110 + RE-111

ปิดหัวใบทั้งสองใน `CLIENT_RE_QUEUE.md` (ต่อท้ายด้วย `### result`, ไม่ลบของเดิม) + วาง `.CONSUMED.txt` +
สำเนาต้นฉบับไป `notes_to_chief/consumed/` แล้วทั้งคู่:

- **RE-110** (cadence/pose): mixed. Pose selector เป็น positive field map แต่ auto-repeat/cadence ชนเพดาน
  static. `BUILD_IMPACT` บอกไม่ให้แก้ production composition จนกว่าจะมี attended one-field A/B — `mob_combat.py`
  เก็บ `ATTACK_CADENCE_MS_PROVISIONAL=600` แบบ provisional ต่อไปตามเดิม ไม่มีโค้ดต้องแก้รอบนี้
- **RE-111** (loot render): bounded negative. 54B ปัจจุบันครบสมบูรณ์สำหรับ generic ground announcement แล้ว
  ห้ามเติม field เดา `mob_loot.py` ตรวจแล้วไม่มีจุดเดาอยู่ ไม่มีโค้ดต้องแก้รอบนี้เช่นกัน

ทั้งสองใบไม่เปิดใบใหม่ต่อ — ใบเดิมเสนอ attended capture แคบที่สุดไว้แล้วในตัวเอง เปิดใบซ้ำจะแค่พูดซ้ำ

## บริโภคบางส่วน: PANYA-ORDER diag-multi-object (รอบ 1/2 ตามเพดานเวลาที่ใบให้)

สร้างชั้น composition ของ D0/D1a/D1b/D2/D3 เสร็จแล้วใน `pirate-force-server`:
`src/pirateforce_foundation/mob_diag_multi_object.py` + `tests/test_mob_diag_multi_object.py`
(companion PR แยกใน `pirate-force-server`) — ทุกอย่างใช้ฟังก์ชัน production เดิม
(`field_mobs.hostile_actor_entry`/`hostile_npc_attr`, `mob_death.kill`/`dying_frames`/`dead_frames`,
`legacy.make_npc_attr` ตรง ๆ สำหรับ D3) ไม่ประดิษฐ์ composer ใหม่ พิสูจน์ byte-diff ด้วยเทส 18 ใบ (รวม
`test_five_objects_five_distinct_identities_five_distinct_positions`,
`test_no_diagnostic_identity_collides_with_a_live_roster_member`, และคู่ `test_d*_byte_diff_from_control`
ที่ re-derive ฝั่งขวาด้วยฟังก์ชัน production เอง ไม่อ่านจากโมดูลตัวเอง) — ผ่าน pf-adversary ก่อน commit ตามกติกา

**ตัวมอน:** เลือก Jungle Big Tiger (`template_id=60`, placement 58 ของ `field_mobs.HOSTILE_PLACEMENTS`) แทน
ตัวอย่าง Mountain Deer ที่ ADDENDUM 19:05 ยกมา เพราะ (ก) `field_mob_ai_tables.AI_WANDER_ROWS[11]` (ที่ตัวนี้ชี้)
เป็นแถวเดียวใน bg0001 ที่มี `n_AGGRO` ไม่เป็นศูนย์ (1200) ที่ mine ไว้แล้วมี digest (ข) `CONSTDATA_TH__MOBS.tsv`
row 60 มี `f_RATIO_EXP=1.0` (เทียบกับ NPC เนื้อเรื่องสองแถวที่เช็คคู่กันซึ่งมี `f_RATIO_EXP=0.0`) และ
`n_MOB_APPEAR=1` (ค่ากลม เทียบกับ id เฉพาะตัวขนาดใหญ่ของ NPC สองตัวนั้น) — ทั้งสองข้อนี้ติดป้าย
`[LANE-B ASSUMPTION - PROVISIONAL]` ในโค้ดว่าเป็นการอ่านโดยเทียบ ไม่ใช่ RE-proven โดยตรง เลือกตัวนี้เพื่อเลี่ยง
เปิด RE ข้ามฉากใหม่สำหรับเกณฑ์ที่ข้อมูลของฉากนี้เองตอบได้แล้ว

**ตำแหน่ง Z:** ใช้ `0.0` เป็น placeholder ตามแบบ `PANYA-DECISION scene17 provisional arrival xyz 0 0 0` (14:45
วันนี้) ไม่ใช่ค่าพื้นดินจริงที่พิสูจน์แล้ว

**Widened ruling สำหรับ `mob_death.kill()`:** ใช้ string ที่ลงทะเบียนไว้แล้ว
`"COO-RULING-20260827-1350 widen-death-scope-bg0001"` ตรงๆ (ไม่ใช่ string ใหม่) เพราะเกตของ `kill()` ตรวจที่
`mob.template_id` ไม่ใช่ identity — template 60 อยู่ใน covered set ของ ruling นี้แล้ว **หมายเหตุถึง COO/pf-adversary:**
`mob_death.py`'s เองมี `[OPEN RISK, NOT MEASURED]` เขียนไว้แล้วว่า ruling นี้เขียนด้วยถ้อยคำเฉพาะ 13 placement จริง
ของ bg0001 แต่บังคับใช้ผ่าน template เท่านั้น โมดูลนี้เป็นตัวแรกที่ใช้ template 60 กับ mob ที่ไม่ใช่ 1 ใน 13 ตัวจริง
(เป็น synthetic diagnostic placement) — เกตของ mob_death.py เองอนุญาตกรณีนี้โดยการออกแบบ แต่ถ้า COO อ่าน ruling
แคบกว่านี้ ให้บอกมา จะปรับ

**D2 อ่านแบบไหน:** เลือกอ่าน D2 ว่าคือสำเนาของ D0 ทุกฟิลด์ยกเว้นตำแหน่ง (จุดอ้างอิงที่สองในจอเดียวกัน) ไม่ใช่การ
ทดลองค่าทางเลือกใหม่ใน mask `0x070C` ที่ RE-109 ทิ้งไว้ที่ method ceiling — ข้อความในตารางของ PANYA-ORDER
("ตัวควบคุม 'แดงเข้ม' ที่เรามีอยู่แล้ว ไม่ต้องสุ่ม") อ่านได้ทั้งสองแบบ แต่การทดลองค่าทางเลือกต้องมีค่าที่มี
provenance ก่อน ซึ่ง RE-109 บอกไว้ชัดว่ายังไม่มี — เลือกอ่านที่ไม่ต้องเดาค่าใหม่

**ที่ยังไม่ทำรอบนี้ (ตามกำหนดเพดาน 2 รอบของใบ):** ยัง**ไม่ wire**เข้า `runtime.py` (เขตของ chief) — จุดที่ต้อง
ต่อสายเขียนไว้ในโมดูลเองที่ `GT_DIAG_MULTI_OBJECT_WIRING` (ต่อท้ายจดหมายนี้) ยังไม่มีใบ GT queue สำหรับให้เจ้าของ
ทดสอบจริง (จะตามมาจาก pf-queue-author รอบนี้/รอบหน้า) และ D1b ต้องการ session state "เคยส่ง TargetVital ให้
identity นี้หรือยัง" ที่ไม่มีอยู่ในเลนนี้ — ฝากไว้ให้ chief บอกว่ามีของแบบนี้อยู่แล้วหรือไม่ในจุดที่ตอบ CORE-REQUEST

## CORE-REQUEST (ฝัง `GT_DIAG_MULTI_OBJECT_WIRING` ในไฟล์เดียวกัน — จุดเดียวที่ต้องต่อสายใน `runtime.py`)

หลัง config diagnostic เปิด (env var เหมือน `PF_GM_ACCOUNTS_CONFIG`, ปิดโดยดีฟอลต์เสมอ):
1. census ที่ฉากนี้ส่ง เพิ่ม `alive_entry(legacy, obj)` ของทั้งห้า object เข้าไป และพิมพ์
   `describe_diag_object(obj)` ทีละบรรทัดตอนประกอบสำมะโน
2. roster ที่ `_dispatch_mob_combat` ใช้ resolve เป้าหมาย ต้องเห็นทั้งห้า identity นี้ด้วยตอน config เปิด
3. ตอนตาย แยกตาม `obj.label`: D0/D2 → `kill_schedule(...)` (hold_ms ปกติ) · D1a →
   `dying_timer_hold_schedule(...)` (hold 20 วิ) · D1b → `dead_only_schedule(..., target_vital_seen=?)` —
   **ถ้าเลนนี้ไม่มีอะไรติดตามว่า "เคยส่ง TargetVital ให้ identity นี้หรือยัง" อยู่แล้ว บอกมาตรง ๆ ในคำตอบแทนที่จะ
   ส่ง `True` ไปดื้อ ๆ** เพราะนั่นคือข้อเท็จจริงเดียวที่ object นี้มีไว้ทดสอบ · D3 ไม่ต้องมี death handling รอบนี้

## สถานะ BUILD-004/005/006

BUILD-004 ยืนยันสดแล้วรอบก่อน (13/13 mobs, 115/115 census) ยังไม่มีอะไรเปลี่ยนรอบนี้ BUILD-005 ดูเหมือนจะ
wire เข้า production แล้ว (พบระหว่างรีเบส ไม่ใช่ผลงานรอบนี้ — chief/COO ควรยืนยัน attended ก่อนเขียนลง
`SERVER_VERSIONS.md`) BUILD-006 มี `dispatch_pickup_request()` จากรอบก่อนแล้ว ไม่มี blocker ใหม่ที่ต้องรายงาน COO
นอกจาก D1b's session-state question ข้างบน

## ADDENDUM 20:2x+07:00 -- ผล pf-adversary ก่อน commit (5 ข้อ แก้แล้วทั้งหมด)

- **[HIGH]** `DIAG_CENTER_Z=0.0` ผิด -- อ้าง precedent ของฉากอื่น (scene17) ทั้งที่ `population.py`
  ของฉากนี้เองมีข้อมูลจริง (placement ใกล้จุดทดสอบสุด z~2231 ห่าง ~931 หน่วย, placement อื่นในรัศมี 3000
  หน่วยอยู่แถบ 2200-2250 ทั้งหมด) แก้เป็น `2231.17` พร้อม provenance ชัด ถ้าไม่แก้ object ทั้งห้าจะลอยอยู่
  ห่างจากพื้นจริง ~2200 หน่วย ผ่านทุกเทส/ผ่านด่าน headless แต่มนุษย์เห็นจอเปล่า
- **[HIGH]** `GT_DIAG_MULTI_OBJECT_WIRING` เขียนเท็จว่า "ทั้งห้าใช้ `DIAG_WIDENED_RULING`" จริงๆ มีแค่
  D0/D2/D1a ที่ผ่านเกตนั้น D1b เรียก `dead_frames()` ตรง ๆ ไม่มีเกตเลย แก้ข้อความ + เพิ่มเทสตรึง signature
  ของ `dead_frames` ว่าไม่มีพารามิเตอร์ `widened` กัน drift กลับ
- **[MEDIUM-HIGH]** อ้างว่ามีมอน aggro ไม่เป็นศูนย์แค่ 2 ตัวใน bg0001 จริงมี 3 (พลาด placement 132 Orc Chief)
  แก้จำนวน + ใส่เกณฑ์เลือก (level ต่ำสุดในสามตัว) + เพิ่มเทสกันนับผิดซ้ำ
- **[MEDIUM]** `n_MOB_APPEAR`/เลข 8700001-2 ที่อ้างเป็นหลักฐานที่สอง ผิดทั้งคู่ (เลขนั้นอยู่คอลัมน์
  `n_DROPS_QUEST` ไม่ใช่ per-NPC id ใด ๆ และ `n_MOB_APPEAR=1` เป็นค่า default 92% ของทั้งตาราง ไม่ใช่ตัวชี้)
  ถอนออกจาก docstring เหลือแค่ `f_RATIO_EXP` (1.0 vs 0.0) เป็นหลักฐานเดียว
- **[DISCLOSED]** `target_vital_seen=True` ของ D1b เป็น attestation ที่เลนนี้พิสูจน์เองไม่ได้ -- เปิดเผยไว้แล้ว
  ในโค้ด ไม่มีอะไรต้องแก้เพิ่มนอกจากให้แน่ใจว่าข้อความ wiring ที่แก้แล้วคือสิ่งที่ chief อ่านจริง

รันเทสซ้ำหลังแก้ทุกข้อ: 110/110 (ไฟล์ที่เกี่ยวข้อง), full suite 3663 เทส เหลือ error เดิม 18 จุด
(capstone/pefile, มีอยู่ก่อนรอบนี้)

## GAME_TEST_QUEUE.md

เขียนใบ **GT-114 DIAG-MULTI-OBJECT-001** แล้ว (`pf_bridge/GAME_TEST_QUEUE.md`) สถานะ `BLOCKED-ON-WIRING`
(ยังไม่ให้บูต จนกว่า CORE-REQUEST ข้างบนจะลง) อ้างอิง RE-107/108/109 + โมดูลรอบนี้ ตรวจเลขซ้ำตอนเขียน (สูงสุด
ก่อนหน้าคือ RE-113 ไม่มีสายอื่นจอง 114 ระหว่างนี้) ขนาดใบ 6.6KB ผ่านกฎ ≤8KB

## เขตเขียนรอบนี้

`pirate-force-server`: `src/pirateforce_foundation/mob_diag_multi_object.py` (ใหม่),
`tests/test_mob_diag_multi_object.py` (ใหม่), `tests/test_field_mobs.py` (แก้ tripwire list บรรทัดเดียว)
`pf_bridge`: `CLIENT_RE_QUEUE.md` (หัวใบ RE-110/RE-111 ที่ตัวเองเปิด), `GAME_TEST_QUEUE.md` (ใบใหม่ GT-114
ต่อท้าย ไม่แตะใบเดิม), `notes_to_chief/`, `rounds/` ไม่แตะ
`runtime.py`/`app.py`/`pf_login_game_server_v141.py`/`scenarios/world_*.json`
