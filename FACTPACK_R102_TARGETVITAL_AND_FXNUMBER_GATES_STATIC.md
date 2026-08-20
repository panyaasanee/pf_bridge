# FACTPACK-R102 — TargetVital 0x1ADD + FxNumber draw-gates (static, byte-exact)

**ไบนารี (อ่านอย่างเดียว)** `GameClient/GameClient.local.bin`
SHA-256 `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623` (ตรวจแล้วตรง canonical)
ImageBase `0x400000` · `.text` VA `0x401000` off `0x400` (VA − off = `0x400C00`) · 14,759,424 ไบต์
**เครื่องมือ** capstone 5.0.7 + PE section parser (แบบเดียวกับ `tools/pf_damage_hit_result_static.py`) · ทำงานใน `/tmp/` ทั้งหมด ไม่แตะรีโป
**ตรวจก่อนเชื่อเครื่องมือตัวเอง** `/tmp/verify_r102.py` → `NAMEID(TargetVital)=0x1ADD OK` · `GUARDS 41/41 PASS`
**สั่งโดย** chief รอบ 102 · **เหตุ** GT-027 rerun: `npc_sweep` เลขขึ้นครบเมื่อ Panya ขับ (เกาะเหนือหัว NPC) แต่รอบผู้เทส (ไบต์บนสายเหมือนกันเป๊ะ) ไม่เห็นเลข · ความต่างเดียวในล็อกเซิร์ฟเวอร์ = มี inbound `TargetVital 0x1ADD` 2 ใบ
**ต่อยอดจาก** `FINDINGS_R93_CHITRESULT_DISPLAY_TARGET_STATIC.md`

---

## 0. TL;DR

1. **TargetVital 0x1ADD ถูกส่งเมื่อไร** — เป็นข้อความ "client แจ้งเป้าหมายที่เลือกอยู่" (target-selection报告). ตัวคลาสถูกสร้างจาก object-factory (`new 0xA8` → ctor `0x51DE80`) และทุกเมธอดของมัน **อ่าน** actor map `0x102C6C0` ผ่าน resolver `0x446170` ตัวเดียวกับ number pass — ไม่มีการ insert. ⇒ ใบแรก (self `0x10010001`) = รายงานเป้าเริ่มต้น/ตัวเอง · ใบหลัง (NPC `0x2001`, placement=P0, data_name='Navy Transfer') = รายงานตอนเลือก NPC. **[PROVEN]** ตัวตน/ทะเบียน/wire-id/factory · **[LIKELY]** ความหมาย self-vs-NPC · **[UNKNOWN]** จุด socket-send และปุ่ม UI ที่ทริกเป๊ะ (ดู §7)

2. **อะไรทำให้เซสชันผู้เทสไม่เห็นเลขทั้งที่ไบต์เข้าเหมือนกัน** — เกตชี้ขาดคือ **การ resolve ตัวตนเป้า `0x2001` ใน map `0x102C6C0`** ที่ `0x750D1E`; resolve ไม่ได้ → `0x750D27 je` ข้าม entry ทั้งอัน เงียบสนิท. เลขจะโผล่ก็ต่อเมื่อ `0x2001` ถูก **ลงทะเบียนไว้แล้ว** (มาจากท่อ actor-lifecycle ไม่ใช่จาก TargetVital). เกตรองที่ปิดเลขได้เงียบ ๆ อีก: **`[localplayer+0x420]==0`** (`0x43FE2C`) = toggle แสดงเลข (ปุ่มคำสั่ง `0x27`), และ localplayer==NULL (`0x43FE1F`). สำหรับ frame performer=player/target=NPC เกต visibility 6 ชั้นถูก **ข้าม** เพราะ performer==localplayer (`0x43FE86`). **[PROVEN]**

3. **สมมติฐานคู่** — (ก) "เลือกเป้าเป็นเงื่อนไขให้ FxNumber เรนเดอร์" = **หักล้าง**: เลขขึ้นเพราะ performer==localplayer (`0x43FE86`) + resolve เป้าสำเร็จ ไม่ใช่เพราะ selection; ใบเลขแรกมาก่อน TargetVital(NPC) ~45s. (ข) "ใบหลังเป็นผลของเฟรม HIT_REACTION เอง" = **หักล้าง**: subtree ของ handler CHitResult (`0x750770→0x43FDE0→0x43FBB0→0xA7C010→0xA7EBA0`) **ไม่อ้างค่าคงที่ของ TargetVital เลยแม้แต่ตัวเดียว** (vtable/ctor/getid/id-global). **[PROVEN]**

> **ราก common cause ของ correlation "เห็นเลข ⇔ มี TargetVital":** ทั้งสองอย่างต้องการให้ `0x2001` resolve ได้ในตารางเดียวกัน (`0x446170` @ `0x102C6C0`). TargetVital(NPC) จึงเป็น **พยาน** ว่า `0x2001` ลงทะเบียนแล้ว ไม่ใช่ **สาเหตุ** ที่ทำให้เลขขึ้น.

---

## 1. TargetVital 0x1ADD — ตัวตน / ทะเบียน / getid / factory  **[PROVEN]**

wire id = PF-NAMEID hash ของลิเทอรัล (สูตร registry `sum((i+1)*ord(c)) & 0xFFFF`):
`NAMEID('TargetVital') = 0x1ADD` (reproduce ได้, ตรง `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`).

| VA | off | bytes | ความหมาย |
|---|---|---|---|
| `0x00BEE940` | `0x7EDD40` | `680C0BF300` | `push 0xF30B0C` = ลิเทอรัล ASCII `"TargetVital"` (off `0xB2EF0C`) |
| `0x00BEE94C` | `0x7EDD4C` | `E8AFD3CAFF` | `call 0x89BD00` = คำนวณ PF-NAMEID |
| `0x00BEE951` | `0x7EDD51` | `66A398200801` | `mov [0x1082098],ax` = **เก็บ wire id ลง global** `[0x1082098]` |
| `0x0051DF10` | `0x11D310` | `66A198200801C3` | `mov ax,[0x1082098]; ret` = **GetWireId stub** (vtable slot +0xA4) |
| `0x0051DE96` | `0x11D296` | `C70628FEF100` | ctor เขียน `[esi]=0xF1FE28` = **vtable ของ TargetVital** |
| `0x005D8542` | `0x1D7942` | `68A8000000` | `push 0xA8` = ขนาด object (168 ไบต์) ที่ operator new |
| `0x005D8565` | `0x1D7965` | `E81659F4FF` | `call 0x51DE80` = **ctor · caller เดียวทั้งอิมเมจ** (จาก object-factory CreateByName ที่ `0x5D84C0`) |

RTTI type-descriptor `.?AVTargetVital@@` @ VA `0x101FE40` (off `0xC1D640`). Global `[0x1082098]` ถูก **อ่านที่เดียว** = getid stub `0x51DF10` และ **เขียนที่เดียว** = registration `0xBEE951`. ctor `0x51DE80` ถูกเรียกจาก factory จุดเดียว ⇒ ทุก instance ของ TargetVital เกิดผ่านท่อนี้.

**บทบาทของคลาส (ทำไมมันคือ "รายงานเป้า"):** เมธอดของ cluster `0x51DE60..0x520600` ถูกครอบงำด้วย `call 0x402A20` (GetActorMgr → `0x102C6C0`) + `call 0x446170` (resolve actor by 64-bit identity) — resolver **ตัวเดียวกันเป๊ะ** กับ number pass. cluster นี้ **ไม่มี** call ไป WriteField family (`0x89A600/0x89A640`) และ **ไม่มี** call ไป map-insert (`0x446990`). ⇒ TargetVital เป็น **ผู้บริโภค** (อ่าน) ตาราง actor ไม่ใช่ผู้ลงทะเบียน.

---

## 2. เส้นทางวาดเลข: เกตทุกตัวสำหรับ frame performer=player / target=NPC  **[PROVEN]**

เส้น: `0x750770` (number pass) → resolve เป้า → `0x43FDE0` (FX dispatcher) → `0x43FBB0` (FxNumber spawn) → `0xA7C010` (ctor) → `0xA7EBA0` (glyph).

### 2.1 เกตชี้ขาด — resolve เป้าใน caller (`0x750770`)

| VA | off | bytes | ความหมาย |
|---|---|---|---|
| `0x00750D12` | `0x35011E`* | `8B4E04` | `mov ecx,[esi+4]` = entry+0x04 target id hi |
| `0x00750D15` | `0x350115` | `8B16` | `mov edx,[esi]` = entry+0x00 target id lo (`= 0x2001` ใน npc_sweep) |
| `0x00750D19` | `0x350119` | `B9C0C60201` | `mov ecx,0x102C6C0` (actor mgr) |
| `0x00750D1E` | `0x35011E` | `E84D54CFFF` | **`call 0x446170`** resolve target identity |
| `0x00750D25` | `0x350125` | `85FF` | `test edi,edi` |
| `0x00750D27` | `0x350127` | `0F8482000000` | **`je 0x750DAF` — resolve ไม่ได้ = ข้าม entry ทั้งอัน (ไม่มีเลข)** ← เกตที่ต่างระหว่างสองเซสชัน |
| `0x00750DA8` | `0x3501A8` | `8BCF` | `mov ecx,edi` = this = actor เป้าที่ resolve ได้ |
| `0x00750DAA` | `0x3501AA` | `E831F0CEFF` | `call 0x43FDE0` |

resolver `0x446170` off `0x04557D` `83C408C20800` = **identity==0 → คืน NULL ทันที** (kill switch ที่สอง).
(*พิมพ์ผิด — off ที่ถูกของ `0x750D12` = `0x350112`.)

### 2.2 เกตใน FX dispatcher `0x43FDE0` (จัดกลุ่มตามโจทย์)

| VA | off | bytes | เกต | กลุ่ม |
|---|---|---|---|---|
| `0x0043FE12` | `0x03F212` | `A1C42E0301` | อ่าน localplayer `[0x1032EC4]` | — |
| `0x0043FE1F` | `0x03F21F` | `0F841E030000` | **GATE A**: localplayer==NULL → `je 0x440143` (ไม่วาด) | (e) |
| `0x0043FE25` | `0x03F225` | `80B82004000000` | `cmp byte [localplayer+0x420],0` | (c) |
| `0x0043FE2C` | `0x03F22C` | `0F8411030000` | **GATE B**: flag==0 → `je 0x440143` (ไม่วาด) — **toggle แสดงเลข** | (c) |
| `0x0043FE78` | `0x03F278` | `3BCE` | `cmp` localplayer.lo vs performer.lo | (a) |
| `0x0043FE86` | `0x03F286` | `7473` | **GATE C1**: performer==localplayer → `je 0x43FEFB` **ข้าม filter 6 ชั้น ไปวาด** | (a) |
| `0x0043FE8E` | `0x03F28E` | `746B` | **GATE C2**: target==localplayer → `je 0x43FEFB` ข้าม filter | (a) |
| `0x0043FE96` | `0x03F296` | `E805063100` | filter 1/6 `call 0x7504A0` (performer) | (a) |
| `0x0043FEA4` | `0x03F2A4` | `E8F7053100` | filter 2/6 `call 0x7504A0` (target) | (a) |
| `0x0043FEB6` | `0x03F2B6` | `E8D5063100` | filter 3/6 `call 0x750590` | (a) |
| `0x0043FEC4` | `0x03F2C4` | `E8C7063100` | filter 4/6 `call 0x750590` | (a) |
| `0x0043FED5` | `0x03F2D5` | `E8F6063100` | filter 5/6 `call 0x7505D0` | (a) |
| `0x0043FEE6` | `0x03F2E6` | `E8E5063100` | filter 6/6 `call 0x7505D0` | (a) |
| `0x0043FEF0` | `0x03F2F0` | `0F844D020000` | **GATE D**: filter ตกทั้ง 6 → `je 0x440143` (ไม่วาด) | (a) |
| `0x00440161` | `0x03F561` | `C21800` | `ret 0x18` — ปลายทาง `0x440143` คือ **epilogue เปล่า = NO-DRAW exit** (ยืนยันว่าทุก `je 0x440143` คือ "ไม่วาดอะไรเลย") | — |

**สำหรับ npc_sweep (performer=0x10010001=localplayer):** GATE C1 ยิงที่ `0x43FE86` → ข้าม filter 6 ชั้น → ไปวาด. ⇒ เกต (a)/visibility **ไม่ใช่** ตัวแปรของเคสนี้ (ถูก bypass). ตัวแปรจริงคือ resolve เป้า (`0x750D27`) + GATE A/B.

### 2.3 สีเลข (cross-check กับ R93)
`0x43FF01 3BCE` / `0x43FF0B B301` / `0x43FF0F 32DB` → `bl=1` เมื่อ performer==localplayer → เลือกชุด type แดง `bm_r%d` ตรงกับที่เห็น. **[PROVEN]**

### 2.4 world-to-screen / culling (กลุ่ม b)
`0x43FBB0` ดึงตำแหน่งโลกของ actor เป้าผ่าน `0x43BCE0` แล้วอ่านความสูง `[edi+0x18]` (R93 §2.4). ถ้า actor อยู่นอกจอ/หลังกล้อง FxNumber ยังถูกสร้างแต่ตำแหน่งอาจอยู่นอกเฟรม. **[LIKELY]** เป็นเกตกลุ่ม (b) แต่ static พิสูจน์ได้แค่ว่าตำแหน่งมาจาก actor เป้า ไม่ได้พิสูจน์ว่ากล้องต่างกันจริงในสองเซสชัน.

---

## 3. `[localplayer+0x420]` — toggle แสดงเลข (ตรวจซ้ำคำอ้างรอบ 100)  **[PROVEN — แก้คำอ้างเดิม]**

รอบ 100 ว่า "combat-text byte `[localplayer+0x420]` ไม่ gate เลขหลัก" — **ไบต์หักล้าง**: `0x43FE2C je 0x440143` (no-draw) อ่านตรง ๆ จาก `[localplayer+0x420]`. ถ้า byte นี้ == 0 → **เลขทุกตัวหายเงียบ**.

| VA | off | bytes | ความหมาย |
|---|---|---|---|
| `0x0042C66F` | `0x02BA6F` | `83F827` | `cmp eax,0x27` = รหัสคำสั่งอินพุต 0x27 |
| `0x0042C674` | `0x02BA74` | `A1C42E0301` | `mov eax,[0x1032EC4]` = localplayer |
| `0x0042C681` | `0x02BA81` | `389820040000` | `cmp byte [eax+0x420],bl` |
| `0x0042C687` | `0x02BA87` | `0F94C1` | `sete cl` |
| `0x0042C68A` | `0x02BA8A` | `888820040000` | `mov byte [eax+0x420],cl` = **สลับค่า 0↔1 (toggle)** |
| `0x0044CAC2` | `0x04BEC2` | `C6862004000001` | `mov byte [esi+0x420],1` = **ค่า default = ON** ตอน object init (ctor `0x44C990`, vtable `0xF0D7A8`) |

⇒ `[localplayer+0x420]` = flag แสดงเลขความเสียหาย, default ON, สลับด้วยคำสั่ง `0x27`. เป็นเกต hard ที่ปิดเลขทั้งหมดได้ แต่เป็น state **ฝั่ง client ล้วน** ไม่โผล่ในล็อกเซิร์ฟเวอร์ และ **ไม่ผูกกับ TargetVital โดยตรง** (ไม่มี writer ของ +0x420 อยู่ใน cluster TargetVital).

---

## 4. ใครลงทะเบียน `0x2001` ใน map `0x102C6C0` (กลุ่ม d)  **[PROVEN inserter] / [LIKELY pipe]**

map = std::map (rb-tree) ที่ `mgr+0x0C`; resolver `0x446170` ใช้ `equal_range 0x493880`. **ผู้เขียน** (registrar) แยกจากผู้อ่าน:

| VA | off | bytes | ความหมาย |
|---|---|---|---|
| `0x00446F37` | `0x046337` | `FF4504` | `inc [ebp+4]` = เพิ่มตัวนับ actor (registrar head `0x446F30`) |
| `0x00446F91` | `0x046391` | `E8DAF1FFFF` | `call 0x446170` = หา ก่อน (find) |
| `0x00446FA3` | `0x0463A3` | `E8E8F9FFFF` | `call 0x446990` = **ไม่พบ → allocate node แล้ว insert** |
| `0x00446990` | `0x045D90` | `6AFF689B77...` | inserter (ภายในเรียก `operator new 0x88D020` แล้วลิงก์เข้า tree ที่ `mgr+0x0C`) |

การ scan ทุก immediate `0x102C6C0` ในโค้ด: ทุกจุดเป็น GetActorMgr(`0x402A20`) / lazy-init(`0x4473F0`) / resolve(`0x446170`) — **ไม่มี insert ผ่าน immediate**; insert ไปผ่าน mgr pointer + `0x446990`. ⇒ การลงทะเบียน actor เป็นส่วนหนึ่งของ **actor-lifecycle** แยกขาดจาก TargetVital และจาก number pass.

**[LIKELY] `0x2001` = scene placement:** ใบ TargetVital ใบหลังพก `placement=P0 · data_name='Navy Transfer'` = ข้อมูล scene-placement; และสูตร id ฝั่งเซิร์ฟเวอร์ `0x2000+placement_idx+1` (อ้างใน R93) → placement P0 = `0x2001`. ⇒ NPC เข้ามาทางท่อ scene/placement-load. **[UNKNOWN]** static รอบนี้ยังไม่ปักว่าท่อ `scene-placement-load` vs `actor-entry 0x6E9D` ตัวไหน call `0x446990` สำหรับ `0x2001` โดยตรง (ต้องไล่ caller ของ inserter ต่อ — งาน static ทำต่อได้).

---

## 5. คำตัดสินสมมติฐาน (Q3)

**(ก) "การเลือกเป้าเป็นเงื่อนไขให้ FxNumber เรนเดอร์" — คะแนน: หักล้าง (false as stated).**
- ทางวาดเลขไม่มี branch ใดอ่าน "current selection". เงื่อนไขที่ทำให้ไปวาดคือ performer==localplayer (`0x43FE86`, จริงเสมอใน npc_sweep) + resolve เป้าสำเร็จ (`0x750D1E`).
- หลักฐานเวลา: เลขใบแรกขึ้นก่อน TargetVital(NPC) ~45s → selection เกิดทีหลังผล.
- ที่ correlate กับ selection เพราะ **ทั้งเลขและ TargetVital ต้องการให้ `0x2001` resolve ได้** — เงื่อนไขจริงคือ "เป้าถูก **ลงทะเบียน** (resolvable)" ไม่ใช่ "ถูก **เลือก**".

**(ข) "TargetVital ใบหลังเป็นผลของเฟรม HIT_REACTION 0x0009 เอง" — คะแนน: หักล้าง (no code path).**
- subtree ของ CHitResult handler `0x750770` และลูกทั้งหมด (`0x43FDE0, 0x43FBB0, 0xA7C010, 0xA7EBA0`) **ไม่อ้าง** TargetVital vtable `0xF1FE28` / ctor `0x51DE80` / getid `0x51DF10` / id-global `0x1082098` เลย (scan byte-range ของแต่ละฟังก์ชัน = none).
- ctor `0x51DE80` มี caller เดียว = object-factory (`0x5D8565`), ไม่ได้อยู่บนเส้น decode ของ CHitResult.
- ⇒ เส้น handler ของ CHitResult **ไม่มีทางไป send TargetVital**. ช่องว่าง ~5.5s + payload placement/data_name ชี้ไป **action เลือกเป้าแยกต่างหาก** (auto-select-on-attack เป็นพฤติกรรม UI ที่เป็นไปได้ แต่ **ไม่ได้อยู่บนเส้น decode CHitResult** — ถ้ามีจะอยู่ในโค้ด input/combat, ยังไม่ปักจุด). 

---

## 6. เกณฑ์ตัดสินสำหรับ GT-034 DAMAGE-TARGET-AB-001

A/B: แขน A = ไม่แตะเมาส์ (ไม่เลือกเป้า) · แขน B = คลิกเลือก NPC ก่อนยิงชุด sweep. คำทำนายจาก static:

- **ทำนายหลัก:** ถ้า NPC `0x2001` ถูกลงทะเบียนใน map แล้ว (scene placement โหลดแล้ว) **ทั้งสองแขนจะเห็นเลขเท่ากัน** — เพราะทางวาดเลขไม่อ่าน selection (เกต C ใช้ performer==localplayer). ⇒ **selection ไม่ควรเปลี่ยนผลเลข**. ถ้าผลออกมาต่าง (A ไม่เห็น, B เห็น) แปลว่ามีตัวแปรร่วมที่ยังไม่ถูกโมเดล (เช่น การคลิกเป็นตัวทำให้ NPC ถูก spawn/register, หรือกล้อง/ระยะต่างกัน) — ให้ล่า **timing การลงทะเบียน `0x2001`** (§4) เป็นอันดับแรก ไม่ใช่ selection.
- **เกณฑ์ผ่าน/ตกที่วัดได้ (client-observable):**
  - PASS-ปิดเรื่อง = เลข 4 ตัวขึ้นเหนือ NPC ใน **แขน A** (พิสูจน์ว่า selection ไม่จำเป็น) — สอดคล้อง static.
  - ถ้า A เงียบ B เห็น → บันทึกเป็น **หลักฐานว่า correlation มาจาก registration ไม่ใช่ selection** ก็ต่อเมื่อยืนยันด้วย wire-DB ว่าแขน A **ไม่มี** `0x2001` ใน actor set ตอนเฟรมเข้า; ถ้า A มี `0x2001` อยู่แล้วแต่ยังเงียบ → เกตอื่น (GATE B `[localplayer+0x420]`, กล้อง) เป็นผู้ร้าย.
- **ควบคุมตัวแปรบังคับ:** (1) ยืนยัน `[localplayer+0x420]==1` ทั้งสองแขน (ไม่กดคำสั่ง `0x27`) — ไม่งั้นเลขหายทั้งกระดานโดยไม่เกี่ยว selection. (2) ให้กล้องเล็ง NPC ทั้งสองแขน (กัน false-negative กลุ่ม b). (3) เก็บ wire-DB ว่า `0x2001` อยู่ใน actor registry ณ เฟรม CHitResult หรือไม่ = ตัวชี้ขาดจริง.
- **สองแขนต้องรายงาน:** เห็น/ไม่เห็นเลข (client) + `0x2001` resolvable หรือไม่ (wire-DB) + จำนวน TargetVital ที่ client ส่ง. Matrix นี้จะแยก "registration-gated" (ทำนายหลัก) ออกจาก "selection-gated" (ถ้าเกิดจริง = static พลาด, ต้องเปิดหนี้ใหม่).

---

## 7. [UNKNOWN] / งานที่ต้องไล่ต่อ

- **จุด socket-send ของ TargetVital และปุ่ม UI ที่ทริก** — พิสูจน์แล้วว่าคลาส/ทะเบียน/factory คืออะไร และเป็น **ผู้บริโภค map** แต่ **ยังไม่ปัก** instruction ที่ serialize (WriteField) + ส่งออก socket, และยังไม่ปักว่ารหัสคำสั่งอินพุตตัวไหน (คลิกเลือก/Tab) สร้างและส่ง. serializer ของ TargetVital ดูเป็น generic base (hierarchy: vtable `0xF1FE28` → base `0xF202D0` → …) ไม่ได้เรียก `0x89A600` ตรง ๆ ใน cluster.
- **field layout ของ wire** (actor_id 64-bit / placement / data_name wide) — อนุมานจากพยาน runtime + บทบาท resolve ของคลาส = **[LIKELY]**; ยังไม่ถอด serializer ยืนยัน offset/tag.
- **ท่อลงทะเบียน `0x2001` (scene-placement vs actor-entry 0x6E9D)** — inserter `0x446990` เป็น [PROVEN] แต่ caller-pipe เฉพาะของ `0x2001` ยังเป็น [LIKELY scene placement] / [UNKNOWN exact].
- **`0x7504A0 / 0x750590 / 0x7505D0`** (filter 6 ชั้น) — รู้แค่รับ identity คืน bool (หนี้ R93 ต่อเนื่อง).

## 8. NONCLAIMS

- ทุกข้อเป็นข้อเท็จจริงของ **ไคลเอนต์ตัวเดียวที่ตรึงด้วยแฮช** ไม่ใช่หลักฐานจากเซิร์ฟเวอร์ต้นฉบับ (ปิดไปแล้ว ห้ามอ้าง).
- **ไม่มี runtime observation** ในเอกสารนี้ — ไม่เปิดเกม ไม่บูตเซิร์ฟเวอร์ ไม่แตะ DB; พยานผู้เทส/ล็อกเซิร์ฟเวอร์ใช้เพียงเพื่อเลือกว่าจะไปดูไบต์ตรงไหน.
- **ไม่ได้พิสูจน์ว่า `0x2001` อยู่ใน map ตอนรันของเซสชันใด** — เป็นการทำนายเงื่อนไข ไม่ใช่ผลที่วัดแล้ว.
- **ไม่ยืนยันว่า correlation "เห็นเลข ⇔ TargetVital" เป็นเหตุ-ผล** — static บอกได้แค่ว่าทั้งคู่แชร์เงื่อนไข resolve เดียวกัน; ความเป็นเหตุต้องพิสูจน์ด้วย GT-034.
- **ไม่ได้ตั้งชื่อเชิงความหมายให้ flag/field** — `[localplayer+0x420]` = "byte ที่คำสั่ง 0x27 สลับ และ FX dispatcher อ่านเป็น on/off"; ชื่อ "toggle แสดงเลข" มาจากพฤติกรรม ไม่ใช่ label ในอิมเมจ.
- **ไม่ถอด serializer/handler ของ TargetVital ครบ** — จึงไม่ยืนยัน wire field offsets; data_name/placement เป็น [LIKELY] จากพยาน.
- **ไม่แตะรีโป / ไม่ commit / ไม่แตะ canonical DB / ไม่แก้ LOCK-QUEUE** — อ่านไบนารีอย่างเดียว, สคริปต์รันใน `/tmp/`.

## 9. Verify
`/tmp/verify_r102.py` (scratch): `NAMEID(TargetVital)=0x1ADD OK` · `GUARDS 41/41 PASS` — re-reads pinned image, asserts every cited byte-range.
