# RE-294 RESULT — `StallOpenVital` **ไม่เขียนเพิ่ม** · `StallStartVital` **เขียน** ผ่าน `0x00766C00` (ถอดครบแล้ว)

ADDRESSEE: LANE-UI — เจ้าของใบ/ผู้บริโภคผล · cc: chief, COO
ผู้ทำ: RE runner บนเครื่องสะพาน (static, read-only) · รอบ `RE-RUNNER-20260907_1100-OWNER-ORDERED-FULL-SWEEP`

## สถานะ: **PASS / DONE** — ตอบคำถามเดียวของใบครบทั้งสองคลาส

---

## 🔴 ก่อนอื่น: VA สองตัวที่ใบ (และแผน `UI_LANE.md`) เรียกว่า "serializer" **ไม่ใช่ serializer**

```
0076ac20  66 a1 ac af 08 01   mov ax, ds:0x0108AFAC      <- StallStartVital
0076ac26  c3                  ret
0076acb0  66 a1 b0 af 08 01   mov ax, ds:0x0108AFB0      <- StallOpenVital
0076acb6  c3                  ret
0076a080  66 a1 b4 af 08 01   mov ax, ds:0x0108AFB4      <- StallOperateVital
0076a086  c3                  ret
```

สองคำสั่ง คืนค่า u16 = **class id getter** (vtable slot `+0x10`) **ไม่เขียนอะไรลงสตรีมเลย**
คอลัมน์ที่ใบหยิบมาคือ `getter_va` ไม่ใช่ `serializer_va` — หัวตาราง `PF_PROTOCOL_REGISTRY.tsv` คือ
`name · name_va · reg_site_va · id_global_va · **getter_va** · vtable_va · **serializer_va** · handler_va`

| คลาส | getter | vtable | **serializer (ตัวจริง)** | handler |
|---|---|---|---|---|
| `StallStartVital` | `0x0076AC20` | `0x00F4A480` | **`0x0076A740`** | `0x0076B0D0` |
| `StallOpenVital` | `0x0076ACB0` | `0x00F4A4A4` | **`0x0076A960`** | `0x0076B0D0` |
| `StallOperateVital` | `0x0076A080` | `0x00F4A418` | **`0x0076A630`** | `0x0076B0D0` |

**และ `0x0076B0D0` ที่ใบสังเกตว่าสามคลาสใช้ร่วมกัน = `handler` (ฝั่งรับ) ไม่ใช่ serializer**
— แบบเดียวกับ `0x00A106C0` ที่ `RE-283` พบว่า 11 คลาสใช้ร่วมกัน · handler ที่แชร์กันเป็นเรื่องปกติ
ในไบนารีนี้ ไม่ได้แปลว่าสามคลาสเข้ารหัสเหมือนกัน

---

## คำตอบ

### `StallOpenVital` (`0x0076A960`, 690 ไบต์) — **ไม่เขียน** ✅

สำมะโน call ทุกตัวในตัวฟังก์ชัน:

| ปลายทาง | จำนวน | คืออะไร | เขียนสตรีมไหม |
|---|---|---|---|
| `0x0089A600` / `0x0089A640` | 5 / 5 | เขียน/อ่านฟิลด์ติดแท็ก | **ใช่ (คือ prefix เอง)** |
| `0x0089A810` / `0x0089A880` | 1 / 1 | เขียน/อ่านสตริง | **ใช่ (คือ prefix เอง)** |
| `ds:0x00C3B4C0` → `0x00C17860` | 5 | ตัวรายงาน invalid-parameter ของ MSVC | **ไม่** |
| `0x0088D050` | 2 | `add ecx,0x0C; call ds:0xC3B1B0` = **InterlockedIncrement** refcount | **ไม่** |
| `0x0088D060` | 2 | `lea eax,[esi+0x0C]; call ds:0xC3B1B4` = **InterlockedDecrement** + ทำลายถ้าเป็นศูนย์ | **ไม่** |
| `0x00B0BF70` | 1 | ตัวตรวจ iterator (`cmp [esi],0` แล้วเรียก `ds:0xC3B4C0`) | **ไม่** |
| `0x00766EF0` | 1 | helper คอนเทนเนอร์ | **ไม่** |
| `0x0068E8B0` | 1 | insert เข้าคอนเทนเนอร์ | **ไม่** |

**⇒ ไม่มี call ตัวใดใน `StallOpenVital` ที่รับพอยน์เตอร์สตรีมเป็นอาร์กิวเมนต์
นอกจาก primitive สี่ตัวที่เป็น prefix เอง ⇒ prefix คือทั้งเฟรม**
⇒ **ปลดล็อก `ui_stall_wire.py` สำหรับ `StallOpenVital` W1-W5 ได้ทันที**

### `StallStartVital` (`0x0076A740`) — **เขียน** ผ่าน `0x00766C00` เท่านั้น ⚠️→✅

`SUBCALL:0x00766C00` ถูกเรียกสองครั้ง (`0x0076A836`, `0x0076A8E4`) และ**รับสตรีมตัวเดียวกับ prefix**:

```
76a77c  mov ebx,[esp+0x50]        ; ebx = stream (prefix ใช้ตัวนี้: mov ecx,ebx; call 0x89a600)
...
76a82d  mov edx,[esp+0x48]        ; flag เขียน/อ่าน
76a831  mov ecx,[ebp+0x10]        ; อ็อบเจ็กต์สมาชิกในคอนเทนเนอร์ = this
76a834  push edx
76a835  push ebx                  ; <<<< สตรีมตัวเดียวกับ prefix
76a836  call 0x00766C00
```

เข้าเกณฑ์ข้อแรกของใบเป๊ะ ("call นั้นรับ pointer ตัวเดียวกับที่ prefix เขียนลงไปเป็นอาร์กิวเมนต์")

**แต่ข่าวดี: `0x00766C00` ถอดครบแล้วในรอบนี้ — มันสั้นและปิดตัวเอง (`ret 8`, ไม่มี subcall ต่อ):**

| ลำดับ | TAG | ขนาด | ที่มา | VA ที่เขียน |
|---|---|---|---|---|
| 1 | `0x32` | 8 | `elem+0x10` | `0x00766C19` |
| 2 | `0x14` | 4 | `elem+0x18` | `0x00766C28` |
| 3 | `0x0F` | 2 | `elem+0x1C` | `0x00766C37` |
| 4 | `0x19` | 4 | `elem+0x20` | `0x00766C46` |

(ฝั่งอ่านที่ `0x00766C50` เป็นกระจกเงาตัวต่อตัวด้วย `0x0089A640` — ลำดับและแท็กเดียวกัน)

**⇒ "เหลืออะไรต้องแกะ" = ไม่เหลือแล้ว** เฟรม `StallStartVital` = prefix + (สี่ฟิลด์นี้ × จำนวนสมาชิก
ในคอนเทนเนอร์ที่ `[this+0x34]`..`[this+0x4C]`)

### `StallOperateVital` (`0x0076A630`) — แถมให้ ตอบด้วยตรรกะเดียวกัน

เรียก `0x00766C00` **4 ครั้ง** และมี primitive 13/13/3/3 ⇒ **เขียน** ด้วยตัวเดียวกัน
⇒ ตารางสี่ฟิลด์ข้างบนใช้ได้กับคลาสนี้ด้วย

---

## แปลป้าย `OPEN` ทั้งห้าใน `PF_PROTOCOL_PRIORITY.tsv:510-513` — ปิดได้กี่ข้อ

| ชื่อเหตุผล | ผลรอบนี้ |
|---|---|
| `invalid_parameter_import_call_wire_effect_unproved` | ✅ **ปิด** — `ds:0xC3B4C0` → `0x00C17860` เป็นตัวรายงาน invalid-parameter ของ MSVC ถึงได้เฉพาะสาขา iterator ไม่ตรง **ไม่มีผลต่อ wire** |
| `atomic_target_object_alias_unproved` | ✅ **ปิด** — `0x0088D050` = `add ecx,0x0C` + `InterlockedIncrement` · เป้าหมายคือ refcount ที่ `this+0x0C` ไม่ใช่บัฟเฟอร์ |
| `dynamic_vtable_plus_0x04_target_unresolved` | ✅ **ปิด** — `0x00766DF0` (ตัว `+0x04`) เป็น pool factory (`push 0x00F0A90C; mov ecx,0x0102DDD4`) ตามด้วย AddRef · **ไม่แตะสตรีม** |
| `direct_call_not_proven_serializer` | ✅ **ปิด** — พิสูจน์แล้วว่า `serializer_va` ที่ลงทะเบียนเรียก primitive `0x0089A600/0x0089A810` โดยตรง |
| `indirect_call_not_proven_serializer_slot` (เฉพาะ `StallOpenVital`) | ✅ **ปิด** — สำมะโน call ทั้งฟังก์ชันข้างบน ไม่มี indirect call ที่รับสตรีม |
| `mutable_chain_target_object_alias_unproved` | ✅ **ปิด** — `0x0068E8B0` รับ `lea ecx,[esp+0x20]` / `lea edx,[esp+0x2C]` = **ตัวแปรบนสแตก ไม่ใช่สตรีม** และอยู่บนสาขาอ่าน (`mov BYTE [esp+0x44],1`) = insert เข้าคอนเทนเนอร์ |

---

## เรื่อง `0x0076A630` กับข้ออ้างเก่าใน `archive/...R77.md:64` — **สองแหล่งไม่ได้ขัดกัน**

R77 เขียนว่า serializer ของ `StallOperateVital` คือ `0x76A630` — **ถูก** ตรงกับคอลัมน์
`serializer_va` ของ registry · ส่วน `direct_call_not_proven_serializer` ใน
`PF_PROTOCOL_PRIORITY.tsv` เป็นป้าย **"ยังไม่มีใครพิสูจน์"** ไม่ใช่ป้าย **"พิสูจน์แล้วว่าไม่ใช่"**
⇒ ไม่ใช่ความขัดแย้ง เป็นช่องว่างหลักฐานที่รอบนี้เพิ่งปิด
🔴 **แต่ผมไม่ได้ยืนยันเลย์เอาต์ฟิลด์ที่ R77 อ้าง** (`u8 0x08@+0x14 · qword 0x32@+0x18 · u32 0x14@+0x20 · string@+0x24`)
— รอบนี้ถอดเฉพาะ `0x00766C00` ไม่ได้ถอด `0x0076A630` ทีละฟิลด์ ⇒ **อย่าเพิ่งเอาเลย์เอาต์ของ R77 ไปใช้**

---

## BUILD_IMPACT

1. **`StallOpenVital` W1-W5 encode ได้ทันที** — prefix คือทั้งเฟรม
2. **`StallStartVital` / `StallOperateVital` encode ได้เช่นกัน** ถ้าเติมสี่ฟิลด์ของสมาชิกตามตาราง
   ⇒ แถว `Stall` ในแผนถอด `NEEDS-RE-STATIC` ออกได้ทั้งสามคลาส
3. **แก้ `docs/UI_LANE.md` และแผนอื่นที่ชี้ `0x0076AC20`/`0x0076ACB0` ว่าเป็น serializer** — ผิดคอลัมน์
4. **แก้ 6 ป้าย `OPEN` ใน `external/PF_PROTOCOL_PRIORITY.tsv:510-512`** ตามตารางข้างบน
   (เจ้าของไฟล์นั้นเป็นคนแก้ ไม่ใช่ RE runner)
5. ⚠️ **ทุกเฟรมยังต้องมี `vital_version` (u8 tag `0x0B`) นำหน้า** ตามที่ `RE-292` ในรอบเดียวกันนี้
   วัดไว้ — prefix ที่ใบพูดถึงเริ่มหลังไบต์นั้น

## nonclaims

1. **ไม่ได้ถอดฟิลด์ของ `0x0076A630` ทีละตัว** ⇒ ไม่ยืนยันและไม่หักล้างเลย์เอาต์ของ R77
2. **ไม่ได้วัดของจริงบนสาย** — `PF_FIELD_VALIDATION.tsv:1016-1021` ยัง `NOT_OBSERVED` เหมือนเดิม
   ผลนี้เป็น static ล้วน ชั้น wire/DB **ไม่มีชั้น client-observable**
3. 🔴 **ข้อจำกัดของวิธี ต้องบอก**: ตัวหาขอบเขตฟังก์ชันของผมใช้ฮิวริสติก "ret ตามด้วย int3 ติดกัน"
   สำหรับ `0x0076A740` มัน**เลยขอบไปกินคอนสตรัคเตอร์ที่อยู่ติดกัน** (`0x0076ABC8`
   `mov DWORD PTR [esi],0x00F4A480` = ติดตั้ง vtable) ⇒ `call 0x006A57F0` ที่ `0x0076ABD9`
   **อยู่ในคอนสตรัคเตอร์ ไม่ใช่ในเส้นทาง serialize** — ผมจึงไม่นับมันเป็นคำตอบ
   call ที่ผมจำแนกทั้งหมดอยู่ในช่วง `0x0076A76E`-`0x0076AB6x` ซึ่งอยู่ในตัว serializer แน่นอน
4. **ไม่ได้ใช้ linear disassembler เป็นหลักฐานผลลบ** — ผลลบทุกข้อมาจากการอ่านอาร์กิวเมนต์
   ที่จุดเรียกจริง (สตรีมถูก push หรือไม่) และจากการเดิน callee ลงไปสองชั้นเพื่อหา primitive
5. **ไม่อ้างว่าเซิร์ฟเวอร์ควรส่งอะไร** — ตอบเฉพาะรูปเฟรมของไคลเอนต์

## SHA (ก่อน = หลัง)

| ไฟล์ | ขนาด | sha256 |
|---|---|---|
| `GameClient\GameClient.local.bin` (read-only) | 14,759,424 | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
