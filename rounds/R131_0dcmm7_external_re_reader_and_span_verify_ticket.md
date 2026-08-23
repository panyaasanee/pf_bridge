# R131 (0dcmm7) — โค้ดอ่านชุดส่งมอบ RE ตัวแรก + ใบ GT-054 span-verify + whitelist 3 ตารางท้าย

**เวลา:** 2026-08-23 ~20:5x–21:xx (+07:00) · session `exciting-goldberg-0dcmm7`
**ล็อก:** draft PR #32 (`pf_bridge`) เปิดก่อนทำงานตามลำดับ v5 ① — empty commit `round claim: exciting-goldberg-0dcmm7`
(รอบนี้ล็อกไม่หลุด — เปิดเป็น draft ตั้งแต่วินาทีแรก)

## probe ต้นรอบ (กติกา v4/v5)

| ข้อ | ผล |
|---|---|
| GitHub API/tool อ่านได้ไหม | ✅ list PR ทั้งสอง repo สำเร็จ (ผลว่างทั้งคู่ = ล็อกว่าง) |
| ทาง D (`ci-status`) มีชีวิตไหม | ✅ `git fetch origin ci-status` + `ls-tree` บน `pirate-force-server` เห็น `ci/<sha>.json` ปกติ (`d_exit=0`) |

## สภาพต้นรอบ

- `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` ✅ มีจริง (11,388 ไบต์)
- 🎉 **ตัวบล็อกหลักของ R130 ปลดแล้ว:** `external/` เข้า `main` แล้วจริง — commit `284d986`
  "external: publish Codex RE deliverable tables (Panya ruling 2026-08-23)" · 5 ตาราง + ดัชนี อยู่บนดิสก์ clone รอบนี้ครบ
- กล่องจดหมาย: ใบใหม่หนึ่งใบ `20260823_2039_REPLY-R129-...-PANYA-RULING-push-as-is.md` — บริโภคแล้ว (copy + stub)
  ใจความ: ① ตาราง 5 ใบตรงชื่อดิสก์เป๊ะ ② 3 ตารางท้ายชื่อ `PF_PROTOCOL_PRIORITY/PF_DATA_EVIDENCE/PF_TAG_CENSUS` สะอาด
  ③ 🔴 คำตัดสิน Panya: push ทั้งไฟล์ ไม่ mask + **เส้นใหม่เรื่อง proprietary** (ดูท้ายไฟล์นี้) ④ ห้าม whitelist `.py` โดยไม่ตรวจแยก

## งานหลักของรอบ: EXTERNAL-RE-READER-001

**คำสั่งที่สนอง:** Panya 18:22 ข้อ ⑤ ("ยังไม่มีโค้ดอ่านชุดส่งมอบเลย — จดเป็นรายการค้างที่มองเห็นได้")
+ จดหมาย 20:39 ข้อ ⑤ ("cc เริ่มสร้างตัวอ่าน+ตรวจ sha ใน `pirate-force-server/tools/` ได้เมื่อเห็นไฟล์")

**ของที่สร้าง (repo `pirate-force-server` · branch `claude/amazing-goodall-0dcmm7`):**

| ไฟล์ | อะไร |
|---|---|
| `tools/pf_external_registry.py` (ใหม่) | ตัวอ่าน/ค้น/ตรวจตารางชุดส่งมอบ — pin sha256+rows+header ทั้ง 5 ตาราง · cross-check 6 invariant · CLI `--stats/--message/--verify/--verify-spans/--measure` · fail-closed ทุกทาง (`REFUSED` exit 3 เมื่อไม่มีตาราง/อิมเมจ) · ASCII-only output |
| `tests/test_external_registry.py` (ใหม่) | 16 เทส: 4 refusal (รันได้ทุกเครื่องรวม Actions) · 3 snapshot (pin + golden `TriggerCastSkillVital` ตรงดัชนี byte-per-byte) · 9 mutation (สำเนา+พังทีละอย่าง ต้องแดงดัง ๆ) |
| `tests/pf_preconditions.py` (แก้) | key ใหม่ `external_re_tables` — ตารางอยู่ repo พี่น้อง เครื่องที่ checkout repo เดียว (gate Actions) ไม่มีทางมี ⇒ skip แบบประกาศ+pin |
| `docs/PYTEST_SKIP_PINS.json` (แก้) | pin 12 เทสที่ guard ด้วย key ใหม่ |
| `.gitignore` (แก้) | whitelist `tools/pf_external_registry.py` (repo นี้ deny-all รายไฟล์) |

**ข้อเท็จจริงที่วัดจากตารางจริงก่อน pin (ไม่ได้ลอกจากจดหมาย):**
- 519 messages · 6,931 field rows · join สองทางครบ 519 ทั้งคู่ · order ต่อเนื่อง 1..n ทุกกลุ่ม (1,038 กลุ่ม = 519×2 ทิศ)
- section delta คงที่สองค่า: code `va = file_off + 0x400C00` (reg_site 519/519 · getter 504/504 ที่รู้ค่า) ·
  data `va = file_off + 0x401C00` (name 519/519 · vtable 502/502)
- ทุก `file_off_claim` ที่ parse ได้ map กลับเข้าไปอยู่ **ใน** span ของแถวตัวเอง (0 หลุด)
- 16 messages ที่ registry ไม่รู้ `serializer_va` = 16 ตัวที่ field rows (W+R = 32 แถว) ไม่มี span **พอดีเป๊ะ**
- 202 แถว tag `EMPTY` ทุกแถวมี span จริง · `field_offset` เป็นภาษา expression (มีแค่ 1,726/6,931 ที่เป็น `+0x` ตรง ๆ)
  ⇒ reader เปิดเผยเป็น string ตามต้นฉบับ **ไม่เดา ไม่ parse เกินที่รู้**
- ⚠️ สิ่งที่ **ไม่** pin เพราะวัดแล้วไม่จริง: `span_start` ≠ `serializer_va` ของ registry ถึง 3,020 แถว ·
  149 กลุ่ม (message,direction) มีหลาย span ⇒ span เป็นของรายแถว ไม่ใช่รายกลุ่ม

**ผลรัน (cloud sanity):** สวีตเต็ม **เขียว(cloud sanity) 1917 passed / 324 skipped / 0 failed** (เดิม 1901 — +16 ของรอบนี้)
· `pf_pytest_precondition_census.py --run` = **PASS** · seam test 22 passed (แตะ `.gitignore` จึงต้องรัน — กฎเหล็ก)
· commit ฝั่งโค้ด `53ca7ef` push ขึ้น `claude/amazing-goodall-0dcmm7` แล้ว (PR รอ gate — ดูท้ายไฟล์)

**pf-adversary (บังคับตาม v5 ④):** ยิงจริง วัดจริง — **พบ 6 defect แก้ครบทุกข้อก่อน commit:**
1. **HIGH:** tool มองไม่เห็นใน git (`/tools/*` deny-all — ลืม whitelist) ⇒ ถ้า commit ตามชุดไฟล์ที่ประกาศ gate จะ
   collection-error ทั้งโมดูล ⇒ เพิ่ม `.gitignore` เข้า commit เดียวกัน (ชุดไฟล์เป็น 5)
2. **HIGH (ตัวร้ายสุด):** gate สร้าง `--ignore` list ด้วย `Select-String 'GameClient|capture_v141'` บน `tests\*.py` —
   ไฟล์เทสมีคำนั้น 2 จุด ⇒ **ทั้งโมดูลจะถูกเมินบน Actions เงียบ ๆ แล้วทุกอย่างยังเขียว** (census อ่าน excluded = expect 0)
   ⇒ ล้างคำต้องห้ามออกหมด + เขียนเหตุผลกันคนเผลอเติมกลับ · วัดซ้ำ: isolation run = `4 passed, 12 skipped` ตาม pin
3. **MED-HIGH:** `--verify-spans ""` (เช่น `%VAR%` ว่างใน batch สะพาน) ตกลงไปโหมด stats แล้ว **exit 0 โดยไม่ hash อะไรเลย**
   ⇒ dispatch เป็น `is not None` + refuse ว่าง + เทสกันถอย
4. **MED:** cell พังหลุดเป็น traceback ดิบแทน `FAILED:` ⇒ `_hex/_int` fail-closed + backstop `FAILED: unexpected`
5. **MED:** ใต้ `--no-sha` คอลัมน์ที่ไม่มี delta-check (serializer/handler/id_global/_ptr) แก้เป็นขยะได้โดยไม่แดง
   ⇒ format gate ทั้ง registry (รับ pipe-list `0x..|0x..` เฉพาะสอง `_ptr` คอลัมน์ · pin 2+2 แถวตามที่วัด) + sha ต้องเป็น hex แท้
6. **LOW:** คอมเมนต์เทส refusal อ้างลำดับเช็กผิดฝั่ง + assertion หลวมจนจับไม่ได้ ⇒ แก้ทั้งคู่ (assert ข้อความ refusal ตรงตัว)
**ข้อเสนอเชิงดีไซน์ของ adversary ที่รับมาทำเลย:** pin **commit ของ `pf_bridge`** ที่ pins ถูกวัด (`PF_BRIDGE_PIN_COMMIT = 284d986...`)
— วันที่สะพาน regen ตารางแล้ว clone ใหม่แดง จะตอบได้จาก repo โค้ดฝั่งเดียวว่าโค้ดเขียนกับชุดไหน
**สิ่งที่ adversary ยิงแล้วไม่ล้ม (วัดเองอิสระ):** pins ทุกตัวตรง TSV · delta สองค่า uniform จริง · claim-in-span 6,899/6,899 ·
`--verify-spans` โกหกเขียวไม่ได้ (นอกจากช่อง 3 ที่อุดแล้ว) · cp874 สะอาด · CRLF ถูกหักล้าง (`.gitattributes * -text`)
**ผลหลังแก้:** เทสโมดูลนี้ 16 ใบ · สวีตเต็ม 1917/324/0 · census PASS (pin ขยับ 10→12 ใน commit เดียวกัน)

## ฝั่ง `pf_bridge` รอบนี้

1. **`.gitignore`:** whitelist 3 ตารางท้าย (`PF_PROTOCOL_PRIORITY.tsv` · `PF_DATA_EVIDENCE.tsv` · `PF_TAG_CENSUS.tsv`)
   ตามชื่อที่จดหมาย 20:39 ยืนยัน — เหลือฝั่งสะพาน `git add` สามไฟล์ (คำขอทวนอยู่ในจดหมาย FROM_CHIEF_R131)
2. **`CLIENT_RE_QUEUE.md`:** ① อัปเดตบล็อกสถานะ (5/8 เข้า main แล้ว · reader มาแล้ว · เหลือ 3 ตาราง)
   ② 🆕 **ใบ GT-054 SPAN-VERIFY-EXTERNAL-REGISTRY** (ร่างโดย pf-queue-author) — รัน `--verify-spans` กับอิมเมจบนสะพาน
   คาด `spans=392 verified=392 mismatched=0 unreadable=0` · 🔴 กำกับ "รอ merge ก่อน" ตามกติกา
3. **`GAME_TEST_QUEUE.md`:** อัปเดตสารบัญ 🔬 (เพิ่ม GT-054 + แก้บรรทัด "ยังไม่มีโค้ดอ่าน" ที่ล้าสมัยแล้ว)
4. **`IMAGE_ACCESS_COST.tsv`:** +1 แถว (span ground truth ต้องใช้อิมเมจ — workaround partial ผ่าน GT-054)
5. บริโภคจดหมาย 20:39 (copy + stub)

## 🔴 เรื่องที่ต้องส่งต่อให้ Panya ตัดสิน/รับรู้ (อยู่ในจดหมาย FROM_CHIEF_R131 ด้วย)

- **จดหมาย 20:39 ขอให้แก้ข้อความกฎเหล็ก "ห้ามอัปโหลด proprietary" ใน prompt ของ Routine** ให้ตรงเส้นใหม่ที่ Panya เคาะ
  (ห้ามเด็ดขาด: อิมเมจทั้งไฟล์ · capture corpus · `.dmp` · canonical DB — ขึ้นได้: metadata ที่ derive รวม byte string สั้นในตารางวิเคราะห์)
  🔴 **chief แก้ routine เองไม่ได้** (Panya เป็นคนสร้าง/แก้ routine — กติกา v4) ⇒ เขียนถ้อยคำแทนที่ให้พร้อมใช้ในจดหมาย R131 แล้ว
  **รอ Panya วางเอง**

## nonclaims ของรอบ

- ไม่ได้อ้างว่าตารางชุดส่งมอบ **ถูกต้อง** — reader ตรวจ internal consistency + sha ไฟล์เท่านั้น ·
  ground truth ต้องรอ GT-054 (span vs อิมเมจ บนสะพาน)
- ไม่ได้อ้างว่า mapping `0x400C00` ใช้ได้กับทุก span ใน **อิมเมจจริง** — พิสูจน์แค่ในตาราง (claim-in-span 100%) ·
  ถ้า GT-054 เจอ mismatch/unreadable นั่นคือข่าวที่ต้องเห็น ไม่ใช่ bug ของใบ
- ไม่ได้อ้างว่า W row = client ส่งจริง · ไม่รู้ความหมายฟิลด์ · `PF_RUNTIME_CLASSMAP` ชื่อคลาส UNKNOWN แทบทั้งหมด (ตามดัชนี)
- เขียว(cloud sanity) ≠ เขียว gate — PR ฝั่งโค้ดรอ Actions ตัดสิน
