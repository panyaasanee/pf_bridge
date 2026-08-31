[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ, กะ1-B | จาก: LANE-B (COMBAT) รอบ `256rvs`
(scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-08-31T18:50+07:00]

# LANE-B STATUS -- ตรวจสามข้อจาก KA1B ต่อ HEAD จริงครบ, ③ ปิดเป็น non-issue,
# ① บันทึกไว้ (ของใหญ่ ไม่ทำรอบนี้), ② สร้าง mob_ai_scheduler.py (ยังไม่ wire)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** โมดูลใหม่รอบนี้ (`mob_ai_scheduler.py`) ไม่มี importer ใน `src/` เลย (พิสูจน์ด้วยเทส
`test_the_scheduler_has_no_importer_yet`, AST sweep) -- ยังไม่ถูกเรียกจาก `runtime.py` ซึ่งเป็นไฟล์
ของ chief ตามเขต ไม่ส่งเฟรมใด ๆ บนไวร์เลยไม่ว่าจะถูกเรียกหรือไม่ (ดู NONCLAIM ในโมดูลเอง) รอบนี้
สร้าง "ผู้เรียก" ที่ขาดหายไปให้ `mob_ai_control.tick_step` เท่านั้น -- ยังไม่ใช่ตัวที่ทำให้มอนเห็นบนจอ

## Protocol A/B (ADDENDUM v2)

**A**: `GET pulls?state=open` สดทั้งสอง repo ตอนเริ่มรอบ (~18:36+07:00) -- ไม่มี `[LANE-B]` PR ค้าง
(มีแค่ `[LANE-GM]` `pirate-force-server#404`) PR `[LANE-B]` ที่ปิดล่าสุดทั้งสอง repo
(`pf_bridge#614`/`pirate-force-server#399`) `merged=true` -- ไม่มีอะไรต้องกู้จาก main

**B**: `ADDRESSEE: LANE-B` ที่ยังไม่มี `.CONSUMED.txt`: มี 1 ใบใหม่จริง --
`20260831_1700_KA1B-TO-LANE-B-three-code-defects-from-owner-audit-verify-then-ticket.md`
(ใบ `20260831_0147_LANE-B-STATUS-addendum-2355-*` ที่ grep เจอด้วยไม่ใช่ใบเข้า เป็นจดหมายที่ LANE-B
เขียนถึง chief เองตั้งแต่รอบก่อน ไม่ต้องมี stub) ตอบใบ KA1B ทั้งหมดด้านล่าง สร้าง stub +
ย้าย consumed แล้ว

## KA1B สามข้อ -- ตรวจกับ HEAD จริง (ไม่ใช่ความจำจากใบเดิม) ทีละข้อ

### ① โปรไฟล์ผู้โจมตีตายตัว level 7 / STR 132 -- **ยืนยันจริง แต่บันทึกไว้แล้วในโค้ดเอง ไม่ใช่ของค้าง
ที่ไม่มีใครเห็น**

`mob_combat.py:1759-1760` (`PIN_ATTACKER_LEVEL = 7` / `PIN_ATTACKER_ABILITY_STR = 132`) และ
`runtime.py:268-277` (`MOB_COMBAT_DEFAULT_ATTACKER = mob_combat.pin_attacker()`) ยืนยันตรงกับที่ใบ
KA1B ชี้ -- แต่ `runtime.py:266-277`'s comment เขียนไว้เองแล้วว่า "[PROPOSED, not measured]... every
player currently deals the same damage numbers... OURS, not the client's" ไม่ได้ซ่อนอยู่ที่ไหน
**สาเหตุที่ยังไม่แก้**: การแก้จริงต้องมีแหล่งสเตตัสผู้เล่นรายคนที่ไม่มีในโปรเจกต์นี้เลย (`model.Position`
มีแค่ identity+xyz) -- ต้นทุน M ตามที่ KA1B ประเมิน และ solution ที่ปลอดภัย (read-only shadow
snapshot ก่อนสลับ authority) ต้องมีข้อมูลสเตตัสผู้เล่นจริงมาก่อน ซึ่งยังไม่รู้ว่าไคลเอนต์ส่งมาทางไหน
(หรือส่งเลยหรือเปล่า) **ตัดสิน**: ไม่เปิดใบใหม่รอบนี้ -- นี่เป็นของใหญ่กว่า S/M ธรรมดา ถ้าเจ้าของ/COO
อยากให้เดินหน้าเรื่องนี้เป็นความคิดริเริ่มถัดไปของ COMBAT ให้สั่งมา จะเปิดใบให้สาย RE ตามหา
per-player battle stat บนไวร์ก่อนเริ่มออกแบบ shadow snapshot

### ③ Training Iron Man (n_ID 916) -- **ตรวจละเอียดแล้ว: ไม่ใช่ของค้าง ปิดเป็น non-issue รอบนี้**

ไล่ทั้งสี่ความกังวลของ KA1B ทีละอย่างกับ HEAD จริง:
- **AI/offensive**: `mob_ai_control.profile_of()` (`mob_ai_control.py:411-436`) บังคับ
  `offensive=False` เมื่อ `ai_combat` เป็น `None` -- 916 มี `n_AI_COMBAT=0` เสมอ (คอมเมนต์ในโค้ดอ้าง
  `COO-DECISION 2026-08-29T00:41+07:00 item 3`: "not inventing a script the data does not have is
  the rule of this house") -- **ไม่มีทางได้ AI ที่ไม่ควรมี แม้ `tick_step` จะถูกต่อสายแล้วก็ตาม**
- **lootable**: `field_mob_tables.py:97-100` มี `drops_normal=drops_equipment=drops_specially=0`
  ทั้งสี่แถว, `mob_loot.py:_set_rows` ข้าม (`continue`) ทุก `set_id == 0` -- **ไม่มีทางดรอปของ**
- **death/kill**: ได้รับอนุญาตให้ตายได้ **โดยตั้งใจ** ผ่าน `mob_death.WIDENING_RULINGS` ที่ตั้งชื่อ
  916 ตรง ๆ (`COO-DECISION widen-death-scope-916-training-iron-man`) -- นี่คือของที่ COO อนุมัติแล้ว
  ไม่ใช่ช่องโหว่
- **respawn**: ค้นทั้ง `src/` ไม่พบกลไก respawn เลยไม่ว่าจะมอนจริงหรือหุ่นฝึก (`grep -rn respawn
  src/pirateforce_foundation/*.py` ไม่มีจุด spawn-again จุดไหน) -- **ไม่มีความเสี่ยงนี้อยู่จริงในโค้ด
  วันนี้ ไม่ว่ากับมอนตัวไหน**

**สรุป**: สถาปัตยกรรมแยก role ไว้ถูกต้องแล้วผ่านข้อมูล (rank=0/ai_combat=0/drops=0,0,0) ไม่ใช่ผ่าน
เทรตแยกต่างหากตามที่ KA1B เสนอ (cost S) -- แต่ผลลัพธ์เดียวกัน: dummy ไม่มีทาง "ถูกนับเป็น monster
fidelity" ผิด ๆ เพราะทุกกลไกที่จะทำให้มันดูเหมือนมอนจริง (AI/loot/respawn) ถูกปิดที่ข้อมูลหมดแล้ว
ไม่เปิดใบ ไม่แก้โค้ด -- นี่คือ "ตรวจแล้วพบว่าไม่ใช่ของค้าง" ตามที่ใบ KA1B ขอให้ตัดสินเอง

### ② `tick_step` มีแต่ไม่มีใครเรียก production -- **ยืนยันจริง, สร้าง `mob_ai_scheduler.py` รอบนี้**

ยืนยันด้วย `grep -n "mob_ai_control\." src/pirateforce_foundation/runtime.py`: มีแค่
`damage_step`/`death_step`/`open_register`/`commit_step` -- ไม่มี `tick_step` เลยสักจุด `damage_step`/
`death_step` เป็นฝั่ง REACTIVE (ตอบสนองหลังเกิดเหตุแล้ว) `tick_step` เป็นฝั่ง PROACTIVE เดียวที่ทำให้
มอนที่ `n_OFFESIVE=1` เห็นผู้เล่นเองโดยไม่ต้องถูกตีก่อน -- นี่คือรูปธรรมของ "มอนไม่เดิน" ที่เจ้าของยกไว้

**สร้างรอบนี้** (pirate-force-server): `src/pirateforce_foundation/mob_ai_scheduler.py` --
`tick_session(ai_register, combat_ledger, player_identity, player_position, player_alive)` วนทุกแถว
ในรีจิสเตอร์ของ**เซสชันเดียว**ที่มีอยู่แล้ว (`self.mob_ai_register` เปิดต่อ session ตามคอมเมนต์ของ
`runtime.py:1231-1247` เอง "same per-session choice... follows the pattern every other mutable
structure on this class already uses") ด้วยผู้เล่นเดียวที่ session นั้นเห็นได้จริง (ตำแหน่งตัวเอง) --
ไม่ประดิษฐ์รายชื่อผู้เล่นในฉากที่ไม่มีอยู่ในโค้ดวันนี้ (grep แล้ว: ไม่มี registry แบบนั้นใน `src/`)
ดึง HP จริงจาก `combat_ledger.balance_of()` ไม่ประดิษฐ์ ใช้ตำแหน่ง placement เป็นตำแหน่งมอน (มอนยังไม่
เคยขยับในโปรเจกต์นี้เลย ข้อความนี้ยังจริงอยู่จนกว่าจะมีมอนขยับจริง) ทดสอบด้วยมอนจริงจากตาราง Bg0002
(placement 92, Orc Chief, `ai_wander=11`) ไม่ได้ประดิษฐ์แถว **ไม่ส่งเฟรมใด ๆ** (`ATTACK_INTENT_
DELIVERABLE` ยังเป็น `False` -- Door B ยังปิดเหมือนเดิม โมดูลนี้ไม่เปิดมันเช่นกัน)

## CORE-REQUEST (ยังไม่ใช่คำขอให้ wire ทันที -- ดู ASK-COO ด้านล่างก่อน)

`MOB_AI_SCHEDULER_WIRING` (docstring ของโมดูลเอง) เขียน call site แบบ "ยังไม่ระบุบรรทัด" โดยตั้งใจ:
เรียก `mob_ai_scheduler.tick_session(...)` จาก dispatch point ที่มีอยู่แล้วและวิ่งถี่พอ (เช่นจุดที่
`self.last_target_pos` อัปเดตอยู่แล้ว) แล้วเก็บ register ที่คืนมากลับที่ `self.mob_ai_register` -- ไม่
composeเฟรมเลยไม่ว่ากรณีไหน จึงปลอดภัยจะต่อสายได้โดยไม่ต้องเปิด Door B ในรอบเดียวกัน **แต่**: ต่อสาย
แล้วผู้เล่นยังไม่เห็นอะไรเปลี่ยนบนจอ (ยังไม่มีเฟรม) เพียงแค่ทำให้ AI state (phase/threat/target) เริ่ม
สะสมความจริงแทนที่จะค้าง idle ตลอดกาล -- คุณค่าอยู่ที่เตรียมพื้นสำหรับ Door B ไม่ใช่ผลที่เห็นทันที
ถ้า chief เห็นว่าคุ้มจะต่อสายตอนนี้ ทำได้เลยตามบรรทัดในโมดูล ถ้าจะรอ Door B decision ก่อนก็ปลอดภัย
เท่ากัน (ไม่ต่อสายไม่มีผลอะไรต่างจากวันนี้)

## เปิดใบให้สาย C

ไม่มี -- ข้อ ① มีคำถามที่แท้จริง (client ส่ง per-player battle stat ที่ไหนไหม) แต่ยังไม่เปิดใบ
เพราะเป็นของใหญ่กว่างานรอบนี้ (M cost ตาม KA1B เอง) รอสัญญาณจากเจ้าของ/COO ว่าจะเดินเรื่องนี้ต่อก่อน

## ASK-COO -- ควรเดินหน้า "Door B" (compose เฟรมให้ tick_step ที่ต่อสายแล้วมีผลบนจอ) เป็นงานถัดไป
## ของ COMBAT ไหม

**ติดอะไร**: `mob_ai_scheduler.py` (รอบนี้) ทำให้ AI state proactive พร้อมต่อสายแล้ว แต่ค่าที่ผู้เล่น
เห็นจริง ("มอนวิ่งเข้าหา/ยืนตีกลับ") ต้องเปิด Door B -- compose เฟรมจาก `MobAiIntent` ให้ client เห็น
ซึ่งเป็นงานใหญ่กว่า M3-M5 vertical slice เดิม (ต้องมีรูปแบบ movement frame ที่พิสูจน์แล้ว, cadence,
ฯลฯ) และ `mob_aggro.ATTACK_INTENT_DELIVERABLE = False` เป็นค่าที่ถูกตั้งไว้อย่างตั้งใจในทุกรอบก่อนหน้า
("Door B was never opened, and this module does not open it either" -- คำของ `mob_ai_control.py` เอง)

**ทางเลือกที่เห็น**:
(ก) เดินหน้า Door B ทันทีเป็นงานถัดไปของ BUILD queue (M6?) -- ผลคือมอนขยับ/ตีกลับได้จริงบนจอเป็นครั้ง
    แรก แต่เป็นงานใหญ่ ไม่รู้ขนาดจริงจนกว่าจะเริ่มสำรวจ wire format การขยับ NPC
(ข) รอจนกว่า BUILD-006 (M5 เก็บของ) ปิดก่อน (`GT-146` ยังไม่มีผล) แล้วค่อยเปิด M6 นี้เป็นลำดับถัดไป
(ค) chief ต่อสาย `mob_ai_scheduler` ตอนนี้เลย (ปลอดภัย ไม่มีผลบนจอ) เพื่อให้ AI state สะสมจริงไว้ก่อน
    รอ Door B โดยไม่ต้องรอ

**เลือกอันไหนไปแล้ว**: ยังไม่เลือก -- รอ COO ตัดสินระหว่าง (ก)/(ข)/(ค) ไม่ใช่บล็อกงานรอบหน้า (จะทำ
งานอื่นในคิว BUILD-006/backlog ต่อระหว่างรอ)

**ถ้าผิดต้องย้อนอะไรบ้าง**: ไม่มี -- `mob_ai_scheduler.py` ยังไม่ถูกเรียกจากที่ไหนเลย ย้อนคือลบไฟล์
เฉย ๆ ไม่กระทบ `runtime.py`/`app.py`

## ตัวเลขที่วัดได้

```
tests/test_mob_ai_scheduler.py : ใหม่ 15 ใบ ผ่านทั้งหมด
src/pirateforce_foundation/mob_ai_scheduler.py : ใหม่ 1 ไฟล์
grep -n "mob_ai_control\." src/pirateforce_foundation/runtime.py : 9 hit (damage_step/death_step/
  open_register/commit_step เท่านั้น -- 0 hit สำหรับ tick_step, ยืนยันข้อค้นพบ ②)
สวีตเต็ม pirate-force-server (pytest tests -q), รันสองครั้ง:
  ก่อนแก้ 3 containment/inventory guard ที่โมดูลใหม่ชน (ตั้งใจให้ชน -- ดูด้านล่าง):
    4 failed, 5855 passed, 323 skipped, 11148 subtests passed (218.52s)
  หลังแก้ tests/test_mob_aggro.py + tests/test_mob_ai_control.py (ContainmentTests รับ importer
  ตัวที่สอง) + tests/test_mob_stat_fabrication_guard.py (LANE_B_MODULES tuple) + แก้วลีไทยที่หลุด
  เข้า docstring ของโมดูลใหม่ (พบจาก ASCII-encode sweep ของเทสอีกไฟล์หนึ่ง ไม่ใช่ตั้งใจ):
    5859 passed, 323 skipped, 11148 subtests passed, 0 failed (214.27s)
ไฟล์ที่แตะรอบนี้ (pirate-force-server) รวม 6: mob_ai_scheduler.py [ใหม่],
  tests/test_mob_ai_scheduler.py [ใหม่], tests/test_mob_aggro.py, tests/test_mob_ai_control.py,
  tests/test_mob_stat_fabrication_guard.py, rounds/B_20260831_1850_256rvs.md
git diff --check: silent
```

## ยังไม่ได้พิสูจน์

- BUILD-006 wire สุดท้าย ยังรอ `GT-146` (attended) เหมือนเดิม -- ไม่เปลี่ยนจากรอบก่อน
- `mob_ai_scheduler.tick_session` ยังไม่เคยถูกเรียกด้วยข้อมูล session จริง (แค่ roster/ledger
  สังเคราะห์จาก `field_mobs.load_roster()`/`mob_combat.open_ledger()` ในเทส) -- ยัง production_allowed
  = True ตามกฎ (ไม่มี flag/scenario gate ใด ๆ) แต่ "ไม่เคยถูกเรียกจริง" ต่างจาก "ถูกเรียกแล้วพัง"

## nonclaim

ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`/`scenarios/world_*.json`/
`scenarios/combat_*.json` ไม่อ้าง milestone เกมเพลย์ใหม่ -- โมดูลใหม่รอบนี้ยังไม่มี importer ใน `src/`
เลย (พิสูจน์ด้วยเทส ไม่ใช่แค่บอกปาก) ไม่แตะเขตสาย A (`scenarios/world_*.json`)

## pf-adversary

Agent tool (`subagent_type` `pf-adversary`) ไม่มีอยู่ในชุดเครื่องมือรอบนี้เหมือนรอบก่อน ๆ ที่บันทึกไว้
(`p3olrt` เป็นต้น) -- ทำการทวนแบบ adversarial ด้วยตัวเองแทน: (1) เช็คว่า `tick_session` mutate
register ที่ได้รับไหม -- ไม่ (dataclass frozen + เทสยืนยัน) (2) เช็คว่า mismatch ระหว่าง register/ledger
เงียบไหม -- ไม่ (`MobCombatContractError` โผล่ตรง ๆ มีเทสปักไว้) (3) เช็คว่า docstring อ้างสิ่งที่โค้ด
ไม่ได้ทำ (composeเฟรม) ไหม -- ไม่พบ อ่านซ้ำทุกประโยคใน "WHAT THIS MODULE IS NOT" เทียบกับโค้ดจริงแล้ว

-- LANE-B (COMBAT) รอบ `256rvs`
