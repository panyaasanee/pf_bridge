# LANE-GM รอบ `0op9bt` — ทำ COO-DECISION `2047` (unlink retry มีขอบเขต) + กู้คอมมิต O_BINARY จาก `#950` ที่ถูกปิด

เริ่ม 2026-09-06T22:12+07:00 · claim `pf_bridge#1572` · PR เซิร์ฟเวอร์ `pirate-force-server#956`

## ต้นรอบ (ตามลำดับ COMMON)

1. **`NOW.md`** (fetch สด · COO ตรวจ `2141`) — บรรทัด LANE-GM: `/lv` ✅ → P-3 ปุ่ม GM 3 หน้า = `GT-279`
   (รอเครื่อง Panya) · **`_best_effort_unlink` retry 3 + doc หลังเกต Windows เขียว (`2047`)** ← งานหลักรอบนี้ ·
   `/speed` ปิดจน mask ล็อกอิน · `/warp <n> <x> <y>` ปิดถาวร · ไม่มีคำสั่งใหม่อื่นถึงสายนี้
2. **กล่องจดหมาย** `ADDRESSEE: LANE-GM` ที่ยังไม่มี `.CONSUMED.txt` — **1 ใบ**:
   `20260906_2141_COO-DECISION-gm2046-report-received-lane-a-owns-it-LANE-GM.md` (บริโภคแล้วรอบนี้ ดูท้ายไฟล์)
3. **`AGENTS.md` §7** — อ่านแล้ว ไม่มีกฎใหม่ที่เปลี่ยนแผนรอบนี้
4. **ไฟล์รอบล่าสุด** `GM_20260906_2046_owqad2_*` "รอบหน้าทำอะไร" ข้อ 0 = ทำ `2047` เป็นงานแรก ✅ ·
   ข้อ 1 = เช็คสถานะ `#950` ก่อน ✅ (ผลด้านล่าง) · ข้อ 2 `GT-279` ยังรอเครื่อง · ข้อ 4 = COO ตอบแล้วใน `2141`
5. คิวในไฟล์สาย — ไม่ต้องใช้ (ข้อ 1-4 ไม่ว่าง)

**ยืนยันไฟล์บังคับต้นรอบ**: `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง ✅

**นาฬิกา**: `TZ=Asia/Bangkok date` = 22:12 ตรงกับป้ายเวลาของรอบนี้ · `_BRIDGE_HEARTBEAT.txt` บรรทัดสุดท้าย
19:00:02 (ห่าง 3 ชม.) = อาการที่ NOW อธิบายไว้แล้ว ("เครื่อง Panya ปิด 19:0x · heartbeat หยุดตามเครื่อง")
ไม่ใช่เรื่องใหม่ที่ต้อง escalate

## ล็อกรอบ

`list_pull_requests` state=open ใน `pf_bridge` หัว `[LANE-GM] round` → **ว่าง** (มีแต่ `[LANE-DB]` `#1571`
และ `[LANE-B]` `#1493` ซึ่งไม่ใช่ล็อกของสายนี้ ห้ามถอยเพราะเห็นมัน) ⇒ ตัดกิ่งจาก `origin/main` (`283ecd7`)
commit `_claim.md` push เปิด `#1572` (ไม่ draft · body ไม่มี marker) · list ซ้ำทันที: ไม่มีใบ `[LANE-GM]`
ที่เก่ากว่า = ไม่แพ้ใคร

## สถานะ `#950` ของรอบก่อน (สิ่งแรกที่ต้องเช็ค)

**ถูกปิดโดยไม่ merge** — `merge-claude-pr.yml` ปิดเองเวลา 21:39 (28 นาทีหลังเปิด) เพราะ job `gate` แดง
(run `34038370603`) · ตารางสรุปเกต: `pytest_subset exit=1 expect=0 RED` ช่องอื่น **เขียวหมด 22/23**

ต้นเหตุ **ไม่ใช่งาน D6 ของรอบนั้น**: ชุดเต็มบนต้นไม้เดียวกันแดงใบเดียวคือ
`tests/test_lane_a_choose_npc_scene1.py::…::test_the_talk_trigger_is_still_missing_at_real_dispatch_today`
= แถวสองของ `KNOWN_RED_MAIN:` ใน NOW (ของ LANE-A) และรอบนี้ผม checkout `origin/main` เปล่ารันใบเดียวกัน
แยกอีกครั้ง: **แดงเหมือนกัน** ⇒ เป็นของ main · COO `2141` ยืนยันเจ้าของคือ LANE-A และอนุญาตให้สายนี้อ้างแถวนี้ได้

⇒ รอบนี้จึง **cherry-pick คอมมิต O_BINARY (`876ce739`) จากกิ่ง `claude/keen-pasteur-owqad2` กลับมา**
รวมกับงานใหม่ในใบเดียว (`#956`) ตามกติกา "reaper ปิดแล้วกู้รอบถัดไปด้วย cherry-pick"

## สิ่งที่สร้างรอบนี้ (เขต `gm/` เท่านั้น)

**COO-DECISION `2047`** (ตอบคำถาม `1940` ของสายนี้เอง): retry มีขอบเขต · ไม่ทำ janitor · ไม่คืนโควตาย้อนหลัง

- `_UNLINK_ATTEMPTS = 3` · `_UNLINK_RETRY_DELAY_SECONDS = 0.05` (ค่าคงที่อย่างละหนึ่งตัวในโมดูล ·
  3 ครั้ง = 2 ช่องว่าง = หน่วงรวมแย่สุด 0.1 วิ ต่ำกว่าเพดาน ~300 ms ที่ COO ตั้ง)
- **เฉพาะเส้นทาง error เท่านั้นที่หน่วง** — unlink ที่สำเร็จครั้งแรกไม่ `sleep` เลย (ลินุกซ์ไม่เห็นความต่าง
  ตามเงื่อนไขที่ COO ตั้งไว้ · มีเทสตรึง)
- **ครบ 3 ครั้งแล้วยังลบไม่ได้** = สัญญาเดิมทุกข้อคงเดิม: คืน `CaptureFileNotVerifiedRemoved` chain จาก
  error เดิม · ไฟล์ยังอยู่ · **ไม่คืนโควตา** · พิมพ์ stderr หนึ่งบรรทัด
  `GM_CAPTURE_UNLINK_STUCK path=<ไฟล์> attempts=3` (ASCII ล้วน)
- บรรทัดพิมพ์นั้น **ห่อด้วย `try/except Exception`** เพราะฟังก์ชันนี้ถูกเรียกจากเส้นทาง
  `except BaseException` ของ `_capture_raw` ด้วย (ตอน interpreter shutdown `sys.stderr` อาจถูกปิดไปแล้ว)
  — บรรทัด log ที่ล้มต้องไม่ไปแทนที่ exception ที่เส้นทางนั้นกำลัง re-raise
- `docs/GM_LANE.md` + docstring เขียนผลลัพธ์ตรง ๆ ตามที่ COO สั่ง: **โควตาที่ค้างแบบนี้ล้างได้ทางเดียวคือ
  รีสตาร์ต process**

**เทส 4 ตัว** (`tests/test_gm_command_capture.py`) — สองตัวที่ COO บังคับ + อีกสอง:
(1) ล้ม 2 สำเร็จครั้งที่ 3 ⇒ `OSError` ธรรมดา (dispatch คืนโควตา) · ไฟล์หายจริง · sleep พอดี 2 ครั้ง
(2) ล้มครบ 3 ⇒ `CaptureFileNotVerifiedRemoved` · chain เดิมอยู่ครบ · ไฟล์ยังอยู่ · stderr **หนึ่งบรรทัด**
ที่มีชื่อไฟล์และเป็น ASCII จริง (3) สำเร็จครั้งแรก ⇒ sleep 0 ครั้ง (4) stderr ตายแล้ว ⇒ ยังได้ exception
ตัวเดิม ไม่ใช่ `ValueError` จากบรรทัด log

**มิวแทนต์ที่ตายแล้ว 5 ตัว**: `_UNLINK_ATTEMPTS = 1` · sleep ก่อนยอมแพ้ครั้งสุดท้าย · sleep บนเส้นทางสำเร็จ ·
ตัดบรรทัด log ทิ้ง · แคบ guard เหลือ `except OSError`

## หลักฐาน (สองชั้น แยกกัน)

**ชั้นยูนิต/มิวแทนต์** — `pytest tests/test_gm_command_capture.py tests/test_gm_commands.py
tests/test_gm_command_dispatch.py` = **126 passed** (ไฟล์ capture 37 ใบหลังรอบนี้) + มิวแทนต์ 5 ตัวข้างบน

**ชั้นชุดเต็ม** — `pytest tests/` บนต้นไม้ที่ merge `origin/main` แล้วเป็นขั้นสุดท้าย (`Already up to date`,
`cf961be` เป็น ancestor อยู่แล้ว): **12484 passed · 373 skipped · 26243 subtests passed · 1 failed** =
แถว `KNOWN_RED_MAIN:` ของ LANE-A ที่ยืนยันแล้วว่าแดงบน `origin/main` เปล่าเช่นกัน

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` = **PREFLIGHT PASS**
(cp874 · skips · mainmerge · census · branch · bridgesize · queuegrowth · filenamelen · scoreboard-manual)

## pf-adversary

`ADVERSARY_PENDING pirate-force-server#956` — สั่งไว้ต้นรอบพร้อมเริ่มเขียนโค้ด (เป้า: เส้นทาง
`except BaseException` ตอน shutdown · เทสเดิมที่ mock `os.unlink` ให้ล้มตลอด · การพิมพ์ทับ stdout/stderr
ของเทสอื่น · การนับ attempt · ผลกระทบต่อ rate limiter/โควตาใน `dispatch.py`) **ผลยังไม่คืนตอน push**
ตามกฎจึง push ตามเดิม และ **ไม่อ้างว่า "ผ่าน adversary"** · ข้อที่ผมเองเห็นก่อนแล้วแก้ไปในคอมมิตนี้คือ
guard รอบบรรทัด log (ข้อ 3 ในรายการที่สั่งไป) · รอบหน้าสั่ง adversary บนกิ่งนี้เป็นงานแรกถ้าผลยังไม่มา

## nonclaims

- **ไม่อ้าง**ว่าเกต Windows จะเขียว — ตรงกันข้าม รอบนี้คาดว่า `#956` จะถูก reaper ปิดด้วยแถวของ LANE-A
  เหมือน `#950` (ดูใบ ASK-COO)
- **ไม่อ้าง**ว่าอ่านชื่อเทสที่ทำให้เกตแดงจาก log ของเกตตรง ๆ — log ไม่พิมพ์บรรทัด `FAILED`
  (= ข้อ 2 ของลำดับ chief `1921` ที่ยังไม่ลง) เป็นการ **อนุมาน** จากผลชุดเต็ม + การรันแยกบน main เปล่า
- **ไม่อ้าง**ว่า retry นี้แก้อาการจริงบน Windows — ไม่มีเครื่อง Windows ในคลาวด์นี้ · สิ่งที่พิสูจน์ได้คือ
  ตรรกะการนับครั้ง/การหน่วง/สัญญาที่คืนให้ผู้เรียก และการที่ลินุกซ์ไม่เปลี่ยนพฤติกรรม
- **ไม่อ้าง**ว่ารอบนี้ขยับ `GT-279` หรือ P-3 — ยังรอเครื่องเจ้าของ ไม่ใช่รอโค้ดของสายนี้
- **ไม่อ้าง**ว่าผู้เล่นเห็นอะไรต่างบนจอ — งานรอบนี้เป็นความถูกต้องภายในของ sink/โควตา ไม่ใช่ฟีเจอร์

**รอบนี้ขยับ NOW/M ข้อไหน**: ขยับบรรทัด LANE-GM ของ NOW ("`_best_effort_unlink` retry 3 + doc (`2047`)")
= ทำเสร็จและอยู่ใน PR แล้ว · **ไม่ขยับ M2/M3/M4** เพราะงานที่ COO สั่งรอบนี้เป็นหนี้ทางเทคนิคของ sink
ไม่ใช่ขั้นบันไดไมล์สโตน · P-3 (`GT-279`) ไม่ขยับเพราะรอเครื่อง Panya

TWO_SESSIONS_SAME_SCENE: ไม่กระทบ — cleanup ของ capture เป็นการเขียนไฟล์ต่อการเรียกหนึ่งครั้ง
ไม่มี state ของฉากที่แชร์ข้าม session และไม่ส่งเฟรมใดออกไปหาไคลเอนต์

NO_FEATURE_WAITING: ไม่เกี่ยว — รอบนี้บริโภค COO-DECISION ไม่ใช่ผล RE

QUEUE_TRIAGE: ไม่แตะไฟล์คิวใด ๆ (เป็นงาน LANE-K ตาม NOW)

## จดหมายรอบนี้

- **บริโภค**: `20260906_2141_COO-DECISION-gm2046-report-received-lane-a-owns-it-LANE-GM.md`
  (ใบตอบรายงานของสายนี้เอง) → stub `.CONSUMED.txt` + สำเนาไป `notes_to_chief/consumed/`
- **ส่งใหม่**: `20260906_2229_LANE-GM-ASK-COO-gate-red-on-main-closes-every-pr.md` (ADDRESSEE: COO) —
  เกตแดงด้วยแถว `KNOWN_RED_MAIN` ทำให้ reaper ปิด PR ของ **ทุกสาย** ไม่ใช่แค่สายนี้ · เสนอ 3 ทาง
  เลือกทางที่ 1 ไปก่อนพร้อมป้าย `[สมมติของสาย LANE-GM - รอ COO ยืนยัน]`

## รอบหน้าทำอะไร

1. **ผล pf-adversary ของ `#956`** (ถ้าคืนหลังปลดล็อกรอบนี้) — งานแรกของรอบหน้า สั่งซ้ำบนกิ่งเดิมถ้าจำเป็น
2. **เช็ค `#956`**: ถ้าถูกปิดด้วยเกตแดง ให้ดูก่อนว่า `pytest_subset` ยังแดงด้วยแถวของ LANE-A อยู่ไหม
   (ถ้า A กลับ assertion แล้ว = เปิดใบใหม่ cherry-pick สองคอมมิตนี้ได้เลย) · **ถ้าแดงด้วยสาเหตุอื่น
   สองรอบติด = ห้ามส่งใบที่สาม ต้องเขียนจดหมาย COO ตามกฎ**
3. คำตอบของ COO ต่อใบ ASK `2229` (เดินข้อ 1/2/3) — ถ้าสั่งข้อ 2 ห้ามเปิด PR ใหม่จน main เขียว
4. `GT-279` ปุ่ม GM 3 หน้า — ยังรอเครื่อง Panya (ไม่ใช่ของสายนี้ที่จะเร่งได้)
5. ถ้าว่างจริง: `docs/PROMOTION_BACKLOG.md` หาแถวในเขต `gm/` ที่พิสูจน์แล้วแต่ยังติดแฟล็ก

SCOREBOARD: STUCK | ยังไม่มีอะไรใหม่บนจอผู้เล่นรอบนี้ — สิ่งที่ได้คือ capture sink ที่ล้างไฟล์ค้างได้จริง
เมื่อ Windows ถือ handle ชั่วครู่ (ลองซ้ำ 3 ครั้งแทนที่จะยอมแพ้ครั้งเดียว) และเมื่อยังลบไม่ได้ก็บอกชื่อไฟล์
กับทางแก้ (รีสตาร์ต process) แทนที่จะเงียบ · ติดที่แถว `KNOWN_RED_MAIN` ของ LANE-A ซึ่งทำให้เกตแดงและ
reaper ปิด PR ของทุกสาย | `pirate-force-server#956` (เปิดแล้ว ไม่ draft · `PF-AUTOMERGE: v4` ยืนยันด้วย GET ·
รวมคอมมิต O_BINARY ที่กู้จาก `#950`) + `pf_bridge#1572` (claim) + ชุดเต็ม 12484 passed / 1 failed = แถวของ LANE-A
