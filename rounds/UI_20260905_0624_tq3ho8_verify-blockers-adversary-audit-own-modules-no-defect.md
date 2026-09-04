# LANE-UI round `tq3ho8` — re-verify every open blocker against fresh `main`, then adversarial audit of LANE-UI's own shipped wire modules (no new opcode/attended-capture work available this round)

เวลา: 2026-09-05 06:24 -> 06:31 +07:00 (`TZ=Asia/Bangkok date`)

## รอบนี้ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
**ไม่ขยับ M-ladder** (M2 คงเดิม) และ**ไม่ปิด "รอเครื่องคุณ" ข้อไหนใหม่**. งานหลักของสายนี้ (`NOW.md` บรรทัด 50,
UI-A/UI-B) ยังบล็อกที่ผล attended `HYP-PF-040` ที่ยังไม่กลับมา, คิวข้อ 4/5 (auto-walk/ร้านค้า NPC) ยังบล็อกที่
CORE-REQUEST ถึง chief/LANE-DB ที่ยังไม่ตอบ, และจดหมายขอเลข RE ใหม่ (`0456`, รอบก่อน) ยังไม่มีคำตอบจาก chief —
**ทั้งสามอย่างตรวจสดรอบนี้ ไม่ใช่แค่เชื่อไฟล์รอบก่อน** (ดูหัวข้อถัดไป) ยังบล็อกเหมือนเดิมทุกจุด ⇒ ไม่มีงานใหม่ที่
เริ่มได้ทันทีในคิวหลัก รอบนี้จึงใช้เวลาไปกับ (ก) ยืนยันบล็อกทุกจุดสดจาก `main`/mailbox แทนที่จะสมมติว่ายังบล็อก
(ข) สั่ง `pf-adversary` ล่าบั๊กจริงในโมดูลที่สายนี้เป็นเจ้าของเอง (`ui_*.py`/`lane_hooks/lane_ui_*.py`) เพราะเป็น
งานเดียวที่เริ่มได้ทันทีไม่ต้องรอใคร — **ผลคือไม่เจอบั๊กจริง** (ดูหัวข้อ ADVERSARY) จึงไม่มี diff โค้ดรอบนี้

## ลำดับตาม §7
1. `git fetch origin main` ทั้งสองรีโป (bridge -> `d669c11`, server -> `7b164ac`) · `checkout -B` จาก `origin/main`
   ทั้งสองฝั่ง · list PR เปิดหัว `[LANE-UI]` ทั้งสองรีโปก่อนเริ่ม — **ไม่มี** ทั้งสองรีโป (server PR ล่าสุดหัว
   `[LANE-UI]` ปิด/merge แล้วก่อนรอบนี้ · bridge ไม่มี PR เปิดหัว `[LANE-UI]` เลยก่อน claim รอบนี้) ⇒ ไม่ต้องถอย ·
   claim `pf_bridge#1271` หัว `[LANE-UI] round tq3ho8: claim` กิ่ง `claude/quiet-lovelace-tq3ho8`
2. รอบก่อน (`npixtd`, 04:50) ไม่ทิ้ง `ADVERSARY_PENDING` ไว้ (ผลคืนและแก้ครบก่อน push รอบนั้นแล้ว) ⇒ ไม่มีอะไรต้อง
   หยิบเป็นงานแรกจากหัวข้อนี้
3. กล่องจดหมาย `grep -l "^ADDRESSEE: LANE-UI" notes_to_chief/*.md` ข้าม `.CONSUMED.txt` — **ไม่มีใบใหม่** (แพตเทิร์น
   เดียวที่ตรงยังเป็น `0332` ไฟล์พรอมป์ประจำสายเอง `ADDRESSEE: COO` ไม่ใช่จดหมายสั่งงาน — ตรวจซ้ำด้วยหัว
   `^ADDRESSEE:` เป๊ะเหมือนทุกรอบ)
4. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงาน — เพราะไม่มีจดหมาย/โค้ดร่างใหม่ให้ตรวจ (คิวหลักบล็อกหมด) จึงสั่งให้ล่า
   บั๊กจริงในโมดูลที่สายนี้ถือเองแทน (ดูหัวข้อ ADVERSARY) — **ผลคืนก่อนจบรอบ ไม่มี `ADVERSARY_PENDING` ค้าง**

## ตรวจงานสำรองของรอบก่อน (`npixtd`) สดจาก `main`/mailbox รอบนี้ — ทั้งสามข้อยังบล็อกเหมือนเดิม
1. **จดหมาย `0456` (ขอเลข RE ใหม่ stall/guild storage) — chief ยังไม่ตอบ**: `ls -t notes_to_chief/*.md | head -8`
   รอบนี้ ใบล่าสุดคือ `0555` (LANE-A) ไม่มีใบตอบ `0456` เลย · `grep -rn "0456" notes_to_chief/*.md
   CLIENT_RE_QUEUE.md` เจอแค่ไฟล์ต้นฉบับเอง ไม่มีการอ้างถึงจากใบอื่น ⇒ ยังรอ ไม่ใช่ตัวบล็อกที่สายนี้แก้เองได้
   (เวลาผ่านมา ~1.5 ชม. จาก 04:56 ยังไม่ถึงเกณฑ์ที่ต้องทวง)
2. **ผล attended `HYP-PF-040`** (กิ่งทิ้ง `e678a37...` บน `pirate-force-server`, `logout_dialog_open_hypothesis`) —
   ยังไม่กลับมา: `git ls-remote origin` ยืนยันกิ่งทิ้งยังอยู่ (ไม่ถูกลบ, ไม่มี commit ใหม่) · `ls -t
   notes_to_chief/*.md` ที่มีคำว่า `KA1A` ล่าสุดคือ R314 (`0233`, ตอบเรื่อง `GT-247`/scene-load แล้ว) ไม่มีผลใหม่
   ของ `GT-184`/`GT-186` boot-from-hash รอบนี้ ⇒ ยังรอเครื่อง Panya จริง (`NOW.md` ข้อ 5 ในหัวข้อ "รอเครื่องคุณ"
   ยังพูดสถานะเดิม ไม่ใช่ตัวที่ค้างเพราะ LANE-UI ไม่ทำอะไร)
3. **CORE-REQUEST `0347`** (fire `lane_hooks.fire(...)` ที่ `runtime.py:7509` หลัง `TRACE_PATH_REQ_VITAL_ID` check,
   เขต chief) — **อ่าน `runtime.py:7495-7530` ตรง ๆ รอบนี้** (ไม่ใช่ grep เดา): บรรทัด 7509 ยังเป็นแค่
   `if nested_id == trace_path.TRACE_PATH_REQ_VITAL_ID:` เฉย ๆ ไม่มี `lane_hooks.fire(...)` เรียกเลย (มี `fire()`
   9 จุดในไฟล์ ทั้งหมดอยู่ที่ `_FRIEND_MAIL_PARTY_TRADE_DISPATCH`'s call sites บรรทัด 8452-8573 ไม่ใช่ 7509) ⇒
   ยังไม่รับ · `registered_but_not_fired = ("vital_inbound_trace_path_req_vital",)` ใน
   `lane_hooks/lane_ui_tracepath_wire_log.py` ยังต้องอยู่ต่อ

เพิ่มอีกจุด (ไม่ได้อยู่ในสามข้อของรอบก่อน แต่เป็นทางที่รอบก่อนวางไว้เป็น "รอบถัดไปทำอะไรต่อ" ข้อ 2): **CORE-REQUEST
`0621`** (LANE-DB, shop money/backpack interface) — `grep -rl "0621\|TradeCmdVital"` รอบนี้ยังไม่เจอใบตอบใหม่จาก
LANE-DB · `grep -n "TRADE_CMD_VITAL\|active_store_session" src/pirateforce_foundation/runtime.py` (server repo) =
0 hit เหมือนเดิม ⇒ ยังบล็อกทั้งสองทาง (chief wire predicate + LANE-DB interface)

## ADVERSARY — ล่าบั๊กจริงในโมดูลของสายนี้เอง (งานเดียวที่เริ่มได้ทันทีรอบนี้)
เนื่องจากคิวหลักบล็อกครบทุกทาง (attended/chief/LANE-DB) และไม่มีจดหมายใหม่ที่ต้องเขียน สั่ง `pf-adversary` ให้ล่า
บั๊กจริงใน `ui_social_wire.py`/`ui_friend_wire.py`/`ui_mail_wire.py`/`ui_party_wire.py`/`ui_trade_wire.py`/
`ui_tracepath_wire.py` และทั้งห้า `lane_hooks/lane_ui_*_wire_log.py` — ไฟล์ที่สายนี้เป็นเจ้าของเต็มตัวและแก้ได้
วันนี้โดยไม่ต้องรอใคร

**ผล: ไม่เจอบั๊กจริง** ตรวจแล้วแปดทาง (round-trip mismatch, trailing-bytes bypass, wstring edge case —
huge-length/odd-length/lone-surrogate/empty/embedded-NUL, `require_exhausted`'s partial-consume detection ที่ชั้น
log, `console_safe`/hex-truncation crash surface, negative/overflow field values, dispatch wiring ตรงกับ
`runtime.py`'s `_FRIEND_MAIL_PARTY_TRADE_DISPATCH`) + รันชุดเทสที่เกี่ยวในสภาพ worktree แยก (`901 passed, 10
skipped` — 10 skip ไม่เกี่ยวไฟล์ของสายนี้เลยสักตัว) — **โมดูลเหล่านี้ผ่านรอบ adversary ก่อนหน้าไปแล้วจริง**
(trailing-bytes fix ตาม COO-DECISION `20260904_1745` ข้อ 2 ปิดคลาสบั๊กที่คาดว่าจะเจอ)

จุดสังเกตหนึ่งจุด (ไม่ใช่บั๊ก เพราะยังไม่มีผู้เรียกจริงที่จะชนมันได้): `encode_untagged_wstring` จะ raise
`UnicodeEncodeError` แบบไม่จับถ้าป้อน Python `str` ที่มี lone surrogate — ทุก `decode_*` fail-closed คืน `None`
แต่ฝั่ง encode ยังไม่มี contract แบบเดียวกัน วันนี้ไม่มีผลเพราะ `encode_*` ถูกเรียกจากเทส/re-encode ค่าที่ decode
มาแล้วเท่านั้น ไม่มี composer ที่สร้างค่าจาก state สดของเกม — บันทึกไว้เป็นข้อสังเกตสำหรับวันที่ CORE-REQUEST
`0347` รับแล้วมี composer จริงตัวแรก ไม่ใช่ตัวบล็อกวันนี้

**ไม่มี `ADVERSARY_PENDING` ค้างข้ามรอบนี้** — ผลคืนและตรวจครบก่อน push รอบนี้แล้ว

## เช็คที่ทำเองก่อน push
- ไม่มีไฟล์โค้ด/เทสถูกแตะรอบนี้ในทั้งสองรีโป (ยืนยัน blocked สด + adversary audit เท่านั้น ไม่มีบั๊กให้แก้) ⇒
  ไม่ต้องรัน `pf_gate_preflight.py --repo` (กติกานั้นบังคับเฉพาะรอบที่มี PR เซิร์ฟเวอร์)
- รัน baseline ก่อนสั่ง adversary เพื่อยืนยันจุดเริ่ม: `pytest tests/test_ui_*.py tests/test_ui_lane_hooks_wire_log.py
  -q` บน `pirate-force-server` = `89 passed, 25 skipped` (ไม่เปลี่ยนหลัง adversary เพราะไม่มีการแก้ไฟล์จริง)
- ตรวจ body ของ claim PR (`pf_bridge#1271`) ด้วย `tools_bridge/pf_gate_preflight.py --pr-body <ไฟล์> --pr-stage
  claim` ก่อนเปิด — **`[prbody] PASS`** (ไม่มีโทเคน marker) · จะรันซ้ำ `--pr-stage final` ก่อน PATCH body สุดท้าย
- ป้ายเวลาเทียบกับ `_BRIDGE_HEARTBEAT.txt` ล่าสุด (`2026-09-05T06:08:01+07:00`) — ห่างไม่เกิน 60 นาทีตอนเขียนรอบนี้

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `#1271` หัว `[LANE-UI] round tq3ho8: claim` กิ่ง `claude/quiet-lovelace-tq3ho8` จาก `origin/main`
  — ไฟล์ใหม่: ไฟล์รอบนี้เท่านั้น (แทน `_claim.md`) — PATCH body มี `PF-AUTOMERGE: v4` = ปลดล็อก
- `pirate-force-server`: **ไม่มี PR รอบนี้** — ไม่มีโค้ด/เทสเปลี่ยนแปลง (adversary audit ไม่เจอบั๊กให้แก้ · ทุกคิวหลัก
  บล็อกที่ external party) — ตามธรรมเนียมรอบตรวจสอบล้วนก่อนหน้านี้ (`llcmcr`, `npixtd`) ที่ก็ไม่มี PR เซิร์ฟเวอร์
  เช่นกันเมื่อไม่มีอะไรให้ส่งจริง
- ไม่มีเลข GT/RE ใหม่ในคิวรอบนี้

## nonclaims
① ไม่อ้างว่าโมดูล wire ของสายนี้ปลอดบั๊กถาวร — แค่ pf-adversary รอบนี้ (8 มุมตรวจ + full test run ใน worktree)
ไม่เจอ ไม่ใช่การพิสูจน์ปลอดบั๊กทางคณิตศาสตร์
② ไม่อ้างว่า `encode_untagged_wstring`'s lone-surrogate gap เป็นบั๊กที่ต้องแก้วันนี้ — ยังไม่มีผู้เรียกจริงที่จะ
ชนมันได้ (nonclaim นี้ต่างจากการปิดเงียบ: บันทึกไว้ให้ผู้เขียน composer ตัวแรกเห็นเมื่อ `0347` รับแล้ว)
③ ไม่ยืนยันว่า chief/LANE-DB/Panya จะตอบ/รันเมื่อไหร่ — แค่ตรวจว่ายังไม่มีอะไรใหม่รอบนี้
④ ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ (ตรวจ+เทสใน worktree ล้วน ไม่มีโค้ดเปลี่ยน ไม่มีการบูตเกม)
⑤ ไม่แก้หัวใบ `GT-253` ที่ค้างข้อมูลเก่า (ไม่ใช่เขตเขียนของสายนี้ — บันทึกซ้ำให้ chief เห็นตอนกวาดคิว ยังไม่แก้เอง
ตั้งแต่รอบ `hq4wtb`/`npixtd`)

## งานสำรอง (พร้อมเริ่มได้ทันทีรอบถัดไปถ้างานหลักติด — ตาม `PANYA 1450` ข้อ 6)
1. เช็คว่า chief ตอบจดหมาย `0456` (ตั้งเลข RE ใหม่ stall/guild storage) แล้วหรือยัง — ถ้าตั้งแล้ว กรอกเนื้อใบเต็มลง
   `CLIENT_RE_QUEUE.md` ในรอบเดียวกัน (ตามธรรมเนียม `RE-235`/`RE-237`)
2. เช็คผล attended `HYP-PF-040` (กิ่งทิ้ง `e678a37`) กลับมาหรือยัง — ถ้ากลับมา อ่านผลแล้วตัดสิน UI-A/UI-B ต่อ
   (พลิกถาวรบน main ถ้าผลบวก / falsified ปิดถ้าลบ ตาม `COO-DECISION 20260904_2047`)
3. เช็คว่า chief รับ CORE-REQUEST `0347` (fire trace_path observer, `runtime.py:7509`) แล้วหรือยัง — ถ้ารับแล้ว
   ลบ `registered_but_not_fired` ออกจาก `lane_ui_tracepath_wire_log.py` ในรอบเดียวกัน

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
1. เช็คงานสำรองข้อ 1-3 ข้างบนตามลำดับ
2. ถ้าไม่มีอะไรขยับสามรอบติดต่อกัน (`npixtd`/`tq3ho8`/รอบถัดไป) ให้พิจารณาเขียนจดหมาย `ADDRESSEE: COO` สรุปห่วงโซ่
   บล็อกทั้งหมดในที่เดียว (ไม่ใช่รอบนี้ เพราะยังไม่ถึงเกณฑ์ "ไม่มีอะไรทำได้" จริง — attended queue ของ Panya เดินตาม
   จังหวะปกติของเธอ ไม่ใช่ค้างเพราะมีใครทำผิด)
3. ถ้ายังไม่มีอะไรขยับ กลับไปดูว่า CORE-REQUEST `0621` (ร้านค้า NPC เงิน/กระเป๋า, LANE-DB) มีความคืบหน้าหรือยัง

— LANE-UI (round `tq3ho8`)
