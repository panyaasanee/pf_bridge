# FINDINGS — idle round 17 (2026-08-17 10:12–10:2x ICT)

**คำถามของรอบ:** ปิด `C1` ที่รอบ 16 จงใจเปิดค้างไว้ — รอบ 16 พิสูจน์ว่า
headless replay จบ handshake บนพอร์ต **LOGIN 10188** ได้และคำตอบตรงทุกไบต์
แต่ **ไม่แตะพอร์ต GAME 10189 เลย** เพื่อให้การทดลองมีตัวแปรเดียว
รอบนี้เพิ่มตัวแปรเดียวนั้น: **พอร์ต GAME**

**คำตอบสั้น:** 🟢 **เข้าเกมได้จริงโดยไม่มี GameClient**
สคริปต์ที่มีแต่ socket ขับ server จนถึงสถานะ `start=True teleport=True runtime_ack=True`
และ **ลำดับ request/response ที่ server ทำกับการเชื่อมต่อสังเคราะห์ของเรา
เหมือนกับที่ทำกับ client จริงทุกเหตุการณ์ (18/18)**

หลักฐาน: `pf_bridge\outbox\040_r17_game_replay.utf8.txt` (job 040, exit 0)

---

## ขอบเขตที่รักษาไว้

- **ไม่เปิด GameClient ไม่แตะ UI เกม** ทั้งรอบ — สอดคล้องกับขอบเขตใหม่ที่ผู้ใช้สั่ง 2026-08-17
- รันบน **สำเนา** ของ canonical DB · canonical sha `673F4BFB…` mtime `04:23:18.5714411`
  พิสูจน์ว่าไม่ขยับทั้งก่อนและหลัง · ไม่มี `-wal`/`-shm` งอก
- `references/` `evidence/` ไม่ถูกแตะ · repo ไม่ถูกแตะ (ยืนยันท้ายไฟล์)

---

## A — FACT เกรด A (วัดสดในรอบนี้)

### A1 — เข้าเกมสำเร็จโดยไม่มี GameClient (การอ้างหลักของรอบ)

replay ส่งเฟรมของ client จริง 10 เฟรมแรกจาก capture เข้าพอร์ต 10189
(ก่อนหน้านั้นทำ LOGIN handshake บน 10188 ตามเส้นทางจริง) ผลจาก log ของ server เอง:

| เฟรมที่เราส่ง | ขนาด | server ตอบ (label + ไบต์) |
|---|---|---|
| `LoginVerifyVital` | 55B | `LOGIN_VERIFY_ACK_ONCE` 55B, `FOUNDATION_CHARACTER_LIST_ONCE` 265B |
| `NotifyEnterCreateActor` | 32B | — |
| `StartGameReq` | 32B | `FOUNDATION_SELECTED_START_GAME` **418B**, `V113_TELEPORT_SCENE1_STABLE_ZERO_TARGET_ONCE` 73B |
| `TeleportVital` | 180B | `RUNTIME_RES_ACK_FIRST_REQ` 24B, `V99_SHOW_MESSAGE_LOCAL_SERVER_ONLINE` **102B**, `V100_MUSIC_CONTROL_CURRENT_SCENE` 39B, `HYP_PF_009_PROACTIVE_SECOND_PASSWORD_OK_ONCE` 44B |
| `GSCN_RunTimeProtocolReq` ×6 | 22B | heartbeat + `HYP_PF_009_SECOND_PASSWORD_OK_KEEPALIVE` 44B |

รับกลับ **24 เฟรม** จากการส่ง 10 เฟรม · `server closed early = False` · **stderr 0 ไบต์ตลอด**

> 🎯 **`V99_SHOW_MESSAGE_LOCAL_SERVER_ONLINE` คือเฟรมเดียวกับข้อความ
> `[ระบบ] : Pirate Force local server online`** ที่ PLAYBOOK ข้อ 6 ใช้เป็นเกณฑ์
> "เข้าแมพแล้ว" — server ยิงมันออกมาให้ client ที่ไม่มีตัวตนของเรา

### A2 — STATE flag ถึงปลายทางเดียวกับ client จริง เร็วกว่า 7 เฟรม

| flag | ของเรา | ของ client จริง |
|---|---|---|
| `start` | `rx=3` | `rx=10` |
| `teleport` | `rx=3` | `rx=10` |
| `runtime_ack` | `rx=4` | `rx=11` |
| `npc_sweep` | **NEVER** | **NEVER** |

ต่างกันเพราะ client จริงมีมนุษย์นั่งดูหน้าเลือกตัวละครอยู่ 16 วินาที ไม่ใช่เพราะโปรโตคอลต่าง
**`npc_sweep` ไม่เคยติดทั้งสองฝั่ง** — ของเดิมก็ไม่เคยติด ไม่ใช่ความบกพร่องของ replay

### A3 — ลำดับ request/response เหมือนกันทุกเหตุการณ์ (18/18) — differential พร้อม control

เทียบ `GAME_LIVE.txt` ของเรากับของ client จริง ผ่าน `pf_bridge\replay\pf_compare_gamelive.py`
(normalise ทิ้ง timestamp, `frame=N`/`rx=N`/`seq=N`, `delay=`/`late_ms=`, `peer=`/`raw=`
เก็บไว้ครบ: ทิศทาง, `pc_len`, `STRUCTURAL_IDS`, `label`, `frame_bytes`, ทั้ง 4 STATE flag)

- โหมด **full** → ต่างที่ signature line 7
- โหมด **events-only** (ตัด STATE ที่เป็น tick ตามเวลา) → ต่างที่ line **14**
- โหมด **events-only + ตัด keepalive ที่ขับด้วยนาฬิกา** → **ไม่ต่างเลย
  first divergence = None ตลอด 18 เหตุการณ์ที่เทียบได้**
- **world-entry prefix 12/12 เหตุการณ์แรกเหมือนกันเป๊ะ** ในทุกโหมด

### A4 — สาเหตุของความต่างที่เหลือถูกวัดเป็นตัวเลขแล้ว: เป็นเรื่องจังหวะ ไม่ใช่โปรโตคอล

| | keepalive `HYP_PF_009_…` | บาร์ `GSCN_RunTimeProtocolReq` ขาเข้า |
|---|---|---|
| ของเรา | ช่วงห่าง `[4.001, 2.0, 2.016]` | **flat 2.0s** (`--gap` ที่เราตั้งเอง) |
| client จริง | ช่วงห่าง `[2.053, 2.082, 2.068, 2.113, 3.826, …]` | **สลับ `0.34s / 1.75s`** = client มี timer สองตัว |

→ ทั้งสองฝั่งยิงเหตุการณ์ **ชนิดเดียวกัน** ต่างแค่เฟสการสอดแทรก
เพราะ keepalive เป็น timer ฝั่ง server (~2.05s) ส่วนจังหวะการส่งเป็นของฝั่ง client
**เลียนแบบจังหวะ `0.34/1.75` ได้ทันทีถ้าต้องการ** (แก้ค่า `--gap` อย่างเดียว)

### A5 — เกิดแถว `sessions` ที่ **แยกไม่ออกจาก client จริง**

`sessions` 1 → **2 แถว** · `selected_character_id IS NOT NULL` 1 → **2** ·
`max(lease_generation)` 1 → **2** · `open sessions` = **0** (ปิดสะอาด) ·
backpack `[(1,0),(2,1),(4,3)]` **ไม่ขยับ** · `integrity_check = ok`

แถวที่เกิด: `('35931537fc4d4c98b1420e0a8f0a9132', account_id=1, selected_character_id=1, closed, lease_generation=2)`

### A6 — corpus ฝั่ง GAME กู้คืนได้ครบ ผิดพลาดศูนย์

`GAME_20260817_042112_525596_60857.txt` → **65 เฟรมขาเข้า** ·
`verify_roundtrip` ด้วย `snappy_raw_decompress` ของ server เอง → **problems = 0**
(รันตรงกันทั้ง Linux sandbox และ Windows `py -3`)

### A7 — repo + canonical ไม่ถูกแตะ

HEAD `eef51fa` เท่าเดิม · dirty **6 ไฟล์ 187+/21−** ครบรายไฟล์ · staged 0 · untracked 0 ·
`diff --check` exit 0 · ไม่มี `index.lock` · tag ยังชี้ `d381be5` ·
canonical `CANON UNTOUCHED = YES` · สำเนา park ไป `backup\pirateforce_r17_replay_20260817_101834.sqlite3`

---

## N — NEGATIVE เกรด A (ค้นแล้วไม่มีจริง)

### N1 — capture ฝั่ง GAME **ไม่มี `SENT_` block เลยแม้แต่บล็อกเดียว**

นับแล้ว = **0** (ฝั่ง LOGIN มี จึงเทียบไบต์ได้ในรอบ 16)
→ **บนพอร์ต 10189 การเทียบระดับไบต์เป็นไปไม่ได้ด้วยหลักฐานที่มีอยู่**
oracle ที่แข็งที่สุดที่ทำได้คือ transcript ที่ server เขียนเอง (A3)
**นี่เป็นข้อจำกัดของหลักฐาน ไม่ใช่ข้อสรุปว่าไบต์ต่างกัน**

### N2 — ไม่มีอะไรบนเส้นทาง GAME ที่ปฏิเสธเฟรมเก่า

เฟรมที่ใช้ถูกจับไว้เมื่อ **04:21** และใช้ได้ผลเหมือนเดิมที่ **10:18** (อายุ ~6 ชม.)
ต่อยอดจาก N1 ของรอบ 16 (ไม่มี nonce/timestamp/sequence/challenge) → **ยืนยันบนพอร์ต GAME ด้วย**

---

## B — INFERENCE เกรด B

- **B1 — GT-003 (client 2 ตัว) ทำได้ headless แล้ว** โดยไม่ต้องเปิดเกมสักหน้าต่าง:
  A5 แสดงว่าหนึ่ง connection = หนึ่งแถวที่ `selected_character_id IS NOT NULL` + `lease_generation` +1
  → รัน `pf_replay_game.py` สองตัวขนานกันได้ตรง ๆ
- **B2 — GT-005 (การเดิน) มีวัตถุดิบครบและมีเส้นทางแล้ว**: เข้าเกมได้ถึง `runtime_ack=True`
  แล้วส่ง `TargetPosVital` (315 รูปแบบใน corpus) ต่อได้ทันที
- **B3 — GT-001 smoke ทำแบบ headless ได้เกือบทั้งรายการ** ยกเว้นข้อที่ต้องเห็นจอ
  (HP bar / minimap / ชื่อแมพ) — แต่ `V99_SHOW_MESSAGE_LOCAL_SERVER_ONLINE` ที่เป็น
  เกณฑ์ "chat online" **ตรวจได้จากสายแล้ว**
- **B4 — ต้นทุนของ harness เต็มตัวต่ำกว่าที่ประเมินไว้อีก**: เส้นทางเข้าเกมทั้งหมด
  = **4 เฟรมที่มีความหมาย + heartbeat แบบเดียว** และโค้ดที่เขียนรอบนี้ (3 ไฟล์ stdlib ล้วน)
  ครอบมันครบแล้ว

---

## 🔴 D — ของใหม่ที่ไม่มีเอกสารไหนเคยบันทึก (ข้อ 13 ใหม่)

**A5 เปิดรูที่กลับด้านกับรูที่รอบ 11 ปิดไป**

รอบ 11 พบว่าการต่อ TCP เปล่าเข้า 10189 สร้างแถว `sessions` ได้ → จึงวางกฎว่า
**ต้องนับเฉพาะ `WHERE selected_character_id IS NOT NULL`** เพื่อกัน "ผ่านด้วยเหตุผลผิด"

รอบนี้พิสูจน์ว่า **สคริปต์ 200 บรรทัดก็สร้างแถวที่ `selected_character_id IS NOT NULL` ได้
และมันแยกไม่ออกจากแถวของ client จริงในทุกคอลัมน์ที่เกณฑ์ผ่านดูอยู่**

→ กฎรอบ 11 **ยังจำเป็นและยังถูก** (มันกัน connection เปล่า) แต่ **ไม่เพียงพออีกต่อไป**
สำหรับเทสที่ต้องการอ้างว่า *"เกมจริงทำงาน"* — DB พิสูจน์ได้แค่ว่า *มีบางอย่างพูดโปรโตคอลถูก*

**ข้อเสนอ (ยังไม่ทำ รอคำสั่ง):** แยกเกณฑ์ในคิวออกเป็นสองชั้นให้ชัด
- **ชั้น wire/DB** — headless พิสูจน์ได้ ✅ ไม่ต้องรอ Panya
- **ชั้น client-observable** — เรนเดอร์/UI/ของที่ตาเห็น ❌ ต้องมี Panya เสมอ
และให้ทุกรายการในคิวระบุว่าตัวเองอยู่ชั้นไหน

---

## ⚠️ NONCLAIMS — สิ่งที่รอบนี้ **ไม่** ได้พิสูจน์

1. **ไม่ได้พิสูจน์ว่าไบต์ที่ server ส่งบนพอร์ต GAME ตรงกับของ client จริง** — ทำไม่ได้ (N1)
   พิสูจน์แค่ **label + จำนวนไบต์ + ลำดับ + STATE flag** ตรง
2. **ไม่ได้พิสูจน์ว่าเกมเรนเดอร์อะไรได้** — ไม่มี client จึงไม่มีภาพ **GT-006 ยังต้องมี Panya**
3. **ไม่ได้พิสูจน์ว่าเล่นเกมได้** — replay ไปถึง "ยืนอยู่ในแมพ" เท่านั้น ไม่ได้เดิน ตี คุย ค้าขาย
4. **ไม่ได้ทดสอบ 2 connection พร้อมกัน** — B1 เป็น inference ยังไม่ได้รัน
5. **เปิด login socket ค้างไว้ระหว่าง replay ฝั่ง GAME** (จงใจ เพื่อไม่เพิ่มตัวแปร)
   → **ยังไม่รู้ว่า GAME ทำงานได้ไหมถ้าไม่มี LOGIN มาก่อนเลย**
6. **ไม่ได้ทดสอบ reconnect / persistence ข้าม restart**
7. **ไม่ได้ทดสอบโหมด `-SecondPasswordMode required`** — ใช้ `bypass` ตามเทมเพลตเดิม
8. **ไม่ใช่ข้อสรุปด้านความปลอดภัย** — listener ผูก `127.0.0.1`, `production_allowed=false`
9. **replay 10 จาก 65 เฟรม** ที่ client จริงส่ง — ส่วนที่เหลือเป็น heartbeat กับ
   `UserSetting_UpdateServerSettingVital` ที่ยังไม่ได้แตะ
10. **ไม่ได้พิสูจน์ว่า `npc_sweep` ควรติด** — ไม่ติดทั้งสองฝั่ง ยังไม่มีใครรู้ว่ามันคืออะไร

---

## ข้อ 12 (จากรอบ 16) — ตอนนี้มีหลักฐานรองรับแล้ว

รอบ 16 เสนอทาง ก–ง สำหรับ "จะลงทุนเขียน headless harness เต็มตัวไหม"
และ chief เอนไปทาง **ข = ทำ job 040 พิสูจน์แคบ ๆ ก่อน** — **job 040 ทำแล้ว ผลเขียว**

**ตัวเลือกสำหรับ Panya (chief เอนไปทาง ค):**

| ทาง | ทำอะไร | ต้นทุน | ได้อะไร | เสียอะไร |
|---|---|---|---|---|
| ก | หยุด รอ attended session อย่างเดียว | 0 | ผลจาก client จริงเสมอ (แข็งที่สุด) | คิวค้างต่อไปจนกว่า Panya ว่าง |
| ข | ทำ probe แคบเพิ่มทีละอัน | ต่ำ | ความรู้เพิ่มทีละหยด | ไม่เคยได้ผลเทสจริงสักรายการ |
| **ค** | **เขียน harness เต็มตัว แล้วรัน GT-001/003/005 ชั้น wire/DB เอง** | **~1–2 รอบ** | **ปลดคิว 3 รายการโดยไม่ต้องรอ Panya** | เป็น **milestone ใหม่** → ต้องให้ Panya เคาะ |
| ง | commit เครื่องมือ 3 ตัวนี้เข้า repo ก่อน | ต่ำ | ของไม่หาย มี gate คุม | ยังไม่ได้ผลเทส |

⛔ **chief ไม่ทำทาง ค เอง** — กติกาห้ามเปิด milestone ใหม่โดยไม่มีคำตัดสินจากผู้ใช้

---

## เครื่องมือที่เพิ่มรอบนี้ (อยู่ใน `pf_bridge\` ทั้งหมด ยังไม่เข้า repo)

1. `pf_bridge\replay\pf_replay_game.py` — replay พอร์ต GAME + reader thread + drain ตามช่วงเวลา
2. `pf_bridge\replay\pf_compare_gamelive.py` — เทียบ transcript แบบ normalise
   (โหมด `--events-only`, รายงาน STATE milestone)
3. `pf_bridge\inbox\040_r17_headless_game_replay.ps1` → `done\`

ทั้งหมด **stdlib ล้วน ไม่ผูกกับ repo** (ยกเว้นตอนดึง `snappy_raw_decompress` จาก `v141.py`
มาใช้เป็น oracle ซึ่งต้องดึง `read_varint` มาด้วย — บทเรียนรอบ 16)
