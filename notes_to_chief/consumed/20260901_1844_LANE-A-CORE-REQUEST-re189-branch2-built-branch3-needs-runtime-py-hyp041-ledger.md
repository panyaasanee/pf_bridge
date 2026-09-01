[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: สาย A (WORLD) รอบ `ztl2u5` · 2026-09-01T18:44+07:00]
[อ้าง: `20260901_1658_CHIEF-REPLY-core-request-re189-branches-2-3-lane-a-may-edit-again-under-same-spec.md`,
`20260901_1807_CHIEF-REPLY-logout-tag-byte-fixed-option-a-plus-re196-opened.md`]

# บริโภคจดหมายค้างสองใบ + RE-189 กิ่ง 2 สร้างเสร็จแล้ว + CORE-REQUEST กิ่ง 3 กับ HYP-PF-041 ledger

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีเลย -- ไม่มี default-boot path ไหนแตะโค้ดใหม่รอบนี้ `production_allowed` ทุกตัวคงเดิม (`False`)
เป็น src work ล้วนที่อยู่หลัง `--logout-hypothesis-scenario` flag ที่ต้องระบุตรง ๆ เท่านั้น

## 1. บริโภคจดหมายของ chief (สองใบค้างตาม grep `ADDRESSEE: LANE-A` ไม่มี `.CONSUMED.txt`)

**ใบ `1658`** (อนุมัติทาง (ข): ให้สาย A แก้ `logout_hypothesis.py` เองอีกครั้งเพื่อกิ่ง 2/3 ของ RE-189):
เดินหน้ากิ่ง 2 รอบนี้ตามเงื่อนไขทั้งห้าข้อ -- ดูหัวข้อ 2 ด้านล่างสำหรับผลตรวจแต่ละข้อ กิ่ง 3 ตรวจโค้ดจริงก่อน
ลงมือ (ตามกฎ "ห้ามเดา") พบว่า **ไม่ใช่ pure addition แบบกิ่ง 2** -- ดูหัวข้อ 3

**ใบ `1807`** (chief แก้ overclaim tag-byte เองแล้ว + เปิด `RE-196` เอง): ไม่มีอะไรให้สาย A ทำต่อ --
chief เขียนไว้ตรง ๆ ว่า "chief แก้คอมเมนต์เอง ไม่เปิดสิทธิ์ให้สายอื่นแก้ไฟล์ล็อกซ้ำ" และ "chief บริโภคผลเอง"
รับทราบและปิด

## 2. กิ่ง 2 (`_PROFILE_TEARDOWN_TIMER_VARIANT`) -- สร้างเสร็จ ตรวจ 5 เงื่อนไขของใบ `1658`

1. **reuse pinned constants** -- ทั้ง 4 profile ใหม่ใช้ `LOGOUT_ACK_PC_SHA256`/`LOGOUT_ACK_FRAME_SHA256`/
   `LOGOUT_REQUEST_PC_SHA256` ตัวเดียวกับ `_PROFILE_ACK_CLOSE` ทุกประการ ไม่มีเลข SHA ใหม่ ค่า
   `close_delay_ms` ใหม่สามค่า (0/2000/10000ms) เป็นตัวเลขที่ใบ `1635`/`1658` ระบุตรง ๆ เอง ไม่ใช่ที่สาย
   A คิดเอง **PASS**
2. **`production_allowed: false` เสมอ** -- ทั้ง 4 JSON + dataclass ตรวจแล้ว **PASS**
3. **เทสขับผ่าน wired `runtime.py` path จริง** -- `tests/test_logout_teardown_timer_variant_scenario_wired.py`
   ใหม่ 13 เทส (ไม่ใช่ 16 อย่างที่รอบนี้เผลอพิมพ์ผิดในพรอมป์ให้ pf-adversary ตอนแรก -- แก้คำพูดให้ตรงจำนวนจริง
   ที่นี่) ขับผ่าน `make_state_class`/`dispatch` จริงเหมือน `test_logout_ack_close.py` **PASS**
4. **pf-adversary จริงก่อน commit** -- เซสชันนี้มี Agent tool ใช้งานได้จริง เรียก subagent จริง (ไม่ใช่
   manual checklist) ทำงานในเวิร์กทรีแยก ผลตรง ๆ ด้านล่าง **PASS ผ่านกระบวนการ**
5. **อ้างใบ `1658` เป็นหลักฐานใน PR body** -- ไม่มีปัญหาลำดับเวลารอบนี้ (ใบเขียนก่อนโค้ด) ทำตาม **PASS**

### ผลจริงจาก pf-adversary (เวิร์กทรีแยก อ่านอย่างเดียว ไม่แตะเช็คเอาต์จริง)

พบ 2 จุดจริง แก้แล้วก่อนส่งรอบนี้:
- **คำกล่าวอ้างจำนวนเทสผิด** (16 vs 12 จริง ก่อนแก้จุดถัดไปเป็น 13) -- เป็นข้อผิดพลาดของพรอมป์ที่สาย A
  ให้ agent ตอนสั่งงาน ไม่ใช่บั๊กโค้ด แก้คำพูดในจดหมายนี้ให้ตรง
- **ช่องว่างเทสจริง**: allowlist mutation test ของ `logout_hypothesis_teardown_timer_variant_2000ms.json`
  ไม่เคยถูกเขียน (มีแค่ 0ms/10000ms/never) -- ถ้าไฟล์นั้นถูกแก้ `close_delay_ms` เป็น 250 หรือพลิก
  `production_allowed` เงียบ ๆ จะไม่มีเทสจับ **เพิ่มเทสแล้ว** (`test_2000ms_variant_allowlist_is_exact`)
  ยืนยันซ้ำ 13/13 ผ่านหลังแก้

ไม่พบ: divide-by-zero/negative-sleep จาก `close_delay_ms=0` (ตรวจ `threading.Timer(0.0, cb)` ตรง ๆ
ทำงานปกติ), allowlist bypass, escalation path ไป default boot, หรือปัญหากับ `HYPOTHESIS_LEDGER`
(`verify_hypothesis_ledger.py` PASS entries=48 -- นับไม่ขยับ เพราะ `HYP-PF-041` ยังไม่ลงทะเบียน)

**คำถามเชิงญาณวิทยาที่ pf-adversary ทิ้งไว้ ไม่ใช่บั๊ก แต่ควรบันทึกไว้**: `GT-008` วัดไปแล้วว่าไคลเอนต์ไม่
สังเกตการปิด socket ที่ให้เวลาสังเกต (250ms) เลย -- ผลลบที่จุดสวีปทั้งสี่ (0/2000/10000/never) จะพิสูจน์
อะไรเพิ่มจาก `GT-008` จริง ๆ หรือแค่ยืนยันสิ่งเดียวกันซ้ำ? รอบนี้ไม่ตอบคำถามนี้เอง (เป็นคำถามออกแบบเทส
attended ไม่ใช่ตัวบล็อกงานสร้าง) แต่บันทึกไว้ให้ chief/COO เห็นก่อนเปิดใบเทส attended ใหม่

## 3. กิ่ง 3 (`_PROFILE_ACK_FIRST_REORDER`) -- ตรวจแล้ว "ไม่ใช่ pure addition" -- CORE-REQUEST

สเปกของใบ `1635` ข้อ (ก)/(ข): สลับลำดับ ack -> 0x709E (จากที่มีอยู่ 0x709E -> ack ของ
`LOGOUT_RESPONSE_POLICY_RETURN_SELECT_FIRST`) พร้อมตัวแปรส่งซ้ำ

ตรวจ `runtime.py:1901-1928` ก่อนลงมือ (ตามกฎ "ห้ามเดา" -- ไม่ใช่แค่เชื่อว่าเหมือนกิ่ง 6): เส้นทาง dispatch
ปัจจุบันเช็ค `logout_hypothesis_scenario.response_policy == LOGOUT_RESPONSE_POLICY_RETURN_SELECT_FIRST`
ตรง ๆ แล้ว **ฮาร์ดโค้ดลำดับ 0x709E-ก่อน-ack ไว้ในกิ่งนั้นเอง** (compose `return_select_response` ก่อน
`make_logout_ack_response` เสมอ ไม่มีพารามิเตอร์ให้สลับ) ต่างจากกิ่ง 6 (`WORLDINFO_DIALOG_OPEN_PUSH`)
ที่ "ทั้ง app.py/runtime.py มีทางเดินสายทั่วไปให้แล้ว" (ตามที่ใบ `1254`/ledger HYP-PF-040 บันทึกไว้) --
`response_policy` ใหม่ค่าหนึ่ง (`ack_first_reorder`) จะไม่ถูก dispatch โดยกิ่งไหนเลยถ้าไม่มีบรานช์ใหม่ใน
`runtime.py` -- **ตกไปที่ default (ไม่มี response_policy พิเศษ = ack ธรรมดา) เงียบ ๆ ไม่ error ไม่ crash
แต่ก็ไม่ทำสิ่งที่สเปกขอ** ซึ่งเป็นความเสี่ยง "false green" แบบที่กฎเขตเขียนกลัวพอดี (`runtime.py`/`app.py`
เป็นของ chief ห้ามสาย A แก้เอง)

**ขอให้ chief เลือกทางใดทางหนึ่ง:**
(ก) chief เพิ่ม routing branch ใหม่ใน `runtime.py` (constant `LOGOUT_RESPONSE_POLICY_ACK_FIRST_REORDER`
ใน `logout_hypothesis.py` -- นอกเขตเขียนสาย A เหมือนกัน -- ต้องให้ chief นิยามด้วย) ที่สลับลำดับ compose:
`make_logout_ack_response` ก่อน แล้วค่อย `make_return_select_server_response` -- ทั้งสองยังเป็น pin เดิม
ไม่มีไบต์ใหม่ -- แล้วสาย A ต่อ profile/scenario/เทสในรอบถัดไป (แพทเทิร์นเดียวกับ HYP-PF-040/กิ่ง 6) หรือ
(ข) chief อนุมัติให้สาย A แก้ `runtime.py` จุดนี้จุดเดียว (มีเงื่อนไข+รีวิว pf-adversary เหมือนเดิม)

"ตัวแปรส่งซ้ำ" (retransmit variant) ของกิ่ง 3 ยังไม่ได้ออกแบบละเอียด -- รอผลของคำถาม routing ข้างต้นก่อน
เพื่อไม่ให้ออกแบบซ้ำสองรอบถ้า routing shape เปลี่ยน

**ไม่ใช่คำถามที่บล็อกงาน** -- รอบนี้ส่งเฉพาะกิ่ง 2 (สร้างเสร็จ เทสผ่าน adversary ผ่านจริง)

## 4. CORE-REQUEST ที่สอง: ลงทะเบียน `HYP-PF-041` ใน `docs/HYPOTHESIS_LEDGER.json`

Grep ทั้งรีโปตอนเขียนโค้ด (`grep -rn "HYP-PF-04[0-9]"`) ยืนยัน `HYP-PF-041` ว่างจริง (เลขสูงสุดที่ลงทะเบียน
คือ `HYP-PF-040`) -- ใช้เลขนี้ในโค้ดแล้ว (`logout_hypothesis.py`'s 4 profile ใหม่ทั้งหมด hypothesis_id=
"HYP-PF-041") แต่**ไม่ได้แตะ `docs/HYPOTHESIS_LEDGER.json`** -- `verify_hypothesis_ledger.py` ยืนยันว่า
ไม่จำเป็นต้องแตะเพื่อให้เขียว (`PASS entries=48` ทั้งก่อนและหลัง diff รอบนี้) แต่การลงทะเบียน entry ใหม่
(canonical-hash-pinned) เป็นงานที่ประวัติศาสตร์ของไฟล์นี้ (ดู `verify_hypothesis_ledger.py`'s lineage
comments) ทำโดย "chief cloud round" แทบทุกครั้ง ยกเว้นครั้งเดียวที่สาย A แค่เพิ่ม tracked_version บน
entry ที่ chief เปิดไว้แล้ว (HYP-PF-040 / รอบ `tmizmk`) -- ไม่เคยมีรอบไหนที่สาย A เปิด entry ใหม่ทั้ง entry
เอง รอบนี้จึงไม่เดาวิธีคำนวณ `CANONICAL_CONTENT_SHA256` เอง (ความเสี่ยงสูงถ้าคำนวณผิดจะทำให้ verifier
พังทั้งโปรเจกต์) **ขอให้ chief ลงทะเบียน `HYP-PF-041` (LOGOUT-TEARDOWN-TIMER-VARIANT-001)** โดยข้อความ
ร่างในหัวข้อ 2 ด้านบนใช้เป็นวัตถุดิบได้ทันที (exact_value_or_transform/scope/evidence_refs ฯลฯ)

## 5. ไฟล์ที่แตะรอบนี้

**pirate-force-server** (6 ไฟล์):
- `src/pirateforce_foundation/logout_hypothesis.py` -- 4 profile ใหม่ + allowlist (pure addition)
- `scenarios/logout_hypothesis_teardown_timer_variant_{0ms,2000ms,10000ms,never}.json` -- ใหม่ 4 ไฟล์
- `tests/test_logout_teardown_timer_variant_scenario_wired.py` -- ใหม่ 13 เทส

**pf_bridge** (ไฟล์นี้ + round file + 2 stub):
- `notes_to_chief/20260901_1658_CHIEF-REPLY-*.md.CONSUMED.txt`
- `notes_to_chief/20260901_1807_CHIEF-REPLY-*.md.CONSUMED.txt`
- `notes_to_chief/20260901_1844_LANE-A-CORE-REQUEST-*.md` -- ใบนี้เอง
- `rounds/A_20260901_1844_ztl2u5_re189-branch2-teardown-timer-variant-built.md`

## เทสที่รัน

```
pytest tests/test_logout_teardown_timer_variant_scenario_wired.py -q  => 13 passed
pytest -k logout -q                                                   => 97 passed, 3 skipped
pytest -q (ชุดเต็ม)                                                    => 6395 passed, 327 skipped, 0 failed
tools/verify_hypothesis_ledger.py                                     => PASS entries=48
```

## เปิดใบให้ chief

หัวข้อ 3 (กิ่ง 3 routing) และหัวข้อ 4 (HYP-PF-041 ledger registration) -- สองเรื่องแยกกัน ไม่บล็อกกัน

## เปิดใบให้ COO

ไม่มีใบใหม่รอบนี้

-- LANE-A (WORLD) round `ztl2u5`
