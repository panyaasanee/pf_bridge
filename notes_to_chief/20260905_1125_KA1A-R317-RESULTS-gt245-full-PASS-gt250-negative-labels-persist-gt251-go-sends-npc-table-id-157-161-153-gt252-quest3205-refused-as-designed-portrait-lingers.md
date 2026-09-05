# KA1A-R317-RESULTS — GT-245 PASS เต็ม · GT-250 NEGATIVE (ป้ายชื่อไม่หาย) · GT-251 ตอบ (ข): GO! ส่ง id ประจำตัว NPC/วัตถุ (157/161/153 ไม่ใช่ลำดับแถว) · GT-252 เก็บครบ (quest 3205 ถูกปฏิเสธตามออกแบบ · หน้าต่างปิดเงียบ รูป Columbus ค้าง)
ADDRESSEE: chief
cc: LANE-DB (GT-245) · LANE-A (GT-250 · GT-252 · ตำแหน่ง NPC) · LANE-UI (GT-251 / RE-236 ข) · COO · ka1-B
ผู้เขียน: ka1-A (ผู้เทส attended · Panya ขับ UI เอง) · เวลา 2026-09-05 11:25 +07:00
รอบ: R317 · boot 11:00:39-11:23:41 · BOOT_COMMIT `c3454949573a084a6c6317709273dcfd78a6e87e` (เขียวล่าสุด · code_delta 0 กับหัว main `b49a4e45`) · **ไร้ธง ไร้ env ทดลอง** · run DB `state\run_gt250_20260905_110039.sqlite3` ต่อจาก run DB ของ R316 (Panya `/warp 1` ไว้ → เกิดที่ Port Royal) · **canonical sha ไม่เปลี่ยน** `4FF37060…8454` · jobs 1524 boot / 1525 teardown / 1526 release · capture `GameClient\capture_r317_20260905_110039\` (hex windows `capture_v141\GT250_251_252_hex_windows.txt`) · OBSERVER_CONFIRMED 2026-09-05T11:20+07:00 (Panya ทุกข้อ)

## 1. GT-245 CHARACTER-SELECT-SCREEN-SHOWS-THE-REAL-SCENE-001 → **[PASS เต็มสองครึ่ง]** (LANE-DB #778)
- R315 10:14: `/warp 2` → `GM_WARP_SCENE_PERSISTED scene=2` → relaunch → หน้าเลือกตัวพิมพ์ **"Prison Exile Island"** (ภาพในแชท 10:24 · จดหมาย R315)
- R317 11:02: หลัง `/warp 1` (R316 10:57 `GM_WARP_SCENE_PERSISTED scene=1`) → relaunch → หน้าเลือกตัวพิมพ์ **"Port Royal"** (ภาพในแชท 11:0x) · ก่อน #778 พิมพ์ Port Royal ตลอด (R310) ⇒ ฟิลด์ `+0x20` = scene id ถูกต้อง · PANYA-DECISION 1857 ปิดได้

## 2. GT-250 NAME-LABEL-PERSISTS-AFTER-WALK-AWAY-001 → **[NEGATIVE — อาการไม่เกิดบนบิลด์นี้]** (LANE-A)
- S0 จุดเกิด (`ScreenShot\20260905_1103xx.png` + ภาพในแชท): ป้าย title ฟ้า + name เขียว ครบ: Navy Transport Officer/Lisa · Sea Watchers/Drunkard Captain · Royal Navy Engineer/Loie · Marine Transport Station/Columbus (+ ไอคอน ! เหลืองเหนือ Drunkard Captain)
- เดิน WASD ออกไปจนพ้นสายตา (HUD ถึง X:-4,735 Y:-1,219) แล้วกลับ → **ป้ายชื่อครบทุกตัวเหมือนเดิม** · Panya: "ป้ายชื่อยังอยู่ดีทุกตัว" · ทำซ้ำตามใบ (เธอยืนยันรวม) · ไม่มีป้ายไหนเหลือแต่ title
- wire: TargetPosVital ตามปกติ · ไม่มี Traceback · census reconcile ไม่ได้ตัดสิน (nonclaim) — ผลลบ = อาการ 27 ส.ค. (ภาพ 235212) ไม่ reproduce หลัง RE-138 fix ⇒ LANE-A ปิด client-observable ของ RE-138 ได้ด้วยผลนี้

## 3. GT-251 TRACEPATH-GO-TWO-TARGETS-DISCRIMINATOR-001 → **[ANSWERED — ตอบ RE-236 ข้อ (ข) / RE-119 T4]** (LANE-UI)
- รายการในหน้าต่างแผนที่ (ภาพในแชท 11:1x): "ค้นหาตัวละครในฉาก" มีแต่แถว NPC/วัตถุ (Antique Store Love Millie · Dorothy · Guild Administrator Hields · Port Royal Congressman Frank · Finance Administrator Locher · Appraisers Joshua · Royal Exchange Manager Mackie · … · Harbor Bulletin 2) **ไม่มีหมวดเควส/จุดสำรวจแยก** (ข้อที่ chief R346 บอกว่ายังไม่มีใครวัด — วัดแล้ว: ไม่มี)
- 5 เฟรม `0x4391` 45 B ทุกเฟรมเซิร์ฟตอบ `TRACE_PATH_EMPTY_VECTOR_REPLY` 35 B (ข้อความ "กำลังค้นหาเส้นทาง" หายเอง · แชท [ระบบ] "ป้าย…ไม่มีอยู่ หรือไม่สามารถบันทึกตำแหน่งนั้นได้" 5 บรรทัด = fallback เดิม GT-120):
  | เวลา | สิ่งที่ Panya ทำ | body หลัง `12 91 43` |
  |---|---|---|
  | 11:09:57 #236 | ดับเบิลคลิกแถว 1 "Antique Store Love Millie" | `0B 00 0F 9D 00 0F 00 00 14 00 00 00 00 0F 00 00 ×4 08 00` → u16 = **157** |
  | 11:10:49 #263 | คลิกแถว 5 "Finance Administrator Locher" + GO! | u16 = **161** |
  | 11:12:06 #302 | เลื่อนหา "Harbor Bulletin 2" + GO! | u16 = **153** |
  | 11:12:56 #328 | คลิกจุดสุ่มบนมินิแมป | `… 0F 00 00 0F 00 00 14 0 0F 01 00 0F 92 3A 0F F7 3B 0F 00 7D 08 02` → id 0 · u16 1 · (14994, 15351) · u16 32000 · u8 2 |
  | 11:13:04 #333 | คลิกจุดสุ่มบนมินิแมป | id 0 · u16 1 · (13923, 4998) · u16 32000 · u8 2 |
- **อ่านผล**: u16 ตัวแรกหลัง version **ไม่ใช่ลำดับแถว** (แถว 1→157 · แถว 5→161 · แถวท้าย ๆ→153) และไม่ใช่ค่าคงที่ ⇒ เป็น **id ประจำตัวของ NPC/วัตถุ** ในตารางฝั่ง client (Columbus = 156 ตาม RE-102 อยู่ช่วงเดียวกัน — **สังเกตการณ์ ไม่ใช่ crosswalk** ให้ LANE-UI เทียบ `CONSTDATA_TH__MOBS.tsv`/ตาราง NPC ว่า 157=Millie 161=Locher 153=Harbor Bulletin 2) · ค่า 743 ของ RE-119 จึงควรเป็น MOBS n_ID "Jail Dead Prisoner" ไม่ใช่ quest 743 (ตัดสินได้เมื่อ LANE-UI ยืนยัน 3 ค่าใหม่) · มินิแมป = อีกรูป (id 0 + ธง 1 + พิกัด) ตรง GT-246
- 🔴 **ข้อเสนอถึง COO (ka1-A):** ผลนี้ต้องออกเป็น**ใบสร้าง** ไม่ใช่แค่ปิด RE: CORE-REQUEST "ตอบ `CTracePathVital 0x2F92` ด้วยเส้นทางไปหา NPC ตาม id ที่ client ส่ง (ตำแหน่ง NPC อยู่ใน roster/placement แล้ว)" (LANE-UI+LANE-A) + ใบ GT ยืนยัน auto-walk · และขยายกติกา §7 ให้ครอบ "RE ที่ตอบแล้วและมีฟีเจอร์รออยู่ → ต้องเปิดใบสร้างในรอบเดียวกัน" (Panya ถามตรง ๆ ว่า "หลังยืนยันตารางแล้วจะเกิดอะไรต่อ" — ตอนนี้ไม่มีใครถือหน้าที่นี้)

## 4. GT-252 COLUMBUS-OPTION2-BORNAGAIN-CLICK-CAPTURE-001 → **[PASS — เก็บครบตามใบ]** (LANE-A)
- P0 ผ่าน: ยืน Port Royal (HUD X:-7,902 Y:-2,307) · คลิก Columbus 11:17:09 (TargetVital 74 B → `V98_NPC_CONVERSATION_DEFAULT_P1` 44 B + `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` 54 B) → หน้าต่าง Story เปิด 2 ตัวเลือก: "ผู้นำไป Atlantic Ocean: Rising Sun Sea" / "ตั้งฐานทัพที่ Port Royal" (ภาพ `110751.png`)
- กดตัวเลือก 2 → 11:17:15 `[G< #460] QuestOperateVital 43 B`: `12 6F 6E 14 00 00 00 00 08 00 0B 02 12 01 00 12 34 3E 0B 03 12 85 0C 08 01 08 00 14 00 00 00 00 32 00 00 00 00 00 00 00 00 05 00` = vital 0x3E34 v3 · u16 **3205** · u8 1 · u8 0 · u32 0 · u64 0 · u8(0x05) 0
- เซิร์ฟ: `COLUMBUS_QUEST3205_BORNAGAIN_REFUSED reason=no_home_marker_persistence_row_evidence` · **ไม่มี** `reason=not_home_scene` (W3 ✓) · ไม่มีเฟรมตอบ (W2 ✓) · ไม่มี Traceback
- client: หน้าต่างบทสนทนา**ปิดเงียบทันที** ไม่มีข้อความ ไม่วาร์ป · 🔴 **รูปการ์ตูน Columbus ค้างบนจอ** หลังหน้าต่างปิด (ภาพ `111711.png`) — ชั้น UI ไม่ถูกล้างเมื่อบทสนทนาจบโดยไม่มี reply (ญาติ RE-168 SCENE-TRANSITION-UI-LAYER-NOT-RESET) → LANE-A/UI ตัดสินว่า reply แบบไหนปิดรูป
- ใบนี้จบที่ "capture" ตามที่ออกแบบ · ฐานทัพ (quest 3205) ยังเป็น refusal จนกว่าจะมี home-marker persistence

## nonclaims
- GT-250: ไม่ตัดสินว่า reconcile ส่งครบเพราะอะไร (แค่จอไม่เกิดอาการ) · GT-251: ไม่ตั้งชื่อ semantic ให้ 157/161/153 เอง · GT-252: ไม่ตัดสินว่ารูปค้างเป็นเพราะไม่มี reply หรือ client ต้องการ frame ปิด · dist ไม่ได้วัดทุกภาพ (`UNMEASURED_DIST` ทั้งหมด)
- ทั้ง 3 ใบไม่ได้อัดวิดีโอ (กติกา Panya) — หลักฐาน = ภาพนิ่งใน `GameClient\Data\ScreenShot\20260905_11*.png` + ภาพในแชท

-- ka1-A
