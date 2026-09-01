# PIRATE FORCE — Chief Architect continuation file

## 🔴 ลำดับงานปัจจุบัน — ไมล์สโตน M1-M6 พักไว้ (คำสั่งตรงเจ้าของ 2026-09-01T02:15 ผ่านกะ1-A)

อ่านหัวข้อนี้ก่อนมอบหมายงานใดๆ ทุกรอบ — อย่ามอบงาน milestone (M1-M6/CHARTER-02) ใหม่จนกว่าเจ้าของจะสั่งกลับมา
(พัก ไม่ใช่ยกเลิก) ใบเต็ม: `notes_to_chief/consumed/20260901_0215_PANYA-ORDER-*.md` · มอบหมายสาย:
`notes_to_chief/consumed/20260901_0302_FROM_CHIEF_R278_*.md`

- **P-1** ของดรอปต้องอยู่บนพื้นนานพอให้เดินไปเก็บทัน → **LANE-B**
- **P-2** สีชื่อมอนต้องถูกสถานะ: ปกติ=ส้ม / สู้=แดง / ตาย=เทา (ห้ามชมพู) → **LANE-GM**
- **P-3** เปิดปุ่ม GM ให้ได้ → **LANE-GM** (Codex ป้อนข้อมูลเรื่อยๆ ใบที่แตะ P-3 หยิบใช้ทันที ไม่เข้าคิวรอ)
- งานสร้างใหม่คู่ขนาน: GM-A `/warp` ไม่ใส่พิกัด (LANE-GM, GT-182 **PASS** รอบ 8zf80f) ·
  UI-A/UI-B ปุ่มกลับหน้าเลือกตัวละคร/logout (LANE-A)
- 🆕 GM-B `/speed` **ย้ายเจ้าของจาก LANE-GM ไป LANE-DB** (`COO-DECISION/ORDER 20260901_1059/1100/1101`
  ทับของเดิมเฉพาะจุดนี้) — เป็นงานส่งมอบชิ้นแรกของสายใหม่ LANE-DB (ดูหัวข้อ "ทีมและเขตเขียน" ด้านล่าง)
- `GT-146`/ใบตีมอนทั้งหมด **ห้ามเข้าคิว attended** จนกว่า P-1 และ P-2 จะเสร็จ

🔴 KA1A-FINDING 20260901_1110 (`notes_to_chief/consumed/`): บล็อกนี้อยู่ใน **จดหมาย/ไฟล์นี้เท่านั้น** —
prompt ของแต่ละสาย (scheduled routine) ยังพูดถึงแต่ milestone เดิม เพราะ**เจ้าของเท่านั้นที่แก้ prompt ได้จริง**
(chief แก้แทนไม่ได้ ห้ามลองด้วย) จนกว่าเธอจะทำ ให้ chief ทุกรอบอ่านบล็อกนี้ก่อนมอบงานใหม่ แทนการพึ่ง prompt สาย

## ทีมและเขตเขียน — 🆕 สายที่ 5: LANE-DB (PERSISTENCE)

ตั้งโดย COO ตามคำสั่งตรงเจ้าของ 2026-09-01T10:5x (`notes_to_chief/consumed/20260901_1059_COO-DECISION-*.md`,
`.../20260901_1100_COO-DECISION-create-lane-db-*.md`, `.../20260901_1101_COO-ORDER-lane-db-first-*.md`)
ลงทะเบียนที่นี่โดย chief รอบ `8zf80f` ตามที่ COO ขอ ("รอบ :51 วันนี้"):

- **ภารกิจ:** persistence ข้าม session แบบ MMORPG จริง — typed columns ใน DB เป็นแหล่งความจริง
  (ความเร็ว/HP/เลเวล/สแตท/EXP/ของสวมใส่/เควส) compose attr block จากค่า typed + บล็อบ creation ของ
  ตัวละครเอง ห้ามเดาฟิลด์ที่ไม่รู้จักเป็นศูนย์ (ข้อห้ามตรงของเจ้าของ ใบ `1059`)
- **เขตเขียนใน `pirate-force-server`:** `migrations/` (ไฟล์เลขใหม่เท่านั้น ห้ามแก้ไฟล์ที่ apply แล้ว) ·
  โมดูลใหม่ `src/pirateforce_foundation/persistence_*.py` · เพิ่ม method ใหม่ใน `store.py` ได้
  แต่ห้ามเปลี่ยน behavior ของ method เดิม · `rounds/DB_*`
- **จุดเสียบ `runtime.py`/`app.py`:** ยังไม่มี — chief สร้างให้ครั้งเดียวเมื่อ LANE-DB ร้องขอ (แบบเดียวกับ
  LANE-B `COO-DECISION 20260830_0046`) ยังไม่มีการร้องขอเข้ามาถึงรอบนี้
- **v141:** ห้ามแตะตลอดกาล เหมือนทุกสาย
- 🔴 **canonical DB (`COO-DECISION 20260901_1112` แก้ทับถ้อยคำใบ `1100`):** เป็นปลายทางที่ LANE-DB
  พัฒนาไปหา ไม่ใช่ของต้องห้าม (1) ยกระดับผ่านไฟล์ migration ของ LANE-DB **ที่ผ่าน pytest +
  pf-adversary แล้วเท่านั้น** รันอัตโนมัติตอน server boot (runner ใน `store.py` +
  `schema_migrations` checksum ledger — migration 003/004 คือแบบอย่าง) (2) ห้ามแก้ไฟล์ `.db` จริง
  ด้วยมือ/SQL ตรง/สคริปต์เฉพาะกิจ นอกเส้น migration เด็ดขาด ไม่มีข้อยกเว้น
  (3) migration ที่แตะแถวข้อมูลเดิม (backfill/UPDATE/rebuild) ต้องมี backup อัตโนมัติ (สำเนาไฟล์ .db
  ก่อน apply) มาก่อนหรือพร้อมกันใน PR เดียวกัน
- 🔴 **ห้ามชี้บูตไปที่ canonical จนกว่าจะมีสามอย่างนี้พร้อมกันใน PR เดียว (`COO-DECISION
  20260901_1241_canon-sha-rotation`, ต่อจาก `1112`):** (1241-①) ด่านตรวจ sha ต้องแยก "sha เปลี่ยนเพราะ
  migration N apply สำเร็จ" (อ่าน `schema_migrations` เทียบ checksum — คาดหมายได้) ออกจาก "sha เปลี่ยน
  เพราะอย่างอื่น" (abort เหมือนเดิม) (1241-②) PR ที่ลง migration ที่แตะ canonical ต้องหมุนค่าใหม่ลง
  `CANON_SHA.txt` พร้อม log ชัดเจนอยู่ใน PR เดียวกันเสมอ ห้ามแยกสองรอบ (1241-③) ต้องระบุชัดว่าใครเป็นผู้บูต
  ครั้งที่ยกระดับ canonical จริง (จ็อบเฉพาะของ LANE-DB หรือแก้ `9001_play_boot.ps1`) — วันนี้ยังไม่มี
  เส้นทางไหนทำ ต้องออกแบบใหม่ ไม่ปล่อยให้เกิดเอง · เหตุผล: ขาดข้อ 1241-①/② = รอบเทส attended ถัดไปจะ abort
  ที่ด่าน sha (`exit 16 canonical mismatch`) แล้วดูเหมือน DB พัง คนจะแก้ด้วยการปลดด่านทิ้งเพราะเข้าใจผิด
  แล้วโปรเจกต์จะเสียตัวจับ corruption ตัวเดียวที่มีอยู่ไปเงียบ ๆ — ตรงกับข้อห้ามของเจ้าของเรื่อง "ปัญหาเงียบ"
  โดยตรง
- **งานแรก:** `/speed <ตัวคูณ>` ใช้เทสได้จริง (ใบ `1101`) — deadline PR แรกภายในรอบ 14:01 วันนี้,
  พร้อมเข้าคิว attended ภายใน 2026-09-02 12:00
- นัยต่อ M4 (ตีได้ตายได้): schema ปัจจุบันไม่มีคอลัมน์ HP เลย — LANE-DB คือตัวปลดล็อกจริง คิวถัดจาก
  `/speed` คือ HP/เลเวล (ตามที่ COO ตั้งข้อสังเกตไว้ในใบ `1100`)

## ดัชนีรอบเก่า (รอบ 44-178) — ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_INDEX.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา

## 0. โครงสร้างทีมคืนนี้ + เช็คก่อนเริ่มทุกครั้ง

### 0.1 ใครทำอะไร (ผู้ใช้สั่ง 04:40 แก้ 04:45)

- **`pirate-force-chief-continue`** (คุณ, ตื่นนาทีที่ 0,10,20,…):
  งานโค้ด / เอกสาร / ledger / verifier / commit
  🚫 **ห้ามเทสในเกม** — ถึงจุดที่ต้องเทส ให้เขียนรายการ PENDING ลง
  `pf_bridge\GAME_TEST_QUEUE.md` แล้วจบรอบ
- **ผู้เทสในเกม = เซสชันหลัก** (Claude ตัวที่คุยกับผู้ใช้ ถือสิทธิ์ computer use อยู่แล้ว)
  task `pirate-force-game-tester` ถูกปิดชั่วคราวคืนนี้
- **กลไกปลุก:** chief-continue จบรอบ → notification ปลุกเซสชันหลักอัตโนมัติ
  → ผู้เทสอ่านคิว ถ้ามี PENDING ก็เทสแล้วกรอกผลกลับ
  **แค่จบรอบให้เรียบร้อย = ปลุกผู้เทสแล้ว ไม่ต้องทำอะไรเพิ่ม**
- ทั้งคู่ใช้ `LOCK.txt` เดียวกัน

### 0.2 เช็คตามลำดับ

1. **`pf_bridge\LOCK.txt`**
   - ขึ้นต้น `RELEASED` = ว่าง ทำงานได้เลย
   - ขึ้นต้น `HELD` และ timestamp อายุ **< 20 นาที** = มีคนทำอยู่ → **หยุดทันที**
     ห้ามเขียน `inbox\` ห้ามแตะ repo
   - `HELD` แต่ timestamp **นิ่ง** เกิน 20 นาที = หมดอายุ เขียนทับเป็นของตัวเองได้
   - timestamp **ขยับ** = เจ้าของยังมีชีวิต ห้ามแย่ง
2. **`pf_bridge\inbox\`** — ถ้ามี `.ps1` ค้าง แปลว่างานก่อนหน้ายังรันไม่จบ → หยุด
3. **`pf_bridge\outbox\`** — อ่านไฟล์ล่าสุด ถ้ามีผลที่ยังไม่วิเคราะห์ ให้อ่านก่อน
4. **`pf_bridge\GAME_TEST_QUEUE.md`** — ถ้ามีรายการที่ผู้เทสกรอก `result` กลับมาแล้ว
   ให้เอามาประมวล/commit ต่อ

---

## CORE-REQUEST registry — ตัวนับเดียวทุกสาย (COO-DECISION 20260826_0656 · ตารางนี้สร้างโดย chief R174 · ตัด+สรุปเหลือเฉพาะแถวเปิด R211 28jd9c)

กติกา: chief เท่านั้นเขียนแถวนี้ · สายเสนอเลขถัดไปในจดหมายตัวเองกำกับ `[เสนอ · รอ chief]` · `ต่อแล้ว` เขียนได้ก็ต่อเมื่อโค้ดอยู่บน `main` แล้วจริง (`COO-DECISION 0401 §③`)

🔴 R211+R229 housekeeping: full table rows 001-026 -> `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` · row 027 (closed, wired R210, merge verified) + R211 preamble + stale WIRED-count note -> `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ตารางข้างล่าง = เฉพาะแถวที่ยังเปิด

(แถวเปิด 011 012 014 015 017 021 026 — สรุปย่อคำต่อคำย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ถ้อยคำเต็มอยู่ใน `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` เหมือนเดิม · เลขจองล่าสุด: 030)

- 030 CORE-REQUEST-GM-049 (สาย GM รอบ `nqba17` · `notes_to_chief/20260901_1728_LANE-GM-CORE-REQUEST-GM-049-speed-sparse-x7-runtime-send-point.md`) — เพิ่ม branch ใน `runtime.py`'s 0xAC52 chat-command action point ให้ `command.name == "speed"` เรียก `gm.speed_wire.compose_sparse_speed_update` แล้วส่ง action tuple **blocked: รอ COO ตัดสิน** — ไม่ใช่ RE-194 (field identity, Panya สั่งข้ามได้แล้ว 2026-09-01 16:39+07) แต่เป็น `attr_wire.UPDATE_ATTR_VITAL_VERSION_CONFIRMED` (`gm/attr_wire.py:154`) ยังเป็น `None` — ประตูนิรภัยระดับโปรโตคอลสามเงื่อนไขที่ COO เคาะเอง 4 รอบ (`20260831_0146`/`1244`/`1650`/`20260901T00:43`) ยังไม่ปลด ผิดไบต์นี้เสี่ยงเฟรมถูกไคลเอนต์ปฏิเสธทั้งเฟรม (recoverable via reconnect ตาม `FINDINGS_R19` แต่เสียรอบเทส attended) ถามตรง COO แล้ว (`20260901_1807_CHIEF-ASK-COO-gm049-speed-runtime-wiring-blocked-on-version-confirmation-gate.md`, สามทางเลือก ก/ข/ค) รอบ `u25irt` (R292) · **เพิ่มเงื่อนไขรอบ `5qs3y7` (R293)** จาก LANE-GM self-correction (`20260901_1836`): ถ้าตอนต่อสายจริง chief เลือกเรียก LANE-DB's `store.compose_sparse_block`/`write_typed_attributes_and_compose_sparse` ตรง ๆ (อ้อม `attr_wire.py`) ต้องมีประตูกั้น `SENSITIVE_FIELDS` (x=30 MD5 รหัสผ่านที่สอง) แยกต่างหากก่อน ไม่งั้น `compose_sparse_block` เป็นตัวกั้นเดียว — ยังไม่บล็อกอะไรเพิ่มเพราะแถวนี้บล็อกอยู่แล้วที่ COO gate ด้านบน ยังไม่ตัดสิน · ยังบล็อก รอ COO

- 028 CORE-REQUEST-GM-047 (สาย GM รอบ `bxkxfc` · P0 · `COO-DECISION 20260901_0741`) — cross-scene GM warp label ไม่เคยเรียก resync ตำแหน่ง (`runtime.py:5304` เดิมเช็คเฉพาะ `WARP_ACTION_LABEL`) เสี่ยง DB position เพี้ยนถ้ารัน `GT-182` ก่อนแก้ · แก้รอบ `ts0deo`: เช็คสมาชิกสามป้าย (`WARP_ACTION_LABEL`/`WARP_CROSS_SCENE_TELEPORT_ACTION_LABEL`/`WARP_CROSS_SCENE_NO_COORDS_TELEPORT_ACTION_LABEL`) ที่ `runtime.py:5304` + เทสถดถอยใหม่ที่พิสูจน์ผ่าน dispatch จริง (ยืนยันเทสล้มบนโค้ดเดิม 1!=2, ผ่านบนโค้ดใหม่) · **ต่อแล้ว (wired) — ยืนยันรอบ `69r41m` (R283)**: `pf_bridge#680` merged `2026-09-01T01:19:23Z`, `pirate-force-server#452` merged `01:27:10Z`, ทั้งคู่ยืนยันด้วย `pull_request_read get` (ไม่ใช่ `list_pull_requests`'s `merged` field ซึ่งอ่านผิดเป็น false — tool quirk เดิม) + อ่านโค้ดตรงจาก `origin/main:runtime.py:5304` เห็น `_GM_WARP_LABELS` สามป้ายจริง · ปลด `GT-182` จาก `BLOCKED-PENDING-GM047-FIX` เป็น `BLOCKED-ON-ATTENDED [NEEDS-ATTENDED-CAPTURE]` แล้วรอบนี้

- 029 (สาย A รอบ `s3m1f7`, `server#465`) — **ถอนแถว หลังตรวจพบว่าใบนี้ล้าสมัยไปแล้วก่อนถูกเปิดด้วยซ้ำ**: chief รอบ `eqkw30` (R286) เช็ค `pull_request_read get` เจอ `server#465` `state:closed merged:false mergeable_state:dirty` (ปิดโดย CI เพราะ merge ไม่ได้ ไม่ใช่เพราะ gate แดง) แล้วอ่านโค้ดตรงจาก `origin/main` พบว่า scene 4 (Slave Market) **ต่อสายครบและเปิดประตูแล้วจริง** ตั้งแต่ก่อนใบนี้จะถูกเปิดเสียอีก: `world_population_bg0004.py` ขึ้น `main` รอบ `2jdde8` (2026-08-30) · ลงทะเบียนใน `lane_hooks/lane_a_scene_census.py`'s `_CONSOLE_LINES_OF["bg0004_roster"]` และ `world_scene_travel.CENSUS_SOURCES[SLAVE_MARKET_SCENE_ID]` (จุดเสียบ census แบบ table-driven ที่มีอยู่แล้ว ไม่ใช่ bespoke elif ที่ chief ต้องเขียนเอง — v6.3 lane_hooks) · `login_entry_allowed` ของฉาก 4 ใน `scenarios/world_scene_registry_001.json` เป็น `true` มาตั้งแต่รอบ `bq4mst` (2026-08-31T06:2x+07:00) `COO-DECISION 20260830_1441` เอง · `server#465` (รอบ `s3m1f7`, เปิด 2026-09-01T04:49) เขียนโมดูลเดียวกันซ้ำจากบริบทที่เก่าไปแล้วกว่าหนึ่งวัน จึง merge ไม่ได้และถูกปิดถูกต้อง ไม่มีงาน chief ต้องทำ ไม่มีอะไรต้องกู้คืน · แจ้ง LANE-A แล้ว (จดหมายรอบนี้) ให้ pull main ก่อนเริ่มรอบถัดไปเสมอ







- รอบ R174-R209 — ย้ายไป archive แล้วทั้งหมด: `archive/CHIEF_CONTINUATION_ARCHIVE_20260827_R166_R178.md` · `archive/CHIEF_CONTINUATION_ARCHIVE_20260828_R179_R190.md` · `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` (R186-R209 + แถว 027 + WIRED note)
- (ดัชนี R210-R214 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R210_R214.md` แล้ว โดย chief รอบ `k882hm` -- เพดาน 30 KB)
- (ดัชนี R215-R221 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R215_R221.md` แล้ว โดย chief รอบ `o1s522` -- เพดาน 30 KB)
(ดัชนี R222-R223 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R222_R223.md` แล้ว โดย chief รอบ `8i0lto` -- เพดาน 30 KB)


- (ดัชนี R224-R230 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R224_R230.md` แล้ว โดย chief รอบ `3ru85y` -- เพดาน 30 KB)
- (ดัชนี R231-R238 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R231_R238.md` แล้ว โดย chief รอบ `bunu7v` -- เพดาน 30 KB)
- (ดัชนี R239-R242 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R239_R242.md` แล้ว โดย chief รอบ `65etwo` -- เพดาน 30 KB)
- (ดัชนี R243-R246 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R243_R246.md` แล้ว โดย chief รอบ `hxri6s` -- เพดาน 30 KB)
- (ดัชนี R247-R252 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R247_R252.md` แล้ว โดย chief รอบ `drvc5e` -- เพดาน 30 KB)
- (ดัชนี R253-R258 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R253_R258.md` แล้ว โดย chief รอบ `52ogem` -- เพดาน 30 KB)
- (ดัชนี R259-R261 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R259_R261.md` แล้ว โดย chief รอบ `sa0qjb` -- เพดาน 30 KB)
- (ดัชนี R262-R264 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R262_R264.md` แล้ว โดย chief รอบ `7dvax5` -- เพดาน 30 KB)
- (ดัชนี R265-R272 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R265_R272.md` แล้ว โดย chief รอบ `gmcj4a` (R274) -- เพดาน 30 KB)
- (ดัชนี R273-R280 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R273_R280.md` แล้ว โดย chief รอบ `eqkw30` (R286) -- เพดาน 30 KB)
- (ดัชนี R281-R282 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R281_R282.md` แล้ว โดย chief รอบ `1mw5lf` (R289) -- เพดาน 30 KB)

- (ดัชนี R283-R284 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R283_R284.md` แล้ว โดย chief รอบ `2zr22w` (R290) -- เพดาน 30 KB)
- (ดัชนี R285-R286 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R285_R286.md` แล้ว โดย chief รอบ `u25irt` (R292) -- เพดาน 30 KB)
- (ดัชนี R287-R288 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260901_R287_R288.md` แล้ว โดย chief รอบ `5qs3y7` (R293) -- เพดาน 30 KB)
- R289(1mw5lf) 2026-09-01T~15:0x+07:00 no runtime.py/app.py change either repo (platform round): fixed GT-188's pass criteria (label-only false-PASS loophole per CODEX_URGENT_20260901_1350 + checkpoint FIFTH conflict #1) -- split model-geometry vs name-label into separate tracked fields at BASELINE/STEP-A/B/C, NO-RESULT fallback if no model at STEP-A; mandatory pf-adversary review caught a real second defect the first draft missed (killed-mob corpse mesh could be mistaken for the dropped item's model -- this project has separately confirmed via GT-084/GT-084-R2/GT-129/RE-107 that corpses freeze and persist indefinitely, unrelated to this ticket), fixed with an explicit corpse exclusion + new nonclaim 6 + multi-drop tracking guidance; answered LANE-DB's two chief-addressed CORE-REQUESTs (DB-002 mirror request: cannot, no bridge-disk access from cloud, confirmed both files absent from git; DB-001: confirmed already wired+merged in R288, dynamic migration-count pin refactor deferred until PR#480 merges to avoid conflict); notified COO that NOW.md's GM-A line is stale (GT-192 already opened in R288, satisfies it); delegated 4 stale doc/comment corrections Codex has repeated across 3 checkpoints to a pf-static-re subagent in pirate-force-server (see companion PR); mailbox triage stubbed 9 chief-addressed letters, deliberately left RE-191-RESULT for LANE-GM (its consumer, per open-it-consume-it rule); WIRED=5/6 lane_hooks modules production_allowed=True (lane_a_choose_npc_scene1 intentionally still False), unchanged from prior rounds' reporting -> rounds/R289_1mw5lf_gt188-model-vs-corpse-fix-mailbox-triage-core-request-replies.md
- R290(2zr22w) 2026-09-01T~16:0x+07:00 wired LANE-DB's BackupError CORE-REQUEST in app.py (outer try/except around the whole boot if/else, not a helper function -- a helper collapsed the pin's textual migrate_with_backup() occurrence count to 1, breaking it; both boot-path pins + full suite green 6345/0 failed); opened RE-194 (BasicAttr+0x54 speed: 150.0 NPC vs 400.0 player-creation conflict, LANE-DB consumes) and RE-195 (does FontStyleID selector's relationship_predicate share BasicAttr+0x68 with the proven faction comparator -- new lead found in the existing Codex TSV, not asserted as fact per G6, LANE-GM consumes) per COO-ORDER 1447 and CORE-REQUEST-GM-048; decided P-2 targets FontStyleID not faction/relation (3-state fit, faction is binary and one measured pairing renders pink); granted LANE-A a one-time permission to add the dialog-open-push allowlist profile to logout_hypothesis.py per their own exact spec (chief didn't have round budget to wire it); mailbox triage stubbed 8 letters; archived R283-R284 index (see archive line above) to stay under the 30KB ceiling; WIRED=5/6 unchanged -> rounds/R290_2zr22w_backuperror-wired-re194-re195-opened-gm048-decided-corerequests-answered.md
- R291(57alcd) 2026-09-01T~17:5x+07:00 opened GT-193 (/speed sparse x=7 test, PENDING interface) per COO-ORDER 1642, caught+corrected a real RE-193-vs-RE-194 numbering slip in the source orders while drafting it; answered CORE-REQUEST RE-189 branches 2/3 (LANE-A, granted option b, second one-time edit); picked up the RE-157 job2 backlog item (mob-combat announced-membership guard) unimplemented since R246 -- wired via pf-builder subagent into runtime.py's _dispatch_mob_combat + 3 census-commit stamp points + 1 GM-warp clear site, 7 new + 19 fixed tests, full suite 6361/0 failed (verified independently twice), pf-adversary review found no bypass but surfaced a real open scope gap (clear/stamp only fires on GM /warp, not the other two production scene-transition paths) routed to LANE-B as a design question, not silently closed; RE-157/CLIENT_RE_QUEUE.md updated append-only; mailbox triage stubbed 11 letters (corrected my own bad "unconsumed" grep first -- most of what looked like 3-day-old backlog was already stubbed); WIRED=5/6 unchanged (re-verified by direct grep, not carried forward) -> rounds/R291_57alcd_re157-job2-wired-gt193-opened-corerequest-re189-mailbox-triage.md
- R292(u25irt) 2026-09-01T~18:0x+07:00 no runtime.py/app.py change either repo (platform round, NOW.md milestones still paused): fixed LANE-A's overclaim finding (logout_hypothesis.py's ReturnSelectServerVital field3 tag-byte comment + verify tool's "independent walker" claim), but mandatory pf-adversary review of the first draft (isolated worktrees, both repos) caught chief's OWN overclaim in the opposite direction -- the draft's [STALE][MEASURED] annotation asserted field3 has NO tag byte per PF_SERIALIZER_FIELDS.tsv:1125's UNTAGGED_STRING8_LEN32LE label, but the same TSV gives the identical label to DeleteActorVital's own field 4 (rows 462/466) despite GT-018/GT-055 confirming that one DOES carry a real 0x44 tag (GT-055: the label describes helper-call scope, not a full-wire claim) -- fixed both files to say UNCONFIRMED in both directions consistently (docstring, inline comments, AND the verify tool's actual runtime PASS-line text, which the first draft missed), rewrote RE-196 to ask the field3/DeleteActorVital question as a matched pair and fixed its wrong line-number citations, and removed an unauthorized "typo exemption" chief's own AGENTS.md wording had added beyond COO-DECISION 20260901_1744's literal "always" before adding the new mandatory-pf-adversary rule (trimmed R260's stale size-history note to archive to stay under the 25,600B ceiling, no rule content lost); answered CORE-REQUEST-GM-049 (LANE-GM's /speed runtime.py send point) as blocked -- not on RE-194 (Panya already waived that live) but on attr_wire.UPDATE_ATTR_VITAL_VERSION_CONFIRMED still None, COO's own 4-round-standing 3-condition unlock gate; asked COO directly rather than guessing the byte (CORE-REQUEST registry row 030, blocked); mailbox triage stubbed 6 chief-addressed letters; re-verified after fixes: 85 passed/3 skipped, verify tool 34/34 guards PASS, ledger PASS entries=48; no new GAME_TEST_QUEUE entry this round (no new player-observable feature, comment/doc + letters only) -> rounds/R292_u25irt_logout-tag-byte-fixed-re196-opened-agentsmd-pf-adversary-rule-gm049-blocked-asked-coo.md
