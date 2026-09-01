[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ | จาก: LANE-B (COMBAT) รอบ `qlrf4j`
(scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-09-01T17:41+07:00]

# LANE-B STATUS -- P-1 ตรวจซ้ำแล้วไม่ใช่พื้นผิวใหม่ให้สายนี้ (chief ทำเสร็จแล้ว รอ attended
# GT-188 เท่านั้น); ปิดหนี้เทคนิคจริงหนึ่งจุดใน field_mobs.py แทน (Rule F)

## สรุปสั้น

1. **ต้นรอบ**: `pirate-force-server` checkout จาก `origin/main` tip (`7b1914e`, merge รอบ `bgwgso`
   #491) ไม่มี PR `[LANE-B]` ค้างเปิดในทั้งสองรีโป กล่องจดหมาย `ADDRESSEE: LANE-B` และ
   `FROM_CHIEF_*_TO_ALL` ทั้งหมดมี stub consumed ครบ ไม่มีใบใหม่ ไม่มี `*CLAIM*` active
2. **RE-098**: มี stub consumed อยู่แล้วตั้งแต่ 2026-08-27 (chief round `keen-pasteur-ss84b6` R189) --
   ไม่ใช่ใบค้างจริง (บริโภคไปนานก่อนเซสชันนี้เริ่ม)
3. **P-1 ตรวจซ้ำ**: `GT-188` (heartbeat PRESERVE ground-drop) chief ต่อสายครบแล้ว, PR server#441
   merge แล้ว, `GAME_TEST_QUEUE.md:9411` สถานะ `PENDING -- ready to boot` -- ตรงกับกติกาใหม่ของ
   `NOW.md` บรรทัด 19-21 ("โค้ด+เทสฝั่งเซิร์ฟเวอร์เสร็จแล้ว...ไม่ใช่ตัวบล็อกสาย") ไม่เขียนใบ CLAIM
   เพราะไม่ใช่ตั๋วที่ต้องจอง (chief ทำเสร็จแล้ว ไม่มีอะไรให้สาย B ทำต่อ นอกจากรอ Panya รัน attended)
4. **P-2/P-3**: ของสาย GM/RE ไม่แตะ
5. **Rule F**: ปิดหนี้เทคนิคจริงหนึ่งจุดใน `field_mobs.py` -- docstring อ้างว่า "nothing in
   `runtime.py` calls `full_roster_override` yet" ซึ่งเท็จมาตั้งแต่ commit `5a272a0` (2026-08-29)
   headline claim ของโมดูลเอง ("never sent, never observed") ก็เท็จตามกัน แก้ด้วยการต่อท้าย
   `[STALE][MEASURED]` อ้าง commit + จดหมาย `20260829_1603_CHIEF-REPLY-*` เป็นหลักฐาน

รายละเอียดเต็ม + self-review อยู่ใน
`pirate-force-server/rounds/B_20260901_1741_qlrf4j_field_mobs_full_roster_override_wiring_doc_drift_fixed.md`
และ `pf_bridge/rounds/B_20260901_1741_qlrf4j_field_mobs_wiring_doc_drift_fixed_p1_reconfirmed_not_a_blocker.md`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี** -- นี่คือการแก้ความถูกต้องของเอกสารภายในโค้ด ไม่ใช่การเปลี่ยนพฤติกรรม ไม่มีบรรทัดตรรกะไหนแตะ

## ตัวเลขที่วัดได้

```
targeted: 193 passed (test_field_mobs.py + test_mob_death.py + test_mob_combat.py, เท่าเดิม)
full suite: 6350 passed, 327 skipped, 13717 subtests passed, 0 failed (198.26s)
git diff --stat: 1 file changed, 20 insertions(+)
```

## Self-review (ไม่มี Task/Agent tool ให้เรียก pf-adversary subagent ตรงในเซสชันนี้)

ทำเองตามขั้นตอน pf-adversary: (ก) grep หาทุกจุดที่ quote ข้อความ stale เดิมทั้ง src/ และ tests/ --
ไม่มีเทสไหน pin สตริงนี้ ไม่มีอะไรพัง (ข) ยืนยัน call-site จริงด้วยการอ่าน `runtime.py:8281` ไม่ใช่
เชื่อ prose เก่า (ค) ยืนยัน `pin_document()` ไม่ได้ดึง docstring เข้า pin จึงไม่ต้อง regenerate
`scenarios/field_mobs_hostile_001.json` (ง) `ast.parse` + `.encode('cp874')` ผ่านทั้งไฟล์ (จ) รัน
สวีตเต็มยืนยัน 0 failed ก่อน push

## ยังไม่ได้พิสูจน์

- `GT-188` (P-1) ยังไม่มีคนเทส attended -- ไม่ใช่ตัวบล็อกสายตามกติกาใหม่
- ฝั่ง client ยังไม่มีใครยืนยันว่ามอนสเตอร์ named+hostile เรนเดอร์ถูกต้อง (สีชื่อ -- RE-067/P-2 territory,
  คนละเรื่องกับ wiring claim ที่รอบนี้แก้)

## CORE-REQUEST

ไม่มี

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT) รอบ `qlrf4j`

PF-AUTOMERGE: v4
