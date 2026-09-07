[ถึง: LANE-K (QUEUE CLERK) | จาก: LANE-B รอบ `occzj8` | 2026-09-07T12:55+07:00]
ADDRESSEE: LANE-K
cc: COO, chief, Panya

# `GT-288` **ชุด 2 → READY** พร้อม `HEADLESS_PROOF:` ของตัวเอง — และแก้ทิศทางเดินในบล็อก `ATTENDED:`

ช่องว่างเดียวที่คุณระบุไว้ในหัวใบรอบ `wb8tfv` ("ชุด 2 ยังไม่มี `HEADLESS_PROOF:` ของตัวเอง") ปิดแล้ว
เงื่อนไขสองข้อที่เคยกั้นชุด 2 หมดอายุทั้งคู่: ผู้สมัคร `actor_type` 3 → **5 อยู่บน main แล้ว**
(`name_colour_sweep.py:226` `ACTOR_TYPE_CANDIDATE = 5`) และ `RE-290` ตอบแล้ว (พับไปแล้วรอบ `wb8tfv`)

## บรรทัดที่ขอให้วางในบล็อก `ATTENDED:` ของ `tickets/GT-288.md` (คำต่อคำ · ห้าบรรทัด · ASCII ล้วน)

```
HEADLESS_PROOF: 2026-09-07 · commit 9d2d1c0 (origin/main) · boot PF_NAME_COLOUR_SWEEP=2
  NAME_COLOUR_SWEEP_ARMED actors=6 census_actors=108 wire=114 pc=21502 frame=21516
  action labels WORLD_CENSUS_INITIAL_108_SWEEP_6 / WORLD_CENSUS_REAPPLY_108_SWEEP_6 (no second collection)
  same boot with the env absent: no NAME_COLOUR_SWEEP_* line, labels WORLD_CENSUS_INITIAL_108 / _REAPPLY_108
  set 2 nameboards N-BASE N-AT5 N-SKIN M-BASE M-AT5 M-SKIN (utf-16le, read back out of the queued payload)
```

## รันยังไง วัดบนอะไร

worktree สะอาดของ `origin/main` = **`9d2d1c0`** (`git log --oneline -1` + `git status --porcelain` ว่าง ยืนยันในรอบเดียวกัน)
ฮาร์เนสเดียวกับ `tests/test_name_colour_sweep_wiring.py` (`_arrive_capturing`) — `make_state_class` ตัวจริง
login → create → start_game → `TARGET_POS_VITAL` หนึ่งเฟรม แล้วอ่าน stdout ของบูตนั้น
ไม่มีโปรเซสเซิร์ฟเวอร์ ไม่มีซ็อกเก็ต ไม่มีไคลเอนต์ · env ล้างด้วย `clear=True` ทั้งสามบูต (`=2`, `=1`, ไม่ตั้ง)

**ติดอาวุธในฉากเป้าหมายจริง** (คำที่ `PANYA-ORDER 0159` บังคับ): บล็อกที่พิมพ์โทเคนอยู่ในสาขา home-scene ของ `runtime.py`
และบูตเดียวกันพิมพ์ `LANE_A_CENSUS_SKIPPED scene=1 source=bg0001_census` = ฉาก 1 Port Royal ซึ่งเป็นฉากที่บล็อก `ATTENDED:` ให้ผู้เทสยืน

**ชั้นที่สองแยกจากโทเคน**: ป้ายชื่อทั้งหกอ่านกลับ **จากไบต์ของ action ที่คิวไว้จะส่ง** (ค้น utf-16le ใน payload 21,516 ไบต์)
ไม่ได้นับจากที่โมดูลสร้าง · ในไบต์ชุดนั้น **ไม่มี** `N-AT3`/`M-AT3` และไม่มีป้ายของชุด 1 เลย
`wire=114 = census 108 + หุ่น 6` และมี action ของสาขานี้ **สองใบเท่านั้น** ⇒ ไม่มี collection ใบที่สอง ⇒ `RE-092` replace-by-omission ไม่ลบ NPC ทั้งเมือง ⇒ ตัวควบคุม `N-BASE` ยังเทียบสีได้

## 🔴 หนึ่งข้อที่ต้องแก้ในบล็อก `ATTENDED:` — ทิศทางเดิน (ไม่ใช่ความเห็น ผมวัด)

บล็อกข้อ 2 เขียนว่า "เรียงตาม **+X** จากจุดเกิด ห่างกัน 150 หน่วย" — **ทิศผิด**
`name_colour_sweep.py:297` คือ `return (x - 150.0 * (ordinal + 1), y, z)` ⇒ แถวเรียงไป **-X**
จุดเกิด X = `-9239.96` · หุ่นหกตัวอยู่ที่ X = `-9390 · -9540 · -9690 · -9840 · -9990 · -10140` (Y `-2830` Z `223` คงที่ทุกตัว)
ผู้เทสที่เดินตาม +X จะไม่เจออะไรเลยแล้วบันทึก "ไม่มีหุ่น" = **FAIL ปลอม** ทั้งที่กลไกติดอาวุธถูกต้อง
⇒ ขอให้แก้เป็น "เรียงไปทาง **-X** จากจุดเกิด ห่างกัน 150 หน่วย (ตัวแรกอยู่ห่าง 150)" · ข้อความเดิมไม่ต้องลบตามกติกาบ้าน

## ชุด 3 (`=3`) — **ยังห้ามบูต ไม่เปลี่ยน** (ยังไม่มีโค้ด · SPEC ONLY ตามเดิม)

## nonclaim (สำคัญ อย่าตัดออกตอนพับ)

- โทเคนนี้เป็น **ชั้น wire ล้วน** ไม่ใช่ client-observable และไม่ได้อ้างว่าเป็น
- ไม่ได้พิสูจน์ว่าไคลเอนต์ **วาด** หุ่นทั้งหกขึ้นจอ และไม่ได้พิสูจน์ว่า `actor_type 5` เรนเดอร์ได้
  (`RE-290` ตอบแค่ว่า `CAvatarNPC` สร้าง `NameBoardNPC` ตัวเดียวกับ `CNetNPC`) — "ไม่เห็นหุ่นเลย" ยังเป็น**ผลลบที่มีค่า**
- ไม่ได้ตอบว่าสีของชื่อเป็นอะไร นั่นคือทั้งหมดของ `RE-155` และต้องมีคนอยู่หน้าจอ
- `NAME_COLOUR_SWEEP_STANDING_REFUSAL allowed=False blockers=3` ออกในบูตเดียวกัน = ถูกแล้ว (พิมพ์ไว้ ไม่ได้ใช้ตัดสินใจ)
- ยังยืนคำเดิม **"รออย่างน้อย 8 วินาที"** จนกว่า chief จะแก้ลิสต์ delay — ใบถอน `0345` ข้อ 1 ยังไม่ถูกกลบ
- เรื่อง "ใบยืนยันเฟรมเดียวของ chief" ที่คุณค้างไว้ในหัวใบชุด 1: **ยังเป็นของ chief ไม่ใช่ของผม** ผมวัดได้แค่ว่าโค้ดบน main ทำเฟรมเดียวจริง

-- LANE-B รอบ `occzj8`
