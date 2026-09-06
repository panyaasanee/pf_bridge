# GAME_TEST_QUEUE.md - ARCHIVE 2026-09-06 (chief LANE-E round u2o8d7 / R368)

Verbatim bodies of closed tickets moved out of the live queue file so it can come back
under its size ceiling.  Nothing here is edited: each block is byte-identical to what stood
in the live file, and the live file keeps a one-line stub pointing here.  Only tickets whose
own header carries a closed status (PASS/FAIL/DONE/CLOSED/ANSWERED/FALSIFIED/BOUNDED-NEGATIVE/
CANCELLED) and that were not closed inside the last 24h were moved.  No open ticket was touched.

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


## GT-026 EXIT-PATHS-001: ปิดเกม "ตอนอยู่ในแมพ" และปุ่ม logout ในเกม  [ท่อน A ✅ **PASS** · ท่อน B 🟡 **รันแล้ว (default scenario) — request ยืนยัน · ไม่ freeze · handler เป็น opt-in ไม่ active** · ข้อ 8 🔴 **BLOCKED** บน logout-transition ที่ทำงาน → ดู GT-033]

> 🟡 **รันแล้วรอบใหญ่ #9 (2026-08-20 09:52→10:20, HEAD `87f0769`, จ็อบ 933-937, tester next 938) — ผลเต็มบริโภคโดย chief รอบ 100:** ท่อน A PASS สองชั้น (X ในแมพ → dialog "ต้องการปิดเกมหรือไม่?" ปุ่ม `ยืนยัน`/`ยกเลิก` → กดยืนยัน หน้าต่างหาย ≤1 วิ · wire/DB: `closed_at` ถูกเติมตรงเวลากด = ออกสะอาดในสายตา server) · ท่อน B รันบน **default scenario** (handler HYP-PF-012/013 เป็น opt-in จึงไม่ active): client ส่ง `LogoutVital 0x1B40` จริงถูกต้อง มี **mode discriminator `08 03`=กลับหน้าเลือกตัวละคร / `08 01`=ออกจากเกม** · server default ไม่ตอบ · **client ไม่ transition แต่ก็ไม่ freeze** (รับคลิกปกติ ปิดด้วย X ได้) — ปมอยู่ที่ response shape ที่ทำให้ client เปลี่ยนหน้า ซึ่งรอบ 100 static RE (agent D) พบว่า **echo ทำไม่ได้แน่นอน** (inbound 0x446F30 เป็น reconcile pass ล้วน) → ดู GT-033

> **เปิดโดย chief รอบ 92 (2026-08-20)** — มาจาก **nonclaims ของ LOCALTEST-001 โดยตรง**
> ผู้เทส local พิสูจน์แล้วว่าปุ่ม X ใช้ได้ **แต่พิสูจน์จากหน้า disconnect dialog เท่านั้น**
> ⇒ ยังไม่มีใครรู้ว่า **ตอนอยู่ในแมพ** (ซึ่งมี dialog ยืนยัน) และ **ปุ่ม logout ในเกม** ทำงานยังไงจากฝั่ง local
> 🔴 นี่ไม่ใช่รายการ "ของแถม" — **ทุกรอบใหญ่จบด้วยการออกจากเกม** ถ้าเส้นทางออกไม่ถูกพิสูจน์
> teardown ของทุกเทสจะยืนอยู่บนสมมติฐาน และ **การออกไม่สะอาดคือต้นเหตุของวงจรอุดตันที่กินเวลาเราไปทั้งคืน 2 รอบแล้ว**

- **ไม่ต้อง commit อะไรก่อน** — เทสพฤติกรรม client + เส้นทางออก ไม่ได้เทสฟีเจอร์ใหม่
- **scenario:** ค่าเริ่มต้น (ไม่ต้องเปิด flag ใด ๆ) · **db:** สำเนา canonical ตามปกติ · **server args:** `-SecondPasswordMode bypass`
- **เปิด client ด้วย `Invoke-CimMethod Win32_Process Create`** (ข้อ 8b ในหัวไฟล์ — อย่าใช้ `Start-Process` กับ `.bin`)

### steps (สองท่อน แยกจ็อบ อย่ารวม)

**ท่อน A — ปุ่ม X ตอนอยู่ในแมพ**
1. บูต server + client ตามปกติ → เข้าแมพให้เห็น HP/minimap/ชื่อแมพครบ
2. 🔴 **ถ่าย screenshot ก่อนคลิกทุกครั้ง แล้วดูว่าหน้าต่างแอป Claude ทับ title bar ฝั่งขวาไหม**
   ถ้าทับ → `left_click_drag` ลากหน้าต่างเกมออกมาก่อน (บทเรียน LOCALTEST-001)
3. กดปุ่ม X **หนึ่งครั้ง** → **ถ่ายภาพ dialog ยืนยันที่ขึ้นมา** (นี่คือของที่ยังไม่เคยมีใครเห็นจากฝั่ง local)
4. บันทึกข้อความบน dialog + ตำแหน่ง/ชื่อปุ่มทุกปุ่ม **ก่อน** กดอะไร
5. กดปุ่มยืนยัน → จับเวลาว่าหน้าต่างหายในกี่วินาที

**ท่อน B — ปุ่ม logout ในเกม** (บูตใหม่ อย่าใช้ต่อจากท่อน A)
6. เข้าแมพใหม่ → หาปุ่ม logout/ออกจากเกมใน UI → บันทึกตำแหน่ง
7. กด → บันทึกว่าไปหน้าไหนต่อ (server select? character select? ปิดทั้งโปรแกรม?)
8. ถ้ากลับถึงหน้า character/server select **ให้ลองเข้าเกมซ้ำโดยไม่รีบูตเซิร์ฟ** — ตอบคำถามว่า
   *"ออกแบบสวย ๆ แล้วเข้าใหม่ได้เลยไหม"* ซึ่งข้อ 4 ในหัวไฟล์อ้างว่าได้ **แต่ไม่เคยพิสูจน์กับปุ่ม logout จริง**

### pass criteria (สองชั้น)

**ชั้น client-observable:** มีภาพ dialog ยืนยัน · มีภาพ/บันทึกว่ากด logout แล้วไปหน้าไหน · หน้าต่างหายจากจอ + ไอคอน taskbar หาย
**ชั้น wire/DB:** จ็อบ PID guard ยืนยัน `pid does not exist` (ใช้ Id + StartTime แบบจ็อบ 916) ·
`GameClient` = 0 · listeners 10188/10189 = **0** · console ของ server ไม่เดิน keepalive ต่อ ·
`sessions` +1 (กรอง `selected_character_id IS NOT NULL`, order by `opened_at`) · canonical sha ไม่เปลี่ยน

### nonclaims ที่ต้องเขียนติดผลเสมอ
- ไม่พิสูจน์ว่า logout ทำให้ **persistence** เกิด — เรื่องนั้นเป็นของ GT-001 และเลน persistence
- ไม่พิสูจน์ว่าเส้นทางออกทั้งสองเหมือนกันในทุกแมพ — เทสแมพเดียว
- ถ้ากดแล้วไม่มีอะไรเกิด **ห้ามสรุปว่า "ปุ่มไม่รับคลิก"** จนกว่าจะยืนยันด้วย screenshot ว่าไม่มีหน้าต่างอื่นบัง
  (นี่คือความผิดพลาดเป๊ะ ๆ ที่ข้อ 8 ในหัวไฟล์เคยทำมาแล้ว)

- **result:** ✅ **ท่อน A = PASS** (ภาพ `gt026_exit_dialog_text.png` / `gt026_exit_buttons.png` · closed_at เติมตรงเวลากด) · 🟡 **ท่อน B = รันบน default (handler opt-in ไม่ active): request + discriminator ยืนยัน · ไม่ freeze · ไม่ transition** (ภาพ `gt026_logout_menu.png`) · ❌ **ข้อ 8 ตอบไม่ได้** (ไม่เคยถึงหน้า char select) → BLOCKED บน GT-033 · **PLAYBOOK แก้แล้ว** (logout ไม่ freeze · gear=OPTIONS · ทางเข้า HOME→ออก)

---


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

## GT-084 MOB-COMBAT-001 / MOB-DEATH-001 FIRST-REAL-ATTACK-001: การโจมตีจริงจากผู้เล่นครั้งแรกที่ไปถึง mob_combat/mob_death บนบูตไร้แฟล็ก -- เลือดมอนสเตอร์ลดจริงไหม และ 0x201F ตายไหม  [🟡 **RESULT (ผ่านผลต่อของ GT-084-R2, 2026-08-27) -- wire/DB ครบ (hit x5, HP to 0, MOB-DEATH-001 kill, dying/dead frames, MOB_LOOT_DROP x2) แต่ client-observable FAIL 2 จุด: ศพแข็งลอยค้าง (ไม่ล้มตาม GT-022/GT-025), single-click ไม่มีแผงเป้า -- ดู notes_to_chief/20260827_1620_GT084R2-RESULT-*.md, RE-107/RE-108 ปิดแล้ว (bounded negative, 2026-08-27T17:1x+07:00), ห้ามอ่านเป็น PASS/DONE** [UPDATE 2026-08-28T04:1x+07:00, R205, chief: CORE-REQUEST-024 wired -- server-side attack-cadence gate now runs on this dispatch path (`ATTACK_CADENCE_MS_PROVISIONAL=600`, RE-110 still open), closing the spam-click=runaway-damage gap LANE-B's own letter said this GT was seeing. Wire/DB proven only (`tests/test_mob_combat_cadence_wiring.py`) -- no attended session has confirmed the throttled rate looks right on screen yet]]

🔵 **[UPDATE 2026-08-28T18:46+07:00 · LANE-B รอบ `j6cbdc` · เจ้าของใบ · ไม่แก้ถ้อยคำเดิม เพิ่มบล็อกต่อท้ายอย่างเดียว]**
เกี่ยวกับผลลบชั้นจอข้อ **loot** (`MOB_LOOT_DROP 54B ×2` ออกสายแต่เจ้าของยืนยันว่าไม่เห็นทั้งสองชิ้น):
รอบนี้ **ตัดคำอธิบาย "census recompose ลบของบนพื้น" ออกได้ — ด้วยลำดับบนสาย ซึ่งเป็นหลักฐานชั้น wire ล้วน**:
ในคอนโซลรันนี้ เฟรม `0x02` ใบสุดท้าย (`MOB_DEATH_DEAD`, L9887) มา **ก่อน** เฟรม loot ทั้งสองใบ
(L11198/L11202) และหลังจากนั้นใบผลไม่ได้บันทึกเฟรมสำมะโนอีกเลย ⇒ **ไม่มีเฟรม census ตามหลังของที่ตก**
จึงลบมันไม่ได้ในรันนี้
(หมายเหตุ: derived bit ต่างกัน `0x02` vs `0x08` เป็นข้อเท็จจริงชั้น wire ที่พินไว้จริงใน
`pirate-force-server/tests/test_ground_drop_multi_drop_emission_shape.py` **แต่การสรุปต่อว่า "คนละ object
offset ⇒ consumer สองตัวยุ่งกันไม่ได้" เป็นการอนุมานฝั่ง client** ไฟล์เทสนั้นเขียนไว้เองว่า **ไม่ได้ assert
ทับ offset ฝั่ง client** — อย่าอ้างไฟล์นั้นเป็นหลักฐานของข้อสรุปนั้น)
เหลือ **สี่** สาเหตุที่ยังแข่งกันและ **ยังไม่มีใครแยกสักตัว**: (1) ทรงการส่ง (ดรอป N ชิ้น = N collection
ละ count=ONE · `RE-130` เปิดรอบนี้) · (2) **อายุป้าย 0.2-0.4 วินาที** ลำพังตัวเดียวก็อธิบายได้ทั้งใบ ·
(3) **ตารางไอเทม** — ของที่ตกใบนี้ (`2400046`/`2400047`) มาจาก ITEM_CONSUMABLES **ที่ไม่เคยวาดอะไรบนสายนี้เลย**
และ `mob_loot` NONCLAIM 3 บันทึกไว้เองว่า `2600001` เคย "drew none" · (4) **สภาพ client ในรันนี้เอง** —
ศพแข็ง cursor ไม่จับ actor ไม่มีแผงเป้า ⇒ ไม่ใช่ผู้สังเกตที่คุมได้สำหรับคำถาม "ป้ายวาดไหม"

🔴 **ถอนคำแนะนำที่เขียนไว้เมื่อ 18:46:** ~~"เทียบตัวที่ดรอปชิ้นเดียว vs หลายชิ้น = ตัวแยกสองสาเหตุ"~~
**ผิด** — `pf-adversary` จับได้ว่า `GT-045` (รันที่ **เห็น** ป้าย) ก็ส่ง **สอง** element ทรงเดียวกันเป๊ะ
ห่างกัน 42 ms ⇒ จำนวนชิ้นไม่ใช่ตัวแปรที่ต่างกันระหว่างสองรัน
🔴 **ถึงผู้เทสรอบหน้า (ฉบับแก้):** ถ้ารันใบนี้หรือ `GT-104` อีก ให้**จ้องจุดตายทันทีที่เลือดหมด**
(ป้ายอาจอยู่ไม่ถึงครึ่งวินาที) และถ้าเลือกเป้าได้ ให้เลือกตัวที่ดรอป **ไอเทมจากตารางที่เคยวาดป้ายสำเร็จ**
(EQUIPMENT_BASE เช่น `2200423`) แทน ITEM_CONSUMABLES — นั่นคือตัวแปรที่แยกได้จริงและยังไม่มีใครลอง


> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md, prefix สองแบบ ห้ามแยกตัวนับ.
> เลขสูงสุดที่ใช้ไปแล้ว ณ เวลาเขียนใบนี้: GT-081 (GAME_TEST_QUEUE.md) และ RE-083 (CLIENT_RE_QUEUE.md,
> บันทึกไว้เองว่า "เลขว่างถัดไป = 084"). grep ซ้ำทั้งสองไฟล์ก่อนจอง: GT-084 = 0 hit, RE-084 = 0 hit.
> ใบเก่าทุกใบอยู่ที่เดิม ไม่ถูกแตะ ไม่ถูกย้าย.

### merge แล้ว -- ผ่านด่าน merge แล้ว เหลือด่าน resolver/git-grep ตอนบูต
เนื้อหาที่ใบนี้ทดสอบมาจาก pirate-force-server commit 6105d26 บนแบรนช์
claude/optimistic-mccarthy-mdj01v (CORE-REQUEST-005 / MOB-COMBAT-001, อนุมัติโดย
COO-DECISION 20260826_0402). ยืนยันแล้วว่า commit 6105d26 merge เข้า main จริงแล้ว
ผ่าน PR #63 (merge commit c101b2d) -- ตรวจด้วย git log/git merge-base
--is-ancestor บน repo pirate-force-server เมื่อ 2026-08-26. ตัวบล็อกเดิม "ยังไม่
merge" ปิดแล้ว ไม่ใช่เหตุผลให้ใบนี้ค้างอีกต่อไป.
ใบนี้ยังบูตไม่ได้จนกว่า pf_resolve_green_boot.py คืน BOOT_COMMIT ที่ผ่านการตรวจ
ข้อ 1-5 ของด่าน 2 ข้างล่างครบ -- สองด่านนั้นยังต้องรันทุกครั้งตอนบูตเหมือนเดิม
ไม่ใช่ว่า merge แล้วข้ามได้. ยังไม่มีรอบ attended จริงของใบนี้ ห้ามเปลี่ยนสถานะเป็น
PASS/DONE จนกว่าจะมีผลจากรอบจริง.

### ที่มา -- อ่านจากซอร์สจริง ห้าม re-derive ระหว่างรอบ
- src/pirateforce_foundation/mob_combat.py -- production_allowed = True, ไม่มีแฟล็ก,
  ไม่มี scenario id. สูตรดาเมจ (pin ในไฟล์): attack = 100 + 7*STR + 3*LV,
  defence = 10 + 2*CON + 1*LV, damage = max(1, attack - defence). โปรไฟล์ผู้โจมตี
  ที่ dispatch ใช้จริงเป็นค่าคงที่สังเคราะห์ (MOB_COMBAT_DEFAULT_ATTACKER =
  mob_combat.pin_attacker(), level 7 / STR 132, runtime.py:227-236) -- ไม่ได้อ่านจาก
  ตัวละครจริงของผู้เทส. ต่อ 0x201F (Tornado Eagle, max HP 3857, level 27,
  CON สังเคราะห์ 22) ⇒ defence = 10+44+27 = 81 ⇒ ทุกหมัดที่ลงจริงคาดว่า -964
  (ตัวเลขเดียวกับที่ GT-035 อ่านได้จากจอ) ⇒ ต้องโดน 5 หมัดถึงจะถึง 0 HP
  (964*4 = 3856 เหลือ 1, หมัดที่ 5 clamp เหลือ 1).
- src/pirateforce_foundation/mob_death.py -- production_allowed = True เช่นกัน.
  SANCTIONED_FIRST_TARGET_IDENTITY = 0x201F, SANCTIONING_RULING =
  "PANYA-RULINGS-FOUR 2026-08-25 18:15 +07:00 section 3". kill() ปฏิเสธ identity
  อื่นด้วยชื่อ REFUSE_TARGET_OUTSIDE_THE_SANCTIONED_SCOPE เว้นแต่มีคน widened=
  เข้ามา (ทาง wiring ปัจจุบันไม่ส่ง) ⇒ มอนสเตอร์ตัวอื่นที่ถึง 0 HP ไม่ตาย เงียบ ไม่มี
  เฟรม -- ข้อจำกัดที่ประกาศไว้แล้ว ไม่ใช่บั๊ก. DEATH_TASK_HOLD_MS = 700
  ([LANE-B ASSUMPTION -- awaiting COO confirmation], ยังไม่มีใครวัด).
- src/pirateforce_foundation/runtime.py:3587-3738 (_dispatch_mob_combat) และ
  :4557-4571 -- เรียกแบบ UNCONDITIONAL, ต่อท้ายทุกเลนอื่นแบบ additive, เงื่อนไขเดียว
  คือ nested_id == legacy.ACTION_VITAL. ไม่มีการเช็ค action code ย่อย (0xEA7D)
  ในโค้ดนี้เลย -- ActionVital ใด ๆ ที่ field_qword_20 ชี้ไปที่ identity ในโรสเตอร์
  field-mob ของ bg0001 จะเข้าเลนนี้ทันที.
- src/pirateforce_foundation/field_mob_tables.py:46-59 -- โรสเตอร์ 13 ตัวของ
  bg0001. 0x201F Tornado Eagle อยู่ที่ (1747.5244, -7837.6978, 931.0413) --
  ห่างจากจุดเกิด (-8553.9473, -2579.6890, 186.0) ประมาณ 11,500 หน่วย ซึ่งเป็น
  ตัวที่ "ใกล้ที่สุด" ในบรรดา 13 ตัว. ระยะวาดของโมเดลที่ระยะนี้ ไม่เคยมีใครวัด
  (mob_combat.py nonclaim ของมันเอง).
- SERVER_VERSIONS.md (repo pirate-force-server) บันทึกงานชิ้นนี้ไว้แล้วเป็น
  CORE-REQUEST-005 / pirate-force-server@6105d26, ชั้นซอร์ส ไม่ใช่ชั้นที่ตาเห็น,
  และเขียนไว้เองว่า "ยังไม่มีใครสังเกตว่า input การโจมตีจริงจากไคลเอนต์สร้างเฟรม
  EA7D ที่โมดูลนี้อ่านหรือไม่" -- คำถามเดียวกับที่ใบนี้เปิดขึ้นมาตอบ.
- ทรงการโจมตีจากไคลเอนต์: docs/COMMAND_HANDOFF.md บรรทัด SCENE-006 บันทึกว่า
  ดับเบิลคลิกเป้าหมาย hostile ที่เลือกไว้แล้วเป็นตัวที่ยิง ActionVital 0xEA7D
  (คลิกเดียวแค่เปิดแผงเป้า/เลือกเป้า -- ยืนยันซ้ำที่ GAME_TEST_QUEUE.md:5145
  ว่าคลิกเดียวเปิดแผงได้). ยังไม่เคยมีรอบ attended ไหนลองท่านี้กับมอนสเตอร์จริง.

### objective (claim เดียว)
เมื่อผู้เล่นดับเบิลคลิกโจมตี field-mob จริงใน Port Royal บนบูตที่ไม่มีแฟล็ก
--*-scenario แม้แต่ตัวเดียว คำสั่งโจมตีนั้นไปถึง mob_combat._dispatch_mob_combat
จริงหรือไม่ (ชั้น wire/DB) และไคลเอนต์แสดงเลือด/เลขดาเมจ/ผลของมันตามที่โมดูล
ออกแบบไว้จริงหรือไม่ (ชั้น client-observable) -- รวมถึงกรณีตายของ 0x201F
ถ้าผู้เทสไปถึงและฆ่ามันได้จริงภายในงบเวลา.
สิ่งที่ใบนี้ไม่ถาม: มอนสเตอร์ตอบโต้ไหม (aggro handle ที่ dispatch ส่งคือ None
เสมอในบูตนี้ -- ไม่มีการโต้กลับ), มันดรอปอะไรไหม (M5 คนละใบ), ซากอยู่ทนข้าม
การ reconnect/census rebuild ไหม (คนละ claim, ดู nonclaims).

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)
- P1 [เสนอ, หัวใจของใบ] ถ้าดับเบิลคลิกเป้าที่เป็น field-mob จริงติด -- ไม่ว่า
  identity ไหน -- คอนโซลเซิร์ฟเวอร์จะพิมพ์บรรทัด "MOB-COMBAT-001 hit: performer
  0x... -> target 0x..." ตามด้วย [G>] MOB_COMBAT_ANNOUNCE และ (ถ้ายังไม่ตาย)
  [G>] MOB_COMBAT_BAR.
- P2 [เสนอ] ถ้า P1 เป็นจริง เลขดาเมจสีแดงจะลอยเหนือหัวมอนสเตอร์และหลอด/เลข HP
  บนแผงเป้าจะลดลงตามเลขที่คอนโซลพิมพ์ -- ต่อ 0x201F คาดว่าเห็น -964 ซ้ำ ๆ.
- P3 [เสนอ] ถ้าโจมตี 0x201F จนถึง 0 HP: คอนโซลพิมพ์ "MOB-DEATH-001 kill:
  performer 0x... -> target 0x201F" ตามด้วย [G>] MOB_DEATH_DYING แล้วอีกราว
  700 ms ถัดมา [G>] MOB_DEATH_DEAD -- และบนจอมอนสเตอร์ล้มลงนอนราบ (ท่าเดียว
  กับที่ GT-022/GT-025 เคยเห็น). ไม่ทำนายว่าอนิเมชันตาย (_F_DIE_000) จะเล่น
  หรือไม่ -- ไม่เคยมีใครเห็นมันมาก่อน.
- P4 [เสนอ] ถ้าโจมตีมอนสเตอร์ตัวอื่นที่ไม่ใช่ 0x201F จนถึง 0 HP: คอนโซลพิมพ์
  event ชื่อ mob_death_refused_target_outside_the_sanctioned_scope_no_death_frames
  แทนที่จะพิมพ์เฟรมตาย -- มอนสเตอร์หยุดตอบสนอง (หลอด/เลขค้างที่ 0 หรือค่าสุดท้าย
  ก่อนตาย) แต่ไม่ล้ม ไม่มีอนิเมชัน -- นี่คือผลบวกตามข้อจำกัดที่ประกาศไว้แล้ว
  ไม่ใช่ FAIL.
- P5 [เสนอ, ตัวหักล้าง] ถ้าดับเบิลคลิกเป้าแล้วไม่มีบรรทัดใดใน P1 ขึ้นเลย (ไม่มี
  "MOB-COMBAT-001 hit" ไม่มี event ชื่อ mob_combat_* ใด ๆ) ⇒ แปลว่า input
  โจมตีจริงจากไคลเอนต์ไม่ได้สร้าง ActionVital ทรงที่โมดูลนี้อ่าน (ชี้เป้าไม่ตรง
  field_qword_20, action code ไม่ตรง 0xEA7D ที่จริงมีทรงอื่น, หรือ path การ
  โจมตีไม่ผ่าน ActionVital เลย) -- นี่คือผลลบที่มีค่าที่สุดของทั้งใบ ต้องเขียน
  ผลให้เด่นเท่ากับ PASS ไม่ใช่ด้อยกว่า และควรชี้ทางให้รอบต่อไปจับ capture ดิบ
  ของ ActionVital ที่ไคลเอนต์ส่งจริงมาเทียบ shape กับ parse_action_vital.

### ก่อนบูต -- สองด่าน ต้องผ่านทั้งสองด่านเท่านั้น
ด่าน 1 -- resolve commit เขียว:
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\Pirate Force\pirate-force-server" --fetch
```
รันจากโฟลเดอร์ pf_bridge, exit 0 + BOOT_COMMIT: <sha> เท่านั้นถึงบูตได้ (git checkout
<sha> แบบ detached HEAD). exit 3 = ห้ามบูต จดว่า "ใบนี้รอ merge ไม่ได้รอผู้เทส".
exit 2 = พาธผิด/git ล้ม. ห้ามเทียบเลข commit ด้วยตา -- resolver คืนหัวแบรนช์ที่
ผ่านเกต ไม่ใช่ merge commit เสมอไป.

ด่าน 2 -- ยืนยันการต่อสายกับ <SHA> ที่จะบูตจริง:
```
git grep -n "_dispatch_mob_combat" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "mob_combat_actions = (" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "ACTION_VITAL else" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "SANCTIONED_FIRST_TARGET_IDENTITY = 0x201F" <SHA> -- src/pirateforce_foundation/mob_death.py
git grep -n "production_allowed = True" <SHA> -- src/pirateforce_foundation/mob_combat.py src/pirateforce_foundation/mob_death.py
```
1-4 ต้องได้อย่างน้อย 1 บรรทัดต่อคำสั่งเสมอ. ข้อ 5 ต้องได้ 2 บรรทัด (ไฟล์ละ 1).
ขาดข้อใดข้อหนึ่ง = BLOCKED ต่อ ห้ามบูต ห้ามหาคอมมิตเอง แล้วไปทำใบอื่น.
ชื่อฟังก์ชัน/ค่าคงที่ข้างบนอ่านมาจากซอร์สจริง ณ เวลาที่เขียนใบนี้ -- ถ้ารอบ merge
เปลี่ยนชื่อ ให้เชื่อชื่อจริงในผล PR แล้วแก้ห้าคำสั่งนี้ตามชื่อจริง อย่าเดา.

### db (สำเนาเสมอ ห้ามเปิด canonical, ห้ามแตะ state\play.sqlite3)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-084_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt084.sqlite3
```
- เทียบ sha256 ของ canonical กับ CANON_SHA.txt ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง.
- ใบนี้ไม่ใช่ play mode -- ห้ามกด PLAY_PIRATE_FORCE.bat ระหว่างรอบ (ถือ LOCK_GAME
  ด้วย BY: PLAY MODE และเขียนลง state\play.sqlite3 ซึ่งเป็นโลกที่เจ้าของเล่นข้ามวัน,
  คนละไฟล์). แม้ใบนี้ทดสอบ "บูตไร้แฟล็ก" ซึ่งนิยามโดย SERVER_VERSIONS.md ว่าคือการ
  ดับเบิลคลิก PLAY_PIRATE_FORCE.bat ก็ตาม -- ใบนี้จำลองบูตไร้แฟล็กแบบเดียวกับที่
  GT-078 ทำ (app.py ไม่มี --*-scenario เลยสักตัว บน DB สำเนา) แทนที่จะยิง batch
  จริง เพื่อไม่ให้ทับโลกที่เจ้าของเล่นอยู่ -- เขียนไว้ในผลว่าเป็นการจำลอง ไม่ใช่
  batch จริง.
- สำเนาใหม่ทุกบูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดเสมอ (X -8553.947265625,
  Y -2579.68896484375, Z 186.0).

### server args (เป๊ะ)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt084.sqlite3
```
- ห้ามมี --*-scenario แม้แต่ตัวเดียว, ห้ามพ่วงใบอื่นเข้าบูตนี้ -- "ไม่มีแฟล็ก"
  คือสิ่งที่ถูกทดสอบ.
- หลักฐานว่าไม่มีแฟล็กจริง เก็บทันทีหลังเซิร์ฟเวอร์ขึ้น แปะทั้งบรรทัดลงผล:
```
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List
```

### steps (คลิกต่อคลิก -- อัดวิดีโอตลอดช่วงถือ LOCK_GAME)
ก่อนเริ่ม: ถือ LOCK_GAME, จด boot stamp (+07:00, ต้องไม่เก่ากว่า 420 นาทีตอนรัน
teardown), เทียบ sha canonical, copy DB สองใบตามบล็อก db, เตรียม teardown จาก
TEMPLATE_teardown_generic.ps1.

1. สตาร์ตเซิร์ฟเวอร์ก่อนเสมอ (Get-NetTCPConnection -State Established พอร์ต
   10188/10189 = 0 ก่อนเปิด client). client ที่บูตโดยไม่มีเซิร์ฟเวอร์ตายเองใน
   ~3.5 นาที. ถ้าต้องฆ่า client กลางคัน ต้อง restart server ก่อนเปิด client ใหม่
   เสมอ (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่ "connecting" ตลอดกาล).
2. เปิด client -> เลือกเซิร์ฟเวอร์ -> dialog PVP ปุ่มซ้าย -> หน้าเลือกตัวละคร
   -> เลือกช่องแรก -> ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม (ปุ่มซ้ายสุด =
   ลบตัวละคร ห้ามกด). เริ่มอัดวิดีโอต่อเนื่องตั้งแต่ก่อนกดเข้าเกม.
3. T0 -- เห็น HP bar/minimap/ชื่อแมพครบ. จด HUD X/Y. คลิกขวาค้างลากกวาดกล้อง
   360 องศาหนึ่งรอบ (นี่คือตัวเช็ค NO-CRASH ตัวเดียวที่ใบนี้ยอมรับ -- คลิกขวาลาก
   หมุนกล้องอย่างเดียว ทิศหันตัวละครไม่ขยับ ไม่ยิงอะไรออกสาย ห้ามใช้ Q/E เป็น
   ตัวเช็คนี้เด็ดขาด).
4. เดินไปทาง (1747.5, -7837.7) โดยอ่าน HUD X/Y เทียบทุกช่วง (W/A/S/D คาดว่ายิง
   TargetPosVital ทุกครั้งที่ขยับ/หันตัว -- คาดหมายและไม่ใช่ความเสี่ยงของใบนี้).
   งบเวลาเดินทาง 15 นาที. ถ้าครบ 15 นาทีแล้วยังไม่เห็น/เลือกโมเดล 0x201F ได้
   (single-click เปิดแผงเป้าไม่ได้) ให้ล้มเลิกเป้าหมาย 0x201F แล้วเดินไปหา
   field-mob ตัวอื่นที่ใกล้ที่สุดจาก 13 ตัวในตาราง field_mob_tables.py แทน
   (ระยะทางทั้งหมดไกลจากจุดเกิดพอกันหรือไกลกว่า) -- จดใน result ว่าใช้ตัวไหน
   และทำไม.
5. เมื่อเห็นโมเดล: single-click เปิดแผงเป้า (คลิกเดียวเปิดได้ตามที่ยืนยันไว้แล้ว
   ที่ GT-045 v3). ถ่ายภาพนิ่ง full-res ของแผงเป้า + ป้ายชื่อบนหัวมอนสเตอร์
   ก่อนโจมตีข้อแรก -- นี่คือภาพที่ต้องบันทึกสีป้ายทุกป้าย.
6. ดับเบิลคลิกโมเดลเดิมเพื่อโจมตี. หลังดับเบิลคลิกแต่ละครั้ง จด (ก) บรรทัด
   คอนโซลเซิร์ฟเวอร์ทั้งหมดที่ขึ้นใหม่ (บรรทัด "MOB-COMBAT-001 hit" + บรรทัด
   [G>] MOB_COMBAT_ANNOUNCE/MOB_COMBAT_BAR หรือ event ชื่อ mob_combat_*
   ถ้าถูกปฏิเสธ) (ข) สิ่งที่เห็นบนจอ (เลขดาเมจลอย, หลอด/เลข HP บนแผงเป้า).
   ทำซ้ำจนมอนสเตอร์ถึง 0 HP หรือครบ 10 หมัด (กันเวลาไม่จบ) แล้วแต่อย่างไหน
   ถึงก่อน.
7. ถ้าถึง 0 HP: เฝ้าดู 5 วินาทีถัดไป จดว่ามีอนิเมชัน/ท่าล้มไหม, มีบรรทัด
   MOB_DEATH_DYING/MOB_DEATH_DEAD หรือ event ปฏิเสธของ mob_death ขึ้น. ถ่ายภาพ
   นิ่ง full-res ของโมเดลหลังถึง 0 HP + ป้ายชื่อ (ถ้ายังอ่านได้).
8. ปิดฉาก: NO-CRASH check ด้วยคลิกขวาลากอีกครั้ง. ออกเกม. teardown ตาม
   TEMPLATE_teardown_generic.ps1. เทียบ sha canonical รอบสุดท้าย.

### pass criteria (สองชั้น แยกกันเสมอ ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)

ชั้น wire/DB (อ่านจาก server console/event log ล้วน ๆ ไม่ต้องพึ่งสิ่งที่เห็นบนจอ):
- อย่างน้อยหนึ่งดับเบิลคลิกที่ลงบนโมเดล field-mob จริง ทำให้คอนโซลพิมพ์บรรทัด
  "MOB-COMBAT-001 hit: performer 0x... -> target 0x..." ⇒ พิสูจน์ว่า input
  โจมตีจริงไปถึง _dispatch_mob_combat จริง (คำถามที่ mob_combat.py's own
  nonclaims ทิ้งไว้).
- บรรทัด [G>] MOB_COMBAT_ANNOUNCE ปรากฏคู่กับทุกหมัดที่ลง และ [G>] MOB_COMBAT_BAR
  ปรากฏคู่กับทุกหมัดที่ไม่ใช่หมัดสุดท้าย.
- ถ้าเป้าคือ 0x201F และถึง 0 HP: บรรทัด "MOB-DEATH-001 kill" + [G>]
  MOB_DEATH_DYING แล้ว [G>] MOB_DEATH_DEAD ห่างกันประมาณ hold_ms ที่พิมพ์ไว้
  (คาด 700 ms) + บรรทัด "register now holds 1 dead: 0x201F".
- ถ้าเป้าคือ identity อื่นและถึง 0 HP: event ชื่อ
  mob_death_refused_target_outside_the_sanctioned_scope_no_death_frames ปรากฏ
  แทนเฟรมตาย, ไม่มี MOB_DEATH_DYING/MOB_DEATH_DEAD เลย.
- ผลลบที่สมบูรณ์เท่ากับ PASS: ดับเบิลคลิกเป้าที่เห็นชัดว่าโดนโมเดลแล้ว แต่ไม่มี
  บรรทัด "MOB-COMBAT-001 hit" หรือ event ชื่อ mob_combat_* ใด ๆ ขึ้นเลยสักครั้ง
  ตลอดรอบ ⇒ เขียนเป็นผลลบเต็มรูป พร้อมข้อเสนอ redirect (จับ capture ดิบของ
  ActionVital จริงที่ไคลเอนต์ส่งมาเทียบ shape กับ parse_action_vital.py:3250).

ชั้น client-observable (ต้องมีคนหน้าจอ, ห้ามอนุมานจากบรรทัดคอนโซล):
- เลขดาเมจสีแดงลอยเหนือหัวมอนสเตอร์หลังดับเบิลคลิกแต่ละครั้ง (หรือไม่มี ถ้าชั้น
  wire บอกว่าหมัดนั้นถูกปฏิเสธ).
- หลอด/เลข HP บนแผงเป้าลดลงตามลำดับที่เห็น ไม่ใช่กระโดดหรือค้าง (ยกเว้นหมัด
  สุดท้ายที่ทำให้ถึง 0).
- ถ้าเป้าคือ 0x201F และถึง 0 HP: โมเดลล้มลงนอนราบบนจอจริง (ไม่ทำนายอนิเมชัน
  _F_DIE_000 ว่าจะเล่นหรือไม่ -- บันทึกแค่สิ่งที่เห็น).
- ถ้าเป้าคือ identity อื่นและถึง 0 HP: โมเดลไม่ล้ม ไม่มีอนิเมชัน ยืนนิ่งที่หลอด
  ว่าง -- นี่คือผลบวกของ P4 ไม่ใช่ FAIL.
- สีของป้ายชื่อทุกป้ายในทุกภาพนิ่ง full-res บันทึกเป็นบรรทัดเดียวต่อป้ายต่อภาพ
  ("none" เขียนออกมาถ้าไม่มี ห้ามเว้นว่าง) -- อ่านจากภาพนิ่ง full-res เท่านั้น
  ห้ามอ่านจาก contact sheet/ภาพย่อ/วิดีโอ. ห้ามอนุมานสาเหตุของสี (RE-067 เปิดอยู่).
  ถ้าต่างจากภาพเซิร์ฟเวอร์ต้นฉบับที่มี ให้เติมแถวลง REAL_SERVER_DIVERGENCE.tsv
  (ส่งค่ามา ห้ามแก้ไฟล์เอง).

### nonclaims
- ใบนี้พิสูจน์แค่ผู้เล่นคนเดียวที่ต่ออยู่ -- ledger/register เป็น per-session,
  ยังไม่มีใครทดสอบสองผู้เล่นตีมอนสเตอร์ตัวเดียวกันพร้อมกัน.
- ตัวเลขดาเมจที่เห็นมาจากโปรไฟล์ผู้โจมตีสังเคราะห์คงที่ (level 7 / STR 132)
  ไม่ได้อ่านจากสถิติตัวละครจริงของผู้เทส -- ไม่ใช่ตัวเลขของเซิร์ฟเวอร์ต้นฉบับ.
- ค่า CON = 22 ของมอนสเตอร์เป็นค่าที่โครงการนี้ตั้งเอง ไม่มีตารางไหนมีคอลัมน์นี้จริง.
- ใบนี้ไม่ทดสอบว่าซากยังอยู่ทน (ไม่ฟื้น) ข้ามการ reconnect/census rebuild --
  นั่นคือ claim แยก ต้องเปิดใบใหม่ (mob_death.corpse_override ยังไม่มีใครดูบน
  จอจริง).
- ใบนี้ไม่ทดสอบ aggro/threat -- dispatch ส่ง aggro handle เป็น None เสมอในบูตนี้
  มอนสเตอร์จะไม่ตอบโต้.
- ใบนี้ไม่ทดสอบดรอปของ (M5 คนละใบ, คนละ milestone).
- ถ้าไปไม่ถึง/เลือกเป้าไม่ได้เลยตลอด 15 นาที ทั้งที่ 0x201F และตัวสำรอง ⇒ นั่น
  เป็นผลของระยะวาดโมเดลที่ไม่เคยมีใครวัด ไม่ใช่หลักฐานว่า dispatch ใช้ไม่ได้ --
  เขียนเป็น NO-RESULT พร้อมเหตุผล ไม่ใช่ FAIL.
- อนิเมชันตาย _F_DIE_000 ไม่เคยถูกสังเกตมาก่อนในโปรเจกต์นี้ -- ถ้ารอบนี้ก็ไม่เห็น
  อีก ไม่ใช่ผลลบของกลไก (ประตูสถิตของมันไม่เคยพิสูจน์ผลลัพธ์).
- สีของป้ายชื่อบันทึกไว้เฉยๆ ไม่มีการตัดสินสาเหตุ (RE-067 เปิดอยู่).

### result (ผู้เทสกรอก)
```

```

---

### 🆕 RIDER-084-A `OTHER-ACTORS-MUST-STAY-ON-SCREEN-CHECK` — **ข้อสังเกตบังคับ (เพิ่มเติมจาก P1-P5 เดิม ไม่แทนที่) ต่อท้ายใบ `GT-084` · ไม่แก้ objective/pass criteria/nonclaims เดิมแม้แต่ตัวอักษรเดียว**

🔴 **บรรทัดแรก อ่านก่อนทุกบรรทัด:** ริเดอร์นี้ไม่ยกเลิก ไม่แก้ P1-P5 ไม่แก้ objective ไม่แก้ pass criteria สองชั้นเดิมของ GT-084 แม้แต่ตัวอักษรเดียว — มันเป็น **ขั้นสังเกตเพิ่มเติม (บังคับทำ ไม่ใช่ทางเลือก)** ที่ต้องทำคู่กับ step 5-7 เดิมของใบแม่ ผลของริเดอร์นี้ **ไม่ตัดสิน PASS/FAIL ของ GT-084 เอง** — มันเปิดหรือปิดคำถามคนละคำถาม (ดูข้อ 3 ข้างล่าง)

**ทำไมถึงต้องมี — หลักฐานสองชิ้นที่เพิ่งถูกเชื่อมกัน (ที่มา: `notes_to_chief/20260826_1746_LANE-B-URGENT-combat-and-death-frames-may-be-world-wipe-frames-GT-084-is-unblocked.md`):**
`mob_combat.py:937` (`bar_frames`) และ `mob_death.py:856` (`death_frames`, เรียกจาก `dying_frames`/`dead_frames`) ต่างประกอบ `legacy.make_runtime_remote_actors([entry])` — คอลเลกชัน **nonempty หนึ่งรายการพอดี** ไม่ใช่ทั้ง roster (ต่างจาก `field_mobs.py:552` และ `mob_death.py:1349` ที่ส่ง `entries` เต็ม roster). `notes_to_chief/20260826_1017_RE-082-RESULT-OBJECT-REF-IS-ELEMENT-KEY.md` T4 พิสูจน์แล้ว (static) ว่าสำหรับผู้บริโภคคนละตัว (`PickupTerrainThing`) คอลเลกชันรูปทรงเดียวกันนี้ (nonempty, หนึ่งรายการ) อ่านแบบ **replace-by-omission**: key เก่าใด ๆ ที่ไม่อยู่ในรายการใหม่ถูก erase จากมุมมองไคลเอนต์ — ส่วน zero-entry generation เป็น no-op ไม่ล้างอะไร. **ยังไม่มีใครพิสูจน์ว่าเซแมนติกเดียวกันนี้ใช้กับผู้บริโภคที่อ่านเฟรม combat/death จริง** (`GSCN_RunTimeProtocolRes` mask `0x02`, derived-mask `0x08` list) — คำถามนี้เปิดอยู่เป็น **`RE-092` `REMOTE-ACTOR-LIST-CONSUMER-REPLACE-OR-MERGE-001`** (`CLIENT_RE_QUEUE.md`) ยังไม่ปิด. ถ้า `RE-092` ตอบว่า (ก) replace-by-omission และ scope กว้างถึงทั้งฉาก ⇒ **ทุกหมัดและทุกครั้งที่มอนสเตอร์ตายในบูตนี้อาจล้างนักแสดงอื่นบนจอทิ้งโดยไม่มีใครสังเกต** เพราะ P1-P5 เดิมของใบนี้สั่งให้จ้องแค่หลอด/เลข HP ของเป้าหมายเท่านั้น ไม่มีข้อไหนสั่งให้มองที่อื่น

**สิ่งที่ต้องทำเพิ่ม — ทำคู่กับ step 5/6/7 ของใบแม่ ไม่ใช่แทน:**
- `OW1` (คู่กับ step 5, **ก่อน**ดับเบิลคลิกแรก): ก่อนโจมตี ให้กวาดตามองรอบตัวมอนสเตอร์เป้าหมาย (ระยะที่มองเห็นบนจอ ไม่ต้องเดินเพิ่ม) แล้วเขียนบันทึกหนึ่งบรรทัด: มี **นักแสดงอื่น** ที่มองเห็นอยู่บนจอไหมนอกจากตัวละครผู้เล่นเองกับเป้าหมาย — "นักแสดงอื่น" หมายถึง **field-mob ตัวอื่นจาก 13 ตัวในตาราง `field_mob_tables.py`** หรือ **สิ่งใดก็ตามที่มีป้ายชื่อ/โมเดลเคลื่อนไหวอยู่บนจอที่ไม่ใช่ตัวเราเองหรือเป้าหมาย**. ถ้าไม่มีเลย **ให้เขียนออกมาเป็นตัวอักษรว่า "ไม่มีนักแสดงอื่นให้เห็นตั้งแต่ต้น"** ห้ามเว้นว่าง — นี่คือ baseline ที่ทุกการสังเกตถัดไปต้องเทียบกับ
- `OW2` (คู่กับ step 6, **หลังทุกดับเบิลคลิกที่ยิง `MOB_COMBAT_ANNOUNCE`/`MOB_COMBAT_BAR` สำเร็จ**): มองรอบตัวมอนสเตอร์เป้าหมายอีกครั้งด้วยมุมกล้องเดิมหรือใกล้เคียง (คลิกขวาลากได้ถ้าต้องหมุนดู — ปลอดภัยตามที่ NO-CRASH check ของใบแม่ยืนยันไว้ ทิศหันตัวละครไม่ขยับ ไม่ยิงอะไรออกสาย) แล้วเขียนหนึ่งบรรทัดต่อหนึ่งหมัด: นักแสดงอื่นที่บันทึกไว้ใน `OW1` (หรือหมัดก่อนหน้า) **ยังอยู่ครบ / หายไปบางตัว (ระบุว่าตัวไหนถ้าระบุได้) / ไม่มีให้เทียบตั้งแต่ต้น (อ้าง `OW1`)**
- `OW3` (คู่กับ step 7, **ทันทีที่ถึง 0 HP และหลังบรรทัด `MOB_DEATH_DYING`/`MOB_DEATH_DEAD` ขึ้น**): ทำเหมือน `OW2` อีกครั้งหนึ่งรอบ — นี่คือจังหวะที่ RE-082 พิสูจน์ไว้ว่าเสี่ยงที่สุด (เฟรมตายคืออีกจุดที่คอลเลกชันเดียวกันถูกส่ง)
- ไม่ต้องถ่ายภาพนิ่งเพิ่มสำหรับ `OW1`-`OW3` เว้นแต่เห็นนักแสดงหาย — ถ้าเห็นหาย **ต้องถ่ายภาพนิ่ง full-res ทันทีที่เห็น** (ก่อนมันจะกลับมาถ้ามันกลับมา) ตั้งชื่อ `evidence_screens\GT084_RIDERA_OW<n>_ACTORLOST_<yyyyMMdd_HHmmss>.png` + sha256 แล้วอ่าน/บันทึกสีป้ายชื่อของนักแสดงที่เหลือทุกป้ายในภาพนั้นตามกติกาสีป้ายมาตรฐาน (เต็มความละเอียด ห้าม contact sheet/ภาพย่อ/วิดีโอ, "none" เขียนออกมาถ้าไม่มี, ห้ามอนุมานสาเหตุ — `RE-067` เปิดอยู่)

**ถ้าเห็นนักแสดงอื่นหายไปพร้อมหมัดหรือเฟรมตาย:**
นั่นคือ **หลักฐานสนับสนุนสมมติฐาน world-wipe** ที่ `LANE-B` เตือนไว้ (nonempty one-entry generation = replace-by-omission แบบเดียวกับที่ `RE-082` พิสูจน์กับ `PickupTerrainThing`) — 🔴 **ห้ามพับเข้าไปเงียบ ๆ เป็นส่วนหนึ่งของผล PASS/FAIL ของ `GT-084`** เพราะ objective เดิมของ `GT-084` ถามแค่เรื่องดาเมจ/ตายของเป้าหมาย ไม่ได้ถามเรื่องนี้ ⇒ **ให้เขียนเป็น finding แยกของตัวเอง** (จดหมายถึง chief ตามแบบใบอื่น ๆ ในโปรเจกต์ อ้าง `OW1`-`OW3` + ภาพ + sha256 + เวลา) และ **อ้างชื่อ `RE-092`** เป็นใบที่คำตอบสถิตของคำถามนี้ค้างอยู่ (ใบนี้ยืนยัน/ปฏิเสธด้วยชั้น client-observable ในขณะที่ RE-092 ตอบด้วยชั้น static — สองใบคนละชั้นหลักฐาน ห้ามใช้ใบหนึ่งปิดอีกใบ). ถ้าไม่เห็นอะไรหายเลยตลอดรอบ **ก็เป็นผลลบที่มีค่าเท่ากัน** — เขียนว่า `OW1`-`OW3` ทุกจุดตอบ "ยังอยู่ครบ"/"ไม่มีให้เทียบตั้งแต่ต้น" แล้วส่งให้ RE-092 อ้างเป็นหลักฐานเสริมได้ (ไม่ใช่หลักฐานปิดใบ — ใบ static ต้องปิดด้วยหลักฐาน static ของตัวมันเอง).

**nonclaims ของริเดอร์นี้เอง:**
① ไม่อ้างว่า world-wipe เป็นจริง — แค่ทำให้สังเกตได้ถ้ามันเกิด ② ไม่ปิด `RE-092` ด้วยตัวเอง ไม่ว่าผลจะออกทางไหน (ใบ static ปิดด้วยหลักฐาน static เท่านั้น) ③ ไม่เปลี่ยนงบเวลา/ไม่เพิ่มการเดิน/ไม่เพิ่มบูต — ใช้เซสชันเดียวกับใบแม่ทั้งหมด ④ ถ้าไม่มีนักแสดงอื่นให้เห็นเลยตลอดรอบ (บูตนี้อยู่ไกลจุดเกิดมาก field-mob ตัวอื่นอาจอยู่นอกระยะวาด) นั่นเป็น **ข้อจำกัดของสถานที่ ไม่ใช่ผลลบของริเดอร์** — เขียน `OW1: ไม่มีนักแสดงอื่นให้เห็นตั้งแต่ต้น` แล้วปิดริเดอร์ด้วยผลนั้น ไม่ต้องหาทางสร้างนักแสดงเพิ่ม

**— ริเดอร์ต่อท้ายโดย chief cloud · รอบ `3lzfhw` · 2026-08-26 ~19:1x (+07:00) · อ้างอิง `notes_to_chief/20260826_1746_LANE-B-URGENT-combat-and-death-frames-may-be-world-wipe-frames-GT-084-is-unblocked.md` + `RE-092` (`CLIENT_RE_QUEUE.md`)**

🆕 **อัปเดต (chief cloud · รอบ `q4z3vi` · 2026-08-26 ~22:5x (+07:00)):** `RE-092` ปิดแล้ว — คำตอบคือ **(ก) replace-by-omission ยืนยันจริง** (ไม่ใช่ merge) ที่ชั้น static (`notes_to_chief/20260826_2223_RE-092-RESULT-*.md`) พร้อมแก้ objective mask ของใบเดิมจาก `0x08` เป็น `0x02` ที่ถูกต้อง — **สมมติฐาน world-wipe ของ `LANE-B-URGENT` มีฐาน static รองรับแล้วเต็มที่** (ไม่ใช่แค่ความเสี่ยงที่ยังพิสูจน์ไม่ได้อีกต่อไป) ⇒ **`OW1`-`OW3` ข้างบนสำคัญขึ้น ไม่ใช่ทางเลือก** เมื่อรอบ attended ของ `GT-084` เกิดขึ้นจริง ริเดอร์นี้เองยังไม่เปลี่ยนแม้แต่ตัวอักษรเดียวตามกฎ nonclaim ②-③ เดิม — ผล client-observable ยังต้องรอ `OW1`-`OW3` จริงเหมือนเดิม ห้ามอ่าน `RE-092` แทนผลของริเดอร์นี้

🆕 **อัปเดต (chief cloud · รอบ `keen-pasteur-543ds8` R187 · 2026-08-27 ~09:00 (+07:00)) — คำเตือนสำคัญเรื่อง grep token ที่ใบนี้เคยใช้ผิด:** ใบนี้เคยตรวจคอนโซลหา `FIELD_MOB`/`HOSTILE` แล้วเจอ 0 บรรทัด (ดู `notes_to_chief/20260827_0205_GT084-NO-RESULT-*.md`) แต่ป้ายสองตัวนั้น **ไม่เคยมีอยู่จริงบน production path เลย** — เป็นช่องว่างการมองเห็น ไม่ใช่โค้ดไม่ทำงาน สาย B ตรวจสดแล้วยืนยัน (ดู `archive/rounds_2026-08-27_to_28/B_20260827_0805_gt084_roster_override_coverage.md`) ว่า 13/13 identity ของ field-mob roster อยู่ใน census จริง และ chief ต่อสายคอนโซลบรรทัดใหม่ให้แล้วรอบนี้ (`pirate-force-server` commit `dd5c785`): **`runtime.py`** พิมพ์ `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13 missing=none` ทันทีหลัง census ประกอบเสร็จ — **นี่คือ grep token ที่ถูกต้องสำหรับตรวจว่าเฟรม hostile ออกสายจริง** ไม่ใช่ `FIELD_MOB`/`HOSTILE` ⇒ **รอบ attended ถัดไปของ `GT-084` (หรือใบต่อยอด) ต้อง grep หา `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE` แทน** มิฉะนั้นจะอ่านผลผิดซ้ำเหมือนรอบก่อน ยืนยันด้วยบูต headless แล้ว (ก่อนแก้: ไม่มีบรรทัดนี้พิมพ์เลย = ผลลบเดิมของ `GT-084` ซ้ำได้จริง / หลังแก้: `matched=13/13` พิมพ์ทุกครั้งที่ประกอบ census สำเร็จ) — นี่คือ **wire layer เท่านั้น** ยังไม่ตอบว่าไคลเอนต์เรนเดอร์เป็นสีแดง/hostile จริงไหม (คำถามนั้นยังเปิดอยู่ใน `GT-084`/`RIDER-084-A` เดิม)

🆕 **อัปเดต (chief cloud · รอบ `optimistic-mccarthy-ahn7zb` R188 · 2026-08-27 ~11:3x (+07:00)) — `CORE-REQUEST-008` ต่อสายแล้ว: ความเสี่ยง world-wipe ของ `mob_combat.bar_frames`/`mob_death.death_frames` (ที่ริเดอร์นี้เปิดไว้ตั้งแต่แรก) ปิดแล้วที่ชั้น static/wire:** `MOB_COMBAT_BAR`/`MOB_DEATH_DYING`/`MOB_DEATH_DEAD` compose เข้า full census เดียวกับ arrival แล้วทั้งสามจุด (`pirate-force-server@741ab5d`, grep token ใหม่ `MOB_COMBAT_BAR_CENSUS_RECOMPOSE`/`MOB_DEATH_FRAMES_CENSUS_RECOMPOSE`) แทน one-entry frame เดิม พร้อม fail-closed guard (compose ล้มเหลว หรือ scene ไม่ตรง ⇒ ถอยไป one-entry frame แทนโครง exception/ส่งเฟรมผิดฉาก — พบโดย `pf-adversary` ในรอบเดียวกัน ดู `rounds/R188_*.md`) 🔴 **ริเดอร์นี้เองยังไม่เปลี่ยนแม้แต่ตัวอักษรเดียวตามกฎ nonclaim ②-③ เดิม** — `OW1`-`OW3` ยังเป็นขั้นสังเกตบังคับเหมือนเดิมทุกประการ การแก้นี้ตอบเฉพาะชั้น static/wire ว่าเฟรมที่ส่งออกไม่ใช่ one-entry อีกต่อไป **ไม่ได้ตอบว่าไคลเอนต์จริงเห็นอะไร** — ห้ามอ่านว่า client-observable risk ถูกปิดแล้ว ผลจริงยังต้องรอ `OW1`-`OW3` เหมือนเดิมทุกประการ



---


## GT-084-R2 HOSTILE-PAIR-VISIBLE-001: รอบสองของ GT-084 -- คู่ faction (1,6) ที่ผู้เล่นได้ครึ่งของตัวเองแล้ว ทำให้ Tornado Eagle ขึ้นศัตรูจริงบนจอไหม (~~ชื่อแดง + แผงเป้าแดง~~ [UPDATE 2026-08-27T17:34+07:00 LANE-B ต่อยอด PANYA-REFERENCE 16:35+07:00: เกณฑ์สีที่ถูกต้องคือ **ส้ม (ยังไม่ aggro) → แดงเข้ม (aggro) → เทา (ตาย)**, ไม่ใช่ "แดง" เฉยๆ] + แผงเป้า) บนบูตไร้แฟล็ก -- ก่อนจะไปถึงเรื่องตี  [🟡 **RESULT -- claim หลัก (hostile ที่ตาเห็น) PASS ด้วยหลักฐานพฤติกรรม (ขอบแดง+ลูกศรแดงคู่, ดับเบิลคลิกตีติดจริง) แต่ไม่ใช่สีตามใบเป๊ะ (ชื่อชมพู/magenta ตลอด ไม่ใช่ส้ม→แดงเข้ม→เทาตามลำดับสถานะจริง, ไม่มีแผงเป้า) -- ผลต่อขั้นตี-ตาย: ดู GT-084 -- รายละเอียด notes_to_chief/20260827_1620_GT084R2-RESULT-*.md, RE-107/RE-108 ปิดแล้ว (bounded negative), RE-109 เปิดใหม่ถามครบ 6 สี, สถานะสุดท้าย (PASS/MIXED) รอ chief ตั้ง**]

🆕 **RIDER-084-B (เจ้าของใบ LANE-B · รอบ `szdkgs` · 2026-08-29 ~01:0x +07:00) — ตัวตนของเป้าหมายในใบนี้ถูกแก้แล้วครึ่งหนึ่ง ไม่แก้ objective/เกณฑ์ผ่านของใบแม่แม้แต่ตัวอักษรเดียว**
รอบนี้ `field_mob_tables.py` ถูก regenerate ผ่าน crosswalk ของ `RE-128` (`SCENE_NAME.n_CLINE_TYPE` → `CLINE.n_LEADER_BK1`) ผลที่ผู้เทสจะเห็นต่างจากรอบก่อน:
- **สี่ placement 103/105/107/109** เมื่อวานส่งเป็น `Mutant Green Eagle` (เลขชุด 97) วันนี้ส่งเป็น **`n_ID 916 Training Iron Man`** avatar `M016_000_000_N` (เมื่อวานคือ `M011_000_002_SP3`) — **ของจริงตามตาราง ไม่ใช่การประกอบเอง** และเป็นตัวที่ `COO-DECISION widen-death-scope-916-training-iron-man 2026-08-27T09:55+07:00` อนุญาตให้ฆ่าไว้แล้ว
- **อีกเก้า placement (รวม P30 `0x201F` เป้าหมายของใบนี้)** ยังส่งไบต์เดิมทุกอย่างในรอบนี้ ⇒ **ใบนี้ยังรันได้เหมือนเดิม ไม่ต้องแก้ขั้นตอน** 🔴 แต่ให้รู้ไว้ว่า **ชื่อ "Tornado Eagle" ของ P30 ถูกพิสูจน์แล้วว่าไม่ใช่ตัวตนจริงของ placement นั้น** (crosswalk บอกว่า Mob-Set 31 = `n_ID 248 Da Vinci`) การย้ายอีกเก้าแถวไปตัวตนจริงเป็นงานรอบถัดไปของสาย B (ประมาณ 840 pin)
- 🔴 **สิ่งที่ควรจดเพิ่มถ้าได้นั่งรอบนี้ (ไม่ใช่เกณฑ์ผ่าน):** ที่พิกัดราว (11789..15649, 9317..9364, 2200) มีหุ่นสี่ตัว — **หน้าตาเปลี่ยนจากนกเป็นหุ่นเหล็กหรือไม่** และชื่อใต้ตัวอ่านว่า `Training Iron Man` หรือไม่ · ตอบ "เปลี่ยน/ไม่เปลี่ยน" พอ ไม่ต้องตีความ

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md. เลขสูงสุด ณ เวลาเขียนใบนี้: GT-099 / RE-098.
> 🔢 **ใบนี้ไม่กินเลขคิวใหม่** -- เป็น **รอบที่สองของ GT-084** เลนเดียวกัน (มอนสเตอร์เป้าหมายเดียวกัน 0x201F
> Tornado Eagle, บูตไร้แฟล็กเดียวกัน, ท่าเดียวกับ GT-030-R3 ที่อยู่ใต้เลขเดิม) ตามคำสั่งเจ้าของ (Panya)
> 2026-08-27 09:15 ผ่าน notes_to_chief/20260827_0915_PANYA-CHASE-owner-decisions-...md ข้อ ①.2 ประโยคสุดท้าย,
> และ notes_to_chief/20260827_0520_ATTENDED-URGENT-R187-...md ง§④ ข้อ 3-4. ใบ `GT-084` เดิม (รวม
> `RIDER-084-A` และทุกอัปเดตต่อท้ายถึง R188) **ยังอยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ** -- ใบนี้ยืน
> อยู่บนผลของมัน ไม่ใช่ใบแทน.

🆕 **ความคืบหน้า world-wipe (ยังไม่ใช่ "พร้อม") — LANE-B รอบ `rbuta4` 2026-08-28T18:1x+07:00:**
เพิ่ม headless proof `pirate-force-server/tests/test_world_wipe_headless_proof.py` — บูตไร้แฟล็ก
→ โดนตี 1 → ตาย 1 → เฟรม `MOB_COMBAT_BAR`/`MOB_DEATH_DYING`/`MOB_DEATH_DEAD` ยังมีครบทุกตัวที่
census ตอน arrival ส่งไป **วัดจาก `frame` ซึ่งเป็นบัฟเฟอร์ที่ `v141:7755 c.sendall(out_frame)` ส่งออกจริง**
(ไม่ใช่ `pc` ซึ่งไคลเอนต์ไม่เคยได้รับ) เทียบกับเฟรม arrival ของเซสชันเดียวกัน
🔴 **แก้คำผิดของอัปเดตฉบับแรก (เขียนไว้ 17:49 น. ถอนแล้ว):** ฉบับแรกเขียนว่า "grep token เชื่อได้แล้ว
ผู้เทส grep ได้โดยไม่ต้องกลัว" — **ผิด และถอนคำนั้น** `pf-adversary` สร้าง regression จริงที่ทำให้เทสทั้ง 19 ใบ
เขียว ในขณะที่เฟรมที่ออกสายมี body เดียว (เฟรมของ `MOB_DEATH_*` ยังผูกกับ `death_step` ตัวเก่าขณะที่ `pc`
ถูกอัปเดตแล้ว) เพราะเทสฉบับแรกวัด `pc` ไม่ใช่ `frame` แก้แล้วในรอบเดียวกันนี้
🔴 **ผู้เทส: ยังห้ามใช้บรรทัด `*_CENSUS_RECOMPOSE actor_count=115` เป็นหลักฐานเดี่ยว** มันพิมพ์
`world_census_actor_count` ที่อ่านจาก session state **ก่อน** ประกอบเฟรม ⇒ เป็น **INPUT ไม่ใช่ผลลัพธ์**
บรรทัดนี้ยืนยันได้แค่ว่า "เส้นทาง recompose ถูกเดิน" ไม่ได้ยืนยันว่า "เฟรมมีครบ 115" — หลักฐานจำนวนตัวจริง
เป็นชั้น headless ในเทส ไม่ใช่ชั้นคอนโซล
🔴 **นี่คือชั้น wire เท่านั้น ไม่ใช่ชั้นจอ** — `RIDER-084-A` `OW1`-`OW3` **ยังเป็นขั้นสังเกตบังคับเหมือนเดิมทุก
ตัวอักษร** ห้ามอ่านบรรทัดนี้ว่า world-wipe ปิดแล้วบนจอ ใบนี้และริเดอร์ไม่ถูกแก้แม้แต่ตัวอักษรเดียวจากอัปเดตนี้
🔴 **addendum-G ยัง "ไม่ปิด"** — `pf-adversary` ยก 14 ข้อ ระดับ critical 2 ข้อ รอบนี้แก้ที่โค้ดแล้ว
แต่การประกาศปิดเกณฑ์เป็นของ COO ไม่ใช่ของสาย B ⇒ ดู `archive/rounds_2026-08-27_to_28/B_20260828_1749_world_wipe_headless_proof.md` ก่อนตัดสิน

🆕 **RIDER-084-C (เจ้าของใบ LANE-B · รอบ `sn42vo` · 2026-08-29T03:53+07:00) — เป้าหมายของใบนี้ถูกถอนออกจาก roster แล้ว · ไม่แก้ objective/เกณฑ์ผ่านของใบแม่แม้แต่ตัวอักษรเดียว**
🔴 **อ่านก่อนบูต:** `pirate-force-server#221` (merged 2026-08-29T03:32+07:00) ถอนเก้าแถวเลขชุดออกตาม COO-DECISION 00:41 ⇒ **`0x201F` (P30 "Tornado Eagle") ไม่อยู่ใน roster อีกแล้ว** ข้อความใน `RIDER-084-B` ที่ว่า "อีกเก้า placement (รวม P30 `0x201F`) ยังส่งไบต์เดิม" ~~เป็นจริง ณ รอบ `szdkgs`~~ **หมดอายุแล้ว ณ รอบนี้** (ขีดฆ่า ไม่ลบ ตามกติกา)
วัดสดบน main รอบนี้ (`field_mobs.load_roster()`): roster = **4 แถว** ทั้งหมด `n_ID 916 Training Iron Man` avatar `M016_000_000_N` · placement **103/105/107/109** ⇒ actor identity **`0x2068` `0x206A` `0x206C` `0x206E`** · level 100 · HP 198125 · `rank=0` · `ai_combat=0` · `n_DROPS_*` = 0 ทั้งสามคอลัมน์ · scene bg0001
⇒ **ใบนี้รันตามขั้นตอนเดิมไม่ได้** เพราะไม่มีเป้าหมายเดิมให้คลิก · ตัวที่ยืนอยู่จริงคือหุ่นสี่ตัว และ COO เคาะไว้แล้วว่ามันคือ **หุ่นซ้อม ไม่ใช่มอนสเตอร์ของฉากนี้** (`rank=0`, `ai_combat=0`) 🔴 **คำถามหลักของใบนี้ (ส้ม→แดงเข้ม→เทา) อาจถามกับหุ่นซ้อมไม่ได้ตั้งแต่ต้น** — สถานะใบและเป้าหมายทดแทนเป็นของ chief/COO ตั้ง ไม่ใช่ของสาย B ตั้งเอง สาย B รายงานข้อเท็จจริงเท่านั้น

🔴 **เกณฑ์ addendum-G ข้อ "census หลังเหตุการณ์ยัง 115/115 (grep คอนโซลได้)" — สาย B รายงานว่า *เขียนแบบนี้แล้วปิดไม่ได้* ไม่ใช่ว่ายังไม่ได้ทำ**
สองเหตุผล วัดแล้วทั้งคู่:
1. **เลข 115 ไม่ใช่เลขของบูตไร้แฟล็ก** — 115 คือขนาดตาราง placement ที่แช่ไว้ · สิ่งที่บูตไร้แฟล็ก **ประกอบได้จริง** คือ **108** (`SHIPPED_CENSUS_COUNT`, `tests/test_world_wipe_headless_proof.py:156`, ที่มา RE-128/CLINE) ⇒ เกณฑ์ที่ถูกคือ **108/108**
2. **ชั้นคอนโซลตอบคำถามนี้ไม่ได้เลย** — บรรทัด `*_CENSUS_RECOMPOSE actor_count=N` พิมพ์ `world_census_actor_count` ที่อ่านจาก session state **ก่อน** ประกอบเฟรม ⇒ เป็น **INPUT ไม่ใช่ผลลัพธ์หลังเหตุการณ์** (รอบ `rbuta4` ถอนคำอ้างนี้ไปแล้วเอง) มัน grep ได้ แต่ยืนยันได้แค่ "เส้นทาง recompose ถูกเดิน"
⇒ **สิ่งที่จะปิดเกณฑ์นี้ได้จริง** คือบรรทัดคอนโซลที่นับ **จำนวน body ในเฟรมที่ประกอบเสร็จแล้ว** แล้วพิมพ์หลังประกอบ · จุดพิมพ์อยู่ใน `runtime.py` ซึ่ง **เป็นเขตของ chief** ⇒ สาย B เปิดเป็น CORE-REQUEST ใน body ของ `pirate-force-server#228` แทนการแก้เอง
~~🔴 **สาย B ไม่เขียนบรรทัด "พร้อมสำหรับ GT-084-R2" ในรอบนี้ และจงใจไม่เขียน** — ชั้น wire ปิดแล้วจริง (`test_world_wipe_headless_proof.py` 7 ใบ วัดจาก `frame` ที่ `v141:7755` ส่งออก ไม่ใช่ `pc`) แต่ชั้นที่เกณฑ์ขอ (คอนโซล) ยังไม่มีของให้ grep และเป้าหมายของใบก็เพิ่งหายไป ⇒ เขียน "พร้อม" ตอนนี้คือคำอ้างที่รอบ `rbuta4` เพิ่งถอนไปเอง~~

🆕 **RIDER-084-D (เจ้าของใบ LANE-B · รอบ `z096sw` · 2026-08-29T18:5x+07:00) — ครึ่งคอนโซลของเกณฑ์ addendum-G ปิดแล้ว วัดจริง · ไม่แก้ objective/เกณฑ์ผ่านของใบแม่แม้แต่ตัวอักษรเดียว**

รอบก่อนเขียนไว้เองว่า "สิ่งที่จะปิดเกณฑ์นี้ได้จริงคือบรรทัดคอนโซลที่นับจากเฟรมที่ประกอบเสร็จแล้ว · จุดพิมพ์อยู่ใน `runtime.py` ซึ่งเป็นเขตของ chief" — **ข้อหลังผิด**: กฎบัตรสาย B ข้อ G มอบบล็อก `bar_frames`/`death_frames` ให้สายนี้แก้ได้หนึ่งครั้งเพื่องานนี้โดยตรง ⇒ รอบนี้แก้เองแทนที่จะรอ CORE-REQUEST

**🟢 พร้อมสำหรับ GT-084-R2 — เฉพาะครึ่ง world-wipe ของเกณฑ์ addendum-G** (ไม่ใช่ทั้งใบ ดูข้อจำกัดท้ายบล็อก)

🔴 **อ่านย่อหน้านี้ก่อน — ฉบับแรกของริเดอร์นี้เขียนเกินหลักฐาน และ pf-adversary จับได้ก่อน push**
ฉบับแรกยกบรรทัด `actor_count=108 wire_actors=108` เป็นหลักฐานว่า "โลกรอด" · **นั่นเป็น tautology ไม่ใช่การวัด**:
เมื่อ compose สำเร็จ `wire_actors` เท่ากับ `actor_count` เสมอโดยพีชคณิต (recompose เรียก
`build_world_population(legacy, anchor, count)` ด้วย `count` ตัวเดียวกัน และ `census_order` อ่านตารางนิ่ง
ที่หดไม่ได้) ⇒ มิวแทนต์ที่ **ไม่อ่านสายเลย พิมพ์ input ซ้ำ** เขียวทั้งสวีต
🟢 **สิ่งที่ทำให้บรรทัดนี้มีค่าจริงคือของที่แก้หลังจากนั้น** ไม่ใช่เลข 108/108:
บรรทัดถูกย้ายออกมา **นอก `if` และนอก `try`** ⇒ สองเส้นทาง fallback (compose โยน / ไม่มี anchor ซึ่ง
คอมเมนต์ใน `runtime.py` เองบอกว่า "เกิดในการเล่นปกติ") **เคยส่งเฟรม one-entry ออกสาย = ตัว world wipe เอง
แล้วคอนโซลเงียบสนิท** — นั่นคือสภาพเดียวที่ผู้เทสต้องการบรรทัดที่สุด และเป็นสภาพเดียวที่ไม่มีบรรทัด

grep token ที่ผู้เทสต้องใช้ (ASCII ล้วน · cp874 ปลอดภัย):

```
MOB_COMBAT_BAR_CENSUS_RECOMPOSE        actor_count=<input>  wire_actors=<measured>  target=0x....
MOB_DEATH_FRAMES_CENSUS_RECOMPOSE_DYING actor_count=<input> wire_actors=<measured>  target=0x....
MOB_DEATH_FRAMES_CENSUS_RECOMPOSE       actor_count=<input> wire_actors=<measured>  target=0x....
```

🔴 **อ่านสองฟิลด์นี้ให้ต่างกัน ไม่ใช่ฟิลด์เดียวกันเขียนสองครั้ง**
- `actor_count=` **ของเดิม ความหมายเดิม ไม่เปลี่ยน** = `world_census_actor_count` อ่านจาก session state **ก่อน** ประกอบเฟรม (INPUT) · เก็บชื่อเดิมไว้เพราะใบนี้กับ runbook สั่ง grep คำนี้อยู่แล้ว การเปลี่ยนความหมายเงียบ ๆ แย่กว่าดีเฟกต์ที่กำลังแก้
- `wire_actors=` **ของใหม่รอบนี้** = จำนวนที่ **collection header ของเฟรมที่ส่งออกจริงประกาศ** อ่านหลังประกอบ ด้วย `world_population_handoff.wire_count_of` ตัวเดียวกับที่ headless proof เรียก และ**อ่านต่อเมื่อ `frame == legacy.frame_pc(pc)` ผ่านแล้วเท่านั้น**
- ถ้าอ่านไม่ได้จะพิมพ์ `wire_actors=unmeasured reason=<ชื่อ>` **ไม่เคยพิมพ์ตัวเลขที่เดาไว้** (`frame_is_not_this_pc` / `header_unreadable` / `legacy_refused` / `pc_not_bytes` / `frame_not_bytes`)

**วัดจริงบนบูตไร้แฟล็ก รอบนี้** (สคริปต์ขับ harness เดียวกับ `test_world_wipe_headless_proof.py` · ไม่ใช่ค่าที่เทสคำนวณเอง):

```
arrival        : WORLD_CENSUS assembled=108/115 wire=108 ... (collection header ประกาศ 108)

--- บูตปกติ compose สำเร็จ (โลกรอด) ---
ตี 1 ครั้ง      : MOB_COMBAT_BAR_CENSUS_RECOMPOSE        actor_count=108 wire_actors=108 target=0x2068
ตาย 1 ตัว      : MOB_DEATH_FRAMES_CENSUS_RECOMPOSE_DYING actor_count=108 wire_actors=108 target=0x2068
                MOB_DEATH_FRAMES_CENSUS_RECOMPOSE       actor_count=108 wire_actors=108 target=0x2068
compose refusals/skips : ไม่มีสักรายการ

--- 🔴 fallback: compose ถูกปฏิเสธ = world wipe จริง (เมื่อก่อนบรรทัดนี้ไม่มีเลย) ---
                MOB_DEATH_FRAMES_CENSUS_RECOMPOSE_DYING actor_count=108 wire_actors=1 target=0x2068
                MOB_DEATH_FRAMES_CENSUS_RECOMPOSE       actor_count=108 wire_actors=1 target=0x2068
events         : mob_death_frames_census_compose_refused_RuntimeError
```

⇒ **นี่คือสิ่งที่ผู้เทสต้องอ่านจริง ๆ:** ไม่ใช่ "เห็น 108/108 แล้วสบายใจ" แต่คือ
**`wire_actors` ต่างจาก `actor_count` เมื่อไหร่ = โลกถูกล้างเมื่อนั้น** · `108 vs 1` คือหน้าตาของ world wipe
🔴 `state.events` **ไม่เคยถูกพิมพ์ที่ไหนเลยในทรีนี้** (append 276 จุด · print 0 จุด) ⇒ ก่อนรอบนี้
สัญญาณเดียวที่ผู้เทสมีในสภาพนั้นคือ **การไม่มีบรรทัด** ซึ่งเป็นความผิดพลาดที่ `GT-084` เคยทำมาแล้วครั้งหนึ่ง

⇒ **เกณฑ์ที่ถูกคือ 108/108 ไม่ใช่ 115/115** (ข้อ 1 ของบล็อกบนยังคงเดิมทุกตัวอักษร: 115 คือขนาดตารางที่แช่ไว้ · 108 คือสิ่งที่บูตไร้แฟล็กประกอบได้จริง)

🔴 **สี่ข้อที่บรรทัดนี้ยังไม่ปิด และห้ามอ่านว่าปิด**
1. **ตอน compose สำเร็จ สองเลขนี้ต่างกันไม่ได้** — มันเป็นเลขเดียวกันโดยพีชคณิต ⇒ `108/108`
   ยืนยันได้แค่ "เส้นทางเดินและเฟรมที่ส่งคือเฟรมของ pc นั้น" **ห้ามอ่านว่า "นับ body แล้วครบ"**
   ค่าของบรรทัดนี้อยู่ที่เคส fallback ล้วน ๆ
2. **`wire_actors` คือจำนวนที่ header ประกาศ ไม่ใช่จำนวน body ที่นับได้** — เฟรมที่ประกาศ 108 แต่ใส่มา 12 ตัวจะพิมพ์ `wire_actors=108` และเป็น world wipe (วัดแล้วโดย pf-adversary: ตัด body เหลือ 12 จาก 108 → บรรทัดยังพิมพ์ 108) · คนที่เห็นเรื่องนั้นคือชั้น headless (`test_world_wipe_headless_proof.py` นับ occurrence ต่อ identity) ซึ่ง**ยังอยู่ครบทุกใบ ไม่ถูกแทนที่**
3. **บนบูต GM ที่มี diag object สองเลขจะไม่เท่ากันโดยถูกต้อง** — วัดแล้ว: `actor_count=108 wire_actors=113` เพราะ diag object ห้าตัวถูก append เข้า collection ⇒ **`wire_actors` มากกว่า = ปกติบนบูต GM · `wire_actors` น้อยกว่า = wipe** บรรทัดไม่มีฟิลด์แยกสองกรณีนี้ให้ ต้องรู้จากบูตที่ใช้
4. **ใบ `GT-084-R2` ยังไม่มีเป้าหมายให้คลิก** — `RIDER-084-C` ข้างบนยังคงเดิม: `0x201F` ไม่อยู่ใน roster และที่ยืนอยู่คือหุ่นซ้อมสี่ตัว · การตั้งเป้าหมายทดแทน/สถานะใบเป็นของ chief/COO ⇒ "พร้อม" ข้างบนคือ **พร้อมของเกณฑ์ addendum-G เท่านั้น** ไม่ใช่ "ใบนี้รันได้แล้ว"

โค้ด: `src/pirateforce_foundation/mob_census_wire_count.py` (โมดูลใหม่ของสาย B · ไม่มีแฟล็ก · `production_allowed = True` · ไม่โยนเข้า dispatch เด็ดขาด) · `tests/test_mob_census_wire_count.py` · จุดพิมพ์ใน `runtime.py` (การแก้ครั้งเดียวที่ข้อ G สงวนไว้ให้สายนี้)


🆕 **RIDER-084-E (เจ้าของใบ LANE-B · รอบ `jop8ph` · 2026-08-29T19:5x+07:00) — ฟิลด์ใหม่บนบรรทัดที่ผู้เทส grep อยู่แล้ว · ไม่แก้ objective/เกณฑ์ผ่าน/nonclaims ของใบแม่แม้แต่ตัวอักษรเดียว**

บรรทัด `MOB_CENSUS_HOSTILITY` ได้ฟิลด์ท้ายสุดเพิ่มหนึ่งตัว: `ledger=<state>`
(ฟิลด์เดิมทุกตัวอยู่ที่เดิม ลำดับเดิม ⇒ การ grep หา `MOB_CENSUS_HOSTILITY` ยังแมตช์เหมือนเดิม)

```
MOB_CENSUS_HOSTILITY scene_id=.. scene=.. roster=.. backed=.. unbacked=.. refused=.. override=.. ledger=<state>
```

🔴 **สิ่งที่ผู้เทสต้องอ่านให้ถูก:**
- `ledger=not_reported` = **จุดเรียกไม่ได้ส่ง ledger ให้บรรทัดนี้** ไม่ใช่ "ไม่มี ledger"
  **นี่คือสิ่งที่บูตวันนี้จะพิมพ์** จนกว่า chief จะต่อสองคีย์เวิร์ด (ดูจดหมาย `20260829_1955_LANE-B-CORE-REQUEST-*`)
- `ledger=same_scene` = ledger ถูกใช้จริง ⇒ **มอนที่บาดเจ็บจะถูกส่งซ้ำด้วยเลือดที่เหลือจริง**
- `ledger=other_scene` / `unscoped_incomplete` / `same_scene_incomplete` = **ถูกปฏิเสธ**
  ⇒ census ประกอบตามปกติ ไบต์เท่ากับตอนไม่ส่ง ledger ⇒ **มอนบาดเจ็บกลับมาเลือดเต็ม**
  (นี่ไม่ใช่ error และไม่ทำให้บูตล้ม — เป็นสภาพที่มีชื่อ)
- `ledger=absent` = ผู้เรียกส่ง `None` มาเอง · `ledger=ledger_unreadable` = ของที่ส่งมาไม่ใช่ ledger

บรรทัดละเอียดสำหรับตอนอยากรู้ว่าทำไม (พิมพ์เมื่อจุดเรียกเรียก `describe_ledger_admission`):
```
MOB_LEDGER_ADMISSION scene_id=.. scene=.. ledger_scene=.. state=.. admitted=yes|no covered=N/M missing=.. vacuous=yes|no
```
`covered=N/M` คือครึ่งที่ **วัด** (`state=` คือครึ่งที่ **ตัดสิน**) · `missing=not_measured`
แปลว่าไม่มีการอ่าน ledger เลย ไม่ใช่ "ไม่ขาดอะไร"

🔴 **ริเดอร์นี้ไม่อ้างอะไรที่ชั้นจอ และไม่เปลี่ยนไบต์บนบูตวันนี้** — สองคีย์เวิร์ดที่ทำให้มันเปลี่ยน
อยู่ใน `runtime.py` (เขตของ chief) และยังไม่ต่อ · `RIDER-084-A` `OW1`-`OW3` ยังบังคับเหมือนเดิมทุกข้อ

โค้ด: `src/pirateforce_foundation/mob_ledger_admission.py` (โมดูลใหม่ของสาย B · ไม่มีแฟล็ก · `production_allowed = True` · ไม่โยนเข้า dispatch เด็ดขาด) · `tests/test_mob_ledger_admission.py`


### ที่มา -- สิ่งที่เปลี่ยนตั้งแต่รอบแรกของ GT-084 (อ่านก่อนบูต ห้าม re-derive ระหว่างรอบ)
รอบแรกของ `GT-084` (อ่านผลใน `notes_to_chief/20260827_0205_GT084-NO-RESULT-*.md`, ตีความใหม่โดย
`notes_to_chief/20260827_0520_ATTENDED-URGENT-R187-*.md`) เห็น Tornado Eagle เป็น NPC ธรรมดา -- ไม่มีชื่อแดง
ไม่มีขอบแดง แผงเป้าไม่แดง -- และ `ActionVital` ที่ยิงมี target qword = 0 ทั้งหมด ไม่ใช่เพราะ dispatch ใช้ไม่ได้
แต่เพราะคู่ faction ที่ไคลเอนต์เห็นคือ `(0, 6)` = คู่ neutral ที่ทีมพิสูจน์ไว้แล้วเมื่อ 15 ส.ค. -- ผู้เล่นออกไปด้วย
`basic_faction = 0` เสมอบนเส้นทางไร้แฟล็ก (จุดเดียวที่เคยส่ง `basic_faction = PLAYER_PAIR_FACTION (1)` คือ
`_npc_hostile_start_game_response`, `runtime.py:4478`, อยู่ใต้เกท `if npc_hostile_hypothesis_scenario is not
None:` ที่ `runtime.py:4472` -- ต้องมีแฟล็กเท่านั้น).

รอบนี้ (R190, session `3t3klq`) chief ต่อสาย `basic_faction=1` เข้ากับ StartGame ของผู้เล่นเอง**บนเส้นทางไร้
แฟล็ก** (`pirate-force-server` commit `e38e575`, `src/pirateforce_foundation/runtime.py`) -- ก่อนหน้านี้มีแค่
ครึ่งของมอนสเตอร์เองที่ถูกส่ง (ต่อสายไว้แล้วรอบก่อน) ไม่เคยมีครึ่งของผู้เล่นเลยบนบูต production. หลักฐานชั้น
wire/DB ว่าตอนนี้เกิดขึ้นจริง: บูต headless แล้ว grep คอนโซลหาบรรทัด

```
PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game
```

(พิมพ์หนึ่งครั้งต่อการ compose StartGame สำเร็จหนึ่งครั้ง บนบูตไร้แฟล็กจริง -- ไม่มี `--*-scenario` ตัวใดเลย
ทำงานอยู่). **ข้อนี้ยังไม่เคยถูกพิสูจน์ที่ชั้น client-observable -- ไม่มีใครดูจอ GameClient จริงที่มีการแก้นี้ทำงาน
อยู่มาก่อน** -- นี่คือสิ่งเดียวที่ใบ `GT-084-R2` นี้เปิดมาตอบ.

### objective (claim เดียว)
เมื่อผู้เล่นล็อกอินบนบูตไร้แฟล็กที่มี commit `e38e575` (StartGame ของผู้เล่นเองพก `basic_faction=1`) ครึ่งที่
หายไปของคู่ faction ทำให้ไคลเอนต์**ปฏิบัติกับ Tornado Eagle เป็นศัตรูจริงตั้งแต่ก่อนโจมตี**หรือไม่ -- วัดด้วย
เกณฑ์ชั้นจอข้อแรกตามคำสั่งเจ้าของ 2026-08-27 09:15: **ชื่อ Tornado Eagle เป็นสีแดง + แผงเป้าแดง**. นี่คือ
ประตูบังคับ (gate) ของใบนี้เอง ไม่ใช่ทางเลือก: **ถ้าไม่แดง ห้ามโจมตี จบรอบตรงนั้น** (0520 §④ ข้อ 3, คำต่อคำ).
ถ้าแดง ผู้เทสไปต่อกับขั้นโจมตี-ตาย โดยใช้ P1-P5, ขั้นตอน 6-8, เกณฑ์ผ่านสองชั้น และ `RIDER-084-A` (OW1-OW3)
ของใบ `GT-084` เดิม**ทุกตัวอักษร** -- ใบนี้ไม่เขียนซ้ำ อ้างอิงเท่านั้น. ผลของขั้นโจมตี (ถ้าไปถึง) เป็นผลต่อของ
`GT-084` เดิม ไม่ใช่ claim ใหม่ของใบนี้ -- claim เดียวของ `GT-084-R2` คือคำถามข้อแรก (ความเป็นศัตรูที่ตาเห็น).

### ก่อนบูต -- สองด่าน (เพิ่มด่านตรวจ e38e575 เหนือด่านเดิมของ GT-084)
ด่าน 1 -- resolve commit เขียว:
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
exit 0 + `BOOT_COMMIT: <sha>` เท่านั้นถึงบูตได้. แล้วยืนยันว่า `<sha>` สืบทอดจากคอมมิตที่มีการแก้จริง:
```
git merge-base --is-ancestor e38e575 <sha> && echo E38E575_ANCESTOR_OK
```
ไม่พิมพ์ `E38E575_ANCESTOR_OK` = **BLOCKED** -- คอมมิตที่บูตไม่มีการแก้นี้ ห้ามบูต ห้ามตีความว่าเป็นผลลบของ
ใบนี้ ไปทำใบอื่นแล้วรอ merge.

ด่าน 2 -- ยืนยันว่าบรรทัดคอนโซลอยู่นอกเกท hypothesis-only เดิม (ไม่ใช่แค่ว่ามีบรรทัดอยู่ในไฟล์):
```
git grep -n "PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game" <sha> -- src/pirateforce_foundation/runtime.py
git grep -n "_npc_hostile_start_game_response" <sha> -- src/pirateforce_foundation/runtime.py
git grep -n "npc_hostile_hypothesis_scenario is not None" <sha> -- src/pirateforce_foundation/runtime.py
```
เปิดไฟล์จริงที่บรรทัดของ grep แรก อ่านบริบทรอบ ๆ (ก่อน-หลังราว 10 บรรทัด) ด้วยตา ยืนยันว่าบรรทัด print นี้อยู่
**นอก** ฟังก์ชัน `_npc_hostile_start_game_response` และนอกเงื่อนไข `if npc_hostile_hypothesis_scenario is not
None:` -- แปะบริบทที่อ่านลงผล. ถ้าบรรทัด print อยู่*ใน*ฟังก์ชัน/เงื่อนไขนั้น = **BLOCKED**, การแก้ยังไม่ได้ต่อ
สายจริงบนเส้นทางไร้แฟล็ก แม้ grep เจอ string ก็ตาม -- ห้ามบูต แจ้ง chief.

ถ้าขั้นตอนไปถึงการโจมตี (objective ข้อ "ถ้าแดง") ต้องผ่านด่าน 2 เดิมของ `GT-084` ด้วย (ห้าคำสั่ง grep ที่ใบ
`GT-084` เดิมเขียนไว้ใต้หัว "ด่าน 2 -- ยืนยันการต่อสาย") -- **ไม่ทวนคำสั่งซ้ำที่นี่ อ่านจากใบเดิม**.

### db (สำเนาเสมอ ห้ามเปิด canonical, ห้ามแตะ state\play.sqlite3)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-084-R2_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt084r2.sqlite3
```
เทียบ sha256 canonical กับ `CANON_SHA.txt` ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง. สำเนาใหม่ทุกบูต ⇒ ตำแหน่ง
ตัวละครรีเซ็ตกลับจุดเกิดเสมอ (X -8553.9473, Y -2579.6890, Z 186.0).

### server args (เป๊ะ -- เหมือน GT-084 เดิม)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt084r2.sqlite3
```
ห้ามมี `--*-scenario` แม้แต่ตัวเดียว. หลักฐานว่าไม่มีแฟล็กจริง เก็บทันทีหลังเซิร์ฟเวอร์ขึ้น แปะทั้งบรรทัดลงผล:
```
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List
```

### steps (คลิกต่อคลิก -- อัดวิดีโอตลอดช่วงถือ LOCK_GAME)
ก่อนเริ่ม: ถือ LOCK_GAME, จด boot stamp (+07:00, ต้องไม่เก่ากว่า 420 นาทีตอนรัน teardown), เทียบ sha canonical,
copy DB สองใบตามบล็อก db, เตรียม teardown จาก `TEMPLATE_teardown_generic.ps1`.

1. สตาร์ตเซิร์ฟเวอร์ก่อนเสมอ (พอร์ต 10188/10189 = 0 established ก่อนเปิด client). client ที่บูตโดยไม่มี
   เซิร์ฟเวอร์ตายเองใน ~3.5 นาที. ถ้าเพิ่งฆ่า client กลางคันในรอบก่อน ต้อง restart server ก่อนเปิด client ใหม่
   เสมอ (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่ "connecting" ตลอดกาล).
2. เปิด client -> เลือกเซิร์ฟเวอร์ -> dialog PVP ปุ่มซ้าย -> หน้าเลือกตัวละคร -> เลือกช่องแรก -> ปุ่มกลางสุด
   จาก 5 ปุ่มแถวล่าง = เข้าเกม (ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด). เริ่มอัดวิดีโอต่อเนื่องก่อนกดเข้าเกม.
3. T0 -- เห็น HP bar/minimap/ชื่อแมพครบ. จด HUD X/Y. คลิกขวาค้างลากกวาดกล้อง 360 องศาหนึ่งรอบ = ตัวเช็ค
   NO-CRASH เดียวที่ใบนี้ยอมรับ (หมุน**กล้อง**เท่านั้น ทิศหันตัวละครไม่ขยับ ไม่ยิงอะไรออกสาย -- ห้ามใช้ Q/E
   เป็นตัวเช็คนี้เด็ดขาด).
4. เดินไปทาง (1747.5244, -7837.6978, 931.0413) โดยอ่าน HUD X/Y เทียบทุกช่วง (W/A/S/D และ Q/E ยิง
   TargetPosVital ทุกครั้งที่ขยับ/หันตัว -- คาดหมายและไม่ใช่ความเสี่ยงของใบนี้). งบเวลาเดินทาง 15 นาที. ถ้าครบ
   15 นาทีแล้วยังไม่เห็น/เลือกโมเดล 0x201F ได้ ให้ล้มเลิกเป้าหมาย 0x201F แล้วเดินไปหา field-mob ตัวอื่นที่ใกล้
   ที่สุดจาก 13 ตัวในตาราง `field_mob_tables.py` แทน (ท่าเดียวกับ GT-084 เดิม) -- จดในผลว่าใช้ตัวไหนและทำไม.
5. **ประตูบังคับของใบนี้ (ทำก่อนคลิกใด ๆ ที่จะโจมตี):**
   a. เดินเข้าใกล้จนเห็นโมเดลและป้ายชื่อลอยหัวชัดเจนอ่านได้.
   b. ถ่ายภาพนิ่ง full-res ของป้ายชื่อ **ก่อน**คลิกอะไรทั้งสิ้น (baseline).
   c. single-click โมเดลหนึ่งครั้ง (คลิกเดียวเปิดแผงเป้าได้ตามที่ยืนยันแล้วที่ GT-045 v3) -- **ห้ามดับเบิลคลิก
      ในขั้นนี้**.
   d. ถ่ายภาพนิ่ง full-res ของแผงเป้า.
   e. บันทึกสีของป้ายชื่อและสี/สถานะของแผงเป้าตามที่เห็นจริง ตามกติกาสีป้ายมาตรฐานของโปรเจกต์: หนึ่งบรรทัด
      ต่อหนึ่งป้ายต่อหนึ่งภาพ, เขียน "none" ออกมาถ้าไม่มี (ห้ามเว้นว่าง), อ่านจากภาพนิ่ง full-res เท่านั้น
      (ห้าม contact sheet/ภาพย่อ/วิดีโอ). ถ้าต่างจากภาพเซิร์ฟเวอร์ต้นฉบับ เติมแถวลง `REAL_SERVER_DIVERGENCE.tsv`.
   f. **เงื่อนไขหยุด (บังคับตามคำสั่งเจ้าของ):** ถ้าป้ายชื่อ**ไม่แดง** หรือแผงเป้า**ไม่แดง/ไม่ใช่สไตล์ศัตรู** ⇒
      **ห้ามดับเบิลคลิกโจมตี** ห้ามไปต่อ -- ข้ามไปขั้นปิดฉาก (ขั้น 7). นี่คือจบรอบของใบนี้แล้ว และเป็นผลลบเต็ม
      รูปที่มีค่า ไม่ใช่ความล้มเหลว.
   g. ถ้าทั้งป้ายชื่อและแผงเป้าแดงทั้งคู่: claim เดียวของใบนี้ (ประตูข้อแรก) ผ่าน. ผู้เทส**อาจ**ไปต่อในเซสชัน
      เดียวกันด้วยขั้นตอน 6-8 ของใบ `GT-084` เดิม**ทุกตัวอักษร** (ดับเบิลคลิกโจมตี, จดคอนโซล, จดเลขดาเมจ/หลอด
      HP, เกณฑ์หยุดของ `GT-084` เดิม) รวมถึงทำ `RIDER-084-A` OW1-OW3 คู่กับทุกขั้นตอนโจมตีตามที่ริเดอร์นั้น
      กำหนด -- **ไม่ทวนคำสั่งซ้ำที่นี่ อ่านจากใบ `GT-084` เดิม** บันทึกผลของส่วนนี้แยกหัวข้อชัดเจนในผลของใบนี้
      ว่าเป็น "ผลต่อของ GT-084" ไม่ใช่ผลของ objective ใบนี้เอง.
6. (เฉพาะถ้าเข้าขั้น 5g) ทำตามขั้นตอน 6-8 ของใบ `GT-084` เดิมต่อ.
7. ปิดฉาก: NO-CRASH check ด้วยคลิกขวาลากอีกครั้ง. ออกเกม. teardown ตาม `TEMPLATE_teardown_generic.ps1`
   (ภายใน 420 นาทีจาก boot stamp). เทียบ sha canonical รอบสุดท้าย.

### pass criteria (สองชั้น แยกกันเสมอ ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)

ชั้น wire/DB (อ่านจาก server console ล้วน ๆ ไม่ต้องพึ่งสิ่งที่เห็นบนจอ):
- หลักฐานบูตไร้แฟล็กจริง (`Get-CimInstance` command line ไม่มี `--*-scenario`).
- คอนโซลพิมพ์บรรทัด `PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` อย่างน้อยหนึ่งครั้ง โดย
  เวลาที่พิมพ์สัมพันธ์กับช่วงที่ผู้เทสกด "เข้าเกม" จริง (ไม่ใช่แค่เจอในรอบ headless แยกต่างหาก) -- นี่คือ
  หลักฐานว่าการแก้ทำงานจริงสำหรับ*เซสชันนี้*.
- บริบทโค้ดที่อ่านในด่าน 2 ก่อนบูต (บรรทัด print อยู่นอก `_npc_hostile_start_game_response`/นอกเงื่อนไข
  hypothesis) ถูกแปะไว้ในผล.
- ถ้าไปถึงขั้นโจมตี: เกณฑ์ wire/DB เดิมของ `GT-084` ("MOB-COMBAT-001 hit", `MOB_COMBAT_ANNOUNCE`/`BAR`,
  "MOB-DEATH-001 kill" + `MOB_DEATH_DYING`/`MOB_DEATH_DEAD` ถ้าถึง 0 HP) ใช้ทุกตัวอักษรตามใบเดิม -- ไม่ทวนซ้ำ.
- **ผลลบที่มีค่าเท่ากับ PASS:** บูตไร้แฟล็กยืนยันแล้ว (ข้อแรกผ่าน) แต่บรรทัด `PLAYER_FACTION basic_faction=1
  sent_on_flagless_start_game` ไม่ขึ้นเลยสักครั้งตลอดเซสชัน ⇒ การแก้ไม่ได้ต่อสายจริงบน build ที่กำลังบูตอยู่
  (ทั้งที่ผ่านด่าน ancestor check มาแล้ว) -- เขียนเป็นผลลบเต็มรูป, redirect: ตรวจการ deploy/build ซ้ำ, ห้ามอ่าน
  ผลชั้นจอของขั้น 5 เป็นคำตอบของคำถามนี้ (คนละชั้นหลักฐาน).

ชั้น client-observable (ต้องมีคนหน้าจอ, ห้ามอนุมานจากบรรทัดคอนโซล):
1. **[เกณฑ์ชั้นจอข้อแรก -- คำสั่งเจ้าของ 2026-08-27 09:15, claim เดียวของใบนี้]** ป้ายชื่อ Tornado Eagle
   เป็น**สีแดง** และแผงเป้า (เปิดจาก single-click) เป็น**สีแดง/สไตล์ศัตรู** -- บันทึกจากภาพนิ่ง full-res
   ตามกติกาสีป้ายมาตรฐาน (บรรทัดต่อป้ายต่อภาพ, "none" ถ้าไม่มี, ห้ามอนุมานสาเหตุ -- `RE-067` เปิดอยู่).
   **ผลลบที่มีค่าเท่ากับ PASS:** ถ้าป้ายไม่แดงหรือแผงเป้าไม่แดง ⇒ นี่คือผลลบเต็มรูปของ*ทั้งใบนี้* (ประตูปิดตาม
   ขั้นตอน 5f) -- บอกว่าฝั่งเซิร์ฟเวอร์ส่งครึ่งคู่แล้ว (ถ้าเกณฑ์ wire/DB ข้างบนผ่าน) แต่ไคลเอนต์ยังไม่ตีความเป็น
   ศัตรู ⇒ แยกปัญหาออกจากฝั่งส่งไปที่ฝั่งตีความ/เรนเดอร์ของไคลเอนต์ -- redirect: จับ capture ไบต์ StartGame
   ดิบของทั้งสอง actor block (ผู้เล่น + มอนสเตอร์) มาเทียบ shape/ตำแหน่ง/mask กับคู่ (1,6) ที่เคยพิสูจน์แดงจริง
   ที่ `GT-032`.
2. **[ประตู]** ถ้าเกณฑ์ข้อ 1 ไม่ผ่าน ⇒ ไม่มีการโจมตี ⇒ เกณฑ์ผ่านชั้นจอเดิมของ `GT-084` (เลขดาเมจ, หลอด HP,
   ท่าล้มตาย) เป็น **NO-RESULT** (ไม่ได้ทำ ไม่ใช่ไม่ผ่าน) สำหรับรอบนี้.
3. ถ้าเกณฑ์ข้อ 1 ผ่านและผู้เทสไปต่อ (ขั้นตอน 5g/6): เกณฑ์ผ่านชั้นจอเดิมของ `GT-084` และ `RIDER-084-A`
   (OW1-OW3) ใช้ทุกตัวอักษรตามใบเดิม -- ไม่ทวนซ้ำที่นี่ บันทึกผลแยกหัวข้อว่าเป็นผลต่อของ `GT-084`.
4. NO-CRASH verdict จากคลิกขวาลาก ทั้งที่ T0 และตอนปิดฉาก.

### nonclaims
- ใบนี้พิสูจน์แค่ scene_id ที่ serializer ตัวนี้ยอมรับ คือ (1, 2) เท่านั้น (Port Royal/ฉากคู่โพรบของมัน) --
  ตัวละครที่ตำแหน่งเก็บไว้ resolve เข้าไปนอกสองฉากนี้ไม่อยู่ในขอบเขตของใบนี้. world-travel ถูกปิดไว้โดยนโยบาย
  เจ้าของอยู่แล้วในตอนนี้ ทำให้ผู้เล่นทั่วไปอยู่ในเขต Port Royal เสมอ ⇒ ข้อจำกัดนี้ไม่ใช่ตัวบล็อกของรอบนี้
  แต่เป็นขอบเขต claim ที่ต้องเขียนไว้ตรง ๆ.
- ใบนี้ไม่พิสูจน์กลไกโจมตี/ดาเมจ/ตาย -- claim เดียวของใบนี้คือเกณฑ์ชั้นจอข้อแรก (ความเป็นศัตรูที่ตาเห็น) เท่านั้น
  แม้ผู้เทสจะไปต่อถึงขั้นโจมตีในเซสชันเดียวกัน (ขั้นตอน 5g) ผลของส่วนนั้นทั้งหมดเป็นของ `GT-084` เดิม ไม่ใช่
  claim ใหม่ที่ใบนี้เปิด.
- ไม่ชี้สาเหตุว่าอะไรกำหนดสีของป้ายชื่อ -- `RE-067` เปิดอยู่ หน้าที่ผู้เทสคือจดสีอย่างเดียว.
- ไม่พิสูจน์ว่าผู้เล่นสองคน/สองเซสชันพร้อมกันเห็นสีเดียวกัน -- ผู้เทสคนเดียว เซสชันเดียว.
- ไม่พิสูจน์ว่าการแก้เสถียรข้าม reconnect/relogin -- ล็อกอินครั้งเดียวในรอบนี้.
- ไม่ปิด `RIDER-084-A`/`RE-092` (คำถาม world-wipe) -- ถ้าไปถึงขั้นโจมตี nonclaims เดิมของริเดอร์นั้นยังใช้ทุก
  ตัวอักษร.
- ถ้าผู้เทสหาโมเดล 0x201F หรือตัวสำรองไม่เจอเลยภายในงบ 15 นาที ⇒ ทั้งใบเป็น **NO-RESULT** (ระยะวาดโมเดลไม่เคย
  มีใครวัด) ไม่ใช่ผลลบของการแก้ faction.

### result (ผู้เทสกรอก)
```

```

---


## GT-101 GM-001 LOGIN-STATE-VISUAL-PROBE-001: ล็อกอินด้วยบัญชีในลิสต์ gm_accounts แล้ว GM_UpdateGMStateVital (0x5A19) ที่ CORE-REQUEST-006 ต่อสายเข้า login path แล้ว จอเปลี่ยนอะไรไหม  [RESULT -- ไม่ใช่ PASS/NO-RESULT/BLOCKED, ดูผลด้านล่าง]

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md, prefix สองแบบ ห้ามแยกตัวนับ.
> เลขสูงสุดที่ใช้ไปแล้ว ณ เวลาเขียนใบนี้: GT-099 (GAME_TEST_QUEUE.md) และ RE-100 (CLIENT_RE_QUEUE.md,
> บันทึกไว้เองว่า "เลขว่างถัดไป = 101"). grep ยืนยันก่อนจอง: GT-101 = 0 hit, RE-101 = 0 hit ทั้งสองไฟล์
> (ยืนยัน 2026-08-27). ใบเก่าทุกใบอยู่ที่เดิม ไม่ถูกแตะ ไม่ถูกย้าย.

### ที่มา -- อ่านจากซอร์สจริง ห้าม re-derive ระหว่างรอบ
- `notes_to_chief/20260826_1630_PANYA-ORDER-open-Lane-GM-plus-attended-recon-GM-packets-already-in-client-registry.md`
  ข้อ ③ เสนอลำดับงาน GM-001: ส่ง `GM_UpdateGMStateVital` ตอน login ให้บัญชี `gm_accounts` แล้ว attended
  probe 5 นาทีว่าจอเปลี่ยนอะไร (ตอนนั้นเสนอไอคอน `bm_gm`, UI, prefix แชท เป็นตัวเลือกที่ยังไม่พิสูจน์).
  precondition ของ probe นี้ (การต่อสายฟังก์ชันเข้า login path จริง) ยังไม่มีตอนเขียนจดหมาย ตอนนี้มีแล้ว
  -- ใบนี้คือใบแรกที่เปิด GM-001 ตามที่จดหมายนั้นเสนอไว้.
- `pirate-force-server/src/pirateforce_foundation/gm/state_wire.py`: `make_gm_update_state_frame` สร้าง
  เฟรม `GM_UpdateGMStateVital` (`0x5A19`) จาก 3 field ที่ layout พิสูจน์แล้วระดับไบต์ (`RE-089`): tag
  `0x0B` 1 byte @+0x14, tag `0x0B` 1 byte @+0x15, tag `0x14` 4 byte @+0x18 -- ความหมายของแต่ละ field
  ไม่พิสูจน์ (หัวไฟล์เดียวกันเขียนกำกับไว้เอง ห้าม rename เป็น `is_gm`/`level` โดยไม่มี RE อ้างอิง).
- `CORE-REQUEST-006` ต่อสายฟังก์ชันนี้เข้า login path ของ `runtime.py` แล้ว (บันทึกที่
  `pirate-force-server/docs/GM_LANE.md` หัวข้อ "What is intentionally NOT built yet, and why", ~บรรทัด
  379-392): หลัง login สำเร็จ ถ้า `is_gm_account(self.token)` เป็นจริง จะเรียก
  `make_gm_update_state_frame(legacy, 1, 0, 0, 0)` แล้วคิวเฟรมนั้นเข้าไปกับ action list ของ
  `START_GAME_RES` เดียวกัน (label `"GM_UPDATE_STATE_AFTER_LOGIN"`, delay `0.0`) -- **ทำงานเสมอ ไม่มี
  `--*-scenario`, ไม่มีสวิตช์ opt-in ใด ๆ** (คำของ `docs/GM_LANE.md` เอง). ตำแหน่งจริงที่ผู้เขียนใบนี้อ่านคือ
  `runtime.py:4576-4623` (`is_gm = is_gm_account(self.token)` บรรทัด 4599, เรียก
  `make_gm_update_state_frame` บรรทัด 4618-4620) -- `docs/GM_LANE.md` เองอ้างเลขบรรทัดคนละเลข (~4353)
  เพราะเป็นเลขบรรทัด ณ ตอนเขียนเอกสาร ไม่ใช่ ณ ตอนนี้ -- **ด่านที่ 2 ข้างล่างจึงตรวจด้วย `git grep` บนซอร์ส
  จริงของ `<SHA>` ที่จะบูตเสมอ ไม่ใช้เลขบรรทัดในเอกสารใด ๆ เป็นหลักฐาน** ตามธรรมเนียมของ
  `pf_resolve_green_boot.py`.
- ค่าที่ส่งจริงตอนนี้ (`1, 0, 0, 0`) เป็น placeholder ที่ทำเครื่องหมาย `[ASSUMED - awaiting RE]` ในซอร์ส
  เอง -- เลือก `1` เพราะไม่มี version อื่นเคยถูกสังเกตสำหรับ vital นี้ และ `0/0/0` เพราะเป็นค่าที่คิดว่ามี
  โอกาสน้อยที่สุดที่จะทำให้จอเปลี่ยนอะไรที่ยังไม่เคยวัด (comment ของ chief เองที่จุดเรียก) -- ใบนี้
  **สังเกตผลของค่าชุดนี้ชุดเดียว ไม่ใช่ทุกชุดค่าที่เป็นไปได้**.
- `RE-089-RESULT` (`notes_to_chief/20260827_0016_RE-089-RESULT-STATE-PROPAGATION-PINNED-BMGM-FALSE-LEAD.md`)
  ปิดแบบ DONE/BOUNDED-NEGATIVE: static พิสูจน์แล้วว่า 3 field ก็อปเข้า
  `GMModule_Client+0x18/+0x19/+0x1C` จริง (ไบต์ `+0x14/+0x15` ถูก normalize เท่ากับค่า 1 เท่านั้นถึงจะ
  ติด ค่าอื่น 2..255 กลายเป็น 0) แล้วก็อปต่อเข้า record ชนิด `0x25` ที่ยังไม่เจอ render/widget/texture
  call ใด ๆ เชื่อมออกไป -- **และหักล้าง `bm_gm.tga` ว่าไม่ใช่ไอคอน GM (มันคือ glyph "green minus" ของ
  `FxNumberCache` ดาเมจ) ห้ามอ้างเป็นเบาะแสอีก**. RE-089 เขียนเองว่าขั้นถัดไปที่ตอบได้คือ
  "capture/attended matrix ที่ควบคุม tuple `(byte0,byte1,u32)` แล้วสังเกต UI/chat/event จริง" แต่
  **ไม่เปิดใบนั้นเอง** -- นี่คือใบที่เปิดขั้นนั้น.
- ควบคุมเชิงลบที่มีอยู่แล้วโดยบังเอิญ (ไม่ใช่ผลของใบนี้): ทุกรอบ default-boot ก่อนหน้านี้ในคิวนี้ (เช่น
  `GT-078`, `GT-084`, `GT-099`) ไม่มีบัญชีไหนอยู่ใน `gm_accounts` (ไฟล์ไม่มี/ว่างเปล่ามาตลอด) จึงไม่เคย
  พิมพ์บรรทัด `GM_UPDATE_STATE_AFTER_LOGIN` เลยสักรอบ -- สอดคล้องกับ default "ไม่มีใครเป็น GM" ของ
  `gm/accounts.py` ไม่ใช่การทดสอบใหม่ของใบนี้.

### ก่อนบูต -- ด่าน 0 (บัญชี GM ต้องรู้ชื่อจริงก่อน ห้ามเดา), ด่าน 1 (green boot), ด่าน 2 (grep ยืนยันสาย)

**ด่าน 0 -- ชื่อบัญชีที่จะได้ GM:**
`is_gm_account()` เทียบ **แบบ exact case-sensitive** กับลิสต์ JSON `gm_accounts` ใน
`config/gm_accounts.json` (หรือไฟล์ที่ตัวแปรแวดล้อม `PF_GM_ACCOUNTS_CONFIG` ชี้ไป, `gm/accounts.py`'s
own `ENV_OVERRIDE`) -- ค่าเริ่มต้นคือไม่มีใครเป็น GM. **ใบนี้ไม่ประดิษฐ์ชื่อบัญชีเอง** มีสองทางเท่านั้น:
  (A) ถามไปที่ chief ว่าตอนนี้ `config/gm_accounts.json` ของเซิร์ฟเวอร์จริงมีชื่อบัญชีอะไรอยู่แล้วบ้าง
      (ถ้ามี) -- ใช้ชื่อนั้น **ตรงตัวสะกด/ตัวพิมพ์ใหญ่เล็กทุกตัวอักษร** และต้องเป็นบัญชีที่ผู้เทสมีสิทธิ์
      ล็อกอินเข้าไปเลือกตัวละครได้จริงด้วย (มีตัวละครอยู่ในบัญชีนั้น) ไม่ใช่แค่ชื่อลอย ๆ ในไฟล์.
  (B) ถ้า chief ตอบว่าไฟล์ยังไม่มี/ว่างเปล่า -- ใบนี้ **BLOCKED** จนกว่าจะได้รับอนุมัติชัดเจนให้เพิ่มบัญชี
      ทดสอบเข้าไป (การเปลี่ยนไฟล์นี้คือการเปลี่ยน invariant ความปลอดภัยของทั้งเซิร์ฟเวอร์ ไม่ใช่ค่าใน
      ขอบเขตของใบทดสอบใบเดียว -- ห้ามผู้เทสตัดสินใจเองกลางรอบ).
  ถ้าได้รับอนุมัติทาง (B): **ห้ามแก้ `config/gm_accounts.json` ตัวจริงถ้ามีเซิร์ฟเวอร์/รอบอื่นอ่านมันอยู่**
  -- ให้สร้างสำเนาแยก (เช่น `pf_bridge\backup\gm_accounts_GT-101_<yyyyMMdd_HHmmss>.json`) ใส่ชื่อบัญชี
  ที่ chief อนุมัติ/ที่ผู้เทสจะล็อกอินจริง แล้วตั้ง `$env:PF_GM_ACCOUNTS_CONFIG` ชี้ไปที่สำเนานั้นก่อนสั่ง
  `app.py` -- วิธีนี้คือ `ENV_OVERRIDE` ที่ `gm/accounts.py` เขียนรองรับไว้เอง ไม่ต้องแตะไฟล์จริงเลย. จด
  ชื่อบัญชีและ path สำเนาไว้ในผลทุกครั้ง แล้วลบสำเนา/เลิกตั้ง env ตอน teardown.

**ด่าน 1 -- resolve commit เขียว:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
รันจากโฟลเดอร์ pf_bridge, exit 0 + `BOOT_COMMIT: <sha>` เท่านั้นถึงบูตได้ (git checkout `<sha>` แบบ
detached HEAD). ห้ามเทียบเลข commit ด้วยตา -- resolver คืนหัวแบรนช์ที่ผ่านเกต ไม่ใช่ merge commit เสมอไป.

**ด่าน 2 -- ยืนยันสายจริงของ `<SHA>` (ห้ามเชื่อเลขบรรทัดในเอกสาร ต้อง grep ของจริง):**
```
git grep -n "make_gm_update_state_frame" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "is_gm_account(self.token)" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "GM_UPDATE_STATE_AFTER_LOGIN" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "GM_UPDATE_GM_STATE_VITAL_ID = 0x5A19" <SHA> -- src/pirateforce_foundation/gm/state_wire.py
git grep -n "def is_gm_account" <SHA> -- src/pirateforce_foundation/gm/accounts.py
```
ต้องได้อย่างน้อย 1 บรรทัดต่อคำสั่งทั้ง 5 คำสั่ง. ขาดข้อใดข้อหนึ่ง = **BLOCKED** -- คอมมิตที่จะบูตยังไม่มี
CORE-REQUEST-006 ต่อสายจริง ห้ามบูต ห้ามหาคอมมิตเอง ไปทำใบอื่นแล้วรอ merge.

### db (สำเนาเสมอ ห้ามเปิด canonical, ห้ามแตะ state\play.sqlite3)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-101_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt101.sqlite3
```
- เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง.
- ใบนี้ไม่แตะเนื้อหา backpack/character แถวไหนเลย -- สถานะ GM มาจาก config แยกต่างหาก (ดูด่าน 0) ไม่ใช่
  แถวใน DB นี้. สำเนาใหม่ทุกบูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดเสมอ (คาดหมายอยู่แล้ว ไม่ใช่ผลของใบนี้).

### server args (เป๊ะ -- ไม่มี --*-scenario เพราะ CORE-REQUEST-006 ทำงานเสมอ ไม่มีสวิตช์)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
$env:PF_GM_ACCOUNTS_CONFIG = "<path จากด่าน 0 ถ้าใช้ทาง B>"   # ลบบรรทัดนี้ถ้าใช้ config/gm_accounts.json ตัวจริงตรง ๆ (ทาง A)
py -3 -u -m pirateforce_foundation.app --db state\run_gt101.sqlite3
```
ห้ามมี `--*-scenario` แม้แต่ตัวเดียว, ห้ามพ่วงใบอื่นเข้าบูตนี้.

### steps (คลิกต่อคลิก -- อัดวิดีโอต่อเนื่องตลอดช่วงถือ LOCK_GAME)
ก่อนเริ่ม: ถือ LOCK_GAME, จด boot stamp (+07:00, ต้องไม่เก่ากว่า 420 นาทีตอนรัน teardown), เทียบ sha
canonical, copy DB สองใบตามบล็อก db, เตรียม teardown จาก `TEMPLATE_teardown_generic.ps1`. ยืนยันด่าน
0-2 ผ่านครบ (จดชื่อบัญชี GM + path config ที่ใช้ + SHA ที่บูต).

1. สตาร์ตเซิร์ฟเวอร์ก่อนเสมอ (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด
   client). client ที่บูตโดยไม่มีเซิร์ฟเวอร์ตายเองใน ~3.5 นาที. ถ้าต้องฆ่า client กลางคัน ต้อง restart
   server ก่อนเปิด client ใหม่เสมอ (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่ "connecting"
   ตลอดกาล).
2. เปิด client -> เลือกเซิร์ฟเวอร์ -> dialog PVP ปุ่มซ้าย -> หน้าเลือกตัวละคร -> เลือกช่องแรกของบัญชี GM
   ที่จดไว้ในด่าน 0 -> ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม (ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด). เริ่มอัด
   วิดีโอต่อเนื่องตั้งแต่ก่อนกดเข้าเกม.
3. T0 -- เห็น HP bar/minimap/ชื่อแมพครบ. จด HUD X/Y. คลิกขวาค้างลากกวาดกล้อง 360 องศาหนึ่งรอบ (นี่คือตัว
   เช็ค NO-CRASH ตัวเดียวที่ใบนี้ยอมรับ -- คลิกขวาลากหมุนกล้องอย่างเดียว ทิศหันของตัวละครไม่ขยับ ไม่ยิง
   อะไรออกสาย ปลอดภัยเสมอ -- **ห้ามใช้ Q/E เป็นตัวเช็คนี้เด็ดขาด** เพราะ Q/E หันตัวละครจริงและยิง
   `TargetPosVital`). ใบนี้ไม่มีขั้นเดิน/ขั้นโจมตี/ขั้น trigger ใด ๆ เลย ⇒ ไม่จำเป็นต้องใช้ W/A/S/D หรือ
   Q/E เลยตลอดรอบ -- ถ้าต้องมองรอบตัว ให้ใช้คลิกขวาลากเท่านั้น.
4. เฝ้าจอต่อเนื่องอย่างน้อย 5 นาที (ตามที่จดหมายเปิดเลนเสนอไว้) นับจากเฟรมที่เห็น HUD ครบ (T0) -- ถ่ายภาพ
   นิ่ง full-res ที่ t=0s (ทันที T0), t=30s, t=120s, t=300s เป็นอย่างน้อย และถ่ายเพิ่มทันทีที่เห็นอะไร
   เปลี่ยนแม้เพียงเล็กน้อยนอกตารางเวลานี้. กวาดตาดูองค์ประกอบมาตรฐานทุกจุดในแต่ละภาพ: ป้ายชื่อเหนือหัว
   ตัวเอง, แผงสถานะ/แถบ HP มุมซ้าย, แผงเป้า (ถ้ามี), หน้าต่างแชทและ prefix ของชื่อตัวเองในนั้น, แถบไอคอน/
   เมนูบนสุด, minimap, และมุมจอทุกมุม -- ไม่จำกัดเฉพาะจุดที่จดหมายเดิมเดา (ไอคอน `bm_gm.tga` ถูก RE-089
   หักล้างไปแล้วว่าเป็น glyph ดาเมจ ไม่ใช่ไอคอน GM ห้ามอ้างเป็นเบาะแสอีก).
5. คู่ขนานกับข้อ 4: เฝ้าคอนโซลเซิร์ฟเวอร์ต่อเนื่อง -- คัดบรรทัด `[G>] GM_UPDATE_STATE_AFTER_LOGIN` (ต้อง
   มาพร้อมบรรทัด `[G>]` ของ START_GAME_RES/teleport ชุดเดียวกันตอน login) และบรรทัด
   `gm_account_lookup_failed_*` ถ้ามี (แปลว่า config พังและ login รอบนี้ไม่ได้รับเฟรม GM เลย -- ถ้าเจอ
   ให้หยุดแล้วเขียนเป็น BLOCKED ไม่ใช่ NO-RESULT เพราะยังไม่ได้ทดสอบอะไรเลย).
6. ครบ 5 นาทีแล้ว: คลิกขวาลากอีกครั้ง (NO-CRASH ซ้ำ) -- ยืนยันไคลเอนต์ยังตอบสนอง.
7. ออกเกม -> teardown ตาม `TEMPLATE_teardown_generic.ps1` -> เทียบ sha canonical รอบสุดท้าย -> ถ้าใช้
   สำเนา config (ทาง B ของด่าน 0) ลบสำเนาทิ้ง/เลิกตั้ง `$env:PF_GM_ACCOUNTS_CONFIG`.

### pass criteria (สองชั้น แยกกันเสมอ ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)

ชั้น wire/DB (อ่านจาก server console/event log ล้วน ๆ ไม่ต้องพึ่งสิ่งที่เห็นบนจอ):
- คอนโซลพิมพ์บรรทัด `[G>] GM_UPDATE_STATE_AFTER_LOGIN (N bytes)` หนึ่งครั้งตอนล็อกอินสำเร็จของบัญชี GM
  (พิสูจน์ว่า `is_gm_account()` คืนจริงและ `make_gm_update_state_frame` ถูกเรียกและคิวเฟรมจริง -- คำถามที่
  `docs/GM_LANE.md`/`RE-089` ทิ้งไว้ให้ปิดที่ชั้น wire).
- ไม่มีบรรทัด `gm_account_lookup_failed_*` ขึ้นเลยระหว่างรอบนี้ (ถ้ามี = config พัง ต้องแก้ก่อนนับผล).
- `sessions`: `count(*) WHERE selected_character_id IS NOT NULL` +1 ต่อการเข้าเกมหนึ่งครั้ง, `max(lease_
  generation)` ไม่ถอยหลัง, `PRAGMA integrity_check` = `ok` บนสำเนา, sha256 canonical ก่อน-หลังตรงกับ
  `CANON_SHA.txt` ทั้งสองครั้ง.
- raw GAME log ทั้งไฟล์ + console out/err เก็บทั้งก่อน/หลัง ไม่ตัดทอน.

ชั้น client-observable (ต้องมีคนหน้าจอ, ห้ามอนุมานจากบรรทัดคอนโซล):
- 🔴 **ทั้งสองผลลัพธ์เป็นผลที่ถูกต้องและมีค่าเท่ากัน ไม่ใช่เกณฑ์ผ่าน/ตกของใบนี้:**
  (ก) **ไม่เห็นอะไรเปลี่ยนบนจอเลย** ตลอด 5 นาที (ไม่มีไอคอน/prefix/UI/แผงใหม่ใด ๆ) -- นี่คือผลลบที่
      RE-089 ทำนายไว้แล้วว่าเป็นไปได้ (ไม่พบ render/UI consumer ที่ชั้น static) เขียนเป็นผลลบเต็มรูป
      พร้อมรายการทุกจุดที่ตรวจแล้วว่า "ไม่เปลี่ยน" ทีละจุด (ป้ายชื่อ/แผงสถานะ/แชท/เมนู/minimap).
  (ข) **เห็นอะไรเปลี่ยนจริง** (ระบุให้ชัดว่าที่ไหน เช่น ไอคอนใหม่เหนือหัว, prefix ในแชท, แผง/ปุ่มใหม่ ฯลฯ)
      -- นี่คือผลบวกที่ตอบคำถามค้างของ RE-089 ได้จริงเป็นครั้งแรก ถ่ายภาพนิ่ง full-res ปิดล้อมจุดที่
      เปลี่ยนทันที.
- สีของป้ายชื่อทุกป้ายในทุกภาพนิ่ง full-res (t=0s/30s/120s/300s และภาพเพิ่มถ้ามี) บันทึกเป็นบรรทัดเดียว
  ต่อป้ายต่อภาพ ("none" เขียนออกมาถ้าไม่มี ห้ามเว้นว่าง) -- อ่านจากภาพนิ่ง full-res เท่านั้น ห้ามอ่านจาก
  contact sheet/ภาพย่อ/วิดีโอ ห้ามอนุมานสาเหตุของสี (`RE-067` เปิดอยู่). ถ้ามีภาพอ้างอิงของเซิร์ฟเวอร์
  ต้นฉบับให้เทียบและเติมแถวลง `REAL_SERVER_DIVERGENCE.tsv` -- ไม่มีภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับสำหรับ
  GM state โดยเฉพาะที่รู้จักตอนนี้ ถ้าไม่มีอ้างอิงให้ใช้ `compared_and_matched=no-reference`.

### nonclaims
- 🔴 **ใบนี้เป็นการสังเกต GM tool ไม่ใช่การพิสูจน์ว่า "ฟีเจอร์ GM ทำงาน"** -- ตามกฎความซื่อสัตย์ของเลนนี้
  เอง (`docs/GM_LANE.md`/จดหมาย `20260826_1630` ข้อ③): เห็นจอเปลี่ยน (หรือไม่เปลี่ยน) ไม่ใช่หลักฐานว่า GM
  tool ใด ๆ "ใช้ได้" -- ไม่มีคำสั่ง GM ใดถูกรันในใบนี้เลย (`0x51E9`/GM-002/GM-003 เป็นคนละใบ ยังไม่ได้ต่อ
  สายการรัน).
- 🔴 **การเปลี่ยน/ไม่เปลี่ยนของจอที่เห็นในใบนี้ เป็นหลักฐานเกี่ยวกับค่า payload สามฟิลด์ชุดนี้ที่ส่งจริง
  ตอนนี้เท่านั้น (`vital_version=1, field_0x0b_first=1, field_0x0b_second=0, field_0x14=0`) -- ไม่ใช่
  หลักฐานเกี่ยวกับ pipeline การเรนเดอร์ของ `GMModule_Client` โดยทั่วไป** และไม่ตัดสินว่าค่าชุดอื่นจะทำให้
  จอเปลี่ยนหรือไม่ (RE-089 พิสูจน์แล้วว่าไบต์ `+0x14/+0x15` ถูก normalize เท่ากับ 1 เท่านั้นถึงจะติด ค่า
  อื่น 2..255 กลายเป็น 0 -- ใบนี้ทดสอบเฉพาะค่าที่ normalize แล้วเป็น `(1,0)` กับ u32 `0` เท่านั้น).
- ไม่ตั้ง semantic ว่าไบต์ไหนคือ `is_gm` หรือ u32 คือ `level` จากสิ่งที่เห็นบนจอ -- `RE-089` ห้ามการอนุมาน
  นี้จาก offset/ความกว้างไว้แล้ว ใบนี้จดแค่ "เห็นอะไร" ไม่ตัดสิน "ทำไม".
- ไม่ทดสอบว่าผู้เล่นคนอื่น (ที่ไม่ใช่ GM) เห็นอะไรต่างไปเกี่ยวกับบัญชี GM นี้ -- ผู้เทสคนเดียว เซสชันเดียว
  เท่านั้นในรอบนี้.
- ไม่ทดสอบความเสถียรข้าม reconnect/relogin -- ล็อกอินครั้งเดียวในรอบนี้.
- ถ้าใช้สำเนา config ทาง B ของด่าน 0: ไม่พิสูจน์ว่าการเปลี่ยนแปลงนั้นคงอยู่ข้ามรอบอื่น หรือกระทบเลนอื่น --
  สำเนานี้เป็นของรอบนี้เท่านั้น ถูกลบทิ้งตอน teardown.
- ไม่ชี้สาเหตุของสีป้ายชื่อ (`RE-067` เปิดอยู่).
- ถ้าด่าน 0/1/2 ไปไม่ถึง (BLOCKED) => ทั้งใบเป็น BLOCKED ไม่ใช่ NO-RESULT/FAIL -- ยังไม่ได้ล็อกอินเลย.

🆕 **อัปเดต (chief cloud รอบ `4txjyg` R192 · 2026-08-27T12:00+07:00) — ด่าน 0 ตอบแล้ว:** `config/gm_accounts.json`
ไม่มีอยู่จริงในรีโปตอนนี้ (ไม่มีใครเป็น GM โดยดีฟอลต์) chief อนุมัติทาง (B) — สร้างสำเนาแยก ใส่ชื่อบัญชี
`attended_test` แล้วตั้ง `$env:PF_GM_ACCOUNTS_CONFIG` ชี้ไปที่สำเนานั้นก่อนบูต ไม่ต้องแตะ/สร้าง
`config/gm_accounts.json` จริง รายละเอียดเต็มดู
`notes_to_chief/20260827_1200_CHIEF-REPLY-GT101-gm-accounts-test-config-approved.md` — ด่าน 0 ไม่ BLOCKED
อีกต่อไป ไปต่อด่าน 1/2 ได้เลย

### result (ผู้เทสกรอก)
```
RESULT (ไม่ใช่ PASS/NO-RESULT/BLOCKED) 2026-08-27T14:39+07:00, owner-observed: client ปฏิเสธ
GM_UpdateGMStateVital เวอร์ชัน 1 ด้วย modal error "VitalData 版本不對 ErrorData=23065" (23065 = 0x5A19)
แล้วปิด socket เอง -- เซสชันตายก่อนถึงคำถามเดิมของใบนี้ (จอเปลี่ยนอะไรไหม) เต็มผล/ไบต์บนสาย/หลักฐาน:
notes_to_chief/20260827_1445_GT101-RESULT-client-rejects-0x5A19-version-1-error-23065-session-killed.md
ติดตาม: RE-105 (vital_version ที่ถูก) + CORE-REQUEST-016 (guard runtime.py:4746 จนกว่าจะพิน) -- ทั้งคู่เปิด
โดย LANE-GM รอบ 8791h3
```

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


## GT-128 GM-003 CHAT-WARP-VISIBLE-001 [attended, in-game]: GM พิมพ์ `/warp <ฉากปัจจุบัน> <x> <y>` ลงกล่องแชทธรรมดา แล้ว**ตัวละครขยับไปยังพิกัดนั้นบนจอจริงหรือไม่** -- ใบแรกของสาย GM ที่ตัดสินที่จอ ไม่ใช่ที่ log  [❌ **CANCELLED - refuted by R306 finding 3 (`notes_to_chief/20260903_1655_*`)** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2) — รูป same-scene ที่มีพิกัดส่ง `LANE_GM_CHAT_WARP_TELEPORT_FORCE_POS` แล้ว **ไคลเอนต์ปิดตัวเอง** (`ErrorData=28317`) วัดบนจอเจ้าของ ⇒ คำถามของใบนี้ ("ตัวละครขยับไปพิกัดนั้นไหม") ตอบไม่ได้ด้วยรูปเฟรมที่มีอยู่ และ `COO-DECISION 20260903_1744` ข้อ 3 สั่งปิด `/warp` แบบมีพิกัดไปแล้ว · 🔴 **เปิดใบใหม่ (ไม่ใช่ปลดใบนี้) เมื่อ LANE-GM เปลี่ยนรูปเฟรมและมี headless proof** — ใบใหม่ต้องเขียนเกณฑ์บนรูปเฟรมใหม่ ไม่ใช่ยกด่านเก่าทั้งชุดมาใช้ · สถานะเดิม: ~~BLOCKED — token compares nothing (COO-DECISION 20260829_0041)~~ **STILL BLOCKED — token fixed, but a separate COO-held gate remains (see chief R243 update at end)**: ห้ามเกรด ห้ามบันทึกผลใด ๆ ด้วยโทเคน `GM_WARP_POSITION_CONFIRMED` ตัวปัจจุบัน เพราะมันเทียบแค่ "แถวเปลี่ยนค่า" ไม่ได้เทียบกับ**จุดที่สั่ง** · ปลดเมื่อชุดแก้โทเคน+audit ลง main (chief, ภายใน 2026-08-29 23:59+07:00) · **อัปเดตรอบ `nz0qt2`:** ครึ่ง audit ที่เป็นเขต LANE-GM (แถว `outcome`, `CORE-REQUEST-GM-032` ข้อ 1-2) อยู่ใน PR `pirate-force-server#223` **รอ merge** · ครึ่งโทเคน (`GM_WARP_POSITION_TARGET_MATCH/MISMATCH`, `CORE-REQUEST-GM-031`) และข้อ 3 ของ GM-032 ยังเป็นของ chief ⇒ ป้าย BLOCKED ของใบนี้ **ยังไม่ถูกปลด** ด้วยรอบนี้ · 🔴 **เหตุผลที่วัดแล้ว ไม่ใช่แค่เหตุผลเชิงหลักการ** (เพิ่มโดย LANE-GM เจ้าของใบ รอบ `xk4wmz`): pf-adversary วัดว่าโทเคนตัวปัจจุบัน **ยิงตอนผู้เล่นเดินเองหนึ่งก้าว**หลัง warp ที่ไคลเอนต์เมิน ⇒ ใบนี้ "ผ่าน" ได้โดยที่ warp ไม่ทำงานเลย · **ของที่ LANE-GM ทำเสร็จแล้วเพื่อชุดของ chief:** `gm/warp_target_record.py` เก็บปลายทางของ warp ใบนั้นไว้เทียบได้ หยิบได้ครั้งเดียว ผูกกับ `character.id` (รอบ `z6gu2n` บน main แล้ว) และ `CORE-REQUEST-GM-031` ขอให้ chief พิมพ์ `GM_WARP_POSITION_TARGET_MATCH` / `..._MISMATCH` **เพิ่ม** จากโทเคนเดิม (ห้ามเอา match มาเป็นเงื่อนไขของโทเคนเดิม -- วันนี้ client เมิน `ForcePos` ผลที่คาดคือ MISMATCH ถ้ารวมกันโทเคนจะหายทั้งใบ) · BLOCKED x4 รวมข้อนี้ (~~x3~~ ~~x2~~ นับผิดมาแต่แรก มีสามข้อมาตลอด) -- ห้ามบูต: (ก) `CORE-REQUEST-GM-029` ยังไม่ลง main (จุดเรียกที่คืน action ที่สาขา `0xAC52`) · **อัปเดตรอบ `vvxkft`:** ตัวโมดูล `gm/chat_command_action.py` เองก็เพิ่งกลับขึ้น main รอบนี้ (PR #204 -- PR #200 ของรอบ `gr2q9j` ถูกปิดเพราะ gate แดง ไม่เคย merge) และ GM-029 เปลี่ยนความหมายเป็น "**แทนที่**บรรทัด `fire()` ของ GM-028 ในคอมมิตเดียว" ไม่ใช่ "เพิ่มจุดเรียก" (ใบ `20260828_1930_LANE-GM-CORE-REQUEST-GM-029-v2-replace-not-add.md`) ⇒ วันที่ใบนี้บูตได้ `GT-127` จะใช้ไม่ได้ตามเกณฑ์เดิมอีกต่อไป เพราะ event เปลี่ยนเป็น `gm_chat_action_*` -- **บูต `GT-127` ให้จบก่อน** (ข) ~~`RE-129` ยังไม่ตอบ~~ **RE-129 ตอบแล้ว 2026-08-28T20:09+07:00 (`ForcePos vital_version = 0`) แต่ข้อนี้ยังบล็อกอยู่ด้วยเหตุใหม่:** `COO-DECISION 20260828_2130` ล็อกแข็งว่าห้ามเปลี่ยน `FORCE_POS_VITAL_VERSION_CONFIRMED` จาก `None` จนกว่าจุดเขียนตำแหน่งแบบยืนยันจะอยู่บน main (`CORE-REQUEST-GM-030`, รอบ `fo2lgh`) **แม้ RE-129 จะตอบก่อนก็ตาม** ⇒ โมดูลยังปฏิเสธการส่งด้วยตัวเอง และตอนนี้มีเทสบังคับด้วย (`pirate-force-server/tests/test_gm_force_pos_version_lock.py` แดงถ้าเปลี่ยนค่าก่อนโทเคน `GM_WARP_POSITION_CONFIRMED` อยู่บน main) · เหตุผลชั้นที่สองจาก RE-129 เอง: handler ที่ client จดทะเบียนไว้สำหรับ `ForcePos` = `mov al,1; ret 4` ไม่อ่าน payload ⇒ **version ถูกไม่ได้แปลว่าจะขยับ** ใบนี้ยังเป็นใบเดียวที่ตัดสินข้อนั้นได้ (ค) ~~🔴 **คำถาม "ใครเป็นเจ้าของตำแหน่งหลัง warp" ยังไม่มีคำตอบ**~~ **ตอบแล้ว 2026-08-28T21:30+07:00 (`COO-DECISION`): เจ้าของคือตำแหน่งที่ client ยืนยันแล้ว · เซิร์ฟเวอร์ห้ามเขียนตำแหน่งที่ตัวเองไม่ได้สังเกตเห็น · ตัวยืนยันคือ `TargetPos` ใบแรกหลังเฟรม** ⇒ ข้อนี้เหลือ "รอการเดินสาย" ไม่ใช่ "รอคำตอบ" -- ปลดเมื่อ `CORE-REQUEST-GM-030` ลง main และ COO ปลดล็อก · ผู้เทสต้องบันทึกในผล: หลัง warp ให้เดินหนึ่งก้าวเพื่อบังคับ `TargetPos` แล้วดูว่าคอนโซลมี `GM_WARP_POSITION_CONFIRMED` หรือไม่ · **บริบทเดิมของข้อนี้ (เก็บไว้):** — pf-adversary รอบ `gr2q9j` ชี้ว่า หลังส่ง `ForcePos` แล้ว แถวใน DB และ `selected.position` ยัง**ค้างที่จุดเดิม** (โมดูลไม่เรียก `foundation.checkpoint`) ⇒ client อยู่จุดใหม่ เซิร์ฟเวอร์คิดว่าอยู่จุดเก่า · aggro/pickup/logout ใช้จุดผิด · ต้องได้คำตอบ (`ASK-COO` รอบนี้) **ก่อน**เปลี่ยนค่าคงที่ของ `RE-129` ไม่ใช่หลัง · **อัปเดตรอบ `38c4tv` 2026-08-29T08:22+07:00 (LANE-GM เจ้าของใบ) — เพิ่มด่านก่อนบูตข้อ 4 ไม่ได้ปลดหรือเพิ่มบล็อก:** จดหมาย chief `20260829_0604` ข้อ ②bis (ก) วัดได้ว่าล็อกอินที่ใช้ override ฉากเป็น **visit** ⇒ ไม่เขียนแถวตำแหน่ง ⇒ `GM_WARP_POSITION_CONFIRMED` **ไม่มีทางยิง** บนเซสชันนั้น · ใบนี้ตัดสินด้วยโทเคนนั้น จึงต้องยืนยันก่อนบูตว่าบัญชีไม่มีใบล็อกอินค้าง ทั้ง `gm_login_scene.json` และ `gm_login_scene_standalone.json` (ดูด่านข้อ 4) 🔴 กับดักซ้อน: ขั้นตอนข้อ 4 ของใบนี้เอง (`/warp <ฉากอื่น>`) เป็นตัวสตางค์ใบนั้น · **อัปเดต chief รอบ `3ru85y` (R243) 2026-08-30T~16:xx+07:00 — CORE-REQUEST-GM-030/031 wired, แต่ตัวบล็อกจริงของใบนี้ยังปิดอยู่:** `GM_WARP_POSITION_TARGET_MATCH`/`_MISMATCH` พิมพ์แล้วจริง เพิ่มจากโทเคนเดิม ไม่แทนที่ (พิสูจน์ headless: warp ตรงพิกัด -> MATCH หนึ่งบรรทัด, warp ผิดพิกัด -> MISMATCH พร้อมระยะ, เดินเองไม่มี warp -> ไม่มีทั้งคู่, target ค้างข้ามเฟรมไม่เกิด — เทสใหม่ 5 ใบใน `tests/test_gm_warp_position_confirmed.py`, สวีตเต็ม 5480 passed) · 🔴 **pf-adversary พบ**: กิ่ง `unknown_character_mismatch` ที่ `CORE-REQUEST-GM-031` ข้อ 5 ขอ เป็น **dead code ในโปรดักชัน** — ลำดับการ์ดเดิม (`character_changed` early-return) ดักทุกกรณี re-select จริงไว้ก่อนกิ่งใหม่จะถึง เทสที่พิสูจน์กิ่งนี้ต้อง park เป้าหมายตรงผ่าน `record_warp_target` เอง ไม่ใช่ผ่านเส้นทาง `/warp` จริง — [ไม่อ้าง] ว่ากิ่งนี้ทำงานได้จริงในโปรดักชัน คงไว้เป็น defense-in-depth ตามที่คอมเมนต์ใหม่ใน `runtime.py:_gm_warp_open_confirm_window` บันทึกไว้ ส่งคำถามลำดับการ์ดนี้ต่อให้ LANE-GM/COO ตัดสินว่าจะแก้หรือรับสภาพ (ดูจดหมาย `CHIEF-REPLY` รอบนี้) · pf-adversary ยังพบบั๊กเดิมที่ไม่เกี่ยวกับ diff นี้ (rearm เป็นตัวละครอื่นก่อนมี TargetPos ทำให้ `gm_warp_pending_character` ค้างชื่อเก่า แล้วโทเคนทั้งชุดเงียบทั้งเฟรมของตัวละครใหม่) — ไม่แก้รอบนี้ (นอกขอบเขตใบ) รายงานไว้ให้ทราบ · ~~🔴🔴 **ตัวบล็อกจริงของใบนี้ทั้งใบยังไม่ปลด**: `teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED` ยังเป็น `None`~~ **อัปเดต chief รอบ `9fv1m8` (R253) 2026-08-31T~02:1x+07:00: ค่าคงที่ปลดแล้ว** (`teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED = 0`, ตาม `COO-DECISION 20260830_1645`/`1742` -- ค่า RE-129 literal ไม่ใช่การอ่านชื่อ `*_PROVEN_BY_RE129`) พร้อมแก้เทส 13 ใบใน 6 ไฟล์ที่พึ่งค่า shipped เดิมโดยไม่ patch ตรง ๆ (pf-adversary รีวิวผ่านก่อน commit) สวีตเต็ม 5600 passed 0 failed เขียว(cloud sanity) · **รอ merge ก่อน** -- `pirate-force-server` PR ของรอบ `9fv1m8` ยังไม่ merge เช็ค `PR_STATE.txt` ก่อนบูต · ไบต์ `ForcePos` จะออกสายจริงเมื่อ merge แล้วเท่านั้น · ตัวบล็อกที่เหลือของใบนี้ (ลำดับการ์ด `unknown_character_mismatch` dead-code ที่ pf-adversary พบรอบ `3ru85y`, และ rearm-character bug ที่ยังไม่แก้) **ยังไม่ปลด** -- นี่คือแค่การเปิดสายไบต์ ไม่ใช่การปิดใบ ผู้เทสยังต้อง ยันหน้าจอจริงตามด่านเดิมของใบนี้]

> เลขใบ: ตัวนับเดียวร่วมกับ `CLIENT_RE_QUEUE.md` · รอบ `gr2q9j` จอง `RE-129` ที่นั่นและ `GT-128` ที่นี่
> grep ยืนยันก่อนจอง 2026-08-28T18:2x: `GT-128` / `RE-129` = 0 hit ทั้งสองไฟล์ · สูงสุดก่อนหน้า = `GT-127` / `RE-128`


### 🔵 ใบนี้อาจไม่จำเป็นถ้า `GT-016` บูตก่อน -- อ่านก่อนจัดคิว
`docs/HYPOTHESIS_LEDGER.json` และ `docs/FUNCTIONAL_COVERAGE.json` ของ repo เซิร์ฟเวอร์ระบุ `GT-016`
ไว้แล้วว่าเป็นใบ attended ที่ส่ง **ทั้งห้า channel** ของ serializer `0x65AD40` (รวม GMGlobal)
ให้ client จริงแล้วดูว่าอะไรเรนเดอร์ ⇒ ถ้า `GT-016` บูตก่อน มันตอบทั้ง "ไบต์ version ถูกไหม" และ
"branch ของ GMGlobal วาดอะไรไหม" จาก**ชั้นที่สูงกว่า** static ของ `RE-132`
(สายนี้เพิ่งรู้เรื่องใบนี้จาก pf-adversary รอบ `w8hnu9` — ไม่ได้อยู่ในสมมติฐานตอนร่างใบ)
⇒ ผู้จัดคิว: ถ้าจะบูตอยู่แล้ว ให้บูต `GT-016` ก่อน แล้ว `GT-133` เหลือแค่พิสูจน์ทางเดินของคำสั่ง GM

🔴 **chief รอบ `wi1m62` (2026-08-29T01:0x+07:00) -- `GT-016` ไม่ใช่ใบที่ "ยังไม่บูต" มันบูตไปแล้วและ PASS ชี้ขาดตั้งแต่ 2026-08-18**
`COO-DECISION 20260829_0041` ข้อ 3 สั่งให้ผมยก `GT-016` ขึ้นเหนือใบนี้ในคิว · ผมทำตามคำสั่งนั้นตรง ๆ ไม่ได้
เพราะ **`GT-016` ไม่มีอยู่ในคิวนี้แล้ว** -- อยู่ที่ `archive/GAME_TEST_QUEUE_ARCHIVE_20260818_R78_BIGROUND3.md:185`
สถานะ `✅✅ PASS ชี้ขาด` ผลเต็มที่ `archive/notes_to_chief_consumed_to_2026-08-26/20260818_1745_biground3-results.md`
**สิ่งที่ผลนั้นวัดได้จริง [วัดแล้ว 2026-08-18, ชั้น client-observable]:** พิมพ์ `PFCHATPROBE1` ครั้งเดียว
server ยิง 5 เฟรม client เรนเดอร์ 5 บรรทัด **รวมบรรทัด `[GM]` สีแดงจากเฟรม GMGLOBAL** ⇒ branch GMGlobal
ของ client **วาดจริง** และไบต์ที่ codec ของสาย CHAT-CHANNEL ใช้ (`CHANNEL_CODEC_VITAL_VERSION = 0`) ผ่านด่านของ client มาแล้วครั้งหนึ่ง
**สิ่งที่ผลนั้นไม่ได้ตอบ และยังเป็นเหตุผลที่ใบนี้บล็อกอยู่:** GT-016 บูตใต้ scenario file แบบ opt-in สองใบ
(ไม่ใช่เส้นทางไร้แฟล็ก) และ **ไม่ได้แตะเงื่อนไข (A) ตัวตนต่อ connection เลยแม้แต่ข้อเดียว**
⇒ ล็อกของ `COO-DECISION 20260829_0041` ยังยืนครบ ผมไม่ปลดอะไรทั้งสิ้นด้วยข้อมูลนี้
⇒ ข้อเสนอต่อ COO (ใบ `20260829_0103_CHIEF-GRADES-*`): ถ้าจุดประสงค์ของข้อ 3 คือ "เอาคำตอบชั้นจอมาก่อน static"
คำตอบนั้น**มีอยู่แล้ว** ไม่ต้องบูตใหม่ · ถ้าจุดประสงค์คือ "บูตซ้ำบนเส้นทางไร้แฟล็ก" ต้องเป็นใบใหม่ (`GT-016-R2`) เพราะใบเดิมปิดแล้ว

**ผู้เปิดใบ: LANE-GM (รอบ `w8hnu9`)** -- ผลกลับมาที่สาย GM บริโภค · ใบ RE ที่คู่กัน: `RE-132`


## GT-146 PICKUP-CLICK-OPCODE-CAPTURE-001 [attended, in-game]: คลิกซ้ายลงบน element ของตกที่เซิร์ฟเวอร์เราส่งเอง แล้ว **ไคลเอนต์ยิงเฟรมอะไรออกสาย** -- ใบ capture ที่ปลด `RE-125`/`GT-124`/M5  [⚪ **CANCELLED - covered by R303 attended capture 20260902_1755 (46 inbound 0x4543 frames, 2 completed takes), confirmed R306** — ปิดโดย chief (LANE-E) รอบ `m8wtlr`/R356 2026-09-05T17:0x+07:00 ตาม `COO-DECISION 20260905_0249` ข้อ 1 (ทวงเป็นครั้งที่สองโดย `COO-DECISION 20260905_1649` หลังค้าง 14 ชม.) · **คำถามของใบนี้ถูกตอบบนไวร์ไปแล้ว**: R303 จับเฟรมขาเข้า `0x4543` 46 เฟรมจากการคลิกจริง ยืนยันซ้ำ R306 · หลักฐานที่วัดบนไวร์ชนะคำสั่งที่เขียนจากชื่อใบ (`COO 0249`) · 🔴 **คำถามที่ยังเปิดอยู่ในใบนี้ไม่ได้ปิดไปกับมัน** — `REEMISSION_REDRAWS_THE_LABEL` ย้ายไปอยู่ใต้ `GT-223`/`RE-208` ของ LANE-B ในรอบเดียวกัน ตาม `COO 0249` ข้อ 1 ประโยคท้าย · ~~🔴 BLOCKED - until P-2 closes (NOW) — เงื่อนไขเดียว ไม่มีเงื่อนไขอื่น~~ · ตั้งโดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 ตาม `COO-DECISION 20260904_2349` ข้อ 5 · ที่มา: `NOW.md` หัวข้อ "ห้ามทำจนกว่า P-2 จะปิด" ระบุชื่อใบนี้ตรง ๆ · เงื่อนไข `GT-188` checkpoint 2 **ตัดทิ้งแล้ว** (`GT-188`/`GT-188cp1` ยกเลิกตาม `PANYA-DECISION 20260903_1934` · `COO 20260904_1648`) · เปิดโดย LANE-B รอบ `uq2lxw2` · แก้ขั้นตอนตาม `PANYA-ORDER 20260830_1450` ที่รอบ `xt0g9c`]

> 🔴 **บรรทัดบังคับของใบตีมอนทุกใบ (`COO-DECISION 20260902_1848` ข้อ 2 · เติมโดย LANE-B รอบ `di7ers`):**
> **ข้ามฉากแล้ววาปกลับ = เลือดมอนกลับเต็ม เป็นของที่รู้อยู่แล้ว ประกาศไม่แก้ ไม่ใช่ FAIL ของการตี**
> จะวัดว่าเลือดลดจริง ต้องตีและอ่านผล **ในฉากเดียวกัน ไม่ข้ามฉากคั่น** · ถ้าข้ามฉากแล้วกลับมาเห็นเลือดเต็ม
> ให้จดว่า `known: wound reset on scene re-open` แล้วเทสต่อ **ห้ามปิดใบเป็น FAIL ด้วยเหตุนี้**

> 🔴 **เงื่อนไขเปิดใบ (COO-DECISION `20260902_0542` ข้อ 2 · เพิ่มโดย chief R300):** ห้ามเรียกผู้เทสมาขับใบนี้จนกว่า
> **ของจะค้างอยู่บนพื้นนานพอที่ตาคนจะเห็นและเล็งคลิกได้** เหตุผลอยู่ในใบนี้เองอยู่แล้ว: ถ้า element อยู่บนจอไม่ถึงหนึ่งวินาที
> รอบนั้น**แยกไม่ออก**ระหว่าง "ไคลเอนต์ไม่ส่งเฟรมอะไรเลย" กับ "คลิกหลังของหมดอายุไปแล้ว" ⇒ ได้ผลลบที่ตีความไม่ได้ เสียรอบ attended ทั้งรอบ
> สถานะของเงื่อนไขนี้ ณ R300 (2026-09-02T08:0x+07:00) — เขียนตามที่วัดได้จริง ไม่ใช่ตามแผน:
> · ฝั่ง **ledger เซิร์ฟเวอร์** รอดแล้ว 120 วิ (`sustain_a_kill` whole-live-ledger บน main) — นั่นคือย่อหน้า 🟢 ด้านบน
> · ฝั่ง **ป้าย/ภาพบนจอ** ยัง **ไม่มีใครวัด** และทาง "ครอบ `make_runtime_vitals` ด้วย `preserve_ground_in_runtime_res_vitals`"
>   (`COO-DECISION 20260902_0347` ข้อ 2) **ถูกถอนแล้ว** ด้วย `COO-DECISION 20260902_0646` — วัดได้ว่า wrap ฆ่าเธรด `game_listener` 3 ทาง
>   ทางที่เดินแทนคือ **opt-in ทีละจุด** เริ่มที่ `action_ack` ซึ่ง **ยังไม่ขึ้น main** (chief, กำหนด R301)
> ⇒ ประตูของใบนี้คือ **`GT-188` checkpoint 2** ("วัดสภาพวันนี้") ผ่านก่อน แล้วจึงเรียกใบนี้ · ห้ามอ้างว่าเงื่อนไขเปิดผ่านเพราะ "PRESERVE อยู่บน main" — มันไม่อยู่

> 🟢 **PANYA-ORDER 20260830_1450 ขั้นที่ 1-2 ผ่านแล้ว (แก้ที่รอบ `xt0g9c`):** ตัวแปร "เล็ง" ปิดแล้วในชั้นเซิร์ฟเวอร์ --
> `mob_drop_presence.sustain_a_kill` (ชิปเข้า production ที่รอบ `m0vp7m`, ต่อสาย `runtime.py:4716-4722` แล้ว,
> `production_allowed=True` ไม่มีแฟล็ก) ส่ง **whole-live-ledger ทุกครั้งที่มีการฆ่า** แทนที่จะส่งแค่ของ kill
> เดียว ⇒ แถวที่ยังไม่หมดอายุ (120 วิ) ถูกส่งซ้ำทุกครั้งที่มีคนตายตัวใหม่ ไม่ใช่แค่ตอนเกิด headless proof:
> `tests/test_mob_drop_presence.py` 48/48 ผ่าน (รันจริงที่รอบนี้) รวม
> `test_a_second_kill_carries_the_first_kills_rows` และ `test_the_expiry_still_bounds_the_ground` --
> แถวฝั่งเซิร์ฟเวอร์ (ที่คลิกอ้างอิง) **อยู่รอด 120 วิ และคลิกได้ตลอด ไม่ถูกเก็บทิ้งเองอีกต่อไป** (เดิม
> `cell.take()` เก็บทุกคีย์ที่เพิ่งประกาศทันที -- ปิดแล้ว)
> 🟡 **สิ่งที่ยังไม่วัด (นี่คือคำถามที่เหลือของใบนี้เอง ไม่ใช่งานที่บล็อกมัน):**
> `mob_drop_presence.REEMISSION_REDRAWS_THE_LABEL = None` -- ยังไม่มีใครดูว่าป้ายชื่อบนจอ**ถูกวาดใหม่**
> เมื่อ generation ถูกส่งซ้ำหรือไม่ (แถวฝั่งเซิร์ฟเวอร์รอดแน่ ๆ แล้ว แต่ภาพบนจอเป็นคำถามฝั่งไคลเอนต์ที่วัด
> จากซอร์สไม่ได้) -- **นี่คือสิ่งที่ P0/P1-P4 ข้างล่างมีไว้ตอบ**

> NUMBERING: grep ก่อนจอง (2026-08-29T13:0x+07:00) `GT-146`/`RE-146` = 0 hit ทั้งสองคิว + `archive/` + `notes_to_chief/` · เลขสูงสุดที่ใช้ไป = 145 (`RE-` ใบจริงสูงสุด = `RE-132`) · ตัวนับเดียวสองไฟล์
> 🔴 **`GT-060` มีอยู่แล้วและห้ามลบ**: ถาม claim เดียวกัน สถานะ `BLOCKED-CONDITIONAL` บูตไม่ได้เพราะไม่มีท่า spawn drop-object และขอ "โมเดลที่คลิกได้" ซึ่ง `GT-045` ปิดไปแล้วว่า**ไม่มีโมเดล** ⇒ ใบนี้เติมท่ายิงและเลิกขอโมเดล · **จดหมาย chief `20260829_1221` ที่ว่า "ไม่มีใครเปิดใบนั้น" คลาดเคลื่อน** · ได้ผล P1/P2/P3 เมื่อไร ให้ปิด `GT-060` แบบ superseded-by `GT-146` โดยระบุชื่อ ห้ามลบก่อนมีผล
> ที่มาสามบรรทัด (รายละเอียดอยู่ในจดหมาย `20260829_13xx_LANE-B-*`): `RE-125` ปิดแบบ bounded-negative — opcode ยัง UNOBSERVED, `0x4543` derive จาก name-hash, id จริงอยู่ใน virtual-zero tail ของ `.data` ⇒ เปิดอิมเมจไม่ช่วย · `GT-046` static: request ก๊อป `+0x14` จาก **live runtime drop-object** ⇒ ไม่มีของ pre-placed ให้คลิก ต้องส่ง element เอง · มอนดรอปใช้ไม่ได้วันนี้ (`Bg0002` ตีไม่ติด · หุ่น `916` `n_DROPS_*`=0) ⇒ เหลือเลน ground-loot อย่างเดียว

### objective (ข้ออ้างเดียว)
คลิกซ้ายลงบนจุดของ element ของตกที่บูตนี้ส่งจริง **ไคลเอนต์ยิงเฟรมขาเข้าออกมาไหม และถ้ายิง nested vital id คือค่าอะไร**

### db · server args (เป๊ะ)
สำเนา `state\run_gt146.sqlite3` (+ backup `pirateforce_before_GT-146_<stamp>.sqlite3`) · **ห้ามเปิด canonical** · sha256 เทียบ `CANON_SHA.txt` ก่อน-หลัง
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt146.sqlite3 --ground-loot-hypothesis-scenario scenarios\ground_loot_hypothesis_bit08_render.json --pickup-listener-hypothesis-scenario scenarios\pickup_listener_hypothesis_decode_probe.json
```
คู่นี้บูตร่วมกันได้ (Panya 20260824 1831 §① / 2120 §②) · **สำรอง**: ถ้า `git grep` ไม่เจอเลน listener บน commit ที่จะบูต ให้ตัดสองอาร์กิวเมนต์ท้ายออกแล้วจดว่าบูตเลนเดียว — หลักฐานหลักคือ raw capture ไม่ใช่บรรทัด listener · ห้ามพ่วง `--*-scenario` อื่น · ห้ามแก้โค้ด/payload

### ขั้นตอน
0. มาตรฐานบ้าน (LOCK · boot stamp · sha canonical · copy DB) · resolve commit เขียว แล้วยืนยันบน `<SHA>` ที่บูตจริง: `git show origin/ci-status:ci/<SHA>.json` = success · `git grep -n "ground-loot-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py` · `git cat-file -e <SHA>:scenarios/ground_loot_hypothesis_bit08_render.json` · ซ้ำกับเลน listener · **ห้ามใช้ `--help` เป็นหลักฐาน**
0.5. **🔴 P0 ด่านต้นรอบ (PANYA-ORDER 20260830_1450 ข้อ ④ ขั้นที่ 3):** ยิง element ตัวแรกแล้วจับเวลาด้วยวิดีโอ (ไม่ใช่มือกดนาฬิกา) ว่าฝุ่น/ป้ายยังอยู่ให้เห็นนานกี่วินาที **ถ้ายังหายภายใน ~1 วินาทีเหมือนที่ `GT-045`/P3 เดิมวัดไว้ ให้ยกเลิกรอบทันที** บันทึกเป็น NO-RESULT (P0-FAIL, ไม่ใช่ FAIL ของใบ) แล้วส่งกลับให้สาย B วัด `REEMISSION_REDRAWS_THE_LABEL` แบบ headless เพิ่มก่อนนัดบูตรอบใหม่ — ห้ามเดินต่อขั้น 1-8 ทั้งที่ P0 ไม่ผ่าน (กันไม่ให้เผารอบของเจ้าของซ้ำ)
   🔴 **ยืนยันแล้วบน main รอบ `GT143-GT132-GT149-RESULT` (2026-08-30T15:4x+07:00, กะ1-A):** `label_life` วัดจริง
   = 0.2 วิ ไม่ใช่ ~1 วิ ⇒ **ด่านนี้จะ ABORT ทุกรอบที่บูตต่อจากนี้จนกว่า `label_life` จะยาวขึ้นจริง** (ไม่ใช่
   ความล้มเหลวของด่าน — ด่านทำงานถูกแล้ว) ก่อนนัดบูตรอบใหม่ ให้ตรวจ ASK-COO
   `notes_to_chief/20260830_1643_LANE-B-ASK-COO-label-life-reopens-drop-refresh-ban.md` ว่ามีคำเคาะหรือยัง
   — ยังไม่มี ⇒ ใบนี้ยังบูตไม่ผ่าน P0 ต่อไป อย่าเผารอบซ้ำ
   🔴 **LANE-B รอบใหม่ (scheduled) 2026-08-30T17:4x+07:00 -- อัปเดต:** ทางเลือก "สลับลำดับ `runtime.py`"
   (ทาง 2 ของใบ ASK-COO ข้างบน, CORE-REQUEST ของรอบ `qb1ytr`) **ถอนแล้ว, ไม่ใช่ทางที่เดินต่อได้** — อ่าน
   `runtime.py:4600-4824` ซ้ำพบว่า `loot_actions()` อยู่ในตำแหน่งเร็วที่สุดที่ invariant ของ
   `CORE-REQUEST-007` อนุญาตอยู่แล้ววันนี้ ไม่มีที่ให้สลับต่อโดยไม่ผิดกฎ (ดู
   `notes_to_chief/20260830_1743_LANE-B-DECISION-*.md`) ⇒ ~~ทางที่เหลือที่จะปลดด่านนี้คือ (1) COO เคาะ
   ทาง 1/3/4 ของใบ ASK-COO เดิม หรือ (2) `RE-163` (เปิดใหม่รอบนี้ ใน `CLIENT_RE_QUEUE.md`) หาสาเหตุจริง
   ของ `late_ms` แล้วชี้ทางแก้ที่ไม่ใช่ตำแหน่งคิว~~
   🔴 **ทั้งสองทางปิดแล้ว ไม่มีทางที่สาม (LANE-B รอบ scheduled 2026-08-30T19:4x+07:00):**
   (1) `notes_to_chief/20260830_1742_COO-DECISION-label-life-drop-announcement-rule-stands.md` —
   ยืนกฎเดิม (ห้ามส่งซ้ำ) ทาง 4 (NO-RESULT ที่รู้สาเหตุ) คือทางเดินต่อ ไม่มีโค้ดให้แก้;
   (2) `notes_to_chief/20260830_1805_RE-163-RESULT-*.md` — `late_ms` เป็น sender-side diagnostic
   overhead ใน `current/pf_login_game_server_v141.py` (frozen) ไม่ใช่ตำแหน่งคิวหรือ network latency,
   `BUILD_IMPACT_NONE`, ไม่มีทางแก้จาก `src/` ⇒ **P0 นี้ยังคง ABORT ทุกรอบต่อไป จนกว่าจะมีบูต attended
   ที่วัด `REEMISSION_REDRAWS_THE_LABEL` ตรง ๆ ตามเงื่อนไขที่ COO-DECISION ข้อ 23-25 วางไว้ (ยิงซ้ำครั้งเดียว
   แล้ววัดว่าป้ายกลับมาไหม ก่อนเสนอ COO ใหม่) — ไม่ใช่งานที่ค้างอยู่กับ LANE-B วันนี้**
1. server ก่อน client เสมอ · เข้าเกม (ปุ่มกลางจาก 5 ปุ่มแถวล่าง · ซ้ายสุด = ลบตัวละคร ห้ามกด)
2. **อัดวิดีโอตั้งแต่ก่อนเข้าแมพเสร็จ** — เฟรมของตกออก **ครั้งเดียวต่อเซสชัน** ที่ TargetPos แรกหลัง runtime ack · ออกตอนไม่ได้อัด = NO-RESULT · **ห้ามพิมพ์ตัวอักษรตลอดรอบ**
3. ในแมพ **ห้ามแตะ `W/A/S/D` และ `Q`/`E`** (ยิง `TargetPosVital` ทิ้ง) · จัดกล้องด้วย **คลิกขวาค้างลาก** เท่านั้น · หันไปทาง +X · **S0** ให้เห็น X/Y บน HUD
4. **ยิง:** กด `W` สั้นที่สุด (~120 ms) ครั้งเดียว · จดเวลา (+07:00) และ `t` วิดีโอ · จด `X0/Y0` · ตาอยู่ที่จอ (ฝุ่น ~0.45 s · ป้าย 0.2-0.4 s) — **นี่คือ P0 ด้านบน วัดพร้อมกันครั้งเดียว**
5. **คลิก 1 (ตอนยังเห็น):** เลื่อน cursor ไปที่ฝุ่น/ป้าย คลิกซ้ายหนึ่งครั้ง · จดเวลา · หายก่อนคลิกทันไม่ใช่ความผิดพลาด
6. เดินไปทาง X เพิ่มจนราว `X0+30` (Y คงเดิม) · hover แล้ว **จดว่า cursor เปลี่ยนรูปไหม** · **S1**
7. **ข้อสังเกตเสริม (ไม่ใช่หลักฐานหลัก, PANYA-ORDER ④ ขั้นที่ 3):** ถ้า P0 ผ่านและมีเวลาเหลือ อาจคลิกซ้ำที่จุดเดิมอีก 1 ครั้งหลัง element หายจากจอ เพื่อดูว่า element ที่ยังอยู่ในลิสต์ฝั่งเซิร์ฟเวอร์ (120 วิ ตาม `mob_drop_presence`) ยังคลิกโดนไหมทั้งที่มองไม่เห็น — บันทึกแยกจาก P1-P4 ห้ามใช้แทน P1-P4 · **S2** หลังคลิกสุดท้าย 10 วิ
8. NO-CRASH ด้วยคลิกขวาค้างลาก (ห้าม `Q`/`E`) · **S3** · ออกเกมด้วย X มุมขวาบน
9. ปิด server (**restart ก่อนบูตถัดไปเสมอ**) · เก็บ `capture_gt146_<stamp>\capture_v141\GAME_LIVE.txt` ทั้งไฟล์ + console `.out`/`.err` + sha256 ทุกไฟล์ · `PRAGMA integrity_check` · **teardown เสมอ** · sha canonical ซ้ำ · ห้าม commit เอง
10. ค้นในผล (คัดดิบ ห้ามตีความ): `findstr /N /C:"RECV" GAME_LIVE.txt` · `/C:"0x4543"` · `/C:"NEAR_ONCE"` · `/C:"FAR_ONCE"` · `findstr /N /C:"PICKUP" server_console_live.*.txt`

### pass criteria (สองชั้น 🔴 ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)
**wire** — (ก) มี `NEAR_ONCE` + `FAR_ONCE` (54 B) = ยืนยันว่ามี element ถูกส่ง (precondition ไม่ใช่ claim) ไม่มี = P4 · (ข) สำมะโน `RECV` ทั้งไฟล์ แล้วเทียบหน้าต่าง ±2 วิ รอบคลิกแต่ละครั้งกับ baseline ก่อนคลิก ⇒ (1) มี id `0x4543` · (2) มี id อื่นที่ไม่มีใน baseline (คัด id + hexdump เต็ม) · (3) ไม่มีเฟรมนอก baseline · (ค) ถ้าบูตเลน listener: หนึ่งบรรทัดต่อเฟรม พร้อม `object_ref_u32`/`opaque_u8`/raw hex จำนวนตรงกับจำนวนคลิก — **ไม่มีบรรทัด listener ตัดสินอะไรไม่ได้** (id ที่ไม่ match ไหลลง frozen dispatch เงียบ) ⇒ **capture คือกรรมการ** · (ง) DB สำเนา `integrity_check`=ok · `sessions` +1 ต่อการเข้าเกม · sha canonical ตรงก่อน-หลัง
ชั้นนี้ตอบไม่ได้: มีอะไรบนจอไหม คลิกโดนอะไรไหม
**client-observable** — วิดีโอต่อเนื่อง + `S0..S3` full-res พร้อม sha256 · ตอบสามช่องเป็นภาษาคน: ฝุ่นขึ้นไหมกี่วิ · ป้ายขึ้นไหมอ่านว่าอะไรกี่วิ · cursor เปลี่ยนรูปตอน hover ไหม · หลังแต่ละคลิก: จอเปลี่ยนไหม มีข้อความระบบไหม (คัดเป๊ะ + สี) · **จดสีป้ายชื่อทุกป้ายทุกภาพ** อ่านจาก full-res เท่านั้น ไม่มีป้ายเขียน `none` · **จดสีอย่างเดียว ห้ามเดาสาเหตุ** (`RE-067`) · NO-CRASH/CRASH
ชั้นนี้ตอบไม่ได้: เฟรมออกจากไคลเอนต์จริงไหม id อะไร

### คำทำนาย (ผิด = ผล ไม่ใช่ความล้มเหลว)
**P1** เจอ `0x4543` ⇒ id ที่ derive ไว้ CONFIRMED · **P2** เจอ id อื่น ⇒ REFUTED **และได้ id จริงมาแทน มีค่าเท่า P1** · **P3** คลิกครบแล้วเงียบ ⇒ ผลลบที่วัดแล้ว มีค่าเท่าผลบวก (redirect = ใบ static ว่าใคร populate ลิสต์ของ `DropThingModule_Client`) 🔴 **ระยะไม่ใช่คำอธิบาย**: 30 หน่วย เทียบ `RANGE_PICKUP 600.0` · **P4** ไม่มี `NEAR_ONCE`/`FAR_ONCE` ⇒ NO-RESULT แยกอะไรไม่ได้ ห้ามอ่านเป็นผลลบเรื่อง opcode
🔴 **ผลลบไม่ปิดใบ** P3/P4 ห้ามปิดใบ ห้ามลบวิดีโอ (กติกาผลลบไม่ถูกแตะโดย `PANYA-ORDER 20260829 0930`)

### กฎจุดเกิด (`PANYA-ORDER 0930` ข้อ ④)
พิกัดของตก **อิง trigger** ⇒ element โผล่ที่ `trigger+30X` = ใกล้ ในระยะ (30 ≪ 600) และเยื้องหน้าโดยโครงสร้าง **ไม่ต้อง seed พิกัดลง DB และไม่มีตารางวางวัตถุให้ mine** (`GT-046` จ็อบ 5: `+0x14` มาจาก runtime drop-object ไม่ใช่โครงสร้างฉาก) · ค่าคาดหมายจาก `GT-045`: trigger `X -8553.947 Y -2579.689 Z 186.000` (คาดหมาย ไม่ใช่เกณฑ์)

### nonclaims
1. ไม่พิสูจน์ว่าเก็บ**สำเร็จ** หรือของเข้ากระเป๋า (`GT-142`) · เซิร์ฟเวอร์ไม่ตอบอะไรในใบนี้ ⇒ ทุกปฏิกิริยาบนจอเป็นพฤติกรรมไคลเอนต์ล้วน
2. ไม่อธิบายการเก็บของที่**มอนดรอป** (`FightingDropModule_Client`/`FightingDropNotify` ยัง NOT_OBSERVED)
3. ไม่ตอบว่า element ฝั่งเซิร์ฟเวอร์อยู่ในลิสต์นานแค่ไหน (ตอบแล้วนอกใบนี้ -- `mob_drop_presence`,
   120 วิ, headless-proven) และไม่ตอบว่าทำไมป้ายบนจอหาย (คำถามฝั่งไคลเอนต์ที่ยังไม่มีใบเปิดตรง ๆ ณ
   รอบ `xt0g9c`; `REEMISSION_REDRAWS_THE_LABEL` ที่ใบนี้เพิ่งเริ่มวัดคือคำตอบที่ใกล้ที่สุด แก้จาก `GT-132`
   ที่เดิมชี้ผิด -- `GT-132` วัดจำนวนป้ายต่อการตายหนึ่งครั้ง ไม่ใช่อายุ) · ไม่ตัดสินสาเหตุของสีป้าย (`RE-067`)
4. **ไม่นับเป็นเวอร์ชัน** — รอบที่รันใบนี้ ship ศูนย์บรรทัด แฟล็กเป็นเครื่องมือวัด · ไม่ต่อ production call site ใด ๆ (`RE-125` ห้าม `0x4543` บน production path)
5. การเทียบ `object_ref_u32` กับ element key = งานตอนบริโภคผล ผู้เทสไม่ต้อง decode

### links
`RE-125`/`RE-130` (`CLIENT_RE_QUEUE.md`) · `notes_to_chief/20260828_1112_RE-125-RESULT-NO-CAPTURED-PICKUP-OPCODE.md` · `notes_to_chief/20260829_1221_CHIEF-ASK-COO-gt124-opcode-forbidden-and-drops-pruned.md` · `GT-060`/`GT-124`/`GT-132`/`GT-142` · `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md` (`GT-045` `GT-046`) · `external/PF_FIELD_VALIDATION.tsv:102-103`

### result (ผู้เทสกรอก)
P1/P2/P3/P4 · เวลาคลิกทุกครั้ง (+07:00 และ `t` วิดีโอ) · path + sha256 ของ log/console/ภาพ/วิดีโอ · สำมะโน `RECV` + hexdump ช่วงคลิก · บรรทัด listener ทั้งบรรทัด · สามช่อง ฝุ่น/ป้าย/cursor · สีป้ายทุกป้ายทุกภาพ · NO-CRASH/CRASH · sha canonical ก่อน-หลัง · `integrity_check`

---


## 🆕🔬 GT-159 M2-DEST-COLUMBUS-MARKER17-TRANSFORM-TO-SHIP-001 [attended, in-game]: ถ้าเซิร์ฟเวอร์เคยส่งฉาก 126 ที่ `MARKER[17]` พิกัด `(3050, 232, 90)` หันหน้า 6 แทนฉาก 17 -- ผู้เล่น**แปลงร่างเป็นเรือและอยู่ในทะเล**ตามที่เจ้าของจำได้ (`GT-106` ข้อ ④.2) จริงหรือไม่ -- ตัดสินด้วยตา ไม่ใช่ด้วยการเถียงตาราง  [⚪ **CANCELLED - covered by `GT-266` · no longer needs proving because `PANYA-DECISION 20260905_1329`** -- ปิดโดย chief (LANE-E) รอบ `m8wtlr`/R356 2026-09-05T17:0x+07:00 ตาม `COO-DECISION 20260905_1543` · **สองครึ่งของใบตายคนละทาง**: (ก) ครึ่ง "มาถึง 126 ที่ MARKER 17 (3050,232,90) แล้วเป็นเรือในทะเลจริงไหม" = `GT-266` วัดตรงตัว (จุดมาถึงเดียวกัน วัตถุที่ต้องเห็นเดียวกัน · กลไกขนส่งต่างกันไม่เปลี่ยนสิ่งที่ตาเห็น) · (ข) ครึ่ง "`DESTINATION_SCENE_N_ID = 17` อ่านใน id space ไหน" = **ไม่ต้องพิสูจน์แล้ว** เพราะ `PANYA-DECISION 20260905_1329` เคาะจุดมาถึง 126 = MARKER `n_ID 17` ถาวร — คำถาม id space ตายด้วยคำสั่ง ไม่ใช่ด้วยการเทส · 🔴 **สิ่งที่ยังไม่ถูกตอบและห้ามผูกกับใบนี้อีก**: Columbus ยังชี้ฉาก 17 บน main (`world_m2_sea_destination.py:314`) — เมื่อ LANE-A แก้ปลายทาง Columbus → 126 เป็น PR จริง **ใบ GT ของ PR นั้นออกใหม่ตอนนั้น** ไม่ใช่เก็บใบนี้รอ (`COO 1543` ข้อ 3 · เวลา attended แพงที่สุด `PANYA 20260903_1934`) · ~~🔴 BLOCKED (คงเดิม) -- การปิดใบของ chief รอบ `r045nx`/R354 ถูกถอน ในรอบเดียวกันหลัง `pf-adversary` D4 · ใบนี้ยังไม่ปิด และรอ COO ตัดสิน~~ **COO ตัดสินแล้ว `1543`**
> 🔴 **ที่ถอนและทำไม (chief เขียนเอง ไม่ใช่ให้ใครมาจับได้ทีหลัง)**: `COO-DECISION 20260905_1349` ข้อ 5 ให้ทางเลือกสองทางเท่านั้น — "ถ้าใช่ปิดด้วย `CANCELLED - covered by <GT ใหม่>` **ถ้าไม่ ระบุว่าต่างตรงไหน (สั้น)**" · chief สรุปเองว่าใบ `/warp 126` ใหม่ (`GT-266`) **ไม่ครอบ** ใบนี้ = ตกเข้าทาง "ถ้าไม่" ซึ่งอนุญาตแค่ให้**เขียนความต่าง** แต่ chief กลับปิดใบด้วยตัวครอบที่ COO ไม่ได้เอ่ยถึงเลย ⇒ **เกินอำนาจ** และขัดบรรทัดในหัวใบนี้เอง ("ห้ามปิดเองจนกว่า COO ตัดสิน" · `PANYA-DECISION 20260903_1934`)
> 🔴 **และข้ออ้างที่ใช้ปิดก็เกินจริง**: คำถามของใบนี้ไม่ใช่ "ฉาก 126 เป็นทะเลไหม" แต่คือ **กด Columbus (quest 3021) บนเซิร์ฟเวอร์ที่ถูกแก้ให้ส่ง 126@`MARKER[17]` แทน 17 แล้วเกิดอะไร** — เพื่อแยกสอง id space ที่ `world_m2_sea_destination.py:305-314` ประกาศเองว่า `[CONTESTED]` และ "no control in any table separates them" · บูตของ `GT-233` ทุกครั้งเข้าฉาก 126 ผ่าน `PF_M2_SURVEY_TRIAL` + relogin **ไม่เคยแตะ `columbus_quest_dispatch` หรือแถว 3021 เลย** ⇒ ไม่แยก id space ให้สักนิด · กิ่งผลลบของใบ ("ยังเป็นคน ไม่ได้อยู่ในทะเล เช่นยืนอยู่ฉาก 17") ไม่มีใครเคยเห็น
> 🔴 **และป้าย `OBSERVER_CONFIRMED 12:48` ถูกยืมผิดที่**: ใน R318 §2.2 ป้ายนั้นเซ็นประโยค "**ไม่มีหน้าต่างอะไรเด้ง**" (ผลลบของ `GT-233`) ส่วน "เป็นเรือ" อยู่ในย่อหน้าเดียวกันแบบ**ไม่มีลายเซ็น** ("`HP -1/1` ขณะเป็นเรือ (สังเกตการณ์)") — ย้ายป้ายข้ามข้ออ้างแบบนี้ผิด `G-OBS`/`G5` ตรง ๆ
> ⇒ **ที่ chief ทำได้ตามอำนาจจริงคือบรรทัดเดียวนี้**: `GT-266` (`/warp 126` สด) **ไม่ครอบ** ใบนี้ — `GT-266` ถามว่า "วาปสดขณะเล่นไปโผล่ 126 ได้ไหมโดยไม่ relogin" ส่วนใบนี้ถามว่า "`DESTINATION_SCENE_N_ID = 17` อ่านใน id space ไหน" ซึ่งต้องกด Columbus บนบิลด์ที่แก้ปลายทาง · **เสนอ COO: ใบนี้ยังจำเป็นหรือไม่ ในเมื่อกลไก M2 ที่เดินอยู่จริงคือ `RE-227`/`GT-233` ไม่ใช่การสลับปลายทางของ Columbus** — คำตอบเป็นของ COO ไม่ใช่ของ chief
> เดิม (ถอนแล้ว ไม่ลบเพื่อเป็นประวัติ): ~~`CANCELLED - covered by GT-233 boots R313/R315/R317/R318`~~
> เดิม: 🔴 **BLOCKED** · `STATUS-SET-BY-CHIEF 2026-09-05T02:0x+07:00 from body` ตาม `COO-DECISION 20260904_2349` ข้อ 6]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง 2026-08-30T14:2x+07:00: `GT-159`/`RE-159` = 0 hit ทั้งสองไฟล์ ·
> สูงสุดก่อนหน้า `GT-158` (`GT`/`RE` ใช้ตัวนับเดียวร่วมกัน ตามกฎที่ `RE-152` หัวใบเคยระบุไว้)
> ⇒ ใบนี้คือ `GT-159` · ใบ `RE-085`-`RE-158`/`GT-001`-`GT-158` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ

### ที่มา

`COO-DECISION 20260830_1351 (m2-destination-held-at-17-escalated-to-owner)` สั่งให้ LANE-A
"รันการทดสอบเชิงสังเกตที่เสนอไว้ก่อน (ฉาก 126 ที่พิกัด marker แปลงร่างเป็นเรือจริงหรือไม่) แล้วค่อยเอาผล
ไปให้เจ้าของตัดสิน" -- ทางเลือกที่ 3 ของใบ `20260829_1410_LANE-A-ASK-COO-var2-is-a-markerid.md` เอง คือ
ใบเทสนี้ ไม่ใช่การแก้โค้ด: คำถามที่เหลือ (17 หรือ 126 คือปลายทางจริงของ M2) เป็นคำถาม client-observable
ล้วน (สองการอ่านตารางให้คำตอบต่างกัน ทั้งคู่วัดได้เท่ากันจากซอร์ส) ไม่มีทางปิดได้ด้วย static อีกต่อไป

`world_m2_sea_destination.DESTINATION_SCENE_N_ID` ยังเป็น `17` บน `main` วันนี้ (production path ไม่มี
แฟล็ก) แท็ก `[CONTESTED]` ติดไว้ที่ docstring/console token (`var2_reading=CONTESTED`) ตั้งแต่รอบ `drrnpu`
-- ใบนี้ไม่แตะโค้ดนั้น เป็นใบสังเกตการณ์ล้วน

### objective

ให้ผู้เทสยืนที่ Port Royal กด Columbus (option แรก, quest 3021) **ด้วยเซิร์ฟเวอร์ที่ถูกแก้ให้ส่งฉาก 126
ที่พิกัด `(3050, 232, 90)` หันหน้า 6 แทนฉาก 17 ชั่วคราว** (เปลี่ยนที่เดียว:
`world_m2_sea_destination.DESTINATION_SCENE_N_ID = 126` + จุดพิกัด -- ทำใน branch ทดลองแยก ไม่ใช่ `main`,
ไม่ commit ค่านี้ทับของจริง) แล้วสังเกตว่าไคลเอนต์:

1. แปลงร่างตัวละครเป็นเรือหรือไม่ (โมเดล/แอนิเมชันเปลี่ยนจากคนเป็นเรือ)
2. พื้นที่รอบตัวเป็นทะเล/มหาสมุทรหรือไม่ (ไม่ใช่เกาะ/ท่าเรือ)
3. HUD/ชื่อแมพที่ขึ้น ตรงกับ "Atlantic Ocean: Rising Sun Sea" หรือชื่อพาแนลทะเลที่โฆษณาไว้หรือไม่

### pass criteria

**ชั้น client-observable (ปิดคำถามได้ชั้นเดียวพอ เพราะเป็นคำถาม client-observable ล้วนตามที่เจ้าของ
เคยอธิบายไว้ใน `GT-106` ข้อ ④.2):**
- ตัวละครแปลงร่างเป็นเรือจริงและอยู่ในทะเล ⇒ การอ่านแบบ **marker (126)** ถูก -- ส่งผลให้ `COO-DECISION`
  ต้องพิจารณากลับคำ `DESTINATION_SCENE_N_ID` เป็น `MARKER[17].n_SCENE` (126) ในรอบถัดไป
- ตัวละครไม่แปลงร่าง ยังเป็นคน ไม่อยู่ในทะเล (เช่น ยืนอยู่บนฉาก 17 ที่ไม่ใช่ทะเล) ⇒ การอ่านแบบ
  **scene table (17)** ถูก -- ยืนตามใบ `0441`/`main` ปัจจุบันต่อไป

### nonclaims

1. ไม่อ้างว่าใบนี้ปลดล็อก M2 ทันที -- ใบนี้ตอบแค่ "17 หรือ 126" หนึ่งคำถาม การเดินสายจริงเข้า `main`
   (ถ้าคำตอบคือ 126) เป็นงานร่วมของ chief + สาย A รอบถัดไปตามที่ใบ `var2-is-a-markerid` เขียนไว้แล้ว
2. ไม่อ้างว่าการทดสอบนี้ต้องรัน production build -- ใช้ branch ทดลอง/เซิร์ฟเวอร์แยกที่แก้ค่าคงที่ตัวเดียว
   ชั่วคราว ห้าม commit การแก้นั้นเข้า `main`
3. ไม่อ้างว่าผลลบ (17 ถูก) แปลว่า M2 เสร็จ -- ปลายทางที่ยืนยันแล้วยังต้องการ CORE-REQUEST อื่นตามที่
   `world_m2_sea_destination.py` ระบุไว้ (จุดมาถึงจริงยังไม่ต่อสาย)

### links

`notes_to_chief/20260830_1351_COO-DECISION-m2-destination-held-at-17-escalated-to-owner.md` ·
`notes_to_chief/20260829_1410_LANE-A-ASK-COO-var2-is-a-markerid.md` (ทางเลือกที่ 3) ·
`notes_to_chief/20260827_1710_GT106-RESULT-...-owner-objects-dest-126-...md` ข้อ ④.2 ·
`src/pirateforce_foundation/world_m2_sea_destination.py` (`DESTINATION_SCENE_N_ID`, บรรทัด 183-190,
306-314) · `src/pirateforce_foundation/columbus_quest_dispatch.py`

**ผู้เปิดใบ: LANE-A (สาย A · WORLD) รอบ `12lyda` 2026-08-30T14:2x+07:00** -- เขียนตามคำสั่งตรงของ
COO-DECISION รอบนี้ ไม่ใช่ริเริ่มเอง

---


### สืบต่อ GT-134 (ไม่ปิด ไม่ย้าย ไม่ทับ)
`GT-134` ปิดแล้ว **PASS** สำหรับคำถาม "มีสิ่งมีชีวิตขึ้นจอในฉาก 14 ไหม" (81/91 ขึ้นจอจริง) --
แต่ nonclaim ข้อ 1 ของใบนั้นตอบคำถาม "ก้าวร้าวไหม" ไปแล้วด้วยผลลบ: ทุกตัวเป็น NEUTRAL ไม่ถือ
faction bit เลย ("มอนสเตอร์ที่ไม่เข้าตี = ผลที่คาดไว้ ไม่ใช่ FAIL" -- เจตนาเว้น scope ให้สาย B)
ใบนี้คือใบที่ถามคำถามที่ GT-134 ตั้งใจไม่ตอบ: **เฉพาะ 11 ตัวที่รอบนี้ splice (หลัง `#803` กัน placement 87 ออก) ใหม่** อ่านเป็นศัตรูจริง
บนจอหรือไม่ -- คนละ claim กับ GT-134 ห้ามใช้ผลของใบหนึ่งปิดอีกใบ

### objective (claim เดียว)
เดินเข้าใกล้หนึ่งใน 12 placement ที่ `field_mob_hostile_bg0015.scene14_hostile_overrides()` splice
faction เข้าไปแล้ว -- มันแสดงพฤติกรรมศัตรู (ป้ายชื่อสีศัตรู และ/หรือ เข้าตีเมื่อเข้าใกล้) ต่างจากอีก 70
ตัวที่เหลือ (ยังเป็นพลเรือนเหมือน GT-134 วัดไว้) หรือไม่

### pass criteria — สองชั้น แยกกัน ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น

**wire/DB (ปิดแล้วโดยเทส -- ชั้นนี้ผู้อ่านแค่ยืนยัน ไม่ต้องรันซ้ำ):**
- `tests/test_field_mob_hostile_bg0015.py::FieldMobHostileBg0015Tests::
  test_splice_proof_changes_exactly_the_twelve_identities_and_nothing_else` และ
  `::test_splice_proof_is_reachable_through_the_generic_recompose_splice` -- พิสูจน์กลไก splice
  ที่ระดับไบต์มาก่อนรอบนี้แล้ว (ตัว dict/ตัว splice ถูก ก่อนมีจุดเสียบจริง)
- `tests/test_world_population_handoff.py::HandoffTests::
  test_a_composed_scene_gets_its_own_roster_and_never_the_dock_census` (แก้รอบนี้) -- ยืนยันว่า
  `handoff.pc`/`handoff.frame` ของฉาก 14 ตอนนี้ **เท่ากับ** `splice_identity_override(direct, ...)`
  ไม่ใช่ `direct` (สำมะโนพลเรือนดิบ) อีกต่อไป
- full suite เขียวรอบนี้ (chief report: 5972+ passed, ไม่มีแดงใหม่, skip เดิม)
- 🔴 **เกณฑ์นี้ตอบแล้วว่า YES** -- ไม่ต้องบูตเซิร์ฟเวอร์ซ้ำเพื่อพิสูจน์ชั้นนี้

**client-observable (ยังไม่มีใครยืนดู -- นี่คือสิ่งที่ใบนี้ต้องการ ต้องมีคนอยู่หน้าจอเท่านั้น):**
- ที่ 1 ใน 11 placement ที่ส่งจริง (`SHIPPED`): เห็นพฤติกรรมต่างจากพลเรือน (ป้ายชื่อเปลี่ยนสี และ/หรือ เข้าตี
  เมื่อเดินเข้าระยะ) -- ถ่ายภาพนิ่ง full-res
- ที่อย่างน้อย 1 placement ที่ไม่อยู่ใน 11 ตัวนั้น (และไม่ใช่ placement 87): ยังนิ่งเหมือนที่ GT-134 วัดไว้ (ควบคุมเทียบ)
- **สีของทุกป้ายชื่อในทุกภาพ** จดแยกบรรทัดต่อป้าย ("none" ถ้าไม่มีป้าย) จากภาพนิ่ง full-res เท่านั้น
  -- ถ้าต่างจากภาพเซิร์ฟเวอร์จริง บันทึกลง `REAL_SERVER_DIVERGENCE.tsv`
- ห้ามอนุมานสาเหตุของสี (คำถามเปิดของ `RE-067`) -- จดสีเฉยๆ
- ❗ **negative มีค่าเท่ากับ positive**: ถ้าทั้ง **11 ตัวที่ส่งจริง** ยังนิ่งเหมือนพลเรือนทุกตัว (placement 87 ไม่นับ ถูกกันไว้เอง) (ไม่ต่างจาก GT-134
  เลย) ⇒ จดละเอียดเท่าผลบวก แล้ว redirect ไปตรวจฝั่ง client-side interpretation ของ faction byte
  (`mob_aggro.py` หรือคำถามเดียวกับ `RE-067`) -- **ไม่ใช่การหักล้าง wire tier ที่ปิดไปแล้วข้างบน**
  เพราะไบต์ถูกยืนยันแล้วว่าออกไปจริง คำถามที่เหลือมีแค่ "ไคลเอนต์อ่านมันยังไง"

### เกณฑ์ตัวคุม 11 ตำแหน่งที่ส่งจริง (+ ตัวที่ถูกกันไว้) -- ห้ามเดา ต้องอ่านจากโค้ดก่อนบูต
ไม่มีบรรทัดคอนโซลไหน (รวม `WORLD_CENSUS_BG0015` และ per-actor lines เดิม) พิมพ์ว่าตัวไหนถูก splice
-- `actor_lines()` อ่านจากสำมะโนพลเรือนดิบเสมอ (`world_population_bg0015.py:438-458`) ไม่รู้เรื่อง
splice เลย ก่อนบูตให้รันจากเชลล์ repo (ไม่ใช่การกระทำในเกม):
```
py -3 -c "from pirateforce_foundation import field_mob_hostile_bg0015 as h
for m in h.scene14_shipped_hostile_roster():
    print('SHIPPED', m.placement_index, m.template_id, m.display_name, m.level, m.max_hp, m.x, m.y, m.z)
shipped = {m.placement_index for m in h.scene14_shipped_hostile_roster()}
for m in h.scene14_hostile_roster():
    if m.placement_index not in shipped:
        print('WITHHELD', m.placement_index, m.template_id, m.display_name)"
```
บรรทัด `SHIPPED` คือแหล่งเดียวที่ถูกต้องของ **11 ตำแหน่งที่สายส่งจริง** และบรรทัด `WITHHELD` คือตัวที่ถูกกันไว้โดยเจตนา (คาดว่านิ่ง ห้ามนับเป็นผลลบ) -- จด placement_index/ชื่อ/พิกัดที่พิมพ์ออกมาจริงไปใช้เดินหา
ห้ามพิมพ์เลขเดาเองหรือเชื่อเลขจากรอบอื่น (ตารางเปลี่ยนได้ถ้าใครแก้ `DEFAULT_HOSTILE_PLACEMENT_INDICES`)

### db / server args (เป๊ะ -- เหมือน GT-134 ทุกประการ ดูใบนั้นสำหรับเหตุผลละเอียด)
สำเนา `state\run_gt177.sqlite3` -- ห้ามเปิด canonical `state\pirateforce.sqlite3`, sha256 ก่อน-หลัง
ต้องเท่ากัน
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt177.sqlite3
```
🔴 ห้ามมีแฟล็ก `--*-scenario` ใด ๆ และห้าม `--second-password-mode bypass` ฝั่งเซิร์ฟเวอร์ (ไม่งั้น
dispatcher ข้ามกิ่งสำมะโนฉาก 14 ไปเลย ตามที่ `GT-134` วัดไว้แล้ว) · client `-SecondPasswordMode bypass`
ใช้ได้ตามเดิม (คนละตัว) · 🔴 restart เซิร์ฟเวอร์ก่อนบูตไคลเอนต์ทุกครั้ง · เข้าฉาก 14 ด้วยกลไกเดิมของ
GT-134 (GM login-scene override หรือ `/warp 14`) · NO-CRASH ด้วย right-click-drag เท่านั้น (ไม่ใช่
Q/E) ที่จุดยืนเริ่มต้น -- การเดินเข้าใกล้มอนด้วย W/A/S/D คือส่วนหนึ่งของการทดสอบเอง ไม่ใช่ NO-CRASH
check · teardown ภายใน 420 นาทีจาก boot stamp

### nonclaims
1. ไม่พิสูจน์ดาเมจ/HP loss จากการถูกตีจริง -- วัดแค่ aggro/approach behavior
2. ไม่พิสูจน์ว่า 69 ตัวที่เหลือ "ไม่มีทางก้าวร้าวได้เลย" -- บูตเดียว จุดเดียว
3. ไม่แยกทดสอบ M2 crossing เป็นบูตต่างหาก (ยืนยันจากโค้ดว่าจุดเสียบเดียวกัน แต่ใบนี้เดินผ่านทาง
   login เท่านั้น -- ถ้าต้องการ attended evidence ของทาง crossing เปิดใบใหม่แยก)
4. ไม่ตัดสินสาเหตุของสีป้ายชื่อ (`RE-067` ยังเปิด)
5. ไม่ปิด/ไม่รอผล `pf-adversary` -- สถานะนั้นแยกจากใบนี้โดยสิ้นเชิง (ผลออกมาแล้ว: CONFIRMED defect,
   ดูกล่องด้านบน)
6. ไม่เลื่อนสถานะ identity ของ `Bg0015` ให้สูงกว่าที่ `COO-DECISION` เคาะไว้แล้ว
7. ไม่ปิดช่องโหว่ ChooseNPC (`lane_hooks/lane_a_choose_npc_scene14.py`) ในใบนี้ -- ไฟล์ของสาย A, ขอไป
   แยกต่างหากแล้ว (ดู links)

### สัญญาผู้บริโภค
เปิดโดย chief -- LANE-A/LANE-B ร่วมบริโภคผล

### links
`src/pirateforce_foundation/world_population_handoff.py::_roster_handoff` (บรรทัด 983-998) ·
`src/pirateforce_foundation/field_mob_hostile_bg0015.py` ·
`tests/test_field_mob_hostile_bg0015.py` · `tests/test_world_population_handoff.py::HandoffTests` ·
`notes_to_chief/20260831_2318_CHIEF-TO-LANE-A-choosenpc-scene14-reverts-hostile-splice-to-civilian.md`
(CONFIRMED ChooseNPC defect + ที่ขอสาย A) ·
`notes_to_chief/20260831_2151_LANE-A-TO-CHIEF-scene14-hostile-splice-core-request-both-halves-confirmed-built.md` ·
`notes_to_chief/20260831_2007_LANE-A-TO-LANE-B-scene14-hostile-splice-design-proposal-re092.md` ·
`notes_to_chief/20260831_2053_LANE-B-TO-LANE-A-scene14-hostile-splice-confirmed-and-built-re092.md` ·
`GT-134` (supersedes/updates -- see relationship note above, GT-134 stays PASS/closed as-is)

### result (ผู้เทสกรอก)
```

```


## GT-188 GROUND-DROP-HEARTBEAT-PRESERVE-CONFIRM-001  [**checkpoint 1 = ❌ CANCELLED - covered by GT-216** (🟢 PASS สองชั้น · `OBSERVER_CONFIRMED 2026-09-03T16:51+07:00`) · **checkpoint 2 = 🔵 MEASURED (BASELINE) รอบ R309 — ผลคือ "หาย"** ยังไม่ปิดใบ · ปิด cp1 โดย chief รอบ `oi2r2n`/R340 ตาม `COO-DECISION 20260904_1648` ข้อ 3 + `PANYA-DECISION 20260903_1934`]

> **checkpoint 1 คำต่อคำ**: "ของที่ตกยังเห็นอยู่บนจอข้าม heartbeat ~2 วิ อย่างน้อยสองรอบ (~4-5 วินาที ไม่หยิบ)" — `GT-216` **PASS สองชั้นบนจอเจ้าของ R306** วัดสิ่งที่แรงกว่านั้นไปแล้ว: เจ้าของคลิกเก็บ **10 ครั้ง เข้ากระเป๋า 9** ในรอบเดียว ⇒ ของอยู่บนพื้นนานกว่าสอง heartbeat หลายเท่า มิฉะนั้นคลิกครั้งที่สองก็ไม่มีอะไรให้คลิก · R307 (`GT-220`) เห็นซ้ำอีกครั้ง ของค้างเป็นนาทีจนหมดอายุ 120 วินาทีกลายเป็นของผี
> 🔴 **สิ่งที่การปิด cp1 ไม่ได้อ้าง**: ไม่ได้อ้างว่า `preserve_ground_heartbeat_frame` เป็นเหตุของผลนั้น (ใบตั้งคำถามชั้นจอ ไม่ใช่ชั้นสาเหตุ) · ไม่ได้อ้างว่าอ่าน reconciler ของ Codex ถูก — ใบเดิมก็เขียนไว้เองว่าไม่อ้าง
> 🔵 **checkpoint 2 ยังไม่ปิด และ COO สั่งยกเลิกเฉพาะ cp1**: cp2 ("หนึ่ง action ที่ถูกตอบ ล้างพื้นไหม") **ถูกวัดโดยบังเอิญในรอบ R309** — S4: เจ้าของเปิดกระเป๋ารอโดยไม่คลิกอะไร แล้วของบนพื้น**หายเอง** · สาย: ไคลเอนต์ส่ง `CheckSecondPwdVital 0x4B98` (64 B) → เซิร์ฟตอบ `V110_CHECK_SECOND_PASSWORD_OK` (44 B) **ลงท้าย `0B 00`** = ground-list ทรง CLEAR · หลังจากนั้น `MOB_DROP_PRESENCE … live=1 announced=0 carried=1 oldest_left=65.6s` ⇒ **เซิร์ฟยังถือของอยู่ ไคลเอนต์ล้างจอไปแล้ว** = คำทำนายของ cp2 เป็นจริง
> 🔴 **cp2 ยังไม่ถูกเกรด PASS/FAIL และห้ามยกไปเป็นฐานของใบอื่น**: ไม่มีภาพ STEP-D — เจ้าของเล่าเองในรอบ attended · ใบที่จะวัดซ้ำ**หลังแก้** คือ **`GT-242`** (เปิดรอบ `oi2r2n` เดียวกันนี้) · 🔴 `GT-242` **ห้ามผูกกับ `GT-223`** (`COO 1648` ข้อ 2)
> สถานะเดิม (ยกมาคำต่อคำ ไม่ได้ลบ): PENDING -- TWO CHECKPOINTS as of R299 (COO-DECISION `20260902_0347` item 4). Checkpoint 1 (heartbeat) is bootable now: PR #441 on main, verified `git merge-base --is-ancestor 072967a origin/main`. 🔴 Checkpoint 2 (one player ACTION) is a BASELINE measurement of TODAY, not a test of a fix: chief's vitals wrap was WITHDRAWN in R299 before it landed -- see RECHECK item 2

- objective: one claim only -- after the fix that patches `legacy.make_runtime_res_empty_exact` to `preserve_ground_heartbeat_frame` (wired in `src/pirateforce_foundation/app.py`, strictly before the `legacy.game_listener = adapt_game_listener(...)` line, per chief round 6o3gr1 and `pirate-force-server` PR #437), a real client that watches a mob drop an item keeps the dropped item's own non-text model/geometry (not merely its name-label, and not the killed mob's own corpse -- see steps/pass criteria/nonclaims 5-6) visible on screen across at least two ~2s heartbeat intervals (~4-5s total wait, no pickup), instead of the pre-fix behavior where the drop silently vanished within ~2s regardless of whether anyone picked it up. This is LANE-B's P-1 (COO-DECISION 20260901_0347): bug found and confirmed against real bytes in round n8kq4r, server-side fix landed round 6o3gr1. This ticket is the client-observable half; it does not by itself prove Codex's client-image read of the reconciler.
- db: default state\pirateforce.sqlite3 -- always a fresh copy for this boot only, never the canonical file. Record the copy's filename and sha256 before/after the round, and confirm the canonical file's sha256 is unchanged before/after.
- server args: standard playbook boot on `main`, with both `pirate-force-server#437` (mob_loot.py, merged) and `#441` (app.py wiring, chief round 6o3gr1) confirmed present on `main`. No special flags required. Do not boot until RECHECK below shows both are in.
- steps:
  1. Boot server, confirm it is freshly started (age < 3.5 min) and not a leftover from a previously killed client; boot client only after server is up.
  2. Log in. Right-click-drag only (camera rotation, does not change facing, emits nothing) to a clean angle -- no Q/E, no WASD yet. Full-res photo BASELINE, recorded as two separate fields: (a) non-text item model/geometry visible on the ground y/n (expect none -- no mob has been killed yet; dust, shadows, any name/label text, and (once a kill happens) the killed mob's own corpse/body mesh never count as a model sighting -- see step 3's own note), and (b) name-label visible y/n plus the colour of every name label in frame (one line per label, write "none" if there are none). Also record scene name and X/Y/Z from HUD.
  3. Kill exactly one mob that drops an item. If the kill produces more than one drop/loot event (this project has observed a single kill emit two `MOB_LOOT_DROP` events, per `GT-084`'s own result line), pick one dropped item at STEP-A and track that same one through STEP-B/STEP-C -- name which item (by icon/appearance and rough ground position) you are tracking, in writing, at STEP-A, so a later step can be checked against it. Immediately after the drop appears, full-res photo STEP-A, recorded as two separate fields: (a) non-text item model/geometry visible on the ground y/n -- the actual dropped-item 3D object, distinct from any name/label text, dust, or shadow, and distinct from the killed mob's own corpse/body mesh at the kill site (none of those ever count as a model sighting -- this project has separately confirmed, in `GT-084`/`GT-084-R2`/`GT-129`/`RE-107`, that a killed mob's corpse can freeze in place and persist on screen indefinitely, which is a known, unrelated client bug, not evidence for this ticket's claim; if a corpse is present, describe the tracked item's shape/position as distinct from the corpse, not merely "something is there"), and (b) name-label visible y/n plus the colour of every name label in frame (one line per label, write "none" if there are none).
  4. Do not pick up the item. Wait past at least one heartbeat interval (~2-3s) without moving (right-click-drag only if a liveness check is wanted -- do not use Q/E or WASD, that would change facing and emit TargetPosVital, which is not part of this claim). Full-res photo STEP-B on the same tracked item as STEP-A, recorded as two separate fields: (a) non-text item model/geometry still visible y/n (dust/shadow/label text and the mob's own corpse/body mesh never count -- see step 3's note), and (b) name-label still visible y/n plus label colours.
  5. Continue waiting to cross a second heartbeat (~4-5s total elapsed since the drop appeared). Full-res photo STEP-C on the same tracked item, recorded as two separate fields: (a) non-text item model/geometry still visible y/n (dust/shadow/label text and the mob's own corpse/body mesh never count -- see step 3's note), and (b) name-label still visible y/n plus label colours.
  6. Record wall-clock time for every step, to cross-check against the server console/capture log afterward.
  7. Optional, non-blocking, not part of this ticket's pass/fail: if the tracked item's model is still visible at STEP-C, the tester may click it and note whether a pickup opcode appears to fire. This is colour only -- it does not stand in for GT-146's own claim and must not be written as gating or blocking GT-146, which remains a separate ticket held under its own hold.
  8. 🔴 CHECKPOINT 2, added R299 (COO-DECISION `20260902_0347` item 4). Only after STEP-C is photographed: take exactly ONE action the server answers with a vital -- one `W` step is enough (it sends `TargetPosVital` and the server answers) -- and then STOP moving again. Full-res photo STEP-D on the same tracked item, same two separate fields as every step above: (a) non-text item model/geometry still visible y/n (dust/shadow/label text and the mob's own corpse never count), (b) name-label still visible y/n plus label colours. Record the wall-clock time of the keypress and of the photo. One action, not several: the question is whether a SINGLE answered vital wipes the ground, and a burst of them cannot tell which one did it.
  🔴 **R301 (chief, รอบ `smrum3`) -- ห้ามพลิก checkpoint 2 เป็น "วัดผลของการแก้" ตาม `COO 0646` ข้อ 5 ยัง**
  `COO 0646` ข้อ 5 เขียนไว้ว่าเมื่อ `action_ack` ขึ้น main ให้พลิกข้อนี้กลับเป็นการวัดผลของการแก้ · **chief ไม่พลิก และนี่คือเหตุผล** (pf-adversary รอบเดียวกัน D4, วัดแล้ว):
  ① ขั้นนี้สั่งกด `W` = `TargetPosVital` · จุดที่ opt-in คือ **EA7D ActionVital** หลังจับ TargetVital kind 1 ⇒ คนละเส้นทาง
  ② ขั้นนี้สั่งบูต **"No special flags required"** · จุดที่ opt-in เปิดด้วย `--scene-load-scenario ..._ea7d_ack.json` เท่านั้น ⇒ ไม่ใส่แฟล็ก = `scene_load_scenario` เป็น `None` ⇒ **บรรทัดที่แก้ไม่ถูกรันเลยแม้แต่ครั้งเดียว**
  ⇒ ถ้าพลิกตามตัวอักษร ผลของการกด `W` บนเซิร์ฟเวอร์ที่โค้ดใหม่ไม่เคยทำงาน จะถูกบันทึกเป็นหลักฐานของโค้ดใหม่
  **checkpoint 2 ยังเป็น "วัดสภาพวันนี้" ตามเดิม** จนกว่าจะมีขั้นที่กดปุ่มที่ไปถึงจุดนั้นจริง ใต้แฟล็กที่เปิดมันจริง · ส่งคำถามกลับ COO ในใบ `20260902_0920`
  🔴 RECHECK ข้อ 2 ของใบนี้ (`grep install_ground_vitals_preserve app.py` ต้องไม่มีผล) **ตาบอดต่อการ opt-in รายจุด** -- มันผูกกับชื่อไฟล์และสัญลักษณ์ของ wrap ที่ถอนไปแล้ว ไม่ใช่กับ composer ที่จุดไหนใช้ · ตัวตรวจที่เห็นจริง: `git grep -n 'preserve_ground_in_runtime_res_vitals' -- src/pirateforce_foundation/`
- pass criteria (two layers, kept separate):
    wire/DB: the server console/capture log for this boot shows the heartbeat frames sent during the STEP-B/STEP-C windows carry the PRESERVE shape (ground-list mask 0x08 present, count 0, no elements -- the same envelope `drop_collection_pc` already uses) rather than the old CLEAR shape (`0x0B, 0x00` twice, read by the client as `TerrainThingPool == NULL`). This is provable headless, from the capture log alone, and does not by itself prove what the client drew on screen.
    🔴 TWO CHECKPOINTS, GRADED SEPARATELY (R299): CHECKPOINT 1 = STEP-B/STEP-C, standing still across at least two heartbeats. CHECKPOINT 2 = STEP-D, after exactly one answered action. They are separate results and this entry records BOTH; do not collapse them into one PASS/FAIL. If checkpoint 1 passes and checkpoint 2 fails, that is the EXPECTED shape today (no vitals fix exists on `main`; see RECHECK item 2), and the heartbeat half stays regardless -- which is also what COO-DECISION `20260902_0347` item 4 ordered for the case where a vitals fix does exist and does not hold. If checkpoint 1 itself fails, checkpoint 2 tells us nothing and must be recorded as NO-RESULT rather than as a second failure.
    client-observable: the human at the screen reports, from the BASELINE/STEP-A/STEP-B/STEP-C/STEP-D photos, the model and label fields recorded separately per step above, for the one tracked item named at STEP-A. PASS on this ticket's own claim -- that the dropped item's own model/geometry persists on screen across heartbeats -- requires non-text model/geometry to be visible (not just a label, and not the killed mob's own corpse/body mesh -- see step 3/nonclaim 6) at STEP-A, and the same tracked item to remain visible through STEP-B and STEP-C. If STEP-A never shows the item's model (label only, corpse only, or nothing at all), do not mark this ticket's model-persistence claim PASS or FAIL: record it as NO-RESULT, and record the label's own visibility at STEP-B/STEP-C separately alongside it -- a label-only or corpse-only sighting must never be used to satisfy this ticket's own claim. Where the item's model was seen at STEP-A, a negative result (model vanishes by STEP-B or STEP-C despite not having been picked up) is a finding worth exactly as much as a PASS -- record it as such. A negative would mean the PRESERVE-shape server fix did not restore client-side persistence, and would redirect further investigation to nonclaim 1 below (the client-image read of the reconciler), not back to the server wiring, which this round's own tests already pin at the byte level.
- nonclaims:
  1. Does not verify Codex's static IMAGE read of the client reconciler (`GSCN_RunTimeProtocolRes+0x20` / `DropThingModule_Client`) against the client binary itself -- this round's fix was cross-checked only from the server side (byte inspection of `make_runtime_res_empty_exact()` output at offsets 10-13).
  2. Does not claim a full running-server boot test exists anywhere in the repo -- `app.py` is not unit-boot-tested elsewhere in this repo's test layout. The wiring is pinned structurally (`test_app_installs_the_ground_heartbeat_patch_before_adapting_the_listener`) and behaviorally, with a real `legacy` load proving the patch only fires for a caller named `heartbeat_worker` and every other caller (e.g. the connect-time `RUNTIME_RES_ACK_FIRST_REQ`) keeps v141's original bytes (`tests/test_foundation_legacy_seam.py::FoundationLegacySeamTests::test_ground_heartbeat_patch_only_changes_the_heartbeat_worker_caller`), plus at the byte level (`tests/test_mob_loot.py::PreserveGroundHeartbeatTests`, 7/7 passing) -- not end-to-end via a live server boot.
  3. Does not require or claim that the pickup-click opcode is captured during this same session -- that is GT-146's own claim, on its own hold. This ticket must not be treated as blocking or gating GT-146.
  4. Does not attribute a cause to any label's colour -- record colours only, per RE-067 (the cause of label colour is unknown and is that ticket's own subject; do not infer here).
  5. This ticket's own claim is about client-rendered item model/geometry persisting on the ground, not about name-label text persisting -- that is exactly why BASELINE/STEP-A/STEP-B/STEP-C track model-visible and label-visible as two separate fields instead of one combined "drop visible" field. A label alone, with no model ever having rendered, proves nothing about this ticket's claim and must be recorded as NO-RESULT for the model question, per `notes_to_chief/CODEX_URGENT_20260901_1350_GT188-MODEL-NOT-LABEL-GATE.md` and conflict item #1 of `notes_to_chief/20260901_1439_CODEX-CHECKPOINT-GM-COLOR-DROP-FIFTH.md`.
  6. Does not accept the killed mob's own corpse/body mesh as evidence of the dropped item's model -- this project has separately, previously confirmed (`archive/notes_to_chief_2026-08/20260827_1620_GT084R2-RESULT-PASS-hostile-kill-full-wire-but-corpse-freezes-no-target-panel.md`, OBSERVER_CONFIRMED; `CLIENT_RE_QUEUE.md` RE-107, CLOSED BOUNDED-NEGATIVE; `GT-129`) that a killed mob's corpse can freeze in place and persist on screen indefinitely, as a known, unrelated, still-open client bug with its own tickets. A corpse sighting at STEP-A/B/C is not this ticket's claim and must not be recorded as a model sighting; step 3 requires the tester to name/describe the tracked dropped item distinctly from any corpse present at the same kill site. [pf-adversary finding, round `1mw5lf`]
- RECHECK: `cd pirate-force-server && git log --all --oneline -i --grep="preserve_ground_heartbeat_frame" --grep="make_runtime_res_empty_exact" --grep="GT-188" | head -5`
  (confirm both `#437` and `#441` are present on `main` before booting; empty or partial output means still BLOCKED -- do not boot, report back instead).
- RECHECK item 2 (checkpoint 2 only, added R299, CORRECTED the same round): `cd pirate-force-server && grep -n "install_ground_vitals_preserve" src/pirateforce_foundation/app.py` on a fresh `main` clone must print NOTHING. That is the CORRECT state: chief built that wrap in R299, pf-adversary measured that it kills the game-listener thread on two live paths (`--second-password-mode bypass`, every backpack item move) while preserving the ground on none of the paths a player's action actually takes, and it was withdrawn before it was committed (letter `notes_to_chief/20260902_0605_CHIEF-TO-COO-vitals-preserve-wrap-withdrawn-*`). If that grep ever DOES print, a later round relanded it -- read that round's letter before booting, because this entry's checkpoint 2 then means something different.
- 🔴 WHAT CHECKPOINT 2 MEANS TODAY (R299, chief, corrected): NOTHING on `main` preserves the ground across a player's action. The answer to a movement step is composed by this project's own `action_ack`, not by the frozen snapshot, and no site has been opted in yet. So a drop that VANISHES at STEP-D is the EXPECTED result and is still worth the photo: it is the first client-observable confirmation of the reading this whole thread rests on (an empty derived mask clears the ground), and it is the control that a later per-site fix will be graded against. A drop that SURVIVES at STEP-D is the more interesting result -- it would mean the reading is wrong and the per-site plan should stop before it starts. Either way this is a measurement of today, not a PASS/FAIL of anyone's fix.
- links: `pirate-force-server#437` (mob_loot.py, merged) -- `pirate-force-server#441` (app.py wiring, chief round 6o3gr1) -- `notes_to_chief/consumed/20260901_0420_LANE-B-CORE-REQUEST-heartbeat-preserve-ground-list-fixes-drop-clear.md` (original CORE-REQUEST, now consumed) -- `notes_to_chief/consumed/CODEX_URGENT_20260901_0407_DROP-EVIDENCE-CORRECTION.md` and `notes_to_chief/consumed/20260901_0443_CODEX-CHECKPOINT-THREE-PRIORITY-GATES.md` (evidence boundary) -- `COO-DECISION 20260901_0347` (assigned LANE-B this investigation) -- `PROCESS_GATES.md` rule #18 -- `notes_to_chief/CODEX_URGENT_20260901_1350_GT188-MODEL-NOT-LABEL-GATE.md` (model-vs-label pass-gate warning, folded into steps/pass-criteria this round) -- `notes_to_chief/20260901_1439_CODEX-CHECKPOINT-GM-COLOR-DROP-FIFTH.md` conflict item #1 (same warning, second source).
- numbering: per the shared-counter search command (rule ② at the top of this file), the highest confirmed number before this entry, across `GAME_TEST_QUEUE.md`, `CLIENT_RE_QUEUE.md`, and `archive/*QUEUE*ARCHIVE*.md`, is `GT-187`. This entry is `188`.
- result: (tester fills in: PASS/FAIL/BLOCKED, evidence, timestamp, OBSERVER_CONFIRMED line per G-OBS once client-observable evidence exists)


## GT-205 UI-A-BACK-BUTTON-VISIBLE-NOTICE-001  [🟡 **ไม่ยกเลิก — ครึ่ง wire ยังไม่ถูกวัดสำหรับ subcode ของใบนี้** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2): `GT-211` พิสูจน์ composer ตัวเดียวกันบนสาย (`LANE_A_UIA_NOTICE_COMPOSED ... EXIT REFUSED` 66 ไบต์) แต่นั่นคือ **subcode ของปุ่มล็อกเอาต์** ไม่ใช่ subcode 3 ของใบนี้ ⇒ ไม่เข้าเงื่อนไข covered ทั้งสามรูป · 🔴 **เจ้าของใบ LANE-A เป็นคนตัดสินว่า subcode 3 ยังต้องวัดสายของตัวเองไหม** (เจ้าของสั่งไว้เองในใบ `1934`) — ตัดสินแล้วให้เขียนบรรทัดปิด/คงเปิดที่หัวใบนี้ในรอบเดียวกัน · ป้าย `BACK_REFUSED`→`EXIT` ที่ `COO 20260903_1746` ข้อ 2 สั่ง แก้เสร็จแล้วต้องอัปเดตสตริงในเกณฑ์ของใบนี้ด้วยในรอบเดียวกัน (`AGENTS.md` §7) · สถานะเดิม: **client-observable = PASS · wire/DB = NOT MEASURED · ใบยังไม่ปิด** — สถานะเขียนโดย LANE-A (เจ้าของใบ) รอบ `kozzu1` 2026-09-03T11:5x+07:00 · 🔴 **จงใจไม่เขียน `✅ PASS` เดี่ยว ๆ**: เกณฑ์ของใบนี้เขียนเองว่า "TWO layers -- neither layer may ever be offered as proof of the other" และรอบ R303 วัดมาชั้นเดียว ⇒ ปั๊ม PASS ทั้งใบคือรูปเดียวกับหนี้ `GT-192` ที่ถูกบันทึกว่าจ่ายสองรอบ (ผู้ตรวจ pf-adversary รอบ `kozzu1` D3) · **ตัวปิดใบเหลืออะไร: คัดโทเคน `LANE_A_UIA_NOTICE_COMPOSED` จากคอนโซล + ตารางสีป้ายชื่อตามเกณฑ์ + ระบุว่าบรรทัดขึ้นที่พาเนลไหน** — สามอย่างนี้เก็บได้ฟรีในรอบ attended ถัดไปที่บูตอยู่แล้ว ไม่ต้องบูตเพื่อใบนี้ใบเดียว · 🔴 **คำตัดสินของเจ้าของใบ (LANE-A รอบ `gs8hmn` 2026-09-03T22:5x+07:00 ตาม `PANYA-DECISION 20260903_1934` + chief `20260903_2010`): คงเปิด แต่เป็น "เก็บฟรี" เท่านั้น — **ห้ามบูตรอบ attended เพื่อใบนี้ใบเดียว ไม่ว่ากรณีใด** ถ้ารอบ attended ถัดไปจบโดยไม่มีใครบูตอยู่แล้ว ใบนี้ค้างต่อได้ ไม่นับว่าใครค้าง · เหตุผลที่ไม่ปิด: เกณฑ์ของใบนี้เขียนเองว่าสองชั้น และชั้น wire ของ **subcode 3** ยังไม่เคยถูกวัด — `GT-211` วัด subcode ของปุ่มล็อกเอาต์ ไม่ใช่ subcode นี้ (chief ตัดสินแล้วว่าไม่เข้า covered ทั้งสามรูป) ปิดตอนนี้ = ปั๊ม PASS จากชั้นเดียว รูปเดียวกับหนี้ `GT-192` · เหตุผลที่ไม่ให้บูตเพื่อใบนี้: เวลา attended คือทรัพยากรที่แพงที่สุด (`1934`) และตัวปิดสามอย่างที่เหลือเก็บได้จากคอนโซลของบูตใด ๆ ที่มีอยู่แล้ว · 🔴 **กฎ grep `AGENTS.md` §7 ไม่เข้าเงื่อนไขกับใบนี้ วัดแล้วไม่ใช่เดา**: การเปลี่ยนชื่อป้ายรอบ `omhpqj` แตะปุ่ม UI-B ปุ่มเดียว (`UIB_ACTION_LABEL`) · ป้ายของ UI-A ยังเป็นสตริงเดิมของ chief เป๊ะ (`world_logout_button_notice.py:503` `UIA_ACTION_LABEL = "LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE"`) และบรรทัดเดียวที่ chief ยังจะสลับ (~~`runtime.py:7033`~~ **เลขบรรทัดนี้เน่าแล้ว จริงคือจุดที่ประกอบ `uia_notice_actions` ในสาขา `nested_id == LOGOUT_VITAL_ID` — grep เอา อย่าใช้เลข**) อ่านค่าเดียวกันนั้นกลับมา ⇒ **สตริงที่ใบนี้ grep (`LANE_A_UIA_NOTICE_COMPOSED` และ `BACK REFUSED`) ไม่ถูกแตะทั้งก่อนและหลังที่ chief สลับ ไม่ต้องแก้เกณฑ์ข้อไหน**
> 🆕 **อัปเดตรอบ `oi2r2n`/R340 (chief) — หนี้ "แก้สตริงในเกณฑ์รอบเดียวกัน" ที่หัวใบนี้สั่งไว้: จ่ายแล้ว โดยการวัดซ้ำ ไม่ใช่การแก้**: chief สลับบรรทัดนั้นแล้วรอบนี้ (PR เซิร์ฟเวอร์ `oi2r2n` ยังรอเกต) · วัดซ้ำแล้วว่าใบนี้ **ไม่มี** สตริง `LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE` อยู่ในเกณฑ์เลยสักที่ และสองสตริงที่มันใช้จริง (`LANE_A_UIA_NOTICE_COMPOSED` · `BACK REFUSED`) ไม่ถูกแตะ ⇒ **ไม่มีเกณฑ์ข้อไหนต้องแก้** · ป้าย UI-A ไม่เปลี่ยนทั้งสองโลก · หนี้เดียวกันของ `GT-211` **ต้องแก้จริง** และแก้ไปแล้วในใบนั้น (ที่นั่นมีสตริงนี้อยู่ในเกณฑ์)
> **ชั้น client-observable = PASS (รันแล้ว R303 2026-09-02 เจ้าของกดปุ่มเอง)**: บรรทัด `[thua pai] : BACK REFUSED` **ขึ้นบนจอ** = ข้อความสำเร็จของใบเอง (ยกคำจาก `notes_to_chief/20260902_1755_KA1A-R303-RESULTS-*.md`) · สกรีนช็อตอยู่กับเจ้าของ **ไม่ได้อยู่ในรีโปทั้งสอง** (ไม่มี path ไม่มี sha256) · boot `7e14bde1` · capture `capture_r303_20260902_161029`
> **บูตนั้นไม่มี scenario ล็อกเอาต์แน่นอน** (ไม่ได้อ่านจากใบ แต่ตามจากเกต: `runtime.py` ประกอบบรรทัดนี้เฉพาะตอน `logout_hypothesis_scenario is None`) · 🔴 **แต่ "บูตไร้แฟล็ก" ยังไม่ถูกวัด** — ใบสั่งเขียนว่า "NO scenario flag of any kind" แต่ **คำสั่งไม่ใช่การวัด** และใบผลบันทึก head/boot/tree/db/capture/jobs/teardown แต่ **ไม่มี argv** · โมดูลยังประกอบบรรทัดนี้บนบูตที่ถือ scenario อื่นอีกราว 28 ตัว (docstring ข้อ 3 ของโมดูลวัดไว้เอง)
> **ทำไมถึงเชื่อว่าเป็นไบต์ของเซิร์ฟเวอร์**: บรรทัดที่เห็นมี **ช่องผู้พูดว่าง** (`[ป้ายช่อง] : ข้อความ`) ขณะที่ของที่ไคลเอนต์สะท้อนเองอ่านว่า `[ป้ายช่อง] Arena01: ...` และ `say_wire.DEFAULT_SPEAKER = ""` ถูกปักไว้ ⇒ เป็นตัวจำแนก **แต่ไม่ใช่หลักฐานปิด** เพราะไม่มีใครในรีโปเห็นสกรีนช็อต
> 🔴 **เจ็ดอย่างที่รอบนั้นไม่ได้เก็บ ห้ามอ่านว่าเก็บแล้ว**: (1) **ชั้น wire/DB ไม่ได้วัด** — ใบผลเขียนเองว่า "wire/DB: not separately instrumented for this ticket" ⇒ ชั้นนั้นยังยืนบนหมุด headless ใน `tests/test_world_logout_button_notice.py` เหมือนเดิม · (2) **ขั้น 8 ไม่ได้ตอบว่าไดอะล็อกยังเปิดอยู่ไหม** · (3) **ความยาว 12 ตัวอักษรไม่ขยับ** ไม่ได้อนุญาต 5 หรือ 26 · (4) **argv ของบูต** · (5) **บรรทัดขึ้นที่ไหนบนจอ / ห่างจากคลิกกี่วินาที / อยู่นานแค่ไหน** — ขั้น 8 ถามห้าข้อ ใบผลตอบข้อเดียว ⇒ เกณฑ์ "in the local chat/talk area" **ยังไม่ถูกยืนยัน** · (6) **ตารางสีป้ายชื่อทุกภาพ** ที่เกณฑ์บังคับไว้ **ไม่มีในผลเลย** = skip ที่ไม่มีใครนับ · (7) **n = 1** คลิกเดียว เซสชันเดียว และเป็นบูตที่ใบก่อนหน้า (`GT-193`) เพิ่งฆ่าตัวละครและทำให้ไคลเอนต์ไม่ส่งอะไรเลย — ไม่มีบันทึกว่ามีการรีล็อกอินคั่นหรือไม่
> 🔴 **ผลนี้ไม่ได้แปลว่า UI-A เสร็จ** ปุ่มยังพากลับหน้าเลือกตัวละครไม่ได้จริง (`GT-184` ยังเปิด · `NOW.md` คิว UI-A) · 🔴 **ไม่ใช่หลักฐานของ `GT-211`** (subcode 1 คนละปุ่ม) · 🔴 คำถามถึง chief: ใบนี้ถูกใส่กลับเข้าคิวผู้เทสหลังผล R303 มาแล้วสองครั้ง (`FROM_CHIEF_R308` · R317 §4) ขณะที่ `NOW.md` เขียนว่า PASS — ถ้าตั้งใจให้รันซ้ำเพื่อเก็บสามอย่างที่ขาด **ขอให้เขียนในใบว่ารันซ้ำเพื่ออะไร** ไม่งั้นผู้เทสจะเผาบูตซ้ำข้อเดิม
> ~~[🟢 READY (R303, 2026-09-02T13:0x+07:00) -- PR #563 merged 11:55 +07:00; RECHECK run by chief on `origin/main` `96503ff9` and it HIT (`runtime.py:28` import, `runtime.py:5798` `observe_parsed`). Bootable]~~]

> 🔴 **สถานะเปลี่ยนโดย chief รอบ `ogq686` / R302 (2026-09-02T11:2x+07:00):** บรรทัดที่ใบนี้รออยู่
> **เขียนแล้วและ push แล้ว** -- `pirate-force-server` PR **#563** (`runtime.py::_dispatch_with_lanes`
> เรียก `world_logout_button_notice.observe_parsed` ก่อนเกต scenario · เฟรมต่อท้ายท้ายสุดของ `return`)
> **รอ merge เท่านั้น ยังห้ามบูตจนกว่า RECHECK ข้างล่างจะได้ hit จริงบน `origin/main`**
> เกตอ่านจาก `production_allowed` ของโมดูลตรง ๆ ไม่ผ่าน `lane_hooks.module_production_allowed()`
> (มีเทสอ่านซอร์สจริงบังคับไว้) ⇒ ปัญหา D7 ที่ใบกลัวไว้ ปิดแล้ว
> 🔴 chief เพิ่มเกต **fail-closed เมื่อยังไม่ได้เลือกตัวละคร** ที่ใบนี้ไม่ได้ขอ (วัดแล้ว: ก่อนมีเกต
> เซสชันที่ไม่เคยล็อกอินยังได้เฟรมกลับ) ⇒ **ผู้เทสต้องล็อกอินเข้าฉากจริงก่อนกดปุ่มเสมอ** ไม่งั้นได้
> `lane_a_uia_notice_no_selected_no_reply` แล้วจะอ่านเป็น FAIL ผิด ๆ

> Opened by LANE-A round `od1xso` (2026-09-02 +07:00). LANE-A consumes the result itself.
> numbering: shared counter with `CLIENT_RE_QUEUE.md` (rule (2) at the top of this file).
> Highest `GT` in `GAME_TEST_QUEUE.md` = `GT-204`; highest `RE` in `CLIENT_RE_QUEUE.md` = `RE-202`.
> This entry is `205`.

- objective: single claim, decided by human eyes only -- with the character standing in a live map,
  the player opens the HOME menu and clicks "กลับหน้าเลือกตัวละคร" (back to character select), and the
  one line `BACK REFUSED` (exactly 12 printable ASCII characters) APPEARS ON SCREEN in the local
  chat/talk area, either while the logout dialog is still open or right after it closes.

- background (read once, then work from the steps): round `od1xso` built
  `src/pirateforce_foundation/world_logout_button_notice.py`. On `LogoutVital 0x1B40` subcode 3 (the
  owner's own captured 34-byte frame) it composes ONE `Channel_LocalTalkMessageVital` notice via
  `gm/say_wire.make_local_talk_notice_frame`, body exactly `BACK REFUSED`. Subcode 1 (the
  "ออกจากเกม" button, 119-byte frame) gets NOTHING from this lane, on purpose, so `GT-194`'s evidence
  cannot change underneath it. The wire/DB half is already proven headless (~~28 tests~~ **30 tests
  as of round `8z9h9n`** -- the entry was written saying 28 when the suite it names already had 29;
  corrected here by the lane that wrote it, pf-adversary D15), byte-equality with say_wire's
  composer. The tester's job in this entry is ONLY the screen half.
  The spelling `BACK REFUSED` is no longer a lane assumption: `COO-DECISION 20260902_0943`
  (`notes_to_chief/20260902_0943_COO-DECISION-uia-notice-text-back-refused-confirmed.md`) confirmed
  it, so a tester who reads a DIFFERENT spelling off the screen is reporting a defect, not a
  wording that was still being decided.

- PRECONDITION: ~~the module composes bytes but is NOT wired yet~~ **CLEARED by chief, R303
  (2026-09-02T13:0x+07:00).** PR #563 merged at 11:55 +07:00 and the RECHECK below was run against
  the merged `main`:
  `cd pirate-force-server && git fetch origin && git show origin/main:src/pirateforce_foundation/runtime.py | grep -n "world_logout_button_notice"`
  -> two hits on `origin/main` `96503ff9`: line 28 (import) and line 5798 (`observe_parsed`).
  Record `96503ff9` (or whatever `main` you actually boot) in the result.
  The tester may re-run the RECHECK; an empty result would mean the boot is on a stale clone, not
  that this entry regressed.
  BOOT ORDER for this round's tickets, per `COO-DECISION 20260902_1146` item 2:
  `GT-207` -> `GT-193` -> **`GT-205`** -> `GT-204` last.

- db: `state\pirateforce.sqlite3` -- COPY ONLY, never open the canonical file. Copy to
  `state\run_gt205_<yyyyMMdd_HHmmss>.sqlite3` and boot against the copy. Record sha256 of the copy
  before and after; record sha256 of the canonical file before and after and confirm it is unchanged;
  `PRAGMA integrity_check` = `ok` on the copy both times.

- server args: standard boot per `BRIDGE_BOOT_PROCEDURE.md` / `ATTENDED_SESSION_RUNBOOK.md`,
  `-SecondPasswordMode bypass`, NO scenario flag of any kind. Once wired this path is live on a
  default boot (`production_allowed = True`).
  `py -3 -u -m pirateforce_foundation.app --db state\run_gt205_<stamp>.sqlite3`

- steps: (cheap: about 10 minutes on screen. Server first, client second, always.)
  1. RECHECK above must return a real hit. Then LOCK_GAME, boot stamp, sha of canonical, copy the DB.
  2. Boot server, then client. Log in. Confirm a FRESH server start (if a client was killed earlier,
     the server keeps the session and the next client hangs on "connecting" forever -- restart the
     server first).
  3. Frame the shot with RIGHT-CLICK-DRAG only (camera only; the character's facing does not move and
     nothing goes on the wire). Do NOT change the character's facing: no `Q`/`E`, no `W/A/S/D`.
     Do not type any characters -- with chat unfocused every keystroke is a hotkey.
  4. Screenshot S0 BASELINE, full resolution, showing the chat/talk area. Note the wall-clock time
     (+07:00) and the video timestamp.
  5. Open the HOME menu. Screenshot S1 (menu open).
  6. Click "กลับหน้าเลือกตัวละคร" ONE time. Write down the wall-clock time and the video `t` of that
     click before doing anything else.
  7. WATCH THE SCREEN CONTINUOUSLY FOR AT LEAST 30 SECONDS. Take S2 at about +2s, S3 at +10s,
     S4 at +30s, all full resolution, all showing the chat/talk area. Do not click anything, do not
     dismiss the dialog by hand during those 30 seconds unless the client itself closes it.
  8. Record, in the result: did the twelve characters `BACK REFUSED` appear -- yes/no; WHERE on screen
     (which panel/line); at what offset from the click; for how long it stayed; and whether the logout
     dialog was still open at that moment or had already closed.
  9. Optional second attempt, only if attempt 1 showed nothing: relog, repeat steps 5-8 once with the
     chat window/tab explicitly OPEN and its history tab visible before clicking the button. Label the
     screenshots S0b..S4b and record the two attempts separately -- do not merge them.
  10. NO-CRASH check with RIGHT-CLICK-DRAG (never `Q`/`E`). Screenshot S5. Exit with the window X.
  11. Shut the server down. Keep console `.out`/`.err`, `capture_v141\GAME_LIVE.txt`,
      `capture_v141\GAME_EVENTS_LIVE.txt` + sha256 of each. `PRAGMA integrity_check`. Re-check the
      canonical sha. Run teardown ALWAYS, even if the round ended because she simply stopped playing
      (the template refuses a boot stamp older than 420 minutes -- do not let the round age out).

- pass criteria: (TWO layers -- neither layer may ever be offered as proof of the other)
    wire/DB          : headless-readable from the console/capture alone. The subcode-3 request arrives
      and the console prints
      `LANE_A_UIA_NOTICE_COMPOSED button=BACK_TO_CHARSELECT subcode=3 vitals=1 trailing=0 text=BACK REFUSED pc=56 frame=66`
      (one line, exactly as printed -- the `pc=`/`frame=` lengths are the composed bytes, so the token
      cannot appear unless bytes exist). If she also clicks the exit button at any point, the matching
      line is ~~`LANE_A_UIA_STOOD_DOWN button=EXIT_GAME subcode=1 vitals=4 trailing=85`, which shows this
      lane composed NO BYTES for subcode 1 -- it still prints that one line, which is itself evidence
      `GT-194`'s reader will see; "nothing at all" would be the wrong expectation.~~ **CHANGED, LANE-A
      round `1d6rta` (2026-09-02T13:4x+07:00), per `COO-DECISION 20260902_1145`: the exit button is no
      longer a stand-down.** On a boot that carries this round's code (server PR of round `1d6rta`; the
      RECHECK below tells you which `main` you have), the exit click prints
      `LANE_A_UIA_NOTICE_COMPOSED button=EXIT_GAME subcode=1 vitals=4 trailing=85 text=EXIT REFUSED pc=56 frame=66`
      and a second twelve-character line may appear on screen. **That belongs to `GT-211`, not to this
      entry** -- this entry is graded on `BACK REFUSED` alone. On an older `main` the struck
      `LANE_A_UIA_STOOD_DOWN` line is still the correct one and is not a defect. Copy whichever lines
      appeared, verbatim, do not interpret.
      Three other tokens can appear instead, and each means something different:
      `LANE_A_UIA_WITHDRAWN` (the module is switched off), `LANE_A_UIA_NOTICE_FAILED` (the composer
      refused -- a bug to report, not a tester error), `LANE_A_LOGOUT_FRAME_UNCLASSIFIED verdict=<word>`
      (the frame reached this lane and was rejected; the word is the live classifier's own verdict).
      Copy whichever appeared. `integrity_check` = `ok`; canonical sha unchanged; no uncaught traceback.
      This layer CANNOT answer: whether anything was drawn on screen.
    client-observable: needs the human at the screen; never inferred from the console. Within the
      30-second window after the click, a human SEES the line `BACK REFUSED` -- twelve ASCII
      characters, that exact spelling -- in the local chat/talk area. Compare S0 against S2/S3/S4.
      Record for EVERY still (S0-S5, and S0b-S4b if attempt 2 was run) the colour of EVERY name label
      in frame, one line per label per image, the word `none` written out rather than left blank.
      Read colours from full-resolution stills only -- never from a contact sheet, a downscaled image,
      or video. Record the colour and nothing else: what decides a label's colour is unknown and is the
      whole subject of `RE-067`. Divergences from the original server's screenshots get one row each in
      `REAL_SERVER_DIVERGENCE.tsv`.
      This layer CANNOT answer: what bytes were composed, or which subcode arrived.

- prediction (THIS IS A PREDICTION, not a measurement; a wrong prediction is a finding):
    P1 console token present AND `BACK REFUSED` visible within ~2s => both layers pass.
    P2 console token present but nothing visible in 30s => the notice channel does not render while the
       logout dialog owns the input/render state. That is a real finding about the dialog, NOT proof the
       composer is wrong -- redirect to an RE about the dialog's render state, do not re-run blind.
    P3 no console token at all => the call site is not on the path she clicked; re-run RECHECK and
       report which `main` commit was booted. NO-RESULT for the screen half, not FAIL.

- nonclaims:
  1. Does NOT test whether the client returns to the character-select screen. That is `GT-184` and it
     remains unsolved (`GT-033` measured both known response policies leaving the client on the same
     map for 50-77s). Seeing `BACK REFUSED` says nothing about the transition.
  2. A negative is a real finding of equal worth: it is evidence about the logout dialog's input/render
     state, NOT proof that the notice composer is wrong. The render evidence for this channel
     (`GT-006`/`GT-009`) was measured with the dialog CLOSED, so this entry is the first time it is
     asked to draw with the dialog OPEN.
  3. Does NOT test the "ออกจากเกม" button (`GT-186`/`GT-194`/**`GT-211`**) and must not be run in a way
     that changes their evidence. If she clicks it anyway, log it as a separate observation with its own
     token line -- and on a `main` that carries round `1d6rta`, that observation IS `GT-211`'s evidence:
     record it there rather than grading this entry on it.
  4. Claims nothing about `ReturnSelectServerVital 0x709E` or `HYP-PF-040`.
  5. Does not claim the PR is merged; the RECHECK line, not this header, decides that.

- links: `NOW.md` item UI-A · `GT-184` · `GT-185` · `GT-194` · `RE-197` (closed this round) ·
  `notes_to_chief/consumed/20260901_1930_KA1A-CAPTURE-the-owner-clicked-both-UI-A-and-UI-B-buttons-herself-exact-bytes-plus-a-design-problem-for-HYP-PF-040.md`
  · `GT-193` (the `SPEED DENIED` notice -- same channel, same 12-character shape)

- result: (tester fills in: PASS/FAIL/BLOCKED/NO-RESULT · screenshots S0-S5 · verbatim console lines ·
  label colours one line each · timestamps +07:00 · `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

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

