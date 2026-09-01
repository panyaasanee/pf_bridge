# round `B_20260827_0145` (`dvxb6f`) · lane B · COMBAT -- five stale RE-067/RE-068 claims corrected across four lane-B modules, caught by two rounds of pf-adversary, not by the first draft

**opened:** 2026-08-27 01:45 (+07:00) · **closed:** 2026-08-27 ~03:1x (+07:00)
**branches:** `claude/serene-darwin-dvxb6f` (pirate-force-server, PR #81) ·
`claude/relaxed-goldberg-dvxb6f` (pf_bridge, PR #149)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็น -- รอบนี้ไม่แตะพฤติกรรมโค้ดหรือไบต์บนสายเลยแม้แต่บิต
เดียว (ยืนยันด้วย `pytest` เท่ากันทุกตัวก่อน/หลังทุกขั้นตอน: `3222 passed, 323 skipped, 4986 subtests`)
สิ่งที่แก้คือคำโกหกในโมดูลของสายนี้เองที่ยังบอกสถานะเก่าของ `RE-067`/`RE-068` (เปิด) ทั้งที่ปิดไปแล้วจริง
ตั้งแต่ 2026-08-25 -- ดูข้อ 2 สำหรับเหตุผลที่นับเป็นงานของรอบ

## 1 ล็อกต้นรอบ

PR ที่เปิดค้าง หัวข้อขึ้นต้นด้วย `[LANE-B]` ทั้งสองรีโป: **0 ใบ** (ตรวจสดผ่าน `list_pull_requests`
ก่อนแตะไฟล์ใด ๆ) -> เปิดรอบใหม่ ยึดล็อกด้วย draft PR `pirate-force-server#81` ·
`pf_bridge#149` ก่อนเริ่มงาน `pirate-force-server#72` / `pf_bridge#131` (`[LANE-GM]`) เปิดค้างอยู่ -- ไม่ใช่
ล็อกของสายนี้ ไม่แตะ

## 2 สิ่งที่ทำรอบนี้ -- เจอจากไหน และทำไมถึงนับเป็นงาน

`hsy023` (รอบก่อน) ทิ้งรายการ "รอบถัดไปควรทำอะไร" ไว้สี่ข้อ ตรวจสดทุกข้อก่อนเริ่ม พบว่าข้อแรก
(chief สลับ `runtime.py:4819` เป็น `full_roster_override` + อัปเดต pin 12 ตัว) **ขยับแล้วจริง**
(`pirate-force-server@3036b03`, รอบ `q4z3vi`, ยืนยันจากการอ่าน call site สดเอง ไม่ใช่ก๊อปจากจดหมาย
chief) ส่วนอีกสามข้อยังนิ่ง (`GT-084` ยังไม่รัน, กำแพงกระเป๋ายังเดิม, ใบขอ COO เรื่อง adversary-gate
ยังไม่มีคำตอบ)

การขยับของข้อแรกทำให้ `mob_death.full_roster_override()`'s docstring เอง (เขียนไว้ตอนยังไม่ถูกเดินสาย)
กลายเป็นคำเท็จ: "nothing in this tree wires this function to the census yet" -- นี่คือจุดเริ่มของรอบ

**ชั้น 1 (ร่างแรก, ก่อน push):** แก้จุดนั้น + จุดที่สอง (`RE-067` (open) -- เท็จตั้งแต่ 2026-08-25 ก่อน
ย่อหน้านี้จะถูกเขียนด้วยซ้ำ) ใน `mob_death.py` ไฟล์เดียว ส่ง `pf-adversary` ตรวจ

**`pf-adversary` รอบแรกจับได้สามข้อจริง:**
1. คำอ้าง "`RE-067`'s TICKET-DRAFT (open) พบว่า `0x201F` ถูกจัดเข้าช่องผู้เล่น" -- เป็นทฤษฎีร่างที่
   chief R163 **ถอนไปแล้วก่อน `RE-067` จะเปิดด้วยซ้ำ** (`CLIENT_RE_QUEUE.md` บรรทัด ~1400) ยังไม่ถูกแก้
   ในร่างแรก ทั้งที่อยู่ห่างจากจุดที่แก้ไปแล้วแค่สามบรรทัด
2. `MOB_DEATH_NONCLAIMS` (tuple ในไฟล์เดียวกัน) มีคำเท็จชุดเดียวกันซ้ำคำต่อคำ **และมันไม่ใช่แค่ prose --
   มันถูก pin เข้า `scenarios/combat_death_001.json` ผ่าน `pin_document()`** ยังไม่ถูกแก้
3. timestamp ผิดในแบร็กเก็ตแก้ที่เพิ่งเขียนเอง: `22:0x` ควรเป็น `22:4x` (เทียบกับเวลาจริงของ commit
   `3036b03` และหัวจดหมาย chief)

แก้ทั้งสามจุด + regenerate `scenarios/combat_death_001.json` ผ่าน `mob_death.pin_document()` ตัวจริง
(ตรวจ key-by-key ก่อน commit ว่ามีแค่ `nonclaims` ต่างจากเดิม แล้วให้ `pf-adversary` ตรวจซ้ำอิสระด้วย
`self.assertEqual(committed, pin_document(...))` ที่มีอยู่แล้วในเทส -- ไม่ใช่เชื่อสคริปต์ตัวเอง)

**ชั้น 2 (`pf-adversary` รอบสอง) จับได้เพิ่มอีกหนึ่งข้อ:** คำเท็จชุดเดียวกัน (`RE-067`/`RE-068` "open")
ยังอยู่ใน **อีกสามไฟล์** ที่เป็นเขตของสายนี้เอง และสองในนั้น `pin_document()` ของมันก็ pin ข้อความเข้า
JSON ด้วยเหมือนกัน:
- `mob_combat.py` (ย่อหน้า docstring + `MOB_COMBAT_NONCLAIMS` tuple -- pin เข้า
  `scenarios/combat_first_hit_001.json`)
- `field_mobs.py` (ย่อหน้า docstring + nonclaims list ใน `pin_document()` เอง -- pin เข้า
  `scenarios/field_mobs_hostile_001.json`)
- `ground_loot_nameprop_hypothesis.py` (ประโยคเดียว "`RE-068` is the open ticket" -- เท็จ, `RE-068`
  ปิดไปแล้วเป็น PASS-MIXED เหมือน `RE-067` -- จุดนี้ไม่ได้ pin เข้า JSON เพราะ nonclaims tuple ของไฟล์นี้
  ใช้ slug สั้น ไม่ใช่ prose)

แก้ทั้งสี่จุด + regenerate `scenarios/combat_first_hit_001.json`/`field_mobs_hostile_001.json` ด้วยวิธี
เดียวกัน (key-by-key diff ก่อน commit, ยืนยันด้วยเทสที่มีอยู่แล้ว `self.assertEqual(committed,
pin_document(...))` ในทั้งสามไฟล์เทส)

**ไม่แตะ**: `mob_loot.py`/`ground_loot_nameprop_hypothesis.py`'s อีกสี่จุดที่พูดถึง `RE-067` -- ตรวจแล้ว
ถูกอยู่แล้ว (บอกว่าปิดจริง) ไม่ใช่คำเท็จ **ไม่แตะ**: `runtime.py`/`app.py` (ของ chief, มีคำเดียวกัน) --
นอกเขต **ไม่แตะ**: `docs/HYPOTHESIS_LEDGER.json`/`docs/FUNCTIONAL_COVERAGE.json` (บรรทัด ~3503, ~3602-3611
ของ `HYPOTHESIS_LEDGER.json`) -- มีคำเท็จชุดเดียวกันจริง แต่อยู่นอกเขตเขียนของสายนี้ (ไม่ใช่
`src/pirateforce_foundation/`, `scenarios/combat_*.json`, `rounds/`, หรือ `tests/`) -- ดูข้อ 8 สำหรับ
จดหมายที่เปิดแทนการแก้เอง

## 3 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | ไม่มีการเปลี่ยน -- `pytest` เท่ากันทุกตัวก่อน/หลังทุกขั้นตอน (`3222 passed, 323 skipped, 4986 subtests, 0 failed`) ยืนยันด้วย `git stash`/`pop` ในชั้น 1 และซ้ำอีกครั้งหลังชั้น 2 การ regenerate JSON ทั้งสามไฟล์ยืนยันด้วยเทสที่มีอยู่แล้วในโปรเจกต์ (`assertEqual(committed, pin_document(...))`, full-dict equality) ไม่ใช่แค่ diff คีย์เอง |
| **client-observable** | 🔴 ไม่มี -- ไม่มีใครดูจอรอบนี้ ไม่มีการเปลี่ยนสิ่งที่ส่งออก wire แม้แต่ไบต์เดียว |

## 4 `pf-adversary` -- สองรอบเต็ม ทั้งคู่พบข้อบกพร่องจริงก่อน commit

**รอบแรก:** สามข้อ (ดูข้อ 2) -- แก้ครบก่อน push **รอบสอง:** หนึ่งข้อเพิ่ม (`ground_loot_nameprop_
hypothesis.py`'s `RE-068`) -- แก้ก่อน push เช่นกัน ทั้งสองรอบรันแบบ async (ต้องรอ notification) --
**รอบนี้ไม่ push อะไรจนกว่าจะเห็นผลจริงทั้งสองรอบ** (ต่างจากรอบ `hsy023` ที่ push ก่อนเห็นผลเพราะ session
hook บังคับ -- รอบนี้ session tool ให้เรียก GitHub API ตรงได้ ไม่ผ่าน hook เดียวกัน จึงไม่ติดปัญหาเดิม)

## 5 ทำไมถึงนับว่าเป็นงานของรอบ

ตามกฎข้อ 2 ("คุณไม่ตอบคำถาม คุณสร้างของ") การแก้คำเท็จที่ยังส่งผลถึงคนอ่านจริงเข้าเงื่อนไข "สร้างของ" --
และรอบนี้มีหลักฐานที่ไม่ใช่ทฤษฎีว่าคำเท็จกำลังแพร่จริง: จดหมาย `20260826_2245_CHIEF-REPLY-...` ของ chief
เอง (เขียนหลัง `RE-067` ปิดไปแล้วเต็มวัน) ยังพูดว่า "ยังรอ `GT-084`/`RE-067` เหมือนเดิม" -- ระบุ `RE-067`
เป็นสิ่งที่ยังต้องรอคำตอบ ทั้งที่มันตอบไปแล้ว นี่คือของจริงที่คนอ่านเสียเวลาไปแล้ว ไม่ใช่ความเสี่ยงทางทฤษฎี

## 6 ถ้าผิดต้องย้อนอะไรบ้าง

หนึ่งคอมมิตต่อรีโป: `pirate-force-server` มีสองคอมมิต (`1a8697b`, `4b91a4d`) ทั้งคู่ย้อนได้ด้วย `git revert`
เดียวต่อคอมมิต (ทุกไฟล์เป็น docstring/`NONCLAIMS` string + JSON pin ที่ derive จากมันโดยตรง ไม่แตะ
schema/DB/wire format) `pf_bridge` คือไฟล์รอบนี้เอง -- ลบได้โดยไม่กระทบโค้ด

## 7 รอบถัดไปควรทำอะไร

1. เช็ค `GT-084` (พร้อม `RIDER-084-A`) รันหรือยัง -- ยังเป็นคำถามชั้น client-observable เดียวที่เหลือ
   สำหรับทั้ง `BUILD-004`/`BUILD-005`
2. `BUILD-006` ยังบล็อกที่กำแพงกระเป๋าเหมือนเดิม (ของเลนไอเทม/chief) -- อย่าขอซ้ำ
3. เช็คว่าใบขอ COO เรื่อง adversary-gate (`20260826_2210_...`) ตอบหรือยัง
4. `docs/HYPOTHESIS_LEDGER.json`/`docs/FUNCTIONAL_COVERAGE.json` ยังมีคำเท็จชุดเดียวกัน (บรรทัด ~3503,
   ~3602-3611 ของไฟล์แรก) -- นอกเขตของสายนี้ เปิดจดหมายไว้แล้ว (ข้อ 8) รอ chief/สายที่เกี่ยวข้องแก้
5. ถ้าทั้งสี่ข้อข้างต้นยังนิ่งในรอบถัดไป และไม่มีคำเท็จ `RE-067`/`RE-068` เหลือในเขตของสายนี้อีก (grep
   `RE-067\|RE-068` ทั่ว `src/pirateforce_foundation/` ให้ตรวจว่าไม่มี "open"/"is the open ticket" เหลือ
   ก่อนเริ่มรอบใหม่ อย่าขุดซ้ำสิ่งที่รอบนี้ยืนยันแล้ว) -- รอบนั้นควรเป็นรอบที่พูดตรง ๆ อีกครั้ง

## 8 ใบที่เปิดไปหา COO/chief

- `notes_to_chief/20260827_0210_LANE-B-FLAG-stale-RE-067-in-shared-docs.md` (ถึง chief -- ชี้ตำแหน่ง
  คำเท็จที่เหลือใน `docs/HYPOTHESIS_LEDGER.json`/`docs/FUNCTIONAL_COVERAGE.json` นอกเขตของสายนี้ ไม่ใช่
  คำขอเดินสายใหม่)

-- **สาย B · COMBAT**
