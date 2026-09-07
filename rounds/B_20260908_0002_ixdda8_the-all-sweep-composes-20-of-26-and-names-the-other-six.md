# LANE-B รอบ `ixdda8` — 2026-09-08T00:02+07:00 → 00:30+07:00 · ล็อก `pf_bridge#1817`

## รอบนี้ขยับ NOW/M ข้อไหน
**M3 / P-2 (สีชื่อ)** — งานแรกที่ `NOW.md` บรรทัด LANE-B และ `COO-ORDER 2342` สั่ง: ขยาย `#1077` เป็นสวีป **ALL / ALL-NOID**
ผลจริง: **ประกอบได้ 20 แถว (ALL) / 16 แถว (ALL-NOID)** จาก 26 ที่เจ้าของสั่ง · อีก 6 แถวมีเหตุผลเขียนไว้ทุกแถว ไม่มีแถวไหนหายเงียบ
`pirate-force-server#1089` (draft ตาม §7 · `ADVERSARY_PENDING`) **ครอบ `#1077` ทั้งใบ**

## สิ่งที่รอบนี้ส่ง
- `name_colour_sweep.py`: `SET_ALL` / `SET_ALL_NOID` · เลย์เอาต์ลาน Iron Man (X `11800` +150 · Y `9340` · แถวสอง +300 · Z **อ่านจากแถวหุ่นที่ shipped** ไม่ได้พิมพ์)
  · splice `n_ENEMY` (BasicAttr บิต `0x0800` · แท็ก `0x14` · u32 · PROVEN_EXACT W ในโคเด็กซ์) ใช้ตัวช่วยแช่แข็งเดิมสองตัว ไม่ derive ตำแหน่งใหม่
  · แถว identity ≤0 · คีย์เวิร์ด `viewer_identity=` (ค่าเริ่มต้น `None` = ไบต์เดิมทุกไบต์)
- `tests/test_name_colour_sweep_all.py` (ใหม่ 14 เทส) + สองเทสเก่าย้ายจาก `KNOWN_SETS` → `_ANCHOR_SETS` (derived ไม่ใช่ลิสต์มือ)
- หมุด census `src_modules_passing_zero_hp_by_named_constant` 7→8 ปักใหม่ครบสามสำเนาในคอมมิตเดียวกันตามที่เทสสั่ง

## หกแถวที่ประกอบไม่ได้ และเหตุผล (คำสั่ง `2342` ข้อ 2 ห้ามเงียบ)
| แถว | ใครปฏิเสธ |
|---|---|
| `N-LNKS` | `mob_viewer_link.REFUSE_VIEWER_IS_THE_MONSTER` — ลิงก์ตัวเองคือรูปที่ `RE-195` แถว 61(a) บอกว่าผิดแน่ |
| `M-DEAD` · `M-IDNEG-DEAD` | `field_mobs.hostile_npc_attr` ปฏิเสธมอนเกิดที่ HP ศูนย์ · `N-HP0` ถามข้อเดียวกันบนต้นแบบ NPC |
| `N-LNKP` · `N-IDNEG-LNKP` · `N-ID0-LNKP` | ต้องใช้ identity ของเซสชันที่กำลังดู ซึ่ง call site ไม่ส่งมา (CORE-REQUEST ส่งแล้ว) |
ไม่ปลดยามสองตัวแรกเพื่อให้ครบจำนวน — ยามถาวรแลกกับป้ายเดียวบนรถบัสเที่ยวเดียวไม่คุ้ม

## ผลลบที่มีค่า (วัดเอง ไม่ได้เดา)
**พิกัดที่เจ้าของกำหนดอยู่ในเมืองจริง**: แถวแรก `N-BASE` ห่าง NPC จริง `Mutant Green Eagle` **23.6 หน่วย** เทียบกับเพดานอ่านป้าย 200 ของโมดูลเอง
⇒ ครึ่ง "โลกว่าง" (`census_actors=0`) ของคำสั่ง `2350` ข้อ 2 **ไม่ใช่ของประดับ** ถ้าไม่มีมัน ka1-A จะอ่านป้ายผิดตัวและผลแยกไม่ออกจากผลที่ผิด
เทส `test_the_owner_row_overlaps_the_live_town_so_all_needs_an_empty_world` พินตัวเลขนี้ไว้ · แต่ `generation` และ viewer identity อยู่ใน `runtime.py` = ของ chief ⇒ ส่ง CORE-REQUEST แทนการแตะ

## หลักฐาน
- ชุดเต็มบนต้นไม้ที่ merge `origin/main` แล้ว: `13959 passed, 432 skipped` (สองแดงที่เหลือคือหมุด census ที่คอมมิตถัดไปปักใหม่ → เขียวบนหัวที่ push)
- `python3 tools_bridge/pf_gate_preflight.py --repo <server>` → **PREFLIGHT PASS**
- บูตปกติ (ไม่ตั้ง env) ไม่ขยับแม้แต่ไบต์: `sweep_actors` คืน `()` · `PF_NAME_COLOUR_SWEEP=ALL ` (มีเว้นวรรค) ถูกรายงานกลับเป็นค่าไม่รู้จัก ไม่ใช่เงียบ
- **ยังไม่มีโทเคน `HEADLESS_PROOF` ของ ALL ในรอบนี้** — กลไก ALL คือโค้ดของ PR ใบนี้เอง กฎ `0159` ต้องการโทเคนที่วัดบน main และครึ่งโลกว่างยังไม่ลง ⇒ ใบ gt-body ไป K **รอบหน้า** (คำสั่งให้เวลา 2 รอบ นี่คือรอบที่ 1)

## กติกาที่รอบนี้ทำ/ไม่ได้ทำ
- `ADVERSARY_PENDING pirate-force-server#1089` — สั่ง `pf-adversary` แล้วบนกิ่งนี้ ผลยังไม่คืนตอน push · **ห้ามอ่านว่า "ผ่าน adversary"** · รอบหน้าของสายนี้หยิบผลเป็นงานแรก
- บริโภคจดหมายสองใบ (`2342` COO-ORDER + COO-DECISION) แล้ว: stub + สำเนาไป `consumed/`
- `TWO_SESSIONS_SAME_SCENE:` ไม่มีผล — รอบนี้ไม่เขียน combat state ลง registry ของ LANE-A และแถวสวีปทุกแถวเป็น dummy ที่ติดอาวุธด้วย env เท่านั้น
- ไม่แตะ `runtime.py` / `app.py` / v141 / เขตสาย A / `bg0002`

## รอบหน้าทำอะไร (งานแรกก่อน)
1. บริโภคผล `pf-adversary` ของ `#1089` แล้วเติม `PF-AUTOMERGE: v4` ให้ใบนั้น (ปลด draft)
2. ถ้า CORE-REQUEST ลง: วัดโทเคน `NAME_COLOUR_SWEEP_ARMED actors=… census_actors=0 wire=…` แล้วส่งใบ `LANE-B-TO-K-gt-body-*` ของ ALL/ALL-NOID
3. แล้วตามคิว `NOW.md`: `name_tokens` → `GT-300` (GT-178 register+tick ทุกฉากที่มี roster) → parser → respawn 120 s · ห้ามพลิก `bg0002`

SCOREBOARD: COMING | บูตเดียวถามคำถามสีชื่อ 20 ข้อพร้อมกันบนลานหุ่น Iron Man แทนที่จะถามทีละข้อต่อการเปิดเกมหนึ่งครั้ง (ชุด ALL/ALL-NOID) และหกข้อที่ถามไม่ได้มีชื่อคนปฏิเสธกำกับทุกข้อ | pirate-force-server#1089 (draft, ครอบ #1077) + pf_bridge#1817 + CORE-REQUEST 20260908_0024
