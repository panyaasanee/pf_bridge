# LANE-UI round qzs91m -- 2026-09-06T04:57+07:00 start

## ล็อกรอบ
- list เปิด `[LANE-UI]` ทั้งสองรีโป ก่อนเริ่ม: ไม่มีใบเปิดอยู่ (list ใน pf_bridge state=open
  title contains "[LANE-UI]" = ว่าง) เปิด claim ของตัวเอง `pf_bridge#1431`
  (`[LANE-UI] round qzs91m: claim`, ไม่ draft, ไม่มี marker ตอนเปิด) จากกิ่ง
  `claude/peaceful-pascal-qzs91m` (pf_bridge) และ `claude/inspiring-feynman-qzs91m`
  (pirate-force-server) -- ทั้งสองกิ่งเป็นกิ่งที่ระบบมอบให้เซสชันนี้ตั้งแต่ต้น ไม่ได้ตั้งชื่อเอง
- list ซ้ำทันทีหลังเปิด: ไม่มีใบ `[LANE-UI]` อื่นเก่ากว่าและยังมีชีวิตแข่งอยู่ ⇒ ชนะ ทำงานต่อ
- 🔴 พบสี่ใบ `SYNC-NOTICE ... closed-never-merged` ใน mailbox (ดูหัวข้อกล่องจดหมายข้างล่าง):
  สามในสี่ใบ (`pr1401` round `c585y5`, `pr1410` round `bxr6uo`, `pr1420` round `couhc0`) เป็น
  claim PR ของ LANE-UI ที่ตายก่อนแตะโค้ด (reaper ปิดเพราะมี marker แต่มีแค่ไฟล์ claim เดียว) --
  ตรวจแล้วว่าไม่มีงานให้กู้ (แต่ละกิ่งมีแค่ `_claim.md`) ไม่ใช่ takeover ของรอบนี้ ดูจดหมายที่ส่ง
  COO ท้ายไฟล์รอบนี้

## กล่องจดหมาย (ADDRESSEE: LANE-UI / UI, ยังไม่ consumed ก่อนรอบนี้)
- `20260904_0332_LANE-PROMPT-*` -- ใบตั้งค่า routine prompt เดิม ไม่มี action item · stub วางแล้ว
- `20260906_0152_SYNC-NOTICE-*pr1377*` (round `c858fn`, เป็นใบ "yield to #1370") -- ไม่มีงานให้กู้
  · stub วางแล้ว
- `20260906_0152_SYNC-NOTICE-*pr1401*` (round `c585y5`, claim-only, ตายก่อนแตะโค้ด) -- ไม่มีงานให้กู้
  · stub วางแล้ว
- `20260906_0320_SYNC-NOTICE-*pr1410*` (round `bxr6uo`, claim-only, ตายก่อนแตะโค้ด) -- ไม่มีงานให้กู้
  · stub วางแล้ว
- `20260906_0444_SYNC-NOTICE-*pr1420*` (round `couhc0`, claim-only, ตายก่อนแตะโค้ด) -- ไม่มีงานให้กู้
  · stub วางแล้ว · แพทเทิร์นสามรอบติดที่ตายก่อนแตะโค้ด รายงาน COO แล้ว
  (`20260906_0501_LANE-UI-STATUS-three-dead-claim-only-rounds-in-a-row-before-this-one.md`,
  ไม่บล็อกงาน แค่รายงาน)
- ตรวจ `GT-184`/`GT-186` (ใบของ LANE-UI จากรอบก่อน `fzwt82`): chief (round `6z131u`/R362) รับทราบ
  บล็อก `ATTENDED:` ที่เสนอไปแล้ว แต่ยังไม่ลงคิวรอบนั้น ("ยกไปรอบหน้าข้อ 5") -- ตรวจ
  `GAME_TEST_QUEUE.md` สดรอบนี้: ทั้งสองใบยังเป็น `BLOCKED-ON-RE-266` ป้ายเดิม ยังไม่ถูกแก้เป็น
  `NEEDS-ATTENDED-CAPTURE`/`READY-FOR-ATTENDED-DUAL-LAYER` ตามที่เสนอ -- ยังไม่มีอะไรให้ LANE-UI
  ทำเพิ่ม (เป็นคิวของ chief แก้ไฟล์) ไม่ได้ consume ใหม่ (ใบเดิม consumed ไปแล้วรอบ `fzwt82`)

## AGENTS.md section 7 -- อ่านครบรอบนี้
ไม่มีกฎใหม่ที่กระทบงานของรอบนี้โดยตรง เทียบกับที่ใช้แล้วรอบก่อน (marker `PF-AUTOMERGE: v4`
derive จาก workflow, `pf_gate_preflight.py --pr-body` ก่อนเปิด/แก้ body, grep ก่อนเปิดใบ RE,
ถ้อยคำเวลา `pf-adversary` สามข้อ) -- ทั้งหมดยังเหมือนเดิม ใช้ตามนั้น

## งานหลัก (คิว LANE-UI) -- สถานะ
1. UI-B ล็อกเอาต์จริง headless: ยังไม่ wired เข้า `runtime.py` (grep ยืนยัน: ไม่มี
   `dispatch_real_exit_game_logout`/`ui_logout_exit_game` ใน `runtime.py` ณ `main` ปัจจุบัน)
   CORE-REQUEST ค้างรอ chief -- ไม่มีอะไรให้ LANE-UI ทำเพิ่มในเขตเขียนของตัวเองตอนนี้
2. UI-A กลับหน้าเลือกตัวละคร: `GT-184`/`GT-186` ยัง `BLOCKED-ON-RE-266` ในไฟล์คิวจริง (chief ยัง
   ไม่ลง `ATTENDED:` ที่เสนอ) -- ไม่มีโค้ดให้เขียนจนกว่าจะมีผล attended
3. tracepath auto-walk: `BLOCKED-ON-LANE-A accessor` ไม่เปลี่ยนตั้งแต่ chief `1407`
4. NPC shop: `BLOCKED-ON-LANE-DB interface` ไม่เปลี่ยน

⇒ **งานหลักทั้งสี่ข้อติดหมดเหมือนรอบก่อน** (2 ข้อรอเครื่อง Panya/chief, 2 ข้อรอสายอื่น) --
หยิบงานสำรองข้อ 2 (ฟังก์ชันถัดไปที่ layout รู้แล้ว) ตามกฎ (ไม่จบรอบเปล่า)

## งานสำรอง -- ทำรอบนี้
**[ทำแล้วรอบนี้]** กลุ่ม `Channel_` (แชท, 16 ของ 327 แถวในสารบัญ) -- อ่าน
`prompts/COMMON_LANE_ROUND.md`'s grep hint แล้วก่อนเริ่ม พบว่ามีของเดิมสามชิ้นที่ต้องเช็คก่อน
เขียนโค้ด (สำคัญ, กันเสียรอบ):
1. ห้าคลาสที่ใช้ serializer ร่วม (`LocalTalk`/`Party`/`Guild`/`ActorBoardcast`/`GMGlobal`) มีโมดูล
   เจ้าของอยู่แล้วในรีโปพร้อม ownership-gate test แบบ exact allowlist -- **ไม่แตะ**
2. รายงาน static byte-exact เดิม (`reports/PF_CHAT_CHANNEL001_CHANNEL_FAMILY_AND_ROUTING_STATIC_20260818.md`,
   grade A) ไขสคีมาไว้แล้วครบทั้ง 17 คลาส **แม่นกว่า** `PF_SERIALIZER_FIELDS.tsv` เอง -- TSV
   เขียนว่า wstring เป็น `UNTAGGED_WSTRING16LE_LEN32LE` แต่รายงานพิสูจน์ว่าจริง ๆ มี tag byte
   `0x48` นำหน้าเสมอ (ยืนยันด้วย disasm ของ codec `0x89A810`/`0x89A880`) -- ถ้าไม่เจอรายงานนี้
   ก่อนเขียนโค้ด จะได้โมดูลผิด (ขาด tag byte) ทั้งกลุ่ม
3. `Channel_JoinClassChannelVital` อยู่ใน grep hint ของ **LANE-CS** ใน
   `prompts/COMMON_LANE_ROUND.md` ไม่ใช่ของ UI -- เว้นไว้ (พร้อมคู่ `ClassChannelMessage` ตาม
   ดุลพินิจของรอบนี้เอง ไม่ใช่ข้อเท็จจริงที่มีแหล่งอ้างเดียวกัน -- ระบุแยกไว้ใน docstring)

ผลลัพธ์: `src/pirateforce_foundation/ui_channel_wire.py` (ใหม่) เข้ารหัส/ถอดรหัส 10 ใน 17 คลาส
(`ForbidTalkNotification`/`Whisper`/`CustomChannelMessage`/`OriginalSinChannelMessage`/
`JoinCustomChannel`/`LeaveCustomChannel`/`OnActorJoinCustomChannel`/
`OnActorLeaveCustomChannel`/`JoinOriginalSinChannel`/`LocalPerformance`) จาก field order ที่
พิสูจน์แล้วในรายงานข้อ 2 ข้างบน + `tests/test_ui_channel_wire.py` (ใหม่, 36 เทส) +
อัปเดต `docs/UI_LANE.md`. ไม่ต่อสายเข้า `runtime.py`/`vital_walk.py` -- pure wire shape เท่านั้น
เหมือนโมดูลพี่น้อง (`ui_treasurehunt_wire.py` ฯลฯ).

## ADVERSARY -- คืนผลแล้วรอบนี้ (ไม่ใช่ PENDING)
สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงาน (ครั้งที่ 1/2) ผลคืนก่อนจบรอบ พบสองข้อจริง แก้แล้วในรอบ
เดียวกัน (commit ที่สอง):
1. คลาสที่ 10 (`Channel_ForbidTalkNotificationVtial` `0xFDF2`) หายไปจากร่างแรก (ร่างแรกนับได้
   9 คลาส + 5 เจ้าของเดิม + 2 เว้นให้ CS = 16 ไม่ใช่ 17) -- เพิ่มแล้ว (dataclass + encode/decode +
   4 เทสใหม่)
2. เหตุผลเว้น `Channel_ClassChannelMessageVital` เขียนปนกับเหตุผลเว้น `JoinClassChannelVital`
   ราวกับมีแหล่งอ้างเดียวกัน ทั้งที่ grep hint มีแค่ตัวแรก -- แก้ docstring ให้แยกชัดว่าส่วนไหน
   เป็นข้อเท็จจริงมีที่มา ส่วนไหนเป็นดุลพินิจของรอบนี้เอง
เทสเพิ่มเติม: เติมเคส trailing-bytes ที่ขาดสำหรับ `OriginalSinChannelMessage`/
`LeaveCustomChannel` (adversary mutation-test ยืนยันโค้ดถูกอยู่แล้ว แค่ปิดช่องว่างเทส)
ไม่ต้องเรียก adversary รอบสอง (แก้เฉพาะ docstring/เพิ่ม class เดียวกันแพทเทิร์น/เทสเพิ่ม
ไม่ใช่ตรรกะใหม่ที่ซับซ้อน)

## เกต
`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` (ก่อน commit ที่สอง):
`[cp874]` PASS · `[skips]` PASS · `[mainmerge]` PASS · `[census]` PASS (มี WARNING ชั่วคราวตอน
`docs/UI_LANE.md` ยังไม่ commit -- แก้แล้วด้วยการ commit ก่อน push จริง) · `[branch]` PASS ทั้ง
สองรีโป · `[bridgesize]` PASS · `[scoreboard-manual]` PASS

## รอบหน้าทำอะไร
1. เช็คว่า `GT-184`/`GT-186` ถูก chief ลง `ATTENDED:` ในคิวจริงหรือยัง (รอบนี้ยังไม่ลง ตาม
   `6z131u`/R362 บอกว่า "ยกไปรอบหน้าข้อ 5" ของ chief เอง ไม่ใช่ของ LANE-UI)
2. ถ้างานหลักยังติดหมด หยิบงานสำรองกลุ่มถัดไปที่ layout รู้แล้ว (backlog เดิม:
   `Pets_`/`Express_`/`Activity_`/`CollectionObj_`/`KnowledgeGuru_`/`HitParade_` ที่ยัง
   ไม่ itemize -- `KnowledgeGuru_` มี `SUBCALL:`/`UNTAGGED_WSTRING16LE_LEN32LE` ปนกัน ต้องอ่านให้
   ครบก่อนเลือก อย่าเดาว่า "ไม่มี CALL_UNCLASSIFIED" แปลว่า layout ง่ายเสมอ -- บทเรียนจากรอบนี้)
3. `Channel_` ยังเหลือ `ForbidTalkNotification` (ทำแล้วรอบนี้) และ 7 คลาสเดิมที่เจ้าของอื่นแล้ว
   (5 sibling module + 2 CS) = ครบ 17 -- ไม่มีอะไรเหลือให้ LANE-UI ในกลุ่มนี้แล้ว

## QUEUE_TRIAGE
ไม่ใช่หน้าที่ของ LANE-UI (เป็นของ chief ตาม `AGENTS.md` section 7) -- ไม่เขียนบรรทัดนี้

SCOREBOARD: COMING | เขียนโมดูลถอดรหัสเฟรมแชท 10 ชนิด (กระซิบ/ข้อความช่องกำหนดเอง/เข้า-ออกช่อง/
ประกาศห้ามพูด ฯลฯ) ฝั่งเซิร์ฟเวอร์เสร็จพร้อมเทส 36 ตัวผ่านหมด แต่ยังไม่ต่อสายเข้าเกมจริง (ผู้เล่น
ยังกดอะไรไม่ได้จากงานนี้วันนี้) | PR `pirate-force-server` (กิ่ง `claude/inspiring-feynman-qzs91m`),
จดหมาย `20260906_0501_LANE-UI-STATUS-three-dead-claim-only-rounds-in-a-row-before-this-one.md`
