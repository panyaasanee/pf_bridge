# LANE-B รอบ `q6r3te` -- ตรวจ BUILD-004/5/6 ทั้งสามใบซ้ำจากซอร์สสด, ปิดหนี้เอกสาร
# `SCENE_RECOMPOSE_WIRING` ที่ค้างมาตั้งแต่รอบ `qf83nz`, และยืนยันด้วยหลักฐานใหม่ (ไม่ใช่แค่
# อ้างจดหมายเดิม) ว่าไม่มีจุดขยาย BUILD-004/5/6 ที่ปลอดภัยให้แตะรอบนี้

เปิดรอบ 2026-08-30T21:33+07:00 (ตามที่ orchestrator ให้มา) · เขียนบันทึกนี้ 21:47+07:00
repo: `pirate-force-server` เท่านั้น (ไม่มีไฟล์ `pf_bridge` นอกจากจดหมาย/บันทึกรอบนี้)
branch: `claude/admiring-galileo-q6r3te` (`pirate-force-server`), `claude/friendly-ride-q6r3te` (`pf_bridge`)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** สิ่งที่แก้รอบนี้คือดอกสตริงเอกสาร (`SCENE_RECOMPOSE_WIRING`) ในโมดูลของสาย B เอง --
ไม่แตะ `runtime.py` (ไฟล์ของ chief) ไม่มีจุดเรียกใหม่ ไม่มีบรรทัดคอนโซลใหม่ที่รันจริง ผู้เล่นเห็น
เกมเหมือนเดิมทุกประการ

## ① mailbox -- ตรวจแล้ว ไม่มีจดหมายใหม่ที่ยังไม่บริโภคถึงสาย B

`ls -t notes_to_chief/*.md | head -30` แล้วเทียบเวลากับ 19:41+07 (จุดจบของรอบ `01nkju` ก่อนหน้า):
จดหมายที่ใหม่กว่านั้นทั้งหมด (20:22-21:23) เป็นของสาย GM/สาย A/COO ระหว่างกัน ไม่มีใบไหน
`ADDRESSEE: LANE-B` และไม่มีใบไหนพูดถึงงานของสาย B โดยตรง -- ไม่มีอะไรต้องบริโภครอบนี้

## ② ตรวจ BUILD-004/5/6 ซ้ำจากซอร์สสด ไม่ใช่จากความจำของจดหมายเดิม

คำสั่งรอบนี้เตือนชัดว่าห้ามจบเปล่าอีก ⇒ ก่อนสรุปว่า "ไม่มีอะไรทำ" ไล่ทั้งสามใบใหม่จาก grep
สดบน `main` ปัจจุบัน (ไม่ใช่ก็อปเลขจากจดหมายรอบก่อน):

**BUILD-005 (M4, ตีได้ตายได้) -- WIRED แล้วจริง:**
`grep -n "mob_death.kill(" src/pirateforce_foundation/runtime.py` = บรรทัด `4503` เรียกจริง
พร้อม `widened=mob_death.ruling_for(mob)` -- monster ที่ COO อนุมัติ (template 916 ในบ0001,
31/34/35/103 ใน Bg0002, 27 = Mountain Deer diag) ตายได้บนบูตไม่มีแฟล็กอยู่แล้ว ไม่ใช่ของค้าง

**BUILD-005 ครึ่งดร็อป (M5 ครึ่งแรก) -- WIRED แล้วจริง:**
`mob_loot.roll_drops` เรียกที่ `runtime.py:4767` จริง ของดรอปจริง วาดป้ายชื่อจริง (GT-045 ปิดแล้ว)

**BUILD-006 (M5, เก็บของ+relog) -- บล็อกจริงที่ COO เคาะแล้ว ไม่ใช่ของค้างให้สาย B แก้เอง:**
`grep -c mob_pickup_persist src/pirateforce_foundation/runtime.py` = **0** ยืนยันสดวันนี้ --
จุดเสียบที่สาม (หลังคำขอเก็บของ) ไม่มีจริง เพราะไม่มี wire vital id ขาเข้าสำหรับคำขอเก็บของจริง
(`RE-125` ปิด `BOUNDED-NEGATIVE`, corpus 2,106 ไฟล์/75,208 blocks มี `PickupTerrainThing` W=0/R=0)
`chief-ask-coo` รอบ `1105` (2026-08-30T11:05+07:00) ถามตรงแล้วว่าจุดเสียบที่สามควรทำยังไง
`COO-DECISION 20260830_1145` ตอบชัด: **ผูกเข้ากับ `GT-124`/`GT-146`** (ใบ capture opcode
คลิกเก็บของจริง) -- "ไม่ใช่ backlog item ห้ามแฮกผ่านเลน hypothesis"
`GT-146` (PICKUP-CLICK-OPCODE-CAPTURE-001) สถานะ **PENDING หัวคิว attended ถัดไป** ยังไม่มีผล
⇒ นี่คือบล็อกที่รอ**คนหน้าจอ** ไม่ใช่โค้ด และมีคำตัดสิน COO รองรับแล้ว ไม่ใช่การเดาของสาย B เอง

**BUILD-004 (M3, มอนหลายฉาก) -- ฉาก 14 (Bg0015) ยังถูกล็อกด้วย COO-DECISION ที่ยังไม่ถูกยกเลิก:**
`field_mobs.py:1086-1090` อ้าง `COO-DECISION 2026-08-26T12:46+07:00` ที่สั่งห้าม import
`field_mob_tables_bg0015.py` ที่ไหนก็ตามใน `src/` จนกว่า "lane A's second travel gate and
geometry/reachability check" จะผ่าน -- grep ยืนยันสดว่า `_SCENE_TABLE_MODULES` (บรรทัด 475-484)
ยังมีแค่ `field_mob_tables` (บ0001) กับ `field_mob_tables_bg0002` เท่านั้น ไม่มี Bg0015

ตรวจแยกให้ชัดว่าประตูที่เปิดแล้ว (`COO-DECISION 20260829_2342` + `20260830_0050`) เป็นคนละเรื่อง:
สิ่งที่เปิดคือ **login เข้าฉาก 14 แบบ neutral census** (`GT-134`, D1-D3 ปิดครบ, merge แล้ว) และ
**player faction wire** (`world_faction_admission.py` ของสาย A, D3) -- **ไม่ใช่**ประตูของ
"lane A's second travel gate" ที่ COO-DECISION 12:46 พูดถึง (นั่นคือ `BUILD-002` เรือ/ทะเลที่
เจ้าของสั่งพักไว้ตั้งแต่ `COO-DECISION 2026-08-28T22:50`) การ splice hostile เข้าฉาก 14 ตอนนี้จะ
เป็นการฝ่าฝืนคำสั่ง COO ที่ยังไม่ถูกยกเลิกโดยตรง (และมี guard เทสที่กวาด AST + string ทั้งแพ็กเกจ
เพื่อกันการ import ตรงนี้ด้วย) -- **ไม่ใช่แค่เสี่ยงชนข้อมูล (collision 16 placements ที่ยังไม่คลี่คลาย)
แต่เป็นการฝ่าฝืนกฎที่ยังไม่ถูกยกเลิก** จึงไม่แตะ

## ③ สิ่งที่ลงมือจริงรอบนี้ -- ปิดหนี้เอกสารที่ตัวเองทิ้งไว้จากรอบ `qf83nz`

`mob_scene_recompose.py`'s `SCENE_RECOMPOSE_WIRING` (ดอกสตริงบอก chief ว่าจะต่อสายยังไง)
ไม่ตรงกับของจริงใน `runtime.py` มาตั้งแต่รอบ `qf83nz` (บันทึกไว้เป็นหนี้ข้อ 2 ในรอบนั้น แต่ไม่มี
ใครแก้) -- ตรวจสดกับ `runtime.py:4321-4416` แล้วพบสองจุดที่ดอกสตริงเก่าไม่ได้บอก:

1. เดิมดอกสตริงเรียก `recompose_frames` แบบไม่มีเงื่อนไข -- ของจริงมี guard สองชั้นก่อนเรียก
   (`anchor_record is not None and census_scene_id == anchor_record.scene_id`) ที่ดอกสตริงไม่เคย
   พูดถึงเลย และ `objects=` ก็มีเงื่อนไขแยกต่างหาก (ส่งเฉพาะเมื่อ anchor เป็นฉาก 1)
2. แขนที่ guard ไม่ผ่าน (ไม่มี anchor หรือ anchor เป็นฉากอื่น) ยังส่งเฟรมตัวเดียวแบบ RE-092 เดิม
   โดย**ไม่พิมพ์บรรทัดของโมดูลนี้เลย** (เหมือนที่ pf-adversary รอบ `k882hm` D4 เคยชี้) --
   `no_anchor_record()` ที่รอบ `qf83nz` สร้างไว้ (`STATE_NO_ANCHOR` / `STATE_ANCHOR_SCENE_MISMATCH`)
   ยังไม่มีจุดเรียกจริงใน `runtime.py` (`grep -c no_anchor_record runtime.py` = 0 ยืนยันสด)

แก้ดอกสตริงให้ตรงทั้งสองจุด รวมชื่อ event จริง
(`mob_combat_bar_census_compose_skipped_no_population_anchor`, ยืนยันตรงกับ
`tests/test_mob_combat_census_wiring.py` / `test_mob_scene_recompose_wiring.py`) แทนการเดาชื่อ
เอง -- ไม่มีไฟล์ทดสอบไหน pin สตริงดิบของ `SCENE_RECOMPOSE_WIRING` (`grep` ยืนยันแล้ว) จึงแก้ได้
โดยไม่ชนเทสเดิม

**นี่ไม่ใช่การแก้บั๊ก -- โค้ดจริงใน `runtime.py` ทำงานถูกอยู่แล้ว** สิ่งที่ผิดคือดอกสตริงที่บอก
chief ว่าจะต่อสายยังไง ถ้าปล่อยไว้ผิดต่อไป รอบหน้าที่มีคนอ่านมันเพื่อต่อสาย `no_anchor_record`
จะต่อผิดรูป

## ④a pf-adversary รอบนี้ -- พบหนี้ที่สามที่ร่างแรกพลาด แก้แล้วก่อน push

ร่างแรกของดอกสตริง (ก่อน orchestrator ส่งให้ pf-adversary ตรวจ) แก้ครบแค่สองจุด แต่ตกจุดที่สาม
ใน `if record.composed: ... else:` arm เดิม -- เขียนไว้ว่า
`"mob_combat_bar_census_compose_skipped_" + record.state` แบบ concatenation ตรง ๆ ทั้งที่ของจริง
ใน `runtime.py:4393-4397` เรียก `_recompose_event_suffix(record)` ซึ่งไม่ทำแบบนั้น -- state ที่ขึ้นต้น
`refused_` จะคงคำเดิมไม่เติม `skipped_` ซ้ำ (กัน `mob_combat_bar_census_compose_skipped_refused_...`
ซึ่งไม่มีอยู่จริงในสตริง console ที่ pin ไว้ใน `tests/test_mob_combat_census_wiring.py:354,424` และ
`tests/test_world_wipe_headless_proof.py:591`) -- แก้ให้เรียก `_recompose_event_suffix(record)` แทน
พร้อมคอมเมนต์อธิบายเหตุผล ยืนยันเทสตรงซ้ำหลังแก้: `tests/test_mob_scene_recompose.py`,
`test_mob_scene_recompose_wiring.py`, `test_field_mobs.py`, `test_mob_combat_census_wiring.py`,
`test_mob_combat_dispatch.py` = **140 passed** (ตัวเลขไม่เปลี่ยน เพราะเป็นดอกสตริงล้วนเหมือนเดิม)

pf-adversary รอบนี้ยังตั้งคำถามว่าตัวเลขสวีตเต็ม (5545/327/9710) reproduce ไม่ได้ใน worktree ชั่วคราวที่
มันสร้างเอง (ได้ 5485/387/9700 แทน) -- ตรวจซ้ำด้วยการรันสวีตเต็มจริงบน live checkout นี้เอง (ไม่ใช่
worktree) ได้ผล **5545 passed, 327 skipped, 9710 subtests passed** ตรงกับตัวเลขเดิมเป๊ะ ⇒ ตัวเลขในจดหมาย
ถูกต้อง ความต่างเป็นสิ่งประดิษฐ์ของ worktree ชั่วคราวที่ pf-adversary สร้างเอง (ขาดทรัพยากรภายนอกบางอย่างที่
live checkout มี) ไม่ใช่ปัญหาของรอบนี้ -- แต่เป็นคำถามที่ยังไม่มีคำตอบว่าทำไม worktree วิธีนั้นถึงขาด
ทรัพยากรที่ live checkout มี ทิ้งไว้ให้ chief/COO พิจารณาถ้าจะใช้วิธี worktree สำหรับ adversary รอบถัดไป

pf-adversary ยังจับได้ว่าจดหมาย notes_to_chief ฉบับนี้เขียนกลับขั้ว "heartbeat ต่าง 25 นาที ไม่ผ่านเกณฑ์"
ทั้งที่เกณฑ์จริงคือเกิน 60 นาทีถึงผิด (25 < 60 = ผ่าน) -- แก้คำผิดนั้นแล้วในไฟล์จดหมาย

## ④ ตัวเลขที่วัดได้

```
ไฟล์ที่แตะ (pirate-force-server): 1 -- src/pirateforce_foundation/mob_scene_recompose.py
  (ดอกสตริงเท่านั้น ไม่มีฟังก์ชัน/คลาส/ค่าคงที่ใหม่)
ไฟล์ที่แตะ (pf_bridge): 2 -- จดหมายฉบับนี้ + บันทึกรอบนี้ (ไฟล์นี้)

เทสเฉพาะจุดหลังแก้: 140 passed (tests/test_mob_scene_recompose.py,
  test_mob_scene_recompose_wiring.py, test_field_mobs.py,
  test_mob_combat_census_wiring.py, test_mob_combat_dispatch.py)
สวีตเต็มก่อนแก้:  5545 passed, 327 skipped, 9710 subtests passed, 0 failed
สวีตเต็มหลังแก้:  5545 passed, 327 skipped, 9710 subtests passed, 0 failed  (ตัวเลขเท่ากันเป๊ะ
  ตามที่ควรเป็นสำหรับการแก้ดอกสตริงล้วน)
cp874: encode สำเร็จ, non-ASCII char count = 0 (ตรวจด้วยสคริปต์ ord(c) > 127 ตรง ๆ)
```

## ⑤ หนี้ที่ตรวจแล้วแต่ตัดสินใจไม่แตะรอบนี้ (พร้อมเหตุผลเจาะจง ไม่ใช่ "ไม่มีเวลา")

1. **จุดเสียบที่สามของ M5 (`mob_pickup_persist`)** -- ไม่แตะ เพราะเป็นบล็อกที่ COO เคาะแล้วว่า
   ผูกกับ `GT-124`/`GT-146` (คนหน้าจอ) ไม่ใช่ backlog item (`COO-DECISION 20260830_1145`)
2. **BUILD-004 ฉาก 14 (Bg0015)** -- ไม่แตะ เพราะมี COO-DECISION ที่ยังไม่ถูกยกเลิก
   (`2026-08-26T12:46+07:00`) สั่งห้าม import ตารางมอนของสาย B เข้า `src/` ที่ไหนก็ตาม
   จนกว่าประตูเรือ/ทะเล (`BUILD-002`, พักโดยเจ้าของ) จะผ่าน -- ประตู login แบบ neutral ที่เพิ่ง
   เปิด (`GT-134`) เป็นคนละประตูกับที่ COO 12:46 พูดถึง อ่านผิดจุดนี้จะกลายเป็นฝ่าฝืนกฎ ไม่ใช่
   แค่เสี่ยงชนข้อมูล
3. **`mob_loot.py` ข้อ 19a (สมมติฐานเรื่องรูปร่าง ledger ถ้าทาง FightingDrop* มาแทน)** -- ยังไม่
   เปิด ASK-COO คู่กัน เพราะไม่มีอะไรบล็อกอยู่ตอนนี้ (เป็นความเสี่ยงล่วงหน้า ไม่ใช่บั๊กที่ใช้งานอยู่)
   -- ทิ้งไว้ให้รอบที่เห็นสัญญาณจริงว่า transport เปลี่ยน
4. **`RE-150`'s M6 implication** -- ไม่เริ่ม M6 (นอกกฎบัตรรอบนี้ M3-M5) และ corpus ปัจจุบันไม่มี
   aggro placement นอกบล็อกที่เจ้าของปฏิเสธอยู่แล้ว (RE-150 ปิด BOUNDED-NEGATIVE) -- ไม่มีข้อมูล
   ให้เริ่มสร้างจริงแม้จะเริ่มได้ตามกฎบัตร

## ⑥ ASK-COO / CORE-REQUEST รอบนี้

ไม่มี -- ทุกจุดที่ต้องเคาะ COO เคาะไปแล้วก่อนรอบนี้เปิด (12:46, 22:54, 23:42, 00:46, 11:45)

## ⑦ เปิดใบให้สาย C

ไม่มี -- ไม่มีจุดไหนที่ต้องเดาหรือวัดเพิ่มที่ตอบเองไม่ได้จาก source ที่มีอยู่แล้ว

-- LANE-B (COMBAT) รอบ `q6r3te`
