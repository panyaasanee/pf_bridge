[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: chief, COO | จาก: RE runner บนเครื่อง Panya | 2026-09-06T23:35+07:00]

# RE-283 RESULT (PARTIAL) — สามหน้า + widget 54 ตัวครบ + **ตารางบิตเลือกฟังก์ชัน** · เหลือจุดส่งจริงจุดเดียว

**สถานะ: PARTIAL — time checkpoint (ไม่ใช่ method ceiling)**
- ✅ ข้อ 1 (ชื่อสามหน้า) · ✅ ข้อ 2 (รายชื่อ widget ต่อหน้า) · ✅ ข้อ 4 (ช่องกรอกคู่กับฟังก์ชันไหน + ช่องในอ็อบเจ็กต์)
- 🟡 ข้อ 3 (เฟรมที่ส่ง) — ได้ **ตารางบิต "ปุ่มไหน = ค่าอะไรใน EDI"** ครบทุกปุ่มที่มีบิต และพิสูจน์ได้ว่าเป็นเส้นทาง **คำสั่งข้อความ** ไม่ใช่ opcode ต่อปุ่ม · ยังไม่ได้เดินถึงคำสั่งส่งจริง
- 🟡 ข้อ 5 (`n_LogType`) — ยังตอบไม่ได้ เพราะผูกกับข้อ 3

- START `2026-09-06T23:17:57+07:00` · เขียนผล `23:35` · static ล้วน ไม่เปิดเกม ไม่จับ `LOCK_GAME` · เป็นใบที่ 2 ของรอบที่ Panya สั่งให้ทำใบที่เหลือให้หมด

## input + SHA

| ไฟล์ | sha256 |
|---|---|
| `GameClient/Data/GUI/Model/GMUI.project` (148 B) | `392f17ba4aba1342ed1e0ec8133e1f2f074b94081fa1ee41bf718021746c0632` |
| `GameClient/Data/GUI/Model/GMUI_1.model` (25,434 B, XML UTF-8 BOM) | `ffd7e5d1c44ffe36b5bacc2857aa049ae6cbea69e11f62541bd0632162bbc69f` |
| `GameClient/GameClient.local.bin` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |

**ค้นใน `external/` แล้ว: ไม่เจอ** สารบัญ widget/หน้า/opcode ของ GMUI · **ค้น `gamedata/` แล้ว: ไม่เจอ** ตารางที่ผูก widget กับ opcode (มีแต่ `TEXTDATA_TH__GMTOOL` 97 ประเภท log ตามที่ใบระบุ)

---

## ✅ ข้อ 1 — ชื่อหน้าทั้งสาม

`GMUI.project` ประกาศ `<Model Name="GMUI_1"/>` ตัวเดียว · `GMUI_1.model` = `BigUIStandardWindow ID="GMUI_1" Size=(660,520)` `<Text>GMUI</Text>` มี `UITabControl` หนึ่งตัวบรรจุ `UITabPage` **สามหน้าพอดี**:

| # | Page ID | Name ในไฟล์ | TextID | ตัวชี้ในอ็อบเจ็กต์ |
|---|---|---|---|---|
| 1 | `GMUI_BASIC` | 基本功能 | 1439 | `this+0x14` |
| 2 | `GMUI_ADVAN` | 進階功能 | 1440 | `this+0x68` |
| 3 | `GMUI_ACTIVITY` | 活動功能 | 1891 | `this+0xb0` |

⇒ **แก้ข้อสันนิษฐานของใบ**: ไม่ใช่ "รู้ชื่อหน้าเดียว" — ทั้งสามชื่ออยู่ในไฟล์เดียวนี้ · ไม่มี `GMUI_BASIC.model` แยกเพราะมันเป็น `UITabPage` ไม่ใช่โมเดลของตัวเอง

ปุ่มยืนยันตัวเดียว อยู่นอกแท็บ: `UIButton ID="BUTTON_OK"` (執行鈕 "ทำงาน") TextID=1413 ตำแหน่ง (495,476) → เก็บที่ **`this+0xe8`**

## ✅ ข้อ 2 + ✅ ข้อ 4 — widget ครบ 54 ตัว + ช่องในอ็อบเจ็กต์ + **บิตเลือกฟังก์ชัน**

ที่มา: ฟังก์ชัน binder `0x00726DF0..0x00727A56` (lookup ทีละตัวด้วย `call 0x00AA1750(<ชื่อ resource>)` แล้วเก็บลง `[esi+off]`) · คอลัมน์ `EDI bit` มาจากบันได selector `0x007288B2..0x00728A66` ซึ่งอ่านสถานะติ๊ก (`cmp byte [widget+0x3DC], 0`) แล้วตั้งค่า `EDI`

### หน้า 1 `GMUI_BASIC` (page ptr `this+0x14`)
| widget | ชนิด | ป้าย | TextID | this+off | EDI bit |
|---|---|---|---|---|---|
| `Radiobutton_HIDE` | radio | 角色隱身 ซ่อนตัวละคร | 1386 | 0x18 | **0x1** |
| `Radiobutton_SCENE` | radio | 飛場景 วาร์ปฉาก | 1389 | 0x1c | **0x2** |
| `Radiobutton_NPC` | radio | 飛NPC | 1393 | 0x20 | **0x4** |
| `Radiobutton_PLAYER` | radio | 飛玩家 | 1394 | 0x24 | **0x8** |
| `Radiobutton_CALLPLAYER` | radio | 招喚玩家 | 1395 | 0x28 | **0x10** |
| `Radiobutton_Message` | radio | 即時訊息 | 1398 | 0x2c | **0x20** |
| `Radiobutton_KICK` | radio | 踢玩家 | 1397 | 0x30 | **0x100** |
| `Radiobutton_BOT` | radio | 提問BOT玩家 | 1396 | 0x34 | **0x1** 🔴 (ดูหมายเหตุ) |
| `Radiobutton_HIDE_1` / `Radiobutton_UNHIDE` | radio | 隱身 / 現身 | 1387 / 1388 | 0x58 / 0x54 | ไม่มีบิตของตัวเอง (เป็นตัวเลือกย่อยของ `HIDE`) |
| `TextBox_SCENE` | text | ช่องฉาก | — | 0x38 | — |
| `TextBox_BOT` | text | | — | 0x3c | — |
| `TextBox_KICK` | text | | — | 0x40 | — |
| `TextBox_CALLPLAYER` | text | | — | 0x44 | — |
| `TextBox_PLAYER` | text | | — | 0x48 | — |
| `TextBox_NPC` | text | | — | 0x4c | — |
| `TextBox_Message` | text | | — | 0x50 | — |
| `TextBox_X` / `TextBox_Y` / `TextBox_Z` | number | พิกัด | — | 0x5c / 0x60 / 0x64 | — |

🔴 **หมายเหตุที่ต้องรายงาน**: `Radiobutton_BOT` (`this+0x34`) ตั้ง `EDI = 0x1` **ซ้ำกับ `Radiobutton_HIDE`** (`0x007289DA` กับ `0x00728A3C`) · ลำดับตรวจทำให้ `HIDE` ชนะเสมอถ้าติ๊กพร้อมกัน — วัดได้จากไบต์ ไม่ตีความว่าเป็นบั๊กหรือเจตนา

### หน้า 2 `GMUI_ADVAN` (page ptr `this+0x68`)
| widget | ชนิด | ป้าย | TextID | this+off | EDI bit |
|---|---|---|---|---|---|
| `Radiobutton_Popmob` | radio | 產生怪 | 1399 | 0x6c | **0x40** |
| `Radiobutton_Killmob` | radio | 殺怪物 | 1400 | 0x70 | **0x80** |
| `Radiobutton_SilenceMap` | radio | 區域禁言 | 1401 | 0x74 | **0x200** |
| `Radiobutton_Cheatcode` | radio | 指令輸入 | 1412 | 0x78 | **0x400** |
| `Radiobutton_SilencePeople` | radio | 角色禁言 | 1407 | 0x7c | **0x800** |
| `Radiobutton_SilenceALL` / `SilenceMost` / `SilenceMapCancel` | radio | 全禁 / 部分玩家禁言 / 解除禁言 | 1402/1403/1404 | 0x90 / 0x94 / 0x98 | ตัวเลือกย่อยของ `SilenceMap` |
| `Radiobutton_SilenceONE` / `SilencePeopleCancel` | radio | 禁言 / 解除禁言 | 1408 / 1404 | 0xa0 / 0x9c | ตัวเลือกย่อยของ `SilencePeople` |
| `TextBox_Killmob` | text | | — | 0x80 | — |
| `TextBox_SilencePeople` | text | | — | 0x84 | — |
| `TextBox_Cheatcode` | text | | — | 0x88 | — |
| `TextBox_Reason` | text | เหตุผล | — | 0x8c | — |
| `TextBox_Popmob` | text | | — | 0xa4 | — |
| `TextBox_MTime` / `TextBox_PTime` | number | เวลา (มอน / ผู้เล่น) | — | 0xa8 / 0xac | — |

### หน้า 3 `GMUI_ACTIVITY` (page ptr `this+0xb0`)
| widget | ชนิด | ป้าย | TextID | this+off | EDI bit |
|---|---|---|---|---|---|
| `Radiobutton_Drop` | radio | 產生寶 | 1892 | 0xb4 | **0x1000** |
| `Radiobutton_SceneBuff` | radio | 場景Buff | 1894 | 0xb8 | **0x2000** |
| `Radiobutton_PVPFaction` | radio | 玩家陣營 | 1671 | 0xbc | **0x4000** |
| `Radiobutton_FreeChat` | radio | 自由聊天 | 1895 | 0xc0 | **0x8000** |
| `Radiobutton_Salvaging` | radio | 打撈活動 | 1896 | 0xc4 | **0x10000** |
| `Radiobutton_FreeChat_On` / `_Off` | radio | 開啟 / 關閉 | 46 / 1177 | 0xd8 / 0xdc | ตัวเลือกย่อยของ `FreeChat` |
| `TextBox_Drop` | number | | — | 0xc8 | — |
| `TextBox_SceneBuff` | number | | — | 0xcc | — |
| `TextBox_PVPFaction` | number | | — | 0xd0 | — |
| `TextBox_Salvaging` | number | | — | 0xd4 | — |
| `TextBox_DropRange` | number | ระยะดรอป | — | 0xe0 | — |
| `TextBox_SalvagingNum` | number | จำนวนที่งม | — | 0xe4 | — |

**วิธีตรวจซ้ำ (ทำเองได้ทุกแถว):** ที่ bind site ตัว store คือ `mov [esi+off], eax` ที่อยู่ **หลัง** push ชื่อของตัวถัดไป (ผลของ lookup ก่อนหน้า) · จุดที่เคยทำให้ลำดับเพี้ยนคือ `BUTTON_OK` (`push 0x00F19E38` ที่ `0x007276BF`) ซึ่งแทรกอยู่กลางกลุ่ม `GMUI_ACTIVITY` — ตารางข้างบนนับมันแล้ว และผลลัพธ์ **ตรงกับบันได selector ทุกแถว** (ตัวตรวจอิสระ)

## 🟡 ข้อ 3 — เท่าที่พิสูจน์ได้

1. คลาสหน้าต่าง = **`GeneralUIHandleModule`** (สตริง ASCII `0x00F45A04`) · vtable `0x00F46208` (ctor `0x00727A60`)
2. ตอนกดปุ่ม: ตัว dispatcher ที่ `0x00728200..0x00729600` **เลือกหน้าที่มองเห็นก่อน** (`vfunc +0xF0` บน page ptr: `0x007288B2` = ADVAN · `0x00728935` = ACTIVITY · fallthrough = BASIC) แล้ว **ไล่บันไดตรวจ `[widget+0x3DC] != 0`** (สถานะติ๊ก) เพื่อตั้ง `EDI` เป็นบิตตามตารางข้างบน
3. จากนั้นแยกงานตาม `EDI` — พบ `cmp edi, imm` ที่ `0x00728A91 (0x10)`, `0x00728CE9 (0x800)`, `0x00728CFB (0x100)`, `0x00728E42 (0x200)`, `0x00728E4E (0x400)`, `0x007290FB (0x4000)`, `0x0072910D (0x1000)`, `0x00729115 (0x2000)`, `0x00729267 (0x8000)`, `0x00729273 (0x10000)`
4. **หลักฐานชี้ทางที่สำคัญที่สุด**: สาขา `EDI = 0x400` (`Radiobutton_Cheatcode`) อ่านข้อความจาก `TextBox_Cheatcode` (`this+0x88`, vfunc `+0x124`) แล้ว **บังคับว่าอักษรแรกต้องเป็น `/`** (`cmp word ptr [eax], 0x2f` ที่ `0x00728EA5` และซ้ำที่ `0x00728EBA`) ตัด `/` ทิ้ง แล้วต่อสตริงลงบัฟเฟอร์ `[ebx+0x1c]` (`0x00728EE1`/`0x00728EEC`) · ตัวเลขไปที่ `[ebx+0x14]` (`0x00728C1B`) · แฟล็กไปที่ `[ebx+0x18]` (`0x00728F3A`/`0x00728F52`)
   ⇒ **GMUI ไม่มี opcode ต่อปุ่ม — ทุกปุ่มประกอบ "คำสั่งข้อความ + ตัวเลข + แฟล็ก" ลงอ็อบเจ็กต์เดียว** ซึ่งเข้ากันได้กับ `RE-091` (แชทเป็น producer ของ `GM_RunGMCommandVital` `0x51E9`)
5. **ยังไม่พิสูจน์**: ยังไม่ได้เดินจากอ็อบเจ็กต์ `EBX` ไปถึงคำสั่งส่ง ⇒ **ยังไม่ยืนยันว่า `0x51E9`** · สตริง `GM_RunGMCommandVital` (`0x00F463A4`) ถูกอ้างจุดเดียวที่ `0x00C07EA1` ซึ่งเป็น**ตารางลงทะเบียนคลาส** ไม่ใช่จุดเรียกของ GMUI

## 🟡 ข้อ 5 — `TEXTDATA_TH__GMTOOL` (97 `n_LogType`)

ยังตอบไม่ได้ เพราะการผูกต้องอ่านจากเฟรมที่ส่งจริง (ข้อ 3 ยังไม่ปิด) · **ไม่จับคู่ด้วยความหมายของข้อความ** ตามที่ใบสั่งห้าม

## รอบหน้าเริ่มตรงนี้ (ไม่ต้องทำซ้ำ)

1. ตาม `EBX` (อ็อบเจ็กต์ปลายทาง: `[ebx+0x14]` เลข · `[ebx+0x18]` แฟล็ก · `[ebx+0x1c]` สตริง) — มันถูกสร้างที่ `0x0072888D` (`call 0x007286E0` บนอ็อบเจ็กต์ global `0x0102E378`) ⇒ เปิด `0x007286E0` และคลาสของ `0x0102E378` จะได้จุดส่ง
2. เมื่อได้จุดส่งแล้ว ข้อ 5 ตอบได้ทันทีถ้าเฟรมพก log type ไปด้วย
3. ตารางข้อ 1/2/4 ข้างบน **ถือว่าปิดแล้ว** ไม่ต้องถอดซ้ำ

## nonclaims

1. ไม่อ้างว่า GMUI ส่ง `0x51E9` — ข้อ 3 ยังเป็นการอนุมานจากรูปแบบ `/` + `RE-091`
2. ไม่อ้างว่าปุ่มที่ไม่มี EDI bit "ไม่ส่งอะไร" — มันเป็นตัวเลือกย่อยที่น่าจะถูกอ่านในสาขาของปุ่มแม่ (ยังไม่ได้ไล่ทุกสาขา)
3. ไม่อ้างว่า `EDI` bit = ฟิลด์บนสาย — มันเป็นตัวเลือกภายในของ dispatcher เท่านั้น
4. TextID ยังไม่ resolve เป็นข้อความไทยจาก `TEXTDATA` (ไม่ได้อยู่ในคำถาม)
5. ไม่ได้แตะ/แก้ไฟล์ใด ๆ ใน `GameClient/`, `external/`, `gamedata/`, `SERVER/` หรือไฟล์คิว

## BUILD_IMPACT

- `gmui_catalog.py` เติมได้แล้ว **ทั้งสามหน้า + 54 widget + member offset + EDI bit** พร้อม provenance (ไฟล์+sha, bind site VA, ladder VA) — คอลัมน์ opcode ยังเว้นไว้จนกว่าปิดข้อ 3
- ใบ GT ต่อปุ่มตาม `COO-DECISION 20260904_0245` **เปิดได้เลย** เพราะรู้จำนวน ชื่อ และหน้าที่อยู่ครบแล้ว
