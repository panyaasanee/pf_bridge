# 📬 ผลรอบใหญ่ #3 (attended, Panya ไม่อยู่หน้าจอ) — 17:01–17:41

- **ผู้เทส:** Claude เซสชันหลัก (skill `pf-attended-test`) · **Panya สั่งให้รันเองจนจบแล้วรายงาน**
- **HEAD ที่เทส:** `f286945` · **เทสทั้งหมดรันบนสำเนา DB** ยกเว้น GT-001 (canonical ตามสเปก)
- **jobs:** 101/102 · 104/105 · **124/125 (ใหม่ — ผู้เทสสร้างเองสำหรับ GT-016)** · 106/107 · 072/073
- 🔴 **canonical DB sha ใหม่ = `159F40EF758D567503828F0381F088247743E9663C13C692854C950F1F32DBC6`**
  (เดิม `B5557E9F..C9ED` — เปลี่ยนโดยคาดจาก GT-001: session ใหม่ + ตำแหน่งที่เดิน)
  ⚠️ **staged jobs ทุกตัวยัง pin `B5557E9F` อยู่ → ต้องอัปเดตก่อนใช้รอบหน้า**

---

## GT-011 · delete v2 ack → 🟡 **PARTIAL PASS (ก้าวหน้าชัด แต่ยังไม่ครบเกณฑ์)**

**client-observable:**
- flow: ปุ่มลบ (ซ้ายสุด) → dialog ใช่/ไม่ → **password pad คีย์บอร์ดสุ่ม** (พิมพ์ `test` ด้วยคีย์บอร์ดจริง) → ยืนยัน
- ✅ **ไม่มี GSCN error dialog อีกแล้ว** — GT-010 เคยเด้ง `ErrorData=28317` ทุกครั้ง → **root cause fix ของ DELETE-SOFT-002 ทำงานที่ชั้น parse จริง**
- ❌ **ตัวละคร Arena01 ยังอยู่ใน list** (nameboard ยังโชว์ ตัวโมเดลยังยืนอยู่) ไม่มีช่องว่าง
- ❌ หลังยืนยัน **ปุ่มอื่นบนหน้า char select ไม่ตอบสนอง** (กด "กลับ" และ "สร้างตัวละคร" ไม่มีอะไรเกิด)
  → เข้ากันได้กับสมมติฐาน "socket ถูกปิดหลัง ack" แต่ **ยังไม่ยืนยัน** (ไม่ได้วัด)
- ⇒ ไม่ได้ทำ step 5 (สร้างใหม่ลงช่องเดิม) เพราะ list ไม่ว่าง

**wire/DB (job 102 + ผู้เทสอ่านสำเนา DB เอง):**
- marker `HYP_PF_015_DELETE_ACTOR_SELECTOR00_SOFT_DELETE_COMMITTED` · **frame 79B ตรงสเปกเป๊ะ** (77B+2 trailing mask)
- สำเนา DB: `characters(1,'Arena01',selector=0,deleted_at='2026-08-18T10:06:10.775Z')` = **soft delete commit สำเร็จ**
- canonical ไม่ถูกแตะ

**สรุปให้ chief:** shape v2 แก้ปัญหา parse ได้ (ไม่มี error) แต่ **client ไม่รีเฟรช list** →
ยังขาดอะไรบางอย่างที่บอก client ว่า "ลบแล้ว รีโหลด list" · **state divergence ยังอยู่** (server ลบ / client ไม่รู้)
lead ที่ผู้เทสเสนอ (ไม่ใช่ข้อสรุป): client อาจรอ **list-refresh response** ไม่ใช่แค่ ack ของคำสั่งลบ

---

## GT-012 · chat speaker-wstring → ✅ **PASS ทุกเกณฑ์**

**client-observable (ตาเห็นชัด):**
- ชื่อตัวละครบน nameboard = `Arena01` (ค่าที่ server ต้องเติม)
- พิมพ์ `PFCHATPROBE1` + Enter → เรนเดอร์ **`[ทั่วไป] Arena01: PFCHATPROBE1`**
  → **รูปแบบเป๊ะ:** `[ทั่วไป]` + เว้นวรรค + `Arena01` + `:` + เว้นวรรค + ข้อความ (ไม่มีเว้นวรรคก่อน `:`)
- `PFCHATPROBE2` → เรนเดอร์เหมือนกันครบ (**ไม่ one-shot**)
- `SHORT` (5 ตัว) → **เงียบสนิท ไม่มี error** = fail-closed ที่ชั้น UI ยืนยันซ้ำ
- ไม่มี crash / ไม่หลุดแมพ / ไม่ desync
- 🟢 **label ที่เห็นจริง = `[ทั่วไป]`** → ยืนยัน prediction ของ CHAT-ECHO-005/006/007 (id 540 path)

**สรุปให้ chief:** HYP-PF-014 v2 **ผ่าน client acceptance** — ชื่อผู้พูดเรนเดอร์จาก wstring#1 จริง

---

## GT-016 · channel sweep → ✅✅ **PASS แบบชี้ขาด (ผลที่สวยที่สุดของรอบนี้)**

พิมพ์ `PFCHATPROBE1` ครั้งเดียว → server ยิง 5 เฟรม → **client เรนเดอร์ 5 บรรทัด คนละ label คนละสี:**

| ลำดับ | label ที่เห็นบนจอ | สี | เฟรม |
|---|---|---|---|
| 1 | `[ทั่วไป]` | ขาว | LOCALTALK |
| 2 | `[ปาร์ตี้]` (อ่านได้ "ปาร์ตี้/ทีม") | ฟ้า | PARTY |
| 3 | `[กิลด์]` | เขียว | GUILD |
| 4 | `[GM]` | แดง | GMGLOBAL |
| 5 | `[ทั้งหมด]` | ชมพู/ม่วง | ACTORBOARDCAST |

**wire (job 125):** เห็นครบ 5 label เรียงตามลำดับเป๊ะ
`HYP_PF_019_CHANNEL_SWEEP_LOCALTALK → _PARTY → _GUILD → _GMGLOBAL → _ACTORBOARDCAST`
· **frame_bytes = 66B เท่ากันทุกเฟรม** · speaker ว่างทุกเฟรมตามดีไซน์

**สรุปให้ chief:** **claim ของ GT-016 ผ่านเต็ม** — payload ไบต์เดียวกันเป๊ะ ต่างแค่ class id (byte 16–17)
→ client แยกช่อง/สี/label ได้ 5 แบบ ⇒ **"channel identifier คือ 16-bit class id ไม่ใช่ field ใน payload" พิสูจน์ที่ชั้น client-observable แล้ว**
· นี่คือหลักฐานที่ดัน CHAT-CHANNEL-001 จาก static → runtime ได้ทั้งก้อน
· 📌 job ที่ใช้: **`124_gt016_boot.ps1` / `125_gt016_teardown.ps1`** (ผู้เทสสร้างจาก 104/105 โดย sed เปลี่ยนธง+scenario)
  ⚠️ บรรทัด log ในไฟล์ยังพิมพ์ป้ายเก่า `scenario=chat_input_hypothesis_speaker_echo` (sed ไม่ได้แตะข้อความ)
  — **ธงจริงที่ใช้บูตถูกต้อง** (`--channel-message-hypothesis-scenario ...channel_sweep.json`) chief แก้ป้ายก่อน stage ถาวรด้วย

---

## GT-013 · logout worldinfo-first → ❌ **FAIL ทั้ง 03 และ 01 (falsify shape ที่สาม)**

**client-observable:**
- **subcode 03** (กลับหน้าเลือกตัวละคร, กด 17:29:12): dialog ปิด → **ไม่ transition** ยังอยู่ในแมพ
  ครบ 15+ วิ · ไม่มี error dialog · UI ยังตอบสนอง (เปิดเมนู HOME ซ้ำได้)
- **subcode 01** (ออกเกม, กดต่อในเซสชันเดียวกัน): **ไม่ปิดตัวเอง** เช่นกัน
  ⚠️ **nonclaim:** 01 รอบนี้ทำหลัง 03 ในเซสชันเดียวกัน — socket อาจถูกปิดไปแล้วตั้งแต่ 03
  → **ผลของ 01 ยัง confounded** ต้องเทสใหม่ในเซสชันสดถ้าจะสรุป
- ออกจริงด้วย X ปกติ

**wire (job 107):** ลำดับถูกต้องครบตามดีไซน์ —
`HYP_PF_016_LOGOUT_SUBCODE03_WORLDINFO_RESPONSE_FIRST **283B**` (late 1.2ms)
→ `HYP_PF_016_LOGOUT_SUBCODE03_ACK_THEN_SERVER_SOCKET_CLOSE **46B**` (late 49.9ms) · open sessions = 0

**สรุปให้ chief:** shape 3 (worldinfo-first) **ถูก falsify ที่ชั้น client** เหมือน shape 1 (echo) และ shape 2 (ack+close)
· **ข้อสังเกตที่อาจสำคัญ:** ทั้ง GT-011 (list ไม่รีเฟรช) และ GT-013 (ไม่ transition) มีอาการร่วมกัน =
**client ไม่เปลี่ยนสถานะ UI จาก response ที่เราส่ง** ทั้งที่ parse ผ่าน (ไม่มี error) →
lead ที่ผู้เทสเสนอ: อาจต้องมี **state-change/scene-change frame** อีกชนิดที่ยังไม่ได้ทำ ไม่ใช่แค่ ack ของคำสั่ง

---

## GT-014 · movement authority (observation) → 🟢 **ไม่มี rubber-band / ไม่มี server correction**

- เดินบนพื้นโล่ง: พิกัดขยับจริง `X:-8,094 Y:-3,207` → `X:-8,553 Y:-2,579`
- **เดินชนสิ่งกีดขวาง (โครงสร้างเรือ/กำแพง) ค้างไว้:** ตัวละคร**หยุดที่ขอบ ไม่ทะลุ ไม่ถูกดึงกลับ**
  พิกัดค้างที่ `-8,553 / -2,579` ไม่กระตุก ไม่ snap-back
- คลิกไปยังจุดที่เดินไม่ถึง (บนโครงสร้าง): **ตัวละครไม่ขยับเลย** (client กันเองที่ pathfinding)
- **wire:** `TeleportVital` = **1 บรรทัด** (echo ตอน entry เท่านั้น — ตรง observation ที่คิวสั่งให้เช็ค) ·
  **`MovementAttr` server→client ระหว่างเดิน = 0 บรรทัด** · `TargetPos` mentions = 8
- DB: `heading` = 4.532 (ค่าเฟรมสุดท้ายตอนหยุด) — sub-observation heading ยังไม่ได้เทส respawn รอบถัดไป

**สรุปให้ chief:** ตอกย้ำ **client-authoritative** ที่ชั้น observed behavior — server ปัจจุบันไม่เคยส่ง reposition
ระหว่างเดิน และ collision ถูกบังคับฝั่ง client ล้วน · **nonclaim เดิมยังยืน:** ไม่ได้บอกว่า server ต้นฉบับทำแบบไหน

---

## GT-001 · smoke → ✅ **PASS ทุกเกณฑ์ที่ `f286945`**

- client-observable: full loop ครบ (HP 100/100 · minimap · Port Royal · chat online) ·
  **เกิดที่ `X:-8,094 Y:-3,207` = ค่า persist จากรอบก่อนเป๊ะ** · เดินได้ · ออกสะอาด X+ยืนยัน
- wire/DB (073): stopped ×1 · stderr 0B · listeners 0 · sessions 6→**7** · lease 6→**7** ·
  open 0 · backpack `[1@0,2@1,4@3]` ไม่เปลี่ยน · integrity ok
- **position ถูกเขียนใหม่ตามที่เดิน** → `(-8553.947, -2579.689, 186.0, h=4.532)` @ 10:38:40Z
  = persistence ทำงานอีกครั้ง (ของแถมจาก GT-014)
- ⚠️ **canonical sha ใหม่** ดูหัวไฟล์

---

## 🔴 ของที่ chief ต้องแก้ (เจอระหว่างรัน)

1. **staged jobs pin sha เก่าหมดทุกตัว** — 072 ABORT ตอนแรกเพราะ pin `D08A89BF` (ค่าเมื่อวาน)
   ผู้เทสแก้เป็น `B5557E9F` แล้วรันต่อ · **ตอนนี้ต้องเป็น `159F40EF..DBC6`**
   → เสนอ: ให้ boot job อ่าน sha คาดหวังจาก **ไฟล์เดียว** (เช่น `pf_bridge\CANON_SHA.txt`)
   แทน hardcode ในทุก job — จะได้แก้ที่เดียวจบ
2. **job 124/125 ที่ผู้เทสสร้าง** ควรถูกรับเข้า `done\`/`staged\` อย่างเป็นทางการ + แก้ป้าย log
3. GT-011/GT-013 มี **อาการร่วม** (client parse ผ่านแต่ไม่เปลี่ยนสถานะ UI) — น่าตั้งเป็นสมมติฐานเดียวกัน

## 📸 หลักฐานภาพ

- `pf_bridge\evidence_screens\biground3\` — **มีแค่ 1 ไฟล์** เพราะผู้เทสพลาด: ใส่ `save_to_disk`
  ไว้ใน action ของ `computer_batch` ซึ่ง**ไม่รองรับ** (ต้องใส่ระดับ tool หรือเรียก `screenshot` เดี่ยว)
  → ภาพทั้งหมดของรอบนี้อยู่ในแชทกับ Panya · **บทเรียนนี้ใส่ skill แล้ว**
- หลักฐาน wire/DB ครบทุกเทสอยู่ใน `GameClient\capture_gt0*_20260818_*` + `outbox\10*/12*/07*`
