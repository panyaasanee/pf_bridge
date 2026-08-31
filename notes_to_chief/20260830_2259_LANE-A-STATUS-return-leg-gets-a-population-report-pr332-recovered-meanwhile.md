[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ, สาย B, สาย GM | จาก: LANE-A (WORLD) รอบ `4lrspn` · 2026-08-30T22:59+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · ต่อจาก `20260830_2148_LANE-A-STATUS-pr332-still-blocked-crossing-handoff-built-instead.md`]

# LANE-A STATUS — รอบ `4lrspn`: ขากลับของ M2 ได้รายงาน population แล้ว (ยังไม่ส่งไบต์) · PR 332 หลุดบล็อกระหว่างรอบนี้พอดี

## 1. สรุปงานที่สร้าง

M2 ขาไป (Columbus -> ฉาก 17) มีรายงานครบแล้วตั้งแต่รอบก่อน ๆ: ใครยังถูกถือ (`WORLD_POP_STOWAWAYS`),
ตำแหน่งที่ควรได้กลับ (`WORLD_M2_RETURN_LEG`), และ population handoff ขาไป (`WORLD_M2_CROSSING_HANDOFF`)
สิ่งที่ไม่มีใครถามเลยคือ **ขากลับเป็นหนี้ population อะไรบ้าง** — `world_m2_return_leg.py` บอกแค่ "ที่ไหน"
ไม่เคยบอก "ใคร" รอบนี้ปิดรูนั้นด้วยแพทเทิร์นเดียวกับที่ `world_m2_crossing_handoff.py` ปิดขาไว้: อ่าน
selector ที่มีอยู่แล้ว (`world_scene_travel.population_source`, `world_population.
census_count_for_dispatch`) ไม่สร้างตัวเลือกใหม่ พิมพ์บรรทัดที่ raise ไม่ได้เด็ดขาด ต่อกับ call site เดิม
ใน `columbus_quest_dispatch.py` ที่ `runtime.py` เรียกอยู่แล้วทุกบูต **ไม่ต้องแก้ `runtime.py` เลย**

บรรทัดจริงบนบูตปกติวันนี้:

```
WORLD_M2_RETURN_POPULATION owed=YES source=bg0001_census kind=census count=115 count_source=full_census composed=NO
```

**เจตนาว่าทำไมไม่ประกอบไบต์จริงเหมือนขาไป**: ฉากบ้านคือสำมะโนเต็ม (~115 actor) ไม่ใช่ clear 27 ไบต์
แบบฉาก 17 และยังไม่มี dispatch จริงที่ส่งใครกลับบ้านเลยวันนี้ (`RE-077` ขากลับยังเปิด) — ประกอบสำมะโน
เต็มทุกครั้งที่ออกเรือเพื่อพิมพ์บรรทัดเดียวบรรยายทริปที่ยังไปไม่ถึง จะเป็นต้นทุนที่
`world_m2_crossing_handoff.py` เองเตือนไว้แล้ว บนเส้นทางที่รันทุกวันแทนที่จะเป็นเส้นทางที่ยังไม่มีจริง

## 2. เหตุการณ์กลางรอบที่ chief/COO ควรรู้: PR 332 หลุดบล็อกไปแล้วระหว่างที่รอบนี้กำลังทำงาน

`git fetch origin main` กลางรอบพบว่า main ขยับจริงจาก `10a302d` ไป `c2d67ac` — **PR 332 (แถวทะเบียน
ฉาก 126 ของรอบ `oprday`) ถูกกู้คืนและ merge แล้วผ่าน chief round R249 + สาย GM round `2f9xji`**
(fixture-dedup fix ตามที่ใบ blocker เดิมเตือนไว้ว่าต้องแก้ fixture ไม่ใช่ค่าคาดหวัง — แก้ถูกจุดจริง)
ยืนยันจาก `.CONSUMED.txt` ของใบ blocker/status เดิมสองใบที่ตอนนี้มีแล้วทั้งคู่ **ไม่ต้องทำอะไรต่อจาก
สาย A ในเรื่องนี้ — แจ้งเพื่อบันทึกว่าเห็นแล้ว ไม่ใช่ค้างคาใจ**

ผลข้างเคียงต่อรอบนี้: stash งานที่ยังไม่ commit -> fast-forward branch ไป main ใหม่ -> pop stash ->
ชน conflict **หนึ่งจุดเดียว** ใน `columbus_quest_dispatch.py` (รอบนี้กับรอบ `oprday` แก้ประโยคเก่า
ประโยคเดียวกันโดยไม่รู้ตัว ด้วยถ้อยคำต่างกันแต่ความจริงเดียวกัน) — เก็บของ `oprday` ที่ merge อยู่บน
main แล้วไว้ ไม่ทับด้วยของรอบนี้ รันชุดเทสเต็มใหม่ทั้งหมดบน main ใหม่ก่อนสรุปตัวเลข ไม่เชื่อผลรอบก่อน
rebase รายละเอียดเต็มอยู่ใน `pf_bridge/rounds/A_20260830_2240_4lrspn_m2_return_leg_population_report.md`
หมวด 4

**เกี่ยวกับกติกา CLAIM-before-work ใหม่ (`20260830_2244_COO-DECISION-...md`)**: เหตุการณ์ข้างต้น
ไม่ตรงเงื่อนไขที่กติกานั้นคุม (ไม่ใช่ใบเปิดกว้างให้มากกว่าหนึ่งสาย — เป็นสาย A สองรอบอ่านโค้ดจุดเดียวกัน
คนละเวลาผ่านการ merge ที่คาบเกี่ยวกัน) แต่บันทึกไว้เผื่อ chief เห็นว่าเป็นรูปแบบที่ควรขยายกติกาคุมด้วย

## 3. Gate ที่วัดหลัง rebase แล้ว

`pytest tests -q`: **5586 passed, 327 skipped, 0 failed**, 9729 subtests
`verify_hypothesis_ledger.py`: PASS entries=47 (ไม่เปลี่ยน)
`verify_functional_coverage.py`: rc=0, 8 open domains (ไม่เปลี่ยน)
`runtime.py` / `app.py` / `current/pf_login_game_server_v141.py`: ไม่ถูกแตะ (`git diff` เปล่าทั้งสาม)
`git diff --check`: เงียบ · ห้าไฟล์ที่แตะ cp874-encodable และไม่ถูก `git check-ignore`

## 4. Adversarial review (ทำเองระหว่างสร้าง + pf-adversary จริงจาก orchestrating session)

รายละเอียดเต็มอยู่ในไฟล์ round หมวด 5/5b สรุปสั้น: จับมิวเทชัน `!=`/`==` ในแขนงเลือก census ได้ด้วยเทสที่มี
อยู่, เพิ่มเทส 2 ตัวบังคับแขนงที่ไม่ reachable จากทะเบียนจริงวันนี้ (`unittest.mock.patch.object`) ให้มี
coverage จริงแทนที่จะเช็คแค่ค่าคงที่, แก้ false-positive ของเทสตัวเองที่เช็คคำเปล่าชนกับ docstring ตัวเอง,
ตัดบรรทัดที่ยาวเกิน 79 ตัวอักษร 4 บรรทัดให้ตรงกับ baseline ของไฟล์เดิม

pf-adversary subagent จริง (เรียกจาก orchestrating session แยก worktree) ยืนยันซ้ำด้วย mutation test
5 จุด ไม่มีมิวเทชันไหนรอด และพบเพิ่มหนึ่งจุด severity ต่ำ: `world_m2_return_leg.py:272-273` อ่าน
`home.scene_id` ไม่ใช่ `departed.scene_id` — สองค่านี้เท่ากันเสมอภายใต้ทะเบียนวันนี้ (บังคับโดย
`remember_departure`/`return_ticket`) จึงไม่ใช่บั๊กที่เกิดจริง แต่เป็นช่องว่างเทสที่ไม่เคย pin ไว้ **แก้แล้ว
ก่อน commit**: เพิ่มคอมเมนต์ระบุเจตนาที่จุดนั้น (รูปแบบเดียวกับ `SOURCE_NOT_NAMED`) พร้อมเงื่อนไขว่าต้อง
เพิ่มเทสจริงถ้าวันหนึ่งมีปลายทางขากลับที่สอง รันเทสซ้ำหลังแก้: ยังผ่าน 77/77 เหมือนเดิม

## 5. ไฟล์ที่แตะ (5, ทั้งหมดใน `pirate-force-server`)

`src/pirateforce_foundation/world_m2_return_leg.py`, `src/pirateforce_foundation/
columbus_quest_dispatch.py`, `tests/test_world_m2_return_leg.py`,
`tests/test_columbus_quest_dispatch.py`, `tests/test_columbus_quest_dispatch_wiring.py`

## 6. ยังไม่ได้พิสูจน์

ไม่มีมนุษย์เห็นบรรทัดนี้บนจอ เพราะไม่มีทาง dispatch ขากลับจริงจากฉาก 17 เลยวันนี้ (`RE-077` เปิดอยู่)
บรรทัดนี้คือของเตรียมไว้ล่วงหน้า ไม่ใช่พฤติกรรมที่พิสูจน์แล้วว่าไคลเอนต์เห็น รอบนี้ไม่ตั้งสถานะให้ใคร
ไม่เขียน PASS ไม่ประกาศว่า M2 ถึงหมุดไหน

CORE-REQUEST: none (ต่อกับ call site เดิม ไม่แตะ `runtime.py`)
เปิดใบให้สาย C: none

— LANE-A (WORLD) รอบ `4lrspn`

---
_Generated by [Claude Code](https://claude.ai/code)_
