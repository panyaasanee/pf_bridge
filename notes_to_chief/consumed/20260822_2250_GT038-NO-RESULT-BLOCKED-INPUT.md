# GT-038 DAMAGE-TARGET-AB-001 — NO-RESULT / BLOCKED-INPUT

**จาก:** เซสชันหลัก ATTENDED (ผู้เทส LOCAL)  
**เวลา:** 2026-08-22 22:40–22:49 (+07:00)  
**HEAD ที่บูต:** `cf81730` (worktree สะอาดตอน boot)  
**สถานะที่เสนอ:** คง GT-038 เป็น **PENDING** และติดป้าย **NO-RESULT / BLOCKED-INPUT** — ห้ามอ่านเป็น PASS หรือ FAIL  
**จ็อบ:** `970_gt038_boot.ps1` + `972_gt038_teardown.ps1` · จ็อบ `971_gt038_client_relaunch.ps1` เตรียมไว้แต่ **ไม่ได้วาง/ไม่ได้รัน** เพราะแขน B เลือกเป้าอย่างน่าเชื่อถือไม่ได้

## สรุปคำตอบ

เซสชันนี้ให้หลักฐาน wire ของแขน A ได้ครบ 4 เฟรม แต่ **ตอบ A/B ไม่ได้**: แขน A รักษาตัวแปร “ไม่เลือกเป้า” ได้จริง ทว่าเมื่อเข้าแมพ กล้องหันเข้ากองลัง/โครงเรือและไม่เห็น `Navy Transfer` ทั้งตัว จึงไม่มีพื้นที่ภาพที่ใช้ตัดสินว่าเลขเหนือ NPC ขึ้นหรือไม่ หลัง sweep จบ ผู้เทสลองเตรียมจอสำหรับแขน B แต่ synthetic mouse ในแมพไม่ทำให้เดิน/เลือกเป้าได้อย่างน่าเชื่อถือ และไม่มี target panel ขึ้น จึงหยุดแทนที่จะยิงแขน B ที่ไม่มีเงื่อนไขควบคุม

## ชั้น client-observable

- เข้า Port Royal สำเร็จ: HP `100/100`, chat `[ระบบ] : Pirate Force local server online`, ชื่อแมพ `Port Royal`  
- พิกัดตอนเข้าแมพที่อ่านได้ประมาณ `X -8,558 / Y -2,579`; ภายหลังอ่านได้ประมาณ `X -8,653 / Y -2,579` — **ไม่ได้พิสูจน์สาเหตุของความต่างนี้**
- แขน A: ตั้งแต่เข้าแมพจนส่ง trigger **ไม่คลิกเมาส์ในแมพเลย** · เปิดแชตด้วย `Return` → พิมพ์ `PFCHATPROBE1` (ยืนยันเห็น ascii 12 ตัวในช่อง) → `Return`
- จุดบอด: ตัวผู้เล่นเห็นเต็มตัว แต่ `Navy Transfer` ไม่อยู่ในภาพและฉากถูกกองลัง/โครงเรือบัง จึงไม่ผ่านข้อบังคับ “กล้องเห็นผู้เล่น+NPC เต็มตัว” ของใบ GT-038
- ภาพที่จับรอบ cadence ไม่มีเลขหรือ `MISS` ที่อ่านความหมายได้ แต่ **ห้ามนับเป็น ‘ไม่เกิด’** เพราะเป้าหมายอยู่นอกภาพและเอฟเฟกต์สั้นกว่าช่วงจับภาพได้
- หลัง sweep จบจึงลอง setup เท่านั้น: คลิกพื้นหลายจุด (รวม single/double click), `Tab`, แป้น `Left`/`W`, และ left-drag; ตำแหน่ง/มุมกล้องไม่เปลี่ยนอย่างน่าเชื่อถือ, บางคลิกขึ้นข้อความปฏิเสธการเคลื่อนที่, และ target panel ไม่เคยขึ้น
- เพราะยังยืนยันการเลือก `Navy Transfer` ไม่ได้ จึง **ไม่รันแขน B** และไม่ส่ง trigger รอบสอง

## ชั้น wire / client log

หลักฐาน: `GameClient\capture_gt038_20260822_224119\`

- client ส่ง frame 54 bytes ที่มี `0xAC52` + UTF-16 `PFCHATPROBE1` เวลา `22:44:03.022`
- server ส่งครบ 4 เฟรมตาม scenario หนึ่งครั้ง:
  - `22:44:03.033` `HYP_PF_024_DAMAGE_NPC_HIT_WEAK` — 95 bytes, late 0.5 ms
  - `22:44:18.034` `HYP_PF_024_DAMAGE_NPC_HIT_STRONG` — 95 bytes, late 1.4 ms
  - `22:44:33.033` `HYP_PF_024_DAMAGE_NPC_MISS` — 95 bytes, late 1.0 ms
  - `22:44:48.033` `HYP_PF_024_DAMAGE_NPC_HIT_REACTION` — 95 bytes, late 0.8 ms
- `capture_v141\GAME_LIVE.txt`: label ทั้งสี่ = 1 ครั้งต่อใบ · `TargetVital` = 0 · `0x1ADD` = 0 · `Navy Transfer` = 0
- `ErrorData=28317` = 0 · traceback = 0 · `server_console_live.err.txt` = 0 bytes
- ชื่อ event `damage_model_hypothesis_npc_sweep_sent` มี **0 occurrence ใน capture log** แม้ source จะ append ชื่อนี้ใน `self.events`; จึงอ้างได้เพียง “ไม่ถูก surface ใน log ชุดนี้” ไม่อ้างว่า internal event ไม่เกิด

## DB / teardown

- run copy: `Pirate Force ServerProject\state\pirateforce_gt038_20260822_224119.sqlite3`
- run-copy SHA หลังรอบ: `C9BC917DDA80E3C735576B53582F1550AF75DA7BB7512E5A280C9F424FA07E57`
- DB before → after: sessions with selected character `7 → 8`; max lease generation `8 → 9`; open sessions after = 0; integrity = `ok`; FK rows = 0
- teardown receipt: `outbox\972_gt038_teardown.utf8.txt` + `972_gt038_teardown_console_tail_20260822_224849.txt`
- stopped marker = 1 · listeners after = 0 · GameClient processes = 0 · inbox ว่าง
- canonical DB SHA **ไม่ขยับ**: `6BFCEDD5593D316A27A6C300206A9A3BEEC5E65631835308E02289B5FE498FC7 → same`
- ไม่มี canonical backup ใหม่ เพราะไม่มีการเขียน canonical; run copy และ capture root ข้างต้นคือ artifact ของรอบ

## nonclaims บังคับ

- ไม่ claim ว่าแขน A “ไม่เห็นเลขเพราะไม่เลือกเป้า” — เป้าหมายอยู่นอกภาพ
- ไม่ claim ว่าเลขไม่ render; ไม่ claim ว่า resolve `0x2001` ล้ม; ไม่ claim ค่า toggle `[localplayer+0x420]`
- ไม่ claim ว่า `TargetVital` เป็น/ไม่เป็นสาเหตุของเลขจากรอบนี้; ได้เพียงยืนยันว่า client log ของแขน A ไม่มี `TargetVital`
- ไม่ claim ผลแขน B ใด ๆ เพราะแขน B ไม่ได้รัน
- ไม่ claim ว่า synthetic input ใช้ไม่ได้ทุกชนิด: `Return` และการพิมพ์แชตทำงาน; ปัญหาที่สังเกตคือ in-map mouse movement/target selection ในจุดเกิดนี้
- สูตรดาเมจและเฟรมทั้งสี่เป็นดีไซน์ของโปรเจกต์ ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับซึ่งกู้ไม่ได้ตลอดกาล

## งานที่ขอให้ chief ทำต่อ

1. คง GT-038 เป็น PENDING/NO-RESULT และอย่า flip ledger/matrix จากรอบนี้
2. เพิ่ม precondition ที่รันได้จริง: จัด player spawn/camera ให้ `Navy Transfer` อยู่ในภาพตั้งแต่เข้าแมพ หรือเพิ่ม trigger/hotkey ที่เลือก identity `0x2001` โดยไม่พึ่ง synthetic click
3. ตรวจว่าชื่อ event `damage_model_hypothesis_npc_sweep_sent` ควรถูก surface ใน capture log หรือ pass criterion ควรอ้างหลักฐาน label 4 ใบแทน

