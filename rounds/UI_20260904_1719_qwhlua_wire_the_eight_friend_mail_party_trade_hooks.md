# LANE-UI round `qwhlua` — wire the eight friend/mail/party/trade log-only hooks (CORE-REQUEST 1120, second half)

เวลา: 2026-09-04 17:19 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับขั้น M — งานนี้เป็นโครงสร้างพื้นฐาน (report-only wiring) ไม่ใช่ปุ่มบนจอที่ผู้เล่นเห็นสิ่งที่สัญญา และไม่ใช่
เกณฑ์ของ M2/M3/M4 ใน `NOW.md` เลย บันไดที่เกี่ยวกับ LANE-UI (UI-A/UI-B, ร้านค้า NPC, สารบัญ) ค้างที่เดิม: UI-A/UI-B
รอ Panya กดจริง (`GT-184`/`GT-186` READY-FOR-ATTENDED อยู่แล้ว), ร้านค้า NPC ยังรอ DB interface (`0621`)

## ลำดับตาม §7
1. `git fetch origin main` ทั้งสองรีโป (bridge `0f9d583→6c85a96`, server `c1660fd→0298313` ตอนเริ่ม แล้วขยับอีกครั้งเป็น
   `33981ba` ระหว่างรอบ — merge เข้าก่อนรันชุดเต็มครั้งสุดท้าย) · `git checkout -B` จาก `origin/main` สดทั้งคู่ · list PR
   เปิดหัว `[LANE-UI]` ทั้งสองรีโป — **ไม่มี** ⇒ ไม่ต้องถอย
2. ตรวจ `PANYA-DECISION 20260904_1158` §22 ก่อนงานอื่น: รอบก่อน (`sg7p4d`) ปิดด้วย `GATE_UNVERIFIED
   pirate-force-server#742` — ตรวจซ้ำรอบนี้: `pull_request_read get` ตอบ `state=closed merged=true
   merged_at=2026-09-04T09:02:18Z` ⇒ เกตผ่านแล้วจริง ไม่ต้องแก้อะไร
3. กล่องจดหมาย `grep -l "ADDRESSEE: LANE-UI" notes_to_chief/*.md` ข้ามใบ `.CONSUMED.txt` — พบสองใบ:
   - `0332` (LANE-PROMPT — พรอมป์ต้นทางของ COO ที่ Panya คัดลอกไปตั้ง routine เอง หัวใบพิมพ์ `ADDRESSEE: COO` ตรง ๆ
     บรรทัดแรก, string ที่ grep เจอ (`grep -l "ADDRESSEE: LANE-UI"`) คือประโยคตัวอย่างคำสั่งในเนื้อพรอมป์เอง ไม่ใช่
     จดหมายถึง LANE-UI จริง — ยืนยันซ้ำตามที่รอบ `md7pjz` วินิจฉัยไว้แล้ว (nonclaim④ ของใบนั้น) ไม่ต้องปรึกษาใครอีก
     ไม่สร้าง `.CONSUMED.txt` ให้ใบนี้ (ไม่ใช่จดหมายจริง)
   - `1522` (chief ตอบ CORE-REQUEST `1120`: dispatch branch ทั้ง 8 จุด push แล้ว รอ merge บอกชัดว่า "ต่อ
     `lane_hooks/lane_ui_*.py` ของแต่ละคลาสได้จากรอบถัดไปของคุณเอง ไม่ต้องขอ chief อีก") — **นี่คืองานของรอบนี้**
     ตอบด้วยการเขียนโค้ดจริงตามหัวข้อ "ทำอะไร" ด้านล่าง สร้าง `.CONSUMED.txt` ให้ใบนี้พร้อมรอบนี้
4. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานจริง (ครั้งที่ 1 ของเพดาน `1428` ≤2 ครั้งต่อรอบ) — ผลคืนก่อน push จริง
   (ดูหัวข้อ "ADVERSARY" ด้านล่าง)

## ทำอะไร
งานหลัก: `pirate-force-server#733` (merge แล้วตั้งแต่ 2026-09-04T06:38:53Z) เปิด dispatch table
`_FRIEND_MAIL_PARTY_TRADE_DISPATCH` ใน `runtime.py` ครอบทั้ง 8 คลาส (`PartyInviteVital`/`PartyCmdVital`/
`Community_RequestBeFriendVital`/`Community_RemoveFriendVital`/`Community_SendMailVital`/
`Community_GetMailContentVital`/`Community_DeleteMailVital`/`TradeInviteVital`) แต่ยังไม่มี `lane_hooks` module
ใดสมัครจุดไหนเลย (`test_no_point_has_a_subscriber_yet` ยืนยันเรื่องนี้ไว้ตรง ๆ ในเนื้อเทส) — chief round
`cool-johnson-7qcsux` (`1522`) ยืนยันจุดเสียบทั้งแปดตรงกับใบ `1120` ทุกตัว (ตรวจซ้ำอิสระด้วยสูตรแฮชแล้ว) และมอบสิทธิ์
เขียน `lane_hooks/lane_ui_*.py` ให้ LANE-UI เองในรอบถัดไป ไม่ต้อง CORE-REQUEST อีก

1. เขียน 4 โมดูลใหม่ `src/pirateforce_foundation/lane_hooks/lane_ui_{party,friend,mail,trade}_wire_log.py`
   (ครอบ 8 จุด รวม) — รูปแบบเดียวกับ `lane_a_enter_instance_log.py` เป๊ะ (sibling ที่ merge ไปแล้ว): report-only,
   ไม่ส่งเฟรมกลับ ไม่แตะ store ไม่แตะ session state, decode ด้วย `ui_party_wire.py`/`ui_friend_wire.py`/
   `ui_mail_wire.py`/`ui_trade_wire.py` ที่พิสูจน์แล้วบน main (round ก่อน `md7pjz`), พิมพ์ค่า field ตำแหน่ง (ไม่มีชื่อ
   เดาความหมาย ตาม nonclaim② ของใบ `1120` ที่ยังยืน — ไม่รู้ caller/verb semantics) หรือ `UNPARSED` + hex (cap 96
   ไบต์) เมื่อ decode ล้ม
2. เขียนเทสของตัวเอง `tests/test_ui_lane_hooks_wire_log.py` (9 เทส/134 subtest) — round-trip ผ่าน `encode_*` ของแต่
   ละคลาสเอง (ไม่พิมพ์ bytes มือ), UNPARSED ทุกความยาวผิด, non-bytes payload, bytearray/memoryview, ascii safety,
   hex cap, guard คำเดาความหมาย
3. แก้ไฟล์เทสของ chief `tests/test_lane_ui_friend_mail_party_trade_dispatch_wiring.py` สองจุด (ไฟล์นี้เขียนไว้ให้
   รอบนี้ต้องแตะ — เนื้อเทสเองบอกตรง ๆ ว่า "this test exists so that round's PR has to touch (and read) this
   file"): `test_no_point_has_a_subscriber_yet` → `test_every_point_now_has_exactly_one_subscriber` (นับ 1 แทน 0)
   และ `test_each_class_dispatches_counts_and_answers_nothing` ตัดข้ออ้าง "ไม่มีวัน UNPARSED" ที่จริงแล้วเป็นจริงแค่
   เพราะไม่มีใครสมัครจุดเลย (payload `b"\x00\x01"` ที่ใบนี้ใช้ไม่ตรงรูป field ของคลาสไหนเลยจริง ๆ — ตรวจซ้ำเองด้วย)
4. `pf-adversary` (ครั้งที่ 1) คืนผลก่อน push จริง — **พบข้อจริงหนึ่งข้อ**: ไม่มี `decode_*` ตัวไหนใน
   `ui_*_wire.py` (4 ไฟล์เดิม ไม่ได้แก้รอบนี้) เช็คว่า parse สำเร็จ "กินหมดทั้ง payload" — payload ที่ตรงรูปฟิลด์
   ตายตัวแต่มีหางไบต์เกินต่อท้ายจะ decode สำเร็จเงียบ ๆ แล้วพิมพ์ "decoded ... bytes_out=0" เหมือนเฟรมที่ match เต็ม
   ทุกไบต์ — ถ้าวันหนึ่ง capture จริงพิสูจน์ว่าคลาสไหนมีฟิลด์มากกว่าที่โมเดลไว้ตอนนี้ บรรทัด console จะโกหกว่า "ครบ"
   ทั้งที่ prefix-match แค่บางส่วน แก้โดย **ไม่แตะ `ui_*_wire.py` เดิมเลย** (คำนวณ `consumed = len(encode_*(fields))`
   ในโมดูล hook เอง แล้วพิมพ์ `consumed=<c>/<n>` ทุกบรรทัดที่ decode สำเร็จ — `encode_*`/`decode_*` เป็น inverse ที่
   พิสูจน์แล้วว่า round-trip ตรงไบต์ ใช้ตรวจได้โดยไม่ต้องแก้ไฟล์เดิม) เพิ่มเทส
   `test_trailing_bytes_after_a_full_match_are_never_silently_dropped` ยืนยันการแก้
5. `git fetch origin main` อีกครั้ง (server ขยับ `0298313→33981ba` ระหว่างรอบ — PR #744 LANE-DB merge) →
   `git merge origin/main --no-edit` (fast-forward สะอาด ไม่ชนกัน) → รันชุดเต็มครั้งเดียวบนต้นไม้ที่ merge แล้ว:
   **9900 passed, 0 failed, 327 skipped** (จำนวน skip เท่าเดิมกับก่อนรอบนี้ ไม่มี skip ใหม่) · เพิ่มไฟล์เทสใหม่ ⇒
   ซ้อม `pytest_subset` + `skip_census` ในสภาพไม่มี `pf_bridge` ข้าง ๆ (`git worktree add --detach`, คัดลอกไฟล์ที่ยัง
   ไม่ commit เข้าไปเอง): ทั้งสองช่อง **exit 0** (`8955 passed / 93 skipped` ในสภาพนั้น, census ตอบ "every skip is
   declared, named and pinned · RESULT: PASS") · `python3 tools_bridge/pf_gate_preflight.py --repo
   ../pirate-force-server` → **PASS** (cp874 + no new skips + main อยู่ใน branch นี้)

## ส่งอะไร (SHA/PR)
- `pirate-force-server` PR (สาขา `claude/inspiring-meitner-qwhlua`, หัว `[LANE-UI] round qwhlua: wire the eight
  friend/mail/party/trade CORE-REQUEST-1120 hooks as report-only log-only subscribers`) — 4 ไฟล์ใหม่
  `lane_hooks/lane_ui_{party,friend,mail,trade}_wire_log.py`, ไฟล์เทสใหม่ `tests/test_ui_lane_hooks_wire_log.py`,
  แก้ `tests/test_lane_ui_friend_mail_party_trade_dispatch_wiring.py` สองจุดตามข้อ 3 ข้างบน
- `pf_bridge` PR `#1172` (`[LANE-UI] round qwhlua: claim` → เติมไฟล์รอบนี้ + จดหมายตอบ chief + `.CONSUMED.txt` ของ
  `1120`)

## nonclaims
① nonclaim② ของใบ `1120` ยังยืนเต็ม — รู้รูปเฟรมทั้งแปดคลาสแล้ว **ไม่ได้แปลว่ารู้ caller/verb semantics** ปุ่ม
"เชิญปาร์ตี้"/"เพิ่มเพื่อน"/"ส่งเมล"/"ชวนเทรด" จริงบนจอ **ยังไม่มี** — รอบนี้เป็นแค่โครงสร้างพื้นฐาน (subscriber ที่นับ
เฟรมและ log เท่านั้น) ไม่ใช่ฟีเจอร์ที่ผู้เล่นเห็นสิ่งที่ปุ่มสัญญา ตามนิยาม "ปุ่มทำงาน" ของพรอมป์สายเอง ⇒ ไม่มีใบ GT
ปิดรอบนี้ (เหมือนที่ `NavigationEx_EnterInstanceVital` ทำมาก่อน — ปิดด้วย RE-227/GT-228 แยกต่างหากทีหลัง)
② ยืนยันว่า `consumed=<c>/<n>` ปิดช่องที่ `pf-adversary` เจอได้จริงสำหรับ **บรรทัด console ของรอบนี้เท่านั้น** —
ไม่ได้แก้ `ui_*_wire.py` เดิม (นอกเขต ไม่ใช่ของรอบนี้) คลาสไหนถูกพิสูจน์ว่ามีฟิลด์เกินโมเดลจริงยังต้องเปิด RE ใบใหม่
③ ไม่แตะ `runtime.py`/`app.py`/`store.py`/`gm/` เลย (เขตเขียนเดิม)
④ ใบ `0332` ยืนยันซ้ำเป็นครั้งที่สองแล้วว่าไม่ใช่จดหมายจริง (ตามที่รอบ `md7pjz` วินิจฉัยไว้) — ไม่สร้าง
`.CONSUMED.txt` ให้ ถ้ายัง grep เจอในรอบหน้าอีกให้ถือว่าเป็นสถานะถาวรของไฟล์นี้ ไม่ใช่เรื่องต้องวินิจฉัยซ้ำทุกรอบ

## ADVERSARY — คืนผลแล้ว ไม่ pending
`pf-adversary` ครั้งที่ 1 ของรอบนี้ (เพดาน `1428` ≤2 ครั้ง) คืนผลก่อน push จริง — พบหนึ่งข้อ (ดูข้อ 4 ข้างบน) แก้แล้ว
ในรอบเดียวกัน ยืนยันด้วยเทสใหม่ + รันชุดเต็มซ้ำ (9900 passed) เขียนคำว่า "ผ่าน adversary" ได้เพราะผลคืนแล้วจริง —
ยังไม่ได้ใช้ครั้งที่ 2 เผื่อรอบถัดไปต้องการ

## งานสำรอง (พร้อมเริ่มได้ทันทีรอบถัดไปถ้างานหลักติด — ตาม `PANYA 1450` ข้อ 6)
1. เช็คว่ามีจดหมายตอบ `20260904_1600` (ช่องโหว่การ์ด word-boundary snake_case ที่พบรอบ `md7pjz`) จาก chief/COO
   หรือยัง — ถ้ามีคำตัดสินว่าใครถือ เดินตามนั้น
2. เช็คว่า CORE-REQUEST `0621` (`TradeCmdVital` wire + DB money/backpack interface สำหรับร้านค้า NPC) มีความ
   คืบหน้าจาก LANE-DB เพิ่มจากใบ `0715` หรือยัง — ถ้ามี DB interface พร้อมแล้ว กลับมาเขียน `TradeCmdVital` wire
   ต่อทันที
3. อ่านสารบัญ 15 แถวเดิม (`0400`) อีกครั้ง หารายการที่ RE ใบใหม่ปิดแล้วระหว่างที่ผ่านมาแต่ยังไม่ถูกต่อสาย — ถ้าไม่มี
   กลับไปคิวปกติ (ข้อ 4 เดินไปหา NPC/มอนอัตโนมัติ — ยังรอ RE ตามที่พรอมป์สายบอก)

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
1. ตรวจสถานะเกตของ PR เซิร์ฟเวอร์รอบนี้ก่อนงานอื่นทั้งหมด (ตาม `PANYA-DECISION 20260904_1158` §22) — ถ้ายังไม่ตัดสิน
   ใน 10 นาทีหลัง push ให้บันทึก `GATE_UNVERIFIED` เหมือนรอบ `sg7p4d` ทำไว้
2. หยิบงานสำรองข้อ 1-3 ข้างบนถ้างานหลักติด มิฉะนั้นกลับคิวปกติ

## GATE_UNVERIFIED #747
`pirate-force-server#747` — push เวลา 10:19:44Z (17:19:44+07:00), gate job ของ run `pull_request` เริ่ม
10:21:01Z/10:21:40Z (17:21+07) ตรวจซ้ำหลายครั้งด้วย `pull_request_read get_check_runs` + curl ตรงต่อ GitHub API
commit `415b095f413fe8051de66f357fdcbd4ff2430208` — **ทั้งสอง job `gate` ยังเป็น `in_progress` ที่ 17:31:15+07** ผ่าน
มาครบ 10 นาทีจากตอน push แล้ว ตาม `PANYA-DECISION 20260904_1158` §22 ⇒ บันทึก `GATE_UNVERIFIED` แทนเขียนว่า "รอ
เกต — routine" **รอบถัดไปของ LANE-UI เปิดด้วยการตรวจ PR นี้ก่อนงานอื่นทั้งหมด** (อ่าน `get_check_runs`/`get_status`
ของ PR `#747` ก่อน) — แดง = แก้ในรอบนั้นทันที (ไม่ต้อง claim ใหม่ เป็น correction ใต้รหัสเดิม `qwhlua`) · เขียว =
merge เอง (ห้าม merge มือ ปล่อยให้ automerge ทำ ถ้ายังไม่ merge เพราะเหตุอื่นให้รายงาน)

## nonclaim เพิ่ม (เรื่องเกต)
① ไม่ยืนยันว่าเกตของ `#747` จะแดงหรือเขียว — แค่ยังไม่รู้ผลตอนเขียนใบนี้ ② การรันเต็มรูปแบบบน cloud (9900 passed, 0
failed) ก่อน push ทำให้คาดว่าเกตจะเขียว แต่ "preflight PASS ไม่ได้แปลว่าเกตจะเขียว" (`AGENTS.md` §7)

— LANE-UI รอบ `qwhlua`
