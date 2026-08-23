# R135 (ahfyuy) — บริโภคผล PASS 3 ใบ + กฎ prefix GT-/RE- + แก้ erratum 0xAC52 ในโค้ด

- **เวลา:** 2026-08-24 ~08:0x–08:3x (+07:00) · (UTC: 2026-08-24 01:0x–01:3x)
- **เซสชัน:** ahfyuy · branch `claude/exciting-goldberg-ahfyuy` (pf_bridge) · `claude/amazing-goodall-ahfyuy` (server)
- **ล็อก:** draft PR #36 (pf_bridge) เปิดเป็น draft ก่อนเริ่มงานตาม v5 ① — จับได้ปกติ

## Probe (ตามบท)
- GitHub API/tool: ✅ อ่านรายการ PR ทั้งสอง repo + เปิด draft PR #36 ได้จริงในรอบนี้
- ทาง D: ✅ `git fetch origin ci-status` + `ls-tree` สำเร็จ (`d_exit=0` · ไฟล์ verdict ครบ)

## สถานะต้นรอบ
- โครงพี่น้อง: `VITAL_REGISTRY_*.tsv` มีจริง ✅ · pf_bridge main = `63ceef3` (sync สะพานเดินอยู่ทุก ~5 นาที) · server main = `1e0b20b`
- กล่องจดหมาย: **4 ใบใหม่** — บริโภคครบ (copy + stub ตามกติกา R108):
  1. `20260824_0025` คำสั่ง Panya: แยก prefix `GT-`/`RE-` + กฎโฟลเดอร์ external/gamedata
  2. `20260824_0033` **GT-054 PASS** — spans 392/392 verified · mismatch 0 · image_sha256 `96272114…8623`
  3. `20260824_0038` **GT-053 PASS** — `Bg0002.npc` N=106 ≥ 61 · index 60 f32 bit-exact ⇒ `0x203D` in-band ⇒ **H1 รอด**
  4. `20260824_0044` **GT-052 PASS** — crosswalk class/skill ครบ (5 อาชีพ · 2165 สกิล · ชื่อ 898 จุดตัด · bit 8 = Voodoo)
     · ผลลบสำคัญ: **label ของ `n_TARGET` codes พิสูจน์ไม่ได้ — ห้ามตั้งชื่อความหมาย**

## งานของรอบ

### ① คิว (pf_bridge)
- ปิด 3 ใบใน `CLIENT_RE_QUEUE.md`: status header → ✅ PASS/DONE + กรอกช่อง `result:` จากจดหมายผล (คงช่องค้นบังคับสองช่อง)
- หัวไฟล์สองคิวได้กฎ prefix ตามคำสั่ง 0025 · **จุดตัดสินที่ต้องจด:** คำสั่งเขียน "เริ่มที่ใบ 055" แต่ใบ 055
  ถูกออกเป็น `GT-055` แล้วใน R134 (ก่อนคำสั่งถึงมือ chief) ⇒ ยึดกฎ "ห้ามเปลี่ยนชื่อใบที่ commit แล้ว"
  (บทเรียนจดหมาย 1605/1656 ที่คำสั่ง 0025 เองก็อ้าง) ⇒ **จุดเริ่มจริงของ prefix ใหม่ = 056** · เขียนเหตุผลกำกับไว้ในหัวไฟล์คิวแล้ว
- `GAME_TEST_QUEUE.md`: เพิ่มบล็อก 📌 R135 + อัปเดตดัชนี 🔬 (เหลือเปิดฝั่ง static: GT-050 · GT-055 · GT-047 จ็อบ 0 · GT-049 ตัวยิง)

### ② โค้ด (pirate-force-server · branch `claude/amazing-goodall-ahfyuy`)
แก้ erratum R134 §5.2 — ประโยค stale `"unknown to the server registry"` ของ 0xAC52:
จริงเฉพาะ v141 · `PF_VITAL_NAMES.json` ตั้งชื่อ `Channel_LocalTalkMessageVital` ให้ตั้งแต่ RESOLVE-001 (รอบ 62)
⇒ ถ้อยคำใหม่: **"absent from the v141 registry"** + ชี้ names table · คง identifier `UNKNOWN_0xAC52` (ไม่ rename)
- **ขอบเขตจริงใหญ่กว่าที่ R134 จด (พิน 4 ที่ → เจอจริง 5 ที่มีชีวิต):**
  1. `src/pirateforce_foundation/chat_input_hypothesis.py` (docstring)
  2. `tests/test_chat_channel_family_static.py` (pin ประโยค — เพิ่ม pin ชื่อ resolved ด้วย)
  3. 🆕 `tools/pf_chat_channel_family_static.py` (docstring + guard ~:950 — **pin ที่ R134 ไม่ได้จด**)
  4. `docs/FUNCTIONAL_COVERAGE.json` (notes)
  5. 🆕 `STATUS.md` (**pin ที่ R134 ไม่ได้จด**)
- คงเดิมโดยเจตนา (ประวัติศาสตร์): `docs/HYPOTHESIS_LEDGER.json` · `reports/*.md` สองใบ
- **แถมจาก adversary D1:** ปลุก dead guard 4 จุดในไฟล์ tool+test เดียวกัน (needle `0x` ตัวเล็ก vs haystack
  `.upper()` — บั๊กมีมาก่อน R135) ให้กลับมา live · ปลุกแล้วยังเขียว = ไม่มี drift จริงซ่อนอยู่
- เทส: `pytest tests/` = **1917 passed / 324 skipped / 0 failed เขียว(cloud sanity)** (เท่าฐาน R131 · รันซ้ำหลังแก้ D1 ก็เท่าเดิม) ·
  seam + coverage tests ผ่าน (กฎเหล็ก: แตะ coverage ⇒ รัน seam ก่อน ✅) · gate จริงรอ Actions บน PR

### ③ ผลสืบเนื่องที่จดแล้วไม่ทำในรอบนี้
- **GT-054 PASS ⇒ spans ทั้ง 392 ของ `PF_SERIALIZER_FIELDS.tsv` verified กับอิมเมจแล้ว** — AGREE ที่ยืนบน span
  ใน `FINDINGS_R134_EXTERNAL_XCHECK.md` (เช่น CHitResult §2.1) แข็งขึ้นหนึ่งชั้น · **ไม่ครอบ** คอลัมน์ VA ของ
  `PF_PROTOCOL_REGISTRY.tsv` (AGREE §2.2) และตารางอื่นของชุดส่งมอบ (scope ตาม adversary D3 · ไม่แก้ไฟล์ findings ย้อนหลัง)
- **คำถามค้างถึง Panya (จาก R134 · ตอนนี้ live แล้วเพราะ GT-054 ผ่าน):** เปิด provenance ชั้น 4 ให้
  `PF_VITAL_NAMES.json` ปิดชื่อ 0x16A0/0x1661/0x16F7 จากชุดส่งมอบที่ verify แล้วได้ไหม (กับดัก: 0x1661 เป็น standing negative ใน src/)
- **เปลี่ยนชื่อ `external\` → `clientbin\`:** เงื่อนไข "รอ GT-054 จบ" ปลดแล้ว แต่ต้องทำทีเดียวพร้อมกันทั้ง
  โฟลเดอร์จริงบนสะพาน (ไฟล์ส่วนหนึ่งไม่อยู่ใน git) + tool hardcode + `.gitignore` + ทุกใบที่อ้าง ⇒ ต้องนัดจังหวะกับ
  ผู้ช่วย/หน้าสะพาน — เขียนข้อเสนอในจดหมาย ไม่ทำฝ่ายเดียวจาก cloud

## ลูกมือ
- `pf-adversary` 1 รอบก่อน commit (~110k tokens) — **จับ 4 defect แก้ครบก่อน commit:**
  - **D1 (มีมาก่อน R135 · false green):** guard/assert เพื่อนบ้านในไฟล์เดียวกันสร้าง needle `"0x%04X" % id`
    (ตัว `x` เล็ก) แล้วค้นใน haystack `.upper()` ⇒ ไม่มีวันเจอ = dead check — tool :939/:946 + test :678/:687
    ⇒ แก้เป็น `("0x%04X" % id).upper()` ทั้ง 4 จุด · ปลุกแล้ว **ยังเขียวจริง** (v141 ไม่มี id ทั้ง 17 · chat มีแค่ 0xAC52)
  - **D2:** ต้อง stage consumed copies + stubs ให้ครบตอน commit (จดหมาย 0025 คือต้นฉบับคำสั่งที่หัวคิวอ้าง) ⇒ นับ staged เทียบประกาศ
  - **D3 (claim elevation):** "ตารางส่งมอบยกชั้น verified" กว้างเกิน — GT-054 ครอบเฉพาะ spans ของ
    `PF_SERIALIZER_FIELDS.tsv` ไม่ครอบ VA columns/ตารางอื่น ⇒ scope ถ้อยคำใหม่ 4 ที่ (GTQ 📌 · RE-queue result · continuation · ไฟล์นี้)
  - **D4:** หัว GT-052 "label พิสูจน์ไม่ได้" แรงกว่าจดหมาย ⇒ แก้เป็น "ไม่พบ legend ในชุดที่ค้น"
  - จุดที่ adversary ลองหักแล้วไม่แตก: การอ่าน 055→056 (timeline พิสูจน์ GT-055 เข้า git ก่อนคำสั่ง 82 วินาที ·
    ทางอ่าน rename ขัด clause ห้าม rename ในคำสั่งเดียวกันเอง) · ตัวเลข/sha ทุกช่อง result ตรงจดหมายต้นทาง ·
    ถ้อยคำใหม่ cp874-safe · pin ที่แก้ไม่อยู่ในเงา skip (test PASSED จริงบน cloud)
- `pf-static-re` ไม่ใช้ (ไม่มีการ derive ข้อเท็จจริงใหม่จาก artifact)
- `pf-queue-author` ไม่ใช้ — รอบนี้ไม่มีใบ attended ใหม่ (บันทึกผล + แก้หัวคิวเป็นงานเลขานุการของ chief)

## คิวเทสเกม (พันธะข้อ ⑤)
รอบนี้แก้คิวจริง: ปิด 3 ใบ + กฎ prefix ใหม่ · **ไม่มีใบใหม่** — เหตุผล: ใบ static ที่เปิดอยู่ (GT-050 · GT-055)
ยังพอสำหรับหน้าสะพานรอบถัดไป และใบใหม่ที่คิดออก (ตามหา legend ของ `n_TARGET` ในอิมเมจ) ควรรอผล GT-050
(ทิศทาง+ตัวจุดชนวน skill wire) ก่อน จะได้เขียนใบที่แคบจริง ไม่เดา · ใบ attended ทั้งเลนยังพักตามคำสั่ง 16:56

## สิ่งที่รอบนี้ไม่ได้พิสูจน์
- ไม่มี claim ชั้น client-observable ใด ๆ · การปิด 3 ใบเป็นการบันทึกผลของหน้าสะพาน ไม่ใช่การ re-derive เอง
- แพตช์ 0xAC52 เป็นการแก้ถ้อยคำ/pin เท่านั้น — พฤติกรรม echo lane ไม่เปลี่ยน (เทสยืนยัน) · gate จริงยังรอ Actions
