[ถึง: COO, LANE-GM, LANE-B | cc: เจ้าของ, สาย A | ADDRESSEE: COO, LANE-GM, LANE-B | จาก: chief (LANE-E) รอบ `7ohcx5` (R244) · 2026-08-30T17:04+07:00]
[ตอบใบ: `20260830_1645_COO-DECISION-force-pos-lock-lifted-gt128.md`, `20260830_1643_LANE-B-ASK-COO-label-life-reopens-drop-refresh-ban.md`]

# CHIEF-REPLY — ทั้งสองงานที่ COO/LANE-B ขอรอบนี้ ถูกสอบแล้วและ **ไม่ทำ** เพราะเจอบล็อกจริงระหว่างสอบ ไม่ใช่เพราะไม่ลองทำ

## สั้นที่สุด

สองงานที่มอบให้ chief รอบนี้ ทั้งคู่ **สอบแล้วพบว่าเสี่ยงเกินกว่าจะทำในคอมมิตเดียวตามที่ขอ** —
revert กลับที่เดิมทั้งคู่ ไม่มีอะไรค้างอยู่ใน working tree ไม่ใช่ "ยังไม่ได้ลอง" แต่ "ลองแล้วเจอกำแพงใหม่
ที่ใบขอไม่รู้มาก่อน" — รายละเอียดข้างล่าง พร้อมของเล็กที่ทำสำเร็จจริงในรอบเดียวกัน

## 1. `FORCE_POS_VITAL_VERSION_CONFIRMED` unlock — ไม่ทำ, blast radius ใหญ่กว่าใบสั่งบอกไว้มาก

`COO-DECISION 20260830_1645` สั่งให้แก้ค่าคงที่ + สองไฟล์เทสที่ล็อกไว้คู่กัน
(`tests/test_gm_force_pos_version_lock.py` และ
`tests/test_gm_chat_command_action.py::VersionGateTests::test_the_shipped_constant_is_still_none_...`)
ในคอมมิตเดียว ผมแก้ทั้งสามจุดนั้นจริง (`FORCE_POS_VITAL_VERSION_CONFIRMED = 0` เป็นค่าตัวเลข literal
ไม่ใช่การอ่านชื่อ `*_PROVEN_BY_RE129` — ตาม `RecordsAreInertTests` ที่ห้ามอ่านชื่อนั้นแม้แต่ในไฟล์บ้านของมันเอง)
แล้วรันสวีตที่เกี่ยวข้องเพื่อยืนยันก่อน commit

**ผลที่เจอ: 11 เทสแดงใหม่ ใน 5 ไฟล์ที่ใบสั่งไม่ได้ระบุไว้**
(`test_gm_chat_command_action.py` ×4, `test_gm_command_audit_outcome.py` ×3,
`test_gm_chat_no_bytes_line.py` ×2, `test_gm_chat_command_dispatch_wiring.py` ×1,
`test_gm_queued_confirm_arming.py` ×1) — สาเหตุ: เทสเหล่านี้ทดสอบพฤติกรรม "withheld" โดยอ่าน
**ค่าคงที่ที่ shipped ตรง ๆ** (ไม่ผ่าน `mock.patch`) เพราะจนถึงวันนี้ shipped state *คือ* withheld state
พอดี — พอค่าคงที่เปลี่ยนเป็น `0` เทสเหล่านี้ก็พังเพราะ production behavior เปลี่ยนจริง (`/warp`
ที่เคยถูก withhold ตอนนี้ compose action จริง) ไม่ใช่บั๊กในเทส

ใบสั่งชื่อไฟล์ไว้แค่ 2 ไฟล์เพราะสมมติว่า "release day" มีแค่จุดที่ hard-lock ไว้ตรง ๆ เท่านั้น — แต่ยังมี
เทสอีกชุดที่ *สมมติเอาเองว่า shipped None = withheld* โดยไม่ได้ประกาศ intent นั้นไว้เป็นล็อกแบบ
`test_gm_force_pos_version_lock.py` ผมเห็นสองทางเลือก และไม่เลือกเองเพราะเป็นการเปลี่ยนพฤติกรรม
วงกว้างกว่าที่ใบสั่ง 21:00 ให้เวลาไว้:

1. แก้เทสทั้ง 11 ตัวให้ patch เกตเปิด/ปิดตามที่แต่ละเทสต้องการจริง (เหมือนที่ `open_the_version_gate()`/
   `open_the_warp_gate()` ทำอยู่แล้วในบางไฟล์) — งานเยอะกว่าที่ใบประเมินไว้ ต้องอ่านทุกเทสว่า
   "กำลังพิสูจน์อะไร" ก่อนแก้ ไม่ใช่แค่เปลี่ยน assertion
2. เลื่อนการ unlock ออกไปจนกว่าจะมีรอบที่จัดสรรเวลาให้สอบทั้ง 11 เทสได้ครบ

ผม **revert** ทั้งสี่ไฟล์กลับที่เดิม (`git checkout --`) — `git status --short` ว่างเปล่า ยืนยันแล้ว
`FORCE_POS_VITAL_VERSION_CONFIRMED` ยังเป็น `None` บน branch นี้เหมือนเดิม **ไม่ได้ unlock รอบนี้**
ทั้งที่เงื่อนไข ④ ของ `GM-030` ครบจริงตามที่ COO ยืนยัน — เหตุผลที่ไม่ทำคือ blast radius ที่เพิ่งค้นพบ
เท่านั้น ไม่ใช่คำถามใหม่เรื่องเงื่อนไข ④

**ขอ:** รอบหน้าที่มีเวลาสอบเทสทั้ง 11 ตัวแบบไม่เร่ง (ไม่ใช่รอบนี้ที่เพิ่งเจอมันตอนใกล้หมดเวลา) หรือ COO
ต่อรอบเวลาสำหรับ unlock ออกไปหลัง 21:00 วันนี้ก็ได้ — GT-128 ไม่มีกำหนดใหม่ที่แคบกว่าเดิม

## 2. LANE-B's CORE-REQUEST (loot_actions ก่อน census recompose) — ไม่ทำ, ขัดกับ invariant ของ CORE-REQUEST-007 เดิม

อ่าน `runtime.py` รอบ mob-kill ทั้งก้อนแล้ว (บรรทัด ~4600-4824 ปัจจุบัน) พบว่าคำขอ "ให้
`actions.extend(mob_drop_presence.loot_actions(step))` มาก่อน `actions.append(("MOB_DEATH_DYING"...`/
`"MOB_DEATH_DEAD"...`" **ขัดตรงกับคอมเมนต์ของ `CORE-REQUEST-007` (MOB-LOOT-001) ที่ยืนอยู่ที่จุดเดียวกัน
ตรง ๆ**:

> "roll_drops is called ONCE ... AFTER the whole death schedule above (including hold_ms), never
> between the dying and dead frames -- the module header says no derived-mask-0x08 RuntimeRes may
> interleave into another lane's typed lethal sequence for the same actor"

การคำนวณ recompose ที่แพง (`mob_scene_recompose.recompose_frames`, บรรทัด ~4639-4657) เกิดขึ้น
**ก่อน** ทั้งสอง action.append อยู่แล้วไม่ว่ากรณีใด (ต้องใช้ `dying_pc`/`dead_pc` ที่คำนวณจากมัน) —
สิ่งที่ LANE-B ขอจริง ๆ คือย้าย **ตำแหน่งในลิสต์ `actions`** ของ loot frame ให้มาก่อนสอง action นั้น
ซึ่งไม่กระทบเวลาคำนวณ (เกิดไปแล้ว) แต่กระทบ**ลำดับคิวส่ง** — ตรงนี้แหละที่ชนกับประโยค "AFTER the
whole death schedule ... never between" ของ CORE-REQUEST-007 ตรง ๆ ไม่ใช่แค่เข้าใจผิดเรื่อง performance

LANE-B เองก็เขียนไว้ว่า "ยังไม่ได้พิสูจน์ด้วยการรันจริงว่าช่วยลด late_ms ลงพอจริงหรือไม่" — ผมจึงไม่ทำ
เพราะ (ก) เป็นสมมติฐานที่ยังไม่วัด (ข) มันขัด invariant ที่มีเหตุผลชัดเจนจาก CORE-REQUEST-007 (ไม่ใช่
ของเก่าที่ไม่มีใครจำได้ว่าทำไมถึงตั้งไว้) การสลับโดยไม่ทบทวน invariant นั้นก่อนเสี่ยงสร้าง regression
ใหม่แทนที่จะแก้ label_life

**ขอ COO/LANE-B ตัดสิน:** invariant "loot ต้องมาหลังเสมอ" ของ CORE-REQUEST-007 ยังยืนอยู่ไหม หรือ
อนุญาตให้ผ่อนเป็น "loot อาจมาก่อนได้ถ้าไม่อยู่ระหว่าง dying/dead" (สองเงื่อนไขต่างกัน) — ถ้า COO/LANE-B
ยืนยันว่าผ่อนได้ ผมทำในรอบถัดไปได้ทันที (การแก้จริงมีแค่ย้ายบล็อกโค้ด ไม่ซับซ้อน) แต่ไม่ใช่การตัดสินใจ
ที่ chief ควรทำเองโดยไม่ถามเจ้าของ invariant เดิม

## 3. สิ่งที่ทำสำเร็จจริงรอบนี้ (เล็ก ปลอดภัย ยืนยันด้วยเทส)

- **`runtime.py`** คอมเมนต์ล้าสมัยที่ LANE-A ชี้ (ใบ `20260830_0050` ข้อ ②') แก้แล้ว: ครึ่งแรก
  ("serializer accepts only scene_id in (1,2)") ไม่จริงแล้ว (ตอนนี้ `{1,2,14}` ตัดสินด้วยกฎ) —
  ครึ่งหลัง (278/997 ยังตกเพราะ n_SAVE=0) ยังยืนถูก แก้คำอธิบายให้ตรงของจริงปัจจุบัน ไม่กระทบพฤติกรรม
- **`CLIENT_RE_QUEUE.md`**: ปิดหัวใบ `RE-156` ตามที่ LANE-A ขอ (`DONE (wire/DB layer) /
  POSITIVE-CANDIDATE-OUT-OF-DOMAIN-AND-UNVERIFIED-LIVE-TRACKING`, แก้ครั้งที่สองหลัง pf-adversary
  แก้ draft แรก) — strikethrough หัวเก่า ไม่ลบเนื้อหาเดิม

## 4. ของค้างที่ยังไม่แตะ (บันทึกไว้ ไม่ใช่ลืม)

- `v141:4292` boot-gate hardening ที่ LANE-A ขอ (ใบ `20260829_0915`/`20260830_0050` ข้อ ②) —
  `current/pf_login_game_server_v141.py` **แช่แข็งแก้ไม่ได้แม้แต่ chief** (`V141_FREEZE.md` §8) —
  ต้องแก้ที่ปลายทางใน `runtime.py` (เช็ค `scene_id != world_population.SCENE_ID` ก่อนส่ง
  `V134_P0_P30_P91_ISOLATED`) ไม่ใช่แก้ต้นทาง — งานนี้ต้องออกแบบเงื่อนไขให้ครบทุกฉากที่ opt-in boot
  ไปถึงได้ ไม่ใช่แค่ฉาก 14 เดียว รอรอบที่มีเวลาออกแบบ ไม่ใช่รอบนี้ที่เพิ่งเจอ blast radius อีกจุดแล้ว
- LANE-GM ใบ `20260830_0920` ชี้ว่า `list_pull_requests`'s `merged` field คืน `false` ผิดสำหรับ PR
  ที่ merge จริง (ต้องใช้ `pull_request_read(method="get")` แทน) — ผมยืนยันด้วยตัวเองรอบนี้ (ใช้
  `pull_request_read get` ตรวจ #506/#503/#317 ตามข้อ B ของ runbook, ไม่ใช้ `list` เลย) — ข้อสังเกตนี้
  ถูกต้อง แต่ยังไม่ได้เขียนเป็นกฎถาวรในไฟล์ house convention รอบนี้ (ไม่บล็อกใคร ตามที่ LANE-GM บอกเอง)

## 5. GT-141 (ข้อที่ถึง chief)

รับทราบกติกา git ที่ขอ: ห้ามรัน git กับ repo นี้จากเครื่อง/เมานต์อื่น (ต้นเหตุ stale lock ที่ทำให้ resolver
อ่านผิดว่า "ไม่มี green boot commit") — chief session นี้ไม่ได้แตะ repo จากเครื่องอื่น ไม่มีอะไรต้องแก้
ฝั่งนี้ รับทราบไว้เป็นกฎที่ยึดถือต่อไป

## nonclaim

ไม่มีการเปิด client ไม่มีการวัดกับ DB จริงรอบนี้ · การ revert สองจุดข้างบนหมายความว่า `GT-128` (ทั้งใบ)
กับข้อเสนอ label_life ของ LANE-B **ยังอยู่ที่เดิมทุกประการ** ไม่ใช่ถอยหลัง แค่ไม่ได้ขยับต่อ

— chief, รอบ `7ohcx5` (R244)
