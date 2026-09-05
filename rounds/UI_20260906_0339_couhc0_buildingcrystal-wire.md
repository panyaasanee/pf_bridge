# LANE-UI round couhc0 -- 2026-09-06T03:17+07:00 start

## ล็อกรอบ
- list เปิด `[LANE-UI]` ทั้งสองรีโป ก่อนเริ่ม: ไม่มีใบ `[LANE-UI]` เปิดอยู่ (list_pull_requests
  state=open, pf_bridge) -- claim ใหม่ ไม่ใช่ takeover
- เปิดใบ claim ของตัวเอง `pf_bridge#1420` (`[LANE-UI] round couhc0: claim`, ไม่ draft, ไม่มี
  marker) จากกิ่ง `claude/ecstatic-volta-couhc0` (pf_bridge) และ `claude/trusting-thompson-couhc0`
  (pirate-force-server) -- ทั้งสองกิ่งเป็นกิ่งที่ระบบมอบให้เซสชันนี้ตั้งแต่ต้น (session-assigned
  `claude/*` branches), ไม่ได้ตั้งชื่อเอง ทั้งสองอยู่ตรง `origin/main` พอดี (ไม่มี commit ค้าง)
  ก่อนรอบนี้
- list ซ้ำทันทีหลังเปิด: ไม่มีใบ `[LANE-UI]` อื่นเก่ากว่าและยังมีชีวิตแข่งอยู่ ⇒ ชนะ ทำงานต่อ

## กล่องจดหมาย (ADDRESSEE: LANE-UI / UI, ยังไม่ consumed ก่อนรอบนี้)
- `grep -l "ADDRESSEE: UI" notes_to_chief/*.md` (ข้าม `.CONSUMED.txt` คู่): ว่าง -- ไม่มีจดหมายค้าง
  จ่าหน้าถึงสายนี้
- จดหมายรอบก่อน `20260905_2259_LANE-UI-TO-CHIEF-re266-consumed-propose-gt184-186-attended-block.md`
  มี `.CONSUMED.txt` วางแล้วจากรอบ `fzwt82` -- ตรวจ `GAME_TEST_QUEUE.md:55-57` รอบนี้: หัวใบ
  `GT-184`/`GT-186` ยังพิมพ์ `BLOCKED-ON-RE-266` เหมือนเดิม, chief ยังไม่รับ/อัปเดตหัวใบตามที่เสนอ
  -- ไม่ใช่หน้าที่ LANE-UI แก้ไฟล์นั้นเอง (ไฟล์ของ chief) เขียนไว้ในบันทึกนี้เฉยๆ ให้รอบหน้าเช็คอีกที

## AGENTS.md section 7 -- อ่านครบรอบนี้
อ่านทั้งหมดตั้งแต่บรรทัด "ห้ามทำ" ถึงจบ ไม่มีกฎใหม่ที่กระทบงานของรอบนี้โดยตรงนอกจากที่ใช้ไปแล้ว:
grep-first ก่อนออกใบ/ก่อนประกาศ "ไม่มี", ถ้อยคำ `pf-adversary` (สั่งต้นรอบ, push ได้แม้ผลไม่คืนพร้อม
บันทึก `ADVERSARY_PENDING`, ห้ามเขียน "ผ่าน adversary" ก่อนผลจริงคืน), marker `PF-AUTOMERGE: v4`
ต้องตรงกับ `.github/workflows/merge-claude-pr.yml` (ตรวจแล้วตรงกับที่ใช้อยู่แล้ว), ceiling ไฟล์กลาง
(ตรวจผ่าน `pf_gate_preflight.py`).

## งานหลัก (คิว LANE-UI) -- สถานะ
1. UI-B ล็อกเอาต์จริง headless: **ปิดแล้วก่อนรอบนี้** (`#846` merged) -- ยังไม่ wired เข้า
   `runtime.py` dispatch จริง, CORE-REQUEST ค้างรอ chief ต่อ ไม่มีอะไรให้ LANE-UI ทำเพิ่มในเขตเขียน
   ของตัวเองตอนนี้ (ไม่เปลี่ยนตั้งแต่รอบ `fzwt82`)
2. UI-A กลับหน้าเลือกตัวละคร: **BLOCKED-ON-RE-266 (static ceiling)** -- รอ chief รับข้อเสนอ
   `ATTENDED:` block แล้วบูต attended (ไม่เปลี่ยนตั้งแต่รอบ `fzwt82`, ดูกล่องจดหมายข้างบน)
3. tracepath auto-walk: BLOCKED-ON-LANE-A accessor (ไม่เปลี่ยน)
4. NPC shop: BLOCKED-ON-LANE-DB interface (ไม่เปลี่ยน)

⇒ **งานหลักทั้งสี่ข้อยังติดหมดเหมือนรอบก่อน** (2 ข้อรอเครื่อง Panya/chief, 2 ข้อรอสายอื่น) -- ทำ
คิวข้อ 3 ต่อ (ฟังก์ชันถัดไปตามแผน `docs/UI_LANE.md` ที่ layout รู้แล้ว)

## งานที่ทำรอบนี้ -- คิวข้อ 3: BuildingCrystal wire modules (11/13 คลาส)
สแกน `external/PF_SERIALIZER_FIELDS.tsv` หา group ถัดไปที่ layout รู้แล้วทั้งหมด (ทุกแถวมี tag
จริง ไม่มี `CALL_UNCLASSIFIED`/`PE_IMPORT_*`/`SUBCALL`/`ATOMIC_*`/`DYNAMIC_*` ปน) ในบรรดา 15 กลุ่ม
ที่ยังไม่ itemize: `KnowledgeGuru_` ตกรอบ (มี `SUBCALL:0x0069F980` ปนทุกคลาส, ตรวจพลาดในรอบแรกที่
กรองแค่ `CALL_UNCLASSIFIED`/`PE_IMPORT`), `Channel_` ทุกคลาส clean จริงแต่ 5/17 ถูกทำไปแล้วโดย
`channel_message_hypothesis.py`/`chat_input_hypothesis.py` (โมดูลเก่าก่อนยุค TSV-driven) และ
`Channel_WhisperVital` ถูกปฏิเสธไว้แล้วในโมดูลนั้น (serializer คนละตัว) -- เลือก `BuildingCrystal_`
แทน: clean 11/13 คลาส, ไม่มีใครแตะมาก่อน (`grep -rln "BuildingCrystal" src/ tests/` ว่าง)

ไฟล์: `pirate-force-server/src/pirateforce_foundation/ui_buildingcrystal_wire.py` (ใหม่, 11
dataclass + encode/decode คู่) + `tests/test_ui_buildingcrystal_wire.py` (ใหม่, 46 เทส) +
`docs/UI_LANE.md` (แถวใหม่ + nonclaim bullet, ตัด `BuildingCrystal_` ออกจากแถว "NOT YET ITEMIZED")

รายละเอียด field-tag/vital-id เต็มอยู่ใน PR body (`pirate-force-server#881`). สรุป: 11 คลาสจาก 13
ในกลุ่มนี้ทุกแถว fully tagged (`0x08`=u8, `0x12`=u16, `0x32`=u64 -- legend เดิมของ
`ui_social_wire.py`), `W`/`R` เหมือนกันทุกคลาส. ตัดออก 2 คลาสแบบเดียวกับที่โมดูลพี่น้องตัดคลาสที่
สามของกลุ่มตัวเองออก: `BuildingCrystal_UpdateCrystalSlotVital` (`0x2D5C`, มี
`CALL_UNCLASSIFIED`/`ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C` ปน) และ
`BuildingCrystal_UpdateNextAbsorbTime` (แถว field เองสะอาดแต่ไม่มี vital id ใน
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` เลย -- ไม่ใช่การกระทำจริงบนสาย)

grep แล้วตาม AGENTS.md §7: `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` ไม่มีคำว่า `BuildingCrystal`
· `archive/`/`notes_to_chief/`/`notes_to_chief/reference_codex_attr/` มีแต่ตัวสารบัญ/เซนซัสสถิตเอง
กับใบ RE คนละเรื่อง (`options-apply-server-setting`) ที่ไม่ได้เอ่ยชื่อกลุ่มนี้ -- ไม่มีใบ RE/GT เดิม
สำหรับกลุ่มนี้ · `external/PF_FIELD_VALIDATION.tsv` ทั้ง 11 คลาส `status=NOT_OBSERVED`,
`observed_frames=0` ทั้ง W/R เหมือนกลุ่ม TreasureHunt/Gathering/Winemaking ก่อนหน้า -- ไม่มีการ
อ้างทิศทาง/verb/ack pattern ใดๆ

## pf-adversary
สั่งต้นรอบพร้อมเริ่มงาน (ครั้งที่ 1/2) หลัง pf-builder ส่งมอบ diff -- **ผลคืนแล้วก่อนจบรอบ: ไม่พบ
ข้อบกพร่อง**. วิธีตรวจ: ตรวจ tag/width/vital-id ทุกตัวจาก TSV เองใหม่ (ไม่เชื่อ docstring),
ยืนยันการตัด 2 คลาสถูกต้องจริง, รันมิวแทนต์สองตัวบน `DoAbsorbingVital` (สลับ tag byte ผิด,
ตัด `require_exhausted` ออกจาก decode) ทั้งคู่ทำให้เทสแดงตามคาด แล้วคืนโค้ดเดิม. หมายเหตุ
กระบวนการที่ adversary ชี้: commit ถูก push ไปแล้วตอนที่ adversary ยังตรวจไม่เสร็จ (บันทึก
`ADVERSARY_PENDING` ไว้ใน commit message ตอน push ตามกฎ "push ตามเดิม ห้ามถือล็อกรอ" เพราะ
เครื่องมือใช้เวลา 25-50 นาที) -- adversary ยืนยันว่าเนื้อหาที่ push ตรงกับที่ตรวจทุกตัวอักษร
ผลจึงยังยืนอยู่ ไม่ต้องแก้อะไรเพิ่ม ไม่มี `ADVERSARY_PENDING` ค้างข้ามรอบ

## เกต
`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` บนกิ่ง
`claude/trusting-thompson-couhc0`: `[cp874]` PASS · `[skips]` PASS (ไม่มี skip ใหม่) ·
`[mainmerge]` PASS (`origin/main` `44f4366` อยู่ใน HEAD แล้ว) · `[census]` PASS · `[branch]` PASS
ทั้งสองฝั่ง · `[bridgesize]` PASS (ไม่มีไฟล์กลางที่กิ่งนี้ทำให้โตกว่า `origin/main` ขณะเกินเพดาน) ·
`--pr-body ... --pr-stage final` PASS ก่อนเปิด PR แล้ว GET body ยืนยัน `PF-AUTOMERGE: v4` อยู่จริง
(`pirate-force-server#881`)

## PR
`pirate-force-server#881` เปิดแล้ว ไม่ draft มี marker ตั้งแต่เปิด (`html_url` ยืนยันด้วย
`pull_request_read get`, `mergeable_state: unstable` = gate กำลังรัน ยังไม่ merge)

## รอบหน้าทำอะไร
1. เช็คว่า `pirate-force-server#881` merge แล้วหรือยัง (`git merge-base --is-ancestor` ก่อนอ้างว่า
   อยู่บน main)
2. เช็คว่าจดหมาย `20260905_2259_LANE-UI-TO-CHIEF-*` (GT-184/186 header) ถูก chief รับหรือยัง --
   ถ้ายัง ไม่ต้องส่งซ้ำ แค่ตรวจสถานะ
3. ถ้างานหลักยังติดหมด หยิบกลุ่มถัดไปที่ layout รู้แล้ว: candidate ที่เหลือหลัง `BuildingCrystal_`
   ตามความสะอาดของ tag (นับใหม่ด้วยตัวจำแนกที่รวม `SUBCALL`/`ATOMIC_*`/`DYNAMIC_*` เป็น "ไม่สะอาด"
   ไม่ใช่แค่ `CALL_UNCLASSIFIED`/`PE_IMPORT_*` -- บทเรียนจากที่ `KnowledgeGuru_` ตกรอบตอนแรก):
   `Dyeing`/`Appraisal` (ทุกคลาส clean, กลุ่มเล็ก) เป็นตัวเลือกถัดไปที่ตรวจเร็วที่สุด
4. เขียนจดหมาย/สอบถาม chief ว่าทำไม commit ของ Gathering/Winemaking (`a30d345`/`2d07850` บน
   `pirate-force-server` main) ไม่มีไฟล์รอบ `rounds/UI_*.md` คู่กันใน `pf_bridge` -- พบตอนรอบนี้ตรวจ
   ประวัติ `docs/UI_LANE.md` แต่ไม่ใช่ตัวบล็อกงานของรอบนี้ จึงไม่ได้ตามสืบต่อ บันทึกไว้ให้ chief/COO
   เห็นเฉยๆ (อาจเป็นรอบที่หายจริงตามกฎ "รอบที่จบโดยไม่ push = รอบที่หายไปทั้งรอบ")

## QUEUE_TRIAGE
ไม่ใช่หน้าที่ของ LANE-UI (เป็นของ chief ตาม `AGENTS.md` section 7) -- ไม่เขียนบรรทัดนี้

SCOREBOARD: COMING | เขียนโมดูลถอดรหัสเฟรมระบบ "คริสตัลอาคาร" (ฝัง/สกัด/ดูดซับ/เพิ่มสารอาหาร/
เพิ่มความเงางาม/ซื้อบริการ/เร่งความเร็ว) ฝั่งเซิร์ฟเวอร์เสร็จ 11 คลาส พร้อมเทส 46 ตัวผ่านหมดและ
ผ่าน pf-adversary แล้ว แต่ยังไม่ต่อสายเข้าเกมจริง (ผู้เล่นยังกดอะไรไม่ได้จากงานนี้วันนี้) | PR
`pirate-force-server#881` (กิ่ง `claude/trusting-thompson-couhc0`, commit `18696cc`)
