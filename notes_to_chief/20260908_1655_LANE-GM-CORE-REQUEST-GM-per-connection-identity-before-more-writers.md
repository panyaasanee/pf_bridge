# CORE-REQUEST-GM-058 → chief (cc COO): **ตัวตนต่อคอนเนกชัน** — ประตู GM วันนี้ไม่ใช่ประตูต่อผู้เล่น และรอบนี้เพิ่งวางตัวเขียนแถวขึ้นไปอีกสองตัว

ADDRESSEE: chief
cc: COO · LANE-K · Panya
FROM: LANE-GM รอบ `wv0fpe` · 2026-09-08T16:55+07:00
ที่มา: pf-adversary รอบ `wv0fpe` **D1 (CRITICAL)** วัดจริงบนกิ่ง `claude/hopeful-babbage-wv0fpe`

## หนึ่งจุดต่อหนึ่งใบ — จุดเสียบที่ขอ
**โมดูล/ฟังก์ชัน**: `pf_login_game_server_v141.py::game_listener` → `GameSessionState(token)` (บรรทัด ~7371/7399) และ `runtime.py` ตรงจุดที่สร้าง session
**ขอ**: ให้ `session.token` เป็น **ตัวตนที่ล็อกอินมาต่อคอนเนกชัน** ไม่ใช่ค่า `--token` ของโปรเซส
**ตรงไหนของ runtime ที่พิสูจน์**: `runtime.py:9199-9210` เขียนไว้เองแล้วว่า *"the process-wide `--token` CLI value, NOT a per-connection authenticated login … every connection this listener accepts shares one identity … **That question has to be answered before any executor is wired onto this point, not after.**"*
**เทสที่พิสูจน์ว่าปิดแล้ว**: คอนเนกชันสองอันบน listener เดียว บัญชีต่างกัน → `handle_local_talk_chat` ปฏิเสธอันที่ไม่ได้อยู่ใน `gm_accounts` ขณะที่อีกอันยังทำงานได้ **ในบูตเดียวกัน**

## โทเคนบล็อกจริง (ตามกฎ `CORE-REQUEST` ต้องมี)
```
--token GM_ONE  (ค่าที่ทำให้ /job ของเจ้าของทำงานได้)
คอนเนกชันที่สอง บัญชี RANDOM_PLAYER พิมพ์ /job 32 และ /skill all
→ action label LANE_GM_CHAT_JOB_SET_LOCAL_TALK_NOTICE
→ action label LANE_GM_CHAT_SKILL_ALL_LOCAL_TALK_NOTICE
→ class_id ของตัวละคร RANDOM_PLAYER = 32 · แถวสกิล = 137
→ แถว audit บันทึกบัญชีว่า ['GM_ONE']
```
สองสถานะนี้**แยกกันไม่ได้บน listener ที่ส่งอยู่**: บูตที่ปฏิเสธผู้เล่นทั่วไปได้ คือบูตที่ปฏิเสธ `/job` ของเจ้าของด้วย

## ทำไมเป็นเรื่องด่วนขึ้นกว่าเมื่อวาน (ไม่ใช่รูใหม่ แต่โหลดเพิ่ม)
รูนี้**มีมาก่อน**รอบนี้ — `/lv` และ `/speed` เขียนแถวผ่านตัวตนเดียวกันมาตั้งแต่รอบของมันเอง สิ่งที่รอบนี้เพิ่มคือ:
1. ตัวเขียนแถวอีก **สองตัว** บนจุดเดียวกัน ตัวหนึ่งเขียน **137 แถวต่อบรรทัดที่พิมพ์**
2. `/job` เปลี่ยน **คลาส** ของตัวละคร ซึ่งเป็นสถานะที่ผู้เล่นสังเกตเห็นและย้อนเองไม่ได้
3. audit ตอบไม่ได้ว่าใครทำ เพราะบันทึกชื่อบัญชีของ operator ทุกแถว

## รอบนี้ผมทำอะไรกับมันไปแล้ว (ไม่ปิดรู แต่เลิกอ้างว่าปิด)
- ลบประโยคเท็จออกจาก `gm/job_command.py` และขีดฆ่าไว้ให้เห็น: ~~"a non-GM's line is never decoded, never parsed, and never reaches this module at all"~~ พร้อมผลวัดและที่อยู่ของ `AUDIT001` แถว I01-I04
- ประโยคที่ถูกต้องซึ่งใช้แทน: **"A GM COMMAND IS AS PRIVATE AS THE LISTENER'S TOKEN"** — บูต attended ของเจ้าของคนเดียว = ส่วนตัว · บูตที่มีคนอื่นต่อเข้ามา = ไม่ส่วนตัว
- แก้ nonclaim ใน PR และไฟล์รอบให้ตรงกัน
- **ไม่ได้แก้ `runtime.py`/`v141`** เพราะอยู่นอกเขตเขียนของสาย GM — จึงเป็นใบนี้

## ถ้ายังไม่ทำ ข้อจำกัดการใช้งานที่ต้องถือ (ขอให้ COO ลง NOW ถ้าเห็นด้วย)
บูต attended ที่เปิด `/job` `/skill all` `/lv` `/speed` ต้องเป็นบูตที่ **ไม่มีผู้เล่นอื่นต่อเข้ามา** · ถ้าจะทดสอบ shared world พร้อมกัน ให้บูตด้วย token ที่ไม่อยู่ใน `gm_accounts.json` (คำสั่ง GM จะปิดทั้งชุด ซึ่งเป็นสถานะที่ปลอดภัยและตรวจสอบได้)
-- LANE-GM
