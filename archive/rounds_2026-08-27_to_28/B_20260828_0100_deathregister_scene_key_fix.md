[LANE-B (COMBAT) · round `y1fqrc` · 2026-08-28T01:00+07:00]

# ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
**ไม่มีอะไรเปลี่ยนบนจอ** -- รอบนี้เป็น server-side bookkeeping ล้วน ไม่แตะ wire format, ไม่แตะ
`actor_identity` ที่ส่งจริง, ไม่มี byte ไหนบนสายเปลี่ยน. ผลที่ผู้เล่นได้ประโยชน์จะมาเมื่อ Bg0002
เปิดบูตจริงพร้อม bg0001 ในเซสชันเดียว (ยังพักตาม M2/PANYA-DECISION 2026-08-27T20:10) -- ตอนนั้น
สองมอนที่บังเอิญมี wire identity ชนกันข้ามฉากจะตายแยกกันถูกต้อง แทนที่จะฆ่าตัวหนึ่งแล้วอีกตัวใน
อีกฉากถูกนับว่าตายไปด้วย

# 0 ล็อกรอบ
ตรวจ `list_pull_requests` ทั้งสอง repo ก่อนแตะไฟล์: ไม่มีใบ `[LANE-B]` เปิดค้าง (PR ล่าสุดของสาย B
คือ `pf_bridge#248`/`pirate-force-server#156` รอบ `n04gzk`, ทั้งคู่ `merged=true` จริง -- งานอยู่บน
`main` แล้ว ไม่ต้องกู้คืนตามข้อ A ของ ADDENDUM v2) ยึดล็อกด้วย branch ที่ session นี้ถืออยู่แล้ว
(`claude/friendly-ride-y1fqrc`, `claude/admiring-galileo-y1fqrc`) แทนการเปิด branch ใหม่ -- นี่คือ
branch ที่ระบบมอบให้ session นี้โดยตรง ตรงกับรูปแบบเดิมที่ทุกรอบก่อนหน้าใช้ branch เฉพาะของ session
ตัวเอง (`n04gzk`, `k25cur`, `wcpm2h`, ...)

# 1 กล่องจดหมาย
กวาด `notes_to_chief/*.md` หาใบที่ไม่มี `.CONSUMED.txt` คู่กันและเป็นของสาย B จริง เจอ:

1. `20260827_2249_COO-DECISION-actor-identity-scene-key-fix.md` -- ตอบ ASK-COO ของรอบ `k25cur`
   (`20260827_2153_...actor-identity-needs-a-scene-term.md`) **ตกหล่นจากรอบ `n04gzk`** (รอบนั้นปิด
   ~23:1x-23:4x แต่ใบนี้มาก่อนแล้วตั้งแต่ 22:49 -- อ่านพลาดหรือ mailbox scan ของรอบนั้นตรวจแค่ใบหลัง
   จุดเริ่มรอบตัวเอง) **บริโภครอบนี้เต็มที่**: implement ตามที่ตัดสิน (ดูหัวข้อ 3) เขียน stub
   `.CONSUMED.txt` แล้ว
2. `20260827_2250_COO-DECISION-widen-death-scope-stage2-ruling-name.md` และ
   `20260827_2259_CHIEF-REPLY-COO-widen-death-scope-stage2-already-landed.md` -- ทั้งคู่ addressed
   ถึง chief เป็นหลัก (cc สาย B) chief ตอบเองแล้วว่าไม่ต้องทำอะไรเพิ่ม (คำเคาะซ้ำของสิ่งที่ทำไปแล้ว
   ตั้งแต่ 13:50) **ไม่สร้าง stub เพราะไม่ใช่ใบที่สาย B เปิดเองหรือ addressed ถึงสาย B โดยตรง** อ่าน
   แล้วรับทราบเฉยๆ

# 2 ของที่เขียนจริงรอบนี้ -- implement COO-DECISION 2249

**การตัดสิน**: `FieldMob.actor_identity` (`0x2000 + placement_index + 1`) ไม่มีมิติ scene --
`field_mobs.cross_scene_identity_collisions()` วัดชนจริง 4 คู่ระหว่าง bg0001/Bg0002 วันนี้ (เช่น
placement 58 -> `0x203B` ทั้งคู่: bg0001's Jungle Big Tiger กับ Bg0002's Fighting Fish soldier)
COO เลือกทางเลือก 3: ไม่แก้สูตร wire เลย (ทางเลือก 1/2 ถูกปฏิเสธ) แก้แค่ `DeathRegister` ฝั่ง
เซิร์ฟเวอร์ให้คีย์ด้วยคู่ `(scene, actor_identity)`

**แก้จริงใน `pirate-force-server`**:
- `src/pirateforce_foundation/mob_death.py`: `DeathRecord`/`DeathRegister` รับ `scene: str` เป็น
  ส่วนหนึ่งของคีย์ (`DEFAULT_SCENE` = bg0001 ให้ทุก call site เดิมที่ไม่เคยรู้จัก scene ทำงานต่อได้
  โดยไม่ต้องแก้) -- `is_dead()`, `record_of()`, `with_death()`, sort order, duplicate-check ทั้งหมด
  อัปเดตให้ใช้คู่คีย์แทนตัวเดียว
- `src/pirateforce_foundation/mob_ai_control.py`: เพิ่มคอมเมนต์อธิบาย (ไม่แก้ logic) ว่าทำไม
  `reconcile()`'s `is_dead(row.actor_identity)` (arg เดียว) ยังตั้งใจปล่อย scene-blind รอบนี้ --
  ผูกกับ `FakeDeaths.is_dead(self, identity)` ใน `tests/test_mob_ai_control.py` ที่จะพังทั้งคลาสถ้า
  ขยายเป็นสอง arg ตอนนี้ และชนกันไม่ได้จริงในวันนี้เพราะ `MobAiRegister`/`DeathRegister` ทั้งคู่สร้าง
  จากฉากเดียวต่อเซสชันเสมอ (M2 ยังพัก) -- ทิ้งเป็นของค้างให้แก้ตอน M2 ปลดพัก ไม่ใช่ตอนนี้
- `tests/test_mob_death.py`: แก้ 1 call site เดิม (`is_dead(mob.actor_identity)` ของมอน Bg0002 ตัว
  หนึ่งที่จะพังเงียบๆ ถ้าไม่ระบุ scene) + เทสใหม่ 2 ตัว: เทสตรงกับ API สังเคราะห์ + เทสข้อมูลจริงใช้
  `cross_scene_identity_collisions()` คู่ placement 58 พิสูจน์ว่าตายแยกฉากได้จริง

**ตัวเลขที่วัดได้**: `tests/test_mob_death.py` 80 -> 82 (ผ่านทั้งหมด) `tests/test_mob_ai_control.py`
ผ่านทั้งหมดไม่มีอะไรพัง (137 เทสรวมสองไฟล์, รันยืนยันเองอีกครั้งก่อน commit ไม่ได้เชื่อแค่รายงานของ
agent) full suite: 3750 -> 3752 (มีเทสใหม่ 2 ตัว) error 18 จุดเดิมเท่าเดิม (ทั้งหมด `capstone`
import ตอน collect ไม่ใช่บั๊กรอบนี้) ไม่มี FAIL ใหม่

# 3 pf-adversary (ทำโดย builder agent ก่อนส่งมาให้ commit)
พบจริง 1 จุด แก้แล้ว: `test_the_bg0002_ruling_authorises_every_real_bg0002_roster_mob` เรียก
`is_dead(mob.actor_identity)` เปล่าสำหรับมอน Bg0002 ตัวหนึ่ง -- จะเช็คกับ `DEFAULT_SCENE` (bg0001)
เงียบๆ แล้วพังหลังแก้ ไม่ใช่ error ที่เห็นชัด แก้โดยส่ง `mob.scene` เข้าไปด้วย

พบแล้วตั้งใจไม่แก้รอบนี้ (บันทึกไว้ ไม่ใช่ของค้างที่ซ่อน): `mob_ai_control.reconcile()`'s call site
(เหตุผลดูข้อ 2) และ `mob_combat.CombatLedger` มีความเสี่ยงคีย์เดียวกันตามหลักการเดียวกันที่ใบ
ASK-COO เดิมเคยตั้งคำถามไว้ แต่ COO-DECISION 2249 สั่งเฉพาะ `DeathRegister` เท่านั้น -- ไม่ขยายเอง
เกินคำสั่ง

# 4 หลักฐานสองชั้น
| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | เทส unit เขียว 3752/3752 (ไม่นับ error เดิม 18 จุด) พิสูจน์ logic ฝั่งเซิร์ฟเวอร์ |
| **client-observable** | ไม่มี -- ไม่มีอะไรเปลี่ยนที่จอผู้เล่นเห็นได้รอบนี้ (bookkeeping ล้วน ไม่ต้อง
  GT ใหม่) |

# 5 CORE-REQUEST
none -- `runtime.py`'s call site ที่มีอยู่แล้วส่ง `FieldMob` เข้า `mob_death.kill()`/`commit_death()`
อยู่แล้ว scene จึงอยู่ใน scope ให้ chief ใช้ได้ทันทีถ้าต้องการ ไม่มี signature ไหนเปลี่ยนแบบ breaking
(พารามิเตอร์ใหม่ทั้งหมด optional มี default)

# 6 เปิดใบให้สาย C
none

# 7 เขตเขียนรอบนี้
`pirate-force-server`: `src/pirateforce_foundation/mob_death.py` (แก้),
`src/pirateforce_foundation/mob_ai_control.py` (แก้ คอมเมนต์เท่านั้น), `tests/test_mob_death.py`
(แก้) -- commit `ef68a69`
`pf_bridge`: ไฟล์นี้ (ใหม่), `notes_to_chief/20260828_0100_LANE-B-STATUS-deathregister-scene-key-fix.md`
(ใหม่)
ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/`scenarios/world_*.json` เลยสักบรรทัด

# 8 ถ้าผิดต้องย้อนอะไรบ้าง
`git revert ef68a69` ใน `pirate-force-server` (การเปลี่ยนแปลง backward-compatible ทุกจุด
`DEFAULT_SCENE` ทำให้ revert ปลอดภัย ไม่มี caller ไหนพังถ้าย้อน)

-- **สาย B · COMBAT**
