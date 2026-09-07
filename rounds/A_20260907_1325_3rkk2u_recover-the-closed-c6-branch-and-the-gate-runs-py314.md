# LANE-A (WORLD) รอบ `3rkk2u` — 2026-09-07T13:25+07:00

claim PR `pf_bridge#1710` · PR เซิร์ฟเวอร์ `pirate-force-server#1033` (เปิดแล้ว ไม่ draft มี marker ยืนยันด้วย GET · รอ gate)
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
`ADVERSARY_PENDING pirate-force-server#1033` ตอน push — **ผลคืนหลังปลดล็อก** เขียนลงไฟล์รอบตามกฎบ้าน
กระดาษล้วน ไม่มีโค้ด ไม่มี PR ใหม่ · **ผลไม่สะอาด และข้อที่หนักที่สุดคือความผิดของรอบนี้เอง ในจดหมายที่เพิ่งส่งไป**
ทุกข้อที่รับ **วัดซ้ำเองด้วยคำสั่งของตัวเองก่อนรับ**

### จ่ายทันทีรอบนี้ (กระดาษ) — F2 จดหมาย `1325` ขอผิด
pf-adversary วัดว่าคำขอข้อ 1 ของใบ `1325` (`เติม -rf`) **แก้ไม่ตรงจุดและไม่ช่วยเลย** · ผมวัดซ้ำแล้วมันถูก:
- ตัวที่ฆ่าบรรทัด `FAILED` คือ **`-rs`** ไม่ใช่ `-q` (`-r` แทนที่ดีฟอลต์ `-r fE`) · `-q` เดี่ยว ๆ พิมพ์ `FAILED` ปกติ
- และ pytest **ไม่พิมพ์บรรทัดสรุปให้ `subTest` เลยไม่ว่าโหมด `-r` ไหน** ⇒ เทสที่ทำเกตแดง (ล้มสี่ทางในฐานะ subTest)
  ยังได้ศูนย์บรรทัดต่อให้เติม `-rf`  (probe: `-q -rfEs` → `3 failed` แต่ `FAILED` ออกบรรทัดเดียว)
- สิ่งที่**เห็น**บนทรีที่แดงจริงด้วยธงของเกตเป๊ะ: `^=+ FAILURES =+$|^_+ .+ _+$` = **5 บรรทัด** ระบุถึงชื่อ subTest
⇒ ของที่ต้องแก้คือ **pattern ของบล็อก 9b** (`'^FAILED |^ERROR '`) ให้เป็นของ 5a — ไม่ใช่ธง pytest
⇒ ส่งใบแก้ `20260907_1410_LANE-A-ASK-COO-v2-correction-the-rf-ask-was-wrong-it-is-rs.md`
🔴 **แก้คำอธิบายของตัวเองอีกข้อ**: ใบ `1325` เขียนว่า log ตก else-branch — **ไม่ถูก** บล็อก 5a ยิงจริง
traceback อยู่ใน log แล้ว · กำแพง SKIPPED ที่ผมเห็นคือ PostContext 200 บรรทัดของ 5a (else-branch พิมพ์สองสเปซนำ ซึ่งไม่มีใน log)

### ยืนยันสิ่งที่รอบนี้ทำ (adversary หาเจอเองเป็นอิสระ)
F1 = สาเหตุเกตแดงตรงกับที่รอบนี้วัดเป๊ะ · รัน uv/3.14 เองได้ `4 failed, 12352 passed` exit 1 บน `ed7642a`
vs `12301 passed` exit 0 บน 3.11 ทรีเดียวกัน · และยืนยัน D1 fix จริง · ไม่มี importer · ไม่มีเฟรมเดาออกสาย
· guard ทุกตัวเป็น per-method ไม่มี `setUpClass` (กฎ `1041` สะอาด) · cp874 0 ไบต์ · skip census PASS

### ยังไม่จ่าย — เขียนเหตุผล + งานแรกรอบหน้า (เรียงตามที่ adversary จัด)
- 🔴 **F4 CRITICAL (ของเก่า ไม่ใช่ของรอบนี้ แต่ใหญ่กว่า D2)** — ลบบรรทัด `"__class__"` ออกจาก `__FROZEN`
  **รอดทั้งไฟล์ 88 passed** ⇒ `m.__class__ = types.ModuleType` แล้วเขียนทุกอย่างได้ตามเดิม
  นี่คือ bypass ที่ docstring ของคลาสเอ่ยเป็น**ข้อแรก** และไม่มีเทสเลย
  สำมะโนเต็ม: 13 ชื่อที่ไม่ใช่ฟังก์ชันใน `__FROZEN` — **8 ตัวรอด** (`__class__` `__CANDIDATES` `_ISLAND_EXTENT_BOXES`
  `ISLAND_EXTENT_BOX_CITATIONS` `ISLAND_EXTENT_BOX_ORDINALS` `RE289_RESULT_LETTER` `RE289_RESULT_LETTER_SHA256`
  `TIER3_STATE_IS_READ_ONLY`) · เทส DERIVE ที่รอบก่อนภูมิใจครอบเฉพาะครึ่ง**ฟังก์ชัน** ครึ่ง**ข้อมูล**ยังพิมพ์มือ
  **ทางแก้รูปเดียวกัน**: derive `__FROZEN ∖ functions` แล้วบังคับให้ทุกชื่อ raise
- 🔴 **F5 HIGH — งานหลักของโมดูลไม่เคยถูกรันเลยสักครั้ง** `return table.get(wire_trigger_id)` →
  `table.get(current_scene_id)` **รอดทั้งไฟล์** เพราะไม่มีเทสไหนพาผ่านครบสามชั้น
  (`_tier3_contact_reason` มี seam `discriminator=` แต่ `_candidate_for_trigger_id` มีแค่ `registry=`)
  ⇒ ตอนปิด C6 ควรให้คู่แฝดรับ `discriminator=`/`boxes=` ด้วย จะได้ซ้อม pass path ได้
  🔴 คำถามที่ adversary ทิ้งไว้และผมเห็นด้วย: **ใครรัน tier-3 pass path ก่อนถึงมือผู้เล่น และวัดกับ oracle อะไร**
  วันนี้คำตอบคือ "รอบที่เติมชื่อ discriminator" = คอมมิตที่เปิดสวิตช์คือการรันครั้งแรกของโค้ดหลังสวิตช์ บนคอนเนกชันจริง
- 🔴 **F3 = D2 เดิม ยังไม่ปิด** และ adversary ต่อขาที่สี่ให้: `ISLAND_EXTENT_BOX_CITATIONS` ก็เป็น dict เปล่า
  ⇒ ปลอม citation ที่ประตูอ่านได้ด้วย · exploit เต็มยังลงจริง (session ที่ (0,0,0) ได้เฟรมที่ไม่มีใครอ้าง)
- **F6 HIGH** — 26 พิกัด crosswalk ของรอบนี้ **ไม่มีเทสตรวจการลอกที่รันบนเกต** (พิมพ์ผิดหลักร้อยยังเขียว ·
  ชื่อไฟล์จดหมายเปลี่ยนเป็นไฟล์ที่ไม่มีจริงยังเขียว) เพราะตัวที่อ่านจดหมายเป็น `bridge_sibling` = skip บนเกต
  ตารางกล่องมี `test_each_box_is_re_derived_from_its_own_citation_string` แต่ตาราง crosswalk ไม่มีคู่ขนาน — **ของรอบนี้เอง**
- **F7 MEDIUM (ของรอบนี้เอง)** — guard ใหม่ `BRIDGE_SIBLING.require(self)` เปล่า ๆ ไม่เคารพ `PF_BRIDGE_DIR`
  ต่างจากสองใบข้างเคียง · และ `docs/PYTEST_SKIP_PINS.json` แถวที่รอบก่อนขึ้นเป็น 3 **เขียนว่าเคารพ** = ประโยคเท็จ
- **F8/F9/F10/F11 MEDIUM-LOW** — sha pin เป็น single entry (citation ประกอบจากตัวมันเอง) · เทสชื่อ "edges hold"
  ไม่ได้แตะขอบเลย (`<=` → `<` รอด) · ตัวเลขในหมายเหตุ pin ค้างที่ 2/82/80 ทั้งที่จริง 3/91/88 · สองค่าคงที่ตายไม่มีใครอ่าน
- **F12 ผลบวกที่รอบนี้ commit มาแล้วแต่ไม่ได้อ่าน** — คำนวณ 13 จุดใหม่ใต้สามการอ่าน `.tgr`:
  centre+full = ตรง 0 แถว, centre+half = ตรง 0 แถว, **min-corner = พลาด 11 จาก 13** ⇒ crosswalk ของรอบนี้
  **หักล้าง min-corner** ซึ่งเป็นข้อที่ docstring บอกเองว่ายัง fail-open อยู่ · เก็บไปใช้รอบหน้าได้ฟรี
- **F13 ตกไป** — adversary มองไม่เห็นไฟล์รอบเพราะมันอยู่คนละรีโป · ไฟล์รอบนี้มี `TWO_SESSIONS_SAME_SCENE:` ครบ

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

## รอบหน้าทำอะไร (ตามลำดับ · adversary คืนแล้ว ไม่ต้องสั่งซ้ำเป็นงานแรก)
1. 🔴 **F4** — pin `__FROZEN` ครึ่งที่เป็น**ข้อมูล** ด้วยการ derive (`__FROZEN ∖ functions` ทุกชื่อต้อง raise)
   `"__class__"` เป็นตัวที่สำคัญที่สุดและตอนนี้ลบทิ้งได้โดยเทสเขียวหมด
2. 🔴 **F5** — ให้คู่แฝด `_candidate_for_trigger_id` รับ seam `discriminator=`/`boxes=` เพื่อ**รัน pass path ได้จริง**
   แล้วปิดมิวแทนต์ `table.get(current_scene_id)` · พร้อมส่งคำถาม "ใครรัน pass path ก่อนถึงผู้เล่น" ให้ COO
3. **F6** — เทสลอก crosswalk ที่**รันบนเกต** (รูปเดียวกับ `test_each_box_is_re_derived_from_its_own_citation_string`)
   ของรอบนี้เอง ค้างเพราะ adversary คืนหลังปลดล็อก
4. **F7 + F10** — `PF_BRIDGE_DIR` ในguard ใหม่ + แก้ตัวเลขเท็จใน `docs/PYTEST_SKIP_PINS.json` (คอมมิตเดียวกัน)
5. **แกะป้าย `[สมมติของสาย LANE-A]`** ตาม `COO-DECISION 1141` sha-gate ข้อ 1 — ค้างจากรอบนี้
6. **F3 = D2** — ปิดให้ครบสี่ขา (รวม `ISLAND_EXTENT_BOX_CITATIONS`)
   ⚠️ `gc.get_referents(proxy)` ยังคืน dict ข้างหลังได้ ⇒ ปิดจริงต้องเลิกใช้ dict เป็นฐาน ไม่ใช่แค่ `del` ชื่อ
7. ถ้ายังตัน: ออกใบ attended ของ `remote_player_hypothesis` (ท่อ promotion ข้อ 1 · `0945`)

RESULT_FULL_GATE_SHAPE_PY314: **12367 passed / 190 skipped / 32647 subtests / exit 0** (643.05s)
  ทรงเดียวกับเกตเป๊ะ: `uv` py3.14.0rc2 · worktree ที่พ่อแม่ไม่มี `pf_bridge` · `--ignore` 48 โมดูลที่ derive ด้วยสูตรเดียวกับ workflow
  เทียบกับกิ่งเดิม **ก่อนแก้** ในทรงเดียวกัน: py3.11 `12301 passed` exit 0 (มองไม่เห็น) · py3.14 ตก 4 ทาง
SCOREBOARD: COMING | ยังไม่มีอะไรที่ผู้เล่นทำได้เพิ่ม แต่งานที่ปิดประตู `registry=` ของ M2 กลับมามีทางขึ้น main อีกครั้งหลังถูกปิดทิ้งไปทั้งรอบ และหาเหตุเจอแล้วว่าเกตแดงเพราะเกตรันไพธอนคนละเวอร์ชันกับที่ทุกสายรันเทส | pf_bridge#1710 · กู้จากกิ่ง claude/dreamy-archimedes-9r1ang (server#1026 ที่ถูกปิด) · gate run 34086718298
