# ARCHIVE ของ GAME_TEST_QUEUE.md — ย้ายมา 2026-08-17 23:1x (chief รอบ 44)
> รายการที่ปิดแล้ว + evidence เต็ม ย้าย verbatim — ห้ามลบ



<!-- ===== GT-007 [FAIL — processed commit b03d207 · follow-up = GT-008] | บรรทัดเดิม 286-364 ===== -->

## GT-007 HYP-PF-012 clean logout: client ออกเกม/กลับ char select ได้จริงจาก echo ack  [FAIL — ประมวลผลแล้ว commit `b03d207` · follow-up = HYP-PF-013 → **GT-008 เข้าคิวแล้ว (ด้านบน)**] ❌ 2026-08-17 19:27–19:40 attended

- objective: (claim เดียว — ชั้น client-observable เท่านั้น) เมื่อ server ตอบ echo ack ของ
  `LogoutVital` แล้ว **ปุ่ม "ออกจากเกม" (subcode 01) ทำให้ client ปิดตัวเองสะอาด และปุ่ม
  "กลับหน้าเลือกตัวละคร" (subcode 03) พา client กลับหน้า char select จริง** — ไม่ค้างจนต้อง
  End task เหมือนก่อน (GT-002 client2) · ชั้น wire/DB พิสูจน์แล้ว headless (report
  `PF_LOGOUT_ACK001_...20260817.md` — อย่าเทสซ้ำ อย่านับเป็นเกณฑ์)
- db: สำเนา canonical สด (copy ใหม่ก่อนรัน · เช็ค sha กับค่าใน LOCK ก่อน)
- server args: บูตตรง `py -3 -m pirateforce_foundation.app` + `--db <copy>` +
  `--capture-root <dir>` + `--second-password-mode bypass` +
  `--logout-hypothesis-scenario scenarios\logout_hypothesis_ack_echo.json`
  (🔴 ไม่ใส่ธง = server ไม่ตอบ logout เลย = client ค้างแบบเดิม — นั่นคือ negative control
  ไม่ใช่ FAIL ของเทสนี้)
- steps:
  1. boot server (ธงครบ) → เปิดเกมผ่าน bridge → PLAYBOOK ข้อ 1–6 เข้าแมพ
  2. เปิด dialog ระบบ → คลิกปุ่ม **"กลับหน้าเลือกตัวละคร"** (subcode 03 ก่อน — ถ้า client
     กลับ char select ได้จริง จะเทส 01 ต่อในเซสชันเดียวกันได้)
  3. สังเกต: client กลับหน้าเลือกตัวละคร? หรือค้าง? (จับเวลา ~15 วิ) — บันทึกทั้งสองกรณี
  4. ถ้ากลับ char select ได้: เข้าแมพใหม่ → เปิด dialog → ปุ่ม **"ออกจากเกม"** (subcode 01)
     → สังเกต: หน้าต่างปิดเอง? process จบสะอาด? (เช็ค exit ผ่าน job teardown)
  5. ถ้า step 3 ค้าง: End task ตามเดิม → ยังต้องรัน step 4 ในเซสชันใหม่ (สอง subcode
     อาจให้ผลต่างกัน — อย่าสรุปข้ามกัน)
  6. teardown มาตรฐาน + เก็บ GAME_EVENTS/GAME_LIVE/console
- pass criteria (แยกชั้น):
  - **client-observable (เทสนี้):** 03 → เห็นหน้า char select กลับมาจริง · 01 → หน้าต่างปิด
    เองโดยไม่ End task · ไม่มี error dialog/crash
  - **wire-DB (ยืนยันซ้ำเฉย ๆ ผ่าน job):** `HYP_PF_012_LOGOUT_SUBCODE0x_ACK...` ใน console ·
    session ที่เกี่ยวข้อง closed_at ไม่ NULL · integrity ok
- nonclaims: ไม่พิสูจน์ multi-cycle logout/login วนหลายรอบ · ไม่พิสูจน์ logout ตอนยังไม่เข้าแมพ ·
  ไม่พิสูจน์ subcode อื่น · ผล FAIL = falsify เฉพาะ "รูปแบบ response ที่ออกแบบ" ไม่ falsify
  การ decode (R38 ยังยืน) — ถ้า client ยังค้างทั้งที่ ack ถึง ให้เก็บ GAME_LIVE ไว้ครบ
  แล้ว chief จะออกแบบ response รูปแบบถัดไป
- result: ❌ **FAIL ตามเกณฑ์ client-observable — แต่เป็น FAIL ที่ให้ข้อมูลครบทุกชั้น**
  attended 19:27–19:40 · ผู้ขับ: เซสชันหลัก (สิทธิ์เดิมของเซสชัน) · jobs `080`→`081` ·
  server บูตด้วยธง `--logout-hypothesis-scenario` บนสำเนา `pirateforce_gt007_20260817_192713.sqlite3`
  - **ชั้น client-observable (ตาเห็นจริง):**
    - dialog logout เปิดจากเมนู HOME → "ออก" (มี 3 ปุ่ม: กลับเข้าเกม / กลับหน้าเลือกตัวละคร / ออกจากเกม)
    - **subcode 03** (กลับ char select, กด 19:32:42): dialog ปิด → **ไม่กลับ char select**
      ยังอยู่ในแมพ · **ไม่ค้าง** — เมนู/UI ในเกมตอบสนองปกติ (เปิด HOME ซ้ำได้)
    - **subcode 01** (ออกเกม, กด 19:33:57): dialog ปิด → **หน้าต่างไม่ปิดตัวเอง** · ไม่ค้างเช่นกัน
    - **X ของหน้าต่างยังใช้ได้ปกติ** → dialog ยืนยัน → ปิดสะอาด (ไม่ต้อง End task!)
      ⚠️ ระหว่างเทสเคยสรุปผิดว่า "X ตาย" — จริง ๆ คือ**หน้าต่างแอป Claude บังปุ่ม X**
      (คลิกโดนหน้าต่าง Claude ที่มองไม่เห็นใน screenshot ของผู้เทส) ย้ายหน้าต่างเกมแล้วเทสซ้ำ
      = X ทำงานปกติ · ผู้เทสรอบหน้าต้องย้ายหน้าต่างเกมให้พ้นเขตขวาของจอก่อนเสมอ
    - เทียบ GT-002 client2 (freeze เต็มตัว ไม่รับอะไรเลย): **อาการ freeze หายไปแล้ว** —
      นี่คือ delta ที่ ack สร้าง (สังเกตการณ์ ไม่ใช่การพิสูจน์เหตุ)
  - **ชั้น wire/DB (job 081 + อ่านสำเนา DB):**
    - GAME_EVENTS: เฟรม `0x1B40` สองลูกตรงเวลากดเป๊ะ — seq=3 19:32:42.440 payload
      `0803...` (03) · seq=5 19:33:57.225 payload `0801...` (01)
    - GAME_LIVE: `SENT label=HYP_PF_012_LOGOUT_SUBCODE03_ACK_AFTER_CLEAN_CLOSE 46B late 0.5ms`
      — **ack ออกเฉพาะ 03 (marker ×1)** · 01 ไม่มี ack = สอดคล้องดีไซน์ fail-closed:
      session ถูกปิดไปแล้วหลัง 03 → เฟรม 01 ที่ตามมาเจอ dispatch เงียบ
    - **DB สำเนา: session ใหม่ (lease 6) opened 19:29:00 → `closed_at 19:32:42.464` =
      +24ms หลังเฟรม 03 และก่อน ack (.485)** — ลำดับ "closed_at ก่อน ack" ของ HYP-PF-012
      เกิดจริงบน GameClient จริงครั้งแรก · open sessions=0 · integrity ok
    - canonical DB **ไม่ถูกแตะ** (sha `FA794D0B..4400` เท่าเดิม — เทสรันบนสำเนา)
  - 🔴 บั๊กเครื่องมือที่ต้องแก้ก่อนใช้ template ซ้ำ: 081 อ่าน DB สำเนาไม่ได้เพราะ info file
    เก็บ path มี space แล้ว parse แบบ split whitespace ตัด path ขาด (บั๊กตระกูลเดียวกับ 069)
    — DB AFTER ในตัว log 081 จึงเป็นค่าขยะ ผู้เทสอ่านซ้ำจากสำเนาโดยตรงแล้ว (ค่าข้างบน) ·
    template teardown รุ่นถัดไปให้เก็บ path ในไฟล์แยกบรรทัด หรือใส่ quote แล้ว parse ใหม่
  - **สรุปสำหรับ chief:** echo ack shape ปัจจุบัน = กัน freeze ได้ (สังเกตการณ์) แต่ **ไม่ trigger
    transition ฝั่ง client** ทั้ง 03/01 → falsify เฉพาะ response shape ตาม nonclaim ·
    ข้อมูลออกแบบ shape ถัดไป: client น่าจะรอ response ที่มีเนื้อหามากกว่า echo (เช่น world/char
    list payload สำหรับ 03, close instruction สำหรับ 01) — raw ครบใน
    `GameClient\capture_gt007_20260817_192713\` + สำเนา DB เก็บไว้เป็นหลักฐาน
  - nonclaims: ไม่พิสูจน์ว่า freeze หายเพราะ ack (ไม่มี control run แบบไม่มีธงในเซสชันนี้) ·
    ไม่พิสูจน์ multi-cycle · ไม่ falsify การ decode R38 (เฟรมมาตรงปุ่มทุกครั้ง = ยิ่งยืนยัน)
- 📍 อัปเดตรอบ 41 (19:1x): **ชั้น wire/DB ปิดแล้ว** — commit **`b90007e`** (gate 415/0 ·
  ledger 19 · domains 8) · headless proof jobs 076/077 (ack byte-exact 01/03 ·
  closed_at ก่อน ack 13–16ms · dispatch เงียบหลัง ack) · report+manifest ใน repo แล้ว
  เทสนี้เหลือชั้น client-observable ล้วน ๆ ตาม steps ข้างบน
- 📍 ประมวลผลรอบ 42 (19:5x scheduled): report
  `reports/PF_GT007_LOGOUT_ECHO_ACK_CLIENT_TRANSITION_NEGATIVE_20260817.md` (+manifest 12 ไฟล์
  รวมสำเนา run DB) · matrix `clean_logout` คง in_progress (แก้ notes อย่างเดียว — digest ไม่รวม
  notes จึงไม่ re-pin) · STATUS.md bullet · gate 082 เขียว 415/0 · **commit `b03d207`** (docs-only)
  · fact ใหม่จาก GAME_LIVE ที่ใช้ออกแบบต่อ: หลัง ack client **ค้างบน socket เดิม ส่ง keepalive
  GSCN_RunTimeProtocolReq ทุก ~2 วิ ไปเรื่อย ๆ** (19:33→19:40 จน teardown) ไม่ปิดเอง ไม่ reconnect
  → follow-up = HYP-PF-013 (ack + server ปิด socket) ดู CHIEF รอบ 42



<!-- ===== GT-002 [PASS — PROCESSED commit b1087bb รอบ 37] | บรรทัดเดิม 467-591 ===== -->

## GT-002 M4 free-slot runtime ชุดแรก  [PASS — PROCESSED ✅ commit `b1087bb` 17:4x รอบ 37] เทส attended 16:30–16:5x ที่ HEAD `55c7c59` · report: `reports\PF_GT002_GENERALIZED_FREE_SLOT_MOVE_FIRST_CLIENT_ACCEPTANCE_RUNTIME_PASS_20260817.md` + manifest 15 ไฟล์ · matrix `inventory/move_known_item_any_free_slot` → `runtime_pass`

> 🟢🟢 **ปลด block รอบ 35 (2026-08-17 16:1x):** M4 runtime hookup **landed = commit `4c29a63`**
> (gate 064 ALL GREEN 398/0 ก่อน commit · ตามมาด้วย item-14 `55c7c59` → เกณฑ์เขียวปัจจุบัน **405/0**)
> `runtime.py` ต่อ wire ItemOperate generic → `session.move_backpack_item_to_free_slot`
> **ใต้ `--item-move-hypothesis-scenario` เท่านั้น** · `production_allowed=false` คงเดิม ·
> occupied/unknown/out-of-range **fail closed** · เทสเฝ้า: `tests/test_item_move_generalized.py` (299 บรรทัด)
>
> **steps/pass criteria ฉบับ chief (ใช้ได้ทั้ง attended และ unattended-with-grant):**
>
> - **db:** สำเนา canonical DB (sha `CACE7F77..F493`) ที่**ยังไม่เคยถูกใช้รันเทสนี้** — copy ใหม่
>   ก่อนรันเสมอ (บทเรียน R21 one-shot merge — คนละ path กับ free-slot แต่กันตีความพลาด)
> - **steps:**
>   1. บูต server ผ่าน bridge: `tools\run_foundation_visible.ps1` **+ `--item-move-hypothesis-scenario`**
>      (visible console ตามกฎเหล็ก) — 🔴 ไม่ใส่ธงนี้ = `PermissionError` ที่ `session.py:78` = แดงปลอม
>   2. เปิดเกมผ่าน bridge (redirect stdout/stderr + วาง teardown job ต่อคิวล่วงหน้า — บทเรียน R31)
>      → รอหน้าต่าง 'Pirate Force' → สิทธิ์: attended มีอยู่แล้ว / scheduled ต้องธง PANYA_PRESENT สด
>   3. login identity1 → เข้าแมพตาม PLAYBOOK ข้อ 1–6
>   4. เปิด Backpack → ลากไอเทมจาก **slot2 → slot10** (ช่องว่าง)
>   5. ตรวจ UI ทันที: ไอเทมอยู่ slot10 · slot2 ว่าง · จำนวนรวมไม่เปลี่ยน
>   6. reconnect: ปิด client (X ปกติ) → เปิดใหม่ → login เดิม → Backpack ต้องแสดง slot10
>   7. teardown มาตรฐาน: Ctrl+C สะอาด · listeners 0 · เก็บ GAME_LIVE/GAME_EVENTS/console tail
>   8. ตรวจ DB จากสำเนาใน /tmp (ห้ามแตะไฟล์จริง):
>      `SELECT slot FROM character_backpack_items WHERE character_id=<id1>` ต้องมีแถว slot=10 ไม่มี slot=2 (ของไอเทมนั้น)
>      และ `character_backpacks.updated_at` ขยับ — **ตาราง persistence = `character_backpack_items` + `character_backpacks`** (จาก `store.py:360`)
> - **pass criteria (หนึ่ง claim — runtime_pass):** ครบทั้ง 4 ชั้น
>   (1) wire: เฟรม `ItemOperateVitalReq` ของการลากปรากฏใน GAME_LIVE **และ server ตอบ** (ไม่เงียบ)
>   (2) DB: แถว `character_backpack_items` เปลี่ยน slot 2→10 ตามข้อ 8
>   (3) UI: หลัง reconnect ไอเทมแสดงใน slot10 (client-observable — ต้องมีคนเห็นถ้า attended)
>   (4) หลังเทส: DB integrity ok + gate ยังเขียว 405/0
> - **การตีความผลลบ:** server เงียบ/ไม่เขียน DB → เช็กก่อนว่าบูตด้วยธง scenario จริงไหม
>   (สาเหตุแดงปลอมอันดับหนึ่ง — R21) · ถ้าธงถูกแล้วยังเงียบ = FAIL จริง บันทึก bytes เต็มเฟรมแล้วหยุด
> - **nonclaims:** occupied slot (ต้อง fail closed — ยังไม่ claim ในรอบแรก) · swap · stack ·
>   ไอเทม id อื่น · multi-move ติดกัน · persistence ข้าม server restart (นั่นคือเทสถัดไป)

> 🟢🟢 **คำตัดสินจาก Panya (15:00 ผ่านเซสชันหลัก AskUserQuestion — เขียน 15:14):
> M4 runtime hookup = อนุมัติ** ตามขอบเขต 21.5.2: ต่อ wire ItemOperate generic เข้า
> `session.move_backpack_item_to_free_slot` ใต้ opt-in scenario เดิม ·
> `production_allowed=false` · occupied fail closed → **chief เริ่ม M4 + เขียน
> steps/pass criteria ของเทสนี้ได้เลย** (รายละเอียดบล็อกเต็มอยู่หัวไฟล์ CHIEF_CONTINUATION.md)

> 🟢 **อัปเดตรอบ 31 (2026-08-17 14:22):** M3/HYP-PF-010 **landed แล้ว** เป็น commit
> `abf3696` (ledger+verifier+src 5 ไฟล์+เทส 2 index, Windows gate 384/0 ก่อน commit)
> แต่ **ตัวปลด block ของเทสนี้ยังไม่ครบ**: `runtime.py` ยังรับ wire request เฉพาะแบบเป๊ะ
> ของ HYP-PF-008 → การลากไอเทมในเกมจริงยังไม่ถึง `session.move_backpack_item_to_free_slot`
> → ต้องทำ **M4 runtime hookup** (รอ Panya เคาะขอบเขต — ดูข้อ 21.5 ใน CHIEF) แล้ว
> chief จะเขียน steps/pass criteria ให้เทสนี้ · ข้อควรรู้ตอนเขียน steps ยังเป็น R21 เดิม:
> ต้องบูตด้วย `--item-move-hypothesis-scenario` และใช้ DB สำเนาที่ยังไม่เคย merge
- objective: identity1 ย้าย slot2→slot10 ผ่าน UI จริง + persistence/reconnect
- db: copy จาก DB post-move (chief จะระบุตอนปลด block) + scenario opt-in
- steps: (chief จะเขียนละเอียดตอนปลด block — ต้องรวม: เปิด Backpack, ลากไอเทม,
  ตรวจ UI count, reconnect แล้วดู slot เดิม)
- pass criteria: (chief กรอก: exact request/response bytes ใน log + DB row + UI)
- nonclaims: occupied slot, swap, stack — ยังเป็น milestone ถัดไป
- evidence R13 (2026-08-17 09:1x, ไม่เปลี่ยนสถานะ BLOCKED): implementation ฝั่ง server
  **มีอยู่แล้วใน worktree** เป็น chain `session.py:74 → lifecycle.py:74 → store.py:354`
  (52 บรรทัด ยังไม่ commit) แต่พิสูจน์แล้วด้วย canary ว่า **ไม่มีเทสใน 337 ตัวเรียกมันเลย**
  และ `git grep` ไม่พบชื่อฟีเจอร์นี้ใน `tests/` `scenarios/` `docs/` `tools/` เลยสักที่
  → เมื่อปลด block แล้ว GT-002 จะเป็น **หลักฐานชิ้นแรกและชิ้นเดียว** ที่แตะโค้ดส่วนนี้
  รายละเอียด: `pf_bridge\FINDINGS_R13_WIP_INVISIBLE_TO_GATE.md`
- evidence R14 (2026-08-17 09:3x, ไม่เปลี่ยนสถานะ BLOCKED): ตอนนี้รู้แล้วว่า **อะไรคือ
  ตัวปลด block** — `docs/FUNCTIONAL_COVERAGE.json` ระบุ capability
  `move_known_item_any_free_slot` เป็น `blocked` พร้อมเหตุผลว่า *"needs a ledger
  decision by the project owner before the work may be committed"* และ
  `HYP-PF-008.evidence_gap` เรียกหา **หลักฐานใหม่** ที่ไม่มีทางได้จากงาน static อีกแล้ว
  (ไม่มี original server ให้ capture) → หลักฐานที่เหลืออยู่ทางเดียวคือ **client acceptance**
  → **GT-002 ไม่ใช่งานปลายทางของ M3 แต่เป็นเงื่อนไขที่ทำให้ M3 เดินต่อได้**
  ลำดับที่ถูกต้อง: Panya เคาะข้อ 6 → chief เขียน steps/pass criteria → game-tester รัน GT-002
  รายละเอียด: `pf_bridge\FINDINGS_R14_LEDGER_BLIND_TO_SEMANTICS.md`
- **evidence R21 (2026-08-17 11:4x, job 044 — ไม่เปลี่ยนสถานะ `BLOCKED`):**
  🔴 **แก้ข้อความในเทสนี้ให้ถูก — บรรทัด boot สำคัญพอ ๆ กับขั้นตอนในเกม**
  - บน **boot มาตรฐาน** (`tools\run_foundation_visible.ps1` = `--db --capture-root
    --second-password-mode`) `runtime.py:479-485` ทำให้ mutator กระเป๋าที่เข้าถึงได้
    **มีตัวเดียวคือ `apply_v111_stack_merge`** ส่วน `move_backpack_item_to_free_slot`
    ที่เป็นเป้าของเทสนี้ raise `PermissionError` ทันที (`session.py:78`)
    → **ต้องบูตด้วย `--item-move-hypothesis-scenario` เท่านั้น** ไม่งั้นผลเทสจะไม่มีทางเขียว
    และจะตีความผิดว่า "implementation พัง"
  - วัดกับเฟรมจริงของ client ทั้ง corpus (630 log / 20,209 เฟรม เท่ารอบ 20):
    `ItemOperate` **24 เฟรม 12 รูปแบบ** (ตรงกับตารางรอบ 16 เป๊ะ) →
    **เขียน DB ได้ 1 ใน 24 เท่านั้น** อีก 23 ตัว *"ไม่ใช่ candidate → ไม่ตอบ ไม่เขียน"*
    ทุกตัวมี `operation=4` ต่างกันที่ `value32`/`item_identity`
  - `apply_v111_stack_merge` บังคับ pre-state เป็น `INITIAL_BACKPACK` เป๊ะ (`store.py:294`)
    → **เขียนได้ครั้งเดียวต่อชีวิตตัวละคร** ครั้งที่สองคืน `None` = replay ไม่เขียน
    → DB ที่ใช้รันเทสนี้ต้องเป็นสำเนาที่ยัง **ไม่เคย** merge มาก่อน
  - 🟢 เทสที่เกี่ยวข้องเขียวจริงวันนี้บน Windows `py -3`: `test_item_lifecycle` 8 ·
    `test_item_move_capture` 8 · `test_item_move_hypothesis` 8 (รวมสวีตรอบนี้ 46 ตัว exit 0)
  - เครื่องมือ: `pf_bridge\replay\pf_itemoperate_audit.py` · เหตุผลเต็ม:
    `pf_bridge\FINDINGS_R21_BACKPACK_WRITES_ARE_ONE_SHOT_AND_DISPATCH_IS_UNGUARDED.md`
- result: ✅ **PASS runtime_pass ครบ 4 ชั้น — attended session 2026-08-17 16:30–16:5x ที่ HEAD `55c7c59`**
  (สิทธิ์ granted tier full 16:32 · jobs `067`/`068` · `069` teardown จะรันอัตโนมัติเมื่อ client2 ถูกปิด)
  - boot: server บน**สำเนา** DB (`state\pirateforce_gt002_20260817_163028.sqlite3` sha ตรง
    canonical `CACE7F77..F493` ✓ canonical ไม่ถูกแตะ) + `--item-move-hypothesis-scenario
    scenarios\item_move_hypothesis_v111_slot2.json` + bypass (บูตตรงผ่าน `pirateforce_foundation.app`
    เพราะ launcher ไม่รองรับธง) · BEFORE: items [1@0 qty2, 2@1, 4@3] · sessions with char 4 · max lease 4
  - ขา move (client1, 16:30–16:38): เข้าแมพ Port Royal **X:-8,094 Y:-3,207 = ตำแหน่ง GT-005 persist ✓**
    → Backpack 3/40 → **ลาก id1 slot0 → slot10** (เจตนาเลี่ยง slot2 ซึ่งเป็น request เป๊ะของ 008):
    1. **wire**: `GAME_EVENTS_LIVE.txt` seq2 frame132 `ItemOperateVitalReq` id=0x4BED
       operation=4 value32=10 item_identity=1 (payload 16B)
    2. **server ตอบ**: `[G>] HYP_PF_010_ITEM_MOVE_ID1_TO_FREE_SLOT10_COMMITTED (82 bytes; late=0.3 ms)`
    3. **DB**: `character_backpack_items` → [(1,2,1),(3,4,1),**(10,1,2)**] ·
       `character_backpacks.updated_at` → 2026-08-17T09:37:24.806Z (=16:37:24 ICT ตรง event) — สองตารางตามที่ระบุ
    4. **UI**: "Adventure Key" ไป slot10 ทันที · slot0 ว่าง · count 3/40 ไม่เปลี่ยน
  - ขา reconnect (client2 ผ่าน job `068` อัตโนมัติ, 16:40–): login ใหม่ → **Backpack แสดง id1 qty2 ที่
    slot10 / slot0 ว่าง** (state อ่านจาก server = read-back ✓) · sessions with char 4→6 · open=1 (client2)
  - nonclaims: occupied/swap/stack/multi-move · ยังไม่ claim durability ข้าม server restart (แค่ reconnect)
  - หลักฐาน: `outbox\067_gt002_boot.utf8.txt` · `068_gt002_reconnect.utf8.txt` ·
    `GameClient\capture_gt002_20260817_163028\` (server console + capture_v141) · AFTER/integrity อยู่ใน 069
- 🔴🔴 **observation ใหม่ระหว่างเทส (ระดับเดียวกับ 0xAC52 ของ GT-006): โปรโตคอลออกจากเกม = `UNKNOWN_0x1B40` และ Foundation ไม่ตอบ:**
  - คลิกปุ่มใน dialog ออกของ client2 ส่งเฟรมจริงทุกครั้ง: `0x1B40` 14 bytes, **subcode ต่างตามปุ่ม**
    (payload `0801..`=ออกจากเกม จับได้ 3 ครั้ง seq 3/5/7 · `0803..`=กลับหน้าเลือกตัวละคร seq 9)
    และการเปิด dialog ยิง `GetWorldInfoVital` 0x3D4B ควบคู่ — ดู `GAME_EVENTS_LIVE.txt` 16:44–16:52
  - **server ไม่ตอบ 0x1B40** → client รอเงียบ dialog ปิดเองแต่ไม่ออกจากเกม → จากนั้น client2 เข้าสถานะ
    **ไม่รับ X / Alt+F4 / Esc** (ยืนยันสถานะ "ต้องให้ผู้ใช้ End task" ที่ PLAYBOOK เคยบันทึกไว้)
  - แปลก: **client1 ปิดผ่าน X → dialog "ต้องการปิดเกมหรือไม่?" → ยืนยัน ได้ปกติ** (เป็น dialog คนละตัว
    ดูเป็น client-local) — เงื่อนไขที่ทำให้ X ตายบน client2 ยัง undecoded · chief ควร decode 0x1B40 ต่อ
    (ห้ามผู้เทส decode ตามกฎ) — แถวใหม่ของ matrix: session lifecycle / clean_logout ยังไม่มี → พิจารณาเพิ่ม
  - ✅ **decode แล้ว (รอบ 38, 17:55–18:1x): `0x1B40` = `LogoutVital`** — string เดียวทั้ง
    client binary ที่ hash (registry v141) ตรง + มี `AVSystemSettingLogoutConfirmEventHandler`
    ยืนยันเส้นทาง dialog · payload `08 <subcode:01=ออกเกม|03=กลับ char select> 08 00 14 0 14 0`
    · ของแถม: `0xAC52` (GT-006) candidate เดียวใน vital namespace = `Channel_LocalTalkMessageVital`
    · registry ครบ 327 wire vitals (collision-free) อยู่ที่
    `pf_bridge\VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — unknown id ต่อไป lookup ได้ทันที
    · รายละเอียด+nonclaims+ข้อเสนอ HYP-PF-012 (ตอบ LogoutVital → clean logout, รอ Panya เคาะ):
    `pf_bridge\FINDINGS_R38_0x1B40_DECODED_LOGOUTVITAL.md`



<!-- ===== GT-003 [CLOSED — known_limitation ทาง (ข)] | บรรทัดเดิม 592-647 ===== -->

## GT-003 concurrent_multi_client — client 2 ตัวพร้อมกัน  [CLOSED — ข้อ 14 = ทาง (ข) known_limitation]

> 🟢🟢 **คำตัดสินจาก Panya (15:00 ผ่านเซสชันหลัก AskUserQuestion — เขียน 15:14):
> ข้อ 14 = ทาง (ข)** ตามที่ chief เอนไว้ใน FINDINGS_R18: บันทึก single-session เป็น
> **`known_limitation`** (ไม่ใช่ `by_design`) + เปิด hypothesis ใหม่ค้างใน ledger
> ไม่ปิดประตู multiplayer → **ปลดรายการนี้ออกจากคิว attended** — ไม่ต้องเผาเวลา
> Panya กับเทสที่ชั้น wire พิสูจน์แล้วว่าไปไม่ถึงโดยโครงสร้าง (listen(4) serial accept)
> งานที่เหลือเป็นของ chief: เขียน ledger entry + แก้แถว matrix ตามแนว (ข)
> (บล็อกเต็มอยู่หัวไฟล์ CHIEF_CONTINUATION.md)
- objective: **หนึ่ง claim เดียว** — server รับ client 2 ตัวพร้อมกันได้โดยแต่ละตัวมี
  session row ของตัวเอง และปิดครบทั้งคู่ตอนออก
  (แถว `concurrent_multi_client` ใน `docs/FUNCTIONAL_COVERAGE.json` domain
  `session_lifecycle` ตอนนี้เป็น `not_started` — เทสนี้จะยกเป็น `runtime_pass` ได้)
- ทำไมทำได้เลย: **ไม่แตะ hypothesis ledger เลย** ไม่เพิ่ม protocol hypothesis ใหม่
  ไม่ต้องรอ Panya เคาะข้อ M3 → เป็นงานที่เดินหน้าได้ทันทีที่สุดที่เหลืออยู่
- db: `state\pirateforce.sqlite3` (canonical, backpack baseline `[1@0,2@1,4@3]`)
- server args: `-SecondPasswordMode bypass`
- steps:
  1. ตาม PLAYBOOK ข้อ 1 (เปิด server) — ห้ามข้าม Ctrl+C server เก่า
  2. เปิด client ตัวที่ 1 (PLAYBOOK ข้อ 2) → เข้าแมพให้ครบตามข้อ 3–6
  3. **เปิด client ตัวที่ 2 ด้วย job แยก** (ProcessStartInfo เหมือนกัน) โดยที่ตัวแรก
     ยังอยู่ในแมพ → ลอง login/select/เข้าแมพให้ครบ
  4. บันทึกว่าเกิดอะไรขึ้นจริง **ไม่ว่าจะสำเร็จหรือไม่** — ผลลบก็เป็นผลที่มีค่า
     (เช่น ถ้า server ปฏิเสธตัวที่ 2 ให้เก็บข้อความ/พฤติกรรมที่ปฏิเสธมาให้ครบ)
  5. ออกทั้งสองตัว แล้วปิด server เก็บหลักฐาน (PLAYBOOK ข้อ 7–8)
- pass criteria (สำหรับ `runtime_pass`):
  - client ทั้งสองเข้าแมพได้ **หรือ** ตัวที่ 2 ถูกปฏิเสธด้วยพฤติกรรมที่อธิบายได้ชัดเจน
  - `SELECT count(*) FROM sessions WHERE selected_character_id IS NOT NULL` = **2**
    (ห้ามนับ `count(*)` เปล่า — ดูกฎรอบ 11 ใต้ PLAYBOOK) แต่ละแถวมี `opened_at` และ `closed_at` ครบ
    + บันทึก `max(lease_generation)` ก่อน/หลัง และจำนวนแถวที่ `selected_character_id IS NULL` แยกไว้
  - `integrity_check=ok`, `foreign_key_check` ว่าง, backpack ไม่เปลี่ยน
  - server/shim exit 0, stopped marker ×1, stderr 0B, listeners เหลือ 0
- nonclaims: ไม่พิสูจน์ account isolation, remote-player projection, การเห็นกัน
  ในแมพ, combat, หรือ authenticated multi-account access control
- ⚠️ ถ้า client ตัวที่ 2 ทำให้ตัวแรกหลุดหรือ server ล้ม **ให้หยุดทันที เก็บ log
  ให้ครบ แล้วรายงาน** อย่าพยายามซ่อมเอง — นั่นเป็นงานของ chief
- 🔴🔴 **evidence R18 (2026-08-17 10:3x, job 041 — ไม่เปลี่ยนสถานะ แต่อ่านก่อนลงมือ):
  ชั้น wire ตอบแล้ว และคำตอบคือ "ผ่านไม่ได้" · อย่าใช้เวลา attended session กับรายการนี้
  จนกว่า Panya จะเคาะข้อ 14**
  - พิสูจน์สดด้วย 2 connection แบบ headless: connection B **ไม่ได้ถูกปฏิเสธและไม่ได้ถูกเตะ**
    แต่ **ถูกเข้าคิวใน TCP backlog** — รอบนพอร์ต LOGIN **42.1 วิ** พอร์ต GAME **22.1 วิ**
    แล้วถูก `accept()` ภายใน **~30 มิลลิวินาที** หลัง connection A ปิด (จากนั้นตอบถูกทุกไบต์)
  - กลไกยืนยันจากซอร์ส `current/pf_login_game_server_v141.py`: `s.listen(4)` แล้ว
    `accept()` + handle **ในลูปเดียวกัน** ทั้งสอง listener (บรรทัด 7388/7395 และ 7939/7943)
    · **ไม่มี thread ต่อ connection ไม่มี selectors ไม่มี ThreadingTCPServer**
  - → กำแพงอยู่ที่ชั้น `accept()` ซึ่งอยู่**ก่อน**ที่ไบต์ของ client จะมีความหมาย
    **GameClient จริงสองตัวจะให้ผลเดียวกัน** ตัวที่สองจะค้างเงียบจนตัวแรกออก
  - ⚠️ **pass criteria ข้อ `count(*) WHERE selected_character_id IS NOT NULL = 2`
    ตอนนี้รู้แล้วว่าไปไม่ถึงโดยโครงสร้าง** — ต้องเขียนเกณฑ์ใหม่ก่อนรัน ไม่ใช่รันแล้วค่อยรู้
    (ของจริงที่วัดได้: 3 แถว แต่ `IS NOT NULL` = 2 โดยแถวที่ 3 ของ B เป็น `char NULL`)
  - ยังเหลือชั้น **client-observable** ที่ต้องมี Panya: *ตัวที่สองแสดงอะไรบนหน้าจอ*
    (ค้างหน้าโหลด / error / timeout) — nonclaim ข้อ 1 ของ R18
  - รายละเอียด + ตัวเลือก ก–ง ของ **ข้อ 14 (ใหม่)**:
    `pf_bridge\FINDINGS_R18_SERVER_IS_STRICTLY_SERIAL.md`
- result: (รอ — แต่ชั้น wire/DB ตอบแล้วว่า NEGATIVE ดู evidence R18)



<!-- ===== GT-005 [PASS ✅ 12:23 — processed] | บรรทัดเดิม 648-855 ===== -->

## GT-005 movement position persistence — เดินแล้วตำแหน่งอยู่ข้าม restart  [PASS] ✅ 2026-08-17 12:23–12:41
> ✅ **ประมวลผลและ commit แล้วโดยรอบ 25 (12:53–13:0x)** — ปิดวงจร "ผลเทสกรอกในคิว → รอบถัดไปประมวล/commit"
> - รายงานใน repo: `reports\PF_GT005_MOVEMENT_POSITION_PERSISTS_ACROSS_RESTART_RUNTIME_PASS_20260817.md`
>   + `.manifest` (format A, 23 ไฟล์, ok=23 missing=0 mismatch=0)
> - matrix: `local_player_position_checkpoint` `in_progress` → **`runtime_pass`** ·
>   domain `movement` ยัง INCOMPLETE (next = `local_player_movement_authority`)
> - commit `7c067b4` (5 ไฟล์: report, manifest, FUNCTIONAL_COVERAGE.json, ROADMAP_TO_PLAYABLE.md, .gitignore)
>   · dirty diff 6 บรรทัดเดิมไม่ถูกแตะ · tag `pf-backup-dirty-20260817_031958` ยังอยู่
> - รอบ 25 ตรวจหลักฐานซ้ำเองแบบอิสระ (ไม่ลอกจาก FINDINGS_R24): DB sha `F37BEFE6..95C8` ·
>   แถว position ตรง · console boot1 มี `TargetPosVital` 29 เฟรม = ที่ฝั่ง client capture นับได้ 29 ·
>   `START_GAME_RES` 418B บูตละ 1 ครั้ง · `[FOUNDATION] stopped` บูตละ 1 · stderr 0B ทั้งคู่
> - แก้ตัวเลขที่ต้องระวัง: job 048 พิมพ์ `stderr = -1 bytes` = sentinel "ยังไม่มีไฟล์" ไม่ใช่ค่าจริง
>   ค่าที่ถูกคือ 0 bytes จาก job 050 (ไฟล์บนดิสก์วันนี้ = 0 ไบต์จริง)
- objective: **หนึ่ง claim เดียว** — ตำแหน่งที่ผู้เล่น *เดินไปจริง* ถูก checkpoint ลง DB
  และเมื่อปิด server แล้วเปิดใหม่ เข้าเกมอีกครั้ง ตัวละครเกิดที่ตำแหน่งใหม่นั้น
  (แถว `local_player_position_checkpoint` ใน domain `movement` ตอนนี้เป็น `in_progress`
  เพราะ FND-010 พิสูจน์แค่ว่าตำแหน่ง **ไม่เปลี่ยน** ข้าม abrupt loss —
  ยังไม่มีหลักฐานว่าตำแหน่งที่ *เปลี่ยนแล้ว* รอด)
- ทำไมคุ้มที่สุดตอนนี้: โค้ดมีอยู่แล้วครบ (`runtime._checkpoint_exact_target` →
  `lifecycle.checkpoint` → `store.save_position`)
  ⚠️ **แก้ข้อความเดิมที่ผิด (รอบ 20):** เดิมเขียนว่า *"`lifecycle.exit` เซฟอีกครั้งตอนออก"*
  — **ไม่จริง** server เรียก `close_connection()` ซึ่ง docstring เขียนเองว่า
  *"close this exact lease **without rewriting its last position**"* · `session.close(position)`
  ที่เซฟตอนออก **ไม่ถูกเรียกจาก server เลย มีแต่ใน test**
  → **ตำแหน่งถูกบันทึกระหว่างเล่นเป็นราย `TargetPos` เท่านั้น ไม่มี "เซฟตอนออก" เป็นตาข่ายรอง**
  → ดังนั้น **ขั้นตอนที่ 3 (เดินให้ไกล) คือขั้นที่ขาดไม่ได้จริง ๆ** ถ้าไม่เดิน จะไม่มีอะไรถูกเขียน
  **ไม่ต้องเขียนโค้ดใหม่ ไม่แตะ hypothesis ledger ไม่ต้องรอ Panya เคาะ**
  ถ้าผ่าน = ยกแถวเป็น `runtime_pass` ได้ทันที ถ้าไม่ผ่าน = เจอบั๊กจริงที่คุ้มค่ากว่าอีก
- db: `state\pirateforce.sqlite3` (canonical, backpack baseline `[1@0,2@1,4@3]`)
  ⚠️ **ก่อนเริ่ม ให้ job copy DB ไปเก็บไว้ก่อน**
  `pf_bridge\backup\pirateforce_before_gt005_<yyyyMMdd_HHmmss>.sqlite3`
  (เทสนี้ **ตั้งใจ** ให้ตำแหน่งใน canonical DB เปลี่ยน — backpack ต้องไม่เปลี่ยน
  guard `is_unmoved_baseline` ดูแค่ backpack ตำแหน่งเปลี่ยนไม่กระทบ)
- server args: `-SecondPasswordMode bypass`
- steps:
  1. job: copy DB สำรองตามข้างบน + **อ่านตำแหน่ง BEFORE** ด้วย read-only connection
     **query ที่ตรวจชื่อคอลัมน์จาก `migrations/001+002` แล้ว ใช้ได้เลย ห้ามเดาเอง:**
     ```sql
     SELECT c.id, c.name, p.scene_id, p.scene_seq, p.x, p.y, p.z, p.heading, p.updated_at
     FROM characters c JOIN character_positions p ON p.character_id = c.id;
     ```
     (ตาราง `character_positions` มีคีย์เป็น `character_id`; `heading` มาจาก
     migration 002 — บทเรียนจาก job 016 ที่ query พังเพราะเดาว่าเป็น `generation`
     ทั้งที่จริงคือ `lease_generation`)
  2. เปิด server + client เข้าแมพให้ครบตาม PLAYBOOK ข้อ 1–6
     จดพิกัดที่มุมจอตอนเพิ่งเข้า (เช่น `X:-9038 Y:-2866`) = **UI BEFORE**
  3. **เดินให้ไกลชัดเจน** (คลิกพื้นไปทิศเดียวกันหลายครั้ง หรือกดปุ่มเดินค้าง)
     ให้พิกัดบนจอเปลี่ยนอย่างน้อยหลักพันหน่วยจากจุดเริ่ม → จด **UI AFTER**
     ⚠️ อย่าเดินเข้าไปชน NPC/ประตู/ท่าเรือ ให้เดินในที่โล่ง
  4. ออกจากเกมให้สะอาดตาม PLAYBOOK ข้อ 7 (X ครั้งเดียว → ยืนยัน)
  5. job: ปิด server (Ctrl+C หนึ่งครั้ง) รอ exit 0 ทั้ง shim และ server
     แล้ว **อ่านตำแหน่ง AFTER** จาก DB ด้วย read-only connection
  6. **เปิด server ใหม่ + client ใหม่** เข้าเกมอีกรอบ → จดพิกัดตอนเพิ่งเข้า
     = **UI RESPAWN**
  7. ออก + ปิด server + เก็บหลักฐานตาม PLAYBOOK ข้อ 7–8
- pass criteria (สำหรับ `runtime_pass`):
  - DB AFTER ≠ DB BEFORE และค่า x/y ตรงกับ **UI AFTER** อย่างมีเหตุผล
    (คลาดเคลื่อนได้เล็กน้อยเพราะ checkpoint ล่าสุดคือ target ล่าสุด ไม่ใช่ทุกเฟรม)
  - **UI RESPAWN ≈ UI AFTER** (ไม่ใช่ UI BEFORE) ← นี่คือหัวใจของ claim
  - `integrity_check=ok`, `foreign_key_check` ว่าง, **backpack ยัง `[1@0,2@1,4@3]`**
  - แถวใหม่ที่ `selected_character_id IS NOT NULL` = **2 แถว** (รอบละแถว) เปิด-ปิดครบทั้งคู่
    (ห้ามนับ `count(*)` เปล่า — ดูกฎรอบ 11 ใต้ PLAYBOOK; บันทึก `max(lease_generation)` ก่อน/หลังด้วย)
  - server/shim exit 0 ทั้งสองรอบ, stopped marker รอบละ 1, stderr 0B, listeners 0
- nonclaims: ไม่พิสูจน์ heading/facing ที่ถูกต้อง, ไม่พิสูจน์ movement validation
  (server ยังรับพิกัดที่ client บอกมาดื้อ ๆ — นั่นคือแถว
  `local_player_movement_authority` ที่ยัง `not_started`), ไม่พิสูจน์ข้ามแมพ,
  ไม่พิสูจน์ว่า checkpoint เกิดทุกเฟรมหรือทุกก้าว
- ⚠️ ถ้า UI RESPAWN กลับไปที่จุดเดิม (UI BEFORE) = **ผลลบที่มีค่ามาก** ให้บันทึกให้ครบ
  แล้วรายงาน อย่าพยายามแก้โค้ดเอง — `src/` มี WIP ของ M3 ค้างอยู่ ห้ามแตะ
- **evidence R19 (2026-08-17 10:5x, job 042 — ไม่เปลี่ยนสถานะ `PENDING`):**
  รอบ 19 วัดครึ่งหลังของเทสนี้ (restart) แบบ headless ไปแล้ว **และมันผ่าน**
  - 🟢 **บูต server สองครั้งบนไฟล์ DB เดียวกันได้จริง** — boot B บนฐานที่มีประวัติ session
    ให้ transcript **เหมือน boot A ทุกโหมด (31/20/39 บรรทัด)** และยัง
    **ตรงกับ GameClient จริง (events-only 20/20 exit 0)**
  - 🟢 **`lease_generation` เดินต่อข้ามโปรเซส** 1→2→3 (คนละ pid) = มาจาก DB ไม่ใช่หน่วยความจำ
  - 🟢 **เกณฑ์ข้อ "แถวใหม่ `IS NOT NULL` = 2 แถว เปิด-ปิดครบ" ผ่านล่วงหน้าแล้ว**
    (restart DB มี 2 แถวใหม่ `closed_at` ครบทั้งคู่, `open sessions = 0`, `integrity ok`)
  - 🔴 **แต่ครึ่งแรกมีปัญหาเรื่องการตีความ:** เทียบสำเนา DB กับ canonical ทีละแถวทุกตาราง
    → **มีตารางเดียวจาก 7 ที่เปลี่ยน คือ `sessions`** · `character_positions`
    **ไม่ขยับเลย** ทั้งใน reconnect และ restart
    (nonclaim: replay หยุดที่ `TeleportVital` **ไม่เคยส่ง `TargetPosVital`** = ไม่เคยเดิน
    ดังนั้นนี่คือ *"เส้นทางเข้าเกมไม่เขียนตำแหน่ง"* ไม่ใช่ *"ตำแหน่งไม่เคยถูกบันทึก"*)
  - ⚠️ **ผลกระทบต่อการรันเทสนี้:** ถ้า Panya เดินแล้ว DB ไม่เปลี่ยน จะ **แยกไม่ออก**
    ว่าเป็น "ฟีเจอร์ไม่ทำงาน" หรือ "ขั้นตอนการเดินยังไม่ได้ trigger checkpoint"
    → **ข้อ 16 ใหม่:** ให้ chief ส่ง `TargetPosVital` ชั้น wire แล้ววัด `character_positions`
    ก่อน (~10 นาที) จะทำให้ผลของ attended session ตีความได้ทันที
    **chief ไม่ทำเองเพราะเป็นการส่ง vital ชนิดใหม่ = อาจเข้าข่ายเปิด milestone**
    เหตุผลเต็ม: `pf_bridge\FINDINGS_R19_RECONNECT_AND_RESTART_WORK_NOTHING_PERSISTS.md`
- **evidence R20 (2026-08-17 11:2x, job 043 — ไม่เปลี่ยนสถานะ `PENDING`):**
  🟢 **คำเตือน "แยกไม่ออก" ของ R19 ข้างบนคลี่คลายไปมากแล้ว โดยไม่ต้องส่งเฟรมใหม่เลย**
  รอบ 20 ไม่บูต server ไม่เปิด socket — ใช้ static analysis + audit corpus + เทสที่มีอยู่แล้ว
  - 🟢 **เส้นทางเขียนตำแหน่งมีอยู่จริงและ active ในโหมดที่เทสนี้จะใช้**
    `runtime.py:638-645` มีเงื่อนไขแค่ `scene_load_scenario is None` +
    `durable_target is not None` + `selected is not None` — **ไม่มีเงื่อนไข
    `runtime_ack`/`teleport`** · และ `tools\run_foundation_visible.ps1` ส่งแค่
    `--db --capture-root --second-password-mode` → **ไม่มี scenario flag ใด ๆ**
    = เงื่อนไขแรกเป็นจริงเสมอ
  - 🟢 **เฟรม `TargetPosVital` ของ client จริง ผ่าน parser ของ server ครบ 435/435 = 100%**
    (reject **0**) จาก 58 capture log ของวันที่ 15–16 ส.ค. · จำลองเงื่อนไข
    `candidate != selected.position` แล้ว → **จะเรียก `save_position()` 346 ครั้ง**
    → **VERDICT: WRITES REACHABLE**
  - 🟢 **cross-check ที่แข็งที่สุด:** ไบต์ `pc` ที่ไม่ซ้ำ = **315** (ตรงกับรอบ 16 เป๊ะ)
    และ `(x,y,z,heading,moving)` ที่ไม่ซ้ำ = **315** เท่ากัน
    → parser มองเห็นทุกไบต์ที่แปรผันจริงในเฟรมชนิดนี้ ไม่มีฟิลด์ซ่อน
  - 🟢 **มี unit test ครอบเส้นทางนี้อยู่แล้วและเขียวจริงวันนี้บน Windows `py -3`**
    `tests/test_foundation.py:124 test_real_v141_dispatch_lifecycle` สร้าง state
    **โดยไม่ใส่ scenario** แล้ว dispatch `TargetPos` จริง → assert ว่า DB เปลี่ยนตามค่าที่ส่ง
    · `test_exit_restart_load_position` พิสูจน์ว่าค่ากลับมาหลังเปิด store ใหม่
    **และถูกฉีดเข้าไบต์ `start_game` ที่ส่งให้ client** · รวม **53 tests เขียว exit 0**
  - ➡️ **แปลว่า:** ถ้าเทสนี้ FAIL สาเหตุที่เหลือ **ไม่น่าใช่ "ฟีเจอร์ไม่มี"** แต่เป็นชั้น client
    (client ไม่ส่ง `TargetPos` เพราะเดินไม่ได้จริง) หรือชั้น session
    (guard `EXISTS(... closed_at IS NULL)` ใน `store.py:215` ไม่ผ่าน)
    → **ให้จดไว้ด้วยว่าเดินแล้วพิกัดบนจอเปลี่ยนจริงหรือไม่** เพราะนั่นคือตัวแยกสองสาเหตุนี้
  - ⚠️ nonclaim: ทั้งหมดนี้เป็นชั้น **wire/DB + โค้ด** — **ยังไม่มีการรัน end-to-end จริง
    บน server ที่บูตอยู่สักครั้ง** และไม่พิสูจน์ว่าหน้าจอจะแสดงตัวละครที่ตำแหน่งเดิม
    เหตุผลเต็ม + nonclaims 10 ข้อ:
    `pf_bridge\FINDINGS_R20_POSITION_WRITE_PATH_EXISTS_AND_IS_REACHABLE.md`
- **evidence R21 (2026-08-17 11:4x, job 044 — ไม่เปลี่ยนสถานะ `PENDING`):**
  **ลายเซ็นของความล้มเหลวแบบที่สอง — ถ้าเห็นแบบนี้ให้จดไว้ว่าเป็นชั้น session ไม่ใช่ client**
  - `_checkpoint_exact_target` (`runtime.py:290`, เรียกจาก `645`) เป็น **DB write ทางเดียว
    ใน `dispatch` ที่ไม่มี `try/except` ครอบ** และ `v141.py:7440` เป็น `try/finally`
    **ไม่มี `except`** → ถ้า `save_position` raise `PermissionError` (`store.py:216`)
    จะไหลถึง `shutdown.py:268-269` → `request_stop("server thread failure")`
    = **หน้าต่าง server ปิดทั้งตัวทันทีที่เดินก้าวแรก** พร้อม traceback
  - 🟢 **แต่ไม่ควรเกิดในเทสนี้:** เงื่อนไขเดียวที่ทำให้ `rowcount != 1` คือมี session ใหม่
    ของ account เดียวกันมาปิด lease เก่า (`store.py:136`) ซึ่งเกิดเฉพาะตอนรับ GAME
    connection ใหม่ — และ **loop แบบ serial ของรอบ 18 กันไว้อยู่ ถ้าเปิด client ตัวเดียว**
  - ➡️ **สิ่งที่ต้องจดถ้าเจอ:** *server ปิดเอง* = ชั้น session (lease ถูกแย่ง) ·
    *server ยังอยู่แต่ DB ไม่เปลี่ยน* = ชั้น client (ไม่ได้ส่ง `TargetPos`)
    → สองอาการนี้แยกกันได้ด้วยตาเปล่า **ห้ามเปิด GameClient ค้างไว้สองตัวระหว่างเทสนี้**
  - เหตุผลเต็ม: `pf_bridge\FINDINGS_R21_BACKPACK_WRITES_ARE_ONE_SHOT_AND_DISPATCH_IS_UNGUARDED.md`
- **evidence R22 (2026-08-17 11:5x, job 045 — ไม่เปลี่ยนสถานะ `PENDING`) ⭐ ข้อ 16 ทำแล้ว:**
  🟢🟢 **ชั้น wire/DB ของเทสนี้ผ่านแล้วจริง ๆ ด้วยการวัด ไม่ใช่การอ่านซอร์ป**
  chief ส่ง `TargetPosVital` ลงสายบน server ที่บูตอยู่ **สองแขนอิสระ** (สำเนา DB คนละใบ)
  - แขน A: entry ของ capture canonical + splice เฟรม `TargetPosVital` 9 เฟรมจาก
    `capture_v134\GAME_20260815_041348_421522_49804.txt` (#20–#28)
  - แขน B: replay capture นั้น **ทั้งไฟล์ 50 เฟรม ไม่ splice**
  - **ผลตรงกันเป๊ะทั้งสองแขน:**
    `BEFORE (-9098.5508, -2866.8618, 186.0, h=2.994371)`
    → `AFTER (-4529.2061, -3245.6492, 194.0, h=0.09852)` = **เฟรมสุดท้ายที่ส่ง ตรงทุกหลัก**
    · `updated_at` ตรงวินาทีที่เฟรมออกจากสาย · ค่ายังอยู่หลังปิด server
  - 🟢 **server ไม่ดับ** `process_alive=True listeners=2` · `stderr 0B` ทั้งสองแขน
    → **ลายเซ็นความล้มเหลวของ R21 (server ปิดเอง) ไม่เกิดกับ client ตัวเดียวจริง ๆ**
  - 🟢 `sessions` +1 แถวต่อการต่อ · `lease_generation` เดินเป็น 2 · **`closed_at` ถูกตั้ง
    ตอนสายหลุด** (`open sessions = 0`) · `integrity ok` · canonical DB sha ไม่ขยับ
  - 🔴 **N สำคัญต่อวิธีตัดสินเทสนี้: transcript ฝั่ง server ไม่พูดถึงการเขียนตำแหน่งเลย**
    (`checkpoint|position` markers = **0** ใน `GAME_LIVE.txt`)
    → **ห้ามใช้ console/transcript ตัดสินว่าเขียนหรือไม่ ต้องอ่าน DB เท่านั้น**
  - ➡️ **แปลว่าตอนนี้เทสนี้เหลือคำถามเดียวจริง ๆ:** *GameClient จริงส่ง `TargetPosVital`
    ตอน Panya เดินหรือไม่* ถ้าเดินแล้ว DB ไม่ขยับ = **ชั้น client ล้วน ๆ** ไม่ใช่ฟีเจอร์ขาด
    ไม่ใช่ session (สองชั้นนั้นถูกตัดออกด้วยการวัดแล้ว)
  - ⚠️ nonclaim: ยังไม่ได้พิสูจน์ครึ่งหลัง (boot ใหม่แล้วตัวละคร **เกิด** ที่พิกัดใหม่บนจอ)
    และไม่ได้นับจำนวนครั้งที่เขียน (วัดได้แค่ค่าสุดท้าย)
  - เหตุผลเต็ม: `pf_bridge\FINDINGS_R22_TARGETPOS_ON_THE_WIRE_WRITES_THE_ROW.md`
- **evidence R23 (2026-08-17 12:1x, job 046 — ไม่เปลี่ยนสถานะ `PENDING`) ⭐ ครึ่งหลังปิดแล้ว:**
  🟢🟢 **ค่าที่เซฟไว้ "เดินทางกลับออกไปหา client" จริง ข้ามการรีสตาร์ทของโปรเซส**
  รอบ 22 พิสูจน์ว่า server **เขียน** ได้ · รอบนี้พิสูจน์ว่า server **อ่านกลับออกไปให้ client**
  2 boot บนไฟล์ DB **ใบเดียวกัน** (boot 1 อ่าน baseline แล้วเดิน → boot 2 โปรเซสใหม่ อ่านซ้ำ)
  - `START_GAME_RES` (ตอบ `StartGameReq`, 32B เข้า → 418B ออก) พก quadruple
    `f32(x) f32(y) f32(z) f32(heading)` ของแถวที่เซฟไว้ ที่ offset 234 ของ container
  - **probe A** (ก่อนเดิน, คาด baseline) = **HIT** `[-9098.5508, -2866.8618, 186.0, 2.9944]`
  - **probe B** (หลังรีสตาร์ท, คาดค่าใหม่) = **HIT** `[-4529.2061, -3245.6492, 194.0, 0.0985]`
  - **probe C** (negative control — ค่าเก่ายังอยู่ไหม) = **MISS** → ค่าเก่าหายจากสายจริง
  - วิธีตัดสินไม่พึ่ง parser: `f32tag` = `0x2A`+LE float ตรง ๆ จึงคำนวณ 20 ไบต์จาก DB
    แล้ว **ค้นเป็น substring ดิบ** ใน container ที่ snappy-decompress แล้ว
  - ขนาดเฟรม/ออฟเซ็ตไม่ขยับทั้งสามครั้ง — **เปลี่ยนแค่ 16 ไบต์ของค่าพิกัด**
  - `boot1_alive=True boot2_alive=True` · stderr 0B ทั้งสอง boot · `open sessions = 0`
    (5 sessions ปิดครบ ไม่รั่ว) · `integrity ok` · canonical sha ไม่ขยับ · stray = 0
  - 🔴 **N1 ที่ต้องจำก่อนเทสจริง (inference จากซอร์ส ยังไม่ได้วัดไบต์):**
    `runtime.py:466` ส่งเฟรมที่ **สอง** ตามหลัง `START_GAME_RES` ทันที คือ
    `legacy.make_login_teleport(1, 0)` ซึ่ง default `x=y=z=0.0` (`v141.py:2431`)
    **ไม่สนใจตำแหน่งที่เซฟเลย** (สาขาที่ใช้ค่าจริงคือ `runtime.py:461` = เฉพาะ scene_load)
    → **client ได้เฟรมพูดถึงตำแหน่งสองเฟรมติดกันที่ไม่ตรงกัน**
    ➡️ **ถ้าเทสจริงแล้วตัวละครโผล่ผิดที่ทั้งที่ DB ถูก — สงสัยเฟรมนี้ก่อนเสมอ
       อย่าไปไล่หาบั๊ก persistence ที่ไม่มีอยู่จริง**
  - ⚠️ nonclaim: probe เข้าเกมด้วย capture frames ไม่ใช่ GameClient จริง →
    พิสูจน์ได้แค่ว่า **server ส่งอะไรออกไป** ไม่ได้พิสูจน์ว่า **client วาดตรงไหน**
  - เหตุผลเต็ม: `pf_bridge\FINDINGS_R23_PERSISTED_POSITION_REACHES_THE_CLIENT.md`
- result: ✅ **PASS ทุกเกณฑ์ (runtime_pass) — attended session 2026-08-17 12:23–12:41**
  ผู้ขับ: Claude (สิทธิ์ tier full — Panya กด Allow 12:25 ขณะหน้าต่างเกมเปิดอยู่) ·
  Panya อยู่หน้าเครื่องตลอด · jobs `047`→`048`→`049`→`050`
  - **ชั้น client-observable (ตาเห็นจริงทุกจุด):**
    - UI BEFORE  = Port Royal `X:-9,098 Y:-2,866` (ตรง DB baseline)
    - เดินจริงด้วยการคลิกพื้น (คลิกขวา = หมุนกล้อง 180° — จดไว้ใช้รอบหน้า)
    - UI AFTER   = Port Royal `X:-8,094 Y:-3,207` (ΔX > 1,000 หน่วยจากจุดเริ่ม)
    - ออกสะอาด X ครั้งเดียว → ยืนยัน → ปิด server → **บูตใหม่ + client ใหม่**
    - **UI RESPAWN = Port Royal `X:-8,094 Y:-3,207` = UI AFTER เป๊ะ ไม่ใช่ UI BEFORE** ← หัวใจของ claim
    - ภาพหลักฐาน 7 ไฟล์ใน `pf_bridge\evidence_screens\gt005_*.jpg`
  - **ชั้น wire/DB:**
    - DB AFTER round 1 = `(-8094.60791015625, -3207.83056640625, 186.0, h=2.4993)`
      **ตรงกับ UI AFTER หน่วยต่อหน่วย** · updated_at = 05:32:03Z (ระหว่างเดิน)
    - GAME_LIVE.txt ของ boot 1: **TargetPos mentions = 29** → GameClient จริง
      ส่ง `TargetPosVital` ตอนเดินจริง — **คำถามเดียวที่เหลือของ R22 ตอบแล้ว**
    - DB FINAL หลัง boot 2 = ค่าเดิม (ไม่เดินรอบสอง) · integrity ok · fk ว่าง
    - sessions `IS NOT NULL`: 1 → **3** (+1 ต่อรอบ ครบสองรอบ) เปิด-ปิดครบ (`open = 0`)
      · lease_generation 1→2→3 · backpack updated_at **ไม่ขยับ** (2026-08-16T10:30Z)
    - server/shim exit 0 ทั้งสองรอบ · stopped marker รอบละ 1 · stderr 0B ทั้งคู่ · listeners 0
  - 🟢 **ของแถมสำคัญ: N1 ของรอบ 23 (เฟรม teleport (0,0,0)) ปิดที่ชั้น client แล้ว** —
    ตัวละครเกิดที่ตำแหน่งที่เซฟไว้ทั้งสองรอบ ไม่ได้ถูกดีดไป (0,0,0)
    → เฟรม teleport hardcoded ไม่มีผลที่ตาเห็น (เหตุผลที่แท้จริงยังไม่วัด — ดู nonclaim)
  - ⚠️ **canonical sha เปลี่ยนโดยตั้งใจ** (ตำแหน่งใหม่ถูกเขียน):
    เดิม `673F4BFB..9708` → ใหม่ `F37BEFE6CFFC967DA7F8BF954F5554363D5FA1517FF5F7D6B6BFAFFA3CB795C8`
    baseline เดิม park ที่ `pf_bridge\backup\pirateforce_before_gt005_20260817_122339.sqlite3`
    → **job ใดที่ gate ด้วย CANON_SHA ต้องอัปเดตค่าใหม่ก่อนใช้**
  - nonclaim: ไม่พิสูจน์ heading บนจอ (DB เก็บ 2.4993 แต่ไม่มีตัวเลข heading ใน UI ให้เทียบ) ·
    ไม่พิสูจน์ว่า client "ไม่สน" เฟรม teleport เพราะอะไร · ไม่พิสูจน์ movement validation ·
    ไม่พิสูจน์ข้ามแมพ · จำนวน checkpoint ต่อการเดินยังไม่นับ (วัดได้แค่ค่าสุดท้าย)



<!-- ===== GT-006 [DONE ✅ observation ครบ] | บรรทัดเดิม 856-1138 ===== -->

## GT-006 chat input observation — พิมพ์ในช่องแชทแล้วมีอะไรวิ่งบนสายไหม  [DONE] ✅ observation ครบ 2026-08-17 14:37–14:38 · ประมวลผลแล้วรอบ 33 (commit `eb6fef0`)
- objective: **สังเกตอย่างเดียว ไม่แก้โค้ด** — พิมพ์ข้อความในช่องแชทของ client
  แล้วดูว่า server ได้รับ frame อะไรหรือไม่
  (แถว `client_chat_input` ใน domain `chat` เป็น `not_started` เพราะ
  **ยังไม่เคยมีใครลองด้วยซ้ำ** — เทสนี้ราคาถูกที่สุดในคิวและได้ข้อมูลใหม่แน่นอน
  ไม่ว่าผลจะออกทางไหน)
- db: `state\pirateforce.sqlite3`
- server args: `-SecondPasswordMode bypass`
- steps:
  1. เข้าเกมตาม PLAYBOOK ข้อ 1–6 (ทำต่อจาก GT-005 รอบที่สองได้เลย ประหยัดเวลา)
  2. คลิกช่องแชทมุมซ้ายล่าง พิมพ์ข้อความ **ASCII ล้วน** ที่หาง่ายใน log เช่น
     `PFCHATPROBE1` แล้วกด Enter
  3. รอ 3 วิ พิมพ์อีกครั้งด้วยข้อความสั้นกว่า `PFCHATPROBE2` กด Enter
  4. ออก + ปิด server + เก็บหลักฐาน
- pass criteria: **ไม่มีเกณฑ์ PASS/FAIL** — นี่คือ observation
  ให้รายงานสิ่งเหล่านี้ครบ:
  - UI แสดงข้อความที่พิมพ์กลับมาในช่องแชทหรือไม่ (client echo เองก็เป็นไปได้)
  - ใน `server_console_live.out.txt` มี frame/vital ใหม่โผล่ตอนกด Enter หรือไม่
    (เทียบ timestamp กับตอนที่พิมพ์) — ถ้ามี ให้ copy บรรทัดนั้นมาทั้งหมด
  - ถ้ามี raw packet log ให้ระบุ path ไว้ (chief จะ decode เอง ห้าม decode มั่ว)
- nonclaims: ไม่พิสูจน์ protocol id, ไม่พิสูจน์ว่า server ควรตอบอะไร,
  ไม่พิสูจน์ channel/whisper — **ห้ามตั้งชื่อ semantic ให้ค่าดิบใด ๆ**
- result: ✅ **observation ครบทุกข้อ — attended 2026-08-17 14:37–14:38
  (รันต่อท้าย GT-001 ในเซสชันเกมเดียวกัน ประหยัดเวลาตามที่ steps แนะ)**
  - **UI:** คลิกช่องแชท → พิมพ์ `PFCHATPROBE1` (ยืนยันด้วย zoom: ข้อความอยู่ในช่อง + caret)
    → Enter → ช่อง input เคลียร์ แต่ **ไม่มีข้อความใด ๆ โผล่ในหน้าต่างแชท**
    (ไม่มี client echo · ไม่มี error · เห็นแต่บรรทัด [ระบบ] เดิม) ·
    `PFCHATPROBE2` ทำแบบตรวจก่อนกดอีกครั้ง 14:38 → ผลเหมือนกันทุกอย่าง
  - ⚠️ note จังหวะที่มีค่า: ความพยายามส่ง PROBE2 *ครั้งแรก* (พิมพ์ทันทีหลัง Enter แรก
    โดยไม่คลิกช่องใหม่) **ไม่เกิดอีเวนต์บนสายเลย** — สอดคล้องกับ "focus หลุดหลังส่ง"
    (keystrokes น่าจะกลายเป็น hotkey) → บนสายจึงมี 2 อีเวนต์ ไม่ใช่ 3 ·
    บทเรียนรอบหน้า: คลิกช่องแชทใหม่ทุกครั้งก่อนพิมพ์
  - **wire (fact ดิบ — ไม่ตีความ semantic):** `GAME_EVENTS_LIVE.txt` จับได้ 2 อีเวนต์
    ตรงเวลากด Enter พอดี ทั้งคู่ id `0xAC52` (**UNKNOWN ต่อ registry ของ server**) payload 34B:
    - 14:37:53.848 frame=56:
      `48000000004818000000500046004300480041005400500052004F00420045003100`
    - 14:38:33.926 frame=87:
      `48000000004818000000500046004300480041005400500052004F00420045003200`
    - ข้อสังเกตระดับไบต์ (นับได้จากตาราง hex ไม่ใช่การ decode): 24 ไบต์ท้าย =
      รหัสตัวอักษรที่พิมพ์สลับ `0x00` ทีละไบต์ (P=50,F=46,C=43,… ต่างกันแค่ท้าย 31/32) ·
      prefix 10 ไบต์เหมือนกันทั้งสองเฟรม: `48 00 00 00 00 48 18 00 00 00`
    - server **ไม่ตอบเฟรมใด ๆ กลับ** (id UNKNOWN) → สอดคล้องกับการไม่มี echo บน UI
    - เหตุที่ 061 grep ASCII `PFCHATPROBE` ได้ 0 ทุกไฟล์: ข้อความบนสายแทรก 0x00
      (ไม่ใช่ ASCII ต่อเนื่อง) — **ไม่ใช่ว่าไม่มีเฟรม** อย่าสรุปผิดจากเลข 0 นี้
  - raw packet log (chief decode เอง): `GameClient\capture_gt001_20260817_143122\capture_v141\`
    → `GAME_EVENTS_LIVE.txt` (seq=2,3) + `GAME_20260817_143546_708289_57440.txt` (raw เต็ม)
  - ผลกระทบต่อ matrix (ให้ chief ตัดสิน): แถว `client_chat_input` domain `chat` มีข้อมูลจริง
    ครั้งแรก — client ส่งเฟรมจริงตอนกด Enter แต่ server ยังไม่รู้จัก id นี้

- **evidence R26 (2026-08-17 13:1x — ไม่เปลี่ยนสถานะ `PENDING`):**
  รอบ 26 เช็ก `mcp__computer-use__list_granted_applications` แล้ว = `allowedApps: []`
  (สิทธิ์ว่างเหมือนเดิม ไม่ติดตัว task) และ **ไม่เรียก `request_access`** โดยตั้งใจ
  เหตุผลตามกฎที่พิสูจน์แล้วในไฟล์ CHIEF: ขอสิทธิ์ตอนหน้าต่างเกมไม่ได้เปิด
  → ระบบตอบ `notInstalled` เงียบ ๆ ไม่มี dialog ขึ้นให้ Panya กด = เผาโอกาสฟรี
  และรอบนี้ **เปิดเกมไม่ได้** เพราะ bridge console ปิดอยู่ (job `051_r25_gates.ps1`
  ยังค้างใน inbox ตั้งแต่ 12:57 ไม่มี `outbox\051_r25_gates.out.txt`)
  → **ของที่ต้องให้ Panya ทำเพื่อปลดล็อก GT ทั้งคิว: เปิด `pf_bridge\pf_bridge.ps1`
  ค้างไว้หนึ่งหน้าต่าง แล้วรอกด Allow ตอน dialog ขึ้น** (สองอย่างนี้เท่านั้น)

- **evidence R27 (2026-08-17 13:28–13:33, job 053 — ไม่เปลี่ยนสถานะ `PENDING`) 🔴🔴 คำตอบชี้ขาดของข้อ 16:**
  รอบนี้ทำสิ่งที่ทุกรอบก่อนหน้าทำไม่ได้ คือ **เปิดเกมจริงก่อนแล้วค่อยขอสิทธิ์**
  (bridge เปิดอยู่ → job 053 บูต server `shim=12528 server=13672` + เปิด client
  `pid=15348` ได้หน้าต่างชื่อ `'Pirate Force'` ยืนยันจาก `MainWindowTitle`)
  แล้วเรียก `mcp__computer-use__request_access(["GameClient.local.bin"])`
  **ผลที่ได้ไม่ใช่ `notInstalled` และไม่ใช่ dialog** แต่เป็นข้อความปฏิเสธเชิงนโยบายตรง ๆ:

  > Computer-use access to "GameClient.local.bin" can't be approved during a scheduled
  > run. To grant it, send a message in this conversation (the approval card will appear),
  > or add the app to the scheduled task's settings. (Retrying returns this same result.)

  🔴 **สมมติฐานเดิมถูกหักล้าง** — เดิมเชื่อว่า "ขอตอนหน้าต่างเกมปิด = notInstalled เงียบ
  ถ้าเปิดเกมค้างไว้แล้วขอ Panya จะได้กด Allow" **ผิด** หน้าต่างเปิดอยู่จริงและก็ยังถูกปฏิเสธ
  → เหตุผลไม่เกี่ยวกับหน้าต่างเลย แต่เป็นเพราะ **เป็น scheduled run**
  → คำแนะนำใน LOCK รอบ 26 ที่บอก Panya ว่า "รอกด Allow ตอน dialog ขึ้น"
    **ใช้ไม่ได้ ไม่มี dialog ไหนจะขึ้นระหว่าง scheduled run เลย** และ
    ข้อความบอกเองว่า **retry ได้ผลเดิม** → ห้ามลองซ้ำทุกรอบ เผา token ฟรี

  ✅ **เหลือทางเดียวสองแบบ (ทั้งคู่ต้องให้ Panya ทำ):**
  - **(ก) ถาวร — ที่ควรทำ:** เพิ่ม `GameClient.local.bin` ลงใน **settings ของ
    scheduled task `pirate-force-chief-continue`** (ช่องรายการแอปสำหรับ computer use)
    → รอบต่อ ๆ ไปเทสในเกมเองได้แม้ Panya หลับ = ปลดล็อก GT-001/003/006 ทั้งคิวถาวร
  - **(ข) ชั่วคราว:** Panya พิมพ์ข้อความในเซสชันหลัก → approval card โผล่ที่นั่น
    → ได้สิทธิ์เฉพาะเซสชันนั้น = เทสแบบ attended เท่านั้น (เหมือน GT-005 รอบ 24)

  📌 ผลข้างเคียงที่ต้องรู้: job 053 ปล่อย server + client ค้างไว้ และ **bridge ถูกบล็อก**
  (ดูกฎใหม่ในไฟล์ CHIEF) → job `054_gt006_teardown.ps1` ถูกวางคิวไว้แล้วและ
  **จะรันเองอัตโนมัติทันทีที่ปิดหน้าต่างเกม** ไม่ต้องทำอะไรเพิ่ม

- **evidence R28 (2026-08-17 13:38–13:4x, ไม่มี job ใหม่ — ไม่เปลี่ยนสถานะ `PENDING`):**
  รอบ 28 เข้ามาเจอสภาพเดิมทุกอย่าง: `inbox\` ยังมี **053 + 054 ค้างทั้งคู่**,
  ไม่มี `outbox\054_*` → **bridge ยังถูกบล็อกอยู่** (หน้าต่างเกมยังไม่ถูกปิด)
  → ตามกฎ **ไม่วาง job ใหม่** และ **ไม่เรียก `request_access`** ซ้ำ
  (`list_granted_applications` = `allowedApps: []` เหมือนเดิม = Panya ยังไม่ได้เพิ่มแอป
  ลง settings ของ scheduled task · ระบบบอกเองแล้วว่า retry ได้ผลเดิม — R27)

  ✅ **สิ่งที่รอบนี้ปิดได้จริงโดยไม่ต้องใช้ bridge: ชื่อคอลัมน์จริงของ DB (แก้ที่ 053 เดาผิด)**
  วิธี: copy `state\pirateforce.sqlite3` ไป `/tmp` แล้วเปิดแบบ `mode=ro` (ไม่แตะไฟล์จริง)

  | ตาราง | คอลัมน์จริง |
  |---|---|
  | `character_backpacks` | `character_id`(pk), `base_mask`, `base_identity`, `range_mask`, `updated_at` |
  | `character_backpack_items` | `character_id`, `item_identity`, `template_id`, `quantity`, **`slot`**, `raw_u8_38`, `raw_u8_39`, `detail_present` |
  | `character_positions` | `character_id`(pk), `scene_id`, `scene_seq`, `x`, `y`, `z`, `updated_at`, `heading` |
  | `characters` | `id`, `account_id`, `selector`, `name`, `actor_wire`, `avatar_wire`, `avatar_typed_json`, `identity_lo`, `identity_hi`, `created_at`, `updated_at`, `deleted_at`, `name_key`, `create_fingerprint` |
  | `sessions` | `id`, `account_id`, `selected_character_id`, `opened_at`, `closed_at`, `lease_generation` |
  | `accounts` | `id`, `login_name`, `created_at` |
  | `schema_migrations` | `version`, `applied_at`, `checksum` |

  🔴 **สาเหตุที่ job 053 พัง `no such column: slot`:** `slot` **ไม่ได้อยู่ใน
  `character_backpacks`** — มันอยู่ใน `character_backpack_items` (คนละตาราง)
  `character_backpacks` เป็นแถวเดียวต่อตัวละคร เก็บแค่ mask/identity ของกระเป๋า
  (มี CHECK บังคับ `base_mask=255`, `base_identity=0`, `range_mask=1`)
  ส่วนของในช่องอยู่ที่ `character_backpack_items` PK=(character_id,item_identity)
  และ **UNIQUE(character_id,slot)** → query กระเป๋าที่ถูกต้องต้อง JOIN สองตาราง

  📊 snapshot แถว (read-only 13:40, ไฟล์ mtime 12:39 = ไม่มีการเขียนใหม่หลัง GT-005):
  accounts=1 · characters=1 · character_positions=1 · character_backpacks=1 ·
  character_backpack_items=3 · sessions=3 (ทั้งสามแถว `selected_character_id IS NOT NULL`)
  → **inference (ไม่ใช่ fact):** client pid 15348 ที่ 053 เปิดค้างไว้ **ยังไม่ได้ล็อกอิน**
  (ไม่มีใครขับ UI) จึงไม่มีแถว sessions ใหม่หลัง 13:28 — คาดว่า teardown 054 จะพบ DB
  เท่าเดิม ถ้าผลจริงต่างจากนี้ ให้ถือว่า inference นี้ผิดและบันทึกไว้

- **evidence R29 (2026-08-17 13:44–13:49, ไม่มี job ใหม่ — สถานะยังเป็น `PENDING` ไม่เปลี่ยน):**
  สภาพเดิมเป๊ะจากรอบ 28 (ห่างกันแค่ ~2 นาที): `inbox\` ยังมี **053 + 054 ค้างทั้งคู่**,
  ไม่มี `outbox\054_*` → **bridge ยังถูกบล็อก** (หน้าต่างเกม pid 15348 ยังไม่ถูกปิด)
  `list_granted_applications` = `allowedApps: []` → **ไม่เรียก `request_access`** ตามกติกา R27
  DB `state\pirateforce.sqlite3` mtime = 12:39 ไม่มี `-wal/-shm` → ไม่มีการเขียนใหม่
  → **สอดคล้องกับ inference ของ R28** ว่า client ที่เปิดค้างยังไม่ได้ล็อกอิน (ยังไม่ยืนยัน
  จนกว่า 054 จะรันจริงและรายงาน sessions after)

  🆕 บันทึกเพิ่ม (ไม่เกี่ยวกับคิวโดยตรงแต่กระทบการเดินคิว): scheduled task ตั้ง cron
  `*/5 * * * *` (+jitter 235s) → ~12 รอบ/ชม. ทุกรอบจะได้ผลเดียวกันจนกว่าจะปลดบล็อก
  ดูข้อเสนอในข้อ 19.2 ของ CHIEF_CONTINUATION.md

  ⏳ **GT-001 / GT-003 / GT-006 ยัง PENDING ทั้งหมด** — ตัวปลดล็อกเดียวคือข้อ 1 และข้อ 2
  ในรายการ "ของที่ต้องให้ Panya ทำ"

- **evidence R30 (2026-08-17 13:49–13:55, job `055` — สถานะ GT-006 ยังเป็น `PENDING` ไม่เปลี่ยน):**
  🟢 **bridge ปลดบล็อกแล้ว** — Panya (หรืออะไรบางอย่าง) ปิดหน้าต่างเกมไปก่อน 13:47
  → `054` ที่ค้างคิวรันเองทันทีตามที่วางไว้ · `inbox\` ว่างเกลี้ยงตอนเข้ารอบ

  🔴 **แต่ `054` พังเงียบ ๆ — bug การอ่านไฟล์ของตัวเอง (ไม่ใช่ bug ของเกม):**
  `053_client_info_*.txt` เป็น **บรรทัดเดียว** คั่นด้วยช่องว่าง:
  `clientpid=15348 shim=12528 server=13672 stamp=20260817_132858`
  แต่ `054` ใช้ regex `^(\w+)=(.+)$` ต่อบรรทัด → `clientpid` งาบทั้งบรรทัดที่เหลือ
  → `shim`/`server` ไม่เคยถูกเซ็ต → cast ได้ **PID 0 = System Idle Process**
  → ทุกคำสั่งหลังจากนั้นยิงใส่ PID 0 ได้ `"Access is denied"` และ ctrl-c sidecar
  บันทึก `"target_pid": 0, "ctrl_c_sent": false` → **server ไม่เคยถูกหยุด**
  (บรรทัดที่ฟ้อง: `listeners remaining = 2`)
  ✅ ค่าเดียวของ `054` ที่เชื่อได้คือ `GameClient processes remaining = 0`
     (มาจากการ query ตาม *ชื่อ* ไม่ใช่ PID เสีย) = client หายไปจริง

  ✅ **job `055` ปิดงานให้เรียบร้อย** (parse ใหม่แบบ split ช่องว่าง + guard กัน PID reuse
  ด้วย ProcessName + StartTime เทียบหน้าต่างบูตของ 053 ก่อนยิงสัญญาณ):
  ```
  BEFORE listener 10189/10188 owningPid=13672 · server pid=13672 name=python start=13:29:03
                                              · shim   pid=12528 name=py     start=13:29:03
  ctrl-c helper exit = 0   (ctrl_c_sent: true, target_pid: 12528)
  server exited=True · shim exited=True · AFTER listeners = 0 · GameClient = 0
  stopped markers = 1 · traceback = 0 · stderr = 0 bytes
  ```
  🟢 **Ctrl+C หยุด server ได้สำเร็จตั้งแต่ครั้งแรก** — น่าบันทึก เพราะ FND-006/007/009
  ต้องใช้ `Stop-Process -Force` ทุกครั้ง (ครั้งนี้ไม่ต้อง)

  📌 **ผลจริงของการบูตแบบไม่มีคนขับ (ปิดคำถามที่ค้างมาตั้งแต่รอบ 26):**
  client **ต่อ LOGIN เองได้โดยไม่ต้องมีใครกดอะไรเลย** —
  `13:29:26 [+] LOGIN connection ('127.0.0.1', 53075)` → `LSCN_LoginVitalReq` (บัญชี `test`)
  → server ตอบ `LoginVitalRes` (`Pirate Force Local` / `Channel 1`) → **`login idle timeout`**
  ไม่มี `GAME_*` log ในโฟลเดอร์ capture เลย · `GAME_LIVE.txt files = 0`
  → **เพดานของ unattended run = หน้าจอเลือกเซิร์ฟเวอร์** ถัดจากนั้นต้องมีคลิก
  → ยืนยัน inference ของ R28 ว่า client ที่เปิดค้างไว้ยังไม่ได้ล็อกอิน (ตอนนี้เป็น fact แล้ว)

  📊 DB หลังหยุด server (อ่านแบบ read-only หลัง process ตายแล้ว): **ไม่ขยับเลย**
  sessions with char = 3 (สามแถวเดิม ปิดครบ) · blank-conn = 0 · max lease_generation = 3
  · integrity ok · position เท่าเดิมเป๊ะ · sha = `F37BEFE6…95C8` = canonical
  · `-wal` 0 ไบต์ + `-shm` 32768 ไบต์ ยังอยู่ (ตรงกับกฎเดิม: ctrl-c ทิ้งสองไฟล์นี้เสมอ)

  🆕 **แก้ความเข้าใจเดิมหนึ่งข้อ (ระดับ inference):** โน้ตเดิมว่า "ต่อ TCP เปล่าก็สร้างแถว
  sessions + กิน lease" **ไม่เป็นจริงกับพอร์ต LOGIN 10188** — การต่อครั้งนี้จบด้วย
  idle timeout โดยไม่มีแถวใหม่และ lease ไม่ขยับ → โน้ตนั้นควรอ่านว่าใช้กับ **GAME 10189**
  เท่านั้น (ยังไม่ยืนยัน จนกว่าจะมี probe ที่ตั้งใจต่อ LOGIN อย่างเดียว)

  🔒 สิทธิ์: `list_granted_applications` = `allowedApps: []` เหมือนเดิม
  → **ไม่เรียก `request_access`** ตามกติกา R27

  📄 รายงาน: `reports\PF_GT006_UNATTENDED_SCHEDULED_ATTEMPT_OPERATIONAL_NEGATIVE_20260817.md`
  (+ `.manifest` 14 ไฟล์) — **Grade E operational negative** · commit `f73433c`
  ⚠️ **ไม่แตะ `docs\FUNCTIONAL_COVERAGE.json`** เพราะรอบนี้ไม่ได้พิสูจน์ฟังก์ชันเกมใด ๆ
  (เป็นข้อสรุปเรื่อง harness/สิทธิ์ ไม่ใช่ coverage) → ไม่ต้องแตะ GRADE_SUBSET_SHA256

  🧹 **สภาพแวดล้อมกลับมาสะอาดแล้ว:** ไม่มี process ค้าง ไม่มี listener ค้าง ไม่มี job ค้าง
  → รอบถัดไปเริ่มจากศูนย์ได้ทันที **แต่ GT-001 / GT-003 / GT-006 ยัง `PENDING` ทั้งหมด**
  ตัวปลดล็อกยังเป็นข้อเดียวเดิม: เพิ่ม `GameClient.local.bin` ลง settings ของ scheduled task

- **evidence R31 (2026-08-17 14:00–14:2x, jobs `056`/`057` — สถานะยัง `PENDING`) 🔴
  การทดลองธง PANYA_PRESENT ได้คำตอบชี้ขาด: ธงช่วยไม่ได้**
  - Panya เขียนธง `PANYA_PRESENT.txt` 13:54 (นั่งรอกด Allow) → รอบ 31 ทำตามลำดับ 🔑
    ครบทุกขั้น: บูต server + เปิดเกมผ่าน bridge (056) → หน้าต่าง 'Pirate Force' ขึ้นใน 1 วิ
    → เรียก `request_access(["GameClient.local.bin"])` หนึ่งครั้งตอนหน้าต่างเปิดอยู่จริง
  - 🔴 **ผลเหมือน R27 ทุกตัวอักษร**: "can't be approved during a scheduled run …
    (Retrying returns this same result.)" → **ไม่มี dialog เกิดขึ้นใน scheduled run
    ไม่ว่าธงจะสดแค่ไหน Panya จะนั่งอยู่หรือไม่** (fact วัดซ้ำ 2 ครั้งแล้ว: R27+R31)
  - `list_granted_applications` = `allowedApps: []` ตลอดรอบ = Panya ยังไม่ได้เพิ่มแอป
    ลง task settings → **นั่นคือตัวปลดล็อกเดียวที่เหลือ จริง ๆ แล้ว**
  - 🆕 พบเพิ่ม: เปิด client แบบ redirect stdout/stderr ลงไฟล์ (Start-Process) **ก็ยังบล็อก
    bridge** จนหน้าต่างถูกปิด ~14:19 → กฎ "redirect แล้วไม่บล็อก" ใช้ไม่ได้ ต้องวาง
    teardown job ต่อคิวล่วงหน้าเสมอ (057 รันเองสำเร็จหลังหน้าต่างปิด: Ctrl+C สะอาด,
    listeners 0, DB sha = canonical, sessions 3/blank 0/lease 3, GAME_LIVE 0)
  - ระหว่างรอ: **M3/HYP-PF-010 landed = commit `abf3696`** (ดูหัว GT-002) —
    GT-002 ขยับจาก "รอ M3" เป็น "รอ M4 runtime hookup"

- [รอบ 32, 14:31] idle round — คิวไม่เปลี่ยน: GT-001/003/006 PENDING (รอเพิ่ม GameClient.local.bin
  ใน task settings — ธง PANYA_PRESENT พิสูจน์แล้วว่าช่วยไม่ได้ ไม่ทดลองซ้ำ), GT-002 รอ M4 runtime hookup
  (รอ Panya เคาะขอบเขต) · ไม่มีการบูต server/เปิดเกมในรอบนี้

- **[รอบ 33, 15:1x] ประมวลผล GT-001 PASS + GT-006 observation จากเซสชันหลัก 14:32–14:44 เสร็จครบ:**
  - GT-006 → `reports\PF_GT006_CHAT_INPUT_UNKNOWN_FRAME_WIRE_CAPTURE_20260817.md`
    (+`.manifest` 5 ไฟล์) **Grade B controlled capture** หนึ่ง claim — commit **`eb6fef0`**
  - **matrix ขยับตามคำตัดสิน:** `chat/client_chat_input` = `in_progress`
    (หลักฐานแรกของแถว — ขึ้นสูงกว่านี้ไม่ได้: จับได้แต่ยังไม่ decode/ไม่ dispatch/ไม่มีคำตอบ) ·
    **เปิด Domain 8 `presentation` (Presentation and audio) ทีเดียวจบ 4 แถว** ตามข้อเสนอ 6.1
    ที่ Panya เคาะ (scene_music_control / system_message_display / ui_error_dialog_surfaces /
    loading_transition_screens ทุกแถว `in_progress` required) + banner ใหม่ใน STATUS.md
  - เทสใหม่ `tests/test_presentation_ownership.py` (7 เทส เฝ้า ownership negatives ของ
    0xAC52 + MusicControl และ pin รูปร่าง domain) — จำเป็นเพราะ ratchet
    "แถวที่มีเกรดต้องมี test ref" · re-pin `GRADE_SUBSET_SHA256` = `0EC17CBB..33A1`
  - **Windows gate job 062 ก่อน commit: 391 passed / 0 failed ALL GREEN**
    🔴 **เกณฑ์เขียวใหม่ = 391 (เดิม 384; test ใหม่ +7)** · ledger PASS entries=17 ·
    coverage PASS domains=8 · diff --check สะอาด
  - HEAD ตอนนี้ = **`eb6fef0`** (`c778535` GT-001 → `eb6fef0` GT-006+matrix) ·
    dirty = lease 1 ไฟล์ · canonical DB sha = `CACE7F77..F493` (ตาม 061) ·
    cleanup tmp_obj/HEAD.lock.stale = job `063`
  - คิวคงเดิม: GT-003 PENDING (สิทธิ์+ข้อ 14) · GT-002 BLOCKED รอ M4 (รอ Panya เคาะขอบเขต) ·
    GT-001 [PASS] recurring พร้อม re-arm เมื่อมี commit แตะ src/ ครั้งถัดไป (เช่น M4)

- **[รอบ 34+35, 15:20–16:2x] M4 + item-14 landed → GT-002 ปลดเป็น PENDING · GT-001 re-armed:**
  - รอบ 34 ตายกลางรอบหลัง commit เสร็จ (ไม่ได้เขียนบันทึก) — รอบ 35 บันทึกแทนจาก outbox 064/065/066 + git
  - **M4 = commit `4c29a63`** (runtime hookup ใต้ opt-in scenario · gate 064: 398/0) ·
    **item-14 ทาง (ข) = commit `55c7c59`** (known_limitation + `HYP-PF-011` · gate 065: **405/0** = เกณฑ์เขียวใหม่ · ledger entries=18)
  - **GT-002 → PENDING** พร้อม steps/pass criteria ฉบับเต็ม (ดูหัวข้อ GT-002 —
    ตาราง persistence: `character_backpack_items` + `character_backpacks`) ·
    **GT-001 → PENDING re-armed** ที่ HEAD `55c7c59` (ทั้งสอง commit แตะ src/) ·
    GT-003 [CLOSED] คงเดิม · GT-005/GT-006 [PASS]/[DONE] คงเดิม
  - สิทธิ์: `list_granted_applications` ในรอบ 35 = **`allowedApps=[]`** → Panya ยังไม่เพิ่ม
    `GameClient.local.bin` ใน task settings — เทสทั้งคู่รอ attended session หรือ grant ใน settings
  - ไม่มีการบูต server/เปิดเกมในรอบ 34–35 (ธง PANYA_PRESENT หมดอายุ 14:54)

- **[attended 16:26–17:1x] GT-002 = PASS ✅ ที่ HEAD `55c7c59` + finding ใหม่ 0x1B40:**
  - Panya ตอบแชทของรอบ 35 → เซสชันเดียวกันกลายเป็น attended → ยืนยันว่า **ไม่มีหน้า settings
    สำหรับ pre-grant แอปให้ scheduled task จริง** (ตรวจเอกสาร Anthropic แล้ว: สิทธิ์เป็น per-session
    ผ่าน dialog เท่านั้น มีแต่ blocklist) → **ทางเทสถาวรทางเดียวคือ attended** — จดทับข้อ 24.4.1
  - request_access ตอนหน้าต่างเกมเปิด → granted tier full 16:32 (ครั้งที่ 3 ที่ยืนยันว่า attended ขอได้จริง)
  - **GT-002 PASS ครบ 4 ชั้น** (wire/response/DB 2 ตาราง/UI+reconnect) — รายละเอียดใน section GT-002
  - **finding ใหม่: logout protocol = `0x1B40` ไม่มีคำตอบจาก Foundation** + client2 เข้าสถานะ
    ไม่รับ X/Alt+F4 → ต้องรอ Panya End task · **069 teardown จะรันอัตโนมัติเมื่อ client2 ปิด**
  - GT-001 ยัง **PENDING re-armed** — ต้องรอ 069 จบ (ports ว่าง) แล้วบูต canonical ใหม่ (jobs 070/071)

- [รอบ 36, 16:2x] idle round — คิวไม่เปลี่ยน: GT-001 + GT-002 PENDING ทั้งคู่ (ตัวปลดล็อก:
  `allowedApps=[]` ยืนยันซ้ำ 16:19 → รอ Panya เพิ่ม `GameClient.local.bin` ใน task settings
  หรือ attended session · ธง PANYA_PRESENT หมดอายุ 14:54 ไม่ทดลอง request_access ซ้ำตาม R27+R31)
  · ไม่มีบูต server/เปิดเกม · HEAD `55c7c59` · dirty = lease 1 ไฟล์ · gate ล่าสุด 405/0 คงเดิม

- **[รอบ 37, 17:35–17:5x scheduled] GT-002 ประมวลผลเสร็จ → commit `b1087bb`:**
  - client2 ถูก End task แล้ว → `069` teardown รันเอง 17:26: server ปิดสะอาด (helper exit 0,
    listeners=0) · canonical UNCHANGED `CACE7F77..F493` (chief re-hash ยืนยันซ้ำจาก sandbox) ·
    🔴 **แต่ AFTER snapshot ในตัว job ล้มเหลว** — path สำเนา DB โดนตัดที่ space
    (`C:\Users\Panya\Desktop\Pirate` — โฟลเดอร์ชื่อ `Pirate Force`) + `uri=True` เปิด DB เปล่า
    → `no such table` · **chief เก็บ AFTER เองจากสำเนา run DB read-only ใน /tmp**: items
    [(1,2,1),(3,4,1),(10,1,2)] ✓ updated_at ขยับ ✓ sessions 6/6 closed ✓ integrity ok ✓
    (sha สำเนา `F9D44AB5..11F9` pin ไว้ใน report prose — ลบสำเนาได้แล้วหลัง commit นี้)
    · 🔴 บทเรียน: job ที่รับ path มี space ต้อง quote/escape เสมอ — snapshot fail ≠ เทส fail
  - report + manifest (PIPE 15 ไฟล์: capture 8 + outbox 067/068/069 7) + `.gitignore` allowlist
    2 บรรทัด + matrix `move_known_item_any_free_slot` → **`runtime_pass`** (evidence ref นำ +
    notes ใหม่ · `next_missing_behavior` inventory → `occupied_destination_policy`) + STATUS.md
    bullet + seam re-pin `GRADE_SUBSET_SHA256` = `400F42B3..6171` → **commit `b1087bb`** (docs-only)
  - gate จริงก่อน commit = job `070`: **ALL GREEN 405/0 · ledger PASS entries=18 ·
    coverage PASS domains=8 · diff --check สะอาด** (Linux pre-check 404+1 fail 3.10-only ตรง baseline)
    · cleanup = job `071` (tmp_obj 30 + HEAD.lock.stale ลบแล้ว · HEAD `b1087bb` · dirty = lease เท่านั้น)
  - ⚠️ เลข job `070`/`071` ที่แผน attended เคยกันไว้ให้ GT-001 boot/teardown ถูกใช้ไปแล้วกับ
    gate/cleanup ของรอบนี้ — **GT-001 รอบหน้าใช้เลขถัดไป (072/073)**
  - ② เทสในเกม: ธง PANYA_PRESENT (13:54) หมดอายุ 14:54 → ข้าม ไม่ request_access ไม่บูต ไม่เปิดเกม
  - คิวหลังรอบนี้: **GT-001 PENDING re-armed** (จาก `4c29a63`+`55c7c59` — `b1087bb` เป็น docs-only
    ไม่ re-arm เพิ่ม) รอ attended · GT-002 ปิดวงจรสมบูรณ์ · 0x1B40 ยังรอ chief decode (งานโค้ดรอบหน้า)
