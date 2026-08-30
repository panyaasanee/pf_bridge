# R184 (session `session_016e3RsDGu2eNMeGYNAKd7S5`, branch suffix `kdx85r`) — 2026-08-27 ~00:5x-01:1x (+07:00)

## ① CORE-REQUEST / WIRED check (v6.1 §17 ข้อ 3 — บังคับก่อนงานอื่น)

ตรวจสด `runtime.py`/`app.py` เทียบ 10 เลนของ `ORG-AUDIT 15:00` (COO-DECISION `20260826_1743` นิยาม (ก)):
`combat_aggro` (`mob_ai_control`→`mob_aggro`) · `combat_death` (`mob_death`) · `combat_first_hit`
(`mob_combat`) · `combat_loot` (`mob_loot`) · `combat_pickup` (`mob_pickup`) · `field_mobs_hostile`
(`field_mobs`) · `world_population_full` (`world_population`) · `world_scene_density` (`world_density`) ·
`world_scene_registry` (`world_scene_entry`+`world_scene_travel`) · `world_travel_gates`
(`world_travel_gate`) — **ทั้ง 10 มี call site จริงใน `runtime.py` แล้ว** (ยืนยันด้วย grep นับ call-site ไม่ใช่แค่
`import`, ทุกตัว ≥1 call site จริงนอก import statement)

**`WIRED` = 10/10** (ไม่ใช่ 6/10 ตามที่ `COO-DECISION 1743` บันทึกไว้ตอน 17:43 — เพิ่มขึ้นจากรอบ R179/R180/R182
ที่ต่อสาย `mob_ai_control`/`mob_loot`/`mob_pickup` (`CORE-REQUEST-007`) ไปแล้ว) **ไม่มี escalation**

**นอกเหนือจาก 10 เลนที่นับ `WIRED`:** พบ `CORE-REQUEST` ค้างจริงหนึ่งใบ — จดหมาย Lane A
`notes_to_chief/20260826_1010_LANE-A-URGENT-the-door-out-of-town-may-never-see-anyone-arrive.md` ข้อ ④(2)
ขอสามคอลรายงานอย่างเดียว (ไม่เขียนแถวบ้านทับ) ให้ `world_scene_liveness.py` ค้างมาตั้งแต่ 10:10 (~7 ชั่วโมง
ข้ามหลายรอบ) — **ต่อสายให้ในรอบนี้** (ดู ③) ตามกฎข้อ 6 ("อย่าให้เขารอข้ามรอบ") `world_scene_liveness` ไม่ใช่หนึ่งใน
10 เลนที่นับ `WIRED` (ไม่มี `scenarios/*.json production_allowed`) จึงไม่เปลี่ยนตัวเลข `WIRED` — เป็นคนละงาน

## ② COO decisions ที่ต้องรับทราบ (ไม่ต้องลงมือเพิ่ม)

- `COO-DECISION 21:47` (`BUILD-002`/scene278): ยังห้ามเป็นดีฟอลต์ — ไม่แตะ `travel_gate_debug_enabled`
- `COO-DECISION 21:46` (mailbox stub backlog): ไม่ backfill 148+74 ใบเดิม แต่จดหมายใหม่ที่อ่าน-ตอบเองต้อง stub
  ที่ `notes_to_chief/consumed/` — ทำแล้วสำหรับ 3 ใบผล RE ที่ปิดรอบนี้ (ดู ④)

## ③ ต่อสาย `world_scene_liveness.py` เข้า `runtime.py` (`pirate-force-server`)

สาม call site ตามที่จดหมาย Lane A ขอเป๊ะ ไม่มีจุดไหนส่ง `rewrite=True`:

1. `SceneLivenessLedger.preload(registry=scene_entry_registry)` ที่ factory scope (ข้าง
   `world_travel_gate.preload()` เดิม) + stand-down ด้วย `scenario_stand_down(active_lanes)` — **ไม่ใช่**
   `lane_reason()` เพราะเลนนี้ไม่เกี่ยวกับประตู walk-in ที่ปิดด้วย debug flag เสมอ (0655 ข้อ (ข) เพรดิเคตเดียว)
2. `_travel_gate_emit(line)` closure ใหม่ (`print(line)` แล้ว `scene_liveness_ledger.observe_console_line(line)`)
   แทนที่ `emit=print` เดิมของ `TravelGateSet.from_preloaded(...)` — จุดเดียวที่ประตูพิมพ์บรรทัดคอนโซลอยู่แล้ว
3. `decide()` + `liveness_console_line()` ต่อท้าย `resolve_entry()` ของ `CORE-REQUEST-003` ทันที (ก่อนบล็อก
   GM `CORE-REQUEST-006`) ใช้ `self.foundation.selected.position` เป็นแถวที่เก็บอยู่ — แถวเดิมก่อน
   `resolve_entry` เพราะไม่มีอะไรเขียนมันมาก่อนบรรทัดนี้

เขียนเทสใหม่ `tests/test_world_scene_liveness_wiring.py` (6 เทส) ขับผ่าน `make_state_class` จริง ไม่ใช่ double:
บูตดีฟอลต์พิมพ์บรรทัด `WORLD_SCENE_LIVENESS` ที่ล็อกอินจริง (`reason=home_row`) · เลนที่มี opt-in scenario
stand-down ledger ด้วยเพรดิเคตเดียวกับประตู · ledger เป็นตัวเดียวกับ process-wide preload (ไม่ใช่สำเนาใหม่) · guard
สถิตว่า `rewrite=True` ไม่ปรากฏในไฟล์ · walk ข้ามฉากจริงผ่าน `state.world_travel_gates` (เปิด debug) ยืนยันว่า
`WORLD_TRAVEL_SETTLED` ไปถึง ledger ผ่าน closure ตัวจริง ไม่ใช่ test double แล้วเปลี่ยนคำตอบของ `decide()` จริง

`pf-adversary` รีวิวก่อน commit: ไม่พบบั๊กที่ทำแถวพัง/crash/หลุด RB7 gate แต่พบสองข้อ —
(1) production จริงวันนี้ `travel_gate_debug_enabled=False` เสมอ ⇒ `settles=` ในบรรทัดคอนโซลจะเป็น `0` ตลอดไป
โดยการออกแบบ (คนละเหตุผลกับ half-wiring) แต่คอมเมนต์เดิมของผมสื่อว่า `lines_seen=0` คือสัญญาณ half-wire ซึ่ง
ไม่จริงเพราะ `lines_seen` นับบรรทัด `INERT` ด้วย — **แก้แล้ว**: คอมเมนต์ที่ `runtime.py` เขียนชัดเจนว่า
`settles=0` ถาวรในโปรดักชันคือของปกติ ไม่ใช่บั๊ก (2) เทส emit-fanout เดิมพิสูจน์แค่บรรทัด `INERT` ไม่พิสูจน์ทาง
`SETTLED` จริง — **แก้แล้ว**: เพิ่มเทส walk ข้ามฉากจริงตามด้านบน

สวีตเต็ม: `3218 passed, 327 skipped, 4986 subtests, 0 failed` เขียว(cloud sanity) · push
`pirate-force-server@731498e`

## ④ ปิดใบ `CLIENT_RE_QUEUE.md` สามใบที่มีผลค้างสถานะ `OPEN`

RE runner local ส่งผลมาแล้วสามใบตั้งแต่ 23:22-00:16 แต่หัวใบยังไม่ถูกปิดให้ตรงสภาพ (ตามแบบที่ Lane A เคยเจอกับ
`RE-077`) — ปิดให้ตรงรอบนี้ทั้งสามใบ พร้อม stub `.CONSUMED.txt` ที่ `notes_to_chief/consumed/`:

- `RE-089` (GM-STATE-VISUAL-001) → `🟠 DONE/BOUNDED-NEGATIVE`: wire `+0x14/+0x15` normalize เป็น "เท่ากับ 1
  เท่านั้น" เก็บที่ `GMModule_Client+0x18/+0x19`, `+0x18` (u32) ก๊อปไป `+0x1C` — ไม่พบ semantic label
  (is_gm/level) หรือ crosswalk ไปหน้าจอ · เบาะแส `bm_gm.tga` หักล้างแล้ว (เป็น glyph `0x29` ของ `FxNumberCache`)
- `RE-090` (TELEPORT-FORCEPOS-WARP-FIELDS-001) → `✅ PASS/DONE`: `ForcePos`=vec3 ล้วน, `CWarpResult`=
  tag 0x32/8B→tag 0x2A×3→tag 0x12/2B, `TeleportVital` มี scene/sequence/vec3+optional object+controls
  (ปิดช่อง UNKNOWN 6 แถวเดิมใน `PF_SERIALIZER_FIELDS.tsv`: เป็น object-pool/refcount ไม่ใช่ wire field)
- `RE-091` (CHEAT-CHAT-TRIGGER-001) → `✅ PASS/DONE`: objective เดิมเป็น false dichotomy — GM UI มีช่อง editor
  แยกต่างหากที่สร้าง `GM_RunGMCommandVital` เอง ไม่ใช่ prefix branch ใน main chat

ทั้งสามใบเป็นชั้น static ล้วน ไม่มีผล client-observable — ไม่ปิดใบ GT ใดด้วยผลนี้

## ⑤ GAME_TEST_QUEUE.md รอบนี้

ไม่มีรายการใหม่/แก้ — งานหลักของรอบ (③) เป็น report-only, พิมพ์บรรทัดคอนโซลเท่านั้น ไม่มีของใหม่ให้ผู้เล่นเห็นบนจอ
และ (④) เป็นชั้น static ล้วน ไม่แตะชั้น client-observable ของใบไหน จึงไม่มีอะไรให้เทสแอตเทนเด็ดรอบนี้

## ⑥ ค้าง

- `RB7` (attended, ยังไม่มีคนขับ): พิกัด HUD สองเฟรมที่ใบแม่ถ่ายอยู่แล้ว — คำตอบจะปลดล็อกว่า `rewrite=True`
  ปลอดภัยหรือไม่สำหรับ `world_scene_liveness.decide()` (ยังไม่แตะจนกว่าจะตอบ)
- ยังไม่มีรอบ attended ยืนยัน `GT-084`
