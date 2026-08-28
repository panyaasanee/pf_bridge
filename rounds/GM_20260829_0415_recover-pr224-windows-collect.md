# รอบ GM `ank2vl` — 2026-08-29T04:15+07:00

**หนึ่งประโยค:** งานทั้งรอบก่อนไม่เคยขึ้น main เพราะ `os.geteuid()` หนึ่งบรรทัดในอาร์กิวเมนต์ของ `skipIf`
รอบนี้กู้ครบ แก้เหตุ ปิดช่องไม่ให้กลับมา และแก้คิวเทสที่กำลังจะหลอกผู้เทส

ค้นแล้ว (`external/00_SEARCH_HERE_FIRST.md`, `gamedata/00_SEARCH_HERE_FIRST.md`): **ไม่เจอ** — รอบนี้ไม่พึ่งข้อมูล client

## ลำดับที่ทำ

1. ยืนยัน `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11388 ไบต์) ✔
2. ตรวจ PR ค้างหัวข้อ `[LANE-GM]` ทั้งสองรีโป = **ไม่มี** ⇒ ยึดล็อก: commit เปล่า `round claim: ank2vl`
   push ทั้งสองสาย เปิด draft `#230` (เซิร์ฟเวอร์) และ `#363` (สะพาน)
3. ADDENDUM ข้อ A — ชะตา PR รอบก่อน: `#224` `merged=false` · `#357` `merged=true`
4. อ่านเหตุจาก log ของเกตจริง ไม่ใช่เดา แล้วกู้ด้วย `git merge origin/claude/sleepy-sagan-gejldf` (ไม่มี conflict, 1552 บรรทัด)
5. แก้เหตุ · เพิ่มด่าน · รันชุดเดียวกับเกต · pf-adversary
6. ADDENDUM ข้อ B — กล่องจดหมาย: ไม่มีใบที่สาย GM ต้องบริโภครอบนี้

## เหตุ (จาก Actions run `33210364835` job `gate`)

```
tests\test_gm_login_scene_stage.py:295: in RefusalLeavesTheFileAloneTests
    @unittest.skipIf(os.geteuid() == 0, "root ignores directory write bits")
E   AttributeError: module 'os' has no attribute 'geteuid'
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

`skipIf` ไม่ป้องกันอาร์กิวเมนต์ของตัวเอง — เงื่อนไขประเมินตอน class body รัน คือตอน import
⇒ ไม่มีลำดับ decorator แบบไหนช่วยได้ · และ collect error หนึ่งจุดทำให้ `pytest_subset` **และ** `skip_census`
แดงพร้อมกัน (census เห็น 0 skip ที่ที่เก้าโมดูลพินรวมกัน 48 แล้วรายงาน PIN DRIFT เก้าบรรทัดที่ไม่เกี่ยวกับต้นเหตุ)

## สิ่งที่แก้ (เขต `tests/test_gm_*.py` ทั้งหมด)

| # | สิ่งที่ทำ | ทำไมไม่ทำอย่างอื่น |
|---|---|---|
| 1 | `PERMISSION_BITS_BITE` ผ่าน `getattr(os, "geteuid", None)` | เรียกตรงคือตัวบั๊ก |
| 2 | เอา skip ทั้งสี่จุดออก ใช้ `if` ในตัวเทสแทน | `docs/PYTEST_SKIP_PINS.json` อยู่นอกเขตผม และ skip ที่ไม่ได้พิน = เกตแดงเอง ⇒ แก้ข้อ 1 อย่างเดียวยังเสียรอบซ้ำ |
| 3 | `tests/test_gm_tests_collect_without_posix.py` | grep จับได้แค่ชื่อที่นึกออก ตัวนี้ import จริงในโปรเซสที่ไม่มี POSIX |

จุดที่ permission bit ไม่กัด (Windows หรือ root) ใช้ `mock.patch("os.replace")` / `mock.patch("os.access")`
แทน `chmod` — **อ่อนกว่าของจริงและเขียนกำกับไว้แล้ว**: พิสูจน์ว่าโมดูลปฏิเสธเมื่อ OS ว่าไม่ได้
ไม่ได้พิสูจน์ว่า OS นี้ว่าไม่ได้ · ฉบับแข็งยังรันทุกเครื่อง POSIX ที่ไม่ใช่ root รวมทั้งสะพาน

## หลักฐาน

- **วัดสองทางกับตัวด่าน**: ไฟล์ฉบับที่ `#224` push จริง ตกด่านด้วย `AttributeError: module 'os' has no attribute 'geteuid'`
  (ข้อความเดียวกับที่เกตพ่น) · ฉบับแก้แล้วผ่าน · เทสตัวที่สามป้อน bait ให้ด่านเอง กันด่านที่เลิกทำงานเงียบ ๆ
- ชุด client-free ด้วย exclusion 48 โมดูลของเกตเอง: **3355 passed / 8 skipped / 0 failed**
- `tools/pf_pytest_precondition_census.py` บน transcript นั้น: **RESULT: PASS** ("every skip is declared, named and pinned")
  — skip ทั้ง 8 เป็น precondition ของ clone ตื้น ไม่มีสักตัวมาจากสาย GM
- `tests/test_tree_is_cp874_safe.py` + `tests/test_gm_source_is_cp874_safe.py`: 8 passed / 395 subtests
- รันไฟล์ซ้ำเป็นผู้ใช้ `nobody`: 30 passed (สาขา `PERMISSION_BITS_BITE = True`) · เป็น root: 30 passed (สาขาแทน)

## คิวเทส

- `GT-141` (ใบของสาย GM เอง) `READY เมื่อ #224 merge` ⇒ **BLOCKED** พร้อมเหตุ วัดด้วย API และเงื่อนไขปลดใหม่ (`#230` `merged=true`)
- `GT-127` (ใบของสาย GM เอง) อัปเดตสองข้อที่วัดได้: `#223` merged แล้ว · `08d2c6d` (สวิตช์ของ chief) อยู่บน main แล้ว

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

เมื่อวานคิวบอกว่า `GT-141` พร้อมบูต ทั้งที่โค้ดที่ใบนั้นเทสไม่มีอยู่บน main — หยิบไปเสียจ็อบเปล่า
วันนี้ใบบอกความจริงพร้อมเงื่อนไขปลดที่ตรวจได้ และเมื่อ `#230` merge `/warp <ฉากอื่น>` จะมีอยู่จริงบน main เป็นครั้งแรก

## nonclaim

1. **รอบนี้ไม่มีการใช้ GM ข้ามขั้นใดเลย** · ความสามารถ GM ไม่เพิ่มไม่ลด · ไม่ประกาศ milestone ใด
2. **เขียว(cloud sanity)** เท่านั้น ไม่ใช่เขียว(Actions) — Actions เป็นคนตัดสิน
3. ทั้ง root และ `nobody` ไม่ใช่ Windows · ที่พิสูจน์คือสองด่านที่แดงผ่านฉบับ local ของมัน
4. บันทึกสถานะว่า **"push แล้ว รอ merge PR #230 / #363"** ไม่ใช่ "เสร็จ"

## จบรอบ

push ครบ → เอา draft ออก (หลัง pf-adversary รายงาน ตาม `COO-DECISION 20260829_0345` เพราะ PR นี้แตะเส้นล็อกอิน)
→ แก้หัวข้อ/body (marker `PF-AUTOMERGE: v4` ต้องอยู่ ยืนยันด้วย GET หลัง PATCH) → wake gate (เซิร์ฟเวอร์เท่านั้น)
รันด่านโทเคน skip-ci กับ commit ล่าสุดก่อน push ทุกครั้ง ทั้งสองรีโป (`COO-DECISION 20260829_0247`)

---

## ภาคผนวก — หลัง pf-adversary (2026-08-29T04:5x+07:00)

รายงาน 10 ข้อ · แก้ครบก่อน push · รายละเอียดเต็มอยู่ในใบ
`notes_to_chief/20260829_0415_LANE-GM-STATUS-pr224-recovered-gt141-blocked.md` ภาคผนวก

ที่สำคัญที่สุดสามข้อ:
1. **false green ที่ผมสร้างเองระหว่างแก้** — รวม "ระบบไฟล์ *เก็บ* mode bit ไหม" กับ "mode bit *ปฏิเสธ* โปรเซสนี้ไหม"
   ไว้ในค่าคงที่เดียว · root **เก็บ** แต่ **ไม่ปฏิเสธ** ⇒ mutant `0o600` → `0o666` (config ของ GM กลายเป็น world-writable)
   เขียวทั้งบนเกตและในคอนเทนเนอร์ root ⇒ แยกเป็น `MODE_BITS_RECORDED` / `MODE_BITS_OBEYED` · วัดซ้ำ mutant ตายแล้ว
2. **ไฟล์ด่านใหม่ยังไม่ได้ `git add`** ⇒ ถ้า push ตอนนั้น หัวใจของรอบขึ้นไปเป็นศูนย์ไบต์
   ⇒ เพิ่มเทสที่แดงเมื่อมีไฟล์ `tests/test_gm_*.py` ที่ git ไม่รู้จัก
3. **รายชื่อ POSIX-only เขียนมือ ไม่ครบ** — เดินผ่านได้หกชื่อ ⇒ ใส่ครบ + พินด้วย bait เทส + ประกาศว่าเป็น [เสนอ]

ผลลบที่เก็บไว้: ตั้ง `os.name = "nt"` ในโปรเซสลูก = false red ทั้ง 28 ไฟล์ (`pathlib` เลือก `WindowsPath`) ⇒ ไม่ ship

บทเรียนของรอบที่ต้องจำ: **commit ก่อน merge และก่อนปล่อย subagent ที่รันคำสั่ง git ได้**
ร่าง `docs/GM_LANE.md` ของรอบนี้หายสองครั้ง (adversary `git checkout --` หนึ่งครั้ง · ผมเอง `git merge` ทับอีกครั้ง) เขียนใหม่ทั้งสองครั้ง

**หลักฐานหลังแก้:** 3357 passed / 8 skipped / 0 failed · census PASS · เขต GM 557 passed / **0 skipped** ทั้งในฐานะ root และ `nobody`
