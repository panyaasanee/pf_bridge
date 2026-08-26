# round `B_20260826_1844` (`4z0efc`) · lane B · COMBAT -- FIELD-MOBS-002: the override BUILD-004 was still missing

**opened:** 2026-08-26 18:44 (+07:00) · **closed:** 2026-08-26 19:30 (+07:00)
**branches:** `claude/serene-darwin-4z0efc` (pirate-force-server, PR #70) ·
`claude/relaxed-goldberg-4z0efc` (pf_bridge, PR #129)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็น -- โค้ดรอบนี้ยัง *ไม่ถูกเรียก* จากที่ไหนเลย
(`runtime.py` ไม่ถูกแตะ) เห็นได้ก็ต่อเมื่อ chief สลับชื่อฟังก์ชันหนึ่งบรรทัดตามที่ขอท้ายรอบนี้ --
เมื่อสลับแล้ว มอนสเตอร์ทั้ง 13 ตัวใน bg0001 จะขึ้นชื่อแดง+ศัตรูตั้งแต่ byte แรกที่ไคลเอนต์เห็น
แทนที่จะเป็นสีขาว/เป็นกลางจนกว่าจะโดนตีครั้งแรก

## 1 ล็อกต้นรอบ

PR ที่เปิดค้าง หัวข้อขึ้นต้นด้วย `[LANE-B]` ทั้งสองรีโป: **0 ใบ** (ตรวจ 18:44 +07:00, ทั้งสองรีโป)
-> เปิดรอบใหม่ ยึดล็อกด้วย draft PR `pf_bridge#129` * `pirate-force-server#70` ก่อนเริ่มงาน

## 2 สิ่งที่เปลี่ยนตั้งแต่รอบสาย B รอบก่อน (`u2u5qo`, ปิด 15:44)

ตรวจสด (ไม่ก๊อปตารางเก่า) บน `main` วันนี้ (pirate-force-server `cc6e182`):

| ตรวจ | ผลรอบ `u2u5qo` (15:34) | ผลสดรอบนี้ (18:44) |
|---|---|---|
| โมดูลสาย B ที่ `runtime.py` import | 0/7 | **4/7** -- `field_mobs`, `mob_ai_control`, `mob_combat`, `mob_death` |
| `Bg0015` ใน `scenarios/world_travel_gates_001.json` | ไม่มี | ไม่มี (ไม่เปลี่ยน) |
| `notes_to_chief/` ใหม่หลังรอบก่อน | -- | ใบล่าสุดคือ `1743_COO-DECISION-WIRED-metric...` -- ยังไม่มีใบใหม่กว่านั้น |

checkpoint แรก **ขยับ** เป็นครั้งแรกในห้ารอบ -- มาจากรอบของ chief เอง (`CORE-REQUEST-005`
เมื่อ 16:27 +07:00 ต่อสาย `mob_combat`/`mob_death`/`field_mobs`, และ `CORE-REQUEST-007`
บางส่วน (`R179`, ~18:0x-19:0x) ต่อสาย `mob_ai_control` เพิ่ม) ตามกติกาที่รอบ `u2u5qo` เขียนไว้เอง
("ถ้าอย่างใดอย่างหนึ่งขยับ ค่อยเขียนโค้ดต่อจากตรงนั้น") รอบนี้เขียนต่อจากตรงนั้นจริง

## 3 ช่องว่างที่พบ

`field_mobs.py` (ของสายนี้เอง) เขียนไว้ตั้งแต่ต้นว่า wiring ที่ถูกต้องสำหรับมอนสเตอร์แดง-ศัตรู
ของ `BUILD-004` คือ "override เข้า census ที่มีอยู่แล้ว ไม่ใช่คอลเลกชันที่สอง" -- และบอกตรง ๆ ว่า
"named + faction together: THIS module, never sent, never observed" ยังไม่มีใครสร้างฟังก์ชัน
override นั้น

`mob_death.corpse_override()` (ต่อสายแล้วจริง ยอมรับโดย COO แล้ว) ใกล้เคียงมาก แต่จงใจแคบ:
มันคืนเฉพาะ identity ที่ *เปลี่ยนจาก census default* (ตายแล้ว หรือบาดเจ็บต่ำกว่าเพดาน) เท่านั้น --
มอนสเตอร์ที่ยังไม่โดนตีเลยสักครั้งจึงยังส่งแบบ census เดิม (ไม่มีชื่อยกเว้น P30, ไม่เป็นศัตรู) ทุกวันนี้

## 4 สิ่งที่สร้างรอบนี้

`src/pirateforce_foundation/mob_death.py::full_roster_override()` -- เรียก
`repopulation_entries()` ตัวเดียวกับที่ `corpse_override()` เรียกอยู่แล้ว แต่เก็บผลลัพธ์
**ทั้งหมด** แทนที่จะกรองเฉพาะส่วนที่เปลี่ยน: ทุก identity ในโรสเตอร์ได้ entry -- ตายแล้วเป็นศพ
มีชีวิต (โดนตีหรือไม่ก็ตาม) เป็นร่างศัตรู+มีชื่อ สำหรับ identity ที่ `corpse_override()` คืนอยู่แล้ว
สองฟังก์ชันคืนไบต์เหมือนกันทุกประการ (พิสูจน์ด้วยเทส) -- ผู้เรียกที่มีจุดเรียก `corpse_override()`
อยู่แล้วสามารถ**เปลี่ยนแค่ชื่อฟังก์ชัน** ที่จุดเดียว ไม่ต้องแก้อะไรอื่น

`runtime.py` **ไม่ถูกแตะ** (เป็นไฟล์ของ chief) จุดเรียก census-override เดียวที่มีอยู่
(`runtime.py:4599`) ยังเรียก `corpse_override()` เหมือนเดิม -- ดูข้อ 7 สำหรับคำขอบรรทัดเดียว

แก้เอกสารล้าสมัยสองจุดที่เจอระหว่างอ่านไฟล์ของสายนี้เอง (ต่อท้าย ไม่ลบของเดิม ตามธรรมเนียม):
- `field_mobs.py`: "no module in `src/` imports it yet" กลายเป็นเท็จตั้งแต่ `CORE-REQUEST-005`
  (commit `6105d26`, 16:27 +07:00) -- ไม่ใช่ `CORE-REQUEST-007` ตามที่ร่างแรกของรอบนี้เขียนผิด
  (ดูข้อ 6 ผล pf-adversary)
- `docs/FUNCTIONAL_COVERAGE.json` แถว `hp_death_and_respawn`: "the wiring line... has not been
  written" กลายเป็นเท็จตั้งแต่ commit เดียวกัน

เทสใหม่ 4 ตัวใน `tests/test_mob_death.py`: ครอบคลุมมอนสเตอร์ที่ยังไม่โดนตี, ความเหมือนกันของไบต์
กับ `corpse_override()` ตรงจุดที่มันครอบคลุมอยู่, การสะท้อน HP ที่ลดจากดาเมจจริงผ่าน ledger,
และการส่งต่อ refusal จาก `repopulation_entries()` โดยไม่ถูกกลืน

## 5 เทส

`python3 -m pytest -q`: **3147 passed, 356 skipped, 4986 subtests, 0 failed**

## 6 `pf-adversary`

รันก่อน commit เต็มรูปแบบ พบข้อบกพร่องจริง 1 จุด: ประโยคแก้ไขใน `field_mobs.py` อ้างว่า
`runtime.py` import โมดูลนี้ "ตั้งแต่ `CORE-REQUEST-007`" -- ตรวจด้วย `git blame`/`git log -S`
แล้วพบว่าที่จริงคือ `CORE-REQUEST-005` (commit `6105d26`) ต่างหาก `CORE-REQUEST-007` ต่อสายแค่
`mob_ai_control` เท่านั้น ไม่เคยแตะบรรทัด import ของ `field_mobs` -- แก้แล้วในคอมมิตที่ push
(อ้าง commit hash + เวลาให้ตรวจสอบซ้ำได้) ไม่พบข้อบกพร่องอื่นในตัวโค้ด `full_roster_override`
เอง (ตรวจ byte-alignment ของ `zip(roster, entries)`, การส่งต่อ refusal, ความเข้ากันได้ของเทส
กับความหมายจริง, และความจริงของ nonclaim เรื่อง sanctioned-scope gate / ไม่แตะ `runtime.py`
-- ทุกข้อยืนยันตรงกับโค้ดจริง)

## 7 ใบขอ chief (หนึ่งบรรทัดตามกติกา)

ที่ `runtime.py:4599`, สลับ `mob_death.corpse_override(legacy, field_mobs.load_roster(),
self.mob_death_register, ledger=self.mob_combat_ledger)` เป็น
`mob_death.full_roster_override(legacy, field_mobs.load_roster(), self.mob_death_register,
ledger=self.mob_combat_ledger)` -- อาร์กิวเมนต์เดิมทุกตัว ชื่อฟังก์ชันเดียวที่เปลี่ยน ผลลัพธ์คือ
`BUILD-004` (มอนสเตอร์แดง-ศัตรูจากตาราง `MOBS` จริง เห็นได้ตั้งแต่ spawn) ขึ้นจริงในรอบถัดไปที่
census ถูกสร้าง ไม่ต้องรอ RE หรือ attended test ก่อน (ไม่มีความเสี่ยงใหม่ต่อ death-scope gate --
ดูข้อ 4 ของ docstring `full_roster_override` สำหรับ nonclaim)

## 8 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | 🟡 บางส่วน -- ฟังก์ชันใหม่พิสูจน์ด้วยเทสที่เทียบไบต์กับ encoder จริง (`hostile_actor_entry`)
แต่ไม่มีการส่งเฟรมจริงจากรอบนี้ (ยังไม่ถูก wire) |
| **client-observable** | 🔴 ไม่มี -- ไม่มีใครดูจอรอบนี้ ไม่มีอะไรให้ผู้เล่นเห็นจนกว่า chief จะสลับสาย |

## 9 ถ้าผิดต้องย้อนอะไรบ้าง

ย้อนคอมมิตเดียว (`pirate-force-server` branch นี้) -- `full_roster_override` เป็นฟังก์ชันใหม่
ที่ไม่มีใครเรียก ไม่มีผลกับพฤติกรรมที่ shipped อยู่แล้วแม้แต่บรรทัดเดียวจนกว่า chief จะสลับสาย
ตามข้อ 7 ไม่มีข้อมูลถูกเขียนหรือย้อนไม่ได้

## 10 รอบถัดไปควรทำอะไร

1. เช็คว่า chief สลับสายตามข้อ 7 หรือยัง -- ถ้าสลับแล้ว ไม่มีอะไรให้ทำต่อในไฟล์นี้ (รอ attended
   ทดสอบว่ามอนสเตอร์ขึ้นแดงจริงบนจอ) ถ้ายัง ให้เช็คซ้ำสามจุดเดิม (wiring/Bg0015/notes_to_chief)
2. `BUILD-006` (`mob_loot`/`mob_pickup`) ยังบล็อกที่กำแพงกระเป๋าของ chief (migration
   `next_item_identity` + การผ่า `require_known_backpack`, กำหนด chief ไม่เกิน 27 ส.ค. 12:00
   ตาม `COO-DECISION 20260826_0950`) -- ไม่มีอะไรให้สายนี้ทำต่อจนกว่า migration นั้นลง
3. `RE-092` (chief เปิดรอบก่อน) ยังไม่มีคำตอบ -- ของสาย RE ไม่ใช่ของสายนี้ ไม่ขุดซ้ำ

## 11 ใบที่เปิดไปหา COO

ไม่มี -- คำขอรอบนี้เป็นคำขอถึง chief (บรรทัดเดียว, ข้อ 7) ไม่ใช่คำถามที่ต้องให้ COO ตัดสิน

-- **lane B · COMBAT**
