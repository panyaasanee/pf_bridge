# รอบ GM `1gia62` — 2026-08-31T18:25+07:00

## บริบท

ต้นรอบ: `list_pull_requests(state=open)` ทั้งสอง repo คืน `[]` — ไม่มี PR ค้างเลย (round-lock ว่าง)
ตรวจรอบก่อนของตัวเอง (`rawblk`) ด้วย `pull_request_read(method=get)`: `pf_bridge#617` `merged=true`,
`pirate-force-server#401` `merged=true` (`list_pull_requests` list-view รายงาน `merged=false` ผิด ๆ
ให้กับ PR หลายสิบใบล่าสุดของทุกสาย รวมทั้งของตัวเอง — ตรวจซ้ำด้วย `get` ต่อใบแล้วพบว่าทุกใบ merged จริง
เป็น artifact ของ list endpoint ไม่ใช่ของจริง บันทึกไว้กันสายอื่นตกใจฟรี) ไม่มีงานหาย ไม่ต้อง cherry-pick
สาขาทั้งสองสะอาด (`git status --short` ว่าง) ยึดล็อกด้วย empty commit "round claim: 1gia62" เปิด draft
`pf_bridge#621` / `pirate-force-server#404`

## กล่องจดหมาย (ลำดับงานข้อ 1)

grep `ADDRESSEE: LANE-GM`/`ถึง: สาย GM` ที่ยังไม่มี `.CONSUMED.txt` คู่: พบหนึ่งใบ —
`20260831_1810_CHIEF-REPLY-GM-044-actor-wire-blob-is-AvatarAttr-not-ActorAttr-BasicAttr-does-not-match.md`

chief ตอบ `CORE-REQUEST-GM-044` (ที่สาย GM เปิดเองรอบ `rawblk`) ว่า **ไม่ตรง**: `characters.actor_wire`
sub-structure เป็น `AvatarAttr` (tag `0x26`/u32) คนละคลาสกับ `ActorAttr`/`BasicAttr` ที่
`gm/attr_wire.py::FIELDS` ใช้ (tag `0x12`/u16 กับ `0x32`/u64) ตรวจข้าม 3 แหล่งอิสระตรงกัน

ไม่พบ CORE-REQUEST/CHIEF-REPLY อื่นที่อ้างเลข GM-0xx ค้าง · `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md`
ไม่มีรายการที่อ้าง `GM-044` (ตรวจด้วย grep แล้ว) จึงไม่มีหัวใบคิวต้องปิด

## งานที่ทำ (หน่วยงานจริงหนึ่งหน่วยของรอบนี้)

หน่วยงานที่เลือก: **บริโภคผล `GM-044` เต็มรูปแบบตามที่ใบเดิม (`1736`) ประกาศไว้ล่วงหน้า** — "ไม่ตรง" ⇒ เปิด
ASK-COO นโยบาย แทนที่จะรอ RE ตอบ layout ต่อไปเรื่อย ๆ

ระหว่างร่างใบ ASK-COO พบว่าใบเดิมร่างไว้แค่สองทาง (1: ยอมรับความเสี่ยง / 2: จำกัดถาวร) แต่ chief เสนอทาง
ที่สามในใบตอบเอง (`1810` ท้ายใบ "งานถัดไปที่เสนอ"): หาแหล่งดิบอื่นก่อน — เพิ่มเป็นทาง 0 และเปิดใบ RE คู่ขนาน
แทนที่จะรอเขียน ASK-COO เปล่า ๆ (สอดคล้องกับหลักการข้อ 2 ของสายนี้: ไม่หยุดรอ ทำเท่าที่ทำได้ไปพร้อมกัน)

1. `pf_bridge/notes_to_chief/20260831_1825_LANE-GM-ASK-COO-attr-wire-raw-block-source-policy-after-gm044-negative.md`
   — ASK-COO เต็ม (3.9KB, ผ่านเกณฑ์ 8KB): สามทาง (0/1/2), เหตุผลว่าทำไมทาง 1 เข้าเงื่อนไข "หยุดรอจริง"
   (ข) ของสายนี้เอง (ย้อนไม่ได้ ไม่มี backup) จึงไม่ตัดสินใจเองแม้ติดป้าย [สมมติ], ทาง 2 อาจเป็นไปไม่ได้ทาง
   เทคนิคไม่ใช่แค่ "จำกัด" ถ้า client apply เป็น bulk-copy จริง, ข้อเสนอ (ลองทาง 0 ก่อน)
2. `pf_bridge/CLIENT_RE_QUEUE.md` — เพิ่ม `RE-172 ACTOR-BASIC-ATTR-LOGIN-OBSERVABLE-SOURCE-001`
   (assigned สาย GM, ผู้เปิด=ผู้บริโภคเอง): ถามสองข้อของ chief ตรง ๆ — เฟรม/message ID อื่นที่ประกอบ
   `ActorAttr`/`BasicAttr` แบบ server-observable, และ column/table อื่นใน DB schema ที่ persist ฟิลด์
   เหล่านี้อยู่แล้วหรือไม่ — pass criteria wire/DB เท่านั้น (static, ไม่ต้อง attended)
3. บริโภคจดหมาย `1810`: stub `.md.CONSUMED.txt` + สำเนาไป `consumed/`

**ไม่มีการแก้ `src/`/`tests/`/`scenarios/*.json` รอบนี้** — `gm/attr_wire.py` ยัง fail-closed เหมือนเดิม
(ไม่มี seed = ส่งอะไรไม่ได้) ไม่มีอะไรต้องแก้โค้ดจนกว่า `RE-172` หรือ ASK-COO ตอบกลับมา

## pf-adversary self-review

ไม่มี agent `pf-adversary` แยกในอิมเมจนี้ (เหมือนทุกรอบก่อนหน้าของสายนี้บันทึกไว้) self-review แทน:
(1) overclaim — ตรวจว่าใบ ASK-COO ไม่ได้อ้างว่าทาง 1 อันตรายแน่/ทาง 2 เป็นไปไม่ได้แน่ ทั้งคู่ระบุชัดว่าเป็น
static claim ยังไม่วัด (nonclaim 1) (2) safety — ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/
canonical DB/`gm_accounts.json` เลยสักไบต์ ไม่มี call site ใหม่ (3) เขตเขียน — เฉพาะ `pf_bridge/notes_to_chief/`,
`pf_bridge/CLIENT_RE_QUEUE.md`, `pf_bridge/rounds/` (4) เลขใบ RE — ตรวจซ้ำว่า `RE-172` ยังว่างจริงก่อนใช้
(`grep "## .* RE-17[2-9]"` คืนศูนย์ผลก่อนเขียน) กัน collision กับสายอื่นที่อาจเปิดพร้อมกัน (5) ตัวเลข list
PR ที่ผิด (merged=false ปลอม) — ตรวจซ้ำด้วย `get` ทุกใบก่อนเชื่อ ไม่ปล่อยให้ข้อมูลผิดหลุดเข้ารอบนี้

## เขียว

ไม่มีการแก้โค้ดรอบนี้ ไม่มีเทสให้รัน — `tests/test_gm_*.py` ยังอยู่ที่ `1150 passed, 511 subtests` จากรอบ
ก่อน (`rawblk`) ไม่เปลี่ยน

## nonclaim

1. ไม่ตัดสินใจนโยบายทาง 1 vs 2 เอง — เข้าเงื่อนไข "หยุดรอจริง" (ข) ของสายนี้เอง (ย้อนไม่ได้ ไม่มี backup)
   ส่งให้ COO เคาะ ไม่ใช่การหลบงาน
2. ไม่อ้างว่า `RE-172` จะได้คำตอบบวก — เปิดเป็นคำถามจริง อาจจบเป็น bounded-negative เหมือน `GM-044`
3. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/`scenarios/world_*.json`/
   `scenarios/combat_*.json`/canonical DB เลยรอบนี้
4. ไม่ให้สถานะ GM กับบัญชีที่ไม่อยู่ใน `gm_accounts.json` ไม่มีการประกาศ milestone จากผลที่ได้ด้วย GM
5. warp ด้วย GM ไปเกาะแล้วเห็นเกาะ ไม่ใช่ M2 ผ่าน — ไม่มีการอ้าง milestone ใดในรอบนี้
6. ไม่มี client image/จอในสภาพแวดล้อมนี้เหมือนทุกรอบ — รอบนี้เป็นจดหมาย/คิวล้วน ไม่มีการยิงเฟรมหรือ RE ใหม่
   ที่ต้องมีอิมเมจ

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ยังไม่มีอะไรใหม่สำหรับผู้เทส** — รอบนี้เป็นจดหมายนโยบาย + เปิดคิว RE ไม่ใช่โค้ดที่เทสได้ ตรงกับที่
`rawblk` บันทึกไว้แล้วว่ายังไม่มีคำสั่งแชทใหม่จนกว่าจะมีแหล่งดิบหรือคำตอบนโยบาย

## PR

- `pf_bridge#621` (draft ต้นรอบ ปิดท้ายรอบนี้เป็น ready + retitle)
- `pirate-force-server#404` (draft ต้นรอบ ปิดท้ายรอบนี้เป็น ready + retitle + wake-gate commit —
  ไม่มีไฟล์เปลี่ยนใน repo นี้รอบนี้ ยังต้องมี PR ตามล็อกรอบเดิม)

— สาย GM รอบ `1gia62`
