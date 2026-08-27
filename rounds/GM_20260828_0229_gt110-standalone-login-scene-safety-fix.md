# LANE-GM round `ccc9wj` — 2026-08-28T02:29+07:00

## บริบท
รอบก่อน (`w8t8vi`) ปิดด้วย args-shape hardening อีกชั้น — ตรวจแล้ว (ขั้น A) ทั้งสอง PR ของรอบนั้น
(`pf_bridge#253`, `pirate-force-server#160`) merge เข้า main จริงแล้ว (`pull_request_read` ยืนยัน
`merged: true`, `merged_at` ตั้งแล้วทั้งคู่) ไม่ต้อง cherry-pick

## ขั้น A (addendum v2) — ตรวจชะตา PR รอบก่อน
`pf_bridge` PR #253, `pirate-force-server` PR #160 — ทั้งคู่ `merged: true` ยืนยันผ่าน GitHub API ตรง ๆ
(ไม่ต้องพึ่ง git fetch เทียบเพิ่มรอบนี้ เพราะ API ตอบตรงและสอดคล้องกัน)

## ขั้น B — กล่องจดหมาย
ใบเดียวที่ pending จริงถึง `LANE-GM`:
`notes_to_chief/20260827_2240_KA1A-NOTE-GT110-unsafe-until-0x5A19-payload-fixed-plus-M1P-jobs-staged.md`
ส่วน (1) เป็นของสาย GM โดยตรง (GT-110 ยังไม่ปลอดภัยจนกว่า 0x5A19 จะพิสูจน์แล้ว) ส่วน (2) M1-P เป็นเขตของ
สาย A/B/chief ไม่ใช่ของสาย GM — อ่านแล้ว ไม่มีอะไรต้องทำต่อฝั่งนี้ บริโภคเฉพาะส่วน (1)

(ใบอื่นที่ grep เจอคำว่า `ADDRESSEE: LANE-GM` เป็นแค่การอ้างอิงในเนื้อความของสถานะเก่าของ LANE-GM เอง
ไม่ใช่ addressee header จริง -- ตรวจแล้วไม่ต้องบริโภคซ้ำ)

## งานที่ทำ

### วิเคราะห์ก่อนแก้
`GT-110` เดิมต้องมีบัญชีอยู่ใน `gm_accounts.json` (ผ่าน `get_login_scene_override`'s GM-gated path) ⇒
`is_gm_account()==True` ⇒ `runtime.py:5045` ส่ง `GM_UpdateGMStateVital` (`0x5A19`) ⇒ เฟรมนี้ฆ่าเซสชันจริง
มาแล้วสองครั้งคนละแบบ (`GT-101` version=1 → error 23065, `GT-107` version=0 → error 28317) `RE-113` แก้
สาเหตุของ `GT-107` แล้ว (`GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED = 0` + `make_runtime_vitals` พหูพจน์)
แต่ **ยังไม่มี attended run ยืนยันบน client จริง** — `GT-107-R3` ยัง `[PENDING]` KA1A-NOTE เสนอทางแก้ที่
"เร็วกว่าและปลอดภัยกว่า": แยก scene override ออกจากสถานะ GM ให้ `GT-110` ไม่ต้องรอคำตอบของ `GT-107-R3`
ก่อน — ตัดสินทำตามข้อเสนอนี้ ติดป้าย `[สมมติของสาย GM - รอ COO ยืนยัน]` (เปลี่ยนสัญญาความปลอดภัยของโมดูล
แม้ไม่ให้สถานะ GM ใด ๆ)

### `gm/login_scene_override.py` (pirate-force-server)
เพิ่มเส้นทาง **standalone** ที่สอง คู่ขนานกับ GM-gated path เดิม (ไม่แก้พฤติกรรมเดิม):
- `load_standalone_login_scene_overrides` อ่าน `config/gm_login_scene_standalone.json` (env
  `PF_GM_LOGIN_SCENE_STANDALONE_CONFIG`) คีย์ `standalone_login_scene` — shape/malformed-config validation
  เดียวกับ path เดิมทุกประการ (non-dict, non-int scene_id, bool-as-int, unknown scene_id → ValueError)
- `get_login_scene_override` เช็ค GM-gated path ก่อน (คงพฤติกรรมเดิม 100% สำหรับบัญชีที่อยู่ใน
  `gm_accounts.json`) แล้วค่อย fallback ไป standalone path ถ้าทางแรกไม่มีคำตอบ
- **ไม่แตะ `runtime.py`** — จุดเสียบเดิมจาก `CORE-REQUEST-015` (`get_login_scene_override(self.token)`)
  พอแล้ว เส้นทางใหม่ทำงานผ่านจุดเดิมโดยอัตโนมัติ ไม่ต้องเขียน CORE-REQUEST ใหม่
- บัญชีที่อยู่ใน standalone config เท่านั้น **ไม่มีทาง** `is_gm_account()` เป็นจริง (`is_gm_account()` ไม่เคย
  อ่านไฟล์นี้เลย) ⇒ `runtime.py`'s `CORE-REQUEST-016` guard ไม่มีวันส่ง `0x5A19` ให้บัญชีนี้

### pf-adversary (subagent จริง, รันก่อน commit ตามธรรมเนียมทุกรอบ)
สั่งให้ตรวจ boundary ระหว่าง `is_gm_account()`/state-frame gate กับเส้นทาง standalone โดยเฉพาะ ไม่ใช่แค่
อ่านโค้ด — ให้รันผ่าน dispatcher จริงด้วย ผล: **claim หลักยืนยันจริง** (พิสูจน์ end-to-end เอง: บัญชี
standalone-only ไม่มี `GM_UPDATE_STATE_AFTER_LOGIN` ในผลของ dispatch, ย้ายไป `gm_accounts.json` แทนแล้วมี
— สองสถานการณ์ต่างกันจริง) พบข้อบกพร่องจริง 2 ข้อ ทั้งคู่แก้แล้วก่อน push:

1. **[MODERATE] `docs/GM_LANE.md` ค้างข้อมูลเก่า** — ส่วน "Modules delivered (GM-005 login-scene-override
   round)" ยังเขียนว่า "Neither file alone can grant anything" ซึ่งไม่จริงอีกต่อไปหลังรอบนี้ — แก้โดยขีดฆ่า
   ประโยคเดิม (ไม่ลบประวัติ) ชี้ไปหัวข้อใหม่ท้ายไฟล์ที่มีสัญญาปัจจุบันที่ถูกต้อง
2. **[LOW] เทส precedence เดิมพิสูจน์อะไรไม่ได้จริง** — `test_gm_gated_path_still_wins_when_both_paths_have_an_entry`
   ใช้ `scene_id` เดียวกันทั้งสองทาง agent สร้าง implementation ที่ผิด (เช็ค standalone ก่อน) แล้วโชว์ว่าเทส
   เดิมยังผ่านอยู่ดี — แก้โดยใช้ scene_id ต่างกันสองค่า (gated=2, standalone=1) ยืนยันว่าผลลัพธ์มาจาก gated
   path จริง ไม่ใช่ standalone

**[INFORMATIONAL, ปิดแล้วในรอบนี้]** ก่อน pf-adversary ชี้ ยังไม่มีเทสระดับ dispatcher จริงพิสูจน์ claim
หลัก (มีแต่เทสเรียกฟังก์ชันเดี่ยว ๆ) — เพิ่ม `tests/test_gm_login_scene_override_wiring.py` 3 เทสใหม่:
บัญชี GM-gated ยังได้ทั้ง override และ `GM_UPDATE_STATE_AFTER_LOGIN` (contrast case), บัญชี standalone-only
ได้ override แต่ **ไม่มี** action นั้นเลย (claim หลัก, พิสูจน์ end-to-end), และ `is_gm_account()` ยังเป็น
`False` แน่นอนสำหรับบัญชีที่อยู่ใน standalone config เท่านั้น

**คำถามเปิดที่ agent ชี้เอง (ไม่ใช่บั๊ก แต่เป็นความเสี่ยงที่มีอยู่แล้ว ไม่ใช่ของใหม่รอบนี้):**
`gm/state_wire.py`'s `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED = 0` (ไม่ใช่ `None`) หมายความว่าบัญชีอื่นที่
ถูกเติมเข้า `gm_accounts.json` ด้วยเหตุผลใดก็ตาม (ไม่ใช่แค่ `GT-110`) จะได้เฟรม `0x5A19` ที่ยังไม่เคย
attended-verify ทันที — ทางแก้รอบนี้ช่วยเฉพาะ `GT-110` ส่งต่อคำถามนี้ให้ COO ในใบ ASK-COO แยก

### เทสใหม่ (pirate-force-server)
- `tests/test_gm_login_scene.py`: +7 (missing-file, grant-with-zero-gm_accounts-membership, unlisted→None,
  malformed config x2, unknown scene_id, precedence-with-differing-values)
- `tests/test_gm_login_scene_override_wiring.py`: +3 (contrast GM-gated case, core safety proof ผ่าน
  dispatcher จริง, `is_gm_account()` ยังเท็จ)
- `tests/test_gm_*.py`: 250/250 (เดิม 240 + 10 ใหม่) ไม่มี regression ของ path เดิม -- ทุก input ที่เคยผ่าน
  ยังผ่านเหมือนเดิมทุกกรณี

### `docs/GM_LANE.md`
ขีดฆ่าประโยคเก่าที่ผิดแล้ว + เพิ่มหัวข้อ "Modules delivered (round `ccc9wj`, GT-110 standalone login-scene
safety fix)"

### `GAME_TEST_QUEUE.md` (pf_bridge)
แก้หัวใบ `GT-110`: server args เปลี่ยนจาก `PF_GM_ACCOUNTS_CONFIG` + `PF_GM_LOGIN_SCENE_CONFIG` เป็น
`PF_GM_LOGIN_SCENE_STANDALONE_CONFIG` เดียว (ห้ามตั้ง `PF_GM_ACCOUNTS_CONFIG` เลยในใบนี้) เงื่อนไขก่อนบูต
เปลี่ยน grep target เพิ่มเงื่อนไข "ต้องไม่เห็นบัญชีทดสอบใน gm_accounts.json จริง" pass criteria เพิ่ม: ต้อง
ไม่มีบรรทัด `[G>] GM_UPDATE_STATE_AFTER_LOGIN` ปรากฏเลยตลอด session (เห็น = FAIL ไม่ว่าจอจะถูกหรือไม่)
teardown ตัดขั้นตอนลบ `gm_accounts.json`/`gm_login_scene.json` ออก (ไม่เคยสร้างในทางแก้นี้) nonclaims เพิ่ม
ว่าใบนี้ไม่พิสูจน์เรื่อง `0x5A19` เอง (เป็นขอบเขตของ `GT-107-R3`) — `GT-110` ไม่ต้องรอ `GT-107-R3` อีกต่อไป

### จดหมาย
- `.CONSUMED.txt` stub สำหรับ KA1A-NOTE 2240 + สำเนาต้นฉบับไป `consumed/`
- ASK-COO ใหม่: `notes_to_chief/20260828_0222_LANE-GM-ASK-COO-standalone-login-scene-override-path.md`
  (ขอ COO ยืนยันการเปลี่ยนสัญญาความปลอดภัยของโมดูล + คำถามเปิดเรื่อง `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED`)

## pf-adversary
รันจริงก่อน commit (subagent, ไม่ใช่ self-review) — พบ 2 ข้อบกพร่องจริง (เอกสารค้าง + เทส precedence
อ่อน) แก้ครบทั้งสองก่อน push ไม่มีข้อค้างที่ตัดสินใจไม่แก้ นอกจากคำถามเปิดที่ส่งต่อ COO แล้ว

## เกณฑ์สองชั้น
- wire/DB: PASS headless — เทสใหม่ผ่านทั้งหมดรวมระดับ dispatcher จริง, 250/250 ทั้งไฟล์ `test_gm_*.py`
- client-observable: ยังไม่มีของรอบนี้ — `GT-110` (ตอนนี้ปลอดภัยและพร้อมรันแล้ว) รอ attended runner

## nonclaim
รอบนี้ headless ล้วน ไม่มีการยิงเฟรมใส่ไคลเอนต์จริง ไม่แก้ `runtime.py` หรือไฟล์ในเขตของสายอื่น การแก้
`login_scene_override.py` เพิ่มเส้นทางใหม่เท่านั้น ไม่เปลี่ยนพฤติกรรมของบัญชี GM-gated เดิมแม้แต่กรณีเดียว
`GT-110` เองยังไม่ถูกรัน (นี่คือรอบที่ทำให้มันปลอดภัยพอจะรัน ไม่ใช่รอบที่รันมัน) การแก้นี้ไม่พิสูจน์อะไรเรื่อง
`GM_UpdateGMStateVital`/`0x5A19` ของตัวมันเอง — ขอบเขตนั้นยังเป็นของ `GT-107-R3` เท่านั้น

ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้: `GT-110` (per-account login-scene override) พร้อมรันจริงแล้ววันนี้
โดยไม่ต้องรอผล `GT-107-R3` ก่อน — เมื่อวานใบนี้เสี่ยงชนเฟรม `0x5A19` ที่ยังไม่ผ่าน attended verify

— LANE-GM รอบ `ccc9wj`
