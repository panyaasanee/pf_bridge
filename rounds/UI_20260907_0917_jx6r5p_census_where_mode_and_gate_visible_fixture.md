# LANE-UI round `jx6r5p` -- 2026-09-07T09:17+07:00 start

## เวลา
บรรทัดล่าสุดของ `notes_to_chief/_BRIDGE_HEARTBEAT.txt` ตอนต้นรอบ = `2026-09-07T09:10:02+07:00`
ต่างจากเวลาเริ่มรอบ 7 นาที ไม่เกิน 60 นาที -- ไม่มีอะไรต้องแก้

## ล็อกรอบ
list `[LANE-UI] round *: claim` ที่เปิดอยู่ใน `pf_bridge` ก่อนเริ่ม: **ว่าง**
(ที่เปิดอยู่ตอนนั้น `#1669` K · `#1668` CS · `#1667` B · `#1666` Q · `#1664` A · `#1662` GM ·
`#1659` addendum ของสายเราเอง (ไม่ใช่ claim) · `#1644`/`#1642`/`#1629`/`#1595`/`#1583`/`#1493`
addendum ของสายอื่น -- ไม่ใช่ล็อก ไม่แตะ)
⇒ เปิด claim `pf_bridge#1670` จากกิ่ง `claude/kind-archimedes-jx6r5p` (กิ่งที่ระบบมอบให้)
กิ่งฝั่งเซิร์ฟเวอร์ `claude/ecstatic-franklin-jx6r5p`
list ซ้ำหลังเปิด: ยังเป็น `[LANE-UI] round ... claim` ใบเดียว ไม่มีใบเก่ากว่าแข่ง

## แหล่งความจริงที่อ่านต้นรอบ (ตามลำดับ)
1. `NOW.md` (COO รอบ `0845`) บรรทัด LANE-UI: **"พิน 30/286/11 · evidence ตัดเลขบรรทัด (`0845`) ปิด ·
   งานแรก `2032` แถบ n/327 · tool ข้าม docstring (AST) · express/community ห้าม"**
2. กล่องจดหมาย `ADDRESSEE: LANE-UI` ที่ยังไม่ consumed: **2 ใบ** (`0845` ui0758 · `0845` ui0801)
   บริโภคทั้งคู่ในรอบนี้ (stub + สำเนาใน `consumed/`)
3. `AGENTS.md` §7 + `prompts/COMMON_LANE_ROUND.md`
4. ไฟล์รอบล่าสุด `UI_20260907_0747_o50gly_*` "รอบหน้าทำอะไร" ข้อ 0 = **รับผล
   `ADVERSARY_PENDING pirate-force-server#1005`** · ข้อ 1 = ยืนยัน sha อยู่บน main · ข้อ 3 = ตอบใบ `0801`
5. คิวในไฟล์สาย -- ข้อ 1-2 (UI-B/UI-A) ยังติด `RE-266`

## รอบนี้ขยับ NOW/M ข้อไหน
ไม่ขยับ M ใด (M2 = A · M3 รอ `GT-288` ของ B) · บรรทัด LANE-UI ของ `NOW.md`:
- "evidence ตัดเลขบรรทัด ปิด" -- **ปิดจริง แต่ปิดไม่สนิท**: การชดเชยที่ใบปิดนั้นเสนอไว้เอง
  (`grep -n`) วัดแล้วผิด 18/30 แถว ⇒ รอบนี้เปลี่ยนการชดเชยเป็นกลไก ไม่ใช่ประโยค
- "งานแรก `2032` แถบ n/327" -- เครื่องมือของงานนั้นเองคือสิ่งที่ซ่อมรอบนี้ (สคริปต์ + หน้า + เทส)
  แต่ **หัวเลข 30/327 ไม่ขยับ** และรอบนี้ไม่ได้เพิ่มความสามารถให้ผู้เล่น พูดตรง ๆ ตามนั้น
- ท่อ promotion ข้อ 4 (`item_operate_res`) -- **ตัดออกจากคิว UI แล้ว** ตามใบ `0801` (เจ้าของ = B)

## 0. ยืนยันด้วยคำสั่ง ไม่ใช่ความจำ
`git merge-base --is-ancestor a764679 origin/main` = **YES** · `c5cd08d` = **YES**
⇒ `#1005` ของรอบ `o50gly` **merge แล้วจริง** รูปแบบ `evidence` ใหม่ (ไฟล์ล้วน) อยู่บน main
สั่ง `pf-adversary` บนกิ่งฝั่งเซิร์ฟเวอร์ทันทีหลัง push คอมมิตแรก (ดูข้อ 4)

## 1. งานแรก = ผล adversary ของ `#1005` (D1/D2) -- ทั้งคู่เป็นความผิดของรอบก่อนเอง
ผลคืนหลังปลดล็อกรอบ `o50gly` และถูกบันทึกไว้ใน `pf_bridge#1659` (addendum · ยังเปิด)
สายอ่านเอง **แล้ววัดซ้ำเองทุกข้อก่อนรับ** ไม่ได้เชื่อรายงาน

### D2 (HIGH) -- คำสั่งกู้เลขบรรทัดที่แจกไปสามที่ ผิด 18 จาก 30 แถว
รอบ `o50gly` ตัดเลขบรรทัดออกจาก `evidence` แล้วเสนอ `grep -n "<name>" <file>` เป็นการชดเชย
(ในคอมมิตเมสเสจ · ในคอมเมนต์ของ tool · ใน `docs/UI_WIRE_COVERAGE.md`)
`grep` คืน**ทุก**บรรทัดที่มีชื่อ รวม docstring และคอมเมนต์เต็มบรรทัด ซึ่ง census ไม่นับ
วัดเองบน `82a3b54` ครบทั้ง 30 แถว SOURCE:
```
VitalData        grep-first=110  counted=115   damage_hp_link_hypothesis.py
TargetVital      grep-first=105  counted=147   diag_multi_object_wiring.py
ActionVital      grep-first= 87  counted=225   mob_combat.py
TeleportVital    grep-first=  1  counted=601   gm/teleport_wire.py
TargetPosVital   grep-first=162  counted=1419  mob_drop_presence.py
UpdateAttrVital  grep-first= 19  counted=998   damage_hp_link_hypothesis.py
... อีก 12 แถว                  รวม 18 จาก 30 ไม่ตรง
```
🔴 สองแถวที่เป็นเหตุให้ตัดเลขบรรทัดตั้งแต่แรก อยู่ใน 18 นั้นด้วย: `gm/command_capture.py` สะกด
`GM_RunGMCommandVital` และ `Activity_CheatCodeVital` ไว้ใน **module docstring บรรทัด 3 และ 4**
ขณะที่ census นับที่ 800 และ 853 ⇒ คำสั่งกู้ที่แจกไป คืนของที่รอบ `9dezrf`/`mg3nr4` จ่ายไปเพื่อตัดทิ้งพอดี

**แก้ด้วยกลไก ไม่ใช่ประโยคใหม่**: เพิ่มโหมด `--where NAME`
```
$ python3 tools/pf_ui_wire_name_census.py --where GM_RunGMCommandVital
src/pirateforce_foundation/gm/command_capture.py:800
$ python3 tools/pf_ui_wire_name_census.py --where Pets_SummonPetVital ; echo $?
NOT A SOURCE ROW: ... 1
```
`source_hit_location()` ใช้ `code_token_lines()` และลำดับไฟล์ **ตัวเดียวกับ** `_build_source_hits`
(แยกออกมาจากฟังก์ชันนั้นในคอมมิตนี้) ⇒ ตรงกันโดยโครงสร้าง ไม่ใช่โดยการดูแลด้วยมือ ·
อ่านเฉพาะรีโปนี้ ⇒ ตอบได้บนเช็คเอาต์ที่ไม่มี `pf_bridge` ข้าง ๆ ซึ่งเป็นที่ที่คนอ่านมักอยู่
🔴 **18 เขียนลงหน้าเป็น "ค่าที่วัดบนคอมมิตชื่อนี้" ไม่ใช่พิน** ไม่มีเทสไหน assert เลขนี้ --
พินเลขที่ derive จากไฟล์ของสายอื่นคือค่าเช่าข้ามสายที่รอบ `mg3nr4`/`o50gly` เพิ่งจ่ายไปเพื่อรื้อทิ้ง
ห้ามพามันกลับมาในชื่อใหม่

### D1 (HIGH) -- คลาสที่ "ไม่ติดการ์ดเพื่อให้รันบนเกต" พิสูจน์อะไรไม่ได้กับการย้อนแบบมีเงื่อนไข
`EvidenceIsInsensitiveToUnrelatedEditsTests` ไม่ติดการ์ดจริง แต่ไฟล์สังเคราะห์ทุกไฟล์ชื่อ
`ui_probe_wire.py` และยาวไม่เกิน 52 บรรทัด ขณะที่ **ไม่มีสักแถวใน 30 แถว SOURCE จริงที่อยู่ในไฟล์
`ui_*`** และสองแถวที่งานทั้งหมดตั้งอยู่บนมันอยู่หลังบรรทัด 800 ของไฟล์ 857 บรรทัด
⇒ มิวแทนต์ที่ใส่เลขบรรทัดกลับ **แบบมีเงื่อนไข** ผ่านคลาสนี้ 34/34 ในทรงของ `gate-windows`
และเทสสองใบที่จับได้ ติดการ์ด `UI_WIRE_CENSUS_INPUTS` ทั้งคู่ = ข้ามบนเกต · **รูของมันคือ fixture ไม่ใช่ assertion**

แก้: fixture ใช้ชื่อไฟล์ที่ไม่ใช่ `ui_*` (`runtime.py`, `delete_actor.py`) + padding 150 บรรทัด
และเพิ่มเทส cross-product (`ui_`/ไม่ใช่ `ui_`) x (สั้น/ยาว) x (hit บรรทัด 1 / hit หลังบรรทัด 150)
วัดหลังแก้ โดยรัน **เฉพาะคลาสที่ไม่ติดการ์ด** (`-k "EvidenceIsInsensitive or SourceHitLocation or MainWhereFlag"`
= ส่วนที่เกตมองเห็น):
```
relpath if path.name.startswith("ui_") ...            8 failed  (เดิม 0)
relpath if len(text.split(LF)) <= 100 ...             7 failed  (เดิม 0)
relpath if _lineno <= 60 ...                          7 failed  (เดิม 0)
relpath if "src/pirateforce_foundation/ui_" in ...    8 failed  (เดิม 0)
f"{relpath}:{_lineno}" (ไม่มีเงื่อนไข)               10 failed
baseline                                             12 passed
```
มิวแทนต์ของโค้ดใหม่อีกสี่ตัว (ตัด comment skip · ตัด prose skip · `--where` สแกนข้อความดิบแบบ grep ·
`--where` คืนบรรทัดคงที่) = 3-4 failed ต่อตัวในชุดเดียวกัน ไม่มีตัวไหนรอด

### D3-D8 ยังไม่ทำในรอบนี้ -- บันทึกไว้ตรง ๆ
D4 (เลข `30/286/11` ลอยในหน้า) **ปิดโดย COO-DECISION `0845`** · D3/D5/D6/D7/D8 ยังเปิด
(D8 = นโยบาย "first hit wins" ไม่มีพินที่ไม่ติดการ์ด) ⇒ ยกไปรอบหน้า ไม่อ้างว่าทำแล้ว

## 2. ที่ไม่ขยับ และเหตุผล
- อาร์ทิแฟกต์ `reports/PF_UI_WIRE_NAME_CENSUS_20260906.tsv` **ไบต์เท่าเดิม** · หัวเลข `30/286/11` เท่าเดิม
- `python3 tools/pf_ui_wire_name_census.py` = `PASS -- committed artifact matches a fresh re-derive`
- ไม่มีโค้ด production เปลี่ยน · ไม่มีเฟรมถึงไคลเอนต์ · ไม่มีสิทธิ์ใหม่
- `docs/UI_LANE.md` ไม่มีแถวไหนถูกแตะ (รอบนี้ไม่มีชื่อ vital ข้าม tier) จึงไม่แก้

## 3. บริโภคจดหมาย -- สองใบ
- `20260907_0845_COO-DECISION-ui0758-*` ⇒ ปลดป้าย `[สมมติของสาย LANE-UI]` · เลขทางการ 30/286/11
  ตรงกับพินอยู่แล้ว ไม่แตะพิน · `KNOWN_RED_MAIN:` ของ census ไม่ต่ออายุ (ชุดเต็มรอบนี้ 0 failed)
- `20260907_0845_COO-DECISION-ui0801-*` ⇒ **ส่งจดหมายโคเดกถึง LANE-B หนึ่งใบตามสั่ง**
  `notes_to_chief/20260907_0917_LANE-UI-TO-B-greenline-codec-item-move-delta-response.md`
  (`inventory.make_item_move_delta_response` · ทรง BAGUPD · ฟิลด์ครบ · `$V2` = ยอดรวมปลายทาง ·
  template id 0x83 `ได้รับ [ $V1 ] * $V2` · อ้าง `GT-063` R158 · จุดยิงหลัง
  `store.commit_acquired_backpack_item` ที่ `mob_pickup_persist.py:628`) · **ไม่ยื่น CORE-REQUEST**
  ตามที่ใบสั่ง · ไม่แตะโค้ด B/`runtime.py`/`store.py`/`mob_pickup*` แม้แต่บรรทัดเดียว
ทั้งสองใบวาง stub `.CONSUMED.txt` + สำเนาใน `consumed/` ไม่ลบต้นฉบับ

## 4. pf-adversary
สั่งบนกิ่ง `claude/ecstatic-franklin-jx6r5p` คอมมิต `7d836b1` ทันทีหลัง push คอมมิตแรก
บรีฟเจ็ดข้อ เน้น **ข้อ 4** (มิวแทนต์ของโค้ดใหม่ทั้งหมด + มีอะไรพินว่า `--where` ห้ามเรียก
`build_rows()` ไหม) และ **ข้อ 6** (ยังมีที่ไหนอีกที่บอกคนอ่านว่า evidence มีเลขบรรทัด หรือยังแนะ
`grep -n`) · กำชับ `try/finally` + `git status --porcelain` หลังทุกสคริปต์ที่แก้ไฟล์
🔴 **ผลยังไม่คืนตอน push** ⇒ `ADVERSARY_PENDING pirate-force-server#1013`
**ห้ามเขียนว่า "ผ่าน adversary"** · รอบถัดไปของสายนี้รับผลนี้เป็นงานแรก (ถ้าคืนหลังปลดล็อก
ให้ทำเป็น addendum ของรอบนี้)
ระหว่างรอ self-review เอง: อ่านทุก hunk ใน `git diff --cached` ก่อน commit · รัน
`tests/test_ui_wire_name_census.py` เดี่ยวทุกครั้งที่แก้ · รันมิวแทนต์เก้าตัวข้างบนเอง

## บล็อกเกอร์เดิม -- บันทึกครั้งเดียว ไม่ใช้รอบไปตรวจซ้ำ
`RE-266` (`CLIENT_RE_QUEUE.md:1135`) ยัง **OPEN** ⇒ คิวข้อ 1 (UI-B ล็อกเอาต์) และข้อ 2 (UI-A
กลับหน้าเลือกตัวละคร) ยังเดินต่อไม่ได้ · ตอบเมื่อไร = งานแรกของรอบนั้นทันที

## เกต / หลักฐาน
- `python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server` = **PREFLIGHT PASS**
  (รวม `--pr-body ... --pr-stage final` = PASS หนึ่งบรรทัด marker บรรทัดที่ 107)
- `tests/test_ui_wire_name_census.py` เดี่ยว = **53 passed, 6 subtests passed** (เดิม 44)
- ชุดเต็ม (`pytest tests/`) รันบนต้นไม้หลัง `git merge origin/main` (Already up to date)
  บนคอมมิตสุดท้ายจริงของรอบ (`3f3a55d`) -- **กำลังรัน ผลเติมในคอมมิตถัดไปของกิ่งนี้**
  🔴 รอบแรกที่สั่งไว้ถูกยกเลิกทิ้งโดยตั้งใจ เพราะระหว่างรันมีการแก้ docstring ของ tool
  (คอมมิต `3f3a55d`) ⇒ ผลนั้นไม่ได้อยู่บนต้นไม้สุดท้าย จึงรันใหม่แทนที่จะรายงานผลของทรีเก่า
- ไม่ stage ด้วย `git add -A` · ไม่มี skip ใหม่ · `docs/PYTEST_SKIP_PINS.json` ไม่ถูกแตะ ·
  ไม่ปิด/ข้ามเทสใดเพื่อให้เขียว · ไม่แตะ canonical DB · ไม่แตะ `.claude/` · ไม่แตะ `prompts/` ·
  ไม่แตะ `v141` · ไม่แก้ `NOW.md` · ไม่แก้หัวใบใน `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md`

## นอนเคลม
- รอบนี้ **ผู้เล่นไม่ได้อะไรใหม่** -- ไม่มีโค้ด production เปลี่ยน · `--where` เป็นของคนอ่าน
  ไม่ใช่เกตใหม่ (ไม่มีอะไรใน CI เรียกมัน และอาร์ทิแฟกต์ไม่ได้ถือผลของมัน)
- ไม่ได้อ้างว่าอาร์ทิแฟกต์ drift ไม่ได้อีก -- ชื่อข้าม tier หรือย้ายไฟล์ยังเขียนใหม่ (หน้าที่ของมัน)
- `SOURCE` ไม่ได้แปลว่า `WIRED` (`AGENTS.md` §7) · `n/327` นับ **ชื่อ** ไม่ใช่ความสามารถ
- **ไม่ได้อ้างว่าผ่าน adversary** -- ผลยังไม่คืน (`ADVERSARY_PENDING`)
- 18/30 คือค่าที่วัดบน `82a3b54` ไม่ใช่ค่าคงที่ของโปรเจกต์ -- แก้ไฟล์ของสายอื่นแล้วเลขนี้ขยับได้
- ไม่ได้บูตเกม ไม่ได้ขอเครื่องเจ้าของ · จดหมายถึง B เป็นการส่งโคเดก ไม่ใช่การอ้างว่าเห็นบรรทัดเขียว
  ขึ้นจากเส้นทาง pickup จริง (ครึ่งนั้นเป็นใบ GT ที่ B ควรเปิด)
- PR ฝั่งเซิร์ฟเวอร์ = **"เปิดแล้ว รอ gate"** ไม่ใช่ landed/อยู่บน main
  (อยู่บน main ต่อเมื่อรอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`)

## รอบหน้าทำอะไร
0. **งานแรก = รับผล `ADVERSARY_PENDING pirate-force-server#1013`** (สั่งบน `7d836b1`)
   ข้อที่บรีฟให้โจมตีหนักสุด: **ข้อ 4** (มิวแทนต์ของ `code_token_lines`/`source_hit_location`/
   `--where` และมีอะไรพินว่า `--where` ห้ามเรียก `build_rows()` ไหม) · **ข้อ 6** (ที่อื่นที่ยังบอกว่า
   evidence มีเลขบรรทัด หรือยังแนะ `grep -n`) · **ข้อ 1** (หาทรีที่ `--where` กับ census ไม่ตรงกัน)
1. ยืนยัน `#1013` อยู่บน main จริงด้วย `git merge-base --is-ancestor 7d836b1 origin/main`
2. **D3/D5/D6/D7/D8 ของรายงาน `#1005`** (ยังเปิด · D4 ปิดแล้วโดย COO `0845`) --
   หยิบ **D8** ก่อน: นโยบาย "first hit wins" ยังไม่มีพินที่ไม่ติดการ์ด มิวแทนต์ "last hit wins"
   ได้ 34 passed / 0 killers ในทรงเกต · รูปเดียวกับ D1 เป๊ะ ⇒ ปิดด้วยเทสในคลาสที่ไม่ติดการ์ด
   ถัดไป **D7** (`docs/PYTEST_SKIP_PINS.json` note ยังเขียน "10 failed / 1 passed" ทั้งที่วัดได้
   10 failed / 34 passed)
3. คิวข้อ 1-2 (UI-B ล็อกเอาต์ · UI-A กลับหน้าเลือกตัวละคร) ยังติด `RE-266` -- blocker เดิม
   บันทึกแล้ว **ห้ามใช้รอบไปตรวจซ้ำ** · `RE-266` ตอบเมื่อไร ข้อนี้ขึ้นเป็นงานแรกทันที
4. ฟังก์ชันถัดไปในแผน `docs/UI_LANE.md` ที่ `layout รู้แล้ว` -- หยิบทีละตัว implement + เทส + ใบ GT
   (นี่คือทางเดียวที่ `n/327` จะขึ้นด้วยโค้ดจริง ไม่ใช่ด้วยการพิมพ์ชื่อลงเอกสาร)
5. ถ้า LANE-B ตอบจดหมายโคเดก `0917` ⇒ ตอบข้อสงสัยเรื่องทรง/ฟิลด์ให้จบในรอบนั้น ไม่ยึดงานคืน

## สองคอมมิตของรอบนี้ (ฝั่งเซิร์ฟเวอร์ `#1013`)
- `7d836b1` -- `--where` + shared `code_token_lines()` + fixture ที่เกตมองเห็น (D1/D2)
- `3f3a55d` -- docstring ของ `_build_source_hits` ยังเขียน `relpath:line` ทั้งที่ค่าหยุดถือเลขบรรทัด
  ตั้งแต่รอบ `o50gly` (เจอเองตอนกวาดหาที่อื่นที่ยังบอกคนอ่านผิด · เอกสารล้วน ไม่มีพฤติกรรมเปลี่ยน)
🔴 pf-adversary ถูกสั่งบน `7d836b1` ไม่ใช่หัวกิ่งปัจจุบัน -- รอบหน้าที่รับผลต้องอ่านด้วยข้อนี้ในมือ

SCOREBOARD: NONE | รอบนี้ผู้เล่นไม่ได้อะไรใหม่ -- ซ่อมเครื่องวัดของตัวเอง: คำสั่งกู้เลขบรรทัดที่รอบก่อนแจกไว้ผิด 18/30 แถว เปลี่ยนเป็นโหมด `--where` ที่ใช้กฎเดียวกับ census และปิดรูที่ทำให้เทสบนเกตจับการย้อนแบบมีเงื่อนไขไม่ได้เลย | pf_bridge#1670 (claim) · pirate-force-server#1013 · 7d836b1 3f3a55d
