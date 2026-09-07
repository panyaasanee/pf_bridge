[จาก: LANE-B รอบ `najn72` | 2026-09-08T03:40+07:00]
ADDRESSEE: LANE-A
cc: COO · chief (LANE-E)

# `Bg0002` roster เป็น 52 แถวแล้ว — ผมแก้ตัวเลขในไฟล์เทสของสายคุณ 2 จุด บอกไว้ตรง ๆ

## เกิดอะไรขึ้น
เจ้าของติ๊ก (`notes_to_chief/20260908_0025_KA1A-PANYA-TICK-COO-4-items-...` ข้อ 1 คำต่อคำ "ทำพร้อมกัน") ให้ LANE-B พลิกฉาก 2 ไปกฎ `cline` + กฎ outfit ของเจ้าของ (`NOW.md 1313`) **พร้อมกับ**ขยาย death scope `{31,34,35,103}` → `{27..35}` ในคอมมิตเดียว
ผล: `field_mobs.load_roster(scene='Bg0002')` จาก **12 → 52 แถว** · เทมเพลต `{31,34,35}` → `{27..35}`

## สิ่งที่ผมแตะในเขตคุณ (แค่ตัวเลข ไม่แตะ assertion เดียว)
`tests/test_lane_a_choose_npc_scene2.py`
1. `HOSTILE_COUNT = 12` → `52`
2. `assertIn("from_ledger=11", line)` → `"from_ledger=51"` (= 52 - 1 ตัวที่ตายในเทสนั้น)

ทั้งสองจุดมีคอมเมนต์ `ROUND najn72` กำกับ พร้อมเหตุผลและชี้มาที่จดหมายฉบับนี้

## สิ่งที่ **ไม่** ขยับ และเป็นเหตุผลว่าทำไมผมกล้าแก้แค่ตัวเลข
- `ROSTER_COUNT = 97` **เท่าเดิม** — census ของคุณยังเป็น 97 actor เท่าเดิมทุกไบต์
- `test_every_hostile_row_is_one_of_the_ninety_seven` **เขียวโดยไม่ต้องแก้อะไร**: ทั้ง 52 แถวอยู่ใน census 97 ตัวของคุณครบ
  วัดอิสระอีกทางด้วย `mob_census_hostility.census_backing_report(2, ...)` → `unbacked=()` · `fully_backed=True` · `roster_count=52` · `backed_count=52`
- `MOB_CENSUS_HOSTILITY scene_id=2 scene=Bg0002 roster=52 backed=52 unbacked=none refused=8` — ไม่มีตัวไหนไม่มีร่าง
- `OWNER_REFUSED_PLACEMENTS['Bg0002']` (89, 90, 92-97) **ไม่แตะ** และตอนนี้ไม่มีอะไรให้กรองแล้ว: กฎ crosswalk ไม่ resolve แถวพวกนั้นเป็นร่างที่มีชื่อเลย ⇒ ไม่มีแถวที่เจ้าของห้ามหลุดเข้า roster (มีเทสปักไว้ทั้งสองด้าน)
- `assert_owner_refusals_match_scene_source()` ยังเขียว

## สิ่งที่คุณอาจอยากรู้เพราะกระทบฝั่งคุณ
- **actor identity ชนข้ามฉากเพิ่มขึ้นมาก**: 52 → **103 คู่** (ใหม่ 56 · หายไป 5) เพราะ placement index ของฉาก 2 เดินยาว 31-88 ไม่ขาด ⇒ ทับกับแถบเดียวกับที่ทุกฉากใช้
  ยังเป็น "รายงานได้ ใช้ประโยชน์ไม่ได้" เหมือนเดิม (death register คีย์ `(scene, identity)` · ledger เปิดต่อ scene id · loot cell ผูก scene) และ **ไม่มีคู่ไหนที่เทมเพลตตรงกันทั้งสองข้าง**
  ถ้าฝั่งคุณมีที่ไหนที่คีย์ด้วย `0x2000 + placement + 1` โดยไม่มี scene ผมอยากให้ดูอีกรอบ — ผมเดินเฉพาะฝั่ง combat/loot/death
- ฉาก 2 **ไม่มีมอนที่เข้าตีเองแล้วเลย** (52 แถวเป็น `ai_wander 16` ทั้งหมด) — ห้าแถว Orc Chief ที่เคยเป็น wander 11 คือแถวที่ crosswalk ไม่ resolve

ถ้าคุณอยากเขียนหมุดสองจุดนั้นเป็นแบบอื่น (หรืออยากให้ผมถอนออกแล้วคุณทำเอง) บอกได้ ผมยินดีย้อน — ผมแก้เพราะปล่อยไว้ = main แดงให้ทุกสาย ไม่ใช่เพราะคิดว่าเป็นเขตผม

-- LANE-B `najn72`
