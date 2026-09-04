# LANE-B รอบ `hlwgri` — 2026-09-05T01:31+07:00 (เริ่ม) · ไฟล์รอบเขียน 01:5x+07:00

รหัสรอบ (session): `hlwgri` · claim PR: `pf_bridge#1237` (เปิด 01:33 ไม่มี marker ตามกติกา) ·
takeover: ไม่มี · กิ่ง: `claude/youthful-ride-hlwgri` (bridge) · `claude/sharp-newton-hlwgri` (server)

## NOW.md ขยับข้อไหน

**ขยับ "งานด่วนตอนนี้" → หาง P-1 → ครึ่ง "หายไป" ของ `RE-208`** (บรรทัด `NOW.md` ที่เขียนว่า
"B เลือก (ข) `refresh_frames` ต่อท้ายหมัดไม่ฆ่า รับแล้ว") — รอบนี้สร้างตัวประกอบของตัวเลือก (ข)
ซึ่ง **ไม่เคยมีอยู่จริงบน main** และส่งบรรทัดเดียวให้ chief เดินสาย

ข้อที่ **ไม่** ขยับ และเพราะอะไร:
- **M2 / "รอเครื่องคุณ" ทุกข้อ** — ของเครื่อง Panya ทั้งหมด ไม่ใช่โค้ด (`GT-247` แฟล็กอยู่บน main แล้ว)
- **P-2 (สีชื่อมอน)** — ทิศปัจจุบันเป็นใบ RE ของ GM/RE ไม่ใช่เขต B (`RE-222` ปิดทิศเดิม)
- **M4 ข้อ (1) `apply_hp_damage` caller** — พักตามที่ COO อนุมัติไว้ (`MOB_AI_PLAYER_DAMAGE_WIRING_ON_HOLD`,
  `2050`) จนกว่า Door B (`MOB_HIT_FRAME_CONFIRMED`) จะเปิด
- **ฉาก 4** — พักตาม `1450` ข้อ 3 จนกว่าฉาก 3/5/14 สักฉากจะครบทุกประตู

## 1 ตรวจล็อก + ชะตา PR รอบก่อน (ADDENDUM ข้อ A)

- `[LANE-B]` open ต้นรอบ: **ไม่มี** ทั้งสองรีโป (bridge: `#1235` GM, `#1236` A · server: `#778` DB)
  ⇒ ไม่ต้องถอย ไม่ต้องยึดต่อ · เปิด claim `#1237` แล้ว list ซ้ำ: ไม่มีใบ `[LANE-B]` ที่เก่ากว่า
- ใบล่าสุดของสาย state=closed: server `#776` **merged=true** (2026-09-04T17:44:32Z) ·
  bridge `#1229` **merged=true** (17:21:06Z) ⇒ **ไม่มีงานหายจาก main ให้กู้**

## 2 กล่องจดหมาย (ข้อ B)

ค้าง `ADDRESSEE: LANE-B` ที่ยังไม่มี stub: **หนึ่งใบ** ·
`20260905_0033_SYNC-NOTICE-pirate-force-server-pr766-closed-never-merged.md`

บริโภคแล้ว: **ไม่มีอะไรต้องกู้** — สอง commit ของ `#766` ถูก cherry-pick ไปกับรอบ `0ugubw`
และขึ้น main ทาง `#771` · **วัดจาก main รอบนี้ ไม่ได้อ่านจากบันทึกรอบก่อน**:
`mob_death_persistence.py:742` `seed_the_session_state` มีตัวแก้ atomic rollback ครบ
(`mutated` เป็นตัวแปรท้องถิ่น · except คืนวัตถุสองตัวของผู้เรียกเดิม) · stub + สำเนาเข้า `consumed/` แล้ว

## 3 งานหลักของรอบ — ตัวเลือก (ข) ที่ถูกรับไว้ตั้งแต่ 3 ก.ย. แต่ไม่เคยถูกเดินสาย

### สิ่งที่วัดได้ (หลักฐาน wire/โครงสร้าง ชั้นที่หนึ่ง)

`COO-DECISION 20260903_1942` ข้อ 4 รับ (ข) ไว้คำต่อคำว่า *"`refresh_frames` ต่อท้ายหมัดที่ไม่ฆ่า"*
รอบนี้วัด `origin/main`:

| ที่ | สิ่งที่เห็น |
| --- | --- |
| `mob_combat.py:2849` | สาขาไม่ฆ่าของ `strike()` คืน `(announce_frame, bar_frame)` เท่านั้น |
| `mob_combat.py:2536` | `CombatStep.frames` = สองเฟรม ไม่มีที่ให้เฟรมพื้น |
| `runtime.py:5100-5292` | ช่วงประกอบคำตอบของหมัด **ไม่มี** `mob_loot` / `mob_drop_presence` / `ground` เลย |
| `runtime.py:5293` | `if step.death_due:` — เฟรมพื้นทุกเฟรมอยู่ใต้บรรทัดนี้ |
| `runtime.py:5721` | `sustain_a_kill(self.mob_loot_cell, legacy, drops)` = ทางเดียวที่พื้นถูกส่ง |

⇒ main วันนี้ = "วาดพื้นใหม่ตอนฆ่า" (ครึ่ง **โผล่กลับ**) · ครึ่ง **หายไป** ยังว่างเปล่า
🔴 จดหมายของสายผมเอง `20260904_0447` เคยบอก chief ว่า (ข) รันอยู่แล้วที่ `runtime.py:5586` —
ที่อยู่นั้นคือ **สาขาตาย** ⇒ หนี้ถูกบันทึกว่าจ่ายทั้งที่ไม่เคยจ่าย (อาการเดียวกับที่ `COO 1849` เตือน)
รอบนี้คือรอบที่จ่ายคืน และแก้คำในใบใหม่ถึง chief

### สิ่งที่สร้าง (เขต LANE-B ล้วน)

`src/pirateforce_foundation/mob_drop_presence.py`
- ใหม่ `reannounce_ground_after_a_surviving_blow(cell, legacy, step)` — **NEVER RAISES** คืน tuple เสมอ
  - `step.death_due is True` → ปฏิเสธโดยระบุชื่อ (`refused_the_blow_killed_kill_path_owns_it`)
    เพราะสาขาตายส่ง generation เดียวกันอยู่แล้ว — หมัดเดียวห้ามส่งซ้ำสองครั้ง
  - `death_due` ที่ไม่ใช่ bool จริง (ไม่มีฟิลด์ · `None` · `0` · `1` · property ที่ raise) →
    **fail closed** คนละชื่อ (`refused_step_death_due_unreadable`) ไม่ใช่ชื่อเดียวกับข้อบน
  - นอกนั้นประกอบด้วย `sustain_a_kill(cell, legacy, ())` + `loot_actions` = **ไบต์เดียวกับสาขาตาย**
    ไม่ใช่ encoder เส้นที่สอง
  - โทเคน `GROUND_REANNOUNCE_AFTER_A_SURVIVING_BLOW` / `GROUND_REANNOUNCE_REFUSED_AFTER_A_SURVIVING_BLOW`
    — **ไม่ใช่** สตริงที่ `GT-242` grep เป็น negative control และไม่ใช่คำนำหน้าของกันเอง
- ใหม่ `GROUND_SURVIVING_BLOW_WIRING` = บรรทัดเดียวสำหรับ chief (ใบ `0145`)
- แก้ `reannounce_ground`: ทุกบรรทัดออกทาง `_say_world_line` — docstring เดิมเขียนว่า NEVER RAISES
  ทั้งที่ `print` เปล่า ซึ่งคือรอยแผล cp874 ที่ pf-adversary วัดไว้เองรอบ `59iqwi` (D7)
  ⇒ คอนโซลที่เขียนไม่ได้ต้องเสีย **บรรทัด** ไม่ใช่ **เฟรม**

`tests/test_mob_drop_presence_surviving_blow.py` (ใหม่) — 21 เทส 6 subtests

### ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่เห็นอะไร จนกว่า chief จะใส่บรรทัดเดียวใน `runtime.py`** — รอบนี้ไม่มีผู้เรียก และไฟล์รอบเขียนไว้ตรง ๆ
แทนที่จะอ้างเป็นอย่างอื่น · เมื่อบรรทัดนั้นลง main: ป้ายชื่อของบนพื้นจะไม่หายชั่วขณะตอนผู้เล่นตีมอนตัวถัดไป
(`GT-223` ขั้น 8 คือหลักฐานชั้นสอง และป้าย `[LANE-B ASSUMPTION - AWAITING COO CONFIRMATION]` คงอยู่จนกว่าจะผ่าน)

## 4 จดหมายของรอบ

- `20260905_0145_LANE-B-CORE-REQUEST-one-line-ground-after-a-surviving-blow.md` (chief) — บรรทัดเดียว
  + แก้คำในใบ `0447` ของสายเอง + ข้อสังเกตเรื่องคำนำหน้าโทเคนของ `GT-242`
- `20260905_0146_LANE-B-ASK-COO-option-b-was-ratified-but-never-wired.md` (COO) — ตัดสินเองแล้วเดินต่อ
  สองข้อที่ขอให้เคาะ: (1) นับเป็น repeated-resend ตามใบ `1742` หรือไม่ (ผมอ่านว่าไม่ · ใบ `1942`
  ใหม่กว่าและแคบกว่า) (2) cadence ของบรรทัดคอนโซล

## 5 pf-adversary

<!-- ADVERSARY -->

## 6 เทส

- ระหว่างทำงาน (เฉพาะไฟล์ที่แตะ): `pytest tests/test_mob_drop_presence_surviving_blow.py` → 21 passed
  · `pytest tests/test_mob_drop_presence.py tests/test_mob_drop_presence_ground_reannounce.py
  tests/test_mob_drop_presence_wiring.py tests/test_mob_drop_presence_sustained_resend_hypothesis.py
  tests/test_npc_interaction_wire.py` + ไฟล์ใหม่ → **134 passed, 39 subtests**
- **มิวแทนต์ (พิสูจน์ว่าเทสจับได้จริง ไม่ใช่ผ่านเพราะเข้าไม่ถึง)**:
  1. ถอดรั้ว `death_due is True` และ `is not False` ทั้งคู่ → **5 เทสแดง** (รวมใบที่พิสูจน์ว่า
     หมัดเดียวไม่ส่ง generation ซ้ำ)
  2. เอา `_say_world_line` ออกจาก `reannounce_ground` กลับเป็น `print` เปล่า → **2 เทสแดง**
- 🔴 ระหว่างทาง เทส `test_mob_drop_presence.py` สองใบแดงเพราะ **อักขระ non-ASCII หนึ่งตัว** (🔴)
  ที่ผมพิมพ์ลงคอมเมนต์ในโมดูล — เทสอ่านซอร์สด้วย codec ascii · ลบแล้ว ซอร์สทั้งสองไฟล์เป็น ASCII ล้วน
  (กติกาบ้าน "โค้ดเป็น ASCII อังกฤษ" มีฟันจริง ไม่ใช่ธรรมเนียม)

<!-- FULLSUITE -->

## 7 งานสำรอง (สามข้อ ตาม `COO 1450` ข้อ 6 — เริ่มได้ทันทีถ้างานหลักถูกบล็อก)

1. **หนี้ `DropLedgerCell` ค้างฉากเดิมเมื่อผู้เล่นเดินข้ามขอบฉาก** — จุดเรียกตอนของตก + `drop_key`
   ระดับเซิร์ฟเวอร์เป็นของ B (`1844` ข้อ 5) แม้ตัวใบ `GT-225` จะเป็นของ chief
2. **หนี้ "ของผี 120 วิ"** (`1942` ข้อ 5.3): ของหมดอายุแล้วไม่มีเฟรมออก ⇒ ไคลเอนต์เห็นของที่เก็บไม่ได้ ·
   เส้นเดียวกับ `_expiry_publication` ที่ `#689` เปิดไว้ครึ่งทาง
3. **ฉาก 3/5/14 ให้ครบทุกประตู (ฆ่า+ดรอป) สักฉาก** เพื่อปลดฉาก 4 ตาม `1450` ข้อ 3 —
   ห้ามเปิดใบ GT ตีมอนจน P-2 ปิด จึงเป็นงานโค้ด+เทสล้วนจนกว่า P-2 จะปิด

## 8 nonclaim

① ไม่อ้างว่าป้ายชื่อเลิกกะพริบบนจอ — ยังไม่มีผู้เรียก และ `GT-223` ขั้น 8 ยังไม่รัน
② ไม่แตะ `runtime.py` / `app.py` / v141 ③ ไม่แตะ `store.py` / migration / canonical DB
④ ไม่แตะเขตสาย A (`scenarios/world_*.json`) ⑤ ไม่แตะหัวใบใน `GAME_TEST_QUEUE.md` ของใครทั้งสิ้น
(รวมถ้อยคำขั้น 8 ที่ยังผิด — ส่งให้ chief แก้ในใบ `0145`) ⑥ ไม่เปิดใบ GT ใหม่ (ใบตีมอนถูกห้ามจน P-2 ปิด)
⑦ ไม่อ้างว่าตัวเลือก (ข) ถูกต้อง — มันถูก **รับ** ไว้ และป้ายสมมติยังติดอยู่ตามที่ใบ `1942` สั่ง

## 9 สถานะท้ายรอบ

<!-- STATUS -->
