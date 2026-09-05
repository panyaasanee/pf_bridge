# LANE-B รอบ `dggvou` — ปิดสองหนี้ adversary ของรอบก่อน แล้ว adversary รอบนี้เจอหนี้ใหม่ในของที่เพิ่งแก้

เริ่ม 2026-09-06T00:05+07:00 · สาย B · COMBAT
PR เซิร์ฟเวอร์ของรอบนี้: **pirate-force-server#867** (เปิดแล้ว ไม่ draft · มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด · รอเกต)
claim PR: **pf_bridge#1397**

## รอบนี้ขยับ NOW ข้อไหน

- **ไม่ขยับตัวเลข M ใด ๆ** เหมือนรอบก่อน — M4 หลัก (`apply_hp_damage`) ยังพักรอ Door B ส่งจริง
  ตามที่ `NOW.md` เขียนเอง จุดต่อสายจริงของ D11 ยังรออยู่ที่บรรทัดใน `runtime.py`
  ซึ่งเป็นเขตของ chief
- **ทำไมไม่ขยับ**: รายการ LANE-B ที่เหลือใน `NOW.md` ยังติดของ chief ทั้งหมดเหมือนรอบก่อน
  รอบนี้จ่ายหนี้ adversary สามข้อที่รอบ `2zybdx` ตั้งใจยกมาให้ (ข้อ 1-3 ของ "รอบหน้าทำอะไร")
  แล้ว adversary ของรอบนี้เองก็เจอหนี้ใหม่ในโค้ดที่เพิ่งเขียน ซึ่งจ่ายในรอบเดียวกันเลย
- **ไม่แตะ `NOW.md`** ตามกติกาเดิม

## ล็อกรอบ

- ต้นรอบ list `[LANE-B]` open ทั้งสองรีโป: pf_bridge **ไม่มี** · pirate-force-server
  **ไม่มี** · `#853`/`#861` ของรอบก่อนปิด/merge ไปแล้ว
- claim = `pf_bridge#1397` branch `claude/practical-knuth-dggvou` ไม่ draft ไม่มี marker
  ตั้งแต่เปิด (เติมตอนจบรอบ) · list ซ้ำหลังเปิด: ไม่มี `[LANE-B]` ใบอื่น ไม่แพ้ใคร

## กล่องจดหมาย

- `ADDRESSEE: LANE-B` ที่ไม่มี `.CONSUMED.txt` คู่: **ไม่มี** (grep ทั้ง `notes_to_chief/*.md`)
- ตรวจสอบ debt เก่า "หนี้ `DropLedgerCell` ค้ามฉากเดิมเมื่อผู้เล่นข้ามฉาก" (`NOW` หาง P-1,
  ยกมาจากรอบ `2zybdx` ข้อ 4): **ไม่ใช่ของค้างที่ไม่มีใครแตะ** — มี CORE-REQUEST เดิมอยู่แล้ว
  (`notes_to_chief/20260904_1652_LANE-B-CORE-REQUEST-seed-the-ground-when-a-session-learns-its-scene.md`,
  รอบ `59iqwi`) chief อ่านแล้วรอบ `ub8svt`/R341 (stub `.CONSUMED.txt` ยืนยัน) แต่ตอบว่า
  "ยังไม่ต่อสายรอบนี้ ... ยกเป็นงานแรกรอบหน้า" — ยังไม่มีรอบไหนของ chief หยิบขึ้นจริง
  โค้ดฝั่ง LANE-B (`mob_ground_persistence.py`/`mob_drop_presence.py`) พร้อมอยู่แล้วบน main
  บรรทัดที่ขอมีระบุพิกัดแม่นในจดหมายเดิม (`runtime.py` ตอน arrival census + ก่อน
  `enter_scene_frames` ~7012) ⇒ **ไม่เปิดใบซ้ำ** เพราะใบเดิมยังไม่ถูก refute/cover
  ยืนยันด้วย `grep -n "seed_cell\|describe_seeded" runtime.py` = ไม่พบ (ยังไม่ต่อสาย)

## 1-2. D11 + D10 — สองหนี้ของรอบ `2zybdx`

รอบก่อน (`2zybdx`) เปิด `commit_death()` hook แต่ adversary เจอสองข้อที่ยกไว้ให้รอบนี้:

**D11 (โค้ดจริงในไฟล์ของสายนี้เอง)** — บั๊กคือ `runtime.py` ทั้งสองจุดเขียน
`self.mob_death_register = mob_death.commit_death(...)` เป็นสเตตเมนต์เดียว: hook เดิมยิง
จาก *ข้างใน* ฝั่งขวาก่อน assignment เกิด ⇒ subscriber ที่ปีนกลับไปอ่าน
`self.mob_death_register` ระหว่าง fire เห็นค่า**ก่อน**การตายนี้ พิสูจน์ด้วยเทสที่จำลอง
สเตตเมนต์จริงของ `runtime.py` (`test_the_ordering_hazard_is_real_on_the_undivided_call`):
เห็น `False` ระหว่าง fire แม้หลังสเตตเมนต์จบจะเป็น `True` แล้ว

แก้ในไฟล์ของสายนี้เอง (ไม่แตะ `runtime.py`) — แยก `commit_death()` เป็นสามส่วน:
`_commit_death_core()` (compare-and-swap + เขียนสมุดโลก, **ไม่**ยิง hook) →
`fire_mob_death_hook()` (ยิงจริง) → `commit_death()` เดิม = เรียกสองอันติดกันไม่มีช่องว่าง
(พฤติกรรมเดิมไบต์ต่อไบต์ ยืนยันด้วยเทสเดิม 18 ตัวผ่านไม่ต้องแก้บรรทัดไหน) +
`commit_death_and_prepare_hook()` ใหม่ให้ผู้เรียกเขียน register กลับก่อนยิงเอง — ยังไม่ได้
wire เข้า `runtime.py` (เขตของ chief) ส่งเป็น CORE-REQUEST พร้อมพิกัดบรรทัดแม่น
(`runtime.py:5424-5426`, `:5484-5486`) แทน:
`notes_to_chief/20260906_0014_LANE-B-TO-CHIEF-mob-death-hook-fires-before-register-write-back.md`

**D10 (ใบ ไม่ใช่โค้ด)** — วัดจริงว่า subscriber ที่ `time.sleep()` บล็อกเธรดผู้เรียกเต็มเวลา
(`test_a_slow_subscriber_blocks_commit_death_for_its_full_duration`) แต่ตัว dispatcher
(`lane_hooks/__init__.py::fire`) อยู่นอกเขตเขียนของสายนี้ (`prompts/LANE-B.md` ให้แค่
`lane_hooks/lane_b_*`) และผลกระทบเป็นระดับสถาปัตยกรรม (แตะทั้ง 13 point ไม่ใช่แค่
`mob_death`) — ลองทำ watchdog ใน `mob_death.py` เองไม่ได้เพราะไฟล์นี้มีเทสของตัวเองห้าม
import `threading`/`time` (`test_mob_death.py::test_nothing_is_installed_by_importing_this_module`)
เขียนเป็น ASK-COO/CORE-REQUEST แทน:
`notes_to_chief/20260906_0015_LANE-B-TO-CHIEF-mob-death-hook-has-no-timeout.md`

## 3. D1 ครึ่งที่เหลือ (`first_in_the_world` ต้องมีคนดูจอจริง)

**ยังไม่ทำรอบนี้** — งบเวลารอบนี้ไปกับ D11/D10 + หนี้ adversary ใหม่ (ข้างล่าง) หมด
ยกไปรอบหน้าอีกครั้ง (ข้อ 1 ของ "รอบหน้าทำอะไร") ไม่ใช่ลืม

## หนี้ใหม่ที่ adversary รอบนี้เจอ ในโค้ดที่รอบนี้เองเพิ่งเขียน — จ่ายในรอบเดียวกัน

สั่ง `pf-adversary` **หนึ่งครั้ง** ต้นรอบพร้อมเริ่มงาน (จากสองครั้งที่กติกาให้) ผลคืนก่อน push
เจอ**ข้อบกพร่องจริงหนึ่งข้อ วัดด้วยการรันจริง** และปัญหาป้ายกำกับหลักฐานอีกหนึ่งข้อ:

**ยิง `PendingMobDeathHook` เดิมซ้ำสองครั้งได้ ไม่มีอะไรกัน** — adversary ยิง `pending`
ตัวเดียวกันเข้า `fire_mob_death_hook()` สองครั้งด้วยมือ ได้ event `mob_death` สอง event
สำหรับการตายครั้งเดียว — เป็นบั๊กประเภทเดียวกับที่ `first_in_the_world` ทั้งกลไกมีไว้กัน
(สองเซสชันฆ่ามอนเดียวกัน) ที่เปิดกลับมาอีกชั้นหนึ่งซึ่ง `first_in_the_world` มองไม่เห็น
(payload สอง fire เหมือนกันทุกไบต์) จดหมาย D11 ที่เสนอให้ `runtime.py` เรียก
`commit_death_and_prepare_hook()` แล้ว `fire_mob_death_hook()` แยกกันสองสเตตเมนต์ คือ
รูปแบบที่ตัวห่อ retry หรือการ copy/paste ผิดระหว่างสองจุดเรียกจะยิงซ้ำได้ง่ายที่สุด

แก้แล้ว: เปลี่ยน `PendingMobDeathHook` จาก `NamedTuple` เป็นคลาสมี `__slots__` +
flag ส่วนตัว `_fired` · `fire_mob_death_hook()` เช็ค/ปักธงก่อนแตะประตู `lane_hooks`
ยิงซ้ำครั้งที่สอง raise `MobDeathContractError(REFUSE_HOOK_ALREADY_FIRED)` ไม่ถึง subscriber
ไหนเลย (เทสใหม่ `test_firing_the_same_pending_hook_twice_is_refused` ปัก)

**คำอ้างเท็จในคอมเมนต์ของเทสตัวเอง** — `test_a_raising_subscriber_on_the_split_path_costs_only_the_hook`
อ้างว่า "มิวแทนต์ที่ถอด try/except ออกจาก `fire_mob_death_hook` จะทำให้เทสนี้แดง" adversary
ถอดจริงแล้วรัน: เทสนี้**ยังเขียวอยู่** เพราะ `lane_hooks.fire()` เองแยก exception ของแต่ละ
subscriber ไว้แล้วชั้นหนึ่งก่อนจะถึง `mob_death.py` — try/except ของ `fire_mob_death_hook`
ป้องกัน `from . import lane_hooks` พัง ไม่ใช่ subscriber ที่ raise แก้คอมเมนต์ให้ตรงกับ
สิ่งที่วัดได้จริงแล้ว ไม่แตะตัวเทส (เทสยังปักของจริงอยู่ แค่คำอธิบายผิด)

**ตรวจแล้วไม่ใช่บั๊ก** (บันทึกไว้กันขุดซ้ำ): สงสัยว่าการย้าย `PendingMobDeathHook(...)` ไป
อยู่นอก try/except (ต่างจาก `commit_death` เดิมที่สร้าง args ข้างในตัว try) จะทำให้
`AttributeError` จาก `step.record` ที่พังหลุดออกไปแทนที่จะถูกกลืนแบบเดิม — ตรวจ
`DeathStep.__post_init__` แล้ว: บังคับ `type(self.record) is DeathRecord` เป๊ะ ซึ่งมีฟิลด์
ครบเสมอ ⇒ เส้นทางนี้สร้างไม่ได้จริงในโค้ดวันนี้ ไม่ใช่บั๊กที่มีชีวิต

adversary ยังยืนยันว่าพิกัดบรรทัดในจดหมาย D11 (`runtime.py:5424-5426`/`:5484-5486`)
ตรงกับ `origin/main` HEAD จริง และโค้ดแทนที่ 3 บรรทัดที่เสนอ วางในบล็อก
`try/except mob_death.MobDeathContractError` เดิมได้ถูกต้องไม่กระทบเส้นทาง refuse

## เทส

- `tests/test_mob_death_lane_hook_point.py`: 18 → 25 เทส (เพิ่ม 7: หกตัวของ D11/D10
  บวกหนึ่งตัวปักการปฏิเสธยิงซ้ำ) ทุกตัวยิง `commit_death()`/`fire_mob_death_hook()` ตัวจริง
- ชุด mob_death ที่เกี่ยวข้องทั้งหมด: **226 passed, 660 subtests passed**
- ชุดเต็มบนต้นไม้สุดท้าย (`71bf9d4`, `origin/main` `387666e` เป็นบรรพบุรุษอยู่แล้ว ไม่มี
  merge ใหม่ระหว่างรอบ): **11431 passed, 355 skipped, 21121 subtests passed** (408s)
- `pf_gate_preflight.py --repo pirate-force-server`: **PASS** ทุกช่อง (cp874 · ไม่มี skip
  ใหม่ · main อยู่ในกิ่ง · precondition census ตรง · ขนาดไฟล์กลางไม่โต) · ไม่ได้เพิ่ม/ลบ/
  ย้าย skip และไม่ได้เพิ่มไฟล์เทสใหม่ (แก้ไฟล์เดิม) ⇒ ไม่ต้องซ้อม `pytest_subset`/`skip_census`
  รอบนี้ · `--pr-body ... --pr-stage final`: **PASS** (marker หนึ่งบรรทัดพอดี)

## เกต (PANYA-DECISION `20260904_1158` §22)

**GATE_UNVERIFIED #867** — เปิด PR 00:3x+07 ยังไม่รอผล job `gate` ครบ 10 นาที ปล่อยล็อก
ตามลำดับจบรอบ ไม่รอ merge

## รอบหน้าทำอะไร

1. **D1 ครึ่งที่ยังไม่ปิด** (ยกมาจากรอบ `2zybdx` เป็นครั้งที่สอง): `first_in_the_world`
   พิสูจน์ด้วยเทสเท่านั้น ไม่เคยมีใครดูสองไคลเอนต์จริงฆ่ามอนตัวเดียวกันบนจอ — ควรเป็นใบ GT
   มีบล็อก `ATTENDED:` (ผ่าน pf-queue-author) ไม่ใช่คำยืนยันจากเทสอีกต่อไป
2. ติดตามว่า chief หยิบ CORE-REQUEST D11 (`0014`)/D10 (`0015`) ไปทำหรือยัง — ยังไม่ใช่
   บล็อกเกอร์ของใคร (ไม่มี subscriber จริงบน point นี้) แต่ค้างนานเข้าจะเสี่ยงมากขึ้นเรื่อย ๆ
3. หนี้ ground-seed เดิม (`20260904_1652`) ยังรอ chief หยิบเป็น "งานแรกรอบหน้า" ตามที่
   ตัวเองสัญญาไว้ตั้งแต่ R341 — ไม่ใช่ของสายนี้ต้องทำต่อ แค่เฝ้าดู
4. `RE-157` Job 1 (TradeCmd stamp) ถ้ามีที่ว่าง: เปิด CORE-REQUEST ถึง chief ตามที่ `2155` บอก
   (ยังไม่ทำอีกรอบ)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี** เหมือนรอบก่อน — รอบนี้ปิดรูในกลไกที่สายอื่นจะมาต่อ (และปิดรูใหม่ที่เพิ่งเปิดเอง
ระหว่างทาง) ไม่มีเฟรมใหม่ถูกส่ง ไม่มีข้อมูลโลกถูกแตะ ยังไม่มีใครลงทะเบียนบน point
`mob_death` เลยสักราย สิ่งที่เปลี่ยนคือ: (1) ผู้เรียกในอนาคตของ `runtime.py` มีเครื่องมือ
ปิดช่องว่างลำดับเวลาได้จริงแล้ว รอแค่ chief ต่อสาย (2) ถ้า/เมื่อต่อสายแล้ว การยิงซ้ำโดย
ไม่ตั้งใจ (เช่น retry-on-failure) จะถูกปฏิเสธด้วยชื่อแทนที่จะส่ง event ปลอมให้ทุก
subscriber เงียบ ๆ

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยวตรง ๆ รอบนี้ — ไม่มีบรรทัดไหนแตะ `runtime.py` หรือเส้นทาง
wire ใด ๆ ทั้งหมดอยู่ในฟังก์ชันของ `mob_death.py` เองและเทสของมัน (กลไก compare-and-swap
per-session เดิมที่รอบ `2zybdx` วัดไว้แล้วไม่เปลี่ยน)

SCOREBOARD: COMING | ยังไม่มีอะไรที่ผู้เล่นทำได้ต่างจากเมื่อวาน แต่ตัวเชื่อม hook ที่เควสจะเกาะปลอดภัยขึ้นสองชั้น (ลำดับเวลาปิดได้เมื่อ chief ต่อสาย, ยิงซ้ำถูกปฏิเสธแทนที่จะนับผิด) | pirate-force-server#867 · pf_bridge#1397 · sha 71bf9d4
