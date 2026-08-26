# R178 (keen-pasteur-6js9ye / optimistic-mccarthy-6js9ye) — 2026-08-26 ~16:5x-17:3x (+07:00)

## บริบทตอนเข้ารอบ
รอบก่อน (R177) ปิดแล้ว, `pirate-force-server` HEAD = `c101b2d`, `pf_bridge` HEAD = `18e9b98`. mailbox มี 6 ใบใหม่ตั้งแต่ 16:00-16:47: `PANYA-DECISION` (ประตูออกเมืองแบบเดิมไม่มีจริง — ทางจริงคือ Columbus→ทะเล→เทียบท่า→รายงานกัปตัน), `ATTENDED-REPLY` (ปิดข้อ ③ ของ COO 15:43 + ชี้แจง §18-1), `PANYA-ORDER` (เปิด [LANE-GM] + ผลสำรวจ GM vitals), และ COO-DECISION สามใบตอบทั้งสามเรื่อง (travel-gate redefine M2, CHARTER-03 อนุมัติ Lane GM, mob-combat ledger per-session ยืนตามเดิม)

**v6.1 §18 — ยืนยันซ้ำเป็นครั้งที่สาม (R175, R176, R177 เขียนไว้แล้วว่าเท็จ/ซ้ำ):** ข้อ 1 (`GT-001` "แก้แล้ว") ยังเป็นข้อความเท็จเดียวกับที่ R175 ตรวจแล้วคืน HOLD และ attended ยืนยันซ้ำในใบ 16:15 ว่าโค้ดแก้จริงแต่หลักฐานทดสอบไม่มีบนสะพาน — **ไม่แตะ `GT-001` รอบนี้เช่นเดิม** ข้อ 2/3/5 ทำเสร็จไปก่อน v6 แล้ว ข้อ 4 ปิดไปคนละเส้นทางแล้ว (`GT-033`=R166, `RE-075`=R175) เจ้าของเองสั่งให้ "รอดู v6.1 ก่อน" ยังไม่แตะ prompt — **ไม่ต้องเสนอซ้ำรอบนี้ เจ้าของรับทราบแล้ว**

## งานที่ทำ (เรียงตามลำดับ §17)

### 1. การ์ดกันรอบซ้อน + จับล็อก
`git fetch --all` ทั้งสอง repo · ตรวจ PR เปิดค้าง: `pf_bridge` ไม่มี · `pirate-force-server` มี PR #61 `[LANE-A]` (ไม่ใช่ล็อกของ chief ไม่แตะ) · จับล็อกด้วย empty commit + draft PR ทั้งสอง repo: `pf_bridge#121`, `pirate-force-server#64` ทั้งคู่ `draft:true` (ยืนยันด้วย `pull_request_read` หลังเปิด)

### 2. ยืนยันโครงพี่น้อง
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง · ทั้งสอง branch เท่ากับ `origin/main` พอดี (0 ahead/0 behind) ไม่ต้อง rebase

### 3. เคลียร์กล่องจดหมาย
consume ครบ 6 ใบ (16:00-16:47) — copy ไป `consumed/` + วาง `.CONSUMED.txt` stub ตามกฎ ไม่ลบ ไม่ย้ายต้นฉบับ

### 4. ทำตามคำตัดสิน COO ทั้งสามใบ

**(ก) travel-gate off-by-default (`COO-DECISION 16:45` ข้อ 1)** — `pf-builder` เขียน `DEBUG_LANE_DISABLED_REASON` + `lane_reason(selected, *, debug_enabled=False)` ใน `world_travel_gate.py` (ไม่แตะ `scenario_stand_down` เดิม, ยังใช้เป็น secondary guard เมื่อ debug=True) พร้อมเทส 6 ตัวใหม่ — **แต่ปฏิเสธแตะ `runtime.py`/`app.py` เอง** ตามกฎเขตเขียนของตัวเอง (ถูกต้อง — ไฟล์นั้นเป็นของ chief คนเดียว) ส่ง `CORE-REQUEST` กลับมาเป็นบรรทัดเดียวตามกฎ · chief เดินสายเอง: `make_state_class(...)` เพิ่ม `travel_gate_debug_enabled=False`, call site เปลี่ยนจาก `scenario_stand_down(active_lanes)` เป็น `lane_reason(active_lanes, debug_enabled=travel_gate_debug_enabled)`, `app.py` เพิ่มแฟล็ก `--enable-travel-gate-debug` (store_true, default off) และร้อยสายเข้า `make_state_class(...)` · **โค้ดเดิมไม่ถูกลบสักบรรทัด** ตามที่ COO สั่ง
สวีตเต็ม (หลังติดตั้ง `capstone`+`pefile` ที่หายไปจาก python3 ของ session นี้ — ไม่ใช่ปัญหาจากการแก้โค้ด ยืนยันด้วยการ `git stash` แล้วรันซ้ำได้ error เดียวกัน): **`3103 passed, 327 skipped, 4986 subtests, 0 failed`** เขียว(cloud sanity) — เพิ่มขึ้นจาก R177 พอดี 6 เทสใหม่ ไม่มี regression

`pf-adversary` รีวิวก่อน commit พบ **2 ข้อจริง**:
- 🔴 **สูง**: จุดต่อสายจริงที่สำคัญที่สุด (`runtime.py:494` ที่ร้อย `travel_gate_debug_enabled` เข้า `lane_reason`) **ไม่มีเทสใดแตะเลย** — พิสูจน์ด้วยการย้อนบรรทัดนั้นกลับเป็น `scenario_stand_down(active_lanes)` เดิมแล้วรันสวีตเต็มซ้ำ: เขียวเหมือนเดิมทุกตัว (เทส 6 ตัวใหม่เรียก `lane_reason`/`TravelGateSet` ตรง ๆ ไม่ผ่าน `make_state_class` เลย) ⇒ **แก้แล้ว**: เพิ่มคลาสเทสใหม่ `TravelGateDebugFlagReachesTheRealBootTests` (3 เทส) ที่บูตผ่าน `runtime.make_state_class` จริง (ล็อกอินจริง ผ่าน `SQLiteStore`/`CharacterLifecycle`/`LegacyProjector` แบบเดียวกับ `test_world_census_wiring.py`) แล้วอ่าน `state.world_travel_gates.inert_reason` — **ยืนยันด้วยการทำซ้ำวิธีของ adversary เอง**: ย้อน `runtime.py:494` กลับ รันเฉพาะคลาสใหม่ → แดง 2/3 ทันที (`AssertionError: None != 'walkin_travel_gate_disabled...'`) แล้วคืนไฟล์กลับ (`diff` ยืนยัน byte-identical) ⇒ เทสนี้จับ regression ที่จุดนี้ได้จริง ไม่ใช่แค่ดูเหมือนจับได้
- 🟡 **ต่ำ**: `scenarios/world_travel_gates_001.json` ฟิลด์ `the_opt_in_lane_guard` ยังบรรยายพฤติกรรมก่อนคำตัดสิน COO เท่านั้น (ไม่ได้อัปเดตตอนแก้ docstring ของโมดูล) ⇒ **แก้แล้ว**: เพิ่มฟิลด์ `COO_RULING_20260826_1645_SUPERSEDES_THE_PARAGRAPH_ABOVE` ต่อท้าย (ไม่ลบของเดิม ตามธรรมเนียมไฟล์นี้) อธิบายว่า default เปลี่ยนไปแล้วและทำไม · ตรวจ JSON valid หลังแก้

สวีตเต็มหลังแก้ทั้งสองข้อ: **`3106 passed, 327 skipped, 4986 subtests, 0 failed`** เขียว(cloud sanity) (3103+3 เทสใหม่)

**(ข) GT-081 supersede (`COO-DECISION 16:45` ข้อ 2)** — เพิ่มกล่อง SUPERSEDED ต่อจากหัวใบ อธิบายทางออกจริง (Columbus→ทะเล→เทียบท่า→รายงานกัปตัน) พร้อมอ้างคำเจ้าของคำต่อคำ · **ไม่ลบ ไม่ย้าย ไม่แก้เนื้อใบเดิมหรือริเดอร์ทั้งสอง** ใบแทนยังไม่มีเลข (รอสาย A/RE มีของจริงตาม COO สั่ง)

**(ค) RE ticket 8 หัวข้อ → 7 ใบจริง (`COO-DECISION 16:45` ข้อ 4 + `16:46` ข้อ ④)** — เปิด `RE-085`-`RE-091` ใน `CLIENT_RE_QUEUE.md` (numbering ตรวจสด: `GT-085`..`091`/`RE-085`..`091` = 0 hit ก่อนจอง): `RE-085` กลไก "กลายเป็นเรือ" · `RE-086` trigger เทียบท่า · `RE-087` packet รายงานกัปตัน · `RE-088` layout `GM_RunGMCommandVital`/`Result` · `RE-089` ความหมายไบต์ `GM_UpdateGMStateVital` · `RE-090` field layout `TeleportVital`/`ForcePos`/`CWarpResult` · `RE-091` chat→GM-command trigger · **หัวข้อที่ 8 (เกาะ↔scene id) ไม่เปิดเป็นใบ RE** เพราะตอบได้จากตารางที่ commit แล้วบนคลาวด์ — ส่ง `pf-static-re` ไปหาแทน (ดูข้อ 5)

**(ง) mob-combat ledger (`COO-DECISION 16:47`)** — รับทราบ ไม่มีงานต้องทำ (ตัวเลือก 1 ที่ chief เสนอเองถูกอนุมัติ per-session พอสำหรับ v4)

### 5. `pf-static-re` — scene-id crosswalk จากตารางคลาวด์ (ปิดคำถามได้จริงบางส่วน โดยไม่ต้องเปิดอิมเมจ)
อ่าน `gamedata/tables/TEXTDATA_TH__SCENE_NAME_TIP.tsv` (331 แถว) + `CONSTDATA_TH__SCENE_NAME.tsv` (271 แถว, sha ตรงกับที่ registry pin) ตรงกันเอง: Port Royal=1, Prison Exile Island=2, Spice Paradise Island=3, Slave Market Island=4, "Ship in the Sea"=17-23, "Ship in the Sky"=24-30 (+ reskin/mission ซ้ำหลายชุด) · **🔴 พบข้อควรระวังสำคัญ:** `world_scene_registry_001.json` เขียนไว้เองว่า `n_ID -> wire scene_id` เป็น **"CANDIDATE, NOT ESTABLISHED"** พิสูจน์แล้วแค่แถว 1-2 — id อื่นทั้งหมดในตารางนี้ (รวมช่วงทะเล/เกาะ) **ยังไม่พิสูจน์เป็น wire scene_id จริง** จนกว่า `RE-090` จะปิด บันทึกไว้เป็นกล่องอ้างอิงในหัว `CLIENT_RE_QUEUE.md` ก่อน `RE-085` ผลเต็มอยู่ในรายงาน agent (ไม่ commit แยก เพราะเป็นข้อมูลอ้างอิง ไม่ใช่โค้ด/pin ใหม่)

### 6. WIRED audit — ตรวจสดใหม่ทั้งหมด แก้ discrepancy ที่พบ
map 10 เลน `production_allowed` ของ `ORG-AUDIT 15:00` เข้ากับโมดูลจริงทีละคู่ แล้ว grep `runtime.py`+`app.py` แยกทีละตัว (ไม่รวมมัด):

| เลน (10 ใบตาม ORG-AUDIT) | โมดูล | wired? |
|---|---|---|
| combat_aggro | `mob_aggro.py` | ❌ 0 |
| combat_death | `mob_death.py` | ✅ 1 |
| combat_first_hit | `mob_combat.py` | ✅ 1 (R177) |
| combat_loot | `mob_loot.py` | ❌ 0 |
| combat_pickup | `mob_pickup.py` | ❌ 0 |
| field_mobs_hostile | `field_mobs.py` | ✅ 1 |
| world_population_full | `world_population.py` | ✅ 1 |
| world_scene_density | `world_density.py` | ❌ 0 |
| world_scene_registry | `world_scene_entry.py` | ✅ 1 |
| world_travel_gates | `world_travel_gate.py` | ✅ 1 (แต่ **inert by default** ตั้งแต่รอบนี้ — ดูข้อ 4ก) |

**`WIRED = 6/10`** 🔴 **ไม่ตรงกับที่ R177 รายงานว่า `4→7/10`** — ตรวจแล้วพบว่า R177 นับ raw import statement ของ `runtime.py` (7 ตัว: `field_mobs`, `mob_combat`, `mob_death`, `world_population`, `world_scene_entry`, `world_scene_travel`, `world_travel_gate`) โดย `world_scene_travel` เป็น helper เคลื่อนฉากที่ไม่ตรงกับเลนใดใน 10 ใบของ `ORG-AUDIT` แบบ 1:1 (มันไม่ใช่ scenario `production_allowed` ของตัวเอง) — ทำให้ตัวเลขพองขึ้นหนึ่งหน่วย เสนอ COO: **ยืนยันนิยาม "WIRED" ให้ตรงกันทั้งโปรเจกต์** (map 1:1 กับ 10 เลนที่ ORG-AUDIT ตั้งไว้ ไม่ใช่ raw import count) มิฉะนั้นกฎ "ไม่ขยับ 2 รอบติด = escalation" จะเทียบเลขกันคนละความหมาย

**WIRED = 6/10** (ไม่ขยับจาก R177's ตัวเลขที่แท้จริง 6/10 ถ้านับด้วยวิธีเดียวกันนี้ย้อนหลัง — ยังไม่มี escalation เพราะเลนใหม่ที่ยังไม่ wire คือ combat_aggro/combat_loot/combat_pickup/world_scene_density ซึ่งไม่มีของใหม่ที่ chief ทำเองรอบนี้ที่ยังไม่ต่อสาย — ไม่มี CORE-REQUEST ค้างจากสาย A/B ในกล่องจดหมายรอบนี้สำหรับ 4 เลนนั้น)

## nonclaims
① ผล `pf-static-re` (ข้อ 5) เป็นข้อมูลระดับ data-table เท่านั้น ไม่พิสูจน์กลไก "กลายเป็นเรือ"/dock/รายงานกัปตัน ② การแก้ `travel_gate` (ข้อ 4ก) ไม่เปลี่ยนพฤติกรรมที่ผู้เล่นเห็น เพราะเลนนี้ยังไม่เคยถูกอนุมัติให้เป็นเกณฑ์ M2 อยู่แล้วตั้งแต่ R176 (v6 prompt เพิ่งบอกว่า "แก้แล้ว" ผิด — ดู CORRECTION ด้านบน) — นี่คือการทำให้โค้ด "ปิดแน่นอน" ตรงตามคำสั่ง COO ไม่ใช่การถอดฟีเจอร์ที่เคยใช้งานจริง ③ RE-085-091 ยังไม่มีผล เป็นใบเปิดรอ RE runner บนสะพาน ④ WIRED audit ข้อ 6 เป็นการนับใหม่ ไม่ใช่การกล่าวหาว่า R177 โกหก — ต่างกันที่นิยาม ต้องให้ COO ชี้ขาด

## ค้าง / ส่งต่อ
- นิยาม `WIRED` ที่ตรงกัน — เขียน `CHIEF-ASK-COO` แยกถ้า COO ไม่ตอบในรอบถัดไปเอง
- `GT-081` ใบแทนยังไม่มีเลข (ตาม COO สั่งไว้ตรง ๆ ว่ายังไม่ใช่ตอนนี้)
- `CHIEF_CONTINUATION.md` ใกล้ ~117KB ต่อจาก R177 ที่บอกไว้แล้วว่าใกล้ archive — ยังไม่ทำรอบนี้ (ไม่ใช่ blocker)
