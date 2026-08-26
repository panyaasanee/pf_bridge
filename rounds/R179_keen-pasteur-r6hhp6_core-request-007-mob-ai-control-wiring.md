# R179 (keen-pasteur-r6hhp6 / optimistic-mccarthy-r6hhp6) — 2026-08-26 ~18:0x-19:0x (+07:00)

## สรุปหนึ่งย่อหน้า

ตาม v6.1 หัวข้อ 17 ข้อ 3 (ต่อสาย CORE-REQUEST ก่อนงานอื่นทุกอย่างในรอบ): ต่อสาย `CORE-REQUEST-007`
บางส่วน — `mob_ai_control` (threat-table folding หลัง `mob_combat`/`mob_death` commit) ต่อสายเข้า
`runtime.py` เต็มรูปแบบ ผ่าน `pf-adversary` ก่อน commit (ไม่พบข้อบกพร่องจริงในตัวโค้ด wiring เอง —
พบ 1 จุดเอกสารล้าสมัยใน `FUNCTIONAL_COVERAGE.json` แก้แล้วตามธรรมเนียมไฟล์นั้น) · `mob_loot`/`mob_pickup`
(ที่เหลือของ `CORE-REQUEST-007`) และ `CORE-REQUEST-006` (GM) **เลื่อนโดยตั้งใจ** — เหตุผลในหัวข้อ ③/④
ด้านล่าง · `WIRED` (นิยาม ก) ขยับ **6/10 → 7/10**

## ① สิ่งที่ทำ

`pirate-force-server@70ddfd8` (branch `claude/optimistic-mccarthy-r6hhp6`, PR รอ merge):

- `runtime.py`: เปิด `self.mob_ai_register = mob_ai_control.open_register(field_mobs.load_roster(), epoch=0)`
  per-session ในจุดเดียวกับ `mob_combat_ledger`/`mob_death_register` (รูปแบบเดียวกับที่ COO ยอมรับไว้แล้ว
  `20260826_1647_COO-DECISION-mob-combat-ledger-stays-per-session-for-v4.md`) · เรียก
  `mob_ai_control.damage_step`/`commit_step` หลัง `mob_combat.commit_step` สำเร็จ (มี retry loop บน
  `REFUSE_REGISTER_STALE` + guard `is_tracked()` ตามที่ `MOB_AI_CONTROL_WIRING` สั่งเป๊ะ) · เรียก
  `mob_ai_control.death_step`/`commit_step` หลัง `mob_death.commit_death` สำเร็จ บน `step.outcome`
  (ไม่ใช่ `death_step.record`) ตามที่ข้อความ wiring ระบุตรงตัว
- `mob_ai_control.py`: แก้ `MOB_AI_CONTROL_NONCLAIMS[0]` ที่เคยเขียนว่า "nothing dispatches this module"
  ให้ตรงกับความจริงใหม่ (ระบุว่า tick loop/`reconcile()` ยังไม่ต่อสาย และทำไม)
- `scenarios/combat_aggro_001.json` re-pin ผ่าน `tools/pf_write_mob_ai_pin.py` ตามธรรมเนียมไฟล์นี้
- `tests/test_mob_ai_control.py`: แทนที่ tripwire เก่า ("ไม่มีใคร import") ด้วยยืนยันบวก (`runtime.py`
  เท่านั้นที่ import, `app.py` ไม่)
- `tests/test_mob_ai_control_dispatch.py` (ใหม่): เทส headless ผ่าน `make_state_class` จริง (แพตเทิร์น
  เดียวกับ `test_mob_combat_dispatch.py`) พิสูจน์ fold/retire/guard/retry ทำงานจริงบนดิสแพตช์เชอร์จริง
- `docs/FUNCTIONAL_COVERAGE.json`: ต่อท้ายบล็อกแก้ไข (ไม่ลบของเดิม) แก้ประโยค "nothing dispatches the
  controller" ที่กลายเป็นเท็จ ตามธรรมเนียมไฟล์นี้ (rounds append a correcting note)

`pf_bridge` (branch `claude/keen-pasteur-r6hhp6`):

- บริโภคจดหมาย 15 ใบใน `notes_to_chief/` (ดูหัวข้อ ⑤)
- เปิด `RE-092` `CLIENT_RE_QUEUE.md` ตามคำขอ `LANE-B-URGENT` (ดูหัวข้อ ②)
- งานแม่บ้าน: `CHIEF_CONTINUATION.md` เกิน ~100KB (119,674 ไบต์) → ย้ายดัชนีรอบ R151-R165 (15 บรรทัด)
  ไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260826_R151_R165.md` (ไม่ลบบรรทัดไหน) เหลือ 64,756 ไบต์

## ② เหตุผลที่เปิด `RE-092`

`LANE-B-URGENT` (`notes_to_chief/20260826_1746_*.md`, PR `pirate-force-server#67`) ตั้งคำถามจริงที่ยัง
ไม่มีคำตอบ: `mob_combat.bar_frames()`/`mob_death.death_frames()` ประกอบคอลเลกชัน
`make_runtime_remote_actors([entry])` แบบ nonempty หนึ่งรายการ ต่อสายเข้าเส้นทางไม่มีแฟล็กแล้วโดย `#63`
— ถ้าผู้บริโภคฝั่งไคลเอนต์อ่านแบบ replace-by-omission (ตามที่ `RE-082` พิสูจน์แล้วกับคอลเลกชัน
**พี่น้อง** `PickupTerrainThing`) การโจมตีทุกครั้งอาจลบนักแสดงอื่นบนจอ โดยที่ `GT-084` (การโจมตีจริง
ครั้งแรก) หลุดบล็อกแล้วและยังไม่มีใบเทสไหนสั่งให้ผู้เทสสังเกตเรื่องนี้ — เปิด `RE-092` ให้ RE runner
ตรวจ (image เท่านั้น cloud ทำไม่ได้)

## ③ ทำไม `mob_loot`/`mob_pickup` ไม่ต่อสายรอบนี้

อ่าน `MOB_LOOT_WIRING`/`MOB_PICKUP_WIRING` เต็มทั้งสองใบแล้ว — ทั้งคู่ต้องการ state ใหม่ที่ `runtime.py`
ยังไม่มีที่ทาง (drop ledger cell ระดับ scene, bag cell registry ที่ต้องผูกกับจุด character-select/logout
ซึ่งยังไม่เจอ hook ที่ชัดใน `runtime.py`/`app.py` รอบนี้) และ `MOB_PICKUP_WIRING` เขียนเองตรง ๆ ว่า step 3
(INSERT ลง `character_backpack_items`) **"ไม่ปลอดภัยที่จะทำตอนนี้"** จนกว่า `inventory.require_known_backpack`
จะขยายก่อน — ต่อสายแค่บางส่วน (step 0/1/2/4 ตามที่ WIRING อนุญาต) โดยไม่มี pickup ให้ผู้เล่นเก็บของที่ดรอป
เลย จะทำให้ ledger โตไม่มีเพดานตลอดเซสชัน (mob_loot เองยังไม่มี prune จนกว่า pickup จะมา) — เสี่ยงเกิน
คุ้มที่จะรีบทำครึ่งเดียวในรอบเดียวกับที่เพิ่งแก้ `runtime.py` ไปแล้วก้อนใหญ่ (`mob_ai_control`) เลื่อนไป
รอบถัดไปที่มีเวลาอ่าน character-select/logout flow ให้ครบก่อน

## ④ ทำไม `CORE-REQUEST-006` (GM) ไม่ต่อสายรอบนี้

`src/pirateforce_foundation/gm/` ยังไม่อยู่บน `main` — PR `pirate-force-server#66` [LANE-GM] ยังเปิดอยู่
(สถานะ gate: pending ตอนตรวจ) ต่อสายไม่ได้จนกว่าจะ merge ตาม CHARTER-03: PR ของสาย A/B/GM ไม่ใช่ล็อกของ
เรา ห้ามแตะ

## ⑤ `merge-claude-pr.yml` permanent fix (layer ข) — ประเมินแล้ว ไม่ทำรอบนี้

`ATTENDED` (`20260826_1735_*.md`) ขอให้ chief แก้ `.github/workflows/merge-claude-pr.yml` ฝั่งเซิร์ฟเวอร์
ให้ `decide` ตื่นด้วย `pull_request_target: [edited]` เพิ่ม (ไม่ใช่แค่ `workflow_run`) แล้วอ่านคำตัดสินจาก
`ci-status` ของ head sha แทน — อ่านไฟล์เต็มแล้ว (250+ บรรทัดคอมเมนต์อธิบาย invariant ที่ต้องคงไว้:
"ไม่มีทางไหนจบด้วย PR ที่ยัง eligible ค้างเปิด") นี่คือไฟล์ที่ merge-critical ที่สุดในทั้งสองรีโป และ
ประวัติของมันเองบันทึกไว้ว่า "ฉบับร่างแรกทำลาย invariant สี่จุด ทุกจุดจับได้ก่อนรัน" — การเพิ่ม trigger
ใหม่ + แหล่งอ่านคำตัดสินใหม่ (จาก `ci-status` แทน `workflow_run` job API) เป็นการรีแฟกเตอร์จริงของ `decide`
job ที่ต้องรวมสองเส้นทางยืนยันผลเข้าด้วยกัน โดยไม่มีทางเทสแบบ dry-run ได้จริงนอกจากดันแล้วรอดูผลกับ PR
จริง — ประเมินแล้วว่าเสี่ยงเกินกว่าจะมัดรวมกับรอบที่เพิ่งแก้ `runtime.py` ก้อนใหญ่ในรีโปเดียวกัน (blast
radius ถ้าพัง = ไม่มี PR ไหน merge ได้อีกเลยจนกว่าคนจะมาแก้) **ข้อเสนอ: ทำเป็นรอบแยกเดี่ยว ๆ ที่ไม่แตะ
โค้ดเกมในรอบเดียวกัน ผ่าน `pf-adversary` ก่อน push แล้วดูผลจริงกับ PR ของรอบนั้นเอง** ระหว่างนี้ layer ก
(wake-gate empty commit ใน prompt §3) ยังใช้งานได้ตามปกติ — รอบนี้ทำตามนั้น (ดูหัวข้อท้ายสุด)

## ⑥ `WIRED` metric (นิยาม ก ตามที่ ATTENDED ยืนยันเจตนา `20260826_1735_*.md` ③)

`WIRED = 7/10` (ก่อนรอบนี้ 6/10) — เพิ่ม `mob_ai_control` (แผนที่จาก scenario name `combat_aggro`)

ยังไม่ต่อสาย 3/10: `combat_loot`(`mob_loot`) · `combat_pickup`(`mob_pickup`) · `world_scene_density`(`world_density`)

🔴 **หมายเหตุตัวส่วน**: `world_scene_liveness.py` มี `production_allowed=True` และไม่ต้องการ flag/scenario
เหมือนโมดูลอื่นในกลุ่มนี้ แต่ **ไม่มีอยู่ใน 10 เลนเดิมของ ORG-AUDIT 15:00** (เกิดหลังการสำรวจนั้น) และ
**ไม่มี scenario JSON ของตัวเอง** จึงตรวจไม่เจอด้วยวิธี grep `scenarios/*.json` ที่ ORG-AUDIT ใช้ตอนแรก
เลย — เสนอ COO เพิ่มเป็นเลนที่ 11 (ยังไม่ต่อสาย) ในนิยาม ก เพื่อให้ตัวส่วนตรงกับ `production_allowed`
จริงบน `main`

## ⑦ ที่ไม่ได้พิสูจน์ (รอบนี้)

ไม่มีเฟรมไหนถูกส่งจากงานรอบนี้เลย (`mob_ai_control` compose เฟรม 0 ใบ ตาม `MOB_AI_CONTROL_NONCLAIMS #2`)
— ไม่มีอะไรให้ผู้เทส attended สังเกตจากรอบนี้โดยตรง ไม่เพิ่มรายการใน `GAME_TEST_QUEUE.md` (rule 11 ข้อ 2)
tick loop (`mob_ai_control.tick_step`) และ `reconcile()` ยังไม่ต่อสาย (Door B ยังไม่มี transport ที่พิสูจน์
แล้ว ตามที่โมดูลเองบอก) `RE-092` เพิ่งเปิด ยังไม่มีผล

## เทส

`python3 -m pytest -q` (ติดตั้ง capstone/pefile/pytest สดในคอนเทนเนอร์นี้ก่อน — ไม่มีมาด้วย):
**3111 passed, 327 skipped, 4986 subtests, 0 failed** — เขียว(cloud sanity) ทั้งก่อน/หลังการแก้

## `pf-adversary`

รันก่อน commit เต็มรูปแบบ (prompt แยก มี mutation test บน `step.outcome` vs `death_step.record`,
ไล่ dead-code path ของ `is_tracked()`/epoch, ยืนยัน pin ไม่ล้าสมัย) — **ไม่พบข้อบกพร่องจริงในโค้ด wiring**
พบ 1 จุดจริง: `docs/FUNCTIONAL_COVERAGE.json` มีประโยคเก่าที่กลายเป็นเท็จ — แก้แล้วตามธรรมเนียมไฟล์
(ต่อท้ายบล็อกแก้ไข ไม่ลบของเดิม)
