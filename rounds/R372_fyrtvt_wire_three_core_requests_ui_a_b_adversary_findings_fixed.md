[LANE-E] round `fyrtvt` · start 2026-09-06T15:22+07:00 · claim (unlocked)

# R372 — CORE-REQUEST 3 ใบ (UI `2006` · A `0914` · B `1952`) wired + pf-adversary fixed 2 findings

## รอบนี้ขยับ NOW/M ข้อไหน
- ขยับข้อ "รอเครื่องคุณ" ข้อ 3 (`GT-276`/ใบ faction ของ A — คนละก้อน แต่**พื้นที่ที่ปล่อยของ A `0914` ปูทางให้ GT ที่ค้างกันมาตั้งแต่ R354** เข้าใกล้เกณฑ์: "ฆ่ามอน 1 → ของตก 2 → เซสชันที่สอง/relogin เห็นของ 2 ที่เดิม" ยังต้องรอ merge)
- ขยับ M4 ทางอ้อม: `mob_respawn` wired = โครงกระดูกสุดท้ายของ "เกิดใหม่" (M4 ข้อ 4) อยู่บน main แล้ว (รอ gate/merge) — ยังไม่ผ่าน M4 เอง เพราะสามข้ออื่นของ M4 (ตีกลับ HP ลดจริง/ตายถูกต้อง/ศพไม่ค้าง) ยังไม่ครบ
- ไม่ขยับ M2/M3/DB-arm(ข)/UI-A — คนละก้อนคนละสาย (M2 บล็อกที่เครื่อง Panya, DB arm(ข) บล็อกที่ RE `1449` ไม่ใช่ที่ chief)
- ทำไมไม่ขยับ DB `1452` (เพิ่มมาเป็นข้อ 4 ใน COO-DECISION `1546` หลังรอบนี้ล็อกไปแล้ว): บล็อกจริงตามใบของ LANE-DB เอง — RE-TICKET `20260906_1449` (ความหมาย bit "สวมอาวุธ") ยังไม่มีคำตอบ + `store.equip_item` ยังไม่ merge ขึ้น main · ใบ LANE-DB เองเขียนไว้ตรง ๆ ว่า "ไม่ใช่คำสั่งให้ทำตอนนี้ถ้าคิวยังแน่น" · COO-DECISION `1549` (หลังรอบนี้เช่นกัน) ยืนยันตรงกันว่า arm(ข) ยังติด RE

## 1. สามจุดเสียบ (pirate-force-server PR `#931`, branch `claude/keen-pasteur-fyrtvt`)
| CORE-REQUEST | จุดเสียบ | ผล |
|---|---|---|
| LANE-UI `20260905_2006` | `runtime.py`, กิ่ง `elif nested_id == LOGOUT_VITAL_ID:` ก่อน `try: world_logout_button_notice.observe_parsed` | คลิก Exit Game จริง (subcode 1, ไม่มี scenario, มีตัวละครที่เลือก) เรียก `ui_logout_exit_game.dispatch_real_exit_game_logout` → ปิด session จริง (ack + close_connection + socket teardown timer) แทนโน้ตปฏิเสธเฉย ๆ |
| LANE-A `20260906_0914` | `mob_scene_recompose.ground_companion_actions(...)` call site (~5437) | เพิ่ม `world=mob_ground_persistence.world_ground()` — เซสชันที่สอง/relogin ฉากเดียวกันเห็นของที่คนอื่นฆ่าทิ้งไว้ |
| LANE-B `20260905_1952` | `_sync_combat_scene_state`, บล็อก `if folder != self.mob_combat_scene_folder:` | สามแก้ (sweep local → loop เปลี่ยนตัววน → field assign หลัง atomic block) = มอนที่ตายกลับมาเกิดใหม่หลัง delay (`RESPAWN_DELAY_SECONDS`, ค่า 120s ยังเป็นสมมติของ B รอ COO) |

ทั้งสามใบก๊อปโค้ดจาก `*_WIRING` constant ของแต่ละโมดูลตรงตัว ไม่มีการตีความเพิ่ม

## 2. pf-adversary (isolated worktree, 1 ครั้ง — ไม่เกิน 2 ตามกฎ) — 2 finding ที่ต้องแก้ก่อน push
1. **แก้แล้ว (HIGH ตอนพบ, ก่อนรอบนี้แก้ full-suite เอง)**: `test_mob_scene_recompose_ground_companion.py::WorldGroundCompanionWiringTests` pinned negative ยังไม่ flip — พบและแก้ก่อน adversary คืนผลด้วยซ้ำ (จาก full-suite run รอบแรก) ไม่ใช่ของ adversary
2. **แก้แล้ว (MEDIUM-HIGH)**: early return ของ UI wiring ข้ามช่องโหว่ frame-หลังปิดจริง — guard เดิม (`logout_hypothesis_scenario is not None and self.logout_acknowledged: return []`) คุ้มครองแค่เส้น scenario ไม่คุ้มครองเส้นปิดจริงใหม่ → เติม mirror guard (`logout_hypothesis_scenario is None and self.logout_acknowledged: return []`) ข้าง ๆ ของเดิม + เทสใหม่ `test_a_later_frame_after_the_real_exit_is_refused_not_processed`
3. **ตรวจแล้ว ปล่อยไว้ (MEDIUM-HIGH เชิงกลไก, ไม่ใช่บั๊กใหม่)**: early return เดียวกันข้าม P-1 PICKUP block (~8155, ไม่ gate ด้วย `nested_id`) ด้วย — ถ้าเฟรมเดียวมี LogoutVital (นำ) + PickupRequestVital (แถม) ปนกัน pickup จะหาย **แต่** `TRACE_PATH_REQ_VITAL_ID` ก็ return ก่อนถึงจุดเดียวกันนี้อยู่แล้วบน main (ของเดิม ไม่ใช่รอบนี้สร้าง) = พฤติกรรมประเภทนี้มีมาก่อนแล้วสำหรับ vital อื่นอย่างน้อยหนึ่งตัว ไม่ใช่ครั้งแรก · ไม่มี capture ยืนยันว่า client จริง batch สองปุ่มนี้ในเฟรมเดียวกัน — **ฝากถาม LANE-UI/LANE-B/COO** ว่าจะยอมรับ trade-off นี้ต่อไปหรือให้ออกแบบใหม่ (ต้องมี capture ก่อนถึงจะออกแบบถูก)
4. **วัดแล้ว (LOW)**: ต้นทุนของ LANE-A ที่ยังไม่มีใครวัด (จดหมายเองบอกไว้) — adversary วัด `WorldGround.standing()` เดี่ยว ~26,600 call/s (~35µs/call) · 4 เธรดชนกันคนละฉาก ~19,600 call/s รวม (เทียบ ~106,000 ถ้าไม่ชนกัน) — ชนจริงแต่ต้นทุนสัมบูรณ์เล็ก ที่อัตราตีที่เป็นไปได้จริง ยังไม่วัดใต้บูตจริงหลายเซสชัน
5. **ตรวจแล้ว ผ่าน**: mob_respawn ทั้งสามจุดถูกตำแหน่ง/ลำดับตาม D3/D5 · หนี้เก่า (ไม่ใช่ของรอบนี้): `test_the_order_keeps_the_death_register_inside_the_atomic_block` ไม่ได้เช็คตำแหน่งจริงใน `runtime.py` เอง เช็คแค่ตัว string ใน `MOB_RESPAWN_WIRING` — รอบหน้าที่แตะไฟล์นี้ควรเสริม (ไม่ใช่ blocking รอบนี้)

## 3. เก็บกวาดข้างทาง (เดียวกัน PR, คอมมิตที่สอง, comment-only)
LANE-A (`notes_to_chief/20260906_1546_LANE-A-TO-CHIEF-...md`) ชี้คอมเมนต์ค้างที่ `runtime.py:~9660` หลัง `world_faction_admission` เลิกเช็ค registry (LANE-A round `q02brx`) — แก้แล้ว comment-only ไม่กระทบพฤติกรรม · อีกสามจุด (gm/attr_wire.py, gm/login_mask.py, tests/test_gm_attr_wire.py — เขต LANE-GM) forward ให้ LANE-GM · จุดที่สี่ (`live_named_attr_values.py`) เจ้าของไม่ชัด — **ฝาก COO ชี้เจ้าของ**

## 4. หลักฐาน
- Full suite (สองรอบ, หลังแก้ adversary finding): **12353 passed, 369 skipped, 25180 subtests passed, 0 failed** (403.83s) บน commit `51255a6`
- `pf_gate_preflight.py --repo pirate-force-server`: PASS (ทั้งสองรอบตรวจ)
- `ast.parse` ยืนยัน syntax ทุกครั้งที่แก้
- PR `pirate-force-server#931` เปิดแล้ว ไม่ draft · `PF-AUTOMERGE: v4` ยืนยันด้วย GET แล้ว

## 5. nonclaims
1. ไม่มีการบูตสด client จริงรอบนี้ — ทุกอย่างพิสูจน์ headless
2. LANE-UI nonclaim เดิมยังยืน: ไม่รู้ client ทำอะไรจริงหลัง FIN
3. LANE-A ต้นทุนวัดที่ระดับ RLock/scan เท่านั้น ไม่ใช่ใต้บูตจริงหลายเซสชัน
4. finding #3 ของ adversary (PICKUP ปนเฟรม) ไม่ได้แก้ — บันทึกเป็นคำถามค้างให้ COO/LANE-UI/LANE-B ไม่ใช่เดาทิ้งไว้

## 5.5 CHIEF_CONTINUATION.md — จงใจไม่แตะรอบนี้
ไฟล์อยู่ที่ 34,841 ไบต์ (เพดาน 30,720) อยู่แล้วก่อนรอบนี้เริ่ม (`old`, pre-existing debt ตาม preflight) — เติมบรรทัดดัชนีของรอบนี้จะทำให้ "over ceiling AND grown vs origin/main" = แดงของกิ่งนี้ทันที (`tools_bridge/pf_gate_preflight.py` เกณฑ์ข้อ 169) จึงจงใจไม่แตะไฟล์นี้เลยรอบนี้ · ต้นเหตุที่แท้จริงคือ R370/R371 ถูกจดเป็นย่อหน้าเต็ม (ผิดกฎ §4 "บรรทัดเดียวต่อท้าย") แทนที่จะเป็นดัชนีบรรทัดเดียว — รอบหน้าควรบีบ R370/R371 ให้เหลือบรรทัดเดียวต่อรอบ (ย้ายเนื้อเต็มไป archive เหมือน R361-R369) ก่อนจะเติมดัชนีของ R372 ได้อย่างปลอดภัย

## 6. งานที่ค้าง (ไม่ใช่ของรอบนี้ แต่ต้องนับ)
- DB `1452` (op=5 สวมอาวุธ): บล็อกจริงที่ RE `1449` — chief พร้อมต่อสายทันทีที่ RE ตอบ (ขนาดงานเท่าจุดเสียบ op=4 ที่มีอยู่แล้ว)
- COO-DECISION `1546` ข้อ 2 (PR(0): เพดานไฟล์ 2,400,000/409,600 ไบต์ + `.gitignore` `!/tickets/`): รอบหน้าของ chief
- COO-DECISION `1546` ข้อ 4(3): §7 ก้อนเดียว +2 บรรทัดใหม่ (เพดานต่อใบ 8,192 B + เพดานคิวใหม่): รอบหน้า
- adversary finding #3 (PICKUP/LOGOUT batching): ต้องการ capture จริงหรือคำตัดสิน COO ก่อนออกแบบต่อ
- `test_the_order_keeps_the_death_register_inside_the_atomic_block` ควรเสริมให้เช็คตำแหน่งจริงใน `runtime.py` ไม่ใช่แค่ string ของ wiring text (หนี้เก่า ไม่ใช่ blocking)

WIRED = 3 โมดูลที่มี emission จริงบน production path (`ui_logout_exit_game`, `mob_scene_recompose.world=` merge, `mob_respawn`) / เลนที่ `production_allowed=True` ทั้งสาม ไม่มีแฟล็ก
TWO_SESSIONS_SAME_SCENE: LANE-A's world= wiring คือคำตอบของ TWO_SESSIONS_SAME_SCENE โดยตรง (ground loot แชร์ผ่าน world registry) · LANE-B's respawn sweep เขียนแค่ field ของเซสชันตัวเอง (`self.mob_death_register`) — ยังไม่แชร์ข้ามเซสชัน (หนี้ที่ `world_scene_registry`'s WORLD_REGISTRY_SEED_WIRING จะปิดเมื่อ paste)
KNOWN_RED_MAIN: 2 แถวเดิม (skip_census pin drift Q #891 · bridgesize) — รอบนี้ไม่แตะไฟล์คิว ไม่กระทบ
QUEUE_TRIAGE: ไม่แตะ `GAME_TEST_QUEUE.md` รอบนี้ (LANE-K ถือไฟล์คิวตาม NOW.md ปัจจุบัน) · เกิน 6 ชม.จากรอบกวาดล่าสุดหรือไม่ไม่ได้ตรวจ — รอบหน้าของ chief ตรวจถ้ายังไม่มีใครทำ
READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ: ไม่มีเพิ่มจากรอบนี้ (chief ไม่แตะคิว)
ADVERSARY_PAID pf_bridge (ไม่มีเลข PR bridge รอบนี้ — ผลจ่ายในคอมมิต pirate-force-server#931 ตามข้างบน)

SCOREBOARD: COMING | Exit Game ตอนนี้ปิด session จริง (ไม่ใช่แค่ปฏิเสธเฉย ๆ) และของพื้นที่คนอื่นฆ่าทิ้งไว้จะไม่หายเปล่าเมื่อเซสชันอื่น/relogin เข้ามาดู และมอนที่ตายจะเกิดใหม่ได้ — ทั้งสามยังรอ merge (PR pirate-force-server#931, PF-AUTOMERGE: v4) ก่อนถึงมือผู้เล่นจริง | pirate-force-server#931 (full suite 12353 passed/0 failed/369 skipped/25180 subtests, pf_gate_preflight PASS, pf-adversary reviewed + 2 findings fixed + 1 documented)

-- LANE-E (chief), round `fyrtvt`
