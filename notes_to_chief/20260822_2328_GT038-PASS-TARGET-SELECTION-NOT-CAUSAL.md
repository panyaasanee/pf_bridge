# GT-038 DAMAGE-TARGET-AB-001 — PASS (target selection ไม่ใช่เงื่อนไขจำเป็นของเลข)

**จาก:** Codex ATTENDED (ผู้เทส LOCAL)  
**เวลา:** 2026-08-22 22:57–23:24 (+07:00)  
**HEAD ที่บูต:** `cf81730` (worktree สะอาดตอน boot และหลังจบ)  
**สถานะที่เสนอ:** **PASS** — ทั้งแขนไม่เลือกเป้าและแขนเลือกเป้าได้รับ sweep wire ครบ และมีหลักฐานเชิงบวกว่าตัวเลข render ได้ทั้งสองเงื่อนไข  
**จ็อบ:** `973` boot · `974` relaunch แขน B1 · `976` เปลี่ยนเฉพาะชื่อหน้าต่าง server console · `977` relaunch แขน B2 · `978` teardown  
`975` teardown ครั้งแรกหยุดด้วย guard ตามแบบ เพราะ info ล่าสุดเปลี่ยนจาก prefix `974_` เป็น `977_`; ไม่มีการ kill ผิดตัว

## ข้อสรุป

ผล A/B สนับสนุนคำทำนายของ GT-038 ว่า **การเลือกเป้า/`TargetVital` ไม่ใช่สาเหตุจำเป็นที่ทำให้เลขเหนือ NPC แสดงผล**:

- **แขน A — ไม่เลือกเป้า:** เห็นเลขแดง `379` เหนือบริเวณ Navy Transfer/ผู้เล่นอย่างชัดเจน โดย client session นี้ไม่มี `TargetVital`, `ChooseNPC` หรือชื่อ `Navy Transfer` ใน event log
- **แขน B — เลือก Navy Transfer:** ยืนยันการเลือกด้วย target UI/เส้นขอบเหลืองและ client event; ในรอบเก็บภาพ B2 เห็นเลขแดง `63` ชัดเจน และเห็น reaction `63` ภายหลัง
- wire ส่งลำดับ deterministic เดียวกันครบ `HIT_WEAK → HIT_STRONG → MISS → HIT_REACTION` ใน A และ B ทุก fresh client ที่ยิง trigger

ดังนั้นผลไม่ได้เปลี่ยนตามการเลือก target. อย่างไรก็ดี หลักฐานภาพไม่ได้ครอบคลุมเลขทุกเฟรม เพราะเอฟเฟกต์บางใบหายภายในประมาณหนึ่งวินาที; รายการที่ไม่ติดภาพถูกบันทึกเป็น **non-observed** เท่านั้น ไม่ใช่ “ไม่เกิด”

## ชั้น client-observable

### แขน A — no target selection

- fresh client: `capture_v141\GAME_20260822_230050_640012_61654.txt`
- ใช้ `Q` กดสั้นและเลื่อนล้อเมาส์เพื่อจัดกล้องให้เห็นผู้เล่นกับ Navy Transfer เต็มตัว; ไม่ใช้ click-ground movement และไม่คลิกเลือกเป้า
- ส่ง `PFCHATPROBE1` เวลา `23:07:30.007`
- **เห็นเลขแดง `379` ชัดเจน** ในภาพต่อเนื่องอย่างน้อย 2 sample
- `63`, `MISS` และ reaction frame ของแขนนี้ **non-observed** — cadence จับภาพไม่ทันเอฟเฟกต์สั้น ห้ามอ่านเป็นผลลบ

### แขน B1 — selected target, protocol arm

- fresh client: `capture_v141\GAME_20260822_231158_951379_55248.txt`
- เลือก Navy Transfer สำเร็จ; target panel แสดงชื่อและ HP `100`
- event `TargetVital actor_id=0x2001 data_name='Navy Transfer'` เวลา `23:13:27.814`
- ส่ง `PFCHATPROBE1` เวลา `23:14:08.091`; wire ครบ 4 ใบ
- visual samples เริ่มช้ากว่า trigger ประมาณ 5.5 วินาที จึง **non-observed ทุก transient frame**; ไม่ใช้เป็นหลักฐานลบ

### แขน B2 — fresh visual retry

- fresh client: `capture_v141\GAME_20260822_231914_655315_52971.txt`
- ใช้ `Q` กดสั้นจัดกล้อง; default zoom เห็นผู้เล่นและ NPC เต็มตัว; ไม่ใช้ click-ground movement
- เลือก Navy Transfer สำเร็จ; มีเส้นขอบ/ลูกศรเหลือง และ event `ChooseNPC actor_id=0x2001 data_name='Navy Transfer'` เวลา `23:20:19.238`
- ส่ง `PFCHATPROBE1` เวลา `23:20:55.813`
- **เห็นเลขแดง `63`** ที่ sample ประมาณ +1.265 วินาที (เห็นซ้ำที่ +1.640 และ +2.603 วินาที)
- **เห็น reaction `63`** ประมาณ +45.491 และ +47.900 วินาที
- `379` และ `MISS` ของ B2 เป็น **non-observed**: ชุดจับ +15 เริ่มจริงที่ประมาณ +17.519 วินาที และไม่มี sample ใกล้ +30 วินาที

ภาพหลักฐานที่บันทึกถาวร:

- `pf_bridge\test_evidence\GT038_armB2_target_selected_20260822_232050.jpg`
- `pf_bridge\test_evidence\GT038_armB2_selected_hit_63_20260822_232055.jpg`
- `pf_bridge\test_evidence\GT038_armB2_selected_reaction_63_20260822_232140.jpg`

## ชั้น wire / client log

capture root: `GameClient\capture_gt038_retry_20260822_225832\`

- server console มี label แต่ละชนิดอย่างละ **3 ครั้ง** (A + B1 + B2), ทุกใบขนาด 95 bytes:
  - `HYP_PF_024_DAMAGE_NPC_HIT_WEAK`: late `0.2 / 0.4 / 0.4 ms`
  - `HYP_PF_024_DAMAGE_NPC_HIT_STRONG`: late `1.0 / 0.8 / 1.2 ms`
  - `HYP_PF_024_DAMAGE_NPC_MISS`: late `0.9 / 0.8 / 0.8 ms`
  - `HYP_PF_024_DAMAGE_NPC_HIT_REACTION`: late `1.2 / 0.5 / 2.2 ms`
- A event log: `TargetVital=0`, `ChooseNPC=0`, trigger `UNKNOWN_0xAC52` เวลา `23:07:30.007`
- B1 event log: `TargetVital` ชี้ `0x2001 / Navy Transfer`, trigger เวลา `23:14:08.091`
- B2 event log: `ChooseNPC` ชี้ `0x2001 / Navy Transfer`, trigger เวลา `23:20:55.813`
- ชื่อ event `damage_model_hypothesis_npc_sweep_sent` ไม่ถูก surface ใน capture log ชุดนี้; ไม่ได้แปลว่า internal event ไม่เกิด เพราะ label wire ทั้งสี่ออกครบ
- `ErrorData=28317` = 0 · traceback = 0 · `server_console_live.err.txt` = 0 bytes

## DB / teardown

- run copy: `Pirate Force ServerProject\state\pirateforce_gt038_20260822_225832.sqlite3`
- run-copy SHA หลังรอบ: `A7581EFC3E26D74AFAF8605A893981F007186756F3020A0700190054666515FB`
- DB before → after: sessions with selected character `7 → 10`; max lease generation `8 → 11`; เพิ่ม 3 fresh sessions ตาม A/B1/B2
- after: open sessions = 0 · integrity = `ok` · FK rows = 0
- teardown receipt: `pf_bridge\outbox\978_gt038_retry_teardown_after_b2.utf8.txt`
- listeners after = 0 · GameClient = 0 · inbox ว่าง · server/console หยุดแล้ว
- canonical DB SHA **ไม่ขยับ**: `6BFCEDD5593D316A27A6C300206A9A3BEEC5E65631835308E02289B5FE498FC7 → same`

## protocol deviations / nonclaims

- ผู้ใช้อนุญาตให้ใช้ `W/A/S/D`, `Q/E` และ mouse wheel เพื่อจัดตำแหน่ง/กล้อง; รอบนี้ใช้ `Q` และ wheel ตามที่ระบุ และไม่ใช้ฟังก์ชัน click-ground ที่ผู้ใช้ปิดไว้
- B2 เป็น fresh-client retry เพิ่มเพื่อกู้หลักฐานภาพชั่วคราวหลัง B1 จับไม่ทัน ไม่ได้เปลี่ยน scenario หรือ payload
- job `976` เปลี่ยนเฉพาะชื่อหน้าต่าง console ที่กำลังรัน เพื่อไม่ให้ input bridge สับสนกับหน้าต่าง GameClient; ไม่แตะ source, DB หรือ game state
- ไม่ claim ว่าเลขทุกใบถูกถ่ายติดภาพ; อ้างเฉพาะ `379` ใน A และ `63`/reaction `63` ใน B2 ที่เห็นจริง
- ไม่ claim เรื่อง HP link, damage persistence, combat semantics หรือสูตรต้นฉบับ
- sweep นี้เป็น scenario ดาเมจที่โปรเจกต์ออกแบบ ไม่ใช่การยืนยันสูตรของเซิร์ฟเวอร์ต้นฉบับ

## งานที่ขอให้ chief ทำต่อ

1. consume note นี้และ flip GT-038 เป็น **PASS** ใน queue/ledger/matrix ตาม ownership ของ chief
2. เก็บ qualification ว่า transient frames ที่ไม่ได้ภาพเป็น **non-observed**, ไม่ใช่ absent
3. หาก pass criterion ยังต้องอ้างชื่อ event โดยตรง ให้ตรวจการ surface `damage_model_hypothesis_npc_sweep_sent`; หลักฐาน wire label ใช้งานได้ครบอยู่แล้ว
