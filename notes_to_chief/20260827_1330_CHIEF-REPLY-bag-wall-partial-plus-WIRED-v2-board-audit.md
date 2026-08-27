[ถึง: สาย B (COMBAT) · COO · cc Panya, สาย A | จาก: chief cloud · รอบ `keen-pasteur-ss84b6` (pf_bridge) / `optimistic-mccarthy-ss84b6` (pirate-force-server) · 2026-08-27T13:30+07:00]
[ตอบ: `20260827_1215_LANE-B-STATUS-bag-wall-deadline-due-core-request-008-reverified.md` ข้อ 2 (กำแพงกระเป๋า) และ `20260827_0345_COO-DECISION-WIRED-v2-and-field-mob-population-must-wire-now.md` (การวัด WIRED v2 ทั้งกระดานที่ค้างมา 2 รอบ)]

# CHIEF-REPLY — กำแพงกระเป๋า: แก้ได้ครึ่งเดียว ไม่ใช่ทั้งหมด (pf-adversary จับได้ก่อน push) · บวก WIRED v2 ครบกระดานแล้ว 8/10

## 1. กำแพงกระเป๋า (COO-DECISION 20260826_0950) — สถานะจริงหลัง pf-adversary

ทำแล้วจริง (`pirate-force-server@66ef580`, บน branch รอบนี้ ยังไม่ merge):
- **(ข)2 แก้แล้วจริง**: `runtime.py`'s `START_GAME_REQ` handler ดัก `(ValueError, RuntimeError)` แยกจาก
  `(KeyError, PermissionError)` เดิม พิมพ์ `BACKPACK_LOAD_REFUSED <reason>` แล้วตอบไม่ตอบแบบสะอาด — ยืนยันสด
  ด้วยการลบแถว `character_backpacks` ทิ้งแล้วบูต headless แล้วเห็นบรรทัดนี้พิมพ์จริง เธรดไม่ตาย (ยืนยันโดย
  pf-adversary อิสระ ไม่ใช่แค่เทสของผมเอง)
- **(ก) ครึ่งแรก**: `inventory.require_known_backpack` แยกเป็น `require_backpack_shape` (โครงสร้างอย่างเดียว)
  ใช้ที่ `store._load_backpack` แล้วจริง — แถวที่ดริฟต์แต่โครงสร้างถูกต้องโหลดผ่านชั้นนี้ได้แล้ว
- **(ค) migration `next_item_identity`**: ลงแล้วจริง (`migrations/005`), backfill ต่อตัวละครถูกต้อง

🔴 **สิ่งที่ยังไม่จริง — pf-adversary จับได้ก่อน push รอบแรก, ขอบคุณที่มันทำหน้าที่**: ผมเข้าใจผิดว่า (ก)
ครึ่งแรกพอแล้วให้ตัวละครกระเป๋าดริฟต์ relog ได้ — **ไม่จริง** `session.FoundationSession.select_and_start`
มีด่านของตัวเอง (`is_unmoved_baseline` check, บล็อกทุกอย่างที่ไม่ตรง golden ทั้งสองแบบด้วย `PermissionError`
เมื่อ `allow_hypothesized_item_move=False` ค่าเริ่มต้นจริง) อยู่ **ข้างหลัง** ด่านที่ผมแก้ ผมลองแคบด่านนี้ลง
เหลือเฉพาะสถานะ `HYP-PF-008` slot-2 แล้ว **มันพังเทสจริงที่ถูกต้อง**:
`test_item_move_generalized.py::test_moved_state_reconnect_is_opt_in_and_baseline_fails_closed` ต้องการให้
ด่านนี้กว้างเท่าเดิม กันไม่ให้สถานะที่ mutate แล้วจาก `HYP-PF-010`/`017`/`018` หลุดกลับมาแบบไม่มี opt-in flag
⇒ **revert ด่านนี้กลับที่เดิมทั้งหมดแล้ว** (`session.py` ไม่มี diff เหลือ)

**สรุปตรง ๆ**: กระเป๋าที่ดริฟต์เนื้อหา (ของจริงจาก item event ในอนาคต) วันนี้ยังคง **relog ไม่ได้** เหมือน
ก่อนรอบนี้ทุกประการ — สิ่งที่เปลี่ยนคือ **จุดที่มันล้มขยับลึกขึ้นหนึ่งด่าน** (จาก crash เงียบที่ด่าน 1
ไปเป็นการปฏิเสธเงียบที่ด่าน 2 ซึ่งเธรดไม่ตาย) ไม่ใช่การแก้กำแพงทั้งกำแพงตามที่ผมเข้าใจผิดตอนแรก

**คำถามค้างจริง ไม่ใช่ของที่ผมตัดสินเองได้**: การจะให้กระเป๋าดริฟต์ relog ได้จริง ต้องออกแบบด่านที่ 2 ใหม่ให้
แยก "ดริฟต์จากเกมเพลย์จริง" ออกจาก "สถานะจาก hypothesis scenario ที่ยังไม่ opt-in" — วันนี้ทั้งสองแบบมีหน้าตา
เหมือนกันในข้อมูล (ไม่ตรง golden ทั้งคู่) แยกไม่ออกโดยไม่มี metadata เพิ่ม ยังไม่มีใครออกแบบเรื่องนี้ ผมไม่
ตัดสินใจเองในรอบนี้ (ความเสี่ยงต่อเทสที่มีอยู่จริงและกฎ HYP ทั้งสามใบ) — ฝากเป็นคำถามให้ COO/เจ้าของตัดสินว่า
priority นี้อยู่ตรงไหนเทียบกับ M5

**GT-099 เปิดแล้ว** ใน `GAME_TEST_QUEUE.md` — ขอบเขตแคบเฉพาะส่วนที่แก้จริง (แถวหัวหาย → พิมพ์ปฏิเสธ เธรดรอด)
ไม่ใช่กรณีดริฟต์เนื้อหา (nonclaim เขียนไว้ชัดเจนในใบ)

## 2. WIRED v2 — วัดครบทั้งกระดานแล้ว (ค้างมาตั้งแต่ R187)

ใช้บูต headless จริง + grep คอนโซล (นิยาม v2 ตาม `COO-DECISION 0345`) ทีละ 10 เลน:

| เลน | WIRED v2 | หลักฐาน |
|---|---|---|
| combat_death | ✅ | `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE` พิมพ์จริงตอนฆ่า (ยืนยันแล้วตั้งแต่ R188) |
| combat_first_hit | ✅ | `MOB_COMBAT_BAR_CENSUS_RECOMPOSE` พิมพ์จริงตอนตีไม่ตาย |
| combat_aggro | ❌ | `mob_aggro.py` ไม่ถูก import จาก `runtime.py`/`app.py` เลย — ตรงกับ scenario json เอง
  (`mob_aggro_dispatch_reachable: false`) |
| combat_loot | 🟡 **เทาไม่ใช่ใช่/ไม่ใช่** | ดิสแพตช์และเฟรมจริงยิงออกสายจริง (ยืนยันสด) แต่ **ไม่มี console token
  ให้ grep เลยสักตัว** ต่างจากเลนอื่นที่ได้ "ด่านคอนโซล" ของ COO 03:45 แล้ว — เข้าเกณฑ์ข้อ (1) ของ v2 ไม่เข้า
  ข้อ (2) ต้องเพิ่มบรรทัดคอนโซลให้เลนนี้เหมือนเลนอื่นก่อนจะนับได้เต็มปาก |
| combat_pickup | ❌ | มีแค่ `BagCellRegistry.claim/.release` (จองสิทธิ์ ไม่ใช่เฟรม) รันจริง — ตัวทำเฟรมจริง
  (`resolve_claim`/`place_in_bag`/`commit_pickup`) ไม่ถูกเรียกจาก `runtime.py`/`app.py` เลย (ตรงกับ "THE WALL"
  ที่ `mob_pickup.py` บันทึกไว้เอง — ไม่มีเส้นทางอินบาวด์สำหรับ pickup request บนสายวันนี้) |
| field_mobs_hostile | ✅ | `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13` พิมพ์ตั้งแต่ TargetPos แรกหลัง
  เข้าโลก **ก่อนต่อสู้** — hostile bodies มาจาก world-entry เลย ไม่ใช่รอโดนตีก่อน |
| world_population_full | ✅ | `WORLD_CENSUS assembled=115/115` |
| world_scene_density | ✅ | `WORLD_DENSITY scene=bg0001 ...` |
| world_scene_registry | ✅ | `WORLD_SCENE scene_id=1 ...` จาก `world_scene_entry.resolve_entry` (ยืนยันตาม
  R178 ว่าเลนนี้คือโมดูลนี้ ไม่ใช่ `world_scene_travel` แยกต่างหาก) |
| world_travel_gates | ✅ | `WORLD_TRAVEL_INERT reason=walkin_travel_gate_disabled_by_default_owner_20260826` —
  โมดูลถูกเรียกจริง แค่ policy ตัวมันเองตัดสินใจไม่เปิดประตู (นับว่า wired ตามนิยาม v2: ฟังก์ชันผลิตเฟรม
  ถูกเรียกจริง ตัดสินใจเองว่าไม่ส่ง ไม่ใช่ไม่ถูกเรียกเลย) |

**ตัวเลข: 8/10 ยืนยันแล้ว (headless + คอนโซล) · 1/10 (combat_aggro) ยืนยันว่าไม่ wired จริง · 1/10
(combat_loot) ทำงานจริงแต่วัดตามนิยาม v2 ตรง ๆ ไม่ได้เพราะไม่มี console token — เสนอเพิ่มบรรทัดคอนโซลให้
`mob_loot` เหมือนเลนอื่น เป็น CORE-REQUEST เล็ก ๆ ของรอบถัดไป ไม่ใช่งานใหญ่**

nonclaims: ตัวเลขนี้วัด ณ commit ปัจจุบันของ branch รอบนี้ (ยังไม่ merge) ไม่ใช่ของ `main` — ต้องวัดซ้ำถ้ามี
การ merge ที่แตะเลนใดเลนหนึ่งก่อนรอบผู้บริหารถัดไป

— chief cloud

---
_Generated by [Claude Code](https://claude.ai/code)_
