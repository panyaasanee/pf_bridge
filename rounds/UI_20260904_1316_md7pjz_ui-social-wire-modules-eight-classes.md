# LANE-UI round `md7pjz` — eight `ui_*.py` pure encode/decode modules (CORE-REQUEST 1120)

เวลา: 2026-09-04 13:16 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ M — งานนี้เป็นโค้ดในเขตเขียนของ LANE-UI เอง (`src/pirateforce_foundation/ui_*.py`) ตาม COO-DECISION
`1244` ข้อ 3 แต่ยังไม่ใช่ปุ่ม/ฟังก์ชันที่ผู้เล่นกดได้บนจอ (ยังไม่มีจุดเสียบ dispatch จาก chief) — เป็นก้าวที่จำเป็น
ก่อนจุดนั้น ไม่ใช่ M/NOW milestone เอง

## ทำอะไร
1. `git fetch origin main` ทั้งสองรีโป · ไม่มีใบ `[LANE-UI]` เปิดค้าง · claim `pf_bridge#1136` กิ่ง
   `claude/lane-ui-round-md7pjz`
2. เช็ค `.CONSUMED.txt` ของ chief สำหรับใบ `1120` ครั้งเดียวตามที่ COO-DECISION `1244` ข้อ 4 สั่ง (เลิกวนเช็คทั้ง
   รอบ) — ยังไม่มีคำตอบ (คาดตามคิว `1245`: จุดเสียบ ≤15:51) ไม่บล็อกงานโมดูลบริสุทธิ์
3. ดึงฟิลด์แปดคลาสเต็มจาก `external/PF_SERIALIZER_FIELDS.tsv` ตรง ๆ (grep ทีละคลาส ไม่เชื่อเลขเก่าจากจดหมาย `1120`)
   ยืนยันจำนวนฟิลด์ตรงกับที่ `1120` สรุปไว้ทุกคลาส (6/4/6/6/18/8/6/6 แถว W+R) · ยืนยัน tag legend จากหลักฐานที่มี
   อยู่แล้วในโปรเจกต์ (`0x08`/`0x0B`=u8, `0x32`=u64 — `FINDINGS_R38_0x1B40_DECODED_LOGOUTVITAL.md`,
   `CLIENT_RE_QUEUE.md:3425`, `current/pf_login_game_server_v141.py:u8tag`/`u32tag` calls) · ยืนยันว่า TSV
   `field_offset` (`+0x14` ฯลฯ) เป็น offset ของ object ในไคลเอนต์ ไม่ใช่ wire byte offset — ฟิลด์บนไวร์เรียงตาม
   `order` ต่อกันไม่มีช่องว่าง (พิสูจน์จากเฟรม `CTracePathReqVital` จริงที่ capture ไว้แล้ว + วิธี
   `make_runtime_vitals` เขียน field ต่อกันเอง)
4. เขียน `pirate-force-server`: `src/pirateforce_foundation/ui_social_wire.py` (primitive กลาง: `u64tag`
   ใหม่ที่ legacy ไม่มี + untagged-wstring encode/decode — ไม่แตะ `current/pf_login_game_server_v141.py` เด็ดขาด
   ตาม `V141_FREEZE.md`) · `ui_party_wire.py` (`PartyInviteVital` `0x37B1`/`PartyCmdVital` `0x2466`) ·
   `ui_friend_wire.py` (`Community_RequestBeFriendVital` `0xB9E9`/`Community_RemoveFriendVital` `0x98A1`) ·
   `ui_mail_wire.py` (`Community_SendMailVital` `0x6E12`/`Community_GetMailContentVital` `0xAF60`/
   `Community_DeleteMailVital` `0x8183`) · `ui_trade_wire.py` (`TradeInviteVital` `0x3700` เท่านั้น — ไม่ใช่
   `TradeCmdVital` ซึ่งยังไม่ resolve และแยกใบ `0621`) — **ทุกฟิลด์ตั้งชื่อแบบ positional
   (`field1_u8`/`field2_u64`/...) ไม่เดาความหมาย** ตามที่ `1120` nonclaim (2) เขียนไว้ว่า caller/verb ยัง
   `CALL_UNCLASSIFIED` ทุกคลาส · ไม่มีไฟล์ไหนแตะ `runtime.py`/`vital_walk.py` เลย · ไม่มี `production_allowed`
   flag เพราะไม่มีการ compose ack/error frame ใด ๆ (แค่ encode/decode รูปเฟรมที่พิสูจน์แล้วเท่านั้น — ไม่เดา
   ack/error shape ที่ไม่มีหลักฐาน)
5. เขียนเทส 5 ไฟล์คู่กัน (`tests/test_ui_social_wire.py` ฯลฯ) — round-trip encode→decode ทุกคลาส + fail-closed
   บน tag ผิด/buffer สั้นเกิน + เช็ค field order ตรงตาม registry — รันผ่านหมด (39 เทส) หลังแก้บั๊กเลขคูณของตัวเอง
   สองจุด (ชื่อเทส `test_payload_is_exactly_ten_bytes` คำนวณผิด — จริง 11 ไบต์ · เทส `RemoveFriend` ตั้งชื่อว่า
   "nineteen_bytes" ทั้งที่ค่าจริงคำนวณจาก `9+9+2`=20 — แก้ชื่อให้ตรง ไม่แก้ตัวเลขที่ผิด (ไม่มีตัวเลข hardcode ผิด
   ในโค้ดจริง มีแค่ชื่อเทสเข้าใจผิด))
6. ซ้อมเกตในสภาพไม่มี `pf_bridge` ข้าง ๆ ตาม §7 (ไฟล์เทสใหม่): `git worktree add --detach` นอกโฟลเดอร์ที่มี
   `pf_bridge` → `pytest_subset` (`--ignore` 48 ไฟล์ตาม `GameClient`/`capture_v141` grep) → **เจอ 9 failed รอบ
   แรก**: (ก) 4 ไฟล์ใหม่มีอักขระ `①②③④` (`0x2461` ฯลฯ) ในคอมเมนต์ — ผิดกฎ cp874 ของโค้ด (ไม่ใช่ปัญหาของจดหมาย
   ที่ใช้ได้ปกติ) แก้เป็น `(2)` ทั้งหมด (ข) `tests/test_npc_interaction_wire.py::test_no_foundation_module_
   implements_quest_or_shop_behavior` จับคำว่า "trade" ในสามไฟล์ (`ui_social_wire.py`/`ui_party_wire.py`/
   `ui_trade_wire.py` — ชื่อคลาส `TradeInviteVital` เป็นคำจริงจากทะเบียน ไม่ใช่คำเดา) — เพิ่มรายการ `ALLOWED_HITS`
   สามบรรทัดตามรูปแบบที่ไฟล์นั้นมีอยู่แล้ว (เทียบเคียงกับ `world_bg3001_identity.py`/`trade_session_membership.py`
   ที่ได้รับยกเว้นแบบเดียวกันมาก่อน) — ไฟล์นี้ไม่ใช่เขตเขียนของ LANE-UI โดยตรง (`tests/test_ui_*` เท่านั้น) แต่
   `AGENTS.md` มีบรรทัดรับรองว่าสายอื่นเติมรายการยกเว้นไฟล์นี้ได้ในรอบเดียวกันเมื่อพิสูจน์ได้ว่าไม่ใช่พฤติกรรมจริง
   (เทียบเคียงหลักการเดียวกับ `EXPECTED_TABLES` ที่ระบุไว้ตรง ๆ) — รันซ้ำ **สะอาด 8750 passed, 0 failed, 89
   skipped** · `skip_census` **PASS** (89 skip ทุกตัว pin ใต้ `preconditions` ครบ ไม่มีตัวใหม่ที่ไม่ประกาศ)
7. `git merge origin/main` เข้ากิ่งเซิร์ฟเวอร์ (ดึง PR ของ LANE-GM ที่ merge ระหว่างรอบ) แล้วรัน
   `python3 tools_bridge/pf_gate_preflight.py --repo <server>` **PASS** ทั้งสองรอบ (ก่อน/หลัง merge) — รันชุดเต็ม
   อีกครั้งบนต้นไม้ที่ merge แล้ว (`python3 -m pytest tests -q`) **PASS: 9694 passed, 0 failed, 327 skipped**
8. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานเขียนโค้ด — รีวิวความถูกต้องของ tag legend/field order เทียบ TSV ทุก
   ฟิลด์ + ตรวจว่าไม่มีการเดา semantic ที่ไหนหลุดเข้าไป + ตรวจ exemption ของ `test_npc_interaction_wire.py` ว่า
   ชอบธรรมจริง — ผลยังไม่คืนตอน push

## ส่งอะไร (SHA/PR)
- `pirate-force-server`: กิ่ง `claude/lane-ui-md7pjz` — 5 โมดูล `ui_*.py` + 5 ไฟล์เทส + fix cp874 + exemption
  ใน `test_npc_interaction_wire.py` — PR หัว `[LANE-UI] ...`
- `pf_bridge` PR `#1136` (`[LANE-UI] round md7pjz: claim` → เติมไฟล์รอบนี้) กิ่ง `claude/lane-ui-round-md7pjz`

## nonclaims
① ฟิลด์ทั้งหมดรู้แค่ "รูปเฟรม" (tag/offset/order/width) ไม่รู้ความหมาย — ไม่มีธุรกิจตรรกะใด ๆ ในไฟล์เหล่านี้เลย
② ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลย ไม่มีการเดา opcode/field ใหม่ใด ๆ — ทุกเลขมาจาก
`PF_SERIALIZER_FIELDS.tsv`/`PF_VITAL_NAMES.json` ที่ commit แล้ว ③ ไม่ได้ตรวจว่า `test_npc_interaction_wire.py`
exemption ของฉันได้รับความเห็นชอบจากเจ้าของไฟล์จริง (ไม่ทราบว่าใครเป็นเจ้าของ) — เทียบเคียงกับ precedent ที่มีอยู่
แล้วในไฟล์เดียวกัน ถ้า chief/COO เห็นว่าไม่เหมาะสมให้แก้ ④ ชุดเต็ม (`pytest -q` ไม่ ignore) บนต้นไม้ merge แล้ว — คืนผลแล้วระหว่างเขียนไฟล์รอบนี้: **9694 passed, 0
failed, 327 skipped** (327 มากกว่า `skip_census`'s 89 เพราะรันทั้งชุดจริง ไม่ ignore 48 ไฟล์เหมือน
`pytest_subset`) — เขียว ⑤ ไม่แตะ `runtime.py`/`vital_walk.py`/`app.py`/`store.py`/
`gm/` เลยสักบรรทัด ⑥ ไม่ยืนยันว่าแก้ครบทุกจุด — รอผล `pf-adversary` ก่อนปิดเด็ดขาด

## ADVERSARY_PENDING
`pf_bridge#1136` (และ PR เซิร์ฟเวอร์) — pf-adversary รีวิวโมดูลใหม่ทั้งหมด เริ่มต้นรอบพร้อมงาน ยังไม่คืนผลตอน push
· รอบถัดไปหยิบเป็นงานแรก

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
- หยิบผล `pf-adversary` ก่อน (ADVERSARY_PENDING ข้างบน) · ยืนยันผล `pytest -q` เต็มที่รันค้างไว้ตอน push
- เช็ค `.CONSUMED.txt` ของใบ `1120` ครั้งเดียว — ถ้าจุดเสียบ dispatch ของ chief ขึ้น main แล้ว (คาด ≤15:51) กลับมา
  ต่อสายจริงในรอบเดียวกัน (import โมดูลเหล่านี้เข้า branch ที่ chief เปิดไว้)
- ถ้ายังไม่มี: ไล่เก็บ RE fields ที่เหลือของสารบัญ (stall/guild storage/black market) ต่อ

— LANE-UI รอบ `md7pjz`
