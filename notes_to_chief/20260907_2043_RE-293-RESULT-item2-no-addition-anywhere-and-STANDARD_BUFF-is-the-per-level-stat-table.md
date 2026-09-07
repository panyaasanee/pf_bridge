# RE-293 RESULT (ข้อ 2) — ไคลเอนต์ **ไม่บวกอะไรเลย** บนเส้นทาง `ActorAttr+0x82` · และตารางสแตทต่อเลเวลที่หายไปคือ **`STANDARD_BUFF`** ไม่ใช่ `POTENTIAL`

- ใบ: `RE-293 PLAYER-STR-DERIVATION-SOURCE-001` — **ข้อ 2 (ผู้เรียก / มีการบวก `n_POINT_ABILITY` ไหม)**
- ผู้ทำ: RE runner บนเครื่องสะพาน · รอบ `RE-RUNNER-20260907_2033`
- ticket START: 2026-09-07T20:36+07:00 · ส่งผล 2026-09-07T20:43+07:00
- เจ้าของใบ/ผู้บริโภคผล: **LANE-CS (CLASS/SKILL)**
- ต่อจากจดหมาย `20260907_1330_RE-293-RESULT-potential-is-keyed-by-n_ID-and-s_SCORE-is-never-read.md` ซึ่งระบุเองว่า checkpoint = **time checkpoint ไม่ใช่ method ceiling** และให้เดินต่อจาก `0x005888D5`

## สถานะ: **PASS / DONE (ข้อ 2 ปิด)** — และ 🔴 **แก้ `BUILD_IMPACT 4` ของจดหมายรอบก่อน**

---

## 0. input (read-only · ก่อน = หลัง)

| ไฟล์ | ขนาด | sha256 |
|---|---|---|
| `GameClient\GameClient.local.bin` | 14,759,424 | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| `GameClient\Data\B_CONSTDATA_TH.pc_` | 426,944 | `496b5c7b5a7f4c1ab5e343937ca7278b3db5b4501250caa7da47f22dc2c9c3f8` |
| `pf_asset_viewer\tools\tables_TH.zip` | — | `66b7342a8f1581c8e411d0655bf2d7caa8e8acf78b3565827f6afb8952f34aa3` |
| `pf_bridge\gamedata\tables\CONSTDATA_TH__STANDARD_BUFF.tsv` | 257 บรรทัด (256 แถวข้อมูล) | `a2906ebf78918f90…` |
| `pf_bridge\gamedata\tables\CONSTDATA_TH__POTENTIAL.tsv` | 1 บรรทัด (หัวตารางล้วน) | `d798d5acefc62098…` |

`GameClient\` ไม่ถูกแตะ · ตรวจ sha256 ของอิมเมจซ้ำหลังจบงาน = ค่าเดิม

## 1. ค้นใน `pf_bridge\external\` แล้ว — เจออะไร/ไม่เจอ (พร้อมขอบเขต)

ขอบเขต: 2,683 ไฟล์ทั้งต้นไม้ `external/` (grep ข้อความ `STANDARD_BUFF`, `STR_CHECK`, `CON_CHECK`, `n_STRENGH`)

- **เจอ**: ชื่อ `STANDARD_BUFF` ปรากฏใน `external/.pf_attr_generator_snapshots/*/pf_rederive_attr_semantics.py` (สแนปช็อตของตัว generator) ในรูป literal `"STANDARD_BUFF_DATA"`, `"STANDARD_BUFF_column_census"`, `"decompressed_table=STANDARD_BUFF"` ⇒ **ตัว generator รู้จักตารางนี้มานานแล้ว**
- **ไม่เจอ**: โทเคน `STR_CHECK` / `CON_CHECK` / `INT_CHECK` / `PER_CHECK` / `AGI_CHECK` **ไม่ปรากฏที่ใดเลยใน `external/`** ⇒ ไม่มีใครเคยถอดความหมายของ `s_BUFF_CONDITON` มาก่อน

## 2. ค้น `gamedata` แล้ว — เจออะไร/ไม่เจอ (พร้อมขอบเขต)

ขอบเขต: 1,109 ไฟล์ใต้ `pf_bridge\gamedata\`

- **เจอ**: `gamedata/00_SEARCH_HERE_FIRST.md:51` เขียนไว้ตรง ๆ ว่า `CONSTDATA_TH__STANDARD_BUFF.tsv 256 แถว x 36 คอลัมน์` และไฟล์จริงอยู่ที่ **`gamedata/tables/CONSTDATA_TH__STANDARD_BUFF.tsv`** (คอมมิตแล้ว) — คอลัมน์ `n_STRENGH`, `n_CONSITUTION`, `n_AGILITY`, `n_PERCEPTION`, `n_INTELLECT` ครบ **พร้อมค่า**
- **เจอ**: `gamedata/PF_GAMEDATA_COLUMNS.tsv` แถว 207-… ให้ ordinal/offset ของทุกคอลัมน์ `STANDARD_BUFF` (`n_STRENGH` = ordinal 6, offset 24, type 0/int, width 4)
- **เจอ (ยืนยันผลลบเดิม)**: `gamedata/tables/CONSTDATA_TH__POTENTIAL.tsv` = **หัวตารางล้วน 0 แถว** ตรงกับที่รอบก่อนวัดจากอิมเมจ
- **ไม่เจอ**: โทเคน `STR_CHECK` ฯลฯ ใน `gamedata/` เช่นกัน

---

## 3. คำตอบข้อ 2 — **ไม่มีการบวกใด ๆ ทั้งอิมเมจ**

### 3.1 `0x005888D5` **ไม่ใช่จุด `find(key)`** — เป็นตัวผูกตาราง (binder) ล้วน

ฟังก์ชันครอบคือ **`0x00588810`** (thiscall · `ecx→esi` · คืน `bool`) ทำแค่สองอย่าง:

1. สร้างเวกเตอร์ชื่อคอลัมน์ห้าตัวไว้ที่ **`this+0x58`** — push ผ่าน `0x00434690`:
   `n_STRENGH`(`0xF14B70`) · `n_CONSTITUTION`(`0xF14B50`) · `n_AGILITY`(`0xF14B3C`) · `n_INTELLECT`(`0xF14B24`) · `n_PERCEPTION`(`0xF14B08`)
2. ขอพอยน์เตอร์ตารางจาก registry singleton **`0x0108CDD0`** ผ่าน **`0x00890EF0`** สามครั้ง แล้วแคชไว้:
   `POTENTIAL`(`0xF14B94`) → **`this+0x4C`** · `BUFF`(`0xF0C270`) → `this+0x50` · `BUFF_TIP`(`0xF29EF8`) → `this+0x54`
   คืน `1` ก็ต่อเมื่อทั้งสามตัวไม่เป็น NULL (`0x00588907`–`0x0058892E`)

**ไม่มี lookup ด้วยคีย์ · ไม่มีเลขคณิต · ไม่เขียน `ActorAttr` เลย**

ผู้เรียก **มีตัวเดียวทั้งอิมเมจ** = `0x00588C8F` (ภายใน init ก้อนใหญ่ที่เช็ค `[esi+0x18]/[0x1C]/[0x20]/[0x24]/[0x28]` ก่อน แล้วเรียก `0x00588810` → `0x005889F0` → `0x00588750` → `0x00588210`)

### 3.2 xref ของ `n_STRENGH` ทั้งสี่ตัวที่รอบก่อนค้างไว้ — **จำแนกครบแล้ว**

| VA (push) | ฟังก์ชันครอบ | ชนิด |
|---|---|---|
| `0x00588842` | `0x00588810` | binder — เวกเตอร์ชื่อคอลัมน์ที่ `this+0x58` (ตาราง `POTENTIAL` ที่ `this+0x4C`) |
| `0x00585970` | `0x00585740` | binder — เวกเตอร์ชื่อคอลัมน์ที่ `this+0x210` (ตาราง `POTENTIAL` ที่ `this+0x204` ตามที่รอบก่อนพินไว้) |
| `0x00655FE2` | `0x00655A40` | **ผู้อ่านค่า** — วนแถว `BUFF` แล้วอ่านคอลัมน์ตามชื่อผ่าน `0x00891EE0` (คืน presence byte ที่ `[eax]` + ค่าที่ `[eax+4]`) เก็บลงกรอบสแตก ไม่แตะ `ActorAttr` |
| `0x005B344A` | `0x005B3270` | **ผู้อ่านค่า + คูณ** — ดูข้อ 3.4 |

⇒ ไม่มีตัวใดเลยที่เอา `n_POINT_ABILITY` มาบวก และ `n_POINT_ABILITY` ยังคงมี xref เดียวในตัวโหลด (`0x004A4124`) ตามที่รอบก่อนวัดไว้ **ยืนยันซ้ำ ไม่เปลี่ยน**

### 3.3 สำมะโนผู้เขียน/ผู้อ่าน `+0x82` แบบ 16-bit ทั้ง `.text` — ทุกตัวเป็น "คัดลอก" หรือ "ศูนย์"

วิธี: สแกนไบต์แพตเทิร์น `disp32 = 82 00 00 00` ที่นำหน้าด้วย `66 89` / `66 8B` ทั้งเซกชัน `.text` (`va=0x00401000` `size=0x838C00`) → 36 hit → ดิสแอสเซมเบิลฟังก์ชันครอบของทุก hit
**ไม่ได้ใช้ linear disassembler เป็นหลักฐานผลลบ** — ผลลบมาจากการจำแนกฟังก์ชันครอบของ hit ทุกตัวทีละตัว

คลาส `ActorAttr` (crosswalk = บันไดฟิลด์เดียวกันเป๊ะ `+0x78,+0x7C` dword / `+0x80..+0x8A` u16 ห้าตัว / `+0x8C,+0x90,+0x94` dword / `+0x98..+0x9B` byte / `+0xA0..+0xAC` dword / `std::string` ที่ `+0xB0,+0xCC,+0xE8,+0x104,+0x120` · vtable ของ copy-ctor = `0xF0E7A0`):

| ฟังก์ชัน | บทบาท | ทำอะไรกับ `+0x82` |
|---|---|---|
| `0x00464BE0` | ctor | `xor ecx,ecx` → `mov word [esi+0x82], cx` = **ศูนย์** (พร้อม `+0x80/84/86/88/8A` เป็นศูนย์ทั้งชุด) |
| `0x00464F30` | `operator=` | คัดลอกฟิลด์ต่อฟิลด์จาก `[edi]` |
| `0x004659B0` | comparator/diff | `mov dx,[esi+0x82]; cmp dx,[edi+0x82]` — **อ่านอย่างเดียว** เพื่อสร้าง mask |
| `0x00465E60` | **masked apply** | `test al,0x20` แล้ว `mov dx,[edi+0x82]` → `mov [esi+0x82],dx` = **คัดลอกล้วน** (บิต `0x20` = `1<<5` ตรงกับ mask ของ STR ที่ใบระบุ) |
| `0x004B23D0` | full copy | คัดลอกล้วน |
| `0x005ACA40` | copy-ctor (เขียน vtable `0xF0E7A0`) | คัดลอกล้วน |

ตัดออกด้วย crosswalk (ไม่ใช่ `ActorAttr` — **ไม่ได้ตัดเพราะออฟเซ็ตเท่ากัน แต่เพราะ layout/vtable ต่าง**):

- `0x0064E8B0` — `inc word [edi+0x82]` แล้ว compare: ตัวนับของอ็อบเจ็กต์อื่น ไม่มีบันไดฟิลด์ `ActorAttr`
- `0x007FF650` / `0x007FF87B` / `0x007FFEA6` — อ็อบเจ็กต์ที่เขียน vtable **`0xF4E648`** และมีฟิลด์ `+0x34/+0x44/+0x48/+0x4C/+0x50/+0x54/+0x58` คนละคลาส

🔴 **สรุปข้อ 2: ในไคลเอนต์บิลด์นี้ ไม่มีจุดใดเลยที่ "คำนวณ" STR** — ทุกการเขียน `ActorAttr+0x82` คือ zero-init, คัดลอกเต็ม, หรือคัดลอกตามบิต mask จาก `ActorAttr` อีกตัว **ไม่มี add / imul / งบแต้ม / เทอมเลเวล**
⇒ **STR ที่เห็นบนจอ = u16 ที่เซิร์ฟเวอร์ส่งมาบนสาย ตรง ๆ** · ที่มาของตัวเลขเป็นเรื่องฝั่งเซิร์ฟเวอร์ทั้งหมด

### 3.4 ที่เดียวในอิมเมจที่ทำเลขคณิตกับคอลัมน์สแตท — และมันชี้ไปที่ตาราง **`STANDARD_BUFF`**

ฟังก์ชัน **`0x005B3270`** (ตัวประเมินเงื่อนไขบัฟ):

- ผูกสองตารางแบบ lazy-once: `BUFF`(`0xF0C270`) → `0x01080EB8` · **`STANDARD_BUFF`**(`0xF2C5F0`) → `0x01080EB4`
- อ่านคอลัมน์ **`s_BUFF_CONDITON`**(`0xF2C5D0`) ของแถว `BUFF` ผ่าน `0x00892500` แล้วแยกด้วย `;`(`0xF0C9AC`) และตัวคั่น `0xF2C53C`
- แต่ละรายการ: token[0] = ชื่อเงื่อนไข (string) · token[1] = ทศนิยม (แปลงด้วย `[0xC3B4F0]` = atof)
- เทียบ token[0] ด้วย strcmp (`[0xC3B51C]`) กับโทเคนห้าตัว แล้วอ่านคอลัมน์คู่ของมันจาก **`STANDARD_BUFF`** ผ่าน `0x00892480` → `cvtsi2ss` (int→float) → **`mulsd` กับทศนิยมจากเงื่อนไข**:

| โทเคนใน `s_BUFF_CONDITON` | VA เทียบ | คอลัมน์ที่อ่านจาก `STANDARD_BUFF` |
|---|---|---|
| `STR_CHECK` (`0xF2C5BC`) | `0x005B342A` | `n_STRENGH` (`0xF14B70`) — `push` ที่ `0x005B344A` |
| `CON_CHECK` (`0xF2C5A8`) | `0x005B34AA` | `n_CONSITUTION` (`0xF2C58C`) — `push` ที่ `0x005B34CA` |
| `AGI_CHECK` (`0xF2C578`) | — | `n_AGILITY` (`0xF14B3C`) |
| `PER_CHECK` (`0xF2C564`) | — | `n_PERCEPTION` (`0xF14B08`) |
| `INT_CHECK` (`0xF2C550`) | — | `n_INTELLECT` (`0xF14B24`) |

🔴 **หมายเหตุการสะกด (สำคัญตอนเขียนโค้ดเซิร์ฟเวอร์)**: `POTENTIAL` สะกด `n_CONSTITUTION` แต่ `STANDARD_BUFF`/`STANDARD_MOB` สะกด **`n_CONSITUTION`** (ตก `T`) — คนละสตริง คนละ VA จริง ๆ ไม่ใช่ typo ของจดหมายฉบับนี้

---

## 4. 🔴 แก้ `BUILD_IMPACT 4` ของจดหมาย `1330` — ตารางสแตทต่อเลเวล **มีอยู่ในของที่เรามีแล้ว**

จดหมายรอบก่อนสรุปว่า *"ค่าฐาน STR ต่อคลาส/เลเวลไม่มีอยู่ในของที่เรามีเลย"* ข้อสรุปนั้น **กว้างเกินหลักฐาน** — มันวัดแค่ `POTENTIAL` ตารางเดียว

วัดรอบนี้จากของที่คอมมิตแล้ว (`gamedata/tables/`) และจากดัมป์ `constdata_TH.json`:

| ตาราง | แถว | คอลัมน์สแตท | ตัวอย่างค่า (`n_ID` = 1 / 2 / 4 / 255) |
|---|---|---|---|
| `POTENTIAL` | **0** | `n_STRENGH` … (สะกด `n_CONSTITUTION`) | — (ว่างจริง · มี `s_HK_VER/s_TC_VER/s_JP_VER/s_TH_VER` ⇒ เป็นตารางที่เปิดตามภูมิภาค) |
| **`STANDARD_BUFF`** | **256** | `n_HPMAX`, `n_RECOVER_HP`, `n_STAMINAMAX`, `n_RECOVER_STAMINA`, `n_SPEED_RUN`, **`n_STRENGH`**, `n_CONSITUTION`, `n_AGILITY`, `n_PERCEPTION`, `n_INTELLECT`, `n_DAMMIN_*`, `n_DAMPLUS_*`, `n_AC_*` … (36 คอลัมน์) | STR = 5 / 5 / 6 / **3624** · HP = 337 / 351 / 403 / 239,184 · (+ แถวเซนติเนล `n_ID=9999` ค่า 1 ทั้งแถว) |
| `STANDARD_MOB` | 255 | ชุดคอลัมน์ **เหมือนกันทุกตัว** | STR = 5 / 6 / 7 / 3384 · HP = 106 / 121 / 163 / 1,771,680 |
| `STANDARD_STATUS` | 255 | `n_POINT_ABILITY` | 0 / 1 / 1 / **41** |

**`STANDARD_BUFF` คือคู่แฝดฝั่งผู้เล่นของ `STANDARD_MOB`** — ชุดคอลัมน์เหมือนกันเป๊ะ 
บันได `n_ID` 1..255 เพิ่มขึ้นทางเดียวเหมือนกัน ต่างกันแค่สเกล (HP ผู้เล่นเริ่มสูงกว่า 337 vs 106 แต่ปลายทางต่ำกว่า)

⇒ **ครึ่ง STR ที่ใบบอกว่า "แก้ไม่ได้จนกว่าใบนี้ตอบ" ปลดบล็อกได้แล้ว** สาย CS มีตารางสแตทต่อเลเวลของผู้เล่นครบ 255 เลเวลอยู่ในรีโป (`gamedata/tables/CONSTDATA_TH__STANDARD_BUFF.tsv`) ไม่ต้องรอไฟล์ข้อมูลจากที่อื่น และไม่ต้องเป็นคำถามออกแบบอีกต่อไป

---

## BUILD_IMPACT

1. **ห้ามใส่ตรรกะคำนวณ STR ฝั่งไคลเอนต์ในโมเดลของเรา** — ไคลเอนต์เป็นผู้แสดงผลล้วน เซิร์ฟเวอร์ต้องส่ง STR สำเร็จรูปมาที่ `ActorAttr+0x82` (u16 · tag `0x12` · mask `1<<5`) การบวกงบแต้มทั้งหมดเป็นหน้าที่เซิร์ฟเวอร์
2. **`STANDARD_BUFF` = ตารางฐานต่อเลเวลของผู้เล่น** ใช้แทน `MOB_COMBAT_DEFAULT_ATTACKER` ที่เป็นค่าคงที่ตัวเดียวได้ · โครงเดียวกับที่โปรเจกต์ใช้ `STANDARD_MOB` อยู่แล้ว ⇒ นำโค้ดเดิมมาใช้ซ้ำได้
3. **`POTENTIAL` ปิดถาวรในฐานะแหล่งสแตท** — 0 แถวทั้งในอิมเมจ (`0x004A439A: test ecx,0xFFFFFFFC / jle` ข้ามลูป) และในไฟล์ที่ ship มา · มี `s_*_VER` สี่คอลัมน์ ⇒ เป็นฟีเจอร์ที่ปิดในเวอร์ชัน TH
4. **`s_BUFF_CONDITON` ถอดได้แล้ว** — ไวยากรณ์ `<TOKEN>,<float>` คั่นด้วย `;` โดย `STR_CHECK/CON_CHECK/AGI_CHECK/PER_CHECK/INT_CHECK` อ้าง `STANDARD_BUFF` แถวหนึ่งแล้วคูณด้วย float · เป็นของใหม่ทั้งก้อน (`external/` และ `gamedata/` ไม่มีโทเคนเหล่านี้เลย) — ถ้าจะทำระบบบัฟให้ครบ ควรออกใบต่อเพื่อถอดว่า "แถวไหนของ `STANDARD_BUFF`" ถูกเลือก
5. **ระวังการสะกด** `n_CONSITUTION` (STANDARD_BUFF/STANDARD_MOB) vs `n_CONSTITUTION` (POTENTIAL)

## nonclaims (ห้ามตัดออก)

1. **ไม่อ้างว่า `STANDARD_BUFF.n_ID` = เลเวลตัวละคร** — วัดได้แค่ว่ามี 255 แถวเรียง 1..255 เพิ่มทางเดียว + แถวเซนติเนล `9999` และชุดคอลัมน์เหมือน `STANDARD_MOB` ทุกตัว · **ยังไม่มี crosswalk field ที่พิสูจน์ว่าเป็นเลเวล** ห้ามจับคู่เพราะเลขช่วงเท่ากัน
2. **ไม่อ้างว่าไคลเอนต์เอา `STANDARD_BUFF` ไปเขียนลง `ActorAttr+0x82`** — การใช้งานที่วัดได้จริงมีทางเดียวคือการคูณในเงื่อนไขบัฟที่ `0x005B3270` ตามข้อ 3.4
3. **ไม่อ้างว่า `STANDARD_BUFF` เป็นสแตทต่ออาชีพ** — ตารางนี้มีบันไดเดียว ไม่มีคอลัมน์อาชีพ ⇒ ค่าฐาน **ต่อคลาส** ยังไม่มีแหล่ง (ยังเปิดอยู่ แต่ไม่ใช่คำถามของใบนี้)
4. **ไม่อ้างว่า STR มีผลต่อดาเมจในบิลด์นี้** (ตาม nonclaim เดิมของเจ้าของใบ)
5. **ผลลบทั้งหมดจำกัดที่**: อิมเมจ `GameClient.local.bin` ไฟล์เดียว (เซกชัน `.text` ทั้งเซกชันสำหรับสำมะโน `+0x82`), ต้นไม้ `pf_bridge\external\` 2,683 ไฟล์, ต้นไม้ `pf_bridge\gamedata\` 1,109 ไฟล์ · **ไม่ได้ค้นไฟล์ข้อมูลไคลเอนต์ตัวอื่นนอก `B_CONSTDATA_TH.pc_`**
6. **ไม่ได้ใช้ linear disassembler เป็นหลักฐานผลลบ** — สำมะโน `+0x82` ทำด้วยการค้นแพตเทิร์นไบต์ของ `disp32` แล้วดิสแอสเซมเบิล **ฟังก์ชันครอบของทุก hit** ทีละตัวเพื่อจำแนก
7. **ไม่ได้แก้ไฟล์ใด ๆ ใน `GameClient\` · `SERVER\` · `external\` · `gamedata\` · คิวใด ๆ** · ไม่ได้บูตเกม ไม่ได้จับ `LOCK_GAME`
8. **หลักฐาน static ล้วน** ไม่มีชั้น client-observable และไม่มีชั้น wire/DB ในจดหมายฉบับนี้

## ทำซ้ำได้

สคริปต์ read-only วางไว้ที่ `pf_bridge\staged\` (ต้องมีคนบนเครื่องสะพาน `git add` — `pf_git_sync.ps1` ไม่พาไฟล์ใหม่ใต้ `staged/` ขึ้นเอง)

| สคริปต์ | sha256 |
|---|---|
| `staged/re293_item2_disasm_probe.py` | `01c642b70eb3fb8930cf2c475c04f51a5bac076de967fb5eaa44e707d89bd203` |
| `staged/re293_item2_xref.py` | `15f3aabe0b4842bba0a8fdef9de4bfd93f7cee4e1a52cd7c2048a8813fa5e2ab` |
| `staged/re293_item2_attr82_writers.py` | `aeb252b3d797f2282372de5a5cb4d0e0d9a8dc65f5d3af7d6242cb73e49715ed` |
| `staged/re293_item2_strings.py` | `87b0fe2da64f1131986c6cc02542ac5055fb0d964c869b09ec31a789d7203afa` |

```
python3 staged/re293_item2_disasm_probe.py <GameClient>/GameClient.local.bin 0x00588810:0x00588960:BINDER
python3 staged/re293_item2_xref.py         <GameClient>/GameClient.local.bin 0x00588810
python3 staged/re293_item2_attr82_writers.py <GameClient>/GameClient.local.bin
python3 staged/re293_item2_strings.py      <GameClient>/GameClient.local.bin 0xF2C5BC 0xF2C5F0 0xF14B70
```

ต้องมี `capstone` + `pefile` · ตัวโหลด PE ใช้ `ImageBase=0x00400000` และ map VA→file offset ตามตาราง section (`.text` va=`0x00401000` raw=`0x400` size=`0x838C00`)

## หมายเหตุเรื่องป้ายใบ

ใบนี้มีป้ายเส้นทาง `[STATIC-ON-BRIDGE]` ครบ · หัวใบตอนหยิบเขียนว่า `PARTIAL` และจดหมายผลเดิมระบุเองว่าเป็น **time checkpoint ไม่ใช่ method ceiling** พร้อม VA ให้เดินต่อ ⇒ หยิบมาทำต่อตามกติกา ไม่ใช่การรัน PARTIAL ซ้ำหลังชนเพดานวิธี

## ผลไปถึงใคร

**LANE-CS (CLASS/SKILL)** = เจ้าของใบ/ผู้บริโภคผล · ขอให้ LANE-K พับหัวใบตามคำในบรรทัด "สถานะ" ข้างบน
