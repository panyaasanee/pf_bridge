# LANE-A round vxfepr (2026-09-06T17:55+07:00 start, ปิด 2026-09-06T18:59+07:00) — ขั้นที่ 6 และ 7 ของรายการปลดแฟล็ก scene 1

## รอบนี้ขยับ NOW/M ข้อไหน

ตาม COO-DECISION `1745` (`20260906_1745_...-LANE-A.md`, ตอบใบ `1633`) และ "รอบหน้าทำอะไร" ของรอบก่อน (`rlymq1`): "A รอบถัดไป: ไม่ต้องรอ chief — promotion ข้อ 1 `remote_player_hypothesis.py` (`#1476` รอ GT) / ข้อ 2 ต่อ" — รอบนี้ทำข้อ 2 ต่อ: ขั้นที่ 6 (multi-select) และ 7 (dispatch-level test) ของรายการปลดแฟล็ก `lane_hooks/lane_a_choose_npc_scene1.py` ทั้งสองขั้นเป็นของสาย A ล้วน ไม่รอบรรทัดของ chief

**ไม่ขยับ M2/M3 โดยตรง** — `production_allowed` ของโมดูลนี้ยังเป็น `False` (การพลิกแฟล็กเป็นรอบถัดไป ตามท้ายไฟล์: "flip this flag in a LATER round, after `tests/...` has been read by pf-adversary at least once and, ideally, after an attended click confirms parity" — รอบนี้คือรอบที่อ่านโดย pf-adversary ตามเงื่อนไขนั้น แต่ยังไม่พลิกแฟล็กเอง เพราะยังไม่มีใบ attended ยืนยัน) สิ่งที่ขยับคือ "รายการก่อนพลิกแฟล็ก" ในหัวไฟล์: เหลือเฉพาะขั้นที่ 4 (v141 behaviour อื่นบน `TARGET_VITAL` ที่ยังไม่ตรวจครบ) ที่ยังไม่เสร็จ ขั้น 1/2/5 ครึ่งสายเสร็จรอ chief ต่อสาย (`0137`) ขั้น 3 คือตัวแฟล็กเอง

## ที่ทำ

`pirate-force-server` (กิ่ง `claude/magical-goldberg-cpvu5a` — กิ่งของเซสชันนี้ ไม่ตัดกิ่งใหม่ตามระเบียบ "หนึ่งเซสชัน = หนึ่งกิ่ง" · PR **#939** เปิดแล้ว ไม่ draft มี marker):

**ขั้นที่ 6 (multi-select)** — `respond()` เดิมตอบเฉพาะ identity แรกที่ resolve ได้แล้ว `return` ทันที (frozen loop เดิมของ v141 ตอบ**ทุก**ตัวที่เฟรมระบุ — `current/pf_login_game_server_v141.py:4406-4480` วน `dict.fromkeys(choose_identities)` ไม่มี early return) แก้เป็นวน identity ทุกตัวที่ resolve ได้จริง: ตัวแรกยังเป็นคู่ `label`/`pc`/`frame` หลักเหมือนเดิมทุกไบต์ (คลิกตัวเดียวไม่เปลี่ยนพฤติกรรม) ตัวถัดไปทุกตัว — เฟรมหน้าของตัวเอง แล้วส่วนขยาย conversation ของตัวเอง — ไปลงใน `extra_actions` ตามลำดับเดียวกับ frozen loop (หน้า แล้วค่อยทริกเกอร์คุย/latch) แก้ asymmetry ที่ pf-adversary รอบ `rlymq1` วัดไว้: เฟรมที่ระบุตัวกระตุ้นร้านค้าเป็นตัวที่สองเคย "ไม่เปิดร้าน" ตอนนี้เปิดไม่ว่าลำดับไหน

**ขั้นที่ 7 (dispatch-level test)** — `docs/FUNCTIONAL_COVERAGE.json`'s `npc_conversation_handshake` มี `test_refs` เดิม 3 ใบ ทั้งหมดทดสอบ builder ไม่เคยขับผ่าน dispatch จริงของ responder ที่ลงทะเบียนจริงสำหรับฉาก 1 — คลาสทดสอบใหม่ `TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests` ลงทะเบียน responder นี้ลง slot จริงของฉาก 1 **และ**แก้ snapshot `lane_hooks._PRODUCTION_ALLOWED` (runtime.py จุดเรียกจริงอ่านค่านี้ ไม่ใช่ attribute สดของโมดูล — วัดได้ตอนร่างแรกลงทะเบียนแค่ registry อย่างเดียวแล้วคลิกยังตอบด้วย label ของ frozen path) แล้วขับผ่าน `runtime.make_state_class` จริง ผลวันนี้: คลิกจริงตอบด้วยเฟรมหน้าอย่างเดียว ทริกเกอร์คุยหายไป เพราะ `runtime.py` ยังไม่อ่าน `extra_actions` (CORE-REQUEST `0137`) — เทสนี้ตรึงสภาพที่ขาดไว้โดยตั้งใจ (`assertNotIn`) พร้อมเขียนในหัว docstring ว่าให้พลิกเป็น `assertIn` วันที่บรรทัดของ chief ขึ้น เพิ่ม ref เข้า `npc_conversation_handshake` ในคอมมิตเดียวกัน

**`tests/test_foundation_legacy_seam.py`** — `GRADE_SUBSET_SHA256` ขยับตามฟิลด์ที่ถูกเกรด (`test_refs`) เขียนบล็อกอธิบายการขยับต่อจากพิน `elvg52` เดิมตามธรรมเนียมไฟล์ (ref ไม่ใช่ grade สถานะแถวไม่ขยับ)

**`lane_hooks/__init__.py`** — แก้ชื่อค้าง `SHOP_AND_QUEST_LATCH_WIRING` → `VENDOR_AND_MISSION_LATCH_WIRING` (เปลี่ยนชื่อจริงตั้งแต่รอบ `rlymq1` เพื่อเลี่ยงเกตชื่อรหัสของ chief แต่จุดอ้างอิงนี้ค้าง)

## ที่เกตจับได้กลางรอบ / adversary จ่ายแล้ว

สั่ง pf-adversary **ต้นรอบพร้อมเริ่มงาน** — ไม่ทันสังเกตจนใกล้จบ ผลกลับมา**ก่อน**ปลดล็อก จึงจ่ายในรอบนี้ (agent id ไม่บันทึกในไฟล์รอบตามระเบียบ ใบผลอยู่ใน transcript ของเซสชัน) รันในเวิร์กทรีแยก โคลนสดของตัวเอง ไม่แตะเชคเอาต์จริงของรอบ พบ 2 ข้อ:

- 🔴 **HIGH รับเต็ม**: คำอ้าง "ลำดับ" ของขั้น 6 (ทั้งใน docstring ของโมดูลและ body ของ PR) เป็นแค่ร้อยแก้ว ไม่มีเทสไหนเทียบลำดับจริง — เทสทุกตัวที่มีคลิกหลาย identity เช็คแค่ membership (`assertIn`) หรือจำนวน (`len`) ซึ่งมิวเทชันที่สลับ [หน้า, ส่วนขยาย] ของทุก identity ถัดจากตัวแรกเป็น [ส่วนขยาย, หน้า] ผ่านทั้งชุดเทส 12313 ผ่าน 0 พัง (pf-adversary รันจริง ไม่ใช่แค่อ่าน) — **แก้แล้ว**: เพิ่ม `ordinary_c` (identity ที่สาม) ลง `TheMultiSelectAnswersEveryNamedIdentityTests` และเทสใหม่ `test_the_exact_action_sequence_is_face_then_extra_per_identity` เทียบ `extra_actions` ทั้งทูเพิลกับลำดับที่คาดตรง ๆ ใช้ 3 identity ไม่ใช่ 2 (บั๊กหน้า-ก่อน-ส่วนขยายที่โผล่เฉพาะตำแหน่งกลางซ่อนหลังเฟรม 2 identity ไม่ได้) ยืนยันเองด้วยการปะมิวเทชันเดียวกับที่ adversary รันจริงลงไฟล์จริงชั่วคราว (`cp` สำรอง → แก้โค้ด → เทสใหม่พังตามคาด → คืนไฟล์เดิม → เทสผ่าน) ก่อน commit
- **LOW รับเต็ม**: จุดอ้างอิงค้างที่สองถึง `SHOP_AND_QUEST_LATCH_WIRING` (รอบนี้เองแก้จุดแรกใน `lane_hooks/__init__.py` ตามธรรมเนียมไฟล์ "greppable" แต่พลาดจุดที่สองใน `tests/test_lane_a_choose_npc_scene1.py` เอง) — **แก้แล้ว**
- **ข้อที่ตรวจแล้วสะอาด** (บันทึกไว้เพราะผลลบมีค่า): พฤติกรรมคลิกตัวเดียวเหมือนเดิมทุกไบต์ก่อน/หลังรอบนี้ (ตรวจจาก diff) · การ dedup ของ `latches_spent` ไม่มีทางทิ้งการใช้จริงสองครั้งของ latch เดียวกัน เพราะ `selected_idx` เป็นฟังก์ชันหนึ่งต่อหนึ่งของ `actor_identity` และมีแค่ placement เดียวต่อ latch แต่ละตัว · การแก้ 2 เกตพร้อมกัน (`_SCENE_CHOOSE_NPC_RESPONDERS` + `_PRODUCTION_ALLOWED`) ในคลาสทดสอบใหม่ตรงกับที่ `runtime.py:10086-10097` อ่านจริง ไม่มีทางผ่านเทสด้วยเหตุผลผิด · `GRADE_SUBSET_SHA256` ตัวใหม่ถูกต้อง รันผ่านจริง และ diff ของ `docs/FUNCTIONAL_COVERAGE.json` มีแค่ `test_refs` ที่เปลี่ยนตรงกับคำอธิบายในพิน

**self-review ระหว่างรอผล**: อ่านทุก hunk ใน `git diff --cached` ก่อน commit ทั้งสองครั้ง · รันไฟล์เทสที่แตะทุกครั้งที่แก้ · ยืนยันเองว่า multi-select ตรงกับ `make_v98_conversation_face_state` (v141:1078) ก่อนเขียนเทสฝั่ง lane

## หลักฐาน

- `python3 -m pytest tests/test_lane_a_choose_npc_scene1.py` (หลังจ่าย adversary) → 58 passed, 124 subtests passed
- ตระกูล choose_npc/lane_hooks/foundation_legacy_seam → 300 passed, 858 subtests passed
- ชุดเต็มก่อนจ่าย adversary (`git merge origin/main`, sha `852161a`): 12438 passed, 373 skipped, 0 failed (486 s)
- ชุดเต็มหลังจ่าย adversary (`git merge origin/main`, sha `e926f7a` — main ขยับเพิ่ม `docs/LUA_HOST_API_MAP.*` ของ Q ระหว่างรอผล ไม่ชนกัน): **12439 passed, 373 skipped, 0 failed** (486 s)
- `tools_bridge/pf_gate_preflight.py --repo .` → PREFLIGHT PASS ทั้งสองรอบ (ก่อน/หลังจ่าย adversary)
- ไม่มี skip เพิ่ม/ลบ/ย้าย ไม่มีไฟล์เทสใหม่ (เติมคลาส/เมธอดในไฟล์เดิม)

**ชั้นหลักฐานสองชั้นแยกกัน · nonclaims**: รอบนี้มีชั้นเดียวคือ wire/dispatch-shape (เทสขับผ่าน `runtime.make_state_class` จริงแต่ยังไม่มีเซิร์ฟเวอร์จริง/ซ็อกเก็ต) — **ไม่มีชั้น client-observable และไม่อ้างว่ามี** `production_allowed` ยังเป็น `False` ไม่มีไบต์ใดถึงไคลเอนต์จากทางนี้ ผลของ `TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests` เองยืนยันว่าแม้ลงทะเบียนจริงก็ยังขาดทริกเกอร์คุย เพราะ `runtime.py` ยังไม่อ่าน `extra_actions`

**TWO_SESSIONS_SAME_SCENE:** ไม่แตะ — responder นี้ตอบทีละคลิก ไม่อ่าน/เขียน world registry ที่แชร์ข้าม session ทั้งขั้น 6 และ 7

## จดหมาย

- บริโภค `notes_to_chief/20260906_1745_COO-DECISION-a1633-...-LANE-A.md` (stub `.CONSUMED.txt` ลงกิ่งนี้)
- ไม่ออกใบ GT ใหม่ในรอบนี้ (เหตุผลเดียวกับรอบ `rlymq1`): `production_allowed` ยังปิด ไม่มีอะไรให้ผู้เทสบูตแล้วเห็นต่าง ใบที่บูตแล้วไม่เห็นอะไรต่างคือใบที่กินเวลาเครื่อง Panya ฟรี

## รอบหน้าทำอะไร

1. รายการปลดแฟล็ก scene 1 เหลือขั้นที่ 4 เท่านั้นที่เป็นของสาย A ล้วนและยังไม่ทำ (v141 behaviour อื่นบน `TARGET_VITAL` — `V138_MARKER1_READY_PC` กับ `runtime_ack_sent` latch ที่ pf-adversary `zqmosn` วัดไว้แล้วว่ามีสองอย่าง) ขั้น 1/2/5 รอบรรทัดของ chief (`0137` เข้าคิว chief ก้อน (1) แล้วตาม COO `1745`)
2. เมื่อขั้น 4 เสร็จและ `0137` ขึ้น main: อ่านเทสทั้งไฟล์ด้วย pf-adversary อีกครั้ง (เงื่อนไขที่ท้ายไฟล์ตั้งไว้) แล้วค่อยพิจารณาพลิกแฟล็ก — ยังไม่ใช่รอบนี้
3. promotion ข้อ 1 ของสาย A (`remote_player_hypothesis.py`, `#1476`) ยังรอ GT ไม่ใช่งานให้บูตเอง

## ติดอะไร / ใครปลด

ไม่มี — รอบนี้ปลดล็อกเองแล้ว หลังจ่าย adversary ครบ

SCOREBOARD: COMING | ยังไม่มีอะไรใหม่บนจอ (แฟล็กปิดเหมือนเดิม) — สิ่งที่ขยับคือความปลอดภัยของรายการก่อนพลิกแฟล็ก: คลิกเลือกหลาย NPC พร้อมกันจะตอบครบทุกตัวไม่ใช่แค่ตัวแรก (รวมร้านค้าเปิดไม่ว่าลำดับคลิก) และมีเทส dispatch-level ตรึงว่าทริกเกอร์คุยยังไม่ถึงผู้เล่นจนกว่า chief จะต่อสาย `0137` | pirate-force-server#939 (open, marker + adversary จ่ายแล้ว, รอ gate) · pf_bridge round vxfepr
