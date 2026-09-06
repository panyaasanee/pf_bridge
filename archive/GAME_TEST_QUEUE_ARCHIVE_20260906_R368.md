# GAME_TEST_QUEUE.md - ARCHIVE 2026-09-06 (chief LANE-E round u2o8d7 / R368)

Verbatim bodies of a SHORT, HAND-CHECKED allowlist of closed tickets, moved out of the live
queue file.  Each block is byte-identical to what stood in the live file and the live file keeps a
one-line stub pointing here.  Selection was NOT done by status regex: pf-adversary proved that
regex-driven selection cut two OPEN tickets (GT-133, GT-178) out of the live file and archived six
tickets whose own headers say they are not closed.  This file therefore carries only tickets whose
H2 header was read by hand and whose closure is unambiguous, and only those closed well over 24h
ago.  Round file R368 records the full finding.


## GT-001 Smoke: full-loop บน canonical DB หลังทุก commit สำคัญ  [🟢 **PASS รอบ UA1 — ปิดโดย chief R232**: `OBSERVER_CONFIRMED: 2026-08-29T19:1x+07:00 โดย Panya ("ยืนยัน" ทั้งรอบ UA1 · ถ่ายทอดผ่านกะ3-A ใบ `20260829_1919` §① — นาทีเป๊ะตามที่ใบบันทึก)` · หลักฐาน smoke = รอบ unattended UA1 (ใบ `20260829_1552` §③, BOOT_COMMIT `33572b24`: boot→login→เข้าแมพ→teardown สะอาด) · **HOLD (recurring) ปลดสำหรับรอบนี้ตามเงื่อนไข v6.3 หัวข้อ 18 ข้อ 7 — recurring ใบยังเปิด รอบถัดไป re-arm ตามปกติ** · ประวัติ HOLD: ดูการแก้ไขของ chief R175 ใต้หัวใบ · 🟡 บันทึกเดิม R230 (ก่อนคำยืนยันมา): AWAITING-OBSERVER เพราะใบ `1728` ยืนยันเฉพาะ GT-063 · **PASS ล่าสุด: `f8562c1` (R168) 2026-08-25 20:43 (+07:00) — PASS พร้อม erratum** · *(PASS ก่อนหน้า: `fa1e804` 2026-08-24 09:41 · R145)*] 🔁

> ### 🔴🔴 R175 correction (chief R175 · 2026-08-26, พบโดย `pf-adversary`) — HOLD ไม่ได้ถูกปลด ต้องขอโทษที่เขียนผิดไปก่อนหน้านี้ในรอบเดียวกัน
> รอบนี้เคยแก้หัวใบเป็น "HOLD ปลดแล้ว" โดยอ้าง `parse errors = 0` และ "ทดสอบสองทาง (หันอยู่กับที่/เดิน 40 หน่วย)"
> **ข้อความสองท่อนนั้นสืบไม่ถึงเอกสารใดในรีโปเลย** — ตรวจแล้วด้วย `pf-adversary`: `notes_to_chief/consumed/20260825_2335_COO-DECISION-R170-*.md:32`
> (จดหมายที่ให้เลขบรรทัด 37-44 มาแต่แรก) เขียนไว้เองชัดเจนว่า **"ยังไม่ได้รัน... จะไม่ขอปลด HOLD จนกว่าจะมีจ็อบ parse-check รันผ่านจริง"**
> และตารางท้ายจดหมายเดียวกันยังคงให้ "parse-check `1166` แล้วรายงาน" เป็นงานค้างข้อ 2 (ยังไม่มีเครื่องหมายว่าเสร็จที่ไหน)
> ที่มาของข้อความที่เขียนผิดไปคือ bullet เดี่ยวในจดหมายส่งมอบกะสองใบ (`HANDOVER-TO-SHIFT-1` และ `HANDOVER-CHIEF-PROMPT-v6-full`)
> ที่บอกว่า "รันผ่านจริงแล้ว" **โดยไม่มีเลขจ็อบ ไม่มีเวลา ไม่มี output แนบมาเลย** — ไม่ต่างจาก bullet เดี่ยว จึงไม่นับเป็นรายงานตาม G1/G8
> ⇒ **คืนสถานะ HOLD** จนกว่าจะมีจดหมายที่อ้างเลขจ็อบ/เวลา/ output จริงของการรัน `1166_gt001_teardown_verify_update_canon.ps1` แบบ parse-check
> 🔴 **บทเรียน:** ห้ามยกรายละเอียดที่ "ฟังดูสมเหตุสมผล" (เช่นวิธีทดสอบสองทาง) มาเติมให้ข้อความบาง ๆ ดูสมบูรณ์ขึ้น — ถ้าไม่มีจดหมายอ้างอิงได้ ให้เขียนว่า "ยังไม่มีรายงาน" ตรง ๆ
>
> ### 🔴🔴 HOLD เดิม (chief R170 · `pf-adversary` จับได้) — ยังมีผลอยู่ ยังไม่ปลด
> เกณฑ์ `samePos` ยังเทียบ `heading` อยู่ และ **`heading` เปลี่ยนทุกครั้งที่ตัวละครหันหน้า**
> ⇒ หยิบใบนี้ตอนนี้ = **`ABORT(20)` ซ้ำแน่นอน ก่อนถึงขั้นอัปเดต `CANON_SHA.txt`** ⇒ **การ์ด CANON ของทุกใบ abort ตาม = สะพานบูตไม่ได้ทั้งสะพานอีกรอบ**
> 🟢 **ปลด HOLD ได้เมื่อ:** สคริปต์เทียบเฉพาะ `X`/`Y`/`Z` และรายงาน `heading` โดยไม่ตัดสิน (ใบสั่งอยู่ในจดหมาย `FROM_CHIEF_R170_*`) ⇒ ผู้ที่แก้ **ตอบกลับมาว่าแก้บรรทัดไหน** แล้ว chief ปลดให้รอบถัดไป
> 🔴 **chief ปลดเองจากคลาวด์ไม่ได้** — สคริปต์อยู่บนสะพาน ไม่อยู่ในรีโป

> ### 🟢 ผลรอบ 2026-08-25 20:43 (+07:00) — **PASS พร้อม erratum** (chief R170 · จ็อบ 1164/1165/1166)
>
> **boot:** `f8562c14781809b39a124f11029d1a6faff60f63` (คอมมิต R168 · merge เข้า `main` ทาง PR #34) ⇒ **ครอบทุกอย่างที่ merge วันนั้น**
> ```
> selected        10 -> 11      ตรงที่ใบคาด
> lease           11 -> 12      ตรงที่ใบคาด
> open sessions   0             integrity ok      FK 0      กระเป๋าเหมือนเดิมทุกแถว
> POS  X -8553.947265625   Y -2579.68896484375   Z 186.0    <- เหมือนเดิมทุกหลัก
>      heading  4.53208589553833 -> 3.1123385429382324      <- เปลี่ยน
> ```
>
> 🔴 **erratum — ข้อบกพร่องของ *เกณฑ์* ไม่ใช่ของเซิร์ฟเวอร์:** `1166_gt001_teardown_verify_update_canon.ps1` เทียบแถว `POS` **ทั้งแถวรวม heading** ⇒ `samePos=False` ⇒ `ABORT(20) DB delta criteria failed`
> **ทุกเกณฑ์อื่นผ่านหมด และเดลต้าทั้งก้อนคือสิ่งที่ใบคาดไว้เอง** ⇒ **chief ตัดสิน: ใบนี้ = PASS**
> 🟢 **คำตัดสินเกณฑ์ (chief R170):** เกณฑ์ `samePos` ต้องเทียบ **`X`/`Y`/`Z` เท่านั้น** · **`heading` ให้รายงานแต่ไม่ตัดสิน**
> 🔴 **สคริปต์อยู่บนสะพาน — chief แก้เองไม่ได้จากคลาวด์** ⇒ ใบสั่งแก้อยู่ในจดหมาย `FROM_CHIEF_R170_*` (แก้แล้วให้ตอบกลับมาว่าแก้บรรทัดไหน)
>
> 🆕 **ของแถมที่ไม่มีใครเคยจด: เซิร์ฟเวอร์เขียน `heading` ลง canonical จริง**
> ตัวละคร **ไม่ได้เคลื่อนที่เลย** (X/Y/Z ตรงกันทุกหลัก) แต่ **ทิศที่หันหน้าถูกบันทึก** ⇒ ต่อยอดจาก `GT-041`
> 🔴 **nonclaim:** ยังไม่รู้ว่า heading ถูกเขียน **ตอนไหน** (ระหว่างเล่น / ตอนออก) และ **ไม่รู้ว่าอ่านกลับมาใช้ตอน relog หรือไม่** — **สังเกตครั้งเดียว ยังไม่ใช่คุณสมบัติ**
>
> 🔴 **ผลลูกโซ่ของการ abort — และคำเคาะของเจ้าของ:** จ็อบ abort **ก่อน** ขั้นอัปเดต `CANON_SHA.txt` ⇒ canonical เปลี่ยนแล้วแต่ไฟล์ยังเป็นค่าเก่า ⇒ **การ์ด CANON ของทุกใบ abort ทั้งหมด**
> 🟢 **เจ้าของเคาะ: รับค่าใหม่เป็นฐานใหม่** (คำเคาะข้อ 1 · จดหมาย `20260825_2110`) ⇒ ผู้ช่วยอัปเดตแล้วและ chief ยืนยันค่าในรีโป:
> ```
> CANON_SHA.txt  670CE534...FEC21  ->  4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454
> backup ก่อนรอบ: backup\pirateforce_before_GT-001_20260825_204328.sqlite3 = 670CE534...FEC21  (ตรวจ sha แล้ว)
> ```
> 🔴 **กฎใหม่ที่ chief รับจากข้อเสนอของผู้ช่วย:** *จ็อบที่ **เขียน** canonical ต้องอัปเดต `CANON_SHA.txt` **ก่อน** ตรวจเกณฑ์ผล หรือไม่ก็ต้องมีขั้นกู้คืนเมื่อ abort*
> เหตุผล: ตอนนี้ **การ abort ของเกณฑ์ตัวเดียวทำให้สะพานทั้งสะพานบูตไม่ได้** — abort ที่แพงเกินกว่าเหตุ

> 🔁 **อัปเดต chief R167 · 2026-08-25 ~19:xx (+07:00) — ใบนี้ *ถึงกำหนดจริง* ไม่ใช่ของแถม**
> ตั้งแต่ PASS ล่าสุด (`fa1e804`) `main` ขยับไปแล้วทั้ง PR #24–#32 **และ R167 กำลัง merge เลนใหม่ที่แตะ `src/` อีกก้อน**
> (`ground_loot_nameprop_hypothesis.py` + wiring ใน `app.py`/`runtime.py` + เพดานเวอร์ชัน ledger ทั้งไฟล์)
> ⇒ บูตที่ commit **หลัง merge ของ R167** · `CANON_SHA` จะขยับตามที่ใบคาดไว้เพราะใบนี้รันบน canonical DB จริง (ต่างจากรอบ GT-033 ที่รันบนสำเนา)


> ✅ **PASS R145 (ผลหน้าสะพาน 2026-08-24 09:41 +07:00 · Codex LOCAL):** full loop บน resolver-green `fa1e804` (tree ตรง main HEAD `94f0ce3`) — login → Port Royal → ออกด้วย X · selected sessions `9→10` · max lease `10→11` · open sessions หลังหยุด 0 · `integrity_check=ok` FK 0 · frame proof 3/3 · **`CANON_SHA.txt` อัปเดตแล้วโดยสะพาน** `EE785A79…` → `670CE534…` (การเข้าเกมเพิ่ม selected session/lease ตามที่ใบคาด)

> ✅ **RESULT 2026-08-23 01:10–01:14 (+07:00) — PASS บน main HEAD `cf81730` (worktree clean)** · full loop: login → Channel 1 → PVP → Arena01 → เข้าแมพ (HP 100/100 · Port Royal · chat online) → ออกด้วย X+ยืนยัน → Ctrl+C สะอาด
> canonical DB SHA เปลี่ยน**แบบคาดหมาย** (session +1): `6BFCEDD5…FE498FC7` → `23FD885AC4CBBFAC5E06C9B11506F6EA9F985DA82F4522383DFCC14A91C1816A` · `CANON_SHA.txt` อัปเดตแล้วโดยผู้เทส · backup ค่าเก่ายังอยู่
> ผลเต็ม: `notes_to_chief/20260823_0115_GT001-PASS-latest-main-smoke.md` (บริโภค R123)

> ✅ **RESULT รอบใหญ่ #3 — PASS ทุกเกณฑ์ที่ `f286945`** · รายละเอียดเต็มย้ายไป archive รอบ 97:
> `archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R97_CLOSED_STUBS.md` ก้อน 2
> - 🔁 **re-arm รอบ 78:** commit รอบ 78 แตะ `src/` (app.py + runtime.py + โมดูลใหม่ — ทุกจุดอยู่หลังธง scenario ที่ boot ปกติไม่ใช้ → ความเสี่ยง regression ต่ำมาก) → เทสที่ HEAD ใหม่ของรอบ 78
> - 🔁 **re-arm รอบ 95:** commit `72d6129` แตะ `src/` (damage_model_hypothesis.py + runtime.py — ทั้งหมดอยู่หลังธง scenario opt-in ที่ boot ปกติไม่ใช้ · full suite 1530 passed บน Windows · ความเสี่ยง regression ต่ำมาก)
> - 🔁 **re-arm รอบ 97 (ล่าสุด — ครอบ commit รอบ 96+97):** `8dfd303` (remote_player) และ `af10536` (damage_hp_link) แตะ `src/` ทั้งคู่ (app.py + runtime.py + โมดูลใหม่ — ทุกจุดอยู่หลังธง scenario opt-in ที่ boot ปกติไม่ใช้ · full suite **1803 passed 1 skipped** บน Windows · ความเสี่ยง regression ต่ำมาก) → **GT-001 = PENDING ที่ `af10536`** รันในรอบใหญ่ถัดไปตามท่ามาตรฐาน PLAYBOOK
> - 🔁 **re-arm R125 (ล่าสุด):** PR #9 GROUND-LOOT-001 merge เข้า `main` แตะ `src/` (app.py + runtime.py + โมดูลใหม่ —
>   ทุกจุดอยู่หลังธง scenario opt-in ที่ mutually exclusive กับโหมดอื่น · boot ปกติไม่เปลี่ยน · เขียว(Actions run 32616696590 · subset))
>   → **GT-001 = PENDING** · **บูต commit จาก `pf_resolve_green_boot.py` ตอนจะรันจริง — จงใจไม่พิน hash ในใบนี้**
>   (ทุก merge ระหว่างหน้าต่างไม่เฝ้าเครื่องจะขยับ HEAD ได้อีก · resolver คือคำตอบเดียวที่ไม่ stale)

> 🗂 **ประวัติ re-arm รอบ 52 / 53 / 65 (superseded โดย re-arm รอบ 78 ด้านบน) ย้ายไป
> `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260819_R85_HOUSEKEEPING.md`** (chief รอบ 85)

- objective: ยืนยันว่า commit ล่าสุดบน main ไม่ทำให้ loop พื้นฐานพัง
  (login → select → เข้าแมพ → ออก → server exit 0)
- db: `state\pirateforce.sqlite3` (ค่าเริ่มต้น)
- server args: `-SecondPasswordMode bypass`
- steps: ตาม PLAYBOOK ทั้ง 8 ข้อ
- pass criteria: เข้าแมพเห็นครบ (HP/minimap/ชื่อแมพ/chat online) + ออกสะอาด X+ยืนยัน +
  stopped ×1 + stderr 0B + listeners 0 + sessions +1 (นับแบบ selected_character_id IS NOT
  NULL) + lease +1 + backpack `[1@0,2@1,4@3]` เดิม + position เดิม (ถ้าไม่เดิน) + integrity ok
- nonclaims: ไม่พิสูจน์ inventory/combat/movement · path delete/logout/chat แยกเทสของตัวเอง
- หมายเหตุ recurring: หลัง commit ใดแตะ src/ ให้ตั้งกลับเป็น PENDING พร้อม hash ที่จะเทส
- result: (ผู้เทสกรอก)


## ⭐ GT-060 PICKUP-CLICK-CAPTURE-001 [attended, in-game]: คลิกซ้ายบน drop-object ที่วาดจริงบนจอ แล้วจับเฟรม `PickupTerrainThing` **ตัวจริงตัวแรก** บน wire — id `0x4543` ที่ derive ไว้ ถูกหรือผิด  [❌ **CANCELLED - covered by GT-146** · ปิดโดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 ตาม `COO-DECISION 20260904_2349` ข้อ 4 · `GT-146` ถามคำถามเดียวกัน (คลิกซ้ายบนของตกที่เซิร์ฟเวอร์ส่งเอง แล้วไคลเอนต์ยิงเฟรมอะไร) ด้วยขั้นตอนที่ใหม่กว่า ⇒ ใบนี้ไม่ต้องใช้เวลาผู้เทสอีกใบ · 🔴 หมายเหตุ: `GT-146` เองอยู่ในสถานะ `BLOCKED - until P-2 closes (NOW)` ⇒ คำถาม opcode ยังไม่ถูกตอบด้วยตา ยังเปิดอยู่ แต่ถืออยู่ที่ `GT-146` ใบเดียว ไม่ใช่สองใบ · เนื้อใบและเงื่อนไขเดิมเก็บไว้ข้างล่างเพื่อการอ้างอิง (ห้ามลบ) — เดิม: **BLOCKED-CONDITIONAL — ห้ามบูตจนกว่าเงื่อนไข (ก)(ข)(ค) ข้างล่างครบทั้งสามข้อ** · เลน server = HYP-PF-036 (R151 · ✅ (ก) ปิดแล้ว R152: PR #22 merge เข้า `main` `2c0e3ba`) · เงื่อนไข (ข) เหลือแค่ผลตา GT-045 (นัด 2026-08-26) — คำเคาะ composition มาแล้ว (จดหมาย 1831 §①) และโค้ด composed-boot merge เข้า `main` แล้ว (R154: PR #23 → `cad3e28` เขียว Actions run 32726495224) · ✅ **(ค) ปลดแล้ว — Panya ปลดพักเลน attended ทั้งเลน (2026-08-24 ~21:1x +07:00 · จดหมาย 2120 §① · บันทึกโดย R155)** — คำสั่งพัก 16:56 ของ 23 ส.ค. สิ้นสุด · กฎรอบ unattended ยังเหมือนเดิมทุกตัวอักษร · 🆕 R155: คำเคาะ 2120 §② ขยาย allow-list เป็น**สามตัว** `ground-loot + pickup-listener + item-operate-res` — ใบนี้ได้ประโยชน์ถ้ารวมบูตกับ GT-063 (โค้ดสามตัว = PR #25 รอ gate — ดูหัวใบ GT-063)]

**ที่มา:** สามใบประกอบกัน — **GT-046** (STATIC PASS: `PickupTerrainThing` เป็น **outbound** สร้างที่ call `0x006B0639` เติมค่าจาก live runtime drop-object · ตัวจุดชนวน = `WM_LBUTTONDOWN` ที่ `0x006B0570` **เฉพาะเส้นทาง in-range**) + **GT-045** (WIRE PASS / CLIENT NO-RESULT — การวาด drop-object จาก wire ยังพิสูจน์ไม่ได้ รอเทสตา) + เลน server ใหม่ **HYP-PF-036** (R151): inbound listener หลัง `--pickup-listener-hypothesis-scenario` — เมื่อเฟรมขาเข้ามี nested vital id `0x4543` มันจะ decode-count-record (`object_ref_u32` · `opaque_u8` · raw body hex) ลง session state `pickup_listener_accepted_count`/`records`/`refusals` และปล่อย **log บรรทัดเดียว ASCII** · **ไม่ตอบกลับ ไม่เขียน DB** · ไบต์ผิดรูป = refusal มีชื่อถูกจดไว้ · codec อิง `external\PF_SERIALIZER_FIELDS.tsv` แถว 859-862

**หมวด:** attended, in-game — ต้องมีคนหน้าจอ **และต้องมีมือคลิก** · จับ `LOCK_GAME` ตามปกติ

**ค้น external แล้ว: เจอ** — `PF_SERIALIZER_FIELDS.tsv` แถว 859-862 (codec ที่ listener ใช้) · `PF_FIELD_VALIDATION` แถว 102-103 (**corpus มีเฟรม `PickupTerrainThing` = 0 เฟรม** — ไม่มีของจริงให้เทียบ) · `FACTPACK_L2_CLASSCENSUS001` แถว 1003 (id `0x4543` เป็นค่า **derive จาก name-hash** ไม่ใช่ค่าที่เคยเห็นบนสาย)
**ค้น gamedata แล้ว: เจอแต่ไม่ใช้เพิ่ม** — `TEXTDATA_TH__MESSAGE.tsv` ผูก `0x1F/0x03/0x22` แล้ว (addendum GT-046 R132) · ใบนี้ไม่แตะข้อความตอบกลับใด (server เราไม่ตอบเลยโดยดีไซน์)

### 🔴 เงื่อนไขปลดบล็อก (ต้องครบ **ทั้งสามข้อ** ก่อนบูต — ขาดข้อเดียว = ใบอยู่ BLOCKED ต่อ)
- ✅ **(ก) ปิดแล้ว (R152 · 2026-08-24 ~18:2x +07:00):** PR #22 (เลน HYP-PF-036) **merge เข้า `main` แล้ว** — merge commit `2c0e3ba` · head `a64d589` เขียว(Actions run 32717828631 · subset · อ่านทาง ci-status · sha ตรงชื่อไฟล์ · conclusion `success`) · `git diff head..merge` ว่าง (tree-identical ⇒ คำตัดสินของ head ใช้กับ `main` ได้) · R152 re-verify สี่ข้อบน `main` ผ่านครบ: flag `app.py:107` · `SCENARIO_PRESENT` (`scenarios/pickup_listener_hypothesis_decode_probe.json` ชื่อตรงกับใบ) · `0x4543` ในซอร์สเลน · เขียว(cloud sanity re-derive บน main clone — ดู rounds/R152) — **ตอนบูตยังต้องเช็คว่า BOOT_COMMIT จาก resolver มีเลนนี้จริง** (บล็อก "ก่อนบูต" ข้างล่าง)
- **(ข)** มี **drop-object ที่วาดจริงและคลิกได้** อยู่ในบูตเดียวกัน — **ตอนนี้ยังไม่มีในบูตใดที่พิสูจน์แล้ว:** ตัว spawn ฝั่ง server ตัวเดียวที่มีคือ GROUND-LOOT-001 (`--ground-loot-hypothesis-scenario`) ซึ่งตัวมันเอง GT-045 = WIRE PASS / CLIENT NO-RESULT (render ยังไม่ยืนยัน · เทสตาเลื่อนไป 2026-08-26) · งาน static GT-046 **ไม่พิสูจน์** ว่า runtime drop-object list ของ client เคยถูก populate ในเซสชันของเรา · 🟡 **อัปเดต 2026-08-24 ~18:3x +07:00 — ครึ่ง composition ปิดแล้ว: Panya เคาะแล้ว** (จดหมาย `notes_to_chief\20260824_1831_PANYA-RULINGS-combine-scenarios-and-open-GT-063.md` §①): **allow-list คู่เดียว `ground-loot-hypothesis + pickup-listener-hypothesis` อยู่ร่วมบูตกันได้** — ไม่ใช่ยกเลิก mutual exclusion · 22 เลนที่เหลือ exclusive เหมือนเดิม · คู่ใหม่ต้องขอ Panya ทีละคู่ · 🔴 **วินัยบังคับเมื่อรวม:** จดหมายผลต้องระบุต่อหนึ่งข้อสังเกตว่าเลนไหนเป็นผู้ทำให้เกิด — แยกไม่ออก = ข้อสังเกตนั้น `NO-RESULT` · โค้ดแก้ด่าน `app.py` ~398-402 ✅ **merge เข้า `main` แล้ว — (ข2) ปิดโดย R154 (2026-08-24 ~19:5x +07:00):** PR #23 (`SCENARIO-COMPOSE-001 + EVENT-EXPORT-001`) → merge commit `cad3e28` · head `99bfa96` เขียว(Actions run 32726495224 · subset · อ่านทาง ci-status · sha ในไฟล์ตรงชื่อไฟล์) · tree ของ head = tree ของ merge commit (diff ว่าง) · เทสพิสูจน์คู่นอก allow-list ยังถูกปฏิเสธอยู่ใน `tests/` ที่ merge แล้ว (rerun บน main: สวีตเต็ม 2222/324 เขียว(cloud sanity R154)) · flag จริง: `--ground-loot-hypothesis-scenario` + `--pickup-listener-hypothesis-scenario` ร่วมบูตได้ · console mode ขึ้น `ground-loot-hypothesis+pickup-listener-hypothesis` ⇒ **(ข) เหลืออย่างเดียว: (ข1) GT-045 เทสตา PASS (นัด 2026-08-26)** — ครบแล้ว chief เติมบล็อก "ท่า spawn drop-object" ในหัวข้อก่อนบูตข้างล่างจากของจริงที่ merge
- **(ค)** ✅ **ปิดแล้ว (R155):** Panya ปลดพักเลน attended แล้ว (2026-08-24 ~21:1x +07:00 · จดหมาย 2120 §① — คำสั่งพัก 16:56 ของ 23 ส.ค. สิ้นสุด)

### objective (claim เดียว)
**id `0x4543` ที่ derive จาก name-hash คือ id จริงของ `PickupTerrainThing` บน wire หรือไม่ — ตัดสินด้วยการจับเฟรม outbound ตัวจริงตัวแรกที่เกิดจากการคลิกซ้ายบน drop-object ที่วาดอยู่จริง**
(ใบนี้วัด "เฟรมอะไรออกจาก client เมื่อคลิก" เท่านั้น — ไม่พิสูจน์ว่าการเก็บสำเร็จ ไม่พิสูจน์ว่าได้ไอเทม)

### คำทำนาย / ตารางอ่านผล 4 กรณี (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว · ท่องก่อนบูต)
- **P1 — คลิกแล้ว server มี record:** id `0x4543` **CONFIRMED** + ได้ไบต์เฟรมจริงชุดแรกของโปรเจกต์ + ได้หลักฐานแรกว่า client ใส่อะไรใน `object_ref_u32` (การเอาไปเทียบกับ `element_key` ที่ spawn = **งานวิเคราะห์ตอนบริโภคผล ไม่ใช่ claim ของใบ**)
- **P2 — คลิกแล้ว server ไม่มี record แต่ raw capture มีเฟรม outbound ที่ nested id เป็นค่าอื่น:** id ที่ derive ไว้ **REFUTED** และ **ได้ id จริงมาแทน** — มีค่าเท่า P1 ทุกประการ (นี่คือเหตุที่ **ต้องเก็บ wire capture เสมอ**: id ที่ไม่ match จะไหลลง frozen v141 dispatch **เงียบสนิท ไม่ตอบ ไม่ error** — ถ้าไม่มี capture เคสนี้จะแยกไม่ออกจาก P3)
- **P3 — คลิกแล้วบน wire ไม่มีอะไรเลย:** เส้นทาง producer ไม่ยิง (in-range gate ของ `0x006B0570`? drop-object list ว่าง?) — **bounded negative** ใช้ได้จริง · จดระยะห่างตอนคลิกให้ละเอียด
- **P4 — ไม่มีวัตถุให้คลิกเลย:** **NO-RESULT** — แยกอะไรไม่ได้สักอย่าง · 🔴 **ห้ามอ่านเป็นผลลบเรื่อง opcode เด็ดขาด** · ใบไม่ปิด กลับไปรอเงื่อนไข (ข)

### 🔴 ก่อนบูต — resolve commit เขียว (ท่าเดียวกับ GT-058/GT-059 · รันเครื่องมือ ไม่ใช่ก๊อป SHA)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` · **exit 3** = ใบนี้รอ gate ไม่ได้รอผู้เทส ห้ามบูต · บรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ จดลงผลเสมอ
- **ยืนยันสี่ข้อกับ `<SHA>` ที่จะบูตจริง (ต้องครบทั้งสี่):**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "pickup-listener-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/pickup_listener_hypothesis_decode_probe.json && echo SCENARIO_PRESENT
git grep -n "0x4543" <SHA> -- src/pirateforce_foundation/
```
1. ไฟล์คำตัดสินมี `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ (success = subset บน Actions ไม่ใช่ gate เต็ม) · 2. เจอ flag จริง (**ห้ามใช้ `--help` เป็นหลักฐาน** — คืน 0 บรรทัดผ่านสะพาน) · 3. เห็น `SCENARIO_PRESENT` · 4. เจอค่า `0x4543` ในซอร์สเลน
- ✅ ชื่อไฟล์ scenario re-verify บน `main` แล้ว (R152 · `git cat-file -e 2c0e3ba:scenarios/pickup_listener_hypothesis_decode_probe.json` = SCENARIO_PRESENT) — ชื่อในใบนี้ถือเป็นจริงได้ · **ห้ามบูตด้วยชื่อเดา**
- 🔴 **ท่า spawn drop-object ตามคำเคาะ (ข):** chief เติมบล็อกนี้หลัง Panya เคาะ (แยก process? ลำดับบูต? เฟรมจากเลนไหน?) — **ใบนี้บูตไม่ได้จนกว่าบล็อกนี้จะถูกเติม**

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-060_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt060.sqlite3
```
- เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง** (canonical ไม่ถูกเปิดตลอดรอบ)
- เลน listener **ไม่เขียน DB โดยดีไซน์** ⇒ เกณฑ์สำเนาใช้แบบ GT-059: **row-diff ทุกตารางต่างได้เฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง** (ไม่ใช้ byte-identical ซึ่งขัดกับ session persist)
- ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกบูต (สำเนา DB ใหม่ทุกครั้ง — เผื่อเวลาเดินไปหาวัตถุ)

### server args (เป๊ะ — opt-in เท่านั้น · `production_allowed=false`)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt060.sqlite3 --pickup-listener-hypothesis-scenario scenarios\pickup_listener_hypothesis_decode_probe.json
```
- **opt-in เท่านั้น ห้าม default-on** (บังคับในโค้ด: ต้องมี `--db` ชี้ไฟล์ที่มีจริง · **mutually exclusive กับ scenario โหมดอื่นทุกโหมด** — รวม `--ground-loot-hypothesis-scenario` ⇒ นี่คือเหตุที่ (ข) ต้องรอคำเคาะ composition)
- หัวหน้าต่าง console ต้องขึ้น mode ของเลนนี้ — ใช้เช็คว่าบูตถูกโหมด
- ⚠️ **ใบนี้ไม่มี chat trigger — ตัวยิงคือเมาส์ซ้ายของคนหน้าจอ** · ตัวอักษรตอนช่องแชตไม่โฟกัส = hotkey ⇒ ระหว่างรอบ **อย่าพิมพ์อะไรเลย** ใช้แค่ `W/A/S/D`, ~~`Q/E`~~, spacebar, เมาส์
  🔴🔴 **แก้ R163 — ใบนี้ยังเปิดอยู่ อ่านข้อนี้ให้จบ:** ~~`Q/E`~~ **ถูกถอดออกจากชุดที่ใช้ได้**
  `Q`/`E` **หันตัวละคร** ⇒ **ยิง `TargetPosVital`** · ใบนี้บูตร่วมสามเลน (`ground-loot + pickup-listener + item-operate-res`)
  และ **เลน ground-loot ยิงที่ `TargetPosVital` เฟรมแรก** ⇒ **เคาะ `Q` หรือ `E` ครั้งเดียว = one-shot ไหม้ก่อนมี drop-object ให้คลิก ⇒ รอบตายทันที**
  ⇒ **ส่องกล้องด้วยคลิกขวาค้างลากเมาส์เท่านั้น** (ไม่หันตัวละคร ⇒ ไม่ยิง) · **จดว่าส่องกี่ครั้ง เวลาไหน**
  ⇒ 🔴 **และรันด่านตัวควบคุมข้อ 3b ของ `GT-035` ก่อน** — กฎคลิกขวาลากยังเป็น "คำให้การ" ไม่ใช่ "การวัด"
- 🆕⭐ **บันทึกสีป้ายชื่อทุกป้ายในเฟรม ตาม PLAYBOOK ข้อ 13** (คำสั่งคุณ Panya 2026-08-25 ~14:2x +07:00)
  ใบนี้ยัง**ไม่มี**บล็อกเต็มแบบข้อ (ช) ของ `GT-035` (งานค้างของ chief รอบหน้า) ⇒ ระหว่างนี้ **ใช้กฎกลางจาก PLAYBOOK ข้อ 13**
  🔴 **ใบนี้เป็นใบที่คุ้มที่สุดสำหรับกฎนี้** เพราะถ้ามี drop-object วาดจริง **นี่จะเป็นครั้งแรกที่มีคนเห็นป้ายชื่อไอเทมค้างนานพอจะถ่ายภาพนิ่งได้**
  ⇒ ถ่าย **full-res** แล้ว commit พร้อม sha256 · ลงทะเบียน `REAL_SERVER_DIVERGENCE.tsv` (`compared_and_matched` ตามจริง)

### steps
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบตามบล็อก db
1. เปิด server ก่อน client เสมอ (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client) — console ขึ้น mode ของเลน listener (🔴 client ที่บูตโดยไม่มี server ตายเองใน ~3.5 นาที)
2. เปิด client (`Invoke-CimMethod Win32_Process Create`) → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
3. เข้าแมพ เห็น HP/minimap/ชื่อแมพ → **เริ่มอัดวิดีโอ/continuous capture ตั้งแต่ตรงนี้ยาวจนจบ** → ทำท่า spawn ตามคำเคาะ (ข) → ยืนยันด้วยตาว่า **มี drop-object วาดอยู่จริง** (โมเดล/ป้ายชื่อ) → ถ่าย **S0** เห็นวัตถุ + X/Y บน HUD · **ถ้าไม่มีวัตถุ = P4 หยุดที่นี่** จด NO-RESULT แล้วข้ามไปข้อ 7
4. **control ระยะไกล (best-effort · ทดสอบ in-range gate ของ GT-046):** จากตำแหน่งไกล (>ระยะที่คาดว่าเก็บได้) เลื่อน cursor ไปบนวัตถุ — จดว่า cursor เปลี่ยนรูปไหม → **คลิกซ้ายหนึ่งครั้ง** → ถ่าย **S1** · คาดว่าไม่มีอะไรบน wire (ถ้ามี = finding จดใหญ่ ๆ)
5. **คลิกหลัก:** เดินเข้าไปประชิดวัตถุ (`W/A/S/D`) → ถ่าย **S2** ระยะใกล้เห็นวัตถุชัด → **คลิกซ้ายบนตัววัตถุ หนึ่งครั้งเดียว** (ห้ามรัวคลิก — หนึ่งคลิกต่อหนึ่งการวัด) → จ้องจอ 10 วิ → ถ่าย **S3** · จด: วัตถุหาย/อยู่ · มีบรรทัดแชตใด ๆ ขึ้นไหม (รวมบรรทัดเขียว `ได้รับ ...`) · ⚠️ server เรา**ไม่ตอบอะไรเลย**โดยดีไซน์ ⇒ ทุกปฏิกิริยาบนจอหลังคลิก = พฤติกรรม client ล้วน จดให้ชัด
6. ถ้าไม่มีบรรทัด listener ใน console: คลิกซ้ำได้อีก 2-3 ครั้ง (เว้นจังหวะ นับจำนวนคลิกให้ตรงกับที่จะไปนับเฟรมใน log) → ถ่าย **S4**
7. จับ NO-CRASH / CRASH: client ยังตอบสนอง (🆕 **แก้ R163: คลิกขวาค้างลากเมาส์แล้วกล้องหมุน** = NO-CRASH — ~~`Q/E`~~ ห้ามใช้เช็ค เพราะมันหันตัวละคร ⇒ ยิง `TargetPosVital`) = NO-CRASH · ออกจากเกม: **X** มุมขวาบน (ตรวจก่อนว่าหน้าต่างแอปตัวเองไม่บัง) → dialog ยืนยัน → ปุ่มซ้าย
8. ปิด server (🔴 server เก็บ session ค้าง — client ตัวถัดไปจะค้าง "connecting" ถ้าไม่ restart) → เก็บ **raw GAME log ทั้งไฟล์** + console out/err → `PRAGMA integrity_check;`
9. **teardown เสมอ** แม้เลิกกลางคันหรือจบที่ P4 (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 — เพดานยกจาก 180 เมื่อ 2026-08-20 · `TEMPLATE_teardown_generic.ps1:135` · แท่นถูกทิ้งข้ามชั่วโมงใช้ `staged\TOOL_stop_stale_server.ps1`)
10. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม

### pass criteria — สองชั้น แยกกันเด็ดขาด
**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ · ทำ headless ได้)**
- **raw GAME log ทั้งไฟล์ = หลักฐานบังคับ ห้ามลบ** — ต้อง diff เฟรม C2S ช่วงเวลาคลิก (เทียบ timestamp วิดีโอ) กับ baseline heartbeat แล้วตอบหนึ่งในสาม: (1) มีเฟรมที่ nested id `0x4543` · (2) มีเฟรม outbound ผิดปกติที่ nested id **เป็นค่าอื่น** — จด id จริง + hexdump เต็ม · (3) ไม่มีเฟรมนอก baseline เลย · 🔴 **การไม่มีบรรทัด listener อย่างเดียวตัดสินอะไรไม่ได้** — id ที่ไม่ match ไหลลง frozen v141 dispatch เงียบ ๆ ⇒ capture คือกรรมการ
- ถ้า listener จับได้: console/log มี **บรรทัด ASCII หนึ่งบรรทัดต่อเฟรมที่รับ** + ค่า `object_ref_u32` · `opaque_u8` · raw body hex ครบ · จำนวนบรรทัดต้องตรงจำนวนคลิก · ถ้าไบต์ผิดรูป: refusal มีชื่อถูกจดแทน — เก็บชื่อ refusal มาด้วย (เป็นผลเหมือนกัน)
- ⚠️ **ตัวนับใน session state (`pickup_listener_accepted_count`/`records`/`refusals`) อาจอ่านไม่ได้ในรัน attended** (บทเรียน GT-045 R127: state ที่ไม่ persist อ่านได้เฉพาะ headless replay) ⇒ หลักฐานชั้นนี้ยึด **log บรรทัด ASCII + raw capture** เป็นหลัก · ถ้าเลนมีท่า dump ให้ใช้ แต่ห้ามนับการอ่าน state ไม่ได้เป็น FAIL
- DB สำเนา: `PRAGMA integrity_check` = `ok` · row-diff ทุกตารางต่างเฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง (`count(*) WHERE selected_character_id IS NOT NULL` — ห้ามนับแถวเปล่า) · จด `max(lease_generation)` ก่อน-หลัง · sha256 canonical ก่อน-หลังตรงกัน
- **ชั้นนี้ตอบไม่ได้:** มีวัตถุบนจอจริงไหม คลิกโดนตัววัตถุจริงไหม ⇒ **ห้ามอ้างชั้นนี้แทนชั้น (2)**

**ชั้น (2) client-observable (ต้องมีคนหน้าจอ)**
- ภาพ **S0..S4** + วิดีโอต่อเนื่องทั้งรอบ · sha256 ทุกไฟล์
- ตอบเป็นภาษาคน: **มี drop-object วาดจริงไหม (โมเดล/ป้ายชื่อ) · cursor เปลี่ยนรูปตอน hover ไหม · คลิกลงบนตัววัตถุกี่ครั้ง เวลาไหน (อ่านจากวิดีโอ) · หลังคลิกมีอะไรบนจอ — วัตถุหาย/อยู่ · บรรทัดแชต/ข้อความระบบใด ๆ (สี/ข้อความเป๊ะ)** · NO-CRASH/CRASH verdict
- **ชั้นนี้ตอบไม่ได้:** เฟรมออกจาก client จริงไหม id อะไร **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

### 🔴 ผลลบมีค่าเท่าผลบวก
- **P2 (id จริงไม่ใช่ `0x4543`)** = ผลที่มีค่า**เท่า P1 เป๊ะ** — เราได้ id จริงมาแทนของ derive · redirect: chief แก้ listener ให้ฟัง id ที่วัดได้ + แก้ FACTPACK แถว 1003 เป็นค่าที่วัดจริง
- **P3 (คลิกแล้ว wire เงียบ)** = bounded negative ที่ใช้ได้ — redirect: แยกต่อว่าเป็น in-range gate (control ข้อ 4 ช่วยตอบ) หรือ runtime drop-object list ว่าง (วัตถุที่เห็นอาจไม่ได้อยู่ใน list ของ `DropThingModule_Client`) — เป็นคำถาม static ใบใหม่ ไม่ใช่การรันซ้ำ
- **P4 (ไม่มีวัตถุให้คลิก)** = **NO-RESULT ไม่ใช่ผลลบ** — ห้ามใครอ้างรอบนี้เป็นหลักฐานเรื่อง opcode ทั้งทางบวกและลบ · ใบไม่ปิด

### เกณฑ์จบ (ใบนี้ปิดเมื่อไร)
- ปิดได้เมื่อบันทึกผลกรณี **P1 / P2 / P3** กรณีใดกรณีหนึ่ง **ครบทั้งสองชั้น** (capture + คำให้การตาคน) — ทั้งสามกรณีคือ PASS ของใบ (ใบนี้วัด ไม่ได้เชียร์ข้างไหน)
- **P4 ไม่ปิดใบ** — สถานะถอยกลับ BLOCKED รอเงื่อนไข (ข) · ห้าม archive ใบตามกฎคิว (ยังไม่ถูกเทส)

### nonclaims (ติดไปกับผลทุกกรณี)
- **ไม่แตะบรรทัดลูทสีเขียว id 131** (`ได้รับ [ $V1 ] * $V2`) — นั่นเป็นเลน `ItemOperateVitalRes` ฝั่ง inbound (GT-049) และเป็นคำถามแยกที่รอ Panya · server เราไม่ตอบอะไรในใบนี้ ⇒ บรรทัดเขียวไม่ควรขึ้นเลย ถ้าขึ้น = finding ใหม่ ไม่ใช่ส่วนของ claim
- **ไม่พิสูจน์ว่าการเก็บของ "สำเร็จ" หรือได้ไอเทมเข้ากระเป๋า** — ใบนี้จับแค่เฟรม request ขาออก
- **ไม่แตะ claim ระบบของวางไว้ล่วงหน้าของ GT-046** (จ็อบ 5 ระบบ ก/ข) — ผลใบนี้อธิบายเฉพาะเลนคลิก `PickupTerrainThing`
- 🔴 **ห้ามอ้างว่าผลนี้อธิบายการเก็บของมอนดรอป** — ครอบครัว `FightingDropModule_Client`/`FightingDropNotify` (ยังไม่ decode) อาจเป็น transport จริงของมอนดรอป (GT-046 จ็อบ 6)
- **การเทียบ `object_ref_u32` กับ `element_key` ที่ spawn = งานวิเคราะห์ตอนบริโภคผล** ไม่ใช่ claim ของใบ — ห้ามเขียนผลราวกับพิสูจน์ mapping แล้ว
- **ไม่ claim ว่าเซิร์ฟเวอร์ต้นฉบับ (ปิดแล้ว กู้ไม่ได้ตลอดกาล) เคยรับ/ตอบเฟรมนี้แบบใด** — listener และการไม่ตอบเป็นดีไซน์ของเราล้วน
- **result:** (ผู้เทสกรอก: กรณีที่ออก P1/P2/P3/P4 · ภาพ S0..S4 + วิดีโอ พร้อม sha256 · จำนวนคลิก+timestamp จากวิดีโอ · path raw GAME log + hexdump เฟรม C2S ช่วงคลิก + nested id ที่วัดได้ · บรรทัด listener/refusal ที่เห็น (ก๊อปมาทั้งบรรทัด) · ค่า `object_ref_u32`/`opaque_u8` ถ้ามี · NO-CRASH/CRASH · เวลา · sha canonical ก่อน-หลัง · row-diff ของ `run_gt060.sqlite3` · `max(lease_generation)` ก่อน-หลัง)

---

## GT-114 DIAG-MULTI-OBJECT-001 [attended, in-game]: five diagnostic objects at the city-center test point (X=11865, Y=6147), each one field away from control D0 -- does each single-field difference produce the on-screen effect that field is predicted to control, jointly closing the attended half of RE-107/RE-108/RE-109's own proposed follow-ups  [CANCELLED - covered by R309 (D0 · RE-108) / refuted by production DYING_TIMER_SECONDS=20 (D1a · ภาพ 185937) / covered by GT-129 (D1b) / D2 control-only / covered by GT-084-R2 + P-2/RE-067 (D3) — Panya agreed 2026-09-04 21:4x · ปิดโดย chief รอบ `epkucn`/R344 2026-09-04 22:56 +07:00 ตาม `COO-DECISION 20260904_2158` (ถอน `2142` ข้อ 2 = ไม่พ่วงบูตกับ `ATTACK-POSE-ONE-FIELD-AB-001`) · กฎ `PANYA-DECISION 20260903_1934` · เหตุผลรายข้ออยู่ใน `notes_to_chief/20260904_2133_KA1A-TO-COO-attack-pose-*` §1 · เดิม: PENDING -- wiring landed R202 (9b6zl6)]

> NUMBERING NOTE: grep confirmed before reserving -- `GT-114`/`RE-114` = 0 hits in both files, archive included (2026-08-27, this round). Highest number in use is `113` (`RE-113`, CLOSED PASS/DONE) => this entry is `114`.
> Entries `RE-085`-`RE-113` and `GT-101`-`GT-110` stay exactly where they are, unchanged -- this is a new entry, not a replacement for any of them.

### source
PANYA-ORDER 18:55+07:00 + ADDENDUM 19:05 (`notes_to_chief/20260827_1855_PANYA-ORDER-diag-multi-object-boot-one-round-answers-RE107-108-109.md`) asked for one boot, five objects, each one field from a shared control D0, byte-diff-proven before any human round. LANE-B built the composition layer that round: `src/pirateforce_foundation/mob_diag_multi_object.py` (`tests/test_mob_diag_multi_object.py` all green). Builds the five `DiagObject` records, prints `describe_boot()`; sends nothing, not called from `runtime.py` yet. RE-107/108/109 are each CLOSED BOUNDED-NEGATIVE/DONE, each proposing this kind of narrow attended capture as its own next step -- this entry is that follow-up.

**CORRECTED, LANE-B round following PANYA-DECISION 2026-08-27T20:10+07:00 "M1-P" item 3**: the body is Mountain Deer, MOBS n_ID 27 (per that same letter's ADDENDUM 20:18), NOT Jungle Big Tiger (template 60), which this entry originally named -- see nonclaim (10) below for the full swap history. `mob_diag_multi_object.DIAG_BODY_TEMPLATE_ID` is now `27`; its stats are hand-mined from `CONSTDATA_TH__MOBS`/`MOBS_TIP`/`STANDARD_MOB` directly (Mountain Deer is not a member of either bg0001's or the newly-mined Bg0002's generated roster -- its `s_OUTFIT` is a two-variant list that fails the mining tool's outfit-unambiguous selection rule). `mob_death.WIDENING_RULINGS` carries a new, dedicated entry for template 27, scoped to scene "bg0001" (where these five objects are actually placed, not Bg0002). Still `BLOCKED-ON-WIRING` -- this round corrects which monster the ticket names, it does not unblock it.

### objective
One boot, five position-distinguished objects, each one field from D0, five independent readings in one sitting:
- D0: does a left-click open the target panel, does Tab (RE-108)
- D1a: does the corpse fall/animate once DEAD is held back 20s instead of 700ms, or freeze like production (RE-107 "DEAD too fast" branch)
- D1b: does a dead-only frame (no DYING), sent only after a prior TargetVital for that identity, fall/animate or freeze (RE-107 "model-loaded bit" branch)
- D2: a second on-screen D0 at another position -- a repeat-control reference point, NOT a new value (nonclaim 4)
- D3: a body without the hostile faction splice (plain-town-NPC shape, same template/HP/name) -- clickable/hittable at all? what name colour?
A reading on one object never substitutes for another (nonclaim 3).

### db
default_state\pirateforce.sqlite3 -- copy only, canonical never opened. Copy to `pf_bridge\backup\pirateforce_before_GT-114_<yyyyMMdd_HHmmss>.sqlite3`, then `state\run_gt114.sqlite3`. sha256 vs `CANON_SHA.txt` before/after; `PRAGMA integrity_check=ok` on the working copy both times.

### server args
WIRED R202 (9b6zl6). No new server CLI flag -- the diagnostic is gated by an on-disk
allowlist, not a `--scenario` argument: create `config/diag_multi_object.json` (or set
`PF_DIAG_MULTI_OBJECT_CONFIG` to point elsewhere) with `{"diag_multi_object_accounts":
["<the attended test account name, exact case>"]}` on the machine that boots this
ticket, BEFORE boot. No file / account not listed = zero behaviour change (pinned by
`tests/test_diag_multi_object_runtime_wiring.py`, run through the real dispatcher, not
just the composer). Boot with no other flag; log in with the listed account; reaching
the bg0001 arrival census (first TargetPos after the runtime ack) prints exactly 5
`DIAG object=<D#> variant=<...> identity=0x<...> pos=(<x>,<y>,<z>)` lines, one per
object in D0/D1a/D1b/D2/D3 order, plus one `DIAG_CENSUS assembled=5 census=115 wire=120
...` line. `world_census_actor_count` stays 115 -- the +5 lives in the frame bytes, not
the census count that gates later recomposes (see `diag_multi_object_wiring.
census_frames()`'s own docstring for why an inflated count there would break every
later hit). D0/D1a/D1b/D2 resolve as combat targets immediately; D3 does too but is not
expected to reach 0 HP this round.

### steps (fill in once server args above holds a real command line)
1. LOCK_GAME; confirm exactly 5 `DIAG object=...` console lines before opening the client -- otherwise BLOCKED, do not boot.
2. Boot, log in, reach (X=11865, Y=6147); record HUD X/Y.
3. NO-CRASH: right-click-drag camera 360 degrees only (never WASD/Q/E -- those move the character and emit TargetPosVital).
4. Per object: visible immediately or late (model-load lag, free data).
5. D0: photo (name colour), click once, photo, Tab, photo; attack to 0 HP, photo death + result.
6. D1a: attack to 0 HP, wait a full 25s, photo result.
7. D1b: click once (emits TargetVital), then attack to 0 HP, photo result.
8. D2: photo name colour before click / after click / after death.
9. D3: photo name colour; try one click and one attack; record if either registers.
10. NO-CRASH again; log out; teardown via `TEMPLATE_teardown_generic.ps1` (stamp under 420 min); recheck canonical sha256; sha256 every capture.

Colour rule (per Panya's order 2026-08-25): one line per label per image, write "none" not blank, full-res stills only (never a contact sheet/video), never infer a cause -- RE-067 is open and is the only place that question lives.

### pass criteria (two layers)
wire/DB: (a) exactly 5 `DIAG object=...` lines matching `describe_boot()`; (b) the module's own pre-human byte-diff (signed off per pf-adversary, run before this ticket is ever booted) shows D1a/D2/D3 differ from D0 only in the one named field, D1a/D1b death frames differ only in schedule timing; (c)/(d) canonical sha256 + integrity_check ok before/after.
client-observable: five separate readings, none substituting for another -- D0 panel/click/Tab + name colour; D1a fall/freeze after 20s hold (either is a finding, not a failure); D1b fall/freeze on dead-only-after-TargetVital; D2 name colour before/after click/death; D3 name colour + does click/attack register at all. All colours per the colour rule.

### nonclaims
(1) WAS blocked pending chief wiring `GT_DIAG_MULTI_OBJECT_WIRING`; landed R202 (9b6zl6), see server args above -- kept as history, not deleted, per queue rule. (2) Does not itself produce the required pre-human byte-diff proof. (3) Bundles five readings into one boot on the owner's own instruction; each stays independently reported. (4) D2 here is a byte-identical repeat of D0, NOT the GT-032 alternate-faction-value object the original order's table named -- that needs a value with provenance RE has not produced yet. (5) Does not test the player's own orange name (ADDENDUM 19:05 excludes it). (6) Does not decide the cause of any colour observed -- RE-067 only. (7) City-center placement is diagnostic only, not a real field-placement claim. (8) D1b's gate is only as good as whatever session state the eventual wiring actually tracks -- if it tracks nothing, the wiring reply must say so. (9) `DIAG_CENTER_Z` (2231.17) is a nearest-neighbour estimate from `population.py`'s own census (~931 units away), not a terrain query at this exact point -- objects rendering mid-air/underground is itself a result to record, not a reason to abort silently. (10) ~~DOUBLY BLOCKED as of ADDENDUM 20:18 (+07:00, same day, landed after this ticket was drafted): the owner named Mountain Deer (MOBS n_ID 27) as the body for all five objects, superseding this round's Jungle Big Tiger (template 60) pick -- Mountain Deer needs a fresh mine (not in bg0001's roster) and a new `mob_death.WIDENING_RULINGS` entry (template 27 not covered by the existing bg0001 ruling). Next LANE-B round's work; do not boot this ticket against the current module without that swap landing first.~~ DONE, the LANE-B round after this one (PANYA-DECISION 2026-08-27T20:10+07:00 "M1-P" item 3): Mountain Deer's row is hand-mined (it is not a member of ANY generated roster, bg0001's or the newly-mined Bg0002's -- both mining runs exclude template 27 on the same outfit-ambiguity ground) and `mob_death.WIDENING_RULINGS` carries a dedicated entry for template 27. Still BLOCKED-ON-WIRING for the unrelated reason nonclaim (1) already names. (11) THE SWAP TRADES AWAY PART OF ADDENDUM 19:05's ORIGINAL JUSTIFICATION FOR AN AGGRO MONSTER: Mountain Deer's own `n_AI_WANDER` (16) maps to `n_AGGRO` 0 in `field_mob_ai_tables.AI_WANDER_ROWS` -- it is NOT an aggro monster, unlike the Jungle Big Tiger pick it replaced (`n_AI_WANDER` 11, `n_AGGRO` 1200). It still grants EXP (`f_RATIO_EXP` 1.0, same contrast this ticket's original criterion used). The owner's later, more specific ADDENDUM 20:18 instruction is followed as given rather than re-argued; this is recorded so a reader of "unmistakably born as a monster" (ADDENDUM 19:05's own phrase) knows which half of that phrase the final body actually satisfies. (12) NEW R202: D1b (step 7 above) has NO death handling this round -- nothing in this codebase tracks "has this client already been sent a TargetVital for this identity", so `dead_only_schedule`'s refusal is never bypassed with a guessed `target_vital_seen=True` (see `diag_multi_object_wiring.D1B_UNWIRED_REASON`). Step 7 will still show a result (photo it as instructed) but expect NO dying/dead frames from the server for D1b specifically -- the client's own local reaction (if any) to a target reaching 0 HP with no server death frames IS itself the reading this object was built to produce, not a wiring bug to report. A follow-up CORE-REQUEST (a per-session set of TargetVital'd identities) would be needed to answer D1b's original question with a real "yes it was sent" rather than this negative result.

### result
(tester fills this in)


---

## GT-107-R3 GM-001-R3 LOGIN-STATE-VISUAL-PROBE-003: after RE-113 (trailing change-mask byte) + CORE-REQUEST-020 (field_0x0b_second=1) both landed on main, does a real client now accept GM_UpdateGMStateVital cleanly, and does BT_GM actually appear  [RESULT -- outcome (a)/(b)/(c) ไม่ตรงเป๊ะสักข้อ, ดูผลด้านล่าง]

> 🔴 **หมายเหตุการอ้างชื่อรอบ (round `y2nhzz`):** ผลที่เข้ามาจริงถูกส่งในจดหมายชื่อ
> `notes_to_chief/20260828_0215_GT101R3-RESULT-*.md` (ผู้เทสอ้างเป็น "GT-101-R3" ไม่ใช่ "GT-107-R3") แต่
> ทุกรายละเอียด (account `localtest`, RE-113 + CORE-REQUEST-020, hex tail prediction, ขอบเขต "Port Royal
> เท่านั้น ไม่รวม GT-110") ตรงกับใบนี้ (`GT-107-R3`) เป๊ะทุกจุด ไม่ใช่ GT-101 เดิม (ซึ่งผลของมันคือ R1's
> negative จาก error 23065, อยู่ที่เดิมด้านล่าง ไม่ถูกแตะ) — ใบนี้บันทึกผลไว้ที่ `GT-107-R3` ตามที่ entry
> นี้นิยามไว้เอง ไม่ย้ายไป `GT-101`

> เลขใบ: reuses GT-107's number with `-R3` (house precedent: `GT-030-R3`), not a fresh draw from the
> shared counter -- grep confirmed 2026-08-28: `GT-107-R3` = 0 hits repo-wide including `archive/`.
> Highest bare number in the shared counter stays `114` (`GT-114`), unaffected. Opened by LANE-GM round
> `3a0tly` per `notes_to_chief/20260827_2305_KA1A-NUDGE-idle-lanes-GM-R3-byte-proof-A-map-window-RE-chief-DIAG-wiring.md`.
> GT-107's own header corrected same round from stale `[PENDING]` to its real negative result.

### source (links only -- see cited files for full detail, not re-derived here)
- RE-113 (round `fmgvbx`, CLOSED PASS/DONE): fixed GT-107's error 28317 -- `gm/state_wire.py` now calls
  `legacy.make_runtime_vitals()` (plural), which appends the trailing change-mask byte the singular helper
  omitted. `archive/rounds_2026-08-27_to_28/GM_20260827_1948_re113-trailing-mask-fix-core-request-020-mailbox.md`.
- CORE-REQUEST-020 (confirmed on main): `field_0x0b_second` 0->1 at the real call site, per RE-089/RE-104's
  proof that wire `+0x15==1` gates `BT_GM` visibility. `notes_to_chief/20260827_2014_CHIEF-REPLY-CORE-REQUEST-020-bt-gm-field-wired.md`.
- Headless proof, driven through the real dispatcher:
  `tests/test_gm_login_state_guard.py::GmLoginStateGuardTests::test_the_re113_plus_core_request_020_frame_matches_a_literal_hex_tail`
  asserts the frame tail equals `12 19 5A 0B 00 0B 00 0B 01 14 00 00 00 00 0B 00` byte-for-byte. 235/235
  green (LANE-GM round `3a0tly`).
- Account: reuses GT-107's own ด่าน 0 resolution (`localtest`), not reopened here --
  `notes_to_chief/20260827_1745_GT107-RESULT-NEGATIVE-*.md`.
- 🔴 **Never fired at a real client.** GT-107 already proved headless-correct is not sufficient (it hit
  28317 despite RE-105's version-0 fix passing). This entry is the only remaining way to learn if this
  combination reaches a real client cleanly.

### 🔴 scope
Login-state frame + `BT_GM` visibility at Port Royal (scene 1) ONLY. **Do NOT combine with `GT-110`**
(login-scene override to Bg0002) in the same session -- two variables in one sitting can't be attributed.
Run `GT-110` as its own later session if wanted.

### procedure -- unchanged from GT-107, follow that entry's ด่าน 0/1/2, db backup, and server-args blocks
verbatim (same repo state gates, same `localtest` config-copy pattern, same green-boot resolver). ด่าน 2
delta to grep on top of GT-107's own list: add
`git grep -n "make_runtime_vitals" <SHA> -- src/pirateforce_foundation/gm/state_wire.py` and
`git grep -n "test_the_re113_plus_core_request_020_frame_matches_a_literal_hex_tail" <SHA> -- tests/test_gm_login_state_guard.py`
-- both must return a line, or **BLOCKED**.

### steps -- delta from GT-107 only
Steps 1-2 (boot, login) identical to GT-107. **Step 3 is new:** watch 10s after load clears for the old
modal (23065) or the new one (28317) -- either recurring means stop here and write a RESULT like
GT-101/GT-107, not a failure of this entry. No modal -> continue as GT-107's steps 4/6/7/8 (HUD check,
NO-CRASH camera drag, console watch, teardown), **plus** a new step 5: search the notification/system UI
for `BT_GM` (up to 3 min), and if found, click through to panel `GMUI_BASIC` (`Radiobutton_Message` +
`TextBox_Message`, Enter sends `0x51E9` per RE-091) -- photograph before/after.

🔮 predicted tail bytes (unproven, a wrong prediction is a finding not a failure): GT-107 measured
`... 12 19 5A 0B 00 0B 00 0B 00 14 00 00 00 00`; this round predicts `0B 00`->`0B 01` (second field) plus
one new trailing `0B 00` (RE-113's byte): `... 12 19 5A 0B 00 0B 00 0B 01 14 00 00 00 00 0B 00`.

### pass criteria (two layers, never mixed)
wire/DB: `[G>] GM_UPDATE_STATE_AFTER_LOGIN (N bytes)` once, no `gm_account_lookup_failed_*`, no
`[G!] game socket closed/reset` within 60s of T0 (GT-107's own failure signature). Hex dump (if console
shows one) matches the 🔮 prediction. DB/sha256 checks same as GT-107.

client-observable (human only, never inferred from console) -- three non-ranked outcomes, each a complete
result:
  (a) strong positive: no modal AND `BT_GM` found + clickable through to `GMUI_BASIC` without error.
  (b) real negative, not a failure: no modal, login fine, button still not found after a reasonable search
      -- list everywhere checked.
  (c) modal recurs (23065, 28317, or other): write up as a RESULT like GT-101/GT-107, stop.
Name-label colours: one line per label per full-res still ("none" if none), same colour rule as every
other entry (RE-067 stays open, no cause inferred).

### nonclaims
Does not test GM commands (`0x51E9` payload, GT-103's scope) or the login-scene override (`GT-110`, see
scope above). Only tests account `localtest`. No reconnect/relogin. Does not assign semantics to the three
opaque state fields beyond the proven `+0x15==1` gate value (RE-089's ban on offset/width inference stays
in force). Headless 235/235 is cited evidence, not reproduced by the human tester. If ด่าน 0/1/2 don't
clear, the whole entry is BLOCKED, not NO-RESULT/FAIL.

### result

**RESULT 2026-08-28T02:15+07:00, owner-observed** (เต็มใบ:
`notes_to_chief/20260828_0215_GT101R3-RESULT-GM-frame-accepted-BT_GM-button-visible-click-does-nothing-no-packet.md`,
วิดีโอ+ภาพ+คอนโซล cite ในนั้น):

wire/DB: PASS เต็ม — เฟรม 41 ไบต์ ท้ายตรง 🔮 prediction เป๊ะไบต์ต่อไบต์:
`12 19 5A 0B 00 0B 00 0B 01 14 00 00 00 00 0B 00` ไม่มี `gm_account_lookup_failed_*` ไม่มี socket
reset/close ที่ไม่ใช่เจ้าของออกเอง ทั้ง 23065 (`GT-101`) และ 28317 (`GT-107`) ไม่เกิดซ้ำเลย

client-observable: **ไม่ตรงกับ (a)/(b)/(c) ที่ตั้งไว้สักข้อ — ผลลัพธ์ที่สี่ที่ใบนี้ไม่ได้เผื่อไว้**: ไม่มี
modal (ตัด (c) ออก) + พบปุ่ม `BT_GM` จริงที่แถบระบบล่าง (ตัด (b) ออก, ไม่ใช่ "หาไม่เจอ") **แต่คลิก 2 ครั้ง
ไม่มีอะไรเกิดขึ้นเลย ไม่ถึง `GMUI_BASIC`** (ไม่ครบเงื่อนไข (a) ที่ต้อง "clickable through to GMUI_BASIC
without error") — คอนโซลไม่เห็นเฟรมขาเข้าใหม่ระหว่างคลิกด้วย (ไม่ใช่แค่ UI ไม่วาด แต่ client ไม่ส่งอะไรออก
สายเลย)

**ต่อ:** เปิด `RE-118` (`CLIENT_RE_QUEUE.md`) สืบจาก `RE-104` หา gate ที่ทำให้คลิกเงียบ — `GT-103` และ
outcome (a) ของใบนี้ยังไม่ปิดจนกว่า `RE-118` จะตอบหรือชี้ทางสำรวจ

**อัปเดต 2026-08-28T04:1x+07:00 (LANE-GM รอบ `4djeqi`):** `RE-118` CLOSED PASS/DONE
(`notes_to_chief/20260828_0411_RE-118-RESULT-CURRENT-UI-KEY-MUST-BE-NONEMPTY.md`) — static พิสูจน์แล้วว่า
คลิกเงียบเพราะ dispatcher ต้องการ current-UI-key ไม่ว่าง (ไม่ใช่ field ใหม่บนเฟรม `0x5A19`) ไม่ใช่ระดับ gate
ของปุ่มเอง static ไม่สามารถชี้ค่ารันไทม์จริงได้ (ไม่มี capture ว่า key ว่างจริงตอน `GT-107-R3`) — ต้องทำ
attended A/B ต่อ (เพิ่มไว้ที่ `GT-103` step 2 แล้ว: คลิกจาก HUD เปล่า vs. คลิกหลังเปิด panel ที่รู้ว่ามี
current-UI key ไม่ว่าง) จึงจะปิด outcome (a) นี้ได้จริง ใบนี้เองยังไม่เปลี่ยนสถานะ RESULT เดิม (ผลลบเดิมยังคง
ถูกต้อง เป็นเพียงคำอธิบายกลไก ไม่ใช่ผลใหม่บนจอ)

nonclaim: ไม่ระบุสาเหตุที่คลิกไม่ทำงาน (ขอบเขตของ `RE-118`) · ไม่สำรวจอะไรบนจอนอกปุ่ม `BT_GM` (เจ้าของไม่ได้
สำรวจต่อ) · ไม่ claim ว่า `GM_UpdateGMStateVital` ทำอย่างอื่นบนจอนอกจากทำให้ปุ่มนี้โผล่

nonclaim ของย่อหน้า "อัปเดต" ด้านบน (รอบ `4djeqi`, แยกจาก nonclaim เดิมของผล 2026-08-28T02:15 ที่ไม่ถูกแก้):
headless-only, ไม่มีเฟรมยิงเข้าไคลเอนต์จริงในรอบนี้เอง

---


## GT-128 GM-003 CHAT-WARP-VISIBLE-001 [attended, in-game]: GM พิมพ์ `/warp <ฉากปัจจุบัน> <x> <y>` ลงกล่องแชทธรรมดา แล้ว**ตัวละครขยับไปยังพิกัดนั้นบนจอจริงหรือไม่** -- ใบแรกของสาย GM ที่ตัดสินที่จอ ไม่ใช่ที่ log  [❌ **CANCELLED - refuted by R306 finding 3 (`notes_to_chief/20260903_1655_*`)** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2) — รูป same-scene ที่มีพิกัดส่ง `LANE_GM_CHAT_WARP_TELEPORT_FORCE_POS` แล้ว **ไคลเอนต์ปิดตัวเอง** (`ErrorData=28317`) วัดบนจอเจ้าของ ⇒ คำถามของใบนี้ ("ตัวละครขยับไปพิกัดนั้นไหม") ตอบไม่ได้ด้วยรูปเฟรมที่มีอยู่ และ `COO-DECISION 20260903_1744` ข้อ 3 สั่งปิด `/warp` แบบมีพิกัดไปแล้ว · 🔴 **เปิดใบใหม่ (ไม่ใช่ปลดใบนี้) เมื่อ LANE-GM เปลี่ยนรูปเฟรมและมี headless proof** — ใบใหม่ต้องเขียนเกณฑ์บนรูปเฟรมใหม่ ไม่ใช่ยกด่านเก่าทั้งชุดมาใช้ · สถานะเดิม: ~~BLOCKED — token compares nothing (COO-DECISION 20260829_0041)~~ **STILL BLOCKED — token fixed, but a separate COO-held gate remains (see chief R243 update at end)**: ห้ามเกรด ห้ามบันทึกผลใด ๆ ด้วยโทเคน `GM_WARP_POSITION_CONFIRMED` ตัวปัจจุบัน เพราะมันเทียบแค่ "แถวเปลี่ยนค่า" ไม่ได้เทียบกับ**จุดที่สั่ง** · ปลดเมื่อชุดแก้โทเคน+audit ลง main (chief, ภายใน 2026-08-29 23:59+07:00) · **อัปเดตรอบ `nz0qt2`:** ครึ่ง audit ที่เป็นเขต LANE-GM (แถว `outcome`, `CORE-REQUEST-GM-032` ข้อ 1-2) อยู่ใน PR `pirate-force-server#223` **รอ merge** · ครึ่งโทเคน (`GM_WARP_POSITION_TARGET_MATCH/MISMATCH`, `CORE-REQUEST-GM-031`) และข้อ 3 ของ GM-032 ยังเป็นของ chief ⇒ ป้าย BLOCKED ของใบนี้ **ยังไม่ถูกปลด** ด้วยรอบนี้ · 🔴 **เหตุผลที่วัดแล้ว ไม่ใช่แค่เหตุผลเชิงหลักการ** (เพิ่มโดย LANE-GM เจ้าของใบ รอบ `xk4wmz`): pf-adversary วัดว่าโทเคนตัวปัจจุบัน **ยิงตอนผู้เล่นเดินเองหนึ่งก้าว**หลัง warp ที่ไคลเอนต์เมิน ⇒ ใบนี้ "ผ่าน" ได้โดยที่ warp ไม่ทำงานเลย · **ของที่ LANE-GM ทำเสร็จแล้วเพื่อชุดของ chief:** `gm/warp_target_record.py` เก็บปลายทางของ warp ใบนั้นไว้เทียบได้ หยิบได้ครั้งเดียว ผูกกับ `character.id` (รอบ `z6gu2n` บน main แล้ว) และ `CORE-REQUEST-GM-031` ขอให้ chief พิมพ์ `GM_WARP_POSITION_TARGET_MATCH` / `..._MISMATCH` **เพิ่ม** จากโทเคนเดิม (ห้ามเอา match มาเป็นเงื่อนไขของโทเคนเดิม -- วันนี้ client เมิน `ForcePos` ผลที่คาดคือ MISMATCH ถ้ารวมกันโทเคนจะหายทั้งใบ) · BLOCKED x4 รวมข้อนี้ (~~x3~~ ~~x2~~ นับผิดมาแต่แรก มีสามข้อมาตลอด) -- ห้ามบูต: (ก) `CORE-REQUEST-GM-029` ยังไม่ลง main (จุดเรียกที่คืน action ที่สาขา `0xAC52`) · **อัปเดตรอบ `vvxkft`:** ตัวโมดูล `gm/chat_command_action.py` เองก็เพิ่งกลับขึ้น main รอบนี้ (PR #204 -- PR #200 ของรอบ `gr2q9j` ถูกปิดเพราะ gate แดง ไม่เคย merge) และ GM-029 เปลี่ยนความหมายเป็น "**แทนที่**บรรทัด `fire()` ของ GM-028 ในคอมมิตเดียว" ไม่ใช่ "เพิ่มจุดเรียก" (ใบ `20260828_1930_LANE-GM-CORE-REQUEST-GM-029-v2-replace-not-add.md`) ⇒ วันที่ใบนี้บูตได้ `GT-127` จะใช้ไม่ได้ตามเกณฑ์เดิมอีกต่อไป เพราะ event เปลี่ยนเป็น `gm_chat_action_*` -- **บูต `GT-127` ให้จบก่อน** (ข) ~~`RE-129` ยังไม่ตอบ~~ **RE-129 ตอบแล้ว 2026-08-28T20:09+07:00 (`ForcePos vital_version = 0`) แต่ข้อนี้ยังบล็อกอยู่ด้วยเหตุใหม่:** `COO-DECISION 20260828_2130` ล็อกแข็งว่าห้ามเปลี่ยน `FORCE_POS_VITAL_VERSION_CONFIRMED` จาก `None` จนกว่าจุดเขียนตำแหน่งแบบยืนยันจะอยู่บน main (`CORE-REQUEST-GM-030`, รอบ `fo2lgh`) **แม้ RE-129 จะตอบก่อนก็ตาม** ⇒ โมดูลยังปฏิเสธการส่งด้วยตัวเอง และตอนนี้มีเทสบังคับด้วย (`pirate-force-server/tests/test_gm_force_pos_version_lock.py` แดงถ้าเปลี่ยนค่าก่อนโทเคน `GM_WARP_POSITION_CONFIRMED` อยู่บน main) · เหตุผลชั้นที่สองจาก RE-129 เอง: handler ที่ client จดทะเบียนไว้สำหรับ `ForcePos` = `mov al,1; ret 4` ไม่อ่าน payload ⇒ **version ถูกไม่ได้แปลว่าจะขยับ** ใบนี้ยังเป็นใบเดียวที่ตัดสินข้อนั้นได้ (ค) ~~🔴 **คำถาม "ใครเป็นเจ้าของตำแหน่งหลัง warp" ยังไม่มีคำตอบ**~~ **ตอบแล้ว 2026-08-28T21:30+07:00 (`COO-DECISION`): เจ้าของคือตำแหน่งที่ client ยืนยันแล้ว · เซิร์ฟเวอร์ห้ามเขียนตำแหน่งที่ตัวเองไม่ได้สังเกตเห็น · ตัวยืนยันคือ `TargetPos` ใบแรกหลังเฟรม** ⇒ ข้อนี้เหลือ "รอการเดินสาย" ไม่ใช่ "รอคำตอบ" -- ปลดเมื่อ `CORE-REQUEST-GM-030` ลง main และ COO ปลดล็อก · ผู้เทสต้องบันทึกในผล: หลัง warp ให้เดินหนึ่งก้าวเพื่อบังคับ `TargetPos` แล้วดูว่าคอนโซลมี `GM_WARP_POSITION_CONFIRMED` หรือไม่ · **บริบทเดิมของข้อนี้ (เก็บไว้):** — pf-adversary รอบ `gr2q9j` ชี้ว่า หลังส่ง `ForcePos` แล้ว แถวใน DB และ `selected.position` ยัง**ค้างที่จุดเดิม** (โมดูลไม่เรียก `foundation.checkpoint`) ⇒ client อยู่จุดใหม่ เซิร์ฟเวอร์คิดว่าอยู่จุดเก่า · aggro/pickup/logout ใช้จุดผิด · ต้องได้คำตอบ (`ASK-COO` รอบนี้) **ก่อน**เปลี่ยนค่าคงที่ของ `RE-129` ไม่ใช่หลัง · **อัปเดตรอบ `38c4tv` 2026-08-29T08:22+07:00 (LANE-GM เจ้าของใบ) — เพิ่มด่านก่อนบูตข้อ 4 ไม่ได้ปลดหรือเพิ่มบล็อก:** จดหมาย chief `20260829_0604` ข้อ ②bis (ก) วัดได้ว่าล็อกอินที่ใช้ override ฉากเป็น **visit** ⇒ ไม่เขียนแถวตำแหน่ง ⇒ `GM_WARP_POSITION_CONFIRMED` **ไม่มีทางยิง** บนเซสชันนั้น · ใบนี้ตัดสินด้วยโทเคนนั้น จึงต้องยืนยันก่อนบูตว่าบัญชีไม่มีใบล็อกอินค้าง ทั้ง `gm_login_scene.json` และ `gm_login_scene_standalone.json` (ดูด่านข้อ 4) 🔴 กับดักซ้อน: ขั้นตอนข้อ 4 ของใบนี้เอง (`/warp <ฉากอื่น>`) เป็นตัวสตางค์ใบนั้น · **อัปเดต chief รอบ `3ru85y` (R243) 2026-08-30T~16:xx+07:00 — CORE-REQUEST-GM-030/031 wired, แต่ตัวบล็อกจริงของใบนี้ยังปิดอยู่:** `GM_WARP_POSITION_TARGET_MATCH`/`_MISMATCH` พิมพ์แล้วจริง เพิ่มจากโทเคนเดิม ไม่แทนที่ (พิสูจน์ headless: warp ตรงพิกัด -> MATCH หนึ่งบรรทัด, warp ผิดพิกัด -> MISMATCH พร้อมระยะ, เดินเองไม่มี warp -> ไม่มีทั้งคู่, target ค้างข้ามเฟรมไม่เกิด — เทสใหม่ 5 ใบใน `tests/test_gm_warp_position_confirmed.py`, สวีตเต็ม 5480 passed) · 🔴 **pf-adversary พบ**: กิ่ง `unknown_character_mismatch` ที่ `CORE-REQUEST-GM-031` ข้อ 5 ขอ เป็น **dead code ในโปรดักชัน** — ลำดับการ์ดเดิม (`character_changed` early-return) ดักทุกกรณี re-select จริงไว้ก่อนกิ่งใหม่จะถึง เทสที่พิสูจน์กิ่งนี้ต้อง park เป้าหมายตรงผ่าน `record_warp_target` เอง ไม่ใช่ผ่านเส้นทาง `/warp` จริง — [ไม่อ้าง] ว่ากิ่งนี้ทำงานได้จริงในโปรดักชัน คงไว้เป็น defense-in-depth ตามที่คอมเมนต์ใหม่ใน `runtime.py:_gm_warp_open_confirm_window` บันทึกไว้ ส่งคำถามลำดับการ์ดนี้ต่อให้ LANE-GM/COO ตัดสินว่าจะแก้หรือรับสภาพ (ดูจดหมาย `CHIEF-REPLY` รอบนี้) · pf-adversary ยังพบบั๊กเดิมที่ไม่เกี่ยวกับ diff นี้ (rearm เป็นตัวละครอื่นก่อนมี TargetPos ทำให้ `gm_warp_pending_character` ค้างชื่อเก่า แล้วโทเคนทั้งชุดเงียบทั้งเฟรมของตัวละครใหม่) — ไม่แก้รอบนี้ (นอกขอบเขตใบ) รายงานไว้ให้ทราบ · ~~🔴🔴 **ตัวบล็อกจริงของใบนี้ทั้งใบยังไม่ปลด**: `teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED` ยังเป็น `None`~~ **อัปเดต chief รอบ `9fv1m8` (R253) 2026-08-31T~02:1x+07:00: ค่าคงที่ปลดแล้ว** (`teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED = 0`, ตาม `COO-DECISION 20260830_1645`/`1742` -- ค่า RE-129 literal ไม่ใช่การอ่านชื่อ `*_PROVEN_BY_RE129`) พร้อมแก้เทส 13 ใบใน 6 ไฟล์ที่พึ่งค่า shipped เดิมโดยไม่ patch ตรง ๆ (pf-adversary รีวิวผ่านก่อน commit) สวีตเต็ม 5600 passed 0 failed เขียว(cloud sanity) · **รอ merge ก่อน** -- `pirate-force-server` PR ของรอบ `9fv1m8` ยังไม่ merge เช็ค `PR_STATE.txt` ก่อนบูต · ไบต์ `ForcePos` จะออกสายจริงเมื่อ merge แล้วเท่านั้น · ตัวบล็อกที่เหลือของใบนี้ (ลำดับการ์ด `unknown_character_mismatch` dead-code ที่ pf-adversary พบรอบ `3ru85y`, และ rearm-character bug ที่ยังไม่แก้) **ยังไม่ปลด** -- นี่คือแค่การเปิดสายไบต์ ไม่ใช่การปิดใบ ผู้เทสยังต้อง ยันหน้าจอจริงตามด่านเดิมของใบนี้]

> เลขใบ: ตัวนับเดียวร่วมกับ `CLIENT_RE_QUEUE.md` · รอบ `gr2q9j` จอง `RE-129` ที่นั่นและ `GT-128` ที่นี่
> grep ยืนยันก่อนจอง 2026-08-28T18:2x: `GT-128` / `RE-129` = 0 hit ทั้งสองไฟล์ · สูงสุดก่อนหน้า = `GT-127` / `RE-128`

### ต่างจาก GT-127 อย่างไร (สองใบนี้ไม่ซ้ำกัน อย่ารวม)
`GT-127` ตัดสินที่ **ndjson audit log** = "เซิร์ฟเวอร์อ่านบรรทัดที่ GM พิมพ์ได้ไหม" (ครึ่งอ่าน)
`GT-128` ตัดสินที่ **จอ** = "แล้วมีอะไรเกิดขึ้นกับตัวละครไหม" (ครึ่งส่ง) · จุดเรียกเดียวกันปลดทั้งสองใบ
แต่ `GT-128` ต้องรอ `RE-129` เพิ่มอีกใบ ⇒ `GT-127` จะบูตได้ก่อนเสมอ

### ด่านก่อนบูต (~~ทั้งสาม~~ **ทั้งสี่** ต้องผ่าน มิฉะนั้นเลื่อน ห้ามบูต)
> นับผิดมาหนึ่งรอบ: ข้อ 4 เพิ่มโดยรอบ `38c4tv` แต่หัวข้อยังเขียนว่าสาม — pf-adversary จับได้
> ก่อน push · ผู้เทสที่อ่านหัวข้อแล้วนับถึงสามจะไม่เคยรันข้อ 4 เลย
1. grep บน `main` เจอจุดเรียก `make_gm_chat_command_action` จริงที่สาขา `0xAC52` ของ `runtime.py`
   (ไม่ใช่แค่ PR merged -- ต้องเห็นบรรทัดบน main)
2. `grep -n "FORCE_POS_VITAL_VERSION_CONFIRMED" src/pirateforce_foundation/gm/teleport_wire.py`
   ต้อง**ไม่ใช่** `None` และคอมเมนต์เหนือมันต้องอ้าง `RE-129` ที่ปิดแล้วพร้อม VA
3. บัญชีที่เจ้าของจะบูตอยู่ใน `gm_accounts.json` (ค่าเริ่มต้นว่าง = ไม่มีใครเป็น GM)
4. 🔴 **ด่านใหม่ ต้องผ่านด้วย** (เพิ่มโดย LANE-GM เจ้าของใบ รอบ `38c4tv` 2026-08-29T08:22+07:00
   หลัง `pirate-force-server#236` merge — เหตุมาจากจดหมาย chief `20260829_0604` ข้อ ②bis (ก)):
   **บัญชีที่จะบูตต้องไม่มีใบล็อกอินฉากค้างอยู่** ทั้งสองแฟ้ม —
   `grep -c '<ชื่อบัญชี>' config/gm_login_scene.json config/gm_login_scene_standalone.json`
   ต้องได้ `0` ทั้งคู่ (ไฟล์ไม่มี = ผ่าน)
   เหตุผลที่ **วัดแล้วในโค้ด ไม่ใช่ข้อควรระวัง**: ล็อกอินที่ใช้ override เป็น **"การไปเยือน"**
   (`runtime.py` ตั้ง `login_scene_override_visit = True`) ⇒ เซสชันนั้น **ไม่เขียนแถวตำแหน่งผ่าน
   checkpoint ของ TargetPos เลย** (ถ้อยคำแคบลงหลัง pf-adversary ชี้: จุดเขียนของ world-travel departure
   ที่ `runtime.py:6139` อยู่ **นอก** guard ตัวนี้ — วันนี้เข้าไม่ถึงเพราะประตู walk-in ปิดอยู่ทั้งหมด
   คอนโซลพิมพ์ `WORLD_TRAVEL_INERT` ทุกเซสชัน แต่ถ้อยคำเดิม "ไม่เขียนแถวตำแหน่งจริงเลย" เป็นจริง
   เพราะแฟล็กตัวนั้น ซึ่งด่านนี้ไม่ได้เอ่ยถึง)
   ⇒ โทเคน `GM_WARP_POSITION_CONFIRMED` **ไม่มีทางยิง** เพราะไม่มีการเขียนจริงให้รอด
   ⇒ ผู้เทสที่เดินตามขั้นตอนข้อ 3 จะเห็นคอนโซลเงียบ แล้วบันทึก FAIL ให้ `/warp`
   ทั้งที่สาเหตุคือใบล็อกอินที่ค้างอยู่ ไม่ใช่ warp
   🔴 กับดักนี้เกิดง่ายเป็นพิเศษกับใบนี้: `/warp <ฉากอื่น>` **สตางค์ใบล็อกอินให้บัญชีเดียวกัน**
   (ขั้นตอนข้อ 4 ของใบนี้เอง) ⇒ ถ้าเทสรอบก่อนพิมพ์คำสั่งนั้นแล้วไม่ได้ล็อกอินกินใบทิ้ง
   ใบยังค้างอยู่ข้ามรอบ · ใบ GM-gated ถูกกินโดยล็อกอินถัดไปหนึ่งครั้ง (`COO-DECISION 0441` ข้อ 2)
   แต่ใบใน **แฟ้ม standalone ไม่ถูกกินเลย** (`COO-DECISION 0542`) ⇒ ค้างจนกว่าจะลบด้วยมือ
   🔴 **grep ที่ path ไหน — อย่าเชื่อ path ปริยาย** (แก้โดย pf-adversary ก่อน push รอบ `38c4tv`):
   ตัว resolve อ่าน **ตัวแปรสภาพแวดล้อมก่อน** แล้วค่อยตกมาที่ path ปริยายซึ่งอิง cwd ⇒ ตรวจตามลำดับนี้
   `echo %PF_GM_LOGIN_SCENE_CONFIG%` และ `echo %PF_GM_LOGIN_SCENE_STANDALONE_CONFIG%` — ตั้งไว้ก็ grep ไฟล์นั้น
   ไม่ได้ตั้งจึงใช้ `config\gm_login_scene.json` และ `config\gm_login_scene_standalone.json`
   **เทียบจาก cwd ที่บูตเซิร์ฟเวอร์จริง ไม่ใช่จากรากรีโป** · `config/` อยู่ใน `.gitignore` (`/*`)
   ⇒ ในโคลนใหม่จะ **ไม่มีโฟลเดอร์นี้เลย** ซึ่ง = ผ่าน ไม่ใช่ = ตรวจไม่ได้
   วิธีเคลียร์: ลบบรรทัดของบัญชีนั้นออกจากทั้งสองแฟ้มก่อนบูต
   🔴 **สิ่งที่คอนโซลยืนยันให้ไม่ได้ ถ้าไม่บูตด้วย `--export-events`** (pf-adversary วัดแล้ว):
   `gm_login_scene_override_applied_*` และ `gm_login_scene_override_visit_no_durable_write_scene_*`
   เป็น `self.events.append` **ล้วน ๆ** ไม่มีที่ไหนใน `runtime.py` พิมพ์ `self.events` ออกมาเอง —
   ทางเดียวที่ออกจอคือ `--export-events` (`app.py`) และรูปที่พิมพ์คือ `PF-EVENT <seq> <event>`
   ⇒ **ถ้าบูตธรรมดา คอนโซลเงียบทุกกรณี** ⇒ "ไม่เห็นบรรทัดนี้" ไม่ใช่หลักฐานว่าไม่มีใบค้าง
   มันคือด่านที่ตอบ PASS ได้อย่างเดียว ซึ่งเป็นความล้มเหลวแบบเดียวกับที่ด่านนี้ถูกเขียนขึ้นมากัน
   ⇒ **ตัว grep สองแฟ้มข้างบนคือด่านจริง** · จะยืนยันซ้ำที่คอนโซลก็ได้ **ต้องบูตด้วย `--export-events`**
   (ตรวจก่อนว่ามีจริง: `git grep -n 'export-events' <SHA> -- src/pirateforce_foundation/app.py`)
   แล้ว grep แบบ substring บนบรรทัด `PF-EVENT` ไม่ใช่ grep ชื่อ event เปล่า ๆ

### ขั้นตอน (ที่ใจกลางเมือง X=11865 Y=6147 ห้ามท่าเรือ ตามกฎสายนี้)
1. login ด้วยบัญชี GM รอจนโหลดฉากเสร็จ **จดพิกัดตั้งต้นที่เห็นบนจอ**
2. พิมพ์ในกล่องแชทธรรมดา: `/warp <scene_id ที่อยู่ตอนนี้> 11900 6200` (ขยับสั้น ๆ ในฉากเดิม)
3. บันทึก: ตัวละครขยับไหม · ขยับไปตรงพิกัดที่สั่งไหม · จมพื้น/ลอยไหม (z มาจาก connection ไม่ได้แต่ง)
4. **เคสลบที่ต้องทำด้วย** พิมพ์ `/warp <ฉากอื่น> 1 2` -> ต้อง**ไม่เกิดอะไรขึ้น** (ForcePos ข้ามฉากไม่ได้
   โมดูลปฏิเสธโดยตั้งใจ ไม่ใช่บั๊ก) · และพิมพ์ข้อความธรรมดา (ไม่ขึ้นต้น `/`) -> ต้องไม่มีอะไรผิดปกติ
5. ให้ผู้เล่นธรรมดา (บัญชีนอก `gm_accounts`) พิมพ์คำสั่งเดียวกัน -> ต้องไม่เกิดอะไร และไม่มีแถวใน ndjson

### เกณฑ์สองชั้น
- **ชั้น wire/DB:** คอนโซลเซิร์ฟเวอร์มี label ~~`LANE_GM_CHAT_WARP_FORCE_POS`~~ **`LANE_GM_CHAT_WARP_TELEPORT_FORCE_POS`**
  หนึ่งครั้งต่อหนึ่งคำสั่งที่รับ (แก้โดยผู้เปิดใบ LANE-GM รอบ `w8hnu9` 2026-08-28T23:3x+07:00 --
  ชื่อเดิมในใบนี้ **ไม่เคยตรงกับโค้ด**: ค่าคงที่จริงคือ `chat_command_action.WARP_ACTION_LABEL`
  ซึ่งมีคำว่า `TELEPORT` คั่นกลางมาตั้งแต่รอบ `gr2q9j` เพราะ `runtime.py:3654-3675` ทดสอบ
  substring นั้นเพื่อเปิด grace window ของ move-authority ⇒ ผู้เทสที่ grep ชื่อเดิมจะไม่เจอ
  แล้วบันทึก FAIL ทั้งที่ระบบทำงานถูก · grep ที่ถูกคือ `LANE_GM_CHAT_WARP` ก็พอ)
  · ndjson: ~~**หนึ่งแถวต่อหนึ่งคำสั่ง (ไม่ใช่สองแถว -- สองแถว = เผลอ wire ทั้ง `fire()` และ action)**~~
  **แก้รอบ `dm8o4l` (chief R240, ของที่ LANE-GM ชี้ 2026-08-30T12:33+07:00):** ตั้งแต่ `CORE-REQUEST-GM-032`
  ข้อ 1-2 หนึ่งคำสั่ง = **`issued` + `outcome`** อย่างน้อย และตั้งแต่ `CORE-REQUEST-GM-040` (R237/GM ครึ่งหลัง
  รอบ `dm8o4l`) เพิ่มเป็น **`issued` → `outcome:composed` → `outcome:queued`** ได้ถึงสามแถวต่อหนึ่งคำสั่ง
  (record_id เดียว append-only ไม่ใช่แก้แถวเดิม) ⇒ วิธีจับ double-wire เปลี่ยนเป็น **นับ `record_id`
  ที่ไม่ซ้ำกัน**: หนึ่งคำสั่งต้องได้ `record_id` เดียว · เห็นสอง `record_id` สำหรับบรรทัดที่พิมพ์ครั้งเดียว =
  เผลอ wire สองทางจริง · คนอ่านที่ต้องการทราบสถานะล่าสุดของคำสั่ง ให้หยิบแถว `outcome` ตัวสุดท้ายของ
  `record_id` นั้น ไม่ใช่ "แถว outcome" เฉย ๆ (ดู P1 ของ `GT-127` สำหรับวิธีตัดสินว่า BOOT_COMMIT ของคุณเป็นแบบไหน)
- **ชั้น client-observable:** ตัวละครอยู่ที่พิกัดใหม่บนจอ (ภาพ/คำบอกเล่าของเจ้าของ)

### 🔴 ถ้าจอไม่ขยับ ให้แยกสามสถานะก่อนบันทึกผล (เพิ่มโดย LANE-GM เจ้าของใบ รอบ `tvbiqc` 2026-08-29T22:3x+07:00)
โทเคนใหม่บนคอนโซลเซิร์ฟเวอร์: `GM_CHAT_NO_BYTES_SENT` (โมดูล `gm/chat_command_action.py` ของสาย GM
· ไม่ต้องใช้ `--export-events` · พิมพ์ลง stderr เหมือนโทเคนอื่นของเส้นทางนี้)
| เห็นอะไรบนคอนโซลหลังพิมพ์คำสั่ง | แปลว่า | บันทึกผลว่า |
|---|---|---|
| `LANE_GM_CHAT_ACTION warp route=action` **แล้วตามด้วย** `GM_CHAT_NO_BYTES_SENT ... why=withheld_force_pos_vital_version` | เซิร์ฟเวอร์ **จงใจไม่ส่ง** เพราะเกต version ยังปิด (ด่านก่อนบูตข้อ 2 ไม่ผ่าน) | **BLOCKED ไม่ใช่ FAIL** -- ใบนี้ยังไม่ได้ถูกทดสอบเลย |
| `LANE_GM_CHAT_ACTION warp route=action` **อย่างเดียว ไม่มีบรรทัดที่สอง** | เฟรมออกไปแล้วจริง ๆ | ใบนี้ถูกทดสอบแล้ว จอไม่ขยับ = **ผลลบของจริง** (คือคำตอบที่ `RE-129` ทำนายไว้) |
| ไม่มี `LANE_GM_CHAT_ACTION` เลย | เส้นทางไม่ถูกเรียก (ด่านข้อ 1) หรือบัญชีไม่ใช่ GM (ด่านข้อ 3) | **ห้ามเกรด** กลับไปด่านก่อนบูต |
🔴 ก่อนรอบนี้ สามสถานะนี้หน้าตาเหมือนกันบนคอนโซล ⇒ ใบนี้เคยเกรดผิดได้โดยไม่มีใครรู้

### nonclaims ที่ผลของใบนี้ **ห้าม**ถูกใช้อ้าง
1. [ไม่อ้าง] ว่า warp ข้ามฉากทำได้ -- ใบนี้ทดสอบ **ในฉากเดียว**เท่านั้น (`ForcePos` ไม่มีช่อง scene id)
2. [ไม่อ้าง] ว่า M2 หรือ milestone ใดผ่าน -- **GM คือเครื่องมือไปถึงสภาพที่จะเทส ไม่ใช่หลักฐานว่าฟีเจอร์ทำงาน**
   ถ้าใบนี้ PASS สิ่งที่พิสูจน์คือ "เราย้ายตัวละครไปจุดที่อยากเทสได้" ไม่ใช่ว่าการเดินทางในเกมทำงาน
3. [ไม่อ้าง] อะไรเกี่ยวกับ `BT_GM`/`GMUI_BASIC`/`0x51E9` -- คนละประตู (`RE-126` ยังเปิด)
4. [ไม่อ้าง] ว่าคำสั่ง GM อื่น (`npc`/`item`/`lv`/`spawn`/`say`) ทำงาน -- ยังไม่มี wire ทั้งห้าตัว

**ผู้เปิดใบ: LANE-GM (รอบ `gr2q9j`)** -- ผลกลับมาที่สาย GM บริโภค

---


## GT-218 SPEED-SAFE-VALUE-400-DRY-RUN-CLIENT-SURVIVES-001  [**CLOSED** -- ❌ **FAIL · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00**
🔴 **คำ `CLOSED` เติมโดย LANE-GM (สายที่ถือผลใบนี้) รอบ `83wujr` 2026-09-06T07:2x+07:00 ตาม `FROM_CHIEF_R364` ข้อ 2 -- ไม่ใช่การเปลี่ยนผล** เหตุผลสองข้อ ตรวจได้เอง: (ก) ใบนี้ **ถูกบูตและเกรดจบไปแล้ว** (FAIL + `OBSERVER_CONFIRMED 2026-09-03T16:51+07:00` โดย chief รอบ `pk14rf`/R326) ⇒ ไม่มีอะไรให้บูตอีก การเติมบล็อก `ATTENDED:` จะพาใบที่ตัดสินแล้วขึ้นรถบัส capture ของเจ้าของโดยไม่มีคำถามค้าง (`FROM_CHIEF_R364` ข้อ 2 สั่งเองว่า "ใบที่ตอบไปแล้วให้ปิด แทนการเติมบล็อก") (ข) ที่ `pf_queue_status.py` รายงานใบนี้ว่า "พร้อมบูต" คือ **รูของ regex ไม่ใช่สถานะจริง**: `FAIL` ไม่อยู่ในรายการโทเคนของ `STATUS` (`tools_bridge/pf_queue_status.py:19`) ⇒ ตัวจับไปหยิบโทเคน "พร้อมบูต" ที่เคยอยู่ในวลีประวัติท้ายหัวใบแทน (วลีนั้นถูกเขียนใหม่ในรอบเดียวกันแล้ว) · คำ `CLOSED` ที่อยู่ซ้ายสุดแก้การนับนี้โดยไม่แตะเครื่องมือ (เครื่องมือไม่ใช่เขตของสายนี้) · 🔴 **ผลและงานที่ผลนี้ส่งต่อไม่ถูกปิดไปด้วย**: ผู้ต้องหาคือ**รูปเฟรม `UpdateAttrVital 0x309A`** (`COO-DECISION 20260903_1744`) ยังเป็นหนี้เปิดของ LANE-GM และเป็นคำถามเดียวกับที่ `RE-LV-LIVE-UPDATE-FRAME-001` (ขอไว้ใน `notes_to_chief/20260906_0434_LANE-GM-TO-CHIEF-slash-lv-*.md`) ถาม · 🔴 **chief/COO ไม่เห็นด้วย = พลิกกลับได้ด้วยการลบคำ `CLOSED` แล้วเขียนสถานะที่ต้องการลงไปแทน** ไม่มีอะไรถูกลบหรือย้าย · 🔴 **อย่าลบเฉย ๆ**: pf-adversary รอบนี้รันจริงแล้วพบว่าการลบคำเดียวโดยไม่ใส่อะไรแทน ทำให้เครื่องมือไปหยิบโทเคน "พร้อมบูต" จากวลีประวัติในบรรทัดถัดมาผ่านหน้าต่าง fallback `body+1` แล้วรายงานว่าอ่านมาจากเนื้อใบอย่างชอบธรรม (คอลัมน์ `body+1`) -- รูเดิมแต่พรางตัวดีกว่าเดิม ⇒ วลีนั้นถูกแก้เป็น "สถานะก่อนบูต (ประวัติ...)" ในรอบเดียวกันเพื่อปิดรูนั้นไม่ว่าใครจะลบ `CLOSED` หรือไม่ (แจ้งไว้ใน `notes_to_chief/20260906_07xx_LANE-GM-TO-CHIEF-*`) (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — `/speed 400` (ค่าเดียวกับที่ล็อกอินส่งทุกวัน) ทำไคลเอนต์ตายในเฟรมเดียว: HP `0/1` เงิน `0` ไดอะล็อกตาย · เฟรม `LANE_GM_CHAT_SPEED_UPDATE_ATTR_VITAL` 74 ไบต์ออกจริงครั้งเดียว `SPEED DEFERRED` = 0 · แถว DB ไม่เสียหาย รีล็อกอินรอดเพราะประตูล็อกอิน (`#632`) ⇒ 🔴 **ค่าพ้นผิด ผู้ต้องหาคือรูปเฟรม `UpdateAttrVital 0x309A`** (`COO-DECISION 20260903_1744`) · ผลไปที่ **LANE-GM** ไม่ใช่ chief · สถานะก่อนบูต (ประวัติ ไม่ใช่สถานะวันนี้): ปลดเป็นบูตได้แล้ว R317 -- RECHECK ผ่านครบ 4/4 · chief วัดเองบน `origin/main` `01960240` 2026-09-03T09:5x+07:00 (ไม่ได้เชื่อจดหมาย: `LANE-GM 0822` และ `COO 0845` เป็นแหล่งที่สองที่สาม) · ล็อกทั้งสองของ `/speed` **ยังปิดค้างไว้ตามเดิม ไม่มีใครพลิก** ประตูเปิดในเซสชันผู้เทสด้วย `PF_SPEED_TRIAL=400` เท่านั้น · 🔴 ใบนี้พิสูจน์ "เส้นทางปลอดภัย" **ไม่ได้พิสูจน์ว่าเซิร์ฟเวอร์อ่านแถว** อ่านหัวข้อ "ข้อจำกัดที่ใบนี้พิสูจน์ไม่ได้" ก่อนรายงานผล]

### 🔴 PRECONDITION ที่ต้องทำจริงก่อนขั้น 1 -- ไม่ใช่หมายเหตุ (`COO-DECISION 20260903_0845` ข้อ 3)
  P1. `set PF_SPEED_TRIAL=400` **ในหน้าต่างคำสั่งเดียวกับที่จะบูตเซิร์ฟเวอร์ และก่อนบูต** · ค่าอื่นนอกจาก `400` = ออกนอกขอบเขตใบ หยุดและรายงาน
  P2. ยืนยันว่าตั้งติดจริงก่อนบูต: `echo %PF_SPEED_TRIAL%` ต้องพิมพ์ `400` (ไม่ใช่ `%PF_SPEED_TRIAL%`) — คัดบรรทัดนี้ลงผลใบ
  P3. บูตเซิร์ฟเวอร์จากหน้าต่างนั้น **หน้าต่างเดียวกัน** · ตัวแปรปิดเองเมื่อโปรเซสตาย · 🔴 **ห้ามแก้โค้ดเพื่อเปิดประตู และห้ามพลิกธงบน `main`**
  P4. ไม่ตั้ง `PF_SPEED_TRIAL` = `/speed 400` จะถูกกักและขึ้น `SPEED DENIED` ⇒ รอบนั้นเป็น **NO-RESULT ไม่ใช่ FAIL** (ดู pass criteria ข้อ (4))
  ที่มาของกลไก: `gm/speed_wire.py:430` `SPEED_TRIAL_ENV = "PF_SPEED_TRIAL"` · `trial_opening()`/`trial_admits()` อ่าน `os.environ` สดทุกครั้ง ไม่แคช · ผู้เรียกบนเส้น dispatch `gm/chat_command_action.py:4122`

### 🔴 ข้อจำกัดที่ใบนี้พิสูจน์ไม่ได้ -- อ่านก่อนเขียนผล (`COO-DECISION 20260903_0845` ข้อ 4 · ย้ำ `COO 0054`)
  หลังไมล์สโตน `009` **ค่า DEFAULT ของคอลัมน์ `characters.speed_walk` = `400.0` = ค่าคงตัวที่ฮาร์ดโค้ดเดิมทุกไบต์**
  ⇒ "เซิร์ฟเวอร์อ่านแถวแล้วส่ง 400" กับ "เซิร์ฟเวอร์ส่งค่าคงตัว 400" ให้ **ไบต์ชุดเดียวกัน** บนดาต้าเบสสดทุกตัว **รวมของเจ้าของ**
  ⇒ ใบนี้พิสูจน์ได้อย่างเดียวว่า **เส้นทาง `/speed` ปลอดภัยที่ค่า 400** · 🔴 **ห้ามรอบไหนรายงานผลใบนี้เป็น "ชัยชนะบนจอ" หรือเป็นหลักฐานว่า `/speed` ทำงาน**
  แยกสองอย่างนี้ออกจากกันได้ด้วย fixture ที่เขียนค่าอื่น หรือด้วยการรัน `/speed` ค่าที่ต่างจาก 400 เท่านั้น = **ใบใหม่หลังใบนี้ผ่าน**

> เปิดโดย chief รอบ R310 ตาม `COO-DECISION 20260902_2148` ใบที่ 1 · numbering: `GT` สูงสุดในคิว = 217 · `RE` สูงสุดใน `CLIENT_RE_QUEUE.md` = 133 ⇒ ใบนี้คือ **218**
> 🔴 โค้ดใต้ล็อกทั้งสอง **ยังไม่เคยถูกรันแม้แต่ครั้งเดียว** วันที่ล็อกที่สองเปิด = วันแรกที่มันทำงาน และมันจะทำงานต่อหน้าเจ้าของ ⇒ ใบนี้ถูกออกแบบให้ **พังได้อย่างปลอดภัย** · 🔴 **ห้ามพ่วงงานอื่นในใบนี้** ใบอื่นห้ามพังไปกับมัน

RECHECK: (ตัดสินด้วยเนื้อโค้ดบน `origin/main` ห้ามเชื่อคำบอกเล่าหรือเลข commit · ผ่านครบสี่ข้อ = เลื่อนเป็น `READY` ได้เองโดยไม่ต้องรอเจ้าของใบ)
  🔴 **บล็อกนี้ถูกเขียนใหม่ทั้งบล็อกตาม `COO-DECISION 20260903_0649` ข้อ ② (chief รอบ R315)** — รูปเดิมเรียกร้อง `SPEED_LOGIN_READ_LANDED = True` และ `SHAPES_CLEARED_BY_A_REAL_CLIENT` ไม่ว่าง **เป็นเงื่อนไขเข้ารอบ** ทั้งที่สองอย่างนั้นคือ **ผลลัพธ์ของรอบนี้เอง** ⇒ ใบไม่มีวันบูตได้ (วงปิดที่ `LANE-GM 20260903_0529` ข้อ 2 รายงาน)
  🔴 **ล็อกทั้งสองตัวคงค่าเดิมบน `main` ตลอดใบนี้ · RECHECK ห้ามวัดว่ามันเปิด และห้ามใครพลิกมันเพื่อให้ใบนี้บูตได้** (`gm/speed_wire.py:357` = `return not SPEED_LOGIN_READ_LANDED` ⇒ ธงนั้นคือ **ล็อกตัวจริง ไม่ใช่บันทึกข้อเท็จจริง** · "`#605` ลงแล้ว" ไม่ใช่เหตุผลที่พลิกได้) · ประตูเปิด **ในเซสชันของผู้เทสเท่านั้น** ผ่านเกต runtime ข้อ 3 และปิดเองเมื่อโปรเซสตาย
  1. `(cd pirate-force-server && git fetch origin && git show origin/main:src/pirateforce_foundation/session.py | findstr /C:"login_speed.resolve_for_character")`
  2. `(cd pirate-force-server && git show origin/main:src/pirateforce_foundation/login_speed.py | findstr /C:"speed_wire.send_deferred()" /C:"wire_deferred")`
  3. `(cd pirate-force-server && git show origin/main:src/pirateforce_foundation/gm/speed_wire.py | findstr /C:"PF_SPEED_TRIAL")`
  4. `(cd pirate-force-server && py -3 -m pytest tests/test_login_speed.py tests/test_gm_speed_deferred.py tests/test_gm_speed_shape_hold.py -q)`
  ข้อ 1 ต้อง **เจอ** = login-read ต่อที่ seam จริง (ล็อกที่ 1 · `COO 1846`)
  ข้อ 2 ต้อง **เจอทั้งสองคำ** = เกตล็อกอินของ `COO-DECISION 20260903_0645` อยู่บน `main` แล้ว: ขณะ `/speed` ถูกกัก ล็อกอิน **ส่งค่าคงตัว** ไม่ใช่ค่าจากแถว (ลงรอบ R315 · `login_speed.held_by_the_speed_deferral`)
     🔴 ข้อนี้คือเหตุผลที่ขั้น "รีล็อกอินเพื่อกู้" ในใบนี้ไม่ใช่กับดัก — ไม่เจอ = **ห้ามบูตใบนี้เด็ดขาด** เพราะแถว `300.0` ที่ `GT-193` ทิ้งไว้จะขึ้นไวร์ตอนล็อกอินถัดไป (`00 00 96 43` ไบต์ชุดเดียวกับที่ล็อกไคลเอนต์ 426 เฟรม)
  ข้อ 3 ต้อง **เจอ** = LANE-GM ลงเกต runtime `PF_SPEED_TRIAL` แล้ว (`COO-DECISION 20260903_0646`) ⇒ ผู้เทสเปิดประตูในเซสชันตัวเองได้โดยไม่ต้องแก้โค้ดและไม่ต้องพลิกล็อกบน `main`
     ~~**ยังไม่เจอวันนี้** (chief วัดบน `origin/main` `d916725` รอบ R315) ⇒ ใบคง `[BLOCKED]`~~ **← ขีดฆ่า ไม่ลบ (R317)**: บรรทัดนั้นจริงตอนเขียน · `#634` merge 2026-09-03T01:11:13Z = **08:11+07:00** คือ **หลัง** การวัดของ R315 ⇒ ไม่ใช่ความผิดของใคร
     **วัดใหม่ R317 (`mgm333`) บน `origin/main` `01960240`: เจอ 8 ครั้ง ⇒ ข้อ 3 ผ่าน** · ทั้งสี่ข้อผ่าน (ข้อ 1 เจอ 1 · ข้อ 2 เจอ 5 และ 3 · ข้อ 4 `138 passed / 66 subtests` รันบน worktree ของ `origin/main` เปล่า) ⇒ **ป้ายพลิกเป็น `[🟢 READY]` ตามที่หัวบล็อกนี้เขียนสั่งไว้เอง**
     🔴 **บล็อก RECHECK ไม่ถูกลบ** — มันยังเป็นเกตถาวรของทุกรอบที่จะบูตใบนี้ · ข้อใดพลิกกลับเป็นไม่เจอเมื่อไหร่ ป้ายกลับเป็น `[BLOCKED]` ทันทีโดยไม่ต้องถามใคร
  ข้อ 4 เขียวทั้งชุด · ข้อใดไม่ตรง = คง `[BLOCKED]` **ห้ามบูต ห้ามเรียกผู้เทส**
  ใบนี้มีชั้น client-observable ⇒ **G-OBS บังคับ**: จดหมายผลต้องมี `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` · รันจบแต่ยังไม่มีลายเซ็นตาคน = **`AWAITING-OBSERVER`** (ไม่ใช่ PASS ไม่ใช่ FAIL) · ทุกเฟรมที่ยกมาอ้างต้องมี `t` เทียบ `T0` และ `dist` (G-FRAME)

- objective: ข้ออ้างเดียว -- **พิมพ์ `/speed 400` หนึ่งครั้งบนไคลเอนต์จริง แล้วตัวละคร "รอด": ไม่ตาย และไคลเอนต์ยังรับอินพุตต่อได้** (`GT-193` FAIL: `/speed 300` ⇒ HP 0 · เงิน 0 · ตาย · 426 เฟรมถัดมาไม่มีคลิกเลย · DB ฝั่งเราสะอาด)

- ค่าที่อนุญาต: **`400` ค่าเดียว** พิมพ์ `/speed 400` เป๊ะ ห้ามลองค่าอื่นในรอบนี้แม้แต่ครั้งเดียว
  🔴 **ซอร์สวันนี้ไม่มี clamp และไม่มี allow-list ของค่าเลย**: `gm/speed_wire.py:132-153` (`parse_speed_value`) และ `:184-188` รับ float finite ทุกค่า ปฏิเสธแค่ bool/NaN/Inf · ช่วงเดียวที่มีคือช่วง f32 ทั้งช่วง (`persistence_typed_attrs.py:114` ใช้ที่ `:227-235`,`:250-254`) ⇒ **`400` ปลอดภัยด้วยหลักฐาน ไม่ใช่ด้วยประตูในโค้ด**
  หลักฐานของ `400`: เป็นเลขที่ทุกล็อกอินส่งให้ไคลเอนต์อยู่แล้ววันนี้ (`player_wire.py:77`) · เป็นค่าคอนสตรัคเตอร์ของไคลเอนต์เอง VA `0x00464AF2` ไบต์ `00 00 C8 43` (`migrations/008_character_speed_walk_seed.sql:39,123` · `persistence_attr_compose.py:281,289`) · เป็นค่าในบล็อก "สมประกอบ" ของตัวละครบูต (x7 = 400)
  ⇒ ค่าตรงกับของเดิมทุกไบต์ ⇒ ถ้าไคลเอนต์ยังตายอีก **ผู้ต้องสงสัยคือทรงเฟรม ไม่ใช่ตัวเลข** ซึ่งเป็นคำตอบที่วันนี้เราไม่มี

- 🔴 **อาจต้องรีล็อกอิน -- รู้ไว้ก่อนกด ไม่ใช่ตอนจอค้าง**: ถ้าไคลเอนต์ล็อกตัวเองซ้ำแบบ `GT-193` ทางออกเดียวคือปิดไคลเอนต์ **แล้วรีสตาร์ตเซิร์ฟเวอร์ก่อน** จึงบูตไคลเอนต์ใหม่ (ไม่รีสตาร์ต = ตัวถัดไปค้าง "connecting" ตลอดกาล) · การรีล็อกอินนี้เป็น **ขั้นกู้ ไม่ใช่ผลวัด** และการที่ต้องใช้มัน = **FAIL ของชั้น client-observable**
  🔴 **ขั้นกู้นี้อยู่ได้ก็ต่อเมื่อ RECHECK ข้อ 2 ผ่านแล้วเท่านั้น** (`COO-DECISION 20260903_0649`): ก่อนเกต `0645` ลง `main` การรีล็อกอินคือทางที่แถวเก่าของ `/speed` ขึ้นไวร์เอง ⇒ ขั้นกู้กลายเป็นกับดักที่ทำซ้ำอาการเดิม · เมื่อกู้แล้วให้บูตเซิร์ฟเวอร์ใหม่ **โดยไม่ตั้ง** `PF_SPEED_TRIAL` (ประตูปิดตามค่าเริ่มต้น) เว้นแต่ใบสั่งใหม่บอกเป็นอย่างอื่น

- db: canonical `state\pirateforce.sqlite3` -- 🔴 **สำเนาเท่านั้น ห้ามเปิด canonical** ⇒ `state\run_gt218_<yyyyMMdd_HHmmss>.sqlite3`
  🔴 **ชื่อสำเนาห้ามเป็น `pirateforce.sqlite3` และห้ามมี `~`** ไม่งั้นเกต `_speed_db_is_canonical` (`gm/chat_command_action.py:3463-3493`) กันคำสั่งทิ้งทั้งใบ
  sha256 สำเนาก่อน/หลัง · sha256 canonical ก่อน/หลัง ต้องเท่ากัน · `PRAGMA integrity_check` = `ok` สองครั้ง · **teardown เสมอ** (เทมเพลตปฏิเสธ boot stamp เก่ากว่า 420 นาที) · รอบคัดลอก DB ⇒ ตัวละครกลับ spawn ทุกบูต ปกติ ไม่ใช่ผลวัด

- server args: บูตมาตรฐาน **ไม่มีแฟล็ก scenario ใด ๆ** · `-SecondPasswordMode bypass` · บัญชี GM ใน `config/gm_accounts.json` · 🔴 เก็บคอนโซลรวม stdout+stderr (โทเคนเลนนี้ออกทาง stderr ล้วน):
  `set PF_SPEED_TRIAL=400`
  `py -3 -u -m pirateforce_foundation.app --db state\run_gt218_<stamp>.sqlite3 2>&1`
  🔴 **ตั้งตัวแปรนี้ในหน้าต่างคำสั่งเดียวกับที่บูตเซิร์ฟเวอร์ ก่อนบูต** (`COO-DECISION 20260903_0646`/`0649`) — มันคือสิ่งเดียวที่เปิดประตู `/speed` ในรอบนี้ · ปิดเองเมื่อโปรเซสตาย · **ห้ามแก้โค้ดเพื่อเปิดประตู และห้ามพลิกธงบน `main`**
  🔴 ค่าที่ตั้งต้องเป็น `400` เท่านั้น ตรงกับค่าที่ใบนี้อนุญาตให้พิมพ์ · ตั้งค่าอื่น = ออกจากขอบเขตใบ หยุดและรายงาน
  🔴 **เกตนี้เปิดประตูเดียว คือ `/speed` ขาออก ไม่เปิดประตูล็อกอิน** — และนั่นตั้งใจ (chief R315 เข้มกว่าใบ `0645` หนึ่งขั้นหลัง pf-adversary): ระหว่าง trial ล็อกอินยังส่ง **ค่าคงตัว** และพิมพ์ `LOGIN_SPEED wire_trial_only` เพราะ trial อนุมัติ **ค่าเดียว** แต่แถวอาจถือค่าที่ไม่ได้รับอนุมัติ (`/speed` เขียนแถวแม้เฟรมถูกกัก)
  ⇒ **ขั้นรีล็อกอินในเซสชันที่ตั้ง `PF_SPEED_TRIAL` จึงปลอดภัย** · เห็น `LOGIN_SPEED wire_trial_only` ในคอนโซล = ปกติ ไม่ใช่ finding · เห็น `LOGIN_SPEED from_row` ระหว่าง trial = **finding หยุดและรายงาน**
  บรรทัด `LOGIN_SPEED ... withheld_row=<ค่า>` บอกว่าแถวถือค่าอะไรอยู่ตอนถูกกัก — คัดดิบลงผลใบด้วย มันคือหลักฐานเดียวที่บอกว่าเกตกันอะไรไว้จริง

- steps: (playbook `ATTENDED_SESSION_RUNBOOK.md` · อัดวิดีโอต่อเนื่องตลอด `LOCK_GAME` · ~10 นาทีบนจอ)
    0. RECHECK ผ่านก่อน · `LOCK_GAME` · boot stamp · sha canonical · คัดลอก DB
    1. **server ก่อน client เสมอ** · ล็อกอิน GM · ยืนยันบล็อก "สมประกอบ" จากคอนโซล (level 1 · class 1 · stats จาก `CHARCREATE_CLASS s_SCORE` · HP/MP จาก `STANDARD_STATUS` · x7 = 400 · ชื่ออยู่ `BasicAttr` x1 `+0x28` ห้ามอยู่ x37 · x39/x41/x42 = 0) ไม่ครบ = หยุด ไม่รัน · จด scene + X/Y/Z + `T0` เป็นเวลาจริง +07:00
    2. `S0-BASE` full-res โดยเห็น **เลข HP และเลขเงิน** ชัด · จัดกล้องด้วย **คลิกขวาค้างลาก** เท่านั้น (หมุนกล้องอย่างเดียว · facing ไม่ขยับ · ไม่มีไบต์ขึ้นไวร์)
    3. baseline: กด `W` ค้าง 5 วินาทีจากจุดที่จำได้ จด X/Y ก่อน-หลัง · `S1-WALK` · (`W/A/S/D` และ `Q`/`E` เปลี่ยน **facing ของตัวละคร** และยิง `TargetPosVital` ⇒ ใช้เฉพาะขั้นที่สั่งให้เดิน)
    4. คลิกช่องแชท **ยืนยันว่าโฟกัสจริง** พิมพ์ `/speed 400` แล้ว Enter · เป็นคำสั่ง GM **ไม่ใช่** ทริกเกอร์แชท 12 ตัวอักษร **ห้ามเติมอักษรให้ครบ 12** · **ห้ามพิมพ์อักษรใดตอนช่องแชทไม่โฟกัส** (กลายเป็นฮอตคีย์)
    5. **ห้ามแตะอะไรเลย 5 วินาที** จ้องจอ · `S2-AFTER` ภายใน ~3 วิ ต้องเห็นเลข HP · เลขเงิน · ช่องแชท
    6. NO-CRASH: **คลิกขวาค้างลากหมุนกล้อง** (🔴 ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้)
    7. เดินซ้ำแบบขั้น 3 จากจุดเดิม กด `W` ค้าง 5 วินาที · `S3-WALK2` · ออกเกมด้วยปุ่ม X
    8. ปิดเซิร์ฟเวอร์ · เก็บ `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **teardown เสมอ** · ห้าม commit เอง
    9. คัดดิบ ห้ามตีความ:
       `findstr /N /C:"LANE_GM_CHAT_ACTION" /C:"LANE_GM_CHAT_SPEED_UPDATE_ATTR_VITAL" /C:"SPEED DEFERRED" /C:"GM_CHAT_NO_BYTES_SENT" /C:"LOGIN_SPEED" server_console_live.*.txt`
    🔴 **STOP:** HP กลายเป็น 0 · เงินกลายเป็น 0 · ตัวละครตาย ⇒ หยุดทั้งใบทันที ถ่าย `S2-AFTER` ให้ได้ แล้วรายงาน (นี่คือ **ผลของใบ** ไม่ใช่ความผิดของผู้เทส)

- pass criteria: (สองชั้น 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**)
    wire/DB (headless พิสูจน์ได้ ไม่ต้องมีตาคน):
      (ก) มี `LANE_GM_CHAT_ACTION speed route=action` แล้วตามด้วย `[G>] LANE_GM_CHAT_SPEED_UPDATE_ATTR_VITAL` **หนึ่งครั้ง** · **ไม่มี** `SPEED DEFERRED` และ **ไม่มี** `GM_CHAT_NO_BYTES_SENT ... why=withheld_speed_*`
      (ข) เฟรมนั้นต้องมี `00 00 C8 43` (400.0) **ไม่ใช่** `00 00 96 43` (300.0 ของ `GT-193`)
      (ค) หลังเฟรมนั้นมีเฟรมขาเข้าที่ **ไม่ใช่ heartbeat อย่างน้อย 1 เฟรม** (`GT-193` วัดได้ 0 จาก 426)
      (ง) `characters.speed_walk` ในสำเนา = `400.0` · ฟิลด์อื่นในแถวเท่าเดิมทุกไบต์ (diff ก่อน/หลัง)
      (จ) `integrity_check` = `ok` สองครั้ง · sha canonical ไม่เปลี่ยน · ไม่มี traceback หลุด
      🔴 **ชั้นนี้ตอบไม่ได้ว่าตัวละครยังมีชีวิตบนจอไหม** -- `GT-193` พิสูจน์แล้วว่า DB ฝั่งเราสะอาดได้ทั้งที่ตัวละครตาย
    client-observable (🔴 ต้องมีคนนั่งหน้าจอ ห้ามอนุมานจากคอนโซล · **ชั้นนี้เท่านั้นที่ตัดสินใบ**):
      (1) ครบ 5 วินาทีหลัง Enter: **เลข HP เท่าเดิมและไม่ใช่ 0 · เลขเงินเท่าเดิม · ไม่ตาย ไม่มีหน้าจอชุบชีวิต** -- เขียนเลขจริงจาก `S0-BASE` และ `S2-AFTER` ทั้งคู่
      (2) ไคลเอนต์ยังรับอินพุต: คลิกขวาค้างลากแล้ว **กล้องหมุนจริงบนจอ** และกด `W` แล้ว **ตัวละครขยับจริงบนจอ**
      (3) **[คำทำนาย ไม่ใช่ผลวัด]** ความเร็วเดิน **ไม่เปลี่ยน** เพราะ 400 คือเลขที่ล็อกอินส่งอยู่แล้ว ⇒ เขียนระยะที่เดินได้ทั้ง `S1-WALK` และ `S3-WALK2` · **ทำนายผิด = finding ไม่ใช่ความล้มเหลว**
      (4) คัดข้อความในช่องแชทตรงตัว · เห็น `SPEED DENIED` (12 ตัวอักษร ASCII) = ล็อกที่ 2 ยังปิด ⇒ รอบนี้เป็น **NO-RESULT ไม่ใช่ FAIL** หยุดและรายงาน
      (5) 🔴 **จดสีป้ายชื่อทุกป้ายทุกภาพ หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** ไม่มีป้ายให้เขียน `none` ห้ามเว้นว่าง · อ่านจาก **full-res เท่านั้น** · **จดสีอย่างเดียว ห้ามเดาสาเหตุ** (`RE-067`) · ต่างจากภาพเซิร์ฟเวอร์จริง ⇒ `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      🔴 **ชั้นนี้ตอบไม่ได้ว่าเฟรมใดออกจากเซิร์ฟเวอร์ หรือแถวใน DB เป็นอะไร**
    🔴 **ผลลบมีค่าเท่าผลบวก**: ตายอีกทั้งที่ค่าเป็น 400 ⇒ ผู้ต้องสงสัยย้ายจาก **ตัวเลข** ไปที่ **ทรงเฟรม** ⇒ redirect ไปคำถาม deserializer · **ห้ามปลด `SHAPES_CLEARED_BY_A_REAL_CLIENT` ด้วยผลลบนี้**

- nonclaims:
  1. ไม่พิสูจน์ว่า `speed_walk` รอดข้ามล็อกอิน -- ใบนี้ใช้ค่าที่เท่ากับค่าเดิมโดยตั้งใจ
  2. ไม่พิสูจน์ว่าค่าอื่นปลอดภัย -- ครอบ `400` ค่าเดียว · `300` ยังเป็นค่าที่ฆ่าตัวละครมาแล้ว (`GT-193`)
  3. ไม่พิสูจน์ว่า `/speed` ทำให้ความเร็วบนจอเปลี่ยนได้จริง (ต้องใช้ค่าที่ต่างจาก 400 = ใบใหม่หลังใบนี้ผ่าน)
  4. ไม่พิสูจน์ vital_version byte ของ `UpdateAttrVital` (0x309A) · ไม่ตัดสินสาเหตุอาการของ `GT-193`
  5. ไม่ตัดสินความหมายของสีป้าย (`RE-067`) · ไม่แตะคอมแบต/ดรอป/กระเป๋า
  6. ไม่ใช่ negative control ของ `check 0/4` -- ใบที่ 2 ของ COO `2148` พ่วงเป็นขั้น `0N` ใน `GT-207` ไม่ใช่ใบนี้

- links: `COO-DECISION 20260902_2148` (ใบที่ 1) · `COO-DECISION 20260902_1846`/`1847` · `GT-193` (FAIL) · `RE-067` ·
  `gm/speed_wire.py:277,327` · `gm/chat_command_action.py:3803,3861` · `session.py` (`login_speed.resolve_for_character`) · `login_speed.py` · `player_wire.py:77`

- result: (ผู้เทสกรอก: PASS/FAIL/NO-RESULT · branch/commit ที่บูต · `S0-BASE`/`S1-WALK`/`S2-AFTER`/`S3-WALK2` · เลข HP/เงินทั้งสองภาพ · บรรทัดคอนโซลดิบทุกโทเคน · ตารางสีป้ายครบทุกป้ายทุกภาพ · sha256 ทั้งสี่ค่า · `integrity_check` · NO-CRASH/CRASH · ต้องรีล็อกอินหรือไม่ · `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: chief (สาย E) รอบ R310 `gnhlin` ตาม `COO-DECISION 20260902_2148` -- chief บริโภคผลใบนี้เอง**

---

