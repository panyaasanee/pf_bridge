# DB round (`f9p5fw`) -- 2026-09-04T14:34+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260904_1310_avc4ky_re229_answer_and_piece4_alias_bounded_negative.md`
รอบนั้นปิดครึ่ง "นามแฝง" ของชิ้น 4 ด้วย bounded-negative และส่งใบ RE-TICKET เรื่องเฟรมขาเข้ารหัสผ่านรอง
ระหว่างรอบนั้นกับรอบนี้ COO ตอบ (`1347`) และ chief จองเลขคิว (`1409`, RE-239) -- รอบนี้ประมวลผลทั้งสองใบ

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับ** -- อ่านฉบับสด (ตรวจล่าสุด COO 14:31) ต้นรอบแล้ว: หัวข้อ "งานด่วนตอนนี้" ไม่มีข้อไหนเรียก
LANE-DB โดยตรง `M4 · LANE-DB` (บรรทัด 49) ยังเขียนว่า `1101` HP/เลเวลถาวร **ล็อกต่อ** เหมือนเดิม
(`runtime.py:6443` ยังไม่ส่ง `store=` -- ของ chief/LANE-B ไม่ใช่ของ DB แก้) ไม่มีบรรทัดไหนของ NOW.md
ที่รอบนี้มีสิทธิ์หรือมีเหตุต้องแก้ ไม่มีสิทธิ์แก้ไฟล์นั้นเองอยู่แล้วตามกติกา

## 1. ล็อกรอบ

- 14:34+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า ⇒ ไม่มีใครต้องปลดล็อก ไม่ใช่ takeover
- กิ่งเซสชัน `claude/admiring-johnson-f9p5fw` ที่ระบบตั้งชื่อให้ fast-forward จาก `origin/main` สด
  (`c2604dcd`→`f902dfe6`) แล้วชี้ตรง 0 ahead/0 behind ก่อนเริ่ม
- commit `rounds/DB_20260904_1434_f9p5fw_claim.md` push แล้วเปิด `pf_bridge#1151 [LANE-DB] round
  f9p5fw: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1151` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ
- `pirate-force-server` มี PR อื่นเปิดอยู่ (`#737` LANE-A, `#738` LANE-B) แต่ไม่ใช่ `[LANE-DB]` จึงไม่ใช่
  ล็อกของสายนี้ ไม่แตะ

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` บน `origin/main` สดของ `pf_bridge` ต้นรอบ หักใบที่มี `.CONSUMED.txt` คู่ ⇒
**สองใบใหม่**:

1. `notes_to_chief/20260904_1347_COO-DECISION-lane-db-1310-piece4-closed-except-incoming-credential-frame-accepted-no-new-deadline-back-to-normal-queue.md`
   -- ตอบจดหมาย `1310` ของรอบก่อน สั่งสี่ข้อสำหรับรอบ 14:31 นี้ (ดู §3.1)
2. `notes_to_chief/20260904_1409_CHIEF-TO-LANE-DB-your-second-password-frame-ticket-is-re239.md`
   -- chief จองคิว `RE-239` ให้ใบ `1309` แล้ว แต่บอกให้ LANE-DB ติดป้าย route เอง (ดู §3.2)

สร้าง stub `.CONSUMED.txt` ให้ทั้งสองใบแล้ว ไม่มีจดหมายอื่นค้าง

## 3. ทำอะไร

### 3.1 ข้อ 4 ของ `1347` -- สามอนุข้อ

**(ก) ตรวจว่าชิ้น 3 (`#723`) อยู่บน main จริง** -- `git fetch origin main` แล้ว
`git merge-base --is-ancestor 531dc9d0 origin/main` บนโคลนที่ fetch สดของ `pirate-force-server` ⇒
**YES** (`531dc9d0` เป็นบรรพบุรุษของ `origin/main` ที่หัว `4d4f879a`/PR #736 ตอนนี้จริง) ชิ้น 3 (บล็อก
`0x309A` เต็มจากแถว typed) ยืนยันอยู่บน main แล้วด้วยกติกาวัด `git merge-base --is-ancestor` ตามที่
`AGENTS.md` §7 ข้อ 3 กำหนด ไม่ใช่แค่คำบอกเล่าของรอบก่อน

อ่าน `src/pirateforce_foundation/persistence_attr_compose.py` (มีอยู่บน main จริงตามที่ตรวจ) ยืนยัน
สถานะที่รอบก่อนสรุปไว้ยังตรง: `RESEND_ADJUDICATED: frozenset[int] = frozenset()` (บรรทัด 420) ยังว่าง
โดยตั้งใจ -- docstring "RESEND ADJUDICATION" (บรรทัด 95-111) อธิบายว่าการแยก construction-default ที่
เป็น codec write ออกจาก gameplay write เป็น **คำถาม RE ที่สายนี้ตอบจากคลังเองไม่ได้** ไม่ใช่ของที่ DB
ตัดสินเองได้โดยเลือกเลขที่ "ดูโอเค" ⇒ ชิ้น 3 ยัง blocked ด้วยเหตุผลเดิม ไม่ใช่การถดถอย และไม่ใช่งานที่
DB ต้องลงมือ (เป็นใบ RE ที่ต้องส่งผ่าน chief ถ้าจะเปิด ยังไม่มีใครเปิด)

**(ข) กลับคิว M4 · LANE-DB ตาม NOW.md** -- อ่านฉบับสด (14:31 ต้นรอบ): `1101` (HP/เลเวลถาวร) ยัง
"ล็อกต่อ" เหมือนที่ `0103`/`0847` วัดไว้ (`runtime.py:6443` ไม่ส่ง `store=`) -- ประตูของบนพื้น
(`commit_ground_drop`/`list_ground_drops_for_scene`) อยู่บน main แล้ว (`#680`) แต่นั่นเป็นคนละเรื่องกับ
caller ของ HP/level ที่ยังไม่เสียบ ไม่มีอะไรเปลี่ยนจากรอบก่อนที่ DB มีสิทธิ์แก้ (caller เป็นของ LANE-B/chief)

**(ค) ว่างได้ ไม่หาเรื่องทำ** -- ตรวจครบทั้งห้าชิ้นของ PLAYER/CHARACTER (`0329`) ต้นรอบนี้:
ชิ้น 1 ✅ (`#699`/`#705` บน main) · ชิ้น 2 บล็อก (RE-229 ceiling, DEFAULT 100 ยืน) · ชิ้น 3 บล็อก
(RESEND_ADJUDICATED ว่างโดยตั้งใจ, ยืนยันซ้ำข้างบน) · ชิ้น 4 ครึ่งเก็บ✅/ครึ่งเฟรมรอ RE-239 (routed
รอบนี้ ดู §3.2) · ชิ้น 5 ✅ (`#707` บน main) -- **ไม่มีชิ้นไหนที่ DB มีสิทธิ์และมีเหตุลงมือแก้โค้ดรอบนี้**
รอบนี้จึงไม่แตะ `pirate-force-server` เลย ตรงตามที่ `1347` ข้อ 4(ค) และ NOW.md บรรทัด 49 อนุญาต

### 3.2 ข้อ 1409 -- ติดป้าย route ให้ RE-239

`CLIENT_RE_QUEUE.md` เป็นเขตของ chief (ห้ามแก้เอง) จึงตอบด้วยจดหมายแทนการแก้ไฟล์คิวตรง ๆ:
`notes_to_chief/20260904_1434_LANE-DB-REPLY-chief-re239-route-needs-attended-capture.md` --
สรุปเหตุผล: ใบ `1309` ต้นทางของ RE-239 ค้นครบสามแหล่งบนดิสก์แล้วพบว่า **ไม่เคย capture เฟรมขาเข้าเลย
สักครั้ง** (`docs/EXPERIMENT_LEDGER.md:20`: "dialog-open emitted no distinct wire request" +
"packet ... was not retained") ไม่ใช่แค่ "มีแต่ยังไม่ parse" ⇒ ป้ายที่ถูกต้องคือ
`NEEDS-ATTENDED-CAPTURE` ไม่ใช่ `STATIC-ON-BRIDGE`/`STATIC-ON-CLOUD` (สองป้ายหลังต้องมีเฟรมอยู่ในคลัง
ให้ขุด ซึ่งกรณีนี้ไม่มี) chief เป็นผู้แก้ `CLIENT_RE_QUEUE.md` เองตามใบนี้

## 4. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- รอบนี้ไม่แตะไฟล์ `pirate-force-server` เลย (`git diff origin/main --stat` บนกิ่งนี้ยืนยัน: มีแค่ไฟล์
  `.md`/`.CONSUMED.txt` ใหม่ในกิ่ง `pf_bridge`) -- ไม่มีชุดเทสให้รันทั้ง targeted และ full เพราะไม่มีโค้ด
  ให้เทส ไม่ใช่การข้ามกติกา
- `pf_bridge#1151 [LANE-DB] round f9p5fw: claim` -- เติม `PF-AUTOMERGE: v4` ทันทีหลัง push ไฟล์รอบนี้
  เพราะเงื่อนไข "PR ฝั่งเซิร์ฟเวอร์ทุกใบของรอบเปิดแล้วพร้อม marker" เป็นจริงโดยปริยาย (ศูนย์ใบฝั่ง
  `pirate-force-server` รอบนี้)
- ไม่มี PR ฝั่ง `pirate-force-server` รอบนี้

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ศูนย์** -- ไม่มีโค้ดเปลี่ยนในสองรีโปเลยรอบนี้ ไม่มีอะไรให้ผู้เล่นเห็นต่างจากเมื่อวาน ไม่เข้าคิว GT

### 5.2 wire-DB

🔴 **ศูนย์การเขียน** -- ไม่มี migration ไม่มีแถวเขียน ไม่มี method ใหม่ใน `store.py`/`persistence_*.py`
สิ่งที่ได้จริงรอบนี้คือ**การวัด** (piece 3 ancestor check ด้วย `git merge-base --is-ancestor` บนโคลนที่
fetch สด) + เอกสาร (สอง stub `.CONSUMED.txt` + จดหมายตอบ chief หนึ่งฉบับ)

## 6. nonclaims

1. **ไม่อ้างว่าชิ้น 3 (`0x309A` full block) พร้อมส่งจริง** -- `#723` อยู่บน main จริง (ยืนยันด้วย
   ancestor check) แต่ `compose_full_block` ยังคืนบล็อกเต็มไม่ได้เพราะ `RESEND_ADJUDICATED` ว่างโดย
   ตั้งใจ (คำถาม RE ที่ไม่มีใครเปิดใบ)
2. **ไม่อ้างว่า `1101` (HP/เลเวลถาวร, M4) ปลดล็อกแล้ว** -- ไม่มีอะไรเปลี่ยนจากรอบก่อน caller ยังไม่เสียบ
3. **ไม่ได้ตัดสินป้าย route ของ RE-239 เอง** -- ส่งเป็นข้อเสนอทางจดหมายให้ chief เป็นผู้แก้
   `CLIENT_RE_QUEUE.md` ตามเขตเขียน ไม่ได้แก้ไฟล์นั้นตรง ๆ
4. **ไม่แตะ `runtime.py`, `app.py`, `gm/`, `migrations/`, `CLIENT_RE_QUEUE.md`, `store.py`,
   `persistence_attr_compose.py`** -- นอกเขตเขียนหรือไม่มีเหตุแก้รอบนี้ (อ่านอย่างเดียว)
5. **ไม่แตะชิ้น 2/5 (ค่าเกิดจากตาราง)** -- ยังบล็อกด้วย `RE-229` (ปิดแล้วรอบก่อน) เหมือนเดิม
6. **ไม่ได้เปิด image/canonical DB/capture corpus** -- ทุกอาร์ติแฟกต์ที่อ้างถึง commit แล้วในสองรีโป
7. **ไม่ได้เปิดใบ RE ใหม่ใด ๆ รอบนี้** -- แค่ตอบป้าย route ของใบที่มีอยู่แล้ว (RE-239)

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. ตรวจว่า chief แก้ `CLIENT_RE_QUEUE.md` ติดป้าย `NEEDS-ATTENDED-CAPTURE` ให้ `RE-239` ตามจดหมายรอบนี้
   หรือยัง -- ถ้ายัง ไม่ใช่เหตุทวง (ไม่มีกำหนด) แค่บันทึกสถานะ
3. ตรวจ Door B caller อีกครั้ง (`1101`/M4) -- ยังไม่ใช่คิวของ DB แก้ (ของ LANE-B/chief) แค่วัดว่าขยับหรือยัง
4. ถ้าไม่มีจดหมายใหม่และไม่มี RE ตอบกลับ -- PLAYER/CHARACTER ยืนที่: ชิ้น 1✅ ชิ้น 2 บล็อก(RE-229)
   ชิ้น 3 บล็อก(RESEND_ADJUDICATED ว่าง, ไม่มีใบ RE เปิด) ชิ้น 4 ครึ่งเก็บ✅/ครึ่งเฟรมรอ RE-239(attended)
   ชิ้น 5✅ -- DB ว่างได้ ไม่หาเรื่องทำ (NOW.md บรรทัด 49)
