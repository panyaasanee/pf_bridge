# LANE-B รอบ `jop8ph-2` — pf-adversary กลับมาแล้ว และมันหักคำอ้างพาดหัวของรอบก่อน

เปิดรอบ 2026-08-29T20:2x+07:00 · เขียน 20:53+07:00
repo: `pirate-force-server` (PR ใหม่ · รอบ `jop8ph` merge ไปแล้ว `7f4107f`)
สาขา: `claude/funny-volta-jop8ph` (รีเซ็ตจาก main ตามกฎ PR-merged-แล้ว)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ผู้เล่นที่ล็อกอินเข้า Prison Exile Island จะไม่ได้ actor ศูนย์ตัว ในสภาพที่รอบก่อนเปิดช่องไว้เอง**

รอบ `jop8ph` (merge แล้ว) เขียนไว้ในโมดูลของตัวเองว่า containment คือ precondition
**อันเดียว** ที่ `mob_death.repopulation_entries` โยน — *"Nothing else is."*
pf-adversary วัดแล้วว่า **มันมีสี่** และรอบก่อนเช็คหนึ่ง

```
ledger ที่ _sync_combat_scene_state ประกอบ + มอนหนึ่งตัวเลือด 0 + ยังไม่ commit การตาย
   (runtime.py:4327 เขียนเองว่าสภาพนี้ "shipped and disclosed")

รอบ jop8ph :  MOB_LEDGER_ADMISSION ... state=same_scene admitted=yes covered=12/12
              -> ส่งต่อ -> MobDeathContractError ในเธรด listener -> ผู้เล่นได้ actor 0 ตัว
รอบนี้     :  MOB_LEDGER_ADMISSION ... state=ledger_disagrees_with_register admitted=no
                                        conflicts=0x2033 register=checked
              -> ไม่ส่งต่อ -> ประกอบ census ตามปกติ -> ไม่โยน
```

## ① ชะตา PR รอบก่อน

| repo | PR | ผล |
|---|---|---|
| `pirate-force-server` | `#275` | ✅ merged `7f4107f` |
| `pf_bridge` | `#434` + `#439` | ✅ merged (`#439` คือ commit ที่ `#434` วิ่งแซง) |

⇒ ดีเฟกต์ทั้งหมดข้างล่าง **อยู่บน main แล้ว** รอบนี้จึงเป็นการแก้ของที่ปล่อยไปแล้ว ไม่ใช่การกันไว้ก่อน
สาขารีเซ็ตจาก main ใหม่ตามกฎ (PR เดิม merge แล้ว ห้ามต่อ commit ทับประวัติที่ merge ไปแล้ว)

## ② ที่ adversary จับได้ และรอบนี้แก้

### 🔴 D1 (ระดับ 1) — คำอ้าง *"Nothing else is"* เป็นเท็จ

`repopulation_entries` โยนสี่อย่าง รอบก่อนเช็คหนึ่ง:

| # | เงื่อนไข | ที่ | รอบก่อน | รอบนี้ |
|---|---|---|---|---|
| 1 | ledger ตอบแทน identity ไม่ได้ (containment) | `_balance_in` | ✅ | ✅ |
| 2 | เลือด 0 ใน ledger แต่ register ไม่ได้ถือว่าตาย | `mob_death.py:2140` | ❌ | ✅ |
| 3 | เลือด > 0 ใน ledger แต่ register ถือว่าตาย | `mob_death.py:2160` | ❌ | ✅ |
| 4 | ceiling ของ register ไม่ตรง roster | `:2168` | — | ของ register ไม่ใช่ของโมดูลนี้ |

⇒ `admit_ledger` รับ `register=` แล้ว · ตัวประกอบ census **ถือ register อยู่แล้ว** จึงส่งให้เสมอ
⇒ ผู้เรียกที่ไม่มี register ได้ `register=unchecked` บนบรรทัด **ไม่ใช่ความเงียบ**

### 🔴 D2 (ระดับ 1) — containment เทียบ *เซ็ตของ identity* เท่านั้น

ledger ที่มี ceiling มาจากตารางอื่น ผ่าน containment แล้วประกอบ body ที่แบก HP
ซึ่งไม่มีในตารางไหนของฉากนี้ — **ไม่โยน ไม่มีบรรทัด ไม่มีใครรู้**
วัดแล้ว: roster 3857 · ledger 11571 · admitted · ไบต์ออกไปพร้อม 11571
`mob_combat.strike` ปฏิเสธคู่นี้โดยมีชื่อมาตั้งแต่แรก (`REFUSE_LEDGER_ROW_DISAGREES_WITH_ROSTER`)
ทางฝั่ง census ไม่มีอะไรเลย · **เลขที่ประกอบผิดแย่กว่าการปฏิเสธ เพราะไม่มีอะไรรายงาน**

### D3 (ระดับ 2) — ยามป้ายฉากตายทางโครงสร้างสำหรับฉากที่ไม่มีตาราง

`if both_named and ...` ⇒ `scene_for_scene_id` คืน `None` สำหรับฉากที่ roster ว่างพอดี
⇒ `admit_ledger(997, <ledger ของ bg0001>)` พิมพ์ `scene=? ledger_scene=bg0001 state=same_scene
admitted=yes` **แล้วส่งต่อ** — บรรทัดที่ขัดกับตัวเองในบรรทัดเดียว
ไบต์ไม่เสียหาย (roster ว่าง override ก็ว่าง) แต่ **หลักฐานเสียหาย และชื่อสถานะคือหลักฐาน**

### D6 (ระดับ 3) — *"Decide, without raising"* คุ้มครองอาร์กิวเมนต์เดียวจากสาม

`scene_id` ที่อ่านไม่ได้ และ `roster=` ที่ไม่ใช่แถว roster **โยนทะลุออกไป**
ความไม่สมมาตรกลับด้าน: ตัวที่ถูกกันคือตัวที่ผู้เรียกมั่นใจที่สุด
⇒ `STATE_INPUTS_UNREADABLE` ทั้งคู่ และตัวห่อทั้งสองสืบทอดแทนที่จะโยนต่อ

### D4/D5 — สอง "การวัด" ที่เป็นสัจพจน์ (ตัวที่ถามหาไว้เอง)

- **D4**: `open_ledger_for_scene_id(..., scene=...)` เป็น **no-op ที่พิสูจน์ได้** —
  `scene_for_scene_id` คืน `None` สำหรับฉากเดียวกับที่ `roster_for_scene_id` คืน `()` เป๊ะ
  (ผ่าน `_SCENE_TABLE_MODULES` ตัวเดียวกัน) ⇒ อาร์กิวเมนต์เป็น `None` พอดีในเคสที่มันถูกเพิ่มมาเพื่อ
  🔴 และเทส `test_a_scene_with_no_roster_still_names_its_scene` **ตัวมันเองยืนยันตรงข้ามกับชื่อตัวเอง**
  (บรรทัด `assertIsNone(scene_for_scene_id(...))`) ⇒ เปลี่ยนชื่อ เขียนใหม่เป็นการพินความเท่ากัน
- **D5**: `roster=` ที่ส่งจากตัวประกอบเป็น pure call เดียวกันกับ default ⇒ ลบทิ้งสวีตยังเขียว
  ⇒ ขีดฆ่าคำอ้าง เก็บ plumbing ไว้ **พร้อมพินว่าวันนี้มันเท่ากัน** วันที่ไม่เท่าคือวันที่มีคนรู้

### D9 — ประโยคเก่าที่กลายเป็นเท็จเพราะรอบก่อน

`CombatLedger` docstring: *"two ledgers built from the same hits compare equal"* —
ตอนนี้ต้องมีป้ายเดียวกันด้วย · ไม่มีผู้เรียกไหนพัง (adversary หาแล้วหาไม่เจอ) แต่ประโยคผิดอยู่ดี ⇒ แก้

## ③ ที่ยังไม่แก้ และบอกว่าไม่ได้แก้

- **D7**: `runtime.py:6752` ยังไม่ส่ง `override=`/`ledger=` ⇒ บูตพิมพ์ `not_reported` ทั้งคู่
  **เป็นของ chief** ใบขอเดิม (`20260829_1955_LANE-B-CORE-REQUEST-*`) ยังยืน
- **D8**: `require_ledger_for_recompose` / `FATAL_TOKEN` **ไม่มีผู้เรียกในทรี** ⇒ บูตไหนก็พิมพ์ไม่ได้
  ข้อผูกพันของ COO ข้อ 3 ถูกปลดกับฟังก์ชันที่ยังไม่มีใครเรียก — เขียนไว้ตรง ๆ ว่ามันคือสภาพจริง
  งาน recompose R231 เป็นของ chief และเป็นคนที่จะเรียกมัน
- **baseline 60 เทสต่าง**: adversary วัด 4940 ที่ HEAD สายนี้วัด 5000 — ต่างที่ `capture/`
  ซึ่ง `.gitignore` ⇒ **ตัวเลขสวีตของสายนี้ re-derive จาก clean clone ไม่ได้** ไม่ใช่ดีเฟกต์ของดิฟนี้
  แต่เป็นข้อจำกัดของตัวเลขที่รายงาน เขียนไว้ให้เห็น

## ④ mutation sweep — ตัวที่ adversary เขียนแล้วรอด กลับมารันใหม่

| มิวแทนต์ (ของ adversary) | ก่อน | หลัง |
|---|---|---|
| M4 `open_ledger` เมิน `scene=` | รอด | **ตาย** |
| M5 ทิ้งยาม `derived is not None` | รอด | **ตาย** |
| M6 `missing` ไม่เรียง | รอด | **ตาย** |
| M7 ทิ้งการปฏิเสธชนิดของ `scene` | รอด | **ตาย** |
| M19 roster คละฉากได้ป้ายมั่ว | รอด | **ตาย** |
| M20 ข้ามยามป้ายเมื่อ roster ว่าง | รอด | **ตาย** (ดู ⑤) |
| M21 FATAL ไม่ยิงสำหรับฉาก vacuous | รอด | **ตาย** (ดู ⑤) |
| M1 `open_ledger_for_scene_id` ทิ้ง `scene=` | รอด | **ยังรอด — และถูกต้องที่รอด** (D4: มันเป็น no-op จริง) |
| M2 ตัวประกอบทิ้ง `roster=` | รอด | **ยังรอด — และถูกต้องที่รอด** (D5) |

🔴 **M1/M2 ยังรอดโดยตั้งใจ** สายนี้ไม่เขียนพินปลอมให้มันตาย — มันเป็นโค้ดที่เท่ากันจริง
สิ่งที่เขียนแทนคือพินว่า **ความเท่ากันนั้นยังเป็นจริง** ⇒ วันที่มันไม่เท่ากันคือวันที่เทสแดง

มิวแทนต์ใหม่ที่รอบนี้เขียนเอง: `N1` ข้ามยาม ceiling · `N2` ข้ามยาม register ·
`N3` ยาม register มองทางเดียว · `N4` input ที่อ่านไม่ได้กลับไปโยน · `M2b` ตัวประกอบทิ้ง `register=`

## ⑤ หลักฐาน

```
=== D1: เลือด 0 ในเลข ไม่มีในทะเบียนการตาย ===
MOB_LEDGER_ADMISSION scene_id=2 scene=Bg0002 ledger_scene=Bg0002
    state=ledger_disagrees_with_register admitted=no covered=12/12 missing=none
    conflicts=0x2033 register=checked vacuous=no
composer: no raise                      <- รอบก่อน: MobDeathContractError

=== D2: ceiling ของ ledger ไม่ตรง roster ===
    state=ledger_row_disagrees_with_roster admitted=no conflicts=0x2033
composed bytes now identical to the no-ledger composition: True   <- รอบก่อน: ส่ง 11571 ออกสาย

=== ของดีต้องยังผ่าน (bb094f0 ของ chief) ===
    state=same_scene admitted=yes covered=12/12 conflicts=none register=checked
wounded body still reaches the wire: True
```

**สวีตเต็ม: `5045 passed · 327 skipped · 8866 subtests`**

**ชั้น client-observable — ไม่มี และรอบนี้ไม่อ้างว่ามี**

## ⑥ บรรทัดคอนโซลเปลี่ยนรูป — ผู้เทสต้องอ่านใหม่

```
MOB_LEDGER_ADMISSION scene_id=.. scene=.. ledger_scene=.. state=.. admitted=..
                     covered=N/M missing=.. conflicts=.. register=checked|unchecked vacuous=..
```

- `conflicts=` ใหม่: identity ที่ ledger **ตอบคนละอย่าง** (ต่างจาก `missing` ที่แปลว่า **ตอบไม่ได้**)
- `conflicts=not_measured` แปลว่าการเทียบยังไม่ได้รัน (ปฏิเสธไปก่อนแล้ว) **ไม่ใช่ "ไม่มีปัญหา"**
  — บทเรียนเดียวกับ `missing=not_measured` ของรอบก่อน คนละฟิลด์ ห่างกันหนึ่งรอบ
- `register=unchecked` แปลว่าเงื่อนไข 2/3 ข้างบน **ไม่ได้ถูกตรวจ** ⇒ `admitted=yes` คู่กับ
  `register=unchecked` บอกชัดว่าตรวจไปแค่ไหน

## ⑦ pf-adversary รอบนี้

🔴 **ยังไม่ได้รันซ้ำบนดิฟของรอบนี้** — รอบนี้ *เกิดจาก* รายงานของมัน และเวลาที่มันใช้จริงคือ
40 นาที (สั่งรัน 19:4x คืนผล 20:2x) ⇒ การรอรอบที่สองแปลว่ารอบนี้ไม่ได้ push
สายนี้ push ก่อนตามข้อ E แล้ว **เขียนไว้ว่ารอบนี้ยังไม่ผ่าน adversary เช่นกัน**
รายงานของมันบนดิฟรอบก่อนเก็บครบใน `notes_to_chief/20260829_2055_LANE-B-STATUS-*`

## ⓘ ของที่รอบนี้ทำพลาดเอง และ hook จับได้ก่อน merge

🔴 **commit ของรอบนี้ติดมิวแทนต์ที่ยังรันอยู่ไปด้วยหนึ่งตัว**

sweep เขียนมิวแทนต์ลงไฟล์จริง รันสวีต แล้วคืนไฟล์ใน `finally` — และ commit โค้ดของรอบนี้
ถูกทำ **ขณะที่ `M19` ยังอยู่ในไฟล์** ⇒ `mob_combat.py` ที่ push ไปมี
`derived = min(scenes) if scenes else None` ซึ่งคือ **ตัวดีเฟกต์ที่ M19 อธิบายเอง**
(roster คละฉากได้ป้ายมั่วแทนที่จะไม่มีป้าย)

- จับได้เพราะ stop-hook เตือนว่ามีไฟล์ที่ยังไม่ commit
- 🔴 **และรอบนี้อ่านทิศทางของ diff ผิดในตอนแรก** — เข้าใจว่าไฟล์ที่ยังไม่ commit *คือ* มิวแทนต์
  ความจริงกลับกัน: **ของที่ commit ไปแล้วคือมิวแทนต์** ส่วน working tree คือของจริงที่ sweep คืนมา
  ⇒ ถ้าเชื่อการอ่านครั้งแรกแล้วไม่ตรวจซ้ำ มิวแทนต์จะอยู่ใน PR ต่อไป
- ทัน: `#282` ยังไม่ merge ⇒ **มิวแทนต์ไม่เคยถึง main** · แก้ด้วย commit `58a51aa`
- 🟢 **พินของรอบนี้เองคือสิ่งที่จับมันได้**: `test_a_mixed_scene_roster_leaves_the_ledger_unscoped`
  แดงกับเวอร์ชันที่ commit ไป เขียวกับเวอร์ชันที่แก้แล้ว — พินที่เขียนเพื่อฆ่า M19 ฆ่า M19 จริง
  แม้ตอนที่ M19 เข้ามาทางที่ไม่มีใครตั้งใจ

**กฎที่เขียนไว้ให้ทุกสาย:** ห้าม commit ขณะที่ mutation sweep กำลังรันบนทรีเดียวกัน
ให้รอ sweep จบ แล้ว `git status` ต้องสะอาดก่อน commit

## ⑧ หนี้

1. D7 (ของ chief) · D8 (ยังไม่มีผู้เรียก จนกว่า R231 จะมา)
2. ตัวเลขสวีต re-derive จาก clean clone ไม่ได้ (`capture/` ถูก ignore) — ของทั้งโปรเจกต์ ไม่ใช่ของสายนี้
3. `_SCENE_TABLE_MODULES[key].SCENE == key` ยังไม่มีที่ไหน assert — ยกมาห้ารอบติด
