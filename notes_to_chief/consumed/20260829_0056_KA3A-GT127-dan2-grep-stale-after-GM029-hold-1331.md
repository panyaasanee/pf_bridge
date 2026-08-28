[ถึง: chief (เจ้าของคิว) · LANE-GM (เจ้าของใบ GT-127) · cc COO, Panya | จาก: ผู้เทส attended "กะ3-A" · 2026-08-29T00:56+07:00 (เวลาประมาณ)]

# GT-127 ด่าน 2 (grep block) + คำทำนาย P1-P4 **ล้าสมัยหลัง GM-029** ⇒ job 1331 ถึง abort · เสนอ hold ไว้จนชุด COO-DECISION 0041 ลง

ช่องทาง: หย่อนกล่องจดหมาย ไม่ถือ LOCK · ผมไม่แตะ GAME_TEST_QUEUE.md / src / commit — นี่เป็นการรายงาน+เสนอ ให้ chief เป็นคนแก้ใบ

## เกิดอะไร
job 1331 (รอบ attended GT-127) abort เวลา 00:44 ด้วย "dan 2 greps not satisfied" · ผมไล่ที่ main HEAD `394206c` แล้ว **ไม่ใช่ว่าใบบล็อกและไม่ใช่ SHA เก่า** — แต่**สายถูกต่อจริงแล้วในรูปแบบใหม่ของ GM-029** ทำให้ grep 2 ใน 4 บรรทัดของด่าน 2 (ที่เขียนไว้สมัย GM-028 `fire()`) เลิกแมตช์ และคำทำนาย/คอนโซลที่ใบคาดก็เปลี่ยน namespace ไปแล้ว

## หลักฐานบน main `394206c` (static/read-only)
ด่าน 2 ตามใบ 4 บรรทัด:
1. `vital_inbound_chat_local_talk` ใน `runtime.py` → **0 hit** — เพราะ GM-029 แทน `fire()` ด้วย**การเรียกตรง** `chat_command_action.make_gm_chat_command_action(...)` ที่ `runtime.py:4936` (และเช็ค label ที่ `runtime.py:4633` `WARP_ACTION_LABEL`) · import ที่ `runtime.py:29` · **บรรทัดนี้คือ "ด่านจริง" ตามที่ใบระบุเอง จึงเป็นตัวที่ทำให้ abort**
2. `def handle_local_talk_chat` ใน `gm/chat_command.py` → OK (`:350`)
3. `vital_inbound_chat_local_talk` ใน `lane_hooks/lane_gm_chat_command.py` → OK (`:14`, `:53`) — แต่โมดูล hook ตัวนี้**ไม่ใช่เส้นทาง production อีกต่อไป** (GM-029 เลิกใช้ hook)
4. `gm_command_log` ใน `gm/chat_command.py` → **0 hit** — ค่าคงที่ `DEFAULT_LOG_PATH = "capture/gm_command_log.ndjson"` อยู่ที่ `gm/commands.py:52` ไม่ใช่ chat_command.py ⇒ grep นี้ล้าสมัยเรื่อง path

คำทำนายก็ล้าสมัย: namespace อีเวนต์เปลี่ยน `gm_chat_command_*` → **`gm_chat_action_*`** (`gm/chat_command_action.py:290-291`; โค้ดคอมเมนต์ `:272-276` เตือนเองว่าเอกสารที่ยัง quote `gm_chat_command_accepted_warp`/`_refused_*` เป็นของเก่า) · และ `/warp` ตอนนี้ยิง `gm_chat_action_warp_withheld_no_confirmed_force_pos_vital_version_re129_open` (เกต RE-129 ปิด) ไม่ใช่ `accepted_warp` · `/say` ยิง `..._say_withheld_...re132_open` · คอนโซลบรรทัด `LANE_HOOK_FIRED ... lane_gm_chat_command` ที่ P4 คาดก็จะไม่โผล่ เพราะไม่ได้ผ่าน hook แล้ว

## เสนอ (ให้ chief ตัดสิน — ผมไม่แก้ใบเอง)
1. 🔴 **ยัง hold GT-127 / job 1331 ไว้ก่อน อย่าเพิ่ง re-run** — ตาม `COO-DECISION 20260829_0041` ตัวชี้ขาดของ GT-127 คือไฟล์ audit `gm_command_log.ndjson` และ COO สั่งแก้ให้ audit "ซื่อสัตย์" (บันทึกว่าต่อคิวจริงไหม ไม่ใช่แค่ประกอบสำเร็จ) + ต่อ kill-switch กลับทาง (ข) ภายใน 12:00 · เท่ากับ**สิ่งที่ใบนี้จะทดสอบกำลังถูกสั่งเปลี่ยนภายในไม่กี่ชั่วโมง** ⇒ boot ตอนนี้เสียรอบฟรีอีกใบ
2. เมื่อชุดนั้นเขียวแล้วค่อย**รีเฟรชด่าน 2 + คำทำนาย**ให้ตรงเส้นทาง direct-call + namespace ใหม่ · ชุด grep ที่ผมเสนอ (แทนของเดิม):
   - `git grep -n "make_gm_chat_command_action" <SHA> -- src/pirateforce_foundation/runtime.py`   (จุดเรียกจริง = ด่านจริง)
   - `git grep -n "def handle_local_talk_chat" <SHA> -- src/pirateforce_foundation/gm/chat_command.py`
   - `git grep -n "gm_chat_action_" <SHA> -- src/pirateforce_foundation/gm/chat_command_action.py`
   - `git grep -n "DEFAULT_LOG_PATH" <SHA> -- src/pirateforce_foundation/gm/commands.py`   (แทนบรรทัด gm_command_log ใน chat_command.py)
   - หลัง (ข) ลง เพิ่มบรรทัดยืนยัน kill-switch: `git grep -n "production_allowed" <SHA> -- src/pirateforce_foundation/runtime.py` (จุดเรียกต้องอ่านก่อน make_gm_chat_command_action)
3. อัปเดตคำทำนาย P1/P2 ให้รับ `gm_chat_action_warp_withheld_...re129_open` เป็นผลที่คาดของ `/warp` ระหว่างเกต RE-129 ยังปิด (ไม่ใช่ `accepted_warp`) — ไม่งั้นผู้เทสจะอ่านผลถูกเป็น FAIL

## nonclaims
1. ไม่อ้างว่าเส้นทาง GM-029 "ทำงานถูก" — ผมตรวจแค่ว่า grep/namespace ในใบไม่ตรงกับ main แล้ว ไม่ได้รันจริง
2. ไม่แตะ/ไม่เสนอแก้เรื่อง kill-switch หรือ token GM-030 — COO เคาะแล้วในใบ 0041 ผมแค่อ้างเป็นเหตุผลของข้อ 1
3. ไม่เปิดใบใหม่ ไม่ commit ไม่แก้คิว — ให้ chief เป็นคนแก้ใบตามที่เห็นควร
