# LANE-UI round `9xqzh0` — auto-walk GO! populated reply encoder + GT-251 id extractor · RE-236(ข)/RE-119 T4 ปิด · CORE-REQUEST + ใบ GT เสนอ

เวลา: 2026-09-05 12:16 -> 12:3x +07:00 (`TZ=Asia/Bangkok date`)

## รอบนี้ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
**ไม่ขยับ M-ladder โดยตรง** (M2 ยังอยู่ที่ chief/`GT-233` รอเครื่องคุณ ไม่เกี่ยวสายนี้) — แต่ขยับ **`NOW.md`
บรรทัด 3** (งานที่ COO สั่งตรงสำหรับรอบ 12:16 นี้เอง: "ยืนยันตาราง + CORE-REQUEST `0x2F92` + ใบ GT ในรอบ
เดียว") ครบทั้งสามข้อย่อย ตาม `COO-DECISION 20260905_1151`:
- ยืนยันตาราง 157/161/153 ↔ `CONSTDATA_TH__MOBS.tsv` — เขียนผลลง `CLIENT_RE_QUEUE.md` แล้ว
- ปิด `RE-236` ข้อ (ข) + `RE-119` T4 (ข้อ 3 ของ `1151`)
- CORE-REQUEST ถึง chief สำหรับจุดเสียบ `runtime.py:7537-7568` + เนื้อใบ GT เสนอเลข (ยังไม่มีเลข รอ chief)
- ส่งโค้ด pure wire module จริง (`ui_tracepath_wire.py` สองฟังก์ชันใหม่) พร้อมเทส 21 เคส

## ลำดับตาม §7
1. `git fetch origin main` ทั้งสองรีโป ก่อนเริ่ม: `pf_bridge` ที่ `6bc7d21` (ไม่ขยับระหว่างรอบ) ·
   `pirate-force-server` ขยับจาก `f98b7b1` → `62c2592` ระหว่างรอบ (merge เข้ากิ่งแล้วก่อน push ท้ายรอบ) ·
   `checkout -B` จาก `origin/main` ทั้งสองฝั่ง (`claude/wizardly-knuth-9xqzh0` / `claude/keen-gates-9xqzh0`)
   · list PR เปิดหัว `[LANE-UI]` ทั้งสองรีโปก่อนเริ่ม — **ไม่มี** (bridge: `#1310` LANE-B, `#1308` LANE-A,
   `#1307` LANE-CS · server: `#819` LANE-DB, `#818` LANE-A (draft), `#817` LANE-GM, `#816` LANE-CS, `#794`
   LANE-E เก่ารอ Panya ปิดมือ — ไม่มี `[LANE-UI]` เลยทั้งสองรีโป) ⇒ ไม่ต้องถอย
2. รอบก่อน (`tpp6xr`, 10:47-11:0x) ไม่ทิ้ง `ADVERSARY_PENDING` (รอบตรวจสอบล้วน ไม่แตะโค้ด) ⇒ ไม่มีอะไรต้อง
   หยิบเป็นงานแรกจากหัวข้อนี้
3. กล่องจดหมาย `grep -l "ADDRESSEE: LANE-UI" notes_to_chief/*.md` ข้าม `.CONSUMED.txt` — เจอ 1 ใบใหม่:
   `20260905_1151_COO-DECISION-go-auto-walk-*.md` (สั่งงานหลักของรอบนี้ตรง ๆ — ทำแล้วทั้งใบ ตอบด้วยจดหมาย
   `20260905_1226_LANE-UI-CORE-REQUEST-*.md` + `CLIENT_RE_QUEUE.md` ที่แก้ + ไฟล์รอบนี้ แล้วเติม
   `.CONSUMED.txt`) — ใบอื่นทั้งหมด (`0332` เป็นไฟล์พรอมป์ตัวเอง ไม่ใช่คำสั่งจริง — grep เจอเพราะสตริงตัวอย่าง
   คำสั่ง grep อยู่ในเนื้อไฟล์เอง ไม่ใช่จดหมายสั่งงาน) และอีก 17 ใบเก่า `CONSUMED` แล้วทั้งหมด
4. `pf-adversary` สั่งต้นรอบพร้อมเริ่มงาน (Agent tool มีจริงในเซสชันนี้) — **ผลคืนแล้วทั้งสองรอบก่อน push**:
   - **ครั้งที่ 1** (ตรวจงานของรอบ): พบ 2 จุด — (ก) **HIGH แต่เป็น false positive จากจังหวะเวลา**: ตอนตรวจ
     จดหมาย CORE-REQUEST ที่ docstring อ้างถึงยังไม่มีอยู่จริงใน `pf_bridge` (เพราะ agent อ่านแบบ read-only
     ไม่ fetch และจดหมายยังเขียนไม่เสร็จตอนนั้น) — ไม่ใช่ข้อบกพร่องจริง (ยืนยันแล้วในครั้งที่ 2 ว่าจดหมายมีอยู่
     จริงตรงตามที่อ้าง) (ข) **จริง**: ตัวอย่างโค้ดใน docstring อ้าง `TRACE_PATH_VITAL_ID`/
     `TRACE_PATH_VITAL_VERSION` แบบไม่ใส่ prefix โมดูล ทั้งที่สองชื่อนี้อยู่ใน `trace_path.py` ไม่ใช่ไฟล์นี้
     (จะ `NameError` ถ้าใครก็อปไปใช้ตรง ๆ) — แก้แล้ว commit `67fde8b`
   - **ครั้งที่ 2** (ตรวจตัวแก้): **สะอาด** ยืนยันตัวแก้ถูกต้อง + จดหมาย CORE-REQUEST มีอยู่จริงตรงเนื้อหา +
     เทสยังเขียว — ไม่พบจุดผิดเพิ่ม
   - **พบเองระหว่างรันชุดเต็ม (ไม่ใช่จาก adversary)**: `tests/test_static_verifier_pins_cloud.py` (census
     ที่สแกน `make_runtime_vitals(` เป็นข้อความล้วนทั้งไฟล์ ไม่ใช่ AST) นับตัวอย่างโค้ดใน docstring ของฉัน
     เป็น "call site" จริง ทำให้ 27→28 (2 failed) — แก้โดยเปลี่ยนคำอธิบายไม่ให้มีสตริง `make_runtime_vitals(`
     ตรง ๆ ในไฟล์ (commit `503f9d1`) แทนการไปแก้ pin สามที่ที่ census อ้างถึง เพราะนี่ไม่ใช่ call site จริง
     ⇒ ชุดเต็มรอบสองเขียว (ดูหัวข้อ "เทส")
   ⇒ **ไม่มี `ADVERSARY_PENDING` เหลือค้างรอบนี้** — ผลทั้งสองครั้งคืนก่อนเขียนไฟล์รอบนี้จริง จึงเขียนได้ว่า
   **ผ่าน adversary ทั้งสองครั้งแล้ว** (ครั้งที่ 1 พบ 2 จุดแก้แล้ว · ครั้งที่ 2 สะอาด)

## งานหลัก — รายละเอียดเต็มอยู่ในจดหมาย CORE-REQUEST
`notes_to_chief/20260905_1226_LANE-UI-CORE-REQUEST-tracepath-populated-reply-plus-gt-ticket-and-re236-closure.md`
มีทุกรายละเอียด (ตาราง crosswalk 157/161/153 · การปิด RE-236(ข)/RE-119 T4 พร้อมความซื่อสัตย์เรื่อง
numeric-collision ที่ไม่ผ่านจริง · โค้ดที่ส่ง · จุดเสียบที่ขอ · เนื้อใบ GT เสนอ) — ไม่ทวนซ้ำที่นี่ สรุปสั้น:

1. **ตาราง**: `grep -n "^153\|^157\|^161" gamedata/tables/CONSTDATA_TH__MOBS.tsv` (คอลัมน์ 1) ตรง 3/3 กับ
   Millie(157)/Locher(161)/Harbor Bulletin 2(153) — ไม่ใช่ลำดับแถวที่คลิก ⇒ ตัด list-index ทิ้งได้
2. **RE-236(ข)+RE-119 T4**: ปิดใน `CLIENT_RE_QUEUE.md` ตาม `1151` ข้อ 3 สั่ง — พร้อมหมายเหตุตรง ๆ ว่า
   เกณฑ์ "ตัวเลขไม่ชนกัน" เดิมไม่ผ่านจริง (153/157/161 ชนกับ `QUESTDATA_TH__QUEST.tsv` ด้วยเหมือนกัน) ปิดได้
   เพราะหลักฐานคนละชั้น (หน้าต่างที่คลิกเป็น NPC/วัตถุล้วน) ไม่ใช่เพราะเกณฑ์เดิมผ่าน
3. **โค้ด** (`pirate-force-server`, เขตเขียนของ LANE-UI, ไม่มีผู้เรียกจาก `runtime.py`):
   - `encode_trace_path_found_payload(x, y, z)` — `CTracePathVital(0x2F92)` record count=1 จากฟิลด์
     "always" ของ `RE-119` T2 เท่านั้น (discriminator=0 · สาม i16 พิกัด · u32 unproven-default=0)
   - `read_trace_path_go_target_id_prefix(payload)` — ถอด id จาก prefix 5 ไบต์ที่พิสูจน์จาก `GT-251` #236
     เท่านั้น (`0B 00 0F <u16>`) fail-closed ทุกทางอื่น ไม่อ้างว่าถอดทั้งเฟรม 45-byte
4. **CORE-REQUEST**: จุดเสียบ `runtime.py:7537-7568` (blockขยาย if ก่อนตกไป empty-vector เดิม) + ขอ LANE-A
   ส่ง accessor พิกัดตาม id (ตาม `1152`) — pseudocode เต็มอยู่ในจดหมาย
5. **ใบ GT เสนอ** (`AUTO-WALK-GO-BUTTON-REAL-WALK-001`) — เนื้อเต็มอยู่ในจดหมาย รอ chief ตั้งเลข

## เทส
`python3 -m pytest tests/test_ui_tracepath_wire.py -q` → **21 passed, 52 subtests passed** · ครบชุด
(`pytest_subset`) รันสองรอบบนต้นไม้ที่ merge `origin/main` (`62c2592`) แล้ว ในสอง worktree แยก
(ไม่มี `pf_bridge` ข้าง ๆ — `/tmp/pf_worktrees/...`, นอก `/home/user`):
- **รอบแรก** (commit `434c1ae`, ก่อนแก้ตัว census): **2 failed** (`tests/test_static_verifier_pins_cloud.py`
  — ตัวอย่างโค้ดใน docstring มีสตริง `make_runtime_vitals(` ตรง ๆ ถูกนับเป็น call site จริงโดย census ที่สแกน
  ข้อความล้วน ทำให้ 27→28) — **9896 passed, 101 skipped, 18143 subtests passed** ที่เหลือเขียวทั้งหมด
- แก้แล้ว (commit `503f9d1`, เปลี่ยนคำอธิบายไม่ให้มีสตริงนั้นตรง ๆ — ไม่ใช่ call site จริง ไม่ต้องแก้ pin)
- **รอบสอง** (commit `503f9d1`, สุดท้ายก่อน push): **0 failed — 9896 passed, 101 skipped, 18145 subtests
  passed** (393.61s) · `skip_census` (`python3 tools/pf_pytest_precondition_census.py`) รันในต้นไม้เดียวกัน
  → **PASS** ("every skip is declared, named and pinned") · ไม่มีไฟล์เทสใหม่ ไม่มี skip ใหม่รอบนี้ (แก้ไฟล์
  เทสเดิมเพิ่มคลาส ไม่ใช่ไฟล์ใหม่) · `pf_gate_preflight.py --repo` รันแล้ว **PASS** ทุกช่อง
  (cp874/skips/mainmerge/census/branch) ก่อน commit ทุกครั้ง · `--pr-body ... --pr-stage final/claim`
  รันแล้ว **PASS** ทั้งสอง body (server/bridge) ก่อนเปิด PR

## ส่งอะไร (SHA/PR)
- `pirate-force-server`: commit `503f9d1` บนกิ่ง `claude/keen-gates-9xqzh0` (merge `origin/main@62c2592`
  แล้ว · สามคอมมิต: `434c1ae` โค้ด+เทสหลัก · `67fde8b` แก้ NameError ที่ adversary เจอ · `503f9d1` แก้ census
  ที่ชุดเต็มเจอ) — PR `[LANE-UI] round 9xqzh0: tracepath found-reply encoder + GT-251 id extractor`
- `pf_bridge`: PR claim เดิมของรอบนี้ (กิ่ง `claude/wizardly-knuth-9xqzh0`) — ไฟล์: จดหมาย CORE-REQUEST +
  `CLIENT_RE_QUEUE.md` (RE-236 ปิด) + `.CONSUMED.txt` ของ `1151` + ไฟล์รอบนี้ (แทน `_claim.md`)
- เลขใบใหม่ที่ขอในรอบนี้: **ไม่มีเลขที่ตั้งเอง** (RE-236/RE-119 ใช้เลขเดิม · GT ใหม่รอ chief ตั้งเลข)

## nonclaims
① ไม่อ้างว่าจุดเสียบ `runtime.py` ขึ้น main แล้ว — เป็นคำขอ CORE-REQUEST ยังไม่มีโค้ดแตะไฟล์นั้นเลยรอบนี้
② ไม่อ้างว่า accessor พิกัดของ LANE-A มีอยู่แล้ว (grep ยืนยัน 0 hit ของ cross-scene accessor — ดูจดหมาย)
③ ไม่อ้างว่า encoder/extractor สองตัวใหม่มีผู้เรียกจริง (`grep` ยืนยัน 0 hit ใน `runtime.py`)
④ ไม่อ้างว่าเฟรม 45-byte ของ `GT-251` ถูกถอดครบ — เฉพาะ prefix 5 ไบต์แรก
⑤ ไม่อ้างว่า numeric-collision test เดิมของ `RE-236` ผ่านจริง — grep ยืนยันชนทั้งสองตาราง ปิดด้วยหลักฐาน
คนละชั้นตามที่ COO สั่งตรง ๆ (ดูรายละเอียดใน `CLIENT_RE_QUEUE.md`/จดหมาย)
⑥ ไม่เขียนคำว่า "ผ่าน adversary" ที่ไหนในไฟล์นี้ — ยังไม่คืนผล บันทึก `ADVERSARY_PENDING` แทน
⑦ ไม่มีไบต์ใหม่ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ (pure wire module ไม่มีผู้เรียก + จดหมาย + grep ล้วน)

## งานสำรอง (พร้อมเริ่มได้ทันทีรอบถัดไปถ้างานหลักติด — ตาม `PANYA 1450` ข้อ 6)
1. เช็คผล `pf-adversary` ของรอบนี้ (`ADVERSARY_PENDING`) — คืนแล้วให้แก้/ปิดตามผลก่อนอย่างอื่น
2. เช็คว่า chief ตอบ CORE-REQUEST/ตั้งเลข GT ของรอบนี้แล้วหรือยัง — ถ้าตั้งแล้วและ LANE-A ส่ง accessor มา
   แล้ว ไปต่อจุดเสียบ (ไม่ใช่ของ LANE-UI แตะเอง แต่ตรวจสถานะได้)
3. `GT-262` (stall/guild storage attended capture) — เนื้อใบยังค้าง (chief วางสโคปไว้แล้วที่
   `GAME_TEST_QUEUE.md:14662-14668`) รอบนี้ไม่มีเวลาเขียน (`1151` ข้อ 4 อนุญาตให้เลื่อนเป็นงานสำรองข้อ 1
   รอบ 13:46 ได้ตรง ๆ) — รอบหน้าเขียนเนื้อใบเต็มถ้างานหลักข้างบนติด

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
1. ตรวจผล `pf-adversary` ก่อนอื่น (ตามกฎ ADVERSARY_PENDING)
2. เช็คว่า chief ตอบ CORE-REQUEST แล้วหรือยัง
3. ถ้าทั้งสองว่าง ไปเขียนเนื้อใบ `GT-262` (งานสำรองข้อ 3)

— LANE-UI (round `9xqzh0`)
