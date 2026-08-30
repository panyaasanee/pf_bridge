# รอบ `gm17278` (สาย GM) -- 2026-08-31T02:28+07:00

## 1. round-lock

- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (ยืนยันขั้นแรก, `external/PF_PROTOCOL_REGISTRY.tsv`
  / `external/PF_SERIALIZER_FIELDS.tsv` ก็มีจริง)
- ต้นรอบไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo (`list_pull_requests(state=open)`: pf_bridge มีแค่
  `[LANE-E]` #550, pirate-force-server มีแค่ `[LANE-E]` #349 -- ไม่บล็อกสายนี้) ⇒ ยึดล็อกด้วย draft
  pirate-force-server **#350** (`PF-AUTOMERGE: v4` ยืนยันในตัว body)
- ชะตารอบก่อน (`aejgap`, PR #345) วัดด้วย `pull_request_read(method="get")` ตรง ไม่เชื่อ `list` endpoint
  (ซึ่งคืน `merged:false` ผิดสำหรับ PR ที่ merge แล้วจริงหลายใบ -- gotcha เดิมที่บันทึกไว้ตั้งแต่รอบ
  `0920_LANE-GM-STATUS-mailbox-clear-plus-list-api-merged-field-gotcha`): `#345` `merged:true`,
  `merged_by: github-actions[bot]` ⇒ อยู่บน `main` แล้ว ไม่มีอะไรต้องกู้ branch มี base `a223273` ตรงกับ
  `origin/main` อยู่แล้ว (ไม่ต้อง cherry-pick)
- heartbeat: `_BRIDGE_HEARTBEAT.txt` ล่าสุด `01:54:04+07:00` · ต้นรอบตรวจ `02:2x` ⇒ ห่าง ~34 นาที ผ่านเกณฑ์ 60

## 2. กล่องจดหมาย

grep `^ADDRESSEE: LANE-GM` บนไฟล์ที่ยังไม่มี `.CONSUMED.txt` คู่กัน: **หนึ่งใบ** --
`20260831_0152_PANYA-ORDER-LANE-GM-make-the-BT_GM-button-and-GMUI_BASIC-window-actually-work.md`
(คำสั่งของเจ้าของ, เขียนแทนโดยกะ1-A) -- consumed แล้วรอบนี้ (stub + copy ไป `consumed/`)

**พบระหว่างทาง แต่ไม่เข้าเกณฑ์กล่องจดหมายของรอบนี้:**
`20260831_0146_COO-DECISION-approve-gm-attr-wire-py-fix-misleading-refusal-line.md` (มอบสาย GM สร้าง
`gm/attr_wire.py` ต่อ `/lv`) -- ใบนี้ใช้หัว `[ถึง: สาย GM | จาก: COO]` แต่**ไม่มี token `ADDRESSEE:` เลย**
(grep ยืนยันแล้ว 0 hit) จึงไม่เข้าเกณฑ์กล่องจดหมายที่กำหนดไว้ ไม่ consume/ไม่ทำ stub รอบนี้ -- และตัวคำสั่ง
`0152` (มาทีหลัง 6 นาที) เขียนไว้เองว่างานหลักของสาย GM รอบนี้คือ BT_GM "**แทนการวนกฎ F ทำงานรองไปเรื่อย ๆ**"
⇒ อ่านว่า `attr_wire.py` ถูกเลื่อนไปตั้งใจ ไม่ใช่ถูกลืม บันทึกไว้ที่นี่ให้ชัดสำหรับรอบถัดไป (COO-DECISION
เองให้เวลา "ไม่ขยับภายใน 3 รอบ" ก่อนต้องรายงานสถานะ -- รอบนี้คือรอบที่ 1)

## 3. การทดลอง BT_GM/GMUI_BASIC (คำสั่งเจ้าของ)

### สร้างในเขต `gm/` (pirate-force-server)

1. `src/pirateforce_foundation/gm/bt_gm_probe.py` (ใหม่): experiment fork แบบ `PF_ADHOC_ATTR_PROBE`
   - `iter_state_vital_bit_variants()`/`build_variant_frame()`/`build_variant_payload()`: 14 variant ของ
     เฟรม `GM_UpdateGMStateVital` (0x5A19, 41 ไบต์ที่พินแล้ว) ทีละฟิลด์ -- ห่อ `gm/state_wire.py`'s proven
     builder ตรง ๆ ไม่เพิ่ม tag/offset ใหม่แม้แต่บิตเดียว
   - `SUSPECT_STUBS` (3 รายการ, แท็ก `[สมมติของสาย GM - รอ RE]`): connection-context / query-gate-value-
     at-click-time / current-UI-object-key -- คำถาม+เหตุผลที่ยังต่อสายไม่ได้รอบนี้ ไม่มีการเดาความหมาย
     ผู้ต้องสงสัยตัวที่สี่ (create path/factory) ไม่ทำเป็น stub เพราะเป็นผลที่การคลิกสังเกต ไม่ใช่ตัวแปร
2. `tests/test_gm_bt_gm_probe.py` (ใหม่, 22 เทส): ตรวจ frame/payload construction เท่านั้น (41/9 ไบต์,
   vital id, field range, variant id ไม่ซ้ำ, stub metadata) -- ไม่มีเทสอ้างว่าหน้าต่างเปิด
3. `docs/GM_LANE.md`: เพิ่มหัวข้อ "รอบ `gm17278`" (ไม่ลบประวัติเดิม)

### เปิดในเขต pf_bridge

- `CLIENT_RE_QUEUE.md`: **`RE-164`** `[NEEDS-ATTENDED-CAPTURE]` -- ใบสอบสวนหลัก สี่ผู้ต้องสงสัย
- `GAME_TEST_QUEUE.md`: **`GT-165`** `[attended, in-game]` -- สเปกคลิกทีละ variant สำหรับกะ1-A
  **สถานะ 🔴 BLOCKED** (ดูข้อ 4)
- `notes_to_chief/20260831_0225_LANE-GM-CORE-REQUEST-GM-043-...md`: ตรวจ `runtime.py:6424-6438` พบว่า
  จุดเรียก `make_gm_update_state_frame` ที่มีอยู่ยิงค่าคงที่ `(0,1,0)` ครั้งเดียวตอนล็อกอินเท่านั้น
  ("ALWAYS ON, no scenario flag") -- ไม่มีทางยิง variant อื่นระหว่าง session เดียวกัน เสนอสองทางเลือก
  (GM chat-command ใหม่ / debug scenario flag) ให้ chief เลือก

## 4. ทำไม `GT-165` ยังคลิกไม่ได้รอบนี้

ตรวจ `runtime.py` แล้วก่อนเขียนสเปก (ไม่ใช่แค่สมมติ) พบว่าจุดเรียกเดียวที่มีตอนนี้ยิงค่าคงที่ `(0,1,0)`
ตอนล็อกอินของบัญชี GM เท่านั้น -- **ค่านี้เองคือค่าที่ `GT-101`/`GT-103`/`GT-107` ทดสอบมาแล้วทั้งหมด** (ปุ่ม
`BT_GM` โผล่จริง แต่คลิกแล้วเงียบ) ⇒ ยังไม่มีทางส่ง variant อื่น 13 ตัวที่เหลือของ `bt_gm_probe.py` ไปทดสอบ
ได้เลยจนกว่า `CORE-REQUEST-GM-043` จะลง -- นี่คือขอบเขตที่แท้จริงของ "สร้างเครื่องมือ" ตามคำสั่งเจ้าของ ไม่ใช่
"พิสูจน์ว่าปุ่มทำงาน"

## 5. pf-adversary

**หมายเหตุเครื่องมือ:** เซสชันนี้ไม่มี subagent `pf-adversary` ให้เรียกโดยตรง (ต่างจากรอบก่อน ๆ ที่เรียกได้)
-- ทำการทวนแบบ adversarial ด้วยตัวเองแทนตามมาตรฐานเดียวกัน (อ่าน source citation ทุกจุดทวนกับใบผลต้นทาง จริง
ไม่เชื่อความจำ) พบข้อบกพร่องจริงหนึ่งจุด: docstring แรกของ `iter_state_vital_bit_variants()` เขียนว่า "RE-089
never measured whether the collapse rule extends to the u32 field" -- ตรวจกับต้นฉบับ
`notes_to_chief/.../RE-089-RESULT-...` (ใน `archive/notes_to_chief_2026-08/`) แล้วพบว่าไม่ถูกต้อง: RE-089
เดิน u32 field จริงและพบรูปร่าง**ตรงข้าม**กับสอง byte -- ก๊อปผ่านสองทอด (`GMModule_Client+0x1C` แล้ว
type-0x25 argument `+0x18`) "โดยไม่มี compare/switch/arithmetic ในสองช่วงที่พิสูจน์" (คำของ RE-089 เอง) --
ไม่ใช่ "ไม่ได้วัด" แต่คือ "วัดแล้ว ไม่พบการ collapse ในสองทอดที่ตามได้" แก้ docstring ให้อ้าง RE-089 ตรงตามนี้
แล้ว รันเทสซ้ำเขียวทั้งคู่ (`test_gm_bt_gm_probe.py`/`test_gm_state_wire.py`)

## ทดสอบ

`pytest tests/test_gm_bt_gm_probe.py -q`: **22 passed**
`pytest tests/test_gm_*.py -q`: **1076 passed** (+22), 471 subtests, 0 failed
`pytest tests/ -q` เต็ม: **5626 passed** (+30), 327 skipped, 9733 subtests passed, 0 failed (cloud sanity,
base `origin/main` ต้นรอบ `a223273`)
`python3 tools/verify_hypothesis_ledger.py` / `verify_functional_coverage.py`: ทั้งคู่ PASS ไม่มี drift

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ยังไม่มี** -- รอบนี้สร้างตัวสร้างเฟรม/เทส/ใบคิวเท่านั้น ยังไม่มีจุดเรียกที่ยิง variant ได้จริง
(`CORE-REQUEST-GM-043` รออยู่) `GT-165` เขียนสเปกล่วงหน้าไว้แล้วแต่คลิกไม่ได้จนกว่าจุดเสียบจะลง จาก
`GMUI_BASIC` เปิดหรือไม่เปิด -- ยังไม่มีใครรู้คำตอบหลังรอบนี้เหมือนก่อนรอบนี้ทุกประการ

## nonclaim

**ไม่มีการอ้างว่า `GMUI_BASIC` เปิดหรือไม่เปิดจาก variant ใดเลยรอบนี้** -- ไม่มีการเปิด client ไม่มีการส่ง
เฟรมจริงไปยังไคลเอนต์จริง สาย GM ไม่มีจอ ไม่มีอิมเมจไคลเอนต์ ไม่มี `gh` การคลิกจริงเป็นของกะ1-A เท่านั้น
งานรอบนี้ทั้งหมดคือการสร้างเครื่องมือให้พร้อมสำหรับการคลิกทดสอบ ไม่ใช่การพิสูจน์ว่าปุ่มทำงาน -- ไม่แตะ
`runtime.py`/`app.py`/`pf_login_game_server_v141.py` (อ่านอย่างเดียวผ่าน `legacy_bridge`) ไม่แตะ
`scenarios/world_*.json`/`scenarios/combat_*.json` ไม่แตะ canonical DB ไม่แตะเขตสาย A/สาย B

## ค้นแล้ว: เจอ/ไม่เจอ

- ค้นชุดส่งมอบ RE (`external/00_SEARCH_HERE_FIRST.md`, `PF_PROTOCOL_REGISTRY.tsv`, `PF_SERIALIZER_FIELDS.tsv`):
  **เจอ** -- ทั้งสามไฟล์มีจริง `state_wire.py` เดิมอ้าง span_sha256 ไว้แล้ว รอบนี้ไม่เพิ่ม field ใหม่จึงไม่ต้อง
  verify span ใหม่
- ค้น fork ทดลอง GM state ที่มีอยู่แล้ว (ตามนonclaim 3 ของใบสั่งเจ้าของ, "กะ1-A ไม่ได้ตรวจ"): **ไม่เจอ** --
  `find`/`grep` หา `bt_gm`/`gmui_basic`/`gm_state_probe`/`gm_click` ใน `src/`/`tests/` ก่อนสร้าง เจอแค่ชื่อ
  ไฟล์ที่มีคำว่า `gm` ทั่วไป ไม่มี probe module เดิม
- ค้น CORE-REQUEST-GM ล่าสุดก่อนจองเลข: **เจอ** สูงสุดคือ `GM-042` ⇒ ใบใหม่รอบนี้คือ `GM-043`
- ค้น RE/GT ล่าสุดก่อนจองเลข: **เจอ** สูงสุดคือ `RE-163` ⇒ `RE-164`/`GT-165` ว่างจริง (grep ยืนยัน 0 hit
  ทั้งคู่ก่อนเขียน)

— สาย GM รอบ `gm17278`
