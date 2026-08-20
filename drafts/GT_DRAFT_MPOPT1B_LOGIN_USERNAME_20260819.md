# ร่างรายการ GT — MP-OPT1-B (login ด้วย username อื่น)

> 📌 **ร่างเท่านั้น — ผู้เขียนร่างนี้ไม่ได้แตะ `pf_bridge\GAME_TEST_QUEUE.md`**
> chief เป็นผู้ย้ายเข้าคิวและตั้งเลข GT เอง (ร่างนี้ตั้งชื่อชั่วคราวว่า **GT-020**)
> ที่มา: `Pirate Force ServerProject\reports\PF_MPOPT1B_LOGIN_VITAL_REQ_0X42BF_STATIC_20260819.md`
> verifier: `tools\pf_login_vital_req_static.py` (126 guards, exit 0)
> **สร้างเมื่อ 2026-08-19 · วัดที่ HEAD `dd1a66c`**

---

## สรุปให้ chief อ่าน 30 วินาที (ทำไมสเปกนี้ไม่เหมือนที่ audit เขียนไว้)

audit G8 เขียนว่า *"decodable with one attended run that types a different username"*
รอบนี้แกะ static แล้วพบว่า **ทั้ง field roles และค่าที่จะออกไปบนสาย พิสูจน์ได้ครบจากไบนารีแล้ว ไม่ต้องรัน**:

* `0x42BF` มี **2 field เท่านั้น** — `wstring @+0x14` (tag `0x48`) = **บัญชี** · `string @+0x30` (tag `0x44`) = **รหัสผ่าน (cleartext)**
* client **hex-decode ค่าของ `-acc`** ก่อนใส่ลงเฟรม (`0x89B070`) ⇒ `-acc test` → `U+000E U+0000` = ไบต์ `0E 00 00 00`
  **ที่ทุก capture เห็นมาตลอด — ไม่ใช่เพราะ field เป็นค่าคงที่ แต่เพราะเราส่ง argument เดิมทุกครั้ง**
* ⇒ **สิ่งที่เทสนี้เหลือให้พิสูจน์คือชั้น client-observable เท่านั้น**: เปลี่ยนบัญชีแล้ว **client ยังเข้าเกมได้ไหม**
  ส่วนไบต์ที่จะออกไป **เราทำนายล่วงหน้าได้เป๊ะทุกไบต์แล้ว** (ตารางด้านล่าง)

⚠️ **ห้ามพิมพ์ชื่อบัญชีตรง ๆ ใน `-acc`** — `-acc bob` จะกลายเป็นขยะบนสาย ไม่ใช่ `L"bob"`
ต้องใส่ **hex ของชื่อ** (2 หลักต่อ 1 ตัวอักษร) เช่นอยากได้ `mptest02` ต้องใส่ `-acc 6D70746573743032`

---

## GT-020 MP-OPT1-B: login ด้วยบัญชีอื่น — เฟรม `LSCN_LoginVitalReq 0x42BF` เปลี่ยนตามจริงไหม และ client ยังเข้าเกมได้ไหม  [PENDING — พร้อมรันทันที ไม่มี prerequisite]

- **ที่มา:** MP-OPT1-B (รอบนี้) ตอบ **G8** ของ MULTIPLAYER-READINESS-AUDIT-001 ระดับ static ครบแล้ว:
  field ของบัญชีคือ `wstring @+0x14` และค่าของมัน = `decode_hex(-acc)` · รหัสผ่าน `@+0x30` ส่งเป็น
  **cleartext** ผ่าน `WideCharToMultiByte` ไม่มี hash · **ไม่มี hypothesis ใหม่ ไม่แตะ `src/` ไม่ต้อง encoder**
- objective (claim เดียว — **ชั้น client-observable**): เมื่อเปลี่ยน `-acc`/`-pwd` ของ client
  **client ยัง login เข้าเกมได้ตามปกติหรือไม่ (ไม่มี error dialog / ไม่ค้าง)**
  — ชั้น wire ใช้เป็นหลักฐานยืนยันว่าไบต์เปลี่ยนจริงตามที่ static ทำนาย
- **prerequisite: ไม่มี**
  - ❌ **ไม่ต้องเตรียมบัญชีในฐานข้อมูลล่วงหน้า** — ตรวจ `src/` แล้ว: server **ไม่เคยอ่าน field บัญชีจากสาย**
    (`v141` ตอบ `0x42BF` ด้วย nested id อย่างเดียว ไม่มี parser ของ payload) และชื่อบัญชีที่ persist
    มาจาก **argument ของ server เอง** (`--token`, default `localtest`) ไม่ใช่จาก client
    · `store.ensure_account` = `INSERT OR IGNORE INTO accounts(login_name,created_at)` → สร้างแถวเองอยู่แล้วถ้าจะใช้
  - ⇒ **DB จะไม่เปลี่ยนตามชื่อบัญชีที่ client ส่ง และนั่นคือผลที่คาด** (ดู nonclaims)
- db: **สำเนาสดของ canonical** (`state\pirateforce_gt020_<stamp>.sqlite3`) · canonical sha ต้องไม่ขยับ
- server args: `--second-password-mode bypass` · **ไม่ต้องใส่ scenario ใด ๆ** (เทสนี้ไม่ใช้ hypothesis lane)
  · `--capture-root "<GameClient>\capture_gt020_<stamp>"`
- **client args (นี่คือหัวใจของเทส — job ทุกตัวที่ผ่านมาใช้ `-acc test -pwd test`):**

  | เฟส | client args ที่ต้องใช้ | บัญชีที่ออกไปบนสายจริง | รหัสผ่านบนสาย |
  |---|---|---|---|
  | **A** | `-launchbypatcher -subbuildversion 132 -acc 4142 -pwd test` | `AB` | `test` |
  | **B** | `-launchbypatcher -subbuildversion 132 -acc 6D70746573743032 -pwd mppass02` | `mptest02` | `mppass02` |

  · **A ออกแบบให้เสี่ยงน้อยที่สุด:** ความยาวเฟรม **เท่าเดิมเป๊ะ** เปลี่ยนแค่ **2 ไบต์** และรหัสผ่านไม่เปลี่ยน
    ⇒ ถ้าอะไรพัง จะรู้ทันทีว่ามาจาก field บัญชีตัวเดียว
  · **B เปลี่ยนทั้งสอง field และเปลี่ยนความยาวทั้งสอง field** ⇒ พิสูจน์ว่า length prefix เป็นตัวแปรจริงด้วย
  · ทำ **A ก่อนเสมอ** · ถ้า A ไม่ผ่าน ให้หยุด รายงาน แล้ว **ไม่ต้องทำ B**

- **ไบต์ที่ทำนายไว้ล่วงหน้า (static — เอาไว้ grep ใน capture ได้ตรง ๆ)**
  ในไฟล์ `capture_gt020_<stamp>\LOGIN_*.txt` ใต้บล็อก `DECOMPRESSED`:

  ```
  ปัจจุบัน (-acc test -pwd test)   12 BF 42 0B 00 48 04 00 00 00 0E 00 00 00 44 04 00 00 00 74 65 73 74
  เฟส A   (-acc 4142 -pwd test)    12 BF 42 0B 00 48 04 00 00 00 41 00 42 00 44 04 00 00 00 74 65 73 74
  เฟส B   (-acc 6D70… -pwd mppass02)
          12 BF 42 0B 00 48 10 00 00 00 6D 00 70 00 74 00 65 00 73 00 74 00 30 00 32 00
                            44 08 00 00 00 6D 70 70 61 73 73 30 32
  ```

  และในไฟล์ `GAME_*.txt` (`LoginVerifyVital 0x3784`) จะเห็นบัญชี **ตัวเดียวกัน** ซ้ำอีกที:

  ```
  ปัจจุบัน  0B 68 48 04 00 00 00 0E 00 00 00 44 09 00 00 00 "localtest"
  เฟส A     0B 68 48 04 00 00 00 41 00 42 00 44 09 00 00 00 "localtest"
  เฟส B     0B 68 48 10 00 00 00 6D 00 70 00 74 00 65 00 73 00 74 00 30 00 32 00 44 09 00 00 00 "localtest"
  ```

  (คอลัมน์ ASCII ของ hexdump จะอ่านได้เป็น `.A.B.` และ `.m.p.t.e.s.t.0.2` ตรง ๆ)

- 🔴 **ความเสี่ยงที่รู้ล่วงหน้า — ต้องอ่านก่อนรัน ไม่ใช่หลังพัง**
  `v141.make_game_login_ack` สร้าง ack ของ `LoginVerifyVital` จาก **literal แช่แข็ง**
  `b"\x0B\x68\x48\x04\x00\x00\x00\x0E\x00\x00\x00" + astr_tag(token)` — คือบัญชีของ `-acc test` **ตัวเก่า**
  ⇒ เมื่อ client ส่งบัญชีใหม่ **server จะ echo บัญชีเก่ากลับไป**
  · ถ้า client ไม่สนใจ → เข้าเกมได้ตามปกติ (นี่คือสิ่งที่คาด เพราะ static ไม่พบ compare ใด ๆ)
  · ถ้า client ค้าง/เด้ง error ที่ขั้นนี้ → **นั่นคือผลบวกที่มีค่ามาก** แปลว่า client ตรวจ echo จริง
    → **จดเป็น observation แล้วจบเทส · ห้ามแก้ `src/` หรือ v141 เองในเซสชันเทส**
  · จุดสังเกตที่แน่นอน: ถ้าผ่านหน้าเลือกเซิร์ฟเวอร์แล้วเข้าหน้าเลือกตัวละครได้ = ผ่านจุดนี้แล้ว

- steps (ทีละคลิก — อ้าง PLAYBOOK ข้อ 1–8):
  1. boot server ตาม PLAYBOOK ข้อ 1 (แบบจาก `staged\072_gt001_boot.ps1`) บน **สำเนา canonical**
     · ยืนยัน listener 2 ตัว (10188/10189) · จด `captureRoot`
  2. **เฟส A** — เปิด client ด้วย ProcessStartInfo (PLAYBOOK ข้อ 2) โดยใช้ args ของ **A** ในตารางข้างบน
  3. รอ ~30 วิ → หน้าเลือกเซิร์ฟเวอร์: คลิกปุ่มซ้ายล่างใต้ panel (ยึดภาพ ไม่ยึดพิกัด)
     · **จุดตัดสินแรก: ถ้าไม่ขึ้นหน้านี้เลย หรือขึ้น error dialog → หยุด เก็บภาพ + capture แล้วรายงาน**
  4. dialog เตือน PVP → คลิกปุ่มซ้าย (ยืนยัน)
  5. หน้าเลือกตัวละคร: ต้องเห็น Arena01 + nameboard ตามปกติ
     · **⚠️ ปุ่มแรกซ้ายสุด = ลบตัวละคร ห้ามกด** · คลิกปุ่ม **กลางสุด** จาก 5 ปุ่มแถวล่าง = เข้าเกม
  6. loading (โปสเตอร์ WANTED) → เข้าแมพ: ต้องเห็น HP bar, minimap, ชื่อแมพมุมขวาบน,
     chat `[ระบบ] : Pirate Force local server online` · **ถ่ายภาพหน้าจอไว้ 1 รูป**
  7. ออก: คลิก X มุมขวาบน **ครั้งเดียว** → dialog ยืนยัน → คลิกปุ่มซ้าย · ถ้าค้าง → End task
  8. **เฟส B** — เปิด client อีกรอบบน **server ตัวเดิมที่ยังรันอยู่** ด้วย args ของ **B**
     (แบบจาก `done\068_gt002_reconnect_client.ps1` ที่พิสูจน์แล้วว่าเปิดซ้ำได้)
     · ทำข้อ 3–5 เหมือนเดิม · **หยุดที่หน้าเลือกตัวละคร ไม่ต้องเข้าแมพ** (ประหยัดเวลา ไม่ลดค่าหลักฐาน)
     · แล้วออกด้วย X (หน้านี้ปิดทันที ไม่มี dialog ยืนยัน)
  9. teardown ตาม PLAYBOOK ข้อ 8 + เก็บ `captureRoot` ทั้งโฟลเดอร์เข้า `outbox\`

- pass criteria (แยกชั้น):
  - **client-observable (นี่คือ claim ของเทสนี้):**
    - เฟส A: ผ่านหน้าเลือกเซิร์ฟเวอร์ → หน้าเลือกตัวละคร → **เข้าแมพได้ครบ** (HP bar + minimap + ชื่อแมพ + chat online)
      · **ไม่มี error dialog ใด ๆ** · client ไม่ค้าง · ออกสะอาด
    - เฟส B: ผ่านหน้าเลือกเซิร์ฟเวอร์ → **เห็นหน้าเลือกตัวละครพร้อม nameboard** · ไม่มี error dialog
  - **wire-DB (ยืนยันซ้ำ ไม่ใช่ claim หลัก):**
    - `capture_gt020_*\LOGIN_*.txt` ของเฟส A มีบล็อก `DECOMPRESSED` ที่ **ตรงกับแถว "เฟส A" ในตารางไบต์ทุกไบต์**
    - `capture_gt020_*\LOGIN_*.txt` ของเฟส B ตรงกับแถว "เฟส B" ทุกไบต์
    - `GAME_*.txt` ของแต่ละเฟสมี `LoginVerifyVital` ที่ขึ้นต้นด้วย prefix ที่ทำนายไว้
    - **canonical sha ไม่เปลี่ยน** (รันบนสำเนา) · `stopped ×1` · `stderr 0B` · `listeners 0` หลัง teardown
    - `sessions` ของสำเนา **+2** (สองการเชื่อมต่อ) และ `accounts.login_name` **ยังเป็น `localtest` เหมือนเดิม**
      ← **ค่านี้ที่ "ไม่เปลี่ยน" คือผลที่ถูกต้อง ไม่ใช่ FAIL** (ดู nonclaims)

- nonclaims (สำคัญมาก อย่า claim เกิน):
  - ❌ **ไม่ claim ว่า DB แยกบัญชีได้** — server ยังไม่อ่าน field นี้เลย ฉะนั้นแถว `accounts` จะไม่งอกตาม `-acc`
    **ถ้าใครเห็นแถวใหม่ชื่อ `AB`/`mptest02` แปลว่ามีอย่างอื่นผิด ไม่ใช่ว่าเทสสำเร็จเกินคาด**
  - ❌ ไม่ claim ว่า server ต้นฉบับ validate บัญชี/รหัสผ่านแบบใด — **ต้นฉบับปิดไปแล้วและไม่เคยมี publish**
  - ❌ ไม่ claim อะไรเกี่ยวกับ `LSCN_LoginVitalRes 0x42E3` (รอบนี้แกะแค่ชื่อ/hash/id slot ของมัน)
  - ❌ ไม่ claim two-client / concurrent — เทสนี้ยังเป็น **client เดียว ต่อกันตามลำดับ** (ข้อจำกัด serial ของ server ยังอยู่)
  - ❌ ไม่ claim ว่า `-pwd` ถูกตรวจสอบที่ใด — พิสูจน์แค่ว่า **มันไปถึงสายเป็น cleartext**
  - ❌ ไม่เปิดเลนใหม่จากผลนี้ (Option 2/3 ยังไม่ได้รับอนุมัติงบ)

- 🩹 **ถ้า FAIL ที่เฟส A:** ทางสำรองที่ถูกที่สุด = รันซ้ำด้วย `-acc 74657374 -pwd test`
  (บัญชี = `L"test"` — ชื่อเดียวกับที่เราเรียกกันมาตลอด แต่ **ไบต์บนสายยาว 8 ไม่ใช่ 4**)
  เพื่อแยกว่าปัญหาคือ *ค่าของบัญชี* หรือ *ความยาวของ field*

- **สิ่งที่ผู้เทสต้องกรอกกลับ (ขั้นต่ำ):**
  1. เฟส A ไปถึงขั้นไหน + ภาพหน้าจอตอนเข้าแมพ
  2. เฟส B ไปถึงขั้นไหน
  3. บล็อก `DECOMPRESSED` ของ `LOGIN_*.txt` ทั้งสองเฟส (คัดลอกมาทั้งบล็อก)
  4. `canonical sha` ก่อน/หลัง · `sessions`/`lease_generation` ก่อน/หลังของสำเนา
  5. มี error dialog อะไรโผล่บ้างไหม (แม้จะกดผ่านไปได้ก็ต้องจด)

- result: (ผู้เทสกรอก)

---

## หมายเหตุสำหรับคนสร้าง job

- job boot ลอกจาก `staged\072_gt001_boot.ps1` ได้ทั้งดุ้น — **แก้แค่**
  ป้าย log, `captureRoot` เป็น `capture_gt020_<stamp>`, ชื่อ run DB, และ **`-ArgumentList` ของ client**
  จาก `'-acc','test','-pwd','test'` เป็น `'-acc','4142','-pwd','test'`
- job เปิด client รอบสอง (เฟส B) ลอกจาก `done\068_gt002_reconnect_client.ps1`
  แก้เป็น `'-acc','6D70746573743032','-pwd','mppass02'`
- **ไม่ต้องใส่ธง scenario ใด ๆ** — เทสนี้ไม่มี hypothesis lane และไม่ควรมี
- ตรวจ `pf_bridge\CANON_SHA.txt` ตามปกติ (boot job จะ ABORT เองถ้าไฟล์หาย/รูปแบบผิด)
