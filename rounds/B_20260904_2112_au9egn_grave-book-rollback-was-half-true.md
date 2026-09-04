# LANE-B รอบ `au9egn` — 2026-09-04 21:12-21:28 +07:00 — ปิด `ADVERSARY_PENDING #762`: rollback ของสมุดหลุมศพเป็นจริงแค่ครึ่งเดียว

**NOW ข้อที่รอบนี้ขยับ**: ไม่ขยับขั้น M — รอบนี้ปิดหนี้ `ADVERSARY_PENDING #762` (บังคับเป็นงานแรกตาม `AGENTS.md` §7)
+ บริโภคจดหมายสองใบ (`2049`/`1935`) ไม่ใช่งานใหม่ตามบันได M

## 0. ล็อกรอบ · ชะตา PR รอบก่อน
- ต้นรอบ list PR open ทั้งสองรีโป: `pirate-force-server` = `#764` (LANE-GM) `#763` (LANE-E) · `pf_bridge` = `#1206` (LANE-CS) `#1202` (LANE-A)
  **ไม่มี `[LANE-B]` open** ⇒ ล็อกว่าง · เปิด claim `pf_bridge#1208` 21:12 (ไม่มี marker ตั้งแต่เปิด) · list ซ้ำแล้วไม่มีใบเก่ากว่าที่ยังมีชีวิต
- ADDENDUM A: `pirate-force-server#762` **merged=true** (`433fde4`) · `pf_bridge#1200` **merged=true** ⇒ งานรอบก่อน (`amz1w5`) อยู่บน main จริง

## 1. กล่องจดหมาย — บริโภคแล้วรอบนี้
- `20260904_2049_COO-DECISION-world-deaths-advisory-*` → stub แล้ว · ป้าย `[LANE-B ASSUMPTION - AWAITING COO]` → `[COO 2049: advisory until Door B]` ใน `mob_death_persistence.py` + สเปก (ข) เขียนลง docstring รอ Door B ไม่มีงานโค้ดใหม่ (ตามใบ)
- `20260904_1935_LANE-DB-REPLY-lane-b-ground-drop-taken-marker-*` → stub แล้ว · แก้ `test_the_restore_half_stands_down_until_the_taken_marker_exists` ให้โพรบ `object()` เปล่าแทน `self.store` จริง (แพทเทิร์นเดียวกับ `test_a_store_without_the_door_is_named_too` ในไฟล์เดียวกัน) ⇒ ไม่ผูกกับว่า `store.py` มีสองเมท็อดหรือยัง = `pirate-force-server#757` (ตายเกตด้วยเทสตัวนี้) retry ได้โดยไม่ชนอีก · ตอบจดหมายแล้ว `20260904_2112_LANE-B-TO-LANE-DB-*`

## 2. งานหลัก: ปิด `ADVERSARY_PENDING #762`
สั่ง `pf-adversary` ต้นรอบ สโคปเฉพาะสิ่งที่ครั้งที่ 2 ของรอบ `amz1w5` แตะ (ไม่ชำระซ้ำครั้งที่ 1)
คืนผล 1 ข้อ **HIGH** (พิสูจน์จริง ไม่ใช่ทฤษฎี) + 1 ข้อ low/theoretical (รับ ไม่แก้ พร้อมเหตุผล) + ยืนยันของเดิมยังถือ 6 จุด

**HIGH — `seed_the_session_state` รักษาสัญญา "ทั้งสองครึ่งหรือไม่ครึ่งไหนเลย" แค่ฝั่ง register**
ลูปที่ zero ค่า ledger เขียนทับ**พารามิเตอร์** `ledger` เองทุกแถวที่สำเร็จ (ผิดกับ `seed_register` ที่แยก `seeded` ออกจาก `register`
อย่างถูกต้องอยู่แล้ว) ⇒ แถวที่สองขึ้นไปพังกลางลูป = คืน `ledger` ที่มีการแก้ของแถวก่อนหน้าติดมา ไม่ใช่ของเดิมที่รับเข้ามา
adversary จำลองจริง: ฆ่าสองตัวใน bg0001, ledger ที่ throw เฉพาะแถวที่สอง ⇒ คอนโซลบอก "ถูกปฏิเสธ" (`SEED_REFUSED`) ทั้งที่ ledger
ที่คืนมามี HP ตัวแรกเป็น 0 ค้างอยู่จริง ⇒ ป้อนคู่นั้นเข้า `repopulation_entries` (จุดเรียกจริง) แล้วพัง `REFUSE_LEDGER_DISAGREES_WITH_REGISTER`
— อุบัติเหตุเดียวกับที่ `#762` เกิดมาปิด แค่ทริกเกอร์หายากกว่า เทสเดิม (`test_a_ledger_that_refuses_costs_the_register_its_seed_too`)
จับไม่ได้เพราะ `Angry` ของมัน throw จาก `identities()` ก่อนลูปวิ่งรอบแรกด้วยซ้ำ

**ตัวแก้**: เปลี่ยนลูปให้แก้ตัวแปร local (`mutated`) แทนพารามิเตอร์ `ledger` — รูปเดียวกับ `seed_register` ทำถูกอยู่แล้ว
except คืน `(register, ledger)` ของเดิมจริงเสมอ ไม่ว่าจะพังที่แถวไหน
**เทสใหม่** `test_a_second_admitted_grave_that_fails_still_costs_the_ledger_nothing` — ฆ่าสองตัว จำลอง ledger ที่ throw เฉพาะแถวสอง
(ต้องเขียนคลาสจำลองให้คงชนิดตัวเองไว้ข้ามการเรียกสำเร็จ เพราะ `with_balance` จริงคืน `CombatLedger(...)` เปล่า ไม่ใช่ `type(self)(...)`
— ถ้าไม่ระวังตรงนี้เทสจะดูเหมือนพังแค่ครั้งเดียวทั้งที่ควรพังสองครั้ง) พิสูจน์ทั้งสองโครงสร้างคืนเป็นของเดิม (`is`) และป้อนต่อเข้า
`repopulation_entries` จริงยืนยันว่าไม่พังอีก

**รับว่าจริงแต่ไม่แก้ (low/theoretical)**: `roster_key_of` ครอบ `try/except` ไม่ถึงบรรทัด `frozenset(...)` ท้ายฟังก์ชัน จึงไม่ "ไม่ raise เลย"
ตามที่ docstring สัญญาจริง ๆ — แต่ทั้งสองจุดเรียก (`bury` ผ่าน `except` กว้างของ `remember_death` และ `seed_register`'s own `try/except`)
กันไว้แล้วอิสระต่อกัน ไม่พบทางที่ใช้ประโยชน์ได้จริงวันนี้ ปิดช่องที่ต้นตอเป็นเรื่องของรอบที่แตะสัญญาฟังก์ชันนี้ครั้งถัดไป

**ยืนยันของเดิมยังถือ (ไม่แก้ซ้ำ)**: roster gate (diag/multi-object) · ceiling gate · `install_world_deaths` raise-by-type
vs. hot path fail-closed-by-name · `commit_death` ไม่กลืน exception เงียบ · roster-cache ไม่จำผลลบจาก raise · lock ทุกจุดเป็น `RLock` จริง

## 3. หลักฐานสองชั้น
- **wire**: เทสใหม่ (ข้อ 2) พิสูจน์ rollback จริงด้วยการจำลองความล้มเหลวกลางลูป + เรียก `repopulation_entries` จริงต่อท้าย
- **client-observable**: ยังไม่มี (เหมือนเดิมจาก `#762`) — รอจุดเรียก `runtime.py` ของ chief (`1945`)

## 4. ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
**ไม่เห็นอะไรใหม่โดยตรงจากรอบนี้** — สิ่งที่รอบนี้ปิดคือช่องที่จะทำให้ **listener thread ล้ม** วันที่มีสองหลุมขึ้นไปในฉากเดียว
แล้วแถวที่สองพังกลางทาง (อนาคต ไม่ใช่วันนี้ เพราะยังไม่มีจุดเรียกจริง) — ปิดก่อนมีจุดเรียก ดีกว่าปิดหลังมีคนเจอ

## 5. ที่ยังไม่ทำ / ไม่อ้าง
- ไม่แตะ `runtime.py` · ไม่แตะ `store.py` · ไม่แตะเขตสาย A
- `claim_the_kill` (สเปก (ข) ที่ `COO 2049` เคาะ) เขียนลง docstring แล้ว ยังไม่ implement — รอ Door B ขึ้น main ตามคำตัดสิน
- call site ของ `mark_ground_drop_taken`/`list_ground_drops_still_on_the_ground` ยังไม่มี — รอ `#757`-เทียบเท่าขึ้น main ก่อน

## 6. ชุดเทส
- ระหว่างทาง: `tests/test_mob_death_persistence.py` (61 ผ่าน) + `tests/test_mob_ground_persistence.py` (49 ผ่าน)
- ชุดเต็ม: **รันครั้งเดียว** บนต้นไม้ merge `origin/main` แล้ว (main ไม่ขยับระหว่างรอบ ⇒ ต้นไม้เดียวกับ `#762`'s tip)
  **`10173 passed, 327 skipped, 19440 subtests passed, 4 failed`** 515.89s
- 🔴 **ทั้ง 4 ที่แดง ไม่ใช่ของ PR นี้** — วัดจริงด้วย `git worktree add` บน `origin/main` สะอาด (ไม่มีดิฟฟ์รอบนี้เลย) แดงเหมือนกันทุกตัว:
  `test_npc_interaction_wire.py::QuestAndShopStateGuardTests::test_every_symbol_exemption_is_still_earned` (การ์ดของ chief `runtime.py`
  แดงมาแต่ `#762` แล้ว) + `test_m2_survey_trial.py::DispatchWiringTests` สองตัว + `test_lane_a_enter_instance_log.py` หนึ่งตัว
  (ทั้งสามตัวหลังไม่เคยเจอมาก่อนในไฟล์รอบสายนี้ — ไม่ใช่ไฟล์ของเขตนี้ ไม่มีตัวแก้ให้ port แจ้งไว้ในใบ PR)
- worktree ที่ใช้เทียบลบทิ้งแล้ว (`git worktree remove --force` + `prune` ยืนยันด้วย `worktree list`)

## 7. สถานะจบรอบ
- push ครบทั้งสองรีโป
- `pirate-force-server` PR **#766** — **เปิดแล้ว รอ gate** (`PF-AUTOMERGE: v4` ตั้งแต่เปิด · GET ยืนยัน marker แล้ว)
- `pf_bridge` claim PR **#1208** — เติม marker ท้ายไฟล์รอบนี้ = ปลดล็อก
- ไม่มี `ADVERSARY_PENDING` ใหม่รอบนี้ (สั่งครั้งเดียว คืนผลครบ ไม่ต้องแก้ซ้ำครั้งที่ 2)
- 🔴 เกต Windows จะแดงที่ 4 จุดข้างบน (ข้อ 6) ซึ่งแดงบน `origin/main` อยู่แล้ว ไม่ใช่ของ PR นี้
- ห้ามอ่านว่า "เสร็จ": รอ merge PR #766

## งานสำรอง (ทำเมื่องานหลักติด)
1. **`mob_deaths` durable table** — CORE-REQUEST ถึง LANE-DB (ยังไม่เขียน) · เกณฑ์ผ่าน: สมุดหลุมศพรอด server restart ไม่ใช่แค่ relogin
   ไฟล์: จดหมายใหม่ `notes_to_chief/*_LANE-B-CORE-REQUEST-mob-deaths-table.md` + เสียบใน `mob_death_persistence.py` เมื่อมีตาราง
2. **ของบนพื้น: wire call site ของ `mark_ground_drop_taken`/`list_ground_drops_still_on_the_ground` + ตัดสินอายุ 120 วิ**
   ไฟล์: `mob_ground_persistence.py` · เกณฑ์ผ่าน: รอ `pirate-force-server#757`-เทียบเท่าขึ้น main ก่อน (ตอนนี้ยังไม่มี) — เริ่มได้ทันทีที่ขึ้น
3. **"ศพยืนแข็ง" (R310 เห็น มอนที่ตายแล้วไม่ล้ม/ไม่มีอนิเมชัน)** — ยังไม่มีเลขใบ · ไฟล์: ยังไม่ทราบ (อาจเป็น `mob_ai_control.py`
   ตามที่ D9 ของรอบ `amz1w5` ตั้งข้อสังเกตไว้) · เกณฑ์ผ่าน: เปิดใบ RE/GT ก่อน อย่าเริ่มโค้ดจากศูนย์
