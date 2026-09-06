# LANE-UI round `x28wjw` -- 2026-09-06T09:24+07:00 start

## ล็อกรอบ
- list เปิด `[LANE-UI]` ทั้งสองรีโปก่อนเริ่ม: ว่างทั้งคู่ -- เปิดคลาม `pf_bridge#1462`
  (`[LANE-UI] round x28wjw: claim`) จากกิ่ง `claude/ecstatic-volta-x28wjw` (pf_bridge, ต้องสร้างใหม่
  ตามที่ผู้สั่งงานยืนยันว่ายังไม่มีบน origin) และ `claude/trusting-thompson-x28wjw`
  (pirate-force-server) -- ทั้งสองกิ่งเป็นกิ่งที่ระบบมอบให้เซสชันนี้ตั้งแต่ต้น ไม่ได้ตั้งชื่อเอง
- list ซ้ำทันทีหลังเปิด: ไม่มีใบ `[LANE-UI]` อื่นแข่งอยู่ -- ชนะ ทำงานต่อ

## กล่องจดหมาย (ADDRESSEE: LANE-UI)
- grep `notes_to_chief/*.md` หา `ADDRESSEE: LANE-UI` ซ้ำเอง (ไม่เชื่อผลที่ผู้สั่งงานให้มาเฉย ๆ):
  ทุกใบที่จ่าหน้าถึง LANE-UI มี `.CONSUMED.txt` คู่อยู่แล้ว (ตรวจด้วยสคริปต์วนลูปทุกไฟล์) --
  รวมสองใบล่าสุด `20260906_0551_COO-DECISION-ui0501-*` และ
  `20260906_0745_COO-DECISION-ui0631-*` (r364/bridgesize known-red, ไม่มีงานเพิ่มให้ LANE-UI) --
  **ไม่มีใบใหม่ให้บริโภครอบนี้**

## NOW.md -- ตรวจข้อ R364 ข้อ 2 ด้วย (ใหม่กว่าที่ผู้สั่งงานเช็คไว้)
NOW.md (ดึงสด 09:16 ก่อนเริ่มรอบ) เขียนว่า "READY 19 ใบไม่มี `ATTENDED:` ... UI 2" -- เขียนสคริปต์
สแกน `GAME_TEST_QUEUE.md` ทั้งไฟล์หาใบ `READY`/`🟢` ที่ไม่มีบล็อก `ATTENDED:` แล้วกรองด้วยเจ้าของใบ =
LANE-UI: ผลคือ **ศูนย์ใบ** -- `GT-251`/`GT-262` (สองใบที่เป็นของ LANE-UI และเคยเป็นเหตุของเลข "UI 2"
ในใบ `0631`/`0745` ที่ consumed ไปแล้ว) มีบล็อก `ATTENDED:` ครบทั้งคู่แล้วในไฟล์ที่ดึงสดรอบนี้ (`GT-253`
เป็น `PENDING` ไม่ใช่ `READY` เลยไม่นับ) -- แปลว่าตัวเลข "UI 2" ใน NOW.md ที่อ่านตอน 08:47 เป็นตัวเลขก่อน
chief archive/แก้ที่ `0745`/`0747` และไฟล์สดตอนนี้ปิดข้อนี้ไปแล้ว **ไม่มีงานเติม `ATTENDED:` ค้างให้
LANE-UI รอบนี้** (ตรวจเอง ไม่ได้เชื่อคำยืนยันของผู้สั่งงานเฉย ๆ)

## AGENTS.md section 7 -- อ่านครบรอบนี้
ไฟล์นี้ไม่มีหัวข้อเลข "7" ตรงตัว (11 หัวข้อทั้งไฟล์, นับลำดับแล้วหัวข้อที่ 7 = "Verification" --
เกต/คำสั่งตรวจสอบก่อน push, ตรงกับที่ `COMMON_LANE_ROUND.md` อ้างถึงเรื่องเกต) -- อ่านครบแล้ว
ไม่มีกฎใหม่ที่กระทบรอบนี้โดยตรงนอกจาก `KNOWN_RED_MAIN` เรื่อง `bridgesize` ที่อ่านผ่านใบ `0745`
ที่ consumed แล้ว (ไม่กระทบรอบนี้เพราะรอบนี้ไม่แตะ `GAME_TEST_QUEUE.md`)

## งานหลัก (คิวเริ่มต้นข้อ 1-2) -- ยังติดเหมือนสองรอบก่อน ตรวจซ้ำสดจากไฟล์ที่ดึงรอบนี้
1. UI-B logout wiring: ยังไม่มีอะไรให้ LANE-UI ทำเพิ่ม (CORE-REQUEST ค้างรอ chief เหมือนเดิม,
   `docs/UI_LANE.md` แถว `LogoutVital` subcode 1 ยังเขียน "CORE-REQUEST pending")
2. UI-A back-to-charselect: `GT-184`/`GT-186` ยัง `BLOCKED-ON-RE-266` ใน `GAME_TEST_QUEUE.md` จริง
   (grep บรรทัด 7052/7204 ยืนยันแล้วสด ไม่เปลี่ยนจากสามรอบก่อน)
3. tracepath auto-walk: `BLOCKED-ON-LANE-A accessor` ไม่เปลี่ยน (`docs/UI_LANE.md` แถวเดิม)
4. NPC shop: `BLOCKED-ON-LANE-DB interface` ไม่เปลี่ยน (`GT-230` ยังรอ)

⇒ ขยับ NOW/M ข้อไหน: **ไม่ได้ขยับ** ข้อไหนในคิวหลัก M2/P-1/P-2/P-3 -- งานหลักทั้งสี่ข้อของ LANE-UI
ยังติดเหมือนเดิม เหตุผลเดียวกับสามรอบก่อน (RE-266 ยังรอ attended capture, LANE-A accessor ยังบล็อก,
LANE-DB interface ยังไม่มี) หยิบ **งานสำรองข้อ 2** ของ `prompts/LANE-UI.md` แทน (ฟังก์ชันที่ layout
รู้แล้ว) ตามลำดับที่ผู้สั่งงานให้: **`Express_` กลุ่ม** (12 คลาสในสารบัญ)

## งานสำรอง -- ทำรอบนี้: `Express_` wire module

`awk -F'\t' '$1 ~ /^Express_/' external/PF_SERIALIZER_FIELDS.tsv` = 138 แถว ครอบคลุม 8 คลาส (จาก
12 คลาสในสารบัญ -- อีก 4 คลาสไม่มีแถวใน serializer TSV เลย). นับแถว `CALL_UNCLASSIFIED`/
`PE_IMPORT_*`/`JUMP_UNCLASSIFIED`/`ATOMIC_*`/`DYNAMIC_INTERLOCKED_*` ต่อคลาส (สคริปต์ python
เดียวกับที่รอบ `avt7pt` ใช้กับ `Pets_`):

- `Express_InitalizeActorExpressVital` (`0xF375`) 20/40 แถวเสีย -- ข้าม
- `Express_ClientGetExpressItemAttrsVital` (`0x2C5D`) 12/22 แถวเสีย -- ข้าม
- `Express_ClientReceiveNewExpressVital` (`0x0E0C`) 6/26 แถวเสีย -- ข้าม
- `Express_ClientSendExpressVital` (`0xBD0D`) 12/28 แถวเสีย -- ข้าม
- `Express_GetActorExpressDataFromDBVital` (`0x1F14`), `Express_GSConfirmActorExpressDataVital`
  (`0x278C`), `Express_GSAddNewExpressVital` (`0xA1E1`), `Express_GSSendSystemExpressVital`
  (`0xD6F1`) -- อยู่ในสารบัญ id แต่ **ไม่มีแถวใน `PF_SERIALIZER_FIELDS.tsv` เลย** (grep ชื่อคลาสไม่เจอ
  สักแถว) -- ไม่ใช่กรณี "ทัดเยอะไม่พอ" แต่เป็น "ไม่รู้ layout เลย" ต้องทำ static RE ตั้งแต่ต้น

เหลือ **4 คลาสที่แท็กครบทุกฟิลด์**: `Express_ClientRemoveExpressVital` `0xD82D` (u64, u64, u8) ·
`Express_ClientSendExpressResultVital` `0x1091` (u64, u8, wstring) ·
`Express_ClientcClaimExpressVital` `0xD5A8` (u64, u64, u8) · `Express_ResetExpressCountVital`
`0xBECD` (u64, u8) -- vital id มาจาก `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (grep
`Express_`), ไม่ใช่จาก serializer tsv (ไม่มีคอลัมน์ id) -- W/R ทุกคลาสรูปร่างเหมือนกันเป๊ะ (ตรวจด้วย
สคริปต์เทียบ tag/order/len ทั้งสองทิศ)

พบเรื่องแปลกหนึ่งจุด: `Express_ClientRemoveExpressVital` กับ `Express_ClientcClaimExpressVital`
มีแถว TSV เหมือนกันทุกประการ (span_start `0x006E7B20` เดียวกัน, sha256 เดียวกัน, tag/order/len
เดียวกันทั้งสามฟิลด์) -- เช็ค `PF_FIELD_VALIDATION.tsv` ยืนยันทั้งคู่ id คนละตัว (`0xD82D` vs
`0xD5A8`) จริง ไม่ใช่ความผิดพลาดของสคริปต์ -- ตีความว่าเป็น shared-serializer เหมือนกรณี
`Channel_` (ห้าคลาสใช้ serializer `0x65AD40` ร่วมกัน ที่ `ui_channel_wire.py` เคยเจอมาก่อน) --
เขียนเป็นสองดาต้าคลาส/ฟังก์ชันแยกกัน ไม่ยุบรวม (semantics คนละอย่าง แม้ wire shape เดียวกัน)

`Express_ClientSendExpressResultVital` field3 เป็น `UNTAGGED_WSTRING16LE_LEN32LE` (u32 LE length +
UTF-16LE, ไม่มี tag byte) -- ใช้ `ui_social_wire.encode_untagged_wstring`/`read_untagged_wstring`
เดิม (แบบเดียวกับที่ `ui_mail_wire.py` ใช้อยู่แล้ว) -- ต่างจากกรณี `Channel_` ตรงที่ไม่มีรายงาน static
byte-exact มาหักล้าง label นี้ ดังนั้นยึด label ของ TSV ตรง ๆ (นโยบายเดียวกับ `ui_mail_wire.py`/
`ui_friend_wire.py`)

ผลลัพธ์ (`pirate-force-server`): `src/pirateforce_foundation/ui_express_wire.py` (ใหม่, 4 คลาส) +
`tests/test_ui_express_wire.py` (ใหม่, 25 เทส + 8 subtests) + อัปเดต `docs/UI_LANE.md` (แถวใหม่
`Express`, ลบ `Express_` ออกจากรายการ NOT YET ITEMIZED, เพิ่มย่อหน้า nonclaim). ไม่ต่อสายเข้า
`runtime.py`/`vital_walk.py` -- pure wire shape เท่านั้น เหมือนโมดูลพี่น้องทุกตัว

grep ตาม `AGENTS.md` section 7 ก่อนเขียนโค้ด: ทั้ง 4 ชื่อคลาสที่ implement 0 hit ใน
`CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md`/`archive/` -- ไม่มีใบเปิดค้างอ้างถึง grep src/
ยืนยันไม่มีโมดูล `Express_` มาก่อนในรีโป

## ADVERSARY -- ADVERSARY_UNAVAILABLE claude/trusting-thompson-x28wjw
ค้นหา `pf-adversary` ผ่าน ToolSearch (คำค้น "pf-adversary") และ ListAgents ต้นรอบ: ไม่พบ tool/agent
type ชื่อนี้ในเซสชันนี้เลย -- บันทึก token `ADVERSARY_UNAVAILABLE` ตามกฎ แล้วทำ self-review แทน:
1. Re-derive field order/tag/len ทั้ง 4 คลาสจาก TSV เอง (สคริปต์ python อ่านตรงจากไฟล์ ไม่เชื่อ
   docstring) -- ตรงกับที่เขียนในโมดูลทุกฟิลด์
2. ตรวจ vital id ทั้ง 4 ตรงกับ `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` ด้วย grep ตรง ๆ
3. นับซ้ำแถวเสียของ 4 คลาสที่ข้าม (20/40, 12/22, 6/26, 12/28) และยืนยัน 4 คลาสที่ไม่มีแถวเลยจริง --
   ตัวเลขตรงกับที่เขียนในโมดูล/เอกสาร
4. grep ยืนยันไม่มี collision กับโมดูลอื่นและไม่ได้ต่อสายเข้า `runtime.py`/`vital_walk.py`
5. มิวเทตทดสอบสามแบบ (ในโปรเซส python ไม่แก้ไฟล์จริง): (ก) สลับลำดับเขียน field1/field2 ของ
   `ClientRemoveExpressVital` -- `test_round_trip` จับได้ (decode คืนค่าคนละตัวกับที่ encode ไป)
   (ข) ถอด `require_exhausted` ออกจาก decoder ของ `ResetExpressCountVital` --
   `test_trailing_bytes_after_a_full_match_fail_closed` จับได้ (decode สำเร็จทั้งที่มีไบต์เกิน)
   (ค) เปลี่ยนค่า vital id ของ `ClientRemoveExpressVital` จาก `0xD82D` เป็น `0xD82E` --
   `VitalIdTests` จับได้ทันที -- ทั้งสามกรณีเทสจับได้จริง ไม่ต้องแก้อะไรเพิ่ม
6. ตรวจเหตุผล shared-serializer (`ClientRemoveExpressVital`/`ClientcClaimExpressVital`) เทียบกับ
   ตัวอย่าง `Channel_` แล้ว -- แพทเทิร์นเดียวกัน คงสองดาต้าคลาสแยกตามที่ตัดสินใจ

## เทส
`PYTHONPATH=src python3 -m pytest tests/test_ui_express_wire.py -q` = 25 passed, 8 subtests passed
`PYTHONPATH=src python3 -m pytest tests/ -q` (ชุดเต็มบนต้นไม้ merge `origin/main` `2841f3c` แล้ว
เป็น commit สุดท้ายจริง) = 12053 passed, 361 skipped, 23474 subtests passed, 0 failed
(519.87s)

## เกต
`python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server`:
`[cp874]` PASS · `[skips]` PASS · `[mainmerge]` PASS · `[census]` PASS · `[branch]` PASS ทั้งสองรีโป ·
`[bridgesize]` PASS (รอบนี้ไม่แตะ `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md`/`AGENTS.md`/
`CHIEF_CONTINUATION.md`, `NOW.md` ยังใต้เพดาน -- ไฟล์เดิมที่เกินเพดานอยู่ก่อน (`old`) ไม่ใช่หนี้ของกิ่งนี้) ·
`[scoreboard-manual]` PASS · `[prbody]` PASS ตรวจ PR body ฝั่งเซิร์ฟเวอร์ก่อนเปิดจริง (1 บรรทัด
marker เป๊ะ ที่บรรทัด 22) ยืนยันด้วย GET หลังเปิด PR แล้วเห็น marker อยู่จริง

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR `[LANE-UI] round x28wjw: claim` (`#1462`) กิ่ง `claude/ecstatic-volta-x28wjw` --
  ลบ `_claim.md`, ไฟล์รอบนี้แทน `_claim.md` (ไม่มี `.CONSUMED.txt` ใหม่ต้องวาง -- ไม่มีใบใหม่ให้บริโภค
  รอบนี้)
- `pirate-force-server`: PR `#905` (`[LANE-UI] Express_ wire module: 4 fully-tagged classes, wire
  shape only`) กิ่ง `claude/trusting-thompson-x28wjw`, ไม่ draft, marker `PF-AUTOMERGE: v4` ยืนยัน
  แล้วด้วย GET -- `ui_express_wire.py` + `test_ui_express_wire.py` + `docs/UI_LANE.md`
- เลขใบใหม่รอบนี้: ไม่มี (ไม่ได้เปิด GT/RE ใหม่ -- โมดูลนี้ยังไม่มีใบเทสเพราะไม่ต่อสายเข้าเกม)

## nonclaims
(1) `ui_express_wire.py` ไม่อ้างความหมายฟิลด์ใด ๆ (express/parcel id, sender/recipient id,
result code ฯลฯ) -- `proven_semantics` ยัง `UNKNOWN` ทุกแถว
(2) ไม่ต่อสาย `ui_express_wire.py` เข้า `runtime.py`/`vital_walk.py` -- ของ CORE-REQUEST แยก
(3) ไม่อ้างว่าทั้ง 4 คลาสเคยถูกเห็นบนสายจริง -- `PF_FIELD_VALIDATION.tsv` เป็น `NOT_OBSERVED`/0
เฟรมทั้งสองทิศทางทุกคลาส
(4) ไม่อ้างว่า `ClientRemoveExpressVital`/`ClientcClaimExpressVital` เป็นการกระทำเดียวกันเพราะ wire
shape เหมือนกัน -- อ้างแค่ว่า byte layout เหมือนกัน id/ดาต้าคลาสยังแยกกันจริง
(5) ไม่อ้างว่าตรวจสอบ NOW.md ข้อ R364 ข้อ 2 (ใบ `ATTENDED:` ที่ขาด) ครบทุกสาย -- ตรวจเฉพาะใบที่เป็น
เจ้าของ LANE-UI เท่านั้น สายอื่นไม่ได้ตรวจ

## รอบหน้าทำอะไร
1. เช็ค `GT-184`/`GT-186` ว่า chief ลง `ATTENDED:`/เปลี่ยนหัวใบหรือยัง (ยังไม่ลงล่าสุดรอบนี้)
2. ถ้างานหลักยังติดหมด หยิบกลุ่มถัดไปที่ layout รู้แล้ว: `CollectionObj_`/`KnowledgeGuru_`/
   `HitParade_`/`Equipment_` (ตรวจ `CALL_UNCLASSIFIED` ก่อนเขียนโค้ดเสมอ ตามบทเรียนสี่รอบติด) --
   `Express_` ปิดไปแล้วรอบนี้ (4 ของ 12 คลาส เหลือ 8 คลาสรอ static RE)
3. `KNOWN_RED_MAIN` เรื่อง `bridgesize` บน `GAME_TEST_QUEUE.md` ไม่ใช่ของ LANE-UI แก้ (chief ใบ
   `0747`) -- ยังเป็นจริงรอบนี้เหมือนเดิม
4. NOW.md ข้อ R364 ข้อ 2 ("UI 2" ที่ขาด `ATTENDED:`) ตรวจสดแล้วรอบนี้พบว่าปิดไปแล้วจริง (ตัวเลข
   ในไฟล์ที่อ่านตอน 08:47 เป็นตัวเลขก่อน chief แก้ที่ `0745`/`0747`) -- ไม่ต้องตรวจซ้ำถ้า NOW.md
   ยังพูดถึงตัวเลขเดิมนี้อีก (เป็นเลขค้าง ไม่ใช่ของจริง)

## QUEUE_TRIAGE
ไม่ใช่หน้าที่ของ LANE-UI (ของ chief ตาม `AGENTS.md` section 7) -- ไม่เขียนบรรทัดนี้

SCOREBOARD: COMING | เขียนโมดูลถอดรหัสเฟรมพัสดุด่วน (express) 4 ชนิด (ลบพัสดุ/รับผลส่งพัสดุ/รับพัสดุ/
รีเซ็ตตัวนับพัสดุ) ฝั่งเซิร์ฟเวอร์เสร็จพร้อมเทส 25 ตัว+8 subtests ผ่านหมด แต่ยังไม่ต่อสายเข้าเกมจริง
(ผู้เล่นยังกดอะไรไม่ได้จากงานนี้วันนี้) | PR `pirate-force-server#905`, PR `pf_bridge#1462`

-- LANE-UI (round `x28wjw`)
