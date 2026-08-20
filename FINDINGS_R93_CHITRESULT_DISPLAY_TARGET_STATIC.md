# FINDINGS-R93 — CHitResult: เลขความเสียหายไปเกาะกับใคร (static, byte-exact)

**ไบนารี (อ่านอย่างเดียว)** `GameClient/GameClient.local.bin` SHA-256 `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623` · ImageBase `0x400000` · `.text` VA `0x401000` · 14,759,424 ไบต์
**เครื่องมือ** capstone 5.0.7 (ลงในแซนด์บ็อกซ์สำเร็จ) + PE plumbing แบบเดียวกับ `tools/pf_damage_hit_result_static.py` · ทำงานใน `/tmp/` ทั้งหมด ไม่แตะรีโป
**ตรวจก่อนเชื่อเครื่องมือตัวเอง** `python3 tools/pf_damage_hit_result_static.py` -> **`GUARDS 235/235 PASS` exit 0**
**สั่งโดย** chief รอบ 93 · **เหตุ** ผลเทส GT-024 คืน 2026-08-19/20: เลขความเสียหายขึ้น "บนตัวผู้เล่น ไม่ใช่บน NPC"

## 0. TL;DR — คำตอบ

> **ไม่ใช่ทั้ง (ก) และไม่ใช่ทั้ง (ข) เพราะสมมติฐานตั้งต้นผิด — เฟรมนั้นไม่เคยยิงใส่ NPC**
> `target.probe_identity_lo = 268500993` **ไม่ใช่ `0x10002001`** · `268500993 = 0x10010001` (ส่วน `0x10002001 = 268443649`)
> `0x10010001` คือ identity ของ **ตัวละครผู้เล่นเอง** ที่โปรเจกต์ปักไว้เป็น probe identity
> และแยกอีกชั้น: **(ก) ถูกหักล้างด้วยไบต์โดยตรง** — ท่อแสดงผล resolve target identity จริงที่ `0x750D1E`,
> resolve ไม่ได้ = ข้าม entry ทิ้ง, และ FxNumber ทั้ง 9 จุดผูกกับ actor ที่ resolve ได้

⇒ **client ทำถูกทุกขั้น และ encoder ของเราก็ทำถูก** — สิ่งที่ผิดคือ *เกณฑ์ในคิว* ที่เขียนว่า "เลขต้องขึ้นเหนือ NPC"

## 1. หลักฐานเลขคณิต + ที่มาในรีโป

```
hex(268500993) = '0x10010001'      0x10002001 = 268443649
```

| ไฟล์ | บรรทัด | เนื้อหา |
|---|---|---|
| `scenarios/damage_model_hypothesis_hit_sweep.json` | 138-144 | `"rule": "the_players_own_actor_is_both_performer_and_target"` · `"probe_identity_lo": 268500993` · `"probe_identity_hi": 0` |
| `src/pirateforce_foundation/damage_model_hypothesis.py` | 581-582 | `DAMAGE_PROBE_IDENTITY_LO = 0x10010001` |
| `src/.../damage_model_hypothesis.py` | 745-754 | ค่าเดียวกันถูกใช้ **ทั้ง** เป็น `target_identity` ของ entry **และ** `performer_identity` ของ header |
| `tests/test_damage_model_hypothesis.py` | 322 | `assertEqual(dmh.DAMAGE_PROBE_IDENTITY_LO, 0x10010001)` |
| `tools/verify_damage_model_encoder.py` | 789-792 | guard "the probe identity is the pinned smoke identity 0x10010001/0" |

`0x10010001` = ผู้เล่น — ยืนยันจาก `docs/EXPERIMENT_LEDGER.md` (CHARACTER-NAME-002: StartGame raw wire carries actor identity `0x10010001`), FND-006/009/010 (`identity 0x10010001:0`)
NPC เป็นคนละแบบ: `current/pf_login_game_server_v141.py:1459` `aid = 0x2000 + placement_idx + 1` -> NPC ตัวแรก = `0x2001` (hi=0) · `V129_QUEST_ACTOR_ID = 0x2001` (บรรทัด 821)

## 2. เส้นทางจากไบต์ hit-entry ถึงตัวเลขบนจอ

### 2.1 number pass ใน handler `0x750770` — resolve จริง

| VA | off | bytes | ความหมาย |
|---|---|---|---|
| `0x00750D12` | `0x350112` | `8B4E04` | `mov ecx,[esi+4]` = entry **+0x04** |
| `0x00750D15` | `0x350115` | `8B16` | `mov edx,[esi]` = entry **+0x00** |
| `0x00750D17` | `0x350117` | `5152` | push hi / push lo |
| `0x00750D19` | `0x350119` | `B9C0C60201` | `mov ecx,0x102C6C0` = actor manager singleton |
| `0x00750D1E` | `0x35011E` | `E84D54CFFF` | **`call 0x446170`** = ค้น actor จาก identity 64-bit |
| `0x00750D23` | `0x350123` | `8BF8` | `mov edi,eax` |
| `0x00750D27` | `0x350127` | `0F8482000000` | **หาไม่เจอ -> ข้าม entry ทั้งอัน (ไม่มีเลข)** |
| `0x00750DA8` | `0x3501A8` | `8BCF` | **`mov ecx,edi`** = `this` คือ actor ที่ resolve ได้ |
| `0x00750DAA` | `0x3501AA` | `E831F0CEFF` | `call 0x43FDE0` |

reaction pass ใช้ตัวเดียวกัน: `0x7508A4 E8C758CFFF` / `0x7508AD 0F84A4030000`
args ที่ส่งเข้า `0x43FDE0`: `0x750D90 8B4E08` (damage, arg6) · `0x750D93 0FB7561C` (flags, arg5) · `0x750D97 8B4604` (target hi) · `0x750D9B 8B0E` (target lo) · `[ebp+0x1C]/[ebp+0x18]` (performer hi/lo)

### 2.2 `0x446170` = map lookup จริง ไม่ใช่การหยิบ local player

| VA | off | bytes | disasm |
|---|---|---|---|
| `0x00446170` | `0x045570` | `8B442404` | `mov eax,[esp+4]` (lo) |
| `0x00446177` | `0x045577` | `0B442410` | `or eax,[esp+0x10]` (hi) |
| `0x0044617D` | `0x04557D` | `83C408C20800` | **identity == 0 -> คืน NULL ทันที** |
| `0x00446186` | `0x045586` | `8D710C` | `lea esi,[ecx+0x0C]` = ตารางที่ `mgr+0x0C` |
| `0x00446196` | `0x045596` | `E8E5D60400` | `call 0x493880` = `equal_range(&out,&key64)` |
| `0x004461C9` | `0x0455C9` | `8B4618` | ค่าที่ผูกกับคีย์ (actor*) |
| `0x004461DD` | `0x0455DD` | `33C0` | ไม่พบ -> NULL |

**ไม่มี `[0x1032EC4]` (local player) ใน `0x446170` เลยแม้แต่ครั้งเดียว** · manager `0x102C6C0` เป็นตัวเดียวกับที่ `0x402A20` คืน และที่ `0x43FDE0` ใช้ — ตารางเดียว คีย์เดียว ท่อเดียวกับ actor-entry

### 2.3 ใน `0x43FDE0` — `this` เก็บเป็น `ebp` และ FxNumber ทั้ง 9 จุดใช้ `ebp`

`0x43FE12 A1C42E0301` (local player, ใช้เป็น gate) · **`0x43FE17 8BE9` `mov ebp,ecx`** · `0x43FE19 896C2414`
call site ของ `0x43FBB0` ใน `0x43FDE0` = **9 จุดพอดี** ทุกจุด `ecx=ebp`:
`0x43FF2A`(type 7) · `0x43FFC3`(4) · `0x43FFFE`(5) · `0x440041`(0/1) · `0x440058`(8) · `0x44006F`(9) · `0x440097`(6) · `0x4400DE`(2) · `0x440126`(3)

### 2.4 `0x43FBB0` — ตำแหน่งเลขมาจาก `this` ตรง ๆ

`0x43FBD5 8BF9` (`edi=this`) · `0x43FBD7 E804C1FFFF` `call 0x43BCE0` (ดึงตำแหน่งโลกของ actor นั้น) · `0x43FBDC F30F7E00` (pos.xy) · **`0x43FBED F30F104718`** `movss xmm0,[edi+0x18]` = ความสูงเหนือหัวของ actor ตัวนั้น · `0x43FC02 F20F58C1`

### 2.5 FxNumber ctor `0xA7C010`

`0xA7C046 8986F8000000` value -> `+0xF8` · **`0xA7C0C5 898E0C010000` type -> `+0x10C`** · `0xA7C0CB/0xA7C0D3` pos -> `+0x100/+0x108`

## 3. คำตัดสิน (ก) / (ข)

**(ก) หักล้างแล้ว** สามชั้น: (1) มี resolve จริง `0x750D1E` (2) resolve ไม่ได้ = เงียบสนิท `0x750D27` (3) จุดเกิดของ FxNumber ผูกกับ actor ที่ resolve ได้ 9/9
`[0x1032EC4]` ถูกอ่านใน `0x43FDE0` สามครั้ง (`0x43FE12`, `0x43FE69`, `0x43FEF6`) และ **ทุกครั้งเป็นเงื่อนไข ไม่ใช่จุดเกาะ**
**(ข) จริงแต่ trivial** — `0x10010001` *คือ* identity ผู้เล่น ไม่มีการ "แปลง" ใด ๆ ใน `0x446170`

**cross-check สีเลข:** `0x43FEFB 8B4878` / `0x43FEFE 8B507C` / `0x43FF01 3BCE` / `0x43FF0B B301` / `0x43FF0F 32DB` -> `bl=1` เมื่อ performer == ผู้เล่น -> เลือก type `0` (`0x44003B 6A00`) แทน `1` (`0x44003F 6A01`) -> ชุดคีย์ `0..9` = `bm_r%d.tga` = **ตัวเลขสีแดง** ตรงกับที่ผู้เทสเห็น "379 สีแดง-ส้ม"

## 4. identity ที่ส่งมีผลอะไร + อะไรจะทำให้เลขไปโผล่บน NPC

`entry+0x00` มีผลสามอย่าง: (1) เป็นคีย์เลือก actor ที่เลขไปเกาะ (2) เป็น kill switch (`0x750D27`/`0x7508AD`/`0x44617D`) (3) มีส่วนใน visibility filter
**สิ่งที่จะทำให้เลขโผล่บน NPC:** ตั้ง `entry+0x00` = identity ที่ client ลงทะเบียนไว้แล้ว = `0x2000 + placement_idx + 1` (NPC ตัวแรก Port Royal = `0x2001`, hi=0) และ NPC ต้องถูกส่งเข้ามาแล้วผ่านท่อ actor-entry `0x6E9D`
**ควรคง `header+0x18` = `0x10010001`** เพราะ `0x43FE78 3BCE` / `0x43FE86 7473` — ถ้า performer เป็นผู้เล่นจะ **ข้าม filter 6 ชั้น** ทันที ถ้าไม่มีฝั่งไหนเป็นผู้เล่นเลย ต้องผ่านอย่างน้อย 1 ใน 6 (`0x7504A0` x2, `0x750590` x2, `0x7505D0` x2) ไม่งั้น `0x43FEF0 0F844D020000` = **ไม่วาดอะไรเลย**

## 5. `MISS` — ตอบได้ครบ

**มันคือเท็กซ์เจอร์ ไม่ใช่คำที่พิมพ์** — ลิเทอรัล ASCII `0xF85AA8` (off `0xB83EA8`) = `.\Data\CP\bmmsg\bm_miss.tga` อ้างถึงจุดเดียวทั้งอิมเมจที่ `0xA7D0B3`

**ตารางคีย์ (ลงทะเบียนใน `0xA7C880`, caller เดียว `0xA7F63D`):**

| คีย์ | ลิเทอรัล | push VA/off/bytes | ไบต์คีย์ VA/off/bytes |
|---|---|---|---|
| `0x2C` | `bm_block.tga` `0xF85AD0` | `0xA7CF2C`/`0x67C32C`/`68D05AF800` | `0xA7CFA1`/`0x67C3A1`/`C64424232C` |
| **`0x2D`** | **`bm_miss.tga` `0xF85AA8`** | **`0xA7D0B2`/`0x67C4B2`/`68A85AF800`** | **`0xA7D10F`/`0x67C50F`/`C64424232D`** |
| `0x2E` | `bm_boom.tga` | `0xA7D1D2`/`0x67C5D2` | `0xA7D233`/`0x67C633`/`C64424232E` |
| `0x2F` | `bm_gored.tga` | `0xA7D4F4`/`0x67C8F4` | `0xA7D551`/`0x67C951`/`C64424232F` |
| `0x30` | `bm_overkill.tga` | `0xA7D37D`/`0x67C77D` | `0xA7D3DA`/`0x67C7DA`/`C644242330` |
| `0x28/0x29/0x2A/0x2B` | `bm_gp/gm/bp/bm` | — | `0xA7E01E`/`0xA7E17F`/`0xA7E2F8`/`0xA7E490` |
| `0..9` | `bm_r%d` | `0xA7D610` | `0xA7D583 32DB` .. `0xA7D713 80FB09` |
| `20..29` | `bm_b%d` | `0xA7D7D3` | `0xA7D730 B314` .. `0xA7D920 80FB1D` |
| `10..19` | `bm_g%d` | `0xA7D9C3` | `0xA7D92D B30A` .. `0xA7DAF8 80FB13` |
| `30..39` | `bm_o%d` | `0xA7DB94` | `0xA7DB0B B31E` .. `0xA7DCC9 80FB27` |

**คีย์ `0x2D` ถูกเลือกด้วย FxNumber type = 6:**
`0xA7EEDA 8B860C010000` (อ่าน `[esi+0x10C]`) · `0xA7EF15 83F807` -> `0xA7EF22 6A2C` (type 7 = block) · **`0xA7F043 83F806`** -> **`0xA7F050 6A2D`** · `0xA7F0E4 83F809` -> `0xA7F0F1 6A30` (overkill) · `0xA7F435 83BE0C01000008` -> `0xA7F446 6A2F` (gored)
glyph builder `0xA7EBA0` วาด **เฉพาะ type 0..5**: `0xA7EBD4 8B870C010000` แล้ว `0xA7EBF5 0F8513020000` = ไม่ใช่ 0..5 -> ออกทันที (ไม่วาดเลข)

**อะไรสั่ง type 6 — ไม่ใช่ bit ไหนเลย เป็น default ของ (bit0 ไม่ติด AND damage == 0):**

| VA | off | bytes | disasm |
|---|---|---|---|
| `0x0043FF11` | `0x03F311` | `8BB42488000000` | `esi = damage` |
| `0x0043FF9F` | `0x03F39F` | `F684248400000001` | `test byte [esp+0x84],1` = bit0 |
| `0x0043FFA7` | `0x03F3A7` | `0F84E1000000` | **bit0 ไม่ติด -> `je 0x44008E`** |
| `0x0044008E` | `0x03F48E` | `85F6` | **`test esi,esi`** |
| `0x00440090` | `0x03F490` | `750F` | **damage != 0 -> ข้าม (ไม่มี MISS)** |
| `0x00440093` | `0x03F493` | `6A06` | **`push 6`** |
| `0x00440095` | `0x03F495` | `8BCD` | `ecx = ebp` (เกาะ actor เป้าหมาย ไม่ใช่ผู้เล่น) |
| `0x00440097` | `0x03F497` | `E814FBFFFF` | `call 0x43FBB0` |

เฟรม `MISS` ของ sweep = `damage 0, flags 0x0000` -> เข้าเงื่อนไขนี้เป๊ะ ⇒ **คำทำนาย "เฟรมนี้จะเงียบ" ผิด และไบต์อธิบายได้ครบ**

**ตาราง flag -> type (ชื่อมาจากลิเทอรัล TGA ไม่ใช่ label ในอิมเมจ):**
bit1 (`0x43FF1B`) -> 7 block · bit0+bit9 (`0x43FFAD`) -> 4/5 (ชุด `bm_o%d`) · bit0 ไม่มี bit9 -> 0/1 (ชุด `bm_r%d`) · bit8 (`0x440046`) -> 8 gored · bit10 (`0x44005D`) -> 9 overkill · **ไม่มี bit0 + damage==0 -> 6 miss** · bit5 (`0x4400A1`) -> 2 · bit6 (`0x4400F2`) -> 3

## 6. กับดักสองอันสำหรับรอบหน้า

**6.1 FX ตัวที่สองใน handler เดียวกัน เกาะกับผู้เล่นเสมอ** (`0x750E43`):
`0x750DE8 A1C42E0301` (local player) · `0x750DF4 8B7078` · `0x750DFC 754A` (ไม่ตรง performer -> ข้าม) · **`0x750E05 8B4524`** (header field 4) · **`0x750E0A 743C`** (`+0x24 == 0` -> ข้ามทั้งก้อน) · **`0x750E27 B920000000`** (flags ฮาร์ดโค้ด `0x20`) · **`0x750E3C 8B0DC42E0301`** (`this` = **ผู้เล่น**) · `0x750E43 E898EFCEFF`
**คืนนั้นเส้นทางนี้ไม่ทำงาน** เพราะ `HEADER_RESERVED_VALUE = 0` (`damage_model_hypothesis.py:181`) ทำให้ `+0x24 = 0` — แต่ถ้าวันไหนปัก `+0x24` เป็นค่าอื่น จะได้เลขเหนือผู้เล่นทันที และดูเหมือนบั๊กเป๊ะกับที่เข้าใจผิดคืนนี้

**6.2 `CFightMsgVital`** (ลิเทอรัล `0xF48AE8`, vtable `0xF489C8`, handler `0x750270`, thunk `0xC0C100`) แปะเลข type 2 บนผู้เล่นแบบไม่มีเงื่อนไข: `0x75039F 8B0DC42E0301` · `0x7503A9 8B4614` · `0x7503AD 6A02` · `0x7503AF E8FCF7CEFF` — เราไม่ได้ส่งคลาสนี้ แต่หน้าตาผลลัพธ์เหมือนกันเป๊ะ

**6.3 gate ที่ทำให้ "ไม่มีเลข" แบบเงียบ:** identity==0 (`0x44617D`) · resolve fail (`0x750D27`/`0x7508AD`) · ไม่มี local player (`0x43FE1F`) · `[localplayer+0x420]==0` (`0x43FE25`+`0x43FE2C`) · filter ตกหมด (`0x43FEF0`) · gate ของ header field 2 (`0x750D45 7568` -> `0x5CAE00`)

## 7. ข้อเสนอ (ไม่ใช่คำสั่ง)

1. แก้บันทึกผล GT-024: `268500993 = 0x10010001` — เกณฑ์ "เลขต้องขึ้นเหนือ NPC" ตั้งผิดตั้งแต่แรก เฟรมนั้นผ่านเกณฑ์ที่ถูกต้องแล้ว
2. เฟรม MISS **ไม่ใช่ผลลบ** — `bm_miss.tga` คือหลักฐานบวกว่าไคลเอนต์อ่าน `flags` และ `damage` ของเราจริง ควรอัปเดต docstring ที่เขียนว่า "MISS ... the control: NO number"
3. รอบหน้า: เพิ่ม step `entry+0x00 = 0x2001` โดยคง `header+0x18 = 0x10010001` (ข้าม filter 6 ชั้น) — เลขโผล่บน NPC = ปิดเรื่องถาวร
4. อย่าปัก `header+0x24` เป็นค่าอื่นโดยไม่ตั้งใจ

## 8. NONCLAIMS

- ทุกข้อเป็นข้อเท็จจริงของ **ไคลเอนต์ตัวเดียวที่ตรึงด้วยแฮช** ไม่ใช่หลักฐานจากเซิร์ฟเวอร์ต้นฉบับ (ปิดไปแล้ว ไม่เคย publish ห้ามอ้าง)
- **ไม่มี runtime observation** ในเอกสารนี้ ไม่เปิดเกม ไม่บูตเซิร์ฟเวอร์ ไม่แตะ DB · พยานของผู้เทสใช้เพียงเพื่อเลือกว่าจะไปดูไบต์ตรงไหน
- **ไม่ได้พิสูจน์ว่า `0x2001` อยู่ใน identity map ตอนรัน** — ข้อ 7.3 เป็น "การทดลองที่ควรทำ" ไม่ใช่ผลที่รู้แล้ว
- **ไม่ตั้งชื่อเชิงความหมายให้ flag bit ใด ๆ** — ตารางข้อ 5 ระบุเฉพาะ "bit ไหนเลือก type ไหน และ type นั้นดึงลิเทอรัลอะไร"; block/crit/overkill = **ชื่อไฟล์ TGA** ไม่ใช่ label ในอิมเมจ
- **ไม่ได้เปิดไฟล์ `Data/CP/bmmsg/*.tga`** — ไม่ได้พิสูจน์ว่าภาพวาดอะไร และ **ไม่ได้พิสูจน์ว่าตัวอักษรบนจอสะกดว่า `MISS`** (พิสูจน์ได้แค่ว่าเลือกเท็กซ์เจอร์ชื่อ `bm_miss.tga`); `bm_r%d` = red ก็ยังไม่พิสูจน์
- **`0x7504A0` ยังไม่ได้ไล่ครบ** — รู้แค่ว่ารับ identity 64-bit คืน bool
- **`[localplayer+0x420]`, `[localplayer+0x348]+0x140/+0x144`, `[actor+0x358]+0xB0/+0xB4` ยังไม่มีชื่อ**
- **`[0x10339B0]` ยังเป็น UNKNOWN ตอนรัน** (หนี้เดิมรอบ 90) · **ความหมายของ `damage >= 0` ยังไม่ปิด** (หนี้เดิมรอบ 83/90)
- **ไม่แตะรีโป** — อ่านอย่างเดียว ไม่มี git operation ไม่รัน pytest ทั้งชุด

## 9. คำถามที่ต้องใช้อิมเมจ/runtime ตอบต่อ

1. NPC identity อยู่ใน map `[0x102C6C0+0x0C]` จริงไหมตอนรัน และคีย์คือ qword `0x2001` ตรง ๆ หรือถูกแปลงก่อน (ต้องไล่ **ผู้เขียน** map — รอบนี้ไล่แต่ผู้อ่าน; เป็นงาน static ที่ทำต่อได้ทันที)
2. `0x7504A0` ทำอะไร (ถ้าเป็น party/guild filter จะกระทบดีไซน์ multiplayer โดยตรง)
3. `[localplayer+0x420]` คืออะไร (เป็น gate ที่ปิดเลขทั้งหมดได้)
4. `0x5CE010` ทำอะไร (หนี้เดิมรอบ 90)
5. ชุดสีตัวเลข — ต้องเปิด TGA หรือถ่ายจอ
