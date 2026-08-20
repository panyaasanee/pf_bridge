# FACTPACK R102 — DYING-COUNTDOWN-UI-FIELD-001 — "วงกลม + เลขแดง" เหนือ NPC ที่กำลังตาย อ่าน `attr.f32[+0x58]` สด หรือเป็นสำเนาที่ UI นับเอง?

**2026-08-20 · assistant lane (ลูกมือ static RE, chief รอบ 102) · static RE เท่านั้น · report-only · additive · ไม่บูต server · ไม่เปิด GameClient · ไม่แตะ DB · ไม่ commit**

**คำถามต้นทาง:** GT-029 (runtime) — หลังเซิร์ฟเวอร์ส่งเฟรม DYING_LATCH (`BasicAttr` bit `0x0080` = death timer 20.0f) NPC ล้ม แล้วมี "วงกลม + ตัวเลขสีแดง" ลอยเหนือ NPC และ **ตัวเลขลดลงเองตามเวลา** (จับได้ 19 -> 15 -> 13 -> 10 -> หาย) โดยเซิร์ฟเวอร์ **ไม่ส่งเฟรมใดตามมาอีก** · ถามชี้ขาด: UI นับถอยหลังตัวนี้ **อ่าน field เดียวกับ predicate ตาย (`attr f32 +0x58`)** หรือ **เก็บสำเนาของตัวเองไว้เรนเดอร์**?

---

## หัวไฟล์ / provenance

| รายการ | ค่า |
| --- | --- |
| ไบนารีหลักฐาน (อ่านอย่างเดียว) | `GameClient/GameClient.local.bin` |
| SHA-256 (ตรวจแล้วในรอบนี้) | `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623` |
| PE | 32-bit, ImageBase `0x400000` |
| `.text` | VA `0x401000`, rawoff `0x400`, rawsz `0x838C00` |
| เครื่องมือ | `capstone 5.0.7` + byte-scan (`E8 rel32` call index, dword-immediate scan) บน scratch ใน `/tmp` · print เฉพาะ ASCII |
| หลักฐานชั้นสอง (อ่านตรง ๆ) | `GameClient/Data/GUI/Model/*.model` (XML) |
| รายงานอ้างอิงก่อนหน้า | `reports/PF_RESCUE_AND_DEATH_ESCALATION_STATIC_20260819.md` (predicate ตาย, DURATION_DYING, Merge polarity) |

**เกรดหลักฐาน:** `[PROVEN]` = span instruction ที่ address ตายตัว / slot vtable / literal / ค่าใน .data ที่อ่านตรง ๆ · `[LIKELY]` = อนุมานจาก [PROVEN] + รูปทรงโค้ด (บอกชัดว่าอนุมาน) · `[UNKNOWN]` = ยังไม่ได้พิสูจน์

---

## 0. คำตัดสิน (อ่านย่อหน้าเดียวพอ)

**(ข) UI เก็บสำเนา/นับเอง — field `attr.f32[+0x58]` ถูกแช่แข็ง · GT-021 ยังถูก · เฟรมที่สี่ (timer=0.0) ยังจำเป็น** — `[PROVEN]`

เหตุผลสามชั้นที่ล็อกกันเอง:
1. **`BasicAttr.f32[+0x58]` ไม่มี writer ที่ลดค่าตาม frame delta เลย** — ไม่ว่าจะเป็น float หรือ integer · ผู้เขียนทุกตัวที่แตะ `[BasicAttr+0x58]` คือ ctor(`=0.0f`) / copy-ctor / `Merge`(คัดลอกค่าเดิม) / wire-load(เมื่อบิต `0x80` ติด) — **ไม่มี sub/subss/dec** (section 2)
2. **ผู้อ่าน `[BasicAttr+0x58]` แบบ float มี 3 ที่ ทั้งหมดเป็น predicate/gate อ่านอย่างเดียว และ ไม่มีตัวไหนแปลงเป็นเลขเพื่อแสดงผล** — ไม่มีฟังก์ชันใดที่อ่าน `[reg+0x58]` แล้วเรียก sprintf/FxNumber/progressbar setter (section 1, section 3)
3. **ตรรกะปิดคดี (runtime x static):** เมื่อ (ก) เซิร์ฟเวอร์ไม่ส่งเฟรมต่อ และ (ข) client ไม่มี decrementer -> `attr+0x58` **แช่แข็งที่ 20.0** · widget ที่อ่าน `attr+0x58` สดจะแสดง **เลขคงที่ 20** ตลอด · แต่ผู้เทสเห็นเลข **ลดลง** 19->10 -> ดังนั้นเลขที่ลดนั้น **เป็นไปไม่ได้ที่จะเป็นการอ่าน `attr+0x58` สด** ต้องเป็นสำเนาที่ตัว UI นับเองด้วย client clock/frame-delta (section 4)

**ผลต่อ GT-021 และเฟรมที่สี่:** สาขา (ก) "client ลด `attr+0x58` จริง" = **เท็จ** -> ข้อสรุป GT-021 ("client ไม่ลด hp_death_timer เอง") **ยังถูก** และเฟรมที่สี่ (`0x0080`=`0.0f` เพื่อให้ `vt+0x3C` เป็นจริง แล้ว escalate เป็น `Common_Death`) **ยังจำเป็น**

**สิ่งที่ ไม่ ยืนยัน:** ตัว widget "วงกลม+เลขแดง" เหนือ NPC ตัวจริงยังไม่ถูก byte-pin เป็นชิ้นเดียว (ดู section 4 + section 6 nonclaim) · แต่ **ไม่ว่ามันจะเป็น widget ไหน คำตัดสินก็คงเดิม** เพราะไม่มี widget ใดในอิมเมจอ่าน `attr+0x58` เพื่อแสดงเลข และ field นั้นแช่แข็ง

---

## 1. ผู้อ่าน `[BasicAttr+0x58]` แบบ float — 3 ที่ ทั้งหมด predicate/gate อ่านอย่างเดียว `[PROVEN]`

บริบท attr: getter = `CNetActor` vtable `+0x74` = `0x44C630` = `mov eax,[ecx+0x348]` · ctor `BasicAttr` = `0x464B0E` (ตั้ง `[obj+0x58]=0.0f`) · ผู้อ่าน float ที่อยู่ในฟังก์ชันซึ่งมี `mov r,[r+0x348]` (getattr) ทั้งหมด:

| VA (read) | off | bytes (span) | ฟังก์ชัน | ทำอะไรกับ `+0x58` |
| --- | --- | --- | --- | --- |
| `0x454A7D` | `0x53E7D` | `0f57c0 0f2f4058 722e` (span `0x454A7A`) | `0x454A70` = `vt+0x3C` predicate ตาย | `comiss 0.0,[attr+0x58]; jb` -> คืน false ถ้า `0.0<timer` หรือ NaN · **เทียบเฉย ๆ** |
| `0x454ACA` | `0x53ECA` | `f30f104058 0f2f059c98f000 762e` | `0x454AC0` = `vt+0x40` IsDying | `movss [attr+0x58]; comiss const0(0xF0989C=0.0); jbe` -> ต้อง `timer>0` · **เทียบเฉย ๆ** |
| `0x44A56D` | `0x4996D` | `f30f104058 f20f2a0d 9c240201 f20f5c0d d092f000 0f5ac0` | `0x44A540` = Main_Dead open-gate | `movss [attr+0x58]; cvtsi2sd DURATION_DYING(=20); subsd 0.5 ...` -> เทียบ `19.5 vs timer` · **เทียบเฉย ๆ** |

**สำมะโนเชิงเครื่อง:** จำนวนฟังก์ชันที่ float-read `[reg+0x58]` (movss/fld/comiss/...) ทั้ง `.text` = **81 ฟังก์ชัน** · ที่มี getattr(`+0x348`) marker = **3 ฟังก์ชัน** = สามตัวข้างบนพอดี · **ไม่มีตัวไหนใน 81 เรียก number formatter จริง** (0x894D20 wide-`%d`, 0x896100 ascii-sprintf, 0x43FBB0 FxNumber-spawn, 0xA7EBA0 glyph-builder, 0x472430 progressbar-SetValue) — **0 hit** (section 3)

> `0x88F2B0` เคยติดธง SPRINTF ตอนคัดกรองหยาบ แต่ตรวจแล้วมันคือ **list-walker** (`while([eax+4]) cmp ecx`) มีผู้เรียก 4597 ที่ = helper ทั่วไป ไม่ใช่ formatter -> false positive ตัดทิ้ง

---

## 2. Writer ทุกตัวที่เขียน `[reg+0x58]` ขนาด 4 ไบต์ — แยก BasicAttr ออกจากคลาสอื่น `[PROVEN]`

**สำมะโนดิบ (นับด้วยเครื่อง):** store 4 ไบต์ไป `[reg+0x58]` ทั้ง `.text` = **437 จุด** (`movss` 115, `fstp` 37, `mov r/m,r32` 242, `mov r/m,imm32` 43)

### 2.1 ผู้เขียนในบริบท `BasicAttr` จริง — ทั้งหมดไม่ลดค่า

| VA | off | bytes | เป็นอะไร |
| --- | --- | --- | --- |
| `0x464B0E` | `0x63F0E` | `f30f114658` | ctor: `movss [obj+0x58], 0.0f` (ตั้งเริ่มต้น) |
| `0x4656A3` | `0x64AA3` | `84c0 7806 d94658 d95f58` | `Merge`: `fld[src+0x58]; fstp[this+0x58]` เฉพาะเมื่อบิต `0x80` **ไม่** ติด (คัดลอกค่าเดิมไปข้างหน้า) |
| `0x4658E8` | `0x64CE8` | `f60380 740f 6a04 8d4658 50 6a2a 8b...` | wire read: อ่าน f32 tag `0x2A` เข้า `[obj+0x58]` เฉพาะเมื่อบิต `0x80` ติด |
| `0x464BB0` | — | (`d95e58` fld/fstp) | copy-ctor: คัดลอกล้วน |

**=> ไม่มีตัวไหน sub/subss/subsd/dec** · เขียนได้แค่ 0.0 (ctor), ค่าเดิม (merge/copy), หรือค่าจากสาย (wire)

### 2.2 ผู้เขียน `[reg+0x58]` ที่ บังเอิญใช้ offset เดียวกัน แต่ **เป็นคนละคลาส** (false positives ที่ต้องตัดออก)

| VA | off | ฐาน `reg` มาจาก | +0x58 คือ | ทำไมไม่ใช่ BasicAttr |
| --- | --- | --- | --- | --- |
| `0x455DAA` | `0x551AA` | `[actor+0x354]+8` หรือ `[actor+0x80]+8` (render node) | **Vec3.z** (คู่กับ `+0x54`,`+0x5c` = movss เป็น float เวกเตอร์) span `0x455D96` | เป็น scene/render node ไม่ใช่ attr; ในทับซ้อน BasicAttr `+0x5c/+0x5e` เป็น word(level) |
| `0x6E1DAA` / `0x6E1E74` | `0x2E1DAA` | `0x43BC00(this)` (render node) | **Vec3.z** (triad `+0x54/+0x58/+0x5c`) span `0x6E1D99` | ตำแหน่งวิดเจ็ตลอยเหนือ actor ไม่ใช่ attr |
| `0x44D6A7` | `0x4CAA7` | pool `0x102D1A4` (outbound vital) | target-pos ล่าง (คู่ `+0x50` qword, `+0x5c`) span `0x44D693` | object ที่ส่งออกสาย ไม่ใช่ attr ที่รับเข้า |
| `0xABBA4E` | `0x6BAE4E` | `[ecx+0x348]` (attr ของ คลาสอื่น) | **int grid-x** (คู่ `+0x5c` = grid-y, `cvttss2si`) span `0xABBA34` | เขียนเป็น **integer pair** + set flag byte `[attr+0x95]`, `[this+0x3c8]` — layout นี้ไม่มีใน `BasicAttr` (ctor ไม่เคยแตะ `+0x95/+0x3c8`); vtable ผูกที่ `0xF8C054/0xF8C8CC/0xF8DA24/0xF8ED54` = ตระกูลคลาสอื่น |

### 2.3 RMW-decrement detector (read `[reg+0x58]` -> sub -> write กลับ) — ทั่วทั้ง `.text`

**float RMW candidates = 3** ตัว ทั้งหมด **ไม่ใช่ BasicAttr:**

| VA (store) | off | คลาส/หน้าที่ | ทำไมไม่ใช่ BasicAttr |
| --- | --- | --- | --- |
| `0x650BE5` | `0x4FFE5` | lerp/integrator ทั่วไป: `[eax+0x58] -= [edx+0x58]*[ecx+0x10]` (สอง object args) | ไม่มี getattr; sibling `0x650BF0` ใช้ `+0x5c` เป็น float; BasicAttr `+0x5c` เป็น word |
| `0x8130BF` | `0x82D0BF` | anim/physics: อ่าน `+0x40/+0x4c/+0x58` แล้ว `mov [esi+0x54],0` (dword) | BasicAttr `+0x54` = `400.0f` maxHP; การล้างเป็น 0 พิสูจน์ว่าเป็นคลาสอื่น |
| `0x860E61` | `0x45FE61` | smooth-follow: `[ebp+0x58] += step` เข้าหา target `[ebp+0x50]` (curve evaluator ใหญ่ มี sqrtsd) | ไม่มี getattr; `+0x50` ใช้เป็น float target; BasicAttr `+0x50`=0 int |

**integer RMW candidates = 7** ตัว (`0x45EF12, 0x4FB9ED, 0x8C5514, 0x8C6325, 0x9E39A3, 0x9EFBF6, 0xA1E259`) — ตรวจแล้ว **ไม่มี attr(`+0x348`) ในรัศมี +-0x300 เลย** และทุกตัวเป็น **null-on-free** (`[reg+0x58]` เป็น pointer, free แล้วเซ็ต 0) หรือ **list-walk** (`[ebx+0x58]=[[ebx+0x58]]`) — **ไม่มีตัวไหนลบ 1/ลบ delta ของ float timer**

**=> สรุป section 2:** ทั้งอิมเมจ **ไม่มี writer ที่ลด `BasicAttr.f32[+0x58]` ตามเวลา** ทั้งทาง float และ integer · ตัวที่ลด `[reg+0x58]` มีอยู่จริงแต่เป็นเวกเตอร์ตำแหน่ง/ฟิสิกส์/pointer ของคลาสอื่นล้วน

---

## 3. ไม่มี display path อ่าน `attr+0x58` `[PROVEN]`

ตรวจ 81 ฟังก์ชันที่ float-read `[reg+0x58]` ว่ามีตัวใดเรียก formatter/spawner ของ "เลขบนจอ" ไหม:

| formatter/target ที่ค้น | ความหมาย | ฟังก์ชัน read-`+0x58` ที่เรียก |
| --- | --- | --- |
| `0x894D20` | wide-string `sprintf("%d")` (ใช้จริงในสาย damage/UI) | **0** |
| `0x896100` | ascii `sprintf` (จาก DAMAGE-MODEL-001 section 8) | **0** |
| `0x43FBB0` | FxNumber spawn (เลขลอยในโลก) | **0** |
| `0xA7EBA0` | glyph builder (`abs`->`%d`) | **0** |
| `0x472430` | progressbar `SetValue` | **0** |

**=> ไม่มีเส้นทางใดที่อ่าน `[reg+0x58]` (รวมทั้งของ attr) แล้วแปลงเป็นตัวเลข/แถบเพื่อเรนเดอร์**

---

## 4. UI countdown ตัวจริงนับเอง — ตัวอย่างที่ byte-pin ได้: Party revive-notify `[LIKELY]`

widget รูปวง+countdown ที่ลอยเหนือ unit ที่ล้ม อยู่ในตระกูล **`Main_Revive_Notify` / `PANEL_REVIVE_NOTIFY`** (`Party_Main.model`): `UIButton BUTTON_REVIVE` (`bt_saveurlife.tga` = ปุ่มกลม "ช่วยชีวิต") + `UIProgressBar Common_ProgressBar` ชื่อจีน countdown-bar = "แถบนับถอยหลัง" · handler ตระกูล ReviveNotify/ReviveAction อยู่ที่ `0x62876x`-`0x629Dxx` (ผูกจากตารางชื่อ `L"ReviveNotify_Show"` `0xF345E0`, `L"ReviveAction_Show"` `0xF345BC`)

ตัว updater `0x6289D0` นับถอยหลังเอง โดย **ไม่แตะ `attr+0x58`:**

| หลักฐาน | VA | off | bytes | ความหมาย |
| --- | --- | --- | --- | --- |
| ctor ผูก child control เข้า `[handler+0x58]` | `0x6287F6` | `0x227BF6` | span `0x6287EF` `6810fdf100 8bce 894658` | **`[handler+0x58]` = pointer ของ `PANEL_REVIVE_ACTION` (คนละความหมายกับ `attr+0x58` โดยสิ้นเชิง)** — ตัวอย่างชัดของ "คลาสอื่นบังเอิญใช้ +0x58" |
| อ่านฐานเวลา `EXTREMIS_TIME` | `0x628BE5` | `0x227FE5` | `f30f1005 e0250201` | `movss xmm0,[0x10225E0]` = **30.0f** (ไม่ใช่ `attr+0x58`) |
| accumulator ของตัวเอง | `0x628B2A`,`0x628B4D` | — | `test [0x10833F8],1` / `movss xmm0,[0x10833F4]` | flag "เริ่มแล้ว" + accumulator ใน global `[0x10833F4]` สะสมด้วย frame-delta ที่รับผ่าน stack args `[esp+0xc]/[esp+0x10]` |
| ผลลัพธ์ -> progressbar 0..100 | `0x628C58` | `0x228058` | `8b4e58 50 e8d397e4ff` | `call 0x472430` (SetValue) บน child `[handler+0x58]`, clamp ที่ `0x64`=100 |

**=> countdown ตัวนี้อ่านฐานจาก `EXTREMIS_TIME`(30.0) + frame-delta + accumulator global ของตัวเอง แล้ว clamp เป็น 0..100 · ไม่เคยอ่าน `BasicAttr+0x58`**

**ข้อควรระวังที่ซื่อสัตย์:** ฐานของ widget นี้คือ `EXTREMIS_TIME`=30 ส่วนเลขที่ผู้เทสเห็นเริ่ม ~19 (ใกล้ `DURATION_DYING`=20) · ตัวเลขที่จับได้ (19->15->13->10) เป็นการ sample เป็นช่วง จึงบอกฐานแน่นอนไม่ได้จาก static · ไม่ว่าจะเป็น widget นี้ (ฐาน 30) หรือ counter ฐาน-20 ตัวอื่น **ทั้งคู่คือ self-counter** เพราะ (section 1-3) ไม่มี display path ใดอ่าน `attr+0x58` และ (section 2) field แช่แข็ง

**DURATION_DYING(=20) มี value-reader เดียว:** `0x44A576` (Main_Dead gate, section 1) · อีก reference คือ `0x483476` = **การลงทะเบียน config** `register_cfg(L"DURATION_DYING", &0x102249C)` ผ่าน `0x482640` (push address ไม่ใช่อ่านค่า) · `EXTREMIS_TIME` ก็ลงทะเบียนคู่กันที่ `0x4839E8` (`&0x10225E0`, ค่า 30.0f) — ยืนยันว่า Main_Dead gate ไม่แสดงเลข และ 20 ไม่ถูกอ่านที่อื่น

---

## 5. ตัวเลข (นับด้วยเครื่อง)

```json R102_DYING_COUNTDOWN_COUNTS
{
  "binary_sha256": "9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623",
  "candidate_stores_to_reg_plus_0x58_text": 437,
  "float_reader_functions_of_reg_plus_0x58": 81,
  "float_readers_with_getattr_0x348": 3,
  "basicattr_0x58_frame_delta_decrementers": 0,
  "float_rmw_decrement_candidates_total": 3,
  "float_rmw_decrement_candidates_basicattr": 0,
  "integer_rmw_decrement_candidates_total": 7,
  "integer_rmw_decrement_candidates_basicattr": 0,
  "reader_functions_calling_number_formatter": 0,
  "duration_dying_value": 20,
  "duration_dying_value_readers": 1,
  "extremis_time_value": 30.0,
  "extremis_time_global_va": 16786912,
  "const_zero_F0989C": 0.0
}
```
*(extremis_time_global_va 16786912 = `0x10225E0`)*

---

## 6. Nonclaims — สิ่งที่ยัง ไม่ได้ พิสูจน์

1. **ไม่ได้ byte-pin ตัว widget "วงกลม+เลขแดง" เหนือ NPC ตัวจริงเป็นชิ้นเดียว** — `Main_Revive_Notify` (section 4) เป็น candidate ที่เข้าเค้าที่สุดและ byte-pin ได้ว่ามันนับเอง แต่ไม่ยืนยันว่าคือ widget เดียวกับที่ GT-029 เห็นเป๊ะ · คำตัดสิน (ข) **ไม่ขึ้นกับ** การระบุ widget เพราะพิสูจน์ระดับ field แล้วว่าไม่มีทางอ่าน `attr+0x58` สด
2. **negative "ไม่มี writer ลด `attr+0x58`" อิงสำมะโน 437 store + RMW detector (float+int)** — RMW detector เป็น heuristic (สแกนหน้าต่าง +-0x40-0x60 รอบ store) · จุดที่แข็งเป็น [PROVEN] คือ: ผู้อ่านทุกเฟรม 3 ตัวอ่านอย่างเดียว, ผู้เขียน BasicAttr 4 ตัวไม่ลด, RMW candidate ทั้ง 10 (3 float + 7 int) ไม่ใช่ BasicAttr · ไม่อ้างเชิงสัมบูรณ์ว่า "ทุก byte ในอิมเมจไม่มีที่ไหนลด" นอกเหนือจากสิ่งที่สแกน
3. **ตรรกะปิดคดี section 0 ข้อ 3 ใช้ข้อเท็จจริง runtime จาก GT-029** ("เซิร์ฟเวอร์ไม่ส่งเฟรมต่อ" + "เห็นเลขลด") — ส่วน static ([PROVEN]) คือ "ไม่มี decrementer + ไม่มี display reader" · การรวมสองอย่างเป็นข้อสรุปเชิงตรรกะ ไม่ใช่ single byte-span
4. **ไม่ได้ยืนยันว่า NPC (CNetNPC) ใช้ predicate/getattr เส้นเดียวกับ CMyActor เป๊ะทุก vtable** — จาก rdata: `vt+0x3C`=`0x454A70` และ `vt+0x40`=`0x454AC0` ปรากฏใน vtable 3 ตัว (`0xF0D7E4/0xF0DD44/0xF0E6AC` และ `0xF0D7E8/0xF0DD48/0xF0E6B0`) => หลายคลาส actor **ใช้ impl predicate ตัวเดียวกัน** (รวม path NPC) แต่ไม่ได้ไล่ทุก vtable ของทุกคลาส
5. **ไม่ได้ถอด `$pcz` / ไม่ได้อ่าน TipID/TextID จริง** · ไม่แตะ server-side · ไม่มี runtime pass ในรอบนี้
6. **ไม่อ้างอะไรเกี่ยวกับ ORIGINAL server** (ปิดไปแล้ว ไม่เคย publish)

---

## 7. วิธีทำซ้ำ (span ที่ตรึงไว้)

ทุกตัวเลข/คำอ้างได้จาก `capstone 5.0.7` + byte-scan บนอิมเมจ read-only (SHA ข้างบน) · สคริปต์ scratch อยู่ใน `/tmp/pfdying/` (print เฉพาะ ASCII): `pf.py` (PE plumbing + call index), `census58.py` (สำมะโน store/read `[reg+0x58]`), `reads58.py` (จำแนก reader + display-path), `rmw58.py`/`intrmw.py` (RMW-decrement detector), `classify58.py` (จับ getattr/const marker)

| VA | off | len | bytes | claim |
| --- | --- | --- | --- | --- |
| `0x454A7A` | `0x53E7A` | 9 | `0f57c00f2f4058722e` | predicate ตายอ่าน `+0x58` แล้ว `jb` (เทียบเฉย ๆ) |
| `0x454ACA` | `0x53ECA` | 14 | `f30f1040580f2f059c98f000762e` | IsDying อ่าน `+0x58` แล้ว `jbe` |
| `0x44A56D` | `0x4996D` | 24 | `f30f104058f20f2a0d9c240201f20f5c0dd092f0000f5ac0` | Main_Dead gate อ่าน `+0x58` เทียบ 19.5 |
| `0x464B0E` | `0x63F0E` | 5 | `f30f114658` | ctor `[obj+0x58]=0.0f` |
| `0x4656A3` | `0x64AA3` | 10 | `84c07806d94658d95f58` | `Merge` copy-forward `+0x58` (ไม่ลด) |
| `0x4658E8` | `0x64CE8` | 14 | `f60380740f6a048d4658506a2a8b...` | wire-load `+0x58` เมื่อบิต `0x80` ติด |
| `0xABBA34` | `0x6BAE34` | 40 | `8b81480300 00...895058...889095000000` | non-attr int-grid writer `+0x58/+0x5c` + flag `+0x95` |
| `0x44D693` | `0x4CA93` | 26 | `8b442438f30f7e00...894e5889565c` | outbound-vital target `+0x50..+0x5c` |
| `0x455D96` | `0x55196` | 25 | `f30f114854...f30f11405cf30f114858` | render-node Vec3 `+0x54/+0x58/+0x5c` |
| `0x6E1D99` | `0x2E1199` | 33 | `f30f10442414...f30f11405c` | render-node Vec3 `+0x54/+0x58/+0x5c` |
| `0x483475` | `0x82875` | 12 | `689c24020168fc18f10056e8` | `register_cfg(L"DURATION_DYING",&0x102249C)` (push address) |
| `0x4839E8` | `0x82DE8` | 12 | `68e025020168c40cf10056e8` | `register_cfg(L"EXTREMIS_TIME",&0x10225E0)` (=30.0f) |
| `0x6287EF` | `0x227BEF` | 10 | `6810fdf1008bce894658` | revive-notify ctor: `[handler+0x58]` = child window ptr |
| `0x628BE1` | `0x227FE1` | 15 | `f30f1005e02502010f5ac9660f2fd1` | revive-notify อ่าน `EXTREMIS_TIME`(30.0) |
| `0x628C54` | `0x228054` | 9 | `8b4e5850e8d397e4ff` | revive-notify `SetValue` บน child `[handler+0x58]` |

ค่าคงที่: `DURATION_DYING`@`0x102249C`=`20` (int) · `EXTREMIS_TIME`@`0x10225E0`=`30.0f` · const0@`0xF0989C`=`0.0f` · `[0xF0F398]`=`5.0`(dbl) · `[0xF0AF90]`=`100.0`(dbl)

ไฟล์ layout (อ่านตรง ๆ): `Data/GUI/Model/Main_Revive_Notify.model` · `Main_Revive_Action.model` · `Party_Main.model` (`PANEL_REVIVE_NOTIFY`) · `Main_Dead.model`
