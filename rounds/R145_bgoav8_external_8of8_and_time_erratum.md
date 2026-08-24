# R145 (bgoav8) — ชุดส่งมอบ RE ครบ 8/8 บน git · erratum เวลาของ R144 · <งานหลักเติมท้ายรอบ>

- เวลา: 2026-08-24 03:5x–xx:xxZ UTC (10:5x–xx:xx +07:00)
- session: bgoav8 · branch เอกสาร `claude/exciting-goldberg-bgoav8` · branch โค้ด `claude/amazing-goodall-bgoav8`
- ล็อก: draft PR #46 (`pf_bridge`) เปิดเป็น draft ตั้งแต่วินาทีแรกตาม v5 ข้อ ① — ยึดล็อกได้ก่อนอ่านซอร์สใด ๆ

## probe ต้นรอบ

1. **GitHub API/tool: ✅** — `list_pull_requests` อ่านได้ทั้งสอง repo (open = ว่างทั้งคู่) · `create_pull_request` เปิด draft ได้ (#46)
2. **ทาง D `ci-status`: ✅** — `git fetch origin ci-status && git ls-tree` สำเร็จ (`d_exit=0`) บน `pirate-force-server`
3. **โครงพี่น้อง: ✅** — `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 bytes)
4. **กล่องจดหมาย: ว่าง** — ไฟล์ `.md` ขาเข้าทุกใบมี `.CONSUMED.txt` คู่ครบ (ไม่มีใบใหม่หลังชุด 5 ใบที่ R144 บริโภค)

## ⏱️ erratum: บล็อกเวลาของ R144 เพี้ยนไป 7 ชั่วโมง

**วัดจริง:** `git show -s --date=iso 0ad4f1a fbd1cfd` ⇒ round claim `2026-08-24 02:51:50 +0000` · commit งาน `03:21:38 +0000`
⇒ R144 รันจริง **02:51–03:21 UTC = 09:51–10:21 (+07:00)**

**ที่ R144 เขียนไว้:** `~09:4x–10:4xZ UTC (~16:4x–17:4x +07:00)` — เลข UTC ใกล้เคียงเวลา **+07:00** จริง
แล้วถูกบวก 7 ซ้ำอีกชั้นตอนแปลงเป็นไทย ⇒ ป้าย +07:00 เลยไปข้างหน้า 7 ชั่วโมง

**จุดที่แก้ในรอบนี้:** `GAME_TEST_QUEUE.md` บล็อกสถานะ R144 ของใบ GT-047 (บรรทัดที่ผู้เทสอ่านจริง — แก้เป็นเวลาจริงพร้อมกำกับ erratum)
**จุดที่ไม่แก้ (โดยเจตนา):** บรรทัด R144 ใน `CHIEF_CONTINUATION.md` (กฎหนึ่งรอบหนึ่งไฟล์ห้ามแก้บรรทัดเก่า — แก้แล้วเสี่ยงชน)
· หัวไฟล์ `rounds/R144_*.md` (บันทึกรอบเป็นของรอบนั้น — erratum อยู่ที่นี่แทน)
· ชื่อไฟล์จดหมาย `FROM_CHIEF_R144_TO_ATTENDED_20260824_1740.md` (rename = deletion ในสายตาตัว sync — ห้ามตามเทส T6)
⇒ **ถ้าอ่านย้อนหลังแล้วเจอ "17:40" ของ R144 ให้อ่านเป็น "10:21 +07:00"**

## 📦 ชุดส่งมอบ RE ของ Codex — ครบ 8/8 บน `main` แล้ว (ปิดของค้างที่เปิดมาตั้งแต่ R129)

สามตารางท้ายที่ R131 whitelist ไว้แล้วรอหน้าสะพาน `git add` **เข้ามาแล้ว** ที่ commit `579b468`
(`external: publish the last 3 Codex RE deliverable tables (Panya ruling 2026-08-23 20:39)` · 2026-08-24 09:29 +07:00)

| ตาราง | แถว data (นับบน cloud clone รอบนี้) |
|---|---|
| `PF_PROTOCOL_PRIORITY.tsv` | 519 |
| `PF_DATA_EVIDENCE.tsv` | 290 |
| `PF_TAG_CENSUS.tsv` | 11 |
| **รวม** | **820 — ตรงกับที่จดหมาย 20:39 พินไว้เป๊ะ** |

**ของใหม่ที่ `PF_TAG_CENSUS.tsv` เพิ่งเปิดให้ฝั่ง cloud เห็น** (มีผลกับทุกใบที่เขียน codec):
11 tag ความยาวคงที่ — `0x05`/`0x08`/`0x0B` = 1 ไบต์ · `0x0F`/`0x12` = 2 · `0x14`/`0x19`/`0x1F`/`0x26`/`0x2A` = 4 · `0x32` = 8
🔴 **คอลัมน์ `proven_semantics` = `UNKNOWN` ทุกตัว ยกเว้น `0x12` = uint16 และ `0x2A` = float32**
⇒ **ห้าม derive ชนิดจากความยาว** — ตารางบอกว่ากว้างเท่าไหร่ ไม่ได้บอกว่ามันคืออะไร

## 🔧 งานโค้ดหลัก — EXTERNAL-REGISTRY-002: ตัวอ่านครอบ 8 ตาราง + cross-check ข้ามตาราง

**ทำไมรอบนี้ถึงทำได้ และรอบก่อนทำไม่ได้:** ตารางที่ 8 เพิ่งเข้า git เมื่อเช้านี้ ⇒ อินเวเรียนต์ที่ต้องใช้ตาราง
**คนละใบ** มาเทียบกันเพิ่งเป็นไปได้เป็นครั้งแรก ตารางใบเดียวตรวจได้แค่ "รูปร่าง" แต่สองใบตรงกันคือหลักฐานเรื่องตัว derivation

**ไฟล์ที่แตะ (repo โค้ด · 4 ไฟล์ · ไม่มีไฟล์ใหม่):**
`tools/pf_external_registry.py` · `tests/test_external_registry.py` · `tests/pf_preconditions.py` · `docs/PYTEST_SKIP_PINS.json`

**อินเวเรียนต์ใหม่ที่ตัวอ่านบังคับแล้ว (ทุกตัววัดบนตารางจริง ไม่มีตัวไหนเดา):**

| # | อินเวเรียนต์ | ตัวเลขที่วัดได้ |
|---|---|---|
| 1 | `PF_TAG_CENSUS` พิน len แบบ FIXED ต่อ tag · ทุกแถวใน serializer ที่ถือ tag นั้นต้อง len ตรง | 2,783 แถว mismatch 0 |
| 2 | `frequency_in_A2` ของ census = จำนวนแถวจริงใน serializer เป๊ะ ทุก tag | 11/11 ตรง |
| 3 | `PF_PROTOCOL_PRIORITY` ตั้งชื่อ message ชุดเดียวกับ registry/serializer | 519 = 519 = 519 |
| 4 | `serializer_status` แยก CLOSED/OPEN | 338 / 181 |
| 5 | 🔴 **ชุด OPEN ของ priority = ชุด static-open ที่ derive จาก `UNKNOWN(` ใน `field_offset`** | **181/181 สมาชิกเดียวกันเป๊ะ** |
| 6 | `PF_DATA_EVIDENCE`: evidence_id ไม่ซ้ำ · sha256 UPPER-case 64 ตัว · parse_status | 290 แถว · 287 PASS / 3 NONSTANDARD_GRAMMAR |
| 7 | `proven_semantics` = `UNKNOWN` ทุก tag ยกเว้น `0x12`=uint16 · `0x2A`=float32 | pin ไว้ กันตารางรุ่นหลัง "อัปเกรด" ชนิดเงียบ ๆ |

**ข้อ 5 คือข้อที่มีค่าที่สุด:** การ์ด `field_offset` ที่ R144 ส่งไปให้สะพาน pin ชุด static-open ไว้ด้วย membership digest
โดย derive จากคอลัมน์ `field_offset` ของตารางใบหนึ่ง · ตาราง priority เดินคนละคอลัมน์ของคนละไฟล์แล้วได้ **181 ใบเดียวกัน**
⇒ เทสยืนยัน **ความเท่ากันของเซ็ต ไม่ใช่แค่จำนวน** เพราะการโจมตีที่ adversary ของ R144 หาเจอคือชนิดที่รักษาจำนวนแล้วสลับสมาชิก

**เทสใหม่ 9 ใบ** (6 ใบเป็น mutation ที่ต้องแดง: census len ขัดแถวจริง · frequency drift · การอัปเกรด semantics ·
membership swap แบบรักษาจำนวน · evidence_id ซ้ำ · sha256 ที่ถูกแปลงเป็นตัวพิมพ์เล็ก)
**สวีตเต็ม:** `2030 passed / 324 skipped / 0 failed` เขียว(cloud sanity) · `--verify` exit 0 ·
`verify_hypothesis_ledger.py` PASS entries=42 (รอบนี้ไม่เปิด hypothesis ใหม่ จึงไม่แตะ ledger/coverage)
**SKIP-CENSUS:** pin ขยับ 12 → 21 (เทสใหม่ทุกใบอยู่ใต้ precondition `external_re_tables` ซึ่งตอนนี้ตั้งชื่อครบ 8 ไฟล์)
**pin commit:** `PF_BRIDGE_PIN_COMMIT` 284d986 → **579b468** (ตรวจแล้วว่า `579b468:external` กับ `origin/main:external`
เป็น tree object เดียวกัน `206370d`)

## 📌 คำถามค้าง #1 ของ R144 (เลนลูท) — มีคำตอบแล้ว และคำตอบคือ "ไม่ต้องเปิดเลนใหม่"

R144 จดคำถามถึงคุณว่า "เลนลูทต้องส่ง `ItemOperateVitalRes` เอง — เกิน pre-approved ไหม" **คำถามนั้นตั้งอยู่บนสมมติฐานที่ผิด**
ลูกมือสำรวจ repo โค้ดแล้วพบว่า **encoder ของ `ItemOperateVitalRes 0x4C13` มีอยู่แล้วสามทรง** ใน
`src/pirateforce_foundation/inventory.py` (move-delta · swap · merge) พร้อม dispatch branch ใน `runtime.py`
และ v141 ก็มี `make_item_operate_move_delta_success` ที่ **ไคลเอนต์ยอมรับเฟรมจริงมาแล้ว** (รายงาน V106 · 2026-08-14)

⇒ สิ่งที่ขาดไม่ใช่ "เลนใหม่" แต่เป็นสองข้อเท็จจริงที่ยังไม่มี — และรอบนี้เปิดเป็นใบสะพานทั้งคู่ (ดูหัวข้อใบใหม่)
① payload หน้าตาแบบไหนที่ทำให้ข้อความเขียว id 131 ยิงจริง (GT-049 พิสูจน์แค่ว่า handler ยิงได้ ไม่ได้พิสูจน์ว่าอะไรทำให้ยิง)
② รหัสไอเทม `26xxxxx` แปลว่าอะไรกันแน่ — `$V1` ในข้อความคือชื่อไอเทมที่ไคลเอนต์ resolve เองจาก template id ที่เราส่ง

**shape ของ `ItemOperateVitalRes` ที่ derive ได้จากตาราง** (เรียงตาม `file_off_claim` — 🔴 **ห้ามเรียงตามคอลัมน์ `order`**
เพราะ extractor ใส่แถว call ซ้ำทั้งขา W และ R ที่ offset เดียวกัน):
`0x08 u8` result · `0x0B u8` bag_present · [call `0x0046F4D0` = nested ItemBagAttr ขนาดคงที่ 0x68] ·
`0x08 u8` affected_identity_count · ต่อด้วย element ละ (`0x32` qword · `0x08` u8)
⚠️ ในตาราง Res มี **13 แถวต่อขา แต่เป็นฟิลด์จริงแค่ 5** (อีก 8 เป็นแถว call/import/atomic ที่ไม่ใช่ไบต์บน wire) —
ถ้ารอบไหนอ่าน "13" เป็นจำนวนฟิลด์จะพังทันที
🔴 **`ItemOperateVitalRes` ไม่มีฟิลด์ string เลยสักแถว** ⇒ `$V1`/`$V2` ถูกเติมฝั่งไคลเอนต์จาก template id + จำนวน
ที่อยู่ **ข้างใน ItemBagAttr ที่ nest อยู่** — ห้ามพยายามส่งชื่อไอเทมเป็นสตริง

## ⚠️ คำอ้างเท็จที่พบในไฟล์แช่แข็ง (จดไว้ ไม่แก้)

`current/pf_login_game_server_v141.py:2470` เขียนคอมเมนต์ว่า
`V103_ITEM_TEMPLATE = 2600001  # STORE_NORMAL row 1 -> ITEM_MISC row 1, Adventure Key`
ตรวจกับ `gamedata/tables/` ที่เพิ่งมีแล้วพบว่า **ผิดอย่างน้อยสองจุด**: `2600001` ไม่ปรากฏเป็น `n_ID` ในตาราง CONSTDATA ใดเลย
· ที่มันปรากฏคือในฐานะ *ค่าที่ถูกอ้างถึง* ที่คอลัมน์ `n_ID_ITEM15` ของ `STORE_NORMAL` (ไม่ใช่ row 1) และ `n_ID_ITEM1` ของ `STORE_GOODS`
· `PF_GAMEDATA_INDEX.tsv` ให้ index ของ `ITEM_MISC` = **042** ไม่ใช่ `26`
🔴 **ไม่แก้ไฟล์นั้น — `current/` คือ v141 immutable** · เรื่องนี้กลายเป็นใบ RE-060 แทน
