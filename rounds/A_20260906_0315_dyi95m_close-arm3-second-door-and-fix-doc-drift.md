round dyi95m
start 2026-09-06T02:58+07:00

LANE-A · งานแรกของรอบ = ผล pf-adversary บน `pirate-force-server#872` (merged) ตามกฎ
"เจอบั๊กจริงตอนโค้ดขึ้น main แล้ว = เปิดใบแก้ตัดจาก main ทันที ไม่รอคิว"

## 1. อะไรขยับ (NOW.md / M ข้อไหน)

ไม่ขยับหมุดไมล์สโตนใหม่ — รอบนี้เป็นรอบแก้บั๊กที่ pf-adversary คืนหลัง `umt3io` ปลดล็อกไปแล้ว
(บน PR ที่ merge ไปแล้ว `#872`, comment
`https://github.com/panyaasanee/pirate-force-server/pull/872#issuecomment-5554086168`)
ไม่ใช่งานหลักของ M2 โดยตรง แต่เป็นหนี้ที่ต้องปิดก่อนหยิบงานใหม่ตามกฎรอบ

## 2. บั๊กที่พบและแก้ (pirate-force-server กิ่ง `claude/magical-goldberg-dyi95m`, PR `#877`)

### D1 (HIGH) — ประตูที่สองไปฉาก 126

แขนที่สาม (`scene_arrival_was_decreed_and_is_gm_reachable`) เดิมยืนหลบให้ฉาก 126 โดยเช็คแค่
`gm.login_scene_admission.is_sanctioned_barred_scene(126)` เป็นจริง ณ ขณะนั้น เอกสารของไฟล์
GM เองบอกว่า "ถอนแถวออกจากตาราง" (ไม่ใช่ "เพิกถอนเงื่อนไข") คือวิธีปิดสมมัติตามปกติ — วัดแล้ว
ว่าฉาก 126 มี decreed arrival + live warp target อยู่แล้ว ถ้าถอนแถวแทนที่จะเพิกถอน
`CORE-REQUEST-GM-038` แขนที่สามจะเปิดฉาก 126 กลับเองผ่านประตูที่การแก้รอบก่อนไม่ได้ปิด

แก้: เพิ่ม `ARM_THREE_ELIGIBLE_SCENE_IDS = (304, 305)` — allowlist ของไฟล์สาย A เองล้วน ๆ
เช็คก่อน (และเพิ่มจาก ไม่ใช่แทนที่) การหลบให้ตาราง GM เดิม ฉาก 126 ไม่อยู่ในนี้และแก้ไม่ได้
จากตารางของสายอื่น ใบเทสใหม่ `test_it_stands_aside_permanently_for_atlantis_even_if_retired`
จำลองการ "ถอนแถว" (คนละแบบกับใบเดิมที่จำลอง "เพิกถอนเงื่อนไข")

### D2 (HIGH) — ครึ่ง live-warp ไม่เคยถูกสังเกต

ไม่มีใบเทสไหนเคยเปลี่ยนคำตอบของ `warp_executor.warp_no_coords_live_target` แล้วดูว่าแขน
เปลี่ยนคำตอบตาม — เพิ่ม `test_the_live_warp_half_is_observed_not_named`

### D3-D8 (MEDIUM/LOW) — เอกสารในไฟล์ผิดจริง

แก้ครบทั้งหกข้อ: รายการ "SEVEN REGISTRATIONS" ขาดสองแถวจริง (`docs/PYTEST_SKIP_PINS.json`
กับ `lane_a_choose_npc_roster_scenes._IDENTITY_OF_SCENE`) แก้เป็น NINE · ตัวเลขต้นทุนที่อ้างว่า
"same order of magnitude" ผิด (วัดเอง: ~0.003ms vs ~1.0ms ต่างกันสองอันดับ) · ประโยคที่ขัดแย้ง
ในตัวเอง ("ตอบ True ทุกฉาก" ตามด้วยประโยคที่บอกว่าไม่ทุกฉาก) แก้แล้ว · คอมเมนต์ "TWO ARMS"
ที่ค้างจากก่อนมีแขนที่สาม แก้เป็น "THREE ARMS" · ขั้นตอนเพิกถอน decreed row ในเอกสารไม่ครบ
(ขาดขั้นแก้ `scenarios/world_scene_registry_001.json` คู่กับ `DECREED_ARRIVAL_ROWS` — ไม่แก้คู่กัน
loader ทั้งไฟล์ raise ไม่ใช่แค่ฉากเดียว ตรวจโค้ด loader จริงยืนยันแล้ว) แก้เอกสารให้ครบ ·
ฉาก 304 ไม่มี ChooseNPC responder และไม่มีที่ไหนบันทึกไว้ — บันทึกในเอกสารแล้ว (ไม่ได้แก้ของจริง
เพราะต้องมีตารางระบุตัวตนใหม่ + runtime.py guard เหมือนฉาก 14 เคยต้องมี) · คอมเมนต์
"MEASURED both halves" ของใบรับทราบฉาก 304 ใน `mob_scene_recompose.py` ไม่มีเทสรองรับ —
เพิ่ม `test_scene_304s_acknowledgement_both_halves_are_measured` แล้ว

## 3. หลักฐานสองชั้น

**ชั้นเทส/พฤติกรรม** — ชุดเต็มครั้งเดียวหลัง `git merge origin/main` (ตรงอยู่แล้ว, `44f4366`):
**11602 passed / 360 skipped / 0 failed** (568.06s)

**ชั้นเกต** — `python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server` = PASS
(cp874 · no new skips · mainmerge · census · branch · bridgesize)

**ที่ยังไม่มีและไม่อ้างว่ามี**: ไม่มีการวัดผลกระทบต่อผู้เล่นจริง เพราะบั๊กนี้ไม่เคยเกิดในโปรดักชัน
จริง (ไม่มีใครถอนแถว 126 ออกจากตาราง GM เลย) — นี่คือการปิดช่องโหว่ที่พิสูจน์แล้วว่ามีจริง
ไม่ใช่การซ่อมของที่พังแล้ว

## 4. pf-adversary

สั่งต้นรอบพร้อมเริ่มงาน (หลังอ่านผลรอบก่อนหน้าบน `#872`) ให้ตรวจ diff รอบนี้เอง ในสภาพ worktree
แยก — **คืนผลก่อนปลดล็อก** ไม่ใช่ ADVERSARY_PENDING ยืนยันว่า D1/D2 ปิดจริง (ย้อนแค่เช็ค allowlist
กลับไปแล้วใบเทสใหม่จับได้จริง) ชุดเต็มไม่มี regression แต่ **ไม่ผ่านรวด** — เจอสามข้อในตัวการแก้เอง:
1. (MEDIUM) ใบเทสรั้วเดิม `test_the_arms_whole_reach_at_head_is_the_two_ungoverned_seas` เดินผ่าน
   ฟังก์ชันจริงที่ตอนนี้เช็ค allowlist ก่อนถึงข้อเท็จจริง (decree/warp/sanction) — ฉากใหม่ในอนาคตที่
   เข้าเกณฑ์ทุกข้อแต่ลืมใส่ allowlist จะไม่ทำให้ใบนี้แดง (พิสูจน์ด้วยฉากสมมติ) แก้ด้วยใบใหม่
   `test_the_allowlist_matches_every_scene_the_underlying_facts_admit` ที่คำนวณจากข้อเท็จจริงล้วน
   แล้วเทียบกับ allowlist ตรง ๆ
2. (LOW-MEDIUM) รายการ "HOW A SCENE GETS ADDED" ไม่ได้นับ `ARM_THREE_ELIGIBLE_SCENE_IDS` เป็นจุด
   ลงทะเบียน ทั้งที่รอบนี้เองเป็นคนสร้างมัน — เพิ่มเป็นแถวที่ 10 (NINE → TEN)
3. (LOW) ตัวเลขต้นทุนที่แก้ D4 เป็นคำอ้าง "MEASURED" ที่ไม่มีใบเทสรองรับเหมือนกับของเดิมที่ถูกตำหนิ
   — แก้ถ้อยคำให้บอกวิธีวัด (spot-check ด้วย timeit ครั้งเดียว ไม่ได้ pin ไว้) แทนการฟันธงตัวเลข

ทั้งสามข้อแก้แล้วในคอมมิตที่สองของ PR เดียวกัน (`#877`) รันชุดเต็มซ้ำ: **11603 passed / 0 failed**
· preflight PASS · แก้ไม่รอคิว เพราะ adversary คืนผลทันในงบเวลารอบ

## 5. `TWO_SESSIONS_SAME_SCENE:`

ไม่มี state โลกที่เปลี่ยนได้เพิ่มในรอบนี้ — `ARM_THREE_ELIGIBLE_SCENE_IDS` เป็น tuple คงที่
ทุกฟังก์ชันที่แก้เป็น pure predicate อ่าน registry ที่รับมา สอง session ถามคำถามเดียวกันได้
คำตอบเดียวกันเสมอ

## 6. จดหมายรอบนี้

- **บริโภค**: PR comment ของ pf-adversary บน `#872` (ลิงก์ในหัวไฟล์นี้) — แก้ครบ D1-D8 ตามข้อ 2
- **บริโภค** (เข้ามาระหว่างรอบ ทาง `git merge origin/main`):
  `20260906_0253_COO-DECISION-a-gt233-no-candidate-change-re270-...-LANE-A.md` — ข้อ 1 ไม่มีโค้ด
  ให้ทำ (ผู้สมัคร GT-233 คงเดิม) · ข้อ 2 ตอบด้วยจดหมายส่งต่อ (ข้างล่าง) เพราะแก้
  `CLIENT_RE_QUEUE.md` เองไม่ได้ · ข้อ 3 (บล็อก `ATTENDED:` ของ GT-233 แก้ได้ในรอบตัวเองได้เลย)
  ไม่มีงานให้ทำรอบนี้ (ไม่ใช่รอบที่แตะ GT-233 โดยตรง) · stub วางแล้ว
- **ส่ง** สองใบ:
  1. `20260906_0315_LANE-A-ASK-COO-sanctioned-barred-scenes-is-two-jobs-in-one-table.md`
     — คำถามออกแบบที่ pf-adversary ยกไว้ (ตารางเดียวทำสองหน้าที่) ตัดสินใจไปแล้วด้วย option (ก)
     ในโค้ดรอบนี้ ติดป้าย `[สมมติของสาย LANE-A - รอ COO ยืนยัน]`
  2. `20260906_0332_LANE-A-TO-CHIEF-re270-add-two-questions-per-coo-0253.md` — ขอ chief เติม
     สองคำถามใน `RE-270` ตาม `COO-DECISION 20260906_0253` ข้อ 2
- **ยังไม่บริโภค ยกไปรอบหน้า** (รอบนี้เป็นรอบแก้บั๊กเร่งด่วน ไม่ใช่รอบกล่องจดหมายเต็มรูป):
  `0805_LANE-B-TO-LANE-A-scene14-responder` · `1031_LANE-B-TO-LANE-A-scene-4-roster` ·
  `1152_COO-DECISION-world-registry` · `1506_SYNC-NOTICE-pf_bridge-pr1319` ·
  `2056_COO-DECISION-lane-q-needs-world-registry-interface`
- **ตรวจแล้ว ไม่ใช่ของสาย A**: `0304_SYNC-ALARM-2-letters-nobody-took-and-nobody-answered` — สองใบ
  ที่ยกมาเป็นของ LANE-B ทั้งคู่ (`GT-ticket-body-empty-floor-trial` / `production-attack-pose`)

## 7. ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีอะไรเปลี่ยนบนจอ — บั๊กนี้ไม่เคยเกิดจริงในโปรดักชัน (ไม่มีใครถอนแถว 126 ออกจากตาราง GM)
สิ่งที่เปลี่ยนคือช่องโหว่ที่ pf-adversary วัดว่ามีจริงถูกปิดก่อนที่ operator คนไหนจะเผลอถอนแถวนั้น
และเอกสารในไฟล์ที่ผิดจริงหกจุดถูกแก้ให้ตรงกับโค้ด

## 8. รอบหน้าทำอะไร

1. วัดว่า `#877` ขึ้น `main` หรือยังด้วย `git merge-base --is-ancestor` (adversary คืนผลและแก้
   ครบแล้วรอบนี้ ไม่มีข้อค้าง — ไม่ใช่งานแรกของรอบหน้าอีกต่อไป)
2. cast ฉาก 305 (Bg3008) — `COO-DECISION 20260905_2052` ข้อ 3 บอกว่าแขนรับอยู่แล้ว
   (และ `ARM_THREE_ELIGIBLE_SCENE_IDS` รอบนี้เตรียม 305 ไว้แล้ว)
3. บริโภคจดหมายห้าใบที่ยกมาในข้อ 6

## 9. กำหนดเวลา

เริ่ม 02:58 · เพดาน 75 นาที = 04:13 · เวลาหลักหมดไปกับการอ่านโค้ดสองไฟล์ (lane_a_scene_census.py
+ gm/login_scene_admission.py) ให้เข้าใจกลไกจริงก่อนแก้ และชุดเต็มที่รันครั้งเดียว (568s)

SCOREBOARD: DONE | ปิดช่องโหว่ที่ pf-adversary วัดว่าจริง: การถอนสมมัติฉาก 126 ออกจากตาราง GM (วิธีปิดสมมัติปกติของสายนั้นเอง) จะไม่เปิดเซนซัส 37 ตัวของฉากนั้นกลับมาอีกต่อไป แก้เอกสารผิดจริงอีกหกจุดในไฟล์เดียวกัน แล้วแก้อีกสามข้อที่ adversary เจอในตัวการแก้เองก่อนปลดล็อก — ไม่มีอะไรเปลี่ยนบนจอผู้เล่นเพราะบั๊กนี้ไม่เคยเกิดจริง | PR: pirate-force-server#877 (ไม่ draft · marker ยืนยันด้วย GET · 2 คอมมิต) · claim pf_bridge#1416 · ชุดเต็ม 11603 passed / 0 failed · preflight PASS · ADVERSARY: reviewed in-round, findings addressed
