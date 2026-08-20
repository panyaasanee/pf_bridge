# CHIEF_CONTINUATION archive — รอบ 93 · 95 · 96 (ย้ายโดย chief รอบ 102, 2026-08-20 — ไฟล์หลักทะลุ 100KB)
# ห้ามลบ · การตัดสินใจที่ยังมีผลถูกยกไปไว้ในบล็อกรอบ 97+ แล้ว

> ## 🆕🆕 รอบ 96 (2026-08-20 04:2x → 05:4x) — **⭐ MULTIPLAYER ก้อน 2 เริ่มแล้ว: HYP-PF-025 REMOTE-PLAYER-ENCODER-001 — actor_type 2 (CNetActor) 5 เฟรมแรกในประวัติโปรเจกต์ · headless-proven ครบ**
>
> **HEAD `72d6129` → `8dfd303` (job 158) · commit เดียว 21 paths** · full suite **1618 passed 1 skipped** · fresh clone reproduce ครบ (ledger=0 coverage=0 rpEnc=0 rpReplay=0) · ledger APPEND entry **32** (index เก่านิ่งหมด) · canonical sha `6BFCEDD5..8FC7` ไม่ขยับ · ถือ `LOCK_GIT` เฉพาะช่วงจ็อบ 156/157/158 (สามจ็อบ: 156/157 REFUSED อย่างถูกต้องเพราะ census drift, 158 commit สำเร็จ) · **ไม่แตะ `LOCK_GAME` เลย** · กล่องจดหมายว่าง
>
> ### ⭐ สิ่งที่ลง: เลน HYP-PF-025 (multiplayer ก้อน 2 — Panya เคาะ 2026-08-19 11:45)
> เขียนจาก `drafts/MULTIPLAYER_CHUNK2_VISIBILITY_DESIGN_R90.md` + สาม CHUNK2 static findings (Q1/Q2/Q3) · pattern เดียวกับ HYP-PF-023 เป๊ะ
> **sweep 5 เฟรม actor_type 2 · one-shot · 15 วิ/เฟรม · opt-in scenario + wire unlock เทียบด้วย identity:**
> ① `SPAWN_BARE` (A `0x00A00001`): ActorAttr พก **BasicAttr bit 0x0001 = ชื่อ** ครั้งแรกบนสาย ActorAttr (oracle เทียบ `make_npc_attr` byte-for-byte) + MovementAttr 0xFF
> ② `SPAWN_AVATAR` (B `0x00A00002`): + AvatarAttr ของตัวละครที่เลือก (replay opaque, rebind identity, **ริมท้าย entry** ให้ walker หาขอบได้) — **pin เป็น SKELETON pin** เพราะ tail เป็นไบต์จาก DB
> ③④ `MOVE_A_1/2` (A): MovementAttr เดี่ยว mask 0x01 → 0x03 (เส้น update vtable+0x20)
> ⑤ `NEGATIVE_CONTROL` (C `0x00A00003`): NPCAttr **ผิดคลาสโดยตั้งใจ** — bind gate 0x4697B0 (CNetNPC) ต้อง drop เงียบ · **ถ้าป้ายชื่อขึ้น = ก้อน 1 ผิด หยุดทั้งเลน**
> ⭐ **nonclaim บังคับติดทุกที่: ดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** — ไม่มี capture remote human player ในคลังเลย
>
> ### ใบเสร็จ (headless-proven ทั้งหมด — ยังไม่มี client เห็นแม้แต่ไบต์เดียว)
> `tools/verify_remote_player_encoder.py` **129 guards** (138 กับ `--binary` — jump table 5 ช่อง, bind thunk 5 ตัว, +0x24 CopyTo load, literal 0x6E9D จากอิมเมจ sha `96272114..B623`) · `tools/pf_remote_player_headless_replay.py` **162 guards** ผ่าน dispatcher จริงบน DB สำเนา (walker อิสระอ่านกลับจากศูนย์ ไม่ import decoder ของโมดูล) · เทส **63 + 25** · full suite Windows คาด ~1618 passed
> spawn: attr order = ActorAttr, Movement, **Avatar last** (ต่างจากร่าง R90 ที่วาง avatar เป็นตัวสอง — เพราะ walker หาขอบ opaque tail ได้เฉพาะตอนมันอยู่ท้าย · จดใน docstring) · spacing = **15 วิ** (ต่างจากร่าง 6 วิ — บทเรียนกล้องรอบ 84)
>
> ### 🔴🔴 บทเรียนแพงสุดของรอบ: จ็อบ 156 REFUSED to commit — **และนั่นคือ guard ทำงานถูก**
> โมดูลใหม่เป็น **src/ module ตัวที่สองที่ build actor entry** ⇒ census สอง standing check ขยับ (จับได้ก่อน commit):
> **①** `pf_stats_progression_static.py`: โมดูลผมมี token `CSkillAttr` (ในคอมเมนต์) → census "src/ ไม่มี progression verb" แดง · **แก้:** ลบชื่อ เขียนแค่ `SKILL_ATTR_ID = 0x1661` (refuse ด้วยเลข ไม่ใช่ชื่อ) + คอมเมนต์อธิบาย
> **②** `pf_runtimeres_actor_entry_static.py`: census "exactly ONE src/ module both builds entry AND **sets** 0x0080" แดง เพราะโมดูลผม *mention* 0x0080 (เพื่อ **forbid** มัน) · **แก้แบบซื่อสัตย์:** แยก "SET" ออกจาก "mention" — SET = build entry + 0x0080 + **ไม่มี** token `FORBIDDEN` → ยังเป็น 1 module (death lane เป๊ะ) · เพิ่ม census ใหม่ "forbidding" ชี้ชื่อ remote_player · re-pin นับ 5→6 (entry sites), 4→5 (builders), 3→4 (mentions) พร้อมชื่อโมดูล · re-pin RUNTIMERES_COUNTS block ในรายงาน + guard count 151→152 + เพิ่ม ERRATUM 3 (เก็บประโยคเก่าไว้ ต่อ erratum) + แก้เทส 21 ตัว
> 🔴 **บทเรียนเข้า PLAYBOOK: เพิ่มโมดูล src/ ที่ build actor entry หรือแตะ token ที่ census ใด ๆ นับ = ต้อง re-pin census tool+report+test ในรอบเดียวกัน** · จ็อบ 156 ทำถูกที่ไม่ commit ตอน guard แดง — ห้าม override
>
> ### coverage / ledger / matrix
> - `movement/remote_player_movement_projection` **ยังเป็น `in_progress`** (ไม่ flip) — เพิ่ม evidence refs (report + 3 CHUNK2) + test refs 2 ตัว + note ยาว · **ห้าม flip จนกว่า GT-030 รันจริง** (ยังไม่มี client เห็น actor_type 2)
> - ledger entry HYP-PF-025: 2 tracked versions (ENCODER + DISPATCH) · **เหลือ 1 version slot** · widening ใด ๆ (name-field variant, cadence probe, despawn) = ใช้ slot สุดท้ายหรือเปิด entry ใหม่
> - seam grade digest re-pin (`EFCDB531..` → `56EE376C..`) เพราะ coverage refs ขยับ
>
> ### คิว attended พร้อมรอบใหญ่ #9 (เพิ่มของใหม่)
> - **GT-030 REMOTE-PLAYER-VIS-001 = PENDING** — boot `--remote-player-hypothesis-scenario scenarios\remote_player_hypothesis_visibility_probe.json` · 5 เฟรม/75 วิ · ตารางถ่ายทีละเฟรมครบใน `GAME_TEST_QUEUE.md` · **ผลลบมีค่า** (ไม่โผล่ = spawn ด้วย mask 0 ไม่เรนเดอร์ ก็เป็นคำตอบ)
> - GT-027/028/029 (damage NPC + slow sweep + dying countdown) ยัง PENDING เหมือนเดิม · GT-001 re-arm ที่ HEAD ใหม่ (commit แตะ src/)
> - เลขจ็อบ: chief ใช้ไป 156/157/158 รอบนี้ ⇒ **chief ถัดไป 159** · ผู้เทส **933**
>
> ### 📌 คำถามค้าง / งานที่จงใจเลื่อน
> - **จบก้อน 2 ต้องกลับมาให้ Panya เคาะก่อนเดินก้อน 3** (Panya 2026-08-19) — ก้อน 2 = เลนนี้ (ยังไม่ "จบ" จนกว่า GT-030 รันและตัดสินว่าเห็นอะไร) · ยังมี design draft questions ค้าง (mask ไหนจำเป็นต่อ render, avatar ยอมรับใต้ identity อื่นไหม) = คำถามของ attended run
> - persistence Lane 2/3 = เลื่อนท้ายสุดตามคำสั่ง (ไม่ถามซ้ำ) · `verify_foundation.ps1` re-pin/ปลดระวาง · `.gitignore !/.github/` · `git remote` = คำถามค้างเดิม
>
> ### nonclaims ของรอบ 96
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่ flip matrix row · ไม่แตะ v141 · ไม่แตะ `LOCK_GAME`**
> · **ไม่มี runtime observation เลย** — actor_type 2 ยังไม่เคยถูกส่งให้ client แม้แต่ไบต์เดียว (นั่นคือ GT-030)
> · ไม่ claim ว่า probe เรนเดอร์/เป็นคน/mask ไหนจำเป็น · ไม่ claim ว่า avatar ยอมรับใต้ identity อื่น · ไม่ใช่ผู้เล่นสองคนจริง (ก้อน 3)
> · full suite รันบน Windows เท่านั้น · census re-pin เป็นการนับ src/ ของเราเอง ไม่ใช่ข้ออ้างเรื่องอิมเมจ

> ## 🆕 รอบ 95 (2026-08-20 03:13 → 04:2x) — **เก็บงานรอบ 94 ที่ตายเงียบ (IMG-QUERY-001 ลงจริง) + DAMAGE-NPC-TARGET-001 ปิดงบ version ของ HYP-PF-024 (3/3)**
>
> **HEAD `2992998` → `dbcbf8f` (job 154) → `72d6129` (job 155)** · สอง commit · worktree สะอาดหลังแต่ละ commit
> ถือ `LOCK_GIT` เฉพาะช่วงจ็อบ 154/155 รันจริง (จ็อบปล่อยธงเอง) · **ไม่แตะ `LOCK_GAME` เลย** · canonical sha `6BFCEDD5..8FC7` ไม่ขยับ (ตรวจก่อน-หลังทุกจ็อบ) · กล่องจดหมายว่าง (ทุกใบเป็นใบปะหน้า consumed แล้ว)
>
> ### ① takeover รอบ 94 (ตามเกณฑ์ที่ประกาศไว้)
> รอบ 94 เริ่ม ~02:2x เขียน `tools/pf_image_query_runner.py` + `tests/test_image_query_runner.py` + `.gitignore` ครบและ**เขียว** (รัน pytest เองตอน 02:41) แล้ว**เงียบไปก่อน stage** — เงียบครบสามช่อง 34+ นาที (outbox 02:19 · worktree 02:41 · ธง 02:19) ⇒ takeover
> รอบ 95 อ่านงาน รันเทสซ้ำ (12/12) ตรวจ ASCII/diff-check/check-ignore เอง แล้ว **commit ให้ที่ `dbcbf8f`** (11→3 path: runner + เทส + .gitignore) — commit message จดที่มาของ authorship ตามธรรมเนียม `d4ed4d4`
> 🟢 **จ็อบ 154 พิสูจน์จาก fresh clone: เทส runner 12/12 ผ่าน · coverage=0 · ledger=0** · ตัวรันครึ่ง local ของ `image_queries\` **มีจริงแล้ว** (kinds: `bytes`/`hash`/`search` · sha-pin ก่อนอ่านทุกไบต์ · เพดาน 4KB/คำถาม + 64KB/วัน · refusal มีชื่อครบ 6 แบบ เห็นแดงครบ) · README ใน `image_queries\` อัปเดตสถานะแล้ว
>
> ### ②⭐ DAMAGE-NPC-TARGET-001 — profile ที่สองของ HYP-PF-024 (commit `72d6129` · 11 path)
> **คำถามเดียวที่ GT-024 ตอบไม่ได้: client เคยถูกขอให้วาดเลขของเราบน actor ที่ไม่ใช่ผู้เล่นหรือยัง** — profile `npc_target` ตอบด้วยการเปลี่ยนแค่สองอย่าง:
> **target = `0x2001`** (placement แรก Port Royal — identity เดียวกับที่ HYP-PF-023 ใช้ · copy พร้อม drift test ไม่ import) และ **spacing = 15 วิ** (ถ่ายทันทุกเฟรม — บทเรียนรอบ 84) · **performer ยังเป็นผู้เล่น** (visibility filter `0x43FEF0` — FINDINGS_R93)
> แผนสี่ก้าวเป็น**อ็อบเจ็กต์เดียวกัน**กับ hit_sweep (fork ไม่ได้) · unlock token แยกต่อ profile เทียบด้วย identity (ท่าซ่อมรอบ 91 ของ HYP-PF-023) — key ข้าม profile เปิดอะไรไม่ได้ พิสูจน์สองทิศ · refusal ใหม่ 3 ชื่อ: `npc_target_identity_not_pinned` · `npc_performer_must_not_be_the_npc_target` · `wire_unlock_is_for_a_different_profile`
> **ใบเสร็จ:** dm verifier **350 guards** (เดิม 322) · replay `--profile npc_target` **141 guards** + `hit_sweep` เดิม 140 · เทสเลน 102+68 (dispatch class ถูก **subclass ทั้งคลาส**ใต้ npc profile — บันได refusal ทั้งชุดวิ่งสองรอบ) · full suite Windows **1530 passed 1 skipped** · **fresh clone รัน ledger + coverage + npc replay ผ่านหมด** (job 155)
> **บัญชี version จ่ายตรง:** stop rule เดิมเขียนว่า "a second target = NEW VERSION" ⇒ ใช้ช่องสุดท้าย **งบเต็ม 3/3** · stop rule เขียนใหม่เป็นขอบเขตที่บังคับจริง · ประโยค scope "never an NPC" แก้เป็นชื่อสอง profile · **canonical sha ของ ledger ถูก re-pin ใน verifier พร้อมคอมเมนต์เล่าเหตุ** (ตามธรรมเนียม amendment ทุกครั้ง) · รายงาน: `reports/PF_DAMAGE_NPC_TARGET001_SECOND_PROFILE_20260820.md`
> **erratum ติดรถ:** docstring เฟรม MISS ที่เขียนว่า "the control: NO number" แก้แล้วตามไบต์ (bm_miss.tga = marker โดยออกแบบ · เลขเท่านั้นที่ต้องไม่มี) — ปิดหนี้ที่รอบ 93 จดค้างไว้
>
> ### ③ คิว attended พร้อมรอบใหญ่ #9 แล้ว (อัปเดตแล้วทั้งหมดใน GAME_TEST_QUEUE.md)
> - **GT-027 = PENDING** — boot ท่า GT-024 เดิม เปลี่ยนไฟล์ scenario เป็น `damage_model_hypothesis_npc_sweep.json` · event/label ใหม่บอกชัดว่าบูตถูกไฟล์ · **ผลลบ = คำตอบว่า `0x2001` ไม่อยู่ใน map ตอนรัน — มีค่าเท่าผลบวก**
> - **GT-028 = PENDING มีเงื่อนไข** — รันคู่ GT-027 บูตเดียวกัน (15 วิ/เฟรมถ่ายทัน) · ถ้า GT-027 ลบ → กลับ BLOCKED (profile ช้าแบบยิงผู้เล่นต้องเปิด entry ใหม่ เพราะงบ HYP-PF-024 เต็ม)
> - **GT-029 = PENDING** — ชี้แล้วว่า `dying_latch_only` (ท่า GT-025) คือ "scenario ค้าง latch นาน" ที่รายการนี้รอ ไม่ต้องเขียนใหม่ · เก็บภาพวงทีละวินาที ≥10 วิ ผลมีความหมายทั้งสองทาง
> - **GT-001 re-arm ที่ `72d6129`** (commit แตะ src/ — ทุกจุดหลังธง opt-in · ความเสี่ยงต่ำ) · GT-026 ยัง PENDING เหมือนเดิม
> - เลขจ็อบ: chief ถัดไป **156** · ผู้เทส **933**
>
> ### 🧹 แม่บ้าน + สิ่งที่ควรรู้
> - ย้ายบล็อกรอบ 90+91 → `archive\CHIEF_CONTINUATION_ARCHIVE_20260820_R90_R91.md` (ไฟล์นี้ 91.6→~90KB หลังรวมบล็อกรอบ 95)
> - 🔴 **พอยน์เตอร์เก่าผิดหนึ่งจุด:** โน้ตรอบ 93 อ้าง `drafts/MULTIPLAYER_CHUNK2_VISIBILITY_DESIGN_R90.md` — **ไฟล์ชื่อนี้ไม่มีจริง** ของจริงคือ `drafts/CHUNK2_Q1_ACTORATTR_MASK_FINDINGS.md` + `CHUNK2_Q2_MOVEMENT_MERGE_FINDINGS.md` + `CHUNK2_Q3_BIND_THUNK_FINDINGS.md`
> - บทเรียนใหม่ (จดใส่หัว): **แซนด์บ็อกซ์ `git checkout --` ไฟล์ใน mount ไม่ได้** (unlink not permitted) — แก้ไฟล์กลับต้องใช้ read-modify-write เท่านั้น · และ **json.dumps ต้องเช็ค indent ของไฟล์เดิมก่อน** (เกือบ reformat ledger ทั้งไฟล์ 2,300 บรรทัด — จับได้จาก diff --stat ก่อน commit)
>
> ### 📌 คำถามค้าง / งานที่จงใจเลื่อน (ไม่เปลี่ยนจากรอบ 93 ยกเว้นข้อแรก)
> - ✅ ~~`tools\pf_image_query_runner.py` ยังไม่มี~~ → มีแล้ว (`dbcbf8f`) · kinds `strings`/`disasm`/`xref` = งานอนาคต เปิดเมื่อมีคำถามจริงชนเพดานของสามตัวแรก
> - **multiplayer ก้อน 2 ยังไม่เริ่ม** — pre-approved แล้ว (Panya 2026-08-19 11:45) · ควรเป็น**งานหลักของรอบถัดไป** · เริ่มจาก drafts/CHUNK2_Q1..Q3 สามใบข้างบน · จบก้อน 2 ต้องกลับไปให้ Panya เคาะก่อนเดินก้อน 3
> - `verify_foundation.ps1` re-pin หรือปลดระวาง (79 vs 105) = รอ Panya · `.gitignore` `!/.github/` = รอคำเคาะ ก./ข. · **`git remote` ยังไม่มี** = คำถามค้างข้อ ข. · persistence Lane 2/3 = เลื่อนไปท้ายสุดตามคำสั่ง (ไม่ถามซ้ำ)
>
> ### nonclaims ของรอบ 95
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่ flip matrix row · ไม่เพิ่ม ledger entry (amend อย่างเดียว) · ไม่แตะ v141 · ไม่แตะ `LOCK_GAME`**
> · **ไม่มี runtime observation ใหม่เลย** — npc profile ยังไม่เคยถูกส่งให้ client เห็นแม้แต่ไบต์เดียว (นั่นคือ GT-027)
> · **ไม่ claim ว่า `0x2001` อยู่ใน identity map ตอนรัน** — นี่คือสิ่งที่ GT-027 วัด และผลลบมีความหมาย
> · full suite รันบน Windows เท่านั้น (1530 passed) — แซนด์บ็อกซ์รันเฉพาะโมดูลที่ปลอดภัย


> ## 🆕 รอบ 93 (2026-08-20 00:53 → 02:4x) — **หนี้หลักฐานที่ทำให้ gate ทำซ้ำจาก git ไม่ได้ ปิดแล้ว + แก้ข้อผิดของ GT-024 ด้วยไบต์**
>
> **HEAD `47c7211` → `2992998`** (commit เดียว 40 path: **เพิ่ม 33 · แก้ 7**) · worktree สะอาดหลัง commit
> ถือ `LOCK_GIT` เฉพาะช่วงจ็อบ 152/153 รันจริง (จ็อบปล่อยธงเอง) · **ไม่ถือ `LOCK_GAME` เลย** · ไม่แตะ bridge server / เกม / canonical DB (sha `6BFCEDD5..8FC7` ไม่ขยับ ตรวจก่อน-หลังทุกจ็อบ)
> **บริโภคกล่องจดหมาย 3 ฉบับ** → `consumed\`: `0110_BIGROUND8-RESULTS` · `0115_SPEC-image-query-queue` · `0130_ORDER-FINAL-cloud-requires-repo`
>
> ### ⭐ สิ่งที่ commit นี้ทำ (EVIDENCE-VISIBLE-001 + cp874 console gate)
> **① 33 ใน 112 path ที่ `docs/FUNCTIONAL_COVERAGE.json` อ้างเป็นหลักฐาน — git มองไม่เห็นมาตลอด**
> อ้างโดย **17 แถวความสามารถ ข้าม 8 domain** และ **9 แถวในนั้นเกรด `runtime_pass`**
> ⇒ clone สดไม่เคยมีเอกสารที่ 9 คำอ้างนั้นยืนอยู่ และ `verify_functional_coverage.py` **exit 2 บน clone**
> **เหตุที่ไม่มีใครเห็น:** check ของรอบ 87 กวาด **ledger อย่างเดียว** · check ที่ครอบ matrix ถาม *ระบบไฟล์* จึงเขียวทั้ง 33
> **ทางแก้ = เพิ่มไฟล์ ไม่ใช่ตัด reference** (แบบเดียวกับรอบ 82/84/86/87/90) + เทสใหม่ใน `tests/test_functional_coverage.py` พร้อม trap และพิน 4 ชื่อ
> 🟢 **ใบเสร็จที่แข็งที่สุด: จ็อบ 153 `git clone` HEAD ลง temp แล้วรันจริง → `coverage=0 ledger=0` · `PF_RE_V` ในทรี = 34**
> ⇒ **gate ทำซ้ำจาก git ได้แล้วจริง ไม่ใช่คำอ้าง**
> **② กับดัก cp874 ที่รอบ 92 เจอแล้วปล่อยไว้** — `tools/pf_move_cadence001_headless_replay.py` 4 บรรทัดพิมพ์ `×`/`±`
> แก้เป็น `x` / `+/-` (ประโยคไม่เปลี่ยน) + **gate ใหม่แบบ AST** ครอบ `tools/` และ `tests/` ทั้งต้นไม้ (85+ ไฟล์)
> ดูเฉพาะสิ่งที่ไปถึง `print`/stdout/stderr (รวม f-string และ banner ระดับโมดูล) **ไม่แตะคอมเมนต์ไทยและ docstring**
> **ไม่ต้องใช้ client image ⇒ รันได้ทั้งสองเครื่อง** (ของรอบ 86 รันได้เฉพาะเครื่องที่มีอิมเมจ) · **trap 4 ตัว** รวม regression pin ที่สร้าง 4 บรรทัดเดิมขึ้นมาใหม่แล้วต้องจับได้ครบ
> **③ เอกสารเน่า:** `README.md` + `AGENTS.md` โฆษณา `tools\verify_foundation.ps1` ว่าเป็น gate — **มันผ่านไม่ได้**
> วัดซ้ำเองแล้ว: พิน **79** สมาชิก แต่ `build_foundation_release.py` ออก **105** (79 เดิมอยู่ครบ เพิ่มมา 26)
> **จงใจปล่อยให้แดง ไม่ re-pin** — census ที่ขยายตามทรีทุกครั้งเลิกเป็น census ⇒ **"re-pin หรือปลดระวาง" = คำถามค้าง**
> **④ erratum** ต่อท้ายรายงาน MOVE-CADENCE-001: manifest **ยังพินไบต์เดิมของเครื่องมือโดยเจตนา** เพราะ evidence manifest บันทึก "ไบต์ที่ผลิตหลักฐาน" · **ไม่ได้รัน replay ซ้ำ**
>
> ### 🔴🔴 บทเรียนที่แพงที่สุดของรอบ: **จ็อบ 152 แดง และมันช่วยชีวิต**
> เทสใหม่ของผมส่ง path เข้า `check-ignore` ทาง **stdin** · Python text mode บน Windows แปลงตัวคั่นเป็น **CRLF**
> ⇒ git เทียบ path ที่มี `\r` ติดท้าย **ไม่ match อะไรเลย** ⇒ **sweep รายงาน "สะอาด" ทั้งที่ยังพัง = false green เงียบ ๆ บนเครื่องเดียวที่รัน gate จริง**
> สิ่งเดียวที่จับได้คือ **trap** (สร้างรีโปชั่วคราวที่มีไฟล์ถูก ignore หนึ่งใบ) ซึ่งเขียวในแซนด์บ็อกซ์แต่แดงบน Windows
> **แก้:** ย้าย path ไป argv เป็นก้อนละ 50 · และ **บังคับให้ trap กับ sweep เรียก helper ตัวเดียวกัน** เพราะเวอร์ชันที่ผิดคือสำเนาที่ trap ไม่ได้ทดสอบ
> **กฎที่ควรจำ:** *"check ที่ไม่เคยเห็นมันแดง ไม่ใช่ check" ยังไม่พอ — trap ต้องยิงใส่ code path เดียวกับของจริง ไม่ใช่ใส่สำเนา*
> (จ็อบ 152 ยังแดงข้อสอง: `git diff --check` เจอบรรทัดว่างท้ายไฟล์ที่ erratum ทิ้งไว้ — แก้แล้ว)
>
> ### ⭐⭐ ผลรอบใหญ่ #8 + **ข้อผิดของเราเองที่ static หักล้าง** (สำคัญกว่าผลเทสเอง)
> GT-025 **[PASS]** · GT-023 **[PASS]** · GT-024 **[PASS แบบมีเงื่อนไข]** — รายละเอียด/nonclaims อยู่ใน `GAME_TEST_QUEUE.md`
> 🔴 **`_F_DIE_000` (ท่าตาย) ยังไม่เคยถูกสังเกต** — ท่านอนเป็นของ `DYING_LATCH` (GT-025 พิสูจน์โดยไม่ใช้นาฬิกา) · **ห้าม flip matrix row ของ HYP-PF-023**
> 🔴 **สองประโยคในคิวที่ผิดและถูกหักล้างด้วยไบต์** (ลูกมือ static รอบนี้ · `FINDINGS_R93_CHITRESULT_DISPLAY_TARGET_STATIC.md`):
> **①** `probe_identity_lo = 268500993` **= `0x10010001` = identity ของผู้เล่นเอง** ไม่ใช่ `0x10002001` (= 268443649)
> scenario เขียนกฎไว้ตรง ๆ ว่า `the_players_own_actor_is_both_performer_and_target`
> ⇒ **"เลขขึ้นบนตัวผู้เล่น" คือพฤติกรรมที่ถูก ไม่ใช่บั๊ก** และ **client resolve target identity จริง** (`0x750D1E → 0x446170` map lookup · resolve ไม่ได้ = ข้าม entry เงียบที่ `0x750D27` · FxNumber 9/9 จุดผูกกับ actor ที่ resolve ได้)
> **②** เฟรม `MISS` **ไม่เงียบโดยออกแบบ**: `bit0 ไม่ติด AND damage == 0` → FxNumber **type 6** (`0x440093 6A06`) → คีย์ `0x2D` → `.\Data\CP\bmmsg\bm_miss.tga`
> ⇒ **การเห็น `MISS` เป็นหลักฐานบวกว่าไคลเอนต์อ่าน `flags` + `damage` ของเราจริง** (nonclaim: พิสูจน์แค่ว่าเลือกเท็กซ์เจอร์ชื่อนั้น ไม่ได้เปิดไฟล์ .tga)
> **กับดักที่ต้องจำ:** ใน handler เดียวกันมี FX ตัวที่สอง (`0x750E43`) ที่ **เกาะผู้เล่นเสมอ** เปิดใช้ด้วย `header+0x24 != 0` และ flags ฮาร์ดโค้ด `0x20` — คืนนั้นมันไม่ทำงานเพราะเราส่ง `+0x24 = 0` · **ถ้าวันไหนเผลอปักค่าอื่น จะดูเหมือนบั๊กเป๊ะกับที่เราเข้าใจผิด**
>
> ### 🧹 งานแม่บ้าน + ของที่สร้างรอบนี้ (นอกรีโป ⇒ ไม่ต้อง commit)
> | ไฟล์ | คือ |
> |---|---|
> | `GAME_TEST_QUEUE.md` **68.0 → 55.9 KB** | ย้ายสเปกเต็ม GT-023/024/025 ไป `archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R93_BIGROUND8.md` ทิ้งสรุปปิด + เพิ่ม **GT-027/028/029** + บทเรียนเครื่องมือ 8 ข้อ |
> | `FINDINGS_R93_CHITRESULT_DISPLAY_TARGET_STATIC.md` | static ตอบ "เลขเกาะกับใคร" + ตาราง flag→type→เท็กซ์เจอร์ ครบทุก address |
> | `FACTPACK_L2_CLASSCENSUS001_20260820.{md,tsv,json}` + `make_factpack_l2_classcensus.py` | สำมะโนคลาส 1,327 ตัว · **224 ยังไม่มีชื่อในทะเบียน** (191 อยู่ใน census รอบ 86 + 30 tsv-only + **3 ใหม่**) + 15 literal ทรงโปรโตคอลที่ไม่มี RTTI |
> | `image_queries\` (`pending/` `answered/` `README.md` `blocked_log.tsv`) | คิวย้อนกลับตามสเปกผู้เทส — **เริ่มจด blocked_log แล้ว 4 แถวจากของจริง** |
>
> ### 📌 งานที่จงใจเลื่อน + คำถามค้าง
> - **`tools\pf_image_query_runner.py` ยังไม่มี** — เป็นโค้ดในรีโป ต้องผ่าน gate ⇒ **งานแรกของรอบถัดไป** (`bytes`+`hash`+`search` ก่อน)
> - **docstring ของเฟรม MISS ใน `damage_model_hypothesis` ยังเขียนว่า "the control: NO number"** = ผิดตามไบต์แล้ว แต่ scenario/verifier พินไบต์ไว้แน่น ⇒ แก้ในรอบที่ตั้งใจแตะเลนนั้น พร้อม GT-027/028
> - **`verify_foundation.ps1` re-pin หรือปลดระวาง** = คำถามค้าง (มีตัวเลข 79 vs 105 วัดซ้ำได้แล้ว)
> - **`.gitignore` เติม `!/.github/`** ยังไม่ทำ — ผูกกับคำถาม ก./ข. ของรอบ 92 ที่ Panya ยังไม่เคาะ
> - 🔴 **`git remote` ยังไม่มีแม้แต่ตัวเดียว** ⇒ ย้าย chief ขึ้น cloud **เดินต่อไม่ได้** (คำถามค้างข้อ ข.)
>
> ### 🔴 แก้บันทึกที่ระบุตัวตนผิดของตัวเอง (ตามใบสั่ง `0130_ORDER-FINAL` ข้อ 0.1)
> **chief รอบ 89 · 90 · 91 · 92 · 93 รัน local ทั้งหมด** — รอบนี้พิสูจน์ซ้ำเองด้วยการทำจริง: อ่านกล่องจดหมายได้ · วางจ็อบลง `inbox\` ได้ · gate+commit ผ่าน bridge ได้
> โน้ตเก่าที่เขียนว่า "บัญชีใหม่" **ถูกอ่านต่อเป็น "cloud"** ซึ่งเป็นคนละเรื่อง · scheduled run บน cloud **แตะเครื่อง Panya ไม่ได้เลยตามการออกแบบ** (ผู้เทสทดสอบแล้ว 01:13)
> **บทเรียนเข้า PLAYBOOK: อย่าเชื่อคำอ้างของ agent ว่าตัวเองรันอยู่ที่ไหน — ให้ทดสอบด้วยการแตะของจริง**
>
> ### nonclaims ของรอบ 93
> **ไม่บูต server · ไม่เปิด client · ไม่เขียน DB · ไม่ flip matrix row · ไม่เพิ่ม/แก้ ledger entry · ไม่แตะ v141 · ไม่แตะ `LOCK_GAME`**
> · **ไม่ได้รัน `pf_move_cadence001_headless_replay.py`** — พิสูจน์แค่ว่าสิ่งที่มัน *พิมพ์* เข้ารหัส cp874 ได้ ไม่ได้พิสูจน์ว่าผลลัพธ์ยังทำซ้ำได้
> · **static รอบนี้ไม่มี runtime observation เลย** — พยานของผู้เทส/Panya ใช้เพียงเพื่อเลือกว่าจะไปดูไบต์ตรงไหน
> · **ไม่ได้พิสูจน์ว่า `0x2001` อยู่ใน identity map ตอนรัน** ⇒ GT-027 เป็นการทดลอง ไม่ใช่ผลที่รู้แล้ว
> · **class census ไม่ได้เปิดอิมเมจ** (อ่านจาก `strings_ascii.tsv` เท่านั้น) และ **ไม่ได้ปิดช่อง 209 คลาส** — ทุกชื่อยังเป็น literal
> · 🔴 **ห้ามรัน `pytest tests` ทั้งชุดจากแซนด์บ็อกซ์** — มันเอื้อมถึง canonical DB ผ่าน mount และ 17 โมดูล import ไม่ได้ที่นั่น (ไม่มี capstone) · **gate จริงคือ Windows เท่านั้น** (รอบนี้ **1,476 passed · 1 skipped · 2,870 subtests** ใน 151.7 วิ)


