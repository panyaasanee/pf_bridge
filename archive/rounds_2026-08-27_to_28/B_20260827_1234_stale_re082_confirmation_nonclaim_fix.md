# round `B_20260827_1234` (`w0ia0f`) · lane B · COMBAT -- fresh re-verify of
BUILD-004/005/006 against everything since the `urlmag` merge, plus one real
(small) fix: `mob_pickup.py` NONCLAIM 2 was still saying "awaiting COO/RE
confirmation" a day after RE-082 answered it PASS/DONE

**opened:** 2026-08-27 ~12:00 (+07:00) · **closed:** 2026-08-27 ~12:34 (+07:00)
**branches:** `claude/trusting-curie-w0ia0f` (pirate-force-server) ·
`claude/lucid-hamilton-w0ia0f` (pf_bridge)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** **ไม่มีอะไรต่างจากเมื่อวานในเกม** รอบนี้ไม่แตะ
`runtime.py`/`app.py` และไม่เปลี่ยนพฤติกรรมของ `resolve_claim`/`place_in_bag`/
`commit_pickup` เลยสักบรรทัด -- สถานะที่ผู้เล่นเห็นได้จริงยังเหมือนรอบก่อนหน้าทุกประการ
(มอนสเตอร์แดง 13 ตัวจากตาราง MOBS จริงในสนาม, ตี/เลือดลด/ตายที่ `0x201F` ได้, ของหล่น/
เก็บครึ่งแรกทำงาน, ครึ่งหลังของการเก็บ -- ธุรกรรมจริงที่เอาของจากพื้นใส่กระเป๋า -- ยังไม่มีจุด
เรียกเลย เหมือนทุกรอบก่อนหน้า) สิ่งที่รอบนี้แก้คือ **เอกสารในโค้ดของสายนี้เอง** ที่ยังบอกว่า
คำถามหนึ่งข้อ "ยังไม่ได้รับการยืนยัน" ทั้งที่มันถูกยืนยันไปแล้วจริงตั้งแต่วันก่อน -- ไม่ใช่งานที่
เข้าข่าย "lane-A/B change" ตามกฎข้อ 3 ของกฎบัตร (ผู้เล่นไม่เห็นอะไรเปลี่ยน) แต่เป็นการปิด
ช่องว่างประเภทเดียวกับที่กฎบัตรฉบับนี้เขียนเตือนไว้เป็นตัวอย่าง (๐ scenarios production
allowed) -- diagnosis เก่าที่ไม่ถูก re-derive ถูกปล่อยให้ยืนอยู่เฉยๆ

## 1 อ่านทุกอย่างที่เปลี่ยนตั้งแต่ PR #189/#112 (`urlmag`, merged 05:06 UTC)

`git log 9f43276..HEAD` ทั้งสอง repo: มีแค่งานของสาย GM (`nzt815`, แก้
`warp_executor.py` args-shape) กับจดหมายจาก Panya หนึ่งฉบับ
(`20260827_1240_PANYA-EVIDENCE-video2-Port-Royal-...md`, คลิปเดินชม Port
Royal ยืนยัน NPC 30+ ตัว) -- **ฉบับนั้นส่งถึงสาย A เป็นหลัก** (roster เมือง =
`world_*.json`, ไม่ใช่เขตเขียนของสายนี้) มี cc สาย B แต่ไม่มีข้อไหนที่สายนี้ต้องทำ
ต่อโดยตรง (รวมถึงบรรทัดที่บอกว่า Training Iron Man 916 มีตำแหน่งจริงในเมือง -- นั่น
คืองาน placement ของสาย A ไม่ใช่ของสายนี้)

ไล่ต่อประวัติก่อนหน้านั้นที่ยังไม่เคยอ่านสดในรอบนี้ (merge ผ่าน sync commit คนละสาย
ก่อน `urlmag` แต่ ancestor ของ HEAD แล้ว) พบจดหมายชุด CHIEF-REPLY สองฉบับ
(`1330`, `1700`) ที่ตรวจบอร์ด **`WIRED v2` ครบ 10 เลนของทั้งโปรเจกต์** -- ของสายนี้ 3
เลนที่ค้าง: `combat_loot` (🟡 -> ✅ ปิดแล้วจริงใน `dfa61ac`, มี console token
`MOB_LOOT_DROPS_CENSUS` แล้ว, ยืนยันสดด้วย `grep` ใน `runtime.py:4167`),
`combat_aggro` (❌ **ตั้งใจ** ตาม `COO-DECISION 20260826_0402`: ยกเป็น
production พร้อมกับตัวการตายครึ่งหลังแล้วจริง (`production_allowed=True`,
import edge ที่ `mob_ai_control.py` สแกนเห็นได้) แต่ tick loop dispatch (จุด
เรียกใน `runtime.py`) ยังไม่ครบตามกำหนด `BUILD-005` 29 ส.ค. -- **ยังไม่เลยเส้นตาย**
ไม่ใช่ของค้าง), `combat_pickup` (❌ THE WALL ตามที่ `mob_pickup.py` บันทึกเอง --
มีแค่ bag-claim bookkeeping รันจริง ไม่มี inbound dispatch จริง)

## 2 ตามหาพื้นที่สร้างใหม่จริงในเขตของสายนี้ -- ไล่ทีละเลน

- **`combat_aggro` dispatch** -- ต้องแตะ `runtime.py` (chief's file), ต้องมี game
  tick loop จริงที่ป้อนตำแหน่งผู้เล่นสด -- ใหญ่กว่า "บรรทัดเดียว" และยังไม่ถึงเส้นตาย
  BUILD-005 -- ไม่ใช่ของรอบนี้
- **`combat_pickup` dispatch** -- `mob_pickup.py`'s THE WALL บอกไว้ตรงๆ ว่ารอ
  RE ยืนยัน real vital id ก่อน (opcode `0x4543` ยัง DERIVED/NOT_OBSERVED per
  GT-046) ผ่าน `GT-060` (attended, ยัง **BLOCKED-CONDITIONAL** ใน
  `GAME_TEST_QUEUE.md` -- เงื่อนไข (ข) รอโมเดลให้คลิกได้จริง) ไม่ใช่ของสายนี้แก้เอง
  ได้โดยไม่มี attended capture
- **`mob_ai_control.reconcile()` vs real `DeathRegister`** -- รอบก่อน (`urlmag`)
  ปิดช่องนี้ไปแล้วสำหรับ `0x201F` -- ตรวจว่ามีช่องคล้ายกันเหลือสำหรับ `916`
  (widened=) ไหม: **ไม่มี** เพราะ `mob_ai_control`'s AI register สร้างจาก
  `field_mobs.load_roster()` (มอนสนาม 13 ตัว) ล้วน ไม่มี `916` (NPC ในเมือง) อยู่
  ในนั้นเลย -- reconcile กับ 916 จะไม่มีความหมายจนกว่า roster ที่ track จริงจะรวม 916
  เข้ามา (งานของสาย A/chief ไม่ใช่ของสายนี้) `is_tracked()` guard ที่มีอยู่แล้วก็ fail
  closed ถูกต้องสำหรับกรณีนี้ (เช็คโค้ดจริงที่ `runtime.py:3976` แล้ว)
- **`mob_combat.strike()`** -- ไม่มี scope gate แบบเดียวกับ `mob_death.kill()`
  เลย (grep แล้ว, ไม่มี `widened`/`SANCTIONED` ใน `mob_combat.py`) ตามที่ตั้งใจไว้
  ตั้งแต่แรก (ตี/เลือดลดเปิดทั้ง 13 ตัวอยู่แล้ว มีแค่ *ตาย* ที่ยังจำกัดขอบเขต) -- ไม่มีช่องโหว่
- **GT-060/GT-069 (BUILD-006 ที่เกี่ยวกับการเก็บของ)** -- ทั้งคู่ blocked บนคำเคาะเจ้าของ
  /attended ไม่ใช่ของสายนี้แก้ได้จากโค้ด

**สรุป:** ไม่พบพื้นที่สร้างใหม่ที่เปลี่ยนพฤติกรรมเกมได้อย่างปลอดภัยรอบนี้ -- ทุกอย่างที่เหลือ
ถูก gate ไว้จริง (chief's runtime.py + game-tick สำหรับ aggro, attended capture
สำหรับ pickup/GT-060/GT-069, roster ของสาย A สำหรับ 916) ตรงกับรูปแบบของรอบ
ก่อนหน้าหลายรอบ (`0345`, `1300`, `2153` ฯลฯ)

## 3 สิ่งที่พบและแก้จริง -- `mob_pickup.py` NONCLAIM 2 ยกตัวอย่างข้อบกพร่องแบบเดียว
กับที่กฎบัตรฉบับนี้เตือนไว้เป๊ะ

ระหว่างไล่อ่าน `mob_pickup.py` เพื่อยืนยันว่า THE WALL ยังถูกต้อง พบว่า NONCLAIM 2
("THE OBJECT REFERENCE IS AN ASSUMPTION") ยังเขียนว่า `[LANE-B ASSUMPTION -
awaiting COO/RE confirmation]` -- แต่ `notes_to_chief/20260826_1017_RE-082-
RESULT-OBJECT-REF-IS-ELEMENT-KEY.md` (RE runner, PASS/DONE, static-only)
**ตอบคำถามนี้ไปแล้วตั้งแต่ 2026-08-26 10:17+07:00**: dword ที่คลิกซ้ายก๊อปจาก
`[drop-object+0x10]` **คือ** wire element key เดียวกับที่ `resolve_claim` เทียบ
ไม่มี transform/hash/index คั่นกลาง (`BUILD_IMPACT` ของใบผลเขียนไว้ตรงๆ ว่า
"MOB-PICKUP-001 สมมติฐานถูกยืนยัน") หนึ่งวันเต็มผ่านไปโดยที่โค้ดของสายนี้เองยังไม่รู้ตัว

นี่คือของแบบเดียวกับที่กฎบัตรของรอบนี้เขียนเตือนไว้เป็นตัวอย่างเปิดเรื่อง (`0`
scenarios production_allowed ไม่ใช่การวินิจฉัย แต่เป็นสิ่งที่ schema บังคับ) -- diagnosis
ที่เคยจริงแต่ไม่ถูก re-derive แล้วถูกปล่อยยืนเป็นข้อเท็จจริงต่อไป ต่างกันแค่ทิศทาง (ที่นี่คือ
"ยังไม่ยืนยัน" ทั้งที่ยืนยันแล้ว แทนที่จะเป็น "ยืนยันแล้ว" ทั้งที่ไม่จริง) แต่รูปแบบเดียวกัน

### แก้อะไรบ้าง (`pirate-force-server@9dc5519`)

- `src/pirateforce_foundation/mob_pickup.py`: docstring NONCLAIM 2 +
  ย่อหน้า WHAT-IS-PROVEN + ค่าคงที่ `MOB_PICKUP_NONCLAIMS[1]` เปลี่ยนจาก
  "awaiting" เป็น "CONFIRMED by RE-082, 2026-08-26 10:17+07:00, PASS/DONE" พร้อม
  ระบุชัดว่า **ยืนยันนี้ไม่ยกเพดานอะไรเพิ่ม** (static-only, image sha เดียว, ไม่มี
  runtime transaction ไหนรันจริง, การ์ด "RESOLVES ไม่ TRUSTS" ใน `resolve_claim`
  ยังคงอยู่เหมือนเดิมเป็น defense-in-depth ไม่ใช่เพราะยังไม่มั่นใจ) -- แก้ commentary
  ใกล้เคียงอีก 2 จุด (`REFUSE_DROP_ALREADY_TAKEN` block, `resolve_claim`'s
  docstring) ที่พูดถึง RE-082 แบบ present-tense ราวกับเป็นการทดลองที่ยังเปิดอยู่ ให้
  เป็น past-tense ที่ปิดแล้ว -- **ไม่แตะข้อความ `raise` จริงที่เทสจับคู่กันอยู่เลย**
- `scenarios/combat_pickup_001.json`: regenerate จาก `pin_document()` ให้ตรง
  กับ nonclaim ที่แก้ (diff 1 บรรทัด เหมือนเดิมทุกฟิลด์อื่น)
- `tests/test_mob_pickup.py`: เทสใหม่ 1 ตัว
  (`test_the_object_reference_nonclaim_reports_re_082_as_closed`) ปักหมุด
  คำว่า "CONFIRMED" + วันที่ RE-082 ไว้ทั้งในค่าคงที่และ docstring พร้อมยืนยันว่า
  "RESOLVED against the" (การ์ดจริง) ยังอยู่ -- กันไม่ให้ใครเผลอเขียน "awaiting" กลับ
  มาแบบเงียบๆ อีก

### สิ่งที่**ไม่ได้แก้** เพราะไม่มั่นใจพอ -- ตั้งใจไม่แตะ ไม่ใช่ลืม

NONCLAIM 1 (docstring บรรทัด ~88, ค่าคงที่บรรทัด ~378) เขียนว่า "...stays
unwired pending **RE-082's vital id**" -- อ่าน `RE-082` result letter ทั้งฉบับแล้ว
**ไม่มีคำว่า "vital"/"opcode" อยู่เลยสักคำ** RE-082 ตอบแค่คำถาม object-ref-is-key
(NONCLAIM 2) เท่านั้น ไม่เกี่ยวกับ opcode ขาเข้าที่ยังไม่ยืนยัน (`0x4543`
DERIVED/NOT_OBSERVED ตาม GT-046, รอ `GT-060` attended capture) ดูเหมือนเป็น
misattribution เดิมในไฟล์ (ผูกเลขใบผิดใบ) แต่ **ไม่แก้รอบนี้** เพราะไม่มั่นใจพอว่าเลขใบที่
"ควรจะ" อยู่ตรงนั้นคือใบไหนแน่ (`GT-060`? หรือใบ RE ที่ยังไม่เปิด?) แก้ผิดจะกลายเป็นสร้าง
ความสับสนใหม่แทนที่จะแก้ของเดิม -- ทิ้งไว้เป็นข้อสังเกตให้ chief/COO เห็น (§5)

## 4 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | `python3 -m unittest tests.test_mob_pickup`: 66/66 (เพิ่ม 1 จาก 65 เดิม) · สวีตเต็มอิสระ: **3487 เทส**, error 18 ตัวเดิม (capstone, environment เท่านั้น), skip 212, **0 FAIL ใหม่** (เพิ่มจาก baseline 3486 ด้วยเทสใหม่ 1 ตัวพอดี) · `grep MOB_LOOT_DROPS_CENSUS runtime.py` ยืนยันสดว่า combat_loot ได้ console token จริงแล้ว (`runtime.py:4167`) · `grep widened mob_combat.py` ยืนยันสดว่าไม่มี scope gate · cp874-encodability เช็คตรงด้วยสคริปต์ (`.encode('cp874')`) ทั้งไฟล์ `.py` ที่แก้และ `.json` ที่ regenerate แล้ว ผ่านทั้งคู่ |
| **client-observable** | ไม่มี -- รอบนี้ไม่ใช่รอบ attended, ไม่มีการเปลี่ยนพฤติกรรมให้สังเกต |

## 5 ข้อสังเกตนอกเขต -- ไม่แก้เอง ส่งให้ chief/COO เห็น

`mob_pickup.py` NONCLAIM 1 อ้าง "pending RE-082's vital id" แต่ RE-082's ผลจริง
ไม่เกี่ยวกับ vital id เลย (ดู §3 ท้ายย่อหน้า) -- น่าจะเป็นเลขใบเดิมที่ผูกผิด (ตั้งแต่ก่อนรอบนี้)
เสนอให้ chief/COO ยืนยันว่าเลขใบที่ถูกต้องคือใบไหน (หรือว่าควรเป็นข้อความทั่วไปไม่ผูก
เลขใบเลย) แล้วสายนี้จะแก้ตามในรอบถัดไป -- **ไม่ใช่ CORE-REQUEST** (ไม่ต้องแตะ
`runtime.py`) แค่คำถามเอกสาร

## 6 ถ้าผิดต้องย้อนอะไรบ้าง

หนึ่งคอมมิตใน `pirate-force-server` (`9dc5519`) แตะสามไฟล์
(`mob_pickup.py`, `combat_pickup_001.json`, `test_mob_pickup.py`) -- ย้อนได้
ทันทีด้วย `git revert 9dc5519` ไม่กระทบ production path ใดๆ เพราะไม่มีบรรทัด
พฤติกรรมเปลี่ยนเลย เป็นเอกสาร + เทสปักหมุดล้วน

## 7 `pf-adversary` -- self-review ก่อน commit

ลองหาทางพัง: (ก) grep หา `assertIn`/`assertNotIn("RE-082"` ใน
`test_mob_pickup.py` ก่อนแก้ ยืนยันว่าไม่มีเทสไหนจับคู่กับข้อความ docstring ที่กำลังจะ
แก้ (เทสจับคู่กับข้อความใน exception `raise` จริง ซึ่งไม่ถูกแตะ) (ข) นับ
`"[LANE-B ASSUMPTION"` ก่อน/หลังแก้ -- ก่อน 4 หลัง 4 (ไม่ลดต่ำกว่า 3 ที่เทสเดิมบังคับ)
(ค) รันเทสไฟล์เดี่ยวก่อนจะ regenerate pin -- เจอ `FAIL` จริง 1 ตัว
(`test_the_shipped_pin_file_is_what_the_code_computes`) เพราะลืม regenerate
`combat_pickup_001.json` ก่อน -- นี่คือของจริงที่ pf-adversary-style pass จับได้ ไม่ใช่
สมมติ -- แก้แล้ว (§3) รันซ้ำเขียว (ง) เช็ค cp874-encodability ตรงด้วยสคริปต์ ไม่ใช่
เดาจากสายตา (จ) พยายามหา call site อื่นที่อาจอ่าน `MOB_PICKUP_NONCLAIMS` แบบ
exact-string-match (นอกเหนือจากเทสที่เห็นแล้ว) -- grep ทั้ง repo หา
`MOB_PICKUP_NONCLAIMS` -- พบแค่ในเทสกับในโมดูลเอง ไม่มีที่อื่น

## 8 รอบถัดไปควรทำอะไร

1. เช็คซ้ำว่า chief ต่อสาย `combat_aggro` tick loop เข้า `runtime.py` หรือยัง
   (เส้นตาย `BUILD-005` 29 ส.ค. 23:59 -- ยังไม่เลย) ถ้าต่อแล้วต้องตรวจว่า game-tick
   loop จริงป้อนตำแหน่งผู้เล่นให้ `tick_step` ได้จริงไหม ไม่ใช่แค่ import edge
2. เช็คสถานะ `GT-060` (BLOCKED-CONDITIONAL) -- ถ้าเงื่อนไข (ข) หลุดแล้ว (มี
   drop-object คลิกได้จริง) นั่นคือทางเข้าสำหรับ `combat_pickup` dispatch (THE
   WALL) ที่แท้จริง
3. ถ้า chief/COO ตอบ §5 (เลขใบที่ถูกต้องของ NONCLAIM 1) มา -- แก้ตามในรอบถัดไป
4. ยังไม่มีอะไรใหม่ให้ attended tester กดทดสอบรอบนี้ (เหมือนหลายรอบก่อนหน้า)

-- **สาย B · COMBAT**
