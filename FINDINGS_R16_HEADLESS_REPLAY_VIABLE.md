# FINDINGS — idle round 16 (2026-08-17 09:56–10:1x ICT)

## คำถามของรอบนี้

รอบ 15 พิสูจน์ว่า **ทั้งกระดานรอ Panya มา attended session** เพราะทุกรายการในคิว
ต้องมีคนเปิด GameClient และกด Allow — `P(อัตโนมัติทำจบเอง) = 0` เชิงโครงสร้าง

รอบนี้ไม่ถามซ้ำว่า "เมื่อไหร่จะมีคนมา" แต่ถามคำถามตรงข้าม:

> **"งานที่ค้างอยู่ *ต้อง* ใช้ GameClient จริงกี่รายการ — และมี capture ที่พอจะทำ
> headless protocol harness มาแทนได้ไหม"**

คำตอบสั้น: **ได้ และพิสูจน์สดแล้วในรอบนี้**

---

## FACT — เกรด A

### A1 · corpus ของ client จริงกู้คืนได้ครบ 20,209 เฟรม ผิดพลาด 0

`pf_login_game_server_v141.py` เขียน hexdump ของ **ทุกเฟรมขาเข้า** ลง capture log
พร้อม block `DECOMPRESSED` ที่เป็นผลถอด snappy ของ server เอง
→ เขียนตัวแกะ (`pf_bridge\replay\pf_capture_frames.py`) แล้วกวาดทั้ง `GameClient\`

| ตัวชี้วัด | ค่า |
|---|---|
| capture file ที่มี inbound | **167** (LOGIN 87 / GAME 80) |
| เฟรมขาเข้ารวม | **20,209** |
| ไบต์รวม | **504,823** |
| **roundtrip problems** | **0** |

การตรวจไม่ใช่แค่ "แกะแล้วไม่ error" — สำหรับทุกเฟรมตรวจ 3 ชั้น:
1. `len(frame) == 8 + compressed_len`
2. header `<II` ที่แกะได้ ตรงกับเลขในบรรทัดข้อความ
3. **เอา `snappy_raw_decompress` ของ server เอง มาถอด body ที่กู้จาก ASCII
   แล้วเทียบกับ block `DECOMPRESSED` ที่ server บันทึกไว้ตอนนั้น** — ตรงทุกไบต์ 20,209/20,209

รันตรงกันทั้ง Linux sandbox และ **Windows `py -3`** (job 039 ขา offline, exit 0)

### A2 · เส้นทาง login ไม่มีอะไรผูกกับ session เลย — ค่าคงที่ล้วน

นับ *จำนวนรูปแบบไบต์ที่ไม่ซ้ำ* เทียบกับจำนวนครั้งที่ปรากฏ:

| vital | ครั้ง | รูปแบบไม่ซ้ำ |
|---|---|---|
| `LSCN_LoginVitalReq` | 87 | **1** |
| `LSCN_SelectServerReq` | 80 | **1** |
| `LoginVerifyVital` | 80 | **1** |
| `StartGameReq` | 78 | **1** |
| `NotifyEnterCreateActor` | 85 | **2** |
| `GSCN_RunTimeProtocolReq` (heartbeat) | 18,848 | **1** |

→ **87 เซสชันอิสระส่งไบต์ชุดเดียวกันเป๊ะ** แปลว่าไม่มี nonce ไม่มี timestamp
ไม่มี sequence number ไม่มี challenge–response ในเส้นทางเข้าเกม
(ดู N1 — นี่คือ negative เกรด A ที่ไม่มีใครเคยตรวจ)

### A3 · ⭐ พิสูจน์สด: headless client จบ LOGIN handshake จริง และคำตอบตรงทุกไบต์

job 039 บูต server จริง (visible console, ไม่มี GameClient, ไม่แตะ UI)
แล้วให้ `pf_bridge\replay\pf_replay_login.py` ต่อ TCP เข้า `127.0.0.1:10188`
ส่งเฟรมที่กู้มา 2 เฟรม แล้วเทียบคำตอบกับที่ **client จริงได้รับใน capture เดียวกัน**

```
SENT  LSCN_LoginVitalReq         48B   ->  RECV  125B
SENT  LSCN_SelectServerReq       40B   ->  RECV   68B

[0] LOGIN_RES : IDENTICAL to capture (125B)
[1] SELECT_RES: IDENTICAL to capture  (68B)
RESULT: REPLAY EXACT          (exit code 0)
```

และ **log ฝั่ง server ที่บันทึกการเชื่อมต่อสังเคราะห์ของเรา อ่านแล้วแยกไม่ออกจากของ client จริง**:

```
STRUCTURAL_IDS [(0, 9375, '0x249F'), (15, 17087, 'LSCN_LoginVitalReq')]  OUTER version=0 mask=0x02 count=1
SENT_LOGIN_RES 125
STRUCTURAL_IDS [(0, 9375, '0x249F'), (15, 21358, 'LSCN_SelectServerReq')] OUTER version=0 mask=0x02 count=1
SELECT_IDS (1, 1)
SENT_SELECT_RES 68
```

`stderr = 0 ไบต์` ตลอด · server ปิดสะอาด `exit 0` · `[FOUNDATION] stopped` ×1 · `integrity_check = ok`

### A4 · โปรโตคอลบนสายไม่มีการเข้ารหัส และ server มีตัวสร้างครบอยู่แล้ว

framing = `struct <II` (magic, length) + body ที่ snappy-compress
`snappy_raw_decompress` (บรรทัด 520) และ **`snappy_raw_literal` (บรรทัด 560)** อยู่ในไฟล์เดียวกัน
→ ตัวสังเคราะห์เฟรม **ไม่ต้องเขียน snappy compressor เลย** ใช้ literal block ได้
พร้อม encoder ครบชุด: `u8tag/u16tag/u32tag/qwordtag/f32tag/wstr_tag/astr_tag/frame_pc`

### A5 · corpus มี vital ของฟีเจอร์จริง และมีความหลากหลายสูงพอจะใช้เป็นวัตถุดิบ

| vital | ครั้ง | ไม่ซ้ำ | เกี่ยวกับ |
|---|---|---|---|
| `TargetPosVital` | 435 | **315** | **การเดิน** → GT-005 |
| `COnLandVital` | 127 | **127** | ลงพื้น/ตำแหน่ง |
| `TeleportVital` | 76 | 19 | วาร์ป |
| `ActionVital` | 37 | 36 | แอ็กชัน |
| `TargetVital` | 56 | 14 | เลือกเป้า |
| `ItemOperateVitalReq` | 24 | **12** | **ย้ายไอเทม** → GT-002 |
| `ChooseNPC` | 21 | 9 | คุย NPC |
| `QuestOperateVital` | 19 | 2 | เควส |
| `TradeCmdVital` | 7 | 7 | ซื้อขาย |
| `CheckSecondPwdVital` | 3 | 3 | รหัสสอง |
| `CreateActorVital` | 2 | 2 | สร้างตัวละคร |

### A6 · รูปแบบ `ItemOperateVitalReq` ถอดไว้ครบแล้วในโค้ดที่ commit อยู่

- `pf_login_game_server_v141.py:3132` — *"Decode the binary-proven ItemOperateVitalReq serializer exactly"*
- `src/pirateforce_foundation/item_move_capture.py` — ตรึงไบต์จริงพร้อม sha256
  `7A59F830…36EE` และระบุฟิลด์ `(operation=4, value32=2, item_identity=1)`
- payload เป็น tag encoding ตรงไปตรงมา: `0B 04` · `14 02 00 00 00` · `32 01 00 …`

→ **สังเคราะห์คำขอย้ายไอเทมแบบอื่นได้ ไม่จำกัดแค่ replay ของเดิม**

### A7 · repo และ canonical ไม่ถูกแตะ

HEAD `eef51fa` เท่าเดิม · dirty **6 ไฟล์ 187+/21− ครบรายไฟล์** · staged 0 · untracked 0
· `diff --check` exit 0 · ไม่มี `index.lock` · tag ยังชี้ `d381be5`
· canonical **sha `673F4BFB…` mtime `04:23:18.5714411` ไม่ขยับ** ไม่มี `-wal`/`-shm`
· รันบน **สำเนา** แล้ว park ไป `backup\pirateforce_r16_replay_20260817_100221.sqlite3`
· console worktree ไม่ได้แตะ (**19 รอบติด**)

---

## NEGATIVE — เกรด A (ของที่ค้นแล้วไม่มีจริง)

**N1 · ไม่มีกลไกกัน replay อยู่ในเส้นทางเข้าเกมเลย**
ค้นแล้วไม่พบ: nonce, timestamp, sequence counter, challenge–response, MAC, หรือ
session key ในเฟรมขาเข้าช่วง login — พิสูจน์เชิงประจักษ์จาก A2 (87 เซสชัน → 1 รูปแบบ)
และยืนยันเชิงพฤติกรรมจาก A3 (เฟรมอายุ 5 ชั่วโมง 40 นาที ยังใช้ได้ผลเหมือนเดิมทุกไบต์)

**N2 · `token` ที่ `SelectServerRes` ส่งกลับ ไม่ใช่ค่าสุ่มต่อเซสชัน**
เป็นสตริง `localtest` (= ชื่อบัญชี) คงที่ใน capture ทุกไฟล์ที่ตรวจ

---

## INFERENCE — เกรด B

**B1 · GT-003 (client 2 ตัวพร้อมกัน) น่าจะทำได้โดยไม่ต้องเปิดเกมเลยแม้แต่หน้าต่างเดียว**
เดิมต้องเปิด GameClient สองหน้าต่างพร้อมกัน ซึ่งเป็นข้อที่ทำมือยากที่สุดในคิว
ถ้า GAME port ทำงานแบบเดียวกับ LOGIN → เปิดสอง socket ในสคริปต์เดียวจบ
พร้อมวัด `lease_generation` ก่อน/หลังตามเกณฑ์ที่รอบ 11 แก้ไว้แล้ว

**B2 · GT-005 (ตำแหน่งอยู่ข้าม restart) มีวัตถุดิบครบ**
`TargetPosVital` 315 รูปแบบไม่ซ้ำ = การเดินจริงที่ client เคยส่ง
เส้นทาง: replay เข้าเกม → ส่ง `TargetPosVital` → ปิด → restart → อ่าน `character_positions`

**B3 · GT-002 (M4 free-slot, any identity/any free slot) สังเคราะห์ได้ตรง ๆ จาก A6**
ซึ่งจะทำให้ GT-002 เดินได้ *ทันทีที่ Panya เคาะข้อ 6* โดยไม่ต้องรอ attended session อีกชั้น

**B4 · ต้นทุนของ harness เต็มตัวน่าจะต่ำกว่าที่เคยประเมิน**
เส้นทางเข้าเกมมีแค่ **5 เฟรมที่มีความหมาย** (`LoginVerifyVital`,
`NotifyEnterCreateActor`, `StartGameReq`, `UserSetting_UpdateServerSettingVital`,
`TeleportVital`) + heartbeat รูปแบบเดียว — ไม่ใช่โปรโตคอลหลายร้อย opcode

---

## HYPOTHESIS — เกรด C/D

**C1** · GAME port `10189` ตอบสนอง replay เหมือน LOGIN — **ยังไม่พิสูจน์**
เป็นการทดลองถัดไปที่ chief ทำเองได้ (ไม่ใช่ "เทสในเกม" เพราะไม่มี GameClient)
→ เสนอเป็น **job 040** ในรอบหน้า ขอบเขตแคบ: replay 3 เฟรมแรกแล้วดูว่าเกิดแถว
`sessions` ที่ `selected_character_id IS NOT NULL` ไหม

**D1** · headless harness ครอบคลุมได้ถึงระดับ "เล่นเกมจบลูป" — ยังไม่มีหลักฐาน

---

## ⛔ NONCLAIMS (สิ่งที่รอบนี้ **ไม่ได้** พูด)

1. **ไม่ได้พิสูจน์ GAME port** — พิสูจน์แค่ LOGIN (2 เฟรม) เท่านั้น
2. **ไม่ได้พิสูจน์ว่า replay ทำให้เกิด movement persistence** — ยังไม่ได้ส่ง `TargetPosVital` สักครั้ง
3. **ไม่ได้บอกว่า headless แทน GameClient ได้ทุกกรณี** — อะไรที่ต้องดู *พฤติกรรมฝั่ง client*
   (เรนเดอร์, UI, ของที่ตาเห็น เช่น GT-006 ที่ถามว่าพิมพ์แชทแล้ว "มีอะไรวิ่งบนสายไหม")
   ยังต้องใช้เกมจริง — replay ตอบได้แค่ฝั่ง server
4. **ไม่ได้ตรวจว่า server ตอบต่างไปเมื่อ state ต่าง** — รันบนสำเนา canonical ชุดเดียว
5. **ไม่ใช่ข้อเสนอให้ยกเลิกรายการในคิว** — เป็น *ทางเลือกเพิ่ม* ไม่ใช่ทดแทน
   ผลจาก client จริงยังเป็นหลักฐานที่แข็งกว่าเสมอ
6. **20,209 เฟรมที่ตรวจผ่าน = ความถูกต้องของการ *กู้ไบต์*** ไม่ใช่ความถูกต้องเชิงความหมาย
   ของสิ่งที่ไบต์นั้นสื่อ
7. **ไม่ได้ตรวจเรื่องจังหวะ/อัตรา** — client จริงส่ง heartbeat เป็นจังหวะ
   replay ยิงรัวติดกัน อาจให้ผลต่างในเส้นทางที่ไวต่อเวลา
8. **ไม่ใช่ข้อสรุปด้านความปลอดภัย** — listener ผูก `127.0.0.1` และ `production_allowed=false`
   N1 เป็นข้อสังเกตเชิงโปรโตคอลของ server ที่ reverse-engineer ขึ้นมาเอง
   ไม่ใช่การประเมินช่องโหว่ของอะไรที่ให้บริการจริง

---

## 🟡 สิ่งที่ผมตั้งใจ *ไม่* ทำ

- **ไม่แตะ GAME port** ทั้งที่โค้ดพร้อมและใช้เวลาอีกไม่ถึง 2 นาที —
  รอบนี้ตั้งใจให้การทดลองมีตัวแปรเดียว ถ้า LOGIN กับ GAME พังพร้อมกันจะแยกสาเหตุไม่ออก
- **ไม่เขียน harness เต็มตัว** — นั่นคือการเปิด milestone ใหม่ ซึ่งกติกาห้ามทำ
  โดยไม่มีคำตัดสินจากคุณ (ดูข้อ 12 ด้านล่าง)
- **ไม่แตะ repo** — ไฟล์ทั้งสามอยู่ใน `pf_bridge\replay\` นอก git ทั้งหมด
- ไม่ enable task ผู้เทส · ไม่แก้ cron ตัวเอง (ยังรอคำสั่งจากรอบ 15)

---

## 📌 ข้อ 12 (ใหม่) — ให้ Panya เคาะ: สร้าง headless harness เต็มตัวไหม

| ทาง | ทำอะไร | ต้นทุน | ได้อะไร | เสียอะไร |
|---|---|---|---|---|
| **ก** | ไม่ทำ รอ attended session อย่างเดียว | 0 | หลักฐานจาก client จริง 100% | คิวค้างต่อไปจนกว่าคุณจะว่าง |
| **ข** ⭐ | chief ทำ **job 040** พิสูจน์ GAME port ก่อน (แคบ ~10 นาที) แล้วค่อยตัดสิน | ต่ำมาก | รู้ว่าทาง ค คุ้มไหม **ก่อน** ลงทุน | ช้าไป 1 รอบ |
| **ค** | สร้าง harness เต็มตัว + ย้าย GT-002/003/005 มาเดินแบบ headless | สูง (milestone ใหม่) | คิวเดินเองได้โดยไม่ต้องรอคุณ | หลักฐานอ่อนกว่า client จริง · เสี่ยงเขียว-ปลอมถ้า harness ผิด |
| **ง** | ทำ ค แล้ว **เลิก** ใช้ client จริง | สูง | เร็วสุด | ❌ ไม่แนะนำ — ตัดหลักฐานชั้นที่แข็งที่สุดทิ้ง |

**chief เอนไปทาง ข** — job 040 เป็นการทดลองแคบที่ตอบ C1 ได้ในรอบเดียว
และ **ทำได้เองโดยไม่ผิดขอบเขต** (ไม่มี GameClient ไม่มี UI) ถ้า GAME port ตอบเหมือน LOGIN
ทาง ค จะมีหลักฐานรองรับ ถ้าไม่ตอบ ก็ประหยัดการลงทุนที่เปล่าประโยชน์ไปทั้งก้อน

> ⚠️ ต่อให้ทาง ค สำเร็จทั้งหมด **ข้อ 11 ก็ยังสำคัญเหมือนเดิม** — GT-006 และทุกอย่างที่
> ต้องดูพฤติกรรมฝั่ง client ยังต้องมีคุณ · headless ลด *จำนวน* งานที่ต้องรอคุณ ไม่ใช่ลบทิ้ง

---

## ไฟล์ที่รอบนี้สร้าง (นอก git ทั้งหมด)

| ไฟล์ | หน้าที่ |
|---|---|
| `pf_bridge\replay\pf_capture_frames.py` | แกะเฟรมขาเข้าของ client จริงจาก capture log + ตัวตรวจ roundtrip |
| `pf_bridge\replay\pf_replay_login.py` | replay LOGIN handshake + เทียบคำตอบทีละไบต์ |
| `pf_bridge\inbox\039_r16_headless_login_replay.ps1` → `done\` | job ที่บูต/replay/ปิด/ตรวจครบ |
| `pf_bridge\outbox\039_r16_replay.utf8.txt` | log เต็ม |
| `pf_bridge\outbox\capture_r16_replay_20260817_100221\` | capture ฝั่ง server ของการเชื่อมต่อสังเคราะห์ |
| `pf_bridge\backup\pirateforce_r16_replay_20260817_100221.sqlite3` | สำเนา DB ที่ใช้รัน (canonical ไม่ถูกแตะ) |

---

## ⭐ บทเรียนรอบนี้ — ต่อจากรอบ 12–15 เป็นชั้นที่ห้า

- รอบ 13 — *"gate ที่รันได้และเขียว ยังไม่ใช่ gate ที่เห็นงานของคุณ"*
- รอบ 14 — *"gate ที่เห็นงานของคุณ ก็ยังไม่ใช่ gate ที่เข้าใจว่างานนั้นทำอะไร"*
- รอบ 15 — *"รายงานที่ถูกต้องทุกตัวอักษร ยังทำให้เข้าใจผิดได้ ถ้าไม่บอกว่าใครคือคนที่เรารอ"*
- **รอบ 16 — "พอรู้แน่ว่ากำลังรอใคร คำถามที่ถูกต้องไม่ใช่ *เมื่อไหร่เขาจะมา*
  แต่คือ *มีงานกี่ชิ้นที่ไม่ต้องรอเขาเลย*"**

25 รอบที่ผ่านมาเปิดรายงานด้วยการนับว่ารอมากี่รอบแล้ว — ไม่มีรอบไหนถามว่า
**สิ่งที่รออยู่นั้นจำเป็นจริงหรือเปล่า** วัตถุดิบที่ตอบคำถามนี้ (capture 20,209 เฟรม)
นอนอยู่บนดิสก์มาตั้งแต่ก่อนรอบแรก และการพิสูจน์ใช้เวลาไม่ถึงหนึ่งรอบ
