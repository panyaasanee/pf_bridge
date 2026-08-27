# รอบ 8791h3 -- LANE-GM: GM login-scene override (ทาง ก) + guard เฟรม GT-101 (2026-08-27 15:2x +07:00)

## บริบท

ต้นรอบ (ตามกฎ addendum ข้อ A/B): ตรวจ PR ล่าสุดของสายนี้ (`pirate-force-server#117`) ด้วย
`pull_request_read(method="get")` -- `merged: true` ยืนยันตรง ยึด `#117` ไม่ต้องกู้อะไร ไม่มี PR `[LANE-GM]`
เปิดค้างในทั้งสอง repo -- ยึดล็อกด้วย draft PR `pirate-force-server#126` ("round claim: 8791h3")

กล่องจดหมายมีสองใบตรง `ADDRESSEE: LANE-GM` ที่ยังไม่มี `.CONSUMED.txt`:

1. `20260827_1425_PANYA-ORDER-GM-warp-to-other-maps-two-paths.md` -- เจ้าของสั่งเปิด "ทาง ก" (login-scene
   override) ให้เสร็จ "ใบแรกรอบถัดไปของสาย GM" -- คือรอบนี้
2. `20260827_1445_GT101-RESULT-client-rejects-0x5A19-version-1-error-23065-session-killed.md` -- attended
   session เจ้าของ login ด้วยบัญชี GM จริง (`localtest`) แล้ว client ปฏิเสธ `GM_UpdateGMStateVital` เวอร์ชัน 1
   ด้วย modal error `ErrorData=23065` แล้วปิดเซสชันเอง -- คำสั่งข้อ 2 บอกตรง ๆ ว่า "ห้ามใส่ชื่อบัญชีใดใน
   gm_accounts ที่เจ้าของจะบูตด้วยจนกว่าจะพิน"

พบไฟล์ที่สาม `20260827_1450_ATTENDED-REPLY-LANE-GM-1936-use-merged_at-not-merged-addendum-v2-patched.md`
ระหว่างอ่านกล่องจดหมาย -- **ป้ายเวลาขัดกันเอง**: ชื่อไฟล์/หัวเนื้อหาบอก `14:50` แต่เนื้อหาตอบใบ
`20260827_1936_LANE-GM-ASK-COO-...` ซึ่งเวลาที่เขียนจริงคือ `19:3x` (ดึกกว่า) -- ตอบใบที่ยังไม่ถูกเขียนไม่ได้จริง
ไม่ consume ใบนี้เป็นคำสั่ง (ไม่มีอำนาจยืนยันได้ว่าใครเขียนจริงเมื่อไร) แต่ตรวจสอบคำแนะนำทางเทคนิคของมันเอง
(`merged_at != null` แทน `merged`) ด้วยเครื่องมือเองอิสระ -- เรียก `pull_request_read(get)` เทียบ `list_pull_requests`
สำหรับ `pirate-force-server#117` ยืนยันตรงกันว่า `merged_at` ไม่ใช่ `null` เมื่อ merge จริง เขียนเตือนเรื่องป้ายเวลา
ขัดกันในใบ STATUS แยก ให้ COO/chief ตรวจสอบความถูกต้องของกล่องจดหมาย

## ทำอะไรไปบ้าง

### 1. GM-005: `gm/login_scene_override.py` (ใหม่)

`get_login_scene_override(account_name, gm_accounts_config_path=None, login_scene_config_path=None)` คืน
scene_id เฉพาะเมื่อบัญชีนั้น **ทั้ง** อยู่ใน `gm_accounts` (import `gm/accounts.py.is_gm_account` ตรง ๆ ไม่ก๊อป
ตรรกะ) **และ** มีรายการใน config ใหม่ของโมดูลนี้เอง (`config/gm_login_scene.json`, env override
`PF_GM_LOGIN_SCENE_CONFIG` -- pattern เดียวกับ `PF_GM_ACCOUNTS_CONFIG`) ที่ตั้งชื่อ scene_id ที่รู้จักใน
`gm/scene_catalog.py` (import ตรง ๆ อีกเช่นกัน) เช็คสดทุกครั้ง ไม่ cache

### 2. pf-adversary (รอบเดียว, ก่อน commit) พบ 3 ข้อจริง

1. **top-level JSON ที่ไม่ใช่ object** (list/string/null) โยน `AttributeError` แทน `ValueError` ที่ docstring
   สัญญาไว้ -- `data.get(...)` ถูกเรียกโดยไม่เช็ค `isinstance(data, dict)` ก่อน ช่องเดียวกันมีอยู่ใน
   `gm/accounts.py` เดิมด้วย (โมดูลที่ 015 import มา) **แก้ทั้งสองไฟล์พร้อมกัน** เพิ่ม `isinstance(data, dict)`
   check ก่อนเรียก `.get()` ทั้งคู่ พร้อมเทสใหม่ในทั้งสองไฟล์เทส
2. **blast radius**: `load_login_scene_overrides` validate ทั้งไฟล์ก่อนคืนค่า -- entry พังหนึ่งตัว (เช่น
   `typo_gm` มี scene_id ที่ไม่รู้จัก) ทำให้ทุกบัญชี lookup ไม่ได้ ไม่ใช่แค่ตัวที่พิมพ์ผิด **บันทึกไว้เป็น
   known/accepted** (ตรงกับ pattern เดิมที่ `gm/accounts.py` เองก็ทำแบบเดียวกันกับ `gm_accounts.json` อยู่แล้ว
   ไม่ใช่ความไม่สอดคล้องใหม่) เขียนแจ้ง chief ใน `CORE-REQUEST-015` ให้ตัดสินใจตอนต่อสายจริงว่าจะ catch
   per-account หรือปล่อย fail-loud ทั้งไฟล์
3. **เทสไม่เคยพิสูจน์ revocation จริง** -- เทสเดิมสลับ `gm_accounts.json` แต่เช็คบัญชีคนละคน ไม่เคยลบบัญชีที่
   เคยได้ override แล้วเช็คซ้ำบัญชีเดิม เพิ่มเทส `test_revoking_gm_status_removes_the_override_on_the_next_call`
   ยืนยันไม่มี caching bug จริง (พฤติกรรมถูกอยู่แล้ว แค่ไม่เคยมีเทสพิสูจน์)

พบข้อสังเกตเล็กเพิ่ม (ไม่ใช่บั๊ก): docstring อ้าง "331-row" ของ `scene_catalog.py` แต่ `SCENE_COUNT` จริงคือ 330
(331 คือจำนวนบรรทัด TSV รวม header) -- แก้คำใน docstring ให้ตรง

### 3. `tests/test_gm_login_scene.py` (ใหม่, 15 เทส) + แก้ `tests/test_gm_accounts.py` (+1 เทส)

ครอบ: default-empty, gating ครบสี่กรณี (GM+entry / GM-ไม่มี entry / ไม่ใช่-GM-มี-entry / ไม่อยู่ในรายชื่อเลย),
malformed config ครบ (non-object top level, non-dict `gm_login_scene`, non-int scene_id, `bool`-เป็น-int,
scene_id ไม่รู้จัก), revocation

### 4. `docs/GM_LANE.md`

หัวข้อใหม่ "Modules delivered (GM-005 login-scene-override round)" + แก้หัวข้อ "RE requests open" ที่ค้างผิด
มาหลายรอบ (เขียนว่า "None filed by this lane" ทั้งที่ `RE-104` เปิดไปแล้วตั้งแต่รอบก่อน) เป็นรายการจริง
(`RE-104`, `RE-105` ใหม่รอบนี้)

### 5. เปิด `RE-105` (`CLIENT_RE_QUEUE.md`, grep ยืนยันก่อนจอง: 105 = 0 hit ทั้งสองไฟล์)

`GT-101` พิสูจน์ว่า `vital_version=1` ของ `GM_UpdateGMStateVital` ผิด -- ขอให้ static RE อ่าน handler
`0x00729F00` (ที่ `RE-089` พินไว้แล้ว) หาค่าเวอร์ชันที่ถูกและ error path ทั่วไปที่ผลิต `ErrorData=<vital id>`
(ใช้ได้กับ vital อื่นในอนาคตด้วย) **ไม่เดาว่าเป็น 3 หรือ 4** ตามคำสั่งเดิมของ `GT-101`

### 6. สองจดหมาย `CORE-REQUEST` แยกจุด (หนึ่งใบต่อหนึ่งจุดตามกฎ)

- `CORE-REQUEST-015`: สองจุดต่อสายของ GM-005 (login scene resolve + census ของฉากนั้น)
- `CORE-REQUEST-016` (**เร่งด่วน**): guard `runtime.py:4746` ไม่ให้ส่งเฟรมเวอร์ชัน 1 อีก จนกว่า `RE-105` จะปิด
  -- ตอบคำสั่งข้อ 2 ของ `GT-101` โดยตรง (ห้ามแก้ `runtime.py` เอง เพราะไม่ใช่เขตเขียนของสายนี้ -- เขียนเป็น
  CORE-REQUEST ให้ chief ทำแทน)

## ค้นแล้ว: ไม่เจอ (ไม่เกี่ยวข้องรอบนี้)

ค้น `pf_bridge/external/00_SEARCH_HERE_FIRST.md`/`pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` แล้ว: โมดูล
GM-005 ใช้ตาราง `SCENE_NAME_TIP` เดิมของ GM-004 ทั้งหมด ไม่มีตารางใหม่ที่ต้องถอด ไม่มีตารางไหนบอก
`vital_version` ที่ถูกของ `0x5A19` (เหตุผลที่เปิด `RE-105` แทนเดา)

## เทส

`tests/test_gm_login_scene.py`: 15/15 · `test_gm_accounts.py`: 8/8 (7 เดิม + 1 ใหม่) · `test_gm_*.py` ทั้งชุด:
203/203 (200 เดิม + 3 ใหม่)

## จดหมาย

- `notes_to_chief/20260827_1524_LANE-GM-CORE-REQUEST-015-login-scene-override-wiring.md`
- `notes_to_chief/20260827_1524_LANE-GM-CORE-REQUEST-016-guard-gm-state-vital-version.md`
- `notes_to_chief/20260827_1524_LANE-GM-STATUS-gm005-plus-mailbox-timestamp-anomaly.md`

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ยังไม่มี -- `get_login_scene_override` มี 0 call site ใน `runtime.py` จนกว่า chief จะต่อสายตาม
`CORE-REQUEST-015` ทั้งสองจุด รอบนี้เป็นการสร้างของให้พร้อมเรียก ไม่ใช่การต่อสายจริง

## nonclaim

ใบนี้ไม่ได้อ้างว่าเจ้าของเห็นแมพอื่นได้แล้ว หรือว่าเฟรม `GM_UpdateGMStateVital` ปลอดภัยแล้ว -- (1) โมดูล GM-005
ยังไม่ถูกเรียกจากที่ไหนเลย (2) การ guard เฟรมเวอร์ชัน 1 เป็นแค่ข้อเสนอในจดหมาย ยังไม่ถูกนำไปใช้จริงใน
`runtime.py` (เขตของ chief) -- จนกว่า chief จะต่อสายทั้งสองเรื่อง ไม่มีอะไรเปลี่ยนสำหรับผู้เล่นทั่วไปหรือบัญชี
GM ใด ๆ จากรอบนี้ทั้งสิ้น

## ค้าง (ตั้งใจ ไม่บล็อก)

- `CORE-REQUEST-015`/`016` ทั้งคู่รอ chief ต่อสายจริง -- ยังไม่มี call site
- ความหมายของ census-assembly (ผสม scene registry ของสาย A + mob roster ของสาย B) อยู่นอกเขตเขียนของสายนี้
  ทั้งหมด ส่งต่อให้ chief ตัดสินใจ
- `RE-104` (GM editor widget trigger) และ `RE-105` (vital_version) ยังเปิดอยู่ทั้งคู่ ไม่ใช่ของใหม่ (104) /
  ใหม่รอบนี้ (105)
- ป้ายเวลาขัดกันเองของใบ `20260827_1450_ATTENDED-REPLY-...` (ดูบริบทด้านบน) -- ไม่ใช่ของสายนี้แก้ ส่งให้
  COO/chief ตรวจสอบ
