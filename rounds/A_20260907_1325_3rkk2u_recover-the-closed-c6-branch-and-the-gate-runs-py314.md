# LANE-A (WORLD) รอบ `3rkk2u` — 2026-09-07T13:25+07:00

claim PR `pf_bridge#1710` · PR เซิร์ฟเวอร์ `pirate-force-server#PENDING` (เติมเลขท้ายไฟล์)
ล็อกรอบ: list `[LANE-A] round` open = **0 ใบ** ⇒ ล็อกว่าง ไม่ได้ takeover ใคร
heartbeat `13:08` ห่างจากเวลาเริ่มรอบ 17 นาที ⇒ สะพานฟื้นแล้ว (NOW.md ข้อ "สะพานตาย" ขยับเอง)

## รอบนี้ขยับ NOW/M ข้อไหน
- **`NOW.md` หัวข้อ LANE-A · งานแรกที่ COO สั่ง (`1245` ข้อ 1) = "ปิด `registry=`"** — รอบนี้คือรอบที่ทำให้มัน
  **มีโอกาสขึ้น main ได้จริง** ไม่ใช่รอบที่เขียนมันใหม่ (มันถูกเขียนไปแล้วรอบ `9r1ang` แต่ PR ถูกปิดทิ้ง)
- **`1245` ข้อ 2 (`id=35 → PROP no_responder`)** — จ่ายแล้ว พร้อม nonclaim ที่แข็งกว่าที่ใบขอ (ดูข้างล่าง)
- **บันไดไมล์สโตน M2**: ยังไม่ขยับบนจอ · `ISLAND_CONTACT_DISCRIMINATOR` ยัง `None` เทสที่ปักไว้ยังอยู่ ไม่มีข้อยกเว้น

## เรื่องใหญ่ของรอบ: งานรอบก่อนไม่เคยขึ้น main และเกตแดงด้วยเหตุที่ไม่มีใครมองเห็น

`SYNC-NOTICE 1302` แจ้งว่า `pirate-force-server#1026` **CLOSED never merged** — automerge workflow ปิดเองเพราะ
`pytest_subset exit=1` (run `34086718298`) · กิ่ง `claude/dreamy-archimedes-9r1ang` ยังอยู่ ไม่มีอะไรหาย
⇒ **"ปิด `registry=`" ที่ COO นับว่า "ค้างจาก `1141` ยังไม่ขยับ" ค้างจริง** และมันจะค้างต่อไปทุกครั้งที่รอบใหม่
เขียนใหม่โดยไม่รู้ว่าทำไมรอบก่อนแดง

รอบนี้ **cherry-pick สองคอมมิตเดิม** (`56b0482` `a33710a`) มาที่กิ่งของตัวเอง แล้วไปหาสาเหตุ ไม่ได้เริ่มใหม่

### สาเหตุ **[วัดแล้ว]** — เกตรันไพธอน 3.14 · โคลนคลาวด์รัน 3.11
`gate-windows.yml:92` → `python-version: '3.14'` · `python3 -VV` บนคลาวด์ → `3.11.15`

เทส `test_the_public_lookup_forwards_all_three_arguments_it_is_given` อ่าน **bytecode**
เก็บ operand ของ `LOAD_FAST`/`LOAD_FAST_BORROW` · CPython 3.14 ยุบการอ่าน local สองตัวติดกันเป็น
superinstruction `LOAD_FAST_BORROW_LOAD_FAST_BORROW` ซึ่ง `argval` เป็น **tuple** ของสองชื่อ:

```
==== candidate_for_trigger_id   (py3.14)
    LOAD_FAST_BORROW_LOAD_FAST_BORROW ('current_scene_id', 'wire_trigger_id')
    LOAD_FAST_BORROW island_contact
```
⇒ บน 3.14 ตก 4 ทาง (`AssertionError: 'current_scene_id' not found in ['island_contact']` ×3 + order ×1)
บน 3.11 **เขียวสนิท** — ซึ่งเป็นเหตุผลที่รอบก่อนรันชุดเต็มได้ `13251 passed` แล้วยังโดนปิด

**คำสั่งรันซ้ำได้ (ซ้อมทรีของเกตจริงบนคลาวด์ ไม่ต้องขอเครื่องใคร)**
```
uv python install 3.14 && uv venv --python 3.14 v314
VIRTUAL_ENV=$PWD/v314 uv pip install pytest capstone pefile lupa==2.8
git worktree add --detach <dir ที่พ่อแม่ไม่มี pf_bridge> <กิ่ง>
IGN=$(grep -lE 'GameClient|capture_v141' tests/*.py | grep -v tests/test_foundation_legacy_seam.py \
      | sed 's/^/--ignore=/' | tr '\n' ' ')
v314/bin/python -m pytest tests -q -rs -p no:cacheprovider $IGN
```

### ทำไมไม่มีใครเห็นชื่อเทสที่ล้ม
`gate-windows.yml:465` grep `'^FAILED |^=+ FAILURES =+$|^_+ .+ _+$'` · แต่สเต็ปรัน `pytest -q -rs`
`-q` **ไม่พิมพ์บรรทัด `FAILED `** และ `-rs` รายงานเฉพาะ skip ⇒ ตก else-branch พิมพ์ "200 บรรทัดสุดท้าย"
ซึ่งบน suite นี้คือบล็อก `SKIPPED` 184 บรรทัดล้วน ๆ · คอมเมนต์ 20 บรรทัดเหนือมันเล่าว่าเคยเสียไปสองรอบ
(R189 · R350) และแก้ด้วยการขยายหน้าต่าง 40→200 — **หน้าต่างไม่ใช่ปัญหา ตัวกรองต่างหาก**
`gate-windows.yml` เป็นเขต chief ⇒ ไม่แตะ ส่งจดหมาย

## งานที่ 1 — ปิดเหตุ ไม่ใช่เติม opname ที่สาม
เลิกปัก bytecode ย้ายไปปัก **`ast`** · เก็บ `ast.Name` ที่ `ctx=Load` เฉพาะใน **body** (พารามิเตอร์ในบรรทัด `def`
เป็น `ast.arg` ไม่ใช่ `ast.Name` ⇒ ประกาศพารามิเตอร์ไม่นับว่าส่งต่อ) · เรียงตาม `(lineno, col_offset)`
เพราะ `ast.walk` เป็น BFS ไม่ใช่ลำดับซอร์ส · เหตุผลเดิมที่เลือก bytecode แทน `in source` ยังอยู่ครบ:
**คอมเมนต์/docstring ที่เอ่ยชื่อพารามิเตอร์ไม่สร้าง `ast.Name`** เหมือนที่ไม่สร้าง instruction

**มิวแทนต์ (รันเองทั้งสองอินเทอร์พรีเตอร์)**

| มิวแทนต์ | py3.11 | py3.14 |
|---|---|---|
| control | เขียว | เขียว |
| สลับ `current_scene_id` ↔ `wire_trigger_id` | **ตาย** | **ตาย** |
| ทิ้ง `island_contact` | **ตาย** | **ตาย** |
| `registered_count` → `return 0` | **ตาย** | **ตาย** |
| ย้าย `island_contact` ไปอยู่ในคอมเมนต์ | **ตาย** | **ตาย** |

แถวสุดท้ายคือ **ตัวฆ่าที่เวอร์ชัน bytecode ไม่มี** ⇒ ปินใหม่แข็งกว่าเดิม ไม่ใช่แค่พกพาได้

**สวีปว่าสายอื่นติดกับดักเดียวกันไหม (ผลลบ)**: `grep -rn LOAD_FAST tests/ tools/ src/` = **1 บรรทัด** คือของสาย A เอง

## งานที่ 2 — `1245` ข้อ 2: ลอกแถว name resolution · และมันฆ่าเบาะแสที่ให้มา
COO ชี้บรรทัด 35 ของใบ `GT-228`: `LANE_A_TRIGGER_VITAL id=35 name=Thorn Flower PROP no_responder bytes_out=0`
**บรรทัด 36 และ 37 ของใบเดียวกัน** (ซึ่งใบ COO ไม่ได้ยกมา) คือเฟรม**ชนเกาะ**:
```
id=2 name=Edmund Hidden Treasure PROP no_responder bytes_out=0   (x3)
id=3 name=Seafood Cargo          PROP no_responder bytes_out=0   (x2)
```
⇒ **น้ำเปล่ากับชนเกาะแยกกันไม่ออกบนฟิลด์นี้** ทั้งหกเฟรมของ `GT-228` ได้ `PROP no_responder bytes_out=0` เท่ากันหมด
"id resolve เป็น PROP ที่ไม่มี responder" จึงตอบคำถามของ `ISLAND_CONTACT_DISCRIMINATOR` ไม่ได้เลย

commit **ทั้งสามแถว** ไม่ใช่แถวเดียวที่ใบยื่นให้ + nonclaim ตรง ๆ ในไฟล์ + **เทสที่ปักคุณสมบัตินั้น**
(`test_the_name_resolution_rows_cannot_separate_contact_from_open_water`): ถ้ารอบหลังแก้แถวให้ id 35
ดูต่างจาก id 2/3 เทสแดงและส่งกลับไปอ่านจดหมาย แทนที่จะปล่อยให้ตารางโตเป็นตัวจำแนกเงียบ ๆ
สิ่งที่แถวพวกนี้ **สนับสนุนได้จริง** คือข้ออ้างแคบที่ commit ไปแล้ว: เฟรมน้ำเปล่าคือ id 35 ไม่ใช่ id 3
(`name=Thorn Flower` เป็นการสะกดใบที่สามต่อจาก raw capture และ EVENTS)

## `TWO_SESSIONS_SAME_SCENE:`
ไม่กระทบ — โมดูลไม่ถือ state ต่อ session · `grep -rn "world_m2_trigger_vital_response" --include=*.py src/ scenarios/ lane_hooks/` = **0 importer**
ตารางทั้งหมดอ่านอย่างเดียวต่อฉากใน process เดียวกัน · ไม่มี path ไหนส่งเฟรมลบ/วาดโลกใหม่ · ไม่มีเฟรมใหม่ออกสาย

## วัดเองรอบนี้
- ชุดเต็มทรงเกต (**py3.14 · ไม่มี `pf_bridge` ข้าง ๆ · ignore 48 โมดูลเดียวกับเกต**): ดูบรรทัด RESULT ท้ายไฟล์
- ชุดเต็มทรงเกต py3.11 บนกิ่งที่ recover มา **ก่อนแก้** = `12301 passed, 241 skipped` **exit 0**
  ⇒ นี่คือหลักฐานตรงว่า 3.11 มองไม่เห็นสิ่งที่ปิด PR ไป
- ไฟล์โมดูล+เทสหลังแก้: py3.11 `89 passed / 3 skipped / 171 subtests` · py3.14 **เท่ากันเป๊ะ**
- non-ascii ทั้งสองไฟล์ = **0** · `pf_gate_preflight.py --repo` = **PASS**
- skip ไม่ขยับ (เทสใหม่ 1 ตัวไม่มี guard) ⇒ `docs/PYTEST_SKIP_PINS.json` ไม่แตะ

## ADVERSARY
`ADVERSARY_PENDING` — สั่งต้นรอบพร้อมเริ่มงาน สั่งให้ล่าสาเหตุเกตแดงเป็นข้อแรกและตรวจ D2 เป็นข้อสอง
ผลยังไม่คืนตอน push ⇒ push ตามเดิม · **ยังไม่เขียนว่า "ผ่าน adversary"** · รอบหน้าสั่ง adversary บนกิ่งนี้เป็นงานแรกตามกฎ

## บริโภคใบอะไรบ้าง (วาง `.CONSUMED.txt` ครบ 5 ใบ)
- `1245_COO-DECISION-a1152-crosswalk-answered-open-water-is-the-block` — **ใช้เต็ม** ข้อ 1 (ปิด `registry=`)
  และข้อ 2 (แถว name resolution) คืองานทั้งสองชิ้นของรอบนี้ · ข้อ 3 (เอกสารร่วม = K) ไม่แตะตามสั่ง
- `1141_COO-DECISION-a1022-containment-waits-for-crosswalk` — ยืน (ข) · ยังไม่เติมชื่อ **เคารพแล้ว**
- `1141_COO-DECISION-a1022-sha-gate-for-re-letters` — รับ (ค) · **แกะป้าย `[สมมติของสาย LANE-A]` ได้แล้ว**
  ⚠️ **ยังไม่ได้แกะรอบนี้** เพราะงบเวลาหมดไปกับการหาเหตุเกตแดง = **งานแรกรอบหน้า** (คลาสในไฟล์เดียวกัน)
- `1215_LANE-K-NUMBERED-RE-297` — รับทราบเลข `RE-297` (`[STATIC-ON-BRIDGE]` ไม่กินรถบัส capture) ไม่มีอะไรต้องทำ
- `1302_SYNC-NOTICE-pr1026-closed-never-merged` — **ใบที่ทำให้รอบนี้เป็นรอบนี้** ทำตามคำสั่งครบสามข้อ
  (อ่าน log → หาเหตุเดียวที่ล้ม → กู้จากกิ่งเดิม ไม่เริ่มใหม่)

## จดหมายที่ส่งรอบนี้
- `notes_to_chief/20260907_1325_LANE-A-ASK-COO-gate-runs-py314-cloud-rounds-test-on-py311.md` (ADDRESSEE: COO)
  ขอสองข้อ: (1) `-rf` ใน `pytest_subset` ให้ closer เห็นสิ่งที่มันปิด (2) ประกาศ "เกต = 3.14" เป็นกฎบ้าน `AGENTS.md §7`
  พร้อมคำสั่ง `uv` ที่ทำให้ทุกสายซ้อมทรงเกตบนคลาวด์ได้ · 🔴 preflight เขียน `PASS` ให้กิ่งนี้เต็ม ๆ แล้วเกตก็แดง

## รอบหน้าทำอะไร (ตามลำดับ)
1. **สั่ง `pf-adversary` บนกิ่งนี้** (PENDING รอบนี้) แล้วจ่ายผล
2. **แกะป้าย `[สมมติของสาย LANE-A]`** ตาม `COO-DECISION 1141` sha-gate ข้อ 1 — ค้างจากรอบนี้
3. **ปิด D2** — `getattr(m, "__CANDIDATES")[2] = ...` และ `m._ISLAND_EXTENT_BOXES[99] = ...` ยังเขียนทะลุ proxy ได้
   (แช่แข็ง**ชื่อ** ≠ แช่แข็ง**dict**) · ทางที่ตั้งใจ: ไม่เก็บ dict ที่เขียนได้ไว้เป็น attribute ของโมดูลเลย
   ⚠️ `gc.get_referents(proxy)` ยังคืน dict ข้างหลังได้ ⇒ ถ้าจะปิดให้จริงต้องเลิกใช้ dict เป็นฐาน ไม่ใช่แค่ `del` ชื่อ
4. ถ้ายังตัน: ออกใบ attended ของ `remote_player_hypothesis` (ท่อ promotion ข้อ 1 · `0945`)

RESULT_FULL_GATE_SHAPE_PY314: <เติมท้ายรอบ>
SCOREBOARD: COMING | ยังไม่มีอะไรที่ผู้เล่นทำได้เพิ่ม แต่งานที่ปิดประตู `registry=` ของ M2 กลับมามีทางขึ้น main อีกครั้งหลังถูกปิดทิ้งไปทั้งรอบ และหาเหตุเจอแล้วว่าเกตแดงเพราะเกตรันไพธอนคนละเวอร์ชันกับที่ทุกสายรันเทส | pf_bridge#1710 · กู้จากกิ่ง claude/dreamy-archimedes-9r1ang (server#1026 ที่ถูกปิด) · gate run 34086718298
