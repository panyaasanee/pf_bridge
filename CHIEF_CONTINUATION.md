# PIRATE FORCE — Chief Architect continuation file


## รอบ 108–111 + แบนเนอร์ครั้งเดียว 2026-08-20 21:30 — ⤴ ย้ายไป archive แล้ว (รอบ 140)
-> `archive/CHIEF_CONTINUATION_ARCHIVE_20260824_R108_R111.md`
(R111 = HYP-PF-029 NPC-HP-LINK-001 ผ่านจอจริง GT-039 · R110 = คำตอบสี่ข้อ+merge-claude-pr · R109 = ทาง D ci-status · R108 = ท่อ sync + prompt A′)
---

---

## รอบ 107 — ⤴ ย้ายไป archive แล้ว (รอบ 109)

`pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R109_ROUND107.md`
— ดีไซน์ sync ฝั่ง Windows (ทำจริงแล้วรอบ 108) · repo ที่สอง · ข้อเท็จจริงของ Routine
· คำถาม A/B เรื่อง push (เคาะเป็น A′ รอบ 108) · วิธีอ่านผล Actions (เคาะเป็นทาง D รอบ 109)

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

## รอบ 112-150 (บรรทัดดัชนี) — ⤴ ย้ายไป archive แล้ว (รอบ 164)
-> `archive/CHIEF_CONTINUATION_ARCHIVE_20260825_R112_R150.md`
(48 บรรทัดจากช่วง R112-R150 = รายการรอบ 42 + บรรทัดว่าง/บรรทัดต่อ 6 · ครบทุกบรรทัด ไม่มีการลบ · บันทึกเต็มของแต่ละรอบยังอยู่ที่ `rounds/R<NNN>_*.md`)

## รอบ 151-165 (บรรทัดดัชนี) — ⤴ ย้ายไป archive แล้ว (รอบ 179)
-> `archive/CHIEF_CONTINUATION_ARCHIVE_20260826_R151_R165.md`
(15 บรรทัดจากช่วง R151-R165 = รายการรอบ 15 · ครบทุกบรรทัด ไม่มีการลบ · บันทึกเต็มของแต่ละรอบยังอยู่ที่ `rounds/R<NNN>_*.md`)

- R166-R173 (8 รอบ) — ↴ ย้ายไป archive แล้ว (รอบ jsrh00, 2026-08-27) -> `archive/CHIEF_CONTINUATION_ARCHIVE_20260827_R166_R178.md`

## CORE-REQUEST registry — ตัวนับเดียวทุกสาย (COO-DECISION 20260826_0656 · ตารางนี้สร้างโดย chief R174 · ปรับปรุงสถานะล่าสุด R177)

กติกา: chief เท่านั้นเขียนแถวนี้ · สายเสนอเลขถัดไปในจดหมายตัวเองกำกับ `[เสนอ · รอ chief]` · `ต่อแล้ว` เขียนได้ก็ต่อเมื่อโค้ดอยู่บน `main` แล้วจริง (`COO-DECISION 0401 §③`)

| เลข | ใบต้นทาง | จุดเรียก | สถานะ ณ R177 |
|---|---|---|---|
| 001 | LANE-A WORLD-CENSUS-001 (สำมะโน bg0001 115 บนเส้นทางไร้แฟล็ก) | `runtime.py` ประกอบสำมะโนหลัง `super().dispatch()` | ต่อแล้ว — บน `main` (`world_population` import ยืนยันด้วย grep R177) |
| 002 | LANE-A ปลายทางฉาก (`world_scene_travel` destination table) | `runtime.py` แทนที่ `make_login_teleport(1, 0)` ตายตัวด้วย lookup ตามแถวตำแหน่งจริง | ต่อแล้ว — บน `main` (`world_scene_travel` import ยืนยันด้วย grep R177) |
| 003 | LANE-A `world_scene_entry.resolve_entry` (v2, `20260826_0645`) | `runtime.py` login frame ก่อน `make_login_teleport` + `session.py:79 select_and_start` ส่ง `entry.position` | ต่อแล้ว — R176 (`67ff98d`) · `world_scene_entry` import ยืนยันด้วย grep R177 |
| 004 | LANE-A `world_travel_gate.observe` (v2, `20260826_0645`, guard = `active_lanes`) | `runtime.py` บนสุดของ `make_state_class` (`preload()`) + `PersistentGameSessionState.__init__` + ต่อท้ายบล็อก `:3943-3949` | ต่อแล้ว — R176 (`67ff98d`) · `world_travel_gate` import ยืนยันด้วย grep R177 |
| 005 | LANE-B `MOB-COMBAT-001` (`20260826_0355` ฉบับแก้หลัง adversary · อนุมัติ `COO-DECISION 0402`) | `runtime.py` inbound EA7D ActionVital ที่เป้าเป็น field-mob → `mob_combat.attack_from_observed_action` + `commit_step` + `mob_death.kill`/`commit_death` เมื่อ `death_due` | ต่อแล้ว — R177 `pirate-force-server@6105d26` (เลยกำหนดเดิม 26 ส.ค. 08:00 มาแล้ว) · `pf-adversary` บังคับก่อน commit: 2 Low + 1 Informational ติดป้ายในโค้ดครบ ไม่มี CRITICAL/HIGH · สวีตเต็มเขียว(cloud sanity) `3097 passed, 327 skipped, 4986 subtests` · 🔴 **คำถามค้าง (ไม่บล็อก):** ledger/register เป็น per-session ไม่ใช่ server-wide → `CHIEF-ASK-COO 20260826_1600` |
| 006-010 | LANE-GM/LANE-B ต่าง ๆ (GM state, mob_loot/pickup, mob_ai_control, world_scene_liveness ฯลฯ) | `runtime.py` หลายจุด ดูรายละเอียดในบันทึกรอบ R179/R180/R184/R190 | ต่อแล้วทั้งหมดบน `main` ตามบันทึกรอบ (R191 พบว่าตารางนี้ไม่เคยถูกเติมแถว 006-010 แม้โค้ดขึ้น `main` แล้วจริง — หนี้เอกสารที่สืบทอดมาหลายรอบ ไม่บล็อกงาน เสนอ backfill รอบถัดไปที่มีเวลา) |
| 011 | LANE-GM `gm/warp_executor.make_warp_force_pos_frame` (`20260827_0724`, same-scene warp ผ่าน `ForcePos`) | ยังไม่มีจุดเรียกใน `runtime.py`/`app.py` | **[เสนอ · บล็อก]** ยังต่อสายไม่ได้จริง — `handle_gm_run_command_vital` (`CORE-REQUEST-010`) ยัง authorize/capture เฟรม 0x51E9 เท่านั้น ไม่ decode wide-string เป็น `GmCommand` จริง จึงไม่มีทางได้คำสั่ง `warp` จาก client จนกว่าจะมี RE เพิ่มหรือ attended console/debug path (R191 ยืนยันซ้ำ ไม่มีการเปลี่ยนแปลงจาก R190) |
| 012 | LANE-GM `gm/say_wire.make_say_broadcast_frame` (`20260827_1600`, ส่งเฟรม say ผ่าน `Channel_GMGlobalMessageVital`) | ยังไม่มีจุดเรียกใน `runtime.py`/`app.py` | **[เสนอ · บล็อก]** เหตุผลเดียวกับ 011 — ไม่มี `GmCommand` ชนิด `say` จาก client จริงจนกว่า 0x51E9 decode จะพิสูจน์ หรือมีทาง console/debug ตรงสำหรับผู้เทส (R191 บันทึกไว้ตามที่ใบขอ) |
| 013 | LANE-A `world_population_handoff.py` (`20260826_0910`, กันเมืองว่างตอนผู้เล่นออกเมือง) | ยังไม่มีจุดเรียกใน `runtime.py`/`app.py` | **[superseded/moot — `COO-DECISION 20260827_1645`]** เลข `013` เลิกถือเป็น CORE-REQUEST เปิดค้างแล้ว (1144 เคยยืนยันว่ายังไม่ moot แต่ 1645 กลับคำ — เหตุผล: ความเสี่ยงที่ใบพูดถึงเกิดได้ก็ต่อเมื่อ `world_travel_gates` เปิดจริง ซึ่งปิดอยู่โดย policy ของเจ้าของเอง `WORLD_TRAVEL_INERT`, และเลข 006 ถูกสาย GM ใช้ซ้ำไปแล้วโดยไม่มีใครทักท้วง) เปิดใหม่เป็นเลขใหม่ (ไม่ชนใคร) เมื่อไหร่ที่ M2 travel gate เปิดจริง — ไม่ใช่ต่อเลขเดิม |
| 014 | LANE-A `NPCConversation op1` MOBS 156 (Columbus, Port Royal) → quest 3021 → scene 17/`Bg1001` ผ่าน `TeleportVital`/`ForcePos` + bind vehicle module ตาม RE-085 (`20260827_1052`) | `runtime.py`/`app.py` — `columbus_quest_dispatch.py` (ใหม่) + `_dispatch_columbus_quest3021` | **[ต่อสายบางส่วน — R192]** ครึ่งแรก (บทสนทนาเควส 3021) ต่อแล้วจริง บน `pirate-force-server@5d9cfd3` (push แล้ว รอ merge PR) · ครึ่งหลัง (ย้ายฉาก+ผูก vehicle) **ปฏิเสธเสมอ fail-closed** ตั้งใจ — บล็อกด้วยหลักฐานสองใบที่เป็นอิสระต่อกัน: `RE-103` (พิกัด player-arrival ฉาก 17 เปิดรอบนี้) + `RE-096` (payload vehicle bind เปิดค้างจากสาย A) ทั้งคู่เป็นงาน RE runner (local) — ดู `notes_to_chief/20260827_1215_CHIEF-STATUS-*` เรื่องความเสี่ยงต่อกำหนด M2 20:00 |
| 015 | LANE-B `mob_pickup.dispatch_pickup_request()` (`20260827_1514`, ประกอบ 4 ขั้นของ `MOB_PICKUP_WIRING` เป็นฟังก์ชันเดียว, `production_allowed=True`) | ยังไม่มีจุดเรียกใน `runtime.py`/`app.py` | **[เสนอ · บล็อก, ไม่เร่ง]** รอ RE ถอด opcode/decoder ของ inbound pickup request เต็ม (`claimant_identity, x, y, z, object_ref_u32, opaque_u8`) — RE-082 พิสูจน์แค่ element key ยังไม่ครบ · nonclaim 15 (bag_cell/claimant_identity ต้องตรง connection) ตอบแล้ว โดย chief: `runtime.py` ต้องเป็นคนเช็ค `claimant_identity == self.foundation.selected.actor_identity` ก่อนเรียก ไม่ใช่ `mob_pickup.py` เพิ่ม defense-in-depth เอง (`20260827_1550_CHIEF-REPLY`) — คำตอบเก็บไว้ใช้ตอนมี opcode decoder แล้ว ไม่บล็อกวันนี้ตามที่สาย B บอกเอง |
| 016 | LANE-GM `gm.state_wire.GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED` guard (`20260827_1524`, กัน `GM_UpdateGMStateVital` ที่ `GT-101` วัดว่าฆ่า session) | `runtime.py` login block, gate บน `state_wire.GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED is not None` | **ต่อแล้ว — R194** (`pirate-force-server` PR #124, merged) · `RE-105` (STATIC-ON-BRIDGE, DONE/PASS) pin ค่าจริง = `0` — ค่าคงที่อัปเดตจาก `None` เป็น `0` แล้ว guard ยังอยู่ (โครงสร้างเดิม ไม่ลบ) |
| 017 | LANE-GM `gm/login_scene_override.get_login_scene_override` (`20260827_1524`, override scene ที่ client login เข้าไปสำหรับบัญชี GM ที่ตั้งค่าไว้) — 🔴 **จดหมายต้นทางเขียนเลขนี้เป็น "015" ผิด**: LANE-B ยื่น `CORE-REQUEST-015` (mob_pickup) ก่อนหน้า 10 นาที (`1514` vs `1524`) — เลขชนกัน chief ขยับ LANE-GM ตัวนี้เป็น `017` ตามกฎ "ชนแล้วห้ามทับ" (`016` เป็นของ GM เองอยู่แล้ว ไม่ชน) | จุดที่ 1 (login, บังคับ): `runtime.py`'s `START_GAME_REQ` handler, ก่อนเรียก `world_scene_entry.resolve_entry()` · จุดที่ 2 (census ของฉาก override, ผสมข้อมูลข้าม LANE-A/LANE-B ที่ยังไม่มีฟังก์ชันให้เรียก) | **[จุด 1 ต่อแล้ว — R196]** ต่อสายตรงใน `runtime.py` (ไม่ผ่าน `lane_hooks` — เหตุผล: ต้องเปลี่ยนค่า `scene_id` ที่ป้อนเข้า `resolve_entry()`, เกินชนิดที่ `lane_hooks.fire()` ออกแบบไว้ ซึ่งเป็น report-only โดยเจตนา ดูคอมเมนต์ที่ call site) เปลี่ยนเฉพาะ `scene_id` ของ row ที่ป้อนเข้า `resolve_entry()` เท่านั้น (x/y/z/heading เป็นของแถวจริง) จึงยังใช้กฎความปลอดภัยเดิมของ `resolve_entry()` ครบ (ground-evidence, home-never-touched, `login_entry_allowed`) ไม่มีการเปิดช่องพิเศษ · เทส wiring 6 ข้อใหม่ `tests/test_gm_login_scene_override_wiring.py` ขับผ่าน dispatcher จริง (รวม 1 ข้อระดับไบต์ที่พิสูจน์ว่า ActorAttr/MovementAttr ตรงกับ teleport ไม่ใช่แค่ teleport ฝ่ายเดียว) · `pf-adversary` 3 รอบพบและแก้บั๊กจริง 3 จุด compose ก่อน push (รายละเอียดใน `rounds/R196_0vjgyy_*.md`) · **nonclaim**: ถ้า override ชี้ไปฉากที่ปักหมุด `login_entry_allowed=False` (วันนี้: ฉาก 17) login ทั้งครั้งจะถูกปฏิเสธเงียบ (fail-closed, ไม่มี reply) ไม่ใช่ fallback ไปที่เดิม — เป็นพฤติกรรมที่ตั้งใจ ไม่ใช่บั๊ก แต่ผู้ตั้งค่า config ต้องรู้ · จุดที่ 2 ยังไม่มีฟังก์ชันให้เรียก ยังไม่ต่อสาย |
| 018 | LANE-A `world_scene_travel.is_position_persist_allowed()` (`20260827_1809`, แก้บั๊ก `GT-106` ④.3 — `character_positions` เขียน `scene_id=1` พร้อม XYZ ของฉาก 17 หลัง teardown, ตาม `COO-DECISION 20260827_1746` ตัวเลือก (ข)) | `lifecycle.py`'s `CharacterLifecycle.checkpoint()`/`exit()` — จุดเดียวที่เรียก `store.save_position()` ทั้งกระดาน (ยืนยันด้วย `tests/test_move_authority_dispatch.py`'s pinned "exactly 2 callers" test) | **ต่อแล้ว — R197** (`pirate-force-server@9c920f4`+`fe89b55`, push แล้ว รอ merge PR) `is_position_persist_allowed(scene_id)` เกตการเขียนเท่านั้น (`False` วันนี้เฉพาะฉาก 17 → ข้ามเขียน แถวเดิมอยู่เฉย ๆ) · `pf-adversary` รอบแรกพบ **HIGH จริง**: ดราฟต์แรกข้ามทั้งการเขียนและด่านตรวจ stale-session/ownership (`store.py`'s `EXISTS` guard, สัญญาณเดียวที่โปรเจกต์นี้มีจับ lease ค้าง/ถูกแย่ง) ทำให้ session ค้างที่หลุด lease แล้วเดินเข้าฉาก 17 จะไม่ error ให้เห็นอีกต่อไป (เดิม `PermissionError` ดัง) แก้แล้ว: `store.save_position()` เพิ่ม `write_position=` — ด่าน ownership ทำงานเสมอ ข้ามเฉพาะคอลัมน์ตำแหน่งจริง · รอบสองยืนยันสะอาด (ไม่มีข้อใหม่) · เพิ่ม cache ตัว registry ที่ `CharacterLifecycle.__init__` (เดิม reload จากดิสก์ทุก checkpoint, วัดแล้ว ~19 ครั้ง/เดินสั้นหนึ่งรอบ) · เทสใหม่ 7 ข้อ `tests/test_lifecycle_persist_position_gate.py` (รวม stale-session repro 2 ข้อจาก adversary) · สวีตเต็ม `3520 passed, 0 failed` เขียว(cloud sanity) ledger verify PASS entries=47 · **ยังไม่ปิด `GT-106` ทั้งใบ**: นี่คือจุดที่ 1/3 ของ `COO-DECISION 1746` — จุดที่ 2 (หลักฐานปลายทางฉาก 126 vs 17, งาน RE) และจุดที่ 3 (ตัวเลือกเควส 3205 ใน dialog Columbus) ยังเป็นของสาย A/GM-RE ตามที่จดหมายต้นทางระบุ ห้ามประกาศ M2 ผ่านจนกว่าจะครบ |

| 019 | LANE-A `columbus_quest_dispatch.make_columbus_conversation_two_options()`/`matches_columbus_bornagain_dispatch()`/`dispatch_columbus_quest3205()` (`20260827_1848`, round `hrz814` — item 3/3 ของ `COO-DECISION 1746`, ตัวเลือกเควส 3205 `Q_BORNAGAIN` ใน dialog Columbus, ตั้งใจ refuse เสมอวันนี้เพราะยังไม่มีคอลัมน์ persist home-marker) | `runtime.py`'s Columbus dispatch loop: (1) เปลี่ยนจุดสร้าง conversation frame เป็น `make_columbus_conversation_two_options` (2) เพิ่มสาขาคู่ขนานเช็ค `matches_columbus_bornagain_dispatch` แล้วเรียก `dispatch_columbus_quest3205` | **ต่อแล้ว — R198** (`pirate-force-server@aeccaa0`, push แล้ว รอ merge PR) latch อิสระของตัวเอง (`columbus_quest3205_dispatch_attempted`) ไม่ใช้ latch เดียวกับ 3021 — ผู้เล่นลองสองตัวเลือกสลับลำดับได้ครบ · quest-3021 path เดิมพิสูจน์ byte-for-byte ไม่เปลี่ยน (เทสเดิมผ่านหมด) · เพิ่มเทสใหม่ 4 ข้อ `tests/test_columbus_quest_dispatch_wiring.py` · **item 3/3 ของ `COO-DECISION 1746` ครบแล้วทั้งสามข้อ (018/RE-096-RE-103/019) — M2 ยังห้ามประกาศผ่านจนกว่า attended ยืนยัน (`GT-106`)** · `pf-adversary` พบจริง 1 ข้อไม่บล็อก (การขยาย outer gate ให้เช็คทั้งสอง latch ทำให้ frame parsing ของ session ที่เคยคุย Columbus ไม่ปิดตัวเองอีกต่อไปถ้าไม่เคยลอง option 2 — ไม่ผิด ไม่เห็นบนจอ ยอมรับไว้ก่อน บันทึกใน docstring) `RE-112` ปิด BOUNDED-NEGATIVE แล้ว (Lane A เอง, กลางรอบ — ไม่มี ack ฝั่ง client หลัง `ResetMarker`, ยืนยันว่า refuse-เสมอถูกต้องไม่ใช่ของชั่วคราว) |
| 020 | LANE-GM `field_0x0b_second=1` ใน `state_wire.make_gm_update_state_frame` call (`20260827_1933`, RE-089/RE-104 พิสูจน์ wire+0x15==1 คือเกตปุ่ม `BT_GM`) | `runtime.py`'s GM-state-after-login call site (~บรรทัด 4979-4986, ในบล็อกที่ `CORE-REQUEST-016` ทำไว้) | **ต่อแล้ว — R198** (`pirate-force-server@aeccaa0`) เปลี่ยน literal argument ตัวเดียวจาก `0, 0, 0` เป็น `0, 1, 0` ตามที่จดหมายขอเป๊ะ · แก้ `tests/test_gm_login_state_guard.py`'s hardcode ในคอมมิตเดียวกันตามที่จดหมายขอ (ไม่รอสาย GM แก้รอบหน้า กัน gate แดงข้ามรอบ) · **ยังไม่ปิดบล็อก GM ทั้งหมด** — `RE-113` (GT-107's `28317` error, PR#141 ยังไม่ merge) ต้องปิดคู่กันก่อนบัญชี GM จะกลับเข้า `gm_accounts` ได้ปลอดภัย |

**`WIRED` (COO-DECISION `20260826_1543` ①) ณ R177 = 7 / 10** — โมดูลเลนที่ `runtime.py`/`app.py` import: `world_population` `world_scene_travel` `world_scene_entry` `world_travel_gate` `field_mobs` `mob_combat` `mob_death` (ยืนยันด้วย grep สด, ไม่ใช่ก็อปตัวเลขรอบก่อน) — ขยับจาก 4/10 ที่วัดตอนต้นรอบ ⇒ ไม่ใช่ "WIRED ไม่ขยับ 2 รอบติด" escalation ไม่ทำงาน

- R174-R178 (5 รอบ) — ↴ ย้ายไป archive แล้ว (รอบ jsrh00, 2026-08-27) -> `archive/CHIEF_CONTINUATION_ARCHIVE_20260827_R166_R178.md`

- R179(keen-pasteur-r6hhp6/optimistic-mccarthy-r6hhp6) 2026-08-26 ~18:0x-19:0x (+07:00) 🎯 **ต่อสาย `CORE-REQUEST-007` บางส่วนตาม v6.1 §17 ข้อ 3 (ต่อสาย CORE-REQUEST ก่อนงานอื่นทั้งหมด)** [สรุปย่อ -> rounds/R179_keen-pasteur-r6hhp6_core-request-007-mob-ai-control-wiring.md]

- R180(3lzfhw) 2026-08-26 ~19:0x-20:0x (+07:00) 🎯 **ต่อสาย `CORE-REQUEST-006` (GM state) เต็มใบ + `CORE-REQUEST-007` ที่เหลือ (`mob_loot`/`mob_pickup` claim/release) ตาม v6.1 §17 ข้อ 3** [สรุปย่อ -> rounds/R180_3lzfhw_core-request-006-007-gm-loot-pickup-wiring.md]
- R181(6t7j6a) 2026-08-26 ~20:4x-21:1x (+07:00) WIRED=9/10 (เท่า R180 ไม่มี CORE-REQUEST ใหม่) [สรุปย่อ -> rounds/R181_6t7j6a_re082-amend-gt084-ready-gm001-reply-mailbox-ask.md]
- R182(q4z3vi) 2026-08-26 ~21:5x-22:5x (+07:00) 🎯 **`WIRED` 9→10/10 — ครบทุกเลนแล้ว** (ต่อสาย `world_density` เลนสุดท้าย) **+ `LANE-B-REQUEST` full_roster_override สลับสำเร็จ** — `pf-builder` ต่อสาย [สรุปย่อ -> rounds/R182_q4z3vi_world_density_wiring_full_roster_override_swap_ops005.md]
- R183(7d9ip6) 2026-08-26 ~23:5x-00:2x (+07:00) 🎯 **ปิด gap ที่ R182 ทิ้งไว้: headless proof ว่า "บาดเจ็บไม่ตาย → census ส่งซ้ำสะท้อน HP ลด"** — `CORE-REQUEST` check ก่อน: ไม่มีใบใหม่ค้าง [สรุปย่อ -> rounds/R183_7d9ip6_census_hp_wire_coverage.md]
- R184(kdx85r) 2026-08-27 ~00:5x-01:1x (+07:00) ต่อสาย CORE-REQUEST ที่ Lane A ขอค้างมา ~7 ชม. (`notes_to_chief/20260826_1010` ข้อ 4-2): `world_scene_liveness.py` เข้า `runtime.py` [สรุปย่อ -> rounds/R184_kdx85r_core-request-world-scene-liveness-wiring.md]
- R185(h53n8f) 2026-08-27 ~01:5x-02:3x (+07:00) `CORE-REQUEST`/`WIRED` check: 10/10 ไม่เปลี่ยนจาก R184 ไม่มีใบค้างใหม่จากสาย A/B/GM [สรุปย่อ -> rounds/R185_h53n8f_re-queue-closures-branch-protection-ask.md]
- R186(561t95) 2026-08-27 ~02:5x-03:2x (+07:00) `CORE-REQUEST`/`WIRED` check: 10/10 ไม่เปลี่ยน [สรุปย่อ -> rounds/R186_561t95_gate-dispatch-fix-plus-mailbox-and-re-queue-closures.md]
- R187(keen-pasteur-543ds8) 2026-08-27 ~08:5x-09:3x (+07:00) `COO-DECISION 0345` สั่งต่อ `build_field_mob_population` เป็นอันดับหนึ่ง — ตรวจสดพบสมมติฐานผิด: hostile bodies ถูกต่อสายไว้แล้วจริงตั้งแต่ [สรุปย่อ -> rounds/R187_keen-pasteur-543ds8_gt084-console-gate-plus-combat-death-wipe-escalation.md]
- R188(keen-pasteur-ahn7zb) 2026-08-27 ~09:0x-11:3x (+07:00) ต่อสาย `CORE-REQUEST-008` ครบสามจุด (`MOB_COMBAT_BAR`/`MOB_DEATH_DYING`/`MOB_DEATH_DEAD` compose เข้า full census แทน one-entry ตามที่สาย [สรุปย่อ -> rounds/R188_keen-pasteur-ahn7zb_core-request-008-wired-plus-adversary-fixes.md]
- R189(keen-pasteur-ss84b6) 2026-08-27 ~13:xx (+07:00) `COO-DECISION 0950` (กำแพงกระเป๋า) แก้ได้ครึ่งเดียว จริง ไม่ใช่ทั้งหมด — `pf-adversary` จับได้ก่อน push ว่า `require_backpack_shape` ที่ store [สรุปย่อ -> rounds/R189_keen-pasteur-ss84b6_bag-wall-partial-plus-wired-v2-audit-plus-gate-dispatch-recovery.md]
- R189 update (keen-pasteur-ss84b6): `pirate-force-server#96` gate แดงจริงตอนเอา draft ออก (`pytest_subset`, ไม่ใช่ของสาย E ผิด, ยืนยันจาก `ci-status`) ถูกปิดโดย workflow ถูกต้อง → กู้สามชั้น: `#99` [สรุปย่อ -> rounds/R189_keen-pasteur-ss84b6_bag-wall-partial-plus-wired-v2-audit-plus-gate-dispatch-recovery.md]
- R190(3t3klq) 2026-08-27 (+07:00) ต่อสาย `CORE-REQUEST-010` (LANE-GM run-command dispatch 0x51E9, `pirate-force-server@dfa61ac`) + `combat_loot` ได้ console token (`WIRED v2` = 9/10) [สรุปย่อ -> rounds/R190_3t3klq_core-request-010-plus-mob-loot-token-plus-player-faction1-flagless.md]
- R191(o72iwp) 2026-08-27 (+07:00) รอบแรกที่อ่าน v6.2 [สรุปย่อ -> rounds/R191_o72iwp_v62-adoption-item0-check-core-request-registry-catchup.md]
- R192(4txjyg) 2026-08-27 ~12:0x-13:xx (+07:00) 🎯🔴 **ต่อสาย `CORE-REQUEST-014` (Lane A, M2, เส้นตาย 20:00): Columbus (MOBS 156, Port Royal) → `NPCConversation`/quest 3021** — บทสนทนาต่อแล้วจริง [สรุปย่อ -> rounds/R192_4txjyg_core-request-014-columbus-quest3021-dispatch.md]
- R192 update (4txjyg): `pf_bridge#191` ถูกปิดโดย `merge-claude-pr`'s conflict guard (main ขยับผ่าน — `RE-101` ของรอบนี้ชนกับ `RE-102` ที่สาย A เปิดพร้อมกัน ทั้งคู่ถูก append ที่ท้ายไฟล์เดียวกัน `CLIENT_RE_QUEUE.md`) กู้ด้วย `git merge origin/main` (เก็บทั้งสองบล็อกไว้ ไม่ทิ้งฝั่งไหน) เปิดล็อกใหม่ `pf_bridge#196` draft
- R193(mnw8z1) 2026-08-27 14:2x (+07:00) ยืนยัน R192 ทั้งสอง repo merged=true จริง (`list_pull_requests`'s `merged` field เป็น false negative — บั๊กที่สาย GM รายงาน, COO ยืนยัน `1350`) [สรุปย่อ -> rounds/R193_mnw8z1_widen-death-scope-bg0001-plus-addendum-v62-item-g.md]
- R194(e0daaa) 2026-08-27 ~15:0x-15:2x (+07:00) COO-DECISION widening-rulings scene gate: `field_mobs.assert_single_scene_tables()` + tests, pf-adversary found 2 real gaps (guard does not cover [สรุปย่อ -> rounds/R194_e0daaa_widening-scene-guard-plus-scene17-provisional-decree.md]
- R194 update (e0daaa): mid-round letters (PANYA-DECISION 1510/1525, LANE-GM CORE-REQUEST-016 urgent) expanded this round well past the original widening-guard+decree scope. Merge conflict found on [สรุปย่อ -> rounds/R194_e0daaa_widening-scene-guard-plus-scene17-provisional-decree.md]
- R195(8soxxm) 2026-08-27 ~16:5x-17:2x (+07:00) built `lane_hooks/` skeleton in pirate-force-server as promised (v6.3 §18.1, R194's own commitment): auto-discovery + fail-closed `fire()`/`hook()` registry [สรุปย่อ -> rounds/R195_8soxxm_lane-hooks-skeleton-plus-mailbox-catchup.md]

- R196(0vjgyy) 2026-08-27 ~18:0x-18:3x (+07:00) wired CORE-REQUEST-017 point 1 (LANE-GM per-account login-scene override) into runtime.py's START_GAME_REQ handler as promised by R195, directly rather [สรุปย่อ -> rounds/R196_0vjgyy_core-request-017-point1-login-scene-override-plus-housekeeping.md]

- R197(kjtyku) 2026-08-27 ~18:5x-19:2x (+07:00) wired CORE-REQUEST-018 (LANE-A `is_position_persist_allowed()`, GT-106 (4).3 persistence bug, item 1/3 of COO-DECISION 1746's M2-not-closed ruling) [สรุปย่อ -> rounds/R197_kjtyku_core-request-018-persist-position-gate.md]

- R198(n2ws3l) 2026-08-27 ~19:5x-20:1x (+07:00) §2 item 7: `pf_bridge#227` merged=true, `pirate-force-server#140` merged=false (gate RED) -- recovered by cherry-picking `9c920f4`/`fe89b55` from the [สรุปย่อ -> rounds/R198_n2ws3l_r197-recovery-plus-core-request-019-020.md]
