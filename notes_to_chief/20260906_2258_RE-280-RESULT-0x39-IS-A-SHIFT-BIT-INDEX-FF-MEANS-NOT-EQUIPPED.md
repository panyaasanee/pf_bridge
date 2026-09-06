[ถึง: LANE-DB | ADDRESSEE: LANE-DB | cc: chief, COO | จาก: RE runner บนเครื่อง Panya | 2026-09-06T22:58+07:00]

# RE-280 RESULT — `ItemAttr+0x39` คือ **เลขบิต (shift count)** ของช่องอุปกรณ์ · `0xFF` = ไม่ได้สวม

**สถานะ: DONE (ask 1 + ask 2 + ask 3) / static ล้วน · ชั้น client-observable ยังเป็นของบล็อก ATTENDED ในใบเอง**

**คำตอบหนึ่งบรรทัดสำหรับแขน (ข):** เฟรมตอบต้องส่ง `ItemAttr+0x39 = N` โดย **N ไม่ใช่ `0xFF`** — client เอา N ไปทำ `mask = 1 << N` ตรง ๆ (`0x005833F9`/`0x005833FE`) ไม่มีการ lookup ตารางใด ๆ ระหว่างทาง ⇒ **N คือดัชนีบิตของช่องอุปกรณ์ ไม่ใช่รหัส equip-type**

- START `2026-09-06T22:52:31+07:00` · ผลเสร็จ `2026-09-06T22:58+07:00` · ทุก input read-only
- ticket: `RE-280` (`CLIENT_RE_QUEUE.md` บรรทัด 1327-1451)

## input + SHA (ตรวจก่อน/หลังงาน ตรงกัน)

| ไฟล์ | sha256 |
|---|---|
| `GameClient/GameClient.local.bin` (14,759,424 B · ImageBase `0x00400000` · `.text` rva `0x1000` raw `0x400`) | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| `external/PF_ATTR_FIELD_SEMANTICS.tsv` | `1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f` |
| `external/PF_SERIALIZER_FIELDS.tsv` | `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` |

span_sha256 ของช่วงที่ดิสแอสเซมบลีจริงรอบนี้:

| ช่วง VA | คืออะไร | span_sha256 |
|---|---|---|
| `0x0046BD30`–`0x0046BEA1` | ItemAttr codec (สองทิศ) | `b21137bde28452c08f8fa6a2eda18accf9c2d51b9b7d82a1b6997986feba86c1` |
| `0x005EDA20`–`0x005EDC31` | `ItemOperateVitalRes` codec | `b5f6a1586a810c0a98ceb7c925a0d4afa10cff41db661eb0947b8918f3a11d54` |
| `0x00583380`–`0x00583420` | equipment-UI bitmask builder | `718a7574e00a07efe751104028de2b8ed95ee9d7e3aba0af35c1a4939641c83d` |

## ค้นก่อนถอด

- **ค้นใน `pf_bridge/external/` แล้ว: เจอ** `PF_ATTR_FIELD_SEMANTICS.tsv` แถว 478-481 = `ItemAttr@0x39` สี่แถว (R/W × vtable `0x00F0EBB0` / `0x00F4A188`): `offset=0x39 tag=0x08 len=1 gate=ALWAYS`, `default_value=0xFF`, `default_writer_va=0x0046B466`, `write_site=0x0046BD92`, `read_site=0x0046BE1F`, span `0x0046BD30..0x0046BEA1` — **verify กับอิมเมจแล้ว span sha ตรง** (ไม่ได้เชื่อตารางลอย ๆ) · `PF_SERIALIZER_FIELDS.tsv` ไม่มีแถว offset `0x39` ของ `ItemOperateVitalRes` (ตรงกับที่ใบบอกว่า layout ไม่ครบ)
- **ค้น `gamedata/` แล้ว: ไม่เกี่ยว** — คำถามอยู่ในโค้ดที่เกมรัน ไม่ใช่ตารางที่เกมอ่าน (ยืนยันตามที่ใบเขียนไว้เอง)

---

## ✅ ask 1 [หลัก] — ค่า N ที่ไม่ใช่ `0xFF` แปลว่าอะไร

### 1.1 จุดตั้ง sentinel — ยืนยันคำที่ใบเดาไว้ พร้อมไบต์

```
0x0046B440  C7 06 B0 EB F0 00  mov dword ptr [esi], 0xf0ebb0     <- vtable ItemAttr
0x0046B44D  83 C9 FF           or  ecx, 0xffffffff               <- cl = 0xFF
0x0046B463  88 5E 38           mov byte ptr [esi + 0x38], bl     (bl = 0)
0x0046B466  88 4E 39           mov byte ptr [esi + 0x39], cl     <- +0x39 = 0xFF  (ctor 0x0046B410)
```
⇒ `default_writer_va=0x0046B466` ใน TSV **ถูกต้อง** และค่าที่เขียนคือ `0xFF` จริง (มาจาก `or ecx,-1`)

### 1.2 ผู้บริโภคที่ตัดสิน "สวมอยู่ช่องไหน" — นี่คือคำตอบ

```
0x005833AC  8B 4B 18           mov ecx, [ebx + 0x18]
0x005833AF  8A 51 39           mov dl, byte ptr [ecx + 0x39]
0x005833B2  3A 15 AF EB F0 00  cmp dl, byte ptr [0x00F0EBAF]     <- เทียบกับ sentinel
0x005833B8  74 6C              je  0x00583426                    <- เท่ากับ sentinel = ข้ามไอเทมนี้ (ไม่สวม)
...
0x005833F6  8A 48 39           mov cl, byte ptr [eax + 0x39]
0x005833F9  BA 01 00 00 00     mov edx, 1
0x005833FE  D3 E2              shl edx, cl                       <- mask = 1 << N
0x00583411  89 54 24 44        mov [esp + 0x44], edx             <- เก็บ mask ลงเรคคอร์ด
0x00583415  89 7C 24 4C        mov [esp + 0x4c], edi             (= [item+0x28])
0x00583419  89 6C 24 50        mov [esp + 0x50], ebp             (= [item+0x2c])
0x0058341D  E8 8E DB FF FF     call 0x00580FB0                   <- ส่งเรคคอร์ดเข้า list ของ UI
```

**ค่าไบต์ที่ `0x00F0EBAF` = `0xFF`** (วัดจากอิมเมจ · อยู่ใน `.rdata` = read-only ⇒ คงที่ตอนรัน)
ไบต์รอบ ๆ: `... 45 78 70 72 65 73 73 42 61 67 41 74 74 72 00 | FF | C0 B3 46 00 ...`
(คือไบต์สุดท้ายก่อน vtable `0x00F0EBB0` ซึ่งสล็อต 0 = `0x0046B3C0` · **ตำแหน่งประหลาดแต่เป็นค่าคงที่จริง**)

⇒ **ตอบตรงคำถามของใบ: "ค่า N ที่ไม่ใช่ 0xFF หมายถึงสวมอยู่ที่ shift-bit N ใช่หรือไม่" = ใช่**
N ถูกใช้เป็น shift count ล้วน ๆ ไม่มี lookup กลางทาง · เกตเดียวคือ `N == 0xFF ⇒ ไม่สวม`
ผลข้างเคียงที่ต้องรู้: `shl` ใช้ `cl & 31` ⇒ **N ที่มีความหมายจริงคือ 0..31** (นี่เองคือเหตุผลที่ต้องมี sentinel แยก — ถ้าไม่กัน `0xFF` จะกลายเป็นบิต 31)

### 1.3 มีตารางแม็ป N → equip-type ไหม

**ไม่พบในเส้นทางนี้ (bounded negative)** — ขอบเขตที่ตรวจ: ทั้งเส้นจาก `[item+0x39]` ถึงจุดสร้าง mask (`0x00583380..0x00583420`) ไม่มี `movzx`+`mov reg,[base+reg*4]` หรือการอ่านตารางใด ๆ · mask ถูกส่งต่อเป็น bitfield ดิบพร้อม `[item+0x28]`/`[item+0x2C]` เข้า `0x00580FB0`
⇒ **การแม็ป "บิตที่ N ↔ ช่องบนจอช่องไหน" อยู่ในผู้บริโภค mask ไม่ใช่ในตารางฝั่ง item** ⇒ ตรงกับที่บล็อก `ATTENDED` ของใบวางไว้ (อ่านค่า N ที่ client เขียนตอนลากของลงแต่ละช่อง) — static ตอบได้ถึงตรงนี้

🔴 **ข้อควรระวังสำหรับ encoder ของ LANE-DB:** `value=8` ที่ client ส่งใน `ItemOperateVitalReq` op=5 **ไม่ควรถูกก๊อปไปใส่ `+0x39` โดยอัตโนมัติ** — ถ้า 8 คือ `n_EQUIPTYPE` มันจะกลายเป็นบิต 8 ซึ่งอาจไม่ใช่ช่องอาวุธ · ใบเองก็ตั้ง nonclaim ข้อ 1 ไว้แล้ว · static รอบนี้**ไม่**ยืนยันและ**ไม่**หักล้างความบังเอิญนั้น

## ✅ ask 2 [รอง] — W3/W5/W7/W10/W11/W12/W13 เป็น non-wire จริงไหม (เฉพาะ `0x005EDA20`)

สำมะโน call ทุกจุดในสแปน `0x005EDA20..0x005EDC31` (19 จุด) แล้วเปิดดูปลายทางทีละตัว + resolve import จาก import directory จริง:

| จุดเรียก | ปลายทาง | คืออะไร (วัดแล้ว) | wire? |
|---|---|---|---|
| `0x5EDA63,0x5EDA7E,0x5EDAAB,0x5EDAE6,0x5EDB0C` | `0x0089A600` | generic **writer** ของสาย (ตัวเดียวกับที่ ItemAttr codec ใช้) | ✅ wire |
| `0x5EDB33,0x5EDB48,0x5EDBA2,0x5EDBBD,0x5EDBCD` | `0x0089A640` | generic **reader** ของสาย | ✅ wire |
| **`0x5EDA91` (W3)** | `call edx` จาก `mov ecx,[esi+0x14]; mov eax,[ecx]; mov edx,[eax+0x34]` | **virtual codec dispatch สล็อต `+0x34` ของอ็อบเจ็กต์ลูกที่ `this+0x14`** — สล็อตเดียวกับที่ ItemAttr ใช้ (`0x00F0EBB0+0x34 = 0x0046BD30`) | 🔴 **wire — ไม่ใช่ non-wire** |
| **`0x5EDB90` (W12)** | เหมือนกันทุกไบต์ (`8B 4E 14 / 8B 01 / 8B 50 34 / FF D2`) | เหมือน W3 คนละทิศ | 🔴 **wire — ไม่ใช่ non-wire** |
| `0x5EDAD2,0x5EDAF8` (W5/W7) | `call dword ptr [0x00C3B4C0]` | **`MSVCR90.dll!_invalid_parameter_noinfo`** (resolve จาก import directory จริง) | ❌ non-wire (CRT param check) |
| `0x5EDB73` (W10) | `0x0088D060` → `call dword ptr [0x00C3B1B4]` | **`KERNEL32.dll!InterlockedDecrement`** บน `this+0x0C` | ❌ non-wire (refcount) |
| `0x5EDB81` (W11) | `0x0088D050` → `call dword ptr [0x00C3B1B0]` | **`KERNEL32.dll!InterlockedIncrement`** บน `this+0x0C` | ❌ non-wire (refcount) |
| `0x5EDB61` | `0x0046F4D0` | plain itembag factory (ตรงกับ `test_item_operate_result_optional_bag_is_plain_not_collection`) | ❌ non-wire (allocation) |
| **`0x5EDC06` (W13)** | `0x005ED2F0` | ดู ask 3 | ❌ non-wire (container) |
| `0x5EDB22` | `0x005EDC1B` | epilogue/SEH unwind ในฟังก์ชันเดียวกัน | ❌ non-wire |

⇒ **W5/W7/W10/W11/W13 = non-wire ยืนยันแล้วเฉพาะฟังก์ชันนี้ (ไม่ใช่ analogy)**
⇒ 🔴 **W3/W12 = wire ต้องแก้สมมติฐานของใบ** — เป็นการเรียก codec ของอ็อบเจ็กต์ลูก (ItemAttr/ItemBag) ผ่าน vtable ไม่ใช่ artifact
⇒ ผลกับ `PF_V5_P1_OPEN.tsv:77` / `PF_PROTOCOL_PRIORITY.tsv:47`: blocker `DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED` **แก้ได้แล้ว** — dynamic dispatch สองจุดนั้น resolve เป็นสล็อต `+0x34` ของ attribute object · **แต่ RE runner ไม่แก้ไฟล์ใน `external/` เอง** (ข้อห้ามของรอบ) ⇒ ฝากผู้ถือไฟล์เติมแถว `ItemOperateVitalRes` เข้า `PF_A2_POOL_46F4D0_DELTA.tsv` + `PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv` **เฉพาะ W5/W7/W10/W11/W13 เท่านั้น ห้ามใส่ W3/W12**

## ✅ ask 3 — `0x005ED2F0` คืออะไร

```
0x005ED2F0  83 EC 08        sub esp, 8
0x005ED2F3  56              push esi
0x005ED2F4  8B F1           mov esi, ecx
0x005ED2F6  8B 4E 0C        mov ecx, [esi + 0x0C]      <- begin
0x005ED302  8B 46 14        mov eax, [esi + 0x14]      <- end_cap
0x005ED305  2B C1 / C1 F8 05   (end_cap-begin) >> 5    <- element size = 0x20
0x005ED30A  8B 7E 10        mov edi, [esi + 0x10]      <- end
0x005ED30F  2B D1 / C1 FA 05   (end-begin) >> 5
0x005ED314  3B D0 / 73 31   cmp; jae 0x5ED349          <- ถ้าเต็มไปทางขยาย
0x005ED333  E8 18 D7 FF FF  call 0x005EAA50            <- ตัวช่วย leaf (ret ที่ 0x005EAA9A ไม่มี call ใด ๆ)
0x005ED346  ret
```
⇒ **เป็น container helper แบบ `vector<T>` ที่ `this+0x0C/+0x10/+0x14` (element 32 ไบต์) — push_back/grow ไม่ใช่ serializer**
⇒ ตรวจแล้วว่า **ทั้งตัวมันและ `0x005EAA50` ไม่เรียก `0x0089A600`/`0x0089A640` เลย** ⇒ non-wire ยืนยัน (ปิดข้อ 3 ของใบ: "ไม่มี closure ไหนอธิบายที่อยู่นี้" — ตอนนี้มีแล้ว)

## เกร็ดที่เจอระหว่างทาง (ไม่ใช่คำตอบของใบ แต่ LANE-DB ควรรู้)

- `+0x39` บนสาย: อยู่ใน ItemAttr codec `0x0046BD30` **เสมอ ไม่มีเกต** ลำดับ: `+0x28` tag `0x32` len 8 → `+0x30` tag `0x14` len 4 → `+0x36` tag `0x0F` len 2 → `+0x34` tag `0x0F` len 2 → `+0x38` tag `0x08` len 1 → **`+0x39` tag `0x08` len 1** (`lea edx,[esi+0x39]` ที่ `0x0046BD92`) → presence tag `0x0B` len 1 ของอ็อบเจ็กต์ลูกที่ `+0x3C` → ลูกเรียก codec ตัวเองผ่าน `vtable+0x34`
- vtable ที่สองของ ItemAttr (`0x00F4A188`, ตัวที่ TSV ผูกกับ stall list) แชร์สล็อต `+0x10..+0x30` กับ `0x00F0EBB0` แต่ codec เป็นของตัวเอง (`+0x34 = 0x00766C90`)
- 🔴 **แก้ข่าวเชิงป้องกัน:** VA `0x005ED722` มี `mov byte ptr [esi+0x39], 0` แต่ **ไม่ใช่ ItemAttr** — เป็น ctor ที่ `0x005ED6C0` ของคลาสอื่น (vtable `0x00F30744`, codec สล็อต `+0x34 = 0x005ED2E0`) ที่บังเอิญ layout ใกล้กัน · อย่าเอาไปอ้างว่า "มีที่ที่ตั้ง +0x39 = 0 ให้ ItemAttr"

## nonclaims

1. ไม่ได้พิสูจน์ว่า "บิตที่ N" ตรงกับช่องไหนบนจอ — static บอกได้แค่ `mask = 1<<N` และ mask ถูกส่งเข้า `0x00580FB0` · การจับคู่บิต↔ช่องยังต้องใช้บล็อก ATTENDED ของใบเอง
2. ไม่ได้พิสูจน์ว่า `value=8` ใน `ItemOperateVitalReq` op=5 คือ `n_EQUIPTYPE` หรือคือค่า `+0x39` ที่ต้องตอบกลับ
3. ไม่ได้รัน `tests/test_equip_state_static.py` (ไม่ใช่งานของรอบนี้ และห้ามแตะรีโปเซิร์ฟเวอร์) — อ่านผลเชิงโครงสร้างจากอิมเมจเอง ซึ่ง**ตรงกับ**สิ่งที่เทสนั้น assert ไว้
4. ไม่ได้ census ว่าใครเรียก `0x0046BD30` ทั้งอิมเมจ (ไม่ได้ถาม)
5. ผลลบข้อ 1.3 มีขอบเขต = สแปน `0x00583380..0x00583420` เท่านั้น ไม่ใช่ image-wide
6. ไม่ได้แตะ/แก้ไฟล์ใด ๆ ใน `GameClient/`, `external/`, `gamedata/`, `SERVER/` หรือไฟล์คิว · ไม่ได้บูตอะไร · ไม่จับ `LOCK_GAME`

## BUILD_IMPACT

- **แขน (ข) ปลดบล็อกได้ทันทีในระดับ "รู้ต้องส่งอะไร"**: encoder ของ `ItemOperateVitalRes` (0x4C13) ต้องใส่ `ItemAttr+0x39 = N` (tag `0x08`, len 1, ตำแหน่งตามลำดับข้างบน) โดย N ≠ `0xFF` และ N ∈ 0..31 · ค่า N ที่ "ถูก" ต่อช่องยังต้องยืนยันด้วยบล็อก ATTENDED ของใบ (หรือลองส่ง N=0..k แล้วดูช่องที่ติด — เป็นการทดลองฝั่ง client ล้วน ไม่ต้องรอ RE เพิ่ม)
- ไม่มี CORE-REQUEST จากรอบนี้ · ไม่มีการแก้โค้ดเซิร์ฟเวอร์โดย RE runner
