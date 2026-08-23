# FINDINGS R128 — GT-051 RENDER-SYNTHESIS-001: เคสไหนไคลเอนต์วาดของจากเซิร์ฟเวอร์สำเร็จ เคสไหนไม่วาด และต่างกันตรงไหน

**ผู้เขียน:** chief cloud (cc) รอบ R128 (session c7swu2) · 2026-08-23 ~18:1x–18:4x (+07:00)
**ที่มา:** คำสั่ง Panya 16:56 (+07:00) `notes_to_chief/20260823_1656_PANYA-DIRECTION-pause-attended-open-class-skill-lane.md` ข้อ ④ ร่าง GT-051
**ชั้นหลักฐาน:** 🔴 **สังเคราะห์เอกสารที่ commit แล้วล้วน ๆ — ไม่มีหลักฐานใหม่แม้แต่ไบต์เดียว** ·
ทุกข้อสรุปห้ามยกระดับเกินหลักฐานต้นทางของแต่ละเคส · เกรดของเอกสารนี้ = **สมมติฐานที่มีหลักฐานสอดคล้อง (ไม่ใช่ข้อพิสูจน์)**
**วิธีทำ:** ลูกมือ pf-static-re สองตัวขนานกัน (ฝั่ง render-FAIL / ฝั่ง render-SUCCESS) · chief สังเคราะห์ ·
**pf-adversary ตรวจก่อน commit และหักล้างร่างแรกสำเร็จหนึ่งประเด็นใหญ่** (ดู ② — รูปแรงของสมมติฐานร่างแรกตายด้วยรายงานยุคก่อน GT
ที่การกวาดรอบแรกไม่ครอบ: ARENA V1 · SCENE-007 · SCENE-002..006) — ฉบับนี้คือฉบับหลังแก้

---

## ① ตารางหลัก — ทุกเคสที่มีผลชั้นจอ เรียงตามคำตัดสิน

**นิยาม "band":** identity อยู่ในช่วง `0x2000+1 .. 0x2000+N` เมื่อ N = จำนวน placement ในไฟล์ฉาก native ของฉากที่โหลด
(bg0001 มี 115 placement ⇒ band = `0x2001..0x2073` · สูตร `0x2000+placement_index+1` ยืนยันจาก GT-022/GT-048/v141)

### กลุ่ม "วาดได้ / entity เปลี่ยนสถานะบนจอ"

| เคส | ช่องทาง/กลไก | entity·identity | in-band? | ตำแหน่ง/template ตรง native? | ชั้นจอ | ข้อจำกัดเกรด |
|---|---|---|---|---|---|---|
| GT-022 | actor_entry bit `0x02` (SPAWN/DYING_LATCH/DEATH_TASK) | NPC `0x2001` Navy Transfer P0 | ✅ | ✅ ตรง (อัปเดตตัว native ในที่เดิม) | ยืน→**นอนราบค้าง** (Panya ถ่ายเอง) | attribution ไป DYING_LATCH = ข้อบ่งชี้หนัก ไม่ใช่พิสูจน์ |
| GT-031 | VitalData `update_attr 12442` hp mask 4/8/128 | **actor ผู้เล่นเอง** `0x10010001` | ✅ (self) | — | หลอด 100→37→0 + **ตัวละครนอน** + `Common_Death` | ช่วง ~45–100 วิ unobserved |
| GT-039 | สองสายพาน: VitalData + actor_entry (actor_type 4) | เป้า NPC `0x2001` | ✅ | ✅ ตรง | แถบเป้า 100→37→0 + **NPC ล้มจริง** | unattended · ไม่มีวิดีโอ |
| GT-032 | actor_entry faction mask_bit 1024 ค่า 6 | NPC `0x2001` | ✅ | ✅ ตรง | Tab แล้วแผงเป้าแดง+ไอคอนศัตรู | เส้นขอบแดง = ของ Tab (GT-043 ตอบ) |
| GT-043 | เฟรม count-1 bit `0x02` (host) | Navy Transfer + วัตถุฉาก native | ✅ | ✅ | ทุกอย่าง**ยังอยู่** +3.5s..+10s | 0–3.524s unobserved |
| **ARENA V1** (ก่อนยุค GT · `reports/PF_FOUNDATION_ARENA_V1_RUNTIME_PASS_CLASSIFICATION_NEGATIVE_20260815.md`) | wire spawn actor_entry | Tornado Eagle `0x201F` scene 1 | ✅ (index 30 < 115) | 🔴 **ไม่ตรง — วาด "near the player" ที่พิกัดที่ wire กำหนด ไม่ใช่พิกัด native P30** · report เขียนเอง "authentic P30 placement not proven" | **โมเดลนกวาดสำเร็จ** | ก่อนยุคเกณฑ์สองชั้น |
| **SCENE-007** (ก่อนยุค GT · `reports/PF_SCENE007_PORT_ROYAL_EA7D_ACTION_ACK_RUNTIME_PASS_20260816.md`) | wire actor_entry | Fighting Fish soldier `0x203D` **ยิงเข้า scene 1** ที่พิกัด P144 · template 34 | ✅ (index 60 < 115) | 🔴 **ไม่ตรง — index 60 ของ bg0001 ใน v141 คือ template 62 `Ancient Civilization Alert Weapon` คนละตัวคนละตำแหน่ง** | **วาดสำเร็จ ทั้งสอง actor ใน default camera frame** | ก่อนยุคเกณฑ์สองชั้น |
| SCENE-005 (ก่อนยุค GT) | remote_actor หลัง runtime ack | Fighting Fish soldier `0x203D` scene 2 · พิกัด P60 (authentic ตาม ledger GEO-PF-002) | ⚠️ **band ของ scene 2 ยังไม่รู้ N — GT-053 ไปตอบ** | พิกัด entity = ค่า authentic P60 (ตัวสังเคราะห์คือตำแหน่ง**ผู้เล่น**) | ชื่อชมพู/แดง + ขอบแดง + Tab เลือกได้ | จุดตรวจของ GT-053 |
| SCENE-002..006 (ก่อนยุค GT · `docs/EXPERIMENT_LEDGER.md`) | wire | Fighting Fish soldier | (scene 2 — N ยังไม่รู้) | — | "rendered with exact name/model" ตั้งแต่ SCENE-002 | บันทึก ledger ระดับแถว |
| OBJECT-POP-002 (ก่อนยุค GT · Grade B) | population 20 actor-entry byte-identical V141 | หลายตัว | ไม่ทราบรายตัว | — | พยานตาเปล่า **ไม่ผูกกับ entrant รายตัว** | เกรดต่ำสุดในตาราง |

### กลุ่ม "UI overlay" (แยก pipeline เชิงพฤติกรรมจาก entity — หลักฐานในตัว)

| เคส | สิ่งที่วาด | หลักฐานว่าคนละเส้นกับ entity |
|---|---|---|
| GT-027/028/038 | เลขดาเมจลอย `63`/`379`/`MISS!` | เลขขึ้นแต่ **HP bar ไม่ขยับ** แม้สะสม 505 · toggle `[localplayer+0x420]` ปิดเลขทั้งจอโดย wire ไม่เปลี่ยน · GT-038: ไม่เลือกเป้าก็เห็นเลข |
| GT-029 | วงนับถอยหลัง 19→…→หาย | **client เดินเอง** — ไม่มีเฟรม wire ป้อนหลัง DYING_LATCH (static R102 ยืนยัน UI นับเอง) |
| GT-031/039 | หลอด HP (ผู้เล่น/เป้า) | ผูกกับเฟรม hp เท่านั้น ไม่ผูกเฟรมเลข |

🔴 ทุกเคส overlay: **ไม่ claim ว่าเป็น "คนละ pipeline ในโค้ด client" ระดับ VA** — ที่มีคือหลักฐานพฤติกรรมแยกกัน ไม่ใช่การไล่โค้ด render

### กลุ่ม "ไม่วาด / ไม่เห็น"

| เคส | ช่องทาง/กลไก | entity·identity | in-band? | ชั้น wire | ชั้นจอ | น้ำหนักผลลบ |
|---|---|---|---|---|---|---|
| GT-030 | actor_entry bit `0x02` **actor_type 2** (remote player) 5 เฟรม | probe `0x00A00001..3` | ❌ นอก band | ครบ 5 เฟรม (label+size ตรง · ไม่มี refusal) | **CLIENT NO-RENDER** — เดินถึงพิกัด (B ห่าง ~33 หน่วย · A-หลัง-MOVE ~52 หน่วย) กวาด Q + Tab ไม่เห็นอะไรเลย | **แข็งที่สุดในสามเคส** แต่แคบ: "ใต้ mask/เฟรมชุดนี้เท่านั้น" · 🔴 **ต่างจากกลุ่ม success สองแกนพร้อมกัน** (identity นอก band **และ** actor_type 2) — ดู confound ใน ② |
| GT-045 v1 | bit `0x08` element mask `0x12` (2 เฟรม) | ground-loot key `1`/`2` | ❌ (คนละชนิดเรคคอร์ด — ไม่ใช่ actor_entry ด้วยซ้ำ) | **WIRE EXACT** — sha ตรง pin | **NO-RESULT** — ภาพแรก +3.560s · geometry ตายจาก spawn drift | อ่อน: ไม่ใช่การเทสแกน identity ตรง ๆ |
| GT-034 | **ไม่มี wire สร้าง entity เลย** (load-only) — พึ่ง native path ล้วน | Tornado Eagle `0x201F` P30 | ✅ แต่เส้นทางคือ native ไม่ใช่ wire | จัดฉากถูก (StartGameRes f32 exact · ไม่มี splice) | **NO-RESULT** — ถึงพิกัด กวาด 360° ไม่เห็นนก | อ่อน: แยกไม่ได้ว่า "client ไม่ spawn เอง" หรือ "เงื่อนไข render อื่น" · **คู่ตรงข้าม ARENA V1: identity เดียวกัน wire วาดได้ / native-only ไม่เห็น** |

---

## ② คำตอบของใบ — สองชั้น: สิ่งที่หลักฐานหักล้างแล้ว กับสมมติฐานที่ยังยืน

### ❌ สิ่งที่ตายแล้วในรอบสังเคราะห์นี้เอง (pf-adversary หักล้างร่างแรกสำเร็จ)

ร่างแรกของเอกสารนี้เสนอว่า *"wire actor_entry = อัปเดตสถานะของ native ในที่เดิมเท่านั้น ไม่ใช่สร้าง/ย้ายตัว"* —
**รูปแรงนี้ผิด**: ARENA V1 วาด `0x201F` ที่พิกัดที่ wire กำหนด (ไม่ใช่พิกัด native P30) และ SCENE-007 วาด `0x203D`
ใน scene 1 ด้วย template 34 ที่พิกัด P144 ทั้งที่ index 60 ของ bg0001 คือ template 62 คนละตัวคนละที่
⇒ **wire override ตำแหน่งและ template ของ identity ใน band ได้ และ client วาดตาม wire**

### สมมติฐานที่ยังยืนหลังแก้ (H1 ฉบับ identity-band)

> **H1 (แก้แล้ว):** ไคลเอนต์วาด entity จาก wire actor_entry **เมื่อ identity อยู่ใน band ของฉากที่โหลด**
> (`0x2000+1 .. 0x2000+N` · N = จำนวน placement ในไฟล์ฉาก native) หรือเป็น actor ของผู้เล่นเอง —
> โดย wire กำหนดตำแหน่ง/template ทับได้ · identity **นอก band ไม่วาด** (หลักฐาน: GT-030)

- สอดคล้องทุกเคสในตาราง ① — success ทุกใบ in-band (หรือ self) · fail ที่เป็น wire ล้วน out-of-band
- 🔴 **confound ที่ต้องเขียนตรง ๆ:** GT-030 (ผลลบแข็งใบเดียว) ต่างจากกลุ่ม success **สองแกนพร้อมกัน** —
  identity นอก band *และ* `actor_type 2` (ทุก success คือ actor_type 4/self) ⇒ **"actor_type 4 คือตัวแยก" อธิบายตารางเดียวกันได้ครบเท่า H1**
  หลักฐานที่มีตอนนี้แยกสองสมมติฐานนี้ไม่ได้ · A/B ในอนาคต (④ ข้อ 3) ต้อง**ตรึง actor_type 4 แล้วสลับเฉพาะ identity**
- คำถามที่ H1 ไม่ตอบและยังเปิดอยู่ (adversary ชี้): เมื่อ wire วาด identity ใน band ที่ template/พิกัดไม่ตรง native —
  client **ย้าย/เปลี่ยนสกิน object native ตัวเดิม** หรือ **สร้าง object ที่สอง** (native ตัวเดิมยังยืนอยู่ที่เดิมไหม)?
  ไม่มีใบไหนเคยวัด — เป็นคำถาม attended (พักตามคำสั่ง 16:56) จดไว้ใน ④ ข้อ 4
- GT-034 ยังเป็นข้อค้านฝั่ง native: identity ใน band แท้ ๆ แต่ **native-only (ไม่มี wire) ไม่เห็นตัว** ขณะที่
  ARENA V1 identity เดียวกัน **wire วาดได้** ⇒ ฝั่ง native มีเงื่อนไข spawn/render เพิ่มที่ยังไม่รู้ (GT-048 เปิดช่องไว้)

**ความอ่อนของหลักฐาน (ห้ามอ่านข้าม):** ผลลบแข็งจริงมีใบเดียว (GT-030) และแคบ + ติด confound ·
GT-045/GT-034 เป็น NO-RESULT · band ของ scene 2 ยังไม่รู้ N (GT-053 ไปตอบ) · เคสยุคก่อน GT เป็นหลักฐานชั้นเดียว/เกณฑ์เก่า

---

## ③ ผลกระทบต่อเลนที่ค้าง (คำถามพ่วงของใบ: "ลูท/ดาเมจยืนบนฐานมั่นคงไหม")

1. **เลนลูท (GT-045 v2):** ถ้า H1 ถูก — bit `0x08` key `1`/`2` เป็นคนละชนิดเรคคอร์ดกับ actor_entry และ key นอก band
   ⇒ มีเหตุให้คาดว่าไม่วาด ไม่ว่าพิกัดถูกแค่ไหน · GT-045 v2 (merge แล้ว · พักรอ Panya) จึงเป็น**ตัวทดสอบข้างเคียงของ H1**:
   วาดได้ = ช่อง render ของ loot ไม่ขึ้นกับ band ของ actor_entry (H1 ไม่ตายแต่แคบลง) · ไม่วาด = สอดคล้อง H1 — สอง outcome มีค่าทั้งคู่ ยิ่งควรรัน attended จริง
2. **เลนดาเมจ:** **ไม่กระทบ** — overlay (เลข/หลอด/แผงเป้า) พิสูจน์เชิงพฤติกรรมแล้วว่าแยกจาก entity render · ฐาน DAMAGE-MODEL ทาง 1 ยังมั่นคง
3. **multiplayer (remote players / GT-030):** 🔴 งาน static ที่ถูกต้องถัดไปต้องเปิด**คำถามคู่** ไม่ใช่คำถามเดียว —
   (ก) มีช่อง instantiate identity นอก band ไหม (แกน identity-band) และ (ข) dispatch ของ **actor_type 2** ฝั่ง client
   ต่างจาก actor_type 4 ตรงไหน (แกน confound) · อย่าเปิดใบจนกว่า GT-053 จะตัดสิน band ของ scene 2 (ยังไม่เปิดใบ — รอผลก่อน อย่าเปิดซ้อน)

---

## ④ สิ่งที่ต้องเก็บเพิ่ม — เรียงจากถูกไปแพง

1. 🆕 **GT-053 SCENE2-NATIVE-IDENTITY-CROSSCHECK-001 [STATIC-ON-BRIDGE]** (ใบใหม่ ท้ายคิว) —
   **เกณฑ์ชี้ขาดหลัก = band membership:** ไฟล์ฉาก native ของ scene 2 มี placement **≥ 61 ตัว** ไหม
   (มี ⇒ `0x203D` in-band ⇒ H1 รอด · ไม่มี ⇒ SCENE-005 วาด identity นอก band ⇒ **H1 ตายทันที**) ·
   identity/template ที่ index 60 และ **f32 triple เทียบพิกัด authentic P60 ของ scenario** = หลักฐาน verify การ parse
   (พิกัด entity ใน scenario เป็นค่า authentic — ตัวที่สังเคราะห์คือตำแหน่ง*ผู้เล่น* ตาม ledger GEO-PF-002)
2. **GT-045 v2 attended** (พักรอ Panya อยู่แล้ว) — ตัวทดสอบข้างเคียงฝั่ง non-actor_entry
3. (อนาคต · ยังไม่เปิดใบ · attended พัก) A/B **ตรึง actor_type 4** เฟรมโครงเดียวกัน: identity in-band (เช่น `0x2002`)
   เทียบ identity นอก band — แยก H1 ออกจากสมมติฐาน actor_type ให้ขาด
4. (อนาคต · attended พัก) คำถาม "update-in-place หรือ instantiate-on-miss": ยิง in-band identity ที่พิกัด/template
   ไม่ตรง native (แบบ SCENE-007) แล้ว**เดินไปดูพิกัด native ตัวเดิม** ว่ายังมี object ยืนอยู่ไหม

## nonclaims ของเอกสารนี้
- **ไม่มีหลักฐานใหม่** — ทุกแถวคือการจัดเรียงของเก่า ห้ามอ้างเอกสารนี้แทนเอกสารต้นทาง
- **H1 เป็นสมมติฐาน** — ยืนบนผลลบแข็งใบเดียว (GT-030 · แคบ · ติด confound actor_type) + NO-RESULT สองใบ
- ไม่ claim ว่า overlay/entity เป็นคนละ pipeline ระดับโค้ด — หลักฐานเป็นเชิงพฤติกรรม
- ไม่ claim พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้วและกู้ไม่ได้ตลอดกาล — ทุก mask/เฟรม/สูตรเป็นดีไซน์ของเรา
- ไม่ claim ว่า band `0x2000+p+1` ใช้กับทุก scene — ยืนยันจริงเฉพาะ bg0001 (N=115) · scene 2 คือหน้าที่ของ GT-053
- เคสยุคก่อน GT (ARENA V1 / SCENE-002..007 / OBJECT-POP-002) เป็นหลักฐานตามเกณฑ์ยุคนั้น — ใช้หักล้าง/สนับสนุนโครงได้ แต่ห้ามอ้างเป็นหลักฐานสองชั้นแบบยุค GT
