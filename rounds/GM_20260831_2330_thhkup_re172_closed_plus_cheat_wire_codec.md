[สาย GM รอบ `thhkup` · 2026-08-31T23:30+07:00 (`TZ=Asia/Bangkok date`)]

# รอบ `thhkup` — RE-172 ปิดเป็น bounded-negative (ใบของสายนี้เอง) + `gm/cheat_wire.py` ใหม่

## หนึ่งบรรทัด

รอบก่อน (`qgmm2s`) เป็นรอบว่างเปล่าติดต่อกันหลายรอบตามที่กฎ F บันทึกไว้ (638/632/628,
418/414/410/404) — รอบนี้ **ไม่ว่างเปล่า**: (1) mailbox มีจดหมายใหม่สองใบชี้ให้เห็นว่า `RE-172`
เป็นของสาย GM เอง ตอบได้แบบ static ไม่ต้องรอ "สาย RE" — หยิบทำจริง ได้คำตอบลบทั้งสองข้อ ปิดใบ และ
(2) เพิ่มโมดูล `gm/cheat_wire.py` ตามตัวอย่างในกฎ F ข้อ (ก) ของ prompt รอบนี้

## 0. round-lock

- ต้นรอบ: repo ทั้งสองมี local clone อยู่แล้วจากรอบก่อน (`/home/user/pf_bridge` บน branch
  `claude/quirky-goodall-thhkup`, `/home/user/pirate-force-server` บน branch
  `claude/magical-mendel-thhkup`) — ทั้งสองยังไม่เคย push ไป origin (`git ls-remote` คืนว่าง)
  `pf_bridge` อยู่หลัง `origin/main` (sync commits จาก Windows bridge) → `git reset --hard
  origin/main` ก่อนเริ่มงาน `pirate-force-server` ตรงกับ `origin/main` อยู่แล้ว
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีอยู่จริง **แก้ตำแหน่งจากที่ prompt สมมติ**: อยู่ที่
  `pf_bridge/` (repo root) ไม่ใช่ `pf_bridge/external/` — ยืนยันด้วย `ls`/`find` ตรง ๆ
- heartbeat `_BRIDGE_HEARTBEAT.txt` ล่าสุด `23:12:02+07:00` เทียบต้นรอบ `23:19+07:00` ห่าง 7 นาที ผ่าน
- ตรวจ open PR: `search`/list ไม่ทำ (ข้อมูลจาก prompt ยืนยันแล้วว่าล็อกว่างตอนต้นรอบ) — ยึดล็อกด้วย
  empty commit "round claim: thhkup" ทั้งสองฝั่ง เปิด draft PR หัวข้อ "[LANE-GM] WIP round claim
  thhkup"

## 1. กล่องจดหมาย (ข้อ 1-3 ของโปรโตคอล)

`grep -rl "ADDRESSEE: LANE-GM" notes_to_chief/*.md` แล้วเช็คคู่ `.CONSUMED.txt`: **พบสองใบใหม่ที่ยังไม่
บริโภค** —

1. `20260831_2305_KA1A-TO-LANE-GM-you-are-waiting-on-a-ticket-assigned-to-yourself-that-needs-no-captures.md`
   (กะ1-A, 23:05) — ชี้ว่า `RE-172` (`CLIENT_RE_QUEUE.md:3277`) จ่าหน้า `[assigned สาย GM]` และ
   "สัญญาผู้บริโภค: สาย GM เปิดเอง บริโภคผลเอง" — ไม่ใช่ของ "สาย RE" (ซึ่งไม่มี routine คลาวด์ชื่อนี้
   จริง) และ pass criteria ของใบเขียนไว้ตรง ๆ ว่าตอบได้จาก static analysis ล้วน ไม่ต้อง capture/attended
2. `20260831_2315_KA1A-SELFCORRECTION-*.md` (กะ1-A, 23:15) — แก้คำ "สาย RE ไม่มีอยู่จริง" (ผิด — มันคือ
   Codex schedule บนเครื่อง Windows ของเจ้าของ ไม่ใช่ cloud routine) แต่ **ข้อเสนอหลักเรื่อง RE-172 ยัง
   ยืนทุกข้อ**

ทั้งสองใบใช้ได้จริง — ตรวจแล้วว่า RE-172 เขียนไว้ตรงตามที่กะ1-A อ้าง (`CLIENT_RE_QUEUE.md:3277-3299`)
วาง `.CONSUMED.txt` คู่กันแล้ว (สำเนาไป `consumed/`) พร้อมเหตุผลที่นำไปใช้จริง — ไม่ใช่แค่รับทราบเฉย ๆ

`ls -t notes_to_chief/*.md | head` เจอ `20260831_2325_KA1A-ROOTCAUSE-*` เพิ่ม แต่ `ADDRESSEE: chief`
(cc สายนี้เท่านั้น ไม่ใช่จ่าหน้า) — อ่านผ่าน ไม่ใช่ของที่ต้อง consume ตามโปรโตคอล ไม่มี COO-DECISION
ใหม่กว่า `1843` ที่เกี่ยวกับสายนี้

## 2. หยิบ RE-172 ทำจริง (ตอบทั้งสองคำถามจาก static source ที่ commit อยู่แล้ว)

รายละเอียดวิธีค้น/หลักฐานเต็มอยู่ใน `notes_to_chief/20260831_2326_RE-172-RESULT-*.md` (สรุปย่อ):

- **Q1** (message ID อื่นที่ carry ActorAttr/BasicAttr เต็มบล็อก): ค้นทั้ง 520 ชื่อ message ใน
  `external/PF_SERIALIZER_FIELDS.tsv` — ไม่มีแถวใดอ้าง codec entry point ของสองคลาสนี้เป็น call
  target ตรวจ candidate ที่ดูเกี่ยวข้องที่สุด (`CWebGMVital_GSGC`) โดยเฉพาะ — shape ไม่ตรง ตัดออก แม้แต่
  census ที่ลึกสุดในเครื่อง (`reference_codex_attr/PF_ATTR_CLASS_CENSUS.tsv`, งาน Codex เอง) ก็ยังบอกว่า
  ผูก vtable+0x34 ของสองคลาสนี้เข้ากับ container ใดไม่ได้ — **ไม่พบ**
- **Q2** (DB column อื่นนอก `characters.actor_wire`): อ่าน `model.py` เต็มไฟล์ + `migrations/001-005`
  เต็มทั้ง 5 ไฟล์ — ไม่มีคอลัมน์รูปร่างตรงกับ `attr_wire.py::FIELDS` เลย — **ไม่พบ**

ทั้งสองข้อลบตรงตาม pass criteria ของใบเอง ("ผลลบก็เป็นคำตอบ") ⇒ ปิด `RE-172` เป็น **DONE /
BOUNDED-NEGATIVE** อัปเดต `CLIENT_RE_QUEUE.md:3277` ในที่เดิม (ขีดฆ่าสถานะเก่า ไม่ลบ) ตามรูปแบบที่
`RE-152`/`RE-161`/`RE-163` เคยใช้

**ผลต่อ**: `COO-DECISION 20260831_1843` สั่งไว้ล่วงหน้าว่าถ้า RE-172 ตอบลบ ต้องส่งตรงถึงเจ้าของ (cc
COO) เป็นคำถามนโยบายทาง 1 (เสี่ยง ย้อนไม่ได้) vs ทาง 2 (อาจเป็นไปไม่ได้ทางเทคนิค) ไม่ใช่ COO เคาะแทน —
เปิดใบ `20260831_2327_LANE-GM-TO-OWNER-attr-wire-path1-vs-path2-after-re172-negative.md` ตามนั้น
`attr_wire.py`/`build_named_field_update` ยัง fail-closed เหมือนเดิมทุกไบต์ ไม่มีการแก้โค้ดจากผลนี้
รอบนี้

## 3. `gm/cheat_wire.py` (ใหม่ — ตัวอย่างในกฎ F ข้อ (ก) ของ prompt รอบนี้)

`CheatVital` (0x162E) proven เป็น single `UNTAGGED_STRING8_LEN32LE @+0x14`
(`external/PF_SERIALIZER_FIELDS.tsv` แถว 565-566, span_sha256
`3e7899321da79221d0bf2c5641dc7e0022bc6acf439794c7f61b6c7efe2f6fad`) — ไม่เคยมีโมดูลในเขตสายนี้ก่อน
รอบนี้ (`grep -rli CheatVital src/ tests/` = ว่างเปล่าก่อนรอบ)

`docs/GM_LANE.md` มีบันทึกเดิมไว้แล้วว่า "(reference only, not reused as GM wire)" — โมดูลใหม่นี้ **ไม่
ขัดกับบันทึกนั้น**: เป็น reference codec ล้วน (encode/decode round-trip) ไม่ import เข้า
`dispatch.py`/`runtime.py`/`chat_command*.py` เลย บทบาทเดียวกับที่ `teleport_wire.py`'s
`ForcePos`/`CWarpResult` เคยมีก่อน `warp_executor.py` ต่อสาย — เก็บ string เป็น raw `bytes` เสมอ ไม่
decode เพราะ byte encoding ไม่ proven

เทส: `tests/test_gm_cheat_wire.py` 14 เคส (encode bounds, round-trip, truncation/oversize/trailing-byte
rejection, vital-id check) — ผ่านหมด

## เขียว

`python3 -m pytest tests/test_gm_*.py -q` → **1164 passed, 529 subtests passed** (จาก 1150/523 รอบก่อน
— เพิ่ม 14 เคสใหม่ ไม่มี regression) รวมเทส tripwire `test_gm_tests_collect_without_posix.py` (ต้อง
`git add` ไฟล์ใหม่ก่อนถึงผ่าน — ทำแล้ว)

## pf-adversary

ไม่มี subagent ชื่อ `pf-adversary` แยกในอิมเมจนี้ (สอดคล้องกับที่รอบก่อน ๆ บันทึกไว้) — ทำ self-review
เข้มแทน: (1) `gm/cheat_wire.py` ไม่มี import ใด ๆ นอก `struct`/`dataclasses` ไม่แตะ state ใด ๆ (2)
`MAX_STRING_LENGTH` ป้องกัน malformed length prefix ไม่ให้ alloc เกินจริง (3) `decode_cheat_vital_payload`
ปฏิเสธ trailing bytes เหมือน `command_wire.py`/`teleport_wire.py` (4) ตรวจว่าไม่มีจุดใดใน `gm/` import
โมดูลใหม่นี้ (`grep -rl cheat_wire src/pirateforce_foundation/gm/` = เจอแค่ตัวมันเอง) ยืนยันว่า "ไม่ต่อ
สาย" เป็นจริงไม่ใช่แค่คำพูด

## nonclaim

1. ไม่อ้างว่า `RE-172` พิสูจน์ว่า **ไม่มี** แหล่งอื่นอยู่จริง — พิสูจน์ได้แค่ "ไม่พบในหลักฐาน static ที่
   commit อยู่ในเครื่องนี้"
2. ไม่แก้ fail-closed gate ใด ๆ (`attr_wire`/`say_wire`) รอบนี้ — ทั้งสองยังปิดเหมือนเดิมทุกไบต์
3. ไม่ให้สถานะ GM กับบัญชีที่ไม่อยู่ใน `gm_accounts.json` ไม่มีการประกาศ milestone จากผลใด ๆ รอบนี้
4. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
   `scenarios/combat_*.json` เลย
5. `gm/cheat_wire.py` ไม่อ้างว่า `CheatVital` เกี่ยวข้องกับ command channel จริงของสายนี้
   (`GM_RunGMCommandVital`) — offset `+0x14` ที่ตรงกันเป็นเรื่องบังเอิญของ struct คนละตัว ระบุไว้ใน
   docstring ของโมดูลเอง
6. ไม่ได้ลบไฟล์จดหมาย/ประวัติเดิมใด ๆ — `CLIENT_RE_QUEUE.md:3277` แก้ด้วยการขีดฆ่า+ต่อท้าย ไม่ใช่ลบ

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มีการเปลี่ยนแปลงที่ผู้เทสสัมผัสได้โดยตรง** — `RE-172` ปิดเป็นข้อมูลนโยบายส่งต่อเจ้าของ (ไม่ใช่ฟีเจอร์
ใหม่), `gm/cheat_wire.py` เป็น reference codec ที่ไม่ต่อสายเข้าอะไรที่ผู้เทสเรียกได้ `GT-172` (READY จาก
รอบก่อน) ยังเป็นทางเดียวที่ผู้เทส attended ทำได้เพิ่มจากเมื่อวาน

## PR

- `pf_bridge#<เลขจริงดูท้ายรอบ>` (draft ต้นรอบ → ready ท้ายรอบนี้)
- `pirate-force-server#<เลขจริงดูท้ายรอบ>` (draft ต้นรอบ → ready ท้ายรอบนี้ + wake-gate commit ท้ายรอบ)

— สาย GM รอบ `thhkup`
