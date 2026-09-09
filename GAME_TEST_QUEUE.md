# GAME TEST QUEUE — คิวเทสในเกม

> 🔴 **นิยามคำว่า "result" — สองงานคนละงาน ห้ามสับสน** (`COO-DECISION 20260907_1541` ถึง LANE-K ข้อ 1 · วางไว้ที่หัวไฟล์เพราะคำถามนี้ถูกถาม **สามครั้งใน 24 ชม.**)
> - **พับ (fold) = LANE-K**: คัดลอกคำตอบ/`BUILD_IMPACT`/nonclaims จากจดหมายผลลงหัวใบ + พลิกสถานะ + วางสตับ `.LANEK-FOLDED.txt` — **เป็นงานเสมียน ไม่ตัดสิน** · คำที่ใส่ต้องเป็น**คำของผู้เทส/เจ้าของใบ** ไม่ใช่คำของ K · ผลสองชั้นไม่ครบ = `🟡 <ชั้นที่ครบ> · <ชั้นที่ขาด> NOT MEASURED` ห้ามปั๊ม PASS
> - **บริโภค (consume) = สายเจ้าของใบ**: เอาผลไปแก้โค้ด / ออกใบสร้าง / เขียน `NO_FEATURE_WAITING:` แล้ววางสตับ `.CONSUMED.txt` — **K ห้ามทำแทนเด็ดขาด**
> ⇒ ประโยคใน `prompts/COMMON_LANE_ROUND.md` ("ใครเปิดใบ คนนั้นบริโภคผล") กับ `NOW.md` `PANYA 1910` ("พับผล = LANE-K") **ไม่ขัดกัน** — คำเดียวกันใช้กับสองงาน · สายเจ้าของใบ **ไม่ต้องแตะไฟล์คิวนี้เอง** เพื่อพับผลของตัวเอง ส่งจดหมายถึง K แล้วบริโภคต่อได้เลย
>
> 🅿️ **`RESERVED` = เลขที่จองแล้วแต่ยังไม่มีเนื้อใบ** (`COO-DECISION 20260907_1541` ข้อ 2 · "ยืนเป็นแบบแผน")
> - แถว `RESERVED` **ห้ามขึ้น `READY`** และ **ห้ามเข้า `QUEUE_STATUS_SNAPSHOT.md`** — ka1-A ต้องไม่มีทางหยิบใบเปล่าขึ้นรถบัส
> - **K ห้ามเขียนโครงเนื้อใบแทนเจ้าของ** (เจ้าของจะกลายเป็นคนเซ็นของที่ตัวเองไม่ได้เขียน) · เนื้อใบมาทางจดหมาย `*-TO-K-gt-body-*` / `*-TO-K-re-body-*` **คำต่อคำ**
> - กำหนดเวลา: เนื้อใบต้องมาภายใน **สองรอบของสายเจ้าของ** · ไม่มา ⇒ K ขึ้นแถวในสแนปช็อตหมวด **ช.** พร้อมชื่อสายและอายุ — **K ขึ้นบัญชีอย่างเดียว ไม่ทวงเอง** (COO ทวง)
> - 🔵 **ไม่ขัดกับกฎ ① "ห้ามจองเลขล่วงหน้า" ข้างล่าง**: เลขยังเกิด**ตอนแถวลงไฟล์นี้จริง**เท่านั้น · แถว `RESERVED` คือแถวที่ลงไฟล์แล้ว สิ่งที่กฎ ① ห้ามคือการอ้างเลขในจดหมาย**ก่อน**มีแถวในไฟล์

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

## 📇 สารบัญ = `QUEUE_STATUS_SNAPSHOT.md` (generate: `python3 tools_bridge/pf_queue_status.py` · สารบัญมือลบ 2026-09-09 ตาม PANYA 16:00 · ของเดิมอยู่ใน git ก่อน PR นี้)

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

## PLAYBOOK → archive/GAME_TEST_QUEUE_PLAYBOOK_20260909.md (ย้ายคำต่อคำทั้งก้อน 6289 B — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:15+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 3 · ไม่มีอะไรถูกลบ)

## PLAYBOOK เพิ่มเติม → archive/GAME_TEST_QUEUE_PLAYBOOK_20260909.md (ย้ายคำต่อคำทั้งก้อน 51546 B — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:15+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 3 · ไม่มีอะไรถูกลบ)

## รายการที่ปิดแล้ว (GT-002..006 · 011 · 015 · 017 · 018-022 · 023-025) — ⤴ stub ทั้งหมดย้ายไป archive (รอบ 97)

> pointer รวม: `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R97_CLOSED_STUBS.md`
> (ในนั้นชี้ต่อไปยัง archive เนื้อหาเต็มของแต่ละรายการอีกชั้น — ไม่มีอะไรถูกลบ)
> ใจความที่ยังต้องรู้: GT-019 พิสูจน์ hp0+timer ตายบนจอ · GT-021 พิสูจน์ client ไม่ลดตัวนับเอง
> · GT-022/025 พิสูจน์ท่านอน = DYING_LATCH (`_F_DIE_000` ยังไม่เคยถูกสังเกต — ห้าม flip HYP-PF-023)
> · GT-024 พิสูจน์เลขเรนเดอร์บนผู้เล่น + HP ไม่ลด (สองปาก) — ที่มาของ GT-031

- ~~GT-001 Smoke: full-loop บน canonical DB หลังทุก commit สำคัญ~~ -> `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md` (🟢 **PASS รอบ UA1 — ปิดโดย chief R232**: `OBSERVER_CONFIRMED: 2026-08-2 ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

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
## GT-036 KILL-HOSTILE-001 [BLOCKED] · body: `tickets/GT-036.md` (เนื้อใบเต็ม 14067 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
## 🆕 GT-037 LOOT-ROLL-001: server-side loot roller จาก client tables [✅ **DONE — chief รอบ 113 (cloud) build เสร็จ · เขียว(cloud sanity) 992 pa... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕 GT-038 DAMAGE-TARGET-AB-001: A/B — การคลิกเลือกเป้าเกี่ยวอะไรกับเลขที่มองเห็นไหม [✅ **PASS — 2026-08-22 23:24 (+07:00): target selection ไ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🎯 GT-039 NPC-HP-LINK-001: **หลอดเลือดของ "เป้าหมาย" ลดจริงไหม** [✅✅ **PASS — รอบใหญ่ #11 (UNATTENDED) 2026-08-21 02:05–02:25 · HEAD `cc46a0... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕🔬 GT-040 DROPTHING-TRANSPORT-PROBE-001 [STATIC-ON-BRIDGE]: "วัตถุลูทบนพื้น" มี transport อยู่ในอิมเมจจริงไหม — สามจุดที่ยังไม่มีใครเปิดสักค... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🆕⭐ GT-041 MOVE-AUTHORITY-002: เซิร์ฟเวอร์ "ไม่ยอมเขียน" ตำแหน่งที่ client รายงาน — ผู้เล่นเห็นอะไรไหม [✅ **PASS (no-rejection) — 2026-08-23 ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-030 REMOTE-PLAYER-VIS-001: "มีคนอื่นอยู่ในโลก" ครั้งแรก — actor_type 2 ทั้ง 5 เฟรม [🟠 **ผล substantive แล้ว — rerun 2026-08-23 00:25 (+07... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-030-R3 REMOTE-PLAYER-VIS-PROVENANCE-001 [attended, in-game]: รอบสามของ `GT-030` — **ของที่เห็นบนแนว probe เป็นผลของเฟรมที่เลนนี้ส่ง หรืออ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-031 DAMAGE-HP-LINK-001: วงเต็ม "ตี → เลือด → ตาย" ครั้งแรก (ฝั่ง**ผู้เล่นเอง**) [✅ **PASS — รอบใหญ่ #12 (2026-08-21 ~08:0x +07:00)**] -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-032 NPC-HOSTILE-001: NPC ตัวแรกของ Port Royal "ขึ้นศัตรู (แดง)" ไหม — Door A ของ mob-aggro [✅ **PASS — รอบใหญ่ #12 ต่อ (2026-08-21 ~09:00... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## 🛠️ บทเรียนเครื่องมือใหม่จากรอบใหญ่ #12 → archive/GAME_TEST_QUEUE_PLAYBOOK_20260909.md (ย้ายคำต่อคำทั้งก้อน 2642 B — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:15+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 3 · ไม่มีอะไรถูกลบ)

## 🛠️ บทเรียนเครื่องมือใหม่จากรอบใหญ่ #9/#10 → archive/GAME_TEST_QUEUE_PLAYBOOK_20260909.md (ย้ายคำต่อคำทั้งก้อน 2587 B — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:15+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 3 · ไม่มีอะไรถูกลบ)

## 🛠️ บทเรียนเครื่องมือจากรอบใหญ่ #8 → archive/GAME_TEST_QUEUE_PLAYBOOK_20260909.md (ย้ายคำต่อคำทั้งก้อน 3350 B — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:15+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 3 · ไม่มีอะไรถูกลบ)

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
## ⭐ GT-060 PICKUP-CLICK-CAPTURE-001 [CANCELLED] · body: `tickets/GT-060.md` (หัวใบเดิม 3052 B + 5 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## GT-063 ITEMOPERATE-RES-GREENLINE-SHAPE-001 [attended, in-game]: ยิง `ItemOperateVitalRes` (`0x4C13`) สามทรงจากเซิร์ฟเวอร์เรา แล้วตัดสินด้วยต... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-064 SKILL-ATTR-WINDOW-KPRESS-IN-GAP-001 [attended, in-game]: กด **K** / คลิก `Bt_main_Skill` **ภายในช่อง 3.0 วิ ระหว่างเฟรม `COUNT0` (57B... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-069 GROUNDLOOT-NAMELABEL-TEXTPROP-SELECTOR-001 [BLOCKED] · body: `tickets/GT-069.md` (หัวใบเดิม 1499 B + 1 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## GT-072 ACTOR-SLOT-DISPLACEMENT-001 [PARTIAL] · body: `tickets/GT-072.md` (หัวใบเดิม 1508 B + 5 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## GT-074 OCCLUSION-CAMERA-ANGLE-CONTROL-001 [attended, in-game]: หลัง `SPAWN_BARE` ทับพิกัด `P0` — **NPC `Navy Transfer` โผล่กลับมาให้เห็นจากมุมกล้องอื่นหรือไม่** (ตัวคุมมุมกล้อง `W2` ที่รอบแรกของ `GT-072` ไม่ได้ทำ)  [🟢 **PENDING — attended · รันได้บน `main` ปัจจุบัน ไม่รอ merge ไม่รอ CI ไม่รอเจ้าของ · ศูนย์สล็อต** · เปิดใบโดย chief R170 (2026-08-25 ~22:2x +07:00 · session `2ilw5p`) ตามผลรอบแรกของ `GT-072` §② · เขียนใบโดย `pf-queue-author`] -- moved to `tickets/GT-074.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `ec26p6` 2026-09-06T21:18+07:00)
## 🆕 GT-076 POPULATION-FULL-001-ACTOR-CEILING-STAIRCASE-001 [attended, in-game]: ไคลเอนต์รับ actor ใน RuntimeRes collection **เดียว** ได้กี่ตัว - เดินบันไดซ้อนของสำมะโน `bg0001` 3 -> 20 -> 60 -> 115  [🔴 **BLOCKED — รอ merge ก่อน** · **`BLOCKED-ON-WIRING` จบแล้ว (chief R173 ต่อสายให้ + ใส่ `--world-census-actors`) ดูบล็อก "แก้ไข R173" ท้ายใบ** · เปิดใบโดย LANE-A 2026-08-25 ~23:1x (+07:00) ตาม `CHARTER-01` §④ BUILD-001 · เขียนใบโดย `pf-queue-author`] -- moved to `tickets/GT-076.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `cm9v9y` 2026-09-06T17:10+07:00)

## GT-078 M1-V1-ACCEPTANCE-PORT-ROYAL-POPULATION-115-001 [attended, in-game]: บูตเซิร์ฟเวอร์ **โดยไม่มีแฟล็ก scenario แม้แต่ตัวเดียว** แล้วเจ้าของเดินทั่ว Port Royal — **เมืองมีคนอยู่จริงหรือไม่ และขอ... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## 🆕 GT-079 SCENE-278-ENTRY-AND-STAGE-EYECHECK-001 [READY] · body: `tickets/GT-079.md` (หัวใบเดิม 2403 B + 11 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
ATTENDED: ขั้น 0: LOCK_GAME · boot stamp (+07:00 · teardown ปฏิเสธ stamp เก่ากว่า 420 นาที) · preflight จอว่าง (เจอหน้าต่าง elevated = ABORT) · เทียบ sha canonical · copy DB · จดแถว character_positions เดิม (scene_id, scene_seq, x, y, z, heading) = ใบเสร็จทางกลับบ้าน ไม่มีบรรทัดนี้ห้ามเริ่ม -> สตาร์ตเซิร์ฟเวอร์ก่อน client ทีหลังเสมอ (ฆ่า client กลางคัน = restart server ก่อนเปิดตัวใหม่ ไม่งั้นค้าง "connecting") -> เริ่มอัดวิดีโอ 30 fps ลง evidence_video\ (ไม่ได้อัด = NO-RESULT) -> เข้าเกม: เลือกเซิร์ฟเวอร์ -> dialog PVP ปุ่มซ้าย -> ช่องแรก -> ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง (ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด) · ห้ามพิมพ์อะไรทั้งรอบ (ช่องแชทไม่โฟกัส = ฮอตคีย์)
ATTENDED: บนจอตามลำดับ ห้ามสลับ: จับเวลากดปุ่มเข้าเกม -> เห็น HUD เป็นวินาที + บรรยายหน้าโหลดหนึ่งประโยค (C4) · ยืนนิ่ง จด HUD X/Y/Z และ **คัดชื่อแมพบน HUD/มินิแมพมาทั้งบรรทัด** (C1) · ยืนนิ่ง 30 วิ มือออกจากคีย์บอร์ด จด Z ที่ 0/10/20/30 วิ (C2) · คลิกขวาค้างลากกวาดกล้องรอบตัวหนึ่งรอบ ค้างทุก ~90 องศา มุมละ 4 วิ (A/B/C/D) จดของบัง/พื้นเรียบ-เนิน/สี/นับ actor ต่อมุม (C3, C5) · แตะ W ครั้งเดียวจด T_STEP แล้วจด X/Y/Z ซ้ำ · เดิน W/S/A/D ทิศละ ~10 วิ · VP-1 เดิน +X 600-800 หน่วยแล้วกวาดกล้องมุมเดิมนับซ้ำ · ภาพนิ่ง full-res >=5 ใบ (ห้ามกดคีย์ในหน้าต่างเกมเพื่อถ่าย ห้าม resize ลง ซูมเท่ากันทุกใบ) · อยู่ครบ 10 นาทีจากที่เห็น HUD (C6) · ห้ามใช้ Q/E ทั้งรอบ
ATTENDED: ค่าที่ต้องอ่าน/จด: บรรทัดคอนโซล `WORLD_SCENE scene_id=278 seq=0 model=Bg1177 name=beach_football_field_(TEST) spawn=(-13270.058,22794.273,-2492.769) sent_before=NO population=none save=0 marker=0 return_ticket=REQUIRED` เป๊ะทั้งบรรทัด (ไม่มีบรรทัดนี้ หรือ scene_id ไม่ใช่ 278 = หยุด N6) · เฟรมเข้าฉาก: label + pc bytes + framed bytes + frame_sha256 + scene_id ที่ decode จาก u16tag 0x12 ต้องอ่านได้ 278 (0x0116) และ scene_seq = 0 · พิกัด f32 ที่ decode ได้เทียบพิน (-13270.058, 22794.273, -2492.769) ห้ามใช้ HUD เป็นฐานคำนวณ · HUD X/Y ตอนเข้าแมพต้องอยู่ในกรอบ x [-14551.5, -8356.5] y [21667.4, 23876.8] นอกกรอบ (เช่นแถว -9239, -2830) = หยุด N6 · ErrorData มีไหม จดเลขเป๊ะ + หลังเฟรมไหน + กี่วินาทีหลัง T_ENTER (28317 = 0x6E9D parse-failure echo ห้ามอ่านเป็น "รายงานจำนวน") · census บรรทัด [G>] ทั้งไฟล์ ต้องไม่มีบรรทัดจาก npc_wire หรือ world_population
ATTENDED: ตัดสินที่ชั้น client-observable ชั้นเดียว (ชั้น wire/DB ตอบ C1-C6 ไม่ได้แม้ข้อเดียว และ "ส่ง 278 แล้วไม่มี ErrorData" ไม่ได้แปลว่าไคลเอนต์โหลด Bg1177): ตอบ C1-C6 ข้อละหนึ่งประโยค ห้ามยุบรวม ไม่ได้ดูให้เขียนว่า "ฉันไม่ได้ดูข้อนั้น" · ชื่อแมพบน HUD/มินิแมพคือสิ่งเดียวที่แยกการอ่านค่าสี่ทาง (n_ID / n_MARKER / n_CLINE_TYPE / ลำดับแถว) ⇒ ชื่อตรง Bg1177 = N1 PASS · เข้าได้แต่ชื่อแมพอื่น = N1b PASS ผลที่แพงที่สุดของใบ · เข้าได้แต่ไม่เรียบ/มีของบัง/สีไม่ขาว = N2 PARTIAL · ไม่มีพื้น = N3 PASS · ไม่ถึงสถานะเล่นได้ = N4 PASS ผลลบมีค่าเท่าผลบวก · traceback ก่อนมีไบต์ออกสาย = N5 NO-RESULT ส่งคืน chief · ห้ามรายงานว่า FAIL ห้ามเปลี่ยนพิกัด/ฉากเองเพื่อให้บูตรอด ห้ามชี้สาเหตุ · NO-CRASH ใช้คลิกขวาค้างลากเท่านั้น จดนาที 2/5/10 แยกสามบรรทัด · จดสีป้ายชื่อทุกป้ายทุกภาพ full-res (ไม่มีให้เขียนคำว่า "ไม่มี") จดสีอย่างเดียวห้ามสรุปสาเหตุ · ปิดใบต้องมี OBSERVER_CONFIRMED:
ATTENDED: บูตด้วย `py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch` (exit 0 -> `git checkout <BOOT_COMMIT>` · exit 3 = ห้ามบูต ใบอยู่ BLOCKED) + ด่านก่อนบูตห้าข้อ โดย `git grep -n 'world_scene_travel' <SHA> -- src/pirateforce_foundation/runtime.py src/pirateforce_foundation/app.py` คือด่านปลด BLOCKED (ไม่มี hit = ห้ามบูต) -> `py -3 -u -m pirateforce_foundation.app --db state\run_gt079.sqlite3 --export-events <CHIEF_FILLS_THIS_IN_AT_WIRING_TIME>` 🔴 ยังมี placeholder = BLOCKED ห้ามบูต ห้ามเดาแฟล็กเอง ห้ามใส่แฟล็ก hypothesis/scenario ตัวอื่นแม้แต่ตัวเดียว ห้ามพ่วง GT-076 · ทางเข้าฉาก 278 มีทางเดียวคือ staged GM account (`config/gm_login_scene.json` scene_id=278) หรือ GM `/warp 278` ไม่ใช่ล็อกอินปกติ · DB สำเนาเท่านั้น `state\run_gt079.sqlite3` (บูตยืนยันใช้ `state\run_gt079_confirm.sqlite3` · หนึ่งสำเนาต่อหนึ่งบูต) ห้ามเปิด canonical เทียบ sha กับ CANON_SHA.txt ก่อน-หลัง · teardown ภายใน 420 นาที + ทางกลับบ้าน `home_return_position()` แล้ว query แถวให้เห็น scene_id = 1

## 🆕 GT-080 EMPTY-VIEW-IS-THE-MAP-NOT-THE-SEND-001 [READY] · body: `tickets/GT-080.md` (หัวใบเดิม 1770 B + 1 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## 🆕 GT-081 TRAVEL-GATE-WALK-OUT-AND-WALK-HOME-001 [attended, in-game]: ผู้เล่นที่ **หยุดยืน** ในเขตที่พินไว้กลางท่าเรือ ทำให้ **ตัวเอง** ข้ามไ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-084 MOB-COMBAT-001 [🟡 **RESULT (ผ่านผลต่อของ GT-084-R2, 2026-08-27) -- wire/DB ครบ (hit x5, HP to 0, MOB-DEATH-001 kill, dying/dead frames, MOB_LOOT_DROP x2) แต่ client-observable …] · body: `tickets/GT-084.md` (หัวใบเดิม 1481 B + 0 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## GT-084-R2 HOSTILE-PAIR-VISIBLE-001: [UPDATE 2026-08-27T17:34+07:00 LANE-B ต่อยอด PANYA-REFERENCE 16:35+07:00: เกณฑ์สีที่ถูกต้องคือ **ส้ม (ยังไม่ aggro) → แดงเข้ม (aggro) → เทา (ตาย)**, ไม่ใช่ "แดง"…] · body: `tickets/GT-084-R2.md` (หัวใบเดิม 1790 B + 1 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## GT-099 BACKPACK-LOAD-REFUSED-001 [PENDING] · body: `tickets/GT-099.md` (เนื้อใบเต็ม 12350 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
## GT-101 GM-001 LOGIN-STATE-VISUAL-PROBE-001: ล็อกอินด้วยบัญชีในลิสต์ gm_accounts แล้ว GM_UpdateGMStateVital (0x5A19) ที่ CORE-REQUEST-006 ต่อสายเข้า login path แล้ว จอเปลี่ยนอะไรไหม  [RESULT -- ไม่ใช่ PASS/NO-RESULT/BLOCKED, ดูผลด้านล่าง] -- moved to `tickets/GT-101.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `43htls` 2026-09-07T00:09+07:00)

## GT-102 CORE-REQUEST-014 [PARTIAL] · body: `tickets/GT-102.md` (หัวใบเดิม 3700 B + 1 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## GT-103 GM-002 COMMAND-WIRE-CAPTURE-MATRIX-001: ล็อกอินด้วยบัญชี GM แล้วหา/เปิด GM editor widget พิมพ์ข้อความหลายแบบ -- capture file ของ `0x51E9` ขึ้นที่ `capture/gm_command_capture/` ไหม (path นี้ live บน production ครั้งแรกรอบนี้)  [NO-RESULT ต่อ claim ของตัวเอง -- A/B ทั้งสี่สถานะ UI เงียบสนิท, blocked on RE-126 · ปิดหัวใบโดย LANE-GM (เจ้าของใบ) รอบ `hs9m2r` 2026-08-28T17:1x+07:00 จากผล attended กะ1-A `notes_to_chief/20260828_1140_GT103AB-RESULT-NEGATIVE-four-ui-states-all-silent-RE118-panel-hypothesis-falsified.md` · OBSERVER_CONFIRMED: 2026-08-28T11:36-11:37+07:00 (BOOT_COMMIT `336857cd` = main HEAD, ไร้แฟล็ก) · เจ้าของคลิก `BT_GM` 4 สถานะ (HUD เปล่า / แผนที่เปิดค้าง / กระเป๋าเปิดค้าง / ปิดกระเป๋าแล้วคลิกซ้ำ) เงียบทุกครั้ง · สำมะโนเฟรมขาเข้าทั้งบูต `0x51E9` = 0 ⇒ `capture/gm_command_capture/` ABSENT ถูกต้องแล้ว ไม่ใช่ teardown fail ⇒ **ใบนี้ไม่เคยไปถึงข้อ 3 จึงไม่มีผลต่อ claim ของตัวเอง** · `TargetPosVital` x3 ช่วงเดียวกัน = client มีชีวิต ไม่ใช่เซสชันตาย · ผลข้างเคียงที่มีค่าสูง: สมมติฐานเชิงปฏิบัติของ RE-118 (เปิด panel ให้ current-UI key ไม่ว่าง) **ถูกหักล้าง** ⇒ เปิด `RE-126` ต่อ (ประตูบานแรก `this+0x48` แทนบานสุดท้าย) · [ไม่อ้าง] ว่า capture path ของ `0x51E9` ใช้ได้หรือไม่ -- ยังไม่เคยถูกทดสอบ live เลย · 🔴 **ทางเลี่ยง:** `GT-127` (คำสั่ง GM ผ่านกล่องแชท `0xAC52`) ไม่ต้องรอใบนี้และไม่ต้องรอ `RE-126`] -- archived 20260907 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md`, LANE-K round `kxpzxi`)

## GT-104 MOB-DEATH-002 [NO-RESULT] · body: `tickets/GT-104.md` (หัวใบเดิม 1796 B + 0 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## GT-106 CORE-REQUEST-014 [PARTIAL] · body: `tickets/GT-106.md` (เนื้อใบเต็ม 16999 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
## GT-106-R2 COO-DECISION-20260830-2048 IN-SESSION-TELEPORT-RENDER-001: เมื่อ TeleportVital ข้ามฉากมาถึงกลางเซสชัน (ผ่าน _dispatch_columbus_quest3021 หลังคลิกเควส 3021 ของ Columbus ไม่ใช่ตอน login) ไค... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-107 GM-001-R2 LOGIN-STATE-VISUAL-PROBE-002: ล็อกอินด้วยบัญชี GM อีกครั้งหลัง RE-105 พิน vital_version=0 (CORE-REQUEST-016 เปิดแล้ว) -- เซสชันรอดจาก error 23065 ที่ GT-101 เจอไหม แล้วจอเปลี่ยนอะไรไหม (คำถามเดิมของ GT-101 ที่ยังไม่มีใครตอบได้เพราะเซสชันตายก่อนถึง)  [RESULT -- NEGATIVE, new failure mode, error 28317, see notes_to_chief/20260827_1745_GT107-RESULT-NEGATIVE-vital-version-0-passes-version-check-but-client-throws-28317-RunTimeProtocolRes-read-failed-session-dies-GT103-not-reached-ka1-B.md -- superseded by GT-107-R3 below] -- archived 20260907 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md`, LANE-K round `kxpzxi`)

## GT-109 VEHICLE-BIND-WIRE-CAPTURE-001 [PENDING] · body: `tickets/GT-109.md` (เนื้อใบเต็ม 17169 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
## GT-110 CORE-REQUEST-017-1 [PENDING] · body: `tickets/GT-110.md` (หัวใบเดิม 2216 B + 5 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## GT-114 DIAG-MULTI-OBJECT-001 [attended, in-game]: five diagnostic objects at the city-center test point (X=11865, Y=6147), each one field away from control D0 -- does each single-field difference produce the on-screen effect that field is predicted to control, jointly closing the attended half of RE-107/RE-108/RE-109's own proposed follow-ups  [CANCELLED - covered by R309 (D0 · RE-108) / refuted by production DYING_TIMER_SECONDS=20 (D1a · ภาพ 185937) / covered by GT-129 (D1b) / D2 control-only / covered by GT-084-R2 + P-2/RE-067 (D3) — Panya agreed 2026-09-04 21:4x · ปิดโดย chief รอบ `epkucn`/R344 2026-09-04 22:56 +07:00 ตาม `COO-DECISION 20260904_2158` (ถอน `2142` ข้อ 2 = ไม่พ่วงบูตกับ `ATTACK-POSE-ONE-FIELD-AB-001`) · กฎ `PANYA-DECISION 20260903_1934` · เหตุผลรายข้ออยู่ใน `notes_to_chief/20260904_2133_KA1A-TO-COO-attack-pose-*` §1 · เดิม: PENDING -- wiring landed R202 (9b6zl6) · archived โดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)]

---

- ~~GT-107-R3 GM-001-R3 LOGIN-STATE-VISUAL-PROBE-003: after RE-113 (trailing change-mask byte) + CORE-REQUEST-020 (field_0x0b_second=1) both landed on main, does a real client now accept GM_UpdateGMStateVital cleanly, and does BT_GM actually appear~~ -> `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md` (RESULT -- outcome (a)/(b)/(c) ไม่ตรงเป๊ะสักข้อ, ดูผลด้านล่าง] ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

## GT-116 CORE-REQUEST-022 CLASS-LEVEL-LOGIN-SKILLWINDOW-UNBLOCK-001: after CORE-REQUEST-022 wires class_id=1 (Gladiator) + level=1 into every login's ActorAttr/BasicAttr frames, does a real client's ... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-122 CORE-REQUEST-027 NAME-FIELD-GUILD-SLOT-FIX-001: after CORE-REQUEST-027 moves the character's own name off ActorAttr's guild-name slot (`+0x164`, mask bit `0x01000000`, `LABEL_GUILD`) and ont... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-120 CORE-REQUEST-025 TRACEPATH-GO-BUTTON-STALL-CLEAR-001: after CORE-REQUEST-025 wires an empty-vector `CTracePathVital` (0x2F92) reply to every `CTracePathReqVital` (0x4391), does a real client... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-121 CORE-REQUEST-026 BG0002-ARRIVAL-CENSUS-NO-WASD-001: after CORE-REQUEST-026 makes the Bg0002 (Prison Exile Island) census fire on `teleport_s... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## GT-124 MOB-PICKUP-CLAIM-PREVALIDATION-001 [BLOCKED-ON-WIRING] · body: `tickets/GT-124.md` (เนื้อใบเต็ม 13045 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
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

## GT-128 GM-003 CHAT-WARP-VISIBLE-001 [attended, in-game]: GM พิมพ์ `/warp <ฉากปัจจุบัน> <x> <y>` ลงกล่องแชทธรรมดา แล้ว**ตัวละครขยับไปยังพิกัดนั้นบนจอจริงหรือไม่** -- ใบแรกของสาย GM ที่ตัดสินที่จอ ไม่ใช่ที่ log -- archived 20260906 (CANCELLED - refuted by R306 finding 3; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

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
## GT-132 GROUND-DROP-COALESCED-GENERATION-DRAWS-N-LABELS-001 [READY] · body: `tickets/GT-132.md` (เนื้อใบเต็ม 20302 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
## GT-133 GM-003 [BLOCKED] · body: `tickets/GT-133.md` (หัวใบเดิม 237 B + 23 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

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
> 🟢 **[LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ทำตาม `notes_to_chief/20260907_1346_COO-DECISION-panya1313-ticket-heads-citing-103-LANE-K.md` ข้อ 1]** เจ้าของเคาะเอง (`PANYA 1313`, ยกมาอยู่ใน `NOW.md`): **แมพ 2 ไม่มี Orc Chief** ⇒ `n_ID/template 103` ที่ setnum อ่านได้ในฉาก 2 = **การอ่านผิด** · `bg0002` ใช้กฎ `cline` (roster 12 ตามที่เซิร์ฟเวอร์พิมพ์บนเครื่องเจ้าของ) · K แก้เฉพาะหัวใบ/แถวคิว ไม่แตะเนื้อใบ ไม่ rename ไม่ลบ (COO ข้อ 4) · **ฉากอื่นที่ `103` โผล่ ไม่ถูกแตะ** (COO ข้อ 2) — พาดหัวใบนี้ถามว่า *"ตรงนั้นมี Orc Chief หรือไม่มีอะไรเลย"* ⇒ **คำตอบเคาะแล้ว: ไม่มี Orc Chief ในแมพ 2** · ใบถูก archive ไปแล้ว (stub ด้านบน) K ไม่เปิดใบใหม่และไม่แก้เนื้อใบใน archive

## GT-142 M5-KILL-PICKUP-RELOG-ROUNDTRIP-001 [BLOCKED] · body: `tickets/GT-142.md` (เนื้อใบเต็ม 18787 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
## GT-144 TEN-MARKER-SCENES-FIRST-EYES-001 [BLOCKED] · body: `tickets/GT-144.md` (เนื้อใบเต็ม 16051 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
## GT-145 CONSOLE-ENCODING-MEASURE-001 [STATIC-ON-BRIDGE -- วัดบนสะพานตอนเซิร์ฟเวอร์รันจริง · ไม่บูตไคลเอนต์ ไม่ล็อกอิน ไม่มีตัวละคร · ~15 นาที]: คอนโซลของเครื่องเจ้าของเป็น encoding อะไร -- พิมพ์สี่ค... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-146 PICKUP-CLICK-OPCODE-CAPTURE-001 [attended, in-game]: คลิกซ้ายลงบน element ของตกที่เซิร์ฟเวอร์เราส่งเอง แล้ว **ไคลเอนต์ยิงเฟรมอะไรออกสาย** -- ใบ capture ที่ปลด `RE-125`/`GT-124`/M5  [⚪ **CANCELLED - covered by R303 attended capture 20260902_1755 (46 inbound 0x4543 frames, 2 completed takes), confirmed R306** — ปิดโดย chief (LANE-E) รอบ `m8wtlr`/R356 2026-09-05T17:0x+07:00 ตาม `COO-DECISION 20260905_0249` ข้อ 1 (ทวงเป็นครั้งที่สองโดย `COO-DECISION 20260905_1649` หลังค้าง 14 ชม.) · **คำถามของใบนี้ถูกตอบบนไวร์ไปแล้ว**: R303 จับเฟรมขาเข้า `0x4543` 46 เฟรมจากการคลิกจริง ยืนยันซ้ำ R306 · หลักฐานที่วัดบนไวร์ชนะคำสั่งที่เขียนจากชื่อใบ (`COO 0249`) · 🔴 **คำถามที่ยังเปิดอยู่ในใบนี้ไม่ได้ปิดไปกับมัน** — `REEMISSION_REDRAWS_THE_LABEL` ย้ายไปอยู่ใต้ `GT-223`/`RE-208` ของ LANE-B ในรอบเดียวกัน ตาม `COO 0249` ข้อ 1 ประโยคท้าย · ~~🔴 BLOCKED - until P-2 closes (NOW) — เงื่อนไขเดียว ไม่มีเงื่อนไขอื่น~~ · ตั้งโดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 ตาม `COO-DECISION 20260904_2349` ข้อ 5 · ที่มา: `NOW.md` หัวข้อ "ห้ามทำจนกว่า P-2 จะปิด" ระบุชื่อใบนี้ตรง ๆ · เงื่อนไข `GT-188` checkpoint 2 **ตัดทิ้งแล้ว** (`GT-188`/`GT-188cp1` ยกเลิกตาม `PANYA-DECISION 20260903_1934` · `COO 20260904_1648`) · เปิดโดย LANE-B รอบ `uq2lxw2` · แก้ขั้นตอนตาม `PANYA-ORDER 20260830_1450` ที่รอบ `xt0g9c` · archived โดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)]

---

## GT-147 COUNTER-RESYNC-RECOVERY-TOOL-001 [BLOCKED] · body: `tickets/GT-147.md` (เนื้อใบเต็ม 13562 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
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

## 🆕🔬 GT-158 ACTIONVITAL-FIELD-U16-4A-LIVE-SCENE-TRACKING-001 [PENDING] · body: `tickets/GT-158.md` (เนื้อใบเต็ม 8660 B ย้ายคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:15+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1 ก้อน 2/2)

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
## 🆕 GT-166 DEEP-SEA-TEMPLE-LANDING-GEOMETRY-001 [READY] · body: `tickets/GT-166.md` (เนื้อใบเต็ม 10437 B ย้ายคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:15+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1 ก้อน 2/2)
ATTENDED: see `tickets/GT-166.md` (บล็อกเดิมเก็บไว้ในไฟล์นั้น คำต่อคำ)

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

## 🆕 GT-171 EVIL-PORT-FIRST-EYES-001 [READY] · body: `tickets/GT-171.md` (เนื้อใบเต็ม 9054 B ย้ายคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:15+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1 ก้อน 2/2)
ATTENDED: see `tickets/GT-171.md` (บล็อกเดิมเก็บไว้ในไฟล์นั้น คำต่อคำ)

## GT-172 GM-003 CHAT-WARP-CROSS-SCENE-LIVE-TELEPORT-001 [attended, in-game]: GM พิมพ์ `/warp <ฉากอื่น> x y` ในกล่องแชท -- จอเปลี่ยนไปฉากปลายทางจริงกลางเซสชันไหม (ไม่ต้อง relog)  [✅ **PASS ทั้งสองชั้น... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-173 OCEAN-WALLED-CITY-FIRST-EYES-001 [READY] · body: `tickets/GT-173.md` (เนื้อใบเต็ม 10667 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
ATTENDED: see `tickets/GT-173.md` (บล็อกเดิมเก็บไว้ในไฟล์นั้น คำต่อคำ)
## GT-174 SILVER-HARBOUR-FIRST-EYES-001 [READY] · body: `tickets/GT-174.md` (เนื้อใบเต็ม 11215 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
ATTENDED: see `tickets/GT-174.md` (บล็อกเดิมเก็บไว้ในไฟล์นั้น คำต่อคำ)
## 🆕 GT-175 SPICE-PARADISE-FIRST-EYES-001 [attended, in-game]: ฉาก 3 (Bg0003, Spice Paradise Island) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเ... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## GT-176 VOODOO-ISLAND-FIRST-EYES-001 [READY] · body: `tickets/GT-176.md` (เนื้อใบเต็ม 12198 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
ATTENDED: see `tickets/GT-176.md` (บล็อกเดิมเก็บไว้ในไฟล์นั้น คำต่อคำ)
## 🆕 GT-177 DEATH-CITY-SEA-FIRST-EYES-001 [BLOCKED] · body: `tickets/GT-177.md` (เนื้อใบเต็ม 9868 B ย้ายคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:15+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1 ก้อน 2/2)

## GT-178 BG0015-HOSTILE-TWELVE-AGGRO-001 [attended, in-game]  [🔴 **NEGATIVE-MEASURED — R322C** 2026-09-07T01:48+07:00 -- moved to `tickets/GT-178.md` (>8,192 B, verbatim, LANE-K round `mb9vtg` 2026-09-08T19:22+07:00 -- GAME_TEST_QUEUE.md was approaching the 1,000,000 B Contents-API ceiling; nothing deleted, full block including R322C result + B's build-ticket proposal preserved verbatim in the ticket file)]

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

## 🆕 GT-180 NAVY-TRAINING-CAMP-FIRST-EYES-001 [BLOCKED] · body: `tickets/GT-180.md` (เนื้อใบเต็ม 10241 B ย้ายคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:15+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1 ก้อน 2/2)

## GT-181 PLAYER-DEATH-PREDICATE-PROBE-001 [PENDING] · body: `tickets/GT-181.md` (เนื้อใบเต็ม 11207 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
## GT-182 GM-A-WARP-NO-COORD-LIVE-SPAWN-001  [PASS -- OBSERVER_CONFIRMED 2026-09-01T10:40+07:00, chief round 8zf80f] -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-183 GM-B-SPEED-COMMAND-001  [❌ **CANCELLED - refuted by GT-218 (`/speed 400` killed the client in one frame, R306); open question carried by GT-... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## GT-184 UI-A-PART-A-BACK-TO-CHARSELECT-BUTTON-001 [BLOCKED] · body: `tickets/GT-184.md` (เนื้อใบเต็ม 13524 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
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
  - FACT CORRECTION [LANE-K round ci8200, per PANYA `1520` item 2 / `COO-DECISION
    20260908_1642 gt186-label-flip-and-gt185-fact-correction`]: the sentence formerly
    here claimed the only way back into the game was closing the window and rebooting
    the whole round. The owner's own play contradicts that: closing the client process
    and opening a fresh `GameClient` already returns the player to a live game
    (character-select -> enter game) with no server reboot -- the server keeps running
    across that. The remaining, narrower cost this entry actually tests is: **there is
    still no known way to get back into a live game WITHOUT closing the client process
    first** -- i.e. a same-process character-select -> game round-trip. This entry
    proves whether that narrower capability exists.
  - (The "full reboot every round" cost some testers see comes from this project's own
    attended-boot tooling, which tears the queue down as soon as the client process
    closes -- that is a tooling limitation, not a game limitation, and ka1-A owns it on
    the tooling side. Not this ticket's scope.)
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

## GT-186 UI-B-REAL-LOGOUT-BUTTON-001  [SUPERSEDED-BY: GT-308 -- withdrawn per `COO-DECISION 20260908_1943` item 1 (rule 0159 "new result covers = withdraw"), applied LANE-K round `g3nkno` 2026-09-09T14:25+07:00] -- archived 20260909 (SUPERSEDED; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260909_closed.md`, LANE-K round `ajt28l`)
## GT-187 GM-045-CENSUS-SCENE-RESYNC-CLIENT-CONFIRM-001  [❌ **CANCELLED - no longer needs proving because ทางเข้าของใบนี้ไม่มีอยู่บน `main` วันนี้** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 202609... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-188 GROUND-DROP-HEARTBEAT-PRESERVE-CONFIRM-001 [CANCELLED] · body: `tickets/GT-188.md` (หัวใบเดิม 1435 B + 5 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

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
## GT-199 CORPSE-REARM-AND-DROP-CROSS-SCENE-SCOPE-001 [PENDING] · body: `tickets/GT-199.md` (เนื้อใบเต็ม 19869 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
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

🔵 **[LANE-K รอบ `lpjqus` 2026-09-07T20:5x+07:00 · ไม่เปลี่ยนสถานะใบ] แถวนี้เป็นแถวเดียวใน 29 แถวที่ `tools_bridge/pf_results_index.py` ตีว่า `HDR-ELSE` (คำว่า PASS อยู่ในประวัติหัวใบแต่ไม่ใช่สถานะปัจจุบัน) — ตรวจแล้ว **ไม่ใช่หัวใบล้าสมัย และไม่ใช่งานค้างของเสมียน**: ใบถูกวัดจริงและได้ผลก่อน แล้วจึงถูกยกเลิกทีหลังด้วยคำตัดสินที่ใหม่กว่า
- ผล (2 ก.ย. · ยกมาคำต่อคำจากบรรทัด `RESULT:` ของจดหมาย `notes_to_chief/20260902_1755_KA1A-R303-RESULTS-*.md`): `RESULT: GT-204 PASS R303 2026-09-02` · หัวข้อในจดหมายคำต่อคำ: *"## GT-204  ->  [PASS] on the full chain, with three defects found on the way"*
- คำตัดสินที่ใหม่กว่า (3 ก.ย.): `CANCELLED - covered by GT-216` โดย chief ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2 ⇒ **สถานะปัจจุบันคือ CANCELLED ไม่ใช่ PASS**
- 🔴 **K ไม่พลิกสถานะกลับเป็น PASS** (นั่นคือการตัดสิน ไม่ใช่การคัดลอก) — บันทึกไว้เพื่อให้คนอ่านรู้ว่าใบนี้ **เคยวัดแล้วผ่าน** ก่อนถูกยุบ
- 🟡 **รันเครื่องมือซ้ำหลังเขียนบรรทัดนี้: ยังขึ้น `HDR-ELSE` เหมือนเดิม (`rows needing a clerk: 1`)** — ไม่ใช่การเขียนแล้วหาย · เครื่องมืออ่าน "คำสถานะแรกของหัวใบ" ซึ่งคือ `CANCELLED` และมันถูกแล้ว ⇒ ที่ควรแก้คือ **กติกาการอ่านของเครื่องมือ** (แยก "ผลที่วัดได้" ออกจาก "สถานะปัจจุบัน") ไม่ใช่หัวใบ · เข้าคิวงานสำรองข้อ 1 ของสาย ไม่แตะในรอบนี้
## GT-205 UI-A-BACK-BUTTON-VISIBLE-NOTICE-001 [🟡 **สถานะเดิม: client-observable = PASS · wire/DB = NOT MEASURED · ใบยังไม่ปิด** (ยกคำต่อคำจากประโยค "สถานะเดิม: ..." ที่ฝังอยู่กลางย่อหน้าเดิม ขึ้นมาไว้หน้าสุด…] · body: `tickets/GT-205.md` (หัวใบเดิม 1082 B + 5 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## GT-207 GM-PLUGIN-THREE-CELL-BUTTON-001  [**PASS** on build 1 -- ka1-A/เจ้าของ 2026-09-02T18:54+07:00 · `OBSERVER_CONFIRMED` มีในใบผล · ผล: `notes_to_chief/20260902_1915_KA1A-GT-207-PASS-the-gm-butt... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-210 CHOOSE-NPC-SCENE3-CLICK-ANSWER-001  [✅ **PASS · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — R306 บนจอเจ้าของ (`no... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-211 UI-B-EXIT-BUTTON-VISIBLE-NOTICE-001  [✅ **PASS สองชั้น · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — R306: `EXIT ... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-212 CHOOSE-NPC-NINE-ROSTER-ISLANDS-CLICK-ANSWER-001  [✅ **PASS · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — R306 บนจ... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
- ~~GT-213 COLUMBUS-SCENE-GUARDS-VISIBLE-COST-001~~ -> `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md` (🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS on (A) และ ( ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

## GT-214 CHOOSE-NPC-SCENE2-CLICK-ANSWER-AND-HOSTILE-SAFETY-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS-AGAIN (regression ยืนยันซ้ำ R321 2026-09-06 11:52 · ผลแรก PASS... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
- ~~GT-215 NEWBORN-CHARACTER-IS-BORN-WITH-VITALS-001~~ -> `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md` (🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS on its own c ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

## GT-216 MULTI-VITAL-WALKER-MAKES-GROUND-PICKUP-PLAYABLE-001  [✅ **PASS สองชั้น · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-217 ATLANTIS-OCEAN-PANEL-CENSUS-ON-A-GM-SINGLE-USE-ENTRY-001 [PASS] · body: `tickets/GT-217.md` (หัวใบเดิม 1137 B + 11 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
ATTENDED: RECHECK สามข้อผ่านก่อนเสมอ (`WORLD_CENSUS_BG3001` + `scene_is_sanctioned_for_a_gm_entry` เจอบน `origin/main` + pytest เขียวทั้งชุด) แล้วค่อยบูต -> ล็อกอิน GM เข้าฉากบ้านถ่าย `S00-HOME` -> คลิกช่องแชทยืนยัน focus จริง พิมพ์ `/warp 126` Enter รอ ~3 วิ -> **ล็อกเอาต์แล้วล็อกอินกลับด้วยตัวละครเดิม** เพื่อลงสเตจที่ spawn `(3050,232,90)` ถ่าย `S126-A/B/C` (หมุนด้วยคลิกขวาลาก) -> เดินหนึ่งก้าว (`W`/`S`) คลิกซ้ายเลือก actor 1-3 ตัว ถ่าย `S126-CLICK1..3` (ห้ามตี ห้ามสกิล มี Jellyfish King)
ATTENDED: คัดคอนโซลรวม `2>&1` หา `WORLD_POP_HANDOFF scene=126` ตามด้วย `WORLD_CENSUS_BG3001 assembled=<N>/38` + actor `<N>` บรรทัด + `BG3001_UNSHIPPED` `38-<N>` บรรทัด · 🔴 `<N>` ไม่ใช่ค่าคงที่ หาเองก่อนบูตตามข้อ 3 (`grep -c NAME_CP874_HEX` บน `origin/main`: `0`=36 · `9`=37) ไม่ตรง = FAIL ชั้น wire + คลิกตอบ `LANE_A_CHOOSE_NPC_SCENE126_ANSWERED`/label `FACE_P<n>` (คลิกแรกก่อนก้าวเดินถูกปฏิเสธ `no_player_position_walk_one_step` = ไม่ใช่ FAIL) · `COLUMBUS_CHOOSE_NPC_WRONG_SCENE` คัดลงเฉย ๆ ไม่ใช่ STOP
ATTENDED: ผลตัดสินอยู่ที่ **client-observable เท่านั้น** (คอนโซลตอบไม่ได้ว่าอะไรถูกวาดบนจอ) -- นับจำนวน actor ที่วาดจริงจาก `S126-A/B/C` เขียนเลขตรง ๆ, บรรยายก้อนเกาะ `MAP_ISLAND_01` สี่ก้อนวาดออกมาเป็นอะไรตามที่เห็นห้ามเดาสาเหตุ, จดว่าเห็นป้ายลอยของมาร์กเกอร์ Tornado กี่ป้ายไหม (ทำนายผิด = finding), และ **สีป้ายชื่อทุกป้ายทุกภาพหนึ่งบรรทัดต่อป้าย** (ไม่มี = `none` · full-res เท่านั้น · จดสีอย่างเดียว)
ATTENDED: บูต = มาตรฐาน ไม่มีแฟล็ก scenario ใด ๆ + `-SecondPasswordMode bypass` + บัญชี GM จาก `config/gm_accounts.json` บนสำเนา DB `state\run_gt217_<stamp>.sqlite3` เท่านั้น (ห้ามเปิด canonical เด็ดขาด จด sha256 ก่อน/หลังทั้งสำเนาและ canonical) -- เซิร์ฟเวอร์บูตใหม่สดก่อนไคลเอนต์เสมอ · 🔴 จอจะเปลี่ยนฉากตอน `/warp 126` หรือไม่ ไม่ใช่ตัวตัดสินใบนี้ จดแล้วเดินต่อ (`decreed_arrival` ของ 126 ขึ้น main แล้ว วาปสดได้ · เรื่องวาปสดเป็นของ `GT-266`) ใบนี้ตัดสินที่สำมะโน 126 เท่านั้น
ATTENDED: STOP ทันทีถ้าเห็นหน้าต่างบทสนทนา/เควสต์ หรือรู้ตัวว่าอยู่คนละฉากหลังคลิก (ปิดไคลเอนต์รายงานทันที ห้าม retry) · NO-CRASH ใช้คลิกขวาลากเท่านั้น ห้าม `Q`/`E` (ยิง `TargetPosVital`) · ปิดใบด้วย `OBSERVER_CONFIRMED: <timestamp>` เท่านั้น ไม่มีลายเซ็น = `AWAITING-OBSERVER`

## GT-218 SPEED-SAFE-VALUE-400-DRY-RUN-CLIENT-SURVIVES-001  [**CLOSED** -- ❌ **FAIL · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00** -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-219 GM-IMAGE-CHECKER-MEETS-TWO-REAL-DLLS-001  [✅ PASS ทั้งสองขั้น -- ปิดใบ · ขั้น A `20260904_1508` (ชิ้น (ก) ผ่านครบ · ชิ้น (ข) `A2 NO-RESULT`... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## GT-220 GROUND-DROP-SURVIVES-A-CLICK-ON-A-TOWNSPERSON-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS (R307 2026-09-03 — killed mobs, 2 drops on floor survived NPC clicks,... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-221 LOGIN-SENDS-THE-ROW-NOT-THE-CONSTANT-THREE-SHAPES-001 [BLOCKED] · body: `tickets/GT-221.md` (เนื้อใบเต็ม 18018 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
## GT-223 GROUND-LEDGER-SURVIVES-A-RECONNECT-001 [FAIL] · body: `tickets/GT-223.md` (เนื้อใบเต็ม 22037 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
ATTENDED: see `tickets/GT-223.md` (บล็อกเดิมเก็บไว้ในไฟล์นั้น คำต่อคำ)
## GT-225 GROUND-CELL-FOLLOWS-A-WALKING-PLAYER-ACROSS-A-SCENE-EDGE-001 [BLOCKED] · body: `tickets/GT-225.md` (เนื้อใบเต็ม 11137 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
## GT-226 LOGIN-DRAWS-THE-CLASS-SHE-PICKED-AT-CREATION-001 [BLOCKED] · body: `tickets/GT-226.md` (หัวใบเดิม 926 B + 5 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## GT-228 ISLAND-CONTACT-TRIGGER-FRAME-CAPTURE-001  [🟢 **PASS (กล่อง B) — ปิดโดย chief (LANE-E) รอบ `wjqykr`/R338 2026-09-04T14:0x+07:00**] ~~[OPEN --... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## GT-230 NPC-SHOP-SELL-SLOT-FRAME-CAPTURE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS ตามเกณฑ์ใบ (เก็บ hex ลากไอเทมลงช่องขาย 2 ครั้งซ้ำได้ NPC 'Chalais') — R320... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-233 M2-PROVISIONING-TRIAL-001 [CLOSED] · body: `tickets/GT-233.md` (หัวใบเดิม 4110 B + 1 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)

## GT-242 BACKPACK-OPEN-DOES-NOT-WIPE-THE-GROUND-001  [✅ **ปิดใบ: PASS สองชั้น (เว้น item(4) NO-RESULT) ตาม `R316` 2026-09-05T11:02+07:00** — ยืนยันโดย `COO-DECISION 20260906_1452` (R321 ด้านล่างในบล็อกประวัติ = ความพยายามวัดซ้ำหลัง PASS ไม่ใช่ผลใหม่) · พับปิด+archive โดย LANE-K รอบ `rsmsia` 2026-09-06T15:09+07:00 -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)]
---

## GT-243 HOTBAR-SKILL-99-VS-WIELD-Z-SAME-SESSION-HEX-DIFF-001 [BLOCKED] · body: `tickets/GT-243.md` (เนื้อใบเต็ม 25977 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
## GT-244 LIVE-WARP-SCENE-PERSISTS-ACROSS-LOGIN-001  [🚫 CLOSED -- CANCELLED - covered by 20260904_1911 R310 ข้อ 3 -- ยกเลิกโดย chief รอบ `t7bsfx`/R342 ตาม `COO-DECISION 20260904_1948` ข้อ 2 -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-245 CHARACTER-SELECT-SCREEN-SHOWS-THE-REAL-SCENE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — ครึ่งหลัง PASS — R317 2026-09-05 §1: หลัง /warp 1 (persist R316) → relaunch... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-246 AUTO-WALK-CLICK-DIFFERENTIAL-001  [ANSWERED -- วัดครบแล้วในรอบ attended R310 (2026-09-04 18:45-19:07 +07:00) ตั้งแต่ก่อนใบนี้มีเลข -- ห้ามบู... -- archived 20260907 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md`, LANE-K round `kxpzxi`)

## GT-247 ATTACK-POSE-ONE-FIELD-AB-001  [🟢 **PASS -- R315 2026-09-05 10:11-10:2x** · `OBSERVER_CONFIRMED 2026-09-05T10:24+07:00` · ปิดหัวโดย chief (LA... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## numbering
ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `246` (`GT-246`) => ใบนี้ `247`
`GT-247`/`RE-247` = 0 hit ทั้งสามที่ก่อนวาง (ตรวจโดย chief รอบ `epkucn`/R344)

---

## GT-249 LEARN-SKILL-RESULT-REAL-KIT-CONTENT-001 [PASS] · body: `tickets/GT-249.md` (หัวใบเดิม 2819 B + 11 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
ATTENDED: บูต `--learn-skill-result-hypothesis-scenario ...learn_sweep.json` (คนละบูตกับ GT-243) Gladiator lv1 กด K ถ่ายภาพ baseline (S-BASE-K)
ATTENDED: focus แชท พิมพ์ `SKILLCONTENT` (12 ตัว) Enter ดึง focus ออก รอ >=20s กด K ถ่ายภาพ (S-FINAL-K)
ATTENDED: ผ่าน = S-FINAL-K มี 4 รายการ: VIP Strive Jump/Gladiator Basic Training/Normal Attack/Strive Jump
ATTENDED: ไม่ผ่าน = 0 รายการ/ไม่ตรงชื่อแม้เฟรม 6 ออกสะอาดแล้ว = finding ไม่ใช่ FAIL (ปิดคำถามเปิดในโมดูลรอบเดียวกัน P3)
ATTENDED: gate 0/1/2 ผ่านก่อนบูต ห้ามเดา SHA

## numbering
`GT-248` ถูกใช้เป็น `RE-248` ในรอบเดียวกัน (`CLIENT_RE_QUEUE.md` -- ตัวนับร่วมสองคิว) => ใบนี้ `249`
`GT-249`/`RE-249` = 0 hit ทั้งสามที่ก่อนวาง (ตรวจโดย chief รอบ `epkucn`/R344)

---

## GT-254 ISLAND-155-CONTACT-TRIGGER-FRAME-CAPTURE-001  [⛔ **CLOSED = `CANCELLED - refuted by KA1A-R318 §3 (Slave Market Island/แถว 155 อยู่ฉาก 304 Dark Fog Sea ไม่ใช่ 126)`** -- ปิดโดย chief (LANE-E)... -- archived 20260905 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260905_closed.md`)
## GT-250 NAME-LABEL-PERSISTS-AFTER-WALK-AWAY-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — NEGATIVE-AGAIN (ป้ายชื่อไม่หายซ้ำ R321 2026-09-06 11:29 · ผลแรก NEGATIVE ที่ R317... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-251 TRACEPATH-GO-TWO-TARGETS-DISCRIMINATOR-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — ANSWERED — ตอบ RE-236(ข)/RE-119 T4: id ที่ client ส่งใน TracePathVital คือ id... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-252 COLUMBUS-OPTION2-BORNAGAIN-CLICK-CAPTURE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS — เก็บครบตามใบ (R317 2026-09-05 §4: quest 3205 ถูกปฏิเสธ... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
- ~~GT-253 OPTIONS-APPLY-ONE-SETTING-DIFFERENTIAL-CAPTURE-001~~ -> `archive/GAME_TEST_QUEUE_ARCHIVE_20260907_closed.md` (🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — ตรวจแล้ว — ไม่มีใ ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

## GT-255 SECOND-PASSWORD-AND-BAG-INBOUND-FRAME-CAPTURE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — ปิดได้ตามเกณฑ์ 'จับเฟรม' — Event B (เปิดกระเป๋า) ครบสองชั้น · Event A... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-257 CHAT-TWO-VITAL-TAIL-ONE-TYPING-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS 3/3 — กด M เปิด/ปิดแล้ว /warp ทันที ไม่พบ two-vital ในบูตนี้ (สมมติฐาน 'จะเห็น vital... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-258 WARP-SEND-FAILURE-ROLLS-THE-SCENE-BACK-001 [READY] · body: `tickets/GT-258.md` (เนื้อใบเต็ม 45561 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
ATTENDED: see `tickets/GT-258.md` (บล็อกเดิมเก็บไว้ในไฟล์นั้น คำต่อคำ)
## GT-262 STALL-AND-GUILD-STORAGE-ATTENDED-CAPTURE-001  -- archived 20260908 (CANCELLED by owner LANE-UI round `fvp9ke` 2026-09-07T04:56+07:00; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260908_closed.md`)

---
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

## GT-266 WARP-126-LIVE-TELEPORT-001 [READY] · body: `tickets/GT-266.md` (เนื้อใบเต็ม 17132 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
ATTENDED: see `tickets/GT-266.md` (บล็อกเดิมเก็บไว้ในไฟล์นั้น คำต่อคำ)
## GT-267 SEA-EDGE-CROSSING-126-TO-304-AND-305-001  [⚪ **RESERVED -- เนื้อใบ**มาถึงแล้ว**แต่ยังไม่ได้วางลงคิว** · LANE-A ส่งเนื้อใบเต็ม 2026-09-05T19:00+07:00 (`notes_to_chief/20260905_1900_LANE-A-GT-267-TICKET-BODY-sea-edge-crossing-126-to-304-305.md`) · 🔴 **chief ยังไม่วางเพราะเนื้อใบ 25,293 อักขระ = เกินเพดานใบใหม่ 8 KB ของ `AGENTS.md` §11 สามเท่า** [วัดแล้ว รอบ `rz1fxh`/R358] และ `GAME_TEST_QUEUE.md` วันนี้ 2.8 MB ที่ทุกสายอ่านทุกรอบ ⇒ chief ย่อเป็นถ้อยคำใบ (คำถาม + เกณฑ์สองชั้น + สถานะ + ลิงก์ไปจดหมาย) แล้ววางในรอบ LANE-E ถัดไป · **ถึง LANE-A: ไม่ต้องส่งซ้ำ ไม่ต้องรอ ใบนี้ไม่บล็อกงานสร้างของคุณ** (ใบนี้เป็นใบ attended และเครื่อง Panya ปิดอยู่) · เดิม: **เลขจองเท่านั้น เนื้อใบยังไม่เขียน** · **เจ้าของใบ/ผู้เขียนเนื้อใบ = LANE-A ร่วม LANE-GM** · จองโดย chief (LANE-E) รอบ `r045nx`/R354 ตาม `COO-DECISION 20260905_1349` ข้อ 4(ค) + `1348` ข้อ 6]

> คำถามที่ใบนี้จะถาม: แล่นเรือชนขอบแมพของฉาก 126 แล้ว**เปลี่ยนฉากจริงบนจอ** -- ขอบตะวันตก -> ฉาก 304 (Atlantic Ocean: Dark Fog Sea) · ขอบใต้ -> ฉาก 305 (Pale Silver Sea) · เป็นกลไกที่ `GT-254` (CANCELLED) ต้องรอ และเป็นทางเดียวที่จะไปถึงเกาะ 155 Slave Market Island
> วัตถุดิบที่วัดแล้ว (R318 §4 · capture-only ไม่แตะเซิร์ฟ): ขอบตะวันตก = เส้น X ≈ -8090 ยิง `TriggerVital 0x1FB2` id **7** ซ้ำได้ 2/2 ที่ Y ต่างกัน 3,478 หน่วย · ขอบใต้ Y ≈ -8384 = id **69** · ขอบเหนือ Y ≈ +6413 = id **48** · ขอบตะวันออก = **ไม่มีเฟรม** (`12 B2 1F` = 0 ในช่วงนั้น)
> 🔴 nonclaim ที่ต้องติดไปกับใบ: id บนสาย **ไม่ตรง**เลขฉากปลายทาง (304/305) และไม่ตรง `trigger_tip_th.tsv` ⇒ เป็น namespace ที่สาม · ชื่อ PROP ที่ hook พิมพ์ (`Viper Wicket`/`Ground Site Entrance`/`Captive Cage`) **ห้ามเชื่อ** · id 48 (ขอบเหนือ) ยังไม่รู้ว่าเป็นทางออกจริงไหม (แผนที่ไม่มีลูกศรเหนือ)
> 🔴 **ห้ามสายอื่นใช้เลข `GT-267`** · ต้องใช้ตัวส่ง "เปลี่ยนฉากสด" ตัวเดียวกับที่ `/warp` สดต้องการ (`GT-258`/`GT-266`) ⇒ งานร่วม A+GM

- numbering: `GT-267`/`RE-267` = **0 hit ทั้งสามที่** ก่อนจอง **[วัดแล้ว รอบนี้]**


## GT-269 GMUI-P3-WINDOW-ROW-CENSUS-LABELS-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS-CLIENT (GMUI 3 แท็บ 7/5/5 แถวตรง census · ต้องมี GameMaster.dll ติดถาวรข้าง client... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)
## GT-272 EQUIP-WEAPON-FROM-BACKPACK-PERSISTS-ACROSS-RELOG-001 [READY] · body: `tickets/GT-272.md` (เนื้อใบเต็ม 8639 B ย้ายคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:15+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1 ก้อน 2/2)
ATTENDED: see `tickets/GT-272.md` (บล็อกเดิมเก็บไว้ในไฟล์นั้น คำต่อคำ)

## GT-276 LEARN-SKILL-RESULT-WALKLOCK-ISOLATE-001  -- archived 20260908 (PASS R323C 2026-09-07T21:33+07:00, trailing u8=1 locks walking; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260908_closed.md`)

---
## GT-277 LV-SET-CHARACTER-LEVEL-RELOG-001  [✅ **PASS สองชั้น** (ตั้งเลข+วางเนื้อ+พับ+archive ในรอบเดียวโดย LANE-K รอบ `n3s0rg` 2026-09-06T14:10+07:00 ตาม `COO-DECISION 20260906_1346` ข้อ 3(ก) · ผลคำต่อคำจาก R321 §3 · เจ้าของใบ = LANE-GM) -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)]

---

- ~~GT-274 PRODUCTION-ATTACK-POSE-BY-CLASS-CONFIRMED-001~~ -> archive/GAME_TEST_QUEUE_ARCHIVE_20260908_closed.md (PASS both layers R322B/R322C · 2026-09-08, archived by LANE-K round `8c7cfo`)

---

## GT-279 GM-PANEL-BUTTON-CAPTURE-001 [🟡 **HELD-ON-BUILD (attended) — รอโทเคน `HEADLESS_PROOF:` วัดใหม่บน main** · เนื้อใบเต็ม (steps/pass criteria/ผลสองชั้น R322B/arrival ledger) ย้ายไป `tickets/GT-…] · body: `tickets/GT-279.md` (หัวใบเดิม 1591 B + 8 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-GM · body: `tickets/GT-279.md` (เนื้อใบเต็ม · ย้ายออกจากคิวเพราะเกิน 8,192 B ต่อใบ)

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

## GT-287 DEATH-OUTLIVES-THE-CONNECTION-001 [PENDING] · body: `tickets/GT-287.md` (หัวใบเดิม 886 B + 18 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: chief (LANE-E)
ATTENDED: บูตตาม `ATTENDED_SESSION_RUNBOOK.md` บนสำเนา `state\run_gtK.sqlite3` (ห้ามเปิด canonical เทียบ sha ก่อน/หลัง) เซิร์ฟก่อนไคลเอนต์ทีหลัง เก็บคอนโซล `2>&1` -> ล็อกอินตัวละคร A เข้า Port Royal (ฉาก 1 `bg0001`) ถ่ายภาพ #1 -> คลิกตีหุ่น Training Iron Man หนึ่งตัวจนตาย (~223 ครั้ง 891 dmg ต่อครั้ง 198125 HP) ถ่ายภาพ #2 -> logout ด้วยปุ่ม X + ยืนยัน -> ล็อกอินตัวเดิมกลับเข้ามา ถ่ายภาพ #3 คลิกตัวที่ฆ่าถ่ายภาพ #4 -> logout อีกครั้ง ล็อกอินตัวละครที่สอง ถ่ายภาพ #5
ATTENDED: ชั้น wire/DB ดูสามโทเคนตามลำดับ `MOB_DEATH_WORLD_SEEDED ... admitted=0 ... identities=none` (ล็อกอิน **แรก** ของบูตเท่านั้น) -> `MOB_DEATH_WORLD_REMEMBERED ... identity=0x20XX ... max_hp=198125` (ตอนฆ่า จด identity) -> `MOB_DEATH_WORLD_SEEDED ... admitted=1 buried=1 skipped=0 identities=0x20XX ledger_zeroed=1` (หลังล็อกอินกลับ และอีกครั้งหลังตัวละครที่สอง) · ชั้นจอดูภาพ #3/#5 เทียบ #1 จากมุมเดียวกัน: หุ่นตัวที่ฆ่ายังไม่ยืนเต็มหลอด
ATTENDED: PASS ต้องได้ทั้งสองชั้น ห้ามใช้ชั้นหนึ่งแทนอีกชั้น · FAIL คือ มีโทเคนที่ 1 และ 2 แต่ **ไม่มี** โทเคนที่ 3 **และ** บนจอหุ่นตัวเดิมยืนเต็มหลอดตีแล้วขึ้นเลขดาเมจสด · ไม่มีโทเคนที่ 1 เลย = NO-RESULT บูตใหม่ · ตีไม่ครบจนตาย = NO-RESULT · เจอ `MOB_RESPAWN` หรือเผลอข้ามฉาก = ปนเปื้อน NO-RESULT ทั้งหมดนี้ไม่ใช่ FAIL
ATTENDED: บูตปกติ ไม่มีแฟล็ก `--*-scenario` ไม่มี env พิเศษ ไม่มี chat trigger (ห้ามพิมพ์อะไรเลยทั้งรอบ ตัวอักษรตอนช่องแชทไม่โฟกัสกลายเป็นฮอตคีย์) · ทรีต้องมีบรรทัด `mob_death_persistence.seed_the_session_state(...)` ใน `runtime.py::_sync_combat_scene_state` บน main · 🔴 ห้าม End task ไคลเอนต์ ห้ามรีสตาร์ตเซิร์ฟเวอร์ระหว่างฆ่ากับล็อกอินกลับ (โปรเซสใหม่ = โลกใหม่ สมุดหลุมศพหายหมด) ห้าม `/warp` ห้ามข้ามแมพ · teardown ต้องรันเสมอแม้เลิกเล่นกลางคัน จด boot stamp ตั้งแต่ต้น (เทมเพลตปฏิเสธ stamp เก่ากว่า 420 นาที)
ATTENDED: จดลงผล — identity ที่ฆ่า (`0x2068`/`0x206A`/`0x206C`/`0x206E`) · จำนวนครั้งที่ตีจริง · เวลาห่างระหว่างตายกับล็อกอินกลับ · ตัวละคร/บัญชีที่ใช้ใน ARM B (ถ้ามีตัวเดียว ARM B = NO-RESULT) · sha canonical ก่อน/หลัง · `sessions` และ `max(lease_generation)` ก่อน/หลัง · **สีป้ายชื่อทุกป้ายในทุกภาพจากภาพเต็มความละเอียด หนึ่งบรรทัดต่อหนึ่งป้าย เขียน `none` ถ้าไม่มี ห้ามอ่านจากภาพย่อ/วิดีโอ ห้ามอนุมานสาเหตุจากสี** · เช็ค NO-CRASH ด้วยคลิกขวาค้างลากเท่านั้น

## GT-288 NAME-COLOUR-SWEEP-DUMMY-ROW-001 [OPEN] · body: `tickets/GT-288.md` (หัวใบเดิม 4208 B + 33 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-B
ATTENDED:

## GT-291 CHARACTER-HP-BAR-RETURNS-AFTER-LEAVING-126-001 [OPEN] · body: `tickets/GT-291.md` (เนื้อใบเต็ม 19388 B ย้ายคำต่อคำ — LANE-K รอบ `vuuhfe` 2026-09-09T16:20+07:00 ตาม `COO-DECISION 20260909_1545` ข้อ 1)
ATTENDED: see `tickets/GT-291.md` (บล็อกเดิมเก็บไว้ในไฟล์นั้น คำต่อคำ)
## GT-299 LEARN-SKILL-REQUEST-TRIGGER-HUNT-001 [READY] · body: `tickets/GT-299.md` (หัวใบเดิม 2775 B + 19 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-CS · ผู้ทำ: ka1-A (attended)
HEADLESS_PROOF: 2026-09-07 main 11f937a | cmd: python3 src/pirateforce_foundation/skill_learn_request_headless.py | LEARN_SKILL_REQUEST_ARMED_SUMMARY probes=3 decoded_no_reply=yes real_frame=refused no_db_write=yes RESULT=PASS
ATTENDED: บูตตาม `ATTENDED_SESSION_RUNBOOK.md` บน DB **สำเนา run-copy** เท่านั้น (ห้ามเปิด canonical · เทียบ sha ก่อน/หลัง) เซิร์ฟก่อนไคลเอนต์ทีหลัง เก็บคอนโซล `2>&1` -> ล็อกอินปกติเข้าเมือง (ฉาก 1) ไม่ต้อง GM ไม่ต้อง warp -> เปิดหน้าต่างสกิลด้วยฮอตคีย์ `K` (คลิกช่องแชทแล้วกด Esc ยืนยันว่าแชท**ไม่**โฟกัสก่อน ไม่งั้นตัวอักษรกลายเป็นฮอตคีย์)
ATTENDED: ทำทีละท่า **หยุด 3 วินาทีระหว่างท่า** และจดชื่อท่ากับเวลานาฬิกาก่อนทำทุกครั้ง (ไม่มีบรรทัดเวลา = อ่านคอนโซลย้อนไม่ออก = ใบเสีย): (1) เปิด/ปิดหน้าต่างสกิล 3 ครั้ง (2) สลับทุกแท็บทีละแท็บ ไล่ซ้ายไปขวา (3) คลิกซ้ายรายการสกิลทีละรายการในแท็บ "พิเศษ" (4) **ดับเบิลคลิก**รายการในแท็บ "พิเศษ" (5) คลิกขวารายการในแท็บ "พิเศษ" (6) ลากรายการลงฮอตบาร์ แล้วลากออก (7) ถ้ามีปุ่ม/เครื่องหมาย `+` หรือปุ่มเรียนสกิลใด ๆ กดมัน (8) กดสกิลจากฮอตบาร์ 1 ครั้ง · ท่า (4)(5)(7) คือสามท่าที่ ka1-A **ไม่ได้**ลองในรอบ R312
ATTENDED: ค่าที่ต้องอ่าน/จด (ชั้น wire): บรรทัด stderr `DISPATCH_NESTED_VITALS vital_count=<N> first_nested_id=0x36AA` = **ตัวจับ** ว่าเฟรมออกจริง — จด `<N>` เป๊ะทุกครั้ง (R312 เคยได้ `2`) และจดว่ามาหลังท่าหมายเลขไหน กี่วินาทีหลังจากท่านั้น · ถัดมาอีกบรรทัดต้องมี `learn_skill_request_hypothesis_..._no_reply` — จด**ชื่อเต็ม**: `_decoded_no_reply` (envelope ที่เลนนี้รับ) หรือ `_wrong_envelope_no_reply` (เฟรมมีหลายไวทัลเหมือน R312) · ชั้นจอแยกต่างหาก: ท่านั้นทำให้หน้าจอเปลี่ยนอะไรไหม (ไอคอน/ตัวเลข/ข้อความ) ประโยคเดียวต่อท่า **ห้ามใช้คอนโซลตอบแทนตา และห้ามใช้ตาตอบแทนคอนโซล**
ATTENDED: ตัดสิน: มีบรรทัด `first_nested_id=0x36AA` อย่างน้อยหนึ่งครั้ง **และ**รู้ว่ามาหลังท่าไหน = **PASS** (นี่คือคำตอบทั้งใบ) · ออกแต่ไม่รู้ว่าท่าไหนเพราะไม่ได้จดเวลา = **PARTIAL** · ทำครบแปดท่าแล้ว **ไม่มีบรรทัดนี้เลยทั้งเซสชัน = ผลลบที่มีค่า บันทึกเป็นผล ไม่ใช่ FAIL** (แปลว่าแปดท่านี้ไม่ใช่ตัวสั่ง ซึ่งเป็นข้อมูลที่ยังไม่มีใครมี) · เห็น `_wrong_envelope_no_reply` = **ไม่ใช่ FAIL** เป็นค่าที่ใบต้องการ (ยืนยันว่าไคลเอนต์จริงห่อหลายไวทัลเสมอ) · traceback ก่อนมีไบต์ออกสาย = NO-RESULT ส่งคืน · ห้ามเปลี่ยนแฟล็ก/ท่าเองเพื่อให้ "ผ่าน" ห้ามชี้สาเหตุ
ATTENDED: บูตด้วยแฟล็กเดียว `--learn-skill-request-hypothesis-scenario scenarios/learn_skill_request_hypothesis_decode_probe.json` **คู่กับ `--db <สำเนา>` เสมอ** (แฟล็กนี้ปฏิเสธการบูตถ้าไม่ระบุ DB) · ห้ามพ่วงแฟล็ก `--*-scenario` ตัวอื่นแม้แต่ตัวเดียว โดยเฉพาะ **ห้ามพ่วง `GT-276`/`learn-skill-result`** (ชุดนั้นทำให้ไคลเอนต์เดินไม่ได้ = ท่าที่ 1-8 ทำไม่ครบ) · ทรีต้องมี `src/pirateforce_foundation/learn_skill_request_hypothesis.py` และรันโทเคน `HEADLESS_PROOF` ให้ตรงก่อนบูต ไม่ตรง = ตัดใบตามกฎ `0159` · teardown ตาม runbook เสมอ

## GT-300 GT-178-BUILD-TICKET-REGISTER-AND-TICK-EVERY-SCENE-WITH-A-ROSTER  [🅿️ **RESERVED — เลขจองแล้ว รอเนื้อใบจากเจ้าของ** · **เจ้าของใบ = LANE-B (COMBAT)** ตาม `COO-DECISION 20260907_1441` ข้อ 1 (ตามคำสั่งเจ้าของ `PANYA-ORDER 20260907_1349`) · ตั้งเลขโดย LANE-K รอบ `dccuar` 2026-09-07T15:24+07:00 = **รอบแรกที่ K เห็นคำสั่ง** · 🔴 **ยังไม่มีเนื้อใบ**: กติกาเสมียนข้อ 3 บังคับว่าเนื้อใบต้องมาจากเจ้าของคำต่อคำ (`*-TO-K-gt-body-*`) และ COO เขียนไว้เองว่า "เนื้อใบมาจากสายเจ้าของ ... คุณไม่ต้องเขียนเนื้อเอง" ⇒ K จองเลขไว้เพื่อกันเลขชนและกันงานหายซ้ำรอบสอง แต่ **ไม่เขียนเนื้อใบแทน LANE-B** · ขอบเขตที่ COO เคาะไว้ (คำต่อคำจากใบ `1441` ถึง LANE-B ไม่ใช่คำของ K): (1) ทุกฉากที่มี hostile roster ⇒ ต้องมี `MobAiRegister` ของฉากนั้น **และ tick เดิน** โทเคน headless `MOB_AI_TICK_LIVE scene=14 mobs=11` และฉาก 2 หลังใบ `1313` · (2) มอนตีถึงผู้เล่นจริง (`intent=attack_undeliverable` → deliver · HP ผู้เล่นลดบนสายและบนจอ) · (3) เกตของ 3 ก.ย. (tick เฉพาะ register ที่ตรงฉาก) **ไม่ถอด** · ที่มาของผลลบ: `GT-178` `NEGATIVE-MEASURED R322C` 2026-09-07T01:48+07:00 · **ใบนี้คือใบสร้าง ไม่ใช่ใบเทส** — `GT-178` รอบ 2 เปิดเมื่อ (1)+(2) ขึ้น main พร้อม `HEADLESS_PROOF:` · แถวนี้ปิดหมวด "ผลลบที่ยังไม่มีเจ้าของใบสร้าง" ใน `QUEUE_STATUS_SNAPSHOT.md` แถวที่ 1]

## GT-301 BOAT-HEALTH-BUILD-TICKET-LEAVING-126-RESTORES-CHARACTER-HP [READY] · body: `tickets/GT-301.md` (หัวใบเดิม 2151 B + 34 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-DB (เจ้าของเดี่ยวตาม `COO-DECISION 20260907_1441` ข้อ 1) · ผู้ทำ: ka1-A (attended) · ผู้บริโภคผล: LANE-DB

## GT-304 M2-ISLAND-GUARD-VERDICT-ON-THE-CONSOLE-001 [READY] · body: `tickets/GT-304.md` (หัวใบเดิม 2286 B + 50 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-A (WORLD) · ผู้ทำ: ka1-A (attended) · ผู้บริโภคผล: LANE-A

## GT-306 NAME-COLOUR-P2-BODY-DIFF-SET3-REDESIGN-001  [SUPERSEDED-BY: GT-288 set 3 (PANYA 20260907_2325) -- withdrawn as a separate ticket by LANE-K round `0109` 2026-09-08T01:16+07:00, do not boot; work moved to GT-288 set 3] -- archived 20260909 (SUPERSEDED; verbatim already in `tickets/GT-306.md`, LANE-K round `ajt28l`)
## GT-307 SKILL-LIST-AT-LOGIN-TRAILING-ZERO-001 [READY] · body: `tickets/GT-307.md` (หัวใบเดิม 5688 B + 7 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-CS · body: `tickets/GT-307.md` (เนื้อใบเต็ม · ย้ายออกจากคิวเพราะเกิน 8,192 B ต่อใบ)

## GT-308 UIB-EXIT-GAME-REALLY-ENDS-THE-SESSION-001 [PENDING] · body: `tickets/GT-308.md` (หัวใบเดิม 6382 B + 13 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-UI · body: `tickets/GT-308.md` (เนื้อใบเต็ม · ย้ายออกจากคิวเพราะเกิน 8,192 B ต่อใบ)
HEADLESS_PROOF: UI_LOGOUT_EXIT_GAME_ARMED subcode=1 ack=1 lease_closed=1 close_scheduled_ms=250 closer_called=1 relogin_after=ok RESULT=PASS

## GT-309 M2-CAPTAIN-REPORT-MARKER-CONFIRM-WARP-001 [🟡 **HELD-ON-BUILD: จุดเสียบ `runtime.py` สองจุด (ส่ง prompt · รับ echo `0x4477` แล้วตอบ transport) + PR ของรอบ `w4cp5c`** · เนื้อใบจาก `notes_to_chief/20260908_…] · body: `tickets/GT-309.md` (หัวใบเดิม 10946 B + 7 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-A · body: `tickets/GT-309.md` (เนื้อใบเต็ม · ย้ายออกจากคิวเพราะเกิน 8,192 B ต่อใบ)

## GT-313 GM-WARP-STAGED-SAYS-ON-SCREEN-AND-RELOG-LANDS-001 [READY] · body: `tickets/GT-313.md` (หัวใบเดิม 1773 B + 7 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-GM · body: `tickets/GT-313.md` (เนื้อใบเต็ม · ย้ายออกจากคิวเพราะเกิน 8,192 B ต่อใบ)

## GT-315 GM-SKILL-SANDBOX-ALL-CLASSES-NO-LEVEL-GATE-PLUS-STARTING-WEAPONS-001 [🟡 **HELD-ON-BUILD** — ออกเลขตาม `COO-DECISION 20260908_1541_COO-DECISION-one-ticket-covers-the-whole-gm-skill-sandbox-LANE-K.md` (`PANYA-ORDER 1455`) · **ใบยาว …] · body: `tickets/GT-315.md` (หัวใบเดิม 921 B + 7 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: COO (เนื้อใบ) / LANE-GM+LANE-CS+LANE-DB (สร้าง) · body: `tickets/GT-315.md` (เนื้อใบเต็ม · ย้ายออกจากคิวเพราะเกิน 8,192 B ต่อใบ)

## GT-317 BASIC-FACTION-EVERY-LOGIN-SCENE-SEA-126-001 [🟡 **ตกรถ: ไม่มี HEADLESS_PROOF (บน main)** — เนื้อใบจาก `notes_to_chief/20260906_1515_LANE-A-TO-K-gt-body-basic-faction-every-login-scene.md` (LANE-A รอบ `q02br…] · body: `tickets/GT-317.md` (หัวใบเดิม 1169 B + 7 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-A · body: `tickets/GT-317.md` (เนื้อใบเต็ม · ย้ายออกจากคิวตั้งแต่วางเพื่อกันเกิน 8,192 B ต่อใบ)

## GT-318 UI-PARTY-INVITE-BUTTON-FIRST-SERVER-ANSWER-001 [HOLD] · body: `tickets/GT-318.md` (หัวใบเดิม 2131 B + 7 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-UI · body: `tickets/GT-318.md` (เนื้อใบเต็ม · ย้ายออกจากคิวตั้งแต่วางเพื่อกันเกิน 8,192 B ต่อใบ)

## GT-319 CENSUS-CHARACTERS-CLASS-ID-WEAPON-READ-ONLY-001 [🟡 **ตกรถ: ไม่มี HEADLESS_PROOF (บน main)** — เนื้อใบจาก `notes_to_chief/20260908_1153_LANE-DB-TO-K-gt-body-census-class-weapon-read-only.md` (LANE-DB รอบ `21lxm…] · body: `tickets/GT-319.md` (หัวใบเดิม 1327 B + 7 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-DB · body: `tickets/GT-319.md` (เนื้อใบเต็ม · ย้ายออกจากคิวตั้งแต่วางเพื่อกันเกิน 8,192 B ต่อใบ)

## GT-320 GM-WARP-NAME-REFUSAL-PRINTS-THE-SCENES-IT-FOUND-001 [BLOCKED] · body: `tickets/GT-320.md` (หัวใบเดิม 1176 B + 5 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-GM · body: `tickets/GT-320.md` (เนื้อใบเต็ม · ย้ายออกจากคิวตั้งแต่วางเพื่อกันเกิน 8,192 B ต่อใบ)

## GT-322 M2-SEA-CAST-ON-ARRIVAL-001 [READY] · body: `tickets/GT-322.md` (หัวใบเดิม 2498 B + 5 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: chief (LANE-E) · body: `tickets/GT-322.md` (เนื้อใบเต็ม · ย้ายออกจากคิวตั้งแต่วางเพื่อกันเกิน 8,192 B ต่อใบ)

## GT-323 GM-WARP-CLIENT-NEVER-FOLLOWS-NO-TWO-OWNER-ROW-001 [🟡 **HELD-ON-BUILD: กลไกยังไม่อยู่บน main** — เนื้อใบจาก `notes_to_chief/20260908_2144_FROM_CHIEF-TO-K-gt-body-warp-the-client-never-follows.md` (chief (LANE-E) …] · body: `tickets/GT-323.md` (หัวใบเดิม 1884 B + 5 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: chief (LANE-E) · body: `tickets/GT-323.md` (เนื้อใบเต็ม · ย้ายออกจากคิวตั้งแต่วางเพื่อกันเกิน 8,192 B ต่อใบ)

## GT-324 LEARN-SKILL-RESULT-FRAME-AND-FIFTH-ROW-001 [HOLD] · body: `tickets/GT-324.md` (หัวใบเดิม 849 B + 6 บรรทัด stub ย้ายไปท้ายไฟล์นั้นคำต่อคำ — COO แทน LANE-K (ใบ `1705`) 2026-09-09T17:55+07:00 · `1545` ข้อ 2)
owner: LANE-CS (หยุดตามใบ `1640` — Codex รับช่วง) · ตั้งเลข/วางคิว = COO แทน LANE-K (ใบ `1705`) · body: `tickets/GT-324.md` (เนื้อใบเต็มคำต่อคำ · ย้ายออกจากคิวตั้งแต่วางเพื่อกันเกิน 8,192 B ต่อใบ)
ATTENDED: see `tickets/GT-324.md` (บล็อก `## ATTENDED:` ของเจ้าของใบอยู่ในไฟล์นั้น คำต่อคำ · `HEADLESS_PROOF:` ในนั้นวัดบนกิ่ง ไม่ใช่ main — ยังใช้ขึ้นรถไม่ได้)
