# LANE-B รอบ `jop8ph` — ledger รู้แล้วว่าตัวเองเป็นของฉากไหน และสาขาฉาก 2 รับมันได้แล้ว

เปิดรอบ 2026-08-29T19:32+07:00 · เขียน 19:5x+07:00
repo: `pirate-force-server` PR #275 · `pf_bridge` PR #434
สาขา: `claude/funny-volta-jop8ph` · `claude/affectionate-bardeen-jop8ph`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

🔴 **ในตัวเกม: ยังไม่เห็น และรอบนี้ไม่อ้างว่าเห็น** — ไบต์ที่ออกสายบนบูตวันนี้ยังไม่เปลี่ยน
เพราะสองคีย์เวิร์ดที่ทำให้มันเปลี่ยนอยู่ใน `runtime.py` ซึ่งเป็นเขตของ chief (ข้อ ⑧)

สิ่งที่ต่างคือ **สิ่งที่จุดเรียกทำได้**:

```
เมื่อวาน  ส่ง ledger ของ session เข้าสาขา Bg0002  -> MobDeathContractError ที่ 0x2033
                                                     โยนใน listener thread = ผู้เล่นได้ actor 0 ตัว
          ไม่ส่ง (ที่ทำอยู่จริง)                    -> มอนที่เพิ่งโดนตี กลับเลือดเต็มทุก recompose

วันนี้    ส่งอะไรมาก็ได้                            -> ไม่มีทางโยน
          ledger ของฉากอื่น -> ปฏิเสธ + พิมพ์บอก + ประกอบ census ไบต์เท่าเดิมเป๊ะ
          ledger ของฉากนี้  -> ใช้จริง แผลรอด recompose
```

## ① ข้อ A ของ ADDENDUM v2 — ชะตา PR รอบก่อน (`z096sw`)

| repo | PR รอบก่อน | ผล (ถามจาก GitHub API ไม่ใช่จาก `rounds/`) |
|---|---|---|
| `pirate-force-server` | `#272` | ✅ merged `2026-08-29T12:27:16Z` |
| `pf_bridge` | `#430` | ✅ merged `2026-08-29T12:21:44Z` |

⇒ งานรอบก่อนอยู่บน main จริง ไม่มีอะไรต้อง cherry-pick

## ② ข้อ B — กล่องจดหมาย

**บริโภคสองใบ** (ทั้งคู่ถึงสายนี้ ทั้งคู่ยังไม่มี stub · สำเนาไป `consumed/` ครบ ไม่ลบต้นฉบับ):

1. `20260829_1842_COO-DECISION-census-race-window-accepted-until-recompose.md`
   ครบสามข้อ และ **ข้อ 3 ถูกสร้างเป็นโค้ดในรอบนี้** ไม่ใช่รับทราบ:
   `require_ledger_for_recompose` + `describe_recompose_admission`
   🔴 สายนี้เลือก **log FATAL ไม่ใช่ raise** ซึ่งคำตัดสินอนุญาตไว้เองในประโยคเดียวกัน
   เหตุผลอยู่ใน docstring: raise ในจุดนั้นแลก "มอนตัวหนึ่งเลือดเต็ม" กับ "โลกว่างทั้งโลก"
2. `20260829_1912_RE-150-RESULT-NO-AGGRO-MONSTER-OUTSIDE-REFUSED.md`
   ⇒ M6 "มอนเริ่มตีเอง" **สร้างจาก corpus ปัจจุบันไม่ได้** โดยไม่ขัดคำสั่งเจ้าของ
   ⇒ พิน `test_no_monster_this_lane_ships_initiates_in_either_scene` ที่รอบก่อนให้ "อายุ"
   ไว้ว่า *ยืนจนกว่า RE-150 ปิด* — RE-150 ปิดแล้ว **พินยังอยู่ ด้วยเหตุผลที่แข็งกว่าเดิม**:
   วัดแล้วว่าไม่มีอะไรให้วาง ไม่ใช่แค่ยังไม่มีใครมอง
   🔴 **DRIFT ที่รายงาน ไม่แก้เอง:** `CLIENT_RE_QUEUE.md:2454` หัวใบ `RE-150` ยังเขียน `[OPEN]`
   ขณะที่ผลรายงาน `DONE/BOUNDED-NEGATIVE` · ใบนี้ chief เปิด สายนี้ไม่แตะหัวใบคนอื่น

**ใบที่สายนี้เปิดและยังไม่มีคำตอบ:** `20260829_0258` · `0549` (ไม่บล็อกรอบนี้)

## ③ ข้อ C (ป้ายเวลา)

heartbeat ล่าสุด `19:30:02+07:00` · `TZ=Asia/Bangkok date` ตอนเปิดรอบ `19:32+07:00`
⇒ ต่าง 2 นาที ผ่าน · ตรวจก่อน push ตามกฎ ไม่ใช่หลัง

## ④ ที่ ship

### (ก) `CombatLedger` ได้ฟิลด์ `scene` — และมันไปถึง ledger ตัวจริงโดยไม่ต้องแก้จุดเรียก

`open_ledger()` **อ่านฉากจากแถว roster เอง** (`mob.scene` ซึ่งมีอยู่แล้วและ `mob_death` อ่านอยู่แล้ว)
🔴 **นี่คือข้อที่สำคัญที่สุดของครึ่ง (ก)**: `runtime.py` เปิด ledger ด้วย `open_ledger()` เปล่า ๆ
ใน `PersistentGameSessionState.__init__` ตอนที่ session ยังไม่มีฉาก ⇒ ถ้าป้ายฉากมาทาง
คีย์เวิร์ดใหม่อย่างเดียว **ledger ตัวเดียวที่เซิร์ฟเวอร์จริงถืออยู่จะไม่มีป้ายตลอดไป**
และทั้งรอบนี้จะเป็นทฤษฎี · วัดแล้ว: `session ledger scene = bg0001 rows = 4`

- roster ที่แถวไม่ตรงกัน ⇒ **ไม่มีป้าย ไม่ใช่ปฏิเสธ** (unscoped เป็นสถานะที่มีชื่อ)
- `scene=` ที่ผู้เรียกใส่เอง **ถูก join กับที่ derive ได้** ⇒ ขัดกันคือปฏิเสธ
- `""` เป็นฉาก **ถูกปฏิเสธ**: มันอ่านว่า "ไม่มีฉาก" ที่ `if ledger.scene:` และอ่านว่า
  "ฉากชื่อว่าง" ที่ `is None` — หนึ่งในสองผู้อ่านผิดเสมอ จึงไม่ให้เขียนเลย
- `with_balance` **พาป้ายไปด้วย** และ `diag_multi_object_wiring` (จุดเดียวในทรีที่ประกอบ
  ledger เองด้วย positional) ก็พาไปด้วยแล้ว — ไม่งั้น ledger จะมีป้ายจนถึงวินาทีที่มีคนใช้มัน

### (ข) โมดูลใหม่ `mob_ledger_admission.py` (สาย B · ไม่มีแฟล็ก · `production_allowed`)

`admit_ledger(scene_id, ledger, roster=...)` คืน **record** ไม่ใช่ bool — ทุกผู้เรียกที่มีจนถึงตอนนี้
ต้องการเหตุผลด้วย (คนหนึ่งพิมพ์ อีกคนยกระดับเป็น FATAL เฉพาะเหตุผลเดียว)

🔴 **สองสัญญาณ และมันไม่เท่ากัน:**
- **คำประกาศ** = `CombatLedger.scene` · ประกาศไม่ตรง = ปฏิเสธทันที ไม่ว่า membership จะพอดีแค่ไหน
- **ความจริงภาคพื้น** = **containment**: ledger ตอบแทนทุก identity ของ roster นี้ได้ไหม
  ซึ่งคือ precondition ที่ `mob_death.repopulation_entries` โยนอยู่จริง ๆ **อันเดียว ไม่มีอย่างอื่น**

🔴 **containment ถูกเช็คแม้ป้ายจะตรงกัน** และนั่นไม่ใช่ความระวังส่วนเกิน: ledger ที่เปิดสำหรับ
`Bg0002` **ก่อน** ตัวกรอง owner-refusal เปลี่ยนว่าแถวไหน ship มี identity คนละชุดกับ roster วันนี้
และจะโยนทั้งที่ป้ายทั้งสองข้างอ่านว่า `Bg0002` ⇒ ป้ายคือคำอ้าง membership คือสิ่งที่บรรทัดถัดไปจะทำจริง

**สถานะที่เป็นไปได้ ทุกตัวมีชื่อ ไม่มีตัวไหนเงียบ:**
`same_scene` (ใช้) · `unscoped_covers_roster` (ใช้ พิสูจน์ด้วย containment) ·
`other_scene` · `same_scene_incomplete` (ตัวที่เคยโยน) · `unscoped_incomplete` ·
`absent` · `ledger_unreadable`

### (ค) บรรทัดคอนโซลที่ผู้เทส grep อยู่แล้ว ได้ฟิลด์ `ledger=`

`describe_census_hostility(..., ledger=...)` — **ไม่ใช่บรรทัดใหม่** เพราะค่าทั้งหมดของ (1)
จะหายไปถ้าบูตบอกไม่ได้ว่า ledger **ถูกใช้หรือถูกปฏิเสธ** · ผู้เรียกที่ไม่ส่งพิมพ์
`ledger=not_reported` (ช่องว่างที่มีชื่อ แบบเดียวกับ `override=`) · ส่ง `None` มาเองพิมพ์ `absent`
— "ไม่ได้บอก" กับ "ไม่มี" เป็นข้อเท็จจริงของคนละคน

## ⑤ หลักฐานสองชั้น

**ชั้น wire — วัดจริง ไม่ใช่ยกจากเทส** (สคริปต์เดินเส้นทางเดียวกับจุดเรียก census):

```
session ledger scene = bg0001 rows = 4        <- ledger ที่ runtime.py ถืออยู่จริง มีป้ายแล้ว

--- สิ่งที่จุดเรียกทำไม่ได้ก่อนรอบนี้ ---
MobDeathContractError: ledger_disagrees_with_register: the ledger cannot answer
for identity 0x2033 (target_not_in_ledger)

--- ข้อเสนอเดียวกัน ผ่านสายนี้ ---
declined, composed anyway: entries=12 identical_to_no_ledger=True
MOB_LEDGER_ADMISSION scene_id=2 scene=Bg0002 ledger_scene=bg0001 state=other_scene
    admitted=no covered=0/12 missing=0x2033,... vacuous=no
MOB_CENSUS_HOSTILITY ... override=12 ledger=other_scene

--- ledger ของฉากนี้เอง มอนหนึ่งตัวบาดเจ็บ ---
target 0x2033  max_hp=3857  wounded_to=1928
body bytes differ from the ceiling body: True
every other identity byte-identical: True
MOB_LEDGER_ADMISSION ... ledger_scene=Bg0002 state=same_scene admitted=yes covered=12/12
MOB_CENSUS_HOSTILITY ... ledger=same_scene

--- recompose ที่ไม่มีใครส่ง ledger มา (COO 18:42 ข้อ 3) ---
MOB_LEDGER_ADMISSION scene_id=2 ... state=absent ... missing=not_measured
MOB_LEDGER_ADMISSION_FATAL scene_id=2 reason=no_ledger_passed_to_recompose
    effect=every_wounded_monster_resent_at_its_ceiling
```

🔴 **`unbacked=` ในบรรทัดสาธิตด้านบนขึ้นครบ 12 ตัวเพราะสคริปต์ส่ง census identities เป็น `()`**
(ไม่ได้ประกอบ census จริงในสคริปต์นั้น) — เป็นของสาธิต **ไม่ใช่ดีเฟกต์** เขียนไว้กันอ่านผิด

**สวีตเต็ม:** ดูข้อ ⑨

**ชั้น client-observable — 🔴 ไม่มี และรอบนี้ไม่อ้างว่ามี** · `GT-084`/`RIDER-084-A` `OW1`-`OW3`
ยัง attended และยังไม่ได้รัน · และสองคีย์เวิร์ดยังไม่ต่อ ⇒ **บูตวันนี้ไบต์ไม่เปลี่ยน**

## ⑥ mutation sweep ที่รันเอง — 12 ตัว ตายทั้งหมด

| มิวแทนต์ | ผล |
|---|---|
| M1 ไม่เช็ค containment เลย (ตัดสินด้วยป้ายอย่างเดียว) | ตาย |
| M2 ไม่อ่านป้ายเลย (containment อย่างเดียว) | ตาย |
| M3 `ledger_for_scene` ส่งต่อทุกก้อน | ตาย |
| M4 ฟิลด์ `missing=` หายเมื่อว่าง | ตาย |
| M5 การปฏิเสธทุกแบบเป็น FATAL | ตาย |
| M6 ไม่มี ledger = admitted | ตาย |
| M7 ของที่อ่านไม่ได้ โยนแทนที่จะปฏิเสธ | ตาย |
| M8 `with_balance` ทำป้ายหาย | ตาย |
| M9 `open_ledger` ไม่ derive ฉากจาก roster | ตาย |
| M10 ตัวประกอบ census ข้ามการตัดสิน | ตาย |
| M11 บรรทัดคอนโซล hardcode `same_scene` | ตาย |
| M12 diag widening ทำป้ายหาย | **เคยรอด → เขียนพินเพิ่มแล้ว → ตาย** |

M12 คือตัวที่สอนอะไรจริง: การแก้ `diag_multi_object_wiring` ให้พาป้ายไปด้วย **ไม่มีพิน**
จนกระทั่งรันสวีปนี้ ⇒ โค้ดที่ไม่มีพินคือโค้ดที่ยังไม่ได้ยืนยัน

## ⑦ pf-adversary

<!-- ADVERSARY -->

## ⑧ ที่ขอจาก chief — สองคีย์เวิร์ด บนสองบรรทัดที่มีอยู่แล้ว

จดหมาย `notes_to_chief/20260829_1955_LANE-B-CORE-REQUEST-bg0002-census-may-now-take-the-ledger.md`

`runtime.py` สาขา Bg0002: `hostile_override_for_scene_id(..., ledger=self.mob_combat_ledger)`
และ `describe_census_hostility(..., override=override, ledger=self.mob_combat_ledger)`
**ไม่มีบรรทัดใหม่ ไม่ต้อง sync ก่อน ไม่ต้องรู้ว่า ledger ก้อนนั้นเป็นของฉากไหน**

🔴 **สายนี้ไม่แตะ `runtime.py` รอบนี้** — สิทธิ์ครั้งเดียวของข้อ G ถูกใช้ไปแล้วในรอบ `z096sw`

## ⑨ ตัวเลขสวีต

<!-- SUITE -->

## ⑩ หนี้ที่รอบนี้จดไว้ ไม่ได้แก้

1. **ledger lifetime ยังไม่มี** — ไม่มีอะไรในทรีนี้สร้าง ledger ใหม่เมื่อผู้เล่นข้ามฉาก
   รอบนี้ทำให้ ledger ของฉากหลังถูก **ปฏิเสธอย่างถูกต้อง** ซึ่งเป็นครึ่งที่ปลอดภัย
   อีกครึ่ง (จุด rebuild) ยังเป็นของ chief และยังเปิดอยู่
2. `admitted=True` บน roster ว่างเป็น **สัจพจน์ว่าง** — มี `vacuous` ให้แยกแล้ว แต่ยังไม่มี
   ผู้เรียกไหนอ่าน `vacuous` (วันนี้ยังไม่มีฉากที่ roster ว่างและมี census ให้ประกอบ)
3. `_SCENE_TABLE_MODULES[key].SCENE == key` ยังไม่มีที่ไหน assert — ยกมาสี่รอบติด
4. `docs/FUNCTIONAL_COVERAGE.json` ยังเขียนว่า Bg0002 มี 17 monsters — นอกเขตสายนี้
5. `CLIENT_RE_QUEUE.md:2454` `RE-150` ยัง `[OPEN]` (ข้อ ②) — ของ chief
