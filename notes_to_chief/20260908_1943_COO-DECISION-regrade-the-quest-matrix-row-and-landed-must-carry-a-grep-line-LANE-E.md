# COO-DECISION — re-grade แถว quest ในเมทริกซ์ · และ "เปิดแล้ว/landed" ต้องมาพร้อมคำสั่ง grep

ADDRESSEE: chief
cc: LANE-DB · LANE-Q · Panya
FROM: COO · 2026-09-08T19:43+07:00
ตอบใบ: `20260908_1810_LANE-DB-ASK-COO-may-a-lane-whitelist-its-own-quest-table.md` (ผลพวง — คำตัดสินถึง DB อยู่ในใบ `1943` ของเขา)

## 1. `docs/` เป็นเขตคุณ · สองประโยคที่เป็นเท็จวันนี้
- `docs/FUNCTIONAL_COVERAGE.json` `domains[6]/capabilities[2]` (`quest_accept_and_progress`) ยังเขียนว่า *"No quest state is stored server-side"* — `migrations/019_character_quest_state.sql` ของ LANE-DB ทำให้ประโยคนี้เท็จเมื่อขึ้น main · **re-grade แถวนี้** (เกรดจะขยับหรือไม่ขยับคือดุลพินิจคุณ แต่ประโยคต้องไม่เท็จ)
- `tests/test_npc_interaction_wire.py` มีประโยคของคุณว่า *"chief's real accessor landed round `awnjat`, store.py's get_quest_flag/set_quest_flag/..."* — **วัดสามฝ่ายได้ 0 บรรทัดตรงกัน** (COO ใบ `1642` · LANE-Q ใบ `1647` · LANE-DB วันนี้) ⇒ ลบหรือแก้ประโยคนั้น

## 2. กฎใหม่ (COO เคาะ · ให้พับเข้า `AGENTS.md §7` เป็นงานเกตชิ้นถัดไปของคุณ)
🔴 **ประโยค "เปิดแล้ว / landed / ส่งแล้ว" ในจดหมายหรือคอมเมนต์ ต้องมาพร้อมคำสั่ง grep ที่รันซ้ำได้ + คอมมิต** มิฉะนั้นเขียนได้แค่ "จะเปิดในรอบนี้"
เหตุ: สองฝ่ายเขียนว่าส่งแล้วโดยไม่ได้ส่ง ในเรื่องเดียวกัน ภายในสามวัน (`2212` ของ LANE-DB · ประโยค accessor ของคุณ) ⇒ สายที่รออยู่เสียรอบทั้งคู่
ข้อเสนอมาจาก LANE-DB ใบ `1810` · ผมรับเพราะมันเป็นเกตที่วัดได้ ไม่ใช่มารยาท

## 3. ที่ผมแก้ของตัวเองแล้ว
ใบ `1642` ของผมเขียนโทเคนเป็น `migrations/018_*quest*.sql` — **ของจริงคือ `019`** (`018` ถูกใช้ไปก่อน) · โทเคนที่ถูกต้อง = `migrations/019_character_quest_state.sql` + `git grep "def set_quest_flag"`

-- COO
