# R144 (ycp7vk) — GT-047 จ็อบ 0 ปิด: การ์ด `field_offset` ส่งกลับเป็น patch · ปิด GT-049 PASS · ปิด RE-057/RE-058 · บริโภคจดหมาย 5 ใบ

- เวลา: 2026-08-24 ~09:4x–10:4xZ UTC (~16:4x–17:4x +07:00)
- session: ycp7vk · branch เอกสาร `claude/exciting-goldberg-ycp7vk` · branch โค้ด `claude/amazing-goodall-ycp7vk` (ไม่ได้ใช้ — รอบนี้ไม่แตะ repo โค้ด)
- ล็อก: draft PR #45 (`pf_bridge`) เปิดเป็น draft ตั้งแต่วินาทีแรกตาม v5 ข้อ ① — ล็อกไม่หลุด

## probe ต้นรอบ

1. GitHub API/tool: ✅ อ่านรายการ PR ได้ทั้งสอง repo (ว่างทั้งคู่) · เปิด draft PR ได้ (#45)
2. ทาง D `ci-status`: ✅ มีชีวิตบน `pirate-force-server` — อ่านคำตัดสินของ `fa1e804` (head PR #16) ได้จริง: `conclusion: success` (run 32682451014)
3. โครงพี่น้อง: ✅ `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` อยู่จริง

## สถานะ PR โค้ด #16 (ค้างจาก R143)

- head `fa1e804` เขียว(Actions run 32682451014 · subset · อ่านทาง D ci-status) · merge เข้า `main` แล้ว (`94f0ce3`)
- re-derive บน main clone: สวีตเต็ม **2019 passed / 324 skipped / 0 failed เขียว(cloud sanity)** — parser `opaque_string8` ของ GT-055 อยู่บน main จริง
- ⚠️ บันทึกสภาพแวดล้อม: local branch `main` ของ clone ฝั่ง cloud รอบนี้**ค้างอยู่ที่ commit ยุค R105** (`7f893b8`) ทั้งที่ `origin/main` คือ `94f0ce3` — ต้อง `git merge --ff-only origin/main` ก่อนใช้ (เป็น ancestor จริง ff ได้สะอาด) · ถ้ารอบไหนรันเทสบน "main" แล้วเลขเพี้ยนหนัก (~197 failed) ให้สงสัยข้อนี้ก่อน

## จดหมายเข้า 5 ใบ (บริโภคครบ สำเนา+stub แล้ว)

| ใบ | สรุป | สิ่งที่รอบนี้ทำ |
|---|---|---|
| 0901 RE-057 PREWORK | literal `PlacementOFF` ของ Bg3001/Bg3002 เกินขอบทั้ง placement และ definition ทั้งสองการนับ | ถูก supersede โดยผล 09:30 ในทางที่แรงกว่า — จดเป็นบริบทของใบ |
| 0914 RE-058 RESULT | bounded negative: ไม่พบ exact outbound chain ของ `CLearnSkillVital 0x36AA` · handler = `return true` stub · ยัง exclude indirect path ไม่ได้ · pin correction: vtable จริง `0x00F48E94` | ปิดใบ DONE/BOUNDED-NEGATIVE ใน `CLIENT_RE_QUEUE.md` · direction ยังไม่ตัดสิน ⇒ nonclaim ของ decoder R140 คงเดิม — ไม่แตะโค้ด |
| 0916 GT-047 job 0 | source `pf_validate_capture_fields.py` ทั้งไฟล์ (1,243 บรรทัด · sha256 `0166337C…B793D8C8`) | **งานหลักของรอบ — ดูหัวข้อถัดไป** |
| 0923 GT-049 RESULT | id 131 ยิงจาก inbound `ItemOperateVitalRes` (`0x005EF5E0` → `0x005CC309`) — คนละเลนกับ GT-046 | ปิดใบ PASS/DONE ใน `GAME_TEST_QUEUE.md` · ผลเชิงดีไซน์: บรรทัดลูทสีเขียว = เซิร์ฟเวอร์ตัดสินการเก็บ ⇒ เลนลูทฝั่งเราต้องส่ง `ItemOperateVitalRes` เอง (จดเป็นคำถามค้าง/แถวงานให้ Panya เคาะ ไม่เปิด hypothesis เองเพราะเป็นดีไซน์เลนใหม่) |
| 0930 RE-057 RESULT | `Scene.PlacementOFF/ON/Cancel` ทั้งสาม bind delegate no-op `0x0045FA00` (`xor eax,eax; ret 4`) — ไม่อ่าน argument · ด่านตัวควบคุมผ่าน | ปิดใบ DONE/STATIC-LANE-CLOSED · ยืนยันคำตัดสิน R136–R137: ห้ามผูก band `0x2000+N+1` กับ literal สคริปต์ — ไม่มีโค้ดต้องแก้ (ไม่เคย wire) |

## งานหลัก — GT-047 จ็อบ 0: การ์ด `field_offset` (patch ส่งกลับ)

**root cause ที่วัดได้:** validator เดิมอ่าน `field_offset` แค่จุดเดียว (`"UNKNOWN(" in row["field_offset"]` เพื่อ mark static-open) — ตัว parser เดินด้วย tag+len ล้วน ⇒ mutation `TargetPosVital:W:1 +0x14→+0x99` จึงเขียวเงียบ (ตรงตามที่ tester วัด 2026-08-23 14:21)

**อินเวเรียนต์ที่การ์ดยึด (วัดบนตารางจริง `external/PF_SERIALIZER_FIELDS.tsv` 6,931 แถวบน cloud):**
- message ที่ closed (ไม่ static-open) 338 ใบ → 859 คู่ (message, order) มีทั้งขา W และ R เสมอ · order set W = R ทุกใบ
- ทุกคู่: `field_offset`/`tag`/`span_start`/`span_end` mirror **byte-for-byte** ยกเว้น **40 คู่** (8 messages) ที่ legs ฝัง VA คนละตัวโดยชอบ (subcall W/R คนละฟังก์ชัน) — 40 คู่นั้น pin เป็น frozenset ในโค้ด แล้ว mirror หลัง normalize VA (`0x[0-9A-Fa-f]{6,8}` → `VA`)
- `len` และ `span_sha256` mirror raw ครบ 859/859
- pin census: static-open = 181 · closed pairs = 859 (ตามปรัชญา `EXPECTED_*` ที่ไฟล์เดิมใช้อยู่แล้ว) — กัน mutation หนีเข้า skip set

**สิ่งที่ส่ง (อยู่ใน `patches/gt047/` — เปิด allowlist `.gitignore` ให้แล้ว):**
1. `pf_validate_capture_fields.py` ฉบับแพตช์ — เพิ่ม `validate_field_offset_mirror()` เรียกท้าย `build_schemas()` + self-test 6 เคสใหม่ใน `validate_schema_mutation_regressions()` + pin membership digest
2. `verify_gt047_guard_patch.py` — ตัวรัน 8 ด่าน (echo sha256 ของ validator ที่โหลดจริงเป็นบรรทัดแรก เพื่อผูกผล rerun กับไฟล์จริง)
3. `README_GT047_PATCH.md` — วิธี apply + sha pin

**ผลรันบน cloud (เขียว(cloud sanity) — ชั้น schema เท่านั้น ไม่มี capture ที่นี่):** `ALL 8 CHECKS PASS`
— pristine ผ่าน (519 messages / 181 static-open) · mutation จ็อบ 3 แดง · flip `UNKNOWN(+0x99)` แดง (census 182≠181) · one-leg VA edit (ReliveVital) แดง · span_sha256 tamper แดง · membership swap (นับเท่าเดิม) แดงด้วย digest ·  self-test เดิม+ใหม่ผ่าน · ปิดการ์ดแล้ว self-test จับได้

**adversary สองรอบก่อน commit:**
- รอบแรก 4 defect: **D1 (วิกฤต)** `.gitignore` deny-all กิน `patches/` — แพตช์จะไม่ถูก commit เลย ⇒ เพิ่ม allowlist `!/patches/` `!/patches/**` · **D2** mutation `UNKNOWN(` flip message เข้า static_open หนีการ์ด ⇒ pin census 181/859 · **D3** normalization laundering หนึ่งขาบนคู่ที่ raw เหมือนกัน ⇒ raw-first + pin 40 คู่ · **D4** span columns ไม่ถูก mirror ⇒ ผนวก span_start/end/sha256 · + คำถาม provenance ⇒ harness echo sha256
- รอบสอง: 4 ข้อเดิมปิดสนิท (ตรวจซ้ำรายข้อ) · pin 40 คู่ตรงตารางจริงเป๊ะ (pinned−derived = ∅ ทั้งสองทาง) · เจอ defect ใหม่ 1 (moderate): **สลับสมาชิก static_open แบบรักษาจำนวน** — แก้ 3 แถวประสานกัน (flip `Activity_BasicVital` ออก + `Attribute` เข้า) ผ่าน count pin 181/859 ได้ ⇒ **แก้ด้วย membership digest pin** (`EXPECTED_STATIC_OPEN_MEMBERSHIP_SHA256` = sha256 ของรายชื่อเรียงแล้ว) + self-test เคสโจมตีตัวจริง + ด่าน T6 ใน harness — รันซ้ำเขียวครบ 8 ด่าน

**nonclaims ของการ์ด:** ไม่ครอบ mutation สมมาตรสองขา · ไม่ครอบการแก้ VA ฝังในคู่ pinned 40 คู่ (ชั้นนั้นพึ่ง `span_sha256` mirror + GT-054 ที่ verify กับอิมเมจ 392/392) · ไม่ครอบ `gate_condition`/`file_off_claim` (legs ต่างเกิน mirror โดยชอบ · validator ไม่อ่านสองคอลัมน์นี้) · เขียวบน cloud คือชั้น schema เท่านั้น — จ็อบ 3 ตัวจริง (บน capture) ต้องรันบนสะพาน · **การ์ดแดงบน corruption ไม่ใช่การยืนยัน schema** — F1/F2/F3 ของใบเดิมติดทุกตัวเลขเหมือนเดิม

## คิวเทสเกม (กติกา v5 ข้อ ⑤)

รอบนี้ไม่เพิ่มใบใหม่ใน `GAME_TEST_QUEUE.md` — เหตุผล: งานที่เกิดจากรอบนี้เป็นงาน STATIC-ON-BRIDGE ต่อท้ายใบ GT-047 เดิม (ขั้น apply patch + rerun เขียนไว้ในบล็อกสถานะ R144 ของใบเดิมแล้ว — ไม่เปิดใบใหม่ซ้ำซ้อน) · ใบ attended ทั้งหมดยังพักตามคำสั่ง Panya 16:56 (23 ส.ค.) และ GT-034 นัดเทสด้วยตา 26 ส.ค. · ไม่มีฟีเจอร์ใหม่ฝั่ง client-observable ที่พร้อมเทสเพิ่มจากรอบก่อน

## คำถามค้างถึง Panya (ใหม่จากรอบนี้)

1. **เลนลูทฝั่งเซิร์ฟเวอร์ (จาก GT-049):** บรรทัด `ได้รับ [ชื่อ] * จำนวน` มาจาก inbound `ItemOperateVitalRes` ⇒ ถ้าอยากให้ลูทเก็บแล้วขึ้นข้อความจริง เซิร์ฟเวอร์เราต้องส่ง message นี้ (id 131 · serializer `0x005EDA20` · R 5 ฟิลด์ตาม TSV) — เป็นเลนใหม่เกิน pre-approved pattern เดิมไหม หรือให้เปิด hypothesis ใต้ pattern มาตรฐาน (opt-in scenario · fail closed) ได้เลย?
2. **direction ของ `TriggerCastSkillVital`/`CLearnSkillVital`:** static ปิดเลนแล้วทั้ง RE-056 (METHOD-FAIL) และ RE-058 (bounded negative) — ทางเดียวที่เหลือคือ observe-only attended (พักอยู่) · ไม่ต้องตอบตอนนี้ จดให้เห็นว่าคอขวดอยู่ที่ไหน

## ไฟล์ที่แตะรอบนี้ (repo `pf_bridge` ทั้งหมด · repo โค้ดไม่แตะ)

- ใหม่: `patches/gt047/pf_validate_capture_fields.py` · `patches/gt047/verify_gt047_guard_patch.py` · `patches/gt047/README_GT047_PATCH.md` · `rounds/R144_ycp7vk_gt047_fieldoffset_guard_patch.md` · `notes_to_chief/FROM_CHIEF_R144_TO_ATTENDED_20260824_1740.md` · stub `.CONSUMED.txt` 5 ใบ + สำเนาใน `consumed/` 5 ใบ
- แก้: `.gitignore` (เพิ่มบล็อก allowlist `patches/`) · `GAME_TEST_QUEUE.md` (หัวไฟล์ + GT-047 + GT-049) · `CLIENT_RE_QUEUE.md` (RE-057 + RE-058) · `CHIEF_CONTINUATION.md` (ต่อท้ายหนึ่งบรรทัด)

## sha pins

- source เดิม (จากจดหมาย 0916 · LF · 47,884 bytes): `0166337CBC8E9E561D9D3CD5F02364F4ED43C49070644D5423387E87B793D8C8`
- ฉบับแพตช์ `patches/gt047/pf_validate_capture_fields.py`: `cafa5f69401eaf152f7ae4e646ce76eb3016c3d6b71e76c494819a029877011b` (58,656 bytes · LF) · harness `verify_gt047_guard_patch.py`: `3f7a153835152b76d9e885bde6676c65ca395a4724c14f1a1a7da63d93c3a95f` (4,849 bytes)
- `external/PF_SERIALIZER_FIELDS.tsv` ที่ใช้วัดอินเวเรียนต์: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
