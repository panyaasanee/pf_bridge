# ROUND A_mvuseu 2026-08-28T01:31+07:00 -- LANE-A (WORLD)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
**ไม่มีอะไรบนจอ** -- รอบนี้เป็นรอบกู้งาน + กล่องจดหมายล้วน Prison Exile Island (Bg0002)
ยังส่งไม่ถึงไคลเอนต์บูตไหนเลย (ไม่มี seed path ให้ character row เป็น scene_id=2 -- ของ
chief ตาม M1-P ข้อ 2 ที่ยังไม่เสร็จ)

## บริบทต้นรอบ (protocol A) -- พบปัญหาจริง
ตรวจ PR ล่าสุดของสาย A ทั้งสอง repo ด้วย single-PR GET (ไม่ใช้ list endpoint):
- `pirate-force-server#153` (round `5irwkp`): **state=open, draft=true, merged=false** --
  ยังไม่ถูก reaper ปิด (threshold 6 ชม. ของ repo นี้ยังไม่ถึง)
- `pf_bridge#244` (round `5irwkp`): **state=closed, draft=true, merged=false** -- ถูก
  reaper ปิดไปแล้ว (threshold 2 ชม. ของ repo นี้)

⇒ **งานของรอบ `5irwkp` หลุดจาก main จริง** ตาม protocol A นี่ไม่ใช่รอบเปล่า/ไม่ใช่ของสายอื่น
ล็อกอยู่ -- เป็น draft ค้างของ**รอบก่อนของ LANE-A เอง** ที่ไม่เคยถูกเอาออกจาก draft

### เหตุ (จากคอมมิทที่กู้มา)
`pf_bridge`'s branch เดิม (`claude/quirky-planck-5irwkp`) มีคอมมิทที่สองบันทึกไว้แล้วว่า
`markPullRequestReadyForReview` ผ่าน GraphQL ถูกบล็อกโดย proxy ของเซสชันนั้น
("only the pinned set of PR-review operations is served") และ REST `PATCH draft:false`
รับคำขอแต่ silent no-op (GET ยืนยันซ้ำว่า `draft` ยังเป็น `true`) -- ทั้งสอง PR เลย **ค้าง
draft ตลอดไป** จนกว่า reaper จะปิดแล้วให้รอบถัดไปกู้ตาม protocol A (สภาพที่เกิดขึ้นจริง)

## การกู้ (ทำแล้วรอบนี้)
1. `pirate-force-server`: cherry-pick คอมมิท `eef7400` (`claude/sleepy-ride-5irwkp` ->
   `claude/sleepy-ride-mvuseu`, บน `origin/main` ปัจจุบัน) -- clean, ไม่มี conflict รันเทส
   `tests/test_scene2_prison_exile_tables.py` 17/17 ผ่าน (ตรงกับที่ PR เดิมอ้าง) + full suite
   `pytest tests -q --continue-on-collection-errors`: 3608 passed, 0 FAIL, 17 error เดิม
   (capstone/pefile ไม่ติดตั้งใน sandbox -- baseline เดิมทุกรอบก่อนหน้า) push แล้ว
2. `pf_bridge`: cherry-pick คอมมิททั้งสอง (`0d9f4a8`, `359daf7`) จาก
   `claude/quirky-planck-5irwkp` -> `claude/quirky-planck-mvuseu` -- clean, ไม่มี conflict
3. **แก้เหตุรอบนี้**: session นี้มี GitHub tool (`update_pull_request`, ไม่ใช่ raw
   GraphQL/REST curl) ที่รองรับ field `draft` ตรง ๆ -- ใช้ตัวนี้เอา PR ใหม่ออกจาก draft
   หลัง push แทนวิธี GraphQL/REST curl ที่ session ก่อนลองแล้วไม่ผ่าน (ดูผลจริงในจดหมายสถานะ)

## กล่องจดหมาย (protocol B)
`notes_to_chief/20260827_2305_KA1A-NUDGE-idle-lanes-GM-R3-byte-proof-A-map-window-RE-chief-DIAG-wiring.md`
ถูก LANE-GM บริโภคเฉพาะส่วนของตัวเองไปแล้ว (`.CONSUMED.txt` มีอยู่แล้ว, เขียนชัดว่า "Not
consumed for this session: the KA1A note's 'สาย A' and 'chief' sections") -- ตาม
`notes_to_chief/README.md` (COO-DECISION 00:43, "Known gap") ผู้บริโภครายที่สองของจดหมาย
หลายผู้รับ**ไม่เขียนทับ stub เดิม** บันทึกการบริโภคของตัวเองในรอบนี้แทน:

ส่วน "สาย A" ของจดหมายขอ 3 อย่าง:
1. **เปิดใบ RE ให้ map window/GO! -- ทำแล้ว**: `CLIENT_RE_QUEUE.md` ใบใหม่
   `RE-115 MAPWINDOW-SCENE-NPC-LIST-SOURCE-001` (grep ยืนยัน 115 ว่างก่อนจอง, เลขสูงสุดเดิม
   คือ `GT-114`) ถามว่ารายการ NPC ในหน้าต่างแผนที่มาจาก census packet เดียวกับที่
   `world_population.py`/`world_population_bg0002.py` ส่งอยู่แล้ว หรือเส้นทางอื่น -- ตัวใบ
   7986 ไบต์ (ใต้เพดาน 8 KB ของ addendum v2 ข้อ H)
2. **จับคู่แลนด์มาร์กจากคลิป (ใบ 1240 ข้อ ③) -- เลื่อนออกจากรอบนี้โดยเจตนา, ไม่ใช่ทำแล้วเงียบ**:
   งานนี้ต้องเทียบตำแหน่งวัตถุฉาก (ปืนใหญ่ ม้านั่ง หอกลมไม้ อาคาร Royal Exchange ฯลฯ) ใน
   `bg0001` placement data กับคำอธิบายภาพ 32+ n_ID ในจดหมาย 1240 -- เป็นงานจับคู่ข้อมูลเชิงลึก
   ที่ต้องอ่าน scene object/placement table ทั้งฉากอย่างละเอียดเพื่อไม่ให้จับคู่ผิด (ความเสี่ยง
   สูงถ้ารีบทำในรอบเดียวที่มีงานกู้คืนเป็นหลักอยู่แล้ว) -- ยกให้รอบถัดไปที่ตั้งใจทำเรื่องนี้
   โดยเฉพาะ ไม่นับเป็นรอบเปล่าเพราะรอบนี้มีงานจริงอื่นอยู่แล้ว (กู้คืน + ใบ RE-115 + ตารางด้านล่าง)
3. **เหตุผลรายจุดของ 9 จุด unresolved ใน Bg0002 -- ทำแล้ว** (ดึงจากโค้ดจริง
   `scene2_prison_exile_tables.py`, ไม่ใช่เดา): ดูตารางด้านล่าง

## ตาราง: 9 placement ที่ unresolved ใน Bg0002 (`UNRESOLVED_PLACEMENTS`, `scene2_prison_exile_tables.py`)

| placement_index | n_ID | เหตุผล |
|---:|---:|---|
| 65 | 37 | ไม่มีแถวใน `MOBS` เลย (`no_mobs_row_for_this_n_id_no_body_data`) -- คนละเหตุจาก 8 แถวล่าง |
| 89 | 102 | บล็อก n_ID 101-104: ความหมายไม่ทราบ, เจ้าของสั่งห้ามวาง (`n_id_101_104_block_meaning_unknown_owner_says_do_not_place`) |
| 90 | 101 | เหมือนแถวบน |
| 92 | 103 | เหมือนแถวบน |
| 93 | 103 | เหมือนแถวบน (mm_instance คนละตัว) |
| 94 | 103 | เหมือนแถวบน |
| 95 | 103 | เหมือนแถวบน |
| 96 | 103 | เหมือนแถวบน |
| 97 | 104 | เหมือนแถวบน |

**นับจริง = 8 (บล็อก 101-104) + 1 (n_ID 37) = 9** -- ไม่ใช่ "5 + 4" ตามที่จดหมาย
`20260827_2305_KA1A-NUDGE` เขียน (ตัวเลข "5" นี้ผิดมาตั้งแต่จดหมายเดิม, round `cyp4zt`
รายงานแก้ไว้แล้วครั้งหนึ่งว่า "9 ไม่ resolve ไม่ใช่ 5 ตามจดหมายเดิม" -- โค้ด `UNRESOLVED_COUNT
= 9` คือตัวเลขที่ยืนยันได้จริง, source ใน `scene2_prison_exile_tables.py` บรรทัด 41-45/59-65
มี comment อธิบายเหตุนี้อยู่แล้วก่อนรอบนี้)

## BUILD-001/BUILD-002 -- ไม่เปลี่ยนจากรอบก่อน
BUILD-001 เสร็จแล้ว (ต่อสาย, ไม่มีแฟล็ก), BUILD-002 ยังพักตาม PANYA-DECISION 2026-08-27 20:10
(M1 identity-first ที่ Prison Exile Island มาก่อน)

## nonclaims
- ไม่ได้แตะ `runtime.py`/`app.py`/canonical DB เลยทั้งรอบ ไม่ได้เปิดเกม
- ไม่ได้ปิด anchor เพิ่มจากรอบ `5irwkp` (ยังรอ attended walk ตาม PANYA-DECISION 20:10 ข้อ 4)
- ไม่ได้จับคู่แลนด์มาร์กของใบ 1240 ข้อ ③ รอบนี้ (ดูเหตุผลข้างบน, ตั้งใจเลื่อน ไม่ใช่ลืม)

Companion code PR: `pirate-force-server` (branch `claude/sleepy-ride-mvuseu`, cherry-pick
recovery only, no new code diff beyond the recovered commit)

-- สาย A
