# CS round fv5xnu — backup item 1 (read 3 hypothesis files to completion) · GT-116 nonclaim reopens an untickered question

เวลาเริ่ม 2026-09-04 21:10 +07:00 · เวลาปิด 2026-09-04 21:13 +07:00 · claim `pf_bridge#1206`

## ขยับ NOW/M ข้อไหน

**ไม่ขยับ M2/M3/M4/M5** — รอบนี้เป็นงานสำรอง (อ่าน+ยืนยัน) ตาม `COO-DECISION 20260904_2046` ข้อ 3: งานหลัก
ของ CS (ผูก `resolve_skill_damage`/`damage_by_skill.py` เข้าฟิลด์จริง) ยังติดเครื่อง Panya (`GT-243`
`🟡 PENDING` — precondition P0 ยังไม่ยืนยัน)

**เหตุที่ไม่ขยับ**: ไม่มีทางลัดฝั่งคลาวด์สำหรับงานหลัก เหมือนรอบก่อน (`plg1ne`) — รอบนี้จึงหยิบงานสำรองข้อ 1
ที่ `plg1ne` วางคิวไว้แทน (`1450`: ห้ามรอบว่าง)

## งานสำรองข้อ 1 — อ่านจบทั้งสามไฟล์ (queue เดิมจาก `plg1ne`)

อ่านทั้งไฟล์ (ไม่ใช่แค่หัว) ทั้งสามไฟล์ที่ `plg1ne` ทิ้งไว้เป็นข้อ 1:

1. `src/pirateforce_foundation/persistence_starting_skills.py` (68 บรรทัด) — resolver สมบูรณ์:
   `resolve_starting_skill_ids(class_id) -> tuple[int,int,int,int] | None` ดึงจาก `class_catalog`
   (ของ LANE-CS เอง) เท่านั้น ไม่มี DB/wire/socket ในไฟล์นี้เลย ปฏิเสธ `bool`/non-`int` (`TypeError`) ·
   `None` แบบมีชื่อสำหรับ `class_id` ที่ catalog ไม่รู้จัก (ไม่เดา) · **ไม่มีช่องว่างเหลือในตัวไฟล์เอง** —
   สิ่งที่ขาดคือ "ผู้เรียก" ตอนสร้างตัวละครจริง ซึ่งอยู่นอกเขตเขียนของ LANE-CS (docstring ของโมดูลเองระบุตรง ๆ
   ว่าเป็นจุดเสียบของ chief ผ่าน CORE-REQUEST คนละใบกับที่ทำไปแล้วในชิ้น 1)
2. `src/pirateforce_foundation/learn_skill_request_hypothesis.py` (530 บรรทัด, `HYP-PF-034`, vital
   `0x36AA`) — decoder ฝั่งเซิร์ฟเวอร์ที่ตรงตาม delivery table (`GT-050` job 1-2) เป๊ะ: u32 tag `0x14` +
   u8 tag `0x0B`, 7 ไบต์ payload, fail-closed 6 เหตุผลตั้งชื่อครบ · `production_allowed=False` ตลอด · **ความ
   หมายฟิลด์ทั้งสอง (`request_u32_0x14`/`request_u8_0x18`) ไม่รู้จริง ตั้งใจไม่ตั้งชื่อ** · ทิศทางธรรมชาติของ
   `0x36AA` (ไคลเอนต์เคยส่งจริงไหม) ก็ไม่พิสูจน์เช่นกัน (nonclaim ของโมดูลเอง)
3. `src/pirateforce_foundation/learn_skill_result_hypothesis.py` (795 บรรทัด, `HYP-PF-033`, vital
   `0x673C`) — encoder ฝั่งเซิร์ฟเวอร์ตรงตาม write/read loop คู่ที่ `GT-050` พิสูจน์แล้ว (`count`u16 + เรคคอร์ด
   12 ไบต์ `(u32·u16·u32)` × N + trailing `u8` ที่ `+0x2C`) · sweep 5 สเต็ป (`COUNT0_TRAIL0` ... `COUNT3_TRAIL1`)
   เป็นค่าตั้งใจให้แยกแยะได้ทางไบต์ ไม่ใช่ค่าจริง · **ความหมายฟิลด์สามตัวในเรคคอร์ดและ trailing `u8` ไม่รู้จริง
   เช่นกัน** · `production_allowed=False` · `database_write=none` เสมอ

**สรุปตรงตามที่ `plg1ne` คาด**: ไม่มีช่องว่างแบบ "มีค่าแต่ไม่มีชื่ออ่าน" เหมือนที่ `skill_catalog.py` เคยมี —
ทั้งสามไฟล์เขียนครบเท่าที่ static เดินได้แล้ว ไม่มีอะไรผูกเพิ่มฝั่งคลาวด์ได้โดยไม่เดาความหมายฟิลด์ (ต้องห้าม
ตามกฎบ้าน)

## finding ใหม่ที่ไม่ได้ตามหา (ไม่ใช่เป้าของงานสำรองข้อ 1 แต่เจอระหว่างยืนยันตัวบล็อกเดิม)

เดินตรวจว่าตัวบล็อกเดิมของสองไฟล์ข้อ 2-3 (`GT-058`/`GT-059`/`GT-064` — ปิดหมดแล้วเพราะ "หน้าต่างสกิล K เปิด
ไม่ได้ใน baseline") ยังเป็นสถานะเดิมจริงไหมก่อนสรุป พบว่า **ไม่จริงแล้ว**:

- `GT-116` (`pf_bridge/GAME_TEST_QUEUE.md:5183`, ปิด PASS 2026-08-28T09:56+07:00) หลัง `CORE-REQUEST-022`
  ผูก `class_id=1`+`level=1` จริงเข้าเฟรม login แล้ว **หน้าต่างสกิลเปิดได้แล้ว** (มี 0 รายการ ตรงเกณฑ์ level 1
  = ปกติ)
- ใบเดียวกันเขียนกำกับตรง ๆ ว่า **"[ไม่อ้าง] ว่ารายการสกิลของ Gladiator ถูก — ยังไม่วัด (คนละเรื่อง)"** และ
  บรรทัด 5377 ของไฟล์เดียวกันย้ำอีกทีว่า "Does not test skill-window content correctness"
- `grep -n "skill window.*content\|skill list\|populate" GAME_TEST_QUEUE.md CLIENT_RE_QUEUE.md` (สองไฟล์
  ที่ยังไม่ archive ทั้งไฟล์) เจอบรรทัด 5377 นั้นเป็นจุดเดียวที่พูดเรื่องนี้ตรง ๆ — **ไม่มีใบ GT/RE เปิดอยู่ตอนนี้
  ที่ถามคำถาม "เนื้อในหน้าต่างสกิลตรงกับที่ควรมีไหม"**

พูดอีกแบบ: ตัวบล็อกที่ทำให้ `GT-058` (0x673C sweep) ปิดแบบตอบไม่ได้ (หน้าต่างเปิดไม่ได้) หลุดไปแล้วตั้งแต่
28 ส.ค. แต่ไม่มีใบไหนเดินคำถามเดิมต่อ — ส่งเฟรม `0x673C` ที่มีความหมายจริง (เช่น skill id ที่รู้ว่าตัวละครมี)
แล้วช่องในหน้าต่างขึ้นตรงไหม เป็นคำถามเดียวที่จะเปิดทางให้ `learn_skill_result_hypothesis.py` เลื่อนจาก
hypothesis เป็นโค้ดที่ทำงานจริง

**ไม่เปิดใบเองรอบนี้** — ส่งเป็นข้อเสนอในจดหมายให้ COO/chief ตัดสินและตั้งเลข (รูปแบบใบ GT ของบ้านนี้ยาวและ
chief คุมเลข/ถ้อยคำเสมอตามที่เห็นทุกจุดใน `NOW.md`)

## ส่งอะไร

**pirate-force-server**: **ไม่มีการเปลี่ยนแปลง** — รอบนี้เป็นรอบอ่าน+ตรวจสอบเอกสารล้วน ไม่แตะไฟล์โค้ด/เทสไฟล์
ใด ๆ (`git status`/`git diff` ว่างเปล่าตลอดรอบ ยังอยู่ที่ `origin/main` = `433fde4`)

**pf_bridge**:
- ไฟล์นี้ (แทน `rounds/CS_fv5xnu_claim.md`)
- `notes_to_chief/20260904_2113_LANE-CS-TO-COO-backup-item1-read-plus-gt116-reopens-skill-window-content-question.md`
- `.CONSUMED.txt` ของ `notes_to_chief/20260904_2046_COO-DECISION-gt243-enters-wait-for-your-machine-cs-holds-backup-LANE-CS.md`

## pf-adversary

**ไม่สั่ง** — รอบนี้ไม่มีโค้ด/เทส/ตรรกะใหม่เลย (อ่าน+เขียนจดหมาย/ไฟล์รอบเท่านั้น) ตรงข้อยกเว้นของ
`COO-DECISION 20260904_1428` ข้อ 2 ("รอบที่แก้ถ้อยคำอย่างเดียว = ไม่สั่ง adversary")

## nonclaims

- **ไม่อ้างว่า `GT-058`/`GT-059`/`GT-064` ผิด** — ปิดถูกต้องตามเงื่อนไข ณ ตอนนั้น (หน้าต่างเปิดไม่ได้จริง) แค่
  ตัวบล็อกนั้นหายไปแล้วหลัง `GT-116`
- **ไม่อ้างว่าเปิดใบใหม่แล้ว** — เป็นข้อเสนอในจดหมาย ไม่ใช่การแก้ `GAME_TEST_QUEUE.md`
- **ไม่แตะ `class_catalog.py`/`skill_catalog.py`/`damage_by_skill.py`** — `git diff --stat
  origin/main..HEAD` บนโคลนเซิร์ฟเวอร์ว่างเปล่า
- **ไม่เดาความหมายฟิลด์ใดใน HYP-PF-033/034** — รายงานตามที่ nonclaims ของสองโมดูลเขียนไว้เองเท่านั้น

## ติดอะไร / ใครปลด

- **`GT-243`** — รอผู้เทส (Panya) attended เหมือนเดิม ไม่บล็อกงานสำรอง
- **ข้อเสนอใบ GT ใหม่ (skill-window content)** — รอ COO/chief ตัดสินว่าคุ้มตั้งเลขไหม (จดหมายรอบนี้)
- **งานสำรองข้อ 2/3 ของ `plg1ne`** (อ่าน `skill_attr_hypothesis.py` 843 บรรทัด ให้จบ · เติม
  `n_EQUIPTYPE`/`n_EQUIPTYPE_LHAND` ถ้ามีเหตุผลใช้จริง) — ยังไม่ทำรอบนี้ ต่อรอบหน้า
