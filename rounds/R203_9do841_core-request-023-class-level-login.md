# R203 (session 9do841) — 2026-08-28 ~01:52–02:31 (+07:00)

## เข้ารอบ
- §2 การ์ดกันรอบซ้อน: ไม่มี PR `[LANE-E]`/WIP round claim เปิดค้างทั้งสอง repo ตอนเริ่ม (มี `pf_bridge#153`
  `[LANE-A]` เปิดอยู่ แต่ไม่นับเป็นล็อกของ chief) → จับล็อกทันที: `pf_bridge#257`, `pirate-force-server#162`
  (draft ทั้งคู่, marker `PF-AUTOMERGE: v4` ยืนยันแล้ว)
- §2 ข้อ 7 (ตรวจชะตา PR รอบก่อน): `pf_bridge#249`/`pirate-force-server#157` (R202, 9b6zl6) ทั้งคู่
  `merged=true` — งาน R202 อยู่บน main แล้ว ไม่ต้อง recovery
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง · `pull --rebase` ทั้งสอง repo (pf_bridge ชน
  main ที่ขยับไปแล้ว rebase สะอาด)

## §17 ข้อ 3: CORE-REQUEST ค้าง
ไม่มี CORE-REQUEST-011/012/015 (บล็อกอยู่แล้ว ยังบล็อกเหมือนเดิม ไม่มีอะไรเปลี่ยน) ที่ต่อได้เพิ่มรอบนี้ —
โฟกัสหลักของรอบคือใบเร่งด่วนที่ COO เพิ่งเปิดให้ chief โดยตรง (ดูล่าง)

## §17 ข้อ 4: บริโภคจดหมาย
อ่านและ stub 3 ใบที่ถึง chief/ทุกคนชัดเจน:
- `20260828_0146_COO-DECISION-boot-character-actorattr-core-request-022-to-chief.md`
- `20260828_0150_M1P-RESULT-PASS-...md`
- `20260828_0200_PANYA-DECISION-new-direction-...md`
ใบใหม่ที่มาระหว่างรอบ (GT-101-R3, RE-115, KA1A-FOUND GO-button 0x4391) มีเจ้าของชัด (LANE-GM/RE/LANE-A)
ไม่ใช่ของ chief ตามกฎ "ใครเปิดใบคนนั้นบริโภค" — ปล่อยให้สายนั้น stub เอง

## งานหลัก: CORE-REQUEST-023 (COO เรียก "022" — ชนกับ R202 ที่จองเลขนั้นไปแล้ว, chief ขยับเป็น 023)
คำสั่ง: ทุกตัวละครที่บูตเทสต้องได้ `probe base 1` อย่างต่ำ — มีชื่อในช่อง 1 และมีค่าขั้นต่ำสมประกอบ (class,
level, ฯลฯ) ไม่ใช่ HP 100/100 + class 0 แบบทุกรอบที่ผ่านมา — บล็อกจริง: GT learn-skill ค้างเพราะหน้าต่าง
สกิลไม่เปิด (client เห็น class=0 เสมอ เพราะ server ไม่เคยส่ง)

### สืบสวนก่อนแก้
ใช้ Explore agent สำรวจ `player_wire.py`/`legacy_bridge.py`/`runtime.py` ก่อน พบว่า:
- `player_wire._make_actor_attr_with_name` เป็น hand-rolled byte string ตายตัว ไม่มี mask-driven field table
- `stats_progression_hypothesis.py` มี `AttrField`/`encode_actor_attr` ที่ pin offset/tag/bit ของ class_id
  (`ActorAttr +0x8C` bit `0x1`, gate `GetClass 0x460160`) และ level (`BasicAttr +0x5E` bit `0x2`, gate
  `GetLv 0x460050`) จริง — Grade A static, ไม่ใช่การเดา
- ชื่อตัวละครที่ `+0x164` (ActorAttr mask `0x01000000`) มีรายงาน static + live-client PASS สองใบยืนยัน
  ว่าถูกต้อง (`PF_CHARACTER_NAME001`/`002`) — **ขัดแย้งตรงกับที่ใบ COO/PANYA-DECISION อ้างว่าเป็น "ช่องกิลด์
  ผิด ต้องย้ายไป +0x28"** — G1/G6 ห้ามอ้างแหล่งเดียว/ห้ามประกาศความหมาย field จากการอ่านครั้งเดียว →
  **ตัดสินใจไม่แตะช่องชื่อ** เขียน CHIEF-REPLY ขอ COO/RE ยืนยันก่อน แทนที่จะเชื่อ probe fork ที่ไม่ได้
  commit เข้ารีโปนี้เลย

### ทำจริง (เวอร์ชันแรกพัง แก้สองรอบ)
1. เวอร์ชันแรก: แก้ `_make_actor_attr_with_name` ตรง ๆ ให้ใส่ class+level → ทำให้ 42 เทสแดง (ทั้งเว็บ
   crosscheck ของ `stats_progression_hypothesis`/`hp_death`/`dying_hold` ที่ pin byte เดิมของฟังก์ชันนี้
   ตรง ๆ) — **revert** เปลี่ยนแนวทาง
2. เวอร์ชันสอง: เพิ่มฟังก์ชันใหม่ `make_actor_attr_with_name_and_class` (ไม่แตะของเดิม) ต่อสายเฉพาะ
   `legacy_bridge.start_game`'s `basic_faction=None` branch → เหลือ 11 เทสแดง
3. สาเหตุที่เหลือ: `runtime.py` มี**สองจุด**ที่ recompose เฟรมที่สองด้วย `basic_faction=1` (scenario-gated
   GT-032-proven probe + flagless production hostile-pairing) แล้ว**เทียบความยาว**กับเฟรม plain จากซีม
   เดียวกัน ปฏิเสธถ้าความยาวไม่ตรง delta ที่ pin ไว้ (`NPC_HOSTILE_PLAYER_FACTION_WIRE_DELTA = 5`) — ถ้า
   ฝั่ง plain ยาวขึ้น (มี class+level) แต่ฝั่ง faction ยังสั้นเท่าเดิม (ฟังก์ชันเดิม ไม่มี class+level) การ
   เทียบจะพังทุกครั้ง (fail-closed) ⇒ **ฟีเจอร์ hostile-pairing ที่ใช้งานจริงอยู่แล้วจะพัง** ถ้าไม่แก้ทั้งคู่
4. เพิ่มฟังก์ชันที่สาม `make_actor_attr_with_name_class_and_faction` (class+level+faction รวมกัน, guard
   เดียวกับของเดิม HYP-PF-001) ต่อสายให้ทั้งสองสาขาของ `legacy_bridge.start_game` ใช้ฟังก์ชันตระกูลใหม่
   สม่ำเสมอ → เหลือ 0 เทสแดง เต็มสวีต

### หลักฐาน
- เทสเต็ม `3546 passed, 198 skipped, 23 errors (เดิม, capstone/pefile ไม่ติดตั้ง sandbox — ยืนยันด้วย
  `git stash` เทียบก่อน/หลัง เลข error เท่ากันเป๊ะ), 0 failed` เขียว(cloud sanity)
- golden hash 2 ไฟล์ (`foundation_v1.json`, `item_lifecycle_v1.json`) อัปเดตเฉพาะฟิลด์ `start_pc`/
  `start_frame`/`merged_start_*` — ยืนยันด้วยสคริปต์คำนวณอิสระว่าฟิลด์อื่น (`actor_wire`, `create_pc`,
  `list_pc`, `initial_backpack`, `merge_response_*`, `merged_backpack`) ไม่ขยับเลย
- `docs/HYPOTHESIS_LEDGER.json`'s HYP-PF-001 source_ref marker ย้ายชื่อฟังก์ชันตามจริง (`legacy_bridge.py`
  ไม่เรียก `make_actor_attr_with_basic_faction` อีกแล้ว) · `tools/verify_hypothesis_ledger.py`'s
  `CANONICAL_CONTENT_SHA256` อัปเดตตาม (คำนวณจริง ไม่ได้เดา) — `HYPOTHESIS_LEDGER PASS entries=47`
- `pf-adversary` รีวิวเต็มก่อน commit ตามกฎ §10 — ไม่พบบั๊ก wire-layout (ตรวจ mask bit/tag/offset/ลำดับ
  เทียบกับ `stats_progression_hypothesis.py`'s field table อิสระ) พบ 3 จุด docstring/label ค้างชื่อ
  ฟังก์ชันเก่า (`npc_hostile_hypothesis.py` ×2 + scenario JSON, `stats_progression_hypothesis.py`,
  `player_wire.py`'s comment เอง) — แก้ครบในคอมมิตเดียวกัน ยังไม่แก้: คำถามเปิดว่า class=1/level=1
  ควรเป็นค่าคงที่ถาวรหรือควรผูกกับข้อมูลตัวละครจริงในอนาคต — ไม่ได้ตัดสินใจในรอบนี้ ทิ้งไว้เป็นคำถามเปิด

## Files touched (13 — เกิน ~6 ไฟล์ตามแนวทาง §7 ด้วยเหตุผลเดียว)
`legacy_bridge.py`, `player_wire.py`, `npc_hostile_hypothesis.py`, `stats_progression_hypothesis.py` (โค้ด
4) · `docs/HYPOTHESIS_LEDGER.json`, `scenarios/npc_hostile_hypothesis_faction_pairing.json`,
`tools/verify_hypothesis_ledger.py` (marker/pin sync 3) · `tests/golden/foundation_v1.json`,
`tests/golden/item_lifecycle_v1.json` (golden hash sync 2) · `tests/test_foundation.py`,
`tests/test_npc_hostile_dispatch.py`, `tests/test_player_name.py`, `tests/test_scene_load.py` (เทสที่
ตรวจไบต์จริงผ่าน dispatch ต้องตามให้ตรง 4) — เรื่องเดียว (CORE-REQUEST-023), ทุกไฟล์เป็นผลตรงของการเปลี่ยน
byte layout เดียวกัน ไม่แยกได้จริงโดยไม่ทำให้ระหว่างทางเทสแดง

## ที่ยังไม่ได้พิสูจน์ / ยังไม่ทำ
- ย้ายชื่อตัวละครจาก `+0x164` ไป `+0x28` — ตั้งใจไม่ทำ รอ COO/RE ยืนยัน (ดูเหตุผลข้างบน)
- HP/MP/abilities ตามตาราง 22 ช่องเต็มของ PANYA-DECISION 0125 — ไม่มีตัวเลข STANDARD_STATUS/
  CHARCREATE_CLASS จริงใน repo นี้ ไม่กล้าเดาแล้วส่งขึ้น wire
- lane_hooks สำหรับ actor-entry composer (PANYA-DECISION 0200 ข้อ ก บรรทัดสุดท้าย, §18 ข้อ 1 ของ prompt)
  — ยังไม่เริ่ม รอบนี้เต็มกับ CORE-REQUEST-023 คนเดียว
- ledger drift root-cause (§18 ข้อ 2), CHIEF_CONTINUATION/AGENTS.md size cut (§18 ข้อ 3) — ไม่ได้แตะรอบนี้

## จบรอบ
push แล้ว รอ merge: `pirate-force-server@8017c71` (branch `claude/awesome-darwin-9do841`),
`pf_bridge` (branch `claude/wonderful-fermat-9do841`, ใบนี้ + mailbox + CHIEF_CONTINUATION + GT queue)
