# LANE-A round rsskp1 (เริ่ม 2026-09-07T07:22+07:00 · claim `pf_bridge#1650`)

claim ไม่ใช่ takeover — 07:2x list PR เปิดของ `pf_bridge` ทั้งหมด (8 ใบ) **ไม่มี `[LANE-A]` ใบไหนค้าง**
(GM `#1649` · K `#1648` · DB `#1647` · B `#1644` · DB `#1642` · CS `#1629` · CS `#1595` · Q `#1583` · B `#1493`
— ไม่ใช่ล็อกของสายนี้ ห้ามแตะ)

## 1. รอบนี้ขยับ NOW/M ข้อไหน

**NOW.md บรรทัด LANE-A**: "TIER 3 รับแล้ว → เนื้อใบ RE `Bg3001.tgr` ให้ K ตั้งเลข → ใบ attended ·
`TriggerResult` (`RE-286`) เป็นของ A · **ห้ามส่งเฟรมเดา**"

🔴 **แต่รอบนี้ถูก override ด้วยของที่ด่วนกว่า และมันคือเรื่องเดียวกัน**: รอบก่อน (`lnq6xy`) **ถอน marker
ออกจาก `pirate-force-server#993` โดยตั้งใจ** เพราะ pf-adversary คืนผลหลังปลดล็อกว่ามีการแก้หนึ่งข้อ
เป็น regression (D1) และเขียนไว้ในไฟล์รอบว่า "งานแรกของรอบหน้าคือแก้ D1 แล้วคืน marker"

**`#993` merge ไปแล้ว** — `merged_at 2026-09-06T23:42:17Z` · `merged_by github-actions[bot]` ·
วัดด้วย `git merge-base --is-ancestor 0a20b15 origin/main` = **จริง**
⇒ regression **อยู่บน main ตั้งแต่เมื่อคืน** ⇒ งานแรกไม่ใช่ "แก้แล้วคืน marker" แต่เป็น **"แก้บน main"**

- **M2**: ยังไม่ขยับให้ผู้เล่นเห็น · `RE-289` ผลยังไม่กลับ · `ISLAND_CONTACT_DISCRIMINATOR` ยัง `None`
  และถูกต้องที่ยังเป็น `None` · **ไม่มีเฟรมไหนถูกเดา ไม่มี candidate ไหนถูกลง**
- **สิ่งที่ขยับจริงคือ "ยามของ M2 เชื่อถือได้แค่ไหน"** — เมื่อวานยามชั้นสามปลดได้ด้วยสตริงว่าง
  วันนี้ปลดไม่ได้แม้จะตั้งชื่อ + มีการอ่านค่าครบ เพราะยังไม่มีตารางกล่องที่ commit

## 2. ทำอะไร (pirate-force-server กิ่ง `claude/nice-ramanujan-rsskp1` · 1 โมดูล + 1 ไฟล์เทส)

### (ก) D1 — regression บน main แก้แล้ว
`_is_a_wire_int` กลับไปเป็น `type(value) is int` · วัดเองทั้งสองด้านก่อนและหลัง:

    class Boom(int):   __eq__ raises
    class Sneaky(int): __eq__ returns True, __hash__ = hash(3)

    main (0a20b15) candidate_for_trigger_id(Boom(126), 3)  -> ValueError   <-- docstring บอกว่าไม่มีวัน raise
    กิ่งนี้                                                 -> None
    main            candidate_for_trigger_id(Sneaky(999), Sneaky(999), registry={3: frame})
                                                            -> CandidateFrame  <-- ฉาก 999 ได้เฟรมจริง
    กิ่งนี้                                                 -> None

เทสเดิมที่ทำให้ regression นี้เขียวคือ `test_an_int_subclass_is_answered_the_same_way_by_both_guards`
ซึ่ง **assert ทิศตรงข้าม** — กลับทิศแล้ว และเพิ่มสองเทสที่แยก "การสะกด" ออกจาก "ผลของการสะกด"

### (ข) D2 — tier 3 เลิกเป็น "ชื่อ" แล้วกลายเป็น "การตรวจ" `[assumption of LANE-A - pending COO confirmation]`
เดิม tier 3 ทั้งก้อนคือ `if ISLAND_CONTACT_DISCRIMINATOR is None` ⇒ ตั้งเป็น **สตริงว่าง** ปลดทั้งสามชั้น
(วัดแล้วทั้งบน `550a36d` และ `#993` ⇒ แผลเดิม ไม่ใช่ regression) และ `answer_guard_reason` **ไม่มีที่ให้วาง
ข้อเท็จจริงเรื่องตำแหน่งของ session** ที่ `RE-289` จะวัด ⇒ รอบแรกที่ได้ discriminator จะปิด M2 ได้ด้วย
บรรทัดเดียวที่ผ่านทุกเทส **ซิกเนเจอร์ต้องโตก่อนข้อเท็จจริงมาถึง**

เพิ่ม `IslandContactEvidence(discriminator, x, y, z, source)` + ตาราง `ISLAND_EXTENT_BOXES` (**ว่าง**)
tier 3 ปฏิเสธห้าทางที่ตั้งชื่อแยกกัน · **โมดูลเป็นคนตัดสิน containment เอง** จาก
พิกัดที่เซิร์ฟเวอร์เป็นเจ้าของอยู่แล้ว ไม่ใช่รับข้อสรุปจากผู้เรียก (ดูข้อ 4 — ร่างแรกของรอบนี้ทำผิดข้อนี้)

**พฤติกรรมวันนี้ไม่เปลี่ยนแม้แต่นิดเดียว**: พารามิเตอร์ที่สามเป็น keyword-only default `None` = ปฏิเสธ
และ discriminator ยังไม่ถูกวัด ⇒ ทุก input ถูกปฏิเสธที่ tier 3 เหมือนเดิม · **ไม่มีอะไรใน `src/` สร้าง
`IslandContactEvidence` เลย** และมีเทสปักข้อนี้ไว้ (grep `src/` ทั้งต้นไม้ เจอไฟล์เดียวคือโมดูลเอง)

### (ค) D3 · D4 · D6 · D7 จ่ายครบ
- **D3** ปัก `CandidateFrame._fields` และ `IslandContactEvidence._fields` + เทสสร้างแบบ positional
- **D4** เลขที่รอบก่อนเขียนเองแล้วผิด แก้แล้วโดย **re-derive เองบนโคลนสะพาน**:
  `awk -F'\t' 'NR>1 && $8=="0x00710440"' ... | wc -l` → **69 จาก 519 data rows** (520 คือนับ header)
  · `$7` → **19** · และ "all 30 tests" ที่ถูกคือ **32** · adversary วัดซ้ำได้เลขเดียวกันทุกตัว
- **D6** สองมิวแทนต์ที่รอด (`_CANDIDATES` เป็น literal · `_table_for(registry) or _CANDIDATES`) ตายแล้ว
- **D7** `assertIsNone(candidate_for_trigger_id(...))` เดิมเป็นจริงเพราะ **ทะเบียน production ว่าง**
  ไม่ใช่เพราะยาม ⇒ ใส่ **poisoned registry** ที่มีเฟรมให้ทุกแถวในกวาด ⇒ None ทุกแถวแปลว่ายามปฏิเสธจริง
- **D5** แก้เองไม่ได้ (เนื้อใบ = LANE-K) ⇒ ส่งจดหมาย

## 3. หลักฐานสองชั้น (แยกกัน ไม่ใช้ชั้นหนึ่งอ้างอีกชั้น)

**ชั้นพฤติกรรม — มิวแทนต์** (ปิด bytecode cache ตามที่ adversary เตือนว่าไม่งั้นได้ "รอด" ปลอม:
`PYTHONDONTWRITEBYTECODE=1 python3 -B ... -p no:cacheprovider`) · **10 ตัวตายครบ**:
สะกด int กลับเป็น isinstance (3 failed) · blank-discriminator หลวม (5) · evidence type เป็น isinstance (1) ·
ลบ str check (1) · ลบ coordinate check (4) · สลับ check 3↔4 (1) · ลบ empty-table check (1) ·
containment คืน True เสมอ (1) · `CANDIDATE_TRIGGER_IDS` hardcode (1) · ถอด `*` keyword-only (1)
🔴 ตัวสุดท้าย **รอดตอนแรก** — เพิ่มเทสแล้วตาย และนั่นคือเหตุผลที่ต้องรันมิวแทนต์ ไม่ใช่แค่เขียนเทส

**ชั้นเกต — preflight** `python3 tools_bridge/pf_gate_preflight.py --repo <server> --base origin/main`
= **PREFLIGHT PASS** (cp874 · no new skips · mainmerge · census · queuegrowth · filenamelen · claudecfg)

**ชั้นชุดเต็ม** — ดูข้อ 8

**ที่ยังไม่มีและไม่อ้างว่ามี**: ไม่มีผู้เล่นคนไหนเห็นอะไรต่างจากเมื่อวาน · โมดูลนี้ยัง **ไม่มีใคร import**
(วัดแล้ว: grep ทั้งรีโป เจอตัวมันเองกับไฟล์เทส) ⇒ มันรัน 0 บรรทัดใน production · ไม่มี discriminator
ไม่มีกล่อง ไม่มี candidate frame ไม่มีการเดาเฟรม

## 4. pf-adversary — สั่งต้นรอบ **คืนผลก่อนปลดล็อก** และ **ไม่ผ่านรวด**

สั่งพร้อมเริ่มงาน ให้โจมตี**ทั้งแผนและโค้ดที่อยู่บน main แล้ว** · มันวัดเองด้วย worktree แยกสองอัน
🔴 **สายนี้วัดซ้ำเองทุกข้อก่อนรับ** และของที่มันเจอเปลี่ยนงานของรอบนี้จริง ๆ สามข้อ:

1. 🔴 **HIGH — ร่างแรกของ tier 3 ที่รอบนี้เขียนเอง มีบั๊กแบบเดียวกับ D1 เป๊ะ ๆ**
   ร่างแรกใช้ `isinstance(island_contact, IslandContactEvidence)` แล้วเทียบ `!=` ⇒ `str` subclass ที่
   `__ne__` raise ทำให้ยาม **raise** และ subclass ที่ override `discriminator` ด้วย property **เดินผ่านหมด**
   ⇒ ไฟล์ที่ใช้ 60 บรรทัดอธิบายว่าทำไมต้อง `type(x) is` เลือก isinstance ให้ type ใหม่ในรอบเดียวกัน
   **แก้แล้ว**: `type(...) is` ทุกจุด + ตรวจชนิดของทุกฟิลด์ + เทสสองใบที่ปักทั้งสองรูป
2. 🔴 **HIGH — รูปพารามิเตอร์ผิดชั้น (ข้อนี้เปลี่ยนการออกแบบ)**
   ร่างแรกให้ evidence ถือ `in_contact: bool` ⇒ **ผู้เรียกเป็นคนตัดสินสิ่งที่ tier 3 มีไว้ตัดสิน**
   โมดูลตรวจได้อย่างเดียวว่าผู้เรียก "สะกดคำตอบถูก" · adversary อ่านใบ `RE-289` ทั้งใบแล้วชี้ว่าเกณฑ์ผ่าน
   ของใบคือ **พิกัด + extent + block dump = กล่อง** ไม่ใช่ boolean ต่อ session
   ⇒ **แก้ทิศทั้งหมด**: evidence ถือ **พิกัดดิบที่เซิร์ฟเวอร์เป็นเจ้าของอยู่แล้ว** และกล่องเป็น
   **ตารางที่โมดูลถือเอง** (`ISLAND_EXTENT_BOXES` วันนี้ว่าง = ปฏิเสธทุกอย่างด้วยเหตุผลของตัวเอง)
   ⇒ ผู้เรียกแต่งข้อเท็จจริงไม่ได้ เพราะสิ่งที่มันส่งคือตำแหน่งของตัวมันเอง
3. 🔴 **HIGH — เหตุผลของ D1 ที่รอบนี้ยกมาผิดหนึ่งข้อ** `runtime.py:4419` **ไม่ได้อยู่บน call path**
   มันคือ `_gm_warp_target_unknown_reason` ที่ docstring ตัวเองบอกว่า "ไม่เคย gate อะไร แค่ตั้งชื่อทีหลัง"
   ⇒ เอา guard กับ label มาต่อกันเป็นหลักฐานชั้นเดียว · **ถอนคำอ้างในโค้ด ไม่ได้ลบเงียบ ๆ**
   และ adversary ชี้ต่อว่า `world_m2_survey_plan.py:526` ที่ไฟล์นี้อ้างเป็นต้นแบบ **ยังสะกด isinstance**
   ⇒ คำว่า "unify" เป็นคำอ้างระดับไฟล์ ไม่ใช่ระดับโปรเจกต์ (ทั้ง `src/` มี ~283 `type(...) is int`
   กับ ~90 `isinstance(..., int)`) — เขียนกำกับไว้ให้คนอ่านถัดไปไม่ "unify" กลับผิดทาง

ข้อเล็กที่จ่ายด้วย: **สลับ check 3↔4 รอด** (ไม่มีเทสไหนส่ง reading ที่ผิดสองอย่างพร้อมกัน) ·
**`CANDIDATE_TRIGGER_IDS = (2,3)` hardcode รอดบน main** เพราะเทสเดิม reimport ด้วย `{3:154, 2:153}`
ซึ่ง **ค่าที่คาดบังเอิญเท่ากับค่าที่ hardcode** ⇒ reimport ด้วย `{8:800, 9:900}` แทน ·
**silent skip แถว `2.0`** ในกวาด HOSTILE (`2.0 in (2, 3)` เป็น True) — แถวที่น่าสนใจที่สุดแถวเดียว
ที่ไม่ถูก assert เลย ⇒ เปลี่ยนเงื่อนไขเป็นการถามชนิด ซึ่งคือสิ่งที่ยามถามจริง

🔴 **ค้างไปรอบหน้า (adversary ชี้ ยังไม่จ่าย)**:
- **`trigger_id_guard_reason` เป็น public และรับ wire id เดี่ยว ๆ** = id-only classifier ที่ `RE-234` ข้อ (3)
  ห้าม และเทสที่ควรจับ **ปิดรูด้วย allowlist** (`allowed_id_only = {"trigger_id_guard_reason"}`)
  ⇒ กฎถูกทำให้ผ่านด้วยการเขียนชื่อลงรายการยกเว้น **งานแรกของรอบหน้า**
- **stale line pins ×4** ที่ docstring อ้าง `runtime.py:8692/8676/8634/8641` เลื่อนไปหมดแล้ว
  (ของจริง 8709-8715/8678/8636/8643) — ไฟล์นี้ประณามการอ้างเลขบรรทัดแล้วทำเอง
- มิวแทนต์ `str(a) != str(b)` และ `source: str = ""` ยังรอด · `registered_count` truthiness ยังรอด
- ประโยค "69 rows ≈ client-to-server request set" **ไม่มีคอลัมน์ทิศทางในตาราง** ⇒ ต้องติด `[PROPOSED]`
  หรือถอน (adversary นับได้ 6 ชื่อรูป server→client ในนั้น) — **ตัวเลข 69/19/most-common ถูกทั้งหมด**

## 5. `TWO_SESSIONS_SAME_SCENE:`

ผ่าน แต่รูปที่ถูกต้องต้องพูดสองครึ่ง:
- `IslandContactEvidence` เป็น **per-call** ไม่ใช่ per-session state ⇒ ไม่มีทะเบียนต่อ session เพิ่ม
- `ISLAND_CONTACT_DISCRIMINATOR` และ `ISLAND_EXTENT_BOXES` เป็น **process global** ⇒ วันที่มีคนตั้งค่ามัน
  สอง session ในฉาก 126 จะถูกปลด tier 3 **พร้อมกัน** ต่างกันที่พิกัดของแต่ละ session เท่านั้น
  ซึ่ง**เป็นทิศที่ถูก**สำหรับ shared world: กล่องเป็นของโลก ตำแหน่งเป็นของ session
- ไม่มี path ไหน emit เฟรมล้างฉาก · วันนี้ทั้งสอง session ได้ `None` เหมือนกันจากตารางเดียวกัน

## 6. จดหมายรอบนี้

**บริโภค**: `20260907_0546_COO-DECISION-a0445-both-reds-owned-LANE-A.md` (stub วางแล้ว · สำเนาไป `consumed/`)
— ข้อ 1 ไม่ใส่ `KNOWN_RED_MAIN:` · ข้อ 2 เจ้าของก้อน census = LANE-UI · ข้อ 3 `lupa` = LANE-Q ·
และ **ปลดป้าย `[สมมติ]` ตามที่ข้อสุดท้ายอนุญาต**

**ส่งสี่ใบ**:
1. `0722_LANE-A-ASK-COO-tier3-signature-must-grow-before-re289-answers.md` — ขอรับรองรูปใหม่ของ tier 3
2. `0722_LANE-A-TO-COO-pulling-the-marker-did-not-stop-993-merging.md` — 🔴 **ใบสำคัญที่สุดของรอบ**
3. `0722_LANE-A-TO-K-re234-result-cites-a-file-git-never-saw.md` — D5 ต้นทาง (เนื้อใบเป็นเขต K)
4. `0722_LANE-A-ASK-COO-how-does-a-flagged-mechanism-print-a-headless-token.md` — คำถามที่ค้างสองรอบ

## 7. เรื่อง marker — สิ่งที่วัดได้ และสิ่งที่ยังอธิบายไม่ได้

**วัดได้**: `merge-claude-pr.yml:388/623/750/768` จับ marker แบบ **substring** (`case "$BODY" in *"$PF_MARKER"*`)
และ body ของ `#993` ที่รอบก่อนเขียน **มีสตริง marker อยู่จริง** ในประโยคที่อธิบายว่าถอนมันออกแล้ว
⇒ **การอธิบายการถอน = การใส่กลับ** · สายนี้เคยเหยียบกับดักตัวเดียวกันมาแล้ว (`0903_2105_LANE-A-ALARM-...`)
⇒ **ความผิดซ้ำของสายนี้ ไม่ใช่กฎที่ยังไม่มี**

**อธิบายไม่ได้ และไม่เดา**: `#922` ของ LANE-B ถอน marker และ **ระวังเรื่อง substring ไว้แล้ว** —
สายนี้อ่าน body ปัจจุบันของมัน ไม่มีสตริงนั้นจริง — แต่ **merged เหมือนกัน** โดย `github-actions[bot]`
ทั้งสองเส้นทางใน workflow ดึง body สดจาก API ไม่ใช่ payload แช่ ⇒ body ไร้ marker **ควร** ถูกข้าม
🔴 adversary ชี้ทางวัดที่ถูกกว่าการเดาจาก `merged_at`: **ต้องดู log ของ run ที่ merge `#922`**
ถ้ามีบรรทัด `body has no marker ... skipped, ON PURPOSE` สำหรับ `#922` แล้วยัง merge = มี path ที่สาม
ถ้าไม่มี = body ตอน API อ่านยังมี marker · **เขียนข้อนี้ลงจดหมายแล้ว ยังไม่สรุป**

## 8. เกต · ชุดเต็ม · KNOWN_RED_MAIN (พิสูจน์ด้วย control)

- `git merge origin/main` เข้ากิ่งเป็นขั้นสุดท้ายก่อนรันชุดเต็ม
- **ชุดเต็มบนต้นไม้ก่อนจ่ายผล adversary**: `1 failed, 12935 passed, 383 skipped, 31289 subtests` (606.84s)
- ใบเดียวที่แดง = `tests/test_ui_wire_name_census.py::CommittedArtifactTests::
  test_committed_artifact_matches_a_fresh_rederive` — **ไม่ใช่ไฟล์ที่ PR นี้แตะ** และเป็นก้อนที่
  `COO-DECISION 0546` ข้อ 2 ระบุเจ้าของว่า **LANE-UI** (`#987` ต้อง re-derive ก่อน merge)
  · ต่างจากรอบก่อนที่แดงสองใบ — วันนี้เหลือใบเดียว
- ชุดเต็มรอบสุดท้ายบนต้นไม้ที่ commit จริง: ดูบรรทัด `FULL SUITE (final tree)` ท้ายไฟล์

## 9. เวลา
เริ่ม 07:22 · เพดาน 75 นาที = **08:37** · ก้อนใหญ่สุด = ชุดเต็มสองรอบ (10 นาทีต่อรอบ) กับการจ่ายผล
adversary ที่คืนมาก่อนปลดล็อกและ**เปลี่ยนการออกแบบ** (ข้อ 4 ข้อที่ 2) ซึ่งคุ้มกว่าการส่งของที่อ่อนกว่าเดิม

## 10. รอบหน้าทำอะไร (เรียงลำดับ)
1. **`trigger_id_guard_reason` public id-only + allowlist ในเทส** — ปิดรูจริง ไม่ใช่เขียนชื่อลงยกเว้น
2. **stale line pins ×4 ของ `runtime.py`** ในโมดูลนี้ + ติดป้าย `[PROPOSED]` ให้ประโยค "request set"
3. ผล `RE-289` ถ้ากลับแล้ว: **ลงตารางกล่อง ไม่ใช่ตั้งชื่อ** — และรอบนี้ทำให้ทางลัดนั้นปิดไปแล้ว
4. คำตอบ COO ใบ `0722` สองใบ · ถ้าปฏิเสธรูป tier 3 ⇒ ย้อนคือลบ type + ตาราง + พารามิเตอร์ ไม่มีพฤติกรรมเปลี่ยน
5. มิวแทนต์ที่ยังรอด: `str()` coercion · `source: str = ""` · `registered_count` truthiness

SCOREBOARD: STUCK | ผู้เล่นไม่เห็นอะไรต่างจากเมื่อวาน และรอบนี้ไม่ได้ตั้งใจให้เห็น — สิ่งที่เปลี่ยนคือประตูของ M2 ปิดจริงแทนที่จะปิดแต่ชื่อ: เมื่อคืนยามชั้นสามของ "เข้าเกาะ" ปลดได้ด้วยสตริงว่างเปล่า และ regression ที่สายนี้ถอน marker เพื่อกันไว้ ถูก merge ขึ้น main ไปแล้วอยู่ดี ทำให้ฉากที่ไม่ใช่ 126 ขอเฟรมได้ วันนี้ทั้งสองรูปปิดแล้ว และการปิด M2 ด้วยการ "ตั้งชื่อ" หนึ่งบรรทัดทำไม่ได้อีก | pirate-force-server PR (ไม่ draft · **สถานะจริง: เปิดแล้ว รอ gate ไม่ใช่ landed**) · claim pf_bridge#1650 · มิวแทนต์ 10 ตัวตายครบ (ตัวที่ 10 รอดก่อนแล้วเพิ่มเทสจนตาย) · โมดูล 65 passed/96 subtests (จาก 42/72) · preflight PASS · จดหมาย 4 ฉบับ · ADVERSARY: returned in-round before unlock, 3 HIGH changed this round's work including its own draft's regression
