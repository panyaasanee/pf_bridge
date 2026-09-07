# LANE-B รอบ `nxcwdn` — กฎ outfit ถอดแล้วและปักคุมแล้ว · แต่ **การพลิก `bg0002` ติดที่ tick เดียวของเจ้าของ** ไม่ใช่ติดโค้ด

ADDRESSEE: COO
cc: Panya · chief · LANE-K
เวลา: 2026-09-07T15:20+07:00 · ตอบใบ `20260907_1346_COO-DECISION-panya1313-outfit-half-out-bg0002-cline-LANE-B.md`

## สรุปหนึ่งบรรทัด
ครึ่ง `s_OUTFIT` ถอดออกจากกฎเลือก hostile แล้วจริง พร้อมคุม bg0001 ที่ **ปักใหม่ ไม่ได้ปิด** — แต่ผมยัง **ไม่พลิก `bg0002` เป็น 52 แถวในรอบนี้** เพราะวัดได้ว่ามอน 40 ตัวที่กลับมา **ตายไม่ได้** และเส้นทางปฏิเสธของมันคือ `raise` ไม่ใช่การปฏิเสธเงียบ ๆ

## ที่ทำเสร็จและอยู่ใน PR รอบนี้ (เขียวทั้งหมด)
1. `tools/pf_mine_scene_mob_roster.py`: `s_OUTFIT` ไม่มีผลต่อการตัดสินว่าเป็นศัตรูอีกต่อไป — ทำเป็น **กฎที่มีชื่อ** `--outfit-rule {unambiguous,any}` ค่า default ยังเป็นของเดิม เพราะโมดูลฉากที่ commit ไว้แล้วสิบไฟล์ถูกขุดด้วยกฎเดิมและมีเทสเทียบไบต์ต่อไบต์ทีละไฟล์ · แถวที่ `s_OUTFIT` ว่าง **ยังถูกปฏิเสธ** — ว่างไม่ใช่ "กำกวม" แต่คือ "ไม่มีตัวละครให้วาด"
2. **คุม bg0001 ปักใหม่ ไม่ได้ปิด/skip/xfail** ตามที่ใบ `1346` สั่ง · `verify_frozen` เดิมยังเทียบ v141 ได้ 115 แถว 0 mismatch · เพิ่ม `verify_frozen_any`: กฎใหม่ได้ **146 แถว** ซึ่ง **ครอบ 115 แถวของ v141 ครบ และไม่มีแถวไหนขยับสักคอลัมน์** (index/template/x/y/z/outfit) — ข้ออ้าง superset แข็งกว่าการเทียบจำนวนเดิม เพราะมันปักทั้งของที่เพิ่มและของที่ห้ามขยับ · มีเทสที่ **ทำให้คุมตัวนี้ล้มจริง** (ขยับ x หนึ่งเมตรแล้วต้องจับได้) ไม่ใช่คุมที่ไม่มีใครเคยเห็นมันแดง
3. เทสใหม่ `tests/test_pf_mine_scene_mob_roster_outfit_rule.py` — 7 ใบ เขียวทั้งหมด · รวมใบที่พิสูจน์ **ข้ออ้างของใบ `1346` เอง**: 40 แถวที่ได้คืนมาใน bg0002 ตกด้วยเหตุ outfit ล้วนจริง (ถามทีละแถวด้วยกฎเก่า คำตอบต้องเป็น `_avatar_is_a_variant_list` ทุกแถว)

## ที่ **ไม่ได้ทำ** และเหตุผลที่วัดได้ (นี่คือส่วนที่ต้องเคาะ)
พลิก `field_mob_tables_bg0002.py` เป็น `--identity-rule cline --outfit-rule any` **ทำได้ด้วยคำสั่งเดียวและผมรันมาแล้ว** ผลคือ:

- roster **12 → 52** แถว · template `{31,34,35}` → `{27,28,29,30,31,32,33,34,35}` (6 ชนิดใหม่ = 40 ตัว ตรงกับที่ NOW เขียนเป๊ะ)
- โทเคน headless ที่วัดได้บนต้นไม้ที่พลิกแล้ว (ไม่ใช่บน main — main ยังเป็น 12):
  `MOB_CENSUS_HOSTILITY scene_id=2 scene=Bg0002 roster=52 backed=52 unbacked=none refused=8 override=not_reported ledger=not_reported withheld=0`
  **`refused=8` ไม่มีเหตุ outfit เหลือเลย** — ทั้ง 8 คือ placement 89,90,92,93,94,95,96,97 ซึ่งเป็นชุดคำสั่งห้ามวางของเจ้าของ + สองแถวที่ `s_OUTFIT` ว่างจริง ⇒ ตรงเงื่อนไข "refused เหลือเฉพาะเหตุที่ไม่ใช่ outfit" ของใบ `1346`
- ต้อง regenerate ตารางลูกอีก **สองใบในคอมมิตเดียวกัน** ไม่งั้นฉากพัง (ผมรันครบแล้ว ทั้งสองอันทำงาน):
  - `field_mob_ai_tables.py` — ไม่ regenerate แล้ว `mob_ai_control.open_register` โยน `MobAiControlError` และ **census ทั้งฉากหายเงียบ** (`world_census_bg0002_compose_refused_MobAiControlError`) ผู้เล่นจะเห็น **ศูนย์ตัว** ไม่ใช่ 52 ตัว
  - `field_drop_tables.py` — ไม่ regenerate แล้วการฆ่าโยน `MobLootContractError: unknown_drop_set` (2802202 / 2802222 / 2802228)
  - หลัง regenerate ทั้งสอง: `tests/test_bg0002_census_wiring.py` **15 ใบเขียวหมด** และ `test_mob_combat_dispatch_bg0002_kill.py` เหลือแดงเฉพาะพินอัตราดรอป

## 🔴 ตัวบล็อกจริง มีข้อเดียว: **death scope**
`mob_death` ถือคำสั่ง `"widen-death-scope-bg0002": frozenset({31, 34, 35, 103})` · roster ใหม่มี template `27..35` ⇒ **6 ใน 9 ชนิด (40 ตัวจาก 52) ไม่ได้รับอนุญาตให้ตาย** วัดได้ตรง ๆ:

```
MobDeathContractError: target_outside_the_sanctioned_scope: widened=
'PANYA-DECISION 2026-08-27T20:10+07:00 (ADDENDUM 20:18) widen-death-scope-bg0002'
... names MOBS template id(s) [31, 34, 35, 103]; mob 0x2020 carries template_id 28,
which is not one of them
```

และเหตุนี้ **ไม่ใช่การปฏิเสธเงียบ**: ที่ `runtime.py:5558` ตัวจับ `MobDeathContractError` ปล่อยผ่านเฉพาะเหตุ `REFUSE_REGISTER_STALE` เหตุอื่น `raise` ต่อ ⇒ **มีทางที่การฆ่ามอนตัวใหม่ตัวแรกจะคลายสแต็กออกจากเธรดฟัง = โลกของผู้เล่นว่าง** (ผมยังไม่ได้วัด dispatch จริงจนถึงจุดนั้น — ผมวัดได้แค่ว่าคำสั่งปฏิเสธ และเส้นทางของเหตุนี้คือ `raise` · นี่คือ **ยังไม่ได้วัด** ไม่ใช่ "ผ่าน")

NOW.md เขียนไว้เองว่าการขยาย `{31,34,35}` อยู่ใน **"รอ Panya ติ๊ก"** ⇒ ผมขยายเองไม่ได้ · และการแก้เทสคุม `test_the_bg0002_ruling_covers_exactly_the_real_bg0002_rosters_templates` ให้ยอมรับ "roster กว้างกว่าคำสั่ง" คือ **การลดกำลังคุมเพื่อให้ของที่ยังไม่ถูกติ๊กผ่าน** ซึ่งกฎ `0945` ห้ามไว้ตรง ๆ ⇒ ผมจึงถอยและถามแทนที่จะดัน (ตรงกับเงื่อนไขหยุดในใบ `1346` เอง)

## `[สมมติของสาย LANE-B - รอ COO ยืนยัน]`
ใบ `1346` เขียนว่า "ถ้า census ออกมาไม่ใช่ 12 = หยุด" · ผมอ่านว่าเลข 12 ในใบนั้นคือ **จำนวนวันนี้** ไม่ใช่จำนวนเป้าหมาย เพราะ NOW.md ของรอบเดียวกันเขียนเองว่า "6 ชนิด (40 ตัว) กลับเป็นศัตรู" และ 12+40 = 52 พอดี ⇒ ผมถือว่า **52 คือผลที่ถูก** ไม่ใช่สัญญาณให้หยุด · ถ้าผิด ต้องย้อน: ไม่มีอะไรต้องย้อนในโค้ด (ผมไม่ได้พลิกตาราง) แค่ทิ้งใบนี้

## ขอเคาะสองข้อ
1. **ติ๊ก death scope `bg0002`**: ขยาย `{31,34,35,103}` → `{27,28,29,30,31,32,33,34,35}` ตามไหม · ติ๊กแล้วการพลิกเป็นงานรอบเดียวจบ (สามคำสั่ง regenerate + ปรับพินในเทสของสาย B เอง ~22 ใบ ล้วนเป็นพินจำนวน)
2. ถ้า **ยังไม่ติ๊ก** — ต้องการให้ผมส่ง 52 ตัวขึ้นจอทั้งที่ 40 ตัวตายไม่ได้ไหม · ความเห็นผม: **ไม่ควร** จนกว่าจะมีเทส dispatch ที่พิสูจน์ว่าการตีมอนนอกคำสั่งปฏิเสธแบบไม่คลายเธรด — M4 คือ "ตีได้ตายได้" มอนตีไม่ตาย 40 ตัวแย่กว่ามอนตายได้ 12 ตัว

## คำสั่งรันซ้ำได้ (ทุกตัวเลขข้างบนมาจากสามบรรทัดนี้)
```
python3 tools/pf_mine_scene_mob_roster.py --gamedata <bridge>/gamedata --scene bg0001 --verify-frozen
python3 tools/pf_mine_scene_mob_roster.py --gamedata <bridge>/gamedata --scene Bg0002 \
        --identity-rule cline --outfit-rule any --predicate-census --out <table>
python3 tools/pf_mine_mob_ai_rows.py    --gamedata <bridge>/gamedata --out src/pirateforce_foundation/field_mob_ai_tables.py
python3 tools/pf_mine_scene_drop_tables.py --gamedata <bridge>/gamedata --out src/pirateforce_foundation/field_drop_tables.py
```

-- LANE-B รอบ `nxcwdn`
