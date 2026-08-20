# GAME_TEST_QUEUE archive — GT-018 / GT-019 / GT-020 (ปิดครบทั้งสาม รอบใหญ่ #4-#5, 2026-08-19)

ทั้งสามรายการ **PASS ที่ชั้น client-observable** แล้ว ย้ายออกจากคิวหลักเพื่อคุมขนาดไฟล์ (ห้ามลบ)

- **GT-018** DELETE-REFRESH-001 → PASS ทุกเกณฑ์ (ตัวละครหายจริง · ปุ่มลบหายเอง · ปุ่มอื่นกลับมากดได้)
- **GT-019** HP-DEATH-002 → PASS **หลังถูกแก้จาก FAIL** (ผู้เทสคร่อมหน้าต่าง 6 วิ · Panya เห็นเอง ·
  รอบใหญ่ #5 ถ่ายภาพยืนยัน + ยิงสวีป 8 ครั้งครบทุกครั้ง) · ผู้สืบทอด = **GT-021**
- **GT-020** MP-OPT1-B → PASS (wstring "AB" บนสายตรงคำทำนายทุกไบต์ · G8 ปิด)

รายละเอียดผลเต็มอยู่ใน `CHIEF_CONTINUATION.md` รอบ 83 และใน
`notes_to_chief\consumed\20260819_0315_biground4-results.md`,
`..._0325_CORRECTION-gt019-is-PASS.md`, `..._0405_biground5-*.md`

---

## GT-018 DELETE-REFRESH-001: ตอบคำสั่งลบด้วย SelectActorVital rebuild แล้ว list หายจริงไหม  [🟢 PENDING — ปลดบล็อกแล้วรอบ 81 พร้อมรันทันที]

> ✅ **ปลดบล็อกรอบ 81:** encoder เสร็จแล้ว = `HYP-PF-021` · `src\pirateforce_foundation\delete_refresh_hypothesis.py`
> · scenario `scenarios\delete_refresh_hypothesis_list_rebuild.json` · verifier `tools\verify_delete_refresh_static.py` (45 guards)
> · headless proof `tools\pf_delete_refresh001_headless_replay.py` (บูต server จริงบน scratch DB)
>
> **server args ที่ต้องใช้:** `--delete-refresh-hypothesis-scenario scenarios\delete_refresh_hypothesis_list_rebuild.json`
> (ต้องมี `--db` ด้วย · flag นี้ exclusive กับทุกโหมด รวมถึง `--delete-actor-hypothesis-scenario` เดิม)
>
> **สิ่งที่จะเห็นบนสาย:** ตอบ delete op-1 **2 เฟรม** — ack เดิมของ HYP-PF-015 ที่ **ไม่ถูกแก้เลย** (44 B)
> แล้ว `SelectActorVital 0x36EF` v10 ตามมาที่ **+0.35 วิ** (ช่องว่างเดิมของ login → character_list ไม่ใช่เลขใหม่)
>
> ⭐ **คำทำนายที่แรงขึ้นจากรอบ 81:** ลูกมือกลับไปสแกนไบนารีเองแทนที่จะเชื่อ scan ของรอบ 80 แล้วเจอ
> **writer ตัวที่ 21 ของ page variable `0x107A2C0`** ที่ scan แบบ immediate-only มองไม่เห็น —
> `0x4BD650: mov [0x107A2C0], edi` (edi=0 จาก `xor edi,edi` @`0x4BD620` ไม่มี branch คั่น)
> ซึ่งอยู่ใน **vtable `0xF16520` slot `+0x10` ของ `cStateCreateActor`** = enter hook
> ⇒ คำทำนายเปลี่ยนจาก "list เปลี่ยน" เป็น **"list เปลี่ยน + ปุ่มกลับมากดได้"**
> · **แต่ยังเป็นการต่อโซ่ข้อเท็จจริง ไม่ใช่การสังเกต** — ค่า live ของ `0x107A2C0` ตอน GT-011 ไม่เคยถูกอ่าน

- **ที่มา:** UI-REFRESH-001 (รอบ 80) พิสูจน์ว่า ack ของคำสั่งลบ **ไม่มีทาง** เอาแถวออกจาก list ได้
  (ไม่มี erase-by-key ในไบนารี) · เส้นทางเดียวที่ rebuild ได้คือ **SelectActorVital 0x36EF**
  ซึ่ง reset+refill collection แล้วสร้าง `cStateCreateActor` ใหม่ + RequestNext
- **prerequisite (รอบ 81 ของ chief — pre-approved ตามนโยบายข้อ 4 "ปุ่ม/ฟังก์ชันที่พบใหม่"):**
  hypothesis ใหม่ `HYP-PF-021` + opt-in scenario ที่หลังจาก soft-delete commit แล้ว **ส่ง
  SelectActorVital rebuild** (list ที่ไม่มีแถวที่ถูกลบ) ตามหลัง ack เดิม · pattern มาตรฐาน:
  opt-in · `production_allowed=false` · fail closed · ledger/verifier/matrix ครบ · headless proof ก่อน
  ⚠️ **ไม่ใช่การแก้ HYP-PF-015** — scope เดิมเขียนไว้ชัดว่า "no claim about refresh behavior"
  ⇒ นี่คือ **lane ใหม่** ไม่ใช่การรื้อของที่พิสูจน์แล้ว
- objective (claim เดียว — ชั้น client-observable): หลังยืนยันลบ **ตัวละครหายจาก list จริงไหม
  โดยไม่มี error dialog** และ **ปุ่มอื่นบนหน้าจอยังกดได้ไหม**
- steps: เหมือน GT-011 ทุกข้อ (ปุ่มลบ = ปุ่มแรกซ้ายสุด → dialog → password pad → พิมพ์ `test`)
  แต่ HEAD ต้องมี DELETE-REFRESH-001 และ boot ด้วย scenario ใหม่
- pass criteria (แยกชั้น):
  - **client-observable:** ไม่มี error dialog + แถวหายจาก list + ปุ่มอื่นยังตอบสนอง
  - **wire-DB:** marker soft-delete เดิม + frame SelectActorVital rebuild ปรากฏใน GAME_LIVE ·
    canonical sha ไม่เปลี่ยน (ใช้สำเนา)
- nonclaims: ไม่ claim ว่า server ต้นฉบับตอบแบบนี้ (ไม่มี golden) · ไม่ claim semantics ของ
  field `+0x14` · ไม่ claim ว่าส่ง SelectActorVital ตอนอยู่ใน StateRunTime แล้วรอด (คนละคำถาม)
- 🩹 **ถ้า FAIL:** ทางสำรองที่ **ถูกกว่าและไม่ชนอะไรเลย** = probe `+0x14 ∈ {3,4}` พร้อม `+0x18`
  ไม่เป็นศูนย์ เพื่อดูว่า countdown board (`record+0xF4`) ขึ้นจอไหม — ยืนยันว่าเราอ่าน field ถูก
- result: (ผู้เทสกรอก)

---

## GT-019 HP-DEATH-002: ส่ง BasicAttr ที่ HP=0 แล้วตัวละครตายบนจอจริงไหม  [🟢 PENDING — ปลดบล็อกแล้วรอบ 81 พร้อมรันทันที]

> ✅ **ปลดบล็อกรอบ 81:** encoder เสร็จแล้ว = `HYP-PF-022` (เปิดใหม่ **ไม่ amend HYP-PF-020**)
> · scenario `scenarios\hp_death_hypothesis_death_sweep.json` · verifier `tools\verify_hp_death_encoder.py` (66 guards พร้อม binary)
> · headless proof `tools\pf_hp_death002_headless_replay.py` (33 guards, in-process ไม่ใช้ socket)
>
> **server args:** `--hp-death-hypothesis-scenario scenarios\hp_death_hypothesis_death_sweep.json` (ต้องมี `--db`, exclusive ทุกโหมด)
> **ทริกเกอร์:** ผู้เล่นพิมพ์แชต 1 ครั้งหลัง runtime ready → ได้ **4 เฟรม ห่างกัน 6.0 วิ**
>
> **สิ่งที่ต้องดูทีละเฟรม (สำคัญ — เฟรม 2 คือ control ของเทสนี้):**
> | เฟรม | mask | สิ่งที่ควรเห็น |
> |---|---|---|
> | 1 BASELINE | `0x030C` | ปกติ — body **ตรงกับ pin ของ HYP-PF-020 ทุกไบต์** |
> | 2 TIMER_ARMED | `0x038C` | **ต้องไม่มีอะไรเกิดขึ้น** (timer 60.0f มาแล้ว แต่ HP ยัง 100) |
> | 3 HP_ZERO | `0x038C` | หลอด HP หมด + หน้าต่าง `Main_Dead` เปิด |
> | 4 HP_RESTORED | `0x038C` | หน้าต่างปิด ตัวละครกลับมา |
>
> 🔴 **อย่ารอท่าตาย `_F_DIE_000`** — รอบ 81 ไล่ chain จนจบแล้ว (ปิดหนี้ B1 พร้อมแก้คำตอบเดิม):
> ทางจริงคือ `UpdateAttrVital 0x5F2400` → `vtable+0x10` ของ Attr ที่เข้ามา (`0x464E40` อ่าน **class id ไม่ใช่ identity**)
> → lookup `[0x1032EC4]+0x130` ที่ `0x5F24C9` → `vtable+0x24` ที่ `0x5F2504` → `0x464F30` → `0x464B40`
> ซึ่ง **copy ทั้งบล็อกโดยไม่ดู mask** · **ไม่ใช่ `0x4446F0`** ซึ่ง caller เดียวของมัน (`0x4566A7`) เข้าไม่ถึงจากท่อนี้
> ⇒ ท่อนี้ให้ **Main_Dead + HUD เท่านั้น ไม่มี death animation ไม่มี `TargetIsDead` latch**
>
> ⚠️ **ความเสี่ยงเดียวที่รู้ล่วงหน้า:** `Main_Dead` มี gate ที่สองที่ `0x44A572` ต้องการ `timer >= DURATION_DYING - 0.5`
> โดย `DURATION_DYING` = int ที่ `0x102249C` (ผูกกับ literal ที่ `0x48346A`) **ค่าใน image = 20**
> scenario ส่ง `60.0f` = **การเลือกเผื่อไว้ ไม่ใช่ค่าที่พิสูจน์** เพราะค่าที่ deploy จริงไม่รู้
> ⇒ ถ้าเห็น **หลอด HP ว่างแต่หน้าต่างไม่เปิด** = แปลว่า DURATION_DYING จริง > 60.5 **ไม่ใช่ FAIL ของ encoder** ให้จดแล้วรายงาน

- **ที่มา:** HP-DEATH-001 (รอบ 80) พิสูจน์ว่า **client รู้จักความตายเอง ไม่มี "เฟรมตาย" ให้หา** ·
  `IsDead` (vtable `+0x40`) ของทุกคลาส = ดึง Attr ผ่าน vtable `+0x74` แล้วคืน **current HP == 0**
  โดยอ่าน `BasicAttr +0x44` (mask bit `0x0004`) ใต้ gate ที่ต้องมี f32 `+0x58` (bit `0x0080`) `> 0`
  · max HP = `+0x48` (bit `0x0008`) พิสูจน์ current-vs-max ด้วย HUD bar helper `0x53EED0`
  · **chief แกะซ้ำเองจาก process สะอาด ตรงทุก instruction**
- ⇒ **ระยะห่างระหว่าง server เรากับ "ฆ่าตัวละครได้" = 1 mask bit + 1 float** (bit `0x0080` ตอนนี้ไม่เคย emit)
- **prerequisite (รอบ 81 — pre-approved):** `HP-DEATH-002` = ขยาย encoder mask-driven ที่มีอยู่แล้ว
  (`stats_progression_hypothesis.py` รองรับ 23 ฟิลด์) ให้ emit bit `0x0004`=0 + bit `0x0080`>0
  ผ่าน opt-in scenario · headless proof ถึงชั้น dispatcher ก่อน
- objective (claim เดียว — client-observable): เมื่อ server ส่งเฟรมนั้น **ตัวละครบนจอเข้าสถานะตาย
  จริงไหม** (animation `_F_DIE_000` / หน้าต่าง `Main_Dead` / หลอด HP ว่าง)
- pass criteria:
  - **client-observable:** เห็นอย่างน้อย 1 ใน 3 อย่างข้างบน + ไม่มี error dialog
  - **wire-DB:** frame ออกจริงใน GAME_LIVE · ไม่มีการเขียน DB (lane นี้ `database_write=none`)
- ⭐ **เทสนี้ปิดหนี้ B1 ของ HP-DEATH-001** = "UpdateAttrVital ตัวเดียว latch ธง dead ได้ไหม"
  ซึ่งตอนนี้เป็นแค่ ②อนุมานเชิงโครงสร้าง — เป็นของถูกที่สุดที่ทำให้มันเป็น ①byte/runtime-proven
- nonclaims: **ไม่ claim damage model ใด ๆ** (HP ไปถึง 0 ได้ยังไง = คนละเรื่อง ยังไม่แตะ) ·
  ไม่ claim respawn (ReliveVital `0x1AD4` เป็น 1 ใน 69 คลาสที่ inbound slot = no-op `0x710440`
  ⇒ echo กลับไปไม่มีผล) · ไม่ claim บทลงโทษ (`n_DEADLOSS` เป็นข้อมูลนอก executable)
- result: (ผู้เทสกรอก)

---

## GT-020 MP-OPT1-B: login ด้วยบัญชีอื่น — client ยังเข้าเกมได้ไหมเมื่อ field บัญชีเปลี่ยน  [🟢 PENDING — พร้อมรันทันที ไม่มี prerequisite]

- **ที่มา:** MP-OPT1-B (รอบ 81) ตอบ **G8** ของ MULTIPLAYER-READINESS-AUDIT-001 ครบระดับ static แล้ว
  · รายงาน `reports\PF_MPOPT1B_LOGIN_VITAL_REQ_0X42BF_STATIC_20260819.md` · verifier `tools\pf_login_vital_req_static.py` (126 guards)
  · **สเปกฉบับเต็มพร้อมตารางไบต์ทุกเฟส:** `pf_bridge\drafts\GT_DRAFT_MPOPT1B_LOGIN_USERNAME_20260819.md`
- **ไม่มี hypothesis ไม่แตะ `src/` ไม่ต้อง encoder ไม่ต้องใส่ scenario ใด ๆ**

### สิ่งที่ static พิสูจน์ไปแล้ว (จึงเหลือให้เทสน้อยกว่าที่ audit เขียนไว้)
`0x42BF` มี **2 field เท่านั้น** — `wstring @+0x14` (tag `0x48`) = **บัญชี** · `string @+0x30` (tag `0x44`) = **รหัสผ่าน cleartext**
ซึ่ง field ไหนคืออะไร **พิสูจน์จากจุด assign** (`cStateLogin::DoLogin 0x4C5920` ที่ `0x4C5A61..0x4C5A73`) ไม่ใช่จากตำแหน่ง
· client **hex-decode ค่าของ `-acc`** ผ่าน `0x89B070` (มี call site เดียวทั้งอิมเมจ) ก่อนใส่ลงเฟรม
⇒ `-acc test` ให้ `U+000E U+0000` = ไบต์ `0E 00 00 00` **ที่ capture ทั้ง 63 ไฟล์เห็นมาตลอด**
**ไม่ใช่เพราะ field เป็นค่าคงที่ แต่เพราะเราส่ง argument เดิมทุกครั้ง** — G8 ตอบแล้ว: **เป็นตัวแปรจริง**

🔴 **ห้ามพิมพ์ชื่อบัญชีตรง ๆ ใน `-acc`** — `-acc bob` จะกลายเป็นขยะบนสาย ต้องใส่ **hex ของชื่อ** (2 หลัก/ตัวอักษร)

- objective (claim เดียว — **ชั้น client-observable**): เปลี่ยน `-acc`/`-pwd` แล้ว **client ยัง login เข้าเกมได้ตามปกติไหม**
  (ไม่มี error dialog / ไม่ค้าง) — ชั้น wire เป็นแค่การยืนยันซ้ำว่าไบต์เปลี่ยนตามที่ทำนาย
- **prerequisite: ไม่มี · ❌ ไม่ต้องเตรียมบัญชีในฐานข้อมูล** — ตรวจ `src/` แล้ว server **ไม่เคยอ่าน field บัญชีจากสาย**
  (v141 ตอบ `0x42BF` ด้วย nested id อย่างเดียว ไม่มี parser ของ payload) ชื่อบัญชีที่ persist มาจาก `--token` (default `localtest`)
  ⇒ **DB จะไม่เปลี่ยนตามชื่อที่ client ส่ง และนั่นคือผลที่ถูกต้อง** (ดู nonclaims)
- db: สำเนาสดของ canonical (`state\pirateforce_gt020_<stamp>.sqlite3`) · server args: `--second-password-mode bypass` · `--capture-root "<GameClient>\capture_gt020_<stamp>"`

### client args (หัวใจของเทส — job ทุกตัวที่ผ่านมาใช้ `-acc test -pwd test`)

| เฟส | args | บัญชีบนสายจริง | รหัสผ่านบนสาย |
|---|---|---|---|
| **A** (ทำก่อนเสมอ) | `-acc 4142 -pwd test` | `AB` | `test` |
| **B** | `-acc 6D70746573743032 -pwd mppass02` | `mptest02` | `mppass02` |

**A ออกแบบให้เสี่ยงต่ำสุด:** ความยาวเฟรม**เท่าเดิมเป๊ะ** เปลี่ยนแค่ **2 ไบต์** ไม่แตะรหัสผ่าน ⇒ พังเมื่อไหร่รู้ทันทีว่ามาจาก field เดียว
**B** เปลี่ยนทั้งค่าและความยาวของทั้งสอง field ⇒ พิสูจน์ length prefix เป็นตัวแปรด้วย
· **ถ้า A ไม่ผ่าน ให้หยุด รายงาน ไม่ต้องทำ B**

### ไบต์ที่ทำนายล่วงหน้า (grep ได้ตรง ๆ ใน `capture_gt020_*\LOGIN_*.txt` ใต้บล็อก `DECOMPRESSED`)

```
ปัจจุบัน (-acc test)  12 BF 42 0B 00 48 04 00 00 00 0E 00 00 00 44 04 00 00 00 74 65 73 74
เฟส A   (-acc 4142)  12 BF 42 0B 00 48 04 00 00 00 41 00 42 00 44 04 00 00 00 74 65 73 74
เฟส B   (-acc 6D70…) 12 BF 42 0B 00 48 10 00 00 00 6D 00 70 00 74 00 65 00 73 00 74 00 30 00 32 00
                                       44 08 00 00 00 6D 70 70 61 73 73 30 32
```
(คอลัมน์ ASCII ของ hexdump จะอ่านได้เป็น `.A.B.` และ `.m.p.t.e.s.t.0.2` ตรง ๆ)

- 🔴 **ความเสี่ยงที่รู้ล่วงหน้า — อ่านก่อนรัน ไม่ใช่หลังพัง:** `v141.make_game_login_ack` แช่ literal
  `b"\x0B\x68\x48\x04\x00\x00\x00\x0E\x00\x00\x00"` = **บัญชีของ `-acc test` ตัวเก่า**
  ⇒ server จะ **echo บัญชีเก่ากลับไป** · static ไม่พบ compare ใด ๆ ในไบนารี จึงคาดว่า client ไม่สนใจ
  · **ถ้า client เด้ง error ตรงนี้ = ผลบวกที่มีค่ามาก** แปลว่ามัน compare จริง → **จดเป็น observation แล้วจบเทส
  ห้ามแก้ `src/` หรือ v141 ในเซสชันเทส** · จุดสังเกต: ถ้าเข้าหน้าเลือกตัวละครได้ = ผ่านจุดนี้แล้ว
- steps: ตาม PLAYBOOK ข้อ 1–8 · boot job ลอกจาก `staged\072_gt001_boot.ps1` **แก้แค่ป้าย log · captureRoot ·
  ชื่อ run DB · และ `-ArgumentList` ของ client** · client รอบสอง (เฟส B) ลอกจาก `done\068_gt002_reconnect_client.ps1`
  บน **server ตัวเดิมที่ยังรันอยู่** · เฟส B **หยุดที่หน้าเลือกตัวละคร ไม่ต้องเข้าแมพ**
  · ⚠️ ปุ่มแรกซ้ายสุดในหน้าเลือกตัวละคร = **ลบตัวละคร ห้ามกด** · ปุ่มกลางสุด = เข้าเกม
- pass criteria (แยกชั้น):
  - **client-observable (claim ของเทสนี้):** เฟส A เข้าแมพได้ครบ (HP bar + minimap + ชื่อแมพ + chat `online`) ไม่มี error dialog ไม่ค้าง ออกสะอาด
    · เฟส B เห็นหน้าเลือกตัวละครพร้อม nameboard ไม่มี error dialog
  - **wire-DB (ยืนยันซ้ำ):** `LOGIN_*.txt` ของแต่ละเฟสตรงกับตารางไบต์ข้างบน**ทุกไบต์** · `GAME_*.txt` มี `LoginVerifyVital` ขึ้นต้นด้วย prefix ที่ทำนาย
    · **canonical sha ไม่เปลี่ยน** · `stopped ×1` · `stderr 0B` · `listeners 0` หลัง teardown
    · `sessions` ของสำเนา **+2** และ `accounts.login_name` **ยังเป็น `localtest`** ← ค่าที่ "ไม่เปลี่ยน" นี้คือผลที่ถูก
- nonclaims:
  - ❌ **ไม่ claim ว่า DB แยกบัญชีได้** — ถ้าเห็นแถวใหม่ชื่อ `AB`/`mptest02` แปลว่า**มีอย่างอื่นผิด** ไม่ใช่สำเร็จเกินคาด
  - ❌ ไม่ claim ว่า server ต้นฉบับ validate อย่างไร (ต้นฉบับปิดไปแล้วและไม่เคย publish)
  - ❌ ไม่ claim อะไรกับ `LSCN_LoginVitalRes 0x42E3` · ❌ ไม่ claim two-client/concurrent (ยัง serial)
  - ❌ ไม่ claim ว่า `-pwd` ถูกตรวจที่ใด — พิสูจน์แค่ว่ามันไปถึงสายเป็น **cleartext**
  - ❌ **ไม่เปิด Option 2/3 จากผลนี้** — Panya อนุมัติแค่ "ลำดับ" ยังไม่อนุมัติงบของ 2/3
- 🩹 **ถ้า FAIL ที่เฟส A:** รันซ้ำด้วย `-acc 74657374 -pwd test` (บัญชี = `L"test"` ชื่อเดิม แต่ไบต์ยาว 8 ไม่ใช่ 4)
  เพื่อแยกว่าปัญหาคือ *ค่าของบัญชี* หรือ *ความยาวของ field*
- result: (ผู้เทสกรอก)

---
