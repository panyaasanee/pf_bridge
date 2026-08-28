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

- 🔥 **ใบแรกของกะ attended ถัดไป — ก่อนใบอื่นทั้งหมด รวม `GT-131`** (คำสั่ง COO 2026-08-28 23:45 ข้อ 3 · จดหมาย `20260828_2345_COO-DECISION-multi-drop-shape-ships-with-a-bounded-blast-radius.md`) · 🆕 **`GT-132` GROUND-DROP-COALESCED-GENERATION-DRAWS-N-LABELS-001** (🟢 **READY — attended · ศูนย์สล็อต ไม่มีแฟล็ก** · เปิดโดย LANE-B รอบ `zxnwtd` ต่อจาก `RE-130` ✅ CLOSED · ฆ่ามอนตัวที่ตกของ ≥ 2 ชิ้น แล้ว**นับป้ายชื่อไอเทมสีแดงจากเฟรมวิดีโอ** · เซิร์ฟเวอร์เปลี่ยนทรงส่งเป็น collection เดียว count=N แล้ว · 🔴 มีด่านบิลด์บังคับก่อนนับ (`generations=1` ในคอนโซล) · `1` ป้าย = **FAIL ของใบนี้** (coalesce ไม่ซื้ออะไรให้ผู้เล่น) · ใบเต็มอยู่ท้ายไฟล์)
- 🆕 **`GT-079` SCENE-278-ENTRY-AND-STAGE-EYECHECK-001** (🔴 **BLOCKED — BLOCKED-ON-WIRING** · ยังไม่มีเส้นทาง runtime ที่พาผู้เล่นเข้าฉาก 278 · เปิดใบโดย LANE-A ตาม `CHARTER-02` BUILD-002 สไลซ์ 1 (v2 / M2 · กำหนด 26 ส.ค. 23:59) · ถามด้วยตาหกข้อ: เข้าได้ไหม **และ HUD บอกว่าแมพอะไร** (ตัวแยกการอ่านค่า `scene_id` สี่แบบ) · มีพื้นไหม · กว้าง-เรียบ-โล่งไหมและสีอะไร · `BgNull` เสียหายไหม · เก้า placement โผล่ไหม · เดินได้และอยู่ครบ 10 นาทีไหม · 🔴 **มีขั้นตอนบังคับ "ทางกลับบ้าน"** เพราะฉาก 278 มี `n_MARKER=0`/`n_SAVE=0` · **ไม่ใช่ใบเรื่องการ *ย้าย* ฉากขณะ live — นั่นคือ `RE-077`** · ใบเต็มอยู่ท้ายไฟล์)
- 🆕 **`GT-080` EMPTY-VIEW-IS-THE-MAP-NOT-THE-SEND-001** (🟢 **หัวใบเดิมล้าสมัย — แก้โดยเจ้าของใบ LANE-A รอบ `o8cy9q` 2026-08-28T18:41+07:00:** เหตุบล็อกเดิมหมดไปแล้ว · วัดบน `main` รอบนี้: `runtime.py` **import ทั้ง `world_population` และ `world_density` จริง** และ `GT-121` ผ่าน (PASS) ยืนยันเส้นทางไร้แฟล็กส่งสำมะโนแล้ว ⇒ **ไม่ใช่ `BLOCKED-ON-WIRING` อีกต่อไป · ใบนี้รันได้ รอผู้เทสจับคิว** · 🔴 เพิ่มรอบ `o8cy9q`: บูตนี้จะพิมพ์โทเคนใหม่ `WORLD_IDENTITY_GUARD ... identity_provable=0` ต่อท้ายบรรทัด `WORLD_CENSUS` — **เป็นเรื่อง identity ไม่ใช่เรื่องจำนวน ไม่กระทบตัวคุมของใบนี้ อย่าอ่านเป็นความล้มเหลว** (`identity_provable=0` เป็นค่าที่ถูกต้องของทุกฉากตอนนี้ ไม่ใช่อาการผิดปกติ) · ~~ถ้อยคำเดิมของหัวใบ:~~ ~~🔴 **BLOCKED — BLOCKED-ON-WIRING** · `world_population`/`world_density` ยังไม่มีใคร import และเส้นทางไร้แฟล็กยังส่ง 3 ตัว (`v141:1863` `V112_TEST_INDICES=(0,30,91)` ใช้ที่ `:4292`) · เปิดใบโดย LANE-A 2026-08-26 ~02:2x (+07:00) ตาม `CHARTER-02` BUILD-001 / M1 · **แยกสาเหตุที่ `GT-078` แยกไม่ได้:** ยืนแล้วไม่เห็นใคร เพราะ **เซิร์ฟเวอร์ไม่ได้ส่ง** หรือเพราะ **ไฟล์ฉากไม่มีใครวางไว้ตรงนั้น** · ตัวคุมคือ **บูตเดียว สำมะโนเดียว ยืนสองจุด** (A จุดเกิดจริงที่ `GT-045` วัดไว้ census 500u = **0** · B จุดหนาแน่นสุดของฉาก census 2000u = **12**) · **เห็น 0-3 ตัวที่ A = ปกติ ไม่ใช่ความล้มเหลว** · ถ้า B เห็น 0 ทั้งที่ `WORLD_CENSUS assembled=115/115 wire=115` ⇒ ปัญหาอยู่ที่ **การเรนเดอร์** ⇒ ชี้ `GT-072` (ยัง PARTIAL) · **ไม่ใช่ใบวัดเพดาน (`GT-076`) ไม่ใช่ใบตรวจรับ v1 (`GT-078`)** · ใบเต็มอยู่ท้ายไฟล์~~ · 🔴 **ตัวใบเต็มท้ายไฟล์ไม่ถูกแตะ** — แก้เฉพาะหัวใบบรรทัดนี้ ตามกฎ "ห้ามลบประวัติเดิม ให้ขีดฆ่าแทน")
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

## GT-001 Smoke: full-loop บน canonical DB หลังทุก commit สำคัญ  [🔴 **HOLD (recurring) ยังคงอยู่ — ดูการแก้ไขของ chief R175 ใต้หัวใบ** · **PASS ล่าสุด: `f8562c1` (R168) 2026-08-25 20:43 (+07:00) — PASS พร้อม erratum** · *(PASS ก่อนหน้า: `fa1e804` 2026-08-24 09:41 · R145)*] 🔁

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
## GT-063 ITEMOPERATE-RES-GREENLINE-SHAPE-001 [attended, in-game]: ยิง `ItemOperateVitalRes` (`0x4C13`) สามทรงจากเซิร์ฟเวอร์เรา แล้วตัดสินด้วยต... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
## GT-064 SKILL-ATTR-WINDOW-KPRESS-IN-GAP-001 [attended, in-game]: กด **K** / คลิก `Bt_main_Skill` **ภายในช่อง 3.0 วิ ระหว่างเฟรม `COUNT0` (57B... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
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
- 🆕 **และมีบรรทัดของเลนเองที่ตอบครบกว่านั้น พิมพ์ก่อนคิวเฟรมทุกบูต (ไม่ต้องมีแฟล็ก):**
```
WORLD_CENSUS assembled=<n>/115 wire=<n> bodies=ok pc=<pc>B frame=<framed>B anchor=(x,y,z) reapply_ms=3000 source=<why> shortfall=<เหตุผลหรือ none>
```
  🔴 **`wire=` คือจำนวนที่ถอดกลับออกมาจากไบต์จริง ไม่ใช่จำนวนที่ตั้งใจส่ง** · ไม่ตรงกันเมื่อไหร่มันขึ้น `MISMATCH:<n>` · `bodies=SHORT` = header บอกมากกว่าที่มี
  ⇒ **คัดบรรทัดนี้ของทุกบูตมาทั้งบรรทัด** และ **`pc bytes` อ่านจากมันได้ตรง ๆ** ไม่ต้องพึ่ง hexdump หรือ event
- **pc bytes** (**504 / 3148 / 9302 / 17928**) ยังตรวจซ้ำได้จาก **event `world_census_committed_actors_<n>_pc_<pc>_frame_<frame>`** ซึ่งบูตของใบนี้จะเห็น **เพราะใส่ `--export-events`**
- 🔴 **ป้ายโผล่ "หลังก้าวแรก" ไม่ใช่ "ตอนบูต"** — ตัวยิงคือ `TargetPosVital` ใบแรกหลัง runtime ack ตามบล็อก ANCHOR ของใบนี้เป๊ะ ⇒ **`steps` ข้อที่ให้อ่านบรรทัดนี้ ให้อ่าน "หลังแตะ `W` ครั้งเดียว" แทน "ตอนบูต"** · **เกณฑ์เดิมยังอยู่: ไม่มีบรรทัดนี้หลังก้าวแรก หรือเลขไม่ตรงขั้นที่ตั้งใจ = หยุด ปิด server บูตนั้นเป็น NO-RESULT**
- **ป้ายเก่า `V134_P0_P30_P91_ISOLATED_*` ต้องไม่ปรากฏเลยในทุกบูตของใบนี้** — เห็นแทน = **การต่อสายไม่ทำงาน หรือการประกอบถูกปฏิเสธแล้วถอยกลับของเดิมแบบ fail-closed** ⇒ **แถว `N4` CONTROL-BROKEN ⇒ หยุดทั้งใบ ส่ง chief ทันที ห้าม archive ใบ**
  - **หมายเหตุ:** ป้ายนั้น **ยังอยู่ใน `current/pf_login_game_server_v141.py` โดยดีไซน์** (แช่แข็ง + `v141Guard`) ⇒ **การ grep เจอมันในไฟล์ ไม่ใช่หลักฐานว่ายังไม่ต่อสาย** หลักฐานอยู่ที่ **คอนโซลของบูตจริง** เท่านั้น

**pass criteria ไม่เปลี่ยนแม้แต่ข้อเดียว — สองชั้นแยกกันเหมือนเดิม:**
- **ชั้น (1) wire/DB (headless ได้):** ข้อ "บรรทัดจำนวน actor ที่คอนโซลพิมพ์ ตัวอักษรเป๊ะ" **ตอบด้วยป้าย `WORLD_CENSUS_INITIAL_<RUNG>` ทั้งบรรทัด** · ข้ออื่นคงเดิมทุกตัวอักษร
- **ชั้น (2) client-observable (ต้องมีคนหน้าจอ):** **ไม่มีอะไรเปลี่ยน** · 🔴 **ป้ายบนคอนโซลไม่ใช่หลักฐานว่ามีอะไรขึ้นจอ และจำนวนหัวที่นับได้ไม่ใช่หลักฐานว่าส่งไปกี่ตัว**
- **nonclaim ที่บล็อกนี้เพิ่ม:** **แฟล็กนี้ไม่ได้ทำให้ "บูตของ `GT-076` เท่ากับบูตดีฟอลต์"** — บูตของใบนี้มี `--export-events` และมีตัวเลือกขั้น ⇒ **ใบนี้ยังไม่ปิด `M1` และยังไม่แทน `GT-078`** · ใบที่ตรวจรับเส้นทางไร้แฟล็กด้วยตาเจ้าของคือ **`GT-078`** และ **ใบนั้นห้ามใส่แฟล็กนี้เด็ดขาด**

---

## GT-078 M1-V1-ACCEPTANCE-PORT-ROYAL-POPULATION-115-001 [attended, in-game]: บูตเซิร์ฟเวอร์ **โดยไม่มีแฟล็ก scenario แม้แต่ตัวเดียว** แล้วเจ้าของเดินทั่ว Port Royal — **เมืองมีคนอยู่จริงหรือไม่ และของเดิมทั้งหมดยังเล่นได้อยู่ไหม** (ใบตรวจรับ `v1` ของ `M1`)  [🟡 **RAN 2026-08-26 12:55-13:37 +07:00 · ชั้น wire PASS ครบ (115/115) · OWNER-REJECTED บนชั้น identity — ห้ามปิดเป็น PASS** · `OBSERVER_CONFIRMED: 2026-08-26T14:10+07:00` · **`v1` ยังไม่ประกาศ** (`COO-DECISION` 2026-08-26T14:42+07:00: placement ถูกทุกจุด แต่ตัว NPC ที่เกิดจริงผิดทุกตัว เทียบกับ capture เซิร์ฟเวอร์เดิม — ดู `REAL_SERVER_DIVERGENCE.tsv` แถวใหม่ 4 แถว 2026-08-26T14:40) · **ใบนี้เปิดค้างไว้ ไม่ปิดเดี่ยว** รอตาราง placement→identity/name/title ของ `bg0001` จากสาย A + RE (อย่างน้อยสามตัวอย่าง Hields/Sase/Columbus) แล้ว `pf-queue-author` จะร่างใบ retest ต่อ · ผลเต็ม: `notes_to_chief/consumed/20260826_1430_GT078-RESULT-*.md` + addendum `20260826_1440_GT078-ADDENDUM-*.md` · ~~ถ้อยคำเดิมของใบ (ก่อนรัน)~~ [🔴 **BLOCKED — รอ merge ก่อน · เหลือเงื่อนไขเดียว** · **ไม่ใช่ `BLOCKED-ON-WIRING` อีกต่อไป (แก้โดย chief R173)**: การต่อสาย `WORLD-CENSUS-001` เข้าเส้นทางดีฟอลต์ **เขียนเสร็จแล้วในรอบ R173** ที่ `src/pirateforce_foundation/runtime.py` (`world_census_enabled = not active_lanes`) + `src/pirateforce_foundation/app.py` **แต่ยังไม่เข้า `main`** ⇒ **ใบนี้รออย่างเดียวคือ PR ของรอบ R173 merge เข้า `main`** · `BUILD-001` (สาย A · PR #78 · `11166a1`) อยู่บน `main` แล้ว **และใบนี้ไม่ได้รอสาย A อีกต่อไป** · **ปลดบล็อกเองไม่ได้ ต้องเดินเช็คลิสต์ปลดบล็อก 5 ข้อในใบนี้ให้ครบก่อน (ข้อ 3 และ 4 ใช้ฉบับแก้ R173)** · attended · **ต้องเป็นเจ้าของนั่งหน้าจอเอง** · กำหนดของ `M1` = **2026-08-26 12:00 (+07:00)** · เปิดใบตาม `COO-CHARTER-01` ④ + `COO-CHARTER-02` ①④⑤ · เขียนใบโดย `pf-queue-author` · **เลขใบเคาะโดย chief R172**]

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
   🆕 **หมายเหตุ chief R174 (2026-08-26 ~12:0x +07:00):** PR ของ R173 (**#41**) เขียวมา 15 ชั่วโมงแล้วไม่มีใครปลุก merge job ⇒ `main` ขยับผ่านมันไป ⇒ workflow ปิด PR #41 ทิ้งแบบ **ไม่ merge** (`COO-ESCALATION-LANE-E` วัดไว้) · กู้คืนสามคอมมิตของ #41 ด้วย `git merge` เข้า branch ของรอบนี้ (`claude/sweet-franklin-mqus9y`) แล้ว push แล้ว: **commit `917f4d6`** (merge, ผ่าน `pf-adversary` อิสระก่อน push) — **แต่ยังอยู่บน branch ของ PR ที่ยังไม่ merge ยังไม่ใช่ "บน `main`"** ⇒ ข้อ 1 นี้ยัง **BLOCKED** จนกว่า PR ของรอบ R174 จะ merge เข้า `main` จริง (เกตต้องเขียวก่อน)
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
   - 🆕 **แก้ไขซ้ำ (chief R173 ตอนท้ายรอบ): มีบรรทัดของเลนเองแล้ว ไม่ต้องอ่านจากป้ายอย่างเดียว**
     สาย A เขียน `census_console_line()` และ chief เรียกมัน **ก่อนคิวเฟรม** ⇒ **บูตธรรมดาพิมพ์บรรทัดนี้เอง ไม่ต้องมี `--export-events`**
```
WORLD_CENSUS assembled=115/115 wire=115 bodies=ok pc=17928B frame=17942B anchor=(x,y,z) reapply_ms=3000 source=full_census shortfall=none
```
     🔴 **นี่คือบรรทัดที่ตอบ `composed` โดยตรง และมันหักล้างตัวเองได้:** `assembled` = ที่ประกอบ · `wire` = จำนวนที่ **ถอดกลับออกมาจากไบต์ที่จะส่ง** ·
     `bodies=ok|SHORT` = ตัวจับกรณี "header บอก 115 แต่ body ไม่ครบ" · **`wire` ขึ้นเป็น `MISMATCH:<n>` เมื่อสองเลขไม่ตรง**
     ⇒ **คัดบรรทัดนี้มาทั้งบรรทัด และคัดป้าย `[G>]` มาด้วย ทั้งสองอย่าง ไม่ใช่อย่างใดอย่างหนึ่ง**
   - **บรรทัดที่ต้องอ่านและคัดมาทั้งบรรทัด** (v141 พิมพ์ทุก action ตอน **ส่ง** ที่ `current/pf_login_game_server_v141.py:7762`):
```
[G>] WORLD_CENSUS_INITIAL_115 (17942 bytes; late=0.0 ms)
[G>] WORLD_CENSUS_REAPPLY_115 (17942 bytes; late=<ms> ms)
```
     ใบ `REAPPLY` มาหลังใบแรกประมาณ **3.00 วินาที** · **จดทั้งสองใบ ห้ามจดใบเดียว**
   - 🔴 **เตือนเรื่องคอนโซลล้น (วัดโดย `pf-adversary` R173):** v141 พิมพ์ **hexdump ของทุก action ที่ป้ายไม่ขึ้นต้น `V98_LOCAL_REFRESH_`/`V141_LOCAL_REFRESH_`** (`v141:7768`)
     ⇒ เฟรมสำมะโนหนึ่งใบ = **~1,121 บรรทัด** · สองใบ = **~2,242 บรรทัดต่อบูต** (เดิม ~64)
     ⇒ **บัฟเฟอร์ของ conhost กลืนบรรทัด `[MILESTONE]` และ ack/welcome/music ไปหมดก่อนที่คุณจะอ่านทัน**
     ⇒ **อ่านจากไฟล์ log ไม่ใช่จากการเลื่อนจอ** · **นี่คือราคาที่รู้ล่วงหน้า ไม่ใช่อาการผิดปกติ ห้ามล้มบูตด้วยเหตุนี้**
   - **สามเลขของใบนี้แมปกับอะไร — กฎเดิมยังอยู่ครบ: 🔴 ห้ามยุบรวม ห้ามใช้เลขหนึ่งแทนอีกเลข**
     - **`composed`** = **ตัวเลขที่ต่อท้ายป้าย** (`..._INITIAL_115` ⇒ `composed = 115`) · **ไม่มีป้าย `WORLD_CENSUS_*` เลยหลังก้าวแรก ⇒ เขียน `composed = unmeasured` หรือ `composed = 3` ตามป้ายที่เห็นจริง ห้ามเดาจากจอ**
     - **`sent`** = อ่านจาก `GAME_LIVE.txt` · **ตัวเลขในวงเล็บของคอนโซล = framed bytes** (คาด **17942**) · **pc bytes** (คาด **17928**) อ่านได้จาก **hexdump ที่ v141 พิมพ์ต่อท้ายป้ายนั้น** เท่านั้น — **อ่านไม่ออกให้เขียน `pc = unmeasured`**
     - **`seen`** = ชั้น (2) เท่านั้น **ไม่มีบรรทัดคอนโซลใดตอบข้อนี้ได้**
     - 🔴 **`composed = 115` เป็นเลขของ "ประกอบได้" ห้ามเขียนว่า "ไคลเอนต์รับ 115" และห้ามเขียนว่า "มี 115 ตัวบนจอ"**
   - **event `world_census_committed_actors_115_pc_17928_frame_17942` มีจริง แต่ใบนี้จะไม่เห็น** เพราะมันโผล่เฉพาะเมื่อมี `--export-events` ซึ่ง **ใบนี้ห้ามใส่** ⇒ **อย่ารอมัน อย่าเติมแฟล็กเพื่อจะได้เห็นมัน** · 🆕 **แต่ `pc=17928B` อ่านได้จากบรรทัด `WORLD_CENSUS ...` ข้างบนแล้ว** ⇒ กฎ `pc = unmeasured` ใช้เฉพาะกรณีที่บรรทัดนั้นไม่ขึ้น
   - 🆕 **ป้าย `V134_*_ISOLATED` โผล่พร้อมกับ event `world_census_fell_back_to_frozen_p0_p30_p91`** = **เลนปฏิเสธการประกอบแล้วถอยกลับไปของเดิมโดยตั้งใจ** (fail closed) ⇒ **`composed = 3` และเป็นผลที่อ่านได้ ไม่ใช่บูตเสีย** · ถ้าเห็นป้ายนั้น **โดยไม่มี** บรรทัด `WORLD_CENSUS ...` และ **ไม่มี** event นั้น ⇒ **การต่อสายไม่ทำงานในบูตนั้น**
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

---

## 🆕 GT-080 EMPTY-VIEW-IS-THE-MAP-NOT-THE-SEND-001 [attended, in-game]: ยืนสองจุดในบูตเดียวที่สำมะโน **ไม่เปลี่ยนแม้แต่ไบต์เดียว** — **"ไม่เห็นใคร" ที่จุดเกิดเป็นคุณสมบัติของ *ที่ที่ยืน* หรือของ *จำนวนที่ส่ง***  [🔴 **BLOCKED — BLOCKED-ON-WIRING** (`world_population` / `world_density` ยังไม่ถูก import จาก `runtime.py` หรือ `app.py` เลย — grep ทั้งแพ็กเกจ) · เปิดใบโดย LANE-A (สาย A · WORLD) 2026-08-26 ~02:2x (+07:00) ตาม `CHARTER-02` BUILD-001 / M1 · ร่างใบโดย `pf-queue-author` · **แก้ตามผล `pf-adversary` ก่อนวาง**]

> 🔴 **เรื่องเลขใบ:** ตัวนับเป็น **ชุดเดียวร่วมกับ `CLIENT_RE_QUEUE.md`** — prefix สองแบบ ตัวนับเดียว **ห้ามแยกตัวนับ**
> `GT-074` (chief R170) · `RE-075` · `GT-076` (BUILD-001) · `RE-077` · `GT-078` (chief R172) · `GT-079` (LANE-A) ถูกใช้แล้วทั้งหมด · **grep ก่อนจอง: `GT-080` = 0 hit ทั้งสองไฟล์** ⇒ **ใบนี้คือ `GT-080`** · **เลขว่างถัดไป = 081**
> 🔴 **ใบ `GT-072` · `GT-074` · `GT-076` · `GT-078` · `GT-079` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ** — ใบนี้ **ชี้ไปหา** พวกมัน ไม่ใช่ใบแทนใคร

> 🎯 **MILESTONE:** อยู่ใต้ `M1` "เมืองมีชีวิต" (`CHARTER-01` §③④ · `CHARTER-02` ④)
> 🔴 **ใบนี้ไม่ปิด `M1` และไม่ประกาศ `v1`** — `M1` ปิดด้วยตาเจ้าของบนใบ `GT-078` เท่านั้น · ใบนี้ส่งมอบ **เหตุผลว่าทำไมภาพที่เห็นถึงเป็นอย่างนั้น** ซึ่ง `GT-078` โดยดีไซน์ตอบไม่ได้

---

### 🔴🔴 ใบนี้ต่างจาก `GT-078` และ `GT-076` ตรงไหน — อ่านก่อนตัดสินใจว่าซ้ำ

| ใบ | ถามว่า | ตัวคุม | **ตอบไม่ได้ว่า** |
|---|---|---|---|
| `GT-076` | ไคลเอนต์รับ actor ใน collection เดียวได้กี่ตัว | จำนวนที่ส่ง | คนเห็นกี่ตัว |
| `GT-078` | **เมืองมีคนอยู่จริงไหม** (ตรวจรับ `v1` ด้วยตาเจ้าของ) | ไม่มีแฟล็ก + ทัวร์ | **ทำไมถึงเห็นเท่านั้น** — ทัวร์เดินอิสระ ไม่มีจุดยืนที่รู้ค่าล่วงหน้า ⇒ `seen` ต่ำอ่านได้ทั้ง "ส่งไม่ถึง" และ "ตรงนั้นไม่มีใครอยู่" |
| **`GT-080` (ใบนี้)** | **`seen` ที่ต่ำเป็นของ *จุดยืน* หรือของ *การส่ง*** | **บูตเดียว · สำมะโนเดียว · ยืนสองจุดที่ค่าคาดหมายต่างกันหลายเท่า** | ไคลเอนต์เรนเดอร์ actor ที่ได้รับหรือไม่ (`GT-072`) · เพดานจำนวน (`GT-076`) |

🔴 **ห้ามพ่วง `GT-078` เข้าบูตเดียวกับใบนี้** — ทัวร์อิสระของ `GT-078` ทำลายตัวคุม "ยืนสองจุดที่พินไว้" ของใบนี้ทันที

---

### ที่มาของตัวเลข — **อ่านจากพิน ห้าม re-derive ระหว่างรอบ**

แหล่ง: `pf_bridge\gamedata\scene\bg0001\bg0001.placements.tsv` (149 แถว) · `CONSTDATA_TH__MOBS.tsv` (3,210 แถว) · `pirate-force-server\scenarios\world_scene_density_001.json` (พิน rev.2) · `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` ของ v141 (115 แถว)

🟢 **ตัวคุมที่พังได้แต่ไม่พัง (สามตัว):** XYZ ทั้ง 115 ตรงกันเป๊ะระหว่างสอง decode · **`visual_preset` ของทั้ง 115 เท่ากับ `s_OUTFIT` ของแถว MOBS ที่ `template_id` ชี้ไป (115/115)** — ตัวนี้แข็งที่สุดเพราะค่าเดินทาง *ผ่าน* ตาราง MOBS · และ **`source_name` ไม่ตรงกันเลย 0/115** (ฝั่งหนึ่งเก็บชื่อโชว์ อีกฝั่งเก็บชื่อชุด) ซึ่ง **เป็นสิ่งที่พิสูจน์ว่าไม่ใช่การคัดลอกกัน**

| จุด | พิกัด (x, y, z) | census 115 ใน **500 / 1000 / 2000 / 5000u** |
|---|---|---|
| **A · จุดเกิดจริงที่ `GT-045` วัดด้วยตา 2026-08-23** | `(-8553.947, -2579.689, 186.000)` | **0 / 2 / 3 / 7** |
| A' · `V134_PLAYER_XYZ` (ค่าคงที่ใน v141 · **ไม่ใช่จุดเกิด**) | `(-9239.957, -2780.045, 223.292)` | 1 / 1 / 2 / 7 |
| **B · จุดหนาแน่นที่สุดในฉาก** | `(22124.383, -4912.918, 2746.361)` | **2 / 4 / 12 / 22** |
| B-alt · จุดหนาแน่นที่สุดที่ **เป็น placement จริง** | `(21694.070, -5071.000, 2812.617)` | census 2000u = **12 เท่ากัน** |

🔴🔴 **`A` กับ `A'` ไม่ใช่จุดเดียวกัน ห่างกัน 715.6 หน่วย** — ตำแหน่งล็อกอินมาจาก **แถว `character_positions` ในสำเนา DB** ไม่ใช่จากค่าคงที่ของ v141 ⇒ **`A` คือจุดที่คนจะไปยืนจริง และที่ `A` ไม่มี census สักตัวในรัศมี 500 หน่วย**
🔴 **แต่ค่าที่ใช้ตัดสินรอบนี้คือบรรทัด `WORLD_DENSITY` ที่คอนโซลพิมพ์จากตำแหน่งจริง ณ ขณะนั้น ไม่ใช่ตารางข้างบน** — ตำแหน่งใน DB เคลื่อนได้ทุกครั้งที่มีคนเดิน
- ระยะ A→B: **~31,470 หน่วย (XY)** · **B สูงกว่า A ~2,560 หน่วยในแกน z**
- **การปิดช่องว่าง 34 แถวไม่ช่วยจุดเกิด** — 🔴 **แต่ข้อนี้พิสูจน์ได้เฉพาะ *พิกัดบ้าน* ของ 34 แถวนั้น** · triple ของพวกมันเข้าใกล้กว่านั้น (ใกล้สุด **2,036.9 หน่วย** · **10 จุดอยู่ใน 3000u**) ⇒ **ห้ามอ่านว่า "ปิดช่องว่างแล้วไม่มีอะไรเปลี่ยนที่จุดเกิด"**
- เส้นทางไร้แฟล็กวันนี้ยังส่ง **3 ตัว**: `current/pf_login_game_server_v141.py:1863` `V112_TEST_INDICES=(0,30,91)` ใช้ที่ **`:4292`** (label `V134_P0_P30_P91_ISOLATED_*`)
- 🔴 **`859` = จำนวน XYZ triple ที่ *เขียนไว้ในไฟล์* ไม่ใช่จำนวนจุดเกิด** — พิกัดซ้ำ 3 จุด (distinct = **856**) และ **หลักฐานที่เก็บรอบนี้ชี้ว่า 710 triple เป็นเส้นทางเดิน ไม่ใช่จุดเกิด** (ทั้ง 11 สายเริ่มห่างจากบ้านตัวเอง 6.1–413.8 หน่วย · 7 ใน 11 วนกลับมาบรรจบใน 500 หน่วย) ⇒ **ห้ามพูดว่า "ฉากมีจุดเกิด 859 จุด"**

---

### objective (claim เดียว)

**ในบูตเดียวที่สำมะโนไม่เปลี่ยนเลยแม้แต่ไบต์เดียว จำนวน NPC ที่คนเห็นบนจอเปลี่ยนไปตาม *จุดที่ยืน* อย่างมีนัยที่ตาแยกออก** ⇒ **"ยืนแล้วไม่เห็นใคร" ที่จุดเกิดเป็นคุณสมบัติของแผนที่ ไม่ใช่หลักฐานว่าเซิร์ฟเวอร์ไม่ได้ส่ง**

**ตัวหักล้าง (falsifier) — เขียนก่อนบูต มีสองหน้า:**
> 🔴 (ก) **`seen(B)` ไม่มากกว่า `seen(A)` อย่างที่ตาแยกออก** ทั้งที่ `WORLD_DENSITY` บอกว่า `census_within_2000u` ต่างกันสี่เท่า ⇒ **claim ถูกหักล้าง** ⇒ ส่งต่อ `GT-072`
> 🔴 (ข) **`seen(B) = 0` ทั้งที่ `WORLD_CENSUS assembled=115/115 wire=115 bodies=ok`** ⇒ **ปัญหาอยู่ที่การเรนเดอร์ ไม่ใช่ที่จำนวน** ⇒ **ผลที่แพงที่สุดของรอบ รายงานเสียงดัง ห้ามกลบ**

🔴 **ของที่ *ไม่ใช่* claim ของใบนี้:** เพดานจำนวน (`GT-076`) · ไคลเอนต์วาด actor ที่ได้รับไหม (`GT-072`) · `M1` ถึงหรือยัง (`GT-078`) · **ระยะ cull ของไคลเอนต์ (ยังไม่มีใบไหนในโปรเจกต์ถาม)**

---

### 🔴 สี่เลขที่ห้ามยุบรวมกัน
1. **`sent`** = actor ที่ออกสายจริง — ชั้น (1) · **ต้องเท่ากันเป๊ะที่ A และ B เพราะเป็นบูตเดียวสำมะโนเดียว นี่คือตัวคุมของทั้งใบ**
2. **`density(A)` / `density(B)`** = `census_within_*` จากบรรทัด `WORLD_DENSITY` — **เลขจากตารางฉาก ไม่ใช่จากจอ**
3. **`seen(A)` / `seen(B)`** = คนนับหัวจากจอ — ชั้น (2) เท่านั้น
4. **`seen_max_frame(A)` / `seen_max_frame(B)`** = มากที่สุดในเฟรมเดียว + ชื่อไฟล์เฟรม

🔴 **`seen` น้อยกว่า `density` เป็น *ผล* ไม่ใช่ *ความล้มเหลว*** · 🔴 **ห้ามยกเลขหนึ่งไปตอบแทนอีกเลขในทุกเอกสารต่อจากนี้**

---

### 🔴🔴 PRECONDITION — **BLOCKED-ON-WIRING · ยังบูตไม่ได้ ห้ามบูต**

**สามสิ่งที่การต่อสาย (งานของ chief ไม่ใช่ของผู้เทส) ต้องส่งมอบ:**

1. **เส้นทางไร้แฟล็กส่งสำมะโนเต็ม** — แทน `make_v112_monster_shop_population_state()` (`v141:4292`) ด้วย
   `world_population.build_world_population(legacy, player_xyz, 115, scene_id=1, count_source="full_census")`
   - 🔴 `scene_id` **ไม่มีค่าเริ่มต้นโดยตั้งใจ** — โมดูลปฏิเสธทุกฉากที่ไม่ใช่ 1 ด้วย `ValueError` ⇒ traceback แบบนี้ = **แถว `D6` ไม่ใช่ผลเรื่องไคลเอนต์**
   - 🔴 `player_xyz` ต้องเป็น **ตำแหน่งจริงของผู้เล่น** — `census_order()` เรียงชุดพิน `(0,30,91)` ก่อน แล้วไล่ใกล้-ไกลจากจุดนี้
2. **บรรทัดคอนโซลสองบรรทัด พิมพ์ก่อนเฟรมออกสาย** (ASCII ล้วน cp874-safe):
```
WORLD_CENSUS assembled=115/115 wire=115 bodies=ok pc=<n>B frame=<n>B anchor=(x,y,z) reapply_ms=3000 source=full_census shortfall=none
WORLD_DENSITY scene=bg0001 at=(x,y,z) census_within_500u=<n> 1000u=<n> 2000u=<n> 5000u=<n> 10000u=<n> pin=best_2000u:12 verdict=THIN_VIEW@500u[PROPOSED]
```
   - ตัวสร้าง: `world_population.census_console_line(gen)` · `world_density.m1_console_line(legacy, player_xyz)`
   - 🔴 `bodies=SHORT` หรือ `wire=MISMATCH:` เมื่อไหร่ = **หยุด อย่าบูตต่อ** (stream-tail misalignment ที่ `ErrorData=28317` ตอบพอดี)
   - 🔴 **`verdict` ตัดที่ `census_within_500u < 2` และติดป้าย `[PROPOSED]` มาเอง** — เป็นเกณฑ์ที่สาย A เลือกเอง **ไม่มีหลักฐานฝั่งไคลเอนต์รองรับ** · คาดว่า **A = `THIN_VIEW` · B = `POPULATED_VIEW`** · 🔴 **`verdict` ไม่ใช่คำพิพากษาเรื่องสิ่งที่อยู่บนจอ**
   - 🔴 **`pin=` คือค่าที่อ่านจากพิน ส่วนเลขอื่นบนบรรทัดคำนวณสด** — ป้ายนี้มีไว้ให้แยกสองชั้นออกจากกัน **ห้ามอ่านรวมกัน**
3. **🎯 "density heartbeat" — สิ่งเดียวที่ใบนี้ขอเพิ่มจากที่ `GT-076`/`GT-078` ขอไว้แล้ว:** พิมพ์ `WORLD_DENSITY` **ซ้ำทุกครั้งที่ผู้เล่นขยับเกิน 1000 หน่วยจากจุดที่พิมพ์ครั้งก่อน** (ตัวกระตุ้น = `TargetPosVital` ขาเข้า · **ไม่ส่งไบต์ใหม่ออกสายแม้แต่ไบต์เดียว**)
   - **เหตุผลเป็นเรื่องหลักฐานล้วน:** ถ้าพิมพ์ครั้งเดียวตอน dispatch จะไม่มีบรรทัดชั้น (1) ที่จุด B เลย และการเทียบ A↔B จะเหลือแค่คำพูดของคนหน้าจอ
   - 🟢 **ถ้า chief ให้ heartbeat ไม่ได้:** ใบยังรันได้แต่ **กลายเป็นสองบูต** และ **ตัวคุมอ่อนลงหนึ่งชั้น จดลงผลทุกครั้ง**
4. **คนที่ต่อสายเสร็จ กลับมาเติม "server args" ให้เป็นสตริงจริง แล้วพลิกสถานะเป็น `PENDING`** — 🔴 **ผู้เทสห้ามเดาแฟล็กเอง ห้ามหาคอมมิตเอง**

🔴 **LANE-A แตะ `runtime.py` / `app.py` / `pf_login_game_server_v141.py` ไม่ได้** (`CHARTER-02` §⑥) · และ v141 มี `v141Guard` ⇒ แก้ตรง ๆ **PR แดงที่เกต**
🔴 **"เครื่องมือชนะใบเสมอ"** — เครื่องมือบอกว่าบูตไม่ได้ ให้เชื่อเครื่องมือ แล้วจดความขัดแย้งลงผล

---

### 🔴🔴 ทางไป B — **ยังไม่มีใครรู้ว่าเดินไปถึงได้จริงไหม · เลือกทางไหนต้องจดลงใบ**

| ทาง | ทำอย่างไร | พิสูจน์อะไรเพิ่ม | ราคา / ความเสี่ยง |
|---|---|---|---|
| **(ก) เดินเอง** | `W/A/S/D` จาก A ไป B · จด HUD X/Y ทุก ~5000 หน่วย | 🟢 **แข็งที่สุด** — ได้ทั้งสองจุดในบูตเดียวตามดีไซน์ และพิสูจน์ว่าไปยืนได้จริง | ~31,470 หน่วย · **ไม่มีใครเคยวัดว่ากี่นาที** · 🔴 **ห้ามเดินลงน้ำ** (`RE-073`) |
| **(ข) เขียนแถวตำแหน่งก่อนล็อกอิน** | `UPDATE character_positions SET x=?,y=?,z=? WHERE character_id=?` **บนสำเนาของรอบ `state\run_gt080b.sqlite3`** แล้วบูตใหม่ | เร็วและแน่นอน | 🔴 **กลายเป็นสองบูต ⇒ สองสำมะโน** · 🔴 **ผลยังไม่มีใครวัด:** `legacy_bridge.start_game` ใส่ `p.x/p.y/p.z` ลง MovementAttr จริง (`legacy_bridge.py:40,52,65`) **แต่เส้นทางไร้แฟล็กยิง `make_login_teleport(1, 0)` เป้าศูนย์ตามหลัง** (`runtime.py:3675`) — **ไม่มีใครรู้ว่าอันไหนชนะ ⇒ HUD X/Y ตอน `T0` คือคำตอบ** |
| **(ค) ย้ายจุด teleport ตอนล็อกอิน** | แก้ `runtime.py:3675` | ตรงที่สุด | 🔴 **ไฟล์ของ chief · กินสล็อตเวอร์ชัน · ต้องขอและรอเกต** ⇒ **ทางสุดท้าย** |

🔴🔴 **ถ้าใช้ (ข) แล้ว HUD ขึ้นค่าจุดเกิดเดิม** ⇒ **teleport เป้าศูนย์ชนะ · ทาง (ข) ใช้ไม่ได้บนบิลด์นี้** ⇒ **นี่คือผลที่มีค่า จดแล้วเปลี่ยนไปทาง (ก) ในบูตถัดไป ห้ามเงียบ**

**🔴 fallback ถ้ายืนที่ B ไม่ได้จริง:** `B` เป็น **extra triple ของ placement 43** (ไม่ใช่พิกัด placement ด้วยซ้ำ) ⇒ พิสูจน์แค่ว่า *ไฟล์ฉากเขียนพิกัดนี้ไว้* **ไม่ได้พิสูจน์ว่ามีพื้นหรือคนไปยืนได้**
- **ถ้าอยากเลือกจุดที่เป็น placement จริง ใช้ `B-alt` `(21694.070, -5071.000, 2812.617)` ซึ่ง census 2000u = 12 เท่ากัน** — 🟢 **ข้อสรุปของใบไม่เปลี่ยนไม่ว่าจะใช้ B หรือ B-alt**
- ตกลงไปเรื่อย ๆ / ลอย / จมน้ำ / ติดกำแพง ⇒ **หยุด ยืนที่จุดไกลสุดที่ยืนได้จริง เรียกว่า `B'`** · จด HUD X/Y/Z และอ่านบรรทัด `WORLD_DENSITY` ของ `B'`
- 🔴 `density(B') < 5` ⇒ **รอบนี้ไม่มีอำนาจแยกแยะ = แถว `D5`** ห้ามอ่านเป็นผลลบ

---

### 🟢 งบเวอร์ชัน — **ศูนย์สล็อตสำหรับผู้เทส**
- ใบนี้ **ไม่แก้โค้ด ไม่แก้ scenario ไม่แก้ mask ไม่แก้ไบต์** — ตรวจของที่ chief ต่อสายมา
- ทาง (ข) แตะ **สำเนา DB ของรอบเท่านั้น** ⇒ ไม่กินสล็อต · 🔴 **ผู้เทสห้ามแก้ ledger และห้ามแก้ `SERVER_VERSIONS.md` เอง**
- 🔴 **ใครคิดจะใส่แฟล็ก "เพื่อให้เห็นเยอะขึ้น" = ทำลาย claim ทั้งใบ** — ตัวคุมคือ *สำมะโนไม่เปลี่ยน* **ห้ามเด็ดขาด**

### 🔴 งบเวลาผู้เทส — **~25-40 นาทีบนจอ**
`T0` → นับที่ A 3 นาที → เดินทาง (**เวลาที่ไม่มีใครรู้**) → นับที่ B 5 นาที → อยู่ครบ ≥10 นาทีจาก `T0`
🔴 **เดินเกิน 20 นาทียังไม่ถึง ⇒ หยุด ประกาศ `B'` แล้วเก็บของให้ครบ** — **รอบที่หมดเวลาระหว่างทางยังเป็นผล ถ้าเก็บครบ**

---

### db (สำเนาเสมอ — **canonical ไม่ถูกเปิดตลอดรอบ**)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-080_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt080.sqlite3
```
- เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง** · `PRAGMA integrity_check;` ทุกสำเนา
- 🔴 **สำเนาใหม่หนึ่งใบต่อหนึ่งบูต ห้ามใช้ไฟล์เดิมซ้ำ** · บูตทาง (ข) ใช้ `state\run_gt080b.sqlite3`
- **จดแถวตำแหน่งก่อนบูตทุกครั้ง** (`scene_id, scene_seq, x, y, z, heading` จาก `character_positions`) — 🔴 **ไม่มีบรรทัดนี้ ห้ามเริ่ม** เพราะเป็นตัวเดียวที่บอกว่า "จุด A ของรอบนี้" อยู่ตรงไหนจริง ๆ
- row-diff ต่างได้เฉพาะ `sessions` **+1 แถวต่อการเข้าเกมหนึ่งครั้ง** และ **แถว `character_positions` ของตัวละครที่ใช้** · `max(lease_generation)` **ห้ามถอยหลัง**
- 🔴 **ใบนี้ไม่ใช่ play mode** — 🔴 **ห้ามกด `PLAY_PIRATE_FORCE.bat` ระหว่างรอบ** (ถือ `LOCK_GAME`) · 🔴 **ห้ามเขียนแถวตำแหน่งลง `state\play.sqlite3` เด็ดขาด**

### 🔴 ก่อนบูต — resolve commit เขียว (รันเครื่องมือ ห้ามก๊อป SHA เก่า)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` · **exit 3 ⇒ ห้ามบูต ใบอยู่ BLOCKED ต่อ**
- **ยืนยันหกข้อกับ `<SHA>` ที่จะบูตจริง** (single quote เท่านั้น · 🔴 **ห้าม `| grep` / `awk`** · แปะสิ่งที่คอนโซลพิมพ์ทุกข้อ):
```
git show origin/ci-status:ci/<SHA>.json
git grep -n 'world_population' <SHA> -- src/pirateforce_foundation/runtime.py src/pirateforce_foundation/app.py
git grep -n 'world_density' <SHA> -- src/pirateforce_foundation/runtime.py src/pirateforce_foundation/app.py
git grep -n 'V112_TEST_INDICES' <SHA> -- current/pf_login_game_server_v141.py
git grep -n 'def m1_console_line' <SHA> -- src/pirateforce_foundation/world_density.py
git cat-file -e <SHA>:scenarios/world_scene_density_001.json && echo DENSITY_PIN_PRESENT
```
- 🔴 **ข้อสองและข้อสามคือด่านปลด BLOCKED** — ไม่มี hit ใน `runtime.py`/`app.py` = **ยังไม่ต่อสาย ห้ามบูต จดแล้วรายงาน**
- 🔴 **ข้อสี่กันเข้าใจผิด:** ยังเห็น `V112_TEST_INDICES=(0,30,91)` ถูกใช้ที่ `:4292` **โดยไม่มีเส้นทางใหม่มาแทน** ⇒ บูตนี้จะส่ง 3 ตัว ⇒ **ยังบล็อกอยู่**
- 🟢 **ด่านฟรีที่ทำ headless ได้ก่อนจองเวลาคน:** `pytest tests/test_world_density.py tests/test_world_population.py` — เขียวคือพินยังตรงตารางที่แช่แข็ง · 🔴 **เขียวที่นี่ไม่ได้แปลว่ามีอะไรขึ้นจอ**

### server args (🔴 **ยังเติมไม่ได้จนกว่าจะต่อสาย**)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt080.sqlite3 <CHIEF_FILLS_THIS_IN_AT_WIRING_TIME>
```
- 🔴 **ยังมี `<CHIEF_FILLS...>` อยู่ ⇒ BLOCKED ห้ามบูต ห้ามเดาแฟล็กเอง**
- 🔴 **เป้าหมายคือ "ไม่มี `--*-scenario` แม้แต่ตัวเดียว"** — ถ้ารอบแรกทำได้แค่หลังแฟล็ก **ยังรันได้ แต่จดว่าเป็นเส้นทางมีแฟล็ก และผลนี้ยกไปตอบ `GT-078` ไม่ได้**
- **เก็บ `CommandLine` ของโปรเซสเซิร์ฟเวอร์ทันทีหลังขึ้น วางทั้งบรรทัดลงผล:**
```
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List
```
- **console ต้องไม่มี label ของเลนหัววัดอื่นแม้แต่บรรทัดเดียว** (`HYP_*`) — เห็น = **บูตผิด หยุด**

---

### 🔴 คีย์บอร์ด เมาส์ และสิ่งที่ยิงไบต์

| ท่า | ทำอะไรจริง | ยิง `TargetPosVital` ไหม | ใบนี้ใช้ได้ไหม |
|---|---|---|---|
| **คลิกขวาค้างลากเมาส์** | หมุน **มุมกล้อง** อย่างเดียว | 🟢 ไม่ยิง | ใช้ได้ทุกจังหวะ · **ตัวเช็ค NO-CRASH ตัวเดียวที่ใบนี้ยอมรับ** · **ท่านับหัวหลักของใบ** |
| **`W/A/S/D`** | เดิน | 🔴 ยิง | **ต้องเดิน — การเดินคือเนื้อของใบ** จดเวลาเริ่ม/หยุดทุกช่วง |
| **`Q` / `E`** | **หันตัวละคร** | 🔴 ยิง | ใช้ได้ · 🔴 **ห้ามใช้เป็นตัวเช็ค NO-CRASH เด็ดขาด** |
| **ล้อเมาส์ (ซูม)** | ซูมกล้อง | **[ไม่มีใครเคยวัด]** | 🔴 **ตั้งระดับซูมของ A กับ B ให้เท่ากัน จดเวลาที่ซูมทุกครั้ง** — ซูมต่างกัน = นับหัวเทียบกันไม่ได้ |
| **พิมพ์ตัวอักษร** | — | — | 🔴 **ห้ามพิมพ์อะไรทั้งรอบ** — ตัวอักษรตอนช่องแชตไม่โฟกัส = **ฮอตคีย์** ไม่มีใครรู้ว่าตัวไหนทำอะไร |

🔴 **ประโยคที่ต้องจำ: ตัวที่ยิง `TargetPosVital` คือ "การเปลี่ยนทิศหันของตัวละคร" ไม่ใช่ "การขยับกล้อง"**

### ไทม์ไลน์ — **`T0` = เฟรมแรกที่เข้าแมพสำเร็จ** (HP bar + minimap + ชื่อแมพครบ · ±2 วิ · **วิดีโอคือกรรมการ ห้ามแต่งผล**)

| หน้าต่าง | เวลา | ผู้เทสทำอะไร |
|---|---|---|
| **PRE** | ก่อน `T0` | จดแถวตำแหน่งใน DB · บูตเซิร์ฟเวอร์ · **อ่านและจด `WORLD_CENSUS` + `WORLD_DENSITY` ใบแรกทั้งบรรทัด** · เริ่มอัดวิดีโอ · ล็อกอิน |
| **STAND-A** | `T0` → `+180` | **ยืนนิ่ง** · กวาดกล้อง 4 ทิศด้วยคลิกขวาลาก **ค้างทิศละ 6 วิ ครบสองรอบ** · **นับหัว พูดเลขออกเสียง** · ถ่าย full-res |
| **TRAVEL** | `+180` → `?` | เดินไป B · จด HUD X/Y ทุก ~5000 หน่วย · 🔴 **จดเวลาที่บรรทัด `WORLD_DENSITY` ใหม่โผล่ทุกครั้ง** |
| **STAND-B** | ถึง B/`B'` → `+300` | ยืนนิ่ง · **ท่าเดียวกันเป๊ะกับ STAND-A** · นับหัว · ถ่าย full-res |
| **HOLD** | ถึง **`+600` จาก `T0`** เป็นอย่างน้อย | อยู่ให้ครบ 10 นาที · เฝ้าดูหลุด/ค้าง |
| **POST** | หลัง `+600` | เช็ค NO-CRASH ที่นาที 2/5/10 · ออก |

---

### steps (ห้ามเปลี่ยนลำดับ)

**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด **boot stamp (+07:00)** · preflight จอว่าง (เจอหน้าต่าง elevated = ABORT ทั้งรอบ) · เทียบ sha canonical · copy DB ตามบล็อก db
**เตรียม teardown:** ก๊อปจาก **`TEMPLATE_teardown_generic.ps1`** เป็นหลัก · ถ้าก๊อปจากจ็อบที่เป็นตัวเลข **ต้องเปิดดูบรรทัดที่ 17 ให้เห็น `-replace '\\','/'` ก่อนเสมอ** · 🔴 **ห้ามก๊อปจาก `1103`/`1105`**

1. **จด boot stamp (+07:00)** — teardown ปฏิเสธ stamp เก่ากว่า **420 นาที** (`TEMPLATE_teardown_generic.ps1:135` · **เลข 180 ในใบเก่า = stale**)
2. **จดแถวตำแหน่งเดิมของตัวละครจากสำเนา** — 🔴 **นี่คือนิยามของ "จุด A" ในรอบนี้ ไม่มีบรรทัดนี้ ห้ามเริ่ม**
   - ถ้าใช้ **ทาง (ข)**: ทำ `UPDATE` พิกัด B **ตรงนี้** บน `state\run_gt080b.sqlite3` แล้ว **query กลับออกมาแปะเป็นใบเสร็จ** ก่อนบูต
3. **สตาร์ตเซิร์ฟเวอร์ก่อน แล้วค่อยบูต client เสมอ** (พอร์ต 10188/10189 established = 0 ก่อนเปิด client)
   - 🔴 client ที่บูตโดยไม่มีเซิร์ฟเวอร์ **ตายเองใน ~3.5 นาที** · 🔴 **ฆ่า client กลางคัน ⇒ ต้อง restart server ก่อนเปิดตัวใหม่เสมอ** (ไม่งั้น client ตัวถัดไปค้างที่ `"connecting"` ตลอดกาล — **สงสัย session ค้างก่อน อย่ารีบโทษเลนประชากร**)
   - 🔴 **ตลอดรอบห้ามคลิก console**
4. **อ่านคอนโซล: `WORLD_CENSUS ...` และ `WORLD_DENSITY ...` — จดทั้งบรรทัดทั้งคู่**
   - 🔴 ไม่มี `WORLD_CENSUS` = **ยังไม่ต่อสาย หยุด `D7`** · `bodies=SHORT` / `wire=MISMATCH:` = **หยุดทันที `D6`**
   - 🔴 ไม่ใช่ `115/115` **ห้ามเดินต่อเงียบ ๆ** — บรรทัดบอกเหตุผลมาเอง **จดเลขจริงและเหตุผลลงผล**
5. **เริ่มอัดวิดีโอต่อเนื่องตั้งแต่ก่อนกดเข้าเกมจนจบ session** (`-FrameRate 30` ลง `evidence_video\`) · จด `VIDEO START pid= start= fps= path=` (🔴 `start=` **ห้ามใช้เป็นสมอเวลา**) · 🔴 **ไม่ได้อัด = NO-RESULT ทันที**
6. เปิด client → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร → **เลือกช่องแรก** → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (🔴 **ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด**) · **จดเวลาทุกขั้น**
7. **`T0`** — พูดออกเสียงว่า "T0" · จดเวลานาฬิกาจริง (+07:00) และ `t` ของวิดีโอ
8. 🎯 **STAND-A — ยืนนิ่ง ห้ามแตะคีย์บอร์ด:**
   - **จด HUD X/Y/Z ทันที** แล้ว **เทียบกับแถว DB ที่จดไว้ข้อ 2** — ตรง/ไม่ตรง **เขียนออกมาเป็นตัวอักษร**
   - **ตั้งระดับซูมแล้วจดค่า** — 🔴 **ต้องใช้เหมือนกันเป๊ะที่ B**
   - **คลิกขวาค้างลากกวาดกล้องรอบตัว ค้างทุก ~90 องศา ทิศละ 6 วินาที ครบสองรอบ** (A-N / A-E / A-S / A-W)
   - **นับ NPC ที่เห็นต่อมุม พูดเลขออกเสียง** · 🔴 **นับหัวที่ *เห็น* เท่านั้น · วิธีตัดตัวซ้ำต้องเขียนลงผลเป็นภาษาคน**
   - **ถ่ายภาพนิ่ง full-res ด้วยเครื่องมือนอกเกม ≥ 2 ใบ** → `evidence_screens\GT080_A_<มุม>_FULLRES_<yyyyMMdd_HHmmss>.png` · 🔴 **ห้ามกดคีย์ในหน้าต่างเกมเพื่อถ่ายภาพ · ห้าม resize ลง**
   - 🔴🔴 **เห็น 0-3 ตัวที่นี่ = ผลที่คาดไว้ ไม่ใช่ความล้มเหลว และไม่ใช่เหตุให้ไปแก้อะไรกลางรอบ** — นี่คือหัวใจของใบทั้งใบ
9. **TRAVEL:** จด **HUD X/Y ทุก ~5000 หน่วย** พร้อมเวลาวิดีโอ · จดเวลาที่ **บรรทัด `WORLD_DENSITY` ใหม่โผล่ทุกครั้ง** · 🔴 **ห้ามเดินลงน้ำ** · เจอกำแพง/หน้าผาให้อ้อมแล้ว **จดว่าอ้อมที่ไหน** · 🔴 **เกิน 20 นาที ⇒ ประกาศ `B'` แล้วไปข้อ 10**
10. 🎯 **STAND-B (หรือ `B'`) — ทำเหมือนข้อ 8 ทุกตัวอักษร** · ไฟล์ภาพ → `evidence_screens\GT080_B_<มุม>_FULLRES_<...>.png` · **จดบรรทัด `WORLD_DENSITY` ของจุดนี้ทั้งบรรทัด** — 🔴 **ไม่มีบรรทัดนี้ ⇒ ชั้น (1) ที่ B ว่าง ⇒ แถว `D5`**
11. **HOLD:** อยู่ในเกมจนครบ **10 นาทีจาก `T0`** · จดเวลาจริงตอนครบ
12. **NO-CRASH / CRASH:** **คลิกขวาค้างลากแล้วกล้องหมุน = NO-CRASH** — เช็คที่นาที **2 / 5 / 10 จดผลแยกสามบรรทัด** · 🔴 **ห้ามใช้ `Q`/`E`**
13. ออกจากเกม: **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย → **หยุดวิดีโอ** → **ปิดเซิร์ฟเวอร์ด้วย**
14. เก็บ **raw GAME log ทั้งไฟล์** + console out/err ทั้งหมด (ทุกบรรทัด `[G>]` / `PF-EVENT` / `ErrorData` / `WORLD_*`) → `PRAGMA integrity_check;` ทุกสำเนา → sha256 ทุกไฟล์
15. **teardown เสมอ — แม้รอบจบเพราะเลิกเล่น** → เทียบ sha canonical กับ `CANON_SHA.txt` อีกครั้ง
16. **หลังรอบ — แตกเฟรม (🔴 ห้ามมี `scale=` ในบรรทัดคำสั่งเด็ดขาด):**
```
ffmpeg -ss <t ของ STAND-A> -i $mkv -t 60.00 -vsync 0 GT080_A_%03d.png
ffmpeg -ss <t ของ STAND-B> -i $mkv -t 60.00 -vsync 0 GT080_B_%03d.png
```
    - 🔴 **รายงานช่วงที่กล้อง *นิ่งจริง* ของแต่ละมุมเป็น `[t_เริ่ม, t_จบ]` และจำนวนเฟรม** — **สั้นกว่า 4.0 วิ ⇒ มุมนั้น "นับไม่ได้" เขียนออกมาเป็นตัวอักษร ห้ามฝืนนับ**
17. 🔴🔴 **`G-FRAME` — บังคับกับ *ทุกเฟรมที่ถูกยกมาอ้าง*:**
```
FRAME: <ชื่อไฟล์>  t=+<วินาที> จาก T0=<YYYY-MM-DDTHH:MM:SS+07:00>  dist=<หน่วยเกม> ถึง <สิ่งที่พูดถึง>
```
    - **`t` ต้องเป็นตัวเลขจริง ห้าม `~` ห้าม `x`** · วัด `dist` ไม่ได้เขียน **`dist=unmeasured`** 🔴 **ห้ามเว้นว่าง ห้ามเขียนว่า "ใกล้"**
    - บรรทัด **`UNMEASURED_DIST: <n>/<ทั้งหมด>`** ในจดหมายผล · **เกินครึ่ง = chief ไม่บริโภคเป็นผลปิดใบ**
18. 🔴🔴 **`G-OBS` — ขั้นสุดท้าย บังคับ:** ผู้ช่วยทวน "สิ่งที่ผู้ช่วยเห็น" ให้ผู้เทสยืนยันทีละข้อ (จำนวนที่ A ต่อมุม · ที่ B ต่อมุม · เดินทางไปทางไหน · ถึง B หรือ `B'` · หลุด/ไม่หลุด · **สีป้ายทุกป้าย**) · ตอบคำเดียวต่อข้อ: **"ตรง" / "ไม่ตรง" / "ฉันไม่ได้ดูข้อนั้น"**
    - จดหมายผลต้องมีบรรทัดนี้ตัวอักษรเป๊ะ: `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`
    - 🔴 **ยังไม่ยืนยัน = ห้ามเขียนผลลงคิว** · 🔴 **บรรทัดนี้เป็น "ขั้นตอน" ไม่ใช่ "หลักฐาน"**

---

### คำทำนาย (**คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว**)

- **P1 [wire]** `WORLD_CENSUS assembled=115/115 wire=115 bodies=ok` **หนึ่งบรรทัด และไม่เปลี่ยนอีกเลยทั้งรอบ**
- **P2 [wire]** `WORLD_DENSITY` ที่ A ได้ `census_within_500u` = **0-1** และ `verdict=THIN_VIEW` · ที่ B ได้ `census_within_2000u` **10-12** และ `verdict=POPULATED_VIEW`
  - 🔴 **A ของรอบนี้อาจไม่ใช่พิกัดในตาราง** เพราะตำแหน่งมาจากแถว DB ⇒ **บรรทัดที่คอนโซลพิมพ์คือกรรมการ ไม่ใช่ตารางในใบ**
- **P3 [ข้อหลัก · ชั้น 2]** `seen(A)` = **0-3** · `seen(B)` = **มากกว่านั้นอย่างชัดเจนจนตาแยกออกโดยไม่ต้องนับละเอียด**
- **P4 [ค่าที่ไม่มีใครรู้ · คาดว่าจะ "ผิดแบบมีประโยชน์" ที่สุด]** `seen(B)` **น้อยกว่า** `density(B)` — ระยะ cull/มุม/LOD ยังไม่มีใครวัด
- **P5 [ไม่มีใครรู้]** เดินจาก A ถึง B ได้จริงในไม่เกิน 20 นาที — **ผิดเมื่อไหร่ให้ประกาศ `B'` ไม่ใช่ล้มใบ**
- **P6 [จดสีอย่างเดียว ห้ามสรุปสาเหตุ]** ป้ายชื่อ NPC เป็น **เหลือง**
- **P7 [ถ้าผิดคือเรื่องใหญ่ที่สุดของรอบ]** ไม่ crash ไม่หลุด ตอนส่ง 115 ตัวแล้วเดินข้ามแมพ — **ถ้าค้าง/หลุด นั่นคือเพดานที่วัดได้ รายงานเสียงดัง**

---

### pass criteria — **สองชั้น 🔴 ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

**ชั้น (1) wire/DB — headless ได้**
1. `BOOT_COMMIT` + ผลด่านก่อนบูตหกข้อทีละข้อ (**แปะสิ่งที่คอนโซลพิมพ์**)
2. **`CommandLine` ของโปรเซสเซิร์ฟเวอร์ทั้งบรรทัด** + console ไม่มี label เลนหัววัดอื่น
3. 🎯 **ตัวคุมของทั้งใบ: `WORLD_CENSUS` เป็น `assembled=115/115 wire=115 bodies=ok` และ *ไม่เปลี่ยน* ระหว่าง STAND-A กับ STAND-B** — รายงาน `pc=`/`frame=` เป็นตัวเลข
   - 🔴 **ถ้าเป็นสองบูตตามทาง (ข):** `assembled`/`wire`/`bodies`/`pc=`/`frame=` **ต้องเท่ากันทั้งสองบูต** · **แต่ `frame_sha256` ต่างได้โดยชอบธรรม** เพราะ `census_order()` เรียงใกล้-ไกลจาก anchor ⇒ **สมาชิกชุดเดียวกัน ลำดับต่างกัน** · 🔴 **sha ต่าง ≠ สัญญาณเตือน · `frame=` ต่าง = สัญญาณเตือน**
4. **บรรทัด `WORLD_DENSITY` อย่างน้อยสองใบ ตัวอักษรเป๊ะทั้งบรรทัด** — ใบหนึ่งที่ A ใบหนึ่งที่ B/`B'` · `at=` สอดคล้องกับ HUD ที่จดไว้
5. **`sent`** = census บรรทัด `[G>]` **ทั้งไฟล์ ไม่กรองอะไรออก**
6. **หลักฐานว่าเดินจริง:** `TargetPosVital` วิ่งตลอดช่วง TRAVEL · **จำนวนในช่วง STAND-A และ STAND-B ควรเป็น `0`** — **ไม่เป็น 0 ⇒ จุดยืนของภาพชุดนั้นไม่นิ่ง จดแล้วตัดออกจากการเทียบ**
7. **session ต่อเนื่อง ≥ 10 นาที:** ไม่มี reconnect · ไม่มี GAME connection ที่สอง
8. ไม่มี traceback · stderr 0 B · **ไม่มี `ErrorData=28317`** (มี = จดว่าโผล่หลังอะไร กี่วินาทีหลัง `T0`)
9. DB สำเนา: `integrity_check` = `ok` · row-diff ตามที่ระบุ · `max(lease_generation)` **ไม่ถอยหลัง** · **sha256 canonical ก่อน-หลัง = `CANON_SHA.txt`**
10. **ความครบของวิดีโอ:** `ffprobe` → เฟรมจริงเทียบ `duration x fps` · **รายงานเฟรมที่หายเป็นตัวเลข**
11. 🔴🔴 **ชั้นนี้ตอบไม่ได้:** `assembled=115/115` **ไม่ใช่หลักฐานว่ามีอะไรขึ้นจอแม้แต่ตัวเดียว** · **`WORLD_DENSITY` เป็นเลขจากตารางฉาก ไม่ใช่จากจอ** · **claim ของใบปิดด้วยชั้นนี้ไม่ได้เด็ดขาด**

**ชั้น (2) client-observable — 🔴 ตัวปิดใบอยู่ชั้นนี้ชั้นเดียว**
1. **หลักฐานบังคับ:** วิดีโอต่อเนื่องคลุมตั้งแต่ก่อนกดเข้าเกมจนออก · ภาพนิ่ง full-res **≥ 4 ใบ (A ≥2 · B ≥2)** · **sha256 ทุกไฟล์** · **ทุกเฟรมที่อ้างมี `FRAME:`** + **`UNMEASURED_DIST:`**
2. 🎯 **เลขหลัก — ตอบเป็นตัวเลขจริง ห้ามตอบเป็นคำ:** `seen(A)` ต่อมุม (4 มุม) + `seen_max_frame(A)` · `seen(B)` ต่อมุม + `seen_max_frame(B)` · **วิธีนับและวิธีตัดตัวซ้ำเป็นภาษาคน**
3. 🎯 **คำตัดสินหลัก — หนึ่งประโยค:** *"ที่ A นับได้ `<n>` · ที่ B นับได้ `<m>` · ระหว่างสองจุดนี้ `WORLD_CENSUS` ไม่เปลี่ยน"*
4. **เงื่อนไขที่ทำให้จุดหนึ่ง "นับได้" — ครบทุกข้อ มิฉะนั้นเป็น "นับไม่ได้" ไม่ใช่ "ไม่เห็น":** (ก) ช่วงกล้องนิ่ง **≥ 4.0 วินาที** (ข) **ระดับซูมเท่ากับอีกจุด** (ค) **HUD X/Y/Z ถูกจดและตรงกับ `at=`** (ง) **`TargetPosVital` ในช่วงนับ = 0**
5. **ตารางต่อ (จุด x มุม):** จุด · มุม · `t` · HUD X/Y/Z · ระดับซูม · ช่วงกล้องนิ่ง + จำนวนเฟรม · จำนวนที่นับได้ · ของบัง · ไฟล์ภาพ
6. **เดินทาง:** ทางไหน (ก/ข/ค) · ถึง B หรือ `B'` · **เวลาเป็นตัวเลข** · จุดที่ต้องอ้อมและเหตุผล
7. **ตารางสีป้ายชื่อครบทุกป้ายทุกภาพ full-res** (PLAYBOOK ข้อ 13)
8. **NO-CRASH / CRASH verdict** (คลิกขวาลากเท่านั้น · นาที 2/5/10 แยกสามบรรทัด)
9. 🔴 **ใบปิดด้วยผลลบได้เฉพาะรอบที่ *คุณ Panya เห็นเอง* + มีวิดีโอต่อเนื่อง** (`AGENTS.md` §9)
10. 🔴 **ชั้นนี้ตอบไม่ได้:** เซิร์ฟเวอร์ส่งไปกี่ตัว · บูตมีแฟล็กหรือไม่ · `density` ของจุดที่ยืน · ทำไม `seen` ไม่เท่า `density`

🔴 **ชั้น (1) ไม่ผ่าน ⇒ NO-RESULT ทางเทคนิค ห้ามอ่านจอเป็นผลใด ๆ แม้จะเห็นชัด ๆ**

---

### ตารางผลลัพธ์ที่มีชื่อ — **ทุกทางออกอ่านได้**

| # | สิ่งที่เห็น | คำตัดสิน | อนุญาตให้สรุปว่า | 🔴 **ไม่** อนุญาต / redirect |
|---|---|---|---|---|
| **D1** POSITION-EXPLAINS-IT 🎯 | `seen(A)` = 0-3 · `seen(B)` มากกว่าอย่างที่ตาแยกออก · `WORLD_CENSUS` ไม่เปลี่ยน | **PASS** | ว่า **"ยืนแล้วไม่เห็นใคร" ที่จุดเกิดเป็นคุณสมบัติของแผนที่ ไม่ใช่ของการส่ง** ⇒ ทุกใบตรวจรับประชากรต่อจากนี้ต้องระบุ **จุดยืน** | ห้ามเขียนว่า "ไคลเอนต์รับ 115 ได้" (`GT-076`) · ห้ามเขียนว่า `M1` ถึง (`GT-078`) · ห้ามตั้ง `seen(B)` เป็นเพดานอะไร |
| **D2** POSITION-EXPLAINS-IT-WITH-CAP | `seen(B) > seen(A)` ชัดเจน **แต่ `seen(B)` น้อยกว่า `density(B)` มาก** | **PASS** + **finding ใหญ่** | ว่า claim ยืน **และ** ที่มุม/ระยะ/ซูมชุดนี้ นับได้ `seen_max_frame(B)` ตัว | **ห้ามเรียกว่า "ระยะ cull"** — ไม่มีตัวคุมเรื่องระยะเลย · **redirect: เปิดใบวัดระยะ cull เป็นใบของตัวเอง** |
| **D3** SEND-REACHES-NOBODY 🔴🎯 | `assembled=115/115 wire=115 bodies=ok` **แต่ `seen(B) = 0`** | **PASS — ผลที่แพงที่สุดของรอบ** | ว่า **ปัญหาอยู่ที่การเรนเดอร์ ไม่ใช่ที่จำนวน** | **ห้ามชี้กลไก** (ช่อง actor / id ชน / LOD / ลำดับใน list — **ไม่มีหลักฐาน static แม้แต่บรรทัดเดียว**) · **redirect: `GT-072` ทันที** |
| **D4** CLAIM-FALSIFIED 🔴 | `seen(B)` ไม่ต่างจาก `seen(A)` อย่างที่ตาแยกออก ทั้งที่ `density` ต่างสี่เท่า | **ผลลบที่สะอาด · มีค่าเท่าผลบวก · ไม่ใช่ FAIL** | ว่า **จุดยืนอธิบายภาพที่เห็นไม่ได้ในรอบนี้** | ห้ามเขียนว่า "ตารางฉากผิด" (115/115 XYZ + 115/115 preset ตรงกันสองการถอด) · **redirect: `GT-072` + ใบระยะ cull** |
| **D5** UNDERPOWERED | ยืน B ไม่ได้และ `density(B') < 5` · มุมค้างไม่ครบ 4 วิ · ซูมไม่เท่ากัน | **PARTIAL** | เฉพาะสิ่งที่นับได้ที่จุดที่นับได้ | **ห้ามอ่านการเทียบเป็นผล** · 🔴 **ใบยังเปิด ห้าม archive** · **redirect: รันซ้ำ commit เดิม เปลี่ยนทางไป B (ก↔ข) หรือใช้ `B-alt`** |
| **D6** SERVER-SIDE-REFUSAL 🔴 | `ValueError`/traceback ก่อนมีไบต์ออกสาย · `bodies=SHORT` · `wire=MISMATCH:` | **NO-RESULT** | ไม่มี | ห้ามอ่านเป็นการปฏิเสธของไคลเอนต์ · **redirect: ส่ง chief · ใบกลับเป็น BLOCKED ห้าม archive** |
| **D7** NON-OBSERVED | ไม่มี `WORLD_CENSUS`/`WORLD_DENSITY` · ไม่ได้อัดวิดีโอ · `T0` หาไม่เจอ · DB ซ้ำ · เห็น label เลนอื่น | **NO-RESULT — ไม่ใช่ผลลบ** | ไม่มี | **redirect: รันซ้ำ commit เดิม** · 🔴 **ห้าม archive ใบ** |
| **D8** CRASH / DISCONNECT | หลุด/ค้างก่อน `+600` | ผลที่มีชื่อ **และอาจเป็นเพดานที่วัดได้** | จดว่าหลุดที่ `t` เท่าไร · ตอนไหน · `sent` เท่าไรตอนนั้น | ห้ามชี้สาเหตุ · **ห้ามลดเลข 115 เองเพื่อให้ผ่าน** (ต้องเป็นคำสั่ง COO และเป็นใบใหม่) · **restart server ก่อนบูตถัดไป** |

### ผลลบของรอบนี้จะ redirect ไปไหน — เขียนก่อนบูตตามกติกา
> - `D3` ⇒ **`GT-072` กลายเป็นคอขวดของ `M1` ทั้งก้อน** ⇒ ส่ง chief ตัดสินลำดับใบทันที
> - `D4` ⇒ คำถามใหม่ทั้งใบ: **ไคลเอนต์ตัดสินใจวาดอะไรจากระยะเท่าไร** ⇒ เปิดใบวัดระยะ cull · **ห้ามแตะโค้ดจนกว่าจะมีใบนั้น**
> - `D5` + ยืน B ไม่ได้ ⇒ **ข้อมูลใหม่เรื่องภูมิประเทศของ `bg0001`** ⇒ สาย A เลือกจุดหนาแน่นอันดับถัดไปที่ *เดินถึงได้* แล้วแก้พิน (**เป็นใบใหม่ ไม่ใช่การแก้ใบนี้เงียบ ๆ**)
> - `D6` ⇒ กลับ chief · **ตรวจได้ headless ไม่ต้องใช้รอบ attended อีกรอบ**

---

### PLAYBOOK ข้อ 13 — บันทึกสีของ **ทุกป้ายชื่อในเฟรม** (คำสั่งคุณ Panya 2026-08-25 · บังคับทุกใบ attended ตั้งแต่ R163)
- **จดอะไร:** ชื่อตัวเราเอง (เหนือหัว + แผง UI ซ้ายบน) · ชื่อ NPC/actor ทุกตัวในเฟรม · ชื่อไอเทมบนพื้น · ชื่อผู้เล่นคนอื่น · บรรทัด title/คำอธิบาย · ชื่อแมพบน HUD/มินิแมพ — **หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ**
- **ไม่มีให้เขียนคำว่า "ไม่มี" ออกมาเป็นตัวอักษร** 🔴 **ห้ามเว้นว่าง**
- **อ่านสีจากภาพนิ่งความละเอียดเต็ม / crop PNG เท่านั้น** 🔴 **ห้ามอ่านจาก contact sheet · ห้ามภาพย่อ · ห้ามจากวิดีโอ** · **sha256 ทุกไฟล์**
- 🆕 **ที่จุด B ป้ายจะเยอะกว่าที่ A โดยดีไซน์** ⇒ จดครบเท่าที่ **อ่านออก** แล้วเขียนตัวเลขว่า **"อ่านไม่ออก/ถูกบัง N ป้าย"** 🔴 **ห้ามข้ามเงียบ ๆ ห้ามเดาสีของป้ายที่อ่านไม่ออก**
- **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับ:** NPC = **เหลือง** · ผู้เล่น = **เขียว** · ไอเทมบนพื้น = **ขาว** · title/คำอธิบาย = **ฟ้า** · ชื่อตัวเอง = **ขาว**
- 🔴🔴 **ผู้เทสจด "สี" อย่างเดียว ห้ามสรุปสาเหตุ** — **อะไรตัดสินสีของป้ายคือคำถามของ `RE-067`** ⇒ **ห้ามเขียนว่า "แปลว่าไคลเอนต์จัดมันเป็นผู้เล่น/NPC/ศัตรู"**
- **`REAL_SERVER_DIVERGENCE.tsv`: 🔴 ส่งค่ากลับมาในจดหมายผล ห้ามแก้ไฟล์เองจากหน้าสะพาน** · หนึ่งแถวต่อหนึ่งป้ายที่เทียบ (คั่นด้วย **TAB**) · `evidence_layer` = **`eye`** เสมอ · `open_ticket` = **`RE-067`** · `blocks_promotion` = `no` · **เติมแถวแม้ผลจะ "ตรงกัน"**

### ⛔ เกณฑ์หยุดทั้งเลนทันที
- ชื่อ probe ใด ๆ (`ProbePlayer01` / `ProbeControl03`) โผล่ที่ไหนก็ตาม ⇒ **บูตไม่สะอาด หยุด เก็บ console ทั้งไฟล์**
- `ErrorData=28317` ⇒ **หยุด จดว่าโผล่หลังอะไร กี่วินาทีหลัง `T0`**
- `WORLD_CENSUS` ขึ้น `bodies=SHORT` หรือ `wire=MISMATCH:` ⇒ **หยุด (`D6`)**
- คอนโซลขึ้น label ของเลน scenario/hypothesis อื่น ⇒ **บูตผิดไฟล์ หยุด**
- ตัวละครเริ่มตกลงเรื่อย ๆ / จมน้ำ ⇒ **หยุดเดิน จดพิกัด แล้วใช้ fallback `B'`**

### teardown + ใบเสร็จ (บังคับ — **แม้รอบจบเพราะคนเลิกเล่น**)
- **teardown เสมอ ภายใน 420 นาทีจาก boot stamp** — เกินเพดาน **ปฏิเสธ exit 12 โดยดีไซน์**
- แท่นที่ถูกทิ้งข้ามชั่วโมง: **อย่าฝืน template** ⇒ `staged\TOOL_stop_stale_server.ps1` แล้วตามด้วย receipt อ่านอย่างเดียว
- ได้ **exit 36** อย่าเดาเอง — แนบบรรทัดที่ 17 ของไฟล์ teardown ที่ใช้จริงมาทั้งบรรทัด
- **ใบเสร็จที่ต้องแนบ:** `AFTER listeners = 0` · **canonical guard: sha256 ก่อน-หลัง = `CANON_SHA.txt`** · **teardown exit code** · `LOCK_GAME` ปล่อยแล้ว · run copy `state\run_gt080*.sqlite3` **เก็บไว้ให้ chief re-derive ห้ามทิ้ง** · path ของ raw GAME log + console + วิดีโอ + ภาพทุกไฟล์ พร้อม **sha256**
- 🔴 **ถ้าใช้ทาง (ข):** แนบ **query แถว `character_positions` ก่อนบูตและหลังจบ** เป็นใบเสร็จ · 🔴 **ห้ามแตะ `state\play.sqlite3` และห้ามแตะ canonical**
- 🔴 **บนสะพานเท่านั้น ห้ามลบ:** ไฟล์ `.mkv` ต้นฉบับ และโฟลเดอร์ capture ของรอบ
- 🔴 **restart เซิร์ฟเวอร์ก่อนบูตรอบถัดไปเสมอ**

### `BUILD_IMPACT` (กฎ `BUILD-003` · บังคับก่อนถือว่าปิดใบ)
```
BUILD_IMPACT: ถ้า D1/D2 -> "จุดยืน" กลายเป็นฟิลด์บังคับของทุกใบตรวจรับประชากรตั้งแต่ M2 เป็นต้นไป
                          + seen(B) เป็นตัวเลขตั้งต้นของงบประชากรต่อฉากใน M2-M6
              ถ้า D3     -> BUILD_IMPACT คือ "ไม่มี" + ชั้นที่พัง (sent ถึง แต่ไม่ถูกวาด) -> GT-072 ขึ้นเป็นคอขวด
              ถ้า D4     -> BUILD_IMPACT คือ "ไม่มี" + เปิดใบระยะ cull ก่อนสร้างอะไรต่อ
```

---

### nonclaims (ติดไปกับผลทุกกรณี — **ห้ามตัดทิ้ง**)

① 🔴🔴 **ตัวเลข 3 และ 12 คือ *จำนวน placement ในรัศมี* ไม่ใช่จำนวนตัวที่ไคลเอนต์จะเรนเดอร์** — ระหว่างทางมีอย่างน้อยสามด่านที่ไม่มีใครวัด: เซิร์ฟเวอร์เลือกส่ง · ไคลเอนต์รับ · ไคลเอนต์วาด
② 🔴🔴 **ระยะทั้งหมดเป็นระยะ 3 มิติรวมแกน z** — **ถ้าไคลเอนต์คัดด้วยระยะ 2 มิติ ตัวเลขจะต่างไป และไม่มีใครวัดว่ามันคัดด้วยอะไร** · ที่ B สำคัญเป็นพิเศษเพราะ z สูงกว่า A ~2,560 หน่วย · **(สำหรับ census 115 วัดแล้วว่า 2D กับ 3D ให้เลขเท่ากันทุกรัศมี — ข้อนี้จึงเป็นเรื่องของฝั่งไคลเอนต์ล้วน)**
③ **พิกัด B เป็น extra triple ของ placement 43 ไม่ใช่พิกัด placement** ⇒ พิสูจน์แค่ว่า **ไฟล์ฉากเขียนพิกัดนี้ไว้** · **ไม่ได้พิสูจน์ว่ามีพื้น หรือคนไปยืนได้** · **`B-alt` เป็นพิกัด placement จริงและได้ census เท่ากัน**
④ **ตัวเลขของ A ในตารางวัดที่พิกัดที่ `GT-045` เคยวัดไว้ ไม่ใช่ที่จุดเกิดของบูตนี้** — ตำแหน่งมาจากแถว DB ซึ่งเคลื่อนได้ ⇒ **ค่าที่ใช้ตัดสินคือบรรทัด `WORLD_DENSITY` ของรอบนั้นเท่านั้น**
⑤ **ไม่ตอบระยะ cull ของไคลเอนต์แม้แต่นิดเดียว** — ไม่มีตัวคุมเรื่องระยะ มุมกล้อง ซูม LOD · **ยังไม่มีใบไหนในโปรเจกต์ถามข้อนี้** ⇒ `seen` ที่วัดได้ **ห้ามเรียกว่าเพดานหรือระยะ**
⑥ **ไม่พิสูจน์ว่าไคลเอนต์เรนเดอร์ actor ที่ได้รับ** — `GT-072` **ยัง PARTIAL และยังไม่มีค่าไหนถูกตัดออกเลย**
⑦ **ไม่ตอบเพดานจำนวน** (`GT-076`) · **ไม่ปิด `M1` ไม่ประกาศ `v1`** (`GT-078`)
⑧ **`WORLD_DENSITY` เป็นเลขจากตารางฉาก ไม่ใช่จากจอ** · `verdict=` เป็น **การตัดที่ `census_within_500u < 2` ซึ่งสาย A เลือกเอง และติดป้าย `[PROPOSED]` มาเอง** ไม่ใช่คำพิพากษาเรื่องภาพ
⑨ **สองจุด สองชุดมุมกล้อง ไม่ใช่ "ทั้งแมพ"** — **อะไรที่อยู่นอกเฟรม = non-observed ไม่ใช่ absent** ⇒ เขียน **"ไม่เห็น"** ห้ามเขียน **"ไม่มี"**
⑩ **รอบเดียวไม่ใช่คุณสมบัติของไคลเอนต์** — เครื่องเดียว แมพเดียว บูตเดียว
⑪ 🔴 **"34 แถวที่ขาดไม่เกี่ยวกับจุดเกิด" พิสูจน์ได้เฉพาะ *พิกัดบ้าน* ของ 34 แถวนั้น** — extra triple ของพวกมันเข้าใกล้กว่า (ใกล้สุด 2,036.9 หน่วย · 10 จุดใน 3000u) ⇒ **ห้ามอ่านเป็น "ปิดช่องว่างแล้วไม่มีอะไรเปลี่ยน"** · การปิดช่องว่างเป็นคำถามของ actor ศัตรู = **งานสาย B**
⑫ 🔴 **`859` = triple ที่เขียนไว้ในไฟล์ ไม่ใช่จำนวนจุดเกิด** (distinct 856) · **หลักฐานที่เก็บรอบนี้ชี้ว่ามันคือเส้นทางเดิน** (11 สายเริ่มห่างบ้านตัวเอง 6.1–413.8 หน่วย · 7 ใน 11 วนกลับมาบรรจบใน 500 หน่วย) · **`CONSTDATA_TH__AI_WANDER.tsv` ยังไม่มีใครอ่าน** ⇒ **ห้ามเขียนว่า "ไม่มีอะไรบอกได้"**
⑬ **สีอ่านด้วยตาจากภาพ ไม่ได้วัดค่าพิกเซล** ⇒ **ไม่ claim ค่า RGB/hex ใด ๆ** · `evidence_layer` = **`eye`** · **ห้ามอนุมานสาเหตุจากสี (`RE-067`)**
⑭ **ภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับอาจเป็น client คนละ build/ภูมิภาค** ⇒ "ต่างจากภาพต้นฉบับ" ยังไม่เท่ากับ "ของเราผิด"
⑮ **ตาราง placement 115 ตัวและการเลือกจุดยืนเป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้วและกู้ไม่ได้ตลอดกาล
⑯ **ไม่มีใครวัดว่าคลิกซ้าย/ล้อเมาส์ยิงไบต์อะไรออกสายหรือไม่**
⑰ **`OBSERVER_CONFIRMED` และ `G-FRAME` เป็นขั้นตอน ไม่ใช่หลักฐาน**
⑱ **การผ่านใบนี้ไม่ปลดใบที่ยังไม่ถูกเทสในคิวนี้แม้แต่ใบเดียว**

---

### ใบนี้ปิดเมื่อไร

- **ปิดเป็น `PASS`** เมื่อได้แถว **`D1` · `D2` · `D3` หรือ `D4`** ครบทั้งสองชั้น **และ** มีบรรทัด `OBSERVER_CONFIRMED:` · **สี่แถวนี้ปิดใบได้เท่ากันหมด — `D3`/`D4` เป็นผลลบที่มีค่าเท่าผลบวก และเป็นทางที่ *เปลี่ยนลำดับงานของโปรเจกต์* มากที่สุด**
- **ใบยังเปิด (ห้าม archive)** เมื่อได้ **`D5` `D6` `D7`** — สามแถวนี้แปลว่า **ยังไม่ได้วัด** ไม่ใช่ **วัดแล้วไม่เจอ**
- **`D8` (CRASH)** ปิดใบไม่ได้ด้วยตัวเอง — เก็บของให้ครบแล้วรันซ้ำ commit เดิม **ห้ามลดเลข 115 เอง**
- 🔴 **ปิดด้วยผลลบได้เฉพาะรอบที่คุณ Panya เห็นเอง + มีวิดีโอต่อเนื่อง** (`AGENTS.md` §9)
- 🔴 **สถานะสุดท้ายของใบ chief เป็นคนตั้ง** — ผู้เทสและผู้ช่วย **กรอกผล ไม่ตั้งสถานะ**

---

- **result:** (ผู้เทสกรอก: ① `BOOT_COMMIT` + ผลด่านก่อนบูตหกข้อทีละข้อ ② **`CommandLine` ของโปรเซสเซิร์ฟเวอร์ทั้งบรรทัด** ③ **บรรทัด `WORLD_CENSUS` เป๊ะทั้งบรรทัด** + ยืนยันว่าไม่เปลี่ยนระหว่าง A กับ B (ถ้าสองบูต: เทียบทีละช่อง และ **บอกว่า `frame_sha256` ต่างหรือไม่ พร้อมคำอธิบายเรื่องลำดับ**) ④ **บรรทัด `WORLD_DENSITY` ทุกใบที่โผล่ เป๊ะทั้งบรรทัด พร้อมเวลา** ⑤ **แถวตำแหน่งใน DB ก่อนบูต** + **HUD X/Y/Z ที่ `T0`** + ตรง/ไม่ตรงกัน ⑥ **ทางไป B ที่เลือก (ก/ข/ค) + เหตุผล + ผล** + เวลาเดินทางเป็นตัวเลข + ถึง `B` / `B-alt` / `B'` (ถ้า `B'` ใส่พิกัดและ `density(B')`) ⑦ **สี่เลขแยกกัน: `sent` · `density(A)`/`density(B)` · `seen(A)`/`seen(B)` · `seen_max_frame`** + วิธีนับและวิธีตัดตัวซ้ำเป็นภาษาคน ⑧ **ตารางต่อ (จุด x มุม)** + **`UNMEASURED_DIST: <n>/<ทั้งหมด>`** ⑨ **ยอด `TargetPosVital` ในช่วง STAND-A และ STAND-B** (คาด `0` ทั้งคู่) + ใบแรก/ใบสุดท้ายของช่วง TRAVEL ⑩ อยู่ครบ ≥10 นาทีไหม (เวลาจริงสองค่า) + NO-CRASH นาที 2/5/10 แยกสามบรรทัด ⑪ **แถวไหนของตารางผล (D1-D8)** ⑫ **ตาราง PLAYBOOK ข้อ 13 ครบทุกป้ายทุกภาพ full-res** ⑬ ค่าที่ต้องเติม `REAL_SERVER_DIVERGENCE.tsv` (**ส่งค่ามา ห้ามแก้ไฟล์เอง**) ⑭ census บรรทัด `[G>]` ทั้งไฟล์ + `ErrorData` ⑮ `ffprobe` เฟรมที่หายเป็นตัวเลข ⑯ path + sha256 ทุกไฟล์ ⑰ เวลา +07:00 · sha canonical ก่อน-หลัง · `integrity_check` · row-diff + `max(lease_generation)` · exit code ของ teardown ⑱ **บรรทัด `BUILD_IMPACT:` ฉบับจริงหลังรู้ผล** ⑲ บรรทัด `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ⑳ ถ้ามีบูตที่สอง: ทุกข้อข้างบนแยกชุด **ห้ามรวมกับบูตแรก**)

---

## 🆕 GT-081 TRAVEL-GATE-WALK-OUT-AND-WALK-HOME-001 [attended, in-game]: ผู้เล่นที่ **หยุดยืน** ในเขตที่พินไว้กลางท่าเรือ ทำให้ **ตัวเอง** ข้ามไ... -- archived 20260827 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`)
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

🆕 **อัปเดต (chief cloud · รอบ `keen-pasteur-543ds8` R187 · 2026-08-27 ~09:00 (+07:00)) — คำเตือนสำคัญเรื่อง grep token ที่ใบนี้เคยใช้ผิด:** ใบนี้เคยตรวจคอนโซลหา `FIELD_MOB`/`HOSTILE` แล้วเจอ 0 บรรทัด (ดู `notes_to_chief/20260827_0205_GT084-NO-RESULT-*.md`) แต่ป้ายสองตัวนั้น **ไม่เคยมีอยู่จริงบน production path เลย** — เป็นช่องว่างการมองเห็น ไม่ใช่โค้ดไม่ทำงาน สาย B ตรวจสดแล้วยืนยัน (ดู `rounds/B_20260827_0805_gt084_roster_override_coverage.md`) ว่า 13/13 identity ของ field-mob roster อยู่ใน census จริง และ chief ต่อสายคอนโซลบรรทัดใหม่ให้แล้วรอบนี้ (`pirate-force-server` commit `dd5c785`): **`runtime.py`** พิมพ์ `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13 missing=none` ทันทีหลัง census ประกอบเสร็จ — **นี่คือ grep token ที่ถูกต้องสำหรับตรวจว่าเฟรม hostile ออกสายจริง** ไม่ใช่ `FIELD_MOB`/`HOSTILE` ⇒ **รอบ attended ถัดไปของ `GT-084` (หรือใบต่อยอด) ต้อง grep หา `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE` แทน** มิฉะนั้นจะอ่านผลผิดซ้ำเหมือนรอบก่อน ยืนยันด้วยบูต headless แล้ว (ก่อนแก้: ไม่มีบรรทัดนี้พิมพ์เลย = ผลลบเดิมของ `GT-084` ซ้ำได้จริง / หลังแก้: `matched=13/13` พิมพ์ทุกครั้งที่ประกอบ census สำเร็จ) — นี่คือ **wire layer เท่านั้น** ยังไม่ตอบว่าไคลเอนต์เรนเดอร์เป็นสีแดง/hostile จริงไหม (คำถามนั้นยังเปิดอยู่ใน `GT-084`/`RIDER-084-A` เดิม)

🆕 **อัปเดต (chief cloud · รอบ `optimistic-mccarthy-ahn7zb` R188 · 2026-08-27 ~11:3x (+07:00)) — `CORE-REQUEST-008` ต่อสายแล้ว: ความเสี่ยง world-wipe ของ `mob_combat.bar_frames`/`mob_death.death_frames` (ที่ริเดอร์นี้เปิดไว้ตั้งแต่แรก) ปิดแล้วที่ชั้น static/wire:** `MOB_COMBAT_BAR`/`MOB_DEATH_DYING`/`MOB_DEATH_DEAD` compose เข้า full census เดียวกับ arrival แล้วทั้งสามจุด (`pirate-force-server@741ab5d`, grep token ใหม่ `MOB_COMBAT_BAR_CENSUS_RECOMPOSE`/`MOB_DEATH_FRAMES_CENSUS_RECOMPOSE`) แทน one-entry frame เดิม พร้อม fail-closed guard (compose ล้มเหลว หรือ scene ไม่ตรง ⇒ ถอยไป one-entry frame แทนโครง exception/ส่งเฟรมผิดฉาก — พบโดย `pf-adversary` ในรอบเดียวกัน ดู `rounds/R188_*.md`) 🔴 **ริเดอร์นี้เองยังไม่เปลี่ยนแม้แต่ตัวอักษรเดียวตามกฎ nonclaim ②-③ เดิม** — `OW1`-`OW3` ยังเป็นขั้นสังเกตบังคับเหมือนเดิมทุกประการ การแก้นี้ตอบเฉพาะชั้น static/wire ว่าเฟรมที่ส่งออกไม่ใช่ one-entry อีกต่อไป **ไม่ได้ตอบว่าไคลเอนต์จริงเห็นอะไร** — ห้ามอ่านว่า client-observable risk ถูกปิดแล้ว ผลจริงยังต้องรอ `OW1`-`OW3` เหมือนเดิมทุกประการ



---

## GT-084-R2 HOSTILE-PAIR-VISIBLE-001: รอบสองของ GT-084 -- คู่ faction (1,6) ที่ผู้เล่นได้ครึ่งของตัวเองแล้ว ทำให้ Tornado Eagle ขึ้นศัตรูจริงบนจอไหม (~~ชื่อแดง + แผงเป้าแดง~~ [UPDATE 2026-08-27T17:34+07:00 LANE-B ต่อยอด PANYA-REFERENCE 16:35+07:00: เกณฑ์สีที่ถูกต้องคือ **ส้ม (ยังไม่ aggro) → แดงเข้ม (aggro) → เทา (ตาย)**, ไม่ใช่ "แดง" เฉยๆ] + แผงเป้า) บนบูตไร้แฟล็ก -- ก่อนจะไปถึงเรื่องตี  [🟡 **RESULT -- claim หลัก (hostile ที่ตาเห็น) PASS ด้วยหลักฐานพฤติกรรม (ขอบแดง+ลูกศรแดงคู่, ดับเบิลคลิกตีติดจริง) แต่ไม่ใช่สีตามใบเป๊ะ (ชื่อชมพู/magenta ตลอด ไม่ใช่ส้ม→แดงเข้ม→เทาตามลำดับสถานะจริง, ไม่มีแผงเป้า) -- ผลต่อขั้นตี-ตาย: ดู GT-084 -- รายละเอียด notes_to_chief/20260827_1620_GT084R2-RESULT-*.md, RE-107/RE-108 ปิดแล้ว (bounded negative), RE-109 เปิดใหม่ถามครบ 6 สี, สถานะสุดท้าย (PASS/MIXED) รอ chief ตั้ง**]

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
แต่การประกาศปิดเกณฑ์เป็นของ COO ไม่ใช่ของสาย B ⇒ ดู `rounds/B_20260828_1749_*.md` ก่อนตัดสิน

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

## GT-102 CORE-REQUEST-014 COLUMBUS-NPCCONVERSATION-QUEST3021-DIALOGUE-001: คลิก Columbus ที่ Port Royal (MOBS n_ID 156, bg0001 placement index 1) ครั้งแรกหลัง CORE-REQUEST-014 -- เห็นบทสนทนาเควสต์ 3021 จริงไหม (เมื่อวานคลิกแล้วเงียบ)  [PENDING]

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md, prefix สองแบบ ห้ามแยกตัวนับ.
> เลขสูงสุดที่ใช้ไปแล้ว ณ เวลาเขียนใบนี้: GT-101 (GAME_TEST_QUEUE.md) และ RE-103 (CLIENT_RE_QUEUE.md,
> บันทึกไว้เองว่า "เลขว่างถัดไป = 102"). grep ยืนยันก่อนจอง: GT-102 = 0 hit, RE-102 = 0 hit ทั้งสองไฟล์
> (ยืนยัน 2026-08-27). ใบเก่าทุกใบอยู่ที่เดิม ไม่ถูกแตะ ไม่ถูกย้าย.

### ที่มา -- อ่านจากซอร์สจริง ห้าม re-derive ระหว่างรอบ
- `notes_to_chief/20260827_1052_LANE-A-CORRECTION-columbus-m2-quest3021-not-3023-scene17-not-19.md`:
  Port Royal Columbus คือ MOBS `n_ID=156` (s_ROLE_GRAPHIC=COLUMBUS_0), bg0001 census placement **index 1**
  -- ข้อผูก "index 1 = MOBS 156" เป็น **owner testimony** (PANYA-DECISION 0925/0950 ในเซสชัน attended
  ต่อเนื่องเดียว) **ไม่ใช่ table crosswalk** และเลขนี้เคยขยับมาแล้วครั้งหนึ่งในวันเดียวกัน (RE-097 เคยเสนอ
  index 0 ก่อน) -- ดูหมายเหตุใน nonclaims ว่าทำไมข้อนี้สำคัญ. quest = **3021** (ไม่ใช่ 3023 ซึ่งเป็นของ MOBS
  n_ID=36 คนละตัว), `s_LUASCRIPT=Q_TELEPORT1`, `n_VARI_2=17` (ปลายทาง scene 17/`Bg1001`, ทะเล) -- ยืนยันจาก
  `QUESTDATA_TH__QUEST.tsv` (`n_ID=3021` แถวเดียว, provenance sha256 ปักไว้ที่
  `tests/test_world_columbus_m2_crosswalk.py`).
- `pf_bridge/gamedata/tables/QUESTTEXT_TH__TEXT_QUEST.tsv:1312` (row `n_ID=3021`): `s_QUEST_NAME` = "มุ่งหน้าไป
  Atlantic Ocean：Rising Sun Sea", `s_WORD1` (คำถามในบทสนทนา) = "พร้อมที่จะออกเดินทางไปยัง<text>[52300126]</text>
  อย่างอิสระแล้วหรือยัง?", `s_WORD2` (ปุ่มตอบรับ) = "ข้าชอบการเดินทางแบบอิสระ", `s_WORD3` (ปุ่มปฏิเสธ) = "ข้า
  จะอยู่ที่นี่" -- **นี่คือข้อความที่ใบนี้คาดว่าจะเห็นบนจอ ถ้า NPCConversation ที่ส่งจริงตรงกับเควสต์ 3021**.
- `src/pirateforce_foundation/columbus_quest_dispatch.py` (pirate-force-server, ยังไม่ merge -- ดูด่าน 0):
  `production_allowed = True`, ไม่มีแฟล็ก. `dispatch_columbus_quest3021()` เขียนไว้เองว่า **ปฏิเสธเสมอวันนี้**
  ด้วยเหตุผลสองข้อที่แยกกัน (`scene17_teleport_refused_scene_has_no_pinned_spawn` จาก `world_scene_entry
  .resolve_entry` เพราะ scene 17 ไม่มี pinned spawn -- ดู RE-103 เปิดอยู่ -- และ
  `no_re096_vehicle_row_evidence` เพราะยังไม่มี wire evidence ของ payload ผูกเรือ -- ดู RE-096 เปิดอยู่) --
  **แต่ทั้งสองเหตุผลนี้เกี่ยวกับ op1 (`QuestOperateVital`) เท่านั้น ไม่เกี่ยวกับการคลิกครั้งแรกที่ใบนี้ทดสอบ**.
- `src/pirateforce_foundation/runtime.py::_dispatch_columbus_quest3021` (บรรทัด ~4186-4301): แขนแรก (คลิก)
  รันเมื่อ `nested_id in (legacy.TARGET_VITAL, legacy.CHOOSE_NPC)` และ `self.population_indices is not None`
  และ `columbus_quest_dispatch.COLUMBUS_PLACEMENT_INDEX in self.population_indices` (เกตนี้ **load-bearing
  ไม่ใช่ defensive** -- คอมเมนต์ของโค้ดเองอ้าง `tests/test_world_census_wiring.py`) -- ถ้าตัวที่คลิกตรงกับ
  actor identity ของ Columbus (`columbus_quest_dispatch.columbus_actor_identity(legacy)` = `0x2000+1+1` =
  `0x2002` ตามสูตรเดียวกับที่ census ทั้งหมดใช้) จะคิวแอ็กชันเลเบล
  `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` เข้าไปครั้งเดียวต่อเซสชัน (ธง
  `self.columbus_quest3021_conversation_sent` กันส่งซ้ำ) และ append event
  `core_request_014_columbus_npc_conversation_sent_once`. เฟรมที่ประกอบเป็น `NPCConversation` (`0x31D8`)
  ทรงเดียวกับ `make_npc_conversation_quest3020` เดิม (RE-094 พิสูจน์ว่าเป็นทรงทั่วไป) พารามิเตอร์ด้วย actor
  identity ของ Columbus กับ quest id `3021`.
- `self.population_indices` ถูกประกอบจาก **arrival census ปกติตอน login** (`runtime.py` บรรทัด ~5332,
  `generation.indices`) -- ไม่มีสวิตช์แยก ไม่ต้องเดินไปใกล้ Columbus ก่อนเซิร์ฟเวอร์จะ "รู้จัก" เขา -- แต่
  ผู้เล่นยังต้อง **เดินไปให้เห็นโมเดลบนจอจริง** ก่อนถึงจะคลิกได้ (นี่คือข้อจำกัดของมนุษย์หน้าจอ ไม่ใช่ของ
  server-side gate).
- พิกัดจริงของ placement index 1 (จากตารางที่ frozen เดิม, `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` แถวที่ 2):
  X **-8013.458984375**, Y **-2780.045166015625**, Z **223.29209899902344** -- 🔴 **หมายเหตุ**: คอลัมน์ชื่อ
  แสดงผล (7th field) ของแถวนี้ในตารางเก่าเขียนว่า `'Sebastian'` ไม่ใช่ `'Columbus'` -- เป็นป้ายเก่าที่ไม่
  อัปเดต ห้ามใช้ตัดสินตัวตน ให้เชื่อ owner testimony (0925/0950) ที่ผูก index 1 = Columbus (MOBS 156) แทน.
  ระยะจากจุดเกิด (X -8553.9473, Y -2579.6890, Z 186.0 ตามที่ GT-084/GT-101 ใช้) ถึงพิกัดนี้ ~576 หน่วย
  (ใกล้กว่า GT-084's target มาก).
- `notes_to_chief/FROM_CHIEF_R192_TO_ATTENDED_20260827_1230.md`: chief เขียนตรงถึงผู้เทสเองว่า "ทดสอบแค่
  Columbus ตอบจริงไหม ไม่ต้องลองกดไปทะเลต่อ (ยังไม่พร้อม)" -- ใบนี้เขียนตามคำสั่งนั้นเป๊ะ (ดู steps ข้อ 6
  และ nonclaims).

### objective (claim เดียว)
เมื่อผู้เล่นคลิกโมเดล Columbus (placement index 1) ที่ Port Royal บนบูตไร้แฟล็ก -- ไคลเอนต์แสดงหน้าต่างบท
สนทนาที่มีข้อความตรงกับเควสต์ 3021 จริงหรือไม่ (ไม่ใช่ความเงียบแบบเมื่อวาน ไม่ใช่ error ไม่ใช่บทสนทนาของ
เควสต์อื่น) -- ทั้งชั้น wire (เฟรม `NPCConversation` + event ถูกคิวจริง) และชั้น client-observable
(สิ่งที่ตาเห็นบนจอ). ใบนี้ **ไม่ทดสอบ** ว่ากด "มุ่งหน้าไป Atlantic Ocean" (ตอบรับ) แล้วเกิดอะไรต่อ -- นั่นคือ
op1/`QuestOperateVital` ซึ่งเขียนไว้แล้วในซอร์สว่า **ปฏิเสธเสมอวันนี้** ด้วยเหตุผลที่ไม่เกี่ยวกับคำถามของใบนี้
(ดู nonclaims).

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)
- P1 [เสนอ, หัวใจของใบ] คลิกโมเดล Columbus ครั้งแรกในเซสชัน -> คอนโซลเซิร์ฟเวอร์พิมพ์บรรทัด
  "[G>] CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE (N bytes)" ครั้งเดียว พร้อม event
  `core_request_014_columbus_npc_conversation_sent_once`.
- P2 [เสนอ] ถ้า P1 เป็นจริง -- หน้าต่างบทสนทนาโผล่บนจอจริง มีข้อความตรง/ใกล้เคียง `s_QUEST_NAME`="มุ่งหน้าไป
  Atlantic Ocean：Rising Sun Sea" และ/หรือ `s_WORD1`="พร้อมที่จะออกเดินทางไปยัง...อย่างอิสระแล้วหรือยัง?" --
  ไม่ใช่ข้อความว่าง ไม่ใช่ error, ไม่ใช่ข้อความของเควสต์อื่น (เช่นเควสต์ 3020 เดิม).
- P3 [เสนอ, ตัวหักล้าง] ถ้าคลิกแล้วไม่มีอะไรขึ้นเลย (เหมือนเมื่อวาน) และคอนโซลไม่มีบรรทัด P1 เลย -> event
  ที่ควรเห็นแทนคือหนึ่งใน `columbus_choose_npc_parse_error_*` / `columbus_actor_not_found_*` /
  `columbus_conversation_compose_refused_*` (ชื่อ event ที่โค้ดเองประกาศไว้สำหรับกรณีปฏิเสธที่แขนคลิก) หรือ
  ไม่มี event ใหม่เลย (แปลว่าเกตไม่ผ่านตั้งแต่ `population_indices`/`nested_id`) -- นี่คือผลลบที่มีค่าเท่ากับ
  PASS ต้องเขียนให้เด่นเท่ากัน พร้อม redirect ไปยังเหตุผลที่คอนโซลพิมพ์จริง.
- P4 [ข้อมูล, ไม่ตัดสิน pass/fail ของใบนี้] ถ้าผู้เทสคลิก/กดปุ่มตอบรับ "ข้าชอบการเดินทางแบบอิสระ" ต่อ (ไม่ว่า
  ตั้งใจหรือพลาด) -- คาดว่าคอนโซลจะพิมพ์ event `columbus_quest3021_dispatch_refused_
  scene17_teleport_refused_scene_has_no_pinned_spawn` แล้ว
  `columbus_quest3021_dispatch_refused_no_re096_vehicle_row_evidence` และ **ไม่มีการย้ายฉาก/กลายเป็นเรือบน
  จอเลย** (ยังอยู่ Port Royal เหมือนเดิม) -- นี่คือพฤติกรรมปฏิเสธที่ตั้งใจ ไม่ใช่บั๊ก แต่ **ไม่ใช่ objective ของ
  ใบนี้** ห้ามใช้ตัดสิน PASS/FAIL ของใบนี้เอง (ดู nonclaims).

### ก่อนบูต -- ด่าน 0 (ยังไม่ merge ณ ตอนเขียนใบนี้ -- ห้ามข้าม), ด่าน 1 (green boot), ด่าน 2 (grep ยืนยันสาย)

**ด่าน 0 -- สถานะ merge:** CORE-REQUEST-014 อยู่ที่ commit `5d9cfd3` บนแบรนช์ `claude/tender-ride-4txjyg`
ของ `pirate-force-server` ณ 2026-08-27 -- **PR ยังเปิดอยู่ ยังไม่ merge เข้า `main`**. `pf_resolve_green_boot
.py` เดินตาม `origin/main` เท่านั้น (คำอธิบายในหัวไฟล์ของสคริปต์เอง) -- ถ้า PR ยังไม่ merge ตอนที่ผู้เทสรัน
ด่าน 1 รีโซลเวอร์จะไม่คืนคอมมิตที่มีโค้ดนี้ (`exit 3` หรือคอมมิตที่ไม่มี `columbus_quest_dispatch.py`) --
ใบนี้ยัง**บูตไม่ได้** ให้บันทึกผลเป็น "รอ merge" แล้วไปทำใบอื่น -- **ห้าม checkout branch `claude/tender-
ride-4txjyg` ตรง ๆ ข้ามรีโซลเวอร์** แม้จะรู้เลข commit ก็ตาม (กติกาเดียวกับทุกใบอื่นในคิวนี้).

**ด่าน 1 -- resolve commit เขียว:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
รันจากโฟลเดอร์ pf_bridge, exit 0 + `BOOT_COMMIT: <sha>` เท่านั้นถึงบูตได้ (git checkout `<sha>` แบบ detached
HEAD). ห้ามเทียบเลข commit ด้วยตา -- resolver คืนหัวแบรนช์ที่ผ่านเกต ไม่ใช่ merge commit เสมอไป.

**ด่าน 2 -- ยืนยันสายจริงของ `<SHA>` (ห้ามเชื่อเลขบรรทัดในเอกสาร ต้อง grep ของจริง):**
```
git grep -n "columbus_quest_dispatch" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "_dispatch_columbus_quest3021" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "def dispatch_columbus_quest3021" <SHA> -- src/pirateforce_foundation/columbus_quest_dispatch.py
git grep -n "core_request_014_columbus_npc_conversation_sent_once" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "COLUMBUS_QUEST_ID = 3021" <SHA> -- src/pirateforce_foundation/columbus_quest_dispatch.py
```
ต้องได้อย่างน้อย 1 บรรทัดต่อคำสั่งทั้ง 5 คำสั่ง. ขาดข้อใดข้อหนึ่ง = **BLOCKED** -- คอมมิตที่จะบูตยังไม่มี
CORE-REQUEST-014 ต่อสายจริง ห้ามบูต ห้ามหาคอมมิตเอง ไปทำใบอื่นแล้วรอ merge.

### db (สำเนาเสมอ ห้ามเปิด canonical, ห้ามแตะ state\play.sqlite3)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-102_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt102.sqlite3
```
- เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง.
- สำเนาใหม่ทุกบูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดเสมอ (X -8553.9473, Y -2579.6890, Z 186.0).

### server args (เป๊ะ -- ไม่มี --*-scenario เพราะ CORE-REQUEST-014 ทำงานเสมอ ไม่มีสวิตช์)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt102.sqlite3
```
ห้ามมี `--*-scenario` แม้แต่ตัวเดียว, ห้ามพ่วงใบอื่นเข้าบูตนี้. หลักฐานว่าไม่มีแฟล็กจริง เก็บทันทีหลัง
เซิร์ฟเวอร์ขึ้น แปะทั้งบรรทัดลงผล:
```
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List
```

### steps (คลิกต่อคลิก -- อัดวิดีโอต่อเนื่องตลอดช่วงถือ LOCK_GAME)
ก่อนเริ่ม: ถือ LOCK_GAME, จด boot stamp (+07:00, ต้องไม่เก่ากว่า 420 นาทีตอนรัน teardown), เทียบ sha
canonical, copy DB สองใบตามบล็อก db, เตรียม teardown จาก `TEMPLATE_teardown_generic.ps1`. ยืนยันด่าน 0-2
ผ่านครบ (จด SHA ที่บูต).

1. สตาร์ตเซิร์ฟเวอร์ก่อนเสมอ (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด
   client). client ที่บูตโดยไม่มีเซิร์ฟเวอร์ตายเองใน ~3.5 นาที. ถ้าต้องฆ่า client กลางคัน ต้อง restart
   server ก่อนเปิด client ใหม่เสมอ (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่ "connecting" ตลอดกาล).
2. เปิด client -> เลือกเซิร์ฟเวอร์ -> dialog PVP ปุ่มซ้าย -> หน้าเลือกตัวละคร -> เลือกช่องแรก -> ปุ่มกลาง
   สุดจาก 5 ปุ่มแถวล่าง = เข้าเกม (ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด). เริ่มอัดวิดีโอต่อเนื่องตั้งแต่ก่อนกดเข้า
   เกม.
3. T0 -- เห็น HP bar/minimap/ชื่อแมพครบ. จด HUD X/Y. คลิกขวาค้างลากกวาดกล้อง 360 องศาหนึ่งรอบ (ตัวเช็ค
   NO-CRASH ตัวเดียวที่ใบนี้ยอมรับ -- คลิกขวาลากหมุนกล้องอย่างเดียว ทิศหันตัวละครไม่ขยับ ไม่ยิงอะไรออกสาย
   ปลอดภัยเสมอ -- **ห้ามใช้ Q/E เป็นตัวเช็คนี้เด็ดขาด** เพราะ Q/E หันตัวละครจริงและยิง `TargetPosVital`).
4. เดินไปทาง (-8013.5, -2780.0) โดยอ่าน HUD X/Y เทียบทุกช่วง (W/A/S/D คาดว่ายิง `TargetPosVital` ทุกครั้งที่
   ขยับ/หันตัว -- คาดหมายและไม่ใช่ความเสี่ยงของใบนี้). งบเวลาเดินทาง 10 นาที (ระยะ ~576 หน่วยจากจุดเกิด,
   ใกล้กว่าที่ GT-084 เคยเดิน). ถ้าครบ 10 นาทีแล้วยังไม่เห็นโมเดล NPC ที่ตำแหน่งนี้เลย ให้หยุดแล้วเขียนเป็น
   NO-RESULT พร้อมเหตุผล (ระยะวาดโมเดล/ตำแหน่งไม่ตรง) ไม่ใช่ FAIL.
5. เมื่อเห็นโมเดล: ถ่ายภาพนิ่ง full-res ของป้ายชื่อเหนือหัวโมเดล **ก่อน**คลิก (บันทึกสีป้าย + ข้อความป้ายถ้า
   อ่านได้). single-click ที่โมเดลหนึ่งครั้ง (ตามแบบ NPC-style interaction ที่ `docs/COMMAND_HANDOFF.md`
   บันทึกไว้แล้วว่าคลิกเดียวพอสำหรับ ChooseNPC/TargetVital -- ไม่ต้องดับเบิลคลิก). จดทันทีหลังคลิก: (ก)
   บรรทัดคอนโซลเซิร์ฟเวอร์ทั้งหมดที่ขึ้นใหม่ (ข) สิ่งที่เห็นบนจอ (หน้าต่างบทสนทนาขึ้นไหม ข้อความอะไร).
6. ถ่ายภาพนิ่ง full-res ทันทีที่เห็นหน้าต่างบทสนทนา (หรือทันทีที่ผ่านไป 10 วินาทีแล้วไม่มีอะไรขึ้นถ้า P3
   เป็นจริง) -- นี่คือภาพหลักที่ตัดสิน P2. **ถ้าเห็นหน้าต่างขึ้นจริง: อ่าน/บันทึกข้อความในหน้าต่างคำต่อคำ
   ห้ามอ่านจากความจำ ต้องอ่านจากภาพนิ่ง full-res เท่านั้น แล้วเทียบกับข้อความที่คาดไว้ใน P2. จากนั้น
   🔴 กดปุ่มที่แปลว่า "ปฏิเสธ/อยู่ที่นี่" (คาดว่าคือปุ่มสอง หรือปุ่มที่มีข้อความใกล้เคียง "ข้าจะอยู่ที่นี่")
   เพื่อปิดหน้าต่าง -- ห้ามกดปุ่มตอบรับ "มุ่งหน้าไป Atlantic Ocean" โดยตั้งใจ (คำสั่งตรงจาก chief letter
   `notes_to_chief/FROM_CHIEF_R192_TO_ATTENDED_20260827_1230.md`) เว้นแต่กดพลาด -- ถ้ากดพลาด ไม่ต้อง
   ตกใจ ให้จดเวลาที่กดพลาดไว้ แล้วสังเกต/จดตาม P4 ต่อ (ข้อมูลเสริม ไม่กระทบ pass/fail ของใบนี้) แล้วกลับมา
   ทำ NO-CRASH check ข้อ 7 ต่อตามปกติ.**
7. NO-CRASH check ซ้ำ: คลิกขวาลากอีกครั้ง -- ยืนยันไคลเอนต์ยังตอบสนอง.
8. ออกเกม -> teardown ตาม `TEMPLATE_teardown_generic.ps1` -> เทียบ sha canonical รอบสุดท้าย.

### pass criteria (สองชั้น แยกกันเสมอ ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)

ชั้น wire/DB (อ่านจาก server console/event log ล้วน ๆ ไม่ต้องพึ่งสิ่งที่เห็นบนจอ):
- single-click ที่โมเดล Columbus ทำให้คอนโซลพิมพ์บรรทัด
  "[G>] CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE (N bytes)" อย่างน้อยหนึ่งครั้งในเซสชันนี้
  (ครั้งแรกเท่านั้น -- ธง `columbus_quest3021_conversation_sent` กันส่งซ้ำโดยออกแบบ ครั้งที่สองไม่ควรพิมพ์
  ซ้ำ ถ้าคลิกซ้ำ ให้จดว่าไม่มีบรรทัดใหม่ขึ้นและถือเป็นพฤติกรรมที่ถูกต้อง ไม่ใช่ผลลบ).
- event `core_request_014_columbus_npc_conversation_sent_once` ปรากฏในเซสชันนี้ (ถ้ามีการ export event log
  ให้แนบ; ถ้าไม่มีช่องทางอ่าน event list โดยตรง ให้ถือบรรทัดคอนโซลข้อบนเป็นหลักฐาน wire เพียงพอ).
- `sessions`: `count(*) WHERE selected_character_id IS NOT NULL` +1 ต่อการเข้าเกมหนึ่งครั้ง, `max(lease_
  generation)` ไม่ถอยหลัง, `PRAGMA integrity_check` = `ok` บนสำเนา, sha256 canonical ก่อน-หลังตรงกับ
  `CANON_SHA.txt` ทั้งสองครั้ง.
- raw GAME log ทั้งไฟล์ + console out/err เก็บทั้งก่อน/หลัง ไม่ตัดทอน.
- ผลลบที่สมบูรณ์เท่ากับ PASS: คลิกโมเดล Columbus แล้วไม่มีบรรทัด
  "CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE" ขึ้นเลย และไม่มี event ใหม่ที่เกี่ยวข้องขึ้นเลย
  ตลอดรอบ ⇒ เขียนเป็นผลลบเต็มรูป พร้อมบรรทัดคอนโซลทั้งหมดที่ขึ้นแทน (ถ้ามี) เพื่อช่วยชี้ว่าเกตไหนไม่ผ่าน
  (`population_indices`/`nested_id`/`columbus_actor_not_found_*`/etc).

ชั้น client-observable (ต้องมีคนหน้าจอ, ห้ามอนุมานจากบรรทัดคอนโซล):
- หน้าต่างบทสนทนาปรากฏบนจอจริงหลังคลิก (หรือไม่ปรากฏ -- ทั้งสองผลมีค่าเท่ากันถ้าตรงกับที่ชั้น wire รายงาน
  ไว้ อย่าตัดสินแยกจากชั้น wire).
- ถ้าปรากฏ: ข้อความในหน้าต่างตรง/ใกล้เคียงกับที่คาดไว้ (`s_QUEST_NAME`/`s_WORD1` ของเควสต์ 3021 ตามที่จดไว้ใน
  "ที่มา") -- บันทึกข้อความที่เห็นจริงคำต่อคำจากภาพนิ่ง full-res แล้วเทียบเป็นบรรทัดต่อบรรทัด ไม่ใช่แค่ "ตรง/
  ไม่ตรง" เฉย ๆ.
- สีของป้ายชื่อทุกป้ายในทุกภาพนิ่ง full-res (ป้ายชื่อ Columbus ก่อนคลิก, ป้ายชื่อตัวเอง, ป้ายอื่นถ้ามีในเฟรม)
  บันทึกเป็นบรรทัดเดียวต่อป้ายต่อภาพ ("none" เขียนออกมาถ้าไม่มี ห้ามเว้นว่าง) -- อ่านจากภาพนิ่ง full-res
  เท่านั้น ห้ามอ่านจาก contact sheet/ภาพย่อ/วิดีโอ ห้ามอนุมานสาเหตุของสี (`RE-067` เปิดอยู่). ไม่มีภาพอ้างอิง
  ของเซิร์ฟเวอร์ต้นฉบับที่รู้จักสำหรับ NPC ตัวนี้โดยเฉพาะ ณ ตอนเขียนใบนี้ -- ใช้
  `compared_and_matched=no-reference` ถ้าไม่มีภาพอ้างอิงจริง ๆ.

### nonclaims
- 🔴 **ใบนี้ไม่ทดสอบว่ากดตอบรับ ("มุ่งหน้าไป Atlantic Ocean") แล้วเกิดอะไรต่อ** -- op1/`QuestOperateVital`
  เขียนไว้แล้วในซอร์สว่าปฏิเสธเสมอวันนี้ด้วยเหตุผลสองข้อที่เปิดอยู่ (`RE-103` พิกัด player-arrival ของ scene
  17, `RE-096` payload ผูกเรือ) -- **ไม่ใช่คำถามของใบนี้** ถ้าผู้เทสกดพลาดแล้วเห็นพฤติกรรมตาม P4 ให้จดไว้เป็น
  ข้อมูลเสริมเท่านั้น ห้ามใช้ตัดสิน PASS/FAIL ของใบนี้เอง (ตามคำสั่งตรงของ chief letter R192).
- ข้อผูก "placement index 1 = Columbus (MOBS 156)" เป็น **owner testimony** ไม่ใช่ table crosswalk (ดู "ที่มา")
  -- ถ้าบทสนทนาที่เห็นไม่ตรงกับเควสต์ 3021 ใบนี้ **แยกไม่ออก** ระหว่าง (ก) การต่อสาย NPCConversation ผิด กับ
  (ข) ข้อผูก index-1-คือ-Columbus เองผิด -- เขียนทั้งสองความเป็นไปได้ไว้ในผล ไม่ตัดสินเอง.
- ใบนี้ไม่ยืนยันไบต์ดิบของเฟรม `NPCConversation` สำหรับเควสต์ 3021 เทียบกับ capture จริง -- RE-094 พิสูจน์แค่
  ทรงทั่วไปของเฟรม (จากเควสต์ 3020), ยังไม่มีใครรัน RE-095-style wire capture ให้กับ 3021 โดยเฉพาะ (มีข้อ
  เสนอชื่อใบอย่างไม่เป็นทางการว่า `NPCCONVERSATION-COLUMBUS-156-QUESTID-3021-WIRE-CONFIRM-001` ใน LANE-A
  correction letter แต่ **ยังไม่ได้เปิดเป็นใบจริงในคิว ณ ตอนเขียนใบนี้** -- อย่าอ้างเลขที่ยังไม่มี) -- ใบนี้
  ปิดคำถามแค่ระดับ "ฟังก์ชันถูกเรียกจริง + คนเห็นข้อความที่ตรงกัน" ไม่ใช่ระดับไบต์.
- ใบนี้ทดสอบผู้เล่นคนเดียว เซสชันเดียว -- ไม่ทดสอบว่าผู้เล่นคนที่สองคลิก Columbus พร้อมกันจะเกิดอะไร.
- ไม่ทดสอบความเสถียรข้าม reconnect/relogin -- ล็อกอินครั้งเดียวในรอบนี้.
- ไม่ชี้สาเหตุของสีป้ายชื่อ (`RE-067` เปิดอยู่).
- ถ้าด่าน 0/1/2 ไปไม่ถึง (ยังไม่ merge/BLOCKED) => ทั้งใบเป็น "รอ merge"/BLOCKED ไม่ใช่ NO-RESULT/FAIL --
  ยังไม่ได้ล็อกอินเลย.

### result (ผู้เทสกรอก)
```

```

---

## GT-103 GM-002 COMMAND-WIRE-CAPTURE-MATRIX-001: ล็อกอินด้วยบัญชี GM แล้วหา/เปิด GM editor widget พิมพ์ข้อความหลายแบบ -- capture file ของ `0x51E9` ขึ้นที่ `capture/gm_command_capture/` ไหม (path นี้ live บน production ครั้งแรกรอบนี้)  [NO-RESULT ต่อ claim ของตัวเอง -- A/B ทั้งสี่สถานะ UI เงียบสนิท, blocked on RE-126 · ปิดหัวใบโดย LANE-GM (เจ้าของใบ) รอบ `hs9m2r` 2026-08-28T17:1x+07:00 จากผล attended กะ1-A `notes_to_chief/20260828_1140_GT103AB-RESULT-NEGATIVE-four-ui-states-all-silent-RE118-panel-hypothesis-falsified.md` · OBSERVER_CONFIRMED: 2026-08-28T11:36-11:37+07:00 (BOOT_COMMIT `336857cd` = main HEAD, ไร้แฟล็ก) · เจ้าของคลิก `BT_GM` 4 สถานะ (HUD เปล่า / แผนที่เปิดค้าง / กระเป๋าเปิดค้าง / ปิดกระเป๋าแล้วคลิกซ้ำ) เงียบทุกครั้ง · สำมะโนเฟรมขาเข้าทั้งบูต `0x51E9` = 0 ⇒ `capture/gm_command_capture/` ABSENT ถูกต้องแล้ว ไม่ใช่ teardown fail ⇒ **ใบนี้ไม่เคยไปถึงข้อ 3 จึงไม่มีผลต่อ claim ของตัวเอง** · `TargetPosVital` x3 ช่วงเดียวกัน = client มีชีวิต ไม่ใช่เซสชันตาย · ผลข้างเคียงที่มีค่าสูง: สมมติฐานเชิงปฏิบัติของ RE-118 (เปิด panel ให้ current-UI key ไม่ว่าง) **ถูกหักล้าง** ⇒ เปิด `RE-126` ต่อ (ประตูบานแรก `this+0x48` แทนบานสุดท้าย) · [ไม่อ้าง] ว่า capture path ของ `0x51E9` ใช้ได้หรือไม่ -- ยังไม่เคยถูกทดสอบ live เลย · 🔴 **ทางเลี่ยง:** `GT-127` (คำสั่ง GM ผ่านกล่องแชท `0xAC52`) ไม่ต้องรอใบนี้และไม่ต้องรอ `RE-126`]

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md. grep ยืนยันก่อนจอง: GT-103 = 0 hit ⇒ ใบนี้คือ GT-103 (RE-104
> ถูกใช้แล้วในรอบเดียวกัน โดยใบพี่น้อง). เลขว่างถัดไป = 105. ใบเก่าทุกใบอยู่ที่เดิม ห้ามแตะ.

### ลิงก์ (รายละเอียดเต็มอยู่ที่นี่ ไม่ใช่ในใบนี้)
- wiring/capture path: `notes_to_chief/20260827_1700_CHIEF-REPLY-CORE-REQUEST-010-...md`, `docs/GM_LANE.md`
- widget-trigger: `RE-091` (producer), `RE-104` (open/toggle trigger -- **CLOSED PASS/DONE รอบ `kcm8ir`**,
  `notes_to_chief/20260827_1518_RE-104-RESULT-BT-GM-MODULE-PLUS19-GATE.md`) -- procedure ด้านล่างอัปเดตแล้ว
- บัญชี/config อนุมัติแล้ว (ใช้ซ้ำ): `notes_to_chief/20260827_1200_CHIEF-REPLY-GT101-gm-accounts-test-config-approved.md`
- decode field pin: `RE-088` (positional names only, no semantics)

### objective (claim เดียว)
ส่งข้อความอย่างน้อยหนึ่งครั้งผ่าน GM editor widget ของไคลเอนต์จริงด้วยบัญชี `attended_test` -- ไฟล์ capture
ตรงจำนวน/ตรงชื่อบัญชีปรากฏที่ `capture/gm_command_capture/` (relative กับ CWD ของ server process ตอนบูต)
จริงหรือไม่. ไม่มี reply frame ส่งกลับ (`0x8C77` ยังไม่ต่อสาย) -- ใบนี้ไม่ทดสอบว่าคำสั่งใดทำงาน (GM-003
คนละใบ).

### ด่าน 0 (ใช้ซ้ำ GT-101 ไม่ขอใหม่) / ด่าน 1 (green boot) / ด่าน 2 (grep ยืนยันสาย ที่ `<SHA>` จริง)
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
git grep -n "GM_RUN_GM_COMMAND_VITAL_ID" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "def handle_gm_run_command_vital" <SHA> -- src/pirateforce_foundation/gm/dispatch.py
git grep -n "def capture_raw_gm_command" <SHA> -- src/pirateforce_foundation/gm/command_capture.py
git grep -n "production_allowed = True" <SHA> -- src/pirateforce_foundation/lane_hooks/lane_gm_run_command.py
```
ขาดข้อใดข้อหนึ่ง = BLOCKED (precondition gate) -- ไปทำใบอื่น. (คนละแบบกับ "หา widget ไม่เจอ" ข้างล่าง)

> 🔴 แก้ด่าน 2 เมื่อ 2026-08-28T17:1x+07:00 โดย LANE-GM (เจ้าของใบ) รอบ `hs9m2r` ตามที่กะ1-A รายงานใน
> `notes_to_chief/20260828_1140_GT103AB-RESULT-NEGATIVE-*.md`: บรรทัดเดิม
> `git grep "handle_gm_run_command_vital" -- src/pirateforce_foundation/runtime.py` **ล้าสมัย** -- โค้ด
> ย้ายออกจาก `runtime.py` ไป `lane_hooks/lane_gm_run_command.py` + `gm/dispatch.py` แล้วตั้งแต่ v6.3
> lane_hooks move-out ⇒ ทำตามใบตรง ๆ จะได้ 0 hit และขึ้น **BLOCKED ทั้งที่ของอยู่ครบ** (กะ1-A เจอสด ๆ
> ตอนบูต 11:36 และต้องเปลี่ยนด่านเอง) ชุด 4 บรรทัดข้างบนคือชุดที่กะ1-A รันจริงแล้วผ่านทั้งหมด
> ประวัติเดิมขีดฆ่า ไม่ลบ: บรรทัดที่ถอดออกคือ `git grep -n "handle_gm_run_command_vital" <SHA> --
> src/pirateforce_foundation/runtime.py`

### db / server args
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-103_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt103.sqlite3
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
$env:PF_GM_ACCOUNTS_CONFIG = "<path จากด่าน 0>"
py -3 -u -m pirateforce_foundation.app --db state\run_gt103.sqlite3
```
ไม่มี `--*-scenario`. `--export-events` เป็นแฟล็กเสริมไม่บังคับ (คอนโซลไม่พิมพ์ event นี้ถ้าไม่เติม --
หลักฐานหลักคือไฟล์ capture บนดิสก์เสมอ). เทียบ sha256 canonical กับ `CANON_SHA.txt` ก่อน/หลัง.

### steps (สืบเนื่องจาก GT-101 เซสชันเดียวกันได้ ไม่ต้อง relogin)
1. เข้าเกม, NO-CRASH กวาดกล้อง (เหมือน GT-101 ขั้น 1-3).
2a. **หาปุ่ม `BT_GM` ก่อน** ตาม procedure ที่ `RE-104` พิสูจน์แล้ว (ไม่ใช่การสุ่มอีกต่อไป): หาปุ่ม/control
   resource ชื่อ `BT_GM` ใน notification/system UI (ปุ่มจะแสดง/กดได้ก็ต่อเมื่อสถานะ GM ของ connection ผ่าน
   gate อยู่แล้ว, ไม่ใช่ทุก account) -- ปุ่มนี้เป็นทางเข้าไปยัง panel ชื่อ `GMUI_BASIC` ที่มี tab
   `Radiobutton_Message` (เลือก lane) และช่อง `TextBox_Message` (พิมพ์ข้อความ). RE-104 ไม่ให้พิกัดบนจอ
   (static เท่านั้น) จึงยังต้องหาตำแหน่งจริงด้วยสายตา 1 ครั้ง -- จดตำแหน่ง/รูปร่างที่เจอไว้ด้วย (ภาพนิ่ง)
   เพื่อให้รอบถัดไปไม่ต้องหาอีก.
   - พบ -> ข้อ 2b (A/B ของ `RE-118`).
   - **Bounded fallback ถ้าไม่พบ `BT_GM` ภายใน 5 การลอง** (สั้นกว่าเดิมเพราะตอนนี้รู้ชื่อ resource และ
     เงื่อนไข gate แล้ว ไม่ใช่การสุ่มเปล่า): บันทึก **NO-RESULT (BT_GM control not found/not visible in this
     UI build, bounded exploration)** พร้อมจุดที่มองแล้ว แล้วข้ามไป teardown (ไม่ใช่ FAIL/BLOCKED -- RE-104
     nonclaim ① ไม่ตัดสินว่าบัญชีที่ไม่ใช่ GM หรือ UI build อื่นจะเห็น control นี้หรือไม่) -> จบ (ไม่ทำข้อ 2b/3).
2b. **A/B ของ `RE-118`** (GT-107-R3 พบว่าคลิก `BT_GM` เงียบสนิท -- RE-118 พิสูจน์ static แล้วว่าสาเหตุคือ
   dispatcher ต้องการ current-UI-key ที่ไม่ว่าง ไม่ใช่ field ใหม่บนเฟรม `0x5A19`), ทำต่อจากข้อ 2a ทันที:
   - **(A) ก่อน**: คลิก `BT_GM` จาก HUD เปล่า (ไม่มี panel อื่นเปิดอยู่ก่อนหน้า) แล้วสังเกต -- คาดหมายตาม
     GT-107-R3 เดิม (เงียบ ไม่มีหน้าต่าง).
   - **(B) ต่อ**: เปิด panel อื่นที่รู้ว่าให้ current-UI key ไม่ว่างก่อน (เช่นหน้าต่างแผนที่ M หรือหน้าต่าง
     inventory -- เลือกอันไหนก็ได้ที่เปิดสำเร็จแน่ ๆ) แล้วคลิก `BT_GM` ซ้ำโดยไม่ปิด panel นั้นก่อน.
   - ถ้า (B) เปิด `GMUI_BASIC` ได้: บันทึกว่า panel ไหนทำให้ current-UI key ไม่ว่าง (ภาพนิ่ง) แล้วไปข้อ 3
     ด้วย panel นั้นเปิดค้างไว้เป็นเงื่อนไขก่อน-คลิกเสมอ -- นี่คือ client-observable ใหม่ที่ RE-118 static
     เดาไม่ได้ (ดู RE-118 T4/T5).
   - ถ้า (B) ยังเงียบเหมือน (A): บันทึก **NO-RESULT (A/B ทั้งคู่เงียบ, current-UI-key ยังไม่ nonempty แม้เปิด
     panel)** พร้อม panel ที่ลอง แล้วข้ามไป teardown -- RE-118 BUILD_IMPACT ระบุขั้นต่อไปคือ instrument
     current-key return/create-null โดยสาย RE ไม่ใช่งานฝั่งเทสอีกแล้ว -> จบ (ไม่ทำข้อ 3).
3. ถ้าผ่าน (B) ในข้อ 2b: พิมพ์ 4-8 ข้อความทดสอบ (สั้น/มีอาร์กิวเมนต์/ว่างเปล่า/ยาว+ไทย) กด Enter ทีละอัน
   เว้น 3 วินาที จดเวลาส่งแต่ละอัน (+07:00).
4. ยืนยันจอไม่มีปฏิกิริยาต่อเนื้อหาข้อความ (คาดหมายอยู่แล้ว) -- ถ่ายภาพนิ่งท้ายสุด.
5. NO-CRASH ซ้ำ -> teardown -> เทียบ sha canonical -> ลบสำเนา config/env -> **เก็บทั้งโฟลเดอร์
   `capture/gm_command_capture/` แนบผล**.

### pass criteria (สองชั้น แยกกันเสมอ)
wire/DB: พบ widget+ส่ง N ข้อความ ⇒ `capture/gm_command_capture/` มีไฟล์ `.txt` ใหม่ N ไฟล์ ชื่อมี
`attended_test`/`_0x51E9`, มี header+decode section (FAILED-pin ก็นับเป็นผลถูกต้อง)+hex dump. ไม่พบ widget
(ข้อ 2a) หรือ A/B ทั้งคู่เงียบ (ข้อ 2b, ดู `RE-118`) ⇒ โฟลเดอร์ไม่มีไฟล์ใหม่เลย (ผลลบสมบูรณ์ ไม่ตอบคำถามหลักแต่
ไม่ใช่ FAIL, ทั้งสอง NO-RESULT ชนิดนี้แยกกันตามสาเหตุที่บันทึกในข้อ 2a/2b). sha256 canonical ตรงก่อน/หลัง,
`PRAGMA integrity_check`=ok, raw log/console เก็บครบ.
client-observable: ปกติ**ไม่มีอะไรเปลี่ยนบนจอ**ตอบสนองเนื้อหาคำสั่ง (nonclaim ล่วงหน้า ไม่ใช่ FAIL) --
สิ่งเดียวที่สังเกตคือผลของการสำรวจหา widget เอง (บันทึกทุกจุดที่ลอง+ผล, ถ่ายภาพรูปร่าง/ตำแหน่ง widget ถ้าพบ).
สีป้ายชื่อในภาพ (ถ้าเห็น) บันทึกแบบ "none" ถ้าไม่มี ไม่ชี้สาเหตุ (`RE-067` เปิดอยู่).

### nonclaims
🔴 เก็บข้อมูลดิบ ไม่ใช่พิสูจน์ว่าคำสั่ง GM ทำงาน -- ไม่มี reply frame เลย. 🔴 "หา widget ไม่เจอ" =
NO-RESULT ที่สมบูรณ์ ไม่ใช่ FAIL/BLOCKED (BLOCKED = ด่าน 0/1/2 เท่านั้น). ไม่ตั้ง semantic ให้
`string_0x1c`/`string_0x38`/`field_0x10`/`field_0x14`/`field_0x18` จากสิ่งที่พิมพ์เอง. ไม่ claim ว่า `RE-104`
ถูกตอบแล้ว. ผู้เทสคนเดียว บัญชี GM เดียว เซสชันเดียว (ต่อจาก GT-101 ได้). สำเนา config ลบทิ้งตอน teardown.
ไม่ชี้สาเหตุสีป้ายชื่อ. NO-RESULT ของขั้น 2 จ. ไม่แยก "widget ไม่มีจริง" จาก "รายการที่ลองผิดตัว" -- อาศัย
บันทึกรายการที่ลองครบ (steps) ให้รอบถัดไปแยกเอง.

---

## GT-104 MOB-DEATH-002 WIDEN-DEATH-SCOPE-BG0001-FIRST-WIDENED-KILL-001: โจมตี field-mob ตัวหนึ่งใน bg0001 ที่ไม่ใช่ 0x201F จนถึง 0 HP บนบูตไร้แฟล็ก -- widening ruling ที่เพิ่งต่อสายทำให้ตายจริงบนจอไหม (ไม่ใช่ค้างที่ 0 HP ตลอดกาลแบบก่อนรอบนี้) และของดรอปตามมาปรากฏ/เก็บได้ไหม  [PENDING -- ไม่บล็อก M4 (29 ส.ค. 23:59), งานเสริมหลัง ruling ผ่าน COO]

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md, prefix สองแบบ ห้ามแยกตัวนับ.
> เลขสูงสุดที่ใช้ไปแล้ว ณ เวลาเขียนใบนี้: GT-102 (GAME_TEST_QUEUE.md) และ RE-103 (CLIENT_RE_QUEUE.md,
> ตามที่ erratum ของ RE-103 เองอธิบายไว้ว่าเลขว่างถัดไปคือ 104). grep ยืนยันก่อนจอง: GT-104 = 0 hit,
> RE-104 = 0 hit ทั้งสองไฟล์ (รวม archive/) (ยืนยัน 2026-08-27). ใบเก่าทุกใบอยู่ที่เดิม ไม่ถูกแตะ ไม่ถูกย้าย.

### ที่มา -- อ่านจากซอร์สจริง ห้าม re-derive ระหว่างรอบ
- `src/pirateforce_foundation/mob_death.py` (ก่อนรอบนี้, ที่มาเดิมยืนยันแล้วที่ `GT-084`): `kill()` มี
  `SANCTIONED_FIRST_TARGET_IDENTITY = 0x201F` เดียว (Tornado Eagle) ตัวอื่นทุกตัวใน 13-placement bg0001
  roster ที่ถึง 0 HP จะค้างอยู่ที่นั่น ไม่มีเฟรมตาย ไม่มีวันตาย -- ปฏิเสธด้วย event ชื่อ
  `mob_death_refused_target_outside_the_sanctioned_scope_no_death_frames`.
- รอบนี้: `COO-DECISION 2026-08-27 13:50 +07:00 "widen-death-scope-bg0001-full-roster-approved"` อนุมัติ
  ASK-COO ของ LANE-B (🔴 **หมายเหตุลำดับเวลา ไม่แก้ไขเอง**: เอกสารต้นทางที่ใบนี้ได้รับมาระบุว่า decision เวลา
  13:50 อนุมัติ ASK-COO "จาก 15:00" ซึ่งมาหลัง decision ตามเวลาที่เขียน -- ใบนี้ไม่พยายามสมานความขัดแย้งนี้
  เอง เขียนไว้ตามที่ได้รับมาเป๊ะ ๆ ผู้ใช้ผลใบนี้ควรยืนยันเวลาจริงกับ `notes_to_chief`/`rounds` ต้นฉบับก่อนอ้าง
  ต่อที่อื่น). **LANE-B** ต่อ `WIDENING_RULINGS` entry ใหม่ชื่อ `"COO-RULING-20260827-1350 widen-death-scope-bg0001"`
  เข้า `mob_death.py` เอง (`pirate-force-server#119`, ไฟล์นี้เป็นเขตเขียนของสาย B) ครอบคลุม 10 template id
  ที่ประกอบเป็น 13 placement ของ bg0001 roster (`field_mob_tables.py`): 31 Tornado Eagle (= 0x201F เดิม,
  1 placement), 34 Fighting Fish soldier, 35 Fighting Fish Sergeant, 60 Jungle Big Tiger, 61 Toxic Vine,
  62 Ancient Civilization Alert Weapon, 65 Ward Apes, 94 An Gebo Little Firebird, 97 Mutant Green Eagle
  (4 placements), 103 Orc Chief.
- `src/pirateforce_foundation/runtime.py` (เขตเขียนของ chief คนเดียว, LANE-B เจตนาเว้นไว้ให้): **chief**
  ต่อจุดเรียก production เดียว (single call site) ส่งชื่อ ruling นี้แบบ **unconditional** เข้า
  `mob_death.kill()` -- ไม่มีสวิตช์ ไม่มี `--*-scenario` -- ต่างจากตอน `GT-084` ถูกเขียนที่ยังไม่มีการ
  widen เลย.
- `CORE-REQUEST-007`/`MOB-LOOT-001` (ต่อสายไว้ก่อนรอบนี้แล้ว ไม่ใช่งานของรอบนี้): ทุก kill ที่ "จบจริง"
  (ไม่ว่า sanctioned เดิมหรือ widened ใหม่) มี loot roll ต่อท้ายเสมอ.
- หลักฐานชั้น wire/DB ที่มีอยู่แล้ว **(headless เท่านั้น ไม่ใช่ client)**: `tests/test_mob_combat_dispatch.py`
  สองเทสต์ -- `test_a_killing_blow_on_a_bg0001_roster_identity_now_finishes_a_kill` (พิสูจน์ผ่าน synthetic
  dispatch harness ว่าตี non-sanctioned bg0001 roster identity ลงไปถึง 1 HP แล้วโดนอีกจนถึง 0 HP ผลิตเฟรม
  `MOB_COMBAT_ANNOUNCE -> MOB_DEATH_DYING -> MOB_DEATH_DEAD` (+ `MOB_LOOT_DROP` ถ้ามี) จริง, death register
  จริง, `mob_combat_kill_count` เพิ่มจริง) และ `test_a_killing_blow_on_a_template_no_ruling_names_still_finishes_no_kill`
  (คู่ควบคุมเชิงลบ -- ยืนยันว่า template นอก 10 ตัวนี้ยังถูกปฏิเสธเหมือนเดิม -- widening ไม่ได้เปิดประตูทั้งหมด
  แบบไม่มีขอบเขต). full suite เขียว 3358 ผ่าน 0 พังใหม่ (17 capstone-import collection error เดิมที่ไม่เกี่ยว
  เป็น baseline).
- commit: push แล้วรอ merge — ดู `rounds/R193_mnw8z1_widen-death-scope-bg0001-plus-addendum-v62-item-g.md`
  (pf_bridge) สำหรับคอมมิตจริงและสถานะ merge ณ เวลาที่จะรันใบนี้.
- 🔴 **สถานะ `GT-084`/`GT-084-R2` ณ ตอนเขียนใบนี้**: ทั้งสองใบยังไม่มีรอบ attended จริงปิดผล (`GT-084`
  สถานะล่าสุดคือ `[READY -- merged, ด่านสองชั้นยังต้องผ่านตอนบูต]`) ⇒ **ใบนี้อาจกลายเป็นการสังเกตความตายของ
  field-mob ครั้งแรกในโปรเจกต์บนจอจริง ไม่ว่าจะเป็นเป้า sanctioned เดิม (0x201F) หรือ widened ใหม่** -- ไม่มี
  baseline ภาพอ้างอิงของ "ความตายที่สำเร็จ" ให้เทียบมาก่อนเลย บันทึกสิ่งที่เห็นให้ละเอียดที่สุดโดยไม่ประเมิน
  ว่า "ควรจะเป็นแบบนี้" จากคำทำนายของใบอื่น.

### objective (claim เดียว)
เมื่อผู้เล่นโจมตี field-mob ตัวหนึ่งใน bg0001 ที่ **ไม่ใช่** 0x201F (Tornado Eagle) จนถึง 0 HP บนบูตไร้แฟล็ก --
widening ruling ที่เพิ่งต่อสาย (`WIDENING_RULINGS["COO-RULING-20260827-1350 widen-death-scope-bg0001"]`) ทำให้
การตายจบจริงบนจอ (โมเดลล้ม/มีอนิเมชัน ไม่ใช่ค้างที่ 0 HP ตลอดกาลแบบก่อนรอบนี้) พร้อมของดรอปที่ตามมาจากการตาย
เดียวกันปรากฏและเก็บได้จริงหรือไม่ -- ทั้งชั้น wire (เฟรม `MOB_DEATH_DYING`/`MOB_DEATH_DEAD` + เฟรมของดรอป
แทนที่จะเป็น event ปฏิเสธเดิม) และชั้น client-observable (สิ่งที่ตาเห็นบนจอ). ใบนี้ **ไม่ทดสอบ** มอนสเตอร์ตัวอื่น
ในบรรดา 9 template ที่เหลือ (ต้องเปิดใบแยกต่างหากถ้าต้องการความครอบคลุมเต็มโรสเตอร์ -- หนึ่งใบพิสูจน์หนึ่ง claim)
และ **ไม่ทดสอบ** 0x201F เอง (มันเป็นเป้าที่ sanctioned อยู่แล้วก่อนรอบนี้ -- คนละใบ ดู `GT-084`).

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)
- P1 [เสนอ, หัวใจของใบ] ตีเป้าที่ไม่ใช่ 0x201F จนถึง 0 HP -> คอนโซลพิมพ์ "MOB-DEATH-001 kill: performer
  0x... -> target 0x..." (identity ที่ไม่ใช่ 0x201F) ตามด้วย `[G>] MOB_DEATH_DYING` แล้ว `[G>] MOB_DEATH_DEAD`
  -- **แทนที่จะเป็น** event ปฏิเสธเดิม `mob_death_refused_target_outside_the_sanctioned_scope_no_death_frames`
  ที่เคยเห็นมาตลอดก่อนรอบนี้ -- นี่คือหลักฐานว่า widening ไปถึง runtime จริง ไม่ใช่แค่ผ่าน headless test.
- P2 [เสนอ] ถ้า P1 จริง -- โมเดลล้มลงนอนราบบนจอจริง (ท่าที่ `GT-084` เคยทำนายไว้สำหรับ 0x201F แต่ยังไม่มีใคร
  ยืนยันด้วยตาจริงกับตัวไหนเลยในโปรเจกต์นี้ ณ จุดที่เขียนใบนี้ -- ดูหมายเหตุ "สถานะ GT-084" ใน "ที่มา").
- P3 [เสนอ] ตามด้วยเฟรมของดรอป (`CORE-REQUEST-007`/`MOB-LOOT-001`) ปรากฏในคอนโซล และไอเทมปรากฏบนพื้นใกล้ซาก
  เก็บได้ด้วยท่าเดียวกับที่กลไก pickup ทั่วไปเคยพิสูจน์แล้ว (`GT-060`/`GT-063`/`RE-082`) -- ใบนี้ไม่พิสูจน์
  กลไก pickup ทั่วไปซ้ำ (ดู nonclaims) แค่สังเกตว่ามันทำงานกับ of ที่มาจาก widened kill เหมือนกัน.
- P4 [เสนอ, ตัวหักล้าง] ถ้าตีถึง 0 HP แล้ว event ปฏิเสธเดิมยังขึ้นอยู่
  (`mob_death_refused_target_outside_the_sanctioned_scope_no_death_frames`) ทั้งที่ headless test สองตัว
  ผ่านแล้ว -- แปลว่า call site จริงใน `runtime.py` บน SHA ที่บูตยังไม่ได้ส่งชื่อ ruling
  (`"COO-RULING-20260827-1350 widen-death-scope-bg0001"`) เข้าไปจริง (merge ไม่ครบ/ชื่อ ruling พิมพ์ผิด/
  threading ผิดจุด) -- นี่คือผลลบที่มีค่าที่สุดของใบนี้ ต้องเขียนให้เด่นเท่ากับ PASS พร้อม redirect ให้ diff
  `runtime.py` จริงเทียบ `rounds/R193_mnw8z1_widen-death-scope-bg0001-plus-addendum-v62-item-g.md`.
- P5 [ข้อมูลเสริม, ไม่ตัดสิน pass/fail ของใบนี้เอง] ถ้าเจอมอนสเตอร์ตัวอื่นในโรสเตอร์ 13 ตัวโดยบังเอิญระหว่าง
  เดินทาง (เช่น Mutant Green Eagle ที่มี 4 placement) -- **ไม่ต้องเปลี่ยนเป้าหมายกลางคัน** บันทึกไว้เป็นข้อ
  สังเกตเสริมเท่านั้น (ป้ายชื่อ/สถานะ) เพราะใบนี้ locked เป้าเดียวตาม step 4.

### ก่อนบูต -- ด่าน 0 (สถานะ commit), ด่าน 1 (green boot), ด่าน 2 (grep ยืนยันสาย)

**ด่าน 0 -- สถานะ commit:** เปิด `rounds/R193_mnw8z1_widen-death-scope-bg0001-plus-addendum-v62-item-g.md`
ก่อนเริ่มเพื่ออ่านคอมมิตจริงและสถานะ merge (merge เข้า `main` แล้วหรือยังอยู่บนแบรนช์). ถ้ายัง merge ไม่ครบ --
ใบนี้ **BLOCKED -- รอ merge ไม่ได้รอผู้เทส** ไปทำใบอื่นแล้วกลับมาเช็คภายหลัง (`pf_resolve_green_boot.py`
เดินตาม `origin/main` เท่านั้น เช่นเดียวกับทุกใบอื่นในคิวนี้).

**ด่าน 1 -- resolve commit เขียว:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
รันจากโฟลเดอร์ pf_bridge, exit 0 + `BOOT_COMMIT: <sha>` เท่านั้นถึงบูตได้ (git checkout `<sha>` แบบ detached
HEAD). exit 3 = ห้ามบูต. ห้ามเทียบเลข commit ด้วยตา -- resolver คืนหัวแบรนช์ที่ผ่านเกต ไม่ใช่ merge commit เสมอไป.

**ด่าน 2 -- ยืนยันสายจริงของ `<SHA>` (ห้ามเชื่อชื่อฟังก์ชัน/เลขบรรทัดในเอกสารนี้ ต้อง grep ของจริงเสมอ):**
```
git grep -n "WIDENING_RULINGS" <SHA> -- src/pirateforce_foundation/mob_death.py
git grep -n "COO-RULING-20260827-1350 widen-death-scope-bg0001" <SHA> -- src/pirateforce_foundation/mob_death.py
git grep -n "SANCTIONED_FIRST_TARGET_IDENTITY = 0x201F" <SHA> -- src/pirateforce_foundation/mob_death.py
git grep -n "widen-death-scope-bg0001" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "test_a_killing_blow_on_a_bg0001_roster_identity_now_finishes_a_kill" <SHA> -- tests/test_mob_combat_dispatch.py
git grep -n "test_a_killing_blow_on_a_template_no_ruling_names_still_finishes_no_kill" <SHA> -- tests/test_mob_combat_dispatch.py
```
ต้องได้อย่างน้อย 1 บรรทัดต่อคำสั่งทั้ง 6 คำสั่ง. ขาดข้อใดข้อหนึ่ง = **BLOCKED** -- คอมมิตที่จะบูตยังไม่มี
widening ต่อสายจริง ห้ามบูต ห้ามหาคอมมิตเอง ไปทำใบอื่นแล้วรอ merge.

### db (สำเนาเสมอ ห้ามเปิด canonical, ห้ามแตะ state\play.sqlite3)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-104_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt104.sqlite3
```
- เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง.
- สำเนาใหม่ทุกบูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดเสมอ (X -8553.9473, Y -2579.6890, Z 186.0 ตามที่
  `GT-084`/`GT-101`/`GT-102` ใช้).

### server args (เป๊ะ -- ไม่มี --*-scenario เพราะ call site ทำงานเสมอ ไม่มีสวิตช์)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt104.sqlite3
```
ห้ามมี `--*-scenario` แม้แต่ตัวเดียว, ห้ามพ่วงใบอื่นเข้าบูตนี้. หลักฐานว่าไม่มีแฟล็กจริง เก็บทันทีหลัง
เซิร์ฟเวอร์ขึ้น แปะทั้งบรรทัดลงผล:
```
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List
```

### steps (คลิกต่อคลิก -- อัดวิดีโอต่อเนื่องตลอดช่วงถือ LOCK_GAME)
ก่อนเริ่ม: ถือ LOCK_GAME, จด boot stamp (+07:00, ต้องไม่เก่ากว่า 420 นาทีตอนรัน teardown), เทียบ sha
canonical, copy DB สองใบตามบล็อก db, เตรียม teardown จาก `TEMPLATE_teardown_generic.ps1`. ยืนยันด่าน 0-2
ผ่านครบ (จด SHA ที่บูต + ผลของ 6 คำสั่ง grep).

1. สตาร์ตเซิร์ฟเวอร์ก่อนเสมอ (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด
   client). client ที่บูตโดยไม่มีเซิร์ฟเวอร์ตายเองใน ~3.5 นาที. ถ้าต้องฆ่า client กลางคัน ต้อง restart
   server ก่อนเปิด client ใหม่เสมอ (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่ "connecting" ตลอดกาล).
2. เปิด client -> เลือกเซิร์ฟเวอร์ -> dialog PVP ปุ่มซ้าย -> หน้าเลือกตัวละคร -> เลือกช่องแรก -> ปุ่มกลาง
   สุดจาก 5 ปุ่มแถวล่าง = เข้าเกม (ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด). เริ่มอัดวิดีโอต่อเนื่องตั้งแต่ก่อนกดเข้า
   เกม.
3. T0 -- เห็น HP bar/minimap/ชื่อแมพครบ. จด HUD X/Y. คลิกขวาค้างลากกวาดกล้อง 360 องศาหนึ่งรอบ (ตัวเช็ค
   NO-CRASH ตัวเดียวที่ใบนี้ยอมรับ -- คลิกขวาลากหมุนกล้องอย่างเดียว ทิศหันตัวละครไม่ขยับ ไม่ยิงอะไรออกสาย
   ปลอดภัยเสมอ -- **ห้ามใช้ Q/E เป็นตัวเช็คนี้เด็ดขาด** เพราะ Q/E หันตัวละครจริงและยิง `TargetPosVital`).
4. เปิด `field_mob_tables.py:46-59` ที่ `<SHA>` จริง (บล็อกเดียวกับที่ `GT-084` อ้างไว้แล้ว) แล้วเลือก
   placement ที่ใกล้จุดเกิดที่สุดในบรรดา **12 placement ที่เหลือ (ห้ามเลือก 0x201F Tornado Eagle ที่
   (1747.5244, -7837.6978, 931.0413) -- นั่นคือเป้าที่ sanctioned อยู่แล้ว ไม่ใช่คำถามของใบนี้)**. จดชื่อ
   template/identity/พิกัดที่เลือกไว้ในผลตั้งแต่ต้น. เดินไปทางพิกัดนั้นโดยอ่าน HUD X/Y เทียบทุกช่วง (W/A/S/D
   คาดว่ายิง `TargetPosVital` ทุกครั้งที่ขยับ/หันตัว -- คาดหมายและไม่ใช่ความเสี่ยงของใบนี้). งบเวลาเดินทาง
   20 นาที. ถ้าครบ 20 นาทีแล้วยังไม่เห็น/เลือกโมเดลได้ ให้ลองตัวถัดไปที่ใกล้กว่าในบรรดา 12 ตัวเดียวกัน แล้ว
   จดว่าใช้ตัวไหนและทำไม.
5. เมื่อเห็นโมเดล: single-click เปิดแผงเป้า. ถ่ายภาพนิ่ง full-res ของแผงเป้า + ป้ายชื่อบนหัวมอนสเตอร์ +
   ป้ายชื่อตัวเอง ก่อนโจมตีข้อแรก -- นี่คือภาพที่ต้องบันทึกสีป้ายทุกป้าย.
6. ดับเบิลคลิกโมเดลเดิมเพื่อโจมตี. หลังดับเบิลคลิกแต่ละครั้ง จด (ก) บรรทัดคอนโซลเซิร์ฟเวอร์ทั้งหมดที่ขึ้น
   ใหม่ ("MOB-COMBAT-001 hit" + `[G>] MOB_COMBAT_ANNOUNCE`/`MOB_COMBAT_BAR`) (ข) สิ่งที่เห็นบนจอ (เลขดาเมจ
   ลอย, หลอด/เลข HP บนแผงเป้า). ทำซ้ำจนมอนสเตอร์ถึง 0 HP หรือครบ 10 หมัด (กันเวลาไม่จบ) แล้วแต่อย่างไหน
   ถึงก่อน.
7. ถ้าถึง 0 HP: เฝ้าดู 5 วินาทีถัดไป จดว่ามีอนิเมชัน/ท่าล้มไหม, มีบรรทัด `MOB-DEATH-001 kill` +
   `MOB_DEATH_DYING`/`MOB_DEATH_DEAD` หรือ event ปฏิเสธเดิมขึ้นแทน. ถ่ายภาพนิ่ง full-res ของโมเดลหลังถึง
   0 HP + ป้ายชื่อ (ถ้ายังอ่านได้). จากนั้นเฝ้าดูอีก 10 วินาทีว่ามีเฟรม/บรรทัดของดรอปตามมาไหม -- ถ้ามีของ
   ปรากฏบนพื้น ถ่ายภาพนิ่ง full-res แล้วลองเก็บด้วยท่าเดียวกับที่ `GT-060`/`GT-063` เคยใช้ (คลิกซ้ายบน
   วัตถุ) จดว่าเก็บสำเร็จไหม (ไอเทมหายจากพื้น/ขึ้นในกระเป๋าหรือไม่).
8. NO-CRASH check ซ้ำ: คลิกขวาลากอีกครั้ง -- ยืนยันไคลเอนต์ยังตอบสนอง.
9. ออกเกม -> teardown ตาม `TEMPLATE_teardown_generic.ps1` -> เทียบ sha canonical รอบสุดท้าย.

### pass criteria (สองชั้น แยกกันเสมอ ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)

ชั้น wire/DB (อ่านจาก server console/event log ล้วน ๆ ไม่ต้องพึ่งสิ่งที่เห็นบนจอ):
- หลักฐาน headless ที่มีอยู่แล้ว (บริบทที่ใบนี้ต่อยอด ไม่ใช่หลักฐานของรอบ attended นี้เอง): เทสต์
  `test_a_killing_blow_on_a_bg0001_roster_identity_now_finishes_a_kill` และ
  `test_a_killing_blow_on_a_template_no_ruling_names_still_finishes_no_kill` (`tests/test_mob_combat_dispatch.py`)
  ผ่านแล้วบนคอมมิตที่ `rounds/R193_mnw8z1_widen-death-scope-bg0001-plus-addendum-v62-item-g.md` อ้างถึง,
  full suite 3358 ผ่าน 0 พังใหม่.
- อย่างน้อยหนึ่งดับเบิลคลิกที่ลงบนโมเดลเป้าหมาย (ไม่ใช่ 0x201F) ทำให้คอนโซลพิมพ์บรรทัด "MOB-COMBAT-001 hit"
  + `[G>] MOB_COMBAT_ANNOUNCE`/`MOB_COMBAT_BAR`.
- เมื่อถึง 0 HP: บรรทัด "MOB-DEATH-001 kill: performer 0x... -> target 0x..." (identity ที่ไม่ใช่ 0x201F)
  + `[G>] MOB_DEATH_DYING` แล้ว `[G>] MOB_DEATH_DEAD` ปรากฏ **แทนที่** event ปฏิเสธเดิม
  `mob_death_refused_target_outside_the_sanctioned_scope_no_death_frames`.
- เฟรม/บรรทัดของดรอป (`CORE-REQUEST-007`/`MOB-LOOT-001`) ปรากฏตามหลังเฟรมตาย.
- `sessions`: `count(*) WHERE selected_character_id IS NOT NULL` +1 ต่อการเข้าเกมหนึ่งครั้ง, `max(lease_
  generation)` ไม่ถอยหลัง, `PRAGMA integrity_check` = `ok` บนสำเนา, sha256 canonical ก่อน-หลังตรงกับ
  `CANON_SHA.txt` ทั้งสองครั้ง.
- raw GAME log ทั้งไฟล์ + console out/err เก็บทั้งก่อน/หลัง ไม่ตัดทอน.
- 🔴 **ผลลบที่สมบูรณ์เท่ากับ PASS**: ตีเป้าที่ไม่ใช่ 0x201F ลงถึง 0 HP แล้ว event ปฏิเสธเดิมยังขึ้นอยู่
  (ไม่มี `MOB_DEATH_DYING`/`MOB_DEATH_DEAD` เลย) ⇒ เขียนเป็นผลลบเต็มรูป พร้อมบรรทัดคอนโซลทั้งหมดที่ขึ้นแทน
  เพื่อช่วยชี้ว่า widening ไม่ถึง runtime จริงบน SHA นี้ (ดู P4).

ชั้น client-observable (ต้องมีคนหน้าจอ, ห้ามอนุมานจากบรรทัดคอนโซล):
- เลขดาเมจสีแดงลอยเหนือหัวมอนสเตอร์หลังดับเบิลคลิกแต่ละครั้ง, หลอด/เลข HP บนแผงเป้าลดลงตามลำดับ.
- ถ้าถึง 0 HP: โมเดลล้มลง/เล่นอนิเมชันตายบนจอจริง (ไม่ใช่ยืนนิ่งค้างที่หลอด/เลข 0 หรือค่าสุดท้ายก่อนตายแบบ
  ที่ทุกมอนสเตอร์นอกเหนือ 0x201F เคยทำก่อนรอบนี้) -- **หรือถ้ายังค้างเหมือนเดิม ก็เป็นผลลบที่มีค่าเท่ากัน**
  ตราบใดที่ตรงกับสิ่งที่ชั้น wire รายงานไว้ (event ปฏิเสธยังขึ้นอยู่) -- อย่าตัดสินแยกจากชั้น wire.
- ของดรอปปรากฏให้เห็นบนพื้นใกล้ซาก (หรือไม่ปรากฏ -- ทั้งสองผลมีค่าเท่ากันถ้าตรงกับที่ชั้น wire รายงานไว้)
  และถ้าปรากฏ: ลองเก็บแล้วบันทึกว่าสำเร็จ/ไม่สำเร็จ (ไอเทมหายจากพื้น และ/หรือขึ้นในกระเป๋าที่เห็นได้จริง
  บนจอ).
- สีของป้ายชื่อทุกป้ายในทุกภาพนิ่ง full-res (ป้ายมอนสเตอร์ก่อน/หลังตาย, ป้ายตัวเอง, ป้ายของดรอปถ้ามี) บันทึก
  เป็นบรรทัดเดียวต่อป้ายต่อภาพ ("none" เขียนออกมาถ้าไม่มี ห้ามเว้นว่าง) -- อ่านจากภาพนิ่ง full-res เท่านั้น
  ห้ามอ่านจาก contact sheet/ภาพย่อ/วิดีโอ ห้ามอนุมานสาเหตุของสี (`RE-067` เปิดอยู่). ไม่มีภาพอ้างอิงของ
  เซิร์ฟเวอร์ต้นฉบับที่รู้จักสำหรับมอนสเตอร์ตัวนี้โดยเฉพาะ ณ ตอนเขียนใบนี้ -- ใช้
  `compared_and_matched=no-reference` ถ้าไม่มีภาพอ้างอิงจริง ๆ.
- 🔴 **G-OBS บังคับ**: จดหมายผลของใบนี้ต้องมีบรรทัด `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ตัวอักษร
  เป๊ะ ก่อน chief จะบริโภคเป็นผลปิดใบได้ (กติกาเดิมของทั้งไฟล์นี้ที่หัวไฟล์) -- ถ้ารันครบ หลักฐานครบ แต่ขาด
  ลายเซ็นตาคนอย่างเดียว ให้ใช้สถานะ `AWAITING-OBSERVER` แทน `PENDING`/`PASS`.

### nonclaims
- ใบนี้พิสูจน์แค่ **หนึ่ง** template จากบรรดา 9 template ที่ไม่ใช่ 0x201F -- ไม่ครอบคลุมทั้ง 10 template/13
  placement ของ ruling นี้ -- ถ้าต้องการความครอบคลุมเต็มโรสเตอร์ ต้องเปิดใบเพิ่มทีละใบ (หนึ่งใบพิสูจน์หนึ่ง
  claim).
- ใบนี้ไม่ทดสอบ 0x201F เอง (คนละใบ ดู `GT-084`) และไม่ทดสอบว่า widening "ปิดประตูถูกที่" สำหรับ template
  นอกรายการ 10 ตัว -- คำถามนั้นปิดแล้วที่ชั้น headless โดย
  `test_a_killing_blow_on_a_template_no_ruling_names_still_finishes_no_kill` และไม่มี field mob นอก
  roster ให้คลิกใน bg0001 อยู่แล้ว (roster ครอบทั้ง 13 placement) จึงไม่มีทางทดซ้ำที่ชั้น client ได้จริง.
- ใบนี้ไม่พิสูจน์ความถูกต้องของตาราง loot (ไอเทม/อัตราดรอปที่ "ควร" ออกจากมอนสเตอร์ตัวนี้) -- แค่สังเกตว่า
  มีของดรอปปรากฏและเก็บได้หรือไม่เท่านั้น.
- ใบนี้ไม่พิสูจน์กลไก pickup ทั่วไปซ้ำ -- นั่นคือขอบเขตของ `GT-060`/`GT-063`/`RE-082` ที่ปิดไปแล้ว ใบนี้แค่
  สังเกตว่ามันทำงานกับของที่มาจาก widened kill เหมือนกันหรือไม่.
- ใบนี้พิสูจน์แค่ผู้เล่นคนเดียวที่ต่ออยู่ -- ไม่ทดสอบสองผู้เล่นตีมอนสเตอร์ตัวเดียวกันพร้อมกัน, ไม่ทดสอบ
  aggro/threat (dispatch ส่ง aggro handle เป็น None เสมอในบูตนี้ตามที่ `GT-084` บันทึกไว้), ไม่ทดสอบว่าซาก
  ยังอยู่ทนข้าม reconnect/census rebuild (claim แยก).
- 🔴 **ใบนี้ไม่บล็อกกำหนดส่ง M4 (29 ส.ค. 23:59)** -- widening นี้เป็นงานเสริมที่ COO อนุมัติแล้วต่างหาก
  พร้อมทดสอบได้ทันทีที่ผู้เทสมีเวลา ไม่ใช่ประตูของ milestone ใด ๆ ที่กำลังจะถึงกำหนด.
- ไม่ชี้สาเหตุของสีป้ายชื่อ (`RE-067` เปิดอยู่).
- ถ้าด่าน 0/1/2 ไปไม่ถึง (ยังไม่ merge/BLOCKED) => ทั้งใบเป็น "รอ merge"/BLOCKED ไม่ใช่ NO-RESULT/FAIL --
  ยังไม่ได้ล็อกอินเลย.
- 🔴 ชื่อฟังก์ชัน/ตัวแปร/event ที่ใช้ในใบนี้ (ด่าน 2, pass criteria) เป็นค่าที่สรุปจากคำอธิบายที่ chief ได้รับ
  มา ผู้เทสต้อง grep ของจริงที่ด่าน 2 เสมอ ห้ามเชื่อถ้อยคำในใบนี้แทนซอร์ส.

### result (ผู้เทสกรอก)
```

```

---

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

---

## GT-107 GM-001-R2 LOGIN-STATE-VISUAL-PROBE-002: ล็อกอินด้วยบัญชี GM อีกครั้งหลัง RE-105 พิน vital_version=0 (CORE-REQUEST-016 เปิดแล้ว) -- เซสชันรอดจาก error 23065 ที่ GT-101 เจอไหม แล้วจอเปลี่ยนอะไรไหม (คำถามเดิมของ GT-101 ที่ยังไม่มีใครตอบได้เพราะเซสชันตายก่อนถึง)  [RESULT -- NEGATIVE, new failure mode, error 28317, see notes_to_chief/20260827_1745_GT107-RESULT-NEGATIVE-vital-version-0-passes-version-check-but-client-throws-28317-RunTimeProtocolRes-read-failed-session-dies-GT103-not-reached-ka1-B.md -- superseded by GT-107-R3 below]

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md. grep ยืนยันก่อนจอง (2026-08-27): GT-107 = 0 hit, RE-107 = 0
> hit ทั้งสองไฟล์ (รวม archive/). เลขสูงสุดที่ใช้แล้วจริงคือ GT-106 (SCENE17-PROVISIONAL-ARRIVAL-001, เปิดโดย
> chief รอบ e0daaa) และ RE-106 (QUEST-FLAG-SYNC-MECHANISM-001, เปิดโดย chief คนละสาย) -- ทั้งสองใบไม่ว่าง ⇒
> 106 ใช้ไม่ได้ ใบนี้คือ 107. เปิดโดย pf-queue-author ตามคำขอ LANE-GM รอบ kcm8ir. ใบเก่าทุกใบอยู่ที่เดิม ห้ามแตะ.

### ที่มา -- อ่านจากซอร์สจริง ห้าม re-derive ระหว่างรอบ
- `GT-101` เอง (ผลจริง `notes_to_chief/20260827_1445_GT101-RESULT-client-rejects-0x5A19-version-1-error-23065-session-killed.md`,
  OBSERVER_CONFIRMED 2026-08-27T14:39+07:00): ส่ง `GM_UpdateGMStateVital` (`0x5A19`) ด้วย `vital_version=1`
  ทำให้ไคลเอนต์ขึ้น modal error "網路 VitalData 版本不對 --- ErrorData=23065" (23065 = 0x5A19) แล้วหยุดรับ
  ข้อมูล/ปิด socket เอง -- **ฆ่าเซสชันของเจ้าของเอง** ก่อนที่คำถามเดิมของ GM-001 ("จอเปลี่ยนอะไรไหม") จะถูกตอบ.
- `RE-105-RESULT` (`notes_to_chief/20260827_1613_RE-105-RESULT-VITAL-VERSION-ZERO-GENERIC-MISMATCH-PATH.md`,
  STATIC-ON-BRIDGE, DONE/PASS): generic VitalData collection reader `[0x005F3E20,0x005F406D)` เทียบ nested
  version แบบ exact-equality กับ `message+0x10`; bootstrap ของ `0x5A19` เอง (`0x007299B0`) เซ็ตค่านั้นเป็น `0`
  โดยตรง (`mov byte ptr [eax+0x10],bl` หลัง `xor ebx,ebx`) -- **`vital_version` ที่ถูกคือ `0` เท่านั้น**, ค่า `1`
  ที่ GT-101 วัดว่าฆ่าเซสชันคือค่าที่ตกทาง mismatch เดียวกันนี้เอง. `08 04` (outer `GSCN_RunTimeProtocolRes`
  protocol version 4) เป็นคนละฟิลด์ ไม่เกี่ยวกับสาเหตุ.
- รอบ `kcm8ir` (`rounds/GM_20260827_1614_re105-vital-version-pin-plus-re104-widget-trigger-close.md`):
  `src/pirateforce_foundation/gm/state_wire.py`'s `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED` เปลี่ยนจาก `None`
  เป็น `0` จุดเดียว -- **ไม่แตะ `runtime.py`** เพราะ guard ของ `CORE-REQUEST-016` (`runtime.py`, เงื่อนไข
  `is_gm and state_wire.GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED is not None`) เปิดเองทันทีที่ค่านี้ไม่ใช่
  `None` อีกต่อไป. เทสใหม่ `tests/test_gm_login_state_guard.py` (`GmLoginStateGuardTests`, 3 เทส) ยืนยันผ่าน
  headless dispatcher จริงว่าเฟรมที่ประกอบมี `b"\x12\x19\x5a\x0b\x00"` (ไบต์เดียวที่ GT-101 พิสูจน์ว่าฆ่าเซสชัน
  ตอนเป็น `0B 01`) และไม่มี `b"\x12\x19\x5a\x0b\x01"` เลย, `08 04` (outer protocol version) ไม่เปลี่ยน, บัญชี
  ไม่ใช่ GM ไม่ได้รับผลกระทบ, และ guard เป็นเงื่อนไขจริง (patch ค่ากลับ `None` แล้วเฟรมถูก withhold เหมือนเดิม
  ด้วย event `gm_update_state_frame_withheld_no_confirmed_vital_version_re105_open`). `tests/test_gm_*.py`
  206/206 ผ่าน, repo เต็ม (`unittest discover`) 3565 เทส ผ่านหมดยกเว้น 18 error เดิมจาก `capstone` import ที่
  ไม่เกี่ยวกับสายนี้ (baseline เดิม ไม่ใช่ของรอบนี้).
- `RE-104-RESULT` (`notes_to_chief/20260827_1518_RE-104-RESULT-BT-GM-MODULE-PLUS19-GATE.md`, PASS/DONE):
  พิสูจน์ trigger ของ dedicated GM editor widget (ปุ่ม `BT_GM` → panel `GMUI_BASIC`) -- **คนละคำถามกับใบนี้**
  ใบนี้ไม่เปิด/ทดสอบ widget นั้นเลย (นั่นคือขอบเขตของ `GT-103` ที่อัปเดตแล้วแยกต่างหาก).
- 🔴 **ใบนี้คือ byte-level regression check ของ GT-101 เท่านั้น ไม่ใช่การสำรวจใหม่.** RE-105/เทสใหม่พิสูจน์แค่
  ระดับ headless dispatcher -- **เวอร์ชัน 0 ไม่เคยถูกยิงใส่ไคลเอนต์จริงเลยสักครั้ง** (คำของ LANE-GM STATUS เอง,
  `notes_to_chief/20260827_1614_LANE-GM-STATUS-re104-re105-closed-vital-version-pinned.md` §"เกณฑ์สองชั้น":
  wire/DB = PASS headless, client-observable = ยังไม่มี). ใบนี้คือก้าวที่ปิดช่องว่างนั้น.

### ก่อนบูต -- ด่าน 0 (ชื่อบัญชี GM -- ห้ามเดา, สองแหล่งขัดกัน ต้องถามก่อน), ด่าน 1 (green boot), ด่าน 2 (grep ยืนยันสาย)

**ด่าน 0 -- ชื่อบัญชี:** สองแหล่งไม่ตรงกัน ใบนี้ไม่เลือกแทน:
  (A) `notes_to_chief/20260827_1200_CHIEF-REPLY-GT101-gm-accounts-test-config-approved.md` -- chief อนุมัติ
      ชื่อ **`attended_test`** (ชื่อ fixture ใน `tests/test_gm_accounts.py` เท่านั้น).
  (B) `GT-101` เอง (ผลจริง, บูต `2217fa47`): `attended_test` ใช้ไม่ได้จริง (ไม่มี client login ตัวไหนส่งชื่อนี้
      ⇒ `is_gm_account()` คืน `False` เสมอ) -- รอบนั้นใช้ **`localtest`** จริง (บัญชีจริงในตาราง `accounts` ที่มี
      ตัวละคร `Arena01`) แล้ว `is_gm_account("localtest")` คืน `True` จริง เฟรมถูกคิวจริง. ผลของ GT-101 เองเขียน
      ไว้ตรง ๆ ว่า chief ควรแก้จดหมาย `1200` -- **แต่ ณ ตอนเขียนใบนี้ยังไม่มีจดหมายแก้ไขอย่างเป็นทางการ** (จดหมาย
      เป็นบันทึกจุดเวลา ไม่ถูกแก้ย้อนหลังตามธรรมเนียมของคิวนี้).
  **ก่อนบูต ต้องถาม chief/เจ้าของตรง ๆ ว่ารอบนี้จะใช้ชื่อไหน** -- ถ้าไม่มีคำตอบใหม่ให้ยึด (B) เพราะเป็นชื่อบัญชี
  จริงเพียงชื่อเดียวที่พิสูจน์แล้วว่า login ได้จริงและติด GM gate จริง (แนบเหตุผลนี้ไปกับคำถามที่ถาม ไม่ตัดสินใจ
  เงียบ ๆ). config เดิมของ GT-101 ถูกลบทิ้งไปแล้วตอน teardown -- ต้องสร้างสำเนาใหม่เสมอ ไม่มีของเก่าให้ใช้ซ้ำ:
  ```
  '{"gm_accounts": ["<ชื่อที่ยืนยันแล้ว>"]}' | Set-Content pf_bridge\backup\gm_accounts_GT-107_<yyyyMMdd_HHmmss>.json
  ```
  **ห้ามแก้ `config/gm_accounts.json` ตัวจริง** -- ใช้ `$env:PF_GM_ACCOUNTS_CONFIG` ชี้ไปที่สำเนาเสมอ (ทาง B เดิม
  ของ GT-101, `gm/accounts.py`'s `ENV_OVERRIDE`). จดชื่อบัญชีที่ยืนยัน + path สำเนาไว้ในผลตั้งแต่ต้น ลบสำเนา/
  เลิกตั้ง env ตอน teardown.

**ด่าน 1 -- resolve commit เขียว:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
รันจากโฟลเดอร์ pf_bridge, exit 0 + `BOOT_COMMIT: <sha>` เท่านั้นถึงบูตได้ (git checkout `<sha>` แบบ detached
HEAD). ห้ามเทียบเลข commit ด้วยตา -- resolver คืนหัวแบรนช์ที่ผ่านเกต ไม่ใช่ merge commit เสมอไป.

**ด่าน 2 -- ยืนยันสายจริงของ `<SHA>` (ห้ามเชื่อเลขบรรทัด/ไบต์ในเอกสารนี้ ต้อง grep ของจริงเสมอ):**
```
git grep -n "GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED = 0" <SHA> -- src/pirateforce_foundation/gm/state_wire.py
git grep -n "state_wire.GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "gm_update_state_frame_withheld_no_confirmed_" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "make_gm_update_state_frame" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "is_gm_account(self.token)" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "test_a_gm_account_gets_the_re105_pinned_state_frame" <SHA> -- tests/test_gm_login_state_guard.py
```
ต้องได้อย่างน้อย 1 บรรทัดต่อคำสั่งทั้ง 6 คำสั่ง, และบรรทัดแรกต้องคืน `= 0` ตรงตัว (ไม่ใช่ `= None`) -- ถ้าเป็น
`None` แปลว่าคอมมิตที่จะบูตยังไม่มีการแก้จริง = **BLOCKED**, ห้ามบูต, ไปทำใบอื่นแล้วรอ merge.

### db (สำเนาเสมอ ห้ามเปิด canonical, ห้ามแตะ state\play.sqlite3)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-107_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt107.sqlite3
```
เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง. สำเนาใหม่ทุกบูต ⇒
ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดเสมอ (คาดหมายอยู่แล้ว ไม่ใช่ผลของใบนี้).

### server args (เป๊ะ -- ไม่มี --*-scenario, guard ทำงานเสมอไม่มีสวิตช์, ไม่มี chat trigger ในใบนี้เลย)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
$env:PF_GM_ACCOUNTS_CONFIG = "<path จากด่าน 0>"
py -3 -u -m pirateforce_foundation.app --db state\run_gt107.sqlite3
```

### steps (คลิกต่อคลิก -- อัดวิดีโอต่อเนื่องตลอดช่วงถือ LOCK_GAME)
ก่อนเริ่ม: ถือ LOCK_GAME, สำรอง state (บล็อก db ด้านบน), จด boot stamp (+07:00, ต้องไม่เก่ากว่า 420 นาทีตอนรัน
teardown), เทียบ sha canonical, ยืนยันด่าน 0-2 ผ่านครบ (จดชื่อบัญชี + path config + SHA ที่บูต).
🔴 **เตรียมใจไว้ก่อนคลิกเข้าเกม: modal error 23065 เดิมของ GT-101 อาจเกิดซ้ำได้จริง** ถ้า RE-105/การแก้รอบนี้ผิด
ที่ใดก็ตาม -- นี่ไม่ใช่ FAIL ของใบนี้ เป็นผลลบที่มีค่าเท่ากับผลบวก (ดู pass criteria). ถ้าเกิดซ้ำ: กด OK ปิด
dialog ตามปกติ, **restart server ก่อนเปิด client ใหม่เสมอ** (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่
"connecting" ตลอดกาลถ้าไม่ restart ก่อน), แล้วหยุดที่ตรงนั้น เขียนผลแบบ RESULT เหมือน GT-101 ไม่ต้องพยายามต่อ.

1. สตาร์ตเซิร์ฟเวอร์ก่อนเสมอ (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client).
   client ที่บูตโดยไม่มีเซิร์ฟเวอร์ตายเองใน ~3.5 นาที.
2. เปิด client -> เลือกเซิร์ฟเวอร์ -> dialog PVP ปุ่มซ้าย -> หน้าเลือกตัวละคร -> เลือกช่องแรกของบัญชี GM ที่
   ยืนยันในด่าน 0 -> ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม (ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด). เริ่มอัดวิดีโอ
   ต่อเนื่องตั้งแต่ก่อนกดเข้าเกม.
3. **ด่านชี้ขาดของใบนี้ (ใหม่ ไม่มีใน GT-101):** จ้องจอตั้งแต่วินาทีที่หน้าโหลดจบทันที 10 วินาทีเต็มก่อนทำอะไร
   ต่อ -- มี modal error กลางจอ (ข้อความจีนขึ้นต้น "網路 VitalData") ขึ้นไหม. ถ่ายภาพนิ่ง full-res ทันทีถ้าเห็น.
   ขึ้น -> ทำตามคำเตือนด้านบน (restart server, เขียนผล RESULT, จบใบ). ไม่ขึ้น -> ไปข้อ 4 เหมือน GT-101 เดิม.
4. T0 -- เห็น HP bar/minimap/ชื่อแมพครบ. จด HUD X/Y. คลิกขวาค้างลากกวาดกล้อง 360 องศาหนึ่งรอบ (ตัวเช็ค NO-CRASH
   ตัวเดียวที่ใบนี้ยอมรับ -- **ห้ามใช้ Q/E เด็ดขาด** เพราะ Q/E หันตัวละครจริงและยิง `TargetPosVital`; คลิกขวาลาก
   หมุนกล้องอย่างเดียว ทิศหันตัวละครไม่ขยับ ไม่ยิงอะไรออกสาย ปลอดภัยเสมอ). ใบนี้ไม่มีขั้นเดิน/โจมตี/trigger ใด ๆ
   เลย ⇒ ไม่จำเป็นต้องใช้ W/A/S/D หรือ Q/E ตลอดรอบ.
5. เฝ้าจอต่อเนื่องอย่างน้อย 5 นาทีนับจาก T0 (โปรโตคอลเดิมของ GT-101 ทั้งหมด) -- ถ่ายภาพนิ่ง full-res ที่ t=0s,
   30s, 120s, 300s เป็นอย่างน้อย และเพิ่มทันทีที่เห็นอะไรเปลี่ยนแม้เล็กน้อย. กวาดตาดูทุกจุด: ป้ายชื่อเหนือหัว
   ตัวเอง, แผงสถานะ/HP มุมซ้าย, แผงเป้า (ถ้ามี), หน้าต่างแชท+prefix ชื่อตัวเอง, แถบไอคอน/เมนูบนสุด, minimap,
   มุมจอทุกมุม.
6. คู่ขนานกับข้อ 5: เฝ้าคอนโซลเซิร์ฟเวอร์ -- คัด `[G>] GM_UPDATE_STATE_AFTER_LOGIN`, `gm_account_lookup_failed_*`
   (ถ้ามี = config พัง, หยุดแล้วเขียน BLOCKED ไม่ใช่ NO-RESULT), และเช็คว่าไม่มี `[G!] game socket closed/reset`
   โผล่ก่อนครบ 5 นาที.
7. ครบ 5 นาทีแล้ว: คลิกขวาลากอีกครั้ง (NO-CRASH ซ้ำ) -- ยืนยันไคลเอนต์ยังตอบสนอง.
8. ออกเกม -> teardown ตาม `TEMPLATE_teardown_generic.ps1` -> เทียบ sha canonical รอบสุดท้าย -> ลบสำเนา config/
   เลิกตั้ง `$env:PF_GM_ACCOUNTS_CONFIG`.

### pass criteria (สองชั้น แยกกันเสมอ ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)

ชั้น wire/DB (อ่านจาก server console/event log ล้วน ๆ ไม่ต้องพึ่งสิ่งที่เห็นบนจอ):
- คอนโซลพิมพ์ `[G>] GM_UPDATE_STATE_AFTER_LOGIN (N bytes)` หนึ่งครั้งตอนล็อกอินสำเร็จ, ไม่มี
  `gm_account_lookup_failed_*` เลย.
- 🔮 **คำทำนาย (ยังไม่เคยยิงใส่ไคลเอนต์จริง, ผิดได้ = ผล ไม่ใช่ความล้มเหลว):** ไบต์บนสายของเฟรมนี้ตรง
  `... 08 04 0B 02 12 01 00 12 19 5A 0B 00 0B 00 0B 00 14 00 00 00 00` (เหมือนไบต์จริงที่ GT-101 จับได้เป๊ะ
  ยกเว้นไบต์เดียวหลัง `12 19 5A` เปลี่ยนจาก `0B 01` เป็น `0B 00` ตามที่ RE-105/เทส `test_gm_login_state_guard.py`
  พิสูจน์แล้วที่ชั้น headless) -- ถ้าคอนโซลมี hex dump ให้เทียบตรงนี้, ถ้าไม่มีก็ข้ามข้อนี้ไปดูแค่ N bytes.
- ไม่มีบรรทัด `[G!] game socket closed/reset` โผล่ก่อนครบ 5 นาทีจาก T0 (สัญญาณทางสาย ทางอ้อม ของการที่ session
  ไม่ตายกลางคัน -- แยกจากการเห็น modal บนจอ ซึ่งเป็นชั้น client-observable คนละชั้น).
- `sessions`: `count(*) WHERE selected_character_id IS NOT NULL` +1 ต่อการเข้าเกมหนึ่งครั้ง, `max(lease_
  generation)` ไม่ถอยหลัง, `PRAGMA integrity_check` = `ok` บนสำเนา, sha256 canonical ก่อน-หลังตรงกับ
  `CANON_SHA.txt` ทั้งสองครั้ง.
- raw GAME log ทั้งไฟล์ + console out/err เก็บทั้งก่อน/หลัง ไม่ตัดทอน.

ชั้น client-observable (ต้องมีคนหน้าจอ, ห้ามอนุมานจากบรรทัดคอนโซล):
- 🔴 **สามผลลัพธ์ต่อไปนี้ทุกอันมีค่าเท่ากัน ไม่ใช่เกณฑ์ผ่าน/ตกของใบนี้ (เหมือน GT-101 บวกผลที่สาม):**
  (ก) **modal error 23065 เดิมขึ้นซ้ำ** -- แปลว่า RE-105/การแก้รอบนี้ยังไม่ปิดสาเหตุจริงบนไคลเอนต์ตัวนี้ ทั้งที่
      headless พิสูจน์แล้ว เขียนเป็นผล RESULT (ไม่ใช่ PASS ไม่ใช่ FAIL) พร้อมภาพ+ไบต์จริงที่จับได้ ตามแบบผลของ
      GT-101 เอง.
  (ข) **ไม่มี modal, login ผ่านปกติ, ไม่เห็นอะไรเปลี่ยนบนจอเลย** ตลอด 5 นาที -- นี่คือผลลบที่ `RE-089` ทำนายไว้
      แล้วว่าเป็นไปได้ (ไม่พบ render/UI consumer ที่ชั้น static) เขียนเป็นผลลบเต็มรูปพร้อมรายการทุกจุดที่ตรวจ
      แล้วว่า "ไม่เปลี่ยน".
  (ค) **ไม่มี modal, login ผ่านปกติ, เห็นอะไรเปลี่ยนจริง** -- ระบุให้ชัดว่าที่ไหน ถ่ายภาพนิ่ง full-res ปิดล้อม
      จุดที่เปลี่ยนทันที -- นี่คือผลบวกที่ตอบคำถามค้างของ `RE-089`/`GT-101` ได้จริงเป็นครั้งแรก.
- สีของป้ายชื่อทุกป้ายในทุกภาพนิ่ง full-res (t=0s/30s/120s/300s และภาพเพิ่มถ้ามี) บันทึกเป็นบรรทัดเดียวต่อป้าย
  ต่อภาพ ("none" เขียนออกมาถ้าไม่มี ห้ามเว้นว่าง) -- อ่านจากภาพนิ่ง full-res เท่านั้น ห้ามอ่านจาก contact
  sheet/ภาพย่อ/วิดีโอ ห้ามอนุมานสาเหตุของสี (`RE-067` เปิดอยู่). ไม่มีภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับสำหรับ GM
  state โดยเฉพาะที่รู้จักตอนนี้ -- ถ้าไม่มีอ้างอิงให้ใช้ `compared_and_matched=no-reference`.

### nonclaims
- 🔴 **ใบนี้เป็น byte-level regression check ของ GT-101 เท่านั้น ไม่ใช่การสำรวจ/ค้นใหม่.** ไม่ทดสอบค่าอื่นของ
  สามฟิลด์ opaque (ยังส่ง `0, 0, 0` ชุดเดิมเหมือน GT-101 เป๊ะ ๆ) และไม่ตั้ง semantic ให้ไบต์ไหนจากสิ่งที่เห็น
  บนจอ (`RE-089` ห้ามการอนุมานนี้จาก offset/ความกว้างไว้แล้ว).
- 🔴 **ใบนี้ไม่พิสูจน์ว่าการแก้ของ RE-105/CORE-REQUEST-016 ถูกต้องที่ชั้นไคลเอนต์จริง** -- headless test พิสูจน์
  แค่ว่า dispatcher ประกอบไบต์ที่ตั้งใจถูกต้อง; **ใบนี้คือรอบแรกที่วัดจริงว่าไคลเอนต์ตัวจริงยอมรับหรือไม่** ถ้า
  modal เดิมขึ้นซ้ำ (ผลลัพธ์ (ก) ข้างบน) นั่นคือคำตอบของใบนี้เอง ไม่ใช่ความล้มเหลวของใบนี้.
- 🔴 **"ไม่เห็นอะไรเปลี่ยนบนจอเลย" (ผลลัพธ์ (ข)) เป็นผลที่คาดไว้แล้วและยอมรับได้เต็มรูป ไม่ใช่ความล้มเหลวของ
  ใบนี้** -- `RE-089` เองพิสูจน์แล้วว่าไม่พบ render/widget/texture consumer ของสามฟิลด์นี้ในโค้ด static ก่อน
  รอบนี้จะเริ่มด้วยซ้ำ.
- ไม่ทดสอบ GM editor widget (`BT_GM`/`GMUI_BASIC`) หรือคำสั่ง GM ใด ๆ เลย -- นั่นคือขอบเขตของ `GT-103`
  (GM-002) คนละใบ, ไม่มีการยิงคำสั่งในใบนี้.
- ไม่ทดสอบผู้เล่นคนอื่นเห็นอะไรต่างไปเกี่ยวกับบัญชี GM นี้, ไม่ทดสอบความเสถียรข้าม reconnect/relogin -- ล็อกอิน
  ครั้งเดียวในรอบนี้.
- ถ้าใช้สำเนา config ตามด่าน 0: ไม่พิสูจน์ว่าการเปลี่ยนแปลงนั้นคงอยู่ข้ามรอบอื่นหรือกระทบเลนอื่น -- สำเนานี้ของ
  รอบนี้เท่านั้น ถูกลบทิ้งตอน teardown.
- ไม่ชี้สาเหตุของสีป้ายชื่อ (`RE-067` เปิดอยู่).
- ถ้าด่าน 0/1/2 ไปไม่ถึง (ยังไม่ merge/BLOCKED/ไม่มีคำตอบชื่อบัญชี) => ทั้งใบเป็น BLOCKED ไม่ใช่ NO-RESULT/FAIL
  -- ยังไม่ได้ล็อกอินเลย.

### result (ผู้เทสกรอก)
```

```

---

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
     login ทั้งครั้งถูกปฏิเสธไม่มี reply เลย (client ค้างที่ "connecting" ตลอดไป) ซึ่งเป็นพฤติกรรม fail-closed
     ที่ตั้งใจ ไม่ใช่บั๊ก แต่เผารอบทดสอบทิ้งเปล่า ๆ ใช้ scene_id=2 (Prison Exile Island, BG0002) แทน: พิสูจน์แล้ว
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

## GT-114 DIAG-MULTI-OBJECT-001 [attended, in-game]: five diagnostic objects at the city-center test point (X=11865, Y=6147), each one field away from control D0 -- does each single-field difference produce the on-screen effect that field is predicted to control, jointly closing the attended half of RE-107/RE-108/RE-109's own proposed follow-ups  [PENDING -- wiring landed R202 (9b6zl6), see server args below. D1b has no death handling this round, see nonclaim (12).]

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
  omitted. `rounds/GM_20260827_1948_re113-trailing-mask-fix-core-request-020-mailbox.md`.
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

## GT-116 CORE-REQUEST-022 CLASS-LEVEL-LOGIN-SKILLWINDOW-UNBLOCK-001: after CORE-REQUEST-022 wires class_id=1 (Gladiator) + level=1 into every login's ActorAttr/BasicAttr frames, does a real client's skill window (K / `Bt_main_Skill`) finally open, and does the wire actually carry those two fields byte-exact -- the one field GT-058/GT-059/GT-064 (all CLOSED, archived) could never get past because class was always 0  [✅ PASS -- ปิดโดย chief round 28jd9c (2026-08-28T09:56+07:00) จากผล attended กะ1-A `20260828_0925_GT116-121-120-RESULT-*.md` · OBSERVER_CONFIRMED: 2026-08-28T09:2x+07:00 (BOOT_COMMIT `98307ae` = main HEAD) · claim เดียว (หน้าต่างสกิลเปิดได้) เท่านั้น: จอเจ้าของ "หน้าต่างสกิลเปิดได้ แต่ยังไม่มีรายการใด ๆ" -- level 1 มี 0 สกิลเป็นเรื่องปกติ ตรงเกณฑ์ P1/P2 เป๊ะ · [ไม่อ้าง] ว่ารายการสกิลของ Gladiator ถูก -- ยังไม่วัด (คนละเรื่อง)]

> NUMBERING NOTE: grep confirmed before reserving -- `GT-116`/`RE-116` = 0 hits in `GAME_TEST_QUEUE.md`,
> `CLIENT_RE_QUEUE.md`, and both `archive/*_closed.md` files (checked this round). Highest number in use
> is `115` (`RE-115` MAPWINDOW-SCENE-NPC-LIST-SOURCE-001, OPEN, unrelated topic -- claimed same round by a
> different lane) => this entry is `116`. Entries `GT-101`-`GT-114`, `GT-107-R3`, and `RE-085`-`RE-115` stay
> exactly where they are, unchanged -- this is a new entry, not a replacement for any of them. `GT-058`
> (CLOSED BOUNDED-NEGATIVE), `GT-059` (CLOSED P2/FALSIFIED), and `GT-064` (CLOSED) are archived, not
> reopened -- per the queue's own archival rule, only PENDING/READY/BLOCKED/RUNNING entries stay live, and
> all three are genuinely closed. This entry supersedes their open question with a new claim, on a new number.

### source (links only -- see cited files for full detail, not re-derived here)
- `notes_to_chief/20260828_0231_CHIEF-REPLY-CORE-REQUEST-022-class-level-wired-name-field-not-touched.md`
  (chief round `9do841`/R203): "class_id = 1 (Gladiator) -- `ActorAttr +0x8C`, mask bit `0x00000001`
  (เดิมไม่เคยส่งเลย, class=0 เสมอ ⇒ หน้าต่างสกิลเปิดไม่ได้ ตรงกับ GT learn-skill ที่ค้าง)" and "level = 1 --
  `BasicAttr +0x5E`, mask bit `0x0002` (เดิมไม่เคยส่งเลย)". Both wired into the flagless production login
  path AND the faction=1 recompose path in the same commit (a runtime length-delta check would otherwise
  fail-closed if only one path got the fields). New functions named in that letter: `player_wire.py`'s
  `make_actor_attr_with_name_and_class` / `make_actor_attr_with_name_class_and_faction`, wired into
  `legacy_bridge.py`'s `LegacyProjector.start_game`. Old functions (`make_actor_attr_with_name`,
  `make_actor_attr_with_basic_faction`) left untouched. Cites `3546 passed, 0 failed` full suite +
  pf-adversary review -- headless evidence, cited not reproduced by this entry.
- `notes_to_chief/20260828_0146_COO-DECISION-boot-character-actorattr-core-request-022-to-chief.md`: opens
  CORE-REQUEST-022, names class+level (+ name-slot fix, see below) as the minimum "สมประกอบ" boot character.
- `notes_to_chief/20260828_0125_PANYA-DECISION-boot-character-must-be-complete-...-ka1-B.md`: **owner's own
  testimony**, from a separate ad-hoc probe fork (never merged, canonical never touched): "GT ที่เทส
  learn skill ก็ติด block มาแล้วเพราะว่าเปิดหน้าต่างสกิลกันไม่ได้ จนตอนนี้เรามารู้แล้วว่าต้องใส่ค่า class
  ก่อนถึงจะเปิดหน้าต่างสกิลได้" -- this is the direct antecedent this entry tests. Same letter's table (③)
  independently pins `x13 = Actor b0 +0x8C u32 class id` and `x2 = Basic +0x5E u16 level`, matching the
  chief-reply's offsets.
- `GT-058` (CLOSED BOUNDED-NEGATIVE), `GT-059` SKILL-ATTR-WINDOW-GATE-001 (CLOSED P2/FALSIFIED: wire-exact
  `CSkillAttr` x3 triggers, window never opened either session), `GT-064`
  SKILL-ATTR-WINDOW-KPRESS-IN-GAP-001 (CLOSED) -- all archived in
  `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md`. None of the three could ever isolate "was it timing,
  was it the wrong trigger, or was the client simply never told it had a class" -- class was 0 in every one
  of those sessions. This entry is the first attended shot with class != 0.
- ✅ **Verified chief round 2y0zil (2026-08-28T09:53+07:00):** branch `claude/awesome-darwin-9do841` /
  commit `8017c71` confirmed on `pirate-force-server` -- `pirate-force-server#162` shows `merged: true`,
  `merged_at: 2026-08-27T19:48:29Z` via the GitHub API, and `git log origin/main` on this round's fresh
  clone shows `8017c71` as an ancestor of HEAD (`08e9f4f Merge pull request #162 ...` -> `8017c71
  CORE-REQUEST-022: send class+level at login...`). No longer unverified; ด่าน 0/1/2 below can boot against
  current `origin/main` directly.

### objective (claim เดียว)
On a completely ordinary, flagless login (no `--*-scenario`), does the client now (a) receive
`class_id=1`/`level=1` byte-exact in its login ActorAttr/BasicAttr frames, and (b) as a direct consequence,
does pressing **K** / clicking `Bt_main_Skill` open an actual skill window for the first time in this
project's history -- instead of the total silence GT-058/059/064 measured every time before. Both layers
are the same claim (wire cause -> client effect), not two claims.

### predictions (a wrong prediction is a finding, not a failure)
- P1 [proposed, the heart of the entry] K / `Bt_main_Skill` after a normal flagless login opens the skill
  window -- something GT-058/059/064 never once observed.
- P2 [proposed, corollary] the window, once open, is not an empty/garbled error panel -- it shows
  Gladiator-plausible content (zero learned skills at level 1 is a perfectly fine result; a broken/garbled
  panel is not).
- P3 [falsifier] K / `Bt_main_Skill` still produces nothing even with class_id=1 + level=1 confirmed on the
  wire -- a real negative, not a failure: it means these two fields are necessary but not sufficient, and
  redirects to the next untested field in the owner's own probe table (③) -- likely `x16`/`x17` (SP /
  remaining status points) or `x18`-`x22` (STR/CON/DEX/INT/PER) -- open a new RE/GT entry naming the next
  candidate rather than re-running this one.

### ก่อนบูต -- ด่าน 0 (สถานะ merge, ยังไม่ merge ณ ตอนเขียนใบ -- ห้ามข้าม), ด่าน 1 (green boot), ด่าน 2 (grep ยืนยันสาย)

**ด่าน 0 -- สถานะ merge:** CORE-REQUEST-022 is reported (chief round `9do841`/R203, `notes_to_chief/
20260828_0231_CHIEF-REPLY-*`) as landed on a branch of `pirate-force-server`, **PR pending, not yet merged
into `main`** at time of writing. `pf_resolve_green_boot.py` follows `origin/main` only -- if the PR has not
merged when the tester runs ด่าน 1, the resolver will not return a commit containing this code (`exit 3`, or
a commit missing `player_wire.py`'s new functions). **The entry stays unbootable** -- record the result as
"รอ merge" and move to another ticket. **Never checkout the branch directly to skip the resolver**, even
with a sha in hand (same rule as every other entry in this queue) -- and never trust the `8017c71` string
above without ด่าน 2 confirming it live, per the source-section warning.

**ด่าน 1 -- resolve commit เขียว:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
Run from the `pf_bridge` folder. Only `exit 0` + a printed `BOOT_COMMIT: <sha>` means bootable (detached
HEAD checkout of `<sha>`). Do not eyeball-compare commit numbers -- the resolver returns whatever gated
branch head is current, not necessarily a merge commit.

**ด่าน 2 -- ยืนยันสายจริงของ `<SHA>` (ห้ามเชื่อเลขบรรทัด/ชื่อฟังก์ชันในเอกสาร ต้อง grep ของจริง):**
```
git grep -n "make_actor_attr_with_name_and_class" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "make_actor_attr_with_name_class_and_faction" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "make_actor_attr_with_name_and_class\|make_actor_attr_with_name_class_and_faction" <SHA> -- src/pirateforce_foundation/legacy_bridge.py
git grep -n "class_id" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "def start_game" <SHA> -- src/pirateforce_foundation/legacy_bridge.py
```
Need at least 1 line from every command. Missing any one = **BLOCKED** -- the commit that would boot does
not actually carry CORE-REQUEST-022 -- do not boot, do not hunt for a different commit yourself, go do
another ticket and come back later.

### db (สำเนาเสมอ ห้ามเปิด canonical, ห้ามแตะ state\play.sqlite3)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-116_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt116.sqlite3
```
- Compare canonical sha256 against `CANON_SHA.txt` both before start and after finish -- must match both
  times.
- Fresh copy every boot => character position resets to spawn every time (same spawn other entries use:
  X -8553.9473, Y -2579.6890, Z 186.0, scene 1 Port Royal), regardless of anything saved from a previous
  session.

### server args (เป๊ะ -- ไม่มี --*-scenario เพราะ CORE-REQUEST-022 ทำงานเสมอ flagless production, ไม่มีสวิตช์)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt116.sqlite3
```
No `--*-scenario` flag of any kind, no other entry piggybacked onto this boot. Capture proof of the bare
command line immediately after the server comes up, paste the full line into the result:
```
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List
```

### steps (click by click -- record continuous video for the whole LOCK_GAME window)
Before start: hold `LOCK_GAME`, note boot stamp (+07:00, must be under 420 min old when teardown runs),
compare canonical sha, copy both DBs per the db block, stage `TEMPLATE_teardown_generic.ps1`. Confirm ด่าน
0-2 all cleared (record the resolved SHA).

1. Start the server first always (`Get-NetTCPConnection -State Established` on ports 10188/10189 must be 0
   before opening the client). A client opened with no server dies on its own in ~3.5 minutes. If the client
   has to be killed mid-session, restart the server before opening the next client -- the server keeps the
   old session, and the next client hangs on "connecting" forever otherwise.
2. Open client -> select server -> PVP dialog left button -> character select -> first slot -> the middle
   of the 5 bottom buttons = enter game (never the leftmost -- that deletes the character). Start continuous
   recording before pressing enter-game.
3. T0 -- HP bar / minimap / map name all visible. Record HUD X/Y. Photograph full-res, name-label colours
   from this still (self, "none" if no other label visible).
4. NO-CRASH check: right-click-drag to sweep the camera 360 degrees once. This is the only liveness check
   this entry accepts -- camera-only, character facing never moves, nothing goes out on the wire, safe at
   any point. **Never use Q/E or W/A/S/D for this check** -- those turn the character and emit
   `TargetPosVital`.
5. Press **K** (or click `Bt_main_Skill` if K does nothing) -- photograph full-res immediately before and
   immediately after. Record every new server console line that appears in the same window.
6. If a window opened: photograph its full content full-res, read/record what it shows character-for-
   character from the still (not from memory). Do not compare it against any expected skill list -- this
   entry does not test content correctness (see nonclaims).
7. Secondary positive control (same move GT-059 used): press **C** to open the `CHARACTER` window,
   photograph, close. This has opened successfully in every prior session even when K didn't -- if C fails
   too, that's a much bigger finding than this entry's own claim, write it up prominently.
8. NO-CRASH check again (right-click-drag).
9. Log out -> teardown via `TEMPLATE_teardown_generic.ps1` (boot stamp must still be under 420 min) ->
   recheck canonical sha256 -> sha256 every capture.

Colour rule (Panya's order, 2026-08-25): one line per label per image, write "none" not blank, full-res
stills only (never a contact sheet or video), never infer a cause -- `RE-067` is open and is the only place
that question lives.

### pass criteria (two layers, never mixed)

wire/DB (read from raw captured frame bytes / server console+log only, never from what's on screen):
- The login/StartGame response's ActorAttr block, at byte offset **+0x8C** relative to that block's start,
  decodes as u32 little-endian **`0x00000001`** (class_id=1), and the frame's own change-mask has bit
  **`0x00000001`** set for that block (previously this field was never sent at all, not merely zero --
  record which of "absent" vs "present-but-zero" the pre-fix baseline actually was if a comparison capture
  exists, otherwise just record what this session shows).
- The same response's BasicAttr block, at offset **+0x5E**, decodes as u16 little-endian **`0x0001`**
  (level=1), with change-mask bit **`0x0002`** set.
- Byte layout reference for locating these offsets inside the captured frame:
  `drafts/CHUNK2_Q1_ACTORATTR_MASK_FINDINGS.md` (pinned 55-field ActorAttr/BasicAttr map).
- `sessions`: +1 row with `selected_character_id` set for this login; `max(lease_generation)` does not go
  backward; `PRAGMA integrity_check` = `ok` on the working copy both times; canonical sha256 matches
  `CANON_SHA.txt` before and after.
- Raw GAME log + console out/err kept whole, not trimmed, both before and after.
- Negative result with equal standing: if class_id/level are still absent or still zero on the wire despite
  ด่าน 0-2 clearing -- write that up in full, it means the merged commit did not do what the letter claims,
  which is itself the finding.

client-observable (a human at the screen only, never inferred from the console):
- Whether the skill window (K / `Bt_main_Skill`) opens at all is the primary reading -- opens (even
  showing zero learned skills) vs. still nothing, both are complete, valid results; write whichever one
  actually happened, do not treat "still nothing" as this entry failing (see P3).
- If it opens: full-res photograph, content transcribed character-for-character from the still.
- `C` / `CHARACTER` window control check per step 7.
- Both NO-CRASH checks pass.
- Name-label colours recorded per the colour rule above, one line per label per full-res still, "none"
  written out where there is none.

### nonclaims
- 🔴 **Does not prove the character-name-slot bug is fixed.** The chief's own reply
  (`...0231_CHIEF-REPLY-...-name-field-not-touched.md`) states the `x37`(`+0x164`, guild-name slot) ->
  `x1`(`+0x28`, real name slot) move was deliberately **not** done this round, pending a second source of RE
  confirmation. **UPDATE 2026-08-28 ~09:xx +07:00, chief round `03d46t`:** CORE-REQUEST-027 now wires this
  move (headless-proven, PR pending merge) -- see `GT-122` for the dedicated attended entry. If GT-116 runs
  before CORE-REQUEST-027 merges, expect the old guild-slot placement per this nonclaim; if it runs after,
  the name should already be correct and GT-122 is the entry that claims/tests it, not this one -- do not
  read either outcome here as this entry's own finding.
- Does not prove "probe base 1" full completeness (movement speed `x7`, HP/MP per `STANDARD_STATUS`, stat
  points `x18`-`x22`, etc. from the owner's own table in `...0125_PANYA-DECISION-...`) -- only `class_id`
  (`x13`) and `level` (`x2`) were wired this round, per the chief reply.
- Does not test or reopen `GT-058`/`GT-059`/`GT-064` -- those stay CLOSED/archived exactly as written. This
  entry answers a related but distinct question (does an ordinary flagless login with class!=0 unblock the
  window) rather than repeating their scenario-driven `CSkillAttr` trigger tests.
- Does not test skill-window **content** correctness (whether the skills shown, if any, actually match a
  level-1 Gladiator's real kit) -- only whether the window opens.
- Does not test the faction=1 / HYP-PF-027 recompose path's client-visible behaviour -- the chief reply
  states headless coverage exists for both paths sharing one length-delta check, cited here, not reproduced.
- Single account, single login, single session -- no reconnect/relogin, no second character, no second
  player observing.
- Does not decide the cause of any name-label colour observed (`RE-067` stays open, no cause inferred).
- If ด่าน 0/1/2 don't clear (PR not merged / functions not found at the resolved SHA) -> the entire entry is
  **BLOCKED**, not NO-RESULT/FAIL -- record it as "รอ merge" and stop.

### result (ผู้เทสกรอก)
```

```

---

## GT-122 CORE-REQUEST-027 NAME-FIELD-GUILD-SLOT-FIX-001: after CORE-REQUEST-027 moves the character's own name off ActorAttr's guild-name slot (`+0x164`, mask bit `0x01000000`, `LABEL_GUILD`) and onto BasicAttr's real name slot (`+0x28`, mask bit `0x0001`, `LABEL_NAME`) -- the guild-slot bug GT-116's own nonclaims section named and CORE-REQUEST-022/023 deliberately left untouched -- does a real client's own nameplate and `CHARACTER` window now show the character's name as a name, with no guild artifact on a freshly-created guildless character [PENDING -- merge confirmed chief round 28jd9c (2026-08-28T09:56+07:00, entry was stale until now -- pf-adversary caught it): `pirate-force-server#187` merged=true via `pull_request_read` method=get (merged_at 2026-08-28T02:28:54Z), commit `5e24e0b` verified an ancestor of `origin/main` HEAD (`9024844`) via `git merge-base --is-ancestor` on this round's fresh fetch. Ready for an attended session. Same handling as GT-116: do not boot until ด่าน 0 clears.]

> NUMBERING NOTE: grep confirmed before reserving -- `GT-122` = 0 hits in `GAME_TEST_QUEUE.md` at time of
> reservation. `RE-122` (`CLIENT_RE_QUEUE.md`) is already in use, filed under the `RE-` prefix for an
> unrelated topic (`PLAYER-STANDARD-STATUS-AND-CHARCREATE-SCORE-VALUES-001`, the still-open MP/STR/CON/DEX/
> INT/PER static probe) -- not this entry, not renamed, not touched here; `GT-` and `RE-` are separate
> counters in separate files, same as `GT-116`/`RE-116` before it. `RE-123`'s own NUMBERING NOTE (round
> `of27sx`, 2026-08-28 ~08:3x+07:00) already lists `GT-101`-`GT-122` alongside `RE-085`-`RE-122` as
> protected/unchanged -- this number was already anticipated before this entry was filed, this is that
> anticipated entry, not a fresh collision. `GT-101`-`GT-121` and `RE-085`-`RE-123` stay exactly where they
> are, unchanged -- this is a new entry, not a replacement for any of them.

### source (links only -- see cited files for full detail, not re-derived here)
- `notes_to_chief/20260828_0125_PANYA-DECISION-boot-character-must-be-complete-min-probe-base-1-plus-name-x1-share-actorattr-probe-to-all-lanes-fix-name-in-guild-slot-ka1-B.md`:
  owner's own live-client probe (row ② item 2, row ③ x1/x37) -- "ชื่อตัวละครที่ปัจจุบันส่งลง
  x37 (+0x164 = LABEL_GUILD ชื่อกิลด์) ต้องย้ายไป x1 -- x37 ต้องว่างสำหรับตัวละครใหม่ (ไม่มีกิลด์)". Table
  row 1 pins `x1 = Basic 0x0001 +0x28 wstring` -> ป้ายล่างสีขาว + หน้าต่าง `CHARACTER`; row 37 pins
  `x37 = ActorAttr b24 +0x164 wstring` -> ชื่อกิลด์ (ควรว่าง) + row 38 (`+0x180` guild-flag byte) -> สีป้าย
  ม่วง(มีกิลด์)/ส้ม(ไม่มี) -- the *flag* byte, not the name field, is what this project's own table says
  drives the purple/orange split; CORE-REQUEST-027 does not touch `+0x180`.
- `notes_to_chief/20260828_0231_CHIEF-REPLY-CORE-REQUEST-022-class-level-wired-name-field-not-touched.md`:
  chief's prior round (`9do841`) deliberately declined to move x1/x37, pending a second independent source
  before touching a field with a prior live-client PASS on it. CORE-REQUEST-027 is the follow-up that answers
  that ask.
- `notes_to_chief/20260828_0912_CHIEF-REPLY-CORE-REQUEST-027-actor-name-slot-wired.md` (chief round `03d46t`,
  this round): `player_wire.py`'s `_make_actor_attr_with_name_and_class` (the real-login-path composer wired
  via `legacy_bridge.py`'s `LegacyProjector.start_game` -- NOT the frozen `make_actor_attr_with_name`/
  `make_actor_attr_with_basic_faction` baseline, left untouched) now writes the name wstring to
  `BasicAttr +0x28` (bit `0x0001`) instead of `ActorAttr +0x164`, and the `ActorAttr` mask literal changed
  `0x01000801` -> `0x00000801` (bit `0x01000000` no longer set at all). Net frame length unchanged. Cited
  headless evidence: full suite `3750 passed, 327 skipped, 0 failed` (skips pre-declared/pinned via
  `tools/pf_pytest_precondition_census.py`), `tools/verify_hypothesis_ledger.py` clean, `pf-adversary` review
  pass before PR. Two golden-hash files re-baselined (`tests/golden/foundation_v1.json`,
  `tests/golden/item_lifecycle_v1.json`) -- only `start_pc`/`start_frame`/`merged_start_pc`/
  `merged_start_frame` keys changed, frozen V141 template path untouched -- cited as blast-radius evidence,
  not reproduced by this entry.
- GT-116's own nonclaims section (see its UPDATE block, this round) already forward-references this entry.

### objective (single claim)
On a completely ordinary, flagless login (no `--*-scenario`), does the character's own name now render in the
correct name slot -- the white nameplate above the character and the `CHARACTER` (`C`) window -- instead of
the guild-name slot, and does the character show no guild artifact (matching a freshly-created character that
has no guild)? Wire cause and client effect are the same claim here, not two entries.

### predictions (a wrong prediction is a finding, not a failure)
- P1 [proposed, the heart of the entry] the nameplate above the character and the `CHARACTER` window both show
  the character's actual own name, transcribed verbatim off a full-res still -- not blank, not garbled, not
  standing in for something else.
- P2 [proposed, corollary] no guild tag/label is visible anywhere on screen for this character, and if the
  `CHARACTER` window has a guild field at all, it reads empty/none -- consistent with a freshly-created
  guildless character.
- P3 [falsifier] the name is missing entirely, garbled, or visibly rendered as if it were a guild
  tag/slot -- a real negative, not a failure: it would mean the fix is wrong or incomplete, and redirects to a
  new RE ticket comparing this session's raw frame bytes against the queue's own pinned ActorAttr/BasicAttr
  mask findings field-by-field rather than re-running this entry. A name-label rendering in guild-styled
  colour (purple, per the owner's own table row 38) is also a P3 finding worth recording, but per the colour
  rule below the tester records the colour only and does not infer that the name-field move caused it -- the
  actual driver per this project's own table is the separate `+0x180` guild-flag byte, untouched by
  CORE-REQUEST-027, and `RE-067` (name-label colour cause) stays open regardless of what this entry sees.

### ก่อนบูต -- ด่าน 0 (สถานะ merge, ยังไม่ merge ณ ตอนเขียนใบ -- ห้ามข้าม), ด่าน 1 (green boot), ด่าน 2 (grep ยืนยันสาย)

**ด่าน 0 -- สถานะ merge:** CORE-REQUEST-027 is reported (chief round `03d46t`) as landed on branch
`claude/jolly-mccarthy-03d46t` of `pirate-force-server`, **PR pending, not yet merged into `main`** at time of
writing. `pf_resolve_green_boot.py` follows `origin/main` only -- if the PR has not merged when the tester
runs ด่าน 1, the resolver will not return a commit containing this code (`exit 3`, or a commit missing
`_make_actor_attr_with_name_and_class`). **The entry stays unbootable** -- record the result as "รอ merge" and
move to another ticket. **Never checkout the branch directly to skip the resolver**, even with a sha in hand,
and never trust any sha string above without ด่าน 2 confirming it live.

**ด่าน 1 -- resolve commit เขียว:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
Run from the `pf_bridge` folder. Only `exit 0` + a printed `BOOT_COMMIT: <sha>` means bootable (detached HEAD
checkout of `<sha>`). Do not eyeball-compare commit numbers.

**ด่าน 2 -- ยืนยันสายจริงของ `<SHA>` (need at least 1 line from every command; missing any one = BLOCKED, do
not boot, do not hunt for a different commit, go do another ticket and come back later):**
```
git grep -n "_make_actor_attr_with_name_and_class" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "0x00000801" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "_make_actor_attr_with_name_and_class" <SHA> -- src/pirateforce_foundation/legacy_bridge.py
git grep -n "def make_actor_attr_with_name\b" <SHA> -- src/pirateforce_foundation/player_wire.py
git grep -n "def start_game" <SHA> -- src/pirateforce_foundation/legacy_bridge.py
```
The fourth command confirms the OLD frozen baseline (`make_actor_attr_with_name`) is still present and
untouched -- if it is gone, more changed than this ticket's description covers, treat as BLOCKED too.

### db (สำเนาเสมอ ห้ามเปิด canonical, ห้ามแตะ state\play.sqlite3)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-122_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt122.sqlite3
```
Compare canonical sha256 against `CANON_SHA.txt` both before start and after finish -- must match both times.
Fresh copy every boot => character position resets to spawn every time (X -8553.9473, Y -2579.6890, Z 186.0,
scene 1 Port Royal), regardless of anything saved from a previous session.

### server args (เป๊ะ -- ไม่มี --*-scenario, production flagless path only)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt122.sqlite3
```
No `--*-scenario` flag of any kind, no other entry piggybacked onto this boot. Capture proof of the bare
command line immediately after the server comes up:
```
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List
```

### steps (click by click -- record continuous video for the whole LOCK_GAME window)
Before start: hold `LOCK_GAME`, note boot stamp (+07:00, must be under 420 min old when teardown runs), compare
canonical sha, copy both DBs per the db block, stage `TEMPLATE_teardown_generic.ps1`. Confirm ด่าน 0-2 all
cleared (record the resolved SHA).

1. Start the server first always (`Get-NetTCPConnection -State Established` on ports 10188/10189 must be 0
   before opening the client). A client opened with no server dies on its own in ~3.5 minutes. If the client
   has to be killed mid-session, restart the server before opening the next client.
2. Open client -> select server -> PVP dialog left button -> character select -> first slot -> the middle of
   the 5 bottom buttons = enter game (never the leftmost -- that deletes the character). Start continuous
   recording before pressing enter-game.
3. T0 -- HP bar / minimap / map name all visible. Photograph full-res immediately.
4. NO-CRASH check: right-click-drag to sweep the camera 360 degrees once. Camera-only, character facing never
   moves, nothing goes out on the wire, safe at any point. **Never use Q/E or W/A/S/D for this check.**
5. Photograph the nameplate above the character full-res, close enough to read it clearly; transcribe the
   text verbatim from the still -- this is the P1 reading.
6. Press **C** to open the `CHARACTER` window; photograph full-res; transcribe the name field shown verbatim,
   and note whether any guild tag/field/label appears anywhere in that window ("none" if none).
7. NO-CRASH check again (right-click-drag).
8. Log out -> teardown via `TEMPLATE_teardown_generic.ps1` (boot stamp must still be under 420 min) -> recheck
   canonical sha256 -> sha256 every capture.

Colour rule (Panya's order, 2026-08-25): one line per label per image, write "none" not blank, full-res stills
only (never a contact sheet or video), never infer a cause -- `RE-067` is open and is the only place that
question lives. Divergences from the original server's screenshots go into `REAL_SERVER_DIVERGENCE.tsv`.

### pass criteria (two layers, never mixed)

wire/DB (read from raw captured frame bytes / server console+log only, never from what's on screen):
- The login/StartGame response's `BasicAttr` block has change-mask bit **`0x0001`** set, with a wstring field
  immediately following the mask field among `BasicAttr`'s emitted fields (ascending mask-bit order -- `0x0001`
  is the lowest bit, so it is emitted first) that decodes to the character's actual stored name.
- The same response's `ActorAttr` block does **NOT** have change-mask bit **`0x01000000`** set at all (absent,
  not merely present-and-zero -- record which the captured frame actually shows).
- Net frame length: record byte length of the `BasicAttr`/`ActorAttr` blocks and the whole StartGame response;
  compare against a pre-fix capture if the tester has one, otherwise record this session's bytes as a fresh
  baseline, not a comparison.
- `sessions`: +1 row with `selected_character_id` set for this login; `max(lease_generation)` does not go
  backward; `PRAGMA integrity_check` = `ok` on the working copy both times; canonical sha256 matches
  `CANON_SHA.txt` before and after. Raw GAME log + console out/err kept whole, both before and after.
- Negative result with equal standing: if `0x01000000` is still set, or the `0x0001` name field does not
  decode to the character's name, despite ด่าน 0-2 clearing -- write that up in full; it means the merged
  commit did not do what this ticket's source description claims, which is itself the finding.

client-observable (a human at the screen only, never inferred from the console):
- Nameplate text (step 5) transcribed verbatim from a full-res still -- PASS reading = matches the character's
  actual own name; anything else (blank/garbled/wrong text) is recorded plainly, not read as this entry's own
  failure (see P3).
- `CHARACTER` window name field (step 6) transcribed verbatim; presence/absence of any guild
  tag/field/label anywhere in that window recorded plainly ("none" if none).
- Both NO-CRASH checks pass.
- Name-label colours recorded per the colour rule above, one line per label per full-res still, "none" written
  out where there is none.

### nonclaims
- Does not test class/level or the skill window (`K` / `Bt_main_Skill`) -- that is `GT-116`'s claim, a
  separate entry on a separate number; do not read either entry's result as evidence for the other.
- Does not test movement speed / HP-MP completeness / STR-CON-DEX-INT-PER stat points -- the remainder of the
  owner's own "probe base 1" table is still open at `RE-122` (`CLIENT_RE_QUEUE.md`), unrelated to this fix.
- Does not test guild membership mechanics (joining, leaving, guild chat, etc.) -- only that a freshly-created
  guildless character shows no guild artifact on login.
- Does not decide the cause of any name-label colour observed -- `RE-067` stays open, no cause inferred, even
  if a guild-styled colour appears (see P3's caveat re the separate `+0x180` guild-flag byte).
- Single account, single login, single session -- no reconnect/relogin, no second character, no second player
  observing, no guild ever actually created or joined.
- Headless full-suite (`3750 passed, 327 skipped, 0 failed`), ledger-verify, and `pf-adversary` review are
  cited evidence from this round's build, not reproduced or re-run by this entry.
- The two golden-hash re-baselines (`tests/golden/foundation_v1.json`, `tests/golden/item_lifecycle_v1.json`)
  are cited as blast-radius evidence only -- this entry does not independently re-verify their diff.
- If ด่าน 0/1/2 don't clear (PR not merged / functions not found at the resolved SHA) -> the entire entry is
  **BLOCKED**, not NO-RESULT/FAIL -- record it as "รอ merge" and stop.

### result (ผู้เทสกรอก)
```

```

---

## GT-120 CORE-REQUEST-025 TRACEPATH-GO-BUTTON-STALL-CLEAR-001: after CORE-REQUEST-025 wires an empty-vector `CTracePathVital` (0x2F92) reply to every `CTracePathReqVital` (0x4391), does a real client's map-window GO! button actually stop the client stuck showing "กำลังค้นหาเส้นทาง..." forever -- the orange stall KA1A found this round -- and does NOT this entry test whether the character walks anywhere (no waypoint/auto-walk logic exists yet)  [✅ PASS -- ปิดโดย chief round 28jd9c (2026-08-28T09:56+07:00) จากผล attended กะ1-A `20260828_0925_GT116-121-120-RESULT-*.md` · OBSERVER_CONFIRMED: 2026-08-28T09:2x+07:00 (BOOT_COMMIT `98307ae` = main HEAD) · claim เดียว (ข้อความไม่ค้างตลอดไป) เท่านั้น: กด GO! ที่ Warden Sebastian แล้ว "กำลังค้นหาเป้าหมาย.." หายใน 1 วินาที (เดิมค้างตลอดไป) จากนั้นแชทแจ้ง "เป้าหมายปัจจุบันไม่มีอยู่..." ตรงกับพฤติกรรม empty-vector fallback ที่ตั้งใจ · [ไม่อ้าง] ว่า GO! พาเดินไปหา NPC ได้จริง -- ยังไม่มี auto-walk/path จริง เป็นงานถัดไป]

> NUMBERING NOTE: grep confirmed before reserving (2026-08-28, round R206) -- `GT-120`/`RE-120` = 0 hits in
> `GAME_TEST_QUEUE.md`, `CLIENT_RE_QUEUE.md`, and `archive/`. Highest number in use anywhere in the shared
> counter is `119` (`RE-119` TRACEPATH-GO-BUTTON-REQREPLY-LAYOUT-001, CLOSED PASS/DONE) -- `GT-116` is the
> highest bare GT number but is lower than 119 -- => this entry is `120`. Entries `GT-101`-`GT-116`,
> `GT-107-R3`, and `RE-085`-`RE-119` stay exactly where they are, unchanged -- this is a new entry, not a
> replacement for any of them.

### source (links only -- see cited files for full detail, not re-derived here)
- `notes_to_chief/consumed/20260828_0235_KA1A-FOUND-GO-button-sends-CTracePathReqVital-0x4391-server-must-answer-0x2F92.md`:
  attended finding, exact repro path `เปิดแผนที่ (M) -> เลือก NPC -> กด GO!` -- nothing happens on the wire
  reply side, orange center-screen text "กำลังค้นหาเส้นทาง..." stays up forever (screenshot
  `M1P_ingame_20260828_prison_exile_pike_deer_*.png`). Server never sent `0x2F92` at all.
- `notes_to_chief/20260828_0424_RE-119-RESULT-DISCRIMINATED-PATH-RECORDS-AND-UI-ACTIONS.md` (STATIC-ON-BRIDGE,
  PASS/DONE): proves the client's own response handler `[0x006EA9E0,0x006EACD3)`, on an empty response vector
  (`u16` count = 0, no records), dispatches UI action `EndFindPath` at object `Main_FindPath` -- a clean stall-
  clear signal, static evidence only, never fired at a real client before this entry.
- `notes_to_chief/20260828_0427_LANE-A-CORE-REQUEST-025-wire-tracepath-empty-response-fallback.md`: opens the
  build request, scoped explicitly to "empty-vector fallback only, do not guess a real path."
- `rounds/R206_confident-ride-l5xxkh_core-request-025-tracepath-empty-vector-plus-024-shadow-numbering-flag.md`:
  chief wired it same round. New `src/pirateforce_foundation/trace_path.py` (`TRACE_PATH_REQ_VITAL_ID`=0x4391,
  `TRACE_PATH_VITAL_ID`=0x2F92, `make_trace_path_empty_response`); `runtime.py` dispatch branch is
  unconditional (no `--*-scenario` flag -- production path), fail-closed if no character selected. New
  `tests/test_trace_path_wiring.py` (4 tests, driven through the real dispatcher): no reply pre-select;
  byte-identical to calling the builder directly; reply re-parses to exactly one `u16` tag `0x12`=0 field and
  nothing else; repeated requests each independent. Full suite `3568 passed, 0 failed` cited, not reproduced
  here.
- `notes_to_chief/consumed/20260828_0200_PANYA-DECISION-new-direction-attr-completeness-use-client-data-map-window-GO-probe.md`
  ADDENDUM 02:35: the owner's own attended GO! probe was stood down "until the payload is understood" --
  RE-119 (closed) + CORE-REQUEST-025 (wired) together lift that pause; this is the first attended shot since.

### objective (single claim -- wire/DB layer is a separate, already-closed claim)
On an ordinary flagless login, after selecting a destination in the in-game map window and clicking GO!, does
the client stop showing the orange "กำลังค้นหาเส้นทาง..." text stuck forever, instead clearing it the way
KA1A's pre-fix capture never once saw. The wire/DB layer of this same fix (does the server actually reply with
a structurally-empty `CTracePathVital`) is already proven headless this round in
`tests/test_trace_path_wiring.py` (pirate-force-server repo) -- cited above, NOT re-proven by this entry. This
entry is the client-observable layer only: the first human eyes on this specific fix.

### predictions (a wrong prediction is a finding, not a failure)
- P1 [primary, proposed]: clicking GO! causes the orange text to either not persist at all, or to appear and
  then clear on its own within a short window -- either way, NOT stuck forever the way KA1A captured it.
- P2 [expected non-event, explicitly NOT a requirement]: the character does not walk/move anywhere. If motion
  is observed, write it up as a surprising bonus finding, separate from this entry's own pass/fail -- CORE-
  REQUEST-025 deliberately implements no waypoint/auto-walk logic (RE-119 T4, request field `u16@+0x14`
  bounded negative, never touched this round).
- P3 [falsifier]: the orange text still appears and never clears within the observation window below -- a real
  negative, not a failure. It would mean either this client build never received the fix, this exact click
  path does not reach the new dispatch branch, or `EndFindPath` needs more than an empty vector in practice
  (RE-119's handler proof was static, never fired at a real client before this entry) -- redirect to a new
  RE/GT entry naming which of those three, do not re-run this one guessing.

### ก่อนบูต -- ด่าน 0 (merge status, MUST clear first), ด่าน 1 (green boot), ด่าน 2 (grep confirms the branch)
**ด่าน 0 -- merge status:** commit `pirate-force-server@4ddfd54` is confirmed merged into `origin/main` as of
round `qynsyw` (`git merge-base --is-ancestor 4ddfd54 origin/main` => ancestor, via `pirate-force-server#173`,
itself an ancestor of the current `origin/main` HEAD `29a3a92`/PR `#180`) -- this replaces the earlier
"not yet confirmed" note, which is now stale. This does NOT mean the tester can skip verification: run
`pf_resolve_green_boot.py` yourself at boot time regardless (more commits may have landed on `origin/main`
between this note and your session) -- if it still returns non-zero or a commit missing `trace_path.py`,
the entry stays unbootable, record "รอ merge" and move to another ticket. Never checkout the branch directly
to skip the resolver, and never trust the `4ddfd54` string above without ด่าน 2 confirming it live.

**ด่าน 1:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
Only `exit 0` + printed `BOOT_COMMIT: <sha>` means bootable.

**ด่าน 2 (need at least 1 line from every command; missing any one = BLOCKED, do not boot):**
```
git grep -n "TRACE_PATH_REQ_VITAL_ID" <SHA> -- src/pirateforce_foundation/trace_path.py
git grep -n "TRACE_PATH_VITAL_ID" <SHA> -- src/pirateforce_foundation/trace_path.py
git grep -n "make_trace_path_empty_response" <SHA> -- src/pirateforce_foundation/trace_path.py
git grep -n "0x4391\|TRACE_PATH_REQ_VITAL_ID" <SHA> -- src/pirateforce_foundation/runtime.py
```

### db
default_state\pirateforce.sqlite3 -- copy only, canonical never opened. Copy to
`pf_bridge\backup\pirateforce_before_GT-120_<yyyyMMdd_HHmmss>.sqlite3`, then `state\run_gt120.sqlite3`. sha256
vs `CANON_SHA.txt` before/after; `PRAGMA integrity_check=ok` on the working copy both times.

### server args (flagless -- the dispatch branch is unconditional/production, no `--*-scenario` of any kind)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt120.sqlite3
```
No scenario flag, no other entry piggybacked onto this boot. Any ordinary character/login works -- default
spawn (Port Royal, scene 1) is enough; the map window's own NPC list is populated by the world census, not by
this fix.

### steps (click by click -- record continuous video for the whole LOCK_GAME window)
Before start: hold `LOCK_GAME`, note boot stamp (+07:00, must be under 420 min old at teardown), compare
canonical sha, copy both DBs per the db block, stage `TEMPLATE_teardown_generic.ps1`, confirm ด่าน 0-2 all
cleared (record the resolved SHA).
1. Start the server first (`Get-NetTCPConnection -State Established` on ports 10188/10189 must be 0 before
   opening the client -- a client opened with no server dies on its own in ~3.5 minutes). If a client has to
   be killed mid-session, restart the server before the next client -- the server keeps the old session, the
   next client hangs on "connecting" forever otherwise.
2. Open client, log in normally to a character, enter the map. Start continuous recording before entering.
3. T0: HP bar / minimap / map name visible. Record HUD X/Y. Photograph full-res, name-label colours from this
   still (self, "none" if no other label visible).
4. NO-CRASH check: right-click-drag to sweep the camera 360 degrees once. Camera-only, character facing never
   moves, nothing goes out on the wire. Never use Q/E or W/A/S/D for this check -- those turn the character
   and emit `TargetPosVital`.
5. Press M to open the map window. Photograph full-res.
6. Select any one destination/NPC entry in the map window's list (KA1A's own path: open map -> select NPC).
   Photograph the selection, before clicking GO!.
7. Click GO!. Immediately watch screen-center.
8. Photograph full-res at: immediately after click, +2s, +5s, +10s, +30s, or until the orange text clears,
   whichever comes first. Record whether it appeared at all, and if so the exact timestamp it appeared and the
   exact timestamp it cleared (or "still present at +30s" if it never clears).
9. Record HUD X/Y again -- expected unchanged (P2); if changed, note prominently as a bonus/surprise finding,
   not a requirement of this entry.
10. Supplementary only, not required for a pass: if the server console is visible, copy verbatim any line
    carrying `CTracePathReqVital`/`0x4391` at the moment of the click and any reply line carrying
    `CTracePathVital`/`0x2F92` -- a missing console line does not fail this entry (see wire/DB pass criteria).
11. NO-CRASH check again (right-click-drag).
12. Log out, teardown via `TEMPLATE_teardown_generic.ps1` (stamp still under 420 min), recheck canonical
    sha256, sha256 every capture.

Colour rule (Panya's order, 2026-08-25): one line per label per image, write "none" not blank, full-res stills
only (never a contact sheet or video), never infer a cause -- RE-067 is open and is the only place that
question lives.

### pass criteria (two layers, never mixed)

wire/DB: the actual claim this layer answers -- "does the server structurally reply with an empty
`CTracePathVital`" -- is already CLOSED headless this round by `tests/test_trace_path_wiring.py` (4/4 green,
cited above, not reproduced by this entry). This entry's own wire/DB obligations are only: canonical sha256
matches `CANON_SHA.txt` before/after; `PRAGMA integrity_check` = `ok` on the working copy both times;
`sessions`/`lease_generation` behave normally for one ordinary login. Any console lines captured per step 10
are recorded as supplementary corroboration only, never as a substitute for the client-observable answer below
and never required for this entry to close.

client-observable (a human at the screen only, never inferred from the console):
- Primary reading: does "กำลังค้นหาเส้นทาง..." ever get stuck forever, or does it clear (including "never even
  appeared because the reply was fast") -- P1 vs P3, both are complete, valid answers; write whichever
  actually happened.
- Secondary: did the character's position change -- expected no (P2); record either way, do not fail this
  entry if it did move.
- Both NO-CRASH checks pass.
- Name-label colours recorded per the colour rule above, one line per label per full-res still.

### nonclaims
- Does not prove any waypoint/auto-walk behavior of any kind. CORE-REQUEST-025 wires only an empty-vector
  reply; RE-119 T4 leaves the request's own discriminator field (`u16@+0x14`) bounded negative -- quest id vs.
  NPC id vs. list index is still unresolved, and no record-carrying reply exists to test.
- Does not test the map window's destination-selection semantics or which NPC/quest a given click corresponds
  to on the wire -- out of scope, RE-119 T4's own open question.
- Does not decide the cause of any name-label colour observed (`RE-067` stays open, no cause inferred).
- Does not reproduce or re-run `tests/test_trace_path_wiring.py` -- that headless proof is cited as already
  closed, this entry supplies only the client-observable half.
- Single account, single login, single session -- no reconnect/relogin, no second character.
- If ด่าน 0/1/2 don't clear (PR not merged / functions not found at the resolved SHA) -> the entire entry is
  **BLOCKED**, not NO-RESULT/FAIL -- record it as "รอ merge" and stop.
- Does not reopen or supersede any other GT/RE entry; PANYA-DECISION 0200's ADDENDUM 02:35 stood the GO! probe
  down only pending payload understanding -- RE-119 (closed) + CORE-REQUEST-025 (wired) lift that pause, this
  is the first attended shot since, on a fresh number.

### result (ผู้เทสกรอก)
```

```

---

## GT-121 CORE-REQUEST-026 BG0002-ARRIVAL-CENSUS-NO-WASD-001: after CORE-REQUEST-026 makes the Bg0002 (Prison Exile Island) census fire on `teleport_sent + runtime_ack_sent` (arrival) instead of waiting for the first `TargetPosVital`, does a real client actually show NPCs/monsters standing on screen the moment the loading screen clears -- **before the player presses any movement key at all** -- closing gap ① from M1-P's own PASS result (`20260828_0150_M1P-RESULT-PASS-*.md`: "เข้าฉากแล้วไม่มีอะไรเกิดขึ้นจนกว่าจะกด Q/E/A/S/D/W หนึ่งครั้ง")  [✅ PASS -- ปิดโดยสาย A (LANE-A) รอบ `kr1kme` (2026-08-28T10:2x+07:00) จากผล attended กะ1-A `20260828_0925_GT116-121-120-RESULT-*.md` · OBSERVER_CONFIRMED: 2026-08-28T09:2x+07:00 (BOOT_COMMIT `98307ae` = main HEAD) · claim เดียว (สำมะโนมาก่อนขยับ) เท่านั้น: wire `WORLD_CENSUS assembled=97/97 source=bg0002_full_roster` พิมพ์ที่ HB#5 ก่อน first `TargetPosVital` ที่ HB#15 (10 heartbeat ต่อมา) · จอเจ้าของ: "เข้าแมพมา NPC ทุกตัวเกิดมารออยู่แล้ว ผ่าน" -- ช่องว่างข้อ ① ของ M1-P ปิด · [ไม่อ้าง] เรื่อง facing/สี/ความหนาแน่นของ actor (คนละเรื่อง, gap ②/③/④/⑥ ของ M1-P ยังเปิดอยู่ -- ไม่รวมข้อ ⑤ ที่แยกเรื่อง Mirage Reel/RE-123 ซึ่งก็ยังเปิดเช่นกัน)]

> NUMBERING NOTE: grep confirmed before reserving (2026-08-28T06:38+07:00, this round) -- `GT-121`/`RE-120` = 0
> hits in `GAME_TEST_QUEUE.md`, `CLIENT_RE_QUEUE.md`, and `archive/`. Highest number in use anywhere in the
> shared counter is `120` (`GT-120`, above) -- => this entry is `121`. `GT-101`-`GT-120` and `RE-085`-`RE-119`
> stay exactly where they are, unchanged -- this is a new entry, not a replacement for any of them.

### source (links only -- see cited files for full detail, not re-derived here)
- `notes_to_chief/20260828_0150_M1P-RESULT-PASS-owner-confirms-Prison-Exile-identities-6-gaps-map-window-lead.md`
  gap ①: the owner's own M1-P session (00:2x-00:5x+07:00, boot commit `6406a05`, BEFORE this fix existed)
  measured the census arriving only after the client's first `TargetPosVital` (console L260 -> L264-265) --
  the scene sat empty from load until the player's first WASD press. This entry is the first attended shot at
  the fix for exactly that gap.
- `rounds/R207_confident-ride-sf9kel_core-request-026-bg0002-census-arrival-trigger.md` /
  `notes_to_chief/consumed/20260828_0234_LANE-A-CORE-REQUEST-024-bg0002-census-trigger-on-arrival.md` (the
  build request, filed under the shadow-collided number `024`, re-registered `026` per
  `CHIEF_CONTINUATION.md` row 026): chief wired `pirate-force-server@13fe3aa` same round -- confirmed on
  `origin/main` ancestry as of this entry (`git log origin/main --oneline | grep 13fe3aa`, merged via
  `pirate-force-server#177`). WORLD-CENSUS-001's bg0002 branch now triggers on
  `teleport_sent and runtime_ack_sent` alone, anchored on
  `world_scene_travel.spawn_position(world_scene_travel.destination(scene_id, scene_entry_registry))`
  when no `TargetPosVital` has arrived yet; a real `TargetPosVital` that does arrive first still wins as the
  anchor, unchanged. bg0001 (Port Royal) is untouched -- still waits for `TargetPosVital` exactly as before,
  not in scope of this entry.
- `notes_to_chief/consumed/20260827_2240_KA1A-NOTE-GT110-unsafe-until-0x5A19-payload-fixed-plus-M1P-jobs-staged.md`
  and the M1-P result above: the run-DB-copy seed procedure this entry reuses (`character_positions.scene_id`
  1->2 on a throwaway copy, never canonical) is not new -- it is the exact procedure M1-P's own jobs
  `1311`-`1314` already ran successfully once today. This entry does not invent a new seed method.

### objective (single claim -- identity/roster correctness is a separate, already-PASSED claim from M1-P)
On a character whose stored position row names `scene_id=2` (seeded the same way M1-P seeded it), does the
Prison Exile Island census (NPCs, monsters) appear on screen **before the player has pressed any movement
key** -- specifically, does the very first `RuntimeProtocolReq` poll after arrival already carry the full
roster, rather than the roster appearing only after the first WASD-triggered `TargetPosVital`. The wire/DB
layer of this claim (does the dispatcher's guard actually admit an arrival with `last_target_pos is None`) is
already proven headless this round in `tests/test_bg0002_census_wiring.py::
test_the_scene2_census_arrives_with_no_target_pos_vital_ever_sent` (cited above, NOT re-proven here). This
entry is the client-observable layer only: the first human eyes on this specific fix, and specifically the
first time anyone tests it WITHOUT pressing a movement key first (M1-P's own PASS session did press WASD,
which is exactly why it could see gap ① at all).

### predictions (a wrong prediction is a finding, not a failure)
- P1 [primary, proposed]: NPCs/monsters are visible standing on the ground the moment the loading screen
  clears and the HUD becomes interactive, with the character standing still and no key pressed yet -- not the
  empty scene M1-P's own PASS session described for the first few seconds.
- P2 [expected non-event, explicitly NOT a requirement]: the actors' facing direction is still the same
  cosmetic four-way round-robin RE-116 already bounded as synthetic (not real client data) -- do not treat
  uniform facing as a new finding, it is gap ② from the same M1-P letter and already understood, unrelated to
  this fix.
- P3 [falsifier]: the scene is still empty until the first movement key is pressed -- a real negative, not a
  failure. It would mean either this client build never received `pirate-force-server@13fe3aa`, the seed did
  not actually land on `scene_id=2` before boot, or the arrival trigger's own anchor fallback
  (`world_scene_travel.spawn_position`) failed silently and latched `world_census_refused` -- redirect to a
  new RE/GT entry naming which of those three (check the console for `world_census_bg0002_arrival_anchor_
  refused_*` specifically -- its presence points at the third), do not re-run this one guessing.

### ก่อนบูต -- ด่าน 0 (merge status, MUST clear first), ด่าน 1 (green boot), ด่าน 2 (grep confirms the branch)
**ด่าน 0 -- merge status:** commit `pirate-force-server@13fe3aa` is confirmed on `origin/main` ancestry as of
this entry's writing (`git log origin/main --oneline` lists it, merged via `pirate-force-server#177`) --
unlike GT-120 at the time it was opened, this fix does not need a fresh re-check before ด่าน 1, but
`pf_resolve_green_boot.py` still follows `origin/main` at boot time, not this entry's writing time, so
re-confirm anyway.

**ด่าน 1:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
Only `exit 0` + printed `BOOT_COMMIT: <sha>` means bootable.

**ด่าน 2 (need at least 1 line from every command; missing any one = BLOCKED, do not boot):**
```
git grep -n "CORE-REQUEST-026" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "world_census_bg0002_arrival_anchor_refused" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "SCENE2_N_ID" <SHA> -- src/pirateforce_foundation/world_population_bg0002.py
git grep -n "test_the_scene2_census_arrives_with_no_target_pos_vital_ever_sent" <SHA> -- tests/test_bg0002_census_wiring.py
```

### db -- seed procedure reused from M1-P jobs 1311-1314, not new
default_state\pirateforce.sqlite3 -- copy only, canonical never opened. Copy to
`pf_bridge\backup\pirateforce_before_GT-121_<yyyyMMdd_HHmmss>.sqlite3`, then `state\run_gt121.sqlite3`. sha256
vs `CANON_SHA.txt` before/after; `PRAGMA integrity_check=ok` on the working copy both times.

Seed, on the working copy only, before first boot:
```
UPDATE character_positions
   SET scene_id=2, scene_seq=0, x=26905, y=21185, z=1680
 WHERE character_id=<the test character's id>;
```
(`26905,21185,1680` is `scenarios/world_scene_registry_001.json`'s own pinned scene-2 spawn -- the same value
`world_scene_travel.spawn_position` reads as the arrival-trigger's anchor fallback, and the same coordinate
M1-P's own seed used.) Print the row before and after the UPDATE as the SEED_BEFORE/SEED_AFTER receipt, the
same convention M1-P's job `1312_m1p_boot_video` used.

### server args (flagless -- the dispatch branch is unconditional/production, no `--*-scenario` of any kind)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt121.sqlite3
```
No scenario flag, no other entry piggybacked onto this boot.

### steps (click by click -- record continuous video for the whole LOCK_GAME window)
Before start: hold `LOCK_GAME`, note boot stamp (+07:00, must be under 420 min old at teardown), compare
canonical sha, copy DB per the db block above, run the seed UPDATE and print SEED_BEFORE/AFTER, stage
`TEMPLATE_teardown_generic.ps1`, confirm ด่าน 0-2 all cleared (record the resolved SHA).
1. Start the server first (ports 10188/10189 must show 0 established connections before opening the client).
2. Open client, log in to the seeded character. **Start continuous recording BEFORE the loading screen
   clears** -- the whole point of this entry is what is on screen in the first few seconds, before any input.
3. **Do not press any key and do not move the mouse over the game viewport** from the moment the loading
   screen clears until step 5 is done. No W/A/S/D, no Q/E, no camera drag -- any of those can emit a
   `TargetPosVital` and would make this test indistinguishable from what M1-P already ran once.
4. Photograph full-res the instant the HUD becomes interactive (T0), and again at +1s, +2s, +5s -- record
   whether any actor (NPC or monster) is visible at each still, and if visible only starting at some later
   still than T0, record which one.
5. Once step 4's stills are captured, THEN it is safe to do the normal M1-P-style tour (WASD to Navy
   Transfer/Sebastian/Pike/etc.) if useful corroboration, but that part is not required for this entry's own
   pass/fail -- it is already what M1-P proved once.
6. If the server console is visible, copy verbatim the first `WORLD_SCENE scene_id=2` line and the first
   `WORLD_CENSUS assembled=.../...` line, and note whether either appears before or after step 3's first
   possible player input (there should be none) -- supplementary corroboration only, not a substitute for the
   client-observable answer.
7. Log out, teardown via `TEMPLATE_teardown_generic.ps1` (stamp still under 420 min), recheck canonical
   sha256, sha256 every capture.

### pass criteria (two layers, never mixed)

wire/DB: the actual claim this layer answers -- "does the dispatcher admit an arrival census with
`last_target_pos is None`" -- is already CLOSED headless this round by
`tests/test_bg0002_census_wiring.py`'s 4 new tests (cited above, not reproduced by this entry). This entry's
own wire/DB obligations are only: canonical sha256 matches `CANON_SHA.txt` before/after; `PRAGMA
integrity_check` = `ok` on the working copy both times; the seed UPDATE's before/after row is printed.

client-observable (a human at the screen only, never inferred from the console):
- Primary reading: are NPCs/monsters visible at T0 (the instant the HUD becomes interactive, before any
  player input) -- P1 vs P3, both are complete, valid answers; write whichever actually happened, and if
  P3, record exactly how many seconds/inputs elapsed before actors did appear (if they ever did).
- Secondary: record which specific NPC(s) are visible at T0 by name/title if legible (does not need to match
  every one of the 97 -- a handful visible near spawn is enough to answer this entry's own question).
- No crash, no stuck loading screen, no error dialog during the no-input observation window (steps 3-4).

### nonclaims
- Does not re-test M1-P's own identity/roster-correctness claim (already PASSED, see the source letter) --
  this entry only tests WHEN the roster appears, not WHETHER it is the right roster.
- Does not test bg0001 (Port Royal) -- CORE-REQUEST-026 deliberately left that branch untouched, still
  requiring `TargetPosVital` exactly as before; a separate entry would be needed if that behavior is ever
  wanted there too.
- Does not prove the arrival-trigger's anchor fallback is correct for any scene OTHER than 2 -- it is scoped
  to `SCENE2_N_ID` only, by the runtime.py branch structure itself, not by anything this entry checks.
- Does not attempt to close gaps ②-⑦ from the M1-P letter (heading, name colour, density, Mirage Reel, pose,
  Attr completeness) -- separate, already-tracked items, out of scope here.
- Single account, single login, single session -- no reconnect/relogin, no second character.
- If ด่าน 0/1/2 don't clear (functions not found at the resolved SHA) -> the entire entry is **BLOCKED**, not
  NO-RESULT/FAIL -- record it as "รอ merge" and stop.

### result (ผู้เทสกรอก)
```

```

---

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

## GT-127 GM-003 CHAT-COMMAND-DOOR-001: GM พิมพ์คำสั่งลง**กล่องแชทธรรมดา**ของเกม (ไม่ใช่หน้าต่าง `BT_GM`/`GMUI_BASIC` ที่คลิกแล้วเงียบ) แล้วเซิร์ฟเวอร์อ่านคำสั่งนั้นได้จริงไหม -- ตัดสินที่ ndjson audit log ไม่ใช่ผลบนจอ  [**READY** -- ปลดบล็อกโดย LANE-GM (เจ้าของใบ) รอบ `vvxkft` 2026-08-28T19:2x+07:00 · ~~BLOCKED-ON-WIRING -- `runtime.py` วันนี้มี `lane_hooks.fire()` **จุดเดียว** (สาขา `0x51E9` ที่ `runtime.py:4824`) และ **ไม่มี**จุดแทรกที่สาขา `0xAC52` ⇒ hook ไม่เคยยิงแม้แต่ครั้งเดียว~~ **ไม่จริงอีกต่อไป:** chief ต่อสายให้แล้วตาม `CORE-REQUEST-GM-028` -- จุดเรียกอยู่บน main ที่ `runtime.py:4784` (merge `d139f12` = PR #201, จดหมาย `notes_to_chief/20260828_1845_CHIEF-REPLY-CORE-REQUEST-GM-028-chat-point-wired.md`) ⇒ **ด่าน 2 บรรทัดแรกต้อง grep เจอแล้ว** ถ้ายังไม่เจอ แปลว่า `<SHA>` ที่ resolve ได้เก่ากว่า `d139f12` ไม่ใช่ว่าใบนี้บล็อก · สองข้อที่ chief ตั้งใจทำต่างจากจุด `0x51E9` และมีผลต่อเกณฑ์ใบนี้: (1) **ไม่มี `return`** เฟรมยังไหลต่อทางเดิมทุกไบต์ ⇒ บรรทัดแชทต้องแสดงผลปกติ (ตรงกับ P3 อยู่แล้ว) (2) **ไม่บวก `rx_frames`** ⇒ สำมะโนเฟรมต้องไม่ขยับเพราะ hook · ข้อจำกัดที่ต้องเขียนลงในผล: `parse_outer` ของ v141 ถอด nested vital **ตัวแรก** แล้วส่งไบต์ที่เหลือทั้งหมดเป็น `nested_payload` ⇒ ถ้าเฟรมหนึ่งมี vital มากกว่าหนึ่งตัว hook จะได้ payload ที่ไม่ใช่บอดี้แชทล้วน และ `handle_local_talk_chat` จะ**ปฏิเสธเพราะรูปไม่ตรง (refusal ไม่ใช่ crash)** -- เฟรมแชทที่เคย capture ทั้งสามใบ (GT-006/GT-009) เป็น `vital_count == 1` ทั้งหมด จึงยังไม่เคยเจอกรณีนี้จริง **ถ้าเจอ `refused_*` ทั้งที่พิมพ์คำสั่งถูก ให้จด `vital_count` ของเฟรมนั้นก่อนสรุปว่า FAIL** · ~~`CORE-REQUEST-GM-028` (`notes_to_chief`, รอบนี้) ขอสามบรรทัดนั้นจาก chief~~ **แทนที่ด้วย `CORE-REQUEST-GM-029` (รอบ `gr2q9j`, 2026-08-28T18:2x+07:00)** -- GM-028 ขอ `fire()` ซึ่งตามสัญญาของตัวมันเอง **ไม่คืนค่า** ⇒ อ่านบรรทัดได้แต่ส่งไบต์กลับไม่ได้ตลอดกาล · GM-029 ขอจุดเดียวที่ **คืน action** รูปเดียวกับ `gm_state_action` (`runtime.py:5122/5331`) ⇒ ครอบทั้งใบนี้และ `GT-128` · 🔴 **wire ได้จุดเดียวเท่านั้น** ถ้าเผลอวางทั้งสองแบบ = authorize ซ้ำ + ndjson ซ้ำแถว + กิน rate limit สองเท่า · 🔴 ห้ามบูตใบนี้จนกว่าด่าน 2 จะ grep เจอจุดเรียกจริงบน `main`]

> เลขใบ: ตัวนับเดียวร่วมกับ `CLIENT_RE_QUEUE.md`, prefix สองแบบ ห้ามแยกตัวนับ. รอบนี้ (LANE-GM รอบ `hs9m2r`,
> 2026-08-28) จอง `RE-126` ที่ `CLIENT_RE_QUEUE.md` และ `GT-127` ที่ไฟล์นี้. grep ยืนยันก่อนจอง:
> `GT-126` / `GT-127` / `RE-126` = 0 hit ทั้งสองไฟล์. เลขสูงสุดก่อนหน้า = `GT-124` / `RE-125`.
> ใบเก่าทุกใบอยู่ที่เดิม ไม่ถูกแตะ ไม่ถูกย้าย -- ใบนี้เป็นใบใหม่ ไม่แทนที่ใบใด.

### ที่มา (ยืนยันแล้ว -- ห้าม re-derive ระหว่างรอบ)
- ไคลเอนต์ส่งทุกบรรทัดที่พิมพ์ในกล่องแชทเป็น vital `0xAC52` `Channel_LocalTalkMessageVital`. เพย์โหลด =
  wstring#1 (speaker, ฝั่ง client->server ว่างเสมอ) + wstring#2 (ข้อความที่พิมพ์); แต่ละ wstring =
  tag `0x48` + u32 LE ความยาวไบต์ + UTF-16LE ล้วน ไม่มี terminator ⇒ รวม = `5 + n1 + 5 + n2`.
- หลักฐานชั้นที่ 1: `GT-006`/`GT-009` จับเพย์โหลดจริงสามความยาว -- 34B ของ `"PFCHATPROBE1"` (12 ตัว),
  20B ของ `"SHORT"` (5), 46B ของ `"PFCHATPROBETOOLONG"` (18) -- ตารางอยู่ที่
  `pf_bridge/reports/PF_CHAT_ECHO002_SPEAKER_FIELD_RESEARCH_20260818.md` หัวข้อ (a).
  ชั้นที่ 2: `tag 0x48 + u32 len + UTF-16LE` คือ wide-string encoding มาตรฐานของไคลเอนต์ Grade A
  (พิสูจน์กับ `CreateActorDataEx`/`ActorAttr` names).
- โมดูลใหม่รอบนี้: `src/pirateforce_foundation/gm/chat_command.py` (`handle_local_talk_chat`) +
  hook `src/pirateforce_foundation/lane_hooks/lane_gm_chat_command.py` (point `vital_inbound_chat_local_talk`).
  unit test 45 ตัวผ่าน -- headless เท่านั้น ยังไม่เคยยิงกับไคลเอนต์จริง.
- ไวยากรณ์ (`gm/commands.py` เดิม): sigil คือ `/` นำหน้า -- `warp <scene_id> [x y]`, `npc on|off <mob_id>`,
  `item <id> <n>`, `lv <n>`, `spawn <mob_id>`, `say <message>`.
- 🔴 **GM-003 v1 ยังไม่มีผลต่อเกมเลย** -- คำสั่งที่รู้จักจะถูก parse แล้วเขียนลง ndjson audit log
  `capture/gm_command_log.ndjson` พร้อม `"executed": false`. **เรคคอร์ดในล็อกนั้นคือเกณฑ์ผ่าน ไม่ใช่ผลบนจอ.**
- event ที่ hook พิมพ์: `gm_chat_command_accepted_<name>` เมื่อสำเร็จ, `gm_chat_command_refused_<reason>`
  เมื่อไม่สำเร็จ (`not_gm_account`, `not_a_command`, `rate_limited`, `command_parse_error_*`).
- สิทธิ์: เฉพาะบัญชีใน allowlist ฝั่งเซิร์ฟเวอร์ (`PF_GM_ACCOUNTS_CONFIG` -> ไฟล์ json
  `{"gm_accounts": ["<name>"]}`) เท่านั้นที่ได้อะไร -- คนอื่นถูกปฏิเสธที่ identity **ก่อน**จะ decode เพย์โหลด.
- ประตูอีกบาน (`BT_GM`/`GMUI_BASIC`/`0x51E9`) ยังตายอยู่: `GT-103` (NO-RESULT ต่อ claim ตัวเอง), `RE-126`.
  ใบนี้ **ไม่รอ**สองใบนั้น.

### objective (claim เดียว)
บนบูตไร้แฟล็ก บัญชีที่อยู่ใน GM allowlist พิมพ์คำสั่งที่ขึ้นต้นด้วย `/` ลงกล่องแชทธรรมดา -- เซิร์ฟเวอร์
**อ่านและ parse คำสั่งนั้นได้จริง** (มีเรคคอร์ดใน `capture/gm_command_log.ndjson`) และบัญชีที่ไม่อยู่ใน
allowlist พิมพ์คำสั่งเดียวกันแล้ว **ไม่ได้อะไรเลย** ใช่หรือไม่.

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)
- P1 [หัวใจของใบ] `/warp 2` และ `/lv 30` -> `gm_chat_command_accepted_warp` / `_lv` + ndjson 2 เรคคอร์ด.
- P2 ประโยคธรรมดา -> `refused_not_a_command`; `/notacommand xyz` -> `refused_command_parse_error_*`;
  บัญชีนอก allowlist -> `refused_not_gm_account`. ทั้งสามไม่มีเรคคอร์ดใน ndjson.
- P3 [บนจอ] เลนนี้ต้อง**มองไม่เห็น** -- บรรทัดแชทแสดงผลเหมือนเดิมทุกประการ ไม่มี warp ไม่มีเลเวลขึ้น.
- P4 [ตัวหักล้าง, ผลลบที่มีค่าเท่ากับ PASS] คอนโซลเงียบสนิททั้งสี่บรรทัดทั้งที่ด่าน 2 ผ่าน ⇒ จุดเรียก
  `lane_hooks.fire()` ที่สาขา `0xAC52` ถูกวางผิดที่ (เช่น อยู่**ก่อน**เลนที่ `return` ของตัวเอง หรือ
  ไม่ถึงเพราะบูตนี้เปิด scenario ที่คีย์บน `0xAC52`) ⇒ แนบ diff/บรรทัดจริงของ `runtime.py` ที่ `<SHA>`
  แล้ว redirect กลับ LANE-GM ~~`CORE-REQUEST-GM-028`~~ **ไม่ใช่เปิดใบเทสใหม่** ·
  คอนโซลต้องเห็น `LANE_HOOK_FIRED pirateforce_foundation.lane_hooks.lane_gm_chat_command
  vital_inbound_chat_local_talk` ตอนลงทะเบียน -- ถ้าบรรทัดนั้นก็ไม่มี ปัญหาอยู่ที่การลงทะเบียน hook
  ไม่ใช่ที่จุดเรียก แยกสองอาการนี้ก่อนรายงาน.

### ก่อนบูต -- ด่าน 0 / ด่าน 1 / ด่าน 2
**ด่าน 0 (บัญชี/คอนฟิก):** ใช้ซ้ำการอนุมัติเดิม
`notes_to_chief/20260827_1200_CHIEF-REPLY-GT101-gm-accounts-test-config-approved.md` -- ต้องมี (ก) บัญชี GM
ที่อยู่ในไฟล์ allowlist และ (ข) บัญชีที่สอง **ที่ไม่อยู่** ในไฟล์นั้น (คู่ควบคุม).
ไม่มีบัญชีที่สอง = ทำได้แค่ครึ่งใบ ให้บันทึกว่าข้ามคู่ควบคุมเพราะเหตุใด.

**ด่าน 1 (green boot):**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
รันจากโฟลเดอร์ `pf_bridge`. เฉพาะ exit 0 + `BOOT_COMMIT: <sha>` เท่านั้นถึงบูตได้ (checkout detached).

**ด่าน 2 (grep ยืนยันสายที่ `<SHA>` จริง -- ห้ามเชื่อเลขบรรทัดในเอกสารนี้):**
```
git grep -n "vital_inbound_chat_local_talk" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "def handle_local_talk_chat" <SHA> -- src/pirateforce_foundation/gm/chat_command.py
git grep -n "vital_inbound_chat_local_talk" <SHA> -- src/pirateforce_foundation/lane_hooks/lane_gm_chat_command.py
git grep -n "gm_command_log" <SHA> -- src/pirateforce_foundation/gm/chat_command.py
```
🔴 **บรรทัดแรกคือด่านจริงของใบนี้** -- ต้องเห็นจุดเรียกทำนอง
`lane_hooks.fire("vital_inbound_chat_local_talk", session=self, payload=bytes(parsed.nested_payload))`
อยู่ที่สาขา `0xAC52` ของ `runtime.py`. ~~0 hit = **BLOCKED (รอ CORE-REQUEST-GM-028)**~~
**ตั้งแต่ merge `d139f12` (2026-08-28T12:04Z) บรรทัดนี้ต้องได้ 1 hit ที่ `runtime.py:4784`** ·
0 hit ตอนนี้ = `<SHA>` ที่ด่าน 1 resolve ให้ **เก่ากว่า** คอมมิตนั้น ⇒ ยังไม่ใช่ FAIL แต่ก็ยังบูตไม่ได้
รัน `pf_resolve_green_boot.py --fetch` ใหม่ให้ได้ sha ที่ใหม่กว่า · ยังห้ามไล่หาคอมมิตเองและห้าม
checkout แบรนช์ตรง ๆ เหมือนเดิม.

### db (สำเนาเสมอ ห้ามเปิด canonical)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-127_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt127.sqlite3
```
เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` ทั้งก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง ·
`PRAGMA integrity_check` = `ok` บนสำเนาทั้งก่อนและหลัง · สำเนาใหม่ทุกบูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับ spawn เสมอ.

### server args (เป๊ะ -- ไม่มี `--*-scenario`)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
$env:PF_GM_ACCOUNTS_CONFIG = "<path ไฟล์ allowlist จากด่าน 0>"
py -3 -u -m pirateforce_foundation.app --db state\run_gt127.sqlite3
```
`capture/gm_command_log.ndjson` เป็น path **relative กับ CWD ของ process เซิร์ฟเวอร์ตอนบูต** -- จดค่า CWD ไว้
ในผล. แนบบรรทัดคำสั่งจริงหลังเซิร์ฟเวอร์ขึ้น:
```
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List
```

### ขั้นตอน (บูตสั้น ~5 นาทีบนจอ -- อัดวิดีโอต่อเนื่องทั้งช่วง LOCK_GAME)
1. ถือ `LOCK_GAME`, จด boot stamp (+07:00), เทียบ sha canonical, ก๊อป DB ตามบล็อกด้านบน, สเตจ
   `TEMPLATE_teardown_generic.ps1`, ยืนยันว่าด่าน 0/1/2 ผ่านครบ (จด `<SHA>`).
2. **เปิดเซิร์ฟเวอร์ก่อนเสมอ** (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 ต้อง = 0 ก่อนเปิด
   ไคลเอนต์). ไคลเอนต์ที่เปิดโดยไม่มีเซิร์ฟเวอร์จะตายเองใน ~3.5 นาที.
3. เข้าเกมด้วย **บัญชี GM**: เลือกเซิร์ฟเวอร์ -> ปุ่มซ้ายของกล่อง PVP -> ช่องตัวละครแรก -> ปุ่ม**กลาง**ของห้าปุ่ม
   ล่าง (ห้ามปุ่มซ้ายสุด = ลบตัวละคร). T0: ถ่ายภาพนิ่ง full-res, จด HUD X/Y.
4. NO-CRASH: right-click-drag กวาดกล้อง 360 องศาหนึ่งรอบ -- เป็น liveness check ชนิดเดียวที่ใบนี้รับ
   (กล้องอย่างเดียว facing ของตัวละครไม่ขยับ ไม่มีไบต์ออกสาย). 🔴 **ห้ามใช้ `Q`/`E` หรือ `W/A/S/D`** --
   สองอย่างนั้นหมุน/ย้ายตัวละครจริงและปล่อย `TargetPosVital`.
5. 🔴 **คลิกเข้าไปในช่องพิมพ์แชทให้เคอร์เซอร์อยู่ในช่องก่อนพิมพ์ทุกครั้ง** -- ตัวอักษรที่พิมพ์ตอนช่องแชท
   ไม่โฟกัสจะกลายเป็น **hotkey**. ยืนยันด้วยตาว่าเห็น caret ในช่องแล้วค่อยพิมพ์.
6. พิมพ์ทีละบรรทัด กด Enter แล้วเว้น 3 วินาที จดเวลาส่งแต่ละบรรทัด (+07:00) และถ่ายภาพนิ่ง full-res ของกล่อง
   แชทหลังแต่ละบรรทัด:
   (1) ประโยคธรรมดาไม่มี `/` (เช่น `hello queue test`) · (2) `/warp 2` · (3) `/lv 30` · (4) `/notacommand xyz`
7. ยืนยันด้วยตาว่า **ไม่มี warp ไม่มีเลเวลเปลี่ยน** (HUD X/Y และเลเวลเท่าเดิม) -- ถ่ายภาพนิ่ง.
8. ออกจากเกม -> 🔴 **restart เซิร์ฟเวอร์ก่อนเปิดไคลเอนต์ตัวถัดไปเสมอ** (เซิร์ฟเวอร์เก็บ session เดิมไว้
   ไคลเอนต์ถัดไปจะค้างที่ "connecting" ตลอดกาลถ้าไม่รีสตาร์ต).
9. เข้าเกมด้วย **บัญชีที่ไม่อยู่ใน allowlist** ทำข้อ 5 ซ้ำแล้วพิมพ์ `/warp 2` หนึ่งบรรทัด ถ่ายภาพนิ่ง
   จดเวลา -- นี่คือคู่ควบคุมที่พิสูจน์ว่าผู้เล่นธรรมดาไม่ได้อะไร.
10. NO-CRASH ซ้ำ (right-click-drag) -> ออกจากเกม -> teardown.

**กฎสี (คำสั่ง Panya 2026-08-25):** ทุกภาพนิ่ง full-res ต้องมีตารางสีป้ายชื่อ **หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่ง
ภาพ** เขียนคำว่า "none" ออกมาเมื่อไม่มีป้าย ห้ามเว้นว่าง · อ่านสีจากภาพนิ่ง full-res เท่านั้น ห้ามอ่านจาก
contact sheet / ภาพย่อ / วิดีโอ · จุดต่างจากภาพเซิร์ฟเวอร์ต้นฉบับลง `REAL_SERVER_DIVERGENCE.tsv` แถวละหนึ่งจุด ·
🔴 ผู้เทสบันทึก**สีเท่านั้น** ห้ามอนุมานสาเหตุของสี (`RE-067` เปิดอยู่ และเป็นที่เดียวที่คำถามนั้นอยู่).

### pass criteria (สองชั้น แยกกันเสมอ ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)

**wire/DB (อ่านจากคอนโซล/ล็อก/ไฟล์บนดิสก์เท่านั้น):**
- คอนโซลขึ้นครบทั้งห้า: `gm_chat_command_accepted_warp`, `gm_chat_command_accepted_lv`,
  `gm_chat_command_refused_not_a_command` (ประโยคธรรมดา),
  `gm_chat_command_refused_command_parse_error_*` (`/notacommand xyz`),
  `gm_chat_command_refused_not_gm_account` (บัญชีคู่ควบคุม).
- `capture/gm_command_log.ndjson` มี **2 เรคคอร์ดพอดี** ทั้งคู่มีชื่อบัญชี GM และ `"executed": false` ·
  **ไม่มี**เรคคอร์ดของบัญชีนอก allowlist และ**ไม่มี**เรคคอร์ดของประโยคธรรมดา.
- `sessions`: +1 แถวต่อหนึ่งการล็อกอิน · `max(lease_generation)` ไม่ถอยหลัง · `PRAGMA integrity_check` = `ok`
  ก่อน/หลัง · sha256 ของ canonical ตรง `CANON_SHA.txt` ก่อน/หลัง · raw GAME log + console out/err เก็บทั้งไฟล์
  ไม่ตัดทอน.
- **ผลลบมีค่าเท่ากับผลบวก:** คอนโซลเงียบทั้งหมด/ndjson ไม่ถูกสร้าง ทั้งที่ด่าน 2 ผ่าน = ผลของใบนี้ (ดู P4)
  เขียนให้เด่นเท่า PASS พร้อม redirect ไป `CORE-REQUEST-GM-028`.

**client-observable (คนหน้าจอเท่านั้น ห้ามอนุมานจากคอนโซล):**
- **สิ่งที่คาดหมายคือ "ไม่มีอะไรเปลี่ยน"** -- บรรทัดแชทต้องแสดงผลเหมือนเดิมทุกประการกับก่อนรอบนี้ เลนนี้ต้อง
  มองไม่เห็น. นี่เป็นคำทำนายล่วงหน้า ไม่ใช่ FAIL.
- 🔴 คำถามที่ต้องตอบตรง ๆ ในผล: **บรรทัด `/warp 2` ที่พิมพ์ไปปรากฏในหน้าต่างแชทเป็นข้อความธรรมดา หรือหายไป
  (ไคลเอนต์กลืนบรรทัดที่ขึ้นต้นด้วย `/` เอง)?** ตอบทีละบรรทัดทั้งสี่บรรทัด อ้างจากภาพนิ่ง ไม่ใช่จากความจำ.
- ไม่มี warp ไม่มีเลเวลเปลี่ยน (GM-003 v1 ไม่มี execution) -- ถ้าเห็นการเปลี่ยนแปลงใด ๆ นั่นคือผลที่ผิดคาด
  ต้องเขียนเด่น ๆ.
- บัญชีคู่ควบคุม: จอไม่มีอะไรเกิดขึ้นเช่นกัน -- บันทึกว่าบรรทัดแสดงผลอย่างไร.
- NO-CRASH ผ่านทั้งสองครั้ง · ตารางสีป้ายชื่อครบตามกฎสีข้างบน.

### nonclaims (ติดไปกับผลทุกกรณี ห้ามตัดทิ้ง)
- 🔴 **ไม่อ้าง** ว่าคำสั่งใดมีผลต่อเกม -- v1 ทำแค่ parse + log (`"executed": false`) ผลบนจอไม่ใช่เกณฑ์ผ่าน.
- 🔴 **ไม่อ้าง** ว่าใบนี้พิสูจน์อะไรเกี่ยวกับ `BT_GM`/`GMUI_BASIC`/`0x51E9` -- คนละประตู ยังตายอยู่
  (`GT-103`, `RE-126`) และผลใบนี้ไม่ว่าบวกหรือลบก็ไม่ปิดสองใบนั้น.
- 🔴 **ไม่อ้าง** ว่าข้อความไม่ใช่ ASCII (ภาษาไทย/ตัวอักษรกว้าง) ผ่านเส้นทางนี้ได้ -- ตัวอย่างที่จับมาได้ทุกตัว
  (`GT-006`/`GT-009`) เป็น ASCII ล้วน. ถ้าอยากรู้ต้องเปิดใบใหม่.
- 🔴 **GM nonclaim (บังคับประกาศ):** ใบนี้ **ใช้สถานะ GM** เพื่อไปให้ถึงสถานะที่ทดสอบ -- การไปถึงสถานะด้วย GM
  ไม่ใช่หลักฐานว่าฟีเจอร์ทำงานสำหรับผู้เล่นทั่วไปหรือทำงานในทางปกติของเกม.
- ไม่ทดสอบไวยากรณ์ที่เหลือ (`npc`, `item`, `spawn`, `say`) และไม่ทดสอบ `rate_limited` -- คนละใบ.
- ไม่ยืนยัน byte layout ของ `0xAC52` ซ้ำ -- อ้าง `GT-006`/`GT-009` เป็นหลักฐานที่มีอยู่แล้ว ไม่ผลิตใหม่.
- unit test 45 ตัวเป็นหลักฐานที่อ้างถึง ไม่ใช่สิ่งที่ผู้เทสรันซ้ำ.
- ผู้เทสคนเดียว สองบัญชี บูตเดียว ไม่มี reconnect/relogin เกินที่ขั้นตอนระบุ.
- ไม่ชี้สาเหตุของสีป้ายชื่อ (`RE-067` เปิดอยู่).
- ถ้าด่าน 0/1/2 ไม่ผ่าน => ทั้งใบเป็น **BLOCKED (รอ wiring)** ไม่ใช่ NO-RESULT/FAIL -- ยังไม่ได้ล็อกอินเลย.

### หลักฐานที่ต้องเก็บ
`capture/gm_command_log.ndjson` **ทั้งไฟล์** + sha256 (ถ้าไฟล์ไม่ถูกสร้างเลย ให้เขียนคำว่า ABSENT พร้อม CWD ของ
เซิร์ฟเวอร์) · console out/err + raw GAME log ทั้งไฟล์ ไม่ตัดทอน · วิดีโอต่อเนื่องทั้งช่วง `LOCK_GAME` (`.mkv`
ต้นฉบับ ห้ามลบ) · ภาพนิ่ง full-res ของกล่องแชทหลังทุกบรรทัด + ภาพ T0 + ภาพหลังข้อ 7 + ภาพของบัญชีคู่ควบคุม ·
ตารางสีป้ายชื่อ (หนึ่งบรรทัดต่อป้ายต่อภาพ, "none" เขียนออกมา) · แถว `REAL_SERVER_DIVERGENCE.tsv` ถ้ามี ·
เวลาส่งทุกบรรทัด (+07:00) · `<SHA>` ที่บูต + บรรทัดคำสั่งจริง · run copy `state\run_gt127.sqlite3`
**เก็บไว้ให้ chief re-derive ห้ามทิ้ง** · sha256 ของทุกไฟล์หลักฐาน.

### teardown (บังคับ -- แม้รอบจะจบเพราะเลิกเล่น ไม่ใช่เพราะเทสจบ)
`TEMPLATE_teardown_generic.ps1` เสมอ ภายใน **420 นาที** จาก boot stamp
(`TEMPLATE_teardown_generic.ps1:135` · เพดานยกจาก 180 เมื่อ 2026-08-20 · เลข 180 ในใบเก่า = stale) --
เกินเพดาน template ปฏิเสธ exit 12 โดยดีไซน์ · ได้ exit ที่ไม่ใช่ 0 อย่าเดาเอง แนบบรรทัดที่ 17 ของไฟล์ teardown
ที่ใช้จริงมาทั้งบรรทัด · ใบเสร็จ: `AFTER listeners = 0`, sha256 canonical ก่อน-หลัง = `CANON_SHA.txt`,
teardown exit code, `LOCK_GAME` ปล่อยแล้ว · **ลบสำเนาไฟล์ allowlist / ล้าง `PF_GM_ACCOUNTS_CONFIG`** ·
🔴 restart เซิร์ฟเวอร์ก่อนบูตรอบถัดไปเสมอ.

### result (ผู้เทสกรอก)
```

```

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

## GT-128 GM-003 CHAT-WARP-VISIBLE-001 [attended, in-game]: GM พิมพ์ `/warp <ฉากปัจจุบัน> <x> <y>` ลงกล่องแชทธรรมดา แล้ว**ตัวละครขยับไปยังพิกัดนั้นบนจอจริงหรือไม่** -- ใบแรกของสาย GM ที่ตัดสินที่จอ ไม่ใช่ที่ log  [BLOCKED x3 (~~x2~~ นับผิดมาแต่แรก มีสามข้อมาตลอด) -- ห้ามบูต: (ก) `CORE-REQUEST-GM-029` ยังไม่ลง main (จุดเรียกที่คืน action ที่สาขา `0xAC52`) · **อัปเดตรอบ `vvxkft`:** ตัวโมดูล `gm/chat_command_action.py` เองก็เพิ่งกลับขึ้น main รอบนี้ (PR #204 -- PR #200 ของรอบ `gr2q9j` ถูกปิดเพราะ gate แดง ไม่เคย merge) และ GM-029 เปลี่ยนความหมายเป็น "**แทนที่**บรรทัด `fire()` ของ GM-028 ในคอมมิตเดียว" ไม่ใช่ "เพิ่มจุดเรียก" (ใบ `20260828_1930_LANE-GM-CORE-REQUEST-GM-029-v2-replace-not-add.md`) ⇒ วันที่ใบนี้บูตได้ `GT-127` จะใช้ไม่ได้ตามเกณฑ์เดิมอีกต่อไป เพราะ event เปลี่ยนเป็น `gm_chat_action_*` -- **บูต `GT-127` ให้จบก่อน** (ข) ~~`RE-129` ยังไม่ตอบ~~ **RE-129 ตอบแล้ว 2026-08-28T20:09+07:00 (`ForcePos vital_version = 0`) แต่ข้อนี้ยังบล็อกอยู่ด้วยเหตุใหม่:** `COO-DECISION 20260828_2130` ล็อกแข็งว่าห้ามเปลี่ยน `FORCE_POS_VITAL_VERSION_CONFIRMED` จาก `None` จนกว่าจุดเขียนตำแหน่งแบบยืนยันจะอยู่บน main (`CORE-REQUEST-GM-030`, รอบ `fo2lgh`) **แม้ RE-129 จะตอบก่อนก็ตาม** ⇒ โมดูลยังปฏิเสธการส่งด้วยตัวเอง และตอนนี้มีเทสบังคับด้วย (`pirate-force-server/tests/test_gm_force_pos_version_lock.py` แดงถ้าเปลี่ยนค่าก่อนโทเคน `GM_WARP_POSITION_CONFIRMED` อยู่บน main) · เหตุผลชั้นที่สองจาก RE-129 เอง: handler ที่ client จดทะเบียนไว้สำหรับ `ForcePos` = `mov al,1; ret 4` ไม่อ่าน payload ⇒ **version ถูกไม่ได้แปลว่าจะขยับ** ใบนี้ยังเป็นใบเดียวที่ตัดสินข้อนั้นได้ (ค) ~~🔴 **คำถาม "ใครเป็นเจ้าของตำแหน่งหลัง warp" ยังไม่มีคำตอบ**~~ **ตอบแล้ว 2026-08-28T21:30+07:00 (`COO-DECISION`): เจ้าของคือตำแหน่งที่ client ยืนยันแล้ว · เซิร์ฟเวอร์ห้ามเขียนตำแหน่งที่ตัวเองไม่ได้สังเกตเห็น · ตัวยืนยันคือ `TargetPos` ใบแรกหลังเฟรม** ⇒ ข้อนี้เหลือ "รอการเดินสาย" ไม่ใช่ "รอคำตอบ" -- ปลดเมื่อ `CORE-REQUEST-GM-030` ลง main และ COO ปลดล็อก · ผู้เทสต้องบันทึกในผล: หลัง warp ให้เดินหนึ่งก้าวเพื่อบังคับ `TargetPos` แล้วดูว่าคอนโซลมี `GM_WARP_POSITION_CONFIRMED` หรือไม่ · **บริบทเดิมของข้อนี้ (เก็บไว้):** — pf-adversary รอบ `gr2q9j` ชี้ว่า หลังส่ง `ForcePos` แล้ว แถวใน DB และ `selected.position` ยัง**ค้างที่จุดเดิม** (โมดูลไม่เรียก `foundation.checkpoint`) ⇒ client อยู่จุดใหม่ เซิร์ฟเวอร์คิดว่าอยู่จุดเก่า · aggro/pickup/logout ใช้จุดผิด · ต้องได้คำตอบ (`ASK-COO` รอบนี้) **ก่อน**เปลี่ยนค่าคงที่ของ `RE-129` ไม่ใช่หลัง]

> เลขใบ: ตัวนับเดียวร่วมกับ `CLIENT_RE_QUEUE.md` · รอบ `gr2q9j` จอง `RE-129` ที่นั่นและ `GT-128` ที่นี่
> grep ยืนยันก่อนจอง 2026-08-28T18:2x: `GT-128` / `RE-129` = 0 hit ทั้งสองไฟล์ · สูงสุดก่อนหน้า = `GT-127` / `RE-128`

### ต่างจาก GT-127 อย่างไร (สองใบนี้ไม่ซ้ำกัน อย่ารวม)
`GT-127` ตัดสินที่ **ndjson audit log** = "เซิร์ฟเวอร์อ่านบรรทัดที่ GM พิมพ์ได้ไหม" (ครึ่งอ่าน)
`GT-128` ตัดสินที่ **จอ** = "แล้วมีอะไรเกิดขึ้นกับตัวละครไหม" (ครึ่งส่ง) · จุดเรียกเดียวกันปลดทั้งสองใบ
แต่ `GT-128` ต้องรอ `RE-129` เพิ่มอีกใบ ⇒ `GT-127` จะบูตได้ก่อนเสมอ

### ด่านก่อนบูต (ทั้งสามต้องผ่าน มิฉะนั้นเลื่อน ห้ามบูต)
1. grep บน `main` เจอจุดเรียก `make_gm_chat_command_action` จริงที่สาขา `0xAC52` ของ `runtime.py`
   (ไม่ใช่แค่ PR merged -- ต้องเห็นบรรทัดบน main)
2. `grep -n "FORCE_POS_VITAL_VERSION_CONFIRMED" src/pirateforce_foundation/gm/teleport_wire.py`
   ต้อง**ไม่ใช่** `None` และคอมเมนต์เหนือมันต้องอ้าง `RE-129` ที่ปิดแล้วพร้อม VA
3. บัญชีที่เจ้าของจะบูตอยู่ใน `gm_accounts.json` (ค่าเริ่มต้นว่าง = ไม่มีใครเป็น GM)

### ขั้นตอน (ที่ใจกลางเมือง X=11865 Y=6147 ห้ามท่าเรือ ตามกฎสายนี้)
1. login ด้วยบัญชี GM รอจนโหลดฉากเสร็จ **จดพิกัดตั้งต้นที่เห็นบนจอ**
2. พิมพ์ในกล่องแชทธรรมดา: `/warp <scene_id ที่อยู่ตอนนี้> 11900 6200` (ขยับสั้น ๆ ในฉากเดิม)
3. บันทึก: ตัวละครขยับไหม · ขยับไปตรงพิกัดที่สั่งไหม · จมพื้น/ลอยไหม (z มาจาก connection ไม่ได้แต่ง)
4. **เคสลบที่ต้องทำด้วย** พิมพ์ `/warp <ฉากอื่น> 1 2` -> ต้อง**ไม่เกิดอะไรขึ้น** (ForcePos ข้ามฉากไม่ได้
   โมดูลปฏิเสธโดยตั้งใจ ไม่ใช่บั๊ก) · และพิมพ์ข้อความธรรมดา (ไม่ขึ้นต้น `/`) -> ต้องไม่มีอะไรผิดปกติ
5. ให้ผู้เล่นธรรมดา (บัญชีนอก `gm_accounts`) พิมพ์คำสั่งเดียวกัน -> ต้องไม่เกิดอะไร และไม่มีแถวใน ndjson

### เกณฑ์สองชั้น
- **ชั้น wire/DB:** คอนโซลเซิร์ฟเวอร์มี label `LANE_GM_CHAT_WARP_FORCE_POS` หนึ่งครั้งต่อหนึ่งคำสั่งที่รับ
  · ndjson มีหนึ่งแถวต่อหนึ่งคำสั่ง (**ไม่ใช่สองแถว** -- สองแถว = เผลอ wire ทั้ง `fire()` และ action)
- **ชั้น client-observable:** ตัวละครอยู่ที่พิกัดใหม่บนจอ (ภาพ/คำบอกเล่าของเจ้าของ)

### nonclaims ที่ผลของใบนี้ **ห้าม**ถูกใช้อ้าง
1. [ไม่อ้าง] ว่า warp ข้ามฉากทำได้ -- ใบนี้ทดสอบ **ในฉากเดียว**เท่านั้น (`ForcePos` ไม่มีช่อง scene id)
2. [ไม่อ้าง] ว่า M2 หรือ milestone ใดผ่าน -- **GM คือเครื่องมือไปถึงสภาพที่จะเทส ไม่ใช่หลักฐานว่าฟีเจอร์ทำงาน**
   ถ้าใบนี้ PASS สิ่งที่พิสูจน์คือ "เราย้ายตัวละครไปจุดที่อยากเทสได้" ไม่ใช่ว่าการเดินทางในเกมทำงาน
3. [ไม่อ้าง] อะไรเกี่ยวกับ `BT_GM`/`GMUI_BASIC`/`0x51E9` -- คนละประตู (`RE-126` ยังเปิด)
4. [ไม่อ้าง] ว่าคำสั่ง GM อื่น (`npc`/`item`/`lv`/`spawn`/`say`) ทำงาน -- ยังไม่มี wire ทั้งห้าตัว

**ผู้เปิดใบ: LANE-GM (รอบ `gr2q9j`)** -- ผลกลับมาที่สาย GM บริโภค

---

## GT-129 MOB-DEATH-001 DEAD-ONLY-NO-DYING-001 [attended, in-game]: ส่ง **DEAD เฟรมเดียว ไม่มี DYING นำหน้า** ให้ศพ 0x201F -- ศพยัง**แข็ง**หรือ**ล้ม**  [🔴 **BLOCKED -- ห้ามบูต**: (ก) ต้องมีทางขับ "DEAD-only" ที่ call site `runtime.py` ซึ่งเป็นไฟล์ของ chief -- สาย B ขับเองไม่ได้ (ข) สะพานฝั่งเครื่องเงียบตั้งแต่ 15:06 (`COO-DECISION 20260828_1841`)]

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
  B0 ต้องได้ 1 กับ 1 · ทั้งสองแขนต้องมี `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE actor_count=115`
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
และวัดบน composer ที่ **ไม่ใช่ตัวที่ลงสายจริง** ดู `rounds/B_20260828_2129_*.md` ข้อ ④


---

## GT-131 NPC-IDENTITY-CLINE-RESOLVED-001 [attended, in-game]: NPC ของ Port Royal แสดง **ตัวจริง** แล้วหรือยัง -- ใบตรวจรับหลัง `GT-078` ถูกเจ้าของปฏิเสธ  [PENDING]

> **LANE-A รอบ `pqx4fj`** (2026-08-28) จอง `GT-131` (ตัวนับร่วมกับ `CLIENT_RE_QUEUE.md` · grep ก่อนจอง = 0 hit ·
> สูงสุดก่อนหน้า `GT-129`/`RE-130`) · ไม่แทนที่ใบใด ใบเก่าอยู่ที่เดิม

### ที่มา
bg0001 ส่ง placement 115 ตัวโดยใส่ **เลข Mob-Set ของไฟล์ฉาก (1..113)** ลงช่องที่ไคลเอนต์อ่านเป็น `MOBS.n_ID`
⇒ `GT-078` = "ตำแหน่งถูกทุกตัว NPC ผิดทุกตัว" · `RE-128` เจอตารางแปลงของไคลเอนต์เอง `CONSTDATA_TH__CLINE`
คีย์ (`n_CLINE_TYPE=1` ผ่าน `SCENE_NAME`, `n_CREATURE_TYPE`=เลข Mob-Set) -> `n_LEADER_BK1` = `MOBS.n_ID` ตัวจริง ·
รอบนี้ต่อสายแล้ว **ไม่มีแฟล็ก ทุกบูต**: actor ถือ n_ID ที่ resolve + `s_OUTFIT` ของแถวนั้น + ชื่อจาก `MOBS_TIP`
🔴 **7 placement ว่างโดยตั้งใจ** (index `0,75,86,87,145,147,148`) -- resolve ได้ id ที่ไม่มีแถวใน MOBS
(`155,819,9107,937,942`) หรือได้ `0` ⇒ เลนนี้ไม่เดา · index 0 = จุดบนท่าเรือข้าง Columbus ·
**ว่างคือของถูก ห้ามรายงานเป็น regression**

### objective
บนบูตไร้แฟล็ก ชื่อที่ไคลเอนต์แสดงให้ NPC ของ bg0001 = แถว `MOBS` ที่ resolve ผ่าน CLINE ใช่หรือไม่

### คำทำนาย (ผิด = ผล ไม่ใช่ความล้มเหลว) · P1/P2 คือสมอของเจ้าของเอง (`PANYA-DECISION 2026-08-27 09:50`)

| # | placement | เคยเห็น | ต้องเห็นรอบนี้ (n_ID) | ที่สังเกต |
|---|---|---|---|---|
| P1 | 1 | `Sebastian` | `Columbus / Marine Transport Station` (156) | ท่าเรือ ข้างเรือลำใหญ่ |
| P2 | 65 | `Columbus` | `Loie / Royal Navy Engineer` (802) | ข้างปืนใหญ่ฐานแดง |
| P3 | 4 | -- | `Hields / Guild Administrator` (159) | ลานดอกไม้+ม้านั่ง 2 ตัว · **คู่ของเขา (placement 59) ยังเป็น `Toxic Vine` ดูแถบแดงข้างล่าง** |
| P4 | 3 / 90 | -- | `Dorothy` (158) **ไม่มีบรรทัดตำแหน่ง** / `Melody / Grocer` (903) | -- |
| P5 | 91 | -- | `Chalais / Illustrations Appraisers` (904) | คู่ของเขาคือ placement 30 ซึ่ง **ยังเป็น `Tornado Eagle`** (แถบแดงข้างล่าง) |

🔴 **13 placement ที่ยัง "ชื่อผิด" อยู่ และนั่นคือของถูกในรอบนี้ ห้ามรายงานเป็น FAIL:**
`12, 30, 33, 58, 59, 60, 63, 95, 103, 105, 107, 109, 132` — `runtime.py` splice โรสเตอร์ศัตรูของ
สาย B (`field_mob_tables.py` ซึ่งยัง generate ด้วยกฎเก่า) ทับ census หลังจากสาย A ประกอบเสร็จ
⇒ **95 จาก 108 ตัวได้ชื่อใหม่ · 13 ตัวยังเป็นของเดิม** · ยกให้สาย B แล้วในจดหมาย
`20260828_2305_LANE-A-STATUS-runtime-splice-*` · **ถ้าผู้เทสเห็น 13 จุดนี้เป็นชื่อเก่า = ตรงตามคาด**
ถ้าเห็น **จุดอื่นนอก 13 นี้** เป็นชื่อเก่า = **นั่นคือของจริงที่ต้องรายงาน**

- **P6 [สัญญาณเดี่ยวที่แรงที่สุด]** หน้าต่างแผนที่ (`M`) ลิสต์ "find character in scene" ต้องเรียงตาม n_ID
  `156,157,158,...` แบบในวิดีโอเจ้าของ -- ด้วย id ชุดเก่า ลิสต์นี้ถูกไม่ได้เลย · กด `GO!` หนึ่งแถวแล้วจดผลที่เห็น
- **P7** 7 จุดข้างบน **ว่าง** ยืนยันด้วยตา (จุดไหนเดินไม่ถึง เขียนว่าไม่ได้ตรวจ ห้ามเดา)
- **P8** `n_ID 917` ไม่มีแถว `MOBS_TIP` ⇒ actor หนึ่งตัวไม่มีบรรทัดชื่อโดยชอบธรรม -- จด ไม่ใช่ข้อบกพร่อง
- **P9 [ตัวหักล้าง ค่าเท่ากับ PASS]** ชื่อยังเป็นชุดเดิม/ยังเห็นชื่อมอนที่ 30 ทั้งที่คอนโซลขึ้น `identity=CLINE:108 shipped`
  ⇒ ไคลเอนต์ไม่ได้ใช้ id ที่เราส่งตัดสินชื่อ ⇒ redirect กลับ `RE-128` (static) **ไม่ใช่เปิดใบเทสใหม่**

### server args (เป๊ะ -- "ไม่มีแฟล็ก" คือส่วนหนึ่งของสิ่งที่ทดสอบ)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt131.sqlite3
```
client `-SecondPasswordMode bypass` · 🔴 ห้ามมี `--*-scenario` / `--world-census-actors` / `--export-events` แม้ตัวเดียว
ก่อนบูต: `pf_resolve_green_boot.py --fetch` (เอาเฉพาะ exit 0 + `BOOT_COMMIT`) แล้ว
`git grep -n "identity_resolved" <SHA> -- src/pirateforce_foundation/` · 0 hit = `<SHA>` เก่ากว่างานรอบนี้ ⇒ fetch ใหม่

### ขั้นตอน (~25-35 นาที · อัดวิดีโอต่อเนื่องทั้งช่วง `LOCK_GAME`)
1. ของมาตรฐานทั้งหมดตาม `ATTENDED_SESSION_RUNBOOK.md` (LOCK · สำเนา DB · `CANON_SHA` ก่อน-หลัง ·
   เซิร์ฟเวอร์ก่อนไคลเอนต์ · teardown ภายใน 420 นาที · กฎสีป้ายชื่อ · หลักฐานครบทุกข้อ)
2. เข้าเกม -> T0 ภาพนิ่ง full-res + HUD X/Y -> NO-CRASH ด้วย **right-click-drag** (🔴 ห้าม `Q`/`E`)
3. 🔴 **ห้ามพิมพ์ตัวอักษรใด ๆ** ยกเว้นกด `M` ในข้อ 5
4. เดินทัวร์ `W/A/S/D` ตามลำดับ ถ่ายภาพนิ่ง full-res + HUD X/Y ทุกจุด: ท่าเรือ (1 และจุดว่าง 0) ·
   ลานดอกไม้ (4, 59) · (3, 90) · (30, 91 ให้อยู่เฟรมเดียวกันอย่างน้อยหนึ่งภาพ) · ปืนใหญ่ฐานแดง (65)
   · ทุกจุดจด **ชื่อ/บรรทัดตำแหน่งที่อ่านได้จริง ตัวอักษรเป๊ะ** (ไม่มี = เขียน "none")
5. กด `M` -> ถ่ายลิสต์ให้อ่านออกทั้งลิสต์ -> จด 10 แถวแรก -> กด `GO!` หนึ่งแถว -> ถ่าย/จดผล
6. NO-CRASH ซ้ำ -> ออกจากเกม -> 🔴 restart เซิร์ฟเวอร์ก่อนบูตถัดไป -> teardown
เฉพาะใบนี้: เก็บ `state\run_gt131.sqlite3` ไว้ให้ chief re-derive · บรรทัด `WORLD_CENSUS` ให้ **คัดลอกตัวอักษร ไม่ใช่ถ่ายรูป**

### pass criteria (สองชั้น แยกกัน ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)
**wire/DB** -- grep stdout+stderr รวมกัน (`2>&1`) ด้วย `WORLD_CENSUS` ต้องได้บรรทัดที่มีครบ:
`assembled=108/115` · `wire=108` (ไม่ใช่ `MISMATCH`) · `bodies=ok` · `source=identity_resolved` ·
`shortfall=identity_resolved=108` · ลงท้าย `identity=CLINE:108 shipped,7 unresolvable`
🔴 เห็น `115` ตรงไหนบนบรรทัดนั้น = การเปลี่ยน identity ไม่ทำงานในบูตนั้น ⇒ จดทั้งบรรทัด ·
`sessions` +1 · `max(lease_generation)` ไม่ถอย · `integrity_check`=`ok` · sha canonical ตรงก่อน-หลัง
**client-observable** -- P1 **และ** P2 ถูกทั้งคู่บนภาพนิ่ง (แกนของการตรวจรับ) · P3/P4/P5 ตรงตาราง
รวม Dorothy ที่ไม่มีบรรทัดตำแหน่ง · P6 ลิสต์ `M` เรียงตาม n_ID · P7 จุดว่างว่างจริง · NO-CRASH ผ่านสองครั้ง

### nonclaims (ติดไปกับผลทุกกรณี)
1. 🔴 ไม่อ้างว่าไคลเอนต์อ่าน CLINE เอง (nonclaim ที่ยังเปิดของ `RE-128`) -- ใบนี้ตอบชั้น client-observable:
   ชื่อบนจอถูก = id ที่เราส่งถูก ไม่ว่าไคลเอนต์อ่านจากตารางไหน
2. 🔴 ไม่อ้างว่าร่าง/โมเดลถูก เกินกว่า "ใช้ `s_OUTFIT` ของ id ที่ resolve ได้" -- **ร่างผิดแต่ชื่อถูก = จด ไม่ใช่ FAIL**
3. `n_ID 910` (Saben) มี `s_OUTFIT` เป็น **รายการหลายตัวคั่นด้วย `;`** สาย A ส่ง **ตัวแรก** เพราะส่งทั้งสตริง
   = ชื่อไฟล์ที่ไม่มีจริง ⇒ ไม่มีร่าง · **ถ้า Saben หน้าตาไม่เหมือนของเดิม = จด ไม่ใช่ FAIL** [สมมติของสาย A - รอ COO ยืนยัน]
4. ไม่อ้างอะไรเรื่อง hp / aggro / เควสต์ / แหล่งแพ็กเก็ตของลิสต์ในหน้าต่างแผนที่
5. ไม่ปิด `GT-078` แทนเจ้าของ ไม่ประกาศ milestone ใด ไม่ใช้สถานะ GM
6. ไม่ชี้สาเหตุของสีป้ายชื่อ (`RE-067` เปิดอยู่) · ผู้เทสคนเดียว บูตเดียว

**ผู้เปิดใบ: LANE-A (รอบ `pqx4fj`)** -- ผลกลับมาที่สาย A บริโภค

### result (ผู้เทสกรอก)
```

```
---

## 🆕🎮 GT-132 GROUND-DROP-COALESCED-GENERATION-DRAWS-N-LABELS-001 [attended, in-game]: **ฆ่ามอนตัวเดียวที่ตกของหลายชิ้น แล้วนับว่ามี "ป้ายชื่อไอเทมสีแดง" ขึ้นกี่ป้าย**

> NUMBERING: จอง `GT-131` ตอนเปิดรอบ (grep = 0 hit) แต่ **สาย A รอบ `pqx4fj` merge `GT-131` เข้า main ก่อน**
> ⇒ ตามกฎ "ชนแล้วห้ามทับ" ใบนั้นอยู่ที่เดิม ใบนี้ขยับเป็น `GT-132`
> 🟢 **READY — attended · ศูนย์สล็อต ไม่มีแฟล็ก** · เปิดโดย LANE-B รอบ `zxnwtd` (2026-08-28T23:0x+07:00)
> ต่อจาก `RE-130` ✅ CLOSED · **ต้องรันบนบิลด์ที่มี PR รอบ `zxnwtd`** — ด่านบิลด์ข้างล่างเป็นตัวบังคับ

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
