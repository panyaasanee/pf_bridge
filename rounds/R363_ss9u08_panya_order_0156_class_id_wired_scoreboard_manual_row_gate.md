[LANE-E] round `ss9u08` (R363) · เริ่ม 2026-09-06T03:49+07:00 · claim: `pf_bridge#1421`
list `[LANE-E]` ตอนเริ่ม = ไม่มีใบเปิด (ใบอื่นที่เปิดอยู่เป็นของสายอื่น: `#1420` LANE-UI, `#1414` LANE-GM) — ไม่มี takeover

# 1. ลำดับที่ทำจริง (อ้างอิงข้อ 3 ของ `AGENTS.md` §17 — CORE-REQUEST มาก่อนคิวเดิม)

1. อ่าน `NOW.md` → พบ 🔴 **PANYA-ORDER `0155`/`0156` เดดไลน์ 14:00** เป็นข้อบังคับแรก
2. บริโภคจดหมายที่ถึงตัวเอง/cc: `20260906_0242_LANE-DB-TO-COO-*` (ตรวจแล้วว่าไม่ใช่ของ chief โดยตรง — ADDRESSEE: COO — ไม่ stub) → นำไปสู่ `20260906_0315_KA1B-TO-CHIEF-*` (ADDRESSEE: chief จริง) → ชี้ตรงไปที่ `20260905_2242_LANE-B-CORE-REQUEST-*` ที่ค้างมา 5 ชม.กว่า
3. ต่อสาย `CORE-REQUEST 2242` ก่อนงานอื่นทุกอย่าง (ตรงตาม §17 ข้อ 3) — ดูหัวข้อ 2
4. COO-DECISION `20260906_0042` (scoreboard manual-row gate) — งานที่ค้างจาก R362b เอง กำหนดส่ง 04:41 — ดูหัวข้อ 3

# 2. CORE-REQUEST `20260905_2242` — `class_id` ต่อเข้า production pose composer

**ปลด PANYA-ORDER `0156` ทาง (ก)**: `runtime.py:5159` (`_dispatch_mob_combat`) เรียก `make_production_hit_pose_echo`
ไม่เคยส่ง `class_id` เลย → `combat_pose.production_behavior_for_class` ถูกเรียกด้วย `None` เสมอ → เส้นทาง
production (`COO-DECISION 20260905_1045`) เป็นโค้ดตายมาตลอด ทั้งที่ทุกจุดอื่นในห่วงโซ่ (class_id resolver ·
login reader · crosswalk `combat_pose.py`) สร้างเสร็จและเทสเขียวแล้ว (ยืนยันจากใบ `20260906_0242` ของ LANE-DB)

**ตัวแก้**: หนึ่งบรรทัด `class_id=selected.class_id` — `selected` คือ `Character` ตัวเดียวกับที่ผูก `performer`
สามบรรทัดเหนือจุดเรียก (ยัง in scope ไม่มี reassignment คั่น — ตรวจอ่านทั้งเมธอด `_dispatch_mob_combat` บรรทัด
4948-5187 เอง) · `Character.class_id: int | None = None` (model.py:88)

**วัดจริง**: บูตไร้แฟล็ก ตัวละคร Gladiator (class_id=1, จาก `_V25_REAL_CREATE_PC`) ตี mob ได้ frame
`MOB_COMBAT_POSE_TRIAL` จริง (`BEHAVIOR 280` ดาบฟัน — ตัวเดียวกับที่ `GT-247`/R315 ยืนยันบนจอ) นำหน้า
announce/bar โดยไม่มี `PF_POSE_TRIAL` เลย — เทสใหม่ `test_production_class_id_reaches_the_composer` พิสูจน์
end-to-end พร้อมยืนยัน `class_id=1` จริงก่อนอ่านผล (ไม่เดา)

**ไม่รับข้อ 2 ของใบ (ตัวนับ provenance)**: `make_production_hit_pose_echo` มีแค่ `class_id=None, environ=None`
วันนี้ ไม่มีพารามิเตอร์รับตัวนับที่ใบขอ · `action_ack.py` เป็นเขต LANE-B ไม่ใช่ของ chief · ยัด kwarg ที่ไม่มี
= `TypeError` ทุกหมัด ใต้ `game_listener` แบบ frozen ไม่มี except handler (interlock X07 — วัดจากการอ่าน
ทั้งเมธอดจริง ไม่มี try/except คั่น) = accept loop ตายทั้ง session · ส่งกลับเป็น CORE-REQUEST ใหม่ให้ LANE-B
รอบหน้าถ้าต้องการ ดูจดหมาย `20260906_0350_CHIEF-REPLY-*`

## 2b. ผลข้างเคียงที่ pf-adversary จับได้จริง (D1, ยืนยันแล้ว, ร้ายแรง) — แก้ครบก่อน push

`_V25_REAL_CREATE_PC` (harness ทดสอบ) resolve เป็น `class_id=1` เสมอ ⇒ **ทุกไฟล์เทสที่สร้างตัวละครจริงแล้ว
ตีจริงผ่าน `_dispatch_mob_combat`** ได้ frame `MOB_COMBAT_POSE_TRIAL` แทรกหน้า assertion เดิม
รอบแรกผมแก้แค่ 2 ไฟล์ (`test_pose_trial_production_hit_wiring.py`, `test_mob_combat_dispatch.py`) แล้วรายงานว่า
"ครบแล้ว" — **pf-adversary รอบแรกจับผิดตรงนี้**: รันชุดเต็มจริงแล้วเจอ **21 แดง ใน 7 ไฟล์อื่นที่ผมไม่ได้แตะ**
(`test_diag_multi_object_runtime_wiring.py` · `test_mob_combat_cadence_wiring.py` ·
`test_mob_combat_census_wiring.py` · `test_mob_combat_membership_wiring.py` ·
`test_mob_scene_recompose_wiring.py` · `test_scene_scoped_combat_wiring.py` ·
`test_world_wipe_headless_proof.py`) — ไฟล์เหล่านี้แต่ละไฟล์มี `_state()`-เทียบเท่าของตัวเองแยกกัน ไม่มีจุดกลาง
แก้ครบทั้ง 7 ไฟล์แล้ว (เคลียร์ `class_id` กลับเป็น `None` หลังสร้างตัวละคร — 2 ไฟล์ต้องย้ายจุดแก้ไปหลัง
`_start_game()` เพราะ `state.foundation.selected` ยังเป็น `None` ตอนสร้างตัวละคร ไม่ใช่หลังนั้น — เจอจาก
`TypeError: obj=None` ตอนรันจริง ไม่ใช่เดา) · ชุดเต็มรอบสุดท้าย (บนต้นไม้ merge origin/main แล้ว):
**11603 passed, 356 skipped, 0 failed** (รันสองครั้ง ก่อน/หลัง merge — merge origin/main ดึงมา 21 ไฟล์ไม่เกี่ยว
ไม่มี conflict) · `verify_hypothesis_ledger.py`/`verify_functional_coverage.py` PASS ไม่มี drift

แก้ docstring ที่ `action_ack.py:262-268` ที่ pf-adversary ชี้ว่าจะเท็จทันทีที่ใบนี้ landed (เขียนว่า
"class_id IS None ON EVERY HIT TODAY" — ไม่จริงอีกต่อไปหลัง merge)

**ADVERSARY_PENDING `pirate-force-server#883`**: สั่งรอบสองแล้วต้นรอบก่อน push (ยืนยันตัวแก้ 7 ไฟล์ + ตัวแก้
docstring) — ยังไม่คืนผลตอน push (สูงสุด 2 ครั้ง/รอบใช้ไปแล้ว 1 ครั้งที่พบ D1 ข้างบน) ผลรอบสองจะจ่ายเป็น
addendum ใต้รหัสรอบเดียวกันถ้าคืนก่อนจบเซสชัน ไม่งั้นรอบหน้ารับช่วง

**PR**: `pirate-force-server#883` — **draft** (แตะเฟรมที่ส่งไคลเอนต์ ตามกฎ §17 ข้อ 2 ต้อง draft จนกว่า adversary
คืน) · ชุดเต็มเขียว preflight PASS ยกเว้น bridgesize (ดูข้อ 4) · ขนาด 11 ไฟล์ (เกิน ~6 ไฟล์/ใบตามปกติ — เป็น
เรื่องเดียวที่แยกไม่ได้จริง: การแก้ 9 ไฟล์เทสเป็นผลบังคับของบรรทัดเดียวในข้อ 3 ไม่ใช่งานคนละเรื่อง แยกใบจะทำให้
มีใบหนึ่งที่ทำให้ชุดเต็มแดงเสมอ)

**GT-271 จองเลข** ให้ LANE-B/LANE-CS เติมเนื้อใบเอง (ตามที่ LANE-DB ขอ ข้อ 4 ในใบ `0242` — chief ไม่ใช่เจ้าของ
โมดูล ไม่เขียนเนื้อใบเอง) เกณฑ์ที่เสนอไว้ในจดหมายตอบ

# 3. COO-DECISION `20260906_0042` — scoreboard manual-row gate (กำหนดส่ง 04:41, ทำก่อนกำหนด)

`tools_bridge/pf_scoreboard.py`: คอลัมน์ 6 (วันที่) ทั้งแถว derive (stamp จาก commit time ของ `rounds/*.md`
ผ่าน `format_bangkok_date`) และแถว manual (ผู้เขียนใส่เอง) · แถว manual สถานะ DONE ที่ขาดวันที่ หรือขาด
`GT-<เลข>` ในฟิลด์ประโยค/หลักฐาน → ขึ้น `MALFORMED` (ไม่ลบ ไม่ลดสถานะเงียบ ๆ) · แถว seed เดิมของ ka1-A
(`2043`, จบด้วยวันที่แทนคำว่า `manual`) อ่าน/เขียนกลับคำต่อคำเหมือนเดิมตามที่ COO สั่ง "ผ่านตามรูปเดิม" · หัว
TSV แก้ข้อความระบุผู้เขียนแถว manual · self-test 30 → 38 เคส ผ่านหมด

`tools_bridge/pf_gate_preflight.py`: เช็คใหม่ `check_scoreboard_manual_rows()` — RED เมื่อกิ่งนี้เพิ่ม/แก้/ลบ
แถว `manual` ใน `SCOREBOARD_FACTS.tsv` เทียบ `origin/main` (เทียบทั้งบรรทัดดิบ ไม่ใช่แค่ฟิลด์เดียว) เว้นแต่ส่ง
`--allow-manual-scoreboard-edit` (สำหรับ courier PR ของ Panya/ka1-A เท่านั้น) · self-test ใหม่ 8 เคส (39 รวม
— 2 เคสแดงเดิมของ `_branchname_self_test_cases` เป็น environment flakiness ไม่เกี่ยวกับรอบนี้ ยืนยันแล้วว่า
เกิดบน `origin/main` ที่ไม่ได้แตะเช่นกัน)

`AGENTS.md` §7: เติมหนึ่งบรรทัดตามที่ COO สั่ง (นับไบต์ตาม `2352`) 🔴 **44161 → 44628 ไบต์ — ไฟล์นี้เกิน
เพดาน 30,720 ไบต์อยู่แล้วเป็นหนี้เก่า (COO-DECISION `20260905_2352` ยืนยันหน่วยเป็นไบต์และให้เกต
regression-only ปล่อยผ่านหนี้เก่าได้) การเติมบรรทัดนี้ทำให้ `pf_gate_preflight.py` รายงาน `AGENTS.md` เป็น RED
สำหรับกิ่งนี้โดยเฉพาะ (โตกว่า base) — ไม่ได้ซ่อน เขียนตรงนี้ตามจริง · ไม่มี CI ใดรัน preflight นี้จริง (R362b
D11, grep `.github/` = 0 hit) จึงไม่ใช่ตัวบล็อกการ merge จริง แต่เป็นหนี้ที่ต้องแก้ (ย้ายเนื้อหาไป
`HOWTO_*`/`docs/` แบบที่ R360 เคยทำ) — ยกไปรอบที่ทำ `PROMOTION_BACKLOG.md` ตามที่ R362 วางแผนไว้แล้ว (บรรทัด
เดียวกัน ไม่สลับลำดับ)

**Regenerate `SCOREBOARD_FACTS.tsv`/`PLAYER_STATUS.html`**: รันหลังไฟล์รอบนี้เขียนเสร็จ (บรรทัด SCOREBOARD ท้าย
ไฟล์นี้จะถูกเก็บในรอบถัดไปที่รันเครื่องมือ เนื่องจากรันเครื่องมือต้องเห็นไฟล์นี้ commit แล้ว)

# 4. ที่ยังไม่ทำและเหตุผล (ยกมาจาก R362 · ยังไม่ขยับ)

1. `docs/PROMOTION_BACKLOG.md` + หัว `AGENTS.md` หน่วยไบต์ (`2351`/`2352`) — รอบนี้เต็มไปด้วย PANYA-ORDER
   เดดไลน์ + COO-DECISION กำหนดส่งเข้ม จึงเลือกสองงานที่มีเดดไลน์จริงก่อน
2. whitelist ประตูเควส DB (`2353`) — ยังไม่ตรวจซ้ำรอบนี้ (ไม่ใช่งานเร่งของรอบ)
3. `DEATH_SEED_WIRING` · GM-061 per-viewer name colour — ไม่ได้แตะ
4. จดหมาย `0014`/`0015` ของ LANE-B (mob-death hook) — ยังไม่บริโภค (ผูกกับ `DEATH_SEED_WIRING` ตามที่ R362
   วางแผนไว้ ไปด้วยกันรอบหน้า)
5. mirror `pf-adversary.md` สองรีโป (`0130`) — ยังไม่ทำ

# 5. รอบหน้าทำอะไร (เรียง)

1. ผล `ADVERSARY_PENDING` รอบสองของ `#883` — อ่านและจ่ายก่อนงานอื่น (ใบแก้ใต้รหัสรอบ `ss9u08` ถ้าจำเป็น)
2. เมื่อ `#883` ready (ไม่ draft, marker ยืนยัน) → ปลดล็อก claim `#1421`
3. `docs/PROMOTION_BACKLOG.md` + หัว `AGENTS.md` หน่วยไบต์ (ลดหนี้ 44628 ไบต์ลงเข้าใกล้ 30,720)
4. whitelist ประตูเควส DB (เช็คซ้ำว่าโค้ด quest-state ขึ้น main หรือยัง)
5. `DEATH_SEED_WIRING` + จดหมาย `0014`/`0015` ของ LANE-B
6. mirror `pf-adversary.md`

TWO_SESSIONS_SAME_SCENE: `class_id` เป็นฟิลด์บน `Character` ของผู้ตีเอง (ผูกกับ connection/session ของผู้เล่น
คนนั้น ไม่ใช่สถานะโลกที่แชร์ข้าม session) — ไม่กระทบกฎ shared-world/delta · การเปลี่ยนนี้ไม่ได้เขียนอะไรลง world
registry ของ LANE-A

WIRED = `combat_pose.production_behavior_for_class` ถูกเรียกจาก call site จริงใน `runtime.py` แล้ว (observed:
เทสใหม่ยืนยัน class_id=1 จริงก่อนเช็ค behavior_id ที่ได้ ไม่ใช่แค่ named) — ยกเลข WIRED v2 ทั้งชุด (15/67) ไม่
เปลี่ยนรอบนี้ (ไม่ใช่ diff ที่ WIRED v2 นับ เป็น production path ใหม่ที่ยังไม่ได้จัดหมวด)

QUEUE_TRIAGE: ไม่ครบ 6 ชม.จากรอบกวาดล่าสุด (R360 23:02 → รอบนี้ 03:49-04:1x = ~5 ชม. — ยังไม่ถึงกำหนด รอบหน้า
~05:02 ถึงกำหนดจริง)

SCOREBOARD: COMING | ผู้เล่นที่เลือกคลาส Gladiator/Paladin/Sniper/Necromancer ควรตีมอนบนบูตปกติไร้แฟล็กใด ๆ
แล้วเห็นท่าโจมตีตรงกับคลาสจริง (ดาบ/กระบอง/ปืน/ลูกไฟฟ้า) แทนที่จะไม่มีท่าอะไรเลย — วัดแล้วที่ headless dispatch
(ไม่ใช่จอจริง) ยังไม่มี `OBSERVER_CONFIRMED`/GT ยืนยันบนจอ — ต้องรอ PR `#883` พ้น draft+merge แล้วบูต GT-271
ก่อนขึ้น DONE ได้ | pirate-force-server#883 (11603 passed/0 failed, verify_* PASS) · pf_bridge#1421 · เทสใหม่
test_production_class_id_reaches_the_composer (headless, ไม่ใช่หลักฐาน client-observable)

-- chief
