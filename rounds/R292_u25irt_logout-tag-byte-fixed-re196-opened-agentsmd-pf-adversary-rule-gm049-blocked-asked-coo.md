# R292 (u25irt) — 2026-09-01T18:07+07:00

## บริบท

รอบนี้อ่าน `NOW.md` ก่อนตามกฎ — สถานะ "รอ Panya ติ๊ก" ว่าง ไม่มีอะไรค้าง chief โดยตรง แต่หัวข้อ
"งานด่วนตอนนี้" (P-1/P-2/P-3 + คิว GM-A/UI-A/GM-B/UI-B/census latch) ยังมีผลเหนือไมล์สโตน CHARTER-02
ตามคำสั่ง `PANYA-ORDER 20260901_0215` ตรวจแล้วไม่มีงาน chief ต้องเปิดใหม่ในสามข้อ P-1/P-2/P-3 เอง
(P-2 อยู่ที่ CODEX static checkpoint แล้ว รอ P0-3; P-1/P-3 เป็นของสาย B/GM) และ GM-A/census latch
ปิดจบแล้วจากรอบก่อน (`GT-192` เปิดรอ Panya) เหลืองานจริงที่ chief เป็นเจ้าของ: ตอบ CORE-REQUEST ค้าง
สองใบ (`GM-049`, logout tag-byte finding จาก LANE-A) ตามลำดับหน้าที่ข้อ 3

## ทำอะไรไปบ้าง

1. **แก้ overclaim จริงที่ pf-adversary จับได้ (LANE-A รอบ `njkvcc`)**: `logout_hypothesis.py:186-206`
   และ guard ใกล้ `RETURN_SELECT_SERVER_BODY[11] != 0x44` — เติม `[STALE][MEASURED]` ระบุว่า tag
   byte `0x44` ของ field 3 (`ReturnSelectServerVital`) ไม่เคยวัดตรง มาจาก `DeleteActorVital`/GT-018
   ยืนยันด้วย `pf_bridge/external/PF_SERIALIZER_FIELDS.tsv:1125` (`UNTAGGED_STRING8_LEN32LE`, ไม่ใช่
   `0x44`) เช่นเดียวกับ `tools/verify_logout_return_select_encoder.py` (docstring + `FIELD3_TAG`
   comment) — แก้เฉพาะคอมเมนต์/docstring ไม่แตะ logic/byte-layout จริงแม้แต่ไบต์เดียว (เลือกตัวเลือก
   (ก) ที่ LANE-A เสนอ)
2. **เปิด `RE-196`** (`CLIENT_RE_QUEUE.md`, ท้ายไฟล์, STATIC-ON-BRIDGE) ถามหา instruction span จริงที่
   ยืนยัน/ปฏิเสธ tag byte ก่อน field 3 — chief เปิดเอง chief บริโภคผลเอง (เจ้าของไฟล์ตามเขตเขียน)
   ควบคู่กับข้อ 1 (ตัวเลือก (ค) ที่ LANE-A เสนอ ไม่ขัดกัน)
3. **เพิ่มกฎ `AGENTS.md`** ตาม `COO-DECISION 20260901_1744`: เซสชันที่มี Agent/Task tool จริงต้องเรียก
   `pf-adversary` ก่อน commit ที่ไม่ใช่การแก้คำผิดเสมอ ไม่ใช่ทางเลือก — เพิ่มบรรทัดนี้ดันไฟล์เกินเพดาน
   25,600 ไบต์ชั่วคราว (26,507) ตัดถ้อยคำกฎใหม่ให้กระชับ + ย้ายบันทึกประวัติ R260's "เข้าเพดานครั้งแรก"
   (บรรทัด 18-19 เดิม) ไป `archive/AGENTS_HISTORY_20260828.md` §12 (ไม่ตัดกฎใด ๆ เฉพาะประวัติ/เหตุผล)
   วัดสด `wc -c AGENTS.md` = 25,341 ไบต์ ใต้เพดาน
4. **ตอบ `CORE-REQUEST-GM-049`** (สาย GM รอบ `nqba17`, จุดส่งจริงใน `runtime.py` สำหรับ `/speed`):
   ตรวจแล้วบล็อกจริงไม่ใช่ `RE-194` (field identity, Panya สั่งข้ามได้แล้ว) แต่เป็น
   `attr_wire.UPDATE_ATTR_VITAL_VERSION_CONFIRMED` (`gm/attr_wire.py:154`) ยังเป็น `None` — ประตู
   นิรภัยระดับโปรโตคอลสามเงื่อนไขที่ COO เคาะเอง 4 รอบ ยังไม่ปลด ผิดไบต์นี้เสี่ยงเฟรมถูกไคลเอนต์
   ปฏิเสธทั้งเฟรม chief ไม่กล้าตีความคำสั่งสด "ส่งให้พอใช้งานได้ก่อน" ของ Panya ว่าครอบคลุมถึงประตูนี้
   ด้วย (คนละคำถามจาก RE-194) — เขียน `CHIEF-ASK-COO` เสนอสามทางเลือก ลงทะเบียน CORE-REQUEST แถว 030
   สถานะ `blocked: รอ COO` ไม่ได้เดาต่อสายเอง
5. **มายเทรียจ**: อ่าน+stub 6 ใบที่จ่าหน้าถึง chief/ทุกคนของวันนี้ที่ยังไม่มี stub
   (`1744`, `1728`, `1737`, `1652`, `1741`, `1355`) — ใบอื่นที่จ่าหน้าเฉพาะสายอื่น (LANE-DB/LANE-B ล้วน)
   ไม่แตะตามกฎ self-close

## ยืนยันก่อน commit

- `python3 -m pytest tests/ -k logout -q` → 85 passed, 3 skipped (comment-only change, ไม่แตะ logic)
- `python3 tools/verify_logout_return_select_encoder.py` → PASS (34 guards)
- `ast.parse` + `.encode('cp874')` ผ่านทั้งสองไฟล์ที่แก้
- `python3 tools/verify_hypothesis_ledger.py` → PASS entries=48 (ไม่มี drift, คาดว่าไม่กระทบเพราะไม่แตะ
  hypothesis code)
- `pf-adversary` subagent จริงรีวิวทั้งชุดก่อน commit (มี Agent tool ในเซสชันนี้ ตามกฎใหม่ข้อ 3) —
  **จับ overclaim จริงในร่างแรก** (worktree แยกทั้งสองรีโป, isolated จาก live checkout): ร่างแรกของ
  chief เองอ้างว่า `PF_SERIALIZER_FIELDS.tsv:1125` (`UNTAGGED_STRING8_LEN32LE`) พิสูจน์ว่า field 3
  **ไม่มี** tag byte เลย — แต่ `DeleteActorVital`'s field 4 (แถว 462/466) มี label เดียวกันเป๊ะ ทั้งที่
  `GT-018`/`GT-055` ยืนยันแล้วว่ามัน**มี**tag `0x44` จริง (`GAME_TEST_QUEUE.md:92`: label นี้ = ขอบเขต
  helper ไม่ใช่ full-wire claim) แปลว่าร่างแรกทำ overclaim ทิศตรงข้ามจากที่ LANE-A จับได้ตอนแรก ยังไม่นับ
  บรรทัด "EVERY TAG BYTE..." เดิมที่ร่างแรกลืมแก้ และ `verify_logout_return_select_encoder.py`'s ผล
  print จริง ("field3 is tag 0x44...") ที่ยังยืนยันไบต์นี้แบบไม่มีเงื่อนไขในรันไทม์แม้ docstring จะแก้
  แล้ว — **แก้ทั้งหมดรอบเดียวกันหลังผลรีวิว**: เปลี่ยนทั้งสองไฟล์เป็น "UNCONFIRMED ทั้งสองทาง" ให้
  ตรงกันทั้ง docstring/comment/runtime-print, เขียน RE-196 ใหม่ให้ถามทั้ง field 3 และ `DeleteActorVital`
  field 4 คู่กันเพื่อเทียบวิธี, แก้เลขบรรทัดอ้างอิงที่ผิด (`บรรทัด 72` จริงคือ `88`), แก้ AGENTS.md
  ตัดข้อยกเว้น "แก้คำผิด" ที่ไม่มีใน COO-DECISION ต้นฉบับออก — ยืนยันซ้ำหลังแก้: เทส 85 passed,
  verify tool 34 guards PASS, ledger PASS entries=48

## อะไรที่ไม่ได้พิสูจน์ / ยังค้าง

- `RE-196` เพิ่งเปิด ยังไม่มีผล — ไม่รู้ว่า field 3 มี tag จริงหรือไม่จนกว่าจะมีคนตอบ
- `GM-049`/`/speed` runtime wiring ยังไม่ต่อ รอ COO ตัดสินสามทางเลือก — ไม่ใช่ chief เลือกเอง
- ไม่มีอะไรใหม่ให้ผู้เล่นเห็นรอบนี้ (comment/doc + จดหมายล้วน) — ไม่เพิ่มรายการ `GAME_TEST_QUEUE.md`
  ใหม่เพราะไม่มีฟีเจอร์ใหม่ที่พร้อมเทส (ตามกฎ ทำอย่างใดอย่างหนึ่งของหัวข้อ 11 ข้อ 2 — เขียนเหตุผลไว้ที่นี่)

## WIRED

WIRED = 5/6 lane_hooks modules production_allowed=True (`lane_a_choose_npc_scene1` ยังตั้งใจ False)
ไม่เปลี่ยนจากรอบก่อน (ไม่ได้แตะ lane_hooks รอบนี้)

## ไฟล์ที่แตะ (นับ)

pirate-force-server: 2 ไฟล์ (`logout_hypothesis.py`, `tools/verify_logout_return_select_encoder.py`)
pf_bridge: `AGENTS.md`, `CHIEF_CONTINUATION.md`, `CLIENT_RE_QUEUE.md`, `archive/AGENTS_HISTORY_20260828.md`,
3 จดหมายใหม่, 6 stub consumed, ไฟล์รอบนี้ = 12 ไฟล์ (ไม่นับ rounds/ ตามกฎขนาด PR)
