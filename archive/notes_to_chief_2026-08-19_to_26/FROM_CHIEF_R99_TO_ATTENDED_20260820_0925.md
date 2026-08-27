# จดหมายจาก chief รอบ 99 → เซสชันหลัก ATTENDED (2026-08-20 09:25)

## สรุปรอบเดียวจบ — ของใหม่ให้เทส 1 ใบ (GT-032)
- **HEAD ใหม่: `87f0769`** (จาก `7a1137c`) — commit **16 paths** · full suite **1847 passed 1 skipped** บน Windows · fresh clone reproduce ครบ · **canonical DB ไม่แตะ** (`6BFCEDD5..8FC7`) · **ไม่แตะ `LOCK_GAME` เลย**
- **ของใหม่: HYP-PF-027 NPC-HOSTILE-001** — **Door A ของ mob-aggro**: ทำ NPC ตัวแรกของ Port Royal (`0x2001`) ให้ "ขึ้นศัตรู (แดง)" ด้วยการจับคู่ faction — ผู้เล่นได้ faction **1** ตอน StartGame + NPC ได้ faction **6** ในเฟรม spawn (คู่เดียวกับที่ SCENE-005 ทำแดงบนจอจริง)
- headless-proven ครบ (verifier 63 guards + replay 52 guards ผ่าน dispatcher จริงบนสำเนา DB) · **แต่ client ยังไม่เคยเห็นแม้แต่ไบต์เดียว** — นั่นคือ GT-032

## 🆕 GT-032 — พร้อมรันทันทีที่ `87f0769` (สเปกเต็มในคิว)
- **boot:** `--npc-hostile-hypothesis-scenario scenarios\npc_hostile_hypothesis_faction_pairing.json` (+ `--db` สำเนา) — ท่าเดียวกับ GT-024/031 เป๊ะ เปลี่ยนแค่ flag
- 🔴 **ต้องเป็นตัวละคร canonical `0x10010001`** — StartGame จะได้ faction 1 เฉพาะตัวนี้ · ตอน StartGame ดู console ว่ามี `npc_hostile_hypothesis_player_faction1_start_game_sent` ก่อนยิง
- trigger: แชต ascii 12 ตัวเป๊ะ → **sweep 1 เฟรม** (`HYP_PF_027_NPC_HOSTILE_HOSTILE_SPAWN`) · event `npc_hostile_hypothesis_faction_pairing_sent` · one-shot
- **คำถามหลัก:** เดินให้เห็น NPC `0x2001` (ตัวแรกใกล้จุดเกิด · XYZ อยู่ในเฟรม SPAWN) แล้วดูว่า **ขึ้นแดงไหม** — เส้นขอบแดง + กด Tab ได้แผง/ลูกศร target แดง เหมือน SCENE-005
- 🔴 **ไม่มีป้ายชื่อแดง** — เฟรมนี้ไม่มี name bit ⇒ ดู **เส้นขอบ + แผง Tab** ไม่ใช่ป้ายชื่อ
- ⛔ **ผลลบมีค่าเท่าผลบวก:** ถ้า NPC **ไม่แดง** = faction บิตตอน spawn บนท่อ actor-entry ไปไม่ถึง relation read → redirect Door A ทั้งประตู จดละเอียด
- จบเทส: ถ่ายภาพ → **End task** (เลนนี้ไม่แตะ DB · ไม่มีปุ่มให้กด) · run copy ทิ้งได้

## คิวที่เหลือ (รอบใหญ่ #9) — เหมือนเดิม
- **GT-031** (วงเต็ม ตี→เลือด→ตาย) · **GT-030** (remote player) · **GT-027/028** (เลขบน NPC) · **GT-029** (วงนับถอยหลัง) · **GT-026** (exit paths) · **GT-001 re-arm** (แนะนำ re-arm ที่ `87f0769` — commit นี้แตะ runtime.py + app.py หลังธง opt-in)

## ธุรการ
- เลขจ็อบคุณ = **933 ขึ้นไป (9xx)** · chief ถัดไป 162
- 🧹 GAME_TEST_QUEUE.md = 65KB — overage เป็นของ PLAYBOOK ที่ skill อ่านเอง + 7 GT ที่ยัง PENDING (archive ไม่ได้จนกว่าปิด)
- nonclaim: **faction 1/6 เป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** · Door B (NPC โจมตี) ยังปิด — จะทำหลัง GT-032 ยืนยัน Door A บวก

— chief รอบ 99 (scheduled)
