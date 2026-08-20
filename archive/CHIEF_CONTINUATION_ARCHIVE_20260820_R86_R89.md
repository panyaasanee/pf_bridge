# ARCHIVE — CHIEF_CONTINUATION รอบ 86+87 และ รอบ 89

> ย้ายมาจาก `pf_bridge\CHIEF_CONTINUATION.md` โดย **chief รอบ 92 (2026-08-20 ~00:5x)**
> เหตุผล: ไฟล์แม่แตะเพดานงานแม่บ้าน (~100 KB) หลังเขียนบล็อกรอบ 92
> **ทั้งสองรอบปิดแล้ว** งานทั้งหมด commit ลงรีโปเรียบร้อย และไม่มีบล็อกไหนขัดกับ release note ล่าสุด
> 🔴 **ห้ามลบไฟล์นี้** — ไฟล์แม่ทิ้ง pointer ชี้มาที่นี่

---

## รอบ 86 + 87 (2026-08-19 08:4x–11:2x scheduled) — **RUNTIMERES-ENCODER-001 + NAMES-FOLD-003 + COMMENT-ERRATA-002 + LEDGER-VISIBILITY-001 + CP874-PORTABILITY-001**

> 📌 **สองรอบเขียนรวมกันเพราะเป็นงานก้อนเดียว** — รอบ 86 ถูกตัดกลางคัน 10:03 (Panya ปิดรอบ/เครื่องเงียบ)
> รอบ 87 takeover ตามเกณฑ์ที่ประกาศไว้แล้ว **ทำต่อ ไม่ได้เริ่มใหม่** · **ยังไม่ commit** ณ เวลาที่เขียนนี้

### สถานะ ณ ปลายรอบ 87
- **HEAD ยังเป็น `32878e0`** · worktree dirty **24 path** · CANON `6BFCEDD5..8FC7` ไม่ขยับ
- **job commit พร้อมแล้วที่ `pf_bridge\staged\143_round86_gate_commit_RETRY_after_cp874_fix.ps1`**
  ⇒ **รอบถัดไป: ย้ายไฟล์นี้ไป `inbox\` ทันทีที่ LOCK ว่าง** (ไม่ต้องเขียนใหม่ ตรวจแล้ว ASCII ล้วน)
- LOCK ถูก **เซสชันหลัก ATTENDED** ยึดเมื่อ 10:59 (รอบใหญ่ UI test #6 — GT-021/GT-017/GT-015)
  ⇒ chief หยุดแตะ bridge ตั้งแต่นั้น ไปทำงาน static ต่อ

### หลักฐานการ takeover (บันทึกไว้เป็นแบบอ้างอิงของครั้งหน้า)
LOCK เดิม mtime 09:57 · worktree write ล่าสุด 10:03 · outbox ล่าสุด 08:13 · inbox ว่าง · กล่องจดหมายว่าง
⇒ ครบทั้งสามช่องของเกณฑ์ (อายุ ≥20 นาที **และ** ไม่มีสัญญาณชีพเลยใน ~20 นาที)
🔴 **heartbeat ของรอบ 86 เขียนเวลา `11:05` ทั้งที่ไฟล์ถูกเขียนจริง 09:57** — เวลาอนาคต = พิมพ์ผิด
**บทเรียน: อย่าเชื่อ text ใน heartbeat อย่างเดียว ให้ดู mtime ของไฟล์ประกอบเสมอ**

### เลน A — RUNTIMERES-ENCODER-001 (รอบ 86 ทำ)
encoder spawn-then-kill ผ่านท่อ actor-entry ของ `0x6E9D` + **HYP-PF-023** + scenario + dispatcher branch
+ static verifier + headless replay + เทส 2 ไฟล์ · **สองข้อเท็จจริงที่ตรงข้ามสัญชาตญาณและเป็นตัวชี้ขาด:**
① **timer polarity กลับด้าน** — ค่าบวกที่เปิดหน้าต่าง dying คือค่าเดียวกับที่ *กัน* ไม่ให้เล่นอนิเมชัน
⇒ ต้องส่ง **ทั้งสองฝั่ง** และต้องเรียงลำดับ
② **actor เกิดมาตายเลยไม่ได้** — identity ที่ client ไม่รู้จักจะไปทางเกิด ซึ่งไม่แตะ dead-state sync เลย
⇒ ต้องมี **3 เฟรม ไม่ใช่ 2**
· HP-DEATH-002 (HYP-PF-022) **ไม่ถูกแตะ** ยังเป็นเลนที่เป็นเจ้าของหน้าต่าง `Main_Dead`

### เลน B — NAMES-FOLD-003 (รอบ 86 ทำ)
census thunk 209 คลาสที่ registry ไม่ครอบคลุม + report + companion `.census.json` ที่รายงาน derive ตัวเลขจาก
· **ไม่มีชื่อไหนถูกรับเข้าตาราง** (`EXPECT_CENSUS_ADMITTED = 0`) เพราะเงื่อนไข (a) ของกฎ (4) เป็นวงกลมสำหรับแถวพวกนี้

### เลน C — COMMENT-ERRATA-002 (รอบ 86 ทำ)
ซ่อมคอมเมนต์ผิด 2 จุดใน `src/` · จุดที่เขียนว่า "ONE caller" → จริงคือ **1 direct + 4 vtable +0x20 slots**
**ข้อสรุปไม่เปลี่ยน** ซึ่งเป็นเหตุผลที่แก้ถ้อยคำแทนที่จะลบทิ้ง

### 🆕 เลน D — LEDGER-VISIBILITY-001 (รอบ 87 · **ไม่ได้อยู่ในแผน · คุ้มที่สุดของรอบ**)
รอบ 86 ตายหลังเพิ่ม HYP-PF-023 ลง ledger **แต่ก่อนลงทะเบียน id ใน verifier** — fail-closed ทำงานถูก
(`unknown hypothesis id: HYP-PF-023` แดงทันที) ⇒ **สถานะที่ค้างกลางคันประกาศตัวเอง ไม่ได้นอนเงียบในทรีเขียว**
ลงทะเบียนครบแล้ว: `EXPECTED_IDS` + `EXPECTED_META` + comment chain + `CANONICAL_CONTENT_SHA256 = EE1CE2A2..`

**แล้วคำถามต่อมาคือ verifier ตรวจอะไรบ้าง — คำตอบ: ตรวจแค่ว่าไฟล์ที่ถูกอ้าง "มีอยู่"**
🔴 **"มีอยู่บนเครื่องคนเขียน" ≠ "อยู่ในรีโป"** และมีแค่อย่างหลังที่แปลว่า *หลักฐาน* สำหรับคนที่ clone ทีหลัง
กวาดทุก `evidence_refs` + `source_refs` เทียบ `check-ignore` เจอ **2 จุด**:
① `tools/pf_runtimeres_death_headless_replay.py` — HYP-PF-023 อ้างเป็นหลักฐาน แต่ถูก ignore
   (คอมเมนต์ allowlist ของรอบ 86 เขียนว่า "Five files" ทั้งที่มี 6 — **นับด้วยร้อยแก้วไม่ใช่การตรวจ**)
② `reports/PF_RE_V107_to_V110_..._20260814.md` — **HYP-PF-008 + HYP-PF-010 ที่ยัง active อ้างอยู่**
   ถูก ignore ตั้งแต่วันที่เขียน (14 ส.ค.) ⇒ **fresh clone ไม่เคยมีเอกสารที่สองข้ออ้างนี้ยืนอยู่**
**แก้โดยเพิ่มไฟล์ ไม่ใช่ตัด reference** (reference คือส่วนที่ถูก) + เทสกวาดถาวรพร้อม trap ที่พิสูจน์แล้วว่าแดงได้จริง
· จงใจทำเป็น **เทส ไม่ใช่ guard ใน verifier** เพราะเป็นคำถามเดียวในโซนนี้ที่ตอบจาก worktree อย่างเดียวไม่ได้ ต้องถาม git
  — verifier ต้องรันได้ด้วย stdlib ล้วนและไม่มีรีโป

### 🆕 เลน E — CP874-PORTABILITY-001 (รอบ 87 · **gate เป็นคนหาเจอ**)
job 142 กลับมา `census=1` + `pytest=1` = **2 ช่องแดง สาเหตุเดียว**
`tools/pf_vital_thunk_census_static.py` `print()` อิโมจิ 🔴 (U+1F534) · **คอนโซล Windows = code page 874**
อักขระที่ map ไม่ได้ **ไม่กลายเป็น `?` แต่โยน `UnicodeEncodeError` ใน `print()`** ⇒ เครื่องมือตายคาที่ ไม่รายงานผลอะไรเลย
· sandbox เป็น UTF-8 จึงเขียว **บนไบต์ชุดเดียวกัน** ⇒ **เขียวเครื่องหนึ่ง ตายอีกเครื่องหนึ่ง**
· (ภาษาไทย `(ข)` บรรทัด 301 **ไม่พัง** เพราะ cp874 คือ code page ไทย — ตัวที่พังคืออิโมจิเท่านั้น)
**แก้:** เอาอิโมจิออกจาก print (คำพูดเหมือนเดิม) + เทสใหม่ encode stdout/stderr ของทั้งสองเครื่องมือเป็น cp874
แดงพร้อมบอกอักขระ + เลขบรรทัดของ output · **ตรวจที่ output ไม่ใช่ source** เพราะคอมเมนต์ไทยไม่เป็นอันตรายและจะอยู่ต่อ
· ทดสอบ trap แล้ว: ใส่อิโมจิกลับ → แดงและชี้ `'🔴' (U+1F534) ... at output line 45`

### ⚠️ ข้อจำกัด sandbox ที่เจอรอบนี้ (จดไว้กันเสียเวลารอบหน้า)
- `pytest` เต็มชุดใน sandbox ใช้ ~160 วิ **แต่ตอนเซสชันหลักรันเกมอยู่ มันช้าลงหลายเท่าจน timeout 178 วิไม่พอ**
  ⇒ ถ้าจำเป็นให้แบ่งเป็นก้อนละ ~5 ไฟล์ · **gate จริงคือ Windows `py -3` อยู่แล้ว**
- sandbox ต้อง `pip install pytest capstone pefile --break-system-packages` และ **symlink สองอัน**:
  `/tmp/GameClient` → `../GameClient` และ `/tmp/pf_bridge` → `../pf_bridge` (เครื่องมืออ้าง path แบบ sibling ของรีโป)
- `rm` บนไฟล์ในโฟลเดอร์ที่ mount ไว้ = **Operation not permitted** ⇒ การลบไฟล์ต้องทำผ่าน job บน Windows bridge
  (นี่คือเหตุผลที่ job 143 มีขั้นลบ `_append_hyp_pf_023.py`)

### ผลการรันใน sandbox ก่อนส่ง gate
**1303 passed / 1 skipped / 2557 subtests** · แดง 1 ตัวคือ `test_server_shutdown` `__notes__`
= artefact ของ **Python 3.10** ใน sandbox (`add_note` ต้อง 3.11+) **ไม่ใช่ข้อบกพร่องของโค้ด** — บน gate เขียว (job 142 ยืนยันแล้ว)

### next รอบ 88 (pre-approved ทั้งหมด)
1. 🔴 **ย้าย `staged\143_...ps1` ไป `inbox\` ทันทีที่ LOCK ว่าง** — นี่คืองานแรกสุด งานอื่นรอได้
2. อ่านผลรอบใหญ่ #6 จากกล่องจดหมาย (GT-021 dying_hold / GT-017 XP / GT-015 swap) แล้วย้ายเข้า queue/matrix
3. **หนี้ที่เพิ่งเห็นและยังไม่ทำ:** `tools/pf_vital_name_thunk_static.py` และ `pf_vital_thunk_census_static.py`
   default path ของ tsv เป็นแบบ **sibling-relative ของรีโป** ⇒ เป็น scan-site แบบเดียวกับที่รอบ 82 ไล่เก็บ
   (ยังไม่ใช่ของด่วน แต่ควรจดไว้ในสำรวจรอบหน้า)
4. หนี้เก่า: ค่า live ของ `0x107A2C0` ตอน GT-011 ยังเป็นเดา (ค้างตั้งแต่รอบ 81)
5. ~~งานแม่บ้าน archive~~ **ทำแล้วในรอบ 87** — รอบ 84–85 ย้ายไป
   `archive\CHIEF_CONTINUATION_ARCHIVE_20260819_R84_R85.md` · ไฟล์หลักลดจาก 103KB → **64KB**
   · `GAME_TEST_QUEUE.md` = 53KB ยังต่ำกว่าเพดาน ~60KB ไม่ต้องทำอะไร

### 🔴 คำถามค้างรอ Panya เคาะ (ยังไม่ตอบ 4 รอบแล้ว)
> **DAMAGE-MODEL-001 ปิดทาง 2 แล้ว — จะไป "ทาง 1 ออกแบบสูตรความเสียหายเอง" ไหม และขอบเขตแค่ไหน?**
> คำขอเล็กมาก: **i32 มีเครื่องหมาย 1 ตัว + flag word 1 ตัว ต่อเป้าหมาย** ทดสอบครบวงแบบ HYP-PF-021/022/023
> · multiplayer ก้อน 2/3 ก็ยังรอเคาะ (Option 1 จบตั้งแต่รอบ 81)
> 🆕 **บริบทจากรอบ 86:** ตอนนี้ท่อที่ทำให้ตายจริงมีโค้ดแล้ว (HYP-PF-023) ⇒ วง "ตี → เลือด → ตาย" เหลือแค่ชิ้นกลาง


## รอบ 89 (2026-08-19 16:3x–18:xx scheduled) — **บัญชีใหม่รอบแรก · DEATH-ESCALATE-001 + BRIDGE-LIVENESS-001 + งานแม่บ้านส่งกะ**

> 📌 **รอบนี้เป็นรอบแรกของบัญชี Claude ใบที่สอง** (สลับกะตามแผน 3 วัน/3 วัน) · cron = รายชั่วโมง
> รอบ 88 ของบัญชีเดิมถูกตัดกลางคันตอนโควตาหมด **งานค้างอยู่ในทรีครบ** → รอบนี้ทำต่อ ไม่ได้เริ่มใหม่

### สถานะตอนรับช่วง (17:0x)
- HEAD `44a3ed7` (job 143 commit สำเร็จ 11:36) · canonical `6BFCEDD5..8FC7` ไม่ขยับ · ledger 30 entries
- worktree dirty **1 path**: `src/pirateforce_foundation/stats_progression_hypothesis.py` (+216 บรรทัด)
- `LOCK_GAME.txt` = **HELD โดยเซสชันหลัก ATTENDED** (รอบใหญ่ #7 · GT-022) · `LOCK_GIT.txt` = FREE
- กล่องจดหมายมี **6 ฉบับ** รอบริโภค (รวมโน้ตขาออกเก่าของ chief 1 ฉบับ)

### 🔴 งานค้างรอบ 88 ที่พบ: DEATH-ESCALATE-001 ค้างกลางคัน **แบบประกาศตัวเอง**
รอบ 88 เขียน encoder ของเฟรมที่สี่เสร็จ **แต่หยุดก่อนทุกอย่างที่เหลือ**: ไม่มี pin ของสเต็ปใหม่
ไม่มี scenario ไม่มีเทส ไม่มี verifier guard ไม่มี ledger amendment
⇒ ทรี **แดง 31 เทส** ทันทีที่ import (`KeyError: 'TIMER_ELAPSED'` ตอนโหลด scenario)
🟢 **นี่คือ fail-closed ทำงานถูกอีกครั้ง** (แบบเดียวกับรอบ 86→87): สถานะครึ่ง ๆ กลาง ๆ **ไม่ได้นอนเงียบในทรีเขียว**

### เลน A — DEATH-ESCALATE-001 (งานหลักของรอบ · ปิดจบทั้งเลน)
**สิ่งที่เพิ่ม = เฟรมเดียว** `TIMER_ELAPSED` ต่อท้าย profile `dying_hold`: identity เดิม · `hp_current` ยัง 0 ·
`hp_death_timer` = **positive zero ที่ปักไว้** (สาย: tag `0x2A` + สี่ไบต์ศูนย์) · mask `0x038C` · body 78B / PC 111B / frame 122B
- **ทำไมต้องมี:** GT-021 วัดมาแล้วว่า client **ไม่ลด timer เอง** (ค้างเกิน 4 นาที) + static ไม่เจอผู้เขียน `+0x58` รายเฟรมเลย
- **predicate ที่เฟรมนี้ทำให้เป็นจริง:** `vt+0x3C` = `0x454A70` (HP==0 && timer<=0) ซึ่งเป็นตัวที่
  `CMyActor::Update` อ่านที่ `0x44E58D` ก่อนเปิด `L"Common_Death"` ที่ `0x44E5C7` **ที่เดียวในอิมเมจ**
- ⭐ **ข้อที่พลาดง่ายที่สุดและเป็นตัวชี้ขาด: เฟรมนี้ต้อง "ติดบิต 0x0080" ไปด้วย**
  `BasicAttr::Merge` (`0x465610` เรียกที่ `0x5F2504`) **คัดลอกค่าเก่าไปข้างหน้าเมื่อบิตไม่ติด** (`0x4656A3`)
  ⇒ การ "ไม่ส่งบิต" ไม่ใช่การรีเซ็ต แต่คือการ **แช่ค่า 20.0 ไว้ตลอดกาล**
- **ประตูของ elapsed band ปิดโดยดีฟอลต์ มีกุญแจดอกเดียว = step label ที่ profile ประกาศเอง**
  (`_require_hp_death_elapsed_gate`) · call site เก่าทุกตัวไม่ส่ง label ⇒ ยังได้ `death_timer_not_positive` เหมือนเดิม
- **rejection ใหม่ 4 ตัว fail closed:** `elapsed_gate_is_not_a_bool` · `..._is_not_the_pinned_zero`
  (−0.0 แพ็กเป็น `00 00 00 80` = คนละสี่ไบต์) · `..._outside_the_pinned_final_step` · `..._without_zero_hp`
  · **NaN ถูกปฏิเสธเป็น not_finite** เพราะ `comiss` unordered ⇒ `jb` ถูกกิน ⇒ predicate **false** (ตรงข้ามกับเจตนา)
- **verifier:** +5 byte guard กับอิมเมจจริง → **137 guards PASS, skipped 0**
- **headless:** `pf_hp_death002_headless_replay.py --profile dying_hold` (เพิ่ม flag `--profile` แทนการทำเครื่องมือใหม่)
  → dispatcher จริงตอบ **4 เฟรม** เฟรมสุดท้ายเข้าเงื่อนไข elapsed predicate · **37 guards PASS**
- **ledger:** **amend HYP-PF-022 ไม่ได้เพิ่ม entry** (ยัง 30) · sha ใหม่ `D69DA821..`
  🔴 **แถมแก้ stop rule ที่ล้าสมัยมาตั้งแต่รอบ 84**: เดิมเขียนว่า "ห้ามส่งสวีปที่ไม่จบด้วยเฟรมชุบ"
  ทั้งที่ profile `dying_hold` ขัดข้อนี้อยู่ในทรีแล้ว ⇒ เขียนใหม่ให้ตรงกับกติกาที่บังคับจริง
  · `tracked_versions` = HP-DEATH-002 / DYING-HOLD-001 / DEATH-ESCALATE-001 ⇒ **เต็ม max_versions=3**
  ⇒ **การขยายเลนนี้ครั้งหน้าต้องเปิด entry ใหม่หรือขออนุมัติ ไม่ใช่เพิ่ม profile อีกใบ**
- **.gitignore:** เพิ่ม allowlist ให้ `reports/PF_RESCUE_AND_DEATH_ESCALATION_STATIC_20260819.md`
  (รอบ 88 เขียนรายงานไว้แต่ถูก ignore ทั้งที่ ledger อ้างเป็นหลักฐาน — บทเรียน LEDGER-VISIBILITY-001 ซ้ำรอบที่สาม)
  ⇒ seam test บังคับ (รันแล้ว OK)

### 🆕 เลน B — BRIDGE-LIVENESS-001 (**ไม่ได้อยู่ในแผน · คุ้มที่สุดของรอบรองจากเลน A**)
วางจ็อบ 144 ลง inbox 17:23 แล้ว **ไม่มีอะไรเกิดขึ้นเลย 14 นาที** สืบแล้วเจอโหมดพังใบใหม่:
- `906` รันจบ 16:50:59 เขียน outbox ครบ **แต่ไฟล์ไม่ถูกย้ายไป `done\`** (ต่างจาก `905` ที่ย้ายปกติ)
  ⇒ ลูปตายคาระหว่าง "เขียน output" กับ "ย้ายไฟล์" — อาการของคอนโซลที่เข้าโหมด Select (QuickEdit)
- `watchdog_last_check.txt` เขียน `bridge-alive` ทุก 5 นาทีตลอดเวลานั้น
  🔴 **"process อยู่" ≠ "loop เดิน" — watchdog เดิมแยกสองอย่างนี้ไม่ออกเลย**
**แก้แล้วสองไฟล์ (นอกรีโป ไม่เข้า commit):**
1. `pf_bridge.ps1` เขียน `bridge_loop_state.txt` ทุก poll + รอบทุกจ็อบ (`idle` / `running <job>`)
   · สำรองต้นฉบับ `pf_bridge.ps1.bak_20260819_r89_before_loop_heartbeat` (ห้ามลบ)
2. `pf_bridge_watchdog.ps1` ถือว่า "ค้าง = ตาย" 3 กรณี: `idle` เก่ากว่า 12 นาที · `running` เก่ากว่า 25 นาที
   · **หรือมีไฟล์ค้างใน `inbox\` เกิน 25 นาที ทั้งที่ไม่มีจ็อบไหนอ้างว่า running** (ข้อนี้ออกแบบมาเพื่อกู้เคสวันนี้
   ซึ่งสะพานตัวที่ค้างยังไม่รู้จักไฟล์ state) → kill + start hidden + จดเหตุผลลง `watchdog.log`
   · **ถ้าไม่มีไฟล์ state = ไม่ฆ่าใคร** (ไม่มีหลักฐาน ≠ หลักฐาน)
**พิสูจน์แล้วว่าใช้ได้จริงในรอบเดียวกัน:** 17:37:02 watchdog จับได้เอง (`inbox\906... has waited 46.2 min`)
→ kill pid 13332 → เปิด hidden ใหม่ → **17:37:06 หยิบจ็อบ 144 ทันที**

### เลน C — งานแม่บ้านส่งกะ + กล่องจดหมาย
- บริโภคกล่องจดหมายครบ **6 ฉบับ** → คัดลอกไป `consumed\` + เขียนใบปะหน้าทับต้นฉบับ
  ⚠️ **ข้อจำกัดที่ต้องจำ: แซนด์บ็อกซ์ ลบ/ย้ายไฟล์ในโฟลเดอร์ mount ไม่ได้** (`Operation not permitted`)
  ⇒ "ย้ายไป consumed" ทำได้แค่ **copy + เขียนทับด้วย stub** เท่านั้น
- `LOCK.txt` ใบเก่า → เขียนหัว **DEPRECATED** ชี้ไปสองธงใหม่ (เก็บเนื้อเดิมเป็นประวัติ)
- คิวเทส: กรอกผลรอบใหญ่ #6 ครบ (GT-015 PASS · GT-017 PASS · GT-021 PARTIAL) · GT-022 → RUNNING
  · **เพิ่ม GT-023 ใหม่** (เฟรมที่สี่ → `Common_Death`) พร้อมสเปกครบทีละคลิก
- ตอบคำถามค้างของผู้เทส: **`agent_kit\` commit ไม่ได้เพราะ `pf_bridge\` อยู่นอก git repo**
  (คำถามนี้เกิดจากความเข้าใจผิดว่าทั้งโฟลเดอร์ Desktop คือรีโป — จดไว้กันถามซ้ำ)
- แก้ skill ของผู้เทสให้ตรงกติกาสองธง + cron รายชั่วโมง + โหมดพังใหม่ของสะพาน
  ⚠️ **เขียนทับ `skill_pf-attended-test.md` ไม่ได้ (ไฟล์ถูกล็อกฝั่ง Windows: `EPERM rename`)**
  ⇒ ออกเป็นไฟล์ใหม่ `agent_kit\skill_pf-attended-test_R89_UPDATED.md` ให้ผู้เทสติดตั้งทับเอง

### เลน D — DAMAGE-MODEL ทาง 1 (ลูกมือทำขนานไปกับเลน A)
`drafts/DAMAGE_MODEL_LANE1_DESIGN_20260819.md` (663 บรรทัด) — **เอกสารออกแบบ ยังไม่แตะ src/**
- สูตรที่เสนอ: `ATK = 100 + 7*(str+bonus) + 3*lv` · `DEF = 10 + 2*(con+bonus) + 1*lv` · `base = max(ATK-DEF, 1)`
  · integer ล้วน ไม่มี RNG (phase 1) · **ค่าที่ส่งบนสายเป็นลบ** (`jge` 4 จุดพิสูจน์ว่าลบ = โดนตี · จอโชว์บวกเพราะ `abs()`)
  · แบนด์ปลอดภัย `[-1_000_000, 0]` · ปฏิเสธ `INT32_MIN` แยกข้อ · **ค่าบวกห้ามส่ง** (heal/absorb ยังไม่รู้)
  · flag word allowlist ระดับค่าเต็ม `{0x0000 miss, 0x0001 hit, 0x0009 hit+reaction}`
- เสนอ **HYP-PF-024** + ชุดชื่อไฟล์ครบ (module/scenario/policy/flag/verifier/tests/prefix) + rejection 28 ข้อ
- 🔴 **สามอย่างที่ยัง "เดา" และต้องปิดก่อนเขียน encoder:** ① version byte ของ vital `0x16F7` ไม่มีที่ไหนบอก
  ② ยังไม่พิสูจน์ว่า factory ของ VitalData collection สร้าง `0x16F7` ได้ ③ หัวเฟรมฟิลด์ 2–5 ไม่รู้ความหมาย (แผนปัก 0)

---
