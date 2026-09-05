round dio9ll
start 2026-09-06T00:02+07:00
LANE-A · executes COO-DECISION `20260905_2349` (GT-233 v3, option ข) + D1/D2/D4/D6/D7/D10 from pf-adversary round `tk4hr7`

## 1. อะไรขยับ (NOW.md / M ข้อไหน)

M2 (บันไดไมล์สโตน "ออกจากเมืองได้") -- ตัวบล็อกโค้ดที่เหลือของ M2 คือ D1+ผู้สมัคร (ข) ตาม
`COO-DECISION 20260905_2349` ข้อ 4-5 ("D1 + ผู้สมัคร (ข) ใน PR เดียวกัน (เรื่องเดียวกัน = ทำให้
`GT-233` v3 ยิงได้) · ห้ามบูต `GT-233` v3 ก่อน D1 ขึ้น `main`"). รอบนี้ปิดทั้งสองข้อในกิ่งเดียว
(pirate-force-server PR, ดูข้อ 3) และแก้หัว `GT-233` ในคิวเป็น v3 (ข้อ 2)

## 2. โค้ด (pirate-force-server, กิ่ง `claude/magical-goldberg-dio9ll`)

**D1 (HIGH, วัดแล้วโดย pf-adversary รอบ `tk4hr7`)**: `world_m2_sailing_result_key.py` เคย bind
`AREA_126_SAILING_RESULT_IDS` ที่ module scope (`_load_ids()` เรียกตอน import) ⇒ ทุกบูตของ
`runtime.py` (ไม่ว่ามีแฟล็กหรือไม่) ต้อง hash ไฟล์สำเนา TSV ให้ผ่านก่อนถึงจะ import จบ · ไฟล์เพี้ยน
= เซิร์ฟเวอร์ไม่บูตเลย บนเครื่อง Panya ในนัดที่ไม่มี BACKUP ก็เหมือนกัน
แก้: ลบ binding ที่ module scope ออก เพิ่ม `area_126_sailing_result_ids()` ที่อ่าน+verify สำเนา
ใหม่ทุกครั้งที่เรียก (ไม่ cache) ตามแบบ `world_marker_copy.py` ที่ไม่เคย bind แถวไว้ที่ module scope
เลยสักฟังก์ชัน
**ทดสอบมือ (นอกเหนือจาก pytest)**: เติม newline ท้ายสำเนา TSV จริงในดิสก์ แล้ว
`import pirateforce_foundation.runtime` -- **import ผ่านสำเร็จ** (ก่อนแก้จะ raise
`SailingResultCopyError` ตั้งแต่ import) เรียก `provisional_area_126_key()` ต่อ ⇒
raise ตามคาด (sha256 mismatch) แล้ว restore ไฟล์กลับ ยืนยันด้วย `git diff` ว่าไม่มีร่องรอยค้าง

**ผู้สมัคร (ข) -- discriminate คอลัมน์ ไม่ใช่แถว (`COO-DECISION 20260905_2349` ข้อ 1)**: ลบ
`provisional_area_126_keys(count)` (ให้สองเรคอร์ดถือ `n_ID` สองแถวต่างกัน, D1 เดิมของ pf-adversary
รอบ `wjprxa` ที่แก้ "ซ้ำแถวเดียว" แต่ยังไม่เคยแก้ "ยังไม่รู้คอลัมน์") แทนด้วย
`column_discriminating_keys(count)`: dock 153 (Prison Exile) = `provisional_area_126_key()`
(`n_ID` ต่ำสุด, ปัจจุบัน `1`) ทดสอบสมมติฐาน "คีย์ = n_ID" · dock 154 (Spice Paradise) =
`n_area_key()` (= `126`, ค่า `n_AREA` เอง) ทดสอบสมมติฐาน "คีย์ = n_AREA" -- RE-265 วัดแค่ว่า
`+0x14` เป็น key เข้า store จริง ไม่เคยวัดว่าคอลัมน์ไหน (pf-adversary D3) เดิมสมมติ `n_ID` ลอย ๆ
**ปิด D8 ไปด้วย**: คู่เดิม (`1`,`2`) ทำให้ key ของเกาะ 3 บังเอิญเท่ากับ `+0x12` (survey_id) ของ
เกาะ 2 พอดี -- คู่ใหม่ (`1`,`126`) ไม่ตรงกับ `+0x12` ฝั่งไหนเลย (`2`/`3`)

**D2 (HIGH, วัดแล้ว)**: `test_a_tampered_copy_is_refused_not_silently_trusted` เคยเขียนทับ artifact
ที่ track อยู่จริงแล้ว restore ใน `finally` -- process ตายกลางเทส = ไฟล์ tracked ค้างการแก้
แก้: ชี้ `COPY_PATH` ไปไฟล์ใน `tempfile.TemporaryDirectory()` แทน (แบบเดียวกับ
`test_world_marker_copy.py::test_editing_the_copy_without_moving_the_pin_is_refused`)

**D4 (MEDIUM, วัดแล้ว)**: docstring อ้างว่า 18 แถวมี `n_ITEM_ID=3` -- ตรวจ TSV จริงแล้ว
`n_ITEM_ID` = `0` ทุกแถว เลข `3` เป็นของ `n_VARI_3` -- แก้คำในโมดูล

**D6 (LOW, วัดแล้ว)**: note ใน `docs/PYTEST_SKIP_PINS.json` มีประโยคยืนยันจากในรีโปไม่ได้ ("Gate
RED" ของ `#847` ไม่มีเลข job) และชี้ผิดรีโป (พูดถึง `AGENTS.md` เฉย ๆ ทั้งที่สูตรอยู่
`pf_bridge/AGENTS.md:176-181`) -- แก้คำใส่เลข job `101313822248` และชื่อรีโปให้ตรง

**D7 (LOW, วัดแล้ว)**: `_load_ids()` ไม่เคยเช็คว่า `n_ID` ซ้ำ (การรับประกัน "ไม่ซ้ำ" มาจากเทสข้างเคียง
เท่านั้น) -- เพิ่ม `len(ids) != len(set(ids))` guard ใน `_load_ids()` เอง

**D10 (LOW)**: คอมเมนต์ `unmeasured_0x14` ใน `navigationex_survey_record.py` ยังเขียนว่า
"UNMEASURED" ทั้งที่ RE-265 วัดความหมายบางส่วนแล้ว (เป็น key จริง แค่ยังไม่รู้คอลัมน์) -- แก้คำ

## 3. หลักฐานสองชั้น

**ชั้น client-observable/behavioral**: `import pirateforce_foundation.runtime` สำเร็จแม้สำเนา TSV
เพี้ยน (ก่อนแก้ = ล้มตั้งแต่ import) -- ทดสอบมือ ดูข้อ 2

**ชั้น wire/DB**: `pytest tests/ -q` เต็มชุด (ครั้งเดียว บน commit สุดท้ายจริงหลัง
`git merge origin/main`, commit `c186874`) = **11429 passed / 355 skipped / 21121 subtests /
0 failed** (378.49s) · `tools_bridge/pf_gate_preflight.py --repo pirate-force-server` = PASS
(cp874 / no new skips / mainmerge / census / bridgesize ทั้งหมดเขียว หลังแก้ข้อ 5)
เก็บ `git diff` ของกิ่งไว้ครบก่อน push

## 4. GT-233 v3 (pf_bridge, `GAME_TEST_QUEUE.md`)

แก้หัวใบจาก `READY-v2` เป็น `READY-v3` เติมบล็อกควตอธิบาย: สองเรคอร์ด discriminate คอลัมน์แทนแถว
(dock 153 = `n_ID`=1, dock 154 = `n_AREA`=126) · ปิด D8 · **ประโยคบังคับ**: "เงียบทั้งสองนัด ≠
ทฤษฎี `SAILING_RESULT` key ผิด -- แปลว่ายังไม่รู้ว่าคอลัมน์ไหนคือ key" (`COO-DECISION 20260905_2349`
ข้อ 2) · เกณฑ์ผ่าน/ทางบูตเดิม (v2) ไม่เปลี่ยน ยังห้ามบูตจนกว่า PR ของรอบนี้ขึ้น `main`

**ไม่ทำในรอบนี้**: item 3 ของ `2349` (เปิดใบ RE ต่อ RE-265 ที่ `0x0072F700`) -- การตั้งเลขใบเป็น
ของ chief จึงส่งจดหมายขอเลขแทน (ดูข้อ 6) ไม่บล็อก `GT-233` v3 ตามที่จดหมายเขียนไว้เอง

## 5. เพดานไฟล์ (`AGENTS.md` §7 · `pf_gate_preflight.py`)

แก้ `GAME_TEST_QUEUE.md` (เติมบล็อก v3) ทำให้ไฟล์โตกว่า `origin/main` ขณะที่ไฟล์เกินเพดาน 300 KB
อยู่แล้ว (หนี้เก่า) ⇒ preflight ขึ้น RED ครั้งแรก -- แก้ตามที่เครื่องมือสั่ง: archive ใบที่ CLOSED
เกิน 24 ชม. ที่ยังไม่เคย archive ไปที่ `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`
เลือก `GT-244` (CANCELLED, ปิดโดย chief 2026-09-04, ตรวจแล้วไม่ชนกับ `GT-172` ที่ยังเปิดอยู่ --
เนื้อใบพูดถึงกันแต่ไม่ได้แก้ `GT-172` เอง) เหลือ stub บรรทัดเดียวไว้ที่เดิม ไม่ลบต้นฉบับ (ย้ายไป
archive ตามกฎ) ผลหลังแก้: ไฟล์เล็กกว่า `origin/main` เดิม (`2330173` < `2340179` bytes) ⇒
preflight PASS ทุกข้อ ไม่แตะใบของสายอื่นนอกจากใบนี้ใบเดียว

## 6. จดหมายรอบนี้

- บริโภค: `20260905_2349_COO-DECISION-*` (ใบสั่งงานหลักของรอบนี้) · `20260905_2245_COO-DECISION-
  a852-closed-by-gate-*` (บริโภคย้อนหลังในนามของรอบ `tk4hr7` ที่ทำจริงแล้วแต่ไม่ได้วาง stub ไว้)
- ส่ง: `20260906_0004_LANE-A-TO-CHIEF-re-ticket-request-sailing-result-key-column-derivation-
  0x0072F700.md` (ขอเลขใบ RE ต่อ RE-265 ตาม `2349` ข้อ 3 -- grep `external/PF_PROTOCOL_REGISTRY.tsv`
  `external/PF_SERIALIZER_FIELDS.tsv` แล้วไม่เจอ layout ของ `0x0072F700` เขียนไว้ในจดหมาย)
- **ยังไม่บริโภค ยกไปรอบหน้า** (ไม่ใช่เรื่องของรอบนี้): `0805_LANE-B-TO-LANE-A-scene14-responder` ·
  `1152_COO-DECISION-world-registry` · `1506_SYNC-NOTICE-pf_bridge-pr1319` ·
  `2052_COO-DECISION-third-admission-arm` (ใช้ตอน re-land cast 304) ·
  `2056_COO-DECISION-lane-q-needs-world-registry-interface`

## 7. adversary

สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงาน (ก่อน commit) ให้ตรวจ diff ทั้งชุด (D1/D2/D4/D6/D7/D10 +
การออกแบบ column-discriminating ใหม่) -- ผลยังไม่คืนตอน push ⇒ `ADVERSARY_PENDING
pirate-force-server (กิ่ง claude/magical-goldberg-dio9ll)` ตามกฎ ห้ามเขียนว่า "ผ่าน adversary"
ก่อนผลคืน · รอบถัดไปของสาย A อ่านผลบนกิ่งนี้เป็นงานแรกถ้ายังไม่คืนตอนจบรอบนี้

## 8. ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ยังไม่เห็นอะไรใหม่บนจอ (`GT-233` v3 ยังไม่มีใครบูต ต้อง attended) -- แต่สิ่งที่พร้อมจริงตอนนี้:
เซิร์ฟเวอร์ไม่มีทางล้มทั้งบูตอีกต่อไปเพราะไฟล์ SAILING_RESULT สำเนาเพี้ยน (D1 ปิด) และเมื่อ Panya
บูต `GT-233` v3 ครั้งถัดไป ผลจะแยกแยะได้จริงว่าคอลัมน์ไหนคือ key แทนที่จะเสี่ยงเงียบทั้งคู่แบบตีความ
ไม่ได้เหมือน v2

## 9. สถานะท้ายรอบ

push ครบทั้งสองรีโป · `pirate-force-server`: เปิด PR ไม่ draft หัว `[LANE-A]` มี
`PF-AUTOMERGE: v4` ตั้งแต่เปิด (ดูเลข PR ในจดหมาย/PR body) · `pf_bridge`: claim
`pf_bridge#1396` เติม marker ปลดล็อกหลัง PR เซิร์ฟเวอร์ยืนยันเปิดไม่ draft มี marker แล้ว ·
ไม่รอ gate ไม่รอ merge ก่อนปิดรอบ

## รอบหน้าทำอะไร

0. อ่านผล `pf-adversary` บนกิ่ง `claude/magical-goldberg-dio9ll` ก่อนอย่างอื่น ถ้ายังไม่คืนตอนจบ
   รอบนี้
1. วัดว่า PR ของรอบนี้ขึ้น `main` หรือยังด้วย `git merge-base --is-ancestor`
2. เมื่อขึ้น `main` แล้ว แจ้ง chief พลิกหัว `GT-233` v3 เป็นบูตได้จริง (ตาม `2349` ข้อ 5)
3. re-land cast ฉาก 304 จากกิ่ง `claude/great-ride-yob0a2` (`#847`) -- ยังค้างจากรอบ `tk4hr7`
   ไม่ใช่งานของรอบนี้
4. บริโภคจดหมายที่ยกมาในข้อ 6 เมื่อถึงคิว

SCOREBOARD: COMING | เซิร์ฟเวอร์ไม่มีทางล้มทั้งบูตอีกต่อไปเพราะไฟล์ SAILING_RESULT สำเนาเพี้ยน (D1) และ `GT-233` v3 ใช้สองเรคอร์ดแยกแยะคอลัมน์คีย์จริงแทนแยกแยะแถว (ปิด D8) -- ผู้เล่นยังไม่เห็นอะไรใหม่จนกว่า PR จะ merge และ Panya บูต `GT-233` v3 | PR: pirate-force-server (กิ่ง `claude/magical-goldberg-dio9ll`), claim `pf_bridge#1396`, ชุดเต็ม 11429 passed/0 failed, gate preflight PASS
