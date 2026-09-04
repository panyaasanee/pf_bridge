# รอบ LANE-GM `sexjmq` — 2026-09-04T14:48+07:00 เริ่ม

## NOW.md — รอบนี้ขยับ NOW ข้อไหน
อ่าน `pf_bridge/NOW.md` เป็นไฟล์แรกของรอบ (ก่อนทุกอย่าง) ตามที่พรอมป์สั่ง
- ข้อที่ขยับ: **ไม่มีข้อของ NOW.md เอง** (M2/P-1/P-2/P-3/M4 ไม่ใช่งานของรอบนี้)
  รอบนี้ปิด **backlog ข้อ 1 ของสายตัวเอง** (`rounds/GM_20260904_1316_zjbjys_*.md`)
  ซึ่งเป็นงานที่ระบุไว้แล้วว่า "ทำได้ทันทีไม่ต้องรอ RE" — ไม่ใช่ข้อของ NOW.md แต่เป็นข้อของ
  ไฟล์รอบตัวเอง (ลำดับหาอันดับงานข้อ 4)
- §22 (`PANYA-DECISION 20260904_1158`): รอบก่อน (`zjbjys`) ทิ้ง `GATE_UNVERIFIED #736` ไว้
  ให้รอบนี้ตรวจก่อนทำอย่างอื่น — ตรวจแล้ว (ดูหัวข้อ "ล็อกรอบ" ข้างล่าง): `#736` **merged=true**
  (07:22:51Z = 14:22+07) ⇒ เกตผ่านแล้ว ไม่ใช่ `GATE_UNVERIFIED` อีกต่อไป ไม่ต้องแก้อะไร

## ล็อกรอบ
- ต้นรอบ list PR `open` ทั้งสองรีโปที่หัวข้อ `[LANE-GM]`: **ไม่มีเลยทั้งสองรีโป** ⇒ claim ใหม่
  ไม่ใช่ takeover
- claim: `pf_bridge#1154` (`rounds/GM_20260904_1448_sexjmq_claim.md` สามบรรทัด) เปิดแล้ว list ซ้ำ —
  ไม่มี `[LANE-GM]` ใบอื่นที่เก่ากว่า ไม่แพ้ · **ไม่ใส่ marker ตอนเปิด** (กติกา `NOW.md` + `AGENTS.md` §7)
- addendum A (ชะตา PR รอบก่อน): `pf_bridge#1138` (claim ของรอบ `zjbjys`) **merged=true**
  (07:09:46Z = 14:09+07) · `pirate-force-server#736` (งานจริงของรอบ `zjbjys`) **merged=true**
  (07:22:51Z = 14:22+07) ⇒ งานรอบ `zjbjys` อยู่บน `main` ทั้งสองรีโปแล้ว ไม่ต้อง cherry-pick
- ยืนยันก่อนเริ่ม: `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` **มีจริง**
  · `external/PF_PROTOCOL_REGISTRY.tsv` · `external/PF_SERIALIZER_FIELDS.tsv`
  · `notes_to_chief/reference_codex_attr/PF_A2_STRING_WIRE_TAG_DELTA.tsv` มีจริงทั้งหมด
  · **ไม่มี** client image / capture corpus / canonical DB / `gh` / หน้าจอ (ตรงตามบรีฟ)
  · session code = branch suffix ทั้งสองรีโป (`claude/serene-bell-sexjmq` /
    `claude/beautiful-sagan-sexjmq`) = `sexjmq` ตามรูปแบบที่ chief ใช้ (`wjqykr`)
- เวลา: heartbeat ล่าสุด `14:42` เทียบเวลาเริ่มรอบ `14:48` ห่าง 6 นาที ผ่าน

## กล่องจดหมาย (addendum B)
grep `ADDRESSEE: LANE-GM` เทียบ `.CONSUMED.txt`: พบสองใบค้างที่ commit หลัง `zjbjys` เริ่ม
(13:16) จึงไม่ถูกใบนั้นเห็น:
1. `20260904_1307_CHIEF-TO-LANE-GM-core-request-gm-053-needs-a-bigger-hookup-than-five-lines-deferred.md`
   (commit 13:32+07) — chief บอกว่า `CORE-REQUEST-GM-053` ยังไม่ลงรอบนั้น ต้องแตะจุดเรียก 4 จุด
   ใน `runtime.py` ไม่ใช่ 5 บรรทัด และถามความเห็นทาง (ก)/(ข) — **บริโภคแล้ว**: ไม่มีคำถามเปิดค้าง
   เพราะใบ `1409` (ข้างล่าง) ซึ่งมาทีหลังตอบไปแล้วว่า "ทาง (ข)" และเลื่อนไปรอบ 15:51 ของ chief เอง
   ตาม `COO 1346` ข้อ 3 · เขียนความเห็นของสายไว้ในสตับเพื่อบันทึก (เห็นด้วยกับทาง (ข))
2. `20260904_1409_CHIEF-TO-LANE-GM-your-0x430E10-ticket-is-re238-paste-the-body.md`
   (commit 14:22+07) — ใบร่าง `RE-0x430E10` ได้เลข `RE-238` แล้ว ให้ยกเนื้อลง
   `CLIENT_RE_QUEUE.md` เอง แทนที่ทุกจุด `RE-0x430E10` เป็น `RE-238` — **บริโภคแล้ว**:
   วางเนื้อใบเต็มใต้หัว `RE-238` ใน `CLIENT_RE_QUEUE.md` (สถานะ `PENDING (RESERVED)` →
   `OPEN`) ตรวจแล้ว `grep -rn "RE-0x430E10\|RE_0x430E10" pirate-force-server/src
   pirate-force-server/tests` = 0 hit (ชื่อใบเก่าไม่เคยถูกอ้างในโค้ด/เทส — ต่างจากการอ้าง VA
   `0x430E10` ดิบซึ่งมีอยู่จริงหลายจุดใน `attr_wire.py` และไม่ใช่เรื่องเดียวกัน แก้ไขคำอธิบายในคิว
   ให้ชัดแล้วหลังพบว่าคำอธิบายร่างแรกกำกวม)

ทั้งสองใบวาง stub `.CONSUMED.txt` แล้ว สำเนาต้นฉบับไป `notes_to_chief/consumed/` แล้ว
ไม่มีใบอื่นค้าง (ตรวจ `notes_to_chief/2026090[3-4]_*` ทั้งหมดที่ชื่อมี `TO-LANE-GM` หรือ
`ADDRESSEE: LANE-GM` แล้ว)

## งานที่หยิบ และทำไม
ลำดับหาอันดับงานตามพรอมป์: (1) จดหมายค้าง = บริโภคสองใบข้างบน แต่ทั้งคู่ไม่สร้างงานโค้ดใหม่
(ใบ `1307` ถูกตอบไปแล้วก่อนรอบเริ่ม, ใบ `1409` งานคือ "วางเนื้อใบลงคิว" ซึ่งทำเสร็จในหัวข้อ
กล่องจดหมายข้างบนแล้ว) → (2) CORE-REQUEST/คำตอบ chief ที่อ้างเลข GM-0xx = ไม่มีใบใหม่ที่ต้องทำ
ต่อ (GM-053 อยู่กับ chief แล้ว) → (3) GT queue อ่านอย่างเดียว ไม่มีอะไรใหม่ที่สายนี้ทำได้จากคลาวด์
→ (4) **ไฟล์รอบล่าสุดของตัวเอง หัวข้อ backlog**: `zjbjys` บันทึกไว้ตรง ๆ ว่า **"codec ของ
`0x8D30 GM_ForbidToTalkResultVital` และ `0x6CEC Activity_CheatCodeVital` ทำได้ทันทีจาก
registry + ตาราง serializer ที่พิสูจน์แล้ว ไม่ต้องรอ RE ใด ๆ"** ⇒ รอบนี้หยิบข้อนี้

---

## 1. RE-238 — เนื้อใบลงคิวแล้ว (รายละเอียดในหัวข้อกล่องจดหมายข้างบน)

## 2. codec ใหม่สองตัว ปิด `GM_VITALS` ที่เหลือ

`external/PF_SERIALIZER_FIELDS.tsv` ให้ layout ของทั้งสองข้อความไว้ครบแล้ว (แถว 4345-4356 และ
6283-6288) — ไม่มีอะไรต้องเดา ไม่มีอะไรต้องรอ RE เพราะ layout ระดับไบต์พิสูจน์แล้วในตารางที่
commit ไว้แล้ว สิ่งเดียวที่ต้องระวังคือคอลัมน์ tag ของฟิลด์สตริงในตารางนั้นเขียนว่า
`UNTAGGED_WSTRING16LE_LEN32LE` ซึ่ง `gm/command_wire.py`/`gm/cheat_wire.py` เคยแก้มาแล้วว่า
เป็นชื่อที่หยาบเกินไป (helper ตัวจริงส่ง tag byte `0x48` ก่อนความยาวเสมอ) — **รอบนี้ไม่ได้อนุมาน
โดยเทียบเคียงข้อความอื่น** ตาราง `PF_A2_STRING_WIRE_TAG_DELTA.tsv` มีแถวของ**ข้อความทั้งสองนี้
เองโดยตรง** (แถว 4347-4356 และ 6287/6288) ระบุ `corrected_tag=0x48` ตรง ๆ

### `gm/forbid_to_talk_wire.py` (ใหม่) — `GM_ForbidToTalkResultVital` (0x8D30, server->client)
สามฟิลด์: `tag 0x0B @+0x14` (u8) · `tag 0x14 @+0x18` (u32) · wstring แท็ก @+0x1C ·
เข้ารหัสผ่านช่อง `legacy` (`legacy.u8tag`/`u32tag`/`wstr_tag`) แบบเดียวกับ `gm/state_wire.py`
เป๊ะ — ใช้ `legacy.wstr_tag` ที่มีอยู่แล้วในไฟล์แช่แข็ง (`current/pf_login_game_server_v141.py:
590-592`) แทนการเขียน struct.pack ใหม่ ตรงตามกฎ "reuse the encoder that already ships"

### `gm/activity_cheat_code_wire.py` (ใหม่) — `Activity_CheatCodeVital` (0x6CEC, client->server)
หกฟิลด์: `tag 0x14 @+0x14` (u32) แล้วตามด้วย wstring แท็กห้าตัวที่ `+0x18/+0x34/+0x50/+0x6C/+0x88`
· decode-only (ข้อความขาเข้า เซิร์ฟเวอร์ไม่เคยส่งเอง) ท่าเดียวกับ `gm/command_wire.py` ที่ถอด
`GM_RunGMCommandVital` โดยไม่มี encoder

ทั้งสองไม่ผูกเข้า `dispatch.py`/`runtime.py` รอบนี้ — codec ไม่ใช่ปุ่มทำงาน `gm/gmui_catalog.py`
`BUTTONS` ยังว่างเหมือนเดิม `total_is_unknown()` ยังเป็น True

### `gm/gmui_catalog.py` + เทส
`GM_VITALS` สองแถวเปลี่ยนจาก `handler_module=None` เป็นชื่อโมดูลใหม่ · `vitals_without_a_codec()`
คืนว่างแล้ว (จากเจ็ดตัวเหลือศูนย์ตัวไม่มี codec) · แก้เทส
`test_the_two_vitals_with_no_codec_are_named_as_such` (ยืนยันข้อเท็จจริงเก่า) เป็น
`test_no_gm_surface_vital_lacks_a_codec_anymore` (ยืนยันข้อเท็จจริงใหม่) — pin ข้อเท็จจริงตรง
ไหนเปลี่ยน ไม่ใช่ลบเทสทิ้ง

### `docs/GM_LANE.md`
ขีดฆ่าบรรทัดเดิมที่บอกว่า "ไม่มี codec เลย" (ไม่ลบ) เติมหมายเหตุชี้ไปท้ายไฟล์ + เพิ่มหัวข้อรอบใหม่
`## รอบ sexjmq` บันทึกรายละเอียดทั้งหมด

## pf-adversary — 🔴 tool ไม่พร้อมในเซสชันนี้ ทำเองแทน ไม่ได้อ้างว่าตัวจริงรัน
เซสชันนี้ไม่มี Task/Agent launcher tool ให้เรียก subagent `pf-adversary` จริง (รายการ tool ที่ได้
มีแค่ Read/Grep/Glob/Bash/Edit/Write) ⇒ **ไม่ได้สั่ง pf-adversary ตัวจริง** ทำรีวิวปฏิปักษ์เองด้วย
เช็คลิสต์ scar-tissue เดียวกัน (`.claude/agents/pf-adversary.md`) แทน แล้วเขียนตรง ๆ แบบนี้แทน
การอ้างว่า "ผ่าน pf-adversary" ซึ่งจะเป็นเท็จ — พบช่องว่างการทดสอบ (ข้อ 2 "green because it never
got there") สี่จุดที่ draft แรกไม่ครอบคลุม แก้แล้วในรอบเดียวกัน:
- `forbid_to_talk_wire.py`: ไม่มีเทส odd-length guard, cap guard (decode-side), lone-surrogate
  encode failure, wrong-second-tag, truncated-before-second-field, accept-at-cap-boundary
  → เพิ่มครบ 7 เทสใหม่
- `activity_cheat_code_wire.py`: ไม่มีเทส truncated-before-first-field → เพิ่ม 1 เทส
- แก้บั๊กในเทสตัวเอง: `MAX_STRING_LENGTH + 1` เป็นเลขคี่ ชนการ์ด odd-length ก่อนถึงการ์ด cap ที่
  เทสตั้งใจวัด (ทั้งสองไฟล์) → เปลี่ยนเป็น `+ 2`
เนื่องจากไม่มี pf-adversary ตัวจริง **ไม่นับเป็นครั้งที่ 1/2 ของโควตา `1428`** (โควตานั้นนับ
เฉพาะการเรียก subagent จริง) — ถ้ารอบหน้ามี tool ให้เรียก แนะนำให้เรียกจริงกับไฟล์สองไฟล์นี้ก่อน
อื่น

## ค้นก่อนถอด — ค้นแล้ว: เจอ/ไม่เจอ
- `external/00_SEARCH_HERE_FIRST.md`, `gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ**
  ความหมายของฟิลด์ทั้งสองข้อความ (คนละชั้นจาก layout ไบต์ซึ่งพิสูจน์แล้วในตาราง serializer)
- `notes_to_chief/reference_codex_attr/` — **ค้นแล้ว: เจอ** `PF_A2_STRING_WIRE_TAG_DELTA.tsv`
  มีแถวของทั้งสองข้อความตรง ๆ (ไม่ใช่การเทียบเคียง)

## เขตเขียนที่แตะรอบนี้ (ตรวจ `git diff --stat` ก่อน push)
- `pirate-force-server`: `src/pirateforce_foundation/gm/forbid_to_talk_wire.py` (ใหม่) ·
  `src/pirateforce_foundation/gm/activity_cheat_code_wire.py` (ใหม่) ·
  `src/pirateforce_foundation/gm/gmui_catalog.py` ·
  `tests/test_gm_forbid_to_talk_wire.py` (ใหม่) ·
  `tests/test_gm_activity_cheat_code_wire.py` (ใหม่) ·
  `tests/test_gm_gmui_catalog.py` · `docs/GM_LANE.md`
- `pf_bridge`: `CLIENT_RE_QUEUE.md` (เนื้อใบ `RE-238`) ·
  `rounds/GM_20260904_1448_sexjmq_*.md` ·
  `notes_to_chief/20260904_1307_*.md.CONSUMED.txt` (ใหม่) ·
  `notes_to_chief/20260904_1409_*.md.CONSUMED.txt` (ใหม่) ·
  `notes_to_chief/consumed/20260904_1307_*.md` (สำเนา) ·
  `notes_to_chief/consumed/20260904_1409_*.md` (สำเนา)
- **ไม่แตะ** `runtime.py` / `app.py` / `pf_login_game_server_v141.py` / canonical DB /
  `scenarios/world_*.json` / `scenarios/combat_*.json`

## ชุดเทส
- ระหว่างทำงาน: `test_gm_forbid_to_talk_wire.py` · `test_gm_activity_cheat_code_wire.py` ·
  `test_gm_gmui_catalog.py` · `test_gm_state_wire.py` · `test_gm_cheat_wire.py` ·
  `test_gm_command_wire.py` · `test_gm_*.py` ทั้งหมด (2225 passed, 1280 subtests) ·
  `test_tree_is_cp874_safe.py` + `test_gm_source_is_cp874_safe.py` (ไฟล์ใหม่มีข้อความไทย
  ตรวจแล้วเข้ารหัส cp874 ได้)
- ชุดเต็ม: `git fetch origin main` แล้ว `git merge origin/main` (merge สะอาด ไม่มี conflict)
  แล้วรัน `pytest tests/` ครั้งเดียวบนต้นไม้ที่ merge แล้ว — ผล: ดูหัวข้อ "เกต" ท้ายไฟล์
- ไม่ได้เพิ่ม skip ใหม่รอบนี้ ⇒ ไม่ต้องซ้อม `skip_census` ตามกติกา `0053`+`0149`

## nonclaim
1. **GM ข้ามขั้นไหน:** **ไม่มี** — รอบนี้ไม่บูตเซิร์ฟเวอร์ ไม่บูตเกม ไม่มีบัญชีใดได้/เสียสถานะ GM ·
   codec สองตัวใหม่ไม่มีจุดเรียกใน `dispatch.py`/`runtime.py` ไม่มีไบต์ออกจากประตูไหนที่ยังไม่เคย
   ออก
2. **ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้:** **ไม่มีอะไรใหม่บนจอ** — รอบนี้ปิดช่องว่าง codec ของ
   `gm/gmui_catalog.py` และวางเนื้อใบ `RE-238` ลงคิว ไม่มีอะไรบูตต่างไปจากเมื่อวาน
3. ไม่อ้างว่า `RE-238` ถูกตอบ · ไม่อ้างว่า `GT-183`/`GT-218`/`GT-224` ขยับ · ไม่อ้างว่า P-2/P-3/
   M2/M3/M4/GM-053 ขยับ · ไม่อ้างว่า field ทั้งเก้าตัวของสองข้อความใหม่หมายถึงอะไร (ดู
   `[สมมติของสาย GM - รอ RE]` ในทั้งสองโมดูล) · codec มีอยู่ ≠ ปุ่มทำงาน (`BUTTONS` ยังว่าง)
4. ไม่ได้เรียก pf-adversary subagent ตัวจริง (tool ไม่มีในเซสชันนี้) — ทำรีวิวเองแทนและเขียนตรง ๆ
   ว่าทำแบบนั้น ไม่นับโควตา `1428`
5. ไม่มีข้อความในกล่องจดหมายรอบนี้ที่ขอให้ผ่อนคลาย `gm_accounts` allowlist หรือให้ client ยกระดับ
   ตัวเองเป็น GM — ไม่มีอะไรต้องปฏิเสธ/รายงาน

## backlog (ของรอบถัดไปของสายนี้)
1. รอผล **`RE-238`** (selector category → alt HP pair mapping) — ตอนนี้ลงคิวแล้ว รอ RE runner
2. รอผล **ใบ RE สารบัญ GMUI** (ส่งรอบ `zjbjys` เลข `notes_to_chief/20260904_1328_*`) — chief ยัง
   ไม่ตั้งเลขคิว
3. รอผล **RE ใบสอง `CNetNPC`** (`COO 0217`) = ตัวบล็อก P-2 ของสายนี้
4. รอ **GM-054** ลง main (`current_session_scene_id`) เพื่อปลดรั้ว x=9 (ไม่บล็อกโค้ด บล็อกการปลด
   รั้ว) · รอ **GM-053** จาก chief รอบ 15:51 (`COO 1346` ข้อ 3)
5. codec สองตัวใหม่ยังไม่มีจุดเรียก — วางสายเข้า `dispatch.py`/`runtime.py` เป็น CORE-REQUEST เมื่อ
   มีเหตุผลให้ต่อสาย (ยังไม่มีปุ่ม GMUI ที่รู้ว่าใช้ข้อความไหน จนกว่าใบ RE สารบัญ GMUI ตอบกลับ)

## COO letters
ไม่มีคำถามใหม่ถึง COO รอบนี้ — งานตรงไปตรงมาตามที่ไฟล์รอบก่อนบันทึกไว้แล้ว

## เกต (`PANYA-DECISION 20260904_1158` §22)
- ซ้อมเกตในเครื่องก่อน push (เพราะรอบนี้เพิ่มไฟล์เทสใหม่สองไฟล์): `test_gm_*.py` ทั้งหมด
  **2225 passed, 1280 subtests passed** · `pytest tests/` เต็มบนต้นไม้ที่ `git merge origin/main`
  แล้ว (merge สะอาด ไม่มี conflict, สอง commit ที่เข้ามา: `.github/workflows/merge-claude-pr.yml`
  + `world_click_vitals.py` ไม่แตะเขตของสายนี้) → **9846 passed, 323 skipped, 18903 subtests
  passed, exit 0 (363.61s)** → **เขียว(cloud sanity, local pytest)**
- ไม่ได้เพิ่ม skip ใหม่รอบนี้ ⇒ ไม่ต้องซ้อม `skip_census` แยก
- เปิด `pirate-force-server#740` (ไม่ draft · marker `PF-AUTOMERGE: v4` ใส่ตั้งแต่เปิด) แล้ว GET
  ยืนยัน: `state=open`, `draft=False`, marker อยู่จริงในบอดี้ — ยังไม่รอผล gate Windows ภายในรอบนี้
  ตามกติกาจบรอบข้อ 3 ("ไม่ต้องรอ gate Windows ไม่ต้องรอ PR เซิร์ฟเวอร์ merge — งานถูกส่งมอบให้
  reaper แล้วคือจบหน้าที่ของรอบ") — §22's 10-minute-wait-then-`GATE_UNVERIFIED` rule applies to
  the round that reads the gate result before ending, and this round's own end-of-round protocol
  (หัวข้อ "จบรอบ" ข้อ 2-3) explicitly overrides waiting for it; รอบถัดไปของสายนี้ต้องเปิดด้วยการ
  ตรวจ `#740` ก่อนทำอย่างอื่น ถ้ายังไม่ merge ภายใน 3 ชั่วโมง

## สถานะท้ายรอบ
- **push แล้ว รอ merge PR `pirate-force-server#740`** — เปิดแล้ว ไม่ draft · marker
  `PF-AUTOMERGE: v4` ยืนยันด้วย GET หลังเปิด (`state=open`, `draft=False`,
  `marker_present=True`) · สถานะ: **เปิดแล้ว รอเกต**
- **push แล้ว รอ merge PR `pf_bridge#1154`** (claim PR) — เติม marker หลัง push ไฟล์รอบนี้ครบทั้ง
  ไฟล์รอบ + จดหมาย + stub + ลบ `_claim.md` = ปลดล็อก
- 🔴 ห้ามอ่านว่า "เสร็จ" หรือ "อยู่บน main" จนกว่า workflow จะ merge จริง และรอบถัดไปเห็น
  `merged=true` ผ่าน `git merge-base --is-ancestor` บนโคลนที่ `fetch --unshallow` แล้ว

-- LANE-GM รอบ `sexjmq`
