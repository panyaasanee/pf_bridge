[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-060 RESULT — PINNED 5 OBSERVED ITEM TABLE CODES

เวลา: 2026-08-24T14:14:58+07:00 ถึง 2026-08-24T14:22:57+07:00  
ชนิดงาน: STATIC-ON-BRIDGE ล้วน · ไม่บูต server/client · ไม่จับ `LOCK_GAME` · ไม่แตะ DB

## คำตอบ objective หนึ่งประโยค

**pin ได้ — `22=EQUIPMENT_BASE`, `24=ITEM_CONSUMABLES`, `25=ITEM_QUEST`, `26=ITEM_MISC`, `35=ITEM_ITEMMALL` (หลักฐานชนิด ค: แต่ละ code มี candidate 100%-hit เพียงหนึ่งตารางจาก 120 ตาราง `CONSTDATA_TH` ที่มี `n_ID`; อิมเมจชนิด ก ยืนยันตัวถอด `full_id / 100000 -> runtime table map` และ `full_id % 100000 -> n_ID` แต่ map contents ถูกโหลดเข้า tree ตอน runtime จึงไม่ใช้ image เพียงลำพังตั้งชื่อตาราง)**

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว:** เจอ `PF_DATA_EVIDENCE.tsv` คำว่า Item เพียง 3 แถว avatar-offset, `PF_PROTOCOL_REGISTRY.tsv` 56 แถวชื่อมี Item และ `PF_RUNTIME_CLASSMAP.tsv` 40 แถวชื่อมี Item (ส่วนมากเป็น UIAutomation RTTI/UNKNOWN); ไม่เจอ `table_code`, `ITEM_MISC`, `ITEM_CONSUMABLES`, `ITEM_QUEST`, `ITEM_ITEMMALL`, `EQUIPMENT_BASE` หรือ crosswalk `code->table` ในชุดส่งมอบ
- **ค้น gamedata แล้ว:** เจอ 120 `CONSTDATA_TH` tables ที่มีคอลัมน์ `n_ID`, item-reference corpus 7,210 occurrences / 2,263 full IDs ไม่ซ้ำจาก 37,499 cells, crosswalk `PF_GAMEDATA_INDEX.flags: ITEM_MISC -> ITEM_MISC_TIP`, plaintext `TEXTDATA_TH__ITEM_MISC_TIP` 1,922 แถว และ decoded Lua 616 ไฟล์; รายละเอียดจ็อบด้านล่าง

## จ็อบ 1 — falsifiable matrix

### ขอบเขตคอลัมน์

| source table | rows | item columns | cells | 7-digit refs |
|---|---:|---:|---:|---:|
| STORE_NORMAL | 15 | `n_ID_ITEM1..20` (20) | 300 | 134 |
| STORE_GOODS | 164 | `n_ID_ITEM`, `n_ID_GOOD1..4` (5) | 820 | 390 |
| DROPS_NORMAL | 267 | `n_ITEM_1..30` | 8,010 | 1,165 |
| DROPS_QUEST | 311 | `n_ITEM_1..20` | 6,220 | 448 |
| DROPS_SPECIALLY | 584 | `n_ITEM_1..30` | 17,520 | 3,913 |
| DROPS_EQUIPMENT | 53 | `n_ITEM_1..20` | 1,060 | 589 |
| COMBINE | 47 | `n_OUTCOME`, `n_MATERIAL_1..5` | 282 | 161 |
| DECOMPOSITION | 48 | ไม่มี direct item column (`n_DROPSGROUP` ไม่ถูกนับเป็น item id) | 0 | 0 |
| DAILY_REWARD | 78 | `n_ITEM_1..30` | 2,340 | 410 |
| ITEM_USING | 947 | `n_ID` | 947 | 0 |
| **รวม** |  |  | **37,499** | **7,210** |

การนับ STORE_GOODS อย่างเดียว reproduce pin เดิมในหัวใบพอดี: `26 x261` (`n_ID_ITEM` 34 + `n_ID_GOOD1` 163 + `n_ID_GOOD2` 64), `24 x115`, `22 x10`, `35 x4`; การขยายไปตารางอ้างไอเทมอื่นพบ code `25` เพิ่มด้วย จึงไม่สรุปว่าทั้งเกมมีแค่สี่ code

### ผลแยก code / remainder

| code | occurrences | unique remainder | min..max | 100%-hit table | 100%-hit candidates |
|---:|---:|---:|---|---|---:|
| 22 | 1,234 | 424 | 9..9,246 | `EQUIPMENT_BASE` | **1** |
| 24 | 2,870 | 1,011 | 7..80,051 | `ITEM_CONSUMABLES` | **1** |
| 25 | 460 | 395 | 2..3,009 | `ITEM_QUEST` | **1** |
| 26 | 2,333 | 373 | 1..5,613 | `ITEM_MISC` | **1** |
| 35 | 313 | 60 | 7..20,018 | `ITEM_ITEMMALL` | **1** |

เมทริกซ์เต็ม **120 rows x 5 codes** (รวมทุก partial/zero rate และจำนวน `n_ID` ต่อ candidate) อยู่ที่:

- `pf_bridge/staged/re060_code_matrix_output.txt` — 31,929 bytes — sha256 `d3f30ca4cf9250ca850f3fb283747492bfe0432cc8a107c782778af4fe49bea2`
- generator ASCII-only: `pf_bridge/staged/re060_code_matrix.py` — sha256 `fa08e6819b83cbe115f55eb2993a2239538b9bf583acea1406c8cfe57e07eefe`

คำทำนาย `26->ITEM_MISC` และ `24->ITEM_CONSUMABLES` **ผ่าน** แต่ยกระดับด้วยกำลังแยกแยะ (candidate 100% = 1) ไม่ใช่เชื่อคอมเมนต์ v141

## จ็อบ 2 — client decoder

พบตัวถอดจริง; ร่องรอยในใบระบุ magic คนละชุดกับ binary นี้:

- raw whole-image census: literal LE `100000` = 61 occurrences; hint magic `A7C5AC47` = 0, `D1B71759` = 0; magic ที่ binary ใช้จริง `0x14F8B589` = 38 occurrences
- `0x00892530` รับ full ID: ถ้า `>100000` ใช้ `imul 0x14F8B589; sar edx,13; sign adjust` ได้ quotient แล้วส่ง quotient เข้า `0x00890FC0`; node ที่ได้มี linked table name ที่ `+0x34`, จากนั้น `0x00890EF0` resolve table object ด้วยชื่อนั้น
- `0x0046B3E0` คำนวณ remainder โดย quotient เดียวกัน, คูณกลับ `100000`, แล้วลบจาก input
- `0x00892580` ทำทั้ง quotient -> table lookup และ remainder -> row lookup (`0x00890E70`) ในฟังก์ชันเดียว
- `0x005AD5B0` เป็น client item-name path ที่ call `0x00892530(full_id)`, call `0x0046B3E0(full_id)`, แล้ว query field literal `s_NAME`
- `0x005AEC30` ทำเส้นเดียวกันแล้ว query `s_COMMON`, `s_USED`, `s_EQUIPED`
- ไม่มี switch hardcoded 0x16/0x18/0x19/0x1A/0x23 ใน decoder: `0x00890FC0` เป็น tree lookup; contents ของ tree ไม่ได้ฝังเป็น static switch จึงใช้ matrix/linked-table data pin ชื่อแทน

### cited spans (recursive CFG)

| role | VA span | file offset | len | sha256 | decode errors |
|---|---|---:|---:|---|---:|
| remainder `%100000` | `[0x0046B3E0,0x0046B40F)` | `0x0006A7E0` | 47 | `b04eab9663994fc76a94c88e56835a0ddef333580c48083332f7db92fc3d3901` | 0 |
| code -> linked table | `[0x00892530,0x0089257B)` | `0x00491930` | 75 | `57f71f14fc7f630f614bfcb0ef2c1d1170c52368379fe6f797e9eee260043e7c` | 0 |
| code-tree lookup | `[0x00890FC0,0x00891026)` | `0x004903C0` | 102 | `9b11d687e5d0ed8030f58e3f9678f9bf82da49fad374f93af6b6a052fe3bbaa3` | 0 |
| code + remainder -> row | `[0x00892580,0x00892606)` | `0x00491980` | 134 | `1ce8aa30afadc034fcfabadcf2ab67c6bf828fad0e30bf48af68283901c368e7` | 0 |
| item `s_NAME` resolver path | `[0x005AD5B0,0x005ADB06)` | `0x001AC9B0` | 1,366 | `bd19324628a467003e5c106c73f43608f4df2d147a7a0d1677f39feeca5cd773` | 0 |
| item text-field resolver | `[0x005AEC30,0x005AEDED)` | `0x001AE030` | 445 | `811cd64dd786caaaf7932518d7ade59a57a605f0474632b73a30c3ab78701aa5` | 0 |

ไม่มี linear-disassembler negative claim; negative จำกัดอยู่ที่ exact whole-image byte census ของ magic hints และ recursive CFG ของ cited functions

## จ็อบ 3 — ข้อจำกัด packed เก่าหมดอายุบางส่วน

### (ก) `B_TEXTDATA_TH.pc_`

ข้ออ้างว่า text table ปิดเพราะ packed **หมดอายุแล้ว**: `TEXTDATA_TH` ถูกแตกเป็น plaintext 65 ตาราง; `TEXTDATA_TH__ITEM_MISC_TIP.tsv` มี 1,922 แถวและอ่าน `s_NAME`/description ได้ตรง

### (ข) UI Lua

ข้ออ้างว่า `.lu_` ปิดเพราะ packed **หมดอายุแล้วเช่นกันในเชิง compression**: corpus แตกสำเร็จ 616/616 ไฟล์ (root 310 เป็น trigger scripts ชื่อ `t_*`; `Quest/` 306 เป็น quest scripts) แต่ corpusนี้ **ไม่ใช่ UI controller/caption corpus**; exact recursive search `Common_NumInput|Common_NumberInput|caption|split|divide|ItemOperate|UIControl` ได้ 0 hits จึงยังตอบ caption dialog 0x12 ไม่ได้จาก Lua ชุดนี้

ข้อเสนอ amend docstring (ผู้รับงานไม่ได้แก้ไฟล์): เปลี่ยนเหตุผลจาก “packed/cracking proprietary data” เป็น “TEXTDATA และ trigger/quest Lua แตกแล้ว แต่ decoded Lua corpus ไม่มี UI caption/controller assets ที่ผูก numeric dialog 0x12; positive split label ยังต้อง asset source อื่นหรือ attended capture”

## จ็อบ 4 — `2600001 -> 26/1 -> ITEM_MISC -> linked TIP name`

crosswalk จริง: `PF_GAMEDATA_INDEX.tsv` แถว `CONSTDATA_TH index=042 table=ITEM_MISC flags=ITEM_MISC_TIP`; จึง join base `ITEM_MISC.n_ID` กับ `TEXTDATA_TH__ITEM_MISC_TIP.n_ID` ด้วย field `n_ID` ไม่ใช่ row order

| n_ID | ITEM_MISC row / `s_NAME` escaped | ITEM_MISC_TIP row / `s_NAME` |
|---:|---|---|
| 1 | row 1 / `\u5192\u96aa\u4e4b\u9470` | row 1 / `Adventure Key` |
| 2 | row 2 / `\u6d77\u795e\u91d1\u5e63` | row 2 / `Poseidon Gold` |
| 10 | row **9** / `\u98a8\u5143\u7d20` | row **10** / `Wind Element` |

`ITEM_MISC` มี 1,646 แถว, TIP มี 1,922 แถว, common `n_ID` 1,646; คู่ n_ID=10 แสดงโดยตรงว่า row order ไม่ใช่ crosswalk. สำหรับ `2600001`, decoder แยก `26` เลือก family ที่ pin เป็น ITEM_MISC, remainder `1` เลือก `n_ID=1`, และ client name path query `s_NAME` จาก linked table — แหล่งชื่อของ Thai data build คือ `TEXTDATA_TH__ITEM_MISC_TIP.s_NAME = Adventure Key`, ไม่ใช่จีนใน `CONSTDATA_TH__ITEM_MISC.s_NAME`

## read-only SHA before = after

manifest ครอบ **1,115 files**: `pf_bridge/gamedata/**` ทั้งหมด (รวม tables + Lua), image, CONSTDATA `.dec`, external 3 tables และ tool docstring; ทุก path ตรวจ size+sha ก่อน verification rerun และหลัง rerunตรงกัน

- manifest: `pf_bridge/staged/re060_input_hashes_before.tsv` — sha256 `41d357aaea9f4b0558fe8c2a3eb2ae98ec6593c19fe5e3a9076ca3f84eb76c18`
- `GameClient.local.bin`: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `B_CONSTDATA_TH.pc_.dec`: size 8,443,000; sha256 `496dfb2ef2cf517482a7b426c9dd5edf0278564fe11195b96f36df90607f0d2d`
- `PF_GAMEDATA_INDEX.tsv`: `a9ab5efd3826a54e0cad3cb86f0c872ebd1d61219721ee8514d42e9d2110b5bc`

## nonclaims

- ไม่พิสูจน์ว่านี่คือสคีมของเซิร์ฟเวอร์ต้นฉบับ; pin เฉพาะ client/data build ที่ ship มา
- ไม่พิสูจน์ว่าชื่อ `$V1` ขึ้นถูกบนจอ; client-observable ว่างโดยเจตนา
- code-to-table names ติดป้ายหลักฐานเชิงนับ (ค); image ยืนยัน split/lookup mechanism แต่ runtime tree contents ไม่ได้ฝังเป็น switch
- ไม่พิสูจน์ความหมายคอลัมน์อื่น
- ไม่สรุปว่าทั้งเกมมีเพียงห้า code; ขอบเขตคือ item-reference columns ที่ระบุในใบและพบ code เพิ่มจาก store ได้หนึ่ง code
- ไม่แก้ v141, docstring, source, ledger หรือ queue; chief เป็นผู้ลงผล
