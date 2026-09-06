[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: chief, COO | จาก: RE runner บนเครื่อง Panya | 2026-09-06T23:28+07:00]

# RE-283 RESULT (PARTIAL) — สามหน้าคือ `GMUI_BASIC` / `GMUI_ADVAN` / `GMUI_ACTIVITY` · widget 53 ตัวถอดครบ · เส้นทางกดปุ่มพินได้ครึ่งทาง

**สถานะ: PARTIAL — time checkpoint (ไม่ใช่ method ceiling)** · ข้อ 1, 2, 4 **ตอบครบ** · ข้อ 3, 5 **ตอบได้บางส่วน** พร้อมจุดเริ่มที่แน่นอนให้รอบหน้าเดินต่อ (ไม่ต้องเริ่มใหม่)

- START `2026-09-06T23:17:57+07:00` · เขียนผล `23:28` · static ล้วน ไม่เปิดเกม ไม่จับ `LOCK_GAME`
- รอบนี้ Panya สั่งให้ทำใบที่เหลือให้หมดโดยไม่จำกัดจำนวนใบ ⇒ ใบนี้เป็นใบที่ 2 ของรอบ

## input + SHA

| ไฟล์ | sha256 |
|---|---|
| `GameClient/Data/GUI/Model/GMUI.project` (148 B) | `392f17ba4aba1342ed1e0ec8133e1f2f074b94081fa1ee41bf718021746c0632` |
| `GameClient/Data/GUI/Model/GMUI_1.model` (25,434 B, XML UTF-8 BOM) | `ffd7e5d1c44ffe36b5bacc2857aa049ae6cbea69e11f62541bd0632162bbc69f` |
| `GameClient/GameClient.local.bin` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |

**ค้นใน `external/` แล้ว: ไม่เจอ** สารบัญ widget/หน้า/opcode ของ GMUI (ยืนยันซ้ำสิ่งที่ใบเขียน) · **ค้น `gamedata/` แล้ว: ไม่เจอ** ตารางที่ผูก widget กับ opcode (มีแต่ `TEXTDATA_TH__GMTOOL` 97 ประเภท log ตามที่ใบระบุ)

---

## ✅ ข้อ 1 — ชื่อหน้าทั้งสาม (จาก shipped data โดยตรง)

`GMUI.project` ประกาศ `<Model Name="GMUI_1"/>` ตัวเดียว · `GMUI_1.model` = `BigUIStandardWindow ID="GMUI_1" Size=(660,520)` `<Text>GMUI</Text>` ภายในมี `UITabControl` หนึ่งตัว บรรจุ **`UITabPage` สามหน้าพอดี**:

| # | Page ID | `Name` (ในไฟล์) | `TextID` | Size |
|---|---|---|---|---|
| 1 | `GMUI_BASIC` | 基本功能 (ฟังก์ชันพื้นฐาน) | 1439 | (620, 358) |
| 2 | `GMUI_ADVAN` | 進階功能 (ฟังก์ชันขั้นสูง) | 1440 | (620, 358) |
| 3 | `GMUI_ACTIVITY` | 活動功能 (ฟังก์ชันกิจกรรม) | 1891 | (620, 358) |

⇒ **แก้ข้อสันนิษฐานของใบ**: ไม่ใช่ "รู้ชื่อหน้าเดียวจากสามหน้า" — ชื่อครบสามหน้าอยู่ในไฟล์เดียวกันนี้ทั้งหมด และ **ไม่มี** `GMUI_BASIC.model` แยกเพราะมันเป็น `UITabPage` ในไฟล์แม่ ไม่ใช่ไฟล์โมเดลของตัวเอง

ปุ่มยืนยันมีตัวเดียว อยู่นอกแท็บ (ระดับหน้าต่าง): `UIButton ID="BUTTON_OK"` Name=執行鈕 (ปุ่ม "ทำงาน") TextID=1413 ตำแหน่ง (495,476)

## ✅ ข้อ 2 + ข้อ 4 — widget ที่กดได้/กรอกได้ ครบทั้งสามหน้า พร้อม member offset ในคลาส

รวม **53 widget + 1 ปุ่ม OK** · ชนิดที่ใช้จริง: `UIRadioButton` 27 · `UITextBox` 13 · `UINumberInput` 11 · `UIButton` 1 (นอกจากนี้เป็น `UIPanel`/`UILabel`/`UIGrid9` ที่กดไม่ได้)

คอลัมน์ `this+off` คือช่องในอ็อบเจ็กต์ที่ตัว binder เก็บพอยน์เตอร์ widget ไว้ — **ถอดจากฟังก์ชัน binder `0x00726DF0..0x00727A56`** (ทุกแถวมี bind site จริง ไม่ได้เดา):

### หน้า 1 `GMUI_BASIC` (this+0x14 = ตัวหน้าเอง)
| widget | ชนิด | ป้าย | TextID | this+off |
|---|---|---|---|---|
| `Radiobutton_HIDE` | radio | 角色隱身 (ซ่อนตัวละคร) | 1386 | 0x18 |
| `Radiobutton_HIDE_1` | radio | 隱身 (ซ่อน) | 1387 | 0x58 |
| `Radiobutton_UNHIDE` | radio | 現身 (ปรากฏ) | 1388 | 0x54 |
| `Radiobutton_SCENE` | radio | 飛場景 (วาร์ปฉาก) | 1389 | 0x1c |
| `Radiobutton_NPC` | radio | 飛NPC | 1393 | 0x20 |
| `Radiobutton_PLAYER` | radio | 飛玩家 (วาร์ปหาผู้เล่น) | 1394 | 0x24 |
| `Radiobutton_CALLPLAYER` | radio | 招喚玩家 (เรียกผู้เล่น) | 1395 | 0x28 |
| `Radiobutton_BOT` | radio | 提問BOT玩家 | 1396 | 0x34 |
| `Radiobutton_KICK` | radio | 踢玩家 (เตะผู้เล่น) | 1397 | 0x30 |
| `Radiobutton_Message` | radio | 即時訊息 (ข้อความทันที) | 1398 | 0x2c |
| `TextBox_SCENE` | text | ช่องกรอกฉาก | — | 0x38 |
| `TextBox_BOT` | text | ช่องกรอก BOT | — | 0x3c |
| `TextBox_KICK` | text | ช่องกรอกชื่อที่จะเตะ | — | 0x40 |
| `TextBox_CALLPLAYER` | text | ช่องกรอก | — | 0x44 |
| `TextBox_PLAYER` | text | ช่องกรอก | — | 0x48 |
| `TextBox_NPC` | text | ช่องกรอก | — | 0x4c |
| `TextBox_Message` | text | ช่องกรอก | — | 0x50 |
| `TextBox_X` / `TextBox_Y` / `TextBox_Z` | number | พิกัด | — | 0x5c / 0x60 / 0x64 |

### หน้า 2 `GMUI_ADVAN` (this+0x68 = ตัวหน้าเอง)
| widget | ชนิด | ป้าย | TextID | this+off |
|---|---|---|---|---|
| `Radiobutton_Popmob` | radio | 產生怪 (เกิดมอน) | 1399 | 0x6c |
| `Radiobutton_Killmob` | radio | 殺怪物 (ฆ่ามอน) | 1400 | 0x70 |
| `Radiobutton_SilenceMap` | radio | 區域禁言 (แบนแชทพื้นที่) | 1401 | 0x74 |
| `Radiobutton_SilenceALL` | radio | 全禁 | 1402 | 0x90 |
| `Radiobutton_SilenceMost` | radio | 部分玩家禁言 | 1403 | 0x94 |
| `Radiobutton_SilenceMapCancel` | radio | 解除禁言 | 1404 | 0x98 |
| `Radiobutton_SilencePeople` | radio | 角色禁言 | 1407 | 0x7c |
| `Radiobutton_SilenceONE` | radio | 禁言 | 1408 | 0xa0 |
| `Radiobutton_SilencePeopleCancel` | radio | 解除禁言 | 1404 | 0x9c |
| `Radiobutton_Cheatcode` | radio | 指令輸入 (ป้อนคำสั่ง) | 1412 | 0x78 |
| `TextBox_Killmob` | text | — | — | 0x80 |
| `TextBox_SilencePeople` | text | — | — | 0x84 |
| `TextBox_Cheatcode` | text | — | — | 0x88 |
| `TextBox_Reason` | text | เหตุผล | — | 0x8c |
| `TextBox_Popmob` | text | — | — | 0xa4 |
| `TextBox_MTime` / `TextBox_PTime` | number | เวลา (มอน/ผู้เล่น) | — | 0xa8 / 0xac |

### หน้า 3 `GMUI_ACTIVITY` (this+0xe8 = ตัวหน้าเอง · ดู nonclaim 3)
| widget | ชนิด | ป้าย | TextID | this+off |
|---|---|---|---|---|
| `Radiobutton_Drop` | radio | 產生寶 (ดรอปของ) | 1892 | 0xb0 |
| `Radiobutton_SceneBuff` | radio | 場景Buff | 1894 | 0xb4 |
| `Radiobutton_PVPFaction` | radio | 玩家陣營 (ฝ่ายผู้เล่น) | 1671 | 0xb8 |
| `Radiobutton_FreeChat` | radio | 自由聊天 | 1895 | 0xbc |
| `Radiobutton_FreeChat_On` / `_Off` | radio | 開啟 / 關閉 | 46 / 1177 | 0xd4 / 0xd8 |
| `Radiobutton_Salvaging` | radio | 打撈活動 (กิจกรรมงมของ) | 1896 | 0xc0 |
| `TextBox_Drop` | number | — | — | 0xc4 |
| `TextBox_DropRange` | number | ระยะดรอป | — | 0xdc |
| `TextBox_SceneBuff` | number | — | — | 0xc8 |
| `TextBox_PVPFaction` | number | — | — | 0xcc |
| `TextBox_Salvaging` | number | — | — | 0xd0 |
| `TextBox_SalvagingNum` | number | จำนวนที่งม | — | 0xe0 |

**ข้อ 4 (ค่าที่ต้องกรอกไปอยู่ไหน)** — ตอบได้ระดับ "ช่องไหนคู่กับฟังก์ชันไหน" จากชื่อ resource + ตำแหน่งบนหน้าจอ (คู่กันตรง ๆ เช่น `Radiobutton_Killmob` ↔ `TextBox_Killmob`) · **ยังไม่ได้ตอบว่าไปอยู่ฟิลด์ไหนของเฟรม** เพราะยังไม่ปิดข้อ 3 (ดูด้านล่าง)

## 🟡 ข้อ 3 — วัดได้ถึงตรงนี้ (ยังไม่ปิด)

1. **คลาสของหน้าต่างนี้ชื่อ `GeneralUIHandleModule`** (สตริง ASCII `0x00F45A04`) · vtable ของอ็อบเจ็กต์ = `0x00F46208` (ctor `0x00727A60` เขียนค่านี้ลง `[eax]`)
2. **binder** `0x00726DF0..0x00727A56` ผูก widget ทั้ง 53 ตัว (+3 หน้า) เข้าช่อง `this+0x14..this+0xe8` ตามตารางข้างบน — ทุกตัว lookup ด้วย `call 0x00AA1750(<ชื่อ resource>)`
3. **เส้นทางตอนกด** อยู่ที่ `0x00728200..0x00729600` — เป็น dispatcher ที่เลือกด้วย **บิตมาสก์ใน `EDI`** (พบ `cmp edi, 0x200` / `cmp edi, 0x400` ที่ `0x00728E42`/`0x00728E4E`) แล้วแตกไปทำงานต่อฟังก์ชัน
4. **หลักฐานชิ้นสำคัญ:** สาขาของ `TextBox_Cheatcode` (`this+0x88`) อ่านข้อความออกมาด้วย vfunc `+0x124` แล้ว **บังคับว่าตัวอักษรแรกต้องเป็น `/` (`cmp word ptr [eax], 0x2f` ที่ `0x00728EA5` และซ้ำอีกครั้งที่ `0x00728EBA`)** จากนั้นตัด `/` ทิ้งแล้วต่อสตริงลงบัฟเฟอร์ที่ `[ebx+0x1c]` (`0x00728EE1`, `0x00728EEC`)
   ⇒ **GMUI ไม่ได้มี opcode ต่อปุ่ม — มันประกอบ "คำสั่งข้อความ" แล้วส่งผ่านทางเดียวกับช่องแชท** ซึ่งตรงกับที่ `RE-091` พิสูจน์ไว้ว่าแชทเป็น producer ของ `GM_RunGMCommandVital` (`0x51E9`)
5. **สิ่งที่ยังไม่ได้พิสูจน์:** ยังไม่ได้เดินจากบัฟเฟอร์ `[ebx+0x1c]` ไปถึงจุดส่งจริง จึง **ยังไม่ยืนยัน** ว่าเป็น `0x51E9` สำหรับ GMUI (ตอนนี้เป็นการอนุมานจากรูปแบบ `/` + ผล `RE-091` เท่านั้น) · สตริง `GM_RunGMCommandVital` (`0x00F463A4`) ถูกอ้างจุดเดียวคือ `0x00C07EA1` ซึ่งเป็น **ตารางลงทะเบียนคลาส** ไม่ใช่จุดเรียกของ GMUI

## 🟡 ข้อ 5 — `TEXTDATA_TH__GMTOOL` (97 `n_LogType`)

**ยังตอบไม่ได้ และนี่คือเหตุผล**: การผูกต้องมาจากเส้นทางส่งจริง (ข้อ 3 ข้อ 5 ของใบเอง) ซึ่งยังเดินไม่ถึง · **ไม่จับคู่ด้วยความหมายของข้อความ** ตามที่ใบสั่งห้าม ⇒ เว้นเป็น "ตอบไม่ได้ เพราะยังไม่ปิดข้อ 3" ไม่ใช่เว้นว่าง

## รอบหน้าเริ่มตรงนี้ (checkpoint — ไม่ต้องทำซ้ำที่ทำไปแล้ว)

1. หา prologue จริงของฟังก์ชัน dispatcher ที่ครอบ `0x00728C24`/`0x00728E5A` (การไล่ padding `CC` ย้อนกลับไม่ได้ผลเพราะฟังก์ชันยาวมาก — ใช้ xref จาก vtable `0x00F46208` แทน)
2. ตามตัวแปร `EBX` (อ็อบเจ็กต์ที่ถูกเติม: `[ebx+0x14]` ตัวเลข · `[ebx+0x18]` แฟล็ก · `[ebx+0x1c]` สตริง) ว่าถูกส่งต่อให้ใคร ⇒ นั่นคือจุดที่จะบอก vital id จริง
3. ถอดบิตมาสก์ `EDI` ทั้งชุด (`cmp edi, imm` ทุกจุดในช่วง `0x00728200..0x00729600`) ⇒ ได้ตาราง "ปุ่มไหน = บิตไหน" ครบ ซึ่งจะเติมข้อ 3/4/5 ได้ทั้งหมดในรอบเดียว

## nonclaims

1. ไม่อ้างว่า GMUI ส่ง `0x51E9` — ข้อ 3 ยังเป็น**การอนุมาน**จากรูปแบบ `/` + `RE-091` ยังไม่ใช่การเดินโค้ดถึงจุดส่ง
2. ไม่อ้างว่า 53 widget ทั้งหมด "กดแล้วมีผลบนสาย" — บางตัวอาจเป็นแค่ตัวเลือกในหน้า (`Radiobutton_SilenceALL/Most` ดูเหมือนตัวเลือกย่อยของ `SilenceMap`)
3. `GMUI_ACTIVITY -> this+0xe8` มาจากลำดับ store ในตัว binder ซึ่งของหน้านี้ถูกเก็บนอกลำดับ (widget ของมันอยู่ `0xb0..0xe0`) — **ค่านี้ยังไม่ได้ยืนยันด้วยการอ่านทีละคำสั่งเหมือนแถวอื่น** ให้ถือเป็น [ต้องตรวจซ้ำ] หนึ่งแถว
4. TextID ที่ยกมาเป็นเลขในไฟล์ `.model` ยังไม่ได้ resolve เป็นข้อความไทยจาก `TEXTDATA` (ไม่ได้อยู่ในคำถามของใบ)
5. ไม่ได้แตะ/แก้ไฟล์ใด ๆ ใน `GameClient/`, `external/`, `gamedata/`, `SERVER/` หรือไฟล์คิว

## BUILD_IMPACT

- `gmui_catalog.py` เติมได้แล้วสองส่วน: **ชื่อหน้าสามหน้า** และ **ตารางปุ่ม 53 แถว** (ที่ตอนนี้ว่างโดยเจตนา) พร้อม provenance = ไฟล์ + sha + bind site VA · คอลัมน์ opcode ยังต้องเว้นไว้จนกว่ารอบหน้าปิดข้อ 3
- ใบ GT ต่อปุ่มตาม `COO-DECISION 20260904_0245` **เปิดได้แล้วโดยไม่ต้องรอข้อ 3** เพราะรู้จำนวนและชื่อปุ่มครบแล้ว
