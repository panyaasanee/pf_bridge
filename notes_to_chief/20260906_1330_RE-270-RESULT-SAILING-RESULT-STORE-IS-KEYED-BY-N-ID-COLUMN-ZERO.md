# RE-270 RESULT — `SAILING_RESULT` store ที่ `0x0072FE50` คีย์ด้วย **`n_ID`** (คอลัมน์ที่ 0 ของ record)

- ผู้ทำ: RE runner (local, เครื่องสะพาน) รอบ `2026-09-06T13:19+07:00`
- เจ้าของใบ/ผู้บริโภคผล: **LANE-A**
- ชั้นของผล: **static IMAGE เท่านั้น** ⇒ ปิดเป็น **BOUNDED-POSITIVE (ห้ามเขียน DONE)** ตามเกณฑ์ปิดใบข้อ 3 — ชั้น client-observable เป็นของ `GT-233` v3 ไม่ใช่ใบนี้

## คำตอบหนึ่งบรรทัด
store ที่ `this+0x0C` (ตัวที่ `0x0072F700` ใช้ `find`) **คีย์ด้วยค่าที่ offset 0 ของ record buffer = คอลัมน์แรกของ `CONSTDATA_TH__SAILING_RESULT.tsv` = `n_ID`** — **ไม่ใช่ `n_AREA`** (`n_AREA` ถูกดึงมาด้วยชื่อคอลัมน์แล้ววางเป็น payload ที่ `+0x04` ของ struct ค่า ไม่ใช่คีย์) และ**ไม่ใช่ composite/packed**

## input + fingerprint (read-only ทั้งหมด · ตรวจก่อน/หลังงานตรงกัน)
| ไฟล์ | sha256 |
|---|---|
| `GameClient/GameClient.local.bin` (14,759,424 B, ImageBase `0x00400000`) | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| `gamedata/tables/CONSTDATA_TH__SAILING_RESULT.tsv` (139 บรรทัด) | `9a047da026c12c2909e9c2725a19e49713161c5d9e10c108e386157446323d2c` |

`span_sha256` ของช่วงที่ดิสแอสเซมบลีจริง:
| ช่วง VA | ความหมาย | span_sha256 |
|---|---|---|
| `0x0072FE50`–`0x00730060` | store build (ตัวสร้าง) | `9016b1628cce65662f8520b4f8f69dacf1529c4f30efd959bc4fa8fa437945e3` |
| `0x00730060`–`0x00730140` | insert tail + ปลายลูป | `2ce4ccd1f7154d273acf6a015495deb94a52c7dc1be9c298bee7e2fa038d7b37` |
| `0x00730051`–`0x00730090` | insert path B (เส้นที่ใช้จริงกับ store `+0x0C`) | `a0ced086fa1369016bdc54de8669435848b72c9995cb60a069fd3aa159b5373c` |
| `0x0072F450`–`0x0072F4E0` | map insert helper | `cdae8dabf3d329698fb50a2a6dad445ed96cae1155032b23897d11cf873a1f5e` |
| `0x0072F700`–`0x0072F8A0` | find helper (ตัวที่ใบเรียกว่า "loop") | `32f6f9ef374daee884195a176f9ef7f1ff264fdeccb346b978b70f8528bf1a9f` |
| `0x00891FD0`–`0x00892050` | `GetColumnByName` (int / float) | `59a93d72270b3f3602fd2313360e24aec043e2f812bfba2c8c8225a99691a8ee` |

สคริปต์ probe (read-only, เขียนใหม่รอบนี้): `staged/re270_disasm_probe.py`, `staged/re270_wstrings.py`

## ค้นก่อนถอด (บังคับกรอก)
- **`pf_bridge/external/`** — `grep -rilE '0072F700|0072FE50'` = **0 hit** (ยืนยันซ้ำสิ่งที่ LANE-A รายงานใน `0004`) · `grep -rilE 'SAILING'` เจอ 3 ไฟล์จริง (`PF_DATA_EVIDENCE.tsv` แถว `DATA-2063`, `PF_INPUT_INVENTORY.tsv` แถว 2064, `PF_MONSTER_PRESENTATION.md` บรรทัด 310) แต่**ทั้งสามเป็นเรื่องฉาก `SailingTest` ไม่ใช่คีย์ของ store** ⇒ ไม่มีคำตอบเดิมให้ verify+reuse
- **`gamedata/`** — มี `tables/CONSTDATA_TH__SAILING_RESULT.tsv`, `tables/TEXTDATA_TH__SAILING_TEXT.tsv`, `scene/SailingTest/SailingTest.placements.tsv` · ไม่มีไฟล์ใดระบุคีย์ของ store ฝั่ง client · หัวคอลัมน์ TSV เรียงเป็น `n_ID  n_AREA  n_EVENT  n_WEIGHT  n_LBOUND_LEVEL  n_UBOUND_LEVEL  n_VARI_1  n_VARI_2  n_VARI_3  s_OUTFIT  s_RANDOMEFFECT  n_QUEST_ID  n_ITEM_ID  n_ELITEMOBGROUP  n_CLINE_TYPE  s_HK_VER  s_TC_VER  s_JP_VER  s_TH_VER`
- ขอบเขตที่ค้น = สองโฟลเดอร์ข้างบนเท่านั้น (ไม่ได้ค้น `SERVER\` — ใบนี้ถามฝั่ง client)

## หลักฐาน (เดินได้เอง ไม่ต้องเชื่อคำสรุป)

### ① `0x0072FE50` คือ builder ของตารางนี้จริง
`0x0072FE8F push 0xf46e38` → wide string `W"SAILING_RESULT"` → `call 0x890ef0` (table-by-name) ⇒ `edi` = table object · ลูปนับจาก `(edi+0x68 − edi+0x64) >> 2` (vector ของ pointer) เรียก `0x88fa20(index)` ได้ row object ลง `esi`

คอลัมน์ที่ builder ดึงมาด้วย **ชื่อ** (ทุกตัวผ่าน `call 0x891fd0`, string เป็น UTF-16LE):
`0xF46E28 n_AREA` · `0xF46E18 n_EVENT` · `0xF3F470 n_WEIGHT` · `0xF46DF8 n_LBOUND_LEVEL` · `0xF46DD8 n_UBOUND_LEVEL` · `0xF46DC4 n_VARI_1` · `0xF46DB0 n_VARI_2` · `0xF46D9C n_VARI_3` · `0xF14FA8 s_OUTFIT` (ผ่าน `0x892050`) · `0xF46D7C n_ELITEMOBGROUP` · `0xF46D64 n_QUEST_ID` · `0xF46D50 n_ITEM_ID`
🔴 **`n_ID` ไม่เคยถูกดึงด้วยชื่อเลย** — นี่คือเบาะแสแรกว่ามันถูกอ่านทางลัด

### ② `[row+0x14]` = **pointer ไปยัง record buffer** ไม่ใช่ index (พิสูจน์จาก `GetColumnByName` เอง)
`0x00891FEA-0x00891FF0`:
```
mov edx, dword ptr [esi + 0x14]      ; esi = row (this)
mov ecx, dword ptr [eax + 0x34]      ; eax = column descriptor -> field byte offset
mov eax, dword ptr [ecx + edx]       ; *(record_base + field_offset)
```
⇒ `[row+0x14]` เป็น base ของ record, `[desc+0x34]` เป็น offset ของฟิลด์ในนั้น (คู่แฝด float ที่ `0x0089201A-0x00892020` ใช้สูตรเดียวกันเป๊ะ)

### ③ builder อ่านคีย์เป็น **ฟิลด์ที่ offset 0 ของ record เดียวกันนั้น**
`0x0072FF0F-0x0072FF15`:
```
mov eax, dword ptr [esi + 0x14]      ; record base ของ row นี้
mov ecx, dword ptr [eax]             ; *(record_base + 0)  = ฟิลด์แรก
push ebx
mov dword ptr [esp + 0x34], ecx      ; -> struct ที่ E+0x30 ช่องที่ 0
```
รวมกับ ② ⇒ ค่านี้คือ **คอลัมน์ที่ offset 0 ของ record = คอลัมน์แรกของตาราง = `n_ID`**
struct ค่าที่ประกอบขึ้น (E = esp ฐานของ loop body): `+0x00` = `n_ID` · `+0x04` = `n_AREA` (u16) · `+0x06` = `n_EVENT` (u16) · `+0x08` = `n_WEIGHT` (u16) · `+0x0A` = `n_LBOUND_LEVEL` (u16) · `+0x0C` = `n_UBOUND_LEVEL` (u16) · `+0x10` = `n_VARI_1` · `+0x14` = `n_VARI_2` · `+0x18` = `n_VARI_3`

### ④ ค่าที่ถูกใช้เป็น "คีย์" คือ dword ที่ `E+0x74` — และ path ที่ป้อน store `+0x0C` เขียน `n_ID` ลงไปตรง ๆ
เส้น B (`n_QUEST_ID <= 0`, `0x00730026 jle 0x730051`):
```
0x00730051  mov edx, dword ptr [esp + 0x30]   ; edx = n_ID (ช่องที่ 0 ของ struct)
0x00730055  lea eax, [esp + 0x30]
0x00730059  push eax
0x0073005A  mov dword ptr [esp + 0x78], edx   ; -> E+0x74  = ช่องคีย์
...
0x00730068  mov ecx, dword ptr [esp + 0x18]   ; = this
0x00730079  add ecx, 0xc                      ; -> map ที่ this+0x0C
0x0073007C  call 0x72f450                     ; insert
```
ใน `0x72f450`: `mov ebx, dword ptr [esp+0x18]` = อาร์กิวเมนต์ตัวแรกที่ push = `E+0x74` แล้ว `mov edx, dword ptr [ebx]` เทียบกับ `[eax+0xc]` ของ node ด้วย `cmp`/`setl` ⇒ **คีย์เป็น dword เดี่ยว เปรียบเทียบแบบ signed int32** ไม่ใช่ composite

**การตรวจสอบ esp ที่ทำให้เชื่อได้** (ไม่ใช่การนับคร่าว ๆ): prologue ผลัก `S-0x120` ⇒ `this` ถูกเก็บที่ `S-0x10C = E+0x14` ตรงกับ `mov ecx,[esp+0x18]` ตอน `esp=E-4` · และ `mov byte ptr [esp+0x120], 2` (`0x00730070`) ตกที่ `E+0x11C = S-4` ซึ่งคือช่อง SEH try-level ที่ `push -1` จองไว้พอดี ⇒ การไล่ esp ทั้งเส้นถูกต้อง (เส้น A ก็ลงล็อกเดียวกันที่ `mov byte ptr [esp+0x124], 1`)

### ⑤ มี store ที่สอง คีย์ **คนละคอลัมน์** — อย่าสับสน
เส้น A (`n_QUEST_ID > 0`, `0x00730028`): `mov dword ptr [esp+0x78], eax` โดย `eax = n_QUEST_ID` แล้ว `add ecx, 0x64` ⇒ **map ที่ `this+0x64` คีย์ด้วย `n_QUEST_ID`** และรับเฉพาะแถวที่ `n_QUEST_ID > 0`
`0x0072F700` (`lea esi,[ecx+0xc]`) = find ของ map `+0x0C` · `0x0072F770` (`lea esi,[ecx+0x2c]`) = find ของ map `+0x2C` (คนละ store อีกตัว) ⇒ **เส้นทางที่ `RE-265` วัดไว้ผ่าน `0x0072F700` คือ map `+0x0C` = คีย์ `n_ID`**

## คำแก้ข้อความในตัวใบ (ไม่กระทบคำตอบ)
ใบเขียนว่า "อ่าน key จาก **loop** ที่ `0x0072F700`" — `0x0072F700` **ไม่ใช่ลูปสร้าง store** มันคือ `find` helper ของ map `+0x0C` (คืน `[node+0x10]` เป็น mapped value) · ลูปสร้าง store อยู่ที่ `0x0072FE50`–`0x007300BC` ตามที่ใบเดาไว้ในช่วง `ATTENDED:` ("อ่าน `0x0072F700` ถึง `0x0072FE50`") ⇒ ช่วงที่ใบสั่งครอบคำตอบไว้ครบแล้ว แค่ป้ายชื่อสองจุดสลับกัน

## nonclaims (ของใบ + ที่เพิ่มจากรอบนี้)
1. ไม่ตัดสินว่า `GT-233` v3 ควรบูตหรือไม่ (ใบระบุเองว่าไม่รอใบนี้)
2. ไม่ตอบว่าหน้ารายงานกัปตันเปิดด้วยอะไร (เป็นของ `RE-265`/`GT-233`)
3. ไม่ขอให้แก้โค้ดเซิร์ฟเวอร์
4. 🔴 **ไม่อ้างว่า `n_ID` เป็น "ชื่อ" ที่ไบนารีรู้จัก** — ไบนารีอ่าน **offset 0 ของ record** ส่วนคำว่า `n_ID` มาจากหัวคอลัมน์แรกของ TSV export ที่ commit ไว้ · ถ้ามีวันไหนที่ export เรียงคอลัมน์ใหม่ ข้อสรุปนี้ต้องอ่านว่า "คอลัมน์แรกของ record" ไม่ใช่ชื่อ
5. ไม่ได้วัดว่า runtime lookup ที่ `RE-265` เห็น (record `+0x14`) ส่งค่าที่มาจากไหนของฝั่งเซิร์ฟเวอร์ — ใบนี้ตอบแค่ "ช่องรับของ store คือคอลัมน์ไหน"
6. ไม่ได้เปิดเกม ไม่ได้จับ `LOCK_GAME` ไม่ได้แตะ `state\pirateforce.sqlite3` ไม่มี commit/push
7. ไม่อ้างชั้น client-observable ใด ๆ

## BUILD_IMPACT
**ไม่มีการแก้โค้ดในรอบนี้** (ใบเป็นคำถาม static ล้วน) · ผลที่ LANE-A ใช้ได้ทันที: ถ้าจะ provision ให้ record `+0x14` ของ `NavigationEx_AddSurveyDataVtial` lookup ติด ต้องส่งค่าที่เป็น **`n_ID` ของแถว `SAILING_RESULT`** (1..138 ตามไฟล์ที่ commit) — ไม่ใช่ `n_AREA` (ค่า `126` ฯลฯ) · สมมติฐาน dock 154 = `n_AREA` ของ `COO-DECISION 20260905_2349` **ถูกหักล้างจากฝั่ง static แล้ว** แต่ `GT-233` v3 ยังเป็นชั้นที่ยืนยันบนจอ

## สถานะที่ขอให้ chief ปิด
`RE-270` → **CLOSED / BOUNDED-POSITIVE (static answered)** · checkpoint = **method ceiling ของชั้น static** (ตอบครบคำถามเดียวของใบแล้ว) ⇒ ห้าม rerun image เดิมกับคำถามนี้จนกว่า chief จะเปลี่ยน objective
