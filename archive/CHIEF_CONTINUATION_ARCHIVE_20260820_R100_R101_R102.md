# CHIEF_CONTINUATION archive - rounds 100, 101, 102 (2026-08-20)

ย้ายมาจาก `CHIEF_CONTINUATION.md` โดย chief รอบ 106 (2026-08-20 ~16:3x) ตามกติกางานแม่บ้าน
(ไฟล์แม่ ~101KB เกินเพดาน ~100KB) — **ทั้งสามรอบปิดแล้ว commit ลงแล้ว ห้ามลบ**
ต้นฉบับเต็มอยู่ข้างล่างนี้ ไม่ตัดทอนสักบรรทัด

---

> ## 🆕🆕 รอบ 102 (2026-08-20 12:1x → 13:0x) — **⭐ ประมวลรอบใหญ่ #9/#10: GT-027/028/029 ปิดครบ · static ปิดคำถามค้างทั้งสองข้อ (GT-021 รอด · toggle 0x420 คือผู้ต้องสงสัยจอมืด) · ERRATUM commit เขียวรวด · ⭐⭐ ORDER retarget hostile จริง: บัญชี 13 ตัว + XYZ + ระยะ ส่งแล้ว — รอ Panya เคาะระยะทาง**
>
> **HEAD `48817be` → `eab98e6` (job 164 — จ็อบเดียว allGreen)** · commit **1 path** (ERRATUM 1 บน draft R100) · full suite **1860 passed 1 skipped 3569 subtests (202 วิ — ไม่มี server สดขนาน)** · fresh clone reproduce (erratumPresent=yes coverage=0 ledger=0) · ledger **35 ไม่ขยับ** · coverage/census ไม่แตะ · canonical `6BFCEDD5..8FC7` ไม่ขยับ · ถือ `LOCK_GIT` 12:54→12:58 (จ็อบเขียน HELD/RELEASED เอง) · **ไม่แตะ `LOCK_GAME` เลย** (ยัง HELD โดยรอบใหญ่ #10 ของเซสชันหลัก — heartbeat 11:35 · สัญญาณชีพล่าสุดผ่านกล่องจดหมาย 12:30 · ไม่เข้าเกณฑ์ takeover และ chief ไม่มีธุระกับเกม)
>
> ### 📬 บริโภคจดหมาย 4 ใบ
> - **`1105_PANYA-RULE-queue-priority-zero-prefix`** — กฎ 0-prefix รับทราบ (LOCK_GAME มีบล็อกอยู่แล้ว) · chief = 1xx เหมือนเดิม · ข้อเสนอ "พักจ็อบ gate ยาวเมื่อ heartbeat < 20 นาที" **ยังไม่อนุมัติ — chief ใช้โดยสมัครใจ** (รอบนี้ heartbeat เก่า >70 นาที จึงเดิน)
> - **`1130_GT027-028-029-RESULTS`** — GT-029 **[PASS]** วงนับถอยหลังลดจริง 19→15→13→10 (สองรอบ) · ผลลบ GT-027 ฉบับนี้ถูก **แทนที่** ด้วย rerun · บทเรียน hold_key ยกเข้าคิวแล้ว
> - **`1200_GT027-RERUN-PANYA-DRIVEN`** — **GT-027 [PASS]** (Panya ขับเอง · วิดีโอ 58 วิ + ภาพนิ่งทุกเฟรม): `63`/`379`/`MISS!`/`63` **เกาะ NPC** ค่าตรง wire เป๊ะ ไม่มี scale/ลบ ⇒ ยืนยัน DAMAGE-MODEL-001 + FINDINGS_R93 บนจอจริง · **GT-028 [PASS]** เหลือข้อ ⑥ (flag 0x0009 มองไม่เห็นความต่าง) · ข้อเท็จจริงใหม่: client resolve `0x2001` → placement P0 'Navy Transfer' · `TargetVital 0x1ADD` โผล่เฉพาะเซสชันที่เห็นเลข → เปิดคำถาม static (ตอบแล้ว ดูล่าง)
> - **`1140_PANYA-ORDER-retarget-real-hostile`** — ORDER ใหญ่ ดูหัวข้อถัดไป
>
> ### ⭐ static RE 2 เส้นขนาน (ลูกมือ 2 ตัว) — ปิดคำถามค้างจากผลเทสทั้งสองข้อในรอบเดียว
> - **DYING-COUNTDOWN (คำถามชี้ขาดของ GT-029): คำตัดสิน (ข) UI นับเอง [PROVEN 3 ชั้น]** — ไม่มี writer ลด `attr.f32[+0x58]` ทั้งอิมเมจ (สำมะโน store 437 จุด · RMW-decrement ทุก candidate เป็นคลาสอื่น) · ผู้อ่าน float ของ field มี 3 ที่ล้วน predicate (`0x454A7D`/`0x454ACA`/`0x44A56D`) · ไม่มี display path อ่าน field นี้ ⇒ **GT-021 ยังถูก · เฟรมที่สี่ timer=0.0 ยังจำเป็น · ไม่รื้อ ledger — เรื่องปิด** · `FACTPACK_R102_DYING_COUNTDOWN_UI_FIELD_STATIC.md`
> - **TARGETVITAL/FXNUMBER GATES (ปริศนา "ผู้เทสตาบอดสองรอบ"):** `TargetVital 0x1ADD` = รายงานเป้าที่เลือก (ผู้บริโภค map `0x102C6C0` ผ่าน resolver `0x446170` ตัวเดียวกับ number pass — **ไม่มี insert**) ⇒ เป็น**พยาน**ว่า `0x2001` resolve ได้ ไม่ใช่สาเหตุของเลข · สมมติฐาน (ก) selection-gate และ (ข) HIT_REACTION-ส่ง-TargetVital **หักล้างทั้งคู่ด้วยไบต์** · 🔴 **ของใหญ่: `[localplayer+0x420]` gate เลขหลักจริง** (`0x43FE2C je no-draw` · toggle = input command `0x27` @ `0x42C68A` · default ON @ `0x44CAC2`) — **หักล้างคำอ้าง Q4 ของรอบ 100** ⇒ คำอธิบายอันดับหนึ่งของจอมืด (เข้าคู่บทเรียน hotkey รอบ #8) · `FACTPACK_R102_TARGETVITAL_AND_FXNUMBER_GATES_STATIC.md` (41/41 guards)
> - **สิ่งที่ commit (job 164):** ERRATUM 1 ต่อท้าย `drafts/MONSTER_SPAWN_LOOT_STATIC_AND_DESIGN_R100_20260820.md` — แก้ประโยค "ไม่มี singleton ไหน blank เลขหลักได้" (ข้อความเดิมคงไว้ตาม norm · pool `0x102dca4` = ยังไม่ตรวจซ้ำ ระบุเป็น UNKNOWN) — เหตุที่ commit ทันที: เป็น safety hazard ต่อการออกแบบเทส
>
> ### ⭐⭐ ORDER retarget (Panya ~11:40): เกมจริงสู้กับ "มอนสเตอร์" ไม่ใช่ NPC เมือง — เลนใหม่ GT-034+
> - **งานแรกตามคำสั่ง เสร็จในรอบ: `FACTPACK_R102_HOSTILE13_ROSTER.md`** — hostile faction-6 ครบ 13 ตัว: identity/XYZ/ระยะจาก observation point (เรียงใกล้→ไกล)/level/**HP จริงจาก STANDARD_MOB** (parse สดตาราง 027)/faction-off-aggro (parse สด AI_WANDER 024)/drops/skills · **ตัวใกล้สุด `0x201F` Tornado Eagle ~11,914 หน่วย** (retaliate-only — เหมาะเป็นเป้าแรก) · ตัวที่จดหมายเดา (`0x200D`) กลับ**ไกลสุด** 38,890 · ตัว AGGRO=1200 สามตัว (`0x203B`/`0x2040`/`0x2085`) ห้ามใช้เป็นเป้าแรก
> - 🔴 **เข้าเงื่อนไขใน ORDER เอง: "ไกลจนเดินไม่ไหว → รายงานระยะทางก่อน อย่าเพิ่งออกแบบเทส"** (11,914 ≈ 120 เท่าของระยะ 0x2001) ⇒ **GT-034 HOSTILE-NATIVE-001 = ⏸ รอ Panya เคาะ**: เดิน (ให้ผู้เทสวัดอัตราเดินก่อน) / เลน teleport opt-in (V129 `TeleportWithVehicle` พิสูจน์ไว้แล้ว — chief ออกแบบได้ใต้ pattern มาตรฐาน) / ตัวอื่น
> - คิวอัปเดตครบ: **GT-034**=HOSTILE-NATIVE (⚠️ เลขชนข้อเสนอผู้เทส — **คำสั่ง Panya ชนะ** · A/B ของผู้เทสเป็น **GT-038** พร้อมคำทำนาย static ประกบ) · **GT-035/036** = BLOCKED โครงพร้อม · **GT-037 LOOT-ROLL-001** = งาน dev headless **ของ chief รอบถัดไป** (ไม่กินคิวสะพาน)
> - 🔴 **ตามคำสั่ง — เขียนให้ชัด: "มอนโจมตีผู้เล่น" (Door B) ยังไม่มีทางบนสายวันนี้** — BEHAVIOR lookup คืน null ทุกครั้งที่เคยเห็น · ActionVital inert (SCENE-008) · ไม่มี capture ต้นฉบับ · ไม่มี encoder · **หมายเหตุต่อคำสั่ง:** ctor walk ที่สั่งให้เป็น static ลำดับหนึ่ง **ทำเสร็จแล้วในรอบ 100** (UseBehavior ctor `0x47ab30` · construct path เปิด ไม่ gate กับ projected NPC) ⇒ unknown จริงที่เหลือ = **populated BEHAVIOR row + wire delivery** — **ตั้งเป็น static ลำดับหนึ่งของรอบ 103** (ทำตามเจตนา ไม่ใช่ตามตัวอักษร): parse `Data/B_CONSTDATA_TH.pc_` หา BEHAVIOR row จริง (คำถามค้าง R98 ข้อ ③) + ออกแบบ fight-vital delivery
>
> ### 🧾 ธุรการ + งานแม่บ้าน
> - แม่บ้านทำแล้ว: **R93/95/96 → `archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R93_R95_R96.md`** (ไฟล์นี้ 104KB → ~75KB) · GT-027/028/029 ข้อความเต็ม → `archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R102_GT027_028_029.md` (สรุปผลคงอยู่ในคิวเป็น stub PASS)
> - GAME_TEST_QUEUE ~78KB — **overage เป็น load-bearing** (GT ใหม่ 5 รายการจาก ORDER + PLAYBOOK/บทเรียน) ตามกฎ PANYA never-drop-untested · บทเรียนเครื่องมือใหม่ลงคิวแล้ว: **toggle 0x420/hotkey 0x27** (กฎบังคับก่อนทุก damage-GT: client ใหม่ = default ON · จอมืดทั้งเซสชัน → relaunch ก่อนสรุป wire ผิด) + กฎ hold_key + ทางลัดปุ่ม `เข้า`
> - เลขจ็อบ: chief ใช้ **164** ⇒ **chief ถัดไป 165** · ผู้เทส 9xx ต่อจากของตัวเอง (done/ ล่าสุด = 946) · จดหมายถึงผู้เทส: `FROM_CHIEF_R102_TO_ATTENDED_20260820_1300.md`
> - 💡 บทเรียน: gate เต็มชุด 202 วิ เมื่อไม่มี server สดขนาน (vs 897 วิ รอบ 100) — ยืนยันตัวเลข R100 อีกด้าน
>
> ### 📌 คำถามค้าง / งานที่จงใจเลื่อน
> - 🔴 **รอ Panya เคาะ: GT-034 เดิน/teleport/ตัวอื่น** (ระยะทางรายงานแล้ว — ห้ามออกแบบท่าเดินก่อนเคาะ) — ระหว่างรอ chief มีงานเดินต่อได้: GT-037 roller + Door B static (ไม่จมรอ)
> - จบก้อน 2 multiplayer (GT-030 รัน) ต้องกลับให้ Panya เคาะก่อนก้อน 3 · HYP-PF-025 เหลือ 1 slot · persistence Lane 2/3 เลื่อนท้ายสุด (ไม่ถามซ้ำ) · GT-028 ข้อ ⑥ = ไม่บล็อกอะไร รอเลนที่ใช้ flag เดียวกัน
> - milestone สำรอง not_started: `pvp_engagement` · `mob_aggro_and_server_ai` (Door B — ปลดล็อกด้วย BEHAVIOR row + delivery ข้างบน)
>
> ### nonclaims ของรอบ 102
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่แตะ `LOCK_GAME` · ไม่ flip coverage · ไม่เพิ่ม ledger · ไม่แตะ census · ไม่แตะ v141 (placements อ่านด้วย regex อย่างเดียว)**
> · runtime observation ทั้งหมดในรอบนี้มาจากจดหมายผู้เทส/Panya — chief ไม่เห็นจอเอง · ระยะทางใน roster = เส้นตรง XY ไม่ใช่ระยะเดินจริง (ไม่มี navmesh) · จุดอ้างอิง = observation point ของ**เซิร์ฟเวอร์เรา** ไม่ claim จุดเกิดของต้นฉบับ · faction/AI/drops/HP = ข้อมูล ship กับ client ไม่ใช่พฤติกรรมเซิร์ฟเวอร์ต้นฉบับ **ซึ่งกู้ไม่ได้ตลอดกาล** · toggle 0x420 เป็นคำอธิบาย**อันดับหนึ่ง**ของจอมืด ไม่ใช่คำพิสูจน์ — ตัดสินจริงที่ GT-038 · pool `0x102dca4` ยังไม่ตรวจซ้ำ [UNKNOWN]

> ## 🆕🆕 รอบ 101 (2026-08-20 11:2x → 12:0x) — **⭐ GT-033 variant B ลงจริง: HYP-PF-028 LOGOUT-RETURN-SELECT-001 — ตอบ LogoutVital ด้วย `ReturnSelectServerVital 0x709E` ที่ประกอบจาก serializer จริงของ client (ไม่มีไบต์เดา) · headless-proven ครบ · commit เดียวเขียวรวด**
>
> **HEAD `48a016b` → `48817be` (job 163 — จ็อบเดียว allGreen ตั้งแต่รอบแรก)** · commit **12 paths** (5 new + 7 modified) · full suite **1860 passed 1 skipped 3569 subtests** (232 วิ บน Windows · +13 เทสใหม่) · fresh clone reproduce ครบ (coverage=0 ledger=0 lrsVerify=0 lrsReplay=0) · ledger APPEND entry **35** (HYP-PF-028 · canonical content sha re-pin `E2253C31..` → `BA5FE4A6..`) · canonical DB sha `6BFCEDD5..8FC7` ไม่ขยับ · ถือ `LOCK_GIT` 12:02→12:07 (จ็อบเขียน HELD/RELEASED เอง) · **ไม่แตะ `LOCK_GAME` เลย** · กล่องจดหมายว่างตั้งแต่ต้นรอบ (R100 บริโภคทุกใบแล้ว)
>
> ### ⭐ สิ่งที่ลง: variant B ของ GT-033 (pre-approved policy #4 "แก้ปุ่มออกเกม" · pattern มาตรฐาน)
> GT-026 (รอบ 100 attended) พบว่า client ส่ง LogoutVital แล้ว **รอ** · agent D พิสูจน์ว่า echo transition ไม่ได้แน่นอน (inbound 0x446F30 = reconcile pass) และชี้ candidate = `ReturnSelectServerVital 0x709E` แต่ **static ตัดสิน response shape ไม่ได้** → ต้อง attended A/B · รอบนี้ทำ **ฝั่ง server ของ variant B ให้พร้อมรัน:**
> - **static RE รอบ 101 (spawn ลูกมือ):** แกะ serializer ของ 0x709E (`0x5e69f0`, descriptor `0xf304ec` slot2) วิธีเดียวกับที่ agent D แกะ LogoutVital — **3 ฟิลด์: +0x14 tag 0x08 u8 · +0x18 tag 0x32 8-byte · +0x20 tag 0x44 std::string** · ทุก tag byte มาจาก serializer จริงของ client · **ไม่มี producer ตั้งค่าฟิลด์** (id-getter `0x5e6960` ไม่มี caller · ไม่มี handler consume 0x709E) ⇒ ค่า = 0 ทั้งหมด string ว่าง = **body 16 ไบต์ `08 00 / 32 00…00 / 44 00000000`** (nonclaim: ค่า = zero default ไม่ใช่ของเซิร์ฟจริง)
> - **lane = response policy ใหม่บน logout_hypothesis.py เดิม** (ไม่ใช่ module ใหม่ · แบบเดียวกับที่ HYP-PF-016 worldinfo_first เพิ่ม policy) · dispatch: LogoutVital → ส่ง 0x709E response ก่อน → ตามด้วย PF-012 ack เดิม (byte-identical) → PF-013 close 250ms · commit closed_at ก่อนไบต์แรก · fail closed ทุก payload/sequence/replay/missing-lever ผิด · scenario exact-allowlist
> - **ใช้ flag เดิม `--logout-hypothesis-scenario`** (ไม่ต้องเพิ่ม flag ใหม่ · app.py ไม่แตะ) · scenario ใหม่ `scenarios/logout_hypothesis_return_select_server.json`
>
> ### ใบเสร็จ (headless-proven — client ยังไม่เคยเห็นแม้แต่ไบต์เดียว)
> `tools/verify_logout_return_select_encoder.py` **34 guards** (re-derive 16-byte body ด้วย walker อิสระ · re-pin response · ยืนยัน PF-012/013 pins · ขับ tamper ทุกตัวให้ refuse by name) · `tools/pf_logout_return_select_headless_replay.py` **45 guards** ผ่าน dispatcher จริงบนสำเนา DB (subcode 03+01 · [0x709E, ack] เรียงถูก · closed_at เติมก่อนไบต์ · แตะแค่ตาราง sessions · source DB ไม่ขยับ · walker อ่าน 0x709E frame กลับจากไบต์) · **13 เทส** (`test_logout_return_select_hypothesis.py`)
> census re-pin: **VitalData carrier (make_runtime_vitals) 15 → 16** (logout_hypothesis.py มี 2 site แล้ว: ack + return_select · module ระบุชื่อข้างเลข) · **actor-entry census + timer census ทั้งสามไม่ขยับ** (lane นี้ไม่สร้าง actor entry ไม่เอ่ย bit 0x0080) · report `PF_RUNTIMERES..._STATIC` COUNTS block re-pin ตาม · `.gitignore` allowlist +3 (2 tools + report) · **coverage ไม่แตะ** (logout lanes อยู่ใน ledger อย่างเดียว · OPEN DOMAINS 8 เท่าเดิม)
>
> ### คิว attended (GT-033 พร้อมทั้งสอง variant แล้ว)
> - 🆕 **GT-033 variant B = PENDING พร้อมรัน** ที่ `48817be` — boot `--logout-hypothesis-scenario scenarios\logout_hypothesis_return_select_server.json` · **คำถามหลัก: client กลับหน้า char-select เมื่อได้ 0x709E ไหม** · ⛔ ผลลบมีค่า (น่าจะลบ เพราะไม่เจอ client consumer → ชี้ว่า lever ที่ถูกคือ connection-teardown = variant A)
> - **variant A = HYP-PF-013 เดิม** (`logout_hypothesis_ack_close.json`) · steps A/B + subcode 01/03 ครบในคิวแล้ว
> - เลขจ็อบ: chief ใช้ **163** ⇒ **chief ถัดไป 164** · ผู้เทส 9xx
>
> ### 🧾 ธุรการ + หมายเหตุ id
> - **HYP-PF-028 = logout-return-select** (จองไปแล้ว commit นี้) ⇒ **Door B attack probe ที่ prose เก่าเรียก "HYP-PF-028" ต้องใช้ id ว่างถัดไป (029) เมื่อเปิดจริง** — ไม่มี ledger entry ของ Door B อยู่ก่อน ไม่ชนของจริง
> - กล่องจดหมายว่าง · ไม่มี PENDING queue ถูกย้าย/ลบ (กฎ PANYA never-drop-untested) · CHIEF_CONTINUATION ~99KB (ใกล้ 100KB — **รอบหน้าเริ่มด้วยงานแม่บ้าน: archive รอบเก่าที่ปิดแล้วไป pf_bridge\archive\ ทิ้ง pointer**) · GAME_TEST_QUEUE ~66KB (overage load-bearing)
>
> ### 📌 คำถามค้าง / งานที่จงใจเลื่อน (ไม่เปลี่ยนจากรอบ 99/100)
> - **Door B (attack probe, id ใหม่ = 029)** = ทำได้หลัง GT-032 ยืนยัน Door A บวก · ctors แกะได้แล้ว (รอบ 100) ⇒ unknown ที่เหลือ = wire delivery + populated behavior row · ผลลบ (null) น่าจะมีค่าที่สุด
> - **จบก้อน 2 multiplayer (GT-030 รัน) ต้องกลับให้ Panya เคาะก่อนก้อน 3** · HYP-PF-025 เหลือ 1 slot
> - persistence Lane 2/3 เลื่อนท้ายสุด (ไม่ถามซ้ำ) · **milestone สำรอง not_started ที่เหลือ:** `pvp_engagement` · `mob_aggro_and_server_ai` (Door B) · monster_spawn_loot (design draft แล้ว รอบ 100)
> - LOOT-ROLL-001 (pure-logic roller จาก client tables) = checkpoint buildable ถัดไปที่ chief แนะนำเอง (รอบ 100) — dependency: DropThing transport decode (blocker)
>
> ### nonclaims ของรอบ 101
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB (นอกจาก session close บนสำเนา) · ไม่ flip/แตะ coverage row · ไม่แตะ v141 · ไม่แตะ `LOCK_GAME` · ไม่แตะ HYP-PF-012/013/016 หรือไบต์ของมัน (isolation test ยืนยัน)**
> · **ไม่มี runtime observation ใหม่** — 0x709E ยังไม่เคยถูกส่งให้ client (นั่นคือ GT-033) · **response = ดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** · field values ของ 0x709E = zero default ไม่มี producer · ไม่ claim ว่า client consume 0x709E หรือ transition · full suite รันบน Windows เท่านั้น

> ## 🆕🆕 รอบ 100 (2026-08-20 10:0x → 10:3x) — **⭐ เปิดแถว `monster_spawn_and_loot`: mine โมเดล loot ครบทั้งชุดจาก client + จัดอันดับ "ประตู" ของวง loot + ⭐⭐ แก้ record Door B รอบ 98: ctors ของ attack task แกะได้แล้ว และ construct path ไม่ถูก gate กับ projected NPC · commit docs-only เขียวรวด (รันขนานกับเซสชัน ATTENDED สด GT-026)**
>
> **HEAD `87f0769` → `48a016b` (job 162 — จ็อบเดียว allGreen ตั้งแต่รอบแรก)** · commit **2 paths** (draft + `.gitignore` allowlist) · full suite **1847 passed 1 skipped 3561 subtests** · ⏱️ **897 วิ (~15 นาที) — ช้าเพราะรันขนานกับเซิร์ฟเวอร์ ATTENDED สด (GT-026) แต่เขียวหมด** · fresh clone reproduce ครบ (draftPresent coverage=0 ledger=0) · ledger **entries=34** · OPEN DOMAINS **8** · census ทั้งสาม (runtimeres 152 / hp 191 / vital-thunk PASS) **ไม่ขยับเลย** (draft อยู่ใน drafts/ ไม่แตะ src/) · canonical sha `6BFCEDD5..8FC7` ไม่ขยับ · ถือ `LOCK_GIT` 10:16→10:34 (จ็อบเขียน HELD/RELEASED เอง) · **ไม่แตะ `LOCK_GAME` เลย** (เซสชัน ATTENDED ถืออยู่ · GT-026 EXIT-PATHS-001 · server 36804 + client เปิดสด)
>
> ### ⭐ สิ่งที่ลง: `drafts/MONSTER_SPAWN_LOOT_STATIC_AND_DESIGN_R100_20260820.md` (362 บรรทัด · ASCII ล้วน)
> เลือก milestone สำรอง pre-approved `monster_spawn_and_loot` (แถว not_started) · spawn ลูกมือ static RE ขนาน 3 ตัว แล้วเขียนเป็น design draft (ไม่ใช่ lane) — เพราะ **ปลายวงสองด้านสร้างได้/สร้างแล้ว แต่ตรงกลางยังไม่มีถนน**
> **ของใหม่ที่ mine ได้รอบนี้ (ไม่เคยมีรายงานไหนแกะเกิน table 033):**
> - **โมเดล loot ครบทั้งชุดใน client const-data** — MOBS(028, 3210×54) ชี้ทุก kill ไป DROPS_NORMAL/EQUIPMENT/SPECIALLY ด้วย encoding **`prefix*100000 + row n_ID`** (พิสูจน์: normal 62/62 · equipment 36/36 · specially 107/107 resolve 100%) · มี rate/quantity/weight/quality ครบ **พอ roll ได้จริงไม่ต้องเดา** · HP มาจาก STANDARD_MOB(027) ตาม level (MOBS ไม่มีคอลัมน์ HP) · faction มาจาก MOBS.n_AI_WANDER → AI_WANDER.n_FACTION (ไม่มีคอลัมน์ faction ตรง)
> - **GT-032 prediction ยืนยันด้วยข้อมูล:** FACTION(085) row 1 enemies="6;11;12;17;18;26" · row 6 enemies="1;2;3;12;13;18" ⇒ **faction 6 ↔ 1 เป็นศัตรูกันสองทาง** ตรงกับคู่ที่ HYP-PF-027 ประกอบเป๊ะ (แต่ค่า player=1 ยังเป็นของเรา · grade ไม่ขยับจนกว่ามีพยานตาเปล่า)
> - **Port Royal จริง:** `0x2001` = template 1 "Navy Transfer" = **NPC เมือง faction 4 ไม่มี combat AI ไม่มี loot** · แต่มี **13 hostiles จริง faction 6** (0x200D "Fighting Fish Sergeant" lvl27, ..., 0x2085 "Orc Chief" lvl58-60) มี combat AI + skills + drop set ครบทุกตัว ⇒ **design note:** hostile lane ในอนาคตควรใช้ hostile จริง ไม่ใช่ splice faction ใส่ NPC เมือง (ไม่ได้หักล้าง HYP-PF-027 ซึ่งเป็น presentation probe ตั้งใจให้แคบ)
>
> ### ⭐⭐ แก้ record Door B (รอบ 98) — ctors ของ attack task แกะได้แล้ว [STATIC]
> รอบ 98 บันทึก Door B ว่า "ctors ยังแกะไม่ได้ (custom RTTI)" = **คำถาม static #1** · รอบนี้แกะสำเร็จด้วยวิธี **token→name binding** (MSVC ไม่มี COL แต่ทุกคลาสมี token record + GetType thunk `mov eax,<token>;ret`):
> - `CActorTask_UseBehavior` vtable **0xf0ef10** ctor **0x47ab30** GetType 0x471dc0→token 0x102ed50 · `[task+0x10]=8` (flags word ไม่ใช่ 0x800000XX — เหตุที่ KIND-scan รอบ 98 หาไม่เจอ)
> - `CActorTask_PlayActionEvent` vtable **0xf0ef28** = base task (UseBehavior derive จากมัน) ไม่มี standalone ctor
> - construct path ที่สะอาด = fight-vital consumer `0x7516c0` (CFightMsgVital, high-conf) resolve target actor จาก handle → lookup 0x702a10 → alloc → **call ctor 0x751809** · **gate เดียวใน ctor = is-a `CActorBaseClient`** (root ที่ทุก actor รวม projected CNetNPC สืบทอด → ผ่าน) · task ถูกสร้างก่อน gate · bail path คืน task เต็ม ⇒ **construct path ไม่ถูก gate กับ NPC**
> - 🔴 **ยังไม่เปิด attack loop:** ทุก BEHAVIOR lookup ยังคืน null · inbound ActionVital พิสูจน์แล้วว่า inert (SCENE-008) · ไม่มี capture · ไม่มี encoder ⇒ Door B ขยับจาก "ctors unresolved" → "ctors resolved + construct path open" · **แถว `mob_aggro_and_server_ai` ยัง not_started**
> - Q2 ยืนยัน: CAIStateCombat = name-only registration · CAIStateCombatProxy = inert stub (ไม่มี tick/update) ⇒ combat ไม่ถูกขับด้วย client FSM นี้ · Q4 ยืนยัน: `[0x10339B0]`=CMacroActionFactory · `[localplayer+0x420]`=byte toggle combat-text รอง — **ทั้งคู่ไม่ gate เลขดาเมจหลัก**
>
> ### วง loot จัดอันดับตามความพิสูจน์ (ในดราฟต์)
> - **ประตู 1 (มอนสเตอร์ เกิด/เป็นศัตรู/ตาย) = ของเราแล้ว** [PROVEN] — spawn 0x6E9D/HYP-PF-023 · hostility HYP-PF-027 · death/damage-link HYP-PF-026
> - **ประตู 2 (roll ว่าดรอปอะไร) = สร้างได้เลยเป็น logic ล้วน** [OUR DESIGN บนข้อมูล PROVEN] — LOOT-ROLL-001
> - **ประตู 3 (loot object โผล่บนพื้น) = ไม่มี wire path** [NEGATIVE] — actor-entry jump table รับแค่ type 2..6 ไม่มี item/object · DropThing family = ชื่อ+id เดา เท่านั้น (ไม่มี transport/serializer/capture) ⇒ **นี่คือ blocker**
> - **ประตู 4 (pickup request) = ไม่มี wire path** [NEGATIVE] — PickupTerrainThing = ชื่อ registered + derived id 0x4543 เท่านั้น
> - **ประตู 5 (client โชว์ item ที่ได้ใหม่) = lead แข็ง** [STATIC] — 0x4C13 v2 ItemBag delta handler clone item เข้า slot **ไม่มี prestate gate**
> - **ประตู 6 (persist) = schema รับได้ แต่ยังไม่มี writer** — ไม่มี code insert item row ใหม่หลัง char creation · identity/slot policy ยังไม่กู้ · writer ใหม่ต้อง catch exception เอง (dispatch unguarded)
>
> ### เสนอ checkpoint ถัดไป (ยังไม่ได้ทำ — ข้อเสนอในดราฟต์)
> 1. **LOOT-ROLL-001** = server-side loot roller (logic ล้วนจาก client tables · unit test Grade A · ไม่มี wire/DB/client) = **win แรกที่ทั้งพิสูจน์ได้และตรงตามของจริง** · ไม่ขยับ grade (ไม่มีอะไรเรนเดอร์) · น่าจะเปิด ledger entry ใหม่
> 2. **DROPTHING-TRANSPORT-PROBE** (static · blocker) = decode `0x446FE1..0x4470E5` (reconcile/removal pass ที่ตั้งชื่อแต่ไม่เคยแกะ) + DropThing registration · ผลลบน่าจะเป็นผลที่มีค่าที่สุด
> 3. **GRANT-ITEM PROBE** (หลัง 1 · ถ้าตัด ground path ออก) = direct-to-backpack grant ผ่านประตู 5+6 · **ต้องปะป้าย non-canonical** (ของจริงดรอปบนพื้น)
>
> ### 🧾 ธุรการ + งานแม่บ้าน
> - 🆕 **บริโภคจดหมาย `20260820_0945_PANYA-RULE-never-drop-untested-queue.md`** → กฎแม่บ้านถาวร: **ห้ามย้าย/ลบคิว GAME_TEST_QUEUE ที่ยัง PENDING/READY/BLOCKED/RUNNING ไม่ว่าค้างนานแค่ไหน · archive เฉพาะ PASS/FAIL/DONE/supersede-โดยชื่อ · เพดาน ~60KB ไม่ใช่เหตุผลย้ายคิวที่ยังไม่เทส → ถ้าเกินให้ปล่อยเกินแล้วรายงานว่าเกินเพราะรายการไหน · คิวยาว → จัดกลุ่ม/ทำสารบัญ ไม่ใช่เอาออก** (ผู้เทสแก้ต้นฉบับ agent_kit แล้ว แต่ sync เข้า scheduled task ฝั่ง local ไม่ได้ → Panya ต้องอัปเดต prompt ของ task บนเครื่องเองถ้าอยากให้ข้ามรอบ) · **chief รอบ 100 ไม่เคยย้าย PENDING ออก ไม่มีอะไรต้องย้ายกลับ**
> - **ไม่เพิ่ม attended test รอบนี้** (ดราฟต์เป็นดีไซน์) ⇒ **GAME_TEST_QUEUE ไม่เปลี่ยน** · คิวรอบใหญ่ #9 (GT-026 กำลังเทสสด · GT-030/031/032/027/028/029 + GT-001 re-arm) ยังค้างเหมือนเดิม
> - CHIEF_CONTINUATION.md ~76KB (< 100KB) · GAME_TEST_QUEUE.md ~65KB (overage เป็น load-bearing ตามกฎ PANYA ใหม่ — ปล่อยเกินได้)
> - fact pack ดิบ 3 ตัว เก็บถาวรที่ `pf_bridge\FACTPACK_R100_{DOORB_ATTACK_TASK_CTORS_STATIC, CONSTDATA_MONSTER_LOOT, INREPO_LOOT_SPAWN_GAPLIST}.md` (working notes · re-derivable · ดราฟต์ที่ commit แล้วถือเป็น durable artifact)
> - เลขจ็อบ: chief ใช้ **162** ⇒ **chief ถัดไป 163** · ผู้เทส 9xx
> - 💡 **บทเรียนรอบนี้:** full suite รันขนานกับเซสชัน ATTENDED สด = **ปลอดภัยแต่ช้า 5-6 เท่า (897 วิ vs ~165 วิ)** · suite เป็น hermetic ต่อพอร์ต 10188/10189 (ทุกเทสที่บูต server ใช้ fake/managed socket · ไม่มีเทสอ้างพอร์ต canonical) และไม่แตะ canonical DB (canonGuard ยืนยัน) ⇒ two-flag split ทำงานตามดีไซน์ · รอบหน้าถ้าเซสชัน ATTENDED สดและอยากเร็ว อาจเลื่อน full-suite gate หรือยอมรับ ~15 นาที
>
> ### 📬 จดหมายที่บริโภคเพิ่มระหว่างรอบ (มาสด ๆ ตอน job 162 กำลังรัน): `20260820_1025_GT026-RESULTS.md`
> เซสชัน ATTENDED สดรัน **GT-026 EXIT-PATHS-001** (รอบใหญ่ #9, HEAD `87f0769`, จ็อบ 933-937, tester next **938**) · ผล:
> - **ท่อน A [PASS] สองชั้น:** ปุ่ม X ในแมพ → dialog "ต้องการปิดเกมหรือไม่?" (`ยืนยัน`/`ยกเลิก`) → กดยืนยัน หน้าต่างหาย ≤1 วิ · **wire/DB: `closed_at` ถูกเติมตรงเวลากด** = ออกสะอาดในสายตา server (ไม่ใช่แค่ process ตาย)
> - **ท่อน B [รันบน default scenario]:** client ส่ง `LogoutVital 0x1B40` จริง มี **mode discriminator `08 03`=กลับหน้าเลือกตัวละคร / `08 01`=ออกจากเกม** (ยืนยัน decode R38 อีกครั้งจาก local สด) · server default ไม่ตอบ (handler HYP-PF-012/013 เป็น opt-in) · **client ไม่ transition แต่ก็ไม่ freeze** (รับคลิกปกติ)
> - **PLAYBOOK แก้ 3 จุด:** ① "logout ไม่มีธง = client freeze ต้อง End task" **ผิด** — ไม่ freeze ② ปุ่มเฟือง=OPTIONS ไม่ใช่ logout ③ ทางเข้า logout = `HOME`→`ออก`→หน้าต่าง 3 ปุ่ม (กลับเข้าเกม/กลับหน้าเลือกตัวละคร/ออกจากเกม)
> - **ข้อ 8 (เข้าเกมซ้ำไม่รีบูต) = BLOCKED** บน logout-transition ที่ทำงานจริง
>
> ### ⭐ ต่อยอดทันที: static RE เส้น LogoutVital transition (agent D · `pf_bridge\FACTPACK_R100_LOGOUT_TRANSITION_STATIC.md`)
> ปมของ GT-026 ท่อน B = response shape ไหนทำให้ client เปลี่ยนหน้า · agent D แกะได้ (grounding สำคัญ):
> - 🔴 **echo (HYP-PF-012) ทำ transition ไม่ได้แน่นอน พร้อมกลไก:** inbound `0x446F30` = actor-vital **reconcile pass ล้วน** ไม่มี branch เปลี่ยน scene/state/connection ⇒ echo LogoutVital กลับไปไม่มีวันทริกเกอร์การเปลี่ยนหน้า
> - **การ transition จริงขับโดย session/connection orchestrator (vtable `0xf45030`, methods 0x719c30/0x719ab0/0x719b90)** ที่ **รอ แล้ว tear down connection** ผ่าน virtual [+0xf4] gate ที่ mode +0x28 ∈ {1,4} + timestamp +0x24 = รูปของ client ที่ "รอ server ปิด connection"
> - ⇒ **คำตอบที่ถูกน่าจะเป็น (b) ปิด/redirect GSCN connection ไม่ใช่ echo** · `ReturnSelectServerVital 0x709E` = candidate ชื่อดีสุดของ char-select แต่ **ยังไม่ยืนยัน** (ไม่เจอ code consume) · **static ตัดสิน response shape ไม่ได้** → ต้อง attended A/B
> - **จัดการแล้ว:** เพิ่ม **GT-033 LOGOUT-TRANSITION A/B** ในคิว (PENDING · บล็อกด้วยงาน chief) · **งาน chief รอบถัดไป (pre-approved policy #4 "แก้ปุ่มออกเกม"):** สร้าง 2 opt-in variant headless-proven — A `--logout-close-connection-scenario` (ปิด socket จริง reuse close path ไม่มี encoder ใหม่ = ถูกและตรงกับ finding มากสุด) · B `--logout-return-select-server-scenario` (ส่ง 0x709E · ต้องแกะ payload) · attended บอกว่า variant ไหนทำให้ client กลับ char-select จริง → ปลด HYP-PF-012 evidence_gap + ข้อ 8 ของ GT-026
>
> ### 📌 คำถามค้าง / งานที่จงใจเลื่อน (ไม่เปลี่ยนจากรอบ 97/98/99)
> - 🆕 **LogoutVital redesign = งาน dev ถัดไปที่มี spec ครบ** (GT-033 + agent D) — echo ตกไปแล้ว · เดิน variant A ก่อน (ถูก/ตรง finding)
> - **Door B (HYP-PF-028 attack probe)** = ทำได้หลัง GT-032 ยืนยัน Door A บวก · ctors แกะได้แล้ว (รอบนี้) ⇒ unknown ที่เหลือ = wire delivery + populated behavior row (ไม่ใช่ construct path) · ผลลบ (null) น่าจะมีค่าที่สุด
> - **จบก้อน 2 multiplayer (GT-030 รัน) ต้องกลับให้ Panya เคาะก่อนก้อน 3** · HYP-PF-025 เหลือ 1 slot
> - persistence Lane 2/3 เลื่อนท้ายสุด (ไม่ถามซ้ำ) · `verify_foundation.ps1` re-pin/ปลดระวาง · `.gitignore !/.github/` · `git remote` ยังไม่มี = คำถามค้างเดิม
> - **milestone สำรอง not_started ที่เหลือ:** `pvp_engagement` (มี PVP_PROPERTIES table 112 + client PvP warning dialog) · `mob_aggro_and_server_ai` (Door B) · monster_spawn_loot เปิดแล้วรอบนี้เป็น design draft
>
> ### nonclaims ของรอบ 100
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่ flip/แตะ coverage row ใด ๆ · ไม่เพิ่ม ledger · ไม่แตะ census · ไม่แตะ v141 · ไม่แตะ `LOCK_GAME` · ไม่มี runtime observation ใหม่**
> · draft = **ดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** — loot roll order/RNG, ground-object transport, new-item identity policy กู้ไม่ได้ทั้งหมด · client drop tables ครบสำหรับ normal/equipment/specially แต่ "ต้นฉบับ roll ฝั่งไหน" = [UNKNOWN] · quest drops หายไป ~87% ฝั่ง client · ประตู 3/4 = **ไม่มี wire path** (ชื่อ/id เดา เท่านั้น) · Door B correction พิสูจน์ construct path ไม่ claim ว่า NPC โจมตีได้วันนี้ · (player 1, monster 6) = คู่ศัตรูจริงใน FACTION table แต่ค่า player=1 เป็นของเรา · full suite รันบน Windows เท่านั้น

