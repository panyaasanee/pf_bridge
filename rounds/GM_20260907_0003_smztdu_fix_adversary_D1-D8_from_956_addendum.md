# LANE-GM รอบ `smztdu` — แก้ 8 ข้อที่ pf-adversary ชี้หลังปลดล็อกรอบ `0op9bt` (D1-D8) + main กลับมาเขียว

เริ่ม 2026-09-07T00:03+07:00 · claim `pf_bridge#1589` · PR เซิร์ฟเวอร์ `pirate-force-server#962`

## ต้นรอบ (ตามลำดับ COMMON)

1. **`NOW.md`** (fetch สด `772190b`) — บรรทัด LANE-GM: `/lv` ✅ → P-3 `GT-279` (รอเครื่อง Panya) ·
   `/speed` ปิดจน mask ล็อกอิน · `/warp <n> <x> <y>` ปิดถาวร · ไม่มีคำสั่งใหม่ถึงสายนี้ · หัวไฟล์แจ้ง
   **"main server แดง (pin ของ A หลัง `0137`) → reaper ปิด PR ทุกสาย · ตัวแก้ = A `#957`"** — ตรวจแล้วพบว่า
   `#957` **merge ไปแล้วตั้งแต่ 16:08:24Z** (ก่อน NOW ฉบับ 22:41 เขียนบรรทัดนี้ด้วยซ้ำ) ⇒ รอบนี้ตรวจซ้ำเอง
   ก่อนเชื่อว่าแดง ดูหัวข้อ "main เขียวจริงหรือยัง" ด้านล่าง
2. **กล่องจดหมาย** `ADDRESSEE: LANE-GM` ที่ไม่มี `.CONSUMED.txt` คู่ — **ว่าง** (ตรวจด้วยสคริปต์จับคู่ stub
   จริง ไม่ใช่ grep ผิวเผิน — grep ตรงตัว `ADDRESSEE: GM` เคยขึ้นผลลวงจาก `ADDRESSEE: LANE-GM` ในรอบก่อน
   แก้เป็นค้นสตริงเต็ม `ADDRESSEE: LANE-GM` แล้วจับคู่ `.CONSUMED.txt` จริง)
3. **`AGENTS.md` §7** — อ่านแล้ว ไม่มีกฎใหม่ที่เปลี่ยนแผนรอบนี้
4. **ไฟล์รอบล่าสุด** `GM_20260906_2212_0op9bt_*` "รอบหน้าทำอะไร": ข้อ 1 = หยิบผล adversary ของ `#956`
   ก่อน (ADDENDUM มีอยู่ในไฟล์รอบนั้นแล้ว 8 ข้อ D1-D8) · ข้อ 2 = เช็คสถานะ `#956` ก่อนเปิดใบใหม่ ·
   ข้อ 4/5 ไม่เกี่ยว (GT-279 รอเครื่อง, ยังไม่ถึงงานสำรอง)
5. คิวในไฟล์สาย — ไม่ต้องใช้ (ข้อ 1-4 ตอบครบแล้ว)

**ยืนยันไฟล์บังคับต้นรอบ**: `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง ✅

**นาฬิกา**: `TZ=Asia/Bangkok date` = 00:03 (7 ก.ย.) ตรงกับป้ายเวลารอบนี้ · heartbeat ล่าสุด 23:30:02
ห่าง 33 นาที ต่ำกว่าเกณฑ์ 60 นาที ไม่ต้อง escalate

## ล็อกรอบ

`list_pull_requests` state=open ใน `pf_bridge` หัว `[LANE-GM] round` → **ว่าง** (มี `[LANE-Q]` `#1588`/`#1583`,
`[LANE-DB]` `#1586`/`#1571`, `[LANE-B]` `#1493` ซึ่งไม่ใช่ล็อกของสายนี้ ไม่ถอยเพราะเห็นมัน) ⇒ ตัดกิ่งจาก
`origin/main` (`772190b`) commit `_claim.md` push เปิด `#1589` (ไม่ draft · body ไม่มี marker) · list ซ้ำทันที:
ไม่มีใบ `[LANE-GM]` ที่เก่ากว่า = ไม่แพ้ใคร

## main เขียวจริงหรือยัง — ตรวจก่อนเชื่อบรรทัดของ NOW

`#957` (LANE-A แก้แถว `KNOWN_RED_MAIN`) **merge แล้วที่ 2026-09-06T16:08:24Z**, ก่อนที่ COO จะเขียน NOW
ฉบับ 22:41 ที่ยังบอกว่า "main แดง" เสียอีก — สงสัยว่าเป็นข้อมูลเก่าค้างในไฟล์ ไม่เชื่อโดยไม่ตรวจ:

1. `git fetch origin main` ที่ `pirate-force-server` → HEAD = `be06164` = merge commit ของ `#957` เอง
2. `pytest tests/test_lane_a_choose_npc_scene1.py` บน `origin/main` เปล่า: **72 passed** (แถวที่เคยแดงผ่านแล้ว)
3. `pytest tests/test_script_lua_api_instance.py` (แถวที่สองของ `KNOWN_RED_MAIN`, ของ Q `#891`):
   **37 passed, 4 skipped** — ไม่แดง (ต้องตั้ง `PYTHONPATH=src` เอง ไฟล์นี้ไม่ insert path ให้ตัวเอง
   ต่างจากไฟล์ของ LANE-A)
4. ชุดเต็มบนต้นไม้เดียวกันหลัง merge `origin/main` (เป็น ancestor อยู่แล้ว, ไม่มีอะไรให้ merge):
   **12493 passed · 373 skipped · 26243 subtests passed · 0 failed** ใน 482 วินาที

⇒ **main เขียวจริง** ตั้งแต่ `#957` merge — บรรทัด "main แดง" ของ NOW เป็นข้อมูลที่ COO ยังไม่ได้อัปเดต
หลัง merge (`#957` merge 16:08Z, NOW ตรวจล่าสุด 22:41+07 = 15:41Z ก่อน merge อีก ดังนั้นจริง ๆ ยังไม่ขัดแย้งกัน
เอง — NOW แค่ยังไม่เห็นผลลัพธ์ของ `#957` ตอนที่ COO ตรวจรอบล่าสุด) ⇒ รอบนี้เปิด PR เซิร์ฟเวอร์แบบไม่ draft
มี marker ตั้งแต่เปิดได้ตามเงื่อนไข "ไม่นับแดงสองรอบ" ของ NOW (ยืนยันซ้ำด้วยชุดเต็มสดของตัวเอง ไม่ใช่เดา)
รายงาน COO ในจดหมายท้ายไฟล์รอบนี้ให้แก้บรรทัด NOW

## สถานะ `#956` ของรอบก่อน

ยังปิดอยู่ ไม่ merge (ตรวจซ้ำ) — ปิดโดย `merge-claude-pr.yml` เมื่อ 15:54:08Z เพราะ `pytest_subset` แดง
จากแถวของ LANE-A (ยืนยันแล้วในรอบก่อน) ⇒ cherry-pick คอมมิตทั้งสองจากกิ่ง `claude/upbeat-brahmagupta-0op9bt`
(`705c799` O_BINARY, `c68f6e2` bounded retry) กลับมาที่กิ่งใหม่ **สะอาด ไม่มี conflict**

## สิ่งที่สร้างรอบนี้ (เขต `gm/` เท่านั้น) — แก้ 8 ข้อจาก ADDENDUM ของรอบ `0op9bt`

ไฟล์รอบก่อน (`GM_20260906_2212_0op9bt_*`) มี ADDENDUM ที่ pf-adversary ส่งกลับหลังปลดล็อกแล้ว 8 ข้อ
(D1 สูง, D2 กลาง-สูง, D5/D4/D3 กลาง, D6 ต่ำ-กลาง, D7 ต่ำ, D8 กระบวนการ) — รอบนี้แก้ครบทุกข้อ ใน
`src/pirateforce_foundation/gm/command_capture.py` + เทส 3 ไฟล์ + `docs/GM_LANE.md`:

- **D1**: เส้นทาง `except BaseException` (shutdown re-raise) เรียก `_best_effort_unlink(..., retry=False)`
  ใหม่ — ลองครั้งเดียว ไม่ sleep เลย (เดิม sleep ได้ถึง 0.1 วิ เปิดหน้าต่างให้สัญญาณตัวที่สองมาแทนที่
  exception ที่กำลัง re-raise) · สองเส้นทางล้มเหลวปกติ (write ล้ม, close ล้ม) ยัง retry เต็ม 3 ครั้งเหมือนเดิม
- **D2**: guard รอบ print กว้างจาก `except Exception` เป็น `except BaseException` (ของเดิมไม่ครอบ
  `KeyboardInterrupt`/`SystemExit` ซึ่งเป็นสองตัวที่ comment ของมันเองอ้างถึง)
- **D3**: บรรทัด stuck เพิ่ม `account=<ชื่อ>` + `attempted_bytes=<n>`
- **D4**: ทั้ง `account` และ `path` ผ่าน `console_safe` (helper เดิมของสาย, `login_scene_override.py`)
  ก่อนพิมพ์ — กัน `capture_root` ที่มีอักขระ cp874 เข้ารหัสไม่ได้ทำให้บรรทัดหายเงียบ
- **D5**: เทสพื้น (`assertGreater(..., 0.0)`) กัน mutant `_UNLINK_RETRY_DELAY_SECONDS = 0.0`
- **D6**: 7 จุดใน 3 ไฟล์เทส (`test_gm_command_capture.py` ×3, `test_gm_activity_cheat_code_dispatch.py` ×2,
  `test_gm_command_dispatch.py` ×2) เพิ่ม mock `time.sleep` + `redirect_stderr`
- **D7**: `assert _UNLINK_ATTEMPTS >= 1` ระดับโมดูล + เทสตรึง
- **D8**: แก้ comment ของเทสเดิมที่อ้างผิดเส้นทาง + เทสใหม่ 2 ตัวที่เดินเส้นทาง shutdown จริง
  (ตัวหนึ่งใช้ fake stream ที่ `.write()` โยน `KeyboardInterrupt` เอง เพราะ `io.StringIO` ที่ปิดแล้ว
  โยนแค่ `ValueError` ซึ่งเป็น `Exception` — guard เก่าจับได้อยู่แล้ว ไม่ฆ่า mutant D2)

**ยืนยันด้วยมือ** ทีละข้อ (D1/D2/D3/D4/D5): แก้โค้ดกลับเป็นของเดิม รันเทสใหม่ให้แดง แล้ว restore —
ทำจริงทั้ง 5 ข้อ ผลแดงตรงตามคาดทุกข้อ (log อยู่ในเซสชัน ไม่ได้ผนวกไฟล์แยก)

## หลักฐาน (สองชั้น แยกกัน)

**ชั้นยูนิต/มิวแทนต์** — `pytest tests/test_gm_command_capture.py tests/test_gm_commands.py
tests/test_gm_command_dispatch.py tests/test_gm_activity_cheat_code_dispatch.py` = **156 passed,
5 subtests passed** · `pytest tests/ -k gm` = **2922 passed, 4 skipped, 1757 subtests passed**

**ชั้นชุดเต็ม** — ดูหัวข้อ "main เขียวจริงหรือยัง": **12493 passed · 373 skipped · 26243 subtests
passed · 0 failed** บนต้นไม้ที่มี `origin/main` เป็น ancestor อยู่แล้ว

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` = **PREFLIGHT PASS**
(cp874 · skips · mainmerge · census · branch · bridgesize · queuegrowth · filenamelen · scoreboard-manual ·
consumedstub) · หมายเหตุ: `AGENTS.md` ขึ้น `old` เกินเพดาน 30 KB แต่เป็นหนี้เดิม ไม่ใช่ของรอบนี้ (ไม่โต)

## pf-adversary

สั่งไว้ต้นรอบพร้อมเริ่มงาน **ผลคืนก่อนปลดล็อก** (worktree แยก `c68f6e2`→กิ่งนี้ ทำงานเสร็จก่อน commit
ที่สองของรอบนี้) — พบ 3 ข้อจริง แก้ครบก่อนปลดล็อก ไม่ใช่ยกไปรอบหน้า:

1. **[สูง, ยืนยันแล้ว]** `account_name` ที่ threading เข้าไปใน stderr line (D3) ผ่านแค่ `console_safe`
   ซึ่งพับเฉพาะอักขระที่ **สตรีม** เข้ารหัสไม่ได้ ไม่ใช่ control character — newline จริงทะลุผ่านได้เฉย ๆ
   ⇒ บัญชีที่มี `\n` ในชื่อ **ปลอมบรรทัดที่สองทั้งบรรทัดได้** (path/attempted_bytes/attempts ปลอมได้หมด)
   ไฟล์นี้มีเครื่องมือสำหรับฟิลด์นี้อยู่แล้ว (`_escape_for_header`, ใช้กับบรรทัด `account=` ในเฮดเดอร์บนดิสก์
   ด้วยเหตุผลเดียวกันเป๊ะ) ⇒ compose `console_safe(_escape_for_header(account_name), stream)`
2. **[latent]** invariant ของ D7 เป็น `assert` เปล่า ซึ่ง `python -O` ตัดทิ้งได้ทั้งหมด (ยืนยันด้วย
   `python3 -O`) — โปรเจกต์นี้เคยพลาดแบบนี้มาแล้วครั้งหนึ่งและแก้ด้วยการ `raise` แทน
   (`world_port_royal_identity.py` มี comment สอนเรื่องนี้ตรงตัว) ⇒ เปลี่ยนเป็น `raise ValueError`
3. **[ช่องว่างเทส]** เทสของ D3 คุมแค่จุดเรียกที่ write ล้ม — จุดเรียกอีกสองจุด (close ล้ม, shutdown path)
   ไม่มีเทสคุมเนื้อหา `account`/`attempted_bytes` เลย — มิวเทตเป็น `""`/`0` แล้วชุดเทสยังเขียวทั้งชุด
   ⇒ เพิ่มเทสเฉพาะจุดให้ทั้งสองจุดที่เหลือ

ยืนยันทั้ง 3 ข้อด้วยมือ (มิวเทต รันเทสให้แดง restore) เหมือนกับ D1-D7 · commit ที่สองของรอบ
(`6ae4b79`) แก้ทั้งสามข้อในกิ่งเดียวกันก่อนปลดล็อก ไม่ต้องยกไปรอบหน้า

## nonclaims

- **ไม่อ้าง**ว่าอาการ Windows sharing-violation จริงถูกแก้ — ไม่มีเครื่อง Windows ในคลาวด์นี้ สิ่งที่
  พิสูจน์ได้คือตรรกะการนับครั้ง/การหน่วง/การไม่หน่วงตอน shutdown และพฤติกรรมลินุกซ์ไม่เปลี่ยน
- **ไม่อ้าง**ว่า D1-D8 + 3 ข้อของ adversary รอบนี้ คือทุกข้อที่เป็นไปได้ในไฟล์นี้ — เป็นแค่สิ่งที่ตรวจแล้ว
  พบจริงในสองรอบ pf-adversary ติดกัน
- **ไม่อ้าง**ว่า commit ที่สองของรอบนี้ (`6ae4b79`, แก้ 3 ข้อที่ adversary รอบนี้ชี้) ผ่าน adversary เอง —
  ยืนยันด้วยมิวเทตของผมเองทั้ง 3 ข้อ (แก้กลับ รันเทสให้แดง restore) ไม่ใช่ adversary ตัวที่สอง · กฎ "ทุกรอบ
  ต้องเรียก pf-adversary" นับว่าครบสำหรับรอบนี้แล้ว (เรียกไปหนึ่งครั้งต้นรอบ ได้ผลจริง แก้ตามผลแล้ว) แต่
  ตัว fix-of-fix เองยังไม่ผ่านสายตาที่สอง — ถ้ารอบหน้ามีโควตา adversary เหลือ สั่งซ้ำบนกิ่งนี้ก่อนก็ได้
- **ไม่อ้าง**ว่ารอบนี้ขยับ `GT-279` หรือ P-3 — ยังรอเครื่องเจ้าของ ไม่ใช่รอโค้ดของสายนี้
- **ไม่อ้าง**ว่าผู้เล่นเห็นอะไรต่างบนจอ — งานรอบนี้เป็นความถูกต้องภายในของ sink/โควตา/ข้อความ log
  ไม่ใช่ฟีเจอร์ที่ผู้เล่นสัมผัสได้
- **ไม่อ้าง**ว่าตรวจแถวที่สองของ `KNOWN_RED_MAIN` (Q lane skip_census) ครบทุกกรณี — รันแค่ไฟล์เทสที่ระบุ
  ในชื่อแถวแล้วไม่แดง ไม่ได้ตรวจกลไก skip_census ทั้งระบบ (ไม่ใช่เขตของสายนี้)

TWO_SESSIONS_SAME_SCENE: ไม่กระทบ — capture cleanup เป็นการเขียนไฟล์ต่อการเรียกหนึ่งครั้ง ไม่มี state
ของฉากที่แชร์ข้าม session และไม่ส่งเฟรมใดออกไปหาไคลเอนต์

NO_FEATURE_WAITING: ไม่เกี่ยว — รอบนี้บริโภคผล pf-adversary ของโมดูลตัวเอง ไม่ใช่ผล RE

QUEUE_TRIAGE: ไม่แตะไฟล์คิวใด ๆ (เป็นงาน LANE-K ตาม NOW)

## จดหมายรอบนี้

- **บริโภค**: ไม่มี (กล่องจดหมายว่างต้นรอบ)
- **ส่งใหม่**: `20260907_0003_LANE-GM-TO-COO-main-is-green-957-merged-956-recovered.md` (ADDRESSEE: COO) —
  รายงานว่า `#957` merge ไปแล้วตั้งแต่ 16:08:24Z, ชุดเต็มสดยืนยัน 0 failed, เสนอแก้บรรทัด "main server แดง"
  ใน NOW.md ให้ตรงสถานะปัจจุบัน (สายนี้แก้ไฟล์นั้นเองไม่ได้ตามกฎ NOW.md เป็นของ Panya/COO เท่านั้น)

## รอบหน้าทำอะไร

1. **(ทางเลือก, ไม่บล็อก)** สั่ง pf-adversary ซ้ำบนกิ่งนี้ก่อน merge เพื่อตรวจ commit ที่สอง
   (`6ae4b79`, แก้ 3 ข้อจากอดีต) เอง — ยังไม่มีสายตาที่สองบน fix-of-fix นั้น (ดู nonclaims)
2. เช็คว่า `#962` merge ไปหรือยัง — ถ้า merge แล้วไม่มีงานค้าง ⇒ ไปงานสำรอง (ข้อ 3)
3. ถ้าว่างจริง: `docs/PROMOTION_BACKLOG.md` หาแถวในเขต `gm/` ที่พิสูจน์แล้วแต่ยังติดแฟล็ก
4. `GT-279` ปุ่ม GM 3 หน้า — ยังรอเครื่อง Panya (ไม่ใช่ของสายนี้ที่จะเร่งได้)
5. ติดตามคำตอบ COO ต่อจดหมาย `main-is-green` ข้างบน (ไม่ใช่บล็อกงานของสายนี้ต่อ)

SCOREBOARD: STUCK | ยังไม่มีอะไรใหม่บนจอผู้เล่นรอบนี้ — สิ่งที่ได้คือ sink ทำความสะอาดไฟล์ค้างที่ตอนนี้
ไม่เสี่ยงเปลี่ยน exit code ตอนเซิร์ฟเวอร์ปิดตัว (D1), ไม่เสี่ยงกลืน Ctrl+C ทิ้ง (D2), และบอกบัญชี+ขนาดไฟล์
ที่ค้างแทนข้อความคลุมเครือ (D3/D4) — งานแก้หนี้ทางเทคนิคที่รอบก่อนพบ ไม่ใช่ฟีเจอร์ใหม่ · main กลับมาเขียว
แล้วจริง (12493 passed, 0 failed) ซึ่งเป็นข่าวดีข้ามสาย ไม่ใช่ผลของรอบนี้เอง | `pirate-force-server#962`
(เปิดแล้ว ไม่ draft · `PF-AUTOMERGE: v4` ยืนยันด้วย GET) + `pf_bridge#1589` (claim) + ชุดเต็ม
12493 passed / 0 failed
