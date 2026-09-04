# DB round (`avc4ky`) -- 2026-09-04T13:05+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260904_1145_1szq3m_re229_close_and_piece4_scope_ask.md` รอบนั้นปิด `RE-229`
เป็น `BOUNDED-NEGATIVE` แล้วส่งจดหมายถาม COO สองเรื่อง (x=30 ปิดด้วยนโยบายได้ไหม + "นามแฝง"
หมายถึงอะไรจริง) ก่อนต้นรอบนี้ COO ตอบมาแล้วในใบ `20260904_1150` -- รอบนี้ทำตามทั้งสามข้อของใบนั้น

## NOW.md -- รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับ** -- ไม่มีสิทธิ์แก้ไฟล์นั้นเอง อ่านฉบับสดต้นรอบ (ตรวจล่าสุด COO 12:46) แล้ว: ไม่มี "งานด่วน
ตอนนี้" ข้อไหนเรียก LANE-DB โดยตรง (หัวข้อ `M4 · LANE-DB` บรรทัด `1101` ยัง "ล็อกต่อ" เหมือนเดิม
ตาม `0103`/`0847` -- ไม่ใช่คิวของรอบนี้ตาม `0329` ข้อ 1 ที่วาง PLAYER/CHARACTER ก่อน) ไม่มีบรรทัดไหนของ
NOW.md ที่รอบนี้ทำให้ต้องแก้

## 1. ล็อกรอบ

- 13:05+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า ⇒ ไม่มีใครต้องปลดล็อก ไม่ใช่ takeover
- กิ่งเซสชัน `claude/admiring-ride-avc4ky` ที่ระบบตั้งชื่อให้ชี้ตรง `origin/main` สด (`ac89e5c5`)
  พอดีอยู่แล้ว (0 ahead / 0 behind ตอนตรวจต้นรอบ) -- ไม่ต้อง reset
- commit `rounds/DB_20260904_1305_avc4ky_claim.md` push แล้วเปิด `pf_bridge#1137 [LANE-DB] round
  avc4ky: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1137` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ
- รอบนี้ไม่แตะ `pirate-force-server` เลย (งานเป็นเอกสาร/จดหมายล้วนฝั่ง `pf_bridge` เหมือนรอบก่อนหน้า) จึง
  ไม่มี PR ฝั่งเซิร์ฟเวอร์ให้เปิด -- เงื่อนไขปลดล็อก "PR ฝั่งเซิร์ฟเวอร์ทุกใบของรอบเปิดแล้วพร้อม marker"
  เป็นจริงโดยปริยาย (ศูนย์ใบ) จึงเติม `PF-AUTOMERGE: v4` ให้ `#1137` ได้ทันทีตอนจบรอบ (ดูข้อ 4)

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` บน `origin/main` สดของ `pf_bridge` ต้นรอบ หักใบที่มี `.CONSUMED.txt` คู่ ⇒
**หนึ่งใบใหม่**: `notes_to_chief/20260904_1150_COO-DECISION-lane-db-piece4-second-password-is-client-md5-
stored-opaque-alias-means-the-creation-screen-input.md` -- ตอบจดหมายที่ผมส่งไปรอบก่อน (`1145`) สามข้อ
เป็นงานของรอบนี้ทั้งหมด (ไม่มีจดหมายอื่นค้าง -- ตรวจ `notes_to_chief/consumed/` แล้วเป็นใบเก่าก่อน
convention stub ไม่ใช่ของค้าง)

สร้าง stub `.CONSUMED.txt` ให้ใบนี้แล้ว

## 3. ทำอะไร

### 3.1 ข้อ 1 ของ `1150` (x=30 second password storage) -- รับทราบ ปิดด้วยนโยบาย

COO ยืนยันการอ่านของรอบก่อนแล้วตรง ๆ ("การอ่านของคุณถูก ยืนยัน") ไม่มีโค้ดหรือจดหมายต้องทำเพิ่ม
บันทึกไว้ที่นี่ตามที่รอบก่อนวางแผน: **x=30 (`second_password_account_md5_upper_hex`,
`ActorAttr@0x148`) ปิดแล้ว (policy: preserve-only opaque, not RE)**

### 3.2 ข้อ 2 ของ `1150` (เฟรมขาเข้าของรหัสผ่านรอง) -- ค้น V110 corpus ก่อน แล้วส่งใบ RE แคบ

ค้นสามแหล่งตามที่สั่งก่อนเปิดใบ RE ใด ๆ (`AGENTS.md` G1 -- ค้นก่อนถอด):

1. `src/pirateforce_foundation/second_password_bypass.py` -- มีแค่เฟรม**ขาออก** (`make_proactive_
   second_password_ok()`, hash-pin แล้วทั้งคู่ `SECOND_PASSWORD_OK_PC_SHA256`/`_FRAME_SHA256`)
2. `src/pirateforce_foundation/runtime.py:9953-9998` -- caller เดียวที่มี ยิงเฟรขาออกแบบ proactive
   (runtime-ready + poll 2 วิ) ไม่มี handler รับเฟรมขาเข้าจากไคลเอนต์เลยในโมดูลนี้หรือที่อื่น
   (`grep -rn "second_password"` ทั้งสองรีโป ยกเว้น `current/pf_login_game_server_v141.py` ตามกฎบัตร
   -- ศูนย์ hit ของ incoming parser)
3. `docs/EXPERIMENT_LEDGER.md:20` (`SECOND-PASSWORD-BYPASS-001/002`) -- บันทึกตรง ๆ ว่า **"dialog-open
   emitted no distinct wire request"** และแพ็กเก็ตจริงตอน live session **"was not retained"** --
   ยืนยันว่าไม่เคย capture เฟรมขาเข้าเลย ไม่ใช่แค่ยังไม่ parse

**สรุป: corpus ไม่ครบ** -- ตอบได้แค่ครึ่งขาออก (ปิดแล้ว) ไม่ตอบคำถาม "เฟรมไหนตั้ง/เฟรมไหนตรวจ" เลย
ส่งใบ RE แคบตามข้อ 2 ของ `1150` สั่งให้ทำเมื่อ corpus ไม่ครบ:
`notes_to_chief/20260904_1309_LANE-DB-RE-TICKET-second-password-incoming-credential-frame.md`
(ถึง chief, cc COO -- ถามสองเส้นทาง: เฟรมตั้งรหัสผ่านรองครั้งแรก + เฟรมเปิดกระเป๋า/คลังจริง ไม่ผูก
deadline ใหม่ตาม `PANYA-DECISION 20260904_0233`)

### 3.3 ข้อ 3/4 ของ `1150` ("นามแฝง") -- ค้น TEXTDATA จริง พบ BOUNDED-NEGATIVE ปิดเองได้

ค้นหกตาราง CharCreate-scope ทั้งหมดที่มีในคลัง ด้วยคำ นามแฝง/นามปากกา/alias/nickname:
`gamedata/tables/CONSTDATA_TH__CHARCREATE_PACKAGE.tsv`, `CONSTDATA_TH__CHARCREATE_CLASS.tsv`,
`CONSTDATA_TH__CHARCREATE_LOOK.tsv`, `CONSTDATA_TH__CHARCREATE_SKIN.tsv`,
`TEXTDATA_TH__CHARCREATE_LOOK_TIP.tsv`, `TEXTDATA_TH__CHARCREATE_SKIN_TIP.tsv` -- **ศูนย์ hit ทั้งหก
ไฟล์** (`grep` exit code 1)

ขยายค้นทั้งคลัง `gamedata/tables/` เจอสตริง นามแฝง/นามปากกา จริงในสามไฟล์เท่านั้น:
`TEXTDATA_TH__UI_MESSAGE.tsv` แถว 1587-1606, `TEXTDATA_TH__MESSAGE.tsv` แถว 704-711/820-821,
`TEXTDATA_TH__COIN_CONSUME_TEXT.tsv` แถว 8 -- อ่านบริบทรอบ ๆ (`UI_MESSAGE.tsv` แถว 1575-1612) พบว่า
สตริงเหล่านี้อยู่ติดกับ "หาผู้เป็นเจ้าของจดหมายขวดแก้ว" / "จดหมายขวดแก้วของ $V1" / "นามแฝงสามารถทำให้
ท่านทำความรู้จักกับเพื่อนต่างเพศได้มากขึ้น" / "การเปลี่ยนนามแฝงจะต้องใช้จ่ายคุกกี้หรือ Token" -- ทั้งชุด
เป็นฟีเจอร์ "เพื่อนทางจดหมาย/ขวดแก้ว" (pen-pal social feature) ที่มีค่าใช้จ่ายเป็นสกุลเงินในเกม
**ไม่ใช่หน้าสร้างตัวละคร (CharCreate) เลย** -- คนละหน้าจอ คนละระบบกับ x=1 (`ชื่อตัวละคร`, ผูกแล้ว)

ปิดครึ่งนี้เป็น **`BOUNDED-NEGATIVE: no such input on CharCreate`** ตามที่ `1150` ข้อ 4 อนุญาตให้ทำได้
เองโดยไม่ต้องถามคุณ Panya (มีหลักฐานสตริงครบ) -- **ไม่เปิดใบ RE** สำหรับข้อนี้ (ไม่มี field เป้าหมาย
ให้ค้น byte จริง ๆ ถ้าเปิดใบจะเป็นการเดา field เป้าหมายแบบที่ `pf-adversary` เพิ่งแก้ให้ `RE-229`)

ส่งจดหมายรายงานรวมสามข้อถึง COO:
`notes_to_chief/20260904_1310_LANE-DB-REPORT-COO-piece4-alias-bounded-negative-mds5-frame-re-sent.md`

### 3.4 ตรวจสถานะ Door B / piece 3 ตามที่รอบก่อนทิ้งไว้ (ไม่ใช่การกระทำ แค่วัด)

- `pirate-force-server#723` (piece 3 gap report, รอบ `1cajqi`) -- **merged** (`531dc9d0`→main, 03:58 UTC)
- `pirate-force-server#717` (Door B recovery, LANE-B) -- **merged** (`f27005c0`→main, 01:55 UTC) --
  แต่ body ของ PR เขียนเองตรง ๆ ว่า "the caller is still not wired (that is the next round's work,
  and D6 should be answered first)" -- ยังไม่ปลดล็อก `1101` จริง ตาม NOW.md บรรทัด 49 ที่ยังเขียนว่า
  "ล็อกต่อ" -- ไม่ใช่ของ LANE-DB แก้ (caller เป็นของ LANE-B/chief) รอบนี้แค่วัด ไม่ได้ลงมือ

## 4. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- รอบนี้ไม่แตะไฟล์ `pirate-force-server` เลย (`git diff origin/main --stat` ยืนยัน: มีแค่สาม `.md`/
  `.CONSUMED.txt` ใหม่ในกิ่ง `pf_bridge` นี้) -- ไม่มีชุดเทสให้รันทั้ง targeted และ full ไม่ใช่การข้าม
  กติกา แต่เพราะไม่มีโค้ดให้เทส
- `pf_bridge#1137 [LANE-DB] round avc4ky: claim` -- เติม `PF-AUTOMERGE: v4` ทันทีหลัง push ไฟล์รอบนี้
  เพราะเงื่อนไข "PR ฝั่งเซิร์ฟเวอร์ทุกใบของรอบเปิดแล้วพร้อม marker" เป็นจริงโดยปริยาย (ศูนย์ใบฝั่ง
  `pirate-force-server` รอบนี้)
- ไม่มี PR ฝั่ง `pirate-force-server` รอบนี้

## 5. หลักฐาน -- สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ศูนย์** -- รอบนี้ไม่มีโค้ดเปลี่ยนในสองรีโปเลย เป็นงานปิดคิวถาม-ตอบ + จดหมายเท่านั้น ไม่เข้าคิว GT

### 5.2 wire-DB

🔴 **ศูนย์** -- ไม่มี migration ไม่มีแถวเขียน ไม่มี method ใหม่ใน `store.py`/`persistence_*.py`
เปลี่ยนแปลงเดียวคือเอกสาร: stub `.CONSUMED.txt` หนึ่งใบ + จดหมายสองฉบับใน `pf_bridge`

## 6. nonclaims

1. **ไม่อ้างว่าชิ้น 4/5 (นามแฝง+รหัสผ่านรอง) ปิดสนิท** -- ครึ่งเก็บ (x=30) ปิดแล้ว ครึ่ง "นามแฝง" ปิด
   ด้วย bounded-negative แล้ว แต่ครึ่ง "เฟรมขาเข้าของรหัสผ่านรอง" (ตั้ง/เปิดกระเป๋า) ยังเปิดรอ RE ที่
   เพิ่งส่งไปรอบนี้ -- ยังไม่มีผล
2. **ไม่อ้างว่า `1101` (HP/เลเวลถาวร, M4) ปลดล็อกแล้ว** -- แม้ `#717` (Door B) merge แล้ว caller ยัง
   ไม่ถูกเสียบตาม body ของ PR เอง ยังล็อกอยู่เหมือนเดิม ไม่ใช่คิวของรอบนี้ตาม `0329` ข้อ 1
3. **ไม่ได้ตัดสินเองว่าคำตอบของใบ RE ที่เพิ่งส่งจะเป็นอะไร** -- แค่ส่งคำถามแคบตามที่ corpus ยืนยันว่า
   ยังขาดจริง ไม่ได้เดาเฟรม/opcode ล่วงหน้า
4. **ไม่แตะ `second_password_bypass.py`, `runtime.py`, `app.py`, `gm/`, `migrations/`,
   `CLIENT_RE_QUEUE.md`** -- นอกเขตเขียนของ LANE-DB ทั้งหมด (การเปิดใบ RE ทำผ่านจดหมายถึง chief
   ตามวินัย "ขอ RE = ใบถึง chief" ไม่ใช่แก้ไฟล์คิวเอง)
5. **ไม่แตะชิ้น 2/5 (ค่าเกิดจากตาราง)** -- ยังบล็อกด้วย `RE-229` (method ceiling, ปิดแล้วรอบก่อน)
   เหมือนเดิม `DEFAULT_PRIMARY_STAT = 100` ยืนตาม `COO-DECISION 20260902_1607`
6. **ไม่ได้เปิด image/canonical DB/capture corpus** -- ทุกอาร์ติแฟกต์ที่อ้างถึง commit แล้วในสองรีโป

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. ตรวจว่า chief เปิด `RE-<เลขถัดไป>` จากใบ `20260904_1309_LANE-DB-RE-TICKET-second-password-
   incoming-credential-frame.md` หรือยัง -- ถ้าผลถึงแล้วให้อ่าน ใช้ แล้วปิดหัวใบเองพร้อม stub (ตาม
   กติกา "ใครเปิดใบคนนั้นบริโภค" ที่ `RE-229` วางไว้)
3. ตรวจว่า COO ตอบใบ `20260904_1310_LANE-DB-REPORT-COO-...` หรือไม่ -- ถ้าเห็นแย้งกับการปิด
   bounded-negative ของ "นามแฝง" ให้แก้ตาม
4. ตรวจ Door B caller อีกครั้ง (`1101`/M4) -- ยังไม่ใช่คิวของรอบนี้ตาม `0329` ข้อ 1 แต่เป็นตัวปลดล็อก
   M4 ที่ LANE-DB รอ caller อยู่ (ของ LANE-B/chief ไม่ใช่ของ DB แก้)
5. ถ้าไม่มีจดหมายใหม่และ RE ที่ส่งไปยังไม่มีผล -- PLAYER/CHARACTER ทั้ง 5 ชิ้นอยู่ในสถานะ: ชิ้น 1✅
   ชิ้น 2 บล็อก(RE-229 ceiling) ชิ้น 3 บล็อก(compose_full_block ยังรอ RESEND_ADJUDICATED) ชิ้น 4
   ครึ่งเก็บ✅/ครึ่งเฟรมรอ RE ชิ้น 5✅ -- DB ว่างได้ ไม่หาเรื่องทำ (NOW.md บรรทัด 49)
