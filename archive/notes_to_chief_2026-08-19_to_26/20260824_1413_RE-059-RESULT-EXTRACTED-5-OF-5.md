[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-059 RESULT — EXTRACTED 5/5 `ItemOperateVitalRes:R`

เวลา: 2026-08-24T14:08:33+07:00 ถึง 2026-08-24T14:13:19+07:00  
ชนิดงาน: STATIC-ON-BRIDGE ล้วน · ไม่บูต server/client · ไม่จับ `LOCK_GAME` · ไม่แตะ DB

## คำตอบ objective หนึ่งประโยค

**ถอดครบ 5/5 — ทั้งห้าเฟรมเป็น opcode `0x4C13` version 2, `R4=0`, `bag_present_flag=1`, มี `ItemBagAttr` ยาว 43/52/69/69/43 ไบต์ตามลำดับ และ `affected_identity_count=0` จึงไม่มี element R11/R12 ทุกเฟรม**

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว:** เจอ registry/schema ของ `ItemOperateVitalRes`, aggregate `R observed_frames=5 / capture_file_count=4 / A2_STATIC_OPEN`, inventory hash ของ exact 4 ไฟล์ และ serializer span `0x005EDA20`; ไม่เจอ raw capture bytes ในชุดส่งมอบ จึงเดิน corpus ตาม logic ของ validator
- **ค้น gamedata แล้ว:** เจอ `template_id` ที่ถอดได้สองค่า: `2600001` ใน `CONSTDATA_TH__STORE_GOODS`, `CONSTDATA_TH__STORE_NORMAL`, `QUESTDATA_TH__QUEST`; `2400901` ใน `CONSTDATA_TH__DROPS_SPECIALLY`, `CONSTDATA_TH__STORE_NORMAL`, `QUESTDATA_TH__QUEST` — รายงานแค่ occurrence ไม่ใช้สรุปสคีมรหัสไอเทม (สงวนไว้ให้ RE-060)

## corpus / inventory gate

root: `C:\Users\Panya\Desktop\Pirate Force\GameClient`

| file (relative to root) | sha256 | frames |
|---|---|---:|
| `capture_item_move_hyp001_25690817_002012/capture_v141/GAME_20260817_002429_300322_58470.txt` | `2e43b7066130cf3c2ac43493aebd7bc9662085ce4fb6276809e6baf52a2a581e` | 1 |
| `capture_item_lifecycle001_25690816_172425/capture_v141/GAME_20260816_172756_032705_62087.txt` | `b35ef7694e4946ffd31ec9a63948a19819009f477d2a783f48aae722bfb6be16` | 1 |
| `capture_gt015_20260819_112154/capture_v141/GAME_20260819_112348_630062_54449.txt` | `1e231e93241a757b1cb21b540334aaae8e6a8e8340ed28b58227965813b119df` | 2 |
| `capture_gt002_20260817_163028/capture_v141/GAME_20260817_163316_585783_61281.txt` | `7b5a7265e37cd1f427910951d5da31fdb955b5c47d72dc34d1938bf2fc268a87` | 1 |

ตัว extractor ตรวจ size+sha กับ `PF_INPUT_INVENTORY.tsv`, ใช้ `extract_pc_blocks()` ตัวเดียวกับ validator, guard `files==4` และ `frames==5`; ผลรัน exit 0

## ตารางต่อเฟรม

`index` คือ ordinal ของ PC block ที่ validator เดินในไฟล์นั้น; `len` เริ่มที่ wrapper tag `0x12` ของ opcode และจบหลัง R10/R12 (ไม่รวม outer tail `0B00`)

| # | file ย่อ | index | PC len | wrapper off | opcode/ver | len | R4 | R5 | bag len | R10 | R11/R12 |
|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `item_move...58470.txt` | 101 | 71 | 15 | `4C13/2` | 54 | 0 | 1 | 43 | 0 | none |
| 2 | `item_lifecycle...62087.txt` | 66 | 80 | 15 | `4C13/2` | 63 | 0 | 1 | 52 | 0 | none |
| 3 | `gt015...54449.txt` | 58 | 97 | 15 | `4C13/2` | 80 | 0 | 1 | 69 | 0 | none |
| 4 | `gt015...54449.txt` | 123 | 97 | 15 | `4C13/2` | 80 | 0 | 1 | 69 | 0 | none |
| 5 | `gt002...61281.txt` | 165 | 71 | 15 | `4C13/2` | 54 | 0 | 1 | 43 | 0 | none |

### full message hex

1. `12134C0B0208000B010BFF3200000000000000000F01003201000000000000001441AC27000F02000F0200080008FF0B000F00000800`
2. `12134C0B0208000B010BFF3200000000000000000F01003201000000000000001441AC27000F02000F0000080008FF0B000F01003203000000000000000800`
3. `12134C0B0208000B010BFF3200000000000000000F02003201000000000000001441AC27000F02000F0100080008FF0B003202000000000000001485A224000F01000F0000080008FF0B000F00000800`
4. `12134C0B0208000B010BFF3200000000000000000F02003201000000000000001441AC27000F02000F0000080008FF0B003202000000000000001485A224000F01000F0100080008FF0B000F00000800`
5. `12134C0B0208000B010BFF3200000000000000000F01003201000000000000001441AC27000F02000F0A00080008FF0B000F00000800`

### nested `ItemBagAttr` hex / parse

โครงที่ลงตัวทุกเฟรม: base (`0B u8`, `32 qword`) -> update collection (`0F u16 count`, element ละ `32 qword + 14 u32 + 0F u16 + 0F u16 + 08 u8 + 08 u8 + 0B u8`) -> removal collection (`0F u16 count`, element ละ `32 qword`)

1. 43 bytes: `0BFF3200000000000000000F01003201000000000000001441AC27000F02000F0200080008FF0B000F0000`  
   base `FF / 0`; update count 1: `(32=1,14=2600001,0Fa=2,0Fb=2,08a=0,08b=255,0B=0)`; removal count 0
2. 52 bytes: `0BFF3200000000000000000F01003201000000000000001441AC27000F02000F0000080008FF0B000F0100320300000000000000`  
   base `FF / 0`; update count 1: `(32=1,14=2600001,0Fa=2,0Fb=0,08a=0,08b=255,0B=0)`; removal count 1: `32=3`
3. 69 bytes: `0BFF3200000000000000000F02003201000000000000001441AC27000F02000F0100080008FF0B003202000000000000001485A224000F01000F0000080008FF0B000F0000`  
   base `FF / 0`; update count 2: `(32=1,14=2600001,0Fa=2,0Fb=1,08a=0,08b=255,0B=0)`, `(32=2,14=2400901,0Fa=1,0Fb=0,08a=0,08b=255,0B=0)`; removal count 0
4. 69 bytes: `0BFF3200000000000000000F02003201000000000000001441AC27000F02000F0000080008FF0B003202000000000000001485A224000F01000F0100080008FF0B000F0000`  
   base `FF / 0`; update count 2: `(32=1,14=2600001,0Fa=2,0Fb=0,08a=0,08b=255,0B=0)`, `(32=2,14=2400901,0Fa=1,0Fb=1,08a=0,08b=255,0B=0)`; removal count 0
5. 43 bytes: `0BFF3200000000000000000F01003201000000000000001441AC27000F02000F0A00080008FF0B000F0000`  
   base `FF / 0`; update count 1: `(32=1,14=2600001,0Fa=2,0Fb=10,08a=0,08b=255,0B=0)`; removal count 0

หลัง nested bag ทุกเฟรมมี `08 00` = R10 count 0 แล้วเหลือ outer runtime tail `0B 00` เท่ากัน

## image cross-check (job 3 เพิ่มเติม)

- direct helper `0x0046F4D0`: recursive CFG `[0x0046F4D0,0x0046F5DB)`, file offset `0x0006E8D0`, len 267, sha256 `b9308abc49969ded9194d369823de1f29207ca8addcfe22f838a4b3d1ea45885`; 87 instructions / 267 decoded bytes / gap 0 / indirect jump 0 / decode errors **0**; path allocates `0x68` bytes (ขนาด memory object ไม่ใช่ wire len)
- vtable `0x00F0ECB8 + 0x34` = `0x0046F180`; serializer recursive CFG `[0x0046F180,0x0046F3E9)`, file offset `0x0006E580`, len 617, sha256 `29e38267ab54c852e3f1338c2fb833e3b9d1a41903544a390489c264c09fa813`; decode errors **0**
- ไม่ใช้ linear disassembly เป็นหลักฐานผลลบ

## เทียบคำทำนาย

คำทำนาย `bag_present_flag=1` และ `affected_identity_count=0` ตรง **5/5**; ข้อสรุปจำกัดอยู่ที่ capture ห้าเฟรมนี้ ไม่ยกระดับเป็นการพิสูจน์ encoder ทุกทรง

## reproducibility

- extractor ASCII-only: `pf_bridge/staged/re059_extract_capture.py` sha256 `4c681d905ce5742dcbdea539e5064267a5a269aea245375189c651ae566e7cca`
- recursive CFG probe: `pf_bridge/staged/static_recursive_cfg_probe.py` sha256 `120a32b4a5b1a7a266a27588e150f52a11de7e92fc241f5277707377cafef903`
- command: `python pf_bridge/staged/re059_extract_capture.py --client GameClient --inventory pf_bridge/external/PF_INPUT_INVENTORY.tsv --validator pf_bridge/patches/gt047/pf_validate_capture_fields.py`

## read-only SHA before = after

- `GameClient.local.bin`: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `PF_PROTOCOL_REGISTRY.tsv`: `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_SERIALIZER_FIELDS.tsv`: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_INPUT_INVENTORY.tsv`: `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1`
- capture 4 ไฟล์: hash ตามตาราง corpus ด้านบน ตรง inventory ทุกไฟล์ทั้งก่อนและหลัง
- `PF_GAMEDATA_INDEX.tsv`: `a9ab5efd3826a54e0cad3cb86f0c872ebd1d61219721ee8514d42e9d2110b5bc`
- `pf_login_game_server_v142.py` (อ่านเฉพาะคำอธิบายโครง): `a19155f3946b7b0cb998559f20a453c2bbda842c49b804fe889589eaa20ef807`

## nonclaims

- ไม่พิสูจน์ความหมายของ R11/R12; ทั้งห้าเฟรมมี count 0 จึงไม่มีค่ามาให้ตั้งชื่อ
- ไม่พิสูจน์ว่า encoder ทุกทรงถูกหรือผิด; พิสูจน์เพียงว่าเฟรมจริงห้าตัวมีรูปข้างต้น
- ไม่พิสูจน์ producer direction หรือกฎของเซิร์ฟเวอร์ต้นฉบับ
- ไม่พิสูจน์ข้อความ/ภาพบน client; client-observable ว่างโดยเจตนา
- capture 5 เฟรมไม่ครอบทุกทรงของ opcode `0x4C13`
- ไม่แก้ ledger/queue/source; chief เป็นผู้ลงผล
