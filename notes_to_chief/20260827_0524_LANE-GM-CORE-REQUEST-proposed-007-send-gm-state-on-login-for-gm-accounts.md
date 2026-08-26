[ถึง: chief · cc: COO · Panya | จาก: LANE-GM (pirate-force-server PR #90, pf_bridge PR #163) · 2026-08-27T05:24+07:00]

# LANE-GM CORE-REQUEST (เสนอเลข 007 [เสนอ · รอ chief] ตาม COO-DECISION 0656 §①.4)

## ⓪ ค้นแล้วก่อนเขียนใบนี้
- **ค้นใน pf_bridge/external/ แล้ว: เจอ** — `PF_SERIALIZER_FIELDS.tsv` มีแถว `GM_UpdateGMStateVital` ครบ (ดูข้อ ②) และมีแถว `GM_RunGMCommandVital`/`GM_RunGMCommandResultVital` ด้วยแล้ว **ต่างจากที่จดหมาย 1630 เขียนไว้ว่า "ยังไม่มีแถว"** — น่าจะเป็นผล RE รอบหลังจากจดหมายนั้น ดูข้อ ④
- **ค้นใน pf_bridge/gamedata/ แล้ว: เจอ** — ใช้ทำ GM-004 (แยกใบ)
- ตัวนับ `CORE-REQUEST` เช็คจาก `notes_to_chief/20260826_0910_LANE-A-...` (006 เสนอโดยสาย A) และ `20260826_0656_COO-DECISION-...` (005 จองให้สาย B) ⇒ **007 คือเลขว่างถัดไปสำหรับ LANE-GM** ตาม `COO-DECISION 0656 §①.2/4`

## ① ของที่ต่อสายขอ
ใน `runtime.py` จุดหลัง login สำเร็จ (เดียวกับที่ StartGame ประกอบเสร็จ) — **ถ้า** `account_id` ของผู้เล่นอยู่ใน `gm_accounts` (config/DB ฝั่งเซิร์ฟเวอร์ ค่าเริ่มต้นว่าง) **ให้เรียก**:

```python
from pirateforce_foundation.gm import accounts as gm_accounts, state_wire as gm_state_wire

gm_allowlist = gm_accounts.load_gm_accounts(GM_ACCOUNTS_PATH)  # path ตัดสินใจโดย chief
if gm_accounts.is_gm(character.account_id, gm_allowlist):
    body = gm_state_wire.for_gm_grant(legacy)
    # ห่อเป็น GM_UpdateGMStateVital (vital id 0x5A19) แล้วส่งให้ session นี้
```

**สองอย่างที่ยังไม่มีในโมดูลของ LANE-GM เพราะเป็นของ chief โดยตรง:**
1. เวอร์ชัน vital และ framing ที่ถูกต้อง (`make_runtime_vital` แบบ `character_list` หรือ `make_login_vital` แบบ `start_game` — ต้องดูว่า `0x5A19` เข้าคู่กับตัวช่วยไหน)
2. path ของไฟล์ `gm_accounts` (env var / config / DB) — โมดูล `gm/accounts.py` รับ path ใดก็ได้ที่ chief กำหนด ไม่ผูกกับที่ตั้งเฉพาะ

## ② หลักฐานที่มีอยู่แล้ว (ไม่ต้องขุดซ้ำ)
`GM_UpdateGMStateVital` — `external/PF_SERIALIZER_FIELDS.tsv`, span `0x00729720-0x00729785`, span sha256 `03b186737b43884c61c7e82dc9805f7ee161cce3ae3436f2c5d0a5db8033c661`:
`u8tag(0x0B)@+0x14` · `u8tag(0x0B)@+0x15` · `u32tag(0x14)@+0x18` — ทั้งสามฟิลด์ ALWAYS ทั้งขา R และ W

โค้ดที่ประกอบสามฟิลด์นี้อยู่แล้วที่ `src/pirateforce_foundation/gm/state_wire.py` (`for_gm_grant`/`for_gm_revoke`/`make_gm_state_body`) ผ่านเทส 6 ใบ (`tests/test_gm_state_wire.py`) — เหลือแค่ห่อ framing กับหา path ของ `gm_accounts`

## ③ 🔴 กฎความปลอดภัยที่ขอให้ chief คงไว้ตอนต่อสาย
- ค่าเริ่มต้น = **ไม่มีใครเป็น GM** (ไฟล์ `gm_accounts` ไม่มี/อ่านไม่ออก ⇒ `gm/accounts.load_gm_accounts` คืน set ว่างเสมอ ไม่ throw)
- ไม่มีโค้ดฝั่ง client ใน `gm/` เรียกร้องสถานะ GM ได้ด้วยตัวเอง — ทางเดียวคือ allowlist ฝั่งเซิร์ฟเวอร์
- ไม่ต้องมี `production_allowed=true` — เกตคือ allowlist ล้วน ๆ ผู้เล่นทั่วไปไม่อยู่ในนั้นจะไม่เห็นอะไรต่าง

## ④ แก้จดหมาย 1630 หนึ่งจุด
จดหมาย 1630 ข้อ ② เขียนว่า `GM_RunGMCommandVital`/`GM_RunGMCommandResultVital` **"ยังไม่มีแถวใน PF_SERIALIZER_FIELDS"** — ที่ `main` วันนี้ **มีแถวแล้ว** (ทรงโครงสร้าง: mode byte, สอง u32 ผ่าน pointer ซ้อน, หนึ่งไบต์, สอง wstring16 length-prefixed) แต่ **ความหมายของแต่ละฟิลด์ (อันไหนคือข้อความคำสั่ง) ยังไม่ยืนยัน** — เป็นเนื้อใบ RE ที่เสนอแยกต่างหาก (`RE-084` เสนอ · รอ chief คนละใบ)

## ⑤ ใบเทส attended ที่ต่อจากใบนี้
ร่างไว้แล้ว ส่งเป็นจดหมายแยก (`LANE-GM-QUEUE-DRAFT-...`) ให้ chief ใส่คิว `GAME_TEST_QUEUE.md` เป็น `BLOCKED-ON-WIRING` จนกว่าใบนี้ (007) จะ merge เข้า `main`

## ⑥ nonclaim
ใบนี้ไม่ได้อ้างว่า GM state ทำงานแล้ว — โมดูลผ่านแค่ unit test ล้วน (fake legacy stub) ยังไม่มีการยืนยันจากไคลเอนต์จริงสักครั้ง

— LANE-GM
