# GAME TEST QUEUE ARCHIVE — รอบใหญ่ #3 (ปิดแล้ว) · ย้ายโดย chief รอบ 78 (2026-08-18 ~18:2x)

> เทส 4 รายการนี้ **ได้ผลชี้ขาดแล้ว**ในรอบใหญ่ #3 (17:01–17:47) จึงย้ายออกจากคิวหลัก
> ผลย่อยังอยู่ใน `GAME_TEST_QUEUE.md` เป็น pointer · เนื้อหาเต็มของผลอยู่ที่
> `pf_bridge\notes_to_chief\consumed\20260818_1745_biground3-results.md`
> และสรุปเชิงสถาปัตยกรรมอยู่ใน `CHIEF_CONTINUATION.md` รอบ 78 · **ห้ามลบไฟล์นี้**

---

## GT-012 CHAT-ECHO-002: client render ชื่อผู้พูดใน chat echo แบบ speaker-wstring ไหม  [✅ PASS — รอบใหญ่ #3 17:1x]

> ✅ **RESULT รอบใหญ่ #3 (17:1x, jobs 104/105) — PASS ทุกเกณฑ์ · ผลเต็ม: `pf_bridge\notes_to_chief\consumed\20260818_1745_biground3-results.md`**
> - เรนเดอร์จริงบนจอ: **`[ทั่วไป] Arena01: PFCHATPROBE1`** — รูปแบบเป๊ะ `[ทั่วไป]`+space+ชื่อ+`:`+space+ข้อความ (ไม่มี space ก่อน `:`)
> - `PFCHATPROBE2` เรนเดอร์ครบเหมือนกัน = **ไม่ใช่ one-shot** · `SHORT` (5 ตัว) **เงียบสนิทไม่มี error** = fail-closed ยืนยันที่ชั้น UI
> - ไม่ crash ไม่หลุดแมพ ไม่ desync · 🟢 label ที่เห็นจริง `[ทั่วไป]` **ยืนยัน prediction ของ CHAT-ECHO-005/006/007 (id 540 path)**
> - ⇒ **HYP-PF-014 v2 ผ่าน client acceptance** — ชื่อผู้พูดเรนเดอร์จาก wstring#1 จริง

- objective: (claim เดียว — ชั้น client-observable) ทำ GT-009 ซ้ำด้วย scenario speaker variant
  (HYP-PF-014 v2, landed รอบ 53): พิมพ์ข้อความ ASCII 12 ตัว →
  **ข้อความ render พร้อมชื่อตัวละครหน้า `:` (คาด `[ทั่วไป] <ชื่อ>: <ข้อความ>`) ไหม?**
  จดรูปแบบช่องว่างรอบ `:` เป๊ะ ๆ (research ยังเปิดไว้) · ชั้น wire พิสูจน์แล้ว headless
  (`reports/PF_CHAT_ECHO003_SPEAKER_WSTRING_VARIANT_HEADLESS_20260818.md` — echo 68B PC /
  79B frame มีชื่อใน wstring#1) — **อย่านับชั้น wire เป็นเกณฑ์**
- db: สำเนา canonical สด (104 copy + เช็ค sha `B5557E9F..C9ED` — ถ้า LOCK ล่าสุดบอก sha ใหม่
  ให้แก้ `$expectedSha` ใน 104 ก่อน) · canonical ต้องไม่ขยับ
- server args: (104 จัดให้ครบ) `--chat-input-hypothesis-scenario
  scenarios\chat_input_hypothesis_speaker_echo.json`
- ⚠️ mutually exclusive: logout ack ไม่ทำงานรอบนี้ → ออกเกมด้วย **End task เท่านั้น**
- steps:
  1. run staged `done\104_gt012_boot.ps1` → login → เลือกตัวละคร → เข้าแมพ (PLAYBOOK 3–6)
     **จดชื่อตัวละครที่เห็นบน nameboard ไว้ก่อน** (ชื่อนี้คือค่าที่ server จะเติม)
  2. คลิกกล่องแชท พิมพ์ `PFCHATPROBE1` (12 ตัวพอดี) + Enter → สังเกตบรรทัดที่ render:
     มีชื่อตัวละครไหม? รูปแบบเป๊ะ ๆ อย่างไร (ถ่าย/จดทุกตัวอักษรรวมช่องว่าง)
  3. พิมพ์ `PFCHATPROBE2` + Enter ซ้ำ (ยืนยันไม่ one-shot)
  4. พิมพ์ `SHORT` + Enter (5 ตัว) → ต้องเงียบเหมือน GT-009 (UI fail-closed เดิม)
  5. ออกด้วย **End task** → run staged `done\105_gt012_teardown.ps1`
- pass criteria (แยกชั้น):
  - **client-observable (เทสนี้):** ข้อความ 12 ตัว render พร้อมชื่อตัวละครในตำแหน่งผู้พูด
    ทั้งสองครั้ง ไม่ desync/ไม่ error dialog + SHORT เงียบ
  - **wire-DB (ยืนยันซ้ำผ่าน 105):** marker `HYP_PF_014_CHAT_INPUT_SPEAKER_ECHO_ASCII12`
    ใน GAME_LIVE · echo frame = **79B** (ชื่อ 6 ตัว; สูตร = 66+2×len(ชื่อ)+1 เมื่อ pc>60) ·
    DB ไม่มี write · canonical sha ไม่เปลี่ยน
- 🟢 **static pre-check รอบ 54 (CHAT-ECHO-004, `reports/PF_CHAT_ECHO004_LOCALTALK_HANDLER_STATIC_20260818.md`):**
  disassembly ยืนยัน Grade A ว่า **field#1 = length-prefixed tag-0x48 wstring** (deserialize
  0x65AD40 อ่าน field#1@obj+0x34 ด้วย reader 0x89A880 ตัวเดียวกับ text) → การออกแบบ speaker
  variant "ถูกโครง" ระดับ parse แน่นอน · **counter-hypothesis candidate 3 (field#1=u32 actor id)
  ถูก falsify แล้ว static** — ดังนั้นถ้า render เพี้ยน/ตัดข้อความ **อย่าสรุปว่า "field#1 อ่านเป็น u32"**
  ให้จดอาการดิบ ๆ ไว้เฉย ๆ (เหตุผลอื่น เช่น client ต้องการ identity binding จริงก่อน format ชื่อ) ·
  tag `[ทั่วไป]` = identity/vital-id-driven ไม่มี field บน payload → คาดว่าโผล่เสมอไม่ว่าชื่อจะว่างหรือไม่
- 🟢 **static pre-check รอบ 55 (CHAT-ECHO-005, `reports/PF_CHAT_ECHO005_LOCALTALK_RENDER_TAG_GATE_STATIC_20260818.md`):**
  pin gate ของ render channel label แล้ว — บรรทัดแชทจะขึ้น id 540 `[ทั่วไป]` เมื่อ message object
  เป็นชนิด is-a type-node 0x1083FA8 ∧ byte +0x45==0 ∧ +0x44!=0 (ถ้า +0x44==0 จะเป็น id 539 อีก label)
  → **ตอนเทสให้จดว่า label ที่ขึ้นจริงคือ `[ทั่วไป]` หรือ label อื่น** (ยืนยัน/หักล้าง prediction 540) ·
  ยัง Grade B ที่ single-SET (parent-chain runtime-built ปิด static ไม่ได้) — ผล client-observable รอบใหญ่
  = หลักฐานตรงที่สุดที่จะดัน B→A
- 🟢 **static pre-check รอบ 56 (CHAT-ECHO-006, `reports/PF_CHAT_ECHO006_LOCALTALK_CTOR_TAG_INIT_STATIC_20260818.md`):**
  พบ constructor ของคลาส message ตัวจริง (target `0x6425D0` ติดตั้ง vtable `0xF3640C`; sibling `0x642540`)
  → constructor **zero-init `+0x44` (และ sibling zero `+0x45` ด้วย) ด้วย immediate 0** = ค่าตั้งต้น `+0x44==0`
  → **default render = id 539** ; การได้ `540 [ทั่วไป]` (`+0x44!=0`) ต้องมี write nonzero ทีหลังตอน parse (runtime) ·
  **prediction ปรับให้ชัด:** ถ้า echo speaker variant ทำงานถูก คาดว่าบรรทัดขึ้น `[ทั่วไป]` (id 540) เพราะ populate
  path เขียน `+0x44` nonzero — **ถ้าเห็น label อื่น/ค่าตั้งต้น ให้จดดิบ ๆ** (อาจแปลว่า populate ไม่ยิงในเส้นนี้) ·
  ยัง Grade B (ยังไม่ pin static ว่า nonzero-write มาจาก message identity) → ผลรอบใหญ่ยังเป็นตัวชี้ขาด B→A
- 🟢 **static pre-check รอบ 57 (CHAT-ECHO-007, `reports/PF_CHAT_ECHO007_LOCALTALK_TAG_PERCLASS_CONST_STATIC_20260818.md`) — แก้/คมกว่ารอบ 56:**
  พบว่า `+0x44` **ไม่ใช่ค่าที่ populate เขียนตอน runtime** แต่เป็น **per-class immediate constant ในตัว constructor**
  (cohort: `0xf35c2c→0x0c`, `0xf35cb0→7`, `0xf35cdc→4`, `0xf35d8c→3`, `0xf35db8→1`, `0xf35e10→6`, `0xf36490→5`, และคู่ target/sibling `0xf3640c/0xf363e0→0`)
  → คลาสที่ render `540 [ทั่วไป]` = **คนละคลาสที่ bake `+0x44` nonzero** ; ไม่มี wire path ไป `+0x44` เลย
  → **prediction ชี้ขาด (binary observable):** ถ้าบรรทัด LocalTalk ขึ้น `[ทั่วไป]` (id 540) ⇒ คลาสของมันมี `+0x44`∈{1,3,4,5,6,7,0xc} ;
  ถ้าขึ้น id 539 ⇒ `+0x44`==0 · **จดค่า label ที่ขึ้นจริง** — ผลนี้ pin binding `0xAC52→คลาส→constant` ที่ static ทำไม่ได้
  (registry key เป็น hash รัน startup) = **ปิด B→A จบในรอบใหญ่**
- 🟢 **static pre-check รอบ 60 (CHAT-ECHO-008, `reports/PF_CHAT_ECHO008_LOCALTALK_COHORT_VTABLE_NAME_MAP_STATIC_20260818.md`) — เพิ่มชื่อคลาสจริง:**
  map cohort ครบ: vtable → get-id (col+0x10, `mov ax,[id-slot]`) → id-slot → **plaintext class name** (ตระกูล `Community_*Vital`) พร้อม `+0x44`:
  `AddFriend=0xc`, `AddBlackList=7`, `RemoveBlackList=4`, `ChangeActorComment=3`, `SetReceiveActiveChange=1`, `ThrowLetterInABottle=6`, `ChangeActorPenName=5` → **540 `[ทั่วไป]`** ;
  `RequestBeFriend`, `RequestorConfirmSoulMateMatch`, `TargetConfirmSoulMateMatch` (`+0x44`==0) → **539** ·
  ⚠️ cohort นี้ = Community family **ไม่ใช่ LocalTalk เอง** (0xAC52 คนละ registration) — render gate 539/540 shared · **id ตัวเลข 16-bit = runtime-assigned** (.data slot ในอิมเมจเป็น filler) จึงยังต้องสังเกต runtime · **ค่า label ที่ผู้เทสจดได้ = หลักฐานชี้ขาดตัวเดียวที่จะ pin `0xAC52→คลาส`**
  — 🟢 **อัปเดตรอบ 62 (commit `7c66b21`, NAMEID-HASH-001):** id 16-bit = **hash บริสุทธิ์ของชื่อคลาส** (`Σ_i (signed char)name[i]*(i+1) mod 2^16` @`0x89b220`) → pin **`0xAC52 → Channel_LocalTalkMessageVital` ได้ static แล้ว** (literal→slot 0x1084458→0xAC52 byte-exact); "runtime-assigned" = แค่ deferred init ของ hash ไม่ใช่ external · **แต่ render-tag 539/540 (+0x44) เป็นกลไกคนละตัว** ยังต้องอาศัย label ที่ผู้เทสจด — nonclaim นี้คงเดิม
- nonclaims: ไม่ claim ชื่อไทย/ข้อความไทย/ความยาวอื่น · static ปิดแค่ชั้น parse ของ field#1
  (ไม่ได้พิสูจน์ว่า client จะ *แสดง* ชื่อบนจอ = ยังเป็น claim ของเทสนี้) · ไม่ claim delivery
  ไป client อื่น/persistence · ไม่ claim ว่า server เดิมตอบแบบนี้ (ไม่มี golden)
- result: (ผู้เทสกรอก)

---

## GT-013 HYP-PF-016: 0x3D4B-first response ทำให้ client ออกจากแมพจริงไหม  [❌ FAIL — รอบใหญ่ #3 17:29 · shape ที่ 3 ถูก falsify]

> ❌ **RESULT รอบใหญ่ #3 (17:29, jobs 106/107) — FAIL · shape ที่ 3 ถูก falsify · ผลเต็ม: `pf_bridge\notes_to_chief\consumed\20260818_1745_biground3-results.md`**
> - **subcode 03** (กลับหน้าเลือกตัวละคร): dialog ปิด → **ไม่ transition** ยังอยู่ในแมพครบ 15+ วิ · ไม่มี error dialog · UI ยังตอบสนอง (เปิดเมนู HOME ซ้ำได้)
> - **subcode 01** (ออกเกม): **ไม่ปิดตัวเอง** เช่นกัน — ⚠️ **nonclaim: confounded** เพราะทำต่อจาก 03 ในเซสชันเดียวกัน socket อาจปิดไปแล้ว → **ต้องเทสใหม่ในเซสชันสดถ้าจะสรุป**
> - wire ถูกครบตามดีไซน์: `..._SUBCODE03_WORLDINFO_RESPONSE_FIRST` **283B** (late 1.2ms) → `..._SUBCODE03_ACK_THEN_SERVER_SOCKET_CLOSE` **46B** (late 49.9ms) · open sessions = 0
> - ⇒ **shape 1 (echo) · shape 2 (ack+close) · shape 3 (worldinfo-first) ถูก falsify ที่ชั้น client ครบทั้งสาม**

- objective: (claim เดียว — ชั้น client-observable) logout ที่ตอบแบบ response-first
  (echo 0x3D4B 248B ที่ client ส่งเองตอนเปิด dialog → ack PF-012 เดิม → close +250ms):
  **client transition จริงไหม — subcode 03 กลับหน้าเลือกตัวละคร / subcode 01 ปิดตัวเอง?**
  (GT-007 echo-only และ GT-008 ack+close ถูก falsify ไปแล้วทั้งคู่ — นี่คือ shape แรกที่มี
  content-bearing response) · ชั้น wire พิสูจน์แล้ว headless
  (`reports/PF_LOGOUT_RESP001_HYP_PF_016_WORLDINFO_FIRST_HEADLESS_20260818.md`) —
  **อย่านับชั้น wire เป็นเกณฑ์**
- db: สำเนา canonical สด (106 copy + เช็ค sha `B5557E9F..C9ED` — แก้ตาม LOCK ถ้าเปลี่ยน) ·
  canonical ต้องไม่ขยับ
- server args: (106 จัดให้ครบ) `--logout-hypothesis-scenario
  scenarios\logout_hypothesis_worldinfo_first.json` (console ต้องเขียน policy worldinfo_first)
- ⚠️ ลำดับแนะนำ: ลอง **subcode 03 ก่อน** (กลับหน้าเลือกตัวละคร — ถ้า client ค้าง/desync
  ยังเก็บหลักฐานได้โดยไม่เสีย run) แล้วค่อย subcode 01 (ออกเกม) เป็นเฟรมสุดท้าย
- steps:
  1. run staged `done\106_gt013_boot.ps1` → login → เลือก → เข้าแมพ (PLAYBOOK 3–6)
  2. เปิดเมนูระบบ (X มุมขวาบน **ครั้งเดียว** — client จะยิง 0x3D4B เต็มตอน dialog เปิด;
     server เก็บเงียบ ๆ ไม่ตอบ = ปกติ) → เลือกปุ่ม **กลับหน้าเลือกตัวละคร** (subcode 03)
  3. สังเกต ~15 วิ: จอเปลี่ยนไปหน้าเลือกตัวละคร? หรือ dialog error? หรือค้างในแมพ
     แบบ GT-008? จดทุกจังหวะ + เวลา (วินาที) — **ถ้าเจอ GSCN error dialog จดเลข ErrorData
     เป๊ะ ๆ** (เลขนี้ = ข้อมูลออกแบบรอบถัดไป เหมือน 28317 ของ GT-010)
  4. ⚠️ หลัง 03 socket ถูกปิดโดย server แล้ว — ถ้าหน้าเลือกตัวละครโผล่แต่กดอะไรไม่ติด
     ให้**จดว่า transition เกิด** (reconnect เป็น nonclaim) แล้ว End task
  5. ถ้า 03 ไม่ transition: End task → รัน 106 ใหม่ → เข้าแมพ → X → คราวนี้ปุ่ม**ออกเกม**
     (subcode 01) → สังเกต: client ปิดตัวเอง ~ภายใน 5 วิไหม?
  6. จบด้วย run staged `done\107_gt013_teardown.ps1` (ถ้า client ยังอยู่ teardown จะจัดการ
     และจะจดให้ว่า client ออกเองหรือไม่)
- pass criteria (แยกชั้น):
  - **client-observable (เทสนี้):** subcode 03 → เห็น transition ออกจากแมพ (หน้าเลือก
    ตัวละคร/หน้าอื่นที่ไม่ใช่แมพ) โดยไม่มี error dialog **หรือ** subcode 01 → client
    ปิดตัวเอง — สำเร็จอย่างใดอย่างหนึ่ง = PASS บางส่วน ระบุชัดว่า subcode ไหน
  - **wire-DB (ยืนยันซ้ำผ่าน 107):** GAME_LIVE มีลำดับ [283B worldinfo response →
    46B ack] marker `HYP_PF_016_LOGOUT_SUBCODE..._WORLDINFO_RESPONSE_FIRST` →
    `..._ACK_THEN_SERVER_SOCKET_CLOSE` · closed_at ใน run copy ไม่ null · canonical ไม่ขยับ
- nonclaims: ไม่ claim reconnect/re-login หลัง transition (ยังไม่มี design) · ไม่ claim
  ความหมาย float/ค่าคงที่ใน 248B (R40 nonclaim เดิม) · ไม่ claim ว่า server เดิมตอบแบบนี้
  (ไม่มี golden) · ถ้าเจอ 28317 อีก: lead แรก = การอ่าน 248B แบบ 3-element
  (0x3D4B ว่าง + 0x0F01 UpdateServerSettingVital ×2 — ดู report §เหตุผล envelope) ·
  FAIL ทั้งสอง subcode = falsify shape นี้ → chief ออกแบบ v2 (เช่น compose ต่างจาก mirror)
- result: (ผู้เทสกรอก)

---

## GT-014 MOVE-AUTHORITY-001: server เดิมเคย "ดึงกลับ" (rubber-band) ตำแหน่ง local player ไหม  [🟢 OBSERVATION เก็บครบ — รอบใหญ่ #3]

> 🟢 **RESULT รอบใหญ่ #3 — OBSERVATION เก็บครบ ไม่มี rubber-band · ผลเต็ม: `pf_bridge\notes_to_chief\consumed\20260818_1745_biground3-results.md`**
> - เดินพื้นโล่ง: `X:-8,094 Y:-3,207` → `X:-8,553 Y:-2,579` · **ชนกำแพง/โครงสร้างเรือ: หยุดที่ขอบ ไม่ทะลุ ไม่ถูกดึงกลับ ไม่ snap-back**
> - คลิกจุดที่เดินไม่ถึง: **ตัวละครไม่ขยับเลย** (client กันเองที่ pathfinding)
> - wire: `TeleportVital` = **1 บรรทัด** (echo ตอน entry เท่านั้น ตรงที่คิวสั่งเช็ค) · **`MovementAttr` server→client ระหว่างเดิน = 0** · `TargetPos` mentions = 8
> - DB `heading` = 4.532 (เฟรมสุดท้ายตอนหยุด) — sub-observation heading ยังไม่ได้เทส respawn
> - ⇒ **ตอกย้ำ client-authoritative ที่ชั้น observed** — server ปัจจุบันไม่เคยส่ง reposition ระหว่างเดิน · collision บังคับฝั่ง client ล้วน
> - **nonclaim เดิมยังยืน:** ไม่ได้บอกว่าเซิร์ฟเวอร์ต้นฉบับทำแบบไหน (ปิดไปแล้ว ไม่เคย publish)

- ที่มา: report `PF_MOVE_AUTHORITY001_..._STATIC_20260818.md` (commit `856f9e9`) พิสูจน์แล้ว
  ว่า **server ปัจจุบัน = client-authoritative เต็มตัว** (รับ TargetPosVital ดิบ ไม่ validate
  ไม่ส่ง correction) และกลไก reposition มีอยู่จริง (MovementAttr bit-0x01 = position vec3) แต่
  ไม่เคยยิงใส่ local player กลางทาง · unknown ที่เหลือ = server เดิมเคยใช้กลไกนี้กลางทางไหม
  (decoded corpus เป็น client→server ล้วน ตอบไม่ได้)
- objective: (observation — ชั้น client-observable + wire, ไม่มี claim grade; nonclaim ว่า
  server เดิมทำแบบไหน) สังเกตว่าเมื่อเดินแบบ "ผิดกติกา" client เห็น server ดึงตำแหน่งกลับ
  (rubber-band/snap) ไหม และ wire มีเฟรม server→client ที่ตั้งตำแหน่ง local player ระหว่างเดิน
- steps (ไม่ต้อง staged .ps1 ใหม่ — ใช้ boot ปกติของ full-loop / GT-001):
  1. บูต server (visible console) + GameClient เข้าแมพ Port Royal เหมือน PLAYBOOK
  2. เดินชน "กำแพง"/ขอบฉาก ค้างไว้ ~3–5 วิ → สังเกตหน้าจอ: ตัวละครทะลุ, หยุด, หรือถูก
     ดึงกลับ (snap-back)? จดพฤติกรรมที่เห็น
  3. เดินกระโดดไกลผิดปกติ (ถ้ามีทางลัด/หน้าผา) → สังเกต snap-back เช่นกัน
  4. teardown: grep `capture_v141\GAME_LIVE.txt` หาเฟรม **server→client** ที่มี MovementAttr
     (`id=0x...` + mask) ที่ actor identity = local player ระหว่างช่วงเดิน (ไม่ใช่ตอน StartGame
     scene-entry) — จดว่ามี/ไม่มี · และดูว่ามี TeleportVital server→client ระหว่างเดินไหม
- pass criteria (observation, ระบุชัดว่าเห็นอะไร):
  - **ถ้าไม่มี snap-back + wire ไม่มี server→client reposition ระหว่างเดิน** → ตอกย้ำ
    "client-authoritative" ขยายจาก server ปัจจุบันไปถึง observed behavior (ยังไม่ใช่ original
    protocol proof — nonclaim) → chief ปิด cap[2] characterization ระดับ negative-strong
  - **ถ้ามี snap-back / server→client reposition** → จับ golden ของ correction ได้ →
    chief เปิด hypothesis ถอด authority rule รอบถัดไป
- nonclaims: ไม่ claim ว่า server เดิม (ตัวจริง) มี/ไม่มี authority — เทสนี้วัด server ปัจจุบัน
  + observed client behavior เท่านั้น · ถ้าเจอ TeleportCheckVital (0x4477) ถูกส่ง จดไว้
  — **semantics ถอดแล้วรอบ 61 (commit `96b76fe`, TELEPORT-CHECK-001):** ไม่ใช่ movement-correction
  แต่เป็น **UI confirm-callback ack** (client→server, tag 0x0F u16 @+0x14, value=1 = positive confirm,
  vtable 0xf0d66c, id runtime-assigned) · server ไม่ต้องตอบ (corpus 8 เฟรม reply=0 ไม่ค้าง) →
  ถ้าเห็นตอนเดิน = แค่ docking/confirm UI ไม่เกี่ยว authority handshake · เหลือ bounded: value != 1 (negative)
  — 🟢 **"id runtime-assigned" ปิดแล้วรอบ 62 (commit `7c66b21`, NAMEID-HASH-001):** id 0x4477 =
  hash บริสุทธิ์ของชื่อ `"TeleportCheckVital"` (`Σ_i (signed char)name[i]*(i+1) mod 2^16` ที่ `0x89b220`,
  literal→slot 0x1082074→0x4477 byte-exact) — ต้นทางอยู่ในอิมเมจครบ ไม่ใช่ external counter
- 📐 **prediction จาก MOVE-CADENCE-001 (รอบ 59, commit `ef9acd7` — จดยืนยัน/หักล้างตอนเทส):**
  1. ระหว่างเดินต่อเนื่อง console จะเห็น TargetPosVital ~ทุก 2–6 วิ และ
     `character_positions.updated_at` ขยับตาม (GT-005 walk: 29 เฟรม → 19 write / 10 dedup)
  2. ยืนนิ่ง ≥30 วิ → `updated_at` **ไม่ขยับเลย** (client ส่งซ้ำตำแหน่งเดิม → dedup ทั้งหมด)
  3. sub-observation heading: จบ walk ให้หันหน้าทิศชัด ๆ ก่อนออก → DB `heading` = ค่าเฟรมสุดท้าย
     (ชั้น DB พิสูจน์แล้ว) · ตอน respawn ครั้งถัดไป **ตัวละครหันตามทิศนั้นไหม** (ชั้น client-observable
     ยังเปิดอยู่ — จดว่าใช่/ไม่ใช่)
- result: (ผู้เทสกรอก)

---

## GT-016 CHAT-CHANNEL-001: class id ตัวเดียวเปลี่ยนช่องแชทบนจอจริงไหม  [✅✅ PASS ชี้ขาด — รอบใหญ่ #3]

> ✅✅ **RESULT รอบใหญ่ #3 — PASS ชี้ขาด (ผลที่ดีที่สุดของรอบ) · ผลเต็ม: `pf_bridge\notes_to_chief\consumed\20260818_1745_biground3-results.md`**
> พิมพ์ `PFCHATPROBE1` **ครั้งเดียว** → server ยิง 5 เฟรม → **client เรนเดอร์ 5 บรรทัด คนละ label คนละสี:**
> | # | label บนจอ | สี | เฟรม |
> |---|---|---|---|
> | 1 | `[ทั่วไป]` | ขาว | LOCALTALK |
> | 2 | `[ปาร์ตี้]` | ฟ้า | PARTY |
> | 3 | `[กิลด์]` | เขียว | GUILD |
> | 4 | `[GM]` | แดง | GMGLOBAL |
> | 5 | `[ทั้งหมด]` | ชมพู/ม่วง | ACTORBOARDCAST |
> - wire (job 125): เห็นครบ 5 marker เรียงเป๊ะ · **frame_bytes = 66B เท่ากันทุกเฟรม** · speaker ว่างทุกเฟรมตามดีไซน์
> - ⇒ **payload ไบต์เดียวกันเป๊ะ ต่างแค่ class id (byte 16–17) → client แยกช่อง/สี/label ได้ 5 แบบ**
>   = **"channel identifier คือ 16-bit class id ไม่ใช่ field ใน payload" พิสูจน์ถึงชั้น client-observable แล้ว**
>   → ดัน CHAT-CHANNEL-001 จาก static ขึ้น runtime ได้ทั้งก้อน
> - 📌 job ที่ใช้ **`124_gt016_boot.ps1` / `125_gt016_teardown.ps1`** (ผู้เทสสร้างเองจาก 104/105) ⚠️ บรรทัด log ยังพิมพ์ป้ายเก่า `scenario=chat_input_hypothesis_speaker_echo` — **ธงจริงถูกต้อง** chief ต้องแก้ป้ายก่อน stage ถาวร

- 🟢 **อัปเดตรอบ 77 (2026-08-18, commit `f286945`) — ปลดบล็อกแล้ว อ่าน 5 บรรทัดนี้ก็พอ:**
  1. **มีทางส่งออกแล้ว** — `CHAT-CHANNEL-003 dispatch hookup` ต่อ codec เข้า runtime เรียบร้อย
     (flag ใหม่ `--channel-message-hypothesis-scenario` + dispatch branch + scenario sweep)
  2. **trigger = พิมพ์แชทในเกม** ข้อความ **ASCII 12 ตัวพอดี** (เช่น `PFCHATPROBE1`) — request ที่ client ส่ง
     คือเฟรมเดิมที่ GT-006 เคยจับได้ · server จะตอบกลับ **5 เฟรม เรียงช่อง เว้น 3 วิต่อเฟรม (รวม ~12 วิ)**
  3. **payload ทั้ง 5 เฟรมเหมือนกันทุกไบต์** (chief วัดเองแล้ว: sha `0DC90C60..`) · PC ต่างกัน **แค่ byte 16–17
     = class id** ⇒ ถ้าจอเรนเดอร์ต่างกัน แปลว่า client แยกช่องจาก class id ล้วน ๆ = claim ของเทสนี้
  4. **ทุก sha คำนวณไว้ล่วงหน้าครบแล้ว** ใน scenario — ผู้เทสเทียบไบต์ได้ทันทีไม่ต้องเดา
  5. ⚠️ **ยังไม่เคยขับผ่าน TCP จริง** — headless พิสูจน์ถึงชั้น dispatcher (ต่ำกว่า socket 1 ชั้น) เท่านั้น
     ⇒ ถ้า boot แล้วไม่มีอะไรออกมาเลย **นั่นคือผลที่มีค่า** ให้จดว่าเงียบที่ชั้นไหน อย่าเพิ่งตีว่าพัง
- 📌 scenario ที่ใช้: **`scenarios/channel_message_hypothesis_channel_sweep.json`** (ตัวใหม่รอบ 77 — **ไม่ใช่**
  `..._shared_serializer.json` ซึ่งเป็นตัว codec-only ของรอบ 76 ที่ไม่มี dispatch)
- 🖥️ **server args (คัดลอกไปใช้ได้เลย):**
  `py -3 -m pirateforce_foundation.app --db "<สำเนา canonical>" --channel-message-hypothesis-scenario "scenarios\channel_message_hypothesis_channel_sweep.json" --second-password-mode bypass`
  (flag นี้ **บังคับ `--db` ที่มีอยู่จริง** · เลนนี้ mutually exclusive กับ scenario อื่นทุกตัว)
- 🔎 **label ที่จะเห็นใน `GAME_EVENTS_LIVE.txt`** (ใช้ยืนยันชั้น wire เรียงตามนี้เป๊ะ):
  `HYP_PF_019_CHANNEL_SWEEP_LOCALTALK` → `_PARTY` → `_GUILD` → `_GMGLOBAL` → `_ACTORBOARDCAST`
- objective: (claim เดียว — ชั้น client-observable) **channel identifier คือ 16-bit class id ไม่ใช่ selector ใน payload**
  — ส่ง payload **ไบต์เดียวกันเป๊ะ** ออกไปใต้ class id ต่างกัน แล้ว client เรนเดอร์คนละช่อง/คนละ style จริงไหม
  · เป็นเทสที่ **ใช้ client เดียวก็พอ** (ไม่ต้องรอ two-client) เพราะพิสูจน์ฝั่ง "ขาเข้า/การเรนเดอร์" ไม่ใช่ fan-out
- ฐานหลักฐานที่มีแล้ว (ชั้น static, **อย่านับเป็นเกณฑ์ผ่าน**): `reports/PF_CHAT_CHANNEL001_CHANNEL_FAMILY_AND_ROUTING_STATIC_20260818.md`
  — 5 ช่องใช้ serializer ร่วม `0x65AD40` (LocalTalk `0xAC52` · Party `0x82E6` · Guild `0x8189` ·
  ActorBoardcast `0xEDFA` · GMGlobal `0x9F2C`) ⇒ wire เหมือนกันทุกไบต์ · dispatcher `0x659870`
  มี style name ต่อช่อง (`LocalTalk` / `PartyTalk` / `GuildTalk` / `YellTalk` / …) ·
  Whisper `0x556C` ต่างออกไป: มี **wstring ตัวที่สาม = recipient @+0x50** + u8 result @+0x6C
- db: สำเนา canonical สด · canonical ต้องไม่ขยับ
- server args: boot ตรงผ่าน `pirateforce_foundation.app` + scenario ของ CHAT-CHANNEL-002 (ชื่อไฟล์จะเติมตอนปลดบล็อก)
  + `-SecondPasswordMode bypass`
- steps (พร้อมรันแล้ว — รอบ 77 ปรับให้ตรงกับ dispatch จริง):
  1. boot ด้วย server args ข้างบน + login → เลือกตัวละคร → เข้าแมพ (PLAYBOOK 3–6) → เปิดกล่องแชทให้เห็นเต็ม
  2. **พิมพ์ในช่องแชท `PFCHATPROBE1` (ASCII 12 ตัวพอดี) แล้ว Enter ครั้งเดียว** → server จะยิงกลับ 5 เฟรมเอง
     เรียง LocalTalk `0xAC52` → Party `0x82E6` → Guild `0x8189` → GMGlobal `0x9F2C` → ActorBoardcast `0xEDFA`
     เว้น 3 วิต่อเฟรม (รวม ~12 วิ) — **ห้ามพิมพ์ซ้ำระหว่างรอ** จะได้แยกออกว่าบรรทัดไหนมาจากเฟรมไหน
     · ถ้าพิมพ์ยาว/สั้นกว่า 12 ตัว = fail closed เงียบโดยตั้งใจ ไม่ใช่บั๊ก
  3. **ถ่าย/จดทุกบรรทัดที่ขึ้นในกล่องแชท**: สี? prefix? ชื่อ tab/ช่อง? ต่างกันจริงไหม? หรือขึ้นเหมือนกันหมด?
     · ชื่อผู้พูดจะ **ว่าง** ทุกเฟรมโดยตั้งใจ (speaker = "" เพื่อให้ payload เท่ากันทุกไบต์) — ไม่ใช่บั๊ก
  4. (ถ้ายังมีเวลา) พิมพ์ซ้ำอีกรอบ → ต้องได้อีก 5 เฟรมเหมือนเดิม (เลนนี้ไม่ one-shot)
  5. 🚫 **ขั้น Whisper ของร่างเดิมตัดออกแล้ว** — เลนนี้ **ปฏิเสธ Whisper `0x556C` โดยตั้งใจ** (schema ต่าง:
     มี wstring ที่สาม = recipient @+0x50 + u8 result @+0x6C) ⇒ ยังไม่มีทางยิงจาก server
     · ถ้าอยากได้ชั้น client-observable ของ whisper/recipient/result-code ต้องเปิด milestone แยก — จดเป็นคำขอได้
  6. teardown ตาม PLAYBOOK 7 + End task
- pass criteria (แยกชั้น):
  - **client-observable (เทสนี้):** payload ไบต์เดียวกันใต้ class id ต่างกัน → **เรนเดอร์ต่างกันอย่างน้อย 2 แบบ**
    บนจอ (style/prefix/ช่อง) โดยไม่มี error dialog และ client ไม่ค้าง/ไม่หลุด
    · (เกณฑ์ Whisper ของร่างเดิมถูกตัดออกรอบ 77 — เลนนี้ปฏิเสธ Whisper โดยตั้งใจ ดู step 5)
  - **wire-DB (ยืนยันซ้ำ ไม่ใช่เกณฑ์หลัก):** `GAME_EVENTS_LIVE.txt` เห็นครบ 5 label เรียงตามลำดับ
    (`HYP_PF_019_CHANNEL_SWEEP_LOCALTALK/_PARTY/_GUILD/_GMGLOBAL/_ACTORBOARDCAST`) ·
    payload หลัง header เหมือนกันทุกช่อง (byte-compare) · canonical ไม่ขยับ
- nonclaims: **ไม่ claim fan-out/routing/membership ของ original server** (ยังต้อง 2 concurrent session —
  ท่อนนั้นของ coverage note ยังยืน) · ไม่ claim ความหมายเชิงค่าของ result code ตัวอื่น ·
  ไม่ claim ว่าช่องที่ไม่มี downcast consumer (`JoinOriginalSinChannel`, `OriginalSinChannelMessage`,
  `JoinClassChannel`) จะเรนเดอร์อะไร — 3 ตัวนี้ **static บอกว่าไม่มี consumer** ถ้าเงียบคือคาดไว้แล้ว ไม่ใช่ FAIL ·
  ถ้าทุกช่องขึ้น**เหมือนกันหมด** = ผลลบที่มีค่า (client แยกช่องที่ชั้นอื่น) → จดเป็น observation อย่าตีเป็น FAIL ของ static

---

