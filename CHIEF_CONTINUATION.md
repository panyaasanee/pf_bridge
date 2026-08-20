# PIRATE FORCE — Chief Architect continuation file

> ## 🆕🆕 รอบ 103 (2026-08-20 13:3x → 13:4x · manual-fire โดย Panya) — **⭐ URGENT ORDER executed ครบถ้วน: allowlist `.github/` + track CI workflow — commit เขียวรวด · จบรอบทันทีตามคำสั่ง ไม่หยิบงานอื่น**
>
> **HEAD `eab98e6` → `2de7d11` (job 165 — จ็อบเดียว allGreen · ถือ LOCK_GIT 13:34→13:41 จ็อบเขียน HELD/RELEASED เอง)** · commit **3 paths**: `.gitignore` (+8 บรรทัดต่อท้าย: คอมเมนต์เล่าเหตุ + `!/.github/` + `!/.github/**`) · `.github/workflows/gate-windows.yml` (489 บรรทัด) · `.github/workflows/README_GATE_CI.md` (411 บรรทัด)
> - **เงื่อนไขจบของ Panya ผ่านครบสามข้อ:** ① `git ls-files .github` = **2 บรรทัด** (ก่อนแก้ = ว่าง · จ็อบพิสูจน์สดก่อนแก้: check-ignore ชี้ `.gitignore:1:/*` จริง) ② gate เขียวปกติ — seam ✓ covTest ✓ coverage (OPEN 8 ไม่ขยับ) ✓ ledger 35 ✓ censuses 3 ตัว ✓ full suite ✓ canonical `6BFCEDD5..8FC7` ไม่ขยับ ✓ v141 ✓ diff --check ✓ ③ **fresh clone มี workflow+runbook จริง** coverage=0 ledger=0 (บทเรียนรอบ 87: อยู่บนดิสก์ ≠ อยู่ในรีโป)
> - 📬 บริโภค 2 ใบ: **`1215_PANYA-GOLIVE`** (คำตัดสิน: `VITAL_REGISTRY...tsv` **ขึ้น** · `evidence_screens/` **ขึ้น** · `report_images/` **กันออก—ยังไม่ตัดสิน** · `verify_foundation.ps1` 79-vs-105 **พัก ไม่ใช่ตัวบล็อก** · ลำดับสับสวิตช์: **push → Actions แดงจริงหนึ่งครั้งแล้วเขียวกลับ → ค่อยสับ chief ขึ้น cloud**) + **`1230_URGENT-ORDER-github-only`**
> - 🔴 **chief ไม่แตะ remote/push ตลอดกาลจนกว่า Panya เปลี่ยนกฎ — credential เป็นของท่าน · ท่าน push เอง** · origin โผล่ใน `git remote -v` กลางรอบ = Panya ไม่ใช่ข้อผิดพลาด · `.git\STALE_index.lock_20260820_1210_delete_me` = ซากที่ผู้เทสเปลี่ยนชื่อกันไว้ Panya ลบเอง **ห้ามยุ่ง**
> - **งานรอบถัดไป (จาก GOLIVE letter + ค้างจากรอบ 102 — ห้ามหล่น):** ① กฎ sibling สองรีโป (clone เป็นพี่น้องกัน ชื่อ `Pirate Force ServerProject` + `pf_bridge` เป๊ะ — `tools\pf_vital_name_thunk_static.py:127` พึ่ง `ROOT.parent / "pf_bridge"`) เป็นเอกสาร + **เทสที่ล้มจริงถ้าโครงไม่ตรง** ② ทำ Actions **แดงจริงหนึ่งครั้งแล้วเขียวกลับ** (เช่นใส่อักขระนอก cp874 ชั่วคราว) — *เขียวที่ไม่เคยแดง ไม่ใช่ gate* — ทำได้ต่อเมื่อ Panya push แล้ว ③ rebase `agent_kit\chief_task_prompt_CLOUD_DRAFT.md` (ตกรุ่น 19 ส.ค. 17:40 — เพิ่มกฎ never-drop-untested-queue + กฎเลขจ็อบ 0-prefix) แล้วให้ Panya เห็น diff ④ ตรวจซ้ำ `DRAFT_gitignore_REPO2_20260820.txt` ด้วยตาที่สองก่อน Panya `git init` (ผู้เทสขอเอง) ⑤ static ลำดับหนึ่งค้างจากรอบ 102: populated BEHAVIOR row ใน `B_CONSTDATA` + fight-vital delivery ⑥ GT-037 LOOT-ROLL-001 (dev headless ของ chief) ⑦ งานแม่บ้าน CHIEF_CONTINUATION ~86KB (เลื่อนมาจากรอบนี้ตามคำสั่ง) · GT-034 HOSTILE-NATIVE-001 ยัง ⏸ รอ Panya เคาะเรื่องระยะ/teleport
> - เลขจ็อบ: chief ใช้ 165 ⇒ ถัดไป **166** · ผู้เทส 9xx/0xxx (0-prefix แซงคิวได้) · จดหมายแจ้งผล: `FROM_CHIEF_R103_TO_ATTENDED_20260820_1345.md` · คิว/ledger/coverage ไม่แตะเลยรอบนี้ตามคำสั่ง

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

> ## 🆕🆕 รอบ 99 (2026-08-20 08:2x → 09:2x) — **⭐ Door A ของ mob-aggro ลงจริง: HYP-PF-027 NPC-HOSTILE-001 — NPC ตัวแรกของ Port Royal "ขึ้นศัตรู" ด้วยการจับคู่ faction (ผู้เล่น 1 + NPC 6) · headless-proven ครบ · commit เดียวเขียวรวด**
>
> **HEAD `7a1137c` → `87f0769` (job 161 — จ็อบเดียว allGreen ตั้งแต่รอบแรก)** · commit **16 paths** (9 modified + 7 new) · full suite **1847 passed 1 skipped 3561 subtests** (167 วิ บน Windows) · fresh clone reproduce ครบ (coverage=0 ledger=0 nhVerify=0 nhReplay=0) · ledger APPEND entry **34** (HYP-PF-027 · canonical sha re-pin `9841B53D..` → `E2253C31..`) · canonical DB sha `6BFCEDD5..8FC7` ไม่ขยับ · ถือ `LOCK_GIT` 09:19→09:22 (จ็อบเขียน HELD เอง ปล่อยเอง) · **ไม่แตะ `LOCK_GAME` เลย** · กล่องจดหมายว่างตั้งแต่ต้นรอบ (ทุกใบ consumed แล้ว)
>
> ### ⭐ สิ่งที่ลง: เลน HYP-PF-027 (Door A — pre-approved gameplay มาตรฐาน + ดราฟต์ mob-aggro รอบ 98)
> ดราฟต์รอบ 98 แยกการสู้เป็นสามประตู hostility/attack/hit-lands · Door A (hostility) คือประตูเดียวที่พิสูจน์บนสายแล้ว (SCENE-005) และเป็น checkpoint แรกที่ honest · เลนนี้ทำ Door A นั้นบนของที่พิสูจน์แล้วสองชิ้นเท่านั้น:
> - **SCENE-005 semantics:** faction = BasicAttr bit `0x0400` @ `+0x68` (u32 tag 0x14) · relation lookup `0x4A1D50` เทียบ **สองactor** · คู่ (ผู้เล่น 1, NPC 6) = แดง (runtime pass) · **arena-v2 พิสูจน์ว่า NPC 6 เดี่ยว vs ผู้เล่น 0 (ค่าคอนสตรัคเตอร์) = เป็นกลาง** (นับ 1,023 ครั้ง) ⇒ **ต้องส่งสองข้าง ไม่งั้น re-run negative**
> - **HYP-PF-023 transport:** ท่อ actor-entry (`0x6E9D` v4 · derived mask 0x02 · actor_type 4 · NPC `0x2001`) พก BasicAttr อยู่แล้ว (GT-022/025 PASS)
> **sweep 1 เฟรม (`HOSTILE_SPAWN`) + entry recompose:**
> - **ครึ่ง sweep:** เฟรม SPAWN ของ HYP-PF-023 เป๊ะ + splice 5 ไบต์ (bit 0x0400 = faction 6 · mask 0x030C → 0x070C) · **guard แข็งสุด = cross-lane byte equality** เทียบ PC กับ composer ของ HYP-PF-023 เอง (module + profile object ของพ่อ) → เลนนี้ drift จากพ่อได้ก็ต่อเมื่อ verifier สองตัวแดงพร้อมกัน · ค่าคงที่ copy + drift test ไม่ import
> - **ครึ่ง entry:** runtime recompose StartGame ผ่าน `player_wire.make_actor_attr_with_basic_faction` (frozen · รับแค่ faction 1 · scene_seq 0 · scene 1/2) **เฉพาะ identity `0x10010001`** · identity อื่น/serializer refuse/length drift → fallback production bytes + named event → dispatch ปฏิเสธ `..._player_faction_not_applied_no_reply` (ผู้เทสเห็นคู่ครบหรือไม่เห็นเลย)
> - **nonclaim บังคับ:** faction 1/6 เป็นของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล · ไม่มี name bit บน spawn (ดูเส้นขอบ+แผง Tab ไม่ใช่ป้ายชื่อ) · ไม่มี aggro/attack (Door B ยังปิด) · ไม่มี persistence
>
> ### ใบเสร็จ (headless-proven ทั้งหมด — client ยังไม่เคยเห็นแม้แต่ไบต์เดียว)
> `tools/verify_npc_hostile_encoder.py` **63 guards** (diff byte-for-byte กับ SPAWN composer ของพ่อ + ขับ refusal ทุกตัว) · `tools/pf_npc_hostile_headless_replay.py` **52 guards** ผ่าน dispatcher จริงบนสำเนา DB — walker อิสระ**อ่าน faction กลับจากไบต์ที่ dispatch จริง** + ยืนยัน StartGame พก faction-1 attr (production ไม่พก) · เทส **44 + 24 subtests** (`test_npc_hostile_hypothesis` + `test_npc_hostile_dispatch`)
> census re-pin: `pf_runtimeres_actor_entry_static.py` actor-entry sites **6→7** + modules **5→6** (โมดูลใหม่ named) · **timer census ทั้งสาม (SET/FORBID/mention 0x0080) ไม่ขยับเลย** — โมดูลใหม่ไม่เคยเอ่ย 0x0080 เลย (forbid ทุกบิตนอก 0x070C ด้วย mask equality) ⇒ **นั่นคือ guard ที่พิสูจน์ว่า builder ที่ 7 ไม่ใช่ตัวฆ่าตัวที่ 3** · report NOTE + COUNTS + test pins ครบ · `.gitignore` allowlist +3 (2 tools + report) · **coverage ไม่แตะเลย** (precedent damage lane: เลน gameplay อยู่ใน ledger อย่างเดียว ไม่มีแถว matrix ของตัวเอง ⇒ seam digest ไม่ re-pin · แถว `mob_aggro_and_server_ai` ยัง not_started จนกว่า client เห็น)
>
> ### คิว attended พร้อมรอบใหญ่ #9 (เพิ่มของใหม่)
> - 🆕 **GT-032 NPC-HOSTILE-001 = PENDING** ที่ `87f0769` — boot `--npc-hostile-hypothesis-scenario` · 1 เฟรม · **คำถามหลัก: NPC `0x2001` ขึ้นแดง (เส้นขอบ/แผง Tab) เหมือน SCENE-005 ไหม** · ⛔ ผลลบมีค่า: ถ้าไม่แดง = faction บิตตอน spawn บนท่อ actor-entry ไปไม่ถึง relation read (redirect Door A) · ตารางถ่าย+เกณฑ์สองชั้นครบในคิว · จบด้วย End task
> - GT-030/031/027/028/029/026 + GT-001 re-arm ยัง PENDING เหมือนเดิม · **GT-001 ควร re-arm ที่ `87f0769`** (commit นี้แตะ src/ runtime.py + app.py — ทุกจุดหลังธง opt-in ความเสี่ยงต่ำ)
> - เลขจ็อบ: chief ใช้ **161** ⇒ **chief ถัดไป 162** · ผู้เทส **933**
>
> ### 🧾 ธุรการ + งานแม่บ้าน
> - 🧹 **GAME_TEST_QUEUE.md = 65KB** (เกิน ~60KB) — **แต่ overage เป็นของ load-bearing:** 7 GT ที่ยัง PENDING + PLAYBOOK/บทเรียนเครื่องมือที่ **skill `pf-attended-test` อ่านจากไฟล์นี้โดยตรง** (SKILL.md บรรทัด 37/53 ชี้มาที่นี่) ⇒ archive ไม่ได้จนกว่า GT พวกนั้นปิด · รอบนี้ trim pointer รอบ-52 ที่ซ้ำซ้อนแล้ว · **การลดจริงเกิดตอนรอบใหญ่ #9 รันแล้ว GT ปิดเป็น stub**
> - CHIEF_CONTINUATION.md = 66KB (ยังไม่ถึง 100KB)
> - static-RE questions เปิดค้าง 4 ข้อ (จากดราฟต์รอบ 98 · ไม่เปลี่ยน): ① walk `CActorTask_UseBehavior`/`PlayActionEvent` ctors (Door B) ② field ที่ `CAIStateCombatProxy` อ่าน ③ parse `Data/B_CONSTDATA_TH.pc_` หา behavior row ④ singletons `[0x10339B0]`/`[localplayer+0x420]`
>
> ### 📌 คำถามค้าง / งานที่จงใจเลื่อน (ไม่เปลี่ยนจากรอบ 97/98)
> - **Door B (HYP-PF-028 attack probe) = ทำได้หลัง GT-032 ยืนยัน Door A บวก** · pre-approved ใต้ pattern มาตรฐาน · ผลลบ (lookup คืน null เหมือนเดิม) น่าจะเป็นผลที่มีค่าที่สุด
> - **จบก้อน 2 (GT-030 รัน) ต้องกลับให้ Panya เคาะก่อนก้อน 3** · HYP-PF-025 เหลือ 1 slot · HYP-PF-026/027 เหลือ 2 slots ต่ออัน
> - persistence Lane 2/3 เลื่อนท้ายสุด (ไม่ถามซ้ำ) · `verify_foundation.ps1` re-pin/ปลดระวาง · `.gitignore !/.github/` · `git remote` ยังไม่มี = คำถามค้างเดิม
> - **milestone สำรอง not_started ที่เหลือ:** `monster_spawn_and_loot` · `pvp_engagement` — รอบหน้าถ้าไม่มีจดหมาย/ผลเทส แนะนำเดิน Door B (HYP-PF-028) หรือ design draft ของ monster_spawn
>
> ### nonclaims ของรอบ 99
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่ flip/แตะ coverage row ใด ๆ · ไม่แตะ v141 · ไม่แตะ `LOCK_GAME` · ไม่แตะ HYP-PF-022/023/024/025/026 หรือไบต์ของมัน (พิสูจน์ด้วย equality)**
> · **ไม่มี runtime observation ใหม่เลย** — NPC hostile presentation ยังไม่เคยถูกส่งให้ client (นั่นคือ GT-032) · ไม่ claim ว่าคู่ (1,6) ทำงานบน NPC ที่ project ผ่าน actor-entry เหมือน scene-load · ไม่ claim ว่า NPC โจมตีได้ (Door B ปิด) · faction 1/6 = การนับ/ประกอบของเราเอง ไม่ใช่ข้ออ้างเรื่องเซิร์ฟเวอร์ต้นฉบับ · full suite รันบน Windows เท่านั้น


> ## 🆕🆕 รอบ 98 (2026-08-20 07:4x → 08:2x) — **⭐ ปิดช่องว่าง "static RE เส้น server AI ยังไม่มีเลย": design draft MOB-AGGRO / server-AI ลง worktree · commit docs-only เขียวรวด**
>
> **HEAD `af10536` → `7a1137c` (job 160 — จ็อบเดียว allGreen ตั้งแต่รอบแรก)** · commit **2 paths เท่านั้น** (draft + `.gitignore` allowlist) · full suite **1803 passed 1 skipped** (162 วิ) · fresh clone reproduce ครบ (draftPresent=yes coverage=0 ledger=0) · **ไม่แตะ ledger/coverage/census เลย** (entries=33 · OPEN DOMAINS 8 · runtimeres 152 · hp 191 นิ่งหมด) · canonical sha `6BFCEDD5..8FC7` ไม่ขยับ · ถือ `LOCK_GIT` 08:15→08:18 (จ็อบเขียน HELD เอง ปล่อยเอง) · **ไม่แตะ `LOCK_GAME` เลย** · กล่องจดหมายว่าง (ทุกใบ consumed แล้ว · R97 ยืนยัน)
>
> ### ⭐ สิ่งที่ลง: `drafts/MOB_AGGRO_SERVER_AI_STATIC_AND_DESIGN_R98_20260820.md` (252 บรรทัด · ASCII ล้วน)
> รอบนี้เลือก **milestone สำรอง pre-approved** `mob_aggro_and_server_ai` (แถว not_started) ตามที่บล็อกรอบ 96/97 แนะนำเอง — spawn ลูกมือ static RE ขนาน 3 ตัว (in-repo fact pack + binary token sweep + combat-state entry dig) แล้วเขียนเป็น design draft ไม่ใช่ lane เพราะ **ความจริงคือถนนส่วนใหญ่ยังไม่ถูกสร้าง**
> **ของใหม่ที่ไม่เคยมีรายงานไหนแกะ:**
> - client มี **local mob-AI FSM เต็ม** ใน RTTI (`CAIStateRamble{_Idle,_Walk}` → `CAIStateCombat`+`CAIStateCombatProxy` → `CAIState_Dead` · `CAIControler/Condition/Behavior` · `PatrolPath` · `MobLuaProxy_Client`) — **แต่ไม่มี live xref นอก registrar และไม่เคยยิงให้ CNetNPC ที่ server project เลย** ⇒ เป็นระบบ client-side/offline ไม่ใช่ตัวขับจากสาย
> - **attack animation vocabulary ~625 คลิป** (`_f_attack_*`/`_c_attack_*` ใน `Data/GC/A/`) เลือกด้วย **BEHAVIOR row** (`.beh` schema: `s_ANIMATION`/`s_HIT_KEYFRAME`/`n_RANGE`/`n_DAMAGE_AREA`) ไม่ใช่ task literal (ต่างจาก `_F_DIE_000`)
> - **task-id space:** id = KIND (`0x80000002/4/5/6`) ไม่ unique ต่อคลาส · family มี `UseBehavior`/`PlayActionEvent`/`Knockdown`/`Stun`/`Dodge`/… **ไม่มี `CActorTask_Attack`**
>
> ### ⭐ ข้อสรุปดีไซน์ (สามประตูของการสู้ เรียงตามความพิสูจน์แล้ว)
> - **Door A HOSTILITY = พิสูจน์แล้วบนสาย:** faction = BasicAttr bit `0x0400` @ `+0x68` · SCENE-005 runtime pass ทำชื่อแดงได้ · ท่อ actor-entry (HYP-PF-023) พก BasicAttr อยู่แล้ว ⇒ **ทำ NPC 0x2001 ให้ขึ้นศัตรูได้เลยด้วยสองกลไกที่พิสูจน์แล้ว**
> - **Door C HIT LANDS = ของเราแล้ว:** damage (GT-024 ถ่ายภาพ) + death (GT-019 หน้าต่างตาย) + HYP-PF-026 เชื่อมแล้ว
> - **Door B ATTACK = ยังไม่พิสูจน์:** ทริกเกอร์เดียวในไบนารีคือ behavior-id vital (`CHitResult+0x22` / `CKnockdownVital+0x20`) → BEHAVIOR lookup `0x702A10` · **แต่ทุก lookup ที่เคยเห็นคืน null · inbound ActionVital พิสูจน์แล้วว่า inert (SCENE-008) · ไม่มี capture ต้นฉบับ · ไม่มี encoder** ⇒ นี่คือ blocker
>
> ### เสนอ checkpoint ถัดไป (ยังไม่ได้ทำ — เป็นข้อเสนอในดราฟต์)
> - **HYP-PF-027 "NPC HOSTILE PRESENTATION"** = ประตูถูก+พิสูจน์แล้ว: scenario opt-in project 0x2001 + BasicAttr `0x0400` อย่างเดียว · headless-provable วันนี้ + attended GT ถาม "NPC ขึ้นแดงเหมือนผู้เล่นไหม" · **ต้อง ledger entry ใหม่ + re-pin runtimeres census** (บทเรียนรอบ 96 — โมดูล src/ ที่ build actor entry ขยับ census)
> - **HYP-PF-028 "attack probe"** (ทำหลัง A เท่านั้น) = ประตูแพง+ไม่แน่: `CKnockdownVital` behavior key ชี้ `7101.beh` (`_F_ATTACK_018`) · **ผลลบ (null เหมือนเดิม) น่าจะเป็นผลที่มีค่าที่สุด**
>
> ### 🧾 ธุรการ
> - เลขจ็อบ: chief ใช้ **160** ⇒ **chief ถัดไป 161** · ผู้เทส **933**
> - **ไม่เพิ่ม attended test รอบนี้** (ดราฟต์เป็นดีไซน์ ยังไม่ใช่เฟรมที่เทสได้) ⇒ **GAME_TEST_QUEUE ไม่เปลี่ยน** · คิวรอบใหญ่ #9 (GT-030/031/027/028/029/026 + GT-001 re-arm) ยังค้างเหมือนเดิม
> - 🧹 **GAME_TEST_QUEUE.md ~59.9KB ชนเพดาน ~60KB แล้ว** — รอบหน้าควรทำแม่บ้าน (ย้ายรอบเก่าที่ปิดแล้วไป archive ทิ้ง pointer) ก่อนเติมของใหม่
> - static-RE questions เปิดค้าง 4 ข้อ (เรียงตามคุณค่า): ① walk `CActorTask_UseBehavior`/`PlayActionEvent` ctors (อีกครึ่งของ Door B) ② field ที่ `CAIStateCombatProxy` อ่าน ③ parse `Data/B_CONSTDATA_TH.pc_` หา behavior row จริง ④ singletons `[0x10339B0]`/`[localplayer+0x420]` (หนี้ค้างตั้งแต่รอบ 90)
>
> ### nonclaims ของรอบ 98
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่ flip/แตะ coverage · ไม่เพิ่ม ledger · ไม่แตะ census · ไม่แตะ v141 · ไม่แตะ `LOCK_GAME` · ไม่มี runtime observation ใหม่**
> · draft = **ดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** · ไม่ claim ว่า NPC โจมตีได้วันนี้ (Door B ยังปิด) · Door A พิสูจน์แค่บน "ผู้เล่น" — project ลง NPC คือคำถามที่ HYP-PF-027 จะตอบ · coverage row `mob_aggro_and_server_ai` **ยัง not_started** (ไม่มี client เห็นอะไร)

> ## 🆕🆕 รอบ 97 (2026-08-20 05:5x → 07:4x) — **⭐ ชิ้นกลางของวง "ตี → เลือด → ตาย" ลงจริง: HYP-PF-026 DAMAGE-HP-LINK-001 — damage ของเราลด HP ที่ server ถือเอง แล้วบอก client ทั้งสองครึ่ง · headless-proven ครบ · commit เดียวเขียวรวด**
>
> **HEAD `8dfd303` → `af10536` (job 159 — จ็อบเดียว เขียวหมดตั้งแต่รอบแรก)** · commit เดียว 14 paths · full suite **1803 passed 1 skipped** (167 วิ) · fresh clone reproduce ครบ (ledger=0 coverage=0 hplEnc=0 hplReplay=0) · ledger APPEND entry **33** (index เก่านิ่งหมด) · canonical sha `6BFCEDD5..8FC7` ไม่ขยับ · ถือ `LOCK_GIT` 07:28→07:32 (จ็อบปล่อยเอง) · **ไม่แตะ `LOCK_GAME` เลย** · กล่องจดหมายว่าง (ทุกใบ consumed ตั้งแต่รอบก่อน)
>
> ### ⭐ สิ่งที่ลง: เลนเชื่อม (นโยบาย #11 ของ Panya — damage model "ทาง 1" อนุมัติเต็ม + pre-approval gameplay มาตรฐาน)
> ปัญหาที่เลนนี้ตอบ: GT-024 เห็นเลขลอยแต่ **HP ไม่ลด (ยืนยันสองปาก)** · GT-019 เห็น hp 0 + timer เปิดหน้าต่างตาย · สองอย่างนี้ไม่เคยแตะกัน — และรอบ 83 พิสูจน์ว่า client **ไม่ลบเลขเอง** ⇒ server ต้องพูดทั้งสองครึ่งเอง
> **sweep 8 เฟรม opt-in เดียว (`--damage-hp-link-hypothesis-scenario`) · 15 วิ/เฟรม · one-shot:**
> `HP_BASELINE`(100/100) → `HIT_WEAK`(-63) → `HP_AFTER_WEAK`(**37 = 100−63 คำนวณจริง ไม่ได้ pin มือ**) → `MISS`(0) → `HP_AFTER_MISS`(37 ซ้ำ — control ไบต์เหมือนเป๊ะ) → `HIT_STRONG`(-379) → `HP_ZERO_DYING`(**clamp 37−379 → floor 0** + timer 20.0 เฟรมเดียว = ท่า GT-019) → `DYING_ELAPSED`(timer 0.0 = ท่า GT-023)
> - **balance ladder `(100,100,37,37,37,37,0,0)` re-walk ด้วยเลขคณิตจริงทุกครั้งที่ compose** — ไม่ตรง = refuse (`hp_arithmetic_not_reproducible`)
> - ⭐ **guard แข็งสุดของเลน: cross-lane byte equality** — เฟรม hit ทุกใบ compose ผ่าน composer ของเลน HYP-PF-024 เอง (unlock ของมันเอง) แล้วเทียบ `==` ไบต์ · เฟรม hp เทียบกับ composer ของ HYP-PF-022 เอง ⇒ เลนนี้ drift จากพ่อแม่ได้ก็ต่อเมื่อ verifier สองตัวแดงพร้อมกัน · ค่าคงที่ทั้งหมด **copy + drift test ไม่ import** (containment census ห้ามชื่อโมดูลข้ามกัน)
> - 🆕 **แคบกว่าทุกเลนเพื่อน: identity-pinned dispatch** — ยิงได้เฉพาะ selected = `0x10010001` (canonical smoke) ไม่งั้น `..._identity_not_pinned_no_reply` ⇒ ผู้เทสเห็นไบต์ตรง pin เป๊ะหรือไม่เห็นเลย
> - nonclaim ติดทุกที่: **สูตรและการเชื่อมเป็นของเรา — ต้นฉบับกู้ไม่ได้ตลอดกาล · ไม่มีคอลัมน์ HP ใน DB และไม่ได้เพิ่ม** (balance ตายพร้อม sweep) · ไม่มี path คืนชีพ (คำต้องห้ามสามคำไม่ปรากฏใน src)
>
> ### ใบเสร็จ (headless-proven ทั้งหมด — client ยังไม่เคยเห็นแม้แต่ไบต์เดียว)
> `tools/verify_damage_hp_link_encoder.py` **270 guards** (ไม่มีโหมด --binary — เลนนี้ไม่ pin อะไรใหม่จากอิมเมจ ใช้ cross-lane equality แทน) · `tools/pf_damage_hp_link_headless_replay.py` **198 guards** ผ่าน dispatcher จริงบนสำเนา DB — walker อิสระ**อ่าน ladder กลับจากไบต์ที่ dispatch จริง** (hp ที่อ่านได้ต้องเท่ากับเลขคณิตบนไบต์ ไม่ใช่บนโมดูล) · เทส **141 + 44** · **48 named refusals** · pc sizes 106/84/106/84/106/84/111/111
> census re-pin 2 ตัวพร้อมเหตุผลข้างตัวเลข (ธรรมเนียมรอบ 90/96): `src_vital_stream_call_sites` 14→15 · `src_modules_mentioning_basicattr_bit_0x0080` 4→5 (+NOTE ต่อท้าย report — SET/FORBID census ไม่ขยับ เลนนี้ไม่ build actor entry) · `.gitignore` allowlist +3 (จับได้โดยเทส EVIDENCE-VISIBLE ใน sandbox ก่อน commit — ระบบทำงาน) · **coverage ไม่แตะเลย** (precedent HYP-PF-024: เลน damage อยู่ใน ledger อย่างเดียว ไม่มีแถว matrix ของตัวเอง ⇒ seam digest ไม่ re-pin)
>
> ### คิว attended พร้อมรอบใหญ่ #9 (อัปเดตแล้ว)
> - 🆕 **GT-031 DAMAGE-HP-LINK = PENDING** — boot `--damage-hp-link-hypothesis-scenario` · 8 เฟรม/105 วิ · ตารางถ่ายทีละเฟรม+เกณฑ์สองชั้นครบในคิว · **คำถามหลัก: หลอดลดเหลือ 37 ที่เฟรม +30 ไหม** · ⛔ ตื่นเต้นพิเศษ: หลอดลดตอนเฟรมเลข = หักล้างรอบ 83 (ผลลบมีค่าที่สุด) · จบเทสต้อง End task (ห้ามกดปุ่มหน้าต่างตาย)
> - **GT-001 re-arm ที่ `af10536`** (ครอบ commit รอบ 96+97 — ทุกจุดหลังธง opt-in) · GT-030/027/028/029/026 ยัง PENDING เหมือนเดิม · GT-028 ได้ทางเลือกใหม่: ภาพ `63`/`MISS` เก็บจาก GT-031 ได้เลยถ้า GT-027 ลบ
> - เลขจ็อบ: chief ใช้ 159 ⇒ **chief ถัดไป 160** · ผู้เทส **933**
>
> ### 📌 คำถามค้าง / งานที่จงใจเลื่อน (ไม่เปลี่ยนจากรอบ 96)
> - **จบก้อน 2 (GT-030 รัน) ต้องกลับให้ Panya เคาะก่อนก้อน 3** · HYP-PF-025 เหลือ 1 version slot · HYP-PF-026 เหลือ 2 slots
> - persistence Lane 2/3 เลื่อนท้ายสุด (ไม่ถามซ้ำ) · `verify_foundation.ps1` re-pin/ปลดระวาง · `.gitignore !/.github/` · `git remote` ยังไม่มี = คำถามค้างเดิม
> - **แถว not_started ที่เหลือเป็น milestone สำรอง:** `mob_aggro_and_server_ai` (ชิ้นถัดไปธรรมชาติของ combat — NPC โต้กลับ) · `monster_spawn_and_loot` — รอบหน้าถ้าไม่มีจดหมาย/ผลเทสให้ประมวล แนะนำเริ่ม design draft ของ mob_aggro (static RE เส้น server AI ยังไม่มีเลย)
>
> ### nonclaims ของรอบ 97
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่ flip/แตะ coverage row ใด ๆ · ไม่แตะ v141 · ไม่แตะ `LOCK_GAME` · ไม่แตะ HYP-PF-022/023/024/025 (ไบต์เดิมทุกเลน — พิสูจน์ด้วย equality)**
> · **ไม่มี runtime observation ใหม่เลย** — วงเต็มยังไม่เคยถูกส่งให้ client เห็น (นั่นคือ GT-031) · ไม่ claim ว่าหลอดจะลดจริงบนจอ · ไม่ claim ว่า GT-019/023 behaviours compose กันได้ในหนึ่ง sweep (นั่นคือคำถามของเทส)

## รอบ 93 + 95 + 96 — ⤴ ย้ายไป archive แล้ว (รอบ 102)

> ฉบับเต็ม: `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R93_R95_R96.md`
> ใจความที่ยังต้องรู้: R93 ปิดหนี้ gate-reproducible + แก้ GT-024 ด้วยไบต์ (FINDINGS_R93 = ท่อแสดงผล CHitResult) ·
> R95 ปิดงบ HYP-PF-024 (3/3) ด้วย profile npc_sweep + IMG-QUERY-001 · R96 เปิด multiplayer ก้อน 2 (HYP-PF-025) ·
> บทเรียน census SET-vs-mention (จ็อบ 156 REFUSED = guard ทำงานถูก) อยู่ในฉบับเต็ม

## รอบ 92 (+ residue ก่อนรอบ 93) — ⤴ ย้ายไป archive แล้ว (รอบ 96)
> เนื้อหาเต็ม: `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R92.md` (ไม่ได้ลบ ไม่ได้แก้)
---

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** รอบเก่า ☕ 26→M13 + คำขอจาก Panya (ตอบครบแล้ว) → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260817.md` ก้อน A

## 0. โครงสร้างทีมคืนนี้ + เช็คก่อนเริ่มทุกครั้ง

### 0.1 ใครทำอะไร (ผู้ใช้สั่ง 04:40 แก้ 04:45)

- **`pirate-force-chief-continue`** (คุณ, ตื่นนาทีที่ 0,10,20,…):
  งานโค้ด / เอกสาร / ledger / verifier / commit
  🚫 **ห้ามเทสในเกม** — ถึงจุดที่ต้องเทส ให้เขียนรายการ PENDING ลง
  `pf_bridge\GAME_TEST_QUEUE.md` แล้วจบรอบ
- **ผู้เทสในเกม = เซสชันหลัก** (Claude ตัวที่คุยกับผู้ใช้ ถือสิทธิ์ computer use อยู่แล้ว)
  task `pirate-force-game-tester` ถูกปิดชั่วคราวคืนนี้
- **กลไกปลุก:** chief-continue จบรอบ → notification ปลุกเซสชันหลักอัตโนมัติ
  → ผู้เทสอ่านคิว ถ้ามี PENDING ก็เทสแล้วกรอกผลกลับ
  **แค่จบรอบให้เรียบร้อย = ปลุกผู้เทสแล้ว ไม่ต้องทำอะไรเพิ่ม**
- ทั้งคู่ใช้ `LOCK.txt` เดียวกัน

### 0.2 เช็คตามลำดับ

1. **`pf_bridge\LOCK.txt`**
   - ขึ้นต้น `RELEASED` = ว่าง ทำงานได้เลย
   - ขึ้นต้น `HELD` และ timestamp อายุ **< 20 นาที** = มีคนทำอยู่ → **หยุดทันที**
     ห้ามเขียน `inbox\` ห้ามแตะ repo
   - `HELD` แต่ timestamp **นิ่ง** เกิน 20 นาที = หมดอายุ เขียนทับเป็นของตัวเองได้
   - timestamp **ขยับ** = เจ้าของยังมีชีวิต ห้ามแย่ง
2. **`pf_bridge\inbox\`** — ถ้ามี `.ps1` ค้าง แปลว่างานก่อนหน้ายังรันไม่จบ → หยุด
3. **`pf_bridge\outbox\`** — อ่านไฟล์ล่าสุด ถ้ามีผลที่ยังไม่วิเคราะห์ ให้อ่านก่อน
4. **`pf_bridge\GAME_TEST_QUEUE.md`** — ถ้ามีรายการที่ผู้เทสกรอก `result` กลับมาแล้ว
   ให้เอามาประมวล/commit ต่อ

---

> 📦 **[ย้ายไป archive 2026-08-18 (chief รอบ 53)]** §1–§35 (ข้อจำกัดเครื่อง §1 · PF BRIDGE §2 ·
> Workspace §3 · Playbook full-loop §7 — สำเนาสดใช้งานอยู่ใน GAME_TEST_QUEUE.md แล้ว ·
> โครงสร้างทีม §16 — ฉบับ authoritative อยู่ใน prompt ของ scheduled task · บันทึกรอบ 41–45 §31–§35)
> → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260818_R53.md`
>
> ⚡ digest ข้อจำกัดที่ยังบังคับ (จาก §1–§3 — รายละเอียดในไฟล์ archive):
> bash=Linux sandbox เท่านั้น งาน Windows ผ่าน PF BRIDGE `.ps1` ASCII → inbox (log UTF-8, quote ทุก path มี space) ·
> request_access ใน scheduled run โดนปฏิเสธเสมอ · เปิดเกมจาก bridge = บล็อก · worktree เดิม 3 path ห้าม clone/สร้างใหม่ ·
> git ใน sandbox: cd เข้า ServerProject + `--no-optional-locks` + หลัง commit `mv HEAD.lock HEAD.lock.stale` ·
> gate จริง = Windows `py -3` ผ่าน bridge · sqlite เปิดจาก sandbox = copy /tmp หรือ mode=ro เท่านั้น · sleep ≤100 วิ

> 📦 **[ย้ายไป archive 2026-08-18 06:1x (chief รอบ 60)]** §36–§44 (บันทึกรอบ 46–54 ปิดครบแล้ว:
> รอบ 46 ดีไซน์ persistence characters/accounts `d0401f0` PROPOSED · รอบ 47+50 probe ลูกมือ Windows
> Claude CLI ผ่าน read `094` + acceptEdits `095` · รอบ 48–49 idle สั้น · รอบ 51 HYP-PF-015 soft delete
> + slot reuse `005b3d4` gate 449/0 · รอบ 52 ประมวลรอบใหญ่ #2 + fix v2 delete ack + ปิดบั๊กระบบ 2 ตัว
> `0411987` + canonical guard · รอบ 53 CHAT-ECHO-002 + HYP-PF-016 headless GREEN TCP จริง →
> GT-012/013 staged + archive §1–§35 · รอบ 54 CHAT-ECHO-004 static 0xAC52 Q1=A `5789f13`)
> → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260818_R60.md`
>
> ⚡ ยังมีผลบังคับ (รายละเอียดใน archive):
> - **ลูกมือ Windows Claude CLI พร้อมใช้** (probe 094 read + 095 acceptEdits ผ่าน — เดิม §37.2/§40.3):
>   full path `& "C:\Users\Panya\.local\bin\claude.exe" -p` · stdout → `.agent_stdout.txt` · กติกา scope/ห้าม
>   commit/ห้ามแตะ canonical อยู่ใน prompt ของ scheduled task แล้ว
> - **❓ คำถามค้าง Panya (รอบ 46, ไม่บล็อก):** ดีไซน์ persistence characters/accounts ยัง PROPOSED
>   รอเคาะ — รายละเอียด §36.2–36.3 ใน archive

## [ARCHIVED รอบ 68] §45–§50 (รอบ 55–60) + รอบ 61–63 → pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260818_R67.md

> ย้ายโดย chief รอบ 68 (housekeeping, CONTINUATION ชนเพดาน 100KB) — สรุปหัวเรื่องที่ย้าย:
> §45–47 CHAT-ECHO-005..007 (Q2 render gate/vtable, static) · §46 e1741db/820d473/eb52975
> §48 MOVE-AUTHORITY-001 856f9e9 (client-authoritative movement, static) · §49 MOVE-CADENCE-001 ef9acd7 (headless B)
> §50 CHAT-ECHO-008 cec8c82 (map 10 คลาส Community_*Vital, Grade A static) + แม่บ้าน archive §36–§44
> รอบ 61 TELEPORT-CHECK-001 · รอบ 62 NAMEID-HASH-001 · รอบ 63 NAMEID-RESOLVE-001 (static, นำไปสู่กำแพง v141 ในรอบ 64)

## รอบ 64–67 — ⤴ ย้ายไป archive แล้ว (รอบ 75)

รอบ 64 (NAMES fold ชนกำแพง v141-immutable → revert · ซ่อม manifest 61–63 · commit `561cb02`) ·
รอบ 65 (occupied_destination_policy → HYP-PF-017 swap headless · commit `9126fb5`) ·
รอบ 66 (same_slot_noop blocked→runtime_pass · commit `e2fca8a`) ·
รอบ 67 (move_negative_paths isolation → MOVE-ISOLATION-001 · commit `2f82af9`)
→ เนื้อหาเต็มอยู่ที่ `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260818_R72.md`

## รอบ 68–71 — ⤴ ย้ายไป archive แล้ว (รอบ 76)

> 📦 `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260818_R76.md`
> - **รอบ 68** SPLIT-OPERATE-001 `950819c` — inventory/split_stack not_started→in_progress, ItemOperate opcode space
> - **รอบ 69** SPLIT-OPERATE-002 `08fb65b` — op6 = quantity-op family 4 call-site
> - **รอบ 70** SPLIT-OPERATE-003 `ab89a24` — verb 0x16 two-panel, static caption route ปิด (เหลือ live capture)
> - **รอบ 71** ITEM-MERGE-001 / HYP-PF-018 `8282a21` — generalized same-template merge, headless wire/DB proven
> ⚡ ที่ยังบังคับอยู่จากสี่รอบนี้: **ป้าย "numeric-input dialog resource 0x12" @0x5A34D7 ของ SPLIT-OPERATE-001/002 ถูกแก้แล้วในรอบ 75** (จริง ๆ คือ MSVC EH trylevel store) — โครงสร้างที่พิสูจน์ไม่กระทบ · GT-015 ต้องการ live capture เท่านั้น

## รอบ 72–75 — ⤴ ย้ายไป archive แล้ว (รอบ 77)

> `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260818_R77.md` — เนื้อหาครบไม่ตัดทอน
> · รอบ 72 MOVE-AUTHORITY-001 `6577626` · รอบ 73→74 MOVE-PROJECT-001 `f0f1968`
> · รอบ 75 USE-DROP-SELL-001 + CHAT-CHANNEL-001 `b2e4669`

## รอบ 76–78 — ⤴ ย้ายไป archive แล้ว (รอบ 81)

> เนื้อหาเต็มของ **รอบ 76 (CHAT-CHANNEL-002/003), รอบ 77 (MULTIPLAYER-READINESS-AUDIT-001),
> รอบ 78 (STATS-PROG-002 + MP-AUDIT-FOLLOWUP-001)** อยู่ที่
> `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260819_R78.md`
>
> สิ่งที่ยังต้องรู้จากสามรอบนี้โดยไม่ต้องเปิด archive:
> - **MP-AUDIT-FOLLOWUP-001 (รอบ 78) ตอบ G1 ของ audit ไปแล้วระดับ ①** — `actor_type` 2..6 =
>   CNetActor / CMyActor / CNetNPC / CAvatarNPC / Pet · **remote player = 2** · F8 ปิด · G2 แคบลง
>   ⇒ **Option 1 ส่วน (a) เสร็จตั้งแต่รอบ 78 ห้ามทำซ้ำ** (รอบ 81 เกือบสั่งลูกมือทำซ้ำ)
> - audit รอบ 77 = ต้นทางของคำถาม G1–G9 และของคำตัดสิน Option 1 ของ Panya
> - รอบ 79 ไม่มีบันทึก: ถือ LOCK 18:2x แล้วตายเงียบ 5h42m โดยไม่ spawn อะไรเลย

---

## รอบ 80–81 — ⤴ ย้ายไป archive แล้ว (รอบ 83)

`archive\CHIEF_CONTINUATION_ARCHIVE_20260819_R80_R81.md`
· รอบ 80 = UI-REFRESH-001 + HP-DEATH-001 · รอบ 81 = สี่ lane ขนาน (NAMES/DELETE-REFRESH/HP-DEATH-002/MP-OPT1-B)
· **ทั้งสี่ lane ของรอบ 81 ถูกเทสจริงในรอบใหญ่ #4-#5 และ PASS หมด** — ผลอยู่ในรอบ 83


## รอบ 82–83 — ⤴ ย้ายไป archive แล้ว (รอบ 85)

> เนื้อหาเต็มของ **รอบ 82 (CORPUS-PIN-001), รอบ 83 (DAMAGE-MODEL-001)** อยู่ที่
> `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260819_R82_R83.md`
>
> สิ่งที่ยังต้องรู้จากสองรอบนี้โดยไม่ต้องเปิด archive:
> - **`docs/PF_CAPTURE_CORPUS.json` = บ้านเดียวของชุดหลักฐาน** (รอบ 82) — เลิกถามไดเรกทอรีว่าไฟล์ไหนคือหลักฐาน
>   ตัวเลขที่เผยแพร่ = **44 จาก 67** (ไม่ใช่ 69 · 2 live tail ถูกกันออกโดยระบุชื่อ) · ถ้าตัวตรวจ corpus แดง
>   **ห้าม regenerate ตารางให้เขียว** ให้ไปหาจ็อบที่เขียนทับหลักฐาน
> - **รอบ 83 พิสูจน์ว่า client ไม่คำนวณ damage เอง** — ตัวเลขที่ลอยขึ้นคือ **i32 มีเครื่องหมาย** ที่ server
>   วางไว้ที่ hit entry `+0x08` ผ่าน abs() แล้วพิมพ์ ⇒ **ตัวเลขต้นฉบับกู้ไม่ได้ตลอดกาล** (ทาง 2 ปิดถาวร)
> - **wire = tagged stream** — ทุก field คือ tag byte 1 ตัวแล้วตามด้วย payload · client เทียบ tag แล้วยก
>   error flag ถ้าไม่ตรง ⇒ **server ต้องส่ง tag ให้ตรงเป๊ะ ไม่ใช่แค่ความกว้างถูก** · hit result = 5 field
>   แล้วตามด้วย array ของ entry ละ 32 ไบต์ (target id · i32 damage · position vec · reaction angle · u16 flag)
> - **`DURATION_DYING` = 20** (อ่านจากอิมเมจรอบ 83) — ปิดหนี้ค่า placeholder 60.0f ของรอบ 81
> - 🔴 **รอบ 85 หักล้างพาดหัวรอบ 83 หนึ่งประโยค** — ดูรอบ 85 หัวข้อ RUNTIMERES-ACTOR-ENTRY-001 และ
>   erratum ที่ต่อท้าย `reports/PF_HP_DEATH001_HP_DEATH_AND_RESPAWN_STATIC_20260819.md`

---

## รอบ 84–85 — ⤴ ย้ายไป archive แล้ว (รอบ 87)

อยู่ที่ `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260819_R84_R85.md` (ไม่ได้ลบ ไม่ได้แก้)
· รอบ 84 = DYING-HOLD-001 + ATTENDED-EVIDENCE-001 + SCAN-DEBT-001 → commit `8360f57`
· รอบ 85 = NAMES-FOLD-002 + RUNTIMERES-ACTOR-ENTRY-001 + RESOLVE-SCOPE-001 → commit `32878e0`
· เรื่องเล่าฉบับเต็มของทั้งสองรอบอยู่ในข้อความ commit ของมันเองด้วย

## รอบ 86 + 87 — ⤴ ย้ายไป archive แล้ว (รอบ 92)
> เนื้อหาเต็ม: `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R86_R89.md`
> (RUNTIMERES-ENCODER-001 + NAMES-FOLD-003 + COMMENT-ERRATA-002 + LEDGER-VISIBILITY-001 + CP874-PORTABILITY-001)
> 🔑 **บทเรียนที่ยังใช้อยู่ อย่าลืม:** เครื่องมือห้ามพิมพ์อักขระนอก cp874 ออก console (อีโมจิทำ gate แดงเฉพาะบน Windows)
> · *"check ที่ไม่เคยเห็นมันแดง ไม่ใช่ check"*

## รอบ 89 — ⤴ ย้ายไป archive แล้ว (รอบ 92)
> เนื้อหาเต็ม: `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R86_R89.md`
> (บัญชีใหม่รอบแรก · DEATH-ESCALATE-001 + BRIDGE-LIVENESS-001 + งานแม่บ้านส่งกะ)

## รอบ 90 (ถูกตัดกลางคัน) + รอบ 91 — ⤴ ย้ายไป archive แล้ว (รอบ 95)

> ฉบับเต็ม: `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R90_R91.md`
> ใจความ: จ็อบ 145 แดงหนึ่ง guard จึงไม่ commit (fail closed ทำงาน) · รอบ 90 ถูกตัดกลางซ่อม ·
> รอบ 91 อ่านทรี รันเทสซ้ำจนเขียว แล้ว commit `d4ed4d4` (HYP-PF-024 ลงจริง 16 path) +
> เปิด RUNTIMERES-LATCHONLY-001 (`47c7211`) ตามที่ผู้เทสขอ · บทเรียนหลัก: **guard ที่แดงคือ guard ที่ทำงาน**
> และ **takeover แล้วให้อ่านทรีก่อน อย่าเขียนทับ**
