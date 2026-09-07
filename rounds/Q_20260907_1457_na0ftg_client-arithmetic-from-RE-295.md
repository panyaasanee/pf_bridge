# LANE-Q รอบ `na0ftg` — จ่ายเลขคณิตของไคลเอนต์เอง (บริโภค RE-295)

- เริ่ม: 2026-09-07T14:57+07:00 · ล็อก: `pf_bridge#1727` (`[LANE-Q] round na0ftg: claim`)
- ล็อกรอบ: list แล้วไม่มี PR หัว `[LANE-Q] round <id>: claim` เปิดค้าง (มีแต่ `#1583` ซึ่งเป็น **addendum** ของรอบ `uadtc7` ไม่ใช่ claim) ⇒ ไม่มี takeover
- ยืนยันของรอบก่อนถึง main แล้ว: `git merge-base --is-ancestor 500138b origin/main` = **จริง** (`#1037` merge เป็น `efbae4e`)

## รอบนี้ขยับ NOW/M ข้อไหน

`NOW.md` แถว **Q**: *"`Lv` = เลเวลผู้เล่น ปัดลง · ไม่รู้ = ปฏิเสธ (`0845`)"* — แถวนี้เขียนไว้ตอนที่มันยังเป็น **สมมติฐาน**
รอบนี้ RE-295 ตอบแล้ว และสาย Q บริโภคผลในรอบเดียวกันตามกฎ "ใครเปิดใบ คนนั้นบริโภคผล":
`Lv` เป็นเลเวลผู้เล่น **วัดแล้ว** · "ปัดลง" ถูกครึ่งเดียว (เป็นการ **ตัดทิ้งเข้าหาศูนย์**) · และ **ความกว้างของการคูณที่รอบก่อนเดา ผิด**
🔴 ไม่ขยับ M2/M3/M4 — รอบนี้ไม่มีอะไรที่ผู้เล่นเห็นบนจอ (ดู nonclaims)

## สิ่งที่ทำ — หกคำสั่ง คัดลอกมาทั้งชุด

RE-295 ถอด `0x00608D10` ออกมาว่าไคลเอนต์คำนวณรางวัลเควสด้วยหกคำสั่งนี้:

```
movss     xmm0,[esi+0x3c]   ; f_EXP อ่านเป็น float32
cvtsi2ss  xmm1,[esp+0x14]   ; ฐานจากตารางเส้นโค้ง int -> SINGLE
cvtss2sd  xmm1,xmm1         ; ขยายฐานเป็น double
cvtps2pd  xmm0,xmm0         ; ขยายตัวคูณเป็น double
mulsd     xmm1,xmm0         ; คูณที่ DOUBLE
cvttsd2si esi,xmm1          ; แล้วตัดทิ้ง (ไม่ขึ้นกับ FPU rounding mode)
```

`lua_api/quest_criteria.py`:
1. `client_product()` = ห้าคำสั่งแรก · `round_amount()` = คำสั่งที่หก · `resolve()` จ่ายจากมัน
2. `ROUNDING_MODE`: `ROUND_FLOOR` → **`ROUND_DOWN`** (คือสิ่งที่ `cvttsd2si` ทำ) — ตรงกันทุกค่าที่ mirror ผลิตได้ (ตัวตั้ง/ตัวคูณ ≥ 0 ทั้งหมด) ต่างกันเฉพาะใต้ศูนย์ ซึ่งเข้าถึงได้ทาง `resolve()` สาธารณะเท่านั้น
3. `CriteriaAmount.raw` = ผลคูณของไคลเอนต์ (จ่ายจากตัวนี้) · `.exact` = ผลคูณตามทศนิยมที่ **ผู้ออกแบบตารางพิมพ์** เก็บไว้เป็นที่มา · `log_fields()` พิมพ์ `authored=` เมื่อสองค่าต่างกัน
4. ถอดป้าย `[COO-ASSUMPTION 0845 - NOT A PROOF]` ออกจาก `LEVEL_SOURCE` · การปฏิเสธเมื่อไม่รู้เลเวลยังอยู่ และตอนนี้ตรงกับไคลเอนต์ (`0x00609308` กระโดดออกเงียบเมื่อไม่มีออบเจกต์ผู้เล่น)

🔴 **รอบนี้ถอนงานของรอบตัวเอง**: `wn088m` เดาว่าคูณที่ single แล้วกู้ทศนิยมของผู้ออกแบบ — การเดานั้นทำให้ **14 ค่าที่ shipped จ่ายเกินไปหนึ่งหน่วย** รอบนี้ขยับกลับลง
เควส **2170 จ่าย 22119 ไม่ใช่ 22120** เพราะไคลเอนต์ **โกงตารางของตัวเอง** หนึ่งหน่วย และเราตามไคลเอนต์ ไม่ตามตาราง

## หลักฐานสองชั้น (ไม่อ้างอิงกัน)

**ชั้นที่ 1 — พฤติกรรมของโค้ด (มิวแทนต์ วัดบนกิ่งนี้)**
คำสั่งรันซ้ำ: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests python3 -B -m pytest tests/test_script_lua_api_quest_criteria.py -q`

| มิวแทนต์ | ผล |
|---|---|
| ถอดขั้น `cvtsi2ss` (ฐานไม่ผ่าน float32) | **1 failed** |
| `ROUND_DOWN` → `ROUND_FLOOR` | **1 failed** (หมุดค่าติดลบ) |
| คูณที่ single (การอ่านแบบ `wn088m`) | **5 failed** |

**ชั้นที่ 2 — ตัวเลขจากคอร์ปัสจริง (คนละแหล่ง ไม่ใช่เทส)** วัดตรงจาก mirror ทั้งสองไฟล์ ทั้งสองการอ่าน:
`plain triples 4632 changed 14` · `all (row,level,kind) 1181160 changed 3632` · เควสที่ขยับ `{2170..2177}` · เฉพาะตัวคูณ `1.4` · `max base 14252800 < 2**24` · ตัวคูณต่างกัน 12 ค่า
ตรงกับตัวเลขที่ RE-295 ทำนายไว้ก่อนวัด และตรงกับเซตเดียวกับที่รอบ `wn088m` ขยับขึ้น — เดินกลับทางตรงข้าม

## nonclaims — สิ่งที่รอบนี้ **ไม่ได้** ทำ

- **ผู้เล่นยังไม่เห็นอะไรบนจอ** ไม่มี API ตัวไหนกลายเป็นของจริงเพิ่ม (ยัง 34/160) · ครึ่งจ่ายรางวัลยังไม่ต่อสาย
- **ขั้น `cvtsi2ss` ไม่มีแถวที่ shipped พิสูจน์** — ฐานทุกค่าในเส้นโค้งต่ำกว่า 2^24 (สูงสุด 14,252,800 วัดแล้ว) ⇒ ขั้นนั้นเป็น identity บนข้อมูลจริง หมุดของมันใช้ฐานที่ทำขึ้นเอง มันอยู่ในโค้ดเพราะคำสั่งทำแบบนั้น ไม่ใช่เพราะข้อมูลบังคับ
- **ไม่ได้ทำ "integer indefinite" (`0x80000000`) ของ `cvttsd2si`** เมื่อผลเกิน int32 — โมดูลคืนจำนวนเต็มจริง และไม่มีผลคูณของ `(row, level, kind)` ใดเข้าใกล้ขอบ
- **ไม่ได้วัดไบนารีเอง** ทุกบรรทัด VA ข้างบนคัดจากใบ RE-295 (โคลนคลาวด์ไม่มีไคลเอนต์)
- **ไม่ได้แตะ `gamedata/PF_GAMEDATA_LUA_API.tsv`** ที่ยังเขียนว่า `AddLvCriteriaExp` = `UNRESOLVED` — ไม่ใช่เขตสาย Q ส่งเป็นจดหมายถึง chief แทน (พร้อมเหตุที่ตัวสร้างพลาด: มันคาด `mov [esp+0x34]` หลัง push แต่จุดนี้ออก `mov [esp+0x18]` ก่อน push)
- **ยังไม่ได้ต่อ `add_typed_attribute` ของ LANE-DB** — วัดแล้วว่าเมธอดยังไม่ถึง main (`git grep -c add_typed_attribute origin/main -- src/pirateforce_foundation/store.py` = ไม่มีแถว บนคอมมิต `abe09f1`) ต่อรอบนี้ = โค้ดที่แดงบน main

## กล่องจดหมาย

- บริโภค **RE-295** (ใบของสาย Q เอง) — ใช้จริงในรอบเดียวกัน ไม่ใช่รับทราบ · วาง `.CONSUMED.txt` + สำเนาไป `consumed/`
- บริโภค **`20260907_1325_LANE-DB-TO-Q-add-typed-attribute-shipped`** (ตอบ CORE-REQUEST ของสาย Q) — เขียนเหตุที่ยังใช้ไม่ได้ลงสตับ พร้อมคำสั่งวัดซ้ำ
- ออกใหม่: `20260907_1508_LANE-Q-TO-CHIEF-fix-AddLvCriteriaExp-row-and-the-generator-pattern.md`

## pf-adversary — **ผลคืนก่อน push และจ่ายครบในรอบนี้ ไม่ใช่ PENDING**

สั่งตั้งแต่ต้นรอบ (หลังคอมมิตแรก) คืนแปดข้อ **จ่ายทั้งแปดในคอมมิตเดียวกัน**:

| ข้อ | สิ่งที่มันหา | จ่ายอย่างไร |
|---|---|---|
| D1 | คอมมิตแรกของรอบแก้โมดูลโดยไม่พาเทสไปด้วย ⇒ SHA นั้น **แดงเดี่ยว ๆ** (6 failed) — bisect/CI ต่อคอมมิตจะเจอ | ยุบสองคอมมิตของรอบเป็นใบเดียวก่อน push ⇒ ไม่มี SHA แดงบนกิ่ง |
| D2 | `_plain()` เรียก `Decimal.quantize` ⇒ `InvalidOperation` เมื่อเกิน 28 หลัก **ในตัวจัดรูป log ที่รันหลังจ่ายรางวัลไปแล้ว** (ทรง D11 เป๊ะ) | เขียนใหม่ไม่ใช้ `quantize` + รับ NaN/Inf ได้ + หมุด `1E+40` และ `resolve(...,1e21)` |
| D3 | `authored=` พิมพ์เมื่อ Decimal ต่างกันเฉย ๆ = **185 ครั้ง จริงแค่ 14** (สัญญาณปลอม 12:1) และ docstring ก็เขียนอีกอย่าง | เงื่อนไขเป็น `round_amount(exact) != amount` + เทสนับจาก mirror ทั้ง 185 และ 14 |
| D4 | `cvtsi2ss` อ่าน **signed DWORD** — โค้ดอ้าง "instruction for instruction" แต่ไม่ได้จำลองโดเมน int32 | base นอกช่วง int32 = **ปฏิเสธ ไม่ wrap** (ไคลเอนต์จะ wrap แล้วจ่ายติดลบ ซึ่งไม่มีใครเคยเห็น) |
| D5 | base ที่ไม่ใช่ตัวเลข ⇒ `TypeError` ดิบหลุดออกจากโมดูล · ข้อความ overflow อ้าง float32 ทั้งที่พังที่ double · พิมพ์เลข 401 หลักลง log | ปฏิเสธด้วยชื่อชนิด · ข้อความบอกขอบ int32 · บอกความกว้างเป็นบิต ไม่พิมพ์ค่า |
| D6 | ยาม non-finite เป็น `isinstance(multiplier, float)` ⇒ `Decimal`/`Fraction` เดินผ่านไปตายเป็น `InvalidOperation` | บังคับผ่าน `float()` + ปฏิเสธข้อความด้วยชื่อ |
| D7 | "`f_EXP` มี 12 ค่า" — จริง ๆ `f_EXP` มี **11** · 12 คือ union สามคอลัมน์ (`f_CASH` 3 · `f_SP` 6 · 0.85 อยู่ใน `f_CASH` เท่านั้น) | แก้ docstring + `docs/SCRIPT_LANE.md` ให้ตรงกัน |
| D8 | memo คีย์ด้วย float ⇒ `-0.0` กับ `0.0` ชนกัน หนึ่งครั้งแล้ว log ทุกบรรทัดต่อมาเป็น `mult=-0` | คีย์ด้วย **บิต float32** |

🔴 สิ่งที่ adversary **ตรวจแล้วไม่พัง** (บันทึกไว้เพราะเป็นหลักฐานฝั่งบวก): สร้าง reference อิสระด้วย `fractions.Fraction` + ปัดเอง 24/53 บิต แล้วเทียบทุกคู่ `(base, multiplier)` ที่ mirror ผลิตได้ 9,180 คู่ = **ไม่ต่างสักคู่** · `ROUND_FLOOR` vs `ROUND_DOWN` บน 1,181,160 ผลคูณ = **ต่าง 0** · ไม่มีเส้นทางคูณรางวัลที่สองในรีโป · log 900 บรรทัดเข้ารหัส cp874 ผ่านหมด

## เกต · ชุดเทส

- `python3 tools_bridge/pf_gate_preflight.py --repo <server> --pr-body <ไฟล์> --pr-stage final` = **PREFLIGHT PASS**
- ชุดเต็มบนต้นไม้สุดท้าย (`git merge origin/main` = Already up to date · คอมมิตเดียวจริงของรอบ `f2a99ec`):
  **`13401 passed, 401 skipped, 0 failed` ใน 615 วินาที** · จำนวน skip เท่าเดิมกับ main (401)
  คำสั่ง: `PYTHONPATH=src:tests python3 -m pytest tests/ -q`
- มิวแทนต์หกตัวหลังจ่าย adversary แล้ว (คำสั่งเดียวกับชั้นที่ 1 ข้างบน): ถอด `cvtsi2ss` = 1 failed · `ROUND_DOWN`→`ROUND_FLOOR` = 1 failed · คูณที่ single = 6 failed · `authored=` กลับไปเงื่อนไขกว้าง = 2 failed · ถอดด่าน int32 = 4 failed · `_plain` กลับไปใช้ `quantize` = 1 failed

## รอบหน้าทำอะไร

1. 🔴 **งานแรก = ต่อ `lua_api/reward.py` `pay()` เข้ากับ `store.add_typed_attribute` ของจริง** เมื่อ grep บน `origin/main` เจอแล้ว — ดักครบทั้งเจ็ดชนิดข้อยกเว้นที่ใบ DB ระบุ (`TypeError`/`ValueError`/`TypedAttrError`/`UnmeasuredTypedAttributeError`/`KeyError`/`WriteLockTimeout`) · ห้าม retry จนกว่าจะมี idempotency key (DB บอกเงื่อนไขไว้แล้ว)
2. ยืนยันคอมมิตรอบนี้ถึง main ด้วย `git merge-base --is-ancestor` ก่อนอ้าง
3. ถ้า chief แก้แถว `AddLvCriteriaExp` แล้ว: ลบข้อความ "TSV ยัง stale" ออกจาก `docs/SCRIPT_LANE.md`
4. หนี้ที่ยังเปิด: `reward_store`/`player_context` ยังไม่ถูกเสียบเข้า `ScriptHost` · panic ของ Lua (D5 รอบ oghyca) · `store.py` quest-state door (`#954`) · inventory ติด `RE-280` · `CheckWishQuest` รอ LANE-GUILD

## สถานะใบเซิร์ฟเวอร์ตามจริง

`pirate-force-server#1044` — เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด (GET ยืนยัน marker) **รอเกต**
🔴 **ยังไม่อยู่บน main** · sha ของหัวใบ = `f2a99ec` · รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor f2a99ec origin/main` ก่อนอ้าง

SCOREBOARD: COMING | รางวัลเควสที่เซิร์ฟเวอร์จะจ่าย ตรงกับที่ไคลเอนต์คำนวณเองแล้ว (เควส 2170 = 22119 exp ไม่ใช่ 22120) — รอบก่อนเดาความกว้างของการคูณผิด ทำให้ 14 ค่าเกินไปหนึ่งหน่วย รอบนี้ RE-295 วัดออกมาแล้วแก้ทั้งชุด และปิดผล adversary ครบแปดข้อในคอมมิตเดียวกัน | pf_bridge#1727 · pirate-force-server#1044 · sha f2a99ec
