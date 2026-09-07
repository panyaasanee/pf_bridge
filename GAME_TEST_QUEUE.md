# GAME TEST QUEUE — คิวเทสในเกม

> 🔤 **กฎชื่อใบ (คำสั่ง Panya 2026-08-24 ~00:2x · จดหมาย `20260824_0025_*`):** ใบในไฟล์นี้ใช้ prefix **`GT-`** (เทสเกม — เปิดเกม · จับ `LOCK_GAME` · ใช้ตาคน) · **ตัวนับเลขเป็นชุดเดียวร่วมกับ `CLIENT_RE_QUEUE.md`** (ใบ static ที่นั่นใช้ prefix **`RE-`** ตั้งแต่ใบ **056** เป็นต้นไป) — เห็น `RE-0xx` ที่ไหนแปลว่าเป็นใบ static ให้ข้ามไปดูไฟล์นั้น · ใบเก่า (รวม `GT-050`/`052`/`053`/`054`/`055` ที่เป็น static แต่ชื่อ GT-) **คงชื่อเดิมตลอดกาล**

> 🔢 **กฎออกเลขใบ (COO-DECISION `20260829_0542_COO-DECISION-vote-item-5-withdrawn-shared-counter-stays.md` ข้อ 3 · แก้ต้นเหตุ "เต้นเลข" โดยไม่แตะตัวนับร่วม):**
> ① **ห้ามจองเลขล่วงหน้า** — เลขเกิดตอนใบลงไฟล์นี้จริงเท่านั้น · จดหมายที่ต้องอ้างใบที่ยังไม่เปิด ให้เขียนว่า **"ใบถัดไป"** ห้ามเขียนเลขที่ยังไม่มีในไฟล์
> ② เลขถัดไป = ผลของ **คำสั่งค้นหาเดียว ไม่ใช่ความทรงจำ** (รันจากรากรีโป `pf_bridge`) แล้ว **+1**:
> &nbsp;&nbsp;&nbsp;&nbsp;`grep -ohE '\b(GT|RE)-[0-9]{3}\b' GAME_TEST_QUEUE.md CLIENT_RE_QUEUE.md archive/*QUEUE*ARCHIVE*.md | grep -oE '[0-9]{3}$' | sort -n | tail -1`
> ③ ชนกันจริง = **คนที่ push ทีหลังขยับเลขของตัวเอง** แล้วเขียนเหตุผลไว้ในใบ · **ไม่มี allocator กลาง** ไม่ต้องรอใครอนุมัติเลข

> 🔴 **G-OBS — ขั้นบังคับข้อสุดท้ายของ **ทุกใบที่มีชั้น client-observable** (คำสั่ง Panya 2026-08-25 ~19:35 +07:00 · **ขยายครอบรอบ unattended โดยเจ้าของเอง ~21:10 +07:00** · เขียนลง `AGENTS.md` §6 แล้วโดย R168 และ R170):**
> **ก่อนเขียนผล ต้องทวนสิ่งที่ผู้ช่วยเห็นให้ผู้เทส (มนุษย์) ยืนยันก่อน** แล้วบันทึกเวลาที่ยืนยันลงในจดหมายผลเป็นบรรทัด
> `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` · **จดหมายผลที่ไม่มีบรรทัดนี้ chief จะไม่บริโภคเป็นผลปิดใบ**
> (เก็บหลักฐานระหว่างรอได้เต็มที่ — ที่ถูกกลั้นคือ *ข้อสรุป*: จดหมายผล · สถานะใบ · nonclaim · การประกาศว่าอะไร "ไม่เกิดขึ้น")
>
> 🔴 **รอบ unattended ไม่ยกเว้นอีกต่อไป** — ไม่มีตาคนตอนรัน **แต่มีวิดีโอให้เจ้าของดูย้อนหลัง** ⇒ จังหวะที่ 3 แค่เลื่อนเวลาออกไป ไม่ได้หายไป
> (ท่านี้เคยใช้ปิด `GT-059` มาแล้วจริง · จดหมาย `20260824_2133 PANYA-VISUAL-SIGNOFF-GT059`)
> 🆕 **สถานะกลาง `AWAITING-OBSERVER`** = รันครบ หลักฐานครบ **ขาดลายเซ็นตาคนอย่างเดียว** ⇒ ใช้สถานะนี้แทน `PENDING` เพื่อให้คอขวดมองเห็นได้
> 🔴 `AWAITING-OBSERVER` **ไม่ใช่ PASS ไม่ใช่ FAIL** — ห้ามยกผลของใบสถานะนี้ไปเป็นฐานของใบอื่น

> 🆕 **`RECHECK:` — กฎใหม่ R260(sm51i5) 2026-08-31 (ข้อเสนอกะ1-A ซ้ำเป็นครั้งที่หก, `20260831_0909_KA1A-NOTE-*.md`):**
> หัวใบล้าสมัย (สถานะในหัวใบไม่ตรงผลจริงที่บริโภคไปแล้ว) ทำให้ผู้เทสบูตซ้ำโดยเปล่าประโยชน์ — เกิดซ้ำ 6 ครั้งในสัปดาห์เดียว
> (`GT-103`/`GT-110`/`GT-132`/`GT-141`/`GT-145`/`GT-134`) **ใบใหม่ที่เปิดสถานะ `BLOCKED`/`HOLD`/`READY` ตั้งแต่วันนี้เป็นต้นไป
> ต้องมีบรรทัด `RECHECK: <คำสั่งรันได้จริงหนึ่งบรรทัด>`** (เช่น grep/pytest ที่บอกว่าสถานะยังจริงไหมโดยไม่ต้องเชื่อหัวใบ)
> ⇒ ผู้เทส/สายที่หยิบใบรันบรรทัดนี้ก่อนเชื่อหัวใบเสมอ · **ไม่ retrofit ใบเก่าทั้งคิวย้อนหลังในรอบเดียว** (คิวใหญ่เกินจะปลอดภัย)
> ปิดหัวใบทุกครั้งที่บริโภคผล — เจ้าของใบเป็นคนปิด (หรือ chief ถ้าเจ้าของใบไม่ว่าง) อย่าปล่อยให้ค้างแบบที่เกิดกับ `GT-134`

> 🔴🆕 **กฎยกเลิกใบเก่าเมื่อผลใหม่ตอบไปแล้ว — `PANYA-DECISION 2026-09-03 ~19:1x+07:00`**
> (ใบ `notes_to_chief/20260903_1934_PANYA-DECISION-*.md` · เขียนลงหัวคิวโดย chief ตาม `COO-DECISION 20260903_1943` ข้อ 2 · **ถ้อยคำเป็นของ chief กฎเป็นของเจ้าของ**)
> ① **ทุกครั้งที่บริโภคจดหมายผล** (attended หรือ headless) สายที่บริโภคต้องกวาดใบที่ยัง **เปิดและยังไม่ได้รัน** ซึ่งแตะพฤติกรรมเดียวกัน แล้วถามทีละใบว่าผลนี้ (ก) **หักล้าง** สมมติฐานของใบเก่า (ข) **พิสูจน์สิ่งที่ใบเก่าตั้งใจจะพิสูจน์ไปแล้ว** หรือ (ค) **ทำให้ไม่ต้องพิสูจน์อีกต่อไป**
> ② ใช่ข้อใดข้อหนึ่ง = **ปิดใบเก่าในรอบเดียวกัน** ห้ามปล่อยค้าง `READY`/`PENDING`/`BLOCKED` ให้ผู้เทสเผาบูตทิ้ง
> ③ บรรทัดปิดต้องระบุใบ/จดหมายที่ใหม่กว่า และต้องเป็นหนึ่งในสามรูปนี้เท่านั้น — **ห้าม "cancelled" เปล่า**:
> &nbsp;&nbsp;&nbsp;&nbsp;`CANCELLED - refuted by <GT-nnn / จดหมาย>` · `CANCELLED - covered by <GT-nnn / จดหมาย>` · `CANCELLED - no longer needs proving because <หนึ่งประโยค>`
> ④ **ยกเลิก ≠ ลบ** — ใบที่ยกเลิกยังอยู่ในไฟล์พร้อมเหตุผล และเข้า archive ตามกฎ 24 ชม. เหมือนใบปิดอื่น · **ห้ามยกเลิกใบที่ผลใหม่ "ไม่ได้" ตอบ** (ตัวอย่างที่เจ้าของยกเอง: `GT-178` ถูกบล็อกโดย `GT-224` ไม่ใช่ถูกตอบ ⇒ ห้ามยกเลิก ให้ต่อคิวหลัง `GT-224`)
> ⑤ เหตุผลของกฎ: เวลา attended คือทรัพยากรที่แพงที่สุดของโปรเจกต์ (คนเดียว คีย์บอร์ดเดียว) — คิว attended ต้องเหลือเฉพาะใบที่ยังต้องใช้คนจริงหน้าจอ
> **คำตัดสินรายใบรอบแรก (chief รอบ `pk14rf`/R326 ตาม `COO 1943` ข้อ 2): `GT-141` `GT-128` `GT-204` `GT-187` ยกเลิก · `GT-178` `GT-205` ไม่ยกเลิก** (เหตุผลอยู่ที่หัวใบแต่ละใบ)

> 🔴🔴 **ไมล์สโตนพักแล้ว (คำสั่งตรง Panya 2026-09-01 ~02:1x+07:00 · จดหมาย `20260901_0215_PANYA-ORDER-*.md` ·
> ประกาศโดย chief รอบ `4w5j25`/R278):** **M1-M6 ทั้งหมดพักไว้ก่อน** ไม่นับ ไม่ใช้เป็นเหตุผลจัดลำดับงาน จนกว่า
> เจ้าของจะสั่งกลับมา (พัก ไม่ใช่ยกเลิก) ทุ่มไปที่: **P-1** ของดรอปต้องอยู่บนพื้นนานพอให้เดินไปเก็บทัน
> (เจ้าของ: LANE-B) · **P-2** ชื่อมอนต้องเห็นสีถูกสถานะ ปกติ=ส้ม/สู้=แดง/ตาย=เทา ห้ามชมพู (เจ้าของ: LANE-GM) ·
> **P-3** เปิดปุ่ม GM (เจ้าของ: LANE-GM ร่วม Codex) · รายละเอียดเต็ม `notes_to_chief/20260901_0302_FROM_CHIEF_R278_priority-reorg-panya-order-P1-P2-P3-plus-new-builds.md`
> 🔴 **~~`GT-146` และ~~ใบตีมอนสเตอร์ทั้งหมด ห้ามเสนอเข้าคิว attended จนกว่า P-1 และ P-2 จะเสร็จ** (ชื่อ `GT-146` ถูกขีดออกจากข้อห้ามนี้โดย chief รอบ `m8wtlr`/R356 — ใบนี้ CANCELLED-covered ไปแล้ว ไม่มีอะไรให้ห้าม · `COO-DECISION 20260905_0249` ข้อ 1 · ส่วน "ใบตีมอนทุกใบ" คงไว้ตามเดิม) — เจ้าของจะไม่เทส
> สองประเภทนี้จนกว่าจะถึงตอนนั้น (นี่คือเหตุผลที่ M5 พักได้) · งานสร้างใหม่ที่เปิดใบแล้ว: `GT-182` `/warp` ไม่ใส่
> พิกัด (LANE-GM) · `GT-183` `/speed` (LANE-GM) · `GT-184`/`GT-185` ปุ่มกลับหน้าเลือกตัวละคร/กลับเข้าเกม (LANE-A)
> · `GT-186` ปุ่ม logout จริง (LANE-A) — ห้าใบนี้ท้ายไฟล์

## 📇 สารบัญใบที่ยังไม่ปิด (คำสั่ง Panya 18:22 · อัปเดตทุกครั้งที่เปิด/ปิดใบ · เป็นดัชนีชี้ลงข้างล่าง — เนื้อใบไม่ถูกย้าย)

- 🆕 **`GT-213` COLUMBUS-SCENE-GUARDS-VISIBLE-COST-001** (🔴 **BLOCKED — รอ merge `server#584` (+ ใบ D3 ของรอบเดียวกัน)** · เปิดโดย chief (LANE-E) รอบ `kt05o0`/R305 ตาม `COO-DECISION 20260902_1347` · ผู้ทำ: **ผู้เทส attended** · chief บริโภคผลเอง · ข้ามไปฉาก 17 ด้วย Columbus แล้ว `/warp 1` กลับมา Port Royal ต้องมีชาวเมือง + คลิก actor index 1 ของฉาก 14 ต้องไม่เปิดบทสนทนา · ใบเต็มอยู่ท้ายไฟล์ · เลขขยับจาก 212 เพราะ LANE-A push ก่อน)
- 🆕 **`GT-184` UI-A-PART-A-BACK-TO-CHARSELECT-BUTTON-001** (🔴 **BLOCKED-ON-WIRING (R311 = NEGATIVE / hypothesis not exercised) — เดิม READY-FOR-ATTENDED, สืบทอดจาก `GT-033` (ANSWERED — สองท่าที่ลองแล้วให้ผลลบ)** [NEEDS-ATTENDED-CAPTURE] · เปิดโดย chief ตาม `PANYA-ORDER 20260901_0215` ข้อ 3 (UI-A ครึ่งแรก) · ผู้ทำ: **LANE-A** · ปุ่มกลับหน้าเลือกตัวละครจากในเกม ต้องพาไปจริงกลางเซสชัน · แยกจาก `GT-185` ตามกฎหนึ่งใบหนึ่งข้อพิสูจน์ · ใบเต็มอยู่ท้ายไฟล์ · **[อัปเดต round `tmizmk` 2026-09-01 15:58+07:00] allowlist ที่หกลงแล้ว พร้อมบูตด้วย `--logout-hypothesis-scenario scenarios/logout_hypothesis_dialog_open_push.json` -- ยังไม่พลิก `production_allowed` (รอ attended pass ก่อนตาม stop_rule) พร้อมให้ผู้เทส attended หยิบได้แล้ว** · **[อัปเดตหัวใบ chief round cool-johnson-7qcsux 2026-09-04 15:22+07:00 ตาม `COO-DECISION 20260904_1451` ข้อ "unblock GT-184/186 heads": หัวเดิมพิมพ์ BLOCKED ทั้งที่ body บอกว่าพร้อมหยิบตั้งแต่รอบ `tmizmk` — แก้หัวให้ตรง body ไม่ใช่การเปลี่ยนสถานะใหม่** · **[อัปเดตหัวดัชนี chief รอบ `t7bsfx`/R342 2026-09-04 20:0x+07:00 ตาม `COO-DECISION 20260904_1948` ข้อ 5: รันแล้ว R311 = NEGATIVE / hypothesis not exercised — push `0x709E` ไม่เคยออกจากเซิร์ฟเวอร์ ⇒ กลับเป็น BLOCKED-ON-WIRING รอ LANE-UI แก้ก่อนรันใหม่]**)
- 🆕 **`GT-185` UI-A-PART-B-BACK-INTO-GAME-ROUNDTRIP-001** (🔴 **BLOCKED — precondition: `GT-184` ต้อง PASS ก่อน** [NEEDS-ATTENDED-CAPTURE] · เปิดโดย chief ตาม `PANYA-ORDER 20260901_0215` ข้อ 3 (UI-A ครึ่งหลัง) · ผู้ทำ: **LANE-A** · จากหน้าเลือกตัวละคร เลือกแล้วกลับเข้าเกมได้จริงในโปรเซสเดิมไหม — ปลดล็อกการเปลี่ยนฉากซ้ำโดยไม่บูตใหม่ · ใบเต็มอยู่ท้ายไฟล์ · **[อัปเดต round `tmizmk`] precondition ยังคือ `GT-184` ต้อง PASS ก่อน — สถานะไม่เปลี่ยน แค่ construction path ของ `GT-184` พร้อมแล้ว**)
- 🆕 **`GT-186` UI-B-REAL-LOGOUT-BUTTON-001** (🔴 **BLOCKED-ON-WIRING (R311 = NEGATIVE / hypothesis not exercised) — เดิม READY-FOR-ATTENDED** [NEEDS-ATTENDED-CAPTURE] · เปิดโดย chief ตาม `PANYA-ORDER 20260901_0215` ข้อ 3 (UI-B) · ผู้ทำ: **LANE-A** · ปุ่ม logout จริง (คนละ subcode กับ `GT-184`) ต้องจบเซสชันสะอาดโดยไม่ต้องปิดหน้าต่างด้วย X · ใบเต็มอยู่ท้ายไฟล์ · **[อัปเดต round `tmizmk`] ไม่ใช่ BLOCKED-ON-WIRING อีกต่อไป — allowlist ที่หกลงแล้ว พร้อมบูตด้วยแฟล็กเดียวกับ `GT-184` ด้านบน ยังไม่พลิก `production_allowed`** · **[อัปเดตหัวใบ chief round cool-johnson-7qcsux 2026-09-04 15:22+07:00 ตาม `COO-DECISION 20260904_1451`: หัวเดิมพิมพ์ BLOCKED-ON-WIRING ทั้งที่ body บอกว่าไม่ใช่แล้วตั้งแต่รอบ `tmizmk` — แก้หัวให้ตรง body** · **[อัปเดตหัวดัชนี chief รอบ `t7bsfx`/R342 2026-09-04 20:0x+07:00 ตาม `COO-DECISION 20260904_1948` ข้อ 5: รันแล้ว R311 = NEGATIVE / hypothesis not exercised — push `0x709E` ไม่เคยออกจากเซิร์ฟเวอร์ ⇒ กลับเป็น BLOCKED-ON-WIRING รอ LANE-UI แก้ก่อนรันใหม่]**)
- 🆕 **`GT-221` LOGIN-SENDS-THE-ROW-NOT-THE-CONSTANT-THREE-SHAPES-001** (🔴 **BLOCKED — รอ fixture สามแถวของใบ `COO 20260903_1051` ที่ LANE-DB จะลง `main` (เขียนผ่าน `store.write_typed_attributes` บน run copy · `COO 20260903_1247` ข้อ 1: ทาง (ก) เท่านั้น · migration ปฏิเสธ)** · เปิดโดย chief รอบ `xnixm6` (R318) ตามใบสั่ง `COO-DECISION 20260903_1052` · **เจ้าของเนื้อหา/ผู้บริโภคผล = LANE-DB · ผู้รัน = Panya** · ใบแรกที่แยก "เซิร์ฟเวอร์อ่านแถว" ออกจาก "เซิร์ฟเวอร์ส่งค่าคงตัว" ได้จริง ซึ่ง `GT-215` ทำไม่ได้โดยโครงสร้าง · 🔴 **ต่อคิวหลัง `GT-216` ห้ามแย่งลำดับกับ P-1** · `RECHECK 1` เป็นตัวปลดป้าย · ใบเต็มท้ายไฟล์)
- 🆕 **`GT-223` GROUND-LEDGER-SURVIVES-A-RECONNECT-001** (🟢 **READY เมื่อ RECHECK ข้อ 1 ผ่าน — ตัวบล็อกหมดอายุทั้งสองตัว** (chief รอบ `dwvbpm`/R330 ตาม `COO-DECISION 20260904_0145` ข้อ 1): `GT-216` PASS (R306) และประตู persistence อยู่บน main แล้วทาง **`#680`** ไม่ใช่ `#672` (chief วัดเอง 2026-09-04T01:5x: `store.py:2261` `commit_ground_drop` · `store.py:2392` `list_ground_drops_for_scene`) · ~~ตัวบล็อกที่เหลือคือ `pirate-force-server#672`~~ **ถอนแล้ว วัดผิด** · 🔴 **ใบนี้คือที่อยู่ของขั้น "ป้ายชื่อของไม่กะพริบ" ของ `RE-208`** ตาม `COO-DECISION 20260903_1942` ข้อ 4 (chief เลือกใบ · LANE-B เขียนขั้น) · ~~คิวหลัง `GT-216` เท่านั้น~~ · เปิดโดย chief รอบ `kjtpza` (R319) ตามใบสั่ง `COO-DECISION 20260903_1048` · **เจ้าของใบ/ผู้แก้ = LANE-B · ผู้รัน = Panya** · ใบข้อบกพร่อง ไม่ใช่ใบสำรวจ: ของที่ดรอปแล้วเป็นของ **โลกต่อฉาก** ไม่ใช่ของเซสชัน ⇒ รีล็อกอินแล้ว ledger ว่าง = **ข้อบกพร่องจริง** · `RECHECK 1` เป็นตัวปลดป้าย · ใบเต็มท้ายไฟล์)
- 🆕 **`GT-224` MOB-AI-TICK-GATE-IS-OPEN-AND-STILL-INVISIBLE-001** (🟢 **READY เมื่อ RECHECK ผ่าน — `#668` merged แล้ว 11:49Z และ `#670` ปลด main แดงแล้ว 12:26Z · เกณฑ์ `mobs=` เปลี่ยน อ่านหัวใบก่อนบูต (chief รอบ `pk14rf`/R326)** · ~~🔴 BLOCKED รอ merge `#668`~~ · เปิดโดย chief รอบ `gjyxt5` (R324) ตาม `COO-DECISION 20260903_1648` · **เจ้าของใบ/ผู้บริโภคผล = chief ร่วม LANE-B · ผู้รัน = ผู้เทส** · 🔴 **PASS ของชั้นจอคือคำว่า "ไม่มีอะไรเปลี่ยน"** มอนขยับ/เข้าตี = finding ไม่ใช่ PASS · `RECHECK` สองข้อเป็นตัวปลดป้าย · ใบเต็มท้ายไฟล์)
- 🆕 **`GT-253` OPTIONS-APPLY-ONE-SETTING-DIFFERENTIAL-CAPTURE-001** (🔴 **BLOCKED** — รอ LANE-UI เขียนเนื้อ `RE-237` ก่อน · เจ้าของ = LANE-UI · เปิดโดย chief รอบ `kj0s6r`/R346 · TOC เติมโดย chief รอบ `s5uz94` — ใบเต็มท้ายไฟล์)
- 🆕 **`GT-258` WARP-SEND-FAILURE-ROLLS-THE-SCENE-BACK-001** (🟢 **READY** · STOP เดิมปลดแล้ว (`#806` บน main) · เจ้าของ = LANE-GM · เลขตั้งโดย chief รอบ `pv4zg1`/R352 — ใบเต็มท้ายไฟล์)
- 🆕 **`GT-262` STALL-AND-GUILD-STORAGE-ATTENDED-CAPTURE-001** (🟡 **PENDING — เลขตั้งแล้ว (RESERVED) เนื้อใบยังไม่เขียน** · เจ้าของ = LANE-UI · คู่กับ `RE-261` — ใบเต็มท้ายไฟล์)
- 🆕 **`GT-264` RECOMPOSE-MID-COMBAT-KEEPS-ANOTHER-MOBS-GROUND-DROPS-001** (🔴 **BLOCKED-ON-WIRING** — เนื้อใบเขียนโดย LANE-A (`#818` merged) · เลขตั้งโดย chief รอบ `r045nx`/R354 ตามคำขอ `notes_to_chief/20260905_1250_LANE-A-TO-CHIEF-*` ข้อ 1 · ปลดเป็น READY เมื่อบรรทัด `ground_companion_actions` อยู่บน main — ใบเต็มท้ายไฟล์)
- 🆕 **`GT-266` WARP-126-LIVE-TELEPORT-001** (⚪ **RESERVED — เลขจองโดย chief รอบ `r045nx`/R354 ตาม `COO-DECISION 20260905_1349` ข้อ 4(ข) + `1346` ข้อ 4 · เนื้อใบเขียนโดย LANE-A (ตก 15:51) · ห้ามสายอื่นใช้เลขนี้**)
- 🆕 **`GT-267` SEA-EDGE-CROSSING-126-TO-304-AND-305-001** (⚪ **RESERVED — เลขจองโดย chief รอบ `r045nx`/R354 ตาม `COO-DECISION 20260905_1349` ข้อ 4(ค) + `1348` ข้อ 6 · เนื้อใบเขียนโดย LANE-A ร่วม LANE-GM · ห้ามสายอื่นใช้เลขนี้**)
- 🆕 **`GT-225` GROUND-CELL-FOLLOWS-A-WALKING-PLAYER-ACROSS-A-SCENE-EDGE-001** (🔴 **BLOCKED — คิวหลัง `GT-215`** · เปิดโดย chief รอบ `dwvbpm`/R330 ตาม `COO-DECISION 20260904_0145` ข้อ 2 · **เจ้าของใบ/ผู้แก้ = chief (LANE-E)** ตาม `COO 20260903_2250` ข้อ 5 ไม่ใช่ LANE-B · ใบข้อบกพร่อง: `_mob_loot_cross_scene_boundary()` มีผู้เรียกจุดเดียวคือเส้นทาง GM warp (`runtime.py:6749/6751`) ⇒ ผู้เล่นที่ **เดิน** ข้ามขอบฉากไม่เคยบอก `DropLedgerCell` · `#675` วัดแล้วไม่ปิด · `RECHECK` เป็นตัวปลดป้าย · ใบเต็มท้ายไฟล์)
- 🚀 **`PROMOTE-153` CHAT-ECHO-ON-A-DEFAULT-BOOT-001 [CHIEF-WORK · ไม่ใช่ใบเทส]** (🟢 **OPEN — เจ้าของ: chief** · ใบแรกของท่อ promotion ตาม `PANYA-DIRECTIVE 20260829_2222` + `COO-DECISION 20260829_2246` · แชทใบ้บนบูตปกติเพราะเส้นทาง echo อยู่ในเลน hypothesis ที่ `production_allowed: False` ทั้งสองเลน [วัดแล้ว รอบ k882hm] · เส้นตายข้อ 1 ของ directive: 30 ส.ค. 21:00 · ใบเต็มอยู่ท้ายไฟล์)
- 📌 [บรรทัดสารบัญโดย chief R235 (t7t5yd) — เนื้อใบไม่ถูกแตะ] **`RIDER-149-A`** (ของสาย B ท้ายไฟล์): chief ต่อสายห้าบรรทัด `MOB_DROP_PRESENCE` ตามใบ 2246 แล้ว **รอ merge `pirate-force-server#291`** — ด่านบิลด์ของ rider (grep `MOB_DROP_PRESENCE` ตอนฆ่า) จะผ่านเมื่อ merge เท่านั้น ก่อนหน้านั้นบูตได้ `NO-RESULT` ตามที่ใบเขียนไว้เอง
- 🆕 **`GT-142` M5-KILL-PICKUP-RELOG-ROUNDTRIP-001** (🔴 **BLOCKED — `BLOCKED-BY: STORE-INSERT-001`** · เปิดโดย chief R222 ตาม `COO-DECISION 20260829_0441` gate-2 ข้อ 3 · ใบปิดวง M5: ฆ่ามอนใน `Bg0002` → เก็บของ → relog → ของยังอยู่ไหม · 🔴 **ห้ามขึ้นหัวคิว ห้ามเรียกผู้เทส** ~~จนกว่าตั๋วราก `STORE-INSERT-001` ปิด~~ [chief R226: ตั๋วรากปิดแล้ว เงื่อนไขย้ายเป็น: จนกว่า `GT-146` ให้ opcode และ call site `GT-124` ลง main] 🔴 **[chief R356: `GT-146` CANCELLED-covered แล้ว — ห้ามรอมันอีก** · opcode ที่ใบนี้รอ **มีแล้ว** จาก R303 (`0x4543` ขาเข้า 46 เฟรม ยืนยัน R306) ⇒ เงื่อนไขที่เหลือของใบนี้คือ call site `GT-124` และข้อห้าม P-2 เท่านั้น] (มติข้อ 6 กฎ 2-3) · 🔴 เกรดไม่ได้จนกว่า `RE-139` ปิด (กฎ 4) · ใบเต็มอยู่ท้ายไฟล์)
- 🛠️ **`STORE-INSERT-001` [CHIEF-WORK · ไม่ใช่ใบเทส]** (✅ **CLOSED -- `#244` merged แล้ว (ยืนยันด้วย API รอบ R226: merged_at 2026-08-29T00:56Z)** · ~~🟡 push แล้ว รอ merge `pirate-force-server#244` (R224 `4gqnwm`)~~ — ~~#241~~ ถูกปิดเพราะเกตแดง (เทสของรอบนี้เองรั่ว sqlite handle บน Windows) แก้แล้วและเปิดใบใหม่บน branch เดิม — เจ้าของ: chief · ~~`store.py` ยังไม่มี INSERT แถวของที่เก็บได้ และไม่เดิน `character_backpacks.next_item_identity` ⇒ ของที่เก็บไม่รอดข้าม DB · เป็นตัวบล็อกเดียวของ `GT-142`~~ [chief R226: ทั้งประโยคเป็นอดีตแล้ว — `store.commit_acquired_backpack_item` อยู่บน main (#244) ตัวบล็อกของ GT-142 ดูบรรทัดของมัน] · M5 ครบกำหนด 31 ส.ค. 12:00 · ใบเต็มอยู่ท้ายไฟล์)
- 🆕 **`GT-147` COUNTER-RESYNC-RECOVERY-TOOL-001** (🔴 **BLOCKED-ON-TOOL · ไม่ด่วน — ห้ามขึ้นหัวคิว** · เปิดโดย chief R227 ตาม `COO-DECISION 20260829_1344` ทาง 3 · เครื่องมือกู้ตัวนับ `next_item_identity` ที่ล้าหลังแถวจริง (attended-only เจ้าของรันเอง · เซิร์ฟเวอร์ปิด · diff → หยุดถาม → ค่อยเขียน) + ตรวจรับงานแก้ข้อความ `PermissionError` ที่ชี้ `HYP-PF-008` ผิดเรื่องในใบเดียวกัน · สล็อตสร้างเครื่องมือ = คิวปกติของ chief หลังงาน M5 · เคสจริงยังไม่เคยเกิด — กติกา restore-ทั้ง-DB ใน `AGENTS.md` §7 กันเหตุแทบทั้งหมด · ใบเต็มอยู่ท้ายไฟล์)
- 🛠️ **`SKIPPINS-FRAGMENTS-001` [CHIEF-WORK · ไม่ใช่ใบเทส]** (🟢 **OPEN — เจ้าของ: chief** · `docs/PYTEST_SKIP_PINS.json` ไฟล์เดียวปิด PR ที่เกตเขียวไปแล้ว **2 ครั้ง** (`#231` สาย A · `#235` สาย B) เพราะสองสายเติม entry ที่บรรทัดเดียวกัน ⇒ แตกเป็น `docs/pytest_skip_pins.d/<โมดูล>.json` รายโมดูล · คำตัดสิน: `notes_to_chief/20260829_0710_CHIEF-DECISION-skip-pins-*` · ใบเต็มอยู่ท้ายไฟล์)
- 🔥 ~~**ใบแรกของกะ attended ถัดไป — ก่อนใบอื่นทั้งหมด รวม `GT-131`**~~ [chief R226: คำสั่งใหม่กว่า `COO-DECISION 20260829_1241` ข้อ 2 ยกใบ capture `GT-146` (ของ LANE-B ท้ายไฟล์ · PENDING บูตได้เลย) ขึ้นหัวคิวแทน — ใบนี้ต่อคิวถัดไป] (คำสั่ง COO 2026-08-28 23:45 ข้อ 3 · จดหมาย `20260828_2345_COO-DECISION-multi-drop-shape-ships-with-a-bounded-blast-radius.md`) · 🆕 **`GT-132` GROUND-DROP-COALESCED-GENERATION-DRAWS-N-LABELS-001** (⛔ **BLOCKED — LANE-B รอบ `j0u64p` วัดแล้วว่าใน `Bg0002` ตีมอนไม่ติดตั้งแต่ต้น ⇒ บูตแล้วได้ `NO-RESULT` เสมอ · ~~รอ chief แก้สองบรรทัดใน `runtime.py`~~ [LANE-B รอบ `k3qe9q`: ครึ่งของสาย B ส่งครบแล้ว — `mob_combat.open_ledger_for_scene_id()` + `field_mobs.roster_for_scene_id()` อยู่บน branch รอบนี้ · **ยังบล็อกอยู่** เพราะบรรทัดที่เรียกอยู่ใน `runtime.py` ซึ่งเป็นไฟล์ของ chief · ใบขอ `notes_to_chief/20260829_1445_LANE-B-CORE-REQUEST-scene-roster-binding-two-lines.md` (เขียนใหม่ 15:0x หลัง pf-adversary: ขอ **จุดประกอบ ledger ใหม่ตอนรู้ฉากแล้ว** ไม่ใช่สลับบรรทัดที่ `__init__` ซึ่งไม่มี scene id) · 🔴 ใบนี้ยังต้องรอ **faction bit ของ Bg0002** ด้วย ledger ไม่ใช่ด่านเดียว] · ~~🟢 READY — attended · ศูนย์สล็อต ไม่มีแฟล็ก~~** · เปิดโดย LANE-B รอบ `zxnwtd` ต่อจาก `RE-130` ✅ CLOSED · ฆ่ามอนตัวที่ตกของ ≥ 2 ชิ้น แล้ว**นับป้ายชื่อไอเทมสีแดงจากเฟรมวิดีโอ** · เซิร์ฟเวอร์เปลี่ยนทรงส่งเป็น collection เดียว count=N แล้ว · 🔴 มีด่านบิลด์บังคับก่อนนับ (`generations=1` ในคอนโซล) · `1` ป้าย = **FAIL ของใบนี้** (coalesce ไม่ซื้ออะไรให้ผู้เล่น) · ใบเต็มอยู่ท้ายไฟล์
  · 🔴🔴 **ต้องรันใน `Bg0002` เท่านั้น ห้ามรันในเมือง** — Port Royal เหลือหุ่นซ้อมสี่ตัวและหุ่น `916` มี `n_DROPS_*` = 0 ทั้งสามคอลัมน์ ⇒ ฆ่าในเมืองแล้วได้ **0 ป้าย** ซึ่งเป็น `NO-RESULT (ฉากผิด)` **ไม่ใช่ FAIL** (chief R221 จาก `20260829_0255_LANE-B-STATUS-*` บรรทัด 46-47))
- 🆕 **`GT-079` SCENE-278-ENTRY-AND-STAGE-EYECHECK-001** (🔴 **BLOCKED — BLOCKED-ON-WIRING** · ยังไม่มีเส้นทาง runtime ที่พาผู้เล่นเข้าฉาก 278 · เปิดใบโดย LANE-A ตาม `CHARTER-02` BUILD-002 สไลซ์ 1 (v2 / M2 · กำหนด 26 ส.ค. 23:59) · ถามด้วยตาหกข้อ: เข้าได้ไหม **และ HUD บอกว่าแมพอะไร** (ตัวแยกการอ่านค่า `scene_id` สี่แบบ) · มีพื้นไหม · กว้าง-เรียบ-โล่งไหมและสีอะไร · `BgNull` เสียหายไหม · เก้า placement โผล่ไหม · เดินได้และอยู่ครบ 10 นาทีไหม · 🔴 **มีขั้นตอนบังคับ "ทางกลับบ้าน"** เพราะฉาก 278 มี `n_MARKER=0`/`n_SAVE=0` · **ไม่ใช่ใบเรื่องการ *ย้าย* ฉากขณะ live — นั่นคือ `RE-077`** · ใบเต็มอยู่ท้ายไฟล์)
- 🆕 **`GT-080` EMPTY-VIEW-IS-THE-MAP-NOT-THE-SEND-001** (🟢 **หัวใบเดิมล้าสมัย — แก้โดยเจ้าของใบ LANE-A รอบ `o8cy9q` 2026-08-28T18:41+07:00:** เหตุบล็อกเดิมหมดไปแล้ว · วัดบน `main` รอบนี้: `runtime.py` **import ทั้ง `world_population` และ `world_density` จริง** และ `GT-121` ผ่าน (PASS) ยืนยันเส้นทางไร้แฟล็กส่งสำมะโนแล้ว ⇒ **ไม่ใช่ `BLOCKED-ON-WIRING` อีกต่อไป · ใบนี้รันได้ รอผู้เทสจับคิว** · 🔴 เพิ่มรอบ `o8cy9q`: บูตนี้จะพิมพ์โทเคนใหม่ `WORLD_IDENTITY_GUARD ... identity_provable=0` ต่อท้ายบรรทัด `WORLD_CENSUS` — **เป็นเรื่อง identity ไม่ใช่เรื่องจำนวน ไม่กระทบตัวคุมของใบนี้ อย่าอ่านเป็นความล้มเหลว** (`identity_provable=0` เป็นค่าที่ถูกต้องของทุกฉากตอนนี้ ไม่ใช่อาการผิดปกติ) · ~~ถ้อยคำเดิมของหัวใบ:~~ ~~🔴 **BLOCKED — BLOCKED-ON-WIRING** · `world_population`/`world_density` ยังไม่มีใคร import และเส้นทางไร้แฟล็กยังส่ง 3 ตัว (`v141:1863` `V112_TEST_INDICES=(0,30,91)` ใช้ที่ `:4292`) · เปิดใบโดย LANE-A 2026-08-26 ~02:2x (+07:00) ตาม `CHARTER-02` BUILD-001 / M1 · **แยกสาเหตุที่ `GT-078` แยกไม่ได้:** ยืนแล้วไม่เห็นใคร เพราะ **เซิร์ฟเวอร์ไม่ได้ส่ง** หรือเพราะ **ไฟล์ฉากไม่มีใครวางไว้ตรงนั้น** · ตัวคุมคือ **บูตเดียว สำมะโนเดียว ยืนสองจุด** (A จุดเกิดจริงที่ `GT-045` วัดไว้ census 500u = **0** · B จุดหนาแน่นสุดของฉาก census 2000u = **12**) · **เห็น 0-3 ตัวที่ A = ปกติ ไม่ใช่ความล้มเหลว** · ถ้า B เห็น 0 ทั้งที่ `WORLD_CENSUS assembled=115/115 wire=115` ⇒ ปัญหาอยู่ที่ **การเรนเดอร์** ⇒ ชี้ `GT-072` (ยัง PARTIAL) · **ไม่ใช่ใบวัดเพดาน (`GT-076`) ไม่ใช่ใบตรวจรับ v1 (`GT-078`)** · ใบเต็มอยู่ท้ายไฟล์~~ · 🔴 **ตัวใบเต็มท้ายไฟล์ไม่ถูกแตะ** — แก้เฉพาะหัวใบบรรทัดนี้ ตามกฎ "ห้ามลบประวัติเดิม ให้ขีดฆ่าแทน")
- 🆕 **`GT-074` OCCLUSION-CAMERA-ANGLE-CONTROL-001** (🟢 **PENDING — attended · รันได้บน `main` ปัจจุบันเลย ไม่รอ merge ไม่รอ CI** · **ศูนย์สล็อต · ~3 นาทีบนจอ** · เปิดโดย chief R170 · เก็บตกตัวคุมเดียวที่ `GT-072` รอบแรกไม่ได้ทำ: **หมุนกล้องอย่างเดียว ไม่เดิน ไม่คลิก** ในช่วง `+10..+29` เพื่อตัดทางหนีสุดท้ายของ "บังทับ" · 🔴 **ต้องรันก่อน `GT-032`** ด้วยเหตุผลเดียวกับ `GT-072` · ใบเต็มอยู่ท้ายไฟล์)
- 🆕 **`GT-226` LOGIN-DRAWS-THE-CLASS-SHE-PICKED-AT-CREATION-001** (🔴 **BLOCKED — รอ merge `pirate-force-server#705` (กิ่ง `claude/gallant-noether-3kwnnr`)** · เปิดโดย chief (LANE-E) รอบ `3kwnnr`/R332 ตาม `COO-DECISION 20260904_0446` ข้อ 2-3 · **ผู้รัน = Panya (attended)** · ชั้น wire/DB พิสูจน์แล้วรอบนี้ด้วย fixture Sniper (class 4) ⇒ **ใบนี้เกรดชั้นจอชั้นเดียว**: สร้างตัวใหม่เลือกคลาสที่ไม่ใช่ Gladiator แล้วไคลเอนต์แสดงคลาสนั้นไหม ทั้งล็อกอินครั้งแรกและครั้งที่สอง + control ตัวเก่าต้องยังล็อกอินได้ · `RECHECK` เป็นตัวปลดป้าย · ใบเต็มท้ายไฟล์)
- **`GT-072` ACTOR-SLOT-DISPLACEMENT-001** (🟡 **PARTIAL — ใบยังเปิด · ผลรอบแรกบันทึกโดย chief R170** · จ็อบ 1167/1168/1169 · 🔴 **ยังไม่มีค่าไหนถูกตัดออกเลย** — ตัวคุมทั้งสองที่เก็บมาถูกวัดที่ `+92.8` วิ **หลังทั้ง NPC และ actor ของเราหายจากจอไปแล้ว** ⇒ อำนาจแยกแยะเป็นศูนย์ · ตัวคุมที่ไม่ได้ทำ: `W2` มุมกล้อง · `W3` เข้าไปใกล้+คลิกในหน้าต่าง · `POST-A` ⇒ ยกไปใบ **`GT-074`** · เปิดโดย chief R168 จากผลข้างเคียงข้อ ④ ของ `GT-030-R3`: `SPAWN_BARE` ทับพิกัด `P0` แล้ว NPC `Navy Transfer` หายใน 0.6 วิ — **แยกไม่ออกระหว่าง despawn / แทนที่ / บังทับ** · ตัวคุมเชิงลบสามตัวฟรีในเลน · 🔴 **ต้องรันก่อน `GT-032`** เพราะ `GT-032` ทำให้ landmark `0x2001` ขึ้นศัตรู · ใบเต็มอยู่ท้ายไฟล์)

**🎮 ต้องเปิดเกม / ต้องใช้ตา Panya** — 🟢 **ปลดพักแล้ว (Panya 2026-08-24 ~21:1x +07:00 · จดหมาย 2120 §① · บันทึกโดย R155 — คำสั่งพัก 16:56 ของ 23 ส.ค. สิ้นสุด) · 🔴 ห้ามปิดด้วยรอบ unattended ยังบังคับเหมือนเดิม** (กติกาอยู่ใน `AGENTS.md` แล้ว)
- `GT-001` smoke recurring (🟢 pending · re-arm ค้าง) · `GT-030` (~~ห้ามรันรอบสาม~~ **ยกเลิกโดยเจ้าของ 18:15 +07:00** ⇒ ดู `GT-030-R3`) · `GT-030-R3` REMOTE-PLAYER-VIS-PROVENANCE-001 (✅ **PASS — ปิดโดย chief R168 · `OBSERVER_CONFIRMED: 2026-08-25T19:40+07:00`** · 🎯 ไคลเอนต์เรนเดอร์ `actor_type 2` ได้เป็นครั้งแรกในประวัติโปรเจกต์ · target panel เปิดแต่ **ช่องชื่อว่าง** (`HP. 0`/`LV. 1`) ⇒ ~~**ไคลเอนต์ไม่บริโภค `BasicAttr` name สำหรับ actor_type 2**~~ 🔴 **ถอนแล้วโดย chief R169** (รอบสี่พบว่า NPC `actor_type 4` ก็ช่องชื่อว่างเหมือนกัน ⇒ เป็นคุณสมบัติของ **แผงในบิลด์นี้** ไม่ใช่ของคลาส actor — ดูบล็อกถอนในใบ) · 🟢 **รอบสี่ (chief R169 · จ็อบ 1161/1162/1163) ปลดข้อผูกพันสองข้อ: ทำซ้ำครบสองรอบแล้ว + ผลลบ 45 วิแรกคุมกล้องได้จริงแล้ว** · 🔴 ที่ยังเหลือ: **ตัวคุม `ProbeControl03` ที่ `-9,290` ยังยืนยันจากวิดีโอไม่ได้สองรอบติด** (ผู้เทสเดินไปทาง `+X` ทั้งสองรอบ) + จูนนาฬิกาด้วย clapper · ผลข้างเคียงแตกเป็น `RE-071` และ `GT-072` แล้ว · ~~ถ้อยคำเดิมของใบ~~ 🟢 **READY — attended · คุณ Panya ขับเอง** · **ศูนย์สล็อต** ไม่แก้โค้ด/mask/ไบต์ (`HYP-PF-025` 2/5 คงเดิม) · ตอบสองข้อที่รอบ #12 และ rerun ตอบไม่ได้: **ชายหนุ่มชุดน้ำเงิน-ขาวที่ X ≈ `-8681` เป็นของแมพหรือของเรา** และ **transient สั้นกว่า 3.487 วิ** · 🔴 **ตัวยิงคือแชต ASCII 12 ตัว ⇒ ห้ามพิมพ์ clapper ตอนต้นรอบ** ลำดับคือ เดินสำรวจ → baseline → *แล้วค่อย* พิมพ์ `PFCHATPROBE1` · 🔴 รันให้จบก่อน `GT-032` เสมอ · ใบ `GT-030` เดิมอยู่ที่เดิมทั้งใบ ห้ามลบ) · `GT-033` ✅ **ANSWERED — ปิดโดย chief R166 (2026-08-25 ~17:5x +07:00)** · สามช่องจากสี่วัดครบในคืนเดียว **ผลลบทั้งสาม** ⇒ ไม่ใช่ response policy ตัวไหนในสองตัวที่เรามี 🔴 **ไม่ใช่ "connection-teardown ถูกหักล้าง"** (ไม่มีใครพิสูจน์ว่าไคลเอนต์เห็นการปิด socket) · 🔴 **`BLOCKED-INPUT` ตายแล้ว** (เป็นข้อจำกัดของเครื่องมือคลิกสังเคราะห์ ไม่ใช่ของไคลเอนต์ — มือคนกดผ่านสามรอบติด) ⇒ ทางต่อเป็น **static** ดู `RE-070` ใน `CLIENT_RE_QUEUE.md`
- `GT-034` (NO-RESULT ×2 — รอบสอง 2026-08-24 02:28: computer-use `list_apps` timeout ×3 หยุดก่อน input แรก · scenario ยังไม่ถูกยิง (`StartGameReq=0`) · ผู้เทสเสนอรอ **Panya เทสด้วยตา 2026-08-26** · tooling blocker "ffmpeg console ทับจอ" แก้แล้ว — ดู R143) · `GT-035` (✅ **PASS 2026-08-25 15:04-15:36 (+07:00) · สองรอบ สองผู้สังเกต · ปิดโดย chief R164** — หลอด HP ของ `0x201F` ลงครบบันได `3857 -> 2893 -> 2893 -> 771` · **ห้ามอ้างกับ GT-036** · "hostile" ยังไม่ถูกพิสูจน์ ป้ายชื่อเขียว ⇒ `RE-067`) / `GT-036` (🔴 **คง BLOCKED — เหตุผลเปลี่ยนโดย R164:** ไม่ใช่ "รอ GT-035" อีกแล้ว แต่ **ไม่มีเลนที่มีครึ่งตาย** (`HP_FLOOR` = FORBIDDEN ใน `HYP-PF-038`) ⇒ ต้องมีเวอร์ชันถัดไปของเลนก่อน **และรอคุณ Panya เคาะ**) · `GT-045` v2 (🟢 merge แล้ว — ก่อนบูตต้องผ่าน (ข) เช็ค resolver/BOOT_COMMIT ว่า clone ที่บูตมีเลน v2 จริง · ✅ (ค) ปลดแล้ว — Panya ปลดพักเลน attended 2026-08-24 ~21:1x จดหมาย 2120 §① (R155) · ถ้อยคำเดิม "พร้อมบูตทันที" ตัดเงื่อนไข (ข) ทิ้ง — แก้โดย R142 ให้ตรงจดหมาย R141)
- 🆕 `GT-058` LEARN-SKILL-RESULT client-observe (✅ **CLOSED — BOUNDED-NEGATIVE โดย R155** ตามคำตัดสิน Panya 2026-08-24 ~21:1x +07:00 จดหมาย 2120 §③ "ปิดเลย" · ขอบเขต: เทียบเนื้อในหน้าต่างสกิลไม่ได้เพราะ baseline เปิด K ไม่ได้ — อาการนั้นย้ายไปเป็นคำถามของ GT-059 · ดูหัวใบ)
- 🆕 `GT-059` SKILL-ATTR-WINDOW-GATE-001 (✅ **CLOSED — P2 (FALSIFIED) โดย R155** · ตัวปิด = ตา Panya บนวิดีโอต่อเนื่องสองไฟล์ FULLROUND (จดหมาย 2133 · 2026-08-24 ~21:33 +07:00): wire byte-exact PASS ×3 triggers แต่หน้าต่างสกิลไม่ขึ้นเลยทั้งสอง session · control C เปิดได้ = เกมไม่ค้าง ⇒ "รับ `CSkillAttr` แล้วหน้าต่างเปิดได้" ถูกหักล้าง · 🔴 nonclaims: A/B (กด K ในช่อง 3 วิ) ยัง UNRESOLVED → เปิดใบต่อ `GT-064` · สาเหตุ (slot-null vs check อื่น) ยังไม่รู้ — งานออกแบบตัววัด runtime ปลดล็อกแล้วตามเงื่อนไข 2120 §④ · ห้ามลบวิดีโอสองไฟล์บนสะพาน · ดูหัวใบ)
- 🆕 `GT-060` PICKUP-CLICK-CAPTURE-001 (🔴 BLOCKED-CONDITIONAL — ใบเปิดโดย R151 ท้ายไฟล์ · จับเฟรม `PickupTerrainThing` ตัวจริงตัวแรกจากคลิกซ้ายบน drop-object ที่วาดจริง — ตัดสิน id derive `0x4543` ถูก/ผิด · เงื่อนไข 3 ข้อ: ✅ (ก) ปิดแล้ว R152 — PR #22 merge เข้า `main` `2c0e3ba` (head `a64d589` เขียว(Actions run 32717828631 · subset) · tree-identical กับ merge commit · re-verify สี่ข้อบน `main` ผ่านครบ) · (ข) มี drop-object วาดจริงคลิกได้ในบูตเดียวกัน — 🟡 ครึ่ง composition ปิดแล้ว: **คำเคาะ Panya มาแล้ว (2026-08-24 ~18:3x +07:00 · จดหมาย `notes_to_chief\20260824_1831_PANYA-RULINGS-combine-scenarios-and-open-GT-063.md` §①): allow-list คู่ `ground-loot + pickup-listener` ร่วมบูตเดียวกันได้** (22 เลนที่เหลือ exclusive เหมือนเดิม · วินัยบังคับ: ทุกข้อสังเกตต้องระบุเลนผู้ก่อ ไม่งั้น NO-RESULT) · โค้ด composed-boot ✅ **merge เข้า `main` แล้ว (R154): PR #23 → merge commit `cad3e28` · head `99bfa96` เขียว(Actions run 32726495224 · subset · ทาง ci-status sha ตรง) · tree-identical · สวีตเต็ม main 2222/324 เขียว(cloud sanity R154)** ⇒ (ข) เหลืออย่างเดียว: **GT-045 เทสตา PASS (นัด 2026-08-26)** · ✅ (ค) ปลดแล้ว — Panya ปลดพักเลน attended (จดหมาย 2120 §① · R155) · 🆕 R155: allow-list ขยายเป็นสามตัว (2120 §②) — ✅ R156: PR โค้ด #25 merge เข้า `main` แล้ว (`3f87fc3` · เขียว run 32743688024) ⇒ รวมบูตกับ GT-063 ได้แล้ว · P4 ไม่มีวัตถุ = NO-RESULT ห้ามอ่านเป็นผลลบ)
- 🆕 `GT-063` ITEMOPERATE-RES-GREENLINE-SHAPE-001 (✅ **PASS — ผลปิด canonical คือ R158 (25 ส.ค. · จดหมาย `20260825_0230` · attended · Panya ขับเอง 01:12-02:09 · เปิดกระเป๋าตรวจจริง 1→5 + เทสหักล้าง 5→1→5 ⇒ โมเดล "$V2 = ยอดรวมปลายทาง client คำนวณ delta เอง") — ใบเต็มพร้อมสถานะ PASS อยู่ `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`** · 🔴 chief R232 แก้ตามใบ `20260829_1852` (กะ3-A): รอบ UC1/R230 เป็น **replication ที่สอดคล้องโมเดล R158** ไม่ใช่ผลปิดใหม่ (บูตซ้ำเพราะบรรทัดสารบัญค้างสถานะเก่า) · ผล UC1 (ใบ `20260829_1552` §① + `OBSERVER_CONFIRMED: 2026-08-29 (Asia/Bangkok) โดย Panya` ใบ `20260829_1728` §3): trigger `greenline001` → สามทรงออกครบ `ITEMOP_RES_CTRL_CAPTURE_REPLAY` 82B → `BAGUPD_ID2400901_QTY1` (+1068ms) → `BAGUPD_ID2400901_QTY5` (+~1ms) · จอขึ้นบรรทัดเขียว **หนึ่งบรรทัดเดียว** `ได้รับ[ Camouflage Item-Cask ] * 4` (4+ นาทียังบรรทัดเดียว) · ~~การอ่านเดิมของ R230: `* 4` สอดคล้องทรง control ⇒ ทรงสังเคราะห์สองทรงไม่ทำให้บรรทัดขึ้น~~ 🔴 **ถอนโดย chief R232 — ขัดโมเดล R158**: [สมมติฐาน — ตามโมเดล R158] CTRL (count=0) เงียบ · QTY1 (total=1 มี 1 ⇒ delta 0) เงียบ · **QTY5 (total=5 มี 1 ⇒ +4) คือเฟรมที่วาด `* 4`** ⇒ ทรงสังเคราะห์ BAGUPD ทำให้บรรทัดขึ้นจริง · ชี้ขาดได้ด้วยครึ่ง attribution จากเฟรมวิดีโอ 15:43:0x (ยัง AWAITING-OBSERVER · ไม่บล็อกใบ) · nonclaim ① เดิม (ของอยู่รอดข้าม session) ยังเปิด — ทางปิดคือ STORE-INSERT-001/GT-142 · 🟡 ครึ่ง attribution รายทรง (บรรทัดโผล่ตรงจังหวะทรงไหนเป๊ะ) = AWAITING-OBSERVER จากเฟรมวิดีโอ 15:43:0x — ไม่บล็อกการปิดใบ · ~~ถ้อยคำเดิม:~~ 🟡 **READY-CONDITIONAL (R155)** — ยิง `ItemOperateVitalRes` `0x4C13` สามทรงแล้วดูจอจริงว่าทรงไหนทำให้บรรทัดเขียว `ได้รับ [<ชื่อ>] * <จำนวน>` ขึ้น · (ก) ✅ ปิดแล้ว R155: **PR #24 merge เข้า `main`** — merge `960716c` · head `1435064f` เขียว(Actions run 32733905271 · subset · ci-status sha ตรง) · tree-identical · flag `--item-operate-res-hypothesis-scenario` + `scenarios/item_operate_res_greenline_sweep.json` · trigger = แชต 12 ตัวอักษร ASCII ใด ๆ (ตกลงใช้ `greenline001`) · label สามตัว `ITEMOP_RES_CTRL_CAPTURE_REPLAY / BAGUPD_ID2400901_QTY1 / BAGUPD_ID2400901_QTY5` (count=0 ทุกเฟรม · มิติ count>0: RE-064 ✅ ปิดแล้ว R156 — ทรง pin แล้ว แต่ยังไม่ compose รอผลตาใบนี้ + คำเคาะ Panya ตาม ledger) · (ข) ✅ ปลดแล้ว — Panya ปลดพัก attended (2120 §① · R155) ⇒ **บูตเดี่ยวได้แล้ว** · (ค) ✅ **ปิดครบ R156: PR #25 merge เข้า `main` แล้ว** — merge `3f87fc3` · head `fc4010e` เขียว(Actions run 32743688024 · subset · ci-status sha ตรง) ⇒ **บูตรวมสามเลนได้แล้ว** · 🆕 R156: rider RE-064 ตอบแล้ว — 15-byte PC prefix IDENTICAL 15/15 ⇒ ถ้า control frame โดน ErrorData ให้ชี้ session context ไม่ใช่ envelope prefix · attribution สามเลนบังคับ: แยกเลนผู้ก่อไม่ออก = NO-RESULT · ปิดใบได้เฉพาะเห็นข้อความบนจอที่อ่านออก — "ไม่ขึ้น" ทุกแบบ = NO-RESULT ห้ามเขียนว่า "ไม่มี/ไม่เกิด")
- 🆕 `GT-064` SKILL-ATTR-WINDOW-KPRESS-IN-GAP-001 (✅ **CLOSED — PASS(P2) โดย R158 · ใบเต็ม archive แล้ว `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`** · ~~ถ้อยคำเดิม: 🟢 READY — ใบเปิดโดย R155~~ 🔴 **บรรทัดสารบัญนี้ค้างสถานะเก่า — แก้โดย chief R232 ตามใบ `20260829_1919` §③ (กะ3-A): ผู้ช่วยสองเซสชันเพิ่งแนะนำ owner ว่ารันได้ทั้งคู่ทั้งที่ปิดไปแล้ว ห้ามเสนอบูตซ้ำ** · คำถามสกิล-window ไปต่อที่ `GT-116` (PASS — หน้าต่างเปิดได้เมื่อ class/level จริง))
- 🆕 `GT-069` GROUNDLOOT-NAMELABEL-TEXTPROP-SELECTOR-001 (🔴 **BLOCKED ×2** — ใบเปิดโดย R165 ท้ายไฟล์ · ยิง **เฟรมคุม mask `0x12` (ไม่มี selector) กับเฟรมทดลอง mask `0x3A` (gate `+0x1B`=1 · index `+0x1A`=6) ที่พิกัดเดียวกัน dword เดียวกัน** แล้วดูว่าหน้าตาป้ายชื่อไอเทมต่างกันไหม — ตัวแปรเดียวคือ "สองฟิลด์ selector มี/ไม่มี" ⇒ **ทุกทางออกอ่านได้ รวมถึงผลลบที่สะอาด** · ที่มา `RE-067`: เลนที่ ship อยู่ส่ง mask `0x12` มาตลอด ⇒ ทุกป้ายที่เราเคยวาดใช้ default property `0x34` ⇒ **สีที่เคยจดไม่ใช่สีที่เราเลือก** · 🔴 **เงื่อนไข (1) คุณ Panya เคาะเรื่องงบเวอร์ชัน — ยังไม่เคาะ** (`HYP-PF-032` เต็ม 3/3 และ `expiry.decision` ของมัน **ไม่มี clause "เปิดใบใหม่ได้"** ต่างจาก `HYP-PF-029` ที่มี ⇒ บรรทัดฐาน `HYP-PF-038` เอื้อมไม่ถึง) · **โค้ดอยู่บน branch `claude/elegant-lamport-ywug3f` และจงใจไม่ merge** ⇒ ถ้ายังไม่เคาะ ใบนี้รอเจ้าของ ไม่ใช่รอผู้เทส ไม่ใช่รอ CI · 🔴 เงื่อนไข (2) ด่านก่อนบูตเจ็ดข้อ · 🔴 **`0x34`/`0x5D..0x62` เป็น UI *text property* ไม่ใช่ "สี" — ห้าม join กับ `FONT_COLOR.n_ID`**)

**🔬 งาน static — ทำเมื่อไรก็ได้ ไม่ต้องมีคนเฝ้า ไม่ต้องจับ `LOCK_GAME` · ขนานกับรอบเทสเกมได้:**
- ใบเก่าในไฟล์นี้: `GT-047` (🟠 จ็อบ 0 ปิดแล้ว 09:16 — source เข้ามือ chief · **R144 ส่ง patch การ์ด `field_offset` กลับแล้วที่ `patches/gt047/` (เขียว 8 ด่านบน cloud) · เหลือฝั่งสะพาน apply patch แล้ว rerun จ็อบ 1–3**) · `GT-049` (✅ **PASS/DONE — ผลหน้าสะพาน 2026-08-24 09:23 · บันทึก R144:** id 131 ยิงจาก **inbound** `ItemOperateVitalRes` handler `0x005EF5E0` → chat emitter `0x005CC309` — คนละเลนกับ `PickupTerrainThing` 0x1F/0x03/0x22 ของ GT-046 ⇒ **บรรทัดลูทสีเขียว = เซิร์ฟเวอร์ตัดสินการเก็บ** — ดีไซน์เลนลูทฝั่งเราต้องส่ง `ItemOperateVitalRes` เอง)
- 🆕 ใบใหม่ตั้งแต่ R128 อยู่ไฟล์ใหม่ **`CLIENT_RE_QUEUE.md`** (คำสั่ง 18:22 ข้อ ③): ✅ **ปิดแล้ว 3 ใบ (ผลหน้าสะพาน 2026-08-24 ~00:3x–00:4x +07:00 · บันทึก R135):** `GT-054` PASS (spans **392/392** ตรงอิมเมจ · mismatch 0) · `GT-053` PASS (**N=106 ≥ 61 ⇒ `0x203D` in-band ⇒ H1 รอด**) · `GT-052` PASS (crosswalk class/skill ครบ · ผลลบ: ไม่พบ legend ของ `n_TARGET` ในชุดที่ค้น — ห้ามตั้ง label) — 🟡 `GT-050` **PARTIAL** (00:55: จ็อบ 1–3 ปิด · `CLearnSkillResultVital` CLOSED · direction `TriggerCastSkillVital` ชนเพดาน static — ทางต่อ observe-only attended) — ✅ `GT-055` **PASS/DONE** (ผลหน้าสะพาน 2026-08-24 02:41 · บันทึก R143: `0x36DB` = **string8** tag `0x44` · `0xAC52` = UTF-16LE tag `0x48` ⇒ parser เราผิดจริงฝั่ง `0x36DB` — แก้แล้ว: PR โค้ด #16 รอ gate ยังไม่เข้า main ณ R143) — **ที่ยังเปิดจริงในไฟล์นั้น: 0 ใบ — `RE-062` ปิด DONE โดย R152** (คำตอบ (ค): inbound ไม่เขียน `[actor+0x3E8]` — กุญแจอ่านผลลบ GT-059 · `RE-056` ปิด DONE/METHOD-FAIL · `RE-057`/`RE-058` ปิดโดย R144 · `RE-059`/`RE-060`/`RE-061` ปิดโดย R149 — ดูหัว `CLIENT_RE_QUEUE.md`) · 🔴 **บรรทัดนี้ล้าสมัยตั้งแต่ R165 — แก้โดย R166:** ที่เปิดจริงในไฟล์นั้นตอนนี้คือ **2 ใบ** — 🟢 `RE-068` ACTOR-NAMEBOARD-VALUE-034-SEMANTICS-001 (เปิดโดย R165) · 🟢 🆕 `RE-070` ORCHESTRATOR-TRANSITION-GATE-001 (เปิดโดย R166 — ทางต่อของ `GT-033` ที่ปิดเป็น ANSWERED · เป้า: ใครเซ็ต MODE `[orch+0x28]` ของ vtable `0xf45030` และ `[orch+0x24]` เป็น gate หรือแค่ display) · 🔢 **เลข 069 ไม่ว่างเพราะ `GT-069` ใช้อยู่ — ตัวนับสองคิวเป็นชุดเดียวกัน**
  🔴 **บรรทัดบนนี้ล้าสมัยอีกครั้ง แก้โดย R298 (2026-09-02):** ข้อความ "ที่เปิดจริงในไฟล์นั้นตอนนี้คือ 2 ใบ — RE-068 · RE-070"
  **ไม่จริงแล้ว** ทั้งสองใบ archive ปิดไปตั้งแต่ 2026-08-27 · และ **ห้ามสรุปสถานะคิว RE ด้วยมือในไฟล์นี้อีก** —
  บล็อกสรุปที่หัว `CLIENT_RE_QUEUE.md` ที่บรรทัดนี้เคยชี้ไป ถูกย้ายเข้า archive แล้วด้วยเหตุผลเดียวกัน (มันค้าง 8 วันแล้วหลอกคนอ่าน)
  สถานะจริงของคิว RE ตอบด้วยคำสั่งเดียวเท่านั้น: `python tools_bridge/pf_re_queue_taglint.py --list-open` (ดู `PROCESS_GATES.md` §18)
- 📊 ค้างที่ต้องมองเห็น: ชุดส่งมอบ RE **8 ตาราง 17,618 แถว data** ผ่าน re-derive แล้ว · ✅ **โค้ดอ่านตัวแรกมาแล้ว R131** (`tools/pf_external_registry.py` · ✅ merge เข้า `main` แล้ว R133 — `1e0b20b`) · ✅ **R145: ครบ 8/8 ตารางบน `main` แล้ว** (สามใบท้ายเข้าที่ `579b468` · นับแถวจริง 519+290+11 = 820 ตรงพิน) — ไม่มีอะไรค้างรอหน้าสะพานในเลนนี้อีก (ดูหัว `CLIENT_RE_QUEUE.md`)

🔴 ก่อนสั่งถอดอะไรใหม่: ค้น `pf_bridge\external\` ก่อนเสมอ — เริ่มที่ `external\00_SEARCH_HERE_FIRST.md` (คำสั่ง 18:22 ข้อ ④)
🔴 🆕 R132: และค้น **`pf_bridge\gamedata\`** (ตารางข้อมูลเกม 188 ตาราง — จดหมาย 2150) ก่อนเปิดใบขุดข้อมูลเกมทุกใบ —
เริ่มที่ `gamedata\00_SEARCH_HERE_FIRST.md` · ✅ **เข้า git แล้ว** (commit `0801541` · ตาราง+`lua/`+`scene/`+API spec — สถานะจริงดูหัว `CLIENT_RE_QUEUE.md` · บรรทัดนี้เคยเขียนว่า "ยังไม่เข้า git" ซึ่งล้าสมัย — แก้โดย R142)

---

> 📌 **R145 (2026-08-24 ~11:xx +07:00 · chief cloud) — บริโภคผลหน้าสะพาน 6 ใบ (GT-001/GT-045/GT-058×3/Lua census) + ปิดของค้าง external 8/8 + แก้เลนโค้ดตัวอ่าน:**
> ✅ **GT-001 → PASS** (recurring · green `fa1e804` · selected 9→10 · CANON_SHA อัปเดตโดยสะพาน `670CE534…`)
> 🟡 **GT-058 → WIRE PASS / CLIENT BOUNDED-NEGATIVE / NO-CRASH** (5 เฟรม `0x673C` รับครบ frame-sha ตรง pin · จอไม่ขึ้นอะไร · 🔴 **finding: หน้าต่างสกิล K เปิดไม่ได้เลยใน local baseline** — C/Quest/Reward เปิดได้ เฉพาะ Skill ตาย · กด K ไม่มี application request วิ่ง = อาการฝั่ง client ล้วน) · ยังปิดใบไม่ได้ (เทียบ content ในหน้าต่างสกิลไม่ได้) — คำถามถึง Panya
> 🔴 **GT-045 v2 → WIRE PASS / CLIENT NO-RESULT** (near/far masked-sha ตรง pin · แต่กล้องถูก geometry บัง + control ไปจุดอื่นไม่ได้ ⇒ ห้ามปิดเป็นผลลบ · รอเทสตา Panya)
> 📦 **ชุดส่งมอบ RE ครบ 8/8 บน git** (3 ใบท้ายเข้า `579b468` · 820 แถวตรงพิน) ⇒ `tools/pf_external_registry.py` ครอบ 8 ตาราง + internal-consistency check (🔴 หลัง adversary: priority/census เป็น projection ของ serializer table — **ไม่ใช่ derivation อิสระ** · check ยืนยัน projection ไม่หลุด sync + grammar gate + evidence→inventory join จริง 290/290) · สวีต 2035/324/0 เขียว(cloud sanity) · SKIP-CENSUS 12→26 · **PR โค้ดรอ gate**
> 📌 **คำถามค้าง #1 ของ R144 (เลนลูท) — ตอบแล้ว: `ItemOperateVitalRes` encoder มีอยู่แล้วใน `inventory.py` 3 ทรง** ⇒ ไม่ต้องเปิดเลนใหม่ · ที่ขาดคือ 2 ใบสะพาน (RE-059 ไบต์จริง Res · RE-060 สคีมรหัสไอเทม `26xxxxx`)
> 📖 **Lua API census (จดหมาย `0951`):** 59/160 ชื่อผูกกับ stub no-op `0x0045FA00` (รวม `Player.MobAppear` 3,532 calls!) ⇒ **ห้ามใช้ call_count เดี่ยว ๆ เป็นลำดับความสำคัญ** ต้องอ่านคู่ `binding_status` · 47 IMPLEMENTED · 51 UNRESOLVED
> ⏱️ **erratum:** บล็อกเวลา R144 เพี้ยน 7 ชม. (จริง 09:51–10:21 +07:00 ไม่ใช่ 16:4x–17:4x) — แก้ในบล็อกสถานะ GT-047

> 📌 **R143 (2026-08-24 ~09:0x +07:00 · chief cloud) — บริโภคจดหมาย 6 ใบหลัง sync ฝั่งสะพานกลับมาเดิน · ปิด 2 ใบ static + แก้บั๊ก parser:**
> ✅ **GT-055 → PASS/DONE** (ผล 02:41: `0x36DB` string field = **tag `0x44` + uint32le byte_len + string8** — 32 ASCII bytes ไม่มี `00` สลับ (GT-018 · corroborate GT-010/011) · `0xAC52` = **tag `0x48` + uint32le byte_len + UTF-16LE** (GT-019) · ป้าย `UNTAGGED_*` ของชุดส่งมอบ = ขอบเขต helper ไม่ใช่ full-wire claim)
> ⇒ **parser เราผิดจริงฝั่ง `0x36DB`** — chief แก้ในรอบเดียวกัน: `opaque_utf16le`→`opaque_string8` · เลิกบังคับความยาวคู่ · dated amendment HYP-PF-015/021 (5 จุด) + re-pin ledger sha · **PR โค้ด #16 (`fa1e804`) เปิดแล้ว รอ gate — ยังไม่เข้า `main` ณ ตอนเขียน · ถ้ารอบหน้าไม่เห็น merge ให้เช็ค PR #16** · ฝั่ง `0xAC52` โค้ดเราถูกอยู่แล้ว ไม่แตะ
> ✅ **RE-056 → DONE/METHOD-FAIL** (ผล 07:28: registrar `0x5F3DF0` = prototype tree ฝั่ง inbound `CreateById` — control `PickupTerrainThing` ก็ถูก register ทั้งที่ outbound จริงไปทาง `0x006B0639`→`0x005DD800` นอก tree ⇒ วิธี registrar จำแนก outbound ไม่ได้ ตกที่ control ⇒ **เลน static ของ direction ปิดถาวร** · direction `TriggerCastSkillVital` ยังไม่ตัดสิน · ทางต่อ = observe-only attended — พักตามคำสั่ง 16:56)
> 📩 **GT-034 → NO-RESULT รอบสอง** (02:28: computer-use `list_apps` timeout ×3 — หยุดก่อน input แรก · wire/DB สะอาด scenario ไม่ถูกยิง · ผู้เทสเสนอรอ **Panya เทสด้วยตา 2026-08-26**) · 🛠️ tooling: ผู้ช่วยส่งผล recorder ใหม่ — ซ่อนคอนโซล ffmpeg + frame proof ผ่านแล้ว (`staged\TEMPLATE_video_recorder.ps1` · เข้า `main` แล้วเป็น `79024e6` — commit local เดิม `234c51f` ถูก sync 08:22 rebase) ⇒ blocker "คอนโซลทับจอ" ของ GT-034 รอบสองถูกปิด (ครึ่ง `list_apps` timeout ยังเปิด)
> 🔧 **sync ฝั่งสะพาน:** ตัน 94 ครั้ง (ff-only + allowlist trap) — **แพตช์ทั้ง 5 จุดลงมือแล้วโดยผู้ช่วย ตามคำสั่ง Panya ~08:3x** (ห้ามเปิดใบซ้ำ) · ไฟล์ shared-tracked (`AGENTS.md` `.gitignore` `agent_kit` ฯลฯ) เดินทางออกอัตโนมัติแล้ว · `AGENTS.md` เคยขาดกฎ 7 ก้อน — คืนครบแล้ว (commit `936c4cc` บน `pf_bridge` main)
>
> 📌 **R135 (2026-08-24 ~08:1x +07:00 · chief cloud) — บริโภคผลหน้าสะพาน 3 ใบ + คำสั่ง prefix:**
> ✅ **GT-054 → PASS/DONE** (span verify: **392/392 distinct spans ตรงไบต์จริงในอิมเมจ** · mismatch 0 · unreadable 0 · image_sha256 `96272114…8623` · รันที่ server main `1e0b20b`) ⇒ **spans ทั้ง 392 ของ `PF_SERIALIZER_FIELDS.tsv` verified กับอิมเมจแล้ว** — AGREE ที่ยืนบน span ใน `FINDINGS_R134_EXTERNAL_XCHECK.md` (เช่น CHitResult §2.1) แข็งขึ้นหนึ่งชั้น · ⚠️ คอลัมน์ VA ของ `PF_PROTOCOL_REGISTRY.tsv` (AGREE §2.2) และตารางอื่นของชุดส่งมอบ **ไม่ได้ถูก verify โดยใบนี้**
> ✅ **GT-053 → PASS/DONE** (`Bg0002.npc` มี **N=106 placements ≥ 61** · index 60 f32 triple ตรง scenario bit-exact ⇒ `0x203D` in-band ⇒ **H1 รอด** — SCENE-005 เข้าตารางเคส in-band ของ GT-051 · สูตร band ยืนยันที่ scene 2 เพิ่มจาก bg0001)
> ✅ **GT-052 → PASS/DONE** (CHARCREATE_CLASS 5 แถว bit 1/2/4/16/32 · SKILL_CONTEXT 2165×20 · ชื่อผูกได้ 898 จุดตัด · bit 8 = Voodoo/Voodooist มีข้อมูลแต่ไม่มีแถวสร้างตัวละคร · **ผลลบ: ไม่พบ legend ของ `n_TARGET` codes 0/1/2/4/5 — ห้ามตั้ง label**)
> 🟡 **GT-050 → PARTIAL** (ผล 00:55 มาถึงกลางรอบ): จ็อบ 1–3 ปิด — span PASS · re-derive PASS ·
> **`CLearnSkillResultVital` codec CLOSED** (`count u16/0x12` + records 12 ไบต์ `(u32·u16·u32)` + trailing `u8/0x0B`) ·
> จ็อบ 4 bounded negative: direction/trigger ของ `TriggerCastSkillVital` ชนเพดาน static (ไม่พบ chain ไป outbound `0x005DD800` ·
> indirect ยังปิดไม่ได้) — ทางต่อเป็น observe-only probe แบบ attended (เลนพักตามคำสั่ง 16:56)
> 📦 **Lua/NPC ถอดครบบนสะพาน** (จดหมาย 0055 ใบสอง): Lua 616/616 · `.npc` 289/289 exact-EOF · correction:
> u16@0x2 = **definition_count** ไม่ใช่ placement_count (bg0001 def 113 / actual 149) · **Bg0002 actual placements = 106
> ตรง GT-053 โดยอิสระ** ✓ · ยังไม่เข้า git (รอกวาดตรวจ + whitelist) · Lua API census: 160 ชื่อ 12,653 calls
> (`Player.MobAppear` 3,532 · `Quest.RewardItemSelect` 1,335 · `Player.AddItem` 1,430)
> 🔤 กฎ prefix `GT-`/`RE-` มีผลแล้ว (หัวไฟล์) — ใบ static ใหม่เริ่ม `RE-056` ใน `CLIENT_RE_QUEUE.md`
> จดหมายผล: `notes_to_chief\20260824_0033_*` · `_0038_*` · `_0044_*` · `_0055_*` ×2 · คำสั่ง: `_0025_*`

> 📌 **R132 (2026-08-23 ~22:0x +07:00 · chief cloud) — บริโภคจดหมาย 21:50: gamedata แกะครบ 188 ตาราง ⇒ scope-cut 3 ใบ + กฎใหม่:**
> 📦 **ข้อเท็จจริงใหม่ (ชั้น client-static · จดหมาย `20260823_2150_GAMEDATA-EXTRACTED-…`):** ผู้ช่วยแกะตารางข้อมูลเกมจาก 4 ไฟล์
> (CONSTDATA_TH 120 · TEXTDATA_TH 65 · QUESTDATA_TH 2 · QUESTTEXT_TH 1) เป็น TSV ครบ **188 ตาราง / 2,365 คอลัมน์** ที่ `pf_bridge\gamedata\`
> (ตัวถอดเดิม `parse_pc_tables.py` พังมาตั้งแต่ 13 ส.ค. — อ่านชนิดฟิลด์หลัง version ผิดใน CONSTDATA/QUESTDATA)
> ✂️ **GT-049 scope-cut — จ็อบ 1 ปิดแล้ว:** template บรรทัดสีเขียวเจอจริง `TEXTDATA_TH__MESSAGE.tsv` **id 0x83 (131)** = `ได้รับ [ $V1 ] * $V2`
> ⇒ เหลือจ็อบ 2-4 (หาตัวยิง id 131 ในไบนารี — คำถามทิศทางเลนยังเปิดอยู่เต็ม) · ดู addendum ในใบ
> ✏️ **GT-046 addendum:** message id ทั้งสามที่ใบจดว่า unbound ตอนนี้ bound แล้วจากตาราง MESSAGE:
> `0x1F`=ระยะไกลเกิน · `0x03`=กระเป๋าเต็ม/ชนเพดานจำนวน · `0x22`=**ไอเทมของผู้อื่น เก็บไม่ได้** ⇒ เกมมีระบบเจ้าของไอเทม + เช็คกระเป๋า + เช็คระยะ
> (ทั้งสามเป็นข้อความ "ล้มเหลว" ทั้งหมด — หนุน [ตีความ] ว่า `ได้รับ` ยิงจากระบบกระเป๋า ไม่ใช่ handler นี้ · ยังไม่พิสูจน์)
> ✂️ **GT-052 scope-cut (ใน `CLIENT_RE_QUEUE.md`):** ตารางเป้าหมาย dump แล้วทั้งคู่ — `CHARCREATE_CLASS` 5x38 (n_ID เป็น bitmask · ไม่มี voodooist)
> · `SKILL_CONTEXT` 2,165x20 (SP/CD/target/cast-condition ครบ) ⇒ ใบเปลี่ยนจาก "ไปดึงตาราง" เป็น "ตีความคอลัมน์ + ผูก TEXTDATA + ผูกไอคอน"
> 🔴 **กฎใหม่:** ก่อนเปิดใบขุดข้อมูลเกม ค้น `pf_bridge\gamedata\` ก่อนเสมอ + ทุกใบมีช่อง `ค้น gamedata แล้ว: เจอ <อะไร> / ไม่เจอ` (บรรทัดหัวไฟล์ + หัว `CLIENT_RE_QUEUE.md`)
> ⏳ **รอ Panya เคาะ:** whitelist `gamedata\` เข้า git หรือไม่ (เนื้อหาเกมโดยตรง — ต่างจาก `external\` เชิงลักษณะ · ผู้ช่วยไม่ตัดสินเอง · chief ก็ไม่ตัดสินแทน) — คำถามอยู่จดหมาย `FROM_CHIEF_R132_*`
> ลำดับที่ค้างไม่เปลี่ยน: **GT-053 → GT-052 (หดแล้ว) → GT-050 → เลน headless สกิล → GT-049 (เหลือจ็อบ 2-4) → GT-047 จ็อบ 0** · ใบ attended ทั้งหมดรอ Panya

> 📌 **R128 (2026-08-23 ~18:0x +07:00 · chief cloud) — บริโภคคำสั่ง Panya 16:56 + scope-cut 17:18 · พักเลน attended · เปิดเลนสกิล:**
> ① 🔴 **คำสั่ง Panya 16:56 — พักทุกใบที่ผลชี้ขาดด้วยตาคน:** `GT-045`(rerun) · `GT-030` · `GT-034` · `GT-035` · `GT-036` ·
> **ห้ามสั่งรัน ห้ามให้ unattended ตัดสิน จนกว่า Panya จะว่าง** · รันเก็บหลักฐานได้ แต่ **สถานะต้องค้าง NO-RESULT / รอ Panya ยืนยันด้วยตา** เสมอ
> (เหตุ: จุดบอด attended วัดได้จริง — GT-045 รอบ 15:08 ภาพแรกหลัง trigger คือ `+3.560s` ⇒ 3.5 วินาทีแรก non-observed ไม่ใช่ absent)
> ② 🔴 **กฎใหม่ติดคิว:** ใบที่ผลชี้ขาดต้องใช้สายตามนุษย์ **ห้ามปิดด้วยรอบ unattended** — ตกลงมาที่ nonclaim ของทุกใบ eye-dependent
> ③ 🎥 **ข้อเสนอวิดีโอ (ฝากผู้รับงานสะพาน — chief แตะ template ไม่ได้):** อัดหน้าต่างเกม `ffmpeg`+`gdigrab` 30-60fps ตลอดช่วงถือ `LOCK_GAME` ·
> **ของเพิ่ม ไม่ใช่ของแทน** (ยังถ่ายภาพนิ่งเหมือนเดิม) · **แก้เรื่องเวลา ไม่แก้เรื่องมุมกล้อง** (กล้องไม่หันไปทางนั้น วิดีโอก็ช่วยไม่ได้ = จุดบอด ① ยังต้องใช้คน) · 🔴 **ห้าม push วิดีโอขึ้น git** (ใหญ่เกิน — เก็บบนดิสก์ อ้างพาธในจดหมาย)
> ④ 🆕 **เปิดเลนสกิล (STATIC-ON-BRIDGE · ผลเป็นตัวเลข เลี่ยงจุดบอด attended):** **GT-050 SKILLCAST-WIRE-001** (scope-cut: ตรวจแล้วใช้ ไม่ใช่ไปถอด) · **GT-052 CLASS-SKILL-TABLE-001** (ขยับเลขจากร่าง GT-049 ในจดหมาย 1656 — GT-049 ถูกใช้ไปแล้ว) — สองใบนี้ + **GT-053** อยู่ไฟล์ใหม่ **`CLIENT_RE_QUEUE.md`** ตามคำสั่ง 18:22 ที่มาถึงกลางรอบ · **GT-051 RENDER-SYNTHESIS-001 = chief ทำเองบน cloud รอบนี้** (ผลอยู่ `FINDINGS_R128_GT051_RENDER_SYNTHESIS.md` · stub ท้ายไฟล์)
> 🔴 **กติกาใหม่ (จดหมาย 1718):** ก่อนสั่งใครไปถอดอะไรใหม่ **ต้องเปิด `pf_bridge\external\*.tsv` (ชุดส่งมอบ RE ของ Codex) ดูก่อนเสมอ** — คำตอบหลายข้ออาจอยู่ในนั้นแล้ว (GT-050 คือหลักฐาน: แถวสกิลถอดไว้ครบ เหลือแค่ verify+ทิศทาง)
> 📎 สถานะแวดล้อม: **GT-045 v2 merge เข้า `main` แล้ว** (PR #10 · เขียว(Actions run 32631974238) · merge `e51bdac`) ⇒ เงื่อนไข "รอ merge" หมดไป **แต่ใบยังพักตามคำสั่ง ① — ห้ามบูตจนกว่า Panya จะว่าง**
> ⑤ ลำดับที่ค้าง: **GT-053 (ถูกสุด · ชี้ขาด H1) → GT-052 → GT-050 (สามใบนี้ใน `CLIENT_RE_QUEUE.md`) → เลน headless ของสกิล (หลัง GT-050 ปิด) → GT-049 → GT-047 จ็อบ 0** · ใบ attended ทั้งหมด (`GT-045`/`GT-030`/`GT-034`/`GT-035`/`GT-036`) **รอ Panya**
> จดหมายรอบนี้: `notes_to_chief\20260823_1656_PANYA-DIRECTION-pause-attended-open-class-skill-lane.md` + `notes_to_chief\20260823_1718_GT050-SCOPE-CUT-codex-registry-already-has-the-skill-answer.md`

> 📌 **R127 (2026-08-23 ~16:xx +07:00 · chief cloud) — บริโภครอบใหญ่ #14 (5 ใบ) · flip 4 + ใบใหม่ 1:**
> ✅ **GT-046 → PASS/DONE** (outbound คลิกเมาส์ · จาก live runtime drop-object · nonclaim สองระบบติดผล — สมมติฐาน "ของวางล่วงหน้า" ของผู้ช่วยถูกถอน)
> ✅ **GT-048 → PASS** (native scene-placement จาก `bg0001.npc` มีจริง ไม่ผ่าน wire · **GT-034 ไม่ปิด** — รอ GT-045 อ่านคู่)
> 🟠 **GT-047 → คง PENDING / TOOL-GUARD-GAP** — การ์ด `field_offset` ไม่แดงจริงตามที่ tester วัด · 🆕 **จ็อบ 0**: ส่ง source `pf_validate_capture_fields.py` เข้า repo ให้ chief patch (ดูใน entry)
> 🔴 **GT-045 → BLOCKED-รอ-merge v2** — รอบแรก wire exact แต่ geometry ตาย (spawn drift ~700 หน่วยจาก V135) + เกณฑ์ event เป็นเกณฑ์ที่สังเกตไม่ได้ (ตัดแล้ว — บั๊กใบสั่งของ chief) ⇒ เลนแก้เป็น **พิกัดอิง trigger** (PR R127 รอ gate) · **ห้ามบูต v1 ซ้ำ** · pass criteria ชั้น wire เปลี่ยนเป็น masked-template — อ่านใบใหม่ทั้งใบ
> ✅ **GT-001 PASS** (sessions 8->9 · `CANON_SHA.txt` ใหม่ `EE785A79…` tester อัปเดตแล้ว) · **re-arm ยิงใหม่รอบนี้** — PR R127 แตะ `src/` ⇒ หลัง merge บูตจาก resolver ใหม่เสมอ · ✅ **controls PASS: W/A/S/D/Q/E/wheel ใช้ได้จริง** (S 120ms ไม่ขยับ HUD — กดสั้นชนภูมิประเทศ · click-to-walk ปิดตามคำ Panya)
> 🆕 ท้ายไฟล์: **GT-049 LOOT-CHAT-TEMPLATE-001** [STATIC-ON-BRIDGE · พร้อม] — ใครยิงบรรทัดสีเขียว `ได้รับ [ชื่อ] * จำนวน` (ช่องว่างที่ GT-046 เปิดไว้ · ถ้า inbound = เซิร์ฟเวอร์ตัดสินการเก็บ = เปลี่ยนดีไซน์เลนลูท)
> ลำดับที่ค้าง: **GT-049 → GT-047 จ็อบ 0 → GT-045 v2 (เมื่อ merge) → GT-001 re-arm (หลัง merge เดียวกัน)** · GT-034/035/036 รอผล GT-045 v2 (+GT-048 ปิดแล้ว — อ่านคู่)
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R127_TO_ATTENDED_20260823_1700.md`

> 📌 **R126 (2026-08-23 ~14:1x +07:00 · chief cloud) — คำเคาะ Panya 13:15 บริโภคแล้ว · ใบใหม่ 1 + แก้ขอบเขต 2:**
> 🆕 ท้ายไฟล์: **GT-048** NATIVE-SPAWN-CONDITION [STATIC-ON-BRIDGE · พร้อม] — GT-034 เดินทาง ① ตามคำเคาะ:
> หาว่าอิมเมจ client มีเส้นทาง native spawn ตอน scene-load ไหม หรือ entity ทุกตัวต้องมาจาก wire ·
> ทาง ② (หลายจุดสังเกต) และทาง ③ (splice) **ยังไม่อนุมัติ ห้ามทำ** · GT-035/036 คง BLOCKED
> ✏️ **GT-046** แทรกจ็อบเพิ่ม 5-6 + nonclaim บังคับ (จดหมาย 1335: ระบบเก็บของมี ≥2 ระบบ — `PickupTerrainThing` อาจเป็นของระบบ "วางไว้ล่วงหน้า" ไม่ใช่มอนดรอป)
> ✏️ **GT-045** เพิ่มหมายเหตุตอนบริโภคผล: อ่านคู่ GT-034+GT-048 เสมอ · ผล render ไม่พิสูจน์การหยิบ
> ลำดับที่ค้าง: **GT-047 → GT-046 → GT-048 → GT-045 (🟢 พร้อมบูต) → GT-001 re-arm** (re-arm ค้างจาก R125 — ยังไม่มีผลเทสมาปลด · บูตจาก resolver ใหม่เสมอ) · GT-034/035/036 รอผล GT-048+GT-045
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R126_TO_ATTENDED_20260823_1420.md`

> 📌 **R125 (2026-08-23 ~12:0x +07:00 · chief cloud) — GT-045 ปลดจาก "รอ merge" → 🟢 PENDING-พร้อมบูต · คิวขยับใบเดียว:**
> PR #9 ของ repo โค้ด merge เข้า `main` แล้ว (merge `9e42cb7`) · resolver ให้ **BOOT_COMMIT `1343305`**
> เขียว(Actions run 32616696590 · subset บน runner ไม่ใช่ gate เต็ม) · chief ยืนยันสามข้อฝั่งคลาวด์ครบแล้ว
> (verdict ตรง SHA · flag `--ground-loot-hypothesis-scenario` อยู่ใน `app.py` จริง · `SCENARIO_PRESENT`)
> — **ผู้เทสยังต้องรัน resolver เองก่อนบูตตามบล็อก "ก่อนบูต" ในใบ เหมือนเดิม** (บูตคำตัดสิน ไม่ใช่ตัวเลขจากความจำ)
> ลำดับที่ค้าง: **GT-047 → GT-046 → GT-045 → GT-001 re-arm** (re-arm ยิงแล้วรอบนี้ — PR #9 แตะ `src/` · บูตจาก resolver ใหม่เสมอ อย่าก๊อปเลขจากแบนเนอร์)
> · GT-034/035/036 รอคำเคาะ Panya เหมือนเดิม
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R125_TO_ATTENDED_20260823_1205.md`

> 📌 **R124 (2026-08-23 ~10:4x +07:00 · chief cloud) — GT-045 ปลดจาก "รอ chief" · คิวขยับใบเดียว:**
> **GT-045 → 🟡 BLOCKED-รอ-merge** — เลนเซิร์ฟเวอร์สร้างแล้ว (HYP-PF-032 GROUND-LOOT-001 · PR รอ gate)
> ชื่อจริง: flag `--ground-loot-hypothesis-scenario` · scenario `scenarios/ground_loot_hypothesis_bit08_render.json`
> (ชื่อเสนอเดิม `groundloot-render-*` **เลิกใช้**) · ดีไซน์จริง: สองเฟรม เฟรมละหนึ่ง element ยิงเองตอนเข้าแมพ —
> **อ่านใบ GT-045 ฉบับแก้ใหม่ทั้งใบก่อนบูต** (steps/พิกัด/pass criteria เปลี่ยนหมด)
> ที่ค้างไม่เปลี่ยน: **GT-047 → GT-046 → GT-045 (เมื่อ merge) → GT-001 re-arm** · GT-034/035/036 รอคำเคาะ
> ⚠️ erratum เวลา: ทุกที่ที่ R123 เขียน "~16:xx +07:00" ให้อ่านเป็น **~09:0x +07:00** (แปลงโซนซ้ำ — ดูจดหมาย R124)
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R124_TO_ATTENDED_20260823_1030.md`

> 📌 **R123 (2026-08-23 ~16:xx +07:00 · chief cloud) — บริโภครอบใหญ่ #13 (14 ใบ) · flip 11 รายการ + ใบใหม่ 3:**
> ✅ PASS: **GT-038** (selection ไม่ใช่เงื่อนไขของเลข) · **GT-041** (no-rejection · relog = last-wire) · **GT-043** (survival · 0–3.524s unobserved) · **GT-042** (re-derive + erratum handler len 47) · **GT-044** (BG0001 = scene id 1) · **GT-001** (smoke `cf81730` · CANON_SHA ใหม่ `23FD885A…`)
> 🟡 **GT-034 NO-RESULT** (ไปถึงพิกัดคาดแต่ไม่เห็นตัว — GT-035/036 คง BLOCKED · รอ Panya เคาะทางไป) · 🟡 **GT-033C** ผลลบมีค่า (ไม่ transition · A/B ยัง BLOCKED-INPUT) · 🟠 **GT-030 CLIENT NO-RENDER** — ห้ามรันรอบสาม
> 🆕 ท้ายไฟล์: **GT-045** GROUNDDROP-RENDER [attended · 🔴 BLOCKED รอเลนใหม่+gate] · **GT-046** PICKUP-DIRECTION [STATIC-ON-BRIDGE · พร้อม] · **GT-047** RUNTIMEPROTO-CAPTURE-VALIDATE ปิด F2 [STATIC-ON-BRIDGE · พร้อม · ต้องรันบน Windows]
> **ที่ค้างสำหรับรอบเทสถัดไป: GT-047 → GT-046 → (GT-001 re-arm หลัง merge สำคัญถัดไป)** · GT-034/035/036 รอคำเคาะ · GT-045 รอ chief
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R123_TO_ATTENDED_20260823_1615.md`

> 📌 **R122 (2026-08-21 ~14:4x +07:00 · chief cloud) — คำตัดสิน Panya 11:04 บริโภคแล้ว · คิวขยับ 3 จุด:**
> ① **GT-034 → 🔴 BLOCKED-รอ-merge** (ปลดจาก "รอ Panya เคาะ") — เป้า `0x201F` Tornado Eagle · วิธี = ย้ายจุดวางตัวละคร+heading (GEO-PF-006 · commit `b665d92` รอ gate) · ใบเขียนใหม่ทั้งใบ มีบล็อกยืนยันสามข้อก่อนบูต
> ② **GT-035** แก้หัวข้อ: เหลือรอผล native-red อย่างเดียว (ระยะทางเคาะแล้ว) · GT-036 ไม่เปลี่ยน
> ③ 🆕 **GT-044** SCENEID-BG0001-001 [STATIC-ON-BRIDGE] = dump SCENE_NAME/MAP_SCENE_LIST ปิดเลข scene id ของ bg0001 (ท้ายไฟล์)
> ที่ค้าง: **GT-030(rerun) · GT-033(variant C) · GT-038 · GT-041 · GT-001 · GT-042 · GT-043 · GT-044** · GT-034 รอ merge · GT-035/036 BLOCKED
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R122_TO_ATTENDED_20260821_1500.md`

> 📌 **R120 (2026-08-21 ~10:4x +07:00 · chief cloud) — บริโภครอบใหญ่ #12 ต่อ + จดหมายผู้ช่วย GT-040 สามฉบับ · คิวขยับ 5 จุด:**
> ① **GT-032 → ✅ PASS** (ทั้งสองชั้น · เกณฑ์ console-event เดิมของ chief สังเกตไม่ได้โดยโครงสร้าง — แก้แล้ว ดูบล็อกผลใน entry)
> ② **GT-033 → 🟢 variant C พร้อมรัน** (HYP-PF-031 merge แล้ว · ปลดโดย chief R121 — ท่าบูตในบล็อก variant C ท้าย entry · A/B ยัง BLOCKED-INPUT)
> ③ **GT-040 → ✅ DONE** (ผู้ช่วยปิดครบ A/B/C · ผลยังไม่ผ่าน re-derive ปฏิปักษ์)
> ④ 🆕 **GT-042** DROPTHING-REDERIVE-001 [STATIC-ON-BRIDGE] = ใบตรวจซ้ำ GT-040 + decode `0x402A20` (ท้ายไฟล์)
> ⑤ 🆕 **GT-043** POP-SURVIVAL-001 = observation พ่วงเลนบิต `0x02` รอบใหญ่หน้า: ประชากรหายไหมหลังเฟรม count-1 (ท้ายไฟล์)
> ที่ค้าง: **GT-030(rerun) · GT-033(variant C) · GT-038 · GT-041 · GT-001 · GT-042 · GT-043** · GT-034 รอ Panya เคาะ · GT-035/036 BLOCKED
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R120_TO_ATTENDED_20260821_1055.md`

> 📌 **R119 (2026-08-21 ~09:2x +07:00 · chief cloud) — บริโภคผลรอบใหญ่ #12 แล้ว คิวขยับ 3 จุด:**
> ① **GT-031 → ✅ PASS** (ทั้งสองชั้น — ดูบล็อกผลใน entry) ② **GT-030 → 🟡 RERUN โปรโตคอลแก้ใหม่ทั้งใบ**
> (wire ผ่านแล้ว · สาเหตุที่หา probe ไม่เจอ = บรรทัดพิกัดฉบับเดิม stale — probe ผูกกับ NPC 'Navy Transfer' ไม่ใช่จุดที่ยืน
> ⇒ ท่าใหม่: เดินไป landmark ก่อนยิง + ระบุตัวด้วย target panel · **ไม่ต้องรอ merge อะไร — โค้ดเดิมใช้ได้เลย**)
> ③ บทเรียนเครื่องมือรอบ #12 ลงหมวด 🛠️ แล้ว (Return-ก่อน-คลิก ฯลฯ)
> ที่ค้าง: **GT-030(rerun) · GT-032 · GT-033 · GT-038 · GT-041 · GT-001** · GT-040 [STATIC-ON-BRIDGE] · GT-034 รอ Panya เคาะ · GT-035/036 BLOCKED
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R119_TO_ATTENDED_20260821_0920.md`

> 📌 **รอบ 109 (2026-08-20 ~19:3x) — คิวนี้ไม่ขยับ ไม่มีรายการใหม่ ไม่มีรายการไหนถูกปิดหรือย้าย**
> รอบนี้แตะ **CI อย่างเดียว**: gate ประกาศผลของตัวเองลง branch `ci-status` ได้แล้ว (ใบสั่ง Panya 19:10 "ทาง D")
> 🔴 **HEAD ของ repo โค้ดขยับ `9045978` → `89ce13b`** — เช็คก่อนบูตตามปกติและจดลงธง
> ✅ **แต่ไม่แตะ `src/` ไม่แตะ scenario ไม่แตะ tool ที่ผู้เทสใช้** ⇒ **พฤติกรรมเซิร์ฟเวอร์และเกมไม่เปลี่ยนเลย
> คิวทุกใบยังใช้ได้เหมือนเดิมทุกประการ**
> ที่ค้างอยู่เหมือนเดิม: **GT-030 · GT-031 · GT-032 · GT-033 · GT-001** (GT-031 ก่อน — เก็บภาพของ GT-028 ได้ในตัว)
> 🔴 **ยังค้าง: รอบใหญ่ #10 (GT-027 รันซ้ำ) ไม่เคย teardown** — รายละเอียดและ nonclaims อยู่ใน `LOCK_GAME.txt`
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R109_TO_ATTENDED_20260820_1930.md`

> 🔔🔔 **รอบ 108 (2026-08-20 ~18:45) — ขั้นแรกของทุกเซสชันเปลี่ยนแล้ว: อ่าน `pf_bridge\NEW_ORDERS.txt` ก่อนเปิดคิวนี้**
> chief กำลังย้ายไปอยู่บน cloud · ตัว sync (`pf_git_sync.ps1`, ทุก 5 นาที) จะดึงของที่ chief push ลงมาที่ดิสก์
> แล้วเขียน `NEW_ORDERS.txt` บอกว่ามีจดหมายใบไหนใหม่และ **คิวนี้ขยับหรือเปล่า**
> 🔴 **ถ้าไม่มีของใหม่ ไฟล์นั้นจะไม่ถูกแตะเลย ⇒ mtime ของมันคือสัญญาณ** · ถ้าคิวขยับ **ห้ามทำงานจากความจำ เปิดอ่านใหม่**
> 🔴 **ห้ามลบ/ย้ายไฟล์ใน `notes_to_chief\`** — ตัว sync ปฏิเสธ commit ที่มีการลบ *ทั้งก้อน* (เทส T6 พิสูจน์แล้ว)
> บริโภคจดหมายเสร็จ = **สำเนา**ไป `consumed\` + วาง stub `.CONSUMED.txt` · **ต้นฉบับอยู่ที่เดิมเสมอ**
> 🛡 **ระหว่างถือ `LOCK_GAME.txt` ตัว sync จะไม่แตะ repo โค้ดเลย** — โค้ดใต้เท้าคุณจะไม่เปลี่ยนกลางรอบเทส
> รายละเอียด: `FROM_CHIEF_R108_TO_ATTENDED_20260820_1845.md` · ติดตั้ง: `HOWTO_INSTALL_GIT_SYNC.md`
> ⚠️ **ทั้งหมดนี้ยังไม่มีผลจนกว่า Panya จะกด `SETUP_GIT_SYNC.bat`** — ยังไม่มีใครติดตั้ง

> 🗂 **โน้ตรอบ 78 (หลังบริโภคผลรอบใหญ่ #3) ย้ายไป `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260819_R85_HOUSEKEEPING.md`**
> (chief รอบ 85) — ทุกข้อปิดแล้ว: canonical sha ย้ายไฟล์เดียวเสร็จ (`CANON_SHA.txt`) ·
> GT-016 job รับเข้า `staged\` เสร็จ · lead เรื่อง GT-011/GT-013 ไม่รีเฟรช UI ถูกตอบแล้วโดย
> UI-REFRESH-001 รอบ 80 (ไม่มี erase-by-key ในไบนารี) → สืบทอดเป็น GT-018 (PASS แล้ว) ·
> GT-015 ที่ข้อ 4 พูดถึงยังเป็น 🟢 PENDING อยู่ในคิวนี้เหมือนเดิม ไม่มีอะไรเปลี่ยน

> 🗂 **แบนเนอร์อัปเดตรอบ 63 / 66 / 67 ย้ายไป `pf_bridge\archive\GAME_TEST_QUEUE_BANNERS_ARCHIVE_20260818_R75.md`** (chief รอบ 75) — ผลรอบปิดแล้ว เนื้อหาเต็มอยู่ใน CHIEF_CONTINUATION + reports/ · โน้ต decode และบล็อกนโยบายด้านล่าง **ยังใช้อยู่ อย่าข้าม**


> 🟢 **โน้ต decode (อัปเดตรอบ 52 จากรอบ 40):** unknown id ใน GT captures decode หมดแล้ว —
> `0x3D4B` = GetWorldInfoVital payload ครบทุกไบต์ (FINDINGS_R40): เฟรม 248B ก่อนกด logout
> ทุกครั้ง = เฟรมเปิด dialog ปกติ server ignore ได้ **อย่านับเป็น FAIL evidence** ·
> `0x1B40 LogoutVital` มี handler แล้ว (HYP-PF-012 echo + HYP-PF-013 ack_close — ทั้งคู่
> opt-in) แต่ **GT-007/GT-008/GT-026 พิสูจน์แล้วว่า echo/ack+close ไม่ทำให้ client ออกจากแมพ**
> 🆕 **รอบ 100 (agent D static RE) พบกลไกว่าทำไม: inbound `0x446F30` เป็น actor-vital reconcile pass ล้วน
> → echo ไม่มีวันทำ transition · การเปลี่ยนหน้าจริงขับโดย session/connection orchestrator (`0xf45030`) ที่รอแล้วปิด connection**
> ⇒ คำตอบที่ถูกน่าจะเป็น **ปิด/redirect GSCN connection** (candidate `ReturnSelectServerVital 0x709E`) → ต้อง attended A/B (GT-033)
> → **0x3D4B-first landed แล้วรอบ 53 (HYP-PF-016 opt-in — มีผลเฉพาะ GT-013 ที่บูตด้วย scenario worldinfo_first)**
> 🆕🔴 **แก้ความเชื่อเก่า (GT-026 2026-08-20):** "ปุ่ม logout ไม่มีธง = client freeze ต้อง End task" **ไม่จริง** —
> บน default scenario client **ไม่ freeze** แค่ไม่มีอะไรเกิด (ยังรับคลิก ปิดด้วย X ได้) · เทสอื่นยังวางแผน End task ได้เพื่อความปลอดภัย แต่ไม่ต้องกลัว freeze
> 🆕 **ทางเข้า logout ในเกม = ปุ่มหกเหลี่ยม `HOME` มุมซ้ายล่าง → เมนู → `ออก` (ล่างสุด ไอคอนประตู) → หน้าต่าง 3 ปุ่ม
> `กลับเข้าเกม`/`กลับหน้าเลือกตัวละคร`/`ออกจากเกม`** · ⚠️ **ปุ่มเฟือง (gear) มุมซ้ายล่าง = OPTIONS ไม่ใช่ logout** · X ในแมพ = dialog ยืนยัน "ต้องการปิดเกมหรือไม่?" (`ยืนยัน`/`ยกเลิก`)
> `0xAC52` = Channel_LocalTalkMessageVital (CHAT-ECHO-002) ไม่ใช่ unknown แล้ว

> 🔵🔵🔵 **นโยบายทีมใหม่จาก Panya (17:40 — เขียน 17:51, บล็อกเต็มอยู่หัว CHIEF_CONTINUATION.md):**
> คิวนี้เดินแบบ "รอบใหญ่" — chief สะสมรายการ UI test เป็น PENDING ให้**พร้อมรันทันที**
> (steps ทีละคลิก + pass criteria สองชั้น + nonclaims) · headless replay chief ทำเองได้เลย
> ไม่ต้องเข้าคิวนี้ · เมื่อถึงจังหวะ Panya จะปลุกเซสชันหลัก (game tester, skill
> `pf-attended-test`) มารันทั้งคิวรวดเดียว แล้วกรอกผลกลับให้ chief ประมวล
> — ธง PANYA_PRESENT ยกเลิกถาวร ข้อความ "รอธง/รอ Panya attend" เก่ากว่านี้ = ล้าสมัย

> 🔑 **วิธีขอสิทธิ์เกมที่ถูกต้อง (บทเรียนจริงจากเซสชันหลัก 03:31 vs 03:52 — อย่าคลำเอง):**
> `request_access(["GameClient.local.bin"])` ตอนเกม**ไม่ได้เปิด** → ระบบตอบ `notInstalled`
> **เงียบ ๆ ไม่มี dialog ขึ้นบนจอเลย** (เกมเป็น .bin ไม่อยู่ใน Start menu)
> ลำดับที่ถูก: ① เปิด server ผ่าน bridge ② เปิดเกมผ่าน bridge (ProcessStartInfo —
> สองขั้นนี้ไม่ต้องใช้สิทธิ์) ③ รอหน้าต่าง 'Pirate Force' โผล่ ④ **แล้วค่อย** เรียก
> `request_access(["GameClient.local.bin"])` → dialog จะขึ้นจริง → Panya กด Allow
> (พิสูจน์แล้ว 03:52: ขอตอนเกมเปิดอยู่ → granted tier full ทันที)

> 🔴 **กฎใหม่ที่ตามมาจากรอบ 17 — ทุกเกณฑ์ผ่านในคิวนี้ต้องระบุว่าตัวเองอยู่ชั้นไหน:**
> รอบ 11 วางกฎว่า "อย่านับ `count(*)` เปล่า ให้นับ `selected_character_id IS NOT NULL`"
> เพื่อกันแถวที่งอกจากการต่อ TCP เปล่า — **กฎนั้นยังถูกและยังจำเป็น แต่ไม่พออีกแล้ว**
> รอบ 17 พิสูจน์ว่า **สคริปต์ ~200 บรรทัดสร้างแถวที่ `selected_character_id IS NOT NULL`
> ได้ และแยกไม่ออกจากแถวของ client จริงในทุกคอลัมน์ที่เกณฑ์ดูอยู่**
> → DB พิสูจน์ได้แค่ว่า *มีบางอย่างพูดโปรโตคอลถูก* ไม่ได้พิสูจน์ว่า *เกมจริงทำงาน*
>
> | ชั้น | ตัวอย่างเกณฑ์ | ใครทำได้ |
> |---|---|---|
> | **wire/DB** | เฟรมที่ server ส่ง, label, `sessions`, `lease_generation`, integrity | 🟢 headless — **ไม่ต้องรอ Panya** |
> | **client-observable** | HP bar, minimap, ชื่อแมพ, ข้อความที่ *ตาเห็นในกล่องแชท*, การเรนเดอร์ | 🔴 **ต้องมี Panya เสมอ** (เช่น GT-006) |
>
> เวลาที่เขียนรายการใหม่ ให้แยกเกณฑ์เป็นสองหัวข้อนี้ และอย่าอ้างชั้นบนเป็นหลักฐานของชั้นล่าง

การประสานงาน (chief-continue อ่านตรงนี้):
- ทุกครั้งที่จบรอบ chief-continue ระบบจะส่ง notification ปลุกเซสชันหลักอัตโนมัติ
  (notifyOnCompletion เปิดแล้ว) — **แค่จบรอบให้เรียบร้อยก็คือการปลุกผู้เทสแล้ว**
  ⚠️ **แต่ notification จะมีผลก็ต่อเมื่อมีคนอ่าน** — ยืนยัน `notifyOnCompletion` จาก API ไม่ได้
  (ไม่มีในผลลัพธ์ของ `list_scheduled_tasks`) และ 24 รอบที่ผ่านมาอยู่ในช่วงตีห้าถึงเช้า
  → **ห้ามเขียนรายงานว่า "รอผู้เทส" เฉย ๆ อีก ให้เขียนตรง ๆ ว่า "รอ Panya มา attended session"**
- ถ้าต้องการเทส: เขียนรายการ PENDING ลงคิวนี้ให้ละเอียด แล้วจบรอบได้เลย
- ถ้ายังไม่ต้องการเทส: จบรอบตามปกติ ผู้เทสจะเห็นว่าคิวว่างและไม่ทำอะไร
- ผลเทสจะถูกกรอกกลับในคิวนี้ → รอบถัดไปของ chief เอาไปประมวล/commit ต่อ

รูปแบบรายการ:

```
## GT-NNN <ชื่อ>  [PENDING|RUNNING|PASS|FAIL|BLOCKED]
- objective: (claim เดียวที่เทสนี้พิสูจน์)
- db: (ไฟล์ DB ที่ใช้ — ค่าเริ่มต้น state\pirateforce.sqlite3)
- server args: (เช่น -SecondPasswordMode bypass)
- steps: (ทีละคลิก อ้างพิกัด/ภาพจาก playbook)
- pass criteria: (ต้องเห็นอะไรใน UI + server log + DB)
- nonclaims: (อะไรที่เทสนี้ไม่พิสูจน์)
- result: (game-tester กรอก: ผล + หลักฐาน + เวลา)
```

## PLAYBOOK — ขั้นตอน full-loop ที่พิสูจน์แล้ว (2026-08-17 04:17–04:24)

1. job เปิด server: copy แบบจาก `pf_bridge\done\014_fullloop_canonical.ps1`
   (Ctrl+C server เก่าก่อนถ้า port ไม่ว่าง) — server ต้องขึ้น listener 2 ตัวใน ~2 วิ
2. job เปิด client: แบบจาก `done\015_launch_client.ps1` (ProcessStartInfo เท่านั้น)
3. รอ ~30 วิ → หน้าเลือกเซิร์ฟเวอร์: คลิกปุ่มซ้ายล่างใต้ panel (ตำแหน่งสัมพัทธ์กับ
   หน้าต่าง — ยึดภาพ ไม่ยึดพิกัดตายตัว เพราะหน้าต่างย้ายได้)
4. dialog เตือน PVP → คลิกปุ่มซ้าย (ยืนยัน)
5. หน้าเลือกตัวละคร: เห็น Arena01 + nameboard → ตัวละครต้องถูกเลือกอยู่
   (มี panel ชื่อด้านบน) ถ้าไม่มี ให้คลิกที่ตัวโมเดลก่อน → คลิกปุ่ม **กลางสุด** จาก 5 ปุ่ม
   แถวล่าง = เข้าเกม (⚠️ แก้ 2026-08-18 จาก GT-010 zoom ยืนยัน: **ปุ่มแรกซ้ายสุด =
   ลบตัวละคร** · ปุ่มที่ 2 = สร้างตัวละคร — โน้ตเก่าที่ว่า "ปุ่ม 2 = ลบ" ผิด · กดลบเฉพาะ
   เทสที่สั่งเท่านั้น · X ที่หน้านี้ปิดหน้าต่างทันทีไม่มี dialog ยืนยัน)
6. loading (โปสเตอร์ WANTED) ~20-30 วิ → เข้าแมพ: ต้องเห็น HP bar, minimap,
   ชื่อแมพมุมขวาบน, chat "[ระบบ] : Pirate Force local server online"
7. ออก: คลิก X มุมขวาบนหน้าต่าง **ครั้งเดียว** → dialog ยืนยัน → คลิกปุ่มซ้าย (ยืนยัน)
8. job ปิด server + เก็บหลักฐาน: แบบจาก `done\016_stop_server_collect.ps1`

ข้อควรระวังที่เจอมาแล้ว:
- ถ้า StartGame แล้วเงียบ (ไม่ loading) = server ปฏิเสธเงียบ → อ่าน
  `server_console_live.out.txt` หา `StartGameReq` แล้วดูว่ามี response ไหม
  อย่าคลิกวนซ้ำ; client ที่ค้างสถานะนี้จะไม่รับ X/Alt+F4 ต้องให้ผู้ใช้ End task
- DB post-move (identity1 ที่ slot≠0) จะโดน guard ปฏิเสธ เว้นแต่เปิด scenario opt-in
- 🔴 **ห้ามใช้ `count(*) FROM sessions` เป็นเกณฑ์ผ่าน (พิสูจน์แล้วรอบ 11 ว่าเชื่อไม่ได้)**
  การต่อ TCP เข้าพอร์ต GAME `10189` **โดยไม่ส่งไบต์ใด ๆ เลย** ก็สร้างแถว `sessions`
  ผูกกับ `account_id=1` (`localtest`) ได้ 1 แถวต่อ 1 การเชื่อมต่อ และดัน `lease_generation`
  ขึ้น 1 (พอร์ต LOGIN `10188` ไม่สร้าง; การบูตเปล่าก็ไม่สร้าง)
  → แถวอาจงอกจากอะไรก็ได้ที่ไม่ใช่ client → เทสจะ **ผ่านด้วยเหตุผลผิด** หรือตกทั้งที่ไม่ผิด
  **ให้นับเฉพาะแถวที่เป็น client จริงเสมอ:**
  ```sql
  SELECT count(*) FROM sessions WHERE selected_character_id IS NOT NULL;
  ```
  และทุกเทสต้องบันทึก `SELECT max(lease_generation) FROM sessions;` ทั้งก่อนและหลัง
  ส่วนแถวที่ `selected_character_id IS NULL` ให้รายงานแยกเป็น "แถวจากการเชื่อมต่อเปล่า"
  **ไม่ถือเป็นความผิดพลาด** (รายละเอียด: `pf_bridge\FINDINGS_R11_ZEROBYTE_GAME_SESSION.md`)
- 🟢 **precondition ยืนยันแล้วที่ HEAD `eef51fa` (รอบ 11, job 033 — ไม่มี client):**
  server ขึ้น listener 2 ตัวใน **1 วินาที**, accept ได้จริงทั้งสองพอร์ต, Ctrl+C helper
  ปิดสะอาด **exit 0 ทั้ง server และ shim**, `[FOUNDATION] stopped` ×1, stderr **0 ไบต์**,
  listener เหลือ 0, `integrity_check=ok`, backpack `[1@0,2@1,4@3]` ไม่ขยับ
  → **ฝั่ง server ไม่มีอะไรบล็อกคิวนี้ ขาดแค่คนเปิดเกม**
- 🔴 **บังคับทุกเทสที่ใช้ `state\pirateforce.sqlite3`:** ขั้นแรกของ job ต้อง copy DB
  ไปเป็น `pf_bridge\backup\pirateforce_before_<GT-id>_<yyyyMMdd_HHmmss>.sqlite3`
  แล้ว **เทียบ sha256 กับต้นฉบับทันที ถ้าไม่ตรงให้หยุด**
  (รอบ 08:07 พบว่า DB ตัวนี้ **ไม่มีสำเนาสำรองเลย** และ **ไม่ได้อยู่ใน git**
  → commit/stash/checkout กู้มันไม่ได้ทางเดียวที่กันได้คือ copy ไฟล์
  ตอนนี้มีฐานอ้างอิงแล้วที่ `backup\pirateforce_canonical_20260817_080705.sqlite3`
  sha256 `673f4bfb…` — รายละเอียด + ค่าฐานทุกแถวอยู่ใน `backup\DB_CANONICAL_BASELINE.md`)

---

## PLAYBOOK เพิ่มเติม — บทเรียนจากรอบใหญ่ #7 (GT-022) · เขียนโดย chief รอบ 91 จากผลของผู้เทส

**การเดินตัวละคร (Panya สอนเอง ~18:5x — การคลิกพื้นเพื่อเดินถูกปิดไปแล้ว):**
`W/A/S/D` เดิน · `spacebar + WASD` กระโดด (ใช้ขึ้นจากน้ำได้) · ล้อเมาส์ซูม
🔴 **แกน a/d เปลี่ยนตามทิศที่หันทุกครั้ง** ⇒ **สูตรที่เวิร์ค:** กด W สั้น ๆ 0.3–0.4 วิ → อ่าน X/Y บน HUD
→ ได้ basis vector → แก้สมการ 2 ตัวแปรว่าจะกด s/a/d กี่วินาที · **ต้องวัดใหม่ทุกครั้งหลังหันตัวหรือ strafe**

### 🔴🔴 กฎกล้อง — **ฉบับแก้ R163 (2026-08-25 ~15:xx +07:00) · ฉบับก่อนหน้าทุกฉบับใช้ไม่ได้แล้ว**

**ที่มาของการแก้:** ผู้เทสแยกสองอย่างนี้ออกจากกันเองในรอบที่ 4 ของ GT-045 v3
(จดหมาย `notes_to_chief\consumed\20260825_1340_GT045-ANSWERED-*.md` §②) — ยกความมาตรง ๆ:
> *"ปุ่ม Q,E ไม่เหมือนกับคลิกขวาลาก · **คลิกขวาลากคือการหมุนมุมกล้องในเกมเฉย ๆ หมุนได้อิสระทุกทิศ
> ทิศการยืนของตัวละครไม่หมุนตาม ไม่มีอะไร trigger** · แต่ถ้ากด Q,E — ตัวละครหันหน้าไปตามกล้อง
> กล้องแพนตามไปด้วย ได้แค่ซ้าย/ขวา ตำแหน่งตัวละครไม่เคลื่อนที่ **และ trigger ด้วย"*

| ท่า | ทำอะไรจริง | ยิง `TargetPosVital` ไหม | ใช้ได้เมื่อไหร่ |
|---|---|---|---|
| **คลิกขวาค้างลากเมาส์** | หมุน **มุมกล้อง** อย่างเดียว · หมุนได้อิสระทุกทิศ · **ทิศหันของตัวละครไม่ขยับ** | 🟢 **ไม่ยิง** | ✅ **ปลอดภัย ใช้ได้เต็มที่ตลอดรอบ รวมถึงก่อนทริกเกอร์** |
| **`Q` / `E`** | **หันตัวละคร** แล้วกล้องแพนตาม (ซ้าย/ขวาเท่านั้น · ตำแหน่งไม่เคลื่อน) | 🔴 **ยิง** | ❌ **ห้ามแตะก่อนทริกเกอร์** |
| **`W/A/S/D`** | เดิน (เปลี่ยนทั้งตำแหน่งและทิศหัน) | 🔴 **ยิง** | ❌ **ห้ามแตะก่อนทริกเกอร์** |

🔴 **ประโยคเดียวที่ต้องจำ: ตัวที่ยิง `TargetPosVital` คือ "การเปลี่ยนทิศหันของตัวละคร" ไม่ใช่ "การขยับกล้อง"**

- 🆕 **R173 — พฤติกรรมที่เปลี่ยนจริงและยังไม่มีใครวัด: "การคลิกตัว NPC ตอนนี้ราคาเท่าเฟรมสำมะโน"**
  หลังต่อสาย `population_indices` ของ session = **ทั้ง 115 placement** ⇒ **คลิกซ้ายใส่ NPC ของสำมะโนตัวใดก็ได้** ทำให้เซิร์ฟเวอร์ตอบ `[G>] V98_NPC_FACE_PLAYER_POSITION_HEADING_P<idx>` ซึ่ง **ประกอบ population ทั้งชุดใหม่ทั้งก้อน** (`v141:1078-1093`) ⇒ **เฟรมขนาดระดับสำมะโน ~17.9 KB ต่อหนึ่งคลิก** แทน ~504 ไบต์แบบเดิม ตามด้วยใบเล็ก `V98_NPC_CONVERSATION_DEFAULT_P<idx>`
  - **ไม่มีใครวัดว่าไคลเอนต์ทำอะไรกับเฟรมนั้น** — **ใบนี้ไม่ได้เกิดมาเพื่อวัดมัน และห้ามใบนี้ตอบมัน**
  - **กติกาของรอบนี้: ห้ามคลิกซ้ายใส่ NPC โดยตั้งใจตลอดรอบ** (ใบนี้ไม่มีขั้นตอนไหนต้องคลิก NPC เลย)
  - **เผลอคลิก = ไม่ใช่รอบเสีย** ⇒ **จดเวลานาฬิกาจริง (+07:00) และ `t` ของวิดีโอ · คัด `[G>]` ทุกบรรทัดหลังจากนั้น · จดว่าจอมีอาการอะไรไหม** แล้วเขียนเป็น **ข้อสังเกตฟรี ไม่ใช่ผลของใบ**

🔴🔴 **ชั้นหลักฐานของกฎนี้ — อ่านก่อนพึ่งมัน (เพิ่มโดย chief R163 หลัง `pf-adversary` จับได้):**
คอลัมน์ "ยิง `TargetPosVital` ไหม" เป็น **คำถามชั้น wire** แต่คำตอบ 🟢 "ไม่ยิง" ของคลิกขวาลาก
มาจาก **คำให้การของผู้เทสหนึ่งรอบ** (จดหมาย `20260825_1340` §②) ซึ่งเป็น **ชั้น client-observable**
— **ผู้เทสไม่ได้ดูสาย เธออนุมานจากพฤติกรรมบนจอ (ตัวไม่หัน)**
· และหลักฐานชั้น wire ที่มีอยู่จริง (`20260825_0015:137`) บันทึกแค่ว่า *"หมุนกล้องอย่างเดียวแล้ว `TargetPosVital` ออก"*
  🔴 **โดยไม่ได้จดว่ารอบนั้นใช้อินพุตอะไรหมุน** — คำว่า `Q/E` ในใบนั้นเป็นการอนุมานของผู้ช่วย ("น่าจะ") ไม่ใช่ input log
  ⇒ **ถ้ารอบ 1104 เธอใช้คลิกขวาลาก กฎฉบับนี้ผิดทันที และ counter-evidence นั้นอยู่ในรีโปแล้ว**
· `evidence_screens\` มี control ของ `Q`/`E` ครบ (`CONTROL_camera_Q_120ms.png` · `GT045_camera_E_quicktap_restore.png`)
  🔴 **แต่ไม่มี control ของคลิกขวาลากแม้แต่ภาพเดียว — ไม่มีใครเคยวัดท่านี้เทียบสายสักครั้ง**
⇒ **ใช้กฎนี้ได้ แต่รอบ attended ถัดไปต้องรันด่านตัวควบคุมราคา ~30 วินาที** (ดูข้อ 3b ของ `GT-035`)
**จนกว่าด่านนั้นจะผ่าน กฎฉบับนี้เป็น "คำให้การ" ไม่ใช่ "การวัด"**

🔴 **ข้อความเก่าที่ถอนแล้ว — ห้ามอ้างอีก:**
- ~~"ห้ามหมุนกล้อง `Q`/`E` เพราะการหมุนกล้องยิง `TargetPosVital`"~~ — **ผลถูกโดยบังเอิญ แต่เหตุผลผิด**
  และเหตุผลที่ผิดทำให้ผู้เทสถูกห้ามใช้กล้องทั้งที่ใช้ได้
- ~~"คลิกขวาค้างลากเมาส์หมุน 360° **แต่เครื่องมือของผู้เทสลากได้แค่ปุ่มซ้าย ⇒ ใช้ได้แค่ `Q/E`**"~~
  — ข้อจำกัดนั้นเป็นของ **เครื่องมือคลิกสังเคราะห์** ไม่ใช่ของ **คนที่นั่งขับ UI เอง**
  🔴 **และมันคือบรรทัดที่ผลักผู้เทสไปหา `Q/E` ซึ่งเป็นตัวยิงทริกเกอร์พอดี**
  ⇒ **ผู้เทสที่เป็นคน ใช้คลิกขวาลากได้เสมอ** · ถ้ารอบไหนขับด้วยเครื่องมือ ให้เขียนกำกับในใบว่ารอบนั้นไม่มีคลิกขวา

⚠️ **เรื่อง "ราคาที่จ่ายไปแล้ว" — ฉบับที่ถูกต้อง (แก้โดย chief R163 หลัง `pf-adversary` จับได้):**
ฉบับแรกเขียนว่า *"GT-045 ตอบไม่ได้สามรอบติดเพราะกฎนี้"* — **ยกมาจากจดหมาย `1340` §② โดยไม่ตรวจ**
🔴 **จดหมายฉบับเดียวกันนั้นค้านตัวเองที่ §④.3** และจดหมายผลทั้งสามใบระบุสาเหตุคนละอย่าง:

| จดหมาย | สาเหตุที่ "หาเฟรมไม่เจอ" ที่ใบนั้นระบุเอง |
|---|---|
| `20260825_1235` §③ | ค้นวิดีโอ 4 ช่วงไม่เจอ · `t 619.0–663.6` **เฟรมนิ่ง 44 วิ** เพราะเกมไม่ได้โฟกัส |
| `20260825_1300` ①② | **`PF_Git_Sync` แย่งโฟกัสทุก 2 นาที ⇒ "บันทึกไม่ติดโดยโครงสร้าง"** · และ **ท่าเดินออกเร็ว ⇒ ของอยู่หลังกล้องที่กำลังวิ่งออก** |
| `20260825_1340` §④.3 | **contact sheet ถูกย่อเหลือ 400px ⇒ ป้ายเหลือจุดเดียว** |

⇒ **มีสาเหตุแข่งกันอย่างน้อยสามอัน และกฎกล้องไม่ใช่อันที่จดหมายผลระบุเป็นสาเหตุหลักสักใบ**
🔴 **หลักฐานเชิงวัตถุที่ค้านฉบับแรกแรงที่สุด:** ชุด `GT045v3r3_1132_FULLRES_*` (รอบ 3) **เห็นพื้นโล่งกว้าง ตัวละครไม่บังอะไรเลย**
— ถ้ารอบ 3 "ตัวละครยืนบังจุดตก" เฟรมชุดนั้นเกิดไม่ได้
⇒ **สิ่งที่พูดได้จริง:** กฎที่ผิดเหตุ **เป็นหนึ่งในอุปสรรค** และมันกันผู้เทสออกจากท่าที่ปลอดภัยจริง
**แต่ห้ามอ้างว่ามันเป็นสาเหตุเดี่ยว** · 🔴 **และห้ามให้การแก้กฎนี้มาแทนการแก้ `PF_Git_Sync`** ซึ่งเป็นสาเหตุที่จดหมายระบุตรงที่สุด
⇒ **นี่คือเหตุผลที่กฎที่ "ถูกผลแต่ผิดเหตุ" อันตรายพอ ๆ กับกฎที่ผิดผล** — และเป็นเหตุผลที่ chief ไม่ควรยกประโยคเดียวจากจดหมายมาเป็นข้อสรุป

**liveness check (NO-CRASH):** ใบเก่าหลายใบเขียนว่า *"ขยับกล้อง `Q/E` ได้ = NO-CRASH"*
⇒ 🔴 **เปลี่ยนเป็น "คลิกขวาลากแล้วกล้องหมุน = NO-CRASH"** — เช็คได้เหมือนกันแต่ **ไม่ยิงอะไรออกสาย**

### 🔴🔴 กฎยืนสองข้อ — เพิ่มโดย chief R164 (2026-08-25 ~16:0x +07:00) · **บังคับกับทุกใบ attended หลังจากนี้**

**ที่มา (ราคาที่จ่ายไปแล้ว):** จดหมาย `20260825_1550` §⑤ ข้อ 1-2 — **ทั้งสองข้อผู้สังเกต (คุณ Panya) เป็นคนจับได้ ไม่ใช่ผู้ช่วย**

**กฎ Z — ใบที่วางเป้าไว้ใกล้ผู้เล่น ต้องมีขั้น "ซูมออกให้สุดก่อนยิงทริกเกอร์" เขียนเป็นขั้นบังคับในใบ**
- 🔴 **เกณฑ์ที่ใช้จริงคือ "หัวเป้าอยู่ในเฟรมไหม" ไม่ใช่ระยะทางเป็นตัวเลข** — ขนาดที่เห็นบนจอเป็นผลของ **ขนาดโมเดล × ระยะ × มุมกล้อง** ไม่ใช่ระยะอย่างเดียว · *(ฉบับแรกของกฎนี้เขียน "~300 หน่วย" ไว้ — `pf-adversary` จับได้ว่า **ไม่มีที่มา ไม่มีนิยาม และเป็นตัวแปรผิด** ⇒ chief ถอนตัวเลขทิ้งก่อน commit · เลนที่วัดมาจริงคือ `dx100/dy50` ≈ 111 หน่วย และมันเต็มจอ)*
- ใบใดที่วางเป้าแบบ `player_relative` **หรือ** ที่ผู้เทสเห็นว่าเป้ากินพื้นที่จอมากจนหัวอาจหลุดเฟรม **ต้องมีขั้นที่เขียนว่า "หมุนล้อเมาส์ซูมกล้องออกให้สุด ก่อนยิงทริกเกอร์" เป็นขั้นที่มีหมายเลขของตัวเอง** — **ไม่ใช่หมายเหตุ ไม่ใช่คำแนะนำ** · ใบที่ไม่มีขั้นนี้ = **ใบบกพร่อง** ผู้เทสเติมขั้นนี้เองได้ทันทีและจดลงในผลว่าเติม
- เกณฑ์ที่ต้องเห็นก่อนเดินต่อ: **หัวของเป้าต้องอยู่ในเฟรม** — เลขดาเมจและ `MISS` เรนเดอร์ **เหนือหัว** ⇒ กล้องที่ซูมใกล้จนตัวเป้าเต็มจอ **ทำให้หลักฐานทั้งสองชนิดหายไปทั้งหมดโดยที่จอยังดูปกติ**
- 🔴 **ถ้ารอบใดจบโดยหัวเป้าไม่เคยอยู่ในเฟรม ผลต้องเขียนตรง ๆ ว่า "เลขดาเมจ/`MISS` = non-observed เพราะกล้องไม่ครอบหัวเป้า" ห้ามเว้นช่องนั้นเงียบ ๆ** — ในรอบที่ 1 ของ `GT-035` เลขดาเมจสองตัวและ `MISS` ทุกครั้งหายไปทั้งหมด **และการหายนั้นไม่ได้ถูกรายงานว่าเป็นช่องว่างด้วยซ้ำ**
- **จดทุกครั้งที่ซูม** (เวลาเทียบนาฬิกาบนจอ) ด้วยวินัยเดียวกับที่บังคับให้จดการส่องกล้อง
- 🔴🔴 **nonclaim ที่ต้องอ่านก่อนใช้กฎนี้ — สองชั้นที่ยังไม่ได้วัด ซ้อนกันอยู่:**
  ① **ไม่มีใครวัดว่าล้อเมาส์ยิง `TargetPosVital` หรือไม่** แม้แต่ครั้งเดียว
  ② **ชั้นที่จะเอาไปเทียบก็ยังไม่ได้วัด** — กฎกล้องฉบับ R163 ยืนบน *คำให้การของผู้เทสหนึ่งรอบ* และไม่มี control ของคลิกขวาลากแม้แต่ภาพเดียว (ด่าน 3b ยังไม่ผ่าน)
  ⇒ 🔴 **ห้ามเขียนว่า "ล้อเมาส์ปลอดภัยเพราะมันเหมือนคลิกขวาลาก"** — ของที่ไม่ได้วัดสองอันตรงกัน ไม่ใช่หลักฐาน
  ⇒ **สิ่งที่กฎนี้อนุญาตจริงคือ: ซูมได้ แต่ต้องจดเวลาที่ซูมทุกครั้ง** เพื่อให้รอบหลังแยกออกว่าเฟรมที่โผล่มาจากอะไร
  ⇒ **ความเสี่ยงที่ยอมรับไว้ตรง ๆ:** ถ้าล้อเมาส์ยิง `TargetPosVital` จริง มันจะกิน one-shot ก่อนผู้เทสพิมพ์ **และจะกินพร้อมกันทุกใบ** เพราะกฎนี้สั่งให้ซูมก่อนทริกเกอร์ ⇒ **ด่าน 3b จึงเป็นหนี้ที่ต้องใช้คืนก่อนใบถัดไป ไม่ใช่ทีหลัง**

**กฎ S — แหล่งที่ไม่ครบ ห้ามอ่านเป็นแหล่งที่ครบ (ขยายด่าน `G1` ลงมาถึงรอบ attended)**
- ก่อนสร้างข้ออ้างใด ๆ บนไฟล์/ล็อก **ต้องพิสูจน์ความครบของแหล่งก่อน แล้วเขียนหลักฐานความครบลงในผล**: จำนวนบรรทัด/ไบต์ที่มีจริง · จำนวนที่คาด · ไฟล์นั้นเป็น live tail / ถูกหมุน / ถูกตัดท้ายหรือไม่ · **แหล่งที่สองที่อิสระคืออะไร**
- 🔴 **ข้ออ้างเรื่องจังหวะการกระทำของคน** ("คลิกช้าไป 1 วินาที" · "ไม่ได้กด" · "กดผิดลำดับ") **ห้ามออกจากล็อกเลย** — ตัดสินได้จาก **วิดีโอต่อเนื่องที่มีนาฬิกาบนจอ** เท่านั้น
- **ตัวอย่างที่เกิดจริงและต้องถือเป็นชนิดของกับดัก:** รอบที่ 1 ของ `GT-035` — `GAME_EVENTS_LIVE.txt` มีอยู่ **5 บรรทัด** ถูกอ่านเป็นบันทึกครบถ้วน ⇒ ได้ข้ออ้างเท็จว่าผู้สังเกตคลิกเป้าช้าไปหนึ่งวินาที
  🔴🔴 **และคำแก้ก็ผิดกฎข้อนี้เหมือนกัน — chief เขียนมันผิดเองในฉบับแรก `pf-adversary` จับได้:** ประโยค "คลิกทันทีหลังพิมพ์" **ก็เป็นข้ออ้างเรื่องจังหวะการกระทำของคน** และ **ไม่มีใครยกเวลาจากวิดีโอมาค้ำมัน** · ยิ่งกว่านั้นภาพในรีโปเอง (`evidence_screens/GT035_1138_HPPANEL_432-476s.jpg`) ไม่มีแผง target ตั้งแต่ `t432` ถึง `t458` ซึ่ง **อาจ** ขัดกับมัน (หรืออาจเป็นการ deselect/reselect — ไม่มีใครรู้)
  ⇒ **สถานะที่ถูกต้องของทั้งสองประโยค: `[ตัดสินไม่ได้]` จนกว่าจะมีใครยกเวลาจากวิดีโอที่มีนาฬิกาบนจอมาวาง** · สิ่งเดียวที่ยืนได้ตอนนี้คือ **`TargetVital` ที่ล็อก 5 บรรทัดจับได้ ไม่พอจะตัดสินอะไรเลย** · 🔴 **กฎนี้เกิดมาพร้อมรอยแผลของตัวเอง ปล่อยไว้ให้เห็นโดยตั้งใจ**
- **ถ้าพิสูจน์ความครบไม่ได้** ให้เขียนว่า **"แหล่งไม่ครบ ⇒ ตัดสินไม่ได้"** แล้วจบ — **ห้ามแปลงเป็นข้อสรุป** (นี่คือด่าน `G1` ตัวเดิม: ห้ามอ้าง "ไม่มี / ไม่ได้ทำ / ช้าไป" จากแหล่งเดียวที่ไม่ได้พิสูจน์ว่าครบ · `RULES_ASSISTANT_GATES_G1G8_20260824.md`)

**หาพิกัด NPC โดยไม่ต้องเดินสุ่ม:** เฟรม `SPAWN` มี float 3 ตัวท้าย `MovementAttr` = X/Y/Z ตรง ๆ
(ตัวอย่างจริง `2A D4CF0EC6 / 2A B9C02DC5 / 2A C74A5F43` → X `-9139.96` Y `-2780.05` Z `223.29`)

**เครื่องมือ/จ็อบ — สี่ข้อนี้ทำให้รอบ #3 เสียเวลาไปเยอะ:**
1. 🔴 **จ็อบที่เปิด GameClient แบบ redirect stdout/stderr จะบล็อก bridge จนหน้าต่างเกมปิด**
   ⇒ จ็อบที่เขียนมาเพื่อไปฆ่า client ที่ค้าง **รันไม่ได้ เพราะถูกบล็อกโดย client ตัวนั้นเอง**
   **ให้เปิด client โดยไม่ redirect หรือแยกเป็นจ็อบ launch ที่ปล่อยลูกแล้วจบทันที**
2. 🔴 **`Get-Process` ครั้งเดียวไม่ใช่หลักฐานว่าไม่มีอะไรค้าง** — จ็อบ 907 เช็คว่า process client หายแล้วจึงเปิดตัวใหม่
   แต่สิ่งที่ต้องเช็คจริงคือ **เซิร์ฟเวอร์ปล่อย session แล้วหรือยัง** (server เป็น serial ตาม R18 ⇒ รายที่สองค้าง "กำลังเชื่อมต่อ...")
   **กฎ: ถ้า client เก่าไม่ได้ปิดแบบสวย ๆ (ไม่ได้กด "ออก" จนถึงหน้า server select) → รีบูตเซิร์ฟเวอร์เสมอ**
3. **จ็อบเดียวไม่ควรทำทั้ง "ปิด" และ "เปิด"** — ถ้าขั้นปิดสรุปผิด ขั้นเปิดจะเดินหน้าต่ออย่างมีความสุข
4. **one-shot ผูกกับ connection ไม่ใช่ process ของเซิร์ฟ** (`self.runtimeres_death_sweep_count`)
   ⇒ ปิด client สวย ๆ แล้วเปิดใหม่ = รีอาร์ม sweep ได้โดยไม่ต้องรีบูตเซิร์ฟ
5. **boot job ควรอ่าน expected sha จาก `CANON_SHA.txt` เสมอ** ไม่ฝังค่าตาย (job 905 ทำแบบนี้)
6. 🔴 **`py -3 -m pirateforce_foundation.app --help` คืน 0 บรรทัด (exit 0) ผ่านสะพาน**
   **ห้ามใช้ `--help` ตรวจว่ามี flag ไหม — ให้ `git grep` ที่ source แทน**
7. **`computer_batch` ที่มี `hold_key`/`key` มักโดน `focus anomaly`** — แยกเป็น call เดี่ยว (`left_click` ก่อน แล้วค่อย `hold_key`) เสถียรกว่า
8. ✏️ **[แก้แล้ว รอบ 92 — ข้อความเดิมอ่านหลักฐานผิด]** เดิมเขียนว่า *"ปุ่ม X / ปุ่ม 'ออก' ไม่รับคลิกสังเคราะห์"*
   🔴 **ผิด — LOCALTEST-001 (2026-08-19 23:06) พิสูจน์แล้วว่ามันรับคลิกสังเคราะห์ปกติ กดครั้งเดียวปิดได้**
   **สาเหตุจริงคือหน้าต่างแอป Claude ทับ title bar ฝั่งขวาของเกม ตรงที่ปุ่ม X อยู่พอดี**
   และเซสชันฝั่ง cloud **มองไม่เห็นหน้าต่างตัวเองใน screenshot** จึงไม่มีทางรู้ว่าโดนบัง
   ⇒ **ท่าที่ถูก:** ผู้เทส local เห็นหน้าต่างตัวเองในภาพ ⇒ **ตรวจว่าโดนบังไหมก่อนคลิกทุกครั้ง**
   ถ้าโดนบัง ให้ `left_click_drag` ลากหน้าต่างเกมออกมาก่อน แล้วค่อยกด X (จ็อบ 916 เป็นใบเสร็จ: `pid does not exist`)
   ⚠️ **ยังไม่พิสูจน์:** ปุ่ม X ตอนอยู่ **ในแมพ** (มี dialog ยืนยัน) และ **ปุ่ม logout ในเกม** — สองอย่างนี้ยังไม่เคยเทสจากฝั่ง local
8b. 🔴 **วิธีเปิด client ที่ถูกต้อง = `Invoke-CimMethod Win32_Process Create`** (บทเรียน LOCALTEST-001)
   · `Start-Process 'xxx.bin'` **ที่ไม่มี** `-Redirect*` = ShellExecute → **ล้มเงียบ** `-PassThru` คืน `$null` (จ็อบ 912)
   · `-RedirectStandardOutput` ใน boot job ตระกูล 072/087/090/097 **ไม่ได้ใส่ไว้เพื่อเก็บ log อย่างเดียว** —
     มันคือสิ่งที่บังคับ `UseShellExecute=false` ให้ `.bin` รันได้ **ใครลบออกเพื่อเลี่ยงการบล็อก จะได้จ็อบที่ไม่เปิดอะไรเลยและไม่ error**
   · `Win32_Process.Create` ได้ทั้งสองอย่าง: client เปิดจริง **และ bridge กลับ idle ทันที** (จ็อบ 913/915 เป็นใบเสร็จ)
9. **run DB เป็นสำเนาใหม่ทุกครั้งที่บูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกรอบ** เผื่อเวลาเดินไว้ในแผน
10. 🆕🔴 **รอบเทสที่จบเพราะคนเลิกเล่น ไม่ใช่เพราะเทสจบ ก็ยังต้อง teardown** (คำสั่ง Panya 1440 ข้อ B ·
   บทเรียนรอบใหญ่ #10: บูต 11:37 แล้วเลิกกลางคัน ไม่มี teardown · LOCK_GAME ค้าง HELD ~3 ชม.
   ไม่มีใครตรวจ canonical guard เลยทั้งรอบ) — สองข้อย่อยที่ต้องรู้:
   - ⚠️ **teardown template ปฏิเสธรอบที่ถูกทิ้ง >420 นาที โดยดีไซน์** (เดิม 180 — ยกเป็น 420 เมื่อ 2026-08-20 ·
     `TEMPLATE_teardown_generic.ps1:135` · แก้ stale โดย chief R119) (stamp age guard → exit 12 —
     จ็อบ 0947 เป็นใบเสร็จจริง) ⇒ แท่นที่ถูกทิ้งข้ามคืน/ข้ามชั่วโมง **อย่าฝืน template** ให้ใช้
     `staged\TOOL_stop_stale_server.ps1` (ทางกู้ที่ออกแบบมาเพื่อกรณีนี้ ไม่อ่าน info file) แล้วตามด้วย
     receipt อ่านอย่างเดียว `staged\0949_gt027_stalepad_canonical_guard.ps1` (แบบร่างพร้อมใช้ รอบ 105)
   - 💡 การ์ดเชิงระบบ (เริ่มรอบ 105): **chief ทุกรอบ scheduled ถ้าเห็น `LOCK_GAME` HELD และ heartbeat
     เก่ากว่า ~30 นาที ให้รายงานธงค้างในจดหมายถึงเซสชันหลัก** — รายงานอย่างเดียว ห้ามเก็บกวาดเอง
11. 🆕🔴 **ห้ามยืดระยะเฟรมของ scenario เพื่อให้ผู้เทสถ่ายทัน — ให้ถ่ายวิดีโอแทน**
   (คำสั่งเชิงวิธีการจาก Panya 2026-08-20 ~15:1x · ผู้เทสรับแล้วและยอมรับว่าเหตุผลของท่านถูก)
   - **เหตุผล:** ตัวเหตุการณ์บนจอ**เองสั้น** ไม่ใช่ว่าเฟรมถี่เกินไป ⇒ ยืด spacing ไปก็ไม่ได้อะไรเพิ่ม
     เสียเวลารอบเทสเปล่า และเพิ่มโอกาสที่รอบจะถูกทิ้งกลางคัน (ดูข้อ 10)
   - **ทางแก้ที่พิสูจน์แล้วสองรอบ:** ถ่ายวิดีโอ — ได้ทั้งภาพคมทุกเฟรม **และนาฬิกาที่ไม่ใช่ของผู้เทสเอง**
     (แก้ปัญหา Nyquist โดยไม่ต้องแตะ scenario สักไบต์ · GT-027 rerun คือใบเสร็จ: วิดีโอ 58 วิ เห็นครบ)
   - ⇒ **ข้อเสนอ "ทำ profile 15–20 วิ/เฟรมเพื่อผู้เทส" ที่ chief เคยส่งไป = ถอนแล้ว ห้ามหยิบกลับมา**
     GT-030 / GT-031 ที่ยังเขียนว่า 15 วิ/เฟรม **คงค่าเดิมไว้ตามที่ commit ไปแล้ว** (ไม่ใช่ profile ยืดเวลา
     มันคือค่าที่ scenario ถูก commit มาแต่แรก) — ห้ามสร้าง profile ใหม่ที่ยืดกว่านี้
12. 🆕⚠️ **ลูกศรเหลืองสองอันเหนือหัว NPC = เครื่องหมาย "เป้าหมายที่ถูกเลือก" ไม่ใช่เอฟเฟกต์ของ hit**
   (มันอยู่ตรงนั้นตั้งแต่ก่อนยิงแล้ว — เห็นชัดในเฟรม t=18 วิ ของวิดีโอ GT-027 rerun)
   ⇒ ห้ามใครอ่านลูกศรนี้เป็นหลักฐานว่าดาเมจถึงเป้า

13. 🆕⭐ **ทุกใบ attended ต่อจากนี้ ต้องบันทึกสีของทุกป้ายชื่อที่เห็นในเฟรม เป็นข้อมูลประจำ ไม่ใช่เฉพาะตอนสงสัย**
   (คำสั่งคุณ Panya 2026-08-25 ~14:2x +07:00 · `notes_to_chief\consumed\20260825_1425_PANYA-PROMOTION-CRITERIA-*.md` §"ผลพลอยได้":
   สีของชื่อคือตัวชี้วัดที่อ่านได้ฟรีทุกรอบว่า **ฟิลด์ไหนที่เรายังไม่เคยเติม** — เราได้เครื่องมือวัดใหม่มาโดยไม่ต้องเขียนโค้ดอะไรเลย)
   - **จดอะไร:** ชื่อตัวเอง (เหนือหัว + แผง UI ซ้ายบน) · ชื่อ actor ทุกตัวในเฟรม · ชื่อบนแผง target · ชื่อไอเทมบนพื้น ·
     บรรทัด title/คำอธิบาย · ชื่อผู้เล่นคนอื่น — **หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** · ไม่มีให้เขียน "ไม่มี" 🔴 **ห้ามเว้นว่าง**
   - **จดที่ไหน:** (ก) ในช่อง `result` ของใบนั้นเสมอ พร้อม path ภาพ + sha256
     (ข) เติม **`REAL_SERVER_DIVERGENCE.tsv`** หนึ่งแถวต่อหนึ่งป้ายที่เทียบ
     🔴 **เติมทุกกรณี ไม่ใช่เฉพาะตอนต่าง** — ใช้คอลัมน์ `compared_and_matched` = `yes` / `no` / `no-reference`
     (`evidence_layer=eye` · `evidence_in_repo` ตามจริง · `evidence_sha256` บังคับเมื่อ `=yes` · `open_ticket=RE-067` · `blocks_promotion=no`)
     **เหตุผลที่ต้องเติมแม้ตรง:** ถ้าทะเบียนเก็บเฉพาะความต่าง **เลนที่เทียบแล้วตรง จะแยกไม่ออกจากเลนที่ไม่เคยเทียบ**
     ⇒ ทะเบียนจะตอบข้อ (a) และ (c) ของ P6 ไม่ได้เลย และตัวเลข "เราห่างกี่เรื่อง" จะไม่มีตัวหาร
   - **อ่านสีจากภาพนิ่งความละเอียดเต็มเท่านั้น** 🔴 **ห้ามอ่านจาก contact sheet หรือภาพที่ย่อแล้ว ห้ามอ่านจากวิดีโอ**
     (บทเรียน GT-045: ย่อเหลือ 400px ป้ายชื่อเหลือจุดเดียว หาเฟรมไม่เจอสามรอบ · การบีบอัดวิดีโอเปลี่ยนสีได้)
   - 🔴 **ห้ามสรุปสาเหตุจากสี** — ไม่มีใครรู้ว่าอะไรตัดสินสี (`RE-067` เป็นใบที่จะตอบ) · ผู้เทส **จดสีที่เห็น** เท่านั้น
     ห้ามเขียนว่า "แปลว่าไคลเอนต์จัดมันเป็นผู้เล่น/NPC/ศัตรู" · ห้ามใช้สีเปลี่ยนคำตอบของคำถามหลักของใบ
   - **ข้อนี้เป็นชั้น client-observable ล้วน** — สีตอบชั้น wire/DB ไม่ได้ และชั้น wire ตอบแทนไม่ได้
     · **สีอ่านด้วยตา ไม่ได้วัดค่าพิกเซล** · **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับอาจเป็น client คนละ build/ภูมิภาค**
     ⇒ nonclaim สองข้อนี้ติดไปกับทุกใบที่ใช้กฎนี้

14. 🆕🔴🔴 **กฎ CLAPPER — จุดจูนนาฬิกาของรอบ · 🔴 ฉบับ R166-b: เป็น "อนุญาตเมื่อพิสูจน์ว่าปลอดภัย" ไม่ใช่ "บังคับทุกใบ"**
   *(เพิ่มโดย chief R166 · 2026-08-25 ~17:5x (+07:00) · **แก้ทั้งข้อในรอบเดียวกันหลัง `pf-adversary` หักล้างฉบับแรกได้สามทาง — อ่านบล็อก 🔴 ข้อจำกัด ให้จบก่อนใช้**)*
   *(ที่มา: จดหมาย `20260825_1730` §④ + `20260825_1745` §④ — หน้าสะพานวัดพบเอง แล้วถอน claim ของตัวเองก่อนที่มันจะเข้าใบ)*

   **ปัญหาที่กฎนี้พยายามแก้:**
   `VIDEO START start=` ในทุกใบจดเวลาที่เรา **สั่ง** `ffmpeg` **ไม่ใช่เวลาที่เฟรมแรกถูกจับจริง**
   ⇒ ทุกตัวเลขในโปรเจกต์ที่แปลง **"เวลาบนสาย ↔ เวลาในวิดีโอ"** มี error ที่ยังไม่เคยมีใครวัด

   🔴 **ขนาดของ error: ไม่ทราบ · และหลักฐานที่มีชี้ว่ามันไม่คงที่ แต่ *ยังแยกไม่ออกจากตัวแปรอื่น***
   สามรอบของคืน 2026-08-25 ให้ระยะ "กล่องเมนูหายบนจอ ↔ เซิร์ฟเวอร์รับ request บนสาย" = **~0 s** (1145) · **0.58 s** (1148) · **1.82 s** (1151)
   🔴 **แต่ค่านั้นคือ `d (offset นาฬิกา)` + `เวลาที่ไคลเอนต์ใช้ตั้งแต่คลิกจนไบต์ถึงเซิร์ฟเวอร์` + `ความหยาบของการสุ่มเฟรม 2 fps (±0.25 วิ)` รวมกัน**
   และ nonclaim ⑤ ของจดหมาย B บอกเองว่ากล่องน่าจะปิดโดย handler ของปุ่ม **ไม่ใช่เพราะเซิร์ฟเวอร์** ⇒ สองเหตุการณ์นี้ **ไม่ใช่เหตุการณ์เดียวกันคนละนาฬิกา** ซึ่งเป็นเงื่อนไขจำเป็นของการวัด offset
   ⇒ 🔴 **ห้ามเขียนว่า "วัดแล้วว่า offset ต่างกันทุกบูต"** — หน้าสะพานเองก็ไม่ claim (*"confound มีขนาดเท่ากับผลพอดี"*) · ฉบับแรกของข้อนี้เลื่อนขั้นมันเป็น [MEASURED] **ซึ่งผิด และถูกถอนแล้ว**
   ⇒ **สิ่งที่ยืนได้จริงคือ: ไม่มีใครรู้ขนาด error นี้ และไม่มีเหตุผลให้เชื่อว่ามันคงที่**

   ### 🔴🔴 ข้อจำกัดสามข้อที่ต้องอ่านก่อนใส่ clapper ลงใบใด ๆ

   **① 🔴🔴 "แชต ASCII 12 ตัว" คือ *predicate ของทริกเกอร์* ทั้งโปรเจกต์ ไม่ใช่ป้ายเวลา**
   classifier `classify_chat_input_attempt` ยิงที่ **12 ตัวอักษร printable ASCII พอดี ตัวไหนก็ได้ ไม่ผูกกับเนื้อสตริง**
   ⇒ `CLAPPER00001` = 12 ตัวพอดี ⇒ **มันคือทริกเกอร์**
   เลนที่ยิงด้วย ascii12 มีอย่างน้อย: `GT-033 variant C` · `HYP-PF-038` · learn-skill · `skillattr001` · `greenline001` (GT-063/HYP-PF-037) · **และบูตรวมสามเลนที่ merge เข้า `main` แล้ว (`3f87fc3`)**
   🔴 **การ์ดต้องอยู่ที่ชั้น *บูต* ไม่ใช่ชั้น *เขียนใบ*** — เลนที่ติดอาวุธถูกเลือกตอนบูต (composable lane sets) ⇒ ใบที่ตรวจแล้วว่า "เลนตัวเองไม่ใช้แชต" **ยังพังได้จากเลนร่วมบูต**
   ⇒ **กติกา: clapper เป็น opt-in · ห้ามใส่โดยปริยาย · ใส่ได้ต่อเมื่อผู้เขียนใบ *ระบุชุดเลนของบูตนั้นทั้งชุด* แล้วยืนยันว่า *ไม่มีเลนไหนในชุดยิงด้วย ascii12*
   ถ้าตอบไม่ได้แม้แต่เลนเดียว ⇒ **ไม่ใส่**
   🔴 **ของแถมชั้นเดียวกัน:** ตัวอักษรที่พิมพ์ตอนช่องแชต **ไม่โฟกัส** = hotkey · มี toggle `[localplayer+0x420]` (input command `0x27`) ที่ **ปิดเลขดาเมจทั้งจอเงียบ ๆ โดย wire เหมือนเดิมทุกไบต์** ⇒ การบังคับพิมพ์ 12 ตัวเป็นขั้นแรกของทุกรอบ = เอาความเสี่ยง "ตาบอดสองรอบ" ที่เคยกินเวลาโปรเจกต์ไปแล้ว มาวางไว้หน้าประตูทุกใบ

   **② 🔴 ต้องระบุ *เฟรมไหน* ให้ชัด มิฉะนั้นกฎจะให้ค่าที่แย่กว่าไม่จูนเลย**
   หลักฐานที่ commit แล้วบอกว่าตัวอักษรโผล่บนจอ **ระหว่างพิมพ์ ไม่ใช่ตอนส่ง**
   (`20260824_1037` §: *"พิมพ์ `PFCHATPROBE1`, เห็นครบ 12 ตัวใน S0 แล้วกด Enter ครั้งเดียว. ช่อง input เคลียร์ทันที"* · `20260821_0900` ยืนยันท่าเดียวกัน)
   ⇒ ถ้าใช้ **เฟรมที่ตัวอักษรตัวแรกโผล่** แล้วผู้เทสพิมพ์ช้า 4 วินาที **offset ที่ได้จะผิดไป 4 วินาที และมันจะถูกเขียนว่า [MEASURED] เพราะมีขั้นตอนในใบรองรับ**
   ⇒ 🔴 **สมอที่ต้องใช้คือ "เฟรมที่ช่อง input เคลียร์"** — เป็นเหตุการณ์บนจอที่ใกล้ Enter จริงที่สุด · **ห้ามใช้เฟรมที่ตัวอักษรโผล่**

   **③ 🔴 ยังไม่มีใครพิสูจน์ว่ามีเหตุการณ์บนจอให้จับหลัง Enter เลย**
   ค้นทั้ง repo แล้ว **ไม่เจอรอบไหนที่บันทึกว่าเห็นบรรทัดแชตที่ตัวเองพิมพ์ปรากฏในหน้าต่างแชต** · ที่เจอคือตรงข้าม —
   `20260825_1745` §④ อ่านภาพที่ `t=224.0` แล้วเห็น *"ช่องแชตมีแค่บรรทัดระบบ"*
   ⇒ **ถ้าไคลเอนต์ไม่ echo เอง และเซิร์ฟเวอร์เราไม่ broadcast กลับ clapper ก็ให้ค่าไม่ได้เลย**
   ⇒ **ใบแรกที่ใส่ clapper ต้องถือว่าตัวเองกำลัง *ทดสอบว่า clapper ทำงานไหม* ไม่ใช่ *ใช้ clapper*** และต้องเขียนผลข้อนี้กลับมา

   ### ขั้นที่ใส่ (เมื่อผ่านข้อจำกัดทั้งสามแล้ว · ราคา ~5 วินาที · ไม่ต้องแตะโค้ด)
   > เข้าแมพแล้ว **พิมพ์แชต ASCII 12 ตัวหนึ่งครั้ง ก่อนทำอะไรอย่างอื่น** ·
   > จด **เฟรมที่ช่อง input เคลียร์** (ไม่ใช่เฟรมที่ตัวอักษรโผล่) ↔ จับคู่กับบรรทัด `RECV ... 0xAC52` ⇒ **offset ของบูตนั้น**

   - **vital id ของแชต = `0xAC52` (44114) = `Channel_LocalTalkMessageVital`**
     🔴 **provenance ที่ตรวจได้จาก repo โดยไม่ต้องพึ่งไฟล์บนสะพาน:** `GAME_TEST_QUEUE.md` (แถวทะเบียน `0xAC52`) · `FINDINGS_R134_EXTERNAL_XCHECK.md` (ชื่อเดียวกัน) · `GT-055` PASS/DONE (พินโครงสร้าง: tag `0x48` + UTF-16LE) · และรอบที่วัดจริงว่าเฟรมแชตถึงเซิร์ฟเวอร์เป็น `0xAC52` 46 ไบต์
   - **ท่าพิมพ์แชตพิสูจน์แล้วว่าผู้เทสทำได้แน่** (GT-032 / GT-035 ใช้ท่านี้มาแล้ว)
   - 🔴 **clapper ครอบไม่ถึงเหตุการณ์ก่อนเข้าแมพ** — พิมพ์แชตได้ต่อเมื่อเข้าแมพแล้ว ⇒ ใบที่วัดเหตุการณ์ **ตอน scene-load / แรกเข้า** (ทรงเดียวกับ GT-034 P1 · `V134`) **ยังไม่มีจุดจูนสำหรับช่วงที่ตัวเองสนใจ** และกฎนี้ช่วยไม่ได้
   - **ทางแก้ถาวรที่ยังค้างอยู่ (ไม่ใช่ตัวแทนของกฎนี้ · ทำเมื่อไหร่ก็ได้):** งาน *"exporter พิมพ์ ISO timestamp"* ที่ R163 §⑥ เลื่อนไว้ — 🔴 **และมันเหนือกว่า clapper ทุกมิติ** เพราะไม่ยิงทริกเกอร์ · ไม่ต้องมีเหตุการณ์บนจอ · ครอบถึงช่วงก่อนเข้าแมพ ⇒ **ถ้าจะลงทุนที่เดียว ลงที่นี่**
   - 🔴 **บันทึกความล้มเหลวของรอบแรกที่ลอง:** จ็อบ 1150-1152 ขอ clapper แบบแทรกกลางรอบ **แล้วมันไม่ถูกส่ง** (ไม่ปรากฏบนสาย · ช่องแชตมีแค่บรรทัดระบบ) — ไม่ใช่ความผิดใคร **แต่เป็นเหตุผลว่าทำไมมันต้องอยู่ในใบ ไม่ใช่ในแชตระหว่างรอบ**

   ### 🔴 กติกาการอ้างตัวเลขข้ามสองนาฬิกา (ฉบับแก้ — ฉบับแรกห้ามแบบเหมารวมซึ่งผิดกฎตัวเองตั้งแต่วันแรก)
   **ห้ามอ้างเมื่อ *ขนาดของ error เทียบเท่าหรือใหญ่กว่าผลที่กำลังอ้าง*** — ไม่ใช่ห้ามทุกกรณี
   - ❌ **ห้าม:** `ไบต์→จอ ~0.12 วิ` (error ที่ไม่รู้ค่าอาจใหญ่กว่าผลสิบเท่า) · การจับคู่เฟรมกับ `SENT` ที่ห่างกัน `1.50 วิ`
   - ✅ **อ้างได้:** `31 วิ หลังปิด socket ยังอยู่บนแมพ` (error ≤ ~2 วิ ไม่พลิกข้อสรุป) — **แต่ต้องเขียนกำกับว่าเป็นค่าข้ามนาฬิกาที่ยังไม่จูน**
   - ✅ **ปลอดภัยเสมอ และควรใช้แทนเมื่อทำได้:** เปรียบเทียบ **ลำดับ** ของเหตุการณ์ **ภายในนาฬิกาวิดีโอตัวเดียว** — `d` ตัดกันทางพีชคณิต

---

> 📦 **[archive]** ประวัติศาสตร์รอบใหญ่ #2 (Q1/Q2 รอบ 22 · โน้ตรอบ 15–19 · GT-008/009/010 · GT-001 ครั้ง 1–3)
> → `pf_bridge/archive/GAME_TEST_QUEUE_ARCHIVE_20260818.md` · ประมวลเข้า repo แล้ว: `reports/PF_BIGROUND2_ATTENDED_RESULTS_20260818.md` · ledger PF-013/014/015 amended · matrix chat_input_echo → runtime_pass

## รายการที่ปิดแล้ว (GT-002..006 · 011 · 015 · 017 · 018-022 · 023-025) — ⤴ stub ทั้งหมดย้ายไป archive (รอบ 97)

> pointer รวม: `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R97_CLOSED_STUBS.md`
> (ในนั้นชี้ต่อไปยัง archive เนื้อหาเต็มของแต่ละรายการอีกชั้น — ไม่มีอะไรถูกลบ)
> ใจความที่ยังต้องรู้: GT-019 พิสูจน์ hp0+timer ตายบนจอ · GT-021 พิสูจน์ client ไม่ลดตัวนับเอง
> · GT-022/025 พิสูจน์ท่านอน = DYING_LATCH (`_F_DIE_000` ยังไม่เคยถูกสังเกต — ห้าม flip HYP-PF-023)
> · GT-024 พิสูจน์เลขเรนเดอร์บนผู้เล่น + HP ไม่ลด (สองปาก) — ที่มาของ GT-031

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

## GT-033 LOGOUT-TRANSITION A/B: response ไหนทำให้ client เปลี่ยนหน้าจริง [✅ **ANSWERED — ปิดโดย chief R166 · 2026-08-25 ~17:5x (+07:00)** · จ็... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕⭐ GT-034 HOSTILE-NATIVE-001: hostile ตัวจริงขึ้นแดงเองตอน scene-load โดยไม่ต้อง splice faction ไหม — เป้า `0x201F` Tornado Eagle · วิธี = ย... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕⭐ GT-035 DAMAGE-ON-HOSTILE-001: หลอดเลือดของ **hostile ตัวจริง** `0x201F` Tornado Eagle (HP baseline 3,857) ลดตามเลขคณิตของเซิร์ฟเวอร์ไหม [... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕 GT-036 KILL-HOSTILE-001: วงเต็ม "ตี → เลือด → ตาย" บน hostile ที่มี HP จริงจาก STANDARD_MOB  [🔴 **คง BLOCKED — เหตุผลถูกเปลี่ยนโดย chief R164 (2026-08-25 ~16:xx +07:00) · GT-035 ปิดเป็น PASS แล้วแต่ ใบนี้ *ไม่* ถูกปลด** · 🔴🔴 **ห้ามอ่านว่า "GT-035 ปิดแล้ว ⇒ ปลดได้" — ตัวบล็อกไม่ใช่ GT-035 อีกต่อไป** · ตัวบล็อกใหม่มีสองชั้นซ้อนกัน: ① **ไม่มีเลนโค้ดที่มีครึ่งตาย** — `HYP-PF-038` ตัดครึ่งตายทิ้งโดยเจตนา (การ์ด lethal-field ของแผนแม่ ที่ซอร์สเรียกว่า `HOSTILE_HP_LINK_HP_FLOOR` และประกาศว่า FORBIDDEN · ladder จบที่ `771`) ② **ต้องให้คุณ Panya เคาะก่อน** — การปลดการ์ดนั้นคือ "เปลี่ยนของที่พิสูจน์แล้ว" ตามนโยบายข้อ 3 · คำถามถูกวางไว้ในจดหมาย `FROM_CHIEF_R164_TO_ATTENDED_20260825_1600.md` §⑤ **และยังไม่มีคำตอบ** · 🔴 **ห้ามอ้างผล GT-035 เป็นหลักฐานของใบนี้ไม่ว่ารูปแบบใด** — เลนนั้นไม่มีเฟรม hp=0 ไม่มี death timer ไม่มี dying latch และหลอดจบที่ `771` ไม่เคยแตะ `0`] *(สถานะเดิมก่อนเปลี่ยนเหตุผล:* [🔴 **BLOCKED — รอ GT-035 (GT-034 ตอบแล้ว 2026-08-25 · chief R158) · ยังไม่ปลด**]

> 🟢 **อัปเดต chief R167 · 2026-08-25 ~19:xx (+07:00) — ชั้นที่ ② ปลดแล้วโดยเจ้าของ ชั้นที่ ① ยังอยู่**
> คำเคาะ ~18:15 (+07:00) (จดหมาย `notes_to_chief\consumed\20260825_1815_PANYA-RULINGS-FOUR-quota-cap5-GT036-lethal-scoped-GT030-rerun.md` ข้อ ③): *"ใช้การข้ามข้อจำกัดเฉพาะกิจ ให้เทส GT-036 นกตายได้"*
> 🔴 **ยกเว้นเฉพาะสองวลีใน `HYP-PF-038.stop_rule` เท่านั้น: `alive at the end` และ `a lethal frame`** (รวม death timer เท่าที่จำเป็นต่อการตาย)
> 🔴 **ที่ยังบังคับเหมือนเดิม ห้ามอ่านว่าถูกปลดไปด้วย:** ห้าม `a second target` · ห้าม `widen the attacker profiles` · `one shot per connection` · identity `0x201F` เท่าเดิม · `production_allowed=false` · ห้ามเอื้อมไป allowlist ของเลน arena
> **ชั้นที่ยังบล็อกอยู่จริง (①):** ยังไม่มีเลนโค้ดที่มีครึ่งตาย — ต้องมี **`HYP-PF-038` v2** ก่อน (เพดานเวอร์ชันขยับ 3→5 ในรอบนี้แล้ว ⇒ `HYP-PF-038` อยู่ที่ 1/5 มีที่ว่าง 4 ⇒ **ไม่ต้องเปิด entry ใหม่**)
> 🔴 **R167 ยังไม่สร้าง v2 และนี่คือเหตุผล:** รอบนี้ถือ PR ที่เป็น merge ก้อนใหญ่ (เลน nameprop 2,523 บรรทัด + เพดาน ledger ทั้งไฟล์) อยู่แล้ว · เอาเฟรมตายที่ยังไม่เคยมีใครออกแบบไปกองรวมใน PR เดียวกัน = ถ้า gate แดงจะแยกไม่ออกว่าใครทำแดง **และเสียสล็อตเวอร์ชันฟรี ๆ ถ้าออกแบบผิด**
> ⇒ **แบบร่างของ v2 ถูกเขียนไว้ให้รอบถัดไปหยิบไปทำทันที** ใน `rounds/R167_2kn5o7_merge-stranded-nameprop-lane-and-raise-version-ceiling.md` §④
> 🔴 **เมื่อรอบตายผ่าน สิ่งที่พิสูจน์คือ "เป้าที่เราสร้างตายได้" ไม่ใช่ "ศัตรูตายได้"** — คำว่า hostile ยังไม่ถูกพิสูจน์ (ป้ายชื่อขึ้นเขียว = สีผู้เล่นของเซิร์ฟเวอร์เดิม · `RE-067`) **เขียนผลให้ตรงชั้นนี้ตั้งแต่ต้น**
> **ขั้นถัดไปที่เจ้าของประกาศล่วงหน้า (จดไว้ อย่าทำก่อน):** ถ้าวงตายผ่านบน `0x201F` แล้ว **ค่อย** เปลี่ยนเป้าเป็น mob จริงจากตารางเกม — **ห้ามรวบสองขั้นเป็นรอบเดียว**


ตาม ORDER ลำดับ 3 · โครง: ทำซ้ำ GT-031 (HYP-PF-026) แต่ ladder ใช้ HP baseline ของตัวที่เลือก (เช่น Tornado Eagle lvl 27 = 3,857) · nonclaim เดิมทุกตัว + HP เป็น baseline ฝั่ง client

> 📌 **อัปเดต chief R159 (2026-08-25) — ตัวบล็อกไม่เปลี่ยน ยังรอ GT-035 เหมือนเดิม · สิ่งที่เปลี่ยนคือ *ความหมาย* ของการรอ**
> เดิมรอคำตอบที่ยังไม่มีใครรู้ · ตอนนี้รอ **สิ่งที่ระบุตัวได้แล้ว**: เลน `HYP-PF-038` เวอร์ชันแรก (ladder ไม่แตะพื้น 0) ผ่านตาคุณ Panya ก่อน
> แล้ว **GT-036 คือเวอร์ชันถัดไปของ slot เดียวกัน** ที่ต่อ ladder ลงถึง 0 + `dying latch 20.0` + `death task 0.0`
> ตามทรงที่ GT-039 พิสูจน์แล้วบน `0x2001` · 🔴 **[แก้โดย chief R164: เงื่อนไข "ก่อน GT-035 ปิด" ในประโยคถัดไป **หมดอายุแล้ว** — GT-035 ปิดเป็น PASS เมื่อ 2026-08-25 และ **ใบนี้ยังไม่ถูกปลด** ตัวบล็อกที่ใช้จริงอยู่ในวงเล็บสถานะหัวใบ อ่านที่นั่น]** · ~~ห้ามเปิด slot ใหม่ให้ GT-036 และห้ามปลดมันก่อน GT-035 ปิด**~~
> 🔴 **และห้ามปิด GT-036 เป็นผลลบจากผลลบของ GT-035** — ถ้า GT-035 ออกลบ ให้ไปเปิดใบ static เทียบสอง identity ก่อน (เขียนไว้ในใบ GT-035 แล้ว)

> ⚠️🔴 **คาเวียตรอบ 118 (static ล้วน — ไม่ได้บูตอะไร ไม่ได้แตะสถานะ/pass criteria ของใบนี้แม้แต่ตัวเดียว):
> เป้าเดียวที่เซิร์ฟเวอร์ของเรา spawn-แล้ว-ฆ่า ได้แบบ headless คือ `0x2001` ซึ่ง "ไม่ดรอปอะไรเลย"**
> - `0x2001` = placement index 0 = MOBS template `n_ID = 1` "Navy Transfer" · `n_RANK = 0` ·
>   `n_MOB_USAGE = 2` (NPC เมือง ไม่ใช่ mob) · `n_DROPS_EQUIPMENT` / `n_DROPS_NORMAL` / `n_DROPS_SPECIALLY`
>   = **0 ทั้งสามช่อง** · `n_DROPS_QUEST` low part **ไม่มีอยู่ในตาราง DROPS_QUEST ที่ ship มากับ client**
>   ⇒ ที่มา: `pf_bridge\FACTPACK_R100_CONSTDATA_MONSTER_LOOT.md` หัวข้อ 7
> - `n_RANK = 0` ซ้ำอีกชั้นหนึ่ง: ถ้ามี roller อยู่ในสายจริง มันจะตอบ named refusal
>   `loot_roll_refused_no_quality_row_for_rank_and_level` ทุกครั้งที่เดินไปถึงขั้น equipment drop
>   (E_DROPS_QUALITY จับ rank แบบ **เท่ากันเป๊ะ ไม่ใช่ bitmask**)
>   ⇒ `reports/PF_LOOT_ROLL001_SERVER_SIDE_ROLLER_20260820.md` (อยู่ใน repo โค้ด ไม่ใช่ bridge)
> - 🔴 **ผลที่ต้องจำให้ได้:** ถ้ารอบไหนในอนาคตต่อ loot roller เข้าสายจริงแล้วเอาเทสฆ่ามารันบน `0x2001`
>   **"ผลว่างเปล่า" คือคำตอบที่ถูกต้องของข้อมูล ไม่ใช่หลักฐานว่าลูทพัง** — ห้ามใครอ่านเป็น FAIL หรือ regression
> - hostile ตัวจริงทั้ง 13 ตัว **มี drop ref จริง** (เช่น `0x201f` Tornado Eagle = `2701001/5400001/2802234`)
>   ⇒ `pf_bridge\FACTPACK_R102_HOSTILE13_ROSTER.md` บรรทัด 18-32 · **แต่ยังไม่มีเลนเซิร์ฟเวอร์ใบไหนเล็งตัวใดตัวหนึ่งได้เลย**
>   และตัวใกล้สุดอยู่ ~11,914 หน่วย = คำถามระยะทางที่ GT-034 จอดรออยู่พอดี
>   ⇒ **คาเวียตนี้ไม่ปลดบล็อกอะไรทั้งสิ้น ใบนี้ยัง 🔴 BLOCKED เหมือนเดิม**
> - **สถานะลูทจริง ณ รอบ 118:** `src/pirateforce_foundation/loot_roll.py` เป็น **ไลบรารีที่ไม่มีใครเรียก** —
>   `production_allowed = False` และ `tools/verify_loot_roller.py` เฝ้าไว้ว่า **ห้ามมีโมดูลอื่นใน `src/` อ้างถึงมัน** ·
>   ไม่มี wire path และไม่มีตาราง DB สำหรับผลการตัดสินลูทเลยสักช่อง
>   ⇒ **GT-036 วันนี้คือ "ตี -> เลือด -> ตาย" ล้วน ๆ ไม่มีครึ่งลูทอยู่ในใบนี้แม้แต่บรรทัดเดียว**
>   (ครึ่งลูทอยู่ที่ GT-037 ✅ DONE และ GT-040 🟢 PENDING)
>
> **บันทึกเพิ่ม — มีผลเฉพาะรอบที่ลูทถูกต่อเข้าสายจริงแล้วเท่านั้น (pass criteria เดิมของใบนี้ไม่เปลี่ยน):**
> - **ชั้น wire/DB:** จด **identity ของเป้าที่ยิงจริง** (`0x2001` หรือเลขจาก roster) ลงในผลทุกครั้ง ·
>   ถ้ามี roller ในสาย ต้องเห็น **refusal ตามชื่อ** ในคอนโซล/ล็อก (`loot_roll_refused_drop_set_id_zero`
>   สำหรับสามช่องที่เป็น 0 · `loot_roll_refused_no_quality_row_for_rank_and_level` สำหรับ rank 0) —
>   🔴 **"เงียบ ไม่มีบรรทัดเลย" ไม่เท่ากับ "ปฏิเสธตามชื่อ" ต้องจดเป็นคนละผลกัน**
> - **ชั้น client-observable:** จดว่าบนจอ **ไม่มี** ของตกพื้น / หน้าต่างลูท / ข้อความใด ๆ หลัง NPC ตาย —
>   นี่คือ **ค่าที่คาดไว้ล่วงหน้า (คำทำนาย ไม่ใช่ข้อเท็จจริง)** สำหรับ `0x2001` และผลลบมีค่าเท่าผลบวก ·
>   ถ้า **เห็น** อะไรโผล่มาจริง = ข่าวใหญ่ จดทันทีพร้อมเวลาบนนาฬิกาในวิดีโอ
>
> **nonclaims ของคาเวียตนี้:** อ่าน artifact ที่ commit แล้วอย่างเดียว — ไม่ได้บูตเซิร์ฟเวอร์ ไม่ได้เปิด client
> ไม่ได้แตะ canonical DB · ตาราง drops ทั้งหมดเป็นข้อมูลที่ ship มากับ client **ไม่ใช่พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ
> ซึ่งกู้ไม่ได้ตลอดกาล** · ไม่ได้พิสูจน์ว่า hostile ตัวจริงจะดรอปอะไรออกมาบนจอ — พิสูจน์แค่ว่า
> **ตารางของมันไม่ว่าง ส่วนของ `0x2001` ว่าง** · ชื่อ refusal ทั้งสองตัวยืนยันแล้วกับ
> `src/pirateforce_foundation/loot_roll.py` (`REFUSAL_ID_ZERO` · `REFUSAL_NO_QUALITY_ROW`) ในรอบนี้

## 🆕 GT-037 LOOT-ROLL-001: server-side loot roller จาก client tables [✅ **DONE — chief รอบ 113 (cloud) build เสร็จ · เขียว(cloud sanity) 992 pa... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕 GT-038 DAMAGE-TARGET-AB-001: A/B — การคลิกเลือกเป้าเกี่ยวอะไรกับเลขที่มองเห็นไหม [✅ **PASS — 2026-08-22 23:24 (+07:00): target selection ไ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🎯 GT-039 NPC-HP-LINK-001: **หลอดเลือดของ "เป้าหมาย" ลดจริงไหม** [✅✅ **PASS — รอบใหญ่ #11 (UNATTENDED) 2026-08-21 02:05–02:25 · HEAD `cc46a0... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 GT-040 DROPTHING-TRANSPORT-PROBE-001 [STATIC-ON-BRIDGE]: "วัตถุลูทบนพื้น" มี transport อยู่ในอิมเมจจริงไหม — สามจุดที่ยังไม่มีใครเปิดสักค... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕⭐ GT-041 MOVE-AUTHORITY-002: เซิร์ฟเวอร์ "ไม่ยอมเขียน" ตำแหน่งที่ client รายงาน — ผู้เล่นเห็นอะไรไหม [✅ **PASS (no-rejection) — 2026-08-23 ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-030 REMOTE-PLAYER-VIS-001: "มีคนอื่นอยู่ในโลก" ครั้งแรก — actor_type 2 ทั้ง 5 เฟรม [🟠 **ผล substantive แล้ว — rerun 2026-08-23 00:25 (+07... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-030-R3 REMOTE-PLAYER-VIS-PROVENANCE-001 [attended, in-game]: รอบสามของ `GT-030` — **ของที่เห็นบนแนว probe เป็นผลของเฟรมที่เลนนี้ส่ง หรืออ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-031 DAMAGE-HP-LINK-001: วงเต็ม "ตี → เลือด → ตาย" ครั้งแรก (ฝั่ง**ผู้เล่นเอง**) [✅ **PASS — รอบใหญ่ #12 (2026-08-21 ~08:0x +07:00)**] -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-032 NPC-HOSTILE-001: NPC ตัวแรกของ Port Royal "ขึ้นศัตรู (แดง)" ไหม — Door A ของ mob-aggro [✅ **PASS — รอบใหญ่ #12 ต่อ (2026-08-21 ~09:00... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🛠️ บทเรียนเครื่องมือใหม่จากรอบใหญ่ #12 (chief R119 ยกจากจดหมายผู้เทส 2026-08-21 08:37 +07:00)

1. 🔴🔴 **ปุ่มในเกมไม่ตอบสนองคลิกสังเคราะห์เป็นช่วง ๆ — แต่ `Return` ใช้ได้เสมอ**
   - หน้า character select: คลิกปุ่ม `เข้าเกม` ไม่ติดเลยสักครั้ง (เคอร์เซอร์อยู่บนปุ่ม ปุ่มขึ้น hover ด้วยซ้ำ) · กด `Return` เข้าเกมทันที
   - ช่องแชต: คลิกแล้วพิมพ์ → ตัวอักษรหาย · **กด `Return` ก่อน → ช่องโฟกัส → พิมพ์ได้ปกติ**
   ⇒ **ท่ามาตรฐานใหม่ทุก GT: `Return` → พิมพ์ → `Return`** · ปุ่มไหนไม่ยอมติดให้ลอง `Return` ก่อนเสมอ
2. 🔴 **หน้าต่าง PowerShell ของ watchdog เด้งทุก ~5 นาทีและแย่งโฟกัส** (เห็นสองครั้งในรอบ #12)
   — เป็นคำอธิบายที่เข้ากับ "คลิกไม่ติดเป็นช่วง ๆ" ข้อ 1 แต่**ยังไม่ได้พิสูจน์ว่าเป็นสาเหตุเดียว**
   ⇒ เข้าคู่บทเรียนเดิมรอบ #9/#10 เรื่อง `hold_key` ค้างเมื่อโฟกัสถูกแย่ง — ความเสี่ยงเดียวกัน คนละอาการ
   🔴 **ข้อเสนอถึง Panya (chief R119): watchdog console โผล่บนจอ = มันไม่ได้รันแบบ hidden** —
   ถ้าจะให้รอบ unattended นิ่ง ควรสลับ task ให้รันแบบซ่อน/ไม่แตะ desktop ของเซสชันเทส (ตัดสินใจฝั่งเครื่องเท่านั้น chief ทำจากคลาวด์ไม่ได้)
3. **คลิกท้องฟ้า/พื้นในหน้า character select = ยกเลิกการเลือกตัวละคร** (ปุ่มเหลือ 3 ปุ่ม) — ต้องคลิกตัวละครเลือกใหม่ก่อน

## 🛠️ บทเรียนเครื่องมือใหม่จากรอบใหญ่ #9/#10 (chief รอบ 102 ยกจากจดหมายผู้เทส + static R102)

- 🔴 **เลขดาเมจทั้งหมด (รวม `MISS!`) ปิดได้เงียบ ๆ ด้วยปุ่มเดียว:** client มี toggle `[localplayer+0x420]`
  (input command `0x27` · byte-proven `0x43FE2C je no-draw` / toggle `0x42C68A` / default ON `0x44CAC2`)
  — ปิดแล้ว **จอไม่ขึ้นเลขเลย แต่ wire เหมือนเดิมทุกไบต์ และไม่มีอะไรโผล่ในล็อกเซิร์ฟเวอร์**
  · เข้าคู่กับบทเรียนเดิม "ตัวอักษรตอนช่อง input ไม่โฟกัส = hotkey" ⇒ นี่คือผู้ต้องสงสัยหลักของ
  เซสชันที่ 'ตาบอด' ใน GT-027 รอบแรก
  **กฎใหม่สำหรับทุก GT ที่ต้องเห็นเลข:** ① ใช้ client ที่เพิ่งเปิดใหม่ (default = ON)
  ② ห้ามพิมพ์อะไรนอกช่องแชตที่ยืนยันโฟกัสแล้ว ③ ถ้าจอมืดทั้งเซสชัน → **relaunch client ก่อนสรุปว่า wire ผิด**
  (ยังไม่รู้ว่าปุ่มไหน map ไป command 0x27 — [UNKNOWN] · อย่าไปลองกดหา)
- 🔴 **batch ที่มี `hold_key` แล้วถูกขัดกลางคัน (หน้าต่างอื่นแย่งโฟกัส) = ปุ่มค้าง ตัวละครเดินเอง** —
  เคยพาหลุดไป X `-11,490` (~2,900 หน่วย เสีย ~6 นาที) · **กฎ: batch ล้ม → ถือว่าตำแหน่งไม่น่าเชื่อถือ
  อ่านพิกัดใหม่เสมอ · อย่าใส่ hold_key หลายตัวใน batch เดียวถ้ามีความเสี่ยงเรื่องโฟกัส**
- ℹ️ **ทางลัดหน้าเลือกเซิร์ฟเวอร์ (Panya สั่ง ใช้แล้วได้ผล):** กด `เข้า` ได้เลย ไม่ต้องคลิก server → channel ก่อน

## 🛠️ บทเรียนเครื่องมือจากรอบใหญ่ #8 (chief รอบ 93 ยกมาจากผลของผู้เทส — ใส่ใน template ให้หมด)

1. ⭐ **เปิด client ด้วย `Invoke-CimMethod Win32_Process Create`** ไม่ใช่ `Start-Process -Redirect*` ⇒ ลูกไม่สืบทอด handle **สะพานกลับ idle ทันที** (วงจรอุดตันของรอบ #7 หายถาวร)
   🔴 **ห้ามแค่ลบ `-Redirect*` ทิ้ง** — `Start-Process 'xxx.bin'` ที่ไม่มี redirect ใช้ ShellExecute และ `.bin` ไม่มี file association ⇒ **ล้มเงียบ `-PassThru` คืน `$null`** · redirect มีไว้บังคับ `UseShellExecute=false`
2. 🔴 **การ์ดบังคับก่อนเปิด client ตัวใหม่:** ถ้า `Get-NetTCPConnection -State Established` บนพอร์ต 10188/10189 **> 0 ให้ ABORT** — ดูแค่ `Get-Process = 0` **ไม่พอ** (จ็อบ 925 พลาดข้อนี้ → ค้าง "กำลังเชื่อมต่อ..." เสียเวลา ~15 นาที) ⇒ **ต้องอยู่ในโค้ดของทุก template ที่เปิด client ไม่ใช่ในดุลพินิจ**
3. 🔴 **จ็อบ relaunch client ต้องเขียน `stamp` ของ *รอบบูต*** ไม่ใช่เวลาของตัวเอง มิฉะนั้น guard window ของ teardown (stamp-1 .. stamp+5 นาที) จะไม่ครอบ console ที่บูตไปก่อน (จ็อบ 918 → 919 fail exit 15)
4. **แชตในเกม: ถ้าไม่ได้โฟกัสช่อง input จริง ตัวอักษรจะกลายเป็น hotkey** ⇒ ท่าที่ปลอดภัย: เลื่อนเมาส์ไปเหนือแผงแชต → คลิกแถบ input → **ถ่ายยืนยันว่าข้อความอยู่ในช่องแล้ว** → กด Enter **ในการเรียกครั้งเดียวกัน**
5. **ทริกเกอร์ต้องเป็น ascii 12 ตัวอักษรจริง ๆ** — `PFPROBE2` (8 ตัว) เฟรมถึงเซิร์ฟ (`0xAC52` 46 ไบต์) แต่ **ไม่เข้าเงื่อนไข ไม่มี sweep ออกมา** ⇒ ความยาวเป็นส่วนหนึ่งของ predicate
6. **หน้าต่างเซิร์ฟเวอร์ (py.exe) เปิดทับหน้าต่างเกมเสมอหลังบูต** — ผู้เทส local ต้องขอสิทธิ์ `py.exe` ไว้ด้วยเพื่อสลับหน้าต่างได้ (tier `click` พอ)
7. **เลขจ็อบ:** ผู้เทสใช้ **9xx** เท่านั้น (รอบใหญ่ #8 ใช้ 912–932 ⇒ ตัวถัดไป **933**) · chief ใช้เลขวิ่ง 1xx (รอบ 99 ใช้ 161 ⇒ ตัวถัดไป **162**)


## 🆕🔬 GT-042 DROPTHING-REDERIVE-001 [STATIC-ON-BRIDGE]: ตรวจซ้ำแบบ "ปฏิปักษ์" ผลสามท่อน A/B/C ของ GT-040 + ปิดชิ้นที่ขาดชิ้นเดียว (`0x402A20`) ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕⭐ GT-043 POP-SURVIVAL-001 [attended, ของแถมสังเกตล้วน]: หลังยิงเฟรม count-1 บิต `0x02` แล้ว NPC/วัตถุตัวอื่นในโลก "หายไหม" [✅ **PASS-PERSIS... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 GT-044 SCENEID-BG0001-001 [STATIC-ON-BRIDGE]: dump SCENE_NAME (ตาราง 007) + MAP_SCENE_LIST (ตาราง 101) จาก `B_CONSTDATA_TH.pc_.dec` — ปิด... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## ⭐ GT-045 GROUNDDROP-RENDER-001 **v3 re-run** [attended, in-game]: บิต `0x08` ของ `0x5F85B0` วาด "วัตถุลูทบนพื้น" ไหม — ยิงเรคคอร์ดพิกัดโลกที... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🔬 GT-046 PICKUP-DIRECTION-001 [STATIC-ON-BRIDGE]: `PickupTerrainThing` เป็นข้อความที่ไคลเอนต์ "ส่งออก" หรือ "รับเข้าอย่างเดียว" — หาจุดสร้าง... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🔬 GT-047 RUNTIMEPROTO-CAPTURE-VALIDATE-001 [STATIC-ON-BRIDGE]: parse เฟรม `GSCN_RunTimeProtocolReq`/`Res` จาก capture corpus ด้วย schema ของ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🔬 GT-048 NATIVE-SPAWN-CONDITION-001 [STATIC-ON-BRIDGE]: อิมเมจ client มีเส้นทาง "สร้าง/วาง entity hostile ตอน scene-load จากข้อมูลที่ ship ม... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 GT-049 LOOT-CHAT-TEMPLATE-001 [STATIC-ON-BRIDGE]: หา template ของบรรทัดสีเขียว `ได้รับ [<ชื่อ>] * <จำนวน>` ในตารางข้อความ/`B_CONSTDATA` แ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-051 RENDER-SYNTHESIS-001 [เอกสารล้วน · ✅ **DONE — chief cloud ทำเองเสร็จใน R128 (2026-08-23 ~18:1x +07:00) · ไม่ใช่งานสะพาน ไม่มีอะไรให้ผ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## ⭐ GT-058 LEARN-SKILL-RESULT-001 [attended, in-game]: ไคลเอนต์ "ทำอะไร" กับเฟรม CLearnSkillResultVital (0x673C) เมื่อรับ sweep 5 สเต็ป — อัปเ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-059 SKILL-ATTR-WINDOW-GATE-001 [attended, in-game]: ส่ง `CSkillAttr` (attr block `0x1661` ขี่ `UpdateAttrVital` `0x309A`) แล้วหน้าต่างสกิ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
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
## GT-063 ITEMOPERATE-RES-GREENLINE-SHAPE-001 [attended, in-game]: ยิง `ItemOperateVitalRes` (`0x4C13`) สามทรงจากเซิร์ฟเวอร์เรา แล้วตัดสินด้วยต... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-064 SKILL-ATTR-WINDOW-KPRESS-IN-GAP-001 [attended, in-game]: กด **K** / คลิก `Bt_main_Skill` **ภายในช่อง 3.0 วิ ระหว่างเฟรม `COUNT0` (57B... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-069 GROUNDLOOT-NAMELABEL-TEXTPROP-SELECTOR-001 [attended, in-game]: ยิง **เฟรมคุม (mask `0x12`) กับเฟรมทดลอง (mask `0x3A` · gate `+0x1B`=1 · index `+0x1A`=6) ที่พิกัดเดียวกัน** แล้วดูว่า **หน้าตาของป้ายชื่อไอเทมบนจอต่างกันหรือไม่**  [🔴 **BLOCKED ×2 — ต้องปลดครบทั้งสองข้อ:** **(1) เจ้าของเคาะว่าเลนนี้เกิดได้หรือไม่** (ดูบล็อก "งบเวอร์ชัน" ข้างล่าง — **ข้อนี้ยังไม่ถูกเคาะ**) · **(2) ผ่านด่านเจ็ดข้อบน commit ที่ gate ตัดสินแล้ว** · โค้ดถูก push ขึ้น branch และ **จงใจยังไม่ merge เพราะข้อ (1)** ⇒ **ถ้าเจ้าของยังไม่เคาะ ใบนี้รอเจ้าของ ไม่ได้รอผู้เทส และไม่ได้รอ CI** · เปิดใบโดย chief R165 (2026-08-25 ~17:0x +07:00) ตามบรรทัดปิดท้ายของ `RE-067`] -- moved to `tickets/GT-069.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `cm9v9y` 2026-09-06T17:10+07:00)

## GT-072 ACTOR-SLOT-DISPLACEMENT-001 [attended, in-game]: spawn actor ของเรา **ทับพิกัด placement ของ NPC ที่มีอยู่** แล้ว NPC ตัวนั้น **หายจากจอหรือไม่ — และถ้าหาย มันคือ despawn / แทนที่ / บังทับ**  [🟡 **PARTIAL — บันทึกผลรอบแรกโดย chief R170 (2026-08-25 ~22:0x +07:00) · ใบยังเปิดอยู่** · จ็อบ 1167/1168/1169 attended · 🔴 **ยังไม่มีค่าไหนในสามค่าถูกตัดออก** — ตัวคุมที่เก็บมาถูกวัด *หลัง* ของที่ต้องแยกแยะหายจากจอไปแล้ว (ดูไทม์ไลน์ท้ายใบ) · ตัวคุมที่ยังไม่ได้ทำ: `W2` · `W3` · `POST-A` ⇒ ยกไปใบ **`GT-074`** · **ผลอยู่ท้ายใบ** · เปิดใบโดย chief R168 (2026-08-25 ~20:3x +07:00) ตามผลข้างเคียงข้อ ④ ของ `GT-030-R3` · เขียนใบโดย `pf-queue-author`]

> 🔢 **เรื่องเลขใบ (อ่านก่อน):** ตัวนับเป็น **ชุดเดียวร่วมกับ `CLIENT_RE_QUEUE.md`** — prefix สองแบบ ตัวนับเดียว
> เลข **071 ถูกจองโดย `RE-071`** (งาน `STATIC-ON-BRIDGE` ของรอบเดียวกัน: *BasicAttr ของ actor ที่เกิดจาก `SPAWN_BARE`*)
> ⇒ **ใบนี้คือ `GT-072`** · grep ยืนยันก่อนจอง: `GT-072`/`RE-072` = 0 hit ทั้งสองไฟล์ ⇒ **เลขว่างถัดไปคือ 073**
> 🔴 **ร่างแรกของใบนี้เขียนเลขเป็น `GT-071` — chief แก้เป็น `GT-072` ตอนวาง** ถ้าเจอ `GT-071` ที่ไหนในเอกสารเก่า นั่นคือใบนี้
> 🔴 **ใบ `GT-030` และ `GT-030-R3` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย** — ใบนี้ยืนอยู่บนผลของมัน

---

### objective (claim เดียว)

**การที่เซิร์ฟเวอร์ spawn actor ของเราลงบนพิกัด placement ของ NPC ที่มีอยู่ ทำให้ NPC ตัวนั้นหายจากจอหรือไม่ — และการหายนั้นอ่านออกเป็นแบบไหนในสามแบบที่มีชื่อ (`despawn` / `แทนที่` / `บังทับ`)**

**ตัวหักล้างมีตัวเดียว:** *"NPC ยังอยู่ให้เห็น/ให้เลือกได้ ที่พิกัด `P0` หลัง `SPAWN_BARE`"*

### 🔴 ทำไมนี่คือ claim เดียว ไม่ใช่สาม (กติกา "หนึ่งใบหนึ่งข้ออ้าง")

`despawn` / `แทนที่` / `บังทับ` **ไม่ใช่สามข้ออ้าง** — มันคือ **สามค่าที่อ่านได้จากการวัดชุดเดียวกัน** (คู่ภาพมุมเดียวกัน + คู่ภาพมุมอื่นที่ถ่ายไว้ก่อน-หลัง + การคลิก/`Tab` ที่จุดเดิม) ⇒ อยู่ในตารางผลลัพธ์ที่มีชื่อ `N1..N8` ใบเดียว
- **บังทับ** แยกออกได้ด้วย **มุมกล้อง/ระยะ** (ของที่ถูกบังจะโผล่กลับมาเมื่อเปลี่ยนมุมหรือเดินเข้าไปใกล้)
- **แทนที่** แยกออกได้ด้วย **มีอะไรให้เลือกที่จุดนั้นไหม** (ลูกศรเลือก + target panel เปิด แต่ไม่ใช่ NPC)
- **despawn** คือแถวที่เหลือ **และมันเป็นแถวที่อ่อนที่สุดโดยธรรมชาติ** (ดู nonclaim ข้อ ③ — "คลิกไม่ติด" ไม่เท่ากับ "ไม่มีอะไรอยู่ตรงนั้น")

🔴 **สิ่งที่ใบนี้ไม่ได้ถาม:** *อะไรในไคลเอนต์ทำให้เกิดผลนี้* (ช่อง actor / id / hash ตำแหน่ง / ลำดับ list) — **ไม่มีหลักฐาน static แม้แต่บรรทัดเดียวในโปรเจกต์เรื่องนี้** ⇒ ห้ามเขียนคำอธิบายกลไกลงในผลไม่ว่ากรณีใด

---

### pass criteria — **สองชั้น แยกกันเด็ดขาด 🔴 ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

**ชั้น (1) wire/DB + หลักฐานเชิงไฟล์ — ทำ headless ได้ ไม่ต้องมีคนหน้าจอ**
1. `GAME_LIVE.txt` / console: **ห้าเฟรมเรียงตามลำดับ** `SPAWN_BARE` → `SPAWN_AVATAR` → `MOVE_A_1` → `MOVE_A_2` → `NEGATIVE_CONTROL` **ห่างกัน 15.0 วิ** · ขนาด **181 / (โครง 172) / 72 / 77 / 218 B** · **`frame_sha256` ของสี่เฟรมที่พินได้ ต้องตรง `probe.per_step.<LABEL>.frame_sha256` ของ scenario ใน commit ที่บูต** · `SPAWN_AVATAR` ตัดสินด้วย `pc_skeleton_sha256` (172 B) เท่านั้น
2. 🔴 **census: นับ *ทุก* บรรทัด `[G>]` ทั้งไฟล์ แล้วรายงานยอดรวม ไม่กรองอะไรออก** — ยอดรวม ≠ 5 **คือคำตอบ ไม่ใช่ความผิดพลาด**
3. 🔴🔴 **ด่านที่เป็นของใบนี้โดยเฉพาะ: ยืนยันว่า *ไม่มีเฟรม despawn/remove/delete ใด ๆ ออกจากเซิร์ฟเวอร์ทั้งรอบ*** — เลนนี้ไม่มีเฟรมชนิดนั้นในดีไซน์ (`GT-030`: *"ไม่มีทาง despawn probe"*) ⇒ ห้าเฟรมข้างบนคือทั้งหมดที่ออก ⇒ **ถ้า NPC หาย มันไม่ได้หายเพราะเราส่งคำสั่งลบ** · 🔴 **ข้อนี้พูดได้แค่ว่า "เราไม่ได้ส่งคำสั่งลบ" ไม่ได้พูดว่า "ไคลเอนต์ทำอะไรกับ NPC"**
4. **พิกัดที่ decode ได้จริงจาก hexdump (f32):** `SPAWN_BARE` ต้องได้ **X `-9139.957` Y `-2780.045` Z `223.292`** (= `P0` เป๊ะ) · `MOVE_A_1` ต้องได้ **X `-8839.957`** · `SPAWN_AVATAR` **X `-8989.957`** · `NEGATIVE_CONTROL` **X `-9289.957`** 🔴 **ห้ามใช้ HUD เป็นฐานคำนวณ**
5. **ไม่มี label `HYP_PF_025_REMOTE_PLAYER_*` ก่อนเฟรมแชตที่ถูกยอมรับ** + จดเวลานาฬิกาจริงของเฟรมแชต (`0xAC52`) และของ `[G>]` แรก
6. ไม่มี `remote_player_hypothesis_*_no_reply` ใด ๆ · ไม่มี `ErrorData=28317` · ไม่มี traceback / stderr
7. DB สำเนา: `PRAGMA integrity_check` = `ok` · row-diff ต่างเฉพาะ `sessions` **+1 ต่อการเข้าเกมหนึ่งครั้ง** · `max(lease_generation)` ก่อน-หลัง ไม่ถอยหลัง · **sha256 canonical ก่อน-หลัง = `CANON_SHA.txt`** · **canonical ไม่ถูกเปิดตลอดรอบ**
8. **ความครบของวิดีโอ (กฎ S):** `ffprobe` → เฟรมจริงเทียบ `duration x fps` · **รายงานเฟรมที่หายเป็นตัวเลข** · หายเป็นช่วงให้ระบุช่วงเวลา 🔴 **ข้อนี้บอกว่าไฟล์ครบแค่ไหน ไม่ได้บอกว่าในเฟรมมีอะไร**
9. 🔴 **ชั้นนี้ตอบไม่ได้ (เขียนไว้ให้ชัดเพราะใบนี้ล่อให้ทำผิดข้อนี้มากเป็นพิเศษ):** **NPC หายหรือไม่ · หายแบบไหน · มีอะไรอยู่ที่ `P0` หรือไม่** — **ชั้น wire ของเลนนี้ไม่มีทางเห็น NPC ของแมพเลยแม้แต่บิตเดียว** ⇒ **ห้ามอ้างว่า "ไม่มีเฟรมลบ ⇒ NPC ไม่ได้หาย"**

**ชั้น (2) client-observable — ต้องมีคนหน้าจอ · 🔴 ตัวปิดใบอยู่ชั้นนี้ชั้นเดียว**
1. **หลักฐานบังคับ:** วิดีโอต่อเนื่องคลุมตั้งแต่ก่อน `PRE_LAST` ถึงหลัง `+70` · `PRE_C`/`PRE_L`/`PRE_R`/`PRE_C2`/`PRE_PANEL`/`PRE_LAST` · `POST_L`/`POST_R`/`POST_C` · `POST_NEAR` + พาเนลทุกใบ · `W4_31`/`W4_36`/`W4_46` · `W5_59`/`W5_62` · `POST_ONP0` + `POST_ORBIT_1..4` · `POST_B` · `POST_AMOVE` · `POST_P1` · **คู่ภาพชี้ขาด `NPC_PRESENT` / `NPC_GONE_SAME_CAMERA` + crop PNG กรอบเดียวกัน** · **sha256 ทุกไฟล์**
2. **คำตัดสินหลักของใบ = เทียบ `PRE_LAST` ↔ คู่ภาพชี้ขาด (มุมเดียวกัน ตัวละครจุดเดียวกัน)** ⇒ **"NPC หาย" หรือ "NPC ไม่หาย"** พร้อม `t_หาย - T0`
3. **คำตัดสินรอง (ตัวแยกสามทาง) — ต้องตอบครบสามข้อ เป็นคำพูดตรง ๆ:**
   - **(ก) มุม:** เทียบ `PRE_L↔POST_L` และ `PRE_R↔POST_R` ⇒ **"เห็น NPC จากมุมอื่น" / "ไม่เห็นจากทุกมุมที่ถ่าย" / "เทียบไม่ได้ (มุมเพี้ยน/กล้องขยับ)"**
   - **(ข) ระยะ:** `POST_NEAR` + `POST_ONP0` + `POST_ORBIT_1..4` ⇒ **"เห็น / ไม่เห็น / ไม่ได้ตรวจ"**
   - **(ค) การเลือก:** ผลคลิกซ้าย 3 ครั้ง + `Tab` 3 ครั้ง ที่จุด `P0` (ทั้ง W3 และ POST-A) ⇒ **"พาเนลเปิดและอ่านได้ว่า ... " / "พาเนลไม่ขึ้นเลยทุกครั้ง" / "ไม่ได้ตรวจ"**
4. **ตอบเป็นตารางเหตุการณ์:** `t` (สัมพัทธ์กับ `T0`) · เห็นอะไร · ที่พิกัดไหน (อ่านจาก HUD) · ภาพไฟล์ไหน — **หนึ่งบรรทัดต่อหนึ่งเหตุการณ์**
5. **NC-1 / NC-2 / NC-3 ตอบครบสามข้อ** ("ไม่ได้ตรวจ" เขียนออกมาเป็นตัวอักษรได้ แต่ห้ามเว้นว่าง)
6. **ตารางสีป้ายชื่อครบทุกป้ายทุกภาพ full-res** (ดูบล็อก PLAYBOOK ข้อ 13)
7. **คำตอบข้อ clapper:** บรรทัดแชตปรากฏบนจอไหม · `T0` อยู่ที่ `t` เท่าไรในวิดีโอ
8. **NO-CRASH / CRASH verdict** (ตัดสินด้วยคลิกขวาลาก)
9. 🔴 **ใบปิดด้วยผลลบได้เฉพาะรอบที่ *คุณ Panya เห็นเอง* + มีวิดีโอต่อเนื่อง** (`UNATTENDED_RULES.md` — รอบ unattended ปิดผลลบไม่ได้)
10. 🔴 **ชั้นนี้ตอบไม่ได้:** เฟรมออกจากเซิร์ฟเวอร์จริงไหม · ไบต์ตรง pin ไหม · พิกัดที่ส่งคือ `P0` จริงไหม

🔴 **ถ้าชั้น (1) ไม่ผ่าน (sha ไม่ตรง pin · พิกัดที่ decode ได้ไม่ใช่ `P0` · มี `*_no_reply` · console ขึ้น label เลนอื่น) ⇒ รอบเป็น NO-RESULT ทางเทคนิค ห้ามอ่านจอเป็นผลใด ๆ แม้จะเห็นของหายชัด ๆ**

---

### nonclaims (ติดไปกับผลทุกกรณี ไม่ว่าบวกหรือลบ — **ห้ามตัดทิ้ง**)

① **ไม่พิสูจน์กลไกฝั่งไคลเอนต์แม้แต่นิดเดียว** — "ช่อง actor" / "id ชนกัน" / "hash ตำแหน่ง" / "ลำดับใน list" **ไม่มีหลักฐาน static แม้แต่บรรทัดเดียวในโปรเจกต์** ⇒ **ชื่อใบใช้คำว่า `SLOT-DISPLACEMENT` เป็นชื่อเรียกปรากฏการณ์ ไม่ใช่คำอธิบายกลไก**
② **ไม่ได้วัด identity/id ของอะไรเลย** — ไม่ claim ว่า identity band `0x00A00001` ของ probe ชนกับ actor identity `0x2001` ของ NPC
③ 🔴 **"คลิกไม่ติด / พาเนลไม่ขึ้น" ไม่เท่ากับ "ไม่มีอะไรอยู่ตรงนั้น"** — สิ่งที่มองไม่เห็น **เล็งคลิกไม่ถูกโดยธรรมชาติ** และ `Tab` ก็ไม่มีใครพิสูจน์ว่ากวาดทุก actor ⇒ **แถว N1 อ่อนกว่าที่ตาเห็นเสมอ**
④ **ไม่ได้พิสูจน์ว่าตัวที่หายคือ `Navy Transfer`** เว้นแต่ `PRE_PANEL` อ่านชื่อออกจริง — R3 ระบุด้วย **ระยะ** ไม่ใช่ป้าย · ถ้ารอบนี้พาเนลไม่ขึ้นชื่อ ให้เขียนว่า **"ระบุจากตำแหน่งเท่านั้น"**
⑤ **รอบเดียวไม่ใช่คุณสมบัติของไคลเอนต์** — จนกว่าจะทำซ้ำได้ · **และการทำซ้ำของใบนี้ไม่ปิดข้อผูกพันการทำซ้ำของ `GT-030-R3` ซึ่งเป็นคนละคำถาม**
⑥ **ไม่ตอบอะไรเลยเรื่อง `ตาย!` / `HP 0` / `LV 1`** ที่ `GT-030-R3` เห็น — **นั่นคือ `RE-071` (งาน static)** ⇒ ถ้ารอบนี้เห็นข้อความหรือพาเนลแบบนั้นอีก **จดเป็นข้อสังเกต ห้ามใช้เป็นข้อสรุปของใบนี้**
⑦ **ตัวคุม NC-1 ไม่ใช่ตัวคุมที่ต่างกันตัวแปรเดียว** (คนละเฟรมคนละทรง) และ **ตัวคุมที่สะอาดจริง (`SPAWN_BARE` ที่พิกัดว่าง) ยังไม่มีในโปรเจกต์** — ต้องกิน 1 สล็อตและ chief ต้องออกแบบ
⑧ **ผลครอบเฉพาะแนวและกรอบกล้องที่ถ่ายจริง** — อะไรที่อยู่นอกเฟรม/นอกแนว = **non-observed ไม่ใช่ absent**
⑨ **ขอบล่างของ transient = ช่วงหนึ่งเฟรมของวิดีโอที่อัดจริง** (30 fps ≈ 0.033 วิ) · สั้นกว่านั้นอยู่นอก claim · ถ้า `ffprobe` พบเฟรมหาย **ขอบล่างคือช่องว่างที่วัดได้จริง ไม่ใช่ `1/fps`**
⑩ **ห้ามอ้างตัวเลขข้ามสองนาฬิกา (วิดีโอ↔สาย) เป็นคำตัดสิน** — offset ต่างกันทุกบูต (`0.0/0.58/1.82` วิ) ⇒ **`0.6 วิ` ของ R3 เป็นตัวเลขที่บวก error ขนาดไม่รู้ค่าอยู่ข้างใน ห้ามยกมาเป็นเกณฑ์**
⑪ **ไม่มีใครวัดว่าคลิกซ้าย / `Tab` / ล้อเมาส์ ยิงไบต์อะไรออกสายหรือไม่** — จึงบังคับให้จดเวลาของทุกคลิกและทุกการซูม
⑫ **ระยะเรนเดอร์ของ client = [UNKNOWN]** — ใบนี้ลดตัวแปรด้วยการยืนติด landmark **ไม่ใช่การวัดระยะ**
⑬ **ground Z ไม่ได้ตรวจ** — ตัวจม/ลอยพื้นไม่ falsify อะไร
⑭ **เฟรม / mask / identity band / การวางตำแหน่ง ทั้งหมดเป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว ไม่เคยเผยแพร่ และกู้ไม่ได้ตลอดกาล — **ไม่มี capture ของ remote human player แม้แต่เฟรมเดียวในคลังทั้งโปรเจกต์** · **ตาราง placement ใน `pf_login_game_server_v141.py` ก็เป็นของเรา**
⑮ **สีอ่านด้วยตาจากภาพ ไม่ได้วัดค่าพิกเซล** ⇒ **ไม่ claim ค่า RGB/hex ใด ๆ** · `evidence_layer` ของทุกแถวที่ออกจากใบนี้คือ **`eye`**
⑯ **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับอาจเป็น client คนละ build/ภูมิภาค** ⇒ "ต่างจากภาพต้นฉบับ" ยังไม่เท่ากับ "ของเราผิด"
⑰ **`OBSERVER_CONFIRMED` เป็นขั้นตอน ไม่ใช่หลักฐาน** — มันบอกว่า "ผู้เทสยืนยันว่าสิ่งที่ผู้ช่วยเขียนตรงกับที่เธอเห็น" **ไม่ได้บอกว่าสิ่งนั้นเป็นความจริงเรื่องไคลเอนต์**


---

### สถานะปัจจุบัน — ผลรอบแรก (จ็อบ 1167/1168/1169 · attended · `OBSERVER_CONFIRMED: 2026-08-25T21:4x+07:00`) คัดมาคำต่อคำจากจดหมายผล

| ค่า | สถานะจริงหลังรอบแรก | ทำไมหลักฐานที่มีถึงตัดไม่ได้ |
|---|---|---|
| **แทนที่ (replace)** | 🟡 **ยังไม่ถูกตัด** | หลักฐานคือ *"คลิกซ้าย/`Tab` ที่ `P0` แล้วไม่มีอะไรถูกเลือก"* — 🔴 **แต่เรารู้อยู่แล้วว่า actor ของเราเองก็คลิก/`Tab` ไม่ติด** (จดหมาย §④ ยืนยันซ้ำในรอบนี้เอง) ⇒ ถ้า actor ของเรามาแทนที่ NPC จริง **ผลที่ได้จะหน้าตาเหมือนกันเป๊ะ** · และการคลิกเกิดที่ `+92.8` **หลังศพหายไปแล้ว 32 วินาที** |
| **บังทับ (occlusion)** | 🟡 **ยังไม่ถูกตัดแม้แต่ครึ่งเดียว** | เฟรมพื้นว่างที่ `+92.8` อยู่ **หลังโมเดลของเราหายไปแล้ว 32.4 วินาที** ⇒ ตัวที่ถูกกล่าวหาว่า "บัง" ไม่อยู่ในฉากตอนวัด ⇒ **ทั้งสามสมมติฐานทำนายพื้นว่างเปล่าตรงกันหมด** = อำนาจแยกแยะเป็นศูนย์ · ตัวคุมมุมกล้อง (`W2`) ก็ไม่ได้ทำ |
| **despawn** | 🟡 **ยังไม่ถูกยืนยัน** | ใบเขียนเองว่าเป็นแถวที่อ่อนที่สุดโดยธรรมชาติ: *"คลิกไม่ติด ไม่เท่ากับ ไม่มีอะไรอยู่ตรงนั้น"* — 🔴 **และประโยคนี้ใช้กับแถว "แทนที่" ได้เท่ากันทุกตัวอักษร ฉบับแรกวางมันไว้แถวเดียว** |

🔴 **บทเรียนที่ต้องอยู่เหนือใบนี้:** **ตัวคุมที่วัดถูกต้องแต่วัด *ผิดเวลา* ให้ผลลบที่อ่านเหมือนผลลบจริงทุกประการ**
ผู้เทสยืนยันด้วยตาแล้วจริง และสิ่งที่เธอเห็นก็จริงทุกคำ — **แต่ `OBSERVER_CONFIRMED` รับรอง *สิ่งที่เห็น* ไม่ได้รับรอง *ว่าเห็นตอนที่มันมีความหมาย***

🔴 **ตัวคุมที่ "ไม่ได้ทำ" มีอย่างน้อยสามตัว ไม่ใช่ตัวเดียวอย่างที่ฉบับแรกเขียน** (ล็อกยืนยันเอง: `TargetPosVital` ใบแรก = `+82.5` ⇒ ผู้เทสยืนนิ่งตลอด `W1`–`W5`):
- **`W2`** มุมกล้อง (`+10..+20`) — ⇒ ยกไปใบ **`GT-074`**
- **`W3`** เดินเข้าไปดูใกล้ + คลิก/`Tab` ที่ `P0` **ในช่วง `+20..+29`** (ใบสั่งข้อ 13) — ⇒ ยกไปใบ **`GT-074` SESSION 2**
- **`POST-A`** ยืนทับพิกัด `P0` (`X -9140 Y -2780`) — ผู้เทสอยู่ `Y -2,537` ตลอดรอบ
⇒ 🔴 **ห้ามเขียนว่า "การเปลี่ยนมุมกล้อง/การเข้าไปใกล้ไม่ทำให้ NPC โผล่กลับมา"** — เขียนได้แค่ **"ไม่ได้ตรวจในหน้าต่างที่มีความหมาย"**

---

**ลิงก์:**
- ผลรอบแรกฉบับเต็ม (wire dump, ที่มา `GT-030-R3`, protocol เต็มของรอบ, ตารางตีความผล N1-N8, ข้อสังเกต R169, ข้อแก้ไข/ถอนคำที่เคยเขียนผิด, ข้อสังเกต `Z=0` เหนือน้ำ): `archive/GT-072_history_20260901.md`
- จดหมายต้นทางผลรอบแรก: `notes_to_chief\consumed\20260825_2145_GT072-RESULT-occlusion-and-replace-both-fail-plus-Z0-over-water.md`
- ตัวคุมที่ยังไม่ได้ทำ (`W2`/`W3`/`POST-A`) ถูกยกไปรันที่ใบ `GT-074` (`GT-074` มี protocol ของตัวเองแล้ว ไม่ต้องย้อนมาอ่าน steps เดิมของใบนี้) — `GT-074` ยังไม่ปิด `GT-072` ด้วยตัวเอง สถานะของ `GT-072` เป็นของ chief ตัดสินเท่านั้น

---

## GT-074 OCCLUSION-CAMERA-ANGLE-CONTROL-001 [attended, in-game]: หลัง `SPAWN_BARE` ทับพิกัด `P0` — **NPC `Navy Transfer` โผล่กลับมาให้เห็นจากมุมกล้องอื่นหรือไม่** (ตัวคุมมุมกล้อง `W2` ที่รอบแรกของ `GT-072` ไม่ได้ทำ)  [🟢 **PENDING — attended · รันได้บน `main` ปัจจุบัน ไม่รอ merge ไม่รอ CI ไม่รอเจ้าของ · ศูนย์สล็อต** · เปิดใบโดย chief R170 (2026-08-25 ~22:2x +07:00 · session `2ilw5p`) ตามผลรอบแรกของ `GT-072` §② · เขียนใบโดย `pf-queue-author`] -- moved to `tickets/GT-074.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `ec26p6` 2026-09-06T21:18+07:00)
## 🆕 GT-076 POPULATION-FULL-001-ACTOR-CEILING-STAIRCASE-001 [attended, in-game]: ไคลเอนต์รับ actor ใน RuntimeRes collection **เดียว** ได้กี่ตัว - เดินบันไดซ้อนของสำมะโน `bg0001` 3 -> 20 -> 60 -> 115  [🔴 **BLOCKED — รอ merge ก่อน** · **`BLOCKED-ON-WIRING` จบแล้ว (chief R173 ต่อสายให้ + ใส่ `--world-census-actors`) ดูบล็อก "แก้ไข R173" ท้ายใบ** · เปิดใบโดย LANE-A 2026-08-25 ~23:1x (+07:00) ตาม `CHARTER-01` §④ BUILD-001 · เขียนใบโดย `pf-queue-author`] -- moved to `tickets/GT-076.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `cm9v9y` 2026-09-06T17:10+07:00)

## GT-078 M1-V1-ACCEPTANCE-PORT-ROYAL-POPULATION-115-001 [attended, in-game]: บูตเซิร์ฟเวอร์ **โดยไม่มีแฟล็ก scenario แม้แต่ตัวเดียว** แล้วเจ้าของเดินทั่ว Port Royal — **เมืองมีคนอยู่จริงหรือไม่ และขอ... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕 GT-079 SCENE-278-ENTRY-AND-STAGE-EYECHECK-001 [attended, in-game]: ไคลเอนต์ตัวนี้ **เข้า** ฉาก 278 (`Bg1177`) ได้จริงหรือไม่ · แมพที่ขึ้นคือแมพไหน · และสิ่งที่ยืนอยู่คือ **เวทีกว้าง เรียบ โล่ง** อย่างที่เจ้าของขอหรือไม่  [~~🔴 **BLOCKED — BLOCKED-ON-WIRING** (ยังไม่มีเส้นทาง runtime ไร้แฟล็กที่ส่ง `scene_id=278`)~~ 🟢 **READY — เหตุบล็อกเดิมหมดแล้ว, แก้โดยเจ้าของใบ LANE-A รอบใหม่ 2026-09-01T05:xx+07:00:** วัดบน `main` รอบนี้ (ไม่ใช่การเดา) — `world_scene_entry.resolve_entry` ถูกเรียกจริงสองจุดใน `runtime.py` (login handler) มาแล้วอย่างน้อยหนึ่งรอบก่อนหน้านี้ (`world_scene_entry.py`'s docstring ของตัวเองยังเขียนผิดว่า "nothing calls it yet" — แก้แล้วรอบนี้) และ `login_entry_allowed` ของฉาก 278 เป็น `true` มาโดย **default** (`DEFAULT_LOGIN_ENTRY_ALLOWED`, ฟิลด์ไม่เคยถูกปักมาก่อน) อยู่แล้ว — รอบนี้ปักเป็น `true` **อย่างชัดเจน** พร้อม safety case เต็มในทะเบียน (`login_entry_allowed_because`) แทนค่า default ที่ซ่อนอยู่ ไม่ใช่การเปลี่ยนพฤติกรรม · เปิดใบโดย LANE-A 2026-08-26 ~01:2x (+07:00) ตาม `CHARTER-02` §⑤ BUILD-002 สไลซ์ 1 · ร่างใบโดย `pf-queue-author` · ถ้อยคำเดิมของหัวใบ (ก่อนแก้) เก็บไว้ขีดฆ่าด้านบน]

ATTENDED: ขั้น 0: LOCK_GAME · boot stamp (+07:00 · teardown ปฏิเสธ stamp เก่ากว่า 420 นาที) · preflight จอว่าง (เจอหน้าต่าง elevated = ABORT) · เทียบ sha canonical · copy DB · จดแถว character_positions เดิม (scene_id, scene_seq, x, y, z, heading) = ใบเสร็จทางกลับบ้าน ไม่มีบรรทัดนี้ห้ามเริ่ม -> สตาร์ตเซิร์ฟเวอร์ก่อน client ทีหลังเสมอ (ฆ่า client กลางคัน = restart server ก่อนเปิดตัวใหม่ ไม่งั้นค้าง "connecting") -> เริ่มอัดวิดีโอ 30 fps ลง evidence_video\ (ไม่ได้อัด = NO-RESULT) -> เข้าเกม: เลือกเซิร์ฟเวอร์ -> dialog PVP ปุ่มซ้าย -> ช่องแรก -> ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง (ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด) · ห้ามพิมพ์อะไรทั้งรอบ (ช่องแชทไม่โฟกัส = ฮอตคีย์)
ATTENDED: บนจอตามลำดับ ห้ามสลับ: จับเวลากดปุ่มเข้าเกม -> เห็น HUD เป็นวินาที + บรรยายหน้าโหลดหนึ่งประโยค (C4) · ยืนนิ่ง จด HUD X/Y/Z และ **คัดชื่อแมพบน HUD/มินิแมพมาทั้งบรรทัด** (C1) · ยืนนิ่ง 30 วิ มือออกจากคีย์บอร์ด จด Z ที่ 0/10/20/30 วิ (C2) · คลิกขวาค้างลากกวาดกล้องรอบตัวหนึ่งรอบ ค้างทุก ~90 องศา มุมละ 4 วิ (A/B/C/D) จดของบัง/พื้นเรียบ-เนิน/สี/นับ actor ต่อมุม (C3, C5) · แตะ W ครั้งเดียวจด T_STEP แล้วจด X/Y/Z ซ้ำ · เดิน W/S/A/D ทิศละ ~10 วิ · VP-1 เดิน +X 600-800 หน่วยแล้วกวาดกล้องมุมเดิมนับซ้ำ · ภาพนิ่ง full-res >=5 ใบ (ห้ามกดคีย์ในหน้าต่างเกมเพื่อถ่าย ห้าม resize ลง ซูมเท่ากันทุกใบ) · อยู่ครบ 10 นาทีจากที่เห็น HUD (C6) · ห้ามใช้ Q/E ทั้งรอบ
ATTENDED: ค่าที่ต้องอ่าน/จด: บรรทัดคอนโซล `WORLD_SCENE scene_id=278 seq=0 model=Bg1177 name=beach_football_field_(TEST) spawn=(-13270.058,22794.273,-2492.769) sent_before=NO population=none save=0 marker=0 return_ticket=REQUIRED` เป๊ะทั้งบรรทัด (ไม่มีบรรทัดนี้ หรือ scene_id ไม่ใช่ 278 = หยุด N6) · เฟรมเข้าฉาก: label + pc bytes + framed bytes + frame_sha256 + scene_id ที่ decode จาก u16tag 0x12 ต้องอ่านได้ 278 (0x0116) และ scene_seq = 0 · พิกัด f32 ที่ decode ได้เทียบพิน (-13270.058, 22794.273, -2492.769) ห้ามใช้ HUD เป็นฐานคำนวณ · HUD X/Y ตอนเข้าแมพต้องอยู่ในกรอบ x [-14551.5, -8356.5] y [21667.4, 23876.8] นอกกรอบ (เช่นแถว -9239, -2830) = หยุด N6 · ErrorData มีไหม จดเลขเป๊ะ + หลังเฟรมไหน + กี่วินาทีหลัง T_ENTER (28317 = 0x6E9D parse-failure echo ห้ามอ่านเป็น "รายงานจำนวน") · census บรรทัด [G>] ทั้งไฟล์ ต้องไม่มีบรรทัดจาก npc_wire หรือ world_population
ATTENDED: ตัดสินที่ชั้น client-observable ชั้นเดียว (ชั้น wire/DB ตอบ C1-C6 ไม่ได้แม้ข้อเดียว และ "ส่ง 278 แล้วไม่มี ErrorData" ไม่ได้แปลว่าไคลเอนต์โหลด Bg1177): ตอบ C1-C6 ข้อละหนึ่งประโยค ห้ามยุบรวม ไม่ได้ดูให้เขียนว่า "ฉันไม่ได้ดูข้อนั้น" · ชื่อแมพบน HUD/มินิแมพคือสิ่งเดียวที่แยกการอ่านค่าสี่ทาง (n_ID / n_MARKER / n_CLINE_TYPE / ลำดับแถว) ⇒ ชื่อตรง Bg1177 = N1 PASS · เข้าได้แต่ชื่อแมพอื่น = N1b PASS ผลที่แพงที่สุดของใบ · เข้าได้แต่ไม่เรียบ/มีของบัง/สีไม่ขาว = N2 PARTIAL · ไม่มีพื้น = N3 PASS · ไม่ถึงสถานะเล่นได้ = N4 PASS ผลลบมีค่าเท่าผลบวก · traceback ก่อนมีไบต์ออกสาย = N5 NO-RESULT ส่งคืน chief · ห้ามรายงานว่า FAIL ห้ามเปลี่ยนพิกัด/ฉากเองเพื่อให้บูตรอด ห้ามชี้สาเหตุ · NO-CRASH ใช้คลิกขวาค้างลากเท่านั้น จดนาที 2/5/10 แยกสามบรรทัด · จดสีป้ายชื่อทุกป้ายทุกภาพ full-res (ไม่มีให้เขียนคำว่า "ไม่มี") จดสีอย่างเดียวห้ามสรุปสาเหตุ · ปิดใบต้องมี OBSERVER_CONFIRMED:
ATTENDED: บูตด้วย `py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch` (exit 0 -> `git checkout <BOOT_COMMIT>` · exit 3 = ห้ามบูต ใบอยู่ BLOCKED) + ด่านก่อนบูตห้าข้อ โดย `git grep -n 'world_scene_travel' <SHA> -- src/pirateforce_foundation/runtime.py src/pirateforce_foundation/app.py` คือด่านปลด BLOCKED (ไม่มี hit = ห้ามบูต) -> `py -3 -u -m pirateforce_foundation.app --db state\run_gt079.sqlite3 --export-events <CHIEF_FILLS_THIS_IN_AT_WIRING_TIME>` 🔴 ยังมี placeholder = BLOCKED ห้ามบูต ห้ามเดาแฟล็กเอง ห้ามใส่แฟล็ก hypothesis/scenario ตัวอื่นแม้แต่ตัวเดียว ห้ามพ่วง GT-076 · ทางเข้าฉาก 278 มีทางเดียวคือ staged GM account (`config/gm_login_scene.json` scene_id=278) หรือ GM `/warp 278` ไม่ใช่ล็อกอินปกติ · DB สำเนาเท่านั้น `state\run_gt079.sqlite3` (บูตยืนยันใช้ `state\run_gt079_confirm.sqlite3` · หนึ่งสำเนาต่อหนึ่งบูต) ห้ามเปิด canonical เทียบ sha กับ CANON_SHA.txt ก่อน-หลัง · teardown ภายใน 420 นาที + ทางกลับบ้าน `home_return_position()` แล้ว query แถวให้เห็น scene_id = 1

> 🔢 **เรื่องเลขใบ:** ตัวนับเป็น **ชุดเดียวร่วมกับ `CLIENT_RE_QUEUE.md`** — prefix สองแบบ ตัวนับเดียว
> `GT-074` (chief R170) · `RE-075` · `GT-076` (BUILD-001) · **`RE-077`** ถูกใช้แล้วทั้งหมด · grep ยืนยันก่อนจอง: `GT-079`/`RE-078` = **0 hit ทั้งสองไฟล์** ⇒ **ใบนี้คือ `GT-079`** · **เลขว่างถัดไป = 079**
> 🔴 **ใบ `GT-030` · `GT-030-R3` · `GT-072` · `GT-074` · `GT-076` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ** — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

> ### ทางเข้า (เพิ่มรอบนี้ — ไม่มี production path ใดเขียนแถว character ให้ชื่อฉาก 278 เอง)
> ไม่มีบูตแบบ "ธรรมดา" ใดส่ง `scene_id=278` เอง (คำถามเดิมของหัวใบข้อ "แมพไหน" ยังเปิดอยู่เหมือนเดิม — นี่คือ
> เรื่อง *เข้าถึงได้* ไม่ใช่เรื่อง *แมพที่ขึ้นคืออะไร*) เข้าได้เฉพาะ staged GM account
> (`config/gm_login_scene.json`, scene_id=278) หรือ GM `/warp 278` — กลไกเดียวกับที่ฉาก 3/4/5/6/7/8/9/10/11/130
> ใช้อยู่แล้ว (`gm/login_scene_admission.py::stageable_scene_ids()`) ไม่ใช่ "ล็อกอินปกติแบบไม่มีแฟล็กเข้าฉากนี้
> เอง" อย่างที่ถ้อยคำเดิมของใบ (2026-08-26) อาจสื่อ — ดู `login_entry_allowed_because` ในทะเบียน
> (`scenarios/world_scene_registry_001.json` แถว `n_id: 278`) สำหรับ safety case เต็ม

> 🎯 **MILESTONE:** ครึ่งแรกของ **`M2` "ออกจากเมืองได้"** = เซิร์ฟเวอร์ **`v2`** (`CHARTER-02` §⑤ · กำหนด **26 ส.ค. 23:59**)
> 🔴 **ใบนี้ไม่ปิด `M2` และไม่ปล่อย `v2`** — ครึ่งที่เหลือ (การ *ย้าย* ตัวละครที่ live อยู่) คือ **`RE-077` ซึ่งยังเปิดและยังไม่มีคำตอบ** · และ `M2` ปิดด้วยตาเจ้าของเท่านั้น

---

### 🔴🔴 อ่านก่อนทุกบรรทัด — **ทุกคำตอบของหกข้อนี้คือ "ผล" ไม่มีข้อไหนเป็น "ความล้มเหลว"**

- ไคลเอนต์ **ไม่เคยได้รับ `scene_id` ค่าอื่นนอกจาก 1 กับ 2 เลยตลอดประวัติโปรเจกต์** ⇒ **การที่มันปฏิเสธ 278 เป็นผลที่แพงกว่าการที่มันรับ** เพราะมันเปลี่ยนดีไซน์ของ `M2`–`M6` ทั้งแถบ
- **ห้ามรายงานว่า FAIL · ห้าม "ไปแก้ให้มันเข้าให้ได้" กลางรอบ · ห้ามเปลี่ยนพิกัด/ฉากเองเพื่อให้บูตรอด**
- **"ไม่ขาว" ไม่ใช่ตก** — สีเป็น **ค่าที่จด** แล้วส่งให้เจ้าของตัดสิน (`RE-073` ปิดไปแล้วด้วยผลว่าไม่มีฉากไหนในสามตัวเลือกที่ขาวจริง)

### 🔴🔴 และข้อที่ใบนี้ตอบได้คนเดียวในโปรเจกต์ — **แมพที่ขึ้นคือแมพไหน**
สาย A ยืน `BUILD-002` อยู่บน **การอ่านค่าแบบหนึ่ง** ว่า `scene_id` บนสาย = คอลัมน์ `n_ID` ของ `CONSTDATA_TH__SCENE_NAME`
🔴 **มันยังไม่ใช่ข้อสรุป** — แถว 1 กับ 2 เป็นสองในสิบสองแถวที่ `n_MARKER` และ `n_CLINE_TYPE` **เท่ากับ `n_ID` พอดี** และยังเป็นแถวข้อมูลที่ 1 และ 2 ของไฟล์ด้วย ⇒ **มีการอ่านค่าคู่แข่งสามแบบที่เข้ากันได้กับหลักฐานทั้งสองชิ้นเท่ากันเป๊ะ:**

| ถ้าฟิลด์นี้คือ… | ค่าที่ควรส่งไป `Bg1177` | ⇒ ส่ง `278` แล้วจะเจอ |
|---|---|---|
| `n_ID` (ที่สาย A ใช้) | **278** | `Bg1177` สนามฟุตบอล |
| `n_MARKER` | **ไม่มีค่าเลย** (`Bg1177` มี marker = 0) | แมพอื่น หรือไม่โหลด |
| `n_CLINE_TYPE` | `4294967295` | แมพอื่น หรือไม่โหลด |
| ลำดับแถวในไฟล์ | **252** | แมพอื่น (แถวที่ 278 ของไฟล์) |

⇒ 🎯 **ชื่อแมพที่ HUD/มินิแมพแสดงในข้อ `C1` คือสิ่งที่แยกสี่ทางนี้ออกจากกัน** · **คัดตัวอักษรมาทั้งบรรทัด ห้ามสรุปว่า "ก็แมพเทสแหละ"**

---

### ที่มา — **พินไว้หมดแล้ว ห้าม re-derive ระหว่างรอบ**
ทุกค่าอยู่ใน `scenarios/world_scene_registry_001.json` (แถว `n_id: 278`) และถูกตรวจโดย `tests/test_world_scene_travel.py`

| ของ | ค่า |
|---|---|
| ปลายทาง | `n_ID` **278** · model **`Bg1177`** · ชื่อที่นักพัฒนาตั้ง **`beach football field (TEST)`** |
| `s_IMAGENAME` | **`BgNull`** (237 จาก 271 แถวใช้ค่านี้ — **เป็นค่าปกติ ไม่ใช่ธงแดง**) |
| `.npc` sha256 | `7dbe6618c21edbc3d23da2789b9b799e9a035f2c2dd91a3a889fb39cd524bfc2` · **9 placement / 26 definition** |
| **จุดยืนที่พินไว้** | **`(-13270.058, 22794.273, -2492.769)`** = **native placement index 4 (`Mob_set_02 04`)** — จุดที่นักพัฒนาวางของไว้จริง |
| จุดที่ **ถูกยกเลิก** | ~~`(-12571.737, 22893.286, -2492.769)` ค่าเฉลี่ยของเก้าจุด~~ — ห่างจากจุดที่ใกล้ที่สุด **705 หน่วย** = จุดเดียวในฉากที่ไม่มีใครวางอะไรไว้เลย · เก็บไว้ในพินเป็นประวัติ |
| ขอบเขต | x `[-14551.545, -8356.516]` · y `[21667.371, 23876.793]` ⇒ **6195.03 x 2209.42** หน่วย (ถ้านับเฉพาะ 6 record ที่มีชื่อชุด: **5548.27**) |
| z ของเก้าจุด | ต่างกันไม่เกิน **0.00195** หน่วย · **ทั้งโปรเจกต์มีแค่ 6 ฉากจาก 251 ที่แบนขนาดนี้** ⇒ เป็นสัญญาณจริง ไม่ใช่ค่า default ของตัวถอด |
| 🔴 คอลัมน์เตือน | **`n_SAVE = 0`** · **`n_MARKER = 0`** · **`n_CAMERA_TYPE = 0`** (มีแค่ 10/271 แถว) · **`n_LIMIT_HEIGHT = 0`** (สองฉากที่วัดแล้วเป็น 30000) — **ทั้งสี่ยังไม่มีใครวัดผลของมัน นี่คือรายการที่ต้องเปิดดูตอนมันพัง** |

🔴🔴 **ข้อจำกัดของหลักฐานพื้น:** *"เก้าจุดกระจาย 6,195 หน่วยแล้ว z เท่ากัน"* เป็นหลักฐานเรื่อง **ที่ที่นักพัฒนาวางมอน** ไม่ใช่การวัด **พื้น** · ไฟล์ `.npc` **ไม่บอกอะไรเลยเรื่อง mesh พื้น กำแพง น้ำ ฟ้า แสง หรือสี** ⇒ **ตาของผู้เทสคือสิ่งเดียวที่ตัดสิน**
🔴 **บรรทัดฐานเดียวที่มี:** ฉากที่ไม่ใช่ default ที่โปรเจกต์นี้เคยเรนเดอร์มีฉากเดียว = `scene_id 2` (`SCENE-001` · `docs/EXPERIMENT_LEDGER.md:31`) **และครั้งนั้นอยู่หลังแฟล็ก** · **ฉาก 278 ไม่เคยถูกส่งให้ไคลเอนต์ตัวไหนเลย**
🔴 **คำขอของเจ้าของ (คำต่อคำ ~20:1x +07:00 · `20260825_2020_PANYA-REQUEST-*`):** *"ฉันอยากได้แมพที่เป็นแมพเทสโมเดลจริง ๆ กว้าง สีขาวล้วน พื้นเรียบ ไม่มีเอฟเฟกใด ๆ"*

---

### objective (claim เดียว)
**ไคลเอนต์ตัวนี้ *เข้า* ฉาก 278 จนถึงสถานะเล่นได้หรือไม่ · แมพที่ขึ้นคือแมพไหน · และสิ่งที่ผู้เล่นยืนอยู่ใช้เป็นเวทีได้หรือไม่**
- "เข้าได้" = **ทั้งสองชั้น**: (ชั้น 1) เฟรมที่มี `scene_id=278` ออกสาย ไม่มี `ErrorData` ตามมา การสื่อสารเดินต่อ · (ชั้น 2) คนหน้าจอเห็นแมพ เดินได้ ไม่ค้าง ไม่หลุด
- 🔴 หกข้อด้านล่างคือ **หกช่องอ่านของ claim เดียวกัน** ไม่ใช่หกใบ · ข้อ 1/2/6 = *ใช้ได้จริงไหม* · ข้อ 3/4/5 = *ใช้ได้ในสภาพไหน*
- 🔴 **ไม่ใช่ใบเรื่องการย้ายฉากขณะ live** (นั่นคือ `RE-077`) และ **ไม่ใช่ใบเรื่องประชากร** (`population_source(278)` คืน `None` โดยตั้งใจ)

### 🔴🔴 ด่านตาหกข้อ — ตอบข้อละ **หนึ่งประโยค**

| # | คำถาม | ✅ เขียนแบบนี้ | ❌ เขียนแบบนี้ | 🔴 หมายเหตุบังคับ |
|---|---|---|---|---|
| **C1** | ไปถึงสถานะเล่นได้ไหม **และ HUD บอกว่าแมพอะไร** | *"เข้าถึงสถานะเล่นได้ · HUD เขียนว่า `<คัดตัวอักษรทั้งบรรทัด>`"* | *"ไม่เข้า: `<error dialog คำต่อคำ>` / หลุดนาทีที่ `<t>` / ค้างที่หน้าโหลด"* | 🔴 มี `ErrorData` ให้จดเลขเป๊ะ · **`28317` = `0x6E9D` = ไคลเอนต์สะท้อน class id ของ envelope ที่ parse ไม่ผ่าน ห้ามอ่านเป็น "รายงานจำนวน"** · 🎯 **ชื่อแมพคือตัวแยกการอ่านค่าสี่แบบข้างบน** |
| **C2** | มีพื้นรองรับที่จุดที่พินไว้ไหม | *"มีพื้น: ยืนนิ่ง 30 วิ Z บน HUD ไม่ขยับ เห็นผิวพื้นใต้เท้า"* | *"ไม่มีพื้น: ตกลงเรื่อย ๆ / ลอยในความว่าง / อยู่ในน้ำ"* | จด **X/Y/Z จาก HUD** ตอนเข้าแมพ · ที่ +30 วิ · และหลังก้าวแรก |
| **C3** | กว้าง-เรียบ-ไม่มีของบังไหม **และสีอะไร** | *"กว้าง เรียบ ไม่มีของบังทั้งสี่มุม · สีที่เห็นคือ `<สี>`"* | *"แคบ / เป็นเนิน-ขั้น / มีของบัง `<อะไร>` ที่มุม `<ไหน>`"* | 🔴 **สี = ค่าที่จด ไม่ใช่เกณฑ์ผ่าน/ตก** · อ่านสีจากภาพนิ่ง full-res เท่านั้น |
| **C4** | `BgNull` ทำให้เกิดข้อบกพร่องที่เห็นได้ไหม | *"ไม่มีอะไรผิดสังเกต · หน้าโหลดใช้เวลา `<n>` วินาที"* | *"จอดำ / ไม่มีภาพโหลด / ค้าง `<n>` วินาที"* | จับเวลาจาก **คลิกปุ่มเข้าเกม** ถึง **เห็น HUD** · **ทั้งสองคำตอบเป็นผล** |
| **C5** | เก้า placement โผล่เป็น actor จริงไหม | *"เห็น 0 ตัวจากทุกมุมที่กวาด"* (**คาดไว้แบบนี้**) | *"เห็น `<N>` ตัว ที่ `<ทิศ/พิกัด>` หน้าตา `<บรรยาย>`"* | 🔴 ตัวเลขเป็น **ขอบล่าง** เสมอ — เขียน *"ไม่เห็นจากมุมที่กวาด"* **ห้ามเขียนว่า "ไม่มี"** |
| **C6** | เดินได้ไหม และอยู่ครบ 10 นาทีไหม | *"เดินได้ทั้งสี่ทิศ · อยู่ครบ 10:00 บนนาฬิกาวิดีโอ ไม่หลุด"* | *"เดินไม่ได้ / หลุดที่ `<mm:ss>` / ค้างที่ `<mm:ss>`"* | กฎข้อ 3 ของเวอร์ชัน (`CHARTER-02` §⑤) · **ตัดสินด้วยนาฬิกาวิดีโอ** |

---

### 🔴🔴 PRECONDITION — **BLOCKED-ON-WIRING · ยังบูตไม่ได้ ห้ามบูต**

**สิ่งที่ยังไม่มี และเป็นงานของ chief ไม่ใช่ของผู้เทส:** `world_scene_travel` **ยังไม่ถูกต่อเข้า `runtime.py`**

🟢 **ข่าวดีที่ลดงานลงมาก (สาย A ไปเปิดโค้ดมาเองในรอบ `jjxgz3`):** **เส้นทางปกติไม่มีการ์ด `scene_id` เลย**
- `legacy_bridge.start_game` (`legacy_bridge.py:47-62`) อ่าน `p.scene_id` จาก **แถวตำแหน่งของตัวละคร** แล้วส่งผ่าน `make_actor_attr_with_name` ตรง ๆ · `store.py:266` รับ `0..0xFFFF` อยู่แล้ว
- 🔴 **การ์ดสามชั้นที่บันทึกไว้ใน `RE-073` อยู่บนเลนหัววัดทั้งหมด ไม่ขวางใบนี้:** `player_wire.py:65` = เลน **faction-1 probe** เท่านั้น · `npc_wire.py:27` = serializer **วินิจฉัย faction 6** · `scene_load.py:117` = ตัวโหลด **scenario**
- ⇒ **สิ่งที่ตรึงผู้เล่นไว้ที่ฉาก 1 คือค่าคงที่หนึ่งตัว: `runtime.py:3675` `legacy.make_login_teleport(1, 0)`**

**สามข้อที่การต่อสายต้องส่งมอบ มิฉะนั้นใบนี้ยัง BLOCKED:**
1. **เส้นทางไร้แฟล็ก** ที่เลือกปลายทางจาก **แถวตำแหน่งของตัวละคร** (กฎข้อ 1 ของเวอร์ชัน) · ฟังก์ชันที่เรียกได้เลย:
```
world_scene_travel.destination(p.scene_id)      -> SceneDestination   (ฉากที่ไม่มีในพิน = KeyError ดัง ๆ ตอนบูต ตั้งใจ)
world_scene_travel.login_teleport_fields(t)     -> (scene_id, seq, x, y, z)   (บ้านคืน (1,0,0.0,0.0,0.0) เป๊ะเหมือนวันนี้)
world_scene_travel.entry_position(t)            -> Position ที่เขียนลงแถวตัวละคร
world_scene_travel.home_return_position()       -> Position ทางกลับบ้าน  🔴 ต้องใช้ตอน teardown
world_scene_travel.population_source(278)       -> None
world_scene_travel.entry_console_line(t)        -> str
```
2. **คอนโซลต้องพิมพ์บรรทัดปลายทาง *ก่อน* วางตัวละคร** — 🔴 **ไม่มีบรรทัดนี้ = ห้ามบูต** · หน้าตาเป๊ะ ๆ (ASCII บรรทัดเดียว):
```
WORLD_SCENE scene_id=278 seq=0 model=Bg1177 name=beach_football_field_(TEST) spawn=(-13270.058,22794.273,-2492.769) sent_before=NO population=none save=0 marker=0 return_ticket=REQUIRED
```
3. **คนที่ต่อสายเสร็จ กลับมาเติม "server args" ของใบนี้เป็นสตริงจริง แล้วพลิกสถานะเป็น `PENDING`**

🔴🔴 **`return_ticket=REQUIRED` ไม่ใช่คำประดับ:** ฉาก 278 มี `n_MARKER = 0` (ไม่มีจุดเข้าที่นักพัฒนาวางไว้) และ `n_SAVE = 0` และ `RE-077` ยังเปิด ⇒ **ตัวละครที่ถูกเขียนแถวเป็น 278 ไม่มีทางเดินกลับเมืองด้วยตัวเอง** · `CHARTER-02` §⑤ กฎข้อ 2 บอกว่าเวอร์ชันที่ทำให้ของเดิมเล่นไม่ได้ **คือของเสีย ไม่ใช่เวอร์ชันใหม่** ⇒ **ขั้นตอน teardown ของใบนี้บังคับให้เขียนแถวกลับด้วย `home_return_position()`**

🟢 ต่อสายเสร็จแล้ว ใบนี้จบในการนั่งครั้งเดียว (~20 นาทีบนจอ + บูต/teardown ⇒ ~40 นาที) · **หนึ่งบูตพอ**

### db (สำเนาเสมอ — **canonical ไม่ถูกเปิดตลอดรอบ**)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-079_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt079.sqlite3
```
- บูตยืนยัน (ถ้ามีตาม STOP RULE) ใช้ `state\run_gt079_confirm.sqlite3` · 🔴 **สำเนาใหม่หนึ่งใบต่อหนึ่งบูต**
- เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง** · `PRAGMA integrity_check;` ทุกสำเนา
- ต่างได้เฉพาะ `sessions` **+1 แถวต่อการเข้าเกมหนึ่งครั้ง** และ **`character_positions` ของตัวละครที่ใช้** (ใบนี้เขียนแถวนั้นโดยตั้งใจ) · จด `max(lease_generation)` ก่อน-หลัง **ห้ามถอยหลัง**
- 🔴🔴 **กับดักที่ใหญ่ที่สุด:** ถ้าเส้นทางที่ต่อสายมาไม่ได้ใช้จุดที่พินไว้ ผู้เล่นจะไปโผล่พิกัด Port Royal **ข้างใน** ฉาก 278 ⇒ **X/Y ตอนเข้าแมพต้องอยู่แถว `(-13270, 22794)`** · เห็นแถว `(-9239, -2830)` **⇒ หยุดทันที บูตนั้นเป็น `N6`**

### 🔴 ก่อนบูต — resolve commit เขียว (รันเครื่องมือ ห้ามก๊อป SHA เก่า)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` · **exit 3** ⇒ **ห้ามบูต ใบอยู่ BLOCKED** · **exit 2** = พาธผิด/git ล้ม
- **ยืนยันห้าข้อกับ `<SHA>` ที่จะบูตจริง** (single quote เท่านั้น · ห้าม `| grep`):
```
git show origin/ci-status:ci/<SHA>.json
git grep -n 'world_scene_travel' <SHA> -- src/pirateforce_foundation/runtime.py src/pirateforce_foundation/app.py
git grep -n 'TEST_STAGE_SCENE_ID = 278' <SHA> -- src/pirateforce_foundation/world_scene_travel.py
git grep -n 'def home_return_position' <SHA> -- src/pirateforce_foundation/world_scene_travel.py
git cat-file -e <SHA>:scenarios/world_scene_registry_001.json && echo PIN_PRESENT
```
- 🔴 **ข้อสองคือด่านปลด BLOCKED** — ไม่มี hit ใน `runtime.py`/`app.py` = **ยังไม่ต่อสาย ห้ามบูต**
- **อ่านค่าคาดหมายจากพินของ commit ที่บูตจริง ห้ามฝังเลขจากความจำ**

### server args (เป๊ะ — 🔴 **ยังเติมไม่ได้จนกว่าจะต่อสาย**)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt079.sqlite3 --export-events <CHIEF_FILLS_THIS_IN_AT_WIRING_TIME>
```
- 🔴 **ถ้าบรรทัดข้างบนยังมี `<CHIEF_FILLS...>` อยู่ ⇒ BLOCKED ห้ามบูต ห้ามเดาแฟล็กเอง**
- 🔴 **ห้ามใส่แฟล็ก hypothesis/scenario ตัวอื่นแม้แต่ตัวเดียว** · เห็น label ของเลนอื่นบนคอนโซล = **บูตผิดไฟล์ หยุด**
- 🔴 **ห้ามพ่วงกับ `GT-076`** — สำมะโน `bg0001` ในฉาก 278 คือ NPC ท่าเรือที่ถูกส่งผิดแมพ และจะทำให้ `C5` อ่านไม่ได้ทั้งข้อ (โค้ดจะปฏิเสธเองด้วย `ValueError` ตั้งแต่ตอนประกอบ ⇒ ถ้าเห็น traceback แบบนี้ นั่นคือ `N5`)

### 🔴 ท่ากล้อง ทิศหัน และการเดิน (คำต่อคำจาก `GT-074`/`GT-076`)
| ท่า | ทำอะไรจริง | ยิง `TargetPosVital` | ใช้ได้เมื่อไร |
|---|---|---|---|
| **คลิกขวาค้างลากเมาส์** | หมุน **กล้อง** อย่างเดียว ทิศหันตัวละครไม่ขยับ | 🟢 ไม่ยิง | ✅ ทุกจังหวะ รวมก่อนก้าวแรก · **เป็นตัวเช็ค NO-CRASH ของใบนี้** |
| **`Q` / `E`** | **หันตัวละคร** | 🔴 ยิง | ⚠️ หลังก้าวแรก + จดเวลา · 🔴 **ห้ามใช้เช็ค NO-CRASH** |
| **`W/A/S/D`** | เดิน | 🔴 ยิง | ✅ ตามสเต็ป · จดเวลาก้าวแรก |
| **ล้อเมาส์** | ซูมกล้อง | **[UNKNOWN]** | ใช้ได้ · จดเวลา · ตั้งระดับซูมของทุกภาพนิ่งให้เท่ากัน |

🔴 **ตัวที่ยิง `TargetPosVital` คือ "การเปลี่ยนทิศหันของตัวละคร" ไม่ใช่ "การขยับกล้อง"**
🔴 **ห้ามพิมพ์แชตทั้งรอบ** — ฉากถูกเลือกตอนบูต ไม่ใช่ด้วยข้อความ · ตัวอักษรตอนช่องแชตไม่โฟกัส = ฮอตคีย์ ⇒ **มือออกจากคีย์บอร์ดเมื่อไม่ได้เดิน**

---

### steps (คลิกต่อคลิก · **หนึ่งบูต** · ห้ามเปลี่ยนลำดับ)

**ก่อนเริ่ม:** ถือ `LOCK_GAME` · preflight จอว่าง (`staged\TEMPLATE_preflight_unattended.ps1` — เจอหน้าต่าง elevated = ABORT) · เทียบ sha canonical · copy DB · เตรียม teardown จาก `TEMPLATE_teardown_generic.ps1` (🔴 ถ้าก๊อปจากจ็อบตัวเลข **ต้องเห็นบรรทัดที่ 17 มี `-replace '\\','/'`** · ห้ามก๊อปจาก `1103`/`1105`)

1. **จด boot stamp (+07:00)** — teardown ปฏิเสธ stamp เก่ากว่า **420 นาที** (`TEMPLATE_teardown_generic.ps1:135` · เลข 180 ในใบเก่า = stale)
2. **จดแถวตำแหน่งเดิมของตัวละครก่อนทุกอย่าง** (`scene_id, scene_seq, x, y, z, heading` จาก `state\run_gt079.sqlite3`) — 🔴 **นี่คือใบเสร็จของทางกลับบ้าน ไม่มีบรรทัดนี้ ห้ามเริ่ม**
3. **สตาร์ตเซิร์ฟเวอร์ก่อน แล้วค่อยบูต client** (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client)
   - 🔴 client ที่ไม่มีเซิร์ฟเวอร์ **ตายเองใน ~3.5 นาที** · 🔴 **ฆ่า client กลางคัน ⇒ ต้อง restart server ก่อนเปิดตัวใหม่เสมอ** (ไม่งั้นค้างที่ `"connecting"` ตลอดกาล — **อาการนี้ให้สงสัย session ค้างก่อน อย่ารีบอ่านว่าเป็นการปฏิเสธฉาก**)
4. **อ่านบรรทัด `WORLD_SCENE ...` จากคอนโซล จดทั้งบรรทัด** — 🔴 ไม่มี หรือ `scene_id` ไม่ใช่ 278 = **หยุด `N6`**
5. **เริ่มอัดวิดีโอ** (`staged\TEMPLATE_video_recorder.ps1 -FrameRate 30` ลง `evidence_video\`) · จด `VIDEO START pid= start= fps= path=` (🔴 `start=` ห้ามใช้เป็นสมอเวลา) · 🔴 **ไม่ได้อัด = NO-RESULT**
6. เปิด client → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร → **ช่องแรก** → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (🔴 **ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด**)
7. 🎯 **`C4`:** จับเวลาตั้งแต่กดปุ่มเข้าเกม → **พูดออกเสียงว่าหน้าโหลดมีอะไร** → หยุดเมื่อเห็น HUD → **จดวินาที**
8. 🎯 **`C1`:** ยืนนิ่ง ห้ามแตะคีย์บอร์ด → **จด X/Y/Z จาก HUD** + **คัดชื่อแมพบน HUD/มินิแมพมาทั้งบรรทัด** → ตอบ `C1` หนึ่งประโยค
   - 🔴 เทียบ X/Y กับกรอบที่พินไว้ทันที (`x [-14551.5, -8356.5]` · `y [21667.4, 23876.8]`) — **นอกกรอบ = `N6` หยุด**
9. 🎯 **`C2` ตอนที่ 1:** ยืนนิ่ง 30 วินาที มือออกจากคีย์บอร์ด → จด Z ที่ 0/10/20/30 วินาที → เห็นผิวน้ำ/ได้ยินเสียงน้ำให้จดคำว่า **"น้ำ"**
10. 🎯 **`C3` + `C5`:** **คลิกขวาค้างลากกวาดกล้องรอบตัวช้า ๆ หนึ่งรอบ ค้างทุก ~90 องศา อย่างละ 4 วินาที** (มุม A/B/C/D) → ต่อมุม: เห็นอะไร · ของบัง · พื้นเรียบ/เนิน · สี · นับ actor ที่เห็น · 🔴 **ห้าม `Q`/`E`**
11. **ก้าวแรก:** แตะ `W` สั้น ๆ ครั้งเดียว → จดเวลาจริง `T_STEP` → ยืนนิ่ง 5 วินาที → **จด X/Y/Z อีกครั้ง** (`C2` ตอนที่ 2)
12. 🎯 **`C6` ตอนที่ 1:** เดิน `W`/`S`/`A`/`D` ทิศละ ~10 วินาที กลับมาราวจุดเดิม → จด X/Y/Z ปลายทางแต่ละทิศ
13. **VP-1:** เดิน `+X` ประมาณ **600-800 หน่วย** แล้วหยุด · จด X/Y/Z · กวาดกล้องมุมเดียวกับข้อ 10 · นับโมเดลต่อมุมอีกครั้ง
14. **ถ่ายภาพนิ่ง full-res ด้วยเครื่องมือนอกเกม อย่างน้อยห้าใบ** → `evidence_screens\GT079_<VP>_FULLRES_<yyyyMMdd_HHmmss>.png` (จุดเกิดสี่มุม + VP-1) · 🔴 ห้ามกดคีย์ในหน้าต่างเกมเพื่อถ่าย · 🔴 ห้าม resize ลง
15. 🎯 **`C6` ตอนที่ 2:** อยู่ในเกมครบ **10 นาทีเต็ม** นับจากเห็น HUD · เช็ค NO-CRASH ด้วย **คลิกขวาค้างลากเมาส์** ที่นาที **2 / 5 / 10** จดผลทีละครั้ง
16. ออกจากเกม: **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย → **หยุดวิดีโอ** → **ปิดเซิร์ฟเวอร์**
17. 🔴🔴 **ทางกลับบ้าน (บังคับ):** เขียนแถวตำแหน่งของตัวละครกลับ — ใช้ `world_scene_travel.home_return_position()` หรือค่าที่จดไว้ในข้อ 2 → **แล้ว query แถวนั้นออกมาแปะเป็นใบเสร็จว่า `scene_id` กลับเป็น 1 แล้ว** · 🔴 **ข้ามข้อนี้ = ตัวละครติดอยู่ในฉากที่ไม่มีทางออก และรอบนี้ทำ `v1` พังตามกฎข้อ 2 ของเวอร์ชัน**
18. เก็บ **raw GAME log ทั้งไฟล์** (`...\capture_v141\GAME_LIVE.txt`) + console out/err ทุกบรรทัด (`[G>]` / `PF-EVENT` / `ErrorData`) → `PRAGMA integrity_check;` → sha256 ทุกไฟล์
19. **teardown ทันที** (ใช้ boot stamp ของบูตนี้) → เทียบ sha canonical กับ `CANON_SHA.txt`
20. **แตกเฟรมรอบหน้าโหลดและรอบเข้าแมพ** (🔴 ห้ามมี `scale=` ในคำสั่ง):
```
$mkv = '<path full of the FULLROUND .mkv of this boot>'
ffmpeg -ss <T_ENTER - 20.00> -i $mkv -t 40.00 -vsync 0 GT079_ENTER_%03d.png
```
21. 🔴🔴 **G-OBS — บังคับ:** ผู้ช่วยทวนรายการ "สิ่งที่ผู้ช่วยเห็น" ให้ผู้เทสยืนยันทีละข้อ (`C1`-`C6` · สี · จำนวน · ค้าง/หลุด · **สีป้ายชื่อทุกป้าย**) → ผู้เทสตอบคำเดียวต่อข้อ: **"ตรง" / "ไม่ตรง" / "ฉันไม่ได้ดูข้อนั้น"** → จดหมายผลต้องมี `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` · 🔴 ยังไม่ยืนยัน = ห้ามเขียนผลลงคิว

### ⛔ STOP RULE
1. **`ErrorData` ใด ๆ หลังเฟรมที่มี `scene_id=278`** ⇒ จดเลขเป๊ะ + หลังเฟรมไหน + กี่วินาทีหลัง `T_ENTER` + เก็บ console ทั้งไฟล์ · 🔴 คาดไว้ว่า `28317` มาพร้อม **ไคลเอนต์ปิดการเชื่อมต่อทั้งสองเส้น**
2. **บูตยืนยันได้หนึ่งครั้ง** ด้วย `run_gt079_confirm.sqlite3` แล้วหยุด · 🔴 restart server ก่อนเสมอ · 🔴 **ทางกลับบ้าน (ข้อ 17) ทำทุกบูต**
3. **ทำซ้ำไม่ได้ก็ยังเป็นผล** — จดว่า "พังหนึ่งในสอง" แล้วหยุด
4. 🔴 **ห้ามลองฉากอื่น ห้ามลองพิกัดอื่น ห้ามแก้การ์ดกลางรอบ**
5. **บูตตายด้วย traceback ก่อนมีไบต์ออกสาย** ⇒ `N5` **ไม่ใช่ผลเรื่องไคลเอนต์** ส่งกลับ chief

### คำทำนาย (**ผิด = ผล ไม่ใช่ความล้มเหลว**)
- **P1 [ข้อที่ไม่มีใครรู้จริง ๆ]** ไคลเอนต์โหลดฉาก 278 ถึงสถานะเล่นได้ — 🔴 **การจับคู่ `scene_id`→ฉาก ยืนยันที่แถว 1 และ 2 เท่านั้น และมีการอ่านค่าคู่แข่งสามแบบ** ⇒ **ผิดเมื่อไหร่คือผลที่มีค่าที่สุดของรอบ**
- **P2** มีพื้นรองรับที่จุดที่พินไว้ (จุดนี้เป็น placement ที่นักพัฒนาวางของไว้จริง) 🔴 หลักฐานเรื่อง placement ไม่ใช่ terrain
- **P3** เวทีกว้าง เรียบ ไม่มีของบังในสี่มุม
- **P4 [🔴 คาดว่าจะผิด]** **สีจะไม่ใช่ขาวล้วน** — `RE-073` พบว่าไม่มีฉากไหนในสามตัวเลือกที่ขาวจริง
- **P5** `BgNull` ไม่ทำให้เกิดข้อบกพร่องที่เห็นได้ (237/271 แถวใช้ค่านี้) 🔴 ไม่มีใครเคยวัด
- **P6 [มั่นใจที่สุด]** ไม่มี actor สักตัวจากเก้า placement — ไม่มีใครส่งอะไรเลยในบูตนี้
- **P7** เดินได้และอยู่ครบ 10 นาที
- **P8 [จดสีอย่างเดียว]** ป้ายชื่อตัวเราเอง = ขาว · ป้ายอื่นคาดว่าไม่มี
- **P9** ไม่มี `ErrorData` — 🔴 โผล่เมื่อไหร่ให้จดเลขเป๊ะและหยุด

### pass criteria — **สองชั้น แยกกันเด็ดขาด 🔴 ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

**ชั้น (1) wire/DB**
1. `BOOT_COMMIT` + ผลด่านก่อนบูตห้าข้อ (**แปะบรรทัดที่ `git grep` พิมพ์ออกมาจริง**)
2. **บรรทัด `WORLD_SCENE ...` ตัวอักษรเป๊ะทั้งบรรทัด** — ต้องมี `scene_id=278` · `seq=0` · `model=Bg1177` · `sent_before=NO` · `population=none` · `return_ticket=REQUIRED`
3. **เฟรมเข้าฉาก:** label + `pc bytes` + `framed bytes` + `frame_sha256` + **`scene_id` ที่ decode ได้จาก `u16tag 0x12` ต้องอ่านได้เป็น `278` (`0x0116`) และ `scene_seq` = 0**
4. **พิกัด f32 ที่ decode ได้** เทียบจุดที่พินไว้ `(-13270.058, 22794.273, -2492.769)` 🔴 ห้ามใช้ HUD เป็นฐานคำนวณ
5. **มี `ErrorData` ไหม** — เลขเป๊ะ + หลังเฟรมไหน + กี่วินาที · 🔴 `28317` = parse-failure echo
6. **การสื่อสารเดินต่อไหม** — บรรทัดถัดไปทั้งขาเข้าขาออกพร้อมเวลาจริง + `TargetPosVital` ยังวิ่งตอนเดินไหม
7. **census: นับทุกบรรทัด `[G>]` ทั้งไฟล์** · ไม่มี traceback/stderr · 🔴 **ต้องไม่มีบรรทัดจาก `npc_wire` หรือ `world_population` ในบูตนี้**
8. **DB:** `integrity_check` = ok · ต่างเฉพาะ `sessions` +1 และแถวตำแหน่งของตัวละคร · `max(lease_generation)` ไม่ถอยหลัง · **sha256 canonical ก่อน-หลัง = `CANON_SHA.txt`**
9. 🔴 **ใบเสร็จทางกลับบ้าน: query แถวตำแหน่งหลัง teardown แล้วแสดงว่า `scene_id` = 1**
10. **ความครบของวิดีโอ (กฎ S):** `ffprobe` เฟรมจริงเทียบ `duration x fps` · รายงานเฟรมที่หายเป็นตัวเลข
11. 🔴🔴 **ชั้นนี้ตอบไม่ได้:** ไม่ตอบ `C1`-`C6` แม้แต่ข้อเดียว · **"ส่ง 278 แล้วไม่มี `ErrorData`" ไม่ได้แปลว่าไคลเอนต์โหลด `Bg1177`** (อาจโหลดแมพอื่นตามการอ่านค่าคู่แข่ง) · **log ไม่รู้จักสี**

**ชั้น (2) client-observable — 🔴 ตัวปิดใบอยู่ชั้นนี้ชั้นเดียว**
1. วิดีโอต่อเนื่องตั้งแต่ก่อนกดเข้าเกมจนออก · ภาพนิ่ง full-res ≥ **ห้าใบ** · sha256 ทุกไฟล์
2. 🎯 **ตอบ `C1`-`C6` ทีละข้อ ข้อละหนึ่งประโยค** 🔴 ห้ามยุบรวม ห้ามข้าม · ไม่ได้ดูให้เขียนว่า "ฉันไม่ได้ดูข้อนั้น"
3. **ตารางต่อมุม:** หนึ่งแถวต่อ (VP x มุม) · X/Y/Z · ของบัง · พื้นเรียบ/ไม่เรียบ · สี · จำนวนที่เห็น (**ขอบล่างเสมอ**)
4. **`C4` เป็นตัวเลข** + คำบรรยายหน้าโหลดหนึ่งประโยค
5. **`C6` เป็นตัวเลข** (`mm:ss`) + NO-CRASH นาที 2/5/10 แยกสามบรรทัด
6. **อาการไคลเอนต์:** ค้าง/กระตุก/dialog error (คัดข้อความทั้งบรรทัด)/หลุด — เวลาสัมพัทธ์กับ `T_ENTER`
7. **ตารางสีป้ายชื่อครบทุกป้ายทุกภาพ full-res** (PLAYBOOK ข้อ 13)
8. 🔴 **ปิดด้วยผลลบได้เฉพาะรอบที่คุณ Panya เห็นเอง + มีวิดีโอต่อเนื่อง** (`UNATTENDED_RULES.md`)
9. 🔴 **ชั้นนี้ตอบไม่ได้:** ส่งค่าอะไรออกไปจริง · ไบต์เท่าไร · มี `ErrorData` ไหม — **"ผมเห็นสนามโล่ง" ไม่ใช่หลักฐานว่าเราส่ง 278**

🔴 **ชั้น (1) ไม่ผ่าน (ไม่มีบรรทัด `WORLD_SCENE` · decode ไม่ได้ · ไม่ได้อัดวิดีโอ · X/Y นอกกรอบ · ใช้ DB ซ้ำ) ⇒ NO-RESULT ห้ามอ่านจอเป็นผล**

### ตารางผลลัพธ์ที่มีชื่อ
| # | สิ่งที่เห็น | คำตัดสิน | สรุปได้ว่า | 🔴 สรุป**ไม่**ได้ว่า / redirect |
|---|---|---|---|---|
| **N1** STAGE-USABLE 🎯 | `C1` เข้าได้ **และ HUD บอกชื่อแมพที่ตรงกับ `Bg1177`** · `C2` มีพื้น · `C3` กว้าง-เรียบ-โล่ง · `C6` ครบ | ✅ **PASS** | ไคลเอนต์ตัวนี้ บนบิลด์นี้ **เข้าฉาก 278 ได้** และจุดที่พินไว้ยืนได้ ⇒ ใช้เป็นเวทีของสาย B/C ได้ · **และการอ่านค่า `n_ID` รอดหนึ่งแถว** | ❌ ห้ามเขียนว่า "ย้ายฉากได้แล้ว" (`RE-077`) · ❌ ห้ามเขียนว่า "ฉากอื่นก็เข้าได้" |
| **N1b** ENTERS-WRONG-MAP 🎯🔴 | เข้าได้ **แต่ HUD บอกชื่อแมพอื่น** | ✅ **PASS — ผลที่แพงที่สุดในใบ** | ว่า **การอ่านค่า `n_ID` ผิด** และแมพที่ขึ้นคือตัวชี้ว่าฟิลด์นี้คืออะไรจริง ๆ | ❌ ห้ามเดาว่าเป็นคอลัมน์ไหนโดยไม่เทียบตาราง · **redirect:** `RE-077` T2 + สาย A แก้พินทันที |
| **N2** ENTERS-BUT-NOT-THE-STAGE-ASKED-FOR | `C1`/`C2`/`C6` ผ่าน · `C3` มีของบัง/ไม่เรียบ หรือสีไม่ขาว | 🟡 **PARTIAL** | ว่า 278 เข้าได้ แต่ยังไม่ตรงคำขอข้อไหน (ระบุข้อ) | ❌ ห้ามรายงานเป็น FAIL · ❌ ห้ามไปหาฉากใหม่เองในรอบเดียวกัน |
| **N3** ENTERS-NO-GROUND 🔴 | `C1` ผ่าน · `C2` ตก/ลอย/อยู่ในน้ำ | ✅ **PASS — ผลของใบ** | ว่าฉากโหลดได้ แต่จุดนั้นยืนไม่ได้ | ❌ ห้ามสรุปว่า "ฉากนี้ไม่มีพื้น" (วัดจุดเดียว) · **redirect:** ใบใหม่เรื่องจุดยืน + คำถาม Z/พื้นที่ค้างจาก `GT-034` |
| **N4** REFUSED-AT-ENTRY 🎯 | error/หลุด/ค้างหน้าโหลด · ทำซ้ำแล้วหนึ่งครั้ง | ✅ **PASS — ผลลบที่มีค่าเท่าผลบวก** | ว่าบนเส้นทางนี้ บิลด์นี้ ไคลเอนต์ไม่ถึงสถานะเล่นได้เมื่อได้รับ `scene_id=278` + **เลข `ErrorData` ที่เห็นจริง** | ❌ **ห้ามชี้สาเหตุ** (ค่านอกตาราง? asset? ลำดับเฟรม? `BgNull`? `n_CAMERA_TYPE=0`? — ไม่ได้วัดสักอย่าง) · **redirect:** `RE-077` T2 |
| **N5** SERVER-SIDE-REFUSAL 🔴 | ตายด้วย `ValueError`/traceback ก่อนมีไบต์ออกสาย | 🔴 **NO-RESULT** | ไม่มี | ❌ ห้ามอ่านเป็นการปฏิเสธของไคลเอนต์ · **redirect:** traceback ให้ chief · **ใบกลับเป็น BLOCKED ห้าม archive** |
| **N6** NON-OBSERVED | ไม่มีบรรทัด `WORLD_SCENE` · decode ไม่ได้ · X/Y นอกกรอบ · ไม่ได้อัด · DB ซ้ำ · เห็น label เลนอื่น | 🔴 **NO-RESULT** | ไม่มี | ❌ สิ่งที่เห็นบนจอไม่ใช่ผล · **redirect:** รันซ้ำ commit เดิม · **ห้าม archive** |
| **N7** PARTIAL-SESSION | เข้าได้ แต่จบก่อน 10 นาทีเพราะคนเลิกเล่น | 🟡 **PARTIAL** | ข้อที่ตอบได้ตอบว่าอะไร | ❌ ห้ามเขียนว่า `C6` ผ่าน · 🔴 **teardown + ทางกลับบ้านยังต้องทำ** |

### ⭐ PLAYBOOK ข้อ 13 — สีของ **ทุกป้ายชื่อในเฟรม** (คำสั่ง Panya 2026-08-25 · บังคับทุกใบ attended)
- **จด:** ชื่อตัวเราเอง (เหนือหัว + แผง UI ซ้ายบน) · ชื่อ NPC/actor ทุกตัว · ชื่อไอเทมบนพื้น · ชื่อผู้เล่นอื่น · title/คำอธิบาย · **ชื่อแมพบน HUD/มินิแมพ** — หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ
- **ไม่มีให้เขียนคำว่า "ไม่มี"** 🔴 ห้ามเว้นว่าง (🎯 ฉากนี้คาดว่าเกือบทุกแถวจะเป็น "ไม่มี" — **นั่นคือแถวที่ต้องเขียน**)
- อ่านสีจาก **ภาพนิ่ง full-res / crop PNG เท่านั้น** 🔴 ห้ามจาก contact sheet · ห้ามจากภาพย่อ · ห้ามจากวิดีโอ
- ภาพอ้างอิงเซิร์ฟเวอร์ต้นฉบับ: NPC = เหลือง · ผู้เล่น = เขียว · ไอเทมบนพื้น = ขาว · title = ฟ้า · ชื่อตัวเอง = ขาว
- 🔴 **จด "สี" อย่างเดียว ห้ามสรุปสาเหตุ** — สาเหตุคือ `RE-067` / `RE-068`
- `REAL_SERVER_DIVERGENCE.tsv`: 🔴 **ส่งค่ากลับมาในจดหมาย ห้ามแก้ไฟล์เอง** · `evidence_layer` = `eye` · `open_ticket` = `RE-067` · `blocks_promotion` = `no` · เติมแถวแม้ผลจะตรงกัน
- 🟡 **สีของพื้น/ฟ้า/หมอก (`C3`) จดในตารางแยก** ห้ามยุบรวมกับตารางป้ายชื่อ · ห้ามเขียนเป็น RGB/hex

### เกณฑ์หยุดทั้งเลนทันที
⛔ `ErrorData` ใด ๆ หลังเฟรมเข้าฉาก ⇒ หยุดตาม STOP RULE
⛔ คอนโซลขึ้น label ของเลน scenario/hypothesis อื่น หรือบรรทัดจากทางประชากร ⇒ บูตผิดไฟล์ หยุด
⛔ X/Y ตอนเข้าแมพนอกกรอบ `x [-14551.5, -8356.5]` / `y [21667.4, 23876.8]` ⇒ หยุด `N6`
⛔ ชื่อ probe ใด ๆ (`ProbePlayer01` / `ProbeControl03`) โผล่ ⇒ หยุด เก็บ console ทั้งไฟล์

### 🧾 teardown + ใบเสร็จ (บังคับ แม้รอบจบเพราะคนเลิกเล่น)
- **teardown ภายใน 420 นาทีจาก boot stamp ของบูตนั้น** (`TEMPLATE_teardown_generic.ps1:135`) — เกินเพดาน template ปฏิเสธ exit 12 โดยดีไซน์
- แท่นที่ถูกทิ้งข้ามชั่วโมง: `staged\TOOL_stop_stale_server.ps1` แล้วตามด้วย receipt อ่านอย่างเดียว `staged\0949_gt027_stalepad_canonical_guard.ps1`
- **exit 36** อย่าเดาเอง — แนบบรรทัดที่ 17 ของไฟล์ teardown ที่ใช้จริงมาทั้งบรรทัด
- **ใบเสร็จ:** `AFTER listeners = 0` · **sha256 canonical ก่อน-หลัง = `CANON_SHA.txt`** · teardown exit code · `LOCK_GAME` ปล่อยแล้ว · **แถวตำแหน่งกลับเป็น `scene_id = 1` แล้ว (query จริง)** · run copy `state\run_gt079*.sqlite3` **เก็บไว้ให้ chief re-derive ห้ามทิ้ง** · path ของ raw GAME log + console + วิดีโอ + ภาพ พร้อม sha256
- 🔴 **ห้ามลบ:** `.mkv` ต้นฉบับ และโฟลเดอร์ capture ของบูตนี้

### nonclaims (ติดไปกับผลทุกกรณี — ห้ามตัดทิ้ง)
① 🔴🔴 **ใบนี้วัด "การ *เข้า* ฉาก" ไม่ใช่ "การ *ย้าย* ฉาก"** — `RE-077` เปิดอยู่ · **ผ่านใบนี้ = ห้ามเขียนว่า "ออกจากเมืองได้แล้ว"**
② 🔴🔴 **ผ่านที่ 278 ไม่พูดถึงอีก 270 ฉาก** · **"addressable" แปลว่ามี `n_ID` เท่านั้น** · และ **การจับคู่ `scene_id`→ฉากยังยืนยันแค่แถว 1 กับ 2 · ใบนี้เพิ่มได้มากที่สุดอีกหนึ่งแถว**
③ 🔴 **ไม่พูดถึงสำมะโน `bg0001` ของ `BUILD-001`** — `population_source(278)` คืน `None` และ `build_world_population` ปฏิเสธทุกฉากที่ไม่ใช่ 1 ⇒ **รอบนี้ไม่มีใครส่ง actor สักตัว**
④ **z ที่แบนของเก้า placement ไม่ใช่การวัด terrain** — และคอลัมน์ f32 อีกสามช่องของแต่ละ record **ยังไม่มีใครถอด** (ถ้ามันคือรัศมี spawn ค่า z อาจเป็นความสูงอ้างอิงของ editor ไม่ใช่พื้น)
⑤ **`C2` วัดจุดเดียว** — มีพื้นที่จุดนี้ ≠ ทั้งฉากมีพื้น และไม่มีพื้นที่จุดนี้ ≠ ทั้งฉากไม่มีพื้น
⑥ **จำนวนใน `C5` เป็นขอบล่างเสมอ** — ระยะมองเห็น/สิ่งบัง/มุมกล้อง/LOD ไม่มีตัวคุมในรอบนี้ ⇒ เขียน **"ไม่เห็น"** ห้ามเขียน **"ไม่มี"**
⑦ **`C4` ไม่พิสูจน์ว่า `BgNull` ปลอดภัยโดยทั่วไป** — วัดฉากเดียว ครั้งเดียว
⑧ **`C6` 10 นาที คือเพดานล่างของกฎข้อ 3 ไม่ใช่คำรับรองความเสถียร** — ไม่ได้วัดชั่วโมง memory หรือ fps
⑨ **สีอ่านด้วยตา ไม่ได้วัดพิกเซล** ⇒ ไม่ claim ค่า RGB/hex · `evidence_layer` = `eye`
⑩ **ไม่ตอบว่าอะไรตัดสินสีป้ายชื่อ** — `RE-067` / `RE-068`
⑪ **"เวทีไม่ขาว" ไม่ใช่คำตอบว่าเจ้าของจะได้เวทีขาวหรือไม่** — `RE-073` ปิดแล้วด้วยผลว่าไม่มีฉากไหนขาวจริง · การตัดสินเป็นของเจ้าของ
⑫ **ไม่รับรองว่าการต่อสายของ chief ถูกต้องโดยทั่วไป** — พิสูจน์แค่ว่าบูตนั้นส่งค่าอะไรและเกิดอะไรขึ้น
⑬ **`ErrorData=28317` ไม่ใช่ "รายงานจำนวน"** — `0x6E9D` = class id ของ envelope ที่ deserialize ไม่ผ่าน (`reports/PF_DELETE_SOFT002_NATURAL_0x36DB_DECODE_20260818.md` §(c)) · ห้ามเขียนว่า "ค่าฉากเกินขอบเขต"
⑭ **ใบนี้ไม่อนุญาตให้ LANE-A แตะ `runtime.py` / `app.py` / `pf_login_game_server_v141.py`** — ไฟล์แกนเป็นของ chief (`CHARTER-02` §⑥)
⑮ **ใบนี้ไม่ปิด `M2` และไม่ประกาศ `v2`** — ใบนี้ส่งมอบหลักฐานหนึ่งชิ้น ไม่ใช่ลายเซ็น
⑯ **`OBSERVER_CONFIRMED` เป็นขั้นตอน ไม่ใช่หลักฐาน**
⑰ **เฟรม การประกอบ ค่าฟิลด์ และการเลือกจุดยืน เป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้วและกู้ไม่ได้

- **result:** (ผู้เทสกรอก: ① `BOOT_COMMIT` + ผลด่านก่อนบูตห้าข้อ ② **บรรทัด `WORLD_SCENE ...` เป๊ะทั้งบรรทัด** ③ label + `pc bytes` + `framed bytes` + `frame_sha256` + `scene_id`/`scene_seq` ที่ decode ได้ ④ พิกัด f32 ที่ decode ได้ + X/Y/Z บน HUD ⑤ **คำตอบ `C1`-`C6` ข้อละหนึ่งประโยค** (🎯 `C1` ต้องมี **ชื่อแมพที่ HUD แสดง คัดมาทั้งบรรทัด**) ⑥ ตารางต่อมุม ⑦ วินาทีหน้าโหลด + คำบรรยาย ⑧ เวลาในเกม `mm:ss` + NO-CRASH นาที 2/5/10 ⑨ `ErrorData` มีไหม เลขอะไร หลังเฟรมไหน กี่วินาที ⑩ บรรทัด traffic ถัดไป + `TargetPosVital` ยังวิ่งไหม ⑪ ตาราง PLAYBOOK ข้อ 13 + ตารางสีพื้น/ฟ้า/หมอกแยก ⑫ ค่าที่ต้องเติม `REAL_SERVER_DIVERGENCE.tsv` ⑬ census `[G>]` ทั้งไฟล์ + ไม่มี traceback ⑭ **แถวไหนของตารางผล (N1-N7)** ⑮ path ทุกไฟล์ + sha256 ⑯ เวลา +07:00 · sha canonical ก่อน-หลัง · `integrity_check` · row-diff + `max(lease_generation)` · teardown exit code ⑰ **ใบเสร็จทางกลับบ้าน: query แถวตำแหน่งแล้วแสดงว่า `scene_id` = 1** ⑱ `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ⑲ `BUILD_IMPACT: <สร้างอะไรได้จากความรู้นี้ / หรือ "ไม่มี" พร้อมเหตุผล>` 🔴 บังคับตาม `CHARTER-01` BUILD-003 ⑳ ถ้ามีบูตยืนยัน: ทุกข้อข้างบนแยกชุด)

---

## 🆕 GT-080 EMPTY-VIEW-IS-THE-MAP-NOT-THE-SEND-001 [attended, in-game]: ยืนสองจุดในบูตเดียวที่สำมะโน **ไม่เปลี่ยนแม้แต่ไบต์เดียว** — **"ไม่เห็นใคร" ที่จุดเกิดเป็นคุณสมบัติของ *ที่ที่ยืน* หรือของ *จำนวนที่ส่ง***  [🟢 **READY** — `unblocked by chief (LANE-E) 2026-09-05T02:0x+07:00 measured on main 2a71c0a5` ตาม `COO-DECISION 20260904_2349` ข้อ 3 · เหตุบล็อกเดิม (BLOCKED-ON-WIRING: "`world_population`/`world_density` ยังไม่ถูก import จาก `runtime.py` หรือ `app.py` เลย") **หมดจริง** — วัดบน `main` ของ pirate-force-server sha `2a71c0a5`: `runtime.py:28` `from . import world_density` · `runtime.py:33` `from . import world_population` · และถูกเรียกจริงไม่ใช่แค่ import (`runtime.py:470` `world_population.WIRE_HEADER_BYTES` · `runtime.py:1131` `world_population.effective_actor_count(...)`) · เจ้าของใบ **LANE-A** ทักท้วงได้หนึ่งรอบผ่านจดหมาย ไม่ทักท้วง = ยืน · เปิดใบโดย LANE-A (สาย A · WORLD) 2026-08-26 ~02:2x (+07:00) ตาม `CHARTER-02` BUILD-001 / M1 · ร่างใบโดย `pf-queue-author` · **แก้ตามผล `pf-adversary` ก่อนวาง**] -- moved to `tickets/GT-080.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `cm9v9y` 2026-09-06T17:10+07:00)

## 🆕 GT-081 TRAVEL-GATE-WALK-OUT-AND-WALK-HOME-001 [attended, in-game]: ผู้เล่นที่ **หยุดยืน** ในเขตที่พินไว้กลางท่าเรือ ทำให้ **ตัวเอง** ข้ามไ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-084 MOB-COMBAT-001 / MOB-DEATH-001 FIRST-REAL-ATTACK-001: การโจมตีจริงจากผู้เล่นครั้งแรกที่ไปถึง mob_combat/mob_death บนบูตไร้แฟล็ก -- เลือดมอนสเตอร์ลดจริงไหม และ 0x201F ตายไหม  [🟡 **RESULT (ผ่านผลต่อของ GT-084-R2, 2026-08-27) -- wire/DB ครบ (hit x5, HP to 0, MOB-DEATH-001 kill, dying/dead frames, MOB_LOOT_DROP x2) แต่ client-observable FAIL 2 จุด: ศพแข็งลอยค้าง (ไม่ล้มตาม GT-022/GT-025), single-click ไม่มีแผงเป้า -- ดู notes_to_chief/20260827_1620_GT084R2-RESULT-*.md, RE-107/RE-108 ปิดแล้ว (bounded negative, 2026-08-27T17:1x+07:00), ห้ามอ่านเป็น PASS/DONE** [UPDATE 2026-08-28T04:1x+07:00, R205, chief: CORE-REQUEST-024 wired -- server-side attack-cadence gate now runs on this dispatch path (`ATTACK_CADENCE_MS_PROVISIONAL=600`, RE-110 still open), closing the spam-click=runaway-damage gap LANE-B's own letter said this GT was seeing. Wire/DB proven only (`tests/test_mob_combat_cadence_wiring.py`) -- no attended session has confirmed the throttled rate looks right on screen yet]] -- moved to `tickets/GT-084.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `hf1gs9` 2026-09-06T23:17+07:00)
## GT-084-R2 HOSTILE-PAIR-VISIBLE-001: รอบสองของ GT-084 -- คู่ faction (1,6) ที่ผู้เล่นได้ครึ่งของตัวเองแล้ว ทำให้ Tornado Eagle ขึ้นศัตรูจริงบนจอไหม (~~ชื่อแดง + แผงเป้าแดง~~ [UPDATE 2026-08-27T17:34+07:00 LANE-B ต่อยอด PANYA-REFERENCE 16:35+07:00: เกณฑ์สีที่ถูกต้องคือ **ส้ม (ยังไม่ aggro) → แดงเข้ม (aggro) → เทา (ตาย)**, ไม่ใช่ "แดง" เฉยๆ] + แผงเป้า) บนบูตไร้แฟล็ก -- ก่อนจะไปถึงเรื่องตี  [🟡 **RESULT -- claim หลัก (hostile ที่ตาเห็น) PASS ด้วยหลักฐานพฤติกรรม (ขอบแดง+ลูกศรแดงคู่, ดับเบิลคลิกตีติดจริง) แต่ไม่ใช่สีตามใบเป๊ะ (ชื่อชมพู/magenta ตลอด ไม่ใช่ส้ม→แดงเข้ม→เทาตามลำดับสถานะจริง, ไม่มีแผงเป้า) -- ผลต่อขั้นตี-ตาย: ดู GT-084 -- รายละเอียด notes_to_chief/20260827_1620_GT084R2-RESULT-*.md, RE-107/RE-108 ปิดแล้ว (bounded negative), RE-109 เปิดใหม่ถามครบ 6 สี, สถานะสุดท้าย (PASS/MIXED) รอ chief ตั้ง**] -- moved to `tickets/GT-084-R2.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `43htls` 2026-09-07T00:09+07:00)

### 🆕 GT-099 BACKPACK-LOAD-REFUSED-001: แถวกระเป๋าที่พังโครงสร้าง (แถวหาย) ตอนนี้เซิร์ฟเวอร์ปฏิเสธเสียงดังจริงไหม แทนที่จะพังเงียบเหมือนก่อน  [PENDING]

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md. เลขสูงสุด ณ เวลาเขียนใบนี้: GT-084 / RE-098 (บันทึกไว้เองว่า
> เลขว่างถัดไป = 099). grep ซ้ำก่อนจอง: GT-099 = 0 hit ทั้งสองไฟล์ (ยืนยัน 2026-08-27). ใบเก่าไม่ถูกแตะ.

### ที่มา
`notes_to_chief/20260826_0950_COO-DECISION-the-bag-wall-is-chief-s-and-the-identity-column-lands-with-it.md`
①(ข)2: ด่าน 1 (`store._load_backpack`) ต้องตอบ ไม่ใช่หายไป — ก่อนรอบนี้ ทั้ง `ValueError` (เนื้อหาไม่ตรง
golden) และ `RuntimeError` (แถวหัวหาย) จากด่านนี้ไม่มี handler รับใน `runtime.py`
(`except (KeyError, PermissionError)` เดิม) ⇒ หลุดขึ้นไปตายเงียบในดิสแพตช์ของ v141 ที่แช่แข็งไว้ (ไม่มีการ
พิมพ์อะไรเลย — วัดจากพฤติกรรมที่ report ไว้ก่อนหน้า ไม่ใช่การเดา).

รอบที่แก้: chief cloud, session `keen-pasteur-ss84b6`, repo `pirate-force-server`:
1. `runtime.py`, handler ของ `START_GAME_REQ`: เพิ่ม `except (ValueError, RuntimeError)` แยกจาก
   `except (KeyError, PermissionError)` เดิม พิมพ์ `BACKPACK_LOAD_REFUSED <reason>` แล้วตอบไม่ตอบ (no reply)
   แบบสะอาด แทนที่จะปล่อยให้หลุดขึ้นไป.
2. `inventory.py`/`store.py`: แยก `require_known_backpack` เป็น `require_backpack_shape` (โครงสร้างอย่างเดียว)
   ใช้ที่ `store._load_backpack` — ไม่กระทบใบนี้โดยตรง (ใบนี้ทดสอบกรณี "แถวหัวหายไปเลย" ซึ่งยังคง raise
   `RuntimeError` เหมือนเดิมไม่ว่าจะแยกฟังก์ชันหรือไม่).

🔴 **คำเตือนขอบเขต สำคัญมาก อ่านก่อนบูต**: ใบนี้**ไม่ทดสอบ**กรณี "กระเป๋าที่มีเนื้อหาดริฟต์แต่โครงสร้างถูกต้อง"
(เช่น item ที่มี `quantity` ผิดจาก golden) — กรณีนั้นยังคงถูกปฏิเสธที่ `session.select_and_start`'s
`is_unmoved_baseline` check (ไม่ถูกแตะในรอบนี้ — ลองแคบแล้วต้อง revert เพราะไปชนกับเทสของ
`HYP-PF-010`/`017`/`018` ที่ต้องพึ่งเช็กนี้กันสถานะที่ mutate แล้วหลุดกลับมาแบบไม่มี opt-in flag) ซึ่งจับด้วย
`except (KeyError, PermissionError)` เดิม (เงียบ ไม่พิมพ์อะไร) — พฤติกรรมที่สังเกตได้จากรอบนี้ **เหมือนเดิม
ทุกประการ** กับก่อนรอบนี้สำหรับกรณีดริฟต์เนื้อหา (ทั้งสองกรณีคือ "ไม่ตอบ" แต่คนละสาเหตุ) ⇒ **ห้ามใช้ใบนี้
ทดสอบกรณีนั้น** ถ้าอยากทดสอบกรณีเนื้อหาดริฟต์ ต้องรอรอบที่ออกแบบ Gate 2 (`is_unmoved_baseline`) ใหม่ให้แยก
"ของจริงจากเกมเพลย์" ออกจาก "สถานะที่มาจาก hypothesis scenario ที่ยังไม่ได้ opt-in" ก่อน — ยังไม่มีรอบไหนทำ.

### objective (claim เดียว)
สำหรับตัวละครที่แถว `character_backpacks` (หัวตาราง ไม่ใช่ items) **ถูกลบทิ้งทั้งแถว** ด้วยมือ (จำลอง DB ที่
เสียหาย/ไม่สมบูรณ์ — ไม่ใช่กรณีเนื้อหาดริฟต์) ผู้เทสเห็น: (1) รายการเลือกตัวละครยังโหลดขึ้นปกติ (ไม่แตะ
backpack table เลย ไม่เกี่ยวกับใบนี้ แต่บันทึกไว้เป็น baseline), (2) กด "เข้าเกม" กับตัวละครนั้นแล้ว
คอนโซลพิมพ์ `BACKPACK_LOAD_REFUSED character Backpack state is missing` ภายในไม่กี่วินาที, (3) process
เซิร์ฟเวอร์ไม่ตาย (ยัง `ProcessId` เดิม), (4) ไม่มี Python traceback ใด ๆ ขึ้นคอนโซลเลย.

**ตัวหักล้าง:** ถ้ากด "เข้าเกม" แล้วคอนโซลเงียบสนิท (ไม่มีทั้ง `BACKPACK_LOAD_REFUSED` และ traceback) หรือ
process เซิร์ฟเวอร์ตาย ⇒ ไม่ผ่าน — การแก้ไม่ได้ผลอย่างที่คาด หรือบูตผิดคอมมิต.

### ก่อนบูต
ด่าน 1: `py -3 pf_resolve_green_boot.py --repo "..." --fetch` ตามธรรมเนียม exit 0 เท่านั้นถึงบูตได้.
ด่าน 2: `git grep -n "BACKPACK_LOAD_REFUSED" <SHA> -- src/pirateforce_foundation/runtime.py` ต้องเจออย่างน้อย
1 บรรทัด. ขาด = BLOCKED.

### db (สำเนาเสมอ ห้ามแตะ canonical/state\play.sqlite3)
copy `state\pirateforce.sqlite3` ไปสำรอง + ไปที่รันจริงตามธรรมเนียม GT-084 แล้ว:
```
sqlite3 state\run_gt099.sqlite3 "SELECT character_id FROM character_backpacks ORDER BY character_id LIMIT 1;"
```
จด `character_id` ของตัวละครช่องแรก (ยืนยันด้วย SELECT ห้ามเดา) แล้ว:
```
sqlite3 state\run_gt099.sqlite3 "DELETE FROM character_backpack_items WHERE character_id = <id>;"
sqlite3 state\run_gt099.sqlite3 "DELETE FROM character_backpacks WHERE character_id = <id>;"
```
(ลบ items ก่อนเสมอ ตามลำดับ FK — `character_backpack_items.character_id` REFERENCES
`character_backpacks.character_id`). ยืนยันว่าลบจริงด้วย SELECT ซ้ำ (ต้องว่าง 0 แถวทั้งสองตาราง).

### server args
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt099.sqlite3
```
ห้ามมี `--*-scenario` — เส้นทางนี้คือดีฟอลต์.

### steps
1. ถือ LOCK_GAME, สตาร์ตเซิร์ฟเวอร์, จด ProcessId (`Get-CimInstance Win32_Process -Filter "Name='python.exe'"`).
2. เปิด client → เลือกเซิร์ฟเวอร์ → หน้าเลือกตัวละคร. สังเกต: รายการโหลดปกติไหม (คาดว่าใช่ — ไม่แตะ backpack
   table).
3. คลิกเลือกตัวละครที่ถูกลบกระเป๋า → ปุ่ม "เข้าเกม". เริ่มจับเวลา.
4. เฝ้าคอนโซลเซิร์ฟเวอร์ต่อเนื่อง 30 วินาที — คัดบรรทัด `BACKPACK_LOAD_REFUSED` มาทั้งบรรทัดถ้ามี, จด traceback
   ใด ๆ ถ้ามี.
5. เฝ้าจอไคลเอนต์คู่ขนาน — จดว่าเห็นอะไร (คาดว่า "connecting" ค้างแล้วไคลเอนต์ตายเองใน ~3.5 นาที เพราะฝั่ง
   client ไม่รู้ความต่างระหว่าง "ปฏิเสธอย่างสุภาพ" กับ "ไม่มีอะไรตอบ" — นี่ไม่ใช่ผลลบ ตราบใดที่ข้อ 4 เห็น
   `BACKPACK_LOAD_REFUSED` และ process ยังไม่ตาย).
6. ยืนยัน ProcessId เดิมยังอยู่ (เช็ค `Get-CimInstance` ซ้ำ).
7. teardown ตาม `TEMPLATE_teardown_generic.ps1`.

### pass criteria (สองชั้น)

ชั้น wire/DB:
- คอนโซลมีบรรทัด `BACKPACK_LOAD_REFUSED character Backpack state is missing` ภายในไม่กี่วินาทีหลังกด
  เข้าเกม.
- ไม่มี Python traceback ใด ๆ ขึ้นคอนโซลตรงจังหวะนี้.
- process เซิร์ฟเวอร์ (ProcessId ที่จดไว้) ยังรันอยู่หลังพยายามเข้าเกม.

ชั้น client-observable:
- หน้ารายการเลือกตัวละครโหลดปกติ ตัวละครที่ถูกลบกระเป๋าปรากฏในรายการ (ไม่ค้าง ไม่หาย).
- กด "เข้าเกม" แล้ว — ไม่คาดว่าจะเห็นอะไรต่างจาก "connecting" ค้าง (ฝั่ง client ไม่รู้จัก
  `BACKPACK_LOAD_REFUSED`) จนกว่า client ตายเองที่ ~3.5 นาที — **นี่คือ PASS ที่คาดไว้** ตราบใดที่ชั้น wire/DB
  ข้างบนผ่านครบ (การแก้รอบนี้อยู่ที่คอนโซล/เสถียรภาพของ process ไม่ใช่ประสบการณ์ผู้เล่น) ถ้าเห็นสัญญาณอื่นที่
  ชัดเจนกว่านั้น (error dialog ฯลฯ) ให้บันทึกเป็นข้อมูลใหม่ ไม่ใช่สิ่งที่คาด.

### nonclaims
- ใบนี้ไม่ทดสอบกรณีเนื้อหากระเป๋าดริฟต์ (ดูคำเตือนขอบเขตใน "ที่มา") — ยังเปิดเป็นงานคนละก้อน.
- ใบนี้ไม่พิสูจน์ว่าตัวละครนั้นเข้าโลกได้ — คาดว่าไม่ได้ ทดสอบแค่ว่าเซิร์ฟเวอร์ตอบสนอง (ทางคอนโซล) และไม่ตาย
  แทนที่จะพังเงียบ.
- ใบนี้ทดสอบกรณีแถวหัวหายทั้งแถวเท่านั้น ไม่ครอบคลุมรูปแบบพังอื่น (เช่น field นอกขอบเขต ที่ตอนนี้ถูกดัก
  ตั้งแต่ `require_backpack_shape` ด้วย `ValueError` — คาดว่าให้ผลเดียวกัน แต่ไม่ได้วัดในใบนี้).

### result (ผู้เทสกรอก)
```

```

## GT-101 GM-001 LOGIN-STATE-VISUAL-PROBE-001: ล็อกอินด้วยบัญชีในลิสต์ gm_accounts แล้ว GM_UpdateGMStateVital (0x5A19) ที่ CORE-REQUEST-006 ต่อสายเข้า login path แล้ว จอเปลี่ยนอะไรไหม  [RESULT -- ไม่ใช่ PASS/NO-RESULT/BLOCKED, ดูผลด้านล่าง] -- moved to `tickets/GT-101.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `43htls` 2026-09-07T00:09+07:00)

## GT-102 CORE-REQUEST-014 COLUMBUS-NPCCONVERSATION-QUEST3021-DIALOGUE-001: คลิก Columbus ที่ Port Royal (MOBS n_ID 156, bg0001 placement index 1) ครั้งแรกหลัง CORE-REQUEST-014 -- เห็นบทสนทนาเควสต์ 3021 จริงไหม (เมื่อวานคลิกแล้วเงียบ)  [**PARTIAL** -- เกรดโดย chief รอบ `wi1m62` 2026-08-29T01:0x+07:00 (ผู้เทสเสนอ `PARTIAL`/`PASS-WITH-FINDING`, chief เลือก `PARTIAL` เพราะคำถามหัวใบถามถึง**บทของเควสต์ 3021** ซึ่งยังไม่ถูกพิสูจน์) · `OBSERVER_CONFIRMED: 2026-08-29T00:17+07:00` · ที่ผ่าน: เส้น `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` (54 bytes) ยิงจริงครั้งเดียว หน้าต่างบทสนทนาเปิดจริงพร้อมสองออปชัน · ที่ยังไม่ผ่าน: ป้ายผู้พูด+เสียงพากย์+เนื้อบทเป็นชุดของ **Sebastian** ไม่ใช่ Columbus ⇒ ~~ชี้ขาดต้องถอดไบต์เฟรม 54 bytes ตรง ๆ = `RE-137`~~ **เส้นทางนี้ปิดแล้ว ไม่ใช่ตัวชี้ขาดอีกต่อไป** (chief `kj0s6r`/R346 2026-09-05T02:0x+07:00) · ผล: `notes_to_chief/20260829_0018_KA3A-*` ข้อ ② · 🔴 **คงสถานะ `PARTIAL` ต่อไป — ห้ามเกรดเป็น PASS** (ka1-A `20260905_0106` หมวด ค. เสนอเป็นนัยว่า `GT-106-R2`+`GT-131` ครอบแล้ว · **ตรวจแล้วไม่จริง**: จดหมายผล `GT-106-R2` (`consumed/20260831_1036`) บันทึกแค่ว่าหน้าต่าง Story ของ Columbus เปิดพร้อมตัวเลือก **ไม่บันทึกป้ายผู้พูด เสียงพากย์ หรือเนื้อบท** ซึ่งคือสามอย่างที่ใบนี้ค้าง · `GT-131` PASS เป็นป้ายชื่อสำมะโนเมือง คนละชั้นคนละเฟรม = ผิดกฎ G5) · **ตัวชี้ขาดใหม่ = ดูด้วยตาหนึ่งครั้งหลังตัวแก้ลง main**: `RE-137` ตอบแล้วว่าไคลเอนต์ประกอบชื่อ/เสียง/บทจาก `MOBS_TIP` ของ template ที่มันเชื่อว่า actor เป็น ไม่ใช่จาก quest id (`consumed/20260829_0238`) · และตัวแก้นั้น**อยู่บน production path แล้ว** — `world_face_frame.py:173` ส่ง `basic_name=identity.name` แทนเลข Mob-Set ของแถวแช่แข็ง (`:209` ระบุว่าอยู่บน production path · พินโดย `tests/test_face_frame_identity_contradiction.py`) ⇒ **ยังไม่มีใครมองป้ายผู้พูดหลังตัวแก้ลง** ราคาเทส ~5 วินาที พ่วงกับใบ Columbus ใบไหนก็ได้ · ต้องมี `OBSERVER_CONFIRMED` ก่อนเกรดเป็น PASS] -- moved to `tickets/GT-102.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `43htls` 2026-09-07T00:09+07:00)

## GT-103 GM-002 COMMAND-WIRE-CAPTURE-MATRIX-001: ล็อกอินด้วยบัญชี GM แล้วหา/เปิด GM editor widget พิมพ์ข้อความหลายแบบ -- capture file ของ `0x51E9` ขึ้นที่ `capture/gm_command_capture/` ไหม (path นี้ live บน production ครั้งแรกรอบนี้)  [NO-RESULT ต่อ claim ของตัวเอง -- A/B ทั้งสี่สถานะ UI เงียบสนิท, blocked on RE-126 · ปิดหัวใบโดย LANE-GM (เจ้าของใบ) รอบ `hs9m2r` 2026-08-28T17:1x+07:00 จากผล attended กะ1-A `notes_to_chief/20260828_1140_GT103AB-RESULT-NEGATIVE-four-ui-states-all-silent-RE118-panel-hypothesis-falsified.md` · OBSERVER_CONFIRMED: 2026-08-28T11:36-11:37+07:00 (BOOT_COMMIT `336857cd` = main HEAD, ไร้แฟล็ก) · เจ้าของคลิก `BT_GM` 4 สถานะ (HUD เปล่า / แผนที่เปิดค้าง / กระเป๋าเปิดค้าง / ปิดกระเป๋าแล้วคลิกซ้ำ) เงียบทุกครั้ง · สำมะโนเฟรมขาเข้าทั้งบูต `0x51E9` = 0 ⇒ `capture/gm_command_capture/` ABSENT ถูกต้องแล้ว ไม่ใช่ teardown fail ⇒ **ใบนี้ไม่เคยไปถึงข้อ 3 จึงไม่มีผลต่อ claim ของตัวเอง** · `TargetPosVital` x3 ช่วงเดียวกัน = client มีชีวิต ไม่ใช่เซสชันตาย · ผลข้างเคียงที่มีค่าสูง: สมมติฐานเชิงปฏิบัติของ RE-118 (เปิด panel ให้ current-UI key ไม่ว่าง) **ถูกหักล้าง** ⇒ เปิด `RE-126` ต่อ (ประตูบานแรก `this+0x48` แทนบานสุดท้าย) · [ไม่อ้าง] ว่า capture path ของ `0x51E9` ใช้ได้หรือไม่ -- ยังไม่เคยถูกทดสอบ live เลย · 🔴 **ทางเลี่ยง:** `GT-127` (คำสั่ง GM ผ่านกล่องแชท `0xAC52`) ไม่ต้องรอใบนี้และไม่ต้องรอ `RE-126`] -- archived 20260907 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md`, LANE-K round `kxpzxi`)

## GT-104 MOB-DEATH-002 WIDEN-DEATH-SCOPE-BG0001-FIRST-WIDENED-KILL-001: โจมตี field-mob ตัวหนึ่งใน bg0001 ที่ไม่ใช่ 0x201F จนถึง 0 HP บนบูตไร้แฟล็ก -- widening ruling ที่เพิ่งต่อสายทำให้ตายจริงบนจอไหม (ไม่ใช่ค้างที่ 0 HP ตลอดกาลแบบก่อนรอบนี้) และของดรอปตามมาปรากฏ/เก็บได้ไหม  [**NO-RESULT / BLOCKED-BY-FINDING** -- เกรดโดย chief รอบ `wi1m62` 2026-08-29T01:0x+07:00 · บูตแล้วจริงบน flagless `3baf65de` แต่**ไม่มีเฟรม attack/damage/death เกิดขึ้นเลยแม้แต่ครั้งเดียว**: คลิกซ้ายบน hostile placement (P33, P58) ถูกตอบด้วยเลนคุย NPC (`V98_NPC_FACE_PLAYER_POSITION_HEADING_P<n>` + `V98_NPC_CONVERSATION_DEFAULT_P<n>`) เปิดหน้าต่างบทสนทนาเปล่า ⇒ ไม่มีทางเข้าโหมดโจมตี · **สำมะโนไม่ใช่ครึ่งที่พัง** (`MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13`) · `RE-136` **ตอบแล้วในรอบเดียวกัน (ชั้นซอร์ส)** และคำตอบเปลี่ยนสถานะใบนี้: 🟢 **ใบนี้บูตซ้ำได้เลย ไม่ต้องรอโค้ดใหม่** -- moved to `tickets/GT-104.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `hf1gs9` 2026-09-06T23:17+07:00)
## GT-106 CORE-REQUEST-014-PARTIAL SCENE17-PROVISIONAL-ARRIVAL-001: เดินทางเข้าฉาก 17 (Bg1001, "เรือกลางทะเล") ด้วยพิกัดชั่วคราวที่เจ้าของเคาะเอง (0,0,0) -- ไคลเอนต์วางผู้เล่นได้อย่างเป็นปกติไหม หรือจมพื้น/หลุดขอบแมพ/ค้าง  [PENDING -- ไม่บล็อก M4/M5, ไม่ใช่การปิด CORE-REQUEST-014 เต็ม]

> เลขใบ: ตัวนับร่วมกับ CLIENT_RE_QUEUE.md, ยืนยัน 105 ว่าง ณ 2026-08-27T15:xx+07:00 (grep 0 hit ทั้งสองไฟล์
> รวม archive/) เปิดโดย chief รอบ `e0daaa`.

### ที่มา
`PANYA-DECISION 2026-08-27T14:45+07:00` (`notes_to_chief/20260827_1445_PANYA-DECISION-scene17-provisional-
arrival-xyz-0-0-0-owner-decree-ka1-B.md`) เจ้าของเคาะเองว่า scene 17 (Bg1001) ใช้พิกัดขาเข้าชั่วคราว
`(0,0,0)` ได้ ป้าย `PROVISIONAL-OWNER-DECREE-20260827-1445` -- **ไม่ใช่ค่าที่วัด** (`Bg1001.placements.tsv`
มีแค่ 8 แถว monster-spawn ไม่มีแถว player-arrival เลย) เป็นข้อยกเว้นครั้งเดียวของเจ้าของต่อกฎ "ห้ามปั้นพิกัด"
รอบ `e0daaa`: `scenarios/world_scene_registry_001.json` ใส่ spawn นี้แล้ว, `world_scene_entry.py`'s
`resolve_entry` พิมพ์ token `SCENE_ENTRY scene=17 xyz=0.000,0.000,0.000
source=PROVISIONAL-OWNER-DECREE-20260827-1445` ทุกครั้งที่ใช้ค่านี้จริง, `columbus_quest_dispatch.
resolve_columbus_arrival()` สำเร็จแล้ว (headless, ยืนยันด้วย `tests/test_columbus_quest_dispatch.py::
ResolveColumbusArrivalTests::test_succeeds_on_the_owner_decreed_provisional_spawn` และ wiring test คู่กัน)

### สองชั้นหลักฐาน
- **wire/DB (พิสูจน์แล้ว headless รอบนี้)**: `resolve_entry`/`resolve_columbus_arrival` คืนตำแหน่ง (0,0,0)
  ที่ scene 17 จริง ไม่ refuse อีกต่อไป พิมพ์ token ด้านบนจริง (grep ยืนยันที่ `<SHA>` ก่อนบูต:
  `git grep -n "PROVISIONAL-OWNER-DECREE-20260827-1445" <SHA> -- src/pirateforce_foundation`)
- **client-observable (ใบนี้ต้องตอบ)**: เข้าฉาก 17 ด้วยพิกัดนี้แล้วไคลเอนต์วางผู้เล่นที่ไหน -- ยืนบนผิวน้ำ/ดาดฟ้า
  ปกติ, จมพื้น, หลุดขอบแมพ, หรือค้าง/ไม่โหลดฉากเลย (n_SCENE_TYPE=4 "sea" ไม่เคยถูกส่งให้ไคลเอนต์เลยในโปรเจกต์นี้
  n_MARKER=0 ด้วย -- ไม่มีจุดขาเข้าที่ผู้พัฒนาเกมกำหนดไว้เลย)

### objective (claim เดียว)
เมื่อผู้เล่นถูกส่งเข้าฉาก 17 ด้วยพิกัดชั่วคราวของเจ้าของ ไคลเอนต์วางผู้เล่นในสภาพที่เล่นต่อได้จริงหรือไม่ --
ใบนี้ตอบแค่ "วางได้ปกติ" vs "วางแล้วมีปัญหา" เท่านั้น **ไม่ปิด** CORE-REQUEST-014 เต็ม (ครึ่งผูก vehicle ยัง
บล็อกด้วย RE-096 ที่เปิดอยู่ ไม่เกี่ยวกับใบนี้)

### nonclaim บังคับ (คำของเจ้าของ)
พิกัดขาเข้าฉาก 17 เป็นค่าชั่วคราวจากเจ้าของ ยังไม่พิสูจน์ว่าไคลเอนต์วางผู้เล่นบนผิวน้ำ/ในขอบแมพ -- ถ้าเข้าแล้ว
ตกขอบ/ค้าง **ให้รายงานเป็นผล ไม่ใช่ FAIL ของกฎ**

### ความเสี่ยงที่ pf-adversary พบ (รอบ e0daaa) -- บันทึกไว้ก่อนลอง อย่ารีบสรุป FAIL
- ไคลเอนต์อาจปฏิเสธ `TeleportVital` เงียบ ๆ ถ้า client-side FSM ไม่อยู่ state `StateRunTime`/`StateNavigation`
  ตอนที่เฟรมมาถึง (`RE-077` T3) -- ไม่มีใครวัด state ตอนคลิกเลือกบทสนทนาว่าเป็น state ไหน ถ้าผู้เล่นไม่ขยับเลย
  หลังคลิก นี่คือหนึ่งในสาเหตุที่เป็นไปได้ ไม่ใช่แค่ "โค้ดพัง"
- ยิงได้แค่ครั้งเดียวต่อ connection (`columbus_quest3021_dispatch_attempted` ล็อกถาวร) -- ถ้าครั้งแรกพลาด
  (เหตุผลข้างบนหรืออื่นใด) ต้อง disconnect/reconnect ใหม่เท่านั้น คลิกซ้ำจะไม่มีอะไรเกิดขึ้นเลย (เงียบสนิท
  ไม่มี event) อย่าคลิกซ้ำแล้วรอ ให้ reconnect แทน
- ก่อนถึงใบนี้ได้เลย ต้องผ่านประตูเควส (110/739/111 = Finish) ก่อน -- ดู `CHIEF-STATUS 20260827_1545` ว่า
  ยังไม่มีใครต่อสายให้ ถ้าไคลเอนต์ไม่ยอมให้เลือกตัวเลือกเควส 3021 เลย นั่นคือคำตอบของคำถามนั้น ไม่ใช่ของใบนี้

### หมดอายุ
ใบนี้ (และค่าพิกัดชั่วคราวเอง) ถูกแทนที่ทันทีที่ `RE-103` T3 มีหลักฐานจริง (client-observable capture หรือ
wire evidence ของจุดขาเข้าจริง) -- ตอนนั้นให้ปิดใบนี้และแก้ registry กลับเป็นค่าที่วัดจริง อย่าปล่อยให้ทั้งใบ
ชั่วคราวนี้และใบหลักฐานจริงเปิดพร้อมกัน

### addendum (pf-queue-author, เติมตอนเปิดใบเดียวกัน -- ห้ามแก้ข้อความเดิมด้านบน แค่เติมฟิลด์บังคับที่ขาด)

**เกตก่อนบูต (ด่าน 0 พิเศษของใบนี้):** ณ วันที่เปิดใบ **ไม่มีทาง production/debug ใดที่พาไคลเอนต์ไปถึง
ฉาก 17 ได้จริงในบูตเดียว** -- `dispatch_columbus_quest3021` refuse เสมอ (vehicle-bind gap `RE-096`,
ไม่เคยส่ง `TeleportVital` จริง), `--scene-load-scenario` เป็น allowlist ปิดเฉพาะฉาก 1/2
(`src/pirateforce_foundation/scene_load.py`) ไม่มีฉาก 17, เส้นทาง `gm_login_scene` ที่ `PANYA-ORDER
20260827_1425` เสนอไว้ (ทาง ก) ยังไม่ถูกเขียน (grep 0 hit ทั่ว `src/`) ก่อนบูตใบนี้ ต้อง grep สามคำสั่งนี้
บน `<SHA>` จริงก่อนเสมอ (ห้ามเชื่อบรรทัดนี้แทนซอร์ส):
```
git grep -n "gm_login_scene" <SHA> -- src/
git grep -n "expected_scene" <SHA> -- src/pirateforce_foundation/scene_load.py
git grep -n "resolve_columbus_arrival\|world_scene_entry.resolve_entry" <SHA> -- src/pirateforce_foundation/runtime.py
```
ไม่พบทางเข้าฉาก 17 จริงในบูตเดียว = ทั้งใบยังคง **PENDING -- รอ wiring ทางเข้าจริง** (ไม่ใช่ BLOCKED ถาวร
ไม่ใช่ NO-RESULT -- ยังไม่ได้ล็อกอินเลย) ห้ามเขียน `TeleportVital` มือเปล่า ห้ามแก้ `src/` เอง ไปทำใบอื่นแล้ว
กลับมาเช็คซ้ำ พบทางแล้ว -> จดชื่อ flag/config/commit ที่ใช้ได้ลงผลก่อนไปด่าน 1/2 มาตรฐาน
(`pf_resolve_green_boot.py --fetch` แล้ว grep ซ้ำบน `<SHA>` ที่บูตจริง)

### db (สำเนาเสมอ ห้ามเปิด canonical)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-106_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt105.sqlite3
```
เทียบ sha256 canonical กับ `CANON_SHA.txt` ก่อน/หลัง ต้องตรงทั้งสองครั้ง

### server args
ขึ้นกับเส้นทางที่ด่าน 0 พิเศษหาเจอจริง (flag/config ต่างกันไปตามทางที่ merge เข้ามา) -- **เขียนบรรทัดคำสั่งที่
ใช้จริงเป๊ะ ๆ ลงผลก่อนบูต** ห้ามคัดลอกจากใบอื่นเดา ห้ามพ่วง `--*-scenario` ตัวอื่นเข้าบูตเดียวกัน

### steps (คลิกต่อคลิก)
1. LOCK_GAME, ผ่านเกตด่าน 0 พิเศษ + ด่าน 1/2 มาตรฐาน, จด BOOT_COMMIT + คำสั่งบูตจริง
2. เข้าเกมด้วยเส้นทางที่พบ จนถึงจุดที่ `resolve_entry`/`resolve_columbus_arrival` ทำงานสำหรับฉาก 17
3. ยืนยันคอนโซลพิมพ์ `SCENE_ENTRY scene=17 xyz=0.000,0.000,0.000 source=PROVISIONAL-OWNER-DECREE-20260827-1445`
   ก่อนดูจอ -- ไม่มีบรรทัดนี้ = ยังไม่ถึงจุดที่ต้องสังเกต กลับไปด่าน 0
4. NO-CRASH: คลิกขวาลากกวาดกล้อง 360 องศา (ห้าม Q/E -- Q/E หันตัวละครจริงและยิง `TargetPosVital`; คลิกขวา
   ลากหมุนกล้องอย่างเดียวไม่ยิงอะไรออกสาย ปลอดภัยเสมอ)
5. บันทึก: ฉากโหลดสำเร็จไหม (ไม่ค้างจอดำ), มีพื้น/น้ำให้ยืนไหม, ผู้เล่นลอย/จม/ตกขอบไหม, HUD X/Y/Z ตรง
   (0,0,0) ไหม ถ่ายภาพนิ่ง full-res ของจอ + ป้ายชื่อตัวเอง
6. ลองเดิน (W/A/S/D คาดว่ายิง `TargetPosVital` ทุกครั้ง -- คาดหมาย ไม่ใช่ความเสี่ยง) 10-20 วินาที บันทึกว่า
   เคลื่อนที่ปกติหรือค้าง/ตกต่อ
7. NO-CRASH ซ้ำ -> teardown -> เทียบ sha canonical

### pass criteria (สองชั้น แยกกันเสมอ)
wire/DB: token `SCENE_ENTRY scene=17 xyz=0.000,0.000,0.000 source=PROVISIONAL-OWNER-DECREE-20260827-1445`
ปรากฏก่อนตัวละครถูกวาง (ปิดแล้วที่ headless ตาม tests ที่ "ที่มา" อ้างถึง -- ใบนี้แค่ยืนยันซ้ำว่าบูตจริงพิมพ์
บรรทัดเดียวกัน) + `sessions`/`max(lease_generation)` ไม่ถอยหลัง + sha256 canonical ตรงก่อน/หลัง +
`PRAGMA integrity_check`=ok
client-observable: อย่างใดอย่างหนึ่งที่เห็นจริง (ไม่เดา) -- ยืนบนผิวน้ำ/ดาดฟ้าปกติ, จมพื้น, ลอยกลางอากาศ,
หลุดขอบแมพ, หรือค้าง/ไม่โหลดฉากเลย + เดินได้ปกติไหม + สีป้ายชื่อทุกป้ายในทุกภาพ full-res (บรรทัดเดียวต่อป้าย,
"none" เขียนออกมาถ้าไม่มี, ห้ามชี้สาเหตุ -- `RE-067` เปิดอยู่) ผลลบ (ตกขอบ/ค้าง) มีค่าเท่ากับผลบวก ตาม
nonclaim บังคับด้านบนของใบนี้

### result (ผู้เทสกรอก)
```

```

### update (chief R197, kjtyku, 2026-08-27T19:15+07:00)

`COO-DECISION 20260827_1746`: M2 ยังไม่ผ่านจนกว่าจะแก้ 3 จุด — (1) persistence bug ที่ใบนี้พบ
(`character_positions` เขียน `scene_id=1` ผิดพร้อม XYZ ฉาก 17), (2) หลักฐานปลายทางฉาก 126 vs 17,
(3) ตัวเลือกเควส 3205 ใน dialog Columbus **จุดที่ 1 ต่อสายแล้วรอบนี้** (`CORE-REQUEST-018`,
`pirate-force-server@9c920f4`+`fe89b55` -- รอ merge PR) จุดที่ 2/3 ยังไม่เสร็จ (งานสาย A/GM-RE)
**`GT-106-R2` ยังไม่เปิด** จนกว่าจะครบทั้งสามตามที่ COO สั่งไว้กับ chief โดยตรง

**update (chief รอบ n2ws3l / R198, 2026-08-27T20:14+07:00)**: จุดที่ 2 ปิด BOUNDED-NEGATIVE แล้ว
(`RE-096`/`RE-103`, ก่อนรอบนี้) และจุดที่ 3 ต่อสายแล้วรอบนี้ (`CORE-REQUEST-019`,
`pirate-force-server@aeccaa0` -- รอ merge PR, ตัวเลือกที่ 2 refuse เสมอโดยตั้งใจ) **ครบทั้ง 3 จุดของ
`COO-DECISION 1746` แล้วในแง่ server-side wiring** แต่ **`GT-106-R2` ยังไม่เปิดในรอบนี้** — chief ไม่ใช่คนตัดสิน
ว่า attended พร้อมรันเมื่อไหร่ (ต้องรอ PR ทั้งสองใบ merge เข้า `main` ก่อน) ให้ COO/pf-queue-author เป็นคนเปิด
`GT-106-R2` อย่างเป็นทางการเมื่อพร้อม

**update (chief รอบ `bunu7v` / R246, 2026-08-30T19:2x+07:00)**: `RE-162` (สืบวันนี้ ตาม `PANYA-ORDER`
คำถามคนละเรื่อง -- เปลี่ยนแมพกลางเซสชันทั่วไป) วัดซ้ำอิสระว่า `_dispatch_columbus_quest3021` ยังคงส่ง
`TeleportVital` ข้ามฉากจริงขณะออนไลน์ (ไม่ใช่แค่ตอนล็อกอิน) และเป็นกลไกเดียวกับที่ใบนี้ต้องการวัดผล
client-observable -- ตัวใบนี้เองยังไม่ถูก COO/pf-queue-author เปิด `GT-106-R2` อย่างเป็นทางการ **chief ไม่เปิด
เองรอบนี้** (นอกเขตตัดสินใจ ตามที่ R198 บันทึกไว้) แต่ยกให้ COO พิจารณาอีกครั้งว่า wiring วันนี้ (3 จุดของ
`COO-DECISION 1746` + Columbus dispatch ที่ `RE-162` เพิ่งยืนยันซ้ำ) พร้อมเปิด `GT-106-R2` หรือยัง --
ดู `notes_to_chief/20260830_1909_RE-162-RESULT-*.md` Job 3(B) สำหรับเกตทั้งหมดที่ต้องผ่านก่อนถึงจุดสังเกต

---

## GT-106-R2 COO-DECISION-20260830-2048 IN-SESSION-TELEPORT-RENDER-001: เมื่อ TeleportVital ข้ามฉากมาถึงกลางเซสชัน (ผ่าน _dispatch_columbus_quest3021 หลังคลิกเควส 3021 ของ Columbus ไม่ใช่ตอน login) ไค... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-107 GM-001-R2 LOGIN-STATE-VISUAL-PROBE-002: ล็อกอินด้วยบัญชี GM อีกครั้งหลัง RE-105 พิน vital_version=0 (CORE-REQUEST-016 เปิดแล้ว) -- เซสชันรอดจาก error 23065 ที่ GT-101 เจอไหม แล้วจอเปลี่ยนอะไรไหม (คำถามเดิมของ GT-101 ที่ยังไม่มีใครตอบได้เพราะเซสชันตายก่อนถึง)  [RESULT -- NEGATIVE, new failure mode, error 28317, see notes_to_chief/20260827_1745_GT107-RESULT-NEGATIVE-vital-version-0-passes-version-check-but-client-throws-28317-RunTimeProtocolRes-read-failed-session-dies-GT103-not-reached-ka1-B.md -- superseded by GT-107-R3 below] -- archived 20260907 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md`, LANE-K round `kxpzxi`)

## GT-109 VEHICLE-BIND-WIRE-CAPTURE-001: ผู้เล่นขึ้นพาหนะ/กลายเป็นเรือครั้งแรก (หรือกลไกใดก็ตามที่เรียก CGCVehicleModule) -- จับเฟรม CVehicleVital (handler 0x00710440, tag 0x32 @object+0x18) จริงได้ทั้งสองทิศไหม (RE-096 ปิด bounded-negative แล้ว เพดาน static หมด เหลือแค่ attended capture)  [PENDING -- รอ wiring ทางเข้า vehicle-bind จริง, ไม่ใช่ BLOCKED ถาวร; ไม่บล็อก M2]

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md. grep ยืนยันก่อนจอง (2026-08-27): เลขล่าสุดที่ถูกใช้จริงคือ
> GT-107 (GAME_TEST_QUEUE.md) และ RE-108 (CLIENT_RE_QUEUE.md, เปิดโดยสาย B รอบ B_20260827_1637) -- GT-108/GT-109/
> RE-109 = 0 hit ทั้งสองไฟล์รวม archive/ ⇒ **ใบนี้คือ GT-109**. เลขว่างถัดไปหลังใบนี้ = 110.
> ใบเก่าทุกใบอยู่ที่เดิม ห้ามแตะ. เปิดโดย pf-queue-author ตามคำขอสาย A รอบ `jafskv`.

### ที่มา (อ้างอิงไฟล์แทนอธิบายซ้ำ)
- `RE-096` CLOSED bounded-negative (`CLIENT_RE_QUEUE.md` ~L213; เต็ม:
  `notes_to_chief/20260827_0509_RE-096-RESULT-NO-VEHICLE-SEASCENE-CROSSWALK.md`): handler `0x00710440` เป็น
  stub 5 ไบต์ `mov al,1; ret 4` เท่านั้น ไม่อ่าน/เขียน/lookup ตารางใด; capture `NOT_OBSERVED` 0/0 เฟรมทั้งสองทิศ
  ในทุกคลังที่มี; ปิดใบเขียนตรงๆ ว่า "ทางเดียวที่เหลือคือ attended capture ของ `CVehicleVital` เฟรมจริง"
- `RE-085` (`notes_to_chief/20260827_0156_RE-085-RESULT-SAME-ACTOR-VEHICLE-MODULE.md`): vehicle state เป็น
  actor-local (`CGCVehicleModule` ผูก actor เดิมกับ `CVehicleAttr`) แต่จุดเรียกที่พบมีจุดเดียวคือภายใน
  `dispatch_columbus_quest3021` -- ไม่พบ trigger อื่น (nonclaim ตรงๆ)
- คำเคาะเจ้าของ `M2-NO-VEHICLE-OWNER-20260827-1525` (`notes_to_chief/20260827_1545_CHIEF-STATUS-M2-quest-gate-skip-needs-bridge-RE-not-cloud-buildable.md`
  ข้อ 2, ยืนยันซ้ำ `notes_to_chief/20260827_1830_CHIEF-REPLY-PANYA-CHASE-0915-status-faction1-wired-M2-plan-RE100-coverage.md`):
  ยืนยันตรงกับซอร์สจริง (`src/pirateforce_foundation/columbus_quest_dispatch.py`, ค่าคงที่
  `VEHICLE_BIND_REFUSED_NO_VEHICLE_ROW` ยังอยู่ในไฟล์แต่ **ไม่มีจุดเรียกใช้เหลือเลย** -- ตรวจเองรอบ `jafskv`):
  `dispatch_columbus_quest3021` **ไม่รอ vehicle-bind อีกต่อไป** -- สำเร็จและส่ง `TeleportVital` ตรงๆ โดยข้าม
  จุดเรียก vehicle-bind ที่ `RE-085` เจอไปเลย ("แผนเต็ม M2 spec table" ที่จะเอา vehicle-bind กลับมา ยังไม่เขียน)

### objective (claim เดียว)
capture เฟรม `CVehicleVital` (tag `0x32`, 8 ไบต์ @`object+0x18`, serializer `0x006C0180-0x006C01A3`,
handler `0x00710440`) จากการเล่นจริงอย่างน้อยหนึ่งครั้งทั้งสองทิศทาง client->server (W) และ server->client (R)
เมื่อผู้เล่นขึ้นพาหนะ/กลายเป็นเรือ -- **ไม่ตัดสิน semantic ของ `+0x18`** (นั่นคืองานของ RE follow-up ที่จะเปิด
เลขใหม่หลังใบนี้จับได้)

### เกตก่อนบูต (ด่าน 0 พิเศษ -- เข้มกว่า GT-106)
ประกาศตรงๆ: **ไม่มีทาง production/debug ใดในซอร์สที่ commit ไว้ตอนนี้ที่จะยิง `CVehicleVital` ได้เลย** เพราะ
จุดเรียกเดียวที่เคยมี (`RE-085` T1/T3) ถูกถอดออกจาก `dispatch_columbus_quest3021` ตาม
`M2-NO-VEHICLE-OWNER-20260827-1525`. grep สามคำสั่งนี้บน `<SHA>` จริงก่อนบูตทุกครั้ง (ห้ามเชื่อบรรทัดนี้แทนซอร์ส):
```
git grep -n "no_re096_vehicle_row_evidence\|vehicle_row\|vehicle_bind" <SHA> -- src/pirateforce_foundation/columbus_quest_dispatch.py
git grep -n "CVehicleVital\|0x00710440\|0x006C0180" <SHA> -- src/pirateforce_foundation/
git grep -n "gm_login_scene\|login_scene_override" <SHA> -- src/pirateforce_foundation/runtime.py
```
- คำสั่งที่ 1 = เจอเฉพาะนิยามค่าคงที่ (ไม่มี `.append`/จุดเรียกใช้จริง) = สถานะปัจจุบัน (vehicle-bind ยังไม่ถูก
  ใส่กลับเข้า dispatch)
- คำสั่งที่ 2 เจอ call site ใหม่ (ไม่ใช่แค่ registry/serializer ที่มีอยู่แล้วเป็นข้อมูลนิ่ง) = สัญญาณทางเข้าใหม่ --
  อ่าน diff จริงก่อนเชื่อ
- คำสั่งที่ 3 = 0 hit หมายความว่า GM login-scene override (`notes_to_chief/20260827_1524_LANE-GM-CORE-REQUEST-015-login-scene-override-wiring.md`,
  ทาง ก ของ `PANYA-ORDER 20260827_1425`) ยังไม่ถูกเรียกจาก `runtime.py` เลย (module มีแล้ว 0 call site) --
  **ถึงจะต่อสายก็ไม่ช่วยใบนี้โดยอัตโนมัติ**: `RE-085` ยืนยันว่า vehicle-bind logic ผูกอยู่เฉพาะใน
  `dispatch_columbus_quest3021` เท่านั้น ยังไม่มีหลักฐานว่าการเข้าฉาก 17 เปล่าๆ (ไม่ผ่าน dispatch) จะยิง
  `CVehicleVital` เอง

ไม่พบทางเข้าใดที่ยิง `CVehicleVital` ได้จริง = ทั้งใบยังคง **PENDING -- รอ wiring ทางเข้าจริง** ห้ามแก้ `src/`
เอง ห้ามปั้นเฟรมมือเปล่า ไปทำใบอื่นแล้วกลับมาเช็คซ้ำ พบทางแล้ว -> จดชื่อ flag/commit ที่ใช้ได้ลงผลก่อนไปด่าน 1/2
มาตรฐาน (`pf_resolve_green_boot.py --fetch` แล้ว grep ซ้ำบน `<SHA>` ที่บูตจริง)

### หมายเหตุ dependency (ไม่ใช่ gate เดียวกันเป๊ะกับ GT-106) + หลักฐานเพิ่มที่เพิ่งมีจริง

`GT-106` (คุณภาพการวางตัวละครที่ฉาก 17) ตอนนี้ gate เบากว่าใบนี้แล้ว เพราะ `M2-NO-VEHICLE-OWNER-20260827-1525`
ทำให้ `dispatch_columbus_quest3021` สำเร็จได้โดยไม่ต้องมี vehicle-bind -- **`GT-106` PASS ไม่ปลดล็อกใบนี้
อัตโนมัติ** เพราะ path ที่ `GT-106` ใช้ข้าม vehicle-bind ไปเลยตามคำสั่งเจ้าของ ใบนี้จะรันต่อได้ทันทีเมื่อ:
(ก) "แผนเต็ม M2 spec table" เอา vehicle-bind กลับเข้ามาใน `dispatch_columbus_quest3021`, หรือ
(ข) มีคนพบ trigger อื่นที่ยิง `CGCVehicleModule`/`CVehicleVital` ได้จริง (ดูหัวข้อถัดไป)

**update (ยืนยันหลัง `GT-106` รันจริงแล้ว 2026-08-27T17:10+07:00)**: ผล `GT-106` (`notes_to_chief/
20260827_1710_GT106-RESULT-M2-Columbus-3021-enters-scene17-*.md` ③) เดินเส้นทาง Columbus -> ฉาก 17 จริงและ
ให้ raw wire log ครบ (`server_console_live.out.txt` 4,031 บรรทัด) -- **frame ที่ client ส่งหลัง teleport มีแค่
`TargetVital`x1, `TargetPosVital`x10, `COnLandVital`x8, `ActionVital`x3 ไม่มี `CVehicleVital` เลยสักเฟรม**
นี่คือหลักฐาน de-facto บวกกับ `RE-096`/gate-0 ของใบนี้ (ยังไม่มีทางเข้าใดยิงเฟรมนี้จริง) แต่ **ไม่ใช่ผลของใบนี้
เอง** (`GT-106` ไม่ได้ตั้งใจสังเกต `CVehicleVital` และไม่ได้บันทึกทุกเฟรมแบบ raw capture ตามที่ใบนี้ต้องการ) --
ใบนี้ยังคง `PENDING` รอ capture ที่ตั้งใจสังเกตเฟรมนี้โดยเฉพาะ (ขั้น 5 ของใบนี้) ไม่ใช่ผลพลอยได้จากรอบอื่น

### ทางเลือกอื่น (เปิดเป็นคำถาม -- ห้ามอ้างว่ามีจริงถ้ายังไม่เจอ)
`RE-085` พบว่า `CGCVehicleModule`/`CVehicleAttr` เป็นกลไก actor-local ทั่วไป (ผูกกับ actor เดิม ไม่ใช่ scene
fixture) แต่ nonclaims ของใบนั้นเขียนตรงๆ ว่าไม่ได้พิสูจน์ trigger อื่นนอกเหนือจาก `dispatch_columbus_quest3021`.
คำถามเปิด: มีเมนู/ไอเทม/สกิล/GM command ใดในไคลเอนต์ที่เรียกกลไกนี้ได้โดยไม่ต้องผ่านฉาก 17 หรือไม่ (เช่น
พาหนะบก/ม้า) -- ถ้าผู้เทสบังเอิญเจอระหว่างสำรวจ UI ตามปกติ (ไม่ใช่การเดา ไม่ใช่การลองสุ่มนอกขอบเขตใบ) ให้บันทึก
เป็น finding แยกและแจ้ง RE runner เปิดใบใหม่ -- **ใบนี้เองไม่อ้างว่าเส้นทางนี้มีจริง**

### nonclaims
- ไม่ตัดสิน semantic ของ qword `+0x18` (vehicle catalog id? model id? อื่น?) -- งานของ RE follow-up
- ไม่ตัดสินว่า `VEHICLE` row หรือ `SHIP` row ใดถูกใช้จริง (นั่นคือของเดิมที่ `RE-096` ปิดไปแล้วว่าตอบไม่ได้)
- ไม่ตัดสินคุณภาพการวาง player ที่ฉาก 17 (นั่นคือ `GT-106`)
- ไม่อ้างว่ามีเส้นทางพาหนะบก/ม้าจนกว่าจะเจอจริงระหว่างทดสอบ
- ผลลบ (บูตถึงจุดที่ควรยิงแต่ capture ว่างเปล่าทั้งสองทิศทาง) **มีค่าเท่าผลบวก** -- แปลว่า trigger ที่ใช้ไม่ใช่
  ตัวที่ยิง `CVehicleVital` จริง หรือ handler stub ไม่เคยถูกเรียกแม้ code path จะถึงจุดนั้น ทั้งสองเป็น finding
  ที่ป้อนกลับให้ RE follow-up ไม่ใช่ FAIL ของใบนี้

### db (สำเนาเสมอ ห้ามเปิด canonical)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-109_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt109.sqlite3
```
เทียบ sha256 canonical กับ `CANON_SHA.txt` ก่อน/หลัง ต้องตรงทั้งสองครั้ง

### server args
ขึ้นกับเส้นทางที่ด่าน 0 หาเจอจริง (ตอนนี้ยังไม่มีเส้นทางเลย) -- **เขียนคำสั่งบูตจริงที่ใช้ลงผลก่อนเสมอ** ห้าม
คัดลอกจากใบอื่นเดา ห้ามพ่วง `--*-scenario` ตัวอื่นเข้าบูตเดียวกัน

### steps (คลิกต่อคลิก -- กรอกเฉพาะเมื่อด่าน 0 ผ่านแล้ว)
1. LOCK_GAME, ผ่านเกตด่าน 0 พิเศษ + ด่าน 1/2 มาตรฐาน, จด BOOT_COMMIT + คำสั่งบูตจริง
2. เข้าเกมจนถึงจุดที่ทางที่พบจริงพาไปเรียก vehicle-bind logic -- บันทึกว่าเป็นเส้นทางไหน (dispatch คืนสาย /
   GM login-scene override + trigger อื่น / อื่นใด)
3. NO-CRASH: คลิกขวาลากกวาดกล้อง 360 องศา (ห้าม Q/E -- Q/E หันตัวละครจริงและยิง `TargetPosVital`; คลิกขวาลาก
   หมุนกล้องอย่างเดียวไม่ยิงอะไรออกสาย ปลอดภัยเสมอ)
4. ถ่ายภาพนิ่ง full-res ก่อน/หลังจุดที่คาดว่าจะยิงเฟรม + สีป้ายชื่อทุกป้ายในภาพ (บรรทัดเดียวต่อป้าย, "none"
   เขียนออกมาถ้าไม่มี, ห้ามชี้สาเหตุ -- `RE-067` เปิดอยู่)
5. เก็บ raw capture ทั้งชุดทันทีหลังจุดนั้น (ตามแบบ `capture_gt031_*`/`capture_gt032_*` ใน
   `external/PF_INPUT_INVENTORY.tsv`): `capture_gt109_<yyyyMMdd_HHmmss>/capture_v141/GAME_LIVE.txt`,
   `GAME_EVENTS_LIVE.txt`, `server_console_live.out.txt`/`.err.txt`, ทุกบรรทัด `[G>]`/`PF-EVENT`/`ErrorData`
6. NO-CRASH ซ้ำ -> teardown -> เทียบ sha canonical -> sha256 ทุกไฟล์ capture

### pass criteria (สองชั้น แยกกันเสมอ)
wire/DB: raw capture ที่เก็บในขั้น 5 มี frame instance อย่างน้อยหนึ่งเฟรมต่อทิศทาง ที่ไบต์ตรงกับ span
serializer `0x006C0180-0x006C01A3` (tag `0x32`, 8 ไบต์, handler_va `0x00710440`) -- ทั้ง W (client->server)
และ R (server->client) ต้องมีอย่างน้อยทิศทางละ 1 เฟรม (การยืนยันไบต์จริงเป็นงานของ RE follow-up ไม่ใช่ผู้เทส --
ผู้เทสแค่ต้องเก็บ raw log ให้ครบไม่หาย/ไม่โดนล้าง) เมื่อ RE follow-up ยืนยันแล้ว `PF_FIELD_VALIDATION.tsv` แถว
`CVehicleVital W`/`R` เปลี่ยนจาก `NOT_OBSERVED` (0/0 เฟรม) เป็น `observed_frames > 0` + sha256 canonical
ตรงก่อน/หลัง + `PRAGMA integrity_check`=ok
client-observable: อย่างใดอย่างหนึ่งที่เห็นจริง (ไม่เดา) -- ตัวละครเปลี่ยนโมเดล/ขึ้นพาหนะที่เห็นได้บนจอ, หรือ
**ไม่มีอะไรเปลี่ยนบนจอเลยแม้ log จะมีเฟรม** (ทั้งสองผลมีค่าเท่ากัน ไม่ใช่ FAIL ของใบนี้ -- ดู nonclaim ผลลบ
ด้านบน) + สีป้ายชื่อทุกป้ายในทุกภาพ full-res บันทึกตามกฎ `RE-067`

### result (ผู้เทสกรอก)
```

```

---

## GT-110 CORE-REQUEST-017-1 GM-LOGIN-SCENE-OVERRIDE-VISUAL-001: per-account login-scene override, wired into START_GAME_REQ -- does a real client actually render the overridden scene on login  [PARKED -- ไม่ใช่ทางวิกฤต: ความสามารถซ้ำกับ seed run-DB ที่พิสูจน์แล้ว 3 รอบ (M1-P, GT-116/121/120) · ไม่มีเนื้อหา GM เหลือหลัง SAFETY FIX 28 ส.ค. (ใบนี้เดินทาง standalone `PF_GM_LOGIN_SCENE_STANDALONE_CONFIG` ⇒ `is_gm` = False ตลอดใบ ไม่มี 0x5A19 ไม่มี GM command surface) · พักตามคำสั่งเจ้าของ `notes_to_chief/20260828_1105_PANYA-ASK-LANE-GM-*.md` ข้อ 1(ก)/1(ข) ดำเนินการโดย LANE-GM (เจ้าของใบ) รอบ `hs9m2r` 2026-08-28T17:1x+07:00 · **ห้ามลบใบ ห้ามย้ายตำแหน่ง** · ถอดออกจากงบรอบของสาย GM แล้ว -- ชื่อใบ `GM-LOGIN-SCENE-OVERRIDE-VISUAL-001` ไม่ตรงเนื้อจริง ควรเป็นใบฟีเจอร์เซิร์ฟเวอร์ธรรมดา (chief จัดสาย, ข้อ 1(ข) ADDRESSEE: chief) · ถ้าจะรันในอนาคตต้องเขียน objective ใหม่ให้ตรงคำถามที่เหลือจริง = "เฟรม resync กลางคันใช้ได้กับ client จริงไหม" ไม่ใช่ "GM วาร์ปได้ไหม" (ข้อ 1(ค)) · ประวัติเดิมขีดฆ่า ไม่ลบ: หัวใบเดิมคือ `[PENDING -- safety fix 2026-08-28: now runs on the standalone path, no GM_UpdateGMStateVital/0x5A19 sent, no longer waits on GT-107-R3, see server args below]`]

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md. จองไว้เป็น GT-109 ตอนแรก (grep ยืนยัน ณ ขณะนั้น: 0 hit)
> แต่ LANE-A จองเลขเดียวกันพร้อมกัน (รอบ jafskv, VEHICLE-BIND-WIRE-CAPTURE-001) และ commit ของเขาลง
> main ก่อน (เจอตอน merge conflict ของ PR รอบนี้) ⇒ ใบนี้ขยับเป็น GT-110 ตามกฎ "ชนแล้วห้ามทับ" ใบ GT-109
> ของ LANE-A อยู่ก่อนหน้าในไฟล์นี้ ไม่มีอะไรถูกย้ายหรือแก้

- objective: (claim เดียว) เมื่อบัญชี GM ถูกลงทะเบียนทั้งใน config/gm_accounts.json (หรือ
  PF_GM_ACCOUNTS_CONFIG) และ config/gm_login_scene.json (หรือ PF_GM_LOGIN_SCENE_CONFIG) ชี้ไป scene_id ที่รู้จัก
  GameClient จริงจะ render ฉากที่ override ไว้บนจอไหม -- ฉาก/พื้นถูกต้องตรงกับ scene_id นั้น ตัวละครยืนที่จุด
  spawn ที่ปักหมุดของฉากนั้น ไม่มี glitch -- แทนที่จะเป็นฉากเดิมที่บัญชีนั้นเคยบันทึกไว้ นี่คือสิ่งเดียวที่ยังไม่ถูก
  พิสูจน์: การสลับค่าฝั่งเซิร์ฟเวอร์เอง (login_scene_override.py ต่อสายเข้า runtime.py's START_GAME_REQ
  handler รอบนี้) พิสูจน์แบบ headless แล้วผ่าน tests/test_gm_login_scene_override_wiring.py (6/6 ข้อ ขับผ่าน
  dispatcher จริง รวมเทสระดับไบต์ที่ยืนยันว่าเฟรม ActorAttr/MovementAttr กับ teleport ตรงกัน ไม่ใช่แค่ teleport
  ฝ่ายเดียว -- pf-adversary สองรอบ พบบั๊กจริงในดราฟต์แรกและแก้แล้ว) full suite เขียว(cloud sanity) ไม่มี
  regression -- ใบนี้ไม่พิสูจน์ซ้ำส่วนนั้น ถามแค่ว่ามนุษย์ที่จอเห็นผลจริงไหม

- db: default_state\pirateforce.sqlite3 (สำเนาเท่านั้น ห้ามแตะตัวจริง) สำเนาไป
  pf_bridge\backup\pirateforce_before_GT-110_<yyyyMMdd_HHmmss>.sqlite3 แล้วไป state\run_gt109.sqlite3
  sha256 ของ canonical เทียบกับ CANON_SHA.txt ทั้งก่อนและหลัง · PRAGMA integrity_check=ok บนสำเนาที่ใช้ทำงาน
  ทั้งสองครั้ง

> 🔧 SAFETY FIX 2026-08-28 (LANE-GM, answering
> `notes_to_chief/20260827_2240_KA1A-NOTE-GT110-unsafe-until-0x5A19-payload-fixed-plus-M1P-jobs-staged.md`):
> the original server-args below required `gm_accounts.json` membership,
> which makes `is_gm_account()==True`, which makes `runtime.py` send
> `GM_UpdateGMStateVital` (`0x5A19`) on login -- the exact frame that killed
> `GT-101`/`GT-107` with two different crash modes, one fixed (`RE-113`) but
> **not yet re-verified against a real client** (`GT-107-R3` still
> `[PENDING]`). Running GT-110 the old way risked a third crash for a
> question this ticket never needed to ask. `gm/login_scene_override.py`
> now has a second, independent "standalone" path
> ([สมมติของสาย GM - รอ COO ยืนยัน], see module docstring) that grants a
> login-scene override WITHOUT any `gm_accounts.json` entry -- `is_gm`
> stays `False` for this account, so the `0x5A19` block in `runtime.py`
> never fires. Server args below now use ONLY the standalone path. GT-107-R3
> stays the ticket that answers whether `0x5A19` itself is now safe -- this
> ticket no longer needs that answer first.

- server args:
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
$env:PF_GM_LOGIN_SCENE_STANDALONE_CONFIG = "<สำเนาทิ้งใต้ pf_bridge\backup\ map บัญชีทดสอบ -> scene_id 2, key 'standalone_login_scene'>"
py -3 -u -m pirateforce_foundation.app --db state\run_gt109.sqlite3
```
  ไม่มีแฟล็ก --*-scenario ใด ๆ -- override ขับด้วย config รอบนี้ ไม่ใช่ scenario-gated **ห้ามตั้ง**
  `PF_GM_ACCOUNTS_CONFIG` หรือแก้ `config/gm_accounts.json` ตัวจริงเลยในใบนี้ -- ปล่อยให้ allowlist ว่างเป็นค่า
  เริ่มต้น (ไม่มีใครเป็น GM) ตามที่ทางแก้นี้ตั้งใจ ห้ามแก้ `config/gm_login_scene.json` หรือ
  `config/gm_login_scene_standalone.json` ตัวจริง ให้ env var ชี้ไปสำเนาทิ้งแล้วลบตอน teardown

  เงื่อนไขก่อนบูต ต้องผ่านก่อนเปิดเกม ไม่งั้นทั้งใบ BLOCKED (ไม่ใช่ NO-RESULT):
  1. resolve commit ที่บูตเขียวตามวิธีมาตรฐานของ repo แล้วยืนยันว่า commit นั้นมีของรอบนี้จริง:
     git grep -n "login_scene_override" <SHA> -- src/pirateforce_foundation/runtime.py
     git grep -n "gm_login_scene_override_applied_" <SHA> -- src/pirateforce_foundation/gm/login_scene_override.py
     git grep -n "gm_login_scene_override_lookup_failed_" <SHA> -- src/pirateforce_foundation/gm/login_scene_override.py
     git grep -n "load_standalone_login_scene_overrides" <SHA> -- src/pirateforce_foundation/gm/login_scene_override.py
     git grep -n "PF_GM_LOGIN_SCENE_STANDALONE_CONFIG" <SHA> -- src/pirateforce_foundation/gm/login_scene_override.py
     ผลลัพธ์ 0 hit ข้อไหน = BLOCKED ห้ามบูต
  2. ยืนยันว่าบัญชีทดสอบที่จะใช้ **ไม่อยู่** ใน `config/gm_accounts.json` จริง (ไฟล์ต้องไม่มีอยู่ หรือมีแต่ allowlist
     ว่าง) -- นี่คือสิ่งที่ทำให้ทางแก้นี้ปลอดภัยจาก `0x5A19`, ห้ามเดาว่า "ว่างอยู่แล้ว" ต้องเปิดไฟล์ดูจริงก่อนบูต
  3. ห้ามชี้ `PF_GM_LOGIN_SCENE_STANDALONE_CONFIG` ไปที่ scene_id=17 หรือฉากใดที่ปักหมุด
     login_entry_allowed=False -- จะทำให้
     ~~login ทั้งครั้งถูกปฏิเสธไม่มี reply เลย (client ค้างที่ "connecting" ตลอดไป) ซึ่งเป็นพฤติกรรม fail-closed
     ที่ตั้งใจ ไม่ใช่บั๊ก แต่เผารอบทดสอบทิ้งเปล่า ๆ~~ **แก้แล้วบางส่วน รอบ `qq0i9u` (LANE-GM เจ้าของใบ)
     2026-08-29T09:2x+07:00 — ข้อห้ามยังอยู่เต็มร้อย โทษเปลี่ยนเฉพาะบางกรณี:** `gm/login_scene_admission.py` ปฏิเสธใบแบบนั้น
     **ตอนอ่านไฟล์ config** ⇒ ล็อกอินไม่ถูกปฏิเสธอีกแล้ว บัญชีเข้าเกมที่แถวของตัวเอง (ฉาก 1) และคอนโซล stderr
     พิมพ์ `GM_LOGIN_SCENE_CONFIG_REFUSED path=... account=... scene_id=17 reason=no_pinned_login_entry
     stageable=(1, 2, 278, 997)` · ⚠️ ยังไม่ได้แปลว่าให้ตั้งค่าผิดได้ตามใจ: override ทั้งไฟล์จะไม่ทำงานเลย
     จนกว่าจะแก้บรรทัดที่ผิด (fail-closed ทั้งแฟ้ม ไม่ใช่ข้ามทีละบรรทัด) ⇒ ใบนี้จะได้ฉาก 1 ไม่ใช่ฉากที่ตั้งใจ
     · **ยังไม่เคยวัดกับ client จริง** — วัดผ่าน dispatcher จริงในชุดเทสเท่านั้น (`pirate-force-server`
     `tests/test_gm_login_scene_admission.py`, `tests/test_gm_login_scene_override_standalone_at_login.py`)
     🔴🔴 **และยังล็อกเอาต์ได้อยู่ในกรณีหนึ่ง อย่าถือว่าปลอดภัยแล้ว** (`pf-adversary` วัดรอบ `qq0i9u`):
     `runtime.py:527` อ่านทะเบียนฉาก **ครั้งเดียวตอนบูต** ส่วนด่านรับเข้าอ่านดิสก์ใหม่ทุกล็อกอิน ⇒ ถ้ามีคน
     แก้ `scenarios/world_scene_registry_001.json` ให้ **กว้างขึ้น** หลังเซิร์ฟเวอร์บูตแล้ว (พลิก
     `login_entry_allowed` เป็น true · เติม spawn · เพิ่มปลายทาง) ล็อกอินจะถูกปฏิเสธไม่มี reply แบบเดิมทุกไบต์
     **และโทเคน `GM_LOGIN_SCENE_CONFIG_REFUSED` จะไม่พิมพ์** ⇒ กติกาสำหรับใบนี้: **ห้ามแก้ทะเบียนฉาก
     ระหว่างที่เซิร์ฟเวอร์รันอยู่ ถ้าแก้ต้องรีสตาร์ตก่อนบูตเกม** · ปลดข้อนี้เมื่อ `CORE-REQUEST-GM-034`
     (ใบ `20260829_0944`) ลง main
     🔴 **แก้คำรอบ `7gplcy` 2026-08-29T10:4x+07:00 (LANE-GM เจ้าของใบ) — ข้อห้ามข้อ 3 กลับไปเต็มโทษเหมือนเดิมชั่วคราว:**
     ย่อหน้า `qq0i9u` ข้างบนเขียนไว้เหมือนว่า `gm/login_scene_admission.py` อยู่บน main แล้ว **ไม่จริง ขอถอน**
     `pirate-force-server#249` `state=closed merged=false` — เกต Windows แดง แล้ว `merge-claude-pr.yml` ปิด PR ทิ้งทั้งใบ
     (จดหมายของรอบนั้นขึ้น main จริงทาง `pf_bridge#389` โค้ดไม่ขึ้น — นี่คือเหตุผลที่ต้องวัดด้วย `merged_at` ไม่ใช่ด้วยจดหมาย)
     ⇒ **วันนี้ชี้ standalone ไปที่ scene_id=17 แล้วล็อกอินยังถูกปฏิเสธไม่มี reply เหมือนเดิมทุกไบต์ และไม่มีโทเคนให้ grep**
     ⇒ ด่านก่อนบูตข้อ 1 ข้างบนช่วยได้จริง: `git grep -n "login_entry_is_pinned" <SHA> -- src/pirateforce_foundation/gm/login_scene_override.py`
     **0 hit = ยังไม่ลง ให้ถือข้อ 3 เต็มโทษ** · งานอยู่ในรอบ `7gplcy` (PR ของรอบนี้) ปลดเมื่อ merge
     · ข้อเตือน `runtime.py:527` (ห้ามแก้ทะเบียนระหว่างเซิร์ฟเวอร์รัน) **ยังใช้ได้ตามเดิม** เป็นพฤติกรรมของ runtime ไม่ใช่ของโค้ดที่หายไป
     🔴 **อัปเดตรอบ `7hfrt0` 2026-08-29T13:3x+07:00 (LANE-GM เจ้าของใบ) — ขีดฆ่าไม่ลบ · ลดโทษข้อ 3 ลง ไม่ปลดทั้งข้อ:**
     ~~"แก้ทะเบียนให้กว้างขึ้นกลางคัน ⇒ ล็อกอินถูกปฏิเสธไม่มี reply และไม่มีโทเคนให้ grep"~~ **ไม่จริงแล้ว**
     `pirate-force-server#253` `merged_at 2026-08-29T05:45:42Z` (วัดด้วย GitHub API ไม่ใช่จดหมาย) พาเกตของ chief ขึ้น main:
     `runtime.py` ยิง `world_scene_entry.resolve_entry` ทดลองกับ snapshot ของโปรเซส**ก่อน**ใช้ override
     ถ้า snapshot ปฏิเสธ ⇒ **ไม่ใช้ override · ตัวละครล็อกอินที่แถวของตัวเอง เข้าเกมได้** พิมพ์
     `GM_LOGIN_SCENE_OVERRIDE_REFUSED ... source=boot_snapshot` และคืนใบที่บริโภคไปแล้วกลับดิสก์
     ⇒ โทษของการแก้ทะเบียนกลางคันเปลี่ยนจาก **"ล็อกเอาต์ถาวรเงียบ"** เป็น **"override ไม่ทำงาน มีโทเคนให้ grep"**
     🔴 **ข้อห้ามยังคงอยู่ทุกตัวอักษร** เพราะใบนี้เกรดว่า "โผล่ที่ฉากที่ตั้งไว้ไหม" — override ที่ไม่ทำงานคือใบนี้เกรดไม่ได้
     ⇒ กติกาเดิม: แก้ทะเบียนแล้ว **รีสตาร์ตเซิร์ฟเวอร์ก่อนบูตเกม** · ถ้าได้ฉากผิด ให้ grep โทเคนข้างบน**ก่อน**สรุปว่า FAIL
     · ทิศตรงข้าม (ทะเบียนถูกแก้ให้**แคบลง**หลังบูต ⇒ override ของ**ทุกบัญชี**ในแฟ้มดับพร้อมกัน) เกตนี้เอื้อมไม่ถึง
     พารามิเตอร์ `scene_registry=` ลงเขตสาย GM แล้วในรอบนี้ แต่ **ยังไม่มีผล** จนกว่า `CORE-REQUEST-GM-036`
     (ใบ `20260829_1330`) จะทำให้ `runtime.py` ส่ง snapshot เข้ามา — วันนี้ให้ถือว่าทิศนี้ยังเปิดอยู่
     · **ยังไม่เคยวัดกับ client จริง** ทั้งย่อหน้านี้อ่านซอร์สบน main กับชุดเทส headless เท่านั้น
     ใช้ scene_id=2 (Prison Exile Island, BG0002) แทน: พิสูจน์แล้ว
     ฝั่งเซิร์ฟเวอร์ว่ามี spawn ปักหมุดแต่ไม่มี ground evidence ที่ x/y จริงของบัญชี ⇒ login จะลงที่ spawn ปักหมุด
     (26905.0, 21185.0, 1680.0) เสมอ ไม่ว่าตำแหน่งจริงที่บันทึกไว้ล่าสุดจะเป็นตรงไหน

- steps:
  1. เปิดเซิร์ฟเวอร์ก่อน ยืนยันพอร์ต 10188/10189 ไม่มี ESTABLISHED ค้างก่อนเปิด client (client เปิดโดยไม่มี
     server รันตายในราว 3.5 นาที)
  2. เปิด client -> เลือกเซิร์ฟเวอร์ -> กล่อง PVP ปุ่มซ้าย -> เลือกตัวละคร -> ช่องตัวละครแรกของบัญชี GM ที่
     ยืนยันแล้ว -> ปุ่มกลางจาก 5 ปุ่มล่าง = เข้าเกม (ห้ามปุ่มซ้ายสุดเด็ดขาด -- ปุ่มนั้นลบตัวละคร)
  3. นับจากจอโหลดจางหาย รอดู 10 วินาทีเต็มก่อนทำอะไรต่อ
  4. เข้าเกมแล้ว: จด HUD X/Y ถ่ายภาพนิ่งความละเอียดเต็ม เช็กว่าพื้น/ฉากบนจอตรงกับ Prison Exile Island / BG0002
     ไหม (ไม่ใช่บ้านหรือฉากที่บันทึกไว้ล่าสุดของบัญชีนั้น) และตัวละครยืนที่จุด spawn ปักหมุด
     (26905.0, 21185.0, 1680.0) ไหม -- ไม่ตกพื้น ไม่ลอย ไม่ค้างจอโหลด
  5. เช็ก NO-CRASH: ลากขวาหมุนกล้องครบ 360 องศา หมุนแค่กล้องเท่านั้น ตัวละครไม่หัน ไม่มีอะไรออกทางสาย
     ปลอดภัยทำได้ทุกจุด ห้ามใช้ Q/E หรือ W/A/S/D สำหรับเช็กนี้ -- ปุ่มพวกนั้นหมุนตัวละครจริงและส่ง TargetPosVital
  6. จดสีของป้ายชื่อทุกป้ายในทุกภาพความละเอียดเต็ม บรรทัดเดียวต่อป้ายต่อภาพ เขียน "none" ถ้าไม่มี อ่านสีจากภาพ
     ความละเอียดเต็มเท่านั้น ห้ามอ่านจาก contact sheet ภาพย่อ หรือวิดีโอ ห้ามชี้สาเหตุของสี (RE-067 เปิดอยู่
     เป็นที่เดียวที่คำถามนั้นอยู่) บันทึกความต่างจากเซิร์ฟเวอร์ต้นฉบับลง REAL_SERVER_DIVERGENCE.tsv บรรทัดละรายการ
  7. ถือค้างอย่างน้อย 60 วินาทีดูว่ามีอะไรเปลี่ยนไหม (texture pop-in, พื้นโหลดช้า, ป้ายชื่อแมพบน HUD ถ้ามี)
  8. ลากขวาหมุนกล้องอีกครั้ง (ทำซ้ำเช็ก NO-CRASH) แล้วออกจากเกม/ปิด client
  9. teardown ผ่าน TEMPLATE_teardown_generic.ps1 (ป้ายเวลาบูตต้องอายุไม่เกิน 420 นาทีตอน teardown) เช็ก
     sha256 canonical กับ CANON_SHA.txt ซ้ำ ลบสำเนาทิ้ง gm_login_scene_standalone.json และ unset
     `PF_GM_LOGIN_SCENE_STANDALONE_CONFIG` (ไม่มี `gm_accounts.json`/`PF_GM_ACCOUNTS_CONFIG` ให้ลบ/unset ในทางแก้
     นี้ -- ไม่เคยตั้งมันเลยตั้งแต่ต้น)

- pass criteria: (สองชั้น แยกกัน)
    wire/DB          : การสลับค่าฝั่งเซิร์ฟเวอร์เองพิสูจน์แบบ headless แล้วรอบนี้โดย
                        tests/test_gm_login_scene_override_wiring.py (6/6 ข้อ ขับผ่าน dispatcher จริง) และ
                        tests/test_gm_login_scene.py's standalone-path tests (ทางแก้ safety fix 2026-08-28) --
                        full suite เขียว ไม่มี regression -- อ้างที่นี่ ไม่พิสูจน์ซ้ำ ชั้น wire/DB ของใบนี้เอง
                        (อ่านจาก console/event log ของการบูตจริงเท่านั้น ไม่ดูจอ) ต้องมีเพิ่ม: console พิมพ์
                        บรรทัด WORLD_SCENE scene_id=2 และ event log บันทึก gm_login_scene_override_applied_2
                        ครั้งเดียวสำหรับ login นี้ ไม่มี event gm_login_scene_override_lookup_failed_* เลย ·
                        **ไม่มีบรรทัด `[G>] GM_UPDATE_STATE_AFTER_LOGIN` ปรากฏเลยตลอด session นี้** (นี่คือ
                        หลักฐานว่าทางแก้ standalone ทำงานจริง -- บัญชีนี้ไม่เคยผ่าน `is_gm_account()` เป็นจริง จึง
                        ไม่มี `0x5A19` ถูกส่งแม้แต่ครั้งเดียว, เห็นบรรทัดนี้ = ทางแก้ไม่ได้ผล ใบนี้ FAIL ไม่ว่าจอจะ
                        เปลี่ยนฉากถูกหรือไม่) · sessions ได้แถวใหม่ 1 แถวที่มี selected_character_id สำหรับ login
                        นี้ · max(lease_generation) ไม่ถอยหลัง · sha256 canonical ตรงกับ CANON_SHA.txt ก่อน/หลัง ·
                        PRAGMA integrity_check=ok บนสำเนาทำงานทั้งสองครั้ง
    client-observable: มนุษย์ที่จอเห็นตัวละครยืนบนพื้น/ฉาก Prison Exile Island / BG0002 ที่จุด (หรือใกล้เคียง
                        สอดคล้องกับ) spawn ปักหมุด (26905.0, 21185.0, 1680.0) ไม่ใช่บ้านหรือฉากที่บันทึกไว้ล่าสุด
                        ของบัญชีนั้น ไม่มี glitch ทางสายตา (ไม่ตกพื้น ไม่ลอย ไม่ค้างจอโหลด) เช็ก NO-CRASH ทั้ง
                        สองครั้งผ่าน สีป้ายชื่อบันทึกตามกฎด้านบนครบทุกภาพความละเอียดเต็ม เขียน "none" ที่ไม่มี

- nonclaims: ใบนี้พิสูจน์ override สำหรับปลายทางเดียว (scene_id=2) บัญชี GM เดียว login ครั้งเดียว เซสชันเดียว
  ไม่พิสูจน์ว่า override ใช้ได้กับ scene_id อื่น ไม่ทดสอบปลายทางที่ปักหมุด login_entry_allowed=False (วันนี้:
  ฉาก 17) เส้นทางนั้นถูกบันทึกไว้ว่าทำให้ login ทั้งครั้งถูกปฏิเสธไม่มี reply เลย (fail-closed ที่ตั้งใจ) และอยู่
  นอกขอบเขตใบนี้ -- config ของใบนี้ต้องไม่ชี้ไปฉาก 17 ไม่ทดสอบ reconnect, relogin, มากกว่าหนึ่งบัญชี GM หรือสิ่ง
  ที่ผู้เล่นคนอื่นเห็น ไม่ตรวจสอบ config/gm_login_scene_standalone.json เกินกว่า mapping เดียวที่ใช้ที่นี่ ไม่
  พิสูจน์อะไรเรื่อง `GM_UpdateGMStateVital`/`0x5A19` เอง (นั่นเป็นขอบเขตของ `GT-107-R3` ต่างหาก -- ทางแก้ safety
  fix 2026-08-28 ของใบนี้แค่ทำให้ไม่ต้องพึ่งคำตอบนั้นก่อน) สำเนาทิ้งถูกลบตอน teardown ใบนี้ไม่พิสูจน์อะไรเรื่องความคงอยู่ของมัน ไม่ชี้สาเหตุของสีป้ายชื่อใด ๆ
  ที่สังเกตได้ (RE-067 เปิดอยู่) ไม่ทำซ้ำหลักฐาน headless ที่ปิดไปแล้วรอบนี้ (tests/test_gm_login_scene_override_wiring.py,
  6/6, full-suite เขียว) -- อ้างเป็นหลักฐานที่มีอยู่แล้ว ไม่ต้องให้มนุษย์รันซ้ำ ผลลบ (เช่น client โชว์ฉากเดิม/บ้าน
  ของบัญชี, โชว์ความเสียหายทางภาพ, หรือค้าง) มีค่าเท่าผลบวก -- จะชี้ไปที่ว่าอะไรฝั่ง client บริโภค scene_id หลัง
  login (คู่ขนานกับคำถามเปิดของ RE-089 เรื่องฟิลด์ GM-login อื่นที่ไม่มี render consumer ที่รู้จัก) ไม่ใช่ที่การ
  สลับค่าฝั่งเซิร์ฟเวอร์ ซึ่งพิสูจน์ถูกต้องแล้วที่ชั้น wire/DB

- result: (ผู้เทสกรอก)
```

```

---

## GT-114 DIAG-MULTI-OBJECT-001 [attended, in-game]: five diagnostic objects at the city-center test point (X=11865, Y=6147), each one field away from control D0 -- does each single-field difference produce the on-screen effect that field is predicted to control, jointly closing the attended half of RE-107/RE-108/RE-109's own proposed follow-ups  [CANCELLED - covered by R309 (D0 · RE-108) / refuted by production DYING_TIMER_SECONDS=20 (D1a · ภาพ 185937) / covered by GT-129 (D1b) / D2 control-only / covered by GT-084-R2 + P-2/RE-067 (D3) — Panya agreed 2026-09-04 21:4x · ปิดโดย chief รอบ `epkucn`/R344 2026-09-04 22:56 +07:00 ตาม `COO-DECISION 20260904_2158` (ถอน `2142` ข้อ 2 = ไม่พ่วงบูตกับ `ATTACK-POSE-ONE-FIELD-AB-001`) · กฎ `PANYA-DECISION 20260903_1934` · เหตุผลรายข้ออยู่ใน `notes_to_chief/20260904_2133_KA1A-TO-COO-attack-pose-*` §1 · เดิม: PENDING -- wiring landed R202 (9b6zl6) · archived โดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)]

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

## GT-116 CORE-REQUEST-022 CLASS-LEVEL-LOGIN-SKILLWINDOW-UNBLOCK-001: after CORE-REQUEST-022 wires class_id=1 (Gladiator) + level=1 into every login's ActorAttr/BasicAttr frames, does a real client's ... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-122 CORE-REQUEST-027 NAME-FIELD-GUILD-SLOT-FIX-001: after CORE-REQUEST-027 moves the character's own name off ActorAttr's guild-name slot (`+0x164`, mask bit `0x01000000`, `LABEL_GUILD`) and ont... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-120 CORE-REQUEST-025 TRACEPATH-GO-BUTTON-STALL-CLEAR-001: after CORE-REQUEST-025 wires an empty-vector `CTracePathVital` (0x2F92) reply to every `CTracePathReqVital` (0x4391), does a real client... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-121 CORE-REQUEST-026 BG0002-ARRIVAL-CENSUS-NO-WASD-001: after CORE-REQUEST-026 makes the Bg0002 (Prison Exile Island) census fire on `teleport_s... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## GT-124 MOB-PICKUP-CLAIM-PREVALIDATION-001: kill a mob, walk to its ground drop, attempt pickup -- does mob_pickup.py's resolve/commit/log-only CLAIM path (BUILD-006 second half) behave exactly as its own unit tests predict when driven by a real human, once runtime.py gets the inbound-pickup-request call site it does not have today  [BLOCKED-ON-WIRING -- see precondition (a) below]

> NUMBERING NOTE: grep confirmed before reserving (2026-08-28, this round) across `GAME_TEST_QUEUE.md`,
> `CLIENT_RE_QUEUE.md`, `notes_to_chief/`, `rounds/`, and `archive/`: `GT-124`/`RE-124` = 0 hits. The shared
> GT-/RE- counter's actual highest used number is `RE-123` (BG0002-MIRAGE-REEL-QUEST-SPAWN-CROSSWALK-001,
> CLOSED, `CLIENT_RE_QUEUE.md`) -- NOT `122` as `rounds/B_20260828_1039_gate2_not_due_yet_prevalidation_
> ticket_opened.md` assumed when it told the queue-author to reserve "GT-123" (that round checked
> `GAME_TEST_QUEUE.md`/archive but not `CLIENT_RE_QUEUE.md`'s own latest entry, whose closing note itself
> already reserved `124` as next-free at 2026-08-28T09:31+07:00). This entry is therefore `124`, not `123`.
> All entries `GT-101`-`GT-122` and `RE-085`-`RE-123` stay exactly where they are, unchanged.

### precondition -- why this is BLOCKED-ON-WIRING, not PENDING (read before booting anything)
(a) **THE HARD BLOCKER.** `mob_pickup.dispatch_pickup_request` / `PickupClaim` / `BagCell.commit_pickup` have
ZERO call sites in `runtime.py` today (grep-confirmed against `pirate-force-server` HEAD this round). Only
`BagCellRegistry.claim`/`.release` are wired (CORE-REQUEST-007, round `3lzfhw`) -- a different, per-connection
bag-*ownership* claim, not a player's ground-drop pickup claim (see mob_pickup.py NONCLAIM 1/12). This is
NOT the same blocker as gate 2 (`session.select_and_start.is_unmoved_baseline`, deferred to 30-31 Aug per
`notes_to_chief/20260827_1350_COO-DECISION-bagwall-second-wall-redesign-deferred-post-M4.md`) -- it is an
EARLIER, separate gap: nobody has wired ANY inbound opcode to this module, because nobody has a confirmed
real wire "vital id" for a pickup request (`rounds/R180_3lzfhw_...md`: "inbound pickup request ยังไม่มีทางไป
(รอ vital id จริงจาก RE)"). A CORE-REQUEST for this call site is not yet filed as of this writing; a fresh
RE ticket (`RE-125`, `CLIENT_RE_QUEUE.md`) was opened the same round as this entry asking for the vital id.
This entry cannot be booted until that CORE-REQUEST lands; it is written now, ready to run the day it does,
so no attended time is spent re-deriving the procedure.
(a2) **SECOND HARD BLOCKER, MEASURED 2026-08-29T12:2x+07:00 (chief round `ni2wh2`/R225). WIRING THE CALL
SITE ALONE WILL NOT MAKE THIS ENTRY RUNNABLE.** `runtime.py:4395-4419` announces every ground drop and then
prunes all of them inside the SAME dispatch call (`for drop in drops: self.mob_loot_cell.take(drop.drop_key)`
at `:4415-4416`). Measured against the real `DropLedgerCell` + `dispatch_pickup_request`, with a control cell
identical except the prune loop did not run: treatment = 0 live rows, every claim REFUSED
`drop_already_taken`; control = 2 live rows, claim ACCEPTED (`identity=5 slot=4`). So a tester would get a
100% refusal rate on a correctly wired build. That prune loop's own comment (`:4402-4413`) says it exists
BECAUSE no pickup path is wired -- GT-124 invalidates its premise. NOTE for whoever fixes it: no test pins
that loop (grep `mob_loot_drops_sent` / `_pruned` / `mob_loot_cell` in `tests/` = 0 assertions), so removing
it goes green silently AND removes the only bound on ledger growth; a replacement bound must land with it.
Chief has asked COO to sequence this (`notes_to_chief/20260829_1221_CHIEF-ASK-COO-gt124-opcode-forbidden-and
-drops-pruned.md`). Do NOT boot this entry until (a), (a2) and the opcode question are all closed.
(b) **OPEN QUESTION, NOT ASSUMED EITHER WAY.** `GT-045` (ANSWERED, archived) and `GT-060` (still
BLOCKED-CONDITIONAL) both found that a ground drop rendered only a floating red name-label (0.2-0.3s), no
model -- "nothing to click" (mob_pickup.py NONCLAIM 12). That measurement predates `mob_loot` being wired
into flagless production (CORE-REQUEST-006, round `3lzfhw`/R180) -- whether the CURRENT production ground
drop is any more clickable is genuinely unknown. This entry's own steps re-check it fresh; a "still nothing
to click" finding is a valid, complete negative for that sub-question (see pass criteria), not a reason to
fail the whole entry, and not something to guess at here.

### source
- `pirate-force-server/src/pirateforce_foundation/mob_pickup.py` (module docstring, "THE WALL", NONCLAIM
  1/9/12): resolve_claim/commit_pickup/dispatch_pickup_request fully unit-tested (`tests/test_mob_pickup.py`,
  green), never called from `runtime.py`.
- `rounds/R180_3lzfhw_core-request-006-007-gm-loot-pickup-wiring.md`: mob_loot ground-drop wired flagless
  into production this round; mob_pickup inbound request path explicitly left unwired, "รอ vital id จริง".
- `archive/notes_to_chief_consumed_to_2026-08-26/20260825_1340_GT045-ANSWERED-...md`: ground drop = name
  label only, no model, on the (older) hypothesis-scenario pipeline. `GT-060` (still BLOCKED-CONDITIONAL) is
  the sibling entry for the wire-id question on that same old pipeline; this entry does not reuse or depend
  on it -- different codepath, different opcode question, different module entirely (mob_pickup.py imports
  neither HYP-PF-036 nor any opcode, per its own docstring).
- `notes_to_chief/20260827_1350_COO-DECISION-bagwall-second-wall-redesign-deferred-post-M4.md`: gate 2
  (persistence/relog) is scheduled for 30-31 Aug and is explicitly NOT this entry's concern -- see nonclaims.

### objective (single claim)
Once runtime.py has a real inbound-pickup-request call site into `mob_pickup.dispatch_pickup_request` (not
yet built, see precondition (a)): does a real human player's kill -> walk -> attempt-pickup sequence, against
a genuine `mob_loot` ground drop, produce exactly the CLAIM-layer outcome the module's own unit tests
predict -- either (i) an accepted claim, printed verbatim as `MOB_PICKUP_ROW_WOULD_INSERT
table=character_backpack_items claimant=... character_id=... item_identity=... template_id=... quantity=...
slot=...` with values matching the drop actually taken, or (ii) exactly one of the named
`MOB_PICKUP_REFUSAL_REASONS` strings (e.g. `claimant_out_of_range`, `not_the_killer`,
`object_ref_never_issued`) -- and never a crash, a hang, or silence on both the console and the wire.
Persistence/relog (gate 2) is explicitly out of scope (see nonclaims): this entry proves the CLAIM
mechanics only, independent of whether the row is ever actually inserted.

### predictions (a wrong prediction is a finding, not a failure)
- P1 [primary, proposed]: click succeeds against a real, killed-by-this-character drop within
  `PICKUP_RADIUS` -> console prints `MOB_PICKUP_ROW_WOULD_INSERT` with the drop's own template/quantity;
  `outcome.delta` composes without raising (no `composed_bytes_off_pin`).
- P2 [proposed, a valid alternate pass]: the attempt is refused by name (e.g. clicked too late,
  `drop_already_taken`) -- any refusal from `MOB_PICKUP_REFUSAL_REASONS`, printed and legible, still proves
  the CLAIM path is live and correctly gated; do not require P1 specifically to close this entry.
- P3 [falsifier]: nothing prints on the console at all despite a click that should have reached the
  handler -- means the call site itself is broken (wrong decode, wrong bag_cell, exception swallowed
  upstream) -- redirect to a new RE/GT entry naming the break, do not re-run this one guessing.
- P4 [open sub-question, NOT this entry's claim, see precondition (b)]: no clickable object exists at the
  drop location at all on today's production build -- record as a clean, bounded NO-RESULT for the
  click-trigger sub-question specifically (mirrors GT-060's own P4 treatment: NOT a negative about the
  CLAIM mechanics, because no request could ever be sent to test them) -- this entry stays open, does not
  FAIL, and the finding should open its own click-trigger RE/GT entry rather than being folded in here.

### db
default_state\pirateforce.sqlite3 -- copy only, canonical never opened. Copy to
`pf_bridge\backup\pirateforce_before_GT-124_<yyyyMMdd_HHmmss>.sqlite3`, then `state\run_gt124.sqlite3`.
sha256 vs `CANON_SHA.txt` before/after; `PRAGMA integrity_check=ok` on the working copy both times.

### server args (fill in the exact command line once precondition (a) lands -- do not guess a flag today)
mob_pickup.py declares `production_allowed = True`, `test_only = False`, no scenario id, no opt-in kwarg
(module docstring: "NO FLAG ... exactly as unconditional as every other symbol in this file"). Once the
CORE-REQUEST for the call site merges, boot is expected to be an ordinary flagless production login:
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt124.sqlite3
```
Before booting: run `pf_resolve_green_boot.py --fetch`, then grep the resolved SHA for the actual call site
(`git grep -n "dispatch_pickup_request(" <SHA> -- src/pirateforce_foundation/runtime.py`) -- 0 hits means
still BLOCKED, do not boot.

### steps (click by click -- fill in once bootable; record continuous video for the whole LOCK_GAME window)
1. LOCK_GAME; confirm the check above returns >=1 hit for the real call site -- otherwise stop, still
   BLOCKED, do not boot.
2. Start server, open client, log in; walk to any hostile mob; kill it (right-click-drag camera only while
   positioning -- never Q/E/WASD before you mean to move, per the camera-vs-facing rule).
3. Photograph full-res the instant the kill lands and again the instant any ground drop appears; record
   whether a model is visible under the name label (precondition (b)) or only the label -- "none" if no
   label either. Record the colour of every name label in frame, one line per label per image, per the
   mandatory colour rule (R163/Panya 2026-08-25) -- never infer a cause, RE-067 owns that question alone.
4. If nothing is clickable: photograph the attempt, record as P4/NO-RESULT for the click sub-question, stop
   here -- do not force a click on empty ground.
5. If something is clickable: left-click it once, immediately photograph the result, and copy the server
   console verbatim from the moment of the click through the next 2 seconds.
6. Repeat once more (a second kill+drop+click) for a second independent reading in the same session.
7. NO-CRASH check: right-click-drag camera 360 degrees (camera only, proves liveness without emitting
   TargetPosVital).
8. Log out; teardown via `TEMPLATE_teardown_generic.ps1` (boot stamp must be under 420 min old); recheck
   canonical sha256; sha256 every capture.

### pass criteria (two layers, never mixed)
wire/DB: server console shows either `MOB_PICKUP_ROW_WOULD_INSERT ...` with values matching the drop
actually taken, or one exact string from `MOB_PICKUP_REFUSAL_REASONS` -- for both of the two attempts in
step 6. No unhandled traceback. Canonical sha256 + `integrity_check=ok` before/after.
client-observable (human at the screen only, never inferred from the console): whether a model was visible
under the drop's name label (yes/no, per attempt); whether the click was even possible; whatever, if
anything, visibly changes on screen after a successful claim (mob_pickup.py's own NONCLAIM 3: nobody has
ever seen a client accept `bag_delta_pc` -- record plainly if the bag/HUD shows nothing at all, that is a
valid, informative negative, not a test failure). Name-label colours per the mandatory colour rule.

### nonclaims
- Does NOT test persistence/relog (gate 2, `is_unmoved_baseline`) -- deliberately out of scope, scheduled
  30-31 Aug per COO-DECISION 20260827_1350; a PASS here proves nothing about whether the item survives a
  relog, only that the claim/resolve/log-only path itself is sound.
- Does NOT test or depend on `GT-060`/HYP-PF-036 (the pickup-listener hypothesis scenario) -- different
  module, different opcode question, mutually exclusive scenario flag; this entry is the production,
  flagless path only.
- Does NOT decide whether P4 (nothing clickable) is a client rendering defect, a missing element field, or
  something else -- that is its own open question for a new entry, not answered or guessed here.
- Does NOT prove `outcome.delta`/`bag_delta_pc` is accepted by a real client even if a `MOB_PICKUP_ROW_
  WOULD_INSERT` line prints correctly -- NONCLAIM 3 in mob_pickup.py stands: nobody has measured that yet,
  and a silent/no-visible-change screen after a "successful" claim is the expected, valid way that surfaces.
- Single account, single session, two kill+pickup attempts -- not a stack/full-bag/race-condition test.
- If precondition (a) or (b)'s call-site grep fails at boot time, the entire entry is BLOCKED, not
  NO-RESULT/FAIL -- record "รอ CORE-REQUEST" and stop.

### result (tester fills this in)
```

```

## GT-127 GM-003 CHAT-COMMAND-DOOR-001: GM พิมพ์คำสั่งลง**กล่องแชทธรรมดา**ของเกม (ไม่ใช่หน้าต่าง `BT_GM`/`GMUI_BASIC` ที่คลิกแล้วเงียบ) แล้วเซิร์ฟเวอร์อ่านคำสั่งนั้นได้จริงไหม -- ตัดสินที่ ndjson audi... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-125 FULLGATE-RED-REPAIR-VERIFY-001 [STATIC-ON-BRIDGE · พร้อมเมื่อ PR ของรอบ lo7e03 (R214) merge แล้ว — ใบเดิมของรอบ swlc56 (#197) ถูกเจ้าของปิดเอง งานถูก cherry-pick มาใบใหม่]: หลังรอบ swlc56 แก้ census/negative ที่ทำให้ full pytest แดง 39 ใบ — รันชุดเต็มบนสะพานอีกครั้งแล้วบอกว่าเหลือแดงกี่ใบ และ regenerate ไฟล์ที่ยังแดงอยู่ใบเดียวที่คลาวด์แตะไม่ได้

- **เปิดโดย** chief สาย E รอบ `swlc56` (2026-08-28T17:0x+07:00) · **ที่มา** `notes_to_chief/20260828_1352_CHIEF-LOCAL-SMOKE-result.md` ข้อ 3: `py -3 -m pytest -q` บนสะพาน = `39 failed, 4050 passed` ที่ main HEAD `336857c`
- **ต้องรันบนสะพานเท่านั้น** เพราะสองในสามโมดูลอ่านอิมเมจ client และใบที่เหลือต้องใช้ game data ของสะพาน — คลาวด์ skip ทั้งหมด (39 skipped = 39 failed ใบเดียวกัน วัดแล้วรอบนี้)
- **รอ merge ก่อน**: ต้องอยู่บน commit ที่มีงานซ่อมของ R213 แล้ว · PR เดิม `#197` **ถูกเจ้าของปิดเองด้วยมือ เพราะปัญหาทางเทคนิคฝั่งเครื่อง (ยืนยันโดยเจ้าของ 2026-08-28 18:1x +07:00) ไม่ได้แดงและไม่ได้ merge** · commit เดิม `8767d499` ถูก cherry-pick ขึ้น branch `claude/bold-dijkstra-lo7e03` (รอบ `lo7e03`, R214) แบบไม่แก้เนื้อ — ใช้ PR ของรอบนั้นแทน

### ขั้นตอน

1. `git pull --rebase` ทั้งสอง repo · จด `git rev-parse HEAD` ของ repo โค้ด
2. `py -3 -m pytest -q -p no:cacheprovider` (ชุดเต็ม ไม่ใช่ subset) · จดบรรทัดสรุปท้ายตรง ๆ
3. ถ้ายังเหลือแดงเฉพาะ `tests/test_pf_scan_field_scene_candidates.py` ให้ regenerate ไฟล์ที่ล้าสมัย:
   `py -3 tools/pf_scan_field_scene_candidates.py --out docs/FIELD_SCENE_CANDIDATES.json`
   แล้วรันโมดูลนั้นซ้ำใบเดียว · commit ไฟล์ JSON ที่ regenerate พร้อมบอกว่า candidate_count ขยับจากเท่าไรเป็นเท่าไร (สมุดสะพานบันทึกไว้ว่า 22 -> 24)
4. push ตามกติกาโหมด local (branch + PR + `PF-AUTOMERGE: v4`) ห้าม push main

### pass criteria — สองชั้น แยกกัน

- **ชั้น wire/DB (ใบนี้ตัดสินได้เอง)**: `py -3 -m pytest -q` ชุดเต็มออก `0 failed` · และ `py -3 tools/pf_runtimeres_actor_entry_static.py` กับ `py -3 tools/pf_hp_death_respawn_static.py` ทั้งคู่ exit 0
- **ชั้น client-observable**: ใบนี้**ไม่มี** และไม่อ้างอะไรเกี่ยวกับหน้าจอเลย — เป็นใบเครื่องมือล้วน ไม่ต้องมี `OBSERVER_CONFIRMED`

### nonclaims

- ไม่อ้างว่า gate เขียว = เกมเล่นได้ · ไม่อ้างว่า census ที่ re-pin แล้ว "ถูก" ในเชิงดีไซน์ อ้างแค่ว่าเลขที่พินตรงกับ `src/` ที่วัดได้จริง
- ถ้าชุดเต็มยังแดงด้วยโมดูลอื่นที่ไม่ได้อยู่ในสามใบนี้ = ผลลบใหม่ ให้เปิดใบใหม่ ห้ามยัดเข้าใบนี้

### result (tester fills this in)
```

```

## GT-128 GM-003 CHAT-WARP-VISIBLE-001 [attended, in-game]: GM พิมพ์ `/warp <ฉากปัจจุบัน> <x> <y>` ลงกล่องแชทธรรมดา แล้ว**ตัวละครขยับไปยังพิกัดนั้นบนจอจริงหรือไม่** -- ใบแรกของสาย GM ที่ตัดสินที่จอ ไม่ใช่ที่ log  [❌ **CANCELLED - refuted by R306 finding 3 (`notes_to_chief/20260903_1655_*`)** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2) — รูป same-scene ที่มีพิกัดส่ง `LANE_GM_CHAT_WARP_TELEPORT_FORCE_POS` แล้ว **ไคลเอนต์ปิดตัวเอง** (`ErrorData=28317`) วัดบนจอเจ้าของ ⇒ คำถามของใบนี้ ("ตัวละครขยับไปพิกัดนั้นไหม") ตอบไม่ได้ด้วยรูปเฟรมที่มีอยู่ และ `COO-DECISION 20260903_1744` ข้อ 3 สั่งปิด `/warp` แบบมีพิกัดไปแล้ว · 🔴 **เปิดใบใหม่ (ไม่ใช่ปลดใบนี้) เมื่อ LANE-GM เปลี่ยนรูปเฟรมและมี headless proof** — ใบใหม่ต้องเขียนเกณฑ์บนรูปเฟรมใหม่ ไม่ใช่ยกด่านเก่าทั้งชุดมาใช้ · สถานะเดิม: ~~BLOCKED — token compares nothing (COO-DECISION 20260829_0041)~~ **STILL BLOCKED — token fixed, but a separate COO-held gate remains (see chief R243 update at end)**: ห้ามเกรด ห้ามบันทึกผลใด ๆ ด้วยโทเคน `GM_WARP_POSITION_CONFIRMED` ตัวปัจจุบัน เพราะมันเทียบแค่ "แถวเปลี่ยนค่า" ไม่ได้เทียบกับ**จุดที่สั่ง** · ปลดเมื่อชุดแก้โทเคน+audit ลง main (chief, ภายใน 2026-08-29 23:59+07:00) · **อัปเดตรอบ `nz0qt2`:** ครึ่ง audit ที่เป็นเขต LANE-GM (แถว `outcome`, `CORE-REQUEST-GM-032` ข้อ 1-2) อยู่ใน PR `pirate-force-server#223` **รอ merge** · ครึ่งโทเคน (`GM_WARP_POSITION_TARGET_MATCH/MISMATCH`, `CORE-REQUEST-GM-031`) และข้อ 3 ของ GM-032 ยังเป็นของ chief ⇒ ป้าย BLOCKED ของใบนี้ **ยังไม่ถูกปลด** ด้วยรอบนี้ · 🔴 **เหตุผลที่วัดแล้ว ไม่ใช่แค่เหตุผลเชิงหลักการ** (เพิ่มโดย LANE-GM เจ้าของใบ รอบ `xk4wmz`): pf-adversary วัดว่าโทเคนตัวปัจจุบัน **ยิงตอนผู้เล่นเดินเองหนึ่งก้าว**หลัง warp ที่ไคลเอนต์เมิน ⇒ ใบนี้ "ผ่าน" ได้โดยที่ warp ไม่ทำงานเลย · **ของที่ LANE-GM ทำเสร็จแล้วเพื่อชุดของ chief:** `gm/warp_target_record.py` เก็บปลายทางของ warp ใบนั้นไว้เทียบได้ หยิบได้ครั้งเดียว ผูกกับ `character.id` (รอบ `z6gu2n` บน main แล้ว) และ `CORE-REQUEST-GM-031` ขอให้ chief พิมพ์ `GM_WARP_POSITION_TARGET_MATCH` / `..._MISMATCH` **เพิ่ม** จากโทเคนเดิม (ห้ามเอา match มาเป็นเงื่อนไขของโทเคนเดิม -- วันนี้ client เมิน `ForcePos` ผลที่คาดคือ MISMATCH ถ้ารวมกันโทเคนจะหายทั้งใบ) · BLOCKED x4 รวมข้อนี้ (~~x3~~ ~~x2~~ นับผิดมาแต่แรก มีสามข้อมาตลอด) -- ห้ามบูต: (ก) `CORE-REQUEST-GM-029` ยังไม่ลง main (จุดเรียกที่คืน action ที่สาขา `0xAC52`) · **อัปเดตรอบ `vvxkft`:** ตัวโมดูล `gm/chat_command_action.py` เองก็เพิ่งกลับขึ้น main รอบนี้ (PR #204 -- PR #200 ของรอบ `gr2q9j` ถูกปิดเพราะ gate แดง ไม่เคย merge) และ GM-029 เปลี่ยนความหมายเป็น "**แทนที่**บรรทัด `fire()` ของ GM-028 ในคอมมิตเดียว" ไม่ใช่ "เพิ่มจุดเรียก" (ใบ `20260828_1930_LANE-GM-CORE-REQUEST-GM-029-v2-replace-not-add.md`) ⇒ วันที่ใบนี้บูตได้ `GT-127` จะใช้ไม่ได้ตามเกณฑ์เดิมอีกต่อไป เพราะ event เปลี่ยนเป็น `gm_chat_action_*` -- **บูต `GT-127` ให้จบก่อน** (ข) ~~`RE-129` ยังไม่ตอบ~~ **RE-129 ตอบแล้ว 2026-08-28T20:09+07:00 (`ForcePos vital_version = 0`) แต่ข้อนี้ยังบล็อกอยู่ด้วยเหตุใหม่:** `COO-DECISION 20260828_2130` ล็อกแข็งว่าห้ามเปลี่ยน `FORCE_POS_VITAL_VERSION_CONFIRMED` จาก `None` จนกว่าจุดเขียนตำแหน่งแบบยืนยันจะอยู่บน main (`CORE-REQUEST-GM-030`, รอบ `fo2lgh`) **แม้ RE-129 จะตอบก่อนก็ตาม** ⇒ โมดูลยังปฏิเสธการส่งด้วยตัวเอง และตอนนี้มีเทสบังคับด้วย (`pirate-force-server/tests/test_gm_force_pos_version_lock.py` แดงถ้าเปลี่ยนค่าก่อนโทเคน `GM_WARP_POSITION_CONFIRMED` อยู่บน main) · เหตุผลชั้นที่สองจาก RE-129 เอง: handler ที่ client จดทะเบียนไว้สำหรับ `ForcePos` = `mov al,1; ret 4` ไม่อ่าน payload ⇒ **version ถูกไม่ได้แปลว่าจะขยับ** ใบนี้ยังเป็นใบเดียวที่ตัดสินข้อนั้นได้ (ค) ~~🔴 **คำถาม "ใครเป็นเจ้าของตำแหน่งหลัง warp" ยังไม่มีคำตอบ**~~ **ตอบแล้ว 2026-08-28T21:30+07:00 (`COO-DECISION`): เจ้าของคือตำแหน่งที่ client ยืนยันแล้ว · เซิร์ฟเวอร์ห้ามเขียนตำแหน่งที่ตัวเองไม่ได้สังเกตเห็น · ตัวยืนยันคือ `TargetPos` ใบแรกหลังเฟรม** ⇒ ข้อนี้เหลือ "รอการเดินสาย" ไม่ใช่ "รอคำตอบ" -- ปลดเมื่อ `CORE-REQUEST-GM-030` ลง main และ COO ปลดล็อก · ผู้เทสต้องบันทึกในผล: หลัง warp ให้เดินหนึ่งก้าวเพื่อบังคับ `TargetPos` แล้วดูว่าคอนโซลมี `GM_WARP_POSITION_CONFIRMED` หรือไม่ · **บริบทเดิมของข้อนี้ (เก็บไว้):** — pf-adversary รอบ `gr2q9j` ชี้ว่า หลังส่ง `ForcePos` แล้ว แถวใน DB และ `selected.position` ยัง**ค้างที่จุดเดิม** (โมดูลไม่เรียก `foundation.checkpoint`) ⇒ client อยู่จุดใหม่ เซิร์ฟเวอร์คิดว่าอยู่จุดเก่า · aggro/pickup/logout ใช้จุดผิด · ต้องได้คำตอบ (`ASK-COO` รอบนี้) **ก่อน**เปลี่ยนค่าคงที่ของ `RE-129` ไม่ใช่หลัง · **อัปเดตรอบ `38c4tv` 2026-08-29T08:22+07:00 (LANE-GM เจ้าของใบ) — เพิ่มด่านก่อนบูตข้อ 4 ไม่ได้ปลดหรือเพิ่มบล็อก:** จดหมาย chief `20260829_0604` ข้อ ②bis (ก) วัดได้ว่าล็อกอินที่ใช้ override ฉากเป็น **visit** ⇒ ไม่เขียนแถวตำแหน่ง ⇒ `GM_WARP_POSITION_CONFIRMED` **ไม่มีทางยิง** บนเซสชันนั้น · ใบนี้ตัดสินด้วยโทเคนนั้น จึงต้องยืนยันก่อนบูตว่าบัญชีไม่มีใบล็อกอินค้าง ทั้ง `gm_login_scene.json` และ `gm_login_scene_standalone.json` (ดูด่านข้อ 4) 🔴 กับดักซ้อน: ขั้นตอนข้อ 4 ของใบนี้เอง (`/warp <ฉากอื่น>`) เป็นตัวสตางค์ใบนั้น · **อัปเดต chief รอบ `3ru85y` (R243) 2026-08-30T~16:xx+07:00 — CORE-REQUEST-GM-030/031 wired, แต่ตัวบล็อกจริงของใบนี้ยังปิดอยู่:** `GM_WARP_POSITION_TARGET_MATCH`/`_MISMATCH` พิมพ์แล้วจริง เพิ่มจากโทเคนเดิม ไม่แทนที่ (พิสูจน์ headless: warp ตรงพิกัด -> MATCH หนึ่งบรรทัด, warp ผิดพิกัด -> MISMATCH พร้อมระยะ, เดินเองไม่มี warp -> ไม่มีทั้งคู่, target ค้างข้ามเฟรมไม่เกิด — เทสใหม่ 5 ใบใน `tests/test_gm_warp_position_confirmed.py`, สวีตเต็ม 5480 passed) · 🔴 **pf-adversary พบ**: กิ่ง `unknown_character_mismatch` ที่ `CORE-REQUEST-GM-031` ข้อ 5 ขอ เป็น **dead code ในโปรดักชัน** — ลำดับการ์ดเดิม (`character_changed` early-return) ดักทุกกรณี re-select จริงไว้ก่อนกิ่งใหม่จะถึง เทสที่พิสูจน์กิ่งนี้ต้อง park เป้าหมายตรงผ่าน `record_warp_target` เอง ไม่ใช่ผ่านเส้นทาง `/warp` จริง — [ไม่อ้าง] ว่ากิ่งนี้ทำงานได้จริงในโปรดักชัน คงไว้เป็น defense-in-depth ตามที่คอมเมนต์ใหม่ใน `runtime.py:_gm_warp_open_confirm_window` บันทึกไว้ ส่งคำถามลำดับการ์ดนี้ต่อให้ LANE-GM/COO ตัดสินว่าจะแก้หรือรับสภาพ (ดูจดหมาย `CHIEF-REPLY` รอบนี้) · pf-adversary ยังพบบั๊กเดิมที่ไม่เกี่ยวกับ diff นี้ (rearm เป็นตัวละครอื่นก่อนมี TargetPos ทำให้ `gm_warp_pending_character` ค้างชื่อเก่า แล้วโทเคนทั้งชุดเงียบทั้งเฟรมของตัวละครใหม่) — ไม่แก้รอบนี้ (นอกขอบเขตใบ) รายงานไว้ให้ทราบ · ~~🔴🔴 **ตัวบล็อกจริงของใบนี้ทั้งใบยังไม่ปลด**: `teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED` ยังเป็น `None`~~ **อัปเดต chief รอบ `9fv1m8` (R253) 2026-08-31T~02:1x+07:00: ค่าคงที่ปลดแล้ว** (`teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED = 0`, ตาม `COO-DECISION 20260830_1645`/`1742` -- ค่า RE-129 literal ไม่ใช่การอ่านชื่อ `*_PROVEN_BY_RE129`) พร้อมแก้เทส 13 ใบใน 6 ไฟล์ที่พึ่งค่า shipped เดิมโดยไม่ patch ตรง ๆ (pf-adversary รีวิวผ่านก่อน commit) สวีตเต็ม 5600 passed 0 failed เขียว(cloud sanity) · **รอ merge ก่อน** -- `pirate-force-server` PR ของรอบ `9fv1m8` ยังไม่ merge เช็ค `PR_STATE.txt` ก่อนบูต · ไบต์ `ForcePos` จะออกสายจริงเมื่อ merge แล้วเท่านั้น · ตัวบล็อกที่เหลือของใบนี้ (ลำดับการ์ด `unknown_character_mismatch` dead-code ที่ pf-adversary พบรอบ `3ru85y`, และ rearm-character bug ที่ยังไม่แก้) **ยังไม่ปลด** -- นี่คือแค่การเปิดสายไบต์ ไม่ใช่การปิดใบ ผู้เทสยังต้อง ยันหน้าจอจริงตามด่านเดิมของใบนี้ · archived โดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)]

---

## GT-129 MOB-DEATH-001 DEAD-ONLY-NO-DYING-001 [attended, in-game]: ส่ง **DEAD เฟรมเดียว ไม่มี DYING นำหน้า** ให้ศพ ~~0x201F~~ **0x2068** (LANE-B รอบ `8ftmbx`: `COO-DECISION 2026-08-29T00:41+07:00` ถอน placement 30 ออกจากโรสเตอร์ ⇒ 0x201F ไม่มีบนสายอีกต่อไป ศพที่ใบนี้ขับได้คือหุ่นซ้อม `n_ID 916` placement 103) -- ศพยัง**แข็ง**หรือ**ล้ม**  [🔴 **BLOCKED -- ห้ามบูต**: (ก) ต้องมีทางขับ "DEAD-only" ที่ call site `runtime.py` ซึ่งเป็นไฟล์ของ chief -- สาย B ขับเองไม่ได้ (ข) สะพานฝั่งเครื่องเงียบตั้งแต่ 15:06 (`COO-DECISION 20260828_1841`)]

> 🔴 **ใบนี้เขียนตามสเปกของ `RE-107` เป๊ะ ไม่ใช่ของสาย B เอง** -- `RE-107` ระบุ capture ที่แคบที่สุดไว้แล้ว
> และ**ห้าม**เปลี่ยน name/faction พร้อมกัน เพราะ static พิสูจน์แล้วว่าสอง field นั้น
> **ไม่ถูกอ่านใน death predicates / task gate** ⇒ แขน name/faction ไม่ใช่แค่ไม่จำเป็น แต่**ต้องห้าม**

### คำถามเดียวของใบ
ลำดับ `DYING → (700 ms) → DEAD` เป็นตัวแปรจริงของอาการ "ศพแข็งลอยค้าง" หรือไม่

### สองแขน (ตัวแปรเดียว: มี/ไม่มี DYING นำหน้า)
- **B0 ฐาน** -- `DYING`(HP 0, timer 20.0) → 700 ms → `DEAD`(HP 0, timer 0.0) = ทรง `GT-084-R2` เป๊ะ ⇒ คาด: แข็ง
- **B1 🔴 แขนเดียวของใบ** -- `DEAD` เฟรมเดียว (HP 0, timer 0.0) **ไม่มี DYING นำหน้าเลย**
  · identity / preset / ชื่อ / faction / body **เหมือน B0 ทุกอย่าง**
  · ต้องรอจน**คลิกล็อกเป้าได้แล้ว** ค่อยส่ง (สเปกของ `RE-107`: "after model-ready")

### อ่านผลยังไง (สเปกของ `RE-107` ไม่ใช่การตีความของสาย B)
- **B1 ยังแข็ง** ⇒ **ตัด** 700-ms DYING→DEAD cutover ออกจากรายชื่อผู้ต้องสงสัย
  เหลือ **model-loaded bit / clip / pick path** เป็นทางเดียว
- **B1 ล้ม** ⇒ **ลำดับเป็นตัวแปรจริง** และ `DEATH_TASK_HOLD_MS` กลายเป็นเรื่องที่ต้องวัด (ไม่ใช่เดา)

### เกณฑ์ผ่านสองชั้น
- **ชั้น wire/DB**: B1 ต้องมี `grep -c MOB_DEATH_DYING` = **0** และ `MOB_DEATH_DEAD` = **1** ·
  B0 ต้องได้ 1 กับ 1 · ทั้งสองแขนต้องมี `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE actor_count=`
  ~~`115`~~ **เท่ากับเลข `assembled=` ของบรรทัด `WORLD_CENSUS` ในบูตเดียวกัน**
  (แก้โดยเจ้าของใบ LANE-B รอบ `szdkgs` 2026-08-29 ตามจดหมาย
  `notes_to_chief/20260828_2245_LANE-A-STATUS-census-count-is-108-*`: ตั้งแต่รอบ `pqx4fj`
  ฉาก 1 ประกอบได้ **108** ไม่ใช่ 115 เพราะ 7 placement แปลง identity ไม่ได้และถูกตัดแบบ fail-closed
  🔴 **108 คือค่าที่ถูก ไม่ใช่ world-wipe** — world-wipe คือเลข**หลังเหตุการณ์น้อยกว่าเลขตอน arrival
  ของบูตเดียวกัน** เลข 115 ที่ปักไว้เดิมจะทำให้ใบนี้หยุดตัวเองด้วยเหตุผลที่ผิด)
  (เพี้ยน = world-wipe กลับมา หยุดทั้งใบ) · เก็บ **raw bytes** ของเฟรมที่ส่งจริง ตามที่ `RE-107` สั่ง
- **ชั้น client-observable**: หลังส่ง ดูด้วยตาที่ t+3 / t+10 / t+16 วินาที · หมุนกล้องรอบตัวหนึ่งครั้ง ·
  ภาพนิ่งอย่างน้อย 2 ใบต่อแขน · บันทึกว่า **ท่าเปลี่ยนหรือไม่เปลี่ยน** เท่านั้น

### ที่ต้องระวัง
- 🔴 **ห้ามเปลี่ยน name หรือ faction ในใบนี้** (`RE-107` ห้ามตรง ๆ) ถ้ามีใครเสนอแขนแบบนั้น = ใบผิด
- 🔴 **ห้ามอ่าน "cursor ไม่จับ actor" ว่าเป็น "ล้ม"** -- `GT-084-R2` เจอสองอย่างนี้พร้อมกัน แต่มันแยกกัน ·
  `RE-107` พิสูจน์ว่า dead-task CFG **ไม่เรียก** actor-map resolver/inserter ⇒ "ถูกถอดจาก logic list"
  กับ "ยังอยู่แต่ pick filter ปฏิเสธ" **ยังแยกไม่ได้** และใบนี้ไม่ได้มาแยกมัน
- 🔴 **`_F_DIE_000` ไม่เคยมีใครเห็น** -- เขียนได้แค่ "ท่าเปลี่ยน/ไม่เปลี่ยน"

### ทางที่ใบนี้ไม่ได้ปิด และควรเปิดใบต่อ
`RE-107` ชี้ **client-local model-loaded bit `[actor+0x70] & 0x40`** ที่ `0x47289E` เป็น gate ของ
`_F_DIE_000` และบอกว่า **corpus ไม่มี crosswalk ว่า preset `M011` resolve `_F_DIE_000` สำเร็จหรือไม่**
⇒ ถ้า B1 ยังแข็ง ใบถัดไปคือ **static**: หา crosswalk `M011` ↔ `_F_DIE_000` (ของสาย RE ไม่ใช่ attended)

### nonclaims
1. [ไม่อ้าง] ว่าลำดับคือสาเหตุ -- นั่นคือสิ่งที่ใบนี้มาวัด
2. [ไม่อ้าง] อะไรเกี่ยวกับค่า `700` -- `COO-DECISION 20260826_0551` สงวนไว้ ใบนี้ไม่ขอเปลี่ยนค่า production
   (ใบนี้เอา DYING **ออก** ไม่ได้ขยับ hold)
3. [ไม่อ้าง] ว่า name/faction เกี่ยวข้อง -- `RE-107` พิสูจน์ static แล้วว่า **ไม่ถูกอ่าน**
4. [ไม่อ้าง] ว่า actor ถูกลบจาก picking list
5. [ไม่อ้าง] ว่าใบนี้แยก "ตัว actor/โมเดล" ออกจากตัวแปรอื่น -- ทั้งสองแขนใช้ 0x201F/preset เดิม โดยตั้งใจ

**ผู้เปิดใบ: LANE-B (รอบ `kfs01z`)** -- ผลกลับมาที่สาย B บริโภค
🔴 **ฉบับแรกของใบนี้ (รอบเดียวกัน) ถูกถอนทั้งใบ** -- มันตั้งแขน name/faction ที่ `RE-107` ห้ามไว้
และวัดบน composer ที่ **ไม่ใช่ตัวที่ลงสายจริง** ดู `archive/rounds_2026-08-27_to_28/B_20260828_2129_corpse_ab_arms_and_28317_debt.md` ข้อ ④


---

## GT-131 NPC-IDENTITY-CLINE-RESOLVED-001 [attended, in-game]: NPC ของ Port Royal แสดง **ตัวจริง** แล้วหรือยัง -- ใบตรวจรับหลัง `GT-078` ถูกเจ้าของปฏิเสธ  [~~PENDING~~ ✅ **PASS · ปิดโดยเจ้าของใบ LANE-... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕🎮 GT-132 GROUND-DROP-COALESCED-GENERATION-DRAWS-N-LABELS-001 [attended, in-game]: **ฆ่ามอนตัวเดียวที่ตกของหลายชิ้น แล้วนับว่ามี "ป้ายชื่อไอเทมสีแดง" ขึ้นกี่ป้าย**

> 🔴 **บรรทัดบังคับของใบตีมอนทุกใบ (`COO-DECISION 20260902_1848` ข้อ 2 · เติมโดย LANE-B รอบ `di7ers`):**
> **ข้ามฉากแล้ววาปกลับ = เลือดมอนกลับเต็ม เป็นของที่รู้อยู่แล้ว ประกาศไม่แก้ ไม่ใช่ FAIL ของการตี**
> จะวัดว่าเลือดลดจริง ต้องตีและอ่านผล **ในฉากเดียวกัน ไม่ข้ามฉากคั่น** · ถ้าข้ามฉากแล้วกลับมาเห็นเลือดเต็ม
> ให้จดว่า `known: wound reset on scene re-open` แล้วเทสต่อ **ห้ามปิดใบเป็น FAIL ด้วยเหตุนี้**

🟢🟢🟢 **READY — กำแพงทั้งสองพังแล้วบน `main`, แก้หัวใบที่รอบ `xt0g9c` (2026-08-30T15:3x+07:00)
ตามที่ กะ1-A วัดสด (`notes_to_chief/20260830_1509_KA1A-MEASURED-...md`) — เดิม ⛔ BLOCKED จากรอบ `j0u64p`**
วัดแล้วด้วยการรัน (ไม่ใช่การอ่านโค้ด · จดหมาย `20260829_0744_LANE-B-STATUS-bg0002-monsters-cannot-be-fought-two-walls.md`):
ใน `Bg0002` — ฉากเดียวที่ใบนี้รันได้ — เคย**ผู้เล่นตีมอนไม่ติดตั้งแต่ต้น** ไม่ใช่ "ตีได้แต่ไม่ตาย"
`runtime.py:3911` เคยโหลด roster ของ `bg0001` ฉากเดียว ⇒ มอน `Bg0002` เคย**ไม่ได้เป็นเป้าหมายการตีเลย**
และชั้นที่สอง: `kill()` เคยปฏิเสธมอน `Bg0002` **ทั้ง 17 ตัว**
🟢 **ปลดล็อกแล้ว — วัดบน `origin/main` วันนี้:**
กำแพง① `_sync_combat_scene_state()` (`runtime.py:3925`, docstring อ้าง `COO-DECISION 2026-08-29T08:48 item 3`,
commit `1e051d1`) `git merge-base --is-ancestor` = ON `origin/main` — combat roster/ledger/AI register
follow ฉากที่ตัวละครยืนจริงแล้ว · กำแพง② `runtime.py:4418` ส่ง `widened=mob_death.ruling_for(mob)`
(หาใบเองจากตัวมอน) และ `mob_death.py:380` มี `"widen-death-scope-bg0002": frozenset({31, 34, 35, 103})`
⇒ **ทั้งสองด่านที่เคยปฏิเสธ ไม่ปฏิเสธแล้วในซอร์สบน main** — บูตได้ตามด่านบิลด์ข้างล่างต่อไปนี้

🔴 **สถานะที่ควรกรอกตอนนี้: `NO-RESULT` ต่อ claim ของใบนี้เอง (นับป้ายไม่ได้) — อัปเดตโดย LANE-B
รอบ `qb1ytr` 2026-08-30T16:4x+07:00 บริโภคจดหมาย `20260830_1554_GT143-GT132-GT149-RESULT-*.md`
(กะ1-A บูตจริงแล้ว 4 ครั้ง ไม่ใช่การอ่านโค้ด):** ~~READY~~ **BOOTED, ANSWERED-DIFFERENTLY.**
วัดชั้น wire ครบ: ของตกจริง 4 ครั้ง (drops = `1/0/1/2`) ครั้งที่ 4 คือ multi-drop (2 ชิ้น, template 34
"Fighting Fish soldier") ที่ใบนี้ต้องการพอดี — เฟรม 82 ไบต์ออกจริง · **แต่จอ (เจ้าของ) เห็น 0 ป้าย
ทั้งสี่ครั้ง ไม่ใช่แค่ครั้งที่มี multi-drop** ⇒ **นับป้ายไม่ได้เลยสักครั้ง** สาเหตุร่วมที่วัดได้คือ
`label_life=0.2s` (ดู `GT-149` ด้านล่างในไฟล์นี้) สั้นกว่าที่เฟรมจะไปถึงจอ (`late=351-949ms` วัดจาก
คอนโซล) ⇒ **นี่ไม่ใช่ FAIL ตามเกณฑ์ "นับได้ 0 ⇒ FAIL" ของใบนี้** เพราะสาเหตุที่นับไม่ได้ไม่ใช่ "เลนไม่วาด
อะไรเลย" แต่คือ "ป้ายมีชีวิตสั้นกว่าที่ตาคน/กล้องจะจับได้" — เงื่อนไขที่ nonclaim ของใบนี้เองไม่ได้กันไว้
🔴 **ถอน "เว้นวรรค" เดิมของรอบ `xt0g9c` ที่แนะนำ template `103` (Orc Chief) เป็นตัวอย่าง multi-drop ที่ดี
ที่สุด** — `103` อยู่ใน `OWNER_REFUSED_PLACEMENTS['Bg0002']` ทั้ง 5 แถว (`92-96`) ⇒ **ไม่เคยถูกส่งลงฉากเลย
สักตัว** (ยืนยันซ้ำโดย `GT-143` ด้านล่าง) ตัวอย่างที่ใช้ได้จริงคือ **template `34`** (พิสูจน์แล้วรอบนี้ว่า
ดรอปได้ 2 ชิ้น) 🔴 **ใบนี้ปิดไม่ได้จนกว่า `label_life` จะยาวพอให้คนเห็นป้าย** — ดู `GT-149` และจดหมาย
`20260830_1554_...` สำหรับรายละเอียดเต็ม · จดหมาย ASK-COO ของรอบนี้เปิดคำถามเรื่องนี้แล้ว
(`notes_to_chief/20260830_1643_LANE-B-ASK-COO-label-life-reopens-drop-refresh-ban.md`)

🔴🔴 **chief รอบ R221 (`950mjq`) — ฉากที่รันใบนี้เปลี่ยนแล้ว อ่านก่อนบูต ไม่งั้นได้ 0 ป้ายแล้วดูเหมือน FAIL ทั้งที่ไม่ใช่:**
**ใบนี้รันในเมือง (Port Royal) ไม่ได้ ต้องรันใน `Bg0002`**
เหตุผล [วัดแล้ว · LANE-B รอบ `sn42vo` จดหมาย `20260829_0255_LANE-B-STATUS-nine-rows-withdrawn-port-royal-has-four-dummies.md` บรรทัด 46-47]:
Port Royal เหลือ **หุ่นซ้อมสี่ตัว** และหุ่น `916` มี `n_DROPS_*` เป็น **0 ทั้งสามคอลัมน์** ⇒ ฆ่าแล้วไม่มีของตกเลย
⇒ ถ้าบูตใบนี้ในเมือง จะนับป้ายได้ **0** ซึ่ง **ไม่ใช่ FAIL ของสมมุติฐาน** แต่เป็นฉากที่ไม่มีของให้ตกตั้งแต่ต้น
🔴 นับได้ `0` ป้าย **ในเมือง** ⇒ บันทึกเป็น `NO-RESULT (ฉากผิด)` **ห้ามบันทึกเป็น FAIL**
🔴 เกณฑ์ `1` ป้าย = FAIL ที่เขียนไว้ข้างล่าง **ใช้ได้เฉพาะเมื่อรันใน `Bg0002`** เท่านั้น

🔴 **chief รอบ `wi1m62` -- อ่านก่อนบูตใบนี้ ไม่งั้นเสียบูตทั้งรอบ:** ใบนี้ต้อง **ฆ่ามอน** ให้ได้ก่อน
และผลรอบ 2026-08-29T00:18 พบว่า **คลิกซ้ายหนึ่งครั้งบนมอนเปิดหน้าต่างบทสนทนาเปล่า ไม่เข้าโหมดตี**
เลนโจมตีอยู่ที่ `ActionVital 0x1AEA` ซึ่ง client ยิงเมื่อ **ดับเบิลคลิก** เท่านั้น (ดูโปรโตคอลเต็มที่สถานะ `GT-104`)
⇒ ใช้ดับเบิลคลิก · ถ้ามีหน้าต่างเปิดทับ ให้ปิดแล้วดับเบิลคลิกซ้ำ และจดไว้ว่าเปิดทับกี่ครั้ง

> NUMBERING: จอง `GT-131` ตอนเปิดรอบ (grep = 0 hit) แต่ **สาย A รอบ `pqx4fj` merge `GT-131` เข้า main ก่อน**
> ⇒ ตามกฎ "ชนแล้วห้ามทับ" ใบนั้นอยู่ที่เดิม ใบนี้ขยับเป็น `GT-132`
> 🟢 **READY — attended · ศูนย์สล็อต ไม่มีแฟล็ก** · เปิดโดย LANE-B รอบ `zxnwtd` (2026-08-28T23:0x+07:00)
> ต่อจาก `RE-130` ✅ CLOSED · **ต้องรันบนบิลด์ที่มี PR รอบ `zxnwtd`** — ด่านบิลด์ข้างล่างเป็นตัวบังคับ
>
> 🔴 **LANE-B รอบ `8ftmbx` (2026-08-29T02:5x+07:00) — เปลี่ยนฉากที่ใบนี้รันได้ อ่านก่อนบูต:**
> `COO-DECISION 2026-08-29T00:41+07:00` สั่งถอนเก้าแถวสุดท้ายของการอ่านแบบเลขชุดออกจาก `bg0001`
> และรอบนี้ถอนแล้ว ⇒ **Port Royal ไม่มีมอนที่ตกของอีกเลย** สิ่งที่เมืองยังส่งคือหุ่นซ้อม `n_ID 916`
> สี่ตัว ซึ่ง `n_DROPS_NORMAL/EQUIPMENT/SPECIALLY` เป็น 0 ทั้งสามคอลัมน์ (ตารางเกมเอง ไม่ใช่ตัวเลือก
> ของสายนี้) ⇒ **ฆ่ากี่ตัวก็ไม่มีของตก ใบนี้จะได้ 0 ป้ายเสมอด้วยเหตุที่ไม่ใช่คำถามของใบ**
> ⇒ **ใบนี้ต้องรันใน `Bg0002` (Prison Exile) ไม่ใช่ Port Royal** — ฉากนั้นมีมอนจริง 17 ตัว
> (`field_mob_tables_bg0002`) ที่มีชุดของตกจริง และตาราง `field_drop_tables` รอบนี้ก็ mine
> ทั้งสองฉากรวมกันแล้ว (union) จึงมีข้อมูลของ Bg0002 ครบ · การเดินทางไป `Bg0002` เป็นของสาย A
> (`GT-121` PASS แล้ว: สำมะโนมาก่อนขยับ) · ถ้าผู้เทสรันใน Port Royal แล้วได้ 0 ป้าย
> **ห้ามบันทึกเป็น FAIL** ให้บันทึกว่า "รันผิดฉาก" แล้วรันใหม่

### คำถามเดียวของใบนี้
เซิร์ฟเวอร์ส่งของทั้งกองของการตายหนึ่งครั้งเป็น **collection เดียว count=N** แล้ว (เดิม N collection ละ 1)
**ผู้เล่นเห็นป้ายกี่ป้าย** — `N` · `1` · หรือ `0`

### ลิงก์ที่ต้องอ่านก่อน
`RE-130` ✅ CLOSED (`consumed/20260828_2018_RE-130-RESULT-*.md`) — codec รับ `count > 1` · generation ที่
nonempty ลบ key ที่ omit · **ใบนั้นเขียนเองว่าไม่รับประกันการวาดหรืออายุป้าย** ⇒ ใบนี้คือชั้นนั้น
`GT-045` ✅ CLOSED — ป้ายสีแดง **อายุ 0.2-0.4 วิ** ไม่มีโมเดลใต้ป้าย
🔴 อายุเท่านี้ลำพังตัวเดียวอธิบาย "ไม่เห็น" ได้ทั้งใบ ⇒ **ต้องอัดวิดีโอ ตาเปล่าไม่นับ**

### วิธีรัน
1. บูต **ไม่ใส่แฟล็กใด ๆ** (เลนนี้ `production_allowed=True` อยู่แล้ว) · จด `BOOT_COMMIT`
2. เข้า Port Royal · **อัดวิดีโอตั้งแต่ก่อนตีจนถึงหลังมอนตาย 5 วินาที** (ป้ายสั้นกว่าครึ่งวินาที)
3. ฆ่ามอนจนคอนโซลพิมพ์บรรทัดที่มีของ **≥ 2 ชิ้น** — ตก 1 ชิ้นไม่ใช่ตัวอย่างของใบนี้ ฆ่าตัวถัดไป
4. ยืนให้เห็นจุดที่มอนล้ม **และเห็นออกไปทางแกน +X อย่างน้อย `30 x (N-1) + 60` หน่วย**
   (สาย B กระจายของทีละ 30 หน่วยบน X ⇒ ของ 2 ชิ้นต้องการแค่ ~90 หน่วย ของ 5 ชิ้นต้องการ ~180)
   🔴 ถ้ากล้องไม่กว้างพอ **ป้ายที่หายอาจอยู่นอกจอ ไม่ใช่ไม่ถูกวาด** ⇒ รอบนั้นเป็น NO-RESULT
5. ตัดเฟรมจากวิดีโอ (ไม่ใช่ตาเปล่า) แล้ว **นับป้ายในเฟรมที่มีป้ายมากที่สุด** · จดข้อความบนป้ายทุกป้ายที่อ่านออก

### 🔴 ด่านบิลด์ ทำก่อนอย่างอื่น ผิดด่านนี้ = หยุดทั้งใบ ห้ามนับป้าย
บรรทัดคอนโซลของการตายที่มีของ ≥ 2 ชิ้น **ต้องมีทั้งสองคำนี้**:
`MOB_LOOT_DROPS_CENSUS ... drops=N generations=1 pc_bytes=<17+27N>`
- **ไม่มีคำว่า `generations=`** ⇒ บิลด์เก่า ⇒ **หยุดทั้งใบ อย่านับป้าย** รายงานว่า build ผิด
- `generations=1` แต่ `pc_bytes` ≠ `17+27N` ⇒ **หยุดทั้งใบ** แจ้งสาย B · จด `BOOT_COMMIT` ทุกครั้ง
🔴 **ห้าม grep `MOB_LOOT_DROP`** (ชื่อ action ในโค้ด ไม่เคยพิมพ์) และห้ามใช้ event `mob_loot_drops_sent_*`
(ออกเฉพาะเมื่อบูตด้วย `--export-events` ซึ่งใบนี้ห้ามใส่แฟล็ก) — ฉบับแรกสั่งทั้งสองอย่าง **ผิดทั้งคู่**

### เกณฑ์ผ่านสองชั้น
- **ชั้น wire/DB**: ด่านบิลด์ข้างบนผ่าน (`generations=1` + `pc_bytes` ตรงสูตร + `drops=N` ≥ 2)
- **ชั้น client-observable**: จำนวนป้ายที่นับได้จากเฟรมวิดีโอ + ข้อความบนป้าย + เวลาที่ป้ายแรกปรากฏและหายไป

### อ่านผลยังไง — 🔴 ใบนี้ต้องมีทางที่ทำให้การเปลี่ยนทรงเสียหน้าได้ ไม่งั้นมันไม่ใช่การวัด
- **นับได้ = `N`** ⇒ ทรงใหม่ทำสิ่งที่ผู้เล่นเห็นต่างจริง ⇒ **PASS**
- **นับได้ = `1` (ด่านบิลด์ผ่าน)** ⇒ 🔴 **FAIL ของใบนี้** — ไม่ใช่ FAIL ว่าทรงผิดกฎ แต่คือคำตอบว่า
  **การ coalesce ไม่ได้ซื้ออะไรให้ผู้เล่น** ⇒ สาย B ต้องตอบรอบถัดไปว่าคงไว้ทำไม หรือถอย
  (`mob_loot` NONCLAIM 22 มี rollback เขียนไว้)
- **นับได้ = `0`** ⇒ รันซ้ำอีกรอบด้วยมอนคนละตัว/ของคนละตาราง · ยัง `0` ⇒ 🔴 **FAIL**
  (เลนนี้ไม่วาดอะไรเลยบนบิลด์นี้ — แรงกว่า `1` ไม่ใช่ NO-RESULT) · ได้ `≥ 1` ⇒ ใช้ค่ารอบที่สอง
- 🔴 **G-OBS บังคับ**: จดหมายผลต้องมีบรรทัด `OBSERVER_CONFIRMED: <เวลา+07:00>` ไม่งั้น chief ไม่บริโภคเป็นผลปิดใบ

### nonclaims
1. [ไม่อ้าง] ว่าใบนี้วัด **อายุ** ป้าย — วัดจำนวน · ได้เวลามาถือเป็นของแถม ห้ามเอาไปทับ `GT-045`
2. [ไม่อ้าง] อะไรเรื่อง **การเก็บของ** — ยังไม่มีเส้นทาง pickup บนบิลด์นี้ (`RE-125`)
3. [ไม่อ้าง] อะไรเรื่อง **ฆ่าสองตัวติดกัน** — ช่องนั้นยังเปิด (`mob_loot` NONCLAIM 20)
4. [ไม่อ้าง] ว่าเห็นกี่ป้ายแปลว่ามี **วัตถุ** บนพื้น — `GT-045` วัดแล้วว่าไม่มีโมเดลใต้ป้าย

**ADDRESSEE: ผู้เทส (attended)** · **ผู้เปิดใบ: LANE-B (รอบ `zxnwtd`)** — ผลกลับมาที่สาย B บริโภค

---

## GT-133 GM-003 CHAT-SAY-VISIBLE-001 [attended, in-game]: GM พิมพ์ `/say <ข้อความ>` ลงกล่องแชทธรรมดา แล้ว**ข้อความโผล่บนจอของ GM เองในรูปแบบ GM global message หรือไม่**  [🔴 **BLOCKED x2 · ห้ามบันทึก `PASS` ไม่ว่าผลบนจอจะออกมาอย่างไร** (`COO-DECISION 20260829_0041` ข้อ 1-2 · เขียนกำกับโดย chief รอบ `wi1m62`): ประตู `GM_GLOBAL_MESSAGE_VITAL_VERSION_CONFIRMED = None` เป็น **ล็อกทางการ** ระดับเดียวกับ `FORCE_POS_*` เปลี่ยนได้ด้วย COO-DECISION ใบใหม่เท่านั้น · เหตุผลคือเงื่อนไข (A) ตัวตนต่อ connection ล้วน ๆ -- ไบต์ที่ถูกไม่ได้แปลว่าคนที่ส่งไบต์นั้นเป็นคนที่เราคิด · ผลที่ดีที่สุดที่ใบนี้บันทึกได้ตอนนี้คือ `AWAITING-DECISION` · 🔴 chief รอบ `wi1m62` เพิ่ม: **ข้อ (ก) ข้างล่าง stale แล้ว** -- `CORE-REQUEST-GM-029` อยู่บน main ตั้งแต่ `pirate-force-server#214` merged 2026-08-28T17:35Z ⇒ ตัวบล็อกที่เหลือจริงคือข้อ (ค) ข้อเดียว (~~x3~~ -- `RE-132` ตอบแล้ว 2026-08-29T00:10+07:00 ข้อ (ข) ตกไป ปิดหัวใบ RE ในรอบ `z6gu2n`) **-- ห้ามบูต:** (ก) `CORE-REQUEST-GM-029` ยังไม่ลง main (จุดเรียกที่ **คืน action** ที่สาขา `0xAC52`; วันนี้ main มีแต่ `fire()` ซึ่งไม่คืนค่า ⇒ ส่งไบต์ไม่ได้ตลอดกาล) ~~(ข) `RE-132` ยังไม่ตอบ~~ **ตอบแล้ว** (`notes_to_chief/20260829_0010_RE-132-RESULT-VERSION-ZERO-RENDER-PATH.md`): ไบต์ = `0` เท่ากับที่ codec ส่งอยู่แล้ว และ handler `0x0065C850` มีทางไป display sink (static เท่านั้น — ตัดทางที่ข้อ (B) จะพังที่ถูกที่สุดออก ไม่ได้ทำให้ (B) ผ่าน) ⇒ **ไบต์ไม่ใช่ตัวบล็อกอีกต่อไป** · `say_wire.GM_GLOBAL_MESSAGE_VITAL_VERSION_CONFIRMED` ยัง `None` **เจตนา** เพราะข้อ (ค) ข้างล่างข้อเดียว และยังมีเทสบังคับไว้ (`tests/test_gm_say_action.py::SayVersionGateTests`) · เกณฑ์ชั้น client-observable ของใบนี้ไม่เปลี่ยน: static render-path ไม่ใช่หลักฐานว่าขึ้นจอ (ค) 🔴 **ตัวตนต่อ connection** -- `runtime.py:4765-4774` บันทึกไว้เองว่า `session.token` คือค่า `--token` ของ **โปรเซส** ไม่ใช่ login ที่ยืนยันตัวตนต่อ connection และเขียนไว้ว่าคำถามนี้ "ต้องตอบ**ก่อน**จะต่อ executor เข้าจุดนี้ ไม่ใช่หลัง" (ยืนยันอิสระโดย `reports/PF_MULTIPLAYER_READINESS_AUDIT001_*_20260818.md` I01-I04: `v141:7859` ค่าเริ่มต้น `"localtest"` · `v141:7399` ทุก connection ที่รับเข้ามาใช้ token เดียวกัน · ไม่มี `parse_login*` ⇒ ชื่อบัญชีที่ client ส่งมาไม่เคยถูกอ่าน) ⇒ `/warp` ติดสามชั้นจนไม่มีวันมาถึงจุดนี้ก่อน แต่ `/say` ติดน้อยที่สุด **จึงเป็นคำสั่งที่จะมาถึงจุดนี้เป็นตัวแรกและเป็นตัวที่จะขึ้นเงินบั๊กนี้**]

> เลขใบ: ตัวนับเดียวร่วมกับ `CLIENT_RE_QUEUE.md` · รอบ `w8hnu9` จอง `RE-132` ที่นั่นและ `GT-133` ที่นี่
> (เว้น `GT-132` ไว้กันชนกับใบที่อาจจองพร้อมกัน) · grep ยืนยันก่อนจอง 2026-08-28T23:2x = 0 hit ทั้งสองไฟล์
> สูงสุดก่อนหน้า = `GT-131` (สาย A) / `RE-130`

### ทำไมใบนี้อาจบูตได้**ก่อน** `GT-128` ทั้งที่เปิดทีหลัง
`GT-128` (`/warp`) ติดสามข้อ และข้อที่หนักที่สุดคือ **ล็อกของ COO เรื่องเจ้าของตำแหน่ง**
(`CORE-REQUEST-GM-030` ต้องลง main ก่อน แล้ว COO ถึงปลด) · `/say` **ไม่ขยับใคร ไม่เขียนแถวถาวร
ไม่แตะ move-authority baseline** ⇒ ไม่มีล็อกนั้นเลย เหลือสองข้อข้างบนเท่านั้น
⇒ ถ้า `RE-132` ตอบก่อนที่ GM-030 จะลง main ใบนี้จะเป็น **คำสั่ง GM ใบแรกที่ตัดสินที่จอ**

### ด่านก่อนบูต (ทั้งสามต้องผ่าน มิฉะนั้นเลื่อน)
1. grep บน `main` เจอจุดเรียก `make_gm_chat_command_action` จริงที่สาขา `0xAC52` ของ `runtime.py`
   (เห็นบรรทัดบน main ไม่ใช่แค่ PR merged) -- ด่านเดียวกับ `GT-128` ข้อ 1
2. `grep -n "GM_GLOBAL_MESSAGE_VITAL_VERSION_CONFIRMED" src/pirateforce_foundation/gm/say_wire.py`
   ต้อง**ไม่ใช่** `None` และคอมเมนต์เหนือมันต้องอ้าง `RE-132` ที่ปิดแล้วพร้อม VA
3. บัญชีที่จะบูตอยู่ใน `gm_accounts.json` (ค่าเริ่มต้นว่าง = ไม่มีใครเป็น GM)

### ขั้นตอน (ที่ใจกลางเมือง X=11865 Y=6147 ห้ามท่าเรือ)
1. login ด้วยบัญชี GM รอโหลดฉากเสร็จ
2. พิมพ์ในกล่องแชทธรรมดา: `/say ทดสอบ GM 133` -- **จดว่าเห็นอะไรบนจอ ทีละอย่าง**:
   ข้อความโผล่ไหม · โผล่ในกล่องแชทหรือกลางจอ · สีอะไร · มี prefix/ชื่อผู้พูดไหม (ควรว่าง)
   · โผล่**สองครั้ง**ไหม (บรรทัดแชทปกติของตัวเอง + GM global = คนละบรรทัด ต้องแยกให้ออก)
3. พิมพ์ `/say` ภาษาไทยยาว ๆ หนึ่งบรรทัด -> ตัวอักษรครบไหม เพี้ยนไหม (สายส่ง UTF-16LE)
4. **เคสลบที่ต้องทำด้วย**: พิมพ์ข้อความธรรมดา (ไม่ขึ้นต้น `/`) -> ต้องเป็นแชทปกติ ไม่มี GM global
   · พิมพ์ `/say` เปล่า ๆ -> ต้องไม่เกิดอะไร ไม่ค้าง ไม่หลุด
5. ให้ผู้เล่นธรรมดา (บัญชีนอก `gm_accounts`) พิมพ์ `/say ...` -> ต้องไม่เกิดอะไร ไม่มีแถวใน ndjson
   🔴 **อ่านก่อนทำข้อนี้ (เพิ่มโดยผู้เปิดใบ หลัง pf-adversary รอบ `w8hnu9`): วันนี้ข้อนี้วัดอะไรไม่ได้เลย**
   ตราบใดที่บล็อกเกอร์ (ค) ยังอยู่ ทุก connection ใช้ `--token` ตัวเดียวกัน ⇒ ชื่อบัญชีที่คุณ login
   ด้วยไม่ถูกอ่านจากสาย · ถ้าคุณ logout แล้ว login ใหม่ด้วยอีกบัญชี **token ฝั่งเซิร์ฟเวอร์ไม่เปลี่ยน**
   ⇒ ผลจะออกมา "ไม่เกิดอะไร" หรือ "เกิด" ตามค่า `--token` ที่บูตมา ไม่ใช่ตามบัญชีที่พิมพ์
   ⇒ **ห้ามบันทึกข้อนี้เป็น PASS** ให้เขียนว่า "ยังตัดสินไม่ได้ (บล็อกเกอร์ ค)" จนกว่าตัวตนต่อ
   connection จะมีจริง · ถ้าอยากตัดสินจริงต้องมีสอง connection พร้อมกัน ซึ่งโปรเจกต์ยังไม่เคยมี
   (`PF_SESSION_LIMIT001`) ⇒ เป็นใบใหม่ ไม่ใช่ขั้นตอนในใบนี้
6. 🔴 **ถ้าจอขึ้น modal error แล้วหลุด** = `vital_version` ที่ `RE-132` ให้มาผิด **หยุดทันที**
   จดเลข `ErrorData=` แล้วปิดใบเป็น FAIL -- นี่คือเหตุการณ์เดียวกับ `GT-101` และเป็นเหตุผลที่ใบนี้ถูกกั้นไว้

### เกณฑ์สองชั้น
- **ชั้น wire/DB:** คอนโซลมี `LANE_GM_CHAT_SAY_GM_GLOBAL_MESSAGE` หนึ่งครั้งต่อหนึ่งคำสั่งที่รับ
  · `LANE_GM_CHAT_ACTION say route=action` บน stderr · ndjson: ~~**หนึ่งแถวต่อหนึ่งคำสั่ง**
  (สองแถว = เผลอ wire ทั้ง `fire()` และ action -- ห้ามมีทั้งคู่)~~ **แก้รอบ `nz0qt2`:** ตั้งแต่
  `CORE-REQUEST-GM-032` ข้อ 1-2 (PR `pirate-force-server#223`) หนึ่งคำสั่ง = **`issued` + `outcome`**
  ⇒ วิธีจับ double-wire เปลี่ยนเป็น **นับ `record_id` ที่ไม่ซ้ำกัน**: หนึ่งคำสั่งต้องได้ `record_id`
  เดียว · เห็นสอง `record_id` สำหรับบรรทัดที่พิมพ์ครั้งเดียว = เผลอ wire สองทางจริง (ดู P1 ของ `GT-127`
  สำหรับวิธีตัดสินว่า BOOT_COMMIT ของคุณเป็นแบบไหน)
- **ชั้น client-observable:** เจ้าของเห็นข้อความบนจอ (ภาพ + คำบอกเล่า)

### nonclaims ที่ผลของใบนี้ **ห้าม**ถูกใช้อ้าง
1. [ไม่อ้าง] ว่าเป็น **broadcast** -- action ไปที่ socket เดียว (ของ GM เอง) ผู้เล่นคนอื่นไม่ได้รับอะไร
   การกระจายทั้งเซิร์ฟเวอร์เป็นจุดใน `runtime.py` และเป็นใบ CORE-REQUEST คนละใบที่ยังไม่เปิด
   ⇒ ถ้าอยากรู้ว่าคนอื่นเห็นไหม ต้องมีผู้เล่นที่สอง **และ**ใบใหม่ ไม่ใช่ใบนี้
2. [ไม่อ้าง] ว่าระบบแชทของเกมทำงาน -- ใบนี้พิสูจน์ทางเดียว (server -> client) ของ **หนึ่ง** channel
3. [ไม่อ้าง] ว่า `/warp` หรือคำสั่งอื่น (`npc`/`item`/`lv`/`spawn`) ทำงาน -- คนละไบต์ คนละด่าน
4. [ไม่อ้าง] ว่า milestone ใดผ่าน -- **GM คือเครื่องมือไปถึงสภาพที่จะเทส ไม่ใช่หลักฐานว่าฟีเจอร์ทำงาน**
   ถ้าใบนี้ PASS สิ่งที่ได้คือ "GM สื่อสารกลับมาที่จอตัวเองได้" = ช่องทางยืนยันผลคำสั่ง GM
   (`GM_RunGMCommandResultVital` ยังไม่รู้ layout) ไม่ใช่ว่าเกมมีระบบประกาศแล้ว

### 🔴 ถ้าไม่มีข้อความโผล่บนจอ ให้แยกสองสถานะก่อนบันทึกผล (เพิ่มโดย LANE-GM เจ้าของใบ รอบ `tvbiqc` 2026-08-29T22:3x+07:00)
พิมพ์ `/say ...` แล้ว grep คอนโซลเซิร์ฟเวอร์หา `GM_CHAT_NO_BYTES_SENT`
· **เจอ** (จะมี `why=withheld_gm_global_message_vital_version`) = เซิร์ฟเวอร์ **จงใจไม่ส่ง** เพราะเกตของ
`gm/say_wire.py` ยังปิดอยู่ ⇒ **BLOCKED ไม่ใช่ FAIL** ใบนี้ยังไม่ได้ถูกทดสอบเลย
· **ไม่เจอ แต่มี** `LANE_GM_CHAT_ACTION say route=action` = เฟรมออกไปจริง จอเงียบ = ผลลบของจริง
(ก่อนรอบ `tvbiqc` สองสถานะนี้หน้าตาเหมือนกันบนคอนโซล)

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

## GT-134 BG0015-FIRST-EYES-001 [attended, in-game]: เกาะภูเขาไฟนรก `Bg0015` (scene 14) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเจกต์ในฉากนี้  ~~[BLOCKED]~~ ~~[READY]~~ **[PASS]** -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-140 GM-KILLSWITCH-WITHHOLDS-AND-SAYS-SO-001 [STATIC-ON-BRIDGE -- เกตเต็มบนสะพาน py -3 · คลาวด์รันแทนไม่ได้]: สวิตช์ `production_allowed` บนเส้นทางตรง `0xAC52` **กั้นได้จริงและเรียกชื่อการกั้นออกมา** หรือเป็นแค่บรรทัดในโค้ด  [BLOCKED -- **รอ merge ก่อน**: `pirate-force-server#222`]

**ที่มา:** commit `630106d` (`COO-DECISION 20260829_0041` ทาง ข) หายจาก `main` เพราะ `#218` ถูกปิดโดยไม่ merge · re-land เป็น `#222`
**ทำไมต้องสะพาน:** คลาวด์รันได้แค่ sanity · เกตเต็มมี cp874 + พฤติกรรม 3.14 ที่คลาวด์มองไม่เห็น

- objective: ธง `production_allowed` ของ `lane_gm_chat_command` = `False` ⇒ เส้นทาง `0xAC52` **ไม่ปล่อยอะไรออก และเรียกชื่อการยืนหยุดบนสองร่องรอย** · = `True` ⇒ **ปล่อยของออกจริง** (สองแขนคือสวิตช์เดียวกัน ใบที่มีแขนเดียวไม่ได้พิสูจน์สวิตช์)
- db: ไม่เปิด DB ใด ๆ · ต้องบูตให้ใช้สำเนา `state\run_gt140.sqlite3` · 🔴 ห้ามเปิด canonical · จด `CANON_SHA` ก่อน-หลังต้องตรงกัน
- server args: ไม่บูตเซิร์ฟเวอร์/ไคลเอนต์ · ขับผ่าน `py -3 -m pytest` และ `git grep` เท่านั้น · ห้ามใส่ `--*-scenario`
- steps:
    0. ด่านก่อนวัด (ไม่ผ่าน = เลื่อนใบ ไม่ใช่ FAIL): `#222` ต้อง `merged=true` · ยังไม่ merge = ห้ามเริ่ม
    1. `git pull --rebase` · จด `git rev-parse HEAD` = `<SHA>`
    2. `git grep -n "module_production_allowed" <SHA> -- src/pirateforce_foundation/runtime.py`
       🔴 ต้องเป็นโค้ดที่รันได้ **ไม่ใช่คอมเมนต์** (`GT-127` เคยผ่านด่านด้วย hit ที่เป็นคอมเมนต์) · เจอแต่คอมเมนต์ = หยุด
    3. เกตเต็ม `py -3 -m pytest -q -p no:cacheprovider` · คัดลอกบรรทัดสรุปดิบ ห้ามสรุปเป็นคำพูด
    4. `py -3 -m pytest -v tests/test_lane_hooks.py tests/test_gm_chat_command_dispatch_wiring.py` · คัดลอกชื่อเทสทุกข้อพร้อมผล
    5. ตัวคุมกันใบว่าง (mutation): ลบ `and lane_hooks.module_production_allowed("lane_gm_chat_command")` ออกจากกิ่ง `0xAC52` ใน working tree -> รันข้อ 4 ซ้ำ -> ต้องมี **อย่างน้อยหนึ่งข้อแดง** -> `git checkout -- src/pirateforce_foundation/runtime.py`
       🔴 ห้าม commit ห้าม push การแก้นี้
    6. `git grep -n "route_closed_not_production_allowed" <SHA> -- src/` แล้วอ่าน else-branch เดียวกันเอา **ชื่อโทเคน stderr ตัวจริง**
       🔴 คัดลอกชื่อจากโค้ด **ห้ามใช้ชื่อในใบนี้เป็นคำตอบ** (ชื่อในใบเป็นคำทำนาย) · 0 hit = จดชื่อที่มีจริง ไม่ใช่ FAIL
    7. ข้อ 3 แดงด้วยโมดูลที่ไม่เกี่ยวกับสาย GM ⇒ จดจำนวน+ชื่อไฟล์ ชี้ไป `GT-125` **ไม่ใช่ FAIL ของใบนี้**
- pass criteria: 🔴 สองชั้นแยกกัน ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น
    wire/DB (พิสูจน์ headless ครบ ไม่ต้องมีคนหน้าจอ):
      (ก) **แขนปิด** `False` -> ไม่มี action ต่อท้ายคิว · ไม่มีแถวใน `capture/gm_command_log.ndjson` · เฟรมเดินต่อครบ (`rx_frames` ไม่ขยับ)
      (ข) **กั้นแล้วถูกเรียกชื่อ ไม่เงียบ** สองร่องรอยพร้อมกัน: event `gm_chat_action_route_closed_not_production_allowed` [คำทำนาย -- ยืนยันด้วยข้อ 6] + โทเคน stderr ของ else-branch เดียวกัน ⇒ แยก "ล็อกว่างเพราะปิดสวิตช์" ออกจาก "ล็อกว่างเพราะสายขาด" ได้ · ขาดร่องรอยใดร่องรอยหนึ่ง = ไม่ผ่านข้อนี้
      (ค) **แขนเปิด** `True` -> `/lv 30` ผ่าน dispatcher จริง: มี action ต่อท้ายคิว + event `gm_chat_action_accepted_lv` + ndjson 1 แถว + โทเคน `LANE_GM_CHAT_ACTION ... route=action`
          🔴 ขาดแขนนี้ ใบ "ผ่าน" ได้เพราะทุกอย่างดับอยู่แล้ว = ไร้ค่า
      (ง) mutation ข้อ 5 ฆ่าได้จริง (>= 1 แดง) · ไม่แดงเลย = เทสไม่ได้พินอะไร ⇒ ผลเป็นโมฆะ
      (จ) เกตเต็มบนคอมมิต merge `0 failed` · sha ของ canonical DB ตรงก่อน-หลัง
    client-observable: 🔴 **ใบนี้ไม่มีชั้นนี้เลย** ไม่มีอะไรถึงจอผู้เล่นแม้แต่พิกเซลเดียว ⇒ ห้ามเกรดราวกับมีชั้นนี้ · **ไม่ต้องมี `OBSERVER_CONFIRMED` และห้ามรอมัน** · ห้ามใช้ผลใบนี้อ้างว่าอะไรปรากฏ/ไม่ปรากฏบนจอ
- nonclaims:
    1. ไม่อ้างว่า `/warp`/`/say` ส่งไบต์ถึงไคลเอนต์ได้ -- คนละบานประตู (`RE-129`) และยังปิดโดยตั้งใจ
       🔴 "ไบต์" ในใบนี้ = ของที่เส้นทางนี้ปล่อยออก (action + ร่องรอย) **ไม่ใช่ไบต์ที่ถึงจอ** · วันนี้ไม่มีคำสั่ง GM ตัวไหน `executed` = true
    2. ไม่อ้างว่าพลิกสวิตช์ตอนรันได้ -- ต้องแก้ไฟล์แล้วรีสตาร์ต (`COO-DECISION 20260829_0141`)
    3. ไม่อ้างอะไรแทน `GT-127`/`GT-128` -- สองใบนั้นตัดสินด้วยบูตจริง ใบนี้ไม่บูตอะไรเลย
    4. **ผลลบมีค่าเท่าผลบวก:** `False` แล้วยังมี action/แถว ndjson = สวิตช์ยังไม่ได้ต่อจริง ⇒ ส่งกลับ chief + COO ว่าคำสั่ง `0041` ยังไม่ถูกทำ (ไม่ใช่เปิดใบ attended)

**ผู้เปิดใบ: chief (สาย E) รอบ `8tpw8k` / R219** -- ผลกลับมาที่ chief บริโภค

### result (ผู้เทสกรอก)
```

```

---

## GT-141 GM-003 CHAT-WARP-STAGED-LOGIN-SCENE-001 [attended]: GM พิมพ์ `/warp <ฉากที่พินไว้>` ลงกล่องแชท แล้วล็อกเอาต์-ล็อกอินใหม่ -- โผล่ที่ฉากนั้นไห... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## STORE-INSERT-001 [CHIEF-WORK · ไม่ใช่ใบเทส ไม่ต้องเปิดเกม]: `store.py` เขียนแถวของที่เก็บได้ลง DB จริง และเดินตัวนับ `next_item_identity`  [push แล้ว รอ merge `pirate-force-server#244` (แทน ~~#241~~ ที่ถูกปิดเพราะเกตแดง) · เจ้าของ: chief (สาย E)]

> 🟡 **สถานะ 2026-08-29T07:1x+07:00 (R224 `4gqnwm`): งานเสร็จและ push แล้ว รอ merge `pirate-force-server#244`** — ห้ามอ่านว่า "อยู่บน main" จนกว่ารอบถัดไปจะเห็น `merged=true`
> เกณฑ์ปิดตั๋วทั้งห้าข้อ ทำครบตามนี้ [วัดแล้ว บน branch `claude/bold-dijkstra-4gqnwm`]:
> ① `store.commit_acquired_backpack_item` — INSERT แถว + `UPDATE next_item_identity` ใน `BEGIN IMMEDIATE` เดียว (เทส atomicity ฉีด exception หลังทั้งสอง write แล้ววัดว่า **ทั้งแถวและตัวนับไม่ขยับ**)
> ② identity มาจากคอลัมน์ ไม่ใช่ `MAX+1` — เทสตั้งตัวนับไว้ที่ 9 บนกระเป๋าที่ identity สูงสุดคือ 4 แล้ววัดว่า `MAX+1` (=5) **ถูกปฏิเสธโดยระบุชื่อ** ส่วน 9 ผ่าน
> ③ เจ้าของ session ตรวจแบบเดียวกับ `save_position` (เทส: session ของบัญชีอื่น + session ที่ปิดแล้ว ⇒ `PermissionError` และไม่มีอะไรถูกเขียน)
> ④ เทส 15 ข้อ ฆ่า mutation ได้จริง 8/8 ที่ลอง (ถอดการเดินตัวนับ · เปลี่ยน identity เป็น `MAX+1` · ถอดการตรวจเจ้าของ · ถอด `-1` ของ `issued_through` · seed ตัวนับจากค่า default · ถอดการตรวจช่องซ้ำ) · roundtrip: เก็บ → relog → `get_backpack` → `bag_admission` ให้ `golden_plus_acquired`
> ⑤ `HYPOTHESIS_LEDGER PASS entries=47` ไม่มี drift · สวีตเต็ม **4,362 passed 0 failed 323 skipped** (หลังแก้ `pf-adversary`) เขียว(cloud sanity — ไม่ใช่เกตเต็ม) · ตระกูล HYP-PF-008/010/017/018 ยังถูกปฏิเสธเหมือนเดิม
>
> 🔴 **ผลข้างเคียงที่ต้องรู้:** เทสวันหมดอายุของสาย B (`tests/test_bag_admission_expiry.py`) ออกแบบให้ **แดงวันที่ตั๋วนี้ลง** และมันแดงจริง
> รอบนี้ **แปลงเป็นหมุด ไม่ได้ลบ** (พินว่าใครเขียนคอลัมน์/INSERT แถวได้บ้าง) และ **ไม่ได้ตัด `_classify_against` ตาม `COO-DECISION 20260829_0441` ข้อ 2**
> เพราะวัดแล้วว่าการตัดทิ้งทำให้ด่าน 2 **รับ** กระเป๋า HYP-PF-008 และ HYP-PF-010 ⇒ ขอคำตัดสิน: `notes_to_chief/20260829_0706_CHIEF-ASK-COO-delete-classify-against-admits-hyp008.md`
>
> 🔴 **ยังไม่ปลด `GT-142`**: ตั๋วนี้ปิดครึ่ง "เขียนลง DB" เท่านั้น · อีกครึ่งคือ call site (`GT-124` — `runtime.py` ยังไม่เรียก `mob_pickup.dispatch_pickup_request`) ซึ่งเป็นใบถัดไปของ chief ตาม `COO-DECISION 20260829_0641`

> เปิดโดย chief R222 ตาม `COO-DECISION 20260829_0441` (gate-2 interim) ข้อ 3 — "เปิดตั๋วงาน INSERT จริง + เดินตัวนับใน `store.py` เป็นเจ้าของเอง คิวก่อน M5 ปิด" · กำหนดเปิดตั๋ว: 30 ส.ค. 12:00 (เปิดแล้วรอบนี้) · M5 ครบกำหนด **31 ส.ค. 12:00**

**สิ่งที่ยังไม่มี [วัดแล้ว R222]:** `store.py` มี INSERT แถวกระเป๋าใบเดียวคือ `_insert_initial_backpack` (ตอนสร้างตัวละคร) · **ไม่มี**เส้นทางเขียนแถวใหม่จากการเก็บของ และ **ไม่มี**อะไรเดินคอลัมน์ `character_backpacks.next_item_identity` (คอลัมน์มีจริงตั้งแต่ `migrations/005_character_backpack_identity_counter.sql` และ backfill แล้ว) · `MOB_PICKUP_ROW_WOULD_INSERT` เป็น **log ไม่ใช่ INSERT**

**เกณฑ์ปิดตั๋ว (wire/DB ล้วน · พิสูจน์ headless ได้ในตัว ไม่ต้องรอผู้เทส):**
1. `store` มีเมธอดเดียวที่ INSERT แถวที่เก็บมา **ในทรานแซกชันเดียวกับ**การเดิน `next_item_identity` (ล้มพร้อมกัน สำเร็จพร้อมกัน) — แถวที่ identity 5 โผล่โดยตัวนับยังเป็น 5 คือความล้มเหลวของตั๋วนี้
2. identity มาจาก `next_item_identity` ของแถวนั้น **ไม่ใช่** `MAX(identity)+1` ที่คำนวณสด (`mob_pickup.next_item_identity` อธิบายไว้เองว่ากระเป๋าที่หดแล้วจะออกเลขซ้ำ)
3. เจ้าของ session ถูกตรวจแบบเดียวกับ `save_position` (สิทธิ์ session/character) — เขียนแทนคนอื่นไม่ได้
4. เทสที่ **ฆ่า mutation ได้**: เก็บของ → อ่านกลับผ่าน `store.get_backpack` → ผ่านด่าน 2 (`bag_admission.may_enter_world`) → `verdict=golden_plus_acquired`
5. `HYPOTHESIS_LEDGER` PASS · สวีตเต็มเขียว(cloud sanity) · ไม่มี regression ของตระกูล HYP-PF-008/010/017/018

**ปลดอะไร:** `GT-142` (ใบปิดวง M5) ที่ `BLOCKED-BY` ตั๋วนี้อยู่ · nonclaim: ตั๋วนี้ไม่แตะ call site ของการคลิกเก็บ (`GT-124` — `runtime.py` ยังไม่มีจุดเรียก `mob_pickup.dispatch_pickup_request`) ⇒ ปิดตั๋วนี้แล้ววง kill→pickup→relog **ยังไม่ครบ** จนกว่าครึ่งนั้นจะมี


---

## GT-143 BG0002-SET103-FIVE-PLACEMENTS-001 [attended, in-game]: ยืนไปดูพิกัดห้าจุดใน Prison Exile -- ตรงนั้นมี Orc Chief หรือไม่มีอะไรเลย  [~~OPEN~~... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## GT-142 M5-KILL-PICKUP-RELOG-ROUNDTRIP-001 [attended, in-game]: ฆ่ามอนใน `Bg0002` -> เก็บของที่ตก -> relog แล้ว **ของชิ้นนั้นยังอยู่ในกระเป๋า** จริงหรือไม่ -- ใบปิดวง M5 ใบเดียว  [🔴 **BLOCKED - P-2 not closed (NOW) + GT-223 FAIL R309 owned by LANE-B 1649** · ตั้งโดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 ตาม `COO-DECISION 20260904_2349` ข้อ 2 · ตัวบล็อกเดิม (`STORE-INSERT-001` · opcode จาก `GT-146` · call site `GT-124`) หมดจริงแล้ว **แต่ใบนี้เป็นใบตีมอน** ⇒ ยังห้ามปลดเป็น READY จนกว่า P-2 จะปิด (`NOW.md` หัวข้อ "ห้ามทำจนกว่า P-2 จะปิด")]

> 🔴 **บรรทัดบังคับของใบตีมอนทุกใบ (`COO-DECISION 20260902_1848` ข้อ 2 · ร่างโดย LANE-B ใบ `20260902_2240` · เติมโดย chief R311):**
> **ข้ามฉากแล้ววาปกลับ = เลือดมอนกลับเต็ม เป็นของที่รู้อยู่แล้ว ประกาศไม่แก้ ไม่ใช่ FAIL ของการตี**
> จะวัดว่าเลือดลดจริง ต้องตีและอ่านผล **ในฉากเดียวกัน ไม่ข้ามฉากคั่น** · ถ้าข้ามฉากแล้วกลับมาเห็นเลือดเต็ม
> ให้จดว่า `known: wound reset on scene re-open` แล้วเทสต่อ **ห้ามปิดใบเป็น FAIL ด้วยเหตุนี้**

> 🔴 **`BLOCKED-BY: STORE-INSERT-001`** (chief เป็นเจ้าของ · เปิดรอบนี้ตาม `COO-DECISION 20260829_0441`
> (gate-2 interim) ข้อ 3) · ตาม `COO-DECISION 20260829_0441` (vote ข้อ 6 กฎ 2-3): ใบนี้ **เริ่มที่ BLOCKED
> ไม่ใช่ READY · ห้ามขึ้นหัวคิว ห้ามเรียกผู้เทส** จนกว่าตั๋วรากปิด · เปิดใบไว้ล่วงหน้าเพื่อไม่ต้องคิดขั้นตอนใหม่ตอนปลด
> 🔴 **กฎ 4 ของมติเดียวกัน:** ห้ามเกรดใบคอมแบตใด ๆ จนกว่า **`RE-139`** ปิด ⇒ ใบนี้ **เก็บหลักฐานได้ แต่ให้ผล
> PASS/FAIL ไม่ได้** จนกว่า `RE-139` ปิด (เขียนสถานะเป็น `AWAITING-OBSERVER` ระหว่างรอ + ต้องมี `OBSERVER_CONFIRMED` ตาม G-OBS)

### ที่มา (วัดสดรอบ R222 · 2026-08-29 · สามบรรทัด ไม่ใช่ประวัติรอบ)
- ด่าน 2 **ต่อสายแล้ว**: `session.select_and_start` เรียก `bag_admission.may_enter_world` แทน
  `inventory.is_unmoved_baseline` และพิมพ์ `BAG_ADMISSION verdict=... golden=... acquired=... [reason=...]`
  ลง **stderr เฉพาะทางปฏิเสธ** (`session.py`) 🔴 **รอ merge ก่อนบูต** (`pirate-force-server` PR #233)
- 🔴 **ตัวบล็อกจริง**: `store.py` **ไม่มี INSERT แถวของที่เก็บได้** ลง `character_backpack_items` (INSERT เดียวที่มีคือ
  `_insert_initial_backpack` ตอนสร้างตัวละคร) และ **ไม่เดิน** `character_backpacks.next_item_identity`
  (คอลัมน์จาก `migrations/005_*.sql`) ⇒ ของที่เก็บ **ไม่รอดข้าม DB** ไม่ว่าด่าน 2 จะรับอะไร ·
  `MOB_PICKUP_ROW_WOULD_INSERT` เป็น **log ไม่ใช่ INSERT** (`mob_pickup.py` หัวข้อ THE WALL)
- `runtime.py` ยังไม่มี call site ของ `mob_pickup.dispatch_pickup_request` (grep รอบ R222 = 0 hit) -- ครึ่งนั้นคือ `GT-124`

### objective (ข้ออ้างเดียว)
หลัง `STORE-INSERT-001` ลง main: ของหนึ่งชิ้นที่ผู้เล่นเก็บจากซากมอนใน `Bg0002` **รอด relog** กลับเข้ามาอยู่ใน
กระเป๋าของตัวละครเดิม -- ครบวง kill -> pickup -> relog **จริงหรือไม่**

### db · server args (เป๊ะ)
db = **สำเนา** `state\run_gt142.sqlite3` (จาก `default_state\pirateforce.sqlite3`) · ห้ามเปิด canonical · sha ก่อน-หลัง
`py -3 -u -m pirateforce_foundation.app --db state\run_gt142.sqlite3 --export-events`
`--export-events` **บังคับ** และปลอดภัย: เปลี่ยนเฉพาะสิ่งที่พิมพ์ ไม่เปลี่ยนสิ่งที่ส่ง (`runtime.py`)
🔴 ห้ามมีแฟล็ก `--*-hypothesis-scenario` ใด ๆ · client `-SecondPasswordMode bypass`

### ขั้นตอน (ต่อเนื่องหนึ่งวิดีโอ)
1. ของมาตรฐานทุกข้อตาม `ATTENDED_SESSION_RUNBOOK.md` (LOCK · สำเนา DB · `CANON_SHA` ก่อน-หลัง · เซิร์ฟเวอร์ขึ้นก่อน
   ไคลเอนต์ · NO-CRASH ด้วย **right-click-drag** ไม่ใช่ `Q`/`E` · 🔴 ห้ามพิมพ์ตัวอักษรใดตลอดรอบ · กฎสีป้ายชื่อ ·
   teardown ภายใน 420 นาที · หลังฆ่าไคลเอนต์ **restart เซิร์ฟเวอร์ก่อนบูตถัดไปเสมอ**)
2. **S0** -- ก่อนบูต: dump `character_backpacks` + `character_backpack_items` ของตัวละครที่จะเล่น
3. เข้า `Bg0002` · **ดับเบิลคลิก** ฆ่ามอนที่ตกของ (คลิกเดียว = หน้าต่างคุย NPC เปล่า -- ไม่ใช่ผลของใบนี้)
4. ถ่ายภาพนิ่ง full-res ตอนของตกลงพื้น -> เดินไปเก็บ -> ถ่ายกระเป๋าหลังเก็บ
5. **S1** -- dump DB ซ้ำ **ทันทีหลังเก็บ ก่อนออกจากเกม** (นี่คือตัวคุมของใบนี้)
6. ออกจากเกม -> restart เซิร์ฟเวอร์ -> เข้าใหม่ตัวละครเดิม -> เปิดกระเป๋า ถ่ายภาพนิ่ง -> **S2** dump DB

### 🔴 ตัวคุมที่แยกสองความล้มเหลวออกจากกัน (ห้ามข้าม)
`S1` เทียบ `S0` ตอบว่า **"ของถูกเขียนลง DB ตอนเก็บหรือเปล่า"** ก่อนที่ relog จะเข้ามาเกี่ยว:
- `S1` ไม่มีแถวใหม่ ⇒ **ของไม่เคยถูกเก็บ/ไม่เคยถูกเขียน** ⇒ ชี้กลับ `STORE-INSERT-001` หรือ `GT-124` (call site) · ไม่ใช่ปัญหา relog
- `S1` มีแถวใหม่ แต่ `S2` ไม่มี ⇒ **เก็บได้จริง แล้วหายตอน relog** = FAIL ของใบนี้ตรง ๆ

### pass criteria (สองชั้น 🔴 ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)
**wire/DB** (headless ตรวจได้ · grep `2>&1`):
- `PF-EVENT <n> mob_loot_drops_sent_<k>_pruned` โดย `k>=1` (มาได้เพราะ `--export-events`)
- `MOB_PICKUP_ROW_WOULD_INSERT table=character_backpack_items claimant=... character_id=... item_identity=...
  template_id=... quantity=... slot=...` หนึ่งบรรทัด ค่าตรงกับของที่เก็บจริง
- 🔴 **ห้าม grep `MOB_LOOT_DROPS_CENSUS`** -- `mob_loot.drops_console_line` ไม่มี call site ใน `runtime.py`
  ⇒ โทเคนนี้ **ไม่เคยถูกพิมพ์** บนบูตจริงวันนี้ (การไม่เจอ ไม่ได้แปลว่าอะไรเลย)
- ตอน select ครั้งที่สอง (relog): **ต้องไม่มีบรรทัด `BAG_ADMISSION`** เลย -- โทเคนนี้พิมพ์เฉพาะทางปฏิเสธ ⇒
  "ไม่มีบรรทัด + เข้าโลกได้" คือหลักฐานว่าด่าน 2 รับ · ถ้ามี ให้ **คัดลอกทั้งบรรทัด** (`verdict=` `golden=`
  `acquired=` `reason=`) แล้วหยุด -- นั่นคือคำตอบที่มีค่าที่สุดของรอบ
- `S2`: สี่แถว golden เดิม (identity `1..4` slot `0..3`) **ไม่ถูกแตะแม้ไบต์เดียว** + แถวใหม่ `item_identity=5`
  `slot=4` `quantity>=1` `raw_u8_38=0` `raw_u8_39=255` `detail_present=0`
  **และ** `character_backpacks.next_item_identity = 6` (ค่าก่อนรอบ = `5` ตาม migration 005)
  🔴 มีแถว identity 5 แต่ `next_item_identity` ยังเป็น `5` = **FAIL ของ `STORE-INSERT-001`** แม้ของจะขึ้นบนจอ
- `sessions` +1 · `max(lease_generation)` ไม่ถอย · `PRAGMA integrity_check` = `ok` · sha canonical ตรงก่อน-หลัง

**client-observable** (ต้องมีคนอยู่หน้าจอ · อนุมานจากคอนโซลไม่ได้เด็ดขาด):
- เห็นป้ายของตกบนพื้นหลังมอนตาย (ภาพนิ่ง full-res)
- **หลังเก็บ**: ช่องกระเป๋าที่เคยว่างมีไอคอนใหม่ อ่านชื่อไอเทมได้ -- จดตัวอักษรเป๊ะ (อ่านไม่ออก = `unreadable`)
- **หลัง relog (คนละบูต ห้ามใช้ภาพเดิม)**: ไอคอนเดิม ชื่อเดิม ช่องเดิม บนภาพนิ่งใหม่
- 🔴 **บันทึกสีของทุกป้ายชื่อในเฟรม** ทุกภาพ (คำสั่ง Panya 2026-08-25) · หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ ·
  ไม่มีป้าย = เขียน `none` ห้ามเว้นว่าง · อ่านจาก full-res เท่านั้น · **จดสีอย่างเดียว ห้ามเดาสาเหตุ** (`RE-067`) ·
  ต่างจาก screenshot เซิร์ฟเวอร์จริง = หนึ่งแถวใน `REAL_SERVER_DIVERGENCE.tsv`
- ❗ **ผลลบมีค่าเท่าผลบวก**: "ของหายหลัง relog" ต้องบันทึกละเอียดเท่ากับ "ของอยู่"

### NO-RESULT (ไม่ใช่ FAIL ไม่ใช่ BLOCKED)
- **รันผิดฉาก**: Port Royal เหลือหุ่นซ้อม `n_ID 916` ที่มี `n_DROPS_*` = 0 ทั้งสามคอลัมน์ ⇒ ฆ่าในเมืองไม่มีของตกเลย
  = `NO-RESULT (ฉากผิด)` · รอบดรอปทั้งหมดอยู่ที่ `Bg0002` เท่านั้น
- **ไม่มีวัตถุให้คลิกเก็บ** (คำถามค้างของ `GT-124` ข้อ (b)) = NO-RESULT ของครึ่ง pickup · ใบนี้ยังเปิด ไม่ FAIL
- `STORE-INSERT-001` ยังไม่ลง main = **ห้ามบูต** (บูตแล้วได้ FAIL ปลอม)

### คำทำนาย (ผิด = ผล ไม่ใช่ความล้มเหลว)
- **P1 [หลัก]** ของอยู่ครบทั้ง `S1`/`S2` และเห็นบนจอทั้งสองบูต ⇒ M5 ปิดวง
- **P2 [หักล้างที่มีค่าที่สุด]** `S1` มีแถว แต่ relog ถูกด่าน 2 ปฏิเสธ ⇒ ต้องมีบรรทัด `BAG_ADMISSION verdict=refused
  reason=<...>` -- `reason` ตัวนั้นคือคำตอบ ⇒ redirect เข้า `bag_admission._classify_against` ไม่ใช่ `store.py`
- **P3** `S1` ไม่มีแถวใหม่เลย ⇒ INSERT ไม่ทำงาน/ไม่ถูกเรียก ⇒ กลับไป `STORE-INSERT-001` ห้ามบูตซ้ำแบบเดา

### nonclaims
1. **ด่าน 2 รับกระเป๋า golden+acquired เป็นเทส "รูปร่าง" ไม่ใช่การพิสูจน์ที่มา** -- แถวที่ถูกแก้มือใน DB ให้ถูกรูป
   ก็ถูกรับเหมือนกัน (`bag_admission` NONCLAIM 1 · COO รับราคานี้ในใบ `20260829_0441` gate-2) ⇒ ใบนี้ไม่พิสูจน์ว่า
   ของในกระเป๋า **มาจากการเก็บจริง** พิสูจน์แค่ว่ามัน **รอด** · ตัวชี้ที่มาจริงคือ `next_item_identity` ที่เดินแล้ว
2. **รอบที่เปิดใบนี้ (R222) ไม่ได้พิสูจน์วงรอบอะไรเลย** -- `store.py` ยังไม่ INSERT ไม่เดินตัวนับ ใบนี้จึงเป็นแบบพิมพ์
   ของการทดสอบวันข้างหน้า ไม่ใช่รายงานผล
3. ไม่พิสูจน์ว่า **คลิกเก็บได้** (นั่นคือ `GT-124` + call site ที่ยังไม่มี) และไม่พิสูจน์เรื่องดรอปหลายชิ้น (`GT-132`)
4. ไม่พิสูจน์อะไรเกี่ยวกับ **สาเหตุของสีป้ายชื่อ** (`RE-067` เป็นเจ้าของคำถามนั้นคนเดียว)
5. ตัวละครเดียว บูตสองครั้ง ของหนึ่งชิ้น -- ห้าม generalize ไปยัง stack/merge/หลายชิ้น/หลายตัวละคร
6. ใบนี้ไม่แตะ `is_unmoved_baseline` และไม่พูดถึงตระกูล HYP-PF-008/010/017/018 แม้แต่ข้อเดียว

### result: (ผู้เทสกรอก)


---

## SKIPPINS-FRAGMENTS-001 [CHIEF-WORK · ไม่ใช่ใบเทส ไม่ต้องเปิดเกม]: แตก `docs/PYTEST_SKIP_PINS.json` เป็นแฟ้มย่อยรายโมดูล เพื่อให้สองสายเติม skip พร้อมกันได้  [OPEN · เจ้าของ: chief (สาย E)]

> เปิดโดย chief R224 ตาม `CHIEF-DECISION 20260829_0710` ซึ่งตอบบรรทัดถึง chief ใน `20260829_0638_LANE-B-STATUS-pr235-*`

**อาการที่วัดแล้ว:** ไฟล์พินเดียว 920 บรรทัด ทุกสายเติม entry ของตัวเองที่ท้ายบล็อกเดียวกัน ⇒ PR ที่ **เกตเขียวแล้ว** ถูก `merge-claude-pr` ปิดเพราะ `mergeable=false` มาแล้ว **สองครั้ง** — `pirate-force-server#231` (สาย A) และ `#235` (สาย B) · ทั้งสองครั้งเป็นการเพิ่มล้วนทั้งคู่ ไม่มีฝ่ายใดผิด

**สิ่งที่ต้องทำ:**
1. `docs/pytest_skip_pins.d/<ชื่อโมดูลเทส>.json` หนึ่งไฟล์ต่อหนึ่งโมดูลที่มี skip — เจ้าของไฟล์คือสายที่เป็นเจ้าของเทสนั้น
2. ไฟล์แม่คงไว้เฉพาะ `version` `why` `preconditions` `windows_gate_excluded_modules`
3. `tools/pf_pytest_precondition_census.py` อ่านไฟล์แม่ **บวก** ทุกไฟล์ในไดเรกทอรี · entry ซ้ำชื่อโมดูลข้ามไฟล์ = แดงโดยระบุชื่อ (ไม่ใช่ทับกันเงียบ)
4. ย้ายของเดิมด้วยสคริปต์ ไม่ใช่มือ · จำนวน skip รวมก่อน/หลังย้ายต้องเท่ากันเป๊ะ และพิสูจน์ด้วย `census --run` ทั้งสองฝั่ง

**เกณฑ์ปิดตั๋ว (wire/DB ล้วน ไม่ต้องเปิดเกม):** `census --run` PASS บนคลาวด์ · สองสายแก้ไฟล์ย่อยคนละไฟล์ในรอบเดียวกันแล้ว rebase ผ่านโดยไม่มี conflict (พิสูจน์ด้วยการทดลอง merge จริงบน branch ทดสอบ) · พิน 48 ไม่เปลี่ยนค่า

**nonclaim:** ตั๋วนี้เปลี่ยน **ที่เก็บ** ของพิน ไม่เปลี่ยน **เกณฑ์** ใด ๆ · ไม่ปลดพิน 48 · ยังไม่วัดผลกระทบต่อเวลารัน census

---

## GT-144 TEN-MARKER-SCENES-FIRST-EYES-001 [attended, in-game]: สิบฉากที่เพิ่งได้จุดมาถึงจากตาราง `MARKER` -- ล็อกอินเข้าไปแล้ว **ยืนบนพื้นที่ยืนได้** หรือโผล่ในหิน  [BLOCKED -- 🔴 **ประตูปิด อย่าเพิ่งหยิบ** · เปิดโดย LANE-A รอบ `ga91m5`]

> **BLOCKED ด้วยเงื่อนไขเดียว**: รอบ `ga91m5` ลงสิบแถวนี้ในทะเบียนครบ (พิกัด · แถวตาราง · digest)
> **แต่ทั้งสิบเป็น `login_entry_allowed: false`** ⇒ `stageable_scene_ids()` ยังเป็น `(1, 2, 278, 997)`
> · `/warp 3` ถูกปฏิเสธตอนเขียน ⇒ ผู้เทสเข้าไม่ได้วันนี้
> **ปลดล็อกเมื่อ** COO เคาะใบ `notes_to_chief/20260829_0915_LANE-A-ASK-COO-ten-doors-shut-and-the-gate-that-would-open-them.md`
> (ขอเกตหนึ่งตัวที่ทุกเส้นทางประกอบ actor ต้องผ่านก่อนส่งเฟรมเข้าฉาก N) แล้วสาย A ลบคีย์เดียวต่อแถว
> ใบนี้พร้อมรันทันที ไม่ต้องเขียนใหม่
> เหตุผลที่ปิด (วัดโดย `pf-adversary`) อยู่ที่ `scenarios/world_scene_registry_001.json`
> คีย์ `arrival_point_rule.why_the_ten_doors_are_shut` -- ย่อ: กิ่ง dispatcher เก่า `v141:4292`
> ยิง actor bg0001 สามตัวฮาร์ดโค้ด `scene_id=1` เข้าฉากที่ผู้เล่นยืน **โดยไม่เช็คฉาก** บนบูตที่ไม่ไร้แฟล็กเป๊ะ ๆ

> 🆕 **อัปเดต LANE-A รอบ `bq4mst` 2026-08-31T06:4x+07:00 -- เกตปลดแล้ว (R236) แต่ใบนี้ยัง BLOCKED สำหรับ 9 ฉาก
> ที่เหลือ เพราะยังไม่มีตัวประกอบ ไม่ใช่เพราะประตูปิด:** เกตที่ใบนี้รอ (`scenarios/world_scene_registry_001.json`
> `arrival_point_rule.why_the_ten_doors_are_shut`) ลง main แล้ว (`scene_admission_gate.py`, R236, ยืนยันโดย
> `COO-DECISION 20260830_1351`) **แต่ฉาก 4 (Slave Market Island) เพียงฉากเดียวเปิดจริงรอบนี้** เพราะเป็นฉากเดียว
> ในสิบที่มีตัวประกอบ (`world_population_bg0004.py`) พร้อมแล้ว (`COO-DECISION 20260830_1441`) --
> **ย้ายฉาก 4 ออกจากขอบเขตใบนี้ ไปที่ `GT-165` ใบใหม่แยกต่างหาก** (มีเกณฑ์ของตัวเอง เพราะฉากนี้ไม่มี faction bit
> เลยต่างจากที่ใบนี้เขียนไว้สำหรับสิบฉากรวม) · **อีกเก้าฉาก (3,5,6,7,8,9,10,11,130) ยังเป็น `login_entry_allowed:
> false` เหมือนเดิมทุกตัวอักษร ยังไม่มีตัวประกอบ ยัง BLOCKED จริง ไม่ใช่แค่ประตูปิด** -- `stageable_scene_ids()`
> วันนี้คือ `(1, 2, 4, 14, 278, 997)`

> 🆕 **อัปเดตที่สอง LANE-A รอบ `3t75jw` 2026-08-31T09:3x+07:00 -- ฉาก 10 (Deep Sea Temple floor 1) เปิดเป็น
> ประตูที่สองด้วย, ย้ายออกจากขอบเขตใบนี้เช่นกัน:** ตัวประกอบ (`world_population_bg0010.py`) พร้อมแล้ว
> (`COO-DECISION 20260830_1441`, คิวเดียวกับฉาก 4) **ย้ายฉาก 10 ไปที่ `GT-166` ใบใหม่แยกต่างหาก** (เกณฑ์
> ของตัวเอง สองคำถามแยก: มี actor ไหม / พื้นยืนได้ไหม -- ฉากนี้คือหนึ่งในสองแถวที่ตารางด้านล่างเตือนไว้ล่วงหน้า
> ว่าเสี่ยงที่สุด จึงไม่รวมกับใบนี้ที่เป็นคำถามเดียว) · **อีกแปดฉาก (3,5,6,7,8,9,11,130) ยังเป็น
> `login_entry_allowed: false` เหมือนเดิมทุกตัวอักษร ยังไม่มีตัวประกอบ ยัง BLOCKED จริง** --
> `stageable_scene_ids()` วันนี้คือ `(1, 2, 4, 10, 14, 278, 997)` · [LANE-A ASSUMPTION - AWAITING COO
> CONFIRMATION] ว่าการเปิดฉาก 10 ทั้งที่ทะเบียนตีตราความเสี่ยงสูงกว่าฉาก 4 นั้นถูกต้อง -- ถามไว้ใน
> `notes_to_chief/20260831_0932_LANE-A-ASK-COO-scene10-landing-geometry-elevated-risk.md`

### objective (claim เดียว)
ฉากที่ได้จุดมาถึงจากกฎ 1 (`COO-DECISION 20260829_0542`) เมื่อล็อกอินเข้าไปจริง
**ตัวละครยืนบนพื้นที่ยืนได้ของแมพที่ถูกต้อง** ใช่หรือไม่ (ไม่ใช่ในหิน ใต้พื้น ในลาวา หรือลอยแล้วร่วง)
ชั้นหลักฐานวันนี้คือ `authored` = คนทำแมพเขียนพิกัดไว้ **ยังไม่เคยมีไคลเอนต์ยืนบนจุดใดใน 10 จุดนี้** ใบนี้คือตาคู่แรก

### db / server args
`state\run_gt144.sqlite3` -- สำเนาเสมอ ห้ามเปิด canonical · จด `CANON_SHA` ก่อน/หลัง ต้องเท่ากัน
`py -3 -u -m pirateforce_foundation.app --db state\run_gt144.sqlite3` · client `-SecondPasswordMode bypass`
🔴 **ห้ามมีแฟล็กฝั่งเซิร์ฟเวอร์ใด ๆ** (`--*-scenario`, `--world-census-actors`, `--second-password-mode`):
แฟล็กพวกนี้ทำให้กิ่ง v141 เก่ายิง actor ฉาก 1 เข้ามาในฉากที่เทส ⇒ **ผลอ่านไม่ได้ทั้งรอบ**

### สิบฉาก และลำดับที่แนะนำ
| ลำดับ | ฉาก | model | ชื่อ | marker | x | y | z |
|---|---|---|---|---|---|---|---|
| 1 | 7 | `Bg0007` | Voodoo Island | 7 | -23266 | 7709 | 5220 |
| 2 | 8 | `Bg0008` | Silver Harbour | 8 | 19440 | 23997 | 560 |
| 3 | 3 | `BG0003` | Spice Paradise Island | 3 | -21215 | 16907 | -830 |
| 4 | 4 | `BG0004` | Slave Market Island | 4 | -19076 | 17634 | 1440 |
| 5 | 5 | `BG0005` | Evil Port | 5 | 13025 | 23379 | -740 |
| 6 | 6 | `Bg0006` | Ocean Walled City | 6 | -9848 | 24151 | 375 |
| 7 | 9 | `Bg0009` | Death City Sea | 9 | 2129 | 20907 | 240 |
| 8 | 130 | `Bg4001` | Navy Training Camp | **1000** | -24482 | 13364 | -990 |
| 9 | 11 | `Bg0011` | Deep Sea Temple floor 2 | 11 | 15179 | 22807 | 380 |
| 10 | 10 | `Bg0010` | Deep Sea Temple floor 1 | 10 | 15740 | 25461 | 465 |

พิกัดจาก `CONSTDATA_TH__MARKER.tsv` อ่านแบบ two's-complement int32
**ลำดับนี้วัดมา ไม่ใช่ความรู้สึก**: 7 กับ 8 ก่อน เพราะจุด marker ห่างจากจุดวาง NPC ของคนทำแมพแค่ **10.8**
และ **8.8** หน่วย · **10 กับ 11 ท้ายสุด** เพราะเป็นสองฉากเดียวที่ `n_CANGLIDE = 0` และ `n_LIMIT_HEIGHT = 0`
(ภายในอาคาร ไม่ใช่เกาะเปิด) ระยะ **5174.7** และ **1107.8** และพื้นจุดวางต่ำถึง z = **-4532.9 / -4592.9**
ขณะที่ marker อยู่ z = 465 / 380 ⇒ **ถ้าจะโผล่ในหินหรือลอยกลางอากาศ สองฉากนี้คือที่ที่มันจะเกิด**

**ทำ "อย่างน้อยหนึ่งฉาก" แล้วรายงานได้เลย ไม่ต้องครบสิบ** ฉากที่ไม่ได้ทำเขียนว่า "ไม่ได้ทำ" ไม่ใช่ PARTIAL

### ขั้นตอน
ของมาตรฐานทุกข้อตาม `ATTENDED_SESSION_RUNBOOK.md` · กลไก `/warp` + logout/login เป็นของ **`GT-141`**
ใบนี้ขี่มัน ไม่เทสซ้ำ (อ่านหัวใบนั้นก่อน: คลิกกล่องแชทให้โฟกัสก่อนพิมพ์ · `/warp` คือการสตางค์ฉากล็อกอิน
**ไม่ใช่ warp** ไม่มีไบต์วิ่งตอนพิมพ์ · ต้อง `/warp` + relog ใหม่ทุกฉาก)
ต่อฉาก: โหลดเสร็จ → **ภาพนิ่งความละเอียดเต็มทันที** + ภาพมินิแมพ/ชื่อฉาก + จดพิกัดที่ UI แสดง →
พิสูจน์ว่าไคลเอนต์ยังไม่ตายด้วย **right-click-drag เท่านั้น** (หมุนกล้อง ไม่มีไบต์ออกสาย ·
🔴 ห้ามใช้ `Q`/`E`/`WASD` เป็นตัววัด มันขยับตัวละครและยิง `TargetPosVital`) → เดินสำรวจได้**หลัง**ถ่ายภาพแล้ว
→ เกรดด้วยคำเดียว: **PASS** / **STANDS-BUT-WRONG-PLACE** (ยืนได้แต่ผิดที่ เช่นกลางทะเล) /
**INSIDE-GEOMETRY** (ในหิน ใต้พื้น ในลาวา ร่วงไม่หยุด) / **DID-NOT-LOAD** (ค้าง แครช เด้งกลับ)
**กฎสีป้ายชื่อ (`Panya` 2026-08-25) บังคับ**: หนึ่งบรรทัดต่อหนึ่งป้ายในเฟรม รวมป้ายตัวเอง ไม่มีป้ายเขียน "none"
อ่านสีจากภาพนิ่งความละเอียดเต็มเท่านั้น · **จดสีอย่างเดียว ห้ามเดาสาเหตุ** (นั่นคือใบ `RE-067`)

### 🔴 กฎหยุด (หัวใจของใบนี้ - คำ COO ในใบ `20260829_0542`)
โผล่ **ในหิน ในลาวา หรือใต้พื้น** = **กฎ 1 ตกทันที** สาย A ย้อนเองโดยไม่ต้องถาม COO ซ้ำ
แปลว่า **ตาราง `MARKER` เลิกเป็นแหล่งจุดเกิดโดยปริยายของโปรเจกต์**
ผลลบมีค่าเท่าผลบวก กรอกง่ายเท่ากัน: `INSIDE-GEOMETRY` + ภาพนิ่ง + พิกัดที่ UI แสดง แค่นั้นพอ
**หนึ่งฉากที่ INSIDE-GEOMETRY พอทำให้กฎตก ไม่ต้องรอครบสิบ**

### pass criteria (สองชั้น แยกกัน ห้ามใช้ชั้นหนึ่งแทนอีกชั้น)
- **wire/DB:** ต่อฉาก ก่อนวางตัวละครต้องมีบรรทัด (คัดลอกตัวอักษร ไม่ใช่ถ่ายรูป)
  `WORLD_SCENE scene_id=<n> seq=0 model=<Bg....> name=<...> spawn=(x,y,z) sent_before=NO population=none save=1 marker=<n_MARKER> return_ticket=not_needed`
  + อีเวนต์ `world_census_skipped_scene_<n>_not_home` (พิสูจน์ว่าสำมะโน Port Royal ไม่ตามเข้าไป)
  + **ไม่มีแถว `character_positions` ถาวรของการเยือน** + ล็อกอินครั้งถัดไปกลับ Port Royal เอง
- **client-observable:** แมพโหลดจริงและ **เป็นเกาะตามชื่อ** (มินิแมพ/ชื่อฉากเปลี่ยนจาก Port Royal) ·
  ตัวละคร **ยืนบนพื้น** · ไคลเอนต์ไม่ค้าง ไม่แครช ไม่เด้งกลับ + `OBSERVER_CONFIRMED: <เวลา +07:00>`
- ขาดชั้นใดชั้นหนึ่ง = PARTIAL ไม่ใช่ PASS

### คำทำนาย (ผิด = ผล ไม่ใช่ความล้มเหลว)
P1 แมพขึ้นและ **ว่างเปล่า** - คือของที่คาด ไม่ใช่ข้อบกพร่อง · P2 ฉาก 7/8 ยืนได้ ฉาก 10/11 เสี่ยงสุด
· P3 ไม่มีบรรทัด `PLAYER_FACTION` เลยทุกฉาก (D3 ยังเปิด) และไม่มีอะไรให้มันทำร้ายเพราะไม่มี NPC

### nonclaims
1. ไม่อ้างว่าสิบฉากนี้เรนเดอร์ได้ - ยังไม่เคยมีฉากใดถูกส่งให้ไคลเอนต์
2. ไม่อ้างว่าจุด marker คือที่ที่เกมต้นฉบับวางผู้เล่นที่มาถึง - ที่วัดได้คือไคลเอนต์เคย**รับ**พิกัด `MARKER` มาแล้วสองครั้ง (`MARKER[1]` V137, `MARKER[2]` SCENE-001)
3. สิบฉากนี้ไม่มีสำมะโนบนบูตไร้แฟล็ก - เกาะร้างคือผลที่ถูกต้อง
4. **D3 ยังเปิด**: `player_wire` ปฏิเสธ faction-1 ทุกฉากนอก (1, 2) ⇒ ไม่มีเฟรม `PLAYER_FACTION` · ไม่มี NPC จึงไม่มีผล -- **แต่ถ้าเห็น NPC ในฉากพวกนี้ คือของค้นพบ รายงานทันที**
5. **ฉาก 14 ไม่อยู่ในใบนี้โดยตั้งใจ** - ประตูยังปิด เจ้าของคือ `GT-134`
6. `return_ticket=not_needed` **ไม่ได้แปลว่ากลับออกมาได้** - มาจาก `n_MARKER != 0` ล้วน ๆ และ marker คือจุด**ขาเข้า** ไม่พูดถึงทางออก

**ผู้เปิดใบ: LANE-A (WORLD) รอบ `ga91m5`** -- ผลกลับมาที่สาย A บริโภค

### result (ผู้เทสกรอก - หนึ่งบรรทัดต่อฉาก)
```
ฉาก 7 / 8 / 3 / 4 / 5 / 6 / 9 / 130 / 11 / 10 :
   PASS | STANDS-BUT-WRONG-PLACE | INSIDE-GEOMETRY | DID-NOT-LOAD | ไม่ได้ทำ
CANON_SHA ก่อน/หลัง :
OBSERVER_CONFIRMED  :
```

---

## GT-145 CONSOLE-ENCODING-MEASURE-001 [STATIC-ON-BRIDGE -- วัดบนสะพานตอนเซิร์ฟเวอร์รันจริง · ไม่บูตไคลเอนต์ ไม่ล็อกอิน ไม่มีตัวละคร · ~15 นาที]: คอนโซลของเครื่องเจ้าของเป็น encoding อะไร -- พิมพ์สี่ค... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-146 PICKUP-CLICK-OPCODE-CAPTURE-001 [attended, in-game]: คลิกซ้ายลงบน element ของตกที่เซิร์ฟเวอร์เราส่งเอง แล้ว **ไคลเอนต์ยิงเฟรมอะไรออกสาย** -- ใบ capture ที่ปลด `RE-125`/`GT-124`/M5  [⚪ **CANCELLED - covered by R303 attended capture 20260902_1755 (46 inbound 0x4543 frames, 2 completed takes), confirmed R306** — ปิดโดย chief (LANE-E) รอบ `m8wtlr`/R356 2026-09-05T17:0x+07:00 ตาม `COO-DECISION 20260905_0249` ข้อ 1 (ทวงเป็นครั้งที่สองโดย `COO-DECISION 20260905_1649` หลังค้าง 14 ชม.) · **คำถามของใบนี้ถูกตอบบนไวร์ไปแล้ว**: R303 จับเฟรมขาเข้า `0x4543` 46 เฟรมจากการคลิกจริง ยืนยันซ้ำ R306 · หลักฐานที่วัดบนไวร์ชนะคำสั่งที่เขียนจากชื่อใบ (`COO 0249`) · 🔴 **คำถามที่ยังเปิดอยู่ในใบนี้ไม่ได้ปิดไปกับมัน** — `REEMISSION_REDRAWS_THE_LABEL` ย้ายไปอยู่ใต้ `GT-223`/`RE-208` ของ LANE-B ในรอบเดียวกัน ตาม `COO 0249` ข้อ 1 ประโยคท้าย · ~~🔴 BLOCKED - until P-2 closes (NOW) — เงื่อนไขเดียว ไม่มีเงื่อนไขอื่น~~ · ตั้งโดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 ตาม `COO-DECISION 20260904_2349` ข้อ 5 · ที่มา: `NOW.md` หัวข้อ "ห้ามทำจนกว่า P-2 จะปิด" ระบุชื่อใบนี้ตรง ๆ · เงื่อนไข `GT-188` checkpoint 2 **ตัดทิ้งแล้ว** (`GT-188`/`GT-188cp1` ยกเลิกตาม `PANYA-DECISION 20260903_1934` · `COO 20260904_1648`) · เปิดโดย LANE-B รอบ `uq2lxw2` · แก้ขั้นตอนตาม `PANYA-ORDER 20260830_1450` ที่รอบ `xt0g9c` · archived โดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)]

---

## GT-147 COUNTER-RESYNC-RECOVERY-TOOL-001 [attended · in-game เฉพาะเฟสตรวจรับ · **เจ้าของรันเครื่องมือเอง**]: DB ที่ตัวนับ `next_item_identity` ล้าหลังแถวจริงในกระเป๋า — หลังรันเครื่องมือกู้ (นอก production path · diff → หยุดถาม → ค่อยเขียน) **ตัวละครที่ด่าน 2 ล็อกออกกลับเข้าโลกได้จริงไหม**  [BLOCKED -- **BLOCKED-ON-TOOL** · เครื่องมือยังไม่ถูกสร้าง · สล็อตสร้าง = คิวปกติของ chief **หลังงาน M5** ตาม `COO-DECISION 20260829_1344` · **ไม่ด่วน** — เคสจริงยังไม่เคยเกิด กติกา `AGENTS.md` §7 (R227) กันเหตุได้เกือบทั้งหมด]

> NUMBERING: grep ตามสูตรข้อ ② หัวไฟล์ (2026-08-29T14:xx+07:00) — เลขสูงสุดที่ใช้ไป = 146 (`GT-146` · `RE-` สูงสุด = 139) ⇒ ใบนี้ = `GT-147` · ตัวนับเดียวร่วม `CLIENT_RE_QUEUE.md`
> ที่มาสองบรรทัด: pf-adversary R226 ชี้เคส [เสนอ — ยังไม่เกิดจริง แต่สร้างได้]: restore บางตาราง ⇒ ตัวนับล้าหลังแถว ⇒ ด่าน 2 (`issued_through` บังคับใน `may_enter_world` ตั้งแต่ `#257`) ปฏิเสธ `acquired_identity_not_issued` ตลอดไป — ไม่มีอะไร re-sync ขึ้นโดยเจตนา (ตัวนับที่ derive จากกระเป๋าเลิกเป็นหลักฐาน) · chief ASK-COO `20260829_1332` → COO เคาะทาง 3: กติกาลง `AGENTS.md` §7 แล้ว (R227) · เครื่องมือกู้ = ใบนี้
> 🔴 **เงื่อนไขแข็งจาก COO — เป็นส่วนหนึ่งของ claim ไม่ใช่คำแนะนำ:** (1) **attended-only เจ้าของรันเอง** (2) **เซิร์ฟเวอร์ปิดสนิทตลอดเวลาที่เครื่องมือรัน** (3) เครื่องมือ**พิมพ์ diff ของทุกอย่างที่จะแก้ แล้วหยุดถามก่อนเขียนแม้แต่ไบต์เดียว** (4) อยู่**นอก production path** — สคริปต์แยก (เช่นใต้ `tools/`) ห้ามถูก import โดย app/runtime
> 🔴 ใบเดียวกันครอบงานแก้ **ข้อความ `PermissionError` ที่วันนี้ชี้ `HYP-PF-008` ผิดเรื่อง** — ผู้ร้ายจริงคือด่านตัวนับ ไม่ใช่ hypothesis นั้น (โทเคน stderr `BAG_ADMISSION ... reason=...` ชี้ถูกอยู่แล้ว) — COO สั่งรวมใบเดียว จึงตรวจรับในเฟส A ของ run เดียวกัน ไม่เปิด claim ที่สอง

- objective: (ข้ออ้างเดียว) บนสำเนา DB ที่**ตั้งใจ**ทำ desync (ตัวนับต่ำกว่า `MAX(identity)` ของแถวจริง หนึ่งตัวละคร) — หลังเจ้าของรันเครื่องมือกู้ครบวง diff→ยืนยัน→เขียน **ด่าน 2 ยอมรับตัวละครตัวนั้นอีกครั้ง และตัวนับตรง max identity จริงของ store**
- db: สำเนา throwaway `state\run_gt147.sqlite3` · สร้าง fixture ด้วยการลด `character_backpacks.next_item_identity` ของตัวละครทดสอบให้ต่ำกว่า `MAX(identity)` ใน `character_backpack_items` (จดค่าก่อน-หลัง) — การแก้มือครั้งนี้คือ**การสร้าง fixture บนสำเนาทิ้ง** ไม่ขัดข้อห้ามใน `AGENTS.md` §7 (ข้อห้ามนั้นคือห้าม*กู้ของจริง*ด้วยมือ) · 🔴 ห้ามเปิด canonical `state\pirateforce.sqlite3` · sha256 canonical ก่อน-หลังทั้งใบต้องเท่ากัน
- server args: `py -3 -u -m pirateforce_foundation.app --db state\run_gt147.sqlite3` · ไม่มีแฟล็ก `--*-scenario` ใด ๆ · คำสั่งเรียกเครื่องมือ: **เติมชื่อ/แฟล็กจริงตอนเครื่องมือลง main — ห้ามเดา ห้ามรันใบนี้ก่อนบรรทัดนี้ถูกเติม** (ปลด BLOCKED-ON-TOOL = แก้บรรทัดนี้ + สถานะ)
- steps:
    0. มาตรฐานบ้าน: LOCK · sha canonical · copy DB · สร้าง fixture · จดสองค่า (`next_item_identity` · `MAX(identity)`)
    1. **เฟส A — พิสูจน์ล็อกเอาต์ก่อนกู้:** บูตเซิร์ฟเวอร์ (server ก่อน client เสมอ) → เข้าเกม เลือกตัวละครทดสอบ → คาดว่า**เข้าโลกไม่ได้** (ค้าง "connecting"/ไม่เข้าแมพ — คำทำนาย ผิด = ผล) · เก็บ console `.err` ทั้งไฟล์: บรรทัด `BAG_ADMISSION` + ข้อความ `PermissionError` เต็มบรรทัด (คัดดิบ ห้ามตีความ) · ปิดไคลเอนต์ → **ปิดเซิร์ฟเวอร์** (กฎบ้าน: ฆ่าไคลเอนต์แล้วต้อง restart เซิร์ฟเวอร์ก่อนบูตหน้า)
    2. **เฟส B — รันเครื่องมือ ขณะเซิร์ฟเวอร์ปิด:** ยืนยันไม่มี LISTENING ที่ `10188`/`10189` (`netstat -ano | findstr "10188 10189"` — คัดลอกผลดิบ) · รันเครื่องมือ**ครั้งที่ 1 แล้วตอบปฏิเสธ** → sha256 สำเนาต้อง**ไม่เปลี่ยน** (พิสูจน์ว่า "หยุดถาม" กันการเขียนจริง ไม่ใช่แค่พิมพ์คำถาม) · รัน**ครั้งที่ 2** อ่าน diff ทั้งหมด (คัดดิบลง result) → ตอบยืนยัน → เครื่องมือเขียน
    3. ตรวจสำเนา: ตัวนับ vs `MAX(identity)` · `PRAGMA integrity_check`
    4. **เฟส C — เข้าโลกจริง:** บูตเซิร์ฟเวอร์ใหม่บนสำเนาเดิม → เจ้าของล็อกอินตัวละครเดิมเข้าโลก · **S0** full-res เมื่อยืนในแมพ · NO-CRASH ด้วย**คลิกขวาค้างลาก** (🔴 ห้าม `Q`/`E`/`W/A/S/D` เป็น liveness — เปลี่ยน facing = ยิง `TargetPosVital`; คลิกขวาลากหมุนแค่กล้อง ไม่มีไบต์ออกสาย) · ออกเกม → ปิดเซิร์ฟเวอร์ → teardown เสมอ · sha canonical ซ้ำ · ห้าม commit เอง
- pass criteria: 🔴 สองชั้นแยกกัน ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น
    wire/DB (headless ไม่ต้องมีคนหน้าจอ):
      (ก) เฟส A: มีโทเคน `BAG_ADMISSION ... reason=acquired_identity_not_issued` และ**ไม่มี**แถว `sessions` ที่ `selected_character_id` = ตัวละครทดสอบ
      (ข) เฟส A: ข้อความ `PermissionError` **ไม่มีสตริง `HYP-PF-008`** และเรียกชื่อด่านตัวนับ/`issued_through` — ตรวจรับงานแก้ข้อความในใบเดียวกัน
      (ค) เฟส B: ตอบปฏิเสธ ⇒ sha สำเนาไม่เปลี่ยน · ตอบยืนยัน ⇒ diff ที่พิมพ์ครอบ**ทุก**ค่าที่เปลี่ยนจริง (เทียบ SELECT ก่อน-หลัง) และไม่มีตาราง/แถว/คอลัมน์นอก diff ขยับ
      (ง) หลังกู้: ตัวนับ = max identity จริงของ store (ตามนิยาม `issued_through`) · `integrity_check`=ok · เฟส C มีแถว `sessions` ใหม่ select ตัวละครนี้ ไม่มีโทเคนปฏิเสธซ้ำ · sha canonical เท่าเดิมก่อน-หลัง
      ชั้นนี้ตอบไม่ได้: เจ้าของเห็นตัวละครยืนในโลกไหม
    client-observable (ต้องมีตาคน):
      เจ้าของเห็นตัวละครตัวเดิม**เข้าแมพ ยืนบนพื้น HUD ขึ้นปกติ** ไม่ค้าง "connecting" · S0 full-res + sha256 · **จดสีป้ายชื่อทุกป้ายในภาพ** หนึ่งบรรทัดต่อป้าย ไม่มีป้ายเขียน `none` อ่านจาก full-res เท่านั้น · **จดสีอย่างเดียว ห้ามเดาสาเหตุ** (`RE-067`) · NO-CRASH/CRASH · 🔴 G-OBS: จดหมายผลต้องมีบรรทัด `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ไม่มี = chief ไม่บริโภค
      ชั้นนี้ตอบไม่ได้: ตัวนับตรงจริงไหม เครื่องมือเขียนอะไร diff ครบไหม
- nonclaims:
    1. ไม่พิสูจน์ว่า auto-resync ปลอดภัย — ต้องห้ามโดยนิยาม (COO 1344): เครื่องมือนี้เป็นทางกู้ที่**ไม่อัตโนมัติโดยตั้งใจ** ใบนี้ห้ามถูกอ้างเพื่อดันให้มันไปอยู่ใน production path
    2. ไม่พิสูจน์ทรง desync อื่น (ตัวนับนำหน้าแถว · หลายตัวละคร · ตารางอื่นนอกคู่ backpack) — เจอเมื่อไรเปิดใบใหม่
    3. ไม่แตะ/ไม่วัดกติกา "restore ทั้ง DB เท่านั้น" (`AGENTS.md` §7 บังคับอยู่แล้ว ใบนี้เป็นทางกู้เมื่อกันไม่ทัน) · ไม่ตัดสินสาเหตุสีป้ายชื่อ (`RE-067`)
    4. **ผลลบมีค่าเท่าผลบวก:** กู้แล้วด่าน 2 ยังปฏิเสธ ⇒ finding เรื่องนิยาม interval ของด่าน (floor `golden_highest` / เพดาน inclusive — ดู R226 §①) ⇒ redirect กลับสเปกเครื่องมือ + คำถาม static เรื่อง interval **ไม่ใช่ความล้มเหลวของผู้เทส ห้ามปิดใบเป็น FAIL เฉย ๆ** · เครื่องมือยังไม่มี/รันไม่ขึ้น = ใบคง BLOCKED ไม่ใช่ FAIL
- links: `notes_to_chief/20260829_1332_CHIEF-ASK-COO-counter-behind-store-locks-a-character-out-forever.md` · `notes_to_chief/20260829_1344_COO-DECISION-restore-rule-now-recovery-tool-as-a-ticket.md` · `AGENTS.md` §7 (กติกา R227) · `rounds/R226_hsz32u_gate2-counter-route1-wired-plus-gt146-capture-ticket.md` §① · ด่าน 2: `pirate-force-server#257` (`bag_admission.py` · `session.py` · `lifecycle.backpack_issued_through`)

### result (ผู้เทสกรอก)
```
ค่า counter ก่อน/หลัง · MAX(identity) · บรรทัด BAG_ADMISSION + PermissionError คัดดิบ · diff เต็มของเครื่องมือ ·
sha สำเนาหลังตอบปฏิเสธ/หลังเขียน · sha canonical ก่อน-หลัง · integrity_check · S0 + สีป้ายทุกป้าย · NO-CRASH/CRASH · OBSERVER_CONFIRMED

## GT-148 SCENE17-STOWAWAY-ACTORS-FIRST-EYES-001 [attended, in-game]: ออกทะเลกับ Columbus แล้ว **ไคลเอนต์ยังโชว์ actor ของ Port Royal ที่ถูกส่งไปตอนล็อกอินอยู่หรือไม่**  [~~PENDING · เปิดโดย LANE-A (W... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-149 DROP-LIFETIME-MEASURE-001 [attended, in-game · แนบไปกับรอบถ่ายวิดีโอของเจ้าของ · ~10 นาที]: ฆ่ามอนแล้ว **จงใจไม่เก็บ** -- ของบนพื้นอยู่ได้กี... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## GT-151 PORT-ROYAL-SEVEN-HOLES-EYES-001 [attended, in-game]: 108 จาก 115 ขึ้นจอ -- **เจ็ดรูที่ผู้เล่นเดินไปเจอ ใช่เจ็ดจุดที่คอนโซลเรียกชื่อหรือไม่**... -- archived 20260907 (CANCELLED by owner LANE-A round `tsdl0w` 2026-09-07T04:26+07:00; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md`)

---

## 🚀 `PROMOTE-153` CHAT-ECHO-ON-A-DEFAULT-BOOT-001  [CHIEF-WORK · ไม่ใช่ใบเทส]

**สถานะ:** 🟢 OPEN — เจ้าของ: chief (สาย E)
**ที่มา:** `PANYA-DIRECTIVE 20260829_2222` ข้อ 1-4 + ADDENDUM `20260829_2233` · พารามิเตอร์จาก `COO-DECISION 20260829_2246` ("เคสแรก: chat echo เข้าบูตปกติ = หัวคิว promotion · chief เปิดใบ PROMOTE ใบแรกให้มันในรอบถัดไปของ chief")
**ใบแรกของท่อ promotion** — ใบนี้เป็นตัววัดว่าท่อ 1→7 ของ directive ทำงานจริง ไม่ใช่พิธีกรรม

### คำถามที่ใบนี้ปิด
ผู้เล่นพิมพ์แชทบนบูตปกติ **ไร้แฟล็ก** แล้วเห็นข้อความของตัวเองบนจอไหม

### เหตุที่วันนี้ยังไม่เห็น [วัดแล้ว รอบ k882hm บน main]
เส้นทาง echo มีอยู่จริงและถูกพิสูจน์ถึงชั้น wire แล้ว (`GT-009`/`GT-012` 18 ส.ค. — `[ทั่วไป] Arena01: PFCHATPROBE1` เรนเดอร์จริง) แต่โค้ดที่ประกอบ echo อยู่ในเลน hypothesis สองเลนที่ **ปิดตายบนบูตปกติทั้งคู่**:
- `src/pirateforce_foundation/chat_input_hypothesis.py:207` และ `:282` — `"production_allowed": False`
- `src/pirateforce_foundation/channel_message_hypothesis.py:636` และ `:744` — `"production_allowed": False` (docstring `:109` ประกาศเองว่า "There is no production path to any of this")
ทั้งสองเลนเข้าถึงได้ต่อเมื่อส่ง `--*-scenario` เท่านั้น ⇒ บูตปกติสาขา dispatch ไม่มีอยู่ ⇒ แชทใบ้ ตรงกับหลักฐานสดของเจ้าของ (เฟรมแชท "1" ถึง server 2026-08-29 20:00:18 ไม่มี echo กลับ)

### สิ่งที่ต้องทำ (chief)
1. **ก่อนอื่น: directive ข้อ 1** — แยกสวิตช์ "เลนทำงาน" ออกจาก "เลนกีดกันเลนอื่น" (วันนี้บูลีน `production_allowed` ตัวเดียวทำสองหน้าที่ = ตัวอุดทุก promotion) เส้นตาย **30 ส.ค. 21:00** ตาม COO 2246
2. เดินสายเส้นทาง echo ที่แคบที่สุดที่ผู้เล่นแตะได้จริงบนบูตปกติ: รับเฟรมแชท `0xAC52` ascii → ประกอบ echo → ส่งกลับ **โดยไม่ต้องมีแฟล็ก** · ขอบเขตของใบนี้คือ **LocalTalk ช่องเดียว** (สี่ช่องที่เหลือของ `channel_message_hypothesis` ไม่อยู่ในใบนี้ — ยังไม่มีใครพิสูจน์ว่าไคลเอนต์วาดมัน)
3. nonclaim ที่ต้องติดไปกับงาน: การเปิดเส้นทางนี้ **ไม่ได้** พิสูจน์ routing/fan-out/membership ของเซิร์ฟเวอร์ต้นฉบับ (ไม่เคยถูก capture) และไม่ได้เปิดช่องอื่นนอก LocalTalk

### pass criteria (สองชั้น 🔴 ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)
- **ชั้น wire/console** — บูต **ไม่ส่ง `--*-scenario` แม้แต่ตัวเดียว** · ส่งเฟรมแชท ascii → คอนโซลพิมพ์โทเคน echo ของเส้นทาง production (ชื่อโทเคนกำหนดตอนเดินสาย) และเฟรมตอบออกสาย · headless พิสูจน์ได้ในตัว ไม่ต้องมีจอ
- **ชั้น client-observable** — เจ้าของ/ผู้เทสพิมพ์ข้อความในเกมบนบูตปกติแล้ว **เห็นบรรทัดของตัวเองบนจอ** · ต้องมี `OBSERVER_CONFIRMED: <ISO+07:00>` · = ข้อ ④ ของนิยาม "เสร็จ" (ADDENDUM ข้อ 9: นัดเจ้าของ 5-10 นาทีกดเอง)

### นิยามเสร็จของใบนี้ (directive ข้อ 4 — ครบสี่ข้อเท่านั้น)
① อยู่บน main · ② ถึงผู้เล่นบนบูตปกติไร้แฟล็ก · ③ ขึ้นสกอร์บอร์ด production (generator ของกะ3-A ตาม COO 2246 ข้อ 3) · ④ เจ้าของกดผ่านหนึ่งรอบ

### links
`notes_to_chief/20260829_2222_PANYA-DIRECTIVE-productive-org-8-items-*.md` · `notes_to_chief/20260829_2233_PANYA-DIRECTIVE-ADDENDUM-items-9-10-*.md` · `notes_to_chief/20260829_2246_COO-DECISION-directive-2222-parameters-set.md` · `GT-009` · `GT-012` · `GT-016` (ใบห้าช่อง คนละขอบเขต)

**ผู้เปิดใบ: chief (สาย E) รอบ `k882hm` 2026-08-29T23:1x+07:00** — ผลกลับมาที่ chief บริโภค

---

## 🆕🔬 GT-158 ACTIONVITAL-FIELD-U16-4A-LIVE-SCENE-TRACKING-001 [attended, in-game, opt-in scenario required]: `field_u16_4a` ของ `ActionVital` ถูกตั้งชื่อ/ใช้เป็น `scene_id` โดย `action_ack.py` -- มันติดตามฉากปัจจุบันของไคลเอนต์แบบสดจริงหรือเป็นค่าที่ผูกไว้ตายตัวต่อการทดลอง  [🟡 **PENDING** · `STATUS-SET-BY-CHIEF 2026-09-05T02:0x+07:00 from body` ตาม `COO-DECISION 20260904_2349` ข้อ 6 · เหตุผลที่เลือกป้ายนี้: เนื้อใบไม่มีตัวบล็อกโค้ด — โค้ดที่ต้องใช้ (`action_ack.py` · `runtime.py:6483-6501`) เดินสายอยู่แล้ว ใบนี้แค่ต้องบูตด้วย `--scene-load-scenario` ตามที่หัวใบระบุ (`opt-in scenario required`) แล้วเดินข้ามฉากใน **หนึ่ง session เดียว** ซึ่งเป็นสิ่งที่ยังไม่มีใครทำ · ไม่บล็อกใคร ต่อคิวหลังรายการใน `NOW.md` · **เจ้าของใบ (LANE-A) แก้ป้ายนี้ได้หนึ่งรอบผ่านจดหมาย ไม่แก้ = ยืน**]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง 2026-08-30T13:5x+07:00: `GT-158`/`RE-158` = 0 hit ทั้งสองไฟล์ ·
> สูงสุดก่อนหน้า `RE-157` (`GT`/`RE` ใช้ตัวนับเดียวร่วมกัน ตามกฎที่ `RE-152` หัวใบเคยระบุไว้)
> ⇒ ใบนี้คือ `GT-158` · ใบ `RE-085`-`RE-157`/`GT-001`-`GT-152` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ

### ที่มา [วัดแล้ว โดย pf-adversary รอบตรวจ `RE-156` ของ LANE-A, 2026-08-30T13:5x+07:00]

ระหว่างตรวจ draft แรกของ `RE-156` (ซึ่งอ้างผิดว่าไม่มี client->server byte พกเลขฉากเลย) `pf-adversary`
พบว่า `current/pf_login_game_server_v141.py:3250-3284` `parse_action_vital`'s field `field_u16_4a`
(offset `0x12`) ถูก `src/pirateforce_foundation/action_ack.py:8-11,63` ตั้งชื่อ/เทียบเป็น `scene_id` ตรงๆ
และเดินสายจริงใน `src/pirateforce_foundation/runtime.py:247,6483-6501` (หลัง `--scene-load-scenario`
เท่านั้น, `src/pirateforce_foundation/app.py:98,287-288`) แคปเจอร์จริงสองชุดเห็นค่าต่างกันตรงกับฉากจริง
ที่ต่างกัน: `reports/PF_SCENE006_EA7D_ATTACK_COMMAND_RUNTIME_PASS_20260815.md:21` = ฉาก 2,
`reports/PF_SCENE007_PORT_ROYAL_EA7D_ACTION_ACK_RUNTIME_PASS_20260816.md:13,27-28` = ฉาก 1 (Port Royal)
**แต่ทั้งสองเป็นคนละ session คนละบูต** ไม่มีใครเดินข้ามฉากในหนึ่ง session แล้ววัดว่าค่าขยับตาม

### objective

แยกสองสมมติฐานที่ static ปัจจุบันแยกไม่ออก:
1. **(A) ไคลเอนต์เขียนฉากปัจจุบันจริงลงฟิลด์นี้ทุกครั้งที่ส่ง `ActionVital`** — ถ้าจริง = สัญญาณยืนยันฉาก
   ที่ใช้งานได้ (แม้จะยังอยู่หลังแฟล็ก opt-in และอยู่นอกโดเมน world/travel เดิม)
2. **(B) ค่านี้ถูก bake ไว้ต่อ scenario/producer และบังเอิญตรงกับฉากจริงของการทดลองแต่ละครั้ง** — ถ้าจริง
   = ไม่ใช่สัญญาณอะไรเลย เป็นเรื่องบังเอิญของการตั้งค่าเทสสองชุดที่ต่างกัน

การทดลอง: ใน session เดียว ให้ตัวละครอยู่ฉาก A แล้วส่ง `ActionVital` (ผ่าน `--scene-load-scenario`
ตามที่กลไกปัจจุบันบังคับ) บันทึกค่า `field_u16_4a` แล้วเปลี่ยนไปฉาก B (เท่าที่ทำได้ภายใต้ M2/สถานะ paused
วันนี้ -- อาจใช้ฉากที่เปิดล็อกอินอยู่แล้วสองฉากคนละบูตที่ควบคุมตัวแปรอื่นให้เหมือนกันที่สุด ถ้าข้าม
session ในตัวเดียวไม่ได้ภายใต้ข้อจำกัดปัจจุบัน) ส่ง `ActionVital` อีกครั้งในฉาก B แล้วเทียบค่า

### pass criteria

**ชั้น client-observable (ปิดใบนี้ได้ ชั้นเดียวพอเพราะคำถามเป็นคำถาม client-observable ล้วน):**
- ค่า `field_u16_4a` ที่สังเกตได้จริงจากไคลเอนต์ต่างกันตามฉากจริงที่ต่างกัน ⇒ สมมติฐาน (A) ได้รับการยืนยัน
- ค่าเดิมไม่ขยับตามฉาก (คงที่ไม่ว่าจะยืนฉากไหน) ⇒ สมมติฐาน (B) ได้รับการยืนยัน, field นี้ตกจากการเป็น
  ผู้สมัครสัญญาณยืนยันฉาก

### nonclaims

1. ไม่อ้างว่าใบนี้ปลดล็อกอะไรใน production -- กลไกทั้งหมดอยู่หลัง `--scene-load-scenario` และเป็น
   `HYP-PF-002 frozen` ของโดเมน combat ไม่ใช่ world/travel
2. ไม่อ้างว่าผลของใบนี้ (ไม่ว่าทางไหน) เปลี่ยนสถานะของ `scene_admission_gate`/`world_travel_gate`
   หรือ M2 -- คนละกลไกกันเป๊ะ, เปิดใบนี้เพื่อตอบคำถามที่ `RE-156` เปิดค้างไว้เท่านั้น
3. ไม่อ้างว่าการทดลองนี้ต้องรอ M2 ปลดล็อกก่อน -- ถ้ามีฉากที่เปิดล็อกอินอยู่แล้ววันนี้สองฉาก (เช่น 1 กับ 14)
   ที่ยิง `ActionVital` ได้ทั้งคู่ภายใต้ opt-in scenario เดียวกัน อาจทดลองข้ามบูตแทนได้ -- ผู้รับใบตัดสินเอง
   ว่าการควบคุมตัวแปรแบบไหนน่าเชื่อถือพอ

### links
ใบผลที่เปิดคำถามนี้: `notes_to_chief/20260830_1327_RE-156-RESULT-no-scene-carrying-client-byte-teleport-check-echo-is-the-nearest-proxy.md`
(ฉบับแก้ 2026-08-30T13:5x+07:00) · `RE-156` (ปิดชั้น wire/DB แล้ว, แยกชั้น client-observable มาที่นี่) ·
`src/pirateforce_foundation/action_ack.py` · `src/pirateforce_foundation/runtime.py:247,6483-6501` ·
`src/pirateforce_foundation/app.py:98,287-288` · `tests/test_action_ack.py`

**ผู้เปิดใบ: LANE-A (สาย A · WORLD) รอบ `re156-answer` 2026-08-30T13:5x+07:00** — คำถามอยู่นอกโดเมนของ
สายนี้ (combat ไม่ใช่ world) แต่เปิดใบไว้ตามกฎ "เจอสิ่งที่ไม่รู้ ให้เปิดใบ" แทนการหยุดสร้างของเพื่อค้นเอง

## 🆕🔬 GT-159 M2-DEST-COLUMBUS-MARKER17-TRANSFORM-TO-SHIP-001 [attended, in-game]: ถ้าเซิร์ฟเวอร์เคยส่งฉาก 126 ที่ `MARKER[17]` พิกัด `(3050, 232, 90)` หันหน้า 6 แทนฉาก 17 -- ผู้เล่น**แปลงร่างเป็นเรือและอยู่ในทะเล**ตามที่เจ้าของจำได้ (`GT-106` ข้อ ④.2) จริงหรือไม่ -- ตัดสินด้วยตา ไม่ใช่ด้วยการเถียงตาราง  [⚪ **CANCELLED - covered by `GT-266` · no longer needs proving because `PANYA-DECISION 20260905_1329`** -- ปิดโดย chief (LANE-E) รอบ `m8wtlr`/R356 2026-09-05T17:0x+07:00 ตาม `COO-DECISION 20260905_1543` — ประวัติ/เหตุผลเต็มของหัวใบเดิม (รวมข้อความ `~~BLOCKED~~` เก่าที่ถอนแล้ว ซึ่งทำให้เครื่องมือ regex อ่านใบนี้กลับเป็น BLOCKED ผิด ตาม chief `R374` ข้อ 2) ย้ายไปบรรทัด "ประวัติหัวใบเดิมคำต่อคำ" ถัดไปคำต่อคำ ไม่แก้เนื้อหา [จัดรูปแบบโดย LANE-K รอบ `x91eo8r2` — ยืนยันแล้วว่า `COO-DECISION 20260905_1543` ตัดสิน CANCELLED นี้ไว้แล้วจริง (`grep -rl "GT-159" notes_to_chief/*COO-DECISION*` เจอฉบับนี้ตรง ๆ — รอบ `x91eo8` ก่อนหน้ารายงานผิดว่า "0 hit", แก้ไขแล้วในจดหมายรอบนี้)]] -- archived 20260907 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md`, LANE-K round `kxpzxi`)

## 🆕🎮 GT-160 TRAINING-DUMMY-NAME-COLOUR-001 [attended, in-game]: หุ่นซ้อม (n_ID 916, `Training Iron Man`) สี่ตัวใน Port Royal ขึ้นชื่อสีศัตรู (แดง/ส้ม ตาม GT-032) บนจอจริงหรือไม่ ทั้งที่ `rank=0`/`ai_combat=0`  [🟢 **READY** · `STATUS-SET-BY-CHIEF 2026-09-05T02:0x+07:00 from body` ตาม `COO-DECISION 20260904_2349` ข้อ 6 · เหตุผล: เนื้อใบเป็น client-observable ชั้นเดียวล้วน ไม่มีตัวบล็อกโค้ด ไม่มีแฟล็ก ไม่ต้องรอ PR ใด — ยืนที่ Port Royal มองป้ายชื่อหุ่นซ้อมสี่ตัว (~1 นาที) · ✅ **ไม่ใช่ใบตีมอน** จึงไม่ติดข้อห้าม "ห้ามใบเทสตีมอนจน P-2 ปิด" ใน `NOW.md` — ห้ามตีหุ่น ให้ดูสีป้ายอย่างเดียว · ผลของใบนี้ป้อน P-2 โดยตรง (เงื่อนไขสีดูที่ `rank`/`ai_combat` หรือดูที่อย่างอื่น) · ไม่บล็อกใคร ต่อคิวหลังรายการใน `NOW.md` · เจ้าของใบ (LANE-B) แก้ป้ายได้หนึ่งรอบ]

> 🔢 **หมายเหตุเลข:** grep ยืนยันซ้ำที่ round `xt0g9c` 2026-08-30T15:3x+07:00 หลัง recovery ของ PR #498
> (round `309h1a` จองเลข `GT-159` ไว้ แต่ PR ไม่ merge เพราะชนกับ lane A ที่จอง `GT-159` สำเร็จก่อน --
> ดู `rounds/B_20260830_1448_309h1a_mailbox_batch_plus_self_aggro_survey.md`) · สูงสุดบน `main` วันนี้คือ
> `GT-159`/`RE-157` ⇒ ใบนี้เปลี่ยนเลขเป็น `GT-160` · ใบ `RE-085`-`RE-157`/`GT-001`-`GT-159` อยู่ที่เดิม
> ทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ

### ที่มา

`COO-DECISION 2026-08-30T13:51+07:00` (`training-dummy-and-partial-roster-withdrawal`, ข้อ "ใครทำอะไรต่อ")
สั่งให้ LANE-B เปิดตั๋วเล็กเรื่องนี้ "ไม่บล็อก M4" — หุ่นซ้อม 916 สี่ตัว (`field_mob_tables.
TOWN_TARGET_PLACEMENTS`) เป็นเป้าตีได้จริงตาม COO-DECISION 2026-08-29T00:41+07:00 แต่เป็น `rank=0`,
`ai_combat=0` ("ไม่ใช่มอนสเตอร์ของ Port Royal" ตามคอมเมนต์ในโค้ด) — GT-032 พิสูจน์แล้วว่า NPC ชื่อขึ้นสีแดง
สำเร็จ แต่ยังไม่มีใครวัดว่าเงื่อนไขสีนั้นดูที่ `rank`/`ai_combat` หรือดูที่อย่างอื่น (เช่น faction splice
อย่างเดียวที่ทุกแถวในไฟล์นี้มี ไม่ว่าจะเป็นหุ่นซ้อมหรือมอนจริง) — RE-067 (สาย RE เปิดค้าง) คือคำถามระดับ
โครงสร้างเดียวกัน ใบนี้แคบกว่า: ถามแค่กรณีหุ่นซ้อมสี่ตัวนี้โดยเฉพาะ

### pass criteria (ชั้น client-observable ชั้นเดียวพอ เพราะคำถามเป็นสายตาล้วน)

ยืนอยู่หน้าหุ่นซ้อมตัวใดตัวหนึ่งใน Port Royal (`x=14455.27,y=9356.76` เป็นต้น) แล้วดูชื่อบนหัว:
- ขึ้นสีแดง/ส้ม (สีศัตรู) เหมือน GT-032 ⇒ สีไม่ได้ผูกกับ `rank`/`ai_combat` (เป็นข้อมูลใหม่ให้ RE-067)
- ขึ้นสีขาว/เหลือง (สีเป็นกลาง/มิตร) ⇒ สอดคล้องกับสมมติฐานว่าสีผูกกับ `rank` หรือ `ai_combat`

### nonclaims

1. ไม่อ้างว่าใบนี้ปิด `RE-067` (ยังเปิดอยู่ เป็นคำถามทั่วไปกว่านี้)
2. ไม่บล็อก M4/M5 — หุ่นซ้อมตีได้ ตายได้ เก็บของได้อยู่แล้วไม่ว่าสีชื่อจะเป็นอะไร

### links
`field_mob_tables.py` (`TOWN_TARGET_PLACEMENTS`) · `COO-DECISION 2026-08-29T00:41+07:00` ·
`COO-DECISION 2026-08-30T13:51+07:00` (`training-dummy-and-partial-roster-withdrawal`) · `GT-032` · `RE-067`

**ผู้เปิดใบ: LANE-B (สาย B · COMBAT) รอบ `309h1a` 2026-08-30T14:4x+07:00, เลขแก้เป็น GT-160 ที่รอบ
`xt0g9c` หลัง recovery** — ตามคำสั่ง COO ข้างต้น ไม่เร่งด่วน ไม่บล็อก M4/M5 รอคิวเทสที่มีคนอยู่หน้าจอตามปกติ

## 🆕🎮 GT-164 BT-GM-VARIANT-CLICK-SWEEP-001 [attended, in-game]: **คลิก `BT_GM` ทีละ variant ของ `gm/bt_gm_probe.py` (สี่ตัวคงที่ + บิต 0-7 ของ `field_0x14` + ค่าสูงสุด) แล้วดูว่า `GMUI_BASIC` เปิดไหม — ตอบข้อ 2 (query-gate เวลาคลิก) ของ `RE-164` เท่านั้น ข้ออื่นตอบด้วย static RE ต่างหาก** [✅ **RESULT รอบ `szmgeh` — bounded negative ครบ 14/14, ปิดหัวใบ; ผลข้างเคียง: `field_0x0b_second` = สวิตช์การมองเห็นปุ่ม `BT_GM` ยืนยันแบบ attended เป็นครั้งแรก**]

### ผล (รอบ `szmgeh`, 2026-08-31T08:50-08:55+07:00, กะ1-A observer)
14/14 variant ถูกยิงผ่าน `/gmprobe <variant_id>` แล้วคลิก `BT_GM` — **ไม่มีตัวไหนเปิด `GMUI_BASIC`** =
bounded negative ตามที่ objective ทำนายไว้ ปิดหัวใบนี้ (`RE-164` ข้อ 2 ถูกตัดออกจากการเป็นประตู ทั้ง static
และ attended ตรงกัน — ดู `CLIENT_RE_QUEUE.md#RE-164` ข้อ 2) ผลข้างเคียงที่ใหญ่กว่า objective เดิม:
`field_0x0b_second` (ฟิลด์ที่รู้จักอยู่แล้วจาก `RE-089`/`RE-104`/`CORE-REQUEST-020` ว่าคุมการมองเห็นปุ่มตอน
login) ยืนยันด้วยตาว่าคุมการมองเห็น**กลางเซสชัน**ด้วยผ่าน `/gmprobe` เช่นกัน 14/14 ไม่มีข้อยกเว้น ไม่ต้อง
relog — codified เป็น `gm/bt_gm_probe.py`'s `observed_button_visible`/`guaranteed_visible_variant_ids`/
`guaranteed_hidden_variant_ids` (รอบ `szmgeh`) เพื่อให้ผู้เทสรอบต่อไปที่ไล่ข้อ 1/3 ของ `RE-164` เลือก
variant ที่รู้อยู่แล้วว่าปุ่มจะโชว์ได้ทันที ไม่ต้องเดา
เอกสารเต็ม:
`notes_to_chief/20260831_0901_GT164-RESULT-bounded-negative-on-suspect-2-plus-field-0x0b-second-is-the-button-visibility-switch.md`
**nonclaim:** ผลนี้ตอบเฉพาะข้อ 2 ของ `RE-164` เท่านั้น (ตามที่ objective เดิมกำหนด) ไม่ตอบข้อ 1/3/4 — และ
"มองเห็นได้" ไม่ใช่ "คลิกได้ผล" สองเรื่องคนละชั้น (ดู `observed_button_visible` docstring)

### สถานะเดิม (ก่อนผลรอบ `szmgeh` — เก็บไว้อ่านประกอบ ไม่ลบ)
**ปลด BLOCKED** (รอบ LANE-GM `jz4don`, `CORE-REQUEST-GM-043` ตัดสินทางเลือก A โดย chief): จุดเสียบใหม่คือ
คำสั่งแชท GM `/gmprobe <variant_id>` (`gm/chat_command_action.py::_gmprobe_action`, ต่อผ่าน dispatch เดียว
กับ `/warp`/`/say`) — บัญชี GM พิมพ์ `/gmprobe <variant_id>` ในแชทระหว่างเซสชัน ได้ทั้ง 14 variant ตามชื่อ
ใน `bt_gm_probe.known_variant_ids()` (`baseline-all-zero`, `first-byte-1`, `second-byte-1`, `both-bytes-1`,
`u32-bit0`..`u32-bit7`, `u32-max`, `all-fields-1`) จุดเสียบเดิมตอนล็อกอิน (`runtime.py:6424-6438`, ค่าคงที่
`(0,1,0)`) ยังอยู่เหมือนเดิม ไม่ถูกแทนที่ — `/gmprobe` เป็นทางเพิ่ม ไม่ใช่ทางแทน **ยังไม่มีการยิงจริงกับ
ไคลเอนต์จริงรอบนี้** — สิ่งที่ลง main คือจุดเสียบเท่านั้น การคลิกจริงยังเป็นงานของกะ1-A ตามใบนี้

### objective
ให้ผู้เทส (กะ1-A) login ด้วยบัญชี GM แล้วพิมพ์ `/gmprobe <variant_id>` ทีละตัวจากทั้ง 14 ชื่อข้างต้น
(เรียงตามลำดับ `bt_gm_probe.known_variant_ids()`) จากนั้นคลิกปุ่ม `BT_GM` **หลังทุก variant** แล้วบันทึกว่า
`GMUI_BASIC` เปิดหรือไม่ — ตัวแรกที่เปิดคือคำตอบ ถ้าไม่มีตัวไหนเปิดเลยทั้ง 14 ตัว = bounded-negative ต่อ
"field_0x14 บิต 0-7/max และสอง u8 field ไม่ใช่ gate" (ยังไม่ปิดคำถามเรื่อง connection-context/create-path/
current-UI-key ซึ่งเป็น stub แยกใน `RE-164`)

### pass criteria — สองชั้น
**client-observable:** เจ้าของ/กะ1-A ยืนยันด้วยตาว่า `GMUI_BASIC` เปิดหลัง variant ใดตัวหนึ่ง (หรือไม่เปิดเลย
ทั้ง 14 ตัว = negative ที่มีค่า)
**wire/DB:** เฟรมขาเข้าที่พิสูจน์ว่า variant ถูกส่งจริงตามลำดับที่ตั้งใจ (log ของ `runtime.py` call site ใหม่)

### ข้อห้าม
ห้ามข้าม variant ห้ามคลิกก่อนยิง variant ครบ (ต้องรู้ว่า "ก่อน/หลัง" variant ไหน) · ห้ามอ้างว่าใบนี้ตอบ
suspect 1/3/4 ของ `RE-164` (connection context / current-UI key / create path) — ใบนี้ตอบเฉพาะ "ค่าของเฟรมนี้
ทำให้เปิดไหม" เท่านั้น

### สัญญาผู้บริโภค
เปิดโดย LANE-GM รอบ `b3fgm6` — LANE-GM บริโภคผลเอง **ปิดหัวใบแล้วรอบ `szmgeh`** (chief ต่อจุดเสียบรอบ
`jz4don`, กะ1-A คลิกจบและรายงานผล 2026-08-31T08:50-08:55+07:00)

### links
`src/pirateforce_foundation/gm/bt_gm_probe.py` (`iter_state_vital_bit_variants`, `known_variant_ids`,
`variant_by_id`, `observed_button_visible`, `guaranteed_visible_variant_ids`,
`guaranteed_hidden_variant_ids` -- รอบ `szmgeh`) ·
`src/pirateforce_foundation/gm/chat_command_action.py` (`_gmprobe_action`) ·
`CLIENT_RE_QUEUE.md#RE-164` · `notes_to_chief/20260831_0321_LANE-GM-CORE-REQUEST-GM-043-bt-gm-variant-call-site-for-gt164.md`
(ใบเปิด) · `notes_to_chief/20260831_0357_CHIEF-REPLY-CORE-REQUEST-GM-043-decision-option-A-gmprobe-chat-command.md`
(ตัดสินใจ) · `GT-101`/`GT-103`/`GT-107` (baseline: ค่า `(0,1,0)` คลิกเงียบ) ·
`notes_to_chief/20260831_0901_GT164-RESULT-bounded-negative-on-suspect-2-plus-field-0x0b-second-is-the-button-visibility-switch.md`
(ผลใบนี้)

## 🆕 GT-165 SLAVE-MARKET-ISLAND-FIRST-EYES-001 [attended, in-game]: เกาะตลาดทาส `Bg0004` (ฉาก 4) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเจกต์ในฉากนี้  [~~READY~~ 🟢 **PASS ทั้งสองชั้น — LANE-A... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕 GT-166 DEEP-SEA-TEMPLE-LANDING-GEOMETRY-001 [attended, in-game]: ฉาก 10 (Bg0010, Deep Sea Temple floor 1) ตัวประกอบ 94/100 ขึ้นจอไหม -- และ MARKER[10] เป็นพื้นที่ยืนได้จริงหรือไม่ (เกณฑ์คู่ ไม่ใช่แค่ actor)  [READY]

ATTENDED: บูตตาม `ATTENDED_SESSION_RUNBOOK.md` บน DB สำเนา run-copy ของ `state\pirateforce.sqlite3` เท่านั้น (ห้ามเปิด canonical · เทียบ sha ก่อน/หลัง) เซิร์ฟก่อนไคลเอนต์ทีหลัง เก็บคอนโซล `2>&1` -> เข้าฉาก 10 (`Bg0010` Deep Sea Temple ชั้น 1) ด้วยทางใดทางหนึ่งที่ใบเขียนไว้เท่านั้น: บัญชี GM staged (`config/gm_login_scene.json`, scene_id=10) หรือพิมพ์ `/warp 10` (คลิกช่องแชทยืนยัน focus จริงก่อนพิมพ์ ไม่โฟกัส = ฮอตคีย์) รอจอนิ่งแล้วถ่ายภาพนิ่งเต็มความละเอียด
ATTENDED: ชั้น wire/DB: หาบรรทัดคอนโซล `WORLD_CENSUS_BG0010 assembled=94/100 ...` หลังล็อกอินเข้าฉาก 10 (pin แล้วโดย `tests/test_lane_a_scene_census.py::OnTheRealDispatcherTests::test_with_the_real_registry_the_deep_sea_temple_census_ships_94`) · ชั้นจอ objective (1): เห็น actor ขึ้นจอหรือไม่ นับคร่าว ๆ พอ ไม่ต้องครบ 94 · ชั้นจอ objective (2): ยืนบนพื้นได้ปกติ หรือหล่น/ติดหิน/จอดำ -- ข้อ (2) **ไม่มีชั้น wire/DB ให้เทียบ** ห้ามใช้คอนโซลตอบแทนตา
ATTENDED: ตัดสินแยกสองข้อ ห้ามรวมกัน: ข้อ (1) ตัดสินที่ชั้นจอเท่านั้น -- เห็นสิ่งมีชีวิต = ตอบว่าใช่ · เข้าไปแล้ว**ว่างเปล่าไม่มีอะไรเลย = ผลลบที่มีค่า บันทึกเป็นผล ไม่ใช่ FAIL** (ใบตาคู่แรกของฉากนี้) · มอนไม่ก้าวร้าวเป็นพฤติกรรมที่คาดไว้ (composer ตั้งใจไม่ส่ง faction bit) ไม่ใช่ FAIL · ข้อ (2) เป็นข้อมูลใหม่ให้ทะเบียน: ตกในหิน/ลอยกลางอากาศ/จอดำ **ไม่ใช่ FAIL ของข้อ (1)** ให้บันทึกตามที่เห็น
ATTENDED: บูตปกติ ใบนี้ไม่ระบุแฟล็ก/env/ทรีพิเศษใด ๆ ⇒ ไม่มีแฟล็ก `--*-scenario` · ทรีต้องมี composer `world_population_bg0010.py`/`world_bg0010_identity.py` และทะเบียน `scenarios/world_scene_registry_001.json` แถว `n_id: 10` ที่ `login_entry_allowed=true` (ไม่งั้นเข้าฉากไม่ได้เลย = NO-RESULT ไม่ใช่ FAIL) · teardown ต้องรันเสมอแม้รอบจบเพราะเลิกเล่นเฉย ๆ
ATTENDED: จดตัวเลขที่ใบต้องการลงผล: จำนวน actor คร่าว ๆ + สภาพจุดยืน (`MARKER[10]` ห่าง placement ใกล้สุด 5174.7 หน่วยและอยู่นอกขอบเขต · z ของ marker 465 เทียบพื้น placement ต่ำสุด -4532.9 · ฉาก interior `n_CANGLIDE=0`/`n_LIMIT_HEIGHT=0` บินร่อนไม่ได้) · จดสีป้ายชื่อทุกป้ายในทุกภาพจากภาพเต็มความละเอียด (`none` ถ้าไม่มี ห้ามอนุมานสาเหตุจากสี) · จัดมุมกล้องและเช็ค NO-CRASH ด้วยคลิกขวาค้างลากเท่านั้น ห้าม `Q`/`E`

> เปิดโดย LANE-A (สาย A · WORLD) รอบ `3t75jw`, 2026-08-31T09:3x+07:00 -- `login_entry_allowed` ของฉาก 10
> พลิกเป็น `true` รอบนี้ (`COO-DECISION 20260830_1441`, ประตูที่สองในคิวเดียวกับฉาก 4; composer
> `world_population_bg0010.py`/`world_bg0010_identity.py` สร้างรอบ `u3jo4g` ผูกรอบ `c42axq` ถูกตัดสินว่า
> พร้อมแล้ว) -- ไม่ใช่สำเนาของ `GT-165` เพราะฉากนี้มีความเสี่ยงที่ `GT-165` ไม่มี: ทะเบียนเอง
> (`table_row_differences.the_two_interiors`, pf-adversary รอบ `ga91m5`) ระบุฉากนี้ (คู่กับฉาก 11) เป็น
> "สองแถวที่รอบ attended ควรดูก่อนถ้าจุดลงมีปัญหา"

### objective (สองคำถาม ไม่ใช่หนึ่ง)
(1) ล็อกอินเข้าฉาก 10 จริงแล้ว **เห็นสิ่งมีชีวิตขึ้นจอ** (ไม่ใช่ถ้ำว่างเปล่า) ใช่หรือไม่ -- composer ตั้งใจไม่ส่ง
faction bit เลย เหมือนฉาก 4 (ดู `world_population_bg0010.py` docstring) จึงไม่ใช่คำถามเรื่องความก้าวร้าว
(2) **ผู้เล่นยืนบนพื้นได้จริงไหม หรือตกในหิน/ลอยกลางอากาศ/จอดำ** -- จุดเกิด `MARKER[10]` อยู่ห่างจาก
placement ที่ใกล้ที่สุดของฉากนี้ถึง 5174.7 หน่วย (นอกขอบเขต placement ทั้งหมด) พื้น placement ต่ำสุดของฉากนี้
อยู่ที่ z=-4532.9 ขณะที่ marker อยู่ที่ z=465 -- ต่างกันเกือบ 5000 หน่วย ฉากนี้ยังเป็น "interior" แบบ
n_CANGLIDE=0/n_LIMIT_HEIGHT=0 (บินร่อนไม่ได้ ไม่มีเพดานจำกัดความสูง) คำถามที่ 2 นี้คือเหตุผลที่ใบนี้แยกจาก
`GT-165` ไม่ใช่ใบเดียวกัน

### ทางเข้า
ไม่มี production path ใดเขียนแถว character ให้ชื่อฉาก 10 เอง (ดู `login_entry_allowed_because` ในทะเบียน) --
เข้าได้เฉพาะ staged GM account (`config/gm_login_scene.json`, scene_id=10) หรือ GM `/warp 10`

### สิ่งที่ยังไม่วัด (บันทึกไว้ล่วงหน้า ไม่ใช่คำทำนายว่าจะพัง)
จุดเกิด `MARKER[10]` เป็นชั้นหลักฐาน `authored` เท่านั้น -- ไม่เคยมีไคลเอนต์ยืนจริง ตัวเลขระยะทาง/z ข้างต้นคือสิ่ง
ที่วัดได้จากตารางไคลเอนต์ ไม่ใช่การคาดเดา -- ถ้าคำถามที่ 2 ตอบว่า "ตกในหิน/หลุดพื้น/จอดำ" **ให้บันทึกเป็น
ข้อมูล ไม่ใช่ FAIL ของ objective (1)** สองคำถามนี้แยกอิสระจากกันโดยตั้งใจ

### pass criteria — สองชั้น, แยกตาม objective
**wire/DB objective (1) (ปิดแล้วโดยเทส):** console line `WORLD_CENSUS_BG0010 assembled=94/100 ...` ปรากฏหลัง
ล็อกอินเข้าฉาก 10 -- pin ไว้แล้ว `tests/test_lane_a_scene_census.py::OnTheRealDispatcherTests::
test_with_the_real_registry_the_deep_sea_temple_census_ships_94`
**client-observable objective (1) (ยังไม่มีใครยืนดู):** ผู้เทสเข้าฉาก 10 จริงแล้วรายงานว่าเห็น actor ขึ้นจอ
หรือไม่ (นับคร่าว ๆ พอ ไม่ต้องนับให้ครบ 94)
**client-observable objective (2), ไม่มีชั้น wire/DB ให้ (ไม่มีอะไรในโค้ดฝั่งนี้ตรวจพื้นได้):** ผู้เทสรายงานว่า
ยืนบนพื้นได้ปกติ หรือหล่น/ติดหิน/จอดำ -- ผลของคำถามนี้เป็นข้อมูลใหม่สำหรับทะเบียน ไม่ใช่เกณฑ์ผ่าน/ไม่ผ่านของ
composer นี้

### สัญญาผู้บริโภค
เปิดโดย LANE-A -- LANE-A บริโภคผลเอง ปิดหัวใบเมื่อผู้เทสยืนยันด้วยตาทั้งสอง objective (แยกกันได้ -- objective
(1) อาจ PASS ขณะ objective (2) รายงานปัญหา)

### links
`scenarios/world_scene_registry_001.json` แถว `n_id: 10` (`login_entry_allowed_because`,
`table_row_differences.the_two_interiors`) · `src/pirateforce_foundation/world_population_bg0010.py`,
`world_bg0010_identity.py` · `notes_to_chief/20260831_0932_LANE-A-ASK-COO-scene10-landing-geometry-elevated-risk.md`
· `GT-165` (scene 4, same shape minus the geometry risk) · `GT-134` (scene 14, same shape)

## 🆕🔬 GT-170 NPC-DIALOGUE-CLOSE-OPCODE-002 [STATIC-ON-BRIDGE -- ต้องเปิด `GameClient.local.bin` จริง คลาวด์ทำต่อไม่ได้]: `RE-169` (คลาวด์, static จาก TSV ที่ commit แล้ว) เจอสามผู้ต้องสงสัยชื่อใกล้เคียง "ปิดหน้าต่างบทสนทนา NPC" แต่ยืนยันบน wire ไม่ได้เพราะไม่มีอิมเมจ -- ใครมี `GameClient.local.bin` ช่วยไล่ต่อสองข้อ

### สามผู้ต้องสงสัย (จาก `RE-169`, ดู `CLIENT_RE_QUEUE.md` สำหรับ provenance เต็ม)
1. `OpenCloseUI` (`PF_PROTOCOL_REGISTRY.tsv:54`) -- มี vtable/serializer/handler VA จริง, serializer ไม่ว่าง
   (สองสตริง + tag ตัวเลข `0x05`/`0x14`/`0x32`) แต่ `NOT_OBSERVED` ใน capture ไหนเลย
2. `WindowClosedPayloadMsg` / `WindowCloseResponseMsg` / `WindowCloseRequestMsg` (RTTI names,
   `PF_RUNTIME_CLASSMAP.tsv`) -- ชื่อใกล้เคียงที่สุดในทั้ง repo แต่ไม่มี opcode ผูกอยู่เลย อยู่ใต้ namespace
   `UIAutomationCoreProto` (อาจเป็นโค้ด UI-automation ทั่วไปของ Windows ไม่ใช่ระบบเกม)

### สองข้อที่ต้องตอบจากอิมเมจ
1. handler ของ `OpenCloseUI` dispatch ตาม UI-id enum อะไร -- มีค่าไหนตรงกับ NPC dialogue/conversation window
2. `WindowClose*` สามชื่อ vtable ไปถึง network message dispatch table จริงหรือเป็นโค้ดที่ตายแล้ว (ไม่ reachable
   จาก network)

### pass criteria -- สองชั้น
**wire/DB (ปิดแล้ว, ดู `RE-169`):** สาม candidate พร้อม provenance จาก TSV ที่ commit แล้ว
**client-observable (ใบนี้ถาม):** เปิดอิมเมจตอบสองข้อบน -- ถ้าพบ UI-id/handler ที่ตรง ให้เปิด CORE-REQUEST
ถึง chief ต่อสาย (`runtime.py:5082`, เขตของ chief) ห้ามต่อ production เองแม้จะดูชัดเจน

### ข้อห้าม
ห้ามต่อ production call site ด้วย `OpenCloseUI`/`WindowClose*` จนกว่าจะยืนยัน handler/vtable จากภาพจริง --
บทเรียนเดียวกับ `RE-125`'s `0x4543` (ชื่อที่ดูใช่ไม่แปลว่า opcode ที่ยืนยันแล้ว)

### สัญญาผู้บริโภค
เปิดโดย chief -- LANE-A บริโภคผลเมื่อมีคนตอบจากอิมเมจ (ตามที่ `RE-169`/`RE-168` มอบหมายไว้)

### links
`CLIENT_RE_QUEUE.md` RE-169 · `notes_to_chief/20260831_1142_RE-168-RESULT-no-dialogue-close-signal-exists-server-is-stateful-enough-to-add-one.md`

## 🆕 GT-171 EVIL-PORT-FIRST-EYES-001 [attended, in-game]: ฉาก 5 (Bg0005, Evil Port) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเจกต์ในฉากนี้  [READY]

ATTENDED: บูตตาม `ATTENDED_SESSION_RUNBOOK.md` บน DB สำเนา run-copy ของ `state\pirateforce.sqlite3` เท่านั้น (ห้ามเปิด canonical) เก็บคอนโซล `2>&1` -> เข้าฉาก 5 (`Bg0005` Evil Port) ด้วยทางใดทางหนึ่งที่ใบเขียนไว้เท่านั้น: บัญชี GM staged (`config/gm_login_scene.json`, scene_id=5) หรือพิมพ์ `/warp 5` (คลิกช่องแชทยืนยัน focus ก่อนพิมพ์) -> รอจอนิ่ง กวาดสายตารอบเมืองท่า ถ่ายภาพนิ่งเต็มความละเอียด
ATTENDED: ชั้น wire/DB: หาบรรทัดคอนโซล `WORLD_CENSUS_BG0005 assembled=87/92 ...` หลังล็อกอินเข้าฉาก 5 (pin แล้วสองที่: `tests/test_lane_a_scene_census.py::OnTheRealDispatcherTests::test_with_the_real_registry_the_evil_port_census_ships_87` และ `tests/test_world_population_bg0005.py` ระดับ composer) · ชั้นจอ: เห็นตัวละคร/มอนสเตอร์ยืนอยู่ในเมืองท่าหรือไม่ นับคร่าว ๆ พอ ไม่ต้องครบ 87
ATTENDED: ตัวตัดสินใบคือชั้นจอเท่านั้น (ชั้น wire ปิดไปแล้วโดยเทส ห้ามใช้แทนตา): เห็นสิ่งมีชีวิตขึ้นจอ = ตอบว่าใช่ · **เมืองว่างเปล่าไม่มีอะไรเลย = ผลลบที่มีค่า บันทึกเป็นผล ไม่ใช่ FAIL** (ใบตาคู่แรกของฉากนี้) · คำถามคือ "มีสิ่งมีชีวิตขึ้นจอไหม" ไม่ใช่ "มันโจมตีไหม" -- มอนไม่ก้าวร้าวเป็นพฤติกรรมที่คาดไว้เพราะ composer ตั้งใจไม่ส่ง faction bit ไม่ใช่ FAIL
ATTENDED: บูตปกติ ใบนี้ไม่ระบุแฟล็ก/env/ทรีพิเศษใด ๆ ⇒ ไม่มีแฟล็ก `--*-scenario` · ทรีต้องมี composer `world_population_bg0005.py`/`world_bg0005_identity.py` และทะเบียนแถว `n_id: 5` ที่ `login_entry_allowed=true` (เข้าฉากไม่ได้เลย = NO-RESULT ไม่ใช่ FAIL) · teardown ต้องรันเสมอแม้รอบจบเพราะเลิกเล่นเฉย ๆ
ATTENDED: ข้อที่ใบสั่งให้บันทึกแยก ไม่ใช่ FAIL: จุดเกิด `MARKER[5]` ยังเป็นชั้น `authored` ห่างจาก placement ที่ใกล้สุด 564.3 หน่วย -- ถ้าตกในหิน/หลุดพื้นให้จดเป็นข้อมูลแยก (ใบนี้ถามว่ามี actor ไหม ไม่ได้ถามว่าพื้นดีไหม) · จดสีป้ายชื่อทุกป้ายทุกภาพจาก full-res (`none` ถ้าไม่มี ห้ามอนุมานสาเหตุ) · กล้อง/NO-CRASH ใช้คลิกขวาค้างลากเท่านั้น ห้าม `Q`/`E`

> เปิดโดย LANE-A (สาย A · WORLD) รอบ `l03cgh`, 2026-08-31T14:xx+07:00 · `login_entry_allowed` ของฉาก 5
> พลิกเป็น `true` รอบนี้ (`COO-DECISION 20260830_1441`, ประตูที่สามในคิวเดียวกับฉาก 4/10; composer
> `world_population_bg0005.py`/`world_bg0005_identity.py` **สร้าง ผูก และเปิดประตูในรอบเดียวกัน** ต่างจาก
> ฉาก 4/10 ที่แยกสามรอบ -- เหตุผล: เทสทั่วไป (`tests/test_lane_a_scene_census.py::
> ComposerContractTests`) สมมติไว้แล้วว่าทุกฉากที่ lane นี้ผูก census ให้ต้องเปิดด้วย เพราะฉาก 4/10/14
> เปิดหมดแล้วตอนรอบนี้เริ่ม) -- ไม่ใช่สำเนาของ `GT-166` เพราะฉากนี้**ไม่มี**ความเสี่ยงแบบ `GT-166`: ทะเบียนเอง
> ไม่ระบุฉากนี้ใน `table_row_differences.the_two_interiors` (ตรวจแล้ว ไม่ใช่สมมติ) -- รูปแบบเดียวกับ `GT-165`
> (ฉาก 4)

### objective (claim เดียว)
ล็อกอินเข้าฉาก 5 จริงแล้ว **เห็นตัวละคร/มอนสเตอร์ยืนอยู่ในเมืองท่า** (ไม่ใช่เมืองว่างเปล่า) ใช่หรือไม่ --
คำถามคือ "มีสิ่งมีชีวิตขึ้นจอไหม" ไม่ใช่ "มันโจมตีไหม": composer ของฉากนี้**ตั้งใจไม่ส่ง faction bit เลย** (ดู
`world_population_bg0005.py` docstring -- เป็นคำตัดสินของสาย B ที่ยังไม่ทำ) จึงไม่มีความเสี่ยงแบบ `GT-134`
ที่มอนไม่ก้าวร้าว -- นั่นเป็นพฤติกรรมที่คาดไว้ ไม่ใช่ FAIL ของใบนี้

### ทางเข้า
ไม่มี production path ใดเขียนแถว character ให้ชื่อฉาก 5 เอง (ดู `login_entry_allowed_because` ในทะเบียน) --
เข้าได้เฉพาะ staged GM account (`config/gm_login_scene.json`, scene_id=5) หรือ GM `/warp 5`

### สิ่งที่ยังไม่วัด (บันทึกไว้ล่วงหน้า ไม่ใช่คำทำนายว่าจะพัง)
จุดเกิด `MARKER[5]` ยังเป็นชั้นหลักฐาน `authored` เท่านั้น -- ไม่เคยมีไคลเอนต์ยืนจริง, ห่างจาก placement
ที่ใกล้ที่สุด 564.3 หน่วย (`table_row_differences.marker_geometry_measured_not_enforced`) -- ถ้าตกในหิน/หลุด
พื้น ให้บันทึกเป็นข้อมูลแยก ไม่ใช่ FAIL ของใบนี้ (คำถามของใบนี้คือมี actor ไหม ไม่ใช่พื้นดีไหม)

### pass criteria — สองชั้น
**wire/DB (ปิดแล้วโดยเทส):** console line `WORLD_CENSUS_BG0005 assembled=87/92 ...` ปรากฏหลังล็อกอินเข้าฉาก 5
-- pin ไว้แล้ว `tests/test_lane_a_scene_census.py::OnTheRealDispatcherTests::
test_with_the_real_registry_the_evil_port_census_ships_87` (เทสเต็มรูปแบบ boot+login+START_GAME+
TargetPosVital ผ่าน dispatcher จริง) และ `tests/test_world_population_bg0005.py` (เทสระดับ composer ตรง)
**client-observable (ยังไม่มีใครยืนดู -- นี่คือสิ่งที่ใบนี้ต้องการ):** ผู้เทสเข้าฉาก 5 จริงแล้วรายงานว่าเห็น
actor ขึ้นจอหรือไม่ (นับคร่าว ๆ พอ ไม่ต้องนับให้ครบ 87)

### สัญญาผู้บริโภค
เปิดโดย LANE-A -- LANE-A บริโภคผลเอง ปิดหัวใบเมื่อผู้เทสยืนยันด้วยตา

### links
`scenarios/world_scene_registry_001.json` แถว `n_id: 5` (`login_entry_allowed_because`) ·
`src/pirateforce_foundation/world_population_bg0005.py`, `world_bg0005_identity.py` ·
`notes_to_chief/20260830_1441_COO-DECISION-scene4-slave-market-first-door.md` · `GT-165` (scene 4, same
shape) · `GT-166` (scene 10, same shape plus the geometry risk this scene does not carry) · `GT-134`
(scene 14, same shape)

## GT-172 GM-003 CHAT-WARP-CROSS-SCENE-LIVE-TELEPORT-001 [attended, in-game]: GM พิมพ์ `/warp <ฉากอื่น> x y` ในกล่องแชท -- จอเปลี่ยนไปฉากปลายทางจริงกลางเซสชันไหม (ไม่ต้อง relog)  [✅ **PASS ทั้งสองชั้น... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕 GT-173 OCEAN-WALLED-CITY-FIRST-EYES-001 [attended, in-game]: ฉาก 6 (Bg0006, Ocean Walled City) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเจกต์ในฉากนี้  [READY]

ATTENDED: บูตตาม `ATTENDED_SESSION_RUNBOOK.md` บน DB สำเนา run-copy ของ `state\pirateforce.sqlite3` เท่านั้น (ห้ามเปิด canonical) เก็บคอนโซล `2>&1` -> เข้าฉาก 6 (`Bg0006` Ocean Walled City) ด้วยทางใดทางหนึ่งที่ใบเขียนไว้เท่านั้น: บัญชี GM staged (`config/gm_login_scene.json`, scene_id=6) หรือพิมพ์ `/warp 6` (คลิกช่องแชทยืนยัน focus ก่อนพิมพ์) -> รอจอนิ่ง กวาดสายตารอบเมืองกำแพงทะเล ถ่ายภาพนิ่งเต็มความละเอียด
ATTENDED: ชั้น wire/DB: หาบรรทัดคอนโซล `WORLD_CENSUS_BG0006 assembled=66/80 ...` หลังล็อกอินเข้าฉาก 6 (pin แล้วสองที่: `tests/test_lane_a_scene_census.py::OceanWalledCityRegistrationTests::test_the_real_registry_now_composes_and_that_is_the_round` และ `tests/test_world_population_bg0006.py` ระดับ composer) · ชั้นจอ: เห็นตัวละคร/มอนสเตอร์ยืนอยู่ในเมืองกำแพงทะเลหรือไม่ นับคร่าว ๆ พอ ไม่ต้องครบ 66
ATTENDED: ตัวตัดสินใบคือชั้นจอเท่านั้น (ชั้น wire ปิดไปแล้วโดยเทส ห้ามใช้แทนตา): เห็นสิ่งมีชีวิตขึ้นจอ = ตอบว่าใช่ · **เมืองว่างเปล่าไม่มีอะไรเลย = ผลลบที่มีค่า บันทึกเป็นผล ไม่ใช่ FAIL** (ใบตาคู่แรกของฉากนี้) · คำถามคือ "มีสิ่งมีชีวิตขึ้นจอไหม" ไม่ใช่ "มันโจมตีไหม" -- มอนไม่ก้าวร้าวเป็นพฤติกรรมที่คาดไว้เพราะ composer ตั้งใจไม่ส่ง faction bit ไม่ใช่ FAIL
ATTENDED: บูตปกติ ใบนี้ไม่ระบุแฟล็ก/env/ทรีพิเศษใด ๆ ⇒ ไม่มีแฟล็ก `--*-scenario` · ทรีต้องมี composer `world_population_bg0006.py`/`world_bg0006_identity.py` และทะเบียนแถว `n_id: 6` ที่ `login_entry_allowed=true` (เข้าฉากไม่ได้เลย = NO-RESULT ไม่ใช่ FAIL) · teardown ต้องรันเสมอแม้รอบจบเพราะเลิกเล่นเฉย ๆ
ATTENDED: สองข้อที่ใบสั่งให้บันทึกแยก ไม่ใช่ FAIL: (1) `MARKER[6]` ยังเป็นชั้น `authored` ห่าง placement ที่ใกล้สุด 772.0 หน่วย -- ตกในหิน/หลุดพื้นให้จดเป็นข้อมูลแยก (ใบนี้ถามว่ามี actor ไหม ไม่ใช่พื้นดีไหม) (2) ฉากนี้มี 3 leader ที่ composer ข้ามไปตั้งแต่ต้นเพราะชื่อ `MOBS_TIP.s_NAME` เป็นอักษรจีนเข้ารหัส cp874 ไม่ได้ -- ไม่ใช่สิ่งที่ผู้เทสจะเห็นหายไปกลางจอ · จดสีป้ายชื่อทุกป้ายทุกภาพจาก full-res (`none` ถ้าไม่มี ห้ามอนุมานสาเหตุ) · กล้อง/NO-CRASH ใช้คลิกขวาค้างลากเท่านั้น ห้าม `Q`/`E`

> เปิดโดย LANE-A (สาย A · WORLD) รอบ `fx0007`, 2026-08-31T17:xx+07:00 · `login_entry_allowed` ของฉาก 6
> พลิกเป็น `true` รอบนี้ (`COO-DECISION 20260830_1441`, ประตูที่สี่ในคิวเดียวกับฉาก 4/5/10; composer
> `world_population_bg0006.py`/`world_bg0006_identity.py` **สร้าง ผูก และเปิดประตูในรอบเดียวกัน** เหมือน
> ฉาก 5 (รอบ `l03cgh`) -- เหตุผลเดียวกัน: เทสทั่วไป (`tests/test_lane_a_scene_census.py::
> ComposerContractTests`) สมมติไว้แล้วว่าทุกฉากที่ lane นี้ผูก census ให้ต้องเปิดด้วย เพราะฉาก 4/5/10/14
> เปิดหมดแล้วตอนรอบนี้เริ่ม) -- ไม่ใช่สำเนาของ `GT-166` เพราะฉากนี้**ไม่มี**ความเสี่ยงแบบ `GT-166`: ทะเบียนเอง
> ไม่ระบุฉากนี้ใน `table_row_differences.the_two_interiors` (ตรวจแล้ว ไม่ใช่สมมติ) -- รูปแบบเดียวกับ `GT-165`
> (ฉาก 4) / `GT-171` (ฉาก 5)

### objective (claim เดียว)
ล็อกอินเข้าฉาก 6 จริงแล้ว **เห็นตัวละคร/มอนสเตอร์ยืนอยู่ในเมืองกำแพงทะเล** (ไม่ใช่เมืองว่างเปล่า) ใช่หรือไม่ --
คำถามคือ "มีสิ่งมีชีวิตขึ้นจอไหม" ไม่ใช่ "มันโจมตีไหม": composer ของฉากนี้**ตั้งใจไม่ส่ง faction bit เลย** (ดู
`world_population_bg0006.py` docstring -- เป็นคำตัดสินของสาย B ที่ยังไม่ทำ) จึงไม่มีความเสี่ยงแบบ `GT-134`
ที่มอนไม่ก้าวร้าว -- นั่นเป็นพฤติกรรมที่คาดไว้ ไม่ใช่ FAIL ของใบนี้

### ทางเข้า
ไม่มี production path ใดเขียนแถว character ให้ชื่อฉาก 6 เอง (ดู `login_entry_allowed_because` ในทะเบียน) --
เข้าได้เฉพาะ staged GM account (`config/gm_login_scene.json`, scene_id=6) หรือ GM `/warp 6`

### สิ่งที่ยังไม่วัด (บันทึกไว้ล่วงหน้า ไม่ใช่คำทำนายว่าจะพัง)
1. จุดเกิด `MARKER[6]` ยังเป็นชั้นหลักฐาน `authored` เท่านั้น -- ไม่เคยมีไคลเอนต์ยืนจริง, ห่างจาก placement
   ที่ใกล้ที่สุด 772.0 หน่วย (`table_row_differences.marker_geometry_measured_not_enforced`) -- ถ้าตกในหิน/
   หลุดพื้น ให้บันทึกเป็นข้อมูลแยก ไม่ใช่ FAIL ของใบนี้ (คำถามของใบนี้คือมี actor ไหม ไม่ใช่พื้นดีไหม)
2. ฉากนี้มี 3 leader ที่ถูกตัดออกด้วยเหตุผลใหม่ (ชื่อ `MOBS_TIP.s_NAME` เป็นอักษรจีน cp874 เข้ารหัสไม่ได้ --
   ดู `world_bg0006_identity.py` docstring) -- ไม่ใช่ FAIL ของใบนี้เช่นกัน (composer ข้ามไปแล้วตั้งแต่ต้น
   ไม่ใช่สิ่งที่ผู้เทสจะเห็นหายไปกลางจอ)

### pass criteria — สองชั้น
**wire/DB (ปิดแล้วโดยเทส):** console line `WORLD_CENSUS_BG0006 assembled=66/80 ...` ปรากฏหลังล็อกอินเข้าฉาก 6
-- pin ไว้แล้ว `tests/test_lane_a_scene_census.py::OceanWalledCityRegistrationTests::
test_the_real_registry_now_composes_and_that_is_the_round` และ `tests/test_world_population_bg0006.py`
(เทสระดับ composer ตรง)
**client-observable (ยังไม่มีใครยืนดู -- นี่คือสิ่งที่ใบนี้ต้องการ):** ผู้เทสเข้าฉาก 6 จริงแล้วรายงานว่าเห็น
actor ขึ้นจอหรือไม่ (นับคร่าว ๆ พอ ไม่ต้องนับให้ครบ 66)

### สัญญาผู้บริโภค
เปิดโดย LANE-A -- LANE-A บริโภคผลเอง ปิดหัวใบเมื่อผู้เทสยืนยันด้วยตา

### links
`scenarios/world_scene_registry_001.json` แถว `n_id: 6` (`login_entry_allowed_because`) ·
`src/pirateforce_foundation/world_population_bg0006.py`, `world_bg0006_identity.py` ·
`notes_to_chief/20260830_1441_COO-DECISION-scene4-slave-market-first-door.md` · `GT-165` (scene 4, same
shape) · `GT-171` (scene 5, same shape) · `GT-166` (scene 10, same shape plus the geometry risk this
scene does not carry) · `GT-134` (scene 14, same shape)

**หมายเหตุผู้เขียนใบนี้:** ควรเขียนผ่านเอเจนต์ `pf-queue-author` ตามกติกาของโปรเจกต์ แต่ในสภาพแวดล้อม
รอบนี้ไม่มีเครื่องมือสำหรับ spawn subagent ชนิดนั้น จึงเขียนเองตามรูปแบบของใบ `GT-171`/`GT-165` ให้ใกล้เคียง
ที่สุด -- ถ้ารูปแบบผิดจากมาตรฐานให้แก้ได้ตามที่ `pf-queue-author` เห็นสมควรในรอบถัดไป

## 🆕 GT-174 SILVER-HARBOUR-FIRST-EYES-001 [attended, in-game]: ฉาก 8 (Bg0008, Silver Harbour) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเจกต์ในฉากนี้  [READY]

ATTENDED: บูตตาม `ATTENDED_SESSION_RUNBOOK.md` บน DB สำเนา run-copy ของ `state\pirateforce.sqlite3` เท่านั้น (ห้ามเปิด canonical) เก็บคอนโซล `2>&1` -> เข้าฉาก 8 (`Bg0008` Silver Harbour) ด้วยทางใดทางหนึ่งที่ใบเขียนไว้เท่านั้น: บัญชี GM staged (`config/gm_login_scene.json`, scene_id=8) หรือพิมพ์ `/warp 8` (คลิกช่องแชทยืนยัน focus ก่อนพิมพ์) -> รอจอนิ่ง กวาดสายตารอบท่าเรือเงิน ถ่ายภาพนิ่งเต็มความละเอียด
ATTENDED: ชั้น wire/DB: หาบรรทัดคอนโซล `WORLD_CENSUS_BG0008 assembled=69/76 ...` หลังล็อกอินเข้าฉาก 8 (pin แล้วสองที่: `tests/test_lane_a_scene_census.py::SilverHarbourRegistrationTests::test_the_real_registry_now_composes_and_that_is_the_round` และ `tests/test_world_population_bg0008.py` ระดับ composer) · ชั้นจอ: เห็นตัวละคร/มอนสเตอร์ยืนอยู่ในท่าเรือเงินหรือไม่ นับคร่าว ๆ พอ ไม่ต้องครบ 69
ATTENDED: ตัวตัดสินใบคือชั้นจอเท่านั้น (ชั้น wire ปิดไปแล้วโดยเทส ห้ามใช้แทนตา): เห็นสิ่งมีชีวิตขึ้นจอ = ตอบว่าใช่ · **ท่าเรือว่างเปล่าไม่มีอะไรเลย = ผลลบที่มีค่า บันทึกเป็นผล ไม่ใช่ FAIL** (ใบตาคู่แรกของฉากนี้) · คำถามคือ "มีสิ่งมีชีวิตขึ้นจอไหม" ไม่ใช่ "มันโจมตีไหม" -- มอนไม่ก้าวร้าวเป็นพฤติกรรมที่คาดไว้เพราะ composer ตั้งใจไม่ส่ง faction bit ไม่ใช่ FAIL
ATTENDED: บูตปกติ ใบนี้ไม่ระบุแฟล็ก/env/ทรีพิเศษใด ๆ ⇒ ไม่มีแฟล็ก `--*-scenario` · ทรีต้องมี composer `world_population_bg0008.py`/`world_bg0008_identity.py` และทะเบียนแถว `n_id: 8` ที่ `login_entry_allowed=true` (เข้าฉากไม่ได้เลย = NO-RESULT ไม่ใช่ FAIL) · teardown ต้องรันเสมอแม้รอบจบเพราะเลิกเล่นเฉย ๆ
ATTENDED: สองข้อที่ใบสั่งให้บันทึกแยก ไม่ใช่ FAIL: (1) `MARKER[8]` ยังเป็นชั้น `authored` แต่ห่าง placement ที่ใกล้สุดเพียง 8.8 หน่วยและอยู่**ภายใน**ขอบเขต placement (แน่นกว่าทุกประตูที่เปิดมาก่อนหน้า) -- ถ้ายังตกในหิน/หลุดพื้นให้จดเป็นข้อมูลแยก (2) ตัวที่ถูกตัด 7 ตัวเป็นเหตุผล "ไม่มีแถว MOBS" หรือ "`s_OUTFIT` ว่าง" เท่านั้น ไม่มีตัวที่ถูกตัดเพราะชื่อไม่ใช่ ASCII แบบฉาก 6 -- composer ข้ามตั้งแต่ต้น ไม่ใช่ของที่หายกลางจอ · จดสีป้ายชื่อทุกป้ายทุกภาพจาก full-res (`none` ถ้าไม่มี ห้ามอนุมานสาเหตุ) · กล้อง/NO-CRASH ใช้คลิกขวาค้างลากเท่านั้น ห้าม `Q`/`E`

> เปิดโดย LANE-A (สาย A · WORLD) รอบ `p4wire`, 2026-08-31T18:xx+07:00 · `login_entry_allowed` ของฉาก 8
> พลิกเป็น `true` รอบนี้ (`COO-DECISION 20260830_1441`, ประตูที่ห้าในคิวเดียวกับฉาก 4/5/6/10; composer
> `world_population_bg0008.py`/`world_bg0008_identity.py` **สร้าง ผูก และเปิดประตูในรอบเดียวกัน** เหมือน
> ฉาก 5/6 (รอบ `l03cgh`/`fx0007`) -- เหตุผลเดียวกัน: เทสทั่วไป (`tests/test_lane_a_scene_census.py::
> ComposerContractTests`) สมมติไว้แล้วว่าทุกฉากที่ lane นี้ผูก census ให้ต้องเปิดด้วย เพราะฉาก 4/5/6/10/14
> เปิดหมดแล้วตอนรอบนี้เริ่ม) -- ไม่ใช่สำเนาของ `GT-166` เพราะฉากนี้**ไม่มี**ความเสี่ยงแบบ `GT-166`: ทะเบียนเอง
> ไม่ระบุฉากนี้ใน `table_row_differences.the_two_interiors` (ตรวจแล้ว ไม่ใช่สมมติ) -- รูปแบบเดียวกับ `GT-165`
> (ฉาก 4) / `GT-171` (ฉาก 5) / `GT-173` (ฉาก 6)

### objective (claim เดียว)
ล็อกอินเข้าฉาก 8 จริงแล้ว **เห็นตัวละคร/มอนสเตอร์ยืนอยู่ในท่าเรือเงิน** (ไม่ใช่ท่าเรือว่างเปล่า) ใช่หรือไม่ --
คำถามคือ "มีสิ่งมีชีวิตขึ้นจอไหม" ไม่ใช่ "มันโจมตีไหม": composer ของฉากนี้**ตั้งใจไม่ส่ง faction bit เลย** (ดู
`world_population_bg0008.py` docstring -- เป็นคำตัดสินของสาย B ที่ยังไม่ทำ) จึงไม่มีความเสี่ยงแบบ `GT-134`
ที่มอนไม่ก้าวร้าว -- นั่นเป็นพฤติกรรมที่คาดไว้ ไม่ใช่ FAIL ของใบนี้

### ทางเข้า
ไม่มี production path ใดเขียนแถว character ให้ชื่อฉาก 8 เอง (ดู `login_entry_allowed_because` ในทะเบียน) --
เข้าได้เฉพาะ staged GM account (`config/gm_login_scene.json`, scene_id=8) หรือ GM `/warp 8`

### สิ่งที่ยังไม่วัด (บันทึกไว้ล่วงหน้า ไม่ใช่คำทำนายว่าจะพัง)
1. จุดเกิด `MARKER[8]` ยังเป็นชั้นหลักฐาน `authored` เท่านั้น -- ไม่เคยมีไคลเอนต์ยืนจริง แต่ห่างจาก placement
   ที่ใกล้ที่สุดเพียง 8.8 หน่วยและอยู่**ภายใน**ขอบเขต placement (`table_row_differences.
   marker_geometry_measured_not_enforced`) -- แน่นกว่าทุกประตูที่เปิดมาก่อนหน้านี้ -- ถ้าตกในหิน/หลุดพื้น
   ให้บันทึกเป็นข้อมูลแยก ไม่ใช่ FAIL ของใบนี้ (คำถามของใบนี้คือมี actor ไหม ไม่ใช่พื้นดีไหม)
2. ฉากนี้ไม่มี leader ที่ถูกตัดเพราะชื่อไม่ใช่ ASCII (ต่างจากฉาก 6) -- ตัวที่ถูกตัด 7 ตัวทั้งหมดเป็นเหตุผล
   "ไม่มีแถว MOBS" หรือ "s_OUTFIT ว่าง" เท่านั้น (ดู `world_bg0008_identity.py` docstring) -- ไม่ใช่ FAIL
   ของใบนี้เช่นกัน (composer ข้ามไปแล้วตั้งแต่ต้น ไม่ใช่สิ่งที่ผู้เทสจะเห็นหายไปกลางจอ)

### pass criteria — สองชั้น
**wire/DB (ปิดแล้วโดยเทส):** console line `WORLD_CENSUS_BG0008 assembled=69/76 ...` ปรากฏหลังล็อกอินเข้าฉาก 8
-- pin ไว้แล้ว `tests/test_lane_a_scene_census.py::SilverHarbourRegistrationTests::
test_the_real_registry_now_composes_and_that_is_the_round` และ `tests/test_world_population_bg0008.py`
(เทสระดับ composer ตรง)
**client-observable (ยังไม่มีใครยืนดู -- นี่คือสิ่งที่ใบนี้ต้องการ):** ผู้เทสเข้าฉาก 8 จริงแล้วรายงานว่าเห็น
actor ขึ้นจอหรือไม่ (นับคร่าว ๆ พอ ไม่ต้องนับให้ครบ 69)

### สัญญาผู้บริโภค
เปิดโดย LANE-A -- LANE-A บริโภคผลเอง ปิดหัวใบเมื่อผู้เทสยืนยันด้วยตา

### links
`scenarios/world_scene_registry_001.json` แถว `n_id: 8` (`login_entry_allowed_because`) ·
`src/pirateforce_foundation/world_population_bg0008.py`, `world_bg0008_identity.py` ·
`notes_to_chief/20260830_1441_COO-DECISION-scene4-slave-market-first-door.md` · `GT-165` (scene 4, same
shape) · `GT-171` (scene 5, same shape) · `GT-173` (scene 6, same shape) · `GT-166` (scene 10, same shape
plus the geometry risk this scene does not carry) · `GT-134` (scene 14, same shape)

**หมายเหตุผู้เขียนใบนี้:** ควรเขียนผ่านเอเจนต์ `pf-queue-author` ตามกติกาของโปรเจกต์ แต่ในสภาพแวดล้อม
รอบนี้ไม่มีเครื่องมือสำหรับ spawn subagent ชนิดนั้น จึงเขียนเองตามรูปแบบของใบ `GT-173`/`GT-171` ให้ใกล้เคียง
ที่สุด -- ถ้ารูปแบบผิดจากมาตรฐานให้แก้ได้ตามที่ `pf-queue-author` เห็นสมควรในรอบถัดไป

## 🆕 GT-175 SPICE-PARADISE-FIRST-EYES-001 [attended, in-game]: ฉาก 3 (Bg0003, Spice Paradise Island) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเ... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## 🆕 GT-176 VOODOO-ISLAND-FIRST-EYES-001 [attended, in-game]: ฉาก 7 (Bg0007, Voodoo Island) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเจกต์ในฉากนี้  [READY]

ATTENDED: บูตตาม `ATTENDED_SESSION_RUNBOOK.md` บน DB สำเนา run-copy ของ `state\pirateforce.sqlite3` เท่านั้น (ห้ามเปิด canonical) เก็บคอนโซล `2>&1` -> เข้าฉาก 7 (`Bg0007` Voodoo Island) ด้วยทางใดทางหนึ่งที่ใบเขียนไว้เท่านั้น: บัญชี GM staged (`config/gm_login_scene.json`, scene_id=7) หรือพิมพ์ `/warp 7` (คลิกช่องแชทยืนยัน focus ก่อนพิมพ์) -> รอจอนิ่ง กวาดสายตารอบเกาะวูดู ถ่ายภาพนิ่งเต็มความละเอียด
ATTENDED: ชั้น wire/DB: หาบรรทัดคอนโซล `WORLD_CENSUS_BG0007 assembled=56/68 ...` หลังล็อกอินเข้าฉาก 7 (pin แล้วสองที่: `tests/test_lane_a_scene_census.py::VoodooIslandRegistrationTests::test_the_real_registry_now_composes_and_that_is_the_round` และ `tests/test_world_population_bg0007.py` ระดับ composer) · ชั้นจอ: เห็นตัวละคร/มอนสเตอร์ยืนอยู่บนเกาะวูดูหรือไม่ นับคร่าว ๆ พอ ไม่ต้องครบ 56
ATTENDED: ตัวตัดสินใบคือชั้นจอเท่านั้น (ชั้น wire ปิดไปแล้วโดยเทส ห้ามใช้แทนตา): เห็นสิ่งมีชีวิตขึ้นจอ = ตอบว่าใช่ · **เกาะว่างเปล่าไม่มีอะไรเลย = ผลลบที่มีค่า บันทึกเป็นผล ไม่ใช่ FAIL** (ใบตาคู่แรกของฉากนี้) · คำถามคือ "มีสิ่งมีชีวิตขึ้นจอไหม" ไม่ใช่ "มันโจมตีไหม" -- มอนไม่ก้าวร้าวเป็นพฤติกรรมที่คาดไว้เพราะ composer ตั้งใจไม่ส่ง faction bit ไม่ใช่ FAIL
ATTENDED: บูตปกติ ใบนี้ไม่ระบุแฟล็ก/env/ทรีพิเศษใด ๆ ⇒ ไม่มีแฟล็ก `--*-scenario` · ทรีต้องมี composer `world_population_bg0007.py`/`world_bg0007_identity.py` และทะเบียนแถว `n_id: 7` ที่ `login_entry_allowed=true` (เข้าฉากไม่ได้เลย = NO-RESULT ไม่ใช่ FAIL) · teardown ต้องรันเสมอแม้รอบจบเพราะเลิกเล่นเฉย ๆ
ATTENDED: สามข้อที่ใบสั่งให้บันทึกแยก ไม่ใช่ FAIL: (1) `MARKER[7]` ยังเป็นชั้น `authored` แม้อยู่ในขอบเขต placement และห่างแค่ 10.793 หน่วย -- ตกในหิน/หลุดพื้นให้จดเป็นข้อมูลแยก (2) ตัวที่ถูกตัด 12 ตัวเป็นเหตุผล "ไม่มีแถว MOBS" 2 ตัว (รวม set 111 ที่ leader `n_ID` เป็นศูนย์) และ "`s_OUTFIT` ว่าง" 10 ตัว เท่านั้น (3) 8 sets เป็น multi-variant outfit ตัวละสองตัวแปร ส่งตัวแปรแรกเสมอ -- ตัวละครหน้าตาแปลกไม่ตรงที่คาด ให้จดเป็นข้อมูลแยก · จดสีป้ายชื่อทุกป้ายทุกภาพจาก full-res (`none` ถ้าไม่มี ห้ามอนุมานสาเหตุ) · กล้อง/NO-CRASH ใช้คลิกขวาค้างลากเท่านั้น ห้าม `Q`/`E`

> เปิดโดย LANE-A (สาย A · WORLD) รอบ `78zayw`, 2026-08-31T21:50+07:00 · `login_entry_allowed` ของฉาก 7
> พลิกเป็น `true` รอบนี้ (`COO-DECISION 20260830_1441`, ประตูที่เจ็ดในคิวเดียวกับฉาก 4/5/6/8/10/3; composer
> `world_population_bg0007.py`/`world_bg0007_identity.py` **สร้าง ผูก และเปิดประตูในรอบเดียวกัน** เหมือน
> ฉาก 5/6/8/3 (รอบ `l03cgh`/`fx0007`/`p4wire`/`p7wm17`) -- เหตุผลเดียวกัน: เทสทั่วไป (`tests/test_lane_a_scene_census.py::
> ComposerContractTests`) สมมติไว้แล้วว่าทุกฉากที่ lane นี้ผูก census ให้ต้องเปิดด้วย เพราะฉาก 3/4/5/6/8/10/14
> เปิดหมดแล้วตอนรอบนี้เริ่ม) -- ไม่ใช่สำเนาของ `GT-166` เพราะฉากนี้**ไม่มี**ความเสี่ยงแบบ `GT-166`: ทะเบียนเอง
> ไม่ระบุฉากนี้ใน `table_row_differences.the_two_interiors` (ตรวจแล้ว ไม่ใช่สมมติ) -- รูปแบบเดียวกับ `GT-165`
> (ฉาก 4) / `GT-171` (ฉาก 5) / `GT-173` (ฉาก 6) / `GT-174` (ฉาก 8) / `GT-175` (ฉาก 3) จุดต่างเดียวคือ
> geometry ของฉากนี้แน่นที่สุดที่ lane นี้เคยเปิด: จุดเกิดอยู่ **ห่างจาก placement ที่ใกล้ที่สุดแค่ 10.793 หน่วย
> และอยู่ในขอบเขต placement เอง** (ตรงข้ามกับฉาก 3 ที่ 405.0 หน่วยและอยู่นอกขอบเขต)

### objective (claim เดียว)
ล็อกอินเข้าฉาก 7 จริงแล้ว **เห็นตัวละคร/มอนสเตอร์ยืนอยู่บนเกาะวูดู** (ไม่ใช่เกาะว่างเปล่า) ใช่หรือไม่ --
คำถามคือ "มีสิ่งมีชีวิตขึ้นจอไหม" ไม่ใช่ "มันโจมตีไหม": composer ของฉากนี้**ตั้งใจไม่ส่ง faction bit เลย** (ดู
`world_population_bg0007.py` docstring -- เป็นคำตัดสินของสาย B ที่ยังไม่ทำ) จึงไม่มีความเสี่ยงแบบ `GT-134`
ที่มอนไม่ก้าวร้าว -- นั่นเป็นพฤติกรรมที่คาดไว้ ไม่ใช่ FAIL ของใบนี้

### ทางเข้า
ไม่มี production path ใดเขียนแถว character ให้ชื่อฉาก 7 เอง (ดู `login_entry_allowed_because` ในทะเบียน) --
เข้าได้เฉพาะ staged GM account (`config/gm_login_scene.json`, scene_id=7) หรือ GM `/warp 7`

### สิ่งที่ยังไม่วัด (บันทึกไว้ล่วงหน้า ไม่ใช่คำทำนายว่าจะพัง)
1. จุดเกิด `MARKER[7]` ยังเป็นชั้นหลักฐาน `authored` เท่านั้น -- ไม่เคยมีไคลเอนต์ยืนจริง แม้จะอยู่ในขอบเขต
   placement และห่างแค่ 10.793 หน่วย (`table_row_differences.marker_geometry_measured_not_enforced`)
   ถ้าตกในหิน/หลุดพื้น ให้บันทึกเป็นข้อมูลแยก ไม่ใช่ FAIL ของใบนี้ (คำถามของใบนี้คือมี actor ไหม ไม่ใช่พื้นดีไหม)
2. ฉากนี้ไม่มี leader ที่ถูกตัดเพราะชื่อไม่ใช่ ASCII (ต่างจากฉาก 6) -- ตัวที่ถูกตัด 12 ตัวทั้งหมดเป็นเหตุผล
   "ไม่มีแถว MOBS" (2 ตัว รวม set 111 ที่ leader n_ID เป็นศูนย์) หรือ "s_OUTFIT ว่าง" (10 ตัว) เท่านั้น
   (ดู `world_bg0007_identity.py` docstring) -- ไม่ใช่ FAIL ของใบนี้เช่นกัน (composer ข้ามไปแล้วตั้งแต่ต้น
   ไม่ใช่สิ่งที่ผู้เทสจะเห็นหายไปกลางจอ)
3. ฉากนี้มี 8 sets ที่ multi-variant outfit ทุกตัวมีแค่สองตัวแปร (ต่างจากฉาก 3 ที่มีตัวหนึ่งเก้าตัวแปร) --
   ส่งตัวแปรแรกเสมอตามกติกาเดิม ถ้าตัวละครดูแปลกตาไม่ตรงกับที่คาด ให้บันทึกเป็นข้อมูลแยก ไม่ใช่ FAIL

### pass criteria — สองชั้น
**wire/DB (ปิดแล้วโดยเทส):** console line `WORLD_CENSUS_BG0007 assembled=56/68 ...` ปรากฏหลังล็อกอินเข้าฉาก 7
-- pin ไว้แล้ว `tests/test_lane_a_scene_census.py::VoodooIslandRegistrationTests::
test_the_real_registry_now_composes_and_that_is_the_round` และ `tests/test_world_population_bg0007.py`
(เทสระดับ composer ตรง)
**client-observable (ยังไม่มีใครยืนดู -- นี่คือสิ่งที่ใบนี้ต้องการ):** ผู้เทสเข้าฉาก 7 จริงแล้วรายงานว่าเห็น
actor ขึ้นจอหรือไม่ (นับคร่าว ๆ พอ ไม่ต้องนับให้ครบ 56)

### สัญญาผู้บริโภค
เปิดโดย LANE-A -- LANE-A บริโภคผลเอง ปิดหัวใบเมื่อผู้เทสยืนยันด้วยตา

### links
`scenarios/world_scene_registry_001.json` แถว `n_id: 7` (`login_entry_allowed_because`) ·
`src/pirateforce_foundation/world_population_bg0007.py`, `world_bg0007_identity.py` ·
`notes_to_chief/20260830_1441_COO-DECISION-scene4-slave-market-first-door.md` · `GT-165` (scene 4, same
shape) · `GT-171` (scene 5, same shape) · `GT-173` (scene 6, same shape) · `GT-174` (scene 8, same shape) ·
`GT-175` (scene 3, same shape) · `GT-166` (scene 10, same shape plus the geometry risk this scene does not
carry) · `GT-134` (scene 14, same shape)

**หมายเหตุผู้เขียนใบนี้:** ควรเขียนผ่านเอเจนต์ `pf-queue-author` ตามกติกาของโปรเจกต์ แต่ในสภาพแวดล้อม
รอบนี้ไม่มีเครื่องมือสำหรับ spawn subagent ชนิดนั้น จึงเขียนเองตามรูปแบบของใบ `GT-175`/`GT-174` ให้ใกล้เคียง
ที่สุด -- ถ้ารูปแบบผิดจากมาตรฐานให้แก้ได้ตามที่ `pf-queue-author` เห็นสมควรในรอบถัดไป

## 🆕 GT-177 DEATH-CITY-SEA-FIRST-EYES-001 [attended, in-game]: ฉาก 9 (Bg0009, Death City Sea) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเจกต์ในฉากนี้  [BLOCKED-ON-ATTENDED -- รอ PR ของรอบ `ir0lpw` (`pirate-force-server`, ยังไม่ merge เข้า `main`) merge ก่อน + รอ human ที่มี game client จริง]

> เปิดโดย LANE-A (สาย A · WORLD) รอบ `ir0lpw`, 2026-08-31 · `login_entry_allowed` ของฉาก 9 พลิกเป็น `true`
> รอบนี้ (`COO-DECISION 20260830_1441`, ประตูที่เก้าในคิวเดียวกับฉาก 4/5/6/8/3/10/7; composer
> `world_population_bg0009.py`/`world_bg0009_identity.py` **สร้าง ผูก และเปิดประตูในรอบเดียวกัน** เหมือน
> ฉาก 5/6/8/3/7) -- **ต่างจาก `GT-165`/`GT-171`/`GT-173`/`GT-174`/`GT-175`/`GT-176` ตรงที่โค้ดของรอบนี้ยังไม่
> merge เข้า `main` ณ เวลาที่เขียนใบนี้** (repo `pirate-force-server`, รอบ `ir0lpw` ยังเปิดอยู่) จึงเปิดใบนี้
> เป็น `BLOCKED-ON-ATTENDED` ไม่ใช่ `READY` -- ไม่ใช่สำเนาของ `GT-166` เพราะฉากนี้**ไม่มี**ความเสี่ยงแบบ
> `GT-166`: ทะเบียนเองไม่ระบุฉากนี้ใน `table_row_differences.the_two_interiors` (ตรวจแล้ว ไม่ใช่สมมติ) --
> รูปแบบเดียวกับ `GT-165` (ฉาก 4) / `GT-171` (ฉาก 5) / `GT-173` (ฉาก 6) / `GT-174` (ฉาก 8) / `GT-175`
> (ฉาก 3) / `GT-176` (ฉาก 7)

### objective (claim เดียว)
ล็อกอินเข้าฉาก 9 จริงแล้ว **เห็นตัวละคร/มอนสเตอร์ยืนอยู่ใน Death City Sea** (ไม่ใช่ฉากว่างเปล่า) และไม่โดน
ปฏิเสธล็อกอินเหมือนก่อนรอบ `ir0lpw` ใช่หรือไม่ -- คำถามคือ "มีสิ่งมีชีวิตขึ้นจอไหมและเข้าประตูนี้ได้จริงไหม"
ไม่ใช่ "มันโจมตีไหม": composer ของฉากนี้**ตั้งใจไม่ส่ง faction bit เลย** (ดู `world_population_bg0009.py`
docstring -- เป็นคำตัดสินของสาย B ที่ยังไม่ทำ) จึงไม่มีความเสี่ยงแบบ `GT-134` ที่มอนไม่ก้าวร้าว -- นั่นเป็น
พฤติกรรมที่คาดไว้ ไม่ใช่ FAIL ของใบนี้

### ทางเข้า
ไม่มี production path ใดเขียนแถว character ให้ชื่อฉาก 9 เอง (ดู `login_entry_allowed_because` ในทะเบียน) --
เข้าได้เฉพาะ staged GM account (`config/gm_login_scene.json`, scene_id=9) หรือ GM `/warp 9` -- ทั้งสองทาง
ต้องรอ PR ของรอบ `ir0lpw` merge เข้า `main` ก่อนถึงจะบูตได้จริง

### สิ่งที่ยังไม่วัด (บันทึกไว้ล่วงหน้า ไม่ใช่คำทำนายว่าจะพัง)
1. Placement จริงของฉากนี้มี 63 ตัว แต่ composer ประกอบ (assemble) ได้ 57 ตัว (6 ตัวไม่มีร่างที่ส่งได้เลยไม่ถูก
   ส่ง -- ดู `world_bg0009_identity.py` docstring สำหรับเหตุผลแยกแต่ละตัว) -- การเห็น "น้อยกว่า 63" ไม่ใช่ FAIL
   ของใบนี้ คำถามของใบนี้คือมี actor ไหม ไม่ใช่ครบ 63 ไหม
2. จุดเกิด `MARKER[9]` = `(2129, 20907, 240)` ยังเป็นชั้นหลักฐาน `authored` เท่านั้น --
   `never_sent_to_any_client_by_this_project` (ไม่เคยมีไคลเอนต์ยืนจริงมาก่อนแม้แต่ครั้งเดียว) ห่างจาก
   placement จริงที่ใกล้ที่สุด **2198.81 หน่วย** -- กว้างที่สุดในบรรดาประตูที่เลนนี้เปิดมา (กว้างกว่าฉาก 7's
   10.793 และฉาก 8's 8.818 มาก) แม้จะยัง "อยู่ในขอบเขต placement" ตามทะเบียน (bounding box กว้างมาก ไม่ใช่
   หลักประกันว่าพื้นดี) -- ผู้เทส**ต้องรายงานผลข้อนี้แยกเป็นบรรทัดของตัวเองไม่ว่าจะยืนได้หรือไม่ได้** เพราะเป็น
   ข้อมูลใหม่ที่ยังไม่มีใครวัด และเป็นช่องว่างกว้างที่สุดเท่าที่เลนนี้เคยเปิดประตูมา

### pass criteria — สองชั้น
**wire/DB (ยังไม่ปิดโดยเทส -- รอ PR ของรอบ `ir0lpw` merge เข้า `main` ก่อน):** console line
`WORLD_CENSUS_BG0009 assembled=57/63 ...` ต้องปรากฏหลังล็อกอินเข้าฉาก 9 -- ดูรูปแบบ log จาก composer
`world_population_bg0009.py` และ console reader `tests/test_lane_a_scene_census.py` (รูปแบบเดียวกับที่
`GT-165`/`GT-171`/`GT-173`/`GT-174`/`GT-175`/`GT-176` ใช้ปิด) -- เทสที่ pin ตัวเลขนี้ให้แน่นอนยังไม่ยืนยันว่า
มีอยู่บน `main` ณ ตอนเขียนใบนี้ (ระบุไว้ตรง ๆ เพื่อไม่ให้อ่านผิดว่าปิดแล้ว)
**client-observable (ยังไม่มีใครยืนดู -- นี่คือสิ่งที่ใบนี้ต้องการ):** ผู้เทสเข้าฉาก 9 จริงแล้วรายงานว่าเห็น
actor ขึ้นจอหรือไม่ (นับคร่าว ๆ พอ ไม่ต้องนับให้ครบ 57) และล็อกอินผ่านได้ปกติ ไม่โดนปฏิเสธเหมือนก่อนรอบ
`ir0lpw` -- พร้อมรายงานแยกบรรทัดว่ายืนบน `MARKER[9]` ได้ปกติหรือไม่ (ไม่ตกขอบแมพ/ไม่ค้างกำแพง/ไม่ตกน้ำแบบ
ผิดปกติ) ตามข้อ 2 ของ "สิ่งที่ยังไม่วัด" ข้างต้น (ข้อมูลใหม่ ไม่ใช่เงื่อนไขบล็อก PASS ของ objective หลัก แต่
สำคัญกว่าปกติเพราะช่องว่าง 2198.81 หน่วยกว้างที่สุดเท่าที่เคยเปิดมา)

### nonclaims
ใบนี้ไม่พิสูจน์ว่า placement ทั้ง 63 ตัวถูกต้อง (พิสูจน์แค่ assembled=57 ที่ composer ตั้งใจส่ง), ไม่พิสูจน์ว่า
มอนก้าวร้าว/ไม่ก้าวร้าว (composer ตัดสินใจไม่ส่ง faction bit ไปแล้วนอกใบนี้), และไม่พิสูจน์อะไรเกี่ยวกับ
`MARKER[9]` เกินกว่า "ยืนได้/ไม่ได้ในบูตนี้" -- ไม่ใช่การรับรองว่าจุดนี้จะยืนได้ทุกครั้งหรือหลัง reset

### สัญญาผู้บริโภค
เปิดโดย LANE-A -- LANE-A บริโภคผลเอง ปิดหัวใบเมื่อผู้เทสยืนยันด้วยตา ตามหลัง PR ของรอบ `ir0lpw` merge แล้ว
เท่านั้น

### links
`scenarios/world_scene_registry_001.json` แถว `n_id: 9` (`table_row_differences.login_entry_allowed_because`) ·
`src/pirateforce_foundation/world_population_bg0009.py`, `world_bg0009_identity.py` ·
`rounds/A_ir0lpw...md` (repo `pirate-force-server`, จะ push พร้อมกับ PR ของรอบ `ir0lpw`) ·
`notes_to_chief/20260830_1441_COO-DECISION-scene4-slave-market-first-door.md` ·
`GT-165` (scene 4, same shape) · `GT-171` (scene 5, same shape) · `GT-173` (scene 6, same shape) ·
`GT-174` (scene 8, same shape) · `GT-175` (scene 3, same shape) ·
`GT-176` (scene 7, same shape, closest marker-tightness precedent 10.793 units) ·
`GT-166` (scene 10, dual-objective shape used only when marker risk is elevated -- not this scene's case,
despite the wide 2198.81-unit gap) · `GT-134` (scene 14, same shape)


## GT-178 BG0015-HOSTILE-TWELVE-AGGRO-001 [attended, in-game] [🔴 **NEGATIVE-MEASURED — R322C** 2026-09-07T01:48+07:00 (roster=11 backed=11 แต่ไม่มี `MOB_AI_TICK_LIVE` ฉาก 14 ทั้งเซสชัน — register ตัวใหม่ตอนมาถึงทำไว้แค่ฉาก 1/2 ⇒ มอนไม่ทำอะไรเลย · แม้ในฉาก 1 ที่ tick เดิน `idle->aggro intent=attack_undeliverable` = โกรธแล้วแต่ส่งโจมตีกลับหาผู้เล่นไม่ได้) · ใบสร้างเสนอของ B (M4): (ก) ทุกฉากที่มี roster สร้าง `MobAiRegister` เองตอนผู้เล่นมาถึง+tick เดิน พิสูจน์ headless ก่อนเรียกเจ้าของ (ข) ต่อสายมอนตีผู้เล่น (attack_undeliverable → deliver) · ผลเต็ม `notes_to_chief/20260907_0158_KA1A-R322C-RESULTS-*.md` (`OBSERVER_CONFIRMED 2026-09-07T01:48+07:00`) · พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00]: ของ 81 ตัวที่ขึ้นจอในฉาก 14

> 🔴 **แก้โดย chief (LANE-E) รอบ `pv4zg1`/R352 2026-09-05T11:1x+07:00 ตามใบ `notes_to_chief/20260905_0845_LANE-B-TO-CHIEF-gt178-control-command-now-reports-12-but-11-ship.md`** — `#803` บน main กันหนึ่ง placement (87 · template 924 · คาร์ลอส · `0x2058`) ออกจากสิ่งที่สาย B ส่ง ตาม `COO-DECISION 20260905_0545` ⇒ **สิ่งที่ splice เป็นศัตรูจริงตอนนี้มี 11 ตัว ไม่ใช่ 12 · ตัวที่เหลือของฉากเป็น 70 ไม่ใช่ 69** · [วัดแล้ว chief รอบเดียวกัน บน `origin/main` ของ pirate-force-server]: `scene14_hostile_roster()` = **12 แถว** (ตัววินิจฉัย ตั้งใจให้เห็นคาร์ลอสต่อไป) · `scene14_shipped_hostile_roster()` = **11 แถว** · ส่วนต่าง = placement `87` เท่านั้น
> 🔴 **placement 87 นิ่ง = ผลที่คาดไว้ ไม่ใช่ negative ของใบนี้** — เรากันเขาออกเอง ห้ามนับรวมในข้อ "negative มีค่าเท่ากับ positive" และห้าม redirect ไป `RE-067`/`mob_aggro.py` เพราะตัวนี้ตัวเดียว

> 🔴 **ไม่ยกเลิก · ต่อคิวหลัง `GT-224`** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` ข้อ ④ ที่เจ้าของยกใบนี้เป็นตัวอย่างเอง) — R306/R307 วัด `roster=0` บนฉาก 14 ⇒ ใบนี้ถูก **บล็อก** ไม่ใช่ถูก **ตอบ** · ต้นเหตุ `roster=0` สองชั้น: (i) register เป็นของฉากก่อนหน้า — chief แก้แล้วรอบนี้ (`_sync_combat_scene_at_edge`, PR เซิร์ฟเวอร์ของรอบ `pk14rf`) (ii) ฉาก 14 ยังไม่ได้ลงทะเบียนตารางมอน — LANE-B ตาม `COO-DECISION 20260903_1942` ข้อ 2 · **ทั้งสองข้อต้องอยู่บน main ก่อน แล้ว `GT-224` ให้ตัวเลขจริงก่อน จึงบูตใบนี้ได้**

(Bg0015, Hell Volcano Island) ที่ GT-134 พิสูจน์แล้วว่าทุกตัว NEUTRAL -- 11 ตัวที่รอบนี้ splice (หลัง `#803` กัน placement 87 ออก)
faction เข้าไปใหม่ เดินเข้าใกล้แล้ว "เข้าตี/อ่านเป็นศัตรู" จริงบนจอหรือไม่ ในขณะที่อีก 70 ตัวยังนิ่ง
เหมือนเดิม  [READY]

> เปิดโดย chief รอบ `gmcj4a` (R274) 2026-08-31 -- CORE-REQUEST ร่วม LANE-A/LANE-B
> (`notes_to_chief/20260831_2151_LANE-A-TO-CHIEF-scene14-hostile-splice-core-request-both-halves-confirmed-built.md`,
> อ้างอิงข้อเสนอ `20260831_2007_LANE-A-TO-LANE-B-*` และคำยืนยัน `20260831_2053_LANE-B-TO-LANE-A-*`)
> ลงจุดเสียบจริงแล้วใน `_roster_handoff` (`src/pirateforce_foundation/world_population_handoff.py:983-998`)
> -- จุดเดียวที่ทั้ง `handoff_for_arrival` (M1-P login) และ `handoff_on_crossing` (M2) เรียกสำหรับ
> source `"bg0015_roster"` ⇒ splice นี้ทำงานทุกครั้งที่ฉาก 14 ถูก compose ไม่ว่าทางไหน
> ไม่ต้องมีจุดเสียบที่สอง (ยืนยันจากโค้ดจริง ไม่ใช่แค่จดหมาย)
> ✅ **[แก้แล้วบน main -- วัดเองโดย chief รอบ `pv4zg1`/R352]** บล็อกเตือน ChooseNPC ข้างล่างนี้ **ล้าสมัยแล้ว** (แจ้งโดย LANE-B ใบ `0845` ข้อ 3 · chief ตรวจซ้ำเองที่ `src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene14.py:259-268` และ `:384` บน `origin/main`): responder อ่าน `field_mob_hostile_bg0015.scene14_shipped_hostile_roster()` แล้ว ⇒ **การคลิก NPC ไม่ลบ hostile splice อีกต่อไป** · ยังคงข้อความเดิมไว้ทั้งบล็อกเป็นประวัติ ห้ามลบ · 🔴 คำสั่ง "ห้ามคลิกก่อนสังเกต" **ยังคงไว้เป็นวินัยการวัด** (คลิกแล้วเปลี่ยนสภาพฉากก่อนถ่ายภาพยังทำให้ผลอ่านยาก) แต่ถ้าเผลอคลิก **ไม่ใช่เหตุให้ทิ้งรอบ** อีกแล้ว
> 🔴 `pf-adversary` ตรวจ diff นี้แล้วรอบนี้ -- **พบ CONFIRMED defect** (ยืนยันด้วยการรัน `respond()`
> จริง ไม่ใช่แค่อ่านโค้ด): `lane_hooks/lane_a_choose_npc_scene14.py`'s ChooseNPC responder ไม่รู้จัก
> hostile splice เลย -- **คลิก NPC ตัวไหนก็ได้ในฉาก 14 (แม้ไม่ใช่ 1 ใน 12 ตัว) จะประกอบ actor ทั้ง 81
> ตัวใหม่แบบพลเรือนล้วนแล้วส่งทับ ลบ hostile splice ของ 11 ตัวทิ้งกลับเป็นพลเรือนทันที** (replace-by-
> omission, RE-092) รายละเอียดเต็ม + ที่ขอให้สาย A แก้:
> `notes_to_chief/20260831_2318_CHIEF-TO-LANE-A-choosenpc-scene14-reverts-hostile-splice-to-civilian.md`
> ⇒ **ผู้เทส: ห้ามคลิก NPC ตัวไหนในฉาก 14 ก่อนสังเกต/ถ่ายภาพพฤติกรรม aggro ของ 11 ตัวที่ส่งจริง**
> ถ้าคลิกไปแล้วเจอว่าทุกตัวนิ่งเหมือนพลเรือน ให้สงสัยข้อนี้ก่อน อย่ารีบสรุปว่า wire tier ผิด (มันถูก
> ยืนยันแล้วด้วยเทส) -- แก้ที่ต้นทาง (ไฟล์ของสาย A) ยังไม่เกิดขึ้น ณ เวลาที่เปิดใบนี้

### สืบต่อ GT-134 (ไม่ปิด ไม่ย้าย ไม่ทับ)
`GT-134` ปิดแล้ว **PASS** สำหรับคำถาม "มีสิ่งมีชีวิตขึ้นจอในฉาก 14 ไหม" (81/91 ขึ้นจอจริง) --
แต่ nonclaim ข้อ 1 ของใบนั้นตอบคำถาม "ก้าวร้าวไหม" ไปแล้วด้วยผลลบ: ทุกตัวเป็น NEUTRAL ไม่ถือ
faction bit เลย ("มอนสเตอร์ที่ไม่เข้าตี = ผลที่คาดไว้ ไม่ใช่ FAIL" -- เจตนาเว้น scope ให้สาย B)
ใบนี้คือใบที่ถามคำถามที่ GT-134 ตั้งใจไม่ตอบ: **เฉพาะ 11 ตัวที่รอบนี้ splice (หลัง `#803` กัน placement 87 ออก) ใหม่** อ่านเป็นศัตรูจริง
บนจอหรือไม่ -- คนละ claim กับ GT-134 ห้ามใช้ผลของใบหนึ่งปิดอีกใบ

ATTENDED: (สรุป <=5 บรรทัด ของ steps/pass criteria เต็มด้านล่าง - เติมโดย LANE-B รอบ `p4ts3e` ตาม R364 ข้อ 2)
  0. 🔴 เงื่อนไขบูต ต้องเช็คก่อนขึ้นรถบัส: ใบนี้ **ต่อคิวหลัง `GT-224`** (หัวใบข้างบน) - `GT-224` ต้องให้ตัวเลข roster ของฉาก 14 มาก่อน ·
     ถ้าบูตแล้ว console ขึ้น `roster=0` **หยุด ไม่ใช่ FAIL** (คือตัวบล็อกเดิม R306/R307 ไม่ใช่คำตอบของใบนี้) - จดแล้วคืน slot
  1. ก่อนบูต: รันบล็อก `py -3 -c ...` ในหัวข้อ "เกณฑ์ตัวคุม" จากเชลล์ repo จด `SHIPPED` 11 แถว (placement/ชื่อ/พิกัด) + `WITHHELD` 1 แถว
     (87 คาร์ลอส กันไว้เองโดย `#803` คาดว่านิ่ง ห้ามนับเป็นผลลบ) - ห้ามใช้เลขเดาเองหรือเลขจากรอบอื่น
  2. กด: เข้าฉาก 14 (GM login-scene override หรือ `/warp 14`) -> NO-CRASH ด้วย right-click-drag ที่จุดยืนเริ่มต้น -> เดิน W/A/S/D เข้าใกล้
     >=1 ตัวใน `SHIPPED` และ >=1 ตัวที่ไม่อยู่ในลิสต์ (ตัวคุม ไม่ใช่ 87) · คลิก NPC ไม่ลบ splice แล้ว (แก้โดย LANE-A รอบ `yfbqmg`
     chief ตรวจซ้ำที่ `lane_hooks/lane_a_choose_npc_scene14.py:259-268` และ `:384` - **ไม่ใช่ `#803`** ซึ่งเป็นคนละเรื่อง) แต่ให้สังเกต/ถ่ายก่อนคลิก
  3. ดู/ตัดสิน: ภาพนิ่ง full-res ของทั้งสองตัว · จดสีป้ายชื่อ **ทุกป้ายในทุกภาพ** แยกบรรทัด ("none" ถ้าไม่มีป้าย) · เข้าตีเมื่อเข้าระยะหรือไม่ ·
     ชั้น wire/DB ปิดแล้วด้วยเทส ไม่ต้องรันซ้ำ - ตัดสินที่ชั้น client-observable อย่างเดียว: `SHIPPED` ต่างจากพลเรือน = PASS ·
     ทั้ง 11 ตัวนิ่งเหมือนพลเรือน **ทั้งที่ roster ไม่ใช่ 0** = FAIL ที่มีค่า ต้องส่ง (redirect ไป client-side faction byte / `RE-067` ห้ามอ่านเป็นการหักล้าง wire tier)
  4. บูต: สำเนา run copy (เนื้อใบเขียน `state\run_gt177.sqlite3` - ธรรมเนียมไฟล์นี้คือ `run_gt<เลขใบ>` ถ้าหาไม่เจอให้สำเนาเป็น `state\run_gt178.sqlite3`
     และจดว่าใช้ชื่อไหน) · sha256 ก่อน-หลังต้องเท่ากัน ห้ามแตะ canonical · `py -3 -u -m pirateforce_foundation.app --db state\<run copy>` ·
     ห้ามแฟล็ก `--*-scenario` ใด ๆ และห้าม `--second-password-mode bypass` ฝั่งเซิร์ฟเวอร์ (client `-SecondPasswordMode bypass` ใช้ได้) ·
     restart เซิร์ฟเวอร์ก่อนบูตไคลเอนต์ทุกครั้ง · teardown ภายใน 420 นาทีจาก boot stamp

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
อ้างจาก `notes_to_chief/20260907_0158_KA1A-R322C-RESULTS-GT274-PASS-mace-284-GT178-NEGATIVE-no-ai-tick-scene14.md` (R322C, ka1-A attended, OBSERVER_CONFIRMED 2026-09-07T01:48+07:00) คำต่อคำ:

> ก่อนบูต (บล็อกในใบ รันจากต้นไม้บูต): `SHIPPED` 11 แถว = Glaucoma(343)×7 · Phosphor Fascinator(345) · Crimson Sharp Teeth(348) · Arbiter Bells(350) · Lava shakers(353) · Horror butcher Lasa(355) — ทุกตัว LV105 HP 228,055 · `WITHHELD 87 924 Carlos`
> `/warp 14` (Hell Volcanic Island) → wire: `MOB_CENSUS_HOSTILITY scene_id=14 scene=Bg0015 roster=11 backed=11 unbacked=none refused=0 withheld=1` · จอ: Glaucoma ชื่อชมพู เจ้าของเดินเข้าประชิด
> **มอนไม่ทำอะไรเลย** (ไม่หัน ไม่วิ่ง ไม่ตี HP เจ้าของ 100/100) — สาเหตุจากคอนโซล:
> 1. **ไม่มี AI tick ในฉาก 14**: ทั้งเซสชันมีบรรทัด `MOB_AI_TICK_LIVE scene=1 mobs=4` บรรทัดเดียว (หุ่นซ้อมเมือง) ไม่มี `MOB_AI_TICK_LIVE scene=14` — การสร้าง register ใหม่ตอนมาถึงทำไว้แค่ฉาก 1/2 ฉาก 14 ที่มี roster 11 ตัวไม่มีใครต่อสาย ⇒ "ปลอดภัยแต่ไม่มีสมอง"
> 2. แม้ในฉาก 1 ที่ tick เดิน: `LANE_B_MOB_AI_TICK actor=0x206E idle->aggro intent=attack_undeliverable` (ตอนเจ้าของตีหุ่น) = มอนเข้าสถานะโกรธแล้วแต่**ส่งการโจมตีกลับหาผู้เล่นไม่ได้**

> สถานะที่เสนอ: GT-178 → NEGATIVE-MEASURED · ใบสร้างของ B (M4) 2 ข้อ: (ก) ทุกฉากที่มี roster สร้าง `MobAiRegister` ของตัวเองตอนผู้เล่นมาถึงและ tick เดิน — พิสูจน์ headless ด้วย `MOB_AI_TICK_LIVE scene=14 mobs=11` ก่อนเรียกเจ้าของ (ข) ต่อสายมอนตีผู้เล่น (`attack_undeliverable` → deliver) · เมื่อ (ก)+(ข) ขึ้น main ค่อยเปิด GT-178 รอบ 2 พร้อม HEADLESS_PROOF

RESULT: GT-178 NEGATIVE-MEASURED R322C 2026-09-07 01:48 (roster=11 backed=11 but no MOB_AI_TICK_LIVE for scene 14 · attack_undeliverable · mobs never react)

พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00
```

## 🆕 GT-179 DEEP-SEA-TEMPLE-FLOOR2-LANDING-GEOMETRY-001 [attended, in-game]: ฉาก 11 (Bg0011, Deep Sea Temple floor 2) ตัวประกอบ 51/56 ขึ้นจอไหม -- และ MARKER[11] เป็นพื้นที่ยืนได้จริงหรือไม่ (เกณฑ์คู่ ไม่ใช่แค่ actor)  [BLOCKED-ON-ATTENDED -- รอ PR ของรอบ `68mm02` (`pirate-force-server`, ยังไม่ merge เข้า `main`) merge ก่อน + รอ human ที่มี game client จริง]

> เปิดโดย LANE-A (สาย A · WORLD) รอบ `68mm02`, 2026-08-31 -- `login_entry_allowed` ของฉาก 11
> พลิกเป็น `true` รอบนี้ (`COO-DECISION 20260830_1441`, ประตูที่เก้าในคิวเดียวกับฉาก 4/5/6/8/3/10/7/9;
> composer `world_population_bg0011.py`/`world_bg0011_identity.py` **สร้าง ผูก และเปิดประตูในรอบเดียวกัน**
> เหมือนฉาก 5/6/8/3/7/9) -- ไม่ใช่สำเนาของ `GT-165`/`GT-171`/`GT-173`/`GT-174`/`GT-175`/`GT-176`/`GT-177`
> เพราะฉากนี้มีความเสี่ยงที่ใบเหล่านั้นไม่มี: ทะเบียนเอง (`table_row_differences.the_two_interiors`,
> pf-adversary รอบ `ga91m5`) ระบุฉากนี้ (คู่กับฉาก 10) เป็น "สองแถวที่รอบ attended ควรดูก่อนถ้าจุดลงมีปัญหา" --
> รูปแบบใบนี้จึงยึด `GT-166` (ฉาก 10) เป็นแม่แบบ ไม่ใช่ `GT-176`/`GT-177`

### objective (สองคำถาม ไม่ใช่หนึ่ง)
(1) ล็อกอินเข้าฉาก 11 จริงแล้ว **เห็นสิ่งมีชีวิตขึ้นจอ** (ไม่ใช่วิหารใต้น้ำว่างเปล่า) ใช่หรือไม่ -- composer
ตั้งใจไม่ส่ง faction bit เลย เหมือนฉากอื่น ๆ ที่เปิดมาก่อนหน้า (ดู `world_population_bg0011.py` docstring)
จึงไม่ใช่คำถามเรื่องความก้าวร้าว
(2) **ผู้เล่นยืนบนพื้นได้จริงไหม หรือตกในหิน/ลอยกลางอากาศ/จอดำ** -- จุดเกิด `MARKER[11]` อยู่ห่างจาก
placement ที่ใกล้ที่สุดของฉากนี้ 1107.764 หน่วย (อยู่ในขอบเขต placement เอง ต่างจากฉาก 10 ที่จุดเกิดอยู่นอก
ขอบเขต) แต่พื้น placement ต่ำสุดของฉากนี้อยู่ที่ z=-4592.9 ขณะที่ marker อยู่ที่ z=380 -- ต่างกันเกือบ 5000
หน่วยเช่นกัน ฉากนี้ยังเป็น "interior" แบบ n_CANGLIDE=0/n_LIMIT_HEIGHT=0 (บินร่อนไม่ได้ ไม่มีเพดานจำกัดความสูง)
เหมือนฉาก 10 คำถามที่ 2 นี้คือเหตุผลที่ใบนี้แยกจากใบ FIRST-EYES ธรรมดา ไม่ใช่ใบเดียวกัน

### ทางเข้า
ไม่มี production path ใดเขียนแถว character ให้ชื่อฉาก 11 เอง (ดู `login_entry_allowed_because` ในทะเบียน) --
เข้าได้เฉพาะ staged GM account (`config/gm_login_scene.json`, scene_id=11) หรือ GM `/warp 11` -- ทั้งสองทาง
ต้องรอ PR ของรอบ `68mm02` merge เข้า `main` ก่อนถึงจะบูตได้จริง

### สิ่งที่ยังไม่วัด (บันทึกไว้ล่วงหน้า ไม่ใช่คำทำนายว่าจะพัง)
1. Placement จริงของฉากนี้มี 56 ตัว แต่ composer ประกอบ (assemble) ได้ 51 ตัว (5 ตัวไม่มี `s_OUTFIT` เลยไม่ถูก
   ส่ง -- ดู `world_bg0011_identity.py` docstring สำหรับเหตุผลแยกแต่ละตัว) -- การเห็น "น้อยกว่า 56" ไม่ใช่ FAIL
   ของ objective (1) คำถามของ objective (1) คือมี actor ไหม ไม่ใช่ครบ 56 ไหม
2. จุดเกิด `MARKER[11]` เป็นชั้นหลักฐาน `authored` เท่านั้น -- ไม่เคยมีไคลเอนต์ยืนจริง ตัวเลขระยะทาง/z ข้างต้นคือ
   สิ่งที่วัดได้จากตารางไคลเอนต์ ไม่ใช่การคาดเดา -- ถ้าคำถามที่ 2 ตอบว่า "ตกในหิน/หลุดพื้น/จอดำ" **ให้บันทึกเป็น
   ข้อมูล ไม่ใช่ FAIL ของ objective (1)** สองคำถามนี้แยกอิสระจากกันโดยตั้งใจ

### pass criteria — สองชั้น, แยกตาม objective
**wire/DB objective (1) (ปิดแล้วโดยเทส):** console line `WORLD_CENSUS_BG0011 assembled=51/56 ...` ปรากฏหลัง
ล็อกอินเข้าฉาก 11 -- pin ไว้แล้วใน `tests/test_lane_a_scene_census.py` (repo `pirate-force-server`, ดู
`Bg0011RegistrationTests`)
**client-observable objective (1) (ยังไม่มีใครยืนดู):** ผู้เทสเข้าฉาก 11 จริงแล้วรายงานว่าเห็น actor ขึ้นจอ
หรือไม่ (นับคร่าว ๆ พอ ไม่ต้องนับให้ครบ 51)
**client-observable objective (2), ไม่มีชั้น wire/DB ให้ (ไม่มีอะไรในโค้ดฝั่งนี้ตรวจพื้นได้):** ผู้เทสรายงานว่า
ยืนบนพื้นได้ปกติ หรือหล่น/ติดหิน/จอดำ -- ผลของคำถามนี้เป็นข้อมูลใหม่สำหรับทะเบียน ไม่ใช่เกณฑ์ผ่าน/ไม่ผ่านของ
composer นี้

### สัญญาผู้บริโภค
เปิดโดย LANE-A -- LANE-A บริโภคผลเอง ปิดหัวใบเมื่อผู้เทสยืนยันด้วยตาทั้งสอง objective (แยกกันได้ -- objective
(1) อาจ PASS ขณะ objective (2) รายงานปัญหา) ตามหลัง PR ของรอบ `68mm02` merge แล้วเท่านั้น

### links
`scenarios/world_scene_registry_001.json` แถว `n_id: 11` (`login_entry_allowed_because`,
`table_row_differences.the_two_interiors`) · `src/pirateforce_foundation/world_population_bg0011.py`,
`world_bg0011_identity.py` · `rounds/A_68mm02...md` (repo `pirate-force-server`, จะ push พร้อมกับ PR ของรอบ
`68mm02`) · `notes_to_chief/20260831_0932_LANE-A-ASK-COO-scene10-landing-geometry-elevated-risk.md` ·
`notes_to_chief/20260831_1042_COO-DECISION-scene10-landing-geometry-open-affirmed.md` ·
`GT-166` (scene 10, same dual-objective shape, wider marker gap 5174.7 units) ·
`GT-165`/`GT-171`/`GT-173`/`GT-174`/`GT-175`/`GT-176`/`GT-177` (single-objective shape, not this scene's case) ·
`GT-134` (scene 14, same shape)

## 🆕 GT-180 NAVY-TRAINING-CAMP-FIRST-EYES-001 [attended, in-game]: ฉาก 130 (Bg4001, Navy Training Camp) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเจกต์ในฉากนี้ และเป็นฉากสุดท้ายจากสิบประตูเดิม  [BLOCKED-ON-ATTENDED -- รอ PR ของรอบ `yfbqmg` (`pirate-force-server`, ยังไม่ merge เข้า `main`) merge ก่อน + รอ human ที่มี game client จริง]

> เปิดโดย LANE-A (สาย A · WORLD) รอบ `yfbqmg`, 2026-09-01 · `login_entry_allowed` ของฉาก 130 พลิกเป็น
> `true` รอบนี้ (`COO-DECISION 20260830_1441`, ประตูที่สิบและประตูสุดท้ายในคิวเดียวกับฉาก 4/5/6/8/3/10/7/9/11;
> composer `world_population_bg4001.py`/`world_bg4001_identity.py` **สร้าง ผูก และเปิดประตูในรอบเดียวกัน**
> เหมือนฉาก 5/6/8/3/7/9/11) -- **ต่างจาก `GT-165`/`GT-171`/`GT-173`/`GT-174`/`GT-175`/`GT-176`/`GT-177` ตรงที่
> โค้ดของรอบนี้ยังไม่ merge เข้า `main` ณ เวลาที่เขียนใบนี้** จึงเปิดใบนี้เป็น `BLOCKED-ON-ATTENDED` ไม่ใช่
> `READY` -- ไม่ใช่สำเนาของ `GT-166`/`GT-178`/`GT-179` เพราะฉากนี้**ไม่มี**ความเสี่ยงแบบนั้น: ทะเบียนเองไม่ระบุ
> ฉากนี้ใน `table_row_differences.the_two_interiors` (ตรวจแล้ว ไม่ใช่สมมติ -- n_CANGLIDE=1, n_LIMIT_HEIGHT=0
> ไม่ใช่คู่ (0,0) ที่แฟล็กนั้นหมายถึง) -- รูปแบบเดียวกับ `GT-165`(4)/`GT-171`(5)/`GT-173`(6)/`GT-174`(8)/
> `GT-175`(3)/`GT-176`(7)/`GT-177`(9)

### objective (claim เดียว)
ล็อกอินเข้าฉาก 130 จริงแล้ว **เห็นตัวละคร/ทหารยืนอยู่ใน Navy Training Camp** (ไม่ใช่ฉากว่างเปล่า) และไม่โดน
ปฏิเสธล็อกอินเหมือนก่อนรอบ `yfbqmg` ใช่หรือไม่ -- คำถามคือ "มีสิ่งมีชีวิตขึ้นจอไหมและเข้าประตูนี้ได้จริงไหม"
ไม่ใช่ "มันโจมตีไหม": composer ของฉากนี้**ตั้งใจไม่ส่ง faction bit เลย** (ดู `world_population_bg4001.py`
docstring -- เป็นคำตัดสินของสาย B ที่ยังไม่ทำ) จึงไม่มีความเสี่ยงแบบ `GT-134` ที่มอนไม่ก้าวร้าว -- นั่นเป็น
พฤติกรรมที่คาดไว้ ไม่ใช่ FAIL ของใบนี้

### ทางเข้า
ไม่มี production path ใดเขียนแถว character ให้ชื่อฉาก 130 เอง (ดู `login_entry_allowed_because` ในทะเบียน) --
เข้าได้เฉพาะ staged GM account (`config/gm_login_scene.json`, scene_id=130) หรือ GM `/warp 130` -- ทั้งสองทาง
ต้องรอ PR ของรอบ `yfbqmg` merge เข้า `main` ก่อนถึงจะบูตได้จริง

### สิ่งที่ยังไม่วัด (บันทึกไว้ล่วงหน้า ไม่ใช่คำทำนายว่าจะพัง)
1. Placement จริงของฉากนี้มี 42 ตัว แต่ composer ประกอบ (assemble) ได้ 41 ตัว (1 ตัวไม่มี `s_OUTFIT`/ชื่อเลยไม่
   ถูกส่ง -- แคบที่สุดในบรรดาสิบเอ็ดฉากที่เลนนี้เคย crosswalk มา -- ดู `world_bg4001_identity.py` docstring)
   -- การเห็น "น้อยกว่า 42" ไม่ใช่ FAIL ของใบนี้ คำถามของใบนี้คือมี actor ไหม ไม่ใช่ครบ 42 ไหม
2. จุดเกิด `MARKER[1000]` (ฉาก 130 อ้าง marker คนละเลขกับ scene id เอง) ยังเป็นชั้นหลักฐาน `authored` เท่านั้น
   -- `never_sent_to_any_client_by_this_project` ห่างจาก placement จริงที่ใกล้ที่สุด **1018.201 หน่วย** และ
   อยู่**นอก**ขอบเขต placement ของฉากนี้ (หนึ่งในหกจากสิบประตูที่จุดเกิดอยู่นอกขอบเขต) -- ผู้เทส**ต้องรายงาน
   ผลข้อนี้แยกเป็นบรรทัดของตัวเองไม่ว่าจะยืนได้หรือไม่ได้** เพราะเป็นข้อมูลใหม่ที่ยังไม่มีใครวัด
3. ระดับ (`n_LEVEL_MIN`) ของ 17 identity ที่ resolve แล้วกระโดดกว้างผิดปกติในฉากเดียว: 15 ตัวอยู่ level 10
   (HP 421) แต่ 2 ตัว (Mob-Set 11 "Lightning Enchanted Generator", 12 "Rookie Recruit") อยู่ level 150
   (HP 616,267 -- ประมาณ 1,464 เท่าของอีก 15 ตัว) -- ไม่ใช่ FAIL แต่เป็นข้อมูลที่ควรรายงานถ้าเห็นความต่าง
   ชัดเจนบนจอ (ตัวใหญ่ผิดปกติ/ยืนแยกกลุ่ม)

### pass criteria — สองชั้น
**wire/DB (ยังไม่ปิดโดยเทส -- รอ PR ของรอบ `yfbqmg` merge เข้า `main` ก่อน):** console line
`WORLD_CENSUS_BG4001 assembled=41/42 ...` ต้องปรากฏหลังล็อกอินเข้าฉาก 130 -- ดูรูปแบบ log จาก composer
`world_population_bg4001.py` และ console reader `tests/test_lane_a_scene_census.py` (รูปแบบเดียวกับที่
`GT-165`/`GT-171`/`GT-173`/`GT-174`/`GT-175`/`GT-176`/`GT-177` ใช้ปิด) -- เทสที่ pin ตัวเลขนี้ให้แน่นอนยังไม่
ยืนยันว่ามีอยู่บน `main` ณ ตอนเขียนใบนี้ (ระบุไว้ตรง ๆ เพื่อไม่ให้อ่านผิดว่าปิดแล้ว)
**client-observable (ยังไม่มีใครยืนดู -- นี่คือสิ่งที่ใบนี้ต้องการ):** ผู้เทสเข้าฉาก 130 จริงแล้วรายงานว่าเห็น
actor ขึ้นจอหรือไม่ (นับคร่าว ๆ พอ ไม่ต้องนับให้ครบ 41) และล็อกอินผ่านได้ปกติ ไม่โดนปฏิเสธเหมือนก่อนรอบ
`yfbqmg` -- พร้อมรายงานแยกบรรทัดว่ายืนบน `MARKER[1000]` ได้ปกติหรือไม่ (ไม่ตกขอบแมพ/ไม่ค้างกำแพง/ไม่ตกน้ำแบบ
ผิดปกติ) ตามข้อ 2 ของ "สิ่งที่ยังไม่วัด" ข้างต้น (ข้อมูลใหม่ ไม่ใช่เงื่อนไขบล็อก PASS ของ objective หลัก)

### nonclaims
ใบนี้ไม่พิสูจน์ว่า placement ทั้ง 42 ตัวถูกต้อง (พิสูจน์แค่ assembled=41 ที่ composer ตั้งใจส่ง), ไม่พิสูจน์ว่า
ทหารก้าวร้าว/ไม่ก้าวร้าว (composer ตัดสินใจไม่ส่ง faction bit ไปแล้วนอกใบนี้), และไม่พิสูจน์อะไรเกี่ยวกับ
`MARKER[1000]` เกินกว่า "ยืนได้/ไม่ได้ในบูตนี้" -- ไม่ใช่การรับรองว่าจุดนี้จะยืนได้ทุกครั้งหรือหลัง reset

### สัญญาผู้บริโภค
เปิดโดย LANE-A -- LANE-A บริโภคผลเอง ปิดหัวใบเมื่อผู้เทสยืนยันด้วยตา ตามหลัง PR ของรอบ `yfbqmg` merge แล้ว
เท่านั้น

### links
`scenarios/world_scene_registry_001.json` แถว `n_id: 130` (`table_row_differences.login_entry_allowed_because`) ·
`src/pirateforce_foundation/world_population_bg4001.py`, `world_bg4001_identity.py` ·
`rounds/A_yfbqmg...md` (repo `pirate-force-server`, จะ push พร้อมกับ PR ของรอบ `yfbqmg`) ·
`GT-166`(ฉาก 10)/`GT-178`(ฉาก 14)/`GT-179`(ฉาก 11) (dual-objective shape, ไม่ใช่กรณีฉากนี้) ·
`GT-165`/`GT-171`/`GT-173`/`GT-174`/`GT-175`/`GT-176`/`GT-177` (single-objective shape, ฉากนี้ใช้แม่แบบเดียวกัน) ·
เป็นใบสุดท้ายของ "สิบประตูเดิม" (`COO-DECISION 20260830_1441`) -- หลังใบนี้ปิด สิบประตูเปิดครบทุกฉากที่จอ

### result (ผู้เทสกรอก)
```

```

## GT-181 PLAYER-DEATH-PREDICATE-PROBE-001  [PENDING]
- objective: single claim - during an attended round already using the ad-hoc ActorAttr probe channel (env PF_ADHOC_ATTR_PROBE=1), does setting the player's own BasicAttr hp_current (probe field x3, offset +0x44) to 0 and then BasicAttr death_timer (probe field x8, offset +0x58) to a non-positive value (0, then -1 if 0 does not trigger) make the client render the player's own character as dead on screen. This tests whether the shared IMAGE-layer death predicate documented at PF_ATTR_ROLE_DISCRIMINATOR.tsv row ACTOR_DEATH_SHARED (axis=death_state: "BasicAttr +0x44 == 0 AND ordered float +0x58 is nonpositive") actually governs the CLIENT's own visible death state for CMyActor (the player's own body), not just the CNetNPC family the row's own evidence audited.
- background (read before running):
  - PF_ATTR_ROLE_DISCRIMINATOR.tsv row ACTOR_DEATH_SHARED (axis=death_state, semantic_status=PROVEN_EXACT at the IMAGE layer only) names the predicate above and says explicitly it is shared behavior across 4 actor-family vtables including CNetNPC - it does NOT itself name CMyActor as audited.
  - pirate-force-server src/pirateforce_foundation/hostile_hp_link_hypothesis.py line 383: `BASIC_BIT_DEATH_TIMER = 0x0080  # f32 tag 0x2A @ +0x58   <- the lethal bit` - the module deliberately does not wire this bit in (see its own comment block starting "THE LETHAL SIDE IS NOT COPIED IN").
  - pirate-force-server src/pirateforce_foundation/mob_death.py lines 74-91: the timer's polarity is inverted from intuition (`timer > 0` = DYING, `timer <= 0` = DEAD, the state that builds CActorTask_Dead and plays the die animation), and NOTHING in the client image ever decrements BasicAttr f32[+0x58] on its own - "the field FREEZES at whatever the server last sent." This is why sending a non-positive value directly (rather than waiting for a countdown) is the only way to test the DEAD side of this gate.
  - the 27-Aug owner-run probe round already tried x8 (death_timer) with several POSITIVE values, alone and together with x3 (hp_current) = 0, and got a negative result both times (notes_to_chief/reference_adhoc_probe/ADHOC_PROBE_ROUND1_FINDINGS_20260827.md, row "8 death_timer"; same table row 8 in ACTORATTR_PROBE_TABLE_x_y.md). Nobody has yet tried a NON-POSITIVE value for x8. That is the one untried leg this entry closes.
  - source letter: notes_to_chief/20260831_2246_KA1B-TO-LANE-B-death-predicate-plus-probe-request.md (ka1-B's hypothesis and exact probe sequence, carried through verbatim below).
- db: whatever copy of state\pirateforce.sqlite3 the host attended round already made for its own boot (this entry does not boot a new round or make a new DB copy - it rides on the tail of a round already in progress, per notes_to_chief/consumed/20260830_2355_PANYA-ADDENDUM-probe-request-intake-4-gates-batched-sheet-rides-on-GT-round-ka1-B.md). Record the host round's own DB copy filename and sha256 (before/after) in the result, whatever they already are for that round - do not open the canonical file.
- server args: this step requires the ALREADY-BOOTED server for the host round to have been started with the ad-hoc probe lane enabled (env var `PF_ADHOC_ATTR_PROBE=1`; reference copy of the code at notes_to_chief/reference_adhoc_probe/adhoc_attr_probe.py, read-only, not part of `main`). This is Panya's own external fork, not the pirate-force-server `main` branch build used for ordinary GT rounds - the standard bypass flag (`-SecondPasswordMode bypass`) is unrelated and does not enable this. If the currently-booted round was NOT started with this env var, "probe 3 0" typed in chat is just an ordinary, inert chat line (it will not reach any special handler) - do not attempt this entry on that round; wait for the next round that is already probe-enabled and mark this entry's steps as not-yet-run for now, do not mark FAIL.
- steps:
  1. Precondition check (do this before touching anything else): confirm this round's server was booted with PF_ADHOC_ATTR_PROBE=1. If you booted it yourself, you already know. If someone else booted it, type `probe show` in chat and press Enter - a probe-enabled server prints the current ActorAttr/BasicAttr block to its own console; if nothing distinct happens (message just sits as a normal chat line, or "unknown command" style feedback), the lane is NOT enabled this round. Stop here and do not run the rest of this entry on this round.
  2. Right-click-drag the camera only (never Q/E, never WASD) until your own character's full body is in frame and unobstructed. This is a camera move only - it does not change facing and emits nothing on the wire, so it is safe at any point.
  3. Take a full-resolution screenshot labelled BASELINE. Record: your HP bar reading, whether your character shows any dead/dying pose already, and the colour of every name label visible in frame (your own nameplate and any other actor's nameplate) - one line per label, write "none" if there is nothing else in frame. Do not infer a cause for any colour, just record it.
  4. Click directly into the chat input box first and confirm the caret/focus is in the chat line (typing anywhere else turns keystrokes into hotkeys instead of chat text). Type exactly: `probe 3 0` and press Enter.
  5. Wait about 2 seconds. Take a full-resolution screenshot labelled STEP-A. Record the same three things as step 3 (HP bar, dead/dying state present or not, every name label's colour).
  6. Click back into the chat input box, type exactly: `probe 8 0` and press Enter.
  7. Wait about 2 seconds. Take a full-resolution screenshot labelled STEP-B. Record the same three things as step 3.
  8. If STEP-B does NOT show a dead state: click into chat, type exactly: `probe 8 -1` and press Enter. Wait about 2 seconds. Take a full-resolution screenshot labelled STEP-C. Record the same three things as step 3.
  9. If STEP-C (or STEP-B, whichever fired) shows a dead state: keep watching for about 20 more seconds (the client's own DYING duration constant is 20s per mob_death.py) and take one more screenshot labelled STEP-D, recording the same three things, to note whether anything changes on its own (mob_death.py already says nothing should - the field freezes - so this is a check against that claim for the player's own body, not an expectation of new behaviour).
  10. If none of STEP-A/B/C show a dead state: stop here, this is a valid negative result - do not try further undocumented probe values under this entry (that would be a new, separate probe-sheet request, per the one-entry-one-claim rule).
  11. End of probe segment for this entry. If the host round's own remaining plan needs a non-broken character afterward, whoever owns that round's own steps is responsible for restoring baseline stats (e.g. `probe base 1` plus re-setting x2-x6) - that restoration is outside this entry's claim and is not this entry's pass criterion.
- pass criteria (two layers, kept separate):
    wire/DB: from the host round's own console/capture log (the file already being written for that round, e.g. `server_console_live.out.txt` or whatever capture path that round's own boot script produces - do not start a separate capture for this), confirm after each of the three probe lines that an UpdateAttrVital (0x309A) frame was sent carrying the BasicAttr mask bits 0x0004 (x3) and/or 0x0080 (x8) set, decoding to exactly: hp_current (u32 @ +0x44) = 0 after "probe 3 0"; death_timer (f32 @ +0x58) = 0.0 (bit pattern 0x00000000) after "probe 8 0"; death_timer = -1.0 (bit pattern 0xBF800000) after "probe 8 -1", if that line was reached. This check can be done after the round is over, from the log alone, by anyone - it needs no human at the screen and it is not evidence of what the screen showed.
    client-observable: exactly what a human watching the screen reports for STEP-A, STEP-B, STEP-C (and STEP-D if reached) per steps 5/7/8/9 above - HP bar reading, dead/dying state present or not and what it actually looks like (describe what is seen, do not assume a specific animation name in advance), and every name label's colour. The three-part prediction this entry is built to falsify is: STEP-A shows NOT dead; STEP-B or STEP-C shows dead; if STEP-B and STEP-C both show NOT dead, the prediction is wrong and that is the result, written up as a negative finding, not a failed test.
- nonclaims:
  - Does not test the death predicate for any CNetNPC / mob / dummy actor - this entry only exercises the player's own CMyActor via the ActorAttr/BasicAttr probe channel; GT-031, GT-032, GT-084 are the mob/NPC-side entries and are not affected by this entry's result either way.
  - A positive result here (character does show dead) shows correlation with the two probed fields sent together; it does not by itself rule out that the client's ship-form is also required (ka1-B's own letter calls the ship-form requirement a guess he thinks becomes unnecessary if this predicate is confirmed, but this entry's steps do not test ship form at all, so it cannot confirm or exclude that guess).
  - Does not test respawn, does not test whether the client's own on-screen death_timer countdown UI actually ticks (mob_death.py already says the underlying field itself does not move once the server stops touching it; this entry's step 9 only checks whether the player's own case matches that same freeze, it is not a new claim about the countdown widget).
  - Does not test combat-triggered death (weapon hits, HP dropping through normal damage) - only a direct probe write of the two fields.
  - FontStyleID 63 is not death and is not being used as a proxy for it anywhere in this entry.
  - This probe channel (PF_ADHOC_ATTR_PROBE) is not part of the `pirate-force-server` `main` branch; this entry's result, positive or negative, says nothing about the standard boot's own production death pipeline except by way of the shared IMAGE-layer predicate both draw on.
  - Every name-label colour recorded in this entry's screenshots is recorded as data only - per Panya's 2026-08-25 order, the tester does not attempt to explain why a label is that colour; that question belongs to RE-067.
- links: notes_to_chief/20260831_2246_KA1B-TO-LANE-B-death-predicate-plus-probe-request.md - notes_to_chief/reference_codex_attr/PF_ATTR_ROLE_DISCRIMINATOR.tsv (row ACTOR_DEATH_SHARED) - pirate-force-server src/pirateforce_foundation/hostile_hp_link_hypothesis.py:383 - pirate-force-server src/pirateforce_foundation/mob_death.py:74-91 - notes_to_chief/reference_adhoc_probe/adhoc_attr_probe.py - notes_to_chief/reference_adhoc_probe/ACTORATTR_PROBE_TABLE_x_y.md - notes_to_chief/reference_adhoc_probe/ADHOC_PROBE_ROUND1_FINDINGS_20260827.md - notes_to_chief/consumed/20260830_2355_PANYA-ADDENDUM-probe-request-intake-4-gates-batched-sheet-rides-on-GT-round-ka1-B.md - numbering: GT-181 assigned after GT-180 collided with LANE-A round `yfbqmg`'s concurrent entry (same round, different topic) -- GT-181/RE-181 grepped as zero hits in GAME_TEST_QUEUE.md and CLIENT_RE_QUEUE.md before reserving this ID (highest prior at collision time: GT-180 taken by LANE-A, RE-172).
- result: (tester fills in: PASS/FAIL/BLOCKED, evidence, timestamp)

## GT-182 GM-A-WARP-NO-COORD-LIVE-SPAWN-001  [PASS -- OBSERVER_CONFIRMED 2026-09-01T10:40+07:00, chief round 8zf80f] -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-183 GM-B-SPEED-COMMAND-001  [❌ **CANCELLED - refuted by GT-218 (`/speed 400` killed the client in one frame, R306); open question carried by GT-... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## GT-184 UI-A-PART-A-BACK-TO-CHARSELECT-BUTTON-001  [🔴 **BLOCKED-ON-RE-266** -- ป้ายเดิม `BLOCKED-ON-WIRING` เปลี่ยนโดย chief (LANE-E) รอบ `rz1fxh`/R358 ตาม `COO-DECISION 20260905_1352` ข้อ 4 และ `20260905_1845` ข้อ 4 (ถ้อยคำ = chief · LANE-UI เสนอมาใน `20260905_1405`) · **ตัวบล็อกไม่ใช่ "ยังไม่ได้ต่อสาย" อีกแล้ว มันถูกต่อและวัดแล้วว่าไม่พอ**: R311 + R319 NEGATIVE -- push `0x709E` ก่อน ACK ไม่พา client เปลี่ยนหน้า (R319 13:47 วัดสด ไบต์ออกจริง 2/2 หลัง `GetWorldInfoVital` แต่จอไม่เปลี่ยน ⇒ HYP-PF-040 FALSIFIED) · เกตของ `0x709E` เองปิดตอบแล้วโดย `RE-075` (state gate `cStateCreateActor` + field gate `vital+0x14==0x1E` · payload ศูนย์ล้วนของ R319 ตกเกตชั้น 2 แน่นอน และตกชั้น 1 อยู่ดีเพราะ client อยู่ HOME ไม่ใช่หน้าสร้างตัวละคร) · **ตัวบล็อกที่เหลือ = `RE-266`** (downstream ของเกตที่ผ่าน + `GetWorldInfoVital 0x3D4B` reply-wait) · 🔴 **ห้ามบูตซ้ำจนกว่า `RE-266` จะชี้ทางใหม่** (`1352` ข้อ 2) · ใบนี้ออกจากหมวด "รอเครื่องคุณ" แล้ว -- มันรอผล RE ไม่ได้รอผู้เทส · **PANYA-ORDER `20260905_1911` (COO `1948`): LANE-UI งานแรกคือ UI-B ล็อกเอาต์จริง headless เป็น PR เซิร์ฟเวอร์ ก่อนใบ RE ใหม่ทุกใบ** -- ใบนี้ไม่ใช่ข้ออ้างให้ไม่มี PR · ประวัติเดิมไม่ลบ ต่อท้ายทันที: รันแล้ว R311 (`notes_to_chief/20260904_1931_KA1A-R311-RESULTS-*`) = **NEGATIVE / hypothesis not exercised**: ปุ่ม "กลับหน้าเลือกตัว" ส่ง `GetWorldInfoVital 0x3D4B` เต็ม 268 B (เซิร์ฟไม่ตอบ) แล้ว `0x1B40` subcode 03 → `HYP_PF_013_LOGOUT_SUBCODE03_ACK_THEN_SERVER_SOCKET_CLOSE` 46 B แล้วปิด socket · จอไม่เปลี่ยน ไม่มีข้อความ 90 วิ (ภาพ `20260904_192129.png`) · `OBSERVER_CONFIRMED: 2026-09-04T19:26+07:00` · 🔴 **push `0x709E` ของ scenario `logout_hypothesis_dialog_open_push` ไม่เคยออกจากเซิร์ฟเวอร์** (ไม่มี `[G>]` เฟรมนั้นทั้งรอบ) ⇒ ยังตัดสิน HYP-PF-040 ไม่ได้ · ห้ามบูตซ้ำจนกว่า **LANE-UI** จะแก้ให้ push ออกจริง (รันใหม่ ~6 นาที) · ป้ายเขียนโดย chief (LANE-E) รอบ `t7bsfx`/R342 ตาม `COO-DECISION 20260904_1948` ข้อ 5] [ประวัติป้ายเดิม] [BLOCKED -- branch-6 (dialog-open unsolicited 0x709E push) module built round `bkgaq8`, `pirate-force-server` PR `#471`: src/pirateforce_foundation/logout_dialog_open_hypothesis.py, not wired into runtime.py yet. CORE-REQUEST open in this letter's own round file/letter for chief to wire; production_allowed stays False until wired + re-read by pf-adversary once more. Do not boot this ticket until wiring lands on main] [STALE as of round `tmizmk` 2026-09-01T15:58+07:00 -- wiring landed round `liq4ri` (PR #476); sixth allowlist profile landed round `tmizmk` (PR pending merge). Boot now with `--logout-hypothesis-scenario scenarios/logout_hypothesis_dialog_open_push.json`. `production_allowed` still False, unchanged -- stop_rule still requires an attended GT-184/GT-186 pass first. Ready for attended capture.] [MEASURED, round `2ahq88` 2026-09-01T16:35+07:00 -- "PR pending merge" above is stale: `pull_request_read get` confirms `pirate-force-server#484` merged=true (merged_at 2026-09-01T09:17:06Z) and `pf_bridge#724` merged=true (merged_at 2026-09-01T09:08:21Z). Sixth allowlist profile is on `main` now, not pending. No other change to this ticket's status -- still awaiting attended capture.]

> Opened by chief this round, directly per Panya's order, same provenance as `GT-182`.
> Source: PANYA-ORDER `notes_to_chief/20260901_0215_PANYA-ORDER-*.md` section 3 (UI-A,
> first half: "back to character select"). Split from the owner's single UI-A line into
> two entries (`GT-184`/`GT-185`) because the two buttons are independently falsifiable
> claims -- both halves opened this same round. Build-owner lane: **LANE-A** per chief's
> broadcast letter this round.

- objective: single claim -- clicking the HOME-menu "กลับหน้าเลือกตัวละคร" (back to
  character select) button while in a live map actually transitions the client to the
  character-select screen, mid-session, without closing the client window. This is the
  exact open question `GT-033` left unanswered: that entry proved (ANSWERED, not PASS)
  that the client sends a real `LogoutVital 0x1B40` subcode-03 frame when this button is
  clicked, and that BOTH response policies tried so far (ack+close-socket; and
  `ReturnSelectServerVital 0x709E`+ack+close-socket) leave the client sitting on the same
  map screen with no transition, no error, no popup, and no process exit -- for 50-77
  seconds of observation in three separate attended rounds. This entry exists to be run
  against whatever NEW response/sequence the implementing lane builds -- it is not a
  repeat of `GT-033`'s already-answered variants A/B.
- background (read before running):
  - `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md` GT-033 RESULT block: full detail
    on what has already been tried and failed, including the six untested branches listed
    there -- do not re-propose one of those six as if it were new.
  - `GT-026`: the HOME menu's exit dialog/buttons exist and are clickable, and clicking
    does not freeze the client -- that plumbing is not what's broken; what's broken is
    what happens (or doesn't) after the click.
  - `RE-070` (`CLIENT_RE_QUEUE.md`): the open static-RE question about what actually gates
    the orchestrator's scene/connection teardown. If this GT entry is still BLOCKED at
    read time, check whether `RE-070` has new findings before assuming nothing has
    changed.
- db: fresh copy of `state\pirateforce.sqlite3` (never canonical) -- record filename +
  sha256 before/after; verify canonical file's sha256 unchanged.
- server args: standard boot, `-SecondPasswordMode bypass`. Requires whatever new
  response-policy scenario/flag the implementing lane builds for this fix; do not attempt
  this entry against the default boot or against the already-answered `GT-033` variant A/B
  scenarios.
- steps:
  1. Boot per standard playbook; confirm server up first; confirm fresh server (not reused
     after a killed client).
  2. Log in normally. Right-click-drag camera only for a clean baseline view. Screenshot
     BASELINE, full resolution, record every name label's colour (one per line, "none" if
     empty).
  3. Open the HOME menu, click "กลับหน้าเลือกตัวละคร". Note the wall-clock time of the
     click.
  4. Watch continuously for at least 90 seconds (GT-033's longest prior negative-result
     window was ~77 seconds). Screenshot at +5s, +30s, +60s, +90s, labelled STEP-A through
     STEP-D. Record at each: is the client still on the map, has any dialog/popup
     appeared, has the screen changed to character-select, and every name label's colour
     if still on a screen with name labels.
  5. If character-select is reached, screenshot it labelled SUCCESS and record what is
     shown (character name, any list of characters, any error text).
- pass criteria (two layers, kept separate):
    wire/DB: server console/capture log shows the `LogoutVital 0x1B40` subcode-03 request
      arriving AND the new response frame(s) the implementing lane sends in reply,
      byte-decoded and logged with a distinct token so a human's screenshot timestamps can
      be lined up against it after the fact.
    client-observable: does the human watching the screen actually see the
      character-select screen appear within the 90-second observation window, with no
      client crash/freeze and no need to close the window. A negative result here (client
      stays on the map, exactly like `GT-033`) is a valid, useful finding.
- nonclaims:
  1. Does not test the "ออกจากเกม" (exit/quit) button or `LogoutVital` subcode 01 -- that
     is `GT-186`, a separate claim.
  2. Does not test what happens AFTER reaching character-select (re-entering the game) --
     that is `GT-185`, which has this entry's PASS as a precondition.
  3. Does not claim any prior `GT-033` variant is retested or re-litigated.
  4. Does not attribute a negative result to any single one of the "kinit-teardown reaches
     the client" open questions from `GT-033`'s nonclaims without new evidence.
- RECHECK: `cd pirate-force-server && git log --all --oneline -i --grep="UI-A" --grep="back.*char.*select" --grep="GT-184" --grep="RE-070" | head -8`
  (empty output for the UI-A/GT-184 terms = still BLOCKED).
- links: `notes_to_chief/20260901_0215_PANYA-ORDER-*.md` (section 3, UI-A) --
  `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md` (GT-033 full result) -- `GT-026` --
  `RE-070` in `CLIENT_RE_QUEUE.md` -- `PROCESS_GATES.md` rule #18 -- `GT-185` (depends on
  this entry's PASS).
- numbering: see `GT-182`'s numbering note. This entry is `184`.
- result: (tester/build lane fills in: PASS/FAIL/BLOCKED, evidence, timestamp,
  OBSERVER_CONFIRMED line per G-OBS once client-observable evidence exists)

## GT-185 UI-A-PART-B-BACK-INTO-GAME-ROUNDTRIP-001  [BLOCKED]

> Opened by chief this round, directly per Panya's order, same provenance as `GT-182`.
> Source: PANYA-ORDER `notes_to_chief/20260901_0215_PANYA-ORDER-*.md` section 3 (UI-A,
> second half: "back into game"). This is the half of UI-A that unblocks the owner's
> stated cost problem: today, changing scene/map to test something new costs a full
> client reboot because there is no working way back into a live game from
> character-select without closing the window. Build-owner lane: **LANE-A** per chief's
> broadcast letter this round.

- objective: single claim -- having reached the character-select screen via the button
  tested in `GT-184` (this entry's hard precondition -- it cannot be attempted at all
  until `GT-184` PASSes), selecting a character from that screen and clicking whatever
  "enter game"/"back into game" control exists there returns the client to a live,
  playable game scene, in the SAME client process (no window close/reopen), and that this
  second entry-into-game behaves the same as an ordinary first login (character loads
  correctly, HUD populates, movement works, no stale state left over from the previous
  session).
- background (read before running):
  - This is explicitly the mechanism the owner said is costing every test round money:
    "ทางเดียวคือปิดหน้าต่างด้วย X ... บูตใหม่ทั้งรอบเพื่อเปลี่ยนฉากหนึ่งครั้ง" (the only way
    is closing the window with X, which means a full reboot just to change scene once).
    This entry is what proves that cost has actually been removed.
  - The normal first-login character-select-to-game path already works today -- the open
    question this entry asks is whether doing it a SECOND time, within the same running
    client process, behaves identically, or whether stale state from the first session
    causes a different, broken result the second time. Do not assume the answer is
    "obviously yes" -- write it down and check instead of assuming.
- db: fresh copy of `state\pirateforce.sqlite3` (never canonical) -- record filename +
  sha256 before/after; verify canonical file's sha256 unchanged.
- server args: same boot as `GT-184` (this is a continuation within the same boot/session,
  not a new boot) -- do not restart the server between `GT-184`'s steps and this entry's
  steps.
- steps:
  1. Complete `GT-184`'s steps first, in the same boot, ending with the client actually on
     the character-select screen. If `GT-184` did not reach character-select, stop here --
     mark this entry NOT-YET-RUN (not FAIL; it was never reached).
  2. Screenshot the character-select screen, full resolution, labelled CHARSELECT-BASELINE.
     Record what is shown and every name label's colour if any are visible on this screen.
  3. Select the same character used earlier this session. Click whatever control returns
     to the game. Record the exact button label seen.
  4. Wait up to 30 seconds. Screenshot STEP-A. Record: did the client load into a live
     scene, which scene (name/background/minimap), HUD state (HP/MP/level match the
     character's last known values or not), and every name label's colour.
  5. If loaded into a scene, right-click-drag camera only to confirm a stable, non-frozen
     view. Then perform ONE ordinary WASD movement to confirm the character can actually
     move.
  6. Screenshot STEP-B after the movement check. Record whether the movement was reflected
     on screen normally.
- pass criteria (two layers, kept separate):
    wire/DB: server console/capture log shows a fresh scene-entry sequence firing
      correctly a SECOND time within the same TCP session/connection as the first login,
      with no duplicate-registration errors, no exception lines, and `sessions`/
      `characters` DB state consistent with one character, one active session.
    client-observable: does the human watching the screen see a normal, playable game
      scene appear after selecting the character and clicking "back into game" -- correct
      HUD values, correct scene, and basic movement working -- within the same client
      process, with no crash and no need to reopen the client.
- nonclaims:
  1. Does not test entering a DIFFERENT scene than the one the character was in before --
     that is closer to a `/warp` claim, already covered by `GT-182`.
  2. Does not test repeating this round-trip a third or further time.
  3. Does not test multiple characters/multiple accounts round-tripping concurrently.
  4. Does not claim this removes the need for any existing teardown/killed-client
     workaround.
- RECHECK: `cd pirate-force-server && git log --all --oneline -i --grep="UI-A" --grep="back into game" --grep="GT-185" | head -5`
  (empty output = still blocked on GT-184's own fix landing).
- links: `notes_to_chief/20260901_0215_PANYA-ORDER-*.md` (section 3, UI-A) -- `GT-184`
  (hard precondition) -- `PROCESS_GATES.md` rule #18.
- numbering: see `GT-182`'s numbering note. This entry is `185`.
- result: (tester/build lane fills in: PASS/FAIL/BLOCKED/NOT-YET-RUN, evidence, timestamp,
  OBSERVER_CONFIRMED line per G-OBS once client-observable evidence exists)

## GT-186 UI-B-REAL-LOGOUT-BUTTON-001  [🔴 **BLOCKED-ON-RE-266** -- ป้ายเดิม `BLOCKED-ON-WIRING` เปลี่ยนโดย chief (LANE-E) รอบ `rz1fxh`/R358 ตาม `COO-DECISION 20260905_1352` ข้อ 4 และ `20260905_1845` ข้อ 4 (ถ้อยคำ = chief · LANE-UI เสนอมาใน `20260905_1405`) · **ตัวบล็อกไม่ใช่ "ยังไม่ได้ต่อสาย" อีกแล้ว มันถูกต่อและวัดแล้วว่าไม่พอ**: R311 + R319 NEGATIVE -- push `0x709E` ก่อน ACK ไม่พา client เปลี่ยนหน้า (R319 13:47 วัดสด ไบต์ออกจริง 2/2 หลัง `GetWorldInfoVital` แต่จอไม่เปลี่ยน ⇒ HYP-PF-040 FALSIFIED) · เกตของ `0x709E` เองปิดตอบแล้วโดย `RE-075` (state gate `cStateCreateActor` + field gate `vital+0x14==0x1E` · payload ศูนย์ล้วนของ R319 ตกเกตชั้น 2 แน่นอน และตกชั้น 1 อยู่ดีเพราะ client อยู่ HOME ไม่ใช่หน้าสร้างตัวละคร) · **ตัวบล็อกที่เหลือ = `RE-266`** (downstream ของเกตที่ผ่าน + `GetWorldInfoVital 0x3D4B` reply-wait) · 🔴 **ห้ามบูตซ้ำจนกว่า `RE-266` จะชี้ทางใหม่** (`1352` ข้อ 2) · ใบนี้ออกจากหมวด "รอเครื่องคุณ" แล้ว -- มันรอผล RE ไม่ได้รอผู้เทส · **PANYA-ORDER `20260905_1911` (COO `1948`): LANE-UI งานแรกคือ UI-B ล็อกเอาต์จริง headless เป็น PR เซิร์ฟเวอร์ ก่อนใบ RE ใหม่ทุกใบ** -- ใบนี้ไม่ใช่ข้ออ้างให้ไม่มี PR · ประวัติเดิมไม่ลบ ต่อท้ายทันที: รันแล้ว R311 (`notes_to_chief/20260904_1931_KA1A-R311-RESULTS-*`) = **NEGATIVE / hypothesis not exercised**: ปุ่ม "ออกจากเกม" ส่ง `GetWorldInfoVital 0x3D4B` เต็ม 268 B (เซิร์ฟไม่ตอบ) แล้ว `0x1B40` subcode 01 → `HYP_PF_013_LOGOUT_SUBCODE01_ACK_THEN_SERVER_SOCKET_CLOSE` 46 B แล้วปิด socket · จอไม่เปลี่ยน ไม่มีข้อความ 90 วิ (ภาพ `20260904_192633.png`) · `OBSERVER_CONFIRMED: 2026-09-04T19:26+07:00` · 🔴 **push `0x709E` ของ scenario `logout_hypothesis_dialog_open_push` ไม่เคยออกจากเซิร์ฟเวอร์** (ไม่มี `[G>]` เฟรมนั้นทั้งรอบ) ⇒ ยังตัดสิน HYP-PF-040 ไม่ได้ · ห้ามบูตซ้ำจนกว่า **LANE-UI** จะแก้ให้ push ออกจริง (รันใหม่ ~6 นาที) · ป้ายเขียนโดย chief (LANE-E) รอบ `t7bsfx`/R342 ตาม `COO-DECISION 20260904_1948` ข้อ 5] [ประวัติป้ายเดิม] [BLOCKED -- branch-6 (dialog-open unsolicited 0x709E push) module built round `bkgaq8`, `pirate-force-server` PR `#471`: src/pirateforce_foundation/logout_dialog_open_hypothesis.py, not wired into runtime.py yet. CORE-REQUEST open in this letter's own round file/letter for chief to wire; production_allowed stays False until wired + re-read by pf-adversary once more. Do not boot this ticket until wiring lands on main] [STALE as of round `tmizmk` 2026-09-01T15:58+07:00 -- wiring landed round `liq4ri` (PR #476); sixth allowlist profile landed round `tmizmk` (PR pending merge). Boot now with `--logout-hypothesis-scenario scenarios/logout_hypothesis_dialog_open_push.json`. `production_allowed` still False, unchanged -- stop_rule still requires an attended GT-184/GT-186 pass first. Ready for attended capture.] [MEASURED, round `2ahq88` 2026-09-01T16:35+07:00 -- "PR pending merge" above is stale: `pull_request_read get` confirms `pirate-force-server#484` merged=true (merged_at 2026-09-01T09:17:06Z) and `pf_bridge#724` merged=true (merged_at 2026-09-01T09:08:21Z). Sixth allowlist profile is on `main` now, not pending. No other change to this ticket's status -- still awaiting attended capture.]

> Opened by chief this round, directly per Panya's order, same provenance as `GT-182`.
> Source: PANYA-ORDER `notes_to_chief/20260901_0215_PANYA-ORDER-*.md` section 3 (UI-B: "a
> real logout button, distinct from the X close-window button, must work"). Build-owner
> lane: **LANE-A** per chief's broadcast letter this round.

- objective: single claim -- clicking the HOME-menu "ออกจากเกม" (exit/quit) control while
  in a live map ends the session cleanly and takes the client itself out of the game
  (screen changes away from the map and/or the client process exits on its own), as a
  genuine alternative to forcibly closing the window with the OS-level X button. `GT-033`
  already measured this exact button (subcode 01 of `LogoutVital 0x1B40`) under variant A
  (ack + close-socket) and found the client's own process did NOT exit on its own within
  the observation window; variant B (adding `ReturnSelectServerVital` first) was
  deliberately NOT run against subcode 01. This entry is scoped to whatever NEW mechanism
  the implementing lane builds, not a repeat of variant A.
- background (read before running):
  - `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md` GT-033 RESULT block, subcode-01
    column specifically: variant A measured, process did not exit on its own; variant B
    subcode 01 explicitly NOT measured -- if the implementing lane's fix is close to
    variant B in shape, running that untested cell for the first time here would itself be
    new information, not a repeat.
  - Distinguish this from `GT-184`/`GT-185`: those are about the "back to character
    select" -> "back into game" round trip. This entry is about actually LEAVING/ending
    the client session as a deliberate, clean alternative to the destructive X-kill.
- db: fresh copy of `state\pirateforce.sqlite3` (never canonical) -- record filename +
  sha256 before/after; verify canonical file's sha256 unchanged.
- server args: standard boot, `-SecondPasswordMode bypass`. Requires whatever new
  response/sequence the implementing lane builds for the exit path; if the fix is shared
  code with `GT-184`'s fix, say so explicitly in this entry's result and cross-reference,
  but still test this button and this subcode separately.
- steps:
  1. Boot per standard playbook; confirm server up first; confirm fresh server (not reused
     after a killed client).
  2. Log in normally. Right-click-drag camera only for a clean baseline view. Screenshot
     BASELINE, full resolution, record every name label's colour (one per line, "none" if
     empty).
  3. Open the HOME menu, click "ออกจากเกม" (exit/quit -- record the exact label text
     seen). Note the wall-clock time.
  4. Watch continuously for at least 90 seconds. Screenshot at +5s, +30s, +60s, +90s,
     labelled STEP-A through STEP-D. Record at each: is the client window still open, is
     it still showing the map, has any dialog/disconnect-notice appeared, and (if the
     window is still open and showing name labels) every name label's colour.
  5. If the client process exits on its own at any point, record the exact wall-clock time
     it happened relative to the click in step 3.
  6. If the client is still sitting on the same map screen after 90 seconds with no change
     of any kind, this is the negative result this entry is built to catch.
- pass criteria (two layers, kept separate):
    wire/DB: server console/capture log shows the `LogoutVital 0x1B40` subcode-01 request
      arriving AND `sessions.closed_at` being written server-side AND whatever new
      response frame(s) the implementing lane sends, logged with a distinct, greppable
      token.
    client-observable: does the human watching the screen see the client actually leave
      the map -- either the process exits on its own, or the screen changes to something
      that clearly indicates a completed logout -- within the 90-second window, without
      the tester needing to close the window with X.
- nonclaims:
  1. Does not test the "back to character select" button or `LogoutVital` subcode 03 --
     that is `GT-184`, a separate claim, even if it turns out to share implementation code.
  2. Does not test what a killed/X-closed client looks like server-side.
  3. Does not claim any existing teardown-template age limit changes because of this
     entry's result either way.
  4. Does not attribute a negative result to any specific untested branch from `GT-033`'s
     six-branches list without first checking whether the implementing lane's fix actually
     touches that branch.
- RECHECK: `cd pirate-force-server && git log --all --oneline -i --grep="UI-B" --grep="logout" --grep="GT-186" | head -5`
  (empty output = still BLOCKED-ON-WIRING).
- links: `notes_to_chief/20260901_0215_PANYA-ORDER-*.md` (section 3, UI-B) --
  `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md` (GT-033 full result, subcode-01
  column) -- `GT-184` (sibling UI ticket, different subcode) -- `PROCESS_GATES.md` rule #18.
- numbering: see `GT-182`'s numbering note. This entry is `186`.
- result: (tester/build lane fills in: PASS/FAIL/BLOCKED, evidence, timestamp,
  OBSERVER_CONFIRMED line per G-OBS once client-observable evidence exists)

## GT-187 GM-045-CENSUS-SCENE-RESYNC-CLIENT-CONFIRM-001  [❌ **CANCELLED - no longer needs proving because ทางเข้าของใบนี้ไม่มีอยู่บน `main` วันนี้** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 202609... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-188 GROUND-DROP-HEARTBEAT-PRESERVE-CONFIRM-001  [🟡 **checkpoint 1 = ❌ CANCELLED - covered by GT-216 · checkpoint 2 = 🔵 MEASURED (BASELINE) รอบ R309 — ผลคือ "หาย" ยังไม่ปิดใบ** (ทั้งหมดคำต่อคำจากหัวใบเดิม — ตัดออกเฉพาะพารามิเตอร์ `(🟢 PASS สองชั้น · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00)` ที่เดิมแทรกอยู่หลัง "covered by GT-216": นั่นคือคำตัดสินของ `GT-216` เอง ไม่ใช่ของใบนี้ ทำให้เครื่องมือ regex อ่านใบนี้เป็น PASS ผิด — ย้ายไปบรรทัด "ประวัติหัวใบเดิม" ด้านล่างแทน) [จัดรูปแบบโดย LANE-K รอบ `x91eo8`/`x91eo8r2` ตามข้อเสนอ chief `R374` ข้อ 2 — คำอื่นทุกคำคงเดิมทุกตัวอักษร ไม่มีการเขียนสรุปใหม่]]

> **ประวัติหัวใบเดิมคำต่อคำ (ก่อนจัดรูปแบบรอบ `x91eo8`)**: checkpoint 1 = ❌ CANCELLED - covered by GT-216 (🟢 PASS สองชั้น · `OBSERVER_CONFIRMED 2026-09-03T16:51+07:00`) · checkpoint 2 = 🔵 MEASURED (BASELINE) รอบ R309 — ผลคือ "หาย" ยังไม่ปิดใบ · ปิด cp1 โดย chief รอบ `oi2r2n`/R340 ตาม `COO-DECISION 20260904_1648` ข้อ 3 + `PANYA-DECISION 20260903_1934`
>
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

## GT-189 PORT-ROYAL-LOGIN-CENSUS-NO-WALK-001  [BLOCKED -- two-part fix not complete: LANE-A built the click-safety half (`lane_hooks/lane_a_choose_npc_scene1.py`, round `yv3k9x`, `production_allowed = False`) but the `runtime.py` login-trigger widen this ticket also needs is a CORE-REQUEST not yet actioned by chief, and must not land before the safety half's gate flips True -- see `notes_to_chief/20260901_1037_LANE-A-STATUS-*`. Do not boot this ticket until RECHECK below shows both landed]

- objective: one claim only -- a fresh login into Port Royal (bg0001) shows NPCs standing on screen immediately, with zero steps taken (no `W`/`A`/`S`/`D`, no `Q`/`E` facing change, no `TargetPosVital` sent), where today the town is provably empty on screen until the player's first step. PANYA-ORDER 2026-09-01T09:55: "ตอนเข้าเกมมา port royal ยังไม่เจอ npc ใดๆ เพราะไม่เดิน ทำไมไม่ทำอันนี้ด้วยล่ะ เว้นไว้ทำไม".
- db: default state\pirateforce.sqlite3 -- always a fresh copy for this boot only, never the canonical file. Record the copy's filename and sha256 before/after the round, and confirm the canonical file's sha256 is unchanged before/after. Use a character whose stored position is scene 1 (Port Royal), so this boot is a real login, not a warp.
- server args: standard playbook boot on `main`, only after RECHECK below shows both halves of the fix landed. No special flags -- the whole point of this ticket is that no scenario flag is involved.
- steps:
  1. Boot server, confirm it is freshly started (age < 3.5 min); boot client only after server is up.
  2. Log in with a character parked in Port Royal. Do NOT move -- no `W`/`A`/`S`/`D`, no `Q`/`E` (both emit `TargetPosVital`). Right-click-drag only if a camera-angle adjustment is wanted (camera only, emits nothing, safe at any point).
  3. Immediately after the world finishes loading (before any input), full-res photo BASELINE: NPCs visible y/n, count if visible, and the colour of every name label in frame (one line per label, "none" if there are none).
  4. Left-click one visible NPC. Full-res photo STEP-A: does the NPC turn to face something / play its click reaction, does the connection stay alive (no disconnect), label colours again.
  5. Only after STEP-A, take one step (`W` once) and repeat the same click on the same NPC. Full-res photo STEP-B: same fields as STEP-A, so a click-before-move and a click-after-move can be compared.
  6. Record wall-clock time for every step, to cross-check against the server console/capture log afterward.
- pass criteria (two layers, kept separate):
    wire/DB: the server console for this boot shows a `WORLD_CENSUS` line (from `world_population.census_console_line`) BEFORE the first `TargetPosVital` the session sends (or with none sent at all, if the tester never moves) -- proof the census composed and queued without a movement trigger. A `LANE_HOOK_FIRED pirateforce_foundation.lane_hooks.lane_a_choose_npc_scene1 scene_choose_npc_responder` line (not a `KeyError`/disconnect) must follow the STEP-A click. Provable headless from the capture log; does not by itself prove the client rendered anything.
    client-observable: the human at the screen reports NPCs standing in view at BASELINE with zero steps taken, and reports whether the STEP-A click (before any movement) got an honest response (NPC turns/reacts) rather than a dropped connection. A negative result (town still empty at BASELINE, or the connection drops on the STEP-A click) is a finding worth exactly as much as a PASS -- record it and note which half of the fix it points back to (composer trigger vs click responder), not a guess.
- nonclaims:
  1. Does not claim the click-response frame this responder builds is byte-identical to what the frozen dispatcher would have sent for the same click after a move -- that is a separate parity question, not yet measured (see the CORE-REQUEST letter's own "ยังไม่ได้พิสูจน์").
  2. Does not claim anything about scenes other than 1 -- the other ten roster scenes' census/click behavior is unaffected by this ticket.
  3. Does not verify frame size/`ConnectionAbortedError 10053` risk named in the PANYA-ORDER's own "ข้อควรระวัง" -- Port Royal's census frame is large (~108-115 actors, ~20 KB) and has been observed to disconnect a client occasionally in the past (GT-165); if that reproduces here, it must be reported as its own finding, never silently worked around by reducing the actor count.
  4. Does not attribute a cause to any label's colour -- record colours only, per RE-067.
- RECHECK: `cd pirate-force-server && git log --all --oneline -i --grep="lane_a_choose_npc_scene1" --grep="GT-189" -- src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene1.py | head -5` (confirms the responder module is on `main`) AND a `notes_to_chief` letter confirming `production_allowed = True` for that module AND `git log -p -- src/pirateforce_foundation/runtime.py | grep -A3 "runtime.py:7578"`-style check that the login-trigger widen landed. All three must be true before booting; anything less is still BLOCKED.
- links: `pf_bridge/notes_to_chief/20260901_0955_PANYA-ORDER-login-path-must-ship-the-census-eagerly-like-the-warp-path-now-does.md` (the order) -- `pf_bridge/notes_to_chief/20260901_1037_LANE-A-STATUS-port-royal-login-census-safety-net-built-core-request-for-chief.md` (this ticket's own build + CORE-REQUEST) -- `pirate-force-server/src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene1.py` -- `pirate-force-server/src/pirateforce_foundation/runtime.py:7569-7599` and `:8256-8266` (the trigger and the field comment naming the crash) -- GT-165 (frame-size disconnect precedent).
- numbering: per the shared-counter search command (rule ② at the top of this file), the highest confirmed number before this entry is `GT-188`. This entry is `189`.
- result: (tester fills in: PASS/FAIL/BLOCKED, evidence, timestamp, OBSERVER_CONFIRMED line per G-OBS once client-observable evidence exists)

## 🆕🔬 GT-190 NPC-IDENTITY-CLINE-RESOLVED-BG0004-001 [attended, in-game, BLOCKED-ON-WIRING]: NPC ของฉาก 4 (Slave Market Island, Bg0004) ตรง CLINE crosswalk ที่คำนวณไว้จริงหรือไม่ -- ยังไม่มีใครยืนที่ฉากนี้แล้วดูมาก่อน

> 🔢 **หมายเหตุเลข:** จองไว้เป็น `GT-160` ตอน 2026-09-01T11:4x+07:00 (grep ตอนนั้น 0 hit) แต่ `main`
> ขยับใต้ branch ระหว่างรอบ -- LANE-B จอง `GT-160` (`TRAINING-DUMMY-NAME-COLOUR-001`) สำเร็จก่อนที่ PR นี้
> จะ merge เข้า `main` ได้ ตอนแก้ conflict (2026-09-01) grep ซ้ำพบสูงสุดบน `main` คือ `GT-189` ⇒ ใบนี้
> เปลี่ยนเลขเป็น `GT-190` เนื้อความอื่นไม่แก้ ใบ `RE-085`-`RE-168`/`GT-001`-`GT-189` อยู่ที่เดิมทั้งใบ
> ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ

### ที่มา

`COO-DECISION 20260830_1441 (scene4-slave-market-first-door)` อนุมัติให้ LANE-A สร้าง crosswalk
CLINE→MOBS แบบเดียวกับ `BUILD-001` (bg0001) ให้ฉาก 4 -- รอบ `s3m1f7` สร้างตัวประกอบเสร็จแล้ว
(`src/pirateforce_foundation/scene4_slave_market_tables.py`,
`src/pirateforce_foundation/world_population_bg0004.py`, ทดสอบ wire/DB 25 ตัวผ่านทั้งหมด) แต่กลไก
เดียวกันนี้ (`RE-128`) ไม่เคยถูกยืนยันด้วยตาที่ฉากนี้มาก่อน -- bg0001 มี `GT-078`/วิดีโอเจ้าของ + `GT-131`
PASS, bg0002 มีภาพถ่าย Sebastian/Pike, แต่ bg0004 ไม่มีหลักฐาน client-observable ใด ๆ เลย ใบนี้เปิดไว้
ตามกฎ "เจอสิ่งที่ไม่รู้ ให้เปิดใบ ไม่ใช่หยุดสร้างของเพื่อค้นเอง"

**สถานะ BLOCKED-ON-WIRING:** ตัวประกอบยังไม่ถูกเรียกจาก `runtime.py` (ไฟล์ของ chief) และ
`login_entry_allowed` ของฉาก 4 ใน `scenarios/world_scene_registry_001.json` ยังเป็น `false` ตามคำสั่ง
ตรงของ COO-DECISION เดียวกัน ("ยังไม่แก้ login_entry_allowed ... จนกว่าตัวประกอบจะพร้อมจริง") -- ใบนี้
เทสไม่ได้จนกว่าจะมี `CORE-REQUEST` ต่อสายและเปิดประตูฉากในรอบถัดไป บันทึกไว้ล่วงหน้าเพื่อไม่ให้ต้องเปิดใบ
ใหม่ทีหลัง

### objective

หลังต่อสาย (chief) + เปิดประตู (LANE-A) แล้ว ให้ผู้เทสเข้าฉาก 4 (Slave Market Island) แล้วดูว่า NPC ที่
ปรากฏตรงกับตารางที่คำนวณไว้หรือไม่ -- ตัวอย่างชื่อที่ควรเห็น: Columbus (ท่าเรือ), Angelina (Princess
Slave), Aston/Hood (Slave Traders), กลุ่มทาสหลายคน, Orc/Dragon Gladiator/Scythe Beetle ในเขตมอนสเตอร์

### pass criteria

**ชั้น client-observable:**
- ชื่อ/ตำแหน่ง NPC อย่างน้อย 3 ตัวที่เจ้าของยืนยันด้วยตาตรงกับตารางที่ประกอบไว้ ⇒ ยืนยัน crosswalk
  ใช้ได้กับฉากนี้ด้วย (ไม่ใช่แค่ bg0001/bg0002)
- ชื่อไม่ตรง หรือ NPC ที่เห็นไม่ใช่ตัวที่ตารางทำนาย ⇒ `RE-128`'s mechanism อาจไม่ generalize ข้ามฉาก
  แบบตรงไปตรงมา ต้องกลับไปดู `CLINE` join ใหม่

**ชั้น wire/DB (ทำได้ตอนนี้โดยไม่ต้องรอ attended):** `python3 -m unittest tests.test_scene4_slave_market_tables tests.test_world_population_bg0004`
ผ่านครบ 25/25 (`assembled=84/84`, `unresolved=32`) -- นี่คือ headless proof ที่พร้อมให้ดูก่อนเปิดจอ
ตามธรรมเนียมของโปรเจกต์ (`PANYA-DECISION 2026-08-27 20:10`)

### nonclaims

1. ไม่อ้างว่า 84 ตัวที่ประกอบได้คือทั้งหมดที่ฉากนี้ควรมี -- 32 placement ยังไม่ resolve (ดู docstring
   ของ `scene4_slave_market_tables.py` สำหรับเหตุผลแยกตามกลุ่ม)
2. ไม่อ้างว่าตัวประกอบพร้อมส่งจริงวันนี้ -- ยังไม่ต่อสายเข้า `runtime.py`, ยังไม่เปิด `login_entry_allowed`
3. ไม่อ้างว่าความสอดคล้องเชิงธีม ("Slave Market" มีชื่อ "slave buyer"/"Princess Slave") คือหลักฐาน
   client-observable -- เป็นการอ่าน pattern ของสายนี้เท่านั้น จนกว่าจะมีคนดูจริง

### links

`notes_to_chief/20260830_1441_COO-DECISION-scene4-slave-market-first-door.md` ·
`notes_to_chief/20260830_1434_LANE-A-STATUS-r236-gate-verified-narrow-plus-door-priority-recommendation.md` ·
`src/pirateforce_foundation/scene4_slave_market_tables.py` ·
`src/pirateforce_foundation/world_population_bg0004.py` ·
`GT-131` (bg0001 precedent, PASS) · `RE-128` (the crosswalk mechanism, closed)

**ผู้เปิดใบ: LANE-A (สาย A · WORLD) รอบ `s3m1f7` 2026-09-01T11:4x+07:00**

## GT-192 GM-A-WARP-MULTI-MAP-CENSUS-CHAIN-001  [✅ **PASS สองชั้น · OBSERVER_CONFIRMED 2026-09-03T18:5x+07:00** (chief รอบ `pk14rf`/R326 เกรดตาม `COO-DECISION 20260903_1743` ข้อ 2 — ห้ามปั๊ม PASS จากช... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-193 SPEED-COMMAND-SPARSE-X7-001 [attended, in-game]: `/speed` ขั้น 9/10 (`1e40` / `fast`) -- บรรทัดปฏิเสธขึ้นจอจริงไหม ... -- archived 20260907 (CANCELLED by owner LANE-A round `lnq6xy` 2026-09-07T06:03+07:00; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md`) [พับ+ย้ายโดย LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00 · จดหมายเจ้าของใบ `notes_to_chief/20260907_0603_LANE-A-TO-K-gt151-and-gt193-both-cancelled.md` · เหตุผลของเจ้าของใบคำต่อคำ (สามข้อ ข้อแรกข้อเดียวก็พอ): (1) ขั้นที่ใบยังเกรดได้ (9 และ 10) วัดของที่ถูกปักไว้ headless บน main แล้วทั้งชุด — `tests/test_gm_speed_denied_nine_paths.py` มี `test_path_4_unparseable_value` (รูปของขั้น 10) และปักครบถึง `test_path_11_row_not_touched` ⇒ ตรงเกณฑ์ (ค) ของ `PANYA-ORDER 0159` 'มีผลใหม่ครอบคลุมแล้ว' (2) ขั้น 4-7 เกรดไม่ได้ตั้งแต่ต้น (`PENDING interface`) ⇒ ใบที่เกรดได้ 2 ขั้นจาก 10 และทั้งสองขั้นซ้ำกับหมุด headless = ใบที่เผารอบ (3) ประตูที่ชื่อใบพูดถึงปิดไปแล้ว — `41e347b3` ปิดประตู sparse `/speed` และ `28efa1af` ใส่ `PF_SPEED_TRIAL` แทน · 🔴 **สิ่งที่ต้องไม่หายไปกับใบ (คำของเจ้าของใบ)**: คำถาม "บรรทัดปฏิเสธของ `/speed` ขึ้นบนจอจริงไหม และขึ้นที่ไหน" **ยังมีค่าอยู่** แต่ `GT-193` ตอบไม่ได้อีกแล้วเพราะขั้นตอนอิงประตูเก่า ⇒ ถ้าต้องการคำตอบนั้น **ให้เปิดใบใหม่ที่วัดโค้ดวันนี้ (11 path ไม่ใช่ประตู sparse) และเจ้าของใบใหม่ควรเป็น LANE-GM ไม่ใช่ LANE-A** — ห้ามปลุกใบนี้ · nonclaim ของเจ้าของใบ: ไม่ได้รันชุดเทสนั้นในรอบที่ตัดสิน (อ่านชื่อเทสจากไฟล์บน main) ⇒ อ้างว่า 'หมุดพวกนี้มีอยู่' ไม่ใช่ 'เขียววันนี้' · 🔴 K ไม่ได้ยกเลิกใบเอง คัดลอกคำตัดสินของเจ้าของใบอย่างเดียว · คืนที่นั่งรถบัส 1 ที่]
## GT-198 GROUND-DROP-MODEL-TYPE-FIELD-RENDER-CHECK-001  [❌ **CANCELLED - covered by GT-216** (🟢 PASS สองชั้น · `OBSERVER_CONFIRMED 2026-09-03T16:51+07:00`) **+ ผลรอบ attended R309** `notes_to_chief/2... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-199 CORPSE-REARM-AND-DROP-CROSS-SCENE-SCOPE-001  [PENDING -- รอ merge ก่อน · ครึ่ง B ถอนแล้ว]

🔴 **แก้ใบโดย chief รอบ `clw1zb` (R297) ก่อนใครเทส — อ่านสามบรรทัดนี้ก่อนอย่างอื่น:**
1. **ครึ่ง B (ของไม่ตามข้ามฉาก) ถูกถอนออกก่อน push** หลัง pf-adversary ⇒ **ห้ามเทสครึ่ง B** จะไม่มีอะไรเปลี่ยน
   และ `PF-EVENT mob_loot_scene_reconcile_cleared_*` **จะไม่ปรากฏ** (ไม่ใช่ FAIL ของใคร คือของที่ไม่ได้ส่ง)
   เหตุผล + คำถามที่ค้างอยู่กับ COO: `notes_to_chief/20260902_0245_CHIEF-ASK-COO-drop-cross-scene-option1-vs-option2-*`
2. **ครึ่ง A (ศพไม่ลุกกลับเป็นท่ากำลังตาย) ยังใช้ได้ตามใบทุกบรรทัด** — เทสได้เมื่อ merge แล้ว
3. 🔴 **ใบนี้ไม่ได้ขยับ NOW.md P-1 และไม่เคยขยับ** — `COO-DECISION 20260901_2148` เขียนเองว่า "P-1/P-2/P-3 ไม่ผูกกับเรื่องนี้"
   ถ้อยคำเดิมของใบที่บอกว่าเป็น "งานใต้ฝากระโปรงของ P-1" ให้อ่านว่า **แก้บั๊ก P0-5 เฉย ๆ**
   (เกณฑ์ "เก็บได้" ของ P-1 ยังต่อสายไม่ได้เลย: `runtime.py` ไม่มี call site ของ pickup) · ดู `20260902_0248_CHIEF-CORRECTION-*`

- objective: ข้อพิสูจน์เดียว: การต่อสายสอง bounded fix ของ P0-5 ใน `runtime.py` (chief รอบ `clw1zb`/R297)
  ให้ผลตามที่ตั้งใจ **ต่อหน้าไคลเอนต์จริง** ไม่ใช่แค่ในเทสไลบรารี
  (A) CORPSE RE-ARM: เดิม `dead_timer` เป็น scalar เดียวที่ใช้กับทุกแถวที่ตายแล้ว ⇒ การ compose เฟรม
  DYING ของศพใหม่ re-arm ศพเก่าทุกตัวกลับเป็น "กำลังตาย" · การต่อสายส่ง `transitioning=(scene,
  actor_identity)` ⇒ กระทบเฉพาะแถวของคอลนั้น
  (B) DROP CROSS-SCENE: drop ledger ไม่มี scene term ⇒ ของที่ยังวางบนพื้นฉาก A ตามไปประกอบ publication
  ของฉากถัดไป · การต่อสายเรียก `mob_loot_cell.reconcile_scene_transition()` หนึ่งครั้งที่ขอบฉาก
  🔴 กฎ "หนึ่งใบหนึ่งข้อพิสูจน์": A กับ B ต้องถูก **เกรดและบันทึกแยกกัน** (A PASS/B FAIL เกิดได้)
  รวมไว้ใบเดียวเพราะเป็นการต่อสายก้อนเดียวในบูตเดียว · ได้ผลแค่ครึ่งเดียว = อีกครึ่งยังเปิด ให้เปิดเป็น
  "ใบถัดไป" (ห้ามจองเลข)
- 🔴 รอ merge ก่อน: โค้ดต่อสาย **(เฉพาะครึ่ง A)** อยู่ repo `pirate-force-server` branch `claude/beautiful-shannon-clw1zb`
  (จาก CODEX_URGENT 2026-09-01T20:40+07:00 · COO-DECISION 2026-09-01T21:48+07:00 · ไลบรารีโดย LANE-B)
  **ต้องอยู่บน `main` ก่อนบูตเท่านั้น** ดู RECHECK ข้างล่าง ห้ามบูตจาก branch
- 🔴 ประตูของ NOW.md: หัวไฟล์นี้สั่งว่า "GT-146 และใบตีมอนสเตอร์ทั้งหมด ห้ามเสนอเข้าคิว attended จนกว่า
  P-1 และ P-2 จะเสร็จ" · ใบนี้ต้องฆ่ามอน ⇒ **ห้ามยกขึ้นหัวคิว ห้ามเรียกผู้เทส จนกว่าเจ้าของ/COO เคาะว่า
  ใบยืนยัน P-1 เองได้รับยกเว้น** (COO-DECISION 20260901_2148 ยกเว้นให้เฉพาะ "การแก้บั๊กใต้ฝากระโปรง"
  ของ LANE-B ไม่ได้พูดถึงใบเทส attended) · สถานะคง PENDING จนได้คำเคาะ
- db: default `state\pirateforce.sqlite3` -- สำเนาเสมอ ห้ามเปิดไฟล์ canonical
  `copy state\pirateforce.sqlite3 state\run_gt199.sqlite3` · จด sha256 ของสำเนาก่อน/หลัง และยืนยันว่า
  sha256 ของไฟล์ canonical เหมือนเดิมก่อน/หลัง (ตำแหน่งตัวละคร reset ไป spawn ทุกบูตเป็นเรื่องปกติ)
- server args: บูตปกติไม่มีแฟล็ก hypothesis ใด ๆ + `--export-events` (ตัวส่งออก event เป็น diagnostic
  ล้วน ไม่แตะ dispatch):
  `$env:PYTHONPATH = Join-Path (Get-Location) 'src'`
  `py -3 -u -m pirateforce_foundation.app --db state\run_gt199.sqlite3 --export-events`
  เซิร์ฟเวอร์ต้องเพิ่งสตาร์ท (< 3.5 นาที) แล้วค่อยบูตไคลเอนต์ · ถ้ารอบก่อนฆ่าไคลเอนต์ทิ้ง **ต้องรีสตาร์ท
  เซิร์ฟเวอร์ก่อนเสมอ** ไม่งั้นไคลเอนต์ใหม่ค้างที่ "connecting" ตลอดกาล
- steps:
  1. RECHECK ผ่านก่อน · บูตเซิร์ฟเวอร์ แล้วบูตไคลเอนต์ · ล็อกอิน
  2. จัดมุมกล้องด้วย **right-click-drag เท่านั้น** (หมุนกล้อง ไม่เปลี่ยนการหันหน้าของตัวละคร ไม่ส่ง
     ไบต์ออกสาย ใช้เป็นตัวเช็คว่าไคลเอนต์ยังไม่ตายได้ทุกจังหวะ) · ยังไม่กด `W/A/S/D` และไม่กด `Q`/`E`
     (สองอย่างนี้เปลี่ยนการหันหน้าของตัวละครและส่ง TargetPosVital)
     ภาพ BASELINE ความละเอียดเต็ม + จด scene/X/Y/Z จาก HUD + **สีป้ายชื่อทุกป้ายในเฟรม บรรทัดละหนึ่งป้าย
     เขียน "none" ออกมาถ้าไม่มี** (อ่านสีจากภาพนิ่งความละเอียดเต็มเท่านั้น ห้ามอ่านจาก contact sheet /
     ภาพย่อ / วิดีโอ)
  3. [A] ฆ่ามอนตัวที่ 1 · เมื่อศพนิ่งแล้วถ่าย PHOTO-A1: ท่าศพเป็นอย่างไร (นอน/ค้างท่ากลางอากาศ) + สีป้าย
     ทุกป้าย + เวลานาฬิกา
  4. [A] ฆ่ามอนตัวที่ 2 ในฉากเดียวกัน โดย **ให้ศพตัวที่ 1 อยู่ในเฟรมตลอด** · อัดวิดีโอตั้งแต่ตัวที่ 2
     เริ่มตายต่อไปอีกอย่างน้อย 25 วินาที · ถ่าย PHOTO-A2 ที่ ~+2 วิ และ PHOTO-A3 ที่ ~+22 วิ หลังตัวที่ 2
     ตาย (ทั้งสองภาพจดสีป้ายทุกป้าย) · คำถามเดียวที่ผู้เทสตอบ: ศพตัวที่ 1 เล่นท่ากำลังตายใหม่ / ลุก /
     ป้ายกลับมา หรือไม่ (ใช่ / ไม่ใช่ / มองไม่ทัน)
  5. [B] ให้มีของตกบนพื้นฉากนี้แล้ว **ห้ามเก็บ** · จด icon + ตำแหน่งคร่าว ๆ ของชิ้นที่ติดตาม ถ่าย PHOTO-B1
     (เห็นโมเดลของบนพื้นไหม + สีป้ายทุกป้าย)
  6. [B] เปลี่ยนฉาก ด้วยเส้นทางที่พิสูจน์แล้วในบิลด์นี้: GM `/warp <mapnum>` (`GT-182` PASS)
     🔴 คลิกช่องแชทให้โฟกัสก่อนพิมพ์เสมอ -- ตัวอักษรที่พิมพ์ตอนช่องแชทไม่โฟกัสจะกลายเป็นฮอตคีย์
     (คำสั่ง GM ไม่ใช่ trigger แชท 12 ตัวอักษร ไม่ต้องนับความยาว) · เปลี่ยนฉากไม่ได้เลย = NO-RESULT
     (ทางเข้าไม่เปิด) ไม่ใช่ FAIL
  7. [B] ถึงฉากใหม่: กวาดมุมกล้องด้วย right-click-drag แล้วถ่าย PHOTO-B2 -- มีของชิ้นจากฉากเดิมนอนอยู่
     บนพื้นไหม (โมเดลหรือป้ายชื่อไอเทม) + สีป้ายทุกป้าย · จากนั้นฆ่ามอนหนึ่งตัวในฉากใหม่ ถ่าย PHOTO-B3
     ทันทีที่ของตก: บนพื้นมีเฉพาะของจากการฆ่าครั้งนี้เท่านั้นใช่ไหม + สีป้ายทุกป้าย
  8. จดเวลานาฬิกาทุกขั้น · เก็บ log คอนโซลทั้งบูต · ทำ teardown เสมอแม้รอบจบเพราะเลิกเล่นกลางคัน
     (เทมเพลตปฏิเสธแสตมป์บูตที่เก่ากว่า 420 นาที)
- pass criteria:
    wire/DB (headless ไม่ต้องใช้ตาคน):
      A1. บน `main` หลัง merge: regression ของ LANE-B ผ่าน (คำสั่งใน RECHECK) -- พิสูจน์ระดับไลบรารีเท่านั้น
      A2. คอนโซลบูตนี้: การตายครั้งที่ 2 มี `MOB_SCENE_RECOMPOSE ... state=composed ... fatal=no` และ
          `wire=` ไม่ขึ้น `MISMATCH` ทั้งสองคอล · `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE_DYING` และ
          `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE` มี `target=<identity ตัวที่ 2>`
          🔴 `dead_timer=` ในบรรทัดนั้นพิมพ์ scalar ที่ "ขอ" ไม่ใช่ค่าที่ลงแต่ละแถว **ห้ามใช้เป็นข้อพิสูจน์
          ของ scoping** · ตัวชี้ขาดฝั่งสายจริงคือ diff สองเฟรม census ของการตายครั้งที่ 2: ต้องต่างกันที่
          actor entry เดียว คือ identity ที่ `target=` บอก ส่วน entry ของศพตัวแรกต้องเหมือนกันไบต์ต่อไบต์
          ไม่มี capture = เขียนว่า "ไม่ได้วัด" ห้ามเดา
      B1. `PF-EVENT <n> mob_loot_scene_reconcile_cleared_<N>` ปรากฏ **หนึ่งครั้ง** ตอนข้ามฉาก โดย N =
          จำนวนแถวที่ยังอยู่บนพื้นฉากเดิม
      B2. บรรทัด `MOB_DROP_PRESENCE` ของการฆ่าครั้งแรกในฉากใหม่: `carried=0` และ `live=` เท่ากับจำนวนที่
          เพิ่งตกในฉากใหม่เท่านั้น
    client-observable (ต้องมีคนอยู่หน้าจอ · G-OBS):
      A. จาก PHOTO-A1/A2/A3 + วิดีโอ ผู้เทสรายงานว่า ศพตัวที่ 1 **ไม่** กลับไปเล่นท่ากำลังตายตอนตัวที่ 2
         ตาย = PASS ของครึ่ง A · เห็นศพตัวแรกกลับเป็น "กำลังตาย" = FAIL ของครึ่ง A · ศพหลุดเฟรม/มองไม่ทัน
         = NO-RESULT
      B. จาก PHOTO-B2/B3 ผู้เทสรายงานว่าไม่มีของจากฉากเดิมนอนอยู่บนพื้นฉากใหม่ = PASS ของครึ่ง B ·
         เห็นของจากฉากเดิม = FAIL ของครึ่ง B
      ทุกภาพต้องมีบรรทัดสีป้ายครบทุกป้าย ("none" เขียนออกมา ไม่เว้นว่าง) · ความต่างจากสกรีนช็อตเซิร์ฟเวอร์
      จริงลง `REAL_SERVER_DIVERGENCE.tsv` แถวละหนึ่งรายการ
      จดหมายผลต้องมีบรรทัด `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ไม่งั้นปิดใบไม่ได้ (G-OBS)
    [คำทำนายของผู้เขียนใบ -- เป็นคำทำนาย ไม่ใช่ผล]: คาดว่า A ผ่านและ B ผ่าน · ผลลบมีค่าเท่าผลบวก:
      A FAIL ⇒ ชี้ว่ามีเส้นทาง compose ที่สองที่ยังไม่ได้ส่ง `transitioning` หรือคอลจริงไม่ใช่คู่นี้
      B FAIL ⇒ ชี้ว่า reconcile ไม่ได้ถูกเรียกที่ขอบฉากจริง หรือถูกเรียกหลัง publish แรกของฉากใหม่
- nonclaims:
  1. การล้าง ledger **ทั้งก้อน** ที่ขอบฉาก เป็นด้านอนุรักษ์นิยมของคำถาม authenticity ที่ CODEX_URGENT เอง
     ติดป้าย RECONSTRUCTED/OPEN -- **ไม่ใช่ข้ออ้างว่าเซิร์ฟเวอร์ต้นฉบับทำแบบนี้** · ผลข้างเคียงที่ตั้งใจ:
     ผู้เล่นที่ออกจากฉากแล้ววกกลับเข้าฉากเดิมทันที **จะไม่เจอของที่ตัวเองเพิ่งทำตกรออยู่** · เห็นอาการนี้
     = พฤติกรรมที่ใบนี้คาดไว้ ไม่ใช่บั๊กใหม่ และไม่ใช่ FAIL ของใบนี้
  2. ไม่ปิด NOW.md **P-1** ("ของดรอปต้องค้างอยู่บนพื้นนานพอที่จะเห็นและเก็บได้") · ใบนี้เป็นงานใต้ฝากระโปรง
     ของ P-1 แต่เกณฑ์ของ P-1 เอง -- ของค้างอยู่นานพอให้เห็นและเดินไปเก็บได้ **ภายในฉากเดียว** -- เป็นคำถาม
     คนละข้อที่ใบนี้ไม่ตอบ (ดู `GT-188`, `GT-149`)
  3. ไม่พิสูจน์ pickup/removal ของชิ้นสุดท้าย (ข้อ 3 ของ CODEX_URGENT ยังเปิด · ห้าม resend และห้าม guessed
     count-zero clear) -- นั่นคือ `GT-146` ของมันเอง
  4. ไม่พิสูจน์ว่า `20.0` วิ / 700 ms / 120 วิ เป็นค่าของเซิร์ฟเวอร์ต้นฉบับ
  5. ไม่สรุปสาเหตุของสีป้ายใด ๆ -- จดสีอย่างเดียว (`RE-067`)
  6. ไม่พิสูจน์เรื่องโมเดล 3 มิติของของบนพื้น (`GT-198`) และไม่พิสูจน์ heartbeat preserve (`GT-188`)
  7. ไม่รับประกันว่าการฆ่าจะดรอปของ (สุ่ม) · ฆ่าแล้วไม่ตกของ = NO-RESULT ของครึ่ง B ไม่ใช่ FAIL
  8. ไม่พิสูจน์เส้นทางเปลี่ยนฉากเอง (`/warp` เป็นของ `GT-182`/`GT-192`)
- RECHECK:
  ```
  cd pirate-force-server && git fetch origin && \
  git show origin/main:src/pirateforce_foundation/runtime.py | grep -n "transitioning=death_transitioning" && \
  python3 -m pytest tests/test_mob_corpse_rearm_wired.py tests/test_mob_scene_recompose.py -q
  ```
  ต้องผ่านทั้งสองส่วน · ผลว่าง/แดง = ยังไม่ merge ⇒ ห้ามบูต ให้รายงานกลับแทน
  🔴 **ห้ามเช็ค `reconcile_scene_transition()`** — ครึ่ง B ถอนแล้ว มันจะไม่มีอยู่บน main และนั่นถูกต้อง
- links: `notes_to_chief/CODEX_URGENT_20260901_2040_P05-CORPSE-DROP-STATE-SCOPE.md` ·
  `notes_to_chief/20260901_2148_COO-DECISION-corpse-rearm-and-cross-scene-drop-bounded-fix-to-lane-b.md` ·
  `notes_to_chief/20260901_2255_LANE-B-STATUS-corpse-rearm-and-drop-cross-scene-bounded-fixes-built-core-request-for-wiring.md` ·
  `runtime.py` (หาโดยชื่อ ไม่ใช่เลขบรรทัด: `_sync_combat_scene_state` / `death_transitioning`) ·
  `mob_loot.reconcile_scene_transition` (module fn + cell method) · `GT-188` · `GT-198` · `GT-149` ·
  `GT-146` · `GT-182` · `RE-067`
- numbering: ตามคำสั่งค้นหาเดียว (กฎ ② หัวไฟล์นี้) -- สูงสุดใน `GAME_TEST_QUEUE.md` = `GT-198`,
  ใน `CLIENT_RE_QUEUE.md` = `RE-198`, ใน `archive/*QUEUE*ARCHIVE*.md` ไม่มีเลข >= 190 และ grep ทั้งรีโปหา
  `GT-199|RE-199` ไม่พบไฟล์ใดเลย ⇒ ใบนี้คือ `199`
- result: (ผู้เทสกรอก: PASS/FAIL/BLOCKED/NO-RESULT แยก **ครึ่ง A** และ **ครึ่ง B** คนละบรรทัด + evidence +
  timestamp + บรรทัด `OBSERVER_CONFIRMED` ตาม G-OBS)

## GT-200 CENSUS-NPC-LEVEL-LABEL-MULTI-SCENE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS (R307 2026-09-03 — เดินครบ 11 ฉากตามใบ arrival census ตรงเกณฑ์ทุกฉาก) ·... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-202 CENSUS-NPC-QUEST-MARK-GATE-WALK-SPEED-001  [**WITHDRAWN / OPENED-IN-ERROR** -- ถอนหัวใบโดย LANE-A (เจ้าของใบ) รอบ `2p4n3h` 2026-09-02T05:3x+07:00 ในรอบเดียวกับที่เปิด · **ไม่ต้องบูต ไม่ต้องมีผู้เทสทำอะไรทั้งสิ้น**] -- archived 20260907 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md`, LANE-K round `kxpzxi`)

## GT-203 AVATARATTR-NAMED-FIELDS-MATCH-THE-CREATION-SCREEN-001  [PENDING -- โค้ดยังไม่ขึ้น `main`: PR รอบ `qtxdpr` · **ไม่มีอะไรเปลี่ยนบนสาย** ใบนี้อ่านของที่เซิร์ฟเวอร์เก็บไว้อยู่แล้ว]

**ผู้เปิดใบ: LANE-A รอบ `qtxdpr` (2026-09-02T06:3x+07:00) · LANE-A บริโภคผลเอง**
**คำถามเดียวที่ใบนี้ตัดสิน:** ชื่อฟิลด์ที่ Codex ถอดไว้ใน `AvatarAttr` **ตรงกับสิ่งที่เธอกดเลือก
บนหน้าจอสร้างตัวละครจริงหรือไม่**

🔴 **ทำไมยังต้องเทส ทั้งที่ Codex ระบุ `PROVEN_EXACT`:** ทุกแถวมี `scope_status = UNKNOWN`
และ `source = IMAGE` (อ่านจากไบนารี ไม่ใช่จากแพ็กเกตจริง) · และรอบ `qtxdpr` วัดแล้วว่า
**สายแยกช่องที่รูปร่างเหมือนกันไม่ออก** (u32 สิบสี่ช่อง: บิต 0-11, 17, 20) ⇒ ที่บอกว่าช่องไหนคือ
`n_HRID` ช่องไหนคือ `n_SLOT_LHAND` คือคอลัมน์ `mask_bit` ของ Codex ล้วน ๆ **ไม่มีการวัดรองรับ**
· ใบนี้เดินทาง **จอ -> ไบต์** จึงไม่ต้องเปลี่ยนอะไรที่เซิร์ฟเวอร์ส่งเลย (14.13 (ง) ห้ามแก้ก่อนตรวจ)

### ต้องบูตไหม
บูตปกติตาม `BRIDGE_BOOT_PROCEDURE.md` · **ไม่ต้องเปิดแฟล็กอะไรทั้งสิ้น**
🔴 RECHECK ก่อนบูต บนโคลนที่ตาม `origin/main` แล้ว:
`python -c "import pathlib;print(pathlib.Path('src/pirateforce_foundation/world_avatar_attr.py').exists())"`
ต้องได้ `True` · ได้ `False` = ยังไม่ merge อย่าเพิ่งบูต

### ขั้นตอน (ประมาณ 10 นาที)
1. บูตเซิร์ฟเวอร์ + GameClient ตามปกติ **จำ path ของ `--db` ที่บูตใช้ไว้**
2. สร้างตัวละครใหม่ **สองตัว** ในบัญชีเดียวกัน ตั้งใจให้ต่างกันให้มากที่สุด:
   - ตัวที่ 1: **เพศหญิง** ทรงผม/ใบหน้าแบบ ก
   - ตัวที่ 2: **เพศชาย** ทรงผม/ใบหน้าแบบ ข (คนละแบบกับตัวที่ 1)
   ถ้าหน้าจอมีตัวเลือกอื่น (หมวก เสื้อ ขา ผิว สัดส่วนตัว) ให้เลือกต่างกันด้วยยิ่งดี
   🔴 **จดบนกระดาษหรือถ่ายภาพนิ่งว่าเธอกดอะไรไปบ้าง ก่อนกดยืนยัน** — นี่คือหลักฐาน
   ชั้น client-observable ของใบนี้ ไม่จด = ใบนี้ตัดสินอะไรไม่ได้เลย
3. ปิดเกม แล้วรันคำสั่งเดียวนี้ในโฟลเดอร์ `pirate-force-server` (อ่านอย่างเดียว):

```
python -c "import sqlite3,sys;sys.path.insert(0,'src');from pirateforce_foundation.world_avatar_attr import describe_avatar_body as d;c=sqlite3.connect('file:%s?mode=ro'%sys.argv[1],uri=True);[print(n,'|',d(bytes(a))) for n,a in c.execute('SELECT name,avatar_wire FROM characters WHERE deleted_at IS NULL ORDER BY selector')]" "<path ของ --db ที่บูตใช้>"
```

   🔴 `mode=ro` คือของจริง ห้ามตัดออก · ห้ามชี้ไปที่ canonical DB
4. คัดลอกบรรทัด `AVATAR_DECODE ...` ของทั้งสองตัว **ทั้งบรรทัด** ลงใบผล

บรรทัดที่ได้ขึ้นต้นว่า `AVATAR_DECODE len=... mask=0x... ` แล้วตามด้วยชื่อฟิลด์=ค่า 21 ช่อง

### เกณฑ์ตัดสิน (สองชั้น)
- **client-observable** = สิ่งที่เธอจดไว้ในข้อ 2 · **wire/DB** = บรรทัด `AVATAR_DECODE`

**ผ่าน** ต้องครบทั้งสี่ข้อ:
1. `n_GENDER_1_female_other_male` ของตัวหญิง = `1` และของตัวชาย **ไม่ใช่ `1`**
2. `n_HRID` (ผม) ของสองตัว **ต่างกัน** · `n_HDID`/`n_FCID` ต่างกันด้วย ถ้าเธอเลือกคนละแบบจริง
3. เปลี่ยนบนจอกี่อย่าง ต้องมีฟิลด์ต่างกันบนบรรทัดไม่น้อยกว่านั้น
   ⇒ เปลี่ยน 4 อย่างแต่บรรทัดต่างแค่ช่องเดียว = ไม่ผ่าน
4. `len=` ของสองบรรทัด **เท่ากัน** และ `mask` เท่ากันทั้งคู่

**ไม่ผ่าน** = ข้อใดข้อหนึ่งไม่จริง 🔴 **ผลลบมีค่าเท่าผลบวก** ไม่ผ่าน = การอ่านชื่อฟิลด์ของ
Codex ไม่ตรงกับสิ่งที่ไคลเอนต์เขียนจริง และ **ห้ามมีสายไหนเอาชื่อพวกนี้ไปต่อสาย**
จนกว่าจะมี RE ใหม่ · เขียนผลลบมาตรง ๆ ไม่ต้องเกลี่ย

🔴 **ของแถมที่อาจมีค่าที่สุด:** ตัวละครที่ **เธอ** สร้าง อาจมี `mask` ไม่ใช่ `0xFFFFFFFF`
และช่องข้อความสีไม่ว่าง ซึ่งเป็นบอดี้แบบที่ยังไม่เคยมีใครในโปรเจกต์นี้เห็นเลย
`len=` ไม่ใช่ 103 หรือ `mask` ไม่ใช่ `0xFFFFFFFF` = รายงานเป็นข้อแรก มีค่ากว่าผลผ่าน/ไม่ผ่าน

### สิ่งที่ใบนี้ **ไม่** ตัดสิน (อ่านก่อนอ้างผล)
1. **ไม่ตัดสินว่าเซิร์ฟเวอร์ตั้งค่าแล้วโมเดลบนจอเปลี่ยน** — คนละทิศ ดูหัวใบ
2. **ไม่แยกช่อง u32 ที่รูปร่างเหมือนกันออกจากกัน** ถ้าผลออกมาว่า "มีบางอย่างเปลี่ยน
   แต่คนละช่องกับที่คาด" นั่นคือหลักฐานว่าคอลัมน์ `mask_bit` ของ Codex ผิด ซึ่งเป็น
   ผลลัพธ์ที่ใบนี้อยากได้พอ ๆ กับผลผ่าน
3. ไม่แตะ P-1/P-2/P-3 · ไม่เกี่ยวกับสีชื่อมอนสเตอร์ · ไม่เกี่ยวกับ quest mark

## GT-204 MOB-DROP-LEFT-CLICK-PICKUP-INTO-BACKPACK-001  [❌ **CANCELLED - covered by GT-216** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2) — `GT-216` PASS บน... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-205 UI-A-BACK-BUTTON-VISIBLE-NOTICE-001  [🟡 **สถานะเดิม: client-observable = PASS · wire/DB = NOT MEASURED · ใบยังไม่ปิด** (ยกคำต่อคำจากประโยค "สถานะเดิม: ..." ที่ฝังอยู่กลางย่อหน้าเดิม ขึ้นมาไว้หน้าสุด — คำอื่นทุกคำในหัวใบเดิมคงเดิมทุกตัวอักษร ย้ายไปบรรทัด "ประวัติหัวใบเดิม" ด้านล่างแทน ไม่มีการเขียนสรุปใหม่) [จัดรูปแบบโดย LANE-K รอบ `x91eo8`/`x91eo8r2` ตามข้อเสนอ chief `R374` ข้อ 2]]

> **ประวัติหัวใบเดิมคำต่อคำ (ก่อนจัดรูปแบบรอบ `x91eo8`)**: 🟡 ไม่ยกเลิก — ครึ่ง wire ยังไม่ถูกวัดสำหรับ subcode ของใบนี้ (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2): `GT-211` พิสูจน์ composer ตัวเดียวกันบนสาย (`LANE_A_UIA_NOTICE_COMPOSED ... EXIT REFUSED` 66 ไบต์) แต่นั่นคือ **subcode ของปุ่มล็อกเอาต์** ไม่ใช่ subcode 3 ของใบนี้ ⇒ ไม่เข้าเงื่อนไข covered ทั้งสามรูป · 🔴 **เจ้าของใบ LANE-A เป็นคนตัดสินว่า subcode 3 ยังต้องวัดสายของตัวเองไหม** (เจ้าของสั่งไว้เองในใบ `1934`) — ตัดสินแล้วให้เขียนบรรทัดปิด/คงเปิดที่หัวใบนี้ในรอบเดียวกัน · ป้าย `BACK_REFUSED`→`EXIT` ที่ `COO 20260903_1746` ข้อ 2 สั่ง แก้เสร็จแล้วต้องอัปเดตสตริงในเกณฑ์ของใบนี้ด้วยในรอบเดียวกัน (`AGENTS.md` §7) · สถานะเดิม: **client-observable = PASS · wire/DB = NOT MEASURED · ใบยังไม่ปิด** — สถานะเขียนโดย LANE-A (เจ้าของใบ) รอบ `kozzu1` 2026-09-03T11:5x+07:00 · 🔴 **จงใจไม่เขียน `✅ PASS` เดี่ยว ๆ**: เกณฑ์ของใบนี้เขียนเองว่า "TWO layers -- neither layer may ever be offered as proof of the other" และรอบ R303 วัดมาชั้นเดียว ⇒ ปั๊ม PASS ทั้งใบคือรูปเดียวกับหนี้ `GT-192` ที่ถูกบันทึกว่าจ่ายสองรอบ (ผู้ตรวจ pf-adversary รอบ `kozzu1` D3) · **ตัวปิดใบเหลืออะไร: คัดโทเคน `LANE_A_UIA_NOTICE_COMPOSED` จากคอนโซล + ตารางสีป้ายชื่อตามเกณฑ์ + ระบุว่าบรรทัดขึ้นที่พาเนลไหน** — สามอย่างนี้เก็บได้ฟรีในรอบ attended ถัดไปที่บูตอยู่แล้ว ไม่ต้องบูตเพื่อใบนี้ใบเดียว · 🔴 **คำตัดสินของเจ้าของใบ (LANE-A รอบ `gs8hmn` 2026-09-03T22:5x+07:00 ตาม `PANYA-DECISION 20260903_1934` + chief `20260903_2010`): คงเปิด แต่เป็น "เก็บฟรี" เท่านั้น — **ห้ามบูตรอบ attended เพื่อใบนี้ใบเดียว ไม่ว่ากรณีใด** ถ้ารอบ attended ถัดไปจบโดยไม่มีใครบูตอยู่แล้ว ใบนี้ค้างต่อได้ ไม่นับว่าใครค้าง · เหตุผลที่ไม่ปิด: เกณฑ์ของใบนี้เขียนเองว่าสองชั้น และชั้น wire ของ **subcode 3** ยังไม่เคยถูกวัด — `GT-211` วัด subcode ของปุ่มล็อกเอาต์ ไม่ใช่ subcode นี้ (chief ตัดสินแล้วว่าไม่เข้า covered ทั้งสามรูป) ปิดตอนนี้ = ปั๊ม PASS จากชั้นเดียว รูปเดียวกับหนี้ `GT-192` · เหตุผลที่ไม่ให้บูตเพื่อใบนี้: เวลา attended คือทรัพยากรที่แพงที่สุด (`1934`) และตัวปิดสามอย่างที่เหลือเก็บได้จากคอนโซลของบูตใด ๆ ที่มีอยู่แล้ว · 🔴 **กฎ grep `AGENTS.md` §7 ไม่เข้าเงื่อนไขกับใบนี้ วัดแล้วไม่ใช่เดา**: การเปลี่ยนชื่อป้ายรอบ `omhpqj` แตะปุ่ม UI-B ปุ่มเดียว (`UIB_ACTION_LABEL`) · ป้ายของ UI-A ยังเป็นสตริงเดิมของ chief เป๊ะ (`world_logout_button_notice.py:503` `UIA_ACTION_LABEL = "LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE"`) และบรรทัดเดียวที่ chief ยังจะสลับ (~~`runtime.py:7033`~~ **เลขบรรทัดนี้เน่าแล้ว จริงคือจุดที่ประกอบ `uia_notice_actions` ในสาขา `nested_id == LOGOUT_VITAL_ID` — grep เอา อย่าใช้เลข**) อ่านค่าเดียวกันนั้นกลับมา ⇒ **สตริงที่ใบนี้ grep (`LANE_A_UIA_NOTICE_COMPOSED` และ `BACK REFUSED`) ไม่ถูกแตะทั้งก่อนและหลังที่ chief สลับ ไม่ต้องแก้เกณฑ์ข้อไหน**
>
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
## GT-207 GM-PLUGIN-THREE-CELL-BUTTON-001  [**PASS** on build 1 -- ka1-A/เจ้าของ 2026-09-02T18:54+07:00 · `OBSERVER_CONFIRMED` มีในใบผล · ผล: `notes_to_chief/20260902_1915_KA1A-GT-207-PASS-the-gm-butt... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-210 CHOOSE-NPC-SCENE3-CLICK-ANSWER-001  [✅ **PASS · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — R306 บนจอเจ้าของ (`no... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-211 UI-B-EXIT-BUTTON-VISIBLE-NOTICE-001  [✅ **PASS สองชั้น · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — R306: `EXIT ... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-212 CHOOSE-NPC-NINE-ROSTER-ISLANDS-CLICK-ANSWER-001  [✅ **PASS · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — R306 บนจ... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-213 COLUMBUS-SCENE-GUARDS-VISIBLE-COST-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS on (A) และ (B) · (C) NO-RESULT ตามที่ใบอนุญาตเอง — R307 2026-09-03: (A) scene14 Columbus เงียบไม่มีคำถาม · (B) harbour Columbus เปิด Story 2 ตัวเลือก กด 1 → วาร์ปเข้า 'Ship in the Sea' ทันที · (C) กลับ Port Royal เดิม แต่ `columbus_q3021_crossing_row_checkpointed` printed 0 ครั้ง = NO-RESULT ตามกติกาใบเอง · 🔴 finding: ตำแหน่งไม่ persist หลังไปฉาก 126/17 (save=0) แล้วไม่กลับมาเขียนตอนคืนฉาก 1 · จาก notes_to_chief/20260903_1901_KA1A-R307-*.md · 🟢 READY (R306, 2026-09-02T17:2x+07:00) -- RECHECK ข้อ 1-2 **ผ่านแล้ว** (`server#584` merge 09:42Z ⇒ `COLUMBUS_Q3021_TELEPORT_REFUSED` และ `COLUMBUS_CHOOSE_NPC_WRONG_SCENE` อยู่บน `main`) · ข้อ 3 (`columbus_q3021_crossing_checkpoint` = ครึ่ง `/warp 1`) **ยังไม่อยู่บน `main`** — เป็น PR ของรอบ R306 ที่ยังไม่ merge ตอนเขียนบรรทัดนี้ · 🔴 **รัน RECHECK ทั้งสามข้อก่อนบูตเสมอ** ข้อ 3 ว่างเมื่อไหร่ ครึ่ง `/warp 1` เป็น `NO-RESULT` ตาม (C) ไม่ใช่ FAIL และครึ่งฉาก 14 ยังตัดสินได้ตามปกติ]

> เปิดโดย chief (LANE-E) รอบ `kt05o0`/R305 ตาม `COO-DECISION 20260902_1347` · **chief บริโภคผลเอง**
> numbering: กฎ ② หัวไฟล์ --
> `grep -ohE '\b(GT|RE)-[0-9]{3}\b' GAME_TEST_QUEUE.md CLIENT_RE_QUEUE.md archive/*QUEUE*ARCHIVE*.md | grep -oE '[0-9]{3}$' | sort -n | tail -1`
> คืน `211` (`GT-211`) ตอนเปิดใบ ⇒ ใบนี้เปิดเป็น `212` แล้ว **ขยับเป็น `213`** ตอน rebase ตามกฎ ③ (คนที่ push ทีหลังขยับ): LANE-A รอบ `gwwpmr` push `GT-212` ขึ้น main ก่อน · `RE-206` เพิ่งปิดรอบนี้ · `RE-210` มีอยู่จริง · ทั้งคู่ไม่ชนเลขนี้
> teardown ตาม `ATTENDED_SESSION_RUNBOOK.md` -- ต้องรันเสมอ แม้รอบจบเพราะเจ้าของเลิกเล่นเฉย ๆ

- objective: ข้อพิสูจน์เดียว ตัดสินด้วยตาคน -- ประตูกันฉากของสาย Columbus M2 **ปฏิเสธเฉพาะสิ่งที่ผิด และไม่ริบสิ่งที่ผู้เล่นเคยได้**:
  ข้ามจากบ้าน (ฉาก 1) ไปฉาก 17 ได้เหมือนเดิม แล้ว `/warp 1` กลับมา **Port Royal ต้องมีชาวเมือง ไม่ใช่เมืองร้าง** ·
  ตัวควบคุมอยู่ในข้อพิสูจน์เดียวกัน: คลิก actor ที่ **placement index 1 ของฉาก 14** ต้อง **ไม่เปิดบทสนทนา และไม่วาปไปไหน**

- ของที่รอ merge (ยังไม่อยู่บน `main` ตอนเขียนใบ):
  (A) op1/quest 3021 ถูกปฏิเสธเมื่อแถว in-memory ไม่ใช่ฉาก 1 · event `columbus_q3021_teleport_refused_wrong_scene_<n>`
      + stderr `COLUMBUS_Q3021_TELEPORT_REFUSED scene=<n> reason=not_home_scene`  (PR `server#584`)
  (B) ChooseNPC บน actor ที่ใช้ placement index เดียวกับ Columbus ในฉากอื่น ถูกปฏิเสธแบบมีชื่อ ·
      event `columbus_choose_npc_wrong_scene_<n>_lane_declined` + stderr `COLUMBUS_CHOOSE_NPC_WRONG_SCENE scene=<n> effect=columbus_lane_declined`
      🔴 คำว่า `lane_declined` ไม่ใช่ `no_reply` โดยตั้งใจ: **สายอื่นตอบคลิกนั้นจริง** (ฉาก 14 = `LANE_A_CHOOSE_NPC_SCENE14_FACE_P1`,
      ฉากโรสเตอร์ = `V98_NPC_CONVERSATION_DEFAULT_P1`) โทเคนนี้บอกได้แค่ว่า **สาย Columbus ไม่ตอบ** ห้ามอ่านว่า "ไม่มีอะไรตอบ"
  (C) D3 (PR `server#587`): checkpoint ตำแหน่ง = ฉาก 17 ตอนข้ามจริง · 🔴 **ถ้า (C) ยังไม่ลง แถว in-memory ยังเป็นฉาก 1 หลังข้าม
      ⇒ `/warp 1` ไม่ถูกนับเป็นการข้ามฉาก ⇒ census latch ไม่ถูกปลด ⇒ Port Royal ว่างได้ · กรณีนั้น = `NO-RESULT` ของครึ่งนั้น ไม่ใช่ FAIL**

- 🔴 สองข้อที่ไม่รู้แล้วเสียรอบ:
  1. โทเคน (B) พิมพ์ได้ **เฉพาะก่อนคุยกับ Columbus ที่ท่าเรือครั้งแรกของเซสชัน** (แลตช์ `columbus_quest3021_conversation_sent` อยู่ทั้งเซสชัน)
     ⇒ **ทำฉาก 14 ก่อน แล้วค่อยกลับบ้าน** · และพิมพ์ **ครั้งเดียวต่อฉาก** ต่อให้คลิกสิบครั้ง
  2. หลังวาปทุกครั้ง **เดินหนึ่งก้าว** (`W`/`S`) ก่อนตัดสินว่าฉากว่าง -- ฉาก 1 เป็นเคส walk-before-census (`GT-192`)

- RECHECK (ตัดสินด้วยเนื้อโค้ด ห้ามเทียบเลข commit):
  ```
  cd pirate-force-server && git fetch origin
  git show origin/main:src/pirateforce_foundation/runtime.py | grep -n "COLUMBUS_Q3021_TELEPORT_REFUSED"
  git show origin/main:src/pirateforce_foundation/runtime.py | grep -n "COLUMBUS_CHOOSE_NPC_WRONG_SCENE"
  git show origin/main:src/pirateforce_foundation/runtime.py | grep -n "columbus_q3021_crossing_row_checkpointed"
  ```
  ข้อ 1-2 ว่าง ⇒ คง `BLOCKED` **ห้ามบูต ไม่เสียเวลาผู้เทสแม้แต่นาทีเดียว** · ข้อ 3 ว่าง ⇒ บูตได้ แต่ครึ่ง `/warp 1` เป็น `NO-RESULT` ตาม (C)

- db: `state\pirateforce.sqlite3` **สำเนาเท่านั้น ห้ามเปิด canonical** → `state\run_gt212_<yyyyMMdd_HHmmss>.sqlite3` ·
  sha256 สำเนาก่อน/หลัง · sha256 canonical ก่อน/หลัง ต้องไม่เปลี่ยน · `PRAGMA integrity_check`=`ok` ทั้งสองครั้ง
- server args: บูตมาตรฐาน `BRIDGE_BOOT_PROCEDURE.md` · `-SecondPasswordMode bypass` · **ไม่มีแฟล็ก scenario ใด ๆ** ·
  บัญชี GM ใน `config/gm_accounts.json` · เก็บคอนโซลรวม stdout+stderr (`2>&1`) -- โทเคนทั้งสองออกทาง **stderr**

- steps:
  1. RECHECK ก่อน · เซิร์ฟเวอร์สดใหม่ · บูตไคลเอนต์ · ล็อกอิน GM ฉาก 1 · ภาพ `S00` (ให้เห็นย่านที่มี NPC หนาแน่น)
  2. 🔴 **ยังห้ามคลิก Columbus ที่ท่าเรือ** (กล่องแดงข้อ 1)
  3. คลิกช่องแชท ยืนยัน focus จริง · `/warp 14` · Enter · รอ ~3 วิ · เดินหนึ่งก้าว · ภาพ `S14-BEFORE`
  4. **คลิกซ้ายหนึ่งครั้ง** บน actor ที่ป้ายเขียน `Columbus` ในฉาก 14 -- **คนละตัวกับที่ท่าเรือ** (ฉาก 14 index 1 = ชื่อ `Columbus` lv110;
     ท่าเรือคือ MOBS 156) · หาไม่เจอให้คลิกทีละตัวแล้วดูคอนโซล พอโทเคน (B) ขึ้นให้หยุด · ภาพ `S14-AFTER` ภายใน ~3 วิ · จด HUD X/Y/Z ก่อน-หลัง
  5. `/warp 1` · เดินหนึ่งก้าว · คลิก Columbus ที่ท่าเรือ → หน้าต่าง QUEST → กด **ตัวเลือกที่ 1** ครั้งเดียว · ภาพ `S17` ทันทีที่ฉากทะเลขึ้น
  6. `/warp 1` กลับบ้าน · เดินหนึ่งก้าว · รอ ~3 วิ · กวาดกล้องด้วย **คลิกขวาลาก** เท่านั้น · ภาพ `S01-RETURN` ที่ย่านเดียวกับ `S00`
  7. NO-CRASH ด้วยคลิกขวาลากหมุนกล้อง (ห้าม `Q`/`E` -- นั่นยิง `TargetPosVital`) · ออกด้วย X
  8. ปิดเซิร์ฟเวอร์ · เก็บ console `.out`/`.err` + capture + sha256 · `integrity_check` · sha canonical ซ้ำ · **teardown เสมอ**
  🔴 ขอบเขต: คลิกเพื่อ **เลือก/คุย** เท่านั้น -- ห้ามตีมอน ห้ามใช้สกิล ทุกฉาก

- pass criteria (สองชั้น 🔴 ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น):
    wire/DB (headless พิสูจน์ได้ ไม่ต้องมีตาคน · grep คอนโซลรวม `2>&1`):
      (ก) คลิกที่ฉาก 14: `COLUMBUS_CHOOSE_NPC_WRONG_SCENE scene=14 effect=columbus_lane_declined` **หนึ่งบรรทัด**
          และ **ไม่มี** `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE`
      (ข) ข้ามจริงจากฉาก 1: มี `CORE_REQUEST_014_COLUMBUS_Q3021_TELEPORT_SCENE17_ONCE`
      (ค) ถ้ามี op1 หลุดออกจากฉากที่ไม่ใช่ 1: `COLUMBUS_Q3021_TELEPORT_REFUSED scene=<n> reason=not_home_scene`
          และ **ไม่มี** `core_request_014_columbus_scene17_teleport_sent` ตามหลัง ·
          **[คำทำนาย ไม่ใช่ผลวัด]** ผู้เทสอาจไม่มีทางยิง op1 จากนอกบ้านด้วยมือได้เลย ⇒ **ไม่เจอบรรทัดนี้ = ไม่ใช่ FAIL** ให้เขียนว่า "ไม่มีโอกาสยิง"
      (ง) `/warp 1` ขาสุดท้าย: มี census ของฉาก 1 ชุดใหม่ (ไม่ใช่ของฉากก่อนหน้า)
      (จ) `integrity_check`=`ok` · sha canonical ไม่เปลี่ยน · ไม่มี traceback
      🔴 ชั้นนี้ **ตอบไม่ได้ว่ามีอะไรอยู่บนจอ**
    client-observable (ต้องมีคนนั่งหน้าจอ · **ชั้นนี้เท่านั้นที่ตัดสินใบ**):
      (ฉ) `S14-AFTER`: คลิกแล้ว **ไม่มี** หน้าต่างบทสนทนา/เควสต์ขึ้น และ **ฉากไม่เปลี่ยน** (HUD ยังเป็นฉาก 14)
      (ช) `S01-RETURN`: Port Royal **มีชาวเมืองให้เห็น** -- ตอบเป็นคำพูดคน: กี่ตัว ชื่อที่อ่านได้ เทียบกับ `S00`
      (ซ) 🔴 **สีป้ายชื่อทุกป้ายในทุกภาพ หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** เขียน `none` ถ้าไม่มี · อ่านสีจาก **ภาพเต็มความละเอียดเท่านั้น**
          · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (`RE-067`) · ต่างจากเซิร์ฟเวอร์จริง → `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      🔴 ชั้นนี้ **ตอบไม่ได้ว่าเฟรมใดออกจากเซิร์ฟเวอร์**

- คำทำนาย (เป็นคำทำนาย ผิด = ผล ไม่ใช่ความล้มเหลว):
  P1 (ฉ) เงียบ + (ช) มีชาวเมือง ⇒ PASS ทั้งใบ
  P2 (ฉ) เงียบ แต่ (ช) ว่าง ⇒ RECHECK ข้อ 3 ว่าง = `NO-RESULT` (D3 ยังไม่ลง) · ข้อ 3 hit = **finding จริงของ census latch** ⇒ เปิดใบ `RE-` ใหม่ **ห้ามถอนเกต**
  P3 คลิกที่ฉาก 14 แล้ว **มีบทสนทนาขึ้น หรือถูกวาป** ⇒ **หยุดทั้งใบทันที รายงานทันที** -- เกต (B) ไม่ทำงาน ผู้เล่นถูกพาออกนอกเกาะได้

- nonclaims:
  1. 🔴 **ไม่อ้างอะไรเลยเกี่ยวกับประชากรของฉาก 17 เอง** -- เป็นเรื่องของ `GT-148` ใบนี้ไม่แตะ
  2. ไม่พิสูจน์ว่าโทเคน (A) ครอบทุกเส้นทางที่ยิง op1 ได้ -- พิสูจน์เฉพาะเส้นทางที่ผู้เทสเดินจริง
  3. ไม่พิสูจน์กลไก `/warp` เอง และไม่แก้ `GT-182`/`GT-192` ไม่ว่าผลจะออกอย่างไร
  4. ไม่พิสูจน์ความหมายของสีป้าย (`RE-067`) · ไม่แตะคอมแบต/ดรอป · ไม่พิสูจน์อะไรที่รอดข้าม relog
  5. **ผลลบมีค่าเท่าผลบวก**: Port Royal ว่าง = หลักฐานเรื่อง latch/checkpoint ไม่ใช่หลักฐานว่าเกตผิด และ **ห้ามใช้เป็นเหตุถอนเกตทั้งสองอัน**

- links: `notes_to_chief/20260902_1347_COO-DECISION-chief-columbus-gate-teleport-on-home-scene-approved-d1-d4-first-d3-is-chief-too.md` ·
  `notes_to_chief/20260902_1332_CHIEF-ASK-COO-columbus-guard-shipped-but-adversary-found-a-live-scene14-hit-and-an-unguarded-teleport.md` ·
  `server#584` (A,B) · `runtime.py` (`_columbus_note_choose_npc_wrong_scene`, `_dispatch_columbus_quest3021`) ·
  `tests/test_columbus_quest_dispatch_wiring.py` · `GT-148` · `GT-192` · `RE-067`
- result: (ผู้เทสกรอก: PASS/FAIL/NO-RESULT · P1/P2/P3 · ภาพ `S00`/`S14-BEFORE`/`S14-AFTER`/`S17`/`S01-RETURN` + sha256 ·
  บรรทัดคอนโซลคัดดิบทุกโทเคนข้างบน · บรรทัดสีป้ายครบทุกภาพ · sha canonical ก่อน/หลัง · `integrity_check` · NO-CRASH/CRASH ·
  timestamp +07:00 · `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: chief (LANE-E) รอบ `kt05o0`/R305 -- chief บริโภคผลเอง**

## GT-214 CHOOSE-NPC-SCENE2-CLICK-ANSWER-AND-HOSTILE-SAFETY-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS-AGAIN (regression ยืนยันซ้ำ R321 2026-09-06 11:52 · ผลแรก PASS... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-215 NEWBORN-CHARACTER-IS-BORN-WITH-VITALS-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS on its own claim + 🔴 finding สำหรับ chief — R307 2026-09-03: เกิดพร้อม 3 vitals ที่ seed ไว้ (level/hp/speed) ไม่ถูกปฏิเสธตอน login · finding: คลาสที่เลือกตอนสร้าง (Sharpshooter) ถูกเซิร์ฟทิ้ง เล่นเป็น Gladiator เสมอ + MP/CP/cash เป็นค่าคงที่ไม่ใช่ค่าตอนเกิด (raw wire มี tag `19 04 00 00 00` แต่ server ไม่ parse) · จาก notes_to_chief/20260903_1901_KA1A-R307-*.md · 🟢 READY -- RECHECK ผ่านทั้งสองข้อ วัดเองโดย chief (เจ้าของใบ) รอบ `uy54tw` (R313) 2026-09-03T03:1x+07:00 บน `origin/main` `425150aa`: ข้อ 1 `new_character_vitals()` = **5 hit** ใน `store.py` บน `origin/main` · ข้อ 2 `tests/test_persistence_vitals_seed_007.py` = **49 passed** · ~~[BLOCKED -- รอ merge ก่อน (PR ของรอบ `7uxscs` / R308 = `server#595` merged 2026-09-02T12:43Z)]~~ · 🔴 ผู้เทสยังต้องรัน RECHECK เองก่อนบูตทุกครั้งตามกติกาของใบ]

> เปิดโดย chief รอบ `7uxscs` (R308) 2026-09-02 +07:00 · chief บริโภคผลเอง
> numbering: รันคำสั่งของตัวนับร่วม (กฎ ② หัวไฟล์นี้) ข้าม `GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` ·
> `archive/*QUEUE*ARCHIVE*.md` -- **คำสั่งคืนค่า `214`** ⇒ ใบนี้คือ `215` · เช็คซ้ำแล้ว `GT-215`/`RE-215`
> = **0 hit** ทั้งสามที่ · บูต/DB/teardown ตาม `BRIDGE_BOOT_PROCEDURE.md` + `ATTENDED_SESSION_RUNBOOK.md`
> (teardown ปฏิเสธ boot stamp เก่ากว่า 420 นาที -- **รัน teardown เสมอ** แม้รอบจบเพราะเจ้าของเลิกเล่นเฉย ๆ)

- objective: ข้ออ้างเดียว -- **ตัวละครที่ถูกสร้างใหม่หลังจาก `migrations/007_character_vitals_seed.sql`
  รันไปแล้ว เกิดมาพร้อมสามคอลัมน์ `level` / `hp_current` / `hp_max` ครบ (ไม่ NULL) และตัวเดียวกันนั้น
  ล็อกอินเข้าฉากได้จริงจนคนเห็นตัวบนจอ** · `007` หว่านเมล็ดให้ **รุ่นเดียว** (แถวที่มีอยู่ ณ วินาทีที่มันรัน)
  ไม่ใช่ทั้งฐานข้อมูล ⇒ ก่อนรอบนี้ ทุกตัวที่เกิดทีหลัง และ **ทุกตัวบนเครื่องติดตั้งใหม่** (ที่ `007` เจอตารางว่าง)
  มีสามคอลัมน์นั้นเป็น NULL ทั้งชุด · **ไม่เคยมีใครนั่งดูตัวละครที่เกิดหลัง 007 ล็อกอินและเรนเดอร์มาก่อนเลย**

- RECHECK: (รันก่อนเชื่อหัวใบเสมอ · ต้องผ่าน **ทั้งสองข้อ** ไม่ผ่าน = ยัง `BLOCKED` ห้ามบูต)
  ```
  (cd pirate-force-server && git fetch origin && git grep -n "new_character_vitals()" origin/main -- src/pirateforce_foundation/store.py)
  (cd pirate-force-server && python3 -m pytest tests/test_persistence_vitals_seed_007.py -q)
  ```
  ข้อ 1 ต้องได้ **>= 1 hit** (0 hit = ยังไม่ merge ⇒ ไม่บูต ไม่เสียเวลาผู้เทสแม้แต่นาทีเดียว) ·
  ข้อ 2 ต้อง **เขียวทั้งชุด** บน clone เดียวกันนั้น · ทดสอบบน branch ก่อน merge ได้ ถ้าเปลี่ยน `origin/main`
  เป็น branch ของรอบ `7uxscs` แล้ว **เขียนในผลว่าใช้ตัวไหนและ commit ไหน**

- db: canonical = `state\pirateforce.sqlite3` ใต้โฟลเดอร์เซิร์ฟเวอร์ (ยืนยันจากรีโป: `BRIDGE_BOOT_PROCEDURE.md:52`
  และ `staged/TEMPLATE_teardown_generic.ps1:818`) -- **สำเนาเท่านั้น ห้ามเปิดไฟล์ canonical** ·
  คัดลอกเป็น `state\run_gt215_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา · จด sha256 ของสำเนาก่อน/หลัง ·
  จด sha256 ของ canonical ก่อน/หลัง และยืนยันว่า **ไม่เปลี่ยน** (เทียบ `CANON_SHA.txt`) ·
  `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง · (รอบคัดลอก DB ⇒ ตำแหน่งตัวละครกลับไป spawn ทุกบูต
  เป็นเรื่องปกติ ไม่ใช่ผลวัด · และ **ตัวละครที่สร้างในใบนี้อยู่แค่ในสำเนา รอบหน้าไม่มีมัน**)

- server args: บูตมาตรฐาน · `-SecondPasswordMode bypass` · 🔴 **ไม่มีแฟล็ก `--*-scenario` ใด ๆ ทั้งสิ้น** ·
  เก็บคอนโซลรวม stdout+stderr (`2>&1`)
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt215_<stamp>.sqlite3
  ```

- steps: (ราว 10 นาทีหน้าจอ · **เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ**)
  1. RECHECK ผ่านก่อน · `LOCK_GAME` · จด boot stamp · sha canonical · คัดลอก DB เป็น run copy
  2. **วัด DB ก่อนบูต** -- ยังไม่เปิดเซิร์ฟเวอร์ รันในโฟลเดอร์ `pirate-force-server` (อ่านอย่างเดียว)
     แล้วคัดผลลัพธ์ทุกบรรทัดลงใบผลเป็นบล็อก `BEFORE`:
     ```
     python -c "import sqlite3,sys;c=sqlite3.connect('file:%s?mode=ro'%sys.argv[1],uri=True);[print(r) for r in c.execute('SELECT id,selector,name,level,hp_current,hp_max,deleted_at FROM characters ORDER BY id')]" "state\run_gt215_<stamp>.sqlite3"
     ```
     🔴 `mode=ro` คือของจริง ห้ามตัดออก · ห้ามชี้ไปที่ canonical · ห้ามรันตอนเซิร์ฟเวอร์ยังเปิดอยู่
  3. บูตเซิร์ฟเวอร์ **ใหม่สด** แล้วค่อยบูตไคลเอนต์ (เคยฆ่าไคลเอนต์ = เซิร์ฟเวอร์ยังถือเซสชันไว้ ตัวถัดไปจะ
     "connecting" ค้างตลอดกาล ⇒ **รีสตาร์ตเซิร์ฟเวอร์ก่อนเสมอ**) · ห้ามเปิดไคลเอนต์ทิ้งโดยไม่มีเซิร์ฟเวอร์
     (ตายเองใน ~3.5 นาที)
  4. ล็อกอินบัญชีจนถึง **หน้าเลือกตัวละคร** · ภาพนิ่ง `S0-BASELINE` เต็มความละเอียด (เห็นรายชื่อทั้งหมด) ·
     จดเวลานาฬิกา (+07:00) และ `t` ของวิดีโอ
  5. กดปุ่ม **สร้างตัวละครใหม่** · เลือกอะไรก็ได้ตามใจ (เพศ/ผม/หน้า) · ภาพนิ่ง `S1` (หน้าจอสร้าง)
  6. คลิกที่ **ช่องกรอกชื่อให้ขึ้น cursor ก่อน** แล้วพิมพ์ชื่อ ASCII เป๊ะ ๆ ว่า
     ```
     GT215BORN01
     ```
     ถ้าไคลเอนต์ปฏิเสธชื่อนี้ (ซ้ำ/ยาวเกิน) ใช้ `GT215BORN02` แล้ว **จดว่าใช้ชื่อไหน** ·
     🔴 **พิมพ์ได้เฉพาะตอนช่องชื่อ focus อยู่เท่านั้น** ออกจากช่องแล้วทุกตัวอักษรกลายเป็นฮอตคีย์ ·
     🔴 ชื่อนี้ **ไม่ใช่** ทริกเกอร์แชท 12 ตัวอักษรของใบอื่น ใบนี้ไม่มีขั้นแชทเลย อย่าพิมพ์อะไรลงแชท
  7. กด **ยืนยัน/สร้าง** หนึ่งครั้ง · จดเวลานาฬิกา · ภาพนิ่ง `S2` = หน้าเลือกตัวละคร **หลัง** สร้างเสร็จ
     (ต้องเห็นชื่อใหม่อยู่ในรายการ)
  8. เลือกตัว `GT215BORN01` แล้ว **เข้าเกม** · รอจนโหลดฉากเสร็จ · ภาพนิ่ง `S3` เต็มความละเอียด
     ให้เห็น **ตัวละครในฉาก + HUD ที่มีเลข level และหลอด HP** · **อ่านเลขที่เห็นบนจอออกมาจดตรง ๆ**
     (level = ? · HP = ?/?) ห้ามเดา ห้ามเติมเลขที่คิดว่าควรเป็น
  9. เดินด้วย `W/A/S/D` สั้น ๆ ~3 วินาที ให้เห็นว่าตัวขยับจริง · ภาพนิ่ง `S4` · (ใบนี้ **ไม่ล็อก facing**
     เดิน/หัน `Q`/`E` ได้ตามสบาย เพราะไม่มีข้ออ้างเรื่อง facing ในใบนี้)
     🔴 **ห้ามตี ห้ามคลิกมอนสเตอร์ ห้ามเข้าใกล้จนโดนตี** -- `NOW.md` ห้ามเปิดใบตีมอนจนกว่า P-1 และ P-2 จะปิด
     เจอมอนให้เดินหนี ถ้าโดนตีจนหลอดลด ให้ **จดเวลาแล้วออกจากเกมทันที** และเขียนไว้ในผล
  10. ตัวเช็ค NO-CRASH: **คลิกขวาค้างลากหมุนกล้อง** เท่านั้น (🔴 ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้ มันยิงไบต์ออกสาย) ·
      ภาพนิ่ง `S5` · ออกจากเกมด้วยปุ่ม X มุมขวาบน
  11. **ปิดเซิร์ฟเวอร์ให้สนิทก่อน** แล้วรันคำสั่งข้อ 2 ซ้ำคำต่อคำ คัดผลลัพธ์เป็นบล็อก `AFTER`
  12. เก็บ console `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `capture_v141\GAME_EVENTS_LIVE.txt`
      + sha256 ทุกไฟล์ · `PRAGMA integrity_check` · เช็ค sha canonical ซ้ำ · **รัน teardown เสมอ** · ห้าม commit เอง

- pass criteria: (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**)
    wire/DB (อ่านจากบล็อก `BEFORE`/`AFTER` + คอนโซล ไม่ต้องมีตาคน):
      (1) `AFTER` มีแถวใหม่ของ `GT215BORN01` **หนึ่งแถว** และสามช่อง `level,hp_current,hp_max`
          **ไม่เป็น `None`/NULL ทั้งสามช่อง** และมีค่า `1, 100, 100`
      (2) 🔴 **ทุกแถวที่มีอยู่แล้วใน `BEFORE` ต้องมีสามช่องนั้นเหมือนเดิมเป๊ะใน `AFTER`** -- คอมมิตนี้เป็น
          INSERT ล้วน ไม่มี UPDATE ⇒ ถ้าค่าของตัวเก่าเปลี่ยนแม้แถวเดียว = **FAIL ทันที** และคือผลที่สำคัญที่สุดของใบ
      (3) `integrity_check` = `ok` · sha256 canonical ตรง `CANON_SHA.txt` ก่อน/หลัง · ไม่มี traceback หลุด
      **ชั้นนี้ตอบไม่ได้เลยว่า:** บนจอเห็นอะไร ตัวละครเข้าฉากได้จริงไหม HUD วาดอะไร
    client-observable (**ต้องมีคนนั่งหน้าจอ · ห้ามอนุมานจากคอนโซล/DB**):
      มนุษย์ **เห็น** ตัวละครที่เพิ่งสร้าง (ก) โผล่ในรายการหน้าเลือกตัวละครใน `S2` และ (ข) **ยืนอยู่ในฉากจริงใน `S3`
      โดยมี HUD ที่อ่านเลข level และหลอด HP ได้** · จดเลขที่อ่านได้ตามที่เห็น ·
      🔴 บันทึก **สีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** สำหรับ `S0`-`S5` ครบทุกใบ
      เขียนคำว่า `none` ออกมาแทนการเว้นว่าง · อ่านสีจาก **ภาพนิ่งเต็มความละเอียดเท่านั้น**
      ห้าม contact sheet / ภาพย่อ / วิดีโอ · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุของสี** (`RE-067` เป็นเจ้าของคำถามนั้น)
      ความต่างจากภาพเซิร์ฟเวอร์จริงลง `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      **ชั้นนี้ตอบไม่ได้เลยว่า:** แถวใน DB มีค่าอะไร หรือมีค่าลงไปหรือไม่
    🔴 ปิดใบด้วย `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` เท่านั้น (G-OBS) ·
    มีหลักฐานครบแต่ยังไม่มีลายเซ็นคน = **`AWAITING-OBSERVER`** ซึ่ง **ไม่ใช่ PASS และไม่ใช่ FAIL**

- prediction (**นี่คือคำทำนาย ไม่ใช่ผลวัด** · ทำนายผิด = finding ไม่ใช่ความล้มเหลว):
    P1 แถวใหม่ได้ `1/100/100` ครบ **และ** เห็นตัวยืนในฉากพร้อม HUD ⇒ ผ่านทั้งสองชั้น
    P2 แถวใหม่ครบ แต่เข้าเกมไม่ได้ / ค้างหน้าโหลด / เข้าไปแล้วไม่มีตัว ⇒ wire/DB ผ่าน · ชั้นจอ FAIL ⇒
       ปัญหาอยู่ที่เส้นทางล็อกอิน **ไม่ใช่ที่ INSERT** ⇒ ห้ามย้อน INSERT ให้เปิดใบใหม่กับเส้นทางล็อกอิน
    P3 แถวใหม่ยังมี `None` อยู่ ⇒ บูตโค้ดเก่า/ยังไม่ merge ⇒ **NO-RESULT ไม่ใช่ FAIL** · รัน RECHECK ใหม่
       แล้วรายงานว่าบูต commit ไหน
    P4 สร้างตัวละครไม่สำเร็จเลย (ปุ่มยืนยันเด้ง / error / เซิร์ฟเวอร์โยน traceback) ⇒ FAIL ของชั้น wire/DB
       และเป็น **ผลที่มีค่าที่สุดของใบนี้** ⇒ คัด traceback ทั้งบล็อกดิบ ๆ ห้ามตีความ
    🔴 **ผลลบมีค่าเท่าผลบวก**: ผลลบทุกแบบข้างบน redirect ไปคนละที่กัน และนั่นคือสิ่งที่ใบนี้ซื้อ

- nonclaims: (อ่านก่อนอ้างผลใบนี้)
  1. 🔴 **`1/100/100` ไม่ใช่ข้ออ้างว่าเกมต้นฉบับให้ตัวละครใหม่เป็นเลขนี้** ·
     `persistence_vitals.NEW_CHARACTER_VITALS_LABEL` เขียนไว้ตรงตัวว่า
     `TRANSCRIBED from player_wire hardcode -- original game default OPEN` ⇒ PASS ของใบนี้แปลว่า
     "เซิร์ฟเวอร์เขียนเลขที่ตัวเองประกาศไว้ลงแถวจริง" **ไม่ใช่** "เลขต้นฉบับได้รับการยืนยันแล้ว"
     คำถามนั้นยังเปิดอยู่และเป็นของ RE ใบอื่น
  2. 🔴 **เลขบนจอไม่ใช่หลักฐานว่าเซิร์ฟเวอร์อ่านแถวใน DB** -- วัดแล้วบนโค้ดวันนี้: `player_wire.py` ฮาร์ดโค้ด
     `PLAYER_LOGIN_LEVEL = 1` และ `legacy.u32tag(0x14, 100)` สองครั้ง ส่วน `runtime.py` **ไม่อ้างถึง
     `persistence_vitals` เลยแม้แต่ที่เดียว** (grep = 0 hit) ⇒ ต่อให้ HUD ขึ้น `1` และ `100/100` พอดี
     ก็ยังพิสูจน์ไม่ได้ว่าเลขนั้นมาจากแถว · ใบนี้ตัดสินแค่ว่า **แถวมีค่า** (ชั้น DB) และ **ตัวเข้าเกมได้** (ชั้นจอ)
  3. **ไม่แตะตัวละครเดิมของใคร** -- คอมมิตนี้เพิ่มสามคอลัมน์ลงใน INSERT ของ `create_character` เท่านั้น
     **ไม่มี UPDATE ที่ไหนเลย** ⇒ HP จริงของตัวเก๋าที่เล่นมานานไม่ถูกรีเซ็ต และ **ไม่มีทางถูกรีเซ็ต**
     ⇒ อย่าเสียเวลาไล่หา regression ที่เกิดขึ้นไม่ได้ · ข้อ (2) ของชั้น wire/DB คือรั้วที่ยืนยันเรื่องนี้ให้เอง
  4. ไม่พิสูจน์อะไรเกี่ยวกับ **HP ลด / ตาย / respawn / การตีและถูกตี** ⇒ 🔴 ใบนี้ห้ามมีขั้นตีมอนโดยเด็ดขาด
     (`NOW.md`: ห้ามเปิดใบตีมอนจนกว่า **P-1** และ **P-2** จะปิด)
  5. ไม่พิสูจน์ว่าค่าอยู่รอดข้าม relog หรืออยู่รอดในฐานข้อมูล canonical -- รอบนี้บูตบน **สำเนา**
     ตัวละครที่เกิดในใบนี้จะไม่มีอยู่ในรอบถัดไป
  6. ไม่ตัดสินสาเหตุของสีป้ายชื่อใด ๆ (`RE-067`) · จดสีอย่างเดียว

- links: `NOW.md` (P-1/P-2 · ที่มาของข้อห้ามตีมอน) ·
  `pirate-force-server/src/pirateforce_foundation/store.py` (`create_character` · INSERT สามคอลัมน์) ·
  `pirate-force-server/src/pirateforce_foundation/persistence_vitals.py`
  (`new_character_vitals()` · `NEW_CHARACTER_VITALS_LABEL`) ·
  `pirate-force-server/migrations/007_character_vitals_seed.sql` (ตัวที่หว่าน "รุ่นเดียว") ·
  `pirate-force-server/tests/test_persistence_vitals_seed_007.py::SeedsACohortNotADatabaseTests` ·
  `GT-203` (ที่มาของสำนวนคำสั่งอ่าน DB แบบ `mode=ro`)

- result: (ผู้เทสกรอกตาม G-OBS: PASS/FAIL/BLOCKED/NO-RESULT · บล็อก `BEFORE` และ `AFTER` ดิบทั้งสองบล็อก ·
  ชื่อตัวละครที่ใช้จริง · เลข level/HP ที่ **อ่านจากจอ** · ภาพ `S0`-`S5` · บรรทัดสีป้ายครบทุกป้ายทุกภาพ ·
  sha256 ทั้งสี่ค่า · branch/commit ที่บูต · timestamp +07:00 ·
  `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: chief รอบ `7uxscs` (R308) -- chief บริโภคผลใบนี้เอง**

## GT-216 MULTI-VITAL-WALKER-MAKES-GROUND-PICKUP-PLAYABLE-001  [✅ **PASS สองชั้น · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-217 ATLANTIS-OCEAN-PANEL-CENSUS-ON-A-GM-SINGLE-USE-ENTRY-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS สองชั้น (ตั๋ว relog 126 ทำงานซ้ำได้) · แต่มีผลข้างเคียง: login เข้า 126 ทำให้ผู้เล่นไร้ faction จนกว่าจะ login ใหม่บนบก (ดู R321 §1) — R321 2026-09-06 §4 (ครั้งแรก PASS ที่ R307 §GT-217 2026-09-03) · RESULT: GT-217 PASS R321 2026-09-06 11:17 · จาก notes_to_chief/20260906_1255_KA1A-R321-*.md · 🟢 READY -- merge ที่รอเกิดขึ้นจริงแล้ว (`pirate-force-server#606` merged 2026-09-02T23:20+07:00) · ผู้เทสรัน RECHECK สามข้อข้างล่างก่อนบูตเสมอ]

ATTENDED: RECHECK สามข้อผ่านก่อนเสมอ (`WORLD_CENSUS_BG3001` + `scene_is_sanctioned_for_a_gm_entry` เจอบน `origin/main` + pytest เขียวทั้งชุด) แล้วค่อยบูต -> ล็อกอิน GM เข้าฉากบ้านถ่าย `S00-HOME` -> คลิกช่องแชทยืนยัน focus จริง พิมพ์ `/warp 126` Enter รอ ~3 วิ -> **ล็อกเอาต์แล้วล็อกอินกลับด้วยตัวละครเดิม** เพื่อลงสเตจที่ spawn `(3050,232,90)` ถ่าย `S126-A/B/C` (หมุนด้วยคลิกขวาลาก) -> เดินหนึ่งก้าว (`W`/`S`) คลิกซ้ายเลือก actor 1-3 ตัว ถ่าย `S126-CLICK1..3` (ห้ามตี ห้ามสกิล มี Jellyfish King)
ATTENDED: คัดคอนโซลรวม `2>&1` หา `WORLD_POP_HANDOFF scene=126` ตามด้วย `WORLD_CENSUS_BG3001 assembled=<N>/38` + actor `<N>` บรรทัด + `BG3001_UNSHIPPED` `38-<N>` บรรทัด · 🔴 `<N>` ไม่ใช่ค่าคงที่ หาเองก่อนบูตตามข้อ 3 (`grep -c NAME_CP874_HEX` บน `origin/main`: `0`=36 · `9`=37) ไม่ตรง = FAIL ชั้น wire + คลิกตอบ `LANE_A_CHOOSE_NPC_SCENE126_ANSWERED`/label `FACE_P<n>` (คลิกแรกก่อนก้าวเดินถูกปฏิเสธ `no_player_position_walk_one_step` = ไม่ใช่ FAIL) · `COLUMBUS_CHOOSE_NPC_WRONG_SCENE` คัดลงเฉย ๆ ไม่ใช่ STOP
ATTENDED: ผลตัดสินอยู่ที่ **client-observable เท่านั้น** (คอนโซลตอบไม่ได้ว่าอะไรถูกวาดบนจอ) -- นับจำนวน actor ที่วาดจริงจาก `S126-A/B/C` เขียนเลขตรง ๆ, บรรยายก้อนเกาะ `MAP_ISLAND_01` สี่ก้อนวาดออกมาเป็นอะไรตามที่เห็นห้ามเดาสาเหตุ, จดว่าเห็นป้ายลอยของมาร์กเกอร์ Tornado กี่ป้ายไหม (ทำนายผิด = finding), และ **สีป้ายชื่อทุกป้ายทุกภาพหนึ่งบรรทัดต่อป้าย** (ไม่มี = `none` · full-res เท่านั้น · จดสีอย่างเดียว)
ATTENDED: บูต = มาตรฐาน ไม่มีแฟล็ก scenario ใด ๆ + `-SecondPasswordMode bypass` + บัญชี GM จาก `config/gm_accounts.json` บนสำเนา DB `state\run_gt217_<stamp>.sqlite3` เท่านั้น (ห้ามเปิด canonical เด็ดขาด จด sha256 ก่อน/หลังทั้งสำเนาและ canonical) -- เซิร์ฟเวอร์บูตใหม่สดก่อนไคลเอนต์เสมอ · 🔴 จอจะเปลี่ยนฉากตอน `/warp 126` หรือไม่ ไม่ใช่ตัวตัดสินใบนี้ จดแล้วเดินต่อ (`decreed_arrival` ของ 126 ขึ้น main แล้ว วาปสดได้ · เรื่องวาปสดเป็นของ `GT-266`) ใบนี้ตัดสินที่สำมะโน 126 เท่านั้น
ATTENDED: STOP ทันทีถ้าเห็นหน้าต่างบทสนทนา/เควสต์ หรือรู้ตัวว่าอยู่คนละฉากหลังคลิก (ปิดไคลเอนต์รายงานทันที ห้าม retry) · NO-CRASH ใช้คลิกขวาลากเท่านั้น ห้าม `Q`/`E` (ยิง `TargetPosVital`) · ปิดใบด้วย `OBSERVER_CONFIRMED: <timestamp>` เท่านั้น ไม่มีลายเซ็น = `AWAITING-OBSERVER`

> 🔴 **แก้ป้ายโดย LANE-A รอบ `gx7xtp` 2026-09-02T23:4x+07:00 · อ่านสองย่อหน้านี้ก่อนนับ actor บนจอ**
> 1. **ตัวบล็อกหมดแล้ว**: PR ของรอบ `l6at2v` merge เข้า `main` แล้ว ⇒ ป้าย `[BLOCKED]` เดิมผิดตั้งแต่เวลานั้น · เกณฑ์ RECHECK สามข้อข้างล่าง **ไม่เปลี่ยน** ยังต้องรันก่อนบูต
> 2. 🔴 **จำนวน actor ของฉากนี้ขยับ 36 → 37** ตาม `COO-DECISION 20260902_2146` ข้อ 1: แถว Mob-Set 56 (placement 37, `MOBS 8180`, ชื่อไทย) เคยถูกตัดทิ้งเพราะคอนโซลของเราพิมพ์ชื่อไทยไม่ได้ COO กลับคำแล้ว ⇒ มันส่งจริง
>    ⇒ ~~สิ่งที่ต้องนับบนจอคือ **37 ตัว จาก 38 placement**~~ 🔴 **ตัวเลขนี้ถูกแทนที่โดยข้อ 4 — วันนี้นับ 36** · ตัวที่จะเพิ่มเมื่อ `#612` merge คือ **สัตว์/วัตถุ lv 60 หนึ่งตัว ที่ป้ายชื่อเป็นภาษาไทย** (อ่านบนจอได้ แต่คอนโซลพิมพ์ไม่ได้)
>    ⇒ บนคอนโซลมันจะออกมาเป็น `placement=37 n_ID=8180 name_cp874_hex=a1c3d0b7a7 lv60 hp43275 @(...)` — **นี่คือสิ่งที่ถูกต้อง ห้ามอ่านว่าผิดปกติ**
> 3. **บอกได้ว่าเครื่องคุณอยู่รุ่นไหน โดยไม่ต้อง grep f-string**:
>    ```
>    (cd pirate-force-server && git show origin/main:src/pirateforce_foundation/world_bg3001_identity.py | findstr /C:"NAME_CP874_HEX")
>    ```
>    เจอ = 37 ตัว (รอบ `gx7xtp` ขึ้นแล้ว) · ว่าง = 36 ตัว (ยังเป็น `main` ของรอบ `l6at2v`) — **ทั้งสองสภาพเทสได้ ไม่ต้องรอ**
> 4. 🔴 **แก้ป้ายโดย LANE-A รอบ `wqg99e` 2026-09-03T01:28+07:00 — ตอนนี้คำตอบของข้อ 3 คือ "ว่าง" ⇒ นับ 36**
>    ~~รอบ `gx7xtp` ขึ้น main แล้ว~~ **ไม่จริง**: `pirate-force-server#609` **ถูก reaper ปิดโดยไม่ merge** เวลา 2026-09-03T01:05+07:00
>    (เหตุ: `main` แดงอยู่ที่ `tests/test_gm_login_scene_override_position_resync.py` ซึ่งไม่ใช่ของรอบนั้น — ดู `NOW.md` P-0)
>    ⇒ `NAME_CP874_HEX` **ยังไม่อยู่บน `main`** — วัดตรงตัวไม่ใช่ผ่านไฟล์อื่น (pf-adversary D8):
>    `git show origin/main:src/pirateforce_foundation/world_bg3001_identity.py | grep -c NAME_CP874_HEX` = **0** · บนแบรนช์ `#612` = **9** · `main` = `30e150a`
>    ⇒ **ผู้เทสที่บูตวันนี้ต้องนับ 36 ตัว จาก 38 placement ไม่ใช่ 37** และ **ไม่มีป้ายชื่อไทย** บนจอ — เห็น 36 = ถูกต้อง ห้ามอ่านว่า FAIL
>    งานถูกกู้ขึ้นแบรนช์ `claude/laughing-archimedes-wqg99e` แล้วในรอบนี้ (`pirate-force-server#612`) · **ข้อ 3 คือผู้ตัดสิน ไม่ใช่เลข PR**
>    🔴 **ก่อนรันคำสั่งข้อ 3 ต้อง `git fetch origin main` ก่อนเสมอ** (pf-adversary D9 · กฎ `NOW.md` "`git fetch` ก่อนอ่านไฟล์เสมอ")
>    เพราะคำสั่งนั้นอ่าน `origin/main` ในเครื่องคุณ ไม่ใช่ของ GitHub ⇒ ไม่ fetch แล้ว `#612` merge ไปแล้ว = คุณจะนับ 36 แต่เห็น 37 แล้วเขียน FAIL ผิด
> 5. 🔴 **แก้ป้ายโดย LANE-A รอบ `nyxlqs` 2026-09-03T03:0x+07:00 — เกณฑ์ของข้อ 4 ไม่เปลี่ยน เปลี่ยนแค่เลข PR ที่ถืองานอยู่**
>    ~~`pirate-force-server#612`~~ **ถูก reaper ปิดโดยไม่ merge** เวลา 02:09+07:00 ด้วยเหตุเดียวกับ `#609` (เกตเช็คเอาต์ *สาขา merge กับ main* และ `main` แดงที่เทสของสายอื่น) · `main` เขียวแล้วตั้งแต่ 01:52 (`notes_to_chief/20260903_0154_CHIEF-TO-ALL-*`)
>    ⇒ สี่คอมมิตงานเดิม (`a6f0ebf 85ab22e 6d3a1ae 888bcd1`) ถูก cherry-pick ขึ้นสาขา `claude/laughing-archimedes-nyxlqs` บน `main` ที่เขียว (`1f8db54`) = **`pirate-force-server#617`**
>    ⇒ **ผู้เทสยังตัดสินด้วยข้อ 3 เท่านั้น ห้ามนับจากเลข PR** — `git fetch origin main` แล้ว `grep -c NAME_CP874_HEX` บน `origin/main`: ได้ `0` = นับ **36** · ได้ `9` = นับ **37**

> 🔴 **แก้ป้ายโดย LANE-A รอบ `l6at2v` 2026-09-02T22:4x+07:00 · ผู้เทสอ่านตรงนี้ก่อน**: PR ของรอบ `4uztfj` (`pirate-force-server#601`) **ถูกปิดโดยไม่ merge** เวลา 14:54Z — `merge-claude-pr.yml` ปิดเองเพราะเกต Windows แดงที่ช่อง `skip_census` ช่องเดียว (UNDECLARED SKIP 6 ตัวใน `tests/test_world_bg3001_identity_rederived.py`) ⇒ **การรอ merge ของ `#601` คือการรอสิ่งที่จะไม่เกิดขึ้นอีกแล้ว**
> งานทั้งก้อนถูกกู้ขึ้นแบรนช์ `claude/laughing-archimedes-l6at2v` ในรอบ `l6at2v` พร้อมแก้ต้นเหตุ (`@BRIDGE_GAMEDATA.skip_unless_present()` + หมุดใน `docs/PYTEST_SKIP_PINS.json`) ⇒ **merge ที่ต้องรอคือ PR ของรอบ `l6at2v`** · เกณฑ์ RECHECK สามข้อข้างล่าง **ไม่เปลี่ยน** ทุกข้อวัดจาก `main` อยู่แล้ว ไม่ได้วัดจากเลข PR

> เปิดโดย LANE-A (WORLD) รอบ `4uztfj` 2026-09-02T20:0x+07:00 · **LANE-A บริโภคผลใบนี้เอง**
> numbering: ตัวนับร่วมกับ `CLIENT_RE_QUEUE.md` · ตอนเปิดวัดได้ `GT` สูงสุด `215` ⇒ เปิดเป็น `216` · 🔴 **ขยับเป็น `217` ตอน rebase ตามกฎ ③ (คนที่ push ทีหลังขยับ)**: chief (LANE-E) push `GT-216 MULTI-VITAL-WALKER-...` ขึ้น main ก่อนในรอบ R309
> 🔴 **ใบนี้ไม่แซงคิวบูตที่ chief ปักไว้ (`FROM_CHIEF_R305`)**: `GT-207` -> `GT-193` -> `GT-205` -> `GT-204` (ท้ายสุด) · ใบนี้ต่อ **หลัง** สี่ใบนั้น
> บูต/DB/teardown ตาม `BRIDGE_BOOT_PROCEDURE.md` + `ATTENDED_SESSION_RUNBOOK.md` · **รัน teardown เสมอ** แม้รอบจบเพราะเลิกเล่นเฉย ๆ (เทมเพลตปฏิเสธ boot stamp เก่ากว่า 420 นาที)

- objective: ข้อพิสูจน์เดียว -- **ฉาก 126 (`Bg3001` "Atlantis" · `n_SCENE_TYPE 8` = OCEAN PANEL) ถูกส่งถึงไคลเอนต์เป็นครั้งแรกของโปรเจกต์ และมีมนุษย์นั่งดูว่าไคลเอนต์วาดอะไรออกมา**
  รอบ `4uztfj` ต่อสายสำมะโนให้ฉากนี้: ขาเข้าเซิร์ฟเวอร์ประกอบ ~~**36 actor**~~ **37 actor จาก 38 placement ดั้งเดิมของฉาก** (ขยับในรอบ `gx7xtp` ดูหัวใบข้อ 2) --
  🔴 **นับเป็นจุดวาง (placement) ไม่ใช่นับชื่อ** — ร่างแรกของบรรทัดนี้เขียนว่า "เรือสิบลำ" ซึ่งบวกได้ 27 ไม่ใช่ 36 (pf-adversary จับ) ⇒ ตัวเลขที่ถูกคือ:
  **20 ลำเรือ** (`SP_*`): "Merchant Ship" x9 · "Pirate Ship" x4 · "Merchant marine Trade Ship" x3 · "Intrepid" · "Santa Maria" · "Skull Phantom" · "Repair ship" อย่างละ 1 ·
  **10 มาร์กเกอร์อากาศ INVISIBLE**: ชื่อ "Tornado" 4 + ไม่มีชื่อ lv 110 อีก 6 ·
  **4 เกาะที่เป็น actor** (`MAP_ISLAND_01`: "Mad Sand Island", "Pirate Lair", "Blood Blade Island", "Lonely Island") ·
  **3 สัตว์/วัตถุ**: "Jellyfish King" (lv 60) · "Sea Monster Fish" · **แถวชื่อไทย lv 60 (`MOBS 8180`, `M081_000_000_N`) ที่รอบ `gx7xtp` เพิ่มเข้ามา** ⇒ ~~รวม 36~~ **รวม 37**
  🔴 **ไม่เคยมีใครเห็นว่าไคลเอนต์วาด `MAP_ISLAND_01` เป็นอะไร หรือวาด actor INVISIBLE ที่มีป้ายชื่ออย่างไร** ⇒ ใบนี้ซื้อ "ตาแรก" ล้วน ๆ

- RECHECK (ตัดสินด้วย **เนื้อโค้ดบน `origin/main`** ห้ามเทียบเลข commit · รันจาก cwd ที่กำหนดในบรรทัดเอง · ผ่านครบสามข้อ = เลื่อนเป็น `READY` ได้เองโดยไม่ต้องรอเจ้าของใบ):
  ```
  (cd pirate-force-server && git fetch origin && git show origin/main:src/pirateforce_foundation/world_population_bg3001.py | findstr /C:"WORLD_CENSUS_BG3001")
  (cd pirate-force-server && git show origin/main:src/pirateforce_foundation/lane_hooks/lane_a_scene_census.py | findstr /C:"scene_is_sanctioned_for_a_gm_entry")
  (cd pirate-force-server && py -3 -m pytest tests/test_world_population_bg3001.py tests/test_world_bg3001_identity.py tests/test_lane_a_scene_census.py -q)
  ```
  ข้อ 1-2 ต้องเจอสตริงจริงทั้งสอง · ข้อ 3 ต้องเขียวทั้งชุด · ว่าง/แดง = ยังไม่ merge ⇒ คง `[BLOCKED]` **ห้ามบูต ไม่เสียเวลาผู้เทสแม้แต่นาทีเดียว**
  🔴 **ห้าม grep สิ่งที่พิมพ์ผ่าน f-string** (`assembled=`, `hp=`) -- ไม่มีอยู่ในไฟล์ (กับดักของรอบ `cu1il6`)
  ทดสอบก่อน merge ได้ ถ้าเปลี่ยน `origin/main` เป็น branch ของรอบ `4uztfj` แล้ว **เขียนในผลว่าใช้ branch/commit ไหน**

- เส้นทางเข้า (วัดรอบนี้ · 🔴 **มีทางเดียวเท่านั้น ห้ามคิดทางใหม่**):
  ประตูล็อกอินปกติของฉาก 126 **ปิดอยู่** (`login_entry_allowed: false`) และ **รอบนี้ไม่ได้แตะมัน** ·
  🔴 **ผู้เทสห้ามพลิกสวิตช์นี้เด็ดขาด** -- `COO-DECISION 20260829_1444` บังคับว่าต้องมีผลใบ attended ใบนี้ก่อนจึงจะพิจารณาพลิกได้ · จุดทั้งหมดของใบคือ "ทางเข้าเดียวคือ grant ของ GM"
  GM เข้าได้ด้วย single-use grant `CORE-REQUEST-GM-038` ที่ลงมาเพื่อ scene id นี้โดยเฉพาะ:
  (1) ล็อกอินด้วยบัญชี GM ที่อยู่ใน `config/gm_accounts.json`
  (2) พิมพ์ `/warp 126` ในแชท · ฉาก 126 **ไม่มี marker ปลายทางในไฟล์ฉาก** (`n_MARKER = 0`) ⇒ `/warp` **ไม่วาปสด** แต่ **สเตจการล็อกอินครั้งถัดไป** · คอนโซลต้องตอบเป็นข้อความ staged-login ไม่ใช่ teleport
  (3) **ล็อกเอาต์แล้วล็อกอินกลับด้วยตัวละครเดิม** ⇒ ลงที่ spawn ที่ registry ปักไว้ `(3050, 232, 90)` = `CONSTDATA_TH__MARKER` แถว 17 (`CHIEF-DECISION 20260829_1603` ข้อ 1)
  วัดรอบนี้: `single_use_stageable_scene_ids()` = `(1,2,3,4,5,6,7,8,9,10,11,14,126,130,278,997)` · `126` **ไม่อยู่** ใน `stageable_scene_ids()` ปกติ · `sanctioned_barred_blocker(126)` = `login_path_bars_it_needs_core_request_gm_038`

- db: canonical = `state\pirateforce.sqlite3` -- 🔴 **สำเนาเท่านั้น ห้ามเปิดไฟล์ canonical** ⇒ คัดลอกเป็น `state\run_gt217_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา
  จด sha256 ของสำเนาก่อน/หลัง · จด sha256 ของ canonical ก่อน/หลัง และยืนยันว่า **ไม่เปลี่ยน** · `PRAGMA integrity_check` = `ok` **ทั้งสองครั้ง** · **รัน teardown เสมอ**
  (รอบคัดลอก DB ⇒ ตำแหน่งตัวละครกลับไป spawn ทุกบูต เป็นเรื่องปกติ ไม่ใช่ผลวัด)

- server args: บูตมาตรฐาน · 🔴 **ไม่มีแฟล็ก scenario ใด ๆ** · `-SecondPasswordMode bypass` · บัญชี GM ใน `config/gm_accounts.json`
  🔴 เก็บคอนโซล **รวม stdout+stderr (`2>&1`)** -- โทเคนของเลนนี้ออกทาง **stderr** ล้วน เก็บแต่ stdout จะไม่เห็นอะไรเลย
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt217_<stamp>.sqlite3 2>&1
  ```

- steps: (เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ · ~15 นาทีบนจอ)
  1. RECHECK ผ่านก่อน · `LOCK_GAME` · จด boot stamp · sha canonical · คัดลอก DB เป็น run copy
  2. บูตเซิร์ฟเวอร์ **ใหม่สด** ก่อน แล้วค่อยบูตไคลเอนต์ (ไคลเอนต์ที่ถูกฆ่า = เซิร์ฟเวอร์ยังถือเซสชัน ตัวถัดไปค้าง "connecting" ⇒ **รีสตาร์ตเซิร์ฟเวอร์ก่อนเสมอ**)
  3. ล็อกอิน GM เข้าฉากบ้านให้เห็นตัวจริงก่อน · ภาพนิ่ง `S00-HOME` เต็มความละเอียด
  4. คลิกช่องแชท **ยืนยันว่า focus จริง** (พิมพ์ตอนไม่ focus = ตัวอักษรกลายเป็นฮอตคีย์) · พิมพ์ `/warp 126` · Enter · รอ ~3 วิ
     (`/warp` เป็นคำสั่ง GM **ไม่ใช่** ตัวยิงแชทที่ต้องยาว **12 ตัวอักษร ASCII พอดี** ของใบอื่น -- **ห้ามเติมตัวอักษรให้ครบ 12**)
  5. คัดบรรทัดคอนโซลดิบที่ตอบกลับ · **คาดว่าเป็นข้อความสเตจล็อกอิน ไม่ใช่การวาป** ⇒ **จอไม่เปลี่ยนฉาก = ผลที่คาดไว้ ไม่ใช่ FAIL**
  6. **ล็อกเอาต์ แล้วล็อกอินกลับด้วยตัวละครเดิม** · รอโหลดจนจบ
  7. ภาพนิ่ง `S126-A` ทันทีที่โหลดเสร็จ **ยังไม่กดอะไรเลย** · จัดมุมมองด้วย **คลิกขวาลาก** เท่านั้น (หมุน **กล้องอย่างเดียว** facing ของตัวละครไม่ขยับ ไม่มีไบต์ออกสาย ปลอดภัยทุกจังหวะ) แล้วเก็บ `S126-B` `S126-C` ให้ครบรอบทิศ
  8. **เดินหนึ่งก้าว** (`W` หรือ `S`) -- จำเป็น เพราะตัวตอบคลิกอ่าน `last_target_pos` ซึ่งยังเป็น `None` ก่อนก้าวแรก
  9. **คลิกซ้ายหนึ่งครั้ง** บน actor ที่มองเห็น โดยมีตัวอื่นในเฟรม · `S126-CLICK1` ภายใน ~3 วิ · ทำซ้ำอีกสองตัวถ้ามี (`S126-CLICK2` `S126-CLICK3`)
     🔴 **คลิกเพื่อเลือกเท่านั้น** ห้ามตี ห้ามใช้สกิล (`NOW.md` ห้ามใบตีมอนจนกว่า P-1/P-2 ปิด) · มี "Jellyfish King" ในฉาก ⇒ **เดินหนีอย่างเดียว**
  10. ตัวเช็ค NO-CRASH: **คลิกขวาลากหมุนกล้อง** เท่านั้น · 🔴 **ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้** (มันหมุน **ตัวละคร** และยิง `TargetPosVital` ออกสาย เช่นเดียวกับ `W/A/S/D`) · ออกด้วยปุ่ม X
  11. ปิดเซิร์ฟเวอร์ · เก็บ `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **รัน teardown เสมอ**
  🔴 **STOP:** มีหน้าต่างบทสนทนา/เควสต์โผล่ หรือรู้ตัวว่าอยู่คนละฉากหลังคลิก ⇒ หยุดทั้งใบทันที ปิดไคลเอนต์ รายงานทันที

- pass criteria (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**):
    wire/DB (headless พิสูจน์ได้ ไม่ต้องมีตาคน · grep จากคอนโซลที่รวม `2>&1`):
      (ก) มี `WORLD_POP_HANDOFF scene=126 ...` แล้วตามด้วยบรรทัดเดียวนี้:
          `WORLD_CENSUS_BG3001 assembled=36/38 shippable=36 wire=36 bodies=ok pc=6377B frame=6390B anchor=(3050.000,232.000,90.000) reapply_ms=3000 source=bg3001_full_roster shortfall=identity_unresolved=2 unresolved=2`
      (ข) ตามด้วยบรรทัด `n_ID=... <name> lv.. hp.. @(x,y,z)` **ครบ 36 บรรทัด** (หนึ่งบรรทัดต่อหนึ่ง actor)
      (ค) มี `BG3001_UNSHIPPED` **สองบรรทัดพอดี**:
          `BG3001_UNSHIPPED placement=28 set=16 cline_row=60415 leader_n_id=0 reason=CLINE_row_carries_leader_0,_no_CONSTDATA_MOBS_row`
          `BG3001_UNSHIPPED placement=37 set=56 cline_row=60455 leader_n_id=8180 reason=MOBS_TIP_name_is_Thai,_not_ASCII;_this_lane_ships_an_ASCII_evidence_layer`
      (ง) คลิกที่ได้คำตอบ: `LANE_A_CHOOSE_NPC_SCENE126_ANSWERED ...` + label `LANE_A_CHOOSE_NPC_SCENE126_FACE_P<n>` · **คลิกแรกก่อนก้าวเดินถูกปฏิเสธโดยตั้งใจ** ด้วย `no_player_position_walk_one_step` (ทรงเดียวกับที่ `GT-214` จดไว้ของฉาก 2) ⇒ **ไม่ใช่ FAIL**
      (จ) `integrity_check` = `ok` ทั้งสองครั้ง · sha canonical ไม่เปลี่ยน · ไม่มี traceback หลุด
      (ฉ) 🔴 **บรรทัดที่จะโผล่และ *ไม่ใช่* เรื่องผิดปกติ ห้ามหยุดใบเพราะมัน** (วัดบนดิสแพตช์จริงรอบ `4uztfj`):
          `COLUMBUS_CHOOSE_NPC_WRONG_SCENE scene=126 effect=columbus_lane_declined`
          เกิดเมื่อคลิก actor ที่ **placement 1** (เรือ "Santa Maria") เพราะ identity ของมันคือ `0x2002` เลขเดียวกับ Columbus ที่พอร์ตรอยัล
          และ guard ของ chief ปฏิเสธให้แล้ว (`conversation_sent` ยังเป็น `False` · ไม่มีหน้าต่างบทสนทนา · ไม่มีการวาป)
          ⇒ **ไม่ใช่เงื่อนไข STOP ของข้อ 11** และ **ไม่ใช่หลักฐานของใบ `GT-213`** (ใบนั้นพูดถึงฉาก 14) · คัดบรรทัดลงรายงานเฉย ๆ
          ถ้าเห็น `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` หรือหน้าต่างบทสนทนาโผล่จริง **นั่นคือ STOP** และรายงานทันที
      🔴 **`pc=` และ `frame=` มาจากบิลด์ของรอบ `4uztfj` ที่ anchor นี้ · anchor ต่างไปแล้วสองเลขนี้เปลี่ยนได้อย่างชอบธรรม ⇒ ผู้เทส "คัดตามที่เห็น" ห้ามใช้สองเลขนี้ตัดสินผ่าน/ตก**
      🔴 **ชั้นนี้ตอบไม่ได้เลยว่ามีอะไรถูกวาดบนจอ**
    client-observable (🔴 **ต้องมีคนนั่งหน้าจอ ห้ามอนุมานจากคอนโซล · ชั้นนี้เท่านั้นที่ตัดสินใบ**):
      (ฉ) หลัง relog: **มี actor ถูกวาดบนจอไหม และกี่ตัว** -- นับจาก `S126-A/B/C` แล้วเขียนเลขที่นับได้ตรง ๆ
      (ช) ก้อนที่ควรเป็น **เกาะ** (`MAP_ISLAND_01` สี่ก้อน) วาดออกมาเป็นอะไร -- บรรยายตามที่เห็น (ก้อนเกาะ / กล่อง / โมเดลผิด / ไม่มีอะไรเลย) **ห้ามเดาสาเหตุ**
      (ซ) **[คำทำนาย ไม่ใช่ผลวัด]** มาร์กเกอร์ "Tornado" สี่ตัว **ไม่ถูกวาดเป็นตัว** เพราะ outfit เป็น INVISIBLE · แต่ **ป้ายชื่อจะขึ้นหรือไม่ ยังไม่มีใครรู้** ⇒ จดว่าเห็นป้ายลอยไหม กี่ป้าย · ทำนายผิด = finding ไม่ใช่ความล้มเหลว
      (ฌ) 🔴 **สีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ ทุกภาพ** · เขียนคำว่า `none` ออกมาแทนการเว้นว่าง · อ่านสีจาก **ภาพนิ่งเต็มความละเอียดเท่านั้น** (ห้าม contact sheet / ภาพย่อ / วิดีโอ) · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุของสี** (`RE-067` เป็นเจ้าของคำถามนั้น) · ความต่างจากภาพเซิร์ฟเวอร์จริงลง `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      🔴 **ชั้นนี้ตอบไม่ได้ว่าเฟรมใดออกจากเซิร์ฟเวอร์**
    🔴 ปิดใบด้วย `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` เท่านั้น (G-OBS) · หลักฐานครบแต่ยังไม่มีลายเซ็นคน = `AWAITING-OBSERVER` ซึ่ง **ไม่ใช่ PASS และไม่ใช่ FAIL**

- ที่รู้อยู่แล้วและ **ไม่ใช่ FAIL**: ฉากนี้ **ไม่มีเฟรม `PLAYER_FACTION`** เพราะ `n_SAVE = 0` · เห็นแล้วอย่าตกใจ อย่าเปิดใบซ้ำ ให้จดไว้เฉย ๆ
- 🔴 **ผลลบมีค่าเท่าผลบวก:** ถ้า **ไม่มีอะไรถูกวาดเลย** ทั้งที่คอนโซลบอก `wire=36` ⇒ คำตอบคือ **finding เรื่องฉากประเภท ocean panel** (ไคลเอนต์กับ `n_SCENE_TYPE 8`) **ไม่ใช่หลักฐานว่าตัวประกอบสำมะโนผิด** และ **ห้ามใช้เป็นเหตุถอน `production_allowed`** ⇒ เปิดใบ `RE-` ใหม่พร้อมภาพและเลข `wire=` ดิบ ๆ · วาดครบแต่ผิดรูป = finding อีกแบบ redirect ไปที่ไฟล์ฉาก ไม่ใช่ที่สำมะโน

- nonclaims:
  1. ไม่พิสูจน์ว่าฉาก 126 ควรเปิดประตูล็อกอินปกติ · ใบนี้ **ไม่พลิก** `login_entry_allowed` และผลของใบนี้ไม่ใช่ใบอนุญาตให้ใครพลิกเอง
  2. ไม่พิสูจน์ว่า 36 ตัวตรงกับต้นฉบับ · ไม่พิสูจน์ระบบ identity ของสอง placement ที่ตกไป (28 และ 37)
  3. ไม่พิสูจน์กลไก `/warp` เอง (`GT-182`/`GT-192`) · ไม่พิสูจน์เส้นทางสเตจล็อกอินของฉากอื่นในลิสต์ single-use
  4. ไม่ตัดสินความหมายของสีป้ายชื่อ (`RE-067`) · ไม่แตะคอมแบต/ดรอป/HP · ไม่พิสูจน์อะไรที่รอดข้าม relog (บูตบนสำเนา)
  5. ไม่แซงลำดับบูตของ `FROM_CHIEF_R305` · ไม่ตัดสินฉาก 2 (`GT-214`) ฉาก 130 / 278 / 997

- links: `world_population_bg3001.py` · `lane_a_scene_census.py` · `gm/login_scene_admission.py` · `CORE-REQUEST-GM-038` ·
  `COO 20260829_1444` · `CHIEF 20260829_1603` · `GT-214` · `RE-067`
- result: (ผู้เทสกรอก: PASS/FAIL/NO-RESULT · branch/commit ที่บูต · ภาพ `S00-HOME`/`S126-A`/`S126-B`/`S126-C`/`S126-CLICK1..3` ·
  บรรทัดคอนโซลดิบทุกโทเคนข้างบน (`WORLD_POP_HANDOFF` · `WORLD_CENSUS_BG3001` · 36 บรรทัด actor · `BG3001_UNSHIPPED` สองบรรทัด · คลิกทุกครั้ง) ·
  จำนวน actor ที่ **นับจากจอ** · บรรทัดสีป้ายครบทุกป้ายทุกภาพ · sha256 ทั้งสี่ค่า · `integrity_check` · NO-CRASH/CRASH · timestamp +07:00 · `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: LANE-A (WORLD) รอบ `4uztfj` 2026-09-02T20:0x+07:00 -- LANE-A บริโภคผลใบนี้เอง**

## GT-218 SPEED-SAFE-VALUE-400-DRY-RUN-CLIENT-SURVIVES-001  [**CLOSED** -- ❌ **FAIL · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-219 GM-IMAGE-CHECKER-MEETS-TWO-REAL-DLLS-001  [✅ PASS ทั้งสองขั้น -- ปิดใบ · ขั้น A `20260904_1508` (ชิ้น (ก) ผ่านครบ · ชิ้น (ข) `A2 NO-RESULT`... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## GT-220 GROUND-DROP-SURVIVES-A-CLICK-ON-A-TOWNSPERSON-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS (R307 2026-09-03 — killed mobs, 2 drops on floor survived NPC clicks,... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-221 LOGIN-SENDS-THE-ROW-NOT-THE-CONSTANT-THREE-SHAPES-001  [🔴 BLOCKED -- **วัดซ้ำ R320 (`88qfv3`) 2026-09-03T14:1x+07:00 บน `origin/main` `39a3a05`: ยัง BLOCKED เหมือนเดิม** — `RECHECK 1` คืนเฉพาะค่าที่อยู่ใน `TemporaryDirectory` ของเทส (`test_login_vitals_seam.py:98` · `test_persistence_login_vitals.py:360`) **ไม่ใช่ fixture สามแถวที่ใบนี้ต้องการ** และคู่ `3/40` กับ `1/7` หาไม่เจอบน main เลย · **รอ fixture สามแถวของใบ `COO-DECISION 20260903_1051` ที่ LANE-DB จะลง `main` (เขียนผ่าน `store.write_typed_attributes` บน run copy)** · ถ้อยคำนี้ COO เคาะเอง (`COO-DECISION 20260903_1247` ข้อ 1: ทาง **(ก) เท่านั้น** · ทาง (ค) migration **ปฏิเสธ**) · chief วัดเองรอบ `xnixm6` (R318) 2026-09-03T12:2x+07:00: **สามแถว `3/40 · 9/250 · 1/7` ยังไม่อยู่บน `main`** — รอบ `l8tn7f` ของ LANE-DB commit แค่ `tests/test_hp_pair_rides_the_proven_bits.py` (`358d4bf4`) ⇒ fixture ที่เขาวัดบน `3e291bf6` เป็นของชั่วคราวในรอบ ไม่ถูก commit · **`RECHECK 1` เป็นตัวปลดป้าย** · 🔴 ห้ามบูตจนกว่าจะปลด — ผู้เทสจะไม่มีอะไรให้ดูต่างจาก `GT-215` เลย]

> เปิดโดย chief รอบ `xnixm6` (R318) ตามใบสั่ง `COO 20260903_1052` · **เจ้าของเนื้อหา/ผู้บริโภคผล = LANE-DB
> · ผู้รัน = Panya** · numbering: คำสั่งตัวนับร่วม (กฎ ②) ได้ `220` ⇒ ใบนี้ `221` · `GT-221`/`RE-221` = 0 hit
> 🔴 **ต่อคิวหลัง `GT-216` ห้ามแย่งลำดับกับ P-1** (`COO 1052` ข้อสุดท้าย)

- objective: ข้ออ้างเดียว -- **เซิร์ฟเวอร์อ่านค่าจากแถวใน DB จริง ไม่ได้ส่งค่าคงตัวที่ฮาร์ดโค้ด**
  พิสูจน์ด้วยเลขสามชุดที่ค่าคงตัว `level 1 · 100/100` **ผลิตไม่ได้เลย**

  | แถวใน DB (`hp_current = 0`) | สิ่งที่ต้องเห็นบนจอหลังล็อกอิน |
  |---|---|
  | `level 3 · hp_max 40` | `level=3` · HP `40/40` |
  | `level 9 · hp_max 250` | `level=9` · HP `250/250` |
  | `level 1 · hp_max 7` | `level=1` · HP `7/7` |

  🔴 **ไม่ซ้ำ `GT-215`**: ใบนั้นวัดตัวเกิดใหม่ ซึ่งค่าเท่ากับค่าคงตัวพอดี (`1 · 100/100`) ⇒ แยก "อ่านแถว"
  ออกจาก "ส่งค่าคงตัว" **ไม่ได้โดยโครงสร้าง** · ที่มาตัวเลข: LANE-DB วัดเอง (ใบ `20260903_0925` ข้อ 3)

- 🔴 ทำไมใบนี้ยัง `BLOCKED` — และ **ประตูเขียนไม่ใช่สิ่งที่ขาด** (อ่านก่อนคิดจะบูต):
  ขาด **ไฟล์เดียว**: fixture สามแถวที่ `COO 20260903_1051` สั่ง LANE-DB ให้ลง `main` เป็นเทสถาวร ·
  chief `git grep` บน `origin/main` แล้ว **ยังไม่มี** · ตัวใกล้ที่สุด `tests/test_login_vitals_seam.py:417`
  `_write_row(...)` ใช้ค่า `7/37/250` บน `TemporaryDirectory` ที่ถูกลบตอนจบ ⇒ ใช้กับใบนี้ไม่ได้
  🔴 **ประตูเขียนมีอยู่แล้วและต่อสายแล้ว — ห้ามเขียนว่า "ไม่มีทางเขียน"**: `store.write_typed_attributes`
  (`store.py:1001`) validate แล้วและรับทั้งสามคอลัมน์ โดย `hp_current = 0` อยู่ในช่วงที่ถูกต้อง
  (`persistence_typed_attrs.py:157`) · migration runner (`store.py:179-229`) ก็เขียนค่าลง `characters` ได้จริง
  (`migrations/007_*.sql:172,174`) **แต่ทางนั้นเขียนลง canonical ตอนบูตจริงครั้งถัดไปด้วย และ checksum
  ledger (`store.py:214-216`) ทำให้ถอดออกไม่ได้** ⇒ 🔴 **ตอบแล้ว: ห้าม** — `COO-DECISION 20260903_1247`
  ข้อ 1 ปฏิเสธทาง migration ทั้งทาง ("ตัวละคร `level 9 / hp_max 250` ติดโลกเธอถาวรโดยไม่มีใบไหนระบุคนถอน")
  และประกาศว่า `COO-DECISION 20260901_1112` ข้อ 2 (migration แตะ canonical ได้) **ไม่ครอบ**
  "migration ที่มีอยู่เพื่อให้เทสผ่าน" ⇒ ห้ามอ้างข้อนั้นกับใบเทสอีก · เหลือทาง (ก) ทางเดียว
  🔴 **ผลลบข้างบนมีขอบเขต**: `git grep` `tests/ src/ tools/` บน `origin/main` หาคู่ตัวเลขสามคู่เท่านั้น
  ที่มาเต็มของทั้งย่อหน้านี้ (รวมที่ chief วัดผิดเองรอบแรก) อยู่ใน `rounds/R318_xnixm6_*.md`

- RECHECK: (รันก่อนเชื่อหัวใบเสมอ · **ข้อ 1 ไม่ผ่าน = ยัง BLOCKED ห้ามบูต**)
  ```
  (cd pirate-force-server && git fetch origin && git grep -n "250" origin/main -- tests/ | grep -i "hp_max")
  (cd pirate-force-server && git grep -n "row_hp_not_positive_revived_on_login" origin/main -- src/pirateforce_foundation/persistence_login_vitals.py)
  ```
  ข้อ 1: มองหา fixture ที่ถือคู่ `level 9 / hp_max 250` (และอีกสองคู่) **ที่รับ path DB จากภายนอกได้**
  ⇒ เจอ = ปลดเป็น `READY` แล้วเขียน **ชื่อไฟล์กับวิธีเรียก** ลงหัวข้อ `db:` ของใบนี้ก่อนบูต ·
  ไม่เจอ หรือเจอแต่ผูกกับ `TemporaryDirectory` = **ยัง BLOCKED** ·
  ข้อ 2 ต้อง **>= 1 hit** (โทเคนที่ขั้น 5 รอดู ยังอยู่บน `main`)

- db: **สำเนาเท่านั้น ห้ามเปิด canonical** · `state\run_gt221_<stamp>.sqlite3` · วินัย sha canonical /
  `integrity_check` **ตามช่อง `db:` ของ `GT-215` ทุกบรรทัด**
  🔴 **ช่องที่ยังว่าง = ตัวบล็อกของใบนี้:** วิธีทำให้สำเนามีสามแถวนั้น · **ห้ามแก้ DB ด้วยมือทุกกรณี**
  (`COO 20260903_1052` + `AGENTS.md` §7)
  ⇒ 🔴 **COO เคาะแล้ว (`20260903_1247` ข้อ 1): ทาง (ก) เท่านั้น** — fixture/สคริปต์ที่รับ path DB
  เป็นอาร์กิวเมนต์แล้วเขียนสามแถวนั้นผ่าน `store.write_typed_attributes` (ประตูที่ validate แล้ว)
  **บน run copy เท่านั้น** เหมือน `GT-215` · **(ค) ไฟล์ migration = ปฏิเสธ ห้ามเสนออีก**
  (มันเขียนลง canonical ตอนบูตจริงครั้งถัดไป และ checksum ledger ทำให้ถอดไม่ได้ = "ย้อนไม่ได้และไม่มี backup")
  · **(ข)** ไฟล์ `.sqlite3` ที่ seed แล้วสามใบพร้อม sha256 ยังรับได้ถ้า LANE-DB เลือกส่งแบบนั้น
  🔴 **ห้ามใช้ `tests/pf_birth_state.py:253` `_clear_columns`** — รับ `db_path` อะไรก็ได้โดยไม่มีการ์ดว่าเป็น
  temp จริง (มีแต่คำสัญญาใน docstring) และเขียน `NULL` ไม่ใช่ค่าที่ใบนี้ต้องการ

- server args: บูตมาตรฐาน · `-SecondPasswordMode bypass` · 🔴 **ไม่มีแฟล็ก `--*-scenario` ใด ๆ** ·
  เก็บคอนโซลรวม stdout+stderr: `py -3 -u -m pirateforce_foundation.app --db state\run_gt221_<stamp>.sqlite3`

- steps: (ราว 10 นาทีหน้าจอ · **เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ** · ทำซ้ำสามรอบ แถวละรอบ)
  1. RECHECK ผ่าน · `LOCK_GAME` · boot stamp · sha canonical · คัดลอก DB + seed ตามช่อง `db:`
  2. **วัด DB ก่อนบูต** (ยังไม่เปิดเซิร์ฟเวอร์) ด้วยคำสั่ง `mode=ro` **ตาม `GT-215` ข้อ 2 คำต่อคำ**
     เปลี่ยนแค่คอลัมน์เป็น `id,name,level,hp_current,hp_max` และชี้ไป run copy ของใบนี้ ⇒ บล็อก `BEFORE`
     🔴 `mode=ro` ห้ามตัดออก · ห้ามชี้ canonical · ห้ามรันตอนเซิร์ฟเวอร์เปิดอยู่
  3. บูตเซิร์ฟเวอร์ใหม่สด แล้วค่อยบูตไคลเอนต์
  4. ล็อกอิน เลือกตัวละครของแถวที่วัด **เข้าเกม** · ภาพนิ่ง `S<n>` เต็มความละเอียด ให้เห็น **HUD ที่อ่าน
     level และหลอด HP ได้** · 🔴 **อ่านเลขบนจอจดตรง ๆ ห้ามเดา ห้ามเติมเลขที่คิดว่าควรเป็น**
  5. คัดบรรทัดคอนโซล `LOGIN_VITALS` ของล็อกอินนั้นมาทั้งบรรทัด
     🔴 **บรรทัดที่คาดคือ `row_hp_not_positive_revived_on_login` ไม่ใช่ `from_row`** เพราะสามแถวนี้
     `hp_current = 0` ⇒ ล็อกอิน**ฟื้นแถวก่อนแล้วส่งสิ่งที่เขียนลงไป** (`persistence_login_vitals.py:183`)
     · `from_row` = แถวไม่ได้ตายจริง ⇒ seed ไม่ตรงใบ **จดแล้วรายงาน อย่ากลบ**
     · ขึ้นต้น `!! LOGIN_VITALS` (`REVIVE_WRITE_FAILED`/`REVIVE_NOT_CONFIRMED`) = **FAIL**
     · คัดโทเคน `apply=` ท้ายบรรทัดเสมอ (`apply=carried` = ตัวละครถือเลขนั้นจริง)
  6. ออกจากเกม · **ปิดเซิร์ฟเวอร์ให้สนิทก่อน** แล้วรันคำสั่งข้อ 2 ซ้ำคำต่อคำ เป็นบล็อก `AFTER`
  7. ทำข้อ 3-6 ซ้ำให้ครบทั้งสามแถว · เก็บหลักฐาน/teardown ตาม `GT-215` ข้อ 12 · ห้าม commit เอง

- pass criteria: (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**)
    wire/DB (อ่านจาก `BEFORE`/`AFTER` + คอนโซล ไม่ต้องมีตาคน):
      (1) `BEFORE` มีสามแถวตามตาราง `hp_current = 0` ทั้งสามแถว
      (2) แต่ละล็อกอินมี `LOGIN_VITALS row_hp_not_positive_revived_on_login` ที่ `level=`/`hp=`
          **ตรงกับแถวของมันเอง** และมี `apply=carried`
      (3) `AFTER` แต่ละแถว `hp_current` = `hp_max` ของแถวนั้น · `level`/`hp_max` **ไม่เปลี่ยน**
      (4) `integrity_check` = `ok` · sha canonical ตรง · ไม่มี traceback หลุด
      **ชั้นนี้ตอบไม่ได้ว่า:** ผู้เล่นเห็นเลขอะไรบน HUD
    client-observable (**ต้องมีคนนั่งหน้าจอ · ห้ามอนุมานจากคอนโซล/DB**):
      มนุษย์ **อ่านจาก HUD** ได้ `3 · 40/40` · `9 · 250/250` · `1 · 7/7` ตรงตามแถวของมัน ครบทั้งสาม
      🔴 **เกณฑ์ตก: แถวไหนออกมาเป็น `level 1` HP `100/100`** = เซิร์ฟเวอร์ส่งค่าคงตัว ไม่ได้อ่านแถว
      🔴 บันทึกสีป้ายชื่อทุกป้าย **ตามกติกาเดียวกับ `GT-215`**
      **ชั้นนี้ตอบไม่ได้ว่า:** แถวใน DB ถืออะไร หรือมีการเขียนกลับหรือไม่

- 🔴 ข้อจำกัดที่ใบนี้พิสูจน์ไม่ได้ (อ่านก่อนรายงานผล):
  1. **ห้ามเขียนว่าใบนี้ปิด `M4`** (`COO 20260903_1052`) — พิสูจน์ครึ่ง **อ่าน** เท่านั้น · ครึ่ง **เขียน**
     ยังไม่มีตัวผลัก: `store.apply_hp_damage` (`store.py:1345`) **ผู้เรียกศูนย์** ใน `src/` และ `tools/`
     (chief วัดเองรอบนี้) ⇒ **ไม่มีอะไรในรีโปลด `hp_current` ได้** ตัวเขียน HP ตอนรันมีตัวเดียวคือ
     `restore_hp_to_full` ซึ่ง**ขึ้นอย่างเดียว**
  2. เลขที่เห็นเป็น `hp_max` ของแถว **เพราะการฟื้นเขียนลงไปแล้วอ่านกลับ** ไม่ใช่เพราะอ่านเฉย ๆ ⇒ พิสูจน์ได้แค่
     "ค่าที่ออกไปผูกกับแถวของตัวเอง" (พอจะหักล้างค่าคงตัว) **ห้ามเขียนว่าล็อกอินอ่านแถวโดยไม่เขียน** — มันเขียน
  3. ไม่พิสูจน์เรื่อง `/speed` · ไม่แตะ `GT-218` · ไม่มีขั้นแชท ไม่มีขั้นตีมอน
  4. `updated_at` ถูกเขียนตอนฟื้นด้วย — คำถามของ COO ในใบ `1051` ไม่ใช่ผลของใบนี้
  5. 🔴 **ห้ามอ้าง `GT-193` ว่าเป็นหลักฐานว่า `hp_current = 0` เคยเกิดจริงใน DB** — ใบนั้นบันทึกเองที่
     `GAME_TEST_QUEUE.md:9976` ว่า **DB ฝั่งเราสะอาด `hp 100/100`** ⇒ HP 0 ที่เห็นเป็นชั้นไคลเอนต์ล้วน

- links: `COO 20260903_1052` · `LANE-DB 20260903_0925` ข้อ 3 · `COO 20260903_1051` · `GT-215` · `GT-216`
  (ต้องมาก่อน) · `persistence_login_vitals.py:183,724` · `store.py:1001,1345,1665`

**ผู้เปิดใบ: chief (LANE-E) รอบ `xnixm6` ตาม `COO 20260903_1052` -- ผู้บริโภคผล: LANE-DB (PERSISTENCE)**

---

> 🔴 **รับโอนจาก `GT-146` (chief รอบ `m8wtlr`/R356 · `COO-DECISION 20260905_0249` ข้อ 1 ประโยคท้าย: "ห้ามหายไปกับใบ"):** `mob_drop_presence.REEMISSION_REDRAWS_THE_LABEL = None` — **ยังไม่มีใครวัดว่าป้ายชื่อของบนพื้นถูกวาดใหม่บนจอเมื่อ generation ถูกส่งซ้ำหรือไม่** · แถวฝั่งเซิร์ฟเวอร์รอด 120 วิ แน่แล้ว (`sustain_a_kill` whole-live-ledger บน main) แต่ภาพบนจอ เป็นคำถามฝั่งไคลเอนต์ที่วัดจากซอร์สไม่ได้ · เป็นครึ่งเดียวกับ `RE-208` ที่ `COO 20260903_1942` ข้อ 4 สั่งให้เป็นขั้นในใบนี้ · **เจ้าของ = LANE-B** · ใบต้นทาง `GT-146` ปิดเป็น CANCELLED-covered รอบเดียวกัน แต่คำถามนี้ไม่ได้ถูกตอบโดย R303 (R303 ตอบ opcode ขาเข้า ไม่ได้ตอบว่าป้ายถูกวาดใหม่)

## GT-223 GROUND-LEDGER-SURVIVES-A-RECONNECT-001  [🔴 LANE-K แก้ผล รอบ `slug54r2` 2026-09-06T13:40+07:00 — **แก้ประโยคผิดจากรอบ `slug54`ที่บอกว่า "ยังไม่มีผลบูตจริง" ทั้งที่มีผลจริงอยู่แล้ว (pf-adversary จับได้)**: **FAIL สองชั้น** (`OBSERVER_CONFIRMED: 2026-09-04T14:19+07:00`) — R309 §GT-223: killed `Fighting Fish soldier`, drop `Energy Cubic Crystal` on floor (ภาพ `140947.png`) → close+relaunch (ล็อกอินสะอาดฉากเดิม) → ภาพ `141440.png` พื้นว่าง คริสตัลหายไป **และมอนที่ฆ่าไปแล้วกลับมามีชีวิตยืนที่เดิม HP 3138/3138** → เก็บของชิ้นเดิมไม่ได้เพราะไม่มีบนจอ = FAIL ตามนิยามของใบเอง (wire: ledger ต่อ session ไม่ข้าม reconnect · client: พื้นว่าง มอนคืนชีพ) · จาก notes_to_chief/20260904_1430_KA1A-R309-RESULTS-*.md §GT-223 · 🔴 หมายเหตุ: จดหมายฉบับนี้มี `.CONSUMED.txt` อยู่แล้วตั้งแต่ 2026-09-04 (LANE-B บริโภคเพื่อสร้างตัวแก้ ไม่ใช่การพับหัวใบ) — เครื่องหมาย consumed เดียวกันใช้สองความหมายจึงบังผลนี้ไว้จนกว่า LANE-K จะเจอ ดู `notes_to_chief/20260906_1350_LANE-K-ASK-COO-*.md` · ต่อมา R321 §8 (2026-09-06) ทดลองฆ่ามอนซ้ำในบูตอื่นแต่ถูก BLOCKED ก่อนวัดอะไรได้ (มอนเขียวตีไม่ได้จากบั๊ก §1 login-126-no-faction) — ไม่ใช่การพลิกผล FAIL เดิม เป็นความพยายามคนละครั้ง · RESULT: GT-223 FAIL R309 2026-09-04T14:19+07:00 (ยืนคำตัดสินเดิม) · 🟢 **READY เมื่อ RECHECK ข้อ 1 ผ่าน** — ปลดบล็อกโดย chief รอบ `dwvbpm` (R330) ตาม `COO-DECISION 20260904_0145` ข้อ 1 · **ตัวบล็อกหมดอายุทั้งสองตัว**: (ก) `GT-216` **PASS** บนจอ R306 ⇒ เงื่อนไข "คิวหลัง `GT-216`" ของ `COO 20260903_1048` ครบแล้ว · (ข) ประตู persistence ของของบนพื้นอยู่บน `main` แล้วทาง **`#680`** — ~~`pirate-force-server#672`~~ เป็นการวัดผิดของหัวใบเดิม ถอนแล้ว (chief วัดเอง 2026-09-04T01:5x+07:00 บน `origin/main`: `src/pirateforce_foundation/store.py:2261` `def commit_ground_drop` · `store.py:2392` `def list_ground_drops_for_scene`) · เปิดโดย chief รอบ `kjtpza` (R319) 2026-09-03T13:0x+07:00 · **เจ้าของใบ/ผู้แก้ = LANE-B** (เจ้าของทางเก็บของ) · **ผู้รัน = Panya** · `RECHECK 1` ยังเป็นตัวปลดป้าย รันก่อนบูตเสมอ]

> 🔴 **ใบนี้เป็นใบข้อบกพร่อง ไม่ใช่ใบสำรวจ** — คำตัดสินมีอยู่แล้ว: *ของที่ดรอปแล้วยังไม่มีใครเก็บ
> = ของ **"โลก"** ผูกกับ **"ฉาก"** ไม่ผูกกับคอนเนกชัน* (`COO 20260903_1048`) ⇒ พฤติกรรมวันนี้
> (รีล็อกอินหนึ่งครั้ง = ledger ใหม่ว่างเปล่า) **เป็นข้อบกพร่องจริง** ห้ามรอบไหนอ่านว่าเป็นดีไซน์ที่ถูก
> · ไคลเอนต์ **ไม่ต้อง** เลิกวาดของบนพื้นหลังรีคอนเนกต์ — เซิร์ฟเวอร์ต่างหากที่ต้องยังจำมันได้
> · 🔴 **ห้ามใครย้าย ledger ขึ้นเหนือ connection ก่อน `GT-216` ให้ผลบนจอ** (COO สั่งลำดับ ไม่ได้สั่งให้ลงมือวันนี้)
> · 🔴 **ห้าม "ซ่อม" ด้วยการกวาดแถว ledger ทิ้ง** (ยืนตาม `COO 20260903_0253`)

ATTENDED: (สรุป ≤5 บรรทัด ของ steps/pass criteria เต็มด้านล่าง — เติมโดย LANE-B รอบ `oabhhe` ตาม R364 ข้อ 2)
  1. กด: ฉาก 2 ฆ่ามอน ≥1 ตัวให้ของตก (ยังไม่เก็บ) ถ่าย S1 → ล็อกเอาต์/ปิดไคลเอนต์ (ห้ามปิดเซิร์ฟเวอร์) →
     ล็อกอินตัวละครเดิมกลับฉากเดิม ถ่าย S2 → ฆ่ามอนอีกตัวในเซสชันใหม่ก่อน (ขั้น 4b) → คลิกของชิ้นเดิมจากขั้น 2 ถ่าย S3
  2. ดู: บรรทัดคอนโซล "ของตก" ขั้น 2 และ 4b (ฉาก/ตำแหน่ง) + บรรทัดเก็บของสำเร็จขั้น 5 + ป้ายชื่อของ
     (ไม่กะพริบ/หาย-แล้ว-กลับมา) ระหว่างขั้น 4b-5 (วิดีโอสั้น) + `AFTER` ของ run copy มีของในกระเป๋า
  3. ผ่าน/ไม่ผ่าน: ครบ 8 ข้อ pass criteria สองชั้น (wire/DB 1-5 + client-observable 6-8) ด้านล่าง — ครบชั้นเดียว
     = 🟡 ไม่ใช่ PASS · S2 พื้นว่างหรือขั้น 5 ถูกปฏิเสธทั้งที่ 4b ผ่านแล้ว = FAIL ที่มีค่า ต้องส่ง ไม่ใช่รอบเสียเปล่า
  4. บูต: มาตรฐาน + `-SecondPasswordMode bypass` · ห้ามแฟล็ก `--*-scenario` ใด ๆ · สำเนา DB เท่านั้น · เก็บคอนโซล stdout+stderr เต็ม

- objective: ข้ออ้างเดียว -- **ของที่ตกบนพื้นและยังไม่มีใครเก็บ ยังอยู่ที่เดิมหลังผู้เล่นคนนั้น
  ล็อกเอาต์แล้วล็อกอินกลับเข้าฉากเดิม** และเก็บได้จริงหลังกลับมา
- ที่มาของเกณฑ์: เจ้าของเขียน P-1 ด้วยคำของเธอเองว่า **"ของดรอปต้องค้างบนพื้นและเก็บได้"** —
  คำว่า *ค้าง* แปลว่าอยู่ต่อโดยไม่ขึ้นกับว่าใครยังต่ออยู่ (COO อ่านกติกาที่เธอเคาะไว้ ไม่ได้ตั้งใหม่)

- RECHECK: (รันก่อนเชื่อหัวใบเสมอ · **ข้อ 1 ไม่ผ่าน = ยัง BLOCKED ห้ามบูต** · รันจากรากรีโป `pf_bridge`)
  ```
  grep -n "^## GT-216 " GAME_TEST_QUEUE.md
  git -C ../pirate-force-server fetch origin && git -C ../pirate-force-server grep -c "cell_has_no_scene" origin/main -- src/
  ```
  🔴 **ข้อ 1 ต้องอ่านหัวใบ `GT-216` แล้วเห็นว่ามัน `PASS` (P-1 ปิดจริง)** ⇒ ปลดใบนี้เป็น `READY`
  · `FAIL` = **ยัง BLOCKED** (P-1 ยังไม่ปิด และ `COO 20260903_1048` สั่งให้ใบนี้เข้าคิว *หลัง P-1 ปิด*
  ไม่ใช่หลัง "มีผลอะไรก็ได้") · `AWAITING-OBSERVER` = **ยัง BLOCKED** เช่นกัน (หัวคิวเขียนเองว่า
  ห้ามยกผลของสถานะนั้นไปเป็นฐานของใบอื่น) · ยังไม่ถูกรันเลย = **ยัง BLOCKED**
  🔴 คำสั่งข้อ 1 จงใจปักที่ `^## GT-216 ` (หัวใบ) ไม่ใช่ `grep | head` — บรรทัดสารบัญของใบอื่นที่เอ่ยถึง
  `GT-216` มีหลายบรรทัดและเพิ่มขึ้นทุกรอบ `head` จะคืนสารบัญแล้วไม่คืนหัวใบ
  · ข้อ 2 เป็นบริบทให้ผู้แก้ ไม่ใช่เกตของผู้รัน

- db: **สำเนาเท่านั้น ห้ามเปิด canonical** · `state\run_gt223_<stamp>.sqlite3` · วินัย sha canonical /
  `integrity_check` **ตามช่อง `db:` ของ `GT-215` ทุกบรรทัด**
- server args: บูตมาตรฐาน · `-SecondPasswordMode bypass` · 🔴 **ไม่มีแฟล็ก `--*-scenario` ใด ๆ** ·
  เก็บคอนโซลรวม stdout+stderr

- steps: (ราว 10 นาทีหน้าจอ · **เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ** · เซิร์ฟเวอร์ **ห้ามรีสตาร์ท**
  ระหว่างขั้น 2-5 มิฉะนั้นวัดคนละเรื่อง)
  1. RECHECK ผ่าน · `LOCK_GAME` · boot stamp · sha canonical · คัดลอก DB
  2. เข้าเกม ฉาก 2 · ฆ่ามอน **อย่างน้อยหนึ่งตัว** จนมีของตกบนพื้น · **อย่าเพิ่งเก็บ**
     ภาพนิ่ง `S1` ให้เห็นของบนพื้น · คัดบรรทัดคอนโซลของการตกทั้งบรรทัด
  3. **ล็อกเอาต์กลับหน้าเลือกตัวละคร** (หรือปิดไคลเอนต์แล้วเปิดใหม่ — จดว่าเลือกทางไหน)
     🔴 **ห้ามปิดเซิร์ฟเวอร์**
  4. ล็อกอินตัวละครเดิม กลับเข้าฉากเดิม · ภาพนิ่ง `S2` มุมเดียวกับ `S1` **ก่อนทำอะไรทั้งสิ้น**
  4b. 🔴 **ฆ่ามอนหนึ่งตัวในเซสชันใหม่นี้ก่อน แล้วค่อยไปคลิกของเก่า** — ไม่ใช่ขั้นตอนตกแต่ง:
     เซสชันใหม่ถือ ground cell ใหม่ที่ยังไม่รู้ว่าตัวเองอยู่ฉากไหน ⇒ ถ้าคลิกของเก่าเลย คำปฏิเสธที่ได้
     จะเป็นคำปฏิเสธของ **cell ใหม่** ไม่ใช่คำตอบว่าของหายจากพื้นหรือไม่ (ดูบล็อกโทเคนข้างล่าง)
  5. เดินไปคลิก **ของชิ้นเดิมจากขั้น 2** · ภาพนิ่ง `S3` ให้เห็นกระเป๋า · คัดบรรทัดคอนโซลของการเก็บทั้งบรรทัด
  6. teardown ตาม `GT-215` ข้อ 12 · ห้าม commit เอง

### 🔴 โทเคนที่ห้ามอ่านว่าเสีย (`COO-DECISION 20260903_0953` ข้อ 2 -- เขียนลงทุกใบที่มีคลิกเก็บของ)
  **`cell_has_no_scene` ก่อนการฆ่ามอนตัวแรก *ของเซสชันล็อกอินนั้น* = พฤติกรรมที่ถูก ไม่ใช่ความเสีย ห้ามรายงาน FAIL**
  🔴 **หน่วยคือ "เซสชัน" ไม่ใช่ "บูตของเซิร์ฟเวอร์"** — `DropLedgerCell()` ถูกสร้างใหม่ต่อหนึ่งเซสชัน (`runtime.py:1328`)
  ⇒ **รีล็อกอินระหว่างบูตเดียวกัน = cell ใหม่ = ตัวนับเริ่มใหม่** เห็นโทเคนนี้อีกครั้งหลังรีล็อกอินก่อนฆ่าอะไร **ยังเป็นปกติ**
  🔴 **ใบนี้มีรีล็อกอินอยู่กลางใบโดยเจตนา ⇒ ตัวนับรีเซ็ตแน่นอน** จึงมีขั้น 4b: ฆ่ามอนหนึ่งตัวก่อน
  แล้วค่อยตัดสินโทเคนนี้ **อย่าตัดสินจากการฆ่าในขั้น 2 ซึ่งอยู่คนละเซสชัน**
  🔴 **คัด *ข้อความ* ไม่ใช่แค่โทเคน** — ข้อความ `does not know which scene it is in` = **กรณีปกติข้างบน** ·
  ข้อความ `could not answer which scene it is in (<เหตุผลข้างใน>)` = **finding เสมอ** ไม่ว่าจะฆ่าอะไรมาแล้วหรือยัง

- pass criteria: (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด** · `COO 20260903_1249` ข้อ 2:
  **ห้ามปั๊ม `✅ PASS` เดี่ยวจากชั้นเดียว**)
    wire/DB (อ่านจากคอนโซล + run copy ไม่ต้องมีตาคน · 🔴 **ไม่มีบรรทัดคอนโซลไหนรายงานเนื้อใน ledger
    ตอนล็อกอิน และ ledger อยู่ในหน่วยความจำต่อเซสชัน ไม่ได้อยู่ในไฟล์ DB** ⇒ เกณฑ์ชั้นนี้จึงวัดที่
    **ผลของการคลิก** ไม่ใช่ที่ "ledger ว่างหรือไม่" ซึ่งวัดไม่ได้จากที่นั่ง):
      (1) ขั้น 2 มีบรรทัดของตกที่ระบุฉากและตำแหน่ง (คัดทั้งบรรทัด)
      (2) ขั้น 4b มีบรรทัดของตกของการฆ่าครั้งใหม่ = cell ของเซสชันใหม่รู้ฉากของตัวเองแล้ว
          (ข้อนี้คือสิ่งที่ทำให้ข้อ 3 และข้อ 4 อ่านได้ ถ้าข้อนี้ไม่มี **หยุด** ผลทั้งใบอ่านไม่ได้)
      (3) ขั้น 5 คลิกของ **ชิ้นเดิมจากขั้น 2** แล้วได้บรรทัดเก็บของสำเร็จ (แถวเข้ากระเป๋า)
      (4) `AFTER` ของ run copy มีของชิ้นนั้นอยู่ในกระเป๋าของตัวละคร (`integrity_check` = `ok` ·
          sha canonical ตรง · ไม่มี traceback หลุด)
      🔴 (5) **`cell_has_no_scene` ที่เห็นหลังขั้น 4b แล้ว = finding เสมอ** จดและรายงาน ห้ามอ่านว่าปกติ ·
          **ก่อนขั้น 4b = ปกติ ห้ามรายงาน FAIL** (กฎบ้าน `COO 20260903_1048` + บล็อกโทเคนข้างบน)
    client-observable (ตาคนเท่านั้น):
      (6) `S2` เห็นของชิ้นเดิม **อยู่ที่เดิม** บนพื้น (ถ่ายก่อนทำอะไรในเซสชันใหม่)
      (7) `S3` เห็นของชิ้นนั้นเข้ากระเป๋า
      (8) 🆕 **ป้ายชื่อของ (item label) ไม่กะพริบ/หาย-แล้ว-กลับมาระหว่างขั้น 4b-5** ก่อนเก็บ
          🔴 **ขั้นนี้พิสูจน์ `#689` (`mob_pickup_request.EXPIRY_PUBLICATION_CALL_SITE_STATUS = "sent"` —
          คลิกที่ถูกปฏิเสธส่ง `ground_after` แทนที่จะทิ้งเฟรมที่ประกอบเสร็จ) ไม่ใช่สังเกตการณ์**
          (`COO-DECISION 20260904_0145` ข้อ 1 · คำสั่ง `PANYA-DECISION 20260904_0125` ข้อ 2: อาการ
          "ของหายชั่วคราวแล้วโผล่กลับ" ต้องแก้ให้เป็นปกติ ไม่ใช่บันทึกไว้เฉย ๆ) ⇒ ข้อนี้ FAIL = โค้ดบน main
          ยังไม่พอ ไม่ใช่ "จดไว้เป็นข้อสังเกต"
          (`RE-208` ครึ่ง "โผล่กลับ" ของ LANE-B · `COO-DECISION 20260903_1942` ข้อ 4 สั่งให้ปิดขั้นนี้ที่นี่
          แทนที่จะผูกกับ `GT-204` ซึ่งถูกยกเลิกแล้ว) · ถ่าย **วิดีโอสั้น** (ไม่ใช่ภาพนิ่ง) คร่อมช่วงฆ่ามอนตัวใหม่
          ในขั้น 4b จนถึงคลิกเก็บในขั้น 5 · **ป้ายชื่อของชิ้นเดิมจากขั้น 2 กะพริบ/หายชั่วขณะแล้วโผล่กลับ
          ระหว่างช่วงนี้ = FAIL ข้อนี้** (บันทึกวินาทีที่เห็น) · **ไม่กะพริบตลอดช่วง = PASS ข้อนี้** ·
          หมายเหตุ: การแก้ปัจจุบัน (`refresh_frames` ต่อท้ายหมัดที่ไม่ฆ่า, ตัวเลือก (ข) ที่ COO รับแล้ว)
          ยังเป็น **`[สมมติของสาย B - รอ COO ยืนยัน]`** จนกว่าข้อนี้จะ PASS บนจอจริง
    🔴 **ห้ามปั๊ม `PASS` จากชั้นเดียว** (`COO 20260903_1249` ข้อ 2): ครบชั้นเดียว = เขียนหัวใบเป็น
      `🟡 <ชั้นที่ครบ> = ... · <ชั้นที่ขาด> = NOT MEASURED · ใบยังไม่ปิด` เท่านั้น
    FAIL ที่คาดไว้วันนี้: `S2` พื้นว่าง **และ/หรือ** ขั้น 5 ปฏิเสธทั้งที่ขั้น 4b ผ่านแล้ว ⇒ **นั่นคือ
      ข้อบกพร่องที่ใบนี้เปิดมาเพื่อจับ** ⇒ ผลนั้น **มีค่าและต้องส่ง** ไม่ใช่รอบเสียเปล่า
      🔴 แต่ FAIL ก็ยังต้องรายงานเป็นสองชั้นแยกกัน ชั้นไหนไม่ได้วัดให้เขียนว่า `NOT MEASURED`
- links: `COO-DECISION 20260903_1048` (คำตัดสิน "ของเป็นของโลกต่อฉาก") · `COO 20260903_0253` (ห้ามลบแถว ledger) ·
  `COO 20260903_1247`/`1946` (ground-preserve ของ LANE-B) · `GT-216` (ตัวปลดคิว) · `GT-204` (ต้นทางของรูปการเก็บของ)
- numbering: คำสั่งตัวนับร่วม (กฎ ②) ได้ `221` · `RE-222` ลงไฟล์ `CLIENT_RE_QUEUE.md` ในคอมมิตเดียวกันนี้ ⇒ ใบนี้ `223`
- result: (ผู้รันกรอก · OBSERVER_CONFIRMED: <ISO+07:00> เมื่อมีชั้น client-observable)

**ผู้เปิดใบ: chief (LANE-E) รอบ `kjtpza` (R319) ตาม `COO 20260903_1048` -- ผู้แก้/ผู้บริโภคผล: LANE-B (COMBAT)**

## GT-224 MOB-AI-TICK-GATE-IS-OPEN-AND-STILL-INVISIBLE-001  [🔧 LANE-K พับผล รอบ `slug54r2` 2026-09-06T13:40+07:00 — 🟡 wire = PASS (`MOB_AI_TICK_LIVE` 1 บรรทัด/เซสชัน ×4 · `mobs=` ตรงฉากที่ยืนทุกครั้ง) · client = รายงานด้วยตา + ภาพ S2 เท่านั้น (ไม่มีภาพ S1) — ไม่ครบตามตัวอักษรของใบ · `OBSERVER_CONFIRMED: 2026-09-04T13:53+07:00` · ผู้เขียนจดหมายเสนอหัวใบนี้เองแล้วทิ้งให้ chief ตัดสินขั้นสุดท้าย (ยังไม่ตัดสิน ณ ที่พบ — LANE-K คัดลอกเท่านั้น ไม่ตัดสินแทน) · จาก notes_to_chief/20260904_1430_KA1A-R309-RESULTS-*.md §GT-224 · เดิม: 🟢 **READY เมื่อ RECHECK ผ่าน — ตัวบล็อกเดิมหมดแล้ว** (chief เจ้าของใบ รอบ `pk14rf`/R326): `#668` **merged 2026-09-03T11:49:37Z** และ main ที่แดงตามมาจากเกตนั้นปลดแล้วด้วย `#670` (merged 12:26:34Z · `ec7bf5f0` · 63 passed) · ~~🔴 BLOCKED รอ merge `#668`~~ · 🔴🆕 **เกณฑ์ `mobs=` เปลี่ยนแล้ว อ่านก่อนบูต:** รอบ `pk14rf` เพิ่ม `_sync_combat_scene_at_edge()` ⇒ บรรทัด `MOB_AI_TICK_LIVE scene=<n> mobs=<n>` รายงาน register **ของฉากที่ยืนอยู่จริง** · ฉากที่ไม่มีตารางมอน (3/4/5/14/278 ทุกฉากนอก bg0001/Bg0002) ต้องได้ **`mobs=0`** · `mobs=4` บนฉากพวกนั้น = **ยังไม่ได้ merge PR ของรอบ `pk14rf`** ไม่ใช่ FAIL ของใบ — เช็ก `git log origin/main` ก่อนสรุป · `RECHECK` ทั้งสองข้อเป็นตัวปลดป้าย ⇒ ผ่าน = `READY` · เจ้าของใบ/ผู้บริโภคผล = chief (LANE-E) ร่วม LANE-B · ผู้รัน = ผู้เทส (attended หรือ unattended ก็ได้ · ~8 นาทีหน้าจอ)]

> 🔴 **PASS ของชั้นจอในใบนี้คือคำว่า "ไม่มีอะไรเปลี่ยน"** -- เส้นทางนี้ไม่ประกอบเฟรมและไม่ส่งอะไรออกสาย
> ผู้เล่นต้อง **ไม่เห็นความแตกต่างใด ๆ** · **มอนขยับเข้าหา/เข้าตี = FINDING ต้องรายงานทันที ไม่ใช่ PASS**
> 🔴🆕 **(chief รอบ `9vec2s` ตาม `COO-DECISION 20260904_1047` ข้อ 4)** หลัง `/warp` ต้อง**รีล็อกอินก่อนเข้าตี** ไม่งั้นไบต์ล็อกอินของฉากไม่ตรงฉากจริง และรั้ว selector ของ `#724` จะ stand-down โดยตั้งใจ (ดู `GT-218`/`(b'')`) -- **stand-down ตรงนี้ไม่ใช่ FAIL ของใบนี้**
> 🔴🆕 **(chief รอบ `9vec2s`)** เกณฑ์ `mobs=0` ข้างบนสำหรับฉาก **5 และ 14** อาจไม่ตรงแล้ว: `server #727` ให้ฉาก 5 มีตาราง `field_mob_tables_bg0005` และฉาก 14 มี `field_mob_tables_bg0015` มาก่อนหน้านั้น -- ทั้งสองฉากอาจรายงาน `mobs=<n>` จริงตอนนี้แทน `mobs=0` ให้เช็ก `field_mobs._SCENE_TABLE_MODULES` บน commit ที่บูตก่อนตัดสิน ไม่ใช่ถือว่า `mobs>0` = ยังไม่ merge

- objective: ข้ออ้างเดียว -- **เกตของ mob-AI tick เปิดจริงบนบิลด์ที่กำลังรันอยู่** (tick ทำงานบนเฟรม
  `TargetPos` จริง) และการเปิดนั้น **ไม่เปลี่ยนอะไรบนจอผู้เล่นแม้แต่อย่างเดียว**

- RECHECK: (รันก่อนเชื่อหัวใบเสมอ · ไม่ผ่านข้อใดข้อหนึ่ง = ยัง `BLOCKED` ห้ามบูต)
  ```
  (cd pirate-force-server && git fetch origin && git grep -n "lane_b_mob_ai_tick.MODULE_NAME" origin/main -- src/pirateforce_foundation/runtime.py)
  (cd pirate-force-server && python3 -m pytest tests/test_mob_ai_tick_gate_wiring.py -q)
  ```
  ข้อ 1 ต้องได้ **>= 1 hit** (0 hit = ยังไม่ merge ⇒ ไม่บูต) · ข้อ 2 ต้อง **เขียวทั้งชุด** บน clone เดียวกัน ·
  ถ้าใช้ branch ก่อน merge ให้เขียนในผลว่าบูต commit ไหน

- db: canonical = `state\pirateforce.sqlite3` -- **สำเนาเท่านั้น ห้ามเปิด canonical** · คัดลอกเป็น
  `state\run_gt224_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา · sha256 canonical ก่อน/หลัง ต้องตรง
  `CANON_SHA.txt` · `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง · (คัดลอก DB ⇒ ตัวละครกลับจุด spawn
  ทุกบูต **เป็นเรื่องปกติ ไม่ใช่ผลวัด**)

- server args: บูตมาตรฐาน · `-SecondPasswordMode bypass` · 🔴 **ไม่มีแฟล็ก `--*-scenario` ใด ๆ**
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt224_<stamp>.sqlite3
  ```
  🔴 **เก็บคอนโซลรวม `2>&1` ไฟล์เดียว** -- `MOB_AI_TICK_LIVE` ออกทาง **stdout** ส่วน `LANE_HOOK_FIRED`
  ออกทาง **stderr** ⇒ เก็บแยกไฟล์จะพลาดหลักฐานไปครึ่งหนึ่ง

- steps:
  1. RECHECK ผ่านทั้งสองข้อ · `LOCK_GAME` · จด boot stamp · sha canonical · คัดลอก DB เป็น run copy
  2. บูตเซิร์ฟเวอร์ **ใหม่สด** ก่อน แล้วค่อยบูตไคลเอนต์ (เคยฆ่าไคลเอนต์ = เซิร์ฟเวอร์ยังถือเซสชันไว้
     ตัวถัดไปจะค้าง "connecting" ตลอดกาล ⇒ **รีสตาร์ตเซิร์ฟเวอร์ก่อนเสมอ**) · ห้ามเปิดไคลเอนต์ทิ้ง
     โดยไม่มีเซิร์ฟเวอร์ (ตายเองใน ~3.5 นาที)
  3. ล็อกอินเข้าฉากตามปกติ · รอโหลดจบ · ภาพนิ่ง `S1` เต็มความละเอียด **ก่อนขยับ** (ให้เห็นตัวละคร +
     HUD + ทุกอย่างที่อยู่รอบตัว)
  4. **เดินด้วย `W/A/S/D` ต่อเนื่องราว 15 วินาที** -- ขั้นนี้บังคับ ไม่ใช่ขั้นตกแต่ง: tick รันเฉพาะบนเฟรม
     `TargetPos` เท่านั้น ไม่เดิน = ไม่มีอะไรให้วัด · ใบนี้ **ไม่ล็อก facing** เดิน/หัน `Q`/`E` ได้ตามสบาย
  5. ยืนนิ่ง ~30 วินาที **มองจออย่างเดียว** · ภาพนิ่ง `S2` มุมเดียวกับ `S1`
  6. 🔴 **ห้ามตี ห้ามคลิกมอนสเตอร์ ห้ามเข้าใกล้จนโดนตี** · 🔴 **ห้ามพิมพ์อะไรลงแชท** (ใบนี้ไม่มีขั้นแชท ·
     ตัวอักษรที่พิมพ์ตอนช่องแชทไม่ได้ focus จะกลายเป็นฮอตคีย์)
  7. ตัวเช็ค NO-CRASH: **คลิกขวาค้างลากหมุนกล้องเท่านั้น** (🔴 ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้ -- มันหมุน
     ตัวละคร ไม่ใช่กล้อง และยิงไบต์ออกสาย) · ภาพนิ่ง `S3` · ออกเกมด้วยปุ่ม X
  8. ปิดเซิร์ฟเวอร์ให้สนิท แล้วคัดหลักฐานจากคอนโซลรวม:
     ```
     findstr /C:"MOB_AI_TICK_LIVE" <ไฟล์คอนโซลรวม>
     findstr /C:"LANE_HOOK_FIRED pirateforce_foundation.lane_hooks.lane_b_mob_ai_tick" <ไฟล์คอนโซลรวม>
     findstr /C:"LANE_B_MOB_AI_TICK actor=" <ไฟล์คอนโซลรวม>
     ```
  9. เก็บคอนโซล + `capture_v141\GAME_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ ·
     **รัน teardown เสมอ** แม้รอบจบเพราะเลิกเล่นเฉย ๆ (เทมเพลตปฏิเสธ boot stamp เก่ากว่า 420 นาที) ·
     ห้าม commit เอง

- pass criteria: (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด** -- "จอไม่มีอะไรเปลี่ยน"
  ไม่ใช่หลักฐานว่าเกตยังปิด และ `MOB_AI_TICK_LIVE` ไม่ใช่หลักฐานว่าจอนิ่ง · ครบชั้นเดียว = เขียนหัวใบว่า
  `🟡 <ชั้นที่ครบ> = ... · <ชั้นที่ขาด> = NOT MEASURED · ใบยังไม่ปิด` ห้ามปั๊ม `PASS`)
    wire/DB (อ่านจากคอนโซล + run copy · ไม่ต้องมีตาคน):
      (1) `MOB_AI_TICK_LIVE scene=<เลข> mobs=<เลข>` ปรากฏ **หนึ่งบรรทัดพอดีต่อหนึ่งเซสชันล็อกอิน**
          (0 บรรทัด = เกตยังปิด/บูตบิลด์เก่า/ไม่ได้เดิน · >1 = finding) · `scene=` ต้องตรงกับฉากที่ยืนจริง ·
          🔴 **`mobs=0` เป็นค่าวัดจริงของ register ที่ว่าง ไม่ใช่ความเสีย ห้ามอ่านเป็น FAIL**
          🔴 **`mobs=` เชื่อไม่ได้ว่าเป็นมอนของฉากที่ `scene=` บอก** (chief วัดเอง R324 · ใบ `20260903_1855` ถึง COO):
          `register` ถูกเปิดใหม่เฉพาะตอนโจมตี และเฉพาะฉาก 1 กับ 2 ⇒ ล็อกอินบ้านแล้ววาปไปฉากอื่น
          บรรทัดจะรายงานจำนวนของ **ฉากก่อนหน้า** · **ให้จดตัวเลขตามที่เห็น ห้ามสรุปว่าฉากนั้นมีมอนกี่ตัว**
          ตัวเลขที่ไม่ตรงกับจำนวนมอนที่เห็นบนจอ = **หลักฐานยืนยันใบ `1855` ไม่ใช่ FAIL ของใบนี้**
      (2) `LANE_HOOK_FIRED pirateforce_foundation.lane_hooks.lane_b_mob_ai_tick vital_inbound_target_pos_mob_ai_tick`
          อย่างน้อย **หนึ่งบรรทัด** (ปกติหลายบรรทัด = หนึ่งต่อเฟรม `TargetPos`)
      (3) `integrity_check` = `ok` · sha canonical ตรงก่อน/หลัง · **ไม่มี traceback หลุด**
      (4) `LANE_B_MOB_AI_TICK actor=...` **มีหรือไม่มีก็ได้ ไม่ใช่เกณฑ์** (พิมพ์เฉพาะแถวที่เปลี่ยนเฟส) --
          เห็นแล้วให้คัดทั้งบรรทัดแนบมาด้วย
      **ชั้นนี้ตอบไม่ได้เลยว่า:** บนจอเกิดอะไรขึ้นหรือไม่เกิด
    client-observable (**ต้องมีตาคน · ห้ามอนุมานจากคอนโซล**):
      (5) **ไม่มีอะไรเปลี่ยนบนจอเลย**: ไม่มีมอนเดินเข้าหา · ไม่มีการเข้าตี · ไม่มีดาเมจ · ไม่มีเลข/ตัวเลข
          ใหม่โผล่ · หลอด HP ไม่ขยับ · `S2` เทียบ `S1` มอนตัวเดิมอยู่ตำแหน่งเดิม
      (6) 🔴 บันทึก **สีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** ครบทั้ง `S1`-`S3` ·
          เขียนคำว่า `none` ออกมาแทนการเว้นว่าง · อ่านสีจาก **ภาพนิ่งเต็มความละเอียดเท่านั้น** ห้าม
          contact sheet / ภาพย่อ / วิดีโอ · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุของสี** (`RE-067` เป็นเจ้าของ
          คำถามนั้น) · ความต่างจากภาพเซิร์ฟเวอร์จริงลง `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      🔴 (7) **มอนขยับเข้าหา/เข้าตี/หลอดลด = FAIL ของชั้นนี้ และเป็น FINDING ที่ต้องส่งทันที** ⇒ หยุดเล่น
          จดเวลานาฬิกา (+07:00) เก็บคอนโซลทั้งไฟล์ ห้ามตีความเอง
    🔴 ปิดใบด้วย `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` เท่านั้น (G-OBS) · ครบหลักฐานแต่ยังไม่มี
    ลายเซ็นคน = `AWAITING-OBSERVER` ซึ่ง **ไม่ใช่ PASS และไม่ใช่ FAIL**

- prediction (**คำทำนาย ไม่ใช่ผลวัด** · ทำนายผิด = finding ไม่ใช่ความล้มเหลว):
    P1 ได้ทั้งสองโทเคน **และ** จอไม่เปลี่ยนอะไรเลย ⇒ ผ่านทั้งสองชั้น (นี่คือที่คาดไว้)
    P2 ไม่มี `MOB_AI_TICK_LIVE` เลย ⇒ บูตบิลด์เก่า / ไม่ได้เดินจริง / เซสชันขาดตัวประกอบข้อใดข้อหนึ่ง ⇒
       **NO-RESULT ไม่ใช่ FAIL** · รัน RECHECK ใหม่แล้วรายงานว่าบูต commit ไหน
    P3 มีโทเคนครบ **แต่มอนขยับ/เข้าตี** ⇒ มีอะไรออกสายจากที่ที่เราคิดว่าเงียบ ⇒ **ผลที่มีค่าที่สุดของใบนี้**
    🔴 **ผลลบมีค่าเท่าผลบวก** -- P2 ชี้ไปที่ตัวบิลด์/ขั้นตอน · P3 ชี้ไปที่ Door B รั่ว · คนละที่กันคนละใบกัน

- nonclaims:
  1. **ไม่พิสูจน์ว่า resolver ผิด** -- `module_production_allowed()` ไม่ถูกแตะในรอบนี้ การตอบ `False`
     บนชื่อที่ไม่มีโมดูลไหนเป็นเจ้าของคือ **หน้าที่ของมัน** (fail-closed) การซ่อมอยู่ที่ฝั่งผู้เรียก
  2. **ไม่เปิด Door B** -- `mob_aggro.ATTACK_INTENT_DELIVERABLE` ยัง `False` ⇒ ใบนี้ไม่ใช่หลักฐานว่า
     ความตั้งใจของ AI ถูกแปลงเป็นไบต์ที่ไคลเอนต์เรนเดอร์ได้
  3. **ไม่ตัดสินว่าการตัดสินใจของ AI ถูกต้องไหม** (phase/threat/aggro) -- ใบนี้วัดแค่ว่า **มันได้รัน**
  4. ไม่พิสูจน์อะไรกับ **P-1** (ของบนพื้น) หรือ **P-2** (สีป้ายมอน) · ไม่ใช่ใบตีมอน ⇒ ห้ามมีขั้นตีมอน
  5. ไม่พิสูจน์อะไรข้าม relog หรือบน canonical -- รอบนี้บูตบน **สำเนา**

- links: `src/pirateforce_foundation/runtime.py` จุดเรียกเกต tick ใน `dispatch()` (เงื่อนไขหกข้อ + บรรทัด
  `MOB_AI_TICK_LIVE`) · `src/pirateforce_foundation/lane_hooks/lane_b_mob_ai_tick.py:120-121,180`
  (`MODULE_NAME` / `POINT` / `announce_direct_fire`) ·
  `src/pirateforce_foundation/lane_hooks/__init__.py:498-508` (โทเคน `LANE_HOOK_FIRED` -> stderr) ·
  `src/pirateforce_foundation/mob_aggro.py` (`ATTACK_INTENT_DELIVERABLE = False`) ·
  `tests/test_mob_ai_tick_gate_wiring.py` · `COO-DECISION 20260903_1648` ข้อ 3 และ 4 ·
  `CORE-REQUEST 20260903_1639` (LANE-B) · `GT-215` (วินัย db/teardown ที่ใบนี้ยืมมา)
- numbering: คำสั่งตัวนับร่วม (กฎ ②) คืนค่า `223` ⇒ ใบนี้ `224` · `GT-224`/`RE-224` = **0 hit** ทั้งสามที่
- result: (ผู้รันกรอก: PASS/FAIL/BLOCKED/NO-RESULT ต่อชั้น · บรรทัด `MOB_AI_TICK_LIVE` ดิบ ·
  จำนวนบรรทัด `LANE_HOOK_FIRED` · บรรทัด `LANE_B_MOB_AI_TICK` ถ้ามี · ภาพ `S1`-`S3` ·
  บรรทัดสีป้ายครบทุกป้ายทุกภาพ · sha256 · commit ที่บูต · timestamp +07:00 ·
  `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: chief (LANE-E) รอบ `gjyxt5` (R324) -- ผู้บริโภคผล: chief ร่วม LANE-B**

## GT-225 GROUND-CELL-FOLLOWS-A-WALKING-PLAYER-ACROSS-A-SCENE-EDGE-001  [🔴 **BLOCKED — คิวหลัง `GT-215`** (`COO-DECISION 20260903_2346` ข้อ 3 · ยืนตาม `COO-DECISION 20260904_0145` ข้อ 2) · เปิดโดย chief รอบ `dwvbpm` (R330) ตาม `COO 20260904_0145` ข้อ 2 คำต่อคำ ("ของที่ไม่มีเลขใบคือของที่หายได้") · **เจ้าของใบ/ผู้แก้ = chief (LANE-E)** ตาม `COO 20260903_2250` ข้อ 5 — **ไม่ใช่ LANE-B** · **ผู้รัน = ผู้เทส (attended หรือ unattended)** · `RECHECK` เป็นตัวปลดป้าย]

> 🔴 **ใบข้อบกพร่อง ไม่ใช่ใบสำรวจ** — คำตัดสินมีอยู่แล้ว: ของที่ตกแล้วเป็นของ **"โลก" ผูกกับ "ฉาก"**
> (`COO 20260903_1048`) ⇒ cell ที่ยังประกาศฉากเก่าอยู่หลังผู้เล่น **เดิน** ข้ามขอบฉาก = ข้อบกพร่องจริง
> 🔴 **ห้ามซ่อมด้วยการกวาดแถว ledger ทิ้ง** (`COO 20260903_0253` ยืน) · 🔴 **ห้ามแตะ `store.py`** (ประตูเขียนเป็นของ LANE-DB/LANE-B)

- objective: ข้ออ้างเดียว -- **ผู้เล่นที่เดินข้ามขอบฉาก (ไม่ใช่ `/warp`) ทำให้ `DropLedgerCell`
  ประกาศฉากใหม่** ⇒ ของที่ตกในฉากใหม่ถูกเก็บได้โดยไม่ต้องวาปก่อน และของฉากเก่าไม่รั่วข้ามมา

- ที่มาของหนี้ (chief วัดเอง 2026-09-04T01:5x+07:00 บน `origin/main` `0765f0e1`):
  `_mob_loot_cross_scene_boundary()` (`src/pirateforce_foundation/runtime.py:6751`) เป็นตัวเดียวที่บอก cell ว่า
  ข้ามฉาก และมี **ผู้เรียกจุดเดียว** คือ `runtime.py:6749` ในเส้นทาง **GM warp** เท่านั้น
  · `_sync_combat_scene_at_edge()` (`runtime.py:4621`) ที่ `#675` เพิ่มเข้ามา จับขอบฉากได้ทุกประตูจริง
  **แต่ไม่แตะ `DropLedgerCell` เลยแม้แต่บรรทัดเดียว** โดยเจตนา (docstring ของมันเอง "GROUND ROWS ARE NOT TOUCHED"
  ตามเงื่อนไข `COO 20260903_0253`) ⇒ **`#675` ไม่ปิดหนี้นี้** (chief รายงานแล้วในจดหมาย `20260904_0027` ข้อ 3)
  · ผลที่ผู้เล่นเจอ: หลังเดินข้ามฉาก คลิกเก็บของได้ `cell_has_no_scene` หรือแย่กว่านั้นคือ cell ยังประกาศฉากเก่า

- 🔴 **สิ่งที่ใบนี้ยังไม่อ้าง (nonclaim)**: ยังไม่วัดว่าการเดินข้ามขอบฉากในเกมวันนี้ **ทำได้จริงหรือยัง**
  ในบิลด์ที่รันอยู่ (ทางข้ามฉากที่พิสูจน์แล้วคือ `/warp <n>` ของ GM) ⇒ ถ้าผู้เทสเดินข้ามขอบไม่ได้เลย
  ให้รายงานว่า `NOT MEASURABLE YET` **ไม่ใช่ PASS และไม่ใช่ FAIL** แล้วส่งกลับให้ chief

- RECHECK: (รันก่อนเชื่อหัวใบเสมอ · **ข้อ 1 ไม่ผ่าน = ยัง BLOCKED ห้ามบูต** · รันจากรากรีโป `pf_bridge`)
  ```
  grep -n "^## GT-215 " GAME_TEST_QUEUE.md
  git -C ../pirate-force-server fetch origin && git -C ../pirate-force-server grep -c "_mob_loot_cross_scene_boundary" origin/main -- src/pirateforce_foundation/runtime.py
  ```
  ข้อ 1 ต้องอ่านหัวใบ `GT-215` แล้วเห็นว่ามันปิดแล้ว (`PASS`/`FAIL`/`CANCELLED` ก็ได้ — ตัวกำหนดคือ **ลำดับคิว**
  ไม่ใช่ผล) · ยังเปิดอยู่ = **ยัง BLOCKED**
  ข้อ 2 คือตัวชี้ว่าหนี้ยังอยู่: ได้ **`2`** = ยังมีผู้เรียกจุดเดียว (นิยาม + จุดเรียก GM warp) ⇒ หนี้ยังไม่จ่าย ·
  ได้ **`>= 3`** = มีผู้เรียกใหม่แล้ว ⇒ chief ต้องอัปเดตหัวใบก่อนบูต

- db: **สำเนาเท่านั้น ห้ามเปิด canonical** · `state\run_gt225_<stamp>.sqlite3` · วินัย sha canonical /
  `integrity_check` **ตามช่อง `db:` ของ `GT-215` ทุกบรรทัด**
- server args: บูตมาตรฐาน · `-SecondPasswordMode bypass` · 🔴 **ไม่มีแฟล็ก `--*-scenario` ใด ๆ** ·
  เก็บคอนโซลรวม stdout+stderr ไฟล์เดียว (`2>&1`)

- steps: (ราว 8 นาทีหน้าจอ · เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง · **ห้ามรีสตาร์ทเซิร์ฟเวอร์ระหว่างขั้น 2-5**)
  1. RECHECK ผ่าน · `LOCK_GAME` · boot stamp · sha canonical · คัดลอก DB
  2. เข้าเกมฉากเริ่ม · ฆ่ามอนหนึ่งตัวจนมีของตก · **อย่าเพิ่งเก็บ** · คัดบรรทัดของตกทั้งบรรทัด
  3. **เดินข้ามขอบฉากด้วยเท้า** ไปฉากติดกัน — 🔴 **ห้ามใช้ `/warp`** (วาปคือเส้นทางที่จ่ายหนี้ไปแล้ว
     ใช้แล้วใบนี้วัดคนละเรื่อง) · จดว่าเดินออกทางไหน · ถ้าเดินข้ามไม่ได้เลย ⇒ `NOT MEASURABLE YET` แล้วหยุด
  4. ในฉากใหม่: ฆ่ามอนหนึ่งตัว · ภาพนิ่ง `S1` ให้เห็นของบนพื้นของฉากใหม่ · คัดบรรทัดของตกทั้งบรรทัด
  5. คลิกเก็บของชิ้นนั้น · ภาพนิ่ง `S2` ให้เห็นกระเป๋า · คัดบรรทัดเก็บของทั้งบรรทัด
  6. teardown ตาม `GT-215` ข้อ 12 · ห้าม commit เอง

### 🔴 โทเคนที่ห้ามอ่านว่าเสีย (`COO-DECISION 20260903_0953` ข้อ 2)
  **`cell_has_no_scene` ก่อนการฆ่ามอนตัวแรก *ของเซสชันล็อกอินนั้น* = ปกติ ห้ามรายงาน FAIL** ·
  ข้อความ `does not know which scene it is in` = กรณีปกติ · `could not answer which scene it is in (<เหตุ>)` = **finding เสมอ**

- pass criteria: (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น** · **ห้ามปั๊ม `PASS` จากชั้นเดียว** `COO 20260903_1249` ข้อ 2)
    wire/DB (อ่านจากคอนโซล + run copy):
      (1) ขั้น 4 มีบรรทัดของตกที่ระบุ **ฉากใหม่** (เทียบเลขฉากกับที่ผู้เทสเดินเข้าไปจริง — **เทียบค่า** ไม่ใช่ grep เจอ)
      (2) ขั้น 5 มีบรรทัดเก็บของสำเร็จ (แถวเข้ากระเป๋า) **ไม่ใช่** `cell_has_no_scene`
      (3) ไม่มีบรรทัดที่ประกาศ **ฉากเก่า** หลังขั้น 3 (cell ค้างฉากเดิม = FAIL ข้อนี้ คือข้อบกพร่องที่ใบนี้เปิดมาจับ)
      (4) `AFTER` ของ run copy มีของชิ้นนั้นในกระเป๋า · `integrity_check` = `ok` · sha canonical ตรง · ไม่มี traceback หลุด
    client-observable (ตาคนเท่านั้น):
      (5) `S1` เห็นของอยู่บนพื้นในฉากใหม่ · (6) `S2` เห็นของชิ้นนั้นเข้ากระเป๋า
      (7) ของของ **ฉากเก่า** ไม่โผล่มาวางในฉากใหม่ (การรั่วข้ามฉาก) — โผล่ = FAIL ข้อนี้และรายงานทันที
    FAIL ที่คาดไว้วันนี้: ขั้น 5 ถูกปฏิเสธ และ/หรือ ข้อ (3) พบฉากเก่า ⇒ **นั่นคือข้อบกพร่องที่ใบนี้เปิดมาเพื่อจับ**
      ผลนั้นมีค่าและต้องส่ง · ชั้นไหนไม่ได้วัดเขียน `NOT MEASURED`
- links: `COO-DECISION 20260904_0145` ข้อ 2 (คำสั่งออกเลขใบ) · `COO 20260903_2346` ข้อ 3 (ลำดับหลัง `GT-215`) ·
  `COO 20260903_2250` ข้อ 5 (เจ้าของ = chief) · `COO 20260903_1048` (ของเป็นของโลกต่อฉาก) ·
  `COO 20260903_0253` (ห้ามลบแถว ledger) · จดหมาย `20260904_0027` ข้อ 3 (หลักฐานว่า `#675` ไม่ปิด) · `GT-223` (ใบพี่น้อง ฝั่งรีล็อกอิน)
- numbering: คำสั่งตัวนับร่วม (กฎ ② หัวไฟล์) คืน `224` ณ 2026-09-04T01:5x+07:00 ⇒ ใบนี้ `225` · ไม่มีการจองล่วงหน้า
- result: (ผู้รันกรอก · OBSERVER_CONFIRMED: <ISO+07:00> เมื่อมีชั้น client-observable)

**ผู้เปิดใบ: chief (LANE-E) รอบ `dwvbpm` (R330) ตาม `COO 20260904_0145` ข้อ 2 -- ผู้แก้/ผู้บริโภคผล: chief (LANE-E)**

## GT-226 LOGIN-DRAWS-THE-CLASS-SHE-PICKED-AT-CREATION-001  [🔴 **BLOCKED — รอ merge ก่อน: `pirate-force-server#705` (กิ่ง `claude/gallant-noether-3kwnnr`) ยังไม่อยู่บน `main`** · เปิดโดย chief (LANE-E) รอบ `3kwnnr` (R332) 2026-09-04T05:2x+07:00 ตาม `COO-DECISION 20260904_0446` ข้อ 2-3 · **เจ้าของใบ/ผู้บริโภคผล = chief (LANE-E)** · **ผู้รัน = Panya (attended เท่านั้น — ใบนี้รัน unattended ไม่ได้โดยโครงสร้าง)** · `RECHECK` เป็นตัวปลดป้าย]

> 🔴 **ใบนี้เกรดชั้นจอชั้นเดียว** — ชั้น wire/DB **พิสูจน์ไปแล้วในรอบนี้** ด้วย `tests/test_class_id_login_wiring.py`
> บน fixture **Sniper (class 4)** ซึ่งเป็นเลขที่ไม่มีค่าคงตัวหรือ default ของ migration ไหนในรีโปถืออยู่
> ⇒ **ใบนี้ไม่ถามซ้ำ ห้ามบูตเพื่อวัดสิ่งที่วัดแล้ว** · สิ่งที่ยังไม่มีใครเห็นคือ **ไคลเอนต์วาดอะไร**

- objective: (ข้ออ้างเดียว) ตัวละครที่ **สร้างใหม่โดยเลือกคลาสที่ไม่ใช่ Gladiator** ล็อกอินแล้ว **ไคลเอนต์
  แสดงคลาสนั้น** และแสดงซ้ำใน **การล็อกอินครั้งที่สอง** — ครั้งที่สองไม่ใช่ข้ออ้างที่สอง มันคือตัวหักล้างว่า
  สิ่งที่เห็นมาจากแถวใน DB ไม่ใช่จากแพ็กเก็ตตอนสร้างที่ยังค้างในหน่วยความจำ

- สิ่งที่ลงในกิ่งรอบนี้ (**ยังไม่อยู่บน `main`**): (ก) CREATE — `lifecycle.persist_class_id_from_starting_gear`
  แกะสามช่องของเสื้อผ้าเริ่มต้น (`n_DRESS_CHEST`/`n_DRESS_LEGGINGS`/`n_SLOT_RHAND`) จาก AvatarAttr ที่เพิ่งเก็บ
  เทียบกับห้า preset ของ `CONSTDATA_TH__CHARCREATE_CLASS` **แบบตรงเป๊ะเท่านั้น** แล้วเขียน `characters.class_id`
  · ไม่ตรง = คอลัมน์ยัง NULL **และตัวละครยังถูกสร้างตามปกติ** · (ข) LOGIN — `session.select_and_start` อ่าน
  คอลัมน์นั้นขึ้นตัวละคร แล้ว `legacy_bridge.start_game` ส่งเป็น `ActorAttr` class (`u32tag 0x19`) ·
  แถว NULL ⇒ `player_wire.PLAYER_LOGIN_CLASS_ID = 1` (Gladiator) เหมือนเดิม
  · เลขคลาส: **1 Gladiator · 2 Paladin · 4 Sniper · 16 Necromancer · 32 Sorcerer**

### โทเคนคอนโซล (stderr) ที่ผู้เทส grep ได้
```
CHARACTER_CLASS_ID cid=<n> written class_id=<k>
CHARACTER_CLASS_ID cid=<n> not_written reason=starting_gear_matches_no_single_preset
LOGIN_CLASS_ID from_row class_id=<k>
LOGIN_CLASS_ID fallback class_id=1 reason=row_has_no_class_id
```

- RECHECK: (รันก่อนเชื่อหัวใบเสมอ · **ข้อใดไม่ผ่าน = ยัง BLOCKED ห้ามบูต** · รันจากรากรีโป `pf_bridge`)
  ```
  git -C ../pirate-force-server fetch --unshallow origin || git -C ../pirate-force-server fetch origin
  git -C ../pirate-force-server merge-base --is-ancestor cf16e5f7 origin/main && echo MERGED
  git -C ../pirate-force-server grep -c "CHARACTER_CLASS_ID" origin/main -- src/pirateforce_foundation/lifecycle.py
  git -C ../pirate-force-server grep -c "LOGIN_CLASS_ID" origin/main -- src/pirateforce_foundation/session.py
  (cd ../pirate-force-server && python3 -m pytest tests/test_class_id_login_wiring.py -q)
  ```
  ข้อ 2 ต้องพิมพ์ `MERGED` (🔴 **ต้องเป็นโคลนที่ `--unshallow` แล้ว** มิฉะนั้น merge-base ตอบผิดได้ · `cf16e5f7`
  = commit ของงานนี้บนกิ่ง ถ้า merge commit ต่างไป ให้ใช้ sha ของ `#705` ที่ merge จริง) ·
  ข้อ 3 และ 4 ต้อง **>= 1 hit** · ข้อ 5 ต้องเขียวทั้งไฟล์ · บูตกิ่งก่อน merge = เขียนในผลว่าบูต commit ไหน

- db: canonical = `state\pirateforce.sqlite3` — **สำเนาเท่านั้น ห้ามเปิด canonical** · คัดลอกเป็น
  `state\run_gt226_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา · sha256 canonical ก่อน/หลังต้องตรง `CANON_SHA.txt` ·
  `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง · (คัดลอก DB ⇒ ตัวละครกลับจุด spawn ทุกบูต **ปกติ ไม่ใช่ผลวัด** ·
  ตัวละครที่เกิดในใบนี้อยู่แค่ในสำเนา รอบหน้าไม่มีมัน)
- server args: บูตมาตรฐาน · `-SecondPasswordMode bypass` · 🔴 **ไม่มีแฟล็ก `--*-scenario` ใด ๆ** ·
  เก็บคอนโซลรวม stdout+stderr ไฟล์เดียว (`2>&1`)
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt226_<stamp>.sqlite3
  ```

- steps: (~12 นาทีหน้าจอ · **เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลังเสมอ** · 🔴 **ห้ามรีสตาร์ตเซิร์ฟเวอร์ระหว่างข้อ 3-12**)
  1. RECHECK ผ่านทุกบรรทัด · `LOCK_GAME` · จด boot stamp · sha canonical · คัดลอก DB
  2. **วัด DB ก่อนบูต** (เซิร์ฟเวอร์ยังไม่เปิด · อ่านอย่างเดียว) คัดผลทุกบรรทัดเป็นบล็อก `BEFORE`:
     ```
     python -c "import sqlite3,sys;c=sqlite3.connect('file:%s?mode=ro'%sys.argv[1],uri=True);[print(r) for r in c.execute('SELECT id,selector,name,class_id,deleted_at FROM characters ORDER BY id')]" "state\run_gt226_<stamp>.sqlite3"
     ```
     🔴 `mode=ro` คือของจริง ห้ามตัดออก · ห้ามชี้ canonical · ห้ามรันตอนเซิร์ฟเวอร์เปิดอยู่
  3. บูตเซิร์ฟเวอร์ **ใหม่สด** ก่อน แล้วค่อยบูตไคลเอนต์ (เคยฆ่าไคลเอนต์ = เซิร์ฟเวอร์ยังถือเซสชันไว้ ตัวถัดไป
     ค้าง "connecting" ตลอดกาล ⇒ **รีสตาร์ตเซิร์ฟเวอร์ก่อนเสมอ**) · ห้ามเปิดไคลเอนต์ทิ้งโดยไม่มีเซิร์ฟเวอร์ (ตายเองใน ~3.5 นาที)
  4. ล็อกอินถึง **หน้าเลือกตัวละคร** · `S0` เต็มความละเอียด เห็นรายชื่อทั้งหมด (ตัวเก่าคือ control ของใบนี้ **ห้ามลบ**)
  5. กด **ปุ่มที่ 2 = สร้างตัวละคร** (🔴 ปุ่มแรกซ้ายสุด = **ลบ** ห้ามแตะ) · **เลือกคลาสที่ไม่ใช่ Gladiator**
     (Sniper/Sharpshooter หรือ Sorcerer) · จด **ชื่อคลาสที่ไคลเอนต์เขียนบนจอคำต่อคำ** · `S1` เต็มความละเอียด เห็นคลาสที่เลือก
  6. **คลิกช่องชื่อให้ขึ้น cursor ก่อน** แล้วพิมพ์ `GT226CLASS01` (ถูกปฏิเสธ/ซ้ำ ⇒ `GT226CLASS02` แล้วจดว่าใช้ชื่อไหน) ·
     🔴 พิมพ์ได้เฉพาะตอนช่องชื่อ focus — นอกช่องทุกตัวอักษรกลายเป็นฮอตคีย์ · **ใบนี้ไม่มีขั้นแชท ห้ามพิมพ์ลงแชท**
  7. กดยืนยันหนึ่งครั้ง · `S2` = หน้าเลือกตัวละครหลังสร้าง (เห็นชื่อใหม่) · คัดบรรทัด `CHARACTER_CLASS_ID` **ทั้งบรรทัด**
  8. **LOGIN#1** เข้าเกมด้วยตัวใหม่ · `S3` เต็มความละเอียด เห็นตัวละคร + HUD · **อ่านจากจอแล้วจดตรง ๆ**: ไคลเอนต์
     เขียนคลาสไว้ที่ไหนบ้าง (หน้าเลือกตัวละคร / หน้าต่างข้อมูลตัวละคร / HUD) และเขียนว่าอะไร — คำต่อคำ ห้ามเดา ·
     ตรวจบล็อก "สมประกอบ" ตาม `PANYA-DECISION 20260828_0125` ก่อนเกรด: level 1 · stats จาก `CHARCREATE_CLASS s_SCORE` ·
     HP/MP จาก `STANDARD_STATUS` · speed `ActorAttr` x7 = 400 · ชื่ออยู่ `BasicAttr` x1 **ห้ามอยู่ x37** · x39/x41/x42 = 0
     🔴 **ยกเว้นช่อง "class 1" ของบล็อกนั้น ซึ่งใบนี้เป็นตัวแก้** — ตัวใหม่ต้องเป็นคลาสที่เธอเลือก
  9. กด `K` หนึ่งครั้ง (หน้าต่างสกิล) · จดว่าเปิดหรือไม่เปิด · `S4` · 🔴 **ไม่เปิด ≠ FAIL ของใบนี้**
     (`GT-058`/`GT-059` ปิด bounded-negative ว่าเซิร์ฟเวอร์ไม่เคยส่งสถานะสกิล · โพรบของเจ้าของ 27 ส.ค. บันทึกว่า
     เปิดได้เมื่อมี class — สองบันทึกขัดกัน ใบนี้เก็บ **ข้อสังเกต** ไม่ใช่คำตัดสิน) · กดเฉพาะ `K` ห้ามกดตัวอักษรอื่น
  10. กลับหน้าเลือกตัวละคร แล้ว **LOGIN#2 ด้วยตัวเดิม** · `S5` มุมเดียวกับ `S3` · อ่านคลาสบนจออีกครั้ง ·
      คัดบรรทัด `LOGIN_CLASS_ID` ของทั้งสองครั้ง
  11. **CONTROL**: ล็อกเอาต์ แล้วล็อกอิน **ตัวละครเก่า** (สร้างก่อนรอบนี้ คอลัมน์เป็น NULL) เข้าเกมจนยืนในฉาก · `S6` ·
      🔴 ล็อกอินไม่ผ่าน/ค้าง = **FAIL ของใบนี้** ไม่ใช่ข้อสังเกตแยกใบ
  12. ตัวเช็ค NO-CRASH: **คลิกขวาค้างลากหมุนกล้องเท่านั้น** — 🔴 ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้: มันหมุน **ตัวละคร**
      (กล้องแค่แพนตาม) และยิง `TargetPosVital` ออกสาย เช่นเดียวกับ `W/A/S/D` · คลิกขวาลาก **ไม่เปลี่ยน facing และ
      ไม่ส่งไบต์ใด ๆ** ปลอดภัยทุกจังหวะ · ออกเกมด้วยปุ่ม X
  13. ปิดเซิร์ฟเวอร์ให้สนิท · รันคำสั่งข้อ 2 ซ้ำคำต่อคำเป็นบล็อก `AFTER` · เก็บคอนโซลรวม + `capture_v141\GAME_LIVE.txt`
      + sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **รัน teardown เสมอ** แม้รอบจบเพราะเลิกเล่นเฉย ๆ
      (เทมเพลตปฏิเสธ boot stamp เก่ากว่า 420 นาที) · ห้าม commit เอง

- pass criteria: (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**)
    wire/DB (อ่านจากคอนโซล + run copy · ไม่ต้องมีตาคน · 🔴 **ไม่ใช่ชั้นที่ใบนี้เกรด** — เก็บเป็นบริบทและตัวชี้ทาง):
      (1) มี `CHARACTER_CLASS_ID ... written class_id=<k>` **หรือ** `... not_written reason=starting_gear_matches_no_single_preset`
          — **ทั้งสองแบบเป็นค่าวัดที่ถูกต้อง** คัดทั้งบรรทัด
      (2) LOGIN#1 และ LOGIN#2 ของตัวใหม่มีบรรทัด `LOGIN_CLASS_ID` (from_row หรือ fallback ตามสภาพแถว)
      (3) control ตัวเก่าได้ `LOGIN_CLASS_ID fallback class_id=1 reason=row_has_no_class_id` — **ถูกต้องตามที่ตั้งใจ ห้ามอ่านเป็น FAIL**
      (4) `AFTER`: แถวใหม่มี `class_id` ตรงกับ `<k>` ในข้อ 1 · **แถวเก่าทุกแถวเหมือน `BEFORE` เป๊ะ** (ไม่มี UPDATE ตัวเก่าในคอมมิตนี้ ⇒ เปลี่ยน = FAIL ทันที)
      (5) `integrity_check` = `ok` · sha canonical ตรง · ไม่มี traceback หลุด
      **ชั้นนี้ตอบไม่ได้เลยว่า:** ไคลเอนต์วาดคลาสอะไรบนจอ
    client-observable (**ชั้นที่ใบนี้เกรด · ต้องมีตาคน ห้ามอนุมานจากคอนโซล/DB**):
      (6) `S1` เห็นหน้าจอสร้างพร้อมคลาสที่เลือก **ไม่ใช่ Gladiator** + ชื่อคลาสบนจอคำต่อคำ
      (7) `S3` (LOGIN#1) ไคลเอนต์แสดงคลาสของตัวใหม่ = คลาสในข้อ 6 · จด **ทีละบรรทัดว่าเห็นที่ไหน/เขียนว่าอะไร** ·
          ไม่ปรากฏที่ไหนเลย = เขียนคำว่า `none` ออกมา
      (8) `S5` (LOGIN#2) เห็นคลาสเดิมซ้ำ — **ข้อนี้คือหัวใจของใบ**
      (9) `S6` control: ตัวละครเก่าเข้าเกมได้จนยืนในฉาก (คลาสที่แสดงจะเป็น Gladiator — **ห้ามเกรดเป็น FAIL**)
      (10) 🔴 บันทึก **สีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** ครบ `S0`-`S6` · เขียน `none`
          แทนการเว้นว่าง · อ่านสีจาก **ภาพนิ่งเต็มความละเอียดเท่านั้น** ห้าม contact sheet/ภาพย่อ/วิดีโอ ·
          **จดสีอย่างเดียว ห้ามอนุมานสาเหตุของสี** (`RE-067` เป็นเจ้าของคำถามนั้น) · ต่างจากภาพเซิร์ฟเวอร์จริง ⇒
          `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      (11) `K` เปิดหรือไม่เปิด = **ข้อสังเกต ไม่ใช่เกณฑ์**
      **ชั้นนี้ตอบไม่ได้เลยว่า:** คอลัมน์ในแถวมีค่าอะไร
    🔴 ปิดใบด้วย `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` เท่านั้น (G-OBS) · หลักฐานครบแต่ไม่มีลายเซ็นคน =
    `AWAITING-OBSERVER` ซึ่ง **ไม่ใช่ PASS และไม่ใช่ FAIL** · ชั้นจอไม่ครบ = ใบไม่ปิด เขียน `NOT MEASURED` ตามข้อ

- อ่านผลอย่างไร (**routing ไม่ใช่เกณฑ์ผ่าน** · ห้ามใช้แทนหลักฐานของชั้นใดชั้นหนึ่ง):
    จอเป็น Gladiator + คอนโซล `not_written` ⇒ ปมอยู่ที่ **หน้าจอสร้าง** (ไอเทมที่ส่งไม่ตรงแถว preset) ไม่ใช่เส้นล็อกอิน ·
    จอเป็น Gladiator + คอนโซล `written class_id=<k!=1>` ⇒ ปมอยู่ **หลัง DB** (เส้นล็อกอินหรือไคลเอนต์) — ผลที่มีค่าที่สุดของใบ

- prediction (**คำทำนาย ไม่ใช่ผลวัด** · ทำนายผิด = finding ไม่ใช่ความล้มเหลว):
    P1 `written class_id=<k!=1>` และจอแสดงคลาสนั้นทั้งสองครั้ง ⇒ ชั้นจอผ่าน (นี่คือที่คาดไว้)
    P2 `not_written reason=starting_gear_matches_no_single_preset` ⇒ **สมมติฐานหน้าจอสร้างไม่จริงสำหรับคลาสนั้น** ⇒
       ชั้นจอ = `NOT MEASURABLE` **ไม่ใช่ FAIL และไม่ใช่บั๊กของเซิร์ฟเวอร์** · คัดบรรทัดคอนโซลคำต่อคำแล้วส่ง ·
       เหลือเวลา = ลองอีกคลาสหนึ่งแล้วจดทั้งสองบรรทัด
    P3 `written class_id=<k!=1>` แต่จอยังเป็น Gladiator ⇒ **FAIL ของชั้นจอ** และเป็นผลที่มีค่าที่สุด ⇒ ส่งทันที
    P4 control ตัวเก่าล็อกอินไม่ผ่าน/ค้าง ⇒ **FAIL ของใบนี้** (regression) ⇒ หยุด เก็บคอนโซลทั้งไฟล์ จดเวลา +07:00
    🔴 **ผลลบมีค่าเท่าผลบวก** — P2 ชี้ไปที่หน้าจอสร้าง · P3 ชี้ไปที่เส้นล็อกอิน/ไคลเอนต์ · P4 ชี้ไปที่เส้นล็อกอินเดิม
    คนละที่กันคนละใบกัน

- nonclaims: (อ่านก่อนอ้างผลใบนี้)
  1. 🔴 **สมมติฐาน "หน้าจอสร้างส่ง item id ของแถว preset มาโดยไม่แก้" ยืนยันแล้วกับคลาสเดียว** — Gladiator
     (`test01` ของ JOB-001) เท่านั้น ⇒ ถ้าการสร้างคลาสอื่นได้ `not_written`/NULL **นั่นไม่ใช่บั๊กของเซิร์ฟเวอร์
     แต่คือค่าวัดที่ใบนี้เปิดมาเพื่อเอา** ต้องรายงานพร้อมบรรทัดคอนโซลคำต่อคำ
  2. ตัวละครเก่าจะยังเป็น class 1 บนสายจนกว่า **backfill ของ LANE-DB** (`COO-DECISION 20260904_0445`) จะรัน —
     🔴 **ห้ามเกรดเป็น FAIL**
  3. ไม่พิสูจน์ว่า tag `0x19` ใน `CreateActorVital` คือ class id (`COO-DECISION 20260903_1943` ข้อ 3) — เส้นทางนี้
     ไม่อ่าน `actor_wire` เลย ใช้สามช่องของ AvatarAttr เทียบตาราง gamedata ที่คอมมิตแล้วเท่านั้น
  4. ไม่พิสูจน์อะไรกับ **เนื้อในหน้าต่างสกิล** หรือสกิลของคลาส (`GT-058`/`GT-059`/`RE-061`) · `K` เป็นข้อสังเกตล้วน
  5. ไม่พิสูจน์ว่า stats/HP/MP/โมเดลตัวละคร เปลี่ยนตามคลาส — ใบนี้วัด **คลาสที่ไคลเอนต์แสดง** อย่างเดียว
  6. ไม่พิสูจน์อะไรบน canonical — บูตบน **สำเนา** · ตัวละครที่เกิดในใบนี้ไม่มีในรอบถัดไป
  7. ไม่ตัดสินสาเหตุของสีป้ายชื่อใด ๆ (`RE-067`) · จดสีอย่างเดียว
  8. ไม่ใช่ใบตีมอน — 🔴 **ห้ามตี ห้ามคลิกมอนสเตอร์ ห้ามเข้าใกล้จนโดนตี** (`NOW.md` P-1/P-2 ยังไม่ปิด)

- links: `src/pirateforce_foundation/lifecycle.py` (`persist_class_id_from_starting_gear`) ·
  `session.py` (`_class_id_on_the_row` / `_class_id_console_line`) · `legacy_bridge.py` (class ขี่ character เข้า `ActorAttr`) ·
  `persistence_class_id.py` (`CLASS_PRESETS` ห้าแถว) · `tests/test_class_id_login_wiring.py` (ชั้น wire/DB ที่พิสูจน์แล้ว) ·
  `COO-DECISION 20260904_0446` ข้อ 2-3 (คำสั่งต่อสองจุดเสียบ) · `COO-DECISION 20260904_0445` (backfill ตัวเก่า) ·
  `PANYA-DECISION 20260904_0328` ข้อ 1 ("คลาสที่เลือกต้องไม่ถูกทิ้ง") · `PANYA-DECISION 20260828_0125` (ตัวละครสมประกอบ) ·
  `GT-215` (ท่าสร้างตัวละคร + วินัย db/teardown ที่ใบนี้ยืมมา) ·
  `notes_to_chief/FROM_CHIEF_R332_TO_ALL_20260904_0515.md` · `rounds/R332_3kwnnr_class-id-create-and-login-wiring.md`
- numbering: คำสั่งตัวนับร่วม (กฎ ② หัวไฟล์) คืน `225` ณ 2026-09-04T05:0x+07:00 ⇒ ใบนี้ `226` ·
  `GT-226`/`RE-226` = **0 hit** ทั้งสามที่ · ไม่มีการจองล่วงหน้า
- result: (ผู้รันกรอกแยกสองชั้น · ชั้นไหนไม่ได้วัดเขียน `NOT MEASURED` · บรรทัด `CHARACTER_CLASS_ID` และ
  `LOGIN_CLASS_ID` ทุกบรรทัดดิบ ๆ · ชื่อตัวละครและชื่อคลาสบนจอคำต่อคำ · บล็อก `BEFORE`/`AFTER` ·
  ภาพ `S0`-`S6` · บรรทัดสีป้ายครบทุกป้ายทุกภาพ · sha256 · branch/commit ที่บูต · timestamp +07:00 ·
  `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: chief (LANE-E) รอบ `3kwnnr` (R332) ตาม `COO-DECISION 20260904_0446` ข้อ 2-3 -- ผู้บริโภคผล: chief (LANE-E) ร่วม LANE-DB**


## GT-228 ISLAND-CONTACT-TRIGGER-FRAME-CAPTURE-001  [🟢 **PASS (กล่อง B) — ปิดโดย chief (LANE-E) รอบ `wjqykr`/R338 2026-09-04T14:0x+07:00**] ~~[OPEN --... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## GT-230 NPC-SHOP-SELL-SLOT-FRAME-CAPTURE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS ตามเกณฑ์ใบ (เก็บ hex ลากไอเทมลงช่องขาย 2 ครั้งซ้ำได้ NPC 'Chalais') — R320... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-233 M2-PROVISIONING-TRIAL-001  [🔴 **CLOSED — NEGATIVE-MEASURED-v3** — R322A 2026-09-06T18:57+07:00 (เงียบทั้งสองเกาะ แม้ `confirmed=126`, record 73 B ผ่าน parser, ระยะเข้าถึง ~50 หน่วย, key ชี้แถวจริงทั้ง `n_ID=1` และ `n_ID=126`) · ผลเต็ม `notes_to_chief/20260906_1909_KA1A-R322A-RESULTS-*.md` (`OBSERVER_CONFIRMED 2026-09-06T18:57+07:00`) · ปิดตาม `PANYA-ORDER 20260906_1910` ข้อ 2.1 (ห้ามบูต v4 ซ้ำ · ห้ามตั้งใบ trial `AddSurveyData` ใหม่) ยืนยันโดย `COO-DECISION 20260906_1955` ข้อ 1 · M2 ไปทาง (ก) ต่อ: เซิร์ฟต้องตอบ `TriggerVital 0x1FB2` trigger 2/3 เอง (งานของ LANE-A/LANE-UI RE static ก่อน ไม่ใช้เครื่องเจ้าของจนมีเฟรมผู้สมัคร) · พับโดย LANE-K รอบ `cu7c2r` 2026-09-06T20:11+07:00 · เดิม: 🟢 **READY-v3 -- บูตได้ทันที (เงื่อนไข "รอ merge ก่อน" จ่ายแล้ว)** — `#865` (`ef843ed`) + `#857` อยู่บน `main` จริง · พลิกหัวโดย chief (LANE-E) รอบ `6z131u`/R362 · **อำนาจพลิก = `COO-DECISION 20260905_1949` ข้อ 1 + `20260905_2349` ข้อ 4-5** (`0147` ข้อ 2 เป็นลำดับงาน ไม่ใช่คำอนุญาต — แก้การอ้างของตัวเองรอบ `6z131u`-b ตาม pf-adversary) (หลักฐานที่ chief วัดเองรอบนี้ อยู่ในบล็อก `ATTENDED:` ด้านล่าง) · v3 ทับ v2 โดย LANE-A รอบ `dio9ll` ตาม `COO-DECISION 20260905_2349` ข้อ 1-2 (ดูบล็อกควตด้านล่าง) · พลิกจาก `BLOCKED-ON-RE` โดย chief (LANE-E) รอบ `rz1fxh`/R358 ตาม `COO-DECISION 20260905_1949` ข้อ 1 · **chief เลือกทางพลิกใบเดิม ไม่ตั้งเลข GT ใหม่** เพราะประวัติ M2 ทั้งหมดอยู่ในใบนี้ และ `GT-267` ถือสาขาข้ามขอบทะเลไปแล้ว -- **ถึง LANE-A: ร่าง GT ที่ `1947` ข้อ 3 สั่ง ให้เขียนลงใบนี้ (v2) อย่าขอเลขใหม่** · 🔴 **เกณฑ์ v2 เปลี่ยนแล้ว** (`RE-265` ปิด BOUNDED-NEGATIVE `notes_to_chief/20260905_1932_*`): ตัวบล็อกไม่ใช่ parser และไม่ใช่ระยะ -- record `+0x14` ต้องเป็น key ที่ lookup ตาราง `SAILING_RESULT` แล้ว**คืนแถวจริง** row ว่าง = client ออกก่อนเกตระยะ ⇒ เฟรมเดิมที่ใส่แค่ `record+0x12=2/3` **ห้าม retry** · เกณฑ์ผ่าน v2/v3 = `Common_Confirm` เด้งบนจอ + ผู้เล่นกดยืนยัน + client ยิง `EnterInstanceVital` **เอง** (เซิร์ฟเวอร์ห้ามส่งให้) · **ห้ามเลือกแถว `SAILING_RESULT` จากเลขที่เท่ากัน** (nonclaim 2 ของผล `1932`) · ป้ายเดิมที่ยังจริงและไม่ลบ: **NEGATIVE-MEASURED (พิกัดหลัก) R318 2026-09-05T13:19+07:00** -- แก้หัวโดย chief (LANE-E) รอบ `r045nx`/R354 ตาม `COO-DECISION 20260905_1349` ข้อ 1 (ผล `notes_to_chief/20260905_1319_KA1A-R318-RESULTS-*.md` · `OBSERVER_CONFIRMED 2026-09-05T12:48+07:00`)** -- moved to `tickets/GT-233.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `cu7c2r` 2026-09-06T20:11+07:00)

## GT-242 BACKPACK-OPEN-DOES-NOT-WIPE-THE-GROUND-001  [✅ **ปิดใบ: PASS สองชั้น (เว้น item(4) NO-RESULT) ตาม `R316` 2026-09-05T11:02+07:00** — ยืนยันโดย `COO-DECISION 20260906_1452` (R321 ด้านล่างในบล็อกประวัติ = ความพยายามวัดซ้ำหลัง PASS ไม่ใช่ผลใหม่) · พับปิด+archive โดย LANE-K รอบ `rsmsia` 2026-09-06T15:09+07:00 -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)]
---

## GT-243 HOTBAR-SKILL-99-VS-WIELD-Z-SAME-SESSION-HEX-DIFF-001  [~~PENDING -- P0~~ 🔵 BLOCKED-ON-PRECONDITION — ปิดโดย LANE-CS รอบ `88ej1z` (ผล `0155` §GT-243) · ต่อ `RE-271` · เจ้าของใบ = **LANE-CS**]

> 🔢 **เลขใบตั้งโดย LANE-CS 2026-09-04T~17:2x+07:00** ตามข้อกำหนดส่งต่อในบรรทัดปิดใบของ `RE-240` (`DONE/BOUNDED-NEGATIVE`, ปิดโดย LANE-CS เอง `notes_to_chief/20260904_1714_RE-240-RESULT-HOTBAR-DISPATCH-EXITS-NO-PRODUCER.md`): "bounded-negative: เดินครบแล้วชนเพดาน ... ระบุเพดานให้ชัด แล้วส่งต่อเป็นใบ attended capture (กด skill 99 จากฮอตบาร์ + control กด Z ในเซสชันเดียวกัน ต้องได้ hex ตระกูล V128 เดิม)" · ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน `242` (`GT-242`) ⇒ ใบนี้ `243` · `GT-243`/`RE-243` = **0 hit ทั้งสามที่ก่อนวาง** (ตรวจแล้วโดย LANE-CS ก่อนร่างใบนี้)
> 🔴 ใบนี้เป็น **ใบ "เก็บ hex แล้วเทียบ" — ไม่ใช่ใบตัดสินว่าฟิลด์ใดคือ skill ID** ผลบวก (พบไบต์ต่าง) ให้ผลเป็น **candidate เท่านั้น** ต้องมีใบ static แยกอีกชั้นผูก offset นั้นเข้ากับ "วัตถุสกิลที่ผู้เล่นเลือกจริง" ก่อนใครจะตั้งชื่อ definitive (คำเตือนนี้มาจาก `RE-240` เอง ไม่ใช่ข้อสรุปใหม่ของใบนี้)

## ที่มา (อ่านตรงนี้พอ ไม่ต้องเปิดใบ RE-240 ซ้ำ)
`RE-240` เดิน static ครบแล้วว่า dispatcher `0x450B20` ผ่านตาราง class `0x4519C4` ไปยัง jump table `0x451970` — **ทุกแถวที่ตั้งชื่อของ hotbar/skillbar** (`TOOLBAR1-3_01..12` = HOTKEY id `12..47` และ `SKILLBAR1..10` = HOTKEY id `111..120`, ทั้ง 46 แถว `n_TYPE=2`) แปลงเป็น **class 20 เหมือนกันหมด** และ jump slot ของ class 20 ชี้ไปที่ `0x4518F3` ซึ่งเป็น epilogue เปล่า (`xor eax,eax` แล้ว return) — **ไม่มี call, ไม่มี allocation, ไม่มี object-field write, ไม่มี queue send**. เพดาน static คือจุดนี้: ไม่ว่าผู้เล่นวางสกิลอะไรลงช่องไหนของ hotbar/skillbar ก็เดินผ่านเส้นเดียวกันนี้ทั้งหมด (skill id ไม่ใช่ตัวกำหนด HOTKEY id — HOTKEY id มาจาก "ช่อง" ที่วาง ไม่ใช่จาก "สกิลที่วางอยู่ในช่อง") ⇒ ผลลบของ `RE-240` ครอบคลุมสกิล 99 ด้วยไม่ว่าจะวางลงช่องไหน **ถ้าวางลงช่องที่ตั้งชื่อสองชุดนี้**
Control ที่ผ่านแล้วในรอบเดียวกัน (`RE-240`): HOTKEY `71` (`WIELD`, คีย์ `Z`) → class `11` → branch `0x451026` → producer `0x0044BC70` ซึ่ง hardcode `0xEA7E` ลง object field `+0x30` ของเฟรมตระกูล `ActionVital` (serializer `0x0074E6A0`) แล้ว queue ส่งจริง — ตรงกับ `pirate-force-server/reports/PF_RE_V128_Wield_Z_ActionVital_Capture_20260814.md:25-33,47-60` ทุกจุด นี่คือ **เฟรมอ้างอิงตระกูล V128** ที่ใบนี้ใช้เทียบ
🔴 **สิ่งที่ static ยังตอบไม่ได้และเป็นเหตุผลทั้งหมดที่ใบนี้ต้องมีคนหน้าจอ**: `RE-240` เป็นผลลบแบบ bounded เฉพาะเส้นทาง dispatcher `0x450B20`/ตาราง `0x4519C4` เท่านั้น — **ไม่ใช่ข้อพิสูจน์ว่าไคลเอนต์ไม่เคยส่งเฟรมสกิลจาก UI callback เส้นอื่น** (เช่น onClick handler ของแผงสกิลที่ไม่ผ่าน HOTKEY dispatch เลย) มีทางเดียวที่จะตอบคำถามนั้นคือฟังสายจริงตอนคนกด

## ตีความคำว่า "ต้องได้ hex ตระกูล V128 เดิม" (บันทึกไว้ตรง ๆ กันเข้าใจผิด)
ถ้อยคำปิดใบของ `RE-240` ไม่ได้บอกว่า **คาดว่า** เฟรมสกิล 99 จะตรงตระกูล V128 — ใบนี้อ่านว่าเป็น **ข้อกำหนดเรื่องรูปแบบการเก็บหลักฐาน**: ทั้งสองการกด (A = สกิล 99, B = control WIELD/Z) ต้องถูกจับเป็น **decompressed RuntimeReq hex ด้วยวิธีเดียวกับที่ `PF_RE_V128_Wield_Z_ActionVital_Capture_20260814.md` ใช้จับ** เพื่อให้เทียบไบต์ต่อไบต์ ณ ตำแหน่งเดียวกันได้จริง ไม่ใช่คำทำนายว่าผลจะออกมาตรงกัน — ผลจะตรงตระกูลหรือไม่ตรงคือสิ่งที่ใบนี้วัด ไม่ใช่สิ่งที่ใบนี้สันนิษฐานไว้ก่อน

## PRECONDITION (เช็คจริงก่อนขั้น 1 ไม่ใช่หมายเหตุ)
P0. **ตัวละครเทสต้องมีสกิลหมายเลข 99 เรียนแล้วและวางอยู่ในช่อง hotbar/skillbar ที่ตั้งชื่อ** (`TOOLBAR1-3_xx` หรือ `SKILLBAR1..10`) ก่อนบูตรอบจริง — ใบนี้ **ไม่มีอำนาจสั่งว่าสกิล 99 คืออะไร** (`RE-240` ปักไว้แล้วว่า `BEHAVIOR.n_ID=99` กับ `SKILL_CONTEXT.n_ID=99` ไม่มี crosswalk — เลข "99" ที่ปรากฏบนปุ่ม UI คือค่าที่ต้องยืนยันจากจอจริง ไม่ใช่จากตาราง) ผู้เตรียมตัวละคร (LANE-CS หรือ GM) ต้องยืนยันและบันทึกไว้ในผลว่าใช้วิธีใดทำให้สกิลนี้มาอยู่บนแผง ก่อนเรียกผู้เทส
    ไม่มีสกิล 99 ให้วางจริง ⇒ **อย่าบูต** เขียนกลับเป็น `BLOCKED-ON-PRECONDITION` พร้อมเหตุผล ไม่ใช่ `NO-RESULT`
P1. เซิร์ฟเวอร์ก่อนไคลเอนต์เสมอ · ไคลเอนต์ที่เปิดทิ้งไว้โดยไม่มีเซิร์ฟเวอร์ตายเองใน ~3.5 นาที
P2. ฆ่าไคลเอนต์แล้ว **เซิร์ฟเวอร์ยังถือเซสชันไว้** — รีสตาร์ตเซิร์ฟเวอร์ก่อนเปิดไคลเอนต์ตัวถัดไปเสมอ ไม่งั้นค้าง "connecting" ตลอดกาล
P3. รอบคัดลอก DB ⇒ ตำแหน่งตัวละครกลับไปจุดเกิดทุกบูต เป็นเรื่องปกติ ไม่ใช่ผลวัด
P4. teardown ปฏิเสธ boot stamp เก่ากว่า 420 นาที (ยกจาก 180 เมื่อ 2026-08-20, `TEMPLATE_teardown_generic.ps1:135`) — ต้องรัน teardown เสมอแม้รอบจบเพราะเลิกเล่นกลางคัน

## db
`state\pirateforce.sqlite3` (canonical) — **ห้ามเปิดไฟล์ canonical เด็ดขาด**: คัดลอกเป็น `state\run_gt243_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนาเท่านั้น
จด sha256 ของสำเนาก่อน/หลัง · จด sha256 ของ canonical ก่อน/หลัง ยืนยันว่า **ไม่เปลี่ยน** · `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง

## server args
บูตมาตรฐาน · **ไม่มีแฟล็ก scenario ใด ๆ** (ใบนี้ไม่ต้องการ hypothesis lane — ฟังสายเปล่า ๆ พอ) · เก็บคอนโซล **รวม stdout+stderr (`2>&1`)**
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt243_<stamp>.sqlite3 2>&1
```
ต้องมีตัวจับแพ็กเก็ตเปิดอยู่ตลอดใบ: `capture_v141\GAME_LIVE.txt` (hex ดิบ) และ `capture_v141\GAME_EVENTS_LIVE.txt`

## steps (คลิกตามลำดับ · จดเวลานาฬิกา `HH:MM:SS+07:00` ทุกครั้งที่เขียนว่า "จดเวลา" — ใช้ตัดหน้าต่าง hex ทีหลัง)
1. PRECONDITION P0-P4 ผ่านก่อน · `LOCK_GAME` · จด boot stamp · sha canonical · คัดลอก DB เป็น run copy
2. บูตเซิร์ฟเวอร์ใหม่สด → เปิดตัวจับแพ็กเก็ต → บูตไคลเอนต์ → ล็อกอิน → รอโหลดจบ → ภาพนิ่ง `S00-HOME` เต็มความละเอียด
3. 🔴 **ยืนยันว่าช่องแชทไม่ focus ก่อนกดคีย์ใด ๆ** (ตัวอักษร/คีย์ที่พิมพ์ตอนแชทไม่ focus กลายเป็นฮอตคีย์ของเกม — ในใบนี้ **นี่คือพฤติกรรมที่ต้องการ** เพราะทั้ง WIELD และการกดสกิลต้องเป็นฮอตคีย์จริง ไม่ใช่ข้อความแชท — แค่ต้องแน่ใจว่าไม่มีการพิมพ์อื่นแทรกโดยไม่ตั้งใจ)
4. **BASELINE/CONTROL รอบที่ 1**: กด `Z` (WIELD, HOTKEY id 71) · **จดเวลา** T_B1 · ภาพนิ่ง `S-CTRL-1`
5. รอ ~5 วิ แล้ว **BASELINE/CONTROL รอบที่ 2** (ทำซ้ำเพื่อพิสูจน์ทำซ้ำได้): กด `Z` อีกครั้ง · **จดเวลา** T_B2 · ภาพนิ่ง `S-CTRL-2`
6. รอ ~5 วิ แล้ว **สกิล 99 รอบที่ 1**: คลิกเมาส์ลงช่อง hotbar/skillbar ที่วางสกิล 99 ไว้ (P0) · **จดเวลา** T_A1 · ภาพนิ่ง `S-SKILL99-1` (เก็บทั้งแผงและตัวละครในเฟรมเดียว)
7. รอ ~5 วิ แล้ว **สกิล 99 รอบที่ 2** (ทำซ้ำ): คลิกช่องเดิมอีกครั้ง · **จดเวลา** T_A2 · ภาพนิ่ง `S-SKILL99-2`
8. NO-CRASH ตอนจบ: **คลิกขวาลากหมุนกล้องอย่างเดียว** (หมุนกล้องล้วน ตัวละครไม่หัน ไม่มีไบต์ออกสาย ปลอดภัยทุกจังหวะ) 🔴 **ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้** — มันหมุนตัวละครจริงและยิง `TargetPosVital` · ออกด้วยปุ่ม X
9. ปิดเซิร์ฟเวอร์ · เก็บ `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **รัน teardown เสมอ** · ห้าม commit เอง
🔴 **STOP**: ไคลเอนต์ปิดตัว/ค้างเมื่อไหร่ หยุดทันที บันทึกเป็นผลการวัด ไม่ใช่รอบเสีย — รายงานว่าหยุดตรงขั้นไหน แล้วยังต้องรัน teardown

## pass criteria (สองชั้น — 🔴 ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด)

**wire/DB** (headless พิสูจน์ได้จาก `GAME_LIVE.txt`/console — ไม่ต้องมีตาคน):
1. ตัด hex ดิบหน้าต่าง +/- 5 วินาที รอบเวลาที่จดไว้ทั้งสี่จังหวะ (T_B1, T_B2, T_A1, T_A2) **ทุก opcode ไม่กรองอะไรทิ้ง** พร้อม index เฟรม + จำนวนไบต์ต่อเฟรม
2. T_B1/T_B2 (control): เฟรมที่จับได้ต้อง **มี** เฟรมตระกูล `ActionVital`/`0x1AEA` ที่ `+0x30 = 0xEA7E` (ตรงกับ `PF_RE_V128_Wield_Z_ActionVital_Capture_20260814.md:25-33,47-60`) — **ไม่ตรง = control พัง หยุดตีความ T_A ต่อ รายงานเป็นผลของใบนี้แล้วส่งกลับ ไม่ใช่ผู้เทสแก้เอง**
3. T_A1/T_A2 (สกิล 99): บันทึกดิบทุกเฟรมที่อยู่ในหน้าต่างนั้นไม่ว่าจะมีหรือไม่มี — นี่คือข้อมูลหลักที่ใบนี้เก็บ
4. `integrity_check` = `ok` ทั้งสองครั้ง · sha256 canonical ไม่เปลี่ยน · ไม่มี traceback หลุด
5. 🔴 **ชั้นนี้ตอบไม่ได้ว่าบนจอผู้เล่นเห็นอะไรตอนกดสกิล 99**

**client-observable** (ต้องมีตาคน — ห้ามอนุมานจากคอนโซล):
6. ตอนกดสกิล 99 แต่ละครั้ง จอเป็นอย่างไร — เขียนตรง ๆ: ไอคอนช่องกะพริบ/ตัวละครมีแอนิเมชัน/ข้อความปฏิเสธ (คัดตามตัวอักษร)/ไม่มีอะไรเลย
7. บันทึกสีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อป้ายต่อภาพ ครบทุกภาพ (`S00-HOME`, `S-CTRL-1/2`, `S-SKILL99-1/2`) — เขียน `none` แทนการเว้นว่าง อ่านจากภาพนิ่งเต็มความละเอียดเท่านั้น ห้ามอนุมานสาเหตุของสี (`RE-067` เป็นเจ้าของคำถามนั้น) — ความต่างจากภาพเซิร์ฟเวอร์จริงลง `REAL_SERVER_DIVERGENCE.tsv`
8. 🔴 **ชั้นนี้ตอบไม่ได้เลยว่าไบต์ใดออกจากไคลเอนต์**
🔴 ปิดใบด้วย `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` เท่านั้น (G-OBS) · หลักฐานครบแต่ไม่มีลายเซ็นคน = `AWAITING-OBSERVER` ไม่ใช่ PASS ไม่ใช่ FAIL

## กล่องผลลัพธ์ (ผู้เทสไม่ต้องตัดสินสมมุติฐาน แค่เลือกกล่องแล้วรายงาน — ผลลบมีค่าเท่าผลบวก)
A. **T_A1/T_A2 ไม่มีเฟรมใดออกเลยในหน้าต่าง +/-5 วิ ทั้งสองรอบ** ⇒ ผลลบที่สอดคล้องกับเพดาน static ของ `RE-240` (เส้นทาง class 20 จบที่ epilogue เปล่าจริงตามที่วัด) → redirect: ปิดคำถามฝั่ง HOTKEY dispatch ได้แน่นขึ้น หัวข้อ "มีเฟรมสกิลจาก UI เส้นอื่นไหม" ยังเปิดอยู่ ไม่ใช่ปิดโดยกล่องนี้
B. **มีเฟรมออกที่ T_A1/T_A2 และเฟรมนั้นตรงตระกูล/ขนาด/ทรงเดียวกับ `ActionVital` ของ control (T_B) แต่ byte-identical นอกฟิลด์ที่รู้อยู่แล้วว่าแปรผัน** (เช่น sequence/timestamp) ⇒ **NO-CANDIDATE** — ตระกูลตรงแต่ไม่มีไบต์ไหนแยกสกิล 99 ออกจาก WIELD ได้ นี่คือผลลบที่มีค่า ชี้ว่า field ตัวเลือกสกิลไม่อยู่ในเฟรมนี้ (หรือค่ามันบังเอิญเท่ากัน — เขียนทั้งสองทางที่เป็นไปได้)
C. **มีเฟรมออกที่ T_A1/T_A2 ตรงตระกูล `ActionVital` แต่มีไบต์ต่างจาก T_B ที่ offset คงที่ (ซ้ำกันทั้ง T_A1 และ T_A2)** ⇒ **CANDIDATE พบ** — จดไบต์/offset ที่ต่างให้ครบ 🔴 **ห้ามตั้งชื่อว่านี่คือ skill-id field** เขียนเป็น "candidate offset X ต้องมีใบ static แยกผูกกับวัตถุสกิลที่เลือกก่อน" แล้วส่งต่อเป็นใบ RE ใหม่
D. **มีเฟรมออกที่ T_A1/T_A2 แต่ไม่ตรงตระกูล/ทรง/ขนาดกับ `ActionVital` เลย** (opcode อื่น/serializer อื่น) ⇒ ผลบวกที่ต่างจากที่ RE-240 ปิดไว้ — จดเฟรมดิบทั้งหมด ส่งต่อเป็นใบ static ใหม่ไล่ producer ของ opcode นั้น (คนละคำถามจาก `RE-240`)
E. **ไคลเอนต์ตาย/ตัวจับแพ็กเก็ตไม่เขียนไฟล์/ล็อกอินไม่ได้เพราะสกิล 99 ไม่มีจริง** ⇒ `NO-RESULT` พร้อมเหตุผลหนึ่งบรรทัด ห้ามเดาแทนไบต์ที่ไม่มี

## ห้ามสรุปสิ่งเหล่านี้ (กติกาหลักฐาน)
- 🔴 **ห้ามใช้ไบต์ที่ต่างกันหนึ่งตำแหน่ง (กล่อง C) เป็นข้อพิสูจน์ว่าพบ skill-id field แล้ว** — ใบนี้ให้ได้แค่ candidate ต้องมีหลักฐานคนละชั้นผูก offset นั้นกับ "วัตถุสกิลที่ผู้เล่นเลือก" ก่อน (คำเตือนสืบมาจาก `RE-240`)
- 🔴 **ห้ามเชื่อม `BEHAVIOR.n_ID=99` กับ `SKILL_CONTEXT.n_ID=99`** — ตัวเลขตรงกันไม่มี crosswalk (G6 rule, ยืนตาม `RE-240`) เลข "99" ในใบนี้อ้างอิงจากสิ่งที่ปรากฏบนปุ่ม UI จริงเท่านั้น
- 🔴 **ห้ามอ้างว่ากล่อง A พิสูจน์ว่าไคลเอนต์ไม่เคยส่งเฟรมสกิลเลย** — พิสูจน์ได้แค่ว่าเส้นทาง HOTKEY dispatch `0x450B20` (ตามที่ `RE-240` เดิน) ไม่ส่ง ยังมีเส้นทาง UI callback อื่นที่ยังไม่ถูกตรวจ
- 🔴 **ห้ามอ้างว่า `ActionVital+0x30` คือ skill ID** — `RE-110` แยกมันเป็น action/behavior selector แล้ว ไม่เปลี่ยนแปลงโดยใบนี้
- 🔴 **ห้ามอ้างว่า `TriggerCastSkillVital` (`0x00600A60`) เป็นหรือไม่เป็นเฟรมของการร่ายสกิล** — ใบนี้ฟังสายจริงเฉพาะเหตุการณ์กดสกิล 99 เท่านั้น ไม่ได้พิสูจน์ทิศทางของ serializer นั้น (คำถามเดิมของ `RE-056`/`GT-050` job 4 ยังไม่ถูกแตะโดยใบนี้)
- 🔴 ไม่ตัดสินสาเหตุของสีป้ายชื่อใด ๆ (`RE-067`) — จดสีอย่างเดียว

## nonclaims
1. ไม่พิสูจน์ผลของสกิล 99 ในเกม (แอนิเมชัน/ดาเมจ/คูลดาวน์) — วัดเฉพาะไบต์ขาออกและสิ่งที่เห็นบนจอ ณ จังหวะกด
2. ไม่พิสูจน์ว่าช่อง/สกิลอื่นนอกจาก "สกิล 99" จะให้ผลเดียวกัน (`PER-CLASS` — ห้ามเหมาไปใช้กับสกิลอื่น)
3. ไม่พิสูจน์อะไรบน canonical DB (บูตบนสำเนาเท่านั้น) และไม่พิสูจน์อะไรที่ต้องรอดข้าม relog
4. ไม่ปิด/ไม่กลับคำ `RE-240` — เป็นชั้นหลักฐานเพิ่ม (attended) ต่อจากชั้น static ที่ `RE-240` ปิดไปแล้ว
5. ไม่ตัดสินสาเหตุของสีป้ายชื่อ (`RE-067`)
6. กล่อง C (ถ้าเกิด) ไม่ใช่การปิดคำถาม skill-id — เป็นจุดเปิดใบ static ใหม่เท่านั้น

## links
`notes_to_chief/20260904_1714_RE-240-RESULT-HOTBAR-DISPATCH-EXITS-NO-PRODUCER.md` (ที่มาทั้งใบ) ·
`CLIENT_RE_QUEUE.md` บล็อก `RE-240` (คำถามเดิม + control WIELD) ·
`pirate-force-server/reports/PF_RE_V128_Wield_Z_ActionVital_Capture_20260814.md:25-33,47-60` (เฟรมอ้างอิงตระกูล V128) ·
`external/PF_SERIALIZER_FIELDS.tsv` (schema `ActionVital`/`TriggerCastSkillVital`) ·
`RE-110` (ปิดแล้ว — `+0x30` = action/behavior selector ไม่ใช่ skill id) ·
`RE-232` (ปิดแล้ว — grammar ของ `s_CAST_CONDITION`/`s_CAST_BEHAVIOR`, คนละคำถาม) ·
`RE-056`/`GT-050` job 4 (ทิศทาง `TriggerCastSkillVital` ยัง UNRESOLVED — ใบนี้ไม่แตะ) ·
`BRIDGE_BOOT_PROCEDURE.md` + `ATTENDED_SESSION_RUNBOOK.md` + `TEMPLATE_teardown_generic.ps1`

## numbering
ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน `242` (`GT-242`) ⇒ ใบนี้ `243` · `GT-243`/`RE-243` = 0 hit ทั้งสามที่ก่อนวาง (ตรวจแล้วโดย LANE-CS)

## result
(ผู้เทสกรอก: กล่อง A/B/C/D/E · hex ดิบทั้งสี่หน้าต่าง (T_B1/T_B2/T_A1/T_A2) พร้อม index เฟรม+ขนาด · offset/ไบต์ที่ต่าง (ถ้ามี, กล่อง C/D) · เวลา `HH:MM:SS+07:00` ทั้งสี่จังหวะ · ภาพ `S00-HOME`/`S-CTRL-1`/`S-CTRL-2`/`S-SKILL99-1`/`S-SKILL99-2` เต็มความละเอียด · บรรทัดสีป้ายครบทุกป้ายทุกภาพ · sha256 ทุกไฟล์ · `integrity_check` สองครั้ง · sha canonical ก่อน/หลัง · branch/commit ที่บูต · วิธีที่ทำให้สกิล 99 มาอยู่บนแผง (P0) · `OBSERVER_CONFIRMED: <ISO+07:00>`)

**ผู้เปิดใบ: LANE-CS ตามข้อกำหนดส่งต่อของ RE-240 (DONE/BOUNDED-NEGATIVE, ปิดโดย LANE-CS เอง 2026-09-04T17:14+07:00) -- ผู้บริโภคผล: LANE-CS**

---

## GT-244 LIVE-WARP-SCENE-PERSISTS-ACROSS-LOGIN-001  [🚫 CLOSED -- CANCELLED - covered by 20260904_1911 R310 ข้อ 3 -- ยกเลิกโดย chief รอบ `t7bsfx`/R342 ตาม `COO-DECISION 20260904_1948` ข้อ 2 -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-245 CHARACTER-SELECT-SCREEN-SHOWS-THE-REAL-SCENE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — ครึ่งหลัง PASS — R317 2026-09-05 §1: หลัง /warp 1 (persist R316) → relaunch... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-246 AUTO-WALK-CLICK-DIFFERENTIAL-001  [ANSWERED -- วัดครบแล้วในรอบ attended R310 (2026-09-04 18:45-19:07 +07:00) ตั้งแต่ก่อนใบนี้มีเลข -- ห้ามบู... -- archived 20260907 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md`, LANE-K round `kxpzxi`)

## GT-247 ATTACK-POSE-ONE-FIELD-AB-001  [🟢 **PASS -- R315 2026-09-05 10:11-10:2x** · `OBSERVER_CONFIRMED 2026-09-05T10:24+07:00` · ปิดหัวโดย chief (LA... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## numbering
ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `246` (`GT-246`) => ใบนี้ `247`
`GT-247`/`RE-247` = 0 hit ทั้งสามที่ก่อนวาง (ตรวจโดย chief รอบ `epkucn`/R344)

---

## GT-249 LEARN-SKILL-RESULT-REAL-KIT-CONTENT-001  [🔧 LANE-K พับผล รอบ `slug54r2` 2026-09-06T13:40+07:00 — **PASS-PARTIAL (กล่อง P4)** — ใบนี้รันจริงไปแล้วตั้งแต่ 2026-09-05 01:53 (R312) แต่ค้างไม่ถูกเกรดในคิว >30 ชม. (pf-adversary จับได้จากรอบ `slug54` ที่ยังไม่มีใครพับ): เฟรม `0x673C` ใส่ id จริง (111/40000/99/110) ทำให้แท็บ "พิเศษ" ของหน้าต่างสกิลขึ้น 3/4 รายการ (Normal Attack/Strive Jump/VIP Strive Jump ชื่อ+ไอคอนถูก · id 40000 ไม่ขึ้น) · `OBSERVER_CONFIRMED 2026-09-05T01:26+07:00` · 🔴 ของแถมสำคัญ: หลังรับชุด 6 เฟรม client เดินไม่ได้เลยจนกว่าจะ relog (ไม่รู้เฟรมไหนเป็นตัวล็อก — แยกใบใหม่ `GT-276` ให้ LANE-CS ไล่แล้ว) · จาก notes_to_chief/20260905_0153_KA1A-R312-RESULTS-*.md (ต้นฉบับ) + notes_to_chief/20260906_1252_LANE-CS-TO-CHIEF-gt249-grade-plus-walklock-isolate-ticket.md (คำขอเกรด ข้อ 1 — LANE-CS เสนอเกรดเดียวกันนี้ ไม่ได้ตัดสินเอง LANE-K แค่พับตามที่ผู้เทส+ผู้บริโภคผลเสนอตรงกัน) · เดิม: 🟢 **READY** -- เนื้อใบเต็มคัดลอกจาก LANE-CS's `pf-queue-author` draft (`notes_to_chief/20260904_2256_LANE-CS-TO-CHIEF-gt-draft-real-skill-id-frame-plus-server-pr.md` / `rounds/CS_20260904_2256_30kpco_...md` §2) โดย chief (LANE-E) รอบ `zwxuuk` ตาม `COO-DECISION 20260905_0044` (หนี้ค้างตั้งแต่ 22:56 ที่ยังไม่ถูกคัดลง) · เลขใบตั้งโดย chief รอบ `epkucn`/R344 · **พ่วงบูตเดียวกับ `GT-243`** แต่**ไม่ใช่ boot เดียวกัน** (ดู BOOT ORDER ด้านล่าง — คนละ server args คนละ flag) · **เจ้าของใบ/ผู้บริโภคผล = LANE-CS** · ผู้รัน = Panya (attended) · ไม่บล็อกใคร · กำหนด **02:21** (`COO-DECISION 20260905_0044`)]

owner/consumer of result = LANE-CS -- runs attended, piggybacked in the same attended appointment as GT-243
(same class_id=1/level=1 character, saves a second scheduled sitting) -- NOT the same server process as
GT-243 (see BOOT ORDER note, GT-243's own server args explicitly forbid any `--*-scenario` flag)

ATTENDED: บูต `--learn-skill-result-hypothesis-scenario ...learn_sweep.json` (คนละบูตกับ GT-243) Gladiator lv1 กด K ถ่ายภาพ baseline (S-BASE-K)
ATTENDED: focus แชท พิมพ์ `SKILLCONTENT` (12 ตัว) Enter ดึง focus ออก รอ >=20s กด K ถ่ายภาพ (S-FINAL-K)
ATTENDED: ผ่าน = S-FINAL-K มี 4 รายการ: VIP Strive Jump/Gladiator Basic Training/Normal Attack/Strive Jump
ATTENDED: ไม่ผ่าน = 0 รายการ/ไม่ตรงชื่อแม้เฟรม 6 ออกสะอาดแล้ว = finding ไม่ใช่ FAIL (ปิดคำถามเปิดในโมดูลรอบเดียวกัน P3)
ATTENDED: gate 0/1/2 ผ่านก่อนบูต ห้ามเดา SHA

> NUMBERING NOTE: `GT-249`/`RE-249` = 0 hit ก่อนวาง (chief `epkucn`/R344) -- ไม่ reopen/supersede `GT-058`/
> `GT-059`/`GT-064`/`GT-116`/`GT-243` (คำถามคนละอัน) เปิดตาม `COO-DECISION 20260904_2154` ตอบจดหมาย
> `notes_to_chief/20260904_2113_LANE-CS-TO-COO-backup-item1-read-plus-gt116-reopens-skill-window-content-question.md`

### source (links only)
- `notes_to_chief/20260904_2154_COO-DECISION-skill-window-content-gt-approved-piggyback-gt243-LANE-CS.md` --
  the approval: send 0x673C with REAL skill ids from class_id=1's own starting kit (not probe values) to a
  character satisfying GT-116's precondition; PASS = skill window (K) populates with exactly the 4 starting
  skills; attended-only, production_allowed stays False; STOP if client closes; a refuting result
  closes/rewords the parent module's open question same round (PANYA-DECISION 20260903_1934).
- `rounds/CS_20260904_2113_fv5xnu_backup-item1-read-plus-gt116-reopens-skill-window-content.md` -- reopened
  this: GT-058/GT-059/GT-064 (archived CLOSED) never answered "does the window's CONTENT track anything the
  server sends" (window never opened in those sessions, class always 0). GT-116 removed that blocker
  2026-08-28 but itself says "[no claim] the skill list is a correct Gladiator kit -- not yet measured".
- GT-116 (`GAME_TEST_QUEUE.md:5183`, CLOSED PASS 2026-08-28): window opens for class_id=1/level=1, 0 entries
  at level 1 is normal -- this entry's precondition IS that proven precondition. class_id=1 is wired into
  every flagless production login (CORE-REQUEST-022) -- no special build needed beyond what GT-243 needs.
- `src/pirateforce_foundation/learn_skill_result_hypothesis.py` (HYP-PF-033, vital 0x673C) -- the module this
  entry exercises. Its own docstring nonclaims (read before using anything from it): the three record member
  positions (record_u32_0 / record_u16_4 / record_u32_8) have UNKNOWN semantics, the trailing u8 has UNKNOWN
  semantics, production_allowed=False, database_write=none. The module's own `[UPDATE, round fv5xnu's
  finding + COO-DECISION 20260904_2154]` paragraph names the sixth sweep step this entry fires:
  `COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0`, sending 4 records, each repeating one of
  `class_catalog.starting_skill_ids(1)`'s 4 ids (111 "VIP Strive Jump", 40000 "Gladiator Basic Training", 99
  "Normal Attack", 110 "Strive Jump", in that order) in all three wire positions of its own record, trailing
  byte 0 -- because the position that means "skill id", if any, is unproven, this removes the need to guess
  which field the client reads before judging the on-screen result.
- The other five steps of the same sweep (COUNT0_TRAIL0, COUNT1_TRAIL0, COUNT1_TRAIL1, COUNT3_TRAIL0,
  COUNT3_TRAIL1) are UNCHANGED, pre-existing, and send arbitrary tellable-apart probe values (not real game
  data) -- this entry's own claim is about the 6th frame only; anything the first five frames visibly do is
  noted as a secondary observation, not this entry's pass/fail measure.

### objective (single claim)
Sent to the SAME class_id=1/level=1 character GT-116 already proved opens the skill window (K /
Bt_main_Skill), does the LAST frame of the HYP-PF-033 sweep -- the one whose 4 records carry class_id=1's own
real starting-kit skill ids (111, 40000, 99, 110) -- make that window populate with entries a human can
recognize as those 4 skills (VIP Strive Jump, Gladiator Basic Training, Normal Attack, Strive Jump), by
whatever names/icons the client actually shows? This is the FIRST attended measurement of whether anything
HYP-PF-033 sends is rendered as content at all, as opposed to merely accepted on the wire without visible
effect (which is all GT-050's static work and this module's own unit tests can ever show).

### predictions (a wrong prediction is a finding, not a failure)
- P1 [proposed, the heart of the entry]: after the full 6-frame sweep completes, the skill window shows
  exactly 4 entries, one per real starting-kit skill id, recognizable (by name text and/or icon, whatever the
  client actually renders) as VIP Strive Jump / Gladiator Basic Training / Normal Attack / Strive Jump.
- P2 [corollary, proposed]: the 4 entries appear in the same order the 6th frame sent them (111, 40000, 99,
  110). If the window instead shows them in a different order, or sorted some other way, write that down --
  it is a finding about display order, not a failure of P1.
- P3 [falsifier]: the window still shows 0 entries (or something clearly unrelated/garbled) after the full
  sweep, despite all 6 frames going out unrejected on the wire -- a REAL NEGATIVE, not a failure. Per
  PANYA-DECISION 20260903_1934, whoever consumes this result must, in the SAME round, close or reword the
  open "does the client render anything" question in learn_skill_result_hypothesis.py's own module
  docstring/NONCLAIMS section -- do not leave that question looking open once this ticket has answered it.
- P4 [possible mixed outcome, not pre-judged]: the window shows some but not all of the 4 entries, or shows
  extra/garbled entries left over from the 5 earlier arbitrary-probe frames (COUNT0/COUNT1/COUNT3 pairs) that
  fired 3.0s-9.0s earlier in the same sweep -- if this happens, it tells us the window is CUMULATIVE across
  frames rather than replace-on-receipt, a separate finding from the main content claim.

### PRECONDITION (verify before step 1, not a footnote)
P0. Same as GT-116's own proven precondition: a normal login on the currently-merged production login path
    (class_id=1/level=1 into every login unconditionally, CORE-REQUEST-022, GT-116 CLOSED PASS). No special
    character build required for THIS ticket's own claim. SEPARATE precondition from GT-243's own P0 (skill
    99 learned and placed on a named hotbar/skillbar slot) -- satisfying either does not hurt or require the
    other.
P1. Server before client always; a client left open with no server dies on its own in ~3.5 minutes.
P2. Killing a client leaves the server holding the session -- restart the server before opening the next
    client or it hangs on "connecting" forever.
P3. A round copies the DB; character position resets to spawn every boot, expected, not a measured result.
P4. Teardown template refuses a boot stamp older than 420 minutes -- run teardown even if the session ends
    because the tester stopped.

### BOOT ORDER / piggyback note (read before scheduling)
Approved to run in the SAME ATTENDED APPOINTMENT as GT-243, to save booking a second sitting -- NOT the same
server process boot. GT-243's own server args are explicit: no `--*-scenario` flag of any kind (it needs a
bare wire to observe the hotkey-dispatch path cleanly). This entry needs
`--learn-skill-result-hypothesis-scenario`, which GT-243 forbids. Run them as two separate boots, back to
back, in either order, inside the same LOCK_GAME hold: fresh DB copy per boot, full teardown between them if
the boot-stamp/server-restart rules require it. Do not merge the two into one boot.

### BEFORE BOOT -- gate 0/1/2 (merge status; do not skip, do not eyeball a SHA)
Gate 0 -- **cleared**: `pirate-force-server#768` (commit `bdfc7885`) merged to `main` (chief confirmed
directly against `src/pirateforce_foundation/learn_skill_result_hypothesis.py` and
`scenarios/learn_skill_result_hypothesis_learn_sweep.json` on `main`, round `zwxuuk` -- six-step
`LEARN_SKILL_RESULT_STEP_ORDER` including `COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0` and `frames_per_accepted_
request: 6` both present).
Gate 1 -- resolve a green commit:
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
Only exit 0 with a printed `BOOT_COMMIT: <sha>` means bootable. exit 3 = this ticket waits on the gate, not
on the tester -- do not boot, do not checkout a branch directly to skip the resolver.
Gate 2 -- confirm the resolved SHA actually carries the code:
```
git grep -n "learn-skill-result-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git grep -n "COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0" <SHA> -- src/pirateforce_foundation/learn_skill_result_hypothesis.py
git cat-file -e <SHA>:scenarios/learn_skill_result_hypothesis_learn_sweep.json && echo SCENARIO_PRESENT
```
Need a hit on all three. Read the exact pin values (payload/pc/frame size and sha256, per step label)
straight from `scenarios/learn_skill_result_hypothesis_learn_sweep.json ->
probe.per_step.COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0` in the commit you actually boot -- do NOT trust any hash
or size written in this ticket.

### db (a copy, always -- never open the canonical file)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-249_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt249_<yyyyMMdd_HHmmss>.sqlite3
```
- sha256 of the canonical file, before and after, must match `CANON_SHA.txt` both times.
- `database_write=none` for this lane (confirmed in the module docstring) -- expect the working copy's only
  diff from a bare login to be the usual +1 row in `sessions`; `PRAGMA integrity_check = ok` both times.

### server args (exact -- opt-in only, production_allowed stays False)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt249_<stamp>.sqlite3 --learn-skill-result-hypothesis-scenario scenarios\learn_skill_result_hypothesis_learn_sweep.json
```
`--db` is required and must point at an existing file. Keep stdout+stderr captured together (2>&1). The
server console must show whatever mode banner the resolved commit prints for this scenario.

### chat trigger -- exactly 12 printable ASCII characters
- This lane's dispatcher fires on ANY chat-input frame whose text is exactly 12 printable ASCII characters --
  shape-triggered, not string-triggered (`classify_chat_input_attempt` -> ascii12). One character short or
  long reaches the server and the condition silently fails to match -- no error, the sweep just does not
  fire.
- Use `SKILLCONTENT` for this ticket (S-K-I-L-L-C-O-N-T-E-N-T = 12 characters exactly).
- Click the chat box to focus it before typing -- characters typed while chat is NOT focused become hotkeys,
  not chat text. Type the 12 characters, press Enter once, then immediately click empty ground to drop focus
  again before pressing K.
- One accepted trigger fires ALL 6 frames of the sweep, 3.0s apart, the first at 0.0s delay -- the 6th frame
  (this ticket's own frame) lands roughly 15s after Enter, plus send/composition time. Budget at least 18-20s
  of continuous recording after Enter before judging the final window state.
- The sweep is not one-shot -- firing the trigger again re-sends all 6 frames from the top.

### steps (click by click; record continuous video for the whole session)
Before start: hold LOCK_GAME, note boot stamp, compare canonical sha, copy DB per the db block, clear gate
0/1/2 above, stage TEMPLATE_teardown_generic.ps1.
1. Start the server first (`Get-NetTCPConnection -State Established` on ports 10188/10189 must be 0 before
   opening the client) -- console shows the scenario's mode banner.
2. Open client -> select server -> PVP dialog left button -> character select -> the character used in this
   sitting -> the middle of the 5 bottom buttons = enter game (never the leftmost -- that deletes the
   character). Start continuous recording before pressing enter-game.
3. T0 -- HP bar / minimap / map name visible. Photograph full-res (S00-HOME). Record every name-label colour
   in this still, one line per label, "none" written out where there is none.
4. NO-CRASH check: right-click-drag to sweep the camera once. Camera-only, character facing never moves,
   nothing goes out on the wire -- safe at any point. Never use Q/E or W/A/S/D for this check.
5. BASELINE: confirm chat is not focused (click empty ground) -> press K (or click Bt_main_Skill) ->
   photograph full-res (S-BASE-K). Expect the same state GT-116 measured (window opens, 0 entries) -- if
   baseline already shows something else, write it down prominently before continuing.
6. Close the window if it opened. Click the chat box to focus it -> type `SKILLCONTENT` -> press Enter once
   -> immediately click empty ground to drop chat focus. Record the clock time (HH:MM:SS+07:00) of Enter as
   T_TRIGGER.
7. Best-effort intermediate captures (not this ticket's pass/fail measure, useful context for P4): press K
   roughly every 3s after T_TRIGGER if quick enough to catch a window already open, photographing each time
   (S-MID-1 .. S-MID-5), noting the approximate elapsed time since T_TRIGGER for each. If timing is missed,
   write "not caught" rather than guessing.
8. Wait until at least 20s have elapsed since T_TRIGGER. Press K (or click Bt_main_Skill) -> photograph
   full-res (S-FINAL-K). This still is the primary evidence for this ticket's own claim.
9. If the window is open: photograph its full content full-res, transcribe what it shows character-for-
   character from the still -- every visible entry's name/label/icon description, count of entries, any
   entry that does not obviously correspond to one of the 4 real skill names. Write "illegible" rather than
   inferring.
10. Secondary positive control: press C to open the CHARACTER window, photograph, close.
11. NO-CRASH check again (right-click-drag).
12. Fire the trigger a second time (type `SKILLCONTENT`, Enter, drop focus) to confirm repeatability -- wait
    20s again, press K, photograph (S-REPEAT-K). Record whether the second sweep changes anything from
    S-FINAL-K.
13. Log out -> teardown via TEMPLATE_teardown_generic.ps1 (boot stamp must still be under 420 min) -> recheck
    canonical sha256 -> sha256 every capture.
STOP: if the game client crashes or closes at any point, stop immediately, record it as a measured result
with the frame/step it happened at, and still run teardown.

Colour rule: one line per name label per image, write "none" not blank, read colours from full-resolution
stills only, never infer a cause for a colour (RE-067 owns that question). Divergences from the original
server's own screenshots go into REAL_SERVER_DIVERGENCE.tsv, one row each.

### pass criteria (two layers, never mixed, never offered as proof of each other)

wire/DB (headless-provable from GAME_LIVE.txt / server console+log, no human needed for this layer):
- Raw capture around T_TRIGGER shows exactly 6 outbound frames spaced ~3.0s apart, the 6th and last being the
  COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0 composition (largest of the 6, per the module's own pinned sizes).
- That 6th frame's body decodes to: u16 tag 0x12 count=4; then 4 records in order, each u32 tag 0x14 / u16
  tag 0x12 / u32 tag 0x14 all three equal to the same skill id, in the order 111, 40000, 99, 110; trailing u8
  tag 0x0B value 0 -- byte-exact against the payload/pc/frame sha256 and size pinned in
  `scenarios/learn_skill_result_hypothesis_learn_sweep.json` for this label at the booted commit.
- `sessions` table +1 row per login; `lease_generation` does not go backward; `PRAGMA integrity_check = ok`
  both times; canonical sha256 matches `CANON_SHA.txt` before and after; no other table changes.
- No traceback, no unexpected socket close, in either console log.
- This layer CANNOT say whether anything appeared on screen -- do not use it as a stand-in for the
  client-observable layer below.

client-observable (a human at the screen only, never inferred from console/log):
- S-BASE-K: baseline state before the trigger (expected: window opens, 0 entries, matching GT-116; write down
  verbatim if it does not).
- S-FINAL-K (>=20s after T_TRIGGER): the PRIMARY reading for this ticket. Write, in plain language, exactly
  what is in the window -- entry count, and for each entry whatever name/icon/tooltip text the client shows.
  PASS reading = exactly 4 entries, each independently recognizable as one of VIP Strive Jump / Gladiator
  Basic Training / Normal Attack / Strive Jump (record the literal display strings, do not paraphrase them).
  NEGATIVE reading = 0 entries, or entries that do not correspond to any of the 4 names, after confirming the
  wire layer above shows the frame went out clean.
- S-MID-1..5 (best-effort): whatever was caught mid-sweep, with elapsed time noted, or "not caught".
- S-REPEAT-K: whether firing the trigger a second time changes S-FINAL-K's state.
- C / CHARACTER window control check (step 10).
- Both NO-CRASH checks pass.
- Name-label colours recorded per the colour rule above, one line per label per full-res still, for every
  photograph taken this session.
- This layer CANNOT say what bytes actually left the server -- do not use it as a stand-in for the wire/DB
  layer above.

### outcome boxes (pick one, report which; a negative result is worth as much as a positive)
A. S-FINAL-K shows exactly 4 entries and all 4 are independently recognizable as the 4 real class_id=1
   starting-kit skills -> PASS. Record display order too (P2).
B. S-FINAL-K shows some but not all 4, or shows extras/garbled entries alongside them -> PARTIAL/MIXED, not a
   clean PASS. Write exactly which of the 4 are present, which are missing, and describe anything extra
   verbatim. Do not average this into a PASS or a FAIL.
C. S-FINAL-K shows 0 entries despite the wire layer confirming all 6 frames went out clean and unrejected ->
   NEGATIVE, complete and valid (P3). Redirect: per PANYA-DECISION 20260903_1934, whoever consumes this
   result closes or rewords the "does the client render this vital's content" open question inside
   `learn_skill_result_hypothesis.py`'s own module docstring/NONCLAIMS in the SAME round.
D. S-FINAL-K shows entries but none of them resemble any of the 4 real skill names/icons -> NEGATIVE of a
   different flavour than C -- the window renders SOMETHING from this vital but not identifiably the sent
   content. Record verbatim; do not guess at what it might mean.
E. Client crashes/closes, or a frame is rejected on the wire, before the 6th frame's window (T_TRIGGER+20s)
   -> NO-RESULT, report exactly where it stopped, still run teardown.

### things this ticket must not conclude (evidence discipline)
- Does not name any of the three record-wire positions (record_u32_0 / record_u16_4 / record_u32_8) as "the"
  skill-id field even on a clean PASS -- each record in this frame repeats the same id in all three
  positions specifically so this question stays open.
- Does not claim anything about the trailing u8's meaning -- this step sends 0 only, no companion is sent.
- Does not claim the original (defunct) server ever sent 0x673C in this shape, this order, or on this
  trigger -- the step plan, values, spacing and trigger policy are this project's own design.
- A PASS here does not prove the 4 skills are actually usable, learnable through any real game action, or
  persisted anywhere (`database_write=none`) -- only that the window can be made to display them via this
  hand-composed frame.
- Does not decide the cause of any name-label colour observed (RE-067 owns that question).
- If gate 0/1/2 does not clear, the entire entry is BLOCKED, not NO-RESULT/FAIL -- record "waiting on merge"
  and stop.

### nonclaims
1. Does not prove or test skill usability, cooldowns, damage or persistence of any of the 4 skills.
2. Does not prove anything about a class other than class_id=1, or about any character other than the one
   used this session.
3. Does not reopen or change the verdicts of GT-058/GT-059/GT-064 (archived CLOSED) or GT-116 (CLOSED PASS)
   -- this is a new, narrower question those tickets never asked.
4. Does not touch or depend on GT-243's own claim (hotbar-vs-hotkey dispatch producer) -- the two tickets
   share only an attended appointment and a login precondition, not a server boot or a claim.
5. Does not resolve the semantics of the three record-wire positions or the trailing u8.
6. Does not prove anything about the inbound CLearnSkillVital 0x36AA direction (no handler exists).
7. Single account, single character, one attended sitting -- no second player observing, no cross-account
   comparison.
8. Does not decide the cause of any name-label colour observed (RE-067 stays open).

### closing instructions (per PANYA-DECISION 20260903_1934)
If the result lands in outcome box C or D above, the lane that consumes this result must, in the SAME round,
open a follow-up edit to `learn_skill_result_hypothesis.py`'s own module docstring (the "NO CLIENT HAS EVER
SEEN ONE OF THESE FRAMES... queued and not run" sentence and any nearby claim implying this question is still
open) so the module's own text stops implying an unanswered question this ticket has just answered. Name
`GT-249` in that edit.

## numbering
`GT-248` ถูกใช้เป็น `RE-248` ในรอบเดียวกัน (`CLIENT_RE_QUEUE.md` -- ตัวนับร่วมสองคิว) => ใบนี้ `249`
`GT-249`/`RE-249` = 0 hit ทั้งสามที่ก่อนวาง (ตรวจโดย chief รอบ `epkucn`/R344)

---

## GT-254 ISLAND-155-CONTACT-TRIGGER-FRAME-CAPTURE-001  [⛔ **CLOSED = `CANCELLED - refuted by KA1A-R318 §3 (Slave Market Island/แถว 155 อยู่ฉาก 304 Dark Fog Sea ไม่ใช่ 126)`** -- ปิดโดย chief (LANE-E)... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-250 NAME-LABEL-PERSISTS-AFTER-WALK-AWAY-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — NEGATIVE-AGAIN (ป้ายชื่อไม่หายซ้ำ R321 2026-09-06 11:29 · ผลแรก NEGATIVE ที่ R317... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-251 TRACEPATH-GO-TWO-TARGETS-DISCRIMINATOR-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — ANSWERED — ตอบ RE-236(ข)/RE-119 T4: id ที่ client ส่งใน TracePathVital คือ id... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-252 COLUMBUS-OPTION2-BORNAGAIN-CLICK-CAPTURE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS — เก็บครบตามใบ (R317 2026-09-05 §4: quest 3205 ถูกปฏิเสธ... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-253 OPTIONS-APPLY-ONE-SETTING-DIFFERENTIAL-CAPTURE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — ตรวจแล้ว — ไม่มีในบันทึก R307/R309/R317/R320/R321 (R320 มีแค่ RE-237 คู่กันซึ่ง CAPTURED แล้ว แต่ GT-253 เองยังไม่ถูกบูต) → คงสถานะ PENDING เดิมไว้ ไม่ปั๊มผล · 🟡 **PENDING -- เนื้อใบครบแล้ว (LANE-UI รอบ `9f2k7c`) รอคิว attended** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-UI** · หัวพลิกโดย chief (LANE-E) รอบ `cooif2`/R357 ตาม `COO-DECISION 20260905_1546` + `20260905_1545` ข้อ 3 · ผู้เปิดใบ/ตั้งเลข = chief (LANE-E) รอบ `kj0s6r`/R346 ตาม `COO-DECISION 20260904_2143` ข้อ 3 และคำตัดสิน COO `NOW.md` 2026-09-05 01:45 · ผู้รัน = Panya (attended) ~3 นาที · **ข้อ 4 (ท้ายสุด) ใน 4 ใบ** (GT-250 > GT-251 > GT-252 > GT-253) · **ต่อท้ายคิว `รอเครื่องคุณ` ไม่ใช่หัวคิว** · ไม่บล็อกสายใด รวมทั้งไม่บล็อก LANE-UI เอง · **ไม่มีการตีมอน**]

> 🔴 **เนื้อใบเคาะจบแล้ว (LANE-UI รอบ `9f2k7c` 2026-09-05T16:5x+07:00 ตาม `COO-DECISION 20260905_1546`)** -- `RE-237` ลงเนื้อจริงแล้วในรอบ `hq4wtb` (02:03) พร้อมร่างใบนี้ติดมาให้เคาะทันที · เนื้อข้างล่างคือแผน differential แบบ wire-only (diff ไบต์ดิบข้ามการเปลี่ยนค่าทีละหนึ่ง เทียบ same-value control) ที่แทนที่เกณฑ์ `[PROPOSED]` เดิม (breakpoint/vtable-slot บนไบนารีไคลเอนต์ -- ไม่มีเครื่องมือ debugger ในชุดผู้เทส attended ของโปรเจกต์นี้) · **สถานะคิวยังเป็น `BLOCKED`/`PENDING` ตามที่ chief พลิกหัวในรอบถัดไป ไม่ใช่ `READY`** -- ห้ามลบ ห้ามย้ายใบนี้จนกว่าจะถูกทดสอบจริง (กติกาคิว: `PENDING`/`READY`/`BLOCKED`/`RUNNING` อยู่ที่เดิมเสมอ)
>
> 🔴 **ใบนี้ไม่มี breakpoint/memory-instrumentation ใด ๆ ทั้งสิ้น** -- ชุดเครื่องมือผู้เทสมีแค่บูตเกม/คลิก UI/จับเฟรมสาย+คอนโซล (`AGENTS.md`, `BRIDGE_BOOT_PROCEDURE.md`) เกณฑ์ `[PROPOSED]` เดิมในจดหมาย `1054` ที่ขอ log vtable slot / identity ของอ็อบเจกต์ที่รันไทม์ **ทำไม่ได้จริงบนชุดเครื่องมือนี้ -- ใบนี้แทนที่เกณฑ์นั้นด้วยการ diff ไบต์ดิบบนสายล้วน (black-box)**

- objective: (ข้ออ้างเดียว) การ diff ไบต์ดิบของเฟรมขาออก `UserSetting_UpdateServerSettingVital` (`0x0F01`) ที่ไคลเอนต์ส่งตอนกดปุ่ม **Apply** ในเมนู Options ระหว่างการเปลี่ยนค่าตั้งค่าทีละหนึ่งค่า เทียบกับการกด Apply โดย**ไม่เปลี่ยนอะไรเลย** (same-value control) บอกได้ว่า **ตำแหน่งไบต์ใดในเฟรมขยับตามการเปลี่ยนค่าตั้งค่าใด** และ **มีตำแหน่งไบต์ใดขยับแม้ไม่มีการเปลี่ยนค่าตั้งค่าเลยหรือไม่** (สัญญาณว่าไบต์นั้นไม่ใช่ค่าตั้งค่าจริง) -- นี่คือหลักฐานเชิงสหสัมพันธ์บนสาย (correlation) ไม่ใช่การพิสูจน์ตัวตน/semantic ของฟิลด์ (ดู nonclaims) · **ค่าที่จะเปลี่ยนจริง 2 ค่า ไม่ตั้งชื่อล่วงหน้า** เพราะยังไม่มีสารบัญตัวควบคุมของแผง Options เลยในโปรเจกต์นี้ (ขั้น 4 บังคับให้จดของจริงจากจอก่อนเลือก แล้วอ้างอิงเป็น `Setting-1`/`Setting-2` ตามลำดับที่เห็น -- ห้ามเดาชื่อล่วงหน้า)

- db: canonical = `state\pirateforce.sqlite3` -- 🔴 **สำเนาเท่านั้น ห้ามเปิด canonical** ⇒ คัดลอกเป็น `state\run_gt253_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา -- sha256 canonical ก่อน/หลังต้องตรง -- `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง -- ใช้ตัวละครเดิมที่มีอยู่แล้วก็ได้ (ใบนี้ไม่แตะกระเป๋า/เงิน/ตำแหน่ง -- ตำแหน่งจะรีเซ็ตกลับจุดเกิดทุกบูตเพราะบูตบนสำเนาใหม่ ไม่ใช่ปัญหาของใบนี้)

- server args: บูตมาตรฐาน -- **ไม่มีแฟล็ก scenario ใด ๆ** -- `-SecondPasswordMode bypass` -- 🔴 เก็บคอนโซล **รวม stdout+stderr (`2>&1`)**
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt253_<stamp>.sqlite3 2>&1
  ```
  ต้องมีตัวจับแพ็กเก็ตเปิดอยู่ตลอดใบ: `capture_v141\GAME_LIVE.txt` (hex ดิบ) และ `GAME_EVENTS_LIVE.txt` 🔴 **เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ** -- เปิดไคลเอนต์ทิ้งไว้โดยไม่มีเซิร์ฟเวอร์ตายเองใน ~3.5 นาที -- ถ้าปิดไคลเอนต์กลางคัน **เซิร์ฟเวอร์ยังถือเซสชันไว้** ⇒ ไคลเอนต์ตัวถัดไปจะค้าง "connecting" ตลอดกาลจนกว่าจะรีสตาร์ตเซิร์ฟเวอร์ก่อน

- steps: (**จดเวลานาฬิกา `HH:MM:SS+07:00` ทุกครั้งที่เขียนว่า "จดเวลา"** -- ใช้ตัดหน้าต่าง hex ทีหลัง)
  1. `LOCK_GAME` -- จด boot stamp -- sha canonical ก่อน -- คัดลอก DB เป็น run copy -- บูตเซิร์ฟเวอร์ใหม่สด
  2. บูตไคลเอนต์ -- ล็อกอิน -- ถึงหน้า HOME -- ภาพนิ่ง `S00-HOME` (เต็มความละเอียด) -- **จดสีป้ายชื่อทุกป้ายที่อยู่ในเฟรมนี้ บรรทัดละหนึ่งป้าย เขียน "none" ถ้าไม่มีป้ายเลย ไม่เว้นว่าง** (คำสั่ง Panya 2026-08-25 บังคับทุกใบ attended ตั้งแต่ R163)
  3. คลิกปุ่มเฟือง (gear) มุมซ้ายล่าง -- เปิดแผง Options โดยตรง (**ไม่ใช่ปุ่มหกเหลี่ยม HOME ที่นำไป logout** -- ดูโน้ตนำทางที่มีอยู่แล้ว `GAME_TEST_QUEUE.md:285`) -- ภาพนิ่ง `S01-OPTIONS-OPEN` เต็มความละเอียด
  4. 🔴 **ขั้นสำรวจบังคับ (ไม่มีใครในโปรเจกต์เคยบันทึกมาก่อน)**: จดรายการ**ทุก**ตัวควบคุมที่เห็นบนแผง Options ตามลำดับบนลงล่าง -- ชื่อป้ายตามตัวอักษรที่เห็นจริง / ชนิด (สไลเดอร์, checkbox, dropdown, radio) / ค่าปัจจุบัน / ช่วงค่าถ้าเป็นสไลเดอร์ -- ตั้งชื่ออ้างอิงในผลลัพธ์ `Setting-1`, `Setting-2`, ... ตามลำดับที่จดไว้ (**ถ้าเห็นไม่ตรงกับที่คาดในเนื้อใบนี้ ให้จดของจริงแทน ไม่เดา**) -- รายการนี้เป็นผลส่งมอบของใบนี้เองแม้ trial ทั้งหมดข้างล่างจะเป็นลบ
  5. **Trial T0 (baseline / same-value control #1)**: **ไม่แตะตัวควบคุมใดเลย** -- คลิก **Apply** -- จดเวลาทันที
  6. **Trial T1..T4 (เปลี่ยนทีละหนึ่งค่า)**: ไล่ทีละ `Setting-1`, `Setting-2`, ... ตามลำดับที่จดในขั้น 4 (สูงสุด 4 ค่า -- ถ้ามีน้อยกว่า 4 ให้ทำเท่าที่มีจริงแล้วข้ามไปขั้น 7 -- ถ้ามีมากกว่า 4 ให้เลือกให้ครบทุก **ชนิด** ตัวควบคุมที่ต่างกัน (สไลเดอร์อย่างน้อยหนึ่ง, checkbox อย่างน้อยหนึ่ง, dropdown/radio ถ้ามี) ก่อนเลือกซ้ำชนิดเดิม): ต่อค่า -- (ก) เปลี่ยน**เฉพาะ**ค่านั้นหนึ่งขั้นจากค่าปัจจุบัน (สไลเดอร์ = ขยับหนึ่งขีดที่มองเห็น, checkbox = สลับ, dropdown = เลือกตัวถัดไป) **ห้ามแตะตัวควบคุมอื่นเลยในสเต็ปเดียวกัน** (ข) จดค่าเก่า -> ค่าใหม่ + จดเวลา (ค) คลิก **Apply** -- จดเวลาอีกครั้ง เรียกว่า `T1`..`T4` ตามลำดับ (ง) **ไม่ต้องคืนค่าเดิม** -- เดินต่อไปยัง Setting ถัดไปจากค่าที่เพิ่งเปลี่ยนไป (สะสม ไม่ revert)
  7. **Trial T_mid (baseline / same-value control #2)**: หลังทำ trial เปลี่ยนค่าไปแล้วอย่างน้อย 2 ค่า (หรือครบเท่าที่มีถ้าน้อยกว่า) -- **ไม่แตะตัวควบคุมใดเลยตั้งแต่ Apply ครั้งก่อน** -- คลิก **Apply** -- จดเวลา
  8. ทำ trial ที่เหลือ (ถ้ามี `Setting-3`/`Setting-4`) ตามรูปแบบขั้น 6 ต่อ
  9. **Trial T_final (baseline / same-value control #3)**: ปิดแผง Options แล้วเปิดใหม่ -- ภาพนิ่ง `S02-OPTIONS-REOPEN` เต็มความละเอียด (ยืนยันด้วยตาว่าค่าที่เปลี่ยนไปแล้วทุกตัวยังอยู่ตามที่ตั้งไว้ -- ถ้าค่าใดเด้งกลับ ให้จดเป็น finding แยก ไม่ใช่ทำให้ใบนี้ล้ม) -- **ไม่แตะตัวควบคุมใดเลย** -- คลิก **Apply** -- จดเวลา
  10. ภาพนิ่ง `S03-OPTIONS-CLOSE` -- ปิดแผง -- เช็ก NO-CRASH ด้วย**คลิกขวาค้างลากเมาส์หมุนกล้องเท่านั้น** (กล้องหมุนไม่ทำให้ facing ของตัวละครเปลี่ยนและไม่ยิงอะไรออกสาย ปลอดภัยทุกจังหวะ) -- 🔴 **ห้ามใช้ `Q`/`E` หรือ `W/A/S/D` เป็นตัวเช็ค NO-CRASH** (ยิง `TargetPosVital` ออกสายจริง ปนกับข้อมูลของใบนี้)
  11. ปิดเซิร์ฟเวอร์ -- เก็บ `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ -- `integrity_check` -- sha canonical ซ้ำ -- **รัน teardown เสมอ** (แม้เลิกกลางคัน -- teardown ปฏิเสธ boot stamp เกิน 420 นาที ตาม `TEMPLATE_teardown_generic.ps1:135` -- อย่าปล่อยรอบค้างข้ามคืน)
  12. คัดผลจากคอนโซล/แคปเจอร์ (ดิบ ห้ามตีความ): `findstr /N /C:"0x0F01" capture_v141\GAME_LIVE.txt` และ/หรือ `findstr /N /C:"UserSetting_UpdateServerSettingVital" capture_v141\GAME_EVENTS_LIVE.txt` -- จับคู่แต่ละบรรทัด `RECV` ที่เจอกับเวลานาฬิกาที่จดไว้ในขั้น 5-9 เพื่อติดป้าย `T0`/`T1`..`T4`/`T_mid`/`T_final` ให้ตรงเฟรม -- คัด hex เต็มของทุกเฟรมที่ติดป้ายได้ลงผล

- pass criteria: (สองชั้น ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)
    wire/DB (พิสูจน์ headless ได้จากไฟล์ที่เก็บมา ไม่ต้องมีตาคนตอนวิเคราะห์ -- แต่การ**เก็บ**ต้องมีตาคนตอนคลิก):
      1. ทุก trial (T0..T_final, ขั้นตอนบังคับ [`T0`, อย่างน้อยหนึ่ง trial เปลี่ยนค่า, `T_mid`, `T_final`] รับประกันอย่างน้อย 4 เฟรมเสมอ -- สูงสุด 7) มีเฟรม `0x0F01` RECV ครบหนึ่งเฟรมต่อหนึ่งคลิก Apply พร้อม hex เต็ม + เวลา -- **ส่งมอบครบ** = deliverable ขั้นต่ำของใบนี้ไม่ว่าไบต์จะเหมือนกันหรือไม่
      2. รายงาน byte-diff ของทุกคู่ trial ที่ติดกัน (T0 vs T1, T1 vs T2, ... ) พร้อม**ตำแหน่งไบต์ที่ต่างกันเป๊ะ (offset นับจาก 0 ของ payload)** ถ้าไม่มีตำแหน่งใดต่างกันเลยก็เขียนว่า "ไม่มี" ตรง ๆ (ผลลบมีค่าเท่าผลบวก)
      3. รายงาน byte-diff ของคู่ baseline ล้วน (T0 vs T_mid, T_mid vs T_final, T0 vs T_final) แยกจากข้อ 2
      4. integrity_check = ok ทั้งสองครั้ง -- sha canonical ก่อน/หลังตรงกัน -- teardown ยืนยัน (process 0, listener 10188/10189 = 0)
      **ชั้นนี้ตอบไม่ได้**: identity ของ callee `0x00720FC0` / ปลายทาง vtable slot / identity ของอ็อบเจกต์ที่ `ECX+0x0C` -- ตอบได้แค่ "ไบต์ตำแหน่งนี้ขยับ/ไม่ขยับพร้อมค่าตั้งค่านี้" เท่านั้น
    client-observable (ต้องมีตาคน -- ห้ามอนุมานจากไฟล์จับสาย):
      5. รายการตัวควบคุมทั้งหมดบนแผง Options ของบิลด์นี้ (ชื่อ/ชนิด/ค่า) ตามที่จดในขั้น 4 -- นี่คือ inventory แรกที่โปรเจกต์นี้มี
      6. ภาพนิ่งเต็มความละเอียด `S00-HOME`/`S01-OPTIONS-OPEN`/`S02-OPTIONS-REOPEN`/`S03-OPTIONS-CLOSE` ยืนยันค่าที่เปลี่ยนจริงบนจอตรงกับที่จดไว้ในแต่ละ trial (ค่าเก่า -> ค่าใหม่)
      7. สีป้ายชื่อทุกป้ายในทุกภาพนิ่ง บรรทัดละหนึ่งป้าย เขียน "none" ถ้าไม่มี -- อ่านจากภาพเต็มความละเอียดเท่านั้น (ห้ามอ่านจาก contact sheet/ภาพย่อ/วิดีโอ) -- ส่วนต่างจาก reference เดิมของค่าย ลงแถวใหม่ที่ `REAL_SERVER_DIVERGENCE.tsv` ถ้ามี
      8. NO-CRASH/CRASH ตามที่เห็นจริงตอนคลิกขวาลากหมุนกล้อง
      9. ปิดใบด้วย `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` -- ไม่มีบรรทัดนี้ chief ไม่บริโภคเป็นผลปิดใบ

- ตารางแปลผล (ผลจากชั้น wire/DB ข้อ 2-3 ข้างบน -> จะปิด/เปิดอะไรต่อใน `RE-237`):

| ผลที่สังเกตได้ (diff ดิบ) | สิ่งที่ปิดได้ | สิ่งที่ยังเปิดอยู่เสมอ |
|---|---|---|
| **(A)** มีตำแหน่งไบต์ P เปลี่ยนเฉพาะตอน trial เปลี่ยนค่า Setting-K ตัวเดียว และ P **คงที่** ในทุกคู่ baseline (T0/T_mid/T_final) | field 3/4/5/6 (อย่างน้อยหนึ่งตัว) **มีอยู่จริงบนสาย** และผูกกับค่าตั้งค่าที่มองเห็นบนจอ -- ปิดข้อกังวลว่า "field พวกนี้ไม่มีอยู่บนสาย" ได้ | **ยังไม่ปิด**: ตำแหน่ง P ตรงกับ field 3 หรือ field 6 (เลขในตาราง `PF_SERIALIZER_FIELDS.tsv`) เป็นแค่ **[PREDICTION]** จากลำดับ call-site ไม่ใช่ข้อพิสูจน์ -- ทายผิดคือ finding ไม่ใช่ความล้มเหลว -- identity ของ callee/vtable ยังไม่รู้เหมือนเดิม |
| **(B)** ไม่มีตำแหน่งไบต์ใดนอกเหนือจากช่วงที่รู้แล้ว (field 1-W/2-R) เปลี่ยนเลย ในทุก trial เปลี่ยนค่า | -- (ไม่ปิดอะไร) | **ผลลบ**: การเปลี่ยนค่าขนาดหนึ่งขีด/หนึ่งครั้งที่ทำรอบนี้ไม่ถึงสาย -- redirect: ใบถัดไปต้องลองเปลี่ยนขนาดใหญ่กว่านี้ (สไลเดอร์ต่ำสุด<->สูงสุด) ก่อนสรุปว่า field 3-6 ไม่มีเนื้อหาจริง |
| **(C)** มีตำแหน่งไบต์เปลี่ยนระหว่างคู่ baseline ล้วน (เช่น T0 vs T_mid) ที่**ไม่มีการแตะตัวควบคุมใดเลย** | ให้สัญญาณ black-box สนับสนุน (ไม่ใช่พิสูจน์) ว่าตำแหน่งนั้นเป็น **counter/lifecycle ไม่ใช่ field ค่าตั้งค่า** -- ใช้ตอบคำถามเปิดของ field 4/5 ได้บางส่วนโดยไม่ต้องมี debugger | **ยังไม่ปิด**: ไม่พิสูจน์ alias/ไม่ alias กับ stream buffer จริง (คำถามเดิมของเอกสารวิธีการที่ปฏิเสธคำว่า "refcount noise" ยังต้องรอ debugger ถึงจะปิดสนิท) |
| **(D)** เฟรมเหมือนกันไบต์ต่อไบต์ทุก trial ทั้งเปลี่ยนค่าและ baseline | -- (ไม่ปิดอะไร) | **ผลลบทั้งใบ**: ตัวควบคุมที่ทดสอบรอบนี้ไม่ไปโผล่ในเฟรมนี้เลย และไม่มีอะไรฟรีรันด้วย -- redirect: ตรวจว่ามีตัวควบคุม Options อื่นที่ยังไม่ได้ลอง (ดูรายการขั้น 4) หรือปุ่ม Apply ตัวนี้ผูกกับเฟรมคนละใบจากที่คาด |

- STOP: ไคลเอนต์ปิดตัวเอง / มี `ErrorData` ใด ๆ ระหว่าง trial ใด -> หยุดทันที บันทึกว่า trial ไหนที่กำลังทำอยู่ก่อนหยุด (ไม่ปกปิด) แล้วเดินขั้น 10-11 ต่อให้จบเพื่อเก็บ teardown ให้ครบ -- **ห้ามเปิดไคลเอนต์ใหม่ทับเซสชันเดิมโดยไม่รีสตาร์ตเซิร์ฟเวอร์ก่อน**

- predictions: (A) เป็นผลที่ ka1-A คาดหวังสูงสุดจาก call-site ordering แต่เป็นแค่การเดา -- (B)/(D) มีโอกาสจริงพอกัน (ทายผิด = finding ไม่ใช่ความล้มเหลว) · ถ้าออก (B) หรือ (D) ให้เปิดใบใหม่ทดลองขนาดการเปลี่ยนค่าที่ใหญ่กว่านี้ก่อนสรุปว่า field 3-6 ไม่มีเนื้อหาจริงบนสาย

- nonclaims:
  1. ไม่ยืนยัน/ปฏิเสธ identity ของ callee `0x00720FC0` (field 3) -- ไม่มีการเปิดไฟล์ไบนารีหรือดัมพ์ใด ๆ ในใบนี้
  2. ไม่ยืนยัน/ปฏิเสธปลายทางจริงของ `DEREF(DEREF(DEREF(OBJ+0x14))+0x34)` (field 1-R/2-W/6) -- ไม่มี log vtable slot ในใบนี้ (เกณฑ์ `[PROPOSED]` เดิมของจดหมาย `1054` ที่ขอสิ่งนี้ทำไม่ได้บนชุดเครื่องมือผู้เทส -- ใบนี้แทนที่เกณฑ์นั้นทั้งหมด ไม่ใช่ทำเพิ่ม)
  3. ไม่พิสูจน์ว่าอ็อบเจกต์ที่ `ECX+0x0C` alias หรือไม่ alias กับ stream buffer จริง (field 4/5) -- ให้ได้แค่สัญญาณบนสายว่าไบต์ตำแหน่งนั้น "ขึ้นกับ state บนจอ" หรือ "ไม่ขึ้นกับ state บนจอ" เท่านั้น
  4. **การจับคู่ตำแหน่งไบต์ที่พบเข้ากับเลข field 3/4/5/6 ของ `PF_SERIALIZER_FIELDS.tsv` เป็น [PREDICTION] จากลำดับ call-site เท่านั้น ไม่ใช่การพิสูจน์** -- ทายผิดคือ finding ของใบนี้ ไม่ใช่ความล้มเหลว
  5. ทุก trial เปลี่ยนค่าเดียวเสมอ (ไม่มี trial ไหนเปลี่ยนหลายค่าพร้อมกัน) -- ไม่ทดสอบผลของการเปลี่ยนหลายค่าในคลิกเดียว
  6. ไม่ทดสอบขนาดการเปลี่ยนค่าที่ใหญ่กว่าหนึ่งขีด/หนึ่งตัวเลือก (ดู outcome B/D สำหรับ redirect)
  7. ไม่ทดสอบว่าค่าตั้งค่ายัง persist หลัง relogin/ข้าม session -- บูตบนสำเนา DB ใหม่ทุกรอบ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดเป็นปกติของกระบวนการนี้ ไม่ใช่ finding
  8. ไม่ทดสอบการกด Apply ซ้อนเร็ว/ดับเบิลคลิก -- ทุกคลิก Apply เว้นช่วงตามจังหวะที่ผู้เทสจดเวลาได้จริง
  9. ผลจากใบนี้ไม่ปิด `RE-237` เอง -- อย่างมากปิดได้แค่บางแถวใน "เกณฑ์ปิดใบ" เดิมของ `RE-237` ถ้าผลออกมาแบบ (A) หรือ (C) -- LANE-UI เป็นผู้ตัดสินว่าปิดแถวไหนได้จริงหลังอ่านผล
  10. ใบนี้ไม่เกี่ยวกับแถวอื่นในสารบัญ 15 แถวของ LANE-UI และไม่บล็อกแถวเหล่านั้น

- links: `CLIENT_RE_QUEUE.md` บล็อก `RE-237` -- `notes_to_chief/20260904_1054_LANE-UI-RE-TICKET-*.md` -- `external/PF_SERIALIZER_FIELDS.tsv:6167-6178` -- `external/PF_FIELD_VALIDATION.tsv:858-859` -- `FACTPACK_L2_CLASSCENSUS001_20260820.tsv:1293` (opcode `0x0F01`) -- `GAME_TEST_QUEUE.md:285` (โน้ตนำทางปุ่มเฟือง = Options) -- `notes_to_chief/20260905_0203_LANE-UI-RE-TICKET-re237-body-filled-plus-gt-number-request.md` (ร่างต้นฉบับที่เคาะเลขแล้วในรอบนี้) -- `notes_to_chief/20260905_1546_COO-DECISION-*.md` (สั่งเคาะขั้นตอน)

- result: (ผู้เทสกรอก: รายการตัวควบคุม Options ทั้งหมด (ขั้น 4) -- ตาราง T0..T_final พร้อมเวลา/ค่าเก่า->ใหม่/hex เต็มของแต่ละเฟรม -- ตาราง byte-diff ของทุกคู่ trial (ข้อ 2-3 ของ pass criteria) -- ระบุ outcome (A)/(B)/(C)/(D) ต่อคู่ที่วัดได้ -- ภาพ `S00-HOME`/`S01-OPTIONS-OPEN`/`S02-OPTIONS-REOPEN`/`S03-OPTIONS-CLOSE` เต็มความละเอียดพร้อม sha256 -- สีป้ายชื่อทุกป้ายทุกภาพ -- `integrity_check` สองครั้ง -- sha canonical ก่อน/หลัง -- NO-CRASH/CRASH -- `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)
  (ว่าง -- ผู้เทสกรอก)

## numbering
`GT-253`/`RE-253` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/`) ก่อนวาง -- ตรวจโดย chief รอบ `kj0s6r`/R346 · ตัวนับร่วมสองคิว + archive คืนสูงสุดที่ `249` ก่อนวางชุดนี้ · ใบชุดนี้กิน `250`-`253` ตามลำดับที่ COO เคาะ

---

## GT-255 SECOND-PASSWORD-AND-BAG-INBOUND-FRAME-CAPTURE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — ปิดได้ตามเกณฑ์ 'จับเฟรม' — Event B (เปิดกระเป๋า) ครบสองชั้น · Event A... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-257 CHAT-TWO-VITAL-TAIL-ONE-TYPING-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS 3/3 — กด M เปิด/ปิดแล้ว /warp ทันที ไม่พบ two-vital ในบูตนี้ (สมมติฐาน 'จะเห็น vital... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-258 WARP-SEND-FAILURE-ROLLS-THE-SCENE-BACK-001  [🟢 **READY** -- **STOP ก่อนบูตของใบต้นเรื่องปลดแล้ว**: `COO-DECISION 20260905_0948` บรรทัด 20 = "`#806` ขึ้น main แล้ว 08:58 -- STOP ก่อนบูตในใบ GT ที่ขอเลขไว้ (`0852`) ปลดได้ทันทีที่ chief ตั้งเลข" **[วัดแล้ว chief `pv4zg1` 11:2x บน clone ของเซิร์ฟเวอร์เอง: `git grep -n "install_send_outcome_observers" origin/main -- src/pirateforce_foundation/runtime.py` = เจอที่ `runtime.py:1627`] · [แหล่งที่สอง บนสะพาน: `notes_to_chief/20260905_0948_*.md:20` + `NOW.md:3` บล็อก 09:48 ("`#806` chief · `#807` DB · `#808` B · `#809` E ขึ้น main 08:58-09:35")]** · เลขตั้งแล้วในใบนี้ ⇒ STOP ปลด · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-GM** · ผู้ตั้งเลข/เปิดใบ = chief (LANE-E) รอบ `pv4zg1`/R352 · ผู้รัน = Panya (attended) · **ต่อท้ายคิว `รอเครื่องคุณ` ไม่ใช่หัวคิว** · ไม่บล็อกสายใด · **ไม่มีการตีมอน** · 🔴 **[LANE-K รอบ `kxpzxi` 2026-09-07T03:15+07:00] ถอนออกจาก `QUEUE_STATUS_SNAPSHOT.md` ชั่วคราว ตาม `PANYA-ORDER 20260907_0159` ข้อ 2** (หน้าที่คัดใบ attended ที่ไม่จำเป็น PANYA `2148` ย้ายมาอยู่กับ LANE-K): ใบนี้เข้าเกณฑ์ (ก) **อายุ >7 วัน** (เปิด 2026-08-25 = 13 วัน) และเป็นหนึ่งใน ใบที่เจ้าของยกเป็นหลักฐานในคำสั่งเอง · **K ยกเลิกใบเองไม่ได้ (พับ=คัดลอก)** — ใบยังเปิดอยู่ทุกตัวอักษร ไม่มีอะไรถูกลบ · **เจ้าของใบ LANE-GM ต้องตอบกลับ: ยืนยันซ้ำว่ายังต้องบูตจริง (แล้ว K ใส่กลับรถบัส) หรือยกเลิกพร้อมเหตุผลตามกฎ PANYA `20260903_1934`** · จดหมายแจ้ง: `notes_to_chief/20260907_0315_LANE-K-CULL-3-tickets-off-bus-need-owner-reconfirm.md`]] [✅ **ยืนยันซ้ำโดยเจ้าของใบ LANE-GM รอบ `vxr32s` — ใส่กลับหมวด ก. ของ `QUEUE_STATUS_SNAPSHOT.md` แล้ว** โดย LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00 · บรรทัดของเจ้าของใบคำต่อคำ: "`GT-258` ยังต้องบูตจริง เงื่อนไขในใบยังใช้ได้บนคอมมิต `34d439a` — ใส่กลับหมวด ก. ได้" · จดหมาย `notes_to_chief/20260907_0451_LANE-GM-TO-K-gt258-reconfirmed-with-headless-proof.md` · `HEADLESS_PROOF:` เติมในบล็อก `ATTENDED:` ข้างล่างแล้ว (โทเคนจากรัน headless บน `origin/main` `34d439a`) · nonclaim ของเจ้าของใบที่ K ยกมาด้วย: โทเคนพิสูจน์แค่ว่า **observer ติดตั้งจริงบน session จริง** (= W1 ด่านก่อนบูต) ไม่ใช่ W2/W3/W4 ที่ต้องบูตจริง · โทเคนไม่มีเลขฉากเพราะใบผูกกับ**การเชื่อมต่อ** ไม่ใช่ฉาก (ต่างจาก `GT-178`) — ถูกต้องสำหรับใบนี้ ไม่ใช่การเลี่ยงคำสั่ง]

ATTENDED: บูตด้วยทรี/ธง/env อะไร -- บูตมาตรฐาน **ไม่มีแฟล็ก scenario** · บัญชี GM จาก `config/gm_accounts.json` (หรือสำเนาผ่าน `PF_GM_ACCOUNTS_CONFIG` ห้ามแก้ไฟล์จริง) · เก็บ stdout+stderr รวมกัน · **อัดวิดีโอต่อเนื่องตลอด `LOCK_GAME`** · 🔴 **ด่านก่อนบูต**: `git grep -n "install_send_outcome_observers" -- src/pirateforce_foundation/runtime.py` ต้องเจอบนคอมมิตที่จะบูต -- ไม่เจอ = `[BLOCKED]` ข้ามใบ ไม่ใช่ FAIL · 🔴🔴 **คัดลอก DB ครั้งเดียวต่อรอบ** เป็น `state\run_gt258_<stamp>.sqlite3` แล้ว**ทุกครั้งที่รีสตาร์ตเซิร์ฟเวอร์ต้องชี้ไฟล์เดิมไฟล์นั้น** (`--db` เป็นของ**เซิร์ฟเวอร์** ไม่ใช่ของไคลเอนต์) -- คัดลอกใหม่กลางรอบ = ตัวละครกลับจุดเกิดทุกบูต = **หลักฐานการย้อน/ไม่ย้อนหายทั้งใบ** · อ่านกล่อง STOP และ pass criteria เต็มก่อนกด บล็อกนี้เป็นสรุปไม่ใช่ตัวแทนเนื้อใบ
ATTENDED: ขั้นควบคุม (confirm case) -- เข้าเกมด้วย **ปุ่มกลางของ 5 ปุ่มล่าง** (ห้ามปุ่มซ้ายสุด) -> ยืนยันคอนโซลมี `GM_WARP_SEND_OBSERVERS <outcome>` หนึ่งบรรทัดต่อการเชื่อมต่อ (ไม่มี = **กล่อง STOP ข้อ 3 · FINDING ใหม่ ไม่ใช่ FAIL เงียบ ๆ**) -> ถ่าย `S0-BEFORE` + NO-CRASH check ด้วย**คลิกขวาค้างลาก**เท่านั้น (ห้าม Q/E) -> คลิกช่องแชทยืนยัน focus ด้วยตา (พิมพ์ตอนไม่โฟกัส = กลายเป็นฮอตคีย์) พิมพ์ `/warp <ฉากอื่น>` เป๊ะ ห้ามเติมอักษร **ปล่อยให้จอเปลี่ยนฉากจริงก่อน** ถ่าย `S1-ARRIVED` แล้วค่อยปิดไคลเอนต์ -> **รีสตาร์ตเซิร์ฟเวอร์ก่อนเสมอ** (ชี้ไฟล์ DB เดิม) แล้วเปิดไคลเอนต์ใหม่ ถ่าย `S2-RELOG-CONFIRM`
ATTENDED: ขั้นล้มเหลว (fail case) -- พิมพ์ `/warp <ฉากอื่น>` แล้ว **End Task ไคลเอนต์ทันทีที่กด Enter** ก่อนเห็นจอเปลี่ยน -> รีสตาร์ตเซิร์ฟเวอร์ (ไฟล์เดิม) -> relog อ่านฉากบนจอ ถ่าย `S3-RELOG-FAIL-<i>` · ทำซ้ำจนได้ทั้งสองผลอย่างละครั้ง **ไม่เกิน 6 รอบบูต** · 🔴 **ขั้น 5b เกิดได้เฉพาะรอบที่ End Task ไม่ทัน คือ ไคลเอนต์ยังเปิดอยู่และยังคุมตัวละครได้ และคอนโซลขึ้น `GM_WARP_SCENE_ROLLED_BACK`** -- รอบนั้น **อย่าเพิ่งปิดไคลเอนต์**: อ่านแถว `character_positions` เก็บไว้ก่อน -> เดินหนึ่งก้าว**ให้ไกลพอ** -> อ่านแถวอีกครั้ง -> ถ่าย `S4-AFTER-ONE-STEP` · **เดินหลัง relog ในเซสชันใหม่ไม่ใช่ขั้น 5b** และห้ามนับ
ATTENDED: ดูเฟรม/ค่าอะไร -- คอนโซล: `GM_WARP_SEND_OBSERVERS` หนึ่งบรรทัดต่อการเชื่อมต่อ (W1) · `SEND_FAILED <label> <exception!r>` ตามด้วย `GM_WARP_SCENE_ROLLED_BACK` หรือ `GM_WARP_SCENE_ROLLBACK_FAILED` (W2) · กรณีสำเร็จ**ต้องไม่มีทั้ง `SEND_FAILED` และ `GM_WARP_SCENE_ROLLED_BACK`** (W3) · DB: อ่าน `character_positions` ตรงจากไฟล์**หลัง**ทุกบูต (W4) และคู่ก่อน/หลังเดินของขั้น 5b (W6) · W5: sha canonical ก่อน=หลัง ตรง `CANON_SHA.txt` · `integrity_check = ok` · `sessions` +1 ต่อการล็อกอิน · `lease_generation` **ไม่ถอยหลัง** · ไม่มี traceback · จอ: ฉากที่ตัวละครยืนจริงทีละรอบเป็นตาราง (C1/C2) + สีป้ายทุกป้ายทุกภาพ บรรทัดละหนึ่งป้าย "none" ถ้าไม่มี (C3)
ATTENDED: ผ่าน/ไม่ผ่านตัดสินจากอะไร -- **PASS** = ได้ทั้ง confirm case และ fail case อย่างละครั้ง W2/W3/W4 ตรงกับ C1/C2 ที่เก็บ**แยกกัน** **และ** ขั้น 5b เกิดจริงโดย W6 ผ่าน: `scene_id` = **ฉากก่อนวาป** อย่างเดียว ห้ามผูกกับพิกัด (พิกัดจะเป็นพิกัดใหม่ที่เพิ่งเดิน นั่นถูกแล้ว) · 🔴 **ด่านกันผลลวง**: แถวหลังเดิน**เหมือนแถวก่อนเดินทุกช่อง** = ไคลเอนต์ขยับไม่พอ ไม่มีการเขียน ⇒ **ไม่นับว่า 5b เกิด** เดินใหม่ให้ไกลขึ้น · **FAIL** = เจอ `GM_WARP_SCENE_ROLLBACK_FAILED` หรือฉากบนจอขัดกับแถว DB หรือ W6 = ฉากปลายทาง · 5b ไม่เคยเกิด = **`PARTIAL (D-2 NOT-EXERCISED)`** 🔴 ห้ามพิมพ์คำว่า `PASS` ที่ไหนในหัวใบตอนนั้น · ครบ 6 บูตยังไม่เจอกรณีที่สอง = `NO-RESULT` · ไม่มี `OBSERVER_CONFIRMED: <ISO+07:00>` = `AWAITING-OBSERVER` · teardown เสมอ (boot stamp <= 420 นาที)
HEADLESS_PROOF: GM_WARP_SEND_OBSERVERS installed -- 2026-09-07 -- pirate-force-server 34d439a -- python3 -m pytest tests/test_connection_lifecycle.py -k real_session_carries_both_send_outcome_observers -q -s

- ทำไมใบนี้ถึงมีอยู่ (ประวัติ ไม่ลบ ขีดฆ่าแทน): ~~`pirate-force-server#806` เปิดอยู่ ยังไม่ merge (`mergeable_state: unstable`) และมันคือ PR เดียวที่มีบรรทัด `runtime.py:1599` เรียก `warp_send_watch.install_send_outcome_observers(self)` -- ก่อนบรรทัดนี้ขึ้น `main` ฟังก์ชันทั้งชุด (`gm/warp_send_watch.py`, `gm/warp_scene_persist.py`) มีชีวิตอยู่แค่ในเทสของสายนี้~~ **← จริงตอนเขียนใบ 08:52 · หักล้างแล้ว 08:58 ตาม `0948` บรรทัด 20** · เหตุผลที่ใบถูกตั้งเลขก่อนบูตได้ยังเหมือนเดิม: ไม่ให้คำขอตายที่รอยต่อ (`COO 20260904_2142` / `AGENTS.md` §7) แบบเดียวกับ `GT-253`/`GT-255`

- objective (ข้ออ้างเดียว): เมื่อเฟรม `TeleportVital` ของคำสั่ง `/warp <n>` ที่เพิ่งเขียนแถว `character_positions` ปลายทางแบบถาวรแล้ว **ไม่ไปถึงไคลเอนต์จริง** (ซ็อกเก็ตตายในช่วงระหว่างเขียน DB กับส่งเฟรม) แถวย้อนกลับไปฉากก่อนวาปจริง -- และเมื่อเฟรม **ไปถึงจริง** แถวต้อง **ไม่** ย้อน แม้จะมี disconnect อื่นที่ไม่เกี่ยวข้องตามมาทันที (= ข้อบกพร่อง D1 ที่ pf-adversary จับได้และ `#804` แก้แล้ว **ในเทส** · ใบนี้คือครั้งแรกที่มีตาคนยืนยันบนจอ)

- db (สำเนาเสมอ ห้ามเปิด canonical):
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-258_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt258_<yyyyMMdd_HHmmss>.sqlite3
```
  🔴 **คัดลอกครั้งเดียวต่อรอบ** -- ทุกรอบย่อย (kill ไคลเอนต์ → รีสตาร์ตเซิร์ฟเวอร์ → เปิดไคลเอนต์ใหม่) ต้องชี้ **ไฟล์ run-copy เดิม** · คัดลอกใหม่กลางรอบ = ตำแหน่งกลับจุดเกิด และหลักฐานการย้อน/ไม่ย้อนหายทั้งใบ
  🔴 ชื่อสำเนา **ห้ามเป็น** `pirateforce.sqlite3` และ **ห้ามมี `~`** (เกต `_speed_db_is_canonical` ของเส้นทางคำสั่ง GM · [วัดแล้ว · `GAME_TEST_QUEUE.md:12122`])
  sha256 canonical ตรง `CANON_SHA.txt` ก่อนและหลัง · `PRAGMA integrity_check = ok` ทั้งสองครั้ง

- server args (บูตมาตรฐาน ไม่มีแฟล็ก scenario · **ด่านก่อนบูตอยู่บรรทัดที่สอง**):
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
git grep -n "install_send_outcome_observers" -- src/pirateforce_foundation/runtime.py
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt258_<stamp>.sqlite3 2>&1
```
  บัญชี GM จาก `config/gm_accounts.json` (หรือสำเนาผ่าน `PF_GM_ACCOUNTS_CONFIG` -- ห้ามแก้ไฟล์จริง) · เก็บ stdout+stderr รวมกัน (โทเคนเลนนี้ออกทาง stderr)

- steps (playbook `ATTENDED_SESSION_RUNBOOK.md` · อัดวิดีโอต่อเนื่องตลอด `LOCK_GAME`):
  0. **ด่านก่อนบูต**: `git grep` ข้างบนต้องเจอบรรทัดเรียก `install_send_outcome_observers` ใน `runtime.py` บนคอมมิตที่จะบูต · **ไม่เจอ = `[BLOCKED]` บันทึก "รอ #806" ข้ามใบนี้ ไม่ใช่ FAIL ไม่ใช่ NO-RESULT** · ถือ `LOCK_GAME` · boot stamp · sha canonical · คัดลอก DB ครั้งเดียว
  1. เซิร์ฟเวอร์ก่อนไคลเอนต์เสมอ → เข้าเกม (ปุ่มกลางของ 5 ปุ่มล่าง ห้ามปุ่มซ้ายสุด) · ยืนยันคอนโซลมี `GM_WARP_SEND_OBSERVERS <outcome>` **หนึ่งบรรทัดต่อการเชื่อมต่อ** · ไม่มี = ดูกล่อง STOP ข้อ 3
  2. **T0** -- ยืนนิ่ง ถ่าย `S0-BEFORE` เต็มความละเอียด · จดฉากที่ยืน + พิกัด HUD + **ทุกป้ายในเฟรม บรรทัดละหนึ่งป้าย** ("none" ถ้าไม่มี) · NO-CRASH check = **คลิกขวาค้างลาก** (กล้องอย่างเดียว ทิศทางตัวละครไม่ขยับ ไม่มีไบต์ออกสาย) · 🔴 **ห้ามใช้ `Q`/`E` เป็น NO-CRASH check**
  3. **ขั้นควบคุม (confirm case)** -- คลิกช่องแชท ยืนยันโฟกัสด้วยตา พิมพ์ `/warp <ฉากอื่น>` ตามปกติ **ปล่อยให้จอเปลี่ยนฉากจริงก่อน** ถ่าย `S1-ARRIVED` แล้ว **ค่อย** ปิดไคลเอนต์ทันที (จำลอง disconnect ที่ไม่เกี่ยวข้อง)
     🔴 `/warp <n>` เป็นคำสั่ง GM **ไม่ใช่ทริกเกอร์แชท 12 ตัวอักษร ห้ามเติมอักษรให้ครบ 12** · **ห้ามพิมพ์อักษรใดขณะช่องแชทไม่โฟกัส** (กลายเป็นฮอตคีย์)
  4. **รีสตาร์ตเซิร์ฟเวอร์ก่อนเสมอ** แล้วค่อยเปิดไคลเอนต์ใหม่ (เซิร์ฟเวอร์ยังถือเซสชันเดิมหลัง kill ไคลเอนต์ · ไม่รีสตาร์ต = ตัวถัดไปค้าง "connecting" ตลอดกาล) · ชี้ไฟล์ DB เดิม · relog แล้ว **อ่านฉากที่ตัวละครยืนจริงบนจอ** ถ่าย `S2-RELOG-CONFIRM` + จดป้ายทุกป้าย
  5. **ขั้นทดลองความล้มเหลว (fail case)** -- พิมพ์ `/warp <ฉากอื่น>` แล้ว **End Task ไคลเอนต์ทันทีที่กด Enter** ก่อนเห็นจอเปลี่ยนฉากเลย → รีสตาร์ตเซิร์ฟเวอร์ → เปิดไคลเอนต์ใหม่ (DB ไฟล์เดิม) → อ่านฉากบนจอ ถ่าย `S3-RELOG-FAIL-<i>` + จดป้าย
     🔴 **บังคับคนไม่ได้ว่าจะติดจังหวะไหน -- นี่คือข้อจำกัดของใบนี้ ไม่ใช่ความผิดพลาดของผู้ทดสอบ**: อาจสุ่มได้ทั้งสองผล เซิร์ฟเวอร์อาจส่งเฟรมทันจริง (ได้ confirm case ซ้ำ) หรือซ็อกเก็ตตายก่อนส่ง (ได้ fail case) · **บันทึกผลที่คอนโซลบอกจริง ไม่ใช่ผลที่ตั้งใจจะเทส**
  5b. 🔴 **ขั้นบังคับเมื่อไคลเอนต์ยังไม่ตาย** (เติมโดย LANE-GM รอบ `0dlc07` ตาม `COO-DECISION 20260905_1150` ข้อ 3(ข) -- "ไม่งั้น PASS ทั้งที่พัง") -- ในรอบย่อยใด ๆ ของข้อ 5 ที่คอนโซลพิมพ์ `GM_WARP_SCENE_ROLLED_BACK` **แล้วไคลเอนต์ยังเปิดอยู่ ยังคุมตัวละครได้** (End Task ไม่ทัน / กดช้าไปเสี้ยววินาที / ซ็อกเก็ตล้มเฉพาะเฟรมนั้นแต่การเชื่อมต่อไม่ตาย):
     (i) **อย่าเพิ่งปิดไคลเอนต์** อ่าน `character_positions` ทันทีหนึ่งครั้ง (= แถวหลัง undo)
     (ii) **เดินหนึ่งก้าว** (กดปุ่มเดินสั้น ๆ ให้ตัวละครขยับจริงบนจอ ห้ามวาปซ้ำ ห้ามพิมพ์คำสั่ง) ถ่าย `S4-AFTER-ONE-STEP`
     (iii) อ่าน `character_positions` **อีกครั้ง** แล้วจดคู่กับบรรทัดคอนโซล
     เหตุผล: undo ที่สำเร็จอาจถูกลบล้างโดยเฟรมเดินถัดไป (`runtime.py:4164` เขียนทับด้วย `selected.position` ที่ `scene_id` ถูก relabel ไปฉากปลายทางตั้งแต่ `runtime.py:6827` และไม่มีใครคืน) -- ขั้นนี้คือทางเดียวที่ผู้เทสมีตาเห็นเรื่องนั้นได้ · **ทำไม่ได้เพราะไคลเอนต์ตายไปแล้วทุกรอบ = เขียน `D-2 NOT-EXERCISED` ในผล ไม่ใช่ข้ามเงียบ ๆ**
  6. ทำซ้ำข้อ 5 จนกว่าจะเจอทั้งสองผลอย่างละครั้ง · **ไม่เกิน 6 รอบบูต** แล้ว STOP แบบ `NO-RESULT` เฉพาะกรณีที่ยังไม่เจอ (อีกกรณีที่เจอแล้วยังนับเป็นผล)
  7. ทุกรอบย่อย: อ่าน `character_positions` ตรงจากไฟล์ DB **หลัง** แต่ละบูต แล้วจดคู่กับบรรทัดคอนโซลของรอบนั้น
```
py -3 -c "import sqlite3;print(sqlite3.connect(r'state\run_gt258_<stamp>.sqlite3').execute('select * from character_positions').fetchall())"
findstr /N /C:"GM_WARP_SEND_OBSERVERS" /C:"SEND_FAILED" /C:"GM_WARP_SCENE_ROLLED_BACK" /C:"GM_WARP_SCENE_ROLLBACK_FAILED" /C:"LANE_GM_CHAT_ACTION" server_console_live.*.txt
```
  8. NO-CRASH check ครั้งสุดท้าย · logout → teardown ด้วย `TEMPLATE_teardown_generic.ps1` (**boot stamp ต้องไม่เกิน 420 นาที** · รอบที่จบเพราะเลิกเล่นก็ต้อง teardown) → เทียบ sha canonical → sha256 ทุกภาพ

- pass criteria (สองชั้น 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น**):
    wire/DB (อ่านคอนโซลเซิร์ฟเวอร์ + ไฟล์ DB · ไม่ต้องมีตาคน):
      W1. ตอนล็อกอิน: `GM_WARP_SEND_OBSERVERS <outcome>` **หนึ่งบรรทัดต่อการเชื่อมต่อ** (จาก `warp_send_watch.INSTALL_CONSOLE_TOKEN` ที่มาจาก `runtime.py:1599`) = ยืนยันว่า hookup มีจริงบน **build ที่กำลังเทส** ไม่ใช่แค่บน `main` เฉย ๆ
      W2. กรณีส่งไม่สำเร็จ: v141 send loop พิมพ์ `SEND_FAILED <label> <exception!r>` (label = `warp_scene_persist.SEND_FAILURE_WARP_ACTION_LABEL`) ตามด้วย `GM_WARP_SCENE_ROLLED_BACK` (สำเร็จ) หรือ `GM_WARP_SCENE_ROLLBACK_FAILED scene=<n> reason=<...>` (ล้ม -- **เจอแบบนี้ = FAIL ทันที ไม่ใช่แค่บันทึกไว้**)
      W3. กรณีส่งสำเร็จ: **ไม่มี** `SEND_FAILED` และ **ไม่มี** `GM_WARP_SCENE_ROLLED_BACK` เลยสักบรรทัด
      W4. `character_positions` ของบัญชีทดสอบ อ่านตรงจาก DB **หลัง** แต่ละบูต ต้องตรงกับผลที่คอนโซลบอกเป๊ะ (ย้อน = ฉากก่อนวาป · ไม่ย้อน = ฉากปลายทาง) -- **ไม่มีฉากที่สามที่ไม่มีใครทำนาย**
      W5. sha canonical ก่อน=หลัง ตรง `CANON_SHA.txt` · `integrity_check = ok` · บูตบนสำเนาเสมอ · `sessions` +1 ต่อการล็อกอิน · `lease_generation` ไม่ถอยหลัง · ไม่มี traceback
      W6. **(ขั้น 5b เท่านั้น -- เติมโดย LANE-GM รอบ `0dlc07` ตาม `COO 1150` ข้อ 3(ข) · 🔴 **แก้เกณฑ์รอบเดียวกันตาม `pf-adversary` D2 ซึ่งวัดจริงบน fixture ของสายนี้ว่าเกณฑ์ร่างแรกไปไม่ถึงทั้ง PASS และ FAIL**)** หลัง `GM_WARP_SCENE_ROLLED_BACK` แล้วเดินหนึ่งก้าว **ตัดสินที่ `scene_id` อย่างเดียว ห้ามผูกกับพิกัด**: `scene_id` = **ฉากก่อนวาป** ⇒ ผ่าน · `scene_id` = **ฉากปลายทาง** ⇒ **FAIL (D-2 ยืนยันบนจอ)** 🔴 **พิกัดจะเป็นพิกัดใหม่ที่เพิ่งเดินไป ไม่ใช่พิกัดก่อนวาป -- นั่นคือพฤติกรรมที่ถูก** (วัดแล้ว `pf-adversary` รอบ `0dlc07`: เฟรมเดินเขียน `candidate` ที่เอา `scene_id` จาก `selected` แต่เอา x/y/z จากรายงานของไคลเอนต์ ⇒ สภาพที่พังจริงคือ `(ฉากปลายทาง, พิกัดใหม่)` ไม่ใช่ `(ฉากปลายทาง, พิกัดก่อนวาป)` ที่ร่างแรกเขียนไว้) · 🔴 **ด่านกันผลลวง**: ถ้าแถวหลังเดิน **เหมือนแถวก่อนเดินทุกช่อง** แปลว่าไคลเอนต์ขยับไม่พอจนไม่มีการเขียนเลย (`candidate != selected.position` ไม่จริง) ⇒ **ไม่นับว่าขั้น 5b เกิด** ให้เดินใหม่ให้ไกลขึ้น หรือบันทึก `D-2 NOT-EXERCISED` ห้ามอ่านว่าผ่าน · ขั้น 5b ไม่เคยเกิดเลย (ไคลเอนต์ตายทุกรอบ) = `D-2 NOT-EXERCISED` เขียนออกมาเป็นบรรทัดในผล
      🔴 **ชั้นนี้ตอบไม่ได้ว่าคนเห็นอะไรบนจอ** -- ห้ามใช้แทนชั้นล่าง
    client-observable (🔴 ต้องมีตาคน ห้ามอนุมานจากคอนโซล):
      C1. **ขั้นควบคุม**: จอเปลี่ยนฉากจริงก่อนปิดไคลเอนต์ (ระบุชื่อฉาก/สิ่งที่เห็น) แล้ว relog **ต้องยังอยู่ฉากปลายทาง** -- นี่คือสิ่งที่ D1 เคยพังมาก่อน `#804`
      C2. **ขั้นทดลองความล้มเหลว**: relaunch แล้วอ่าน **ฉากที่ตัวละครยืนจริงบนจอ** ทีละรอบ เทียบกับที่คอนโซลบอกไว้ก่อนปิด -- เขียนเป็นตารางรอบต่อรอบ (รอบที่ / กดอะไร / เห็นอะไรก่อนปิด / เห็นอะไรหลัง relog)
          ช่องอ่านผลเสริมบนจอ **[วัดแล้ว: `GT-245` ครึ่งแรก PASS R315 -- `/warp 2` แล้ว relaunch ทำให้หน้าเลือกตัวละครพิมพ์ "Prison Exile Island"]** · **[เสนอ]** ใช้ข้อความบนหน้าเลือกตัวละครเป็นการอ่านฉากครั้งที่สองได้ ถ้าปลายทางเป็นฉาก 2 -- **บันทึกทั้งสองที่ ห้ามใช้แทนการเข้าเกมจริง**
      C3. **บรรทัดสีป้ายครบทุกป้ายทุกภาพ** (ข้อบังคับ R163 คำสั่ง Panya 2026-08-25): หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ · "none" เขียนออกมา ไม่เว้นว่าง · อ่านจาก **ภาพนิ่งเต็มความละเอียด** เท่านั้น (ห้าม contact sheet / ภาพย่อ / วิดีโอ) · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (`RE-067` เป็นเจ้าของคำถามนั้น) · ต่างจากภาพเซิร์ฟเวอร์เดิม = ลง `REAL_SERVER_DIVERGENCE.tsv` แถวละหนึ่งข้อ
      C4. NO-CRASH check ผ่านทุกครั้งที่กำหนด
      **`OBSERVER_CONFIRMED: <ISO+07:00>` เป็นข้อบังคับแข็งของชั้นนี้ (G-OBS) -- ไม่มี = ชั้นนี้ไม่ PASS** · รันจบแต่ไม่มีลายเซ็นตาคน = `AWAITING-OBSERVER` ไม่ใช่ PASS ไม่ใช่ FAIL
      C5. **(ขั้น 5b)** ภาพ `S4-AFTER-ONE-STEP` ต้องแสดงว่าตัวละคร **ขยับจริง** และผู้เทสระบุด้วยตาว่ายืนอยู่ฉากไหน -- เทียบกับแถว DB ของ W6 แยกกัน ห้ามอนุมานจากกัน · บรรทัดสีป้ายครบทุกป้ายเหมือนภาพอื่น
    การอ่านผล: **PASS** = ได้ทั้ง confirm case และ fail case อย่างละหนึ่งครั้ง และทั้งสองครั้ง W2/W3/W4 ตรงกับ C1/C2 ที่เก็บแยกกัน **และ** ขั้น 5b เกิดขึ้นจริงอย่างน้อยหนึ่งครั้งโดย W6/C5 ผ่าน · 🔴 **ห้ามเขียน PASS เมื่อขั้น 5b ไม่เคยเกิด** -- หัวใบต้องเขียนสถานะว่า **`PARTIAL (D-2 NOT-EXERCISED)`** เท่านั้น (เกณฑ์เดิมผ่านครบ แต่ใบยังไม่ได้พิสูจน์ว่า undo อยู่รอดถึงก้าวถัดไป) `COO 1150` ข้อ 3(ข) · 🔴 **ห้ามใช้คำว่า `PASS` ที่ไหนก็ตามในหัวใบตอนนั้น** และห้ามเขียน `PASS-PARTIAL`: `tools_bridge/pf_queue_status.py` จับสถานะจากหัวใบด้วย regex ที่ `PASS` ชนะตำแหน่งซ้ายสุด ⇒ ใบจะถูกรายงานว่า `PASS` และหลุดออกจากดัชนีใบที่ยังเปิด (วัดแล้ว `pf-adversary` รอบ `0dlc07`: ร่างแรก `PASS (D-2 NOT-EXERCISED)` ถูก tooling แปลงเป็น `PASS` เต็มตัว) · `PARTIAL` อยู่ใน regex อยู่แล้วและ **ไม่อยู่ใน** `CLOSED` · **FAIL** = เจอ `GM_WARP_SCENE_ROLLBACK_FAILED` หรือฉากบนจอขัดกับแถว DB หรือ W6 เป็นฉากปลายทาง · **NO-RESULT** = ครบ 6 รอบบูตแล้วยังไม่เจอกรณีที่สอง (บันทึกกรณีที่เจอไว้เป็นผลจริง) · **ผลลบมีค่าเท่าผลบวก**: ไม่มีการย้อนเลยทั้งที่ `SEND_FAILED` ขึ้น = redirect ไปที่ลำดับ hook ใน `warp_send_watch.py` ไม่ใช่ที่ `warp_scene_persist.py`

- predictions (ทายผิด = finding ไม่ใช่ความล้มเหลว):
  - P1 [เสนอ]: confirm case = ไม่มี `SEND_FAILED` เลย และ relog อยู่ฉากปลายทาง
  - P2 [เสนอ]: fail case จะเจอภายใน 6 รอบ และคอนโซลจะพิมพ์ `SEND_FAILED` ตามด้วย `GM_WARP_SCENE_ROLLED_BACK`
  - P3 [ตัวหักล้าง]: End Task ทันทีที่กด Enter ยังทัน "ส่งสำเร็จ" ทุกครั้ง ⇒ ใบนี้บังคับ fail case ไม่ได้จากหน้าจอ = ข้อจำกัดที่ต้องเขียนลงผล และ redirect ไปหาวิธีอื่นที่ไม่ใช่ attended

- nonclaims:
  1. ไม่ตอบคำถาม thread/lock ของ `send_lock` vs `heartbeat_worker` (`20260905_0554` ครึ่งหลัง) -- ใบนั้นตอบแล้วว่า "ไม่มีคำถามกลับ" (`store.connect` เปิด-ปิดต่อคอล) แต่ไม่มีใครวัดบนจอว่าจริงภายใต้ภาระจริง **ใบนี้ไม่ใช่ใบนั้น** (เจ้าของ = LANE-GM รอบ 11:11 ตาม `0948` ข้อ 2(ข))
  2. ไม่ประกาศไมล์สโตนใดขยับ (M2/M3/M4/P-1/P-2/P-3)
  3. ไม่ตัดสินว่า design "replace ไม่ใช่ queue" ของ `park_warp_send` เมื่อมีหลาย `/warp` ค้างพร้อมกันถูกไหม (ปิดแยกไปแล้วโดย `DoubleWarpTests` · `COO-DECISION 20260905_0345` ข้อ 3) -- ใบนี้ทดสอบ **วาปเดียวต่อบูต**
  4. ไม่ตัดสินสาเหตุของสีป้ายใด ๆ (`RE-067`)
  5. ไม่มีการตีมอน
  6. ~~🔴 **ไม่ทดสอบ pf-adversary D-2**~~ **← แก้แล้วโดย LANE-GM รอบ `0dlc07` (`COO-DECISION 20260905_1150` ข้อ 3(ข)): ใบนี้ **ทดสอบ D-2 แบบมีเงื่อนไข** ผ่าน **ขั้น 5b + W6 + C5** และห้าม PASS เปล่าเมื่อขั้นนั้นไม่เกิด (`PASS (D-2 NOT-EXERCISED)`) · ข้อความเดิมด้านล่างเก็บไว้เป็นประวัติ เพราะเหตุผลทางเทคนิคของมันยังจริง (บังคับ fail case ให้ไคลเอนต์รอดไม่ได้จากหน้าจอ) -- สิ่งที่เปลี่ยนคือ **ไม่ปล่อยให้ข้อจำกัดนั้นกลายเป็น PASS เงียบ ๆ** อีก · 🔴 **และข้อความเดิมมีตัวเลขผิดหนึ่งจุด อ่านตามไม่ได้**: ที่เขียนว่าแถวจะกลายเป็น "ฉากปลายทาง + **พิกัดก่อนวาป**" นั้น**เขียนไม่ได้เลย** เพราะ `runtime.py:4164` เขียนใต้ `elif candidate != selected.position:` ⇒ พิกัดไม่เปลี่ยน = ไม่มีการเขียน · สภาพที่พังจริงคือ **ฉากปลายทาง + พิกัดใหม่ที่เพิ่งเดินไป** (วัดแล้ว `pf-adversary` รอบ `0dlc07`: `scene_id=2 x=-9234.957`) ⇒ **ตัดสินที่ `scene_id` อย่างเดียว ดู W6**:** (round `j2jluj`: undo ที่ **สำเร็จ** ถูกลบล้างด้วยก้าวเดินถัดไปของผู้เล่น --
     `rollback_warp_scene` คืน `selected` เป็น snapshot ที่ `scene_id` ถูก resync ไปฉากปลายทางแล้วตั้งแต่ก่อนส่ง
     [`runtime.py:6827`], ไม่มีใครคืนป้ายฉากนั้น ⇒ เฟรมเดินถัดไปเขียนถาวรเป็น **ฉากปลายทาง + พิกัดก่อนวาป** --
     แย่กว่าทั้งแถวก่อนวาปและแถวปลายทาง) **โดยตั้งใจ**: วิธีวัด fail case ของใบนี้ (ข้อ 5, End Task ทันทีที่กด
     Enter) ตัดการเชื่อมต่อทิ้งเพื่อจำลอง send ล้ม ⇒ ไม่มีทางมีเฟรมเดินถัดไป**ในเซสชันเดียวกัน**หลัง rollback ให้วัด
     -- D-2 ต้องการบิลด์ที่ทำให้ `sendall` ล้มโดยที่ซ็อกเก็ต**ไม่**ตาย (เช่น drop แพ็กเก็ตชั่วคราวที่ไม่ทำให้
     disconnect) ซึ่งนอกเขตของ attended รอบนี้ · **ถ้าเจอโดยบังเอิญ**: หลัง `GM_WARP_SCENE_ROLLED_BACK` ถ้าไคลเอนต์
     ยังไม่ตายและมีเฟรมเดินอีกอย่างน้อยหนึ่งครั้งก่อนปิด ให้อ่าน `character_positions` อีกรอบทันที -- เจอ
     `scene_id` = ฉากปลายทาง **พร้อมกับ** พิกัดที่ไม่ใช่ของฉากนั้น (พิกัดก่อนวาป) = D-2 ยืนยันบนจอ บันทึกเป็น
     FAIL แยกจากเกณฑ์ข้างบน ไม่ใช่ NOT-EXERCISED · ~~จุดแก้อยู่ใน `runtime.py` = เขตของ chief~~ · คำถามออกแบบ
     ("แถวไหนคือผู้มีอำนาจของ undo และใครคืนป้ายฉากใน `selected` หลัง rollback") อยู่ใน
     `notes_to_chief/20260905_1105_LANE-GM-ASK-COO-which-position-is-the-undo-authority.md`
     🔴 **ขีดฆ่า 2026-09-05T16:2x+07:00 (LANE-GM รอบ `bdl0w3`) -- จุดแก้ไม่ได้อยู่ใน `runtime.py`**: chief ตัดสิน
     (`notes_to_chief/20260905_1522_CHIEF-TO-LANE-GM-core-request-gm-059-jurisdiction-yours-not-mine.md`)
     ว่า `CORE-REQUEST-GM-059` เป็นของ LANE-GM เอง เพราะบรรทัดที่ต้องเขียนอยู่ใน `gm/warp_send_watch.py`
     ทั้งหมด · **ครึ่งเซิร์ฟเวอร์ลงแล้ว** (`_restore_selected_scene` เรียกบนกิ่ง `OUTCOME_ROLLED_BACK`
     ของ `on_game_frame_send_failed` · PR เซิร์ฟเวอร์ของรอบ `bdl0w3`) พร้อมมิวแทนต์ที่ฆ่าได้จริงผ่าน
     `runtime.dispatch` จริง (`tests/test_gm_warp_send_watch.py::RealDispatchSendFailureTests`)
     🔴 **เกณฑ์ W6 ไม่เปลี่ยนแม้แต่ตัวเดียว และใบนี้ยังต้องรัน**: ครึ่งเซิร์ฟเวอร์เป็น headless
     ไม่ใช่หลักฐานบนจอ · ถ้าขั้น 5b เกิดจริงแล้ว W6 ยังอ่านได้ **ฉากปลายทาง** = ตัวแก้ไปไม่ถึงเส้นทางจริง
     (redirect ไปที่ลำดับ hook ใน `warp_send_watch.py` ตามบรรทัด "ผลลบมีค่าเท่าผลบวก" ข้างบน) · ห้ามอ่านว่า
     "แก้แล้วไม่ต้องรัน"

- STOP:
  1. **STOP ถ้าไคลเอนต์ปิดตัวเองนอกจังหวะที่ใบสั่งให้ปิด** -- บันทึกว่าหยุดที่ขั้นไหน แล้ว teardown อยู่ดี
  2. STOP ถ้าเจอ `ErrorData` ใด ๆ ที่ไม่เกี่ยวกับใบนี้
  3. STOP ถ้าคอนโซล **ไม่มีบรรทัดใดในสี่บรรทัดที่กำหนดเลย** หลังทำตามขั้นตอน -- แปลว่า observer ไม่ได้ถูกเรียกจริง (hookup อาจ merge แต่ path การเรียกไม่ตรงที่คาด) ⇒ **FINDING ใหม่ ไม่ใช่ FAIL เงียบ ๆ**
  4. ~~STOP ก่อนบูตถ้า `#806` ยังไม่ merge~~ **← ปลดแล้ว** (`COO-DECISION 20260905_0948` บรรทัด 20 · `NOW.md:3`) · เหลือเป็น **ด่านก่อนบูตข้อ 0** (`git grep`) ซึ่งเป็นการวัดจริงบนคอมมิตที่จะบูต ไม่ใช่การอ้างจดหมาย

- links: `notes_to_chief/20260905_0852_LANE-GM-GT-TICKET-REQUEST-warp-send-failure-rollback-on-screen.md` (ใบต้นเรื่อง · เนื้อเต็ม) · `notes_to_chief/20260905_0948_COO-DECISION-*.md:20` (STOP ปลด) · `NOW.md:3` (บล็อก 09:48) · `pirate-force-server#806` (GM-058 hookup · `runtime.py:1599`) · `pirate-force-server#804` (D1 fix · merged `b2ea1a0`) · `src/pirateforce_foundation/gm/warp_send_watch.py` (`on_game_frame_sent`, `on_game_frame_send_failed`, `install_send_outcome_observers`, `INSTALL_CONSOLE_TOKEN`) · `src/pirateforce_foundation/gm/warp_scene_persist.py` (`rollback_warp_scene_on_send_failure`, `ROLLBACK_CONSOLE_TOKEN`, `ROLLBACK_FAIL_CONSOLE_TOKEN`, `SEND_FAILURE_WARP_ACTION_LABEL`) · `tests/test_gm_warp_send_watch.py` · `notes_to_chief/20260905_0719_LANE-GM-REPORT-COO-second-layer-built-in-zone-one-line-left.md` · `ATTENDED_SESSION_RUNBOOK.md` + `BRIDGE_BOOT_PROCEDURE.md`

- result:
  (ว่าง -- ผู้เทสกรอก **แยกสองชั้น · ชั้นไหนไม่ได้วัดเขียน `NOT MEASURED`**: PASS / `PARTIAL (D-2 NOT-EXERCISED)` / FAIL / NO-RESULT / AWAITING-OBSERVER · branch+commit ที่บูต · ผลของ `git grep` ด่านข้อ 0 · ตารางรอบย่อยทุกรอบ · บรรทัดคอนโซลดิบทุกบรรทัดจาก `findstr` · ผลอ่าน `character_positions` หลังทุกบูต **และคู่ก่อน/หลังเดินหนึ่งก้าวของขั้น 5b ถ้าเกิดขึ้น** · ภาพ `S0`-`S3` (+ `S4-AFTER-ONE-STEP` ถ้าขั้น 5b เกิดขึ้น) + sha256 · **บรรทัดสีป้ายครบทุกป้ายทุกภาพ** · sha canonical ก่อน/หลัง · `integrity_check` · NO-CRASH/CRASH · teardown รันแล้ว · `OBSERVER_CONFIRMED: <ISO+07:00>`)

## numbering
`GT-258`/`RE-258` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*`) ก่อนวาง **[วัดแล้ว รอบนี้]** · ตัวนับร่วมสองคิว + archive คืนสูงสุดที่ `256` (`RE-256`) ⇒ ใบชุดนี้กิน `257`-`258` · ตรวจโดย chief (LANE-E) รอบ `pv4zg1`/R352

---

## GT-262 STALL-AND-GUILD-STORAGE-ATTENDED-CAPTURE-001  [🟢 **READY -- เนื้อใบเต็มลงแล้วโดยเจ้าของใบ (LANE-UI)** · สถานะเปลี่ยนจาก `PENDING` (เลขจองไว้ เนื้อยังว่าง) → `READY` เพราะเนื้อใบมาครบแล้ว (รูปแบบเดียวกับ `GT-230` ที่พลิกจาก `PENDING`→`OPEN` รอบ `ziuhft` เมื่อ LANE-UI เติมเนื้อใบเอง) · คู่กับ `RE-261 STALL-AND-GUILD-STORAGE-FIELD-SEMANTICS-FROM-A-REAL-SESSION-001` (`CLIENT_RE_QUEUE.md:5607`) ตาม `AGENTS.md` §7 (`COO-DECISION 20260904_2142` ข้อ 3: ผล RE ที่ขอ attended capture ⇒ ผู้บริโภคผลเปิดใบ GT รอบเดียวกัน) · เลขตั้งโดย chief (LANE-E) รอบ `pv4zg1`/R352 · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-UI** · ผู้รัน = Panya (attended) · **ต่อท้ายคิว "รอเครื่องคุณ" ไม่ใช่หัวคิว** · ไม่บล็อกใคร · ไม่มีการตีมอน · 🔴 **[LANE-K รอบ `kxpzxi` 2026-09-07T03:15+07:00] ถอนออกจาก `QUEUE_STATUS_SNAPSHOT.md` ชั่วคราว ตาม `PANYA-ORDER 20260907_0159` ข้อ 2** (หน้าที่คัดใบ attended ที่ไม่จำเป็น PANYA `2148` ย้ายมาอยู่กับ LANE-K): ใบนี้เข้าเกณฑ์ (ก) **อายุ >7 วัน** (เปิด 2026-08-25 = 13 วัน) และเป็นหนึ่งใน ใบที่เจ้าของยกเป็นหลักฐานในคำสั่งเอง · **K ยกเลิกใบเองไม่ได้ (พับ=คัดลอก)** — ใบยังเปิดอยู่ทุกตัวอักษร ไม่มีอะไรถูกลบ · **เจ้าของใบ LANE-UI ต้องตอบกลับ: ยืนยันซ้ำว่ายังต้องบูตจริง (แล้ว K ใส่กลับรถบัส) หรือยกเลิกพร้อมเหตุผลตามกฎ PANYA `20260903_1934`** · จดหมายแจ้ง: `notes_to_chief/20260907_0315_LANE-K-CULL-3-tickets-off-bus-need-owner-reconfirm.md`]] [🚫 **CANCELLED โดยเจ้าของใบ LANE-UI รอบ `fvp9ke` 2026-09-07T04:56+07:00** — วางโดย LANE-K รอบ `rlapyk` 2026-09-07T06:11+07:00 · K ไม่ได้ยกเลิกเอง (พับ=คัดลอก) · จดหมาย `notes_to_chief/20260907_0456_LANE-UI-TO-K-gt262-cancel-with-reason.md` · บรรทัดของเจ้าของใบคำต่อคำ: "`GT-262` = ยกเลิก (CANCELLED BY OWNER) — K ไม่ต้องใส่กลับรถบัส" · เหตุผลคำต่อคำตามกฎ `PANYA 20260903_1934`: "ไม่มีกลไกให้ 'ติดอาวุธ' ในฉากเป้าหมาย ⇒ **ใบนี้ออก `HEADLESS_PROOF:` ไม่ได้เลยโดยโครงสร้าง** ไม่ใช่เพราะเจ้าของใบขี้เกียจเติม แต่เพราะยังไม่มีอะไรให้ headless พิมพ์ออกมา ... การยืนยันซ้ำจึงเป็นการถือที่นั่งบนรถบัสไว้เฉย ๆ ยกเลิกจึงตรงกว่าและซื่อสัตย์กว่า" · วัดซ้ำหน้างานที่เจ้าของใบยกมา: `grep -rn "Stall\|GuildStorage" src/pirateforce_foundation/ --include=*.py` = 0 hit · `StallOpenVital 0x2A3E`/`StallStartVital 0x30FE`/`StallOperateVital 0x3DE4` = `NAME-ONLY` · `GuildStorageOpenVital 0x5CAD`/`GuildStorageResultVital 0x70D0` = `UNTOUCHED` · **`RE-261` ยังเปิดอยู่ ไม่ได้ถูกยกเลิกไปด้วย** (คำของเจ้าของใบ) · nonclaim ที่ยกมาด้วย: เจ้าของใบไม่ได้อ้างว่า layout ที่รู้แล้ว = WIRED และไม่ได้แตะสถานะใบอื่นที่ K ถอน]

- ทำไมใบนี้ถึงมีอยู่: `RE-261` ปิดจาก static เดี่ยวไม่ได้ (จดหมายต้นทางของมันเองยอมรับ `[NEEDS-ATTENDED-CAPTURE]`) เพราะ opcode ของทั้งสองระบบมีจริงในไบนารีแต่ `external/PF_FIELD_VALIDATION.tsv` ทุกแถวเป็น `NOT_OBSERVED`/`serializer_status=OPEN` — ไม่เคยมีเฟรมจริงจากสองระบบนี้ในคลังแคปเจอร์เลยสักครั้ง · ตาม `AGENTS.md` §7 (`COO-DECISION 20260904_2142` ข้อ 3) ผลของมันต้องมีใบ GT คู่ในรอบเดียวกัน มิเช่นนั้น `RE-261` จะไม่มีวันถูกทดสอบ (ผู้เทสอ่าน `GAME_TEST_QUEUE.md` เท่านั้น ไม่เคยอ่าน `CLIENT_RE_QUEUE.md`) · ใบนี้คือใบนั้น

- objective (ข้ออ้างเดียว): ผูกสิ่งที่คนเห็นบนจอ — หน้าต่างแผงขายเอง/ช่องราคา/หน้าต่างคลังกิลด์/ช่องฝาก-ถอน — เข้ากับเฟรมและ opcode ที่ `RE-261` ระบุ (`StallStartVital 0x30FE` · `StallOpenVital 0x2A3E` · `StallOperateVital 0x3DE4` · `GCSS_GuildStorageOpenVital 0x8B66` · `GCGS_GuildStorageCmdVital 0x7F17`) โดยเรียงลำดับคำถามและด่านกั้นเดียวกับที่ `RE-261` บังคับไว้เป๊ะ (positive control ก่อนอย่างอื่นทั้งหมด) · **ใบนี้ตัดสินแค่ชั้น client-observable เท่านั้น** — คำตัดสินว่าไบต์ `+0x20` (`u32` tag `0x14` ของ `StallOperateVital` serializer `0x76A630`) แปลว่าราคาจริงหรือไม่ (สมมติฐาน chief round 75 · `archive/CHIEF_CONTINUATION_ARCHIVE_20260818_R77.md:64` + `FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md:132` — **[เสนอ] ยังไม่ยืนยัน**) เป็นหน้าที่ของ `RE-261`/LANE-UI ไม่ใช่ของใบนี้

- 🔴 **สองสิ่งที่ยังไม่รู้จริง ณ วันเปิดใบ (ห้ามอ้างว่ารู้แล้ว) — ใบนี้คือใบสำรวจของทั้งสี่ข้อ**:
  ① **ไม่มีพิกัด/ชื่อ NPC หรือปุ่ม UI ตัวไหนที่เปิด "แผงขายเอง" ถูก pin ไว้ในคลังเลยสักตัว** — ใบนี้จึงเป็นใบ**ไล่คลิก** เหมือน `GT-230` P2 ไม่ใช่ใบที่บอกพิกัดตายตัว
  ② **ไม่มีพิกัด/ชื่อ NPC หรือปุ่ม UI ตัวไหนที่เปิด "คลังกิลด์" ถูก pin ไว้เช่นกัน** — ไล่คลิกแยกรอบสอง
  ③ **ไม่มีใครในโปรเจกต์นี้เคยเปิดแผงขายเองหรือคลังกิลด์สำเร็จบนเซิร์ฟเวอร์ของเราเอง (`pirateforce_foundation.app`)** — ไม่มี dispatcher ผูก opcode เหล่านี้ในโค้ดฝั่งเซิร์ฟเวอร์เลย (`external/PF_PROTOCOL_PRIORITY.tsv`: `serializer_status=OPEN` ทุกคลาส ไม่ใช่ `CLOSED`) ⇒ ใบนี้เป็นการทดลองล้วน ไม่ใช่การยืนยันฟีเจอร์ที่ทำงานได้แล้ว
  ④ **ไม่มีใครวัดว่าคลังกิลด์ต้องมีสังกัดกิลด์ก่อนหรือไม่** — ถ้าตัวละครทดสอบไม่มีกิลด์และหน้าต่างคลังเปิดไม่ได้ด้วยเหตุนั้น นี่คือผลลบที่ใช้ได้ (ดูผลลัพธ์ `E` ด้านล่าง) ไม่ใช่ใบล้ม

- 🔴 PRECONDITION ที่ต้องเช็คจริงก่อนขั้น 1:
  P1. **ไม่มีโค้ดฝั่งเซิร์ฟเวอร์จับ opcode กลุ่มนี้เลย** (ตรวจซ้ำหน้างานด้วย `git grep` ในขั้นตอนด่านก่อนบูตด้านล่าง) ⇒ ใบนี้เป็น**ใบเก็บ hex บวกภาพหน้าจอ** ไม่ใช่ใบตัดสินว่าธุรกรรมสำเร็จ (รูปแบบเดียวกับ `GT-230` — "เก็บ hex ไม่ใช่ใบตัดสินว่าขายสำเร็จ") · ไบต์ว่าง/ไม่มีเฟรมออกเลยก็เป็นผลที่ใช้ได้
  P2. **ไอเทมที่ใช้วางในแผง/ฝากคลังไม่ต้องหา — สร้างตัวละครใหม่หนึ่งตัว**: `SQLiteStore._insert_initial_backpack` (`pirate-force-server/src/pirateforce_foundation/store.py:674`, เรียกจาก `store.py:575`) ใส่ของ 4 ชิ้นจาก `INITIAL_BACKPACK` (`inventory.py:39-49`) ให้ทุกตัวละครใหม่เสมอ (`template_id 2600001` x2 ช่อง 0/2 · `2400901` ช่อง 1 · `2200002` ช่อง 3) ⇒ ใช้ตัวละครใหม่ตัวเดียวตลอดใบ ไม่ใช้ตัวเก่าที่เคยเทสอย่างอื่นมาก่อน จะได้ของที่รู้ต้นทางแน่ชัดทั้งสำหรับตั้งราคาในแผงและฝากคลังกิลด์ · ถ้ากระเป๋าตัวใหม่ว่างผิดจากนี้ ⇒ finding ของใบนี้เอง ลองตัวละครใหม่อีกตัว
  P3. **การคลิกตัวเลือก/NPC หนึ่งครั้งไม่จำเป็นต้องเปิดแผง/คลังทันที** — [ทำนายจาก `GT-230` P2/P3 ยังไม่ใช่ผลวัดตรงกับกรณีนี้]: `GT-230` วัดพฤติกรรมนี้กับ NPC ร้านค้าเท่านั้น ยังไม่เคยมีการคลิกอะไรเพื่อหา "แผงขายเอง" หรือ "คลังกิลด์" มาก่อนเลย ⇒ **ไม่ใช่ NPC/ปุ่มทุกตัวเป็นทางเข้าของสองระบบนี้** ต้องไล่คลิกหลายตัว/หลายเมนูจนกว่าจะเจอตัวที่เปิดหน้าต่างที่ถูกต้องจริง
  P4. **เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ** (กฎเดียวกับ `GT-228`/`GT-230`) · ห้ามเปิดไคลเอนต์ทิ้งไว้โดยไม่มีเซิร์ฟเวอร์ (ตายเองใน ~3.5 นาที) · kill ไคลเอนต์แล้วเซิร์ฟเวอร์ยังถือเซสชันเดิม — ต้องรีสตาร์ตเซิร์ฟเวอร์ก่อนเปิดไคลเอนต์ตัวถัดไปเสมอ ไม่งั้นค้าง "connecting" ตลอดกาล
  P5. `-SecondPasswordMode bypass` (กฎเดียวกับ `GT-228`/`GT-230`) กันกล่องรหัสผ่านที่สองขวางถ้าแผง/คลังเรียกมัน — **ใบนี้ไม่ตัดสินพฤติกรรมรหัสผ่านที่สอง** เจอกล่องนั้นทั้งที่ตั้ง bypass ไว้ = finding แยก ไม่ใช่ใบล้ม

- db: canonical = `state\pirateforce.sqlite3` — 🔴 **สำเนาเท่านั้น ห้ามเปิด canonical** ⇒ คัดลอกเป็น
  `state\run_gt262_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา (คัดลอกครั้งเดียวต่อรอบ เหมือน `GT-258`) ·
  sha256 canonical ก่อน/หลังต้องตรง `CANON_SHA.txt` · `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง ·
  จด sha256 ของสำเนาก่อน/หลังด้วย

- server args: บูตมาตรฐาน · **ไม่มีแฟล็ก scenario ใด ๆ** · `-SecondPasswordMode bypass` ·
  🔴 เก็บคอนโซล **รวม stdout+stderr (`2>&1`)**
  ```
  py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
  git grep -n "StallStartVital\|StallOpenVital\|StallOperateVital\|GCSS_GuildStorageOpenVital\|GCGS_GuildStorageCmdVital" -- src/pirateforce_foundation
  py -3 -u -m pirateforce_foundation.app --db state\run_gt262_<stamp>.sqlite3 2>&1
  ```
  ต้องมีตัวจับแพ็กเก็ตเปิดอยู่ตลอดใบ: `capture_v141\GAME_LIVE.txt` (hex ดิบ) และ `GAME_EVENTS_LIVE.txt`

- steps: (**จดเวลานาฬิกา `HH:MM:SS+07:00` ทุกครั้งที่เขียนว่า "จดเวลา"** — ใช้ตัดหน้าต่าง hex ทีหลัง)
  0. **ด่านก่อนบูต**: รัน `git grep` ข้างบน — คาดว่า**ไม่เจอ** dispatcher ผูก opcode กลุ่มนี้ (สอดคล้อง P1) · **ถ้าเจอจริง** (มีคนเพิ่ม handler ระหว่างนี้) นี่คือการเปลี่ยนแปลงที่ `RE-261` ยังไม่รู้ ⇒ บันทึกเป็น finding แยกทันที แล้วเดินใบต่อตามเดิม (ไม่ใช่เหตุ BLOCK) · `LOCK_GAME` · boot stamp · sha canonical · คัดลอก DB เป็น run copy
  1. บูตเซิร์ฟเวอร์ใหม่สด · เปิดตัวจับแพ็กเก็ต
  2. บูตไคลเอนต์ · **สร้างตัวละครใหม่หนึ่งตัว** (ตาม P2) · ล็อกอิน · ภาพนิ่ง `S00-HOME` · เปิดกระเป๋ายืนยัน 4 ช่องตาม `INITIAL_BACKPACK` จริง — ถ้าไม่ตรง บันทึกของจริงแทน ไม่เดา
  3. **ข้อ 1 ของ `RE-261` (positive control ก่อนอย่างอื่นทั้งหมด — ห้ามข้าม ห้ามสลับลำดับ)**: ไล่คลิก/ไล่เมนูหาทางเข้า "แผงขายเอง" (NPC/ปุ่ม/hotkey ก็ได้ ยังไม่รู้ว่าเป็นแบบไหน) · **จดเวลา** ทุกครั้งที่คลิก + สิ่งที่คลิก + ผลลัพธ์ที่เห็น
     🔴 **เพดานการไล่คลิกรอบนี้: ไม่เกิน 15 นาทีนาฬิกาจริงหรือ 20 จุดคลิก แล้วแต่ถึงก่อน** — เกินแล้วยังไม่เจอ ⇒ ไปผลลัพธ์ `C`
  4. เจอทางเข้าแล้ว: เปิดแผง (`StallStartVital`) · ภาพนิ่ง `S1-STALL-OPEN` · **จดเวลา** · วางไอเทมหนึ่งชิ้นจากกระเป๋าลงช่องขาย (`StallOpenVital`) · ภาพนิ่ง `S1-ITEM-PLACED` · **จดเวลา**
  5. **trial A**: ตั้งราคาค่าที่ 1 บนช่องราคา (`StallOperateVital`) · **จดเวลาทันทีก่อน/หลังยืนยันราคา** · ภาพนิ่งเต็มความละเอียด `S1-PRICE-A` ให้เห็นตัวเลขราคาชัดบนจอ
  6. **trial B (เซสชันเดียวกัน ห้ามปิดไคลเอนต์/รีล็อกอินระหว่างนี้)**: เปลี่ยนราคาช่องเดิมเป็นค่าที่ 2 ที่ต่างจาก trial A (`StallOperateVital` อีกเฟรม) · **จดเวลา** · ภาพนิ่งเต็มความละเอียด `S1-PRICE-B` ให้เห็นตัวเลขราคาใหม่ชัดบนจอ · 🔴 **ทั้งสอง trial ต้องต่างกันเฉพาะตัวเลขราคาเท่านั้น** (ไอเทมเดิม ช่องเดิม ไม่ปิด-เปิดแผงใหม่ระหว่างนั้น) — นี่คือ positive control ที่ `RE-261` ขอ ถ้าทำสิ่งอื่นเปลี่ยนไปด้วย (เช่น สลับไอเทม) การเทียบไบต์จะสกปรก บันทึกไว้ตรง ๆ แล้วทำ trial ใหม่
  7. ปิดแผง · ภาพนิ่ง `S1-STALL-CLOSE`
  8. **ข้อ 3 ของ `RE-261`**: ไล่คลิก/ไล่เมนูหาทางเข้า "คลังกิลด์" แยกรอบใหม่ · **จดเวลา** ทุกครั้งที่คลิก + สิ่งที่คลิก + ผลลัพธ์ที่เห็น · **ทำต่อไม่ว่าผลลัพธ์ trial A/B ข้างบนจะออกทางบวกหรือลบ** (การผูก opcode กับหน้าจอของคลังกิลด์เป็นคนละคำถามจากไบต์ราคา ตาม `RE-261`)
     🔴 **เพดานการไล่คลิกรอบนี้: ไม่เกิน 10 นาทีนาฬิกาจริงหรือ 15 จุดคลิก แล้วแต่ถึงก่อน** — เกินแล้วยังไม่เจอ ⇒ ไปผลลัพธ์ `C` (ส่วนคลังกิลด์)
  9. เจอทางเข้าแล้ว: เปิดคลังกิลด์ (`GCSS_GuildStorageOpenVital`) · ภาพนิ่ง `S3-GS-OPEN` · **จดเวลา** · ถ้าเปิดไม่ได้เพราะไม่มีสังกัดกิลด์หรือเหตุอื่นที่ระบุได้ ⇒ ผลลัพธ์ `E` (บันทึกข้อความ/เหตุผลที่จอบอกตามตัวอักษร)
  10. ฝากไอเทมหนึ่งชิ้นจากกระเป๋าเข้าคลัง (`GCGS_GuildStorageCmdVital`) · **จดเวลา** · ภาพนิ่ง `S3-GS-DEPOSIT`
  11. ถอนไอเทมชิ้นเดิมกลับ (`GCGS_GuildStorageCmdVital` อีกเฟรม) · **จดเวลา** · ภาพนิ่ง `S3-GS-WITHDRAW`
  12. ปิดคลัง · ภาพนิ่ง `S3-GS-CLOSE` · เช็ก NO-CRASH ด้วย**คลิกขวาค้างลาก** (กล้องอย่างเดียว ทิศทางตัวละครไม่ขยับ ไม่มีไบต์ออกสาย) · 🔴 **ห้ามใช้ `Q`/`E` เป็น NO-CRASH check**
  13. ปิดเซิร์ฟเวอร์ · เก็บ `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **รัน `TEMPLATE_teardown_generic.ps1` เสมอ** (**boot stamp ต้องไม่เกิน 420 นาที** ตาม `TEMPLATE_teardown_generic.ps1:135` — รอบที่จบเพราะเลิกเล่นก็ต้อง teardown)

- เกณฑ์สองชั้น (🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น**):
    wire/DB (อ่านคอนโซลเซิร์ฟเวอร์ + hex ดิบ + ไฟล์ DB · ไม่ต้องมีตาคน · 🔴 **การตัดสินว่าไบต์ `+0x20` แปลว่าราคาหรือไม่ ไม่ใช่ของใบนี้ — เป็นของ `RE-261`/`CLIENT_RE_QUEUE.md` เท่านั้น**):
      W1. hex ครบทั้งสองเฟรมของ trial A/B (`StallOperateVital`) พร้อมเลข `[G<#N]` และเวลาที่จับคู่กับขั้น 5-6
      W2. hex ของเฟรม `StallStartVital`/`StallOpenVital` (ถ้าเจอทางเข้า) จับคู่เวลากับขั้น 4
      W3. hex ของเฟรม `GCSS_GuildStorageOpenVital`/`GCGS_GuildStorageCmdVital` (ถ้าเจอทางเข้า) จับคู่เวลากับขั้น 9-11
      W4. sha canonical ก่อน=หลัง ตรง `CANON_SHA.txt` · `integrity_check = ok` สองครั้ง · บูตบนสำเนาเสมอ · `sessions` +1 ต่อการล็อกอิน · `lease_generation` ไม่ถอยหลัง · ไม่มี traceback
      🔴 **ชั้นนี้ตอบไม่ได้ว่าคนเห็นอะไรบนจอ — ห้ามใช้แทนชั้นล่าง**
    client-observable (🔴 ต้องมีตาคน ห้ามอนุมานจาก hex):
      C1. ภาพ `S1-PRICE-A`/`S1-PRICE-B` แสดงตัวเลขราคาที่ต่างกันจริงบนจอ อ่านได้ชัดจากภาพเต็มความละเอียด
      C2. ภาพ `S1-STALL-OPEN`/`S1-ITEM-PLACED` แสดงหน้าต่างแผงขายเองเปิดจริง + ไอเทมอยู่ในช่อง
      C3. ภาพ `S3-GS-OPEN`/`S3-GS-DEPOSIT`/`S3-GS-WITHDRAW` แสดงหน้าต่างคลังกิลด์เปิดจริง + ไอเทมย้ายเข้า/ออกจริง (หรือข้อความปฏิเสธตามตัวอักษรถ้าเปิดไม่ได้ — ผลลัพธ์ `E`)
      C4. **บรรทัดสีป้ายครบทุกป้ายทุกภาพ** (ข้อบังคับ R163 คำสั่ง Panya 2026-08-25): หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ · "none" เขียนออกมา ไม่เว้นว่าง · อ่านจากภาพนิ่งเต็มความละเอียดเท่านั้น (ห้าม contact sheet/ภาพย่อ/วิดีโอ) · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (`RE-067` เป็นเจ้าของคำถามนั้น) · ต่างจากภาพเซิร์ฟเวอร์เดิม = ลง `REAL_SERVER_DIVERGENCE.tsv` แถวละหนึ่งข้อ
      C5. NO-CRASH check ผ่านทุกครั้งที่กำหนด
      **`OBSERVER_CONFIRMED: <ISO+07:00>` เป็นข้อบังคับแข็งของชั้นนี้ (G-OBS) — ไม่มี = ชั้นนี้ไม่ PASS**

- predictions (ทายผิด = finding ไม่ใช่ความล้มเหลว — carry-over hedge เดียวกับที่ `RE-261` ติดป้าย):
  - P1 [เสนอ, ยกจาก chief round 75 / `docs/FUNCTIONAL_COVERAGE.json`'s `use_drop_sell`]: ไบต์ `+0x20` ของ `StallOperateVital` เปลี่ยนตามราคาที่ตั้งบนจอ
  - P2 [เสนอ]: ทางเข้า "แผงขายเอง" หาเจอภายในเพดาน 15 นาที/20 จุดคลิก
  - P3 [เสนอ]: ทางเข้า "คลังกิลด์" อาจต้องมีสังกัดกิลด์ก่อน — ยังไม่มีใครวัด อาจจบที่ผลลัพธ์ `E`

- ทำอย่างไรกับผลแต่ละแบบ:
  A. **trial A/B ต่างกันแค่ราคาสำเร็จ + เจอทางเข้าแผง/คลังทั้งคู่ + ผูก opcode กับหน้าจอได้ครบ** ⇒ **PASS** (ชั้น client-observable ของใบนี้) · เกณฑ์ C1-C5 ตัดสิน · คำตัดสินไบต์ `+0x20` ให้ LANE-UI เขียนแยกลง `RE-261:result`
  B. **เจอทั้งแผง/คลัง ผูก opcode กับหน้าจอได้ แต่ hex ของ trial A/B (เมื่อ LANE-UI อ่าน) พบว่า `+0x20` ไม่ขยับตามราคา** ⇒ **PASS พร้อมคำตัดสิน `PRICE-BYTE-NOT-CONFIRMED`** — เป็นผลลบที่มีค่าเท่าผลบวก หักล้างสมมติฐาน chief round 75 (เขียนเป็น finding ไม่ใช่ความล้มเหลว) · ชั้น client-observable ของใบนี้ (การผูกหน้าจอกับ opcode) ยัง **PASS ได้ตามปกติ** เพราะเป็นคนละคำถามจากไบต์ราคา
  C. **ไล่คลิกจนครบเพดานแล้วไม่เจอทางเข้าแผงหรือคลังเลย (แยกกันได้ — เจอแผงแต่ไม่เจอคลัง หรือกลับกัน)** ⇒ **PASS พร้อมคำตัดสิน `NO-STALL-ENTRY-FOUND`/`NO-GUILDSTORAGE-ENTRY-FOUND`** (มีค่าเท่าผลบวก เหมือน `NO-SHOP-FOUND` ของ `GT-230`) · redirect: ทางเข้าอยู่นอกระยะที่ไล่คลิกถึง หรือบิลด์นี้ยังไม่มี UI/NPC ที่ประกาศเป็นทางเข้าเลย ⇒ ใบถัดไปต้องขอพิกัด/เมนูจากฝั่ง static RE
  D. **ไคลเอนต์ตาย/ตัวจับแพ็กเก็ตไม่เขียนไฟล์** ⇒ **NO-RESULT** พร้อมเหตุผลหนึ่งบรรทัด
  E. **เจอทางเข้าคลังกิลด์แต่เปิดไม่ได้เพราะไม่มีสังกัดกิลด์ (หรือเหตุอื่นที่ระบุได้จากข้อความบนจอ)** ⇒ **PASS พร้อมคำตัดสิน `NO-GUILDSTORAGE-ACCESS`** (ผลลบที่ใช้ได้ ไม่ใช่ใบล้ม) · ส่วนแผงขายเอง (trial A/B) ยังตัดสินแยกตามผลลัพธ์ A/B/C ข้างบนตามปกติ · redirect: ต้องมีใบ/ฟีเจอร์สร้าง-เข้าร่วมกิลด์ก่อนถึงจะไล่ต่อได้

- nonclaims:
  1. 🔴 **ห้ามเดาความหมาย tag ที่เหลือ** (`+0x14`/`+0x18`/`+0xB0` ฯลฯ) — `RE-261` สั่งห้ามตรง ๆ ว่าห้ามเดาก่อนข้อ 1 ผ่าน ใบนี้ก็ไม่เดาเช่นกัน ไม่ว่า trial A/B จะออกผล A หรือ B ก็ตาม
  2. ไม่ตัดสินว่าเซิร์ฟเวอร์เราเอง (`pirateforce_foundation.app`) จำลองพฤติกรรมแผงขายเอง/คลังกิลด์ของเซิร์ฟเวอร์ค่ายได้ถูกต้อง — **ไม่มีโค้ดฝั่งเซิร์ฟเวอร์จับ opcode กลุ่มนี้เลยตอนเปิดใบ** (`serializer_status=OPEN` ทุกคลาส) ใบนี้แค่จับสิ่งที่บิลด์นี้ทำจริงตอนนี้
  3. ไม่อ้างว่าถอดฟิลด์ในเฟรมได้มากกว่า hex ดิบที่จับได้จริง — ระดับฟิลด์ที่เหลือของ `StallOpenVital`/`StallOperateVital`/ตระกูล guild storage อีก 12 คลาส ยังไม่แกะราย field (ของ `RE-261`/รอบ static ถัดไป ไม่ใช่ของใบนี้)
  4. **ใบนี้ไม่ปิด `RE-261` ด้วยตัวเอง** — `RE-261` ปิดเมื่อ LANE-UI เขียนคำตัดสินชั้น wire/DB (ไบต์ `+0x20` ขยับตามราคาหรือไม่) ลง `CLIENT_RE_QUEUE.md:RE-261` เอง ตามที่ "ผลไปถึงใคร" ของใบนั้นระบุไว้
  5. ไม่อ้างว่า `STALL_SET.n_ID` ที่เห็นบนจอ (ถ้าอ่านได้) ตรงกับแถวใดใน `gamedata/PF_GAMEDATA_INDEX.tsv:117`/คอลัมน์ `gamedata/PF_GAMEDATA_COLUMNS.tsv:1924-1933` เว้นแต่ผู้เทสอ่านค่าออกมาตรง ๆ จากจอ — ตารางนั้น**ไม่มีคอลัมน์ราคา** จึงช่วยระบุ "แผงชนิดไหน" เท่านั้น ไม่ช่วยตอบคำถามไบต์ราคา
  6. ไม่ทดสอบ/ไม่อ้างอะไรเกี่ยวกับ `GuildStorageOpenVital`(`0x5CAD`)/`GuildStorageResultVital`(`0x70D0`) — สองคลาสชื่อเปล่าที่ `RE-261` เองระบุว่า "ใบนี้ไม่ขอ" (ไม่มีแถวให้เทียบเลย)
  7. ไม่มีการซื้อขายจริงข้ามผู้เล่นสองคน (ไม่มีตัวละครที่สองมากดซื้อของในแผง) — ใบนี้จบที่ "ของอยู่ในช่องขาย + ตั้งราคาสองค่า" ตามขอบเขตที่ chief ระบุไว้ในหัวใบเดิม ไม่ใช่การยืนยันธุรกรรมสำเร็จ
  8. ไม่ยืนยัน/ปฏิเสธว่าคลังกิลด์ต้องมีสังกัดกิลด์ก่อนหรือไม่โดยทั่วไป — บันทึกแค่สิ่งที่จอบอกจริงในรอบนี้ (ดูผลลัพธ์ `E`)

- STOP:
  1. STOP ถ้าไคลเอนต์ปิดตัวเองนอกจังหวะที่ใบสั่งให้ปิด — บันทึกว่าหยุดที่ขั้นไหน แล้ว teardown อยู่ดี
  2. STOP ถ้าเจอ `ErrorData` ใด ๆ ที่ไม่เกี่ยวกับใบนี้ — บันทึกเป็น finding แยก ไม่ใช่ทำให้ใบนี้ล้ม
  3. STOP การไล่คลิกทันทีที่ถึงเพดานของแต่ละรอบ (ข้อ 3/8 ของ steps) แล้วไปผลลัพธ์ `C` ของส่วนนั้น — ห้ามยืดเพดานเอง
  4. STOP การเดาความหมาย tag ใด ๆ นอกเหนือจาก `+0x20`/ราคา ไม่ว่าที่จุดใดของใบ (ตามข้อห้ามของ `RE-261`)

- links: `CLIENT_RE_QUEUE.md:RE-261` (`RE-261 STALL-AND-GUILD-STORAGE-FIELD-SEMANTICS-FROM-A-REAL-SESSION-001`) ·
  `notes_to_chief/20260905_0456_LANE-UI-RE-TICKET-stall-and-guild-storage-opcodes-known-fields-partial.md` (จดหมายต้นทาง เนื้อเต็ม) ·
  `GT-230` (ใบต้นแบบของรูปแบบ — ใบเก็บ hex ไม่ใช่ใบตัดสิน) ·
  `gamedata/PF_GAMEDATA_INDEX.tsv:117` + `gamedata/PF_GAMEDATA_COLUMNS.tsv:1924-1933` (`STALL_SET`, ไม่มีคอลัมน์ราคา) ·
  `gamedata/PF_GAMEDATA_LUA_API.tsv:122` (`Guild.OpenGuildStorage`, `Quest/q_guildstorage.lua`, สถานะ `UNRESOLVED`) ·
  `external/PF_SERIALIZER_FIELDS.tsv` (แถว `StallStartVital`/`StallOpenVital`/`StallOperateVital`/`GCSS_GuildStorageOpenVital`/`GCGS_GuildStorageCmdVital`) ·
  `external/PF_FIELD_VALIDATION.tsv:1018-1023,418-421` (ทุกแถว `NOT_OBSERVED` ก่อนใบนี้) ·
  `pirate-force-server/src/pirateforce_foundation/inventory.py:39-49` (`INITIAL_BACKPACK`) · `pirate-force-server/src/pirateforce_foundation/store.py:575,674` (`_insert_initial_backpack`) ·
  `ATTENDED_SESSION_RUNBOOK.md` + `BRIDGE_BOOT_PROCEDURE.md` + `TEMPLATE_teardown_generic.ps1`

ATTENDED: สร้างตัวละครใหม่ 1 ตัว ไล่คลิก/ไล่เมนูหาทางเข้า "แผงขายเอง" (เพดาน 15 นาที/20 คลิก) -- เจอแล้วเปิดแผง วางไอเทม 1 ชิ้น ตั้งราคา trial A แล้วเปลี่ยนเป็นราคา trial B ในเซสชันเดียวกัน (ห้ามปิด-เปิดแผงใหม่) -- แยกรอบไล่คลิกหา "คลังกิลด์" (เพดาน 10 นาที/15 คลิก) เปิดแล้วฝากไอเทม 1 ชิ้นแล้วถอนกลับ
ATTENDED: ดูเฟรม `StallStartVital 0x30FE`/`StallOpenVital 0x2A3E`/`StallOperateVital 0x3DE4` (สองเฟรม trial A/B) และ `GCSS_GuildStorageOpenVital 0x8B66`/`GCGS_GuildStorageCmdVital 0x7F17` (ฝาก/ถอน) -- ใบนี้ไม่ตัดสินว่า `+0x20` แปลว่าราคา (เป็นของ `RE-261`)
ATTENDED: PASS ชั้นจอ = ภาพ `S1-PRICE-A`/`S1-PRICE-B` อ่านตัวเลขราคาต่างกันได้ชัด + แผง/คลังเปิดจริงเห็นไอเทมย้าย (หรือข้อความปฏิเสธตามตัวอักษรถ้าเปิดไม่ได้ = ผล `E`) + บรรทัดสีป้ายครบทุกภาพ + `OBSERVER_CONFIRMED: <ISO+07:00>` -- ไม่มี = ไม่ PASS
ATTENDED: บูตมาตรฐาน ไม่มีแฟล็ก scenario ใด ๆ `-SecondPasswordMode bypass` ตัวจับแพ็กเก็ตต้องเปิดตลอดใบ (`capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt`)
ATTENDED: ไล่คลิกครบเพดานแล้วไม่เจอทางเข้า = ไปผล `C` (`NO-STALL-ENTRY-FOUND`/`NO-GUILDSTORAGE-ENTRY-FOUND`) แยกกันได้ต่อระบบ -- ไม่ใช่ใบล้ม

- result: (ผู้เทสกรอก: PASS `A`/`PRICE-BYTE-NOT-CONFIRMED`/`NO-STALL-ENTRY-FOUND`/`NO-GUILDSTORAGE-ENTRY-FOUND`/`NO-GUILDSTORAGE-ACCESS` หรือ `NO-RESULT` · branch+commit ที่บูต · ผลของ `git grep` ด่านข้อ 0 · ทุกจุดคลิกของทั้งสองรอบไล่คลิกพร้อมเวลาและผลลัพธ์ · hex ดิบครบของ trial A/B (`StallOperateVital`) พร้อม `[G<#N]` · hex ดิบของ `StallStartVital`/`StallOpenVital`/`GCSS_GuildStorageOpenVital`/`GCGS_GuildStorageCmdVital` ถ้าจับได้ · ภาพ `S00-HOME`/`S1-STALL-OPEN`/`S1-ITEM-PLACED`/`S1-PRICE-A`/`S1-PRICE-B`/`S1-STALL-CLOSE`/`S3-GS-OPEN`/`S3-GS-DEPOSIT`/`S3-GS-WITHDRAW`/`S3-GS-CLOSE` (เฉพาะที่ถ่ายได้จริง) + sha256 ทุกภาพ · **บรรทัดสีป้ายครบทุกป้ายทุกภาพ** · sha canonical ก่อน/หลัง · `integrity_check` สองครั้ง · NO-CRASH/CRASH · teardown รันแล้ว (boot stamp ไม่เกิน 420 นาที) · `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` · 🔴 **คัดลอกผล hex + คำตัดสิน `+0x20` (ถ้าวัดได้) ไปกรอกใน `RE-261:result` ด้วยตัวเอง (LANE-UI) — ใบนี้ไม่กรอกให้**)

- **ลำดับ**: ต่อท้าย "รอเครื่องคุณ" ของ `NOW.md` — **ไม่แซง** `GT-233` / `GT-230` / `GT-243` (งานที่ค้างอยู่ก่อนแล้ว) · ไม่บล็อกใคร

## numbering
`GT-262`/`RE-262` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*`) ก่อนวาง [วัดแล้ว chief `pv4zg1`/R352] · ตัวนับร่วมสองคิวคืนสูงสุดที่ `256` ก่อนรอบนี้ · รอบนี้กิน `257`-`262`


## GT-264 RECOMPOSE-MID-COMBAT-KEEPS-ANOTHER-MOBS-GROUND-DROPS-001  [🔴 **BLOCKED-ON-WIRING -- บูตไม่ได้จนกว่าบรรทัดต่อสายจะอยู่บน main** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A** · ผู้ตั้งเลข/วางใบ = chief (LANE-E) รอบ `r045nx`/R354 ตามคำขอข้อ 1 ของ `notes_to_chief/20260905_1250_LANE-A-TO-CHIEF-ground-drop-fix-shipped-registry-carried-gt-number-needed.md` · ผู้รัน = Panya (attended) ~5 นาทีบนจอ · พ่วงบูตอื่นได้]

> 🔴 **ตัวบล็อก (เงื่อนไขปลดเดียว)**: `mob_scene_recompose.ground_companion_actions(...)` ถูกเรียกจริงจาก `runtime.py` บน `main` -- ฟังก์ชันเองอยู่บน main แล้ว (`pirate-force-server#818` merged 2026-09-05T06:03Z) แต่ยัง**ไม่มีผู้เรียก** ⇒ บูตวันนี้ได้ผลของบั๊กเดิมเสมอ ไม่ใช่คำตอบของใบนี้ · เมื่อบรรทัดขึ้น main แล้วให้ chief แก้หัวใบเป็น 🟢 READY
> 🔴 **ใบนี้อยู่ใต้ข้อห้าม "ห้ามใบเทสตีมอนจนกว่า P-2 จะปิด"** (`NOW.md`) -- ใบนี้ตีมอนสองตัว ⇒ **แม้ปลด BLOCKED-ON-WIRING แล้วก็ยังรันไม่ได้จนกว่า P-2 ปิด หรือ COO/Panya ยกเว้นให้เป็นรายใบ** (แบบที่ `ATTACK-POSE-ONE-FIELD-AB-001` ได้รับ) · chief บันทึกข้อนี้ไว้ตรง ๆ แทนที่จะปล่อยให้ผู้เทสไปเจอเองหน้าเครื่อง

- objective: recompose ระหว่างต่อสู้ต้องไม่ลบของพื้นของมอนอื่นในฉากเดียวกัน

- เตรียม: ยืนในฉากที่มีมอนอย่างน้อย 2 ตัวที่ยังไม่ตาย (เช่น Bg0002)

- steps: (1) ฆ่ามอนตัว A -> สังเกต `MOB_LOOT_DROPS_CENSUS` ประกาศของตก และเห็นของบนจอ (2) ตีมอนตัว B (คนละตัวกับ A ที่ยังไม่ตาย) นัดแรก -> สังเกต `MOB_COMBAT_BAR_CENSUS_RECOMPOSE` ยิง

- pass criteria: 🔴 **สองชั้น ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น** (`G5`)
  **wire/DB**: บรรทัด `MOB_COMBAT_BAR_CENSUS_RECOMPOSE` ยิงจริงในคอนโซล **และ** ตามด้วยบรรทัดของพื้นที่ **`frames=` มากกว่า 0** และบรรทัดเหตุการณ์ `ground_companion_after_bar_appended_<n>` ที่ **`<n>` ≥ 1**
  🔴 **ห้ามเกรดจากการเห็นโทเคนอย่างเดียว** (แก้ตาม `pf-adversary` D5 รอบ `r045nx`): `ground_companion_actions` พิมพ์ `mob_drop_presence.describe_presence` **ก่อน**ตรวจว่าถูกปฏิเสธหรือไม่ ⇒ บูตแล้วไม่ฆ่าอะไรเลยแล้วตีมอนหนึ่งครั้ง จะได้ `MOB_COMBAT_BAR_CENSUS_RECOMPOSE` ตามด้วย `MOB_DROP_PRESENCE state=refused_cell_has_no_scene_to_publish … frames=0` ซึ่ง**อ่านเป็นลำดับโทเคนที่ถูกต้องทั้งที่ไม่มีอะไรถูกส่งเลย** (สตริงปฏิเสธตัวนี้เคยเป็น negative control ของ R316) ⇒ **ต้องอ่านตัวเลข ไม่ใช่ชื่อโทเคน**
  **client-observable**: ของที่มอน A ทิ้งไว้ **ยังคงอยู่บนจอและยังเก็บได้** ทันทีหลังนัดแรกที่ตี B -- ไม่ต้องรอให้ B ตายหรือมีการประกาศของครั้งถัดไปก่อนของ A จะกลับมา
  🔴 ปิดใบด้วย `OBSERVER_CONFIRMED: <ISO+07:00>` เท่านั้น (`G-OBS`) -- ครบหลักฐานแต่ไม่มีลายเซ็นคน = `AWAITING-OBSERVER`

- เกณฑ์ไม่ผ่าน (บั๊กเดิม, R316): ของ A หายจากจอทันทีที่ `MOB_COMBAT_BAR_CENSUS_RECOMPOSE` ยิง

- nonclaims: (1) ไม่ตัดสินว่าไคลเอนต์วาดของกลับทันทีหรือมีดีเลย์ที่ตาเห็น (`#818` เขียนเองว่ายังไม่วัดแยก) (2) ไม่ตัดสินเรื่องสีป้ายชื่อ (`RE-067`/P-2) (3) ไม่ตัดสินอายุของของบนพื้น (`1247` ยังคงพฤติกรรมเดิมจนกว่าจะวัด)

- links: R316 finding ที่สาม (`notes_to_chief/20260905_1102_KA1A-R316-RESULTS-*`) · `COO-DECISION 20260905_1152` ข้อ 2(1) · `pirate-force-server#818` (`mob_scene_recompose.ground_companion_actions` + `GROUND_COMPANION_WIRING`) · `GT-242` (PASS R316 -- กลไกประกาศของพื้นตัวเดียวกันที่ไคลเอนต์เคยรับแล้ว)

- numbering: `GT-264`/`RE-264` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*`) ก่อนวาง **[วัดแล้ว รอบนี้]** · ตัวนับร่วมสองคิว + archive คืนสูงสุดที่ `263` (`RE-263`) ⇒ ใบนี้ `264` · จองต่อในรอบเดียวกัน: `RE-265` (`CLIENT_RE_QUEUE.md`) · `GT-266` · `GT-267`

- result: (ผู้รันกรอก)

**STOP:** ไคลเอนต์ปิดตัว / `ErrorData` ใด ๆ -> หยุดทันที บันทึกสิ่งที่กดล่าสุด

## GT-266 WARP-126-LIVE-TELEPORT-001  [🟢 **READY -- attended, in-game** · ส่วน 'อยู่ทะเลเดิมหลัง relog' = NOT MEASURED (ใบสั่งห้าม relog รอบนั้น · server เองรายงาน `GM_WARP_SCENE_PERSIST_FAILED` แล้ว stage relog แบบใช้ครั้งเดียว) — chief/LANE-GM ต้องชี้ขาดว่าปิดใบนี้ได้หรือแยกใบสำหรับส่วนที่สอง (คำถามที่ Panya ฝากใน R320) (คำต่อคำจากหัวใบเดิมทั้งสองท่อน — คำตัดสิน "PASS สองชั้น เฉพาะส่วน 'วาปสด'" ที่เดิมขึ้นก่อน READY ถูกย้ายไปบรรทัด "ประวัติหัวใบเดิม" ด้านล่างแทน เพราะทำให้เครื่องมือ regex อ่านทั้งใบเป็น PASS ผิด) · **เจ้าของใบ/ผู้เขียนเนื้อใบ = LANE-A** (ตรวจสด/persist = LANE-GM ตาม `COO-DECISION 20260905_1347`) · เนื้อใบเต็มวางโดย chief (LANE-E) รอบ `cooif2`/R357 · PR ที่ใบนี้เทส (`pirate-force-server#838`, decreed arrival) **merged to main 2026-09-05T18:04+07:00** [จัดรูปแบบโดย LANE-K รอบ `x91eo8`/`x91eo8r2` ตามข้อเสนอ chief `R374` ข้อ 2 — คำอื่นทุกคำคงเดิม]] [🟢 **`HEADLESS_PROOF:` มาแล้ว — ใบขึ้นรถบัสได้ (หมวด ก.)** · วางโดย LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00 · จดหมาย `notes_to_chief/20260907_0604_LANE-A-TO-K-gt266-headless-proof-line.md` (เจ้าของใบ LANE-A รอบ `lnq6xy` 06:04) · บรรทัดเดียวที่เจ้าของใบขอให้วาง **คำต่อคำ ไม่แก้อักขระใด** วางไว้ท้ายบล็อก `ATTENDED:` · เจ้าของใบวัดบน `pirate-force-server` `550a36d` และยืนยัน `git merge-base --is-ancestor HEAD origin/main` เอง · 🔴 nonclaims ของเจ้าของใบที่ห้ามตัดทิ้ง: บรรทัดนี้ **ไม่ใช่ชั้น client-observable** (ไม่มีไคลเอนต์ ไม่มีจอ ไม่มีเฟรมออกสาย) ตอบเฉพาะคำถามของ `PANYA-ORDER 0159` ว่า 'บูตไปแล้วจะไม่เจอกลไกที่ถูกถอดออก' · ใบยังต้องบูต attended ครบทุกขั้น และผลบนจอยังเป็นสิ่งเดียวที่ตัดสิน PASS · ไม่ได้รัน `/warp 126` ผ่านเส้น GM chat จริง ⇒ ถ้าเส้น chat→executor ขาดกลาง บรรทัดนี้จับไม่ได้ · ส่วน 'อยู่ทะเลเดิมหลัง relog' = NOT MEASURED ยังคาอยู่เหมือนเดิม · 🔴 K ไม่ได้รันโทเคนนี้เอง]

> **ประวัติหัวใบเดิมคำต่อคำ (ก่อนจัดรูปแบบรอบ `x91eo8`)**: 🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS สองชั้น เฉพาะส่วน 'วาปสด ไม่ต้อง relog' — R320 2026-09-06 §GT-266 · ส่วน 'อยู่ทะเลเดิมหลัง relog' = NOT MEASURED (ใบสั่งห้าม relog รอบนั้น · server เองรายงาน `GM_WARP_SCENE_PERSIST_FAILED` แล้ว stage relog แบบใช้ครั้งเดียว) — chief/LANE-GM ต้องชี้ขาดว่าปิดใบนี้ได้หรือแยกใบสำหรับส่วนที่สอง (คำถามที่ Panya ฝากใน R320) · จาก notes_to_chief/20260906_0155_KA1A-R320-*.md
>

ATTENDED: บูตเซิร์ฟปกติ **ไม่มีแฟล็ก ไม่ตั้ง env** บนโค้ด main -> ล็อกอิน GM ที่ Port Royal รอเห็นเมือง -> จดฉาก/สิ่งที่เห็น (ภาพก่อน) -> พิมพ์ในช่องแชต `/warp 126` -> **ห้ามล็อกเอาต์ ห้ามรีสตาร์ต** ดูจอทันทีนับ 10 วินาที
ATTENDED: มองหาบรรทัดคอนโซล `WORLD_SCENE scene_id=126 ... marker=0 ... decreed_arrival=17` (สองค่านี้ต้องคู่กัน) และ **ไม่มี** `STAGED_NEXT_LOGIN` สำหรับคำสั่งนี้ · ต้องมี `GM_WARP_SCENE_PERSIST_FAILED scene=126 reason=login_would_refuse` ด้วย (คาดไว้ว่าจะเห็น -- ไม่เห็นบรรทัดนี้ = ผิดคาด ให้รายงาน) · relogin ต่อ = คัด `GM_WARP_RELOG_ENTRY_STAGED`
ATTENDED: 🔴 PASS = ครบ **ทั้งสองชั้น** (wire/DB บรรทัดบน + จอบรรทัดนี้ ขาดชั้นใด = ยังไม่ PASS) · ชั้นจอ ไม่ relogin: จอเปลี่ยนเป็นทะเลใน 10 วิ + ตัวละครเป็นเรือ + ไม่มีหน้าจอโหลดพาไปเลือกตัวละคร ไม่มีตัดการเชื่อมต่อ · ⚠️ สามข้อนี้ทะเลฉากไหนก็ผ่าน (304/305 วาปสดได้แล้ว) สิ่งเดียวที่ปักว่า 126 คือ `WORLD_SCENE scene_id=126` ชั้น wire ห้ามตัด · เห็น `WORLD_SCENE` แต่จอไม่เปลี่ยน = NO-RESULT ชั้น client จดแยกชั้น
ATTENDED: ต่อในบูตเดียวกันถ้าขั้นบนผ่าน: `/warp 126 3050 232 90` ต้องถูกปฏิเสธไม่มีไบต์ออก · `/warp 278` ต้องยัง stage เหมือนเดิม · `/warp 2` ต้องยังวาปสดเหมือนเดิม -- ผลตรงข้ามข้อใด = เกตพัง รายงานทันที · 🔴 ใบนี้ต้องรันเป็นใบแรกของบูต (มันเปลี่ยนฉากตัวละคร ใบที่ยืน Port Royal จะเสีย) · ห้ามพ่วงกับ `GT-233`
ATTENDED: relogin ทำได้ ไม่ใช่ข้อห้าม (บรรทัดเดิมสั่งห้าม = ผิด ใบนี้แค่ไม่อ้างผล) · ทำได้หลังเก็บสองชั้นข้างบนครบแล้วเท่านั้น จดดิบ ๆ ว่าโผล่ที่ไหน: ใบคาดเด้งกลับ Port Royal (`WORLD_SCENE_ENTRY_REFUSED`) แต่ `gm/warp_relog_stage.py` บน main คาดว่ายังอยู่ทะเลเดิม + เห็น `GM_WARP_RELOG_ENTRY_STAGED` · 🔴 สองอย่างขัดกัน จดอย่างเดียว ห้ามตีความ ห้ามตัดสิน PASS/FAIL จากขา relogin (chief แยกใบตาม NOW.md) · เจอ `.err.txt` มี `ErrorData=` ที่ไม่เคยเห็น หรือไคลเอนต์ปิดตัวเอง/ค้าง = STOP ทันที จดเลขแล้วออก ห้าม retry

HEADLESS_PROOF: 2026-09-07 commit 550a36d (origin/main) -- PYTHONPATH=src python3 -c "from pirateforce_foundation.gm import warp_executor as w, warp_scene_persist as p; t=w.warp_no_coords_live_target(126); print('marker=%s decreed_arrival=%s live_target=%s login_would_accept=%s persist_fail=%s.%s' % (t.entry_marker, t.decreed_arrival_marker, t is not None, p.login_would_accept(126), p.FAIL_CONSOLE_TOKEN, p.OUTCOME_LOGIN_WOULD_REFUSE))" -> marker=0 decreed_arrival=17 live_target=True login_would_accept=False persist_fail=GM_WARP_SCENE_PERSIST_FAILED.login_would_refuse

> **คำถามเดียวที่ใบนี้ตอบ**: พิมพ์ `/warp 126` แล้ว **ย้ายเดี๋ยวนี้** หรือยังต้องล็อกอินใหม่
> **ทำไมถึงมีใบนี้**: `PANYA-DECISION 20260905_1329` -- "`/warp 126` ต้องวาปสดเหมือน `/warp 2`" · จุดมาถึงถาวรของฉาก 126 = `CONSTDATA_TH__MARKER.tsv` แถว `n_ID 17` (3050, 232, 90, `n_DIRTECTION` 6)
> **ผู้ทำ**: ผู้เทสที่หน้าเครื่อง (attended) · **บิลด์**: main (PR รอบ `ihjytc` merge แล้ว)

### ขั้นตอน
1. บูตเซิร์ฟเวอร์ปกติ **ไม่มีแฟล็ก** ไม่ตั้ง env อะไรเลย
2. ล็อกอินตัวละคร GM ที่ Port Royal (ฉาก 1) -- รอให้เห็นเมืองบนจอก่อน
3. บันทึกไว้: ตอนนี้อยู่ฉากไหน มองเห็นอะไร (จับภาพหนึ่งใบ)
4. พิมพ์ในช่องแชต: `/warp 126`
5. **ห้ามล็อกเอาต์ ห้ามรีสตาร์ต** -- ดูจอทันที นับ 10 วินาที

### เกณฑ์ผ่าน -- ต้องครบทั้งสองชั้น
**ชั้น client-observable (บนจอ, ไม่ relogin)**
- จอเปลี่ยนจากเมืองเป็น **ทะเล** ("Atlantis Ocean" / Rising Sun Sea) ภายใน 10 วินาทีหลังพิมพ์
- ตัวละครอยู่ในสภาพ **เป็นเรือ** ไม่ใช่คนเดินบนน้ำ
- ไม่มีหน้าจอโหลดที่พาไปหน้าเลือกตัวละคร ไม่มีการตัดการเชื่อมต่อ

**ชั้น wire/DB**
- คอนโซลมีบรรทัด `WORLD_SCENE scene_id=126 ... marker=0 ... decreed_arrival=17` (`marker=0` กับ `decreed_arrival=17` ต้องอยู่คู่กัน)
- คอนโซล **ไม่มี** `STAGED_NEXT_LOGIN` สำหรับคำสั่งนี้
- 🔴 **แถว `character_positions` จะ *ไม่* เป็น 126 และนั่นคือสิ่งที่คาดไว้ในรอบนี้** -- คอนโซลต้องมี `GM_WARP_SCENE_PERSIST_FAILED scene=126 reason=login_would_refuse` · **ไม่มีบรรทัดนี้ = ผิดคาด รายงาน**

### กลุ่มควบคุม (ทำต่อในบูตเดียวกัน ถ้าขั้นบนผ่าน)
- `/warp 126 3050 232 90` (ใส่พิกัดเอง) -- คาดว่า **ถูกปฏิเสธพร้อมบรรทัดคอนโซล ไม่มีไบต์ออก** (`FORCE_POS` 45 ไบต์ ErrorData=28317) · ถ้ามันกลับส่งเฟรมออกจริง = ข้อบกพร่อง รายงานทันที
- `/warp 278` -- ต้องยัง **stage** เหมือนเดิม (`GT-141`) · ถ้ามันวาปสด = เกตพัง รายงานทันที
- `/warp 2` -- ต้องยังวาปสดเหมือนเดิม

### STOP ทันที (หยุด บันทึก รายงาน ห้ามลองซ้ำ)
- ไคลเอนต์ปิดตัวเอง ค้าง หรือหลุดออกจากเกม
- `.err.txt` มี `ErrorData=` ใด ๆ ที่ไม่เคยเห็นมาก่อน (จดตัวเลข)
- ตัวละครล็อกอินกลับเข้ามาไม่ได้หลังจากนี้ -- วิธีถอย: `rollback GT-258` (`#806`)

### 🔴 ครึ่งที่ยังไม่ได้ -- อ่านก่อนเทส ไม่ใช่หลังเทส
ฉาก 126 เขียนแถวถาวรไม่ได้ และเป็นความตั้งใจ (`gm/warp_scene_persist.login_would_accept` ปฏิเสธเพราะ `login_entry_allowed` ของ 126 ยัง `false` จนกว่าจะมี attended var2 test ตาม `COO-DECISION 20260829_1444`) ⇒ **ปิดไคลเอนต์แล้วเข้าใหม่ = กลับ Port Royal** ไม่ใช่ข้อบกพร่องของใบนี้ · พิมพ์ `/warp 126` ใหม่ได้ทันที ไม่ล็อกตัวละคร · เรื่องนี้รอ COO เคาะ (`20260905_1708_LANE-A-ASK-COO-warp-126-live-but-not-persisted-*.md`) **ผู้เทสไม่ต้องทำอะไรกับเรื่องนี้ นอกจากบันทึกว่าเห็นบรรทัด `PERSIST_FAILED` จริงหรือไม่**

### สิ่งที่ใบนี้ **ไม่** อ้าง (ห้ามอ่านเกิน)
- **ไม่อ้างเรื่องทิศหันหน้า** -- `n_DIRTECTION 6` ไม่ได้ถูกส่งไปกับเฟรม teleport ยังไม่มีใครวัดว่าไคลเอนต์เอา heading ไปใส่ตัวละครหรือกล้อง · ตัวละครหันทางไหนก็ตาม **ไม่ใช่เกณฑ์ตก**
- **ไม่อ้างว่าล็อกอินใหม่แล้วยังอยู่ 126** -- ประตูล็อกอินของ 126 ยังปิด 🔴 **ถ้าผู้เทสล็อกเอาต์แล้วล็อกอินใหม่ในบูตนี้ คาดว่าจะถูกดีดกลับ Port Royal พร้อม `WORLD_SCENE_ENTRY_REFUSED`** -- ตั้งใจ ไม่ใช่ข้อบกพร่อง
- **ไม่อ้างว่ามอน/NPC ในฉาก 126 ครบ** -- census ของ Bg3001 เป็นคนละใบ (`GT-217`)

### พ่วงบูตอื่นได้
พ่วงกับใบอื่นในบูตเดียวกันได้ ถ้าใบนี้ **รันเป็นใบแรก** (มันเปลี่ยนฉากของตัวละคร) · 🔴 ห้ามพ่วงกับ `GT-233` (`BLOCKED-ON-RE`)

- result: (ผู้รันกรอก)

> วัดไว้แล้วก่อนใบนี้ (R318 §6): `/warp 126` ตอน 12:25:31 ได้ `GM_CHAT_STAGED_NEXT_LOGIN account='localtest' command=warp scene_id=126 coordinates=none basis=server_believed_scene next='this scene has no confirmed spawn point'` = ทำงานถูกตามบิลด์เดิม แต่ไม่ใช่สิ่งที่เจ้าของต้องการ -- แก้แล้วโดย `#838`
> ใบนี้**ไม่ใช่**ตัวที่ครอบ `GT-159` -- คำถามคนละครึ่ง (ใบนี้: "วาปสดไปโผล่ 126 ได้ไหมโดยไม่ relogin" · `GT-159`: "`DESTINATION_SCENE_N_ID = 17` อ่านใน id space ไหน" ซึ่งต้องกด Columbus บนบิลด์ที่แก้ปลายทาง) · ~~🔴 `GT-159` ยังไม่ปิด -- การปิดของ chief รอบ `r045nx` ถูกถอนในรอบเดียวกันหลัง `pf-adversary` D4 และรอ COO ตัดสิน~~ **ปิดแล้ว: `GT-159` = CANCELLED - covered by `GT-266` · no longer needs proving because `PANYA-DECISION 20260905_1329` (`COO-DECISION 20260905_1543` · chief รอบ `m8wtlr`/R356)** — ใบนี้ (`GT-266`) คือครึ่งที่ครอบ ดูหัวใบ `GT-159` ก่อนอ้างต่อ

- numbering: `GT-266`/`RE-266` = **0 hit ทั้งสามที่** ก่อนจอง **[วัดแล้ว รอบนี้]**

## GT-267 SEA-EDGE-CROSSING-126-TO-304-AND-305-001  [⚪ **RESERVED -- เนื้อใบ**มาถึงแล้ว**แต่ยังไม่ได้วางลงคิว** · LANE-A ส่งเนื้อใบเต็ม 2026-09-05T19:00+07:00 (`notes_to_chief/20260905_1900_LANE-A-GT-267-TICKET-BODY-sea-edge-crossing-126-to-304-305.md`) · 🔴 **chief ยังไม่วางเพราะเนื้อใบ 25,293 อักขระ = เกินเพดานใบใหม่ 8 KB ของ `AGENTS.md` §11 สามเท่า** [วัดแล้ว รอบ `rz1fxh`/R358] และ `GAME_TEST_QUEUE.md` วันนี้ 2.8 MB ที่ทุกสายอ่านทุกรอบ ⇒ chief ย่อเป็นถ้อยคำใบ (คำถาม + เกณฑ์สองชั้น + สถานะ + ลิงก์ไปจดหมาย) แล้ววางในรอบ LANE-E ถัดไป · **ถึง LANE-A: ไม่ต้องส่งซ้ำ ไม่ต้องรอ ใบนี้ไม่บล็อกงานสร้างของคุณ** (ใบนี้เป็นใบ attended และเครื่อง Panya ปิดอยู่) · เดิม: **เลขจองเท่านั้น เนื้อใบยังไม่เขียน** · **เจ้าของใบ/ผู้เขียนเนื้อใบ = LANE-A ร่วม LANE-GM** · จองโดย chief (LANE-E) รอบ `r045nx`/R354 ตาม `COO-DECISION 20260905_1349` ข้อ 4(ค) + `1348` ข้อ 6]

> คำถามที่ใบนี้จะถาม: แล่นเรือชนขอบแมพของฉาก 126 แล้ว**เปลี่ยนฉากจริงบนจอ** -- ขอบตะวันตก -> ฉาก 304 (Atlantic Ocean: Dark Fog Sea) · ขอบใต้ -> ฉาก 305 (Pale Silver Sea) · เป็นกลไกที่ `GT-254` (CANCELLED) ต้องรอ และเป็นทางเดียวที่จะไปถึงเกาะ 155 Slave Market Island
> วัตถุดิบที่วัดแล้ว (R318 §4 · capture-only ไม่แตะเซิร์ฟ): ขอบตะวันตก = เส้น X ≈ -8090 ยิง `TriggerVital 0x1FB2` id **7** ซ้ำได้ 2/2 ที่ Y ต่างกัน 3,478 หน่วย · ขอบใต้ Y ≈ -8384 = id **69** · ขอบเหนือ Y ≈ +6413 = id **48** · ขอบตะวันออก = **ไม่มีเฟรม** (`12 B2 1F` = 0 ในช่วงนั้น)
> 🔴 nonclaim ที่ต้องติดไปกับใบ: id บนสาย **ไม่ตรง**เลขฉากปลายทาง (304/305) และไม่ตรง `trigger_tip_th.tsv` ⇒ เป็น namespace ที่สาม · ชื่อ PROP ที่ hook พิมพ์ (`Viper Wicket`/`Ground Site Entrance`/`Captive Cage`) **ห้ามเชื่อ** · id 48 (ขอบเหนือ) ยังไม่รู้ว่าเป็นทางออกจริงไหม (แผนที่ไม่มีลูกศรเหนือ)
> 🔴 **ห้ามสายอื่นใช้เลข `GT-267`** · ต้องใช้ตัวส่ง "เปลี่ยนฉากสด" ตัวเดียวกับที่ `/warp` สดต้องการ (`GT-258`/`GT-266`) ⇒ งานร่วม A+GM

- numbering: `GT-267`/`RE-267` = **0 hit ทั้งสามที่** ก่อนจอง **[วัดแล้ว รอบนี้]**


## GT-269 GMUI-P3-WINDOW-ROW-CENSUS-LABELS-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS-CLIENT (GMUI 3 แท็บ 7/5/5 แถวตรง census · ต้องมี GameMaster.dll ติดถาวรข้าง client... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-272 EQUIP-WEAPON-FROM-BACKPACK-PERSISTS-ACROSS-RELOG-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — NEGATIVE-EXPECTED (server ยังไม่ตอบ op=5 · relog วันนี้ไม่มีอาวุธ ตามคาด) — R321 2026-09-06 §2 · RESULT: GT-272 NEGATIVE-EXPECTED R321 2026-09-06 (server no reply yet) · จาก notes_to_chief/20260906_1255_KA1A-R321-*.md · 🟢 **READY -- attended, in-game, pending capture ร่วมกับ `RE-272`** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-DB** · ตั้งเลขโดย chief (LANE-E) รอบ `ss9u08`/R363 ตาม `PANYA-ORDER 20260906_0156` ข้อ 1 (นิยาม "เสร็จ" คำต่อคำ) + `COO-DECISION 20260906_0345` ข้อ 4 · เนื้อใบมาจากจดหมาย `notes_to_chief/20260906_0404_LANE-DB-TO-CHIEF-order-0156-arm-b-re-draft-and-gt-draft-ready-for-numbering.md` คำต่อคำ] [🟡 **ถอนออกจาก `QUEUE_STATUS_SNAPSHOT.md` ชั่วคราว โดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 ตาม `PANYA-ORDER 20260907_0159` ข้อ 2 — เกณฑ์ (ข) โค้ดที่ใบพึ่งพาเปลี่ยนหลังวันเขียนใบ** · เนื้อใบมาจากจดหมาย `20260906_0404` (2026-09-06T04:04+07:00) และอ้าง **เฉพาะ `migrations/003_character_inventory.sql`** · วัดสดบน `origin/main`: **`f03b2fd1` 2026-09-06T14:54+07:00 "LANE-DB: equip-item persistence door (migration 015 + store.py + tests)"** (`migrations/015_character_equipment.sql` +81 · `store.py` +172 · `tests/test_store_character_equipment.py` +208) และ **`fc5ed587` 2026-09-06T15:01+07:00** — ทั้งคู่ `git merge-base --is-ancestor` = **อยู่บน `origin/main` แล้ว** ⇒ เส้นทาง persistence ของอุปกรณ์เปลี่ยนหลังใบถูกเขียน และข้อสมมติของใบที่ว่า "server ยังไม่ตอบ op=5" (ผล NEGATIVE-EXPECTED R321) อาจไม่จริงอีกต่อไป · 🔴 **LANE-K ไม่ได้ตัดสินว่าแขน (ข) ขึ้น main แล้วหรือยัง** — `NOW.md` ยังเขียนว่าแขน (ข) รอ `RE-282` · รอ **LANE-DB (เจ้าของใบ)** ตอบหนึ่งบรรทัดว่าใบยังวัดสิ่งเดิมอยู่หรือไม่ · ใบยังเปิดอยู่ทุกตัวอักษร ไม่ได้ยกเลิกและไม่ได้แตะเนื้อใบ · จดหมาย `notes_to_chief/20260907_0409_LANE-K-CULL-B-gt193-gt272-code-changed-after-ticket.md`] [🟡 **ยังถอนจากสแนปช็อตต่อ — เหตุผลที่บันทึกคือ "รอ seam `1452` + `RE-280` ATTENDED capture" ไม่ใช่ "เจ้าของใบเงียบ"** · LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00 · เจ้าของใบ LANE-DB ตอบแล้วใน `notes_to_chief/20260907_0402_LANE-DB-TO-K-gt272-no-headless-proof-until-seam-1452.md`: ผลิต `HEADLESS_PROOF:` **ไม่ได้** ไม่ใช่ **ยังไม่ได้ผลิต** — วัดบน `pirate-force-server` `8a20214`: `grep "op == 5|op==5|equip_item("` ที่ `runtime.py`+`item_move_capture.py` = **0 hit** · `equip_item(` ทั้ง `src/` เจอแค่ตัวนิยาม `store.py:3579` (ไม่มี caller production) · `ls tools/ | grep headless` = 15 ตัว **ไม่มีตัว equip/item-operate** · ไม่มีใบ `*RE-280*ATTENDED-RESULT*` ใหม่ ⇒ ยังไม่รู้ N-to-slot · 🔴 **K ไม่นับใบนี้เข้าตัววัด "เจ้าของใบไม่เติม `HEADLESS_PROOF:` ใน 2 รอบ"** (`COO-DECISION 0405` ข้อ 3) เพราะเงื่อนไขที่จะเติมได้ยังไม่เกิด · ใบยังเปิดอยู่ทุกตัวอักษร ไม่ยกเลิก ไม่แตะเนื้อใบ]

**คำถามของใบ**: ตัวละคร Gladiator เปิดกระเป๋า กดสวมอาวุธที่ช่องเดิม (`migrations/003_character_inventory.sql` ซีด `template_id=2200002` slot 3 ให้ทุกตัวละครแล้ว) -> เห็นช่องอุปกรณ์เปลี่ยนบนจอ -> relog -> ยังสวมอยู่ (นิยาม "เสร็จ" คำต่อคำของ `0156`)

**พ่วงบูตเดียวกับ**: `RE-272` ได้และควรทำพร้อมกัน — การกดสวมครั้งเดียวตอบทั้งสองใบ (RE จับแพ็กเก็ต, GT จับผลบนจอ) ห้ามพ่วงกับใบที่เปลี่ยนฉาก/ล็อกอินซ้ำก่อนถึงขั้น relog ของใบนี้

ATTENDED: บูตปกติ ไม่มีธง ล็อกอินตัวละคร Gladiator เปิดกระเป๋า ถ่ายภาพช่องอุปกรณ์ก่อนกด
ATTENDED: กดสวมอาวุธช่องกระเป๋าที่มี template `2200002` **หนึ่งครั้ง** ถ่ายภาพช่องอุปกรณ์ทันทีหลังกด
ATTENDED: ล็อกเอาต์แล้วล็อกอินตัวละครเดิมอีกครั้ง (relog แบบเดียวกับ `GT-266`) ถ่ายภาพช่องอุปกรณ์รอบสอง
ATTENDED: ผ่าน = ภาพหลังกด **และ** ภาพหลัง relog ทั้งคู่แสดงอาวุธอยู่ในช่องอุปกรณ์ (ไม่ใช่ในกระเป๋า)
ATTENDED: ไม่ผ่าน = กดไม่ติด (รายงานปัญหาอินพุตตามกติกา 3 ครั้ง) หรือช่องอุปกรณ์ว่างในภาพใดภาพหนึ่ง — ระบุว่าภาพไหน

**เกณฑ์ผ่านสองชั้น**
- **client-observable**: สองภาพ (หลังกด, หลัง relog) แสดงช่องอุปกรณ์มีอาวุธ
- **wire/DB**: ผลจาก `RE-272` ที่จับพร้อมกัน (เฟรมตอบกลับถ้ามี + แถว DB ที่เปลี่ยนถ้ามี) — ใบนี้ไม่อ้างชั้นนี้เอง ถ้า `RE-272` ยังไม่ปิด ให้ผลชั้น client-observable ยืนตามลำพังก่อน

**nonclaims**: ไม่อ้างว่ามีอาวุธในกระเป๋าเพราะเลือกคลาสถูก — ซีด `003` ให้ทุกคลาสเหมือนกัน ไม่ใช่ตรงคลาส (แก้คำอ้างเดิมของ LANE-DB เองตามจดหมาย `0242`) · ไม่อ้างว่าท่าโจมตีเปลี่ยนตามอาวุธที่สวม (คนละกลไกกับทาง (ก) `combat_pose.py` ที่อ่าน `class_id` ล้วน) · ไม่อ้างว่าตัวละครคลาสอื่นนอก Gladiator ได้ผลเดียวกัน

> 🔴 **ห้ามสายอื่นใช้เลข `GT-272`** · numbering: คำสั่งนับเลขของบ้าน คืน **271** (จาก `RE-271` ที่ LANE-CS อ้างถึงใน `GT-243` หัวใบ รอบ `88ej1z`, ยังไม่ลงเนื้อใบเต็ม) ⇒ เลขว่างตัวถัดไปคือ **272** [วัดแล้ว รอบ `ss9u08`/R363] · เลขเดียวกับ `RE-272` ตามที่ LANE-DB ขอ (วางพร้อมกันรอบเดียว)

## GT-276 LEARN-SKILL-RESULT-WALKLOCK-ISOLATE-001  [🟢 **READY -- attended -- เจ้าของใบ/ผู้บริโภคผล = LANE-CS** · ตั้งเลขโดย LANE-K รอบ `slug54r2` 2026-09-06T13:40+07:00 ตามคำขอ `notes_to_chief/20260906_1252_LANE-CS-TO-CHIEF-gt249-grade-plus-walklock-isolate-ticket.md` ข้อ 2 (เนื้อใบวางคำต่อคำจากร่างท้ายจดหมายนั้น) · เลขว่างตัวถัดไปหลัง `GT-274`/`GT-275` (จองไว้ก่อนหน้า ยังไม่วางเนื้อใบ — ไม่ชนกัน) · ยืนยันไม่ซ้ำ: grep `GT-276`/`RE-276` ทั้ง `GAME_TEST_QUEUE.md` `CLIENT_RE_QUEUE.md` `archive/` `notes_to_chief/` `NOW.md` = ไม่เจอที่อื่นก่อนวาง] 🔴 [LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00] เนื้อใบส่วน `boot:`/`ATTENDED:` **ถูกแทนคำต่อคำ** ตามคำขอเจ้าของใบ (`notes_to_chief/20260907_0437_LANE-CS-TO-K-gt-body-gt276-headless-proof-plus-corrected-boot.md`) เพราะใบเดิมสั่งใช้เครื่องมือที่ไม่มีในทรี = ใบตกรถแน่นอน · `HEADLESS_PROOF:` มาแล้วแต่ผูกกับคอมมิต `c6a9a95` ซึ่ง**ยังไม่ใช่ main** ⇒ ยังไม่ขึ้นรถบัส (หมวด ค.) [🟢 **เงื่อนไขข้อ (1) ของเจ้าของใบเป็นจริงแล้ว — K วัดเอง รอบ `rlapyk` 2026-09-07T06:11+07:00** · เจ้าของใบ LANE-CS เขียนเงื่อนไขไว้เองสามข้อ: (1) PR รอบ `li5jc1` เข้า main (2) LANE-CS รันคำสั่งเดิมซ้ำบน main (3) เปลี่ยนเลขคอมมิตในใบ · K วัดสดบนโคลนที่ `git fetch origin main` (`pirate-force-server` head `550a36d`): `git cat-file -e c6a9a95^{commit}` = **มีแล้ว** และ `git merge-base --is-ancestor c6a9a95 origin/main` = **ผ่าน** ⇒ คอมมิตที่ผลิตโทเคน `LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS` **อยู่บน `origin/main` แล้ว** (รอบก่อน `70l5du` วัดตอน main = `e4670a5` ยังไม่มีอ็อบเจกต์นี้) · 🔴 **K ไม่พลิกใบขึ้นรถบัสเอง** — ข้อ (2)(3) เป็นของเจ้าของใบ (พับ=คัดลอก ไม่ใช่ตัดสิน) · จดหมายแจ้ง LANE-CS: `notes_to_chief/20260907_0611_LANE-K-TO-CS-gt276-token-commit-is-on-main-now.md` · ใบจะขึ้นหมวด ข. ของสแนปช็อตในรอบแรกที่ LANE-CS ตอบกลับ] [🟢 **LANE-CS ตอบกลับแล้ว — ใบขึ้นรถบัสได้ (หมวด ก.)** · พับโดย LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00 · จดหมาย `notes_to_chief/20260907_0618_LANE-CS-TO-K-gt276-headless-proof-on-main-550a36d.md` (06:18) · เจ้าของใบทำครบทั้งสามข้อที่ตั้งไว้เอง: (1) `c6a9a95` เข้า main แล้ว (2) รันคำสั่งเดิมซ้ำบนทรี main สะอาด `550a36d` (3) เปลี่ยนเลขคอมมิตในบรรทัด `HEADLESS_PROOF:` ⇒ บรรทัดนั้นถูกแทนคำต่อคำแล้วในเนื้อใบ · 🔴 K ไม่ได้ตัดสินสถานะผลของใบ (ยัง READY เหมือนเดิม ยังไม่มีผลเทส) — เปลี่ยนแค่ 'ขึ้นรถบัสได้/ไม่ได้' ตามหลักฐานที่เจ้าของใบส่งมา]

**คำถามของใบ**: ส่งทีละเฟรมของ sweep 6 ขั้น `learn_skill_result_hypothesis_learn_sweep.json` (คนละรอบจาก `GT-249` ที่ส่งครบ 6 เฟรมรวด) แล้ว "เดินไม่ได้" (พบครั้งแรกใน `GT-249`/R312) มาจากเฟรมไหน

owner/consumer = LANE-CS -- ต้องการ capture บนเครื่อง Panya

HEADLESS_PROOF: 2026-09-07 main 6b5b6b8 | cmd: python3 src/pirateforce_foundation/skill_learn_step_headless.py | LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS
> [LANE-K รอบ `ek1gk9` 2026-09-07T09:4x+07:00] บรรทัดข้างบนวางคำต่อคำจาก `notes_to_chief/20260907_0746_LANE-CS-TO-K-gt276-plain-command-works-on-main-6b5b6b8.md` — เจ้าของใบรันซ้ำเองบนทรี `main` สะอาด `6b5b6b8` โดยไม่ตั้ง env ใด ๆ เลย
> ทำไมต้องเปลี่ยน: ฟอร์มเก่าต้องตั้ง `PYTHONPATH=src` เอง — ka1-A ที่รันโทเคนซ้ำก่อนบูตบนเช็คเอาต์เปล่าจะได้ `ModuleNotFoundError` ไม่ใช่โทเคน = ตัดใบทั้งที่กลไกติดอาวุธจริง (`NOW.md` `0159`)
> ที่ K วัดเอง (ไม่ได้เชื่อจดหมาย): `git merge-base --is-ancestor 6b5b6b8 origin/main` ผ่าน · `git cat-file -e origin/main:src/pirateforce_foundation/skill_learn_step_headless.py` ผ่าน (ไฟล์มีจริงบน main) · K **ไม่ได้** รันโมดูลเอง — ค่าโทเคนเป็นคำของเจ้าของใบ
> บรรทัดเดิม (เก็บไว้ ไม่ลบ — เจ้าของใบยืนยันว่ายังวัดได้จริงบนคอมมิตนั้น): `HEADLESS_PROOF: 2026-09-07 main 550a36d | cmd (บน 550a36d): PYTHONPATH=src python3 -m pirateforce_foundation.skill_learn_step_headless | LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS`
ATTENDED: บูตด้วยไฟล์ขั้นแรก (count0_trail0) เข้าเกม Gladiator lv1 ยืนยันเดินได้ก่อน (baseline)
ATTENDED: พิมพ์แชททริกเกอร์หนึ่งครั้ง (ทริกเกอร์เดิมของ sweep) รอ >=5 วิ แล้วลองเดิน (WASD/คลิกพื้น) ถ่ายภาพ
ATTENDED: เดินได้ = ปิดเซิร์ฟเวอร์ บูตด้วยไฟล์ขั้นถัดไป relog แล้วทำซ้ำ · เดินไม่ได้ = หยุด ขั้นนั้นคือตัวต้องสงสัย
ATTENDED: ดูคอนโซลเซิร์ฟเวอร์ว่าออก action label ชื่อ HYP_PF_033_LEARN_SKILL_RESULT_<LABEL> ครั้งเดียวต่อทริกเกอร์
ATTENDED: ผ่าน = ระบุขั้นที่ล็อกการเดินได้ หรือครบหกขั้นแล้วไม่ล็อกเลย (แปลว่า R312 เจอเงื่อนไขอื่น เขียนตรง ๆ ห้ามเดา)

> 🔴 [LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00] **`c6a9a95` ยังไม่ใช่ `main`** — เจ้าของใบเขียนข้อจำกัดนี้มาเอง: โทเคนมาจากหัวกิ่งรอบ CS `li5jc1` (= `origin/main` + PR ของรอบนั้น) · `NOW.md` บังคับว่า `HEADLESS_PROOF:` ต้องมาจากรัน "บนคอมมิต main ปัจจุบัน" ⇒ **ใบนี้ยังขึ้นรถบัสไม่ได้จนกว่า PR รอบ `li5jc1` เข้า main แล้ว LANE-CS รันซ้ำบน main และยืนยันด้วย `git merge-base --is-ancestor`** · K ไม่ได้นับใบนี้ว่าผ่านล่วงหน้า (ดูหมวด ค. ใน `QUEUE_STATUS_SNAPSHOT.md`) · ห้าบรรทัด `ATTENDED:` เดิมและบรรทัด boot เดิมถูกแทนคำต่อคำจาก `notes_to_chief/20260907_0437_LANE-CS-TO-K-gt-body-gt276-headless-proof-plus-corrected-boot.md` §3/§5

> 🟢 [LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00] **ข้อจำกัดข้างบนหมดอายุแล้ว** — เจ้าของใบ LANE-CS รันซ้ำบนทรี `main` สะอาด `550a36d` เองแล้วส่งบรรทัดใหม่มา (`notes_to_chief/20260907_0618_LANE-CS-TO-K-gt276-headless-proof-on-main-550a36d.md` 2026-09-07T06:18+07:00) · บรรทัด `HEADLESS_PROOF:` ข้างบนถูก**แทนคำต่อคำตามคำขอเจ้าของใบ** (แทนของใบ `0437` และ `0620` เฉพาะสองบรรทัดนั้น) · สองบรรทัดเดิมที่ถูกแทน เก็บคำต่อคำไว้ตรงนี้ ไม่ได้หายไป: `HEADLESS_PROOF: LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS` / `HEADLESS_PROOF: (python3 -m pirateforce_foundation.skill_learn_step_headless) 2026-09-07 commit c6a9a95` · เจ้าของใบยืนยันเองว่า `git merge-base --is-ancestor c6a9a95 origin/main` = จริง แล้ว stash งานของรอบออกก่อนรันบนทรี main เปล่า · หกบรรทัดคอนโซลเต็ม ๆ อยู่ในจดหมายฉบับนั้น · 🔴 **ข้อที่ ka1-A ต้องรู้ (คำของเจ้าของใบ)**: บน `550a36d` คำสั่งต้องมี `PYTHONPATH=src` — ไม่งั้นได้ `ModuleNotFoundError` ซึ่งเป็นช่องว่างของคำสั่ง **ไม่ใช่กลไกไม่ติดอาวุธ** · ถ้า PR รอบ `t04sgo` ของ LANE-CS เข้า main แล้ว ใช้ฟอร์ม `python3 src/pirateforce_foundation/skill_learn_step_headless.py` ได้ โทเคนเหมือนกัน · 🔴 K ไม่ได้รันโทเคนนี้เอง และไม่ได้ตัดสินว่าใบนี้ PASS — คัดลอกอย่างเดียว
boot: หนึ่งขั้น = หนึ่งบูต (โปรเซสหนึ่งรับแผนเดียว โมดูลปฏิเสธการเปลี่ยนแผนกลางคัน)
boot: py -3 -u -m pirateforce_foundation.app --db state\run_gt276_<stamp>.sqlite3 --learn-skill-result-hypothesis-scenario scenarios\learn_skill_result_hypothesis_learn_step_<label>.json
boot: <label> เรียงตามลำดับ: count0_trail0 · count1_trail0 · count1_trail1 · count3_trail0 · count3_trail1 · count4_real_skill_ids_class1_trail0

> [LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00] สามบรรทัด `boot:` ข้างบนแทนบรรทัด boot เดิมทั้งบรรทัด คำต่อคำจาก `notes_to_chief/20260907_0437_LANE-CS-TO-K-gt-body-gt276-headless-proof-plus-corrected-boot.md` §4 (เจ้าของใบ LANE-CS) · บรรทัด boot เดิมที่ถูกแทน: "`py -3 -u -m pirateforce_foundation.app --db state\run_gt276_<stamp>.sqlite3` (ไม่มีแฟล็ก `--*-scenario` ใด ๆ ... รายละเอียดเครื่องมือส่งเฟรมเดี่ยวให้ผู้รันเลือกจากที่มีอยู่แล้วในทรี)" — เจ้าของใบ grep แล้วว่าเครื่องมือนั้น**ไม่มีอยู่ในทรี** (`send_raw` `inject_frame` `single_frame` `raw_frame` `dev_console` = 0 hit ทั้ง `tools/` และ `src/`)

**เกณฑ์ผ่านสองชั้น**
- **client-observable**: ภาพ/บันทึกการเดินไม่ได้ที่ขั้นใดขั้นหนึ่ง (หรือครบ 6 ขั้นไม่ล็อก)
- **wire**: label ของเฟรมที่ส่งไปก่อนแต่ละครั้งลองเดิน (จาก sweep json)

## nonclaims
- ไม่อ้างว่ารู้สาเหตุ "เดินไม่ได้" แล้ว -- แค่รายงานว่าเกิดขึ้นจริงและยังไม่แยกเฟรม (จากจดหมาย `20260905_0154_KA1A-R312-RESULTS-*.md` เอง)
- ไม่อ้างว่า `GT-249` ปิดแล้วด้วยใบนี้ -- ดูข้อ 1 ของคำขอเดียวกัน (พับแยกลงหัวใบ `GT-249` แล้วโดย LANE-K รอบเดียวกัน)
- ไม่อ้างว่าใบนี้เข้าคิวจริงมาก่อนรอบนี้ -- เพิ่งวางเลข+เนื้อใบรอบนี้เป็นครั้งแรก
- ไม่อ้างว่า `production_allowed` ของโมดูลใดขยับรอบนี้ -- ยังคง `False` ทั้งคู่

> numbering: เลขว่างตัวถัดไปหลัง `RE-273`/`GT-274`/`GT-275` (จองไว้ก่อนหน้า ยังไม่ลงเนื้อใบ) ⇒ **276** [ตรวจโดย LANE-K รอบ `slug54r2` — grep ไม่เจอ `GT-276`/`RE-276` ที่อื่นในรีโปก่อนวาง]

## GT-277 LV-SET-CHARACTER-LEVEL-RELOG-001  [✅ **PASS สองชั้น** (ตั้งเลข+วางเนื้อ+พับ+archive ในรอบเดียวโดย LANE-K รอบ `n3s0rg` 2026-09-06T14:10+07:00 ตาม `COO-DECISION 20260906_1346` ข้อ 3(ก) · ผลคำต่อคำจาก R321 §3 · เจ้าของใบ = LANE-GM) -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)]

---

## GT-274 PRODUCTION-ATTACK-POSE-BY-CLASS-CONFIRMED-001  [✅ **PASS ทั้งสองชั้น (arm i เต็ม · arm ii รอ GT-272) — R322B/R322C** 2026-09-07T01:36+07:00 (Gladiator ตี Fighting Fish: จอฟันดาบ · wire `POSE_PRODUCTION class=1 equip_type=1 base=2 behavior=280` (R322B 00:5x) · Paladin look #1 ตี Training Iron Man 916: จอฟาดกระบอง (ดาเมจ 891 ตรงจอ) · wire `POSE_PRODUCTION class=2 equip_type=2 base=3 behavior=284` ×4 (R322C) · arm ii (สวมอาวุธ+relog) ไม่ได้ทำ — GT-272 ยังไม่ผ่าน) · ผลเต็ม `notes_to_chief/20260907_0158_KA1A-R322C-RESULTS-*.md` (`OBSERVER_CONFIRMED 2026-09-07T01:48+07:00`) · พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00 · เดิม: 🟢 **READY -- arm (i) บูตได้ทันที ไม่มีธง (ต้องผ่านกาน "ก่อนบูต (gate)" ด้านล่างก่อน) · arm (ii) พ่วงได้เมื่อ `GT-272` ผ่านก่อนในบูตเดียวกัน** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-CS** · ผู้ตรวจคู่เนื้อใบ (ท่าเป็นเขต B) = LANE-B ไม่ต้องรอ B ก่อนวาง (`COO-DECISION 20260906_0645`) · เปิดตาม `COO-DECISION 20260906_0645` ข้อ 1 -- **ยกเว้น P-2 ในฐานะผู้สืบทอดใบที่สองของ `ATTACK-POSE-ONE-FIELD-AB-001`/`GT-247`** (วัดชนิดเดียว: ท่าเปลี่ยนตามคลาส ไม่วัดสี/ดาเมจ/ดรอป/ตาย) · เลขนับเลขสดเอง (`0434`, ไม่ต้องรอ chief ตั้ง) · **ไม่ปิด `PANYA-ORDER 20260906_0156`** (ปิดด้วย `GT-272` แขน ข ของ DB) และ**ไม่ใช่เกณฑ์ผ่าน M4** (M4 = `GT-224` ของ LANE-B) · v2 แก้ตาม pf-adversary รอบ `rabwxj-adv` (ดูหมายเหตุ v2 ท้ายใบ) · เนื้อใบวาง (v2 คำต่อคำ) โดย LANE-K รอบ `rsmsia` 2026-09-06T15:09+07:00 จาก `notes_to_chief/20260906_0805_LANE-CS-TO-CHIEF-gt274-v2-supersedes-0749-adversary-found-two-real-gaps.md`]

**คำถามของใบ**: บนบูต production ไม่มีแฟล็ก เมื่อตัวละคร Gladiator (class_id=1) ตี Training Iron Man (`n_ID 916`) หนึ่งครั้งที่ยอมรับ ท่าตีบนจอตรงกับดาบตามที่ `GT-247`/R315 ยืนยันแล้วหรือไม่ (BEHAVIOR 280) -- และเมื่อตัวละครอีกตัวที่สร้างใหม่เลือกอาชีพ Paladin ตอนสร้างตัว (look #1 -- ตัวเลือกแรก/ซ้ายสุดในแผงเลือกหน้าตา ณ จอสร้างตัวละคร ถ้าจอไม่มีตัวเลือกแยกชัดเจนให้ใช้ค่าเริ่มต้นที่จอเลือกไว้แล้วบันทึกว่าเลือกโดยไม่ได้กดเปลี่ยน) ตี Training Iron Man ตัวเดิม ท่าต่างจากตัวแรกอย่างเห็นได้ชัดหรือไม่ (คาด BEHAVIOR 284 ค้อน) -- อ่านคู่กับบรรทัดคอนโซล `POSE_PRODUCTION`/`POSE_REFUSED`/`POSE_NO_EQUIP_PROVENANCE` ของ `combat_pose.py` ที่พิมพ์สดต่อฮิต ไม่ใช่สร้างย้อนหลัง

**ก่อนบูต (gate 0/1/2 -- เนื้อจริง ไม่ใช่แค่ชื่อ)**: arm (i) พึ่ง `pirate-force-server` commit `d52cae3` (`CORE-REQUEST 20260905_2242`, ต่อ `class_id=selected.class_id` เข้า `combat_pose` ที่ `runtime.py` บรรทัด ~5172) ต้องเป็นบรรพบุรุษของคอมมิตที่จะบูต -- ตรวจด้วย `git merge-base --is-ancestor d52cae3 <commit ที่จะบูต>` (ผ่าน = เจอ exit 0) แล้วยืนยันซ้ำด้วย `git grep -n "class_id=selected.class_id" <commit นั้น> -- src/pirateforce_foundation/runtime.py` ต้องเจอ 1 บรรทัด -- ใช้ `tools/pf_resolve_green_boot.py` หา `BOOT_COMMIT` ที่ผ่านเกตแล้วรันสองคำสั่งนี้กับ SHA ที่มันคืนมา ห้ามเดา SHA เอง · **ไม่ผ่านสองคำสั่งนี้ = ห้ามบูต**: ตัวละคร Gladiator จะขึ้น `POSE_NO_EQUIP_PROVENANCE` แทน `POSE_PRODUCTION` ทั้งที่ `combat_pose.py` เองไม่มีปัญหา (คอมมิตที่บูตแค่ยังไม่มีสายที่ป้อน `class_id` เข้าไป) -- นี่คือผลลวงที่เช็คนี้มีไว้กันโดยเฉพาะ

**หมายเหตุ (ไม่ใช่ FAIL)**: `persistence_class_id.py`'s docstring เองบันทึกไว้ว่า capture ของคลาสที่สอง (ไม่ใช่ Gladiator) ยังไม่เคยมีใครยืนยันว่า class-selection ตอนสร้างตัวจับคู่กับแถวถูกต้อง (`GT-226` เปิดอยู่) -- ตัวละคร Paladin ที่คืนค่า `class_id` ผิด/`None` ที่ล็อกอินขึ้น `POSE_NO_EQUIP_PROVENANCE reason=no_class_id` ส่วนที่คืนค่าเป็นคลาสอื่นที่ถูกต้องแต่ผิดคาด (เช่น class=4) จะขึ้น `POSE_PRODUCTION class=4 ... behavior=282` ไม่ใช่ `POSE_NO_EQUIP_PROVENANCE` -- ทั้งสองแบบเป็น**ผลลบจริงของคำถามที่สอง** บันทึกบรรทัดคอนโซลจริงเป็น finding ให้ `persistence_class_id.py`/`GT-226` ไม่ใช่ทำให้ใบนี้ FAIL ทั้งใบ (คำถามแรก Gladiator/280 ยังยืนได้ตามลำพัง -- อาศัย `app.py`'s `backfill_missing_class_ids` ที่รันทุกบูตเติม `class_id` ให้ตัวละครเก่าที่แถวยังว่าง ตรวจแล้วว่ามีจริงในบูตปกติไม่มีแฟล็ก)

**ส่วนขยาย (arm ii, ไม่บังคับ)**: ถ้า `GT-272` (DB แขน ข, สวมอาวุธจากกระเป๋าคงอยู่ข้าม relog) ผ่านแล้วในบูตเดียวกัน ให้ตัวละคร Gladiator ตีหุ่นซ้ำอีกครั้งหลังสวมอาวุธ+relog -- คาดว่าท่ายังเป็นดาบ 280 เหมือนเดิม (`combat_pose.py` อ่านอาวุธเริ่มต้นของคลาสเท่านั้น ยังไม่อ่านช่องอุปกรณ์ที่สวมจริง ตามที่โมดูลระบุเป็นรอยต่อที่ยังไม่ต่อ) -- arm (ii) ไม่ผ่าน/ไม่ได้ทำ **ห้ามบล็อก arm (i)**

ATTENDED: บูตปกติ ไม่มีธง (ผ่านกาน "ก่อนบูต (gate)" ข้างบนก่อน) ล็อกอินตัวละคร Gladiator (class 1, ตัวเดิมจาก `GT-116`/`GT-243`/`GT-249`) เดินไปตี Training Iron Man (`n_ID 916`) หนึ่งครั้งที่ยอมรับ ถ่ายภาพท่าตี + คัดลอกบรรทัดคอนโซล `POSE_*` คู่ฮิตนั้น
ATTENDED: ล็อกเอาต์ สร้างตัวละครใหม่เลือกอาชีพ Paladin (look #1) หน้าจอสร้างตัวละคร ล็อกอินตัวใหม่ เดินไปตี Training Iron Man ตัวเดิมหนึ่งครั้งที่ยอมรับ ถ่ายภาพท่าตี + คัดลอกบรรทัดคอนโซล `POSE_*` คู่ฮิตนั้น
ATTENDED: (ถ้า `GT-272` ผ่านแล้วในบูตนี้) ให้ตัวละคร Gladiator สวมอาวุธจากกระเป๋าตาม `GT-272` ขั้น 2 แล้ว relog แล้วตีหุ่นซ้ำหนึ่งครั้ง ถ่ายภาพ + คัดลอกบรรทัดคอนโซลอีกชุด (arm ii ส่วนขยาย ข้ามได้ถ้า `GT-272` ยังไม่ผ่าน)
ATTENDED: ผ่าน = สองภาพแรกต่างกันจริงบนจอ **และ** คอนโซลตัวแรกอ่าน `POSE_PRODUCTION class=1 ... behavior=280` -- ตัวที่สองอ่าน `POSE_PRODUCTION class=2 ... behavior=284` ถือเป็นผ่านเต็ม ถ้าตัวที่สองอ่านอย่างอื่นถือเป็นผ่านคำถามแรกอย่างเดียว + finding แยกตามหมายเหตุข้างบน (ไม่ใช่ FAIL ทั้งใบ)
ATTENDED: ไม่ผ่าน = ตัวแรก (Gladiator) ไม่ขึ้น `POSE_PRODUCTION class=1` หรือท่าไม่ใช่ดาบ หรือคอนโซลไม่มีบรรทัด `POSE_*` เลยคู่ฮิตนั้น **หลังผ่านกาน "ก่อนบูต (gate)" แล้ว** -- ไม่ผ่านกานเองไม่นับ FAIL ให้หยุดก่อนบูตตามที่กานสั่ง

**เกณฑ์ผ่านสองชั้น**
- **client-observable**: ภาพท่าตีของสองตัวละครต่างกันจริงบนจอ (ผู้สังเกตยืนยัน)
- **wire/DB**: บรรทัดคอนโซล `POSE_PRODUCTION`/`POSE_REFUSED`/`POSE_NO_EQUIP_PROVENANCE` ที่ `combat_pose.production_behavior_for_class` พิมพ์สดต่อฮิต (ค่าเดียวกับ selector ที่ประกอบเป็นเฟรม ไม่ใช่ reconstructed) -- ห้ามอ้างชั้นนี้แทนชั้นบน หรือกลับกัน

**nonclaims**: ไม่วัดสีชื่อ ไม่วัด HP ลด ไม่วัดดรอป ไม่วัดตาย (ขอบเขตยกเว้น P-2 แคบเฉพาะท่า -- พบสีผิดระหว่างเทสให้จดเป็นข้อสังเกตของ P-2 ห้ามนับผ่าน/ตกของใบนี้) · ไม่อ้างว่า `persistence_class_id.py` ยืนยันคลาสที่สองถูกต้องเสมอไป -- capture ของ Paladin ในใบนี้คือครั้งแรก ไม่ว่าผลจะออกทางไหน (ดูหมายเหตุข้างบน) · ไม่อ้างว่าอาวุธที่สวมจาก `GT-272` เปลี่ยนท่า -- `combat_pose.py` อ่านอาวุธเริ่มต้นของคลาสเท่านั้น (module docstring, seam ยังไม่ต่อ) · ไม่อ้างว่าใบนี้ปิด `PANYA-ORDER 0156` หรือผ่านเกณฑ์ M4 · ไม่อ้างว่ามอนอื่นหรือใบตีมอนที่วัดดาเมจ/ดรอป/สีได้รับยกเว้นเดียวกัน (ยกเว้นเฉพาะใบนี้กับ `GT-247`/`ATTACK-POSE-ONE-FIELD-AB-001` เท่านั้น)

### result:
อ้างจาก `notes_to_chief/20260907_0158_KA1A-R322C-RESULTS-GT274-PASS-mace-284-GT178-NEGATIVE-no-ai-tick-scene14.md` (R322C, ka1-A attended, OBSERVER_CONFIRMED 2026-09-07T01:48+07:00) คำต่อคำ, ต่อจากครึ่งแรกใน R322B:

> ครึ่งแรก (R322B 00:5x): Gladiator (Arena01) ตี Fighting Fish → จอ: ฟันดาบ · wire: `POSE_PRODUCTION class=1 equip_type=1 base=2 behavior=280`
> ครึ่งหลัง (R322C): สร้างตัวใหม่ **Paladin หน้าตา #1** → ตี Training Iron Man (916) ในเมือง 4 ครั้ง → จอ: **ฟาดกระบอง** (เจ้าของยืนยัน + ภาพ ดาเมจ 891 บนจอ) · wire: `POSE_PRODUCTION class=2 equip_type=2 base=3 behavior=284` ×4 · `damage announced -891, applied 891` HP 192779→189215/198125 ตรงจอ
> ขั้น 3 ของใบ (สวมอาวุธแล้วตีซ้ำ) ไม่ได้ทำ — GT-272 ยังไม่ผ่าน (RE-280) · `TWO_SESSIONS_SAME_SCENE:` ไม่ได้วัด (ผู้เล่นคนเดียว)

RESULT: GT-274 PASS R322C 2026-09-07 01:36 (Paladin mace pose · POSE_PRODUCTION class=2 behavior=284 · Gladiator half class=1 behavior=280 in R322B)

พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว -- ใบนี้อ่าน `class_id` จาก `Character` ที่ผูกกับ session/connection ของผู้ตีเอง (`combat_pose.production_behavior_for_class` ต่อฮิตต่อคน) ไม่แตะ world registry/มอน/ตำแหน่ง/ของพื้น/ศพที่แชร์ข้าม session ตามกฎ shared-world (สอดคล้องกับที่ chief เองตอบไว้ใน `CORE-REQUEST 2242` ที่ใบนี้อ้างอิงโค้ดเดียวกัน)

> 🔴 **ห้ามสายอื่นใช้เลข `GT-274`** · numbering: เลขจองไว้ก่อนหน้า (จดหมาย `0749`/`0805`) ⇒ **274** -- ตรวจซ้ำโดย LANE-K รอบ `rsmsia`: `GT-274`/`RE-274` = 0 hit จริงใน `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md`/`archive/*QUEUE*ARCHIVE*` ก่อนวาง (สองที่ที่ขึ้นตอน grep คือ "จองไว้" ในหัวใบ `GT-276` เท่านั้น ไม่ใช่เนื้อใบซ้ำ)

> v2 (รอบ `rabwxj-adv`): pf-adversary จับได้สองข้อจาก v1 -- (1) ขาดบรรทัด `TWO_SESSIONS_SAME_SCENE:` บังคับตาม `PROCESS_GATES.md` §25 -- เติมแล้วข้างบน (2) วลี "gate 0/1/2 ผ่านก่อนบูต ห้ามเดา SHA" ที่ยกมาจาก `GT-249` เป็นชื่อเปล่าไม่มีเนื้อหา (v1 ไม่มี PR/SHA/grep ให้ตรวจจริง ขณะที่ arm (i) พึ่ง `d52cae3` ที่เพิ่งขึ้น main ~3.5 ชม.ก่อนร่างใบ) -- เติมย่อหน้า "ก่อนบูต (gate)" ให้มีคำสั่งตรวจจริงแล้วข้างบน · แก้เพิ่มสองจุดเล็ก: หมายเหตุ (แยก `POSE_NO_EQUIP_PROVENANCE` ออกจากกรณี class อื่นที่ถูกต้อง) และ "look #1" (นิยามสั้นกันทดสอบเข้าใจผิด)

**ผู้เปิดใบ: LANE-CS (ผ่าน `notes_to_chief/20260906_0749_LANE-CS-TO-CHIEF-gt274-ticket-body-ready-for-numbering.md` + v2 `20260906_0805_*`) -- ตั้งเลข/วาง: LANE-K รอบ `rsmsia` -- ผู้บริโภคผล: LANE-CS**

---

## GT-279 GM-PANEL-BUTTON-CAPTURE-001  [🟡 **ผลสองชั้นแยกทาง — R322B** 2026-09-07T01:17+07:00 (client-observable: PASS — ปุ่ม "ปฏิบัติ" มุมล่างขวา (ไม่ใช่ radio แถว) เป็นตัวส่งจริง กด 5 ครั้งได้ 3 เฟรม `GM_RunGMCommandVital` 0x51E9 บน PC hexdump · wire/server: NEGATIVE — เซิร์ฟตอบ `exact empty RuntimeRes` ทุกครั้ง และ **ไม่มีโฟลเดอร์ `capture/gm_command_capture` ใต้ต้นไม้บูต** ⇒ hook `capture_raw_gm_command` ที่ใบอ้างไม่ได้เขียนไฟล์จริง) · ผลเต็ม `notes_to_chief/20260907_0123_KA1A-R322B-RESULTS-*.md` (`OBSERVER_CONFIRMED 2026-09-07T01:05+07:00`) · พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00 · เดิม: 🟢 **READY -- attended -- ไม่แตะเซิร์ฟเวอร์ (อ่านไฟล์ capture ที่เขียนเองหลังคลิก) ⇒ ขึ้นรถบัส capture คันเดียวกับ `GT-233`/`GT-266`/`GT-269` ได้** · เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-GM · เสนอเวลา: ท้ายรอบ attended ที่บูตอยู่แล้ว ~2 นาที · ตั้งเลข/วางเนื้อโดย LANE-K รอบ `rsmsia` 2026-09-06T15:09+07:00 (เนื้อคำต่อคำจาก `notes_to_chief/20260906_0852_LANE-GM-TO-CHIEF-p3-button-capture-gt-body.md`)]

## ใบ GT ที่ขอ (เนื้อพร้อมลอก — ผมแก้ `GAME_TEST_QUEUE.md` เองไม่ได้)

รอบก่อน (`83wujr`) วัดได้ว่า: `gm/dispatch.py:11,56` เรียก `command_capture.capture_raw_gm_command` ให้กับ **ทุก** เฟรม 0x51E9 ขาเข้า (`GM_RunGMCommandVital`) — ไม่ใช่แค่ประกาศไว้เฉย ๆ — และเขียนไฟล์ลง `capture/gm_command_capture/` (ค่าเริ่มต้นใน `gm/command_capture.py:43`) ยืนยันซ้ำในรอบนี้ (`zaeg4o`) ด้วย grep เดียวกัน: ยังเจอที่บรรทัดเดิม ไม่มีอะไรเปลี่ยน ⇒ คำถาม "ปุ่ม GM ปุ่มไหนส่งอะไร" ไม่ใช่คำถาม RE ที่ต้องมี image เปล่าอีกต่อไป (ไม่มีการรับสายให้สงสัย) แต่เป็นคำถามที่ตอบได้ฟรีจากรถบัส capture ที่บูตอยู่แล้ว: คนกดปุ่มแล้วเปิดไฟล์ที่เขียนไว้ดู

ATTENDED: เปิด GMUI ด้วยปุ่ม GM แบบเดียวกับ GT-207/GT-269 (บูตปกติ ไม่ต้องมีธง ไม่ต้องบัญชีพิเศษ)
ATTENDED: คลิกทีละปุ่ม/แถวที่มี radio ทั้ง 3 หน้า (7/5/5 ตาม GT-269) เว้น 2 วิ ต่อปุ่ม -- ปุ่มที่ทำให้ป๊อปอัปค้างหรือขอ input เพิ่ม ให้กด Cancel/Esc แล้วข้ามไปปุ่มถัดไป (จดชื่อ/ตำแหน่งที่ข้าม)
ATTENDED: หลังคลิกครบ ปิดไคลเอนต์ (ไม่ต้อง logout พิเศษ) แล้วเปิดโฟลเดอร์ capture/gm_command_capture/ บนเครื่องที่รันเซิร์ฟเวอร์ -- นับจำนวนไฟล์ที่ mtime อยู่ในช่วงที่เพิ่งคลิก
ATTENDED: ผ่าน = มีไฟล์ capture อย่างน้อย 1 ไฟล์ที่ mtime ตรงช่วงคลิก -- แนบชื่อไฟล์ + เนื้อ decode section (ส่วน hex dump/decode ที่ command_capture.py เขียน ไม่ใช่ทั้งไฟล์ถ้ายาว) กี่ไฟล์ก็ได้
ATTENDED: ไม่ผ่าน = คลิกครบทุกปุ่มแล้วโฟลเดอร์ว่างเปล่า/ไม่มีไฟล์ mtime ตรงช่วง -- นี่คือผลลบมีค่า (แปลว่าไคลเอนต์ปุ่มเหล่านั้นไม่ส่ง 0x51E9 เลย ไม่ใช่ว่า capture พัง)

> 🔴 [LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00] **เจ้าของใบ LANE-GM (รอบ `wxh2tw`) ขอเติมสองขั้นที่ใบยังไม่มี และเสนอเกณฑ์ผ่านใหม่** — จดหมาย `notes_to_chief/20260907_0556_LANE-GM-TO-K-gt279-allowlist-is-a-sufficient-explanation-not-a-proven-one.md` §2 · **ไม่ใช่การยกเลิกใบ** · ห้าบรรทัด `ATTENDED:` เดิมข้างบนคงไว้ทุกตัวอักษร บล็อกนี้เติมต่อ ไม่แทนที่ · ข้อความข้างล่างยกมาคำต่อคำจากจดหมาย K ไม่แก้สำนวน:

ATTENDED-ADD-A: **ขั้นเตรียมที่ใบยังไม่มี** -- ไม่มีขั้นนี้ ใบจะวัด "ไม่มีอะไรเกิดขึ้น" ซ้ำอีกรอบ: สร้าง `config/gm_accounts.json` ที่รากทรีบูต = `{"gm_accounts": ["<ชื่อล็อกอินที่ใช้เทส>"]}` (หรือชี้ env `PF_GM_ACCOUNTS_CONFIG`) แล้วรีสตาร์ตเซิร์ฟเวอร์ · ตรงตัว case-sensitive · ไฟล์นี้ **จงใจไม่ ship** -- allowlist ในรีโปคือการแจกสถานะ GM ที่มากับ `git pull`
ATTENDED-ADD-B: **ขั้นกดปุ่ม** -- ใบ 279/269 เดิมไม่เคยระบุ และ ka1-A วัดมาแล้วในบูตเดียวกัน: แถวทั้งสามหน้าเป็น **radio เลือกคำสั่ง** ตัวส่งจริงคือปุ่ม **"ปฏิบัติ" มุมล่างขวา**
ATTENDED-ADD-C: เกณฑ์ผ่าน/ไม่ผ่านที่เจ้าของใบเสนอ (สองชั้น แยกกัน) -- client-observable: กด "ปฏิบัติ" แล้ว **จอไม่เปลี่ยน ไม่มีเฟรมตอบ** (เป็นคุณสมบัติ ไม่ใช่ความล้มเหลว -- ผู้เล่นทั่วไปต้องแยกเซิร์ฟที่มี GM ไม่ออกจากการกดปุ่ม) · wire/DB: มีไฟล์ใต้ `capture/gm_command_capture/<UTC>_<account>_0x51E9.txt` · **ถ้าบัญชียังไม่อยู่ใน allowlist**: คอนโซลมีบรรทัดเดียวขึ้นต้น `GM_COMMAND_REFUSED_NOT_GM` บอกไฟล์ที่เปิดจริง · กฎที่เลือก (`argument`/`env`/`default`) · เจอกี่บัญชี (`missing`/`unreadable`/ตัวเลข) -- **ไม่พิมพ์รายชื่อ**

> 🔴 **`HEADLESS_PROOF:` ของใบนี้ยังใช้ไม่ได้ -- ใบยังไม่ขึ้นรถบัส** [LANE-K รอบ `4af3qf`] เจ้าของใบเขียนเองว่าโทเคนอยู่ **บนกิ่ง ไม่ใช่ main** และ "**ต้อง re-derive หลัง merge ก่อนขึ้นรถบัส**" ⇒ ตาม `PANYA-ORDER 0159` ใบนี้ยังไม่มี `HEADLESS_PROOF:` ที่ผ่านเกณฑ์ · โทเคนที่เจ้าของใบส่งมา (เก็บไว้ให้ครบ ไม่ใช่บรรทัด `HEADLESS_PROOF:` ที่ใช้ได้): `GM_COMMAND_REFUSED_NOT_GM account="panya" allowlist="config/gm_accounts.json" source=default accounts=missing` · คำสั่ง `PYTHONPATH=src python3 -m pytest tests/test_gm_allowlist_probe.py -q -s` · ฐาน `origin/main` = `550a36d` · กิ่ง `claude/zealous-hawking-wxh2tw` · K วัดเองรอบนี้: `git cat-file`/`merge-base` บนกิ่งนั้น **ทำไม่ได้จากโคลนที่ fetch แต่ main** ⇒ K ไม่ยืนยันและไม่ปฏิเสธว่ากิ่งนี้เข้า main แล้วหรือยัง -- เจ้าของใบต้องส่งบรรทัดใหม่มาเมื่อ merge

> 🟡 [LANE-K รอบ `4af3qf`] **คำถามปลายเปิดที่ใบผล R322B ทิ้งไว้ (บรรทัด 25: เฟรมไปทาง v141 path หรือ allowlist) -- เจ้าของใบตอบแล้ว แต่ตอบว่า "ยังแยกไม่ได้"** คำต่อคำ: allowlist เป็น **คำอธิบายที่เพียงพอ แต่ยังไม่ได้พิสูจน์ว่าคือสิ่งที่เกิด** (`pf-adversary` รอบนั้นจับได้ว่าร่างแรกสรุปแรงเกินหลักฐาน) · `gm/accounts.py::load_gm_accounts` ถือว่าไฟล์ไม่มี = allowlist ว่าง โดยตั้งใจ · `config/gm_accounts.json` ไม่มีในทรีที่ ship · ⇒ **ถ้า**เฟรมถึง dispatch มันได้ `REFUSAL_NOT_GM` · `captured_path=None` · ไม่เขียนอะไร ตามดีไซน์ · 🔴 **แต่ "เฟรมไม่เคยถึง" กับ "ถึงแล้วถูกปฏิเสธ" ทำนายผลสังเกตเดียวกันเป๊ะ** ⇒ ยังแยกไม่ได้ด้วยหลักฐานวันนี้ · สิ่งที่พิสูจน์ได้แค่: จุดยิง hook มีจริง · โมดูลถูก discover · เส้นทางปฏิเสธ reproduce อาการเป๊ะเมื่อป้อนไบต์จริง

> 🔴 [LANE-K รอบ `4af3qf`] **เรื่องที่แยกออกเป็นใบของตัวเองแล้ว**: เฟรมจริงสามใบจาก R322B **ไม่ผ่าน pin `RE-088` ของ decoder** ⇒ ได้เลขใบแล้ว = **`RE-292`** (ตั้งเลขรอบเดียวกัน `4af3qf` · เนื้อใบจาก `notes_to_chief/20260907_0614_LANE-GM-TO-K-gt279-real-frames-do-not-satisfy-the-re088-pin.md` คำต่อคำ) · ใบนั้นไม่ต้องใช้เครื่องเจ้าของ (มีไบต์จริงแล้ว)

**เกณฑ์ผ่านสองชั้น**
- **client-observable**: ปุ่มไหนกดแล้วมี dialog/ข้อความอะไรขึ้นจอบ้าง (แม้จะเป็น error) — จดทุกปุ่ม
- **wire**: ไฟล์ใน `capture/gm_command_capture/` ที่ mtime ตรงช่วง — เนื้อ decode section บอกว่าไบต์ตรงพิน `RE-088` หรือ `FAILED`

**nonclaims**
- ไม่อ้างว่ารู้ความหมายของฟิลด์ในเฟรม (ชื่อคำสั่ง/อาร์กิวเมนต์) — นั่นคือ `RE-091` คนละใบ (`command_capture.py` docstring บรรทัด 12-13)
- ไม่อ้างว่าปุ่มที่ไม่ส่งอะไรเป็นปุ่ม "เสีย" — อาจเป็นปุ่มที่ยังไม่ผูก handler ฝั่งไคลเอนต์เลยก็ได้ ข้อมูลนี้ตอบไม่ได้จากใบนี้
- ไม่อ้างว่าใบนี้ให้สถานะ GM กับบัญชีไหน — ไม่มีการเปลี่ยนบัญชีในใบนี้
- ไม่อ้างว่า `/lv`/`npc`/`item`/`spawn`/`say` (คำสั่งแชท) ทำงานจากผลใบนี้ — ใบนี้วัดเฉพาะปุ่ม GMUI คนละเส้นกับดิสแพตช์แชท (`gm/chat_command_action.py`)

**grep แล้ว: เจอ/ไม่เจอ** (รอบ `zaeg4o`, ผู้เขียนใบ LANE-GM)
- เจอ: `gm/dispatch.py:11,56` เรียก `capture_raw_gm_command` ทุกเฟรม 0x51E9 ขาเข้า
- เจอ: `gm/command_capture.py:43` `DEFAULT_CAPTURE_ROOT = "capture/gm_command_capture"`
- เจอ: `GAME_TEST_QUEUE.md` GT-269 (READY) ยืนยันว่าเปิด GMUI ด้วยปุ่ม GM ได้จากบูตปกติไม่ต้องมีธง เค้าโครง 7/5/5 แถวสามหน้า
- ไม่เจอ: หลักฐานว่าเคยมีใครกดปุ่มจริงแล้วดู `capture/gm_command_capture/` มาก่อน

**วิธีอ่าน id ที่ไม่มีใครรับ (ตอบ `GM-063` ที่ถูกหักล้าง — COO-DECISION 20260906_1454, ต่อท้ายโดย
LANE-K รอบ `x91eo8` คำต่อคำจากจดหมาย
`notes_to_chief/20260906_1751_LANE-GM-TO-K-gt-body-gt279-add-unclaimed-id-reading-block.md`)**

`runtime.py` พิมพ์สองบรรทัดทุกเฟรมที่มี vital ซ้อน (ไม่ต้องเปิด flag/hook ใหม่ — v141
`IDs=[...]`/`STRUCTURAL_IDS` ก่อน dispatch · `_say_dispatch_nested_vitals`
"DISPATCH_NESTED_VITALS vital_count=%s first_nested_id=0x%04X"). ถ้าอยากรู้ว่า id ที่เห็น
มี branch ไหนใน dispatch รับหรือไม่ ให้ grep ครั้งเดียวตอนอ่านผล (ไม่ต้องพึ่งตารางที่ตายตัว
เพราะรายชื่อนี้เปลี่ยนได้ทุกรอบที่มีคนเพิ่ม branch ใหม่):

    grep -noE "nested_id == [A-Za-z_.]+" src/pirateforce_foundation/runtime.py | sort -u

ผลรอบนี้ (`q7950e` 2026-09-06, อ้างอิงเท่านั้น — รันซ้ำเองเสมอ อย่าเชื่อเลขนี้ข้ามรอบ) คืนชื่อค่าคงที่
26 ตัว (CHAT_INPUT_VITAL_ID, COMMUNITY_*_VITAL_ID ห้าตัว, DELETE_ACTOR_VITAL_ID,
GM_RUN_GM_COMMAND_VITAL_ID, LEARN_SKILL_REQUEST_VITAL_ID, LOGOUT_VITAL_ID,
NAVIGATIONEX_ENTER_INSTANCE_VITAL_ID, PARTY_CMD_VITAL_ID, PARTY_INVITE_VITAL_ID,
PICKUP_LISTENER_VITAL_ID, TRADE_INVITE_VITAL_ID, WORLDINFO_VITAL_ID,
legacy.{ACTION_VITAL,CREATE_ACTOR_VITAL,ITEM_OPERATE_REQ_VITAL,LOGIN_VERIFY_VITAL,
QUEST_OPERATE_VITAL,START_GAME_REQ,TARGET_POS_VITAL,TRIGGER_VITAL},
mob_pickup_request.PICKUP_REQUEST_VITAL_ID, trace_path.TRACE_PATH_REQ_VITAL_ID).
ค่าคงที่แต่ละตัว = เลขฐานสิบหก grep หาที่นิยามได้อีกที (เช่น `grep -rn "GM_RUN_GM_COMMAND_VITAL_ID ="`)

ถ้า `first_nested_id` ที่ปรากฏบนคอนโซลไม่ตรงกับผล grep ด้านบนสักตัว (แปลง match เป็นเลขฐานสิบหก
เทียบ) แปลว่าไม่มี branch ไหนรับ id นั้นตอนนี้จริง ๆ — นี่คือธงที่ COO-DECISION `1454` ข้อ 3
ผูกไว้กับ CORE-REQUEST ใบใหม่ (`GM-064`) ไม่ใช่ก่อนหน้านั้น (`GM-063` เดิมถูกถอนเพราะสมมติฐาน
"ไม่มีใครพิมพ์เลย" ผิด — พิมพ์อยู่แล้วทุกเฟรมโดยไม่ต้องเสียบอะไรเพิ่ม)

nonclaims ของบล็อกนี้ (จาก LANE-GM คำต่อคำ):
- ไม่อ้างว่าเคยเห็น `first_nested_id` ที่ไม่ตรงกับ 26 ชื่อข้างบนจริงบนเครื่อง — บล็อกนี้สอนวิธีเช็ค
  ไม่ใช่ผลของการเช็คแล้ว (ต้องรอ P-3 บูตครั้งแรกตาม `1454` ข้อ 3)
- ไม่อ้างว่ารายชื่อ 26 ตัวนี้จะเหมือนเดิมในรอบถัดไป — `runtime.py` เป็นของ chief แก้บ่อย รันคำสั่ง
  grep เองเสมอ อย่าก็อปตัวเลข/รายชื่อจากใบนี้ไปใช้ข้ามรอบ

### result:
อ้างจาก `notes_to_chief/20260907_0123_KA1A-R322B-RESULTS-GT281-screen-PASS-GT279-execute-0x51E9-x3-bg0002-hostile-gap.md` (R322B, ka1-A attended, OBSERVER_CONFIRMED 2026-09-07T01:05+07:00) คำต่อคำ:

> เจ้าของคลิกทุกปุ่ม/แถว 3 หน้าก่อน → **0 เฟรม** · ka1-A ขับต่อ (computer use): **แถวทั้ง 3 หน้าเป็น radio เลือกคำสั่ง ตัวส่งจริงคือปุ่ม "ปฏิบัติ" มุมล่างขวา** (ใบ 279/269 ไม่เคยระบุ)
> กดปฏิบัติ 5 ครั้ง → client ยิง **`GM_RunGMCommandVital` 0x51E9 3 เฟรม** (PC hexdump หลัง id `E9 51`): หน้า 1 แถว 1 "ตัวละครซ่อนตัว" 44 B · เดิม เลือก "ปรากฏตัว" 44 B (ต่างไบต์เดียว) · หน้า 1 แถว 2 "วาร์ป" ช่องว่าง X/Y/Z=0 46 B — หน้า 2/3 แถวที่มีช่องว่าง client ไม่ส่ง (คาดว่ากันช่องว่างฝั่ง client — nonclaim)
> server: ตอบ `exact empty RuntimeRes` ทุกครั้ง · **ไม่มีโฟลเดอร์ `capture/gm_command_capture` ใต้ต้นไม้บูต** ⇒ hook `gm/dispatch.py → capture_raw_gm_command` ที่ใบอ้าง **ไม่ได้เขียนไฟล์** (ต้องหาว่าเฟรมไปทางไหน — v141 path หรือ allowlist บัญชี) — นี่คือผลลบที่ใบบอกว่ามีค่า

RESULT: GT-279 CAPTURED-CLIENT-NEGATIVE-SERVER R322B 2026-09-07 01:17 (EXECUTE button sends 0x51E9 · 3 frames captured · server empty reply · capture hook wrote nothing)

พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00

> numbering: ตัวนับร่วม (กฎ ②) คืน `278` ⇒ ใบนี้ `279` -- ตรวจ 0 hit `GT-279`/`RE-279` ทั้ง `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md`/`archive/*QUEUE*ARCHIVE*` + ไม่มี RESERVED ใน `NOW.md` ก่อนวาง โดย LANE-K รอบ `rsmsia`

**ผู้เปิดใบ: LANE-GM (ผ่าน `notes_to_chief/20260906_0852_LANE-GM-TO-CHIEF-p3-button-capture-gt-body.md`) -- ตั้งเลข/วาง: LANE-K รอบ `rsmsia` -- ผู้บริโภคผล: LANE-GM**

---

## GT-281 BASIC-FACTION-EVERY-LOGIN-SCENE-SEA-126-001  [✅ **PASS ทั้งสองชั้น — R322B** 2026-09-07T00:55+07:00 (client-observable: login กลางทะเลผ่าน return ticket → `/warp 2` → Fighting Fish ชื่อชมพู ไม่เขียว คลิกโจมตีติด มอนตาย · wire: `PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` บน login ทะเล) · หลอดฟ้าใต้ชื่อ/HP -1 ยังอยู่แต่วัดแล้วว่าไม่ใช่เรื่อง faction — แยกเป็นใบสร้างใหม่ของ A/DB (BoatHealth ไม่ถูกตั้งกลับเป็น HP ตัวละครตอนออกจาก 126) ไม่ใช่เกณฑ์ตกของใบนี้ · ปลดล็อก GT-220/GT-223 · ผลเต็ม `notes_to_chief/20260907_0123_KA1A-R322B-RESULTS-*.md` (`OBSERVER_CONFIRMED 2026-09-07T01:05+07:00`) · พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00 · เดิม: 🟢 **READY — ชั้น wire PASS R322A** (`PLAYER_FACTION basic_faction=1` on sea login) · ชั้นจอ NOT MEASURED ยัง เหลือ `/warp 2` ดูสีชื่อมอน (ผล `notes_to_chief/20260906_1909_KA1A-R322A-RESULTS-*.md` · เติมโดย LANE-K รอบ `cu7c2r` ตาม `COO-DECISION 20260906_1955` ข้อ 1) — precondition ปลดแล้ว ตรวจสดโดย LANE-K รอบ `cm9v9y` 2026-09-06T17:10+07:00: `pirate-force-server` PR `#1501` (LANE-A round `q02brx`) merge เข้า `origin/main` (`b9a552d`) แล้ว · `git show origin/main:src/pirateforce_foundation/world_faction_admission.py` ยืนยัน `admits()` ไม่เช็ค registry อีกต่อไป ("every scene a login can legally carry ... is admitted") ตรงเงื่อนไขที่ตั้งไว้ ~~[เดิม: 🔴 BLOCKED-ON-WIRING จนกว่า PR ของรอบนี้ (`pirate-force-server` LANE-A round `q02brx`, แก้ `world_faction_admission.admits` ให้ไม่เช็ค registry — ทุกฉากที่ login ได้ = ได้ faction) จะขึ้น main]~~ · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A** · ตั้งเลขโดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 ตาม `NOW.md` ("P-2 ชั้นแรกเจอต้นเหตุ ... LANE-A งานแรกรอบถัดไป ส่งfaction ทุก login scene + ใบ GT (`1347`)") · เนื้อใบมาจากจดหมาย `notes_to_chief/20260906_1515_LANE-A-TO-K-gt-body-basic-faction-every-login-scene.md` คำต่อคำ · อ้าง: `COO-DECISION 20260906_1347` · `KA1A-R321-RESULTS §1`]

**คำถาม**: login ผ่านตั๋ว relog เข้าฉาก 126 (ทะเล, Atlantis ocean panel) ทำให้ผู้เล่นได้ `basic_faction` เหมือน login บกหรือไม่ — และหลัง `/warp 2` มอนในฉาก 2 ตีได้ปกติหรือไม่ (ก่อนหน้านี้ login ผ่าน 126 ทำให้ผู้เล่นไร้ฝ่ายถาวรทุกฉากจนกว่าจะ login ใหม่บนบก — `KA1A-R321 §1`)

**เกณฑ์สองชั้น**:
- ชั้น client-observable (บนจอ): `/warp 126` (ต้องเป็นบัญชี GM ที่มีตั๋ว relog) → ออกเกม → login ใหม่ (เกิดกลางทะเล Rising Sun Sea) → `/warp 2` → **ชื่อมอน Fighting Fish ต้องไม่เขียว คลิกโจมตีได้** · **ตัวละครต้องไม่มีหลอดสีฟ้าเหนือหัว**
- ชั้น wire (เทียบไบต์เฟรม `FOUNDATION_SELECTED_START_GAME` ตอน login เข้า 126): ต้องมี mask `0x074F` (ไม่ใช่ `0x034F`) และมีฟิลด์ `basic_faction=1` (`14 01 00 00 00` หลัง scene block) — เทียบกับ `KA1A-R321` ภาคผนวก B

ATTENDED: กด/พิมพ์: `/warp 126` (บัญชี GM ที่อยู่ใน allowlist) → ปิด client → เปิดใหม่ login → `/warp 2`
ATTENDED: ดู: ชื่อมอน Fighting Fish ในฉาก 2 (สีเขียว=FAIL, สีอื่น=ผ่านเกณฑ์นี้) · หลอดสถานะเหนือหัวตัวละคร (มี=FAIL)
ATTENDED: ผ่าน/ไม่ผ่าน: ตัดสินจากสีชื่อมอน + คลิกโจมตีได้ + ไม่มีหลอดฟ้า — ไม่ใช่จากตัวเลข HP (P-2 สีชื่อมอนที่ถูกต้องยังเป็นชั้นแยก B ไม่เกี่ยวกับใบนี้)
ATTENDED: บูต: ไร้ธง ไร้ env (FLAGLESS) · ต้องมีบัญชี GM ในตั๋ว relog 126 (ดู `tests/test_gm_warp_relog_stage.py`)
ATTENDED: 🆕 ชั้น wire ผ่าน R322A แล้ว (`PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` ที่ login 126 ผ่าน return ticket 2026-09-06T18:40+07:00) — เหลือแค่ `/warp 2` ดูสีชื่อมอนบนจอ (ชั้น client-observable) เท่านั้น · เติมโดย LANE-K รอบ `cu7c2r` ตาม `COO-DECISION 20260906_1955` ข้อ 1 · ผล `notes_to_chief/20260906_1909_KA1A-R322A-RESULTS-*.md`

**nonclaims**
- ไม่ยืนยันสีมอนที่ "ถูกต้อง" ตามเกณฑ์ P-2 (เหลือง/ส้ม/แดง/เทา) — ใบนี้วัดแค่ "ไม่เขียว/ตีได้/ไม่มีหลอดฟ้า" (อาการของ §1) เท่านั้น

**links**: `COO-DECISION 20260906_1347` (`notes_to_chief/20260906_1347_COO-DECISION-ka1a1255-...-LANE-A.md`) · `KA1A-R321-RESULTS §1` (`notes_to_chief/20260906_1255_KA1A-R321-RESULTS-...md`) · PR pf_bridge (claim `[LANE-A] round q02brx`) · PR pirate-force-server (round q02brx)

### result:
อ้างจาก `notes_to_chief/20260907_0123_KA1A-R322B-RESULTS-GT281-screen-PASS-GT279-execute-0x51E9-x3-bg0002-hostile-gap.md` (R322B, ka1-A attended, OBSERVER_CONFIRMED 2026-09-07T01:05+07:00) คำต่อคำ:

> ขั้น: login Arena01 ฉาก 1 → `/warp 126` (วาปสด) → X → relaunch (1545) → login **ลงทะเล 126 ผ่าน return ticket** (`WORLD_SCENE scene_id=126 … return_ticket=REQUIRED` บรรทัด 1245) → `/warp 2`
> wire: `PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` **บน login ทะเล** (บรรทัด 1248) — สิ่งที่ R321 ไม่มี
> จอ (Panya + ภาพ): Fighting Fish soldier ชื่อ**ชมพู ไม่เขียว** · คลิกโจมตีติด · มอนตาย · wire: `damage announced -966, applied 966, hp 3138 -> 2172` (max HP ตรงตาราง 3138)
> **หลอดฟ้าใต้ชื่อ + แผงตัวเอง HP -1**: ยังมีอยู่ **ทั้งที่ faction มาครบ** ⇒ **ไม่ใช่เรื่องฝ่าย** — R321 โยงหลอดกับ faction **ผิด** — ขอให้ A แยกเกณฑ์ "ไม่มีหลอดฟ้า" ออกจากใบ 281 ไปเป็นใบสร้างของ A/DB
> **ปลดล็อก**: GT-220 / GT-223 (BLOCKED จน GT-281 ผ่านจอ) เดินต่อได้

RESULT: GT-281 PASS R322B 2026-09-07 00:55 (sea login ships basic_faction=1 · /warp 2 mob names pink not green · attack+kill OK · blue bar = boat HP not restored, separate ticket)

พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00

> numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน **280** (`RE-280`, ตั้งเลขรอบเดียวกัน `zqq4qz` ก่อนหน้าใบนี้) ⇒ ใบนี้ **281** · ตรวจ 0 hit ของ `GT-281`/`RE-281` ทั้งสามที่ (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*.md`) + ไม่มี RESERVED ใน `NOW.md` ก่อนวาง [ตรวจโดย LANE-K รอบ `zqq4qz`]

**ผู้เปิดใบ: LANE-A (ผ่าน `notes_to_chief/20260906_1515_LANE-A-TO-K-gt-body-basic-faction-every-login-scene.md`) -- ตั้งเลข/วาง: LANE-K รอบ `zqq4qz` -- ผู้บริโภคผล: LANE-A**

---

## GT-284 WORLD-SCENE-STATE-SURVIVES-RELOGIN-001  [🔴 **BLOCKED** จนกว่าจะครบสองอย่าง: (ก) `CORE-REQUEST world_scene_registry.WORLD_REGISTRY_SEED_WIRING` ลง main (ข) LANE-B เรียก `note_balance` ที่จุดรับหมัด — ตรวจซ้ำสดรอบ `zqq4qz`: grep `\.note_balance(` ใน `pirate-force-server/src/` = ไม่พบ call site จริง (พบแค่ docstring/comment) ⇒ ยังไม่ต่อสาย ทั้งสองข้อยังไม่ลง main [ตรวจโดย LANE-K รอบ `zqq4qz`] · **ห้ามเรียก Panya จนสองข้อนั้นอยู่บน main** (เขียนไว้ในจดหมายต้นทางเอง) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A** · ตั้งเลขโดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 (คำขอค้างจากรอบ `tz2rgc` 2026-09-05 — จดหมายส่งถึง chief แต่รูปแบบเป็นคำขอเลขใบ GT ตามนิยามของ `prompts/LANE-K.md`) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260905_1340_LANE-A-TO-CHIEF-world-registry-landed-gt-body-relogin-needs-a-number.md` คำต่อคำ · = เกณฑ์ผ่านเดียวของ shared world ตาม `COO-DECISION 20260905_1152` ข้อ 3]

**หัวเรื่อง**: โลกของฉากเดิมต้องอยู่ตรงนั้นหลัง relogin โดยเซิร์ฟเวอร์ไม่รีบูต

precondition: เซิร์ฟเวอร์ **ห้ามปิด/รีสตาร์ตระหว่างใบนี้** (รีบูต = โลกใหม่โดยกติกา `PANYA-DECISION 20260905_1224` ⇒ รีบูตกลางใบ = ใบนี้เป็นโมฆะ ไม่ใช่ FAIL)

ATTENDED: เข้าฉากที่มีมอน (เช่น Bg0002) · จดบรรทัด `WORLD_REGISTRY_VIEW` บรรทัดแรกไว้ (ค่าตั้งต้น)
ATTENDED: ตีมอนตัวหนึ่งให้บาดเจ็บแต่ไม่ตาย (แถบเลือดลดแต่ยังยืน) แล้วฆ่ามอนอีกตัวหนึ่งจนของตกพื้น 2 ชิ้น **ห้ามเก็บของ**
ATTENDED: ปิดไคลเอนต์ด้วย X แล้วล็อกอินกลับเข้าตัวละครเดิม ฉากเดิม (**เซิร์ฟเวอร์ยังรันอยู่ ห้ามปิด**)
ATTENDED: จดบรรทัด `WORLD_REGISTRY_VIEW` ของการเข้าฉากครั้งที่สอง
ATTENDED: บูตปกติ ไม่ต้องมีธง/env พิเศษ

**เกณฑ์ผ่าน (สองชั้น ต้องครบทั้งคู่)**
- **บนจอ**: มอนที่บาดเจ็บ **ยังบาดเจ็บเท่าเดิม** (ไม่กลับมาเลือดเต็ม) · ศพของตัวที่ตาย **ยังเป็นศพ** · ของ 2 ชิ้น **ยังอยู่ที่เดิมและเก็บได้**
- **คอนโซล**: `WORLD_REGISTRY_VIEW` ของขั้น 4 ให้ตัวเลข `monsters=`/`graves=`/`ground=` **ไม่น้อยกว่า** ของขั้น 1 และมีบรรทัด `WORLD_REGISTRY_SEEDED scene=<ฉาก> monsters=<n>` อย่างน้อยหนึ่งบรรทัดในการล็อกอินครั้งที่สอง

**เกณฑ์ไม่ผ่าน (พฤติกรรมวันนี้)**: มอนกลับมาเลือดเต็ม · หรือ `monsters=0` ทั้งที่เพิ่งตีไป (ไม่ใช่ FAIL ถ้ายังไม่ครบสอง precondition ข้างบน — คือ "ยังไม่ต่อสาย")

**nonclaims**
- ไม่อ้างว่า `mob_death_persistence`/`mob_ground_persistence` (ของ LANE-B) เปลี่ยนพฤติกรรมจากใบนี้ — ใบนี้วัดเฉพาะ "เลือดมอนที่ยังไม่ตาย + ตำแหน่งล่าสุด" ผ่าน `world_scene_registry.py` เท่านั้น

**links**: `world_scene_registry.py` (LANE-A, `pirate-force-server`) · `COO-DECISION 20260905_1152`/`1153` · `PANYA-DECISION 20260905_1057`/`1140`/`1224` · `rounds/A_20260905_1324_tz2rgc_*.md`

### result:
(ว่าง)

> numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน **283** (`RE-283`, ตั้งเลขรอบเดียวกัน `zqq4qz`) ⇒ ใบนี้ **284** · ตรวจ 0 hit ของ `GT-284`/`RE-284` ทั้งสามที่ + ไม่มี RESERVED ใน `NOW.md` ก่อนวาง [ตรวจโดย LANE-K รอบ `zqq4qz`]

**ผู้เปิดใบ: LANE-A (ผ่าน `notes_to_chief/20260905_1340_LANE-A-TO-CHIEF-world-registry-landed-gt-body-relogin-needs-a-number.md`) -- ตั้งเลข/วาง: LANE-K รอบ `zqq4qz` -- ผู้บริโภคผล: LANE-A**

---

## GT-287 DEATH-OUTLIVES-THE-CONNECTION-001  [PENDING] -- objective: มอนสเตอร์สนามที่ถูกฆ่าแล้ว "ตายค้าง" ข้ามการเชื่อมต่อ (ARM A logout/login ตัวเดิม · ARM B ตัวละครที่สอง) -- เนื้อใบเต็ม (steps/pass criteria/nonclaims) อยู่ที่ `tickets/GT-287.md` (>8,192 B ตั้งแต่เกิด, per `PANYA-ORDER 1448`) · เจ้าของใบ = chief (LANE-E) ต่อสาย DEATH_SEED_WIRING · ผู้เทส/ผู้บริโภคผล = LANE-B/chief · ตั้งเลขโดย LANE-K รอบ `hf1gs9` 2026-09-06T23:17+07:00 · เนื้อใบมาจากจดหมาย `notes_to_chief/20260906_2030_FROM_CHIEF-TO-K-gt-body-death-seed-relog.md` คำต่อคำ

owner: chief (LANE-E)
ATTENDED: บูตตาม `ATTENDED_SESSION_RUNBOOK.md` บนสำเนา `state\run_gtK.sqlite3` (ห้ามเปิด canonical เทียบ sha ก่อน/หลัง) เซิร์ฟก่อนไคลเอนต์ทีหลัง เก็บคอนโซล `2>&1` -> ล็อกอินตัวละคร A เข้า Port Royal (ฉาก 1 `bg0001`) ถ่ายภาพ #1 -> คลิกตีหุ่น Training Iron Man หนึ่งตัวจนตาย (~223 ครั้ง 891 dmg ต่อครั้ง 198125 HP) ถ่ายภาพ #2 -> logout ด้วยปุ่ม X + ยืนยัน -> ล็อกอินตัวเดิมกลับเข้ามา ถ่ายภาพ #3 คลิกตัวที่ฆ่าถ่ายภาพ #4 -> logout อีกครั้ง ล็อกอินตัวละครที่สอง ถ่ายภาพ #5
ATTENDED: ชั้น wire/DB ดูสามโทเคนตามลำดับ `MOB_DEATH_WORLD_SEEDED ... admitted=0 ... identities=none` (ล็อกอิน **แรก** ของบูตเท่านั้น) -> `MOB_DEATH_WORLD_REMEMBERED ... identity=0x20XX ... max_hp=198125` (ตอนฆ่า จด identity) -> `MOB_DEATH_WORLD_SEEDED ... admitted=1 buried=1 skipped=0 identities=0x20XX ledger_zeroed=1` (หลังล็อกอินกลับ และอีกครั้งหลังตัวละครที่สอง) · ชั้นจอดูภาพ #3/#5 เทียบ #1 จากมุมเดียวกัน: หุ่นตัวที่ฆ่ายังไม่ยืนเต็มหลอด
ATTENDED: PASS ต้องได้ทั้งสองชั้น ห้ามใช้ชั้นหนึ่งแทนอีกชั้น · FAIL คือ มีโทเคนที่ 1 และ 2 แต่ **ไม่มี** โทเคนที่ 3 **และ** บนจอหุ่นตัวเดิมยืนเต็มหลอดตีแล้วขึ้นเลขดาเมจสด · ไม่มีโทเคนที่ 1 เลย = NO-RESULT บูตใหม่ · ตีไม่ครบจนตาย = NO-RESULT · เจอ `MOB_RESPAWN` หรือเผลอข้ามฉาก = ปนเปื้อน NO-RESULT ทั้งหมดนี้ไม่ใช่ FAIL
ATTENDED: บูตปกติ ไม่มีแฟล็ก `--*-scenario` ไม่มี env พิเศษ ไม่มี chat trigger (ห้ามพิมพ์อะไรเลยทั้งรอบ ตัวอักษรตอนช่องแชทไม่โฟกัสกลายเป็นฮอตคีย์) · ทรีต้องมีบรรทัด `mob_death_persistence.seed_the_session_state(...)` ใน `runtime.py::_sync_combat_scene_state` บน main · 🔴 ห้าม End task ไคลเอนต์ ห้ามรีสตาร์ตเซิร์ฟเวอร์ระหว่างฆ่ากับล็อกอินกลับ (โปรเซสใหม่ = โลกใหม่ สมุดหลุมศพหายหมด) ห้าม `/warp` ห้ามข้ามแมพ · teardown ต้องรันเสมอแม้เลิกเล่นกลางคัน จด boot stamp ตั้งแต่ต้น (เทมเพลตปฏิเสธ stamp เก่ากว่า 420 นาที)
ATTENDED: จดลงผล — identity ที่ฆ่า (`0x2068`/`0x206A`/`0x206C`/`0x206E`) · จำนวนครั้งที่ตีจริง · เวลาห่างระหว่างตายกับล็อกอินกลับ · ตัวละคร/บัญชีที่ใช้ใน ARM B (ถ้ามีตัวเดียว ARM B = NO-RESULT) · sha canonical ก่อน/หลัง · `sessions` และ `max(lease_generation)` ก่อน/หลัง · **สีป้ายชื่อทุกป้ายในทุกภาพจากภาพเต็มความละเอียด หนึ่งบรรทัดต่อหนึ่งป้าย เขียน `none` ถ้าไม่มี ห้ามอ่านจากภาพย่อ/วิดีโอ ห้ามอนุมานสาเหตุจากสี** · เช็ค NO-CRASH ด้วยคลิกขวาค้างลากเท่านั้น
body: `tickets/GT-287.md`

### result:
(ว่าง)

> 🔴 **ห้ามสายอื่นใช้เลข `GT-287`** · numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` + `tickets/` คืนสูงสุด **286** (`RE-286`, ตั้งเลขรอบ `camatf` 2026-09-06T22:17+07:00) ⇒ ใบนี้ **287** · ตรวจ 0 hit ของ `GT-287`/`RE-287` ครบสี่ที่ (live สองคิว · `archive/*QUEUE*ARCHIVE*` · `tickets/`) + ไม่มี RESERVED ใน `NOW.md` ก่อนวาง [ตรวจโดย LANE-K รอบ `hf1gs9`]

**ผู้เปิดใบ: chief (LANE-E) (ผ่าน `notes_to_chief/20260906_2030_FROM_CHIEF-TO-K-gt-body-death-seed-relog.md`) -- ตั้งเลข/วาง: LANE-K รอบ `hf1gs9` -- ผู้บริโภคผล: LANE-B/chief**

---

## GT-288 NAME-COLOUR-SWEEP-DUMMY-ROW-001  [PENDING -- หมายเหตุจากผู้เปิดใบ (B): สปาวน์เนอร์ยังไม่ต่อสายเข้า runtime.py/app.py จนกว่าจะมี CORE-REQUEST แยกต่อสาย env -> dispatch ใบนี้ยังบูตขึ้นจริงไม่ได้ · 🔴 เงื่อนไขที่สอง (chief ถอนคำสั่งตัวเอง `20260907_0345`, พับโดย LANE-K รอบ `kxpzxi` 2026-09-07T03:13+07:00): **ห้ามขึ้นรถบัส attended** จนกว่า chief ส่งใบยืนยันว่าแก้เป็น **เฟรมเดียวผนวกเข้า census** ลง main แล้ว -- เฟรม collection แยกจะลบ NPC ทั้งเมืองออกจากจอ (RE-092 replace-by-omission) ทำให้ตัวควบคุม `N-BASE` ใช้ไม่ได้ · คำสั่ง "รอ 4 วินาที" และรายการป้ายชื่อในบล็อก `0250` **ถูกถอนแล้ว** (ค่าที่ถูก: รอ >=8 วินาที · ชุด `=1` ไม่มี `N-AT3`/`N-SKIN`) -- ดูบล็อก "ใบถอนของ chief" ใน `tickets/GT-288.md`] -- objective: "RE-155 ใบแรกของ B ตามเส้นตาย 02:00 -- แถวหุ่นทดลอง สองต้นแบบ (NPC + Training Iron Man 916) พร้อมโค้ดสปาวน์ รายการผู้สมัคร บล็อก ATTENDED" (คำต่อคำจากหัวจดหมาย) -- เนื้อใบเต็ม (steps/pass criteria/ตารางผู้สมัคร) อยู่ที่ `tickets/GT-288.md` (>8,192 B ตั้งแต่เกิด, per `PANYA-ORDER 1448`) · เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้ทดสอบ = LANE-B (ตาม PANYA `2142`+`2150` ใน `NOW.md`: "เจ้าของ = B") · ผู้บริโภคผล = LANE-B/COO/Panya · ตั้งเลขโดย LANE-K รอบ `6rj6h1` 2026-09-07T01:09+07:00 (ก่อนเส้นตาย NOW `07 ก.ย. 02:00`) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_0021_LANE-B-TO-K-gt-body-RE-155-dummy-row-npc-and-916-sweep.md` คำต่อคำ 🔴 [LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00] **บล็อก `ATTENDED:` ใหม่ (เฟรมเดียวผนวกเข้า census) วางแล้วใน `tickets/GT-288.md`** คำต่อคำจาก `notes_to_chief/20260907_0341_FROM_CHIEF-TO-K-re155-one-frame-with-the-census.md` ซึ่งแทนบล็อกในจดหมาย `0250` และ `0345` ทั้งสองใบ · บล็อกเดิมของ LANE-B ไม่ถูกลบ แต่ห้ามใช้บูต · **ยังไม่ขึ้นรถบัส**: chief เขียนเองว่าโค้ดอยู่ใน `pirate-force-server#981` (draft) **ยังไม่ใช่ main** และ "ยังไม่จัดคิวจนกว่าผมส่งใบว่า merge แล้ว" ⇒ ใบยังอยู่หมวด **ง. ตกรถ** · ยังไม่มี `HEADLESS_PROOF:` (โทเคน census มาจากกิ่ง ไม่ใช่ main) · 🔴 **ชุด 2 (`=2`) ห้ามบูต** — `N-AT3`/`M-AT3` ใช้ `actor_type=3` (`CMyActor`) ซึ่ง thunk `+0x38` ของ `NPCAttr` รับเฉพาะ `CNetNPC` (4,5) ⇒ ได้ทั้ง FAIL ปลอมและ PASS ปลอม รอ LANE-B ตัดผู้สมัครใหม่ (3 -> 5 `CAvatarNPC`) [🟡 **ยังเป็น PENDING ต่อ — เจ้าของใบ LANE-B ตอบ K แล้วว่า "ยังพลิก READY ไม่ได้"** · วางโดย LANE-K รอบ `rlapyk` 2026-09-07T06:11+07:00 · จดหมาย `notes_to_chief/20260907_0441_LANE-B-TO-K-gt288-cannot-flip-ready-no-caller-on-main.md` · ถ้อยคำเจ้าของใบคำต่อคำ: "ไม่ใช่เพราะ B ไม่ยอมพลิก แต่เพราะเขียนบรรทัด `HEADLESS_PROOF:` ให้เป็นจริงไม่ได้บนคอมมิต main ปัจจุบัน" · สิ่งที่เจ้าของใบวัด (บน `pirate-force-server` `70e6018`): โมดูล `src/pirateforce_foundation/name_colour_sweep.py` อยู่บน main จริง แต่ `git grep -n "name_colour_sweep" origin/main -- '*.py'` เจอแค่ตัวไฟล์เอง + คอมเมนต์ใน `tools/pf_runtimeres_actor_entry_static.py` ⇒ **ไม่มีผู้เรียกใน `src/`** · `git grep -rn "sweep_entries\|NAME_COLOUR_SWEEP_UNARMED" origin/main` = 0 แถว · บูต headless ด้วย `PF_NAME_COLOUR_SWEEP=1` ไม่มีโทเคนออกคอนโซล · **K ต้องทำอะไร: "ยังไม่ต้องทำอะไร" (คำของเจ้าของใบ)** ⇒ ใบคงสถานะเดิม ไม่ขึ้น `QUEUE_STATUS_SNAPSHOT.md` · ผู้สมัคร `actor_type` เปลี่ยน 3 -> 5 (`CAvatarNPC`) แล้วโดย B แต่ **อยู่ใน `pirate-force-server#990` ซึ่ง `notes_to_chief/20260907_0604_SYNC-NOTICE-pirate-force-server-pr990-closed-never-merged.md` แจ้งว่าถูกปิดโดยไม่ merge (gate RED)** — งานยังอยู่บนกิ่ง `claude/magical-albattani-b08g3z` · คำถามป้ายชื่อของ AT5 ได้เลขใบแล้ว = **`RE-290`** (ตั้งเลขรอบเดียวกัน `rlapyk`) · nonclaim ที่เจ้าของใบยกมาด้วย: ใบนี้ไม่ได้บอกว่าสีบนจอเป็นอะไร และไม่ได้บอกว่า `actor_type 5` จะเรนเดอร์จริง] [🟢 **เงื่อนไขที่เจ้าของใบ LANE-B ตั้งไว้เองเป็นจริงแล้ว — K วัดเอง รอบ `rlapyk` 2026-09-07T06:11+07:00** · จดหมาย `0441` ของเจ้าของใบเขียนว่า B จะส่ง `*-TO-K-*` พลิก READY "ในรอบแรกที่ `git grep -n \"name_colour_sweep\" origin/main -- 'src/*.py'` มีผู้เรียกจริง" · K วัดสดบน `pirate-force-server` head `550a36d`: **มีผู้เรียกแล้ว** — `runtime.py:27` `from . import name_colour_sweep` และ `runtime.py:12095` `sweep_bodies = name_colour_sweep.sweep_entries(` พร้อมโทเคน `NAME_COLOUR_SWEEP_ARMED` (`runtime.py:12202`) / `NAME_COLOUR_SWEEP_UNARMED value=` (`12231`) / `NAME_COLOUR_SWEEP_REFUSED` (`12105`) · เทียบกับรอบ `b08g3z` ที่ B วัดบน `70e6018` แล้วเจอ 0 แถว ⇒ ตัวเชื่อมลง main ระหว่างสองคอมมิตนี้ · 🔴 **K ไม่พลิก READY เอง และไม่เขียน `HEADLESS_PROOF:` ให้ใคร** — เจ้าของใบต้องรัน headless เองบน main แล้วส่งโทเคนมา (พับ=คัดลอก) · จดหมายแจ้ง LANE-B: `notes_to_chief/20260907_0611_LANE-K-TO-B-gt288-the-caller-you-waited-for-is-on-main.md`]
> ✅ [LANE-K รอบ `wb8tfv` 2026-09-07T11:10+07:00] **`RE-290` ตอบแล้ว ⇒ ชุด 2 คงผู้สมัคร `actor_type 5` ไว้ ไม่ถอน** — พับจากจดหมายเจ้าของใบ `notes_to_chief/20260907_1046_LANE-B-re290-consumed-gt288-set2-stays.md` (LANE-B รอบ `abibfm` 2026-09-07T10:46+07:00) ซึ่งบริโภคผล `notes_to_chief/20260907_1027_RE-290-RESULT-cavatarnpc-builds-the-same-nameboardnpc-as-cnetnpc.md` · **K คัดลอก ไม่ได้ตัดสิน** · เงื่อนไขที่ใบ `RE-290` ตั้งไว้เอง: ตอบ `0x45C560` ⇒ ชุด 2 พร้อม · ตอบอย่างอื่น ⇒ ถอนผู้สมัครทั้งชุด — RE ตอบ `[0xF0DFF8 + 0x7C] = 0x0045C560` ⇒ **ชุด 2 เดินต่อ** (`CAvatarNPC` AT5 และ `CNetNPC` ชี้ initializer ป้ายชื่อตัวเดียวกัน `NameBoardNPC`, `push 0xC0`)
> ↳ 🔁 **ประโยคเดิมในเนื้อใบถูกแทนที่แล้ว ไม่ถูกลบ**: บล็อก "ผลกระทบต่อ `GT-288` ถ้าใบนี้ยังไม่ตอบตอนบูต" ใน `RE-290` สั่งให้เตือนผู้เทสว่า *"AT5 ไม่มีป้ายชื่อ เป็นผลที่เป็นไปได้ ห้ามบันทึกเป็น FAIL ของสี"* · RE runner เขียนเองใน `BUILD_IMPACT` ข้อ 2 ว่าข้อความนั้น **ไม่จำเป็นอีกแล้ว** เพราะโครงสร้างตอบแล้วว่า *มี* ป้าย ⇒ **ห้ามใช้ประโยคนั้นเป็นทางออกของผู้เทสอีก** · ถ้าสีไม่ขึ้นบนจอ = FAIL ของ**สี** ไม่ใช่ "ไม่มีป้าย" · K ไม่ลบบรรทัดเดิมออกจาก `RE-290` ตามกติกา "ห้ามลบอะไรทั้งสิ้น"
> ↳ 🔴 **ที่ยังไม่เปลี่ยน**: ใบยังไม่ขึ้นรถบัส · ชุด 2 ยัง**ไม่มี** `HEADLESS_PROOF:` ของตัวเอง (ชุด 1 มีแล้ว) · nonclaims ของเจ้าของใบคำต่อคำ: ผลนี้ไม่ได้พิสูจน์ว่า AT5 **ระบายสีชื่อ** ได้ · ไม่ได้พิสูจน์ว่า AT5 **เรนเดอร์บนจอ** — นั่นคือสิ่งที่ชุด 2 บนเครื่องเจ้าของต้องตอบ
> 🟢 [LANE-K รอบ `ek1gk9` 2026-09-07T09:4x+07:00] **`HEADLESS_PROOF:` ของชุด 1 มาแล้วและ K ยืนยัน sha เอง** — `git merge-base --is-ancestor 6b5b6b8 origin/main` = ผ่าน · โทเคนคำต่อคำอยู่ใน `tickets/GT-288.md` จากจดหมายเจ้าของใบ `notes_to_chief/20260907_0741_LANE-B-TO-K-gt288-set1-ready-headless-proof.md` · เจ้าของใบขอพลิก **ชุด 1 เท่านั้น** เป็น READY (ชุด 2/3 ยังห้ามบูต) · 🔴 **แต่ใบยังอยู่หมวด ง. ตกรถ**: เงื่อนไขข้อ (1) ของ K ยังไม่ครบ — ไม่มีใบยืนยันจาก chief ว่าเฟรมเดียวลง main แล้ว หลังใบถอน `0345` และเจ้าของใบเองติดป้าย `[สมมติของสาย LANE-B - รอ COO ยืนยัน]` ว่าการวัดของตนแทนใบ chief ได้ไหม ⇒ **เสมียนไม่ตัดสินคำสองปาก** ถาม COO ในจดหมายรอบ `ek1gk9` พร้อมพลิกทันทีที่ได้คำตอบ

owner: LANE-B
ATTENDED:
1. บูตเซิร์ฟเวอร์ด้วย env `PF_NAME_COLOUR_SWEEP=1` (ชุด faction) หรือ `=2` (ชุด actor_type+skin); เข้าเกม ฉาก 1 (Port Royal) ใกล้จุดเกิด
2. เดินไปหน้าแถวหุ่น (เรียงตาม +X จากจุดเกิด ห่างกัน 150 หน่วย); ถ่ายภาพหน้าจอ 1 รูปครอบทั้งแถว
3. อ่านฉลากบนหัวแต่ละตัว (N-BASE/N-F07/.../M-BASE/M-AT3/...) จดสีที่เห็นคู่กับฉลาก
4. ผ่าน/ไม่ผ่าน: ตามตารางสี `2150` (เขียว=ผู้เล่นฝ่ายเดียวกัน · ชมพู=ผู้เล่นฝ่ายตรงข้าม · เหลือง=NPC · ส้ม=มอนไม่ aggro · แดง=มอน aggro · เทา=มอนตาย · ขาว=ชื่อตัวเอง) + เกณฑ์: NPC เหลือง**และ**มอนส้ม = PASS · ข้างเดียว = PARTIAL · ทั้งแถวยังเขียว/ชมพู = ผลลบที่มีค่า
5. ทำซ้ำกับอีก env value (รวม ≤2 ชุดรอบนี้ + สำรอง `=3` รอบยืนยันถ้าจำเป็น) -- ~15 นาที/ชุด
(บล็อกนี้เจ้าของใบ LANE-B เขียนเองคำต่อคำ -- K ไม่ย่อ)
body: `tickets/GT-288.md`

### result:
(ว่าง)

> 🔴 **ห้ามสายอื่นใช้เลข `GT-288`** · numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` + `tickets/` คืนสูงสุด **287** (`GT-287`, ตั้งเลขรอบ `hf1gs9` 2026-09-06T23:17+07:00) ⇒ ใบนี้ **288** · ตรวจ 0 hit ของ `GT-288`/`RE-288` ครบสี่ที่ (live สองคิว · `archive/*QUEUE*ARCHIVE*` · `tickets/`) + ไม่มี RESERVED ใน `NOW.md` ก่อนวาง [ตรวจโดย LANE-K รอบ `6rj6h1`]

**ผู้เปิดใบ: LANE-B (ผ่าน `notes_to_chief/20260907_0021_LANE-B-TO-K-gt-body-RE-155-dummy-row-npc-and-916-sweep.md`) -- ตั้งเลข/วาง: LANE-K รอบ `6rj6h1` -- ผู้บริโภคผล: LANE-B/COO/Panya**

---

## GT-291 CHARACTER-HP-BAR-RETURNS-AFTER-LEAVING-126-001  [🟡 **OPEN · ยังไม่ขึ้นรถบัส — เหลือช่องว่างเดียว** (โทเคนใหม่บน main `e42ea63` วางแล้วรอบ `73i74a` และ K วัด `merge-base` เอง = ผ่าน · สองเหตุผลเดิมปิดครบ · เหลือคำเดียวของ `PANYA-ORDER 20260907_0159` คือ **"ในฉากเป้าหมาย"** ซึ่งโทเคนชุดนี้ยังไม่แสดง -- ดูบล็อก "K วัดอะไรเอง" ท้ายใบ) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-DB** · **ผู้ร่วมเขต (ทางออกจากฉาก) = LANE-A** · ตั้งเลขโดย LANE-K รอบ `rlapyk` 2026-09-07T06:11+07:00 (ภายในรอบที่เห็นคำขอ) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_0532_LANE-DB-TO-K-gt-body-hp-bar-after-leaving-126.md` คำต่อคำ · เปิดตามบรรทัด `NOW.md` (COO รอบ `0445`) "ใบสร้าง A/DB: ออก 126 คืน HP · BoatHealth != -1" และคำขอใน `notes_to_chief/20260907_0123_KA1A-R322B-RESULTS-*.md` ให้แยกออกจาก `GT-281`]

"ออกจาก 126 แล้วหลอด HP ตัวละครต้องกลับมา"

ใบนี้คือ **ใบสร้าง A/DB** ที่ `NOW.md` (COO รอบ `0445`) สั่งไว้หนึ่งบรรทัด และที่ `notes_to_chief/20260907_0123_KA1A-R322B-RESULTS-*.md` ขอให้แยกออกจาก `GT-281` — คำขอเดิมคำต่อคำ: *"ออกจาก 126 ต้องส่ง HP/หลอดตัวละครกลับ และ BoatHealth ห้ามเป็น -1"*

**เจ้าของใบ / ผู้เขียนเนื้อใบ / ผู้บริโภคผล = LANE-DB** · **ผู้ร่วมเขต (ทางออกจากฉาก) = LANE-A**

### สิ่งที่วัด (หนึ่งอย่าง)
หลังผู้เล่นออกจากฉาก 126 มาขึ้นบก แล้วคลิกตัวเอง **แผงตัวเองแสดง HP ของตัวละคร (ไม่ใช่ -1)** และหลอดใต้ชื่อไม่ใช่หลอดฟ้าค้าง

### ทำไมถึงเป็นไปได้ที่จะเห็น -1 (หลักฐานในรีโป ไม่ใช่การเดา)
- `src/pirateforce_foundation/gm/attr_wire.py` แถว `x=9` = `category_5C` (BasicAttr +0x5C, u16) โน้ตของแถวเอง: `0x430E10(this)==8 swaps HP to x52/53`
- แถว `x=52`/`x=53` = `alt_hp_current`/`alt_hp_max` (ActorAttr +0x1A8/+0x1AC, u32) "used when 0x430E10(x9)==8"
- `SELECTOR_NOTE_R301` (ไฟล์เดียวกัน) ระบุรูปเป๊ะ: **ไม่ใช่เอา x=9 ไปเทียบ 8** แต่เอา x=9 ป้อน `0x430E10` แล้วเทียบ **ผลลัพธ์** กับ 8 · สองเส้นทางอิสระ (nameboard `0x5BD3C0..0x5BD3DB` และ HUD `0x53F180` ผ่านไบต์แคช `[actor+0x358]` ที่ผู้เขียนเดียวคือ `al = (0x430E10(sceneId) == 8)`)
- `persistence_attr_compose.CLIENT_CONSTRUCTION_DEFAULTS`: `x=52 = 0xFFFFFFFF`, `x=53 = 1` ⇒ **ถ้าเซิร์ฟไม่เคยตั้งคู่สำรอง ไคลเอนต์แสดง -1/1 เอง** ตรงกับที่เจ้าของเห็น
- วัดสดรอบนี้: ไม่มีคอลัมน์ใดของ `characters` แมปเข้า `x=52`/`x=53` (`SERVER_OWNED_FIELDS` มี 22 แถว ไม่มีสองตัวนี้) ⇒ เซิร์ฟไม่มีอะไรจะส่งให้คู่สำรองแม้อยากส่ง

### 🔴 ที่ใบนี้ **ไม่** อ้าง (สำคัญ อย่าเติมให้)
- **ไม่อ้างว่าฉาก 126 คือ category 8** · `SELECTOR_NOTE_R301` เขียนไว้ตรง ๆ ว่า "WHAT CATEGORY 8 IS: not decoded" และร่างเก่าของโน้ตนั้นเองเคยต้องขีดฆ่าประโยคที่บอกผู้เทสว่าให้ไปฉากไหน — ใบนี้จึงไม่บอกว่าฉากไหนได้คู่สำรอง
- **ไม่อ้างว่า x=9 คือ scene id** · สวีปไบต์ของรีโปนี้เองถอนชื่อนั้นแล้ว
- ไม่วัดสีชื่อ ไม่วัดดาเมจ ไม่วัดดรอป ไม่วัดตาย ไม่วัดเลเวล
- ไม่อ้างว่าเซิร์ฟวันนี้ส่งคู่สำรอง `x=52`/`x=53` ให้ไคลเอนต์ — **`x=52`/`x=53` ไม่อยู่ใน login shape ใดเลย ส่วน `x=9` อยู่ในทุก shape** (ดู `HEADLESS_PROOF:` ด้านล่างซึ่งบอกตรง ๆ ว่าพิสูจน์อะไรและไม่พิสูจน์อะไร)
  > 🔁 **บรรทัดนี้แทนบรรทัดเดิมทั้งบรรทัด** ตามคำขอเจ้าของใบข้อ 5 ใน `notes_to_chief/20260907_1013_LANE-DB-TO-K-gt291-second-request-false-sentence-still-in-the-ticket.md` (ทวงครั้งที่หนึ่ง) · วางโดย LANE-K รอบ `wb8tfv` 2026-09-07T11:10+07:00 · **ถ้อยคำใหม่เป็นของเจ้าของใบคำต่อคำ K ไม่ได้ตัดสินอะไร**
  > บรรทัดเดิม เก็บไว้ไม่ลบ: *"ไม่อ้างว่าเซิร์ฟวันนี้ส่ง `x=9`/`x=52`/`x=53` ให้ไคลเอนต์ — **ไม่มีเส้นทางส่ง**"*
  > ทำไมเดิมถึงเท็จ (เหตุผลของเจ้าของใบ วัดสดบน `pirate-force-server` main `c570522`): `admitted_field_x_sets(legacy)` → `((1,2,3,4,7,9,10,13,24),(1,2,3,4,7,9,10,11,13,24))` · `x=9 in EVERY admitted shape = True` · `x=52/53 in ANY admitted shape = False` · `attr_wire.CURRENT_SCENE_SOURCED_ROWS = frozenset({9})` ⇒ ประโยคเดิมเหมาสามแถวเป็นก้อนเดียว จึงเท็จหนึ่งในสาม และเป็นหนึ่งในสามที่เปลี่ยนคำตอบของใบ
  > 🔴 บล็อก `HEADLESS_PROOF:` ถูกแก้ไปแล้วในรอบ `73i74a` (จดหมาย `0842` ข้อ 4.1) — รอบนี้ปิดครึ่งที่เหลือ คือบรรทัด nonclaims บรรทัดนี้ ตามที่รอบก่อนเขียนไว้เองว่า "ส่งคืนเจ้าของ" และเจ้าของส่งกลับมาแล้ว

ATTENDED:
1. บูตปกติ ไม่มีธง เข้าเกม ออกทะเลไปฉาก 126 (เส้นทางเดียวกับ `GT-281`/R322B) แล้ว **คลิกตัวเอง** อ่านตัวเลข HP บนแผง จดค่าที่เห็นคำต่อคำ
2. กลับขึ้นบก (ออกจาก 126) แล้ว **คลิกตัวเองซ้ำ** อ่าน HP บนแผงอีกครั้ง + ดูหลอดใต้ชื่อว่ายังเป็นหลอดฟ้าไหม
3. ผ่าน = ขั้น 2 แสดง HP ของตัวละครเป็นบวก (เช่น 100/100) และไม่มี -1 · ไม่ผ่าน = ขั้น 2 ยังเป็น -1 หรือหลอดฟ้ายังค้าง
4. ฝั่งสาย: คัดลอกบรรทัดคอนโซลของเซิร์ฟช่วงออกจาก 126 ทั้งบล็อก (ยังไม่มีโทเคนเฉพาะของกลไกนี้ — ต้องการ raw เพื่อดูว่ามีเฟรม attr ออกตอนเปลี่ยนฉากหรือไม่)
5. บูตด้วยทรี `origin/main` ปัจจุบัน ไม่ต้องตั้งธง ไม่ต้องใช้ GM

HEADLESS_PROOF:
```
HEADLESS_PROOF: HP_PAIR_SELECTOR_REPORT character_id=1 | primary x=3/4 shows 100/100 | alternate x=52/53 shows -1/1 (constructor layer: client construction default, what it holds when no frame ever wrote them) | alternate x=52/53 shows 0/0 (frame layer: a frame that arms the selector with these rows absent, RE-222 Q0) | alternate_pair_supplied_by_this_server=False | selector x=9 armed value 8; 0x430E10 is not evaluated here
cmd: python3 -c "..." -> pirateforce_foundation.persistence_hp_pair_selector.live_hp_pair_report(store, character.id) + format_report  (สร้าง SQLiteStore ชั่วคราว migrate แล้ว create_character หนึ่งตัว · read-only ต่อ DB จริง · ไม่แตะ canonical DB)
commit: pirate-force-server origin/main e42ea63  (2026-09-07)  [byte-identical output also produced on 3cfe79b and f791fc5 earlier the same round; the token's inputs did not move between them -- `git diff --stat 3cfe79b e42ea63 -- persistence_hp_pair_selector.py gm/attr_wire.py persistence_attr_compose.py store.py migrations/` is empty]
```
> 🔁 **บรรทัดนี้แทนที่บรรทัดเดิมทั้งบรรทัด** ตามคำขอของเจ้าของใบ (`notes_to_chief/20260907_0842_LANE-DB-TO-K-gt291-headless-proof-on-main-and-a-correction-to-my-own-ticket.md` ข้อ 4.1) ซึ่งขอให้ **ลบ** ประโยค *"วันนี้ไม่มีเส้นทางส่ง `x=9`/`x=52`/`x=53` เลยทั้งรีโป"* ทิ้ง ไม่ใช่แก้คำ — เจ้าของใบวัดเองแล้วว่า **ครึ่งแรกของประโยคนั้นเป็นเท็จ** (`x=9` อยู่ในทุกรูป login ที่ผ่านกำแพง · `attr_wire.CURRENT_SCENE_SOURCED_ROWS -> [9]`) · วางโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00 **คำต่อคำ ไม่แก้สำนวน**

### 🔴 K วัดอะไรเอง (ไม่เชื่อจดหมาย · `NOW.md` `0159` "ka1-A รันซ้ำก่อนบูต ไม่ตรง = ตัดใบ")
**รอบ `73i74a` 2026-09-07T10:09+07:00 — วัดสดบนโคลนที่ `git fetch origin main` แล้ว (`pirate-force-server` head `b302d55`):**
- `git merge-base --is-ancestor e42ea63 origin/main` = **ผ่าน** ⇒ คอมมิตที่ผลิตโทเคนใหม่ **อยู่บน main จริง**
- `git cat-file -e origin/main:src/pirateforce_foundation/persistence_hp_pair_selector.py` = **มี** ⇒ ไฟล์ที่ผลิตโทเคนอยู่บน main
- `git merge-base --is-ancestor c19132f origin/main` = **ผ่านแล้วในรอบนี้** (รอบ `rlapyk` ยังไม่ reachable · ขึ้น main ระหว่างนั้น)
- คอมมิต `e42ea63` ลงวันที่ 2026-09-07 ⇒ **อยู่ในระยะ ≤3 วัน** ตาม `0159`

**สองเหตุผลเดิมที่ทำให้ใบนี้ไม่ขึ้นสแนปช็อต — ปิดไปแล้วทั้งคู่:**
1. ~~โทเคนไม่ได้มาจากคอมมิต main ปัจจุบัน~~ ⇒ **ปิด** (K วัดเอง ข้างบน)
2. ~~เจ้าของใบเขียนเองว่าโทเคนไม่ได้พิสูจน์ว่ากลไกติดอาวุธในฉากเป้าหมาย~~ ⇒ **เจ้าของใบถอนประโยคนั้นเอง** (จดหมาย `0842` ข้อ 2-3): `x=9` คือแถวที่เซิร์ฟส่งอยู่แล้ว **ทุก login** และเป็นแถวที่ถือ scene ของ session ⇒ กลไกติดอาวุธ **มีจริง** · สิ่งที่รีโปถอดไม่ได้คือ `0x430E10` แปลง `x=9` เป็น 8 หรือไม่ ซึ่งเป็นคำถามของจอ

🟡 **ช่องว่างเดียวที่เหลือ ซึ่ง K ไม่มีสิทธิ์ปิดเอง — และเป็นเหตุผลเดียวที่ใบนี้ยังอยู่หมวด ง. รอบนี้**
`0159` เขียนว่าโทเคนต้องแสดงว่ากลไกติดอาวุธ **"ในฉากเป้าหมาย"** · โทเคนชุดนี้ผลิตจาก **`create_character` หนึ่งตัวใน SQLiteStore ชั่วคราว** ไม่ใช่จาก session ที่อยู่ในฉาก **126** ⇒ อ่านตามตัวอักษร ยัง**ไม่ครบ**คำว่า "ในฉากเป้าหมาย" แม้จะครบทุกข้ออื่น
🔴 K **ไม่ยกเว้นให้เอง** (`COO-DECISION 20260907_0641` ข้อ 1: "เสมียนไม่มีสิทธิ์ยกเว้นคำสั่งเจ้าของ ถูกแล้ว และ COO ก็ไม่มี" · `0159` เป็นคำสั่งที่ Panya เคาะเอง) · **ปลดได้สองทาง ทางไหนก็ได้ ไม่ต้องรอกัน**: (ก) LANE-DB เติมโทเคนบรรทัดเดียวที่รันโดย session อยู่ในฉาก `126` แล้วพิมพ์ค่าที่แถว `x=9` ถืออยู่ตอนนั้น ⇒ K พลิกขึ้นหมวด ก. ในรอบที่เห็น (ข) COO/Panya เคาะว่าโทเคน login-wide ของ `x=9` นับว่า "ในฉากเป้าหมาย" แล้ว ⇒ K พลิกในรอบที่เห็นเช่นกัน

> ✅ **[LANE-K รอบ `wb8tfv` 2026-09-07T11:10+07:00] ปิดแล้ว** — เจ้าของใบส่งใบทวงครั้งที่หนึ่ง (`notes_to_chief/20260907_1013_LANE-DB-TO-K-gt291-second-request-false-sentence-still-in-the-ticket.md` ข้อ 5) พร้อมถ้อยคำแทน ⇒ K วางให้แล้วในบล็อก nonclaims ข้างบน คำต่อคำ · บล็อกเดิมข้างล่างนี้เก็บไว้ไม่ลบ เพื่อให้เห็นว่าค้างอยู่ 3 รอบ (`rlapyk` → `73i74a` → `wb8tfv`)
> ✅ **โทเคนใหม่บน main ปัจจุบัน (เจ้าของใบวัดเอง · K ยืนยัน `merge-base` เอง)**: เจ้าของใบรันซ้ำทั้งดุ้นบน `pirate-force-server` `c570522` ได้ผลคำต่อคำเดียวกับชุด `e42ea63` ที่อยู่ในบล็อก `HEADLESS_PROOF:` ⇒ โทเคนไม่เปลี่ยนความหมาย · **K วัดเองรอบนี้** (server head `e4ae180`): `git merge-base --is-ancestor c570522 origin/main` = **ผ่าน** · คอมมิตลงวันที่ 2026-09-07 ⇒ อยู่ในระยะ ≤3 วันตาม `0159`
> 🔴 **ช่องว่าง "ในฉากเป้าหมาย" ยังไม่ปิด และไม่ได้ปิดด้วยใบนี้** — เจ้าของใบเขียนเองในข้อ 4 ว่า **ไม่ขอข้อยกเว้น ไม่ถอนคำของตัวเอง และไม่เติมโทเคนปลอมให้ผ่านเกณฑ์** ⇒ ใบยังอยู่หมวด ง. ตาม `COO-DECISION 20260907_0641` ข้อ 1-2 (รอ Panya ติ๊กข้อยกเว้น `NO_MECHANISM_TO_ARM:` ใน `NOW.md`) · เจ้าของใบเขียนว่า **จะไม่ทวงซ้ำอีกหลังใบนี้**

**ที่ยังไม่ปิดในเนื้อใบ (K ไม่แตะเนื้อใบ ส่งคืนเจ้าของ)**: บรรทัด nonclaims ข้างบนยังเขียนว่า *"ไม่อ้างว่าเซิร์ฟวันนี้ส่ง `x=9`/`x=52`/`x=53` ให้ไคลเอนต์ — **ไม่มีเส้นทางส่ง**"* ซึ่งเป็น **ประโยคเดียวกันที่เจ้าของใบเพิ่งถอน** · K ลบไม่ได้ (เนื้อใบ = ของเจ้าของใบ) ⇒ แจ้ง LANE-DB ในจดหมายรอบนี้แล้ว
🔴 **K ไม่ได้ตัดสินว่าใบนี้ผิดหรือใช้ไม่ได้** — K คัดลอกสิ่งที่เจ้าของใบเขียนไว้เอง แล้วยกคำถาม "ใบสังเกตฝั่งไคลเอนต์ล้วนต้องมี `HEADLESS_PROOF:` แบบติดอาวุธไหม" ให้ COO ตัดสิน ตามที่เจ้าของใบขอมาในจดหมายเอง · จดหมาย: `notes_to_chief/20260907_0611_LANE-K-ASK-COO-headless-proof-for-observation-only-tickets.md`

### result:
(ว่าง)

> numbering: ตัวนับร่วมสองคิว + `archive/*ARCHIVE*` + `tickets/` คืนสูงสุด **290** (`RE-290`, ตั้งเลขรอบเดียวกัน `rlapyk`) ⇒ ใบนี้ **291** · ตรวจ 0 hit ของ `GT-291`/`RE-291` ทั้งสี่ที่ (live สองคิว + `archive/*ARCHIVE*` + `tickets/` + `notes_to_chief/FROM_CHIEF_*`/`*COO-DECISION*`) ก่อนวาง [ตรวจโดย LANE-K รอบ `rlapyk`]

## GT-299 LEARN-SKILL-REQUEST-TRIGGER-HUNT-001  [🟠 **READY (attended)** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-CS** · ผู้ทำ: **ka1-A (attended)** · ตั้งเลขโดย LANE-K รอบ `du6wre` 2026-09-07T13:32+07:00 (คำขอเข้ามา 2026-09-07T12:27 — ตั้งเลขในรอบแรกที่ K เห็นคำขอ) · สั่งโดย `COO-DECISION 20260907_1141` ข้อ 2 · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_1227_LANE-CS-TO-K-gt-body-learn-skill-request-0x36aa-trigger-hunt.md` **คำต่อคำ K ไม่แก้สำนวนแม้คำเดียว**]

> numbering [LANE-K รอบ `du6wre`]: ตัวนับร่วมสองคิว + `archive/*.md` + `tickets/` + เลขที่จองใน `FROM_CHIEF_*`/`*COO-DECISION*` คืนสูงสุด **298** (`RE-298` วางในรอบเดียวกันนี้) ⇒ ใบนี้จอง **299** · `grep -rl 'GT-299\|RE-299'` ทั้งรีโป (นอก `.git/`) = **0 hit** ก่อนวาง
> ✅ **ครบเงื่อนไขขึ้นรถบัส capture ตามกฎ `PANYA 0159`**: มีบล็อก `ATTENDED:` (5 บรรทัด) และมีบรรทัด `HEADLESS_PROOF:` ที่เจ้าของใบวัดในรอบเดียวกัน — 🔴 **แต่เจ้าของใบเขียนข้อจำกัดไว้เองว่าไฟล์พิสูจน์ `skill_learn_request_headless.py` ยังอยู่ใน PR ฝั่ง `pirate-force-server` ที่เพิ่งเปิด ไม่ใช่บน `origin/main`** ⇒ K **ไม่ตัดสิน**ว่านับหรือไม่นับตามกฎ `0159` (ka1-A รันไม่ตรง = ตัดใบ) · ถามไว้ในจดหมายรอบถึง COO แล้ว · คำของเจ้าของใบอยู่ครบข้างล่าง ไม่ถูกตัด
> 🔴 K **ไม่ได้รับรอง**โทเคน/ตัวเลข/ข้อสรุปใดในเนื้อใบ — ทุกบรรทัดข้างล่างเป็นคำของเจ้าของใบ (LANE-CS)

# หัวใบ
**LEARN-SKILL-REQUEST-TRIGGER-HUNT-001** — ผู้เล่นกดอะไรบนจอ แล้วไคลเอนต์จริงถึงยิงเฟรม `0x36AA`
และเซิร์ฟเวอร์ที่ติดอาวุธแล้วอ่านมันออกไหม

## คำถามเดียวของใบ (ทั้งใบตอบข้อนี้ข้อเดียว)
`learn_skill_request_hypothesis.py` เป็น **decoder อย่างเดียว** ต่อสายบนสาย `0x36AA` แล้ว แต่ nonclaim
ของโมดูลเองเขียนว่า **ยังไม่มีใครรู้ว่า UI ท่าไหนทำให้ไคลเอนต์ยิงเฟรมนี้** — ka1-A ลองเปิด/ปิดหน้าต่างสกิล
สลับแท็บ คลิกรายการ ลากลงฮอตบาร์ ทีละท่าแบบแยกกัน **ไม่มีท่าไหนส่งอะไรเลย** เฟรมจริงใบเดียวที่มีอยู่
(R312 `#70`, GT-249) มาตอนที่เธอ *จำไม่ได้* ว่ากำลังทำอะไรกับแท็บ "พิเศษ"
⇒ ใบนี้ไม่ได้ถามว่า "สกิลขึ้นจอไหม" ใบนี้ถามว่า **ท่าไหนทำให้เฟรมออก**

## HEADLESS_PROOF (กฎ `0159` · วัดรอบนี้ ไม่ได้คัดลอกของเก่า)
```
HEADLESS_PROOF: 2026-09-07 main 11f937a | cmd: python3 src/pirateforce_foundation/skill_learn_request_headless.py | LEARN_SKILL_REQUEST_ARMED_SUMMARY probes=3 decoded_no_reply=yes real_frame=refused no_db_write=yes RESULT=PASS
```
🔴 **ข้อจำกัดที่ต้องอ่านก่อนใช้บรรทัดนี้ — ผมไม่ปิดบัง**: *กลไก* (สาขา `0x36AA` ใน `runtime.py`
+ decoder + ไฟล์ scenario) **อยู่บน `origin/main` `11f937a` แล้ววันนี้** แต่ *ตัวไฟล์พิสูจน์*
`skill_learn_request_headless.py` เพิ่งเกิดรอบนี้ อยู่ใน PR ฝั่ง `pirate-force-server` ที่เพิ่งเปิด
ผมวัดโดย **สร้าง worktree สะอาดจาก `origin/main` `11f937a` แล้ววางไฟล์พิสูจน์ไฟล์เดียวลงไป**
(`git status --porcelain` = `?? src/pirateforce_foundation/skill_learn_request_headless.py` บรรทัดเดียว
ไม่มีอย่างอื่นเลย) แล้วรัน ได้โทเคนสี่บรรทัด + `RESULT=PASS` exit 0
⇒ โทเคนนี้เป็นคำพูดถึง **กลไกบน main** ไม่ใช่กลไกบนกิ่งผม · เมื่อ PR เข้า main ผมจะส่งจดหมายสั้น
ยืนยันบรรทัดเดิมด้วยคอมมิต main ใหม่ (ท่าเดียวกับ `GT-276` `0618` → `0746`) — ถ้า K อยากถือใบไว้จนถึง
ตอนนั้นก่อนขึ้นรถ ผมไม่เถียง
โทเคนสี่บรรทัดที่ออกจริง:
```
LEARN_SKILL_REQUEST_ARMED case=probe_ZERO actions=0 event=learn_skill_request_hypothesis_decoded_no_reply u32=0 u8=0 db_unchanged=yes
LEARN_SKILL_REQUEST_ARMED case=probe_MID actions=0 event=learn_skill_request_hypothesis_decoded_no_reply u32=1000001 u8=11 db_unchanged=yes
LEARN_SKILL_REQUEST_ARMED case=probe_MAX actions=0 event=learn_skill_request_hypothesis_decoded_no_reply u32=4294967295 u8=255 db_unchanged=yes
LEARN_SKILL_REQUEST_ARMED case=real_r312_frame70 actions=0 event=learn_skill_request_hypothesis_wrong_envelope_no_reply vitals=2 second_vital=0x0F01 db_unchanged=yes
```

## บล็อก `ATTENDED:` (ห้าบรรทัด · วางลงคิวได้ตรง ๆ)
ATTENDED: บูตตาม `ATTENDED_SESSION_RUNBOOK.md` บน DB **สำเนา run-copy** เท่านั้น (ห้ามเปิด canonical · เทียบ sha ก่อน/หลัง) เซิร์ฟก่อนไคลเอนต์ทีหลัง เก็บคอนโซล `2>&1` -> ล็อกอินปกติเข้าเมือง (ฉาก 1) ไม่ต้อง GM ไม่ต้อง warp -> เปิดหน้าต่างสกิลด้วยฮอตคีย์ `K` (คลิกช่องแชทแล้วกด Esc ยืนยันว่าแชท**ไม่**โฟกัสก่อน ไม่งั้นตัวอักษรกลายเป็นฮอตคีย์)
ATTENDED: ทำทีละท่า **หยุด 3 วินาทีระหว่างท่า** และจดชื่อท่ากับเวลานาฬิกาก่อนทำทุกครั้ง (ไม่มีบรรทัดเวลา = อ่านคอนโซลย้อนไม่ออก = ใบเสีย): (1) เปิด/ปิดหน้าต่างสกิล 3 ครั้ง (2) สลับทุกแท็บทีละแท็บ ไล่ซ้ายไปขวา (3) คลิกซ้ายรายการสกิลทีละรายการในแท็บ "พิเศษ" (4) **ดับเบิลคลิก**รายการในแท็บ "พิเศษ" (5) คลิกขวารายการในแท็บ "พิเศษ" (6) ลากรายการลงฮอตบาร์ แล้วลากออก (7) ถ้ามีปุ่ม/เครื่องหมาย `+` หรือปุ่มเรียนสกิลใด ๆ กดมัน (8) กดสกิลจากฮอตบาร์ 1 ครั้ง · ท่า (4)(5)(7) คือสามท่าที่ ka1-A **ไม่ได้**ลองในรอบ R312
ATTENDED: ค่าที่ต้องอ่าน/จด (ชั้น wire): บรรทัด stderr `DISPATCH_NESTED_VITALS vital_count=<N> first_nested_id=0x36AA` = **ตัวจับ** ว่าเฟรมออกจริง — จด `<N>` เป๊ะทุกครั้ง (R312 เคยได้ `2`) และจดว่ามาหลังท่าหมายเลขไหน กี่วินาทีหลังจากท่านั้น · ถัดมาอีกบรรทัดต้องมี `learn_skill_request_hypothesis_..._no_reply` — จด**ชื่อเต็ม**: `_decoded_no_reply` (envelope ที่เลนนี้รับ) หรือ `_wrong_envelope_no_reply` (เฟรมมีหลายไวทัลเหมือน R312) · ชั้นจอแยกต่างหาก: ท่านั้นทำให้หน้าจอเปลี่ยนอะไรไหม (ไอคอน/ตัวเลข/ข้อความ) ประโยคเดียวต่อท่า **ห้ามใช้คอนโซลตอบแทนตา และห้ามใช้ตาตอบแทนคอนโซล**
ATTENDED: ตัดสิน: มีบรรทัด `first_nested_id=0x36AA` อย่างน้อยหนึ่งครั้ง **และ**รู้ว่ามาหลังท่าไหน = **PASS** (นี่คือคำตอบทั้งใบ) · ออกแต่ไม่รู้ว่าท่าไหนเพราะไม่ได้จดเวลา = **PARTIAL** · ทำครบแปดท่าแล้ว **ไม่มีบรรทัดนี้เลยทั้งเซสชัน = ผลลบที่มีค่า บันทึกเป็นผล ไม่ใช่ FAIL** (แปลว่าแปดท่านี้ไม่ใช่ตัวสั่ง ซึ่งเป็นข้อมูลที่ยังไม่มีใครมี) · เห็น `_wrong_envelope_no_reply` = **ไม่ใช่ FAIL** เป็นค่าที่ใบต้องการ (ยืนยันว่าไคลเอนต์จริงห่อหลายไวทัลเสมอ) · traceback ก่อนมีไบต์ออกสาย = NO-RESULT ส่งคืน · ห้ามเปลี่ยนแฟล็ก/ท่าเองเพื่อให้ "ผ่าน" ห้ามชี้สาเหตุ
ATTENDED: บูตด้วยแฟล็กเดียว `--learn-skill-request-hypothesis-scenario scenarios/learn_skill_request_hypothesis_decode_probe.json` **คู่กับ `--db <สำเนา>` เสมอ** (แฟล็กนี้ปฏิเสธการบูตถ้าไม่ระบุ DB) · ห้ามพ่วงแฟล็ก `--*-scenario` ตัวอื่นแม้แต่ตัวเดียว โดยเฉพาะ **ห้ามพ่วง `GT-276`/`learn-skill-result`** (ชุดนั้นทำให้ไคลเอนต์เดินไม่ได้ = ท่าที่ 1-8 ทำไม่ครบ) · ทรีต้องมี `src/pirateforce_foundation/learn_skill_request_hypothesis.py` และรันโทเคน `HEADLESS_PROOF` ให้ตรงก่อนบูต ไม่ตรง = ตัดใบตามกฎ `0159` · teardown ตาม runbook เสมอ

## ทำไมใบนี้ไม่ซ้อน `GT-276` และไม่ควรรวมกัน
`GT-276` ถามว่า *เฟรมขาออกใบไหน* ล็อกการเดิน · ใบนี้ถามว่า *ท่าไหน* ทำให้เฟรม**ขาเข้า**ออกจากไคลเอนต์
คนละทิศ คนละแฟล็ก และ **ห้ามบูตพร้อมกัน** ด้วยเหตุผลในบรรทัด `ATTENDED:` สุดท้าย
แต่บูตเดียวกันของ **รถบัสเดียวกัน** ทำได้ ถ้าแยกโปรเซสเซิร์ฟเวอร์คนละรอบ — K จัดลำดับตามที่ `1141` เขียนไว้
(หลัง `GT-288` และ `GT-276`)

## grep แล้ว (กฎ "ใบ RE ที่ถามสิ่งที่มี layout อยู่แล้ว = เสียรอบ")
- `external/PF_SERIALIZER_FIELDS.tsv` → **เจอ** สี่แถวของ `0x36AA` (W/R สมมาตร) ⇒ ใบนี้ **ไม่ได้**ถาม layout
  ถามเฉพาะสิ่งที่ static ตอบไม่ได้เลย คือ *มนุษย์กดอะไร*
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` → **เจอ** `CLearnSkillVital` เป็นการกระทำจริงบนสาย
- `GAME_TEST_QUEUE.md` / `CLIENT_RE_QUEUE.md` grep `0x36AA` และ `learn_skill_request` → **ไม่เจอใบใด**
  ⇒ ใบนี้ไม่ซ้ำใบเก่า และเป็นใบแรกที่ถามคำถามนี้

## nonclaims ของใบนี้
- ไม่อ้างว่าไคลเอนต์ **จะ** ยิง `0x36AA` จากท่าใดท่าหนึ่งในแปดท่า — ถ้าไม่ยิงเลย นั่นคือผลของใบ
- ไม่อ้างว่ารู้ความหมายของสองค่าที่ decode ได้ (`u32@0x14` / `u8@0x18`) เฟรมจริงใบเดียวให้ `(0, 2)`
  และไม่มีใครรู้ว่า 0 กับ 2 คืออะไร ใบนี้ไม่ได้ถามข้อนั้นด้วย
- ไม่อ้างว่าเลนนี้ทำอะไรให้ผู้เล่นเห็น: มันอ่านแล้วเงียบ ไม่ตอบ ไม่เขียน DB (วัดแล้วในโทเคน `db_unchanged=yes`)
- ไม่อ้างว่า envelope ที่เลนนี้รับคือ envelope ที่ไคลเอนต์ใช้ — **ตรงกันข้าม** โทเคนบรรทัดที่สี่พิสูจน์ว่า
  เฟรมจริงถูกปฏิเสธเป็น `wrong_envelope` วันนี้ และใบนี้จะบอกว่ามันเป็นแบบนั้น **ทุกครั้ง** หรือแค่ครั้งเดียว
- ไม่อ้างว่าใบขึ้นรถแล้ว — K ตัดสิน · LANE-CS ส่งเฉพาะของที่เจ้าของใบต้องส่ง

-- LANE-CS (รอบ `s425vn`)
