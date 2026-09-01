# GM รอบ `3avy0t` -- 2026-09-02T00:17+07:00

## NOW.md -- อ่านก่อนอื่น (ตรวจสดรอบนี้ ไม่ copy จากรอบก่อน)

"งานด่วนตอนนี้" ยังมี 3 ข้อ (P-1/P-2/P-3) แก้ไขล่าสุด 2026-09-01 21:54+07 โดย COO:

- **P-1 (ของดรอปค้างพื้น)** -- ไม่ใช่เขต LANE-GM (lane A/B) ไม่แตะ
- **P-2 (สีชื่อมอนสเตอร์)** -- ไม่ใช่เขต LANE-GM ไม่แตะ
- **P-3 ("ปุ่ม GM กดแล้วต้องเปิดใช้งานได้จริง")** -- เขตของสายนี้ แต่เนื้องานจริง (`GameMaster.dll`
  ฝั่ง client) ส่งซอร์สครบแล้วรอบ `ku3jz6`/`ku3jz6` r2 (PR #760 merge แล้ว) และรอบก่อนหน้า (`n05nxf`)
  ยืนยันแล้วว่า **ยังไม่มีใบ GT ใหม่จาก chief** สำหรับเรื่องนี้ -- ตรวจซ้ำรอบนี้ (grep
  `GAME_TEST_QUEUE.md` หา `GameMaster.dll`/`BT_GM`/`GMUI_BASIC`/`P-3`/`P0-3`): ไม่มีบรรทัดใหม่
  หลังรอบก่อน, grep `notes_to_chief/` หา `CHIEF-REPLY` ใหม่เรื่องนี้: ไม่มี ⇒ ยังไม่มีอะไรให้ LANE-GM
  ทำต่อกับ P-3 รอบนี้ (ไม่ใช่ตัวบล็อกสายตามกฎบรรทัด 19-21 ของ NOW.md เพราะโค้ดฝั่งนี้ "เสร็จ" แล้ว)
- **GM-A** (`/warp` cross-scene) -- โค้ดจบแล้ว รอ Panya รัน `GT-192` ไม่บล็อกสาย
- **GM-B** (`/speed`) -- ดูหัวข้อ "งานจริง" ด้านล่าง มีความเคลื่อนไหวใหม่จาก LANE-DB รอบนี้
- **UI-A/UI-B/census latch** -- ไม่ใช่เขต LANE-GM

⇒ ไม่มีข้อไหนบังคับให้ LANE-GM หยุดรออย่างอื่น เดินคิวปกติต่อได้

## 1. ล็อก

`search`/`list` ทั้งสอง repo ด้วย state=open + หัวข้อ `[LANE-GM]`: ว่างทั้งคู่ ⇒ claim ใหม่
(`pf_bridge` #775, `pirate-force-server` #521, draft ทั้งคู่ตั้งแต่วินาทีแรก, commit เปล่า
"round claim: session_013nss1ekLPKipnzjiEm98vf")

## 2. ชะตารอบก่อน (n05nxf, PR pf_bridge#769 / pirate-force-server#517)

`list_pull_requests` คืน `merged: false` ให้ทั้งคู่ -- **ค่านี้ไม่น่าเชื่อถือ** (list endpoint ของ GitHub
API คืน `false` เสมอ ไม่ว่าจะ merge จริงหรือไม่ ตามที่บันทึกไว้แล้วในรอบ `743q5t` และใบ
`20260901_1105_KA1A-DISPROVEN-*.md`) ตรวจจาก `list_commits` ของ `main` โดยตรงแทน: sha ของทั้งสอง PR
(`5fc5926...` pf_bridge, `aa552949...` server) ปรากฏอยู่จริงในประวัติ `main` ตามด้วย merge commit
ของ GitHub actions bot ⇒ งานรอบก่อนอยู่บน `main` แล้วจริง ไม่ต้อง cherry-pick อะไร

## 3. กล่องจดหมาย -- 2 ใบใหม่จ่าหน้า LANE-GM ที่ยังไม่ consume

ใช้ `grep -rl "ADDRESSEE: LANE-GM" notes_to_chief/*.md` แล้วเช็ค stub `<ชื่อไฟล์>.md.CONSUMED.txt`
คู่กันทีละใบ (ระวัง: การ strip `.md` ก่อนต่อ `.CONSUMED.txt` ผิด -- stub เก็บ `.md` ไว้แล้วต่อท้าย
ชื่อไฟล์เต็ม ตรวจซ้ำกับใบเก่าที่มี stub อยู่แล้วก่อนสรุปว่าใบไหน "ยังไม่ consume" เพื่อไม่ให้นับผิดเหมือน
ที่เกือบเกิดตอนต้นรอบนี้)

| ใบ | จาก | สิ่งที่ทำ |
|---|---|---|
| `20260901_2213_LANE-DB-TO-LANE-GM-speed-sparse-live-on-main-but-speed-does-not-persist.md` | LANE-DB | **ลงมือจริง** -- ดูหัวข้อ 4 |
| `20260901_2344_COO-DECISION-old-audit-rows-stay-wall-clock-bound-not-account-bound.md` | COO | อ่านอย่างเดียว -- พับเข้า `CORE-REQUEST-GM-049` เดิม ไม่มี item ใหม่ให้ LANE-GM |

ทั้งสองใบ: วาง `.CONSUMED.txt` stub + สำเนาเข้า `consumed/` แล้ว

## 4. งานจริง: /speed ยังไม่จำข้าม session -- ขอ method จาก LANE-DB + ถาม COO เรื่องลำดับ

ใบ `2213` ยืนยัน (อ้างโค้ดจริงบน `main`, ไม่ได้เดา): sparse-x7 write path ของ LANE-DB
(`persistence_attr_compose.py:668`, `store.py:886`) ขึ้น `main` แล้วจริง เงื่อนไข (a) ของ `GT-193`
ปิด แต่ `/speed` ที่ `gm/chat_command_action.py:2481-2483` ต่อไว้ compose **เฟรมเท่านั้น** ไม่เขียน
DB แถวไหนเลย (docstring ของโค้ดเองยืนยัน) ⇒ ถ้า `GT-193` ผ่าน จะพิสูจน์แค่ "เฟรมถูก" ไม่ใช่ "จำได้"

LANE-DB เสนอ method ให้แต่ทิ้งสองข้อไว้ให้สาย GM/chief ตัดสิน (ไม่ใช่ของสาย DB): (1) จะแปลง
`identity_lo/hi` เป็น `character_id` ตรงไหน (2) DB ปฏิเสธค่าแล้วเฟรมควรออกไหม

**ตัดสินใจ**:
1. ขอ method เดียวที่รับ `identity_lo/hi` ตรง ๆ ให้ LANE-DB เป็นคนแปลงเอง (gm/ ไม่ควร
   reverse-engineer schema ของสาย DB) -- ใบ `20260902_0017_LANE-GM-TO-LANE-DB-request-speed-persistence-method.md`
2. ลำดับ DB-ก่อน-ไวร์: ตัดสินเองชั่วคราวเป็น **DB-ก่อน-ไวร์** (`None` จาก DB = ไม่ส่งเฟรม) เพราะ
   ตรงกับหลักการโปรเจกต์ที่ห้ามผลลัพธ์บนจอโกหกสถานะจริง แต่พฤติกรรมนี้ต่างจากวันนี้ (วันนี้ parse
   ผ่าน = ส่งเสมอ) ⇒ แท็ก **[สมมติของสาย GM - รอ COO ยืนยัน]** แล้วส่งใบถาม COO คู่กัน
   (`20260902_0017_LANE-GM-ASK-COO-speed-db-first-ordering-change.md`) ตามกฎ "ตัดสินแล้วเดินต่อ
   ไม่ใช่หยุดรอ" -- **ยังไม่ต่อสายโค้ดจริงรอบนี้เพราะ method ยังไม่มีให้เรียก** (เขียนโค้ดที่พึ่ง method
   ที่ไม่มีจริง = เสี่ยง import ล้ม/ทดสอบเทียม ขัดกฎ "ค้นก่อนถอด" ในทางปฏิบัติ)

## 5. pf-adversary

ไม่มีโค้ด/wire/behavior เปลี่ยนรอบนี้ (มีแค่จดหมาย + round file + CONSUMED stub) -- ไม่ต้องเรียก
`pf-adversary` ตามโปรโตคอล (ใช้ก่อน commit ที่ไม่ใช่การแก้คำผิด/เอกสาร) หมายเหตุสำหรับรอบถัดไป:
เซสชันนี้ (orchestrator หลัก ไม่ใช่ sub-agent) **มี** Agent tool จริง เห็น `pf-adversary` อยู่ในรายการ
agent type ที่เรียกได้ -- ต่างจากรอบ `n05nxf` ที่ไม่มี เมื่อรอบหน้ามีโค้ดจริงให้ต่อสาย (method จาก
LANE-DB มาถึง) ให้เรียก `pf-adversary` จริงก่อน commit ตามกฎ

## ค้นแล้ว

- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` -- ค้นแล้ว: เจอ
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` -- ค้นแล้ว: เจอ
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` -- ค้นแล้ว: เจอ (อยู่ที่ root ของ `pf_bridge`
  ไม่ใช่ใต้ `external/`)
- `GAME_TEST_QUEUE.md` หา `GameMaster.dll`/`BT_GM`/`P-3` -- ค้นแล้ว: เจอเฉพาะรายการเก่า (GT-107-R3,
  GT-164 ฯลฯ) ไม่มีใบใหม่สำหรับ P-3 รอบนี้
- `notes_to_chief/` หา `CHIEF-REPLY` ใหม่เรื่อง P-3 -- ค้นแล้ว: ไม่เจอ

## nonclaim

1. ไม่อ้างว่า GM-B "เสร็จ" -- ตรงข้าม: รอบนี้ชี้ชัดว่า `/speed` ยังไม่เขียน DB, `GT-193` ที่จะรันตอนนี้
   วัดได้แค่ว่าเฟรมถูก ไม่วัดว่าค่าจำได้ข้าม session
2. ไม่อ้างว่าตัดสินใจ DB-ก่อน-ไวร์เป็นคำตัดสินสุดท้าย -- เป็นสมมติที่ระบุชัดว่ารอ COO ยืนยัน
3. ไม่อ้างว่า P-3 ขยับ -- ไม่มีใบ GT ใหม่ ไม่มีอะไรให้ทำต่อกับ `patches/gm_plugin/` รอบนี้
4. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/
   `scenarios/world_*.json`/`scenarios/combat_*.json`/ไฟล์ใด ๆ ของสาย DB
5. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone, ไม่ boot เกม/เซิร์ฟเวอร์ใด ๆ
   รอบนี้ (mailbox/coordination round ล้วน ๆ ไม่มี GM ใช้เพื่อข้ามขั้นตอนใด ๆ)
6. ไม่ลบประวัติเดิมใด ๆ -- ใบเก่าทุกใบยังอยู่ครบ, stub ใหม่วางเพิ่มเท่านั้น

## ไฟล์ที่แตะ

`pf_bridge` เท่านั้น (ไม่มีโค้ด `pirate-force-server` เปลี่ยนรอบนี้): `notes_to_chief/` 2 stub ใหม่
+ 2 สำเนาเข้า `consumed/` + จดหมายใหม่ 2 ใบ (`20260902_0017_LANE-GM-TO-LANE-DB-request-speed-persistence-method.md`,
`20260902_0017_LANE-GM-ASK-COO-speed-db-first-ordering-change.md`) + ไฟล์รอบนี้

## PR

`pf_bridge` #775 · `pirate-force-server` #521 (companion, ไม่มี diff ซอร์ส -- round-file/letters only)
