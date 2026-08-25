# GAME TEST QUEUE — คิวเทสในเกม

> 🔤 **กฎชื่อใบ (คำสั่ง Panya 2026-08-24 ~00:2x · จดหมาย `20260824_0025_*`):** ใบในไฟล์นี้ใช้ prefix **`GT-`** (เทสเกม — เปิดเกม · จับ `LOCK_GAME` · ใช้ตาคน) · **ตัวนับเลขเป็นชุดเดียวร่วมกับ `CLIENT_RE_QUEUE.md`** (ใบ static ที่นั่นใช้ prefix **`RE-`** ตั้งแต่ใบ **056** เป็นต้นไป) — เห็น `RE-0xx` ที่ไหนแปลว่าเป็นใบ static ให้ข้ามไปดูไฟล์นั้น · ใบเก่า (รวม `GT-050`/`052`/`053`/`054`/`055` ที่เป็น static แต่ชื่อ GT-) **คงชื่อเดิมตลอดกาล**

> 🔴 **G-OBS — ขั้นบังคับข้อสุดท้ายของ **ทุกใบที่มีชั้น client-observable** (คำสั่ง Panya 2026-08-25 ~19:35 +07:00 · **ขยายครอบรอบ unattended โดยเจ้าของเอง ~21:10 +07:00** · เขียนลง `AGENTS.md` §6 แล้วโดย R168 และ R170):**
> **ก่อนเขียนผล ต้องทวนสิ่งที่ผู้ช่วยเห็นให้ผู้เทส (มนุษย์) ยืนยันก่อน** แล้วบันทึกเวลาที่ยืนยันลงในจดหมายผลเป็นบรรทัด
> `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` · **จดหมายผลที่ไม่มีบรรทัดนี้ chief จะไม่บริโภคเป็นผลปิดใบ**
> (เก็บหลักฐานระหว่างรอได้เต็มที่ — ที่ถูกกลั้นคือ *ข้อสรุป*: จดหมายผล · สถานะใบ · nonclaim · การประกาศว่าอะไร "ไม่เกิดขึ้น")
>
> 🔴 **รอบ unattended ไม่ยกเว้นอีกต่อไป** — ไม่มีตาคนตอนรัน **แต่มีวิดีโอให้เจ้าของดูย้อนหลัง** ⇒ จังหวะที่ 3 แค่เลื่อนเวลาออกไป ไม่ได้หายไป
> (ท่านี้เคยใช้ปิด `GT-059` มาแล้วจริง · จดหมาย `20260824_2133 PANYA-VISUAL-SIGNOFF-GT059`)
> 🆕 **สถานะกลาง `AWAITING-OBSERVER`** = รันครบ หลักฐานครบ **ขาดลายเซ็นตาคนอย่างเดียว** ⇒ ใช้สถานะนี้แทน `PENDING` เพื่อให้คอขวดมองเห็นได้
> 🔴 `AWAITING-OBSERVER` **ไม่ใช่ PASS ไม่ใช่ FAIL** — ห้ามยกผลของใบสถานะนี้ไปเป็นฐานของใบอื่น

## 📇 สารบัญใบที่ยังไม่ปิด (คำสั่ง Panya 18:22 · อัปเดตทุกครั้งที่เปิด/ปิดใบ · เป็นดัชนีชี้ลงข้างล่าง — เนื้อใบไม่ถูกย้าย)

- 🆕 **`GT-079` SCENE-278-ENTRY-AND-STAGE-EYECHECK-001** (🔴 **BLOCKED — BLOCKED-ON-WIRING** · ยังไม่มีเส้นทาง runtime ที่พาผู้เล่นเข้าฉาก 278 · เปิดใบโดย LANE-A ตาม `CHARTER-02` BUILD-002 สไลซ์ 1 (v2 / M2 · กำหนด 26 ส.ค. 23:59) · ถามด้วยตาหกข้อ: เข้าได้ไหม **และ HUD บอกว่าแมพอะไร** (ตัวแยกการอ่านค่า `scene_id` สี่แบบ) · มีพื้นไหม · กว้าง-เรียบ-โล่งไหมและสีอะไร · `BgNull` เสียหายไหม · เก้า placement โผล่ไหม · เดินได้และอยู่ครบ 10 นาทีไหม · 🔴 **มีขั้นตอนบังคับ "ทางกลับบ้าน"** เพราะฉาก 278 มี `n_MARKER=0`/`n_SAVE=0` · **ไม่ใช่ใบเรื่องการ *ย้าย* ฉากขณะ live — นั่นคือ `RE-077`** · ใบเต็มอยู่ท้ายไฟล์)
- 🆕 **`GT-074` OCCLUSION-CAMERA-ANGLE-CONTROL-001** (🟢 **PENDING — attended · รันได้บน `main` ปัจจุบันเลย ไม่รอ merge ไม่รอ CI** · **ศูนย์สล็อต · ~3 นาทีบนจอ** · เปิดโดย chief R170 · เก็บตกตัวคุมเดียวที่ `GT-072` รอบแรกไม่ได้ทำ: **หมุนกล้องอย่างเดียว ไม่เดิน ไม่คลิก** ในช่วง `+10..+29` เพื่อตัดทางหนีสุดท้ายของ "บังทับ" · 🔴 **ต้องรันก่อน `GT-032`** ด้วยเหตุผลเดียวกับ `GT-072` · ใบเต็มอยู่ท้ายไฟล์)
- **`GT-072` ACTOR-SLOT-DISPLACEMENT-001** (🟡 **PARTIAL — ใบยังเปิด · ผลรอบแรกบันทึกโดย chief R170** · จ็อบ 1167/1168/1169 · 🔴 **ยังไม่มีค่าไหนถูกตัดออกเลย** — ตัวคุมทั้งสองที่เก็บมาถูกวัดที่ `+92.8` วิ **หลังทั้ง NPC และ actor ของเราหายจากจอไปแล้ว** ⇒ อำนาจแยกแยะเป็นศูนย์ · ตัวคุมที่ไม่ได้ทำ: `W2` มุมกล้อง · `W3` เข้าไปใกล้+คลิกในหน้าต่าง · `POST-A` ⇒ ยกไปใบ **`GT-074`** · เปิดโดย chief R168 จากผลข้างเคียงข้อ ④ ของ `GT-030-R3`: `SPAWN_BARE` ทับพิกัด `P0` แล้ว NPC `Navy Transfer` หายใน 0.6 วิ — **แยกไม่ออกระหว่าง despawn / แทนที่ / บังทับ** · ตัวคุมเชิงลบสามตัวฟรีในเลน · 🔴 **ต้องรันก่อน `GT-032`** เพราะ `GT-032` ทำให้ landmark `0x2001` ขึ้นศัตรู · ใบเต็มอยู่ท้ายไฟล์)

**🎮 ต้องเปิดเกม / ต้องใช้ตา Panya** — 🟢 **ปลดพักแล้ว (Panya 2026-08-24 ~21:1x +07:00 · จดหมาย 2120 §① · บันทึกโดย R155 — คำสั่งพัก 16:56 ของ 23 ส.ค. สิ้นสุด) · 🔴 ห้ามปิดด้วยรอบ unattended ยังบังคับเหมือนเดิม** (กติกาอยู่ใน `AGENTS.md` แล้ว)
- `GT-001` smoke recurring (🟢 pending · re-arm ค้าง) · `GT-030` (~~ห้ามรันรอบสาม~~ **ยกเลิกโดยเจ้าของ 18:15 +07:00** ⇒ ดู `GT-030-R3`) · `GT-030-R3` REMOTE-PLAYER-VIS-PROVENANCE-001 (✅ **PASS — ปิดโดย chief R168 · `OBSERVER_CONFIRMED: 2026-08-25T19:40+07:00`** · 🎯 ไคลเอนต์เรนเดอร์ `actor_type 2` ได้เป็นครั้งแรกในประวัติโปรเจกต์ · target panel เปิดแต่ **ช่องชื่อว่าง** (`HP. 0`/`LV. 1`) ⇒ ~~**ไคลเอนต์ไม่บริโภค `BasicAttr` name สำหรับ actor_type 2**~~ 🔴 **ถอนแล้วโดย chief R169** (รอบสี่พบว่า NPC `actor_type 4` ก็ช่องชื่อว่างเหมือนกัน ⇒ เป็นคุณสมบัติของ **แผงในบิลด์นี้** ไม่ใช่ของคลาส actor — ดูบล็อกถอนในใบ) · 🟢 **รอบสี่ (chief R169 · จ็อบ 1161/1162/1163) ปลดข้อผูกพันสองข้อ: ทำซ้ำครบสองรอบแล้ว + ผลลบ 45 วิแรกคุมกล้องได้จริงแล้ว** · 🔴 ที่ยังเหลือ: **ตัวคุม `ProbeControl03` ที่ `-9,290` ยังยืนยันจากวิดีโอไม่ได้สองรอบติด** (ผู้เทสเดินไปทาง `+X` ทั้งสองรอบ) + จูนนาฬิกาด้วย clapper · ผลข้างเคียงแตกเป็น `RE-071` และ `GT-072` แล้ว · ~~ถ้อยคำเดิมของใบ~~ 🟢 **READY — attended · คุณ Panya ขับเอง** · **ศูนย์สล็อต** ไม่แก้โค้ด/mask/ไบต์ (`HYP-PF-025` 2/5 คงเดิม) · ตอบสองข้อที่รอบ #12 และ rerun ตอบไม่ได้: **ชายหนุ่มชุดน้ำเงิน-ขาวที่ X ≈ `-8681` เป็นของแมพหรือของเรา** และ **transient สั้นกว่า 3.487 วิ** · 🔴 **ตัวยิงคือแชต ASCII 12 ตัว ⇒ ห้ามพิมพ์ clapper ตอนต้นรอบ** ลำดับคือ เดินสำรวจ → baseline → *แล้วค่อย* พิมพ์ `PFCHATPROBE1` · 🔴 รันให้จบก่อน `GT-032` เสมอ · ใบ `GT-030` เดิมอยู่ที่เดิมทั้งใบ ห้ามลบ) · `GT-033` ✅ **ANSWERED — ปิดโดย chief R166 (2026-08-25 ~17:5x +07:00)** · สามช่องจากสี่วัดครบในคืนเดียว **ผลลบทั้งสาม** ⇒ ไม่ใช่ response policy ตัวไหนในสองตัวที่เรามี 🔴 **ไม่ใช่ "connection-teardown ถูกหักล้าง"** (ไม่มีใครพิสูจน์ว่าไคลเอนต์เห็นการปิด socket) · 🔴 **`BLOCKED-INPUT` ตายแล้ว** (เป็นข้อจำกัดของเครื่องมือคลิกสังเคราะห์ ไม่ใช่ของไคลเอนต์ — มือคนกดผ่านสามรอบติด) ⇒ ทางต่อเป็น **static** ดู `RE-070` ใน `CLIENT_RE_QUEUE.md`
- `GT-034` (NO-RESULT ×2 — รอบสอง 2026-08-24 02:28: computer-use `list_apps` timeout ×3 หยุดก่อน input แรก · scenario ยังไม่ถูกยิง (`StartGameReq=0`) · ผู้เทสเสนอรอ **Panya เทสด้วยตา 2026-08-26** · tooling blocker "ffmpeg console ทับจอ" แก้แล้ว — ดู R143) · `GT-035` (✅ **PASS 2026-08-25 15:04-15:36 (+07:00) · สองรอบ สองผู้สังเกต · ปิดโดย chief R164** — หลอด HP ของ `0x201F` ลงครบบันได `3857 -> 2893 -> 2893 -> 771` · **ห้ามอ้างกับ GT-036** · "hostile" ยังไม่ถูกพิสูจน์ ป้ายชื่อเขียว ⇒ `RE-067`) / `GT-036` (🔴 **คง BLOCKED — เหตุผลเปลี่ยนโดย R164:** ไม่ใช่ "รอ GT-035" อีกแล้ว แต่ **ไม่มีเลนที่มีครึ่งตาย** (`HP_FLOOR` = FORBIDDEN ใน `HYP-PF-038`) ⇒ ต้องมีเวอร์ชันถัดไปของเลนก่อน **และรอคุณ Panya เคาะ**) · `GT-045` v2 (🟢 merge แล้ว — ก่อนบูตต้องผ่าน (ข) เช็ค resolver/BOOT_COMMIT ว่า clone ที่บูตมีเลน v2 จริง · ✅ (ค) ปลดแล้ว — Panya ปลดพักเลน attended 2026-08-24 ~21:1x จดหมาย 2120 §① (R155) · ถ้อยคำเดิม "พร้อมบูตทันที" ตัดเงื่อนไข (ข) ทิ้ง — แก้โดย R142 ให้ตรงจดหมาย R141)
- 🆕 `GT-058` LEARN-SKILL-RESULT client-observe (✅ **CLOSED — BOUNDED-NEGATIVE โดย R155** ตามคำตัดสิน Panya 2026-08-24 ~21:1x +07:00 จดหมาย 2120 §③ "ปิดเลย" · ขอบเขต: เทียบเนื้อในหน้าต่างสกิลไม่ได้เพราะ baseline เปิด K ไม่ได้ — อาการนั้นย้ายไปเป็นคำถามของ GT-059 · ดูหัวใบ)
- 🆕 `GT-059` SKILL-ATTR-WINDOW-GATE-001 (✅ **CLOSED — P2 (FALSIFIED) โดย R155** · ตัวปิด = ตา Panya บนวิดีโอต่อเนื่องสองไฟล์ FULLROUND (จดหมาย 2133 · 2026-08-24 ~21:33 +07:00): wire byte-exact PASS ×3 triggers แต่หน้าต่างสกิลไม่ขึ้นเลยทั้งสอง session · control C เปิดได้ = เกมไม่ค้าง ⇒ "รับ `CSkillAttr` แล้วหน้าต่างเปิดได้" ถูกหักล้าง · 🔴 nonclaims: A/B (กด K ในช่อง 3 วิ) ยัง UNRESOLVED → เปิดใบต่อ `GT-064` · สาเหตุ (slot-null vs check อื่น) ยังไม่รู้ — งานออกแบบตัววัด runtime ปลดล็อกแล้วตามเงื่อนไข 2120 §④ · ห้ามลบวิดีโอสองไฟล์บนสะพาน · ดูหัวใบ)
- 🆕 `GT-060` PICKUP-CLICK-CAPTURE-001 (🔴 BLOCKED-CONDITIONAL — ใบเปิดโดย R151 ท้ายไฟล์ · จับเฟรม `PickupTerrainThing` ตัวจริงตัวแรกจากคลิกซ้ายบน drop-object ที่วาดจริง — ตัดสิน id derive `0x4543` ถูก/ผิด · เงื่อนไข 3 ข้อ: ✅ (ก) ปิดแล้ว R152 — PR #22 merge เข้า `main` `2c0e3ba` (head `a64d589` เขียว(Actions run 32717828631 · subset) · tree-identical กับ merge commit · re-verify สี่ข้อบน `main` ผ่านครบ) · (ข) มี drop-object วาดจริงคลิกได้ในบูตเดียวกัน — 🟡 ครึ่ง composition ปิดแล้ว: **คำเคาะ Panya มาแล้ว (2026-08-24 ~18:3x +07:00 · จดหมาย `notes_to_chief\20260824_1831_PANYA-RULINGS-combine-scenarios-and-open-GT-063.md` §①): allow-list คู่ `ground-loot + pickup-listener` ร่วมบูตเดียวกันได้** (22 เลนที่เหลือ exclusive เหมือนเดิม · วินัยบังคับ: ทุกข้อสังเกตต้องระบุเลนผู้ก่อ ไม่งั้น NO-RESULT) · โค้ด composed-boot ✅ **merge เข้า `main` แล้ว (R154): PR #23 → merge commit `cad3e28` · head `99bfa96` เขียว(Actions run 32726495224 · subset · ทาง ci-status sha ตรง) · tree-identical · สวีตเต็ม main 2222/324 เขียว(cloud sanity R154)** ⇒ (ข) เหลืออย่างเดียว: **GT-045 เทสตา PASS (นัด 2026-08-26)** · ✅ (ค) ปลดแล้ว — Panya ปลดพักเลน attended (จดหมาย 2120 §① · R155) · 🆕 R155: allow-list ขยายเป็นสามตัว (2120 §②) — ✅ R156: PR โค้ด #25 merge เข้า `main` แล้ว (`3f87fc3` · เขียว run 32743688024) ⇒ รวมบูตกับ GT-063 ได้แล้ว · P4 ไม่มีวัตถุ = NO-RESULT ห้ามอ่านเป็นผลลบ)
- 🆕 `GT-063` ITEMOPERATE-RES-GREENLINE-SHAPE-001 (🟡 **READY-CONDITIONAL (R155)** — ยิง `ItemOperateVitalRes` `0x4C13` สามทรงแล้วดูจอจริงว่าทรงไหนทำให้บรรทัดเขียว `ได้รับ [<ชื่อ>] * <จำนวน>` ขึ้น · (ก) ✅ ปิดแล้ว R155: **PR #24 merge เข้า `main`** — merge `960716c` · head `1435064f` เขียว(Actions run 32733905271 · subset · ci-status sha ตรง) · tree-identical · flag `--item-operate-res-hypothesis-scenario` + `scenarios/item_operate_res_greenline_sweep.json` · trigger = แชต 12 ตัวอักษร ASCII ใด ๆ (ตกลงใช้ `greenline001`) · label สามตัว `ITEMOP_RES_CTRL_CAPTURE_REPLAY / BAGUPD_ID2400901_QTY1 / BAGUPD_ID2400901_QTY5` (count=0 ทุกเฟรม · มิติ count>0: RE-064 ✅ ปิดแล้ว R156 — ทรง pin แล้ว แต่ยังไม่ compose รอผลตาใบนี้ + คำเคาะ Panya ตาม ledger) · (ข) ✅ ปลดแล้ว — Panya ปลดพัก attended (2120 §① · R155) ⇒ **บูตเดี่ยวได้แล้ว** · (ค) ✅ **ปิดครบ R156: PR #25 merge เข้า `main` แล้ว** — merge `3f87fc3` · head `fc4010e` เขียว(Actions run 32743688024 · subset · ci-status sha ตรง) ⇒ **บูตรวมสามเลนได้แล้ว** · 🆕 R156: rider RE-064 ตอบแล้ว — 15-byte PC prefix IDENTICAL 15/15 ⇒ ถ้า control frame โดน ErrorData ให้ชี้ session context ไม่ใช่ envelope prefix · attribution สามเลนบังคับ: แยกเลนผู้ก่อไม่ออก = NO-RESULT · ปิดใบได้เฉพาะเห็นข้อความบนจอที่อ่านออก — "ไม่ขึ้น" ทุกแบบ = NO-RESULT ห้ามเขียนว่า "ไม่มี/ไม่เกิด")
- 🆕 `GT-064` SKILL-ATTR-WINDOW-KPRESS-IN-GAP-001 (🟢 READY — ใบเปิดโดย R155 ท้ายไฟล์ · ปิดคำถาม A/B ที่ GT-059 ทิ้งไว้: กด K/คลิกปุ่มสกิล **ภายในช่อง 3.0 วิ** ระหว่าง `COUNT0` (57B) กับ `COUNT1` (68B) แล้วหน้าต่างสกิลเปิดไหม · มือคนกดทัน — computer-use ไม่ทัน (เหตุที่รอบ unattended พลาด S1) · เลนโค้ด = เลน GT-059 เดิมบน `main` ตั้งแต่ `543382c` ไม่มีโค้ดใหม่ · attended ปลดพักแล้ว (2120 §①) · เหลือเช็ค BOOT_COMMIT ตอนบูตอย่างเดียว · ผลลบปิดได้เฉพาะ Panya เห็นเอง + วิดีโอต่อเนื่อง · press นอกช่อง/ตัดสินไม่ได้ = NO-RESULT ต่อ attempt)
- 🆕 `GT-069` GROUNDLOOT-NAMELABEL-TEXTPROP-SELECTOR-001 (🔴 **BLOCKED ×2** — ใบเปิดโดย R165 ท้ายไฟล์ · ยิง **เฟรมคุม mask `0x12` (ไม่มี selector) กับเฟรมทดลอง mask `0x3A` (gate `+0x1B`=1 · index `+0x1A`=6) ที่พิกัดเดียวกัน dword เดียวกัน** แล้วดูว่าหน้าตาป้ายชื่อไอเทมต่างกันไหม — ตัวแปรเดียวคือ "สองฟิลด์ selector มี/ไม่มี" ⇒ **ทุกทางออกอ่านได้ รวมถึงผลลบที่สะอาด** · ที่มา `RE-067`: เลนที่ ship อยู่ส่ง mask `0x12` มาตลอด ⇒ ทุกป้ายที่เราเคยวาดใช้ default property `0x34` ⇒ **สีที่เคยจดไม่ใช่สีที่เราเลือก** · 🔴 **เงื่อนไข (1) คุณ Panya เคาะเรื่องงบเวอร์ชัน — ยังไม่เคาะ** (`HYP-PF-032` เต็ม 3/3 และ `expiry.decision` ของมัน **ไม่มี clause "เปิดใบใหม่ได้"** ต่างจาก `HYP-PF-029` ที่มี ⇒ บรรทัดฐาน `HYP-PF-038` เอื้อมไม่ถึง) · **โค้ดอยู่บน branch `claude/elegant-lamport-ywug3f` และจงใจไม่ merge** ⇒ ถ้ายังไม่เคาะ ใบนี้รอเจ้าของ ไม่ใช่รอผู้เทส ไม่ใช่รอ CI · 🔴 เงื่อนไข (2) ด่านก่อนบูตเจ็ดข้อ · 🔴 **`0x34`/`0x5D..0x62` เป็น UI *text property* ไม่ใช่ "สี" — ห้าม join กับ `FONT_COLOR.n_ID`**)

**🔬 งาน static — ทำเมื่อไรก็ได้ ไม่ต้องมีคนเฝ้า ไม่ต้องจับ `LOCK_GAME` · ขนานกับรอบเทสเกมได้:**
- ใบเก่าในไฟล์นี้: `GT-047` (🟠 จ็อบ 0 ปิดแล้ว 09:16 — source เข้ามือ chief · **R144 ส่ง patch การ์ด `field_offset` กลับแล้วที่ `patches/gt047/` (เขียว 8 ด่านบน cloud) · เหลือฝั่งสะพาน apply patch แล้ว rerun จ็อบ 1–3**) · `GT-049` (✅ **PASS/DONE — ผลหน้าสะพาน 2026-08-24 09:23 · บันทึก R144:** id 131 ยิงจาก **inbound** `ItemOperateVitalRes` handler `0x005EF5E0` → chat emitter `0x005CC309` — คนละเลนกับ `PickupTerrainThing` 0x1F/0x03/0x22 ของ GT-046 ⇒ **บรรทัดลูทสีเขียว = เซิร์ฟเวอร์ตัดสินการเก็บ** — ดีไซน์เลนลูทฝั่งเราต้องส่ง `ItemOperateVitalRes` เอง)
- 🆕 ใบใหม่ตั้งแต่ R128 อยู่ไฟล์ใหม่ **`CLIENT_RE_QUEUE.md`** (คำสั่ง 18:22 ข้อ ③): ✅ **ปิดแล้ว 3 ใบ (ผลหน้าสะพาน 2026-08-24 ~00:3x–00:4x +07:00 · บันทึก R135):** `GT-054` PASS (spans **392/392** ตรงอิมเมจ · mismatch 0) · `GT-053` PASS (**N=106 ≥ 61 ⇒ `0x203D` in-band ⇒ H1 รอด**) · `GT-052` PASS (crosswalk class/skill ครบ · ผลลบ: ไม่พบ legend ของ `n_TARGET` ในชุดที่ค้น — ห้ามตั้ง label) — 🟡 `GT-050` **PARTIAL** (00:55: จ็อบ 1–3 ปิด · `CLearnSkillResultVital` CLOSED · direction `TriggerCastSkillVital` ชนเพดาน static — ทางต่อ observe-only attended) — ✅ `GT-055` **PASS/DONE** (ผลหน้าสะพาน 2026-08-24 02:41 · บันทึก R143: `0x36DB` = **string8** tag `0x44` · `0xAC52` = UTF-16LE tag `0x48` ⇒ parser เราผิดจริงฝั่ง `0x36DB` — แก้แล้ว: PR โค้ด #16 รอ gate ยังไม่เข้า main ณ R143) — **ที่ยังเปิดจริงในไฟล์นั้น: 0 ใบ — `RE-062` ปิด DONE โดย R152** (คำตอบ (ค): inbound ไม่เขียน `[actor+0x3E8]` — กุญแจอ่านผลลบ GT-059 · `RE-056` ปิด DONE/METHOD-FAIL · `RE-057`/`RE-058` ปิดโดย R144 · `RE-059`/`RE-060`/`RE-061` ปิดโดย R149 — ดูหัว `CLIENT_RE_QUEUE.md`) · 🔴 **บรรทัดนี้ล้าสมัยตั้งแต่ R165 — แก้โดย R166:** ที่เปิดจริงในไฟล์นั้นตอนนี้คือ **2 ใบ** — 🟢 `RE-068` ACTOR-NAMEBOARD-VALUE-034-SEMANTICS-001 (เปิดโดย R165) · 🟢 🆕 `RE-070` ORCHESTRATOR-TRANSITION-GATE-001 (เปิดโดย R166 — ทางต่อของ `GT-033` ที่ปิดเป็น ANSWERED · เป้า: ใครเซ็ต MODE `[orch+0x28]` ของ vtable `0xf45030` และ `[orch+0x24]` เป็น gate หรือแค่ display) · 🔢 **เลข 069 ไม่ว่างเพราะ `GT-069` ใช้อยู่ — ตัวนับสองคิวเป็นชุดเดียวกัน**
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

## GT-001 Smoke: full-loop บน canonical DB หลังทุก commit สำคัญ  [🔴 **HOLD (recurring) — ห้ามหยิบจนกว่าเกณฑ์ `samePos` ของ `1166_*.ps1` จะถูกแก้** (chief R170 · เหตุผลใต้หัวใบ) · **PASS ล่าสุด: `f8562c1` (R168) 2026-08-25 20:43 (+07:00) — PASS พร้อม erratum** · *(PASS ก่อนหน้า: `fa1e804` 2026-08-24 09:41 · R145)*] 🔁

> ### 🔴🔴 HOLD — อ่านก่อนหยิบใบนี้ (chief R170 · `pf-adversary` จับได้)
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

## GT-033 LOGOUT-TRANSITION A/B: response ไหนทำให้ client เปลี่ยนหน้าจริง  [✅ **ANSWERED — ปิดโดย chief R166 · 2026-08-25 ~17:5x (+07:00)** · จ็อบ `1143-1146` (B/03) · `1147-1149` (A/03) · `1150-1152` (A/01) · attended คุณ Panya ขับ UI เอง · จดหมาย `20260825_1710` + `20260825_1730` + `20260825_1745` · **คำตอบของใบ: ไม่ใช่ response policy ตัวไหนในสองตัวที่เรามี** — ส่ง `0x709E` แล้วปิด socket **ไม่ทำให้เปลี่ยนหน้า** และ ack แล้วปิด socket เฉย ๆ ก็ **ไม่ทำ** ⇒ ทางต่อที่ chief เลือกคือ **mode/timer ของ orchestrator** (`RE-070`) 🔴 **แต่ห้ามอ่านว่า "connection-teardown ถูกหักล้างแล้ว"** — เราพิสูจน์ว่า *เราปิด socket แล้วไคลเอนต์ไม่เปลี่ยนหน้า* **ไม่ได้พิสูจน์ว่าไคลเอนต์เห็นการปิดนั้น** (ไม่มี positive control สักรอบเดียวทั้งโปรเจกต์) 🔴 **และตารางสามกิ่งของใบไม่ exhaustive** — ดูบล็อก **กิ่งที่ตารางไม่ครอบ** ใต้หัวใบ (หกกิ่ง · ส่วนใหญ่ยังวัดได้ในเกม) · 🔴 **`BLOCKED-INPUT` ตายแล้ว** ใบนี้เป็น **attended-only ไม่ใช่ blocked** · 🔴 **ANSWERED ไม่ใช่ PASS** — เกณฑ์ client-observable ของใบ (ถึงหน้า char-select / process exit) **ไม่ผ่านสักช่อง** · 🔴 **ข้อ 8 ของ GT-026 ยังไม่ปลด** — ปลดได้ต่อเมื่อกลับถึงหน้าเลือกตัวละครได้จริง ซึ่งยังไม่เกิด · ดูบล็อก **RESULT R166** ใต้หัวใบ] *(สถานะเดิมก่อนปิด:* [🟡 **variant C รันแล้ว 2026-08-23 00:06 (+07:00) — ผลลบมีค่า** · A/B ยัง 🔴 BLOCKED-INPUT]*)*

> ## ✅ RESULT R166 — สามช่องจากสี่ วัดครบในคืนเดียว ผลลบทั้งสาม (2026-08-25 ~17:00-17:45 +07:00)
>
> **boot commit เดียวกันทั้งสามรอบ: `06b62abd423cff9fc9c965d52178fd2fca62c38e`** (tree ตรงกับ `main` head `0a030f97` · CODE_DELTA 0 ทุกรอบ · ด่าน 6a-6e ผ่านทุกรอบ) ⇒ **ตัวควบคุมคุมถึงระดับ commit**
>
> | | **subcode 03** (กลับหน้าเลือกตัวละคร) | **subcode 01** (ออกจากเกม) |
> |---|---|---|
> | **variant A** (ack + close socket) | ❌ วัดแล้ว **ไม่เปลี่ยนหน้า** (จ็อบ 1148) | ❌ วัดแล้ว **โปรเซสไม่ออกเอง** (จ็อบ 1151) |
> | **variant B** (`0x709E` → ack + close) | ❌ วัดแล้ว **ไม่เปลี่ยนหน้า** (จ็อบ 1145) | ⬜ **ไม่ได้วัด — จงใจ · คำตัดสิน chief R166: ไม่ต้องรัน** (เหตุผลใต้ตาราง) |
>
> **ชั้น (1) wire/DB — ✅ PASS ครบทุกรอบ**
> - ไคลเอนต์ส่ง `LogoutVital 0x1B40` จริง · PC 34 B · discriminator `08 03` / `08 01` ตรงปุ่มที่กด · **byte-identical ระหว่างรอบ A/03 กับ B/03**
> - รอบ B: sha256 ตรง pin **สามชิ้น** (request 34 B `EC5B53DC…` · `return_select_first` 38 B `A4C8DF42…` · ack 36 B `FC8B9E2C…`) ⇒ 🎯 **ครั้งแรกที่ไคลเอนต์ตัวจริงได้รับ `0x709E` *ในฐานะ response ต่อ `LogoutVital` ตัวจริง*** (เฟรม 48 B บนสาย)
> 🔴🔴 **แก้โดย chief R166 หลัง `pf-adversary` ตัวที่สอง — ถ้อยคำเดิมของบล็อกนี้เขียนว่า "ครั้งแรกในประวัติโปรเจกต์" ซึ่ง *เป็นเท็จ*:**
> **`GT-033 variant C` ส่งเฟรม `0x709E` ชุดเดียวกันเป๊ะถึงไคลเอนต์ตัวจริงไปแล้วตั้งแต่ 2026-08-23 00:06 (+07:00)** (บูตเขียว `7b80025` · PC/frame sha ตรง pin เดียวกัน)
> หลักฐานอยู่ในรีโปเราเอง: `pirate-force-server/docs/HYPOTHESIS_LEDGER.json` แถว `HYP-PF-031.evidence_gap` ซึ่ง **chief R123 amend ไว้เองเมื่อ 2026-08-23** ว่า *"the push HAS now been shown to a real client"*
> 🔴 **สิ่งที่ต่างจริงระหว่าง C กับ B คือ *การจับคู่*:** C เป็น **unsolicited push** (ยิงด้วยแชต · ไม่มี request) · B เป็น **response ต่อ `LogoutVital` ตัวจริงที่ผู้เทสกดเอง** ⇒ **นั่นคือความใหม่ของรอบ B ไม่ใช่ "ไบต์แรก"**
> 🔴 **และ `external/PF_FIELD_VALIDATION.tsv:144` บอกว่า `ReturnSelectServerVital` มี `observed_frames=2` ใน capture corpus ที่แช่แข็งไว้ตั้งแต่ 2026-08-15/16** — **ก่อน** variant B/C ทุกครั้ง ⇒ **ยังไม่มีใครแยกว่าเป็นของจริงหรือ schema collision** (rider ของ `RE-070`)
> ⇒ 📌 **บทเรียน: superlative จากแหล่งเดียว (จดหมายสะพาน) ถูกยกเข้าทะเบียนโดยไม่เปิด ledger ที่นั่งอยู่ในรีโปเดียวกัน — ห้ามเขียน "ครั้งแรก/ไม่เคยมี" โดยไม่ grep ledger ก่อน**
> ⇒ บรรทัดเดิมของใบที่ว่า *"ยังไม่เคยมี client เห็น `0x709E` แม้แต่ไบต์เดียว"* **ตายไปตั้งแต่ variant C แล้ว ไม่ใช่ตายคืนนี้**
> - รอบ A: **census เฟรมขาออกทั้งรอบ** ยืนยันว่า **ไม่มี `0x709E` แม้แต่ไบต์เดียว** ⇒ A กับ B ต่างกัน **ตัวแปรเดียวเป๊ะ**
> - `sessions.closed_at` ถูกเขียน **ก่อน** ไบต์ response ถูกคิว (รอบ B วัดได้ 26 ms) ตรงกับที่ scenario ประกาศ · `OPEN_SESSIONS 0 · INTEGRITY ok · FK_ROWS 0` · **CANON ไม่ขยับ** · teardown exit 0 ทุกรอบ
>
> **ชั้น (2) client-observable — ❌ ไม่ผ่านทั้งสามช่อง**
> - ทั้งสามรอบ: กล่อง `ล็อคเอาท์` หายไปเฉย ๆ แล้ว **ไม่มีอะไรเกิดขึ้นอีกเลย** — ไม่มีหน้าเลือกตัวละคร · ไม่มีป๊อปอัพ disconnect · ไม่มี error · ไม่ค้าง · **โปรเซสไม่ออกเอง** · ผู้เทสต้องกด X เอง
> - วัดบนวิดีโอเอง ไม่ใช่คำบอกเล่าอย่างเดียว (แตกเฟรม 2 fps · ยืนยันจุดสำคัญ 30 fps): รอบ B **50 วิ** · รอบ A/03 **57.6 วิ** · รอบ A/01 **~68-77 วิ** ที่ไม่มีการเปลี่ยนสถานะใด ๆ · `X:-8,553 Y:-2,579` ไม่ขยับสักหลักทั้งสามรอบ
> - 🔴 ช่วงที่ค่าต่างต่อเฟรมสูงขึ้น (1,200-2,900 px) ในรอบ A ทั้งสอง = **ผู้เทสหมุนกล้องระหว่างรอ** ไม่ใช่การเปลี่ยนสถานะ (พิกัด HUD เท่าเดิมทุกหลัก) — จดไว้เพราะถ้าไม่จด ตัวเลขนั้นจะถูกอ่านผิด
>
> **🔴 คำตัดสิน chief R166 เรื่องช่องที่สี่ (B/subcode 01): ไม่ต้องรัน *ในรอบถัดไป* — และนี่คือการตัดที่ประกาศ ไม่ใช่การลืม**
> เหตุผลสองข้อ ① สามช่องที่วัดแล้ว **ให้ผลลบเหมือนกันหมด** และ A เป็นซับเซ็ตของ B **ในมิติไบต์ขาออก** ⇒ ช่องที่สี่มีข้อมูลคาดหวังต่ำที่สุด **ในบรรดาสี่ช่องของตารางนี้** ② มีการทดลองในเกมอื่นที่ให้ข้อมูลมากกว่าต่อการบูตหนึ่งครั้ง (ดูบล็อก **กิ่งที่ตารางไม่ครอบ** ข้างล่าง) ⇒ ถ้าจะจ่ายบูต ควรจ่ายให้กิ่งพวกนั้นก่อน
>
> 🔴🔴 **สองเหตุผลที่ chief เคยเขียนแล้ว *ถอนเอง* หลัง `pf-adversary` (R166 · ห้ามยกกลับมาใช้):**
> - ~~*"ชื่อ `ReturnSelectServerVital` จับคู่กับ 'ออกจากเกม' ขัดความหมายในตัว"*~~ — **ตัดสินด้วยชื่อ ซึ่งเป็นชั้นหลักฐานที่อ่อนที่สุดที่เรามี** และ `RE-070` เตือนเองว่า mapping `1=exit`/`4=char-select` **ไม่มีหลักฐาน** ⇒ เราไม่รู้ด้วยซ้ำว่า mode สองค่านั้นแยกกันตามชื่อปุ่มจริงไหม · เหตุผลนี้ยืนอยู่บนโมเดลที่ช่องนั้นมีไว้ทดสอบพอดี
> - ~~*"คำตอบที่เหลือเป็น static ล้วน ⇒ บูตเกมไม่ขยับ"*~~ — **ผิด** · `+0x24` เป็น timestamp และเราปิด socket ที่ **250 ms หลัง ack เสมอทั้งสามรอบ ไม่เคยแปรค่าเลย** ⇒ การเปลี่ยนเลขเดียวใน scenario **คือการทดลองในเกมที่ตรงกิ่งนั้น** ⇒ กิ่งนี้ **ไม่ใช่ static ล้วน**
>
> 🔴 **และต้นทุนของการตัดไม่ใช่ "8 นาที"** — ทั้งสามรอบใช้ boot commit เดียวกัน `06b62abd…` ⇒ เมื่อโค้ดเดินหน้า **ช่องที่สี่จะไม่มีวันถูกวัดใต้ตัวควบคุมระดับ commit เดียวกันอีก** ⇒ ตารางจะเหลือ "สามช่องเทียบกันได้ + หนึ่งช่องเทียบไม่ได้" ตลอดไป · **นี่คือราคาที่จ่ายโดยรู้ตัว**
> 🔴 **ช่องนี้ยัง "ไม่ถูกวัด" ไม่ใช่ "ถูกตอบ"** — ห้ามใครอ่านตารางนี้ว่าครบสี่ช่อง · ถ้าคุณ Panya สั่งให้ครบ รันเพิ่มได้ ~8 นาที ไม่มีอะไรกีดขวาง
>
> **🔴 nonclaims — ยกมาครบจากจดหมายทั้งสามใบ ห้ามอ้างผลใบนี้ที่ไหนโดยไม่พกไปด้วย**
> ① **ไม่ได้พิสูจน์ว่า `0x709E` ไม่ใช่ trigger** — พิสูจน์เฉพาะว่า *องค์ประกอบนี้* (`0x709E` ค่าฟิลด์ศูนย์ทั้งหมด → ack → ปิด socket) ไม่ทำให้เปลี่ยนหน้า
> ② **แยกไม่ออกสามทาง:** "vital ผิดตัว" / "vital ถูกแต่ค่าฟิลด์ผิด" / "vital ถูกแต่ต้องมีอย่างอื่นคู่กัน" — ค่าฟิลด์เป็น zero default เพราะไม่มี producer
> ③ **A ไม่ใช่ "ตัวชี้ขาด" แต่เป็น "ตัวควบคุม"** — B ทำทุกอย่างที่ A ทำ บวก `0x709E` · สิ่งที่ A ตอบจริงคือ *"เฟรม `0x709E` ที่ไม่มีใครบริโภค ไปขวางไม่ให้ไคลเอนต์เห็นการปิด connection หรือเปล่า"* ⇒ **ไม่ขวาง** (หน้าสะพานถอนคำว่า "ชี้ขาด" ด้วยตัวเองก่อนเข้าใบ)
> ④ **ไม่ได้พิสูจน์ว่าไคลเอนต์ "ไม่มีทาง" กลับหน้าเลือกตัวละคร** — พิสูจน์ว่า **สอง response policy ที่เรามี ไม่ทำ**
> ⑤ **การที่กล่องเมนูหายไป ไม่ใช่หลักฐานว่าไคลเอนต์บริโภคอะไรจากเซิร์ฟเวอร์** — handler ของปุ่มน่าจะปิดกล่องเองตอนคลิก · **สองการอ่านนี้แยกไม่ออกจากหลักฐานชุดนี้** (ดูข้อ ⑦ เรื่องนาฬิกา — การเรียงเวลาช่วยไม่ได้)
> ⑥ **ไม่ claim ว่า response ของเรา = ของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งกู้ไม่ได้ตลอดกาล
> ⑦ 🔴 **ยังไม่ได้เทส variant D ที่ยังไม่มี** — ปิด socket **โดยไม่ ack เลย** · ack แล้วเงียบ **โดยไม่ปิด** · **ไม่เคยมีใครลองสองอันนี้**
> ⑧ 🔴 **ไม่ได้เทสในสถานะ logout-dialog ที่ยังเปิดอยู่** — คาเวียตเดิมของ `pf-adversary` (R120) **ยังมีผลกับ A/B ไม่ใช่แค่กับ variant C**
> เพราะ nonclaim ⑤ บอกเองว่า handler ของปุ่มน่าจะปิดกล่องตอนคลิก ⇒ ตอน `0x709E` มาถึง (≥40 ms หลังคลิก) **กล่องปิดไปแล้ว**
> ⇒ **B อยู่ใน state เดียวกับ C ทุกประการในมิติที่คาเวียตพูดถึง** · *(ข้อนี้ตกหล่นจากฉบับแรกของบล็อกนี้ — `pf-adversary` จับได้ · เติมโดย chief R166 ในรอบเดียวกัน)*
>
> ### 🔴🔴 กิ่งที่ตารางสามกิ่งของใบ **ไม่ครอบ** — เขียนโดย chief R166 หลัง `pf-adversary` หักล้างฉบับแรก
> ถ้อยคำต้นฉบับของใบคือ *"ถ้าทั้งคู่ไม่ทำ = **คำตอบอยู่ที่อื่น** (mode/timer ที่ orchestrator รอ)"* —
> **"คำตอบอยู่ที่อื่น" + วงเล็บเดา** ไม่ใช่ "กิ่งที่สามที่ปิดเซต" · ฉบับแรกของบล็อกนี้แปลงวงเล็บให้กลายเป็นเซตปิด **ซึ่งผิด**
> **หกกิ่งที่ไม่มีใครเขียนไว้ และส่วนใหญ่ยัง *วัดได้ในเกม*:**
> 1. 🔴 **ครึ่ง "redirect" ไม่เคยถูกสร้างเลย** — สมมติฐานที่ดีที่สุดของใบเอง (`FACTPACK_R100…:215-216`) คือ *"END **or redirect** the GSCN session (close **or hand back to select-server**)"* · variant A ทำแค่ครึ่ง `close` ⇒ **ครึ่ง hand-back ไม่เคยมี scenario**
> 2. 🔴 **timer เป็นพารามิเตอร์ฝั่งเรา** — ปิด socket ที่ `250 ms` หลัง ack **เสมอ ทั้งสามรอบ ไม่เคยแปรค่า** ⇒ `0 / 2 วิ / 10 วิ / ไม่ปิดเลย` คือการทดลองในเกมที่ยังไม่มีใครทำ
> 3. 🔴 **ลำดับเฟรม** — scenario ที่มีชื่อ `..._RESPONSE_FIRST` คือ `0x709E` **ก่อน** ack · ลำดับตรงข้าม และการส่งซ้ำหลายเฟรม **ไม่เคยลอง**
> 4. 🔴 **ค่าฟิลด์** — body 16 ไบต์ศูนย์ทั้งหมด (ไม่มี producer) ตาม nonclaim ②
> 5. 🔴 **คนละ connection** — มีสองพอร์ต `LOGIN 10188` / `GAME 10189` และ `FINDINGS_R18:151` เขียนว่า *"ไม่มีอะไรผูก LOGIN เข้ากับ GAME เลย"* · static ยังบอกว่า orchestrator ปิด **สอง** sub-object (`[esi+0x18]`/`[esi+0x1c]`) แต่เราปิดแต่ socket เกม ⇒ **ไม่มีใครแตะฝั่ง login เลยแม้แต่รอบเดียว**
> 6. 🔴 **สถานะ logout-dialog** — ดู nonclaim ⑧
>
> ### 🔴🔴 ช่องว่างที่ใหญ่ที่สุดของใบนี้: **ไม่มีใครตรวจว่า "ยาถึงคนไข้"**
> ข้ออ้าง *"connection-teardown ถูกวัดแล้วว่าไม่ทำให้เกิด transition"* ยืนอยู่บนหลักฐานว่า **ฝั่งเราปิด socket** ไม่ใช่ **ฝั่งไคลเอนต์เห็นว่าถูกปิด**
> - ไม่มีบรรทัดไหนในสามจดหมายรายงานว่า **หลัง `[G!]` ไคลเอนต์ส่งอะไรออกมาอีกไหม / มี error / มี reconnect attempt** — ทั้งที่ variant C เคยรายงานเฟรมขาออกต่อเนื่อง `#44→#95` ⇒ **ข้อมูลนี้อ่านได้จาก capture เดิม ไม่ต้องบูตใหม่**
> - 50-77 วินาทีหลังปิด socket ไคลเอนต์ยัง HUD ครบ ไม่มีป๊อปอัพ ⇒ **อ่านได้สองทางที่แยกไม่ออก:** (ก) เห็นแล้วแต่ไม่ทำอะไร (ข) **ไม่เคยเห็นเลย**
> - 🔴 **ไม่มี positive control:** ทั้งโปรเจกต์ไม่มีรอบไหนที่แสดงว่าไคลเอนต์ตัวนี้ **แสดงอาการหลุดการเชื่อมต่อขณะอยู่ในแมพ** ได้ (ที่มีคือ `disconnect dialog` ของหน้า login เท่านั้น)
> ⇒ 🔴 **ถ้อยคำที่ถูกต้องคือ "เราปิด socket แล้วไคลเอนต์ไม่เปลี่ยนหน้า" ไม่ใช่ "connection-teardown ถูกหักล้างแล้ว"**
> ⇒ **เช็คราคาศูนย์ที่ปิดข้อนี้ได้ทันทีจากไฟล์บนสะพาน:** `grep` หา `[G<`/`SENT` ใด ๆ ที่เวลาหลัง `[G!]` ใน `capture_gt033a_*` และ `capture_gt033a2_*` — **ขอไว้ในจดหมาย `FROM_CHIEF_R166` แล้ว**



> 🟡 **RESULT variant C 2026-08-23 00:01–00:06 (+07:00)** (บูต green `7b80025` exact tree): server รับ ascii12 trigger + ส่ง pinned `0x709E` 1 ครั้งจริง (PC 38 B / frame 48 B SHA ตรง pin) · client **อยู่หน้าแมพเดิม** ส่ง runtime req ต่อเนื่อง (#44→#95) จนผู้เทสออกเอง ~63 วิ หลัง push
> - ตอบเฉพาะ variant C: **ไม่มี persistent transition** · แยกไม่ได้ระหว่าง "wrong trigger" กับ "right trigger, wrong client state" (อาจต้องอยู่ใน logout-dialog state ก่อน — adversary caveat เดิม)
> - ไม่ claim ว่าไม่มี flash <4s (screenshot latency) · ไม่ได้เทส subcode 01 · ไม่ได้ส่ง `LogoutVital`
> - ผลเต็ม: `notes_to_chief/20260823_0007_GT033C-NO-TRANSITION-709E-PUSH.md` (บริโภค R123)

> **เปิดโดย chief รอบ 100** จากผล GT-026 ท่อน B + static RE agent D (`pf_bridge\FACTPACK_R100_LOGOUT_TRANSITION_STATIC.md`)
> 🎯 **ปมที่ต้องปลด:** client ส่ง `LogoutVital 0x1B40` (subcode 03=char-select / 01=exit) แล้ว **รอ** อะไรบางอย่างจาก server เพื่อ transition · **echo (HYP-PF-012) พิสูจน์แล้วว่าไม่ทำงาน และรอบ 100 พบกลไกว่าทำไม** — inbound handler `0x446F30` เป็น actor-vital reconcile pass ล้วน ไม่มี branch เปลี่ยน scene/state/connection · การ transition จริงขับโดย session/connection orchestrator (vtable `0xf45030`) ที่ **รอแล้ว tear down connection** (gate ที่ mode +0x28 + timestamp +0x24) 🔴 **[แก้โดย chief R166]** ถ้อยคำเดิมตรงนี้เขียนว่า `+0x28 ∈ {1,4}` ซึ่ง **แข็งเกินหลักฐานหนึ่งขั้น** — หลักฐานจริง (`FACTPACK_R100…:142-144`) บอกแค่ว่า *"branches on `==1` and `==4`"* ⇒ นั่นคือ **เซตของค่าที่ถูกเทียบ** ไม่ใช่ **เซตของค่าที่ฟิลด์ถือได้** · และ **ห้ามใช้เป็น mapping `1=exit`/`4=char-select`** — ใบไม่เคยบอก · ดู `RE-070` ในหัวใบ
> ⇒ คำตอบที่ถูกน่าจะเป็น **(b) ปิด/redirect GSCN connection** ไม่ใช่ echo · `ReturnSelectServerVital 0x709E` = candidate ชื่อที่ดีที่สุดของ "กลับ char-select" แต่ยังไม่ยืนยัน (ไม่เจอ code ที่ consume มัน) · **static ตัดสินไม่ได้ → ต้อง A/B test**

- **✅ ทั้งสอง variant พร้อมแล้ว (chief รอบ 101 · pre-approved ใต้ policy #4 "แก้ปุ่มออกเกม" · production_allowed=false · fail closed · headless-proven):**
  - **variant A = HYP-PF-013 (มีอยู่แล้ว):** บูต `--logout-hypothesis-scenario scenarios\logout_hypothesis_ack_close.json` → รับ LogoutVital → ack + **ปิด socket/connection** ที่ 250ms (reuse close path ที่พิสูจน์แล้ว ไม่มี encoder ใหม่)
  - **variant B = HYP-PF-028 (build รอบ 101):** บูต `--logout-hypothesis-scenario scenarios\logout_hypothesis_return_select_server.json` → รับ LogoutVital → **ส่ง `ReturnSelectServerVital 0x709E` ก่อน** (body 16 ไบต์จาก serializer จริงของ client 0x5e69f0 · ทุกไบต์ tag มาจาก client · ค่า field = 0 เพราะไม่มี producer) → ตามด้วย ack เดิม → ปิด socket · headless: verifier 34 guards + replay 45 guards
  - ⚠️ **ทั้งสอง flag ใช้ `--logout-hypothesis-scenario` ตัวเดียว (ไม่ใช่ flag ใหม่)** · mutually exclusive · ต้องมี `--db` สำเนา canonical เหมือนเทสอื่น
- **steps (attended):** บูต **variant B ก่อน** (candidate ที่ตรง lead ชื่อที่สุด) → เข้าแมพ → HOME→ออก→`กลับหน้าเลือกตัวละคร` (subcode 03) → **ดูว่า client กลับหน้า character select ไหม** (ถ่ายภาพ) · ถ้าไม่เปลี่ยน → บูต variant A (close-only) ทำซ้ำ · แล้วทดสอบ subcode 01 (`ออกจากเกม`) ทั้งสอง variant
- **pass criteria สองชั้น:** client-observable = client เปลี่ยนไปหน้า char-select จริง (หรือ process exit สำหรับ subcode 01) · wire/DB = closed_at เติม (พิสูจน์แล้ว headless) · ถ้า variant B ทำให้ transition = **0x709E ยืนยันเป็น trigger** (ยกจาก candidate → confirmed) · ถ้า variant A ทำแต่ B ไม่ทำ = **response ที่ถูกคือ connection-teardown ไม่ใช่ vital** · ถ้าทั้งคู่ไม่ทำ = คำตอบอยู่ที่อื่น (mode/timer ที่ orchestrator รอ) — ผลลบมีค่าทุกกรณี
- **ปลดข้อ 8 ของ GT-026:** ถ้ากลับถึง char-select ได้ → ลองเข้าเกมซ้ำโดยไม่รีบูตเซิร์ฟ
- **nonclaims:** ไม่ claim ว่า response ของเรา = ของ server ต้นฉบับ (กู้ไม่ได้) · echo ถูกหักล้างพร้อมกลไกแล้ว · 0x709E เป็น candidate ไม่ใช่ข้อพิสูจน์ · field values ของ 0x709E = zero default ไม่มี producer · static ตัดสิน response shape ไม่ได้ (agent D) — นี่คือเหตุที่ต้อง attended A/B · **ยังไม่เคยมี client เห็น 0x709E แม้แต่ไบต์เดียว**
- **evidence (chief รอบ 101):** `reports\PF_LOGOUT_RETURN_SELECT001_HYP028_20260820.md` · ledger HYP-PF-028 · `tools\verify_logout_return_select_encoder.py` (34) · `tools\pf_logout_return_select_headless_replay.py` (45)

> 🔴 **สถานะรอบใหญ่ #12 ต่อ (จ็อบ 968/969 · บริโภคโดย chief R120):** บูต variant B ได้ เข้าแมพได้ เปิดเมนู HOME ได้
> **แต่รายการ `ออก` ไม่รับคลิกสังเคราะห์ 4 ครั้งติด** (zoom ยืนยันพิกัด · mouse_move ก่อนคลิก · double-click — เงียบ) ·
> `Return` ช่วยไม่ได้เพราะรายการเมนูไม่ใช่ปุ่ม default ⇒ **client ไม่เคยส่ง LogoutVital ⇒ ไม่มีผล variant ใดทั้งสิ้น — ห้ามอ่านเป็นผลลบ**
> 🆕 **variant C (chief R120 build · HYP-PF-031 LOGOUT-CHAT-PUSH-001 · ✅ gate เขียว + merge แล้ว — ปลดโดย chief R121):**
> ตัด HOME→`ออก` ออกจากสมการ — บูต `--logout-hypothesis-scenario scenarios\logout_hypothesis_chat_push_return_select.json`
> แล้วพิมพ์แชต ascii 12 ตัว (ท่า trigger เดียวกับ GT-032 ที่ผู้เทสทำได้แน่ผ่าน `Return`) ⇒ server **push**
> `ReturnSelectServerVital 0x709E` (เฟรม 48 ไบต์แช่แข็งตัวเดียวกับ variant B · sha256 pin เดิม) **โดยไม่รอ LogoutVital** ·
> คำถามที่ใบนี้ตอบ: client transition จาก push เดี่ยว ๆ ไหม — **yes = 0x709E คือ trigger จริงและไม่ต้องการ request pairing** ·
> no = transition ต้องการ pairing/ตัวอื่น (แล้ว variant A close-path ยังต้องรอเมนูหรือคนกดจริง ⇒ ยกเป็นใบที่ต้องมี Panya หน้าจอ)
> 🔴 **คาเวียตจาก pf-adversary (R120) — อ่านก่อนตีความผล:**
> ① **ผลลบของ variant C กำกวมโดยธรรมชาติ** — client อาจ consume `0x709E` เฉพาะตอนอยู่ใน state ของ logout dialog
> (state ที่เราไปไม่ถึงเพราะเมนูกดไม่ได้ — ตัวบล็อกเดียวกันที่ทำให้ต้องมีใบนี้) ⇒ ผลลบแยกไม่ออกว่า
> "0x709E ไม่ใช่ trigger" หรือ "เป็น trigger เฉพาะ state ที่เราสร้างไม่ได้" · **ผลลบห้ามสรุปข้ามไปหา connection-teardown ทันที** — จดว่า client ทำอะไร (เมิน? แชตค้าง? อาการใด ๆ)
> ② **one-shot latch เป็นราย connection** — ถ้า relog/reconnect ระหว่างเทส แชตอีกครั้งจะ push ซ้ำได้ ⇒ ถ้าเห็น push ครั้งที่สอง **จดว่ามี relog เกิดขึ้น** อย่าอ่านเป็นบั๊ก
> ✅ **ปลดแล้ว (chief R121 · 2026-08-21 ~11:1x +07:00):** HYP-PF-031 merge เข้า `main` แล้ว (merge commit `c6146a3`) ·
> **ท่าบูต: `git checkout 7b8002522fedeecf9bcd5ea9d0d4ec5e732e4034` (detached HEAD — บูตคำตัดสิน ไม่ใช่ branch)**
> commit นี้มีคำตัดสินเขียวของตัวเอง (`conclusion=success` run 32444037989 · 2026-08-21T03:44:20Z UTC = ~10:44 +07:00)
> และ tree byte-identical กับ main `c6146a3` (วัดโดย `pf_resolve_green_boot.py` — จะยืนยันสดก่อนบูตก็ได้:
> `py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch`) · เขียวนี้คือ subset บน Actions ไม่ใช่ gate เต็ม  [✅ **PASS ทั้งสามใบ — ⤴ ย้ายเนื้อหาเต็มไป archive แล้ว (chief รอบ 111)**]

เนื้อหาเต็ม (ผล · หลักฐาน · nonclaims · ข้อความตอน PENDING) อยู่ที่ `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260821_R111_GT027_028_029_CLOSED.md` — **ไม่มีอะไรถูกลบ**
- **GT-027 DAMAGE-ON-NPC-001** ✅ PASS (รอบใหญ่ #10 rerun ที่ Panya ขับเอง) — เลขเรนเดอร์ครบ แต่ **HP ของเป้าไม่ขยับแม้แต่หน่วยเดียวทั้งที่ดาเมจสะสม 505** ⇒ รายงานที่ re-derive ได้: `ServerProject\reports\PF_NPC_HP_LINK029_GT027_RERUN_ATTENDED_RESULT_20260820.md` ⇒ เป็นที่มาของ **GT-039** ด้านล่าง
- **GT-028 DAMAGE-SLOW-SWEEP-001** ✅ PASS — เหลือข้อ ⑥ (flags `0x0009` vs `0x0001` ต่างกันตรงไหนบนจอ) ที่ยังตอบไม่ได้ · **ไม่บล็อกอะไร ไม่ต้องรันรอบใหม่เพื่อข้อนี้**
- **GT-029 DYING-COUNTDOWN-001** ✅ PASS — เลขในวงลดจริง และคำถาม static ที่มันเปิด (UI นับเอง) ปิดแล้วในรอบ 102

## 🆕⭐ GT-034 HOSTILE-NATIVE-001: hostile ตัวจริงขึ้นแดงเองตอน scene-load โดยไม่ต้อง splice faction ไหม — เป้า `0x201F` Tornado Eagle · วิธี = ย้ายจุดวางตัวละคร + heading ตอนเข้าเกม  [✅ **ANSWERED (P1 ยืนยัน · คำถามหลักตอบแล้ว) — จ็อบ 1118 · 2026-08-25 ~01:5x (+07:00) · attended (Panya ขับ UI เอง) · จดหมาย `20260825_0230` · บันทึกโดย chief R158** — **คำตอบ: ไคลเอนต์ไม่ spawn hostile เองตอน scene-load — ขึ้นก็ต่อเมื่อเราส่งไปให้เท่านั้น** · P1 ยืนยัน: HUD ตอนเข้าแมพ `X 1,847 · Y -7,837` ตรงจุดที่ใบกำหนดเป๊ะ ⇒ **anomaly 731 หน่วยของรอบใหญ่ #12 ไม่เกิดซ้ำ** · client-observable: กวาด `Q` รอบตัว · เดินหา · เดินกลับถึงท่าเรือ — ไม่เจอทั้งนกทั้ง NPC · **census เฟรมขาออกอธิบายว่าทำไม: เลน scene-load ส่งออกแค่ `SCENE2_LOAD_ONLY_*` · `V99_SHOW_MESSAGE` · `V100_MUSIC` · login/keepalive — ไม่มีเฟรม actor เลยแม้แต่เฟรมเดียว** (`Tornado Eagle` ในล็อกทั้งหมดเป็นบรรทัด `[SELFTEST] PASS`) · 🎯 **ตัวควบคุมเชิงบวก คนเดียวกัน คืนเดียวกัน ห่างกัน 3 ชม.:** รอบ GT-045 เราส่ง `V134` ที่มี `P30 = TornadoEagle` (ยืนยันด้วย ASCII ในตัวเฟรม) ⇒ Panya เห็นจุดฟ้าบน minimap ตรงตำแหน่งนั้น + NPC บนจอ · รอบนี้ไม่ส่งอะไรเกี่ยวกับ actor ⇒ ว่างเปล่า ⇒ **ผลลบนี้มีตัวควบคุมเชิงบวกครบ แข็งแรงกว่า NO-RESULT สองรอบก่อนมาก** · `RUN_SHA_BEFORE = RUN_SHA_AFTER` (เลนนี้ไม่เขียน DB) · CANON ตรง · teardown exit 0 · 🔴 **nonclaims:** ① ไม่ได้พิสูจน์ว่า**ไม่มีทางใด**ที่จะทำให้ client spawn เอง — พิสูจน์เฉพาะว่า**เลน scene-load ที่ไม่ส่ง actor ไม่ทำให้เกิด** ② ไม่ได้เดินสำรวจทั้งแมพ ③ ~~`TornadoEagle` ยืนยันจาก ASCII ในเฟรม แต่**ยังไม่ได้ยืนยันด้วยตาว่าตัวนกถูกวาดบนจอ**~~ ✅ **ปิดแล้วโดย chief R163 (2026-08-25 ~15:xx +07:00): คุณ Panya เห็นโมเดลนกจริงบนจอ + ป้ายชื่อ `Tornado Eagle` อ่านออก ระหว่างรอบ GT-045 v3 · ภาพ `GameClient\Data\ScreenShot\20260825_121434.png` · จดหมาย `20260825_1235` §④ (ยืนยันซ้ำ `20260825_1300` §③ · `20260825_1340` §⑤)** — 🔴 **ปิดเฉพาะข้อ "วาดได้ไหม" เท่านั้น · เรื่อง "ระยะวาดเท่าไร" ยังไม่ตอบ** และ positive control ของ GT-035 ยังบังคับเหมือนเดิม · 🆕 ของแถม: **ป้ายชื่อนกเป็นสีเขียว** ⇒ ที่มาของ `RE-067`] *(สถานะเดิมก่อนตอบ:* [🟡 **PENDING / NO-RESULT — รันแล้ว 2026-08-22 23:56 (+07:00) กรณี 3: ไปถึงพิกัดคาดจริงแต่ไม่เห็นตัวนกเลยหลังกวาด 360° — คำถามหลักยังไม่ถูกตอบ · ห้าม redirect Door A · GT-035/036 ยัง BLOCKED**]

> 🟡 **RESULT 2026-08-22 23:47–23:56 (+07:00) — NO-RESULT ตามตารางกรณี 3** (บูต green `b665d92` exact tree):
> - placement ทำงานตามดีไซน์: HUD `X 1,847 / Y -7,837` ตรงค่าคาดเป๊ะ (wire `1847.5244, -7837.6978, z 931.04, heading π` · TeleportVital รายงานกลับตรงทุกค่า **ยกเว้น z ที่ client ปัดเป็น `931.0`**) — **GEO-PF-006 ชั้น wire/client พิสูจน์แล้ว**
> - แต่กวาด Q ครบ 360° ที่จุดวาง: **ไม่เห็นมอนสเตอร์รูปนก/ป้ายชื่อ `Tornado Eagle` เลย** ไม่ถูกโจมตี · ไม่มี S2 (โดยเจตนา — ไม่มีเป้าให้เลือก)
> - runtime outbound **ไม่มี** label ตระกูล population/NPC/actor (scenario เป็น load-only ตามดีไซน์) ⇒ แยกไม่ได้ว่า "client ไม่ spawn จากข้อมูล ship เอง" หรือ "ตัวอยู่แต่ไกล/มุมอื่น/เงื่อนไข render อื่น"
> - 🔴 ห้ามอ่านเป็น "เห็นตัวแต่ไม่แดง" (ผลลบนิยามแคบของใบนี้) · **ห้าม redirect Door A** · GT-035/036 คง BLOCKED
> - คำถามถัดไปที่ต้องเคาะก่อนออกแบบรอบใหม่ (chief จะเสนอในจดหมาย): ตัวเลือกการแตกสาเหตุ เช่น วางจุดสังเกตหลายจุด / ตรวจว่า client มีเงื่อนไข spawn NPC ฝั่ง data ที่ต้องการเฟรมจาก server
> - ผลเต็ม: `notes_to_chief/20260822_2359_GT034-NO-RESULT-native-render.md` (บริโภค R123) · tooling notes: right-drag ทำกล้อง top-down ค้าง · teardown template เลือก capture root ผิดเมื่อไม่ส่ง `CaptureFilter` (ฝากเจ้าของ tooling)

**ที่มา:** ORDER `20260820_1140_PANYA-ORDER-retarget-real-hostile.md` + **คำตัดสิน Panya
`notes_to_chief/consumed/20260821_1104_PANYA-DECISION-GT034-spawn-relocate.md` (2026-08-21 11:04 +07:00)** —
ปลดสถานะ "⏸ รอเคาะเรื่องระยะทาง" ที่ค้างตั้งแต่ 2026-08-20 ~11:40
- ① เป้า = **`0x201F` Tornado Eagle** (ตัวเดียวใน 13 ตัวที่ **retaliate-only** · บัญชีเต็ม: `FACTPACK_R102_HOSTILE13_ROSTER.md`)
- ② วิธี = **แก้จุดวางตัวละครตอนเข้าเกม + ตั้ง heading หันเข้าเป้าตั้งแต่วินาทีแรก**
  🔴 **ห้ามออกแบบท่าเดิน · ห้ามให้ผู้เทสวัดอัตราเดิน · ห้ามเปิดเลน teleport เพื่อใบนี้** — Panya ตัดทิ้งทั้งสองทางเอง
- 🔴 **ห้ามเปลี่ยนเป้าเป็นตัว aggressive** (`0x203B` Jungle Big Tiger · `0x2040` Ward Apes · `0x2085` Orc Chief — AGGRO=1200) — Panya ไม่ได้อนุญาต
- เลนที่ build แล้ว (chief รอบ 122 · GEO-PF-006): scenario `scenarios/port_royal_tornado_eagle_p30_load_only.json`
  บนเลน scene_load เดิม — **read-only session = เขียน DB ไม่ได้โดยโครงสร้าง** · เขียว(cloud sanity) 1868 pass · **ยังไม่ merge**

**คำถามหลัก (คำต่อคำจาก Panya — ห้ามแก้แม้แต่ตัวอักษรเดียว):**
> **hostile ตัวจริงขึ้นแดงเองตอน scene-load โดยไม่ต้อง splice faction ไหม**

⭐ **ผลลบมีค่าเท่าผลบวก** — ถ้าไม่ขึ้นแดงเอง = faction ของ placement ไม่ได้ถูกส่งตอน scene-load
⇒ **redirect ประตู A ทั้งประตู** ซึ่งเป็นคำตอบที่แพงพอ ๆ กัน · **จดเป็นผล ไม่ใช่ fail**
🔴 **แต่ผลลบของคำถามหลักมีนิยามแคบ: "เห็นตัวมัน แต่ชื่อ/กรอบไม่แดง" เท่านั้น** — "ไม่เห็นตัวมันเลย" คือ NO-RESULT
ของคำถามหลัก (ดูตารางผลด้านล่าง) **ห้าม redirect Door A จากการไม่เห็นตัว** (กติกาจาก adversary review R122)

### 🔴 ก่อนบูต — resolve commit เขียว (ท่าเดียวกับ GT-041 · รันเครื่องมือ ไม่ใช่ก๊อป SHA)

```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` (detached HEAD ถูกแล้ว — บูต*คำตัดสิน* ไม่ใช่ branch)
- **exit 3** = ห้ามบูต จดว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · มีบรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ จดลงผลเสมอ
- ⚠️ ณ วันที่เขียน (รอบ 122) โค้ดใบนี้อยู่บน branch `claude/wizardly-wright-hk4raq` (commit `b665d92`) **ยังไม่ merge เข้า `main`**
  ⇒ เครื่องมืออาจคืน commit เขียวที่**ยังไม่มี scenario ใบนี้** — จึงต้องยืนยันสามข้อนี้กับ `<SHA>` ที่จะบูตจริง:
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "scene-load-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/port_royal_tornado_eagle_p30_load_only.json && echo SCENARIO_PRESENT
```
1. ไฟล์คำตัดสินมี `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ (`success` = subset บน Actions ไม่ใช่ gate เต็ม)
2. `git grep` เจอ flag จริง — **ห้ามใช้ `--help` เป็นหลักฐาน** (คืน 0 บรรทัดผ่านสะพาน — บทเรียนรอบใหญ่ #7 ข้อ 6)
3. เห็นคำว่า `SCENARIO_PRESENT`
- **ไม่ครบสามข้อ = ห้ามบูต** ใบนี้อยู่ BLOCKED ต่อ · **ปล่อยไว้ที่เดิม ห้ามลบ ห้ามย้าย**

### คาเวียตแมพ/โซน (ข้อบังคับข้อ 1 ของ Panya — สถานะการยืนยัน ณ รอบ 122)

- **ระดับสูงสุดที่ artifact ที่ commit แล้วตอบได้ = "แมพเดียวกัน":** จุดสังเกตปัจจุบัน (P0+100X) กับเป้า (P30)
  เป็นแถวของ**ตาราง frozen เดียวกัน** `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` 115 แถว (bg0001 / Port Royal)
  และแข็งกว่านั้น: V127/V128 เคยให้ client จริง**ยืนที่จุด +100X ของ P30 นี้เป๊ะ ๆ** ในเลน runtime ที่ผ่านแล้ว
- 🔴 **เลข scene id เชิงตัวเลขยังไม่ถูกพิสูจน์** — ต้อง dump SCENE_NAME (007) + MAP_SCENE_LIST (101) บนเครื่องสะพาน = **GT-044** (ท้ายไฟล์)
- ⇒ ถ้า client โหลดแล้วเจอ**พื้นที่ผิด/ว่างเปล่า** — **นั่นแหละคือคำตอบเรื่องโซนที่เดินทางมาถึง** ถ่ายภาพ จดพิกัด HUD
  ออกจากเกม รายงานกลับ · **ห้ามวนบูตซ้ำเพื่อ "ลองใหม่"** (คำสั่ง Panya: คนละโซนให้หยุด อย่าเดา อย่าดันต่อ)

### คาเวียต Z และทิศกล้อง (การตีความของ chief — เปิดเผยต่อ Panya ในจดหมาย R122 · ถ้าไม่เห็นด้วยแก้ค่าเดียวจบ)

- **Z ของจุดวาง = Z ของแถวเป้าเป๊ะ (931.0413208007812) โดยเจตนา** — จดหมายสั่ง "อย่าวางที่ Z เดียวกับเป้าเป๊ะ"
  แต่ความเสี่ยงที่เธอระบุคือลอย/ร่วง (ΔZ +707.7 จากจุดเก่า) · จุดที่เลือกคือจุดที่ **client จริงเคยยืนได้** (V127/V128)
  = หลักฐานกันร่วง/ลอยที่แข็งที่สุดที่มี — ตีความตามเจตนา ไม่ใช่ตามตัวอักษร · **ตัวละครร่วง/ลอย/จมพื้น = จดพิกัด HUD Z
  แล้วดำเนินต่อได้ ไม่ใช่ falsify**
- **trade-off ที่แลกมา:** จุด +100X ยืนได้แน่ แต่ตามแบบแผนที่พิสูจน์แล้ว (V134 camera workaround + R119)
  **กล้องแรกเข้าน่าจะหัน +X = หันหนีเป้า** — heading π ที่เซิร์ฟเวอร์ส่งเป็น **heading ผู้เล่นแรกเข้าที่ไม่ใช่ศูนย์ครั้งแรก
  ของทั้ง lineage** และไม่มีหลักฐานว่า client ใช้มันกับ avatar/กล้อง (nonclaims: `heading_mapping` / `camera_orientation`)
  ⇒ **การหมุนกล้องหาเป้า (~180°) เป็นส่วนหนึ่งของโปรโตคอล ไม่ใช่ความผิดพลาด** · ถ้าเข้าเกมแล้วหันเข้าเป้าเลย
  = การวัด heading_mapping ครั้งแรกที่มีค่ามาก จดทันที

- **objective:** พิสูจน์หนึ่งข้อ: **`0x201F` Tornado Eagle (hostile faction-6 ตัวจริง) แสดงสถานะแดงเองตอน scene-load
  โดยที่เซิร์ฟเวอร์ไม่ splice faction ใด ๆ หรือไม่** — สังเกตล้วน ไม่มีการโจมตี ไม่มีการเดิน

- **db:** สำเนาเสมอ ห้ามเปิด canonical · เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ**
  ```
  copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-034_<yyyyMMdd_HHmmss>.sqlite3
  copy state\pirateforce.sqlite3 state\run_gt034.sqlite3
  ```
  - เลนนี้เป็น **read-only session โดยโครงสร้าง** — คำทำนายคือ*ไม่มีไบต์ไหนของสำเนาเปลี่ยนเลย* ⇒ เก็บ sha256 ของ
    `state\run_gt034.sqlite3` ก่อน-หลังไว้เทียบด้วย (ถ้าขยับ = ผิดคำทำนาย จดว่าแถวไหนขยับ — นั่นคือข้อมูล ไม่ใช่ fail)
  - scenario บังคับตัวละครชื่อ **`Arena01`** · pre-flight บนสำเนา (อ่านอย่างเดียว `mode=ro`):
    `SELECT id,name FROM characters WHERE name='Arena01' AND deleted_at IS NULL;`
    ⇒ ถ้าไม่เจอ **หยุด รายงานกลับ** ห้ามสร้างตัวละครสดเพื่อใบนี้
  - เพราะจุดยืนถูก override โดย scenario ทุกบูต ตำแหน่งเดิมใน DB ไม่มีผลกับใบนี้

- **server args (เป๊ะ · รันจาก working tree ของ checkout ที่ผ่านสามข้อยืนยัน):**
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt034.sqlite3 --scene-load-scenario scenarios\port_royal_tornado_eagle_p30_load_only.json
  ```
  - flag นี้ mutually exclusive กับ scenario โหมดอื่นทุกตัว · 🔴 **ต้องใส่ `--db` ชี้สำเนาเสมอ** — ถ้าลืม เลน scene-load
    จะเงียบ ๆ ไปใช้ `state\test_arena_v1.sqlite3` เป็น default (`app.py:362`) ไม่ใช่ไฟล์ของรอบนี้
  - **เลนนี้ไม่มี chat trigger — ไม่ต้องพิมพ์อะไรเลยทั้งรอบ** (และอย่าลืม: ตัวอักษรที่พิมพ์ตอนช่องแชตไม่โฟกัส = hotkey)

- **คำทำนาย (จดไว้ล่วงหน้า — คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว):**
  - **P1:** HUD แสดงตัวละครยืนใกล้ `(1847.5, -7837.7)` Z ~931 (ค่าเต็มที่เซิร์ฟเวอร์ส่ง: `1847.5244140625, -7837.69775390625, 931.0413208007812`)
    ⚠️ anomaly ที่รู้ตัว: รอบใหญ่ #12 ผู้เทสยืนห่างจากจุดที่เซิร์ฟเวอร์ส่ง **~731 หน่วย** สาเหตุ [UNKNOWN] —
    **ถ้ายืนไม่ตรงคำทำนาย จดพิกัด HUD จริง แล้วเดินหน้าต่อ นั่นคือข้อมูล**
  - **P2:** Tornado Eagle (มอนสเตอร์รูปนก) อยู่ **~100 หน่วยทาง −X ของตัวละคร** — client เรนเดอร์ placement จาก map data
    ของตัวเอง (พิสูจน์กับ `0x2001` ที่จุดเก่า ระยะ 100 หน่วยเท่ากัน · แต่ **ไม่มีใครเคยเห็น `0x201F` บนจอมาก่อน** — nonclaim `native_render`)
  - **P3 (คำทำนายหลักของกล้อง):** กล้องแรกเข้า**หัน +X = เป้าอยู่ข้างหลัง** ตาม V134/R119 ⇒ ต้องหมุน ~180° จึงเห็นเป้า ·
    ถ้าเข้าเกมแล้วเห็นเป้าเลยโดยไม่หมุน = client ใช้ heading π ที่ส่งไป — **การวัด heading_mapping ครั้งแรก** จดละเอียด
  - **P4 (คำถามของใบ):** ชื่อ/กรอบของมัน**แดงเอง**แบบเดียวกับที่ GT-032 เคยเห็นตอน splice `0x2001` —
    แต่รอบนี้**ไม่มี splice สักไบต์** · ทำนายจาก faction=6 ใน client tables — **นี่คือสิ่งที่ยังไม่รู้จริง**

- **steps (บูตเดียว · สังเกตล้วน ~5 นาทีในเกม):**
  1. ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบ + pre-flight `Arena01` ตามบล็อก db
  2. เปิด **server ก่อนเสมอ** ด้วย args ข้างบน (client ที่บูตโดยไม่มี server ตายใน ~3.5 นาที)
  3. เปิด client (`Invoke-CimMethod Win32_Process Create`) → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย
  4. หน้าเลือกตัวละคร → เลือก **`Arena01`** → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
  5. เข้าแมพแล้ว **ห้ามแตะเมาส์/คีย์บอร์ดก่อนถ่าย S0** → **ถ่าย S0 ทันที** ให้เห็น X/Y บน HUD + นาฬิกาบนจอ —
    บันทึกว่า ณ วินาทีแรก กล้องหันทางไหน เห็นอะไรตรงหน้า
  6. **ยืนนิ่ง** สังเกต ~30 วินาที → **ถ่าย S1** มุมมองตรงหน้า
  7. 🔴 **ขั้นบังคับ ไม่ว่าเห็นเป้าหรือไม่:** หมุน**กล้องอย่างเดียว** (เมาส์/Q/E) ให้ครบ **360°** ช้า ๆ — คำทำนาย P3 บอกว่า
    เป้าน่าจะอยู่ข้างหลัง (~180°) · ระหว่างหมุน ถ่ายภาพทุกครั้งที่เห็นสิ่งมีชีวิต/ป้ายชื่อ —
    🔴 **ห้ามกด W/A/S/D ห้ามขยับตำแหน่งเด็ดขาด** (คำสั่ง Panya: ไม่มีท่าเดินในใบนี้)
  8. ถ้าเห็นเป้า: **คลิกซ้ายเลือกมันหนึ่งคลิก** (ท่า target-panel เดียวกับ GT-030/GT-038) → **ถ่าย S2** ให้เห็น target panel:
    ชื่ออะไร · กรอบ/ชื่อแดงหรือไม่ · 🔴 **ห้ามกดสกิล ห้ามกดปุ่มโจมตี ห้ามดับเบิลคลิก** — `0x201F` เป็น retaliate-only
    และ GT-035/036 ยัง BLOCKED · การตีคือใบอื่น
  9. **ถ่าย S3** ภาพสุดท้ายก่อนออก (HUD + นาฬิกา) → ออกจากเกม: **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย
  10. ปิด server · เก็บ raw GAME log ทั้งไฟล์ + console out/err **ห้ามลบ** · เทียบ sha canonical + sha สำเนา อีกครั้ง
  11. **teardown เสมอ แม้เลิกกลางคัน** (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 · `staged\TOOL_stop_stale_server.ps1`) ·
    ⚠️ ถ้า kill client กลางคัน **server ยังถือ session อยู่ — ต้อง restart server ก่อนเปิด client ใหม่** ไม่งั้นค้าง "connecting" ตลอดกาล

- **pass criteria — สองชั้น แยกกันเด็ดขาด ห้ามอ้างชั้นหนึ่งแทนอีกชั้น:**
  - **ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ):**
    - raw GAME log แสดง **StartGameRes พา f32 สี่ตัว** `x=1847.5244140625 · y=-7837.69775390625 · z=931.0413208007812 · heading=pi(3.14159...)`
      และ **เฟรม teleport scene 1 พา XYZ ชุดเดียวกัน** (ไม่ใช่กับดัก `(1,0,(0,0,0))` ของ boot ปกติ)
    - **ต้องไม่มีเฟรม splice/faction injection ใด ๆ ในล็อก** — เลนนี้ population=none, ไม่มี remote_actor (หัวใจของใบ: ไม่ splice)
    - sha256 canonical ก่อน-หลังตรง `CANON_SHA.txt` ทั้งสองครั้ง · sha สำเนา `run_gt034.sqlite3` ก่อน-หลัง (คำทำนาย: เท่าเดิม)
    - **ชั้นนี้ตอบไม่ได้:** มีอะไรบนจอ · นกแดงหรือไม่แดง · กล้องหันทางไหน
  - **ชั้น (2) client-observable (ต้องมีคนหน้าจอ):**
    - ภาพนิ่งบังคับ **S0 · S1 · S2 · S3** ทุกใบเห็นนาฬิกาบนจอ + จด **sha256 ของไฟล์ภาพทุกใบ** ลงในผล
    - ตอบสี่ข้อเป็นภาษาคน: **(ก)** เห็นมอนสเตอร์รูปนกไหม ทิศไหน (เทียบทิศกล้องแรกเข้า) ระยะประมาณเท่าไร
      **(ข)** ชื่อที่แสดง (ป้ายลอย และ/หรือ target panel) คืออะไร · **ชื่อ/กรอบแดง (hostile) หรือสีปกติ (neutral)** — คำตอบของใบทั้งใบอยู่ข้อนี้
      **(ค)** HUD X/Y/Z ที่ยืนจริง เทียบคำทำนาย P1 ห่างกี่หน่วย
      **(ง)** ตอนโหลดเสร็จ (ก่อนแตะอะไร) กล้องหันทิศไหน — เห็นเป้าโดยไม่ต้องหมุนไหม (= คำตอบ P3/heading_mapping)
    - **ชั้นนี้ตอบไม่ได้:** ภาพหน้าจอไม่ใช่หลักฐานว่าเซิร์ฟเวอร์ส่ง/ไม่ส่งไบต์อะไร

- **ตารางผล (จดเป็นผลทุกกรณี — ไม่มีกรณีไหนเป็น fail ของผู้เทส):**
  1. **เห็นนก + ชื่อแดงเอง** ⇒ native-red ยืนยัน · GT-035/036 รอ chief/Panya ปลด (**ห้ามปลดเอง**)
  2. **เห็นนก แต่ชื่อไม่แดง** ⇒ **ผลลบของคำถามหลัก — กรณีเดียวที่ redirect ประตู A** (faction ของ placement ไม่ได้ถูกส่ง/ใช้ตอน scene-load)
  3. **หมุนครบ 360° แล้วไม่เห็นนกเลย** ⇒ 🔴 **NO-RESULT ของคำถามหลัก — ห้าม redirect Door A** · จดเป็นผลเรื่อง
    `native_render`/ตำแหน่งยืนจริงแทน (ระยะ/เงื่อนไขเรนเดอร์ = ข้อมูลใหม่) — จดพิกัด HUD + ทุกทิศที่กวาดแล้ว
  4. **โหลดเข้าพื้นที่ผิด/ว่างเปล่า** ⇒ คำตอบเรื่องโซน — หยุด ถ่ายภาพ รายงาน **ห้ามวนบูตซ้ำ**
- **เกณฑ์หยุดเพิ่ม:** นกเข้าโจมตีเองทั้งที่ไม่ถูกตี (ขัด retaliate-only ใน client tables) = ข่าวใหญ่ — ถ่ายภาพ/จดเวลา
  แล้วออกจากเกมทันที ห้ามสู้กลับ

- **nonclaims (บังคับจากคำตัดสิน — ติดไปกับผลทุกกรณี):**
  - faction / AI / drops **เป็นข้อมูลที่ ship มากับ client** ไม่ใช่พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล
  - **การย้ายจุดวางตัวละครเป็นดีไซน์ของเรา** (GEO-PF-006) ไม่ใช่ท่าของเซิร์ฟเวอร์ต้นฉบับ · **ห้าม claim ว่าผู้เล่นจริงเคยเกิดตรงนั้น**
  - ใบนี้**ไม่ตอบ**ว่าตีมันได้ไหม (GT-035) หรือฆ่าได้ไหม (GT-036) — ตอบแค่ "ขึ้นแดงเองไหม"
  - `heading_mapping` / `camera_orientation` / `native_render` / `client_standing_position` / `scene_id_numeric_provenance` /
    `scene_seq_provenance` = nonclaims ทางการของเลน (ตาม scenario JSON + GEO-PF-006)
  - "แมพเดียวกัน" พิสูจน์ที่ระดับตาราง placement + จุดยืน V127/V128 — **เลข scene id เชิงตัวเลขยังเปิดอยู่ (GT-044)**

- **result:** (ผู้เทสกรอก: คำตอบ (ก)(ข)(ค)(ง) · หมายเลขกรณีจากตารางผล · ภาพ S0–S3 พร้อม sha256 · เวลา ·
  sha canonical ก่อน-หลัง · sha สำเนา run_gt034 ก่อน-หลัง · path ของ raw GAME log + console · BOOT_COMMIT ที่ใช้จริง + ผลสามข้อยืนยัน)

⚠️ **เลขชนกัน (ประวัติ — คงไว้):** จดหมายผู้เทส 12:00 (2026-08-20) เสนอ "GT-034 DAMAGE-TARGET-AB-001" — **คำสั่ง Panya ชนะเลขนี้** · ข้อเสนอผู้เทสได้เลขใหม่ = **GT-038**

## 🆕⭐ GT-035 DAMAGE-ON-HOSTILE-001: หลอดเลือดของ **hostile ตัวจริง** `0x201F` Tornado Eagle (HP baseline 3,857) ลดตามเลขคณิตของเซิร์ฟเวอร์ไหม  [✅ **PASS เฉพาะชั้น (2) client-observable — คำทำนายครบทั้งสี่ · สองรอบ · แต่ผู้สังเกตสองคน *ไม่ได้* ยืนยันตรงกันครบทั้งสี่ อ่านบล็อก 🔴 ขอบเขตของคำว่า PASS ท้ายใบก่อนอ้างอิง** · จ็อบ `1137/1138/1139` (รอบ 1) + `1140/1141/1142` (รอบ 2) · **2026-08-25 15:04-15:36 (+07:00)** · attended (**รอบ 1 ผู้ช่วยขับ UI เอง · รอบ 2 คุณ Panya ขับเอง**) · จดหมาย `20260825_1550` · บันทึกโดย chief R164
· **คำตอบของทั้งใบ: หลอด/ตัวเลข HP ของ `0x201F` Tornado Eagle บนจอ ลดตามเลขคณิตที่เซิร์ฟเวอร์ส่งจริง — `3857 -> 2893 -> 2893 -> 771` อ่านได้ครบทั้งสี่ค่า**
· `BOOT_COMMIT d856ff4bb8ae498292b276d036b8482a53deaac6` = **คอมมิตของเลน `HYP-PF-038` เอง** · `CODE_DELTA_vs_main = 0` · CANON ก่อน = หลัง **ทั้งสองรอบ** · teardown **exit 0 ทั้งสองรอบ** · วิดีโอ `1138_gt035_*` (รอบ 1) · `1141_gt035r2_*` (รอบ 2)
· **P1 ✅** โมเดลนกถูกวาดจริงที่ `dx100/dy50` — **ไม่ใช่แค่พอเห็น มันใหญ่เต็มจอ** ⇒ ปลด nonclaim ที่ chief ฝังไว้ในซอร์ส `hostile_hp_link_hypothesis.py` (*"nobody has confirmed with their own eyes that a model at this distance is inside the client's model draw distance"*) — ยืนยันแล้ว **สองรอบ สองผู้สังเกต** · **chief R164 ปลดออกจากซอร์สแล้ว** — commit `06b62ab` · **PR โค้ด `pirate-force-server#31`** · 🔴 **สถานะ ณ เวลาที่เขียน: เปิด PR แล้ว ยังไม่ merge รอ gate** ⇒ **ใครจะบูตเลนนี้ต้องเช็คว่า merge แล้วจริงก่อน ห้ามอ่านบรรทัดนี้ว่าอยู่บน `main` แล้ว**
· **P2 ✅ (หัวใจของใบ)** หลอด/เลขของเป้าลงตามบันไดครบสี่ค่า · **P3 ✅** แผง target แสดง `Tornado Eagle` + เลข + หลอดที่ยาวตามสัดส่วนจริง · **P4 ✅** `MISS` ไม่ทำให้หลอดขยับ **และ `MISS` ไม่เงียบ**
· **[วัดแล้ว · เฟรมวิดีโอรอบ 2 · video เริ่ม 15:26:23.065 · ทริกเกอร์แชต t=367.3]** — t368-378 HP `3857` หลอดเต็ม (คร่อม `HIT_WEAK` ที่ 373.3) · t380-402 HP `2893` ~75% (คร่อม `MISS` 385.3 · `AFTER_MISS` 391.3 · `HIT_STRONG` 397.3) · t404 HP `771` ~20% · 🔴 **เรื่อง "6 วินาที" — อ่านให้ครบ:** contact sheet สุ่มทุก **2 วินาที** (`378s`=3857 · `380s`=2893) ⇒ **ขอบที่วัดได้จริงคือ `(4.7, 6.7]` วินาที ไม่ใช่ `6.0` เป๊ะ** · `6.0` คือ **ค่าคงที่ที่เลนนี้ออกแบบไว้** (`HOSTILE_HP_LINK_SPACING_SECONDS = 6.0`) ⇒ **ผลที่วัดได้สอดคล้องกับมัน ซึ่งไม่ใช่ประโยคเดียวกับว่าวัดมันได้** · ผู้สังเกตกะด้วยตาว่า "ประมาณ 6 วิ" ก่อนใครไปวัดวิดีโอ · **ห้ามอ้าง 6.0 เป็นคุณสมบัติของไคลเอนต์**
· 🔴 **สองข้อสรุปมาจากช่วงที่หลอด "ไม่ขยับ" ไม่ใช่ช่วงที่มันขยับ:** ① `3857` นิ่งข้าม `HIT_WEAK` และ `2893` นิ่งข้าม `HIT_STRONG` ⇒ **เฟรมโจมตีอย่างเดียวไม่ขยับหลอด — ตัวที่ขยับคือเฟรม HP เท่านั้น** (สอดคล้องกับโมเดลของ GT-039) ② `2893` นิ่ง 22 วินาทีคร่อมทั้ง `MISS` และ `TARGET_HP_AFTER_MISS` ⇒ **ตัวคุม MISS ทำงาน**
· 🆕 **ครั้งแรกของโปรเจกต์บนเป้าที่ไคลเอนต์ ship ข้อมูล HP มาเอง** (🔴 **ห้ามเขียนว่า "hostile" — ป้ายชื่อขึ้นสีของ *ผู้เล่น* ดู `RE-067`**)**:** เลขดาเมจ `964` **สีแดง ลอยเหนือหัวนก + นกแฟลชขาว** (t373.3) · `MISS!` อ่านออกเต็มคำ **นกไม่แฟลช** (t385.4) · `2122` + แฟลชขาว (t397.3) · เลข **ตรงค่าที่ส่งเป๊ะ ไม่ scale ไม่มีเครื่องหมายลบ**
· 🔴 **ห้ามอ่านผลนี้เกินขอบ — nonclaims ห้าข้อในบล็อก "nonclaims ที่ต้องติดไปกับผล PASS นี้เสมอ" ท้ายใบ ต้องเดินทางไปกับผลทุกครั้ง** โดยเฉพาะ: **ห้ามอ้างผลนี้กับ GT-036 (ไม่มีครึ่งตายในเลนนี้โดยดีไซน์)** และ **คำว่า "hostile" ในชื่อใบยังไม่ถูกพิสูจน์ — ป้ายชื่อนกขึ้นสีเขียว ⇒ `RE-067`**] *(สถานะเดิมก่อนตอบ:* [🟢 **READY-CONDITIONAL — ปลดจาก BLOCKED ON CODE LANE แล้วโดย chief R162 (2026-08-25 ~12:1x +07:00)**
· เลน `HYP-PF-038` **merge เข้า `main` แล้ว**: PR โค้ด **#30** → merge commit `4b36ae8` (เนื้อคือ `d856ff4`)
· **เขียว(Actions run 32811533781 · subset · อ่านทาง `ci-status`)** — ไฟล์คำตัดสิน `ci/d856ff4….json` มี `"conclusion":"success"` และ `"sha"` ตรงกับที่ขอเป๊ะ
· 🔴 **เงื่อนไขที่เหลือ ห้ามข้าม:** รัน `pf_resolve_green_boot.py` เอง แล้ว `BOOT_COMMIT` ที่ได้ **ต้องผ่านห้าข้อในบล็อก "ด่าน 2" + ด่านข้อ 6 (บล็อก R162)** ครบทุกข้อ · **ห้ามเทียบเลข commit ด้วยตา** ให้ตัดสินด้วยเนื้อเหมือนที่ GT-045 เรียนรู้มา (resolver คืนหัว branch ไม่ใช่ merge commit โดยดีไซน์)]*)

**ตัวบล็อกหนึ่งประโยค:** สองครึ่งที่จำเป็นถูกพินอยู่คนละที่ — เลนที่ *spawn* `0x201F` ได้ (arena/P30) ประกาศ `damage` เป็น **nonclaim** ในตัว allowlist เอง (`src/pirateforce_foundation/scenario.py:83`, caps ได้แค่ `("spawn","target")` ที่ `:82`) ส่วนเลนเดียวที่ *ขยับ HP ของเป้า* ได้ (HYP-PF-029) ถูกพินไว้กับ **identity คนละตัว** `0x2001` Navy Transfer (`src/pirateforce_foundation/npc_hp_link_hypothesis.py:422`) พร้อม byte pins ที่คำนวณจาก ladder 100 ⇒ **ยังไม่มีเลนไหนที่ทั้ง spawn 0x201F และพูดเรื่อง damage ได้ในเลนเดียว**

### ทำไมใบนี้เปลี่ยนสถานะ (R159 — เหตุผลเดิม "รอผล GT-034" ตายแล้ว)
1. **GT-034 ตอบแล้ว (ANSWERED, บรรทัด ~499):** ไคลเอนต์ไม่ spawn hostile เองตอน scene-load — ขึ้นก็ต่อเมื่อ**เราส่งไปให้**เท่านั้น ⇒ คำถามที่ใบนี้เคยจอดรอ ปิดไปแล้ว
2. **enabler merge แล้ว (verify รอบนี้):** `0x201F` + HP 3857 + ชื่อ `Tornado Eagle` อยู่บน `main` แล้วสองเส้นทาง
   - `current/pf_login_game_server_v141.py:1869` `V112_MONSTER_ACTOR_ID = 0x201F` · `:1873` `V117_P30_EXACT_HP = 3857` · `:1875` `V119_P30_TARGET_NAME = "Tornado Eagle"` · แถว placement `:1349` = `(30, 31, 1747.5244140625, -7837.69775390625, 931.0413208007812, 'M011_000_000_SP3', 'Tornado Eagle')` — **visual preset ไม่ว่าง** (สำคัญ: actor ที่ preset ไม่ resolve จะไม่มีวันถูกวาด)
   - **เส้น default** `:4292-4304` ยิง `V134_P0_P30_P91_ISOLATED_INITIAL_READY` จาก `make_v112_monster_shop_population_state()` (`:1908`) — วาง P30 ที่ **placement จริง**
   - **เส้น arena** `src/pirateforce_foundation/scenario.py:94 make_p30_target()` — วางแบบ **player-relative** (`scenarios/arena_v1.json` dx 100 / dy 50 / dz 0) และ **ปิดเส้น V134 ทิ้งสำหรับเซสชันนั้น** (`src/pirateforce_foundation/runtime.py:3640-3641`) · label = `ARENA_V1_P30_INITIAL` / `ARENA_V1_P30_MODEL_READY_REAPPLY` (`runtime.py:3648-3650`)
3. **ตัวบล็อกย้ายที่แล้ว:** ไม่ใช่ "ไม่มีทางเอา hostile ขึ้นจอ" อีกต่อไป — เป็น "สองครึ่งถูกพินคนละที่" (ประโยคบนสุด)

### 🎯 ตัวควบคุมเชิงบวกที่มีอยู่แล้ว และ **ข้อจำกัดที่ต้องพกไปทั้งใบ**
รอบ GT-045 (คืนเดียวกับ GT-034 ห่างกัน ~3 ชม.) เราส่งเฟรม `V134_P0_P30_P91_ISOLATED_INITIAL_READY` (517 B) ที่มี P30 = `Tornado Eagle` (ยืนยันด้วย ASCII ในตัวเฟรม) ⇒ **Panya เห็นจุดฟ้าบน minimap ตรงตำแหน่งนั้น + NPC บนจอ**
~~🔴 **แต่ nonclaim ③ ของ GT-034 ยังยืน: ยังไม่เคยมีใครยืนยันด้วยตาว่า "ตัวนก" ถูกวาดบนจอ** — สิ่งที่เห็นคือ**จุดบน minimap** (โมเดลอยู่ไกลเกินระยะวาด)~~
✅ 🆕 **nonclaim ③ ของ GT-034 ปิดแล้ว — ปิดโดย chief R163 (2026-08-25 ~15:xx +07:00)**
ระหว่างรอบ GT-045 v3 (จ็อบ 1122–1136) **คุณ Panya เห็นโมเดลนกจริงบนจอ และป้ายชื่อ `Tornado Eagle` อ่านออก**
· หลักฐาน: `GameClient\Data\ScreenShot\20260825_121434.png` (จดหมาย `20260825_1235` §④ · ยืนยันซ้ำใน `20260825_1300` §③ และ `20260825_1340` §⑤)
⇒ **"ไคลเอนต์วาดโมเดลของ `0x201F` ได้จริง" ไม่ใช่สมมติฐานอีกต่อไป** — เหลือแค่เรื่อง **ระยะ** ซึ่งเหตุผลยังวัดได้เหมือนเดิม:
เส้น default วาง P30 ที่ placement จริง `(1747.5, -7837.7)` ซึ่งไกลจากจุดเกิด V135 มาก
🔴 **แต่ positive control ข้อ 5 ของใบนี้ยังบังคับเหมือนเดิม ห้ามถอด** — การที่เคยเห็นครั้งหนึ่งในเลนหนึ่ง **ไม่ได้แปลว่าจะเห็นในเลนนี้**
· 🆕 **ของแถมที่มากับหลักฐานชิ้นเดียวกัน: ป้ายชื่อนกเป็น *สีเขียว*** ⇒ เป็นที่มาของข้อ (ช) และของใบ `RE-067`
⇒ **นี่คือเหตุผลที่เลนใหม่ต้องวางเป้าแบบ player-relative แบบ `make_p30_target` ไม่ใช่ placement จริง** และเป็นเหตุผลที่ใบนี้บังคับ positive control ด้วยตาก่อนทุกขั้น (ดูชั้น (2))

---

## 🛠 ดีไซน์เลนโค้ดที่ปลดใบนี้ — **HYP-PF-038 HOSTILE-HP-LINK-001** (งานของรอบถัดไป ไม่ใช่รอบนี้)

เขียนไว้ให้ละเอียดพอที่รอบหน้าจะ build ได้โดยไม่ต้อง derive ใหม่ · **ชื่อทุกชื่อข้างล่างเป็นชื่อ "เสนอ" — รอบ build เป็นเจ้าของชื่อจริง** และผู้เทสต้องยืนยันชื่อจริงด้วย `git grep` ก่อนบูตเสมอ (ห้ามใช้ `--help` เป็นหลักฐาน — บทเรียนรอบใหญ่ #7 ข้อ 6)

**① slot ใหม่ = `HYP-PF-038`** — บังคับ ไม่มีทางเลี่ยง:
- `HYP-PF-029` งบเต็ม **3/3** (`docs/HYPOTHESIS_LEDGER.json:2713-2720` — `max_versions: 3`, tracked = `NPC-HP-LINK-001/002/003`) ⇒ ต่อเวอร์ชันที่สี่บนเลนเดิมไม่ได้
- slot สูงสุดที่ใช้ไปแล้ว = `HYP-PF-037` (`src/pirateforce_foundation/app.py:216`) ⇒ ตัวถัดไปคือ **038**
- `HYP-PF-026` ก็ต่อไม่ได้: dispatcher ปฏิเสธ **identity ของผู้เล่นที่เลือก** ที่ไม่ใช่ canonical smoke (`runtime.py:2509 damage_hp_link_hypothesis_identity_not_pinned_no_reply`) และ pins ของมันคำนวณจาก `0x2001`/ladder 100

**② target identity = `0x201F`** (ไม่ใช่ `0x2001`) · **performer = ตัวผู้เล่นเอง** พินที่ canonical smoke `0x10010001:0` เหมือนทุกเลนข้างเคียง
- เหตุผลที่ performer ต้องเป็นผู้เล่น: หนึ่งข้างของเฟรม `CHitResult` ต้องเป็นผู้เล่น ไม่งั้นตัวกรอง visibility หกชั้นที่ `0x43FEF0` ไม่วาดอะไรเลย (บันทึกไว้แล้วที่ `npc_hp_link_hypothesis.py:429-435`)
- 🔴 ที่ HYP-PF-029 พินเป้าไว้เป็น `0x2001` **ไม่ใช่การ์ด runtime** แต่เป็น module constant (`:422`) + pin ตอน resolve เทียบตาราง placement แช่แข็ง (`:480-487` refusal `target_placement_drifted_from_the_pin`) ⇒ **เปลี่ยนเป้า = byte pins ทั้งชุดใช้ไม่ได้ทั้งชุด** = เลนใหม่ ไม่ใช่ flag ใหม่

**③ ladder มาจากไหน — `3857` ไม่ใช่ `100`**
- ที่มาของ 3857 = `V117_P30_EXACT_HP` (`pf_login_game_server_v141.py:1873`) ซึ่งเป็น **HP baseline ที่ ship มากับ client** (`STANDARD_MOB` lvl 27) — **ไม่ใช่กฎของเซิร์ฟเวอร์ต้นฉบับ** (ดู nonclaims)
- โครง ladder ให้ isomorphic กับแผนแม่ (`npc_hp_link_hypothesis.py:537-551`) แต่ **ตัดครึ่งตายทิ้ง** (เหตุผลที่ ④)
- **เลขความเสียหายต้องออกจากเครื่องคิดเลขของเลนเอง** (`compute_npc_hp_link_damage_wire` + `apply_hit_to_balance` + `replay_..._balance_ladder` แบบเดียวกับ `:592-657`) และต้อง **re-derive ทุกครั้งที่ compose** — ไม่ตรง = `hp_arithmetic_not_reproducible` และไม่มีไบต์ออก
- 🔴 **ข้อบังคับเรื่องสายตา (ของใหม่ที่แผนแม่ไม่ต้องคิด):** `-63` บนสระ 3,857 = **1.6% ของหลอด — ตาคนอ่านไม่ออก** ⇒ ค่ากลางของ ladder ต้องเป็นสัดส่วน**ที่เห็นได้ชัด** (ข้อเสนอ chief: ขั้นแรกลงมาราว **60%** ขั้นสองราว **20%** ของ 3,857) · ถ้าสูตรของเลนให้เลขที่เล็กเกินกว่าจะเห็น ให้รอบ build **พูดออกมาตรง ๆ ในรายงาน** แล้วเลือกโปรไฟล์ผู้โจมตีที่ให้เลขใหญ่พอ — **ห้ามแต่งเลขนอกเครื่องคิดเลข**
- 🟢 ตัวคุม `MISS` (damage 0 + เฟรม actor ถัดไป **ไบต์เหมือนเฟรมก่อนหน้าเป๊ะ**) **ต้องมี** เหมือนแผนแม่ (`:80-85`) — sweep ที่ทุกเฟรมลดหลอดแยกไม่ออกว่าไคลเอนต์อ่านเลขคณิตของเราหรือเล่นแอนิเมชันของมันเอง

**④ ห้ามแตะพื้น 0 ในใบนี้ — หนึ่งใบหนึ่ง claim**
แผน 7 เฟรม (spacing 6.0 s ตามคำเคาะ Panya 2026-08-20 ที่ `:512-521` ⇒ ~36 วิทั้งชุด):
```
TARGET_SPAWN             balance 3857   alive · placed player-relative · name bit ON
HIT_WEAK                 announce       เลขจากสูตรของเลน
TARGET_HP_AFTER_WEAK     balance B1     คำถามหลักของทั้งใบอยู่เฟรมนี้
MISS                     announce 0     ตัวคุม
TARGET_HP_AFTER_MISS     balance B1     ไบต์เหมือนเฟรมบนเป๊ะ
HIT_STRONG               announce       เลขจากสูตรของเลน
TARGET_HP_AFTER_STRONG   balance B2     B2 ต้องมากกว่า 0 เสมอ
```
🔴 **ไม่มีเฟรม hp = 0 · ไม่มี death timer · ไม่มี dying latch ในเลนนี้เลย** — การ์ด lethal-field ของแผนแม่ (`:131-132`, `:559-568`) จึงไม่มีวันถูกยิง · ครึ่ง "ตาย" เป็น claim ของ **GT-036** และต้องเป็นเวอร์ชันถัดไปของ `HYP-PF-038` ไม่ใช่ใบนี้

**⑤ geometry — เหตุผลที่ทั้งใบจะได้ผลหรือเสียเปล่า**
`TARGET_SPAWN` ต้องวาง `0x201F` แบบ **player-relative** ตามท่าที่พิสูจน์แล้วของ `make_p30_target` (`scenario.py:97-98`, `arena_v1.json` dx 100 / dy 50 / dz 0 · ป้าย ledger `GEO-PF-001 harness_only`) — **ห้ามใช้ placement จริง** เพราะนั่นคือสาเหตุที่ GT-045 ได้แค่จุด minimap
🔴 และเลนต้อง **suppress เส้นประชากร V134 P0/P30/P91 ทิ้งสำหรับเซสชันของตัวเอง** (ท่าเดียวกับ `runtime.py:3640-3641`) ไม่งั้น `0x201F` มีแหล่งกำเนิดสองแหล่งในบูตเดียว = แยกไม่ออกว่าตัวไหนของใคร = NO-RESULT โดยโครงสร้าง

**⑥ กติกาบ้านที่ต้องติดมากับเลน (เหมือนทุกเลนข้างเคียง)**
- `production_allowed = False` ในโมดูล **และ**ในไฟล์ scenario
- **opt-in flag เดียว** (เสนอ `--hostile-hp-link-hypothesis-scenario`) + scenario allowlist แบบ exact-tree (คีย์เกิน/ขาดหนึ่งตัว = ปฏิเสธ)
- **one-shot** ต่อ connection · ยิงซ้ำ = `..._already_sent_no_reply`
- trigger = แชต **ascii 12 ตัวเป๊ะ** (ทรง 34 ไบต์เดิมที่ทุกเลนใช้ร่วมกัน)
- **ทุกการปฏิเสธมีชื่อ ไม่มี fallback เงียบ**
- ต้องมาพร้อม **`tools/verify_*` + `tools/pf_*_headless_replay.py`** เหมือนพี่น้อง — เพราะ **นั่นคือที่เดียวที่ named refusal ถูกมองเห็นได้** (ดูชั้น (1) ข้อ 🔴)
- ledger: append entry ใหม่ ไม่ขยับ entry เก่า ไม่เปลี่ยน index เก่า · re-pin canonical hash

---

## objective (claim เดียวที่ใบนี้พิสูจน์)
**เมื่อเซิร์ฟเวอร์ส่งเลขคณิต HP ของตัวเองมาให้ hostile ตัวจริง `0x201F` Tornado Eagle ที่มี HP baseline 3,857 หลอดเลือดของ "เป้า" บนจอลดตามค่านั้นจริงหรือไม่**
🔴 **ที่ใบนี้ไม่ได้ถาม:** มันตายไหม (GT-036) · ดรอปอะไรไหม (คาเวียตรอบ 118 ใต้ GT-036) · มันตอบโต้ไหม (`0x201F` เป็น retaliate-only — เราไม่ได้ตีมันจริง เราแค่**บอก**ว่ามันโดน)
📎 **บริบทที่ทำให้ claim นี้แคบและวัดได้:** GT-039 ✅ PASS แล้วว่าหลอดของเป้าลด `100 -> 37 -> 0` ตามที่เซิร์ฟเวอร์บอก — **บน `0x2001` และ ladder สังเคราะห์ 100** ⇒ ใบนี้ถามข้อเดียวที่เหลือ: **ท่าเดียวกันบน identity ตัวจริง + HP baseline ตัวจริง**

## คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)
- **P1 [คำทำนาย]** โมเดลนกถูกวาดบนจอที่ ~111 หน่วยจากตัวผู้เล่น (dx 100 / dy 50) — **ยังไม่เคยมีใครเห็น `0x201F` บนจอมาก่อน** จึงเป็นคำทำนายจริง ๆ ไม่ใช่ของแถม
- **P2 [คำทำนาย · หัวใจของใบ]** หลอด/ตัวเลขของเป้าลงจาก `3857` เป็น `B1` ที่เฟรม `TARGET_HP_AFTER_WEAK` และ **ไม่ขยับ**ที่เฟรมเลข (`HIT_WEAK`/`HIT_STRONG`) — ถ้าขยับที่เฟรมเลข = **หักล้างผลรอบ 83 ("ไคลเอนต์ไม่ลบเลขเอง") ทั้งเลน** จดละเอียดที่สุด
- **P3 [คำทำนาย]** แผง target แสดงตัวเลข HP อ่านได้ (GT-032 เห็น `HP 100/100 Lv.1` บนแผง target ของ `0x2001` มาแล้ว) ⇒ คาดว่าอ่าน `3857/3857` ได้ก่อนยิง
- **P4 [ตีความ]** `MISS` ไม่ทำให้หลอดขยับ (ตัวคุมทำงานเหมือน GT-039)

---

### 🔴 ก่อนบูต — สองด่าน **ต้องผ่านทั้งสองด่านเท่านั้น**

**ด่าน 1 — resolve commit เขียว (รันเครื่องมือ ไม่ใช่ก๊อป SHA · ท่าเดียวกับ GT-041/034/045)**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\Pirate Force\pirate-force-server" --fetch
```
🔴 **เครื่องหมายคำพูดรอบ path เพิ่มโดย R162** — โฟลเดอร์จริงมีช่องว่างในชื่อ (`Pirate Force` · `ATTENDED_SESSION_RUNBOOK.md:31`) ⇒ ไม่ครอบแล้ว PowerShell ตัดคำ resolver ได้ path ผิด
- รันจากโฟลเดอร์ `pf_bridge` · **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` (detached HEAD ถูกแล้ว — บูต*คำตัดสิน* ไม่ใช่ branch)
- **exit 3** + `BOOT_COMMIT: NONE` ⇒ ห้ามบูต จดว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · **exit 2** = พาธผิด/git ล้ม
- บรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ จดลงผลเสมอ

**ด่าน 2 — ยืนยันห้าข้อกับ `<SHA>` ที่จะบูตจริง (ข้อ 3/4/5 คือด่านกัน "บูตเลนเก่า")**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "hostile-hp-link-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/hostile_hp_link_hypothesis_p30_sweep.json
$LASTEXITCODE
git grep -n -e "0x201F" -e "3857" <SHA> -- src/pirateforce_foundation/hostile_hp_link_hypothesis.py
git grep -n "HYP-PF-038" <SHA> -- docs/HYPOTHESIS_LEDGER.json src/pirateforce_foundation/hostile_hp_link_hypothesis.py
```
1. ไฟล์คำตัดสินมี `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ (`success` = subset บน Actions ไม่ใช่ gate เต็ม)
2. `git grep` เจอ flag จริง — **ห้ามใช้ `--help` เป็นหลักฐาน** (คืน 0 บรรทัดผ่านสะพาน)
3. บรรทัดถัดจากคำสั่งพิมพ์ `0` (ไฟล์ scenario มีอยู่ใน commit นั้นจริง) — 🆕 **R162 เปลี่ยนรูปคำสั่งข้อนี้**
   จากเดิมที่ใช้ `&& echo SCENARIO_PRESENT` เพราะ `&&` **ไม่ใช่ตัวคั่นคำสั่งบน PowerShell 5.1** (`The token '&&' is not a valid statement separator in this version`)
   ⇒ ด่านเดิมอาจตายกลางคันบนสะพานโดยไม่มีใครรู้ · รูปใหม่ใช้ `$LASTEXITCODE` ซึ่งรันได้ทั้ง PS 5.1 และ PS 7
   *(ใบอื่นในไฟล์นี้ยังใช้รูปเดิมอยู่ — chief จะไล่แก้เป็นงานแยก ไม่ใช่รอบนี้ · ถ้าผู้เทสเจอ error นี้ที่ใบไหน ให้จดไว้ในผล)*
4. เจอทั้ง `0x201F` และ `3857` ในโมดูลของเลน — **ถ้าเจอ `0x2001` แทน แปลว่ากำลังจะบูตเลนแม่ ห้ามบูต**
5. เจอ `HYP-PF-038` ทั้งใน ledger และในโมดูล
- **ไม่ครบห้าข้อ = ห้ามบูต** ใบนี้อยู่ BLOCKED ต่อ **ปล่อยไว้ที่เดิม ห้ามลบ ห้ามย้าย** แล้วให้ผู้เทสไปทำใบอื่น
- 🔴 **ชื่อ flag/ไฟล์/โมดูลข้างบนเป็นชื่อ "เสนอ" ของ R159** — ถ้ารอบ build ใช้ชื่ออื่น **ให้เชื่อชื่อจริงในผล PR แล้วแก้ห้าคำสั่งนี้ตามชื่อจริง** อย่าเดา

### db (สำเนาเสมอ ห้ามเปิด canonical)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-035_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt035.sqlite3
```
- เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง**
- pre-flight บนสำเนา (อ่านอย่างเดียว `mode=ro`) — เลนพินที่ **canonical smoke identity `0x10010001:0` ชื่อ `Arena01`** (`docs/COMMAND_HANDOFF.md:333`):
  `SELECT id,name FROM characters WHERE name='Arena01' AND deleted_at IS NULL;`
  ⇒ **ไม่เจอ = หยุด รายงานกลับ ห้ามสร้างตัวละครสดเพื่อใบนี้**
- 🔴 **เลือกตัวละครผิด = ไม่มีไบต์ออกเลย** (ท่าบ้านนี้: เห็นไบต์ตรง pin เป๊ะ หรือไม่เห็นเลย) — และการ์ดนั้น**ไม่พิมพ์อะไรลงคอนโซล** (ดูชั้น (1))
- ตำแหน่งตัวละคร **รีเซ็ตกลับจุดเกิดทุกบูต** เพราะรอบก๊อป DB ใหม่ — เป้าวางแบบ player-relative ใบนี้จึงไม่พังเพราะเรื่องนี้

### server args (เป๊ะ · รันจาก working tree ของ checkout ที่ผ่านห้าข้อ)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt035.sqlite3 --hostile-hp-link-hypothesis-scenario scenarios\hostile_hp_link_hypothesis_p30_sweep.json
```
🔴 **บรรทัด `PYTHONPATH` เพิ่มโดย R162 หลัง `pf-adversary` วัดว่าคำสั่งเดิม *บูตไม่ขึ้น*** — แพ็กเกจอยู่ใต้ `src/` และ repo ไม่มี `pyproject.toml`/`setup.py`/`conftest.py` ⇒ `ModuleNotFoundError: No module named 'pirateforce_foundation'` · เทมเพลตบูตเก่าตั้ง `PYTHONPATH` ให้อยู่แล้ว (เช่น `staged\090_gt009_boot.ps1:53`) แต่บล็อกในใบนี้ลอกมาไม่ครบ
- 🔴 **ต้องใส่ `--db` ชี้สำเนาเสมอ** — **แก้ R162:** ประโยคเดิม ("ถ้าลืมจะไปใช้ `state\test_arena_v1.sqlite3` เป็น default") **ล้าสมัยแล้ว** ปัจจุบัน `app.py` ปฏิเสธแข็ง: `--hostile-hp-link-hypothesis-scenario requires an explicit existing --db` ⇒ ลืมแล้ว **บูตไม่ขึ้นเลย** ไม่ใช่บูตผิดไฟล์เงียบ ๆ
- 🔴 **บูตเลนเดียว ห้ามรวมเลนอื่น** ถึงแม้ allow-list (คำเคาะ Panya 1831 §① · ขยาย 2120 §②) จะยอมให้รวมได้แล้ว — ใบนี้ตัดสินด้วยตา ถ้ามีเลนอื่นวิ่งด้วยจะแยก "ใครวาด/ใครขยับหลอด" ไม่ออก = NO-RESULT
- หัวหน้าต่าง console ของ server จะขึ้น mode ของเลนนี้ — ใช้เช็คว่าบูตถูกโหมด

### steps (บูตเดียว · ~10 นาทีในเกม · **อัดวิดีโอตลอดช่วงถือ `LOCK_GAME`**)
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบตามบล็อก db · **เริ่มอัดวิดีโอก่อนเปิด client**

1. **เปิด server ก่อน client เสมอ** — เช็ค `Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = **0** ก่อนเปิด client · client ที่บูตโดยไม่มีเซิร์ฟเวอร์ **ตายเองใน ~3.5 นาที**
   🔴 **ถ้าต้องฆ่า client กลางคัน ต้องรีสตาร์ต server ก่อนเปิด client ใหม่เสมอ** (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่ "connecting" ตลอดกาล)
2. เปิด client (`Invoke-CimMethod Win32_Process Create`) → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร → เลือก **`Arena01`** → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**) · ปุ่มไม่ติดให้ใช้ `Return` (บทเรียนรอบใหญ่ #12 ข้อ 1)
3. เข้าแมพ → **ถ่าย H0 ทันทีก่อนแตะอะไร** ให้เห็น X/Y บน HUD + นาฬิกาบนจอ

3b. 🆕🔴 **ด่านตัวควบคุมกฎกล้อง — ขั้นบังคับ ราคา ~30 วินาที ทำก่อนข้ออื่นทั้งหมด**
   **เหตุผล:** กฎกล้องฉบับ R163 (คลิกขวาลาก = ไม่ยิงทริกเกอร์) ยืนอยู่บน **คำให้การของผู้เทสหนึ่งรอบ ไม่ใช่การวัดบนสาย**
   ไม่มีใครเคยวัดท่านี้เทียบ `[G<]` สักครั้ง (`evidence_screens\` มี control ของ `Q`/`E` ครบ แต่ **ไม่มีของคลิกขวาลากแม้แต่ภาพเดียว**)
   ⇒ ถ้ากฎผิด **one-shot ของเลน ground-loot จะไหม้ตั้งแต่ตอนส่องกล้อง** และไม่มีใครวินิจฉัยได้ว่ารอบตายเพราะอะไร
   a. เข้าแมพแล้ว **ห้ามแตะคีย์บอร์ดเลยแม้แต่ปุ่มเดียว**
   b. **คลิกขวาค้างลากเมาส์หมุนกล้องรอบตัว 360° ช้า ๆ** (นี่คือขั้นเดียวที่ทำ)
   c. **อ่าน server console:** มีบรรทัด `[G<] TargetPosVital` ออกมาไหม
   | ผลที่อ่านได้ | แปลว่า | ทำต่อยังไง |
   |---|---|---|
   | **0 เฟรม** | 🟢 **กฎ R163 ได้หลักฐานชั้น wire เป็นครั้งแรก** | จดลงผล แล้วเดินข้อ 4 ต่อตามปกติ |
   | **มี ≥1 เฟรม** | 🔴🔴 **กฎ R163 ผิด — คลิกขวาลากก็ยิงทริกเกอร์** | **หยุดรอบทันที ห้ามเดินต่อ** (one-shot ไหม้ไปแล้ว) · จดจำนวนเฟรม + เวลา · รายงาน ⇒ chief ต้องถอนกฎทั้งฉบับและแก้ทุกใบกลับ |
   🔴 **ผลของด่านนี้ต้องอยู่ในช่อง `result` เสมอ ไม่ว่าออกทางไหน** — นี่คือด่านที่ทำให้กฎกล้องหยุดเป็นคำเล่าลือ
   *(ด่านนี้ไม่กินงบเวอร์ชัน: ไม่เปลี่ยน scenario ไม่เปลี่ยนไบต์ เป็นการอ่านอย่างเดียว)*
4. 🔴 **ห้ามกด `W/A/S/D` และห้ามกด `Q`/`E` เด็ดขาด** — 🆕 **ถ้อยคำฉบับแก้ R163 (2026-08-25 ~15:xx +07:00)**
   **สิ่งที่ยิง `TargetPosVital` คือ "การเปลี่ยนทิศหันของตัวละคร" ไม่ใช่ "การขยับกล้อง"** (ผู้เทสแยกออกมาเองในรอบ 4 ของ GT-045 v3)
   ⇒ 🟢 **คลิกขวาค้างลากเมาส์ = ปลอดภัย ใช้ได้เต็มที่ตลอดรอบ ไม่ยิงอะไรออกสาย** — เอากล้องไปส่องมุมไหนก็ได้ ไม่ต้องขออนุญาต
   ⇒ 🔴 `Q`/`E` **หันตัวละคร** (กล้องแค่แพนตาม) ⇒ ยิง · `W/A/S/D` เดิน ⇒ ยิง
   ~~เดิมเขียนว่า "การหมุนกล้องยิง TargetPosVital เองได้"~~ — **ผลถูกโดยบังเอิญ เหตุผลผิด · ดูตารางเต็มใน PLAYBOOK**
   · เลนนี้ยิงด้วยแชต ไม่ได้ยิงด้วย TargetPos จึงไม่มีเหตุผลใดที่ต้อง **ขยับตัว** · การขยับ/หันตัวคือความเสี่ยงล้วน ๆ
   · แต่ **การส่องกล้องไม่ใช่ความเสี่ยง** และใบนี้ต้องการให้ส่องหาโมเดลนกให้เจอ (ข้อ 5) ⇒ **ส่องได้เต็มที่**
   · 🔴 **ตัวอักษรที่พิมพ์ตอนช่องแชตไม่โฟกัส = hotkey** และมี toggle `[localplayer+0x420]` (input command `0x27`) ที่ **ปิดเลขดาเมจทั้งจอได้เงียบ ๆ โดย wire เหมือนเดิมทุกไบต์** ⇒ ใช้ client ที่เพิ่งเปิดใหม่ (default ON) และห้ามพิมพ์นอกช่องแชตที่ยืนยันโฟกัสแล้ว
5. 🟢 **POSITIVE CONTROL — ขั้นบังคับ ทำก่อนยิงเสมอ ห้ามข้าม (เหตุ: GT-034 nonclaim ③)**
   a. หา **โมเดลนก** ด้วยตา — เป้าอยู่ที่ผู้เล่น `+100X / +50Y` ⇒ ราว 111 หน่วย ควรอยู่ในระยะวาด
      · 🆕 **แก้ R163:** ถ้ามุมกล้องแรกเข้าไม่เห็น ⇒ **คลิกขวาค้างลากเมาส์ส่องหาได้ ไม่จำกัดจำนวนครั้ง**
        (คลิกขวาลากไม่หันตัวละคร ⇒ ไม่ยิงอะไร) · 🔴 **แต่ยังห้าม `Q`/`E` และห้าม `W/A/S/D`** ตามข้อ 4
        ~~เดิมเขียนว่า "อนุญาตให้หมุนกล้องได้เฉพาะขั้นนี้ขั้นเดียว"~~ — ข้อจำกัดนั้นเกิดจากถ้อยคำที่ผิด ถอนแล้ว
        🔴🔴 **แต่ยังต้องจดอยู่ ห้ามข้าม: จดว่าส่องกล้องกี่ครั้ง เวลาไหน (เทียบนาฬิกาบนจอ)**
        ฉบับแรกของ R163 เขียนว่า "ไม่ต้องจดว่าหมุน" — **`pf-adversary` จับได้ว่านั่นคือการลบร่องรอยเดียวที่จะพิสูจน์กฎใหม่ผิด**
        ⇒ ถ้ารอบนี้จบด้วย one-shot ที่ไหม้โดยไม่มีใครอธิบายได้ **บรรทัดที่จดไว้นี้คือสิ่งเดียวที่จะบอกว่าเกิดอะไรขึ้น**
   b. **ถ่าย H1**: ให้เห็น **ตัวนก** เต็มตัวในภาพ — **จุดบน minimap ไม่นับเป็นการยืนยันโมเดล**
   c. **คลิกซ้ายเลือกมันหนึ่งคลิก** → **ถ่าย H2**: แผง target ต้องอ่านออกว่า **ชื่ออะไร · HP เท่าไร** (คาด `Tornado Eagle` · `3857/3857`)
   d. 🔴 **ถ้า (b) ไม่ได้ — คือหาโมเดลไม่เจอ — หยุดตรงนี้ ห้ามยิงทริกเกอร์** · ออกจากเกม รายงานเป็น **NO-RESULT (positive control ล้ม)** · จดทุกทิศที่กวาดแล้ว + HUD X/Y · **ห้ามเขียนว่า "หลอดไม่ลด"** เพราะไม่เคยมีหลอดให้ดู
6. **ยิงทริกเกอร์:** เลื่อนเมาส์ไปเหนือแผงแชต → คลิกแถบ input (หรือกด `Return`) → **ถ่ายยืนยันว่าข้อความอยู่ในช่องแล้ว** → พิมพ์สตริง **ascii 12 ตัวอักษรเป๊ะ** → `Enter` **ในการเรียกครั้งเดียวกัน**
   🔴 **สั้นกว่า 12 ตัว เฟรมถึงเซิร์ฟเวอร์แต่เงื่อนไขไม่เข้า และ "ล้มแบบเงียบ"** — ไม่มี sweep ออกและ**ไม่มีบรรทัดบอกด้วย** (บทเรียนรอบใหญ่ #8 ข้อ 5)
7. **ยืนนิ่งดูจนจบชุด (~36 วิ) ห้ามแตะอะไร** — เป้ายังถูกเลือกอยู่ ⇒ ตาอยู่ที่ **แผง target** เป็นหลัก และเหลือบดู**หลอดลอยเหนือหัวเป้า**ด้วย
   · ถ่ายภาพทุกครั้งที่เห็นตัวเลขเปลี่ยน: **H3** (หลัง `TARGET_HP_AFTER_WEAK`) · **H4** (ช่วง `MISS`/`TARGET_HP_AFTER_MISS`) · **H5** (หลัง `TARGET_HP_AFTER_STRONG`)
   · 🔴 **เลขลอย** (เลขความเสียหาย) อายุสั้นกว่า cadence ของภาพนิ่ง ⇒ **"ไม่ติดภาพ" = non-observed ไม่ใช่ absent** — วิดีโอคือหลักฐานของเลขลอย ไม่ใช่ภาพนิ่ง
8. **ถ่าย H6** ภาพสุดท้ายก่อนออก (HUD + นาฬิกา) → ออกจากเกม: **X** มุมขวาบน (ตรวจก่อนว่าหน้าต่างแอปตัวเองไม่บังปุ่ม X) → dialog ยืนยัน → ปุ่มซ้าย
9. ปิด server · เก็บ **raw GAME log ทั้งไฟล์ + console out/err ห้ามลบ** → `PRAGMA integrity_check;` บนสำเนา
10. **teardown เสมอ แม้เลิกกลางคัน แม้รอบจบเพราะคนเลิกเล่น** — boot stamp เกิน **420 นาที** template ปฏิเสธ exit 12 (เพดานยกจาก 180 เมื่อ 2026-08-20 · `TEMPLATE_teardown_generic.ps1:135`) · แท่นที่ถูกทิ้งข้ามชั่วโมงใช้ `staged\TOOL_stop_stale_server.ps1`
11. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม

---

## 🔴 pass criteria — สองชั้น แยกกันเด็ดขาด ห้ามอ้างชั้นหนึ่งแทนอีกชั้น

### ชั้น (1) wire/DB — **ผลิตแบบ headless ได้ ไม่ต้องใช้สายตาคนหน้าจอ**
- **เฟรมที่ต้องเห็นใน server console (ตัวพิมพ์เดียวคือ `[G>] <label> (N bytes)` ที่ `current/pf_login_game_server_v141.py:7762`) — ครบ 7 ใบ เรียงตามนี้ ห่างกัน 6.0 วิ:**
  `HYP_PF_038_HOSTILE_HP_LINK_TARGET_SPAWN` → `..._HIT_WEAK` → `..._TARGET_HP_AFTER_WEAK` → `..._MISS` → `..._TARGET_HP_AFTER_MISS` → `..._HIT_STRONG` → `..._TARGET_HP_AFTER_STRONG`
  · **เห็นชื่ออื่น (เช่น `HYP_PF_029_NPC_HP_LINK_*` หรือ `ARENA_V1_P30_*`) = บูตผิดไฟล์/ผิดเลน — ยกเลิกรอบ**
- **identity ที่ต้องปรากฏในเฟรม (ตรวจจาก hexdump ใน raw GAME log — นี่คือหัวใจที่แยกใบนี้จาก GT-039):**
  - `0x201F` เป็น identity 64 บิต ⇒ ไบต์ **`1F 20 00 00 00 00 00 00`** ต้องอยู่ใน **ทุกเฟรมของ sweep** ทั้งฝั่ง actor-entry และฝั่ง `CHitResult`
  - 🔴 **`01 20 00 00 00 00 00 00` (`0x2001`) ต้องไม่ปรากฏเลยสักเฟรม** — เจอ = บูตเลนแม่ ยกเลิกรอบ
  - เฟรม `TARGET_SPAWN` ต้องมี ASCII **`Tornado Eagle`** และ preset **`M011_000_000_SP3`** อยู่ในตัวเฟรม
  - ค่า `max_hp` ต้องเป็น **3857** (`0x0F11` ⇒ ไบต์ `11 0F ...` ตามความกว้างฟิลด์จริงของ NPCAttr) และ `current_hp` เดินตาม ladder
- **พิกัดของ `TARGET_SPAWN`** decode f32 แล้วต้อง = ตำแหน่งผู้เล่น `+100X / +50Y / +0Z` (เทียบที่ความละเอียด f32) — **ไม่ใช่** `(1747.52, -7837.70, 931.04)` ซึ่งเป็น placement จริง (ถ้าเป็นค่าหลัง = เลนวางเป้าผิดท่า ⇒ positive control จะล้มแน่นอน จดแล้วยกเลิกรอบ)
- 🔴 **"เงียบ" ไม่เท่ากับ "ปฏิเสธตามชื่อ" — กฎนี้ยกมาจากคาเวียตของ GT-036 และรอบนี้มันแรงกว่าเดิม:**
  - refusal ทุกตัวของเลนตระกูลนี้ถูก append ลง `self.events` ซึ่งเป็น **list ในหน่วยความจำ ไม่มีบรรทัดไหนใน `src/` พิมพ์มันออกคอนโซล** (สืบแล้ว R120/R123 · `runtime.py:1819`) ⇒ **ในรอบ attended ผู้เทสมองไม่เห็น named refusal เลยแม้แต่ตัวเดียว**
  - ⇒ สิ่งที่สังเกตได้ในรอบ attended มีแค่ **"มีไบต์ออก" / "ไม่มีไบต์ออก"** · **ห้ามเขียนในผลว่า "ถูกปฏิเสธด้วย X" จากการที่จอเงียบ** ให้เขียนว่า **"เงียบ: ไม่มีบรรทัด `[G>]` เลย"** แล้วจบ
  - **named refusal พิสูจน์ได้ที่เดียว = ฝั่ง headless** ⇒ ✅ **R162 ส่งมอบแล้ว: `tools\pf_hostile_hp_link_headless_replay.py`**
    รันที่ไหนก็ได้ ไม่ต้องมี DB ไม่ต้องมีเกม: `py -3 tools\pf_hostile_hp_link_headless_replay.py --player-position=<x>,<y>,<z>`
    ⇒ พิมพ์ **ชื่อ refusal ทุกตัวที่มันขับจริง** + **พิกัดที่เฟรม `TARGET_SPAWN` วางตัวนกไว้ (decode กลับจากไบต์จริง)** + ladder + ขนาดทุกเฟรม · exit 0 = ผ่านทุกด่าน
    🔴 **ประโยชน์ตรงของใบนี้:** รันด้วยพิกัดที่ผู้เทสจะยืนจริง **ก่อนบูต** ⇒ ถ้ารอบจบด้วย "ไม่เห็นตัวนก" เรามีเลขพิกัดที่เฟรมส่งจริงอยู่ในมือแล้ว ⇒ **แยก "อยู่นอกระยะวาด" ออกจาก "เฟรมวางผิดที่" ได้ทันที ไม่ต้องเดา**
- **DB (🔴 อ่านให้ดี — ต่างจาก GT-034):**
  - **HP ไม่มีคอลัมน์ในฐานข้อมูลเลยแม้แต่ช่องเดียว และเลนนี้ไม่เพิ่มให้** (ยืนยันแล้ว: ค้น `migrations/` ทั้งโฟลเดอร์ = 0 hit สำหรับ `hp`/`health`) — balance อยู่ในเลขคณิตของโมดูลตลอดอายุหนึ่ง sweep แล้วตายไปกับมัน
  - ⇒ เกณฑ์ที่ถูกคือ **schema ไม่ใช่ file hash**: หลังรอบ ตรวจบนสำเนาว่าไม่มีตารางไหนโผล่คอลัมน์ hp ขึ้นมา
  - 🔴 **`RUN_SHA_BEFORE == RUN_SHA_AFTER` ใช้กับใบนี้ไม่ได้** (มันเป็นเกณฑ์ของ GT-034 ซึ่งเป็นเลน read-only โดยโครงสร้าง) — ใบนี้เป็น full-flow login ⇒ **สำเนาต้องขยับ** เพราะ `sessions`/`lease_generation`
  - เกณฑ์ DB จริงของใบนี้: `sessions` — `count(*) WHERE selected_character_id IS NOT NULL` **+1 ต่อการเข้าเกมหนึ่งครั้ง** · `lease_generation` **ไม่ถอยหลัง** · `PRAGMA integrity_check` = `ok` · **sha256 canonical ก่อน-หลังตรง `CANON_SHA.txt` ทั้งสองครั้ง** (canonical ไม่ถูกเปิดเลยตลอดรอบ)
- **ชั้นนี้ตอบไม่ได้:** จอวาดอะไร · หลอดขยับหรือไม่ · เห็นตัวนกหรือไม่ · **การมีเฟรมออกไม่ได้พิสูจน์ว่าไคลเอนต์อ่านมัน**

### ชั้น (2) client-observable — **ต้องมีคนอยู่หน้าจอ ปิดด้วยรอบ unattended ไม่ได้เด็ดขาด**
**หลักฐานบังคับ:** วิดีโอต่อเนื่องคลุมตั้งแต่ก่อนยิงทริกเกอร์ถึง +10 วิหลังเฟรมสุดท้าย · ภาพ **H0–H6** ทุกใบเห็นนาฬิกาบนจอ · **จด sha256 ของไฟล์ภาพ/วิดีโอทุกไฟล์**

🟢 **POSITIVE CONTROL มาก่อนทุกอย่าง (ประตูของชั้นนี้ทั้งชั้น):**
| ผลของ control | ใบอ่านต่ออย่างไร |
|---|---|
| **เห็นโมเดลนกเต็มตัว (H1) + แผง target อ่านชื่อ/HP ได้ (H2)** | 🟢 ประตูเปิด — คำตอบเรื่องหลอดอ่านได้เต็มปาก **ทั้งบวกและลบ** |
| **เห็นแค่จุดบน minimap ไม่เห็นตัว** | 🔴 **NO-RESULT — ห้ามยิงทริกเกอร์ ห้ามอ่านเป็นผลลบใด ๆ** · นี่คือสถานการณ์เดียวกับ GT-034 nonclaim ③ เป๊ะ ๆ · จดเป็นผลเรื่อง**ระยะวาด/เงื่อนไขเรนเดอร์ของ `0x201F`** ซึ่งเป็นข้อมูลใหม่ที่มีค่าในตัวเอง |
| **ไม่เห็นอะไรเลย ทั้งจุดทั้งตัว** | 🔴 **NO-RESULT (regression)** — ตรวจห้าข้อก่อนบูต · ตรวจว่า `TARGET_SPAWN` ออกจริงไหมในคอนโซล · แล้วรันใหม่ · **ห้ามเขียนว่า "ไคลเอนต์ไม่วาด"** |

**คำถามที่ต้องตอบเป็นภาษาคน (ตอบทุกข้อ ไม่ว่าผลออกทางไหน):**
- **(ก)** เห็นโมเดลนกไหม · ทิศไหนเทียบทิศกล้องแรกเข้า · ระยะประมาณเท่าไร · **หมุนกล้องไปกี่องศาถึงเห็น (ถ้าหมุน)**
- **(ข)** แผง target ก่อนยิง อ่านได้ว่าอะไร (ชื่อ · ตัวเลข HP · Lv.) — ตรงคำทำนาย `Tornado Eagle 3857/3857` ไหม
- **(ค)** ⭐ **หลอด/ตัวเลขของเป้าลงจาก `3857` เป็นค่าใหม่ที่เฟรม `TARGET_HP_AFTER_WEAK` หรือไม่ · ค่าที่อ่านได้บนจอคือเท่าไร** — **คำตอบของทั้งใบอยู่ข้อนี้**
- **(ง)** ตอนเฟรมเลข (`HIT_WEAK` / `HIT_STRONG`) หลอด **ขยับหรือไม่** — ถ้าขยับ = **หักล้างผลรอบ 83** ข่าวใหญ่ที่สุดที่เป็นไปได้ ตัดคลิปมาให้ครบ
- **(จ)** ช่วง `MISS`/`TARGET_HP_AFTER_MISS` หลอด **ค้าง**ไหม · ไคลเอนต์กระพริบ/รีเฟรชไหมเมื่อได้ค่าที่มันถืออยู่แล้ว (มีค่าทั้งสองทาง)
- **(ฉ)** เห็น **เลขลอย** บนตัวเป้าไหม เลขเท่าไร — 🔴 **"ไม่ติดภาพ" = non-observed ไม่ใช่ absent** ให้ตอบจากวิดีโอเท่านั้น
- **(ช)** 🆕⭐ **สีของป้ายชื่อ — บันทึก "ทุกป้ายที่เห็นในเฟรม" เป็นข้อมูลประจำ ไม่ใช่เฉพาะตอนสงสัย**
  (คำสั่งคุณ Panya 2026-08-25 ~14:2x +07:00 · `notes_to_chief\consumed\20260825_1425_PANYA-PROMOTION-CRITERIA-*.md` §"ผลพลอยได้")
  🔴 **ข้อนี้อยู่ในชั้น (2) ล้วน** — สีอ่านจากจอเท่านั้น ⇒ **ตอบชั้น (1) wire/DB ไม่ได้เลย** และชั้น (1) ก็ตอบแทนไม่ได้
  (ไม่มีไบต์ไหนในเลน `HYP-PF-038` ที่พาค่า "สี") · **ตอบข้อนี้ทุกรอบ แม้ positive control ไม่ผ่าน** — ถ้ารอบจบที่ NO-RESULT ก็ยังต้องจดสีของทุกป้ายที่ทันเห็น

  **จดครบทุกบรรทัด หนึ่งบรรทัดต่อหนึ่งป้าย ต่อหนึ่งภาพ · ไม่มีให้เขียน "ไม่มี" 🔴 ห้ามเว้นว่าง:**

  | # | ป้ายที่ต้องจด | ดูที่ไหน | ถ้าไม่มี ให้เขียนว่า |
  |---|---|---|---|
  | 1 | **ชื่อตัวละครของเราเอง** เหนือหัว | H0 · H1 · H6 | "เหนือหัวไม่มีชื่อ" |
  | 2 | **ช่องชื่อบนแผง UI ซ้ายบน** ของเราเอง | H0 · H6 | "แผงซ้ายบนไม่มีชื่อ" (เป็นความต่างที่รู้อยู่แล้ว — ยังต้องยืนยันซ้ำทุกรอบ) |
  | 3 | **ชื่อ NPC เป้า** `Tornado Eagle` ป้ายลอยเหนือหัว | H1 (บังคับ) · H3 · H4 · H5 | "เห็นตัวแต่ไม่มีป้าย" |
  | 4 | **ชื่อเป้าบนแผง target** (คนละที่กับป้ายลอย) | H2 (บังคับ) | "แผง target ไม่ขึ้น" |
  | 5 | **ตัวเลข/หลอด HP บนแผง target** — จดสีของตัวเลข **และ** สีของหลอด | H2 · H3 · H4 · H5 | "อ่านไม่ออก" |
  | 6 | **title / บรรทัดคำอธิบายเหนือหรือใต้ชื่อ** ของทุกป้าย | ทุกภาพที่มีป้าย | "ไม่มีบรรทัดคำอธิบาย" |
  | 7 | **ชื่อ actor อื่นทุกตัวในเฟรม** (NPC อื่น · ร้าน · ยาม) | ทุกภาพ | "ไม่มี actor อื่นในเฟรม" |
  | 8 | **ชื่อผู้เล่นคนอื่น** | ทุกภาพ | "ไม่มี" (เลนนี้ `population=none` คาดว่าไม่มี — ยังต้องจด) |
  | 9 | **ชื่อไอเทมบนพื้น** ถ้าบังเอิญมี | ทุกภาพ | "ไม่มีไอเทมบนพื้นในเฟรม" |

  **รูปแบบที่จดลงในผล (ก๊อปตารางนี้ไปกรอก):**

  | ภาพ | ป้ายที่ # | ข้อความที่อ่านได้ | สีที่เห็น | ไฟล์ภาพ full-res | sha256 |
  |---|---|---|---|---|---|
  | H1 | 3 | `Tornado Eagle` | (กรอก) | (กรอก) | (กรอก) |

  - ชื่อสีเขียนเป็น **คำธรรมดา**: ขาว · เหลือง · เขียว · แดง · ส้ม · ฟ้า · เทา
  - 🔴 **ไม่แน่ใจ ให้เขียน "ไม่แน่ใจระหว่าง X กับ Y" — ห้ามเดาให้ลงล็อก** ("ไม่แน่ใจ" เป็นข้อมูลที่ใช้ได้ · การเดาไม่ใช่)

  🔴 **วิธีอ่านสี — บังคับ เพราะเคยเสียเวลาไปแล้วสามรอบ:**
  1. อ่านสีจาก **ภาพนิ่งความละเอียดเต็ม (full-res) เท่านั้น**
  2. 🔴 **ห้ามอ่านสีจาก contact sheet หรือภาพที่ย่อแล้วเด็ดขาด** — บทเรียน GT-045: contact sheet ถูกย่อเหลือ **400px**
     ป้ายชื่อจึงเหลือเป็นจุดเดียว **หาเฟรมไม่เจอสามรอบติด**
  3. จะทำภาพครอปให้ดูง่าย ⇒ **crop จากต้นฉบับ ห้าม resize ลง** · เก็บทั้งต้นฉบับและครอป
  4. **ห้ามใช้วิดีโอเป็นแหล่งหลักของสี** — การบีบอัดเปลี่ยนสีได้ · วิดีโอใช้ตอบข้อ (ฉ) และยืนยัน "ป้ายอยู่ตรงนั้นตอนไหน" ได้
     แต่ **ค่าที่ลงในตารางสีต้องมาจากภาพนิ่ง**
  5. เก็บที่ `evidence_screens\GT035_H<N>_FULLRES_<yyyyMMdd_HHmmss>.png` · **จด sha256 ทุกไฟล์** (ชั้น (2) บังคับอยู่แล้ว)
  6. เฟรม H ใดไม่มีป้ายเลย ⇒ เขียน **"H<N>: ไม่มีป้ายในเฟรม"** — นั่นเป็นผล ไม่ใช่ช่องว่าง

  **P5 [คำทำนาย · หักล้างได้ — คำทำนายที่ผิดคือผล ไม่ใช่ความล้มเหลว]**
  จากภาพเซิร์ฟเวอร์ต้นฉบับที่คุณ Panya เทียบมา (NPC=เหลือง · ผู้เล่น=เขียว · ไอเทมบนพื้น=ขาว · title/คำอธิบาย=ฟ้า · ชื่อตัวเอง=ขาว):
  - จัดเข้าช่อง **"ผู้เล่น"** ⇒ ป้าย `Tornado Eagle` เป็น **เขียว** (คาดว่าจะเจอผลนี้ — GT-034/GT-045 เห็นเขียวมาแล้ว)
  - จัดเข้าช่อง **"NPC"** ⇒ **เหลือง** ⇒ แปลว่ารอบก่อนอ่านผิด หรือมีอะไรเปลี่ยนระหว่างรอบ — **ข่าวใหญ่ จดละเอียด**
  - จัดเข้าช่อง **"ศัตรู"** ⇒ **น่าจะแดง** — ยังไม่มีใครเคยเห็นป้ายแดงในโปรเจกต์นี้ ถ้าเจอถือเป็นของใหม่ทั้งดุ้น
  - ได้ **สีที่ไม่อยู่ในสามข้อบน** ⇒ จดสีที่เห็นตรง ๆ แล้วจบ · 🔴 **ห้ามยัดเข้าช่องที่ใกล้ที่สุด**

  🔴 **ข้อจำกัดที่ต้องอ่านคู่กับ P5 เสมอ — และรอบนี้มันแรงกว่าตอนร่าง:**
  **การจับคู่ "สี ⇒ ช่องผู้เล่น/NPC/ศัตรู" ยังไม่ถูกพิสูจน์เลยแม้แต่นิดเดียว** · ใบที่จะตอบคือ **`RE-067`** (`CLIENT_RE_QUEUE.md` · STATIC-ON-BRIDGE · เปิดอยู่)
  🔴🔴 **และ R163 วัดแล้วว่าชั้น wire ไม่หนุนคำอธิบายที่ง่ายที่สุด:** เซิร์ฟเวอร์เราส่ง `actor_type = 4` (`CNetNPC`)
  ให้ `0x201F` **ทุกจุดที่บูตปกติเดิน** (19 call site ใน v141 + 9 ใน `src/`) ⇒ **ถ้าป้ายขึ้นเขียว เหตุผลไม่ใช่ "เราส่งไบต์ชนิดผิด"**
  ⇒ **หน้าที่ของผู้เทสในข้อนี้คือ "จดสี" อย่างเดียว** · 🔴 **ห้ามเขียนในผลว่า "เพราะฉะนั้นไคลเอนต์จัด `0x201F` เป็นผู้เล่น/NPC/ศัตรู"**
  · 🔴 **ห้ามใช้สีเปลี่ยนคำตอบของข้อ (ค)** ซึ่งเป็นคำถามหลักของทั้งใบ

  🟢 **ผลลบของข้อนี้มีค่าเท่าผลบวก และ redirect อะไร:**
  - **ทุกป้ายสีตรงกับเซิร์ฟเวอร์ต้นฉบับหมด** ⇒ **ผลลบที่มีค่า** ⇒ **redirect `RE-067`:** ลดน้ำหนักเส้น actor (จ็อบ S6/S7/S8) ไปโฟกัสเส้นไอเทมแทน
    · 🔴 **เขียนในผลว่า "ตรวจแล้ว ตรง" ให้ชัด ห้ามเงียบ** — **"ไม่ได้จด" กับ "จดแล้วไม่ต่าง" คนละเรื่องกัน**
  - **สีต่างจากเซิร์ฟเวอร์ต้นฉบับ** ⇒ ลง `REAL_SERVER_DIVERGENCE.tsv` ⇒ **หนุน `RE-067` H2** (สีมาจากสถานะบนสายที่เราไม่เคยส่ง)
  - **ป้ายไม่ขึ้นเลยทั้งที่เห็นโมเดล** ⇒ **ผลใหม่ที่ไม่มีใครเคยเห็น** — จดเป็นเรื่องของตัวเอง 🔴 **ห้ามอ่านเป็น "สีผิด"**

  **ผลต้องไปลงทะเบียนกลางด้วย — `REAL_SERVER_DIVERGENCE.tsv`** (อ่านหัวไฟล์ก่อนกรอก · คั่นด้วย **TAB** · **หนึ่งแถวต่อหนึ่งความต่าง ห้ามยุบสองความต่างเป็นแถวเดียว**):
  - `timestamp` = เวลาที่เห็นบนจอ (+07:00) · `capability_or_lane` = ชนิดของป้าย เช่น `npc-spawn / ป้ายชื่อ actor`
  - `what_was_compared` = ป้ายอะไร ของ identity/ไอเทมตัวไหน (ใส่ `0x201F` หรือ `n_ID` ให้ครบ)
  - `real_server` = สีในภาพต้นฉบับ · 🔴 **ไม่มีภาพต้นฉบับของป้ายชนิดนั้น ⇒ ใส่ `(ยังไม่มีภาพอ้างอิงของเซิร์ฟเวอร์เดิมสำหรับข้อนี้)` ห้ามเดา**
  - `ours` = สีที่เราเห็น · `evidence_layer` = **`eye` เสมอสำหรับข้อนี้** (ไม่ใช่ `pixel` ไม่ใช่ `wire`)
  - `evidence_ref` = path ภาพ full-res · **`evidence_sha256` = sha256 ของไฟล์นั้น (คนละคอลัมน์ ห้ามยัดรวม)**
  - **`evidence_in_repo`** = `yes` เฉพาะเมื่อไฟล์ commit เข้ารีโปแล้วจริง ๆ · `open_ticket` = `RE-067` · `blocks_promotion` = `no`
  - 🆕 **`compared_and_matched`** = `yes` (เทียบแล้วตรง) / `no` (เทียบแล้วต่าง) / `no-reference` (ไม่มีภาพเซิร์ฟเวอร์เดิมให้เทียบ)
    🔴 **เติมแถวแม้ผลจะ "ตรงกัน"** — ถ้าเก็บเฉพาะความต่าง เลนที่เทียบแล้วตรงจะแยกไม่ออกจากเลนที่ไม่เคยเทียบ
  - `observation_note` = ข้อความที่อ่านได้ + เฟรม H ที่ใช้ + ข้อสังเกต · 🔴 **ห้ามเขียนสาเหตุหรือข้ออนุมานลงช่องนี้**

  🔴🔴 **ข้อยกเว้นที่ต้องรู้ และเป็นความไม่สอดคล้องที่ chief ยอมรับตรง ๆ (R163):**
  กฎข้อ 4 ข้างบนห้ามใช้วิดีโอเป็นแหล่งของสี **แต่แถวไอเทมในทะเบียนตอนนี้มาจากเฟรมวิดีโอพอดี**
  (เป็นหลักฐานชิ้นเดียวที่มี · ชุด jpg ที่จดหมายอ้างคู่กัน **ไม่แสดงป้ายนั้น** — chief เปิดดูเองแล้วทั้ง 6 ใบ)
  ⇒ **แถวนั้นถูกทำเครื่องหมาย `evidence_in_repo=no` และรอภาพนิ่ง full-res จากหน้าสะพาน**
  ⇒ 🔴 **กฎยังบังคับกับรอบใหม่ทุกรอบ** — ข้อยกเว้นนี้เป็นของแถวเก่าที่เก็บย้อนหลังไม่ได้แล้ว **ห้ามใช้เป็นบรรทัดฐาน**

**🔴 ผลลบมีค่าเท่าผลบวก และเขียนไว้ล่วงหน้าว่าจะ redirect อะไร:**
- **โมเดลขึ้น + เลขลอยขึ้น + หลอดไม่ขยับเลยทั้ง sweep** ⇒ **ผลลบสมบูรณ์ ไม่ใช่ FAIL** — แปลว่า "หลอดของเป้าขยับได้" ที่ GT-039 พิสูจน์บน `0x2001` **ไม่ generalise ไปถึง `0x201F`/HP baseline จริง** ⇒ redirect: เปิดใบ static หาว่าอะไรต่างกันระหว่างสอง identity (template 1 vs 31 · usage 2 vs 1 · preset · `n_RANK`) **ก่อน**กลับมา attended อีกรอบ · **ห้ามปิด GT-036 เป็นลบจากผลนี้**
- **โมเดลขึ้น + หลอดขยับตามคาด** ⇒ ✅ **PASS ครึ่ง client-observable** ⇒ 🔴 **[แก้โดย chief R164: ถ้อยคำเดิม "GT-036 ได้เงื่อนไขที่มันรออยู่" **ผิดและถูกถอน** — ผลนี้เกิดขึ้นจริงแล้วและ GT-036 **ไม่ได้ถูกปลด** ดูวงเล็บสถานะหัวใบ GT-036]** ~~GT-036 ได้เงื่อนไขที่มันรออยู่~~ (ดูบรรทัดท้ายใบ)
- **ชั้นนี้ตอบไม่ได้:** ภาพหน้าจอไม่ใช่หลักฐานว่าเซิร์ฟเวอร์ส่ง/ไม่ส่งไบต์อะไร **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

---

### 🔴 รอ merge ก่อน — ใบนี้บูตไม่ได้จนกว่าเลนโค้ดจะลง `main`
**ณ R159 ยังไม่มีโมดูล ไม่มี flag ไม่มีไฟล์ scenario ไม่มี slot `HYP-PF-038` อยู่ที่ไหนเลย** — สิ่งที่ใบนี้มีคือ *ดีไซน์* ⇒
🔴 **ห้ามบูตใบนี้ · ห้ามยืมเลน HYP-PF-029 หรือ arena มารันแทน · ห้ามให้รอบ unattended แตะ**
เงื่อนไขปลดมีข้อเดียวและวัดได้: **เลน `HYP-PF-038` merge เข้า `main` แล้ว และ `<SHA>` ที่จะบูตผ่านห้าข้อในบล็อก "ด่าน 2" ครบทั้งห้า**
ก่อนถึงตอนนั้นสถานะคือ **BLOCKED ON CODE LANE — รอ merge ไม่ได้รอผู้เทส** · **ปล่อยใบไว้ที่เดิม ห้ามลบ ห้ามย้าย ห้ามย่อ**

### nonclaims (ติดไปกับผลทุกกรณี ไม่ว่าบวกหรือลบ)
- ⭐ **สูตรความเสียหาย · ladder · การเชื่อม "เลข ↔ หลอด" ทั้งหมดเป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้ว ไม่เคยเผยแพร่ และกู้ไม่ได้ตลอดกาล** — ไม่มี capture ชุดไหนแสดง HP ของเป้าขยับตามดาเมจ และรอบ 83 พิสูจน์แล้วว่าไคลเอนต์ไม่ลบเลขเอง นั่นคือเหตุที่เซิร์ฟเวอร์ต้องพูดทั้งสองครึ่งเอง
- **`3857` เป็น HP baseline ที่ ship มากับ client** (`STANDARD_MOB`) ไม่ใช่กฎของเซิร์ฟเวอร์ต้นฉบับ · เลข `faction`/`AI`/`drops` ของ `0x201F` ก็เป็นข้อมูลฝั่ง client เช่นกัน
- **การวางเป้าแบบ player-relative เป็น harness ของเรา** (`GEO-PF-001 harness_only`) — **ห้าม claim ว่าผู้เล่นจริงเคยเจอ Tornado Eagle ตรงนั้น**
- **ไม่ claim ว่าตีมันได้จริง** — เราไม่ได้ตี เรา*บอก*ว่ามันโดน · `0x201F` เป็น retaliate-only ตามตาราง client และใบนี้ไม่ทดสอบข้อนั้น
- **ไม่ claim เรื่องความตาย** (ladder ของใบนี้ไม่แตะพื้น 0 โดยเจตนา) · **ไม่ claim เรื่องลูท** (ครึ่งลูท = GT-037 ✅ DONE / GT-040 · และคาเวียตรอบ 118 ใต้ GT-036) · **ไม่ claim เรื่อง aggro/threat/chase**
- **ไม่ claim ว่า HP persist** — ไม่มีคอลัมน์ HP ในฐานข้อมูล balance ตายพร้อม sweep
- **ไม่ claim ว่าผลนี้ generalise ไปถึง hostile ตัวอื่นใน 13 ตัวของ roster** — ใบนี้ยิงตัวเดียว
- **`heading_mapping` / `camera_orientation` / `native_render` / `client_standing_position` / `scene_id_numeric_provenance`** ยังเป็น nonclaims ทางการของเลนนี้เหมือนที่ GT-034 ติดไว้
- 🔴 **ไม่ claim ว่ามีการปฏิเสธตามชื่อเกิดขึ้น จากการที่คอนโซลเงียบ** — เหตุผลอยู่ในชั้น (1)
- 🆕 🔴 **สีที่จดในข้อ (ช) อ่านด้วยตาจากภาพ ไม่ได้วัดค่าพิกเซล** — **ไม่ claim ค่า RGB/hex ใด ๆ** และ **ไม่ claim ว่าสองสีที่จดในสองรอบเป็นสีเดียวกันจริง** · ป้าย `evidence_layer` ของทุกแถวที่ออกจากใบนี้คือ **`eye`** เท่านั้น · การวัดค่าพิกเซลเป็นงานคนละใบ
- 🆕 🔴 **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับอาจเป็น client คนละ build หรือคนละภูมิภาค** — ยังตัดข้อนี้ทิ้งไม่ได้ (คุณ Panya ระบุเอง) ⇒ **"ต่างจากภาพต้นฉบับ" ยังไม่เท่ากับ "ของเราผิด"**
- 🆕 **ไม่ claim ว่าอะไรเป็นตัวตัดสินสี** — นั่นคือ objective ของ `RE-067` ทั้งใบ · ข้อ (ช) ผลิตแค่ **การสังเกต** ไม่ผลิตข้อสรุปเรื่องกลไก
- 🆕 **ไม่ claim ว่าสีเกี่ยวข้องกับ hostility · damage · aggro หรือคำตอบของข้อ (ค)** — **สีเปลี่ยนหรือไม่เปลี่ยน ไม่กระทบสถานะ PASS/FAIL ของใบนี้เลย** ข้อ (ช) เป็นข้อมูลประจำที่เก็บพ่วงไปกับรอบ

- **result:** (ผู้เทสกรอก: ① `BOOT_COMMIT` + ผลเช็คห้าข้อ (โดยเฉพาะข้อ 4: เจอ `0x201F`+`3857`, ไม่เจอ `0x2001`) ② label ทั้ง 7 ใบ + ขนาดไบต์ + เวลาที่ออก ③ ผล hexdump: `1F 20 00 …` ปรากฏกี่เฟรม · `01 20 00 …` = 0 เฟรมหรือไม่ · ASCII `Tornado Eagle` · `max_hp` 3857 ④ พิกัด `TARGET_SPAWN` ที่ decode ได้ เทียบผู้เล่น +100X/+50Y ⑤ **ผลของ positive control (แถวไหนในตาราง)** ⑥ คำตอบ (ก)–(ช) เป็นภาษาคน ⑦ ภาพ H0–H6 + วิดีโอต่อเนื่อง พร้อม sha256 ทุกไฟล์ ⑧ sha canonical ก่อน-หลัง · sessions/lease_generation/integrity_check ของสำเนา ⑨ path ของ raw GAME log + console out/err ⑩ teardown exit code ⑪ 🆕 **ตารางสีป้ายชื่อครบทุกป้ายทุกภาพ H0–H6** (ตามข้อ (ช)) + path ภาพ full-res + sha256 + **เลขแถวที่เติมลง `REAL_SERVER_DIVERGENCE.tsv` หรือคำว่า "ตรวจแล้ว ไม่มีความต่าง"**)


### 🔴🔴 ขอบเขตของคำว่า PASS ในใบนี้ — เขียนโดย chief R164 หลัง `pf-adversary` หักล้างฉบับแรก **อ่านก่อนอ้างอิงผลนี้ที่ไหนก็ตาม**

**① PASS นี้เป็น PASS ของ *ชั้น (2) client-observable* เท่านั้น — ชั้น (1) wire/DB ไม่ถูกรายงานเลยแม้แต่ข้อเดียว**
กฎของใบเอง (`pass criteria — สองชั้น แยกกันเด็ดขาด **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**`) และบรรทัดเกณฑ์ของใบเขียนไว้เองว่า
ผลบวกแบบนี้คือ **"PASS ครึ่ง client-observable"** ⇒ **ห้ามอ่านหัวใบว่าเป็น PASS ของทั้งใบ**
สิ่งที่ **ยังไม่มีใครรายงาน**: นับเฟรมขาออกครบเจ็ด · hexdump `1F 20 00 00` ในทุกเฟรม · `01 20 00 00` = 0 เฟรม
· ASCII `Tornado Eagle` + `M011_000_000_SP3` ใน `TARGET_SPAWN` · decode f32 placement · `sessions` +1 · `integrity_check`
· ภาพ H0-H6 · sha256 ของภาพ/วิดีโอ · ตารางสีป้ายชื่อครบทุกป้าย · คำตอบ (ก)-(ช)
⇒ 🔴 **ช่อง `result:` ของใบนี้ยังว่าง และ chief ปล่อยให้ว่างโดยตั้งใจ** — การเติมมันเป็นงานของรอบ attended ไม่ใช่ของ chief

**② "สองผู้สังเกตอิสระ" ครอบคลุมแค่ไหน — ผู้สังเกตทั้งสองไม่ได้ยืนยันตรงกันครบทั้งสี่ค่า**
หลักฐานของรอบ 1 เอง (`evidence_screens/GT035_1138_HPPANEL_432-476s.jpg`) ไม่มีแผง target เลยตั้งแต่ `t432` ถึง `t458`
แผงโผล่ที่ `t460` โดยอ่านค่า `2893` อยู่แล้ว และ `771` ที่ `t472` ⇒ **รอบ 1 ไม่เคยเห็น `3857` และไม่เคยเห็นขั้นแรก**
บวกกับที่จดหมาย §⑤.1 บันทึกเอง: รอบ 1 **พลาดเลขดาเมจทั้งสองตัวและ `MISS` ทั้งหมด**

| สิ่งที่อ้าง | ยืนยันโดยกี่ผู้สังเกต |
|---|---|
| โมเดลถูกวาด (P1) | **สอง** |
| หางบันได (`2893` → `771`) | **สอง** |
| ค่า `3857` และขั้นแรก `3857 → 2893` (**คำตอบของทั้งใบ**) | 🔴 **หนึ่ง** — วิดีโอรอบ 2 เท่านั้น |
| เลขดาเมจ `964` / `2122` · `MISS` บนจอ (P4) | 🔴 **หนึ่ง** — วิดีโอรอบ 2 เท่านั้น |

⇒ **ห้ามเขียนว่า "ยืนยันสองรอบ" แล้วใช้เป็นเหตุผลข้ามตัวควบคุมของใบอื่น** — ข้อที่แบกน้ำหนักมากที่สุดมีแหล่งเดียว

**③ ข้อสรุป ② ("ตัวคุม MISS ทำงาน") เป็นข้ออ้างชั้น (1) ที่สร้างจากหลักฐานชั้น (2)**
ใบนี้เขียนไว้เองว่าด้วยตาแยกไม่ออก และตัวชี้ขาดคือการนับเจ็ดบรรทัด `[G>]` ซึ่ง **ไม่มีใครนับ**
⇒ ที่พูดได้จริงคือ **"หลอดไม่ขยับตลอด 22 วินาทีที่คร่อม MISS"** ไม่ใช่ **"ตัวคุม MISS ทำงาน"**

**④ ไฟล์หลักฐานที่ใบนี้อ้างถึง (ยังไม่ได้จด sha256 — เป็นหนี้ที่ค้าง ไม่ใช่ของที่ไม่ต้องมี):**
`evidence_screens/GT035_1138_HPPANEL_432-476s.jpg` · `GT035r2_1141_HPLADDER_v2_366-406s.jpg`
· `GT035r2_1141_FULLRES_t373.3s.jpg` · `GT035r2_1141_FULLRES_t385.4s.jpg` · `GT035r2_1141_FULLRES_t397.3s.jpg`

**⑤ ด่าน 3b (ตัวควบคุมกฎกล้อง ~30 วินาที) — ถูกข้ามทั้งสองรอบ และไม่มีใครจดว่าข้าม**
ใบบังคับว่า *"ผลของด่านนี้ต้องอยู่ในช่อง `result` เสมอ ไม่ว่าออกทางไหน"* · GT-035 **คือรอบ attended ถัดไป** ที่หนี้ก้อนนั้นฝากไว้
⇒ 🔴 **นับเป็น skip ที่เปิดเผยแล้วตรงนี้** (SKIP-CENSUS style) · หนี้ยังค้าง ตกไปที่รอบ attended ถัดไป
⇒ **แปลว่ากฎกล้องฉบับ R163 ยังเป็น "คำให้การ" ไม่ใช่ "การวัด" อยู่เหมือนเดิม**

### 🔴 nonclaims ที่ต้องติดไปกับผล PASS นี้เสมอ (ยกจากจดหมาย `20260825_1550` §③ · ห้ามอ้างผล GT-035 ที่ไหนโดยไม่พกห้าข้อนี้ไปด้วย)

1. ⭐ **เลขคณิต · บันได · การเชื่อม "เลข ↔ หลอด" ทั้งหมดเป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** — nonclaim ยืนของ `HYP-PF-026`/`HYP-PF-029` · **ใบนี้ไม่ปลดมัน แม้แต่ข้อเดียว**
2. 🔴 **ไม่ได้พิสูจน์การตาย** — เลนนี้ **ไม่มีครึ่งตายเลยโดยดีไซน์** (`HP_FLOOR` ประกาศว่า FORBIDDEN · ไม่มีเฟรม hp = 0 · ไม่มี death timer · ไม่มี dying latch) และหลอด **จบที่ `771` ไม่เคยแตะ `0`** ⇒ **ห้ามอ้างผลนี้กับ `GT-036` ไม่ว่ารูปแบบใด**
3. 🔴 **คำว่า "hostile" ในชื่อใบยังไม่ถูกพิสูจน์** — ป้ายชื่อนกขึ้น **สีเขียว** ซึ่งบนเซิร์ฟเวอร์ต้นฉบับคือ **สีของผู้เล่น** (NPC = **เหลือง**) ⇒ ไคลเอนต์จัดมันเข้าช่อง "ผู้เล่น" ไม่ใช่ "ศัตรู" (จดหมาย `20260825_1420` · ใบ `RE-067`) ⇒ **หลอดขยับได้โดยที่เป้าไม่ต้องเป็นศัตรู** · 🔴 ผู้เทสจดสีอย่างเดียว **ห้ามอนุมานสาเหตุจากสี** — สาเหตุคือ objective ของ `RE-067` ทั้งใบ
4. **ไม่ได้พิสูจน์ว่าไคลเอนต์คำนวณอะไร** — มันแสดง **เลขที่เราส่ง** เท่านั้น
5. **ไม่ได้ตี ไม่ได้ใช้สกิล** — ทุกเฟรมมาจากเซิร์ฟเวอร์ยิงเอง ผู้เล่นแค่พิมพ์แชตหนึ่งครั้ง (`0x201F` เป็น retaliate-only · เรา *บอก* ว่ามันโดน ไม่ได้ตีมันจริง)

### 📌 สถานะปลายน้ำหลัง GT-035 PASS (chief R164 · เปลี่ยนสองใบ · **ไม่มีใบไหนถูกลบ ย้าย หรือย่อ**)

- **`GT-036` KILL-HOSTILE-001 → 🔴 คง BLOCKED (เหตุผลเปลี่ยน ไม่ใช่สถานะเปลี่ยน)** — เดิมบล็อกเพราะ "รอ GT-035" · **ตอนนี้บล็อกเพราะไม่มีเลนที่มีครึ่งตาย** · `HYP-PF-038` ที่เพิ่งผ่านมา **ตัดครึ่งตายทิ้งโดยเจตนา** (`HP_FLOOR` = FORBIDDEN · ladder จบที่ `771`) ⇒ ตัวปลดคือ **เวอร์ชันถัดไปของ `HYP-PF-038` ที่มีครึ่ง lethal ไม่ใช่เลนที่บูตในรอบนี้** · 🔴 **ห้ามอ้างผล GT-035 เป็นเงื่อนไขปลด GT-036** และ **ห้ามยืมเลนนี้มารันแทน** · 🔴 **เลน lethal ยังไม่ถูกสร้าง และ chief จะไม่สร้างเองจนกว่าคุณ Panya จะเคาะ** — การปลดการ์ด `HP_FLOOR = FORBIDDEN` เข้าข่าย "เปลี่ยนของที่พิสูจน์แล้ว" ตามนโยบายข้อ 3 (คำถามอยู่ในจดหมาย `FROM_CHIEF_R164_*` §⑤)
- **`RE-067` NAME-COLOR-SOURCE-001 (`CLIENT_RE_QUEUE.md`) → 🟢 OPEN เหมือนเดิม แต่ได้น้ำหนักเพิ่มจากข้อมูลใหม่** — **หลอด HP ของเป้าขยับได้ตามที่เซิร์ฟเวอร์บอก ทั้งที่ไคลเอนต์จัดป้ายชื่อมันเป็นสี "ผู้เล่น"** ⇒ **สีป้าย กับ กลไก HP เป็นคนละเส้นกัน** — เป็นข้อเท็จจริงใหม่ของใบนั้น (ก่อนหน้านี้ยังไม่มีรอบไหนที่ทั้งสองอย่างเกิดพร้อมกันในเฟรมเดียว) · 🔴 **ข้อนี้เป็นการสังเกต ไม่ใช่กลไก** — ยังไม่ claim ว่าอะไรตัดสินสี · หลักฐานเต็มเขียนไว้ท้ายใบ `RE-067` แล้ว (chief R164)

### 🆕 อัปเดต R162 (2026-08-25 ~11:3x +07:00) — ข้อบังคับ placement + ด่านข้อ 6 + ข้อห้ามแตะ allowlist ของ arena

**ที่มา:** จดหมายหน้าสะพาน `20260825_1010_GT035-DESIGN-CONSTRAINT-hyp038-must-inherit-arena-player-relative-placement.md` §②③ · chief ตรวจซ้ำเองบน clone รอบนี้ครบทุกข้อ
**สถานะไม่เปลี่ยน: 🟠 BLOCKED ON CODE LANE** · บล็อกนี้ **เพิ่มด่าน** ไม่ได้แทนที่ห้าข้อเดิม · ไม่มีรายการใดถูกลบ/ย่อ/ย้าย

**① placement เป็น "เงื่อนไขก่อนรอบ" ไม่ใช่ทางเลือกของคนบูต** (ยกระดับจาก §⑤ ข้างบน — เนื้อเดิมคงไว้ทั้งหมด)
- เส้น default บังคับพิกัดโลกคงที่ **โดยโครงสร้าง ไม่ใช่โดยการตั้งค่า**: `make_v112_monster_shop_population_state()` นิยาม `v141:1908` · **signature ไม่มี argument ตำแหน่งผู้เล่นเลย** (`:1908-1912`) · ถูกเรียกที่ `:4294` ใต้เงื่อนไข `:4293` (`not self.npc_spawn_sent`) · label ที่ `:4296` ⇒ ได้ `(1747.5244140625, -7837.69775390625, 931.0413208007812)` จากแถว `v141:1349` เสมอ ไม่ว่าผู้เทสยืนตรงไหน
- เส้น arena เป็นเส้นเดียวที่คำนวณจากผู้เล่น: `arena_v1.json:10-14` `"mode":"player_relative","dx":100,"dy":50,"dz":0` → `scenario.py:94 make_p30_target()` คิดที่ **`:97-98`** · heading derive จากผู้เล่นที่ `:117`
- ปิดเส้น default ต่อเซสชัน: `runtime.py:3638-3642` (`arena_spawned=True` · `npc_spawn_sent=True` · `population_indices=(legacy.V112_MONSTER_INDEX,)`) · กันซ้อนอีกชั้นที่ `runtime.py:3608-3615`
- ⇒ **ข้อบังคับ:** เลน `HYP-PF-038` ต้องมีทั้ง (ก) วางเป้าแบบ `player_relative` และ (ข) suppress เส้น V134 ของตัวเอง · **เลนที่ merge มาโดยไม่มีสองข้อนี้ = ห้ามบูต ใบอยู่ BLOCKED ต่อ ไม่ใช่ให้ผู้เทสลองดูก่อน**
- 📎 identity ไม่ขึ้นกับ placement: สูตร `aid = 0x2000 + idx + 1` เขียนซ้ำ **4 ที่** (`v141:1095` · `v141:1459` · `v141:1917` · `scenario.py:101` ที่มี assert เทียบ `legacy.V112_MONSTER_ACTOR_ID`) และอีกจุดที่ `population.py:46` ⇒ ย้ายพิกัดได้ **แต่ `0x201F` ยังผูกกับ idx 30 เหมือนเดิมทุกเลน**

**② 🔴 ด่านก่อนบูต "ข้อ 6" — static ล้วน รันได้ก่อนบูต (ต่อจากห้าข้อในบล็อก "ด่าน 2" ข้างบน ซึ่งคงไว้ทั้งหมด)**
เหตุผลที่ต้องเป็น static: ถ้าเลนวางเป้าผิดท่า ผู้เทสจะรู้ตอนที่ยืนอยู่ในเกมแล้ว = **เผารอบ attended ทิ้งทั้งรอบ ทั้งที่โค้ดทำงานถูกทุกบรรทัด**
🔴 **กติกาการเขียนคำสั่ง (พังมาแล้ว 4 ครั้งติดที่ด่านของ GT-045):** ต้องรันบน **PowerShell 5.1** ได้ · **ห้ามไปป์ยูนิกซ์** (`| awk`, `| wc`) · **ห้ามมีอักขระ `"` อยู่ในตัว regex** (ใช้ `.?` แทน) · **ห้ามใช้ `&&`** · พิมพ์ `$LASTEXITCODE` ต่อท้ายทุกคำสั่ง (`0` = เจอ · `1` = รันแล้วไม่เจอ · อย่างอื่น = คำสั่งล้ม/rev ผิด)
```
git grep -n -e "mode.?: .?player_relative" <SHA> -- scenarios/hostile_hp_link_hypothesis_p30_sweep.json
$LASTEXITCODE
git grep -n -e "1747.5" -e "7837.6" <SHA> -- scenarios/hostile_hp_link_hypothesis_p30_sweep.json
$LASTEXITCODE
git grep -n -e "HOSTILE_HP_LINK_TARGET_WORLD_X" <SHA> -- src/pirateforce_foundation/hostile_hp_link_hypothesis.py
$LASTEXITCODE
git grep -n -e "player_relative" <SHA> -- scenarios/arena_v1.json
$LASTEXITCODE
```
- **6a ต้อง exit 0 และมีอย่างน้อยหนึ่งบรรทัด** — ไฟล์ scenario ของเลนใหม่ระบุ `player_relative` จริง
🔴🔴 **6b ฉบับแรก (เขียนโดยผู้ช่วย รอบ GT-035 15:0x) พังและทำให้บูตแรก abort — ถอนแล้วโดย chief R164 อ่านก่อนใช้**
ฉบับนั้น grep **ทั้งโมดูลด้วย** แล้วสั่งว่า "เจอแม้บรรทัดเดียว = ห้ามบูต" · แต่โมดูล **pin ค่า `1747.5` / `-7837.6` ไว้โดยตั้งใจ** (`hostile_hp_link_hypothesis.py:37` docstring · `:438-439` ค่าคงที่) และ **ใช้มันเป็นเงื่อนไข *ปฏิเสธ*** ⇒ 6b ฉบับนั้น **exit 0 เสมอ ⇒ "ห้ามบูต" เสมอ ⇒ ผ่านไม่ได้ตลอดกาล**
🔴 **รูปทรงของบั๊ก (ครั้งที่ห้าติดกัน — R159 เช็ค 5 · R161 เช็ค 5 · R161-b · 6b · และครั้งนี้เป็นครั้งแรกที่กินเวลา attended จริง):** **ด่านที่คาดหวังว่า "ไม่มีเอาต์พุต" ห้ามเล็งไปยังไฟล์ที่ค่านั้นปรากฏได้ในฐานะ *ข้อความ*** — grep แยก "ค่าที่ถูกส่ง" ออกจาก "ค่าที่ถูกพูดถึง" ไม่ได้
⇒ 🔴 **นี่คือกฎ ไม่ใช่บั๊ก** · chief R164 ยกขึ้นเป็นกติกาการเขียนด่านของโปรเจกต์ **ทุกด่านที่คาดหวังผลว่าง ต้องระบุ path ให้แคบจนค่านั้นเป็นได้แค่ค่าที่ถูกส่ง**
- **6b (ฉบับแก้) ต้อง exit 1 และไม่มีบรรทัดใดออกมาเลย** — **เฉพาะไฟล์ scenario เท่านั้น** ไม่มีพิกัดโลกคงที่ `1747.5` / `-7837.6` ฝังอยู่ในไฟล์ scenario
- 🆕 **6d = ตัวควบคุมเชิงบวกของ 6b ต้อง exit 0 และมีอย่างน้อยหนึ่งบรรทัด** — โมดูล **ต้องยังมี** `HOSTILE_HP_LINK_TARGET_WORLD_X` อยู่ เพราะมันคือแถว WORLD ที่แช่แข็งไว้ **เพื่อใช้ปฏิเสธ** · **6d ออก 0 บรรทัด = เลนถูกแก้ผิดทาง ⇒ ห้ามบูต** *(เดิม 6b พยายามยืนยันเรื่องนี้ด้วยการหาว่า "ไม่มี" ซึ่งกลับหัว)*
- *(ถ้อยคำเดิมของ 6b ที่ถูกถอน:* ~~ไม่มีพิกัดโลกคงที่ `1747.5` / `-7837.6` ฝังอยู่ในไฟล์ scenario หรือโมดูล~~ของเลน · **เจอแม้บรรทัดเดียว = เลนกำลังจะวางนกที่ placement จริง = ห้ามบูต** (ผลจะซ้ำ GT-045: จุด minimap ไม่มีตัว)
- **6c = positive control ต้อง exit 0 เสมอ** — ถ้า 6c ออก 0 บรรทัด แปลว่า **คำสั่งไม่ได้รันจริง / `<SHA>` ผิด / path ผิด** ⇒ ผลของ 6b เป็นโมฆะ **ห้ามอ่าน 6b ว่า "ผ่าน"**
- **หน้าตาผลที่จะเห็นจริง:** ใส่ rev ในคำสั่ง ⇒ ทุกบรรทัดขึ้นต้นด้วย `<SHA>:` เช่น `<SHA>:scenarios/arena_v1.json:12:      "mode": "player_relative",` (ไม่ใช่ขึ้นต้นด้วยชื่อไฟล์เปล่า) · ถ้าเห็นบรรทัดที่ **ไม่มี** `<SHA>:` นำหน้า แปลว่ากำลัง grep working tree ไม่ใช่ commit ที่จะบูต — รันใหม่
- **ไม่ครบ 6a/6b/6c/6d = ห้ามบูต** เหมือนห้าข้อเดิม · ชื่อไฟล์ข้างบนยังเป็นชื่อ "เสนอ" ⇒ ยืนยันชื่อจริงจากผล PR ก่อน อย่าเดา

**③ 🔴 ข้อห้ามเด็ดขาด — ห้ามเติม `"damage"` เข้า `caps` ของ arena เพื่อให้เลนใหม่ผ่าน**
- กฎจริงอยู่ที่ `scenario.py:82-83` (`caps != ("spawn","target")` · `nonclaims != ("authentic_position","tab","combat","ai","damage","loot")`) แล้ว `raise ValueError` ที่ `:86`
- ผู้บริโภคของ allowlist นี้ **3 ไฟล์**: `app.py:63,235` · `runtime.py:164,3635,3713` · `tests/test_arena.py` (13 จุด · **`:110-113` วัด allowlist ตัวนี้ตรง ๆ**) ⇒ แก้ทีเดียว **ความหมายของเลนที่พิสูจน์และ merge ไปแล้วเปลี่ยนเงียบ ๆ โดยไม่มีรอบไหนวัดการขยายนั้น**
- 🔴 **ของเน่าที่จะหลอกคนแก้:** `scenario.py:28-29` มี `_CAPABILITIES` / `_NONCLAIMS` เป็น **set ที่ไม่มีใครอ้างถึงเลยทั้ง repo** ⇒ เป็นแหล่งความจริงคู่ขนานกับบรรทัด 82-83 · **ใครแก้ set สองตัวนี้แล้วนึกว่าแก้กฎ จะได้กฎเดิมแบบเงียบ ๆ**
- ⇒ `HYP-PF-038` ต้องเป็น **slot ใหม่ที่มี allowlist ของตัวเอง ยืม geometry ของ arena มาใช้** ไม่ใช่แก้ arena · ยืนยันสถานะ slot (วัด R162): `HYP-PF-029` เต็ม **3/3** · `HYP-PF-032` เต็ม **3/3** · ทั้งคู่ `extension_approval_ref: null` · slot สูงสุดที่ใช้แล้ว = `HYP-PF-037` (`docs/HYPOTHESIS_LEDGER.json:3410`)
- 🔴 **กับดักการอ่าน ledger:** `tracked_versions` อยู่ **ใต้คีย์ `expiry`** ไม่ใช่ระดับ entry ⇒ ต้องอ่าน `e["expiry"]["tracked_versions"]` · อ่านผิดระดับจะเห็นเป็น "ยังไม่เต็ม" ทั้งที่เต็มแล้ว

**④ ช่องกรอกผลเพิ่ม — แยก "ไม่เห็นตัวนก" ออกจาก "damage ไม่ทำงาน" ตั้งแต่แรก** (เพิ่มเติม ไม่แก้ตาราง positive control และไม่แก้ข้อ (ก)-(ฉ))
ผู้เทสกรอกสามข้อนี้ **ก่อน** เขียนคำตอบ (ค)-(ฉ) ทุกกรณี:
- **R6-1 [ข้อเท็จจริงจากคอนโซล]** เฟรม `..._TARGET_SPAWN` ออกจริงหรือไม่ (`[G>] <label> (N bytes)`) · N = เท่าไร · เวลา
- **R6-2 [ข้อเท็จจริงจาก hexdump]** พิกัดที่ decode ได้จาก `TARGET_SPAWN` = **ผู้เล่น +100X/+50Y/+0Z** หรือ = **`(1747.52, -7837.70, 931.04)`** · แนบ HUD X/Y จากภาพ H0 มาเทียบ
- **R6-3 [การอ่านผล — เลือกหนึ่งข้อ ห้ามเว้น]**
  1. เฟรมออก + พิกัด player-relative + **เห็นตัวนก** ⇒ ประตูชั้น (2) เปิด อ่านคำตอบ (ค)-(ฉ) ได้เต็มปาก
  2. เฟรมออก + พิกัด player-relative + **ไม่เห็นตัวนก (เห็นแค่จุด/ไม่เห็นเลย)** ⇒ 🔴 **นี่คือข้อมูลใหม่เรื่องระยะวาด/เงื่อนไขเรนเดอร์ของ `0x201F` ไม่ใช่ความล้มเหลวของ damage** · (ค)-(ฉ) ต้องกรอกว่า **non-observed** · **ห้ามเขียนว่า "หลอดไม่ลด"** · **ห้ามปิด GT-035 หรือ GT-036 เป็นผลลบจากข้อนี้** ⇒ redirect: ใบ static เรื่องเพดานระยะวาดโมเดล + ทดลอง dx/dy ที่สั้นลง **ก่อน**กลับมา attended
  3. เฟรมไม่ออก **หรือ** พิกัดเป็น placement จริง ⇒ **เลนผิดท่า/บูตผิดเลน = NO-RESULT เชิงโครงสร้าง** ยกเลิกรอบ · **ห้ามอ่านเป็นข้อมูลเรื่องระยะวาด** (ข้อ 6b ควรดักได้ตั้งแต่ก่อนบูต — ถ้าหลุดมาถึงตรงนี้ ให้จดว่าข้อ 6 พลาดตรงไหน)
- 🔴 **[ปรับโดย chief R164 หลัง GT-035 PASS: ข้อนี้ปิดเฉพาะครึ่งเดียว]** `dx100/dy50` (~111 หน่วย) **ยืนยันด้วยตาแล้วสองผู้สังเกตว่าอยู่ในระยะวาด** ⇒ ครึ่ง "วาดได้ไหม" ปิด · 🔴 **ครึ่ง "ระยะเท่าไร" ยังไม่มีใครวัด และขนาดที่เห็นบนจอขึ้นกับระยะซูมกล้อง ไม่ใช่ระยะถึงขอบตัด** ⇒ **offset อื่นไม่ได้รับมรดกข้อนี้** · ถ้อยคำเดิมที่ถูกแทน: ~~ยังไม่เคยมีใครยืนยันด้วยตาว่าอยู่ในระยะวาดโมเดล** — เป็นค่าที่เลน arena ใช้อยู่เท่านั้น ไม่ใช่ระยะที่พิสูจน์แล้ว ⇒ P1 ยังเป็นคำทำนายจริง และ R6-3 ข้อ 2 คือผลที่มีค่าในตัวเอง ไม่ใช่ความล้มเหลว~~


### 🆕 อัปเดต R162-b (2026-08-25 ~12:2x +07:00) — ตัวเลขจริงของเลนที่ build เสร็จ + สามข้อที่ `pf-adversary` จับได้

**เลน `HYP-PF-038` build เสร็จแล้วในรอบเดียวกัน** (PR ของ repo โค้ดเปิดแล้ว รอ gate) · บล็อกนี้แก้ตัวเลข/ข้อความในใบให้ตรงกับสิ่งที่ merge จริง

**① ตัวเลขที่จะเห็นบนจอ — ไม่ใช่ที่ใบเคยเสนอ อ่านก่อนกด**
| | ใบเสนอไว้ (R159 §③) | เลนที่ build จริง |
|---|---|---|
| ขั้นแรก | หลอดลงมา ~60% | **ลงมา 2893 = 75.0%** (ลดลง 25% ของหลอด) |
| ขั้นสอง | ~20% | **ลงมา 771 = 20.0%** ✅ ตรง |
| damage | (ไม่ระบุ) | `HIT_WEAK` **-964** · `HIT_STRONG` **-2122** |
🔴 **ส่วนต่างนี้เป็นการเบี่ยงจากใบ และ chief ประกาศตรงนี้ตามที่ใบสั่งให้ประกาศ** — เหตุผล: โปรไฟล์ผู้โจมตีต้องให้เลขที่ **สูตรเดิมคำนวณออกมาได้พอดี** (ห้ามแต่งเลขนอกเครื่องคิดเลข) และคู่ที่ลงตัวที่สุดกับ defender lv27/con22 ให้ 75/20 · **ขั้นแรก 25% ของหลอดยังใหญ่พอที่ตาคนเห็นชัด** (เทียบกับ 1.6% ของ ladder เดิม)

**② 🔴 การ์ด "เลือกตัวละครผิด" มีจริงแล้ว (ก่อนหน้านี้ไม่มี — adversary จับได้ก่อน commit)**
เลนปฏิเสธทุกกรณีที่ผู้เล่นที่เลือกไม่ใช่ identity `0x10010001:0` (`Arena01` ตัวเดียวกับที่ pre-flight ในใบสั่งให้เช็ค) ⇒ event `hostile_hp_link_hypothesis_identity_not_pinned_no_reply` · **ไม่มีไบต์ออกเลย**
⇒ ประโยคในใบที่ว่า *"เลือกตัวละครผิด = ไม่มีไบต์ออกเลย"* **ตอนนี้เป็นความจริงที่มีโค้ดรองรับ** (ก่อนรอบนี้เป็นเพียงความคาดหวัง)
· การ์ดใหม่อีกตัว: ถ้าตัวละครอยู่คนละ scene กับแถว placement ⇒ `..._wrong_scene_no_reply` · เงียบเหมือนกัน

**③ 🔴 ข้อจำกัดของตัวคุม MISS ที่ใบยังไม่ได้เขียนไว้ — กระทบคำถาม (จ) โดยตรง**
เฟรม `TARGET_HP_AFTER_WEAK` กับ `TARGET_HP_AFTER_MISS` **เป็นไบต์เดียวกันเป๊ะ** (ตั้งใจ) ⇒ ระหว่างสองจุดนั้น **บนจอไม่มีอะไรเปลี่ยนเลย**
⇒ ในชั้น (2) **"ไคลเอนต์รับ MISS แล้ววาดค่าเดิมซ้ำ" กับ "เฟรมไม่ถึง/ถูกทิ้ง" ให้ภาพเหมือนกันทุกประการ** — แยกไม่ได้ด้วยตา
· ⇒ คำตอบข้อ **(จ)** ให้ตอบเท่าที่เห็นจริง (กระพริบ/ไม่กระพริบ) แล้ว **ห้ามสรุปว่าไคลเอนต์ "รับ" หรือ "ไม่รับ" เฟรม MISS จากภาพ**
· ตัวแยกมีที่เดียวคือ **ชั้น (1): นับบรรทัด `[G>]` ให้ครบ 7 ใบ** ⇒ ถ้าครบ 7 แปลว่าเฟรมออกครบ ที่เหลือเป็นเรื่องของไคลเอนต์
· 🟢 **สิ่งที่ตัวคุมซื้อได้จริงและยังแข็งแรง:** แยก "หลอดขยับ **6 วิหลัง** เฟรมเลข" ออกจาก "ขยับ **ที่** เฟรมเลข" — ซึ่งคือคำถาม (ง) และเป็นข้อที่ใบให้ค่าสูงสุด

**④ ลำดับ label ยืนยันแล้วว่าตรงกับที่ใบเขียนไว้** — 7 ใบจบที่ `..._TARGET_HP_AFTER_STRONG` (ไม่มี `TARGET_HP_ZERO_DYING` / `TARGET_DYING_ELAPSED` ในเลนนี้) · ค่า `max_hp` ในทุกเฟรม actor = **3857** · เฟรม `TARGET_SPAWN` มี ASCII `Tornado Eagle` + preset `M011_000_000_SP3` และเป็นเฟรมเดียวที่มี MovementAttr

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

## 🆕 GT-037 LOOT-ROLL-001: server-side loot roller จาก client tables  [✅ **DONE — chief รอบ 113 (cloud) build เสร็จ · เขียว(cloud sanity) 992 pass · gate Actions ตัดสินแล้ว: โค้ดอยู่บน `main` ที่ `74b8add` พร้อมคำตัดสิน `conclusion=success` (ยืนยันรอบ 117) — ไม่มีอะไรค้างรอใครอีก**]

ตาม ORDER ลำดับ 4 = ดราฟต์ R100 §3 ประตู 2 · pure logic + unit tests ถึง Grade A ได้โดยไม่มี client · ไม่มีอะไรให้ผู้เทสทำในรายการนี้
✅ **รอบ 113 ส่งมอบ:** `src/pirateforce_foundation/loot_roll.py` + 66 เทส + verifier 30 guards + fixture + `reports/PF_LOOT_ROLL001_SERVER_SIDE_ROLLER_20260820.md` · DROPS_QUEST = named refusal โดยเจตนา (client มี 311/2478 ชุด) · **ยังไม่มีทางส่งผล roll ถึงผู้เล่น** (Door 3/4 ไม่มี wire path) · coverage `monster_spawn_and_loot` ยัง `not_started` — ถูกต้องตามกติกา (ไม่มี client เห็นสักไบต์)
🔎 **re-derive คำตัดสินได้ตลอด:** `git show origin/ci-status:ci/74b8add309cd2f7b5e7626393652c36582cb00dd.json`
ต้องเห็น `"conclusion": "success"` และ `"sha"` ตรงกับชื่อไฟล์ · ถ้าอยากได้ commit เขียวล่าสุดของ `main` ใช้
`py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch` (เครื่องมือรอบ 117)

## 🆕 GT-038 DAMAGE-TARGET-AB-001: A/B — การคลิกเลือกเป้าเกี่ยวอะไรกับเลขที่มองเห็นไหม  [✅ **PASS — 2026-08-22 23:24 (+07:00): target selection ไม่ใช่เงื่อนไขจำเป็นของเลข — ตรงคำทำนาย static R102**]

> ✅ **RESULT 2026-08-22 22:57–23:24 (+07:00) — PASS** (บูต main HEAD `cf81730` worktree สะอาด — tree เดียวกับ green `b665d92` ยืนยันย้อนหลังโดย resolver ของ GT-041 · รอบนี้ไม่ได้รัน resolver ก่อนบูต):
> - แขน A (ไม่เลือกเป้า · ไม่มี `TargetVital`/`ChooseNPC` ใน log): **เห็นเลขแดง `379`** ชัดเจน ≥2 sample
> - แขน B2 (เลือก `Navy Transfer` · `ChooseNPC 0x2001`): **เห็นเลขแดง `63`** (+1.265s เห็นซ้ำสองครั้ง) + **reaction `63`** (~+45.5s/+47.9s)
> - wire ครบ `HIT_WEAK → HIT_STRONG → MISS → HIT_REACTION` ทั้ง A/B1/B2 (label ละ 3 ครั้ง · 95 B ทุกใบ) · canonical ไม่ขยับ
> - 🔴 qualification ติดถาวร: เฟรม transient ที่ไม่ติดภาพ = **non-observed ไม่ใช่ absent** (เอฟเฟกต์สั้นกว่า cadence จับภาพ)
> - รอบก่อนหน้าคืนเดียวกัน (22:40–22:49) = NO-RESULT/BLOCKED-INPUT (เป้าอยู่นอกภาพ) — ไม่ใช่ผลลบ · ผลเต็มสองใบ:
>   `notes_to_chief/20260822_2328_GT038-PASS-TARGET-SELECTION-NOT-CAUSAL.md` + `20260822_2250_GT038-NO-RESULT-BLOCKED-INPUT.md` (บริโภค R123)
> - ✅ ตอบคำถามผู้เทสข้อ 3 (chief R123 ตรวจซอร์สแล้ว): `damage_model_hypothesis_npc_sweep_sent` เป็น `self.events` **ในหน่วยความจำโดยดีไซน์** (`runtime.py:1819` — พินโดย dispatch tests + headless replay) ไม่เคยถูก print ⇒ **เกณฑ์ attended ต้องอ้าง wire label 4 ใบจาก server console เท่านั้น** — ไม่มีบั๊ก ไม่ต้องแก้โค้ด

**ที่มา:** ข้อเสนอผู้เทสในจดหมาย 12:00 (เดิมเรียก GT-034 — เปลี่ยนเลขเพราะชนคำสั่ง Panya) · ปริศนา: สองเซสชันผู้เทสไม่เห็นเลข ทั้งที่ไบต์เหมือนเซสชันของ Panya ที่เห็นครบ · ความต่างที่วัดได้เดียวในล็อก = `TargetVital 0x1ADD` (มีเฉพาะเซสชันที่เห็นเลข)
**static R102 (`FACTPACK_R102_TARGETVITAL_AND_FXNUMBER_GATES_STATIC.md`) ตอบล่วงหน้า [PROVEN]:**
- สมมติฐาน (ก) "ต้องเลือกเป้าก่อนเลขถึงขึ้น" = **หักล้าง** — เลขขึ้นเพราะ performer==localplayer + resolve `0x2001` สำเร็จ · TargetVital เป็นแค่**พยาน**ว่า `0x2001` resolve ได้ (common cause) ไม่ใช่สาเหตุ
- สมมติฐาน (ข) "TargetVital ใบหลังเป็นผลของเฟรม HIT_REACTION" = **หักล้าง** — subtree ของ CHitResult ไม่มีทางเรียก send TargetVital
- เกตที่อธิบายจอมืดได้จริง: ① resolve `0x2001` ล้มเหลว ณ เวลาเฟรม (timing การลงทะเบียน) ② **toggle `[localplayer+0x420]` = 0** (ดูบทเรียนเครื่องมือ ⬇)
**โปรโตคอล (บูตเดียว · scenario `damage_model_hypothesis_npc_sweep.json` เดิม):** แขน A = ไม่แตะเมาส์เลยหลังเข้าแมพ ยิง trigger · แขน B = คลิกเลือก NPC (`Navy Transfer`) ก่อน แล้วยิง trigger รอบใหม่ (relaunch client รีอาร์ม one-shot ระหว่างแขน)
**ข้อบังคับทั้งสองแขน:** กล้องเห็นผู้เล่น+NPC เต็มตัว · **ห้ามพิมพ์อะไรนอกช่องแชตที่โฟกัสแล้ว** (กัน hotkey 0x27) · ใช้ client ที่เพิ่งเปิดใหม่ (toggle default ON)
**คำทำนาย static:** ทั้งสองแขน**ควรเห็นเลขเท่ากัน** — ถ้าแขน A มืดแต่ B เห็น = static ผิด จดละเอียด · ถ้ามืดทั้งคู่บน client ใหม่ = ปัญหาคือ resolve-timing ไม่ใช่ toggle
**pass criteria สองชั้น:** ① wire: เฟรมครบทั้งสองแขน ② client: บันทึกเลขเห็น/ไม่เห็น ต่อแขน + มี/ไม่มี `TargetVital` ในล็อกต่อแขน
## 🆕🎯 GT-039 NPC-HP-LINK-001: **หลอดเลือดของ "เป้าหมาย" ลดจริงไหม**  [✅✅ **PASS — รอบใหญ่ #11 (UNATTENDED) 2026-08-21 02:05–02:25 · HEAD `cc46a03`**]

> ### 🏆 **ครั้งแรกในประวัติโปรเจกต์ที่ HP ของ "เป้าหมาย" ขยับ**
> **แถบเลือดของ NPC ลด `100 → 37 → 0` ตรงตามค่าที่เซิร์ฟเวอร์ส่ง และ NPC ล้มจริง**
> · 8 เฟรมครบเรียงถูกทุกใบ · **`grep -c 28317` = 0** ⇒ **การสลับสองสายพานในเซสชันเดียวไม่พัง**
> (นี่คือความเสี่ยงเฉพาะที่คิวใบนี้เตือนไว้เอง — ตอบแล้วว่าไม่เกิด)
> · `MISS` ไม่ทำให้ HP ขยับ — ค้าง 37 สังเกตได้ 4 ภาพติด (ตัวควบคุมทำงาน)
> · teardown สะอาด · canonical sha ไม่ขยับ · ผลเต็ม: `notes_to_chief\20260821_0225_GT039-RESULTS-and-teardown-template-bug.md`
>
> ⭐ **คำตอบของคำถามที่ค้างมาตั้งแต่รอบ 83:** client ไม่ลบเลขเอง — **แต่มันเชื่อสิ่งที่เซิร์ฟเวอร์บอก**
> ⇒ วง "ตี → เลือด → ตาย" ปิดครบบนเป้าหมายจริงแล้ว
> 🔴 **nonclaim ที่ยังต้องติดทุกครั้ง: เลขคณิต บันได และการเชื่อม เป็นดีไซน์ของเรา**
> **ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** · ยังไม่ใช่ combat จริง (NPC ไม่โจมตีกลับ) · HP ไม่ persist
> 🟡 ข้อที่ยังไม่ปิด: ไม่มีวิดีโอ/พยานตาเปล่ารอบนี้ (unattended ตามที่ประกาศไว้ตอนถือธง)

<details><summary>ข้อความตอน PENDING (เก็บไว้ทั้งก้อน — เป็นคำทำนายที่ตรวจสอบย้อนได้)</summary>

[🟢 เดิมเป็น PENDING — พร้อมรันหลัง commit ของ chief รอบ 111 (จ็อบ 178 · HYP-PF-029) — อ่าน SHA จาก `outbox\178_round111_*`**]

#### (ฉบับ PENDING ที่ chief cloud รอบ 114/117 ปรับท่าบูต — เก็บไว้ทั้งก้อน)

🗄 (หัวข้อเดิมตอน PENDING — เก็บไว้เป็นคำทำนายที่ตรวจย้อนได้) 🆕⭐ GT-039 NPC-HP-LINK-001: **หลอดเลือดของ "เป้าหมาย" ลดจริงไหม** — ชิ้นกลางที่วิดีโอรอบใหญ่ #10 พิสูจน์ว่าหายไป  [🟢 **PENDING (HYP-PF-029) — บูตที่ commit ที่ `pf_resolve_green_boot.py` ชี้ให้ (ดูบล็อก 🔎 ใต้หัวข้อ)** · โมดูล + scenario + dispatcher + CLI flag เข้า main ตั้งแต่ `cc46a03` (CI success run 32406182274) · แก้ pointer chief รอบ 114 (เดิมชี้ `outbox\178_round111_*` ซึ่ง gitignored หา SHA ไม่ได้) · แก้ท่าบูต chief รอบ 117 (ประโยคเดิม "HEAD ล่าสุดที่ ci-status = success" **รันไม่ได้แล้ว** — เหตุผลอยู่ในบล็อกใต้หัวข้อ) · เนื้อการทดสอบและ pass criteria ไม่เปลี่ยนแม้แต่ตัวเดียว]

> 🔎 **หา SHA ที่จะบูต — ใช้เครื่องมือรอบ 117 อย่า hard-pin และอย่าอ่านที่ HEAD:**
> `py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch`
> (รันจากโฟลเดอร์ `pf_bridge` · แทน `C:\path\to\pirate-force-server` ด้วยพาธ clone จริงบนสะพาน · คำสั่งเป็น ASCII ล้วน ปลอดภัยกับคอนโซล cp874)
> - **exit 0** + บรรทัด `BOOT_COMMIT: <sha>` ⇒ บูต sha นั้น: `git checkout <sha>` (detached HEAD ถูกแล้ว — เราบูต *คำตัดสิน* ไม่ใช่ branch)
> - **exit 3** + `BOOT_COMMIT: NONE` ⇒ **ห้ามบูต** · จดในผลว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · **exit 2** = พาธผิด/git ล้ม
> - 🔴 มีบรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ **จดลงในผลด้วย** (มี commit แดงบนสาย main เหนือคำตอบ)
> - ⚠️ `success` ที่เครื่องมือส่งต่อ = **subset ของ gate บน GitHub runner** ไม่ใช่ "ผ่าน gate เต็ม" (gate จริงอยู่บนสะพาน)
> 🔴 **ทำไมประโยคเดิม ("บูต `origin/main` HEAD ล่าสุดที่ ci-status = success") รันไม่ได้แล้ว:** HEAD ของ `main` หลัง automerge เป็น
> **merge commit** ที่ push ด้วย `GITHUB_TOKEN` ⇒ **ไม่ trigger workflow ⇒ ไม่มีใครเขียน `ci/<sha>.json` ให้มันเลย ตลอดไป**
> (วัดรอบ 116 จาก Actions API · ยืนยันซ้ำรอบ 117 ที่ HEAD `520e2cf`) — นี่ไม่ใช่ "คำตัดสินยังไม่มา" แต่คือ "จะไม่มีใครเขียนให้"
> ⇒ คนที่ทำตามประโยคเดิมจะไม่เจอไฟล์คำตัดสิน แล้ว **ปฏิเสธการบูตอย่างถูกกฎ** ทั้งที่โค้ดเขียวนั่งอยู่ต่ำลงไปแค่คอมมิตเดียว
> ⇒ เครื่องมือจึง **เดินไล่ ancestor** ให้ แทนการ lookup ที่ HEAD (ค่าปริยาย: `origin/main` · `origin/ci-status` · ย้อน 60 commit)
> **ยืนยันด้วยมือ (ทำได้ ไม่บังคับ · แทน `<SHA>` ด้วยเลขที่เครื่องมือให้):**
> `git show origin/ci-status:ci/<SHA>.json` ต้องเห็น `"sha"` ตรงชื่อไฟล์ **และ** `"conclusion": "success"` (สี่กฎการอ่าน ci-status)
> `git grep -n "npc-hp-link-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py` ต้องเจอบรรทัดจริง
> 🔴 **ห้ามใช้ `--help` เป็นหลักฐานว่ามี flag** (คืน 0 บรรทัดผ่านสะพาน — บทเรียนรอบใหญ่ #7 ข้อ 6)
> ถ้า sha ที่เครื่องมือชี้ **ไม่มี** โมดูล `npc_hp_link_hypothesis.py` (มีตั้งแต่ `cc46a03`) ⇒ **หยุดและรายงาน** อย่าไล่ลง commit เองด้วยมือ

</details>

**ที่มา (นี่คือเทสที่เกิดจากผลของพวกท่านโดยตรง):** รอบใหญ่ #10 ที่ Panya ขับเอง ยิงใส่ `Navy Transfer` `0x2001` โดย**คลิกเลือกเป้าก่อน** ⇒ แถบ HP ของเป้าอยู่บนจอตลอดทั้งรอบ · ดาเมจสะสม **63 + 379 + 63 = 505** · **แถบไม่ขยับแม้แต่หน่วยเดียว** (100 Lv.1 เต็มหลอด ทั้งก่อนและหลัง) ⇒ ตอกย้ำรอบ 83: **client ไม่ลบเลขเอง เป็นตัวแสดงผลล้วน ๆ**
⇒ เลนใหม่นี้คือคำตอบตรง ๆ ของผลนั้น: **เซิร์ฟเวอร์พูดทั้งสองครึ่งเอง** — ทำเลขคณิต HP ของ *เป้าหมาย* เอง (100 − 63 = 37 → clamp 0) แล้วสลับสองสายพานส่งออก 8 เฟรม
🆕 **ของใหม่ที่ไม่เคยมีในโปรเจกต์:** GT-031 (HYP-PF-026) เดินบันได HP ของ **ผู้เล่นเอง** บนสายพาน VitalData เท่านั้น — **ไม่เคยมีเลนไหนขยับ HP ของเป้าหมาย** เลนนี้เป็นเลนแรก และเป็น**เลนแรกที่สลับสองสายพานในเซสชันเดียว** (VitalData `+0x18` สำหรับเฟรมเลข · actor-entry `+0x1C` actor_type 4 สำหรับเฟรมหลอด)
⭐ **nonclaim ที่ต้องติดทุกผล: เลขคณิต บันได และการเชื่อม เป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** · ไม่มี capture ใบไหนในคลังแสดงว่า HP ของเป้าขยับตามดาเมจ ไม่ว่าทางใด

**boot (ท่าเดียวกับ GT-027/031 เป๊ะ เปลี่ยนแค่ flag):**
- `--npc-hp-link-hypothesis-scenario scenarios\npc_hp_link_hypothesis_target_sweep.json` (+ `--db` สำเนาตามปกติ)
- trigger เดิม: แชต **ascii 12 ตัวเป๊ะ** → sweep **8 เฟรม ห่างกัน 6 วิ/เฟรม (42 วิทั้งชุด)**
- 🔴 **6 วิเป็นความตั้งใจ ไม่ใช่ความพลาด** — ตามคำสั่ง Panya 2026-08-20: *เลิกยืดระยะเฟรมเพื่อผู้เทส* เพราะตัวเหตุการณ์เองสั้น ไม่ใช่เฟรมถี่เกินไป · **ทางแก้ที่ถูกคือถ่ายวิดีโอ** (พิสูจน์แล้วสองรอบว่าได้ทั้งภาพคมและนาฬิกาที่ไม่ใช่ของผู้เทสเอง)
- console label = `HYP_PF_029_NPC_HP_LINK_<STEP>` · event = `npc_hp_link_hypothesis_target_sweep_sent` — เห็นชื่ออื่น = บูตผิดไฟล์
- **one-shot** — ยิงซ้ำได้ `..._already_sent_no_reply` (relaunch client เพื่อรีอาร์ม)

**🔴 ข้อบังคับก่อนยิง — ข้อนี้คือสิ่งที่ทำให้รอบใหญ่ #10 มีค่า อย่าข้าม:**
① **คลิกเลือก NPC `Navy Transfer` ก่อนเสมอ** เพื่อให้**แถบ HP ของเป้าโผล่บนจอ** (ยืนยันใน client log ว่ามี `TargetVital 0x2001 'Navy Transfer'`) — ไม่เลือก = ไม่มีแถบให้ดู = เทสทั้งใบเสียเปล่า
② **ถ่ายวิดีโอทั้ง 42 วินาทีต่อเนื่อง** ตั้งแต่ก่อนกด trigger — ไม่ใช่ภาพนิ่งรายเฟรม
③ กล้องเห็นทั้งตัวผู้เล่น · NPC · **แถบ HP ของเป้า** · และแถบ HP ผู้เล่น ในเฟรมเดียว
④ client ที่เพิ่งเปิดใหม่ · ห้ามพิมพ์อะไรนอกช่องแชตที่ยืนยันโฟกัสแล้ว (กัน hotkey 0x27)

**สิ่งที่ควรเห็นทีละเฟรม (คำทำนาย — ไม่ใช่ข้อเท็จจริง):**
| t | เฟรม | สายพาน | ถ่าย/ดูอะไร |
|---|---|---|---|
| +0s | `TARGET_SPAWN` hp 100/100 | actor-entry | NPC อยู่ครบ แถบเป้า 100 (ถ้ากระพริบ/รีสปอว์นให้จด) |
| +6s | `HIT_WEAK` เลข **63** flags 0x0001 | VitalData | เลขลอยบน NPC · **แถบเป้าต้องยังไม่ขยับ** — ถ้าขยับที่เฟรมนี้ = หักล้างรอบ 83 ทั้งเลน จดละเอียดสุด |
| +12s | `TARGET_HP_AFTER_WEAK` hp **37**/100 | actor-entry | ⭐⭐ **แถบของเป้าลดเหลือ 37 ไหม — นี่คือคำถามเดียวของเทสทั้งใบ** |
| +18s | `MISS` flags 0x0000 | VitalData | marker `MISS!` ขึ้น (texture `bm_miss.tga`) · แถบค้าง 37 |
| +24s | `TARGET_HP_AFTER_MISS` hp 37 ซ้ำ (**ไบต์เหมือนเฟรม +12 เป๊ะ**) | actor-entry | แถบค้าง 37 · client กระพริบ/รีเฟรชไหมเมื่อได้ค่าที่ถืออยู่แล้ว (มีค่าทั้งสองทาง) |
| +30s | `HIT_STRONG` เลข **379** flags 0x0001 | VitalData | เลขลอย · แถบยังไม่ขยับ |
| +36s | `TARGET_HP_ZERO_DYING` hp 0 + death timer 20.0 **ในเฟรมเดียว** | actor-entry | แถบเป้า 0/100 + **วงนับถอยหลังเหนือ NPC** (เหมือน GT-021/029) — clamp: 37−379 = floor 0 |
| +42s | `TARGET_DYING_ELAPSED` timer 0.0 | actor-entry | เลขในวงหายไป NPC ยังนอน ไม่มีอะไรเกิดต่อ (พฤติกรรมเดิมของ GT-029 — **ไม่ใช่บั๊ก**) |

**pass criteria สองชั้น:**
① **wire** = 8 เฟรมครบตาม label + delay ใน console + event `npc_hp_link_hypothesis_target_sweep_sent` ใบเดียว
② **client-observable** = ตอบสามข้อ: **(ก) แถบของเป้าลดเป็น 37 ที่ +12 หรือไม่** · (ข) แถบขยับตอนเฟรมเลข (+6/+30) หรือไม่ · (ค) วงนับถอยหลังเปิดที่ +36 เหมือนตอน GT-029 ที่รันแยกไหม
🔴 **ผลลบมีค่าเท่าผลบวก** — "เลขขึ้นครบแต่แถบไม่ลดเลยแม้เซิร์ฟเวอร์ส่ง ActorAttr hp 37" = คำตอบที่ชี้ขาดพอ ๆ กัน และแปลว่าปัญหาไม่ได้อยู่ที่ "ใครทำเลขคณิต" แต่อยู่ที่ทางเข้า reconcile ของ actor ที่รู้จักแล้ว **จดเป็นผล ไม่ใช่ fail**

**⛔ เกณฑ์หยุด / ตื่นเต้นพิเศษ:**
- แถบลด **ก่อน** เฟรม hp (คือลดตอนเฟรมเลข +6/+30) = **หักล้าง "client ไม่ลบเอง" ของรอบ 83** — ผลลบที่มีค่าที่สุดที่เป็นไปได้ · วิดีโอช่วง +6..+12 คือหลักฐานชิ้นเอก
- 🔴 **`ErrorData=28317` ในล็อก = การสลับสองสายพานในเซสชันเดียวพัง** — เลนนี้เป็นเลนแรกที่ทำ ⇒ นี่คือความเสี่ยงเฉพาะตัวของเทสใบนี้ **หยุด จด แล้วเก็บ console log ทั้งไฟล์** (headless พิสูจน์แล้วว่าประกอบไบต์ได้ถูก แต่ **ไม่มี client ตัวไหนเคยเห็นไบต์ชุดนี้แม้เฟรมเดียว**)
- NPC หายไปทั้งตัวแทนที่จะแค่ HP ลด = จด แล้วดูว่าเป็นที่เฟรมไหน

**หลังจบ:** ถ่ายภาพปิดท้าย → ปิด client ตาม PLAYBOOK → **teardown เสมอ แม้รอบจะจบเพราะเลิกเล่น** (บทเรียนรอบใหญ่ #10: ไม่ teardown = ชั้น wire หายถาวร) · ถ้าเลยเวลาไปแล้ว ใช้ `-Salvage` ของ template teardown (ดู `HOWTO_SALVAGE_A_DEAD_ROUND.md` — ของใหม่รอบ 111)

**nonclaims บังคับ:**
- สูตร/บันได/การเชื่อม **เป็นของเรา** ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล
- **ไม่ claim ว่า HP ของ NPC persist** — ไม่มีคอลัมน์ HP ให้เขียน balance ตายพร้อม sweep
- ไม่ใช่ combat จริง — **ไม่มี NPC โจมตีกลับ** (แถว mob_aggro ยัง not_started) · ผู้เล่นไม่ได้เป็นคนสั่งตี เซิร์ฟเวอร์เป็นคนเล่าเรื่อง
- ไม่ claim path คืนชีพ/ลูท/XP
- **ผลของรอบใหญ่ #10 ที่เป็นที่มาของเลนนี้ = ชั้น client-observable เท่านั้น** (ไม่มี teardown ⇒ ไม่มีหลักฐานชั้น wire เลย) — บันทึกเต็มพร้อม sha256 ของภาพทั้งห้าใบอยู่ที่ `reports\PF_NPC_HP_LINK029_GT027_RERUN_ATTENDED_RESULT_20260820.md` (ของใหม่รอบ 111)

## 🆕🔬 GT-040 DROPTHING-TRANSPORT-PROBE-001 [STATIC-ON-BRIDGE]: "วัตถุลูทบนพื้น" มี transport อยู่ในอิมเมจจริงไหม — สามจุดที่ยังไม่มีใครเปิดสักครั้ง  [✅ **DONE — ผู้ช่วยของ Panya ปิดครบสามท่อน A/B/C (2026-08-21 09:36-09:56 +07:00) · ผลเต็ม: `notes_to_chief/20260821_09{36,51,56}_GT040-PART-{A,B,C}-RESULTS-from-assistant.md` · บริโภค+ตรวจสอบเอกสารโดย chief R120 · ✅ GT-042 ปิดแล้ว (PASS 2026-08-23 พร้อม erratum ขอบเขต handler: len 47 ไม่ใช่ 712) ⇒ ข้อห้ามเขียนโมดูล/encoder **ปลดเฉพาะแถวที่รอด re-derive/ขอบเขตที่แก้แล้ว** — ดู GT-042**]

**หมวด:** `STATIC-ON-BRIDGE` — งานที่ **ต้องเปิด `GameClient.local.bin`** จึงทำบน cloud clone ไม่ได้เลย
ผู้รับงานคือคนที่นั่งอยู่หน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม · **ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว** (ดู "ชั้น ②" ด้านล่าง)

**ที่มา:** รอบ 113 ส่ง **ประตู 2** ของดีไซน์ลูทรอบ 100 เสร็จ (`src/pirateforce_foundation/loot_roll.py`
= loot roller ฝั่ง server, Grade A บน pure logic — GT-037 ✅ DONE) · รอบ 115 สำรวจ **ประตู 3 "ของลูทโผล่บนพื้น"**
แล้วพบว่า **ทำบน cloud ไม่ได้เลยสักข้อ** — ทุกคำถามที่เหลือต้องอ่านไบต์จากอิมเมจ
⇒ ใบนี้คือใบสั่งที่ปลดล็อกประตู 3/4 · 🔴 **การเขียนโมดูลก่อนได้คำตอบ = การประดิษฐ์ wire format ขึ้นเอง ซึ่งบ้านนี้ห้าม**
⇒ **ใบนี้ขอ "ข้อเท็จจริง" เท่านั้น ไม่ขอดีไซน์ ไม่ขอโมดูล ไม่ขอ encoder**

### objective (claim เดียวที่ใบนี้พิสูจน์)
**อิมเมจของ client มีทางส่ง/ทางเก็บ "วัตถุบนพื้น" (ground thing) อยู่จริงหรือไม่** —
ตอบด้วยการเปิดสามจุดที่ยัง `[UNKNOWN]` แล้วบอกว่าแต่ละจุด **มี** หรือ **ไม่มี**
🔴 **ผลลบคือคำตอบเต็มใบ ไม่ใช่ความล้มเหลว** (ดูบล็อกผลลบท้ายใบ)

### 🔒 ข้อเท็จจริงที่ "ปิดแล้ว" — ห้ามเอาใบนี้ไปรื้อซ้ำ
- **[NEGATIVE, ปิดสนิท] ท่อ actor-entry ส่งของบนพื้นไม่ได้** — jump table `0x4469BD` รับ `actor_type`
  **เป๊ะ ๆ แค่ 2..6** (`add eax,-2; cmp eax,4; ja -> return NULL`, entry ที่ไม่เข้าเงื่อนไข **ถูกทิ้งเงียบ**)
  2=`CNetActor` · 3=`CMyActor` · 4=`CNetNPC` · 5=`CAvatarNPC` · 6=`Pet` — **ไม่มีเคสของ item/object เลย**
  ที่มา: `pf_bridge\FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md` — **grep คำว่า `0x4469BD` แทนการนับบรรทัด**
  (เลขบรรทัดขยับแล้วเพราะ ERRATUM ของรอบ 115) ⇒ **ห้ามเสียเวลาไล่หา actor_type ตัวที่ 7** มันไม่มี
- **[NEGATIVE, re-derive แล้วรอบ 115] ไม่มีชื่อ DropThing/Pickup ในทะเบียนชื่อของเราเลย** —
  0 hit ใน `pf_bridge\VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` และ 0 hit ใน
  `pirate-force-server\docs\PF_VITAL_NAMES.json` ⇒ **อย่าไปค้นสองไฟล์นั้นซ้ำ** ต้องอ่านอิมเมจอย่างเดียว

### 📌 ข้อแก้ที่ต้องอ่านก่อนหยิบ citation เก่า (✅ **merge แล้ว** — ฝั่ง repo โค้ดเข้า `main` ที่ `24d5b94` ซึ่งมีคำตัดสิน `conclusion=success` · ยืนยันรอบ 117)
`DropThingBoard` และ `DropThingGameObj` **ไม่ได้อยู่ใน 521-class registration join** — ทั้งคู่ `literal_kind=none`
และ `in_round86_census=False` (`pf_bridge\FACTPACK_L2_CLASSCENSUS001_20260820.tsv:482,483`)
ส่วน 521 join นิยามไว้ว่า "มี **ทั้ง** RTTI type descriptor **และ** runtime name literal ใน `.rdata`"
(`FACTPACK_L2_CLASSCENSUS001_20260820.md:34`) ⇒ สองตัวนั้นเป็น **RTTI descriptor ล้วน ๆ** เข้าไม่ได้
มีแค่สองตัวนี้ที่ถือ runtime literal จริง:

| คลาส | บรรทัดใน tsv | literal VA | ใช้เป็นหลักฐานอะไรได้ |
|---|---|---|---|
| `DropThingModule_Client` | `:484` | `0x00F0BAD0` | มี literal (ยังไม่พิสูจน์ว่าถูก register) |
| `PickupTerrainThing` | `:1003` | `0x00F3093C` | มี literal **และ** registration พิสูจน์แล้ว (ท่อน C) |

ข้อความ erratum เต็มอยู่ใน `FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md` (ERRATUM E1, รอบ 115)
🔴 **ใบนี้ไม่ได้พึ่ง erratum ในการทำงาน** — ทั้งสามท่อนอ่านจากอิมเมจตรง ๆ · erratum แค่กันไม่ให้ใครหยิบ
citation ผิดไปอ้างว่า "DropThingBoard/GameObj ถูก register แล้ว" · ⏳ ถ้ายังหา erratum ไม่เจอบน `main` = PR ยังไม่ merge ทำงานต่อได้ตามปกติ

### สิ่งที่ต้องมี (precondition)
- **อิมเมจ:** `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · PE32 · ImageBase `0x00400000`
  (ค่าอ้างอิงจาก `pf_bridge\factpack_L1\MANIFEST.md:21-22`) — 🔴 **จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง เปิดอ่านอย่างเดียวเสมอ**
- **ไม่ต้องมี:** เซิร์ฟเวอร์ · client ที่บูตแล้ว · canonical DB · สำเนา DB · `LOCK_GAME` · teardown · boot stamp
  ⇒ ใบนี้ **ไม่ใช่รอบเทสในเกม** กติกา stamp 420 นาที (เดิม 180)/teardown ไม่เกี่ยวกับใบนี้เลย
- **capture corpus:** ไม่บังคับ · หยิบมาได้ถ้าอยากเช็คว่าเคยมีเฟรมรูปร่างนี้ผ่านสายจริงไหม (คาดว่า 0 — ถ้าเจอ **นั่นคือข่าวใหญ่ จดทันที**)
- **ท่าทำงาน:** ตามวินัยของ `pf-static-re` (`pf_bridge\.claude\agents\pf-static-re.md`) และเมธอดของ
  RUNTIMERES-ACTOR-ENTRY-001: 🔴 **ห้ามใช้ linear disassembler เป็นหลักฐานของ negative** (มันหยุดที่ไบต์แรกที่ decode ไม่ได้
  แล้วรายงาน negative อย่างมั่นใจ = ความผิดพลาดรอบ 83 เป๊ะ ๆ) · ให้ census ด้วย byte matching (`E8`/`E9 rel32` ทุกออฟเซ็ต ·
  dword sweep ทั้งไฟล์สำหรับ table/vtable/immediate) · **สวีปทั้งสอง executable section: `.text` (`0x401000`) และ `.code` (`0xC3A000`)**
- **บันทึกต้นทุน:** สามแถวของ Door 3/4 ลงใน `pf_bridge\IMAGE_ACCESS_COST.tsv` แล้วโดยรอบ 115

### steps — สามท่อน **แยกจ็อบ แยกผล อย่ารวม** (ทำตามลำดับความสำคัญ A → B → C)

**ท่อน A (สำคัญสุด) — สอง derived bit ของ `0x6E9D` ที่ยังไม่มีใครเปิด**
พาหะ: `GSCN_RunTimeProtocolRes` · literal `0xF2FFF8` · id `0x6E9D` (=28317) · vtable `0xF2FFC0` · sizeof `0x28` ·
Serialize `0x5E3EE0` (เรียก base `0x5F4070` ก่อน) · inbound handler `0x5E4060` → `0x446F30`
bit `0x02`/obj `+0x1C` = actor-entry collection = **decode แล้ว ไม่ต้องแตะ**

| derived bit | object | sub-serializer | สถานะวันนี้ |
|---|---|---|---|
| `0x04` | `+0x24` | `0x5E2960` | **ยังไม่ decode** · ฝั่ง inbound รู้แค่ว่า `[+0x10]` → `[0x1093198]+0x7BC` · `[+0x14]` → `0x5F6B70` · `[+0x18]` → `[actor+0x574]` |
| `0x08` | `+0x20` | `0x5F85B0` | **ยังไม่ decode เลยแม้แต่บรรทัดเดียว** |

(ที่มาของตาราง: `pirate-force-server\reports\PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md:54-55`
และรายการ "explicitly not examined" ที่ `:343`)

1. decode `0x5E2960` และ `0x5F85B0` ให้ได้ **ตารางฟิลด์** (tag ไบต์ · offset ในอ็อบเจกต์ · ชนิด) —
   **รูปแบบคำตอบที่นับว่าเป็นคำตอบ = ตารางหน้าตาเดียวกับ disassembly ของ `StallOperateVital` ที่**
   `pirate-force-server\reports\PF_USE_DROP_SELL001_ITEM_OPERATE_USE_DROP_SELL_STATIC_20260818.md:160-166`
2. แนบ span `[start,end)` + sha256 ของ span ทุกอันที่อ้าง (cross-check กับ `factpack_L1\blocks_256.tsv` ได้)
3. ตอบคำถามเดียวของท่อนนี้: **สอง sub-object นี้ พา "อ็อบเจกต์ที่ไม่ใช่ actor" มาด้วยไหม**
   (เช่นอ้าง literal VA `0x00F3093C` / `0x00F0BAD0`, สร้างอ็อบเจกต์ผ่าน vtable ที่ไม่ใช่ actor 2..6, หรือแตะ terrain/ground container)

**ท่อน B — reconcile/removal pass `0x446FE1..0x4470E5`** (ลูปที่สองของ `0x446F30`)
เหตุผลที่ต้องเปิด: มันคุม **การถอด/อายุของอ็อบเจกต์** และวันนี้มี **[TENSION, UNRESOLVED]** ค้างอยู่ระหว่าง
"V91 = actor-entry list เป็น authoritative membership ต่อ generation" (ละตัวไหน ตัวนั้นหายจากจอ+เรดาร์)
กับ **เฟรม count-1 ที่เลน HYP-PF-023/025 ส่งอยู่ทุกวันนี้** (ถ้า membership authoritative จริง เฟรม count-1 ควรกวาดประชากรที่เหลือหายหมด — ไม่มีใครรายงานว่าเกิด)
ที่มา: `FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md` §4.2 (**grep `0x446FE1`** แทนการนับบรรทัด)

4. decode ลูปนั้นและตอบว่า: มัน diff กับ **สำเนา collection ของเฟรมก่อนหน้า** (singleton `[0x01081A90]+0x154` ตามที่ CHUNK2-Q2 อ้าง)
   หรือ diff กับ actor registry · ต่อ entry ที่ถูกละ มันเรียกอะไร · และ **เฟรม count-1 กวาดประชากรที่เหลือหรือไม่**
5. 🔴 **ของบนพื้นที่โผล่แล้วไม่มีวันหาย ไม่ใช่ฟีเจอร์** — ถ้าท่อน A ได้ผลบวก ท่อนนี้คือสิ่งที่ตัดสินว่าลูทมี "อายุ" ได้ไหม

**ท่อน C — serializer ของ `PickupTerrainThing` (ประตู 4 ฝั่ง request)**
วันนี้มีอยู่แค่ **ชื่อกับที่อยู่**: name VA `0xF3093C` · registration `0xBEE5E5` (ท่า `push <name>` → `call 0x89C080`)
ที่มา: `PF_USE_DROP_SELL001_ITEM_OPERATE_USE_DROP_SELL_STATIC_20260818.md:158` · derived id `0x4543`
**[DERIVED, เลขคณิตล้วน]** จากแฮชชื่อ `sum((i+1)*ord(c)) & 0xFFFF` — **id ที่ derive มาไม่ใช่หลักฐาน**
รายงานใบเดียวกันพิมพ์ serializer เต็มของ `StallOperateVital` ไว้ที่ `:160-166` แต่ **ไม่มีของ `PickupTerrainThing` แม้บรรทัดเดียว**

6. จาก registration `0xBEE5E5` ไล่ไปหา **vtable** ของคลาสนี้ แล้วอ่าน **slot `+0x18` = serializer**
   (ท่าเดียวกับที่ `StallOperateVital` ทำ: vtable `0xF4A418` → `+0x18` = `0x76A630`)
7. พิมพ์ตารางฟิลด์ + span + sha แบบเดียวกับท่อน A ข้อ 1-2

### pass criteria — **สองชั้น แยกกันเด็ดขาด**

**ชั้น ① wire/DB (ไบต์+ดิสแอสเซมบลี — headless ล้วน ไม่ต้องมีคนเฝ้าจอ)**
ใบนี้ผ่านเมื่อ **ทุกท่อนได้คำตอบชี้ขาด ไม่ว่าบวกหรือลบ** โดยแต่ละคำตอบต้องมี VA + span + sha:
- **ท่อน A ผลบวก** = ชี้ได้ว่า bit `0x04`/`+0x24` หรือ bit `0x08`/`+0x20` สร้าง/อัปเดต **อ็อบเจกต์ที่ไม่ใช่ actor ในตาราง 2..6**
  พร้อมตารางฟิลด์ของ `0x5E2960` และ/หรือ `0x5F85B0`
  **ท่อน A ผลลบ** = ทั้งสองบิต decode ออกมาแล้วเป็นข้อมูล scene/zone/กล้อง/สภาพแวดล้อม **ไม่มีการสร้างอ็อบเจกต์** และ
  **ไม่มีการอ้าง `0x00F3093C` หรือ `0x00F0BAD0` เลย** ⇒ ประตู 3 ปิดผ่านท่อนี้ด้วย **อีกหนึ่ง [NEGATIVE] ที่ระบุตัวได้**
- **ท่อน B ผลบวก** = ระบุได้ว่า `0x446FE1..0x4470E5` diff กับอะไร และ **ปิด TENSION** ได้ว่าเฟรม count-1 กวาดหรือไม่กวาด
  **ท่อน B ผลลบ** = static ตัดสินไม่ได้ (เช่นจบที่ vtable dispatch ที่ resolve ชนิดไม่ได้) ⇒ **พูดออกมาตรง ๆ** ว่า
  ทางเดียวที่เหลือคือ membership-omission GT ที่มีขอบเขต บน identity เดียวที่รู้จัก — **นั่นจะเป็นใบใหม่ ไม่ใช่ใบนี้**
- **ท่อน C ผลบวก** = ได้ **serializer VA จริง** + ตารางฟิลด์ + span sha ของ `PickupTerrainThing`
  **ท่อน C ผลลบ** = slot `+0x18` เป็น stub/ตกไปที่ base หรือหา vtable ไม่เจอ ⇒ ประตู 4 **ยังไม่มีรูปร่าง request ให้สร้าง** คงสถานะ `[NO PATH KNOWN]`
- ทุกท่อน: **sha256 ของอิมเมจก่อน-หลัง ต้องตรงกัน** · ถ้าเขียนสคริปต์ ให้ commit ลง `tools/` แบบรันซ้ำได้พร้อมจำนวน guard
  (ท่ามาตรฐานของบ้านนี้: verifier + guard count + exit 0)

**ชั้น ② client-observable (ต้องมีคนอยู่หน้าจอเกม)**
🔴 **ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้แม้แต่ชิ้นเดียว และห้ามใครอ้างชั้น ① เป็นหลักฐานของชั้น ②**
ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย ไม่มีจอให้ดู · ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย**
**สิ่งที่ผลบวกจะไปปลดล็อก (ยังไม่ใช่ตอนนี้):** เมื่อท่อน A หรือ C คืน "รูปร่างไบต์" มาได้จริง
ถึงจะมีสิทธิ์เขียนใบ GT ตัวถัดไปที่เป็น **attended** และถามคำถามชั้น ② ว่า *"มีอะไรโผล่ขึ้นบนพื้นให้ตาเห็นไหม"*
🔴 **ก่อนถึงตอนนั้น ห้ามเขียนโมดูล/encoder/scenario ใด ๆ** — ไม่มีรูปร่างไบต์ = การเขียนคือการแต่ง wire format ขึ้นมาเอง

### 🔴 ผลลบมีค่าเท่าผลบวก — เขียนไว้ล่วงหน้าว่าจะทำอะไรต่อ
ถ้า **ทั้งสามท่อนเป็นลบ** (สอง derived bit ไม่พาอ็อบเจกต์อะไรมา · removal pass ตัดสินด้วย static ไม่ได้ ·
`PickupTerrainThing` ไม่มี serializer ของตัวเอง) ⇒ **นั่นคือผลที่สมบูรณ์ ไม่ใช่ FAIL** และโครงการเดินต่อแบบนี้:
1. **ประตู 3 ปิดต่อไป** และคราวนี้ปิดพร้อมเหตุผลที่ระบุตัวได้ ไม่ใช่ปิดเพราะ "ยังไม่มีใครดู"
2. **loot roller คงเป็นเลน pure-logic ต่อไป** (GT-037 ที่ DONE แล้ว) — coverage `monster_spawn_and_loot`
   คง `not_started` **ซึ่งถูกต้องตามกติกา** เพราะยังไม่มี client เห็นสักไบต์
3. **ไม่มีโมดูลใหม่ถูกเขียน ไม่มี hypothesis slot ถูกใช้ ไม่มีใบ attended ถูกเปิด**
4. คำถามที่เหลืออยู่จะย้ายไปอยู่บนเลนที่แพงกว่า (เช่น membership-omission GT ในเกม) — **และต้องเป็นใบใหม่ที่เขียนขึ้นหลังเห็นผลใบนี้เท่านั้น**

### nonclaims (ติดไปกับผลทุกกรณี)
- **ไม่ claim ว่าอะไรก็ตามที่เจอ ถูกส่งจริงโดยเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว ไม่เคยเผยแพร่ และกู้ไม่ได้ตลอดกาล
- **ไม่ claim ว่ามีอะไรเรนเดอร์บนจอ** — ทั้งใบเป็นชั้น ① ล้วน · การมี literal/serializer อยู่ในอิมเมจ
  **ไม่ได้พิสูจน์ว่าคลาสนั้นถูกสร้าง ถูก register หรือเคยขึ้นสาย** (nonclaim หัวตารางของ CLASSCENSUS-001 · `tsv:3`)
- **ไม่ claim ว่า derived id `0x4543` ถูก** — เป็นเลขคณิตจากชื่อ ไม่ได้อ่านจากตารางใดในอิมเมจ
- **ไม่ claim ว่า `DropThingBoard` / `DropThingGameObj` ถูก register** — ดูบล็อก erratum ด้านบน
- **ไม่รื้อ** [NEGATIVE] ของ jump table `0x4469BD` (actor_type 2..6) — ปิดแล้ว
- ไม่แตะ DB · ไม่แตะเกม · ไม่แตะ `LOCK_GAME` · ไม่มีรอบเทสไหนถูกเปิดหรือปิดด้วยใบนี้
- **ไม่มีดีไซน์ ไม่มีโมดูล ไม่มีข้อเสนอ wire ในผลของใบนี้** — ถ้าผลกลับมาพร้อมดีไซน์ = ทำเกินใบสั่ง ให้ตัดทิ้ง

> ℹ️ ถ้าฝ่ายคิวถือกฎ **"หนึ่งใบ = หนึ่ง claim"** อย่างเคร่งครัด: ทั้งสามท่อนเขียนแบบพึ่งตัวเองได้
> ⇒ แยก **ท่อน B → GT-041** และ **ท่อน C → GT-042** ได้ทันทีโดยไม่ต้องแก้ข้อความสักบรรทัด
> (ท่อน A คงเลข GT-040 ไว้ เพราะเป็นลำดับความสำคัญที่หนึ่ง)

- **result:** (ผู้รับงาน static บนสะพานกรอก: ผลรายท่อน + VA/span/sha + เวลา + sha อิมเมจก่อน-หลัง)

## 🆕⭐ GT-041 MOVE-AUTHORITY-002: เซิร์ฟเวอร์ "ไม่ยอมเขียน" ตำแหน่งที่ client รายงาน — ผู้เล่นเห็นอะไรไหม  [✅ **PASS (no-rejection) — 2026-08-23 01:01 (+07:00): การเดินธรรมดาไม่ชน gate เลย · relog กลับจุดล่าสุดที่ขึ้นสาย**]

> ✅ **RESULT 2026-08-23 00:32–01:01 (+07:00) — PASS แบบ no-rejection** (บูต green `b665d92`):
> - `TargetPosVital` 122 เฟรม ถอดครบ 122/122 · over-budget **0/122** (max planar step 847.192/งบ 2000 · max speed 411.858/เพดาน 1500 · |dz| 186/งบ 400) — falsification ของ HYP-PF-030 ("เดินธรรมดาถูกปฏิเสธ") **ไม่ถูกยิง**
> - เฟรมสุดท้าย = แถว DB ทุกค่าพอดี · relog (บูต B) กลับเข้า **จุดล่าสุดที่ client เคยส่งขึ้นสาย** (T6) ไม่ใช่จุด HUD สุดท้าย (A4 ไม่เคยอยู่บนสาย — ต่างกัน 2187.65 หน่วย = ตำแหน่ง local ล้วน)
> - ไม่เห็น rubber-band คงอยู่ · client เดินเข้าน้ำ/ทะลุ geometry ได้ (ไม่ claim collision/terrain)
> - ผลเต็ม: `notes_to_chief/20260823_0106_GT041-PASS-NO-REJECTION-RELOG-LAST-WIRE.md` (บริโภค R123) · วิดีโอ 13:30 นาทียังไม่ทบทวนทุกเฟรม — transient <1s = non-observed

**ที่มา:** chief รอบ 116 (HYP-PF-030) — เลนแรกของโปรเจกต์ที่เซิร์ฟเวอร์ **ปฏิเสธการเขียนตำแหน่งที่ client รายงาน** ได้
(`reports/PF_MOVE_AUTHORITY002_SERVER_SIDE_GATE_20260821.md` · `src/pirateforce_foundation/move_authority_hypothesis.py`)
ชั้น wire/DB พิสูจน์จบแบบ headless แล้ว (63 เทส + verifier 87 guards) · **ชั้น client-observable = ศูนย์** นั่นคือใบนี้

### ✅ merge แล้ว (ยืนยันรอบ 117) — ท่าบูต: SHA ตรง ๆ + วิธี re-derive ถ้า `main` ขยับไปอีก

🔴 **ขั้นแรกคือรันเครื่องมือ ไม่ใช่ก๊อป SHA** — SHA ข้างล่างเป็น *คำตอบที่คาดไว้* ไว้เทียบ ไม่ใช่คำสั่ง
(เหตุผล: `git checkout <sha เก่า>` สำเร็จเงียบ ๆ เสมอ ต่อให้ `main` เดินไปอีกสามรอบแล้ว — ผู้เทสจะบูตของเก่า
โดยไม่มีสัญญาณอะไรเลย นี่คือความพังชิ้นเดียวกับที่เครื่องมือถูกเขียนขึ้นมาเพื่อฆ่า · `pf-adversary` ชี้ให้รอบ 117)

```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · แทน `C:\path\to\pirate-force-server` ด้วยพาธ clone จริง (คำสั่ง ASCII ล้วน ปลอดภัยกับคอนโซล cp874)
- **exit 0** + `BOOT_COMMIT: <sha>` ⇒ บูต sha นั้น: `git checkout <sha>` (detached HEAD ถูกแล้ว — เราบูต *คำตัดสิน* ไม่ใช่ branch)
- **exit 3** + `BOOT_COMMIT: NONE` ⇒ **ห้ามบูต** · จดในผลว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · **exit 2** = พาธผิด/git ล้ม
- 🔴 ถ้า output มีบรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ **จดลงในผลด้วยเสมอ** (มี commit แดงอยู่บนสาย main
  เหนือคำตอบ — เป็นปัญหาของ chief ไม่ใช่ของคุณ แต่รายงานที่ไม่พูดถึงมันจะดูเหมือนไม่เคยเกิดขึ้น)

**คำตอบที่คาดไว้ ณ วันที่เขียนใบนี้ (รอบ 117):** `cdc52f11b8d93b0eec9db42c83a06f0ed57e2050`
= head ของ PR รอบ 116 (MOVE-AUTHORITY-002) · `conclusion=success` run_id `32426106992` · `2026-08-20T22:54:09Z`
· และเครื่องมือยืนยันเองว่า **tree ของมันเท่ากับ tree ของ `520e2cf` (HEAD ของ main) ทุกไบต์** ⇒ โค้ดที่ถูก gate
กับโค้ดที่อยู่บน branch เป็นก้อนเดียวกันจริง (วัด ไม่ใช่สมมติ)
- ได้ SHA เดียวกัน ⇒ เดินต่อได้เลย · ได้ SHA **ใหม่กว่า** ⇒ ปกติ (มีรอบใหม่ merge เข้าไป) ให้ยืนยันสามข้อข้างล่างกับตัวใหม่
- รันเซิร์ฟเวอร์จาก working tree ของ checkout นี้เท่านั้น · บล็อก **server args** ด้านล่างไม่เปลี่ยนแม้แต่ตัวอักษรเดียว
- ⚠️ คำว่า `success` ที่เครื่องมือส่งต่อ = **subset ของ gate บน GitHub runner** (เก้า check รันบนนั้นไม่ได้)
  **ไม่ใช่ "ผ่าน gate เต็ม"** — gate ตัวจริงยังเป็นจ็อบบนสะพานของคุณ

🔴 **ห้ามบูต HEAD ของ `origin/main` เฉย ๆ และห้ามตีความว่า "คำตัดสินยังไม่มา":**
HEAD (รอบ 117 = `520e2cf`) เป็น **merge commit** ที่ automerge push ด้วย `GITHUB_TOKEN` ⇒ ไม่ trigger Actions
⇒ **ไม่มี `ci/520e2cf....json` และจะไม่มีตลอดไป** (วัดรอบ 116 จาก Actions API · ยืนยันซ้ำรอบ 117)
⇒ ของที่ถูก gate จริงคือ **parent ฝั่ง PR** = SHA ข้างบน · ใครก็ตามที่ไปอ่านคำตัดสินที่ HEAD จะไม่เจอไฟล์
แล้วปฏิเสธการบูตอย่างถูกกฎ ทั้งที่โค้ดเขียวอยู่ต่ำลงไปแค่คอมมิตเดียว — **นี่คือกับดัก ไม่ใช่ความผิดของผู้เทส**

**ยืนยันสามข้อก่อนบูต (ต้องผ่านครบสามข้อ · แทน `<SHA>` ด้วย commit ที่จะบูตจริง):**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "move-authority-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/move_authority_hypothesis_speed_gate.json && echo SCENARIO_PRESENT
```
1. ไฟล์คำตัดสินต้องมี `"conclusion": "success"` **และ** `"sha"` ตรงกับชื่อไฟล์
2. `git grep` ต้องเจอ flag จริง — **ห้ามใช้ `--help` เป็นหลักฐานว่ามี flag** (คืน 0 บรรทัดผ่านสะพาน — บทเรียนรอบใหญ่ #7 ข้อ 6) ใช้ `git grep` เท่านั้น
3. ต้องเห็นคำว่า `SCENARIO_PRESENT`
- ไม่ครบสามข้อ = **ห้ามบูต** ใบนี้กลับไป BLOCKED · **ปล่อยไว้ที่เดิม ห้ามลบ ห้ามย้าย**

### 🔴 อ่านก่อนออกแบบท่าทำงาน — เลนนี้ "เงียบสองทาง"

1. **ไม่ประกอบไบต์แม้แต่ตัวเดียว** — ทำได้อย่างเดียวคือ *ไม่เขียน* แถวใน `character_positions`
   เฟรมเดียวกัน เซสชันที่เปิด gate กับไม่เปิด **คืน action list เท่ากันเป๊ะ** (พิสูจน์ headless แล้ว)
   ⇒ **ไม่มีเฟรมใหม่ให้หาใน capture** อย่าเสียเวลาไล่หา
2. **ชื่อ event ของเลน (`move_authority_hypothesis_..._admitted` / `..._no_write`) ไม่ถูกพิมพ์ที่ไหนเลย**
   มันอยู่ใน `state.events` ในหน่วยความจำล้วน ๆ · คอนโซลจะเหมือนบูตปกติทุกประการ = **ถูกแล้ว ไม่ใช่บูตผิดไฟล์**
   ⇒ **สัญญาณที่จับได้จริงมีสองอย่าง:** (ก) hexdump ของ `TargetPosVital` ทุกเฟรมใน raw GAME log
   (ข) แถว `character_positions` ในสำเนา DB · **ลายเซ็นของการปฏิเสธ = ตำแหน่งโผล่ใน log แต่ไม่โผล่ในแถว DB**
   ⇒ **เก็บ raw GAME log ทั้งไฟล์ + สำเนา DB ของรอบไว้ ห้ามลบ** (chief re-derive ขั้นบันไดทีหลัง ท่าเดียวกับ MOVE-CADENCE-001)

### objective (claim เดียว)

**การที่เซิร์ฟเวอร์ปฏิเสธการเขียนตำแหน่ง เปลี่ยนอะไรที่ผู้เล่นมองเห็นหรือไม่ — และการเดินธรรมดาทำให้มันทำงานหรือเปล่า**
(เลนนี้ mutually exclusive กับทุกโหมด ⇒ ไม่มีทางยั่วยุด้วยเลนอื่น · **การเดินธรรมดาคือเครื่องมือเดียวที่มี**)

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-041_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt041.sqlite3
```
- เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง**
- 🔴 **บูตที่สองต้องชี้ `--db state\run_gt041.sqlite3` ไฟล์เดิม ห้าม copy ใหม่** ไม่งั้นการ relog ไม่มีความหมาย (แถวถูกทับ)

### server args (เป๊ะ)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt041.sqlite3 --move-authority-hypothesis-scenario scenarios\move_authority_hypothesis_speed_gate.json
```
- flag นี้ **ห้ามใช้ร่วมกับ scenario โหมดอื่น** และ **ไม่ยอมสตาร์ตถ้าไม่มี `--db` ที่มีอยู่จริง**
  pre-flight ราคาถูก (argparse ตายก่อนแตะไฟล์ใด ๆ): รันคำสั่งเดิมโดยไม่ใส่ `--db` ⇒ คาด exit 2 + ข้อความ
  `--move-authority-hypothesis-scenario requires an explicit existing --db`
- **ไม่มี chat trigger** ไม่ต้องพิมพ์อะไร · ⚠️ ตัวอักษรที่พิมพ์ตอนช่องแชตไม่โฟกัส = hotkey ⇒ ใช้แค่ `W/A/S/D`, `Q/E`, `spacebar`
  (การคลิกพื้นเพื่อเดินถูกปิดไปแล้ว — ดู PLAYBOOK)

### งบที่ ship มา (ทุกตัวเป็นดีไซน์ของเรา)
`max_step_units 2000.0` · `max_speed_units_per_second 1200.0` (+tolerance 0.25 ⇒ เพดานจริง **1500/วินาที**)
· `max_vertical_step_units 400.0` · `min_measurable_elapsed_seconds 0.5` · **`enforce_moving_flag false`**
· `teleport_grace_reports 1` (ให้เฉพาะตอน **เซิร์ฟเวอร์เป็นฝ่าย teleport** เช่นตอนเข้าฉาก ไม่ใช่ตอนต่อเชื่อมใหม่)

🔴 **ห้ามอ้าง `n_SPEED_WALK`/`n_SPEED_RUN` เป็นที่มาของงบ** — เป็นคอลัมน์ของ mob หน่วยไม่รู้ ไม่มีคอลัมน์ของผู้เล่น

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)

- **P1 — คาดว่า "ไม่มีการปฏิเสธเลย" ในการเดินธรรมดา** · chief replay ตารางเดินจริงใบเดียวที่มี
  (`reports/move_cadence001_smoke/replay_output.txt` 29 รายงานของ GT-005) ผ่านบันไดนี้แล้ว: **ปฏิเสธ 0 จาก 29**
  · step ใหญ่สุด 538.4 (งบ 2000) · เร็วสุด 269.2/วินาที (เพดาน 1500) · dz สูงสุด 8.0 (งบ 400)
  ⚠️ นี่คือ **เส้นทางเดียว บูตเดียว ผู้เล่นคนเดียว** — ถ้าเดินจริงแล้วโดนปฏิเสธ **นั่นคือผลที่มีค่าที่สุดของใบนี้**
- **P1b — สองงบถูกหักล้างไปแล้วก่อน ship** (จากตารางเดียวกัน): ถ้าเราบังคับ `moving` flag จะปฏิเสธ **23 จาก 29**
  และถ้าหารด้วยเวลาที่ต่ำกว่าพื้น จะปฏิเสธรายงานปกติเพราะสองเฟรมอยู่ใน heartbeat เดียวกัน ⇒ **แก้ไปแล้วทั้งคู่**
- **P2 — ระหว่างเดินจะไม่มีอะไรเกิดบนจอเลย** (เซิร์ฟเวอร์ไม่ส่งไบต์) · ผลที่เห็นได้คือ **ผลที่มาช้า**: ตอน relog
  ตัวละครจะยืนที่ตำแหน่ง *ที่ถูกยอมรับล่าสุด* (อ้าง GT-005 ที่พิสูจน์แล้วว่า client เข้ามายืนตามแถวใน DB)
- **P3 — ช่องโหว่ที่เรารู้ตัวและจดไว้:** รายงาน **หนึ่งใบแรกหลังเซิร์ฟเวอร์ teleport (ตอนเข้าฉาก) ไม่ถูกวัดเลย**
  ⇒ ถ้าเห็นตำแหน่งแปลก ๆ ถูกเขียนทันทีหลังเข้าแมพ **ไม่ใช่บั๊กใหม่** เป็นช่องที่เขียนไว้ในรายงานแล้ว

### steps (สองบูต)

**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบตามบล็อก db ·
อ่านสแนปช็อต **T0** จากสำเนาแบบอ่านอย่างเดียว (`mode=ro`):
`SELECT character_id,x,y,z,heading,updated_at FROM character_positions;`
+ `SELECT count(*) FROM sessions WHERE selected_character_id IS NOT NULL;` + `SELECT max(lease_generation) FROM sessions;`

**บูต A**
1. เปิด server ด้วย args ข้างบน (listener 2 ตัวใน ~2 วิ) — **เปิด server ก่อน client เสมอ**
2. เปิด client (`Invoke-CimMethod Win32_Process Create`) → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย
3. หน้าเลือกตัวละคร → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
4. เข้าแมพแล้ว **ถ่าย A0 ทันที ให้เห็น X/Y บน HUD** (จุดที่เซิร์ฟเวอร์วางเราไว้)
5. **ยืนนิ่ง 60 วินาที** → อ่าน DB (**T1**) · คาด: ไม่มี `TargetPosVital` เข้ามาเลย (GT-005 บูต 2 = 0 เฟรม)
6. **กด W ค้างเดินตรง ~20 วินาที** → หยุด → **ถ่าย A1** → อ่าน DB (**T2**) → **เทียบ HUD กับแถว DB ทันที**
7. **เดินข้ามแมพ 2–3 นาที** เลี้ยวด้วย `Q/E` สลับเดินสั้น-ยาว → หยุด → **ถ่าย A2** → อ่าน DB (**T3**)
8. **ขึ้น-ลงทางลาด/บันได + กระโดด (`spacebar`+`W`) อย่างน้อย 5 ครั้ง** → หยุด → **ถ่าย A3** → อ่าน DB (**T4**)
9. **ยืนนิ่ง 30 วินาที** → อ่าน DB (**T5**) → **ถ่าย A4 = จุดสุดท้ายก่อนออก (หลักฐานชิ้นเอก)**
10. ออกจากเกม: **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย (ตรวจก่อนว่าหน้าต่างแอปตัวเองไม่บังปุ่ม X)
11. **ปิด server** เก็บ raw GAME log + console out/err → อ่าน DB หลัง server หยุดสนิท = **T6** + `PRAGMA integrity_check;`

**บูต B (relog)**
12. เปิด server ใหม่ **คำสั่งเดิมเป๊ะ ชี้ไฟล์ DB เดิม** → เปิด client → ทำซ้ำข้อ 2–3
13. **ถ่าย B0 ทันทีที่เข้าแมพ ให้เห็น X/Y** — คำตอบของคำถามที่สอง
    เทียบสามค่า: **A4** (ที่ผู้เล่นยืนตอนออก) vs **T6** (แถวใน DB) vs **B0** (ที่ client วางเราไว้)
14. ยืนนิ่ง 30 วินาที → ออกตามข้อ 10 → ปิด server เก็บหลักฐาน → **T7** + `PRAGMA integrity_check;`
15. **teardown เสมอ** แม้เลิกกลางคัน (boot stamp เกิน 420 นาที template จะปฏิเสธ exit 12 — เพดานยกจาก 180 เมื่อ 2026-08-20 · ใช้ `staged\TOOL_stop_stale_server.ps1`)
16. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง **ต้องเท่าเดิม**

### pass criteria — สองชั้น แยกกันเด็ดขาด

**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ)** — ผ่านเมื่อเก็บครบและตอบได้ชี้ขาด ไม่ว่าบวกหรือลบ:
- raw GAME log ทั้งสองบูตครบทั้งไฟล์ (มี hexdump `TargetPosVital` ทุกเฟรม) + console out/err **ห้ามลบ**
- สแนปช็อต `character_positions` ครบ 8 จุด `T0..T7`
- ตอบได้ว่า **มีตำแหน่งที่โผล่ใน log แต่ไม่เคยโผล่ในแถว DB ไหม**
  (ถ้ามี: `updated_at` ต้องค้างช่วงหนึ่งทั้งที่ยังมีรายงานเข้ามา · ถ้าไม่มี: แถวสุดท้าย = รายงานล่าสุด)
- `sessions`: `count(*) WHERE selected_character_id IS NOT NULL` เพิ่ม **+1 ต่อการเข้าเกมหนึ่งครั้ง** (สองบูต ⇒ +2)
- `PRAGMA integrity_check` = `ok` · sha256 canonical ก่อน-หลังตรงกัน
- **ต้องไม่มี `[G>]` บรรทัดใหม่ที่เป็นของเลนนี้** (เลนนี้ไม่ส่งไบต์ — ถ้าเห็น ให้หยุด)
- **ชั้นนี้ตอบไม่ได้:** ผู้เล่นเห็นอะไร · จอกระตุกไหม · **และขั้นไหนของบันไดทำงาน** (chief re-derive offline)

**ชั้น (2) client-observable (ต้องมีคนหน้าจอ)**
- **วิดีโอต่อเนื่อง** ช่วงเดินข้อ 6–8 เห็นตัวละคร + ค่าพิกัด HUD ในเฟรมเดียว
- ตอบสามข้อเป็นภาษาคน: **(ก)** ระหว่างเดินจอ rubber-band/กระตุก/ถูกดึงกลับไหม หรือไม่มีอะไรเลย
  **(ข)** ที่ T2/T3/T4 ค่า HUD กับแถว DB ตรงกันหรือแยกกัน แยกกี่หน่วย
  **(ค)** ตอน relog **B0 = A4 หรือ B0 = T6**
- ภาพนิ่งบังคับ **A0 · A1 · A2 · A3 · A4 · B0** อ่านค่า X/Y ได้ทุกใบ
- **ชั้นนี้ตอบไม่ได้:** ภาพหน้าจอไม่ใช่หลักฐานว่าเซิร์ฟเวอร์ไม่ได้เขียนแถว **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

### เกณฑ์หยุด
- **จอ rubber-band หรือถูกดึงกลับจริง ทั้งที่เซิร์ฟเวอร์ไม่ส่งไบต์ใหม่เลย** = ข่าวใหญ่ที่สุดที่ใบนี้เป็นไปได้
  ⇒ หยุด เก็บวิดีโอช่วงนั้น + console ทั้งไฟล์ + raw GAME log แล้วจดให้ละเอียด
- มี `[G>]` เฟรมใหม่ที่ไม่มีในบูตปกติ ⇒ หยุด · `ErrorData=28317` ⇒ หยุด เก็บ console ทั้งไฟล์
- ตัวละครจม/ลอย/หลุดพื้นหลัง relog = จด แต่ **ไม่ใช่ falsify** (ground Z ไม่เคยถูกตรวจ)

### ผลลบมีค่าเท่าผลบวก
1. **ไม่มีการปฏิเสธเลย** ⇒ **ผลเต็มใบ** งบรอดจากการเดินจริง (ยืนยัน P1) · คำถามชั้น client-observable **ยังไม่ถูกตอบ**
   ต้องเป็นใบใหม่ที่หาวิธียั่วยุอย่างถูกกติกา — **ให้ chief/Panya เคาะ ห้ามออกแบบเองในใบนี้**
2. **เดินธรรมดาแล้วโดนปฏิเสธ** ⇒ **ผลที่มีค่าที่สุด** — หักล้าง *ตัวเลข* โดยไม่หักล้าง *กลไก*
   ⇒ chief re-derive ขั้นบันไดจาก log แล้วแก้ scenario · `production_allowed` ยัง false · **coverage ไม่ขยับ**
3. **มีการปฏิเสธ แต่ผู้เล่นไม่เห็นอะไรระหว่างเล่น และ B0 = T6** ⇒ **ผลเต็มใบ** = "การไม่ยอมเขียนมองไม่เห็นจนกว่าจะ relog"
   ⇒ authority ที่มีผลในเซสชันต้องมี corrective wire ซึ่ง **เราไม่มีหลักฐานและห้ามประดิษฐ์** ⇒ คงไว้ที่ stop rule เดิม

### nonclaims (ติดไปกับผลทุกกรณี)
- **บันได ลำดับ และทุกตัวเลขในงบ เป็นดีไซน์ของเรา ไม่ใช่นโยบายของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล**
- **ห้ามอ้าง `n_SPEED_WALK`/`n_SPEED_RUN` เป็นที่มาของงบ** · หน่วยพิกัดโลกแปลงเป็นหน่วยจริงไม่ได้
- **ไม่ใช่การตรวจ collision / terrain / line-of-sight** — เซิร์ฟเวอร์ไม่มีเรขาคณิตของแมพ
- **ไม่มี client ตัวไหนเคยเห็นไบต์ของเลนนี้ เพราะมันไม่มีไบต์**
- **ไม่ claim ว่า corrective reposition ควรมีหน้าตาอย่างไร** — TELEPORT มีในฐานะ transport แต่ผลกับ client เป็น UNKNOWN
- **ความเร็วแนวดิ่งไม่ถูกจำกัด** (หารด้วยเวลาเฉพาะแนวราบ) · **หนึ่งรายงานแรกหลังเซิร์ฟเวอร์ teleport ไม่ถูกวัด**
- `production_allowed=false` · **แถว coverage ไม่ขยับไม่ว่าใบนี้จะออกหัวหรือก้อย**

> ℹ️ **เลขชนกัน:** บันทึกท้าย GT-040 เสนอให้แยกท่อน B เป็น GT-041 — **เลข 041 ถูกใช้โดยใบนี้แล้ว**
> ถ้าจะแยกท่อน B/C ของ GT-040 ให้ใช้ **GT-042 / GT-043**

- **result:** (ผู้เทสกรอก: T0..T7 · ภาพ A0–A4/B0 พร้อม sha256 · วิดีโอช่วงเดิน · คำตอบ (ก)(ข)(ค) · เวลา ·
  sha canonical ก่อน-หลัง · path ของ raw GAME log ทั้งสองบูต · **สำเนา `state\run_gt041.sqlite3` เก็บไว้ให้ chief re-derive**)


## GT-030 REMOTE-PLAYER-VIS-001: "มีคนอื่นอยู่ในโลก" ครั้งแรก — actor_type 2 ทั้ง 5 เฟรม  [🟠 **ผล substantive แล้ว — rerun 2026-08-23 00:25 (+07:00): CLIENT NO-RENDER ใต้ mask ชุดนี้ (ตรวจถึงพิกัดจริงระยะประชิด) · ~~🔴 ห้ามรันรอบสาม — เส้นทางต่อ = static render-mask/selection~~ 🟢 **ข้อห้ามนี้ถูกยกเลิกโดยเจ้าของ 2026-08-25 ~18:15 (+07:00)** (จดหมาย `20260825_1815_PANYA-RULINGS-FOUR-*` §④ · บันทึกโดย chief R167) ⇒ **รอบสามอยู่ที่ใบ `GT-030-R3` ถัดจากใบนี้** · เส้นทาง static ยังเปิดอยู่เหมือนเดิม ไม่ได้ถูกยกเลิกไปด้วย**]

> 🟠 **RESULT rerun 2026-08-23 00:09–00:25 (+07:00)** (บูต green `b665d92`): wire ครบ 5 เฟรม (`SPAWN_BARE → SPAWN_AVATAR → MOVE_A_1 → MOVE_A_2 → NEGATIVE_CONTROL`) ไม่มี refuse/error · ผู้เทสเดินไปตรวจ**พิกัดจริง**:
> - B `ProbePlayer02` (ยืนห่าง ~33 หน่วย · กวาด 4 มุม): **ไม่เห็นโมเดล/ตัวใส/ป้ายใด**
> - A หลัง MOVE (ยืนห่าง ~52 หน่วย · ระยะประชิด + Tab ×4): **ไม่เห็นโมเดล ไม่มี target panel**
> ⇒ ยกระดับจาก "ระบุตัวไม่ได้" (รอบ #12) เป็น **no-render ใต้ mask/เฟรมชุดนี้** — ผลลบที่ใช้ได้จริง
> - ⚠️ ภาพ before/after ทุก cadence ไม่ครบฟอร์ม (ภาพแรก +3.487s · baseline ไม่คงอยู่ใน root) ⇒ transient <3.487s = non-observed · no-render ยึดจาก persistent check เท่านั้น
> - 📌 เส้นทางต่อ (ห้ามรันเกมเพิ่ม): งาน static — mask bit ไหนจำเป็นต่อ render ของ actor_type 2 / เส้นทาง selection — รอ chief ออกใบ STATIC-ON-BRIDGE เมื่อคำถามคมพอ
> - ผลเต็ม: `notes_to_chief/20260823_0030_GT030-NO-RENDER-GT043-PARTIAL.md` (บริโภค R123)

> 🟡 **ผลรอบใหญ่ #12 (2026-08-21 07:55→08:37 +07:00 · จดหมาย `notes_to_chief\20260821_0840_GT031-PASS-GT030-PARTIAL.md`):**
> - **ชั้น wire: ผ่านครบ** — 5 เฟรมออกครบ ขนาดตรงดีไซน์ทุกเฟรม
>   (`SPAWN_BARE` 181 B · `SPAWN_AVATAR` 288 B · `MOVE_A_1` 72 B · `MOVE_A_2` 77 B · `NEGATIVE_CONTROL` 218 B)
>   grep `compose_refused` / `already_sent` = ไม่พบ
> - **ชั้น client: ยังตัดสินไม่ได้** — ผู้เทสไม่พบป้ายชื่อ `ProbePlayer01/02/ProbeControl03` ที่ไหนเลย
>   คลิกตัวที่สงสัยแล้ว target panel ไม่ขึ้น ⇒ **ระบุ identity ไม่ได้** (ไม่ใช่ "ไม่เรนเดอร์" — ผู้เทสติด nonclaim นี้ไว้เอง ถูกต้องแล้ว)
> - ⭐ **การพบเห็นที่ยังไม่อธิบาย (ห้ามหล่นหาย — chief R119 เติมกลับตามผล adversary):** ผู้เทสเห็น
>   **ตัวละครหน้าตาแบบผู้เล่น (ชายหนุ่มชุดน้ำเงิน-ขาว) ยืนที่ X ≈ `-8681`** — ต่างจาก NPC Navy Transfer ที่คุ้นเคย
>   คลิกแล้ว target panel ไม่ขึ้น · จุดนั้นห่างตำแหน่ง ProbePlayer01 หลัง MOVE (`-8839.957`) ~159 หน่วยทาง +X
>   ⇒ **อาจเป็น actor_type 2 ตัวแรกที่เรนเดอร์จริงในประวัติโปรเจกต์ หรืออาจเป็น NPC ประจำแมพ — ยังตัดสินไม่ได้ทั้งสองทาง**
>   รอบ rerun มีขั้นตรวจจุดนี้ซ้ำโดยเฉพาะ (steps ข้อ 7)
> - เกณฑ์หยุดทั้งเลน (ชื่อ `ProbeControl03` โผล่) **ไม่ถูกยิง** · ไม่มี `ErrorData=28317`
> - ผู้เทสยิงจากจุดเกิดที่รายงาน X `-8553` Y `-2579` กวาดกล้อง 360° แล้วเดิน +X ถึงช่วง X `-8681..-8414`
>
> **วินิจฉัย static ของ chief R119 (มี provenance ครบใน `rounds\R119_mrcii9_gt031_pass_gt030_diagnosis.md`):**
> 1. **ชื่ออยู่ในไบต์ขาออกจริงทั้งสามเฟรม spawn** — BasicAttr bit `0x0001` + wstring tag `0x48` (UTF-16LE)
>    encoder **ปฏิเสธ compose ถ้าไม่มีชื่อ** (`remote_player_hypothesis.py:651-652,668`) · 181 B สอดคล้องเฉพาะกรณีมีชื่อ
>    (ไม่มีชื่อจะเหลือ 150 B) ⇒ **"ไม่เห็นป้ายชื่อ" ไม่ใช่ความล้มเหลวของ wire**
> 2. **ไม่มี claim ที่ commit แล้วว่า nameplate ลอยหัวเรนเดอร์สำหรับ actor_type 2** — ผู้บริโภคชื่อ (BasicAttr+0x28)
>    ที่พิสูจน์ static ได้มีตัวเดียวคือ **target panel** (updater `0x51F920` → `LABEL_NAME 0x5BD624`)
>    ⇒ วิธีระบุตัวในรอบ rerun ต้องเป็น **"คลิก/Tab → อ่าน target panel"** ไม่ใช่ "มองหาป้ายลอยหัว"
> 3. **พิกัดจริงของ probe** — ยึด placement-0 NPC **'Navy Transfer'** ที่ X `-9139.957` Y `-2780.045` Z `223.292`
>    (`pf_login_game_server_v141.py:1324`) · 🔴 **NPC ตัวนี้คือ actor identity `0x2001`** — ตัวเดียวกับที่
>    **GT-032 ทำให้ขึ้นศัตรู** และ GT-022/025 เคยฆ่า ⇒ **ในรอบใหญ่เดียวกัน ให้รัน GT-030 ก่อน GT-032 เสมอ**
>    (landmark ที่เพิ่งถูกทำให้แดง/ตาย ใช้เป็นจุดอ้างอิงกลาง ๆ ไม่ได้):
>    `ProbePlayer01` = **ทับตำแหน่ง Navy Transfer เป๊ะ (ตั้งใจ — จะเห็นตัวซ้อนกัน)** · `ProbePlayer02` = X+150 (`-8989.957`)
>    · `ProbeControl03` = X−150 (`-9289.957`) · A หลัง MOVE = X+300 (`-8839.957`)
> 4. 🔴 **บรรทัดเดิม "probe อยู่แนว +X ~112–412 หน่วยจากจุดเกิด" ผิด/ค้างสองทาง:** (ก) จริงเฉพาะเมื่อยืนที่ค่าคงที่
>    spawn v135 (`-9239.957, -2830.045`) — รอบ #12 ผู้เทสยืนห่างจากจุดนั้น ~731 หน่วย · (ข) `ProbeControl03` อยู่ทาง **−X**
>    คือ**หลังกล้อง**ที่หัน +X · จากจุดที่ผู้เทสยืนจริง probe ทุกตัวอยู่ **350–765 หน่วยทาง −X** — อาจพ้นระยะเรนเดอร์/ระบุ
>    (ระยะเรนเดอร์ของ client = **[UNKNOWN]**)
> 5. ข้อเสนอของผู้เทสข้อ 1 (ให้ client console พิมพ์ identity ของ actor) **ทำไม่ได้ — client binary แก้ไม่ได้**
>    ⇒ แทนด้วยวิธี landmark + target panel ตามโปรโตคอลด้านล่าง
> - **rerun ไม่ต้องแก้โค้ด** — one-shot flag เป็นของ**ต่อ GAME connection** (`remote_player_sweep_count` อยู่ใน
>   session state ที่สร้างใหม่ต่อ connection ที่ accept — `runtime.py:509` · accept loop `pf_login_game_server_v141.py:7399`)
>   ⇒ บูตใหม่ = connection ใหม่ = flag รีเซ็ตแน่นอน · แต่ **reconnect ในบูตเดียวกันก็ได้ sweep ชุดใหม่ได้เช่นกัน** —
>   ถ้าเกิด reconnect กลางรอบ จดไว้ว่า probe อาจถูก spawn ซ้ำ (ตัวเก่าไม่ despawn)

- **objective:** พิสูจน์หนึ่งข้อ: **client เรนเดอร์และให้ระบุตัว actor_type 2 (remote player) ที่เซิร์ฟเวอร์ spawn ได้หรือไม่**
  (ทุกเฟรม "ตัวอื่นในโลก" ก่อนหน้านี้ = actor_type 4 ทั้งหมด · นี่คือ actor_type 2 = `CNetActor` สาขา remote player ครั้งแรกของโปรเจกต์)
- **db:** สำเนา `state\pirateforce.sqlite3` ตามปกติ — **ห้ามเปิด canonical** · ตรวจ sha256 canonical ก่อน-หลังรอบ ต้องตรงกัน
  (เพราะเป็นสำเนา ตำแหน่งตัวละครจะรีเซ็ตกลับจุดเกิดทุกบูต — โปรโตคอลข้างล่างนับข้อนี้ไว้แล้ว)
- **server args:** `--remote-player-hypothesis-scenario scenarios\remote_player_hypothesis_visibility_probe.json` (+ `--db` สำเนา)
  ท่าบูตเดียวกับ GT-024/027 เป๊ะ เปลี่ยนแค่ flag · console label = `HYP_PF_025_REMOTE_PLAYER_<STEP>` ·
  event = `remote_player_hypothesis_visibility_probe_sent` — เห็นชื่ออื่น = บูตผิดไฟล์
  **one-shot ต่อ GAME connection** — ยิงซ้ำใน connection เดียวได้ `..._already_sent_no_reply` · **reconnect = ยิงใหม่ได้**
  (ดูโน้ตในบล็อกวินิจฉัยข้างบน) · compose ถูกปฏิเสธ = `..._compose_refused_no_reply_<เหตุผล>` และไม่มีไบต์ออกเลย
- **steps:**
  1. preflight จอว่าง (การ์ด elevated ของรอบ 111) → **สตาร์ตเซิร์ฟเวอร์ก่อน แล้วค่อยบูต client** (client ไร้เซิร์ฟเวอร์ตายใน ~3.5 นาที ·
     ถ้ารอบก่อนเพิ่งฆ่า client ไป **ต้อง restart เซิร์ฟเวอร์ก่อน** ไม่งั้นค้าง "connecting")
  2. เข้าเกมด้วยตัวละครเดิม (ท่า `Return` → เข้าเกม ตามบทเรียนรอบ #12 — คลิกปุ่มอาจไม่ติด)
  3. 🔴 **เดินไปหา NPC 'Navy Transfer' ก่อน** (landmark ใกล้จุดเกิด · X `-9139.957` Y `-2780.045`) — **ห้ามยิงจากจุดเกิด**
  4. ยืนข้าง Navy Transfer แล้วถ่าย **baseline สองใบก่อนยิง**: ใบหนึ่งหันกล้องเห็นฝั่ง **X+150** ใบหนึ่งเห็นฝั่ง **X−150**
     (หรือเฟรมเดียวที่เห็นทั้งสองฝั่งถ้ามุมกว้างพอ) — จำกรอบกล้องทั้งสองไว้ใช้ซ้ำทุกเฟรม
  5. ยิง trigger: **`Return` → พิมพ์ ascii 12 ตัวเป๊ะ → `Return`** (สั้นกว่านี้ = ถึงเซิร์ฟเวอร์แต่เงื่อนไขเงียบ ·
     พิมพ์ตอนช่องแชตไม่โฟกัส = กลายเป็น hotkey)
  6. sweep **5 เฟรม ห่างกัน 15 วิ/เฟรม (75 วิทั้งชุด — cadence เดิม)**: ทุกเฟรมถ่าย before/after **ที่กรอบกล้องเดียวกับ baseline**
     ทั้งสองฝั่ง ตามตารางคำทำนายข้างล่าง
  7. หลังจบชุด: **ระบุตัวด้วยตำแหน่งเทียบ Navy Transfer + คลิกซ้าย (ลอง Tab ด้วยถ้าคลิกไม่ติด) → อ่านชื่อใน target panel**
     ทีละตัว: จุดทับ Navy Transfer (คาด ProbePlayer01 ซ้อน — คลิกอาจโดน NPC ก่อน จดว่าโดนตัวไหน) · X+150/X+300 · X−150
     · ⭐ **เทียบหน้าตากับ "ชายหนุ่มชุดน้ำเงิน-ขาว" ที่รอบ #12 เห็นที่ X ≈ −8681** — ตัวแบบเดียวกันโผล่อีกไหม
     ที่จุดไหน ขยับตาม MOVE ไหม ถ่ายภาพเสมอแม้ target panel ไม่ขึ้น
  8. จบเทส: ปิด client → teardown ตามปกติ **ภายใน 420 นาทีจาก boot stamp** (เพดานถูกยกจาก 180 → 420 เมื่อ 2026-08-20 —
     `staged\TEMPLATE_teardown_generic.ps1:135` · เลข 180 ที่เห็นในใบเก่า ๆ = stale) · run copy ทิ้งได้ ·
     restart เซิร์ฟเวอร์ก่อนบูตรอบถัดไป
- **สิ่งที่ควรเห็นทีละเฟรม (คำทำนาย — ไม่ใช่ข้อเท็จจริง · พิกัดแก้เป็นค่าจริงยึด Navy Transfer แล้ว):**
  | t | เฟรม | ถ่ายอะไร |
  |---|---|---|
  | +0s | `SPAWN_BARE` — identity A `0x00A00001` ชื่อ `ProbePlayer01` **ทับตำแหน่ง Navy Transfer เป๊ะ** | มีตัว**ซ้อน/stack** กับ Navy Transfer ไหม? รูปร่างอะไร (คน/กล่อง/ตัวใส)? |
  | +15s | `SPAWN_AVATAR` — identity B `ProbePlayer02` ที่ **X `-8989.957`** (X+150) **พก AvatarAttr ของตัวละครที่เลือกอยู่ (replay)** | **B ต่างจาก A ตรงไหน — คำตอบของ "AvatarAttr จำเป็นไหม"** ถ่ายให้เห็นทั้งคู่เฟรมเดียวถ้าทำได้ |
  | +30s | `MOVE_A_1` — MovementAttr เดี่ยว mask `0x01` → A ควรย้ายไป **X `-8839.957`** (X+300) | ตัวที่ซ้อน Navy Transfer หายจากจุดเดิม/ไปโผล่จุดใหม่ไหม? เดินหรือวาร์ป? |
  | +45s | `MOVE_A_2` — mask `0x03` heading π/2 | A หันหน้าไหม? |
  | +60s | `NEGATIVE_CONTROL` — identity C ที่ **X `-9289.957`** (X−150 — **ฝั่งตรงข้ามกับ B/A**) พก **NPCAttr ผิดคลาสโดยตั้งใจ** (ชื่อ `ProbeControl03`) | ฝั่ง −X มีตัวโผล่ไหม? (bind gate `0x4697B0` เกต CNetNPC ต้อง drop เงียบ) |
  | หลังจบ | ขั้นระบุตัวตาม steps ข้อ 7 | target panel ขึ้นไหม / ชื่อในพาเนลคือ `ProbePlayer01`/`ProbePlayer02` ไหม / ตัวจม-ลอยพื้น (ground Z ไม่ได้ตรวจ — ไม่ falsify) |
- **pass criteria (สองชั้น แยกกัน — ห้ามอ้างชั้นหนึ่งแทนอีกชั้น):**
  - **wire/DB (headless ได้ ไม่ต้องมีคน):**
    - 5 เฟรมออกครบตาม label + delay 15 วิ · ขนาด **181/288/72/77/218 B ตามลำดับ** (ตรงกับรอบ #12 — เบี่ยงจากนี้ = จดทันที
      **ยกเว้น 288 B ของ `SPAWN_AVATAR`**: หาง avatar เป็น replay ของตัวละครที่เลือกอยู่ scenario ตั้งใจไม่พินหาง
      (`avatar_tail_excluded_from_pin: true` — พินเฉพาะโครง 172 B) ⇒ 288 เป็นตัวเลขผูกตัวละคร ณ รอบ #12 เปลี่ยนได้โดยไม่ผิด)
    - ไม่มี `compose_refused` / `already_sent` (ในบูตแรกของรอบ) · ไม่มี `ErrorData=28317`
    - sessions +1 ต่อการเข้าเกม · `PRAGMA integrity_check` = `ok` · sha256 canonical ก่อน-หลังตรงกัน
    - **ชั้นนี้ตอบไม่ได้ว่าจอเห็นอะไร** — 181 B พิสูจน์ว่า *ชื่ออยู่ในไบต์* ไม่ใช่ว่า *ชื่อเรนเดอร์*
  - **client-observable (ต้องมีคนหน้าจอ):**
    - ตอบได้อย่างน้อย: **(ก)** เฟรม +0 มีอะไรโผล่/ซ้อนที่ตำแหน่ง Navy Transfer หรือไม่ (เทียบ baseline กรอบเดียวกัน)
      **(ข)** target panel ของตัวที่ X+150 (หรือ X+300 หลัง MOVE) ขึ้นชื่อ `ProbePlayer02`/`ProbePlayer01` หรือไม่
      **(ค)** ฝั่ง X−150 มีตัวโผล่หรือไม่ และถ้าโผล่ target panel ว่าง/ไม่ขึ้นหรือไม่
    - ภาพบังคับ: baseline 2 ใบ + before/after ทุกเฟรม (กรอบกล้องเดิม) + ภาพ target panel ทุกครั้งที่เปิดได้
    - **ผลลบมีค่าเท่าผลบวก:** ข้อสรุป "ไม่เรนเดอร์" ให้ยึดจาก **B (X+150) และ A หลัง MOVE (X+300) เท่านั้น** —
      เฟรม +0/+15 ของ A ทับตัว NPC จึงอาจถูกโมเดล NPC บังทั้งตัว (ตัดสินจากจุด stack ไม่ได้) ·
      ถ้า B และ A-หลัง-MOVE **ไม่โผล่ทั้งคู่** = "actor_type 2 spawn แล้วไม่เรนเดอร์ด้วย mask ชุดนี้"
      — เป็น**ผลเต็มใบ ไม่ใช่ fail** · redirect: chief สอบ mask bit ฝั่ง render แบบ static ก่อนออกใบใหม่ (ห้ามเดา bit ในใบนี้)
      ส่วน "โผล่แต่ target panel ไม่ขึ้นชื่อ" = ผลอีกแบบ (เรนเดอร์ได้แต่ bind ชื่อไม่ถึงพาเนล) — จดแยกข้อ ห้ามยุบรวม
- **เกณฑ์หยุดทั้งเลนทันที (คงเดิม):** ⛔ ชื่อ **`ProbeControl03` โผล่ที่ไหนก็ตาม** (ป้ายหรือพาเนล) = ข้ออ้าง bind-gate ของก้อน 1 ผิด —
  ทุกข้อสรุปก้อน 1 ต้องรื้อ · หรือ server log มี `ErrorData=28317` ⇒ หยุด เก็บ console ทั้งไฟล์
- 🔴 **ไม่มีทาง despawn probe** — สามตัวค้างจนตัด connection · จบเทสปิด client แล้ว teardown ตามปกติ
- 🔴 HP ของ probe = 100 ทุกตัว — ถ้าเห็นตัวไหน "ตาย" เอง = ผิดคาด จดละเอียด
- **nonclaims:** (คงของเดิมครบ + เพิ่มจาก R119)
  - ดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล (ไม่มี capture remote human player แม้แต่เฟรมเดียว)
  - ไม่ claim ว่า mask bit ไหนของ ActorAttr จำเป็นต่อการเรนเดอร์
  - ไม่ claim ว่า avatar ถูกยอมรับใต้ identity อื่น (จนกว่าจะเห็น B)
  - นี่ไม่ใช่ผู้เล่นสองคนจริง (ก้อน 3 ยังไม่อนุมัติ)
  - **ไม่ claim ว่า nameplate ลอยหัวมีอยู่สำหรับ actor_type 2** — ผู้บริโภคชื่อที่พิสูจน์แล้วมีแค่ target panel · "ไม่เห็นป้าย" ตัดสินอะไรไม่ได้
  - **ระยะเรนเดอร์ของ client = [UNKNOWN]** — ใบนี้ลดตัวแปรด้วยการยืนติด landmark ไม่ใช่การวัดระยะ
  - "ระบุตัวไม่ได้" (รอบ #12) ≠ "ไม่เรนเดอร์" — สองประโยคนี้ห้ามใช้แทนกันในทุกผลของใบนี้
  - **ยังไม่มีหลักฐาน static ว่า click/Tab targeting bind กับ actor_type 2 ได้เลย** — เส้น `0x51F920→LABEL_NAME`
    พิสูจน์เฉพาะ "copy ชื่อหลัง bind แล้ว" ไม่ใช่ "bind ได้" · ถ้า rerun จบที่ "พาเนลไม่ขึ้นทุกตัว" อีก
    ~~**อย่ารันซ้ำรอบสาม**~~ 🟢 **ยกเลิกโดยเจ้าของ 2026-08-25 ~18:15 (+07:00)** (📌 ข้อห้ามเดิมเป็นข้อห้ามแบบมีเงื่อนไข — ห้าม*ไล่ target panel*ซ้ำ ซึ่ง `GT-030-R3` ไม่ได้ทำ) — — chief ต้องสอบ selection path ฝั่ง client แบบ static ก่อน (จดเป็นงาน static รอบหน้าแล้ว)
- **result:** (ผู้เทสกรอกรอบ rerun: คำตอบ (ก)(ข)(ค) · ภาพ baseline + before/after ทุกเฟรม + target panel พร้อม sha256 ·
  เวลา · sha canonical ก่อน-หลัง · path raw GAME log — *ผลรอบ #12 ถูกจดไว้ในบล็อกหัวใบแล้ว ห้ามลบ*)

## GT-030-R3 REMOTE-PLAYER-VIS-PROVENANCE-001 [attended, in-game]: รอบสามของ `GT-030` — **ของที่เห็นบนแนว probe เป็นผลของเฟรมที่เลนนี้ส่ง หรืออยู่บนแมพมาก่อนแล้ว**  [✅ **PASS — รันแล้ว attended 2026-08-25 18:42-18:48 (+07:00) · จ็อบ 1154/1158/1159/1160 · ปิดโดย chief R168** · `OBSERVER_CONFIRMED: 2026-08-25T19:40+07:00` · เขียนใบโดย chief R167 (`pf-queue-author`) · ปลดล็อกโดยเจ้าของ 2026-08-25 ~18:15 (+07:00)]

### ✅ ผลรอบสาม — สรุปสองชั้น (chief R168 · จดหมาย `notes_to_chief\consumed\20260825_1900_GT030-ROUND3-PASS-*.md`)

**ชั้น wire/DB:** ครบทั้งห้าเฟรม ขนาดตรงดีไซน์ทุกเฟรม ห่างกัน `15.000` วิเป๊ะ (`SPAWN_BARE 181 B` · `SPAWN_AVATAR 288 B` ·
`MOVE_A_1 72 B` · `MOVE_A_2 77 B` · `NEGATIVE_CONTROL 218 B`) · ไม่มี `compose_refused` · ไม่มี `already_sent` · ไม่มี `ErrorData=28317`
`SESSIONS_SELECTED 11 · MAX_LEASE 12 · OPEN_SESSIONS 0 · INTEGRITY ok · FK 0` · **CANON ไม่ขยับ** · teardown exit 0 · boot `06b62abd` · CODE_DELTA 0 (ศูนย์สล็อตตามใบ)

**ชั้น client-observable (ยืนยันโดยผู้เทสครบทุกข้อ):**

| คำถาม | ผล |
|---|---|
| ไคลเอนต์ **เรนเดอร์** `actor_type 2` ได้ไหม | ✅ **ได้** — ครั้งแรกในประวัติโปรเจกต์ · `evidence_screens/GT030R3_1159_ACTORTYPE2_BODY_RENDERED_t278.0s.jpg` |
| **เลือก** ได้ไหม | ✅ ได้ — ลูกศรเหลืองคู่ขึ้นบนตัว |
| **target panel** เปิดไหม | ✅ เปิด (`t=280.5`) · `GT030R3_1159_TARGET_PANEL_OPEN_HP0_NONAME_t280.5s.jpg` |
| panel แสดง **ชื่อ** ไหม | ❌ **ช่องชื่อว่างเปล่า** — แสดง `HP. 0` · `LV. 1` แทน |
| **ป้ายชื่อลอยหัว** ไหม | ❌ ไม่มีเลยแม้แต่เฟรมเดียว |
| **AvatarAttr** ถูกใช้ไหม | ❌ ไม่ — โมเดลเป็นร่างเปลือยค่าเริ่มต้นทั้งที่ `SPAWN_AVATAR` แนบ `AvatarAttr` ของตัวละครที่เลือกไว้แล้ว |
| ตัวคุมเชิงลบ `ProbeControl03` | ✅ เงียบสนิท (ไม่มีโมเดล ไม่มีชื่อ) ⇒ **เกณฑ์หยุดเลนไม่ถูกยิง** |

🎯 **ข้อสรุปที่แข็งที่สุดของใบ:** ชั้น wire ยืนยันว่า **ชื่ออยู่ในไบต์แน่นอน** (encoder ปฏิเสธ compose ถ้าไม่มีชื่อ · `181 B` สอดคล้องเฉพาะกรณีมีชื่อ)
แต่ **ผู้บริโภคชื่อตัวเดียวที่พิสูจน์ static ได้ — target panel (`0x51F920` → `LABEL_NAME 0x5BD624`) — เปิดขึ้นมาแล้วและยังว่าง**
⇒ ~~**ไคลเอนต์ไม่บริโภค `BasicAttr` name ที่เราส่งสำหรับ `actor_type 2`** · ไม่ใช่แค่ "ไม่มีป้ายลอยหัว" แต่ **ผู้บริโภคที่ควรกินก็ไม่กิน**~~
⇒ ~~ยืนยันวินิจฉัย static ของ chief R119 ข้อ 2 ตรงเป๊ะ · และเป็นเส้นหลักฐานใหม่ที่ `RE-067` (อะไรตัดสินชื่อ/สี) ยังไม่มี~~

🔴🔴 **ถอนสองบรรทัดข้างบนแล้ว — chief R169 (2026-08-25 ~21:0x +07:00)**
**[MEASURED · client-observable]** ตัวหักล้างที่ถูกและถูกที่สุด **ไม่ใช่ NPC ของรอบสี่ แต่อยู่ในภาพควบคุมของใบนี้เองมาตลอด**
`evidence_screens/GT030R3_1159_TARGET_PANEL_CROP_t280.5s.png` (chief เปิดดูเองรอบ R169) แสดงสองแผงในเฟรมเดียวกัน:

```
ซ้าย  (แผงของผู้เล่นเอง):  [orb แดง]  HP. 100 /100   [ตรา] LV. 1     <- ไม่มีชื่อ
ขวา   (แผงเป้าหมาย):       [orb ฟ้า]  HP.   0        [ตรา] LV. 1     <- ไม่มีชื่อ
```

🎯 **แผงของผู้เล่นเองก็ไม่มีชื่อ** ทั้งที่เป็นตัวละครที่ไคลเอนต์รู้ชื่อแน่นอนและกำลังวาด `Arena01` ลอยอยู่กลางจอในเฟรมเดียวกัน
⇒ 🔴 **วิดเจ็ตหลอด HP นี้ไม่มีแถวชื่ออยู่เลยตั้งแต่แรก** ⇒ **"ช่องชื่อว่าง" ไม่ใช่ข้อมูลเกี่ยวกับการ bind ชื่อของ actor ตัวใดทั้งสิ้น**
⇒ ข้อสรุปเดิมเห็นแผงว่างของ actor ตัวเดียวแล้วตั้งเป็นคุณสมบัติของ **คลาส `actor_type 2`** ⇒ **ผิดกฎ G6 ตรง ๆ**

🔴 **และคำแทนที่เวอร์ชันแรกของ chief เอง (*"แผงในบิลด์นี้ไม่แสดงชื่อ ไม่ว่า type 2 หรือ type 4"*) ก็ถูกถอนด้วย** —
มันเป็นการอนุมานสากลจาก **n=1** เหมือนกัน แค่ยกขึ้นไปอีกชั้นเดียว **[เสนอ]** ไม่ใช่ **[MEASURED]**

**🟢 เส้นที่ยังใช้ได้จริง และแข็งกว่าที่เคยเขียน — เพราะมี positive control ในบิลด์เดียวกัน:**
> **[MEASURED]** บิลด์นี้ **วาดชื่อ actor ได้** — `Tornado Eagle` อ่านออกและเป็นสีเขียว (`GAME_TEST_QUEUE.md:919,922`) · `Red leaves Hammer` สีแดง · `Arena01` ของผู้เล่นเอง
> **แต่ไม่วาดให้ `actor_type 2` ที่เราส่งเลยสักเฟรมเดียวตลอดทั้งรอบสามและรอบสี่**
> 🔴 **nonclaim:** ป้ายของ `Tornado Eagle` อาจมาจากเทมเพลตฝั่งไคลเอนต์ที่ผูกกับ preset ไม่ใช่จาก ASCII ที่เราส่ง — **ยังไม่ได้แยก**

🔴 **ตัวคุม `actor_type 4` ของรอบสี่ยังใช้ได้ แต่ระบุตัวไม่ได้ — ดูบล็อก `R4` ข้อ ③ ข้างล่าง**

🔴 **ผลข้างเคียงสองข้อ — แตกเป็นใบของตัวเองแล้ว อย่าอ่านเป็นข้อสรุปในใบนี้:**
1. `MOVE_A_2` (`MovementAttr` เดี่ยว mask `0x03`) ตามด้วยข้อความ `ตาย!` ที่ `t=268.0` (`+0.63` วิหลังไบต์ออกสาย) และ panel อ่าน `HP. 0`
   **ทั้งที่รอบนี้ไม่ส่ง HP ออกไปเลยสักไบต์** ⇒ ดูใบ **`RE-071`** ใน `CLIENT_RE_QUEUE.md` — **ต้องวัดก่อนสร้างเลนตายของ `GT-036`**
   🔴 **erratum ของ chief R168 ต่อจดหมายผล:** จดหมายเรียกข้อนี้ว่า *"ผลที่ไม่มีใครทำนาย"* — **ไม่จริง มีคนทำนายไว้แล้วสามที่ commit ก่อนรอบสามหลายวัน**
   (`reports/PF_CHUNK2_Q1_*.md:380` · `src/pirateforce_foundation/remote_player_hypothesis.py:225-230` · `reports/PF_RUNTIMERES_ACTOR_ENTRY001_*.md:5` *"An actor cannot be born dead ... needs at least two actor-entries for the same identity"*)
   🔴 **และกรอบคำถามเดิมผิดด้วย** — chief วัดจบบนคลาวด์แล้วว่า **ไม่มีฟิลด์ไหนใน `MovementAttr` แตะ HP/ชื่อ/สถานะตายเลยแม้แต่ bit เดียว**
   ตัวทริกคือ **การมาถึงของ actor-entry ใบที่สองของ identity เดิม** ไม่ใช่เนื้อของเฟรม ⇒ **`MOVE_A_1` (ใบที่สอง · `t=252.37`) น่าจะเป็นตัวทริกมากกว่า `MOVE_A_2`**
   แต่ nonclaim ① ข้างล่างบอกว่าช่วงนั้นกล้องคุมไม่ครบ ⇒ **อ่านไม่ได้ทั้งสองทาง** · รายละเอียดครบอยู่ในหัวใบ `RE-071`
2. `SPAWN_BARE` (วางที่พิกัด `P0` เป๊ะ) แล้ว NPC `P0 Navy Transfer` หายไปภายใน `0.6` วิ (ภาพคู่ before/after กล้องมุมเดียวกัน `t=221.5`/`t=223.0`)
   ⇒ ดูใบ **`GT-072`** ข้างล่าง — แยกไม่ออกระหว่าง despawn/แทนที่/บังทับ จากหลักฐานชุดนี้
   (🔢 เลข: ตัวนับเป็นชุดเดียวกับ `CLIENT_RE_QUEUE.md` ⇒ `RE-071` จองแล้วในรอบเดียวกัน ใบนี้จึงเป็น **072** ไม่ใช่ 071)

🔴 **nonclaims ที่ยังยืน:** ① ช่วง `t=222.4→267.4` ที่ "ไม่มีอะไรขึ้น" เป็น **ผลลบที่กล้องคุมไม่ครบ** ⇒ อ่านได้แค่ "ไม่ถูกสังเกต"
② `ตาย!` หลัง `MOVE_A_2` เป็น **การเรียงเวลา ไม่ใช่การพิสูจน์เหตุ** ③ ไม่ได้พิสูจน์ว่าร่างที่เห็นคือ `ProbePlayer01` หรือ `02` (ไม่มีป้ายชื่อ ระบุจากตำแหน่งเท่านั้น)
① 🔴 **ยังไม่ปลด (chief R169 แก้ตัวเองหลัง `pf-adversary` — ฉบับแรกของ R169 เขียนว่าปลดแล้ว นั่นผิด)**
   ตัวเลข 1.4% ของรอบสี่ **ไม่ได้วัดความไวของเครื่องมือ** — โมเดลมนุษย์ที่ระยะนั้นกินราว **390 px** เทียบเพดานสัญญาณรบกวน **3,120 px**
   ⇒ **ต่ำกว่าเพดาน ~8 เท่า** ⇒ ยังอ่านได้แค่ **"ไม่ถูกสังเกต"** · ท่าปลดที่ถูกอยู่ในบล็อก `R4` ข้อ ② (crop + positive control ในวิดีโอเดิม)
④ ~~**รอบเดียว หนึ่งเซสชัน ⇒ ยังไม่ใช่คุณสมบัติของไคลเอนต์จนกว่าจะทำซ้ำได้** — การทำซ้ำเป็นงานที่ยังเหลือของใบนี้ ไม่ใช่ของใบใหม่~~
   🟢 **ปลดแล้วโดยรอบสี่ (chief R169 · 2026-08-25 ~21:0x +07:00) — แต่ปลดเฉพาะ *ลำดับเหตุการณ์*** (latency ต่างกัน 3.3 เท่า · ระยะสังเกตต่างกัน 5 เท่า) · ดูบล็อก `R4` ข้อ ①
⑤ ~~`ProbeControl03` เงียบเป็น **คำยืนยันด้วยตาของผู้เทส** · ผู้ช่วยยังไม่ได้ไล่วิดีโอยืนยันว่ากล้องกวาดถึง `X -9,290` จริงในช่วง `t=282..300`~~
   🔴 **ยังไม่ปลด — แต่เหตุผลที่ chief R169 เขียนตอนแรกผิด และแก้แล้ว**
   ~~ผู้เทสเดินไปทาง `+X` ทั้งสองรอบ ไม่เคยเข้าใกล้ `-9,290`~~ ⇒ **ล็อกการเดิน `-7,939 → -7,294` เป็นของ *รอบสี่* เท่านั้น** (จดหมายรอบสี่ §⑦ generalize ไปยังรอบสามเอง)
   🔴 **รอบสามผู้เทสอยู่ที่ `X -8,876`** (HUD ในภาพ `GT030R3_1159_NAVYTRANSFER_PRESENT_t221.5s.jpg` ที่ commit แล้ว) = **ห่างจาก `-9,290` แค่ 414 หน่วย**
   ซึ่งเป็นระยะที่ NPC มองเห็นได้ชัดในเฟรมพวกนี้ ⇒ 🟢 **วิดีโอรอบสามอาจตอบข้อนี้ได้ และยังไม่มีใครเปิด** — นี่คืองานที่ถูกกว่าการรันรอบใหม่มาก

### 🟢 R4 — รอบที่สี่ (attended · คุณ Panya ขับเอง) · จ็อบ 1161/1162/1163 · **บันทึกโดย chief R169 · 2026-08-25 ~21:0x (+07:00)**

**`OBSERVER_CONFIRMED: 2026-08-25T20:05+07:00`** (ยืนยันสองครั้ง: 19:5x และ 20:0x) · จดหมาย `notes_to_chief\consumed\20260825_2010_*.md`

**① ทำซ้ำได้ — 🔴 *เฉพาะลำดับเหตุการณ์* ไม่ใช่ "ตัวเลขเดียวกัน" ⇒ nonclaim ④ ปลด (แต่ปลดแคบกว่าที่จดหมายเขียน)**

🔴 **chief R169 แก้ถ้อยคำของตัวเองหลัง `pf-adversary`:**
- **latency ไม่ได้ทำซ้ำ** — R3: `ตาย!` ที่ `268.0` vs `MOVE_A_2` `267.37` = **`+0.63` วิ** · R4: `400.6` vs `400.41` = **`+0.19` วิ** ⇒ **ต่างกัน 3.3 เท่า**
  และ nonclaim ④ ของ R3 เองบอกว่านาฬิกาวิดีโอ-vs-สาย **ยังไม่จูน** (error ที่วัดได้ `0.0`/`0.58`/`1.82` วิ ข้าม GT-033 สามรอบ) ⇒ **ทั้งสองค่าอยู่ในแถบ error ที่ยังไม่วัด**
- **คำว่า "วินาทีที่ 45" ของผู้เทสแทบไม่มีข้อมูล** — เฟรมของเลนนี้ห่างกัน `15.000` วิ **โดยการออกแบบ** ⇒ `MOVE_A_2` อยู่ที่ trigger+45 อยู่แล้ว
  คนแยก `MOVE_A_2` จากอย่างอื่นในช่วง ±7 วิไม่ได้ ⇒ **หลักฐานการทำซ้ำตัวจริงคือเฟรม `400.6`** คำพูดของผู้เทสเป็นแค่ตัวประกอบ
- 🔴 **เงื่อนไขการสังเกตไม่เหมือนกันและต่างกัน 5 เท่า** — ผู้เทสอยู่ห่างจุด spawn **272 หน่วยในรอบสาม** แต่ **1,387 หน่วยในรอบสี่**
  ⇒ ขนาดโมเดล ความอ่านออกของแผง และคำถามเรื่องความไวทั้งหมดในข้อ ② สเกลไปตามระยะนี้ ⇒ **ห้ามเทียบผลเชิงภาพข้ามสองรอบก่อนเทียบเงื่อนไขครบสี่ข้อ** (ตำแหน่ง · มุมกล้อง · ซูม · ระยะ)
- 🔴 **จดหมายรอบสี่ไม่มี `BOOT_COMMIT`/HEAD ที่บูต** (`AGENTS.md:190` บังคับ · จดหมายรอบสามมี `06b62abd`) ⇒ **"ไม่แก้โค้ด ⇒ ไม่กินสล็อต" ยังยืนยันจากรีโปไม่ได้ ยืนบนคำบอกของจดหมาย**

**สิ่งที่ทำซ้ำได้จริง: บูตอิสระคนละใบ (จ็อบ 1161/1162/1163 · ห่างจากรอบสาม ~59 นาที) ให้ *ลำดับ* เดียวกัน — `ตาย!` ตามหลัง `MOVE_A_2` สองรอบติด**
```
VIDEO START                      19:41:07.862
RECV 0xAC52 (แชต ascii12)        19:47:03.259   t = 355.40
SENT SPAWN_BARE        181 B     19:47:03.269   t = 355.41
SENT SPAWN_AVATAR      288 B     19:47:18.269   t = 370.41
SENT MOVE_A_1           72 B     19:47:33.269   t = 385.41
SENT MOVE_A_2           77 B     19:47:48.270   t = 400.41
SENT NEGATIVE_CONTROL  218 B     19:48:03.269   t = 415.41
```
ผู้เทสรายงาน *"วินาทีที่ 45"* อีกครั้ง ⇒ `355.40 + 45 = 400.40` = **`MOVE_A_2` เป๊ะ เป็นรอบที่สอง**
**wire/DB:** `OPEN_SESSIONS 0 · INTEGRITY ok · FK 0` · CANON ไม่ขยับ · teardown exit 0 · ไม่แก้โค้ด ⇒ **ไม่กินสล็อต**

**② 🔴 ผลลบ 45 วินาทีแรก — กล้องนิ่งจริง แต่ nonclaim ① *ยังไม่ปลด* (chief R169 แก้ตัวเองหลัง `pf-adversary`)**

**[MEASURED · ผู้ช่วยหน้าสะพาน]** `t = 354 → 404` **ความต่างระหว่างเฟรมสูงสุด 3,120 px จาก 230,400 (1.4%)** ·
สิ่งเดียวที่ขยับคือ **วงรอบคาบ 10 วินาที** (ยอดที่ 360/370/380/390/400) = แอนิเมชัน ambient

🔴🔴 **แต่เลขนี้ *พิสูจน์ผลลบไม่ได้* — และเลขคณิตบนเฟรมของรอบสี่เองเป็นตัวหักล้าง:**
`230,400 px` = `640×360` ⇒ การ diff รันที่ **1/3 ของความละเอียดภาพจริง (1920×1080)**
**[MEASURED-approx · วัด bounding box บนภาพที่ commit แล้ว]** ที่ระยะของจุด spawn ในเฟรมนั้น:

| วัตถุ | ที่ 1920×1080 | ที่ความละเอียดของ diff (÷9) | เทียบเพดาน 3,120 px |
|---|---|---|---|
| โมเดลมนุษย์ทั้งตัว | ~38 × 92 ≈ 3,500 px² | **~390 px** | **ต่ำกว่าเพดาน ~8 เท่า** |
| ร่างที่กำลังทรุด + ข้อความ `ตาย!` (t=400.6) | ~3,900 px² | **~435 px** | ต่ำกว่าเพดาน ~7 เท่า |

⇒ 🔴 **เครื่องมือมองไม่เห็นสิ่งที่กำลังบอกว่าไม่มี** · และ **เหตุการณ์ที่เกิดขึ้นจริงสองอย่างอยู่ในหน้าต่างที่วัด**
(NPC + แผงหายที่ `356.5` · โมเดลปรากฏ+ทรุดที่ `400.6`) **แต่ค่าสูงสุดยังคงเป็น 3,120 px** ⇒ metric นี้ตาบอดต่อทั้งสองเหตุการณ์
⇒ **ไม่มี positive control** — ไม่มีใครแสดงว่าสิ่งที่ *ถูกวาดจริง* ทำให้ตัวเลขเกิน 3,120 px

🔴 **สถานะที่ถูกต้อง: `nonclaim ①` ยังเปิดอยู่** — อ่านได้แค่ **"ไม่ถูกสังเกตด้วยเครื่องมือที่ยังไม่ได้วัดความไว"**
**ห้ามเขียนคำว่า "ผลลบที่คุมตัวแปรได้" กับหน้าต่างนี้** · และ **[เสนอ]** เท่านั้นสำหรับ *"หนุนสมมติฐาน (ข) actor เกิดแล้วแต่วาดไม่ออก"*

🟢 **ท่าที่ปลด ① ได้จริงและถูกมาก — ทำได้จากวิดีโอที่มีอยู่แล้ว ไม่ต้องบูตใหม่:**
รัน diff ใหม่ **โดย crop เฉพาะกล่องรอบพิกเซลของจุด spawn** แล้ว **calibrate ด้วย positive control ที่อยู่ในวิดีโอเดียวกัน** —
**การหายของ NPC ที่ `356.5` และการปรากฏของร่างที่ `400.6` เป็น positive control ฟรีที่ระยะเดียวกันเป๊ะ**
⇒ 🔴 **กฎที่ควรใช้กับผลลบทุกใบหลังจากนี้: ผลลบจะ "คุมตัวแปรได้" ก็ต่อเมื่อ *วัดเพดานการตรวจจับแล้ว* และ *ระบุ positive control ที่ขนาดเดียวกันได้*** — ไม่ใช่แค่บอกว่ากล้องนิ่ง

**③ 🔴 ตัวคุม `actor_type 4` — ใช้ได้ แต่ *ระบุตัวไม่ได้* (chief R169 · `pf-adversary` จับได้)**
จดหมายเรียกมันว่า `P0 Navy Transfer` — **นั่นคือการยกชื่อมาจากรอบสาม ไม่ใช่การวัดของรอบสี่**
**[MEASURED · chief re-derive เองจาก `gamedata/scene/bg0001/bg0001.placements.tsv` ที่ commit แล้ว]** จากพิกัดผู้เทสของแต่ละรอบ:

| รอบ | พิกัดผู้เทส | ใกล้ที่สุด | อันดับของ placement `P0 (-9140,-2780)` |
|---|---|---|---|
| R3 | `(-8876,-2715)` | **`idx 0` = `P0` · 271.9** | **ที่ 1** ⇒ การระบุของรอบสามสมเหตุสมผล |
| **R4** | `(-7775,-2531)` | **`idx 1` `(-8013.5,-2780)` · 344.8** | 🔴 **ที่ 3 · ห่าง 1,387.5 (ไกลกว่าตัวที่ใกล้สุด 4 เท่า)** |

⇒ 🔴 **ตรรกะ "ตัวที่ใกล้ที่สุด" ที่ทำให้รอบสามระบุถูก ให้คำตอบคนละตัวในรอบสี่** ⇒ **ห้ามเรียกมันว่า `Navy Transfer` จนกว่าจะวัด**
⇒ 🔴 **และข้ออ้าง "จุด spawn อยู่ในกรอบภาพเพราะเห็น `Navy Transfer`" ตกไปด้วย** — ถ้าร่างนั้นคือ `idx 1` ก็ไม่มีอะไรในเฟรมมาร์กพิกัด `-9,140` เลย
🟢 **แต่การถอนข้อสรุปเรื่องชื่อไม่ต้องพึ่งการระบุตัวนี้** — มันยืนอยู่บนแผงของผู้เล่นเอง (บล็อกถอนข้างบน) ซึ่งไม่มีข้อสงสัยเรื่องตัวตนเลย

**④ แอนิเมชันการตาย — รอบสามจับไม่ได้ รอบสี่จับได้**

| t | เห็นอะไร |
|---|---|
| `400.41` | `MOVE_A_2` ออกสาย |
| **`400.6`** | `ตาย!` ขึ้นแล้ว · โมเดล **ยันตัวด้วยแขนข้างเดียว หัวยังเงย** — กำลังทรุด |
| **`401.3`** | **ฟุบราบกับพื้น** |

⇒ **ไคลเอนต์เล่น transition การตายยาว ~0.7 วินาที** ไม่ได้โผล่มาเป็นศพนิ่ง
🔴 **สำคัญต่อ `GT-036`:** โมเดล **ปรากฏพร้อมกับการตาย** — ไม่เคยถูกวาดในสภาพเป็น ๆ เลยแม้แต่เฟรมเดียว
⇒ ยังแยกไม่ออกระหว่าง **(ก)** `mask 0x03` จุดการตาย กับ **(ข)** actor เกิดมาตายอยู่แล้ว แล้ว `MOVE_A_2` แค่ทำให้มันถูกวาดครั้งแรก ⇒ **`RE-071` ยังจำเป็นเหมือนเดิม**

**⑤ NPC แมพตัวหนึ่งหายอีกครั้ง — ผลนี้เป็นของ `GT-072`**
`t=354.5` NPC ยืนอยู่ ถูก target แผงเปิด → `t=356.5` มุมกล้องเดิม ทั้งคู่ไม่อยู่ในเฟรมหลัง
🔴 **ห้ามอ่านมากกว่านี้ที่นี่** — สองเฟรมห่างกัน **2.0 วิ (60–120 เฟรมที่ไม่มีใครเปิด)** และในช่วงนั้น **ผู้เทสกด Enter ส่งแชต** (`RECV 0xAC52` `t=355.40`)
⇒ **"หายพร้อมกัน" ยังไม่ได้วัด · ห้ามอนุมานกลไกฝั่งไคลเอนต์** · รายละเอียดครบและตัวก่อกวนที่ยังไม่ถูกตัดออก อยู่ในบล็อกปิดผนึกท้ายใบ `GT-072`
(🔴 chief R169 เคยเขียนที่นี่ว่า *"ไคลเอนต์ทำลาย actor object ทิ้ง"* — **ถอนแล้ว** เป็นคำอธิบายกลไกที่ใบ `GT-072` ห้ามไว้เอง และหลักฐานเป็นกลางระหว่าง `N1` กับ `N2`)

**⑥ วิธีเลือกเป้า:** ผู้เทสยืนยัน **ต้อง double-click เท่านั้น · คลิกเดียวไม่ได้ · `Tab` ไม่ได้**
🔴 **แต่จดหมายไม่ได้ระบุว่าผู้เทสลอง `Tab` กับ actor ตัวไหน** — และ `GAME_TEST_QUEUE.md:2409` (`GT-032` PASS) บันทึกว่า **`Tab` ใช้ได้จริงกับ NPC `actor_type 4` `0x2001`**
⇒ ข้อนี้อ่านได้เฉพาะ **scoped กับ `actor_type 2` ของเรา** ⇒ ครึ่ง `Tab` ของวินิจฉัย R119 ใช้กับ `actor_type 2` ไม่ได้ **แต่ยังใช้ได้กับ NPC แมพ**

**หลักฐานที่ commit แล้ว:**

| ไฟล์ (`evidence_screens/`) | ขนาด | sha256 |
|---|---|---|
| `GT030R4_1162_NAVY_TARGETED_PANEL_HP100_NONAME_t354.5s.jpg` | 417,178 | `63e4e8a584d3371678b7c00059036eae1e4c5b29501f335f1e09f26ad223b7a4` |
| `GT030R4_1162_NAVY_AND_PANEL_BOTH_GONE_t356.5s.jpg` | 413,373 | `07ea78110ca3cec10339adc263a2da0b7fe9129b1c5a796fd23a3e9bce8486a3` |
| `GT030R4_1162_DEATH_ANIM_MIDCOLLAPSE_t400.6s.jpg` | 417,356 | `5e242f19e8c2ed856b6aa66a223841f383de5398cbd8fef77da14a64a063c29a` |
| `GT030R4_1162_DEATH_ANIM_FLAT_t401.3s.jpg` | 417,064 | `58b8f9c741a74c7d0d900392fe7324803d6134a459653fd5f118c55df48298fc` |

**บนสะพานเท่านั้น 🔴 ห้ามลบ:** `evidence_video\1162_gt030r4_FULLROUND_20260825_194107.mkv` · `GameClient\capture_gt030r4_20260825_194103\`

> 🔢 **ใบนี้ไม่กินเลขคิวใหม่** — เป็น **รอบที่สามของ `GT-030`** เลนเดียวกัน (`HYP-PF-025`) เป้าเดียวกัน
> ท่าเดียวกับ `GT-045 v2/v3` ที่อยู่ใต้เลขเดิม · ใบ `GT-030` เดิม **ยังอยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย** — ผลรอบ #12 และรอบ rerun เป็นประวัติที่ใบนี้ยืนอยู่บนมัน

### 🔴 คำเคาะที่ปลดล็อกใบนี้ (เก็บถ้อยคำเดิมไว้เป็นประวัติ — ขีดฆ่าได้ ลบไม่ได้)

**ถ้อยคำเดิมในหัวใบ `GT-030`:** ~~🔴 ห้ามรันรอบสาม — เส้นทางต่อ = static render-mask/selection~~
**ถ้อยคำเดิมใน nonclaims ของ `GT-030`:** ~~ถ้า rerun จบที่ "พาเนลไม่ขึ้นทุกตัว" อีก **อย่ารันซ้ำรอบสาม**~~

> 🟢 **ยกเลิกโดยเจ้าของ (คุณ Panya) 2026-08-25 ~18:15 (+07:00)** — *"ให้รัน GT-030 เทสอีกรอบได้ โดยฉันจะ attend และขับเอง"*
> จดหมาย: `notes_to_chief\consumed\20260825_1815_PANYA-RULINGS-FOUR-quota-cap5-GT036-lethal-scoped-GT030-rerun.md` §④
> 📌 **และข้อห้ามเดิมเป็นข้อห้ามแบบมีเงื่อนไข** — มันห้าม *"รันซ้ำเพื่อไล่ target panel"* · **ใบนี้ไม่ได้ไล่ target panel** มันไล่คำถามคนละข้อ (ดู objective) ⇒ แม้แต่บนเงื่อนไขของตัวเอง ข้อห้ามเดิมก็ไม่ครอบใบนี้ · แต่ **ตัวที่ปลดจริงคือคำเคาะของเจ้าของ ไม่ใช่การตีความข้อนี้**

### 🟢 งบเวอร์ชัน: **ศูนย์สล็อต** (ตรวจเองแล้ว ไม่ได้เชื่อคำบอก)
- `docs/HYPOTHESIS_LEDGER.json` → `HYP-PF-025` มี `tracked_versions` **2 ตัว** (`REMOTE-PLAYER-ENCODER-001`, `REMOTE-PLAYER-DISPATCH-001`) · `max_versions: 5` ⇒ **2/5**
- ใบนี้ **ไม่แก้โค้ด ไม่แก้ mask ไม่แก้ไบต์ ไม่แก้ scenario แม้ตัวอักษรเดียว** ⇒ ไม่เพิ่ม tracked version ⇒ **ไม่กินสล็อต**
- 🔴 **ถ้าใครระหว่างรอบคิดจะเปลี่ยน mask/ไบต์เพื่อ "ลองให้มันขึ้น" — นั่นคือ wire change · กินสล็อต · ต้องให้ chief ออกแบบก่อน · รอบนี้ห้ามเด็ดขาด**

### ที่มา (อ่านก่อนบูต — ทั้งหมดอยู่ในใบ `GT-030` เดิมแล้ว ไม่ทวนซ้ำเกินจำเป็น)
- **รอบ #12 (2026-08-21):** wire ครบ 5 เฟรม · client ตัดสินไม่ได้ · ⭐ **การพบเห็นที่ยังไม่อธิบาย:** ตัวละคร**หน้าตาแบบผู้เล่น (ชายหนุ่มชุดน้ำเงิน-ขาว) ที่ X ≈ `-8681`** — *"อาจเป็น actor_type 2 ตัวแรกที่เรนเดอร์จริงในประวัติโปรเจกต์ หรืออาจเป็น NPC ประจำแมพ — ยังตัดสินไม่ได้ทั้งสองทาง"*
- **รอบ rerun (2026-08-23 00:09-00:25):** wire ครบ 5 เฟรม ไม่มี refusal · ผู้เทสเดินไปยืนติด B (~33 หน่วย) และ A-หลัง-MOVE (~52 หน่วย) **ไม่เห็นโมเดล ไม่มีพาเนล** ⇒ **CLIENT NO-RENDER แบบ persistent**
  🔴 **แต่รอบนั้นทิ้ง nonclaim ไว้สองข้อ ซึ่งเป็นเหตุผลทั้งหมดของรอบสาม:** (ก) ภาพ before/after ไม่ครบฟอร์ม — ภาพแรกที่อ่านได้อยู่ที่ **+3.487 วิ** หลังทริกเกอร์ · baseline/+0 ไม่คงอยู่ ⇒ **transient < 3.487 วิ = non-observed ไม่ใช่ไม่เกิด** (ข) รอบนั้น**ไม่ได้กลับไปดูจุด X ≈ `-8681` เลย** — จดหมายผลไม่มีบรรทัดไหนพูดถึงชายหนุ่มคนนั้น (grep `8681` = 0 hit)
- 🆕 **ของที่สองรอบก่อนไม่มี:** **PLAYBOOK ข้อ 13 (จดสีป้ายชื่อทุกป้าย)** และ **`RE-067` ปิดแล้ว (PASS/MIXED)** ที่พินว่าไคลเอนต์เลือก *UI text property* ของป้ายอย่างไร ⇒ **รอบนี้เก็บสีได้ ซึ่งสองรอบก่อนเก็บไม่ได้**
- 🔴 **erratum ของใบเดิม (chief R167 · ไม่ได้แก้ถ้อยคำเดิม แค่ติดป้ายไว้):** หัวใบ `GT-030` เดิมเขียนว่าสวีป *"75 วิทั้งชุด"* — **ไม่ตรงกับ scenario ที่บูตจริง** ซึ่งตั้ง `spacing_seconds: 15.0` · `first_frame_delay_seconds: 0.0` · 5 สเต็ป ⇒ เฟรมตกที่ **+0/+15/+30/+45/+60** · **ใบนี้ใช้หน้าต่าง +0 ถึง +90 วิ** และตัวเลข 75 วิในใบเก่าเป็นของที่ล้าสมัย **อย่ายึด**

### objective (claim เดียว)
**ของทุกอย่างที่ปรากฏบนจอในแนว probe (X `-9289.957` ถึง `-8681` · Y ≈ `-2780`) ระหว่างสวีป อยู่ที่นั่นมาก่อนแล้วตั้งแต่ก่อนเลนนี้ส่งไบต์แรก ใช่หรือไม่**
ตัดสินด้วย: **ภาพก่อนทริกเกอร์ ↔ วิดีโอต่อเนื่องกรอบกล้องเดียวกันตลอดสวีป ↔ ภาพหลังสวีป**

🔴 **ทำไมนี่คือ claim เดียว ไม่ใช่สอง** (กติกา "หนึ่งใบหนึ่งข้ออ้าง"): ตัวหักล้างมีตัวเดียว = **"มีอะไรใหม่โผล่หลังทริกเกอร์"** · คำถามสองข้อที่ค้างเป็น **สองผลลัพธ์ของตัวหักล้างตัวเดียวกัน** ไม่ใช่สองข้ออ้าง:
- **(ก) ชายหนุ่มที่ X ≈ `-8681` เป็นใคร** — ถ้าเขาอยู่ในภาพ **ก่อน**ทริกเกอร์ ⇒ เขาอยู่ในเซต "อยู่มาก่อนแล้ว" ⇒ **เขาไม่ใช่หลักฐานว่า actor_type 2 เรนเดอร์** · ถ้าเขาไม่มีก่อนแล้วมีหลัง ⇒ claim ถูกหักล้าง และเขาคือผู้สมัครตัวจริง
- **(ข) transient สั้นกว่า 3.487 วิ** — คือ **ความละเอียดทางเวลา**ของการเทียบเดียวกันนั้น ไม่ใช่คำถามใหม่ (รอบก่อนวัดด้วยภาพนิ่ง จึงหยาบ 3.487 วิ · รอบนี้วัดด้วยวิดีโอ 30 fps)

### 🔴🔴 ลำดับที่ห้ามสลับ — และเหตุผลที่มันเกือบทำรอบนี้พัง
**ตัวยิงของเลนนี้คือ "แชต ASCII 12 ตัว"** — เปิดโค้ดอ่านเองแล้ว ไม่ใช่อนุมานจากถ้อยคำในใบ:
`src/pirateforce_foundation/runtime.py` → `_dispatch_remote_player_hypothesis` (docstring: *"the same accepted 34-byte ascii12 shape"*)
```
classification = classify_chat_input_attempt(legacy, parsed)
if classification != "ascii12":
    self.events.append(f"remote_player_hypothesis_{classification}_no_reply")
    return []
```
⇒ 🔴 **ถ้าพิมพ์แชต 12 ตัวเป็นขั้นแรกของรอบ (ท่า clapper มาตรฐาน) sweep จะยิงทันทีตั้งแต่ยืนอยู่จุดเกิด — ก่อนเดินถึง landmark ก่อนถ่าย baseline — และ one-shot ไหม้ทั้งรอบ**
⇒ **ลำดับบังคับ: เดินสำรวจ + ถ่าย PRE → ถ่าย baseline → *แล้วค่อย* พิมพ์แชต** · **แชตครั้งเดียวทำสองหน้าที่: เป็นตัวยิง และเป็น clapper** (จุดจูนอยู่ที่ตอนยิง ซึ่งใช้ได้เต็มที่)

**ชุดเลนของบูตนี้ (กติกา clapper R166-b บังคับให้ระบุทั้งชุด):** **หนึ่งเลนเดียว = `HYP-PF-025`** · ไม่ใช่บูตรวม · ไม่มี flag hypothesis ตัวอื่นในคำสั่งบูต ⇒ เลนที่ยิงด้วย `ascii12` ในบูตนี้มีตัวเดียว และมันคือเลนของใบนี้เอง ⇒ **ห้ามใส่ clapper แยกอีกบรรทัด — ใช้ตัวยิงเป็น clapper**

### 🔴 ท่าเดิน/ท่ากล้อง — ข้อที่เคยทำโปรเจกต์เสียสามรอบ อ่านให้ครบก่อนแตะคีย์
| ท่า | ทำอะไรจริง | ยิง `TargetPosVital` ไหม | ใบนี้ใช้ได้เมื่อไร |
|---|---|---|---|
| **คลิกขวาค้างลากเมาส์** | หมุน **มุมกล้อง** อย่างเดียว · **ทิศหันของตัวละครไม่ขยับ** | 🟢 ไม่ยิง | ✅ **ปลอดภัยตลอดรอบ รวมถึงก่อนทริกเกอร์** · ใช้เป็นตัวเช็ค NO-CRASH |
| **`Q` / `E`** | **หันตัวละคร** กล้องแพนตาม | 🔴 ยิง | ⚠️ ใช้ได้ก่อนทริกเกอร์ · ❌ **ห้ามใช้ระหว่างสวีป** (ทำกรอบกล้องเสีย) · ❌ **ห้ามใช้เป็นตัวเช็ค NO-CRASH** |
| **`W/A/S/D`** | เดิน (เปลี่ยนทั้งตำแหน่งและทิศหัน) | 🔴 ยิง | ⚠️ ใช้ได้ก่อนทริกเกอร์ · ❌ ห้ามระหว่างสวีป |

🟢🔴 **ข้อที่ต้องอ่านคู่กันเสมอ มิฉะนั้นผู้เทสจะแข็งตัวอยู่กับที่:**
บรรทัด *"ห้ามแตะก่อนทริกเกอร์"* ในตารางกลางของ PLAYBOOK เป็นกฎของ**เลนที่การเคลื่อนไหวไปแตะตัวยิง**
🔴 **เลนนี้ตัวยิงคือแชต `ascii12` เท่านั้น (เปิดโค้ดยืนยันแล้วข้างบน)** ⇒ **`W/A/S/D` และ `Q/E` ก่อนทริกเกอร์ *ไม่* ทำให้ sweep ยิง และ *ไม่* กิน one-shot**
⇒ **การเดินไป landmark และเดินสำรวจแนว +X ก่อนทริกเกอร์ เป็นขั้นบังคับของใบนี้ ไม่ใช่ความเสี่ยง**
🔴 **ประโยคเดียวที่ต้องจำ:** ตัวที่ยิง `TargetPosVital` คือ **การเปลี่ยนทิศหันของตัวละคร** ไม่ใช่ **การขยับกล้อง** — และ `TargetPosVital` **ไม่ใช่** ตัวยิงของเลนนี้

### db (สำเนาเสมอ — canonical ไม่ถูกเปิดตลอดรอบ)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-030-R3_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt030r3.sqlite3
```
- เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง**
- เลนนี้ `persisted_post_state.database_write = "none"` ⇒ เกณฑ์สำเนา: **row-diff ทุกตารางต่างได้เฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง** · จด `max(lease_generation)` ก่อน-หลัง
- 🔴 **สำเนาใหม่ทุกบูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดเสมอ** — เผื่อเวลาเดินไป landmark ไว้ในแผน

### 🔴 ก่อนบูต — resolve commit เขียว (รันเครื่องมือ ห้ามก๊อป SHA เก่า)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` · **exit 3** = ใบนี้รอ gate ไม่ได้รอผู้เทส **ห้ามบูต** · บรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ จดลงผลเสมอ
- **ยืนยันหกข้อกับ `<SHA>` ที่จะบูตจริง — ต้องครบ:**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "remote-player-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/remote_player_hypothesis_visibility_probe.json && echo SCENARIO_PRESENT
git grep -n "HYP_PF_025_REMOTE_PLAYER_" <SHA> -- src/pirateforce_foundation/ scenarios/
git grep -n "classify_chat_input_attempt" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "export-events" <SHA> -- src/pirateforce_foundation/app.py
```
1. `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ · 2. เจอ flag จริง (🔴 **ห้ามใช้ `--help` เป็นหลักฐาน — มันคืน 0 บรรทัด exit 0 ผ่านสะพาน**) · 3. เห็น `SCENARIO_PRESENT` · 4. เจอ label prefix · 5. **ยืนยันว่าตัวยิงยังเป็น `ascii12` ใน commit ที่จะบูตจริง** · 6. เจอ `export-events` ⇒ ใส่ flag · ไม่เจอ ⇒ ตัดออกแล้วจดไว้
- **อ่านค่า pin ต่อเฟรมจาก scenario ใน commit ที่บูต ห้ามฝังเลข sha ลงในใบนี้:**
  `scenarios/remote_player_hypothesis_visibility_probe.json` → `probe.per_step.<LABEL>.frame_sha256` / `frame_size`
  · 🔴 **`SPAWN_AVATAR` พินเฉพาะโครง `pc_skeleton_sha256` 172 B** (`avatar_tail_excluded_from_pin: true`) — หาง avatar เป็น replay ของตัวละครที่เลือกอยู่ **ตัวเลขรวม (รอบก่อน 288 B) เปลี่ยนได้โดยไม่ผิด**
- ไม่ครบหกข้อ + ยังไม่ได้ค่า pin = **ห้ามบูต** ใบอยู่ READY รอต่อ

### server args (เป๊ะ · opt-in เท่านั้น · `production_allowed=false`)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt030r3.sqlite3 --remote-player-hypothesis-scenario scenarios\remote_player_hypothesis_visibility_probe.json --export-events
```
- 🔴 **ห้ามใส่ flag hypothesis ตัวอื่นแม้แต่ตัวเดียว** — ชุดเลนของบูตนี้ต้องเป็น **หนึ่งเลน**
- console label = `HYP_PF_025_REMOTE_PLAYER_<STEP>` · event = `remote_player_hypothesis_visibility_probe_sent` — **เห็นชื่ออื่น = บูตผิดไฟล์ หยุด**
- **one-shot ต่อ GAME connection** ⇒ **บูตใหม่ = รีอาร์ม** · ยิงซ้ำใน connection เดิม = `remote_player_hypothesis_already_sent_no_reply` · **reconnect กลางรอบ = ได้ sweep ชุดใหม่ และ probe ชุดเก่าไม่ despawn — ถ้าเกิด ให้จดทันทีและถือว่ารอบเสียการเทียบ**

### 🔴 ตัว trigger แชต — 12 ตัวอักษร printable ASCII เป๊ะ
- ใช้ **`PFCHATPROBE1`** (นับ: P-F-C-H-A-T-P-R-O-B-E-1 = **12 ตัวพอดี** · เป็นสตริงเดียวกับที่รอบ rerun ใช้ ⇒ ไบต์ขาเข้าเหมือนรอบก่อน ไม่มีตัวแปรใหม่)
- 🔴 **สั้น/ยาวกว่า 12 = ถึงเซิร์ฟเวอร์แต่เงื่อนไขเงียบ ๆ ไม่ผ่าน ไม่มี error sweep ไม่ออกเฉย ๆ**
- 🔴 **คลิกช่องแชตให้โฟกัสก่อนพิมพ์เสมอ** — ตัวอักษรที่พิมพ์ตอนช่องแชตไม่โฟกัส **กลายเป็นฮอตคีย์** (มี toggle ที่ปิดเลขดาเมจทั้งจอเงียบ ๆ โดยที่ wire เหมือนเดิมทุกไบต์)
- Enter **หนึ่งครั้ง** · หลัง Enter **ห้ามพิมพ์อะไรอีกทั้งรอบ**

### steps (คลิกต่อคลิก)
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp (+07:00) · preflight จอว่าง (`staged\TEMPLATE_preflight_unattended.ps1` — เจอหน้าต่าง elevated = ABORT ทั้งรอบ) · เทียบ sha canonical · copy DB สองใบ

1. **สตาร์ตเซิร์ฟเวอร์ก่อน แล้วค่อยบูต client เสมอ** (🔴 client ที่บูตโดยไม่มีเซิร์ฟเวอร์ตายเองใน ~3.5 นาที · 🔴 ถ้ารอบก่อนเพิ่งฆ่า client ไป **ต้อง restart เซิร์ฟเวอร์ก่อน**) — จัดหน้าต่าง console ให้มองเห็นข้างจอเกมโดยไม่บังพื้นที่วัด · **ตลอดรอบห้ามคลิก console**
2. เข้าเกมด้วยตัวละครเดิม (ท่า `Return` → เข้าเกม · คลิกปุ่มอาจไม่ติด — บทเรียนรอบ #12) · เลือก**ช่องแรก** · ปุ่มซ้ายสุดของแถวล่าง = **ลบตัวละคร ห้ามกด**
3. เข้าแมพ เห็น HP/minimap/ชื่อแมพ → **เริ่มอัดวิดีโอต่อเนื่องตรงนี้ ยาวจนจบ session** ลง `evidence_video\` ด้วย `staged\TEMPLATE_video_recorder.ps1 -FrameRate 30` · จดบรรทัด `VIDEO START pid= start= fps= path=` ลงผล (🔴 `start=` คือเวลาที่เรา**สั่ง** ffmpeg ไม่ใช่เวลาที่เฟรมแรกถูกจับ — ห้ามใช้เป็นสมอเวลา)
4. **เดินไปหา NPC `Navy Transfer`** (landmark · identity `0x2001` · X `-9139.957` Y `-2780.045` Z `223.292`) — ยืนข้าง ๆ ไม่ทับ · จด X/Y บน HUD
5. **PRE-SURVEY (ขั้นที่ตอบคำถาม (ก) — ทำ *ก่อน* ทริกเกอร์เท่านั้น):** เดินตามแนว **+X** จาก landmark ไปจนถึง **X ≈ `-8681`** โดยแวะถ่ายภาพ **full-res** เป็นชุด `PRE1..PREn` ให้ครอบทั้งแนว (`-9289.957` / `-9139.957` / `-8989.957` / `-8839.957` / `-8681`) — **ทุกภาพต้องอ่าน X/Y บน HUD ได้**
   - ⭐ **สิ่งที่ต้องตอบให้ได้จากชุด PRE:** *"ที่ X ≈ `-8681` มีตัวละครหน้าตาแบบผู้เล่น (ชายหนุ่มชุดน้ำเงิน-ขาว) ยืนอยู่ **ก่อน**ที่เลนนี้จะส่งไบต์แรกหรือไม่"* — **มี / ไม่มี / อยู่นอกเฟรม** เขียนตรง ๆ สามทาง
   - ถ้า **มี**: ถ่ายเพิ่มระยะประชิด + เต็มตัว + เห็นหัว (ป้ายชื่อถ้ามี) · **ยังไม่ต้องคลิกเขาตอนนี้** (คลิกทีหลังในข้อ 12)
   - 🔴 **ห้ามพิมพ์อะไรทั้งสิ้นในขั้นนี้**
6. เดิน**กลับ**มายืนที่จุดที่มองเห็นแนว probe ได้กว้างที่สุด · จด X/Y
7. **ซูมออกให้สุด (ขั้นบังคับ):** หมุนล้อเมาส์ซูมกล้องออกจนสุด · **จดเวลาที่ซูมทุกครั้ง** (🔴 nonclaim: ไม่มีใครเคยวัดว่าล้อเมาส์ยิง `TargetPosVital` หรือไม่)
8. **ตั้งกรอบกล้อง `BASE_WIDE` แล้วล็อกไว้:** ใช้ **คลิกขวาค้างลากเมาส์** อย่างเดียวจัดมุมจนเห็นแนว probe ให้มากที่สุด **โดยหัวของทุกจุดที่จะดูอยู่ในเฟรม** → ถ่าย **`BASE_WIDE`** (full-res)
   - ถ้ามุมเดียวครอบไม่หมดจริง ๆ: ให้ `BASE_WIDE` ครอบ **ฝั่ง +X (จุดทับ NPC · B `-8989.957` · A-หลัง-MOVE `-8839.957`)** เป็นหลัก แล้วถ่าย **`BASE_MINUSX`** ของฝั่ง `-9289.957` เพิ่มหนึ่งใบ
   - 🔴 **ถ้าเลือกทางนี้ ต้องเขียนลงผลว่า "ฝั่ง `-X` (C) ไม่ได้อยู่ใต้วิดีโอต่อเนื่อง ⇒ transient ของ C = non-observed"** — ห้ามเงียบ
9. 🔴 **ยิงทริกเกอร์ = clapper (ครั้งเดียวของทั้งรอบ):** คลิกช่องแชตให้โฟกัส → พิมพ์ **`PFCHATPROBE1`** → **`Return` หนึ่งครั้ง** → **คลิกพื้นว่างเพื่อปลดโฟกัสแชต** → **มือออกจากคีย์บอร์ด**
   - **จดสองอย่างทันที:** (i) **เฟรมที่ช่อง input เคลียร์** (🔴 **สมอเวลาคือเฟรมนี้ ไม่ใช่เฟรมที่ตัวอักษรโผล่**) (ii) **บรรทัดแชตที่พิมพ์ ปรากฏในหน้าต่างแชตบนจอหรือไม่**
   - 🔴 **ข้อ (ii) คือการทดสอบว่า clapper ใช้ได้จริงไหม ไม่ใช่การใช้ clapper** — ทั้งโปรเจกต์ยังไม่เคยมีรอบไหนบันทึกว่าเห็นบรรทัดแชตของตัวเองปรากฏบนจอ **ถ้าไม่ปรากฏ ⇒ ไม่มีจุดจูน ⇒ เขียนลงผลว่า "clapper ไม่ให้ค่าในรอบนี้" นั่นคือผล ไม่ใช่ความล้มเหลว**
10. **ระหว่างสวีป (+0 ถึง +60 วิ · เผื่อถึง +90 วิ): ห้ามขยับอะไรทั้งสิ้น** — ห้ามเดิน ห้าม `Q/E` ห้ามซูม ห้ามคลิกอะไร ห้ามพิมพ์ · **ปล่อยวิดีโออัดกรอบ `BASE_WIDE` นิ่ง ๆ**
    - เหลือบดู console เพื่อยืนยันว่าเฟรมออก (`[G>]` / `PF-EVENT`) **ด้วยตาอย่างเดียว ห้ามคลิก**
    - ถ่าย **full-res** ที่ **+0 / +15 / +30 / +45 / +60 / +90 วิ** **โดยไม่ขยับกล้อง**
11. **หลัง +90 วิ — NO-CRASH:** **คลิกขวาค้างลากเมาส์แล้วกล้องหมุน = NO-CRASH** 🔴 **ห้ามใช้ `Q`/`E` เป็นตัวเช็ค**
12. **POST-SWEEP — เดินตรวจพิกัดจริง (ตอนนี้เดินได้แล้ว):** ไปทีละจุด ถ่าย full-res + อ่าน X/Y บน HUD ทุกจุด และ **คลิกซ้ายเลือกหนึ่งครั้ง (ลอง `Tab` ถ้าคลิกไม่ติด) → ถ่ายภาพ target panel เสมอ แม้พาเนลจะไม่ขึ้น**
    | จุด | พิกัด | ถ่ายเป็น |
    |---|---|---|
    | C (negative control) | X `-9289.957` | `POST_C` |
    | A จุดทับ Navy Transfer | X `-9139.957` | `POST_STACK` (🔴 คลิกอาจโดน NPC ก่อน — **จดว่าโดนตัวไหน**) |
    | B `ProbePlayer02` | X `-8989.957` | `POST_B` |
    | A หลัง MOVE | X `-8839.957` | `POST_AMOVE` |
    | ⭐ จุดชายหนุ่มรอบ #12 | X ≈ `-8681` | `POST_8681` (+ พาเนล `POST_8681_PANEL`) |
13. ออกจากเกม: **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย → **หยุดวิดีโอ** → **ปิดเซิร์ฟเวอร์ด้วย**
14. เก็บ raw GAME log ทั้งไฟล์ + console out/err (ทุกบรรทัด `[G>]` / `PF-EVENT`) → `PRAGMA integrity_check;` บนสำเนา → sha256 ทุกไฟล์
15. **teardown เสมอ** (ดูบล็อกใบเสร็จ) → เทียบ sha canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม

### 🔴 ลำดับข้ามใบ (คงเดิม ห้ามลืม)
- **ในรอบใหญ่เดียวกัน ต้องรัน `GT-030-R3` ให้จบ *ก่อน* `GT-032`** — `GT-032` ทำให้ landmark `0x2001` ขึ้นศัตรู แล้วมันจะใช้เป็นจุดอ้างอิงกลาง ๆ ไม่ได้อีก
- ห้ามพ่วงใบอื่นเข้าบูตนี้ (ชุดเลนต้องเป็นหนึ่งเลน)

### สิ่งที่ควรเห็นทีละเฟรม (คำทำนาย — **ไม่ใช่ข้อเท็จจริง · คำทำนายที่ผิดคือผล ไม่ใช่ความล้มเหลว**)
| t | เฟรม | คำทำนายของรอบนี้ |
|---|---|---|
| +0s | `SPAWN_BARE` — A `ProbePlayer01` **ทับตำแหน่ง Navy Transfer เป๊ะ** | คาดว่า **ไม่มีอะไรเปลี่ยนใน `BASE_WIDE`** · จุด stack ตัดสินอะไรไม่ได้อยู่แล้ว (โมเดล NPC บังได้ทั้งตัว) |
| +15s | `SPAWN_AVATAR` — B `ProbePlayer02` ที่ X `-8989.957` พก AvatarAttr ของตัวละครที่เลือกอยู่ | คาดว่า **ไม่มีอะไรโผล่** · **แต่ถ้าโผล่แม้เพียงเฟรมเดียวบนวิดีโอ นี่คือผลที่ใหญ่ที่สุดที่รอบนี้ทำได้** |
| +30s | `MOVE_A_1` — MovementAttr เดี่ยว mask `0x01` → A ไป X `-8839.957` | คาดว่าไม่มีอะไรขยับ · ถ้ามี: เดินหรือวาร์ป |
| +45s | `MOVE_A_2` — mask `0x03` heading π/2 | ถ้ามีตัวอยู่: หันหน้าไหม |
| +60s | `NEGATIVE_CONTROL` — C ที่ X `-9289.957` พก **NPCAttr ผิดคลาสโดยตั้งใจ** | คาดว่า **ไม่มีอะไรโผล่ฝั่ง `-X`** (bind gate `0x4697B0` เกต CNetNPC ต้อง drop เงียบ) |
| ตลอดสวีป | — | ⭐ **transient:** คาดว่า **ไม่มีแฟลช/เงา/โครงตัวใส ในเฟรมใดเลยบนวิดีโอ 30 fps** |
| PRE | — | ⭐ **คำทำนายหลักของรอบ:** **ชายหนุ่มที่ X ≈ `-8681` จะอยู่ในภาพ PRE (คือเป็นของแมพ)** — ถ้าเขา **ไม่อยู่ใน PRE แต่โผล่หลังทริกเกอร์** คำทำนายนี้ผิด และนั่นคือ **actor_type 2 ตัวแรกที่เรนเดอร์จริงในประวัติโปรเจกต์** |

### pass criteria — สองชั้น แยกกันเด็ดขาด 🔴 **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

**ชั้น (1) wire/DB + หลักฐานเชิงไฟล์ — ทำ headless ได้ ไม่ต้องมีคนหน้าจอ**
1. raw GAME log / console: **5 เฟรมเรียงตามลำดับ** `SPAWN_BARE` → `SPAWN_AVATAR` → `MOVE_A_1` → `MOVE_A_2` → `NEGATIVE_CONTROL` ห่างกัน **15.0 วิ** · ขนาด **181 / (โครง 172) / 72 / 77 / 218 B** · **`frame_sha256` ของสี่เฟรมที่พินได้ ต้องตรง `probe.per_step.<LABEL>.frame_sha256` ของ scenario ใน commit ที่บูต** · `SPAWN_AVATAR` ตัดสินด้วย `pc_skeleton_sha256` (172 B) เท่านั้น
2. 🔴 **census: นับ *ทุก* บรรทัด `[G>]` ทั้งไฟล์ แล้วรายงานยอดรวม ไม่กรองอะไรออก** — ยอดรวม ≠ 5 สำหรับเลนนี้ **คือคำตอบ ไม่ใช่ความผิดพลาด**
3. **ไม่มี label `HYP_PF_025_REMOTE_PLAYER_*` ปรากฏก่อนเฟรมแชตที่ถูกยอมรับ** + จดเวลานาฬิกาจริงของเฟรมแชต (`0xAC52`) และของ `[G>]` แรก
   🔴 **ข้อนี้เป็นเงื่อนไขก่อนหน้าของภาพชุด PRE ไม่ใช่หลักฐานว่าจอเห็นอะไร** · และ**ลำดับนี้ถูกค้ำด้วยเหตุ-ผลในโค้ด** — sweep ถูก compose **ในฐานะคำตอบต่อเฟรมแชต** ⇒ ไม่มีทางที่เฟรมเลนนี้จะออกก่อนแชต
4. ไม่มี `remote_player_hypothesis_*_no_reply` ใด ๆ · ไม่มี `ErrorData=28317` · ไม่มี traceback / stderr
5. DB สำเนา: `PRAGMA integrity_check` = `ok` · row-diff ต่างเฉพาะ `sessions` +1 ต่อการเข้าเกมหนึ่งครั้ง · จด `max(lease_generation)` ก่อน-หลัง · **sha256 canonical ก่อน-หลัง = `CANON_SHA.txt`**
6. **ความครบของวิดีโอ (กฎ S):** `ffprobe` → จำนวนเฟรมจริง เทียบ `duration × fps` · **รายงานเฟรมที่หายเป็นตัวเลข** · ถ้าหายเป็นช่วง ให้ระบุช่วงเวลาที่หาย
   🔴 **ข้อนี้บอกว่าไฟล์ครบแค่ไหน ไม่ได้บอกว่าในเฟรมมีอะไร**
7. 🔴 **ชั้นนี้ตอบไม่ได้:** จอเห็นอะไร · ตัวที่ `-8681` เป็นใคร · มี transient ไหม · **181 B พิสูจน์ว่า *ชื่ออยู่ในไบต์* ไม่ใช่ว่า *ชื่อเรนเดอร์***

**ชั้น (2) client-observable — ต้องมีคนหน้าจอ · ตัวปิดใบอยู่ชั้นนี้**
1. **ชุด PRE ครบแนว** พร้อม X/Y บน HUD อ่านได้ทุกใบ ⇒ ตอบข้อ (ก) เป็นสามทาง: **มี / ไม่มี / อยู่นอกเฟรม**
2. **`BASE_WIDE` (และ `BASE_MINUSX` ถ้าใช้)** + **วิดีโอต่อเนื่องกรอบเดิมตลอด +0 ถึง +90 วิ**
3. **การไล่ดูวิดีโอทีละเฟรมตลอดหน้าต่างสวีป** ⇒ ต่อ "ของที่เห็น" หนึ่งชิ้น ให้คำตัดสินหนึ่งใน **`NEW` / `ALREADY-IN-BASELINE` / `UNDECIDABLE`**
   🔴 **`UNDECIDABLE` = NO-RESULT ของชิ้นนั้น ห้ามนับเป็นผลลบ และห้ามนับเป็นผลบวก** · ถ้าเจอ `NEW` ให้ดึงเฟรมนั้นออกมาเป็นภาพ **full-res** พร้อมเวลา `t` ในวิดีโอ
4. **ภาพ POST ครบห้าจุด + ภาพ target panel ทุกครั้งที่คลิก/Tab** (พาเนลไม่ขึ้นก็ต้องมีภาพ และเขียนคำว่า "พาเนลไม่ขึ้น" ออกมาเป็นตัวอักษร)
5. **ตารางสีป้ายชื่อครบทุกป้ายทุกภาพ full-res** (ดูบล็อกข้อ 13)
6. **NO-CRASH verdict** จากคลิกขวาลาก
7. **ตอบคำถามข้อ clapper:** บรรทัดแชตที่พิมพ์ **ปรากฏ/ไม่ปรากฏ** บนหน้าต่างแชต · **เฟรมที่ช่อง input เคลียร์** อยู่ที่ `t` เท่าไรในวิดีโอ
8. 🔴 **ใบปิดด้วยผลลบได้เฉพาะรอบที่ *คุณ Panya เห็นเอง* + มีวิดีโอต่อเนื่อง** (`AGENTS.md` §9 — รอบ unattended ปิดผลลบไม่ได้)
9. 🔴 **ชั้นนี้ตอบไม่ได้:** เฟรมออกจากเซิร์ฟเวอร์จริงไหม · ไบต์ตรง pin ไหม

### 🔴 ผลลบมีค่าเท่าผลบวก — และเขียนไว้ล่วงหน้าว่ามัน redirect อะไร
- **ผลลบเต็มรูป** = ชายหนุ่มอยู่ในชุด PRE (เป็นของแมพ) **และ** ไม่มีชิ้นไหนได้คำตัดสิน `NEW` เลยตลอดวิดีโอ
  ⇒ **ผลเต็มใบ ไม่ใช่ FAIL** · มันทำสองอย่างที่สองรอบก่อนทำไม่ได้: (i) ยกขอบเขตผล no-render จาก *"persistent"* เป็น **"ไม่เรนเดอร์ในทุกชั่วขณะที่ยาวกว่าหนึ่งเฟรมที่ 30 fps"** (ii) **ปลดการพบเห็นที่ค้างมาตั้งแต่รอบ #12 ออกจากบัญชี**
  ⇒ **redirect:** คำถาม actor_type 2 ย้ายไปชั้น static ทั้งก้อน (mask bit ฝั่ง render · เส้น selection · ป้ายชื่อฝั่ง actor = `RE-068`) · 🔴 **และไม่ควรจองรอบ attended ของเลนนี้อีก จนกว่าจะมีผล static ที่ทำให้คำถามคมกว่าเดิม** (ข้อเสนอของใบ **ไม่ใช่คำสั่ง**)
- **ผลบวก** = มีชิ้นที่ได้คำตัดสิน `NEW` (ไม่ว่าจะอยู่กี่เฟรม) ⇒ **นี่คือการเรนเดอร์ actor_type 2 ครั้งแรกในประวัติโปรเจกต์**
  ⇒ **redirect:** chief ออกใบระบุตัว (พาเนล/ป้าย/ตำแหน่ง/สี) เป็นใบของตัวเอง · **ห้ามรวบขั้นระบุตัวเข้ามาในรอบนี้**
- **ผลผสม** = ชายหนุ่มไม่โผล่เลยทั้งรอบ (ไม่มีทั้ง PRE และ POST) ⇒ **ข้อ (ก) = NO-RESULT ของรอบนี้ ไม่ใช่ผลลบ** — การพบเห็นรอบ #12 **ยังค้างอยู่เหมือนเดิม ห้ามปิด**
- **NO-RESULT ทั้งใบ** = วิดีโอหายเป็นช่วงกินหน้าต่างสวีป หรือกรอบกล้องหลุดกลางสวีป ⇒ **ห้าม archive ใบ** จดสาเหตุกลับมา

### เกณฑ์หยุดทั้งเลนทันที (คงเดิม)
⛔ ชื่อ **`ProbeControl03`** โผล่ที่ไหนก็ตาม (ป้ายหรือพาเนล) = ข้ออ้าง bind-gate ของก้อน 1 ผิด — ทุกข้อสรุปก้อน 1 ต้องรื้อ · **หยุด เก็บ console ทั้งไฟล์**
⛔ server log มี `ErrorData=28317` ⇒ หยุด เก็บ console ทั้งไฟล์
🔴 **ไม่มีทาง despawn probe** — สามตัวค้างจนตัด connection · HP ของ probe = 100 ทุกตัว **ถ้าเห็นตัวไหน "ตาย" เอง = ผิดคาด จดละเอียด**

### 🆕⭐ ข้อ 13 — จดสีป้ายชื่อทุกป้ายในเฟรม (บังคับทุกใบ attended · คำสั่งคุณ Panya 2026-08-25 ~14:2x +07:00)
- **จดอะไร:** ชื่อตัวเอง (เหนือหัว + แผง UI ซ้ายบน) · ชื่อ actor ทุกตัวในเฟรม · ชื่อบนแผง target · ชื่อไอเทมบนพื้น · บรรทัด title/คำอธิบาย — **หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** · ไม่มีให้เขียนคำว่า **"ไม่มี"** ออกมาเป็นตัวอักษร 🔴 **ห้ามเว้นว่าง**
- **อ่านสีจากภาพนิ่งความละเอียดเต็มเท่านั้น** 🔴 **ห้ามอ่านจาก contact sheet · ห้ามจากภาพย่อ · ห้ามจากวิดีโอ**
  ⇒ เก็บ **full-res PNG** ที่ `evidence_screens\GT030R3_<TAG>_FULLRES_<yyyyMMdd_HHmmss>.png` **และ** สำเนา JPEG กว้าง <=1280 px <500 KB ไว้ใช้ทั่วไป · **sha256 ทุกไฟล์**
- **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับที่คุณ Panya เทียบมา:** NPC = **เหลือง** · ผู้เล่น = **เขียว** · ไอเทมบนพื้น = **ขาว** · title/คำอธิบาย = **ฟ้า** · ชื่อตัวเอง = **ขาว**
- ⭐ **ถ้าอะไรก็ตามโผล่ขึ้นมาในรอบนี้ ให้จดสีป้ายของมัน** — ป้ายของ actor ที่เซิร์ฟเวอร์ส่งเป็น **actor_type 2** ยังไม่เคยมีใครในโปรเจกต์เห็น
  🔴 **หน้าที่ของผู้เทสคือ "จดสี" อย่างเดียว** — **ห้ามเขียนว่าสีนั้นแปลว่าไคลเอนต์จัดมันเป็นผู้เล่น/NPC/ศัตรู** · อะไรตัดสินสี = คำถามของ `RE-067`/`RE-068` ไม่ใช่ของใบนี้
- **ลง `REAL_SERVER_DIVERGENCE.tsv` หนึ่งแถวต่อหนึ่งป้ายที่เทียบ** (คั่นด้วย **TAB** · อ่านหัวไฟล์ก่อนกรอก)
  `evidence_layer` = **`eye`** เสมอ · `evidence_ref` = path ภาพ full-res · `evidence_sha256` = คนละคอลัมน์ **ห้ามยัดรวม** · `open_ticket` = **`RE-067`** ตาม PLAYBOOK ข้อ 13 (🔴 ครึ่ง actor ตอนนี้อยู่ที่ `RE-068` — **ผู้เทสไม่เปลี่ยนคอลัมน์เอง**) · `blocks_promotion` = `no` · `compared_and_matched` = `yes`/`no`/`no-reference`
  🔴 **เติมแถวแม้ผลจะ "ตรงกัน"** — **"ไม่ได้จด" กับ "จดแล้วไม่ต่าง" คนละเรื่องกัน** · ไม่มีภาพต้นฉบับของป้ายชนิดนั้น ⇒ `real_server` = `(ยังไม่มีภาพอ้างอิงของเซิร์ฟเวอร์เดิมสำหรับข้อนี้)` **ห้ามเดา**
- `observation_note` = ข้อความที่อ่านได้ + ชื่อภาพที่ใช้ + ข้อสังเกต 🔴 **ห้ามเขียนสาเหตุหรือข้ออนุมานลงช่องนี้**

### 🧾 teardown + ใบเสร็จ (บังคับ — แม้รอบจะจบเพราะเลิกเล่น ไม่ใช่เพราะเทสจบ)
- **teardown เสมอ ภายใน 420 นาทีจาก boot stamp** (`staged\TEMPLATE_teardown_generic.ps1:135` · **เลข 180 ที่เห็นในใบเก่า ๆ = stale**) · เกินเพดาน template **ปฏิเสธ exit 12 โดยดีไซน์**
- แท่นที่ถูกทิ้งข้ามชั่วโมง: **อย่าฝืน template** ⇒ `staged\TOOL_stop_stale_server.ps1` แล้วตามด้วย receipt อ่านอย่างเดียว `staged\0949_gt027_stalepad_canonical_guard.ps1`
- **ใบเสร็จที่ต้องแนบมากับผล ทุกข้อ:** `AFTER listeners = 0` · **canonical guard: sha256 ก่อน-หลัง เท่ากับ `CANON_SHA.txt`** · **teardown exit code** · `LOCK_GAME` ปล่อยแล้ว · run copy `state\run_gt030r3.sqlite3` **เก็บไว้ให้ chief re-derive ห้ามทิ้ง** · path ของ raw GAME log + console out/err + วิดีโอ + ภาพทุกไฟล์ พร้อม **sha256**
- 🔴 **restart เซิร์ฟเวอร์ก่อนบูตรอบถัดไปเสมอ**

### nonclaims (ติดไปกับผลทุกกรณี ไม่ว่าบวกหรือลบ)
- ⭐ **เฟรม/mask/identity band/การวางตำแหน่ง ทั้งหมดเป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้ว ไม่เคยเผยแพร่ และกู้ไม่ได้ตลอดกาล** — ไม่มี capture ของ remote human player แม้แต่เฟรมเดียวในคลังทั้งโปรเจกต์
- **ไม่ claim ว่า mask bit ไหนของ ActorAttr จำเป็นต่อการเรนเดอร์**
- **ไม่ claim ว่า avatar ถูกยอมรับใต้ identity อื่น**
- **นี่ไม่ใช่ผู้เล่นสองคนจริง** (ก้อน 3 ยังไม่อนุมัติ)
- **ไม่ claim ว่า nameplate ลอยหัวมีอยู่สำหรับ actor_type 2** — ผู้บริโภคชื่อที่พิสูจน์ static ได้มีตัวเดียวคือ target panel ⇒ **"ไม่เห็นป้าย" ตัดสินอะไรไม่ได้**
- **ระยะเรนเดอร์ของ client = [UNKNOWN]** — ใบนี้ลดตัวแปรด้วยการยืนติด landmark **ไม่ใช่การวัดระยะ**
- **"ระบุตัวไม่ได้" ≠ "ไม่เรนเดอร์"** — สองประโยคนี้ห้ามใช้แทนกันในทุกผลของใบนี้
- **ยังไม่มีหลักฐาน static ว่า click/Tab targeting bind กับ actor_type 2 ได้เลย**
- 🆕 **ผล "อยู่มาก่อนแล้ว" ครอบเฉพาะแนวและกรอบกล้องที่ถ่ายจริง** — อะไรที่อยู่นอกเฟรม/นอกแนว = **non-observed ไม่ใช่ absent**
- 🆕 **ขอบล่างของ transient = ช่วงหนึ่งเฟรมของวิดีโอที่อัดจริง** (ที่ 30 fps ≈ 0.033 วิ) · **สั้นกว่านั้น = อยู่นอก claim** · ถ้า `ffprobe` พบเฟรมหาย **ขอบล่างคือช่องว่างที่วัดได้จริง ไม่ใช่ 1/fps**
- 🆕 **การระบุที่มา (attribution):** บูตนี้ติดอาวุธเลนเดียว แต่ **actor บนแมพเดินเข้าเฟรมเองได้** ⇒ ของที่ได้คำตัดสิน `NEW` **ไม่ถูกนับเป็นของเราโดยอัตโนมัติ** — จดว่ามันโผล่ที่ไหน เมื่อไร หน้าตาอย่างไร แล้วปล่อยให้ chief ตัดสิน
- 🆕 **สีอ่านด้วยตาจากภาพ ไม่ได้วัดค่าพิกเซล** ⇒ **ไม่ claim ค่า RGB/hex ใด ๆ** · `evidence_layer` ของทุกแถวที่ออกจากใบนี้คือ **`eye`**
- 🆕 **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับอาจเป็น client คนละ build หรือคนละภูมิภาค** ⇒ **"ต่างจากภาพต้นฉบับ" ยังไม่เท่ากับ "ของเราผิด"**
- 🆕 **ไม่ claim อะไรเลยเกี่ยวกับ offset นาฬิกาวิดีโอ↔สาย** — รอบนี้ *ทดสอบว่ามีเหตุการณ์บนจอให้จับหรือไม่* · **ห้ามอ้างตัวเลขข้ามสองนาฬิกาเมื่อขนาด error เทียบเท่าหรือใหญ่กว่าผลที่กำลังอ้าง** · การเทียบ **ลำดับ** ภายในวิดีโอไฟล์เดียวปลอดภัยเสมอ
- 🆕 **ไม่มีใครวัดว่าล้อเมาส์ (ขั้นซูมออก) ยิง `TargetPosVital` หรือไม่** — จึงบังคับให้จดเวลาที่ซูมทุกครั้ง
- **ground Z ที่จุด offset ไม่ได้ตรวจ — ตัวจม/ลอยพื้นไม่ falsify อะไร**
- **ไม่มี interest management / cadence / interpolation** (นั่นคือก้อน 3) · **ไม่มี second connection / broadcast**

- **result:** (ผู้เทสกรอก: ① `BOOT_COMMIT` + ผลเช็คหกข้อก่อนบูต ② ยอดรวมบรรทัด `[G>]` ทั้งไฟล์ + 5 label + ขนาด + เวลาที่ออก + `frame_sha256` ตรง pin ไหมทีละเฟรม ③ เวลาเฟรมแชต `0xAC52` และ `[G>]` แรก + ยืนยันว่าไม่มี label เลนนี้ก่อนแชต ④ คำตอบข้อ (ก) สามทาง **มี/ไม่มี/อยู่นอกเฟรม** พร้อมภาพ PRE ที่ใช้ตัดสิน ⑤ ตารางคำตัดสินต่อชิ้น `NEW`/`ALREADY-IN-BASELINE`/`UNDECIDABLE` พร้อม `t` ในวิดีโอ ⑥ ผล `ffprobe`: เฟรมจริง/เฟรมคาด/เฟรมหาย ⑦ ภาพ PRE1..n · `BASE_WIDE` (+`BASE_MINUSX`) · +0/+15/+30/+45/+60/+90 · POST ห้าจุด · target panel ทุกใบ — **full-res + JPEG + sha256 ทุกไฟล์** ⑧ **ตารางสีป้ายชื่อครบทุกป้ายทุกภาพ full-res** + เลขแถวที่เติมลง `REAL_SERVER_DIVERGENCE.tsv` **หรือคำว่า "ตรวจแล้ว ไม่มีความต่าง"** ⑨ คำตอบข้อ clapper: บรรทัดแชตปรากฏบนจอไหม + `t` ที่ช่อง input เคลียร์ ⑩ NO-CRASH/CRASH ⑪ เวลาที่ซูมทุกครั้ง ⑫ sha canonical ก่อน-หลัง · row-diff + `max(lease_generation)` ของ `run_gt030r3.sqlite3` · `integrity_check` ⑬ path raw GAME log + console out/err + วิดีโอ ⑭ **teardown exit code + `AFTER listeners`** ⑮ **คุณ Panya เห็นเองไหม** (ผลลบปิดได้เฉพาะเห็นเอง) · เวลาทุกจุดเป็น **+07:00**)

---

## GT-031 DAMAGE-HP-LINK-001: วงเต็ม "ตี → เลือด → ตาย" ครั้งแรก (ฝั่ง**ผู้เล่นเอง**)  [✅ **PASS — รอบใหญ่ #12 (2026-08-21 ~08:0x +07:00)**]

> ✅ **PASS ทั้งสองชั้น (chief R119 จดจากจดหมายผู้เทส `notes_to_chief\20260821_0840_GT031-PASS-GT030-PARTIAL.md`):**
> - **wire:** ครบ 8 เฟรมเรียงถูกลำดับ (`HP_BASELINE`…`DYING_ELAPSED` — ขนาดไบต์ตรงดีไซน์ทุกเฟรม)
> - **client:** หลอด HP ลดเป็น `37/100` **เฉพาะช่วงเฟรม `HP_AFTER_WEAK` (+30)** — ที่ ~21 วิ (หลัง `HIT_WEAK` +15)
>   หลอดยัง `100/100` ⇒ **การเชื่อมเป็นของเฟรม hp ไม่ใช่ของเฟรมเลข** (เกณฑ์หักล้างรอบ 83 **ไม่ทำงาน** — เรื่องดี)
> - จบชุด: `0/100` + ตัวละครนอนพื้น + หน้าต่าง `Common_Death` เปิด · ไม่กดปุ่มคืนชีพใด ๆ ตามข้อห้าม
> - teardown สะอาด: `AFTER listeners = 0` · `canonical guard OK: unchanged` · ภาพ: `outputs\screenshot-1787274365547-01eea183.jpg`
> - **nonclaims ที่ผู้เทสติดไว้ (คงไว้ทั้งหมด):** ไม่ได้สังเกตเลขลอย 63/379/MISS รอบนี้ · ไม่ได้สังเกตช่วง ~45–100 วิ
>   (MISS/HP_AFTER_MISS/HIT_STRONG — ถูกขัดจังหวะ) = "ไม่ได้สังเกต" ไม่ใช่ "ไม่เกิด" · สูตร/การเชื่อมเป็นดีไซน์ของเรา · ไม่ claim HP persist
> โปรโตคอลด้านล่างเก็บไว้เพื่อ re-run ในอนาคต (เช่น GT-038 ที่ใช้ HP baseline ตัวจริง)

[🟢 เดิม: PENDING — บล็อกรอบใหญ่ #11 โดยหน้าต่าง elevated (preflight guard จับได้แล้ว · รอบ #12 blockers = 0)]

> 🔴 **รอบใหญ่ #11 (2026-08-21 ~02:3x): บล็อกโดยหน้าต่าง `Administrator: Windows PowerShell` (elevated, always-on-top)**
> ที่ค้างอยู่กลางจอ · Windows ห้าม process ธรรมดาแตะหน้าต่าง elevated **ทุกช่องทาง** — ผู้เทสวัดครบทั้งสาม:
> คลิก = ไม่มีผล · `ShowWindow(SW_MINIMIZE)` = ไม่มีผล · `SetWindowPos` = **`False` `lastError=5` ACCESS DENIED**
> ย้าย**หน้าต่างเกม**หนีได้ (จ็อบ 955/956) แต่เกมยังไม่รับคลิก — คาดว่า foreground lock **แต่ยังไม่ได้พิสูจน์**
> ⇒ **ไม่ได้ยิงทริกเกอร์ ไม่ได้เข้าแมพ ⇒ ไม่มีผลใด ๆ ทั้งสิ้น** · เสียเวลาไป ~20 นาที
> ✅ **การ์ดใหม่ (chief รอบ 111): `staged\TEMPLATE_preflight_unattended.ps1`** — ลิสต์หน้าต่างที่มองเห็นทั้งหมด
> แล้ว **ABORT ทั้งรอบพร้อมบอกชื่อ ถ้าเจอหน้าต่าง elevated** (อ่านอย่างเดียว ไม่ย้าย ไม่ปิด ไม่ฆ่าอะไร)
> · "ตรวจไม่ได้ว่า elevated หรือไม่" ถูกนับเป็น **สิ่งที่ต้องรายงาน ไม่ใช่ผ่าน** (นั่นคืออาการปกติของ elevated)
> 🔴 **ข้อเสนอถึง Panya: ก่อนสั่งรอบ unattended ให้เหลือแต่หน้าต่างธรรมดาบนจอ** — ผู้เทสแก้เองไม่ได้จริง ๆ
> 🟢 **ตัวเทสเองไม่มีอะไรเปลี่ยน** — โปรโตคอลด้านล่างยังใช้ได้ทั้งหมด รันได้ทันทีที่จอว่าง
> 💡 **บริบทใหม่:** GT-039 (ฝั่งเป้าหมาย) PASS ไปแล้ว ⇒ ใบนี้ตอบคำถามที่เหลือคือ **ฝั่งผู้เล่นเอง**

[🟢 เดิมเป็น PENDING — พร้อมรันหลัง commit ของ chief รอบ 97 (`af10536` · HYP-PF-026)**]

**ที่มา:** GT-024 พิสูจน์ว่าเลขความเสียหายเรนเดอร์บนจอ **แต่ HP ไม่ลด (ยืนยันสองปาก)** · GT-019 พิสูจน์ว่า hp 0 + timer เปิดหน้าต่างตาย · **สองข้อเท็จจริงนี้ไม่เคยแตะกันเลย — เลนนี้คือชิ้นกลางที่เชื่อม**: เซิร์ฟเวอร์ทำเลขคณิต HP เอง (100 − 63 = 37 → clamp 0) แล้วส่งทั้ง "เลขลอย" และ "หลอดเลือด" สลับกัน 8 เฟรม
⭐ **nonclaim ที่ต้องติดทุกผล: สูตรและการเชื่อมเป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** (รอบ 83 พิสูจน์แล้วว่า client ไม่ลบเลขเอง — นั่นคือเหตุที่ server ต้องพูดทั้งสองครึ่งเอง)

**boot (ท่าเดียวกับ GT-024/027/030 เป๊ะ เปลี่ยนแค่ flag):**
- `--damage-hp-link-hypothesis-scenario scenarios\damage_hp_link_hypothesis_link_sweep.json` (+ `--db` สำเนาตามปกติ)
- trigger เดิม: แชต **ascii 12 ตัวเป๊ะ** → sweep **8 เฟรม ห่างกัน 15 วิ/เฟรม** (105 วิทั้งชุด — เผื่อถ่ายทุกเฟรม)
- console label = `HYP_PF_026_HP_LINK_<STEP>` · event = `damage_hp_link_hypothesis_link_sweep_sent` — เห็นชื่ออื่น = บูตผิดไฟล์
- **one-shot** — ยิงซ้ำได้ `..._already_sent_no_reply` · 🔴 **เลนนี้ยิงได้เฉพาะตัวละคร canonical (identity `0x10010001`)** — ถ้าเผลอสร้าง/เลือกตัวอื่นจะได้ `..._identity_not_pinned_no_reply` และไม่มีไบต์ออกเลย (ตั้งใจ: ผู้เทสต้องเห็นไบต์ตรง pin เป๊ะหรือไม่เห็นเลย)
- ก่อนยิง: ถ่าย baseline หลอด HP (ควรเป็น 100/100) + เปิดมุมกล้องเห็นทั้งตัวละครและหลอด

**สิ่งที่ควรเห็นทีละเฟรม (คำทำนาย — ไม่ใช่ข้อเท็จจริง):**
| t | เฟรม | ถ่ายอะไร |
|---|---|---|
| +0s | `HP_BASELINE` — ActorAttr hp 100/100 | หลอดยัง 100/100 (ถ้ากระพริบ/รีเฟรชให้จด) |
| +15s | `HIT_WEAK` — เลข **63** flags 0x0001 | เลขลอยบนตัวผู้เล่น (เหมือน GT-024) · **หลอดต้องยังไม่ขยับ** — ถ้าหลอดลดที่เฟรมนี้ = หักล้างรอบ 83 ทั้งเลน จดละเอียดสุด |
| +30s | `HP_AFTER_WEAK` — hp_current **37** | ⭐ **หลอดลดเหลือ 37/100 ไหม — นี่คือคำถามหลักของเทสทั้งใบ** |
| +45s | `MISS` — คำว่า MISS flags 0x0000 | MISS ขึ้น (เหมือน GT-024) · หลอดค้าง 37 |
| +60s | `HP_AFTER_MISS` — hp_current 37 ซ้ำ (ไบต์เหมือนเฟรม +30 เป๊ะ) | หลอดค้าง 37 · client กระพริบ/รีเฟรชไหมเมื่อได้ค่าที่ถืออยู่แล้ว (มีค่าทั้งสองทาง) |
| +75s | `HIT_STRONG` — เลข **379** flags 0x0001 | เลขลอย · หลอดยังไม่ขยับ |
| +90s | `HP_ZERO_DYING` — hp 0 + death timer 20.0 **ในเฟรมเดียว** | หลอด 0/100 + **ท่าคุกเข่า + ปุ่ม "ล้มเลิกการช่วยเหลือ"** (เหมือน GT-019) — clamp: 37−379 = floor 0 |
| +105s | `DYING_ELAPSED` — timer 0.0 | **`Main_Dead` ปิด → `Common_Death` เปิด** ("ท่านตายแล้ว…" เหมือน GT-023) · **ห้ามกดปุ่มใด ๆ ในหน้าต่างตาย** (เลนนี้ไม่มี path คืนชีพ — จบเทสด้วย End task ตาม PLAYBOOK) |

**pass criteria สองชั้น:** ① wire = 8 เฟรมครบตาม label+delay (console) ② client = ตอบอย่างน้อย 3 ข้อ: หลอดลดเป็น 37 ที่เฟรม +30 หรือไม่ · หลอดขยับตอนเฟรมเลข (+15/+75) หรือไม่ · หน้าต่างตายเปิดที่ +90/+105 เหมือนตอนเทสแยกไหม — **ผลลบก็มีค่า** (เลขขึ้นแต่หลอดไม่ลด = ตอบคำถาม link เป็นลบ จดเป็นผล ไม่ใช่ fail)
**เกณฑ์หยุด/ตื่นเต้นพิเศษ:** ⛔ หลอดลด**ก่อน**เฟรม hp (คือลดตอนเฟรมเลข) = หักล้าง "client ไม่ลบเอง" ของรอบ 83 — ผลลบที่มีค่าที่สุดที่เป็นไปได้ ถ่ายวิดีโอ/ภาพต่อเนื่องช่วง +15..+30 ไว้ให้มากที่สุด · `ErrorData=28317` ใน log = การสลับ carrier ในเซสชันเดียวพัง หยุดและจด
🔴 หลังหน้าต่าง Common_Death เปิด: ถ่ายภาพแล้ว **End task** ปิด client (ห้ามกด "กลับจุดเกิด"/"คืนชีพที่เดิม" — พฤติกรรมปุ่มพวกนั้นยังไม่มี server path และไม่ใช่คำถามของเทสนี้) · teardown ตามปกติ · run copy ทิ้งได้
**nonclaims บังคับ:** สูตร/การเชื่อมเป็นของเรา · ไม่ claim ว่า HP persist (ไม่มีคอลัมน์ HP ใน DB — balance ตายพร้อม sweep) · ไม่ claim path คืนชีพ · ไม่ใช่ combat จริง (ไม่มี NPC โจมตี — น่ันคือแถว mob_aggro ที่ยัง not_started)

## GT-032 NPC-HOSTILE-001: NPC ตัวแรกของ Port Royal "ขึ้นศัตรู (แดง)" ไหม — Door A ของ mob-aggro  [✅ **PASS — รอบใหญ่ #12 ต่อ (2026-08-21 ~09:00 +07:00 · จ็อบ 966/967) · ผลเต็มบริโภคโดย chief R120**]

> ✅ **ผล (chief R120 บริโภคจาก `notes_to_chief/20260821_0900_GT032-PASS-GT033-BLOCKED-input.md`):**
> wire = 1 เฟรม `HYP_PF_027_NPC_HOSTILE_HOSTILE_SPAWN` (190 bytes · late 0.5ms · ไม่มี refusal) ·
> client = NPC `0x2001` กด Tab เลือกเป็นศัตรูได้จริง — **แถบเป้าหมายสีแดง `HP 100/100 Lv.1` + ไอคอนศัตรู** ·
> ไม่มีป้ายชื่อแดง (ตรงคำทำนาย — เฟรมนี้ไม่มี name bit) · ภาพ `outputs\screenshot-1787276810199-d317fb3d.jpg`
> 🔴 **แก้เกณฑ์ที่ chief เขียนผิดเอง (สืบโดย R120):** ข้อ "ควรเห็น event `..._start_game_sent` ใน console" **สังเกตไม่ได้โดยโครงสร้าง**
> — `self.events` เป็น list ในหน่วยความจำ ไม่มีบรรทัดไหนใน src/ พิมพ์มันออก console (ตัวพิมพ์เดียวคือ `[G>] label (N bytes)`
> ที่ `current/pf_login_game_server_v141.py:7762` ซึ่งพิมพ์เฉพาะเฟรมขาออก) ⇒ การ grep ไม่เจอของผู้เทส = พฤติกรรมปกติ ไม่ใช่ความผิดปกติ
> ✅ **pairing ครบทั้งสองข้างพิสูจน์ทางอ้อมได้แน่น:** dispatch มี guard `runtime.py` — ถ้า faction-1 StartGame ไม่ถูกส่ง
> จะปฏิเสธ `npc_hostile_hypothesis_player_faction_not_applied_no_reply` และไม่มีไบต์ออก ⇒ **การที่ HOSTILE_SPAWN ออกไปได้เลย = faction-1 ลงแล้วจริง**
> (ทางเลือก (ค) ของผู้เทส "hostility ไม่ต้องพึ่ง player faction" ตกไปด้วย arena-v2 อยู่แล้ว: NPC 6 เดี่ยว vs player faction 0 = เป็นกลาง 1,023 ครั้ง)
> 🟡 **ค้างหนึ่งข้อ (ยกเป็นเกณฑ์แถมของรอบใหญ่หน้า ไม่เปิดใบใหม่):** แยกไม่ออกว่า "เส้นขอบแดงรอบตัว" เป็นผลของ hostility
> หรือของการเลือกเป้า — ผู้เทสถ่ายก่อน Tab (ไม่มีขอบ) กับหลัง Tab (มีขอบ) ⇒ ครั้งหน้าถ้าแวะเลนนี้ **ถ่ายหลังยิงแต่ก่อนกด Tab** หนึ่งภาพ

**ที่มา:** ดราฟต์ mob-aggro รอบ 98 แยกการสู้เป็นสามประตู — **hostility · attack · hit-lands** — และมีแค่ประตู hostility (Door A) กับ hit-lands ที่พิสูจน์บนสายแล้ว · SCENE-005 เคยทำ **ชื่อแดง + เส้นขอบแดง + แผง target แดง** บนจอจริง โดยจับคู่ faction: **ผู้เล่น 1 vs NPC 6** · แต่ arena-v2 พิสูจน์ว่า **NPC 6 เดี่ยว ๆ กับผู้เล่น faction 0 (ค่าคอนสตรัคเตอร์) = เป็นกลาง** (นับ 1,023 ครั้ง) ⇒ ต้องส่งสองข้าง เลนนี้ทำครบสองข้าง แล้วยิง NPC `0x2001` ตัวเดิมที่ GT-022/025 ทำให้ตาย
⭐ **nonclaim ที่ต้องติดทุกผล: faction 1 และ 6 เป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** · เลนนี้พิสูจน์ hostility เท่านั้น — **ยังไม่มี NPC โจมตี** (Door B ยังปิด)

**boot (ท่าเดียวกับ GT-024/027/030/031 เป๊ะ เปลี่ยนแค่ flag):**
- `--npc-hostile-hypothesis-scenario scenarios\npc_hostile_hypothesis_faction_pairing.json` (+ `--db` สำเนาตามปกติ)
- 🔴 **เลนนี้ผูกกับ identity `0x10010001` (ตัวละคร canonical smoke) — ตัว StartGame จะได้ faction 1 ต่อเมื่อเป็นตัวนี้เท่านั้น** ถ้าเผลอเลือก/สร้างตัวอื่นจะได้ StartGame ปกติ (ไม่มี faction) แล้ว sweep จะปฏิเสธ `..._player_faction_not_applied_no_reply` — ไม่มีไบต์ออก (ตั้งใจ: เห็นคู่ครบหรือไม่เห็นเลย)
- trigger เดิม: แชต **ascii 12 ตัวเป๊ะ** → **sweep 1 เฟรมเดียว** (`HOSTILE_SPAWN`)
- console label = `HYP_PF_027_NPC_HOSTILE_HOSTILE_SPAWN` · event = `npc_hostile_hypothesis_faction_pairing_sent` — เห็นชื่ออื่น = บูตผิดไฟล์ · **one-shot** (ยิงซ้ำ `..._already_sent_no_reply`)
- ⚠️ ตอน StartGame ควรเห็น event `npc_hostile_hypothesis_player_faction1_start_game_sent` ใน console **ก่อน** ยิง — ยืนยันว่าครึ่ง entry ลงแล้ว
- ก่อนยิง: เดินให้ NPC `0x2001` (ตัวแรกของ Port Royal ใกล้จุดเกิด — XYZ อยู่ในเฟรม SPAWN) อยู่ในเฟรมกล้อง เห็นทั้งชื่อ/ตัว NPC
- 🔴 **โน้ตข้ามใบ (chief R119):** `0x2001` = NPC **'Navy Transfer'** = **landmark ของ GT-030 rerun** ⇒
  **ในรอบใหญ่เดียวกัน รัน GT-030 ให้จบก่อนใบนี้เสมอ** — ใบนี้ทำให้ landmark ขึ้นศัตรู ใช้เป็นจุดอ้างอิงกลาง ๆ ต่อไม่ได้

**สิ่งที่ควรเห็น (คำทำนาย — ไม่ใช่ข้อเท็จจริง):**
- **หลังยิง 1 เฟรม:** NPC `0x2001` เปลี่ยนเป็น **ขึ้นศัตรู** — เส้นขอบแดง · กด Tab เลือกแล้วได้ **ลูกศร/แผง target สีแดง** เหมือนตอน SCENE-005 ทำกับ NPC `0x203D`
- 🔴 **ไม่มีป้ายชื่อแดง** — เฟรมนี้ **ไม่มี name bit** (ต่างจาก SCENE-005 ที่เป็น scene-load) ⇒ สิ่งที่ดูคือ **เส้นขอบ + แผง Tab target** ไม่ใช่ป้ายชื่อ
- **ผลลบมีค่าเท่าผลบวก:** ถ้า NPC **ไม่ขึ้นแดง** (แต่ SCENE-005 แบบ scene-load ยังทำได้) ⇒ faction บิตตอน spawn บนท่อ actor-entry **ไปไม่ถึง relation read** — เป็นคำตอบที่ redirect Door A ทั้งประตู จดละเอียด

**pass criteria สองชั้น:** ① wire = 1 เฟรม `HOSTILE_SPAWN` + StartGame มี faction-1 (console: สอง event ข้างบน) ② client = NPC `0x2001` ขึ้นศัตรู (เส้นขอบ/แผง Tab แดง) หรือไม่ — **ตอบ yes/no พร้อมภาพ** · ถ้า Tab แล้วเลือกไม่ได้/ไม่มีแผงแดง = ผลลบ (จดเป็นผล)
🔴 **จบเทส:** ถ่ายภาพแล้ว **End task** (เลนนี้ไม่แตะ DB · ไม่มี path ใด ๆ ให้กด) · run copy ทิ้งได้ · teardown ตามปกติ
**nonclaims บังคับ:** faction 1/6 เป็นของเรา · ไม่ claim ว่าคู่ (1,6) ทำงานบน NPC ที่ project ผ่าน actor-entry เหมือนตอน scene-load (นั่นคือสิ่งที่เทสนี้วัด) · ไม่มี aggro/threat/chase/attack · ไม่มี persistence (faction ไม่มี write path)

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


## 🆕🔬 GT-042 DROPTHING-REDERIVE-001 [STATIC-ON-BRIDGE]: ตรวจซ้ำแบบ "ปฏิปักษ์" ผลสามท่อน A/B/C ของ GT-040 + ปิดชิ้นที่ขาดชิ้นเดียว (`0x402A20`)  [✅ **PASS — 2026-08-23 02:03 (+07:00) หลัง adversarial re-derive · มี erratum ขอบเขต handler หนึ่งจุด · แถว semantic รอดทั้งหมด**]

> ✅ **RESULT 2026-08-23 01:54–02:03 (+07:00) — PASS พร้อม erratum** (อิมเมจ SHA ก่อน/หลังทุกจ็อบตรง `9627211412ac…8b623` · read-only):
> - แถว semantic ของ GT-040 A/B/C **รอดทั้งหมด**: ตารางฟิลด์สอง sub-serializer (`0x5E2960` bit 0x04 · `0x5F85B0` bit 0x08) · generation-stamp reconcile (`0x446F30`/`0x441C40`) · gate bit `0x02` · vtable/serializer/handler ของ `PickupTerrainThing`
> - 🔴 **ERRATUM ต้องพกไปทุกที่ที่อ้าง:** span เดิม `[0x005EF640,0x005EF908)` len 712 "hash ตรงแต่ป้ายผิด" — **ไม่ใช่** handler ฟังก์ชันเดียว · handler จริง = `[0x005EF640,0x005EF66F)` len 47 SHA `5d17fc4…8d602e` (อ่าน `+0x18` แยก FC/FD/FE → message 1F/03/22)
> - ชิ้นที่ขาดปิดแล้ว: `0x402A20` **ไม่อ่าน argument** — one-time init คืน singleton `0x0102C6C0` · **`[mgr+0x24]` = ordered registry ของ network actor objects (actor_type 2..6) ที่ singleton นี้ลงทะเบียน — subset ของ runtime actors ไม่ใช่ collection เฟรมล่าสุด และไม่ใช่ scene-load population ทั้งหมด** · สมมติฐาน `[esi+0x1C]+0x10` เป็นตัวเลือก manager = ตาย
> - ⭐ **คำสั่งปลดล็อกของ GT-040 มีผล:** ใบนี้ปิด ⇒ ข้อห้าม "เขียนโมดูล/encoder จาก span GT-040" **ปลดเฉพาะแถวที่รอด/ขอบเขตที่แก้แล้ว** (การเขียนจริงยังต้องเดินตาม pattern มาตรฐาน: opt-in · production_allowed=false · fail closed · ledger/verifier/matrix · headless proof)
> - ผลเต็ม + artifact 9 ใบใน `pf_bridge/outbox/`: `notes_to_chief/20260823_0203_GT042-REDERIVE-PASS-WITH-HANDLER-SPAN-ERRATUM.md` (บริโภค R123)

**หมวด:** `STATIC-ON-BRIDGE` — ต้องเปิด `GameClient.local.bin` จึงทำบน cloud clone ไม่ได้เลย
ผู้รับงานคือคนที่นั่งอยู่หน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม · **ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว** (ดู "ชั้น ②")

**ที่มา:** GT-040 ปิดครบสามท่อนโดยเซสชันผู้ช่วยของ Panya (2026-08-21 09:36-09:56 +07:00)
จดหมายผลสามฉบับประกาศเงื่อนไขของตัวเองไว้ชัด: **(ก) ไม่มี subagent ตัวไหนเดินซ้ำผลเลย**
**(ข) ผลทั้งหมดเป็นชั้น wire/static ล้วน** **(ค) ห้ามเขียนโมดูล/encoder จาก span พวกนี้จนกว่าจะมีคนตรวจซ้ำ**
ทุกข้ออ้างในสามใบแนบ **span VA + file offset + len + sha256** ไว้ให้เดินซ้ำเอง ⇒ ใบนี้คือการเดินซ้ำนั้น
🔴 **ท่าคือ "พยายามหักล้าง ไม่ใช่พยายามยืนยัน"** — ถ้าเดินตามรอยเดิมเพื่อจะเห็นสิ่งเดียวกัน จะมองข้ามจุดที่ผิดเสมอ

### objective (claim เดียวที่ใบนี้พิสูจน์)
**ผลสามท่อนของ GT-040 ตรวจซ้ำแบบปฏิปักษ์บนอิมเมจแล้ว "รอด" หรือ "ตาย" แถวไหนบ้าง** —
และปิดชิ้นที่ขาดชิ้นเดียวที่ท่อน B ระบุ (`0x402A20` -> ขอบเขตของ `[mgr+0x24]`) เพื่อดัน TENSION ไป 100%
🔴 **ทุกแถวที่ "ตาย" (ปฏิปักษ์หักล้างได้) มีค่าเท่าหรือมากกว่าทุกแถวที่ "รอด"** — จดเป็นผล ไม่ใช่ fail

### db
**ไม่ใช้ DB เลย** — ไม่แตะ canonical ไม่ทำสำเนา ไม่มีรอบเทสในเกม (กติกา stamp 420 นาที/teardown ไม่เกี่ยวกับใบนี้)

### server args
**ไม่มี** — ไม่บูตเซิร์ฟเวอร์ ไม่บูต client · เปิดอ่านอิมเมจอย่างเดียว

### สิ่งที่ต้องมี (precondition)
- **อิมเมจ:** `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · PE32 · ImageBase `0x00400000`
  🔴 **จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง เปิดอ่านอย่างเดียวเสมอ**
- **ไม่ต้องมี:** เซิร์ฟเวอร์ · client ที่บูตแล้ว · canonical DB · สำเนา DB · `LOCK_GAME` · teardown · boot stamp
- **ท่าทำงาน:** ตามวินัย `pf-static-re` · 🔴 **ห้ามใช้ linear disassembler เป็นหลักฐานของ negative**
  (มันหยุดที่ไบต์แรกที่ decode ไม่ได้แล้วรายงาน negative อย่างมั่นใจ = ความผิดพลาดรอบ 83) · census ด้วย byte matching
  (`E8`/`E9 rel32` ทุกออฟเซ็ต · dword sweep ทั้งไฟล์สำหรับ table/vtable/immediate) · สวีปทั้งสอง exec section:
  `.text` (`0x00401000`, Vsize `0x00838A2C`) และ `.code` (`0x00C3A000`, Vsize เพียง `0x2E1` ไบต์)

### 🔴 กติกาข้อแรก — verify sha ของ span **ก่อน** re-derive
สำหรับทุกฟังก์ชันข้างล่าง: ตัดไบต์ตาม file offset ที่บันทึกไว้ แล้ว sha256 เทียบกับค่าที่จดหมายให้มา **ก่อน** เริ่ม decode
- **sha ของ span ตรง** ⇒ เดินซ้ำ decode บนไบต์ชุดนั้นได้
- 🔴 **sha ไม่ตรงแม้ตัวเดียว = หยุดทันที รายงานว่า span ไหนเพี้ยน ห้าม re-derive ทับ** (span เพี้ยน = ฐานผิด ทุกอย่างที่ต่อยอดไร้ค่า)

### span ที่ต้องตรวจ (จาก GT-040 A/B/C — จดหมายอยู่บน `main` แล้ว ผู้เทส push ผ่าน sync ก่อนรอบ R120:
`notes_to_chief\20260821_09{36,51,56}_GT040-PART-{A,B,C}-RESULTS-from-assistant.md`)

| ฟังก์ชัน | บทบาท | span VA `[start,end)` | file offset | len | sha256 ที่ต้องเจอ |
|---|---|---|---|---|---|
| `0x005E2960` | tag table บิต `0x04` / obj `+0x24` | `[0x005E2960,0x005E2AF6)` | `[0x1E1D60,0x1E1EF6)` | 406 | `259e551604b81fece3659d38f74be5f5a9148cbf44c9cc7d74c2301c995d8acc` |
| `0x005F85B0` | dirty-mask table บิต `0x08` / obj `+0x20` | `[0x005F85B0,0x005F8869)` | `[0x1F79B0,0x1F7C69)` | 697 | `ce0a58f72c5798f1d5263ebdb5ee449659ed04e2974f63f77657ea968a4f1b5b` |
| `0x00446F30` | generation-stamp reconcile (ลูป1+ลูป2) | `[0x00446F30,0x004470DE)` | `[0x046330,0x0464DE)` | 430 | `9c1157d3109c27c41783d6eed630a6eb46511ef6789a4e121306944ec1271d7d` |
| `0x005E5E30` | serializer ของ `PickupTerrainThing` (vtable `0x00F3005C` slot `+0x18`) | `[0x005E5E30,0x005E5E83)` | `[0x1E5230,0x1E5283)` | 83 | `8e439d4f3ff1479e723b220d8dd78a262b41df3b74839da9d4cb728f69773066` |
| `0x005EF640` | handler สองทาง (slot `+0x1C`) | `[0x005EF640,0x005EF908)` | `[0x1EEA40,0x1EED08)` | 712 | `22da3ff4c2bcf8f7a006fab20d48f6ed5102617954cad3c68305c82480726c83` |

**span สนับสนุน (ตรวจ sha ด้วยถ้าจะพึ่ง):** `0x005F3490` (3 float · sha `b5f5a2063ff9...`) · `0x005E2630`/`0x005F82C0` (pool alloc)
· `0x00441C40` (removal จริง · sha `f7b9b6afd070...`) · `0x005E4060` (inbound handler · sha `85ff71ffceff...`)
· `0x0088F2B0` (`IsKindOf` comparator · sha `00076eb0d61b...`) · `0x005E46A0` (GetId · sha `d3fc621e95d5...`)
· `0x00BEE5E0` (registration · sha `8fa9ec1ebc0b...`)

### steps — สี่จ็อบ แยกผล อย่ารวม (ทำตามลำดับ 1 -> 2 -> 3 -> 4)

**จ็อบ 1 (แกน) — หักล้างตารางฟิลด์ของ `0x5E2960` และ `0x5F85B0`**
1. verify sha ของทั้งสอง span ก่อน (กติกาข้อแรก)
2. decode ใหม่จากศูนย์ **โดยไม่เปิดตารางเดิม** แล้วค่อยเทียบ · ต้องยืนยัน/หักล้างทุกแถว:
   - `0x5E2960`: หัว 4 แถว (`0x14`->`+0x10`/4 · `0x0B`->`+0x14`/1 · `0x0B`->`+0x18`/1 · `0x12`=จำนวนสมาชิก/2)
     + ลูปสมาชิก (`0x0B`->`elem+0x10`/1 · `0x2A`->`elem+0x14`/4) · ขนาดสมาชิก `0x18` จาก `push 0x18` ใน `0x5E2630`
   - `0x5F85B0`: หัว (`0x12`=`[obj+0x2C]`/2) + ต่อสมาชิก (`0x14`->`+0x10` เสมอ · `0x0B`->`+0x28`=mask เสมอ ·
     mask`0x02`->`0x14`/`+0x14` · mask`0x04`->`0x0F`/`+0x18` · mask`0x08`->`0x05`/`+0x1B` ·
     mask`0x10`->`0x2A`x3/`+0x1C,+0x20,+0x24` · mask`0x20`->`0x08`/`+0x1A`) · ขนาดสมาชิก `0x2C` จาก `push 0x2C` ใน `0x5F82C0`
3. หักล้างข้ออ้างสำคัญของท่อน A ให้ตรง: **bit `0x08`/`+0x20` พา record ที่มีพิกัดโลก (สาม float ที่ `+0x1C`) ที่ไม่ใช่ actor type 2..6**
   — ตรวจว่า record นี้ **ไม่** ผ่าน jump table `0x4469BD` และ **ไม่** อ้าง literal `0x00F3093C`/`0x00F0BAD0`
   (จดหมาย A ยืนยัน census `E8/E9` ในสองฟังก์ชันไม่แตะ terrain/ground เลย — เดินซ้ำเอง)

**จ็อบ 2 — หักล้าง generation-stamp reconcile ของ `0x446F30` (Part B)**
4. verify sha แล้ว decode ลูป1/ลูป2 ใหม่ · ยืนยัน/หักล้าง: `inc [mgr+0x04]` ที่ `0x446F37` ·
   ประทับ `[obj+0xD0]=[mgr+0x04]` ที่ `0x446FBE` · ลูป2 เก็บตัวที่ประทับแล้วหรือ `IsKindOf` ผ่าน · ที่เหลือเรียก `0x441C40` ถอดจริง
5. 🔴 **หักล้างข้ออ้างเชิงลบของจดหมาย B โดยตรง** (ข้ออ้างเชิงลบหักล้างง่ายที่สุดถ้ามันผิด): dword sweep เฉพาะช่วง
   `[0x046330,0x0464DE)` หา `0x01081A90` และ `0x01093198` — จดหมายอ้างว่า **0/0** (คือไม่ diff กับสำเนาเฟรมก่อนของ CHUNK2-Q2)
   ถ้าเจอแม้ครั้งเดียว = **ข่าวใหญ่ จดทันที** (พลิกคำวินิจฉัย TENSION)
6. ยืนยัน census ผู้เรียก: `0x446F30` ถูกเรียกจุดเดียว `0x5E4085` · `0x441C40` ถูกเรียกจุดเดียว `0x4470B2`
   (สแกน `E8/E9 rel32` ทั้ง `.text` เอง — ถ้าเจอผู้เรียกตัวที่สอง gate ที่คิดว่าปิดอาจไม่ปิด)

**จ็อบ 3 (ชิ้นที่ขาด — ดัน TENSION ไป 100%) — decode `0x402A20`**
7. `0x402A20` คือฟังก์ชันที่ค่า return กลายเป็น `mgr` (`ecx`) ของ `0x446F30` — เรียกที่ `0x5E407E` โดยอาร์กิวเมนต์ = `[esi+0x1C]+0x10`
   (sub-object ของ derived bit `0x02`) · จดหมาย B เตือนว่า **มี SEH ไม่ใช่ getter สั้น ๆ** จึงยังไม่มีใครเปิด
8. ตอบคำถามเดียวของจ็อบนี้: **`[mgr+0x24]` (ลิสต์ที่ลูป2 กวาด) ครอบคลุมประชากรอะไร** —
   scene-load population ทั้งหมด · หรือเฉพาะ actor-entry ของเฟรมล่าสุด · หรือ subset อื่น
   นี่คือชิ้นเดียวที่กั้นไม่ให้ปิด TENSION 100% และเป็นตัวตัดสินความเป็นไปได้ (ข) ของ GT-043 ล่วงหน้า
9. แนบ span `[start,end)` + file offset + len + sha256 ของ `0x402A20` (และทุกฟังก์ชันใหม่ที่อ้าง) แบบเดียวกับจดหมายเดิม

**จ็อบ 4 (ของแถมถ้าเหลือเวลา) — สามบิตที่ว่าง `0x01`/`0x40`/`0x80` ของ mask ใน `0x5F85B0`**
10. จดหมาย A อ้างว่าสามบิตนี้ **ไม่เคยถูก test เลยทั้งขาเขียนขาอ่านในฟังก์ชันนี้** · ตรวจว่า **ที่อื่นในอิมเมจ**
    มีจุดไหน test บิตเหล่านี้ของ byte `[member+0x28]` หรือไม่ (ถ้ามี ⇒ mask มีความหมายมากกว่าที่ decode ในฟังก์ชันเดียว — จด)
    🔴 ถ้าเวลาไม่พอ **ข้ามจ็อบนี้ได้ ไม่กระทบการปิดใบ** — จ็อบ 1-3 คือแกน

### pass criteria — **สองชั้น แยกกันเด็ดขาด**

**ชั้น ① wire/DB (ไบต์+ดิสแอสเซมบลี — headless ล้วน ไม่ต้องมีคนเฝ้าจอ)**
ใบนี้ผ่านเมื่อครบทั้งสองส่วนนี้:
- **(layer 1a — ราย row) ทุกแถวของสามตารางแกน** (`0x5E2960` · `0x5F85B0` · `0x446F30`) และตารางฟิลด์ของ `0x5E5E30`
  ถูก **ยืนยันหรือหักล้างทีละแถวด้วยหลักฐานไบต์ที่ file offset ที่บันทึกไว้** — ไม่ใช่ "อ่านผ่านแล้วเหมือนเดิม"
  ต้องเห็น sha ของทุก span (verify ก่อน) และไบต์จริงของแถวที่ตัดสิน
- **(layer 1b — บัญชีรอด/ตาย) รายการชัดเจนสองคอลัมน์:** ข้ออ้างของ GT-040 **ตัวไหนรอดการตรวจปฏิปักษ์ · ตัวไหนตาย**
  โดยเฉพาะสี่ข้ออ้างเสาหลัก: (i) bit `0x08` พา record มีพิกัดที่ไม่ใช่ actor · (ii) reconcile ใช้ generation stamp ไม่ diff สำเนา
  (ข้ออ้างเชิงลบ `0x01081A90`/`0x01093198` = 0/0) · (iii) เฟรม count-1 กวาดจริงแต่มี gate ที่ `[res+0x1C]` (`0x5E4078 je`) ·
  (iv) vtable `0x00F3005C` -> serializer `0x5E5E30` / handler สองทาง `0x5EF640`
- **จ็อบ 3 ต้องตอบเป็นประโยคเดียวได้:** `[mgr+0x24]` ครอบคลุม `<...>` พร้อม span+sha ของ `0x402A20`
  **ถ้า static ตัดสินขอบเขตนี้ไม่ได้** (เช่นจบที่ lookup รันไทม์อย่างที่ descriptor `0x0102CB04` เป็น) ⇒ **พูดตรง ๆ ว่าตัดสินไม่ได้**
  และระบุว่าเหลือทางเดียวคือ GT-043 (attended) — **นั่นคือผลที่สมบูรณ์ ไม่ใช่ fail**
- ทุกจ็อบ: **sha256 ของอิมเมจก่อน-หลัง ต้องตรงกัน** · ถ้าเขียนสคริปต์ commit ลง `tools/` แบบรันซ้ำได้พร้อม guard count + exit 0

**ชั้น ② client-observable (ต้องมีคนอยู่หน้าจอเกม)**
🔴 **ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้แม้แต่ชิ้นเดียว และห้ามใครอ้างชั้น ① เป็นหลักฐานของชั้น ②**
ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย · ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย**
**สิ่งที่ผลบวกจะไปปลดล็อก (ยังไม่ใช่ตอนนี้):** เมื่อสามท่อนรอดการตรวจ ⇒ ปลดล็อก **สิทธิ์เขียนโมดูล/encoder** (ก่อนหน้านี้ห้าม)
และจ็อบ 3 ป้อนคำตอบขอบเขต `[mgr+0x24]` ให้ GT-043 ตีความผลบนจอได้

### 🔴 ผลลบมีค่าเท่าผลบวก — เขียนไว้ล่วงหน้า
- **ถ้าทุกแถวรอด** ⇒ GT-040 ผ่านการตรวจปฏิปักษ์ · ปลดล็อกสิทธิ์เขียนโค้ด (ยังไม่ใช่คำสั่งให้เขียน)
- **ถ้ามีแถวตาย** ⇒ ระบุแถว + ไบต์ที่หักล้าง + ผลกระทบ (เช่น ถ้า gate `0x5E4078` ไม่มีจริง TENSION พลิก · ถ้า `0x01081A90` โผล่ คำวินิจฉัย diff พลิก)
  ⇒ cc ลง erratum · **ห้ามเขียนโค้ดจาก span ที่เกี่ยวข้องกับแถวที่ตายจนกว่าจะ decode ใหม่**
- **ถ้า `0x402A20` ตัดสินขอบเขตด้วย static ไม่ได้** ⇒ ส่งไม้ต่อให้ GT-043 อย่างเป็นทางการ · TENSION ค้างที่ <100% อย่างมีเหตุผลระบุตัวได้

### nonclaims (ติดไปกับผลทุกกรณี)
- **ไม่ claim ว่าอะไรก็ตามที่เจอ ถูกส่งจริงโดยเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว ไม่เคยเผยแพร่ และกู้ไม่ได้ตลอดกาล ·
  **การประกอบ/ตีความของเราไม่ใช่ของเซิร์ฟเวอร์เดิม ซึ่งกู้ไม่ได้**
- **ไม่ claim ว่ามีอะไรเรนเดอร์บนจอ** — ทั้งใบเป็นชั้น ① ล้วน · การมี serializer/vtable ในอิมเมจ **ไม่พิสูจน์ว่าคลาสถูกสร้าง ถูก register หรือเคยขึ้นสาย**
- **ไม่ claim ว่ารู้ชื่อคลาสของ record บิต `0x08` หรือคลาสที่ `IsKindOf` ยกเว้น** — สอง vtable ไม่มี RTTI/name literal ·
  descriptor `0x0102CB04` เป็นศูนย์ในไฟล์ (สร้างตอนรัน) · **ห้ามเดาชื่อ = ห้ามประดิษฐ์ wire format**
- **ไม่ claim ว่ารู้ความหมายของ tag** — ยืนยันได้แค่ len (`0x2A`=float32/4 · `0x12`=uint16/2 · ที่เหลือรู้แค่ len)
- **ไม่ claim ว่า derived id `0x4543` ถูก** — id จริงมาจาก `0x89BD00` รันไทม์เก็บใน `ds:0x0108202C` ซึ่ง `.data` เป็นศูนย์ในไฟล์ ⇒ static พิสูจน์เลข id ไม่ได้
- **ไม่รื้อ** [NEGATIVE] ของ jump table `0x4469BD` (actor_type 2..6) — ปิดแล้ว
- ไม่แตะ DB · ไม่แตะเกม · ไม่แตะ `LOCK_GAME` · **ไม่มีดีไซน์/โมดูล/ข้อเสนอ wire ในผลของใบนี้** (ถ้าผลกลับมาพร้อมดีไซน์ = ทำเกินใบสั่ง ตัดทิ้ง)

- **result:** (ผู้รับงาน static บนสะพานกรอก: บัญชีรอด/ตายรายแถว + ไบต์ที่ตัดสิน + คำตอบขอบเขต `[mgr+0x24]` + span/sha ของ `0x402A20`
  + เวลา + sha อิมเมจก่อน-หลัง · ⏳ ถ้าเดินซ้ำแล้ว span sha ไม่ตรง = หยุดตรงนั้น รายงาน span ที่เพี้ยน ห้าม re-derive ทับ)


## 🆕⭐ GT-043 POP-SURVIVAL-001 [attended, ของแถมสังเกตล้วน]: หลังยิงเฟรม count-1 บิต `0x02` แล้ว NPC/วัตถุตัวอื่นในโลก "หายไหม"  [✅ **PASS-PERSISTENT-SURVIVAL / subsecond-unobserved — 2026-08-23 01:50 (+07:00): ไม่พบ NPC/วัตถุที่ติดตามหายแบบค้าง · ช่วง 0–3.524s ห้ามสรุป**]

> ✅ **RESULT 2026-08-23 01:33–01:50 (+07:00) — PASS-PERSISTENT-SURVIVAL** (host lane HYP-PF-027 · เฟรม `HYP_PF_027_NPC_HOSTILE_HOSTILE_SPAWN` 1×190 B ออกจริง):
> - หลังเฟรม count-1 bit `0x02`: Navy Transfer + landmark ฉาก (เรือ/โคม/เสา/โซ่) **ยังอยู่ครบ** ในภาพมุมเดิม +3.524..+9.978s และหลังแพน P2
> - 🔴 qualification: เครื่องมือจับภาพให้ภาพแรกช้า +3.524s แม้ขอ 0ms ⇒ **ปิดได้เฉพาะ "ไม่มีการหายแบบค้าง" — transient ต่ำกว่านั้น = non-observed**
> - ⭐ side-note ตอบ GT-032: **เส้นแดง/target panel เกิดหลัง Tab-select ไม่ใช่จาก hostility frame เพียงอย่างเดียว** (ภาพก่อน/หลัง Tab แยกกัน · target HP 100/100 Lv.1)
> - รอบ partial ก่อนหน้า (00:30 ใบ GT-030/043) นับเป็นหลักฐานเสริม ไม่ใช่ตัวปิด · รอบแรกคืนนี้ (boot 1012) ยกเลิกก่อน trigger — ไม่มี label ออก
> - ผลเต็ม: `notes_to_chief/20260823_0156_GT043-PASS-PERSISTENT-SURVIVAL-subsecond-unobserved.md` (บริโภค R123)

**ที่มา:** GT-040 ท่อน B decode ว่า **เฟรม `0x6E9D` ขาเข้าที่พา derived bit `0x02` (actor-entry collection) จะ trigger reconcile เต็ม**:
ทุกอ็อบเจกต์ใน `[mgr+0x24]` ของ client ที่ **ไม่อยู่ใน entry list ของเฟรมนั้น และไม่ผ่าน `IsKindOf` ที่ยกเว้น** จะถูกถอดจากทะเบียนกลางในการเรียกเดียวกัน
เลนที่พิสูจน์แล้วของเรา (HYP-PF-023/025/027 เช่น `HOSTILE_SPAWN` ของ GT-032) ส่งเฟรมแบบนี้ด้วย **count 1 เป๊ะ**
แต่ **ไม่เคยมีใครรายงานว่าประชากรถูกกวาด** (และไม่เคยมีใคร assert ว่าไม่ถูกกวาด — คือไม่เคยมีใครดู)
ท่อน B ทิ้งความเป็นไปได้สามข้อที่ตัดสินไม่ได้ด้วย static: **(ก)** เฟรมเราไม่ได้เดินเข้า path นั้นจริง ·
**(ข)** ประชากร scene-load ไม่ได้อยู่ใน `[mgr+0x24]` · **(ค)** ไม่เคยมีใครดูผลหลังยิงจริง
🔴 **ใบนี้ปิดข้อ (ค) ด้วยวินัยการสังเกตล้วน — ศูนย์โค้ดใหม่ ศูนย์ flag บูตใหม่** แนบเข้ากับเลนที่ยิงอยู่แล้ว

### objective (claim เดียว)
**หลังยิงเฟรม count-1 ที่พาบิต `0x02` หนึ่งเฟรม NPC/วัตถุตัวอื่นที่อยู่ในโลกก่อนหน้า "หายจากโลก/เรดาร์" หรือไม่**
🔴 **ทั้งสองผลชี้ขาด:** **หาย** = reconcile ทำงาน live กับประชากรฉากจริง (ใหญ่มาก — ทุกเฟรม count-1 ในอนาคตเป็น destructive) ·
**ไม่หาย** = ประชากร scene-load อยู่นอก `[mgr+0x24]` หรือได้รับการยกเว้น (จำกัดกรอบดีไซน์ loot-despawn ทั้งหมด)

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
- ใช้ **db และ args ของเลนเจ้าบ้านที่แนบไป** เป๊ะ (GT-030 rerun หรือ GT-032-family) — **ใบนี้ไม่เพิ่ม flag ไม่เปลี่ยน args แม้ตัวอักษรเดียว**
- เทียบ sha256 canonical กับ `CANON_SHA.txt` ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง

### server args (เป๊ะ)
**= args ของเลนเจ้าบ้าน** (เช่น `--npc-hostile-hypothesis-scenario scenarios\npc_hostile_hypothesis_faction_pairing.json` สำหรับตระกูล GT-032
หรือ scenario ของ GT-030 rerun) + `--db` สำเนาตามปกติ · ไม่มีอะไรใหม่
🔴 **แนบกับเลนไหน ให้ยืนยันก่อนว่าเฟรมของเลนนั้นเป็น count-1 บิต `0x02` จริง** (GT-032 `HOSTILE_SPAWN` = ใช่ · GT-030 actor_type 2 = ใช่)
เลนที่ไม่พาบิต `0x02` **ไม่เข้าข่ายใบนี้** (ตาม gate `0x5E4078 je` ที่ท่อน B เจอ — ไม่มีบิต `0x02` = ไม่แตะประชากรเลย)

### 🔴 อ่านก่อน — ท่ามาตรฐานอินพุตของรอบใหญ่ #12
- **ปุ่ม/ช่องแชตคลิกสังเคราะห์ไม่ติดเป็นช่วง ๆ · `Return` ใช้ได้เสมอ** ⇒ ท่า: `Return` -> พิมพ์ -> `Return`
- trigger แชต = **ascii 12 ตัวเป๊ะ** (สั้นกว่านั้นถึงเซิร์ฟแต่ไม่เข้าเงื่อนไข เงียบ ไม่มี sweep) · ตัวอักษรตอนช่องไม่โฟกัส = hotkey
- เปิด server ก่อน client เสมอ · การ์ด `Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client

### steps (แนบเข้ากับการยิงเฟรมของเลนเจ้าบ้าน — เพิ่มแค่การถ่ายภาพรอบการยิง)
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · ทำสำเนา DB ตามเลนเจ้าบ้าน
1. บูตตามเลนเจ้าบ้านจนเข้าแมพ (server -> client -> เลือกตัว -> เข้าเกม ด้วย `Return`)
2. เดินให้ **NPC/วัตถุอื่นหลายตัว** อยู่ในเฟรมกล้องพร้อมกับเป้าของเลนเจ้าบ้าน — เลือกมุมที่เห็น landmark หลายตัว (เช่น NPC ประจำแมพรอบจุดเกิด Port Royal)
3. 🔴 **BEFORE — ถ่ายชุดหลักฐานก่อนยิง:**
   - ภาพ **P0** = ภาพรวมมุมกล้องเห็น NPC/วัตถุอื่นหลายตัว (นับจำนวน จดตำแหน่ง/ชื่อที่อ่านได้)
   - **เฟรมทีละตัว:** คลิก/Tab เลือก NPC อื่นแต่ละตัวที่เห็น ถ่ายแผง target ให้เห็นว่า "มีตัวตนก่อนยิง" (P0a, P0b, ...)
   - เปิดเรดาร์/มินิแมพถ้ามี ถ่ายให้เห็นจุดของตัวอื่น (P0r)
4. **ยิงเฟรมของเลนเจ้าบ้าน** (แชต ascii 12 ตัว -> sweep 1 เฟรม) · ยืนยัน console เห็น label ของเลนนั้นออก 1 เฟรม
5. 🔴 **AFTER — ถ่ายชุดเดียวกันจากมุมเดิมเป๊ะ:**
   - ภาพ **P1** = มุมเดิม นับ NPC/วัตถุอื่นที่ยังเหลือ เทียบกับ P0
   - เฟรมทีละตัวซ้ำ NPC ชุดเดิม (P1a, P1b, ...) — ตัวไหนคลิก/Tab ไม่ขึ้นแผงแล้ว = ผู้ต้องสงสัยว่าหาย
   - เรดาร์/มินิแมพ (P1r) เทียบจุด
6. **เดิน/แพนกล้องยืนยัน:** เดินเข้าหาจุดที่ NPC อื่นเคยยืน (จาก P0) ถ่าย **P2** — ถ้าตัวนั้นหายจริง ต้องหายทั้งจากภาพและจากการเดินเข้าไปใกล้ (กันกรณี culling ระยะไกล)
7. **โน้ตข้ามใบจาก GT-032 (เก็บพร้อมกัน ประหยัดรอบ):** ที่เป้าของเลนเจ้าบ้านเอง **ถ่ายหลังยิงแต่ก่อนกด Tab หนึ่งภาพ (P-tab-before)** แล้วค่อยกด Tab ถ่าย (P-tab-after)
   — เพื่อแยก "เส้นขอบแดงจาก hostility" ออกจาก "เส้นขอบจากการเลือกเป้า" ที่ GT-032 ค้างไว้
8. ออกจากเกมตาม PLAYBOOK -> ปิด server เก็บ raw GAME log + console -> `PRAGMA integrity_check;`
9. **teardown เสมอ** แม้เลิกกลางคัน (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 — เพดานยกจาก 180 เมื่อ 2026-08-20 · `TEMPLATE_teardown_generic.ps1:135`)
10. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม

### pass criteria — สองชั้น แยกกันเด็ดขาด

**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ)** — เก็บเพื่อพิสูจน์ว่า "เฟรมออกไปจริง" (ถ้าไม่ออก การไม่หายไม่มีความหมาย):
- raw GAME log เห็นเฟรมของเลนเจ้าบ้านออก **1 เฟรม** (label ถูกต้อง · ขนาดตรงดีไซน์ของเลนนั้น · ไม่มี `compose_refused`/`already_sent`/refusal)
- ไม่มี `ErrorData=28317` · `PRAGMA integrity_check` = `ok` · sha canonical ก่อน-หลังตรงกัน
- **ชั้นนี้ตอบไม่ได้:** NPC ตัวอื่นหายหรือไม่ (การถอดจากทะเบียนกลางไม่พิมพ์อะไรใน log ฝั่งเซิร์ฟเวอร์ — ท่อน B nonclaim ข้อ 1) ⇒ **ห้ามอ้างชั้นนี้แทนชั้น (2)**

**ชั้น (2) client-observable (ต้องมีคนหน้าจอ)** — คือหัวใจของใบนี้:
- ชุดภาพ **P0/P0a../P0r (ก่อน)** และ **P1/P1a../P1r (หลัง)** จากมุมเดิม + **P2 (เดินยืนยัน)** ครบ อ่านได้
- ตอบข้อเดียวเป็นภาษาคน: **NPC/วัตถุตัวอื่น (ที่ไม่ใช่เป้าของเลน และไม่ใช่ผู้เล่นเอง) หายจากโลก/เรดาร์หลังยิงหรือไม่ · ถ้าหาย หายกี่ตัว ตัวไหน**
- เก็บ **P-tab-before / P-tab-after** ของเป้าเลนเจ้าบ้าน (โน้ต GT-032)
- **ชั้นนี้ตอบไม่ได้:** ทำไมถึงหาย/ไม่หาย (เป็นข้อ ก/ข/ค ของท่อน B ซึ่ง static ต้องปิด — ดู GT-042 จ็อบ 3) · **ภาพหน้าจอไม่ใช่หลักฐานของการถอดทะเบียนระดับไบต์ ห้ามอ้างข้ามชั้น**

### 🔴 ผลลบมีค่าเท่าผลบวก
1. **มีตัวอื่นหาย** ⇒ **ข่าวใหญ่ที่สุดของใบนี้** — reconcile ทำงาน live กับประชากรฉาก ⇒ ทุกเฟรม count-1 บิต `0x02` ในอนาคตเป็น destructive
   ⇒ หยุด เก็บวิดีโอ/ภาพช่วงยิง + console + raw GAME log ทั้งไฟล์ · เลนที่ยิงเฟรมแบบนี้ทั้งหมดต้องทบทวนใหม่
2. **ไม่มีตัวไหนหายเลย** ⇒ **ผลเต็มใบเท่ากัน** — ประชากร scene-load อยู่นอก `[mgr+0x24]` หรือได้รับการยกเว้น `IsKindOf`
   ⇒ ตัดความเป็นไปได้ (ก) ของท่อน B ทิ้ง เหลือ (ข) เป็นคำอธิบายหลัก · จำกัดกรอบดีไซน์ loot-despawn (ลูทที่โผล่จะไม่โดนกวาดโดยเฟรม actor ปกติ)
   ⇒ ส่งไม้ต่อให้ GT-042 จ็อบ 3 ยืนยันขอบเขต `[mgr+0x24]` ฝั่ง static

### เกณฑ์หยุด
- NPC ตัวใดตัวหนึ่งหายทันทีหลังยิง = หยุด เก็บภาพ/วิดีโอ + console ทั้งไฟล์ + raw GAME log
- `ErrorData=28317` = หยุด เก็บ console ทั้งไฟล์ (การสลับสองสายพานในเซสชันเดียวพัง)
- ชื่อเกณฑ์หยุดของเลนเจ้าบ้านโผล่ (เช่น `ProbeControl03` ของ GT-030) = ปฏิบัติตามเกณฑ์หยุดของเลนนั้นก่อน

### nonclaims (ติดไปกับผลทุกกรณี)
- **การประกอบเฟรม/faction/สูตรของเลนเจ้าบ้านเป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล**
- **ไม่ claim ว่า "ถอดจากทะเบียน" = "หายจากจอ"** ในทางกลับกันด้วย — ใบนี้วัดสิ่งที่ตาเห็นเท่านั้น · การเชื่อมไปถึงไบต์ `[mgr+0x24]`/`0x441C40` เป็นงานของ GT-042 (static)
- **ไม่ claim ว่ารู้ว่าทำไมหาย/ไม่หาย** — ข้อ ก/ข/ค ตัดสินด้วยใบนี้ใบเดียวไม่ได้ ต้องคู่กับ GT-042
- **ไม่ใช่ combat/aggro/persistence** — ไม่มี NPC โจมตี ไม่มี HP write path · เลนเจ้าบ้านพิสูจน์สิ่งของมันเอง ใบนี้พ่วงการสังเกตประชากรเท่านั้น
- **ไม่ claim ว่า "ของลูทบนพื้น" มีอยู่จริงในเกม** — record บิต `0x08` ที่ท่อน A เจอยังไม่พิสูจน์ว่าเรนเดอร์ · ใบนี้ไม่แตะเรื่องนั้น
- **แถว coverage ไม่ขยับไม่ว่าใบนี้ออกหัวหรือก้อย** — เป็นการสังเกตพ่วง ไม่เปิด/ปิดรอบเทสด้วยตัวเอง

- **result:** (ผู้เทสกรอก: เลนเจ้าบ้านที่แนบ + label เฟรมที่ออก + ชุดภาพ P0../P1../P2 + P-tab-before/after พร้อม sha256 ทุกใบ
  + คำตอบ "ตัวอื่นหายไหม กี่ตัว" เป็นภาษาคน + เวลา + sha canonical ก่อน-หลัง + path raw GAME log)

## 🆕🔬 GT-044 SCENEID-BG0001-001 [STATIC-ON-BRIDGE]: dump SCENE_NAME (ตาราง 007) + MAP_SCENE_LIST (ตาราง 101) จาก `B_CONSTDATA_TH.pc_.dec` — ปิดเลข scene id เชิงตัวเลขของ bg0001  [✅ **PASS — 2026-08-23 02:07 (+07:00): `BG0001` = numeric scene id `1` ตรงกับที่ lane scene_load ส่งอยู่**]

> ✅ **RESULT 2026-08-23 02:03–02:07 (+07:00) — PASS** (source read-only · SHA ก่อน/หลังตรง):
> - `SCENE_NAME` (007) แถว index 0: `n_ID = 1` · `s_MODLE_ID = BG0001` · `s_SCENE_NAME = 皇家港` · `s_IMAGENAME = Bg0001_air` ⇒ **mapping ตรงจากตารางเดียว ไม่พึ่ง numeric coincidence**
> - dump เต็มสองตาราง: `outbox/GT044_SCENE_NAME_007.tsv` (271 แถว) + `GT044_MAP_SCENE_LIST_101.tsv` (15 แถว)
> - 🔴 ข้อห้ามที่ได้มาด้วย: **ห้าม join `MAP_SCENE_LIST.n_ID=1` กับ `SCENE_NAME.n_ID=1` เพียงเพราะเลขเท่ากัน** — ไม่มี crosswalk field พิสูจน์ · namespace แยกกัน
> - nonclaim: พิสูจน์ mapping ใน client data เท่านั้น ไม่พิสูจน์ว่า runtime ใช้เลขนี้อย่างไร · ไม่เปลี่ยนผล GT-034
> - ผลเต็ม: `notes_to_chief/20260823_0207_GT044-PASS-bg0001-scene-id-1.md` (บริโภค R123) ⇒ nonclaim `scene_id_numeric_provenance` ของ GEO-PF-006 **ปิดที่ชั้น client-table แล้ว**

**ที่มา:** รอบ 122 ยืนยันโซนให้ GT-034 ได้สูงสุดแค่ระดับ **file-membership** (P0 กับ P30 เป็นแถวของตาราง frozen
`PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` 115 แถวเดียวกัน ที่ derive จาก `bg0001_npc_placements_decoded.tsv`) —
**เลข scene id เชิงตัวเลขของ bg0001 ไม่เคยถูก dump** เพราะสองตารางนี้อยู่ในอิมเมจที่เข้าถึงได้จากเครื่องสะพานเท่านั้น
(จดคำขอลง `IMAGE_ACCESS_COST.tsv` แล้วรอบ 122)

- **objective:** พิสูจน์หนึ่งข้อ: **scene id เชิงตัวเลขของ bg0001/Port Royal ตาม client tables คือเลขอะไร** —
  และเลขนั้นตรงกับ `scene_id: 1` ที่เลน scene_load ส่งอยู่หรือไม่
- **แหล่ง (อ่านอย่างเดียว ห้ามแก้อิมเมจ · จด sha อิมเมจก่อน-หลัง):**
  `Pirate Force ServerProject/backups/v103_one_item_backpack_20260814_103143/derived/v97_mapping_audit/B_CONSTDATA_TH.pc_.dec`
  - ตาราง **007 SCENE_NAME**: offset `0x0000B3D4-0x0001D148` · 271 แถว x 24 คอลัมน์
  - ตาราง **101 MAP_SCENE_LIST**: offset `0x007F9580-0x007FA044` · 15 แถว x 15 คอลัมน์
  - (offsets จาก `FACTPACK_R100_CONSTDATA_MONSTER_LOOT.md` หัวข้อดัชนีตาราง · เครื่องมือ: `parse_pc_tables.py` ตัวเดิมที่ใช้ parse STANDARD_MOB)
- **steps:** ① parse สองตารางเป็น TSV เต็มทุกแถวทุกคอลัมน์ ② หาแถวที่ผูกกับ bg0001 / Port Royal
  (ชื่อไฟล์ฉาก, ชื่อแสดงผล, หรือ mapping ใน MAP_SCENE_LIST) ③ จดเลข id + เส้นทางการ join ที่ใช้หาให้ re-derive ได้
- **pass criteria:**
  - **ชั้น static (ชั้นเดียวของใบนี้ — ไม่มีชั้น client-observable):** TSV dump ครบสองตาราง + sha256 ของ TSV +
    คำตอบชี้ขาด: bg0001 = scene id เลขอะไร · ตรง/ไม่ตรงกับ `1` ที่เลนส่ง
  - **ผลลบมีค่าเท่าผลบวก:** ถ้าสองตารางไม่มี mapping ที่ resolve ได้ = จดเป็นผล ("ตอบจาก tables ชุดนี้ไม่ได้") —
    คาเวียตใน GT-034 คงอยู่ต่อไปตามเดิม ไม่มีใครต้องรันอะไรซ้ำ
- **ผลต่อใบอื่น:** ยกระดับคำตอบ "แมพเดียวกัน" ของ GT-034 จาก file-membership เป็นเลขตัวเลข ·
  **ไม่บล็อกและไม่ปลดบล็อกการรัน GT-034** — GT-034 รันได้ก่อนใบนี้ปิด (คาเวียตแมพ/โซนในใบนั้นรองรับแล้ว)
- **nonclaims:** ตารางทั้งสองเป็นข้อมูลที่ ship มากับ client — ไม่ใช่พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล ·
  ไม่พิสูจน์ว่า client *ใช้* เลขนี้ที่ runtime ตอนตัดสินใจโหลดฉาก — พิสูจน์แค่ mapping ในไฟล์ข้อมูล
- **result:** (ผู้รับงาน static บนสะพานกรอก: เลข id + เส้นทาง join · path TSV + sha256 · sha อิมเมจก่อน-หลัง · เวลา)


## ⭐ GT-045 GROUNDDROP-RENDER-001 **v3 re-run** [attended, in-game]: บิต `0x08` ของ `0x5F85B0` วาด "วัตถุลูทบนพื้น" ไหม — ยิงเรคคอร์ดพิกัดโลกที่ payload ชี้ไอเทม **ที่มี drop model จริง** แล้วดูว่าไคลเอนต์วาดอะไร  [✅ **ANSWERED — ปิดโดย chief R163 (2026-08-25 ~15:xx +07:00) จากผลสี่รอบ attended 1122–1136 (2026-08-25 11:48–13:4x +07:00) · จดหมาย `20260825_1235` · `20260825_1300` · `20260825_1340` — Panya ขับ UI เองทุกขั้น**

🔴 **ปิดเป็น `ANSWERED` ไม่ใช่ `PASS` เต็ม — และความต่างนี้มีผลต่อ P2 ของ promotion โดยตรง**
คำถามของใบถูกตอบครบ แต่ **คำตอบคือ "ไคลเอนต์วาดบางส่วน ไม่ใช่ทั้งหมด"** ⇒ ไม่ใช่ PASS ที่จะยกไปนับเป็น P2 ได้เฉย ๆ

| ชั้น | ผล |
|---|---|
| **wire/DB** | ✅ **PASS เป๊ะทุกไบต์ ทั้งสี่รอบ — ปิดถาวร ไม่ต้องพิสูจน์ซ้ำ** · `NEAR` = trigger `+30.000` X payload `67 93 21 00` = **2200423** · `FAR` = `+800.000` X payload `c3 91 21 00` = **2200003** · 54 B ทั้งคู่ · Y/Z ของ trigger ทุกบิต |
| **client-observable** | ✅ **ตอบแล้ว แต่เป็นคำตอบผสม:** ป้ายชื่อ `Red leaves Hammer` **ตัวอักษรสีแดง วาดจริง อ่านออกเต็มคำ** (อายุ ~0.2–0.3 วิ แล้วหาย) · **ฝุ่นสีน้ำตาลวาดจริง** · 🔴 **โมเดลไอเทม ไม่มี** · **ไม่เหลืออะไรบนพื้น** (เดินทับทั้ง NEAR และ FAR) |

🔴🔴 **แก้หลักฐานโดย chief R163 หลัง `pf-adversary` จับได้ — อ่านข้อนี้ก่อนอ้างใบนี้เป็น P2 ของ promotion**

จดหมาย `20260825_1340` §① อ้างหลักฐานภาพสองชุด · **chief เปิดดูชุดแรกเองแล้วทีละใบ และมันไม่แสดงสิ่งที่อ้าง:**

| หลักฐานที่จดหมายอ้าง | อยู่ในรีโปไหม | เปิดดูแล้วเห็นอะไรจริง |
|---|---|---|
| ~~`evidence_screens\GT045v3r3_1132_FULLRES_t179*.jpg` (รอบ 3)~~ | ✅ มี 6 ใบ (`t178.0`–`t180.5`) | 🔴 **ไม่มีป้ายชื่อไอเทมในเฟรมไหนเลย** · ข้อความลอยชิ้นเดียวคือ **`Arena01` = ชื่อตัวละครของผู้เทสเอง** (สีส้ม) · HUD `X:-8,690 Y:-2,741` **ไม่ใช่จุด trigger** (`-8553.9 / -2579.7`) · พื้นโล่ง ไม่มีอะไรวางอยู่ |
| `1135_gt045v3r4_FULLROUND_20260825_132508.mkv` ~`t=249 s` (รอบ 4) | ❌ **ไม่มี** (เกินเพดาน 2 MB) · **ไม่มี sha256** | ยังไม่มีใครนอกจากผู้เทสเห็น |

⇒ 🔴 **หลักฐานชิ้นเดียวที่ค้ำคำว่า "ป้ายชื่อวาดจริง" คือเฟรมวิดีโอรอบ 4 ซึ่งไม่มีใครตรวจซ้ำได้**
· ชุด jpg รอบ 3 **ถูกอ้างผิด** — chief ยกมาจากจดหมายโดยไม่เปิดดูก่อน **นั่นคือความผิดของ chief ไม่ใช่ของผู้เทส**
· 🔴 **ห้ามใครอ่านคำว่า `Arena01` สีส้มในชุด jpg นั้นว่าเป็น "ป้ายไอเทมสีแดง/ส้ม"** — มันคือป้าย **ชื่อผู้เล่น**
  คนละชนิด คนละเส้นโค้ด (`NameBoardPlayer` ไม่ใช่ ground-item label)

📌 **ที่ยังทำให้ปิดใบได้:** ท่าปิดใบด้วย **คำยืนยันด้วยตาของคุณ Panya บนวิดีโอต่อเนื่องที่อยู่บนสะพาน**
เป็นบรรทัดฐานที่ใช้ปิด `GT-059` มาแล้ว (จดหมาย `20260824_2133` — วิดีโอสองไฟล์นั้นก็เข้ารีโปไม่ได้ด้วยเหตุเดียวกัน)
· เธอขับ UI เองทุกขั้นทั้งสี่รอบ · **ชั้น wire แยกต่างหากและ byte-exact ทั้งสี่รอบ**
🔴 **แต่ต้องพก nonclaim นี้ติดใบตลอดไป: ชั้น client-observable ของใบนี้ตรวจซ้ำจากรีโปไม่ได้**

🔴 **สิ่งที่ขอจากหน้าสะพาน (ไม่บล็อกการปิดใบ แต่ทำให้ใบตรวจซ้ำได้):**
export เฟรม `t≈249 s` ของ `1135_gt045v3r4_FULLROUND_20260825_132508.mkv` เป็น **ภาพนิ่ง full-res**
แล้ว commit เข้า `evidence_screens\` พร้อม **sha256** (ถ้าเกิน 2 MB ให้ **crop จากต้นฉบับ ห้าม resize ลง**)
· 🔴 **ห้ามลบวิดีโอไฟล์นั้นบนสะพาน — เป็นหลักฐานชิ้นเดียวที่ปิดครึ่ง client ของใบนี้**

🔴 **คำทำนายของใบเองที่ถูกหักล้าง — จดไว้เพราะมันบอกความจริงมากกว่าข้อที่ถูก:**
- **P1** *("ขึ้นโมเดลแบบค้อน และคาดว่าค้างบนพื้น")* — **ผิดทั้งสองท่อน**
- **P3** *("ป้ายชื่ออาจไม่ขึ้นเพราะเราส่ง mask `0x12` เท่านั้น")* — **ถูกหักล้าง: ป้ายขึ้นทั้งที่ไม่เคยส่งฟิลด์ชื่อ**
  ⇒ สอดคล้องกับ `RE-066` (create path A query `s_NAME` เอง) และ `RE-060` ⇒ **ไคลเอนต์ไปหยิบชื่อจากตารางตัวเอง**

🆕 **ของที่ใบนี้ผลิตออกมาโดยไม่ได้ตั้งใจ และกลายเป็นงานต่อสองใบ:**
① **สีของป้ายเป็นแดง แต่เซิร์ฟเวอร์ต้นฉบับวาดไอเทมตัวเดียวกันเป็นขาว** ⇒ เปิด **`RE-067`** (`CLIENT_RE_QUEUE.md`)
② เกณฑ์ **P6 "เทียบกับของจริง"** + ทะเบียน `REAL_SERVER_DIVERGENCE.tsv` (คำสั่งคุณ Panya ~14:2x +07:00)

🔴 **สิ่งที่ใบนี้ยัง *ไม่* ตอบ และห้ามใครอ่านว่าตอบแล้ว:** **อะไรทำให้โมเดลไม่ขึ้น**
`HYP-PF-032` เต็ม **3/3 ⇒ ไม่มี v4** · จะไล่ต่อต้องเป็น **scoped approval ที่ระบุ ID** หรือ slot ใหม่ **ห้ามเปิดเวอร์ชันที่สี่เอง**
🔴 **`GT-060` เงื่อนไข (ข) ยังไม่ปิด** — ไม่มี drop-object ที่คลิกได้ เพราะไม่มีโมเดลให้คลิก]

*(สถานะเดิมก่อนปิด:* [🟢 **PENDING — พร้อมบูต · เงื่อนไข "รอ merge" ปิดแล้วโดย chief R159 (2026-08-25 ~09:0x +07:00)**
· PR โค้ด **#28** เขียว(Actions run `32797565782` · อ่านทาง `ci-status` · `sha` ในไฟล์ตรงกับที่ขอเป๊ะ · `conclusion:"success"`)
· merge `4745635` (เนื้อของ `e99ac0d` เข้า `main` ครบ ตรวจด้วย tree-identity ตอน R159)
· **เงื่อนไขที่ยังเหลือ ห้ามข้าม:** `BOOT_COMMIT` ที่ resolver ให้ **ต้องผ่านห้าข้อในบล็อก "ก่อนบูต" ข้างล่าง**

🔴 **ห้ามเทียบ `BOOT_COMMIT` กับเลข commit ใด ๆ ด้วยตา — ให้ตัดสินด้วยเนื้อ (ข้อ 4/5) เท่านั้น**
เหตุผล (วัดจริงรอบ R159 · pf-adversary จับได้): resolver คืน **`e99ac0d`** ซึ่งเป็น **หัว branch ที่ gate ตัดสิน**
ไม่ใช่ merge commit `4745635` — และ `e99ac0d` **"เก่ากว่า"** `4745635` ทุกวิธีวัด (เป็น parent ของมัน · เวลาก่อนหน้า 4m44s)
⇒ กฎแบบ "ถ้าเก่ากว่า `4745635` ห้ามบูต" **จะสั่งห้ามบูตเสมอ ทั้งที่ commit นั้นถูกต้อง** ⇒ เผารอบทิ้งฟรี
· merge commit **ไม่มีไฟล์คำตัดสินของตัวเอง** (`ci/4745635….json` ไม่มีจริง) ⇒ resolver จะไม่มีวันชี้มา **โดยดีไซน์**] · ครึ่ง wire ปิดแล้วรอบ 1104 (PASS เป๊ะทุกไบต์) · ครึ่ง client เปิดอยู่ (PARTIAL — ฝุ่นขึ้น ไม่มีโมเดล) · **ห้ามบูต v1/v2 ซ้ำ** · อ่านคู่ FINDINGS_R128 + GT-034 + GT-048*)*

### 🆕 อัปเดต R162 (2026-08-25 ~11:1x +07:00) — 🔴 งบเวอร์ชันของเลนนี้เต็มแล้ว: v3 คือใบสุดท้าย
**อ่านก่อนกดบูต · ผู้เทสไม่ต้องตัดสินใจเรื่องงบเอง ทุกทางออกข้างล่างมี "ขั้นต่อไป" เขียนไว้แล้ว**

**[วัดแล้ว R162 · chief อ่าน `docs/HYPOTHESIS_LEDGER.json` repo `pirate-force-server` เอง — ห้ามแก้ตัวเลขเหล่านี้]**
- `HYP-PF-032`: `max_versions: 3` · `tracked_versions` (อยู่ **ใต้คีย์ `expiry`** ไม่ใช่ระดับ entry) =
  `["GROUND-LOOT-001", "GROUND-LOOT-001-v2-trigger-relative", "GROUND-LOOT-001-v3-equipment-base-drop-model-ids"]`
  ⇒ **เต็ม 3/3 เหลือศูนย์** · `extension_approval_ref: null` · `status: active` · `production_allowed: false`
- ฟิลด์ `decision` ของ entry เขียนไว้เองว่า **further wire change ต้องมี extension decision จากเจ้าของก่อน** ·
  นโยบายกลาง `policy.max_related_versions = 3`
- 🔴 **แปลว่า: GT-045 v3 ที่กำลังจะบูตคือเวอร์ชันสุดท้ายที่งบอนุญาต — ถ้าผลกำกวม ไม่มี v4**
  เลนจะแช่แข็งจนกว่าจะมี **scoped approval** จากเจ้าของ
- 🔴 **รอบนี้ห้ามแก้ ledger ห้ามเติม `tracked_versions` ห้ามตั้งชื่อ v4 ไม่ว่าผลจะออกแถวไหน** —
  คุณ Panya กำลังพิจารณาแก้นโยบายงบเวอร์ชันอยู่ **จดหมายแยกจะตามมา** ⇒ รอจดหมายนั้น ไม่ใช่รอผู้เทส

**ตารางงบเวอร์ชันต่อแถวของเมทริกซ์ A-E (ตารางเสริม · ชี้กลับแถวเดิมที่ท้ายใบ — 🔴 ความหมายของแถวเดิมไม่ถูกแก้แม้แต่แถวเดียว)**
| แถวเดิม | นับเป็น | ใช้เวอร์ชันสุดท้ายไปแล้วคุ้มไหม | ขั้นต่อไป **โดยไม่ต้องใช้ v4** |
|---|---|---|---|
| **A** | ✅ **ตอบแล้ว** | **คุ้ม** — claim เดียวของใบปิดฝั่งบวก | บริโภคผลตามใบ (ครึ่ง "มีวัตถุวาดจริง" ของเงื่อนไข (ข) ใน GT-060) · คำถามที่เหลือ (ฟิลด์ไหนขับ · คลิกได้ไหม) **แตะ wire ⇒ ต้องมี scoped approval ก่อน ห้ามเปิดเอง** |
| **B** | ✅ **ตอบแล้ว** (คำตัดสินมาจาก E1 อย่างเดียว) | **คุ้ม** เท่าแถว A | เท่าแถว A · E2 จดเป็น **คำถามเปิดเรื่องระยะ** ตามแถวเดิม — ไม่ใช่งานที่ต้องเปิดเวอร์ชันใหม่ |
| **C** | 🟡 **กำกวมสำหรับ claim ของใบ** (แต่ E2 ให้ผลบวกเรื่อง "ไคลเอนต์วาดจาก wire ได้") | **คุ้มครึ่งเดียว** — ได้ผลบวกเรื่องการวาด แต่ไม่ได้คำตอบเรื่องเลขไอเทม | ทำได้ทันทีโดยไม่กินงบ: **ใบ static แยก D-i/D-ii** (ใช้กับ E1 ได้ตรง ๆ) + จดคำถาม **ระยะ** และ **table code 22 vs 26** ไว้ · 🔴 ใบ "ยิงสองไอเทมที่ระยะเท่ากัน" และตัวคุม `2600022` = **แตะ wire ⇒ ต้องมี scoped approval ก่อน** |
| **D** (D-i / D-ii) | 🔴 **ผลลบสมบูรณ์ = ตอบแล้ว มีค่าเท่าผลบวก** แต่ **ยังไม่ระบุกลไก** (RE-066 ตัดทาง "ไคลเอนต์ไม่อ่านเลข" ทิ้งแล้ว เหลือสองทาง) | **คุ้ม** — ผลลบนี้คือสิ่งที่ทำให้ใบ static ถัดไปเล็งถูกจุด | **ใบ static แยก D-i/D-ii เป็นอย่างแรก** (D-i ตัวขวางหลัง lookup · D-ii ไม่เคยเดินเข้า `0x005F41E0`) — 🟢 **static ไม่แตะ wire ⇒ ไม่กินงบเวอร์ชันของ `HYP-PF-032` เลย** เปิดได้ทันทีไม่ต้องขออนุมัติ |
| **E** | 🔴 **NO-RESULT (regression) — ไม่ใช่ผลลบ และ "ไม่กินงบ"** | ยังไม่ได้ใช้เวอร์ชันจริง (ไม่มีการเปลี่ยน wire) | 🟢 **รันซ้ำ commit เดิมได้เลย ไม่นับเป็นเวอร์ชันใหม่ ไม่ต้องขออนุมัติใคร** — ตรวจห้าข้อ/label/ช่วงวิดีโอตามบล็อกตัวคุมบวก แล้วบูตใหม่ · 🔴 แต่ถ้าจะ **แก้ payload/มาสก์/เลขไอเทม** แม้แต่นิดเดียว = เวอร์ชันใหม่ = **ต้องมี scoped approval ก่อน หยุดแล้วเขียนจดหมาย** |

- 🔴 **กฎเดียวที่ผู้เทสต้องจำ:** ออกแถวไหนก็ตาม ให้ **กรอกช่อง result ตามปกติแล้วหยุด** — ห้ามเปิดรอบ attended ต่อเนื่องเอง
  ห้ามแก้เลขไอเทมเอง "เพื่อลองอีกที" · ทุกทางที่แตะ wire ต้องผ่านจดหมายถึงเจ้าของก่อนเสมอ
- ⚠️ **nonclaim ของบล็อกนี้:** นี่เป็นเรื่อง **งบเวอร์ชัน/กระบวนการ** เท่านั้น — **ไม่แก้ objective, steps, pass criteria, คำทำนาย
  หรือความหมายของแถว A-E ใด ๆ** และไม่พิสูจน์อะไรเกี่ยวกับพฤติกรรมไคลเอนต์

### 🆕 อัปเดต R161 (2026-08-25 ~10:0x +07:00) — **สามเรื่อง อ่านก่อนบูต**
1. ✅ **teardown ไม่ต้องแก้เองแล้ว** — บั๊ก `-replace '\','/'` ถูกแก้ที่ต้นทางทั้ง `1103`/`1105`
   **กฎใหม่: ก๊อป teardown จาก `1116` หรือ `1119` ห้ามก๊อปจาก `1103`/`1105`** (คำวินิจฉัยเดิม "ต้องแก้ตัวสร้างเทมเพลต" **ผิด ถอนแล้ว**)
2. 🔴 **เช็คข้อ 5 เปลี่ยนอีกครั้ง (ครั้งที่สาม) — คราวนี้เล็ง `.py` ด้วย** เพราะ **ไฟล์ที่ส่งไบต์ออกสายคือ `.py:211/216` ไม่ใช่ JSON**
   ฉบับ R159 เล็ง JSON อย่างเดียวจึงเป็น **ตัวแทน** ไม่ใช่ตัววัดตรง · ดูบล็อกประวัติใต้ห้าข้อ (เหตุผล + ผลวัดครบห้า commit)
3. ✅ **RE-066 ปิดแล้ว = ข่าวดีของใบนี้:** **ไคลเอนต์อ่านเลขไอเทมจริง** (T2 ตาย) ⇒ การเปลี่ยนเลขของ v3
   **เป็นการทดสอบตัวแปรที่ไคลเอนต์อ่านจริง ไม่ใช่การเดา** · และฟิลด์ที่มัน query คือ **`n_DROPMODEL_TYPE`** ⇒ เกณฑ์เลือกไอเทมเล็งถูก
   🔴 **แต่แถว D เปลี่ยนความหมาย ไม่ได้หายไป** — ดูเมทริกซ์และบล็อก nonclaims

### ✅ สถานะ v3 (อัปเดต R159 · 2026-08-25 ~09:1x +07:00) — **merge แล้ว พร้อมบูต**
*(หัวข้อเดิมของ R158 คือ "🔴 BLOCKED-รอ-merge · PR เปิดอยู่ ยังไม่ merge" — **ล้าสมัยแล้ว** PR #28 merge เข้า `main` ตั้งแต่ 08:3x +07:00)*
เลนโค้ดเปลี่ยน `payload_dword` แล้ว (chief · server repo · **อยู่บน `main` เรียบร้อย**):
```
element 1 (ใกล้ +30X)   payload_dword 2200423   EQUIPMENT_BASE n_ID=423  (n_ID_MODEL=0 · n_DROPMODEL_TYPE=1)
element 2 (ไกล +800X)   payload_dword 2200003   EQUIPMENT_BASE n_ID=3    (n_ID_MODEL=2 · n_DROPMODEL_TYPE=1)
เดิม (รอบ 1104) ทั้งสอง element = 2600001  ITEM_MISC n_ID=1  (n_ID_MODEL=0 · n_DROPMODEL_TYPE=0)
```
🔴 **บูตบน commit เก่า = ยิง `2600001` ซ้ำ = ได้ผลรอบ 1104 อีกรอบ = เผารอบ attended ทิ้งฟรี**
⇒ **ข้อ 5 ในบล็อก "ก่อนบูต" คือด่านที่กันเรื่องนี้** — ผ่านข้อ 5 เมื่อไหร่ บูตได้เลย ไม่ต้องเทียบเลข commit กับอะไรอีก
`2200423` = `紅葉之鎚` Red leaves Hammer = **ตัวเดียวกับคลิปอ้างอิงของเจ้าของโปรเจกต์** ⇒ มีวิดีโอบอกอยู่แล้วว่า "ถ้าถูกหน้าตาแบบนี้"
`EQUIPMENT_BASE` มี drop model **925 จาก 974 แถว** (เทียบ `ITEM_MISC` มีแค่ **7 จาก 1,646 แถว** ⇒ ตารางเดิมผิดตารางสำหรับใบนี้)

### ✅ ประวัติรอบ 1104 (attended · 2026-08-24 22:40:13-23:33:23 +07:00 · คุณ Panya ขับ UI เอง) — **WIRE PASS / CLIENT PARTIAL**
> ผลเต็ม: `notes_to_chief\consumed\20260825_0015_GT045-RESULT-WIRE-EXACT-CLIENT-PLAYS-DROP-DUST-NO-ITEM-MODEL.md`
> `BOOT_COMMIT fc4010efa619690887e2dbe7511f5f128aeae1df` · guards v2 = PASS · CANON `670CE534…` ก่อน=หลัง · integrity ok · OPEN_SESSIONS 0
- **ชั้น wire = ✅ PASS เป๊ะทุกไบต์ (ปิดแล้ว ไม่ต้องพิสูจน์ซ้ำ):** trigger `X -8553.947 · Y -2579.689 · Z 186.000` ·
  near `= trigger +30.000` · far `= trigger +800.000` · **Y/Z = ของ trigger ทุกบิต** · label อย่างละ 1 ครั้ง
  (`…NEAR_ONCE` late 10.2 ms · `…FAR_ONCE` late 0.7 ms · 54 B ทั้งคู่) · trigger X ตรงเลข HUD ที่ผู้เล่นเห็น (`X:-8,553`)
- **ชั้น client-observable = 🟡 PARTIAL:** **ฝุ่นสีน้ำตาล "ของตกพื้น" ขึ้นจริงที่พิกัดที่ยิง อายุ ~0.45 s**
  (t=631.65 → 632.10 ในวิดีโอ · ภาพนิ่ง 5 ใบ `evidence_screens\GT045_1104_DROPDUST_t631p50s…t632p10s_20260824.jpg`)
  · ❌ **ไม่มีโมเดลไอเทม** · ❌ **ไม่มีป้ายชื่อลอย** · ❌ ไม่มีอะไรค้าง — ผู้สังเกตเดินไปยืนทับทั้งสองพิกัดแล้วกวาดกล้อง
  (NEAR คลาด 9/3 หน่วย · FAR คลาด X 0.1 หน่วย) ไม่เจออะไร
- **ต้นเหตุ (วัดแล้ว ไม่ใช่การเดา):** `2600001` = ITEM_MISC n_ID=1 · `n_ID_MODEL=0` **และ** `n_DROPMODEL_TYPE=0`
  ⇒ **ไคลเอนต์ไม่มีอะไรให้วาด ฝุ่นคือทุกอย่างที่มันวาดได้** ⇒ v3 เปลี่ยนเลขไอเทม (บล็อกบนสุด)
- 🆕 **ของแถมที่วัดได้และกลายเป็นกฎของ steps v3:** คุณ Panya **หมุนกล้องอย่างเดียว ไม่แตะปุ่มเดิน** แล้ว `TargetPosVital` ออก
  (HUD X/Y ไม่ขยับแม้แต่หน่วยเดียว) ⇒ **`Q`/`E` ยิง trigger ได้** ⇒ คำสั่งเดิม "ห้ามแตะปุ่มเดิน" ไม่พอ
- 🆕 **บั๊กเครื่องมือ — ✅ แก้แล้วฝั่งสะพาน 2026-08-25 ~09:1x (+07:00) · ไม่มีอะไรค้างให้ผู้เทสทำ:**
  `staged\1103_gt045_teardown_video.ps1:17` (และสำเนา `1105:17`) บรรทัด
  `$uri = 'file:' + ($runDb -replace '\','/') + '?mode=ro'` — `'\'` เป็น regex ไม่ถูกต้อง ⇒ จ็อบ exit 36 · DB1 อ่านไม่ได้
  **ที่ถูกคือ `-replace '\\','/'`** ⇒ แก้ทั้งสองไฟล์แล้ว (3496 → 3497 ไบต์ · ASCII ล้วน · จำนวน CRLF ไม่เปลี่ยน · ยืนยันด้วย grep หลังเขียน)
  🔴🔴 **คำวินิจฉัยเดิมของ chief ผิด — แก้แล้วตรงนี้ ห้ามอ่านฉบับเก่า** (จดหมาย `20260825_0915` §② · หน้าสะพานสแกน `staged\` ทุก `.ps1` ที่มี `mode=ro`)
  ฉบับเก่าเขียนว่า *"chief แก้ให้ไม่ได้ · ต้องแก้ที่ตัวสร้างเทมเพลตฝั่งสะพาน"* — **สั่งงานไม่ได้ เพราะไม่มีอะไรให้แก้ตรงนั้น**
  **[วัดแล้ว] เทมเพลตถูกอยู่แล้วทุกใบ:** `TEMPLATE_teardown_generic.ps1:800` ✅ · `1091_gt059_s1_boot_video.ps1:78` (เทมเพลตบูตที่ก๊อปทุกใบ) ✅ ·
  `1092` · `1108` · `1111` · `1113` · `1116` · `1119` ✅ ทั้งหมด — **ผิดแค่สองไฟล์คือ `1103` และ `1105` (ซึ่งเป็นสำเนาของ `1103`) เกิดจากมือตอนสร้าง `1103`**
  ⇒ **ถ้าผู้เทสไปตามหา "ตัวสร้างเทมเพลต" ตามใบฉบับเก่า จะเสียเวลาเปล่าและอาจแก้ของที่ถูกอยู่แล้วให้พัง**
  ⇒ **กฎที่ใช้แทน (ฉบับทนเวลา · R161-b): ก๊อปจาก `TEMPLATE_teardown_generic.ps1` เป็นหลัก ·
  ถ้าก๊อปจากจ็อบที่เป็นตัวเลข ต้องเปิดดูบรรทัด 17 ให้เห็น `-replace '\\','/'` ก่อนเสมอ · ห้ามก๊อปจาก `1103`/`1105`**
  *(`1116`/`1119` เป็นตัวอย่างที่ถูก ณ วันนี้ แต่เลขจ็อบเดินหน้าเรื่อย ๆ ⇒ ยึดชื่อเทมเพลต ไม่ใช่เลข)*
  ⚠️ **nonclaim ของหน้าสะพาน:** แก้ให้ regex ถูกเท่านั้น **ยังไม่ได้รันจ็อบ** ⇒ ยังไม่มีหลักฐานว่า teardown อ่าน DB1 ได้จริง — พิสูจน์ที่รอบ GT-045 ถัดไป
- 🆕 NPC `Navy Transfer` ที่โผล่ในเฟรมชุดเดียวกัน (`V134_P0_P30_P91_ISOLATED_INITIAL_READY` 517 B) **เป็นวัตถุของเราเอง
  ไม่ใช่ของลูท** — อยู่ ~`X -8,892` ห่างจุด NEAR ~368 หน่วยคนละทิศ · อย่าสับสนตอนอ่านวิดีโอ

### 🟡 บล็อกผลรอบแรก (2026-08-23 14:52-15:08 · ผลเต็ม: `notes_to_chief\20260823_1530_gt-results.md` §GT-045) — `[DONE: WIRE EXACT / CLIENT NO-RESULT]` ไม่ใช่ FAIL
- **ชั้น wire ผ่านเป๊ะตามดีไซน์ v1** · **แต่ geometry ของใบตาย:** ใบสั่ง v1 คาด spawn ที่ V135 `(-9239.9, -2830.0, 223.2)`
  แต่ spawn จริงคือ `(-8553.947265625, -2579.68896484375, 186.0)` ⇒ **ความผิดของดีไซน์เลน/ใบสั่ง (chief R124) ไม่ใช่ผู้เทส**
  ⇒ v2 เปลี่ยนพิกัดเป็นแบบอิง trigger (แก้เหตุนี้ถาวร · v3 ไม่แตะส่วนนี้)
- **ชั้น client = NO-RESULT (ไม่ใช่ผลลบ):** ภาพแรกหลัง trigger อยู่ที่ +3.560s ไม่มี continuous capture 0-3.56s
- **เกณฑ์ event `hyp_pf_032_ground_loot_bit08_pair_committed` count=0 = บั๊กใบสั่ง:** เซิร์ฟเวอร์จริงไม่ persist `state.events`
  ⇒ สังเกตไม่ได้โดยโครงสร้างในรัน attended · **ตัดออกจาก pass criteria แล้ว ห้ามเอากลับมาใส่**

### 🟡 ประวัติ R145 (รอบ unattended 2026-08-24 09:54-10:06 · Codex LOCAL) — WIRE PASS / CLIENT **NO-RESULT**
กล้องถูกชั้นไม้/ถังบังพื้นที่ข้างหน้า · computer-control สูญเสีย enumerate หน้าต่างช่วงท้าย ⇒ แยก "ไม่วาด" ออกจาก
"วาดนอกมุม/ถูก geometry บัง" ไม่ได้ · 🔴 ห้ามปิดเป็นผลลบ (รอบ 1104 แทนที่รอบนี้แล้ว)

**ที่มา:** ร่างผู้ช่วย `notes_to_chief\20260823_0805_GT-TICKET-DRAFT-ground-drop-and-pickup-direction.md`
(อ่านคู่กับ `notes_to_chief\20260823_0800_GROUND-DROP-FRAME-MEASUREMENT-pickup-is-not-contact.md`)
การวัดเฟรมพิสูจน์แล้วว่า: ของโผล่บนพื้นเป็นวัตถุ 3 มิติ + ป้ายชื่อลอย อยู่ 0.633 s แล้วหาย · ตอนหายไม่มีใครแตะ ·
ของหาย + บรรทัด `ได้รับ [Red leaves Hammer] * 1` เกิดเฟรมเดียวกัน

### สมมติฐาน (จาก GT-040 ท่อน A · ผ่าน re-derive ปฏิปักษ์ใน GT-042 — verify sha ก่อนพึ่งเสมอ)
`0x5F85B0` (บิต `0x08` / obj `+0x20`) = list แบบ dirty-mask · element ยาว `0x2C` ไบต์ · vtable `0xF313C4`
float 3 ตัวที่ `+0x1C/+0x20/+0x24` = ตำแหน่งในโลก · mask: `0x02`->`+0x14` tag `0x14` · `0x10`->ตำแหน่ง
(v1/v2/v3 ส่ง mask `0x12` = `0x10` พิกัด + `0x02` dword เท่านั้น — ฟิลด์อื่นของ element **เราไม่เคยส่งเลยสักรอบ**)

### objective (claim เดียว — **element 1 คือใบวัด · element 2 ไม่ใช่การทดลองที่สอง**)
**เมื่อ payload_dword ของ element ชี้ไอเทมที่ตารางบอกว่ามี drop model จริง (`2200423`) ไคลเอนต์วาด "โมเดลไอเทมบนพื้น"
ที่พิกัด trigger+30X หรือไม่**
🔴 **element 2 (`2200003` ที่ +800X) = ตัวคุมระยะ/นอกจอเท่านั้น** — มันต่างจาก element 1 **ทั้งเลขไอเทมและระยะ**
⇒ ผลลบของ element 2 **ตีความเดี่ยว ๆ ไม่ได้** · ห้ามใช้ element 2 ตัดสินอะไรก็ตามเกี่ยวกับไอเทมหรือฟิลด์

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)
- **P1 [คำทำนาย] — ถ้าสมมติฐาน "เลขไอเทมคือสาเหตุ" ถูก:** ที่ trigger+30X ขึ้น **โมเดลไอเทมวางบนพื้น** หน้าตาแบบค้อน
  (`Red leaves Hammer` เหมือนคลิปอ้างอิง) และ **คาดว่าค้างอยู่** ⇒ เดินไปยืนทับแล้วยังเห็น
- **P2 [คำทำนาย · positive control] — ฝุ่นสีน้ำตาลขึ้นอีกทั้งสองจุด** เหมือนรอบ 1104 (~0.45 s)
- **P3 [ตีความ · ความไม่แน่นอนที่ต้องพกไป] — ป้ายชื่อลอยอาจไม่ขึ้นถึงแม้โมเดลจะขึ้น** เพราะเราส่ง mask `0x12` เท่านั้น
  (ฟิลด์อื่นของ element ไม่เคยถูกส่ง) ⇒ 🔴 **"ไม่มีป้ายชื่อ" เดี่ยว ๆ ไม่ใช่ผลลบของใบนี้** — ตัวชี้ขาดคือ **โมเดล**
- **P4 [คำทำนาย] — ถ้าจอไม่ขึ้นโมเดลแต่ฝุ่นยังขึ้น:** สมมติฐาน "เลขไอเทมคือสาเหตุ" ถูกหักล้าง (ดูแถว D ของเมทริกซ์)

### 🔴 ก่อนบูต — resolve commit เขียว (ท่าเดียวกับ GT-041/GT-034 · รันเครื่องมือ ไม่ใช่ก๊อป SHA)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` (detached HEAD ถูกแล้ว)
- **exit 3** + `BOOT_COMMIT: NONE` ⇒ ห้ามบูต จดว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · **exit 2** = พาธผิด/git ล้ม
- 🔴 บรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ จดลงผลเสมอ
- 🆕 **R158: เครื่องมือยอมรับ commit ที่ tree ต่างจาก `main` ได้แล้ว ถ้าไฟล์ที่ต่างเป็นของที่เซิร์ฟเวอร์รันไม่ได้**
  (`docs/ tests/ reports/ drafts/ .github/ .claude/` + markdown ระดับบนสุด + ไฟล์ verifier ที่ระบุชื่อทีละไฟล์สองตัว) และมันจะ **พิมพ์รายชื่อไฟล์ที่ต่างออกมาเสมอ**
  ⇒ commit เอกสารของ chief ไม่ปิดหน้าต่างเทสอีกต่อไป
  · 🔴 **`tools/` นับเป็นโค้ด** เพราะ `tools\run_foundation_visible.ps1` **คือคำสั่งบูตเอง** (มันตั้ง `PYTHONPATH` และเลือก DB)
  · ถ้าต่างที่ `src/ scenarios/ current/ tools/ migrations/` **ยังปฏิเสธเหมือนเดิม**
  · 🔴 **เทียบกับ `main` ปัจจุบัน ไม่ใช่กับ merge commit** ⇒ ถ้า main ขยับหลัง merge ด้วย commit ที่แตะ `src/` มันจะปฏิเสธ ซึ่งถูกแล้ว
- **ยืนยันห้าข้อกับ `<SHA>` ที่จะบูตจริง (ต้องครบทั้งห้า — ข้อ 4/5 เป็นของใหม่ v3 และเป็นด่านกัน "บูตเลนเก่า"):**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "ground-loot-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/ground_loot_hypothesis_bit08_render.json && echo SCENARIO_PRESENT
git grep -n "x_offset" <SHA> -- src/pirateforce_foundation/ground_loot_hypothesis.py
git grep -c payload_dword <SHA> -- src/pirateforce_foundation/ground_loot_hypothesis.py scenarios/ground_loot_hypothesis_bit08_render.json
git grep -c -E 'payload_dword.?[=:] ?(2200423|2200003)' <SHA> -- src/pirateforce_foundation/ground_loot_hypothesis.py scenarios/ground_loot_hypothesis_bit08_render.json
git grep -n -E 'payload_dword.?[=:] ?2600001' <SHA> -- src/pirateforce_foundation/ground_loot_hypothesis.py scenarios/ground_loot_hypothesis_bit08_render.json
```

🔴🔴 **กฎตัดสินเมื่อ "ข้อความในใบ" กับ "ผลที่เครื่องมือพิมพ์ออกมา" ขัดกัน — อ่านก่อนทำห้าข้อ**
**ผลที่เครื่องมือพิมพ์ออกมาชนะเสมอ** · ใบนี้เป็นกระดาษที่เขียนไว้ล่วงหน้า เครื่องมืออ่านของจริง ณ วินาทีนั้น
⇒ ถ้าห้าข้อผ่านครบ **แต่มีประโยคไหนในใบสั่งห้ามบูต** ⇒ **บูตได้** แล้ว **จดความขัดแย้งนั้นลงผล** เพื่อให้ chief แก้ใบ
⇒ ถ้าห้าข้อไม่ผ่าน **แต่ใบบอกว่าพร้อมบูต** ⇒ **ห้ามบูต** — ห้าข้อคือด่านจริง ใบเป็นแค่คำอธิบาย
*(กฎนี้เพิ่มโดย R159 หลัง pf-adversary พบว่าใบฉบับก่อนหน้ามีประโยค "ห้ามบูต" ค้างอยู่สี่จุดพร้อมกับหัวข้อ 🟢 พร้อมบูต)*
1. ไฟล์คำตัดสินมี `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ (`success` = subset บน Actions ไม่ใช่ gate เต็ม)
2. `git grep` เจอ flag จริง — **ห้ามใช้ `--help` เป็นหลักฐาน** (คืน 0 บรรทัดผ่านสะพาน — บทเรียนรอบใหญ่ #7 ข้อ 6)
3. เห็นคำว่า `SCENARIO_PRESENT`
4. เจอ `x_offset` (กัน v1 · v1 ไม่มีคำนี้)
5. 🔴 **สามคำสั่ง ต้องผ่านครบ (ฉบับ R161-b — เล็ง `.py` ด้วย + มีตัวคุมเชิงบวก)**

   🔴🔴 **อ่านก่อน: ทุกบรรทัดที่พิมพ์ออกมา ขึ้นต้นด้วย `<SHA>:` เสมอ** เพราะเราใส่ rev ลงในคำสั่ง
   ⇒ หน้าตาจริงคือ `4745635:scenarios/…json:2` **ไม่ใช่** `scenarios/…json:2`
   *(ฉบับแรกของ R161 เขียนผิดตรงนี้ — `pf-adversary` จับได้ · ถ้าผู้เทสเทียบกับสตริงที่ไม่มี `<SHA>:` จะเห็นว่า "ไม่ตรง" แล้วปฏิเสธ tree ที่ถูกต้อง)*

   - **5-control (ตัวคุมเชิงบวก — พิสูจน์ว่า "คำสั่งรันจริง" ไม่ใช่ "รันแล้วไม่เจอ")**
     ต้องได้ **สองบรรทัด**: `<SHA>:scenarios/…json:3` และ `<SHA>:src/…ground_loot_hypothesis.py:7`
     🔴 **ถ้าตัวนี้ไม่พิมพ์อะไรเลย ⇒ ห้ามตีความว่า "commit ผิด"** — แปลว่า **คำสั่งไม่ได้รัน** (พิมพ์ผิด · quote เพี้ยน · path ผิด · ไม่ได้อยู่ในโฟลเดอร์ repo)
     หรือ commit นั้นไม่มีเลนนี้เลย · **ทั้งสองกรณี = หยุด แล้วแปะสิ่งที่คอนโซลพิมพ์มาทั้งดุ้น ห้ามเดา**
   - **5a** ต้องได้ **สองบรรทัด และเป็น `:2` ทั้งคู่** — `<SHA>:scenarios/…json:2` · `<SHA>:src/…ground_loot_hypothesis.py:2`
     🔴 **อ่านเลขรายไฟล์ ห้ามรวมเป็นผลบวก** — `json:4 / py:0` ก็บวกได้ 4 เหมือนกันแต่ผิด
     *(`git grep -c` **ไม่พิมพ์บรรทัดของไฟล์ที่นับได้ 0** ⇒ "ได้สองบรรทัด" คือสัญญาณจริง · วัดแล้ว)*
   - **5b** ต้อง **ไม่พิมพ์อะไรเลย** · **เห็น `2600001` = เลนเก่า ⇒ ห้ามบูต**

   **[วัดแล้ว R161-b · ครบห้า commit · รันจริงทั้งสามคำสั่ง]**

   | commit | 5-control | 5a | 5b | คำตัดสิน |
   |---|---|---|---|---|
   | `4745635` (merge PR #28) | `json:3` `py:7` | `json:2` `py:2` | ว่าง | ✅ บูตได้ |
   | `e99ac0d` (resolver คืนตัวนี้) | `json:3` `py:7` | `json:2` `py:2` | ว่าง | ✅ บูตได้ |
   | `4f31956` (v2) | `json:3` `py:7` | ว่าง | 4 บรรทัด (`json:16,22` · `py:157,162`) | 🔴 ปฏิเสธถูกต้อง |
   | `1343305` (v1) | `json:3` `py:7` | ว่าง | 4 บรรทัด (`json:16,22` · `py:145,152`) | 🔴 ปฏิเสธถูกต้อง |
   | `7f893b8` (ไม่มีเลนเลย) | **ว่าง** | ว่าง | ว่าง | 🔴 หยุด — ตัวคุมตก ⇒ ไม่ใช่ "commit ผิด" แต่ "ไม่มีเลนนี้ในต้นไม้" |

   🔴 **ใช้ single quote `'…'` เท่านั้น ห้ามเปลี่ยนเป็น double quote** — สะพานเป็น **PowerShell 5.1** ซึ่ง
   ① ใช้ backtick ไม่ใช่ `\` เป็นตัว escape ⇒ `"…\"…"` จะ **จบสตริงกลางคัน** แล้วค้างที่ `>>`
   ② ไม่ escape `"` ที่ฝังอยู่ตอนส่งอาร์กิวเมนต์ให้ `git.exe` ⇒ regex ถูกหั่นเป็นสองชิ้น
   ⇒ **regex ฉบับนี้จึงไม่มีอักขระ `"` อยู่เลย** (ใช้ `.?` แทน `"?`) — วัดแล้วว่าให้ผลเท่ากันเป๊ะทั้งห้า commit
   และ **ไม่แมตช์** สตริง nonclaim `payload_dword_is_an_item_template_id` · field decl `.py:198` · `_EXPECTED` `.py:272/280`
- **ไม่ครบห้าข้อ = ห้ามบูต** จดว่า "รอ merge ไม่ได้รอผู้เทส" แล้วไปทำใบอื่น
  · **ครบห้าข้อ = บูตได้** (ดูกฎตัดสินความขัดแย้งข้างบน)

   ---
   🔴 **ประวัติการแก้ข้อ 5 — อ่านไว้กันเขียนด่านแบบเดิมซ้ำ (chief R159 · pf-adversary จับสองรอบ)**

   **ฉบับ R158 (ผลลบลวง):** `git grep … -e 2600001 … -- …ground_loot_hypothesis.py …json` + กฎ "ต้องเหลือ 0 บรรทัด"
   รันจริงบน `4745635` (เลน v3 ที่ merge แล้ว) **ยังเจอ `2600001` สองบรรทัด** คือ `ground_loot_hypothesis.py:50` และ `:79`
   ซึ่งเป็น **คำบรรยายใน docstring ที่เล่าประวัติ** ไม่ใช่ค่าที่ส่งออกสาย ⇒ **สั่งไม่บูตใบที่พร้อมบูตแล้ว**

   **ฉบับแก้ครั้งแรกของ R159 (ยังพัง สองแบบ):** `git show <SHA>:…json | grep -n "payload_dword"`
   ① คำสั่งนั้นคืน **สามบรรทัด ไม่ใช่สอง** — บรรทัด 41 คือสตริง nonclaim `"payload_dword_is_an_item_template_id"`
      ⇒ กฎ "ต้องเห็นสองบรรทัดเท่านั้น" **ตกเพราะสตริงบรรยายอีกตัวหนึ่ง — ความผิดพลาดทรงเดียวกับที่กำลังแก้อยู่พอดี**
   ② 🔴 **`| grep` ใช้ไม่ได้บนสะพาน** — คอนโซลเป็น **PowerShell 5.1** และ `grep` ไม่ได้อยู่ใน `PATH` โดยปริยาย
      (ทั้งไฟล์นี้ 606 KB ใช้ `git grep` 14 ครั้ง และ **ไม่มี `| grep` ที่ไหนเลย** — บรรทัดนั้นเป็นบรรทัดเดียว)

   **ฉบับ R159 (ใช้ได้ แต่เล็งไม่ครบ — ถูกแทนแล้ว):** `git grep -n "\"payload_dword\": " <SHA> -- …json`
   ใช้ `git grep` ไม่มีไปป์ และจับ colon-space จึงไม่โดนสตริง nonclaim ⇒ ได้ 2 บรรทัดตามต้องการ
   **แต่มันเล็งเฉพาะไฟล์ JSON ซึ่ง *ไม่ใช่* ไฟล์ที่ส่งไบต์ออกสาย**

   **ฉบับปัจจุบัน (R161 · หลังหน้าสะพานค้าน + `pf-static-re` วัดซ้ำ):** เล็ง **สองไฟล์** และแยกเป็น 5a/5b
   🔴 **เหตุผลที่ `.py` ต้องอยู่ในสโคป — เขียนไว้ตรงนี้เพื่อกันคนแก้กลับไปเล็ง JSON อย่างเดียวอีก:**
   **[วัดแล้ว]** ค่าที่ประกอบเป็นเฟรมมาจาก `ground_loot_hypothesis.py:211/216` (`_NEAR`/`_FAR`) ผ่าน
   `:391 legacy.u32tag(0x14, element.payload_dword)` · ไฟล์ JSON **ไม่เคยถูกอ่านเป็นค่า**
   (`:361` โหลด → `:372` เทียบ exact กับ `_EXPECTED` → `:377` **คืนโปรไฟล์แช่แข็งของโมดูลเอง** ไม่ได้พาค่าจาก JSON ไปไหนเลย
   · `runtime.py:395` ตรวจซ้ำด้วย **identity** `value is profile`)
   ⇒ ด่านที่เล็ง JSON อย่างเดียวเป็น **ตัวแทน (proxy)** ไม่ใช่ตัววัดตรง
   ⚠️ **ที่มันยังไม่เคยพลาดจนวันนี้ เพราะ invariant ที่ใบไม่เคยเขียนไว้:** `_EXPECTED` สร้างจาก `_NEAR`/`_FAR` เอง (`:272/280`)
   ⇒ ถ้าสองไฟล์ไม่ตรงกัน **บูตตายเสียงดังที่ `app.py:149`** (`ground_loot_scenario_exceeds_allowlist`) ไม่ใช่ยิงค่าผิดออกสายเงียบ ๆ
   ⇒ ราคาของการเล็งพลาดคือ **เผารอบ attended ทิ้งพร้อม crash** ไม่ใช่ผลเทสที่ผิด — **แต่ก็ยังเป็นราคาที่ไม่ต้องจ่าย**
   🔴 **และ invariant นั้นพังได้:** ถ้าวันหนึ่งมีใครเขียนเลขตรง ๆ ลง `_EXPECTED` แทนการอ้าง `_NEAR`/`_FAR`
   ด่านที่เล็ง JSON อย่างเดียวจะกลายเป็น **ด่านลวงเงียบของจริงทันที** ⇒ นี่คือเหตุผลที่ไม่รอให้ถึงวันนั้น
   **[วัดแล้ว] ประวัติสองไฟล์นี้ไม่เคยแยกกันเลย:** ทั้งคู่ถูกแตะโดย **commit เดียวกันสามใบ** (`1343305` · `4f31956` · `e99ac0d`)
   สแกน `git rev-list --all` ทั้งสอง path แล้ว **ไม่มี tree ไหนในประวัติที่สองไฟล์ไม่ตรงกัน** — ความเสี่ยงนี้จึงเป็น *เชิงโครงสร้าง* ไม่ใช่เคสที่เคยเกิด

   🔴 **ข้อเสนอของหน้าสะพาน (จดหมาย `20260825_0915`) ถูกรับ "เกือบทั้งหมด" — สามจุดที่ถูกแก้ก่อนเอาลงใบ:**
   ① `| awk -F: '{s+=$NF} END{print s}'` — **ไปป์แบบยูนิกซ์ ซึ่งใบนี้ห้ามไว้เองสองบรรทัดข้างบน** (สะพาน = PowerShell 5.1)
      · และ `awk` จะมีใน PATH หรือไม่ **ไม่มีใครวัดได้จากคลาวด์** ⇒ ตัดทิ้ง ใช้ `git grep -c` เปล่า ๆ ซึ่งพิมพ์ `json:2`/`py:2` อยู่แล้ว
   ② **[วัดแล้ว] `END{print s}` พิมพ์บรรทัดว่าง ไม่ใช่ `0` เมื่อไม่มีผลลัพธ์** (ยืนยันด้วย `od -c` บน `4f31956`)
      ⇒ ผู้เทสที่ถูกบอกว่า "ต้องได้ 4" จะเห็น **ความว่างเปล่า** ซึ่งแยกจาก "เครื่องมือพัง" ไม่ออก
   ③ **ผลบวก = 4 ไม่ได้แปลว่าไฟล์ละ 2** — `json:4 / py:0` ก็ได้ 4 ⇒ ต้องอ่านเลขรายไฟล์
   ⇒ **บทเรียนซ้ำรอยเดิม: ด่านที่ "สรุปเป็นตัวเลขเดียว" ทำให้ความผิดปกติหายไปในผลรวม** — ให้เครื่องมือพิมพ์รายไฟล์เสมอ

   🔴 **[วัดแล้ว R161] อย่าเขียน `origin/main` เป็นตัวแทน SHA ในใบเด็ดขาด**
   ตอนตรวจรอบนี้ `origin/main` ของ clone บนคลาวด์ **ค้างอยู่ที่ `7f893b8` (2026-08-20)** ซึ่ง **ไม่มีเลนนี้อยู่เลย**
   จนกระทั่งสั่ง `git fetch` ⇒ **สองเครื่องไม่เห็น `origin/main` ตรงกัน ณ เวลาเดียวกัน**
   ⇒ ใบต้องพิน SHA (`4745635`) เสมอ · ส่วน `pf_resolve_green_boot.py` ปลอดภัยเพราะมันมี `--fetch` ของตัวเอง

   🔴 **บทเรียนที่ต้องใช้กับด่านทุกตัวที่จะเขียนต่อจากนี้ (แก้ถ้อยคำ R161-b — ฉบับเดิมขัดกับตัวเองและอันตราย):**
   ~~"ด่านตรวจค่าต้องเล็งไฟล์ที่เป็นข้อมูลล้วน (JSON/TSV)"~~ ❌ **ถอนประโยคนี้**
   มันคือเหตุผลที่ R159 หด scope ลงเหลือ JSON อย่างเดียว แล้วกลายเป็นด่านตัวแทน (ดูบล็อกเหตุผลข้างบน)
   ✅ **ฉบับที่ถูก: ด่านตรวจค่าต้องเล็ง "ไฟล์ที่ค่านั้นถูกใช้จริง" — ไปดูให้แน่ว่าอันไหน แล้วเล็งให้ครบทุกอัน**
   ส่วนที่ยังจริงและเป็นเหตุผลตั้งต้นของบทเรียนนี้: **ต้องแมตช์ให้แคบพอที่จะไม่โดนสตริงบรรยาย**
   (เลนพวกนี้ **บังคับ** ให้เขียน provenance/nonclaim ลงไฟล์อยู่แล้ว ⇒ grep กว้าง ๆ จะโดนคำบรรยายเสมอ)
   และ 🔴 **ห้ามใช้ท่อ shell แบบยูนิกซ์ในใบเทส · ห้ามใช้ double quote รอบ regex** — สะพานเป็น PowerShell 5.1
   🆕 **และข้อที่สาม ซึ่งใบนี้เพิ่งเรียนแบบเจ็บ ๆ: ด่านทุกตัวต้องมีตัวคุมเชิงบวก**
   *"ไม่พิมพ์อะไรเลย"* ต้องแยกให้ออกระหว่าง **"รันแล้วไม่เจอ"** กับ **"ไม่ได้รัน"**
   ⇒ ถ้าด่านไหนยังแยกไม่ออก **มันจะคืน `ห้ามบูต` จากเครื่องมือที่ไม่เคยเริ่มทำงาน** — สามรอบที่ผ่านมาเป็นแบบนี้ทุกครั้ง

   ⚠️ **หมายเหตุความจริงที่ต้องไม่เข้าใจผิด (ยังจริงทุกคำ · ตอนนี้ข้อ 5 เล็งครบทั้งสองไฟล์แล้ว):**
   ไฟล์ scenario **ไม่ใช่ "แหล่งความจริงของ payload"** — `ground_loot_hypothesis.py:126,355-357` เขียนไว้ตรง ๆ ว่ามันเป็น
   **permission token ไม่ใช่แหล่งค่า** · ค่าจริงที่ประกอบเป็นเฟรมอยู่ใน `_NEAR`/`_FAR` (`:209-218`) และออกสายที่ `:391`
   · ไฟล์ JSON ถูกเทียบกับ `_EXPECTED` แบบ exact (`:372`) และ **ล้มทั้งบูตถ้าไม่ตรง**
   🔴 **ห้ามอ่านย่อหน้านี้เป็น "แก้ JSON แล้วสายจะเปลี่ยนตาม" — มันจะไม่เปลี่ยน มันจะพังตอนบูตแทน**
   🆕 **ด่านชั้นที่สองที่คุ้ม dword อยู่แล้วโดยที่ไม่มีใครสังเกต (พบโดย `pf-static-re` R161):** masked-template sha256 (`:480-489`)
   มาสก์ **เฉพาะช่วงพิกัด** `[30:34]/[35:39]/[40:44]` ⇒ **ไบต์ของ payload dword อยู่ในช่วงที่ถูกพิน**
   ⇒ แก้ค่าฝั่ง `.py` โดยไม่ re-derive พิน จะได้ `ground_loot_frame_drift` ทันที
   ⇒ **สี่ค่า masked-sha ที่ผู้เทสแปะกลับมา คือสิ่งเดียวในรอบที่อ่าน "ไบต์ที่ออกจริง"**
   🔴🔴 **แต่มันเป็น "ใบเสร็จ" ไม่ใช่ "ด่าน" — ห้ามเอามาแทนข้อ 5 เด็ดขาด** (`pf-adversary` จับฉบับแรกของ R161 ที่เขียนผิดตรงนี้)
   เหตุผล: การเทียบ sha เกิดขึ้นกับ **ค่าคงที่ในโมดูลของ commit เดียวกันนั้นเอง**
   ⇒ บน `4f31956` พินคือ `915331D5…` ซึ่ง **ตรงกับไบต์ `2600001` ของ commit นั้นพอดี ⇒ ไม่มี drift ให้ raise เลย**
   ⇒ มันกลายเป็นตัวจับ "บูตผิด commit" **ก็ต่อเมื่อ** เอาไปเทียบกับค่าที่พินไว้ในใบ (บล็อกเกณฑ์ชั้น wire)
   ซึ่งเกิด **ตอนจบรอบ** — และรอบ attended เป็น **one-shot** ⇒ **ถ้ารอถึงตอนนั้น รอบก็ถูกเผาไปแล้ว**
   ⇒ **ลำดับที่ถูก: ข้อ 5 กันก่อนบูต · masked-sha ยืนยันหลังบูต** ทำหน้าที่คนละอย่าง ไม่แทนกัน

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-045_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt045.sqlite3
```
- เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง** (canonical เปิดอ่านไม่ได้ตลอดรอบ)
- ตำแหน่งตัวละคร **รีเซ็ตกลับจุดเกิดทุกบูต** (สำเนา DB ใหม่ทุกครั้ง) — พิกัดอิง trigger จึงไม่พังเพราะเรื่องนี้

### server args (เป๊ะ — ชื่อจริง ยืนยันแล้ว R124 · v3 ไม่เปลี่ยน flag/ชื่อ scenario)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt045.sqlite3 --ground-loot-hypothesis-scenario scenarios\ground_loot_hypothesis_bit08_render.json
```
- 🔴 **รอบนี้บูตเลนเดียว ห้ามรวมเลนอื่น** ถึงแม้ allow-list (คำเคาะ Panya 1831 §① · ขยาย 2120 §②) จะยอมให้รวมได้แล้ว —
  ใบนี้ตัดสินด้วยตา ถ้ามีเลนอื่นวิ่งด้วยจะแยก "ใครวาด" ไม่ออก = NO-RESULT
- หัวหน้าต่าง console ของ server จะขึ้น mode `ground-loot-hypothesis` — ใช้เช็คว่าบูตถูกโหมด
- ⚠️ **ไม่มี chat trigger และไม่มีปุ่มยิง** — เฟรมออกเองที่ TargetPos แรกหลัง runtime ack ครั้งเดียวต่อเซสชัน
  🔴 **TargetPos แรกไม่ได้ออกตอนเข้าแมพ — ออกตอนผู้เล่นขยับ/หมุนตัวครั้งแรก** ⇒ **ผู้เทสคือคนคุมจังหวะยิงเอง**
  · ตัวอักษรตอนช่องแชตไม่โฟกัส = hotkey ⇒ ใช้แค่ `W/A/S/D`, `Q/E`, `spacebar`

### steps
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบตามบล็อก db ·
🆕 **teardown (แก้โดย R161 · จดหมาย `20260825_0915` §②) — เรียงตามลำดับที่ทนต่อเวลา:**
① **ก๊อปจาก `TEMPLATE_teardown_generic.ps1`** (ชื่อเสถียร · หน้าสะพานวัดแล้วว่าบรรทัด `:800` ถูกอยู่แล้ว)
② ถ้าจะก๊อปจากจ็อบที่เป็นตัวเลข ให้ **เปิดดูบรรทัดที่ 17 ก่อนเสมอ ต้องเห็น `-replace '\\','/'` (backslash สองตัว)**
③ 🔴 **ห้ามก๊อปจาก `1103`/`1105` ไม่ว่ากรณีใด**
*(เลขจ็อบ `1116`/`1119` ที่เคยเขียนไว้เป็นตัวอย่างที่ถูก ณ 2026-08-25 — **แต่เลขจ็อบเดินหน้าเรื่อย ๆ**
⇒ อย่ายึดเลข ให้ยึด **ชื่อเทมเพลต + การตรวจบรรทัด 17** ซึ่งไม่เน่าตามเวลา)*
*(บั๊ก `-replace '\','/'` → exit 36 ถูกแก้ที่ต้นทางแล้วทั้ง `1103` และ `1105` เมื่อ 09:1x +07:00 · **ไม่ต้องแก้เทมเพลตเองอีก** —
คำสั่งฉบับเก่าที่ให้ไปแก้ตัวสร้างเทมเพลตถูกถอนแล้ว เพราะเทมเพลตทุกใบถูกอยู่แต่แรก)*
🔴 **ถ้ารอบนี้ยังได้ exit 36 อีก ⇒ อย่าเดาเอง** ให้แนบบรรทัดที่ 17 ของไฟล์ teardown ที่ใช้จริงมาทั้งบรรทัดในผล
1. **เปิด server ก่อน client เสมอ** (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client) —
   client ที่บูตโดยไม่มีเซิร์ฟเวอร์ **ตายเองใน ~3.5 นาที** · 🔴 **ถ้าต้องฆ่า client กลางคัน ให้รีสตาร์ต server ก่อนเปิด client ใหม่เสมอ**
   (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่ "connecting" ตลอดกาล)
2. เปิด client (`Invoke-CimMethod Win32_Process Create`) → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร
   → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
3. เข้าแมพ เห็น HP/minimap/ชื่อแมพ → 🔴 **ห้ามแตะปุ่มเดิน `W/A/S/D` และห้ามหมุนกล้อง `Q`/`E` เด็ดขาด**
   (**วัดแล้วรอบ 1104: การหมุนกล้องยิง `TargetPosVital` เองได้ ทั้งที่ HUD X/Y ไม่ขยับ** — ข้อห้ามเก่าที่เขียนว่า
   "เลี่ยงการหมุนกล้อง" ไม่พอ ต้องเป็น "ห้าม") → **ถ่าย G0** ให้เห็น X/Y บน HUD และพื้นที่รอบตัว
   ⚠️ ถ้าเฟรมเผลอออกก่อนกำหนด **รอบไม่เสียถ้ากล้องกำลังอัดอยู่** — พิกัดอิง trigger เสมอ · แต่ถ้าไม่ได้อัด = **NO-RESULT ทันที**
   (ฝุ่น 0.45 s + โมเดลที่อาจโผล่แล้วหาย = ตามเก็บย้อนหลังไม่ได้) ⇒ **ให้เริ่มอัดก่อนเข้าแมพเสร็จเสมอ**
4. **จังหวะยิง (หัวใจของใบ — สิ่งที่ต้องเห็นคือ "ช่วง 2 วินาทีแรก" ไม่ใช่สภาพพื้นหลังจากนั้น):**
   ① **เริ่มอัดวิดีโอ/continuous capture ก่อน** หันกล้องไปทาง +X (ทางที่ของจะโผล่ · ทาง `Navy Transfer`) —
      🔴 **ต้องหันให้เสร็จตั้งแต่ก่อนขั้นนี้** เพราะการหมุนกล้องเองก็เป็น trigger (ถ้าหมุนแล้วเฟรมออกเลย ก็ถือว่าเริ่มขั้น ② แล้ว)
   ② **กด `W` สั้นที่สุด (~120ms) หนึ่งครั้ง** — เฟรมทั้งสองออกที่ TargetPos ของการขยับครั้งนี้ (ห่างกัน 0.10s)
   ③ 🔴 **ตาต้องอยู่ที่จอ ณ วินาทีนั้น** — รอบ 1104 ฝุ่นมีอายุ **~0.45 s** (t=631.65→632.10) ⇒ **เดินไปดูทีหลังไม่มีวันเจอ**
      · **โมเดล** (ถ้าถูกวาด) **คาดว่าค้าง** ⇒ อันนั้นเดินไปหาทีหลังได้ · **สองอย่างนี้ต้องรายงานแยกกันเสมอ**
   ④ **อัดต่อเนื่องอย่างน้อย 5 วินาทีหลังกด** แล้วอย่าเพิ่งขยับ — ดูพื้นนิ่ง ๆ 3 วินาที ว่ามีอะไรค้างอยู่ไหม
   ⚠️ `W` 120ms เลื่อน ~51.6 หน่วย ⇒ **trigger X ≈ X(G0)+~50 ไม่ใช่ X(G0)** · **จุดใกล้ = X(trigger)+30 · จุดไกล = X(trigger)+800 ·
   Y/Z ของ trigger** — ค่า trigger เป๊ะอ่านจาก **hexdump ของเฟรม TargetPos ใน raw GAME log บรรทัดก่อน `SENT …NEAR_ONCE`**
   (**ห้ามใช้ "X ตอนเข้าแมพ" หรือ HUD เป็นฐานคำนวณ**) ระหว่างเทสใช้ "HUD หลังหยุด +30" นำทางได้ แล้วยืนยันเลขจริงจาก log ตอนเขียนผล
   → ถ่าย **G1** มุมที่เห็น (หรือมุมที่ควรเห็นแล้วไม่มี)
5. **เดินเข้าไปยืนทับจุดใกล้** (~30 หน่วยทาง +X จากจุดที่หยุด) → ถ่าย **G1b** ระยะใกล้ + **กวาดกล้อง 360° ที่จุดนั้น** —
   นี่คือขั้นที่ตัดสิน "โมเดลค้างอยู่ไหม" (รอบ 1104 ทำขั้นนี้ครบและได้ผลลบที่เชื่อถือได้ — ทำแบบเดียวกัน)
6. **จุดไกล (X(trigger)+800 · Y เดิม):** เดินต่อไปทาง +X จนถึง → ถ่าย **G2** + กวาด 360°
   🔴 **จดว่านี่คือตัวคุม ไม่ใช่ผล** — ดูเมทริกซ์ชั้น (2)
7. บันทึกแยกสามอย่างเป็นภาษาคน: **(ก) ฝุ่นขึ้นไหม กี่วินาที · (ข) โมเดลขึ้นไหม ที่ element ไหน ค้างหรือหาย ·
   (ค) ป้ายชื่อลอยขึ้นไหม** ⚠️ เซิร์ฟเวอร์เรา **ไม่เคยส่งเฟรมลบ/หมดอายุ** — ของหายเอง = พฤติกรรม client ล้วน
8. ออกจากเกม: **X** มุมขวาบน (ตรวจก่อนว่าหน้าต่างแอปตัวเองไม่บังปุ่ม X) → dialog ยืนยัน → ปุ่มซ้าย
9. ปิด server เก็บ raw GAME log + console out/err → `PRAGMA integrity_check;`
10. **teardown เสมอ** แม้เลิกกลางคัน/แม้รอบจบเพราะคนเลิกเล่น (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 —
    เพดานยกจาก 180 เมื่อ 2026-08-20 · `TEMPLATE_teardown_generic.ps1:135` · ใช้ `staged\TOOL_stop_stale_server.ps1`
    สำหรับแท่นที่ถูกทิ้งข้ามชั่วโมง)
11. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม

### pass criteria — สองชั้น แยกกันเด็ดขาด
**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ · pin แบบ masked template — 🆕 pin ทั้งสี่ re-derive ใหม่รอบ R158 เพราะเลขไอเทมเปลี่ยน)**
- 🔴 **สถานะของชั้นนี้เปลี่ยนบทบาทแล้ว:** รอบ 1104 พิสูจน์ชั้นนี้จบไปแล้ว ⇒ ในรอบ v3 ชั้นนี้ **ไม่ใช่คำถามที่เปิดอยู่
  แต่เป็นด่านยืนยันว่าบูตเลนถูก** · **wire ไม่ตรง pin = ยกเลิกรอบ (NO-RESULT ทางเทคนิค) ห้ามอ่านจอเป็นผลใด ๆ**
- raw GAME log มี **สองเฟรม** (เฟรมละ element เดียว · ใกล้ก่อน ไกลตาม 0.10s) · **pc 44 ไบต์ · frame 54 ไบต์**
- **masked sha256 pin (mask = ไบต์พิกัดเท่านั้น · pc `[30:34]+[35:39]+[40:44]` · frame = span เดียวกันเลื่อน `+10` คือ
  `[40:44]+[45:49]+[50:54]` · zero ไบต์เหล่านั้นก่อน hash):**
```
near_pc_template_sha256      F9875639513F38E0D2603A53137D205AF47246447102B431665B27AE23BD4576
far_pc_template_sha256       159DD1AB3074519EF95821DE6953697A03C035F35804024F8CD27FFFD22E39D7
near_frame_template_sha256   A67230FCC80A619F0ADBD35F99332DC3597768A28C603368D41D8DD0192E7902
far_frame_template_sha256    6B0F7FA8B3685914B68503891A5E4CCCD988278B93F8BF72E3C2FB772EE33B1B
```
  (ที่มา: chief R158 · re-derive ทั้งสี่ตัวรอบนี้ · verify ด้วยการ rebuild struct อิสระ · ความยาว/ขอบเขต mask **ไม่เปลี่ยน** จาก v2)
- **ไบต์ dword ที่เปลี่ยนจาก v2 (ตรวจตาเปล่าได้ในhexdump):** `2200423` = `0x00219367` ⇒ ไบต์ `67 93 21 00` ·
  `2200003` = `0x002191C3` ⇒ ไบต์ `c3 91 21 00` · (v2 คือ `2600001` = `0x0027AC41` ⇒ `41 ac 27 00`)
  🔴 **ถ้าไบต์กับ sha ขัดกัน ให้เชื่อ sha แล้วหยุดรายงาน**
- **เกณฑ์พิกัด:** decode f32 จาก 12 ไบต์นั้นแล้วต้องได้ **ใกล้ = trigger+30X · ไกล = trigger+800X · Y/Z = ของ trigger เป๊ะ**
  โดย trigger = TargetPos แรกหลัง runtime ack (อ่านจาก raw GAME log เอง) — เทียบที่ความละเอียด f32
- action labels ฝั่ง server: `GROUND_LOOT_BIT08_RENDER_NEAR_ONCE` แล้ว `GROUND_LOOT_BIT08_RENDER_FAR_ONCE`
  อย่างละ 1 ครั้ง · เก็บ hexdump ทั้งไฟล์ **ห้ามลบ**
  🔴 **เกณฑ์ event `hyp_pf_032_ground_loot_bit08_pair_committed` ถูกตัดออกถาวร (R127):** เซิร์ฟเวอร์จริงไม่ persist `state.events`
- `sessions`: `count(*) WHERE selected_character_id IS NOT NULL` +1 ต่อการเข้าเกมหนึ่งครั้ง · `PRAGMA integrity_check` = `ok` ·
  `lease_generation` ไม่ถอยหลัง · sha256 canonical ก่อน-หลังตรงกัน · run-copy เท่านั้น canonical ไม่ถูกเปิด
- **ชั้นนี้ตอบไม่ได้:** จอวาดอะไร (การมีเฟรมออกไม่พิสูจน์ว่าไคลเอนต์วาด) ⇒ **ห้ามอ้างชั้นนี้แทนชั้น (2)**

**ชั้น (2) client-observable (ต้องมีคนหน้าจอ · 🔴 ชั้นนี้เป็น "เมทริกซ์การอ่าน" ไม่ใช่ ผ่าน/ไม่ผ่าน)**
หลักฐานที่ต้องมี: วิดีโอต่อเนื่องคลุมตั้งแต่ก่อนกด `W` ถึง +5s · ภาพ **G0/G1/G1b/G2** อ่านค่า X/Y ได้ทุกใบ ·
คำตอบเป็นภาษาคนสามช่องแยกกัน: **ฝุ่น** / **โมเดล** / **ป้ายชื่อ** × **element 1** / **element 2**

🟢 **ตัวคุมบวก (positive control) — ของใหม่ที่ใบนี้ไม่เคยมี:** รอบ 1104 พิสูจน์แล้วว่าเลนนี้ทำให้ไคลเอนต์
**เล่นเอฟเฟกต์ฝุ่น "ของตกพื้น" ที่พิกัดที่เราส่ง** ⇒ ในรอบ v3 **ฝุ่นคือหลักฐานว่า transport + เส้นทางของตกพื้นยังทำงาน**
- **ฝุ่นขึ้น** ⇒ ท่อทั้งเส้นดี ⇒ ผลเรื่องโมเดลอ่านได้เต็มปาก (ทั้งบวกและลบ)
- 🔴 **ฝุ่นไม่ขึ้นเลย** ⇒ **มีอะไรถอยหลัง — รอบนี้เป็น NO-RESULT ไม่ใช่ผลลบ** · ห้ามเขียนว่า "ไม่วาด" ·
  ให้ตรวจ: บูตถูก commit ไหม (ห้าข้อ) · label ออกครบไหม · วิดีโอคลุมวินาที trigger จริงไหม (รอบ 1104 ผู้ช่วยเคยหาผิดช่วง
  แล้วรายงาน "ไม่เจอ" ทั้งที่มี — ด่าน **G1**: ห้ามสรุป "ไม่มี" จากการค้นช่วงเดียว/แหล่งเดียว) แล้วรันใหม่

**เมทริกซ์การอ่าน (element 1 = ใบวัด · element 2 = ตัวคุมระยะ/นอกจอ)**
| # | E1 (+30X · 2200423) | E2 (+800X · 2200003) | คำตัดสินของใบ | อนุญาตให้สรุปว่า | 🔴 **ไม่** อนุญาตให้สรุปว่า |
|---|---|---|---|---|---|
| **A** | มีโมเดล | มีโมเดล | ✅ **ปิดครึ่ง client-observable เป็น PASS** | ไคลเอนต์วาดวัตถุพิกัดโลกจาก wire ของเราได้จริง · สาเหตุที่รอบ 1104 ไม่มีโมเดลคือ payload ชี้ไอเทมที่ไม่มี drop model (ยืนยันแล้ว) · ปลด **ครึ่ง "มีวัตถุวาดจริง"** ของเงื่อนไข (ข) ใน GT-060 | ❌ ว่าบิต `0x08` = "รายการวัตถุลูทบนพื้น" ในความหมายเต็ม · ❌ ว่ามี entity อยู่จริง/คลิกได้/หยิบได้ · ❌ ว่าฟิลด์ไหน (`n_ID_MODEL` vs `n_DROPMODEL_TYPE`) เป็นตัวขับ · ❌ ตัวเลข culling ใด ๆ |
| **B** | มีโมเดล | ไม่มี | ✅ **ปิดครึ่ง client-observable เป็น PASS เท่าแถว A** (คำตัดสินมาจาก E1 อย่างเดียว) | เท่าแถว A | ❌ ทุกข้อของแถว A · ❌ **ห้ามอ่าน E2 เป็นผลลบใด ๆ** — E2 ต่างจาก E1 ทั้งเลขไอเทมและระยะ 800 หน่วย ⇒ "ไม่ขึ้น" อาจเป็น culling/นอกมุมกล้อง/ไอเทมคนละตัว · ห้ามเขียนว่า `2200003` ไม่มีโมเดล · จดเป็น **คำถามเปิดเรื่องระยะ** |
| **C** | ไม่มี | มีโมเดล | 🟡 **P1 ผิด = ผล ไม่ใช่ FAIL · ห้ามปิดใบเป็น PASS** | ว่า**ไคลเอนต์วาดวัตถุจาก wire ของเราได้จริง** (จาก E2 — ข้อนี้อย่างเดียวก็มีค่ามาก) | ❌ **ห้ามประกาศว่าฟิลด์ไหนสำคัญโดยเด็ดขาด** — 🔴 `n_ID_MODEL=0` **เป็นดัชนีโมเดลที่ใช้ได้จริง ไม่ใช่ "ไม่มีโมเดล"** (วัดแล้ว R158: `s_ID_ICON` = `ICON_<PARTS>_<n_ID_MODEL:03d>_<n_ID_MAP:03d>` ตรง **376/376 แถว** ที่มี parts · มี `_000_` อยู่ 6 ตระกูล · และ **ทุกแถวของ `ITEM_MISC` ทั้ง 1,646 แถวมี `n_ID_MODEL=0` รวมทั้ง 7 แถวที่มี drop model**) ⇒ E1/E2 **ไม่ได้ต่างกันแค่ฟิลด์เดียว (ต่างกัน 10 จาก 39 คอลัมน์)** และยัง confounded กับระยะ ⇒ ต้องเปิดใบใหม่ยิงสองไอเทม **ที่ระยะเท่ากัน** ก่อนเคลม |
| **D** | ไม่มี | ไม่มี | 🔴 **ผลลบสมบูรณ์ · มีค่าเท่าผลบวก · ไม่ใช่ FAIL ของใบ** (มีผลก็ต่อเมื่อ **ฝุ่นขึ้น**) | ว่า **"เลขไอเทมที่มี `n_DROPMODEL_TYPE≠0` เพียงอย่างเดียว ไม่พอให้ไคลเอนต์วาดโมเดล"** · ฝุ่น (ตัวคุมบวก) ยืนยันว่า transport + เส้นทางของตกพื้นทำงาน ⇒ สิ่งที่ขาดอยู่ที่อื่น — น่าจะเป็น **ฟิลด์/มาสก์ที่เรายังไม่เคยส่ง** (เราส่งแค่ `0x10\|0x02`) ⇒ **redirect: เปิดใบ static หาชุดฟิลด์ขั้นต่ำของ drop-object ก่อนกลับมา attended อีกรอบ** · 🆕 **RE-066 ทำให้แถว D แคบลงหนึ่งขั้น แต่ยังเป็นสองทาง — ห้ามอ่านเป็นทางเดียว:** RE-066 พิสูจน์ว่า **เส้นทางมีอยู่ในอิมเมจ** ไม่ได้พิสูจน์ว่า **runtime เดินเข้าไป** ⇒ แถว D แปลได้สองอย่าง: **(D-i) เดินเข้า create path แล้วอ่านเลขจริง แต่ยังไม่วาด** (ตัวขวางอยู่หลัง lookup — มาสก์/ฟิลด์ที่เราไม่เคยส่ง · เงื่อนไข render) **(D-ii) ไม่เคยเดินเข้า `0x005F41E0` เลยสำหรับเฟรมของเรา** (เงื่อนไขก่อนหน้า เช่น `SCENE-013` null prior ⇒ ตัวขวางอยู่ **ก่อน** lookup) ⇒ **ใบ static ถัดไปต้องแยก D-i/D-ii ก่อนเป็นอย่างแรก** ห้ามกระโดดไปที่ "เกิดอะไรหลัง `0x00890E70` คืนค่า" ทันที | ❌ **ห้ามสรุปว่า "บิต `0x08` ไม่ใช่ช่องของวัตถุบนพื้น"** — ฝุ่นค้านข้อสรุปนั้นอยู่ · ❌ ห้ามตัดสมมติฐาน HYP-PF-032 ทิ้ง · ❌🆕 **ห้ามสรุปว่า "ไคลเอนต์ไม่อ่านเลขไอเทมได้เลยโดยโครงสร้าง"** — RE-066 หักล้างข้อนั้นแล้ว · ❌🆕 **แต่ก็ห้ามสรุปกลับกันว่า "runtime อ่านแน่นอน"** — นั่นคือ D-i ซึ่งยังไม่ถูกพิสูจน์ |
| **E** | — | — | 🔴 **ฝุ่นไม่ขึ้นเลยทั้งสองจุด = NO-RESULT (regression) ไม่ว่าจะเห็นโมเดลหรือไม่** | ไม่มี | ❌ ห้ามอ่านเป็นผลลบทุกกรณี — ดูบล็อกตัวคุมบวกข้างบนแล้วรันใหม่ |

- 🟡 **กรณีพิเศษ: โมเดลขึ้นแต่ฝุ่นไม่ขึ้น** ⇒ ยังอ่านเป็นแถว A/B ได้ (**โมเดลคือสัญญาณที่ใบนี้ตัดสิน**) แต่ให้จดความต่างจากรอบ 1104 ไว้เป็นข้อสังเกต
- 🟡 **ป้ายชื่อลอย:** เป็น bonus signal — **ขึ้น** = จดว่าเกินคาด (P3) · **ไม่ขึ้น** = ไม่กระทบคำตัดสินแถวใด ๆ
- 🔴 **ความเสี่ยงเรื่องมุมมองที่ต้องระวังตั้งแต่ก่อนกด (adversary R158):** E1 อยู่ห่างแค่ **30 หน่วยบน Y/Z เดียวกับตัวผู้เล่น**
  ⇒ **โมเดลอาจถูกตัวละครของเราเองบัง** (รอบ 1104 ฝุ่นขึ้น "ที่เท้าตัวละคร") · ส่วน E2 มีแนวสายตาโล่งแต่ถูกประกาศว่าอ่านไม่ได้
  ⇒ 🔴 **ถ้าไม่ระวัง รอบนี้อาจไม่มีแขนที่อ่านได้เลยสักข้าง** · **ทางแก้ที่ผู้เทสทำได้ทันทีและไม่ต้องแก้โค้ด:**
  หลังกด `W` แล้วเฟรมออก **ให้ถอยกล้อง/หมุนดูรอบตัวช้า ๆ (ตอนนี้ยิงไปแล้ว หมุนได้)** และ **เดินถอยหลังออกจากจุดนั้น 1-2 ก้าว**
  เพื่อให้จุด +30X อยู่ในแนวสายตาโล่ง แล้วค่อยถ่าย G1 · **ห้ามลืมว่าฝุ่นหมดใน ~0.45 วิ** ⇒ ถอยกล้องเพื่อหา **โมเดล** ไม่ใช่ฝุ่น
- **ชั้นนี้ตอบไม่ได้:** ภาพหน้าจอไม่ใช่หลักฐานว่าเฟรมออกจากเซิร์ฟเวอร์จริง **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

### nonclaims (ติดไปกับผลทุกกรณี)
- **ไม่ claim ว่าบิต `0x08` คือ "รายการวัตถุลูทบนพื้น" ในความหมายเต็ม — ยัง UNPROVEN** ถึงแม้จะได้แถว A ·
  สิ่งที่พิสูจน์ได้มากที่สุดคือ "ไคลเอนต์วาดของที่พิกัดที่เราส่ง"
- **ไม่ claim ว่าที่วาดออกมา = ไอเทมที่หยิบได้** — **การวาดไม่ใช่การหยิบ** (ทิศทางการหยิบ = GT-046 · เลนสีเขียว = GT-049)
- **ไม่ claim ว่ามี entity อยู่บนพื้นจริง** — รอบ 1104 ฝุ่นอยู่ ~0.45 s สั้นเกินกว่าจะคลิกทดสอบ ⇒ ยังแยก
  "entity เกิดแล้วถูกลบ" ออกจาก "เล่นเอฟเฟกต์อย่างเดียวโดยไม่เคยมี entity" ไม่ได้
- 🆕 **ไม่ claim ว่าฟิลด์ไหนขับโมเดลบนพื้น** (`n_ID_MODEL` หรือ `n_DROPMODEL_TYPE`) — v3 **ไม่ใช่การทดลองแยกฟิลด์**
  · เหตุผลสามชั้น (adversary R158): ① `n_ID_MODEL=0` เป็น**ดัชนีที่ใช้ได้จริง ไม่ใช่ "ไม่มี"** (376/376 icon correlation)
  ② E1/E2 ต่างกัน **10 จาก 39 คอลัมน์** ไม่ใช่ฟิลด์เดียว ③ ต่างกันที่ระยะด้วย
  ⇒ ข้อเสนอแยกฟิลด์ใน `…NO-ITEM-MODEL.md` §④ **ไม่ถูกนำมาใช้**
  🆕 **ข้อมูล static ที่เพิ่มเข้ามาจาก RE-066 (R161) — เพิ่มน้ำหนัก แต่ "ไม่ปลด" ข้อห้ามข้างบน:**
  ใน concrete inbound graph ของ list `0x5F85B0` มี **named lookup ของ `n_DROPMODEL_TYPE`** (`0x00F30F88` ที่ `0x005F4285`)
  และ **ไม่มี named lookup ของ `n_ID_MODEL` เลย** (refs ในสาม span `CREATE`/`UPDATE`/`CONSUMER` = 0 · ทั้งอิมเมจมี 21 จุดแต่อยู่นอก graph นี้)
  ⇒ สอดคล้องกับคำแก้ของ R158 และ **ทำให้เกณฑ์เลือกไอเทมของ v3 (`n_DROPMODEL_TYPE=1` ทั้งสอง element) เล็งถูกฟิลด์**
  🔴 **แต่ยังห้ามประกาศจากผล attended ว่าฟิลด์ไหนขับโมเดล** — เหตุผลสามชั้นข้างบนไม่มีข้อไหนถูกแก้:
  RE-066 บอกว่า *ไคลเอนต์เปิดอ่านฟิลด์ไหน* **ไม่ได้บอกว่า *อะไรตัดสินการวาด*** และ RE-066 เองประกาศ nonclaim ว่า
  ไม่ตัด indirect alias ทั่วทั้งโปรแกรม ⇒ การแยกฟิลด์ยังต้องใช้ใบที่ยิงสองไอเทม **ที่ระยะเท่ากัน** ตามเดิม
- ✅🆕 **~~ไม่ claim ว่าไคลเอนต์ "อ่าน" ฟิลด์ `+0x14` เลย~~ — ข้อนี้ถูกตอบแล้ว ไม่ใช่ nonclaim อีกต่อไป (chief R161 · 2026-08-25 ~09:5x +07:00)**
  **RE-066 = DONE/PASS · T2 หักล้างเชิงโครงสร้าง:** `+0x14` **ถูกอ่านกลับเป็น full item ID จริง** และเดินถึง item-row decoder ที่ RE-060 พินไว้
  (create path A `0x005F46FA → 0x00892580 → 0x00890FC0 → 0x00890EF0 → 0x00890E70` query **`s_NAME`** ·
  create path B `0x005F426D → 0x00892DD0 → 0x00892610 → 0x00890FC0 → 0x00890E70` query **`n_DROPMODEL_TYPE`** ·
  update path `0x005F4CAC` query `s_TAG_EXTRA`/`n_QUALITY`) · 17 span · CFG gap 0 · errors 0 · sha ก่อน=หลังครบ
  ⇒ ทฤษฎี *"handler เล่นเอฟเฟกต์ตามตำแหน่งโดยไม่เคยแตะ dword"* **ตายแล้ว** ⇒ **การเปลี่ยนเลขไอเทมของ v3 เป็นการทดสอบตัวแปรที่ไคลเอนต์อ่านจริง**
  🔴🔴 **แต่ข้อห้ามเรื่องแถว D ยังอยู่ และแคบลงแค่ "หนึ่งขั้น" ไม่ใช่ "เหลือทางเดียว" — อ่านให้ครบ**
  *(ฉบับแรกของ R161 เขียนว่า "ตอนนี้เหลือทางเดียว: อ่านแล้วแต่ไม่วาด" — **ผิด `pf-adversary` จับได้** เพราะนั่นคือ
  การเอาผล **static** (เส้นทางมีอยู่) ไปสรุปเรื่อง **runtime** (เดินเข้าไปจริง) ซึ่งเป็นสิ่งที่ RE-066 ประกาศ nonclaim ไว้เอง)*
  **RE-066 ตัดทางที่ว่า "โครงสร้างไม่มีทางอ่านได้เลย" ทิ้ง — ไม่ได้ตัดทางที่ว่า "runtime ไม่ได้เดินเข้าไป"**
  ⇒ แถว D **ยังเป็นสองทาง** แต่ทางที่สองมีชื่อแล้ว:
  - **D-i** เดินเข้า create path อ่านเลขจริง **แต่ยังไม่วาด** ⇒ ตัวขวางอยู่ **หลัง** lookup (มาสก์/ฟิลด์ที่ไม่เคยส่ง · เงื่อนไข render)
  - **D-ii** **ไม่เคยเดินเข้า `0x005F41E0` เลยสำหรับเฟรมของเรา** ⇒ ตัวขวางอยู่ **ก่อน** lookup (เช่น `SCENE-013` null prior)
  ⇒ 🔴 **ยังห้ามปิดสมมติฐาน "เลขไอเทมคือสาเหตุ" ด้วยแถว D เดี่ยว ๆ** · และ **ใบ static ถัดไปต้องแยก D-i/D-ii ก่อนเป็นอย่างแรก**
  ⚠️ **nonclaim ของ RE-066 เองที่ต้องพกมาด้วย:** static ไม่บอกว่า runtime เดินเส้นนี้จริง · ไม่แทนที่รอบ attended · ไม่ตัด indirect alias ทั่วโปรแกรม
- 🆕 **ตัวคุมที่ถือ table code คงที่ = `2600022`** (ITEM_MISC · `n_DROPMODEL_TYPE=12` · ต่างจาก `2600001` เฉพาะเรื่อง drop model)
  — **จงใจไม่รวมเข้ารอบนี้** เพราะรอบ attended เป็น one-shot · ถ้าได้แถว D ⇒ นี่คือการทดลองถัดไป
  🔴 เหตุที่ต้องมี: การย้าย `2600001 -> 2200423` เปลี่ยน **table code 26 -> 22** ด้วย และ RE-060 พินไว้แล้วว่า
  ไคลเอนต์ decode `full_id / 100000` เป็น **การเลือก table object ตอน runtime** ⇒ ผลบวกแยก "ไอเทมนี้มี drop model"
  ออกจาก "code 22 resolve ได้ · code 26 ไม่ได้" **ไม่ได้**
- **ไม่ claim ว่าเซิร์ฟเวอร์ต้นฉบับ (ปิดไปแล้ว กู้ไม่ได้ตลอดกาล) เคยใช้ช่องนี้** — ใบนี้ทดสอบแค่ว่าไคลเอนต์รับได้ไหม
- **ไม่ claim ว่าคลิปวิดีโออ้างอิงยืนยันช่องทาง transport ใด ๆ** — คลิปอยู่ชั้น client-observable ล้วน
- **การประกอบ element เป็นดีไซน์ของเรา** ไม่ใช่ของเซิร์ฟเวอร์เดิม · หน่วยพิกัดโลกแปลงเป็นหน่วยจริงไม่ได้
- **ตารางไอเทม (`EQUIPMENT_BASE`/`ITEM_MISC`) คือข้อมูลที่ ship มากับ client** ไม่ใช่กฎของเซิร์ฟเวอร์ต้นฉบับ

- **result:** (ผู้เทสกรอก: ① BOOT_COMMIT + ผลเช็คห้าข้อ (โดยเฉพาะข้อ 5 `2600001` = 0 บรรทัด) ② masked sha ทั้งสี่ตรง pin หรือไม่
  ③ trigger X/Y/Z + near/far ที่ decode ได้ ④ **แถวไหนของเมทริกซ์ (A/B/C/D/E)** ⑤ สามช่องแยก: ฝุ่น (ขึ้น/ไม่ขึ้น · กี่วินาที) ·
  โมเดล (element ไหน · ค้าง/หาย) · ป้ายชื่อ ⑥ ภาพ G0/G1/G1b/G2 + วิดีโอต่อเนื่อง พร้อม sha256 ทุกไฟล์ ⑦ ผลเดินไปยืนทับทั้งสองพิกัด
  ⑧ path raw GAME log · เวลา · sha canonical ก่อน-หลัง · `integrity_check` · exit code ของ teardown)

### 🔴 หมายเหตุตอนบริโภคผล (แทรก R126 · คงไว้ · ไม่แก้ steps/pass criteria)
- **chief อ่านผล GT-045 คู่กับ GT-034 เสมอ** (คำสั่ง Panya 1315 §③): ถ้า wire ผ่านแต่จอไม่ขึ้นอะไรทั้งสองพิกัด
  นั่นเป็นสัญญาณที่กว้างกว่า GT-034 มาก · อ่านคู่กับ **GT-048** (client สร้าง entity จากข้อมูลตัวเองได้ไหม) ด้วย —
  GT-045 = แหล่งป้อนจาก wire · GT-048 = แหล่งป้อนจากข้อมูล client · **คนละแหล่ง ห้ามอ่านแทนกัน**
  🆕 **R158: GT-034 ได้ข้อสรุปแล้ว** (ไคลเอนต์ไม่ spawn hostile เอง · มีตัวควบคุมเชิงบวกครบ) — อ่านคู่กันได้เต็มที่แล้ว
- **ระบบเก็บของมีอย่างน้อยสองเลน** (จดหมาย 1335/1350 · ชั้น client-observable จากเฟรมคลิป + คำให้การผู้เล่น
  — ไม่มีหลักฐานชั้น wire/DB): เลนสัมผัส (ออกฤทธิ์ทันที ไม่มีข้อความ `ได้รับ`) และเลนไม่สัมผัส (เข้ากระเป๋า มีบรรทัดเขียว) ·
  🔴 **ผล render ของ GT-045 พิสูจน์ได้เฉพาะฝั่ง render — ไม่พิสูจน์ว่ามันหยิบได้** (1335 §④)
- **ผลกระทบต่อ GT-060:** แถว A/B ปลดได้เฉพาะครึ่ง "มีวัตถุวาดจริง" ของเงื่อนไข (ข) — **ครึ่ง "คลิกได้" ยังไม่ถูกแตะ**


## 🔬 GT-046 PICKUP-DIRECTION-001 [STATIC-ON-BRIDGE]: `PickupTerrainThing` เป็นข้อความที่ไคลเอนต์ "ส่งออก" หรือ "รับเข้าอย่างเดียว" — หาจุดสร้าง/จุดส่ง  [✅ **PASS / DONE (STATIC) — ปิดโดย chief R127 จากผล 2026-08-23 14:28-14:35 (+07:00)**]

### ✅ บล็อกผล (R127 · ผลเต็ม: `notes_to_chief\20260823_1435_GT046-PASS-outbound-mouseclick-runtime-drop-object.md`)
- **outbound พิสูจน์แล้ว:** `PickupTerrainThing` ถูกสร้างที่ call `0x006B0639` เติมค่าจาก **live runtime drop-object
  ที่ module เลือก** (`[esi+0x7C]` -> `[ptr+0x10]`) เข้าคิวส่งที่ `0x006B0653` · serializer `0x005E5E30`
  เขียนสองฟิลด์ผ่าน WRITE `0x0089A600`
- **ตัวจุดชนวน:** callback ของ `DropThingModule_Client` เทียบ `WM_LBUTTONDOWN (0x201)` ที่ `0x006B0570` —
  ส่งเฉพาะเส้นทาง in-range · **คลิกเมาส์ ไม่ใช่ timer/passive**
- **response mapping:** `0xFC->0x1F` (bounded = too-far) · `0xFD->0x03` · `0xFE->0x22` (ความหมายสองตัวหลังยังไม่ผูก ณ R127 — ดู addendum R132 ล่าง) ·
  🔴 **ไม่พบ static link จากสามตัวนี้ไปบรรทัดสีเขียว `ได้รับ [ชื่อ] * จำนวน`** — ช่องว่างนี้กลายเป็นใบ **GT-049**

### ✏️ addendum (chief R132 · 2026-08-23 ~22:0x +07:00 · จากจดหมาย `20260823_2150_GAMEDATA-EXTRACTED-…` · ชั้น client-static)
- **message id ทั้งสาม bound แล้ว** จาก `pf_bridge\gamedata\tables\TEXTDATA_TH__MESSAGE.tsv` (907/907 แถว · ตรงสารบัญ):
  `0x1F`(31) = `ระยะทางไกลเกินไป!` · `0x03`(3) = `ช่องว่างในกระเป๋าไม่เพียงพอหรือจำนวนไอเทมดังกล่าวมีถึงจำนวนจำกัดแล้ว!` ·
  `0x22`(34) = `ไอเทมของผู้อื่น ไม่สามารถเก็บขึ้นมาได้!`
- **ข้อเท็จจริงใหม่สามข้อที่ตกจากตาราง (ระดับ client-static — เกมต้นฉบับมีข้อความรองรับพฤติกรรมนี้):**
  ① `0x22` ⇒ เกมมีระบบสิทธิ์/เจ้าของไอเทมที่ดรอป — เซิร์ฟเวอร์เราต้องถือ owner ของ drop และปฏิเสธคนอื่น
  ② `0x03` ⇒ การเก็บล้มเหลวเพราะกระเป๋าเต็ม/ชนเพดานจำนวนได้ — ต้องเช็คก่อนให้ของ
  ③ `0x1F` ⇒ ยืนยันการเช็คระยะ (GT-046 อนุมานจากโค้ด · ข้อความยืนยันตรง)
- [ตีความ] ทั้งสามเป็นข้อความ **ล้มเหลว** ⇒ handler นี้แจ้งเฉพาะเก็บไม่สำเร็จ · `ได้รับ` น่าจะยิงจากระบบกระเป๋า —
  ปิดได้ต่อเมื่อ GT-049 จ็อบ 2-4 เจอจุดยิง id 131 · **nonclaim: ตารางคือสิ่งที่ไคลเอนต์ถือ ไม่ใช่กฎเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล**
- 🔴 **nonclaim บังคับติดผล:** มี `FightingDropModule_Client` + `FightingDropNotify` แยกอีกครอบครัว (ยังไม่ decode) ⇒
  **ห้ามอ้างว่าผลนี้อธิบายการเก็บของมอนดรอป** — ระบบเก็บของมี ≥2 เลนตามจดหมาย 1335/1350 ·
  static ไม่พิสูจน์ว่าเลนนี้รันจริงในเฟรมคลิป (สมมติฐาน "ของวางไว้ล่วงหน้า" ของผู้ช่วยถูกถอนแล้ว — ERRATUM 15:20)

**ที่มา:** ร่างผู้ช่วย `notes_to_chief\20260823_0805_GT-TICKET-DRAFT-ground-drop-and-pickup-direction.md` (ท่อน GT-046)
ทำไมสำคัญกว่าที่เห็น: ถ้าไคลเอนต์ **ส่ง** เอง ⇒ มีตัวจุดชนวนฝั่งไคลเอนต์ (auto-loot/เพ็ต/ระยะ) เซิร์ฟเวอร์แค่ตอบ ·
ถ้าไคลเอนต์ **ไม่เคยส่ง** ⇒ การเก็บถูกตัดสินฝั่งเซิร์ฟเวอร์ทั้งหมด · **สองทางนี้ทำให้เราต้องเขียนเซิร์ฟเวอร์คนละแบบ**

**หมวด:** `STATIC-ON-BRIDGE` — ต้องเปิด `GameClient.local.bin` จึงทำบน cloud clone ไม่ได้ ·
ผู้รับงานคือคนที่นั่งหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม · **ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว**

### objective (claim เดียว)
**`PickupTerrainThing` ถูกสร้างและเขียนลงสตรีมผ่าน `0x0089A600` (WRITE) ที่ VA ใดในอิมเมจ หรือไม่พบจุด WRITE เลย**
(ทิศทางตัดสินด้วยว่า object เข้าสตรีมผ่าน `0x0089A600` WRITE หรือ `0x0089A640` READ — สองตัวนี้พิสูจน์แล้วตั้งแต่ GT-040)

### db / server args
**ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client** — เปิดอ่านอิมเมจอย่างเดียว (กติกา stamp 420 นาที/teardown ไม่เกี่ยวกับใบนี้)

### สิ่งที่ต้องมี (precondition)
- **อิมเมจ:** `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · PE32 · ImageBase `0x00400000`
  🔴 **จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง เปิดอ่านอย่างเดียวเสมอ**
- **ท่าทำงาน:** ตามวินัย `pf-static-re` · 🔴 **ห้ามใช้ linear disassembler เป็นหลักฐานของ negative** (มันหยุดที่ไบต์แรกที่ decode
  ไม่ได้แล้วรายงาน negative อย่างมั่นใจ = ความผิดพลาดรอบ 83) · census ด้วย byte matching (`E8`/`E9 rel32` ทุกออฟเซ็ต) ·
  สวีป exec section ทั้งสอง: `.text` (`0x00401000`, Vsize `0x00838A2C`) และ `.code` (`0x00C3A000`, Vsize `0x2E1`)
- **span ฐานผ่านปฏิปักษ์แล้ว:** GT-042 **PASS 2026-08-23** — span ข้างล่างรอด re-derive และขอบเขต handler ถูกแก้แล้ว ·
  กติกาเดิมยังบังคับ: **verify sha ของทุก span ก่อนพึ่งด้วยตัวเอง** · sha ไม่ตรง = หยุด รายงาน

### ของที่มีอยู่แล้ว (จาก GT-040 ท่อน C · ผ่าน re-derive ปฏิปักษ์ใน GT-042 · verify sha ก่อนพึ่ง)
```
vtable                0x00F3005C
serializer  slot +0x18  [0x005E5E30,0x005E5E83)  len 83
                        sha 8e439d4f3ff1479e723b220d8dd78a262b41df3b74839da9d4cb728f69773066
                        2 ฟิลด์: tag 0x14 @ +0x14 len 4  ·  tag 0x08 @ +0x18 len 1  (ไม่มีฟิลด์ที่สาม)
handler (ขอบเขตแก้แล้ว) [0x005EF640,0x005EF66F)  len 47
                        sha 5d17fc4fdeeafde0a4a34e900e76d0336e404f8d2f058ba085044ae8d88d602e
                        อ่าน +0x18 แยก FC/FD/FE -> message id 1F/03/22 แล้วคืน true
census                PickupTerrainThing 0xF3093C 1 จุด · 0x108202C 2 จุด · constructor 3 จุด
```
🔴 **erratum ที่ต้องพกไปด้วย (ปิดโดย GT-042):** span handler เก่า `[0x005EF640,0x005EF908)` len 712 (sha `22da3ff4...`)
**hash ตรงแต่ป้ายผิด** — ไม่ใช่ handler ฟังก์ชันเดียว (`0x005EF66F=CC` · `0x005EF670` เริ่ม prologue ฟังก์ชันถัดไป) ·
ขอบเขตที่ถูกคือ `[0x005EF640,0x005EF66F)` len 47 ข้างบน — ใบนี้อ้างขอบเขตที่แก้แล้วเท่านั้น

### จ็อบ (ทำตามลำดับ 1 -> 2 -> 3 -> 4 · **แล้วต่อจ็อบ 5-6 ในบล็อก "แก้ขอบเขต" ข้างล่าง — บังคับเท่ากัน**)
1. ไล่ทั้ง 3 จุดที่อ้าง vtable literal `0x00F3005C` (constructor) → ใครเรียก constructor พวกนั้น (census `E8/E9 rel32` เอง)
2. ตามสายขึ้นไปจนถึงจุดที่ object ถูกป้อนเข้าสตรีม → ใช้ **`0x0089A600` (WRITE)** หรือ **`0x0089A640` (READ)** — ตัวตัดสินทิศทาง
3. ถ้าเจอฝั่ง WRITE: อะไรเป็นตัวเรียก (input handler / timer / entity update)? ค่าที่ใส่ `+0x14` มาจากไหน
4. ค่า `FC/FD/FE` ที่ `+0x18` — หาว่าฝั่งไหนเป็นคนเซ็ต · message id `0x1F/0x03/0x22` แปลเป็นข้อความอะไร
   (**เชื่อมกับคลิปได้ตรงนี้:** คลิปเห็นบรรทัด `ได้รับ [<ชื่อ>] * <จำนวน>` **สีเขียว** แยกจาก EXP/ค่าฝีมือที่**สีขาว** —
   ถ้า message id ใดใน 1F/03/22 ตรงกับ template ที่มี `* <จำนวน>` นั่นคือจุดเชื่อมสองชั้นแรก · จดว่าเชื่อมได้/ไม่ได้)

### 🔴 แก้ขอบเขต (แทรก R126 · ตามจดหมาย 1335 §② + 1350 §⑤ · ไม่รื้อจ็อบ 1-4 เดิม · **จ็อบ 5-6 ข้างล่างบังคับเท่าจ็อบ 1-4 — ใบไม่จบถ้ายังไม่ตอบ**)
GT-046 อาจถามผิดระบบ: มีระบบเก็บของ **อย่างน้อยสองระบบ** (จดหมาย 1335) —
(ก) ของที่ **วางบนพื้นล่วงหน้า** (ของเควส เช่น `Sky Lantern`) เก็บด้วยการสัมผัส `[ความจำผู้เล่น — ยังไม่มีหลักฐานเฟรม/ไบต์]` ·
(ข) ของที่ **มอนดรอป** วิธีเก็บยังไม่ทราบเต็ม · ชื่อ `Terrain Thing` อ่านตรงตัว = ของในฉากที่วางไว้ (เอียงไปทางระบบ ก — **สมมติฐานจากชื่อ** ไม่ใช่ข้อเท็จจริง)
🔴 **ห้ามเอาผลของระบบหนึ่งไปอธิบายอีกระบบ**

**จ็อบเพิ่ม 5:** ฟิลด์ `tag 0x14 @ +0x14 len 4` เป็น id ของอะไร — ของ *วัตถุในฉากที่วางไว้ล่วงหน้า*
หรือ *วัตถุที่ถูกสร้างตอนรันไทม์* · ตัดสินจากว่าค่ามันถูกอ่านมาจาก **โครงสร้างฉาก/ทะเบียน** ตัวไหน (span + VA)

**จ็อบเพิ่ม 6:** census หาข้อความอื่นที่มีคำว่า `Drop` / `Loot` / `Item` ในตารางชื่อ แล้วเทียบว่ามีตัวไหน
ที่ **ไม่ใช่** `PickupTerrainThing` และดูเหมือนเป็นเลนของ *ของที่มอนดรอป* ·
🔴 **ผลลบ ("ไม่มีตัวอื่นเลย") เป็นคำตอบที่มีค่า** — แปลว่าทั้งสองระบบใช้ข้อความเดียวกัน

**หมายเหตุสมมติฐานสองเลน (จาก 1350 §⑤ · ห้ามใช้แทนหลักฐานไบต์):**
ถ้าไบต์ของ `PickupTerrainThing` มีแค่ 2 ฟิลด์ (`tag 0x14 @+0x14 len4` + `tag 0x08 @+0x18 len1`)
และผลลัพธ์แตกเป็น `FC/FD/FE` ⇒ *น่าสงสัย* ว่าเป็นเลน "ร้องขอเก็บวัตถุหนึ่งชิ้น แล้วได้ผลลัพธ์สามแบบ"
ซึ่งเข้ากับเลนสัมผัสมากกว่าเลนอัตโนมัติ ·
🔴 **GT-046 ต้องตัดสินด้วยไบต์เท่านั้น ห้ามตัดสินด้วยใบวัดเฟรม (1350) หรือคำให้การผู้เล่น (1335)** —
ใบวัดเฟรมอยู่ชั้น client-observable ล้วน คนละชั้นหลักฐานกับ static ของใบนี้

### pass criteria — **STATIC-ON-BRIDGE (span + sha256 + re-derive · ชั้นเดียว)**
**ชั้น static (ชั้นเดียวของใบนี้):**
- verify sha ของ **ทุก** span ที่พึ่งก่อน re-derive · 🔴 **sha ไม่ตรงแม้ตัวเดียว = หยุด รายงาน span ที่เพี้ยน ห้าม re-derive ทับ**
- ตอบ objective เป็นประโยคเดียวได้: `PickupTerrainThing ถูกสร้างและเขียนลงสตรีมที่ <VA> ผ่าน 0x0089A600`
  **หรือ** `ไม่พบจุด WRITE เลยในอิมเมจ (ไล่ census E8/E9 + indirect ครบแล้ว)`
- แนบ span `[start,end)` + file offset + len + sha256 ของ **ทุก** ฟังก์ชันที่อ้าง (รูปแบบเดียวกับ GT-040/GT-042/GT-044)
- sha256 อิมเมจก่อน-หลังตรงกัน · ถ้าเขียนสคริปต์ commit ลง `tools/` แบบรันซ้ำได้พร้อม guard count + exit 0

**ชั้น client-observable:** 🔴 **ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้ และห้ามใครอ้าง static เป็นหลักฐานว่าจอเห็นอะไร**
ไม่มีเกมให้บูต ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย**

### 🔴 ผลลบมีค่าเท่าผลบวก
- **"ไม่พบจุด WRITE เลย"** = ผลที่มีค่าเท่าการเจอ ⇒ ชี้ว่าไคลเอนต์อาจรับเข้าอย่างเดียว (การเก็บตัดสินฝั่งเซิร์ฟเวอร์)
  **แต่ต้องเขียนกำกับว่าไล่ indirect ครบหรือยัง** — "ไม่พบ WRITE" ≠ "ไคลเอนต์ไม่ส่ง" ถ้าเป็นการเรียกผ่าน table/indirect
- **เจอจุด WRITE** = redirect ไปหาตัวจุดชนวนฝั่งไคลเอนต์ (input/timer/entity) — งานออกแบบเซิร์ฟเวอร์เปลี่ยนทิศทันที

### nonclaims (ติดไปกับผลทุกกรณี)
- **static ไม่พิสูจน์ว่ารันไทม์ส่งจริง** — พิสูจน์ได้แค่ว่ามี/ไม่มีเส้นทางในอิมเมจ
- **"ไม่พบจุด WRITE" ≠ "ไคลเอนต์ไม่ส่ง"** ถ้ายังไล่ indirect ไม่ครบ — ต้องระบุสถานะการไล่ indirect
- **ห้ามอ้างว่าคลิปวิดีโอยืนยันทิศทางของข้อความ** — คนละชั้นหลักฐาน
- **ไม่ claim ว่ารู้ชื่อคลาส** ของ record — vtable ไม่มี RTTI/name literal · **ห้ามเดาชื่อ = ห้ามประดิษฐ์ wire format**
- **ไม่ claim ว่า derived id ถูก** — id จริงมาจากรันไทม์ที่ `ds:0x0108202C` ซึ่ง `.data` เป็นศูนย์ในไฟล์
- 🔴 **nonclaim บังคับ (แทรก R126 · 1335 §② ข้อ 3):** ห้ามสรุปว่าผลของ `PickupTerrainThing` อธิบายการเก็บของที่มอนดรอป
  จนกว่าจ็อบเพิ่ม 5-6 จะตอบว่ามันเป็นระบบเดียวกัน (ระบบ ก vs ระบบ ข)
- **result:** (ผู้รับงาน static บนสะพานกรอก: ประโยคทิศทาง WRITE/READ + VA · span/file-offset/len/sha256 ทุกฟังก์ชัน ·
  **คำตอบจ็อบ 5**: id ที่ `+0x14` อ่านมาจากโครงสร้าง/ทะเบียนไหน (span + VA) · **คำตอบจ็อบ 6**: ผล census `Drop`/`Loot`/`Item`
  ในตารางชื่อ — รายชื่อที่พบ หรือประกาศ "ไม่มีตัวอื่นเลย" ·
  สถานะการไล่ indirect · เวลา · sha อิมเมจก่อน-หลัง)


## 🔬 GT-047 RUNTIMEPROTO-CAPTURE-VALIDATE-001 [STATIC-ON-BRIDGE]: parse เฟรม `GSCN_RunTimeProtocolReq`/`Res` จาก capture corpus ด้วย schema ของ Codex — ปิด F2 ของใบตรวจปฏิปักษ์  [✅ **DONE / GUARD-GAP FIXED / METHOD-RUN COMPLETE — แต่ claim F2 คง OPEN (ผลหน้าสะพาน 2026-08-24 14:43 +07:00 · R149 บันทึก)**]

> ✅ **ผลปิดใบ (จดหมาย `20260824_1443`):** patched validator (`CAFA…011B` จาก `patches/gt047/`) ผ่านการ์ด **8/8** บนสะพาน · จ็อบ 3 mutation `TargetPosVital:W:1 field_offset +0x14→+0x99` **แดงจริง** (`exit 1`) ⇒ ช่องโหว่ TOOL-GUARD-GAP เดิมปิดแล้ว · จ็อบ 2 re-derive สดตรง byte-for-byte สามไฟล์ · จ็อบ 1 frozen corpus 1,772 ไฟล์ exit 0 — **แต่** `Req/W 40,747` และ `Res/R 10,073` เฟรม ยัง `A2_STATIC_OPEN` ทั้งหมด (parse success 0) ⇒ 🔴 **claim F2 ยัง OPEN**: `A2_STATIC_OPEN 50,820/50,820` จนกว่าจะมี parser เข้าถึง body สองข้อความนี้จริง · `mismatch=0` ของรอบนี้ **ไม่ใช่** หลักฐาน schema (เฟรมถูกจัด static-open ก่อน parse) · external/ ต้นทางไม่ถูกแตะ (SHA เดิม)

### 🟠 สถานะ R144 (2026-08-24 ~09:5x–10:2x +07:00 · chief cloud) — ⏱️ **erratum R145:** บรรทัดนี้เคยเขียน `~16:5x–17:3x +07:00` ซึ่งเพี้ยนไป 7 ชั่วโมง (commit จริงของ R144 คือ `02:51`–`03:21` UTC = `09:51`–`10:21` +07:00 · ตรวจด้วย `git show -s --date=iso 0ad4f1a fbd1cfd`) — สาเหตุ: R144 เอาเวลา +07:00 ไปติดป้าย `Z` แล้วบวก 7 ซ้ำอีกชั้น
- จ็อบ 0 ปิด: จดหมาย `20260824_0916_GT047-validator-source.py.md` ส่ง source ครบ (sha256 `0166337C…B793D8C8` ตรงกับที่จดหมายพิน · AST parse PASS)
- **การ์ดใหม่ (`validate_field_offset_mirror`) อยู่ที่ `patches/gt047/pf_validate_capture_fields.py`** — หลักการ: W/R legs ของ message ที่ closed ต้อง mirror กัน (field_offset/tag/span_start/span_end raw — ยกเว้น 40 คู่ที่ pin ว่า VA-dependent ใช้ normalized · len/span_sha256 raw เสมอ) + pin census 181 static-open / 859 คู่ กัน mutation หนี้เข้า skip set
- เขียว(cloud sanity) 8 ด่าน: pristine ผ่าน · mutation จ็อบ 3 ของ tester (`+0x14→+0x99`) **แดง** · flip `UNKNOWN(`, one-leg VA edit, span_sha256 tamper, membership swap (นับเท่าเดิมแต่สลับสมาชิก) แดงหมด · self-test จับการ์ดที่ถูกปิดได้ — ตัวรัน `patches/gt047/verify_gt047_guard_patch.py` (echo sha256 ของ validator ที่โหลดจริงบรรทัดแรก — **ให้ quote บรรทัดนั้นในผล rerun**)
- adversary สองรอบก่อน commit (รอบแรกจับ 4 defect: `.gitignore` กิน `patches/` · flip เข้า static_open · normalization laundering · span columns — แก้ครบ)
- nonclaims ของการ์ด: ไม่ครอบ mutation สมมาตรสองขา · ไม่ครอบ VA ฝังในคู่ pinned 40 คู่ (ชั้นนั้นพึ่ง span_sha256 + GT-054) · ไม่ครอบ `gate_condition`/`file_off_claim` (legs ต่างกันเกิน mirror โดยชอบ — validator ไม่เคยอ่านสองคอลัมน์นี้)
- **ฝั่งสะพานทำต่อ:** ① pull main หลัง PR รอบนี้ merge ② ตรวจ sha256 ของ `patches/gt047/pf_validate_capture_fields.py` ตรงกับที่จดหมาย `FROM_CHIEF_R144_*` พิน ③ สำเนาทับตัวเดิมใน `pf_bridge\external\` ④ รัน `verify_gt047_guard_patch.py --external <โฟลเดอร์ external>` ต้องได้ `ALL 8 CHECKS PASS` ⑤ rerun จ็อบ 3 (mutation ต้องแดง — log ทั้งก่อน/หลัง) แล้วจ็อบ 1–2 ตามใบเดิม

### 🟠 สถานะ R127 (ผลรัน 2026-08-23 14:21-14:27 · ผลเต็ม: `notes_to_chief\20260823_1427_GT047-GUARD-GAP-fieldoffset-mutation-accepted.md`)
- จ็อบ 1: frozen view 1,772 ไฟล์ validator exit 0 · `mismatch=0` · แต่สองข้อความเป้าหมาย **ยังค้าง `A2_STATIC_OPEN` ทั้งคู่**
  (W observed 40,747 · R observed 10,073 — สถานะไม่ขยับเป็น `VALIDATED`) ⇒ **F2 ยังไม่ปิด**
- จ็อบ 2: re-derive ตรงไบต์ต่อไบต์ครบสาม TSV · image sha ไม่เปลี่ยน ✅
- จ็อบ 3 (การ์ดบังคับ): กลายพันธุ์ `TargetPosVital:W:1 field_offset +0x14 -> +0x99` แล้ว validator **ยังเขียว
  (mismatch=0 ตัวเลขเดิมเป๊ะ)** = **การ์ดไม่ครอบคลุม `field_offset` จริงตามที่ใบตรวจ 07:30 เตือน** ·
  ผู้เทสไม่ patch เอง (นอกบทบาท) — **เจ้าของเครื่องมือ (chief) ต้อง patch จนแดง แล้วค่อย rerun ใบนี้**
- 🔴 **จุดติด:** `pf_validate_capture_fields.py` อยู่ที่ `pf_bridge\external\` บนสะพานเท่านั้น **ไม่อยู่ใน VCS** ⇒
  chief บนคลาวด์มองไม่เห็น source จึง patch แบบมีหลักฐานไม่ได้
- 🆕 **จ็อบ 0 (ทำก่อน rerun · ฝั่งสะพาน · ไม่ต้องบูตอะไร):** ส่ง source ของ `pf_validate_capture_fields.py`
  (และไฟล์ที่มันเรียกใช้ เช่นตัว `validate_schema_mutation_regressions()` ถ้าแยกไฟล์) เข้า repo `pf_bridge`
  ทางใดทางหนึ่ง: ① วางสำเนาเป็นไฟล์ใหม่ใต้ `notes_to_chief\` ชื่อ `<YYYYMMDD_HHMM>_GT047-validator-source.py.md`
  (เนื้อไฟล์ทั้งดุ้นใน fenced code block · ห้ามแนบ capture/TSV) หรือ ② เพิ่มพาธนั้นใน allowlist ของ
  `pf_git_sync.ps1` ถ้า Panya อนุญาต · แล้ว chief จะเขียนการ์ด + เทสการ์ด (ต้องแดงบน mutation `field_offset`)
  ส่งกลับเป็น patch ในรอบถัดไป
- สถานะปลายทางของใบ: **ห้ามอ่าน `mismatch=0` รอบนี้เป็นการยืนยัน schema** — validator ที่ไม่แดงบน corruption
  ยังไม่มีสิทธิ์ promote อะไร (D4/D5 รอบ 118)

**ที่มา:** ใบตรวจปฏิปักษ์ `notes_to_chief\20260823_0705_ADVERSARY-VERDICT-on-codex-RE-handoff.md` (F2) +
`notes_to_chief\20260823_0730_ADVERSARY-FOLLOWUP-plus-GROUND-DROP-evidence.md` (ข้อ 2 · การ์ด mutation `field_offset`)
F2: สองใบที่สำคัญที่สุดในโปรเจกต์ (`GSCN_RunTimeProtocolReq` W 40,747 เฟรม · `GSCN_RunTimeProtocolRes` R 10,073 เฟรม =
รวม 50,820 เฟรม คลังหลักฐานที่รวยที่สุด) ยังเป็น `A2_STATIC_OPEN` **ไม่เคยถูก parse สักเฟรม** ·
และงานคอมแบต/ลูท/การเคลื่อนที่ทั้งหมดขี่อยู่บนใบนี้ (actor-entry collection · derived bit `0x02`/`0x04`/`0x08` ของ GT-040)

**หมวด:** `STATIC-ON-BRIDGE` — ใช้ capture corpus + ชุดส่งมอบ RE ที่อยู่บนเครื่องสะพานเท่านั้น ·
🔴 **ต้องรันบน Windows ของสะพาน** — ใบตรวจ 07:30 พิสูจน์แล้วว่าชั้น capture รันจาก Linux mount ไม่ได้
(`PF_INPUT_INVENTORY.tsv` ปักพาธ Windows · เจอ `ERROR: fresh capture path set differs from input inventory`)
**ไม่มีอะไรให้ดูบนจอเกม** ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย**

### objective (claim เดียว)
**สถานะของ `GSCN_RunTimeProtocolReq` (W) และ `GSCN_RunTimeProtocolRes` (R) ขยับจาก `A2_STATIC_OPEN` เป็น `VALIDATED`
ด้วยการ parse capture 50,820 เฟรมผ่าน schema จากชุดส่งมอบ RE ของ Codex หรือรายงาน mismatch เป็นตัวเลข**
🔴 **mismatch > 0 มีค่าเท่าหรือมากกว่า `VALIDATED`** — จดเป็นผล ไม่ใช่ fail (mismatch ที่วัดได้ = ที่ที่เราเดาผิด ชี้ตัวได้)

### db / server args
**ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client** — parse capture + อ่าน schema TSV อย่างเดียว
(กติกา stamp 420 นาที/teardown/canonical ไม่เกี่ยวกับใบนี้ · แต่ **ห้ามแก้ capture และห้ามแก้ TSV ส่งมอบ** — เปิดอ่านอย่างเดียว)

### สิ่งที่ต้องมี (precondition · verify ก่อนเริ่ม)
- ชุดส่งมอบ RE ของ Codex ที่ `pf_bridge\external\` (บนเครื่องสะพาน — ยังไม่ได้ push เข้า repo) · verify จำนวนแถวตามที่ใบตรวจ 07:05 นับไว้:
  `PF_PROTOCOL_REGISTRY.tsv` 520 บรรทัด (519 + หัว) · `PF_SERIALIZER_FIELDS.tsv` 6,932 (6,931 + หัว) ·
  `PF_TAG_CENSUS.tsv` · `PF_FIELD_VALIDATION.tsv` · `PF_RUNTIME_CLASSMAP.tsv` 6,244 แถว (ทั้งหมด UNKNOWN — ห้ามพึ่งเป็นชื่อคลาส)
- เครื่องมือ: `pf_validate_capture_fields.py` (เรียก `validate_schema_mutation_regressions()` ทุกครั้ง) ·
  `pf_extract_protocol.py` (A4 · re-derive ผ่านแล้วใน 07:30 — sha256 TSV ตรงไบต์ต่อไบต์)
- capture corpus ที่อ้างใน `PF_INPUT_INVENTORY.tsv` (พาธ Windows ของสะพาน — อย่าแก้)
- 🔴 **ไม่ต้อง WAIT merge อะไร** — ชุดส่งมอบถูกรับเข้าใช้งานแล้ว (ใบตรวจ 07:05) และอยู่บนสะพานครบ ·
  แต่ **การ์ด mutation ตัวใหม่ (ดูจ็อบ 3) ต้องเพิ่ม/รันบน Windows** เพราะ Linux mount รันชั้น capture ไม่ได้

### จ็อบ (ทำตามลำดับ 1 -> 2 -> 3)
**จ็อบ 1 (แกน) — parse 50,820 เฟรมของสองข้อความ**
1. เอา schema ของ `GSCN_RunTimeProtocolReq` (W) และ `GSCN_RunTimeProtocolRes` (R) จาก `PF_SERIALIZER_FIELDS.tsv`
   (Res อ้าง serializer `0x005E3EE0` / handler `0x005E4060` ในใบตรวจ 07:05 — verify กับ TSV จริง อย่าฝังค่า)
2. รัน `pf_validate_capture_fields.py` บนคลัง 40,747 (W) + 10,073 (R) เฟรม · รายงานเป็นตัวเลข:
   parse ok / parse fail / **mismatch นับรายฟิลด์** · สถานะปลายทางของแต่ละข้อความ (`VALIDATED` หรือค้าง `A2_STATIC_OPEN` พร้อมเหตุ)

**จ็อบ 2 — re-derive ยืนยันว่า schema สกัดสดจากอิมเมจ ไม่ใช่ตารางจำ**
3. คัด `pf_extract_protocol.py` ไปรันในไดเรกทอรีเปล่านอกโฟลเดอร์ส่งมอบ ชี้อิมเมจเดิม → เทียบ sha256 ของ
   `PF_PROTOCOL_REGISTRY.tsv`/`PF_SERIALIZER_FIELDS.tsv`/`PF_TAG_CENSUS.tsv` ต้องตรงไบต์ต่อไบต์ (ใบตรวจ 07:30 ได้ตรงแล้ว — ยืนยันซ้ำ)

**จ็อบ 3 (ข้อบังคับจากใบตรวจ) — เพิ่ม mutation guard ที่ `field_offset`**
4. กลายพันธุ์ `field_offset` ของข้อความที่สถานะ `VALIDATED` (เช่น `TargetPosVital:W:1` จาก `+0x14` เป็น `+0x99`
   — เคสที่ใบตรวจ 07:30 พบว่า `build_schemas()` ยอมรับตารางผิดเงียบ ๆ) → **บังคับว่าผลตรวจ capture ต้องรายงาน `mismatch > 0`**
5. 🔴 **ถ้าไม่แดง (mismatch = 0) = การ์ดไม่ครอบคลุมการทุจริตชนิด `field_offset` — ต้องแก้การ์ดจนแดง**
   (บทเรียน D4/D5 รอบ 118: guard ที่ทำแดงไม่ได้ = หลักฐานปลอม) · เก็บ log การรัน mutation ทั้งก่อน (คาดเขียว) และหลังกลายพันธุ์ (ต้องแดง)

### pass criteria — **STATIC-ON-BRIDGE (span/schema + sha256 + re-derive · ชั้นเดียว)**
**ชั้น static (ชั้นเดียวของใบนี้):**
- ตัวเลขชี้ขาดของสองข้อความ: parse ok / fail / **mismatch รายฟิลด์** ต่อ `GSCN_RunTimeProtocolReq` (W) และ `GSCN_RunTimeProtocolRes` (R)
  พร้อมสถานะปลายทาง (`VALIDATED` หรือ `A2_STATIC_OPEN` + เหตุผล) · จำนวนเฟรมที่ประมวลจริงต้องเท่า 40,747 / 10,073 (หรืออธิบายส่วนต่าง)
- re-derive จ็อบ 2: sha256 ของ TSV ที่สกัดใหม่ = sha256 ของชุดส่งมอบ (ยืนยัน schema สดจากอิมเมจ)
- จ็อบ 3: log สองรอบ — ก่อนกลายพันธุ์ (เขียว) และหลังกลายพันธุ์ `field_offset` (**mismatch > 0 / แดง**) · ถ้าไม่แดง ต้องแนบ patch การ์ดที่ทำให้แดง
- sha256 ของอิมเมจ + ของ capture ก่อน-หลังตรงกัน (เปิดอ่านอย่างเดียว) · สคริปต์/การรันซ้ำได้พร้อม guard count + exit 0

**ชั้น client-observable:** 🔴 **ว่างเปล่าโดยเจตนา** — ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย · ห้ามอ้าง static เป็นหลักฐานว่าจอเห็นอะไร

### 🔴 ผลลบมีค่าเท่าผลบวก
- **mismatch > 0** ⇒ ข่าวใหญ่: schema ของ Codex ไม่ตรง capture ที่ฟิลด์ไหน จำนวนเท่าไร ⇒ ชี้จุดที่ต้อง re-derive · หยุด จดตัวเลข
- **parse ok เต็ม 50,820 → `VALIDATED`** ⇒ ปิด F2 · แต่ **ยังห้ามอ้าง "0 mismatch" ลอย ๆ** (ดู nonclaims)
- **การ์ด mutation ไม่แดง** ⇒ พบช่องโหว่ของ validator เอง = ผลที่มีค่า ⇒ แนบ patch ที่ทำให้แดง แล้วรันซ้ำ

### nonclaims (ติดไปกับตัวเลขทุกครั้ง — 🔴 ห้ามอ้าง "0 mismatch" โดยไม่ติดสามข้อนี้)
- **F1** — ตัวเลข 11,904 instance ถูกแบกด้วย `CheckSecondPwdVital` (R) **9,166 = 77%** ใบเดียว + หางบาง 34 คู่ ·
  **ห้ามอ่านว่า "ตารางโปรโตคอลถูกยืนยันกว้าง ๆ"** — มันคือข้อความง่ายใบเดียวปริมาณมาก
- **F2** — ก่อนใบนี้ปิด สองข้อความนี้ยัง `A2_STATIC_OPEN` (static ล้วน) · ผลของใบนี้ยกได้เฉพาะสองข้อความนี้ ไม่ใช่ทั้งตาราง
- **F3** — 980 คู่ (95%) เป็น `NOT_OBSERVED` · 37 คู่ (3.6%) `VALIDATED` · "0 mismatch" ไม่พูดถึง 980 คู่นั้นเลย
- แถวที่ `status = VALIDATED` เท่านั้นนับเป็นหลักฐานสองชั้น · เวลาอ้างในเอกสารต้องเขียน `ยืนยันด้วย capture` หรือ `static ล้วน` เสมอ
  **ห้ามเขียนคำว่า "ยืนยันแล้ว" เฉย ๆ**
- **ไม่ claim ว่ารู้ความหมายของ tag** เกิน len (`0x2A`=float32/4 · `0x12`=uint16/2 · ที่เหลือ UNKNOWN ตามที่ Codex ประกาศ)
- **ไม่พึ่ง `PF_RUNTIME_CLASSMAP.tsv` เป็นชื่อคลาส** — 6,244 แถว UNKNOWN 100% (บันทึกผลลบ ไม่ใช่แหล่งชื่อ)
- **การประกอบ/ตีความของเราไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล
- **result:** (ผู้รับงาน static บนสะพานกรอก: ตัวเลข parse ok/fail/mismatch รายฟิลด์ของสองข้อความ + สถานะปลายทาง ·
  sha256 re-derive จ็อบ 2 · log การ์ด mutation ก่อน/หลัง (+patch ถ้าต้องแก้) · เวลา · sha อิมเมจ+capture ก่อน-หลัง)


## 🔬 GT-048 NATIVE-SPAWN-CONDITION-001 [STATIC-ON-BRIDGE]: อิมเมจ client มีเส้นทาง "สร้าง/วาง entity hostile ตอน scene-load จากข้อมูลที่ ship มากับ client เอง" หรือ entity ทุกตัวต้องมาจากเรคคอร์ด wire ของเซิร์ฟเวอร์ — ตอบด้วย VA/span/sha  [✅ **PASS (STATIC) — ปิดโดย chief R127 จากผล 2026-08-23 14:20-14:50 (+07:00) · GT-034 ไม่ปิด**]

### ✅ บล็อกผล (R127 · ผลเต็ม: `notes_to_chief\20260823_1450_GT048-PASS-native-scene-npc-placement-path.md`)
- **native path มีจริง:** client อ่าน placement จาก `Data\Scene\Save\bg0001\bg0001.npc` ตอน scene-load
  ผ่าน `SceneNPCCreation` (`0x0043A9D0` trigger · loader `0x00439E90` · parser `0x00439780` ·
  per-placement create `0x0043A6F0`) — ชื่อคลาสจาก RTTI จริง ไม่ใช่ชื่อเดา · **ไม่รอ wire และไม่ผ่าน `0x0089A640`**
- **แถว P30/TID31 Tornado Eagle เจอเป๊ะ:** f32 triple `(1747.524..., -7837.697..., 931.041...)` พบครั้งเดียว
  ใน `bg0001.npc` offset `0x1D46` — Y/Z ตรง GT-034 ทุกบิต X ต่าง +100 ตาม scenario
- indirect census ครบ (`E8/E9` ทุกไบต์ + dword refs = 0 ค้าง) · image sha ไม่เปลี่ยน
- 🔴 **สิ่งที่ผลนี้ไม่พิสูจน์:** ไม่พิสูจน์ว่า path นี้รันจริง/render Tornado Eagle ใน GT-034 · **GT-034 ยังไม่ปิด**
  ต้องอ่านคู่ GT-045 (แหล่งป้อน wire) — GT-048 = แหล่งป้อนข้อมูล client · คนละแหล่ง ห้ามอ่านแทนกัน

**ที่มา:** คำตัดสิน Panya `notes_to_chief\20260823_1315_PANYA-DECISION-GT034-option1-static-spawn-condition.md`
(ทาง ① — ร่างใบ STATIC-ON-BRIDGE หาเงื่อนไข spawn ก่อนตัดสินระหว่างทาง ② กับ ③) ·
สืบเนื่องจาก GT-034 NO-RESULT (กรณี 3: ไปถึงพิกัดคาดจริงแต่กวาด 360 องศาแล้วไม่เห็นตัวนกเลย —
`notes_to_chief\20260822_2359_GT034-NO-RESULT-native-render.md`)

**หมวด:** STATIC-ON-BRIDGE — ต้องเปิด `GameClient.local.bin` จึงทำบน cloud clone ไม่ได้ ·
ผู้รับงานคือคนที่นั่งหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม · ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว ·
กติกา stamp 420 นาที / teardown / canonical DB ไม่เกี่ยวกับใบนี้ (ไม่บูตอะไรทั้งสิ้น)

### ทำไมใบนี้ตอบ GT-034 NO-RESULT (ต้องอ่านก่อนทำ)
GT-034 กรณี 3 = "ไม่เห็นตัวนกเลย" ซึ่งใบ GT-034 นิยามไว้ชัดว่าเป็น **NO-RESULT ของคำถามหลัก ไม่ใช่ผลลบ**
(ผลลบนิยามแคบ = "เห็นตัวแต่ชื่อ/กรอบไม่แดง" เท่านั้น) ⇒ แยกไม่ออกระหว่างสองความเป็นไปได้:
  (i) client ไม่ spawn มอนจากข้อมูลของตัวเองเลย — entity ทุกตัวต้องรอเรคคอร์ดจาก wire
  (ii) entity มีอยู่จริงแต่ไกล/มุมอื่น/ติดเงื่อนไข render อื่น
ใบนี้แยกสองอันนี้ที่ชั้น static:
- **ถ้าไม่พบเส้นทาง native spawn** ⇒ การไม่เห็นนก **ไม่ใช่ความผิดพิกัด** แต่เป็นเพราะเซิร์ฟเวอร์ของเรา
  ไม่เคยส่งเรคคอร์ด spawn ⇒ **เขียนรายงานเสนอ Panya** ว่าทาง ② หมดเหตุผล และเสนอเมนูใหม่
  (เลน server-side spawn record) ให้เธอตัดสิน — **ห้ามเริ่มออกแบบ/เขียนโค้ดเองก่อนคำเคาะ** (1315 §③)
- **ถ้าพบเส้นทาง native spawn** ⇒ การไม่เห็นนกกลายเป็นคำถามเรื่อง render/ระยะ/มุม ⇒ ทาง ② (หลายจุดสังเกต) มีเหตุผล
🔴 ใบนี้ **reframe** NO-RESULT เท่านั้น — ยังไม่ปิด GT-034 (ดู nonclaims)
**อ่านผลใบนี้คู่กับ GT-045 (คำสั่ง Panya 1315 §③)** — GT-045 ตอบว่าไคลเอนต์วาดวัตถุพิกัดโลก
"ที่เซิร์ฟเวอร์ส่งมา" ได้ไหม · GT-048 ตอบว่าไคลเอนต์สร้างจาก "ข้อมูลของตัวเอง" ได้ไหม · สองใบคนละแหล่งป้อน

### objective (claim เดียว)
**ในอิมเมจ `GameClient.local.bin` มีเส้นทางโค้ดที่สร้าง/วาง entity hostile ตอน scene-load
จากตารางข้อมูล placement ที่ ship มากับ client เอง (ไม่ต้องรอเรคคอร์ดจาก wire) หรือไม่ —
ตอบด้วย VA/span/sha ของ constructor + ตัวเรียก หรือรายงานว่าไม่พบเส้นทางเลย
(entity ทุกตัวเข้าทางเดียวคือ READ ฝั่ง wire `0x0089A640`)**

### db / server args
**ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client** — เปิดอ่านอิมเมจอย่างเดียว

### สิ่งที่ต้องมี (precondition · verify ก่อนเริ่ม)
- **อิมเมจ (sha/size เดียวกับที่ GT-046 พิน):** `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · PE32 · ImageBase `0x00400000`
  🔴 **จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง เปิดอ่านอย่างเดียวเสมอ**
- **ท่าทำงาน:** ตามวินัย `pf-static-re` · 🔴 **ห้ามใช้ linear disassembler เป็นหลักฐานของ negative**
  (หยุดที่ไบต์แรกที่ decode ไม่ได้แล้วรายงาน negative มั่นใจ = ความผิดพลาดรอบ 83) ·
  census ด้วย byte matching (`E8`/`E9 rel32` ทุกออฟเซ็ต) + ไล่ indirect (call ผ่านตาราง/vtable) ·
  สวีป exec section ทั้งสอง: `.text` (`0x00401000`, Vsize `0x00838A2C`) และ `.code` (`0x00C3A000`, Vsize `0x2E1`)
- **verify sha ของทุก span ก่อนพึ่งด้วยตัวเอง** · sha ไม่ตรงแม้ตัวเดียว = หยุด รายงาน span ที่เพี้ยน ห้าม re-derive ทับ

### แหล่งข้อมูล placement + จุดเทียบฝั่ง wire (verify sha ก่อนพึ่งทุกตัว)
- **ตาราง placement ของ roster (13 ตัว + XYZ) ที่เราใช้:** `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS`
  ใน `current/pf_login_game_server_v141.py` (115 แถว · identity = `0x2000 + pidx + 1`)
  🔴 **นี่เป็นตารางฝั่งเซิร์ฟเวอร์ของเรา ไม่ใช่ในอิมเมจ client** — ใช้เป็น "ชุดค่าที่คาดหวัง"
  เพื่อไล่หาว่า **อิมเมจ client มีตาราง placement ของตัวเองที่ให้ค่าชุดเดียวกันหรือไม่**
  (แหล่งอ้างอิง: `FACTPACK_R102_HOSTILE13_ROSTER.md` · เป้าใบ GT-034 = `0x201F` Tornado Eagle
  XYZ `(1747.5, -7837.7, 931.0)` retaliate-only)
- **ตารางข้อมูลมอบที่ ship มากับ client** (ถ้ามี native spawn ต้องอ่านจากพวกนี้): `MOBS.json` (v97_mapping_audit) ·
  `STANDARD_MOB` (ตาราง 027 · `B_CONSTDATA_TH.pc_.dec` offset `0x351094`) ·
  `AI_WANDER` (ตาราง 024 · offset `0x329A46`) — ที่มาตาม factpack
- **จุดเทียบฝั่ง wire (พิสูจน์แล้วตั้งแต่ GT-040 · verify sha ก่อนพึ่ง):**
  stream primitive `0x0089A600` (WRITE) / `0x0089A640` (READ) — เส้นทาง "entity มาจากเรคคอร์ด wire"
  ต้องขี่ผ่าน READ `0x0089A640` · เชิงโครงสร้างเทียบกับ actor-entry collection + derived bit `0x02/0x04/0x08`
  ของ GT-040 (อ้างใน GT-047) และ list `0x5F85B0` ของ GT-045
- **VA ของตาราง placement ฝั่ง client และ constructor ที่ scene-load เรียก:** ยังไม่มีในไฟล์ที่ chief อ่าน —
  **ผู้รับงานบนสะพานต้องหาเอง**

### จ็อบ (ทำตามลำดับ 1 -> 2 -> 3 -> 4)
1. หาว่าในอิมเมจมี **ตาราง/โครงสร้าง placement** (พิกัด XYZ + identity/tid ต่อ instance) ที่ให้ค่าตรงกับ
   `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` หรือไม่ — census literal XYZ ของ `0x201F` และ/หรือ identity `0x201F` ใน section ข้อมูล
   🔴 **ห้าม grep ด้วยค่าปัดในใบนี้ (`1747.5, -7837.7, 931.0`) — จะ miss แน่นอน** · ค่า float เต็มให้อ่านจากแถว `0x201F`
   ของ `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` ใน `current/pf_login_game_server_v141.py` บนสะพานโดยตรง แล้วประกอบ
   byte pattern เป็น IEEE-754 float32 little-endian เอง · จุด cross-check: GT-034 วัดค่าที่เซิร์ฟเวอร์ส่งจริง (จุดวางผู้เล่น
   = placement + 100X) = `x 1847.5244140625 · y -7837.69775390625 · z 931.0413208007812` ⇒ ค่าตารางต้องสอดคล้อง
   (Y/Z ตรง · X ต่างกัน 100 พอดี) — ถ้าไม่สอดคล้อง = หยุด รายงาน อย่า census ต่อ
   · ถ้าไม่พบ literal ให้ระบุว่าไล่ที่ไหนบ้าง (ไม่พบ = ข้อมูล · ลอง float64 และ fixed-point ก่อนประกาศไม่พบ)
2. **ใครอ่านตารางนั้น** — census `E8/E9 rel32` + indirect ของฟังก์ชันที่แตะฐานตาราง placement นั้น
3. **เส้นทางไปถึงตัวสร้าง entity ตอน scene-load หรือไม่** — ตามสายจากตัวอ่านตาราง (จ็อบ 2) ว่าไปเรียก
   entity-constructor ในเฟรม scene-load (โหลดแมพ) โดยไม่รอ input จาก wire หรือไม่ · ระบุ VA constructor + span
4. **เทียบกับเส้นทางสร้าง entity จากเรคคอร์ด wire** — ยืนยันว่าเส้นทาง (3) แยกต่างหากจากเส้นทางที่ป้อนผ่าน
   READ `0x0089A640` (actor-entry collection ของ GT-040) จริง หรือทั้งสองมาบรรจบที่ constructor เดียวกัน
   (ถ้าบรรจบตัวเดียวกัน = constructor เป็นกลาง แต่ **ตัวจุดชนวน** ต่างกัน — จดว่าฝั่ง scene-load มีตัวจุดชนวนของตัวเองไหม)

### pass criteria — **STATIC-ON-BRIDGE (span + sha256 + re-derive · ชั้นเดียว)**
**ชั้น static (ชั้นเดียวของใบนี้):**
- verify sha ของ **ทุก** span ที่พึ่งก่อน re-derive · sha ไม่ตรง = หยุด รายงาน ห้าม re-derive ทับ
- ตอบ objective เป็นประโยคเดียวได้อย่างใดอย่างหนึ่ง:
  `client สร้าง entity hostile ตอน scene-load จากตาราง placement ที่ <VA> ผ่าน constructor <VA> ตัวจุดชนวน <VA>`
  **หรือ** `ไม่พบเส้นทาง native spawn (ไล่ census E8/E9 + indirect ครบทั้ง .text/.code แล้ว) — entity เข้าทาง READ 0x0089A640 เท่านั้น`
- แนบ span `[start,end)` + file offset + len + sha256 ของ **ทุก** ฟังก์ชันที่อ้าง (รูปแบบเดียวกับ GT-040/GT-042/GT-044/GT-046)
- ระบุ **สถานะการไล่ indirect** ให้ชัด (ครบ/ไม่ครบ + ที่ยังค้าง)
- sha256 อิมเมจก่อน-หลังตรงกัน · ถ้าเขียนสคริปต์ commit ลง `tools/` แบบรันซ้ำได้พร้อม guard count + exit 0

**ชั้น client-observable:** 🔴 **ว่างเปล่าโดยเจตนา** — ใบนี้ไม่ผลิตหลักฐานชั้นนี้ ·
ไม่มีเกมให้บูต ผู้เทสหน้าจอไม่ต้องทำอะไรกับใบนี้เลย · ห้ามใครอ้าง static เป็นหลักฐานว่าจอเห็นหรือไม่เห็นนก

### 🔴 ผลลบมีค่าเท่าผลบวก
- **"ไม่พบเส้นทาง native spawn เลย"** (ไล่ census + indirect ครบ) = ผลที่มีค่าเท่าการเจอ ⇒
  การไม่เห็นนกใน GT-034 ไม่ใช่ความผิดพิกัด ⇒ chief **เขียนรายงานเสนอ Panya ตัดสิน** (เลน server-side
  spawn record เป็นเมนูใหม่นอกทาง ②/③ — ยังไม่มีใครอนุมัติ · 1315 §③ สั่งรอผลสองใบแล้วให้ Panya เคาะ)
  🔴 แต่ต้องระบุว่าไล่ indirect ครบหรือยัง — "ไม่พบ" ≠ "ไม่มี" ถ้ายังเรียกผ่าน table/indirect ที่ยังไม่ไล่
- **เจอเส้นทาง native spawn** = GT-034 NO-RESULT กลายเป็นคำถาม render/ระยะ/มุม ⇒ เป็นข้อมูลให้เหตุผลกับทาง ②
  (หลายจุดสังเกต) — **แต่ทาง ② ยังไม่อนุมัติจนกว่า Panya เคาะ** (1315 §②)

### nonclaims (ติดไปกับผลทุกกรณี)
- **static ไม่พิสูจน์รันไทม์** — พิสูจน์ได้แค่ว่ามี/ไม่มีเส้นทางในอิมเมจ ไม่ใช่ว่ารันจริงตอน scene-load
- 🔴 **ห้ามอ้างว่าใบนี้ตอบ/ปิด GT-034** จนกว่าจะมีหลักฐานประกอบ (ผล GT-045 + การบูตจริงหนึ่งรอบ) — ใบนี้ **reframe** เท่านั้น
- **"ไม่พบเส้นทาง" ≠ "client ไม่ spawn"** ถ้ายังไล่ indirect ไม่ครบ — ต้องระบุสถานะการไล่
- faction / AI / drops / placement **เป็นข้อมูลที่ ship มากับ client** ไม่ใช่พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล
- **ไม่ claim ว่ารู้ชื่อคลาส** ของ entity/record — vtable ไม่มี RTTI/name literal · ห้ามเดาชื่อ = ห้ามประดิษฐ์ wire format
- **การย้ายจุดวาง/ตีความ placement เป็นดีไซน์ของเรา** — ห้าม claim ว่าผู้เล่นจริงเคยเกิดตรงนั้น
- **result:** (ผู้รับงาน static บนสะพานกรอก: ประโยคทิศทาง native-spawn/ไม่พบ + VA · span/file-offset/len/sha256 ทุกฟังก์ชัน ·
  สถานะการไล่ indirect · เวลา · sha อิมเมจก่อน-หลัง)


## 🆕🔬 GT-049 LOOT-CHAT-TEMPLATE-001 [STATIC-ON-BRIDGE]: หา template ของบรรทัดสีเขียว `ได้รับ [<ชื่อ>] * <จำนวน>` ในตารางข้อความ/`B_CONSTDATA` แล้วไล่ static ว่า "ใครยิง id นั้น" — เลนคลิกเมาส์ของ GT-046 (0x1F/0x03/0x22) หรือเลนที่สอง (อาจ inbound ผ่าน READ 0x0089A640)  [✅ **PASS/DONE — จ็อบ 2–4 ปิดโดยผลหน้าสะพาน 2026-08-24 09:23 (+07:00) · บันทึกโดย chief R144 · จุดยิง id 131 (`0x83`) มี 2 จุด: `0x005CC309` (global chat emitter — ตัวจริง) + `0x00578E00` (local UI object) · chain: `ItemOperateVitalRes` vtable `0x00F30668` slot `+0x1C` handler `0x005EF5E0` → `0x005A8A00` → extractors → emitter — serializer มีขา READ 5 จุด + capture เห็น R 5/5 W 0/0 ⇒ เลน inbound · template สตริงไม่ resident ใน PE (packed) จึงไม่มี static string VA — ใช้ id immediate เป็น anchor · nonclaim: ไม่พิสูจน์ runtime occurrence ของเฟรมคลิป**]

> ✂️ **SCOPE-CUT (chief R132 · 2026-08-23 ~22:0x +07:00 · จากจดหมาย `20260823_2150_GAMEDATA-EXTRACTED-…`):**
> **จ็อบ 1 ปิดแล้ว — ไม่ต้องหา template อีก:** ตาราง `pf_bridge\gamedata\tables\TEXTDATA_TH__MESSAGE.tsv` (907 แถว 4 คอลัมน์ · อ่านครบ 907/907)
> มีแถว **id `0x83` (131) col2=1 ค่า `ได้รับ [ $V1 ] * $V2`** — ตรงกับบรรทัดเขียวในคลิป (`$V1`=ชื่อไอเทม `$V2`=จำนวน)
> และ message id ทั้งสามของ handler GT-046 bound แล้ว: `0x1F`(31)=`ระยะทางไกลเกินไป!` · `0x03`(3)=`ช่องว่างในกระเป๋าไม่เพียงพอ…` ·
> `0x22`(34)=`ไอเทมของผู้อื่น ไม่สามารถเก็บขึ้นมาได้!` — **ทั้งสามเป็นข้อความล้มเหลวทั้งหมด** ⇒ [ตีความ] handler แจ้งเฉพาะเก็บไม่สำเร็จ ·
> `ได้รับ` น่าจะยิงจากระบบกระเป๋าตอนของเข้าจริง — **ยังเป็น [ตีความ] จนกว่าจ็อบ 2-4 จะเจอจุดยิง id 131 ในไบนารี**
> ⚠️ หมายเหตุแหล่ง: จ็อบ 1 เดิมชี้ `B_CONSTDATA` แต่ template จริงอยู่ฝั่ง **TEXTDATA_TH** (ตัวถอดใหม่ `gamedata\pf_extract_gamedata.py` ·
> id 131 มาจากตาราง MESSAGE ไม่ใช่ VA — **จ็อบ 2 ยังต้องหา VA ของสตริง/ดัชนี template ในอิมเมจเองก่อน census**) ·
> `gamedata\` อยู่บนดิสก์สะพานเท่านั้น ยังไม่เข้า git (รอ Panya เคาะ) · ช่องบังคับใหม่: กรอก `ค้น gamedata แล้ว: …` ในผลด้วย

**พ่อของใบนี้:** GT-046 PICKUP-DIRECTION-001 (**PASS · ปิด R127**) · ใบนี้ปิดช่องว่างที่ GT-046 จดไว้เองด้วยคำนี้:
> *"No static link from any of these three message IDs (`0x1F`/`0x03`/`0x22`) to the green `received [name] * quantity` chat template was found."*

**ที่มา:**
- `notes_to_chief\20260823_1520_ERRATUM-my-terrainthing-hypothesis-is-dead-plus-missing-chat-template-lane.md` **ท่อน ④** (ข้อเสนอที่ใบนี้ลงมือทำ — คำต่อคำ)
- `notes_to_chief\20260823_1435_GT046-PASS-outbound-mouseclick-runtime-drop-object.md` (ผล GT-046 ที่เปิดช่องว่าง · จ็อบ 4 + nonclaim)

ทำไมสำคัญกว่าที่เห็น: คลิปเห็นบรรทัด `ได้รับ [ Red leaves Hammer ] * 1` **สีเขียว** โผล่ในเฟรมเดียวกับตอนค้อนหาย
แต่เลนคลิกเมาส์ที่ GT-046 พิสูจน์แล้ว (outbound · `WM_LBUTTONDOWN` · response `0xFC->0x1F` `0xFD->0x03` `0xFE->0x22`)
**ต่อไม่ถึงบรรทัดนั้นเลย** · ถ้าเลนที่ยิงบรรทัดสีเขียวเป็น **inbound (server-push ผ่าน READ `0x0089A640`)**
⇒ เซิร์ฟเวอร์เป็นคนตัดสินผลการเก็บ **⇒ เปลี่ยนดีไซน์เซิร์ฟเวอร์ทั้งเลนลูท**

**หมวด:** `STATIC-ON-BRIDGE` — ต้องเปิด `GameClient.local.bin` + TSV ส่งมอบของ Codex บนสะพาน จึงทำบน cloud clone ไม่ได้ ·
ผู้รับงานคือคนที่นั่งหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม · **ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว** ·
กติกา stamp 420 นาที / teardown / canonical DB ไม่เกี่ยวกับใบนี้ (ไม่บูตอะไรทั้งสิ้น)

### objective (claim เดียว)
**หา template ของบรรทัดสีเขียว `ได้รับ [<ชื่อ>] * <จำนวน>` (received `[<name>] * <qty>`) ใน string table / `B_CONSTDATA`
ของอิมเมจ ระบุ template/message id + VA ของสตริง แล้วไล่ static ว่า id นั้นถูกยิงจากที่ใด —
ชี้ให้ได้ว่าเชื่อมกับข้อความใดใน 3 ตัวของ GT-046 (`0x1F`/`0x03`/`0x22`) หรือมาจากเลนแยกตัวที่สอง
(สงสัย inbound ผ่าน READ `0x0089A640`) หรือรายงานว่าไม่พบ template / ไม่พบ static link เลยหลัง census indirect ครบ**

### db / server args
**ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client** — เปิดอ่านอิมเมจ + อ่าน TSV ส่งมอบอย่างเดียว
🔴 **ห้ามแก้ อิมเมจ / capture / TSV ส่งมอบ — เปิดอ่านอย่างเดียวทั้งหมด**

### สิ่งที่ต้องมี (precondition · verify ก่อนเริ่ม)
- **อิมเมจ (sha/size เดียวกับที่ GT-046/GT-048 พิน):** `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · PE32 · ImageBase `0x00400000`
  🔴 **จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง เปิดอ่านอย่างเดียวเสมอ**
- **ตารางข้อความ/B_CONSTDATA:** ไฟล์ฝั่งภาษาไทยที่แสดง `ได้รับ` (เช่น `B_CONSTDATA_TH.pc_` ที่ decode แล้ว) ·
  จด offset/ขนาด/sha256 ของไฟล์ที่พึ่ง
- **TSV ส่งมอบ RE ของ Codex ที่ `pf_bridge\external\`** (verify จำนวนแถวตามที่ใบตรวจ 07:05 นับ):
  `PF_PROTOCOL_REGISTRY.tsv` 520 บรรทัด · `PF_SERIALIZER_FIELDS.tsv` 6,932 · `PF_TAG_CENSUS.tsv` · `PF_FIELD_VALIDATION.tsv` ·
  `PF_RUNTIME_CLASSMAP.tsv` 6,244 แถว (UNKNOWN 100% — ห้ามพึ่งเป็นชื่อคลาส)
- **ท่าทำงาน:** ตามวินัย `pf-static-re` · 🔴 **ห้ามใช้ linear disassembler เป็นหลักฐานของ negative**
  (หยุดที่ไบต์แรกที่ decode ไม่ได้แล้วรายงาน negative มั่นใจ = ความผิดพลาดรอบ 83) ·
  census ด้วย byte matching (`E8`/`E9 rel32` ทุกออฟเซ็ต) + dword refs (data xref ไปยัง VA ของ id/สตริง) + vtable slots ·
  สวีป exec section ทั้งสอง: `.text` (`0x00401000`, Vsize `0x00838A2C`) และ `.code` (`0x00C3A000`, Vsize `0x2E1`)
- **verify sha ของทุก span ก่อนพึ่งด้วยตัวเอง** · sha ไม่ตรงแม้ตัวเดียว = หยุด รายงาน span ที่เพี้ยน ห้าม re-derive ทับ

### ของที่มีอยู่แล้ว (จาก GT-046 PASS · verify sha ก่อนพึ่ง)
```
response mapping    status 0xFC -> message 0x1F  ·  0xFD -> 0x03  ·  0xFE -> 0x22
handler             [0x005EF640,0x005EF66F) len 47  sha 5d17fc4fdeeafde0a4a34e900e76d0336e404f8d2f058ba085044ae8d88d602e
serializer          [0x005E5E30,0x005E5E83) len 83  sha 8e439d4f3ff1479e723b220d8dd78a262b41df3b74839da9d4cb728f69773066
stream primitive    0x0089A600 (WRITE / outbound)  ·  0x0089A640 (READ / inbound)  [GT-040]
gap ที่ต้องปิด      ไม่พบ static link จาก 0x1F/0x03/0x22 -> บรรทัดสีเขียว `ได้รับ`
```

### จ็อบ (ทำตามลำดับ 1 -> 2 -> 3 -> 4)
1. ~~**หา template สตริง**~~ ✅ **ปิดแล้ว R132 (จดหมาย 2150):** template = `TEXTDATA_TH__MESSAGE.tsv` id **131 (0x83)** ค่า `ได้รับ [ $V1 ] * $V2` ·
   สิ่งที่จ็อบนี้ยังไม่ให้คือ **VA ของสตริง/ดัชนี template ในอิมเมจ** — หาใน 2 (ค้นไบต์จริงของสตริง/id 131 ในอิมเมจ · verify กับ `gamedata\tables\` ก่อน)
2. **ไล่ว่าใครอ้าง VA ของสตริง/แถวนั้น** — census `E8/E9` + dword ref ที่โหลด VA สตริง/ดัชนี template นั้นเข้ารีจิสเตอร์
3. **ตามขึ้นไปหาตัวยิง** — ฟังก์ชันที่ format บรรทัดนี้ลง chat log ถูกเรียกจากที่ใด · เทียบว่า
   (ก) มาจาก handler/เลนของ `0x1F`/`0x03`/`0x22` (เลนคลิกเมาส์ของ GT-046) หรือ
   (ข) มาจากเลนแยกที่ป้อนผ่าน READ `0x0089A640` (server-push · actor-entry/notify) · ระบุ VA + span ของจุดยิง
4. **ตัดสินทิศทางเลน** — ถ้าจุดยิง (จ็อบ 3) ขี่ผ่าน READ `0x0089A640` = **inbound (เซิร์ฟเวอร์ตัดสิน)** ·
   ถ้าขี่ผ่านเลน outbound-response ของ GT-046 = **เลนเดียวกัน (ไคลเอนต์แสดงผลจาก response ของตัวเอง)** · จดพร้อม xref chain

### pass criteria — **STATIC-ON-BRIDGE (span + sha256 + census · สองชั้น)**
**ชั้น static (ชั้นที่ผลิตตัวเลขของใบนี้):**
- verify sha ของ **ทุก** span/ไฟล์ที่พึ่งก่อน re-derive · 🔴 **sha ไม่ตรงแม้ตัวเดียว = หยุด รายงาน span ที่เพี้ยน ห้าม re-derive ทับ**
- ตอบ objective เป็นประโยคเดียวได้อย่างใดอย่างหนึ่ง:
  `template ได้รับ อยู่ที่สตริง <VA> id <id> ถูกยิงจาก <VA> ซึ่งขี่เลน inbound READ 0x0089A640` **หรือ**
  `... ถูกยิงจากเลน response 0x1F/0x03/0x22 (เลนเดียวกับ GT-046)` **หรือ**
  `ไม่พบ template ในตารางข้อความ (ไล่ทุก encoding แล้ว)` **หรือ**
  `พบ template ที่ <VA> แต่ไม่พบ static link ไปตัวยิงใด (census E8/E9 + dword ref + vtable slot ครบทั้ง .text/.code แล้ว)`
- แนบ **template id + VA สตริง + xref chain (VA/span/sha256 ของทุกฟังก์ชันที่อ้าง)** รูปแบบเดียวกับ GT-040/GT-042/GT-046/GT-048
- ระบุ **สถานะการไล่ indirect ให้ชัด** (E8/E9 direct + dword refs + vtable slots — ครบ/ไม่ครบ + ที่ยังค้าง · สไตล์ census ของ GT-048)
- sha256 อิมเมจ + ไฟล์ B_CONSTDATA + TSV ก่อน-หลังตรงกัน · ถ้าเขียนสคริปต์ commit ลง `tools/` แบบรันซ้ำได้พร้อม guard count + exit 0

**ชั้น client-observable:** 🔴 **ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้** (เหมือน GT-047/GT-048) ·
ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย · ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย** ·
🔴 **ห้ามใครอ้าง static เป็นหลักฐานว่าจอเห็นบรรทัดสีเขียวจากเลนใด** — คนละชั้นหลักฐานกับคลิป

### 🔴 ผลลบมีค่าเท่าผลบวก
- **"ยิงจากเลน inbound READ `0x0089A640`"** = ข่าวใหญ่ ⇒ เซิร์ฟเวอร์ตัดสินผลการเก็บ ⇒ **redirect ดีไซน์เซิร์ฟเวอร์เลนลูททันที**
- **"ยิงจากเลน response `0x1F/0x03/0x22`"** = ปิดช่องว่าง GT-046 ⇒ ไคลเอนต์แสดงบรรทัดจาก response ของตัวเอง (เลนเดียว)
- **"ไม่พบ template" / "ไม่พบ static link"** = ผลที่มีค่าเท่าการเจอ ⇒ **แต่ต้องเขียนกำกับว่า census ไล่ไปถึงไหน**
  (E8/E9 direct + dword refs + vtable slots ครบทั้ง `.text`/`.code` หรือยัง) · "ไม่พบ" ≠ "ไม่มี" ถ้ายังไล่ indirect ไม่ครบ

### nonclaims (ติดไปกับผลทุกกรณี)
- **static ไม่พิสูจน์ว่าเลนใดรันจริงในเฟรมที่คลิปเห็นบรรทัดสีเขียว** — พิสูจน์ได้แค่ว่ามี/ไม่มีเส้นทางในอิมเมจ
- **การเจอ template ไม่พิสูจน์ว่าเลนใดวิ่งในเฟรมที่วัด** (`~163 s`) — คนละชั้นหลักฐานกับคลิป
- **ไม่ claim เรื่องเพ็ต** ว่าเกี่ยวหรือไม่เกี่ยวกับการยิงบรรทัดนี้ — pet UI ในคลิปถูก facecam บังจนอ่านโหมดไม่ได้ (ERRATUM 15:20 §③)
- **ไม่ claim เรื่องเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล · การตีความเลน/ดีไซน์เซิร์ฟเวอร์เป็น **งานออกแบบของเรา**
- **ไม่ claim ว่ารู้ชื่อคลาส** ของ record/notify — vtable ไม่มี RTTI/name literal · ห้ามเดาชื่อ = ห้ามประดิษฐ์ wire format
- **ไม่พึ่ง `PF_RUNTIME_CLASSMAP.tsv` เป็นชื่อคลาส** — UNKNOWN 100% (บันทึกผลลบ ไม่ใช่แหล่งชื่อ)
- **"ไม่พบ static link" ≠ "ไม่มีเลนที่สอง"** ถ้ายังไล่ indirect ไม่ครบ — ต้องระบุสถานะการไล่
- **result:** (ผู้รับงาน static บนสะพานกรอก: ประโยคทิศทางเลน + template id + VA สตริง · xref chain span/file-offset/len/sha256 ทุกฟังก์ชัน ·
  สถานะการไล่ indirect (E8/E9 + dword ref + vtable slot · ครบ/ค้าง) · เวลา · sha อิมเมจ+B_CONSTDATA+TSV ก่อน-หลัง)


## GT-051 RENDER-SYNTHESIS-001 [เอกสารล้วน · ✅ **DONE — chief cloud ทำเองเสร็จใน R128 (2026-08-23 ~18:1x +07:00) · ไม่ใช่งานสะพาน ไม่มีอะไรให้ผู้เทสทำ**]

**ผลเต็ม:** `pf_bridge/FINDINGS_R128_GT051_RENDER_SYNTHESIS.md` — อ่านที่นั่น ใบนี้เป็นแค่ stub กันเลขห้อยลอย
**คำตอบย่อหนึ่งย่อหน้า (ภาษาสมมติฐาน — ห้ามอ่านเป็นข้อเท็จจริง):** ตั้งสมมติฐาน **RENDER-DISCRIMINATOR-H1
(ฉบับ identity-band)**: ไคลเอนต์วาด entity จาก wire actor_entry เมื่อ identity อยู่ใน band native ของฉากที่โหลด
(`0x2000+1..0x2000+N`) หรือเป็นตัวผู้เล่นเอง — โดย wire **override ตำแหน่ง/template ได้** (ARENA V1 · SCENE-007
หักล้างรูปแรง "อัปเดตของเดิมในที่เดิมเท่านั้น" ของร่างแรกไปแล้ว — pf-adversary จับ) · identity นอก band ไม่วาด
(หลักฐานแข็งใบเดียว: GT-030 · แคบ · ติด confound actor_type 2 — "actor_type คือตัวแยก" ยังอธิบายข้อมูลได้เท่ากัน) ·
สอดคล้องทุกเคสที่ตรวจ แต่**ยังไม่พิสูจน์** และการกวาดเอกสารยุคก่อน GT อาจยังไม่ครบ · จุดตรวจถูกสุด = **GT-053**
(band ของ scene 2 ≥ 61 ไหม — ท้ายไฟล์) · เลนดาเมจไม่กระทบ (overlay แยกเชิงพฤติกรรม) · เลนลูท: GT-045 v2 attended
= ตัวทดสอบข้างเคียง (bit 0x08 เป็นคนละชนิดเรคคอร์ดกับ actor_entry)


---

📇 **ใบ static ใหม่ตั้งแต่ R128 เป็นต้นไปไม่อยู่ไฟล์นี้แล้ว** — อยู่ที่ **`CLIENT_RE_QUEUE.md`** (คำสั่ง Panya 18:22 · ตอนนี้: GT-053 · GT-052 · GT-050) · ใบเทสเกม attended ยังเปิดที่ไฟล์นี้เช่นเดิม

---

## ⭐ GT-058 LEARN-SKILL-RESULT-001 [attended, in-game]: ไคลเอนต์ "ทำอะไร" กับเฟรม CLearnSkillResultVital (0x673C) เมื่อรับ sweep 5 สเต็ป — อัปเดตหน้าต่างสกิล / ขึ้นบรรทัดแชต / ไม่เห็นอะไร / หลุด  [✅ **CLOSED — BOUNDED-NEGATIVE (คำตัดสิน Panya 2026-08-24 ~21:1x +07:00 · จดหมาย `notes_to_chief\20260824_2120_PANYA-RULINGS-6-items-attended-unpaused-and-triple-scenario.md` §③ "ปิดเลย" · ปิดโดย chief R155)** — ชั้น wire: PASS (sweep `0x673C` 5 เฟรมรับครบ frame-sha ตรง pin · ผลหน้าสะพาน R145) · ชั้น client-observable: BOUNDED-NEGATIVE / NO-CRASH — **ขอบเขตที่บันทึกตามคำตัดสิน: "เทียบเนื้อในหน้าต่างสกิลไม่ได้ เพราะ baseline เปิดหน้าต่าง K ไม่ได้"** · อาการ "เปิดหน้าต่างสกิลไม่ได้" ย้ายไปเป็นคำถามของ `GT-059` (ซึ่งปิด P2/FALSIFIED แล้ว — ดูใบถัดไป) — ไม่ค้างสองใบด้วยเหตุเดียวกัน]

> 🟡 **สถานะ R145 (2026-08-24 ~11:xx +07:00 · chief cloud — บริโภคผลหน้าสะพาน 3 ใบ: `0953` + correction `1037` + addendum `1056`):**
> **ชั้น wire:** ✅ PASS — client รับ sweep `0x673C` ครบ 5 เฟรม (37/50/50/77/77 bytes · frame sha256 ตรง pin ทั้ง 5 · raw `GAME_20260824_094807_404629_62314.txt`) · version byte `0` ไม่ทำให้ reject/crash
> **ชั้น client-observable:** 🟡 **BOUNDED-NEGATIVE** — ทั้ง 5 สเต็ปไม่มี skill window/list เปลี่ยน · ไม่มีแถวแชต/system message ใหม่ · HP/HUD/แมพเดิม · หลัง sweep client ยังรับ input Q/X ได้ = **NO-CRASH / responsive**
> 🔴 **finding ใหม่ (correction `1037` หลัง Panya ทัก · addendum `1056`):** หน้าต่างสกิล **(K) เปิดไม่ได้เลยใน local baseline นี้** — tooltip `สกิล (K)` แสดงแต่ทั้ง hotkey K และคลิกไอคอนตรง ๆ ไม่เปิดหน้าต่าง ทั้งก่อนและหลัง sweep · **control พิสูจน์ว่าไม่ใช่ input/focus พัง:** `C`=CHARACTER เปิดได้ · `Quest(J)`/`Reward` เปิดได้ · เฉพาะเส้นทางเปิด Skill window ที่ตาย · **wire control:** ช่วงกด K ทุก C2S frame (#21–#178, 158 เฟรม) เป็น `GSCN_RunTimeProtocolReq` heartbeat 12 ไบต์ล้วน — **ไม่มี application request วิ่งตอนกด K** ⇒ อาการอยู่ฝั่ง client ล้วน ไม่ถึง server · สาเหตุภายในยังไม่พิสูจน์
> ⇒ **เทียบ content ภายใน skill window ไม่ได้** เพราะเปิดหน้าต่างไม่ได้ ⇒ **NO-RESULT ต่อ objective หลักของใบ (ไคลเอนต์อัปเดตอะไรใน skill window)** · คำถามถึง Panya: ปิดใบที่ bounded-negative (0x673C เดี่ยวไม่ขยับ UI) หรือค้างรอเปิด skill-window ให้ได้ก่อน?
> 🔧 **ผู้เทสเสนอแก้ pass criteria:** ใบสั่งกำหนดทั้ง "sessions selected +1" และ "run-copy ไบต์ตรงก่อน-หลัง" ซึ่งขัดกันเอง (session ถูก persist ⇒ ไบต์ต้องเปลี่ยน) — ผลจริงคือ **row-diff ทุกตารางต่างเฉพาะ `sessions` +1 แถว (selected char 1, lease 12) ตามที่ใบเองคาด** ⇒ เสนอเปลี่ยน "byte-identical" เป็น "row-diff-except-one-expected-session" · **chief เห็นด้วย** — บันทึกเป็นข้อเสนอถึง Panya (ไม่แก้ pass criteria เองเพราะเป็น attended ที่ Panya ขับ)

> 📎 **สถานะแวดล้อม (R139 · 2026-08-24 04:5x +07:00): เงื่อนไข (ก) ปิดแล้ว** — PR โค้ด #14 merge เข้า `main` แล้ว (merge commit `9691bcc` · commit เลน `e34d91f` เป็น ancestor ของ `origin/main` ยืนยันด้วย `merge-base --is-ancestor`) · gate เขียว(Actions run 32668480284 · **subset ไม่ใช่ gate เต็ม** · verdict `success` จาก `ci-status:ci/e34d91f….json` · ref `refs/pull/14/merge`) · ยืนยันซ้ำบน clone `main` ฝั่ง cloud: โมดูลเทสของเลน 84 passed / 22 skipped เปิดเผย / 220 subtests และสวีตเต็ม เขียว(cloud sanity 1976/324/0) ⇒ **(ก) จบ** · **ใบยังพักตามคำสั่ง 16:56 — ห้ามบูตจนกว่า Panya ปลดพัก** และตอนบูตต้องเช็ค (ข) BOOT_COMMIT มี `9691bcc` เป็น ancestor

> 🔬 **หมายเหตุ chief R146 (2026-08-24 ~11:5x +07:00 · ไม่ปิดใบ ไม่แก้ pass criteria — เพิ่มเส้นทางปลดล็อกเท่านั้น):** finding "หน้าต่างสกิล (K) เปิดไม่ได้" มี **สมมติฐานต้นเหตุ (ยังไม่พิสูจน์)** จากจดหมาย correction `1147`: client มีข้อมูลสกิลครบ แต่ **server เราไม่เคยส่ง skill STATE (`CSkillModule`/`CSkillAttr`)** ⇒ หน้าต่างอาจไม่มีอะไร populate · pf-static-re R146 ยืนยันว่ารูปไบต์ของสองคลาสนี้ **ปิดบน cloud ไม่ได้** (serializer row EMPTY · capture NOT_OBSERVED · id เป็น name-hash candidate) ⇒ เปิดใบ **RE-061 SKILLSTATE-WIRE-DIRECTION-001** (`CLIENT_RE_QUEUE.md`) เป็นใบทดสอบสมมติฐาน · **ลำดับปลดล็อก GT-058:** RE-061 ปิด wire (static) + ตอบจากอิมเมจว่าไคลเอนต์มี inbound decoder + skill-window-open ขึ้นกับ state ไหม → **บวก** chief เปิดเลนโค้ด sender (opt-in · headless proof) แล้ว rerun GT-058 attended · **ลบ** ตัวขวางมีสาเหตุอื่น ไม่เปิด sender · **UNANSWERABLE** (corpus เป็น emulator-only ตอบ direction ต้นฉบับไม่ได้ — SCENE-013) → รอ Panya ตัดสิน · 🔴 **ใบนี้ยังพัก/ค้างเหมือนเดิม ไม่ถูกปิดด้วยรอบ unattended**

> 🔬 **หมายเหตุ chief R149 (2026-08-24 ~22:xx +07:00 · ไม่ปิดใบ):** เส้นทางปลดล็อกที่ R146 วางไว้ **เดินครบแล้ว** — RE-061 ปิดออกทาง **บวก** (gate `0x761ED0` บน `CSkillAttr` พิสูจน์จากอิมเมจ) ⇒ chief เปิดเลนโค้ด sender แล้ว (**HYP-PF-035** · PR #21 รอ gate) ⇒ ใบ attended ตัวต่อคือ **GT-059 SKILL-ATTR-WINDOW-GATE-001** (ถัดจากใบนี้ในไฟล์) · ผล GT-059 คือสิ่งที่จะตัดสินว่า GT-058 ปิดที่ bounded-negative หรือ rerun ได้จริง *(อัปเดต R150: PR #21 merge เข้า `main` แล้ว `543382c` · เขียว(Actions run 32706893952 · subset) — สถานะปัจจุบันดูหัวใบ GT-059)*

> 🔴 ~~**รอ gate เขียว + merge ก่อน:** เลน server (opt-in scenario) ยังอยู่บน branch `claude/amazing-goodall-bcc9z5` · PR ยังไม่ merge เข้า `main` — **ใบนี้ยังบูตไม่ได้** จนกว่า (ก) PR merge แล้ว~~ *(ปิดแล้ว — ดู 📎 R139 ข้างบน)* และ (ข) resolver คืน BOOT_COMMIT ที่มีเลนนี้ · **และ** (ค) เลน attended ถูกปลดพักโดย Panya — ~~ทั้งสามข้อต้องครบ~~ **เหลือ (ข)+(ค)**

**ที่มา:** ครึ่ง wire ปิดแล้วที่ **GT-050** (`CLearnSkillResultVital` codec CLOSED · จดหมาย `notes_to_chief\20260824_0055_*`):
รูปสายจริงคือ `count u16` (tag `0x12`) + records ยาว 12 ไบต์ `(u32 tag 0x14 / u16 tag 0x12 / u32 tag 0x14)` + trailing `u8` (tag `0x0B`) ·
msg tag `0x673C` · **version byte = 0 เป็นดีไซน์ของเรา ยัง unpinned** · 🔴 **ความหมายของฟิลด์ใน record (u32/u16/u32) ยังไม่รู้ — opaque** ·
ครึ่งที่ใบนี้ตอบคือ **client-observable: ไคลเอนต์ทำอะไรกับเฟรมพวกนี้** (อัปเดต skill window? ขึ้นบรรทัดแชต? ไม่เห็นอะไรบนจอ? disconnect?) —
คำตอบ "จอไม่ขึ้นอะไร" เป็นผลที่ใช้ได้จริง (bounds ว่า `0x673C` เดี่ยว ๆ ทำอะไรได้/ไม่ได้)

### objective (claim เดียว)
**เมื่อเซิร์ฟเวอร์ตอบ chat-input trigger หนึ่งครั้งด้วย sweep 5 เฟรมของ `CLearnSkillResultVital` (`0x673C`) ที่ count/trailing ต่างกันตามพินด้านล่าง ไคลเอนต์แสดงพฤติกรรมอะไรบนจอ และ NO-CRASH หรือ CRASH**
(ใบนี้พิสูจน์พฤติกรรม client เท่านั้น — ไม่ตีความว่าฟิลด์ใน record หมายถึงอะไร)

### 5 เฟรมของ sweep (พินตามลำดับที่เซิร์ฟเวอร์ต้องยิง · count = u16 record count · TRAIL = trailing u8 ที่ +0x2C ค่า 0/1)
```
1. LEARN_SKILL_RESULT_SWEEP_COUNT0_TRAIL0   (count=0, trail=0)
2. LEARN_SKILL_RESULT_SWEEP_COUNT1_TRAIL0   (count=1, trail=0)
3. LEARN_SKILL_RESULT_SWEEP_COUNT1_TRAIL1   (count=1, trail=1)
4. LEARN_SKILL_RESULT_SWEEP_COUNT3_TRAIL0   (count=3, trail=0)
5. LEARN_SKILL_RESULT_SWEEP_COUNT3_TRAIL1   (count=3, trail=1)
```
- เฟรมเว้นระยะแบบเดียวกับ stats sweep (spacing เดียวกัน) ⇒ **ต้องอัดวิดีโอ/continuous capture** ไม่ใช่ภาพนิ่งอย่างเดียว
- 🔴 **version byte 0 เป็นดีไซน์ของเรา ยัง unpinned:** ถ้าไคลเอนต์ reject/หลุดตั้งแต่เฟรมแรก **จุดต้องสงสัยอันดับหนึ่งคือ version byte** ไม่ใช่ record semantics — จดให้ชัด

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)
- **P1:** จอมี skill window / รายการสกิล อัปเดต (เพิ่ม/เปลี่ยน) ที่เฟรม count>0 · เฟรม count=0 อาจเป็น no-op หรือ clear
- **P2:** ไม่มีอะไรบนจอเปลี่ยนเลยทั้ง 5 เฟรม — เป็นผลลบที่สมบูรณ์ (bounds ว่า `0x673C` เดี่ยว ๆ ไม่พอจะขยับ UI ที่ตามองเห็น)
- **P3:** ขึ้นบรรทัดแชต/ข้อความระบบแทนที่จะแตะ skill window
- **P4:** ไคลเอนต์ reject/หลุดที่เฟรมใดเฟรมหนึ่ง ⇒ ชี้ version byte 0 ก่อน (ดูข้อ pin ด้านบน)

### 🔴 ก่อนบูต — resolve commit เขียว (ท่าเดียวกับ GT-045 · รันเครื่องมือ ไม่ใช่ก๊อป SHA)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` (detached HEAD ถูกแล้ว)
- **exit 3** + `BOOT_COMMIT: NONE` ⇒ ห้ามบูต จดว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · **exit 2** = พาธผิด/git ล้ม
- 🔴 บรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ จดลงผลเสมอ
- **ยืนยันสี่ข้อกับ `<SHA>` ที่จะบูตจริง (ต้องครบทั้งสี่):**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "learn-skill-result-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/learn_skill_result_hypothesis_learn_sweep.json && echo SCENARIO_PRESENT
git grep -n "COUNT3_TRAIL1" <SHA> -- src/pirateforce_foundation/ scenarios/
```
1. ไฟล์คำตัดสินมี `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ (success = subset บน Actions ไม่ใช่ gate เต็ม)
2. `git grep` เจอ flag จริง — **ห้ามใช้ `--help` เป็นหลักฐาน** (คืน 0 บรรทัดผ่านสะพาน — บทเรียนรอบใหญ่ #7 ข้อ 6)
3. เห็นคำว่า `SCENARIO_PRESENT`
4. เจอ label สเต็ปที่ 5 (`COUNT3_TRAIL1`) ในซอร์ส — ยืนยันว่าเป็น sweep 5 สเต็ปจริง ไม่ใช่เลนเก่า
- **อ่านค่า pin ต่อเฟรม (label + sha256) จาก manifest ของ scenario ที่ merge แล้ว** (จดหมาย `20260824_0055_*` เป็นแหล่งอ้างอิง wire shape · **ค่า sha ตัวจริงอ่านจาก scenario ตอน merge — ห้ามฝังเลขเดาในใบนี้**)
- ไม่ครบสี่ข้อ + ยังไม่ได้ค่า pin = **ห้ามบูต** ใบนี้อยู่ BLOCKED ต่อ

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-058_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt058.sqlite3
```
- เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง** (canonical เปิดอ่านไม่ได้ตลอดรอบ)
- เลนนี้ **read-only by design** — DB สำเนา (`run_gt058.sqlite3`) ต้อง **ไบต์ตรงกันก่อน-หลัง** ด้วย (ดู pass criteria ชั้น 1)
- ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกบูต (สำเนา DB ใหม่ทุกครั้ง — เผื่อเวลาเดินไว้)

### server args (เป๊ะ — opt-in เท่านั้น · `production_allowed=false`)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt058.sqlite3 --learn-skill-result-hypothesis-scenario scenarios\learn_skill_result_hypothesis_learn_sweep.json
```
- **opt-in เท่านั้น ห้าม default-on** (บังคับในโค้ด: mutually exclusive กับ scenario โหมดอื่นทุกโหมด + ต้องมี `--db` ชี้ไฟล์ที่มีจริง + `production_allowed=false`)
- หัวหน้าต่าง console ของ server จะขึ้น mode `learn-skill-result-hypothesis` — ใช้เช็คว่าบูตถูกโหมด
- ⚠️ **การยิงมาจาก chat trigger หนึ่งบรรทัดเท่านั้น** — sweep 5 เฟรมออกหลังจากเซิร์ฟเวอร์รับ chat-input frame ที่ตรง predicate

### 🔴 ตัว trigger แชต — 12 ตัวอักษร printable ASCII เป๊ะ (บทเรียนที่เคยเสียเวลาโปรเจกต์)
- predicate ของ chat trigger คือ **12 ตัวอักษร printable ASCII พอดี** — สั้นกว่านั้นถึงเซิร์ฟเวอร์แต่ **เงื่อนไขเงียบ ๆ ไม่ผ่าน** (ไม่มี error) ⇒ sweep ไม่ออกและดูเหมือนเลนพัง
- **อ่านสตริงจริง 12 ตัวจากซอร์สก่อนพิมพ์:** `git grep -n "trigger" <SHA> -- src/pirateforce_foundation/learn_skill_result*.py` — จดสตริงเป๊ะ นับให้ครบ 12 ตัว
- 🔴 **ตัวอักษรที่พิมพ์ตอนช่องแชตไม่โฟกัส = hotkey** ⇒ ต้อง **คลิกเข้าช่องแชตให้โฟกัสก่อน** แล้วค่อยพิมพ์ · พิมพ์ครบ 12 ตัวแล้วกด Enter หนึ่งครั้ง

### steps
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบตามบล็อก db
1. เปิด server ก่อน client เสมอ (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client) — ขึ้น mode `learn-skill-result-hypothesis`
2. เปิด client (`Invoke-CimMethod Win32_Process Create`) → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร
   → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
3. เข้าแมพ เห็น HP/minimap/ชื่อแมพ/`[ระบบ] : Pirate Force local server online` → **ถ่าย S0** (สภาพก่อนยิง · ถ้ามีปุ่ม/หน้าต่างสกิล เปิดค้างไว้ให้เห็น baseline)
4. **เริ่มอัดวิดีโอ/continuous capture ก่อน** (เฟรม spacing แบบ stats sweep — ภาพนิ่งพลาดได้)
5. **คลิกช่องแชตให้โฟกัส** → พิมพ์ trigger 12 ตัว ASCII (อ่านจากซอร์สตามบล็อกด้านบน · นับให้ครบ 12) → กด Enter หนึ่งครั้ง
6. **มองจอต่อเนื่อง ~30 วินาที** ระหว่าง sweep 5 เฟรมทยอยออก → ถ่าย **S1..S5** ทีละสเต็ป (COUNT0_TRAIL0 → ... → COUNT3_TRAIL1)
   จดต่อสเต็ป: หน้าต่างสกิล/รายการสกิลเปลี่ยนไหม · มีบรรทัดแชต/ข้อความระบบไหม · ไม่มีอะไรเลยไหม
7. **จับ NO-CRASH / CRASH ชัดเจน:** client ยังอยู่และตอบสนอง (ขยับกล้อง `Q/E` ได้) = NO-CRASH · ถ้าหลุด/ค้าง/หน้าต่างปิด = CRASH + จดว่าหลุดที่เฟรมที่เท่าไร (ชี้ version byte 0 ก่อน) *(🔴 **หมายเหตุ chief R163 — ไม่ใช่การแก้ขั้นตอน:** ใบนี้**ปิดไปแล้ว** ขั้นตอนข้างบนคือขั้นตอนที่รันจริงในรอบนั้น **จึงคงไว้ตามเดิมทั้งตัวอักษร** · ฉบับแรกของ R163 เขียนทับมัน ซึ่งผิดกติกา — `pf-adversary` จับได้ ถอนแล้ว · **ถ้ารอบนั้นใช้ `Q/E` จริง แปลว่ามี `TargetPosVital` ออกกลางรอบ ซึ่งเป็นข้อเท็จจริงที่กระทบการอ่านผล ห้ามลบร่องรอย** · สำหรับรอบ **ใหม่** ให้ใช้ **คลิกขวาค้างลากเมาส์** เช็ค NO-CRASH แทน — เหตุผลอยู่ในบล็อกกฎกล้องของ PLAYBOOK)*
8. ออกจากเกม: **X** มุมขวาบน (ตรวจก่อนว่าหน้าต่างแอปตัวเองไม่บังปุ่ม X) → dialog ยืนยัน → ปุ่มซ้าย
9. ปิด server เก็บ raw GAME log + console out/err → `PRAGMA integrity_check;`
10. **teardown เสมอ** แม้เลิกกลางคัน (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 — เพดานยกจาก 180 เมื่อ 2026-08-20 · `TEMPLATE_teardown_generic.ps1:135` · ใช้ `staged\TOOL_stop_stale_server.ps1` สำหรับแท่นที่ถูกทิ้งข้ามชั่วโมง)
11. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม

### pass criteria — สองชั้น แยกกันเด็ดขาด
**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ · ทำ headless ได้)**
- raw GAME log มี **5 เฟรม `0x673C`** ที่เซิร์ฟเวอร์ dispatch จริง เรียงตามลำดับพิน:
  `..._COUNT0_TRAIL0` → `..._COUNT1_TRAIL0` → `..._COUNT1_TRAIL1` → `..._COUNT3_TRAIL0` → `..._COUNT3_TRAIL1` อย่างละ 1 ครั้ง
- แต่ละเฟรมตรง **label + sha256 พิน** ที่อ่านจาก manifest ของ scenario ตอน merge (ค่า pin มาจาก scenario — ไม่ใช่เลขเดาในใบ) · เก็บ hexdump ทั้งไฟล์ **ห้ามลบ**
- โครงสาย (GT-050-proven) ที่ต้องเห็นในทุกเฟรม: `count u16 tag 0x12` · record 12 ไบต์ `(u32 0x14 / u16 0x12 / u32 0x14)` · trailing `u8 0x0B` · msg tag `0x673C`
- **DB สำเนา `run_gt058.sqlite3` ไบต์ตรงกันก่อน-หลัง** (เลน read-only by design) + `PRAGMA integrity_check` = `ok`
- `sessions`: `count(*) WHERE selected_character_id IS NOT NULL` +1 ต่อการเข้าเกมหนึ่งครั้ง · sha256 canonical ก่อน-หลังตรงกัน
- **ชั้นนี้ตอบไม่ได้:** จอทำอะไร (การมีเฟรมออกไม่พิสูจน์ว่าไคลเอนต์วาด/อัปเดต/หลุด) ⇒ **ห้ามอ้างชั้นนี้แทนชั้น (2)**

**ชั้น (2) client-observable (ต้องมีคนหน้าจอ)**
- ภาพ **S0..S5** + วิดีโอต่อเนื่องช่วง sweep · sha256 ทุกไฟล์
- ตอบเป็นภาษาคน **ต่อสเต็ป:** หน้าต่างสกิล/รายการเปลี่ยนไหม · บรรทัดแชต/ข้อความระบบขึ้นไหม · ไม่มีอะไรเลยไหม
- **NO-CRASH / CRASH verdict ชัดเจน** (ถ้า CRASH: หลุดที่เฟรมที่เท่าไร)
- **ชั้นนี้ตอบไม่ได้:** ภาพหน้าจอไม่ใช่หลักฐานว่าเฟรมออกจากเซิร์ฟเวอร์จริง **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

### 🔴 ผลลบมีค่าเท่าผลบวก
- **wire ครบ 5 เฟรมแต่จอไม่ขึ้น/ไม่เปลี่ยนอะไรทั้ง 5 สเต็ป** = ผลลบที่สมบูรณ์ **ไม่ใช่ FAIL** ⇒ bounds ว่า `0x673C` เดี่ยว ๆ ไม่พอจะขยับ UI ที่สังเกตได้ · redirect: ต้องหา trigger/สถานะประกอบอื่น (จดว่าเลนถัดไปควรลองอะไร)
- **NO-CRASH โดยไม่มีการเปลี่ยนบนจอ** = ยืนยันว่า client รับเฟรมได้ (version byte 0 ผ่าน) แต่ไม่มี UI hook ที่ตามองเห็น — เป็นข้อเท็จจริงที่ใช้ได้
- **CRASH ที่เฟรมแรก** = ชี้ version byte 0 (ดีไซน์เรา ยัง unpinned) ก่อน record semantics

### nonclaims (ติดไปกับผลทุกกรณี)
- **ไม่ตีความว่าฟิลด์ใน record (u32/u16/u32) หมายถึงอะไร** — semantics ยัง opaque · ใบนี้วัดพฤติกรรม client เท่านั้น
- **ไม่ claim ว่าเซิร์ฟเวอร์ต้นฉบับ (ปิดไปแล้ว กู้ไม่ได้ตลอดกาล) เคยใช้เฟรมนี้แบบนี้** — การประกอบเฟรม/version byte เป็นดีไซน์ของเรา
- **ไม่ claim ว่า count/trailing ที่ต่างกัน map กับความหมายเชิงเกมใด ๆ** — sweep นี้ทดสอบ tolerance/พฤติกรรม ไม่ใช่ decode ความหมาย
- **ไม่พิสูจน์ทิศทาง (client ส่งกลับหรือไม่)** — ใบนี้ inbound-only observe
- **result:** (ผู้เทสกรอก: ภาพ S0..S5 + วิดีโอ พร้อม sha256 · คำตอบต่อสเต็ป "จอเปลี่ยนอะไร" ภาษาคน · NO-CRASH/CRASH verdict (+เฟรมที่หลุดถ้ามี) · path raw GAME log + label/sha 5 เฟรม · เวลา · sha canonical ก่อน-หลัง · sha `run_gt058.sqlite3` ก่อน-หลัง)


## GT-059 SKILL-ATTR-WINDOW-GATE-001 [attended, in-game]: ส่ง `CSkillAttr` (attr block `0x1661` ขี่ `UpdateAttrVital` `0x309A`) แล้วหน้าต่างสกิล (K / ปุ่ม `Bt_main_Skill` ล่างซ้าย -> `Skill_Main2`) เปิดได้ไหม  [✅ **CLOSED — P2 (FALSIFIED) โดย chief R155 · ตัวปิด = คำยืนยันด้วยตาของ Panya บนวิดีโอต่อเนื่องทั้งสองไฟล์ (2026-08-24 ~21:33 +07:00 · จดหมาย `notes_to_chief\20260824_2133_PANYA-VISUAL-SIGNOFF-GT059-negative-confirmed-on-continuous-video.md`)** — สมมติฐานที่ถูกหักล้าง: *"client รับ `CSkillAttr` แล้วหน้าต่างสกิลจะเปิดได้"* — **ไม่จริง** · สองชั้นแยกขาด: **wire = byte-exact PASS** (S1 สอง trigger · S2 หนึ่ง trigger · `COUNT0` 57B → `COUNT1` 68B ห่าง 3.0s · sha ตรง pin ทุกเฟรม — จดหมาย `1757`) · **client = ตา Panya บนวิดีโอต่อเนื่อง `1091_...s1_FULLROUND...mkv` (51,633,077 B) + `1093_...s2_FULLROUND...mkv` (24,957,564 B): "ดูหมดแล้ว ไม่เห็นมีอะไรขึ้นมาเลย"** — K ×4 · ปุ่ม Skill ×2 · รวม session relog ที่ไม่เคยกด K มาก่อน · control: `C` เปิด CHARACTER ได้ทั้งสอง session = เกมไม่ค้าง · เข้าเงื่อนไขปิดใบที่ chief วางใน R152b ครบ (คนดูเอง + วิดีโอต่อเนื่อง ไม่ใช่ point-sample) · 🔴 **nonclaims ที่ปิดใบนี้ไม่ได้กลบ (ยกจากจดหมาย 2133 ทั้งก้อน):** ① **A/B ยัง UNRESOLVED** — ไม่มีใครกด K ในช่อง 3 วิ `COUNT0`→`COUNT1` เลย วิดีโอจึง**ไม่ตอบ**ว่า "ถ้ากด K ตรงนั้นจะเปิดไหม" ⇒ เปิดใบต่อ **GT-064** (ใบใหม่ท้ายไฟล์ — มือคนกดได้ · attended ปลดพักแล้ว) ② **ไม่รู้สาเหตุ** — เคส (ก) slot `[actor+0x3E8]` null จริง vs (ข) slot มีของแต่ check อื่นใน `0x761ED0` ขวาง ยังแยกไม่ได้โดยไม่มีตัววัด runtime — เงื่อนไข "เลื่อนออกแบบตัววัดไปหลังผลลบยืนยัน" (คำเคาะ 2120 §④) **ครบแล้ว** ⇒ งานออกแบบตัววัด runtime เปิดได้ ③ ไม่อ้างข้ามชั้น · 🔴 **ห้ามลบวิดีโอสองไฟล์บนสะพาน — หลักฐานชิ้นเดียวที่ปิดใบนี้** (เกินเพดาน 2 MB เข้า repo ไม่ได้)]  *(สถานะเดิมก่อนปิด: เงื่อนไข (ก) ปิดแล้ว R150 —* PR #21 **merge เข้า `main` แล้ว** (`543382c` · head `01b8b9e` เขียว(Actions run 32706893952 · subset) — sha ตรงไฟล์ `ci-status` · conclusion `success`) · R150 ตรวจซ้ำบน `main` แล้ว: verify สี่ข้อของใบนี้ผ่านครบ (flag `app.py:103` · `SCENARIO_PRESENT` · label `COUNT1_KEY1` เจอทั้งโมดูล+scenario · mode string `skill-attr-hypothesis` `app.py:506`) + พิน `frame_size` 57/68 ในไฟล์ scenario ตรงกับใบ — **เหลือ (ข) resolver คืน BOOT_COMMIT ที่มีเลนนี้ตอนบูต · (ค) เลน attended ถูกปลดพักโดย Panya — ต้องครบทั้งสองข้อ** · 🆕 **R152: มีรอบ UNATTENDED แล้วหนึ่งรอบ (2026-08-24 17:31-17:55 +07:00 · ผู้เทส local ตามคำสั่ง Panya · จดหมาย `notes_to_chief\20260824_1757_GT059-NO-RESULT-unattended-no-skill-window-wire-exact.md`): ชั้น wire = byte-exact PASS** (3 triggers · 6 เฟรม 57→68B ห่าง 3.000-3.001s · SHA ตรง pin ทุกเฟรม · DB row-diff `sessions` +1 ต่อ session · canonical ตรงก่อน-หลัง) · **ชั้น client = provisional "ไม่พบ window ในรอบนี้ ทุกจุดวัด S0/S2-S6 รวม relog variant · ยังไม่ได้วัดผลลบโดย Panya"** · S1 (K ใน 3 วิ) เก็บไม่ทัน — A/B UNRESOLVED ห้ามใช้ S2 แทน S1 · **ใบคงสถานะ PENDING/NO-RESULT — ห้ามปิดเป็น P2/falsify จากรอบ unattended** (กฎ AGENTS.md §9) · ตัวปิดใบ = Panya ยืนยันภาพ negative จาก evidence หรือรัน attended เอง — **เงื่อนไขข้อนี้คือข้อที่ R155 ปิดสำเร็จด้วยจดหมาย 2133)*

**ที่มา (สองใบที่ใบนี้ต่อยอด — อ่านก่อนบูต):**
- **GT-058 finding (correction `1037` + addendum `1056`):** local baseline เปิดหน้าต่างสกิล **(K) ไม่ได้เลย** — hotkey K และคลิกไอคอนตรง ๆ ไม่เปิด ทั้งที่ `C`/`Quest(J)`/`Reward` เปิดได้ปกติ · ช่วงกด K ไม่มี application request วิ่งเลย (C2S เป็น heartbeat 12 ไบต์ล้วน) ⇒ อาการอยู่ฝั่ง client
- **RE-061 (DONE · จดหมาย `notes_to_chief\20260824_1437_RE-061-RESULT-SKILLATTR-GATE-PINNED.md`):** พินจากอิมเมจ (static) ว่า controller init ของ `Skill_Main2` ที่ `0x761ED0` **return false เมื่อ `[actor+0x3E8]` (`CSkillAttr`) ยังไม่พร้อม** (ctor `0x760DE0` อ่าน slot นี้) · `CSkillAttr` ไม่ใช่ vital เดี่ยว — เป็น attr block `class_id 0x1661` ขี่ `UpdateAttrVital 0x309A` · เส้นทาง apply ฝั่งรับมีจริง (`0x5F2400` -> `0x751C70`) · 🔴 **NONCLAIM ของ RE-061 ที่ใบนี้เกิดมาทดสอบ: หนึ่งแพ็กเก็ตยังไม่ถูกพิสูจน์ว่า "พอ" ให้หน้าต่างเปิด** — init มี base/UI check อื่นก่อน/หลัง gate
- **เลน server (R149 · HYP-PF-035 SKILL-ATTR-001):** โมดูล `src/pirateforce_foundation/skill_attr_hypothesis.py` · scenario id `skill_attr_hypothesis_attr_sweep` · flag `--skill-attr-hypothesis-scenario` · `production_allowed=false` · ต้องมี `--db` ชี้ไฟล์ที่มีจริง · mutually exclusive กับทุกโหมดอื่น · `database_write=none` (read-only by design)
- ✅ **คำถาม RE-062 ตอบแล้ว (DONE · ผลหน้าสะพาน 2026-08-24 17:01 +07:00 · บันทึก R152):** คำตอบคือ **(ค) เส้นทางอื่น — ไม่มีแขนงใดใน decoder/handler/lookup/insert/bind/apply ที่เขียน `[actor+0x3E8]`**: inbound สร้าง `CSkillAttr` ชั่วคราวผ่าน factory ได้จริง แต่ handler resolve target ด้วย class id `0x1661` ใน **generic attribute map** (ไม่ใช่ dedicated slot) · slot `[actor+0x3E8]` ถูกสร้างตั้งแต่ `CMyActor` ctor (`0x44CBC1`) · bind thunk อ่าน slot ที่ `0x4698DF` โดยไม่สร้าง — slot null ⇒ apply ตรวจ null แล้ว return (no-op, ไม่ repair) ⇒ **ถ้า runtime slot เป็น null จริง sweep นี้พลิก gate ไม่ได้เชิงโครงสร้าง** — แต่ ctor สร้าง slot ไว้ก่อนแล้วโดย normal construction จึงยังต้องวัด runtime ว่าเคสจริงอยู่ฝั่งใด (จดหมาย `notes_to_chief\20260824_1701_RE-062-RESULT-INBOUND-OTHER-PATH-NO-SLOT-WRITE.md`)

### objective (claim เดียว)
**เมื่อไคลเอนต์รับ attr block `CSkillAttr` (`0x1661` ใน `0x309A`) จากเซิร์ฟเวอร์เราแล้ว พฤติกรรมการเปิดหน้าต่างสกิล (K / `Bt_main_Skill`) เปลี่ยนจาก baseline ของ GT-058 หรือไม่ — เปิดได้ (มี/ไม่มีรายการ) หรือยังเปิดไม่ได้เหมือนเดิม**
(ใบนี้ทดสอบ "sufficiency" ของการรับ `CSkillAttr` ต่อ window gate เท่านั้น — ไม่ตีความความหมายของฟิลด์ใด)

### sweep 2 เฟรมต่อหนึ่ง trigger (พินตามลำดับ · spacing 3.0 s · ยิงซ้ำได้ ไม่ one-shot)
```
1. HYP_PF_035_SKILL_ATTR_COUNT0_EMPTY   (record_count=0 · body ว่างที่สุดที่ well-formed · frame 57 bytes)
2. HYP_PF_035_SKILL_ATTR_COUNT1_KEY1    (1 record: key=1, opaque_u16=0, opaque_u32=0 · ค่า probe ตามใจเรา ความหมายไม่รู้ · frame 68 bytes)
```
- 🔴 **ข้อจำกัดเชิงดีไซน์ที่ต้องรู้ก่อนวางมือ:** trigger หนึ่งครั้ง = ออก **ทั้งสองเฟรม** ห่างกัน 3.0 วินาที — แยกยิงทีละ variant ไม่ได้ ⇒ การเทียบ A/B ทำผ่าน (ก) กด K ในหน้าต่าง 3 วิ ระหว่างเฟรม (best-effort · ให้วิดีโอตัดสินทีหลังว่า K ลงก่อน/หลังเฟรม 2) และ (ข) สถานะหลัง sweep จบ (ตัวที่ apply ล่าสุด = COUNT1_KEY1) · **ถ้ากด K ไม่ทันหน้าต่าง 3 วิ ให้จดว่า "A/B แยกไม่ได้ในรอบนี้" ตรง ๆ ห้ามแต่งผล**
- 🔴 **identity guard:** เลนยิงเฉพาะเมื่อตัวละครที่ select คือ probe identity ที่พิน (`identity_lo 0x10010001` = ตัวละครแรกของ account แรกบน store สำเนาสด) — **ต้องเลือกตัวละครช่องแรก** · ถ้าไม่ตรง เลนปฏิเสธเงียบ (event `skill_attr_hypothesis_identity_not_pinned_no_reply`)
- 🔴 **version byte 0 ของ vital เป็นดีไซน์เรา ยัง unpinned** — ถ้า client reject/หลุดตั้งแต่เฟรมแรก จุดต้องสงสัยอันดับหนึ่งคือ version byte ไม่ใช่ตัว attr block

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)
- **P1:** หลังรับเฟรม K เปิดหน้าต่างได้ — COUNT0_EMPTY ให้หน้าต่าง**ว่าง** · COUNT1_KEY1 ให้มีอะไรโผล่ 1 แถว/ช่อง
- **P2:** K ยังเปิดไม่ได้เหมือนเดิมทั้งก่อน-หลัง — **ผลลบที่สมบูรณ์** ⇒ falsify "รับ `CSkillAttr` แล้วพอ" (ตรง NONCLAIM ของ RE-061 — gate `0x761ED0` มี check อื่นขวางอยู่ หรือ `[actor+0x3E8]` ไม่ได้ populate จากเลนรับนี้ — RE-062 DONE ตอบแล้วว่าเลนรับ**เขียน slot ไม่ได้เชิงโครงสร้าง**: ต้องแยกเคส `slot null (เลนรับซ่อมไม่ได้)` ออกจาก `slot non-null + gate อื่นขวาง` ด้วยหลักฐาน runtime)
- **P3:** เปิดไม่ได้ใน session ที่รับเฟรม แต่**เปิดได้หลัง relog ที่รับเฟรมก่อนกด K ครั้งแรก** — ชี้ว่า gate อ่าน slot ตอน controller construction (จังหวะสำคัญกว่าการรับ)
- **P4:** client reject/หลุด — ชี้ version byte 0 ก่อน record semantics

### 🔴 ก่อนบูต — resolve commit เขียว (ท่าเดียวกับ GT-058 · รันเครื่องมือ ไม่ใช่ก๊อป SHA)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` · **exit 3** = ใบนี้รอ gate ไม่ได้รอผู้เทส ห้ามบูต
- **ยืนยันสี่ข้อกับ `<SHA>` ที่จะบูตจริง (ต้องครบทั้งสี่):**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "skill-attr-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/skill_attr_hypothesis_attr_sweep.json && echo SCENARIO_PRESENT
git grep -n "COUNT1_KEY1" <SHA> -- src/pirateforce_foundation/ scenarios/
```
1. ไฟล์คำตัดสินมี `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ · 2. เจอ flag จริง (**ห้ามใช้ `--help` เป็นหลักฐาน**) · 3. เห็น `SCENARIO_PRESENT` · 4. เจอ label `COUNT1_KEY1` ในซอร์ส
- **อ่านค่า pin ต่อเฟรมจาก scenario ที่ merge แล้ว:** `scenarios/skill_attr_hypothesis_attr_sweep.json` -> `probe.per_step.<LABEL>.frame_sha256` / `frame_size` (พินซ้ำในโมดูลที่ `SKILL_ATTR_PROBE_FRAME_SHA256`) — **ค่า sha ตัวจริงอ่านจากไฟล์ตอน merge ห้ามฝังเลขในใบนี้**
- ไม่ครบสี่ข้อ + ยังไม่ได้ค่า pin = **ห้ามบูต** ใบนี้อยู่ PENDING ต่อ

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-059_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt059.sqlite3
```
- เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง** (canonical ไม่ถูกเปิดตลอดรอบ)
- เลนนี้ `database_write=none` · เกณฑ์ DB สำเนาใช้แบบที่ผู้เทส GT-058 เสนอและ chief เห็นด้วย: **row-diff ทุกตารางต่างได้เฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง** (ไม่ใช้ "byte-identical" ซึ่งขัดกับ session persist)
- ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกบูต (สำเนา DB ใหม่ทุกครั้ง)

### server args (เป๊ะ — opt-in เท่านั้น · `production_allowed=false`)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt059.sqlite3 --skill-attr-hypothesis-scenario scenarios\skill_attr_hypothesis_attr_sweep.json
```
- หัวหน้าต่าง console ของ server ต้องขึ้น mode `skill-attr-hypothesis` — ใช้เช็คว่าบูตถูกโหมด

### 🔴 ตัว trigger แชต — 12 ตัวอักษร printable ASCII เป๊ะ (บทเรียนที่เคยเสียเวลาโปรเจกต์)
- เลนนี้ trigger ด้วย **รูปร่าง** ไม่ใช่สตริงตายตัว: chat-input frame ที่ตัวข้อความเป็น **printable ASCII 12 ตัวพอดี** (classifier `classify_chat_input_attempt` -> `ascii12` — ท่าเดียวกับเลน learn-skill-result) · **สั้น/ยาวกว่านั้นถึงเซิร์ฟเวอร์แต่เงื่อนไขเงียบ ๆ ไม่ผ่าน ไม่มี error** — sweep ไม่ออกเฉย ๆ
- ใช้สตริงมาตรฐานของใบนี้เพื่อให้ log อ่านง่าย: `skillattr001` (นับ: s-k-i-l-l-a-t-t-r-0-0-1 = 12 ตัว)
- 🔴 **คลิกช่องแชตให้โฟกัสก่อนพิมพ์** (ตัวอักษรตอนไม่โฟกัส = hotkey) · พิมพ์ครบ 12 ตัวแล้ว Enter หนึ่งครั้ง · **ก่อนกด K ทุกครั้งต้องเอาโฟกัสออกจากช่องแชตก่อน** (คลิกพื้นว่าง) ไม่งั้น K กลายเป็นตัวอักษรในช่องแชต
- โหมดนี้**ไม่มี echo lane** — บรรทัดที่พิมพ์อาจไม่เด้งกลับในแชต **ไม่ใช่สัญญาณว่า trigger พัง** · ⚠️ **แก้ R152 (พิสูจน์จากซอร์ส):** event ทั้งฝั่งส่ง (`skill_attr_hypothesis_attr_sweep_sent`) และฝั่งปฏิเสธ (`..._wrong_length/_wrong_text/_wrong_envelope/_no_selected/_wrong_sequence/_identity_not_pinned_no_reply`) อยู่ใน `self.events` **ใน memory เท่านั้น — build ปัจจุบันไม่เขียนออกไฟล์/console เลย** (`runtime.py` append 179 จุด ไม่มีจุดอ่าน/พิมพ์ · ผู้บริโภคเดียวคือเทส) ⇒ **หลักฐานว่า trigger ผ่าน = `[G>]` action labels + raw SENT/frame hexdump ตรง pin** · ถ้า sweep ไม่ออก **ปัจจุบันวินิจฉัยเหตุปฏิเสธจาก log ไม่ได้** — จดข้อเท็จจริง (trigger ที่พิมพ์ · ความยาว · จังหวะ) แล้วส่งกลับให้ chief วินิจฉัยฝั่ง server · เลนโค้ด EVENT-EXPORT-001 (รอบถัดไป) จะพิมพ์**ทั้ง dispatch และ reject events** ออก console เพื่อปิดช่องนี้

### steps
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบตามบล็อก db
1. เปิด server ก่อน client เสมอ (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client) — console ขึ้น mode `skill-attr-hypothesis` (🔴 client ที่บูตโดยไม่มี server ตายเองใน ~3.5 นาที)
2. เปิด client → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร → **เลือกตัวละครช่องแรก** (identity guard ข้างบน) → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
3. เข้าแมพ เห็น HP/minimap/ชื่อแมพ → **เริ่มอัดวิดีโอ/continuous capture ตั้งแต่ตรงนี้ยาวจนจบ session** (หน้าต่าง 3 วิ ระหว่างเฟรมต้องพึ่งวิดีโอ)
4. **BASELINE (ต้องทำก่อนยิงเฟรมใด ๆ — replicate GT-058):** คลิกพื้นว่างให้แน่ใจว่าแชตไม่โฟกัส → กด **K** → คลิกปุ่มสกิลล่างซ้าย (`Bt_main_Skill` · tooltip `สกิล (K)`) → ถ่าย **S0** · คาดว่า**ไม่เปิด**ตาม GT-058 — ถ้า baseline เปิดได้เฉย ๆ ให้จดใหญ่ ๆ (เงื่อนไขใบเปลี่ยน) แล้วทำต่อ
5. คลิกช่องแชตให้โฟกัส → พิมพ์ `skillattr001` → Enter หนึ่งครั้ง → **คลิกพื้นว่างทันที** (ปลดโฟกัส)
6. **หน้าต่าง 3 วิ หลังเฟรม 1 (best-effort):** กด **K** หนึ่งครั้งให้เร็วที่สุดหลัง Enter+ปลดโฟกัส → ถ่าย **S1** · วิดีโอจะตัดสินทีหลังว่า K นี้ลงก่อนหรือหลังเฟรม COUNT1_KEY1 — ถ้าไม่ทัน จดว่าไม่ทัน
7. **หลัง sweep จบ (>5 วิ หลัง Enter):** กด **K** → ถ่าย **S2** · คลิก `Bt_main_Skill` → ถ่าย **S3** · จดผลเป็น tri-state: **เปิด+มีรายการ / เปิด+ว่าง / ไม่เปิด** (ถ้าเปิด: ถ่ายให้เห็นเนื้อในหน้าต่างชัด ๆ ว่ามีอะไร)
8. ยิง trigger ซ้ำอีกหนึ่งครั้ง (เลนไม่ one-shot) แล้วกด K อีกรอบ → ถ่าย **S4** — กันเคส "ต้องรับมากกว่าหนึ่ง sweep"
9. จับ NO-CRASH / CRASH: client ยังตอบสนอง (ขยับกล้อง `Q/E` ได้) = NO-CRASH · หลุด/ค้าง = CRASH + จดเฟรม (ชี้ version byte 0 ก่อน) *(🔴 **หมายเหตุ chief R163 — ไม่ใช่การแก้ขั้นตอน:** ใบนี้**ปิดไปแล้ว** ขั้นตอนข้างบนคือขั้นตอนที่รันจริงในรอบนั้น **จึงคงไว้ตามเดิมทั้งตัวอักษร** · ฉบับแรกของ R163 เขียนทับมัน ซึ่งผิดกติกา — `pf-adversary` จับได้ ถอนแล้ว · **ถ้ารอบนั้นใช้ `Q/E` จริง แปลว่ามี `TargetPosVital` ออกกลางรอบ ซึ่งเป็นข้อเท็จจริงที่กระทบการอ่านผล ห้ามลบร่องรอย** · สำหรับรอบ **ใหม่** ให้ใช้ **คลิกขวาค้างลากเมาส์** เช็ค NO-CRASH แทน — เหตุผลอยู่ในบล็อกกฎกล้องของ PLAYBOOK)*
10. **SESSION 2 — relog variant (ทดสอบ gate ตอน controller construction):** ออกจากเกมด้วย **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย → **ปิด server ด้วย** (🔴 server เก็บ session ค้าง — ถ้าไม่ restart server ก่อน client ตัวถัดไปจะค้าง "connecting" ตลอดกาล) → เก็บ raw GAME log/console ของ session 1 → copy DB สำเนาใหม่ (`run_gt059b.sqlite3`) → บูต server (args เดิม เปลี่ยน `--db`) → บูต client → เข้าเกมตัวละครช่องแรก → **ห้ามกด K ก่อน** → ยิง trigger (ข้อ 5) → รอ sweep จบ → ค่อยกด **K** ครั้งแรกของ session → ถ่าย **S5** + ปุ่ม → **S6** · จดว่าผลต่างจาก session 1 ไหม
11. ออกจากเกม + ปิด server → เก็บ raw GAME log + console out/err ทั้งสอง session → `PRAGMA integrity_check;` ทั้งสองสำเนา
12. **teardown เสมอ** แม้เลิกกลางคัน (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 — เพดานยกจาก 180 เมื่อ 2026-08-20 · `TEMPLATE_teardown_generic.ps1:135` · แท่นถูกทิ้งข้ามชั่วโมงใช้ `staged\TOOL_stop_stale_server.ps1`)
13. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม

### pass criteria — สองชั้น แยกกันเด็ดขาด
**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ · ทำ headless ได้)**
- raw GAME log ต่อ trigger หนึ่งครั้ง มี **2 เฟรม** เรียง `HYP_PF_035_SKILL_ATTR_COUNT0_EMPTY` (57 bytes) → `HYP_PF_035_SKILL_ATTR_COUNT1_KEY1` (68 bytes) ห่าง ~3.0 s · server events มี `skill_attr_hypothesis_attr_sweep_sent` ครั้งละหนึ่ง — ⚠️ **คำเคาะ chief R152 (จากช่องว่างที่รอบ unattended พบ): build ปัจจุบันไม่ serialize ชื่อ event นี้ออกไฟล์ console** ⇒ **ยอมรับ `[G>]` action labels + raw SENT/frame hexdump ที่ SHA ตรง pin เป็นหลักฐาน dispatch แทน literal event string ได้** (raw frame ตรง pin คือหลักฐานปฐมภูมิอยู่แล้ว — event string เป็นแค่ตัวยืนยันรอง) · งานให้ exporter พิมพ์ event ออก console **ทั้ง dispatch และ reject** = เลนโค้ด EVENT-EXPORT-001 รอบถัดไป (จดใน rounds/R152 + CHIEF_CONTINUATION)
- sha256 ของแต่ละเฟรมที่ dispatch **ตรง pin** `probe.per_step.<LABEL>.frame_sha256` ใน `scenarios/skill_attr_hypothesis_attr_sweep.json` ของ commit ที่บูต (พินเดียวกับ `SKILL_ATTR_PROBE_FRAME_SHA256` ในโมดูล) · เก็บ hexdump ทั้งไฟล์ **ห้ามลบ**
- โครงสาย (RE-061-proven) ที่ต้องเห็น: carrier `0x309A` · attr_count 1 · class id `0x1661` · body: `u8 0x0B mask=0x01` → `u64 0x32 identity` → `u16 0x12 count` → record 11 ไบต์ `(u16 0x12 key / u16 0x12 / u32 0x14)`
- DB สำเนาทั้งสองใบ: `PRAGMA integrity_check` = `ok` · **row-diff ทุกตารางต่างเฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง** · sha256 canonical ก่อน-หลังตรงกัน
- **ชั้นนี้ตอบไม่ได้:** หน้าต่างเปิดหรือไม่ (เฟรมออก ≠ client รับ/ใช้) ⇒ **ห้ามอ้างชั้นนี้แทนชั้น (2)**

**ชั้น (2) client-observable (ต้องมีคนหน้าจอ)**
- ภาพ **S0..S6** + วิดีโอต่อเนื่องทั้งสอง session · sha256 ทุกไฟล์
- ตอบ **tri-state ต่อจุดวัด** (S0 baseline · S1 ระหว่างเฟรม-ถ้าทัน · S2/S3 หลัง sweep · S4 หลัง sweep ที่สอง · S5/S6 session 2): **เปิด+มีรายการ / เปิด+ว่าง / ไม่เปิด** — ทั้งทาง K และทางปุ่ม `Bt_main_Skill` แยกกัน
- ถ้าเปิดได้: บรรยายเนื้อในเป็นภาษาคน (มีกี่แถว/ช่อง · ว่างไหม) — **ห้ามตีความว่าค่าที่เห็นหมายถึงอะไร**
- NO-CRASH / CRASH verdict ชัดเจน + คำตอบ "relog เปลี่ยนผลไหม" (session 1 vs session 2)
- **ชั้นนี้ตอบไม่ได้:** เฟรมออกจากเซิร์ฟเวอร์จริงไหม **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

### 🔴 ผลลบมีค่าเท่าผลบวก
- **wire ครบแต่ K ยังไม่เปิดทุกจุดวัดรวมทั้ง session 2** = ผลลบที่สมบูรณ์ **ไม่ใช่ FAIL** ⇒ **falsify "รับ `CSkillAttr` หนึ่งครั้งแล้วพอ"** (ยืนยัน NONCLAIM ของ RE-061 ด้วยหลักฐาน runtime) · redirect (อัปเดต R152 หลัง RE-062 DONE): **RE-062 ตอบแล้ว — inbound เขียน `[actor+0x3E8]` ไม่ได้เลย (no-slot-write · เคส (ค))** ⇒ ผลลบไม่ต้องเปิดใบ static ซ้ำ · งานถัดไปคือแยกด้วย runtime ว่า `slot null (เลนส่งช่วยไม่ได้ — ต้องหาทางอื่นที่ทำให้ client สร้าง slot เอง)` หรือ `slot non-null + check อื่นใน 0x761ED0 ขวาง` — สองเคสนี้ static แยกให้ไม่ได้แล้ว (จดหมาย 1701 §ผลต่อ GT-059) · ⚠️ **ตัววัด runtime ของ slot นี้ยังไม่ถูกนิยาม** (บูต attended ไม่มี debugger) — ถ้าผลลบเกิดจริง ให้จดผลลบตามชั้นที่วัดได้แล้วเปิดงานออกแบบตัววัดเป็นใบใหม่ **ห้ามเดาเคสเอง** (คำถามค้างข้อ ③ จดหมาย R152)
- **เปิดได้เฉพาะ session 2 (trigger ก่อน K แรก)** = ผลบวกแบบมีเงื่อนไขจังหวะ — จุดอ่านคือ controller construction · redirect: เลน server ควรส่ง `CSkillAttr` ตอน entry flow ไม่ใช่รอ trigger
- **เปิดได้แต่ว่างที่ COUNT0/มีของที่ COUNT1 แยกไม่ได้** (กด K ไม่ทันหน้าต่าง 3 วิ) = จดว่า A/B UNRESOLVED — ยัง PASS ชั้น observable ได้ในคำถามหลัก (gate เปิด/ไม่เปิด)
- **CRASH ที่เฟรมแรก** = ชี้ version byte 0 (ดีไซน์เรา ยัง unpinned) ก่อน record semantics

### nonclaims (ติดไปกับผลทุกกรณี)
- **ไม่ตีความความหมายของ `opaque_u16`/`opaque_u32`/ค่า `key`** — key=1 เป็นค่า probe ตามใจเรา ไม่ claim ว่าเป็นสกิลจริงตัวใด
- **ไม่ claim ว่าเซิร์ฟเวอร์ต้นฉบับ (ปิดแล้ว กู้ไม่ได้ตลอดกาล) เคยส่ง `CSkillAttr` แบบนี้/จังหวะนี้** — step plan, ค่า record, db_mask policy, spacing, trigger policy เป็นดีไซน์ของเราทั้งหมด (ไม่มี capture ของ block นี้ทิศทางใดเลย)
- **ไม่พิสูจน์ว่าสกิล "ใช้งานได้"** — ใบนี้วัดแค่ window gate เปิด/ไม่เปิด ไม่แตะการกดใช้สกิล
- **ผลบวกไม่พิสูจน์ว่า `CSkillAttr` เป็นเงื่อนไข "เดียว"** — พิสูจน์แค่ว่าในสภาพแวดล้อมนี้การรับมัน (ร่วมกับสภาพ baseline เดิม) เพียงพอ
- **result:** (ผู้เทสกรอก: ภาพ S0..S6 + วิดีโอ พร้อม sha256 · tri-state ต่อจุดวัด ทาง K และทางปุ่มแยกกัน · K ระหว่างเฟรมทัน/ไม่ทัน · session 1 vs 2 ต่างไหม · NO-CRASH/CRASH · path raw GAME log + label/sha 2 เฟรมต่อ trigger + `[G>]` labels/hexdump ตรง pin (แทน event string — ดู ⚠️ R152 ข้างบน) · เวลา · sha canonical ก่อน-หลัง · row-diff ของ `run_gt059*.sqlite3`)
  - 🟡 **บันทึกรอบ UNATTENDED (R152):** จดหมาย `notes_to_chief\20260824_1757_GT059-NO-RESULT-unattended-no-skill-window-wire-exact.md` — wire byte-exact PASS ×3 triggers · client provisional "ไม่พบ window ในรอบนี้" ทุกจุดวัด (S1 ไม่มีไฟล์ — เก็บไม่ทัน) · **ใบยังไม่ปิด**


---
## ⭐ GT-060 PICKUP-CLICK-CAPTURE-001 [attended, in-game]: คลิกซ้ายบน drop-object ที่วาดจริงบนจอ แล้วจับเฟรม `PickupTerrainThing` **ตัวจริงตัวแรก** บน wire — id `0x4543` ที่ derive ไว้ ถูกหรือผิด  [🔴 **BLOCKED-CONDITIONAL — ห้ามบูตจนกว่าเงื่อนไข (ก)(ข)(ค) ข้างล่างครบทั้งสามข้อ** · เลน server = HYP-PF-036 (R151 · ✅ (ก) ปิดแล้ว R152: PR #22 merge เข้า `main` `2c0e3ba`) · เงื่อนไข (ข) เหลือแค่ผลตา GT-045 (นัด 2026-08-26) — คำเคาะ composition มาแล้ว (จดหมาย 1831 §①) และโค้ด composed-boot merge เข้า `main` แล้ว (R154: PR #23 → `cad3e28` เขียว Actions run 32726495224) · ✅ **(ค) ปลดแล้ว — Panya ปลดพักเลน attended ทั้งเลน (2026-08-24 ~21:1x +07:00 · จดหมาย 2120 §① · บันทึกโดย R155)** — คำสั่งพัก 16:56 ของ 23 ส.ค. สิ้นสุด · กฎรอบ unattended ยังเหมือนเดิมทุกตัวอักษร · 🆕 R155: คำเคาะ 2120 §② ขยาย allow-list เป็น**สามตัว** `ground-loot + pickup-listener + item-operate-res` — ใบนี้ได้ประโยชน์ถ้ารวมบูตกับ GT-063 (โค้ดสามตัว = PR #25 รอ gate — ดูหัวใบ GT-063)]

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
## GT-063 ITEMOPERATE-RES-GREENLINE-SHAPE-001 [attended, in-game]: ยิง `ItemOperateVitalRes` (`0x4C13`) สามทรงจากเซิร์ฟเวอร์เรา แล้วตัดสินด้วยตาคนว่า **ทรงไหนทำให้บรรทัดเขียว `ได้รับ [<ชื่อ>] * <จำนวน>` ขึ้นบนแชตจริง**  [✅ **PASS — จ็อบ 1115 · 2026-08-25 01:12-02:09 (+07:00) · attended (Panya ขับ UI เอง) · `BOOT_COMMIT 6d5eb7b3` (resolver exit 0 · `FILES_CHANGED_vs_main = 0`) · จดหมาย `20260825_0230` · บันทึกโดย chief R158** — **wire:** ยิงครบ 3 เฟรม เฟรมละ 82 ไบต์ (`CTRL_CAPTURE_REPLAY` → เงียบ · `BAGUPD_ID2400901_QTY1` → เงียบ · `BAGUPD_ID2400901_QTY5` → 🟢 ขึ้น) · trigger แชต `greenline001` เวลา Enter จาก `--export-events` (`0xAC52`) `01:18:37.855` · **client-observable:** 🟢 **`ได้รับ [ Camouflage Item-Cask ] * 4` ขึ้นจริง + ของเข้ากระเป๋าจริง (ถังไม้ 5 ชิ้น จากเดิม 1)** · ชื่อตรวจข้ามชั้นผ่าน: `2400901` → code 24 `ITEM_CONSUMABLES` n_ID 901 = `Camouflage Item-Cask` · 🔴 **คำทำนายในใบผิดแบบที่บอกความจริง:** ใบเขียนว่า `* 5` แต่ได้ `* 4` ⇒ **ฟิลด์นั้นไม่ใช่ "จำนวนที่เพิ่ม" แต่คือ "ยอดรวมที่ควรมีหลังจบ"** — client โชว์ `ที่ส่งมา − ที่มีอยู่` · กฎเดียวอธิบายทั้งเสียงเงียบของเฟรม 2 (1−1=0) และเลข 4 ของเฟรม 3 (5−1=4) · โมเดลนี้ผ่านเทสหักล้างที่ Panya รันเองต่อทันที · 🔴 **nonclaims:** ① **ไม่ได้พิสูจน์ว่าของลง DB จริง** (`database_write=none`) และ **Panya กดออกไปหน้าเลือกตัวละครไม่ได้ (เมนูในเกมใช้ไม่ได้) ต้องปิดด้วย X ⇒ ยังไม่ได้เทสว่าของอยู่รอดข้าม session — เปิดเป็นคำถามค้าง** ② โมเดล "ยอดรวมปลายทาง" ยืนยันจาก 4 จุดข้อมูล แต่ยังไม่เคยลองค่าอื่นนอกจาก 1 กับ 5 ③ เฟรม 1 เงียบตามคาด ไม่ถูกปฏิเสธ ไม่มี ErrorData ⇒ **envelope ที่ v141 สร้างถูกไคลเอนต์รับ** (สอดคล้อง rider 15/15 ของ RE-064)] *(สถานะเดิมก่อนปิด:* [🟡 **READY-CONDITIONAL (อัปเดต R155)** · ใบเปิดตามคำอนุมัติ Panya 2026-08-24 ~18:3x +07:00 §② (จดหมาย `notes_to_chief\20260824_1831_PANYA-RULINGS-combine-scenarios-and-open-GT-063.md`) · (ก) ✅ **ปิดแล้ว (R155): PR #24 merge เข้า `main` แล้ว** — merge commit `960716c` · head `1435064f` เขียว(Actions run 32733905271 · subset · อ่านทาง ci-status · sha ในไฟล์ตรง) · tree ของ head = tree ของ merge commit (diff ว่าง) · (ข) ✅ **ปลดแล้ว — Panya ปลดพักเลน attended (จดหมาย 2120 §① · 2026-08-24 ~21:1x +07:00)** · (ค) ✅ **คำเคาะรวมบูตมาแล้ว: Panya อนุมัติ allow-list สามตัว `ground-loot + pickup-listener + item-operate-res` ร่วมบูตเดียวกัน (จดหมาย 2120 §② "รวม 3 scenario มาเลย")** — ✅ **โค้ดสามตัวเข้า `main` แล้ว (ปิดโดย R156): PR #25 merge** — merge commit `3f87fc3` · head `fc4010e` เขียว(Actions run 32743688024 · subset · อ่านทาง ci-status · sha ในไฟล์ตรง) ⇒ **บูตรวมสามเลนได้แล้ว** (BOOT_COMMIT ต้องเป็น `main` ที่มี `3f87fc3` — เช็คด้วย `git grep -n "COMPOSABLE_SCENARIO_LANE_SETS" <SHA> -- src/pirateforce_foundation/runtime.py` ต้องเจอ set สามตัว) · วินัย attribution สามเลนบังคับเต็ม: ทุกข้อสังเกตต้องระบุเลนผู้ก่อ แยกไม่ออก = NO-RESULT (จดหมาย 2120 §②)]

**ที่มา (สามใบที่ปิดแล้ว 2026-08-24 — อ่านก่อนบูต):**
- **GT-049** (PASS/DONE · ผลหน้าสะพาน 2026-08-24 09:23 +07:00 · บันทึก R144): ข้อความ id 131 (template `ได้รับ [ $V1 ] * $V2`) ยิงจาก **inbound** `ItemOperateVitalRes` handler `0x005EF5E0` -> chat emitter `0x005CC309` ⇒ **เซิร์ฟเวอร์เป็นผู้ตัดสินว่าเก็บสำเร็จ** ไม่ใช่ไคลเอนต์ — บรรทัดเขียวขึ้นได้ก็ต่อเมื่อฝั่งเราส่งเฟรมนี้เอง
- **RE-059** (DONE · 2026-08-24 14:13 +07:00): ถอดเฟรม capture จริงครบ 5/5 — ทั้งห้าเป็น `version 2` · `R4=0` · `bag_present_flag=1` · `ItemBagAttr` ยาว 43/52/69/69/43 ไบต์ · 🔴 **`affected_identity_count = 0` ทุกเฟรม** ⇒ เราไม่มี capture ของทรงที่ `count>0` เลยสักเฟรม
- **RE-060** (DONE · 2026-08-24 14:22 +07:00): pin รหัสตารางไอเทม `22=EQUIPMENT_BASE` · `24=ITEM_CONSUMABLES` · `25=ITEM_QUEST` · `26=ITEM_MISC` · `35=ITEM_ITEMMALL` · สคีม `full_id / 100000 -> table` · `full_id % 100000 -> n_ID` · 🔴 หลักฐานชนิด **ค (candidate 100%-hit) — ไม่ใช่การยืนยันบนสาย**

🔴 **ช่องว่างที่ใบนี้ปิด:** เรามีไบต์ของ 5 เฟรมจริงครบ **แต่ไม่มีใครบันทึกว่าตอนนั้นบนจอขึ้นอะไร** — มีซองจดหมาย ไม่รู้ว่าฉบับไหนทำให้เกิดอะไร · เลน static หมดทางแล้ว (GT-049/RE-059/RE-060 ปิดครบ) ⇒ ต้องยิงจริงแล้วดูจอ

**หมวด:** attended, in-game — ต้องมีคนหน้าจอ · จับ `LOCK_GAME` ตามปกติ

### เงื่อนไขปลดบล็อก — ✅ **(ก)(ข) ปิดครบโดย R155 ⇒ บูตเดี่ยวได้แล้ว** · (ค) รวมสามเลนรอ merge
- **(ก) ✅ ปิดแล้ว (R155 · 2026-08-24 ~21:5x +07:00):** PR **#24** (`HYP-PF-037 ITEMOP-RES-GREENLINE-001`) **merge เข้า `main` แล้ว** — merge commit `960716c` · head `1435064f` เขียว(Actions run 32733905271 · subset · อ่านทาง ci-status · `"sha"` ในไฟล์ตรงชื่อไฟล์ · conclusion `success`) · tree ของ head = tree ของ merge commit (diff ว่าง) · ของจริงที่ต้องใช้ตอนบูต: flag `--item-operate-res-hypothesis-scenario` · ไฟล์ `scenarios/item_operate_res_greenline_sweep.json` · trigger แชต = ข้อความ **12 ตัวอักษร printable ASCII เป๊ะ** (ตัวไหนก็ได้ — ตกลงใช้ `greenline001` เพื่อให้จดหมายผลอ่านตรงกัน · 🔴 ระวังในบูตรวม: แชต 12 ตัวอักษรใด ๆ ก็ยิง sweep ได้ — อย่าพิมพ์แชต 12 ตัวโดยไม่ตั้งใจ) · identity guard ตัวละครช่องแรก · label สามตัวตามบล็อก sweep ข้างล่าง · pin `message/pc/frame_sha256 + size` ต่อ label อ่านจากไฟล์ scenario ใน commit ที่บูต
- **(ข)** ✅ **ปิดแล้ว (R155):** Panya ปลดพักเลน attended แล้ว (2026-08-24 ~21:1x +07:00 · จดหมาย 2120 §① — คำสั่งพัก 16:56 สิ้นสุด · จดหมาย 1831 §④ ถูก supersede ในข้อนี้)
- **(ค) รวมบูตกับ GT-060 — คำเคาะมาแล้ว แต่รอโค้ด:** Panya อนุมัติ**สามเลน** `ground-loot + pickup-listener + item-operate-res` ร่วมบูตเดียวกันแล้ว (จดหมาย 2120 §② "รวม 3 scenario มาเลย" — supersede เงื่อนไข "ต้องขอทีละคู่" ของ 1831 §① เฉพาะสามตัวนี้) · 🔴 **แต่โค้ดบน `main` ณ จุดเคาะยังอนุญาตแค่คู่ `ground-loot + pickup-listener`** ⇒ chief แก้ allow-list เป็น exact-set สามตัว (sub-pair ไม่เปิด — fail-closed) ใน **PR โค้ด #25 (รอบ R155 · commit `fc4010e`)** — ✅ **merge เข้า `main` แล้ว (ปิดโดย R156): merge commit `3f87fc3` · head `fc4010e` เขียว(Actions run 32743688024 · subset · ทาง ci-status)** ⇒ **บูตรวมสามเลนได้เมื่อ BOOT_COMMIT มี `3f87fc3` จริง** (เช็คด้วย resolver + `git grep -n "COMPOSABLE_SCENARIO_LANE_SETS" <SHA> -- src/pirateforce_foundation/runtime.py` ต้องเจอ) · ระหว่างนี้: บูตเดี่ยว หรือคู่เดิม ได้ตามปกติ · flow ถ้ารวม: คลิกเก็บของ (GT-060) -> ดูเฟรมขาออก -> เลนใบนี้ส่ง `0x4C13` -> ดูบรรทัดเขียว (GT-063) · 🔴 **วินัย attribution (บังคับถ้ารวม — สามเลนยิ่งเข้ม):** ทุกข้อสังเกตในจดหมายผลต้องระบุว่า **เลนไหนเป็นผู้ทำให้เกิด** — แยกไม่ออก ⇒ ข้อสังเกตนั้นเป็น `NO-RESULT` ห้ามนับให้เลนใด · ถ้าไม่รวม ใบนี้บูตเดี่ยวได้ตามปกติ (sweep ยิงด้วย chat trigger ไม่ต้องมีของบนพื้น)

### objective (claim เดียว)
**ทรงไหนของ `ItemOperateVitalRes` (`0x4C13`) ที่ทำให้บรรทัดเขียว `ได้รับ [<ชื่อ>] * <จำนวน>` (ข้อความ id 131) ขึ้นบนแชตของไคลเอนต์จริง**
(ใบนี้วัด "ทรงไหนทำให้ข้อความขึ้น" เท่านั้น — ไม่ตีความความหมายของฟิลด์ใด ๆ)

### sweep 3 เฟรมต่อหนึ่ง trigger (spacing 3.0 s ตาม convention เลน sweep อื่น · ยิงซ้ำได้ ไม่ one-shot · 🔴 ต้องอัดวิดีโอต่อเนื่อง) — ✅ **ชื่อ label เป็นชื่อจริงจากเลนโค้ดแล้ว (chief R154 · PR #24)**
```
1. ITEMOP_RES_CTRL_CAPTURE_REPLAY       (ตัวควบคุม: replay byte-exact เฟรม capture RE-059 #1
                                         ที่ชั้น message (54 ไบต์ · ItemBagAttr 43 ไบต์) —
                                         version 2, R4=0, bag_present_flag=1,
                                         affected_identity_count=0 · dual-derived: hex ที่ commit
                                         == output ของ codec golden `make_item_move_delta_response`
                                         ไบต์ต่อไบต์ พิสูจน์ R154)
2. ITEMOP_RES_BAGUPD_ID2400901_QTY1     (ทรง bag-update ที่พิสูจน์แล้วทรงเดียวกัน · item id จริง
                                         จาก RE-060: 2400901 -> table 24 = ITEM_CONSUMABLES,
                                         n_ID 901 — item เดียวกับ golden backpack (identity 2,
                                         slot 1) · quantity=1 — ทรงที่คาดว่าทำให้บรรทัดเขียวขึ้น)
3. ITEMOP_RES_BAGUPD_ID2400901_QTY5     (เหมือน #2 แต่ quantity=5 — ทดสอบช่อง "* <จำนวน>"
                                         ของ template id 131)
```
- เหตุผลเฟรม 1: ถ้าทรงที่มีอยู่จริงในสาย (ทรง capture เป๊ะ) ไม่ทำให้เกิดอะไรบนจอ = **ผลที่มีค่า** ไม่ใช่เฟรมทิ้ง
- 🔴 **คำเคาะดีไซน์ chief R154 — ทำไมไม่มีเฟรม `affected_identity_count=1` ตามร่างเดิม:** โครง element
  ตอน count>0 เป็นแค่ static candidate (`0x32` u64 + `0x08` u8) และ **R13 (`0x005ED2F0`) ยังไม่รู้ว่าอยู่ใน
  loop per-element หรือเป็น trailer** — ไม่มี capture ตัวอย่างเลย (5/5 เฟรม count=0) ⇒ ประกอบ = เดาไบต์
  ขัด fail-closed (เฟรมอาจสั้น/ยาวผิดทรง ⇒ ปนเปื้อน P4 ทั้ง sweep) · มิติ count>0 เข้าคิว **RE-064**
  (`CLIENT_RE_QUEUE.md`) — ปิดใบนั้นแล้วค่อยเปิด sweep variant count>0 เป็นรอบใหม่ (เวอร์ชันใหม่ของ
  HYP-PF-037 ตาม stop_rule) · ทั้งสามเฟรมของใบนี้จึง count=0 ทั้งหมด — แยกกันด้วยเนื้อใน ItemBagAttr
- 🔴 **version byte = 2 ตาม capture (RE-059) — เลนโค้ดพินแล้ว** · ถ้า client reject/หลุดตั้งแต่เฟรมแรก
  จุดต้องสงสัยอันดับหนึ่งคือโครงซอง/prefix ไม่ใช่ semantics (บทเรียน GT-058/059) · 🔴 หมายเหตุ attribution:
  replay เป๊ะเฉพาะชั้น message — prefix ซอง 15 ไบต์ของ capture ยังไม่เคยถูกเทียบกับของ v141
  (rider ในใบ RE-064) ⇒ ErrorData ที่เฟรม 1 ยังชี้ prefix หรือ session context ไม่ได้จนกว่า rider จะปิด
- ✅ ข้อกำหนดดีไซน์เลน (ตามที่ merge จริง): identity guard ตัวละครช่องแรก (smoke `0x10010001/0`) ·
  `production_allowed=false` · `database_write=none` (dispatch path ไม่เขียน — ตัวบูตยัง migrate/expire
  sessions บน `--db` สำเนาตามปกติทุกเลน) · pin ต่อ label ครบสามชั้น (message/pc/frame · sha256+size)
  ในไฟล์ scenario

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว · ท่องก่อนบูต)
- **P1:** บรรทัดเขียวขึ้นที่เฟรม 2 หรือ 3 ⇒ **ปิดใบได้** — แนบว่าเฟรมไหน + ข้อความที่อ่านได้ทั้งบรรทัด (ชื่อไอเทม + จำนวน เป๊ะ) · ถ้าเฟรม 3 แสดง `* 5` = ช่อง `$V2` ผูกกับ quantity ที่เราส่งจริง
- **P2:** ไม่ขึ้นเลยทั้งสามเฟรม ⇒ **`NO-RESULT` ตามกติกา Panya 2026-08-24 — 🔴 ห้ามเขียนคำว่า "ไม่มี" หรือ "ไม่เกิด"** · อ่านว่า "ทรงที่ลองยังไม่พอ" · ใบไม่ปิด — redirect: ออกแบบทรงชุดถัดไป (เช่น bag delta จริงใน ItemBagAttr) เป็น sweep รอบใหม่
- **P3:** ขึ้น**ข้อความอื่น**แทน (ถุงเต็ม / ของคนอื่น / นอกระยะ — โค้ด `0xFD`/`0xFE`/`0xFC` ที่ GT-046 ถอดไว้ผูก `TEXTDATA_TH__MESSAGE.tsv`) ⇒ **ผลที่มีค่ามาก** — จดข้อความเป๊ะ + เฟรมไหนทำให้ขึ้น · ชี้ว่า handler อ่านฟิลด์ status ที่เรายังไม่ได้ตีความ
- **P4:** client reject/หลุด ⇒ ชี้ **version byte / โครงซองก่อน semantics** (บทเรียน GT-058/059) — จดว่าหลุดที่เฟรมไหน

### 🔴 ก่อนบูต — resolve commit เขียว (ท่าเดียวกับ GT-058/059/060 · รันเครื่องมือ ไม่ใช่ก๊อป SHA · ทำได้ต่อเมื่อ (ก) ปิดแล้ว)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` · **exit 3** = ใบนี้รอ gate ไม่ได้รอผู้เทส ห้ามบูต
- **ยืนยันสี่ข้อกับ `<SHA>` ที่จะบูตจริง (✅ ชื่อ flag/scenario/label ข้างล่างเป็นชื่อจริงจาก PR #24 แล้ว):**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "item-operate-res-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/item_operate_res_greenline_sweep.json && echo SCENARIO_PRESENT
git grep -n "ITEMOP_RES_BAGUPD_ID2400901_QTY1" <SHA> -- src/pirateforce_foundation/ scenarios/
```
1. ไฟล์คำตัดสินมี `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ · 2. เจอ flag จริง (**ห้ามใช้ `--help` เป็นหลักฐาน**) · 3. เห็น `SCENARIO_PRESENT` · 4. เจอ label ในซอร์ส
- **ยืนยันเพิ่มว่า `--export-events` มีจริงใน `<SHA>`** (แลนด์ใน PR R153): `git grep -n "export-events" <SHA> -- src/pirateforce_foundation/app.py` — ถ้าไม่เจอ ให้จดไว้ว่า evidence ฝั่ง event จะอ่านจาก console ไม่ได้ (ตกกลับไปท่า `[G>]` labels + hexdump แบบ GT-059)
- **อ่านค่า pin ต่อเฟรมจากไฟล์ scenario ที่ merge แล้ว** (`frame_sha256`/`frame_size` ต่อ label) — **ค่า sha ตัวจริงอ่านจากไฟล์ตอน merge ห้ามฝังเลขในใบนี้**
- ไม่ครบ = **ห้ามบูต** ใบอยู่ BLOCKED ต่อ

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-063_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt063.sqlite3
```
- เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง** (canonical ไม่ถูกเปิดตลอดรอบ)
- เกณฑ์สำเนาแบบ GT-059/060: **row-diff ทุกตารางต่างได้เฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง** (ไม่ใช้ byte-identical ซึ่งขัดกับ session persist) · จด `max(lease_generation)` ก่อน-หลัง
- ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกบูต (สำเนา DB ใหม่ทุกครั้ง)

### server args (เป๊ะ — opt-in เท่านั้น · `production_allowed=false` · ✅ ชื่อ flag/scenario เป็นชื่อจริงจาก PR #24 แล้ว — บูตได้เมื่อ (ก) ปิดเท่านั้น)
**บูตเดี่ยว (default):**
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt063.sqlite3 --item-operate-res-hypothesis-scenario scenarios\item_operate_res_greenline_sweep.json --export-events
```
**บูตรวมกับ GT-060 (เฉพาะเมื่อ (ค) ผ่านครบ: PR R153 merge แล้ว + Panya อนุมัติ composition ที่รวมเลนใบนี้เพิ่มจากคู่ allow-list):**
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt063.sqlite3 --ground-loot-hypothesis-scenario scenarios\<ตามใบ GT-045> --pickup-listener-hypothesis-scenario scenarios\pickup_listener_hypothesis_decode_probe.json --item-operate-res-hypothesis-scenario scenarios\item_operate_res_greenline_sweep.json --export-events
```
- 🆕 **`--export-events` (แลนด์ใน PR R153 — เลนโค้ด EVENT-EXPORT-001):** สั่งให้ server พิมพ์บรรทัด `PF-EVENT` ออก console **ทั้ง dispatch และ reject** — ใช้เป็นหลักฐานชั้น wire ว่า sweep ออกจริง/ถูกปฏิเสธเพราะอะไร (ปิดช่องที่รอบ unattended ของ GT-059 เจอ: build เก่าเก็บ event ใน memory เท่านั้น) · ถ้า flag ยังไม่อยู่ใน BOOT_COMMIT ให้ตัดออกจากคำสั่งแล้วจดว่า evidence ฝั่ง event ใช้ไม่ได้รอบนี้
- หัวหน้าต่าง console ต้องขึ้น mode ของเลนนี้ — ใช้เช็คว่าบูตถูกโหมด

### 🔴 ตัว trigger แชต — 12 ตัวอักษร printable ASCII เป๊ะ (บทเรียนที่เคยเสียเวลาโปรเจกต์)
- ใช้สตริงมาตรฐานของใบนี้: `greenline001` (นับ: g-r-e-e-n-l-i-n-e-0-0-1 = 12 ตัวพอดี) — **สั้น/ยาวกว่านั้นถึงเซิร์ฟเวอร์แต่เงื่อนไขเงียบ ๆ ไม่ผ่าน ไม่มี error** sweep ไม่ออกเฉย ๆ
- 🔴 **คลิกช่องแชตให้โฟกัสก่อนพิมพ์** (ตัวอักษรตอนไม่โฟกัส = hotkey) · พิมพ์ครบ 12 ตัวแล้ว Enter หนึ่งครั้ง · หลัง Enter **คลิกพื้นว่างปลดโฟกัสทันที**
- บรรทัดที่พิมพ์อาจไม่เด้งกลับในแชต (ไม่มี echo lane) — **ไม่ใช่สัญญาณว่า trigger พัง** · ตัวยืนยัน = บรรทัด `PF-EVENT` dispatch/reject บน console (`--export-events`) + raw SENT/hexdump ตรง pin

### steps
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบตามบล็อก db
1. เปิด server ก่อน client เสมอ (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client) — console ขึ้น mode ของเลนนี้ (🔴 client ที่บูตโดยไม่มี server ตายเองใน ~3.5 นาที)
2. เปิด client → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร → **เลือกตัวละครช่องแรก** (identity guard) → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
3. เข้าแมพ เห็น HP/minimap/ชื่อแมพ → **เริ่มอัดวิดีโอต่อเนื่องตั้งแต่ตรงนี้ยาวจนจบ session** ลง `evidence_video\` (spacing 3.0 s ต่อเฟรม — ตาคนถ่ายภาพนิ่งไม่ทันต่อเฟรม **วิดีโอคือกรรมการว่าบรรทัดไหนขึ้นหลังเฟรมไหน**)
4. ถ่าย **S0** = พื้นที่แชต baseline ก่อนยิงอะไร (เห็นบรรทัดล่าสุดในแชตชัด)
5. คลิกช่องแชตให้โฟกัส → พิมพ์ `greenline001` → Enter หนึ่งครั้ง → **คลิกพื้นว่างทันที** (ปลดโฟกัส) → **จ้องพื้นที่แชตนิ่ง ๆ ตลอด ~10 วิของ sweep** ห้ามพิมพ์/กดปุ่มใด (ตัวอักษรตอนไม่โฟกัส = hotkey)
6. หลัง sweep จบ (>10 วิหลัง Enter): ถ่าย **S1** = พื้นที่แชตเต็ม ๆ อ่านออกทุกบรรทัดที่เพิ่มมา (บรรทัดเขียวค้างใน chat log — ภาพนี้คือหลักฐานปิดใบ ส่วน "ขึ้นหลังเฟรมไหน" ให้วิดีโอตัดสิน)
7. ยิง trigger ซ้ำอีกหนึ่งครั้ง (เลนไม่ one-shot) → จ้องแชต → ถ่าย **S2** — กันเคสข้อความขึ้นเฉพาะครั้งแรก/สะสม
8. จับ NO-CRASH / CRASH: client ยังตอบสนอง (ขยับกล้อง `Q/E` ได้) = NO-CRASH · หลุด/ค้าง = CRASH + จดว่าหลังเฟรมไหน (ชี้ version byte ก่อน — P4) *(🔴 **หมายเหตุ chief R163 — ไม่ใช่การแก้ขั้นตอน:** ใบนี้**ปิดไปแล้ว** ขั้นตอนข้างบนคือขั้นตอนที่รันจริงในรอบนั้น **จึงคงไว้ตามเดิมทั้งตัวอักษร** · ฉบับแรกของ R163 เขียนทับมัน ซึ่งผิดกติกา — `pf-adversary` จับได้ ถอนแล้ว · **ถ้ารอบนั้นใช้ `Q/E` จริง แปลว่ามี `TargetPosVital` ออกกลางรอบ ซึ่งเป็นข้อเท็จจริงที่กระทบการอ่านผล ห้ามลบร่องรอย** · สำหรับรอบ **ใหม่** ให้ใช้ **คลิกขวาค้างลากเมาส์** เช็ค NO-CRASH แทน — เหตุผลอยู่ในบล็อกกฎกล้องของ PLAYBOOK)*
9. **ถ้าเป็นบูตรวมกับ GT-060:** ทำ steps ของ GT-060 ก่อน (spawn → คลิกเก็บ) แล้วค่อยยิง trigger ของใบนี้ · 🔴 จดต่อทุกข้อสังเกตว่า **มาจากเลนไหน** (เช่น บรรทัดเขียวหลังคลิกแต่ก่อน trigger = ต้องอธิบายได้ว่าเลนไหนส่ง `0x4C13` ตอนนั้น — ถ้าแยกไม่ออก ข้อสังเกตนั้นเป็น NO-RESULT ตามวินัย §①)
10. ออกจากเกมด้วย **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย → **ปิด server ด้วย** (🔴 server เก็บ session ค้าง — client ตัวถัดไปจะค้าง "connecting" ตลอดกาลถ้าไม่ restart server ก่อน)
11. เก็บ raw GAME log ทั้งไฟล์ + console out/err (รวมบรรทัด `PF-EVENT` ทั้งหมด) → `PRAGMA integrity_check;` บนสำเนา
12. **teardown เสมอ** แม้เลิกกลางคัน (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 — เพดานยกจาก 180 เมื่อ 2026-08-20 · `TEMPLATE_teardown_generic.ps1:135` · แท่นถูกทิ้งข้ามชั่วโมงใช้ `staged\TOOL_stop_stale_server.ps1`)
13. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม

### pass criteria — สองชั้น แยกกันเด็ดขาด
**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ · ทำ headless ได้)**
- raw GAME log ต่อ trigger หนึ่งครั้ง มี **3 เฟรม** เรียงตาม label (CTRL_CAPTURE_REPLAY → BAGUPD_QTY1 → BAGUPD_QTY5 · เต็ม: `HYP_PF_037_ITEMOP_RES_*`) ห่าง ~3.0 s · sha256 ของแต่ละเฟรมที่ dispatch **ตรง pin** `frame_sha256` ในไฟล์ scenario ของ commit ที่บูต · เก็บ hexdump ทั้งไฟล์ **ห้ามลบ** · นับจำนวนเฟรมที่ออกจริงให้ตรงจำนวน trigger x 3
- console มีบรรทัด `PF-EVENT` dispatch หนึ่งบรรทัดต่อเฟรม (จาก `--export-events`) · ถ้า trigger ไม่ออก: บรรทัด `PF-EVENT` reject ต้องบอกเหตุ — เก็บมาทั้งบรรทัด (เป็นผลเหมือนกัน) · ถ้า build ที่บูตไม่มี flag นี้ ให้ยึด raw SENT/hexdump ตรง pin เป็นหลักฐานปฐมภูมิแทน (ท่า GT-059 R152)
- DB สำเนา: `PRAGMA integrity_check` = `ok` · row-diff ทุกตารางต่างเฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง · จด `max(lease_generation)` ก่อน-หลัง · sha256 canonical ก่อน-หลังตรงกัน
- **ชั้นนี้ตอบไม่ได้:** บรรทัดเขียวขึ้นบนจอหรือไม่ (เฟรมออก != client รับ/แสดง) ⇒ **ห้ามอ้างชั้นนี้แทนชั้น (2) — ห้ามปิดใบด้วยชั้นนี้**
**ชั้น (2) client-observable (ต้องมีคนหน้าจอ — ตัวปิดใบอยู่ชั้นนี้ชั้นเดียว)**
- 🔴 **ปิดใบได้เฉพาะกรณีเห็นข้อความบนจอและอ่านออก** (กติกา Panya 2026-08-24) — ตอบต่อเฟรม (1/2/3): ข้อความอะไรขึ้น (ก๊อปคำเป๊ะ ชื่อไอเทม+จำนวน) / ข้อความอื่น (P3 — คำเป๊ะ+สี) / ยังไม่เห็นข้อความในรอบนี้
- "ไม่ขึ้น" ทุกแบบ = **`NO-RESULT / รอ Panya`** · 🔴 **ห้ามเขียนคำว่า "ไม่มี" หรือ "ไม่เกิด"**
- หลักฐานบังคับ: ภาพ **S0..S2** เป็น **JPEG กว้าง <=1280 px · ต่ำกว่า 500 KB ต่อไฟล์** ลง `evidence_screens\` + วิดีโอต่อเนื่องทั้ง session ลง `evidence_video\` (กฎ 2026-08-24) · sha256 ทุกไฟล์ · การผูก "บรรทัดไหนขึ้นหลังเฟรมไหน" ต้องอ่านจาก timestamp วิดีโอเทียบ log — ห้ามเดาจากความจำ
- ถ้าบูตรวม GT-060: ทุกข้อสังเกตต้องระบุเลนผู้ก่อ — แยกไม่ออก = NO-RESULT ต่อข้อสังเกตนั้น
- NO-CRASH / CRASH verdict ชัดเจน
- **ชั้นนี้ตอบไม่ได้:** เฟรมออกจากเซิร์ฟเวอร์จริงไหม ไบต์ตรง pin ไหม **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

### 🔴 ผลลบมีค่าเท่าผลบวก
- **wire ครบ 3 เฟรมตรง pin แต่จอไม่ขึ้นอะไรเลย (P2)** = ข้อมูลจริงว่า "สามทรงนี้ยังไม่พอ" — บันทึกเป็น NO-RESULT ตามกติกา (ห้ามคำว่า "ไม่มี/ไม่เกิด") · redirect: ออกแบบทรงชุดถัดไป (เช่น ItemBagAttr มี delta จริง / ค่า R4 อื่น) เป็นใบ sweep ใหม่ — ไม่ใช่รันซ้ำทรงเดิม
- **P3 (ข้อความอื่นขึ้น)** = ผลบวกของใบในความหมายกว้าง — เราได้ mapping ทรง->ข้อความ ชิ้นแรกของโปรเจกต์ · redirect: เปิดใบ static ตีความฟิลด์ status ที่ต้องสงสัย
- **P4 (reject/หลุด)** = ชี้ version byte/โครงซองก่อน semantics — เทียบไบต์เรากับ capture RE-059 ทีละฟิลด์ก่อนสงสัยอย่างอื่น

### nonclaims (ติดไปกับผลทุกกรณี)
- พิสูจน์ **"ทรงไหนทำให้ข้อความขึ้น"** เท่านั้น — **ไม่ตีความความหมายของฟิลด์ใด ๆ** (R4, mask, โครง ItemBagAttr ฯลฯ)
- **ไม่ claim ว่าเซิร์ฟเวอร์ต้นฉบับ (ปิดแล้ว กู้ไม่ได้ตลอดกาล) เคยส่งทรง count>0 แบบนี้** — เฟรม 2/3 เป็นดีไซน์ของเราล้วน (capture มีแต่ count=0)
- item id `2400901` ที่ใช้เป็น probe อิงสคีม RE-060 ซึ่ง pin ด้วยหลักฐานชนิด **ค (candidate 100%-hit) — ไม่ใช่การยืนยันบนสาย** · ถ้าชื่อไอเทมบนจอไม่ตรงตาราง = finding ใหม่ ไม่ใช่ความผิดของใบ
- **ไม่พิสูจน์ว่าไอเทมเข้ากระเป๋า/DB จริง** — ใบนี้วัดแค่บรรทัดแชต (เลนอ่าน bag state เป็นคำถามแยก)
- **ไม่แตะ claim ของ GT-060** (`PickupTerrainThing` `0x4543` ขาออก) — ต่อให้บูตรวมกัน ผลของสองใบแยกกันเด็ดขาดตามวินัย attribution
- **result:** (ผู้เทสกรอก: ทรงไหนทำให้ข้อความอะไรขึ้น — ต่อเฟรม 1/2/3 · คำเป๊ะของบรรทัดที่ขึ้น + สี · ภาพ S0..S2 (JPEG <=1280 · <500 KB · `evidence_screens\`) + วิดีโอ (`evidence_video\`) พร้อม sha256 · timestamp วิดีโอเทียบเฟรมจาก log · จำนวน trigger x เฟรมที่ออกจริง + sha ตรง pin ไหม · บรรทัด `PF-EVENT` dispatch/reject ที่เห็น (ก๊อปทั้งบรรทัด) · ถ้าบูตรวม: attribution ต่อข้อสังเกต · NO-CRASH/CRASH · เวลา +07:00 · sha canonical ก่อน-หลัง · row-diff + `max(lease_generation)` ของ `run_gt063.sqlite3`)


---

## GT-064 SKILL-ATTR-WINDOW-KPRESS-IN-GAP-001 [attended, in-game]: กด **K** / คลิก `Bt_main_Skill` **ภายในช่อง 3.0 วิ ระหว่างเฟรม `COUNT0` (57B) กับ `COUNT1` (68B)** ของ skill-attr sweep แล้วหน้าต่างสกิล (`Skill_Main2`) เปิดไหม — ปิดคำถาม A/B ที่ GT-059 ทิ้งไว้  [✅ **PASS — สมมติฐานถูกหักล้าง (P2) · จ็อบ 1112 · 2026-08-25 00:38-00:58 (+07:00) · attended (Panya ขับ UI เอง) · จดหมาย `20260825_0105` · บันทึกโดย chief R158** — **คำตอบ: ไม่จริง** · กด `K` รัว ๆ และคลิก `Bt_main_Skill` **ภายในช่อง 3.0 วิ** ก็ไม่เปิด ⇒ **nonclaim ① ที่ค้างจากการปิด GT-059 ปิดแล้ว — A/B ไม่ใช่ UNRESOLVED อีกต่อไป** · อ่านคู่กับ GT-059: ไม่ว่าจะกดตอนไหน (ก่อนเฟรม · ระหว่างช่อง · หลัง sweep · หลัง relog) ไม่เปิดทั้งหมด · **wire:** sweep ออกจริงสองรอบ (`COUNT0_EMPTY` 57B · `COUNT1_KEY1` 68B · late ≤0.5 ms) · 🔴 **`--export-events` ตรึงขอบช่องด้วยเวลาสัมบูรณ์จากล็อกได้เป็นครั้งแรก** แทนการเดาจากภาพ (Enter `00:50:06.056` / `00:50:28.156` ⇒ ช่อง t=684.1-687.1 / t=706.2-709.2 ในวิดีโอ) — เครื่องมือคุ้มทันทีในรอบแรกที่ใช้ · **client-observable:** ครอปมุมล่างซ้ายทีละ 0.25 วิ พิสูจน์ว่า tooltip `สกิล (K)` ค้างทุกเฟรมตลอด 3 วินาที ⇒ เคอร์เซอร์จอดบนปุ่มจริง **และ tooltip เรนเดอร์ได้เฉพาะตอนหน้าต่างเกมโฟกัส** ⇒ ปิดข้อแก้ตัว "เกมไม่ได้โฟกัส/กดไม่ทัน" ไปพร้อมกัน · ภาพเต็มจอ t=683.0-690.0 ไม่มีหน้าต่างสกิลสักเฟรม · **CODE_DELTA_vs_main = 0** (ด่านใหม่แทน tree-equality — เหตุผลและใบเสร็จอยู่ในจดหมาย §④; chief R158 แก้ `pf_resolve_green_boot.py` ให้ถาม "โค้ดที่รันเปลี่ยนไหม" แทน "tree เหมือนไหม" แล้ว) · `SESSIONS_SELECTED 10 -> 11` ตามเกณฑ์ใบ · CANON ตรง · 🔴 **nonclaims:** ① control `C` เป็นคำให้การ ไม่ใช่วิดีโอ (หน้าต่างเกมออกจากจอราว t=742) ② วิดีโอพิสูจน์ว่าเคอร์เซอร์อยู่บนปุ่ม แต่แยก "คลิกจริง" ออกจาก "วางเมาส์" ไม่ได้จากภาพ ③ **ไม่ได้ระบุสาเหตุ** — สองเคสของ RE-062 ยังแยกไม่ได้ ต้องมีตัววัด runtime ④ ไม่อ้างข้ามชั้น ⑤ บูตด้วย commit ที่ไม่ใช่ผลของ resolver — เหตุผลใน §④ ของจดหมาย] *(สถานะเดิมก่อนปิด:* [🟢 **READY** · เปิดตาม nonclaim ① ของการปิด GT-059 (chief R155 · จดหมาย `notes_to_chief\20260824_2133_PANYA-VISUAL-SIGNOFF-GT059-negative-confirmed-on-continuous-video.md`) · เลนโค้ดอยู่บน `main` แล้วตั้งแต่ `543382c` (PR #21 — สืบทอดจาก GT-059 ทั้งเลน ไม่มีโค้ดใหม่) · เลน attended **ปลดพักแล้วโดย Panya** (2026-08-24 ~21:1x +07:00 · จดหมาย 2120 §① · บันทึก R155) · เงื่อนไขเดียวที่เหลือเช็คตอนบูต: resolver คืน `BOOT_COMMIT` ที่มีเลนนี้จริง (บล็อก "ก่อนบูต" ข้างล่าง)]

**ที่มา (อ่านก่อนบูต — ใบนี้เกิดจากช่องว่างที่เหลือชิ้นเดียวของ GT-059):**
- **GT-059 = CLOSED P2 (FALSIFIED · chief R155):** รับ `CSkillAttr` แล้วหน้าต่างสกิล**ไม่เปิด** — พิสูจน์ด้วยตา Panya บนวิดีโอต่อเนื่องสองไฟล์ (จดหมาย `2133`) · **แต่ทุกการกด K / คลิกปุ่มในรอบนั้นลง "นอก" ช่อง 3 วิ ระหว่างสองเฟรมทั้งหมด** — ไม่มีใครกดในช่องเลยแม้แต่ครั้งเดียว ⇒ nonclaim ① ของจดหมาย 2133 คือคำถามที่ใบนี้ตอบ: *"ถ้ากดตรงนั้นจะเปิดไหม"*
- **ทำไมรอบ unattended พลาด S1 (จดหมาย `notes_to_chief\20260824_1757_GT059-NO-RESULT-unattended-no-skill-window-wire-exact.md`):** round-trip ของ computer-use ยาวเกินหน้าต่าง 3 วิ — action ลงหลัง `COUNT1_KEY1` เสมอ · **มือคนกดทัน** (จังหวะที่วัดจริง: Enter → `COUNT0` = 0.560 วิ **(n=1 — วัดครั้งเดียวในรอบ 1757 ยังไม่รู้ variance)** · `COUNT0` → `COUNT1` = 3.000-3.001 วิ (n=3)) — นี่คือเหตุที่ใบนี้เป็น attended เท่านั้น
- **สถานะระหว่างสองเฟรมคืออะไร:** ช่องนี้ = ไคลเอนต์รับ `COUNT0_EMPTY` (attr block ว่าง) ไปแล้ว แต่ยังไม่รับ `COUNT1_KEY1` · ใบนี้วัดว่า "สถานะหลัง COUNT0 ก่อน COUNT1" เปิดหน้าต่างได้ไหม — GT-059 วัดเฉพาะก่อนเฟรมแรกและหลังเฟรมสุดท้าย

### objective (claim เดียว)
**การกด K หรือคลิก `Bt_main_Skill` ที่ลง "ภายใน" ช่อง 3.0 วิ ระหว่างการ dispatch `HYP_PF_035_SKILL_ATTR_COUNT0_EMPTY` (57 bytes) กับ `HYP_PF_035_SKILL_ATTR_COUNT1_KEY1` (68 bytes) ทำให้หน้าต่างสกิลเปิดหรือไม่**
(ใบนี้พิสูจน์เฉพาะการกด**ในช่อง** — การกดนอกช่องถูกปิดไปแล้วโดย GT-059 และ**ไม่นับเป็นผลของใบนี้**)

### 🔴 นิยาม "ในช่อง" + วินัยตัดสิน attempt (ท่องก่อนบูต)
- attempt หนึ่งครั้ง = trigger หนึ่งครั้ง + การกด/คลิก**หนึ่งครั้งเดียว** (ห้ามรัว — หนึ่ง press ต่อหนึ่งการวัด ไม่งั้นจับคู่กับวิดีโอไม่ได้)
- press นับเป็น **ในช่อง** ต่อเมื่อ `t_press` (อ่านจากวิดีโอ + crosswalk wall-clock ท่าเดียวกับจดหมาย 2133) อยู่ใน `[t_COUNT0 + 0.5s, t_COUNT1 - 0.5s]` โดย `t_COUNT0`/`t_COUNT1` อ่านจาก timestamp การ dispatch ใน raw log · ถ้าแถบความไม่แน่นอนของ crosswalk คร่อมขอบช่อง ⇒ **attempt นั้น = NO-RESULT ของ claim นี้ จดตรง ๆ ห้ามแต่งผล**
- **จังหวะมือ (timing aid):** Enter → `COUNT0` ออก ~0.6 วิ ⇒ กด/คลิกที่ **~2.0 วิ หลัง Enter** (นับ "หนึ่งพัน-สองพัน") จะลง ~1.4 วิ หลัง `COUNT0` — กลางช่องพอดี · ตัวยืนยันสด = บรรทัด `[G>]` / `PF-EVENT` บน console server (**ดูด้วยตาอย่างเดียว ห้ามคลิกหน้าต่าง console — click = ขโมย focus จากเกม**)
- ทำได้**สูงสุด 3 attempts ต่อ session** (เลนไม่ one-shot ยิง trigger ซ้ำได้) · ครบ 3 แล้วยังไม่มี attempt ที่ in-gap ⇒ ปิด session แล้วเปิด session ใหม่ได้หนึ่งครั้ง (สำเนา DB ใหม่ `run_gt064b.sqlite3`) · ยังไม่ได้อีก = ใบทั้งใบ **NO-RESULT ไม่ปิด** รายงาน chief

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)
- **P1:** press ในช่องเปิดหน้าต่างได้ (มี/ไม่มีรายการ) — finding ใหญ่: gate ผูกกับสถานะชั่วคราวหลัง `COUNT0` ⇒ redirect: เลน server ควรมี variant ที่ค้างสถานะนั้นไว้
- **P2:** press ในช่องก็**ไม่เปิด**เหมือนกัน — ผลลบที่สมบูรณ์ ปิดคำถาม A/B ทุกจังหวะกดที่เคยตั้งไว้ ⇒ ทางเดียวที่เหลือของเรื่องนี้คือตัววัด runtime ของ `[actor+0x3E8]` (งาน chief — แยกใบ)
- **P3:** client reject/หลุด — ชี้ version byte 0 (ดีไซน์เรา ยัง unpinned) ก่อน semantics ตามบทเรียน GT-058/059
- **NO-RESULT:** ไม่มี press ใดถูกตัดสินว่า in-gap ได้ — ไม่ใช่ผลลบ ห้ามอ่านเป็นหลักฐานทางใด ใบไม่ปิด

### 🔴 ก่อนบูต — resolve commit เขียว (ท่าเดียวกับ GT-059 · รันเครื่องมือ ไม่ใช่ก๊อป SHA)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` · **exit 3** = ใบนี้รอ gate ไม่ได้รอผู้เทส ห้ามบูต · บรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ จดลงผลเสมอ
- **ยืนยันสี่ข้อกับ `<SHA>` ที่จะบูตจริง (ต้องครบทั้งสี่ — ชุดเดียวกับ GT-059):**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "skill-attr-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/skill_attr_hypothesis_attr_sweep.json && echo SCENARIO_PRESENT
git grep -n "COUNT1_KEY1" <SHA> -- src/pirateforce_foundation/ scenarios/
```
1. `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ · 2. เจอ flag จริง (**ห้ามใช้ `--help` เป็นหลักฐาน**) · 3. เห็น `SCENARIO_PRESENT` · 4. เจอ label `COUNT1_KEY1` ในซอร์ส
- **ยืนยันเพิ่ม (ตัวช่วยจับจังหวะ):** `git grep -n "export-events" <SHA> -- src/pirateforce_foundation/app.py` — เจอ ⇒ ใส่ `--export-events` ในคำสั่งบูต แล้วใช้บรรทัด `PF-EVENT` บน console เป็นตัวยืนยันสด · ไม่เจอ ⇒ ตัด flag ออก จดไว้ แล้วใช้ `[G>]` action labels + raw SENT hexdump แทน (ท่า GT-059 R152)
- **อ่านค่า pin ต่อเฟรมจาก scenario ใน commit ที่บูต:** `scenarios/skill_attr_hypothesis_attr_sweep.json` -> `probe.per_step.<LABEL>.frame_sha256`/`frame_size` (57/68) — **ค่า sha ตัวจริงอ่านจากไฟล์ ห้ามฝังเลขในใบนี้**
- ไม่ครบสี่ข้อ + ยังไม่ได้ค่า pin = **ห้ามบูต** ใบอยู่ READY รอต่อ

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-064_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt064.sqlite3
```
- เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง** (canonical ไม่ถูกเปิดตลอดรอบ)
- เลนนี้ `database_write=none` · เกณฑ์สำเนาแบบ GT-059: **row-diff ทุกตารางต่างได้เฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง** (ไม่ใช้ byte-identical ซึ่งขัดกับ session persist) · จด `max(lease_generation)` ก่อน-หลัง
- ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกบูต (สำเนา DB ใหม่ทุกครั้ง)

### server args (เป๊ะ — opt-in เท่านั้น · `production_allowed=false`)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt064.sqlite3 --skill-attr-hypothesis-scenario scenarios\skill_attr_hypothesis_attr_sweep.json --export-events
```
- `--export-events` ใส่เฉพาะเมื่อ git grep ยืนยันว่ามีใน `<SHA>` (บล็อกก่อนบูต) — ไม่มีก็ตัดออก
- console ต้องขึ้น mode `skill-attr-hypothesis` — ใช้เช็คว่าบูตถูกโหมด

### 🔴 ตัว trigger แชต — 12 ตัวอักษร printable ASCII เป๊ะ (บทเรียนที่เคยเสียเวลาโปรเจกต์)
- ใช้ `skillattr001` (นับ: s-k-i-l-l-a-t-t-r-0-0-1 = 12 ตัวพอดี) — สั้น/ยาวกว่านั้นถึงเซิร์ฟเวอร์แต่**เงื่อนไขเงียบ ๆ ไม่ผ่าน ไม่มี error** sweep ไม่ออกเฉย ๆ
- 🔴 **คลิกช่องแชตให้โฟกัสก่อนพิมพ์** (ตัวอักษรตอนไม่โฟกัส = hotkey) · Enter หนึ่งครั้ง · **ก่อนกด K ต้องปลดโฟกัสแชตก่อนเสมอ** (คลิกพื้นว่าง) ไม่งั้น K กลายเป็นตัวอักษรในช่องแชต
- **identity guard:** เลนยิงเฉพาะตัวละครช่องแรกของ account แรก (`identity_lo 0x10010001`) — เลือกผิดช่อง เลนปฏิเสธเงียบ

### steps
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบตามบล็อก db
1. เปิด server ก่อน client เสมอ (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client) — console ขึ้น mode `skill-attr-hypothesis` · **จัดหน้าต่าง console ให้มองเห็นได้ข้างจอเกมโดยไม่บังพื้นที่วัด — ตลอดรอบห้ามคลิกมัน** (🔴 client ที่บูตโดยไม่มี server ตายเองใน ~3.5 นาที)
2. เปิด client → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → **เลือกตัวละครช่องแรก** → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
3. เข้าแมพ เห็น HP/minimap/ชื่อแมพ → **เริ่มอัดวิดีโอต่อเนื่องตั้งแต่ตรงนี้ยาวจนจบ session** ลง `evidence_video\` (ช่อง 3 วิ ตัดสินด้วยวิดีโอเท่านั้น — ภาพนิ่งเป็น point-sample ใช้ตัดสินจังหวะไม่ได้)
4. **BASELINE:** คลิกพื้นว่าง → กด **K** → คลิก `Bt_main_Skill` → ถ่าย **S0** · คาดว่า**ไม่เปิด** (GT-058/059 ปิดแล้ว) — ถ้า baseline เปิดได้เฉย ๆ จดใหญ่ ๆ (เงื่อนไขใบเปลี่ยน) แล้วรายงานก่อนทำต่อ
5. **ATTEMPT 1 — ทางคลิก (ตัวหลัก เพราะ cursor+คลิกเห็นบนวิดีโอ ตัดสินง่ายสุด):** คลิกช่องแชต → พิมพ์ `skillattr001` → Enter หนึ่งครั้ง → เลื่อน cursor ไปบน `Bt_main_Skill` ทันที → **คลิกหนึ่งครั้งที่ ~2.0 วิ หลัง Enter** (นับ "หนึ่งพัน-สองพัน" · เหลือบดู `[G>]`/`PF-EVENT` เป็นตัวยืนยันว่า sweep ออก — ห้ามคลิก console) → จ้องจอต่อจนพ้น `COUNT1` (>4 วิ หลัง Enter) → ถ่าย **S1** · จด tri-state: **เปิด+มีรายการ / เปิด+ว่าง / ไม่เปิด** และจดว่าตอน `COUNT1` มาถึง จอเปลี่ยนอะไรไหม
6. เว้น >10 วิ · **ATTEMPT 2 — ทาง K:** คลิกช่องแชต → `skillattr001` → Enter → **คลิกพื้นว่างทันที** (ปลดโฟกัส) → เลื่อน cursor ไป hover บน `Bt_main_Skill` (tooltip `สกิล (K)` โผล่ = เกมโฟกัสอยู่จริง) → **กด K หนึ่งครั้งที่ ~2.0 วิ หลัง Enter พร้อมสะบัด cursor แรง ๆ หนึ่งที** (K-mark — ให้วิดีโอมีจุดเวลาของการกด) → จ้องจอจนพ้น `COUNT1` → ถ่าย **S2** · จด tri-state เหมือนข้อ 5
7. **ATTEMPT 3 (ถ้าข้อ 5/6 มีอันที่คาดว่าไม่ทัน/คร่อมขอบ):** ทำซ้ำด้วยท่าที่ adjudicate ได้ดีกว่า → ถ่าย **S3** · สูงสุด 3 attempts ต่อ session — เกินนั้นดูวินัยตัดสิน attempt ข้างบน (session ใหม่ได้หนึ่งครั้ง `run_gt064b.sqlite3` · restart server ก่อนเสมอ)
8. **control:** กด **C** เปิดหน้าต่าง `CHARACTER` → ถ่าย **S4** → ปิด = positive NO-CRASH control (ท่าเดียวกับ GT-059)
9. จับ NO-CRASH / CRASH: client ยังตอบสนอง (ขยับกล้อง `Q/E` ได้) = NO-CRASH · หลุด/ค้าง = CRASH + จดว่าที่เฟรมไหน (ชี้ version byte 0 ก่อน — P3) *(🔴 **หมายเหตุ chief R163 — ไม่ใช่การแก้ขั้นตอน:** ใบนี้**ปิดไปแล้ว** ขั้นตอนข้างบนคือขั้นตอนที่รันจริงในรอบนั้น **จึงคงไว้ตามเดิมทั้งตัวอักษร** · ฉบับแรกของ R163 เขียนทับมัน ซึ่งผิดกติกา — `pf-adversary` จับได้ ถอนแล้ว · **ถ้ารอบนั้นใช้ `Q/E` จริง แปลว่ามี `TargetPosVital` ออกกลางรอบ ซึ่งเป็นข้อเท็จจริงที่กระทบการอ่านผล ห้ามลบร่องรอย** · สำหรับรอบ **ใหม่** ให้ใช้ **คลิกขวาค้างลากเมาส์** เช็ค NO-CRASH แทน — เหตุผลอยู่ในบล็อกกฎกล้องของ PLAYBOOK)*
10. ออกจากเกม: **X** มุมขวาบน (ตรวจก่อนว่าไม่มีหน้าต่างอื่นบัง) → dialog ยืนยัน → ปุ่มซ้าย → **ปิด server ด้วย** (🔴 server เก็บ session ค้าง — client ตัวถัดไปจะค้าง "connecting" ตลอดกาลถ้าไม่ restart server ก่อน)
11. เก็บ raw GAME log ทั้งไฟล์ + console out/err (รวม `[G>]`/`PF-EVENT` ทุกบรรทัด) → `PRAGMA integrity_check;` บนสำเนา
12. **teardown เสมอ** แม้เลิกกลางคัน (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 — เพดานยกจาก 180 เมื่อ 2026-08-20 · `TEMPLATE_teardown_generic.ps1:135` · แท่นถูกทิ้งข้ามชั่วโมงใช้ `staged\TOOL_stop_stale_server.ps1`)
13. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม
14. **หลังรอบ — ตัดสิน in-gap ต่อ attempt:** crosswalk wall-clock วิดีโอกับ raw log (ท่าจดหมาย 2133: เวลาใน log ลบเวลาเริ่มอัดในชื่อไฟล์ + cross-check ป้ายวินาที) → ต่อ attempt จด `t_COUNT0` / `t_press` / `t_COUNT1` และ verdict **IN-GAP / OUT / UNDECIDABLE** — OUT และ UNDECIDABLE = NO-RESULT ของ attempt นั้น

### pass criteria — สองชั้น แยกกันเด็ดขาด
**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ · ทำ headless ได้)**
- raw GAME log ต่อ trigger: **2 เฟรม** เรียง `HYP_PF_035_SKILL_ATTR_COUNT0_EMPTY` (57 bytes) → `HYP_PF_035_SKILL_ATTR_COUNT1_KEY1` (68 bytes) ห่าง ~3.0 วิ · sha256 ต่อเฟรม**ตรง pin** ใน `scenarios/skill_attr_hypothesis_attr_sweep.json` ของ commit ที่บูต · จำนวนคู่เฟรม = จำนวน trigger ที่ยิงจริง · เก็บ hexdump ทั้งไฟล์ **ห้ามลบ**
- **timestamp การ dispatch ของ `COUNT0`/`COUNT1` ต่อ attempt อ่านออกมาเป็นตัวเลขระดับ ms** — นี่คือขอบช่องที่ใช้ตัดสิน in-gap (ชั้นนี้ให้ "ขอบ" แต่**ตัดสิน t_press ไม่ได้** — t_press อยู่ชั้น 2)
- ตัวยืนยัน dispatch: บรรทัด `PF-EVENT` (ถ้าบูตด้วย `--export-events`) หรือ `[G>]` labels + raw SENT hexdump ตรง pin (ท่า GT-059 R152) — raw frame ตรง pin คือหลักฐานปฐมภูมิเสมอ
- DB สำเนา: `PRAGMA integrity_check` = `ok` · row-diff ทุกตารางต่างเฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง · `max(lease_generation)` ก่อน-หลังจดไว้ · sha256 canonical ก่อน-หลังตรงกัน
- **ชั้นนี้ตอบไม่ได้:** press ลงเมื่อไร · หน้าต่างเปิดไหม ⇒ **ห้ามอ้างชั้นนี้แทนชั้น (2)**

**ชั้น (2) client-observable (ต้องมีคนหน้าจอ — ตัวปิดใบอยู่ชั้นนี้)**
- วิดีโอต่อเนื่องทั้ง session ลง `evidence_video\` + ภาพ **S0..S4** (JPEG กว้าง <=1280 px · <500 KB ต่อไฟล์ ลง `evidence_screens\` — กฎ 2026-08-24) · sha256 ทุกไฟล์
- ต่อ attempt: verdict **IN-GAP / OUT / UNDECIDABLE** (จากขั้น 14) + tri-state **เปิด+มีรายการ / เปิด+ว่าง / ไม่เปิด** ณ จังหวะ press และหลัง `COUNT1` มาถึง · ถ้าเปิด: บรรยายเนื้อในเป็นภาษาคน (กี่แถว/ช่อง · ว่างไหม) — ห้ามตีความความหมายค่าที่เห็น
- **ใบปิดได้ต่อเมื่อมี attempt ที่ IN-GAP ยืนยันแล้วอย่างน้อย 1 ครั้ง และผลชัด** — ผลลบ (ไม่เปิด) ปิดได้เฉพาะ **รอบ attended ที่ Panya เห็นเอง + วิดีโอต่อเนื่อง** (เงื่อนไข R152b · กฎ AGENTS.md §9: รอบ unattended ปิดผลลบไม่ได้) · press ที่ OUT/UNDECIDABLE พิสูจน์อะไรใหม่ไม่ได้เลย — จดเป็น NO-RESULT ของ attempt ห้ามนับเป็นผลลบ (press ที่ไกลช่องชัดเจนถูกปิดไปแล้วโดย GT-059 · press ที่อยู่ในแถบขอบ 0.5 วิ GT-059 **ไม่เคยวัด** — มันแค่ตัดสินไม่ได้ด้วย crosswalk ของเรา)
- control `C` เปิด `CHARACTER` ได้ = NO-CRASH · NO-CRASH/CRASH verdict ชัดเจน
- **ชั้นนี้ตอบไม่ได้:** เฟรมออกจากเซิร์ฟเวอร์จริงไหม ไบต์ตรง pin ไหม **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

### 🔴 ผลลบมีค่าเท่าผลบวก
- **P2 (IN-GAP แล้วยังไม่เปิด · Panya เห็นเอง)** = ผลลบที่สมบูรณ์ **ไม่ใช่ FAIL** — ปิดคำถาม A/B ค้างของ GT-059 ทุกจังหวะกด ⇒ redirect: เลิกลงทุนกับจังหวะกดในเลนนี้ · เส้นทางเดียวที่เหลือคือ**ตัววัด runtime ของ `[actor+0x3E8]`** (แยกเคส slot-null vs check อื่นใน `0x761ED0` — งานออกแบบของ chief เปิดได้แล้วตามคำเคาะ 2120 §④ ไม่ใช่ส่วนของใบนี้)
- **P1 (เปิดได้เฉพาะในช่อง)** = ผลบวกแบบมีเงื่อนไขจังหวะ — redirect: เลน server variant ที่ค้างสถานะหลัง `COUNT0` + ใบ static ว่าสถานะนั้นต่างอะไร
- **NO-RESULT (ไม่มี press ที่ IN-GAP)** = ไม่ใช่ผลลบ ห้าม archive ใบตามกฎคิว — จดจังหวะที่ทำได้จริงกลับมาให้ chief ปรับ timing aid

### nonclaims (ติดไปกับผลทุกกรณี)
- **ไม่ตัดสินสาเหตุ** — เคส (ก) `[actor+0x3E8]` null จริง vs (ข) slot มีของแต่ check อื่นใน `0x761ED0` ขวาง เป็นงานตัววัด runtime แยกใบ ใบนี้ไม่แตะ
- **ไม่อ้างข้ามชั้น** — เฟรมออก != จอเปลี่ยน · จอไม่เปลี่ยน != เฟรมไม่ออก
- **ไม่ claim ว่าเซิร์ฟเวอร์ต้นฉบับ (ปิดแล้ว กู้ไม่ได้ตลอดกาล) เคยส่ง `CSkillAttr` รูปนี้/spacing นี้/จังหวะนี้** — เฟรม ค่า record, spacing 3.0 วิ และ trigger policy เป็นดีไซน์ของเราทั้งหมด
- **ไม่ตีความ `key=1`/`opaque_u16`/`opaque_u32`** — ค่า probe ตามใจเรา ความหมายไม่รู้
- **ไม่พิสูจน์ว่าสกิลใช้งานได้** — วัดเฉพาะ window gate เปิด/ไม่เปิด
- **ผลบวกไม่พิสูจน์ว่า in-gap เป็นเงื่อนไขเดียว** และ**ผลลบไม่ครอบคลุมจังหวะที่ตัดสินไม่ได้** (press ชิดขอบช่องกว่า 0.5 วิ อยู่นอก claim)
- **result:** (ผู้เทสกรอก: ต่อ attempt — `t_COUNT0`/`t_press`/`t_COUNT1` + verdict IN-GAP/OUT/UNDECIDABLE + tri-state ณ press และหลัง COUNT1 · ทางคลิก/ทาง K แยกกัน · ภาพ S0..S4 + วิดีโอ พร้อม sha256 · path raw GAME log + label/sha 2 เฟรมต่อ trigger ตรง pin ไหม · บรรทัด `PF-EVENT`/`[G>]` ที่เห็น (ก๊อปทั้งบรรทัด) · NO-CRASH/CRASH · Panya เห็นเองไหม (ผลลบปิดได้เฉพาะเห็นเอง) · เวลา +07:00 · sha canonical ก่อน-หลัง · row-diff + `max(lease_generation)` ของ `run_gt064*.sqlite3`)

---

## GT-069 GROUNDLOOT-NAMELABEL-TEXTPROP-SELECTOR-001 [attended, in-game]: ยิง **เฟรมคุม (mask `0x12`) กับเฟรมทดลอง (mask `0x3A` · gate `+0x1B`=1 · index `+0x1A`=6) ที่พิกัดเดียวกัน** แล้วดูว่า **หน้าตาของป้ายชื่อไอเทมบนจอต่างกันหรือไม่**  [🔴 **BLOCKED ×2 — ต้องปลดครบทั้งสองข้อ:** **(1) เจ้าของเคาะว่าเลนนี้เกิดได้หรือไม่** (ดูบล็อก "งบเวอร์ชัน" ข้างล่าง — **ข้อนี้ยังไม่ถูกเคาะ**) · **(2) ผ่านด่านเจ็ดข้อบน commit ที่ gate ตัดสินแล้ว** · โค้ดถูก push ขึ้น branch และ **จงใจยังไม่ merge เพราะข้อ (1)** ⇒ **ถ้าเจ้าของยังไม่เคาะ ใบนี้รอเจ้าของ ไม่ได้รอผู้เทส และไม่ได้รอ CI** · เปิดใบโดย chief R165 (2026-08-25 ~17:0x +07:00) ตามบรรทัดปิดท้ายของ `RE-067`]

> 🟢🟢 **อัปเดต chief R167 · 2026-08-25 ~19:xx (+07:00) — บล็อกทั้งสองข้อขยับ อ่านให้ครบก่อนบูต**
> **ข้อ (1) ปลดแล้ว** โดยคำเคาะเจ้าของ ~17:5x (+07:00) (จดหมาย `notes_to_chief\consumed\20260825_1800_PANYA-RULING-GT069-new-entry-HYP-PF-039-plus-attended-queue-is-drained.md`):
> เลนนี้เกิดเป็น **entry ใหม่ `HYP-PF-039`** (checkpoint `GROUND-LOOT-NAMEPROP-001`) พร้อมงบเวอร์ชันของตัวเอง · **`HYP-PF-032` ไม่ถูกแตะ ไม่ถูก override** และได้ **หมายเหตุ scoped** เขียนลง `evidence_gap` ของมันแล้วในรอบนี้
> **ข้อ (2):** 🔴 **สิ่งที่ค้างจริงไม่ใช่ CI — โค้ดเขียวอยู่แล้ว แต่ไม่เคยมีใครเปิด PR ให้มันเลย**
> วัดในรอบนี้: branch `claude/elegant-lamport-ywug3f` sha `13baff27` · `ci/13baff27….json` = `"conclusion":"success"` (run `32838572131`, 2026-08-25 10:47 UTC = 17:47 +07:00) · `list_pull_requests` ด้วย head นั้น = **ว่างเปล่า** ⇒ R165 **จงใจไม่เปิด PR** เพราะรอคำเคาะงบเวอร์ชัน (ถูกแล้ว) **แต่ไม่มีกลไกไหนพามันกลับเข้าเส้นทางหลังคำเคาะมาถึง**
> ⇒ **R167 เอาเลนนี้มา merge บน branch ของตัวเองแล้วเปิด PR ให้** (แก้ conflict สองไฟล์: pin `GRADE_SUBSET_SHA256` และ `CANONICAL_CONTENT_SHA256` คำนวณใหม่บนเนื้อที่ merge แล้ว)
> 🔴 **ก่อนบูต ต้องเช็คว่า `main` มี `src/pirateforce_foundation/ground_loot_nameprop_hypothesis.py` จริง** (`BOOT_COMMIT` ต้องอยู่หลัง merge ของ R167) — ถ้าไม่มี แปลว่า PR ยังไม่ merge **ห้ามบูต** เพราะ flag `--ground-loot-nameprop-scenario` จะไม่มีอยู่
> **สถานะใบตอนนี้:** 🟠 **รอ merge อย่างเดียว — ไม่รอเจ้าของ ไม่รอผู้เทส**


**ที่มา (สามแหล่ง อ่านก่อนบูต — ทั้งหมดวัดแล้ว ห้าม re-derive ระหว่างรอบ):**
- **`RE-067` (CLOSED PASS/MIXED · 2026-08-25 16:26 +07:00 · static · verifier `re067_static_verify.py` 54/54 exit 0):** พิน selector ของป้ายชื่อไอเทมบนพื้นในไคลเอนต์ที่ ship มา — element **`+0x1B` = GATE** (`cmp byte [element+0x1B],0` · ศูนย์ ⇒ push **default UI text property `0x34`**) · element **`+0x1A` = INDEX** (signed · รับเฉพาะ `1..6`) lookup `dword [index*4 + 0x00F30EC4]` ⇒ map `1..6 -> 0x5D..0x62` · นอกช่วง ⇒ กลับไป `0x34` · ctor ของ element ตั้ง default **`+0x1B=0`, `+0x1A=1`** · ใน list codec: dirty-mask bit **`0x08` -> `+0x1B`** · bit **`0x20` -> `+0x1A`**
  🔴 **สิ่งที่ `RE-067` พินคือ "UI text property" ไม่ใช่ "สี"** — `0x34` และ `0x5D..0x62` เป็นอะไรก็ได้: ฟอนต์ · ขนาด · สไตล์ · การจัดวาง · หรือพรีเซ็ตทั้งชุด ⇒ **ชื่อใบและถ้อยคำในใบจึงพูดว่า "text property / หน้าตา" ไม่ใช่ "สี"** · (ผู้เทสยัง **จดสีที่เห็นเป็นคำพูดตามเดิมทุกประการ** — นั่นคือการบันทึกสิ่งที่เห็น ไม่ใช่การตั้งชื่อกลไก)
- **เลน ground-loot ที่ ship อยู่ (`HYP-PF-032` · GT-045 v1/v2/v3):** ส่ง element mask **`0x12 = 0x10|0x02`** (พิกัด + payload dword) เท่านั้น — **ไม่เคยมีบิต `0x08` หรือ `0x20` ออกสายแม้แต่เฟรมเดียว** ⇒ CREATE ตกไปใช้ default `0x34` เสมอ ⇒ 🔴 **หน้าตาป้ายที่ผู้เทสเคยเห็น (ตัวอักษรแดง) ยังไม่เคยเป็นสิ่งที่เราเลือก**
- **ตัวเลขเวลาที่วัดแล้วจากรอบ 1135 (จดหมาย `notes_to_chief\20260825_1615_GT045-EVIDENCE-COMMITTED-*.md` §②):** ไบต์ออกสาย -> ตัวอักษรขึ้นจอ **~0.12 วิ** · **อายุป้ายบนจอ 0.2-0.4 วิ** (recorder เขียน 30 fps แต่เฟรมไม่ซ้ำจริงมาราว 10 fps ⇒ ขอบมีความคลาดเคลื่อน +/-0.1 วิ) แล้วหายเอง — **เลนส่งครั้งเดียว ไม่ refresh ไม่มีเฟรมลบ**
  🔴🔴 **ERRATUM R166 (2026-08-25 ~17:5x +07:00) — ตัวเลข `~0.12 วิ` ข้างบน *ใช้ไม่ได้* จนกว่าใบจะมีขั้น CLAPPER**
  ที่มา: จดหมาย `20260825_1745` §④ — หน้าสะพานวัดพบเองว่า offset ระหว่างนาฬิกาวิดีโอกับนาฬิกาสาย **ไม่ใช่ค่าคงที่ แต่ต่างกันทุกบูต** (สามรอบคืน 2026-08-25 ให้ ~0 s / 0.58 s / 1.82 s)
  ⇒ `0.12 วิ` เป็นผลต่างของสองนาฬิกาที่ไม่เคยถูกจูนเข้าหากัน **จึงเป็นตัวเลขที่บวก error ขนาดไม่รู้ค่าอยู่ข้างใน** · nonclaim ข้อ 4 ของจดหมาย `20260825_1615` พูดถึงเรื่องนี้ไว้แล้ว แต่ตอนนั้นยังเข้าใจว่าเป็นค่าคงที่เล็ก ๆ
  🔴 **สิ่งที่ยังใช้ได้:** **อายุป้ายบนจอ 0.2-0.4 วิ** (วัดในนาฬิกาวิดีโอตัวเดียว ไม่ข้ามนาฬิกา ⇒ ไม่โดน erratum นี้)
  🔴 **สิ่งที่ต้องทำ — และมันไม่ใช่ clapper:** ใบนี้แก้ด้วยการ **เลิกใช้ตัวเลขข้ามนาฬิกาเป็นเกณฑ์ตัดสิน** แล้วตัดสินด้วย **ลำดับของสองแฟลชในนาฬิกาวิดีโอตัวเดียว** แทน (ดูบล็อก **หลักฐานภาพ** ข้อ ก. ท้ายใบ ซึ่งถูกแก้ในรอบเดียวกัน) — วิธีนี้ **ปลอดภัยโดยไม่ต้องมี clapper เลย**
  🔴 **ห้ามใส่ clapper ลงใบนี้** จนกว่าจะตอบได้ว่า **ชุดเลนของบูตนั้นทั้งชุดไม่มีเลนไหนยิงด้วย ascii12** — ใบนี้บูตร่วมกับเลนที่ยิงด้วยแชตได้ (`greenline001` / `HYP-PF-037`) ⇒ ดูข้อจำกัด ① ของ PLAYBOOK ข้อ 14
  🔴 **บทเรียนที่แพงที่สุดจากการวัดครั้งนั้น (nonclaim ข้อ 2 ของจดหมาย):** รอบก่อนสอง element ออกห่างกันจริง **42 ms** และผู้สังเกต **บอกไม่ได้ว่าป้ายที่เห็นคือตัวไหน** ⇒ **ระยะห่างที่ตั้งไว้ 1.50 วิ ของใบนี้คือตัวแก้ข้อนั้นโดยตรง ห้ามย่อ ห้ามรวมเฟรม** (ตัวเลข 42 ms นั้นอธิบายได้แล้ว — ดูบล็อก "ระยะห่างจริง")

---

### 🔴🔴 งบเวอร์ชัน — **ยังไม่ถูกเคาะ และนี่คือเงื่อนไขบล็อกข้อที่ (1)**
*(chief เคยเขียนในฉบับก่อนว่า "ปิดแล้วเพราะมี `HYP-PF-039`" — **ผิด และเป็นความผิดของ chief เอง** `pf-adversary` จับได้ · แก้ไว้ตรงนี้ ห้ามอ่านฉบับเก่า)*
- **`HYP-PF-029`** เขียนในช่อง `expiry.decision` ว่าการขยายเพิ่มต้องมี **"a new entry OR a scoped approval"** — **clause นี้เองคือสิ่งที่อนุญาตให้ `HYP-PF-038` เกิดเป็น entry ใหม่ตอน 3/3**
- **`HYP-PF-032`** เขียนว่า **"ANY FURTHER WIRE CHANGE TO THIS LANE NEEDS AN EXTENSION DECISION FROM THE OWNER FIRST"** — และ **ไม่มี clause "entry ใหม่"** เลย · ยิ่งกว่านั้น `stop_rule` ของมัน **แช่แข็งฟิลด์ชุดเดียวกับที่เลนนี้จะส่งพอดี** ("other element masks — `0x04`/`0x08`/`0x20` fields stay unsent")
- ⇒ **การเปิด entry ใหม่จึงไม่ใช่ทางออกที่ตัวเอกสารอนุญาตโดยอัตโนมัติ** ⇒ ต้องให้เจ้าของเคาะว่า **เลนนี้เกิดได้ในรูปใด** — เป็น **tracked version ที่สี่ของ`HYP-PF-032` พร้อม `extension_approval_ref` แบบ scoped** หรือเป็น **entry แยก `HYP-PF-039` (checkpoint `GROUND-LOOT-NAMEPROP-001`)**
- 🔴 **โค้ดถูก push ขึ้น branch และจงใจไม่ merge ด้วยเหตุผลข้อนี้โดยตรง** ⇒ **ถ้ายังไม่มีคำเคาะ ใบนี้ "รอเจ้าของ" ไม่ใช่ "รอผู้เทส" และไม่ใช่ "รอ CI"**
- 🔴 **ผู้เทสไม่ต้องตัดสินเรื่องงบเวอร์ชัน และห้ามแก้ ledger ไม่ว่าผลจะออกแถวไหน** — ถ้าไม่แน่ใจว่าเคาะแล้วหรือยัง ให้ถามก่อนบูต

### เลนที่ใบนี้บูต (ของจริงบน branch — ไม่ใช่แผน)
- โมดูล **`src/pirateforce_foundation/ground_loot_nameprop_hypothesis.py`** (🔴 **ไม่ใช่** `ground_loot_hypothesis.py`)
- flag **`--ground-loot-nameprop-scenario`** · ไฟล์ **`scenarios/ground_loot_nameprop_probe.json`** · scenario id **`ground_loot_nameprop_probe`**
- 🔴 **แยกจากเลน `HYP-PF-032` เด็ดขาด mutually exclusive ตอนบูต ไม่แชร์ state:** latch ของตัวเอง **`ground_loot_nameprop_sent`** · event ปฏิเสธ **`ground_loot_nameprop_compose_refused_no_reply`** · pair event **`hyp_pf_039_ground_loot_nameprop_pair_committed`** ⇒ **โมดูล / scenario / label / latch / ไบต์ที่ออกสายของ `HYP-PF-032` ไม่ถูกแตะ** · 🔴 **เฟรมคุมของใบนี้ถูกยิงโดยเลนใหม่เอง ไม่ใช่โดยเลนเก่า** (เลนเก่าต้องไม่ยิงเลยสักเฟรม)

### 🎯 ดีไซน์ของรอบ — **หนึ่งตัวคุม หนึ่งตัวทดลอง ที่พิกัดเดียวกัน** (ของใหม่รอบนี้ · แทนดีไซน์ "สองตัวทดลอง" ที่ถูก adversary ยิงตก)
```
frame A  GROUND_LOOT_NAMEPROP_CONTROL_ONCE  scheduler delay 0.00  element_key 3  payload_dword 2200423
         element mask 0x12  - ไม่มี gate ไม่มี index (ทรงเดียวกับที่ HYP-PF-032 ส่งอยู่ทุกวันนี้เป๊ะ)
         x = trigger + 30.0   (Y,Z = ของ trigger)      pc 44 ไบต์ / frame 54 ไบต์
frame B  GROUND_LOOT_NAMEPROP_IDX6_ONCE     scheduler delay 1.50  element_key 4  payload_dword 2200423
         element mask 0x3A  - gate +0x1B = 1, index +0x1A = 6
         x = trigger + 30.0   (Y,Z = ของ trigger)      pc 48 ไบต์ / frame 58 ไบต์
```
🔴 **dword เดียวกัน · x/y/z เดียวกัน · trigger เดียวกัน · session เดียวกัน · กล้องมุมเดียวกัน · พิกเซลชุดเดียวกัน**
⇒ **ตัวแปรเดียวที่เหลือคือ "สองฟิลด์ selector มีอยู่หรือไม่มี"** — ทุกทางออกจึงอ่านได้ (ดูตารางผล)
- **ทำไมทิ้งจุด +60:** ทั้งสอง element อยู่ที่ **+30 จุดเดียว** — เป็นจุดเดียวในประวัติโปรเจกต์ที่เคยมีคนเห็นป้ายจริง ⇒ **เกณฑ์ซูมเหลือเป้าเดียว** (ดูกฎ Z ข้างล่าง)
- **ทำไมทิ้ง index 1:** **`+0x1A` = 1 คือค่า default ของ ctor เอง** ⇒ `gate=1, index=1` จะแยกไม่ออกที่ฝั่งไคลเอนต์จาก `gate=1 โดยไม่ส่ง index` · **index 6 คือปลายสุดของช่วง `1..6` ที่ไคลเอนต์รับ** ⇒ ให้ contrast มากที่สุดเท่าที่ตารางของไคลเอนต์เองจะให้ได้เมื่อเทียบกับ default `0x34`
- trigger = **`TargetPosVital` เฟรมแรกหลัง runtime ack** (ท่าเดียวกับ GT-045 · ไม่มี chat trigger ไม่มีปุ่มยิง)

### ⏱️ ระยะห่างจริงระหว่างสองเฟรม — **"1.50 วิ" เป็นค่าที่ตั้ง ไม่ใช่ค่าที่จะวัดได้**
- send loop ที่แช่แข็งของ v141 **สะสม deadline แบบสัมบูรณ์** และ action ที่ delay = 0 **ไม่เลื่อน deadline** ⇒ **ความสายของเฟรม A ถูกหักออกจากช่องที่ B ต้องรอ**: `realized_gap ~= 1.50 - lateness(A)`
- ค่าที่โปรเจกต์วัดเองไว้แล้ว: lateness ราว **85 ms** บนคู่เฟรมของ 2026-08-25 (ตั้ง delay 0.0 กับ 0.10 · ออกจริงห่าง **42 ms**) — **นี่คือที่มาของเลข 42 ms ที่ใบนี้อ้างข้างบน**
- ⇒ **คาดว่า realized gap รอบนี้ราว 1.41-1.44 วิ** · **หน้าต่างที่ยอมรับจึงเป็น 1.20-1.60 วิ** (ไม่ใช่ 1.40-1.60)
- 🔴 **ไม่มีอะไรในรีโปที่วัด realized gap ได้เลย — capture ของผู้เทสรอบนี้เท่านั้นที่วัดได้** ⇒ **ต้องอ่านออกมาเป็นตัวเลขระดับ ms แล้วรายงานเสมอ ไม่ว่าจะตรงคาดหรือไม่**
- 🔴 **ถ้า realized gap < 1.00 วิ ⇒ การ attribute ด้วยเวลาใช้ไม่ได้ ⇒ ชั้น (2) เป็น NO-RESULT ทั้งใบ** (ชั้น (1) ยังรายงานได้ตามปกติ) · **หน้าต่าง attribution 0.50 วิ ไม่เปลี่ยน**

### 🟢 สิ่งที่ **ไม่ใช่** คำถามที่เปิดอยู่แล้ว — ชั้น wire และชั้น dispatcher
- `tools/pf_ground_loot_nameprop_headless_replay.py` — **ทุก guard ในเครื่องมือผ่าน dispatcher ตัวจริง บนสำเนา DB ที่ทิ้งได้** (🔴 **ใบนี้จงใจไม่พิมพ์จำนวน guard** เพราะเครื่องมือยังเขียนไม่จบและตัวเลขจะขยับ — **ถ้าเห็นตัวเลขที่ไหน ให้เชื่อเครื่องมือ ไม่ใช่ใบ**) · ตอนนี้ถูกขับโดย test module แบบ subprocess ⇒ **จำนวน guard เป็นเลขที่มีอะไรบางอย่างรันจริง ไม่ใช่เลขที่เขียนไว้เฉย ๆ**
- สิ่งที่มันพิสูจน์: ① **hand-walker อิสระ** เดินไบต์เอง แล้ว **อ่าน gate byte และ index byte กลับออกมาจากเฟรมทดลองที่ dispatch จริง** ② **เฟรมคุมกับเฟรมทดลองมี payload dword ตรงกันทุกบิต และพิกัดตรงกันทุกบิต ต่างกันเฉพาะ element key · ไบต์มาสก์ · และสองฟิลด์ selector เท่านั้น** ③ **เลน `HYP-PF-032` ไม่ยิงเลยสักเฟรม**
- ⇒ 🔴 **คำถามที่ยังเปิดจริงเหลือข้อเดียว: ไคลเอนต์ตัวจริงทำอะไรกับ mask `0x3A`** — นั่นคือเหตุผลทั้งหมดที่ใบนี้ต้องใช้คนหน้าจอ
- ⚠️ **หลักฐานชุดนี้เป็นชั้น wire/dispatcher ล้วน** — 🔴 **ห้ามใครยกไปตอบแทนชั้น (2) เด็ดขาด** headless replay ไม่มีไคลเอนต์อยู่ในนั้น (กฎสองชั้นของบ้านนี้ ไม่ยกเว้นให้ใบไหน)

### objective (claim เดียว)
**เมื่อ element เดียวกัน (payload dword เดียวกัน พิกัดเดียวกัน) ถูกส่งสองครั้งในเซสชันเดียว ครั้งแรกไม่มีฟิลด์ selector (mask `0x12`) ครั้งที่สองมี gate `+0x1B`=1 และ index `+0x1A`=6 (mask `0x3A`) — หน้าตาของป้ายชื่อไอเทมบนจอ "ต่างกัน" หรือ "เหมือนกัน"**
(ใบนี้วัด **"ต่าง/ไม่ต่าง" ระหว่างเฟรมคุมกับเฟรมทดลองในรอบเดียวกัน** เท่านั้น — **ไม่ตีความว่าสิ่งที่ต่างนั้นแปลว่าอะไร และไม่หาสาเหตุ**)

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว · ท่องก่อนบูต)
- **P1 [คำทำนาย]** ป้ายขึ้นทั้งสองครั้ง และ **หน้าตาต่างกันเห็นได้ด้วยตา** (สี/ขนาด/น้ำหนัก/สไตล์/การจัดวาง อย่างน้อยหนึ่งอย่าง) ⇒ selector เดินถึงป้ายจริง
- **P2 [คำทำนาย]** ป้ายขึ้นทั้งสองครั้ง **หน้าตาเหมือนกันทุกอย่าง** ⇒ **ผลลบที่สะอาด** — และ **ตัวคุมเป็นตัวพิสูจน์เองว่าท่อทั้งเส้นยังมีชีวิต** (นี่คือแถวที่ดีไซน์เก่าไม่มีวันได้)
- **P3 [คำทำนาย]** ป้ายขึ้นเฉพาะเฟรมคุม **เฟรมทดลองไม่ขึ้น** ⇒ **ไคลเอนต์ปฏิเสธ element ที่กว้างกว่า** — ได้คำตอบของคำถาม V43 มาฟรี ๆ ในรอบเดียวกัน
- **P4 [คำทำนาย]** ไม่ขึ้นทั้งสองครั้ง ⇒ **เซสชันล้มหรือเรื่องมุมกล้อง/เรขาคณิต — ทิ้งรอบ ไม่ใช่ผลลบเรื่อง selector**
- **P5 [คำทำนาย · ถ้าเกิดคือเรื่องใหญ่]** เฟรมคุมไม่ขึ้น แต่เฟรมทดลองขึ้น ⇒ **นอกความคาดหมายทั้งหมด รายงานเสียงดัง ห้ามกลบให้เรียบ**
- **P6 [คำทำนาย · ยกมาจากรอบ 1135]** ป้ายแต่ละอันอยู่ 0.2-0.4 วิ แล้วหายเอง · ~~หน่วงจากไบต์ออกสายราว 0.12 วิ~~ 🔴 **ครึ่งหลังถูกถอนโดย chief R166** — เป็นค่าข้ามสองนาฬิกาที่ไม่เคยจูน (ดู ERRATUM ในบล็อกที่มา) ⇒ **P6 ทำนายแค่ "อายุป้าย 0.2-0.4 วิ" ซึ่งวัดในนาฬิกาวิดีโอตัวเดียว ⇒ ยังยืนได้** · **ห้ามใช้ตัวเลขหน่วงเป็นคำทำนายหรือเป็นเกณฑ์จับคู่**
- **P7 [ตีความ]** ข้อความจะอ่านได้ว่า `Red leaves Hammer` ทั้งสองครั้ง (ไคลเอนต์หยิบชื่อจากตารางตัวเอง — RE-066/RE-060) · **ถ้าข้อความสองครั้งไม่เหมือนกัน = finding ใหญ่ จดใหญ่ ๆ แล้วรายงาน ห้ามกลบ**

### 🔴 ก่อนบูต — resolve commit เขียว (รันเครื่องมือ ไม่ใช่ก๊อป SHA)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` (detached HEAD ถูกแล้ว)
- **exit 3** + `BOOT_COMMIT: NONE` ⇒ ห้ามบูต จดว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · **exit 2** = พาธผิด/git ล้ม · บรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ จดลงผลเสมอ
- 🔴 **ห้ามเทียบ `BOOT_COMMIT` กับเลข commit ใด ๆ ด้วยตา** — resolver คืน **หัว branch ที่ gate ตัดสิน** ซึ่งมัก "เก่ากว่า" merge commit เสมอโดยดีไซน์ (บทเรียน R159/R161: merge commit ไม่มีไฟล์คำตัดสินของตัวเอง) ⇒ **ตัดสินด้วยเนื้อ (ข้อ 3-7) เท่านั้น**

**ยืนยันเจ็ดข้อกับ `<SHA>` ที่จะบูตจริง — ต้องครบทั้งเจ็ด · ใช้ single quote เท่านั้น (สะพานเป็น PowerShell 5.1) · ห้ามใช้ท่อแบบยูนิกซ์ (`| grep`, `awk` ไม่มีใน PATH)**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n 'ground-loot-nameprop-scenario' <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/ground_loot_nameprop_probe.json && echo SCENARIO_PRESENT
git grep -c 'ground_loot_nameprop_probe' <SHA> -- src/pirateforce_foundation/ground_loot_nameprop_hypothesis.py scenarios/ground_loot_nameprop_probe.json
git grep -n 'GROUND_LOOT_NAMEPROP_IDX6_ONCE' <SHA> -- src/pirateforce_foundation/ scenarios/
git grep -c 'payload_dword' <SHA> -- src/pirateforce_foundation/ground_loot_nameprop_hypothesis.py scenarios/ground_loot_nameprop_probe.json
git grep -c 'GROUND_LOOT_NAMEPROP_TREATMENT_MASK = 0x3A' <SHA> -- src/pirateforce_foundation/ground_loot_nameprop_hypothesis.py
```
🔴 **ทุกบรรทัดที่พิมพ์ออกมาขึ้นต้นด้วย `<SHA>:` เสมอ** เพราะเราใส่ rev ลงในคำสั่ง — หน้าตาจริงคือ `abc1234:scenarios/ground_loot_nameprop_probe.json:2` ไม่ใช่ `scenarios/...json:2`
1. ไฟล์คำตัดสินมี `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ (`success` = subset บน Actions ไม่ใช่ gate เต็ม)
2. เจอ **flag ใหม่** `--ground-loot-nameprop-scenario` ใน `app.py` — 🔴 **ห้ามใช้ `--help` เป็นหลักฐาน** (คืน 0 บรรทัด exit 0 ผ่านสะพาน · บทเรียนรอบใหญ่ #7 ข้อ 6)
3. เห็นคำว่า `SCENARIO_PRESENT`
4. **ต้องได้สองบรรทัด และต้อง >=1 ทั้งคู่** — `...ground_loot_nameprop_hypothesis.py:<n>` และ `...ground_loot_nameprop_probe.json:<n>` 🔴 **อ่านเลขรายไฟล์ ห้ามรวมเป็นผลบวก** (`json:4 / py:0` ก็บวกได้ 4 เหมือนกันแต่ผิด — บทเรียน R161-b) · เหตุที่ `.py` ต้องอยู่ในสโคป: **ไฟล์ scenario เป็น permission token ไม่ใช่แหล่งค่า** ค่าจริงที่ประกอบเป็นเฟรมอยู่ในโมดูล
5. **ด่านกันบูตผิดเลน** — เจอ label `GROUND_LOOT_NAMEPROP_IDX6_ONCE` ในซอร์ส (เลน `HYP-PF-032` ทุกเวอร์ชันไม่มีคำนี้)
6. **ตัวคุมเชิงบวก** ต้องพิมพ์ **สองบรรทัด** (ไฟล์ละหนึ่ง) 🔴 **ถ้าข้อนี้ไม่พิมพ์อะไรเลย ห้ามตีความว่า "commit ผิด"** — แปลว่า **คำสั่งไม่ได้รัน** (พิมพ์ผิด/quote เพี้ยน/ไม่ได้อยู่ในโฟลเดอร์ repo) หรือไม่มีเลนนี้ในต้นไม้เลย ⇒ **หยุด แปะสิ่งที่คอนโซลพิมพ์มาทั้งดุ้น ห้ามเดา**
7. **ด่านค่ามาสก์ของเฟรมทดลอง** ต้องพิมพ์ **หนึ่งบรรทัด** `<SHA>:src/pirateforce_foundation/ground_loot_nameprop_hypothesis.py:1` · ⚠️ ถ้า **ข้อ 6 พิมพ์สองบรรทัดแล้วแต่ข้อ 7 เงียบ** ⇒ **ไม่ใช่เหตุห้ามบูตโดยอัตโนมัติ** แปลว่าค่าคงที่ถูกเขียนคนละรูปแบบกับที่ใบคาด ⇒ **เปิดไฟล์ scenario อ่านค่ามาสก์ของเฟรมทดลองด้วยตาให้เห็นว่าเป็น `0x3A` แล้วจดความต่างลงผลเพื่อให้ chief แก้ใบ** (กฎ "เครื่องมือชนะใบเสมอ") · ถ้า **ทั้งข้อ 6 และ 7 เงียบ** ⇒ คำสั่งไม่ได้รัน ⇒ หยุด

**อ่านค่า pin จากไฟล์ scenario ของ commit ที่บูต — 🔴 ห้ามฝังตัวเลขจากความจำ · ค่าที่ใบเขียนไว้มีไว้ "เทียบว่าตรงไหม" ไม่ใช่ "ใช้แทนไฟล์"**
`scenarios/ground_loot_nameprop_probe.json` พินสองชุด **แยกกันคนละเฟรม**:
```
control_pc_size                     44
control_frame_size                  54
control_coordinate_bytes_masked     pc[30:34]+pc[35:39]+pc[40:44]
control_pc_template_sha256 / control_frame_template_sha256

treatment_pc_size                   48
treatment_frame_size                58
treatment_coordinate_bytes_masked   pc[32:36]+pc[37:41]+pc[42:46]
treatment_pc_template_sha256 / treatment_frame_template_sha256
```
🔴🔴 **สองเฟรมมี "ช่วงไบต์พิกัด" คนละช่วง** (mask `0x3A` เพิ่มสองฟิลด์ ⇒ ไบต์พิกัดเลื่อนไป 2) — **นี่คือจุดที่พลาดง่ายที่สุดตอนตรวจ sha ด้วยมือ** ⇒ ใช้ span ของ control กับเฟรม control และ span ของ treatment กับเฟรม treatment เท่านั้น **สลับกันเมื่อไร sha จะไม่ตรงทั้งที่ไบต์ถูก**

🔴🔴 **กฎตัดสินเมื่อ "ข้อความในใบ" กับ "ผลที่เครื่องมือพิมพ์" ขัดกัน:** **ผลที่เครื่องมือพิมพ์ชนะเสมอ** — ใบเป็นกระดาษที่เขียนล่วงหน้า เครื่องมืออ่านของจริง ณ วินาทีนั้น · เจ็ดข้อผ่านครบแต่ใบมีประโยคห้ามบูต ⇒ **บูตได้** แล้วจดความขัดแย้งลงผล · เจ็ดข้อไม่ผ่านแต่ใบบอกพร้อม ⇒ **ห้ามบูต**

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-069_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt069.sqlite3
```
- เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง** (canonical ไม่ถูกเปิดตลอดรอบ)
- เกณฑ์สำเนาแบบ GT-059/060/063: **row-diff ทุกตารางต่างได้เฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง** (`count(*) WHERE selected_character_id IS NOT NULL` — ห้ามนับแถวเปล่า) · จด `max(lease_generation)` ก่อน-หลัง · `lease_generation` ห้ามถอยหลัง
- ถ้าเปิด session 2: สำเนาใหม่ `state\run_gt069b.sqlite3` (ห้ามใช้ไฟล์เดิมซ้ำ)
- ตำแหน่งตัวละคร **รีเซ็ตกลับจุดเกิดทุกบูต** (สำเนา DB ใหม่ทุกครั้ง) — พิกัดของใบนี้อิง trigger จึงไม่พังเพราะเรื่องนี้

### server args (เป๊ะ — opt-in เท่านั้น · `production_allowed=false`)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt069.sqlite3 --ground-loot-nameprop-scenario scenarios\ground_loot_nameprop_probe.json --export-events
```
- 🟢🔴 **ด่านเชิงบวกที่คอนโซล — ใช้ทุกครั้งก่อนเปิด client:** หัวหน้าต่าง console ต้องขึ้น mode **`ground-loot-nameprop`**
  🔴 **ถ้าขึ้น `ground-loot-hypothesis` แปลว่าบูตผิดเลน (เลน `HYP-PF-032`) ⇒ ปิด server ทันที ห้ามเปิด client ห้ามอ่านจอเป็นผล**
- 🔴 **บูตเลนเดียว ห้ามรวมเลนอื่น** — สองเลน ground-loot เป็น mutually exclusive ตอนบูตอยู่แล้วโดยโค้ด และถึงจะรวมเลนตระกูลอื่นได้ตาม allow-list ก็ **ห้ามทำในใบนี้**: ใบนี้ตัดสินด้วยตาบนหน้าตาของป้าย มีเลนอื่นวิ่งด้วยเมื่อไรก็แยก "ใครวาดป้ายนั้น" ไม่ออก = NO-RESULT ทั้งรอบ
- `--export-events` ใส่เฉพาะเมื่อ `git grep -n 'export-events' <SHA> -- src/pirateforce_foundation/app.py` เจอจริง — ไม่เจอก็ตัดออกแล้วจดไว้ว่ารอบนี้ยึด `[G>]` labels + raw SENT hexdump เป็นหลักฐาน dispatch แทน (ท่า GT-059 R152)
- **ชื่อ event ที่จะเห็นบนคอนโซลถ้ามี `--export-events`:** dispatch คู่ = `hyp_pf_039_ground_loot_nameprop_pair_committed` · ปฏิเสธ/ไม่ตอบ = `ground_loot_nameprop_compose_refused_no_reply`
  ⚠️ **แต่ห้ามใช้ event เป็นเกณฑ์ผ่านเดี่ยว ๆ** — เซิร์ฟเวอร์ไม่ persist `state.events` (เกณฑ์ event ถูกตัดออกจาก GT-045 อย่างถาวรตั้งแต่ R127 เพราะสังเกตไม่ได้เชิงโครงสร้างในรัน attended) ⇒ **raw frame ที่ sha ตรง pin คือหลักฐานปฐมภูมิเสมอ · บรรทัด event เป็นตัวยืนยันรอง**
- **latch:** เลนนี้ยิงครั้งเดียวต่อ connection (`ground_loot_nameprop_sent`) — ปิด client ให้สวยจนถึงหน้าเลือกเซิร์ฟเวอร์แล้วเปิดใหม่ = รีอาร์มได้ (PLAYBOOK เครื่องมือ ข้อ 4) แต่ **ปิดไม่สวยเมื่อไร ต้องรีสตาร์ต server ก่อนเสมอ**

### 🔴 ไม่มี chat trigger — และนั่นแปลว่า "ห้ามพิมพ์อะไรเลยทั้งรอบ"
- เฟรมออกเองที่ `TargetPosVital` แรกหลัง runtime ack **ครั้งเดียวต่อ connection** ⇒ **ผู้เทสคือคนคุมจังหวะยิง**
- 🔴 ตัวอักษรตอนช่องแชตไม่โฟกัส = **hotkey** ⇒ ระหว่างรอบ **อย่าพิมพ์ตัวอักษรใด ๆ** · (บันทึกไว้เพื่อรอบหลัง: เลน sweep ตัวอื่นในโปรเจกต์ยิงด้วยแชต **printable ASCII 12 ตัวพอดี** สั้น/ยาวกว่านั้นถึงเซิร์ฟเวอร์แต่เงื่อนไขเงียบ ๆ ไม่ผ่าน ไม่มี error — ถ้ารอบไหนบูตรวมเลน อย่าพิมพ์แชต 12 ตัวโดยไม่ตั้งใจ)

### 🔴🔴 กล้อง ทิศหัน และการซูม — อ่านให้จบก่อนแตะเมาส์ (กฎกล้องฉบับ R163 + กฎ Z ของ R164)
| ท่า | ทำอะไรจริง | ยิง `TargetPosVital` ไหม | ใบนี้ |
|---|---|---|---|
| **คลิกขวาค้างลากเมาส์** | หมุน **มุมกล้อง** อย่างเดียว · ทิศหันของตัวละครไม่ขยับ | 🟢 **ไม่ยิง** | ✅ ใช้ได้เต็มที่ **รวมถึงก่อนทริกเกอร์** |
| **`Q` / `E`** | **หันตัวละคร** กล้องแพนตาม | 🔴 **ยิง** | ❌ **ห้ามแตะก่อนทริกเกอร์** |
| **`W/A/S/D`** | เดิน (เปลี่ยนทั้งตำแหน่งและทิศหัน) | 🔴 **ยิง** | ❌ ใช้เป็น **ตัวยิง** ที่ข้อ 6 เท่านั้น |
🔴 **ประโยคเดียวที่ต้องจำ: ตัวที่ยิง `TargetPosVital` คือ "การเปลี่ยนทิศหันของตัวละคร" ไม่ใช่ "การขยับกล้อง"** · **liveness check ของใบนี้ = คลิกขวาลากแล้วกล้องหมุน — ห้ามใช้ `Q/E` เช็ค NO-CRASH** (มันยิงไบต์ออกสาย)
🔴 **กฎ Z (บังคับ · เป้าเป็น player-relative +30):** ต้องมีขั้น "ซูมกล้องออกก่อนยิงทริกเกอร์" เป็นขั้นที่มีหมายเลขของตัวเอง (ข้อ 5) · **เกณฑ์ของใบนี้: จุด +30 อยู่ในเฟรม *และ* ตัวอักษรใหญ่พอจะอ่านออก** — เป้าเหลือจุดเดียวแล้ว แต่ **แรงดึงสวนทางยังจริง**: ซูมออกมากไป = ตัวอักษรเล็กจนอ่านหน้าตาจากภาพนิ่งไม่ได้ ⇒ ลองมุม/ระดับซูมให้พอใจตั้งแต่ก่อนยิง (คลิกขวาลาก + ล้อ ทำได้ปลอดภัย) · **จดระดับซูมและเวลาที่ซูมทุกครั้ง**
🔴 **nonclaim ที่ต้องพกไป: ไม่มีใครเคยวัดว่าล้อเมาส์ยิง `TargetPosVital` หรือไม่** ⇒ ถ้าเฟรมออกตอนหมุนล้อ **รอบไม่เสีย ถ้ากล้องกำลังอัดอยู่และหันไปทาง +X แล้ว** (พิกัดอิง trigger เสมอ) — แต่ **ต้องจดลงผลว่าเฟรมออกที่จังหวะนั้น**

### steps
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบตามบล็อก db ·
**เตรียม teardown:** ก๊อปจาก **`TEMPLATE_teardown_generic.ps1`** เป็นหลัก · ถ้าก๊อปจากจ็อบที่เป็นตัวเลข **ต้องเปิดดูบรรทัดที่ 17 ให้เห็น `-replace '\\','/'` ก่อนเสมอ** · 🔴 **ห้ามก๊อปจาก `1103`/`1105`**
1. **เปิด server ก่อน client เสมอ** (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client) — **ยืนยันว่าคอนโซลขึ้น mode `ground-loot-nameprop`** (ถ้าเป็น `ground-loot-hypothesis` = บูตผิดเลน หยุด) · (🔴 client ที่บูตโดยไม่มีเซิร์ฟเวอร์ **ตายเองใน ~3.5 นาที**) · 🔴 **ถ้าต้องฆ่า client กลางคัน ให้รีสตาร์ต server ก่อนเปิด client ใหม่เสมอ** (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่ "connecting" ตลอดกาล)
2. เปิด client (`Invoke-CimMethod Win32_Process Create`) → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร → **เลือกตัวละครช่องแรก** (เลนตระกูลนี้พิน identity ไว้ที่ช่องแรก — เลือกผิดช่อง เลนอาจปฏิเสธเงียบผ่าน `ground_loot_nameprop_compose_refused_no_reply`) → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
3. **เริ่มอัดวิดีโอต่อเนื่องตั้งแต่ก่อนเข้าแมพเสร็จ** ลง `evidence_video\` ยาวจนจบ session — 🔴 **ไม่ได้อัด = NO-RESULT ทันที** (ป้ายอยู่ 0.2-0.4 วิ ตามเก็บย้อนหลังไม่ได้) · **จดบรรทัด `VIDEO START pid=... start=... fps=30` จากล็อกจ็อบบูตวิดีโอไว้** — นี่คือสมอเวลาสัมบูรณ์ที่ใช้ crosswalk ทั้งรอบ
4. เข้าแมพ เห็น HP/minimap/ชื่อแมพ → 🔴 **ห้ามแตะ `W/A/S/D` และ `Q/E`** → **หันมุมกล้องด้วยคลิกขวาค้างลากเมาส์** ให้มองไปทาง **+X** และให้แนวสายตาโล่งถึงจุด +30 (ยกกล้องสูงขึ้นเล็กน้อยกันตัวละครเราเองบังจุดนั้น — บทเรียน adversary R158) → ถ่าย **G0** ให้เห็น X/Y บน HUD และพื้นที่รอบตัว
5. **ซูมออก (ขั้นบังคับ กฎ Z):** หมุนล้อเมาส์ปรับจนเห็นจุด +30 ในเฟรม **และตัวอักษรยังใหญ่พออ่านออก** → ถ่าย **G0b** → **จดเวลาที่ซูม**
6. **จังหวะยิง (หัวใจของใบ):**
   ① ยืนยันว่ากำลังอัดอยู่ และกล้องนิ่งแล้ว (หลังจากนี้ **อย่าขยับกล้องอีกจนพ้นวินาทีที่ 5** — 🔴 **กล้องต้องเป็นมุมเดียวกันเป๊ะทั้งสองแฟลช ไม่งั้นตัวคุมกับตัวทดลองไม่ได้ถูกดูด้วยพิกเซลชุดเดียวกัน ซึ่งเป็นหัวใจของดีไซน์**)
   ② **กด `W` สั้นที่สุด (~120 ms) หนึ่งครั้ง** — trigger ออกที่การขยับครั้งนี้ · **แล้วปล่อยมือ ยืนนิ่ง ห้ามขยับอะไรอีก**
   ③ **ตาอยู่ที่จอตลอด 5 วินาที** — จะเห็น **สองแฟลชที่จุดเดียวกัน ห่างกันราว 1.4-1.5 วิ** แต่ละอันอยู่ 0.2-0.4 วิ 🔴 **แฟลชแรก = เฟรมคุม · แฟลชที่สอง = เฟรมทดลอง (แยกด้วยลำดับ ไม่ใช่ด้วยเวลาสัมบูรณ์ — แก้โดย chief R166)** · *(ถ้อยคำเดิม "คุมที่ ~+0.12 วิ · ทดลองที่ ~+1.5 วิ" ถูกถอน — ดูข้อ ก. ของบล็อกหลักฐานภาพ)* 🔴 **อย่าพยายามถ่ายภาพนิ่งให้ทันแฟลช** — วิดีโอคือกรรมการ ภาพนิ่งมาจากการแตกเฟรมทีหลัง (PLAYBOOK ข้อ 11)
   ④ พูดออกเสียง/จดทันทีหลังจบ: **เห็นกี่แฟลช · แฟลชแรกหน้าตาอย่างไร · แฟลชที่สองหน้าตาอย่างไร · ต่างกันตรงไหนบ้าง (สี/ขนาด/ความหนา/สไตล์/ตำแหน่ง) · อ่านข้อความออกไหม** (ความจำสด ๆ มีค่า แต่ **คำตัดสินต้องมาจากภาพนิ่ง full-res เท่านั้น**)
   ⑤ **อัดต่อเนื่องอย่างน้อย 5 วินาทีหลังกด** แล้วยืนนิ่งดูพื้นอีก 3 วินาที
7. **ข้อสังเกตแถม (ไม่ใช่ผลของใบ · จดแยกช่อง):** มีฝุ่นสีน้ำตาลขึ้นไหม กี่ครั้ง · มีอะไรค้างบนพื้นหลังแฟลชหายไหม — 🔴 **ห้ามใช้ข้อนี้ตอบคำถามหลักของใบ และห้ามใช้เวลารอบไปตามหาโมเดล** (GT-045 ตอบเรื่องโมเดลไปแล้ว)
8. **SESSION 2 (แนะนำ ไม่บังคับ · ทำได้เมื่อเวลาเหลือ):** ออกจากเกมให้สวยจนถึงหน้าเลือกเซิร์ฟเวอร์ → **ปิด server ด้วยเสมอ** → copy DB ใหม่ (`run_gt069b.sqlite3`) → บูต server (args เดิม เปลี่ยน `--db`) → **ยืนยัน mode `ground-loot-nameprop` อีกครั้ง** → ทำข้อ 2-7 ซ้ำ · 🔴 **หลักฐานของสอง session แยกกันเด็ดขาด ห้ามรวมภาพ/ห้ามรวมคำตัดสิน** · **สูงสุด 2 sessions**
9. **NO-CRASH / CRASH:** **คลิกขวาค้างลากเมาส์แล้วกล้องหมุน = NO-CRASH** · หลุด/ค้าง = CRASH + จดว่าหลังเฟรมไหน
10. ออกจากเกม: **X** มุมขวาบน (ตรวจก่อนว่าหน้าต่างแอปตัวเองไม่บังปุ่ม X) → dialog ยืนยัน → ปุ่มซ้าย → **ปิด server ด้วย**
11. เก็บ **raw GAME log ทั้งไฟล์** (`...\capture_v141\GAME_LIVE.txt`) + console out/err ทั้งหมด (รวมทุกบรรทัด `[G>]` / `PF-EVENT` / `ErrorData`) → `PRAGMA integrity_check;` บนสำเนาทุกใบ
12. **teardown เสมอ** แม้เลิกกลางคัน/แม้รอบจบเพราะคนเลิกเล่น (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 — เพดานยกจาก 180 เมื่อ 2026-08-20 · `TEMPLATE_teardown_generic.ps1:135` · แท่นที่ถูกทิ้งข้ามชั่วโมงใช้ `staged\TOOL_stop_stale_server.ps1`) · ถ้าได้ exit 36 อีก **อย่าเดาเอง** แนบบรรทัดที่ 17 ของไฟล์ teardown ที่ใช้จริงมาทั้งบรรทัด
13. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม
14. **หลังรอบ — แตกเฟรมและอ่านหน้าตาป้าย (ทำตามบล็อกหลักฐานภาพข้างล่าง ห้ามข้าม)**

### 🔴 หลักฐานภาพ — ท่าเดียวกับที่หน้าสะพานทำในจ็อบ 1135 แล้วได้ผล (จดหมาย `20260825_1615` §① คือเทมเพลตของบล็อกนี้)
**ก. crosswalk เวลา (ทำก่อนแตะ ffmpeg):**
`t_ในวิดีโอ = เวลานาฬิกา - เวลาใน VIDEO START` · อ่าน `SENT GROUND_LOOT_NAMEPROP_CONTROL_ONCE` และ `..._IDX6_ONCE` จาก `GAME_LIVE.txt` ⇒ ได้ **`t_A`** (คุม) และ **`t_B`** (ทดลอง)
🔴🔴 **แก้โดย chief R166 หลัง `pf-adversary` — บรรทัดนี้เคยเขียนว่า "คาดว่าป้ายโผล่ราว `t + 0.12`" และนั่นทำให้ใบตอบกลับหัวได้**
`t_A`/`t_B` เป็นค่า **ข้ามสองนาฬิกาที่ยังไม่จูน** · ถ้า offset ของบูตนั้นอยู่ราว `1.8 วิ` (ค่าที่เกิดขึ้นจริงแล้วในจ็อบ 1151) มันจะ **เกินครึ่งของระยะห่าง `1.50 วิ` ที่ใบตั้งไว้** ⇒ เฟรมของ *เฟรมทดลอง* ไปตกใกล้เวลาคาดของ *เฟรมคุม* ⇒ **สลับป้ายคุมกับป้ายทดลอง ซึ่งเป็นตัวแปรเดียวของทั้งใบ** ⇒ **ใบให้คำตอบกลับหัวโดยที่ทุกด่าน wire ยังเขียว (sha ตรง pin ทุกเฟรม)**
🔴 **กติกาตัดสินที่ต้องใช้แทน — ปลอดภัยโดยไม่ต้องมี clapper เลย:**
**ตัดสินด้วย *ลำดับ* ของสองแฟลชในนาฬิกาวิดีโอตัวเดียว** — แฟลชแรกที่ปรากฏคือของเฟรมคุม แฟลชที่สองคือของเฟรมทดลอง เพราะเราเป็นคนกำหนดลำดับส่งเอง และระยะห่างระหว่างสองแฟลช (~`1.4-1.5 วิ`) วัดได้ **ภายในไฟล์วิดีโอไฟล์เดียว** ⇒ `offset` ตัดกันทางพีชคณิต
⇒ **ใช้ `t_A`/`t_B` เพื่อ *เล็งหน้าต่างที่จะแตกเฟรม* เท่านั้น ห้ามใช้เพื่อ *ระบุว่าแฟลชไหนเป็นของเฟรมไหน*** · และให้แตกเฟรมด้วยหน้าต่างที่กว้างพอรับ offset ที่ไม่รู้ค่า (ดูข้อ ข.)
🔴 **ถ้าสองแฟลชแยกจากกันไม่ได้ในวิดีโอ (เห็นแฟลชเดียว หรือเรียงลำดับไม่ได้) ⇒ `NO-RESULT` ห้ามเดาจากตัวเลขเวลา**
**ข. แตกเฟรมช่วงหน้าต่าง (ห้ามมี `scale=` ในบรรทัดคำสั่งเด็ดขาด):**
```
$mkv = '<path เต็มของไฟล์ FULLROUND .mkv>'
ffmpeg -ss <t_A - 2.50> -i $mkv -t 5.00 -vsync 0 GT069_A_%03d.png
ffmpeg -ss <t_B - 2.50> -i $mkv -t 5.00 -vsync 0 GT069_B_%03d.png
```
🔴 **หน้าต่างถูกขยายจาก `1.20 วิ` เป็น `5.00 วิ` (คร่อม `-2.50`) โดย chief R166** — หน้าต่างเดิมแคบกว่า offset ที่ไม่รู้ค่า ⇒ **แตกเฟรมแล้วอาจไม่มีแฟลชอยู่ในนั้นเลย แล้วอ่านเป็น "ป้ายไม่ขึ้น"**
🔴 **หน้าต่าง A กับ B จะซ้อนกัน (ห่างกันแค่ 1.5 วิ แต่กว้าง 5 วิ) — นั่นคือความตั้งใจ** · การแยกว่าแฟลชไหนเป็นของใครทำด้วย **ลำดับ** ตามข้อ ก. **ไม่ใช่ด้วยว่ามันอยู่ในโฟลเดอร์ A หรือ B**
**ค. เลือกเฟรมที่ป้ายชัดที่สุดของแต่ละแฟลช แล้วดึงเป็นภาพนิ่ง full-res จากต้นฉบับโดยตรง (ไม่ย่อ ไม่ crop):**
```
ffmpeg -ss <t ที่เลือก> -i $mkv -frames:v 1 -q:v 2 -y GT069_<job>_NAMEPROP_A_CONTROL_FULLRES_t<t>s.jpg
```
**ง. ครอปสำหรับอ่านหน้าตา — PNG ไม่สูญเสีย ตัดจากต้นฉบับ ห้ามย่อ:**
```
ffmpeg -ss <t ที่เลือก> -i $mkv -frames:v 1 -vf 'crop=<W>:<H>:<X>:<Y>' -c:v png -y GT069_<job>_NAMEPROP_A_CONTROL_CROP_t<t>s.png
```
🔴 **ใช้ค่ากรอบ crop เดียวกันเป๊ะทั้ง A และ B** (ป้ายอยู่พิกัดโลกเดียวกันและกล้องไม่ขยับ) — **นี่คือสิ่งที่ทำให้เทียบสองภาพได้ตรง ๆ** · จ็อบ 1135 ใช้ `crop=420:120:1000:400` ได้ผล แต่ **ค่ารอบนี้ขึ้นกับมุมกล้อง ให้หาเองจากภาพเต็มแล้วจดค่าลงผล**
**จ. ตัวควบคุมภาพ (บังคับ อย่างน้อยหนึ่งใบ):** ภาพนิ่ง full-res ที่ **กล้องมุมเดิมแต่ป้ายหายแล้ว** — ที่ดีที่สุดคือช่วง **ระหว่างสองแฟลช** (`t_A + 0.8` วิ โดยประมาณ) เพราะพิสูจน์พร้อมกันสองอย่าง: ป้ายไม่ใช่ฉากถาวร **และ** แฟลชที่สองเป็นคนละเหตุการณ์กับแฟลชแรก · ตั้งชื่อ `..._CONTROL_GONE_t<t>s.jpg`
**ฉ. commit เข้า `evidence_screens\` พร้อม sha256 ทุกไฟล์** · 🔴 **ห้ามลบไฟล์ `.mkv` ต้นฉบับบนสะพาน**
**ช. เรื่องขนาดไฟล์ — แก้ความขัดแย้งไว้ตรงนี้ อย่าไปตัดสินใจเองหน้างาน:** กฎ 2026-08-24 (`JPEG กว้าง <=1280 px`) **ใช้กับใบนี้ไม่ได้กับภาพที่จะอ่านหน้าตาป้าย** เพราะ PLAYBOOK ข้อ 13 ห้ามอ่านสีจากภาพย่อ ⇒ **ภาพชี้ขาดของใบนี้ต้องเป็น full-res เต็มเฟรม (1920x1080) ไม่ย่อ** · จ็อบ 1135 พิสูจน์แล้วว่าทำได้จริงและยังเล็ก: JPEG เต็มเฟรม **363,898 B** และ PNG crop **70,265 B** ⇒ ไม่ชนเพดานอยู่แล้ว · ถ้าใบไหนเกิน 2 MB ให้ **crop จากต้นฉบับ ห้าม resize ลง**

### ⭐ PLAYBOOK ข้อ 13 — บันทึกสีของ **ทุกป้ายชื่อในเฟรม** (คำสั่งคุณ Panya 2026-08-25 ~14:2x +07:00 · บังคับกับทุกใบ attended)
- **หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** — ป้ายชื่อไอเทมบนพื้น · ชื่อตัวละครเราเอง (เหนือหัว + แผง UI ซ้ายบน) · ชื่อ actor/NPC ทุกตัวในเฟรม · ชื่อบนแผง target · ชื่อผู้เล่นคนอื่น · บรรทัด title/คำอธิบาย
- **ไม่มีให้เขียนคำว่า "ไม่มี" ออกมาเป็นตัวอักษร** 🔴 **ห้ามเว้นว่าง**
- **อ่านสีจากภาพนิ่งความละเอียดเต็ม/ครอป PNG เท่านั้น** 🔴 **ห้ามอ่านจาก contact sheet · ห้ามอ่านจากภาพย่อ · ห้ามอ่านจากวิดีโอ** (บทเรียน GT-045: ย่อเหลือ 400px ป้ายเหลือจุดเดียว หาเฟรมไม่เจอสามรอบ · การบีบอัดวิดีโอเปลี่ยนสีได้)
- **จดที่ไหน:** (ก) ในช่อง `result` ของใบนี้ พร้อม path ภาพ + sha256 (ข) **ส่งค่าที่ต้องเติม `REAL_SERVER_DIVERGENCE.tsv` กลับมาในจดหมายผล — 🔴 อย่าแก้ไฟล์นั้นเองจากหน้าสะพาน** (ไฟล์อยู่นอก allowlist ของ `pf_git_sync.ps1` ⇒ แก้แล้วจะกลายเป็น tracked file ที่ dirty แล้วบล็อก rebase — บทเรียน `20260825_1615` §③) · แถวที่ใบนี้แตะคือ `ground-loot / ป้ายชื่อไอเทมบนพื้น` (แถวนั้นชี้มาที่ `GT-069` ถูกต้องแล้วตั้งแต่ R165) · คอลัมน์ `compared_and_matched` = `yes`/`no`/`no-reference` ตามจริง · `evidence_layer=eye` · `evidence_sha256` บังคับเมื่อ `evidence_in_repo=yes` · `open_ticket=RE-067` · `blocks_promotion=no`
- 🔴🔴 **ผู้เทสจด "สิ่งที่เห็น" เท่านั้น ห้ามสรุปสาเหตุ** — ไม่มีใครรู้ว่าอะไรตัดสินหน้าตาของป้าย ครึ่ง actor ของ `RE-067` ปิดแบบ **bounded negative** และเปิดต่อเป็น **`RE-068` ซึ่งยังเปิดอยู่** ⇒ ห้ามเขียนว่า "แปลว่าไคลเอนต์จัดมันเป็นผู้เล่น/NPC/ศัตรู" · **ห้ามจับคู่ `0x5D..0x62` กับ `FONT_COLOR.n_ID 1..57` เพราะเลขดูคล้ายกัน — ไม่มี crosswalk จริง**

### pass criteria — สองชั้น แยกกันเด็ดขาด
**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ · ทำ headless ได้)**
- `GAME_LIVE.txt` ต่อหนึ่ง session มี **สองเฟรม** เรียง `GROUND_LOOT_NAMEPROP_CONTROL_ONCE` -> `GROUND_LOOT_NAMEPROP_IDX6_ONCE` **อย่างละหนึ่งครั้ง** (latch `ground_loot_nameprop_sent` เป็น one-shot ต่อ connection — เห็นมากกว่านี้ = จดแล้วรายงาน)
- **masked template sha256 ตรง pin ทั้งสี่ค่า** (`control_pc` · `control_frame` · `treatment_pc` · `treatment_frame`) ที่อ่านจาก `scenarios/ground_loot_nameprop_probe.json` ของ commit ที่บูต · 🔴 **ใช้ span พิกัดคนละชุดกับคนละเฟรมตามที่เตือนไว้ข้างบน** · เก็บ hexdump ทั้งไฟล์ **ห้ามลบ**
- 🔴🔴 **ด่านความยาวไบต์ (กลับด้านจากฉบับก่อน — อ่านให้ครบ):**
  - **เฟรม A ต้องเป็น pc 44 / frame 54** — **มันคือตัวคุม ทรงเก่าโดยตั้งใจ ไม่ใช่ความผิดพลาด**
  - **เฟรม B ต้องเป็น pc 48 / frame 58**
  - **ถ้าทั้งสองเฟรมเป็น 54 ⇒ ตัวทดลองไม่เคยพา selector ออกไปเลย ⇒ NO-RESULT ห้ามอ่านจอเป็นผลใด ๆ**
  - **ถ้าสองเฟรมยาวเท่ากันไม่ว่าค่าใด ⇒ มีอะไรผิด หยุดแล้วรายงาน**
- **hexdump ต้องเห็น:** ไบต์มาสก์ของเฟรม A อ่านได้ **`12`** · ของเฟรม B อ่านได้ **`3A`** · ไบต์ payload dword **`67 93 21 00`** (= `2200423`) **เหมือนกันทั้งสองเฟรม** · **ไบต์พิกัดเหมือนกันทั้งสองเฟรม** · 🔴 **ถ้าไบต์กับ sha ขัดกัน ให้เชื่อ sha แล้วหยุดรายงาน**
- **realized gap** อ่านเป็นตัวเลขระดับ ms จาก timestamp ของสองบรรทัด SENT — ยอมรับ **1.20-1.60 วิ** · **< 1.00 วิ ⇒ ชั้น (2) เป็น NO-RESULT** · 🔴 **รายงานค่าที่วัดได้เสมอ ไม่มีอะไรในรีโปวัดค่านี้แทนได้**
- **เกณฑ์พิกัด:** decode f32 ของทั้งสองเฟรมแล้วต้องได้ **x = trigger+30 · Y/Z = ของ trigger เป๊ะ ทั้งคู่** โดย trigger อ่านจากเฟรม `TargetPosVital` บรรทัดก่อน `SENT ..._CONTROL_ONCE` ใน raw log 🔴 **ห้ามใช้ HUD หรือ "X ตอนเข้าแมพ" เป็นฐานคำนวณ**
- **ไม่มีบรรทัด `ErrorData=28317`** ในคอนโซล/ล็อก — **ถ้ามี ให้จดว่ามันโผล่หลังเฟรมไหน** แล้วอ่านคู่กับตารางผล (แถว N3/N7) เก็บคอนโซลทั้งไฟล์
- ตัวยืนยัน dispatch: บรรทัด `PF-EVENT` `hyp_pf_039_ground_loot_nameprop_pair_committed` (ถ้าบูตด้วย `--export-events`) หรือ `[G>]` action labels + raw SENT hexdump ตรง pin — **raw frame ตรง pin คือหลักฐานปฐมภูมิเสมอ · ห้ามใช้ event เดี่ยว ๆ เป็นเกณฑ์ผ่าน** · ถ้าไม่ออกเลย ให้มองหา `ground_loot_nameprop_compose_refused_no_reply` แล้วเก็บทั้งบรรทัด (เป็นผลเหมือนกัน)
- DB สำเนา: `PRAGMA integrity_check` = `ok` · row-diff ทุกตารางต่างเฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง · `max(lease_generation)` ก่อน-หลังจดไว้ ไม่ถอยหลัง · sha256 canonical ก่อน-หลังตรงกัน · canonical ไม่ถูกเปิดตลอดรอบ
- **ชั้นนี้ตอบไม่ได้:** จอวาดป้ายหน้าตาอย่างไร (เฟรมออก != ไคลเอนต์รับ/วาด) ⇒ 🔴 **ห้ามอ้างชั้นนี้แทนชั้น (2)** · 🔴 **และห้ามอ้าง guards ของ headless replay แทนชั้น (2) เช่นกัน — dispatcher ไม่ใช่ไคลเอนต์**

**ชั้น (2) client-observable (ต้องมีคนหน้าจอ — ตัวปิดใบอยู่ชั้นนี้ชั้นเดียว)**
- หลักฐานบังคับ: **วิดีโอต่อเนื่องคลุมตั้งแต่ก่อนกด `W` ถึง +5 วิ** · ภาพ **G0 / G0b** · **A_CONTROL_FULLRES + A_CONTROL_CROP** · **B_IDX6_FULLRES + B_IDX6_CROP** · **CONTROL_GONE** อย่างน้อยหนึ่งใบ · **sha256 ทุกไฟล์** · **ค่ากรอบ crop ต้องเป็นค่าเดียวกันระหว่าง A กับ B**
- 🔴🔴 **การ attribute ต้องทำ "ด้วยเวลา" เท่านั้น:**
  - แฟลชนับเป็น **ของเฟรมคุม (A)** เมื่อเฟรมแรกที่ป้ายปรากฏอยู่ในช่วง **`[t_A, t_A + 0.50]`**
  - แฟลชนับเป็น **ของเฟรมทดลอง (B)** เมื่อเฟรมแรกที่ป้ายปรากฏอยู่ในช่วง **`[t_B, t_B + 0.50]`**
  - แฟลชที่วางลงไทม์ไลน์ไม่ได้ หรือคร่อมขอบ ⇒ **NO-RESULT ของ element นั้น จดตรง ๆ ห้ามแต่งผล**
  - 🔴 **ห้ามใช้ตำแหน่งบนจอเป็นตัวตัดสินว่าแฟลชไหนคือเฟรมไหน** — รอบนี้ทั้งสองอยู่ **จุดเดียวกัน** ⇒ **เวลาเป็นตัวแยกอย่างเดียวที่มี** (บทเรียน 1135: สอง element ห่าง 42 ms แล้วผู้สังเกตแยกไม่ออก)
- **ตอบเป็นตารางต่อแฟลช:** `t` ที่ป้ายโผล่ / `t` ที่ป้ายหาย / อายุ (วิ) / **ข้อความที่อ่านออกทั้งบรรทัด** / **หน้าตาเป็นภาษาคน: สี · ขนาด · ความหนา · สไตล์ (เอียง/ขอบ/เงา) · การจัดวาง** — 🔴 **บันทึกทุกมิติที่เห็น ไม่ใช่เฉพาะสี** (สิ่งที่ `RE-067` พินคือ text property ซึ่งอาจไม่ใช่สีเลย)
- **คำตัดสินของใบ = เทียบ CROP ของ A กับ CROP ของ B แบบวางข้างกัน** ⇒ **"ต่าง" หรือ "เหมือน"** และถ้าต่าง **ต่างตรงไหนบ้าง** · *(ภาพ `evidence_screens\GT045v3r4_1135_NAMELABEL_CROP_t249.833s.png` sha `18e357ec...` ใช้เป็นตัวเทียบข้ามรอบได้ **แต่ไม่ใช่ตัวตัดสิน** — ตัวตัดสินคือคู่ A/B ในรอบเดียวกันนี้เท่านั้น)*
- **ตาราง PLAYBOOK ข้อ 13 ครบทุกป้ายทุกภาพ** (ดูบล็อกข้างบน) — ขาดตารางนี้ = หลักฐานไม่ครบ
- **NO-CRASH / CRASH verdict ชัดเจน** (ตัดสินด้วยคลิกขวาลาก)
- **ชั้นนี้ตอบไม่ได้:** เฟรมออกจากเซิร์ฟเวอร์จริงไหม ไบต์ตรง pin ไหม 🔴 **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

### ตารางผลลัพธ์ที่มีชื่อ — **ทุกทางออกอ่านได้ นี่คือสิ่งที่ดีไซน์ควบคุมซื้อมาให้**
| # | สิ่งที่เห็น | คำตัดสินของใบ | อนุญาตให้สรุปว่า | 🔴 **ไม่** อนุญาตให้สรุปว่า / redirect |
|---|---|---|---|---|
| **N1** BOTH-DIFFERENT | ป้ายขึ้นทั้งสองแฟลช **หน้าตาต่างกัน** | ✅ **ปิดใบ — ผลบวกที่สะอาด** | **สองฟิลด์ selector (gate `+0x1B` + index `+0x1A`) เดินถึงป้ายจริง** — ตัวแปรเดียวที่ต่างคือฟิลด์สองตัวนั้น | ❌ ห้ามบอกว่า `0x34`/`0x62` "แปลว่าอะไร" (สี? ฟอนต์? ขนาด? พรีเซ็ต? — ยังไม่รู้) · ❌ ห้ามผูกกับ `FONT_COLOR.n_ID` · ❌ ห้ามอ้างถึงป้ายชื่อ actor (นั่นคือ `RE-068`) |
| **N2** BOTH-SAME | ป้ายขึ้นทั้งสองแฟลช **หน้าตาเหมือนกันทุกมิติ** | 🔴 **ผลลบที่สะอาด · มีค่าเท่าผลบวก · ไม่ใช่ FAIL** — **ตัวคุมพิสูจน์เองว่าท่อทั้งเส้นมีชีวิตในวินาทีนั้น** | ว่า **"ส่ง gate+index ใต้ mask `0x3A` แล้วหน้าตาป้ายไม่เปลี่ยนใน runtime นี้"** | ❌ ห้ามสรุปว่า `RE-067` ผิด · 🔴🔴 **ห้ามลืมความเป็นไปได้ที่ผลลบนี้ถูกด้วยเหตุผลผิด: ไม่เคยมีใครเชื่อม CREATE path ที่ `RE-067` พินในไบนารี เข้ากับ "ป้ายลอยที่ผู้สังเกตเห็น" เลย** — ถ้าป้ายที่เห็นเป็น widget คนละตัว การตั้ง `+0x1B`/`+0x1A` ก็ไม่มีวันเปลี่ยนอะไร และผลลบนี้จะ **ถูกในเชิงผล แต่ผิดในเชิงเหตุ** ⇒ redirect: ใบ static ที่ผูก selector กับ widget ที่วาดจริง **ก่อน** จะไปกวาด index อื่น |
| **N3** CONTROL-ONLY | ป้ายขึ้นเฉพาะแฟลชคุม **แฟลชทดลองไม่ขึ้น** | ✅ **ผลที่มีชื่อและมีค่าสูง — ได้คำตอบของคำถาม V43 มาฟรีในรอบเดียวกัน** | ว่า **ไคลเอนต์ปฏิเสธ/ทิ้ง element ที่กว้างกว่า (mask `0x3A`)** — และตัวคุมพิสูจน์ว่าไม่ใช่เรื่องกล้อง/เรขาคณิต | ❌ ห้ามสรุปเรื่องหน้าตา/สีใด ๆ · ❌ ห้ามชี้ว่าฟิลด์ไหนทำให้ถูกปฏิเสธ (มาสก์พาสองฟิลด์มาพร้อมกัน) · แนบว่ามี `ErrorData=28317` หรือไม่ · redirect: ลดมาสก์ทีละบิต (gate อย่างเดียว = `0x1A`) เป็นเวอร์ชันถัดไป — **แตะ wire ⇒ กลับไปที่เงื่อนไข (1) เจ้าของต้องเคาะก่อน** |
| **N4** NEITHER | ไม่ขึ้นทั้งสองแฟลช | 🔴 **ทิ้งรอบ (เซสชันล้ม/เรื่องเรขาคณิต) — 🔴 ไม่ใช่ผลลบเรื่อง selector เด็ดขาด** | ไม่มี | ❌ ห้ามเขียนว่า "selector ไม่มีผล" · redirect: ตรวจ mode คอนโซล · เจ็ดข้อ · label ครบไหม · วิดีโอคลุมวินาที trigger จริงไหม · มุมกล้อง/ซูม แล้ว **รันซ้ำ commit เดิมได้เลย ไม่นับเป็นเวอร์ชันใหม่ ไม่ต้องขอใครใหม่** |
| **N5** TREATMENT-ONLY | แฟลชคุม**ไม่ขึ้น** แต่แฟลชทดลอง**ขึ้น** | 🟠 **นอกความคาดหมายทั้งหมด — finding ใหญ่** | ไม่มี (ยังไม่มีทฤษฎีที่ทำนายสิ่งนี้) | 🔴 **รายงานเสียงดัง ห้ามกลบให้เรียบ ห้ามเขียนว่า "คงเป็นเรื่องบังเอิญ"** · แนบวิดีโอช่วง `[t_A - 0.5, t_B + 1.0]` ทั้งช่วง + hexdump ทั้งสองเฟรม แล้วส่งให้ chief ตัดสิน |
| **N6** NON-OBSERVED | ป้ายอยู่นอกเฟรม / ถูกบัง / ตัวอักษรเล็กจนอ่านหน้าตาไม่ได้ / crosswalk คร่อมขอบ / กล้องขยับกลางคัน | 🔴 **NO-RESULT — ไม่ใช่ผลลบเด็ดขาด** | ไม่มี | ❌ 🔴 **"ป้ายไม่ขึ้น" ของแฟลชใดแฟลชหนึ่งเดี่ยว ๆ ไม่ใช่ผลลบของใบนี้ ไม่ว่ากรณีใด** · redirect: รันซ้ำ commit เดิม แก้มุมกล้อง/ระดับซูม |
| **N7** CRASH | ไคลเอนต์หลุด/ค้าง | 🟡 ผลที่มีชื่อ | จดว่าหลุดหลังเฟรมไหน (คุมหรือทดลอง) | ❌ ห้ามชี้สาเหตุ · จุดต้องสงสัยอันดับแรกคือ **โครงซอง/ทรงมาสก์** ไม่ใช่ semantics ของค่า (บทเรียน GT-058/059) · เก็บคอนโซลทั้งไฟล์ |
🔴 **ถ้าชั้น (1) ไม่ผ่าน (sha ไม่ตรง pin · สองเฟรมยาวเท่ากัน · ทั้งคู่เป็น 54 · realized gap < 1.00 วิ · คอนโซลขึ้น mode ผิด) ⇒ รอบเป็น NO-RESULT ทางเทคนิค ทุกกรณี — ห้ามอ่านจอเป็นผลใด ๆ แม้จะเห็นความต่างชัด ๆ**

### nonclaims (ติดไปกับผลทุกกรณี ห้ามตัดทิ้ง)
- 🆕🔴 **ยังไม่เคยมีใครเชื่อม "static" เข้ากับ "จอ" ในเรื่องนี้เลย** — `RE-067` พิน **CREATE path ในไบนารี** ส่วนป้ายที่ผู้สังเกตเห็นเป็น **ของชั้น client-observable** · **สองชั้นที่ลงรอยกันคือความสอดคล้อง ไม่ใช่การพิสูจน์** ⇒ ถ้าป้ายลอยที่เห็นเป็น widget คนละตัวกับที่ `RE-067` พิน การตั้ง `+0x1B`/`+0x1A` ก็ไม่เปลี่ยนอะไร และ **ใบจะคืนผลลบด้วยเหตุผลที่ผิด** (ย้ำไว้ข้างแถว N2 ด้วยแล้ว)
- 🆕🔴 **verifier ของ `RE-067` ไม่อยู่ใน version control** (`pf_bridge\staged\re067_static_verify.py` sha `838c70ef…` — ตรวจแล้วสองรอบว่ายังไม่มีใน VCS) ⇒ **ครึ่ง CREATE-selector ซึ่งเป็นฐานของเลนนี้เป็นแหล่งเดียว re-derive ที่ HEAD ไม่ได้ แม้แต่ระดับอ่านวิธี** · สิ่งเดียวที่มีการยืนยันอิสระคือ **ลำดับฟิลด์และ tag ของ codec** (`pf_bridge/external/PF_SERIALIZER_FIELDS.tsv`)
- 🆕🔴 **"+30 เป็นจุดที่รู้ว่าใช้ได้" เป็นข้ออนุมาน ไม่ใช่การวัด** — ป้ายที่จุด +30 ในจ็อบ 1135 ถูก attribute **ด้วยข้อความบนป้าย** ซึ่งตั้งอยู่บนสมมติฐานว่า payload dword คือคีย์ที่ใช้ lookup (**nonclaim ประจำของ `HYP-PF-032`** · หนุนที่ชั้น static โดย `RE-066` **แต่ไม่เคยหนุนที่ชั้น wire**) · และ **ไม่มีใครเคยวัดว่าขอบ frustum ของกล้องอยู่ตรงไหน**
- **ไม่พิสูจน์ว่า `+0x14` (payload dword) เป็น "item id"** — ใบนี้ใช้ค่าเดิม `2200423` เป็นตัวคงที่เพื่อให้ข้อความบนป้ายเหมือนกัน ไม่ได้ทดสอบความหมายของฟิลด์
- **ไม่พิสูจน์ว่า property `0x34` หรือ `0x5D..0x62` "แปลว่าอะไร"** — มันคือ **UI text property** ซึ่งอาจเป็นฟอนต์/ขนาด/สไตล์/การจัดวาง/พรีเซ็ต · 🔴 **ห้ามเรียกมันว่า "ตัวเลือกสี" ในเอกสารใด ๆ**
- **ไม่พูดถึงหน้าตาป้ายชื่อ actor/NPC เลย** — ครึ่ง actor ของ `RE-067` ปิดแบบ bounded negative และเปิดต่อเป็น **`RE-068` ซึ่งยังเปิดอยู่**
- **ไม่ claim ว่าเซิร์ฟเวอร์ต้นฉบับ (ปิดแล้ว กู้ไม่ได้ตลอดกาล) เคยส่งบิต `0x08`/`0x20`** — การประกอบเฟรม ค่ามาสก์ ค่า index จังหวะ 1.50 วิ เป็น **ดีไซน์ของเราทั้งหมด**
- **หน้าตาที่ตรงกับภาพเก่าของเซิร์ฟเวอร์ต้นฉบับ ไม่ใช่หลักฐานว่าเซิร์ฟเวอร์ต้นฉบับส่งไบต์ชุดเดียวกัน** — และภาพอ้างอิงอาจมาจาก **client คนละ build/ภูมิภาค** (nonclaim ข้อ 2 ของ `RE-067`)
- **สีอ่านด้วยตา ไม่ได้วัดค่าพิกเซล** (nonclaim ข้อ 1 ของ `RE-067` · PLAYBOOK ข้อ 13)
- **guards ของ `pf_ground_loot_nameprop_headless_replay.py` พิสูจน์ชั้น wire/dispatcher เท่านั้น** — ไม่มีไคลเอนต์อยู่ในนั้น **ห้ามยกไปตอบแทนชั้น (2) ไม่ว่าผลจะออกแถวไหน**
- **ใบนี้ไม่แตะ claim ใด ๆ ของ `HYP-PF-032`/GT-045** — คนละโมดูล คนละ flag คนละ latch · **เฟรมคุมเป็นทรงเดียวกับที่เลนเก่าส่ง แต่ถูกยิงโดยเลนใหม่และมี element key ของตัวเอง** ⇒ **ห้ามอ้างว่ามันคือเฟรมของ `HYP-PF-032` และห้ามเอา sha ของ GT-045 มาเทียบ**
- **ไม่แตะคำถามเรื่องโมเดลไอเทมบนพื้น** และ **ไม่ปลดเงื่อนไข (ข) ของ `GT-060`** — ป้ายชื่อไม่ใช่วัตถุที่คลิกได้ · **การวาดไม่ใช่การหยิบ** · **ไม่ claim ว่ามี entity อยู่จริงบนพื้น**

- **result:** (ผู้เทสกรอก: ① คำเคาะเรื่องงบเวอร์ชันมาแล้วหรือยัง (ใครเคาะ เมื่อไร) ② `BOOT_COMMIT` + ผลเช็คเจ็ดข้อทีละข้อ (แปะสิ่งที่คอนโซลพิมพ์) + **mode ที่คอนโซลขึ้นตอนบูต** ③ ความยาว pc/frame ของ **แต่ละเฟรมแยกกัน** (ต้องเป็น 44/54 กับ 48/58) + masked sha ทั้งสี่ค่าตรง pin หรือไม่ + ไบต์มาสก์ที่อ่านได้ (`12` / `3A`) ④ **realized gap ระดับ ms** ⑤ trigger X/Y/Z + พิกัดที่ decode ได้ของทั้งสองเฟรม (ต้องเท่ากัน) ⑥ **แถวไหนของตารางผล (N1-N7)** ⑦ ตารางต่อแฟลช: เวลาโผล่/หาย · อายุ · ข้อความ · **หน้าตาทุกมิติ (สี/ขนาด/ความหนา/สไตล์/การจัดวาง)** ⑧ **ต่างหรือเหมือน และต่างตรงไหน** ⑨ **ตาราง PLAYBOOK ข้อ 13 ครบทุกป้ายทุกภาพ ("ไม่มี" เขียนออกมา ห้ามเว้นว่าง)** ⑩ path + sha256 ของ G0/G0b/A_CONTROL_FULLRES/A_CONTROL_CROP/B_IDX6_FULLRES/B_IDX6_CROP/CONTROL_GONE + วิดีโอ + **ค่ากรอบ crop ที่ใช้ (ต้องค่าเดียวกันทั้ง A และ B)** ⑪ ค่าที่ต้องเติม `REAL_SERVER_DIVERGENCE.tsv` (**ส่งค่ามา ห้ามแก้ไฟล์เอง**) ⑫ มี `ErrorData=28317` ไหม หลังเฟรมไหน + บรรทัด `PF-EVENT` ที่เห็น (ก๊อปทั้งบรรทัด) + NO-CRASH/CRASH ⑬ path raw GAME log + console ทั้งไฟล์ ⑭ เวลา +07:00 · sha canonical ก่อน-หลัง · `integrity_check` · row-diff + `max(lease_generation)` ของ `run_gt069*.sqlite3` · exit code ของ teardown ⑮ ถ้ามี session 2: ทุกข้อข้างบนแยกชุด **ห้ามรวมกับ session 1**)

---

## GT-072 ACTOR-SLOT-DISPLACEMENT-001 [attended, in-game]: spawn actor ของเรา **ทับพิกัด placement ของ NPC ที่มีอยู่** แล้ว NPC ตัวนั้น **หายจากจอหรือไม่ — และถ้าหาย มันคือ despawn / แทนที่ / บังทับ**  [🟡 **PARTIAL — บันทึกผลรอบแรกโดย chief R170 (2026-08-25 ~22:0x +07:00) · ใบยังเปิดอยู่** · จ็อบ 1167/1168/1169 attended · 🔴 **ยังไม่มีค่าไหนในสามค่าถูกตัดออก** — ตัวคุมที่เก็บมาถูกวัด *หลัง* ของที่ต้องแยกแยะหายจากจอไปแล้ว (ดูไทม์ไลน์ท้ายใบ) · ตัวคุมที่ยังไม่ได้ทำ: `W2` · `W3` · `POST-A` ⇒ ยกไปใบ **`GT-074`** · **ผลอยู่ท้ายใบ** · เปิดใบโดย chief R168 (2026-08-25 ~20:3x +07:00) ตามผลข้างเคียงข้อ ④ ของ `GT-030-R3` · เขียนใบโดย `pf-queue-author`]

> 🔢 **เรื่องเลขใบ (อ่านก่อน):** ตัวนับเป็น **ชุดเดียวร่วมกับ `CLIENT_RE_QUEUE.md`** — prefix สองแบบ ตัวนับเดียว
> เลข **071 ถูกจองโดย `RE-071`** (งาน `STATIC-ON-BRIDGE` ของรอบเดียวกัน: *BasicAttr ของ actor ที่เกิดจาก `SPAWN_BARE`*)
> ⇒ **ใบนี้คือ `GT-072`** · grep ยืนยันก่อนจอง: `GT-072`/`RE-072` = 0 hit ทั้งสองไฟล์ ⇒ **เลขว่างถัดไปคือ 073**
> 🔴 **ร่างแรกของใบนี้เขียนเลขเป็น `GT-071` — chief แก้เป็น `GT-072` ตอนวาง** ถ้าเจอ `GT-071` ที่ไหนในเอกสารเก่า นั่นคือใบนี้
> 🔴 **ใบ `GT-030` และ `GT-030-R3` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย** — ใบนี้ยืนอยู่บนผลของมัน

---

> 🔴🔴 **มีข้อสังเกตจากรอบสี่ของ `GT-030` ที่เกี่ยวกับใบนี้ — แต่ chief จงใจวางไว้ที่ *ท้ายใบ* ในบล็อกปิดผนึก**
> **ห้ามอ่านก่อนสังเกตจบ** (หัวข้อ *"🔴 อ่านหลังจบการสังเกตเท่านั้น"* ท้ายใบ) — เหตุผล: มันเป็นข้อสังเกตที่ยังไม่แยกสาเหตุ
> และการอ่านมันก่อนรันจะ **ชี้นำผู้เทสไปทาง despawn** ทั้งที่หลักฐานยังเป็นกลางระหว่าง `N1` กับ `N2`

---

### ที่มา — **ทั้งหมดวัดแล้วในรอบ `GT-030-R3` (จ็อบ 1154/1158/1159/1160) ห้าม re-derive ระหว่างรอบ**

จดหมายต้นทาง: `notes_to_chief\consumed\20260825_1900_GT030-ROUND3-PASS-actor_type2-rendered-for-the-first-time-plus-a-death-nobody-predicted.md` §④ · และบล็อกผลของ `GT-030-R3` ในไฟล์นี้

- เฟรม **`SPAWN_BARE` (181 B)** ของเลน **`HYP-PF-025`** ออกสายที่ **t=222.37** (นาฬิกาวิดีโอของรอบนั้น) วางตัว `ProbePlayer01` ที่พิกัด **เดียวกันเป๊ะ** กับ placement **`P0 (-9140.0, -2780.0)` `P_MALE_002_000_SP1` ชื่อ `Navy Transfer`** ในตาราง `pf_login_game_server_v141.py`
- **ภาพคู่ before/after กล้องมุมเดียวกัน ตัวละครยืนจุดเดิม ห่างกัน 1.5 วิ คร่อมไบต์:**

  | ภาพ | t | เห็นอะไร |
  |---|---|---|
  | `evidence_screens/GT030R3_1159_NAVYTRANSFER_PRESENT_t221.5s.jpg` | 221.5 | NPC ชุดน้ำเงิน-ขาว **ยืนอยู่** · ช่องแชตยังพิมพ์ค้าง ยังไม่กด Enter · ผู้เทสอยู่ `X -8,876 Y -2,715` |
  | `evidence_screens/GT030R3_1159_NAVYTRANSFER_GONE_SAME_CAMERA_t223.0s.jpg` | 223.0 | **มุมกล้องเดิม พิกัดผู้เทสเดิม — NPC หายไป** |

- **ตัวที่หายถูกระบุด้วยระยะ ไม่ใช่ด้วยป้าย:** จาก `(-8876, -2715)` ⇒ `dist 271.9` ไป `P0 Navy Transfer` · `dist 865.0` ไป `P1 (-8013.5,-2780.0) M010_001_000_N Sebastian` (ไกลกว่า 3 เท่า)
- **ตัวแปรกวนที่ชัดที่สุดถูกปิดด้วยการวัดแล้ว:** เลน population `V134_P0_P30_P91_ISOLATED_*` **เก็บ P0 ไว้** และถูกส่งที่ **t=197.97 = ก่อน `SPAWN_BARE` 24.4 วินาที** ⇒ **NPC ไม่ได้หายเพราะเลน population**
- 🔴🔴 **และนี่คือเหตุผลทั้งหมดที่ใบนี้เกิด: หลักฐานชุดนั้น *แยกไม่ออก* ระหว่างสามความเป็นไปได้ — `despawn` · `แทนที่ (replace)` · `บังทับ (occlusion)`** เพราะรอบนั้น **ไม่มีใครเปลี่ยนมุมมอง ไม่มีใครเดินเข้าไปดู และไม่มีใครคลิกที่จุดนั้น**

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

### 🟢 งบเวอร์ชัน — **ศูนย์สล็อต**

- `docs/HYPOTHESIS_LEDGER.json` → **`HYP-PF-025` = 2/5** (`REMOTE-PLAYER-ENCODER-001`, `REMOTE-PLAYER-DISPATCH-001`) · เพดาน `max_versions: 5` (เจ้าของยกเป็น 5 แล้ว)
  🔴 **provenance ของตัวเลขนี้:** ยกมาจากบล็อก "งบเวอร์ชัน" ของ `GT-030-R3` ซึ่ง **chief R167 เปิด ledger ตรวจเอง** · **รอบ R168 ไม่ได้เปิด ledger ซ้ำ** ⇒ ถ้าจะใช้ระดับ "วัดในรอบนี้" ให้ `git grep` ledger อีกครั้งก่อนบูต
- ใบนี้ **ไม่แก้โค้ด ไม่แก้ mask ไม่แก้ไบต์ ไม่แก้ scenario แม้ตัวอักษรเดียว** — บูตเลนเดิมที่ `GT-030-R3` เพิ่งบูต ⇒ **ไม่เพิ่ม tracked version ⇒ ไม่กินสล็อต**
- 🔴🔴 **ตัวคุมที่ "สะอาดกว่า" ที่ใบนี้ *ไม่มี* และทำไมถึงไม่มี:** ตัวคุมในฝันคือ **`SPAWN_BARE` เฟรมเดียวกันเป๊ะ ยิงลงพิกัดที่ไม่มี placement ใด ๆ** — นั่นคือการเพิ่ม/ย้ายเฟรมใน scenario = **wire change = กิน 1 สล็อต (2/5 → 3/5) และ chief ต้องออกแบบก่อน** ⇒ **รอบนี้ไม่ทำ** · ใบนี้ใช้ตัวคุมที่มีอยู่แล้วในเลน (บล็อกถัดไป) และเขียนตรง ๆ ว่ามันคุมอะไรไม่ได้บ้าง
- 🔴 **ถ้าใครระหว่างรอบคิดจะขยับพิกัด/มาสก์/ไบต์ "เพื่อลองดู" — นั่นคือ wire change · กินสล็อต · ห้ามเด็ดขาดในรอบนี้** · ผู้เทสไม่ต้องตัดสินเรื่องงบเวอร์ชัน และ **ห้ามแก้ ledger ไม่ว่าผลจะออกแถวไหน**

### 🟢 ใบนี้รอ merge อะไรไหม — **ไม่รอ รันได้บน `main` ปัจจุบันเลย**

เลน `HYP-PF-025` + flag + scenario **ship อยู่แล้วและถูกบูตจริงเมื่อ 2026-08-25 18:42 (boot `06b62abd`, CODE_DELTA 0)** ⇒ **ไม่ต้องรอ PR ไม่ต้องรอ branch ไม่ต้องรอคำเคาะเจ้าของ**
🔴 **แต่ยังต้องรัน `pf_resolve_green_boot.py` และด่านหกข้อทุกครั้งตามปกติ** — "เครื่องมือชนะใบเสมอ" (ถ้าเครื่องมือบอกว่าบูตไม่ได้ ให้เชื่อเครื่องมือ แล้วจดความขัดแย้งลงผล)

---

### 🔴 ตัวคุมเชิงลบของรอบนี้ — **สามตัว ทั้งหมดฟรี ไม่กินสล็อต** (และเขียนไว้ล่วงหน้าว่าแต่ละตัวคุมอะไรไม่ได้)

| ตัวคุม | ของจริงในเลน | คำถามที่มันแยกออก | 🔴 สิ่งที่มัน **แยกไม่ออก** |
|---|---|---|---|
| **NC-1 พิกัดว่าง `B`** | `SPAWN_AVATAR` ที่ **X `-8989.957`** (+15 วิ) — **ไม่ทับ placement ใด ๆ** (ตัวใกล้สุดคือ `P0` ห่าง **150 หน่วย**) | *"สิ่งที่หายไปหายเพราะ **ทับ placement** หรือหายเพราะ **มีการ spawn เกิดขึ้นเฉย ๆ**"* — ถ้ามีของหายรอบ ๆ จุด `B` ตอน +15 ด้วย ⇒ ไม่ใช่เรื่องการทับ | 🔴 **เป็นคนละเฟรมคนละทรง** (`SPAWN_AVATAR` พก `AvatarAttr`, ขนาดต่างกัน) ⇒ **ไม่ใช่ตัวคุมที่ต่างกันตัวแปรเดียว** — ห้ามเขียนว่า "คุมได้เท่ากับ `SPAWN_BARE` ที่พิกัดว่าง" |
| **NC-2 พิกัดว่าง `C`** | `NEGATIVE_CONTROL` ที่ **X `-9289.957`** (+60 วิ) — ไม่ทับ placement ใด ๆ · NPCAttr ผิดคลาสโดยเจตนา (bind gate `0x4697B0` ต้องทิ้งเงียบ) | เหมือน NC-1 อีกจุดหนึ่ง คนละฝั่ง (`-X`) · **และเป็นเกณฑ์หยุดทั้งเลนของก้อน 1** | ถูกออกแบบให้ถูกทิ้ง ⇒ **ถ้าไม่มีอะไรเกิดที่จุดนี้ นั่นคือสิ่งที่คาดไว้อยู่แล้ว ไม่ใช่ข้อมูลใหม่เรื่องการทับ** |
| **NC-3 NPC ตัวอื่นบนแมพ** | `P1 (-8013.5, -2780.0) M010_001_000_N` ชื่อ `Sebastian` — **อยู่คนละจุด ไม่มีเฟรมไหนของเราแตะจุดนั้นเลย** | *"เป็นผลเฉพาะจุดที่ทับ หรือเป็นการกวาด NPC ทั้งย่าน/ทั้งแมพ"* ⇒ ถ้า `Sebastian` ยังอยู่ครบหลังรอบ = ผลไม่ใช่การกวาด | **ไม่ได้อยู่ใต้วิดีโอต่อเนื่องกรอบเดียวกัน** (ต้องเดินไปดูทีหลัง) ⇒ ตอบได้แค่ **"ยังอยู่ตอนไปดู"** ไม่ใช่ "ไม่เคยหายเลย" |

🔴 **ถ้าจุดใดในสามตัวนี้ตรวจไม่ได้จริงในรอบ (เดินไม่ทัน / อยู่นอกเฟรม / หาไม่เจอ) ⇒ เขียนคำว่า "ไม่ได้ตรวจ" ออกมาเป็นตัวอักษร ห้ามเว้นว่าง ห้ามเดา**

---

### db (สำเนาเสมอ — **canonical ไม่ถูกเปิดตลอดรอบ**)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-072_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt072.sqlite3
```
- เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง**
- เลนนี้ `persisted_post_state.database_write = "none"` ⇒ เกณฑ์สำเนา: **row-diff ทุกตารางต่างได้เฉพาะ `sessions` +1 แถวต่อการเข้าเกมหนึ่งครั้ง** (`count(*) WHERE selected_character_id IS NOT NULL` — ห้ามนับแถวเปล่า) · จด `max(lease_generation)` ก่อน-หลัง · ห้ามถอยหลัง
- 🔴 **สำเนาใหม่ทุกบูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกครั้ง** — เผื่อเวลาเดินไป landmark ไว้ในแผนเสมอ
- ถ้าเปิด session 2: สำเนาใหม่ `state\run_gt072b.sqlite3` (**ห้ามใช้ไฟล์เดิมซ้ำ**)

### 🔴 ก่อนบูต — resolve commit เขียว (รันเครื่องมือ ห้ามก๊อป SHA เก่า)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` (detached HEAD ถูกแล้ว)
- **exit 3** + `BOOT_COMMIT: NONE` ⇒ **ห้ามบูต** จดว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · **exit 2** = พาธผิด/git ล้ม · บรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ จดลงผลเสมอ
- 🔴 **ห้ามเทียบ `BOOT_COMMIT` กับเลข commit ใด ๆ ด้วยตา** — ตัดสินด้วยเนื้อ (หกข้อข้างล่าง) เท่านั้น

**ยืนยันหกข้อกับ `<SHA>` ที่จะบูตจริง — ต้องครบ · single quote เท่านั้น (สะพานเป็น PowerShell 5.1) · ห้ามใช้ `| grep` / `awk`**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n 'remote-player-hypothesis-scenario' <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/remote_player_hypothesis_visibility_probe.json && echo SCENARIO_PRESENT
git grep -n 'HYP_PF_025_REMOTE_PLAYER_' <SHA> -- src/pirateforce_foundation/ scenarios/
git grep -n 'classify_chat_input_attempt' <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n 'export-events' <SHA> -- src/pirateforce_foundation/app.py
```
1. `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ · 2. เจอ flag จริง (🔴 **ห้ามใช้ `--help` เป็นหลักฐาน** — คืน 0 บรรทัด exit 0 ผ่านสะพาน) · 3. เห็น `SCENARIO_PRESENT` · 4. เจอ label prefix · 5. **ยืนยันว่าตัวยิงยังเป็น `ascii12`** · 6. เจอ `export-events` ⇒ ใส่ flag · ไม่เจอ ⇒ ตัดออกแล้วจดไว้ว่ารอบนี้ยึด `[G>]` labels + raw SENT hexdump เป็นหลักฐาน dispatch
- **อ่านค่า pin ต่อเฟรมจาก scenario ของ commit ที่บูต ห้ามฝัง sha จากความจำ:** `scenarios/remote_player_hypothesis_visibility_probe.json` → `probe.per_step.<LABEL>.frame_sha256` / `frame_size` · 🔴 **`SPAWN_AVATAR` พินเฉพาะโครง `pc_skeleton_sha256` 172 B** (`avatar_tail_excluded_from_pin: true` — ตัวเลขรวม 288 B เปลี่ยนได้โดยไม่ผิด)
- ไม่ครบหกข้อ + ยังไม่ได้ค่า pin = **ห้ามบูต** ใบอยู่ PENDING รอต่อ

### server args (เป๊ะ · opt-in เท่านั้น · `production_allowed=false`)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt072.sqlite3 --remote-player-hypothesis-scenario scenarios\remote_player_hypothesis_visibility_probe.json --export-events
```
- 🔴 **ห้ามใส่ flag hypothesis ตัวอื่นแม้แต่ตัวเดียว** — ชุดเลนของบูตนี้ต้องเป็น **หนึ่งเลน** (และนั่นคือสิ่งที่ทำให้ใช้แชตเป็น clapper ได้)
- console label = `HYP_PF_025_REMOTE_PLAYER_<STEP>` · event = `remote_player_hypothesis_visibility_probe_sent` — **เห็นชื่ออื่น = บูตผิดไฟล์ หยุด ปิด server ห้ามอ่านจอเป็นผล**
- **one-shot ต่อ GAME connection** ⇒ บูตใหม่ = รีอาร์ม · ยิงซ้ำใน connection เดิม = `remote_player_hypothesis_already_sent_no_reply` · 🔴 **reconnect กลางรอบ = ได้ sweep ชุดใหม่ และ probe ชุดเก่าไม่ despawn ⇒ ถ้าเกิด ให้จดทันทีและถือว่ารอบนั้นเสียการเทียบ**
- ⚠️ event ใช้เป็น **ตัวยืนยันรอง** เท่านั้น — เซิร์ฟเวอร์ไม่ persist `state.events` · **raw frame ที่ sha ตรง pin คือหลักฐานปฐมภูมิเสมอ**

### 🔴 ตัว trigger แชต — printable ASCII **12 ตัวเป๊ะ**
- ใช้ **`PFCHATPROBE1`** (P-F-C-H-A-T-P-R-O-B-E-1 = **12 ตัวพอดี** · สตริงเดียวกับสองรอบก่อน ⇒ ไบต์ขาเข้าไม่มีตัวแปรใหม่)
- 🔴 **สั้น/ยาวกว่า 12 = ถึงเซิร์ฟเวอร์แต่เงื่อนไขเงียบ ๆ ไม่ผ่าน ไม่มี error — sweep ไม่ออกเฉย ๆ**
- 🔴 **คลิกช่องแชตให้โฟกัสก่อนพิมพ์เสมอ** — ตัวอักษรที่พิมพ์ตอนช่องแชตไม่โฟกัส **กลายเป็นฮอตคีย์** (มี toggle ที่ปิดเลขดาเมจทั้งจอเงียบ ๆ โดยที่ wire เหมือนเดิมทุกไบต์)
- `Return` **หนึ่งครั้ง** · **หลัง Enter ห้ามพิมพ์ตัวอักษรใด ๆ อีกทั้งรอบ**
- 🔴 **ลำดับที่ห้ามสลับ:** ตัวยิงคือแชต ⇒ **ถ้าพิมพ์แชตเป็นขั้นแรกของรอบ sweep จะยิงตั้งแต่ยังยืนอยู่จุดเกิด ก่อนถ่าย baseline และ one-shot ไหม้ทั้งรอบ** ⇒ **สำรวจ + ถ่าย PRE ให้ครบก่อนเสมอ แล้วค่อยพิมพ์**

### 🔴🔴 ท่ากล้อง ทิศหัน และการเดิน — อ่านให้จบก่อนแตะเมาส์

| ท่า | ทำอะไรจริง | ยิง `TargetPosVital` ไหม | ใบนี้ใช้ได้เมื่อไร |
|---|---|---|---|
| **คลิกขวาค้างลากเมาส์** | หมุน **มุมกล้อง** อย่างเดียว · **ทิศหันของตัวละครไม่ขยับ ไม่มีอะไร trigger** | 🟢 ไม่ยิง | ✅ ปลอดภัยทุกจังหวะของรอบ · **เป็นตัวเช็ค NO-CRASH ของใบนี้** · ❌ **ยกเว้น WINDOW-1 ซึ่งห้ามแตะด้วยเหตุผลเรื่องกรอบภาพ ไม่ใช่เรื่องสาย** |
| **`Q` / `E`** | **หันตัวละคร** กล้องแพนตาม | 🔴 ยิง | ⚠️ ไม่ทำให้ sweep ยิง (ตัวยิงคือแชต) แต่ **ทำกรอบกล้องเสีย** ⇒ ❌ ห้ามใช้ตลอดรอบ · 🔴 **ห้ามใช้เป็นตัวเช็ค NO-CRASH เด็ดขาด** |
| **`W/A/S/D`** | เดิน (เปลี่ยนทั้งตำแหน่งและทิศหัน) | 🔴 ยิง | ✅ ใช้ได้ในขั้นที่ใบระบุ (PRE · WINDOW-3 · POST) — **การเดินไม่ทำให้ sweep ยิงและไม่กิน one-shot** ❌ ห้ามใน WINDOW-1/2/4 |
| **ล้อเมาส์ (ซูม)** | ซูมกล้อง | **[UNKNOWN — ไม่มีใครเคยวัด]** | ใช้ได้เฉพาะขั้นซูมก่อนทริกเกอร์ · **จดเวลาที่ซูมทุกครั้ง** |

🔴 **ประโยคเดียวที่ต้องจำ: ตัวที่ยิง `TargetPosVital` คือ "การเปลี่ยนทิศหันของตัวละคร" ไม่ใช่ "การขยับกล้อง"** — และ `TargetPosVital` **ไม่ใช่** ตัวยิงของเลนนี้
🔴 **เหตุผลที่ WINDOW-1 ห้ามแตะแม้แต่คลิกขวาลาก เป็นเรื่องหลักฐาน ไม่ใช่เรื่องไบต์:** เกณฑ์ชี้ขาดของใบคือ **"กล้องมุมเดียวกันเป๊ะ ตัวละครยืนจุดเดียวกันเป๊ะ ก่อน/หลัง"** — ขยับเมื่อไรคู่ภาพนั้นเทียบไม่ได้

### ⏱️ กติกาตัดสินเวลา — **นาฬิกาเดียว ห้ามข้ามนาฬิกา**
- 🔴 **offset ระหว่างนาฬิกาวิดีโอกับนาฬิกาสายไม่ใช่ค่าคงที่** — สามรอบของ 2026-08-25 ได้ `~0.0 / 0.58 / 1.82` วิ ⇒ **ห้ามใช้ตัวเลข "หายภายใน 0.6 วิหลังไบต์" ของ R3 เป็นเกณฑ์ และห้ามผลิตตัวเลขข้ามนาฬิกาใหม่เป็นคำตัดสิน**
- **สมอเวลาในจอของรอบนี้ = `T0` คือ *เฟรมที่ช่อง input ของแชตเคลียร์*** (🔴 **ไม่ใช่เฟรมที่ตัวอักษรโผล่**) — เป็นเหตุการณ์ที่อยู่ในวิดีโอไฟล์เดียวกับสิ่งที่จะวัด ⇒ **offset ตัดกันทางพีชคณิต**
- **ลำดับถูกค้ำด้วยเหตุ-ผลในโค้ด:** sweep ถูก compose **ในฐานะคำตอบต่อเฟรมแชต** (`runtime.py` → `_dispatch_remote_player_hypothesis`) ⇒ **ไม่มีทางที่ `SPAWN_BARE` จะออกก่อน `T0`**
- ⇒ **สิ่งที่รายงานได้:** `t_หาย - T0` เป็นวินาที (นาฬิกาวิดีโอตัวเดียว) · **สิ่งที่รายงานแยกต่างหากในฐานะข้อสังเกต ไม่ใช่เกณฑ์:** เวลานาฬิกาจริงของ `SENT ..._SPAWN_BARE` จาก `GAME_LIVE.txt` และผลต่างของสองนาฬิกาที่คำนวณได้
- 🔴 **ถ้า `T0` หาไม่เจอในวิดีโอ (ช่องแชตอ่านไม่ออก/ไม่เคลียร์) ⇒ ใช้เกณฑ์สำรอง: "NPC อยู่ในภาพ `PRE_LAST` และไม่อยู่ในหน้าต่างสวีป"** ซึ่ง **หยาบกว่าแต่ยังใช้ได้** — และต้องเขียนลงผลว่าใช้เกณฑ์สำรอง

---

### ⏱️ ไทม์ไลน์ของรอบ — **หน้าต่างมีหมายเลข · เวลาเป็นวินาทีนับจาก `T0`** (เผื่อคลาด ±2 วิ · **หลุดจังหวะให้จดเวลาจริง ห้ามแต่งผล · วิดีโอคือกรรมการ**)

| หน้าต่าง | เวลา | เฟรมของเลนที่ตกในช่วงนี้ | ผู้เทสทำอะไร | ทำไม |
|---|---|---|---|---|
| **PRE** | ก่อน `T0` | — | สำรวจ · ตั้ง CAM-C/L/R · คลิกอ่านพาเนลของ NPC · `PRE_LAST` | baseline ชี้ขาด + **ระบุตัว NPC ด้วยชื่อ ไม่ใช่ด้วยระยะ** |
| **W1** | `T0` → `+10` | `SPAWN_BARE` (~+0) | 🔴 **ห้ามแตะเมาส์และคีย์บอร์ดเลย** ยืนนิ่ง มองจอ | ทำซ้ำคู่ภาพ same-camera ของ R3 ให้ได้ก่อน แล้วค่อยไปทำอย่างอื่น |
| **W2** | `+10` → `+20` | — | **คลิกขวาลากอย่างเดียว**: CAM-L → CAM-R → กลับ CAM-C | **แยก "บังทับ" ด้วยมุม โดยตัวละครยังยืนจุดเดิมเป๊ะ** ⇒ เทียบกับ `PRE_L`/`PRE_R` ได้ตรง ๆ |
| **W3** | `+20` → `+29` | — | เดิน `W/A/S/D` เข้าไปหา `P0` หยุดห่าง ~40-80 หน่วย · **คลิกซ้าย 3 ครั้ง + `Tab` 3 ครั้ง ที่จุดที่ NPC เคยยืน** | **แยก "บังทับ" ด้วยระยะ/พารัลแลกซ์ + แยก "แทนที่" ด้วย target panel** |
| **W4** | `+29` → `+50` | `MOVE_A_1` (~+30) · `MOVE_A_2` (~+45) | ยืนนิ่ง ให้ `P0` อยู่ในเฟรม เฝ้าดู | 🔴 **`A` ออกจาก `P0` ตอน +30** ⇒ **"NPC กลับมาไหมเมื่อของเราย้ายออก" คือคำถามที่ตอบได้ฟรีในรอบนี้** |
| **W5** | `+55` → `+70` | `NEGATIVE_CONTROL` (~+60) | คลิกขวาลากหันกล้องไปทาง `-X` ให้เห็นจุด `C` | NC-2 + **เกณฑ์หยุดทั้งเลน** |
| **POST** | `+70` เป็นต้นไป | — | เดินไปยืน**ทับ** `P0` · วนรอบ 4 ทิศ · คลิก/`Tab` · แล้วไป `B` / `A-หลัง-MOVE` / `Sebastian` | ปิดทั้ง "บังทับ" และ NC-3 |

---

### steps (คลิกต่อคลิก)

**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด **boot stamp (+07:00)** · preflight จอว่าง (`staged\TEMPLATE_preflight_unattended.ps1` — เจอหน้าต่าง elevated = ABORT ทั้งรอบ) · เทียบ sha canonical · copy DB สองใบตามบล็อก db
**เตรียม teardown:** ก๊อปจาก **`TEMPLATE_teardown_generic.ps1`** เป็นหลัก · ถ้าก๊อปจากจ็อบที่เป็นตัวเลข **ต้องเปิดดูบรรทัดที่ 17 ให้เห็น `-replace '\\','/'` ก่อนเสมอ** · 🔴 **ห้ามก๊อปจาก `1103`/`1105`**

1. **สตาร์ตเซิร์ฟเวอร์ก่อน แล้วค่อยบูต client เสมอ** (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client)
   - 🔴 client ที่บูตโดยไม่มีเซิร์ฟเวอร์ **ตายเองใน ~3.5 นาที**
   - 🔴 **ถ้าต้องฆ่า client กลางคัน ต้อง restart server ก่อนเปิด client ตัวใหม่เสมอ** (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่ "connecting" ตลอดกาล)
   - จัดหน้าต่าง console ให้เห็นข้างจอเกมโดยไม่บังพื้นที่วัด · **ตลอดรอบห้ามคลิก console**
2. เปิด client (`Invoke-CimMethod Win32_Process Create`) → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร → **เลือกช่องแรก** → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (🔴 **ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด**) · ถ้าคลิกปุ่มไม่ติด ใช้ท่า `Return`
3. เข้าแมพ เห็น HP/minimap/ชื่อแมพ → **เริ่มอัดวิดีโอต่อเนื่องตรงนี้ ยาวจนจบ session** ลง `evidence_video\` ด้วย `staged\TEMPLATE_video_recorder.ps1 -FrameRate 30` · จดบรรทัด `VIDEO START pid= start= fps= path=` (🔴 `start=` คือเวลาที่เรา**สั่ง** ffmpeg **ห้ามใช้เป็นสมอเวลา**) · 🔴 **ไม่ได้อัด = NO-RESULT ทันที**
4. **เดินไปหา NPC `Navy Transfer`** (landmark · actor identity `0x2001` · `P0` X `-9139.957` Y `-2780.045` Z `223.292`) — **ยืนห่าง ~200-300 หน่วย ฝั่งที่มองเห็นตัวเต็ม ๆ** (รอบ R3 ยืนที่ `(-8876,-2715)` = ห่าง `271.9` และเห็นชัด — ใช้เป็นตัวอ้างอิงได้) · **จด X/Y จาก HUD**
5. **ซูมด้วยล้อเมาส์** จนเห็น `P0` เต็มตัว **และเห็นพื้นที่รอบ ๆ อีกราว 200 หน่วย** · **จดเวลาที่ซูมทุกครั้งและระดับซูม** · 🔴 **หลังขั้นนี้ห้ามแตะล้ออีกจนจบ W4** (ซูมเปลี่ยน = คู่ภาพเทียบไม่ได้)
6. **ตั้ง `CAM-C` ด้วยคลิกขวาค้างลากเมาส์** ให้ `P0` อยู่กลางเฟรม → ถ่าย **`PRE_C`** (full-res)
7. **คลิกขวาลากไป `CAM-L` (~45° ทางซ้าย)** → ถ่าย **`PRE_L`** → **`CAM-R` (~45° ทางขวา)** → ถ่าย **`PRE_R`** → **กลับ `CAM-C`** → ถ่าย **`PRE_C2`**
   - 🔴 **จดจุดอ้างอิงบนฉากของแต่ละมุม** (ภูเขา/อาคาร/เส้นขอบฟ้า) ลงกระดาษ — **W2 ต้องกลับมาที่สามมุมนี้ให้ใกล้เคียงที่สุด**
   - 🔴 ห้ามแตะคีย์บอร์ดและล้อเมาส์ในขั้นนี้
8. **ระบุตัว NPC ด้วยพาเนล (ขั้นบังคับ — แก้ nonclaim ของ R3 ที่ระบุตัวด้วยระยะอย่างเดียว):** คลิกซ้ายที่ตัว NPC หนึ่งครั้ง (ถ้าคลิกไม่ติดให้ลอง `Tab`) → ถ่าย **`PRE_PANEL`** (full-res) → **อ่านและจดทุกตัวอักษรบนพาเนล + สีของทุกป้ายในเฟรม** → คลิกพื้นว่างเพื่อยกเลิกเป้า
   - 🔴 **ห้ามกดปุ่มโจมตีใด ๆ** · 🔴 **จดเวลานาฬิกา (+07:00) ของการคลิก/`Tab` ทุกครั้ง** — **ไม่มีใครเคยวัดว่าคลิกซ้าย/`Tab` ยิงไบต์อะไรออกสายหรือไม่**
   - ⚠️ ถ้าการคลิกทำให้ตัวละคร**ขยับหรือหัน** ให้จดไว้ แล้วจัด `CAM-C` ใหม่ด้วยคลิกขวาลาก และถ่าย **`PRE_C3`**
9. ถ่าย **`PRE_LAST`** ที่ `CAM-C` **ภายใน 10 วินาทีก่อนพิมพ์แชต** — 🔴 **ภาพนี้คือ baseline ชี้ขาด: NPC ต้องอยู่ในภาพ และ X/Y บน HUD ต้องอ่านออก**
10. 🔴 **ยิงทริกเกอร์ = clapper (ครั้งเดียวของทั้งรอบ):** คลิกช่องแชตให้โฟกัส → พิมพ์ **`PFCHATPROBE1`** → **`Return` หนึ่งครั้ง** → **คลิกพื้นว่างเพื่อปลดโฟกัสแชต** → **มือออกจากคีย์บอร์ดและเมาส์**
    - **จดทันทีสองอย่าง:** (i) **เฟรมที่ช่อง input เคลียร์ = `T0`** (ii) **บรรทัดแชตที่พิมพ์ ปรากฏในหน้าต่างแชตบนจอหรือไม่**
    - 🔴 ข้อ (ii) คือ **การทดสอบว่า clapper ใช้ได้จริงไหม ไม่ใช่การใช้ clapper** — ถ้าไม่ปรากฏ ให้เขียนลงผลว่า **"clapper ไม่ให้ค่าในรอบนี้"** นั่นคือผล ไม่ใช่ความล้มเหลว
11. **W1 (`T0` → `+10`): ห้ามแตะเมาส์และคีย์บอร์ดเลยแม้แต่คลิกขวาลาก** — ยืนนิ่ง ตาอยู่ที่จอ
    - **พูดออกเสียงทันทีที่เห็นอะไรเปลี่ยน** (มีคนจดเวลาให้ หรืออัดเสียงไว้)
    - ภาพนิ่งทุกใบของใบนี้ **ถ่ายด้วยเครื่องมือนอกเกม** — 🔴 **ห้ามกดคีย์ในหน้าต่างเกมเพื่อถ่ายภาพ** (คีย์ = ฮอตคีย์) · **อย่าพยายามถ่ายให้ทันเหตุการณ์ วิดีโอคือกรรมการ**
12. **W2 (`+10` → `+20`): กล้องอย่างเดียว** — คลิกขวาลากไป `CAM-L` ถ่าย **`POST_L`** (~+12) → `CAM-R` ถ่าย **`POST_R`** (~+15) → กลับ `CAM-C` ถ่าย **`POST_C`** (~+18)
    - 🔴 **ห้ามแตะ `W/A/S/D` `Q/E` และล้อเมาส์** — ตำแหน่งตัวละครต้องเท่าเดิมกับตอน PRE **มิฉะนั้นคู่ `PRE_L↔POST_L` / `PRE_R↔POST_R` ใช้ไม่ได้ ซึ่งเป็นตัวแยก "บังทับ" หลักของใบ**
13. **W3 (`+20` → `+29`): เดินเข้าไปดูใกล้ ๆ** — `W/A/S/D` เข้าหา `P0` หยุดห่างราว **40-80 หน่วย** (อ่าน X/Y จาก HUD) → ถ่าย **`POST_NEAR`**
    - **คลิกซ้ายที่จุดที่ NPC เคยยืน 3 ครั้ง (ห่างกัน ~1 วิ)** แล้ว **กด `Tab` 3 ครั้ง** → **ถ่ายภาพพาเนลทุกครั้งที่พาเนลเปิด** (`POST_NEAR_PANEL_1..n`)
    - 🔴 **ถ้าพาเนลไม่เปิดเลย ต้องมีภาพอย่างน้อยหนึ่งใบ และเขียนคำว่า "พาเนลไม่ขึ้น" ออกมาเป็นตัวอักษร**
    - 🔴 **ห้ามกดปุ่มโจมตีใด ๆ** · จดเวลาการคลิก/`Tab` ทุกครั้ง
14. **W4 (`+29` → `+50`): ยืนนิ่ง ให้ `P0` อยู่ในเฟรม** — เฝ้าดูว่า **มีอะไรกลับมาที่ `P0` ไหม** ตอน `MOVE_A_1` (~+30) และ `MOVE_A_2` (~+45) → ถ่าย **`W4_31`**, **`W4_36`**, **`W4_46`**
    - 🔴 **ถ้า NPC กลับมา นี่คือผลที่ใหญ่ที่สุดของรอบ — จดเวลาให้ละเอียดที่สุดเท่าที่ทำได้ และห้ามกลบให้เรียบ**
15. **W5 (`+55` → `+70`):** คลิกขวาลากหันกล้องไปทาง `-X` ให้เห็นจุด `C` (**X `-9289.957`**) → ถ่าย **`W5_59`** และ **`W5_62`**
    - ⛔ **เกณฑ์หยุดทั้งเลน:** ชื่อ **`ProbeControl03`** โผล่ที่ไหนก็ตาม (ป้ายหรือพาเนล) ⇒ **หยุด เก็บ console ทั้งไฟล์ รายงานทันที**
16. **POST-A (`+70` เป็นต้นไป):** เดินไป **ยืนทับพิกัด `P0`** (HUD ต้องอ่านได้ราว X `-9140` Y `-2780`) → ถ่าย **`POST_ONP0`** → **เดินวนรอบจุดนั้นหนึ่งรอบ ถ่าย 4 ทิศ** (`POST_ORBIT_1..4`) → **คลิกซ้าย + `Tab` ที่จุดนั้นอีกครั้ง ถ่ายพาเนลทุกใบ**
17. **POST-B:** เดินไปจุด **`B` X `-8989.957`** ถ่าย **`POST_B`** + คลิก/`Tab` + ภาพพาเนล → จุด **`A-หลัง-MOVE` X `-8839.957`** ถ่าย **`POST_AMOVE`** + คลิก/`Tab` + ภาพพาเนล
18. **POST-C (ตัวคุม NC-3):** เดินต่อไปทาง `+X` หา **`P1 Sebastian` (X ≈ `-8013.5` Y ≈ `-2780`)** → ถ่าย **`POST_P1`** ให้เห็นตัวและป้าย (ถ้ามี) + คลิก/`Tab` อ่านพาเนล ⇒ ตอบ **"NPC ตัวอื่นบนแมพยังอยู่หรือไม่"**
    - 🔴 หาไม่เจอ/เวลาไม่พอ ⇒ เขียน **"ไม่ได้ตรวจ"** ออกมาเป็นตัวอักษร **ห้ามเว้นว่าง ห้ามเดา**
19. **NO-CRASH / CRASH:** **คลิกขวาค้างลากเมาส์แล้วกล้องหมุน = NO-CRASH** · หลุด/ค้าง = CRASH + จดว่าหลังเฟรมไหน · 🔴 **ห้ามใช้ `Q`/`E` เป็นตัวเช็ค** (มันยิงไบต์ออกสาย)
20. ออกจากเกม: **X** มุมขวาบน (ตรวจก่อนว่าหน้าต่างแอปตัวเองไม่บังปุ่ม X) → dialog ยืนยัน → ปุ่มซ้าย → **หยุดวิดีโอ** → **ปิดเซิร์ฟเวอร์ด้วย**
21. เก็บ **raw GAME log ทั้งไฟล์** (`...\capture_v141\GAME_LIVE.txt`) + console out/err ทั้งหมด (ทุกบรรทัด `[G>]` / `PF-EVENT` / `ErrorData`) → `PRAGMA integrity_check;` บนสำเนาทุกใบ → sha256 ทุกไฟล์
22. **teardown เสมอ** — แม้รอบจบเพราะเลิกเล่น ไม่ใช่เพราะเทสจบ (ดูบล็อกใบเสร็จ) → เทียบ sha canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม
23. **หลังรอบ — แตกเฟรมและทำคู่ภาพชี้ขาด (ห้ามข้าม · 🔴 ห้ามมี `scale=` ในบรรทัดคำสั่งเด็ดขาด):**
```
$mkv = '<path เต็มของไฟล์ FULLROUND .mkv>'
ffmpeg -ss <T0 - 3.00> -i $mkv -t 15.00 -vsync 0 GT072_W1_%03d.png
```
    - หา **เฟรมสุดท้ายที่ยังเห็น NPC** และ **เฟรมแรกที่ไม่เห็นแล้ว** ⇒ ดึงเป็นภาพนิ่ง **full-res จากต้นฉบับโดยตรง**:
      `GT072_<job>_NPC_PRESENT_t<t>s.jpg` และ `GT072_<job>_NPC_GONE_SAME_CAMERA_t<t>s.jpg`
    - + **crop PNG ไม่สูญเสีย ค่ากรอบเดียวกันเป๊ะทั้งสองใบ** (`..._CROP_t<t>s.png`) · **จดค่ากรอบ crop ลงผล**
    - รายงาน **`t_หาย - T0`** เป็นวินาที (นาฬิกาวิดีโอตัวเดียว) 🔴 **ห้ามแปลงข้ามนาฬิกา**
    - 🔴 **ถ้า NPC ค่อย ๆ หาย/กะพริบ/หายแล้วกลับ ให้ดึงภาพทุกช่วงและเขียนออกมาตามที่เห็น ห้ามย่อให้เหลือ "หาย"**
24. 🔴🔴 **G-OBS — ขั้นสุดท้าย บังคับ (กฎเจ้าของ 2026-08-25 ~19:35 +07:00 · อยู่ใน `AGENTS.md` §6 แล้ว):** ก่อนเขียนผลลงคิว/จดหมาย **ผู้ช่วยต้องทวนรายการ "สิ่งที่ผู้ช่วยเห็น" ทั้งหมดให้ผู้เทสยืนยันทีละข้อ** (NPC ในภาพ PRE · เฟรมที่หาย · สามมุมกล้องก่อน-หลัง · ผลคลิก/`Tab` ทุกครั้ง · สิ่งที่เกิด/ไม่เกิดที่ `+30`/`+45`/`+60` · จุด `B`/`A-หลัง-MOVE`/`Sebastian` · สีป้ายทุกป้าย)
    - ผู้เทสตอบเป็นคำเดียวต่อข้อ: **"ตรง" / "ไม่ตรง" / "ฉันไม่ได้ดูข้อนั้น"**
    - จดหมายผล **ต้องมีบรรทัดนี้ตัวอักษรเป๊ะ:** `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`
    - 🔴 **ยังไม่ยืนยัน = ห้ามเขียนผลลงคิว** · 🔴 **บรรทัดนี้เป็น "ขั้นตอน" ไม่ใช่ "หลักฐาน" — ห้ามใช้แทนเกณฑ์ผ่านชั้นใดชั้นหนึ่ง**

**SESSION 2 (แนะนำ ไม่บังคับ · ทำเมื่อเวลาเหลือ · สูงสุด 2 sessions):** ออกจากเกมให้สวย → **ปิด server ด้วยเสมอ** → copy DB ใหม่ (`run_gt072b.sqlite3`) → บูต server (args เดิม เปลี่ยน `--db`) → ทำข้อ 2-23 ซ้ำ
🔴 **หลักฐานของสอง session แยกกันเด็ดขาด ห้ามรวมภาพ ห้ามรวมคำตัดสิน** · 🔴 **และ session 2 ของใบนี้ไม่ปิดข้อผูกพันเรื่องการทำซ้ำของ `GT-030-R3` (nonclaim ④ ของใบนั้น) — คนละคำถาม**

### 🔴 ลำดับข้ามใบ
- **ในรอบใหญ่เดียวกัน ต้องรัน `GT-072` ให้จบ *ก่อน* `GT-032`** — `GT-032` ทำให้ landmark `0x2001` (`Navy Transfer`) ขึ้นศัตรู แล้วมันจะใช้เป็นจุดอ้างอิงกลาง ๆ ไม่ได้อีก
- **ห้ามพ่วงใบอื่นเข้าบูตนี้** — ชุดเลนของบูตนี้ต้องเป็นหนึ่งเลน

---

### คำทำนาย (**คำทำนายคือคำทำนาย · คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว** · ท่องก่อนบูต)

- **P1 [คำทำนาย]** NPC `Navy Transfer` **หายจากจอภายในไม่กี่วินาทีหลัง `T0`** ⇒ ทำซ้ำผลข้างเคียงของ R3 ได้
- **P2 [คำทำนาย]** จาก `CAM-L` และ `CAM-R` (W2) **ก็ยังไม่เห็น NPC** ⇒ ไม่ใช่ **บังทับ**
- **P3 [คำทำนาย · อ่อนโดยธรรมชาติ]** คลิก/`Tab` ที่จุด `P0` ใน W3 **ไม่ได้อะไรเลย ไม่มีพาเนล** ⇒ ชี้ไปทาง **despawn** 🔴 **แต่ไม่ตัดขาด** — สิ่งที่มองไม่เห็น **เล็งคลิกไม่ถูกอยู่แล้ว**
- **P4 [คำทำนาย]** NPC **ไม่กลับมา**ที่ `P0` หลัง `MOVE_A_1` (~+30) และ `MOVE_A_2` (~+45)
- **P5 [คำทำนาย]** `Sebastian (P1)` **ยังอยู่ครบตอนเดินไปดู** ⇒ ไม่ใช่การกวาด NPC ทั้งย่าน
- **P6 [คำทำนาย]** ที่จุด `B` (+15) และจุด `C` (+60) **ไม่มีอะไรหายและไม่มีอะไรโผล่**
- **P7 [คำทำนาย · ถ้าเกิดคือเรื่องใหญ่]** NPC **กลับมาเอง**หลัง `A` ย้ายออกจาก `P0` ⇒ **ช่อง/ตำแหน่งถูกยึดชั่วคราวแล้วคืน** — 🔴 **รายงานเสียงดัง ห้ามกลบให้เรียบ**
- **P8 [คำทำนาย]** ป้ายชื่อลอยหัวของ actor ที่เราส่ง **ไม่มี** และ target panel ของมัน (ถ้าเปิดได้) **ช่องชื่อว่าง** (ตรงกับผล `GT-030-R3`) — **ข้อนี้ไม่ใช่คำถามของใบนี้ จดเป็นข้อสังเกตเท่านั้น**

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
9. 🔴 **ใบปิดด้วยผลลบได้เฉพาะรอบที่ *คุณ Panya เห็นเอง* + มีวิดีโอต่อเนื่อง** (`AGENTS.md` §9 — รอบ unattended ปิดผลลบไม่ได้)
10. 🔴 **ชั้นนี้ตอบไม่ได้:** เฟรมออกจากเซิร์ฟเวอร์จริงไหม · ไบต์ตรง pin ไหม · พิกัดที่ส่งคือ `P0` จริงไหม

🔴 **ถ้าชั้น (1) ไม่ผ่าน (sha ไม่ตรง pin · พิกัดที่ decode ได้ไม่ใช่ `P0` · มี `*_no_reply` · console ขึ้น label เลนอื่น) ⇒ รอบเป็น NO-RESULT ทางเทคนิค ห้ามอ่านจอเป็นผลใด ๆ แม้จะเห็นของหายชัด ๆ**

---

### ตารางผลลัพธ์ที่มีชื่อ — **ทุกทางออกอ่านได้**

| # | สิ่งที่เห็น | คำตัดสินของใบ | อนุญาตให้สรุปว่า | 🔴 **ไม่** อนุญาตให้สรุปว่า / redirect |
|---|---|---|---|---|
| **N1** GONE-EVERYWHERE-NOTHING-TO-SELECT | NPC หาย · ไม่เห็นจากทุกมุมและระยะประชิด · คลิก/`Tab` ที่ `P0` ไม่ได้อะไรเลย · ไม่กลับมาหลัง `+30` | ✅ **ปิดใบ — "หายจริง ไม่ใช่บังทับ" และเข้าทาง despawn** | ว่า **การ spawn actor ของเราลงบนพิกัด placement สัมพันธ์กับการที่ NPC ตัวนั้นหายจากจอ และการหายนั้นไม่ใช่ผลของมุมกล้อง/ระยะ** | ❌ **ห้ามแยก despawn ออกจาก "แทนที่ด้วยตัวที่มองไม่เห็นและเลือกไม่ติด"** — "คลิกไม่ติด" ไม่เท่ากับ "ไม่มีอะไรอยู่ตรงนั้น" · ❌ ห้ามเขียนกลไกฝั่งไคลเอนต์ · **redirect:** ใบ static (ไคลเอนต์คีย์ actor ด้วยอะไร) **ก่อน** จะยิงเกมเพิ่ม |
| **N2** GONE-BUT-SOMETHING-SELECTABLE | NPC หาย · แต่คลิก/`Tab` ที่ `P0` **เปิดพาเนลได้** (ช่องชื่อว่าง หรือชื่ออื่น / `HP`/`LV` แปลก ๆ) | 🎯 **ผลที่แข็งที่สุดที่รอบนี้ทำได้ — เข้าทาง "แทนที่"** | ว่า **มี entity ที่เลือกได้อยู่ที่พิกัดนั้นหลัง `SPAWN_BARE` และมันไม่ให้ข้อมูลแบบเดียวกับ NPC เดิม** | ❌ ห้ามเขียนว่า "ตัวนั้นคือ `ProbePlayer01`" (**ไม่มีป้ายชื่อ ⇒ ระบุจากตำแหน่งเท่านั้น**) · ❌ ห้ามผูกกับผล `HP 0` ของ `GT-030-R3` เป็นสาเหตุ (นั่นคือ `RE-071`) · แนบภาพพาเนลทุกใบ |
| **N3** OCCLUDED | เห็น NPC อีกครั้งจากมุมอื่นหรือระยะประชิด | ✅ **ผลที่มีชื่อและมีค่าสูง — "บังทับ" · หลักฐานของ R3 ถูกอธิบายจนหมด** | ว่า **NPC ยังอยู่ · สิ่งที่ R3 เห็นคือการถูกบัง ไม่ใช่การหาย** | ❌ ห้ามสรุปว่า **อะไร**บัง (โมเดลเรา? เอฟเฟกต์? LOD?) — ไม่ได้วัด · **redirect:** ปิดผลข้างเคียงข้อ ④ ของ R3 ทันที และ **แก้ถ้อยคำในใบ `GT-030-R3` ให้ตรง** |
| **N4** RESTORED-AFTER-MOVE | NPC หายในช่วง `+0..+30` แล้ว **กลับมา**หลัง `MOVE_A_1`/`MOVE_A_2` | 🟠 **นอกความคาดหมาย — finding ใหญ่** | ว่า **การหายผูกกับ *ช่วงเวลาที่ actor ของเราอยู่ที่พิกัดนั้น*** | 🔴 **รายงานเสียงดัง ห้ามเขียนว่า "คงบังเอิญ"** · แนบวิดีโอช่วง `[T0+25, T0+50]` ทั้งช่วง + เวลาที่ NPC กลับมา · ส่งให้ chief ตัดสิน |
| **N5** NO-VANISH | NPC **ยังอยู่ตลอด** ไม่หายเลย | 🔴 **ผลลบที่สะอาด · มีค่าเท่าผลบวก · ไม่ใช่ FAIL** | ว่า **ผลข้างเคียงข้อ ④ ของ R3 ทำซ้ำไม่ได้ในรอบนี้** ⇒ หนุน nonclaim ④ ของ `GT-030-R3` (รอบเดียว ≠ คุณสมบัติของไคลเอนต์) | ❌ ห้ามเขียนว่า "R3 เห็นผิด" — **R3 มีคู่ภาพ same-camera อยู่ในรีโป** · **redirect:** เทียบเงื่อนไขสองรอบให้ครบ (ตำแหน่งผู้เทส · มุมกล้อง · ระดับซูม · ระยะ) แล้วรันซ้ำ commit เดิมได้เลย **ไม่นับเป็นเวอร์ชันใหม่ ไม่ต้องขอใครใหม่** |
| **N6** SPAWN-WIDE-EFFECT | มีของหาย/เปลี่ยนที่จุด `B`/`C` ด้วย หรือ `Sebastian` หายไปด้วย | 🟠 **ผลที่มีชื่อ — ไม่ใช่เรื่องการทับ** | ว่า **ผลกว้างกว่าพิกัดที่ทับ** ⇒ **ตัวคุม NC-1/NC-2/NC-3 ทำงานและมันหักล้างการอ่านแบบ "ทับ"** | ❌ ห้ามระบุขอบเขตของผล (ย่าน? ทั้งแมพ? ทั้ง list?) — ไม่ได้วัด · **redirect:** ใบใหม่ที่นับจำนวน NPC ทั้งย่านก่อน-หลัง |
| **N7** NON-OBSERVED | กล้องขยับกลางหน้าต่าง · `P0` อยู่นอกเฟรม · `T0` หาไม่เจอ · วิดีโอหายช่วง · ซูมเปลี่ยนระหว่างคู่ภาพ | 🔴 **NO-RESULT — ไม่ใช่ผลลบเด็ดขาด** | ไม่มี | ❌ **"ไม่เห็น NPC" ในเงื่อนไขนี้ไม่ใช่ผลของใบ** · **redirect:** รันซ้ำ commit เดิม แก้มุมกล้อง/ระดับซูม/วินัยของ W1 · **🔴 ห้าม archive ใบ** |
| **N8** CRASH | ไคลเอนต์หลุด/ค้าง | 🟡 ผลที่มีชื่อ | จดว่าหลุดหลังเฟรมไหน | ❌ ห้ามชี้สาเหตุ · เก็บ console ทั้งไฟล์ · restart server ก่อนบูตรอบถัดไป |

---

### ⭐ PLAYBOOK ข้อ 13 — บันทึกสีของ **ทุกป้ายชื่อในเฟรม** (คำสั่งคุณ Panya 2026-08-25 · บังคับทุกใบ attended ตั้งแต่ R163)
- **จดอะไร:** ชื่อตัวเราเอง (เหนือหัว + แผง UI ซ้ายบน) · ชื่อ NPC/actor ทุกตัวในเฟรม · ชื่อบนแผง target · ชื่อไอเทมบนพื้น · ชื่อผู้เล่นคนอื่น · บรรทัด title/คำอธิบาย — **หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ**
- **ไม่มีให้เขียนคำว่า "ไม่มี" ออกมาเป็นตัวอักษร** 🔴 **ห้ามเว้นว่าง**
- **อ่านสีจากภาพนิ่งความละเอียดเต็ม / crop PNG เท่านั้น** 🔴 **ห้ามอ่านจาก contact sheet · ห้ามจากภาพย่อ · ห้ามจากวิดีโอ**
  ⇒ เก็บ **full-res** ที่ `evidence_screens\GT072_<TAG>_FULLRES_<yyyyMMdd_HHmmss>.png|jpg` (ภาพชี้ขาดของใบนี้ **ต้องเต็มเฟรมไม่ย่อ** · ถ้าไฟล์ใหญ่เกิน ให้ **crop จากต้นฉบับ ห้าม resize ลง**) · **sha256 ทุกไฟล์**
- **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับที่คุณ Panya เทียบมา:** NPC = **เหลือง** · ผู้เล่น = **เขียว** · ไอเทมบนพื้น = **ขาว** · title/คำอธิบาย = **ฟ้า** · ชื่อตัวเอง = **ขาว**
- 🔴🔴 **ผู้เทสจด "สี" อย่างเดียว ห้ามสรุปสาเหตุ** — **อะไรตัดสินสีของป้ายเป็นคำถามของ `RE-067` (ครึ่ง actor อยู่ที่ `RE-068`)** ⇒ **ห้ามเขียนว่า "แปลว่าไคลเอนต์จัดมันเป็นผู้เล่น/NPC/ศัตรู"** · **ห้ามจับคู่เลข property กับ `FONT_COLOR.n_ID` เพราะเลขดูคล้ายกัน — ไม่มี crosswalk จริง**
- **`REAL_SERVER_DIVERGENCE.tsv`: 🔴 ส่งค่ากลับมาในจดหมายผล ห้ามแก้ไฟล์เองจากหน้าสะพาน** (อยู่นอก allowlist ของ `pf_git_sync.ps1` ⇒ แก้แล้วจะ dirty แล้วบล็อก rebase) · หนึ่งแถวต่อหนึ่งป้ายที่เทียบ (คั่นด้วย **TAB** · อ่านหัวไฟล์ก่อน) · `evidence_layer` = **`eye`** เสมอ · `evidence_ref` = path ภาพ full-res · `evidence_sha256` **คนละคอลัมน์ ห้ามยัดรวม** · `open_ticket` = **`RE-067`** · `blocks_promotion` = `no` · `compared_and_matched` = `yes`/`no`/`no-reference`
- 🔴 **เติมแถวแม้ผลจะ "ตรงกัน"** — "ไม่ได้จด" กับ "จดแล้วไม่ต่าง" คนละเรื่อง · ไม่มีภาพอ้างอิง ⇒ `real_server` = `(ยังไม่มีภาพอ้างอิงของเซิร์ฟเวอร์เดิมสำหรับข้อนี้)` **ห้ามเดา** · `observation_note` = ข้อความที่อ่านได้ + ชื่อภาพ + ข้อสังเกต 🔴 **ห้ามเขียนสาเหตุ**

### เกณฑ์หยุดทั้งเลนทันที (คงเดิมจากก้อน 1)
⛔ ชื่อ **`ProbeControl03`** โผล่ที่ไหนก็ตาม (ป้ายหรือพาเนล) = ข้ออ้าง bind-gate ของก้อน 1 ผิด — ทุกข้อสรุปก้อน 1 ต้องรื้อ · **หยุด เก็บ console ทั้งไฟล์**
⛔ server log มี `ErrorData=28317` ⇒ หยุด เก็บ console ทั้งไฟล์
🔴 **ไม่มีทาง despawn probe ของเราเอง** — สามตัวค้างจนตัด connection · **HP ของ probe = 100 ทุกตัวตามดีไซน์ ถ้าเห็นตัวไหน "ตาย" เอง = ผิดคาด จดละเอียด** (และ **ห้ามสรุปสาเหตุ — นั่นคือ `RE-071`**)

### 🧾 teardown + ใบเสร็จ (บังคับ — **แม้รอบจะจบเพราะคนเลิกเล่น ไม่ใช่เพราะเทสจบ**)
- **teardown เสมอ ภายใน 420 นาทีจาก boot stamp** (`staged\TEMPLATE_teardown_generic.ps1:135` · เพดานถูกยกจาก 180 เมื่อ 2026-08-20 · **เลข 180 ในใบเก่า = stale**) — เกินเพดาน template **ปฏิเสธ exit 12 โดยดีไซน์**
- แท่นที่ถูกทิ้งข้ามชั่วโมง: **อย่าฝืน template** ⇒ `staged\TOOL_stop_stale_server.ps1` แล้วตามด้วย receipt อ่านอย่างเดียว `staged\0949_gt027_stalepad_canonical_guard.ps1`
- ได้ **exit 36** อย่าเดาเอง — แนบบรรทัดที่ 17 ของไฟล์ teardown ที่ใช้จริงมาทั้งบรรทัด
- **ใบเสร็จที่ต้องแนบมากับผล ทุกข้อ:** `AFTER listeners = 0` · **canonical guard: sha256 ก่อน-หลัง = `CANON_SHA.txt`** · **teardown exit code** · `LOCK_GAME` ปล่อยแล้ว · run copy `state\run_gt072*.sqlite3` **เก็บไว้ให้ chief re-derive ห้ามทิ้ง** · path ของ raw GAME log + console out/err + วิดีโอ + ภาพทุกไฟล์ พร้อม **sha256**
- 🔴 **บนสะพานเท่านั้น ห้ามลบ:** ไฟล์ `.mkv` ต้นฉบับ และโฟลเดอร์ capture ของรอบ
- 🔴 **restart เซิร์ฟเวอร์ก่อนบูตรอบถัดไปเสมอ**

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

- **result:** (ผู้เทสกรอก: ① `BOOT_COMMIT` + ผลเช็คหกข้อทีละข้อ (แปะสิ่งที่คอนโซลพิมพ์) + **label/mode ที่คอนโซลขึ้นตอนบูต** ② ยอดรวมบรรทัด `[G>]` ทั้งไฟล์ + ห้า label + ขนาดทีละเฟรม + เวลาที่ออก + `frame_sha256` ตรง pin ไหมทีละเฟรม ③ **พิกัดที่ decode ได้ของทั้งสี่เฟรมที่มีพิกัด** (`SPAWN_BARE` ต้อง = `P0` เป๊ะ) ④ **`T0` อยู่ที่ `t` เท่าไรในวิดีโอ** + บรรทัดแชตปรากฏบนจอไหม ⑤ **`t_หาย - T0`** (นาฬิกาวิดีโอตัวเดียว) หรือคำว่า **"NPC ไม่หาย"** ⑥ **คำตัดสินสามข้อ (ก) มุม (ข) ระยะ (ค) การเลือก** ⑦ **แถวไหนของตารางผล `N1-N8`** ⑧ ตารางเหตุการณ์ (`t` / เห็นอะไร / พิกัด HUD / ไฟล์ภาพ) ⑨ **NC-1 / NC-2 / NC-3 ครบสามข้อ** ("ไม่ได้ตรวจ" เขียนออกมา ห้ามเว้นว่าง) ⑩ **ตาราง PLAYBOOK ข้อ 13 ครบทุกป้ายทุกภาพ full-res** + ค่าที่ต้องเติม `REAL_SERVER_DIVERGENCE.tsv` (**ส่งค่ามา ห้ามแก้ไฟล์เอง**) ⑪ path + sha256 ของภาพทุกใบ + วิดีโอ + **ค่ากรอบ crop ที่ใช้ (ต้องค่าเดียวกันทั้งคู่ภาพชี้ขาด)** ⑫ ผล `ffprobe`: เฟรมจริง/เฟรมคาด/เฟรมหาย ⑬ มี `ErrorData=28317` ไหม หลังเฟรมไหน + บรรทัด `PF-EVENT` ที่เห็น (ก๊อปทั้งบรรทัด) + **NO-CRASH/CRASH** ⑭ เวลาที่ซูมทุกครั้ง + เวลาที่คลิก/`Tab` ทุกครั้ง (+07:00) ⑮ sha canonical ก่อน-หลัง · `integrity_check` · row-diff + `max(lease_generation)` ของ `run_gt072*.sqlite3` · **teardown exit code + `AFTER listeners`** ⑯ path raw GAME log + console out/err ⑰ **คุณ Panya เห็นเองไหม** (ผลลบปิดได้เฉพาะเห็นเอง) ⑱ 🔴 **บรรทัด `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ในจดหมายผล** — ไม่มีบรรทัดนี้ = ผลยังเขียนลงคิวไม่ได้ ⑲ ถ้ามี session 2: ทุกข้อข้างบนแยกชุด **ห้ามรวมกับ session 1**)

---

### 🔴🔴 อ่านหลังจบการสังเกตเท่านั้น — ข้อสังเกตจากรอบสี่ของ `GT-030` (chief R169 · 2026-08-25 ~21:2x +07:00)

> **ห้ามอ่านบล็อกนี้ก่อนบันทึกผลของ `GT-072` เสร็จ** — วางไว้ท้ายใบโดยเจตนา เพราะมันเป็นข้อสังเกตที่ **ยังแยกสาเหตุไม่ได้**
> และการอ่านก่อนสังเกตจะชี้นำผู้เทส · 🔴 **ห้ามใช้ปิดใบนี้ไม่ว่ากรณีใด** — เป็นหลักฐานที่มา *ก่อน* ใบ ไม่ใช่ผลของใบ

**สองข้อเท็จจริง (แค่นี้ ไม่มีการตีความ):** จดหมาย `notes_to_chief\consumed\20260825_2010_*.md` §⑤

| ภาพ (`evidence_screens/`) | t | เห็นอะไร |
|---|---|---|
| `GT030R4_1162_NAVY_TARGETED_PANEL_HP100_NONAME_t354.5s.jpg` | 354.5 | NPC แมพตัวหนึ่งยืนอยู่ · ถูก target · แผงเป้าหมายเปิด `HP 100` `LV 1` |
| `GT030R4_1162_NAVY_AND_PANEL_BOTH_GONE_t356.5s.jpg` | 356.5 | มุมกล้องเดิม — ทั้งตัว NPC และแผงเป้าหมาย **ไม่อยู่แล้วทั้งคู่ในเฟรมหลัง** |

🔴🔴 **สี่ข้อที่ทำให้บล็อกนี้ *ไม่ใช่* หลักฐานเรื่องกลไก — `pf-adversary` จับได้ และ chief เห็นด้วยทั้งหมด:**

1. 🔴 **ห้ามเขียนว่า "หายพร้อมกัน" — ยังไม่ได้วัด** สองเฟรมห่างกัน **2.0 วินาที** = **60–120 เฟรมที่ไม่มีใครเปิดดู**
   **ไม่มีใครรู้ว่าอันไหนหายก่อน** และคำว่า "พร้อมกัน" คือคำที่แบกน้ำหนักทั้งหมดของการตีความ
2. 🔴🔴 **ในช่วง 2 วินาทีนั้นมีตัวก่อกวนที่รู้จักอยู่:** `RECV 0xAC52` (ทริกเกอร์แชต ascii-12) ลงที่ **`t = 355.40`**
   ⇒ **ผู้เทสกด Enter ในช่องแชตระหว่างสองเฟรมนั้นพอดี** · การเสียการเลือกเป้าเมื่อโฟกัสไปช่องแชต/กด Enter **เป็นพฤติกรรมปกติของไคลเอนต์**
3. 🔴 **ห้ามเขียนคำอธิบายกลไก** — ใบนี้ห้ามไว้เองแล้วในหัวข้อ *"สิ่งที่ใบนี้ไม่ได้ถาม"* ⇒ **ประโยค "ไคลเอนต์ทำลาย actor object ทิ้ง" ถูกถอนออกจากใบนี้แล้ว** (chief เคยเขียนไว้ในฉบับแรกของ R169 — ผิด ถอนแล้ว)
   **สิ่งอื่นที่ปิดแผงเป้าหมายได้ และยังไม่ถูกตัดออกสักข้อ:** โฟกัส/Enter ในแชต (เกิดขึ้นจริงในช่วงนั้น) · `Esc` หรือคลิกพื้นว่าง · range check ของการเลือก ·
   AOI/interest-management unload · LOD/streaming ปล่อย render proxy · actor เข้าสถานะตาย/ซ่อนแล้วล้างการเลือก · การเลือกใหม่ทับของเก่า · การใช้ actor-id ซ้ำโดย `SPAWN_BARE` ทำให้ handle ของแผงเป็นโมฆะ · NPC เดินเองตาม ambient AI
4. 🔴 **หลักฐานนี้ *เป็นกลาง* ระหว่าง `N1` (despawn) กับ `N2` (แทนที่)** — แถว `N2` ทำนายแผงที่ผูกค้างแล้วกลายเป็นโมฆะ **พอดีเป๊ะ**
   ⇒ **ห้ามอ่านว่า `N1` เป็นตัวเต็ง** · 🔴 **และห้ามลดน้ำหนัก `N3`/`N5`** — ฉบับแรกของ R169 เขียนว่าทั้งคู่ "อ่อนลงมาก" **ถอนแล้ว**
   โดยเฉพาะ **`N5` (NO-VANISH) ยังเป็นผลลบที่สะอาดและมีค่าเท่าผลบวกเหมือนเดิมทุกประการ** — ถ้ารอบนี้ NPC ไม่หาย **นั่นคือผลที่มีค่า ไม่ใช่ผลอ่อน**

🔴 **และตัว NPC เองก็ยังระบุตัวไม่ได้** — จดหมายเรียกมันว่า `Navy Transfer` แต่นั่นคือชื่อที่ยกมาจากรอบสาม
**[MEASURED · chief re-derive จาก `gamedata/scene/bg0001/bg0001.placements.tsv`]** จากพิกัดผู้เทสรอบสี่ `(-7775,-2531)`
placement ที่ใกล้ที่สุดคือ **`idx 1` `(-8013.5,-2780)` ที่ 344.8 หน่วย** ส่วน **`P0` `(-9140,-2780)` เป็นอันดับสามที่ 1,387.5 หน่วย (ไกลกว่า 4 เท่า)**
⇒ 🔴 **ถ้าร่างนั้นไม่ใช่ `P0` เรื่องเปลี่ยนทั้งหมด** — มันจะกลายเป็น NPC ที่อยู่ห่างจากพิกัดที่เราแตะ **345 หน่วย** แล้วหายไป
= แถว **`N6 SPAWN-WIDE-EFFECT`** ซึ่ง **ใหญ่กว่า**สิ่งที่ใบนี้ตั้งใจถาม · และจะทำให้ตัวคุม **`NC-3`** ของใบนี้เป็นโมฆะ
⇒ 🎯 **ด่านที่ถูกที่สุดที่ตอบข้อนี้: ดูว่าเฟรมของเลนแบกplacement ตัวไหนจริง หรือวัดความสูงพิกเซลของร่างเทียบโมเดลที่รู้ระยะในวิดีโอเดียวกัน**

---

### 🟡 ผล `GT-072` รอบแรก — **PARTIAL** (บันทึกโดย chief R170 · 2026-08-25 ~22:0x +07:00)

**ที่มา:** `notes_to_chief\consumed\20260825_2145_GT072-RESULT-occlusion-and-replace-both-fail-plus-Z0-over-water.md`
**จ็อบ 1167/1168/1169 · attended (คุณ Panya ขับ UI เอง) · `OBSERVER_CONFIRMED: 2026-08-25T21:4x+07:00`**
**ไม่แก้โค้ด ⇒ ไม่กินสล็อต** · DB สำเนา · CANON ตรงทั้งก่อนและหลัง · teardown exit 0 · วิดีโอ 698.8 วิ

**ชั้น wire/DB — ทำซ้ำเป็นครั้งที่สาม ตรงทุกหลัก:**

```
videostart               2026-08-25T21:20:52.265
RECV 0xAC52 (chat)       21:30:28.342   t = 576.08
SENT SPAWN_BARE          21:30:28.359   t = 576.09
SENT SPAWN_AVATAR        21:30:43.360   t = 591.10
SENT MOVE_A_1            21:30:58.359   t = 606.09
SENT MOVE_A_2            21:31:13.359   t = 621.09
SENT NEGATIVE_CONTROL    21:31:28.359   t = 636.09
```

**ชั้น client-observable — 🔴 ตารางสามค่าของใบ: ยังไม่มีค่าไหนถูกตัดออกเลย**

🔴🔴 **ฉบับแรกของบล็อกนี้ (chief R170) เขียนว่า "แทนที่ ❌ ตัดออกแล้ว" และ "บังทับ 🟡 ตัดออกได้ครึ่งเดียว" — `pf-adversary` หักล้างทั้งสองข้อ และ chief เห็นด้วยทั้งหมด ที่เขียนอยู่ตอนนี้คือฉบับแก้แล้ว**

**ไทม์ไลน์ที่หักล้าง — ประกอบจากตัวเลขในจดหมายฉบับเดียวกันทั้งหมด:**

| `t` (วิดีโอ) | เทียบ `T0` | เกิดอะไร |
|---|---|---|
| `576.09` | `+0` | `SPAWN_BARE` ออกสาย |
| `~576.7` | `+0.6` | **NPC `Navy Transfer` หายจากจอ** |
| `636.09` | `+60.0` | `NEGATIVE_CONTROL` ออกสาย |
| `636.5` | `+60.4` | **ศพ (actor ของเรา) หายจากจอ** — จดหมาย §④ |
| `658.6` | `+82.5` | `TargetPosVital` ใบแรก = **ผู้เทสเพิ่งเริ่มเดิน** |
| `668.9` | `+92.8` | เฟรม "พื้นว่างเปล่า" ที่เคยถูกใช้ตัด occlusion |

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

🔴 **ถอนข้ออ้างเรื่อง `ProbeControl03` ที่ chief เขียนไว้ในฉบับแรก:** ผู้เทสที่ `t=668.9` อยู่ `(-9,299, -2,537)` และ `ProbeControl03` อยู่แนว `X -9,289.957 · Y ≈ -2,780`
⇒ **ห่างกัน 243 หน่วย ตรงกันแค่แกน X แกนเดียว ไม่ใช่ "ทับพอดี"** · และใบ `GT-030-R3` สั่งให้ตรวจจุดนั้นด้วย **การหันกล้องไปทาง −X (`W5`)** ไม่ใช่ด้วยพิกัดที่ยืน
⇒ **`NC-2 / ProbeControl03` ยังค้างเหมือนเดิม ไม่ได้ถูกปิดในรอบนี้** (บรรทัดสารบัญที่ยังเขียนว่า "ยืนยันจากวิดีโอไม่ได้สองรอบติด" **ถูกแล้ว ห้ามแก้ตาม**)
🔴 **และระยะที่ฉบับแรกเขียนว่า "ห่าง `P0` 159 หน่วย" ก็ผิด** — `159` คือ `ΔX` ล้วน · ระยะจริง = **290.5 หน่วย** (`ΔY = 243`)

🔴 **ถอนคำที่เคยเขียนไว้ผิด (ผู้ช่วยแก้เอง ผู้เทสยืนยัน 21:3x):** จดหมาย `20260825_1900` §⑥ และ `20260825_2010` §⑥ เขียนว่า *"ต้อง double-click เท่านั้น คลิกเดียวไม่เปิดแผง"* — **ผิด ถอน** · **คลิกเดียวก็เปิดแผงได้**
**สิ่งที่ยังยืน:** `Tab` **เลือก actor ตัวนี้ไม่ได้** (ยืนยันซ้ำในรอบนี้ที่จุด `P0` ด้วย)

🆕 **ข้อสังเกตที่ chief แยกออกจากผลของใบนี้โดยเจตนา — `Z = 0.00` เหนือผืนน้ำ**
ผู้เทสตั้งใจเดินลงน้ำเอง: บนท่าเรือ `Z = 186.00` ตลอดรอบ · ที่ `(-10,086.56, -2,735.39)` และ `(-10,376.65, -2,799.60)` ไคลเอนต์ส่ง **`Z = 0.00`**
🔴 **ไม่ใช่ผลของ `GT-072`** และ nonclaims สี่ข้อของจดหมายยกมาทั้งดุ้น: ① เป็นค่าที่ **ไคลเอนต์ส่งมา** ใน `TargetPosVital` ไม่ได้บอกว่าเซิร์ฟเวอร์ควรส่งอะไรกลับ ② **แยกไม่ออกระหว่าง "ผิวน้ำอยู่ที่ Z=0 จริง" กับ "หาความสูงพื้นไม่เจอ ⇒ ตกค่าเริ่มต้น 0"** ③ **ไม่มีใคร spawn อะไรลงน้ำในรอบนี้** ⇒ คำถามเดิมของเจ้าของ (*"ของที่เกิดในน้ำจะเป็นยังไง"*) **ยังไม่ถูกตอบ** ④ จุดเดียว แมพเดียว รอบเดียว
⇒ เข้าเป็น **ข้อมูลตั้งต้น** ของใบเรื่องผืนน้ำ/พื้น (คู่กับใบ test-stage ในจดหมาย `20260825_2020`)

**หมายเหตุขั้นตอนที่ผู้ช่วยแก้เอง และ chief รับ:** ใบสั่งถ่ายภาพนิ่ง `PRE_C/L/R/C2` สี่ใบ → เปลี่ยนเป็น **ค้างมุมละ ~3 วิ แล้วดึงเฟรมจากวิดีโอ 30 fps ทีหลัง**
🟢 **chief รับ** — ลดการกดถ่ายมือซึ่งเป็นต้นเหตุ nonclaim *"ภาพ before/after ไม่ครบฟอร์ม"* ของ `GT-030` รอบสอง
🔴 **สองข้อที่ยังต้องคงไว้:** ① กล้องต้อง **เคย** หันไปทางนั้นและนิ่งพอ (วิดีโอย้อนได้เฉพาะสิ่งที่กล้องเคยเห็น) ② **สีป้ายชื่อยังต้องกดถ่ายเอง** (PLAYBOOK ข้อ 13 ห้ามอ่านสีจากวิดีโอที่ถูกบีบอัด)

---

## GT-074 OCCLUSION-CAMERA-ANGLE-CONTROL-001 [attended, in-game]: หลัง `SPAWN_BARE` ทับพิกัด `P0` — **NPC `Navy Transfer` โผล่กลับมาให้เห็นจากมุมกล้องอื่นหรือไม่** (ตัวคุมมุมกล้อง `W2` ที่รอบแรกของ `GT-072` ไม่ได้ทำ)  [🟢 **PENDING — attended · รันได้บน `main` ปัจจุบัน ไม่รอ merge ไม่รอ CI ไม่รอเจ้าของ · ศูนย์สล็อต** · เปิดใบโดย chief R170 (2026-08-25 ~22:2x +07:00 · session `2ilw5p`) ตามผลรอบแรกของ `GT-072` §② · เขียนใบโดย `pf-queue-author`]

> 🔢 **เรื่องเลขใบ:** ตัวนับเป็น **ชุดเดียวร่วมกับ `CLIENT_RE_QUEUE.md`** — prefix สองแบบ ตัวนับเดียว
> คำสั่งเปิดใบรอบนี้ระบุเลข **073** แต่ **grep ตอนเขียนใบพบว่า `073` ถูกใช้ไปแล้ว**: `RE-073 TEST-STAGE-GEOMETRY-SURVEY-001` เปิดโดย chief R169 (`CLIENT_RE_QUEUE.md` ~บรรทัด 2141)
> · `GT-073` = 0 hit · `RE-072` = 0 hit (072 ใช้โดย `GT-072` ใบเดียว) ⇒ **เลขว่างจริงคือ 074** ⇒ **ใบนี้คือ `GT-074`**
> 🔴 **ใบ static ของรอบเดียวกันนี้คือ `RE-075`** ⇒ **เลขว่างถัดไปคือ 076**
> 🔴 **ใบ `GT-030` · `GT-030-R3` · `GT-072` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ** — ใบนี้เป็นใบใหม่ที่ **ชี้ไปหา** พวกมัน ไม่ใช่ใบแทน

---

### ที่มา — **วัดมาแล้วทั้งหมดในรอบแรกของ `GT-072` (จ็อบ 1167/1168/1169) ห้าม re-derive ระหว่างรอบ**

จดหมายต้นทาง: `notes_to_chief\consumed\20260825_2145_GT072-RESULT-occlusion-and-replace-both-fail-plus-Z0-over-water.md`
(**`OBSERVER_CONFIRMED: 2026-08-25T21:4x+07:00`** — ผู้เทสยืนยันแล้ว)

🔴🔴 **อ่านบรรทัดนี้ก่อน:** ผลรอบแรกของ `GT-072` **ไม่ได้ตัดค่าไหนออกเลยสักค่า** — `pf-adversary` หักล้างฉบับแรกของบันทึกรอบ R170 และ chief เห็นด้วย · **ตัวคุมสองตัวที่เก็บมา ถูกวัดที่ `T0 + 92.8` วินาที ซึ่งเป็นเวลาหลังทั้ง NPC (`+0.6`) และ actor ของเราเอง (`+60.4`) หายจากจอไปแล้ว** ⇒ ทั้งสามสมมติฐานทำนายภาพเดียวกันหมด = **อำนาจแยกแยะเป็นศูนย์**

| ค่าในตารางของ `GT-072` | สถานะจริงหลังรอบแรก | เหตุผล |
|---|---|---|
| **แทนที่ (replace)** | 🟡 **ยังไม่ถูกตัด** | actor ของเราเองก็คลิก/`Tab` ไม่ติดอยู่แล้ว ⇒ "คลิกแล้วไม่มีอะไรถูกเลือก" คือผลที่ replace ทำนายไว้เป๊ะเช่นกัน · และคลิกเกิดหลังศพหายไป 32 วิ |
| **บังทับ (occlusion)** | 🟡 **ยังไม่ถูกตัดแม้แต่ครึ่งเดียว** | เฟรมพื้นว่างถ่ายตอนโมเดลของเราไม่อยู่ในฉากแล้ว ⇒ ตัวที่ถูกกล่าวหาว่าบัง ไม่มีอยู่ตอนวัด · มุมกล้อง (`W2`) ก็ไม่ได้ทำ |
| **despawn** | 🟡 **ยังไม่ถูกยืนยัน** | *"คลิกไม่ติด ไม่เท่ากับ ไม่มีอะไรอยู่ตรงนั้น"* — และประโยคนี้ใช้กับแถว "แทนที่" ได้เท่ากันทุกตัวอักษร |

- 🔴 **สาเหตุที่ตัวคุมทั้งหมดหายไปพร้อมกัน:** ผู้เทส **ยืนนิ่งทั้งสวีป** — ล็อกยืนยันเอง: **`TargetPosVital` ใบแรกหลังทริกเกอร์อยู่ที่ `t = 658.6` = `T0 + 82.5` วินาที** ⇒ `W1`–`W5` ไม่มีอะไรถูกเดินเลย (`W2` มุมกล้อง · `W3` เข้าไปใกล้+คลิก · `POST-A` ยืนทับ `P0` — **ขาดทั้งสามตัว**)
- ⇒ ตอนนี้ **ห้ามใครเขียนว่า "การเปลี่ยนมุมกล้อง/การเข้าไปใกล้ไม่ทำให้ NPC โผล่กลับมา"** — เขียนได้แค่ **"ไม่ได้ตรวจในหน้าต่างที่มีความหมาย"**
- 🔴🔴 **กติกาที่ใบนี้เกิดมาเพื่อบังคับ: ตัวคุมต้องถูกเดิน *ขณะที่ของที่ต้องแยกแยะยังอยู่บนจอ*** — นั่นคือช่วง `T0 + 0.6` ถึง `T0 + 60` (ก่อน `NEGATIVE_CONTROL` เก็บ actor ของเราไป) · **นอกหน้าต่างนี้ ผลลบไม่ใช่ผลลบ มันคือการวัดฉากที่ว่างอยู่แล้ว**
- **ทำซ้ำแล้วสามรอบติด ตัวเลขเดียวกัน** (`SPAWN_BARE` → `SPAWN_AVATAR` → `MOVE_A_1` → `MOVE_A_2` → `NEGATIVE_CONTROL` ห่างกัน 15.0 วิ) ⇒ **รอบนี้ไม่ต้องพิสูจน์การหายซ้ำอีก มันเป็นแค่ฉากหลัง**

---

### objective (claim เดียว)

**หลัง `SPAWN_BARE` ทับพิกัด `P0` แล้ว — เมื่อผู้เทส *เปลี่ยนมุมกล้องอย่างเดียว โดยตัวละครยืนจุดเดิมเป๊ะ* NPC `Navy Transfer` โผล่กลับมาให้เห็นหรือไม่**

**ตัวหักล้าง (falsifier) — มีตัวเดียวและเขียนไว้ก่อนบูต:**
> 🔴 **"NPC โผล่กลับมาที่ `P0` เมื่อมองจากมุมกล้องอื่น"** ⇒ **"บังทับ (occlusion)" กลับขึ้นโต๊ะทันที และ `despawn` ยังไม่ถูกตั้งขึ้นเลย** ⇒ ต้องแก้ถ้อยคำผลรอบแรกของ `GT-072` และ **รายงานเสียงดัง ห้ามกลบให้เรียบ**

### 🔴 ทำไมนี่คือ claim เดียว ไม่ใช่การรัน `GT-072` ซ้ำ

`GT-072` ถามสามค่า (`despawn` / `แทนที่` / `บังทับ`) จากการวัดชุดเดียว — **สองค่าถูกตัดออกด้วยการวัดไปแล้ว** ⇒ สิ่งที่เหลือคือ **ตัวคุมตัวเดียวที่ยังไม่มีข้อมูล** = มุมกล้อง
ใบนี้จึงพิสูจน์ **ข้ออ้างเดียว: "การหายไม่ใช่ผลของแนวสายตา"** · ทุกอย่างที่เกินจากนี้ในรอบนี้เป็น **ข้อสังเกตฟรี ไม่ใช่ผลของใบ**

🔴 **สิ่งที่ใบนี้ไม่ได้ถาม:** อะไรในไคลเอนต์ทำให้เกิดผลนี้ (ช่อง actor / id / hash ตำแหน่ง / ลำดับ list) — **ไม่มีหลักฐาน static แม้แต่บรรทัดเดียวในโปรเจกต์** ⇒ **ห้ามเขียนคำอธิบายกลไกลงในผลไม่ว่ากรณีใด**

---

### 🟢 งบเวอร์ชัน — **ศูนย์สล็อต** · และ **ไม่รอ merge**

- ใบนี้ **ไม่แก้โค้ด ไม่แก้ scenario ไม่แก้ mask ไม่แก้ไบต์ ไม่แก้พิกัด แม้ตัวอักษรเดียว** — บูตเลนเดิมที่รอบแรกของ `GT-072` เพิ่งบูตเมื่อ 2026-08-25 21:2x ⇒ **ไม่เพิ่ม tracked version ⇒ ไม่กินสล็อต** (`HYP-PF-025` = 2/5 คงเดิม · ผู้เทส **ห้ามแก้ ledger** ไม่ว่าผลจะออกแถวไหน)
- เลน `HYP-PF-025` + flag + scenario **ship อยู่บน `main` แล้ว** ⇒ **ไม่ต้องรอ PR ไม่ต้องรอ branch ไม่ต้องรอคำเคาะเจ้าของ**
- 🔴 **ถ้าใครระหว่างรอบคิดจะขยับพิกัด/ไบต์ "เพื่อลองดู" — นั่นคือ wire change · กินสล็อต · ห้ามเด็ดขาดในรอบนี้**
- 🔴 **แต่ยังต้องรัน `pf_resolve_green_boot.py` และด่านก่อนบูตทุกครั้งตามปกติ** — "เครื่องมือชนะใบเสมอ"

### ⏱️ งบเวลาผู้เทส — **~3 นาทีบนจอ** (ไม่รวมบูต/teardown)

เดินไป landmark → ตั้งมุมสามมุม → พิมพ์ทริกเกอร์ 12 ตัว → **หมุนกล้องอย่างเดียว** → ยืนดูจนถึง `+70` → จบ
🔴 **ไม่ต้องเดินหลังทริกเกอร์ · ไม่ต้องคลิกเป้า · ไม่ต้องกด `Tab` · ไม่ต้องเดินไป `Sebastian`/`B`/`C`** — ทั้งหมดนั้นรอบแรกทำไปแล้ว

---

### db (สำเนาเสมอ — **canonical ไม่ถูกเปิดตลอดรอบ**)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-074_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt074.sqlite3
```
- เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง**
- เลนนี้ `persisted_post_state.database_write = "none"` ⇒ row-diff ต่างได้เฉพาะ `sessions` **+1 แถวต่อการเข้าเกมหนึ่งครั้ง** (`count(*) WHERE selected_character_id IS NOT NULL`) · จด `max(lease_generation)` ก่อน-หลัง **ห้ามถอยหลัง**
- 🔴 **สำเนาใหม่ทุกบูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกครั้ง** — เผื่อเวลาเดินไป landmark ไว้เสมอ (นี่คือส่วนที่กินเวลาที่สุดของรอบ)
- ถ้าเปิด session 2: สำเนาใหม่ `state\run_gt074b.sqlite3` (**ห้ามใช้ไฟล์เดิมซ้ำ**)

### 🔴 ก่อนบูต — resolve commit เขียว (รันเครื่องมือ ห้ามก๊อป SHA เก่า)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` · **exit 3** ⇒ **ห้ามบูต** ใบอยู่ PENDING ต่อ · **exit 2** = พาธผิด/git ล้ม
- **ยืนยันหกข้อกับ `<SHA>` ที่จะบูตจริง — เหมือนบล็อกของ `GT-072` ทุกบรรทัด** (single quote เท่านั้น · **ห้าม `| grep` / `awk`**):
```
git show origin/ci-status:ci/<SHA>.json
git grep -n 'remote-player-hypothesis-scenario' <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/remote_player_hypothesis_visibility_probe.json && echo SCENARIO_PRESENT
git grep -n 'HYP_PF_025_REMOTE_PLAYER_' <SHA> -- src/pirateforce_foundation/ scenarios/
git grep -n 'classify_chat_input_attempt' <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n 'export-events' <SHA> -- src/pirateforce_foundation/app.py
```
- **อ่านค่า pin ต่อเฟรมจาก scenario ของ commit ที่บูต ห้ามฝัง sha จากความจำ** · 🔴 `SPAWN_AVATAR` พินเฉพาะโครง `pc_skeleton_sha256` 172 B
- ไม่ครบหกข้อ + ยังไม่ได้ค่า pin = **ห้ามบูต**

### server args (เป๊ะ · opt-in เท่านั้น · `production_allowed=false`)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt074.sqlite3 --remote-player-hypothesis-scenario scenarios\remote_player_hypothesis_visibility_probe.json --export-events
```
- 🔴 **ห้ามใส่ flag hypothesis ตัวอื่นแม้แต่ตัวเดียว** — บูตนี้ต้องเป็น **หนึ่งเลน**
- console label = `HYP_PF_025_REMOTE_PLAYER_<STEP>` · **เห็นชื่ออื่น = บูตผิดไฟล์ หยุด ปิด server ห้ามอ่านจอเป็นผล**
- **one-shot ต่อ GAME connection** ⇒ บูตใหม่ = รีอาร์ม · 🔴 **reconnect กลางรอบ = รอบนั้นเสียการเทียบ จดทันที**

### 🔴 ตัว trigger แชต — printable ASCII **12 ตัวเป๊ะ**
- ใช้ **`PFCHATPROBE1`** (P-F-C-H-A-T-P-R-O-B-E-1 = **12 ตัวพอดี** · สตริงเดียวกับสามรอบก่อน ⇒ ไบต์ขาเข้าไม่มีตัวแปรใหม่)
- 🔴 **สั้น/ยาวกว่า 12 = ถึงเซิร์ฟเวอร์แต่เงื่อนไขเงียบ ๆ ไม่ผ่าน ไม่มี error — sweep ไม่ออกเฉย ๆ**
- 🔴 **คลิกช่องแชตให้โฟกัสก่อนพิมพ์เสมอ** — ตัวอักษรที่พิมพ์ตอนช่องแชตไม่โฟกัส **กลายเป็นฮอตคีย์**
- `Return` **หนึ่งครั้ง** · **หลัง Enter ห้ามพิมพ์ตัวอักษรใด ๆ อีกทั้งรอบ**
- 🔴 **ห้ามพิมพ์แชตเป็นขั้นแรกของรอบ** — sweep จะยิงตั้งแต่ยังยืนจุดเกิด และ one-shot ไหม้ทั้งรอบ ⇒ **เดินไป landmark + ตั้งสามมุมให้ครบก่อนเสมอ**

### 🔴🔴 ท่ากล้อง ทิศหัน และการเดิน — **หัวใจของใบนี้ อ่านให้จบก่อนแตะเมาส์**

| ท่า | ทำอะไรจริง | ยิง `TargetPosVital` ไหม | ใบนี้ใช้ได้เมื่อไร |
|---|---|---|---|
| **คลิกขวาค้างลากเมาส์** | หมุน **มุมกล้อง** อย่างเดียว · **ทิศหันของตัวละครไม่ขยับ ไม่มีอะไร trigger** | 🟢 ไม่ยิง | ✅ **นี่คือท่าเดียวที่ใบนี้ต้องการ** · ปลอดภัยทุกจังหวะ · **และเป็นตัวเช็ค NO-CRASH ของใบนี้** · ❌ ยกเว้น `W1` ซึ่งห้ามแตะด้วยเหตุผลเรื่องกรอบภาพ ไม่ใช่เรื่องสาย |
| **`Q` / `E`** | **หันตัวละคร** กล้องแพนตาม | 🔴 ยิง | ❌ **ห้ามใช้ตลอดรอบ** · 🔴 **ห้ามใช้เป็นตัวเช็ค NO-CRASH เด็ดขาด** |
| **`W/A/S/D`** | เดิน (เปลี่ยนทั้งตำแหน่งและทิศหัน) | 🔴 ยิง | ✅ ใช้ได้เฉพาะ **ก่อน `T0`** (เดินไป landmark) และ **หลัง `+70`** · ❌ **ห้ามเด็ดขาดระหว่าง `T0` ถึง `+70`** — การเดินหนึ่งก้าวทำให้คู่ภาพ `PRE_L↔POST_L` ใช้ไม่ได้ = รอบเสีย |
| **ล้อเมาส์ (ซูม)** | ซูมกล้อง | **[UNKNOWN — ไม่มีใครเคยวัด]** | ใช้ได้เฉพาะขั้นซูมก่อน `T0` · **จดเวลาที่ซูมทุกครั้ง** · ❌ ห้ามแตะล้ออีกจนจบ `+70` |

🔴 **ประโยคเดียวที่ต้องจำ: ตัวที่ยิง `TargetPosVital` คือ "การเปลี่ยนทิศหันของตัวละคร" ไม่ใช่ "การขยับกล้อง"**
🔴 **เหตุผลที่ห้ามเดินหลัง `T0` เป็นเรื่องหลักฐาน ไม่ใช่เรื่องไบต์:** เกณฑ์ชี้ขาดคือ **"ตัวละครยืนจุดเดียวกันเป๊ะ เปลี่ยนแค่มุมกล้อง"** — ขยับเมื่อไร ตัวคุมมุมกล้องก็ปนกับตัวคุมระยะทันที และรอบนี้ก็ไม่ได้ตอบอะไรที่รอบแรกยังไม่ตอบ

### 📸 กติกาภาพนิ่งของรอบนี้ (**กฎยืนจากจดหมายผล `GT-072` §⑥ — ทวนคำต่อคำ**)
- **ภาพนิ่งทั่วไปดึงจากวิดีโอ 30 fps ทีหลัง — ผู้เทส *ไม่ต้อง* กดปุ่มถ่ายภาพ** (คีย์ในหน้าต่างเกม = ฮอตคีย์ · และการถ่ายมือคือที่มาของ nonclaim "ภาพ before/after ไม่ครบฟอร์ม" ของ `GT-030` รอบสอง)
- 🔴 **แต่กล้องต้อง *เคย* หันไปทางนั้นจริง และต้อง *ค้างนิ่งนานพอ*** — **วิดีโอย้อนได้เฉพาะสิ่งที่กล้องเคยเห็น** ⇒ ทุกมุมของใบนี้ **ค้างนิ่งอย่างน้อย 4 วินาที** (≈120 เฟรม)
- 🔴 **ข้อยกเว้นข้อเดียวที่ยังต้องถ่ายภาพจริง: สีป้ายชื่อ** (วิดีโอถูกบีบอัด · **PLAYBOOK ข้อ 13 ห้ามอ่านสีจากวิดีโอ/ภาพย่อ/contact sheet**) ⇒ ถ่าย full-res **ด้วยเครื่องมือนอกเกม** สองครั้ง: **ก่อน `T0`** (มี NPC ในเฟรม) และ **หลัง `+70`** · 🔴 **ห้ามกดคีย์ใด ๆ ในหน้าต่างเกมเพื่อถ่ายภาพ**

---

### ⏱️ ไทม์ไลน์ของรอบ — **เวลาเป็นวินาทีนับจาก `T0`** (`T0` = **เฟรมที่ช่อง input ของแชตเคลียร์** 🔴 ไม่ใช่เฟรมที่ตัวอักษรโผล่ · เผื่อคลาด ±2 วิ · หลุดจังหวะให้จดเวลาจริง **ห้ามแต่งผล วิดีโอคือกรรมการ**)

| หน้าต่าง | เวลา | เฟรมของเลนที่ตกในช่วงนี้ | ผู้เทสทำอะไร |
|---|---|---|---|
| **PRE** | ก่อน `T0` | — | เดินไปยืนห่าง `P0` ~200-300 หน่วย · ซูม · ตั้ง **CAM-C → CAM-L → CAM-R → กลับ CAM-C** ค้างมุมละ **4 วิ** · ถ่ายภาพสีป้าย full-res · จดจุดอ้างอิงบนฉากของแต่ละมุม |
| **W1** | `T0` → `+10` | `SPAWN_BARE` (~+0) | 🔴 **ห้ามแตะเมาส์และคีย์บอร์ดเลย แม้แต่คลิกขวาลาก** ยืนนิ่ง มองจอ |
| **W2** 🎯 | `+10` → `+29` | — | 🎯 **หัวใจของใบ — คลิกขวาลากอย่างเดียว:** CAM-L (ค้าง 4 วิ) → CAM-R (ค้าง 4 วิ) → กลับ CAM-C (ค้าง 4 วิ) |
| **W3** | `+29` → `+70` | `MOVE_A_1` (~+30) · `MOVE_A_2` (~+45) · `NEGATIVE_CONTROL` (~+60) | ยืนนิ่งที่ CAM-C ให้ `P0` อยู่ในเฟรม เฝ้าดูเฉย ๆ (**ข้อสังเกตฟรี ไม่ใช่ claim ของใบ**) |

🔴 **`W2` ของใบนี้กว้างกว่าของ `GT-072` (ซึ่งเขียนไว้ `+10..+20`) โดยตั้งใจ** — เพราะสามมุม × ค้าง 4 วิ + เวลาลากเมาส์ ไม่มีทางลงตัวใน 10 วินาที และ **การค้างนิ่งคือสิ่งเดียวที่ทำให้ดึงเฟรมจากวิดีโอได้** · ยังจบก่อน `MOVE_A_1` (~+30) พอดี

---

### steps (คลิกต่อคลิก)

**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด **boot stamp (+07:00)** · preflight จอว่าง (`staged\TEMPLATE_preflight_unattended.ps1` — เจอหน้าต่าง elevated = ABORT ทั้งรอบ) · เทียบ sha canonical · copy DB สองใบตามบล็อก db
**เตรียม teardown:** ก๊อปจาก **`TEMPLATE_teardown_generic.ps1`** เป็นหลัก · ถ้าก๊อปจากจ็อบที่เป็นตัวเลข **ต้องเปิดดูบรรทัดที่ 17 ให้เห็น `-replace '\\','/'` ก่อนเสมอ** · 🔴 **ห้ามก๊อปจาก `1103`/`1105`**

1. **สตาร์ตเซิร์ฟเวอร์ก่อน แล้วค่อยบูต client เสมอ** (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client)
   - 🔴 client ที่บูตโดยไม่มีเซิร์ฟเวอร์ **ตายเองใน ~3.5 นาที**
   - 🔴 **ถ้าต้องฆ่า client กลางคัน ต้อง restart server ก่อนเปิด client ตัวใหม่เสมอ** (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่ "connecting" ตลอดกาล)
   - จัดหน้าต่าง console ให้เห็นข้างจอเกมโดยไม่บังพื้นที่วัด · **ตลอดรอบห้ามคลิก console**
2. เปิด client → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร → **เลือกช่องแรก** → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (🔴 **ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด**)
3. เข้าแมพ เห็น HP/minimap/ชื่อแมพ → **เริ่มอัดวิดีโอต่อเนื่องตรงนี้ ยาวจนจบ session** (`staged\TEMPLATE_video_recorder.ps1 -FrameRate 30` ลง `evidence_video\`) · จดบรรทัด `VIDEO START pid= start= fps= path=` (🔴 `start=` **ห้ามใช้เป็นสมอเวลา**) · 🔴 **ไม่ได้อัด = NO-RESULT ทันที**
4. **เดินไปหา NPC `Navy Transfer`** (`P0` X `-9139.957` Y `-2780.045` Z `223.292`) — **ยืนห่าง ~200-300 หน่วย ฝั่งที่มองเห็นตัวเต็ม ๆ** (รอบ R3 ยืนที่ `(-8876,-2715)` = ห่าง `271.9` และเห็นชัด — ใช้เป็นตัวอ้างอิงได้) · **จด X/Y จาก HUD** 🔴 **นี่คือการเดินครั้งสุดท้ายของรอบจนถึง `+70`**
5. **ซูมด้วยล้อเมาส์** จนเห็น `P0` เต็มตัวและเห็นพื้นรอบ ๆ อีกราว 200 หน่วย · **จดเวลาและระดับซูม** · 🔴 **หลังขั้นนี้ห้ามแตะล้ออีกจนจบ `+70`**
6. **ตั้ง `CAM-C` ด้วยคลิกขวาค้างลากเมาส์** ให้ `P0` อยู่กลางเฟรม → **ค้างนิ่ง 4 วินาที** (นับออกเสียง) → **พูดออกเสียงว่า "CAM-C"** เพื่อให้มีสมอในไฟล์เสียง/วิดีโอ
7. **คลิกขวาลากไป `CAM-L` (~45° ทางซ้าย)** → **ค้าง 4 วิ พูดว่า "CAM-L"** → **`CAM-R` (~45° ทางขวา)** → **ค้าง 4 วิ พูดว่า "CAM-R"** → **กลับ `CAM-C`** → **ค้าง 4 วิ พูดว่า "CAM-C2"**
   - 🔴🔴 **จดจุดอ้างอิงบนฉากของแต่ละมุมลงกระดาษ** (ภูเขา/อาคาร/เสาท่าเรือ/เส้นขอบฟ้า) — **`W2` ต้องกลับมาที่สามมุมนี้ให้ใกล้เคียงที่สุด และจุดอ้างอิงนี้คือสิ่งที่พิสูจน์ว่ามุมหลังตรงกับมุมก่อน**
   - 🔴 ห้ามแตะคีย์บอร์ดและล้อเมาส์ในขั้นนี้
8. **ถ่ายภาพนิ่ง full-res ด้วยเครื่องมือนอกเกม 1 ใบ ที่ `CAM-C`** → `GT074_PRE_LABELS_FULLRES_<yyyyMMdd_HHmmss>.png` — 🔴 **ใบนี้มีไว้เพื่ออ่าน *สี* ป้ายชื่อเท่านั้น** (NPC ต้องอยู่ในเฟรม) · **ถ้าอ่านชื่อบนป้ายลอยหัวออก ให้จดตัวอักษรที่อ่านได้ด้วย** — นั่นคือสิ่งเดียวที่ทำให้รอบนี้ระบุตัว NPC ด้วยชื่อได้โดยไม่ต้องคลิก
   - 🔴 **ห้ามคลิกที่ตัว NPC · ห้ามกด `Tab` · ห้ามกดปุ่มโจมตี** — "แทนที่" ถูกตัดออกไปแล้วในรอบแรก รอบนี้ไม่ต้องทำซ้ำ และการคลิกอาจทำให้ตัวละครขยับ
9. 🔴 **ยิงทริกเกอร์ = clapper (ครั้งเดียวของทั้งรอบ):** คลิกช่องแชตให้โฟกัส → พิมพ์ **`PFCHATPROBE1`** → **`Return` หนึ่งครั้ง** → **คลิกพื้นว่างไกล ๆ เพื่อปลดโฟกัสแชต** → **มือออกจากคีย์บอร์ด**
   - **จดทันทีสองอย่าง:** (i) **เฟรมที่ช่อง input เคลียร์ = `T0`** (ii) **บรรทัดแชตปรากฏในหน้าต่างแชตบนจอหรือไม่**
   - 🟢 **การคลิกพื้นว่างท่านี้ปลอดภัย มีหลักฐาน:** รอบแรกทำท่าเดียวกันแล้ว **ไม่มี `TargetPosVital` ออกสายอีก 82.5 วินาที** ⇒ คลิกนี้ไม่ทำให้ตัวละครขยับ · 🔴 **แต่ยังต้องจดเวลาคลิกทุกครั้ง** (ไม่มีใครเคยวัดว่าคลิกซ้ายยิงไบต์อะไร)
10. **W1 (`T0` → `+10`): ห้ามแตะเมาส์และคีย์บอร์ดเลย** — ยืนนิ่ง ตาอยู่ที่จอ · **พูดออกเสียงทันทีที่เห็นอะไรเปลี่ยน** · **อย่าพยายามถ่ายให้ทันเหตุการณ์ วิดีโอคือกรรมการ**
11. 🎯 **W2 (`+10` → `+29`) — ขั้นที่ทั้งใบนี้มีอยู่เพื่อมัน · คลิกขวาค้างลากเมาส์อย่างเดียว:**
    - `+10`→`+13` ลากไป **`CAM-L`** (มุมเดิมกับ PRE ใช้จุดอ้างอิงบนกระดาษ) → **`+13`→`+17` ปล่อยเมาส์ ค้างนิ่งสนิท 4 วินาที พูดว่า "POST CAM-L"**
    - `+17`→`+19` ลากไป **`CAM-R`** → **`+19`→`+23` ค้างนิ่ง 4 วินาที พูดว่า "POST CAM-R"**
    - `+23`→`+25` ลากกลับ **`CAM-C`** → **`+25`→`+29` ค้างนิ่ง 4 วินาที พูดว่า "POST CAM-C"**
    - 🔴🔴 **ห้ามแตะ `W/A/S/D` · `Q/E` · ล้อเมาส์ · ห้ามคลิกซ้าย** — ตำแหน่งและทิศหันของตัวละครต้องเท่าเดิมกับตอน PRE เป๊ะ **มิฉะนั้นคู่ `PRE_L↔POST_L` / `PRE_R↔POST_R` ใช้ไม่ได้ และรอบนี้ก็ไม่มีอะไรเหลือ**
    - 🔴 **ถ้ามุมไหนลากพลาด/เลยไป ให้ค้างที่มุมที่ได้จริงให้ครบ 4 วิ แล้วพูดออกเสียงว่า "มุมนี้เพี้ยน"** — **ห้ามลากไปลากมาแก้** (การลากซ้ำ ๆ ทำให้ไม่มีช่วงนิ่งให้ดึงเฟรม)
12. **W3 (`+29` → `+70`): ยืนนิ่งที่ `CAM-C` ให้ `P0` อยู่ในเฟรม** — เฝ้าดูเฉย ๆ ว่ามีอะไรกลับมาที่ `P0` ตอน `MOVE_A_1` (~+30) / `MOVE_A_2` (~+45) / `NEGATIVE_CONTROL` (~+60) ไหม
    - 🔴 **นี่เป็นข้อสังเกตฟรี ไม่ใช่ claim ของใบนี้** — แต่ **ถ้ามีอะไรกลับมา ให้จดเวลาให้ละเอียดที่สุดและรายงานเสียงดัง ห้ามกลบให้เรียบ**
    - ⛔ **เกณฑ์หยุดทั้งเลน:** ชื่อ **`ProbeControl03`** โผล่ที่ไหนก็ตาม (ป้ายหรือพาเนล) ⇒ **หยุด เก็บ console ทั้งไฟล์ รายงานทันที**
13. **POST (`+70` เป็นต้นไป):** ถ่ายภาพนิ่ง full-res ใบที่สองที่ `CAM-C` → `GT074_POST_LABELS_FULLRES_<yyyyMMdd_HHmmss>.png` (สำหรับตารางสีป้าย — **ถ้าไม่มีป้ายใดในเฟรมเลย ให้เขียนคำว่า "ไม่มี" ออกมาเป็นตัวอักษร**) · จบรอบได้ทันที
14. **NO-CRASH / CRASH:** **คลิกขวาค้างลากเมาส์แล้วกล้องหมุน = NO-CRASH** · หลุด/ค้าง = CRASH + จดว่าหลังเฟรมไหน · 🔴 **ห้ามใช้ `Q`/`E` เป็นตัวเช็ค** (มันยิงไบต์ออกสาย)
15. ออกจากเกม: **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย → **หยุดวิดีโอ** → **ปิดเซิร์ฟเวอร์ด้วย**
16. เก็บ **raw GAME log ทั้งไฟล์** (`...\capture_v141\GAME_LIVE.txt`) + console out/err ทั้งหมด (ทุกบรรทัด `[G>]` / `PF-EVENT` / `ErrorData`) → `PRAGMA integrity_check;` บนสำเนาทุกใบ → sha256 ทุกไฟล์
17. **teardown เสมอ** — แม้รอบจบเพราะเลิกเล่น ไม่ใช่เพราะเทสจบ → เทียบ sha canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม
18. **หลังรอบ — แตกเฟรม (ห้ามข้าม · 🔴 ห้ามมี `scale=` ในบรรทัดคำสั่งเด็ดขาด):**
```
$mkv = '<path full of the FULLROUND .mkv>'
ffmpeg -ss <T0 + 8.00> -i $mkv -t 24.00 -vsync 0 GT074_W2_%03d.png
ffmpeg -ss <T0 - 30.00> -i $mkv -t 30.00 -vsync 0 GT074_PRE_%03d.png
```
    - ดึงเป็นภาพนิ่ง **full-res จากต้นฉบับโดยตรง** หกใบ (มุมละคู่): `GT074_<job>_PRE_L_t<t>s.jpg` / `POST_L` · `PRE_R` / `POST_R` · `PRE_C2` / `POST_C`
    - + **crop PNG ไม่สูญเสีย ค่ากรอบเดียวกันเป๊ะทั้งคู่ของแต่ละมุม** · **จดค่ากรอบ crop ลงผล**
    - 🔴 **รายงานช่วงเวลาที่กล้อง *นิ่งจริง* ของแต่ละมุม POST เป็น `[t_เริ่ม, t_จบ]` และจำนวนเฟรม** — **สั้นกว่า 3.0 วิ ⇒ มุมนั้น "ค้างไม่พอ ⇒ เทียบไม่ได้" เขียนออกมาเป็นตัวอักษร ห้ามฝืนใช้**
19. 🔴🔴 **G-OBS — ขั้นสุดท้าย บังคับ:** ก่อนเขียนผลลงคิว/จดหมาย **ผู้ช่วยต้องทวนรายการ "สิ่งที่ผู้ช่วยเห็น" ให้ผู้เทสยืนยันทีละข้อ** (NPC ในภาพ PRE ทั้งสามมุม · มุม POST ทั้งสามมุมเห็น/ไม่เห็นอะไร · จุดอ้างอิงบนฉากตรงกันไหม · เดินหรือไม่เดิน · สิ่งที่เกิด/ไม่เกิดที่ `+30`/`+45`/`+60` · **สีป้ายทุกป้าย**)
    - ผู้เทสตอบเป็นคำเดียวต่อข้อ: **"ตรง" / "ไม่ตรง" / "ฉันไม่ได้ดูข้อนั้น"**
    - จดหมายผลต้องมีบรรทัดนี้ตัวอักษรเป๊ะ: `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`
    - 🔴 **ยังไม่ยืนยัน = ห้ามเขียนผลลงคิว** · 🔴 **บรรทัดนี้เป็น "ขั้นตอน" ไม่ใช่ "หลักฐาน" ห้ามใช้แทนเกณฑ์ผ่านชั้นใดชั้นหนึ่ง**

**SESSION 2 — 🔴 บังคับถ้าเวลาเหลือ และมันคือของที่ `GT-072` ค้างไว้จริง ๆ (ไม่ใช่การทำ session 1 ซ้ำ):**
ออกจากเกมให้สวย → **ปิด server ด้วยเสมอ** → copy DB ใหม่ (`run_gt074b.sqlite3`) → บูต server (args เดิม เปลี่ยน `--db`) → ทำข้อ 2-9 เหมือนเดิม **แต่หลัง `T0` เดินตามนี้แทน:**

| หน้าต่าง | เวลา | ทำอะไร |
|---|---|---|
| `T0` → `+25` | — | ยืนนิ่ง มองจอ (ไม่ต้องหมุนกล้อง — session 1 ทำไปแล้ว) |
| **`+25` → `+50`** 🎯 | **นี่คือตัวคุมที่ `GT-072` ขาด** | **เดินเข้าไปที่ `P0` ให้ถึงระยะประชิด แล้วคลิกซ้าย + กด `Tab` ที่จุดนั้น** · จด **เวลาทุกคลิกทุกก้าว** |
| `+50` → `+60` | — | ยืนที่ `P0` ให้กล้องเห็นพื้นตรงนั้น **ก่อน `NEGATIVE_CONTROL` (~`+60`) จะเก็บ actor ของเราไป** |
| หลัง `+60` | — | ทำซ้ำการคลิก/`Tab` ที่จุดเดิมอีกครั้ง **เพื่อเป็นตัวเทียบว่า "หลังศพหาย" หน้าตาต่างจาก "ก่อนศพหาย" หรือไม่** |

🔴🔴 **เหตุผลทั้งหมดของ session 2 อยู่ในบรรทัดเดียว: ตัวคุมของ `GT-072` ถูกเก็บที่ `+92.8` ซึ่งสายเกินไป 32 วินาที** ⇒ ครั้งนี้ต้องเก็บ **ก่อน `+60`**
🔴 session 2 **ยิง `TargetPosVital` แน่นอน (เพราะต้องเดิน)** ⇒ **เกณฑ์ "`TargetPosVital` = 0" ใช้กับ session 1 เท่านั้น ห้ามเอามาตัดสิน session 2**
🔴 **หลักฐานของสอง session แยกกันเด็ดขาด ห้ามรวมภาพ ห้ามรวมคำตัดสิน**

### 🔴 ลำดับข้ามใบ
- **ต้องรัน `GT-074` ให้จบ *ก่อน* `GT-032`** — `GT-032` ทำให้ landmark `0x2001` (`Navy Transfer`) ขึ้นศัตรู แล้วมันจะใช้เป็นจุดอ้างอิงกลาง ๆ ไม่ได้อีก
- **ห้ามพ่วงใบอื่นเข้าบูตนี้** — ชุดเลนของบูตนี้ต้องเป็นหนึ่งเลน

---

### คำทำนาย (**คำทำนายคือคำทำนาย · คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว** · ท่องก่อนบูต)

- **P1 [คำทำนาย]** NPC `Navy Transfer` **หายจากจอภายในไม่กี่วินาทีหลัง `T0`** (ทำซ้ำครั้งที่สี่)
- **P2 [คำทำนาย · ข้อหลักของใบ]** จาก `CAM-L` และ `CAM-R` ใน `W2` **ก็ยังไม่เห็น NPC** ⇒ **ตัดทางหนีสุดท้ายของ "บังทับ"**
- **P3 [คำทำนาย · ชั้น wire]** **ไม่มี `TargetPosVital` เลยแม้แต่ใบเดียวในช่วง `[T0, T0+70]`** (รอบแรกได้ใบแรกที่ `+82.5`)
- **P4 [คำทำนาย]** ไม่มีอะไรกลับมาที่ `P0` ตอน `+30` / `+45` / `+60`
- **P5 [คำทำนาย · จดสีอย่างเดียว ห้ามสรุปสาเหตุ]** ป้ายชื่อ NPC ในภาพ PRE เป็น **เหลือง** ตามภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับ
- **P6 [คำทำนาย · ถ้าผิดคือเรื่องใหญ่ที่สุดของรอบ]** ไม่มีมุมไหนทำให้ NPC โผล่กลับมา — **ถ้าโผล่ = falsifier ⇒ "บังทับ" กลับขึ้นโต๊ะ ⇒ รายงานเสียงดังทันที**

---

### pass criteria — **สองชั้น แยกกันเด็ดขาด 🔴 ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

**ชั้น (1) wire/DB + หลักฐานเชิงไฟล์ — ทำ headless ได้ ไม่ต้องมีคนหน้าจอ**
1. `GAME_LIVE.txt` / console: **ห้าเฟรมเรียงตามลำดับ** `SPAWN_BARE` → `SPAWN_AVATAR` → `MOVE_A_1` → `MOVE_A_2` → `NEGATIVE_CONTROL` **ห่างกัน 15.0 วิ** · ขนาด **181 / (โครง 172) / 72 / 77 / 218 B** · **`frame_sha256` ของสี่เฟรมที่พินได้ ต้องตรง `probe.per_step.<LABEL>.frame_sha256` ของ scenario ใน commit ที่บูต** (`SPAWN_AVATAR` ตัดสินด้วย `pc_skeleton_sha256` 172 B เท่านั้น)
2. **พิกัดที่ decode ได้จริงจาก hexdump (f32):** `SPAWN_BARE` ต้องได้ **X `-9139.957` Y `-2780.045` Z `223.292`** (= `P0` เป๊ะ) 🔴 **ห้ามใช้ HUD เป็นฐานคำนวณ**
3. 🎯🔴 **ด่านที่เป็นของใบนี้โดยเฉพาะ — หลักฐานว่า "ผู้เทสไม่ได้เดิน":** จาก `PF-EVENT target_pos` / บรรทัดขาเข้าใน `GAME_LIVE.txt` **นับ `TargetPosVital` ทุกใบในช่วง `[T0, T0+70]`**
   - **เกณฑ์ผ่าน: นับได้ `0`** · และรายงาน **เวลาของ `TargetPosVital` ใบสุดท้ายก่อน `T0`** และ **ใบแรกหลัง `T0`** เป็นตัวเลข
   - 🔴 **ถ้ามีแม้แต่ใบเดียวตกในช่วง `[T0, T0+29]` ⇒ `W2` ปนเปื้อน ⇒ รอบนี้เป็น `M5 NON-OBSERVED` สำหรับตัวคุมมุมกล้อง** (ยังเก็บทุกอย่างไว้ได้ แต่ห้ามอ่านคู่ภาพเป็นผล)
   - 🟢 **การหมุนกล้องด้วยคลิกขวาลากไม่ใส่ไบต์ลงสายเลย** ⇒ **ยอด `0` คือหน้าตาที่ถูกต้องของสวีปที่หมุนแต่กล้อง**
4. **ไม่มี label `HYP_PF_025_REMOTE_PLAYER_*` ก่อนเฟรมแชตที่ถูกยอมรับ** + จดเวลานาฬิกาจริงของเฟรมแชต (`0xAC52`) และของ `[G>]` แรก
5. ไม่มี `remote_player_hypothesis_*_no_reply` · ไม่มี `ErrorData=28317` · ไม่มี traceback / stderr · **census: นับ *ทุก* บรรทัด `[G>]` ทั้งไฟล์แล้วรายงานยอดรวม ไม่กรองอะไรออก** (ยอด ≠ 5 **คือคำตอบ ไม่ใช่ความผิดพลาด**)
6. DB สำเนา: `PRAGMA integrity_check` = `ok` · row-diff ต่างเฉพาะ `sessions` **+1 ต่อการเข้าเกมหนึ่งครั้ง** · `max(lease_generation)` ก่อน-หลังไม่ถอยหลัง · **sha256 canonical ก่อน-หลัง = `CANON_SHA.txt`** · **canonical ไม่ถูกเปิดตลอดรอบ**
7. **ความครบของวิดีโอ (กฎ S):** `ffprobe` → เฟรมจริงเทียบ `duration x fps` · **รายงานเฟรมที่หายเป็นตัวเลข** · หายเป็นช่วงให้ระบุช่วงเวลา 🔴 **ข้อนี้บอกว่าไฟล์ครบแค่ไหน ไม่ได้บอกว่าในเฟรมมีอะไร**
8. 🔴🔴 **ชั้นนี้ตอบไม่ได้ — เขียนไว้ให้ชัดเพราะใบนี้ล่อให้ทำผิดข้อนี้เป็นพิเศษ:**
   - **NPC เห็นหรือไม่เห็นจากมุมไหน** — ชั้น wire ของเลนนี้ **ไม่เห็น NPC ของแมพแม้แต่บิตเดียว**
   - 🔴 **และที่สำคัญกว่า: `TargetPosVital` = 0 พิสูจน์แค่ว่า *ตัวละครไม่ได้เดินและไม่ได้หันตัว* — มัน *ไม่* พิสูจน์ว่ากล้องเคยหันไป `CAM-L`/`CAM-R` จริง** (การขยับกล้องไม่ทิ้งไบต์ไว้ที่ไหนเลย) ⇒ **หลักฐานว่ามุมเปลี่ยนจริงอยู่ในชั้น (2) ทั้งหมด**

**ชั้น (2) client-observable — ต้องมีคนหน้าจอ · 🔴 ตัวปิดใบอยู่ชั้นนี้ชั้นเดียว**
1. **หลักฐานบังคับ:** วิดีโอต่อเนื่องคลุมตั้งแต่ก่อน PRE ถึงหลัง `+70` · เฟรมที่ดึงจากวิดีโอครบหกใบ **`PRE_L`/`POST_L` · `PRE_R`/`POST_R` · `PRE_C2`/`POST_C`** + crop PNG กรอบเดียวกันต่อคู่ · **ภาพนิ่ง full-res ที่ถ่ายจริงสองใบสำหรับสีป้าย** · **sha256 ทุกไฟล์**
2. 🎯 **คำตัดสินหลักของใบ — ตอบเป็นคำพูดตรง ๆ ทีละมุม (สามบรรทัด ห้ามยุบรวม):**
   - `PRE_L ↔ POST_L` ⇒ **"เห็น NPC" / "ไม่เห็น NPC" / "เทียบไม่ได้"**
   - `PRE_R ↔ POST_R` ⇒ **"เห็น NPC" / "ไม่เห็น NPC" / "เทียบไม่ได้"**
   - `PRE_C2 ↔ POST_C` ⇒ **"เห็น NPC" / "ไม่เห็น NPC" / "เทียบไม่ได้"**
3. 🔴 **เงื่อนไขที่ทำให้มุมหนึ่ง ๆ "ใช้ได้" — ต้องตอบครบต่อมุม มิฉะนั้นมุมนั้นเป็น "เทียบไม่ได้" ไม่ใช่ "ไม่เห็น":**
   - (ก) **ช่วงนิ่งจริง `[t_เริ่ม, t_จบ]` ≥ 3.0 วินาที** (รายงานเป็นตัวเลขและจำนวนเฟรม)
   - (ข) **จุดอ้างอิงบนฉากที่จดไว้ตอน PRE ปรากฏในเฟรม POST ด้วย** ⇒ เป็นมุมเดียวกันจริง
   - (ค) **พิกัด `P0` อยู่ในกรอบภาพ** (ระบุว่าอ่านจากอะไร: จุดสังเกตบนพื้น/HUD/เงา)
   - (ง) **X/Y ของผู้เทสบน HUD ในเฟรม POST เท่ากับตอน PRE**
4. **ตารางเหตุการณ์:** `t` (สัมพัทธ์กับ `T0`) · เห็นอะไร · ที่ไหน · เฟรมไฟล์ไหน — **หนึ่งบรรทัดต่อหนึ่งเหตุการณ์** (รวมสิ่งที่เกิด/ไม่เกิดที่ `+30`/`+45`/`+60` ในฐานะ **ข้อสังเกต ไม่ใช่ผลของใบ**)
5. **ตารางสีป้ายชื่อครบทุกป้ายทุกภาพ full-res** (PLAYBOOK ข้อ 13 · **"ไม่มี" เขียนออกมาเป็นตัวอักษร ห้ามเว้นว่าง** · 🔴 **อ่านจากภาพนิ่ง full-res/crop PNG เท่านั้น ห้ามอ่านจากวิดีโอ/ภาพย่อ/contact sheet**)
6. **คำตอบข้อ clapper:** บรรทัดแชตปรากฏบนจอไหม · `T0` อยู่ที่ `t` เท่าไรในวิดีโอ
7. **NO-CRASH / CRASH verdict** (ตัดสินด้วยคลิกขวาลากเท่านั้น)
8. 🔴 **ใบปิดด้วยผลลบได้เฉพาะรอบที่ *คุณ Panya เห็นเอง* + มีวิดีโอต่อเนื่อง** (`AGENTS.md` §9)
9. 🔴 **ชั้นนี้ตอบไม่ได้:** เฟรมออกจากเซิร์ฟเวอร์จริงไหม · ไบต์ตรง pin ไหม · พิกัดที่ส่งคือ `P0` จริงไหม · ผู้เทสเดินหรือไม่ (ข้อหลังนี้ **ยืนยันด้วยชั้น (1) เท่านั้น** — สายตาคนตัดสินไม่ได้ว่าขยับ 1 หน่วยหรือ 0)

🔴 **ถ้าชั้น (1) ไม่ผ่าน (sha ไม่ตรง pin · พิกัด decode ไม่ใช่ `P0` · มี `*_no_reply` · console ขึ้น label เลนอื่น · มี `TargetPosVital` ใน `W2`) ⇒ รอบเป็น NO-RESULT ทางเทคนิค ห้ามอ่านจอเป็นผลใด ๆ แม้จะเห็นชัด ๆ**

---

### ตารางผลลัพธ์ที่มีชื่อ — **ทุกทางออกอ่านได้**

| # | สิ่งที่เห็น | คำตัดสินของใบ | อนุญาตให้สรุปว่า | 🔴 **ไม่** อนุญาตให้สรุปว่า / redirect |
|---|---|---|---|---|
| **M1** NOT-VISIBLE-FROM-ANY-ANGLE | มุม `L` และ `R` ใช้ได้ทั้งคู่ (ครบเงื่อนไข ก-ง) · **ไม่เห็น NPC ทั้งสองมุม** | ✅ **ปิดใบนี้ (PASS) — ตัวคุมมุมกล้องได้แล้ว** | ว่า **การหายของ NPC ไม่ใช่ผลของแนวสายตาในสองมุมที่ถ่ายจริง** ⇒ รวมกับเฟรมระยะประชิดของรอบแรก ⇒ **"บังทับ" ถูกตัดออกครบทั้งสองทาง** | ❌ **ห้ามเขียนว่า "พิสูจน์ despawn แล้ว"** — ดู nonclaim ① · ❌ ห้ามเขียนกลไกฝั่งไคลเอนต์ · **redirect:** ส่ง `GT-072` ให้ chief ตัดสินสถานะ (chief ตัดสินเอง ผู้เทส/ผู้ช่วยไม่ตั้ง) |
| **M2** VISIBLE-FROM-SOME-ANGLE 🔴 | **เห็น NPC อีกครั้งจากมุมใดมุมหนึ่ง** | 🎯🔴 **falsifier โดน — ผลที่ใหญ่ที่สุดที่รอบนี้ทำได้** | ว่า **NPC ยังอยู่ · "บังทับ" กลับขึ้นโต๊ะ · `despawn` ยังไม่ถูกตั้งขึ้นเลย** | ❌ ห้ามสรุปว่า **อะไร**บัง (โมเดลเรา? เอฟเฟกต์? LOD?) — ไม่ได้วัด · **redirect:** แก้ถ้อยคำผลรอบแรกของ `GT-072` ทันที + ต้องอธิบายเฟรมระยะประชิด `t=668.9` ที่พื้นว่างให้ได้ (สองอย่างนี้ขัดกัน = ของใหญ่ ส่ง chief) |
| **M3** ONE-ANGLE-ONLY | มุมหนึ่งใช้ได้ อีกมุมค้างไม่พอ/เพี้ยน/`P0` นอกเฟรม | 🟡 **PARTIAL** | ว่า **มุมที่ใช้ได้เห็น/ไม่เห็นอะไร ตามที่เห็นจริง** | ❌ ห้ามเหมารวมเป็น "ทุกมุม" · 🔴 **ใบยัง PENDING สำหรับมุมที่ขาด ห้าม archive** · **redirect:** รันซ้ำ commit เดิม เฉพาะมุมที่ขาด (ไม่นับเป็นเวอร์ชันใหม่ ไม่ต้องขอใครใหม่) |
| **M4** NPC-NEVER-VANISHED | NPC **ยังอยู่ตลอด** ไม่หายเลยตั้งแต่ `T0` | 🔴 **ผลลบที่สะอาด · มีค่าเท่าผลบวก · ไม่ใช่ FAIL** | ว่า **การหายทำซ้ำไม่ได้ในรอบนี้** ⇒ แม้จะทำซ้ำได้สามรอบก่อนหน้า **นี่คือรอบที่สี่ที่ขัด** | ❌ ห้ามเขียนว่า "สามรอบก่อนเห็นผิด" — คู่ภาพ same-camera อยู่ในรีโป · **redirect:** เทียบเงื่อนไขให้ครบ (ตำแหน่งผู้เทส · มุม · ระดับซูม · ระยะ · commit) แล้วรันซ้ำได้เลย |
| **M5** NON-OBSERVED | มี `TargetPosVital` ใน `W2` · กล้องขยับตลอดไม่มีช่วงนิ่ง · `P0` นอกเฟรม · `T0` หาไม่เจอ · วิดีโอหายช่วง · ซูมเปลี่ยน | 🔴 **NO-RESULT — ไม่ใช่ผลลบเด็ดขาด** | ไม่มี | ❌ **"ไม่เห็น NPC" ในเงื่อนไขนี้ไม่ใช่ผลของใบ** · **redirect:** รันซ้ำ commit เดิม แก้วินัยของ `W1`/`W2` · **🔴 ห้าม archive ใบ** |
| **M6** CRASH | ไคลเอนต์หลุด/ค้าง | 🟡 ผลที่มีชื่อ | จดว่าหลุดหลังเฟรมไหน | ❌ ห้ามชี้สาเหตุ · เก็บ console ทั้งไฟล์ · **restart server ก่อนบูตรอบถัดไป** |

---

### ⭐ PLAYBOOK ข้อ 13 — บันทึกสีของ **ทุกป้ายชื่อในเฟรม** (คำสั่งคุณ Panya 2026-08-25 · บังคับทุกใบ attended ตั้งแต่ R163)
- **จดอะไร:** ชื่อตัวเราเอง (เหนือหัว + แผง UI ซ้ายบน) · ชื่อ NPC/actor ทุกตัวในเฟรม · ชื่อไอเทมบนพื้น · ชื่อผู้เล่นคนอื่น · บรรทัด title/คำอธิบาย — **หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ**
- **ไม่มีให้เขียนคำว่า "ไม่มี" ออกมาเป็นตัวอักษร** 🔴 **ห้ามเว้นว่าง**
- **อ่านสีจากภาพนิ่งความละเอียดเต็ม / crop PNG เท่านั้น** 🔴 **ห้ามอ่านจาก contact sheet · ห้ามจากภาพย่อ · ห้ามจากวิดีโอ** ⇒ เก็บ full-res ที่ `evidence_screens\GT074_<TAG>_FULLRES_<yyyyMMdd_HHmmss>.png|jpg` (**ถ้าไฟล์ใหญ่เกิน ให้ crop จากต้นฉบับ ห้าม resize ลง**) · **sha256 ทุกไฟล์**
- **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับ:** NPC = **เหลือง** · ผู้เล่น = **เขียว** · ไอเทมบนพื้น = **ขาว** · title/คำอธิบาย = **ฟ้า** · ชื่อตัวเอง = **ขาว**
- 🔴🔴 **ผู้เทสจด "สี" อย่างเดียว ห้ามสรุปสาเหตุ** — **อะไรตัดสินสีของป้ายคือคำถามของ `RE-067` (ครึ่ง actor อยู่ที่ `RE-068`)** ⇒ **ห้ามเขียนว่า "แปลว่าไคลเอนต์จัดมันเป็นผู้เล่น/NPC/ศัตรู"**
- **`REAL_SERVER_DIVERGENCE.tsv`: 🔴 ส่งค่ากลับมาในจดหมายผล ห้ามแก้ไฟล์เองจากหน้าสะพาน** · หนึ่งแถวต่อหนึ่งป้ายที่เทียบ (คั่นด้วย **TAB** · อ่านหัวไฟล์ก่อน) · `evidence_layer` = **`eye`** เสมอ · `evidence_ref` = path ภาพ full-res · `evidence_sha256` **คนละคอลัมน์** · `open_ticket` = **`RE-067`** · `blocks_promotion` = `no` · **เติมแถวแม้ผลจะ "ตรงกัน"**

### เกณฑ์หยุดทั้งเลนทันที (คงเดิมจากก้อน 1)
⛔ ชื่อ **`ProbeControl03`** โผล่ที่ไหนก็ตาม (ป้ายหรือพาเนล) ⇒ **หยุด เก็บ console ทั้งไฟล์**
⛔ server log มี `ErrorData=28317` ⇒ **หยุด เก็บ console ทั้งไฟล์**
🔴 **ไม่มีทาง despawn probe ของเราเอง** — สามตัวค้างจนตัด connection · **HP ของ probe = 100 ทุกตัวตามดีไซน์ ถ้าเห็นตัวไหน "ตาย" เอง = ผิดคาด จดละเอียด** (**ห้ามสรุปสาเหตุ — นั่นคือ `RE-071`**)

### 🧾 teardown + ใบเสร็จ (บังคับ — **แม้รอบจะจบเพราะคนเลิกเล่น ไม่ใช่เพราะเทสจบ**)
- **teardown เสมอ ภายใน 420 นาทีจาก boot stamp** (`staged\TEMPLATE_teardown_generic.ps1:135` · เพดานถูกยกจาก 180 เมื่อ 2026-08-20 · **เลข 180 ในใบเก่า = stale**) — เกินเพดาน template **ปฏิเสธ exit 12 โดยดีไซน์**
- แท่นที่ถูกทิ้งข้ามชั่วโมง: **อย่าฝืน template** ⇒ `staged\TOOL_stop_stale_server.ps1` แล้วตามด้วย receipt อ่านอย่างเดียว `staged\0949_gt027_stalepad_canonical_guard.ps1`
- ได้ **exit 36** อย่าเดาเอง — แนบบรรทัดที่ 17 ของไฟล์ teardown ที่ใช้จริงมาทั้งบรรทัด
- **ใบเสร็จที่ต้องแนบมากับผล ทุกข้อ:** `AFTER listeners = 0` · **canonical guard: sha256 ก่อน-หลัง = `CANON_SHA.txt`** · **teardown exit code** · `LOCK_GAME` ปล่อยแล้ว · run copy `state\run_gt074*.sqlite3` **เก็บไว้ให้ chief re-derive ห้ามทิ้ง** · path ของ raw GAME log + console out/err + วิดีโอ + ภาพทุกไฟล์ พร้อม **sha256**
- 🔴 **บนสะพานเท่านั้น ห้ามลบ:** ไฟล์ `.mkv` ต้นฉบับ และโฟลเดอร์ capture ของรอบ · **และห้ามลบหลักฐานรอบแรกของ `GT-072`** (`evidence_video\1168_gt072_FULLROUND_20260825_212052.mkv` · `GameClient\capture_gt072_20260825_212050\`)
- 🔴 **restart เซิร์ฟเวอร์ก่อนบูตรอบถัดไปเสมอ**

---

### nonclaims (ติดไปกับผลทุกกรณี ไม่ว่าบวกหรือลบ — **ห้ามตัดทิ้ง**)

① 🔴🔴 **ผลลบของรอบนี้ *ไม่* พิสูจน์ `despawn` ด้วยตัวมันเอง** — มันทำอย่างเดียว: **ตัดทางหนีสุดท้ายของ "บังทับ" (มุมกล้อง)** · `despawn` ยังเป็น **แถวที่เหลือ** และ **จดหมายผลของ `GT-072` เขียนเองว่ามันคือแถวที่อ่อนที่สุดโดยธรรมชาติ** — *"คลิกไม่ติด ไม่เท่ากับ ไม่มีอะไรอยู่ตรงนั้น"*
② **สองมุม ~45° คือสองแนวสายตา ไม่ใช่ "ทุกมุม"** — ผลครอบเฉพาะแนวและกรอบกล้องที่ถ่ายจริง · **อะไรที่อยู่นอกเฟรม/นอกแนว = non-observed ไม่ใช่ absent**
③ **ไม่พิสูจน์กลไกฝั่งไคลเอนต์แม้แต่นิดเดียว** — "ช่อง actor" / "id ชนกัน" / "hash ตำแหน่ง" / "ลำดับใน list" **ไม่มีหลักฐาน static แม้แต่บรรทัดเดียวในโปรเจกต์**
④ **ไม่ได้พิสูจน์ว่าตัวที่หายคือ `Navy Transfer`** เว้นแต่ **อ่านชื่อบนป้ายลอยหัวออกจากภาพ full-res ใบ PRE จริง ๆ** — รอบนี้ **ไม่คลิกเป้าโดยเจตนา** ⇒ ถ้าอ่านป้ายไม่ออก ให้เขียนว่า **"ระบุจากตำแหน่งและรูปลักษณ์เท่านั้น"**
⑤ 🔴 **`TargetPosVital` = 0 พิสูจน์ว่าตัวละครไม่เดิน/ไม่หัน — *ไม่* พิสูจน์ว่ากล้องหันไปมุมอื่นจริง** · ข้อพิสูจน์เรื่องมุมอยู่ในชั้น (2) ทั้งหมด (จุดอ้างอิงบนฉาก + ช่วงนิ่ง)
⑥ **รอบเดียวไม่ใช่คุณสมบัติของไคลเอนต์** — จุดเดียว แมพเดียว รอบเดียว · **และรอบนี้ไม่ปิดข้อผูกพันการทำซ้ำของ `GT-030-R3` ซึ่งเป็นคนละคำถาม**
⑦ **ใบนี้ไม่ปิด `GT-072` ด้วยตัวเอง และไม่แทนที่มัน** — มันเติมช่องเดียวที่ `GT-072` เว้นไว้ · **สถานะของ `GT-072` เป็นของ chief ตัดสิน ผู้เทสและผู้ช่วยห้ามตั้งเอง**
⑧ **ไม่ตอบอะไรเลยเรื่อง `ตาย!` / `HP 0` / `LV 1` / `BasicAttr` ของ probe** — นั่นคือ `RE-071` · เห็นอีกให้จดเป็นข้อสังเกต
⑨ **ไม่ตอบอะไรเลยเรื่อง `Z = 0.00` เหนือผืนน้ำ / เวทีเทสโมเดล** — นั่นคือ `RE-073` และใบเรื่องผืนน้ำ · รอบนี้ **ห้ามเดินลงน้ำ** (จะทำให้ `TargetPosVital` เด้งและตัวคุมพัง)
⑩ **สิ่งที่เกิด/ไม่เกิดที่ `+30`/`+45`/`+60` เป็นข้อสังเกตฟรี ไม่ใช่ claim ของใบนี้** — `W3` ไม่มีตัวคุม
⑪ **สีอ่านด้วยตาจากภาพ ไม่ได้วัดค่าพิกเซล** ⇒ **ไม่ claim ค่า RGB/hex ใด ๆ** · `evidence_layer` ของทุกแถวที่ออกจากใบนี้คือ **`eye`** · **และผู้เทสจดสีอย่างเดียว ห้ามอนุมานสาเหตุจากสี (`RE-067`)**
⑫ **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับอาจเป็น client คนละ build/ภูมิภาค** ⇒ "ต่างจากภาพต้นฉบับ" ยังไม่เท่ากับ "ของเราผิด"
⑬ **ไม่มีใครวัดว่าคลิกซ้าย / ล้อเมาส์ ยิงไบต์อะไรออกสายหรือไม่** — จึงบังคับให้จดเวลาของทุกคลิกและทุกการซูม
⑭ **ขอบล่างของ transient = ช่วงหนึ่งเฟรมของวิดีโอที่อัดจริง** (30 fps ≈ 0.033 วิ) · ถ้า `ffprobe` พบเฟรมหาย **ขอบล่างคือช่องว่างที่วัดได้จริง ไม่ใช่ `1/fps`**
⑮ **ห้ามอ้างตัวเลขข้ามสองนาฬิกา (วิดีโอ↔สาย) เป็นคำตัดสิน** — offset ต่างกันทุกบูต (`0.0/0.58/1.82` วิ วัดจากสามรอบของ 2026-08-25)
⑯ **เฟรม / mask / identity band / การวางตำแหน่ง ทั้งหมดเป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้วและกู้ไม่ได้ตลอดกาล · **ตาราง placement ใน `pf_login_game_server_v141.py` ก็เป็นของเรา**
⑰ **`OBSERVER_CONFIRMED` เป็นขั้นตอน ไม่ใช่หลักฐาน** — บอกว่า "ผู้เทสยืนยันว่าสิ่งที่ผู้ช่วยเขียนตรงกับที่เธอเห็น" **ไม่ได้บอกว่าสิ่งนั้นเป็นความจริงเรื่องไคลเอนต์**

- **result:** (ผู้เทสกรอก: ① `BOOT_COMMIT` + ผลด่านหกข้อทีละข้อ (แปะสิ่งที่คอนโซลพิมพ์) ② ห้าเฟรม + ขนาด + `frame_sha256` เทียบ pin ทีละเฟรม + พิกัดที่ decode ได้ของ `SPAWN_BARE` ③ **ยอด `TargetPosVital` ในช่วง `[T0, T0+70]`** + เวลาใบสุดท้ายก่อน `T0` + ใบแรกหลัง `T0` ④ `T0` อยู่ที่ `t` เท่าไรในวิดีโอ + บรรทัดแชตขึ้นจอไหม ⑤ **ตารางต่อมุม 6 ใบ: ชื่อไฟล์ · `[t_เริ่ม, t_จบ]` ของช่วงนิ่ง · จำนวนเฟรม · จุดอ้างอิงบนฉากที่เห็น · X/Y บน HUD · เห็น/ไม่เห็น/เทียบไม่ได้** ⑥ ค่ากรอบ crop ที่ใช้ (ต้องค่าเดียวกันในแต่ละคู่) ⑦ **แถวไหนของตารางผล (M1-M6)** ⑧ ตารางเหตุการณ์ `t` สัมพัทธ์ `T0` ⑨ สิ่งที่เกิด/ไม่เกิดที่ `+30`/`+45`/`+60` (**ข้อสังเกต ไม่ใช่ผล**) ⑩ **ตาราง PLAYBOOK ข้อ 13 ครบทุกป้ายทุกภาพ full-res ("ไม่มี" เขียนออกมา ห้ามเว้นว่าง)** ⑪ ค่าที่ต้องเติม `REAL_SERVER_DIVERGENCE.tsv` (**ส่งค่ามา ห้ามแก้ไฟล์เอง**) ⑫ census บรรทัด `[G>]` ทั้งไฟล์ + มี `ErrorData=28317` ไหม + NO-CRASH/CRASH ⑬ path raw GAME log + console ทั้งไฟล์ + วิดีโอ + ภาพทุกไฟล์ พร้อม sha256 ⑭ เวลา +07:00 · sha canonical ก่อน-หลัง · `integrity_check` · row-diff + `max(lease_generation)` ของ `run_gt074*.sqlite3` · exit code ของ teardown ⑮ ถ้ามี session 2: ทุกข้อข้างบนแยกชุด **ห้ามรวมกับ session 1**)

---

## 🆕 GT-076 POPULATION-FULL-001-ACTOR-CEILING-STAIRCASE-001 [attended, in-game]: ไคลเอนต์รับ actor ใน RuntimeRes collection **เดียว** ได้กี่ตัว - เดินบันไดซ้อนของสำมะโน `bg0001` 3 -> 20 -> 60 -> 115  [🔴 **BLOCKED — รอ merge ก่อน** · **`BLOCKED-ON-WIRING` จบแล้ว (chief R173 ต่อสายให้ + ใส่ `--world-census-actors`) ดูบล็อก "แก้ไข R173" ท้ายใบ** · เปิดใบโดย LANE-A 2026-08-25 ~23:1x (+07:00) ตาม `CHARTER-01` §④ BUILD-001 · เขียนใบโดย `pf-queue-author`]

> 🔢 **เรื่องเลขใบ:** ตัวนับเป็น **ชุดเดียวร่วมกับ `CLIENT_RE_QUEUE.md`** — prefix สองแบบ ตัวนับเดียว
> `GT-074` ถูกใช้แล้ว (chief R170) · `RE-073` ถูกใช้แล้ว (R169) · **`RE-075` ถูกใช้แล้ว** ⇒ **ใบนี้คือ `GT-076`** · **`RE-077` ถูกจองในรอบเดียวกันนี้โดย LANE-A** ⇒ **เลขว่างถัดไปคือ 078**
> 🔴 **ใบ `GT-030` · `GT-030-R3` · `GT-072` · `GT-074` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ** — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

> 🎯 **MILESTONE:** ใบนี้คือ **การวัดที่อยู่เบื้องหลัง `M1` "เมืองมีชีวิต"** (`CHARTER-01` ตารางไมล์สโตน แถว M1 · เกณฑ์ที่ตาเจ้าของตัดสิน: **เดินใน Port Royal แล้วเห็น NPC ทั่วเมือง ไม่ใช่ 3 ตัว** · **กำหนด 26 ส.ค.**)
> 🔴 **ใบนี้ไม่ได้ปิด `M1` ด้วยตัวเอง** — `M1` ปิดด้วยตาเจ้าของเท่านั้นตามกฎการวัดใน `CHARTER-01` §③ · ใบนี้ส่งมอบ **ตัวเลข** ที่ทุกไมล์สโตนหลังจากนี้ต้องใช้

> ---
> ### 🔴🔴 **AMENDMENT · 2026-08-26 ~01:0x (+07:00) · โดยสาย A (LANE-A · `pf-builder`) รอบ `jjxgz3` ตาม `CHARTER-02 §④`**
> **เจ้าของสั่งยกเลิกขั้นบันได — ใบนี้ยิง `115` ทีเดียว** · ถ้อยคำเดิมของใบทั้งใบ **คงไว้ทุกตัวอักษร** ตามกฎห้ามลบประวัติ · อ่านบล็อกนี้ทับ
>
> | | เดิม (ยังอ่านได้ข้างล่าง) | **ที่ต้องทำจริงตั้งแต่บัดนี้** |
> |---|---|---|
> | จำนวนที่ส่ง | ~~บันได `3 -> 20 -> 60 -> 115` สี่บูต~~ | **`115` ทีเดียว หนึ่งบูต** |
> | ตัวคุม | ~~ขั้น 3 เป็นขั้นคุมไบต์เท่าเดิม~~ | เลิกใช้เป็นลำดับบังคับ · **ยังใช้เป็นเครื่องมือวินิจฉัยได้ถ้าการยิงทีเดียวตาย** (`world_population.build_staircase()` ยังอยู่ ไม่ถูกลบ) |
> | สิ่งที่กันการเดาแทนบันได | ~~ไต่ทีละขั้นเพื่อบีบช่วง~~ | **นับ actor ที่ประกอบได้จริงก่อนส่ง แล้วพิมพ์ลงคอนโซล** |
>
> **เหตุผลของเจ้าของ (คำต่อคำใน `CHARTER-02 §④`):** *"เคยไล่มาก่อนแล้วด้วย ai ตัวเก่า เห็นว่า 115 ก็ทำได้ไม่มีปัญหา ก่อนจะมาลดเหลือเทสแค่ 3 ตัว"*
> 🔴 **ป้ายกำกับหลักฐานตามกฎ `G8`:** ข้อนี้เป็น **`[เจ้าของยืนยันจากประสบการณ์ตรง]` ไม่ใช่ `[วัดแล้ว]` ในโปรเจกต์นี้** — ผู้เทสยังต้องรายงานสิ่งที่เห็นตามจริง ห้ามอ่านบล็อกนี้ว่า "รู้อยู่แล้วว่าผ่าน"
>
> **บรรทัดคอนโซลที่ต้องมีก่อนเฟรมออก** (`world_population.census_console_line()` · ASCII ล้วน cp874-safe):
> ```
> WORLD_CENSUS assembled=115/115 wire=115 bodies=ok pc=17928B frame=17942B anchor=(x,y,z) reapply_ms=3000 source=full_census shortfall=none
> ```
> 🔴 **`wire=` คือจำนวนที่ถอดจากไบต์ที่จะส่งจริง และ `bodies=` คือการเทียบผลรวมความยาว actor body** — `pf-adversary` วัดให้เห็นแล้วว่าการนับที่นับแต่ฝั่งอินพุตจะพิมพ์ `115/115` ทับเฟรมที่ actor หายไปหนึ่งตัว (สั้น 148 ไบต์) ซึ่งคือ stream-tail misalignment ที่ `ErrorData=28317` ตอบพอดี ⇒ **เห็น `bodies=SHORT` หรือ `wire=MISMATCH:` เมื่อไหร่ = หยุด อย่าบูตต่อ**
> 🔴 **ถ้าเลขไม่ใช่ `115/115` ห้ามเดินต่อเงียบ ๆ** — บรรทัดนั้นบอกเหตุผลมาเอง (`caller_requested=` หรือ `measured_client_ceiling=`) · **บันทึกเลขจริงและเหตุผลลงผลใบ** ตามข้อห้าม *"ห้ามเปลี่ยนตัวเลข 115 เป็นค่าอื่นเงียบ ๆ"*
> 🟢 **สิ่งที่ไม่เปลี่ยนเลย:** กฎ "ขั้นที่พังคือผล ไม่ใช่ความล้มเหลว" ข้างล่าง **ใช้กับการยิงทีเดียวเหมือนกันทุกตัวอักษร**
> ---

---

### 🔴🔴 อ่านบรรทัดนี้ก่อนทุกบรรทัด — **ขั้นที่พังคือ "ผล" ไม่ใช่ "ความล้มเหลว"**

**ถ้าขั้นไหนของบันไดพัง นั่นคือเพดานที่วัดได้ ไม่ใช่เทสตก**
- **ห้ามรายงานว่า FAIL** · **ห้าม "ไปแก้ให้มันผ่าน"** · **ห้ามลดจำนวนลงเองเพื่อให้บูตรอด**
- ตัวเลขที่โปรเจกต์นี้อยากได้คือ **"ไคลเอนต์รับได้ถึงเท่าไร แล้วปฏิเสธที่เท่าไร"** — ขั้นที่พังคือครึ่งหลังของประโยคนั้น และมันมีค่าเท่ากับครึ่งแรกเป๊ะ
- **ผลลบมีค่าเท่าผลบวก** — ถ้าไคลเอนต์รับ 115 ตัวสบาย ๆ นั่นก็เป็นผล · ถ้ามันตายที่ 20 นั่นก็เป็นผล **และเป็นผลที่แพงกว่า เพราะมันเปลี่ยนดีไซน์ของ M2-M6 ทั้งหมด**

---

### ที่มา — **สามข้อเท็จจริง อ่านครั้งเดียวจบ ห้าม re-derive ระหว่างรอบ**

1. **วันนี้ runtime ส่ง 3 ตัวจาก 115 placement ของ `bg0001` ทุกบูต** — label `V134_P0_P30_P91_ISOLATED_INITIAL_READY` (`current/pf_login_game_server_v141.py:4292`) · เจ้าของเดินเข้า Port Royal แล้วเห็นเมืองร้าง
   🔴 **เลข 3 นี้เป็นเศษเหลือของการแยกตัวแปร `V112 -> V129 -> V134` ไม่ใช่เพดานที่ใครวัดมา** — ไม่มีเอกสารบรรทัดใดในโปรเจกต์บอกว่า 3 คือขีดจำกัด
2. **ไม่มีเอกสารในสองรีโปนี้บันทึกเพดาน actor พร้อมกันของไคลเอนต์ไว้เลย** — จำนวนสูงสุดที่ **มีผลบันทึกไว้** คือ **20** (V94 authoritative nearest-set · ไคลเอนต์รับ)
   🔴🔴 **แต่ห้ามเขียนว่า "ไม่เคยมีใครส่งมากกว่านั้น"** — `current/pf_login_game_server_v141.py:1441` `make_v62_port_royal_population_snapshot()` **สร้างเฟรม 115 ตัวในสแนปช็อตเดียว** ป้าย `V73_PORT_ROYAL_GOLDEN_POPULATION_115` และ docstring เรียกมันว่า *"the golden runtime-state baseline"* · **วันนี้ไม่มีใครเรียกฟังก์ชันนั้น ไม่มีเทสแตะ และไม่มีรายงานผลรันไทม์ของยุคนั้นหลงเหลือในสองรีโปนี้เลย** (เรื่องเล่าอยู่ใน `handoff.txt` ซึ่งไม่ได้อยู่ในรีโป)
   ⇒ **สิ่งที่พูดได้คือ "ไม่มีบันทึกว่าผลเป็นอย่างไร" ไม่ใช่ "ไม่เคยมีใครลอง"**
3. **บันทึกเก่าสุดใน frozen source:** สตรีมรวม **หกตัว** เคยทำให้เกิด `ErrorData=28317` (V43) ขณะที่สตรีม **หนึ่งตัว** parse ผ่าน (V42)
   🔴🔴 **และรีโปนี้ถอดรหัสเลขนั้นไว้แล้ว — มันไม่ใช่ตัวเลขเรื่อง "จำนวน":** `reports/PF_DELETE_SOFT002_NATURAL_0x36DB_DECODE_20260818.md` §(c) สรุปว่า **28317 = 0x6E9D = `GSCN_RunTimeProtocolRes`** คือ **ไคลเอนต์สะท้อน class id ของ envelope ที่ deserialize ไม่ผ่าน** และทุกเคสที่ทำซ้ำได้ในรายงานนั้นเป็น **stream-tail / misalignment fault ของ RuntimeRes ทั้งหมด** · **หลังเกิด error ไคลเอนต์ปิดการเชื่อมต่อทั้งสองเส้น**
   ⇒ **`28317` แปลว่า "เฟรมนี้ parse ไม่ผ่าน" ไม่ได้แปลว่า "ตัวเยอะไป"** ⇒ ขั้นที่ตายให้ **ช่วง** ไม่ใช่ **สาเหตุ**

---

### 🔴🔴 สิ่งที่ใบนี้จะ **ไม่** ทำให้เห็น — **วัดก่อนเขียนใบ อ่านก่อนคาดหวัง**

**สำมะโน 115 แถวนี้ไม่ใช่ "รายชื่อคนในเมือง" — มันกระจายทั้งแมพ กว้างราว 39,000 หน่วย และบางแทบทุกจุด** (วัดจากตารางแช่แข็งโดยตรง):

| ยืนที่ | ในรัศมี 500u | 1,000u | 2,000u | ตัวที่ 20 ห่าง | ตัวที่ 60 ห่าง | ตัวที่ 115 ห่าง |
|---|---|---|---|---|---|---|
| จุดเกิดตัวละครใหม่ (`V135`) | **1** | **1** | **2** | 13,012 | 26,719 | 39,425 |
| anchor อ้างอิง (`V134`) | 1 | 1 | 2 | 12,998 | 26,696 | 39,394 |

**จุดที่หนาแน่นที่สุดในตารางทั้งใบคือ `P67` มีเพื่อนบ้านในรัศมี 1,000u = 8 ตัว** (และอยู่ห่างจากจุดเกิดราว 30,000 หน่วย)

🔴🔴 **ผลที่ตามมาสามข้อ ต้องอ่านให้จบก่อนบูต:**
1. **"ส่ง 115 แล้วเมืองจะแน่นขึ้น" เป็นเท็จ** — ที่จุดเกิด ขั้น 20 กับขั้น 115 มีสมาชิก *ในระยะที่มองเห็น* เท่ากัน เพราะตัวที่เพิ่มมาอยู่ห่างเป็นกิโลเมตร
2. ⇒ **จำนวนหัวที่นับได้ "เท่าเดิม" ระหว่างขั้น คือผลที่ *คาดไว้แล้ว* ไม่ใช่เพดานการเรนเดอร์** (ดูแถว N3 ในตารางผล — เกณฑ์ถูกแก้ตามข้อนี้)
3. ⇒ **ชั้นที่แยกขั้นออกจากกันได้จริงคือชั้นสาย ไม่ใช่ชั้นตา** · ชั้นตามีหน้าที่เดียวที่ยังมีค่ามาก: **ยืนยันว่าไคลเอนต์ยัง *เรนเดอร์อะไรก็ได้* อยู่** (หมุด `P30`) และ **ไม่ค้าง/ไม่หลุด**

🎯 **แล้วผู้เล่นได้อะไรจริง ๆ:** วันนี้ทั้งแมพ `bg0001` มี actor อยู่ **3 ตัว** ⇒ ทุกที่นอกมุมท่าเรือหนึ่งมุม **ว่างเปล่าแน่นอน** · เมื่อส่งทั้งสำมะโน **ทุก placement ที่ข้อมูลต้นฉบับกำหนดไว้จะมีตัวตน** ⇒ **เดินไปที่ไหนในแมพก็เจอคนที่ควรอยู่ตรงนั้น** — นั่นคือสิ่งที่เปลี่ยน ไม่ใช่ "จุดเกิดแน่นขึ้น"

---

### objective (claim เดียว)

**ที่ขั้นบันไดซ้อน `3 -> 20 -> 60 -> 115` ขั้นสูงสุดที่ไคลเอนต์ตัวนี้ *รับ* RuntimeRes collection เดียวได้ คือขั้นไหน**

- "รับ" = **ทั้งสองชั้น**: (ชั้น 1) เฟรมออกไปแล้วไม่มี `ErrorData` ตามมา และการสื่อสารเดินต่อ · (ชั้น 2) คนที่หน้าจอเห็นเมืองมีคน ไคลเอนต์ไม่ค้าง ไม่หลุด
- **ขั้นบันไดซ้อนกัน (nested):** ทุกขั้นเป็น **superset แท้** ของขั้นล่าง — 🔴 **แต่ซ้อนกันเฉพาะเมื่อ anchor เดียวกันเท่านั้น** (`build_staircase()` การันตีได้แค่ภายในการเรียกครั้งเดียวที่ anchor เดียว) · **สี่บูต = สี่ anchor ที่อาจไม่เท่ากัน** ⇒ ทำตามบล็อก ANCHOR ให้เป๊ะ แล้วให้ chief ตรวจย้อนด้วย `nesting_break()` จาก XYZ ที่จดมา
- 🔴 **ทำไมความซ้อนถึงสำคัญ:** ถ้าขั้นไม่ซ้อนกัน ขั้นที่พังจะแปลว่า "ชุดนี้พัง" ซึ่งอ่านไม่ได้ · **ซ้อนแล้ว ขั้นที่พังแปลว่า "รับ N ได้ ปฏิเสธที่ N+"**
- 🔴🔴 **และแม้ซ้อนกันสนิท "จำนวน" ก็ไม่ใช่ตัวแปรเดียวที่เปลี่ยน — ยอมรับตรง ๆ ตั้งแต่ต้น:** ขึ้นหนึ่งขั้นคือเพิ่ม **จำนวนสมาชิก + ขนาดเฟรม + `template_id` ใหม่ + visual preset ใหม่** ซึ่งแต่ละ preset คือ **ชื่อไฟล์ avatar template ที่ไคลเอนต์ต้องโหลด** (`.\Data\GC\V\%s.avt` · docstring ของ `make_npc_attr`) ⇒ **template เดียวที่โหลดไม่ได้ ทำให้ขั้นนั้นพังโดยไม่เกี่ยวกับจำนวนเลย**
  🟢 สิ่งที่ **ไม่ใช่** ตัวกวน: การบีบอัดฝั่งเรา — `frame_pc()` ห่อด้วย snappy raw **literal** (v141:560) ⇒ ขนาดเฟรมโตตามเนื้อตรง ๆ

**🔴 ใบนี้ไม่ใช่สองใบ:** จำนวนโมเดลบนจอ **ไม่ใช่ claim ที่สอง** — มันคือ **ตัวขยายความของเลขเดียวกัน** และเป็นเหตุผลที่ชั้น (2) ต้องมีคนอยู่หน้าจอ · 🔴 **แต่ดูบล็อก "สิ่งที่ใบนี้จะไม่ทำให้เห็น" ก่อน — ชั้นตาแยกขั้นออกจากกันไม่ได้ในเลนนี้**

---

### 🔴🔴 PRECONDITION — **BLOCKED-ON-WIRING · ยังบูตไม่ได้ ห้ามบูต**

**ตัวนับยังไม่ถูกต่อเข้าเส้นทาง runtime ไร้แฟล็ก**
- โมดูลที่รอต่อ: **`src/pirateforce_foundation/world_population.py`** (LANE-A เขียนเสร็จแล้ว · `production_allowed = True` · `test_only = False` · ไม่ติดตั้งอะไรด้วยตัวเอง โดยตั้งใจ)
- ฟังก์ชันที่การต่อสายต้องเรียก **สองตัวนี้ ชื่อเป๊ะ:**
```
build_world_population(legacy, player_xyz, actor_count)
effective_actor_count()
```
- **`runtime.py` / `app.py` เป็นไฟล์ของ chief — LANE-A ไม่แก้** ⇒ ใบนี้ **รอ chief ไม่ได้รอผู้เทส ไม่ได้รอ CI ไม่ได้รอเจ้าของ**
- ตัวพินตัวเลขที่มีอยู่แล้วและ **ไม่ใช่สวิตช์**: `scenarios/world_population_full_001.json` (ไม่มีแฟล็กไหนอ่านมัน · เป็นที่เก็บเลขคาดหมายอย่างเดียว · ถูกตรวจโดย `tests/test_world_population.py::test_pin_file_still_describes_what_the_module_builds`)

**🔴 สามข้อที่การต่อสายต้องส่งมอบ มิฉะนั้นใบนี้ยัง BLOCKED ต่อ:**
1. **วิธีเลือกจำนวน actor ต่อบูต** (แฟล็ก / env / commit ละขั้น — chief เลือกเอง LANE-A ไม่ตัดสินแทน)
2. **คอนโซลต้องพิมพ์จำนวนที่ *ส่งจริง* ตอนบูต** — 🔴 **ไม่มีบรรทัดนี้ = ห้ามบูต** เพราะจะแยกไม่ออกว่ารอบนั้นเป็นขั้นไหน (นี่คือกับดักหลักของใบนี้: สี่บูตหน้าตาเหมือนกันหมด)
3. **คนที่ต่อสายเสร็จ ต้องกลับมาเขียน "server args" ของใบนี้ให้เป็นสตริงจริง** แล้วพลิกสถานะใบเป็น `PENDING`

**🟢 ต่อสายเสร็จแล้ว สี่บูตจบในการนั่งครั้งเดียว** (~15 นาทีบนจอต่อบูต + บูต/teardown ⇒ ประมาณหนึ่งชั่วโมงกว่า ๆ)

---

### db (สำเนาเสมอ — **canonical ไม่ถูกเปิดตลอดรอบ**)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-076_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt076_r3.sqlite3
copy state\pirateforce.sqlite3 state\run_gt076_r20.sqlite3
copy state\pirateforce.sqlite3 state\run_gt076_r60.sqlite3
copy state\pirateforce.sqlite3 state\run_gt076_r115.sqlite3
```
- 🔴 **สำเนาใหม่หนึ่งใบต่อหนึ่งบูต ห้ามใช้ไฟล์เดิมซ้ำ** · ถ้าต้องรันขั้นเดิมซ้ำเพื่อยืนยัน (ดู STOP RULE) ให้ใช้ `state\run_gt076_r<N>_confirm.sqlite3`
- เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง**
- 🟢 **สำเนาใหม่ทุกบูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกครั้ง — รอบนี้นั่นคือ *ข้อดี* ไม่ใช่ความรำคาญ** เพราะมันทำให้ anchor ของสี่บูตเหมือนกันได้ (อ่านบล็อก anchor ข้างล่าง)
- ต่างได้เฉพาะ `sessions` **+1 แถวต่อการเข้าเกมหนึ่งครั้ง** · จด `max(lease_generation)` ก่อน-หลัง **ห้ามถอยหลัง** · `PRAGMA integrity_check;` ทุกสำเนา

### 🔴 ก่อนบูต — resolve commit เขียว (รันเครื่องมือ ห้ามก๊อป SHA เก่า)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` · **exit 3** ⇒ **ห้ามบูต** ใบอยู่ BLOCKED ต่อ · **exit 2** = พาธผิด/git ล้ม
- **ยืนยันห้าข้อกับ `<SHA>` ที่จะบูตจริง** (single quote เท่านั้น · **ห้าม `| grep` / `awk`**):
```
git show origin/ci-status:ci/<SHA>.json
git grep -n 'build_world_population' <SHA> -- src/pirateforce_foundation/
git grep -n 'effective_actor_count' <SHA> -- src/pirateforce_foundation/runtime.py src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/world_population_full_001.json && echo PIN_PRESENT
git grep -n 'PORT_ROYAL_SOURCE_COUNT = 115' <SHA> -- src/pirateforce_foundation/population.py
```
- 🔴 **ข้อสามคือด่านปลด BLOCKED** — ถ้า `runtime.py`/`app.py` ยังไม่มีการเรียก `effective_actor_count()` แปลว่า **ยังไม่ต่อสาย ห้ามบูต ใบยัง BLOCKED**
- **อ่านเลขคาดหมายจาก pin ของ commit ที่บูตจริง ห้ามฝังเลขจากความจำ**

### server args (เป๊ะ — 🔴 **ยังเติมไม่ได้จนกว่าจะต่อสาย**)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt076_r<RUNG>.sqlite3 --export-events <ACTOR_COUNT_SELECTOR__CHIEF_FILLS_THIS_IN_AT_WIRING_TIME>
```
- 🔴 **ถ้าบรรทัดข้างบนยังมีตัวอักษร `<ACTOR_COUNT_SELECTOR__...>` อยู่จริง ๆ ⇒ ใบนี้ BLOCKED ห้ามบูต ห้ามเดาแฟล็กเอง**
- 🔴 **ห้ามใส่แฟล็ก hypothesis / scenario ตัวอื่นแม้แต่ตัวเดียว** — เลนนี้คือ **เส้นทางไร้แฟล็ก** และนั่นคือประเด็นทั้งหมดของ BUILD-001 · เห็น label เลนอื่นบนคอนโซล = บูตผิดไฟล์ **หยุด ปิด server ห้ามอ่านจอเป็นผล**
- **หนึ่งบูต = หนึ่งขั้น** · 🔴 **ห้ามรวมสองขั้นในบูตเดียว ห้ามพ่วงใบอื่นเข้าบูตนี้**

---

### 🔴🔴 ANCHOR — **จุดที่ใบนี้พังได้ง่ายที่สุด อ่านให้จบก่อนแตะปุ่มเดิน**

**collection ถูกสร้างจาก `TargetPosVital` ใบ *แรก* หลัง runtime ack** (`pf_login_game_server_v141.py:4292` · pin เขียนไว้ว่า `trigger = first_exact_target_pos_after_runtime_ack`)
⇒ **anchor คือจุดที่ยืนตอน "ก้าวแรก" ไม่ใช่จุดที่เดินไปถึง**

- 🔴 **สมาชิกของขั้น 20 และ 60 ขึ้นกับ anchor** (ลำดับคือ พินสามตัวก่อน แล้วเรียงใกล้ที่สุดก่อนด้วย `(ระยะยกกำลังสอง, placement index)`)
- 🔴 **ถ้าไม่จด XYZ ของทุกบูต จะประกอบสมาชิกของขั้นกลับไม่ได้ และทั้งรอบอ่านไม่ออก** — จดจาก **hexdump ของ `TargetPosVital` ใบแรก (f32) ไม่ใช่ HUD** (HUD ใช้ได้เฉพาะการยืนซ้ำจุดเดิมด้วยตา)
- 🟢 **วิธีทำให้สี่บูตมี anchor เดียวกัน (บังคับ):** ทุกบูต **ก้าวแรกคือ "แตะ `W` สั้น ๆ ครั้งเดียวที่จุดเกิด แล้วปล่อย"** — สำเนา DB ใหม่ทำให้จุดเกิดเท่ากันทุกบูต ⇒ anchor เท่ากันทุกบูต
  🔴 **ห้ามเดินไป landmark ก่อนก้าวแรก** — เดินก่อน = anchor เพี้ยน = ขั้น 20/60 คนละชุดกับบูตอื่น = **เทียบข้ามบูตไม่ได้**
- **pin เก็บ anchor ไว้สองจุด และเลขไบต์เท่ากันทั้งสองจุด:**
```
V134_PLAYER_XYZ  x = -9239.95703125        y = -2780.045166015625   z = 223.29209899902344
V135_PLAYER_XYZ  x = -9239.95703125        y = -2830.045166015625   z = 223.29209899902344   <- จุดเกิดตัวละครใหม่
```
  🟢 **ที่จุดเกิดจริง (`V135`) ขั้น 3 และ 20 มีสมาชิก *ชุดเดียวกันเป๊ะ* กับ anchor อ้างอิง และทั้งสี่ขั้นมีขนาดไบต์เท่ากันทุกขั้น** ⇒ **ตารางเลขคาดหมายข้างล่างใช้ได้จริงที่จุดเกิด ไม่ใช่เลขลอย ๆ**
  🔴 **แต่ยังต้องจด XYZ ทุกบูตอยู่ดี** — ถ้าผู้เทสเผลอเดินก่อนก้าวแรก anchor จะเลื่อน และสมาชิกของขั้น 20/60 จะเปลี่ยน · **`nesting_break()` ของ chief ต้องใช้ XYZ จริงในการตรวจ ไม่ใช่ค่าที่พินไว้**

---

### เลขคาดหมายบนสาย — **จดแล้วเทียบทีละขั้น** (`RuntimeRes` collection เดียว ที่ anchor อ้างอิง)

| ขั้น | pc bytes | framed bytes | `last_index` ของขั้น | ขึ้นกับ anchor ไหม |
|---|---|---|---|---|
| **3** (CONTROL) | **504** | **517** | `91` | 🟢 **ไม่ขึ้น** — สมาชิกถูกพินเป็น `P0/P30/P91` เป๊ะ · **v141 self-test พินเลข 504/517 ไว้เองที่ `v141:6104-6107`** |
| **20** | **3,148** | **3,161** | `82` | 🟡 สมาชิกขึ้นกับ anchor **แต่ที่ `V134` และ `V135` เป็นชุดเดียวกัน** |
| **60** | **9,302** | **9,315** | `103` | 🟡 เหมือนกัน — ขนาดตรงกันทั้งสอง anchor |
| **115** (ทั้งสำมะโน) | **17,928** | **17,942** | `142` | 🟢 **ไม่ขึ้น** — สมาชิกคือทั้งสำมะโน |

- **ที่มาของเลข:** `scenarios/world_population_full_001.json` -> `staircase.rungs` (ตรวจโดยเทสอยู่แล้ว) · **ผู้เทสอ่านจาก pin ของ commit ที่บูตจริง ไม่ใช่จากใบนี้**
- **[คำทำนาย · เหตุผลอ่านมาจาก encoder ห้ามถือเป็นข้อเท็จจริงจนกว่าจะเห็น]** `pc` เป็น **การต่อไบต์ตรง ๆ ไม่ถูกบีบอัด** (`make_runtime_remote_actors`) และ `frame_pc()` ห่อด้วย snappy raw **literal** ⇒ **ยอดรวมไม่ขึ้นกับลำดับสมาชิก** ⇒ ขั้น 3 และขั้น 115 ต้องได้เลขข้างบน **เป๊ะ ไม่ว่าจะยืนตรงไหน**
  🔴 **ถ้าขั้น 3 หรือ 115 ได้เลขอื่น = เรื่องใหญ่ ให้หยุดและรายงานทันที** (แปลว่าสมาชิกไม่ใช่ชุดที่คิด หรือ encoder ขยับ)
- **ขั้น 20 / 60:** เลขที่เห็นจริงจะ **ไม่** ตรงตารางถ้า anchor ไม่ใช่ anchor อ้างอิง ⇒ **ให้ส่ง XYZ ที่ decode ได้กลับมา แล้วให้ chief re-derive ด้วย `staircase_report(legacy, player_xyz)` แบบ headless** · 🔴 **"ไม่ตรงตาราง" ในกรณีนี้ไม่ใช่ความผิดพลาด และห้ามเขียนว่าเป็น**
- **เรื่องขั้น 20 กับ V94 — 🔴 อย่าเรียกว่า "ตัวคุม" มันอ่อนกว่านั้น:** ที่ anchor อ้างอิง ขั้น 20 บังเอิญมี **สมาชิกชุดเดียวกับ** V94 nearest-20 **แต่คนละไบต์ คนละลำดับ และที่ anchor อื่นก็คนละชุด** ⇒ **ไม่มี anchor ไหนที่ขั้น 20 ของเราเท่ากับเฟรมที่ไคลเอนต์เคยรับจริง** · ให้ chief เทียบ `set(rung20)` กับ `build_port_royal_initial_population(legacy, anchor)` ที่ anchor จริง แล้วรายงาน symmetric difference · **ต่างกันได้ ไม่ใช่บั๊ก**
- **ขั้น 115 ผูกกับของเดิมด้วยไบต์ ไม่ใช่ด้วยเซ็ต:** เฟรมของเราต้องใหญ่กว่า `V73_PORT_ROYAL_GOLDEN_POPULATION_115` (v141:1441) **เท่ากับความยาวชื่อ `Tornado Eagle` พอดี (31 ไบต์) ไม่มากไม่น้อย** (`tests/test_world_population.py::test_top_rung_differs_from_the_frozen_golden_115_by_p30_alone`) ⇒ census ของสาย A ไม่ใช่ชุดที่ใครเลือกขึ้นใหม่
- 🔴 **หนึ่งบูตมี SENT สองใบ ไม่ใช่ใบเดียว** — เส้นทางที่ ship อยู่คิว `..._INITIAL_READY` ที่ `0.0` และ `..._REAPPLY_READY` ที่ `+3.00` วินาที ⇒ **จดทั้งสองใบ พร้อมขนาดทั้งสองใบ** · **label ที่พิมพ์จริงหลังต่อสายอาจเปลี่ยนชื่อ — จดตัวอักษรที่เห็น ห้ามเดาว่าเหมือนเดิม**

---

### 🔴🔴 ความเสี่ยงที่ใหญ่ที่สุดของชั้นตา — **มีจดหมาย attended จากคืนเดียวกันบอกว่าพื้นตรง `P0` ว่างเปล่า**

`notes_to_chief\20260825_2145_GT072-RESULT-occlusion-and-replace-both-fail-plus-Z0-over-water.md` (`OBSERVER_CONFIRMED` แล้ว · ~4 ชั่วโมงก่อนใบนี้ถูกเขียน):
- ผู้เทสเดินไปที่ `X -9,299 Y -2,537` — **ห่างจาก `P0` ประมาณ 159 หน่วย** — เฟรมที่ `t=668.9` เห็น *"พื้นหินโล่ง ไม่มี NPC ไม่มีโมเดล ไม่มีอะไรเลย"*
- `Tab` ที่จุดนั้นไม่เลือกอะไรเลย · คำตัดสิน chief R170: *"แต่การวัดเกิดตอนฉากว่างอยู่แล้ว"*
- และ `R169` ข้อ D2: จากพิกัดรอบสี่ **`P0` เป็นตัวที่ใกล้เป็นอันดับสาม ไม่ใช่อันดับหนึ่ง**

🔴 **ผลต่อใบนี้:** **ขั้น 3 คือ `P0/P30/P91`** ⇒ ถ้าขั้น 3 ไม่ทำให้เห็นอะไรบนจอเลย **ทุกขั้นก็จะไม่เห็นอะไรเหมือนกัน ไม่มีขั้นไหน "พัง" และชั้นตาจะกลายเป็นศูนย์ทั้งใบโดยที่เทสฝั่งโค้ดเขียวหมด**
🎯 **ดังนั้นข้อ 9 (VP-B) เป็น *ด่านคุมของชั้นตา* ไม่ใช่ของแถม:**
- **ถ้าที่ VP-B ขั้น 3 เห็น `P30 Tornado Eagle` (ป้ายชื่อ/HP)** ⇒ ชั้นตาใช้งานได้ เดินต่อได้เต็มใบ
- **ถ้าที่ VP-B ขั้น 3 ไม่เห็นอะไรเลยสักตัว** ⇒ **จดว่า `VISUAL-LAYER-VOID` แล้วเดินบันไดต่อ "โดยอ่านเฉพาะชั้นสาย"** · 🔴 **ห้ามหยุดทั้งใบ** (ชั้นสายยังตอบคำถามเพดานได้) · 🔴 **และห้ามเขียนว่า "ส่งไปแล้วไม่ขึ้น" เป็นผลลบของ BUILD-001** — มันเป็นอาการของ `GT-072` ที่ยังเปิดอยู่ ให้ส่งตัวเลขและภาพไปที่ใบนั้น

### 🔴 ท่ากล้อง ทิศหัน และการเดิน (คำต่อคำจาก `GT-074` · ค่าใช้จ่ายของการเขียนผิดคือสามรอบ attended ที่เสียไปแล้ว)

| ท่า | ทำอะไรจริง | ยิง `TargetPosVital` ไหม | ใบนี้ใช้ได้เมื่อไร |
|---|---|---|---|
| **คลิกขวาค้างลากเมาส์** | หมุน **มุมกล้อง** อย่างเดียว · **ทิศหันของตัวละครไม่ขยับ ไม่มีอะไร trigger** | 🟢 ไม่ยิง | ✅ ใช้ได้ทุกจังหวะ **รวมถึงก่อนก้าวแรก** · **และเป็นตัวเช็ค NO-CRASH ของใบนี้** |
| **`Q` / `E`** | **หันตัวละคร** กล้องแพนตาม | 🔴 ยิง | ❌ **ห้ามใช้ก่อนก้าวแรก** (จะกลายเป็นตัวยิง anchor เอง) · หลังก้าวแรกใช้ได้แต่ **จดเวลา** · 🔴 **ห้ามใช้เป็นตัวเช็ค NO-CRASH เด็ดขาด** |
| **`W/A/S/D`** | เดิน (เปลี่ยนทั้งตำแหน่งและทิศหัน) | 🔴 ยิง | ✅ **ก้าวแรก = ตัวยิง collection ของรอบนี้** · หลังจากนั้นเดินได้เต็มที่ (ต้องเดินเพื่อดูเมือง) |
| **ล้อเมาส์ (ซูม)** | ซูมกล้อง | **[UNKNOWN — ไม่มีใครเคยวัด]** | ใช้ได้ · **จดเวลาที่ซูมทุกครั้ง** · 🔴 **ตั้งระดับซูมของ VP ให้เท่ากันทั้งสี่บูต ไม่งั้นจำนวนโมเดลในเฟรมเทียบข้ามบูตไม่ได้** |

🔴 **ประโยคเดียวที่ต้องจำ: ตัวที่ยิง `TargetPosVital` คือ "การเปลี่ยนทิศหันของตัวละคร" ไม่ใช่ "การขยับกล้อง"**

### 🔴 เรื่องแชต — **เลนนี้ไม่มี trigger แชต**
- **ห้ามพิมพ์แชตทั้งรอบ** · ตัวยิงของเลนนี้คือ **การเดิน** ไม่ใช่ข้อความ
- 🔴 **ตัวอักษรที่พิมพ์ตอนช่องแชตไม่โฟกัส = ฮอตคีย์** ⇒ มือออกจากคีย์บอร์ดเมื่อไม่ได้เดิน
- (บันทึกไว้เพื่อกันคนหยิบ playbook ใบอื่นมาใช้ผิด: predicate แชตของเลนอื่นคือ **printable ASCII 12 ตัวเป๊ะ** · สั้น/ยาวกว่านั้นถึงเซิร์ฟเวอร์แต่เงื่อนไขเงียบ ๆ ไม่ผ่าน — **แต่ใบนี้ไม่ใช้มันเลย**)

---

### steps (คลิกต่อคลิก · **ทำซ้ำสี่รอบ เปลี่ยนแค่ `<RUNG>` และไฟล์ DB — ห้ามเปลี่ยนอย่างอื่นแม้แต่อย่างเดียว**)

**ลำดับบูตบังคับ: `3` -> `20` -> `60` -> `115`** (ถูกที่สุดก่อน · ขั้น 3 เป็นตัวคุมที่พิสูจน์ว่าแท่นดีก่อนจะปีน)

**ก่อนเริ่มทั้งการนั่ง:** ถือ `LOCK_GAME` · preflight จอว่าง (`staged\TEMPLATE_preflight_unattended.ps1` — เจอหน้าต่าง elevated = ABORT ทั้งรอบ) · เทียบ sha canonical · copy DB ครบสี่ใบ · **เตรียม teardown จาก `TEMPLATE_teardown_generic.ps1` เป็นหลัก** (ถ้าก๊อปจากจ็อบที่เป็นตัวเลข **ต้องเปิดดูบรรทัดที่ 17 ให้เห็น `-replace '\\','/'` ก่อนเสมอ** · 🔴 **ห้ามก๊อปจาก `1103`/`1105`**)

**ต่อหนึ่งบูต:**

1. **จด boot stamp (+07:00) ของบูตนั้น** — 🔴 **หนึ่ง stamp ต่อหนึ่งบูต ไม่ใช่ stamp เดียวทั้งการนั่ง** (teardown template ปฏิเสธ stamp ที่เก่ากว่า **420 นาที** · `TEMPLATE_teardown_generic.ps1:135` · เพดานถูกยกจาก 180 เมื่อ 2026-08-20 — **เลข 180 ในใบเก่า = stale**)
2. **สตาร์ตเซิร์ฟเวอร์ก่อน แล้วค่อยบูต client เสมอ** (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client)
   - 🔴 client ที่บูตโดยไม่มีเซิร์ฟเวอร์ **ตายเองใน ~3.5 นาที**
   - 🔴 **ถ้าต้องฆ่า client กลางคัน ต้อง restart server ก่อนเปิด client ตัวใหม่เสมอ** (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่ "connecting" ตลอดกาล) — 🔴 **ใบนี้บูตสี่ครั้ง ⇒ ข้อนี้จะถูกใช้จริงสามครั้ง ปิด server ทุกครั้งระหว่างบูต**
   - จัดหน้าต่าง console ให้เห็นข้างจอเกมโดยไม่บังพื้นที่วัด · **ตลอดรอบห้ามคลิก console**
3. **อ่านบรรทัดจำนวน actor ที่คอนโซลพิมพ์ตอนบูต แล้วจดตัวอักษรเป๊ะ ๆ** — 🔴 **ไม่ตรงกับขั้นที่ตั้งใจ หรือไม่มีบรรทัดนี้ = หยุด ปิด server บูตนั้นเป็น NO-RESULT**
4. เปิด client → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร → **เลือกช่องแรก** → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (🔴 **ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด**)
5. เข้าแมพ เห็น HP/minimap/ชื่อแมพ → **เริ่มอัดวิดีโอต่อเนื่องตรงนี้ ยาวจนจบ session** (`staged\TEMPLATE_video_recorder.ps1 -FrameRate 30` ลง `evidence_video\`) · จดบรรทัด `VIDEO START pid= start= fps= path=` (🔴 `start=` **ห้ามใช้เป็นสมอเวลา**) · 🔴 **ไม่ได้อัด = NO-RESULT ทันที**
6. **ยืนนิ่งที่จุดเกิด อย่าเพิ่งเดิน** → **จด X/Y/Z จาก HUD** → **คลิกขวาลากกวาดกล้องรอบตัวช้า ๆ หนึ่งรอบ ค้างทุก ~90 องศา อย่างละ 4 วินาที** → 🔴 **นี่คือภาพ "ก่อนมีประชากร" ของบูตนั้น** (collection ยังไม่ถูกส่ง เพราะยังไม่มี `TargetPosVital`)
   - **นับโมเดล NPC ที่เห็นในรอบกวาดนี้แล้วจดเป็นตัวเลข** — คาดว่า **0**
7. 🎯 **ก้าวแรก = ตัวยิง:** **แตะ `W` สั้น ๆ ครั้งเดียวแล้วปล่อย** → **มือออกจากคีย์บอร์ด ยืนนิ่ง 10 วินาที**
   - **จดเวลาจริง (+07:00) ของก้าวแรก = `T0` ของบูตนั้น**
   - **เฝ้าดูจอตลอด 10 วินาที** — collection ใบแรกมาที่ `~T0+0` และใบ reapply ที่ `~T0+3`
   - 🔴 **พูดออกเสียงทันทีที่เห็นอะไรโผล่** (มีสมอในไฟล์เสียง) · **อย่าพยายามถ่ายให้ทันเหตุการณ์ วิดีโอคือกรรมการ**
8. **VP-A (ยืนที่เดิม ไม่เดิน):** กวาดกล้องรอบตัวอีกหนึ่งรอบ **ค้างมุมละ 4 วินาที มุมเดียวกับข้อ 6** → **นับโมเดล NPC ที่เห็นได้แต่ละมุม แล้วจดเป็นตัวเลขต่อมุม**
   - 🔴 **ใช้คลิกขวาลากเท่านั้น ห้าม `Q`/`E`** — VP-A ต้องเทียบกับข้อ 6 ได้ และการหันตัวจะเปลี่ยนกรอบภาพ
9. **VP-B:** เดินไปที่ landmark NPC `Navy Transfer` (`P0` X `-9139.957` Y `-2780.045` Z `223.292`) **ยืนห่าง ~200-300 หน่วย ฝั่งที่เห็นตัวเต็ม ๆ** (จุดอ้างอิงที่ใช้ได้จริง: `(-8876,-2715)` = ห่าง `271.9` จาก `GT-030-R3`) · **จด X/Y จาก HUD** · กวาดกล้องรอบตัว ค้างมุมละ 4 วินาที · **นับโมเดลต่อมุม**
   - 🎯 **ที่ VP-B ให้ยืนยัน `P30 "Tornado Eagle"` ด้วยตา: ป้ายชื่อขึ้นไหม · หลอด/ตัวเลข HP ขึ้นไหม** (P30 อยู่ในทุกขั้น ⇒ มันคือหมุดที่ต้องเหมือนกันทั้งสี่บูต)
10. **VP-C:** เดินลึกเข้าไปในย่านที่มีสิ่งปลูกสร้างอีก ~600-800 หน่วย แล้วหยุด · **จด X/Y จาก HUD** · กวาดกล้องรอบตัว ค้างมุมละ 4 วินาที · **นับโมเดลต่อมุม**
    - 🔴 **บูตแรก (ขั้น 3) เป็นคนกำหนด VP-C** — จด X/Y ไว้ **แล้วสามบูตที่เหลือต้องกลับมายืนที่ X/Y เดิม (คลาดได้ ~30 หน่วย จดค่าจริงทุกครั้ง)**
    - 🔴 **VP ทั้งสามต้องเป็นจุดเดิมและระดับซูมเดิมทั้งสี่บูต** — นี่คือสิ่งเดียวที่ทำให้ "นับโมเดลเทียบข้ามขั้น" มีความหมาย
11. **เดินสำรวจเมืองอย่างอิสระ 3-4 นาที** — เก็บภาพรวมว่า "เมืองมีคนหรือเมืองร้าง" · **พูดออกเสียงระหว่างเดิน** · 🔴 **ห้ามลงน้ำ ห้ามออกนอกเมือง**
12. **ถ่ายภาพนิ่ง full-res ด้วยเครื่องมือนอกเกม อย่างน้อยสามใบต่อบูต** (VP-A / VP-B / VP-C) → `GT076_R<RUNG>_<VP>_FULLRES_<yyyyMMdd_HHmmss>.png`
    - 🔴 **ใบพวกนี้มีไว้เพื่ออ่าน *สี* ป้ายชื่อ (PLAYBOOK ข้อ 13) และเพื่อ *นับ* หัวจากภาพเต็มความละเอียด** · 🔴 **ห้ามกดคีย์ใด ๆ ในหน้าต่างเกมเพื่อถ่ายภาพ**
13. **NO-CRASH / CRASH:** **คลิกขวาค้างลากเมาส์แล้วกล้องหมุน = NO-CRASH** · หลุด/ค้าง/ภาพแข็ง = CRASH + **จดว่าเกิดหลัง SENT ใบไหน และกี่วินาทีหลัง `T0`** · 🔴 **ห้ามใช้ `Q`/`E` เป็นตัวเช็ค**
14. ออกจากเกม: **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย → **หยุดวิดีโอ** → **ปิดเซิร์ฟเวอร์ด้วยเสมอ**
15. เก็บ **raw GAME log ทั้งไฟล์** (`...\capture_v141\GAME_LIVE.txt`) + console out/err ทั้งหมด (ทุกบรรทัด `[G>]` / `PF-EVENT` / `ErrorData`) → `PRAGMA integrity_check;` บนสำเนา → sha256 ทุกไฟล์
16. **teardown ของบูตนั้นทันที** (ใช้ boot stamp ของบูตนั้น) → เทียบ sha canonical กับ `CANON_SHA.txt`
17. **ไปบูตถัดไป** — 🔴 **restart server เสมอ · DB สำเนาใบใหม่เสมอ**

**หลังครบทุกบูต:**
18. **แตกเฟรมจากวิดีโอ (ห้ามข้าม · 🔴 ห้ามมี `scale=` ในบรรทัดคำสั่งเด็ดขาด):**
```
$mkv = '<path full of the FULLROUND .mkv of that boot>'
ffmpeg -ss <T0 - 20.00> -i $mkv -t 40.00 -vsync 0 GT076_R<RUNG>_T0_%03d.png
```
19. 🔴🔴 **G-OBS — ขั้นสุดท้าย บังคับ:** ก่อนเขียนผลลงคิว/จดหมาย **ผู้ช่วยต้องทวนรายการ "สิ่งที่ผู้ช่วยเห็น" ให้ผู้เทสยืนยันทีละข้อ** (เมืองเต็ม/ไม่เต็มในแต่ละบูต · จำนวนที่นับได้ต่อ VP ต่อบูต · `Tornado Eagle` มีชื่อ/มี HP ไหมทุกบูต · ค้าง/สะดุด/หลุดไหม · **สีป้ายทุกป้าย**)
    - ผู้เทสตอบเป็นคำเดียวต่อข้อ: **"ตรง" / "ไม่ตรง" / "ฉันไม่ได้ดูข้อนั้น"**
    - จดหมายผลต้องมีบรรทัดนี้ตัวอักษรเป๊ะ: `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`
    - 🔴 **ยังไม่ยืนยัน = ห้ามเขียนผลลงคิว** · 🔴 **บรรทัดนี้เป็น "ขั้นตอน" ไม่ใช่ "หลักฐาน" ห้ามใช้แทนเกณฑ์ผ่านชั้นใดชั้นหนึ่ง**

---

### ⛔ STOP RULE — **ขั้นไหนพัง หยุดปีนทันที**

1. **ขั้นพัง** = อย่างใดอย่างหนึ่ง: มี `ErrorData` ตามหลัง collection · client หลุด/ค้าง/ไม่เข้าแมพ · การสื่อสารหยุดเดินหลัง collection
2. **จดขั้นที่พังให้ละเอียดที่สุด** (label · ขนาด pc/framed · เลข `ErrorData` เป๊ะ ๆ · เกิดหลัง SENT ใบไหน · กี่วินาทีหลัง `T0`)
3. **รันขั้นเดิมซ้ำ *หนึ่งครั้ง* ด้วย `state\run_gt076_r<N>_confirm.sqlite3`** เพื่อดูว่าทำซ้ำได้ไหม
4. **แล้วหยุด** — 🔴 **ห้ามปีนขั้นถัดไป ห้ามลองเลขระหว่างกลางเอง**
   ⇒ **เพดานอยู่ระหว่าง "ขั้นที่ดีขั้นสุดท้าย" กับ "ขั้นที่พัง"** และรอบถัดไปเป็นคนบีบช่วงนั้น (นั่นคือใบใหม่ ไม่ใช่ใบนี้)
5. 🔴 **ทำซ้ำไม่ได้ (รอบยืนยันผ่านเฉย ๆ) ก็ยังเป็นผล** — จดว่า "พังหนึ่งในสอง" แล้วหยุดเหมือนเดิม **ห้ามรันครั้งที่สาม**
6. 🔴🔴 **คาดไว้ก่อนเลย: `ErrorData=28317` มาพร้อมกับ "ไคลเอนต์ปิดการเชื่อมต่อทั้งสองเส้น"** (รายงาน `PF_DELETE_SOFT002...` §(c)4) ⇒ **เซสชันนั้นตายทันที** · **รอบยืนยันคือบูตใหม่** ⇒ **จด XYZ ของบูตยืนยันด้วย** เพราะมันคือ anchor ใหม่ · ถ้า XYZ ต่างจากบูตที่พัง **ให้ chief ตรวจด้วย `nesting_break()` ก่อนอ่านผลเทียบกัน**

---

### คำทำนาย (**คำทำนายคือคำทำนาย · คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว** · ท่องก่อนบูต)

- **P1 [คำทำนาย · ตัวคุม]** ขั้น 3 ได้ **pc 504 / framed 517** เป๊ะ และ **ไบต์เหมือนที่เซิร์ฟเวอร์ส่งอยู่ทุกวันนี้ทุกประการ** ⇒ **จอต้องหน้าตาเหมือนบูตปกติที่เจ้าของเคยเห็น**
- **P2 [คำทำนาย]** ขั้น 20 ผ่าน — เพราะไคลเอนต์เคยรับ 20 มาแล้ว (V94) · 🔴 **แต่สมาชิกอาจคนละชุด ⇒ ผ่านที่ 20 ไม่ใช่ของแถมฟรี**
- **P3 [คำทำนาย · ข้อที่ไม่มีใครรู้จริง ๆ]** ขั้น 60 และ 115 **ผ่านทั้งคู่ ไม่มี `ErrorData`** — 🔴 **นี่คือการเดา ไม่ใช่ความรู้** · ถ้าผิด **นั่นคือผลที่มีค่าที่สุดของรอบ**
- **P4 [คำทำนาย]** ขั้น 115 ได้ **pc 17,928 / framed 17,942** เป๊ะ ไม่ว่ายืนตรงไหน
- **P5 [คำทำนาย · client-observable · 🔴 แก้แล้วหลังวัดความหนาแน่นของตาราง]** **ภาพที่จุดเกิดจะ *เหมือนกัน* ทั้งขั้น 20 / 60 / 115** เพราะตัวที่เพิ่มมาอยู่ห่าง 13,000-39,000 หน่วย ⇒ **สิ่งที่ทำนายคือ "จำนวนที่นับได้ไม่ลดลง" ไม่ใช่ "เมืองแน่นขึ้น"** · 🔴 **ใครเขียนว่าคาดหวังเมืองแน่นที่จุดเกิด คนนั้นยังไม่ได้อ่านบล็อกความหนาแน่น**
- **P6 [คำทำนาย]** `P30 "Tornado Eagle"` **ยังมีป้ายชื่อและ HP เหมือนวันนี้ทุกขั้น** (มันอยู่ในทุกขั้น และ encoder ไม่ได้แตะ)
- **P7 [คำทำนาย · จดสีอย่างเดียว ห้ามสรุปสาเหตุ]** ป้ายชื่อ NPC เป็น **เหลือง** ตามภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับ
- **P8 [คำทำนาย]** ไม่มี `ErrorData=28317` ปรากฏที่ขั้นใดเลย — 🔴 **ถ้าโผล่ ให้จดเลขเป๊ะ ๆ และหยุดตาม STOP RULE** (เลขนี้คือเลขในประวัติศาสตร์ของ V43 · **การเจอมันซ้ำไม่ได้แปลว่าเป็นสาเหตุเดียวกัน**)

---

### pass criteria — **สองชั้น แยกกันเด็ดขาด 🔴 ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

**ชั้น (1) wire/DB + หลักฐานเชิงไฟล์ — ทำ headless ได้ ไม่ต้องมีคนหน้าจอ**
1. **ต่อบูต:** `BOOT_COMMIT` + ผลด่านก่อนบูตห้าข้อ + **บรรทัดจำนวน actor ที่คอนโซลพิมพ์ (ตัวอักษรเป๊ะ)**
2. **ต่อบูต:** **label ของ SENT ทุกใบ (คาดว่าสองใบ: initial + reapply ที่ ~`+3.00` วิ) + `pc bytes` + `framed bytes` ของแต่ละใบ** — เทียบตารางเลขคาดหมาย **ทีละใบ ห้ามยุบรวม**
3. **ต่อบูต:** **XYZ ที่ decode ได้จาก `TargetPosVital` ใบแรก (f32 จาก hexdump)** 🔴 **ห้ามใช้ HUD เป็นฐานคำนวณ** — **ไม่มีค่านี้ = บูตนั้นอ่านไม่ได้ = NO-RESULT ของบูตนั้น**
4. **ต่อบูต:** **มี `ErrorData` ตามหลัง collection ไหม** — มี ⇒ **จดเลขเป๊ะ ๆ** + จดว่าหลัง SENT ใบไหน + กี่วินาทีหลัง `T0`
5. **ต่อบูต:** **traffic ที่คาดว่าจะมาต่อ ยังมาไหม** — จด **บรรทัดถัดไปหลัง collection ทั้งขาเข้าและขาออก พร้อมเวลานาฬิกาจริง** · และ **ตอนผู้เทสเดิน `TargetPosVital` ยังวิ่งออกไหม** (นี่คือหลักฐาน "socket ยังมีชีวิต" ของชั้นสาย 🔴 **คนละอันกับ NO-CRASH ซึ่งเป็นของชั้น (2)**)
6. **ต่อบูต:** **census: นับ *ทุก* บรรทัด `[G>]` ทั้งไฟล์แล้วรายงานยอดรวม ไม่กรองอะไรออก** · ไม่มี traceback / stderr
7. **DB สำเนาทุกใบ:** `PRAGMA integrity_check` = `ok` · row-diff ต่างเฉพาะ `sessions` **+1 ต่อการเข้าเกมหนึ่งครั้ง** · `max(lease_generation)` ก่อน-หลังไม่ถอยหลัง · **sha256 canonical ก่อน-หลัง = `CANON_SHA.txt`** · **canonical ไม่ถูกเปิดตลอดรอบ**
8. **ความครบของวิดีโอ (กฎ S):** `ffprobe` → เฟรมจริงเทียบ `duration x fps` · **รายงานเฟรมที่หายเป็นตัวเลข** 🔴 **ข้อนี้บอกว่าไฟล์ครบแค่ไหน ไม่ได้บอกว่าในเฟรมมีอะไร**
9. 🔴🔴 **ชั้นนี้ตอบไม่ได้ — เขียนไว้ให้ชัดเพราะใบนี้ล่อให้ทำผิดข้อนี้เป็นพิเศษ:**
   - **"ไคลเอนต์ *แสดง* actor กี่ตัว"** — ชั้นสายเห็นแค่ว่า **ส่งไปกี่ตัว** · **ส่ง 115 แล้วไม่มี `ErrorData` ไม่ได้แปลว่ามี 115 ตัวบนจอ แม้แต่นิดเดียว**
   - **"เมืองมีชีวิตหรือยัง"** — เป็นเกณฑ์ของตาเจ้าของ ไม่ใช่ของ log

**ชั้น (2) client-observable — ต้องมีคนหน้าจอ · 🔴 ตัวปิดใบอยู่ชั้นนี้ชั้นเดียว**
1. **หลักฐานบังคับต่อบูต:** วิดีโอต่อเนื่องตั้งแต่ก่อนเข้าแมพจนออกจากเกม · ภาพนิ่ง full-res อย่างน้อยสามใบ (VP-A/B/C) · **sha256 ทุกไฟล์**
2. 🎯 **คำตัดสินหลัก ตอบเป็นคำพูดตรง ๆ ต่อบูต (หนึ่งบรรทัดต่อบูต ห้ามยุบรวมสี่บูต):**
   **"เมืองมีคนทั่วเมือง" / "มีคนบ้างแต่บาง" / "เมืองร้างเหมือนเดิม" / "ดูไม่ได้"**
3. 🎯🔴 **ตารางนับหัว — และ *เกณฑ์อ่านที่ถูกแก้แล้ว* หลังวัดความหนาแน่นของตาราง:**
   - **หนึ่งแถวต่อ (บูต x VP x มุมกล้อง)** · ช่อง: **จำนวนโมเดล NPC ที่เห็นได้ชัด** · **อ่านจากภาพ full-res** · **จดเป็นตัวเลข**
   - 🔴 **ตัวเลขนี้เป็น *ขอบล่าง* เสมอ ห้ามเขียนว่า "มีอยู่ N ตัว"** — เขียนว่า **"เห็นอย่างน้อย N ตัวจากมุมนี้"**
   - 🔴🔴 **เกณฑ์เดิมที่ว่า "นับได้เท่าเดิม = เพดาน render" ถูกยกเลิก** — ตารางถูกวัดแล้ว: ที่จุดเกิดมี placement ในรัศมี 2,000u แค่ **2 ตัว** ⇒ **ขั้น 20 / 60 / 115 ให้ภาพเหมือนกันที่จุดเกิด และนั่นคือสิ่งที่คาดไว้แล้ว** ⇒ **"นับได้เท่าเดิม" ไม่ใช่หลักฐานของอะไรทั้งสิ้นในเลนนี้ ห้ามรายงานเป็นเพดาน**
   - 🎯 **สิ่งที่ตารางนับหัวยังมีค่าจริง ๆ สองข้อ:**
     ① **นับได้ *น้อยลง* เมื่อขึ้นขั้น** ⇒ ผิดคาดจริง **เรื่องใหญ่** (เข้าข่าย actor-slot displacement ของ `GT-072` ที่ยังเปิดอยู่) จดละเอียดที่สุด
     ② **ที่ `VP-B` (ข้าง `P0`) จำนวนต้องไม่เป็นศูนย์ทุกขั้น** — นี่คือ **ตัวคุมว่าไคลเอนต์ยังเรนเดอร์อะไรอยู่เลย** ดูบล็อกความเสี่ยง `GT-072` ข้างล่าง
4. **`Tornado Eagle` (P30) ต่อบูต:** **ป้ายชื่อขึ้นไหม (อ่านตัวอักษรที่อ่านได้ออกมา)** · **HP ขึ้นไหม** · **เหมือนหรือต่างจากบูตก่อนหน้า**
5. **อาการของไคลเอนต์ต่อบูต:** ค้าง / กระตุก / โหลดช้าตอน collection มาถึง / dialog error (**คัดข้อความบน dialog มาทั้งบรรทัด**) / หลุด — **จดเวลาสัมพัทธ์กับ `T0` ทุกอาการ**
6. **ตารางสีป้ายชื่อครบทุกป้ายทุกภาพ full-res** (PLAYBOOK ข้อ 13 · **"ไม่มี" เขียนออกมาเป็นตัวอักษร ห้ามเว้นว่าง** · 🔴 **อ่านจากภาพนิ่ง full-res/crop PNG เท่านั้น ห้ามอ่านจากวิดีโอ/ภาพย่อ/contact sheet**)
   - 🔴 **ถ้าป้ายเยอะจนจดไม่ไหวที่ขั้น 60/115: จดให้ครบทุกป้าย *ในภาพ full-res ของ VP-B* เป็นอย่างน้อย แล้วเขียนออกมาเป็นตัวอักษรว่าภาพไหนจดไม่ครบและเพราะอะไร** — 🔴 **ห้ามเว้นว่าง ห้ามเขียนว่า "เยอะเกิน" เฉย ๆ**
7. **NO-CRASH / CRASH verdict ต่อบูต** (ตัดสินด้วย **คลิกขวาค้างลากเมาส์** เท่านั้น)
8. 🔴 **ใบปิดด้วยผลลบได้เฉพาะรอบที่ *คุณ Panya เห็นเอง* + มีวิดีโอต่อเนื่อง** (`AGENTS.md` §9)
9. 🔴 **ชั้นนี้ตอบไม่ได้:** ส่งไปกี่ตัว · ไบต์เท่าไร · anchor อยู่ที่ไหน · มี `ErrorData` ไหม — **ทั้งหมดนี้ยืนยันด้วยชั้น (1) เท่านั้น** · 🔴 **"ผมเห็นคนเยอะมาก" ไม่ใช่หลักฐานว่าส่ง 115 และ "ผมเห็นน้อย" ก็ไม่ใช่หลักฐานว่าส่งไม่ครบ**

🔴 **ถ้าชั้น (1) ไม่ผ่าน (คอนโซลไม่พิมพ์จำนวน · ขั้น 3 ไบต์ไม่ตรง 504/517 · decode anchor ไม่ได้ · ไม่ได้อัดวิดีโอ · ใช้ DB ซ้ำใบ) ⇒ บูตนั้นเป็น NO-RESULT ทางเทคนิค ห้ามอ่านจอเป็นผลใด ๆ แม้จะเห็นชัด ๆ**

---

### ตารางผลลัพธ์ที่มีชื่อ — **ทุกทางออกอ่านได้**

| # | สิ่งที่เห็น | คำตัดสินของใบ | อนุญาตให้สรุปว่า | 🔴 **ไม่** อนุญาตให้สรุปว่า / redirect |
|---|---|---|---|---|
| **N1** CEILING-AT-OR-ABOVE-CENSUS | สี่ขั้นผ่านหมด ไม่มี `ErrorData` ไม่ crash | ✅ **PASS** | ว่า **ไคลเอนต์รับ 115 actor ใน collection เดียวได้ ที่ anchor นี้ บนบิลด์นี้** ⇒ เติม `MEASURED_CLIENT_ACTOR_CEILING` ไม่ได้ **แต่ปลดค่า default เต็มสำมะโนได้** | ❌ **ห้ามเขียนว่า "ไม่มีเพดาน"** — 115 คือเพดานของ *สำมะโน* ไม่ใช่ของไคลเอนต์ · **redirect:** ส่งเลขให้ chief ตัดสินว่าจะ ship 115 เป็น default ไหม (chief ตัดสิน ผู้เทสไม่ตั้ง) |
| **N2** CEILING-MEASURED-PARSE 🎯 | ขั้น N ผ่าน ขั้นถัดไปมี `ErrorData` / หลุด / เงียบ · **ทำซ้ำแล้วหนึ่งครั้ง** | ✅ **PASS — นี่คือผลของใบ ไม่ใช่ FAIL** | ว่า **เพดานอยู่ในช่วง [N, ขั้นที่พัง)** และ **default ต้องไม่เกิน N จนกว่าจะบีบช่วง** | ❌ **ห้ามรายงานเป็น FAIL · ห้าม "ไปแก้ให้ผ่าน" · ห้ามชี้สาเหตุ** (ขนาดเฟรม? จำนวนสมาชิก? โมเดล? หน่วยความจำ? — ไม่ได้วัดสักอย่าง) · **redirect:** ใบใหม่บีบช่วงระหว่าง N กับขั้นที่พัง |
| **N3** SAME-PICTURE-EVERY-RUNG (**ผลที่คาดไว้ ไม่ใช่การค้นพบ**) | ทุกขั้น parse ผ่าน **และจำนวนที่นับได้ที่ VP เดิมไม่เพิ่มเลย** | ✅ **PASS ตามชั้นสาย · ชั้นตาไม่ให้ข้อมูลเพิ่ม** | ว่า **ขั้นบนถูกส่งและถูกรับ** และว่า **ภาพเหมือนกันตามที่ความหนาแน่นของตารางทำนายไว้** | ❌ **ห้ามเขียนว่าเป็นเพดานการเรนเดอร์** — ตัวที่เพิ่มมาอยู่ห่างเป็นกิโลเมตร ภาพเหมือนกันคือผลที่ทำนายไว้ตั้งแต่ก่อนบูต · **redirect:** อยากวัดเพดาน render ต้องมีใบที่พาผู้เล่นไปยืนที่กระจุกหนา (`P67`) ซึ่งต้องมี M2 ก่อน |
| **N3b** COUNT-WENT-DOWN 🔴 | จำนวนที่นับได้ที่ VP เดิม **ลดลง** เมื่อขึ้นขั้น | 🟡 **PARTIAL — ผลที่มีค่าที่สุดรองจาก N2** | ว่า **มีบางอย่างทำให้ actor ที่เคยเห็นหายไปเมื่อส่งเพิ่ม** | ❌ ห้ามชี้กลไก · 🔴 **ต่อกับ `GT-072` ACTOR-SLOT-DISPLACEMENT-001 ที่ยังเปิดอยู่ (PARTIAL) ห้ามยุบรวม** · **redirect:** ส่งตัวเลขและภาพให้ `GT-072` |
| **N4** CONTROL-BROKEN 🔴 | **ขั้น 3 เองไม่ตรง 504/517 หรือจอไม่เหมือนบูตปกติ** | 🔴 **NO-RESULT ทั้งใบ หยุดทันที** | ไม่มี | ❌ **ห้ามอ่านขั้นบนใด ๆ เลย ห้ามบูตต่อ** — แท่นหรือการต่อสายพัง · **redirect:** ส่ง chief ทันที · **🔴 ห้าม archive ใบ** |
| **N5** NON-OBSERVED | ไม่มีบรรทัดจำนวน actor · decode anchor ไม่ได้ · ไม่ได้อัดวิดีโอ · VP ไม่ตรงกันข้ามบูต · ซูมเปลี่ยน · ใช้ DB ซ้ำ | 🔴 **NO-RESULT — ไม่ใช่ผลลบเด็ดขาด** | ไม่มี | ❌ **"เห็นคนน้อย" ในเงื่อนไขนี้ไม่ใช่ผลของใบ** · **redirect:** รันซ้ำ commit เดิม แก้วินัยของบูต · **🔴 ห้าม archive ใบ** |
| **N6** CRASH | ไคลเอนต์หลุด/ค้าง | 🟡 ผลที่มีชื่อ **และมักจะเป็น N2 ในคราบอื่น** | จดว่าหลัง SENT ใบไหน กี่วินาทีหลัง `T0` ขั้นไหน | ❌ ห้ามชี้สาเหตุ · เก็บ console ทั้งไฟล์ · **restart server ก่อนบูตรอบถัดไป** |
| **N7** PARTIAL-STAIRCASE | เวลาหมด/เจ้าของเลิกเล่นก่อนครบสี่ขั้น | 🟡 **PARTIAL** | ว่า **ขั้นที่รันจริงให้ผลอะไร** | ❌ ห้ามเหมารวมขั้นที่ไม่ได้รัน · 🔴 **ใบยัง PENDING สำหรับขั้นที่ขาด ห้าม archive** · 🔴 **teardown ยังต้องทำ แม้รอบจบเพราะเลิกเล่น** |

---

### ⭐ PLAYBOOK ข้อ 13 — บันทึกสีของ **ทุกป้ายชื่อในเฟรม** (คำสั่งคุณ Panya 2026-08-25 · บังคับทุกใบ attended ตั้งแต่ R163)
- **จดอะไร:** ชื่อตัวเราเอง (เหนือหัว + แผง UI ซ้ายบน) · ชื่อ NPC/actor ทุกตัวในเฟรม · ชื่อไอเทมบนพื้น · ชื่อผู้เล่นคนอื่น · บรรทัด title/คำอธิบาย — **หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ**
- **ไม่มีให้เขียนคำว่า "ไม่มี" ออกมาเป็นตัวอักษร** 🔴 **ห้ามเว้นว่าง**
- **อ่านสีจากภาพนิ่งความละเอียดเต็ม / crop PNG เท่านั้น** 🔴 **ห้ามอ่านจาก contact sheet · ห้ามจากภาพย่อ · ห้ามจากวิดีโอ** ⇒ เก็บที่ `evidence_screens\GT076_R<RUNG>_<VP>_FULLRES_<yyyyMMdd_HHmmss>.png|jpg` (**ไฟล์ใหญ่เกินให้ crop จากต้นฉบับ ห้าม resize ลง**) · **sha256 ทุกไฟล์**
- **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับ:** NPC = **เหลือง** · ผู้เล่น = **เขียว** · ไอเทมบนพื้น = **ขาว** · title/คำอธิบาย = **ฟ้า** · ชื่อตัวเอง = **ขาว**
- 🔴🔴 **ผู้เทสจด "สี" อย่างเดียว ห้ามสรุปสาเหตุ** — **อะไรตัดสินสีของป้ายคือคำถามของ `RE-067` (ครึ่ง actor อยู่ที่ `RE-068`)** ⇒ **ห้ามเขียนว่า "แปลว่าไคลเอนต์จัดมันเป็นผู้เล่น/NPC/ศัตรู"**
- **`REAL_SERVER_DIVERGENCE.tsv`: 🔴 ส่งค่ากลับมาในจดหมายผล ห้ามแก้ไฟล์เองจากหน้าสะพาน** · หนึ่งแถวต่อหนึ่งป้ายที่เทียบ (คั่นด้วย **TAB** · อ่านหัวไฟล์ก่อน) · `evidence_layer` = **`eye`** เสมอ · `evidence_ref` = path ภาพ full-res · `evidence_sha256` **คนละคอลัมน์** · `open_ticket` = **`RE-067`** · `blocks_promotion` = `no` · **เติมแถวแม้ผลจะ "ตรงกัน"**

### เกณฑ์หยุดทั้งเลนทันที
⛔ `ErrorData` ใด ๆ ตามหลัง collection ⇒ **หยุดตาม STOP RULE เก็บ console ทั้งไฟล์** (`28317` = เลขในประวัติศาสตร์ของ V43 · **จดเลขที่เห็นจริง ห้ามเขียนว่า "น่าจะตัวเดียวกัน"**)
⛔ คอนโซลขึ้น label ของเลน scenario/hypothesis อื่น ⇒ **บูตผิดไฟล์ หยุด ปิด server**
⛔ ชื่อ `ProbeControl03` โผล่ที่ไหนก็ตาม ⇒ **หยุด เก็บ console ทั้งไฟล์** (ไม่ควรมีในเลนนี้เลย)

### 🧾 teardown + ใบเสร็จ (บังคับ — **แม้รอบจะจบเพราะคนเลิกเล่น ไม่ใช่เพราะเทสจบ**)
- **teardown เสมอ ภายใน 420 นาทีจาก boot stamp *ของบูตนั้น*** (`staged\TEMPLATE_teardown_generic.ps1:135` · เพดานถูกยกจาก 180 เมื่อ 2026-08-20 · **เลข 180 ในใบเก่า = stale**) — เกินเพดาน template **ปฏิเสธ exit 12 โดยดีไซน์**
- 🔴 **ใบนี้บูตสี่ครั้ง ⇒ ทำ teardown ทีละบูต อย่ารวบท้ายการนั่ง** (ไม่งั้น stamp ของบูตแรกจะแก่จนโดนปฏิเสธ)
- แท่นที่ถูกทิ้งข้ามชั่วโมง: **อย่าฝืน template** ⇒ `staged\TOOL_stop_stale_server.ps1` แล้วตามด้วย receipt อ่านอย่างเดียว `staged\0949_gt027_stalepad_canonical_guard.ps1`
- ได้ **exit 36** อย่าเดาเอง — แนบบรรทัดที่ 17 ของไฟล์ teardown ที่ใช้จริงมาทั้งบรรทัด
- **ใบเสร็จที่ต้องแนบมากับผล ทุกข้อ ทุกบูต:** `AFTER listeners = 0` · **canonical guard: sha256 ก่อน-หลัง = `CANON_SHA.txt`** · **teardown exit code** · `LOCK_GAME` ปล่อยแล้ว · run copy `state\run_gt076_*.sqlite3` **เก็บไว้ให้ chief re-derive ห้ามทิ้ง** · path ของ raw GAME log + console out/err + วิดีโอ + ภาพทุกไฟล์ พร้อม **sha256**
- 🔴 **บนสะพานเท่านั้น ห้ามลบ:** ไฟล์ `.mkv` ต้นฉบับสี่ไฟล์ และโฟลเดอร์ capture ของทุกบูต
- 🔴 **restart เซิร์ฟเวอร์ก่อนบูตรอบถัดไปเสมอ**

---

### nonclaims (ติดไปกับผลทุกกรณี ไม่ว่าบวกหรือลบ — **ห้ามตัดทิ้ง**)

① 🔴🔴 **เลขที่ได้ไม่ใช่ "คุณสมบัติของไคลเอนต์"** — มันคือ **หนึ่งบิลด์ หนึ่งฉาก (`bg0001`) หนึ่ง anchor หนึ่งเครื่อง หนึ่งบูตต่อขั้น** · **collection เดียว ไม่ใช่หลายเฟรมสะสม**
② 🔴 **"ส่งไป N ตัวโดยไม่มี `ErrorData`" ไม่เท่ากับ "ไคลเอนต์แสดง N ตัว"** — และ **"เห็นบนจอ M ตัว" ไม่เท่ากับ "ไคลเอนต์รับได้แค่ M"** · สองประโยคนี้อยู่คนละชั้นและ **ห้ามใช้แทนกันไม่ว่ากรณีใด**
③ **จำนวนหัวที่นับได้เป็น *ขอบล่าง* เสมอ** — ระยะมองเห็น สิ่งบัง มุมกล้อง LOD ทำให้เห็นน้อยกว่าที่มีได้ทั้งนั้น · **รอบนี้ไม่มีตัวคุมสำหรับสามอย่างนั้น** ⇒ **N3 เป็น "ตัวเลือก" ไม่ใช่ "ข้อสรุป"**
④ **ขั้น 115 ไม่ใช่ "จำนวนสูงสุดที่ไคลเอนต์รับได้"** — มันคือ **ขนาดของสำมะโน `bg0001`** · ผ่านครบ = **">= 115"** ไม่ใช่ "= เพดาน"
⑤ **`ErrorData=28317` ไม่ใช่ "รายงานจำนวน"** — รีโปนี้ถอดไว้แล้วว่ามันคือ `0x6E9D` = class id ของ envelope ที่ deserialize ไม่ผ่าน (`reports/PF_DELETE_SOFT002_NATURAL_0x36DB_DECODE_20260818.md` §(c)) ⇒ **เจอเลขนี้แปลว่า "เฟรมนี้ parse ไม่ผ่าน" เท่านั้น ห้ามเขียนว่า "ตัวเยอะไป" และห้ามเขียนว่า "สาเหตุเดียวกับ V43"**
⑤b **ขั้นที่พังไม่ได้ชี้สาเหตุ** — จำนวนสมาชิก / ขนาดเฟรม / avatar template ตัวใดตัวหนึ่งโหลดไม่ได้ / ตำแหน่ง — **สี่อย่างนี้เปลี่ยนพร้อมกันทุกครั้งที่ขึ้นขั้น** ⇒ ผลของใบนี้คือ **ช่วง** ไม่ใช่ **กลไก**
⑤c **ใบนี้ไม่ตอบเรื่องระยะมองเห็น การบดบัง LOD หรือ actor-slot displacement** — และ **ความบางของตารางแปลว่าชั้นตาแยกขั้นออกจากกันไม่ได้** ⇒ ห้ามใช้ภาพเป็นหลักฐานเรื่องเพดาน
⑥ **ใบนี้ไม่ให้ actor ตัวไหนมี ชื่อ / HP / ฝ่าย / ความเป็นศัตรู / AI / การเดิน / ลูท เกินกว่าที่ encoder V134 ให้อยู่แล้ว** — `P30` เก็บ HP ที่วัดไว้ (V117) และชื่อที่วัดไว้ (V119) · **อีก 114 ตัว HP 100 และไม่มีชื่อ เหมือนวันนี้เป๊ะ** · การตั้งชื่อ 114 แถวจากตารางที่ decode แล้วเป็น **ตัวแปรที่สองในเฟรมเดียวกัน** และเป็นใบสั่งสร้างของมันเอง
⑦ **ไม่ตอบอะไรเลยเรื่องประสิทธิภาพ/เฟรมเรต** เกินกว่าที่คนเห็นด้วยตาแล้วพูดออกมา — **ไม่มีเครื่องวัด fps ในรอบนี้**
⑧ **ไม่ตอบว่าอะไรตัดสินสีป้ายชื่อ** — นั่นคือ `RE-067` / `RE-068` · **จดสี ห้ามอนุมานสาเหตุ**
⑨ **ไม่ปิด `M1`** — `M1` ปิดด้วยตาเจ้าของตามกฎการวัดของ `CHARTER-01` เท่านั้น · ใบนี้ส่งมอบเลขและหลักฐาน ไม่ใช่ลายเซ็น
⑩ **ไม่รับรองว่าการต่อสายของ chief ถูกต้องโดยทั่วไป** — พิสูจน์แค่ว่า **บูตนั้นส่งไปเท่าไรและเกิดอะไรขึ้น**
⑪ **ไม่ตอบว่า collection *ที่สอง* หรือการรีเฟรชตอนเดินไกล จะให้ผลเหมือนกันไหม** — รอบนี้วัด **collection เดียวต่อบูต** (เฟรม reapply ที่ `+3.00` เป็นไบต์ชุดเดิม ไม่ใช่ชุดที่สอง)
⑫ **เลขไบต์เป็นของ anchor ที่จดไว้เท่านั้น** — ขั้น 20/60 ที่ anchor อื่นคือคนละชุดสมาชิกและคนละเลข · **ไม่มี XYZ = ไม่มีผล**
⑬ **`placement_index` ไม่ใช่ `0..114`** (pin ระบุ `last_index` ของขั้น 115 = `142`) ⇒ **จดตัวเลขที่เห็น ห้ามแปลงเป็น "ตัวที่เท่าไร"**
⑭ **ใบนี้ไม่อนุญาตให้ LANE-A แตะ `runtime.py` / `app.py`** — ไฟล์เหล่านั้นเป็นของ chief · **ถ้าระหว่างรอบมีใครคิดจะแก้เพื่อ "ให้มันรัน" นั่นคือการเปลี่ยนไบต์กลางรอบ ห้ามเด็ดขาด**
⑮ **`OBSERVER_CONFIRMED` เป็นขั้นตอน ไม่ใช่หลักฐาน** — บอกว่า "ผู้เทสยืนยันว่าสิ่งที่ผู้ช่วยเขียนตรงกับที่เธอเห็น" **ไม่ได้บอกว่าสิ่งนั้นเป็นความจริงเรื่องไคลเอนต์**
⑯ **เฟรม / mask / ตาราง placement / การวางตำแหน่ง ทั้งหมดเป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้วและกู้ไม่ได้ตลอดกาล

- **result:** (ผู้เทสกรอก — **แยกเป็นสี่ชุดตามขั้น ห้ามรวมกัน · ถ้ามีรอบยืนยันตาม STOP RULE ให้เป็นชุดที่ห้าแยกต่างหาก**: ① `BOOT_COMMIT` + ผลด่านก่อนบูตห้าข้อ (แปะสิ่งที่คอนโซลพิมพ์) + **บรรทัดจำนวน actor ที่คอนโซลพิมพ์** ② **label + `pc bytes` + `framed bytes` ของ SENT ทุกใบในบูตนั้น** เทียบตารางเลขคาดหมายทีละใบ ③ **XYZ ที่ decode ได้จาก `TargetPosVital` ใบแรก (f32)** + เวลา `T0` (+07:00) ④ **มี `ErrorData` ไหม เลขอะไร หลัง SENT ใบไหน กี่วินาทีหลัง `T0`** ⑤ บรรทัด traffic ถัดไปหลัง collection (ขาเข้า+ขาออก) + `TargetPosVital` ยังวิ่งตอนเดินไหม ⑥ **ตารางนับหัว: บูต x VP x มุม -> จำนวนที่เห็นได้อย่างน้อย** + X/Y บน HUD ของทุก VP + ระดับซูม ⑦ **คำตัดสินเมืองหนึ่งบรรทัดต่อบูต** ("ทั่วเมือง"/"บาง"/"ร้าง"/"ดูไม่ได้") ⑧ `Tornado Eagle`: ชื่อขึ้นไหม HP ขึ้นไหม เทียบกับบูตก่อน ⑨ อาการไคลเอนต์ + NO-CRASH/CRASH ⑩ **ตาราง PLAYBOOK ข้อ 13 ครบทุกป้ายทุกภาพ full-res ("ไม่มี" เขียนออกมา ห้ามเว้นว่าง)** ⑪ ค่าที่ต้องเติม `REAL_SERVER_DIVERGENCE.tsv` (**ส่งค่ามา ห้ามแก้ไฟล์เอง**) ⑫ census บรรทัด `[G>]` ทั้งไฟล์ ⑬ **แถวไหนของตารางผล (N1-N7)** + **ถ้าเป็น N2/N3: ช่วงเพดานที่วัดได้ เขียนเป็น `[N, ขั้นที่พัง)`** ⑭ path raw GAME log + console ทั้งไฟล์ + วิดีโอ + ภาพทุกไฟล์ พร้อม sha256 ⑮ เวลา +07:00 ทุกบูต · sha canonical ก่อน-หลัง · `integrity_check` · row-diff + `max(lease_generation)` ของ `run_gt076_*.sqlite3` · **teardown exit code ต่อบูต** ⑯ `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ⑰ `BUILD_IMPACT: <สร้างอะไรได้จากความรู้นี้ / หรือ "ไม่มี" พร้อมเหตุผล>` — 🔴 **บังคับตาม `CHARTER-01` BUILD-003 ก่อนถือว่าปิด**)

---

### 🆕 แก้ไข R173 (append-only) — **BLOCKER ของ PRECONDITION ถูกปลดแล้ว มีกลไกเลือกขั้นจริงแล้ว**
**เขียนโดย chief R173 · ไม่แตะเนื้อใบของสาย A แม้แต่ตัวอักษรเดียว · ทุกอย่างข้างบนเส้นนี้ยังใช้ได้ทั้งหมด**

**สถานะใบ:** `BLOCKED-ON-WIRING` **จบแล้ว** ⇒ ใบนี้อยู่ในสถานะ **`BLOCKED — รอ merge ก่อน`** (การต่อสายอยู่ในรอบ R173 ยังไม่เข้า `main`) · **เมื่อ PR ของรอบ R173 เข้า `main` ให้พลิกใบเป็น `PENDING` ได้ทันทีโดยไม่ต้องรออะไรอีก**

**กลไกที่ปลดบล็อก — ตอบสามข้อของ PRECONDITION ทีละข้อ:**
1. **วิธีเลือกจำนวน actor ต่อบูต:** `--world-census-actors <int 1..115>` ใน `src/pirateforce_foundation/app.py`
   - 🔴 **มันเป็นตัวเลือกขั้น ไม่ใช่สวิตช์เปิดฟีเจอร์** — สำมะโนเปิดอยู่แล้วบน **บูตไร้แฟล็ก** ด้วย `world_census_enabled = not active_lanes` (`src/pirateforce_foundation/runtime.py`) · **ไม่ใส่แฟล็ก = สำมะโนเต็ม**
   - **ค่านอกช่วง `1..115` ตายตั้งแต่ตอนสตาร์ต ไม่ใช่ตอนไคลเอนต์ก้าวแรก**
   - **`--export-events` ไม่ใช่เลนหัววัด** ⇒ ใส่ได้ตามใบเดิม และ **ไม่ทำให้สำมะโนปิด**
2. **คอนโซลพิมพ์จำนวนที่ส่งจริง:** **จำนวนอยู่ในตัวป้ายเอง** ⇒ อ่านจากคอนโซลได้โดยไม่ต้องมีบรรทัดพิเศษ
3. **server args เป็นสตริงจริง:** สี่บรรทัดข้างล่างนี้ **ใช้แทนบรรทัดที่ยังเขียนว่า `<ACTOR_COUNT_SELECTOR__CHIEF_FILLS_THIS_IN_AT_WIRING_TIME>`** (บรรทัดเดิมคงไว้ที่เดิมเพื่ออ่านย้อน · **เกณฑ์ "เห็นตัวอักษรนั้น = BLOCKED" ถือว่าตอบแล้วด้วยบล็อกนี้**)

**คำสั่งบูตทั้งสี่ขั้น — ลำดับบังคับ `3 -> 20 -> 60 -> 115` ตามใบเดิม · หนึ่งบูตหนึ่งขั้นหนึ่งสำเนา DB:**
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt076_r3.sqlite3   --export-events --world-census-actors 3
py -3 -u -m pirateforce_foundation.app --db state\run_gt076_r20.sqlite3  --export-events --world-census-actors 20
py -3 -u -m pirateforce_foundation.app --db state\run_gt076_r60.sqlite3  --export-events --world-census-actors 60
py -3 -u -m pirateforce_foundation.app --db state\run_gt076_r115.sqlite3 --export-events --world-census-actors 115
```
- 🔴 **ห้ามใส่แฟล็ก scenario/hypothesis ตัวอื่นแม้แต่ตัวเดียว** — เลนหัววัดตัวใดตัวหนึ่งที่เปิดอยู่ **ปิดสำมะโนทั้งก้อน** (`world_census_enabled = not active_lanes`) ⇒ บูตนั้นจะกลับไปเป็นสามตัวเดิมเงียบ ๆ
- **ห้ามรวมสองขั้นในบูตเดียว · ห้ามพ่วงใบอื่น · restart server ทุกครั้งระหว่างบูต** (ตามใบเดิม)

**บรรทัดที่พิสูจน์ว่ากำลังรันขั้นไหน — อ่านจากคอนโซล:**
```
[G>] WORLD_CENSUS_INITIAL_<RUNG> (<framed> bytes; late=<ms> ms)
[G>] WORLD_CENSUS_REAPPLY_<RUNG> (<framed> bytes; late=<ms> ms)     <- ราว +3.00 วินาทีถัดมา
```
- **เลขต่อท้ายป้าย = ขั้นของบูตนั้น** (`_3` / `_20` / `_60` / `_115`) — นี่คือสิ่งที่ทำให้ **สี่บูตที่หน้าตาเหมือนกันหมด แยกออกจากกันได้** ซึ่งคือกับดักหลักที่ใบนี้เขียนไว้เอง
- **เลขในวงเล็บ = framed bytes** ⇒ เทียบตารางเลขคาดหมายของใบ: **517 / 3161 / 9315 / 17942**
- **pc bytes** (**504 / 3148 / 9302 / 17928**) อ่านได้สองทาง: **hexdump ที่ v141 พิมพ์ต่อท้ายป้ายนั้น** หรือ **event `world_census_committed_actors_<n>_pc_<pc>_frame_<frame>`** ซึ่งบูตของใบนี้จะเห็น **เพราะใส่ `--export-events`**
- 🔴 **ป้ายโผล่ "หลังก้าวแรก" ไม่ใช่ "ตอนบูต"** — ตัวยิงคือ `TargetPosVital` ใบแรกหลัง runtime ack ตามบล็อก ANCHOR ของใบนี้เป๊ะ ⇒ **`steps` ข้อที่ให้อ่านบรรทัดนี้ ให้อ่าน "หลังแตะ `W` ครั้งเดียว" แทน "ตอนบูต"** · **เกณฑ์เดิมยังอยู่: ไม่มีบรรทัดนี้หลังก้าวแรก หรือเลขไม่ตรงขั้นที่ตั้งใจ = หยุด ปิด server บูตนั้นเป็น NO-RESULT**
- **ป้ายเก่า `V134_P0_P30_P91_ISOLATED_*` ต้องไม่ปรากฏเลยในทุกบูตของใบนี้** — เห็นแทน = **การต่อสายไม่ทำงาน หรือการประกอบถูกปฏิเสธแล้วถอยกลับของเดิมแบบ fail-closed** ⇒ **แถว `N4` CONTROL-BROKEN ⇒ หยุดทั้งใบ ส่ง chief ทันที ห้าม archive ใบ**
  - **หมายเหตุ:** ป้ายนั้น **ยังอยู่ใน `current/pf_login_game_server_v141.py` โดยดีไซน์** (แช่แข็ง + `v141Guard`) ⇒ **การ grep เจอมันในไฟล์ ไม่ใช่หลักฐานว่ายังไม่ต่อสาย** หลักฐานอยู่ที่ **คอนโซลของบูตจริง** เท่านั้น

**pass criteria ไม่เปลี่ยนแม้แต่ข้อเดียว — สองชั้นแยกกันเหมือนเดิม:**
- **ชั้น (1) wire/DB (headless ได้):** ข้อ "บรรทัดจำนวน actor ที่คอนโซลพิมพ์ ตัวอักษรเป๊ะ" **ตอบด้วยป้าย `WORLD_CENSUS_INITIAL_<RUNG>` ทั้งบรรทัด** · ข้ออื่นคงเดิมทุกตัวอักษร
- **ชั้น (2) client-observable (ต้องมีคนหน้าจอ):** **ไม่มีอะไรเปลี่ยน** · 🔴 **ป้ายบนคอนโซลไม่ใช่หลักฐานว่ามีอะไรขึ้นจอ และจำนวนหัวที่นับได้ไม่ใช่หลักฐานว่าส่งไปกี่ตัว**
- **nonclaim ที่บล็อกนี้เพิ่ม:** **แฟล็กนี้ไม่ได้ทำให้ "บูตของ `GT-076` เท่ากับบูตดีฟอลต์"** — บูตของใบนี้มี `--export-events` และมีตัวเลือกขั้น ⇒ **ใบนี้ยังไม่ปิด `M1` และยังไม่แทน `GT-078`** · ใบที่ตรวจรับเส้นทางไร้แฟล็กด้วยตาเจ้าของคือ **`GT-078`** และ **ใบนั้นห้ามใส่แฟล็กนี้เด็ดขาด**

---

## GT-078 M1-V1-ACCEPTANCE-PORT-ROYAL-POPULATION-115-001 [attended, in-game]: บูตเซิร์ฟเวอร์ **โดยไม่มีแฟล็ก scenario แม้แต่ตัวเดียว** แล้วเจ้าของเดินทั่ว Port Royal — **เมืองมีคนอยู่จริงหรือไม่ และของเดิมทั้งหมดยังเล่นได้อยู่ไหม** (ใบตรวจรับ `v1` ของ `M1`)  [🔴 **BLOCKED — รอ merge ก่อน · เหลือเงื่อนไขเดียว** · **ไม่ใช่ `BLOCKED-ON-WIRING` อีกต่อไป (แก้โดย chief R173)**: การต่อสาย `WORLD-CENSUS-001` เข้าเส้นทางดีฟอลต์ **เขียนเสร็จแล้วในรอบ R173** ที่ `src/pirateforce_foundation/runtime.py` (`world_census_enabled = not active_lanes`) + `src/pirateforce_foundation/app.py` **แต่ยังไม่เข้า `main`** ⇒ **ใบนี้รออย่างเดียวคือ PR ของรอบ R173 merge เข้า `main`** · `BUILD-001` (สาย A · PR #78 · `11166a1`) อยู่บน `main` แล้ว **และใบนี้ไม่ได้รอสาย A อีกต่อไป** · **ปลดบล็อกเองไม่ได้ ต้องเดินเช็คลิสต์ปลดบล็อก 5 ข้อในใบนี้ให้ครบก่อน (ข้อ 3 และ 4 ใช้ฉบับแก้ R173)** · attended · **ต้องเป็นเจ้าของนั่งหน้าจอเอง** · กำหนดของ `M1` = **2026-08-26 12:00 (+07:00)** · เปิดใบตาม `COO-CHARTER-01` ④ + `COO-CHARTER-02` ①④⑤ · เขียนใบโดย `pf-queue-author` · **เลขใบเคาะโดย chief R172**]

> 🔢 **เรื่องเลขใบ — ขยับสองครั้งในรอบเดียว เขียนที่มาไว้ให้ครบ:** ตัวนับเป็น **ชุดเดียวร่วมกับ `CLIENT_RE_QUEUE.md`** — prefix สองแบบ ตัวนับเดียว **ห้ามแยกตัวนับ**
> ① `pf-queue-author` เขียนหัวใบมาเป็น `GT-075` ตามคำสั่ง แล้ว **ทักท้วงเองว่าเลขชนกับ `RE-075`** (chief R170) ⇒ chief เคาะเป็น `GT-076`
> ② แล้ว **สาย A วาง `GT-076` ของตัวเอง (ACTOR-CEILING-STAIRCASE) และ `RE-077` แล้ว merge เข้า `main` ก่อนใบนี้** ⇒ **ใบนี้ขยับอีกครั้งเป็น `GT-078`**
> ⇒ **ชื่อไฟล์และ prefix ภาพในใบใช้ `gt078`/`GT078_` ทั้งหมด · เลขว่างถัดไป = `079`**
> 🔴 **ใบ `GT-076` ของสาย A อยู่ที่เดิมทั้งใบ ไม่ถูกแตะแม้แต่ตัวอักษรเดียว** — ตอน merge ผมเก็บของทั้งสองฝั่ง แล้วขยับเลขของ *ตัวเอง* ตามกฎ "ชนแล้วห้ามทับ"
> 🎯 **สองใบนี้ไม่ทับกันและควรอ่านคู่กัน:** `GT-076` วัด **เพดานที่ไคลเอนต์รับได้** (บันได 3→20→60→115) · **`GT-078` (ใบนี้) ตรวจรับ `v1` ด้วยตาเจ้าของบนเส้นทางไร้แฟล็ก**
> 🔴 **ใบเก่าทุกใบอยู่ที่เดิม ห้ามลบ ห้ามย้าย** — ใบที่ยังไม่ถูกเทส (`PENDING`/`READY`/`BLOCKED`/`RUNNING`) **ห้าม archive ไม่ว่าคิวจะยาวแค่ไหน**

### ที่มา — **อ่านจากเอกสาร ไม่ต้อง re-derive ระหว่างรอบ**

- `notes_to_chief\20260825_2215_COO-CHARTER-01-*.md` §③ + §④ `BUILD-001` · `notes_to_chief\20260825_2345_COO-CHARTER-02-*.md` §①④⑤
- `AGENTS.md` §6 (`G-OBS` · 🆕 `G-FRAME` · 🆕 `BUILD_IMPACT`)

**สิ่งที่วัดไว้แล้วและใบนี้ยืนอยู่บนมัน:**
- `current/pf_login_game_server_v141.py:4292` — **เส้นทางรันไทม์ปกติ ไม่ได้อยู่หลังแฟล็กใด ๆ** ส่ง `V134_P0_P30_P91_ISOLATED` = **3 actor จาก 115 placement ของ `bg0001`** · การจำกัดที่ 3 คือ **การแยกตัวแปรของการทดลองยุค V112→V129→V134 ที่กลายเป็นดีฟอลต์ถาวร** ไม่ใช่ข้อจำกัดของ encoder
- `BUILD-001` (สาย A · **PR #78**) ขยาย `make_v112_monster_shop_population_state()` จาก **3 → 115 placement** บน **เส้นทางดีฟอลต์เดิม** · encoder ตัวเดิม ตารางเดิม **เปลี่ยนแค่ชุดที่เลือก**
- คำสั่งเจ้าของ (`CHARTER-02` ④): **ยิง 115 ทีเดียว ยกเลิกขั้นบันได** · ที่มาเป็น **`[เจ้าของยืนยันจากประสบการณ์ตรง]` ไม่ใช่ `[วัดแล้ว]`** — จดตามกฎ `G8`
- 🔴 **กฎการวัดไมล์สโตน: นับว่าถึงก็ต่อเมื่อ *เจ้าของมองเห็นมันบนจอ* เท่านั้น** — เอกสาร เกตเขียว ledger หรือ log **ไม่นับ** ⇒ **ใบนี้เป็น attended โดยธรรมชาติ ไม่มีทางทำ headless ได้**

### objective (claim เดียว)

**คอมมิตที่บูตโดยไม่ส่ง `--*-scenario` แม้แต่ตัวเดียว ผ่านนิยาม "เวอร์ชัน" ครบทั้งสี่ข้อของ `CHARTER-02` ⑤ ⇒ มันคือเซิร์ฟเวอร์ `v1` และ `M1 เมืองมีชีวิต` ถึงแล้ว**

**ตัวหักล้าง (falsifier) — เขียนก่อนบูต มีสองหน้า:**
> 🔴 (ก) **บูตแบบไม่มีแฟล็กแล้วเมืองยังเหมือนเดิม (~3 ตัว)** ⇒ กฎข้อ 1 ไม่ผ่าน ⇒ **ยังไม่ใช่ `v1`**
> 🔴 (ข) **ของที่ `v0` เคยทำได้ ทำไม่ได้แม้ข้อเดียว** (ล็อกอิน/เลือกตัวละคร/เดิน/อยู่ครบ 10 นาที) ⇒ กฎข้อ 2 ไม่ผ่าน ⇒ **นั่นไม่ใช่เวอร์ชันใหม่ นั่นคือของเสีย** — **ล้มใบทันทีแม้เห็น NPC เต็มเมือง**

**ทำไมเป็น claim เดียว:** นิยาม "เวอร์ชัน" เป็น **เพรดิเคตเดียวที่มีสี่เงื่อนไข AND กัน** · บูตครั้งเดียวตอบทั้งก้อน · เงื่อนไขใดตก = ตกทั้งเพรดิเคต
🔴 **ของที่ *ไม่ใช่* claim ของใบนี้:** **"ไคลเอนต์รับ actor พร้อมกันได้กี่ตัว"** — ใบนี้ **วัดแล้วบันทึกไว้เฉย ๆ** · **ห้ามตั้งค่าที่วัดได้เป็น "เพดานของไคลเอนต์"** เพราะรอบนี้ไม่มีตัวคุมเรื่องระยะ/มุมกล้อง/culling เลย ⇒ ต้องเปิดใบของตัวเอง

### 🎁 การวัดฟรีของรอบนี้ — **ตัวเลขที่โปรเจกต์นี้ไม่เคยมี**

🔴 **สามเลขแยกกันเด็ดขาด ห้ามยุบรวม ห้ามใช้เลขหนึ่งแทนอีกเลข:**
1. **`composed`** = จำนวนที่เซิร์ฟเวอร์ **ประกอบได้** ก่อนส่ง (log พิมพ์เอง ตาม `CHARTER-02` ④) — ชั้น (1)
2. **`sent`** = จำนวน actor ที่ **ออกสายจริง** อ่านจาก `GAME_LIVE.txt` — ชั้น (1)
3. **`seen`** = จำนวนที่ **คนนับได้จากจอ** — ชั้น (2) เท่านั้น
- **เห็นน้อยกว่า 115 = *ผล* ไม่ใช่ *ความล้มเหลว*** และไม่ทำให้ใบเป็น FAIL โดยตัวมันเอง
- 🔴 **ห้ามเปลี่ยนตัวเลข 115 เป็นค่าอื่นเงียบ ๆ** ส่งไม่ครบให้รายงานเลขจริงและเหตุผลที่โค้ดพิมพ์ออกมาเอง

### 🔒 เช็คลิสต์ปลดบล็อก — **ครบ 5 ข้อเท่านั้นถึงบูตได้ · ไม่ครบ = `BLOCKED` ต่อ ห้ามบูต ห้ามหาคอมมิตเอง**

1. **การต่อสายอยู่บน `main` แล้วจริง — 🆕 ฉบับแก้ R173** · `BUILD-001` (PR #78 · `11166a1`) อยู่บน `main` แล้ว **แต่โมดูลที่มันสร้างไม่มีใครเรียกจนถึงรอบ R173** ⇒ **ของที่ต้องเห็นบน `main` คือการต่อสายของ R173 ไม่ใช่ PR #78** ⇒ **ตัวปลดบล็อกใบนี้คือข้อ 3 ข้างล่าง ไม่ใช่การเห็นว่า PR ไหน merge แล้ว**
2. `py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch` คืน **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` · **exit 3 ⇒ ห้ามบูต** · exit 2 = พาธผิด/git ล้ม
3. **ยืนยันการต่อสายกับ `<SHA>` ที่จะบูตจริง — 🆕 ฉบับแก้ R173** (single quote เท่านั้น · 🔴 **ห้าม `| grep` / `awk`** · แปะสิ่งที่คอนโซลพิมพ์ทุกข้อ **รวมถึงข้อที่ได้ 0 บรรทัด**)

   🔴 **ทำไมข้อเดิมถูกแทนที่ (เก็บไว้ให้อ่านย้อน ห้ามลบบรรทัดนี้):** ฉบับ R172 grep เฉพาะ `current/pf_login_game_server_v141.py` แล้วสั่งว่า *"ถ้าเส้นทางดีฟอลต์ยังเรียก `V134_P0_P30_P91_ISOLATED` ⇒ ยังบล็อก"* — เกณฑ์นั้น **ตัดสินคำถามไม่ได้ และจะบล็อกใบนี้ตลอดกาล** เพราะ `v141` **แช่แข็งและมี `v141Guard`** ⇒ สาขาสามตัว **ต้อง** อยู่ในไฟล์นั้นโดยดีไซน์ · ตัวที่กดสาขานั้นให้เงียบอยู่คนละไฟล์ คือ `src/pirateforce_foundation/runtime.py` (ตั้ง `npc_spawn_sent` ก่อนเรียก `super().dispatch`)
```
git grep -n 'world_census_enabled = not active_lanes' <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n 'build_world_population' <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n 'WORLD_CENSUS_INITIAL_' <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n 'world-census' <SHA> -- src/pirateforce_foundation/app.py
git grep -n 'V134_P0_P30_P91_ISOLATED' <SHA> -- current/pf_login_game_server_v141.py
```
   **อ่านผลทีละบรรทัด — เขียนไว้ให้ตัดสินได้โดยไม่ต้องคิดเอง:**
   - **บรรทัดที่ 1 — "สำมะโนเปิดโดยไม่ต้องมีแฟล็ก":** **GO** = ได้ **อย่างน้อย 1 บรรทัด** ใน `runtime.py` · **STILL BLOCKED** = **0 บรรทัด** หรือเจอเป็นรูปอื่นที่ผูกกับแฟล็ก ⇒ สำมะโน **ไม่ได้เปิดเองบนบูตไร้แฟล็ก** ซึ่งขัดกฎข้อ 1 ของใบนี้ **จดแล้วรายงาน ห้ามบูตแล้วค่อยดู**
   - **บรรทัดที่ 2 — "มีคนเรียกจริง ไม่ใช่แค่มีโมดูล":** **GO** = ได้ **อย่างน้อย 1 บรรทัด** · **STILL BLOCKED** = **0 บรรทัด** ⇒ นี่คือกรณี **"สำมะโนมีอยู่แต่ไม่มีอะไรเรียกมัน"** ซึ่งเป็นสภาพเดิมก่อน R173 เป๊ะ ๆ **และเป็นสิ่งเดียวที่ข้อ 3 ฉบับเก่ามองไม่เห็น**
   - **บรรทัดที่ 3 — "จำนวนอยู่ในป้าย ⇒ อ่านจากคอนโซลได้":** **GO** = ได้ **อย่างน้อย 1 บรรทัด** · **STILL BLOCKED** = **0 บรรทัด** ⇒ **ข้อ 4 จะไม่มีที่ให้อ่าน** และสี่บูตจะแยกกันไม่ออก
   - **บรรทัดที่ 4 — "แฟล็กที่มีต้องเป็นตัวเลือกขั้น ไม่ใช่สวิตช์เปิดฟีเจอร์":** **GO** = ได้ **หนึ่งบรรทัดเดียว** และเป็น `--world-census-actors` (`type=int, default=None`) · **STILL BLOCKED สำหรับใบนี้** = เจอชื่ออื่นที่เป็นสวิตช์ (`--world-census` · `--enable-world-census` · `--world-census-scenario`) ⇒ เส้นทางไร้แฟล็กจะ **ไม่มี** สำมะโน **จดแล้วส่ง chief ทันที ห้ามเดาว่าต้องใส่แฟล็กเอง**
   - **บรรทัดที่ 5 — ตัวคุมของไฟล์แช่แข็ง (🔴 ความหมายกลับด้านจากฉบับ R172):** **GO** = **ยังเจอสี่บรรทัด** ⇒ **นี่คือสิ่งที่ถูกต้อง** ไฟล์แช่แข็งไม่ถูกแตะ · **หยุดและรายงาน** = **0 บรรทัด** หรือจำนวนเปลี่ยน ⇒ มีคนแก้ไฟล์ที่มี `v141Guard` **นั่นจะแดงที่เกต ไม่ใช่ที่ใบนี้ แต่ห้ามบูตไปก่อน**
   - **สรุปกติกาเดียว:** **GO ต่อเมื่อบรรทัด 1-4 ผ่านครบทั้งสี่ และบรรทัด 5 ยังเจอสี่บรรทัดตามเดิม** · **ขาดข้อใดข้อหนึ่ง = `BLOCKED` ต่อ ห้ามบูต**
   - 🔴 **ไม่มี grep ข้อไหนพิสูจน์ว่าบูตจริงส่งอะไรออกสาย** — grep ตัดสินแค่ว่า *ควรบูตได้หรือยัง* · สิ่งที่บูตทำจริงอ่านจากข้อ 4 และจากชั้น (1) เท่านั้น
4. **มีที่ให้อ่านจำนวน actor ที่ประกอบได้ — 🆕 ฉบับแก้ R173: อ่านจาก "บรรทัดตอนส่ง" ไม่ใช่ "บรรทัดตอนบูต"**
   - 🔴 **กับดักที่ต้องอ่านก่อนตกใจ:** บล็อกสำมะโนถูกยิงโดย **`TargetPosVital` ใบแรกหลัง runtime ack** ⇒ **ตอนเซิร์ฟเวอร์ขึ้นและตอนเข้าแมพ คอนโซลจะเงียบสนิทเรื่องสำมะโน** และจะพิมพ์ก็ต่อเมื่อเจ้าของ **ขยับตัวครั้งแรก** ⇒ **"ยังไม่เห็นบรรทัดตอนบูต" ไม่ใช่หลักฐานว่าไม่ได้ต่อสาย ห้ามล้มบูตด้วยเหตุนี้**
   - **บรรทัดที่ต้องอ่านและคัดมาทั้งบรรทัด** (v141 พิมพ์ทุก action ตอน **ส่ง** ที่ `current/pf_login_game_server_v141.py:7762`):
```
[G>] WORLD_CENSUS_INITIAL_115 (17942 bytes; late=0.0 ms)
[G>] WORLD_CENSUS_REAPPLY_115 (17942 bytes; late=<ms> ms)
```
     ใบ `REAPPLY` มาหลังใบแรกประมาณ **3.00 วินาที** · **จดทั้งสองใบ ห้ามจดใบเดียว**
   - **สามเลขของใบนี้แมปกับอะไร — กฎเดิมยังอยู่ครบ: 🔴 ห้ามยุบรวม ห้ามใช้เลขหนึ่งแทนอีกเลข**
     - **`composed`** = **ตัวเลขที่ต่อท้ายป้าย** (`..._INITIAL_115` ⇒ `composed = 115`) · **ไม่มีป้าย `WORLD_CENSUS_*` เลยหลังก้าวแรก ⇒ เขียน `composed = unmeasured` หรือ `composed = 3` ตามป้ายที่เห็นจริง ห้ามเดาจากจอ**
     - **`sent`** = อ่านจาก `GAME_LIVE.txt` · **ตัวเลขในวงเล็บของคอนโซล = framed bytes** (คาด **17942**) · **pc bytes** (คาด **17928**) อ่านได้จาก **hexdump ที่ v141 พิมพ์ต่อท้ายป้ายนั้น** เท่านั้น — **อ่านไม่ออกให้เขียน `pc = unmeasured`**
     - **`seen`** = ชั้น (2) เท่านั้น **ไม่มีบรรทัดคอนโซลใดตอบข้อนี้ได้**
     - 🔴 **`composed = 115` เป็นเลขของ "ประกอบได้" ห้ามเขียนว่า "ไคลเอนต์รับ 115" และห้ามเขียนว่า "มี 115 ตัวบนจอ"**
   - **event `world_census_committed_actors_115_pc_17928_frame_17942` มีจริง แต่ใบนี้จะไม่เห็น** เพราะมันโผล่เฉพาะเมื่อมี `--export-events` ซึ่ง **ใบนี้ห้ามใส่** ⇒ **อย่ารอมัน อย่าเติมแฟล็กเพื่อจะได้เห็นมัน**
   - **เลขต่อท้ายป้ายไม่ใช่ `115`:** **ห้ามแก้ ห้ามบูตใหม่เพื่อให้ได้ 115** — **จดเลขจริงแล้วรายงาน** (ความเป็นไปได้ที่รู้อยู่แล้ว: มีคนตั้ง `MEASURED_CLIENT_ACTOR_CEILING` ใน `src/pirateforce_foundation/world_population.py` หรือมีแฟล็กหลุดเข้ามาในบูต)
   - **เห็น `V134_P0_P30_P91_ISOLATED_INITIAL_READY` แทน `WORLD_CENSUS_INITIAL_*`:** ⇒ **การต่อสายไม่ทำงานในบูตนั้น หรือการประกอบถูกปฏิเสธแล้วถอยกลับของเดิมแบบเงียบ (fail-closed)** ⇒ **`composed = 3`** ⇒ **เดินใบต่อจนจบตามขั้นตอน** แล้วรายงานเป็น **แถว `V3` + `composed = 3`**
5. **ผู้ที่นั่งหน้าจอคือเจ้าของ (คุณ Panya) เอง** — 🔴 คนอื่นนั่งแทน = **เก็บชั้น (1) ได้ครบ แต่ปิด `M1` ไม่ได้** (แถว `V6 OWNER-ABSENT`)

🔴 **"เครื่องมือชนะใบเสมอ"** — เครื่องมือบอกว่าบูตไม่ได้ ให้เชื่อเครื่องมือ แล้วจดความขัดแย้งลงผล

### 🟢 งบเวอร์ชัน — **ศูนย์สล็อต ไม่เกี่ยวกับ ledger**
- ใบนี้ **ไม่แก้โค้ด ไม่แก้ scenario ไม่แก้ไบต์** — ตรวจรับของที่สาย A ส่งมา
- `BUILD-001` เป็น **เลนบนเส้นทางดีฟอลต์ ไม่ใช่หัววัด** ⇒ **ไม่กินสล็อต** · 🔴 **ผู้เทสห้ามแก้ ledger ไม่ว่าผลออกแถวไหน**
- 🔴 **ใครคิดจะใส่แฟล็กเพิ่ม "เพื่อให้เห็นเยอะขึ้น" = ทำลาย claim ของใบทั้งใบ** (กฎข้อ 1 คือ "ไม่มีแฟล็ก") **ห้ามเด็ดขาด**

### ⏱️ งบเวลาผู้เทส — **~20 นาทีบนจอ** (ไม่รวมบูต/teardown)
เข้าเกม → เดินทัวร์ 6 จุด → ยืนให้ครบ **10 นาทีเต็มเป็นอย่างน้อย** → ถ่ายภาพสีป้าย → ออก
🔴 **10 นาทีเป็นเกณฑ์ผ่านของกฎข้อ 3 ไม่ใช่การถ่วงเวลา** — ทัวร์จบก่อนก็ยืนต่อจนครบ แล้วจดเวลาเข้า/ออกเป็นตัวเลข

### db (สำเนาเสมอ — **canonical ไม่ถูกเปิดตลอดรอบ**)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-078_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt078.sqlite3
```
- เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง**
- 🔴 **สำเนาใหม่ทุกบูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกครั้ง** — ทัวร์เริ่มที่จุดเกิดเสมอโดยดีไซน์ (`X -8553.947265625 · Y -2579.68896484375 · Z 186.0`)
- 🔴 **ใบนี้ *ไม่ใช่* play mode** — โลกที่เจ้าของเล่นข้ามวันคือ `state\play.sqlite3` (คนละไฟล์) ⇒ **ใบนี้ไม่ตัดสินอะไรเลยเรื่องของที่ค้างข้ามวัน** · 🔴 **ห้ามกด `PLAY_PIRATE_FORCE.bat` ระหว่างรอบ** (มันถือ `LOCK_GAME` ด้วย `BY: PLAY MODE`)
- session 2: สำเนาใหม่ `state\run_gt078b.sqlite3` (**ห้ามใช้ไฟล์เดิมซ้ำ**)

### server args — 🔴🔴 **"ไม่มีแฟล็ก" คือสิ่งที่ถูกทดสอบ ไม่ใช่รายละเอียดการตั้งค่า**
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt078.sqlite3
```
- client: `-SecondPasswordMode bypass` (ท่ามาตรฐาน)
- 🔴 **ห้ามมี `--*-scenario` แม้แต่ตัวเดียว · ห้ามมี `--export-events` · ห้ามพ่วงใบอื่นเข้าบูตนี้**
- **หลักฐานว่าไม่มีแฟล็กจริง — เก็บทันทีหลังเซิร์ฟเวอร์ขึ้น วาง *ทั้งบรรทัด* ลงผล:**
```
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List
```
- 🆕 **console ของบูตนี้ — ฉบับแก้ R173 (ความหมายกลับด้านจากฉบับเดิม อ่านให้จบก่อนตัดสิน):**
  - **สิ่งที่ต้องเห็นหลังก้าวแรก:** `[G>] WORLD_CENSUS_INITIAL_<n>` และอีกราว 3.00 วินาทีถัดมา `[G>] WORLD_CENSUS_REAPPLY_<n>`
  - **สิ่งที่ต้องไม่เห็นทั้งบูต:** `V134_P0_P30_P91_ISOLATED_INITIAL_READY` และ `V134_P0_P30_P91_ISOLATED_REAPPLY_READY`
  - 🔴 **ความหมายเมื่อเห็น `V134_*_ISOLATED` — เปลี่ยนแล้ว: ไม่ใช่ "บูตผิดเลน" อีกต่อไป** · `v141` ยังมีสาขาสามตัวอยู่ในไฟล์โดยตั้งใจ (แช่แข็ง + `v141Guard`) และการต่อสายทำงานโดย **กดสาขานั้นให้เงียบ** ⇒ **เห็นป้ายนี้บนบูตไร้แฟล็ก = การต่อสายไม่ได้ทำงานในบูตนั้น** ⇒ **ไม่ใช่ NO-RESULT · ไม่ต้องหยุดรอบ** ⇒ **เดินใบต่อให้ครบ แล้วรายงานเป็นแถว `V3` พร้อม `composed = 3`**
  - **ไม่เห็นทั้งสองอย่างเลยหลังก้าวแรก:** เขียน `composed = unmeasured` + คัด `[G>]` ทุกบรรทัดของบูตนั้นมาทั้งชุด **ห้ามสรุปว่าไม่ได้ต่อสาย และห้ามสรุปว่าต่อสายแล้ว**
  - **ของเดิมที่ยังอยู่ครบและยังเป็นเกณฑ์หยุด:** เห็น label ของ **เลนหัววัด** (`HYP_*` · `ARENA_*` · `SCENE_*` · label ของ population/scenario lane ใด ๆ) แม้บรรทัดเดียว ⇒ **บูตผิด หยุด ปิด server ห้ามอ่านจอเป็นผล**
- 🔴 **ห้ามใส่ `--world-census-actors` ในใบนี้เด็ดขาด** — มันไม่ใช่สวิตช์เปิดสำมะโน (**ไม่ใส่ = สำมะโนเต็ม**) แต่การใส่มันทำให้ประโยค **"บูตนี้ไม่มีแฟล็กแม้แต่ตัวเดียว"** ของกฎข้อ 1 เป็นเท็จ ⇒ **claim ของใบพังทั้งใบ ⇒ แถว `V7` NON-OBSERVED** · **ใบที่ใช้แฟล็กนี้คือ `GT-076` ACTOR-CEILING-STAIRCASE**

### 🔴 คีย์บอร์ด เมาส์ และสิ่งที่ยิงไบต์

| ท่า | ทำอะไรจริง | ยิง `TargetPosVital` ไหม | ใบนี้ใช้ได้ไหม |
|---|---|---|---|
| **คลิกขวาค้างลากเมาส์** | หมุน **มุมกล้อง** อย่างเดียว · ทิศหันตัวละครไม่ขยับ | 🟢 ไม่ยิง | ✅ ใช้ได้ทุกจังหวะ · **เป็นตัวเช็ค NO-CRASH ตัวเดียวที่ใบนี้ยอมรับ** |
| **`W/A/S/D`** | เดิน (เปลี่ยนทั้งตำแหน่งและทิศหัน) | 🔴 ยิง | ✅ **ต้องเดิน — การเดินคือเนื้อของใบ** จดเวลาเริ่ม/หยุดแต่ละช่วง |
| **`Q` / `E`** | **หันตัวละคร** กล้องแพนตาม | 🔴 ยิง | ✅ ใช้ได้ · 🔴 **ห้ามใช้เป็นตัวเช็ค NO-CRASH** |
| **ล้อเมาส์ (ซูม)** | ซูมกล้อง | **[UNKNOWN — ไม่มีใครเคยวัด]** | ✅ ใช้ได้ · **จดเวลาที่ซูมทุกครั้ง** |
| **พิมพ์ตัวอักษร** | — | — | ❌ 🔴 **ห้ามพิมพ์อะไรทั้งรอบ** (ตัวอักษรตอนช่องแชตไม่โฟกัส = ฮอตคีย์ ไม่มีใครรู้ว่าตัวไหนทำอะไร) |

🔴 **ประโยคเดียวที่ต้องจำ: ตัวที่ยิง `TargetPosVital` คือ "การเปลี่ยนทิศหันของตัวละคร" ไม่ใช่ "การขยับกล้อง"**

### ⏱️ ไทม์ไลน์ — **`T0` = เฟรมแรกที่เข้าแมพสำเร็จ** (เห็น HP bar + minimap + ชื่อแมพครบ 🔴 ไม่ใช่เฟรมที่ loading จบ · ±2 วิ · หลุดจังหวะให้จดเวลาจริง **ห้ามแต่งผล วิดีโอคือกรรมการ**)

| หน้าต่าง | เวลา | ผู้เทสทำอะไร |
|---|---|---|
| **PRE** | ก่อน `T0` | ล็อกอิน → เลือกตัวละคร → เข้าแมพ · **จับเวลาทุกขั้น** |
| **S0** | `T0` → `+60` | **ยืนนิ่งที่จุดเกิด** · คลิกขวาลากกวาดกล้อง 4 ทิศ **ค้างทิศละ 4 วิ** · **นับหัวที่เห็น** |
| **TOUR** | `+60` → `+540` | เดินทัวร์ **S1 → S5** · ทุกจุดทำเหมือน `S0` |
| **HOLD** | `+540` → **`+600` เป็นอย่างน้อย** | ยืนจนครบ 10 นาทีจาก `T0` · เฝ้าดูว่าหลุด/ค้างไหม |
| **POST** | หลัง `+600` | ภาพนิ่ง full-res ใบสุดท้าย → เช็ค NO-CRASH → ออก |

### steps (คลิกต่อคลิก)

**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด **boot stamp (+07:00)** · preflight จอว่าง (`staged\TEMPLATE_preflight_unattended.ps1` — เจอหน้าต่าง elevated = ABORT ทั้งรอบ) · เทียบ sha canonical · copy DB สองใบ
**เตรียม teardown:** ก๊อปจาก **`TEMPLATE_teardown_generic.ps1`** เป็นหลัก · ก๊อปจากจ็อบที่เป็นตัวเลข **ต้องเปิดดูบรรทัดที่ 17 ให้เห็น `-replace '\\','/'` ก่อนเสมอ** · 🔴 **ห้ามก๊อปจาก `1103`/`1105`**

1. **สตาร์ตเซิร์ฟเวอร์ก่อน แล้วค่อยบูต client เสมอ** (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client)
   - 🔴 client ที่บูตโดยไม่มีเซิร์ฟเวอร์ **ตายเองใน ~3.5 นาที** · 🔴 ฆ่า client กลางคัน **ต้อง restart server ก่อนเปิดตัวใหม่เสมอ**
   - **เก็บ `CommandLine` ของโปรเซสเซิร์ฟเวอร์ทันที** · จัดหน้าต่าง console ให้เห็นข้างจอโดยไม่บังพื้นที่วัด · **ตลอดรอบห้ามคลิก console**
2. เปิด client → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร → **เลือกช่องแรก** → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (🔴 **ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด**) · **จดเวลาทุกขั้น** (นี่คือกฎข้อ 2 ครึ่งหนึ่ง ไม่ใช่พิธีกรรม)
3. **อัดวิดีโอต่อเนื่องตั้งแต่ก่อนกดเข้าเกมจนจบ session** (`staged\TEMPLATE_video_recorder.ps1 -FrameRate 30` ลง `evidence_video\`) · จด `VIDEO START pid= start= fps= path=` (🔴 `start=` **ห้ามใช้เป็นสมอเวลา**) · 🔴 **ไม่ได้อัด = NO-RESULT ทันที**
4. **`T0`** — เห็น HP/minimap/ชื่อแมพ/chat online ครบ ⇒ **พูดออกเสียงว่า "T0"** จดเวลานาฬิกาจริง (+07:00) และ `t` ของวิดีโอ
5. **`S0` (จุดเกิด):** ยืนนิ่ง · **คลิกขวาค้างลากกวาดกล้อง 4 ทิศ ทิศละ 4 วินาที** (นับออกเสียง) · **จด HUD `X/Y`** · **นับ NPC ที่เห็น พูดเลขออกเสียง**
   - 🔴 **นับหัวที่ *เห็น* เท่านั้น ห้ามนับจากป้ายที่เดาเอา ห้ามนับซ้ำ** — วิธีนับที่ใช้จริงต้องเขียนลงผล
6. **`S1` → `S5` — เดินทัวร์ ทำเหมือนข้อ 5 ทุกจุด:**
   - **`S1`** = ฝั่ง `Navy Transfer` (`P0` X `-9139.957` Y `-2780.045`) · **`S2`** = ฝั่ง `Sebastian` (`P1` X `-8013.5` Y `-2780.0`)
   - **`S3`/`S4`/`S5`** = **สามทิศที่ยังไม่มีใครเดินไปเลย** — 🔴 **ไม่มีพิกัดพินไว้เพราะไม่มีใครวัด** ⇒ **จด HUD `X/Y` ของทุกจุดที่ยืนจริง นั่นคือพิกัดของรอบนี้**
   - 🔴 **ห้ามเดินลงน้ำ** — `Z = 0.00` เหนือผืนน้ำยังเป็นคำถามเปิด (`RE-073`) และรอบนี้ไม่มีตัวคุมเรื่องนั้น
   - ⛔ **เกณฑ์หยุดทั้งรอบ:** เห็นชื่อ probe (`ProbePlayer01` · `ProbeControl03`) ที่ไหนก็ตาม ⇒ **บูตไม่สะอาด หยุด เก็บ console ทั้งไฟล์ รายงานทันที**
7. **ภาพนิ่ง full-res ด้วยเครื่องมือนอกเกม อย่างน้อย 3 ใบ** ที่จุดที่มี NPC ในเฟรมมากที่สุด → `evidence_screens\GT078_S<n>_FULLRES_<yyyyMMdd_HHmmss>.png`
   - 🔴 มีไว้สองอย่าง: **(i) อ่าน *สี* ป้ายชื่อ (ii) นับหัวแบบตรวจซ้ำได้** · 🔴 **ห้ามกดคีย์ใด ๆ ในหน้าต่างเกมเพื่อถ่ายภาพ**
8. **`HOLD`:** ยืนจนครบ **10 นาทีจาก `T0` เป็นอย่างน้อย** — **จดเวลานาฬิกาจริงตอนครบ** · เฝ้าดู: หลุดไหม ค้างไหม chat ยังตอบไหม
9. **NO-CRASH / CRASH:** **คลิกขวาค้างลากแล้วกล้องหมุน = NO-CRASH** · หลุด/ค้าง = CRASH + จดว่าเกิดที่ `t` เท่าไร · 🔴 **ห้ามใช้ `Q`/`E` เป็นตัวเช็ค**
10. ออก: **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย → **หยุดวิดีโอ** → **ปิดเซิร์ฟเวอร์ด้วย**
11. เก็บ **raw GAME log ทั้งไฟล์** + console out/err ทั้งหมด (ทุกบรรทัด `[G>]` / `ErrorData`) → `PRAGMA integrity_check;` บนสำเนาทุกใบ → sha256 ทุกไฟล์
12. **teardown เสมอ — แม้รอบจบเพราะเลิกเล่น ไม่ใช่เพราะเทสจบ** → เทียบ sha canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม
13. **หลังรอบ — แตกเฟรม (ห้ามข้าม · 🔴 ห้ามมี `scale=` ในบรรทัดคำสั่งเด็ดขาด):**
```
$mkv = '<path full of the FULLROUND .mkv>'
ffmpeg -ss <T0 - 5.00> -i $mkv -t 80.00 -vsync 0 GT078_S0_%03d.png
ffmpeg -ss <t ของ S1> -i $mkv -t 30.00 -vsync 0 GT078_S1_%03d.png
```
14. 🔴🔴 **`G-FRAME` — บังคับกับ *ทุกเฟรมที่ถูกยกมาอ้าง* ไม่ว่าจะอ้างเพื่อบอกว่าเห็นหรือไม่เห็น:**
```
FRAME: <ชื่อไฟล์>  t=+<วินาที> จาก T0=<YYYY-MM-DDTHH:MM:SS+07:00>  dist=<หน่วยเกม> ถึง <สิ่งที่พูดถึง>
```
    - **`t` ต้องเป็นตัวเลขจริง ห้าม `~` ห้าม `x`** · **`dist` วัดจากตัวละคร ณ เฟรมนั้น** วัดไม่ได้เขียน **`dist=unmeasured`** 🔴 **ห้ามเว้นว่าง ห้ามเขียนว่า "ใกล้"**
    - 🆕 **บังคับเพิ่มโดย chief R172 (หลัง `pf-adversary` ชี้ว่ากฎร่างแรกปล่อยเหตุการณ์ที่มันเกิดมาเพื่อกัน ผ่านได้):**
      บรรทัด **`UNMEASURED_DIST: <n>/<ทั้งหมด>`** ในจดหมายผล · **เกินครึ่ง = cc ไม่บริโภคเป็นผลปิดใบ**
    - ที่มาของกฎ: ตัวคุมของ `GT-072` วัดที่ `T0 + 92.8` วิ = หลังทุกอย่างหายไปแล้ว · ประโยค "ยืนทับพอดี" จริง ๆ ห่าง **243 หน่วย**
15. 🔴🔴 **`G-OBS` — ขั้นสุดท้าย บังคับ:** ผู้ช่วยทวนรายการ "สิ่งที่ผู้ช่วยเห็น" ให้ผู้เทสยืนยันทีละข้อ (จำนวนต่อจุด · เดินไปจุดไหน · หลุดหรือไม่ · **สีป้ายทุกป้าย**) · ผู้เทสตอบคำเดียวต่อข้อ: **"ตรง" / "ไม่ตรง" / "ฉันไม่ได้ดูข้อนั้น"**
    - จดหมายผลต้องมีบรรทัดนี้เป๊ะ: `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` (🔴 นาทีจริง ห้าม `x` ห้าม `~`)
    - 🔴 **ยังไม่ยืนยัน = ห้ามเขียนผลลงคิว** · 🔴 **บรรทัดนี้เป็น "ขั้นตอน" ไม่ใช่ "หลักฐาน"**

### คำทำนาย (**คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว** · ท่องก่อนบูต)
- **P1 [ชั้น wire]** log พิมพ์ `composed = 115` และ `sent = 115`
- **P2 [ข้อหลักของใบ]** เจ้าของเห็น NPC **มากกว่า 3 ตัวอย่างชัดเจน หลายจุด หลายทิศ**
- **P3 [ค่าที่ไม่มีใครรู้จริง ๆ]** `seen` **น้อยกว่า** `sent` ⇒ **คำทำนายที่ผมคาดว่าจะ "ผิดแบบมีประโยชน์" ที่สุด**
- **P4 [กฎข้อ 2]** ล็อกอิน / เลือกตัวละคร / เดิน / 10 นาที **ผ่านครบ ไม่มี regression**
- **P5 [จดสีอย่างเดียว ห้ามสรุปสาเหตุ]** ป้ายชื่อ NPC เป็น **เหลือง**
- **P6 [ถ้าผิดคือเรื่องใหญ่ที่สุดของรอบ]** ไม่ crash / ไม่ lag จนเล่นไม่ได้ตอนส่ง 115 ตัวทีเดียว — **ถ้าค้างหรือหลุดตอนเข้าแมพ นั่นคือเพดานที่วัดได้ ไม่ใช่ความล้มเหลว รายงานเสียงดัง**

### pass criteria — **สองชั้น แยกกันเด็ดขาด 🔴 ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

**ชั้น (1) wire/DB — ทำ headless ได้ ไม่ต้องมีคนหน้าจอ**
1. **`BOOT_COMMIT`** + ผลเช็คลิสต์ปลดบล็อกข้อ 3 ทั้งสี่บรรทัด (แปะสิ่งที่คอนโซลพิมพ์)
2. 🎯 **หลักฐานกฎข้อ 1:** `CommandLine` ของโปรเซสเซิร์ฟเวอร์ **ทั้งบรรทัด** · **ต้องไม่มีสตริง `-scenario` เลย** · console ไม่มี label เลนหัววัดแม้แต่บรรทัดเดียว
3. **`composed`** = เลขที่ log พิมพ์ก่อนส่ง · วัดไม่ได้เขียน **`composed = unmeasured`**
4. **`sent`** = นับจาก `GAME_LIVE.txt` · **census: นับ *ทุก* บรรทัด `[G>]` ทั้งไฟล์แล้วรายงานยอดรวม ไม่กรองอะไรออก**
5. **session ต่อเนื่อง ≥ 10 นาที:** ไม่มี reconnect · ไม่มี GAME connection ที่สอง · เวลาเข้า-ออกเป็นตัวเลข
6. ไม่มี traceback · stderr 0 B · **ไม่มี `ErrorData=28317`** (มี = จดว่าโผล่หลังอะไร เก็บคอนโซลทั้งไฟล์)
7. DB สำเนา: `PRAGMA integrity_check` = `ok` · row-diff ต่างเฉพาะ `sessions` **+1 ต่อการเข้าเกมหนึ่งครั้ง** (`count(*) WHERE selected_character_id IS NOT NULL`) · `max(lease_generation)` **ไม่ถอยหลัง** · **sha256 canonical ก่อน-หลัง = `CANON_SHA.txt`** · **canonical ไม่ถูกเปิดตลอดรอบ**
8. **ความครบของวิดีโอ:** `ffprobe` → เฟรมจริงเทียบ `duration x fps` · **รายงานเฟรมที่หายเป็นตัวเลข** 🔴 บอกว่าไฟล์ครบแค่ไหน ไม่ได้บอกว่าในเฟรมมีอะไร
9. 🔴🔴 **ชั้นนี้ตอบไม่ได้:** **`composed = 115` และ `sent = 115` ไม่ใช่หลักฐานว่ามีอะไรขึ้นจอแม้แต่ตัวเดียว** · **`M1` ปิดด้วยชั้นนี้ไม่ได้เด็ดขาด**

**ชั้น (2) client-observable — ต้องมีคนหน้าจอ · 🔴 ตัวปิดใบและตัวปิด `M1` อยู่ชั้นนี้ชั้นเดียว**
1. **หลักฐานบังคับ:** วิดีโอต่อเนื่องครอบคลุม ≥ 10 นาทีในแมพ · ภาพนิ่ง full-res ≥ 3 ใบ · **sha256 ทุกไฟล์** · **ทุกเฟรมที่อ้างมีบรรทัด `FRAME:`** + **`UNMEASURED_DIST:`**
2. 🎯 **เลขหลักของใบ — ตอบเป็นตัวเลขจริง ห้ามตอบเป็นคำ:**
   - **`seen_max_frame`** = จำนวน NPC มากที่สุดที่นับได้ **ในเฟรมเดียว** + ชื่อไฟล์เฟรมนั้น + บรรทัด `FRAME:`
   - **`seen_tour_total`** = จำนวนตัวที่นับได้ตลอดทัวร์ **แบบไม่นับซ้ำ** + **วิธีตัดตัวซ้ำ เขียนเป็นภาษาคน**
   - **ตารางต่อจุด `S0..S5`:** HUD `X/Y` · `t` ที่ถึงจุด · จำนวนที่นับได้ · ไฟล์ภาพ
   - 🔴 **`seen` น้อยกว่า `sent` ไม่ใช่ FAIL** — เป็นค่าที่วัดได้ · 🔴 **ห้ามอนุมานสาเหตุ**
3. **กฎข้อ 2 (สะสม) — ตอบทีละบรรทัด ห้ามยุบรวม:** ล็อกอิน **ผ่าน/ไม่ผ่าน** · หน้าเลือกตัวละคร **ผ่าน/ไม่ผ่าน** · เดิน `W/A/S/D` **ผ่าน/ไม่ผ่าน** · **อยู่ครบ 10 นาทีโดยไม่หลุด ผ่าน/ไม่ผ่าน** (พร้อมเวลาจริงสองค่า)
4. **ประโยคของเจ้าของ (กฎข้อ 4) — คัดคำต่อคำ ห้ามเรียบเรียงใหม่:** *"ผู้เล่นทำอะไรได้ ที่เวอร์ชันก่อนทำไม่ได้"* + *"เมืองมีชีวิตหรือยัง"*
   - 🔴 **ผู้ช่วยห้ามเขียนประโยคนี้แทนเจ้าของ** — ถ้าเธอไม่ได้พูด ให้เขียนว่า **"เจ้าของยังไม่ได้ให้ประโยคนี้"**
5. **ตารางสีป้ายชื่อครบทุกป้ายทุกภาพ full-res** (PLAYBOOK ข้อ 13)
6. **NO-CRASH / CRASH verdict** (ตัดสินด้วยคลิกขวาลากเท่านั้น)
7. 🔴 **ชั้นนี้ตอบไม่ได้:** เซิร์ฟเวอร์ประกอบ/ส่งไปกี่ตัว · บูตมีแฟล็กหรือไม่ · ทำไม `seen` ไม่เท่า `sent`

🔴 **ชั้น (1) ไม่ผ่านข้อ 2 (พบแฟล็ก scenario) ⇒ NO-RESULT ทางเทคนิคทันที — ห้ามอ่านจอเป็นผลใด ๆ แม้เห็นเมืองแน่นไปหมด**

### ตารางผลลัพธ์ที่มีชื่อ — **ทุกทางออกอ่านได้**

| # | สิ่งที่เห็น | คำตัดสิน | อนุญาตให้สรุปว่า | 🔴 **ไม่** อนุญาต / redirect |
|---|---|---|---|---|
| **V1** SHIPPED | ไม่มีแฟล็ก · `seen` ≫ 3 หลายจุด · กฎข้อ 2 ผ่านครบ · ≥10 นาที | ✅ **PASS — `M1` ถึง · เรามี `v1` แล้ว** | ว่า **คอมมิตนี้คือ `v1`** ⇒ cc เขียนบล็อก `v1` ลง `SERVER_VERSIONS.md` พร้อม sha จริง | ❌ ห้ามเขียนว่า "ไคลเอนต์รับได้ 115" ถ้า `seen < sent` · ❌ ห้ามอ้าง `sent` เป็นเลขบนจอ |
| **V2** SHIPPED-WITH-CAP | เมืองมีคนจริง **แต่ `seen` น้อยกว่า `sent` ชัด ๆ** | ✅ **PASS ของ `M1` ได้ (เจ้าของตัดสิน)** + 🎁 **finding ใหญ่** | ว่า **ในรอบนี้ ที่มุม/ระยะเหล่านี้ นับได้ `seen_max_frame` ตัว** | ❌ **ห้ามเรียกว่า "เพดานของไคลเอนต์"** · **redirect: เปิดใบวัดเพดานของตัวเอง** |
| **V3** NO-CHANGE 🔴 | ไม่มีแฟล็กแล้ว **ยังเห็นเท่าเดิม (~3 ตัว)** | 🔴 **ผลลบที่สะอาด มีค่าเท่าผลบวก** ⇒ **`M1` ยังไม่ถึง** | ว่า **`BUILD-001` ยังไม่ถึงจอในเส้นทางดีฟอลต์** | ❌ **ห้ามสรุปว่าไคลเอนต์รับไม่ได้** · **redirect: อ่าน `composed`/`sent` ก่อนอย่างอื่น** — `115/115/seen=3` = ปัญหาฝั่งไคลเอนต์/การมองเห็น · `composed=3` = **ปัญหาฝั่งโค้ด ⇒ ส่งกลับสาย A ทันที ไม่ต้องใช้รอบ attended อีกรอบ** |
| **V4** REGRESSION 🔴 | ของ `v0` พังข้อใดข้อหนึ่ง | 🔴 **FAIL ของ `M1` ทันที แม้เห็น NPC เต็มเมือง** | ว่า **นี่ไม่ใช่เวอร์ชันใหม่ นี่คือของเสีย** | ❌ ห้ามปล่อย `v1` · ❌ ห้ามชี้สาเหตุ · **redirect: ส่งกลับสาย A + chief ทันที · เก็บ console ทั้งไฟล์ · restart server ก่อนรอบถัดไป** |
| **V5** CRASH / DISCONNECT | หลุด/ค้างก่อน `+600` | 🟡 ผลที่มีชื่อ **และอาจเป็นเพดานที่วัดได้** | จดว่าหลุดที่ `t` เท่าไร · ตอนเข้าแมพหรือระหว่างเดิน · `sent` เท่าไรตอนนั้น | ❌ ห้ามชี้สาเหตุ · ❌ **ห้ามลดเลข 115 เองเพื่อให้ผ่าน** — ไล่ลงต้องเป็นคำสั่ง COO และเป็นใบใหม่ |
| **V6** OWNER-ABSENT | เก็บครบ **แต่คนหน้าจอไม่ใช่เจ้าของ** | 🟡 **ชั้น (1) ใช้ได้ · `M1` ปิดไม่ได้** | ว่า **ชั้นเทคนิคผ่านแล้ว** | ❌ **ห้ามเขียนว่า `M1` ถึง** · **redirect: รันซ้ำ commit เดิมโดยเจ้าของนั่งเอง — ไม่นับเป็นเวอร์ชันใหม่** |
| **V7** NON-OBSERVED | ไม่ได้อัดวิดีโอ · บูตมีแฟล็ก · `T0` หาไม่เจอ · วิดีโอหายช่วง | 🔴 **NO-RESULT — ไม่ใช่ผลลบ** | ไม่มี | ❌ ห้ามอ่านจอเป็นผล · **redirect: รันซ้ำ commit เดิม · 🔴 ห้าม archive ใบ** |

### 🔁 ผลลบของรอบนี้จะ redirect ไปไหน — เขียนก่อนบูตตามกติกา
> - `V3` + `composed=3` ⇒ **PR ไม่ได้อยู่บนเส้นทางดีฟอลต์จริง** ⇒ กลับสาย A · **ตรวจได้ headless ไม่ต้องใช้รอบ attended อีกรอบ**
> - `V3` + `115/115` ⇒ **คำถามใหม่ทั้งใบ: ไคลเอนต์ทำอะไรกับ actor ที่ได้รับ** ⇒ เปิดใบวัดเพดาน/การมองเห็นเป็นใบของตัวเอง · **ห้ามแตะโค้ดจนกว่าจะมีใบนั้น**
> - `V4` ⇒ **หยุดเลน `M2` ทันที** — `CHARTER-02` ⑤ กฎข้อ 2 · **กำหนดแพ้วินัย ไม่ใช่วินัยแพ้กำหนด**
> - `V5` ⇒ ได้เลขเพดาน "จำนวนที่ส่งแล้วไคลเอนต์อยู่ไม่ได้" ⇒ **มีค่ากับ `M3`–`M6` ทุกใบ** ⇒ ส่ง COO ตัดสิน (**ผู้เทสไม่ตัดสินข้อนี้**)

### ⭐ PLAYBOOK ข้อ 13 — บันทึกสีของ **ทุกป้ายชื่อในเฟรม** (คำสั่ง Panya 2026-08-25 · บังคับทุกใบ attended ตั้งแต่ R163)
- **จดอะไร:** ชื่อตัวเราเอง (เหนือหัว + แผง UI ซ้ายบน) · ชื่อ NPC/actor ทุกตัวในเฟรม · ชื่อไอเทมบนพื้น · ชื่อผู้เล่นคนอื่น · บรรทัด title/คำอธิบาย — **หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ**
- **ไม่มีให้เขียนคำว่า "ไม่มี" ออกมาเป็นตัวอักษร** 🔴 **ห้ามเว้นว่าง**
- **อ่านสีจากภาพนิ่งความละเอียดเต็ม / crop PNG เท่านั้น** 🔴 **ห้ามอ่านจาก contact sheet · ห้ามภาพย่อ · ห้ามจากวิดีโอ** ⇒ `evidence_screens\GT078_<TAG>_FULLRES_<yyyyMMdd_HHmmss>.png|jpg` (**ไฟล์ใหญ่เกินให้ crop จากต้นฉบับ ห้าม resize ลง**) · **sha256 ทุกไฟล์**
- 🆕 **ใบนี้ป้ายจะเยอะกว่าทุกใบที่ผ่านมา** ⇒ จดครบเท่าที่ **อ่านออก** แล้วเขียนตัวเลขว่า **"อ่านไม่ออก/ถูกบัง N ป้าย"** 🔴 **ห้ามข้ามเงียบ ๆ ห้ามเดาสีของป้ายที่อ่านไม่ออก**
- **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับ:** NPC = **เหลือง** · ผู้เล่น = **เขียว** · ไอเทมบนพื้น = **ขาว** · title = **ฟ้า** · ชื่อตัวเอง = **ขาว**
- 🔴🔴 **ผู้เทสจด "สี" อย่างเดียว ห้ามสรุปสาเหตุ** — อะไรตัดสินสีคือ `RE-067` (ครึ่ง actor อยู่ที่ `RE-068`) ⇒ **ห้ามเขียนว่า "แปลว่าไคลเอนต์จัดมันเป็นผู้เล่น/NPC/ศัตรู"**
- **`REAL_SERVER_DIVERGENCE.tsv`: 🔴 ส่งค่ากลับมาในจดหมายผล ห้ามแก้ไฟล์เองจากหน้าสะพาน** · หนึ่งแถวต่อหนึ่งป้าย (**TAB** · อ่านหัวไฟล์ก่อน) · `evidence_layer` = **`eye`** เสมอ · `open_ticket` = **`RE-067`** · `blocks_promotion` = `no` · **เติมแถวแม้ผลจะ "ตรงกัน"**

### 🧾 teardown + ใบเสร็จ (บังคับ — **แม้รอบจะจบเพราะคนเลิกเล่น**)
- **teardown เสมอ ภายใน 420 นาทีจาก boot stamp** (`staged\TEMPLATE_teardown_generic.ps1:135` · **เพดานถูกยกจาก 180 เมื่อ 2026-08-20 · เลข 180 ในใบเก่า = stale**) — เกินเพดาน **ปฏิเสธ exit 12 โดยดีไซน์**
- แท่นที่ถูกทิ้งข้ามชั่วโมง: **อย่าฝืน template** ⇒ `staged\TOOL_stop_stale_server.ps1` แล้วตามด้วย receipt อ่านอย่างเดียว `staged\0949_gt027_stalepad_canonical_guard.ps1`
- ได้ **exit 36** อย่าเดาเอง — แนบบรรทัดที่ 17 ของไฟล์ teardown ที่ใช้จริงมาทั้งบรรทัด
- **ใบเสร็จที่ต้องแนบ:** `AFTER listeners = 0` · **canonical guard: sha256 ก่อน-หลัง = `CANON_SHA.txt`** · **teardown exit code** · `LOCK_GAME` ปล่อยแล้ว · run copy `state\run_gt078*.sqlite3` **เก็บไว้ให้ chief re-derive ห้ามทิ้ง** · path ของ raw GAME log + console out/err + วิดีโอ + ภาพทุกไฟล์ พร้อม **sha256**
- 🔴 **บนสะพานเท่านั้น ห้ามลบ:** `.mkv` ต้นฉบับ และโฟลเดอร์ capture ของรอบ · 🔴 **restart เซิร์ฟเวอร์ก่อนบูตรอบถัดไปเสมอ**

### `BUILD_IMPACT` (กฎ `BUILD-003` · บังคับก่อนถือว่าปิดใบ)
```
BUILD_IMPACT: v1 = คอมมิตที่บูตได้จริงโดยไม่มีแฟล็ก -> cc เขียนบล็อก v1 ลง SERVER_VERSIONS.md
              (5 บรรทัด: commit / ผู้เล่นทำอะไรได้เพิ่ม / ยังทำไม่ได้ / regression ที่ตรวจแล้ว)
              + seen_max_frame กลายเป็นตัวเลขตั้งต้นของงบประชากรทุกฉากใน M2-M6
              + ถ้าผลเป็น V3/V4 -> BUILD_IMPACT คือ "ไม่มี" พร้อมชั้นที่พัง (composed / sent / seen) เขียนตรง ๆ
```
🔴 **บรรทัด `regression` ใน `SERVER_VERSIONS.md` เขียนจากการ *เล่นจริง* เท่านั้น ไม่ใช่จากการที่เกตเขียว**
🔴 **ผู้เทสส่งค่ามา ห้ามแก้ `SERVER_VERSIONS.md` เองจากหน้าสะพาน**

### nonclaims (ติดไปกับผลทุกกรณี **ห้ามตัดทิ้ง**)
① 🔴🔴 **`composed`/`sent` ไม่ใช่ `seen`** — เฟรมออก **≠** ไคลเอนต์รับ **≠** ไคลเอนต์วาด **≠** คนเห็น · **ห้ามยกเลขหนึ่งไปตอบแทนอีกเลขในทุกเอกสารต่อจากนี้**
② **`seen` ของรอบนี้ไม่ใช่ "เพดานของไคลเอนต์"** — ไม่มีตัวคุมเรื่องระยะ มุมกล้อง ซูม culling หรือ LOD เลย · มันคือ "จำนวนที่คนหนึ่งคนนับได้ในทัวร์หนึ่งรอบ"
③ **ไม่พิสูจน์กลไกฝั่งไคลเอนต์แม้แต่นิดเดียว** — **ไม่มีหลักฐาน static แม้แต่บรรทัดเดียวในโปรเจกต์**
④ **ไม่ตอบอะไรเลยเรื่อง `scene_id != 1` / แมพที่สอง** — นั่นคือ `M2`/`BUILD-002`
⑤ **ไม่ตอบอะไรเลยเรื่องมอนสเตอร์/สีแดง/การตี/การตาย/การเก็บของ** — `M3`–`M5` · เห็นอะไรแปลกให้จดเป็น **ข้อสังเกตฟรี ไม่ใช่ผลของใบ**
⑥ **ไม่ตอบเรื่องของที่ค้างข้ามวัน** — รันบนสำเนา `run_gt078.sqlite3` ส่วนโลกที่เจ้าของเล่นคือ `state\play.sqlite3` **คนละไฟล์**
⑦ **ไม่ตอบเรื่องการหายของ NPC ที่ถูก spawn ทับ** — `GT-072`/`GT-074` · รอบนี้ **ไม่มี `SPAWN_BARE` เพราะไม่มีแฟล็ก**
⑧ **รอบเดียวไม่ใช่คุณสมบัติของไคลเอนต์** — เครื่องเดียว แมพเดียว ทัวร์เดียว มุมกล้องชุดเดียว
⑨ **สีอ่านด้วยตาจากภาพ ไม่ได้วัดค่าพิกเซล** ⇒ **ไม่ claim ค่า RGB/hex** · `evidence_layer` = **`eye`** · **ห้ามอนุมานสาเหตุจากสี (`RE-067`)**
⑩ **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับอาจเป็น client คนละ build/ภูมิภาค** ⇒ "ต่างจากภาพต้นฉบับ" ยังไม่เท่ากับ "ของเราผิด"
⑪ **ตาราง placement 115 ตัวเป็นของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้วและกู้ไม่ได้ตลอดกาล ⇒ **"เมืองเหมือนของจริง" เป็นความรู้สึก ไม่ใช่ข้ออ้างที่ใบนี้พิสูจน์**
⑫ **`OBSERVER_CONFIRMED` และ `G-FRAME` เป็นขั้นตอน ไม่ใช่หลักฐาน**
⑬ **ไม่มีใครวัดว่าล้อเมาส์ (ซูม) ยิงไบต์อะไรออกสายหรือไม่** — จึงบังคับให้จดเวลาที่ซูมทุกครั้ง
⑭ **การผ่านใบนี้ไม่ปลด `M2`–`M6` แม้แต่ข้อเดียว** และ **ไม่ปลดใบที่ยังไม่ถูกเทสในคิวนี้แม้แต่ใบเดียว**
⑮ 🆕 **ไม่ตอบอะไรเลยเรื่องราคาของการคลิก NPC หลังสำมะโน** — คลิกหนึ่งครั้งตอนนี้ประกอบ population ทั้งชุดใหม่ (~17.9 KB) และ **ไม่มีใครวัดว่าไคลเอนต์ทำอะไรกับมัน** ⇒ ถ้าเกิดขึ้นในรอบนี้เป็น **ข้อสังเกตฟรี** และ **ต้องเป็นใบของตัวเอง** ห้ามผูกกับผลของใบนี้
⑯ 🆕 **ไม่รับรองว่าการต่อสายของ chief ถูกต้องโดยทั่วไป** — พิสูจน์ได้แค่ว่า **บูตนี้ประกอบได้เท่าไร ส่งออกกี่ใบ และเจ้าของเห็นอะไร** · **event ที่ยังเขียนว่า `v129_isolated_population_retained_p0_p30_p91` เป็นถ้อยคำที่ล้าสมัยของ v141 ที่แช่แข็งไว้ — ไม่ได้แปลว่าสำมะโนล้มเหลว ห้ามอ่านเป็นผลลบ**

- **result:** (ผู้เทสกรอก: ① เช็คลิสต์ปลดบล็อก 5 ข้อทีละข้อ + `BOOT_COMMIT` ② **`CommandLine` ของโปรเซสเซิร์ฟเวอร์ทั้งบรรทัด** ③ **`composed` / `sent` / `seen_max_frame` / `seen_tour_total` — สี่เลขแยกกัน ห้ามยุบรวม** + วิธีนับที่ใช้จริง ④ ตารางต่อจุด `S0..S5`: HUD `X/Y` · `t` · จำนวนที่นับได้ · ไฟล์ภาพ (**ทุกไฟล์มีบรรทัด `FRAME:`**) + **`UNMEASURED_DIST: <n>/<ทั้งหมด>`** ⑤ กฎข้อ 2 ทีละบรรทัด: ล็อกอิน / เลือกตัวละคร / เดิน / **≥10 นาที (เวลาจริงสองค่า)** ⑥ **ประโยคของเจ้าของสองประโยค คัดคำต่อคำ** ⑦ **แถวไหนของตารางผล (V1-V7)** ⑧ **ตาราง PLAYBOOK ข้อ 13 ครบทุกป้ายทุกภาพ full-res ("ไม่มี" เขียนออกมา + จำนวนป้ายที่อ่านไม่ออก)** ⑨ ค่าที่ต้องเติม `REAL_SERVER_DIVERGENCE.tsv` (**ส่งค่ามา ห้ามแก้ไฟล์เอง**) ⑩ census บรรทัด `[G>]` ทั้งไฟล์ + มี `ErrorData=28317` ไหม + NO-CRASH/CRASH ⑪ `ffprobe` เฟรมที่หายเป็นตัวเลข ⑫ path raw GAME log + console ทั้งไฟล์ + วิดีโอ + ภาพทุกไฟล์ พร้อม sha256 ⑬ เวลา +07:00 · sha canonical ก่อน-หลัง · `integrity_check` · row-diff + `max(lease_generation)` ของ `run_gt078*.sqlite3` · exit code ของ teardown ⑭ **บรรทัด `BUILD_IMPACT:` ฉบับจริงหลังรู้ผล** ⑮ บรรทัด `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ⑯ ถ้ามี session 2: ทุกข้อข้างบนแยกชุด **ห้ามรวมกับ session 1**)

---

## 🆕 GT-079 SCENE-278-ENTRY-AND-STAGE-EYECHECK-001 [attended, in-game]: ไคลเอนต์ตัวนี้ **เข้า** ฉาก 278 (`Bg1177`) ได้จริงหรือไม่ · แมพที่ขึ้นคือแมพไหน · และสิ่งที่ยืนอยู่คือ **เวทีกว้าง เรียบ โล่ง** อย่างที่เจ้าของขอหรือไม่  [🔴 **BLOCKED — BLOCKED-ON-WIRING** (ยังไม่มีเส้นทาง runtime ไร้แฟล็กที่ส่ง `scene_id=278`) · เปิดใบโดย LANE-A 2026-08-26 ~01:2x (+07:00) ตาม `CHARTER-02` §⑤ BUILD-002 สไลซ์ 1 · ร่างใบโดย `pf-queue-author` · **แก้ตามผล `pf-adversary` ก่อนวาง**]

> 🔢 **เรื่องเลขใบ:** ตัวนับเป็น **ชุดเดียวร่วมกับ `CLIENT_RE_QUEUE.md`** — prefix สองแบบ ตัวนับเดียว
> `GT-074` (chief R170) · `RE-075` · `GT-076` (BUILD-001) · **`RE-077`** ถูกใช้แล้วทั้งหมด · grep ยืนยันก่อนจอง: `GT-079`/`RE-078` = **0 hit ทั้งสองไฟล์** ⇒ **ใบนี้คือ `GT-079`** · **เลขว่างถัดไป = 079**
> 🔴 **ใบ `GT-030` · `GT-030-R3` · `GT-072` · `GT-074` · `GT-076` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ** — ใบนี้เป็นใบใหม่ ไม่ใช่ใบแทนใคร

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
8. 🔴 **ปิดด้วยผลลบได้เฉพาะรอบที่คุณ Panya เห็นเอง + มีวิดีโอต่อเนื่อง** (`AGENTS.md` §9)
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
