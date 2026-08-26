# GM round 2026-08-26 ~17:1x-17:4x (+07:00) — LANE-GM first round

🎯 เปิด LANE-GM ตามคำสั่งเจ้าของ (`PANYA-ORDER` 16:1x, จดหมาย `20260826_1630`) — ยึดล็อกด้วย draft PR ทั้งสอง repo ก่อนเริ่ม (`pf_bridge#123`, `pirate-force-server#66`) แล้วสร้าง GM-001/002/003/004 ตามลำดับที่สั่งไว้

## สร้างแล้ว (`pirate-force-server`, เขตเขียนของสายนี้ทั้งหมด)
- `src/pirateforce_foundation/gm/__init__.py`, `accounts.py`, `state_wire.py`, `command_capture.py`, `scene_catalog.py`, `commands.py`, `data/gm_scene_name_tip.tsv`
- `docs/GM_LANE.md`
- `tests/test_gm_accounts.py` (9) · `test_gm_state_wire.py` (8) · `test_gm_command_capture.py` (10, หลังแก้ pf-adversary) · `test_gm_scene_catalog.py` (7) · `test_gm_commands.py` (24, หลังแก้ pf-adversary) — 58 เทสใหม่ ผ่านทั้งหมด
- `pf-adversary` รันก่อน commit ตามกฎ (ดูผลข้อล่าง)

## ผลตรวจ
- สวีตเต็มรอบแรก (ก่อน pf-adversary แก้): 3264 เทส · หลังแก้ (ดูหัวข้อ "แก้ไขหลัง pf-adversary" ด้านล่าง): **3272 เทส**, 18 error เดิมเท่าเดิม (`ModuleNotFoundError: capstone`/`pefile`/`pytest` — cloud container ไม่มีแพ็กเกจพวกนี้ ไม่เกี่ยวกับรอบนี้), 212 skip เดิม — **ไม่มี regression จากรอบนี้** เขียว(cloud sanity)
- `pf-adversary` ตรวจ 5 โมดูล + เทสใหม่ก่อน commit ตามกฎบังคับ — พบ 2 HIGH + 1 MEDIUM + 1 LOW ยืนยันได้จริงทั้งหมด แก้ครบก่อน push (รายละเอียดด้านล่าง) ไม่มีอะไรหลุดเข้า `main` ระหว่างนี้

## ยังไม่ทำ (ตั้งใจ ไม่ใช่ลืม — เหตุผลเต็มใน `docs/GM_LANE.md`)
- ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` — ขอผ่าน `CORE-REQUEST-006` (เสนอเลข รอ chief ยืนยัน) แทน
- `gm/commands.py` v1 = parse+log เท่านั้น ไม่ execute คำสั่งไหนเลย (บล็อกด้วย layout ที่ยังไม่รู้ของ `TeleportVital` + ~~`GM_RunGMCommandResultVital`~~ (แก้: layout โครงสร้างของ `GM_RunGMCommandResultVital` พิสูจน์แล้ว จริง ๆ ที่ยังบล็อกคือความหมายของไบต์ผลลัพธ์ ไม่ใช่ layout — ดูหัวข้อ "แก้ไขหลัง pf-adversary") + wiring ที่ยังไม่มี)
- ยังไม่มี attended probe ที่ทำได้จริง — รอ `CORE-REQUEST-006` ต่อสายและ merge เข้า `main` ก่อน

## จดหมายที่ส่งรอบนี้
- `notes_to_chief/20260826_1731_LANE-GM-CORE-REQUEST-006-gm-state-after-login.md`
- `notes_to_chief/20260826_1732_LANE-GM-STATUS-round-one-gm001-002-003-004.md` (รวม "ค้นแล้ว: เจอ" ทั้งสองแหล่ง + แจ้งสาย A ว่า `gm/scene_catalog.py` ใช้ต่อได้)
- `notes_to_chief/20260826_1741_LANE-GM-CORRECTION-gm-run-command-vital-layout-already-proven.md` (แก้คำอ้างผิดในใบก่อนหน้า)

## nonclaim
โค้ดรอบนี้ทั้งหมดยังไม่ผ่านการต่อสาย runtime และยังไม่มีการเทสในเกมจริงแม้แต่นาทีเดียว — ทุกผลข้างต้นเป็นเทสหน่วยฝั่งเซิร์ฟเวอร์ (`unittest`, ในโปรเซส, ไม่มี client) เท่านั้น

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
ยังไม่มี — รอบนี้เป็น scaffolding ล้วน (allowlist, wire builder, catalog, parser) ยังไม่ต่อเข้า runtime จริง ผู้เทสยังทำอะไรในเกมไม่ได้เพิ่มจนกว่า `CORE-REQUEST-006` จะถูก merge เข้า `main`

## ค้าง
- `CORE-REQUEST-006` รอ chief ต่อสาย + ยืนยันเลขทะเบียน
- ~~RE-open ทั้งสามข้อจากใบ 1630 (ยังไม่มีใครทำ, ไม่ใช่ของใหม่รอบนี้)~~ **แก้แล้วด้านล่าง — ข้อ `GM_RunGMCommandVital`/`GM_RunGMCommandResultVital` มี layout โครงสร้างพิสูจน์แล้วจริง ๆ ไม่ใช่ "ยังไม่มีใครทำ"** เหลือค้างจริงแค่ 2 ข้อ (`GM_UpdateGMStateVital` handler ความหมาย, `TeleportVital`/`ForcePos`/`CWarpResult` layout) + trigger condition ของ 0x51E9
- GM-002 ต้องการรอบ attended จริง (พิมพ์ในแชทหลายแบบ) เพื่อได้ capture มาอ่าน layout — ยังไม่มีให้จับเพราะยังไม่ต่อสาย (ยังจริงอยู่ แม้ layout โครงสร้างจะรู้แล้ว เพราะยังไม่รู้ sub-path จริงที่ client ใช้)

## แก้ไขหลัง `pf-adversary` (ก่อน push ครั้งแรก — งานยังไม่เคยหลุดเข้า `main`)

`pf-adversary` ตรวจก่อน commit จริงพบ 2 ข้อ HIGH + 1 MEDIUM + 1 LOW ยืนยันได้จริงทั้งหมด แก้ครบก่อน push:

1. **HIGH (ยืนยันจริง)** — คำอ้าง "`GM_RunGMCommandVital`/`GM_RunGMCommandResultVital` ไม่มีแถวใน `PF_SERIALIZER_FIELDS.tsv`" ที่ก๊อปมาจากใบ 16:30 **เป็นเท็จ** — commit `5ab34dc` (09:50+07:00) เพิ่มแถวไปแล้วก่อนใบ 16:30 เกือบ 7 ชม. แก้ `gm/command_capture.py`, `gm/commands.py`, `docs/GM_LANE.md` ให้ตรงกับ HEAD จริง (มี layout โครงสร้างแล้ว ยังไม่รู้ความหมาย/sub-path) — จดหมายแก้ `20260826_1741_LANE-GM-CORRECTION-*.md`
2. **HIGH (ยืนยันจริง)** — `gm/command_capture.py`: สองคำสั่งจากบัญชีเดียวกันในวินาทีเดียวกันเขียนทับไฟล์กัน (ไม่มี uniqueness suffix, ไม่มี exist-check) — ข้อมูลหายเงียบ ๆ แก้ด้วย `os.open(O_CREAT|O_EXCL)` วนหาเลขต่อท้ายที่ว่างแทนการเขียนทับ + เทสคุมไว้ (`test_same_account_same_second_captures_do_not_overwrite_each_other`, `test_many_same_second_captures_from_one_account_all_survive`)
3. **MEDIUM (ยืนยันจริง)** — `gm/commands.py`: `warp <scene_id> x y` รับ `nan`/`inf` เงียบ ๆ เป็นพิกัด แก้ `_require_number` ให้ปฏิเสธค่าไม่ finite + เทสคุม
4. **LOW (ยืนยันจริง)** — ตัวกรองชื่อบัญชีของ `command_capture.py` ใช้ `str.isalnum()` (Unicode-aware) ทำให้ชื่อไทยถูกตัดกลาง grapheme และไม่มี length cap (เสี่ยง `ENAMETOOLONG`) แก้เป็น ASCII-only whitelist + ตัดความยาว 40 ตัวอักษร + fallback `"unnamed"` เมื่อไม่เหลืออะไรเลย + เทสคุม

เทสรวมหลังแก้: 58 (จากเดิม 50) ผ่านทั้งหมด · สวีตเต็ม 3272 เทส (จากเดิม 3264) 18 error เดิมเท่าเดิม (capstone/pefile/pytest ไม่เกี่ยวกับรอบนี้) ไม่มี regression ใหม่ — เขียว(cloud sanity)

## ตรวจซ้ำครั้งที่สอง — `pf-adversary` ยืนยันการแก้ทั้งสี่ข้อ + จับได้อีก 1 ข้อ LOW

รัน `pf-adversary` รอบสองบน diff ที่แก้แล้ว (ไม่ใช่ตรวจใหม่ทั้งหมด) — ยืนยันทั้งสี่ข้อข้างบนแก้จริง (ทดสอบ race condition จริงด้วย 16 โปรเซส × 200 เรียก ไม่ชนกันเลย, ตรวจ `grep`/`git log` เองบน `pf_bridge` ยืนยัน commit/sha ที่อ้างถูกทุกตัว) พบเพิ่มอีก 1 ข้อ:

5. **LOW (ยืนยันจริง)** — header comment ของไฟล์ capture ใส่ `account_name` ดิบไม่ผ่านการกรอง ⇒ ชื่อบัญชีที่มี `\n` ปลอมบรรทัด header เพิ่มได้ (เช่นปลอมบรรทัด `account=` อีกอัน) แก้ด้วย `str.encode("unicode_escape")` ก่อนเขียนลง header (ไบต์จริงยังอ่านได้ครบจาก hex dump ด้านล่างเหมือนเดิม) + เทสคุม (`test_account_name_cannot_forge_extra_header_lines`)

เทสรวมสุดท้าย: 59 · สวีตเต็ม 3273 เทส 18 error เดิมเท่าเดิม ไม่มี regression ใหม่ — เขียว(cloud sanity)

## ปิดรอบ — gate แดงจริงหนึ่งรอบ (ไม่ใช่ของ `pf-adversary`), แก้แล้ว, merge สำเร็จ

หลังปิด draft และแก้หัวข้อ PR (ขั้นตอนปกติ) ต่อสาย `wake gate` commit ตามกฎ — **`gate-windows` แดงจริง** (run `32960112999`, job `gate`, ตรวจแล้วว่าไม่ใช่ flake):
`pytest_subset` ล้มตั้งแต่ collection เพราะ `gm/scene_catalog.py` เช็ค sha256 ของ `gm/data/gm_scene_name_tip.tsv` ไม่ผ่าน — ไฟล์ commit ด้วย LF แต่ runner Windows เช็คเอาต์เป็น CRLF (`.gitattributes` ไม่มีกฎ `*.tsv` เลย ทั้งที่มีกฎ `text eol=lf` ให้ `.py`/`.md`/`.json`/`.sql` อยู่แล้วด้วยเหตุผลเดียวกัน) `skip_census` แดงตามเป็นผลพวง (pytest collection ล้มก่อนถึงโมดูลอื่น)

แก้ด้วยการเพิ่ม `*.tsv text eol=lf` ใน `.gitattributes` (บรรทัดเดียว เนื้อไฟล์ไม่เปลี่ยน sha256 เดิม) — **นี่คือไฟล์นอกเขตเขียนที่ประกาศไว้ของสายนี้** (`.gitattributes` ไม่อยู่ใน `src/pirateforce_foundation/gm/`/`scenarios/gm_*.json`/`tests/test_gm_*.py`/`docs/GM_LANE.md`) แต่แก้เพราะเป็นบั๊กที่ไฟล์ของสายนี้เองสร้างขึ้น เป็นบรรทัดเดียวไม่กระทบใคร และ CI แดงเป็นงานตอนนี้เสมอตามกฎ — แจ้งไว้ตรงนี้เพื่อความโปร่งใส

ระหว่างนั้น PR ถูก `merge-claude-pr.yml` ปิดอัตโนมัติ (ตามกฎ "gate แดง = ปิด PR กันล็อกค้าง" — branch ไม่หาย) เปิด PR เดิม (`#66`) กลับด้วย API (ไม่ใช่ PR ใหม่ ไม่เสียเลขคอมเมนต์เดิม) หลัง push ตัวแก้ — gate รอบใหม่ (commit `e9cc3a8`) เขียวหมด **PR #66 merge สำเร็จโดย `merge-claude-pr.yml`** เวลา `10:56:37Z` · pf_bridge PR #123 merge ไปแล้วก่อนหน้า (`10:49:24Z`)

**ทั้งสอง repo อยู่บน `main` แล้ว ณ จบรอบ — ไม่มีอะไรค้างบน branch ที่ยังไม่ merge**

## บทเรียนสำหรับรอบถัดไปของสายนี้ (หรือสายอื่นที่จะ commit ไฟล์ข้อมูลใหม่)
ไฟล์ข้อมูลที่ pin sha256 (แบบ `gm/data/*.tsv`) ต้องเช็ค `.gitattributes` ให้มีกฎ `eol=lf` **ก่อน** commit เสมอ ไม่ใช่หลัง gate แดง — `main` merge ไปแล้วก่อนจะทันเพิ่มเช็คลิสต์นี้ลง `docs/GM_LANE.md` เอง รอบถัดไปของสาย GM ที่จะเพิ่มตารางจาก gamedata อีก (เช่น `CONSTDATA_TH__MOBS`/`QUESTDATA_TH__QUEST` สำหรับ `npc on|off`) ควรเปิด `docs/GM_LANE.md` เพิ่มหัวข้อนี้เป็นข้อแรกก่อนสร้างไฟล์ข้อมูลใหม่
