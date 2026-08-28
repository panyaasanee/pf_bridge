# R213 (swlc56) — ซ่อม full-gate RED 39 ใบที่สะพานเจอ: census สาม pin ล้าสมัย + negative สองข้อที่แดงเพราะ "ข้อความ" ไม่ใช่โค้ด

- เวลา: `2026-08-28T17:1x+07:00` (ป้ายเวลาจาก `TZ=Asia/Bangkok date`)
- สาย: E PLATFORM (chief, cloud) · ล็อกรอบ: `pf_bridge` PR #301 (draft)
- HEAD ที่ทำงานด้วย: `pirate-force-server` main `336857c` · `pf_bridge` main `4537081`

## รอบนี้ทำอะไร

ที่มา: จดหมาย `20260828_1352_CHIEF-LOCAL-SMOKE-result.md` (chief โหมด local บนสะพาน) รายงานว่า
`py -3 -m pytest -q` **ชุดเต็ม** ที่ main `336857c` ออก `39 failed, 4050 passed` — และไม่มีใครแก้เพราะรอบนั้นถูกสั่งห้ามแก้โค้ด

รอบนี้แก้ 38 ใบจาก 39 ใบนั้น (อีกใบต้องทำบนสะพาน ดู GT-125) แยกเป็นสองเรื่องในใบเดียว:

### 1. `tests/test_runtimeres_actor_entry_static.py` (19 ใบ) — census ของ section [5] ล้าสมัย

วัดบนคลาวด์ที่ HEAD เดียวกัน ได้เลขตรงกับที่สะพานรายงานทุกตัว (สองแหล่ง G1):
entry sites **15** · carrier sites **23** · โมดูลที่สร้าง entry **14** · vital carrier **25**

- pin เดิม 13 / 16 / 12 / 21
- 🔴 **สองใน pin เหล่านั้นผิดตั้งแต่วันที่เขียน**: ที่ commit `d9f9aac` (2026-08-27 11:50 UTC) ซึ่งเป็นคอมมิตที่ใส่ `== 16` และ `== 21`
  ต้นไม้เดียวกันนั้นวัดได้ **21** และ **23** อยู่แล้ว [วัดแล้ว: `git ls-tree d9f9aac` + regex เดิม]
  ⇒ tool ใบนี้ exit 1 บนเครื่องที่รันมันได้ **ตั้งแต่วันนั้น** และไม่มีใครเห็น เพราะ gate ของ Actions รัน pytest แบบ subset ที่ **ตัดโมดูลนี้ทิ้ง** (มันอ่านอิมเมจ client)
- ต้นเหตุเชิงระบบ: tool อ่านอิมเมจตอน import ⇒ รันบนคลาวด์ไม่ได้ ⇒ รอบที่ re-pin ทำได้แค่ "อ่านแล้วนับด้วยตา" แล้วนับพลาด (คอมเมนต์ในไฟล์ของรอบนั้นเขียนไว้เองว่า "the only thing that catches it here is reading it")
- แก้: re-pin ทั้งสี่ค่าพร้อมชื่อเลนที่ขยับ (entry +2 = `mob_diag_multi_object.py` ของสาย B, `world_population_bg0002.py` ของสาย A · vital +2 = `columbus_quest_dispatch.py` 1→2 (CORE-REQUEST-019), `trace_path.py` 0→1 (CORE-REQUEST-025))
- และแก้ pin ที่ค้างในตัวไฟล์เทสเองซึ่งเก่ากว่านั้นอีก (stream 11, entry 9, modules 8, doing_both 3, zero-hp-const 1 ชื่อ) ให้ตรงกับที่วัดได้

### 2. `tests/test_hp_death_respawn_static.py` (19 ใบ) — negative สองข้อแดงเพราะ substring ไม่ใช่เพราะมีเลนคืนชีพ

ตรวจทีละ hit บนคลาวด์แล้วพบว่า **ไม่มี hit ไหนเป็นโค้ดจริงเลยสักอัน** [วัดแล้ว]:

- id hit เดียว = `6868` (เลขฐานสิบของ `0x1AD4`) โผล่กลาง **สตริง SHA-256** ใน `skill_attr_hypothesis.py` (`...060605C96868C882...`)
- verb hits 9 อัน = **ข้อความภาษาอังกฤษล้วน** ในคอมเมนต์/ข้อความ guard: `mob_loot.py` x3 ("a respawned monster killed again..."), `columbus_quest_dispatch.py` x3 ("player-chosen respawn scene"), `mob_aggro.py` x2, `mob_death.py` x1 (อ้าง path `hp_death_and_respawn` ของ FUNCTIONAL_COVERAGE)

แก้แบบเดียวกับที่รอบ 96 เคยแก้ในไฟล์พี่น้อง ("mentions 0x0080 ไม่เท่ากับ sets 0x0080"): เปลี่ยนตัวแยกแยะให้ถามสิ่งที่ประโยคอ้างจริง ๆ คือ **encoder/dispatch** โดยนับจาก **code token**

- NUMBER token เทียบด้วย **ค่า** (0x1AD4 / 0x3DD6 / 0x8B12) ⇒ เขียนเป็น `6_868` หรือฐานแปดก็จับได้ (เข้มกว่าเดิม) และสตริงเลขฐานสิบหกชนไม่ได้อีก
- NAME token ที่มี stem ของ verb = hit (เช่น `def respawn_actor`)
- STRING literal ที่ **ไม่มีช่องว่าง** และมี stem = hit (เช่น `"ReliveVital"` ที่เป็น dispatch key) — ประโยคภาษาคนมีช่องว่าง จึงตกไปโดยโครงสร้าง
- ไฟล์ที่ tokenize ไม่ได้ **ถอยไปนับ substring แบบเดิม** (fail-closed) และรายงานชื่อไฟล์ในข้อความ guard · เลข prose เดิมยังพิมพ์ไว้ข้าง ๆ ทุกครั้ง ไม่มีอะไรถูกซ่อน

ทดสอบตัวแยกแยะด้วยการปลูกของปลอม 8 แบบ: `def respawn_*`, `RELIVE_VITAL_ID = 0x1AD4`, `wire = 6868`, dict key `"ReliveVital"`, `verb == "Relive"` ⇒ **จับได้ทุกอัน**; คอมเมนต์/ประโยค/สตริง SHA ⇒ ไม่จับ [วัดแล้ว]

### 3. ปิดรูที่ทำให้เรื่องนี้เงียบมาหลายสิบรอบ

เพิ่ม `tests/test_static_verifier_pins_cloud.py` — คำนวณ census ทุกตัวที่มาจาก `src/` (11 ค่า) ใหม่ **โดยไม่ต้องมีอิมเมจ**
แล้วเทียบกับ (ก) เลขที่ pin ในตัว tool และ (ข) บล็อก `RUNTIMERES_COUNTS` ในรายงาน
⇒ ต่อไป pin ที่ผิดจะแดงใน PR ทุกใบ ไม่ใช่แดงเฉพาะตอนมีคนรันชุดเต็มบนสะพาน
มี trap test ในตัว (ปลูก call site ปลอม แล้วต้องขยับ) และพิสูจน์ว่ามัน**แดงจริง**ด้วยการแก้ pin เป็น 22 ชั่วคราวแล้วดูข้อความ fail [วัดแล้ว]

## ที่พิสูจน์แล้ว / ที่ยังไม่ได้พิสูจน์

- [วัดแล้ว] ชุด client-free subset แบบเดียวกับที่ gate ใช้ (tests ทั้งโฟลเดอร์ ลบ 48 โมดูลที่อ่านอิมเมจ/corpus): `2921 passed, 4 skipped, 3239 subtests passed` เขียว(cloud sanity)
- [วัดแล้ว] `tools/verify_hypothesis_ledger.py` = PASS 47 entries (ไม่มี ledger drift รอบนี้)
- [วัดแล้ว] `compileall src tests tools` ผ่าน · ไฟล์ที่แตะทุกใบ ASCII สะอาดในส่วนที่เพิ่ม
- [ยังไม่พิสูจน์] tool สองใบนี้รันจริง exit 0 — คลาวด์รันไม่ได้ ต้องรอสะพาน (GT-125)
- [ยังไม่พิสูจน์] `tests/test_pf_scan_field_scene_candidates.py` (แดงใบที่ 39) — generator ต้องใช้ game data ของสะพาน คลาวด์ regenerate ไม่ได้ ⇒ อยู่ใน GT-125 ข้อ 3
- ไม่มีชั้น client-observable ในรอบนี้ จึงไม่มี `OBSERVER_CONFIRMED`

## pf-adversary (บังคับ) — ยก 7 ข้อ แก้ 7 ข้อ

รันก่อน commit ตามกติกา ผลคือ "ห้ามอนุมัติ" ตามหน้าที่ของมัน และจับของจริงได้หลายข้อ:

1. 🔴 **negative กลายเป็นรายงาน ไม่ใช่ guard** — ตัวเลข prose ที่ guard เลิกใช้ตัดสิน ไม่ถูก pin ไว้ที่ไหนเลย
   ⇒ แก้: guard สองข้อ**ยืนยันสองครึ่งพร้อมกัน** (code hits = 0 **และ** prose = 1/9 พร้อมชื่อโมดูลที่ถือ prose)
   ประโยค respawn ใบที่สิบ หรือ docstring แผนที่ไวร์ของเลนคืนชีพ ยังทำให้แดงเหมือนเดิม
2. 🔴 **เทสใหม่ไม่ pin สำเนาที่เน่าจริง** — มันอ่าน tool + รายงาน แต่ไม่อ่าน `tests/test_runtimeres_actor_entry_static.py`
   ซึ่งคือไฟล์ที่พินค้าง 11 รอบ · และไม่ได้ตรวจเลขจำนวนโมดูล (พิสูจน์ด้วย mutation ว่าผ่านทั้งที่ guard ผิด)
   ⇒ แก้ทั้งสอง แล้ว mutation ซ้ำสามจุด (tool guard / บล็อกในรายงาน / assertion ในไฟล์เทส) แดงครบทั้งสาม
3. 🔴 **คำว่า "เข้มกว่าเดิมทุกทาง" ไม่จริง** — dict key ที่เขียน id เป็นสตริง (`{"0x1AD4": h}` สไตล์ที่ repo นี้ใช้จริงใน `scene_load.py`) หลุด
   ⇒ แก้: สตริงที่ไม่มีช่องว่างถูกตรวจกับ**ค่า id** ด้วย ไม่ใช่แค่ verb · และแก้คอมเมนต์ให้บอกตรง ๆ ว่ากว้างขึ้นตรงไหน แคบลงตรงไหน
4. 🔴 **โค้ดใหม่ ~50 บรรทัดไม่มีเทสแตะเลย** เพราะอยู่ในโมดูลที่ gate ตัดทิ้ง
   ⇒ แก้: ย้ายตัวสแกนออกมาเป็น `tools/pf_code_token_scan.py` แล้วเขียน unit test 6 ใบในเทสคลาวด์ (รวมสาขา fallback)
5. 🔴 **ผลขึ้นกับเวอร์ชัน Python** — 3.12+ แตก f-string เป็น FSTRING_* token ⇒ `f"Relive{n}"` หลุด **และสะพานรัน 3.14**
   ⇒ แก้: อ่าน FSTRING_MIDDLE ด้วย + เทสกำกับ
6. 🔴 **แก้ 4 พินจาก 11 พินที่มาจาก src/** อีก 7 ตัวยังอยู่ในกับดักเดิม ⇒ แก้: เทสคลาวด์ครอบทั้ง 11 ตัว
7. `_pinned_int` อ่าน source รวมคอมเมนต์ ⇒ แก้: anchor ที่ต้นบรรทัด + เทสที่แดงถ้ามีใครยกคำ guard เก่ามาไว้ในคอมเมนต์

ข้อที่มันยิงแล้วไม่เข้า: เทสคลาวด์ผ่านแบบ vacuous ไม่ได้ (มีพื้น 30 โมดูล) · ไม่ขยับพิน 48 โมดูลที่ gate ตัด ·
ไม่มี non-ASCII เพิ่ม · NGUARD ไม่ขยับ (ไม่ต้องแก้เลข guards ในรายงาน)

## PR ของรอบนี้

- `pirate-force-server` **#197** — 7 ไฟล์ (เกินเพดาน ~6 หนึ่งไฟล์เพราะบรรทัด allowlist ใน `.gitignore` ซึ่งเป็น mechanical
  และการแยกสองเครื่องมือเป็นสองใบจะทิ้งให้สะพานแดงคาระหว่างสองใบ) · seam test รันแล้วตามกติกาไฟล์ `.gitignore`
- `pf_bridge` **#301** — จดหมาย/คิว/บันทึกรอบ/stub 13 ใบ

## สถานะท้ายรอบ

push แล้ว รอ merge — `pirate-force-server` PR #197 และ `pf_bridge` PR #301 (ยังไม่อยู่บน main จนกว่ารอบถัดไปจะเห็นว่า merge จริง)
