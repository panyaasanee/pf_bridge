# LANE-UI round `urhd6h` — decoder-level fail-closed on trailing bytes (COO-DECISION `20260904_1745` item 2, backup item 1)

เวลา: 2026-09-04 18:27 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ — งานนี้เป็นความถูกต้องของ decoder (fail-closed) ไม่ใช่ปุ่ม/ฟีเจอร์ที่ผู้เล่นเห็นสิ่งที่สัญญาบนจอ
ตามนิยาม "ปุ่มทำงาน" ของพรอมป์สายเอง ⇒ ไม่มีใบ GT ปิดรอบนี้ · บันไดที่เกี่ยวกับ LANE-UI ใน `NOW.md` (UI-A/UI-B,
ร้านค้า NPC, สารบัญ) ค้างที่เดิมทั้งหมด: UI-A/UI-B ยังไม่ทำสิ่งที่สัญญาจริง (ต้องแตะ `runtime.py`/บูต/ล็อกอิน =
นอกเขตเขียนของ LANE-UI, ต้องขอ chief เป็น CORE-REQUEST ก่อน — ยังไม่มีใบ CORE-REQUEST ใหม่รอบนี้), ร้านค้า NPC
ยังรอ DB interface (`0621`)

## ลำดับตาม §7
1. `git fetch origin main` ทั้งสองรีโป (bridge/server ทั้งคู่หยุดที่ `d01ae97` #750 ตอนเริ่ม — เซสชันนี้เพิ่งเริ่ม
   ที่จุดนี้พอดี ไม่มีอะไรขยับระหว่างรอบ) · กิ่งที่ระบบให้ (`claude/wizardly-knuth-urhd6h` bridge ·
   `claude/keen-gates-urhd6h` server) อยู่บน `origin/main` สดอยู่แล้ว (`HEAD == merge-base(HEAD, origin/main) ==
   origin/main`) ไม่ต้อง `checkout -B` ใหม่ · list PR เปิดหัว `[LANE-UI]` ทั้งสองรีโป — **ไม่มี** ⇒ ไม่ต้องถอย
2. รอบก่อน (`qwhlua`) ไม่มี `ADVERSARY_PENDING` ค้าง (ไฟล์รอบเขียนไว้ชัดว่า "คืนผลแล้ว ไม่ pending")
3. กล่องจดหมาย `grep -l "ADDRESSEE: LANE-UI" notes_to_chief/*.md` ข้ามใบ `.CONSUMED.txt` — พบสามใบ:
   - `0332` (LANE-PROMPT ต้นทางของ COO — ยืนยันซ้ำเป็นครั้งที่สามแล้วว่าไม่ใช่จดหมายจริงถึง LANE-UI ตามที่รอบ
     `md7pjz`/`qwhlua` วินิจฉัยไว้แล้ว ไม่สร้าง `.CONSUMED.txt`)
   - `1709` (chief ยืนยัน property-swap ที่ `runtime.py:7396` ลงจริงแล้ว วัดซ้ำเอง G1 — ข้อมูลเท่านั้น ไม่มี
     คำสั่งให้ทำอะไรต่อ · ย้ำ nonclaim: ยังไม่อ้างว่า UI-B ล็อกเอาต์ได้จริง) — รับทราบ สร้าง `.CONSUMED.txt`
   - `1745` (COO: `#747` รอเกต + finding ของ adversary รับเป็นกฎบ้าน + สั่งงานสำรองข้อ 1 = แก้ที่ตัว decoder
     กำหนดรอบ 19:46) — **นี่คืองานของรอบนี้** สร้าง `.CONSUMED.txt`
4. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานจริง (ครั้งที่ 1 ของเพดาน `1428` ≤2 ครั้งต่อรอบ) — ผลคืนก่อน push จริง
   (ดูหัวข้อ "ADVERSARY" ด้านล่าง)

## ทำอะไร
### ข้อ 1 ของใบ `1745` — เกตของ `#747`
`mcp__github__pull_request_read get owner=panyaasanee repo=pirate-force-server pullNumber=747` ตอบ
`state=closed merged=true merged_at=2026-09-04T10:44:26Z` (17:44:26+07) — ยืนยันซ้ำด้วย `git log --oneline
origin/main` เห็น `c9c65f2 Merge pull request #747 ...` ตรงกัน ⇒ **เกตผ่านแล้วจริง** ไม่ต้องเขียน
`GATE_UNVERIFIED #747` (ไฟล์รอบ `qwhlua` บันทึกสถานะจริง ณ ตอนเขียนไว้ถูกต้องแล้ว ไม่ต้องแก้ย้อนหลัง)

### ข้อ 2 ของใบ `1745` — decoder เองเช็ค `consumed==len` (ไม่ใช่แค่ชั้น log อีกต่อไป)
รอบ `qwhlua` แก้ที่ชั้น log เท่านั้น (`lane_hooks/lane_ui_*_wire_log.py` คำนวณ `consumed=<c>/<n>` เอง) —
รอบนี้ (`1745` ข้อ 2) สั่งแก้ที่ตัว `decode_*` เอง:

1. เพิ่ม `require_exhausted(buf, offset)` ใน `src/pirateforce_foundation/ui_social_wire.py` — raise
   `WireDecodeError` เมื่อ `offset != len(buf)` (สมมาตร: เช็คทั้ง `offset < len(buf)` หางเกิน และในทางทฤษฎี
   `offset > len(buf)` แม้ reader ทั้งสี่ตัว (`read_u8tag`/`read_u32tag`/`read_u64tag`/`read_untagged_wstring`)
   จะ bounds-check จนกรณีนี้เป็นไปไม่ได้อยู่แล้ว)
2. เรียก `wire.require_exhausted(payload, offset)` เป็นขั้นตอนสุดท้ายในทุก `decode_*` ของทั้งสี่ไฟล์พี่น้อง
   ก่อนคืนค่า dataclass (อยู่ใน `try` block เดิม จับด้วย `except wire.WireDecodeError: return None` เดิม
   ไม่ต้องเปิด except ใหม่): `ui_party_wire.py` (`decode_party_invite_payload`, `decode_party_cmd_payload`),
   `ui_friend_wire.py` (`decode_request_be_friend_payload`, `decode_remove_friend_payload`),
   `ui_mail_wire.py` (`decode_send_mail_payload`, `decode_get_mail_content_payload`,
   `decode_delete_mail_payload`), `ui_trade_wire.py` (`decode_trade_invite_payload`) — 8 ฟังก์ชันครบ
3. ผลลัพธ์: เพย์โหลดที่ตรงรูปฟิลด์แต่มีหางไบต์เกินตอนนี้ decode ล้มเหลว (`None`) → ชั้น hook พิมพ์ `UNPARSED`
   (fail-closed) แทนที่จะ "decoded" แบบ partial อย่างเงียบ ๆ · `lane_hooks/lane_ui_*_wire_log.py` **ไม่ต้องแก้เลย**
   — decode คืน non-None รับประกัน `consumed==len(payload)` เสมอแล้ว บรรทัด `consumed=<c>/<n>` ของรอบก่อนยัง
   ถูกต้อง (`c` จะเท่า `n` ทุกครั้งที่ decode สำเร็จ)
4. เทสมิวแทนต์ตามที่ใบ `1745` สั่ง ("หางเกิน 1 ไบต์ต้องไม่ผ่านเป็น match เต็ม"):
   - `tests/test_ui_social_wire.py`: `RequireExhaustedTests` ใหม่ 4 เทส (exact-length ผ่าน, empty-buffer ผ่าน,
     หาง 1 ไบต์ fail, หางหลายไบต์ fail)
   - `tests/test_ui_{party,friend,mail,trade}_wire.py`: เพิ่ม `test_trailing_bytes_after_a_full_match_fail_closed`
     หนึ่งเทสต่อคลาส (8 เทสรวม ทดสอบทั้งหาง 1 และ 37 ไบต์) — ทดสอบตรงที่ `decode_*` ไม่ใช่ผ่านชั้น hook
   - `tests/test_ui_lane_hooks_wire_log.py`: แก้เทสเดิมของรอบ `qwhlua`
     (`test_trailing_bytes_after_a_full_match_are_never_silently_dropped`) ให้ตรงพฤติกรรมใหม่ — เดิมคาดว่าเห็น
     บรรทัด "decoded" กับ `consumed=<c>/<n>` ที่ `c<n`, ตอนนี้คาดว่าเห็น `UNPARSED` แทน (สอดคล้องกับที่ decoder
     ล้มเหลวจริงแล้ว)

## ADVERSARY — คืนผลแล้วก่อน push จริง ไม่ pending
`pf-adversary` ครั้งที่ 1 (เพดาน `1428` ≤2 ครั้ง) — ตรวจแบบแยก worktree (`git worktree add --detach` + มิวแทนต์
ทดสอบ: ลบ `require_exhausted` ออกจาก `ui_party_wire.py` ใน worktree แล้วรันซ้ำ ยืนยันเทส 6 ตัวแดงตรงจุดที่ควร
แดง แล้ว restore คืน byte-identical) — **ไม่พบข้อบกพร่อง**: ทั้ง 8 `decode_*` เรียก `require_exhausted` ด้วย
offset ตัวสุดท้ายถูกต้องครบทุกฟังก์ชัน ไม่มี path ไหนข้าม, ขอบเขต `offset > len(buf)` พิสูจน์แล้วว่าเป็นไปไม่ได้
จาก bounds-check ของ reader ทั้งสี่ตัว, grep ทั้งรีโปไม่พบ caller อื่นที่พึ่งพฤติกรรม partial-match เดิม (`runtime.py`
import แค่ค่าคงที่ opcode ไม่เคยเรียก `decode_*` ตรง — ผ่าน `lane_hooks` เท่านั้น), ไม่พบ `decode_*` พี่น้องตัวอื่นที่
ใช้ reader ชุดเดียวกันแล้วยังไม่แก้ · รันชุดเต็มใน worktree แยก: **9924 passed, 412 skipped, 19159 subtests
passed, 0 failed** (จำนวน skip ต่างจากรันปกติ 327 เพราะ worktree ของ agent ไม่มี `pf_bridge` sibling ข้าง ๆ —
สภาพเดียวกับ `pytest_subset`/`skip_census` ที่ต้องซ้อมอยู่แล้วเวลามีไฟล์เทส/skip ใหม่ ซึ่งรอบนี้ไม่มีทั้งสองอย่าง
จึงไม่บังคับ แต่ผล 0 failed ยืนยันไม่มีอะไรพัง)

**คำถามเปิดจาก adversary (ยังไม่ปิด — ไม่บล็อกรอบนี้)**: `require_exhausted` ทำให้ "field model ผิด (นับฟิลด์/ลำดับ
พลาด)" กับ "หางไบต์ปลอม" แยกไม่ออกอีกต่อไป (ทั้งคู่กลายเป็น `UNPARSED` เหมือนกัน) — เป็น fail-closed ที่ปลอดภัยกว่า
แต่ก็ทำให้สัญญาณ "decode ได้บางส่วน จำนวนไบต์ที่เหลือ" ที่เคยช่วยชี้ RE รอบต่อไปหายไปสำหรับ 8 คลาสที่ยัง
`CALL_UNCLASSIFIED` — ส่งต่อให้ COO/chief พิจารณาว่าต้องการเก็บสัญญาณนั้นไว้ที่ไหน (เช่น log ความยาวหางก่อนทิ้ง)
หรือรับ trade-off นี้เป็นการถาวร

## ส่งอะไร (SHA/PR)
- `pirate-force-server` PR หัว `[LANE-UI] round urhd6h: decoders fail closed on trailing bytes
  (COO-DECISION 20260904_1745 item 2)` กิ่ง `claude/keen-gates-urhd6h` — แก้ 5 ไฟล์ src
  (`ui_social_wire.py` + สี่ไฟล์พี่น้อง), แก้ 6 ไฟล์เทส (`test_ui_social_wire.py` +
  `test_ui_{party,friend,mail,trade}_wire.py` + `test_ui_lane_hooks_wire_log.py`)
- `pf_bridge` PR หัว `[LANE-UI] round urhd6h: claim` กิ่ง `claude/wizardly-knuth-urhd6h` — ไฟล์รอบนี้ + จดหมายตอบ
  COO (`20260904_1827`) + `.CONSUMED.txt` ของใบ `1709`/`1745`

## nonclaims
① ไม่ใช่ปุ่ม/ฟีเจอร์ใหม่บนจอ — งานนี้เป็นความถูกต้องของ decoder เท่านั้น ไม่มีใบ GT ปิดรอบนี้ (เหมือนที่รอบ
`qwhlua` บันทึกไว้สำหรับงานโครงสร้างพื้นฐานก่อนหน้า)
② ไม่แตะ `lane_hooks/lane_ui_*_wire_log.py`, `runtime.py`, `app.py`, `store.py`, `gm/` เลย (เขตเขียนเดิม)
③ nonclaim② ของใบ `1120` ยังยืนเต็ม — รู้รูปเฟรม (และตอนนี้รู้ว่าหางไบต์เกินต้องถูกปฏิเสธ) **ไม่ได้แปลว่ารู้
caller/verb semantics** ปุ่มจริงทั้งแปดคลาสยังไม่มี
④ UI-A/UI-B (`GT-184`/`GT-186`, คิวข้อ 2-3 ของพรอมป์สาย) ยังไม่ขยับ — ต้องแตะจุดในบูต/ล็อกอิน/`runtime.py` ซึ่ง
นอกเขตเขียนของ LANE-UI โดยตรง ต้องขอ chief เป็น CORE-REQUEST ก่อนถึงจะเริ่มเขียนโค้ดจริงได้ (ยังไม่ได้ยื่นรอบนี้ —
ตามลำดับงานสำรอง `1450` ข้อ 6 ที่ให้ทำงานสำรองก่อน งานหลักที่ต้องรอจุดเสียบถือเป็นของค้างที่ต้อง CORE-REQUEST
ไม่ใช่งานสำรอง จะยื่นรอบถัดไปถ้าไม่มีงานสำรองอื่นค้าง)
⑤ ไม่ยืนยันว่าไม่มีบั๊กอื่นในสี่โมดูลนี้ — pf-adversary รอบนี้ (grep ทั้งรีโป + มิวแทนต์ควบคุม) ไม่พบอย่างอื่น
แต่ "ตรวจแล้วไม่พบ" ไม่เท่ากับ "ไม่มี"

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
1. ตรวจสถานะเกตของ PR เซิร์ฟเวอร์รอบนี้ก่อนงานอื่นทั้งหมด (`PANYA-DECISION 20260904_1158` §22)
2. เขียน CORE-REQUEST ถึง chief สำหรับจุดเสียบ UI-A/UI-B ใน `runtime.py` (คิวข้อ 2-3 ของพรอมป์สาย ค้างมานาน
   ต้องขยับ) ถ้าไม่มีงานสำรองอื่นค้างก่อน
3. ตอบคำถามเปิดของ adversary ถ้า COO/chief สั่งมา (เก็บสัญญาณ "decode บางส่วน" ไว้ที่ไหนสำหรับคลาสที่ยัง
   `CALL_UNCLASSIFIED`)

— LANE-UI รอบ `urhd6h`
