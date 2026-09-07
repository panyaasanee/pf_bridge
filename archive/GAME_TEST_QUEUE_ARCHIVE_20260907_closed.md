# GAME_TEST_QUEUE ARCHIVE 20260907 (LANE-K round `kxpzxi`)

เนื้อใบยกมาคำต่อคำจาก `GAME_TEST_QUEUE.md` ไม่แก้แม้แต่ตัวอักษรเดียว - ในคิวเหลือ stub หนึ่งบรรทัดชี้มาที่นี่

`GT-246` เป็นกรณีพิเศษ: รอบ archive 20260906 เขียน stub ในคิวว่า "verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`" แต่สำเนาในไฟล์นั้นมีแค่หัวใบ (1,283 B) ส่วนเนื้อใบเต็ม (13,926 B) ยังค้างอยู่ในคิว - ไม่มีอะไรสูญหาย เนื้อเต็มถูกยกมาไว้ที่นี่ครบรอบนี้ และ stub ในคิวถูกแก้ให้ชี้มาที่ไฟล์นี้แทน

---

## GT-103 GM-002 COMMAND-WIRE-CAPTURE-MATRIX-001: ล็อกอินด้วยบัญชี GM แล้วหา/เปิด GM editor widget พิมพ์ข้อความหลายแบบ -- capture file ของ `0x51E9` ขึ้นที่ `capture/gm_command_capture/` ไหม (path นี้ live บน production ครั้งแรกรอบนี้)  [NO-RESULT ต่อ claim ของตัวเอง -- A/B ทั้งสี่สถานะ UI เงียบสนิท, blocked on RE-126 · ปิดหัวใบโดย LANE-GM (เจ้าของใบ) รอบ `hs9m2r` 2026-08-28T17:1x+07:00 จากผล attended กะ1-A `notes_to_chief/20260828_1140_GT103AB-RESULT-NEGATIVE-four-ui-states-all-silent-RE118-panel-hypothesis-falsified.md` · OBSERVER_CONFIRMED: 2026-08-28T11:36-11:37+07:00 (BOOT_COMMIT `336857cd` = main HEAD, ไร้แฟล็ก) · เจ้าของคลิก `BT_GM` 4 สถานะ (HUD เปล่า / แผนที่เปิดค้าง / กระเป๋าเปิดค้าง / ปิดกระเป๋าแล้วคลิกซ้ำ) เงียบทุกครั้ง · สำมะโนเฟรมขาเข้าทั้งบูต `0x51E9` = 0 ⇒ `capture/gm_command_capture/` ABSENT ถูกต้องแล้ว ไม่ใช่ teardown fail ⇒ **ใบนี้ไม่เคยไปถึงข้อ 3 จึงไม่มีผลต่อ claim ของตัวเอง** · `TargetPosVital` x3 ช่วงเดียวกัน = client มีชีวิต ไม่ใช่เซสชันตาย · ผลข้างเคียงที่มีค่าสูง: สมมติฐานเชิงปฏิบัติของ RE-118 (เปิด panel ให้ current-UI key ไม่ว่าง) **ถูกหักล้าง** ⇒ เปิด `RE-126` ต่อ (ประตูบานแรก `this+0x48` แทนบานสุดท้าย) · [ไม่อ้าง] ว่า capture path ของ `0x51E9` ใช้ได้หรือไม่ -- ยังไม่เคยถูกทดสอบ live เลย · 🔴 **ทางเลี่ยง:** `GT-127` (คำสั่ง GM ผ่านกล่องแชท `0xAC52`) ไม่ต้องรอใบนี้และไม่ต้องรอ `RE-126`]

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md. grep ยืนยันก่อนจอง: GT-103 = 0 hit ⇒ ใบนี้คือ GT-103 (RE-104
> ถูกใช้แล้วในรอบเดียวกัน โดยใบพี่น้อง). เลขว่างถัดไป = 105. ใบเก่าทุกใบอยู่ที่เดิม ห้ามแตะ.

### ลิงก์ (รายละเอียดเต็มอยู่ที่นี่ ไม่ใช่ในใบนี้)
- wiring/capture path: `notes_to_chief/20260827_1700_CHIEF-REPLY-CORE-REQUEST-010-...md`, `docs/GM_LANE.md`
- widget-trigger: `RE-091` (producer), `RE-104` (open/toggle trigger -- **CLOSED PASS/DONE รอบ `kcm8ir`**,
  `notes_to_chief/20260827_1518_RE-104-RESULT-BT-GM-MODULE-PLUS19-GATE.md`) -- procedure ด้านล่างอัปเดตแล้ว
- บัญชี/config อนุมัติแล้ว (ใช้ซ้ำ): `notes_to_chief/20260827_1200_CHIEF-REPLY-GT101-gm-accounts-test-config-approved.md`
- decode field pin: `RE-088` (positional names only, no semantics)

### objective (claim เดียว)
ส่งข้อความอย่างน้อยหนึ่งครั้งผ่าน GM editor widget ของไคลเอนต์จริงด้วยบัญชี `attended_test` -- ไฟล์ capture
ตรงจำนวน/ตรงชื่อบัญชีปรากฏที่ `capture/gm_command_capture/` (relative กับ CWD ของ server process ตอนบูต)
จริงหรือไม่. ไม่มี reply frame ส่งกลับ (`0x8C77` ยังไม่ต่อสาย) -- ใบนี้ไม่ทดสอบว่าคำสั่งใดทำงาน (GM-003
คนละใบ).

### ด่าน 0 (ใช้ซ้ำ GT-101 ไม่ขอใหม่) / ด่าน 1 (green boot) / ด่าน 2 (grep ยืนยันสาย ที่ `<SHA>` จริง)
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
git grep -n "GM_RUN_GM_COMMAND_VITAL_ID" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "def handle_gm_run_command_vital" <SHA> -- src/pirateforce_foundation/gm/dispatch.py
git grep -n "def capture_raw_gm_command" <SHA> -- src/pirateforce_foundation/gm/command_capture.py
git grep -n "production_allowed = True" <SHA> -- src/pirateforce_foundation/lane_hooks/lane_gm_run_command.py
```
ขาดข้อใดข้อหนึ่ง = BLOCKED (precondition gate) -- ไปทำใบอื่น. (คนละแบบกับ "หา widget ไม่เจอ" ข้างล่าง)

> 🔴 แก้ด่าน 2 เมื่อ 2026-08-28T17:1x+07:00 โดย LANE-GM (เจ้าของใบ) รอบ `hs9m2r` ตามที่กะ1-A รายงานใน
> `notes_to_chief/20260828_1140_GT103AB-RESULT-NEGATIVE-*.md`: บรรทัดเดิม
> `git grep "handle_gm_run_command_vital" -- src/pirateforce_foundation/runtime.py` **ล้าสมัย** -- โค้ด
> ย้ายออกจาก `runtime.py` ไป `lane_hooks/lane_gm_run_command.py` + `gm/dispatch.py` แล้วตั้งแต่ v6.3
> lane_hooks move-out ⇒ ทำตามใบตรง ๆ จะได้ 0 hit และขึ้น **BLOCKED ทั้งที่ของอยู่ครบ** (กะ1-A เจอสด ๆ
> ตอนบูต 11:36 และต้องเปลี่ยนด่านเอง) ชุด 4 บรรทัดข้างบนคือชุดที่กะ1-A รันจริงแล้วผ่านทั้งหมด
> ประวัติเดิมขีดฆ่า ไม่ลบ: บรรทัดที่ถอดออกคือ `git grep -n "handle_gm_run_command_vital" <SHA> --
> src/pirateforce_foundation/runtime.py`

### db / server args
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-103_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt103.sqlite3
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
$env:PF_GM_ACCOUNTS_CONFIG = "<path จากด่าน 0>"
py -3 -u -m pirateforce_foundation.app --db state\run_gt103.sqlite3
```
ไม่มี `--*-scenario`. `--export-events` เป็นแฟล็กเสริมไม่บังคับ (คอนโซลไม่พิมพ์ event นี้ถ้าไม่เติม --
หลักฐานหลักคือไฟล์ capture บนดิสก์เสมอ). เทียบ sha256 canonical กับ `CANON_SHA.txt` ก่อน/หลัง.

### steps (สืบเนื่องจาก GT-101 เซสชันเดียวกันได้ ไม่ต้อง relogin)
1. เข้าเกม, NO-CRASH กวาดกล้อง (เหมือน GT-101 ขั้น 1-3).
2a. **หาปุ่ม `BT_GM` ก่อน** ตาม procedure ที่ `RE-104` พิสูจน์แล้ว (ไม่ใช่การสุ่มอีกต่อไป): หาปุ่ม/control
   resource ชื่อ `BT_GM` ใน notification/system UI (ปุ่มจะแสดง/กดได้ก็ต่อเมื่อสถานะ GM ของ connection ผ่าน
   gate อยู่แล้ว, ไม่ใช่ทุก account) -- ปุ่มนี้เป็นทางเข้าไปยัง panel ชื่อ `GMUI_BASIC` ที่มี tab
   `Radiobutton_Message` (เลือก lane) และช่อง `TextBox_Message` (พิมพ์ข้อความ). RE-104 ไม่ให้พิกัดบนจอ
   (static เท่านั้น) จึงยังต้องหาตำแหน่งจริงด้วยสายตา 1 ครั้ง -- จดตำแหน่ง/รูปร่างที่เจอไว้ด้วย (ภาพนิ่ง)
   เพื่อให้รอบถัดไปไม่ต้องหาอีก.
   - พบ -> ข้อ 2b (A/B ของ `RE-118`).
   - **Bounded fallback ถ้าไม่พบ `BT_GM` ภายใน 5 การลอง** (สั้นกว่าเดิมเพราะตอนนี้รู้ชื่อ resource และ
     เงื่อนไข gate แล้ว ไม่ใช่การสุ่มเปล่า): บันทึก **NO-RESULT (BT_GM control not found/not visible in this
     UI build, bounded exploration)** พร้อมจุดที่มองแล้ว แล้วข้ามไป teardown (ไม่ใช่ FAIL/BLOCKED -- RE-104
     nonclaim ① ไม่ตัดสินว่าบัญชีที่ไม่ใช่ GM หรือ UI build อื่นจะเห็น control นี้หรือไม่) -> จบ (ไม่ทำข้อ 2b/3).
2b. **A/B ของ `RE-118`** (GT-107-R3 พบว่าคลิก `BT_GM` เงียบสนิท -- RE-118 พิสูจน์ static แล้วว่าสาเหตุคือ
   dispatcher ต้องการ current-UI-key ที่ไม่ว่าง ไม่ใช่ field ใหม่บนเฟรม `0x5A19`), ทำต่อจากข้อ 2a ทันที:
   - **(A) ก่อน**: คลิก `BT_GM` จาก HUD เปล่า (ไม่มี panel อื่นเปิดอยู่ก่อนหน้า) แล้วสังเกต -- คาดหมายตาม
     GT-107-R3 เดิม (เงียบ ไม่มีหน้าต่าง).
   - **(B) ต่อ**: เปิด panel อื่นที่รู้ว่าให้ current-UI key ไม่ว่างก่อน (เช่นหน้าต่างแผนที่ M หรือหน้าต่าง
     inventory -- เลือกอันไหนก็ได้ที่เปิดสำเร็จแน่ ๆ) แล้วคลิก `BT_GM` ซ้ำโดยไม่ปิด panel นั้นก่อน.
   - ถ้า (B) เปิด `GMUI_BASIC` ได้: บันทึกว่า panel ไหนทำให้ current-UI key ไม่ว่าง (ภาพนิ่ง) แล้วไปข้อ 3
     ด้วย panel นั้นเปิดค้างไว้เป็นเงื่อนไขก่อน-คลิกเสมอ -- นี่คือ client-observable ใหม่ที่ RE-118 static
     เดาไม่ได้ (ดู RE-118 T4/T5).
   - ถ้า (B) ยังเงียบเหมือน (A): บันทึก **NO-RESULT (A/B ทั้งคู่เงียบ, current-UI-key ยังไม่ nonempty แม้เปิด
     panel)** พร้อม panel ที่ลอง แล้วข้ามไป teardown -- RE-118 BUILD_IMPACT ระบุขั้นต่อไปคือ instrument
     current-key return/create-null โดยสาย RE ไม่ใช่งานฝั่งเทสอีกแล้ว -> จบ (ไม่ทำข้อ 3).
3. ถ้าผ่าน (B) ในข้อ 2b: พิมพ์ 4-8 ข้อความทดสอบ (สั้น/มีอาร์กิวเมนต์/ว่างเปล่า/ยาว+ไทย) กด Enter ทีละอัน
   เว้น 3 วินาที จดเวลาส่งแต่ละอัน (+07:00).
4. ยืนยันจอไม่มีปฏิกิริยาต่อเนื้อหาข้อความ (คาดหมายอยู่แล้ว) -- ถ่ายภาพนิ่งท้ายสุด.
5. NO-CRASH ซ้ำ -> teardown -> เทียบ sha canonical -> ลบสำเนา config/env -> **เก็บทั้งโฟลเดอร์
   `capture/gm_command_capture/` แนบผล**.

### pass criteria (สองชั้น แยกกันเสมอ)
wire/DB: พบ widget+ส่ง N ข้อความ ⇒ `capture/gm_command_capture/` มีไฟล์ `.txt` ใหม่ N ไฟล์ ชื่อมี
`attended_test`/`_0x51E9`, มี header+decode section (FAILED-pin ก็นับเป็นผลถูกต้อง)+hex dump. ไม่พบ widget
(ข้อ 2a) หรือ A/B ทั้งคู่เงียบ (ข้อ 2b, ดู `RE-118`) ⇒ โฟลเดอร์ไม่มีไฟล์ใหม่เลย (ผลลบสมบูรณ์ ไม่ตอบคำถามหลักแต่
ไม่ใช่ FAIL, ทั้งสอง NO-RESULT ชนิดนี้แยกกันตามสาเหตุที่บันทึกในข้อ 2a/2b). sha256 canonical ตรงก่อน/หลัง,
`PRAGMA integrity_check`=ok, raw log/console เก็บครบ.
client-observable: ปกติ**ไม่มีอะไรเปลี่ยนบนจอ**ตอบสนองเนื้อหาคำสั่ง (nonclaim ล่วงหน้า ไม่ใช่ FAIL) --
สิ่งเดียวที่สังเกตคือผลของการสำรวจหา widget เอง (บันทึกทุกจุดที่ลอง+ผล, ถ่ายภาพรูปร่าง/ตำแหน่ง widget ถ้าพบ).
สีป้ายชื่อในภาพ (ถ้าเห็น) บันทึกแบบ "none" ถ้าไม่มี ไม่ชี้สาเหตุ (`RE-067` เปิดอยู่).

### nonclaims
🔴 เก็บข้อมูลดิบ ไม่ใช่พิสูจน์ว่าคำสั่ง GM ทำงาน -- ไม่มี reply frame เลย. 🔴 "หา widget ไม่เจอ" =
NO-RESULT ที่สมบูรณ์ ไม่ใช่ FAIL/BLOCKED (BLOCKED = ด่าน 0/1/2 เท่านั้น). ไม่ตั้ง semantic ให้
`string_0x1c`/`string_0x38`/`field_0x10`/`field_0x14`/`field_0x18` จากสิ่งที่พิมพ์เอง. ไม่ claim ว่า `RE-104`
ถูกตอบแล้ว. ผู้เทสคนเดียว บัญชี GM เดียว เซสชันเดียว (ต่อจาก GT-101 ได้). สำเนา config ลบทิ้งตอน teardown.
ไม่ชี้สาเหตุสีป้ายชื่อ. NO-RESULT ของขั้น 2 จ. ไม่แยก "widget ไม่มีจริง" จาก "รายการที่ลองผิดตัว" -- อาศัย
บันทึกรายการที่ลองครบ (steps) ให้รอบถัดไปแยกเอง.

---

---

## GT-107 GM-001-R2 LOGIN-STATE-VISUAL-PROBE-002: ล็อกอินด้วยบัญชี GM อีกครั้งหลัง RE-105 พิน vital_version=0 (CORE-REQUEST-016 เปิดแล้ว) -- เซสชันรอดจาก error 23065 ที่ GT-101 เจอไหม แล้วจอเปลี่ยนอะไรไหม (คำถามเดิมของ GT-101 ที่ยังไม่มีใครตอบได้เพราะเซสชันตายก่อนถึง)  [RESULT -- NEGATIVE, new failure mode, error 28317, see notes_to_chief/20260827_1745_GT107-RESULT-NEGATIVE-vital-version-0-passes-version-check-but-client-throws-28317-RunTimeProtocolRes-read-failed-session-dies-GT103-not-reached-ka1-B.md -- superseded by GT-107-R3 below]

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md. grep ยืนยันก่อนจอง (2026-08-27): GT-107 = 0 hit, RE-107 = 0
> hit ทั้งสองไฟล์ (รวม archive/). เลขสูงสุดที่ใช้แล้วจริงคือ GT-106 (SCENE17-PROVISIONAL-ARRIVAL-001, เปิดโดย
> chief รอบ e0daaa) และ RE-106 (QUEST-FLAG-SYNC-MECHANISM-001, เปิดโดย chief คนละสาย) -- ทั้งสองใบไม่ว่าง ⇒
> 106 ใช้ไม่ได้ ใบนี้คือ 107. เปิดโดย pf-queue-author ตามคำขอ LANE-GM รอบ kcm8ir. ใบเก่าทุกใบอยู่ที่เดิม ห้ามแตะ.

### ที่มา -- อ่านจากซอร์สจริง ห้าม re-derive ระหว่างรอบ
- `GT-101` เอง (ผลจริง `notes_to_chief/20260827_1445_GT101-RESULT-client-rejects-0x5A19-version-1-error-23065-session-killed.md`,
  OBSERVER_CONFIRMED 2026-08-27T14:39+07:00): ส่ง `GM_UpdateGMStateVital` (`0x5A19`) ด้วย `vital_version=1`
  ทำให้ไคลเอนต์ขึ้น modal error "網路 VitalData 版本不對 --- ErrorData=23065" (23065 = 0x5A19) แล้วหยุดรับ
  ข้อมูล/ปิด socket เอง -- **ฆ่าเซสชันของเจ้าของเอง** ก่อนที่คำถามเดิมของ GM-001 ("จอเปลี่ยนอะไรไหม") จะถูกตอบ.
- `RE-105-RESULT` (`notes_to_chief/20260827_1613_RE-105-RESULT-VITAL-VERSION-ZERO-GENERIC-MISMATCH-PATH.md`,
  STATIC-ON-BRIDGE, DONE/PASS): generic VitalData collection reader `[0x005F3E20,0x005F406D)` เทียบ nested
  version แบบ exact-equality กับ `message+0x10`; bootstrap ของ `0x5A19` เอง (`0x007299B0`) เซ็ตค่านั้นเป็น `0`
  โดยตรง (`mov byte ptr [eax+0x10],bl` หลัง `xor ebx,ebx`) -- **`vital_version` ที่ถูกคือ `0` เท่านั้น**, ค่า `1`
  ที่ GT-101 วัดว่าฆ่าเซสชันคือค่าที่ตกทาง mismatch เดียวกันนี้เอง. `08 04` (outer `GSCN_RunTimeProtocolRes`
  protocol version 4) เป็นคนละฟิลด์ ไม่เกี่ยวกับสาเหตุ.
- รอบ `kcm8ir` (`archive/rounds_2026-08-27_to_28/GM_20260827_1614_re105-vital-version-pin-plus-re104-widget-trigger-close.md`):
  `src/pirateforce_foundation/gm/state_wire.py`'s `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED` เปลี่ยนจาก `None`
  เป็น `0` จุดเดียว -- **ไม่แตะ `runtime.py`** เพราะ guard ของ `CORE-REQUEST-016` (`runtime.py`, เงื่อนไข
  `is_gm and state_wire.GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED is not None`) เปิดเองทันทีที่ค่านี้ไม่ใช่
  `None` อีกต่อไป. เทสใหม่ `tests/test_gm_login_state_guard.py` (`GmLoginStateGuardTests`, 3 เทส) ยืนยันผ่าน
  headless dispatcher จริงว่าเฟรมที่ประกอบมี `b"\x12\x19\x5a\x0b\x00"` (ไบต์เดียวที่ GT-101 พิสูจน์ว่าฆ่าเซสชัน
  ตอนเป็น `0B 01`) และไม่มี `b"\x12\x19\x5a\x0b\x01"` เลย, `08 04` (outer protocol version) ไม่เปลี่ยน, บัญชี
  ไม่ใช่ GM ไม่ได้รับผลกระทบ, และ guard เป็นเงื่อนไขจริง (patch ค่ากลับ `None` แล้วเฟรมถูก withhold เหมือนเดิม
  ด้วย event `gm_update_state_frame_withheld_no_confirmed_vital_version_re105_open`). `tests/test_gm_*.py`
  206/206 ผ่าน, repo เต็ม (`unittest discover`) 3565 เทส ผ่านหมดยกเว้น 18 error เดิมจาก `capstone` import ที่
  ไม่เกี่ยวกับสายนี้ (baseline เดิม ไม่ใช่ของรอบนี้).
- `RE-104-RESULT` (`notes_to_chief/20260827_1518_RE-104-RESULT-BT-GM-MODULE-PLUS19-GATE.md`, PASS/DONE):
  พิสูจน์ trigger ของ dedicated GM editor widget (ปุ่ม `BT_GM` → panel `GMUI_BASIC`) -- **คนละคำถามกับใบนี้**
  ใบนี้ไม่เปิด/ทดสอบ widget นั้นเลย (นั่นคือขอบเขตของ `GT-103` ที่อัปเดตแล้วแยกต่างหาก).
- 🔴 **ใบนี้คือ byte-level regression check ของ GT-101 เท่านั้น ไม่ใช่การสำรวจใหม่.** RE-105/เทสใหม่พิสูจน์แค่
  ระดับ headless dispatcher -- **เวอร์ชัน 0 ไม่เคยถูกยิงใส่ไคลเอนต์จริงเลยสักครั้ง** (คำของ LANE-GM STATUS เอง,
  `notes_to_chief/20260827_1614_LANE-GM-STATUS-re104-re105-closed-vital-version-pinned.md` §"เกณฑ์สองชั้น":
  wire/DB = PASS headless, client-observable = ยังไม่มี). ใบนี้คือก้าวที่ปิดช่องว่างนั้น.

### ก่อนบูต -- ด่าน 0 (ชื่อบัญชี GM -- ห้ามเดา, สองแหล่งขัดกัน ต้องถามก่อน), ด่าน 1 (green boot), ด่าน 2 (grep ยืนยันสาย)

**ด่าน 0 -- ชื่อบัญชี:** สองแหล่งไม่ตรงกัน ใบนี้ไม่เลือกแทน:
  (A) `notes_to_chief/20260827_1200_CHIEF-REPLY-GT101-gm-accounts-test-config-approved.md` -- chief อนุมัติ
      ชื่อ **`attended_test`** (ชื่อ fixture ใน `tests/test_gm_accounts.py` เท่านั้น).
  (B) `GT-101` เอง (ผลจริง, บูต `2217fa47`): `attended_test` ใช้ไม่ได้จริง (ไม่มี client login ตัวไหนส่งชื่อนี้
      ⇒ `is_gm_account()` คืน `False` เสมอ) -- รอบนั้นใช้ **`localtest`** จริง (บัญชีจริงในตาราง `accounts` ที่มี
      ตัวละคร `Arena01`) แล้ว `is_gm_account("localtest")` คืน `True` จริง เฟรมถูกคิวจริง. ผลของ GT-101 เองเขียน
      ไว้ตรง ๆ ว่า chief ควรแก้จดหมาย `1200` -- **แต่ ณ ตอนเขียนใบนี้ยังไม่มีจดหมายแก้ไขอย่างเป็นทางการ** (จดหมาย
      เป็นบันทึกจุดเวลา ไม่ถูกแก้ย้อนหลังตามธรรมเนียมของคิวนี้).
  **ก่อนบูต ต้องถาม chief/เจ้าของตรง ๆ ว่ารอบนี้จะใช้ชื่อไหน** -- ถ้าไม่มีคำตอบใหม่ให้ยึด (B) เพราะเป็นชื่อบัญชี
  จริงเพียงชื่อเดียวที่พิสูจน์แล้วว่า login ได้จริงและติด GM gate จริง (แนบเหตุผลนี้ไปกับคำถามที่ถาม ไม่ตัดสินใจ
  เงียบ ๆ). config เดิมของ GT-101 ถูกลบทิ้งไปแล้วตอน teardown -- ต้องสร้างสำเนาใหม่เสมอ ไม่มีของเก่าให้ใช้ซ้ำ:
  ```
  '{"gm_accounts": ["<ชื่อที่ยืนยันแล้ว>"]}' | Set-Content pf_bridge\backup\gm_accounts_GT-107_<yyyyMMdd_HHmmss>.json
  ```
  **ห้ามแก้ `config/gm_accounts.json` ตัวจริง** -- ใช้ `$env:PF_GM_ACCOUNTS_CONFIG` ชี้ไปที่สำเนาเสมอ (ทาง B เดิม
  ของ GT-101, `gm/accounts.py`'s `ENV_OVERRIDE`). จดชื่อบัญชีที่ยืนยัน + path สำเนาไว้ในผลตั้งแต่ต้น ลบสำเนา/
  เลิกตั้ง env ตอน teardown.

**ด่าน 1 -- resolve commit เขียว:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
รันจากโฟลเดอร์ pf_bridge, exit 0 + `BOOT_COMMIT: <sha>` เท่านั้นถึงบูตได้ (git checkout `<sha>` แบบ detached
HEAD). ห้ามเทียบเลข commit ด้วยตา -- resolver คืนหัวแบรนช์ที่ผ่านเกต ไม่ใช่ merge commit เสมอไป.

**ด่าน 2 -- ยืนยันสายจริงของ `<SHA>` (ห้ามเชื่อเลขบรรทัด/ไบต์ในเอกสารนี้ ต้อง grep ของจริงเสมอ):**
```
git grep -n "GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED = 0" <SHA> -- src/pirateforce_foundation/gm/state_wire.py
git grep -n "state_wire.GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "gm_update_state_frame_withheld_no_confirmed_" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "make_gm_update_state_frame" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "is_gm_account(self.token)" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "test_a_gm_account_gets_the_re105_pinned_state_frame" <SHA> -- tests/test_gm_login_state_guard.py
```
ต้องได้อย่างน้อย 1 บรรทัดต่อคำสั่งทั้ง 6 คำสั่ง, และบรรทัดแรกต้องคืน `= 0` ตรงตัว (ไม่ใช่ `= None`) -- ถ้าเป็น
`None` แปลว่าคอมมิตที่จะบูตยังไม่มีการแก้จริง = **BLOCKED**, ห้ามบูต, ไปทำใบอื่นแล้วรอ merge.

### db (สำเนาเสมอ ห้ามเปิด canonical, ห้ามแตะ state\play.sqlite3)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-107_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt107.sqlite3
```
เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง. สำเนาใหม่ทุกบูต ⇒
ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดเสมอ (คาดหมายอยู่แล้ว ไม่ใช่ผลของใบนี้).

### server args (เป๊ะ -- ไม่มี --*-scenario, guard ทำงานเสมอไม่มีสวิตช์, ไม่มี chat trigger ในใบนี้เลย)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
$env:PF_GM_ACCOUNTS_CONFIG = "<path จากด่าน 0>"
py -3 -u -m pirateforce_foundation.app --db state\run_gt107.sqlite3
```

### steps (คลิกต่อคลิก -- อัดวิดีโอต่อเนื่องตลอดช่วงถือ LOCK_GAME)
ก่อนเริ่ม: ถือ LOCK_GAME, สำรอง state (บล็อก db ด้านบน), จด boot stamp (+07:00, ต้องไม่เก่ากว่า 420 นาทีตอนรัน
teardown), เทียบ sha canonical, ยืนยันด่าน 0-2 ผ่านครบ (จดชื่อบัญชี + path config + SHA ที่บูต).
🔴 **เตรียมใจไว้ก่อนคลิกเข้าเกม: modal error 23065 เดิมของ GT-101 อาจเกิดซ้ำได้จริง** ถ้า RE-105/การแก้รอบนี้ผิด
ที่ใดก็ตาม -- นี่ไม่ใช่ FAIL ของใบนี้ เป็นผลลบที่มีค่าเท่ากับผลบวก (ดู pass criteria). ถ้าเกิดซ้ำ: กด OK ปิด
dialog ตามปกติ, **restart server ก่อนเปิด client ใหม่เสมอ** (server ถือ session ค้าง ⇒ client ตัวถัดไปค้างที่
"connecting" ตลอดกาลถ้าไม่ restart ก่อน), แล้วหยุดที่ตรงนั้น เขียนผลแบบ RESULT เหมือน GT-101 ไม่ต้องพยายามต่อ.

1. สตาร์ตเซิร์ฟเวอร์ก่อนเสมอ (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client).
   client ที่บูตโดยไม่มีเซิร์ฟเวอร์ตายเองใน ~3.5 นาที.
2. เปิด client -> เลือกเซิร์ฟเวอร์ -> dialog PVP ปุ่มซ้าย -> หน้าเลือกตัวละคร -> เลือกช่องแรกของบัญชี GM ที่
   ยืนยันในด่าน 0 -> ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม (ปุ่มซ้ายสุด = ลบตัวละคร ห้ามกด). เริ่มอัดวิดีโอ
   ต่อเนื่องตั้งแต่ก่อนกดเข้าเกม.
3. **ด่านชี้ขาดของใบนี้ (ใหม่ ไม่มีใน GT-101):** จ้องจอตั้งแต่วินาทีที่หน้าโหลดจบทันที 10 วินาทีเต็มก่อนทำอะไร
   ต่อ -- มี modal error กลางจอ (ข้อความจีนขึ้นต้น "網路 VitalData") ขึ้นไหม. ถ่ายภาพนิ่ง full-res ทันทีถ้าเห็น.
   ขึ้น -> ทำตามคำเตือนด้านบน (restart server, เขียนผล RESULT, จบใบ). ไม่ขึ้น -> ไปข้อ 4 เหมือน GT-101 เดิม.
4. T0 -- เห็น HP bar/minimap/ชื่อแมพครบ. จด HUD X/Y. คลิกขวาค้างลากกวาดกล้อง 360 องศาหนึ่งรอบ (ตัวเช็ค NO-CRASH
   ตัวเดียวที่ใบนี้ยอมรับ -- **ห้ามใช้ Q/E เด็ดขาด** เพราะ Q/E หันตัวละครจริงและยิง `TargetPosVital`; คลิกขวาลาก
   หมุนกล้องอย่างเดียว ทิศหันตัวละครไม่ขยับ ไม่ยิงอะไรออกสาย ปลอดภัยเสมอ). ใบนี้ไม่มีขั้นเดิน/โจมตี/trigger ใด ๆ
   เลย ⇒ ไม่จำเป็นต้องใช้ W/A/S/D หรือ Q/E ตลอดรอบ.
5. เฝ้าจอต่อเนื่องอย่างน้อย 5 นาทีนับจาก T0 (โปรโตคอลเดิมของ GT-101 ทั้งหมด) -- ถ่ายภาพนิ่ง full-res ที่ t=0s,
   30s, 120s, 300s เป็นอย่างน้อย และเพิ่มทันทีที่เห็นอะไรเปลี่ยนแม้เล็กน้อย. กวาดตาดูทุกจุด: ป้ายชื่อเหนือหัว
   ตัวเอง, แผงสถานะ/HP มุมซ้าย, แผงเป้า (ถ้ามี), หน้าต่างแชท+prefix ชื่อตัวเอง, แถบไอคอน/เมนูบนสุด, minimap,
   มุมจอทุกมุม.
6. คู่ขนานกับข้อ 5: เฝ้าคอนโซลเซิร์ฟเวอร์ -- คัด `[G>] GM_UPDATE_STATE_AFTER_LOGIN`, `gm_account_lookup_failed_*`
   (ถ้ามี = config พัง, หยุดแล้วเขียน BLOCKED ไม่ใช่ NO-RESULT), และเช็คว่าไม่มี `[G!] game socket closed/reset`
   โผล่ก่อนครบ 5 นาที.
7. ครบ 5 นาทีแล้ว: คลิกขวาลากอีกครั้ง (NO-CRASH ซ้ำ) -- ยืนยันไคลเอนต์ยังตอบสนอง.
8. ออกเกม -> teardown ตาม `TEMPLATE_teardown_generic.ps1` -> เทียบ sha canonical รอบสุดท้าย -> ลบสำเนา config/
   เลิกตั้ง `$env:PF_GM_ACCOUNTS_CONFIG`.

### pass criteria (สองชั้น แยกกันเสมอ ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)

ชั้น wire/DB (อ่านจาก server console/event log ล้วน ๆ ไม่ต้องพึ่งสิ่งที่เห็นบนจอ):
- คอนโซลพิมพ์ `[G>] GM_UPDATE_STATE_AFTER_LOGIN (N bytes)` หนึ่งครั้งตอนล็อกอินสำเร็จ, ไม่มี
  `gm_account_lookup_failed_*` เลย.
- 🔮 **คำทำนาย (ยังไม่เคยยิงใส่ไคลเอนต์จริง, ผิดได้ = ผล ไม่ใช่ความล้มเหลว):** ไบต์บนสายของเฟรมนี้ตรง
  `... 08 04 0B 02 12 01 00 12 19 5A 0B 00 0B 00 0B 00 14 00 00 00 00` (เหมือนไบต์จริงที่ GT-101 จับได้เป๊ะ
  ยกเว้นไบต์เดียวหลัง `12 19 5A` เปลี่ยนจาก `0B 01` เป็น `0B 00` ตามที่ RE-105/เทส `test_gm_login_state_guard.py`
  พิสูจน์แล้วที่ชั้น headless) -- ถ้าคอนโซลมี hex dump ให้เทียบตรงนี้, ถ้าไม่มีก็ข้ามข้อนี้ไปดูแค่ N bytes.
- ไม่มีบรรทัด `[G!] game socket closed/reset` โผล่ก่อนครบ 5 นาทีจาก T0 (สัญญาณทางสาย ทางอ้อม ของการที่ session
  ไม่ตายกลางคัน -- แยกจากการเห็น modal บนจอ ซึ่งเป็นชั้น client-observable คนละชั้น).
- `sessions`: `count(*) WHERE selected_character_id IS NOT NULL` +1 ต่อการเข้าเกมหนึ่งครั้ง, `max(lease_
  generation)` ไม่ถอยหลัง, `PRAGMA integrity_check` = `ok` บนสำเนา, sha256 canonical ก่อน-หลังตรงกับ
  `CANON_SHA.txt` ทั้งสองครั้ง.
- raw GAME log ทั้งไฟล์ + console out/err เก็บทั้งก่อน/หลัง ไม่ตัดทอน.

ชั้น client-observable (ต้องมีคนหน้าจอ, ห้ามอนุมานจากบรรทัดคอนโซล):
- 🔴 **สามผลลัพธ์ต่อไปนี้ทุกอันมีค่าเท่ากัน ไม่ใช่เกณฑ์ผ่าน/ตกของใบนี้ (เหมือน GT-101 บวกผลที่สาม):**
  (ก) **modal error 23065 เดิมขึ้นซ้ำ** -- แปลว่า RE-105/การแก้รอบนี้ยังไม่ปิดสาเหตุจริงบนไคลเอนต์ตัวนี้ ทั้งที่
      headless พิสูจน์แล้ว เขียนเป็นผล RESULT (ไม่ใช่ PASS ไม่ใช่ FAIL) พร้อมภาพ+ไบต์จริงที่จับได้ ตามแบบผลของ
      GT-101 เอง.
  (ข) **ไม่มี modal, login ผ่านปกติ, ไม่เห็นอะไรเปลี่ยนบนจอเลย** ตลอด 5 นาที -- นี่คือผลลบที่ `RE-089` ทำนายไว้
      แล้วว่าเป็นไปได้ (ไม่พบ render/UI consumer ที่ชั้น static) เขียนเป็นผลลบเต็มรูปพร้อมรายการทุกจุดที่ตรวจ
      แล้วว่า "ไม่เปลี่ยน".
  (ค) **ไม่มี modal, login ผ่านปกติ, เห็นอะไรเปลี่ยนจริง** -- ระบุให้ชัดว่าที่ไหน ถ่ายภาพนิ่ง full-res ปิดล้อม
      จุดที่เปลี่ยนทันที -- นี่คือผลบวกที่ตอบคำถามค้างของ `RE-089`/`GT-101` ได้จริงเป็นครั้งแรก.
- สีของป้ายชื่อทุกป้ายในทุกภาพนิ่ง full-res (t=0s/30s/120s/300s และภาพเพิ่มถ้ามี) บันทึกเป็นบรรทัดเดียวต่อป้าย
  ต่อภาพ ("none" เขียนออกมาถ้าไม่มี ห้ามเว้นว่าง) -- อ่านจากภาพนิ่ง full-res เท่านั้น ห้ามอ่านจาก contact
  sheet/ภาพย่อ/วิดีโอ ห้ามอนุมานสาเหตุของสี (`RE-067` เปิดอยู่). ไม่มีภาพอ้างอิงของเซิร์ฟเวอร์ต้นฉบับสำหรับ GM
  state โดยเฉพาะที่รู้จักตอนนี้ -- ถ้าไม่มีอ้างอิงให้ใช้ `compared_and_matched=no-reference`.

### nonclaims
- 🔴 **ใบนี้เป็น byte-level regression check ของ GT-101 เท่านั้น ไม่ใช่การสำรวจ/ค้นใหม่.** ไม่ทดสอบค่าอื่นของ
  สามฟิลด์ opaque (ยังส่ง `0, 0, 0` ชุดเดิมเหมือน GT-101 เป๊ะ ๆ) และไม่ตั้ง semantic ให้ไบต์ไหนจากสิ่งที่เห็น
  บนจอ (`RE-089` ห้ามการอนุมานนี้จาก offset/ความกว้างไว้แล้ว).
- 🔴 **ใบนี้ไม่พิสูจน์ว่าการแก้ของ RE-105/CORE-REQUEST-016 ถูกต้องที่ชั้นไคลเอนต์จริง** -- headless test พิสูจน์
  แค่ว่า dispatcher ประกอบไบต์ที่ตั้งใจถูกต้อง; **ใบนี้คือรอบแรกที่วัดจริงว่าไคลเอนต์ตัวจริงยอมรับหรือไม่** ถ้า
  modal เดิมขึ้นซ้ำ (ผลลัพธ์ (ก) ข้างบน) นั่นคือคำตอบของใบนี้เอง ไม่ใช่ความล้มเหลวของใบนี้.
- 🔴 **"ไม่เห็นอะไรเปลี่ยนบนจอเลย" (ผลลัพธ์ (ข)) เป็นผลที่คาดไว้แล้วและยอมรับได้เต็มรูป ไม่ใช่ความล้มเหลวของ
  ใบนี้** -- `RE-089` เองพิสูจน์แล้วว่าไม่พบ render/widget/texture consumer ของสามฟิลด์นี้ในโค้ด static ก่อน
  รอบนี้จะเริ่มด้วยซ้ำ.
- ไม่ทดสอบ GM editor widget (`BT_GM`/`GMUI_BASIC`) หรือคำสั่ง GM ใด ๆ เลย -- นั่นคือขอบเขตของ `GT-103`
  (GM-002) คนละใบ, ไม่มีการยิงคำสั่งในใบนี้.
- ไม่ทดสอบผู้เล่นคนอื่นเห็นอะไรต่างไปเกี่ยวกับบัญชี GM นี้, ไม่ทดสอบความเสถียรข้าม reconnect/relogin -- ล็อกอิน
  ครั้งเดียวในรอบนี้.
- ถ้าใช้สำเนา config ตามด่าน 0: ไม่พิสูจน์ว่าการเปลี่ยนแปลงนั้นคงอยู่ข้ามรอบอื่นหรือกระทบเลนอื่น -- สำเนานี้ของ
  รอบนี้เท่านั้น ถูกลบทิ้งตอน teardown.
- ไม่ชี้สาเหตุของสีป้ายชื่อ (`RE-067` เปิดอยู่).
- ถ้าด่าน 0/1/2 ไปไม่ถึง (ยังไม่ merge/BLOCKED/ไม่มีคำตอบชื่อบัญชี) => ทั้งใบเป็น BLOCKED ไม่ใช่ NO-RESULT/FAIL
  -- ยังไม่ได้ล็อกอินเลย.

### result (ผู้เทสกรอก)
```

```

---

---

## 🆕🔬 GT-159 M2-DEST-COLUMBUS-MARKER17-TRANSFORM-TO-SHIP-001 [attended, in-game]: ถ้าเซิร์ฟเวอร์เคยส่งฉาก 126 ที่ `MARKER[17]` พิกัด `(3050, 232, 90)` หันหน้า 6 แทนฉาก 17 -- ผู้เล่น**แปลงร่างเป็นเรือและอยู่ในทะเล**ตามที่เจ้าของจำได้ (`GT-106` ข้อ ④.2) จริงหรือไม่ -- ตัดสินด้วยตา ไม่ใช่ด้วยการเถียงตาราง  [⚪ **CANCELLED - covered by `GT-266` · no longer needs proving because `PANYA-DECISION 20260905_1329`** -- ปิดโดย chief (LANE-E) รอบ `m8wtlr`/R356 2026-09-05T17:0x+07:00 ตาม `COO-DECISION 20260905_1543` — ประวัติ/เหตุผลเต็มของหัวใบเดิม (รวมข้อความ `~~BLOCKED~~` เก่าที่ถอนแล้ว ซึ่งทำให้เครื่องมือ regex อ่านใบนี้กลับเป็น BLOCKED ผิด ตาม chief `R374` ข้อ 2) ย้ายไปบรรทัด "ประวัติหัวใบเดิมคำต่อคำ" ถัดไปคำต่อคำ ไม่แก้เนื้อหา [จัดรูปแบบโดย LANE-K รอบ `x91eo8r2` — ยืนยันแล้วว่า `COO-DECISION 20260905_1543` ตัดสิน CANCELLED นี้ไว้แล้วจริง (`grep -rl "GT-159" notes_to_chief/*COO-DECISION*` เจอฉบับนี้ตรง ๆ — รอบ `x91eo8` ก่อนหน้ารายงานผิดว่า "0 hit", แก้ไขแล้วในจดหมายรอบนี้)]]

> **ประวัติหัวใบเดิมคำต่อคำ (ก่อนจัดรูปแบบรอบ `x91eo8r2`)**: **สองครึ่งของใบตายคนละทาง**: (ก) ครึ่ง "มาถึง 126 ที่ MARKER 17 (3050,232,90) แล้วเป็นเรือในทะเลจริงไหม" = `GT-266` วัดตรงตัว (จุดมาถึงเดียวกัน วัตถุที่ต้องเห็นเดียวกัน · กลไกขนส่งต่างกันไม่เปลี่ยนสิ่งที่ตาเห็น) · (ข) ครึ่ง "`DESTINATION_SCENE_N_ID = 17` อ่านใน id space ไหน" = **ไม่ต้องพิสูจน์แล้ว** เพราะ `PANYA-DECISION 20260905_1329` เคาะจุดมาถึง 126 = MARKER `n_ID 17` ถาวร — คำถาม id space ตายด้วยคำสั่ง ไม่ใช่ด้วยการเทส · 🔴 **สิ่งที่ยังไม่ถูกตอบและห้ามผูกกับใบนี้อีก**: Columbus ยังชี้ฉาก 17 บน main (`world_m2_sea_destination.py:314`) — เมื่อ LANE-A แก้ปลายทาง Columbus → 126 เป็น PR จริง **ใบ GT ของ PR นั้นออกใหม่ตอนนั้น** ไม่ใช่เก็บใบนี้รอ (`COO 1543` ข้อ 3 · เวลา attended แพงที่สุด `PANYA 20260903_1934`) · ~~🔴 BLOCKED (คงเดิม) -- การปิดใบของ chief รอบ `r045nx`/R354 ถูกถอน ในรอบเดียวกันหลัง `pf-adversary` D4 · ใบนี้ยังไม่ปิด และรอ COO ตัดสิน~~ **COO ตัดสินแล้ว `1543`**
> 🔴 **ที่ถอนและทำไม (chief เขียนเอง ไม่ใช่ให้ใครมาจับได้ทีหลัง)**: `COO-DECISION 20260905_1349` ข้อ 5 ให้ทางเลือกสองทางเท่านั้น — "ถ้าใช่ปิดด้วย `CANCELLED - covered by <GT ใหม่>` **ถ้าไม่ ระบุว่าต่างตรงไหน (สั้น)**" · chief สรุปเองว่าใบ `/warp 126` ใหม่ (`GT-266`) **ไม่ครอบ** ใบนี้ = ตกเข้าทาง "ถ้าไม่" ซึ่งอนุญาตแค่ให้**เขียนความต่าง** แต่ chief กลับปิดใบด้วยตัวครอบที่ COO ไม่ได้เอ่ยถึงเลย ⇒ **เกินอำนาจ** และขัดบรรทัดในหัวใบนี้เอง ("ห้ามปิดเองจนกว่า COO ตัดสิน" · `PANYA-DECISION 20260903_1934`)
> 🔴 **และข้ออ้างที่ใช้ปิดก็เกินจริง**: คำถามของใบนี้ไม่ใช่ "ฉาก 126 เป็นทะเลไหม" แต่คือ **กด Columbus (quest 3021) บนเซิร์ฟเวอร์ที่ถูกแก้ให้ส่ง 126@`MARKER[17]` แทน 17 แล้วเกิดอะไร** — เพื่อแยกสอง id space ที่ `world_m2_sea_destination.py:305-314` ประกาศเองว่า `[CONTESTED]` และ "no control in any table separates them" · บูตของ `GT-233` ทุกครั้งเข้าฉาก 126 ผ่าน `PF_M2_SURVEY_TRIAL` + relogin **ไม่เคยแตะ `columbus_quest_dispatch` หรือแถว 3021 เลย** ⇒ ไม่แยก id space ให้สักนิด · กิ่งผลลบของใบ ("ยังเป็นคน ไม่ได้อยู่ในทะเล เช่นยืนอยู่ฉาก 17") ไม่มีใครเคยเห็น
> 🔴 **และป้าย `OBSERVER_CONFIRMED 12:48` ถูกยืมผิดที่**: ใน R318 §2.2 ป้ายนั้นเซ็นประโยค "**ไม่มีหน้าต่างอะไรเด้ง**" (ผลลบของ `GT-233`) ส่วน "เป็นเรือ" อยู่ในย่อหน้าเดียวกันแบบ**ไม่มีลายเซ็น** ("`HP -1/1` ขณะเป็นเรือ (สังเกตการณ์)") — ย้ายป้ายข้ามข้ออ้างแบบนี้ผิด `G-OBS`/`G5` ตรง ๆ
> ⇒ **ที่ chief ทำได้ตามอำนาจจริงคือบรรทัดเดียวนี้**: `GT-266` (`/warp 126` สด) **ไม่ครอบ** ใบนี้ — `GT-266` ถามว่า "วาปสดขณะเล่นไปโผล่ 126 ได้ไหมโดยไม่ relogin" ส่วนใบนี้ถามว่า "`DESTINATION_SCENE_N_ID = 17` อ่านใน id space ไหน" ซึ่งต้องกด Columbus บนบิลด์ที่แก้ปลายทาง · **เสนอ COO: ใบนี้ยังจำเป็นหรือไม่ ในเมื่อกลไก M2 ที่เดินอยู่จริงคือ `RE-227`/`GT-233` ไม่ใช่การสลับปลายทางของ Columbus** — คำตอบเป็นของ COO ไม่ใช่ของ chief
> เดิม (ถอนแล้ว ไม่ลบเพื่อเป็นประวัติ): ~~`CANCELLED - covered by GT-233 boots R313/R315/R317/R318`~~
> เดิม: 🔴 **BLOCKED** · `STATUS-SET-BY-CHIEF 2026-09-05T02:0x+07:00 from body` ตาม `COO-DECISION 20260904_2349` ข้อ 6]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง 2026-08-30T14:2x+07:00: `GT-159`/`RE-159` = 0 hit ทั้งสองไฟล์ ·
> สูงสุดก่อนหน้า `GT-158` (`GT`/`RE` ใช้ตัวนับเดียวร่วมกัน ตามกฎที่ `RE-152` หัวใบเคยระบุไว้)
> ⇒ ใบนี้คือ `GT-159` · ใบ `RE-085`-`RE-158`/`GT-001`-`GT-158` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ

### ที่มา

`COO-DECISION 20260830_1351 (m2-destination-held-at-17-escalated-to-owner)` สั่งให้ LANE-A
"รันการทดสอบเชิงสังเกตที่เสนอไว้ก่อน (ฉาก 126 ที่พิกัด marker แปลงร่างเป็นเรือจริงหรือไม่) แล้วค่อยเอาผล
ไปให้เจ้าของตัดสิน" -- ทางเลือกที่ 3 ของใบ `20260829_1410_LANE-A-ASK-COO-var2-is-a-markerid.md` เอง คือ
ใบเทสนี้ ไม่ใช่การแก้โค้ด: คำถามที่เหลือ (17 หรือ 126 คือปลายทางจริงของ M2) เป็นคำถาม client-observable
ล้วน (สองการอ่านตารางให้คำตอบต่างกัน ทั้งคู่วัดได้เท่ากันจากซอร์ส) ไม่มีทางปิดได้ด้วย static อีกต่อไป

`world_m2_sea_destination.DESTINATION_SCENE_N_ID` ยังเป็น `17` บน `main` วันนี้ (production path ไม่มี
แฟล็ก) แท็ก `[CONTESTED]` ติดไว้ที่ docstring/console token (`var2_reading=CONTESTED`) ตั้งแต่รอบ `drrnpu`
-- ใบนี้ไม่แตะโค้ดนั้น เป็นใบสังเกตการณ์ล้วน

### objective

ให้ผู้เทสยืนที่ Port Royal กด Columbus (option แรก, quest 3021) **ด้วยเซิร์ฟเวอร์ที่ถูกแก้ให้ส่งฉาก 126
ที่พิกัด `(3050, 232, 90)` หันหน้า 6 แทนฉาก 17 ชั่วคราว** (เปลี่ยนที่เดียว:
`world_m2_sea_destination.DESTINATION_SCENE_N_ID = 126` + จุดพิกัด -- ทำใน branch ทดลองแยก ไม่ใช่ `main`,
ไม่ commit ค่านี้ทับของจริง) แล้วสังเกตว่าไคลเอนต์:

1. แปลงร่างตัวละครเป็นเรือหรือไม่ (โมเดล/แอนิเมชันเปลี่ยนจากคนเป็นเรือ)
2. พื้นที่รอบตัวเป็นทะเล/มหาสมุทรหรือไม่ (ไม่ใช่เกาะ/ท่าเรือ)
3. HUD/ชื่อแมพที่ขึ้น ตรงกับ "Atlantic Ocean: Rising Sun Sea" หรือชื่อพาแนลทะเลที่โฆษณาไว้หรือไม่

### pass criteria

**ชั้น client-observable (ปิดคำถามได้ชั้นเดียวพอ เพราะเป็นคำถาม client-observable ล้วนตามที่เจ้าของ
เคยอธิบายไว้ใน `GT-106` ข้อ ④.2):**
- ตัวละครแปลงร่างเป็นเรือจริงและอยู่ในทะเล ⇒ การอ่านแบบ **marker (126)** ถูก -- ส่งผลให้ `COO-DECISION`
  ต้องพิจารณากลับคำ `DESTINATION_SCENE_N_ID` เป็น `MARKER[17].n_SCENE` (126) ในรอบถัดไป
- ตัวละครไม่แปลงร่าง ยังเป็นคน ไม่อยู่ในทะเล (เช่น ยืนอยู่บนฉาก 17 ที่ไม่ใช่ทะเล) ⇒ การอ่านแบบ
  **scene table (17)** ถูก -- ยืนตามใบ `0441`/`main` ปัจจุบันต่อไป

### nonclaims

1. ไม่อ้างว่าใบนี้ปลดล็อก M2 ทันที -- ใบนี้ตอบแค่ "17 หรือ 126" หนึ่งคำถาม การเดินสายจริงเข้า `main`
   (ถ้าคำตอบคือ 126) เป็นงานร่วมของ chief + สาย A รอบถัดไปตามที่ใบ `var2-is-a-markerid` เขียนไว้แล้ว
2. ไม่อ้างว่าการทดสอบนี้ต้องรัน production build -- ใช้ branch ทดลอง/เซิร์ฟเวอร์แยกที่แก้ค่าคงที่ตัวเดียว
   ชั่วคราว ห้าม commit การแก้นั้นเข้า `main`
3. ไม่อ้างว่าผลลบ (17 ถูก) แปลว่า M2 เสร็จ -- ปลายทางที่ยืนยันแล้วยังต้องการ CORE-REQUEST อื่นตามที่
   `world_m2_sea_destination.py` ระบุไว้ (จุดมาถึงจริงยังไม่ต่อสาย)

### links

`notes_to_chief/20260830_1351_COO-DECISION-m2-destination-held-at-17-escalated-to-owner.md` ·
`notes_to_chief/20260829_1410_LANE-A-ASK-COO-var2-is-a-markerid.md` (ทางเลือกที่ 3) ·
`notes_to_chief/20260827_1710_GT106-RESULT-...-owner-objects-dest-126-...md` ข้อ ④.2 ·
`src/pirateforce_foundation/world_m2_sea_destination.py` (`DESTINATION_SCENE_N_ID`, บรรทัด 183-190,
306-314) · `src/pirateforce_foundation/columbus_quest_dispatch.py`

**ผู้เปิดใบ: LANE-A (สาย A · WORLD) รอบ `12lyda` 2026-08-30T14:2x+07:00** -- เขียนตามคำสั่งตรงของ
COO-DECISION รอบนี้ ไม่ใช่ริเริ่มเอง

---

---

## GT-202 CENSUS-NPC-QUEST-MARK-GATE-WALK-SPEED-001  [**WITHDRAWN / OPENED-IN-ERROR** -- ถอนหัวใบโดย LANE-A (เจ้าของใบ) รอบ `2p4n3h` 2026-09-02T05:3x+07:00 ในรอบเดียวกับที่เปิด · **ไม่ต้องบูต ไม่ต้องมีผู้เทสทำอะไรทั้งสิ้น**]

> เหตุ: pf-adversary ของรอบเดียวกันหักล้างสมมติฐานที่ใช้เปิดใบ และ LANE-A ตรวจซ้ำเองแล้วยืนยันว่า
> ผู้ตรวจถูก · ใบนี้ตั้งอยู่บนการอ่านว่า `+0x70` ในเงื่อนไขข้ามของ `QuestIconBoard` คือ
> `BasicAttr+0x70` (`field_presence_mask`) ⇒ บิต `0x0040` = `MOBS.n_SPEED_WALK`
> **แต่** `reference_codex_attr/PF_COMBAT_LETHAL_TAIL_DELTA` มีแถว `PROVEN_EXACT` ว่า
> `Both dead-task start and update gate _F_DIE_000 on actor+0x70 bit 0x40` และ
> `The separately pinned CNetNPC model callback sets bit 0x40 only after its callback/resource
> gates complete` ⇒ มี `actor+0x70` บิต `0x40` ที่ถอดแล้วอยู่จริง เป็นบิตความพร้อมของโมเดล
> ฝั่ง **CNetNPC** · และแถว selector เดียวกัน **เขียนคำนำหน้าคลาสเมื่อหมายถึง BasicAttr**
> (`local-singleton BasicAttr+0x5E opaque u16 threshold`) ส่วน `+0x360`/`+0x364` ในประโยค
> เดียวกันเป็นของ CNetNPC ⇒ `+0x70` เปล่า ๆ น่าจะเป็นของ CNetNPC
> · โค้ดที่ใบนี้จะเทส **ถูกถอนออกจาก PR ของรอบ `2p4n3h` ทั้งหมดแล้ว** (อยู่ใน commit `e1e2b7c`
> บน branch `claude/dazzling-volta-2p4n3h` กู้กลับได้ถ้า `RE-202` ตอบว่าเป็น BasicAttr)
> · แทนที่ด้วย **`RE-202`** ใน `CLIENT_RE_QUEUE.md` ซึ่งเป็นสิ่งเดียวที่ปลดล็อกงานนี้ได้จริง
> · ไม่ลบใบ เก็บไว้เป็นประวัติตามกติกา
> · บทเรียนที่ต้องไม่ทำซ้ำ: ใบนี้ประกาศว่า `+0x70` เป็น "แถวเดียวที่ Codex ถอดไว้" โดยที่
> **ไม่ได้ grep ทั้งโฟลเดอร์ก่อน** — รูปแบบ G1 เดียวกับที่ `RE-201` โดนมาแล้วเมื่อรอบก่อน
> · ข้อผิดพลาดข้อที่สองที่บันทึกไว้: ใบนี้เรียกประโยคนั้นว่า "ท่อนแรก" ของ `skip_conditions`
> ทั้งที่มันเป็น **ท่อนที่สอง** (ท่อนแรกคือ `QuestNPCModule_refresh validated prerequisites reject`)

**ผู้เปิดและผู้ถอนใบ: LANE-A รอบ `2p4n3h`**

---

## GT-246 AUTO-WALK-CLICK-DIFFERENTIAL-001  [ANSWERED -- วัดครบแล้วในรอบ attended R310 (2026-09-04 18:45-19:07 +07:00) ตั้งแต่ก่อนใบนี้มีเลข -- ห้ามบู... -- archived 20260906 (closed; verbatim in `archive/GAME_TEST_QUEUE_ARCHIVE_20260906_closed.md`)

## คำถามเดิมที่ใบนี้ถูกเปิดมาตอบ
มาจาก `notes_to_chief/20260904_1226_LANE-UI-RE-TICKET-tracepath-record0-semantic-needs-attended-differential.md`
บวก `COO-DECISION 20260904_1244` ข้อ 2 (มินิแมปพับเข้าชุด differential เดียวกัน ไม่เปิดใบแยก):
**คลิกพื้น / คลิก NPC / คลิกมินิแมป -- สามอย่างนี้ทำให้ client ส่งเฟรมคลาสไหนออกสาย และอันไหน (ถ้ามี) ที่ยิง
`CTracePathReqVital` (`0x4391`)** สมมติฐานตั้งต้นของสารบัญ LANE-UI คือมินิแมปน่าจะเป็น `TargetPosVital` (`0x2A90`)
เหมือนคลิกพื้น -- ใบนี้วัดว่าจริงหรือไม่ (คำทำนายผิดคือ finding ไม่ใช่ความล้มเหลว)

- objective: (ข้ออ้างเดียว) คลาสของเฟรมขาออกต่างกันตามชนิดของคลิก และ **มีเฉพาะคลิกมินิแมปเท่านั้นที่ยิง
  `CTracePathReqVital 0x4391`** ส่วนคลิกพื้นและคลิก NPC ไม่แตะ trace-path เลย
  (ความหมายของ payload 0x4391 ไม่ใช่ข้ออ้างของใบนี้ -- ดู nonclaims 1)
- db: R310 บูตบน **สำเนา** `state\run_gt219_20260904_184529.sqlite3` (สำเนาที่ทำไว้สำหรับ GT-219 รอบเดียวกัน
  ใบนี้อาศัยบูตนั้น ไม่ได้บูตของตัวเอง) canonical ไม่ถูกเปิด sha256 ก่อน = หลัง `4FF37060...A548454`
  `PRAGMA integrity_check` = ok -- teardown PASS (job 1500: stopped x1, traceback 0, listeners 0, client 0)
- server args: `pirate-force-server` commit `d01ae973124abcc3dfcfaff2b0eda679f872a8ae` (newest green)
  **ไม่มีแฟล็ก scenario ใด ๆ** -- ฉากตามที่จดหมายจด: บรรทัดบูตเขียน `Arena01` ข้อ 2 เขียน "ฉาก 1" session 1
  (จดไว้ตามที่เป็น ไม่รวบเป็นค่าเดียว) raw capture `GAME_20260904_184*`
  capture root `GameClient\capture_r310_20260904_184529\`
- steps: **ไม่มีขั้นตอนให้ทำ -- ห้ามบูต** บันทึกไว้เป็นประวัติว่าอะไรถูกกดจริงในรอบ R310:
  คลิกพื้น 1 ครั้ง -> คลิก NPC (Columbus P65) 1 ครั้ง -> คลิกมินิแมป 1 ครั้ง ในเซสชันเดียวกัน
  จับสายด้วย `GAME_EVENTS_LIVE.txt` (seq 2-5) ตลอดช่วง
- pass criteria (สองชั้น -- ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น):
    wire/DB (headless พิสูจน์ได้ ไม่ต้องมีตาคน):
      (1) เฟรมขาออกของทั้งสามคลิกถูกจับครบ พร้อม opcode/ขนาดไบต์/เวลา -- **ส่งมอบครบ** (ตาราง result)
      (2) ระบุได้ว่าคลิกใดยิง `0x4391` และคลิกใดไม่ยิง -- **ส่งมอบครบ** (มีเฉพาะมินิแมป)
      (3) จับ payload ดิบของ `0x4391` ไว้ทั้งก้อน -- **ส่งมอบครบ** (25 B, hex เต็มใน `GAME_EVENTS_LIVE.txt`)
      (4) integrity ok + canonical sha ไม่เปลี่ยน + teardown -- **ส่งมอบครบ**
      **ไม่ส่งมอบ**: การถอดความหมายฟิลด์ใน payload (ไม่ใช่ของชั้นนี้และไม่ใช่ของใบนี้)
      ชั้นนี้ตอบไม่ได้ว่าบนจอเห็นอะไร
    client-observable (ต้องมีตาคน -- ห้ามอนุมานจากไฟล์จับสาย):
      (5) สิ่งเดียวที่ชั้นนี้ได้จริงคือ **"คลิกพื้นแล้วตัวละครเดิน"** ตามที่จดหมายเขียนกำกับแถวแรกว่า "(เดิน)"
          -- เท่านี้ ไม่มีมากกว่านี้
      **ไม่ส่งมอบ (จดตามจริง ไม่กลบ)**:
        (ก) ไม่มีภาพนิ่งใดอยู่ในช่วง 18:50-18:52 (ภาพในรอบคือ 184909/185512/185526/185844/1859xx)
            จึง **ไม่มีบรรทัดสีป้ายชื่อของเฟรมที่เป็นของใบนี้เลย** -- ข้อบังคับ R163 (คำสั่ง Panya 2026-08-25)
            ไม่ได้ถูกสนองสำหรับใบนี้ และแก้ไม่ได้เพราะห้ามบูตซ้ำ (บรรทัดสีที่มีในจดหมายเป็นของ GT-219 ภาพ
            184909 และของ P-2 ภาพ 1859xx -- คนละการสังเกต ห้ามยืมมาใช้กับใบนี้)
        (ข) จดหมาย **ไม่ได้บอก** ว่าคลิก NPC หรือคลิกมินิแมปทำให้ตัวละครขยับหรือไม่ ประโยคสรุป
            "มีแค่คลิกมินิแมปที่เดิน 0x4391" หมายถึงเส้นทางบนสาย ไม่ใช่ว่าตัวละครเดิน -- ห้ามอ่านเป็นอย่างหลัง
      **ใบนี้ไม่มีลายเซ็นผู้สังเกตของตัวเอง**: `OBSERVER_CONFIRMED: 2026-09-04T18:49+07:00` ในจดหมายเป็น
      บรรทัดปิดของ **ข้อ 1 (GT-219 ขั้น B)** และมีเวลา **ก่อน** ทั้งสามคลิก (18:50-18:52) จึงเซ็นใบนี้ไม่ได้
      สิ่งที่ใบนี้พิงแทนคือ: ชั้น wire/DB ที่พิสูจน์ headless ได้ทั้งหมด + ข้อเท็จจริงว่าเป็นรอบ attended จริง
      (ผู้ขับ Panya อยู่หน้าจอ ผู้วัด ka1-A) + teardown PASS + canonical sha ก่อน=หลัง
      => สถานะจึงเป็น `ANSWERED` (คำถามบนสายถูกตอบครบ) **ไม่ใช่ `PASS`** เพราะชั้น client-observable
      ไม่ครบตามมาตรฐานบ้านและไม่มีลายเซ็น

## result (คัดคำต่อคำจาก `20260904_1911` ข้อ 2 -- R310 ฉาก 1 session 1 raw `GAME_20260904_184*`)
| คลิก | เวลา | เฟรมที่ client ส่ง |
|---|---|---|
| พื้น 1 ครั้ง | ~18:50-18:51 | **`TargetPosVital` เท่านั้น** (เดิน) -- ไม่มี 0x4391 |
| NPC (Columbus P65 actor 0x2042) 1 ครั้ง | 18:51:52 / 18:51:54 | `TargetVital 0x1ADD` (40 B, kind=2) แล้ว `ChooseNPC 0x0FB6` (38 B) |
| มินิแมป 1 ครั้ง | 18:52:12 | **`CTracePathReqVital 0x4391`** 25 B payload `0F00000F000014000000000F01000F65010FB2000F007D0802` -> server ตอบ `TRACE_PATH_EMPTY_VECTOR_REPLY` (35 B) ตามด้วย `TargetVital target=clear` 18:52:16 |

สรุปที่จดหมายบันทึก: **มีแค่คลิกมินิแมปที่เดิน 0x4391 -- คลิกพื้น/NPC ไม่แตะ trace-path เลย**
hex เต็มอยู่ที่ `GAME_EVENTS_LIVE.txt` seq 2-5 ใต้ capture root ข้างบน
ผลข้างเคียงที่ต้องบันทึก: สมมติฐานเดิมของสารบัญ LANE-UI ที่ว่ามินิแมป = `TargetPosVital` (`0x2A90`)
**ถูกหักล้าง** -- นี่คือ finding ของใบนี้ ไม่ใช่ข้อผิดพลาดของใคร

## ของที่เหลือ (ชี้ทางเฉย ๆ ไม่ใช่ขั้นตอน attended ใหม่ในใบนี้)
LANE-UI เป็นผู้ตัดสินความหมายของ payload `0x4391` 25 ไบต์ข้างบน (field layout ปิดไว้แล้วโดย `RE-119`
`external/PF_SERIALIZER_FIELDS.tsv:5521-5536`) -- ทำจาก static ล้วนได้ ไม่ต้องใช้เครื่อง
คำถามคนละใบที่ **ยังไม่ถูกแตะ** โดย R310: semantic ของ `u16@+0x14` (เคย capture ได้ `743` ซึ่งชนทั้ง
`gamedata/tables/QUESTDATA_TH__QUEST.tsv n_ID=743` และ `CONSTDATA_TH__MOBS.tsv n_ID=743`) --
วิธีปิดที่ `1226` เสนอไว้คือกด GO! ไปสองเป้าที่ n_ID ไม่ชนกัน ซึ่ง **R310 ไม่ได้ทำ**
ถ้า LANE-UI ยังต้องการ ให้เปิดใบใหม่ของตัวเอง (หนึ่งใบ = หนึ่งข้ออ้าง) ห้ามต่อท้ายใบนี้

## nonclaims
1. ไม่ตัดสินความหมายของ payload `0x4391` และไม่ตัดสินว่า `743` คือ quest id / NPC id / list index --
   ยกมาจาก nonclaim ข้อ 1 ของ R310 เอง ("ไม่ตัดสินความหมาย payload 0x4391 (LANE-UI)") สามทางยังเปิดเท่ากัน
2. ไม่พิสูจน์ว่า `RunFindPath` ทำอะไรต่อเมื่อ response ไม่ว่าง -- รอบนี้ server ตอบ empty-vector เท่านั้น
3. ไม่พิสูจน์ว่าคลิกทั้งสามชนิดให้ผลเดิมในฉากอื่น/เป้าอื่น/เซสชันอื่น (วัดฉากเดียว session เดียว คลิกละ 1 ครั้ง)
4. ไม่พิสูจน์ว่าตัวละครเดินหรือไม่เดินตอนคลิก NPC และตอนคลิกมินิแมป (ดูข้อ (ข) ของชั้น client-observable)
5. ไม่มีบรรทัดสีป้ายชื่อของใบนี้ จึงไม่พิสูจน์และไม่ขัดแย้งอะไรกับ `RE-067` และไม่มีแถวใหม่ลง
   `REAL_SERVER_DIVERGENCE.tsv` จากใบนี้
6. ไม่ปิด ไม่กลับคำ และไม่ทับ `RE-119` (ปิดแล้ว PASS/DONE) -- เป็นชั้นหลักฐาน attended ต่อจาก static
7. ไม่พิสูจน์อะไรบน canonical DB (บูตบนสำเนา) และไม่พิสูจน์อะไรที่ต้องรอดข้าม relog

## links
`notes_to_chief/20260904_1911_KA1A-R310-RESULTS-gt219-step-B-PASS-gmui-opens-auto-walk-differential-captured-live-warp-persists-scene-CONFIRMED-p2-pixel-mob-name-pink-in-all-three-states.md` (ข้อ 2 = ที่มาทั้งหมดของ result) --
`notes_to_chief/20260904_1226_LANE-UI-RE-TICKET-tracepath-record0-semantic-needs-attended-differential.md` (คำถามเดิม) --
`notes_to_chief/20260904_1244_COO-DECISION-lane-ui-catalog-closed-at-14-of-15-minimap-folds-into-auto-walk-write-the-eight-handlers-now-as-pure-modules.md` ข้อ 2 (มินิแมปพับเข้าชุดนี้) --
`notes_to_chief/20260904_1948_COO-DECISION-consume-R310-R311-close-GT219-1430-number-select-screen-GT-answer-0554-chief.md` ข้อ 4 (คำสั่งตั้งเลข + ห้ามบูตซ้ำ) --
`CLIENT_RE_QUEUE.md` บล็อก `RE-119` (CLOSED PASS/DONE) -- `external/PF_SERIALIZER_FIELDS.tsv:5491-5536` --
`GameClient\capture_r310_20260904_184529\GAME_EVENTS_LIVE.txt` seq 2-5

## numbering
ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `245` (`GT-245`) => ใบนี้ `246`
`GT-246`/`RE-246` = 0 hit ทั้งสามที่ก่อนวาง (ตรวจโดย chief รอบ `t7bsfx`/R342)

**ผู้เปิดใบ: chief (LANE-E) ตาม `COO-DECISION 20260904_1948` ข้อ 4 -- ผู้บริโภคผล: LANE-UI**

---

---

## GT-151 PORT-ROYAL-SEVEN-HOLES-EYES-001 [attended, in-game]: 108 จาก 115 ขึ้นจอ -- **เจ็ดรูที่ผู้เล่นเดินไปเจอ ใช่เจ็ดจุดที่คอนโซลเรียกชื่อหรือไม่**  [OPEN (PARTIAL) · เปิดโดย LANE-A (สาย A · WORLD) รอบ `tz2eri` · 🆕 **อัปเดตโดยเจ้าของใบ LANE-A รอบ `n4wj7k` 2026-08-30T08:30+07:00 — 1/7 จุดตรวจแล้ว ใบไม่ปิด:** กะ3-A ใบ `notes_to_chief/20260830_0030_KA3A-GT131-PASS-owner-confirmed-gt151-partial-plus-four-polish-gaps-and-mob-vs-npc-question.md` เดินไปตรวจจุด P0 (Navy Transfer เดิม) พบว่าง ไม่มีใครยืน มีตัวคุมชัด (Columbus/Loie ยืนใกล้ในเฟรมเดียวกัน) สอดคล้องคำทำนาย "ว่าง" · อีก 6 จุดยังไม่ได้เดินไปตรวจ ตามกติกาใบเขียนว่า "ไม่ได้ตรวจ" ห้ามเดา — ยกไปรอบ attended ถัดไป · 🔴 **[LANE-K รอบ `kxpzxi` 2026-09-07T03:15+07:00] ถอนออกจาก `QUEUE_STATUS_SNAPSHOT.md` ชั่วคราว ตาม `PANYA-ORDER 20260907_0159` ข้อ 2** (หน้าที่คัดใบ attended ที่ไม่จำเป็น PANYA `2148` ย้ายมาอยู่กับ LANE-K): ใบนี้เข้าเกณฑ์ (ก) **อายุ >7 วัน** (เปิด 2026-08-29 = 9 วัน) และเป็นหนึ่งใน ใบที่เจ้าของยกเป็นหลักฐานในคำสั่งเอง · **K ยกเลิกใบเองไม่ได้ (พับ=คัดลอก)** — ใบยังเปิดอยู่ทุกตัวอักษร ไม่มีอะไรถูกลบ · **เจ้าของใบ LANE-A ต้องตอบกลับ: ยืนยันซ้ำว่ายังต้องบูตจริง (แล้ว K ใส่กลับรถบัส) หรือยกเลิกพร้อมเหตุผลตามกฎ PANYA `20260903_1934`** · จดหมายแจ้ง: `notes_to_chief/20260907_0315_LANE-K-CULL-3-tickets-off-bus-need-owner-reconfirm.md`]] [🚫 **CANCELLED โดยเจ้าของใบ LANE-A รอบ `tsdl0w` 2026-09-07T04:26+07:00** — วางโดย LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00 · K ไม่ได้ยกเลิกเอง (พับ=คัดลอก) · จดหมาย `notes_to_chief/20260907_0426_LANE-A-TO-K-gt151-cancelled-no-longer-needs-proving.md` · บรรทัดของเจ้าของใบคำต่อคำตามรูปแบบบังคับของ `PANYA-DECISION 20260903_1934`: "CANCELLED - no longer needs proving because M1/v1 was declared on GT-131's on-screen population pass (R249) and the six unchecked spots only refine WHICH seven of 115 are missing, which blocks no milestone and no other ticket; the one spot LANE-A did walk (P0, round n4wj7k) matched the console prediction, so there is no measured disagreement to chase, and the console side of the question is derivable headless without owner-machine time." · เจ้าของใบรับผิดชอบต่อ: ถ้ารอบ attended ในอนาคตบูตที่ Port Royal (bg0001) อยู่แล้ว LANE-A จะเสนอหกจุดที่เหลือเป็น **rider บรรทัดเดียวในใบนั้น** ไม่ขอที่นั่งบนรถบัสของตัวเอง · nonclaim ที่ยกมาด้วย: ประชากร bg0001 ยังเป็น **108/115** ไม่ใช่ครบ · หกจุดที่เหลือ**ยังไม่ตรวจ** และยกเลิกโดยรู้ตัวว่ายังไม่ตรวจ]

> NUMBERING: grep ก่อนจอง -- `GT-150`/`GT-151`/`GT-152` = 0 hit ทั้งสองไฟล์ · สูงสุดก่อนหน้า = `GT-149` (`RE-` สูงสุด = 150) ⇒ ใบนี้ = `GT-151` · ตัวนับเดียวร่วม `CLIENT_RE_QUEUE.md`
> ที่มา: จดหมายผล `RE-149` (`notes_to_chief/20260829_1814_RE-149-RESULT-NO-SHIPPED-AVATAR-SOURCE.md`) · โค้ดที่พิมพ์บรรทัด = `world_population.ceiling_console_token` / `undressable_console_token` (ลงใน `pirate-force-server#271`) · ชั้น wire/DB ของ `BUILD-001` วัดครบแล้ว: บูตไร้แฟล็กประกอบ **108 จาก 115** แถวแช่แข็งของ `bg0001` และเจ็ดตัวที่ตกมี**เหตุผลระบุชื่อรายตัว**บนคอนโซลรอบนี้ · สิ่งที่ยังไม่มีใครยืนยันด้วยตา คือรูบนจอเป็นเจ็ดจุด**นั้น** ไม่ใช่เจ็ดจุดอื่น
> 🔴 **ไม่ซ้ำกับ `GT-131`**: `GT-131` (PENDING) ถามว่า NPC ที่ **มาถึง** แสดง **ตัวจริง** หรือไม่ (เรื่องตัวตน หลัง `GT-078` ถูกเจ้าของปฏิเสธ) · ใบนี้ถามคนละข้อ -- **จุดที่ว่าง ใช่จุดที่ถูกเรียกชื่อหรือไม่** · ห้ามปิดใบหนึ่งด้วยผลของอีกใบ
> 🆕 **อัปเดตโดยเจ้าของใบ LANE-A รอบ `6oyud5` 2026-08-31T04:34+07:00 — ใบไม่ปิด, เครื่องมือใหม่เท่านั้น:** เจ็ดพิกัดในตารางด้านล่างนี้เคยมาจากการเปิดซอร์สคำนวณมือครั้งเดียวตอนรอบ `tz2eri`
> ตอนนี้บูตไร้แฟล็กทุกบูตพิมพ์พิกัดเดียวกันเองบนบรรทัด `WORLD_CENSUS` ท้ายสุด (`undressable_positions=7 P0@x,y,z,...`, `world_population.undressable_placements_positioned`/
> `undressable_positions_console_token`, ยังไม่ merge -- ดู `PR_STATE.txt`) จึงไม่มีทางเพี้ยนจากตารางค้างเก่าถ้าตารางแช่แข็งเคยเปลี่ยน และใบพี่น้อง (`GT-143`, คนละฉาก) ไม่ต้องคำนวณมือซ้ำอีก
> **ไม่เปลี่ยนตัวคุมหรือ pass criteria ของใบนี้แม้แต่ข้อเดียว** -- เจ็ดจุดในตารางด้านล่างยังใช้เดินได้เหมือนเดิมทุกประการ ตัวเลขตรงกันทั้งสองแหล่ง (ยืนยันด้วย test คนละไฟล์)

### objective (claim เดียว)
เจ็ดพิกัดที่คอนโซลเรียกชื่อว่าถูกตัด **ว่างเปล่าบนจอจริง** -- ใบนี้ตอบข้อเดียว: "ตรงจุดนี้มีอะไรยืนอยู่ไหม"

### db / server args (เป๊ะ)
สำเนา `state\run_gt151.sqlite3` · 🔴 ห้ามเปิด canonical `state\pirateforce.sqlite3` · sha256 canonical ก่อน-หลังต้องเท่ากัน
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt151.sqlite3
```
🔴 **บูตไร้แฟล็ก** ห้ามมีแฟล็กฉากใด ๆ (`--*-scenario`, `--world-census-actors`) · client `-SecondPasswordMode bypass` · 🔴 **restart เซิร์ฟเวอร์ก่อนบูตไคลเอนต์ทุกครั้ง** (session ค้าง ⇒ ไคลเอนต์ถัดไปค้าง "connecting") · จด `BOOT_COMMIT`

### เจ็ดจุด (P = `placement_index` ของแถวเอง 🔴 ไม่ใช่ลำดับในรายการ -- การอ่านรอบก่อนพลาดตรงนี้)

| ลำดับ | P | set | lead | x | y | z | ชื่อในไฟล์ฉาก | ชื่อฝั่งไคลเอนต์ |
|---|---|---|---|---|---|---|---|---|
| 1 | P0 | set1 | lead155 | -9139.96 | -2780.05 | 223.29 | Navy Transfer | Port transportation |
| 2 | P145 | set110 | lead9107 | 1788.80 | -1528.39 | 930.42 | Filet | Jack |
| 3 | P147 | set112 | lead937 | 5882.73 | -2021.71 | 1985.66 | Rude pirates | Mengsk |
| 4 | P148 | set113 | lead942 | 13396.38 | -5367.95 | 2210.97 | Pirates from afar | NON_ASCII (CJK พิมพ์บน cp874 ไม่ได้) |
| 5 | P86 | set86 | lead0 | -10974.88 | -1231.23 | 747.38 | Mori Hiroko | (ไม่มีสิ่งมีชีวิต) |
| 6 | P87 | set87 | lead0 | -15017.48 | -12759.95 | 308.27 | Sea Phantom | (ไม่มีสิ่งมีชีวิต) |
| 7 | P75 | set76 | lead819 | 19984.35 | 18249.38 | 1111.40 | Hasan | Tuna |

🔴 **P0 แทบไม่มีต้นทุน**: ห่างจุดเกิดล็อกอิน `(-9239.957, -2780.045, 223.292)` ราว **100 หน่วย** ⇒ ได้ข้อมูลจุดแรกโดยไม่ต้องเดินไปไหน · **ใบนี้คุ้มรันแม้ทำแค่ P0 จุดเดียว** · จุดที่ไม่ได้ทำเขียนว่า "ไม่ได้ทำ" ไม่ใช่ PARTIAL

### ขั้นตอน
0. มาตรฐานบ้าน: LOCK · boot stamp (+07:00) · sha canonical · copy DB · จด `BOOT_COMMIT`
1. **server ก่อน client เสมอ** · 🔴 **ห้ามพิมพ์ตัวอักษรใด ๆ ตลอดรอบ** -- ตัวอักษรตอนช่องแชตไม่โฟกัสกลายเป็น hotkey
2. ล็อกอิน ยังไม่ขยับ → **S0** ภาพนิ่ง full-res ที่จุดเกิด
3. 🔴 **ตัวคุม (หัวใจของใบ)**: ก่อนรายงานว่า P0 ว่าง ต้องเห็น **NPC ที่มาถึงอย่างน้อยหนึ่งตัว**บริเวณรอบ P0 และถ่ายติดมาด้วย -- ไม่มีตัวคุม จอที่ว่างเพราะสำมะโนไม่มาถึงจะถูกอ่านเป็น PASS โดยบังเอิญ
4. เดินไป P0 ด้วย `A/S/D/W/Q/E` (click-to-walk ปิดในตั้งค่า) → ถ่าย **full-res** + จดพิกัดที่ UI แสดง
5. ทำซ้ำข้อ 3-4 กับจุดที่เหลือตามลำดับตาราง จุดละหนึ่งภาพ **พร้อมตัวคุมของจุดนั้น** (หรือเขียนว่า "รอบจุดนี้ไม่มีใครเลย" ซึ่งเป็นผลสำคัญ)
6. NO-CRASH ด้วย **คลิกขวาค้างลากเท่านั้น** (หมุนกล้องอย่างเดียว ไม่มีไบต์ออกสาย · 🔴 ห้ามใช้ `Q`/`E` เป็นตัววัด NO-CRASH มันหัน**ตัวละคร**จริงและยิง `TargetPosVital`)
7. ออกเกมด้วย X → ปิดเซิร์ฟเวอร์ → เก็บภาพ + console `.out`/`.err` + sha256 ทุกไฟล์ · `PRAGMA integrity_check` บน**สำเนา** · **teardown เสมอ ภายใน 420 นาทีจาก boot stamp** (`TEMPLATE_teardown_generic.ps1:135`) · sha canonical ซ้ำ · 🔴 ห้าม commit เอง

### pass criteria (สองชั้น 🔴 ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)
**wire/DB (headless ล้วน · grep บรรทัดเดียวจากคอนโซลบูต · 🔴 grep ต้องมี `2>&1` บางโทเคนอยู่บน stderr):** คัดลอกดิบ ๆ ท้ายบรรทัดต้องอ่านได้ว่า
```
| undressable=7 P0/set1/lead155/Port_transportation,P75/set76/lead819/Tuna,P86/set86/lead0/NO_CREATURE,P87/set87/lead0/NO_CREATURE,P145/set110/lead9107/Jack,P147/set112/lead937/Mengsk,P148/set113/lead942/NON_ASCII | ceiling=108/115 client_data_bounded RE-149:BOUNDED-NEGATIVE no_avatar_source=5,no_creature=2
```
+ `integrity_check`=ok · `sessions` +1 ต่อการเข้าเกม · `max(lease_generation)` ไม่ถอยหลัง · sha canonical ตรงก่อน-หลัง
🔴 ชั้นนี้ **ตอบไม่ได้ว่ามีอะไรอยู่บนจอ**
**client-observable (ต้องมีคนหน้าจอ):** ภาพนิ่ง full-res ต่อจุด + sha256 · ต่อจุดตอบสองอย่าง**แยกกัน**: (ก) บนจุดนั้นมีอะไรยืนอยู่ไหม ถ้ามีชื่ออะไร (ข) **ตัวคุม** รอบจุดเห็น NPC อื่นกี่ตัว · **จดสีป้ายชื่อทุกป้ายทุกภาพ** บรรทัดละป้าย รวมป้ายตัวเอง ไม่มีป้ายเขียน `none` · อ่านสีจาก **ภาพนิ่ง full-res เท่านั้น** ห้ามอ่านจาก contact sheet ภาพย่อ หรือวิดีโอ · 🔴 **จดสีอย่างเดียว ห้ามเดาสาเหตุ** (`RE-067`) · ต่างจากภาพเซิร์ฟเวอร์จริง → `REAL_SERVER_DIVERGENCE.tsv` แถวละหนึ่งข้อ · NO-CRASH/CRASH · `OBSERVER_CONFIRMED`
🔴 ชั้นนี้ **ตอบไม่ได้ว่าเฟรมใดออกจากเซิร์ฟเวอร์**
**PASS** = ทุกจุดที่ทำ **ว่าง** และ **รอบจุดนั้นมีคนอยู่** (ตัวคุมผ่าน) -- ขาดตัวคุม = PARTIAL ไม่ใช่ PASS
**FAIL / ของน่าสนใจ** = (ก) มีอะไรยืนบนจุดที่ถูกเรียกชื่อ ⇒ รายชื่อที่ตัดไม่ตรงกับจอ · (ข) รอบจุดว่างด้วย ⇒ เรื่องใหญ่กว่าเจ็ด · **ทั้งสองแบบมีค่าเท่ากับ PASS** ⇒ redirect เป็นใบใหม่ ไม่ใช่ความล้มเหลว

### คำทำนาย (เป็นคำทำนาย ผิด = ผล ไม่ใช่ความล้มเหลว)
**P1** เจ็ดจุดว่าง รอบ ๆ มีคน ⇒ รายชื่อที่ตัดตรงกับจอ · **P2** จุดใดมีคนยืน ⇒ index ที่ใช้อ้างแถวเพี้ยน เปิดใบ RE ทันที · **P3** รอบจุดว่างด้วย ⇒ สำมะโนไม่มาถึงบริเวณนั้น ใหญ่กว่าใบนี้

### กฎจุดเกิด
รอบนี้ก๊อป DB ⇒ ตัวละครกลับจุดเกิดทุกบูต · ตามกฎ `pf-attended-test` (เกิด**ใกล้และหันหน้าเข้าหา**สิ่งที่ทดสอบ) จุดเกิดล็อกอินห่าง P0 ~100 หน่วยอยู่แล้ว ไม่ต้องตั้งค่าเพิ่ม

### [ไม่อ้าง] nonclaims
1. **ไม่ตัดสินว่า 108 ตัวที่มาถึงแสดงตัวตนถูกหรือไม่** -- นั่นคือ `GT-131` ห้ามปิดสองใบทับกัน
2. ไม่ตัดสินว่าห้าตัวที่ไม่มีแหล่ง avatar จะวาดได้ในอนาคตไหม -- `RE-149` ตอบจากข้อมูลสถิตล้วน และประกาศเองว่า**ไม่ได้ดูจอ**
3. ไม่ตัดสินเลข 115 ในตารางแช่แข็ง · ไม่ตัดสิน encoding ของชื่อ CJK (`GT-145`) · ไม่วัดว่าเซิร์ฟเวอร์ต้นฉบับมีใครยืนตรงนั้น

### links
`notes_to_chief/20260829_1814_RE-149-RESULT-NO-SHIPPED-AVATAR-SOURCE.md` · `world_population.undressable_placements_named` + `population.load_port_royal_placements` (ที่มาพิกัดเจ็ดจุด วัดรอบนี้) · `pirate-force-server#271` · `GT-131` (คนละข้ออ้าง) · `GT-143` (ใบพี่น้อง วิธีเดียวกันคนละฉาก) · เพิ่มรอบ `6oyud5`: `world_population.undressable_placements_positioned` / `undressable_positions_console_token` (พิมพ์เจ็ดพิกัดนี้เองทุกบูต, ยังไม่ merge)

**ผู้เปิดใบ: LANE-A (สาย A · WORLD) รอบ `tz2eri` 2026-08-29T18:4x+07:00** -- ผลกลับมาที่สาย A บริโภค

### result (ผู้เทสกรอก -- หนึ่งบรรทัดต่อจุด)
```
BOOT_COMMIT :
บรรทัด undressable/ceiling จากคอนโซล (คัดดิบ grep 2>&1) :
P0 / P145 / P147 / P148 / P86 / P87 / P75 :
   วาง | มีคนยืน(ชื่อ) | ไม่ได้ทำ  + ตัวคุม: รอบจุดเห็น NPC อื่นกี่ตัว/ชื่อ (หรือ "ไม่มีเลย")
สีป้ายชื่อทุกป้ายทุกภาพ (บรรทัดละป้าย, ไม่มี = none) :
path + sha256 ของภาพ/console/DB :
CANON_SHA ก่อน/หลัง · integrity_check · sessions · lease_generation · NO-CRASH/CRASH :
OBSERVER_CONFIRMED  :
```

---

> ย้ายมาโดย LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00 · เหตุผล: CANCELLED โดยเจ้าของใบ LANE-A รอบ `lnq6xy` (จดหมาย `notes_to_chief/20260907_0603_LANE-A-TO-K-gt151-and-gt193-both-cancelled.md`) · เนื้อใบข้างล่างยกมาคำต่อคำ ไม่แก้แม้แต่ตัวอักษรเดียว

## GT-193 SPEED-COMMAND-SPARSE-X7-001  [🟢 READY **เฉพาะขั้น 9 และ 10** · 🔴 **ขั้น 4-7 ยังเป็น `PENDING interface` ห้ามเกรด** -- HOLD ของ R315 ปลดแล้วตาม `COO-DECISION 20260903_0745` ข้อ ② (chief วัด RECHECK ข้อ 6 เองบน `1e184532`) แต่ **ปลดอันตราย ≠ เกรดได้** และ pf-adversary รอบ `pa5pn8` หักล้างว่าผมกำลังจะปล่อยใบที่เผารอบทิ้ง: [🟡 **ถอนออกจาก `QUEUE_STATUS_SNAPSHOT.md` ชั่วคราว โดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 ตาม `PANYA-ORDER 20260907_0159` ข้อ 2 — เกณฑ์ (ข) โค้ดที่ใบพึ่งพาเปลี่ยนหลังวันเขียนใบ** · ใบเขียน 2026-09-01 · วัดสดบน `origin/main` (คลอน unshallow) `git log --since=2026-09-01 -- <ไฟล์>`: `gm/chat_command_action.py` **36 คอมมิต** · `gm/speed_wire.py` **10** · `docs/FUNCTIONAL_COVERAGE.json` **8** · `tests/test_gm_speed_denied_notice.py` **7** · `persistence_attr_compose.py` **4** · `login_speed.py` **3** · `gm/say_wire.py` **5** — ทั้งเจ็ดไฟล์ที่ใบอ้างถึงเปลี่ยนหมด · คอมมิตที่ชนขั้น 9-10 ของใบตรง ๆ: `28efa1af` (2026-09-03 `PF_SPEED_TRIAL` คีย์รันไทม์ที่เปิด `/speed` ให้ค่าเดียว) · `41e347b3` (2026-09-03 "the sparse `/speed` door closes") · `3bb6b4e4` (2026-09-04 "(b'') becomes the login mask set") · 🔴 **ใบยังเปิดอยู่ทุกตัวอักษร LANE-K ไม่ได้ยกเลิกและไม่ได้แตะเนื้อใบ** — รอ **LANE-A (เจ้าของใบ)** ตอบหนึ่งบรรทัด (ยืนยันซ้ำ ⇒ ใส่กลับรถบัสทันที · หรือยกเลิกพร้อมเหตุผลตามกฎ PANYA `20260903_1934`) · จดหมาย `notes_to_chief/20260907_0409_LANE-K-CULL-B-gt193-gt272-code-changed-after-ticket.md`]
>
> 🔴 **ทำไมขั้น 4-7 เกรดไม่ได้วันนี้** -- `gm/speed_wire.py:342` `SPEED_LOGIN_READ_LANDED = False` ⇒ `send_deferred()` (บรรทัด 357) คืน **True** ⇒ `gm/chat_command_action.py:3994` **กันเฟรมไว้ทุกครั้ง ไม่มีไบต์ออกเลย** (chief วัดเองบน `origin/main 1e184532` รอบ `pa5pn8`) ⇒ เกณฑ์ wire ข้อ (ก) (change-mask บิต `0x0040`) และเกณฑ์ client-observable ("เดินเร็วขึ้นไหม") **เป็นจริงไม่ได้ทั้งคู่** — ไม่ใช่ FAIL แต่เป็นเกตที่ทำงานถูกต้อง
> **ห้ามเกรดขั้น 4-7 เป็น FAIL เด็ดขาด** · ถ้าบูตแล้วเห็นศูนย์ไบต์ = ถูกแล้ว จดว่า `SPEED DEFERRED` แล้วข้ามไปขั้น 9
>
> 🔴 **และหน้าจอเงียบ** -- แขนง deferral ไม่ส่ง notice action ใด ๆ (`[ASSUMPTION OF LANE-GM, AWAITING COO]` ในซอร์สเอง) ⇒ เงื่อนไข "ห้ามเงียบ" ของ `COO-DECISION 20260902_0147` ที่ RECHECK ข้อ 5 ปิดไปแล้วสำหรับ*คำปฏิเสธ* **เปิดใหม่สำหรับ*การรับคำสั่ง*** (เกิดหลัง R299 เมื่อ 2026-09-02T18:47) ⇒ บรรทัด "Do NOT promote to READY" ในเนื้อใบ (9906/9930) **ยังยืนสำหรับขั้น 4-7 เท่านั้น**
>
> 🟢 **ขั้น 9 (`/speed 1e40`) และขั้น 10 (`/speed fast`) เกรดได้ตามปกติ** -- ทางปฏิเสธอยู่ **เหนือ** เกต deferral (`_speed_denied(...)` ยิงก่อนบรรทัด 3994) ⇒ นี่คือของที่รอบ attended รอบนี้ได้จริง
>
> 🔴 **แก้คำของ chief เอง**: R316 ฉบับแรกของผมเขียนว่า "เนื้อใบ ขั้นตอน และเกณฑ์ไม่เปลี่ยนสักข้อจาก R299" -- **เท็จ** ขั้น 10 เพิ่ม R303 · ประโยคในขั้น 6 และ RECHECK ข้อ 6 เพิ่ม R315 · ที่ COO เขียนว่า "ตามเดิมทุกประการ" หมายถึงเทียบกับ**ตอน HOLD** ไม่ใช่เทียบ R299
>
> 🔴 **RECHECK ข้อ 6 ไม่ใช่ตัวกันประตูที่ฆ่าตัวละคร** -- อันตรายที่ `GT-193` วัดได้จริงใน R303 คือ**เฟรมขาออกในเซสชัน** (DB ฝั่งเราสะอาด) ประตูนั้นถือโดย `SPEED_LOGIN_READ_LANDED` ไม่ใช่โดยเกตล็อกอิน ⇒ RECHECK ข้อ 6 ถูกเสริมเป็นสามคำในรอบนี้ (ดูข้างล่าง) และมี **ตัวรีล็อกอัตโนมัติ** ที่ใบนี้เคยไม่มี]

RECHECK ข้อ 6 (ตัวปลด/ตัวรีล็อก · เพิ่มโดย chief R315 · **เสริมเป็นสามคำโดย chief R316** หลัง pf-adversary หักล้างว่ารูปเดิมพอใจกับคำใน docstring):
  🔴 **ทำไมรูปเดิมอ่อน (วัดแล้ว R316)**: `findstr /C:"wire_deferred"` ติดที่ `login_speed.py:90` และ `:379` ซึ่งเป็น **docstring** ⇒ ถอดบรรทัด `held = held_by_the_speed_deferral(fallback)` ที่ 424 ออก แล้วเกตนี้ก็ยัง "ผ่าน" · ห้ามใช้รูปเดิมอีก
  **ทั้งสามคำต้องเจอครบ จึงถือว่าผ่าน** (รูปเดียวกับ RECHECK ข้อ 2 ของ `GT-218` ที่ chief เขียนไว้เองรอบก่อน):
  `(cd pirate-force-server && git fetch origin && git show origin/main:src/pirateforce_foundation/login_speed.py | findstr /C:"held_by_the_speed_deferral(fallback)")`
  `(cd pirate-force-server && git show origin/main:src/pirateforce_foundation/gm/speed_wire.py | findstr /C:"send_deferred")`
  `(cd pirate-force-server && git show origin/main:src/pirateforce_foundation/gm/chat_command_action.py | findstr /C:"speed_wire.send_deferred()")`
  **เจอครบสาม** = ประตูล็อกอิน**และ**ประตูขาออกยังปิดทั้งคู่ ⇒ ขั้น 9-10 บูตได้ · **ขาดข้อใดข้อหนึ่ง** = กลับเป็น `[🔴 HOLD]` ทันที ห้ามบูต
  🔴 **ตัวรีล็อกอัตโนมัติ (ใหม่ R316 · ใบนี้ไม่เคยมี)**: ถ้า
  `(cd pirate-force-server && git show origin/main:src/pirateforce_foundation/gm/speed_wire.py | findstr /C:"SPEED_LOGIN_READ_LANDED: bool = True")`
  **เจอ** ⇒ ประตูขาออกเปิดแล้ว ⇒ ใบนี้กลับเป็น `[🔴 HOLD]` **ทันทีและอัตโนมัติ** ห้ามบูตจนกว่ารอบ `GT-218` (ค่า `400` ค่าเดียว พร้อมวิดีโอและกฎ STOP-on-HP-0) จะเกิดและมีผล ตาม `COO 2147` · เหตุผล: ขั้น 4 ของใบนี้พิมพ์ `/speed 800` ซึ่ง **2.67 เท่าของ `300` ที่ฆ่าตัวละครมาแล้ว** และซอร์สวันนี้ **ไม่มี clamp ไม่มี allow-list** (`GT-218` nonclaim 2)
  สถานะ ณ R316 (2026-09-03T08:3x+07:00): เจอครบสามคำบน `origin/main = 1e184532` (chief วัดเอง) และ `SPEED_LOGIN_READ_LANDED` ยังเป็น `False`
  🔴 **บรรทัดนี้ไม่ใช่ประวัติ** ยังเป็นเกตของทุกการบูต — โคลนเก่า/สาขาเก่าให้ผลว่างได้ ให้รันเองทุกครั้ง
  🔴 **แก้บันทึกที่ผิด (chief R316 · หลักฐาน git ไม่ใช่จดหมาย)**: `COO 0745` ข้อ ② เขียนว่าตัวปลดของ chief "เขียวแล้วตั้งแต่ตอนเขียนใบ" และว่า chief วัด `d916725` ที่ "เก่ากว่าหัวจริง" — **ไม่จริง** · `git log -1 75f242f0` = `2026-09-03T00:41:09Z` = **07:41+07** แต่ใบ `CHIEF-REPORT 0715` เขียน **07:15+07** และ `git show d9167254:...login_speed.py | grep -c held_by_the_speed_deferral` = **0** ⇒ ตอน chief เขียนว่า "push แล้ว รอ merge" **นั่นถูกต้อง** เกตยังไม่ขึ้น main อีก 26 นาที · บันทึกไว้ที่นี่เพื่อไม่ให้รอบหลังอ้างผิด

> Opened by chief per direct COO order `notes_to_chief/20260901_1642_COO-ORDER-speed-sparse-x7-chief-open-gt-entry.md`,
> itself citing `20260901_1640_COO-ORDER-speed-sparse-x7-approved-panya-live-override-of-1447.md` (LANE-DB,
> approves a sparse x=7-only write path in `persistence_attr_compose.py`, reversing part of COO-ORDER
> `1447` item 2) and `20260901_1641_COO-ORDER-speed-sparse-x7-lane-gm-wire-chat-command.md` (LANE-GM,
> wires `/speed <value>` to call it). Both orders record Panya's live confirmation in-session
> 2026-09-01 16:39+07 to proceed without waiting for the BasicAttr+0x54 player-vs-NPC value RE.
>
> **Correction to the source orders' own cross-reference:** `1640` and `1642` both write "RE-193" for
> the BasicAttr+0x54 player-vs-NPC pilot question that is explicitly NOT a blocker for this entry.
> Checked directly against `CLIENT_RE_QUEUE.md`: `RE-193` is actually
> `ACTORATTR-SEVEN-UNKNOWN-FIELDS-CLIENT-DEFAULT-VALUES-001` (unrelated, opened round `liq4ri`/R288).
> The BasicAttr+0x54 player-vs-NPC pilot RE is `RE-194 BASICATTR-0X54-SPEED-PLAYER-VS-NPC-CONFLICT-001`
> (chief opened it round `2zr22w`/R290) -- COO-ORDER `1447` itself, when opening that pilot RE, said to
> number it "after RE-193", i.e. 194 (confirmed again by `COO-DECISION 20260901_1542` item 2, same
> wording). This entry treats `RE-194` as the correct non-blocking parallel RE. Flag this numbering
> slip back to COO/chief when consuming this entry -- do not silently repeat "RE-193" as the speed-value
> ticket.
>
> Numbering: highest `GT` at open time is `GT-192`; highest `RE` in `CLIENT_RE_QUEUE.md` is `RE-195`.
> This entry is `193`.

ATTENDED: บูตด้วยทรี/ธง/env อะไร -- บูตมาตรฐาน **ไม่มีแฟล็ก scenario** ผ่าน `staged/*_boot.ps1` · `-SecondPasswordMode bypass` · run-copy `state\pirateforce_gt193_<stamp>.sqlite3` เท่านั้น (ห้ามชี้ canonical · **คัดลอกครั้งเดียวต่อรอบ**) · บัญชี GM · **ห้ามตั้ง `PF_SPEED_TRIAL`** (นั่นคือ `GT-218` คนละใบ) · 🔴 ก่อนบูตรัน RECHECK ข้อ 6 สดทั้งสี่คำสั่ง: เจอครบสามคำ **และ** `SPEED_LOGIN_READ_LANDED: bool = True` ต้อง**ไม่เจอ** -- ผิดข้อใด = `[🔴 HOLD]` ห้ามบูต · 🔴 **อ่านหัวข้อ "ขั้น 8" (modal error / socket หลุด / บังคับรีล็อกอิน) และ reconnect gate ในเนื้อใบให้จบก่อนกดอะไรทั้งสิ้น** -- บล็อกห้าบรรทัดนี้เป็นสรุป ไม่ใช่ตัวแทนเนื้อใบ
ATTENDED: 🔴 เฟอร์นิเจอร์กันตาย ตั้งก่อนพิมพ์คำสั่งแรก (chief R316 ยกมาใส่ใบนี้เพราะ `/speed 300` เคยฆ่าตัวละครจริงใน R303) -- (1) **อัดวิดีโอต่อเนื่อง**ตั้งแต่ก่อนพิมพ์ (2) **HP แตะ 0 เมื่อไหร่ STOP ทันที** จดว่าหยุดที่ขั้นไหน teardown อยู่ดี (3) ถ้าไคลเอนต์ล็อกตัวเอง: ปิดไคลเอนต์ **แล้วรีสตาร์ตเซิร์ฟเวอร์ก่อน** จึงเปิดไคลเอนต์ใหม่ชี้ run-copy ไฟล์เดิม (ไม่รีสตาร์ต = ตัวถัดไปค้าง "connecting" ตลอดกาล) · การต้องกู้ = **FAIL ของชั้น client-observable** ไม่ใช่ขั้นวัด
ATTENDED: กดอะไร/พิมพ์อะไร -- ขั้นเตรียม (ต้องมี ไม่งั้นวัดข้อ (ข)/(ง) ไม่ได้): จัดมุมด้วย **คลิกขวาค้างลาก** เป็น NO-CRASH check (ห้าม Q/E) -> ถ่าย `BASELINE` + จด**ระยะอ้างอิงการเดินหนึ่งค่า** (เวลาข้ามช่องว่างที่รู้จัก) -> **อ่านแถว DB เก็บไว้เป็นสแนปช็อตก่อนคำสั่ง** (แทน step-7 snapshot ที่รอบนี้ไม่ได้ทำ) · จากนั้น **เฉพาะขั้น 9 และ 10**: คลิกช่องแชทยืนยัน focus ด้วยตา -> `/speed 1e40` Enter ถ่าย `STEP-C` ทันที -> `/speed fast` Enter ถ่าย `STEP-D` ทันที · 🔴 **ห้ามพิมพ์ `/speed 800` และ `/speed 100` (ขั้น 4-7)** และห้ามค่าตัวเลขอื่นที่ผ่าน parser
ATTENDED: ดูเฟรม/ค่าอะไร -- (ก) บรรทัดแชท `SPEED DENIED` หลัง `1e40` และ `TYPO REFUSED` หลัง `fast` โผล่ไหม จับเวลาหลัง Enter (ข) ความเร็ว**ต้องไม่เปลี่ยน** เทียบกับระยะอ้างอิงที่จดไว้ (ค) คอนโซลบรรทัดจังหวะเดียวกัน คัดคำต่อคำ (ขั้น 9 คาด `GM_CHAT_NO_BYTES_SENT ... why=refused_speed_persist_... character_id=<rowid>`) (ง) แถว DB หลังกดทั้งสองครั้ง byte-identical กับสแนปช็อตก่อนคำสั่ง (จ) สีป้ายทุกป้ายใน `STEP-D` บรรทัดละหนึ่งป้าย ("none" ถ้าไม่มี) (ฉ) sha256 run-copy ก่อน/หลัง **และ** canonical ก่อน/หลัง
ATTENDED: ผ่าน/ไม่ผ่านตัดสินจากอะไร -- **PASS** = เห็นทั้ง `SPEED DENIED` และ `TYPO REFUSED` ภายในราวหนึ่งวินาที ความเร็วไม่ขยับ แถว DB ไม่เปลี่ยน · **FAIL** = ปฏิเสธแล้ว**จอเงียบ** (ผิดกฎห้ามเงียบ `COO-DECISION 20260902_0147`) หรือความเร็ว/แถว DB ขยับ หรือ reconnect gate ตีที่ vital_version byte (ตรวจ**ก่อน**เกรด) · ขั้น 10 RECHECK `git grep -n "TYPO REFUSED" origin/main -- src/pirateforce_foundation/gm/` ว่าง ⇒ **SKIP ขั้น 10** เกรดใบเป็น **`PARTIAL`** (ห้าม `PASS` ห้าม `FAIL`) · 🔴 เผลอไปแตะขั้น 4-7 แล้วเห็น**ศูนย์ไบต์** = ถูกแล้ว จด `SPEED DEFERRED` **ห้ามเกรด 4-7 เป็น FAIL เด็ดขาด** · teardown เสมอ (boot stamp <= 420 นาที) · ไม่มี `OBSERVER_CONFIRMED: <ISO+07:00>` = `AWAITING-OBSERVER` ไม่ใช่ PASS

- objective: single claim -- once LANE-DB's sparse write path (mask bit x=7 / `BasicAttr+0x54` only, in
  `persistence_attr_compose.py`) is wired to LANE-GM's `/speed <value>` chat command, sending
  `/speed <value>` on a normal boot writes ONLY that one field (mask bit `0x0040`) in the persisted
  attribute block, and produces ONLY that one visible effect (movement speed) -- no other attribute,
  wire-level or DB-level, is touched by this command. This is a narrower, distinct claim from `GT-183`
  (full-55-field-block `/speed` variant, separate entry, do not merge the two).

- 🔴 db (READ FIRST -- dangerous if skipped): this entry MUST run against a run-copy DB produced by one
  of the `staged/*_boot.ps1` jobs (e.g. `staged/087_gt008_boot.ps1`), which copy
  `state\pirateforce.sqlite3` (canonical) to a fresh timestamped run-copy
  (`state\pirateforce_gt193_<stamp>.sqlite3` or equivalent) BEFORE boot. **This entry must never point a
  boot at the canonical file directly.** Record the run-copy's filename and sha256 before/after this
  round, and separately verify the canonical file's own sha256 is byte-identical before and after (it is
  never opened for this test).

- server args: standard boot via a `staged/*_boot.ps1` job as above (`-SecondPasswordMode bypass`), GM
  account from `config/gm_accounts.json`. Requires `pirate-force-server@main` at or after the commit
  that ships BOTH (a) LANE-DB's sparse x=7-only write function in `persistence_attr_compose.py` and
  (b) LANE-GM's `/speed <value>` chat-command wiring that calls that function (not the full-block path
  `GT-183` exercises) -- see RECHECK.

- steps:
  1. Boot server + client per standard playbook on a `staged/*_boot.ps1` run-copy DB (see db section
     above). Confirm a fresh server start, not reused from a prior client.
  2. Log in with the GM account. Right-click-drag camera only for a clean baseline view (camera-only,
     does not change facing, emits nothing on the wire). Screenshot BASELINE, full resolution. Record
     every name label's colour in frame, one line each ("none" if nothing else visible), and a fixed
     walking reference (distance between two landmarks, or time to cross a known gap).
  3. Query the persisted attribute row for this character directly from the run-copy DB (read-only) and
     record every field's current value -- this is the pre-command wire/DB snapshot.
  4. Click into the chat box, confirm focus, type exactly `/speed 800`, press Enter.
  5. Walk the fixed distance from step 2 using normal WASD movement. Screenshot STEP-A. Record whether
     the character visibly moves faster than baseline, and every name label's colour again.
  6. Re-query the same persisted attribute row from the run-copy DB. Diff field-by-field against the
     step-3 snapshot.
     🔴 [COO-DECISION `20260903_0649` item ③, one sentence, added by chief round R315] A CHANGED ROW HERE
     DOES NOT MEAN THE CLIENT WILL RECEIVE THAT VALUE AT THE NEXT LOGIN: once the gate of `COO-DECISION
     20260903_0645` is on `main` (RECHECK item 6 above -- pushed in R315, not merged at the time this line
     was written), `login_speed.resolve_for_character` returns the wire CONSTANT (400.0, reason
     `wire_deferred`) for as long as `gm/speed_wire.send_deferred()` is true, so this diff grades the WRITE
     only. Nothing in this step may be read as "the value was delivered".
  7. Repeat steps 3-6 once more with `/speed 100` (STEP-B, expect visibly slower than baseline).
  8. [COO-DECISION `20260901_1847`, item 4] Between step 4 and step 5, before anything else: watch for a
     client-side modal error, a dropped/closed socket, or a forced reconnect-and-relogin immediately after
     the `/speed <value>` line is sent. This checks the `UpdateAttrVital` (0x309A) `vital_version` byte
     specifically -- chief set it to `0` this round (`attr_wire.UPDATE_ATTR_VITAL_VERSION_CONFIRMED`),
     picked from the converging pattern of two OTHER, independently-proven vital_version bytes in the same
     wire family (`gm/state_wire.py` and `gm/teleport_wire.py`, both `0`), not measured against a real
     client for THIS opcode. `GT-101` already showed what a wrong version byte does: modal error,
     connection halted, socket closed.
  9. 🔴 THE REFUSAL STEP (added R299, COO-DECISION `20260902_0345`). After step 7, with the chat box
     focused, type exactly `/speed 1e40` and press Enter. That value parses as a finite number (so the
     grammar accepts it) and the typed column then refuses it, which is one of the nine refusal paths.
     Screenshot STEP-C at full resolution IMMEDIATELY, showing the chat area. Record: (a) does a chat
     line reading exactly `SPEED DENIED` appear, y/n, and how long after Enter; (b) does the character's
     speed change at all (it must not); (c) the server console line for the same moment
     (`GM_CHAT_NO_BYTES_SENT ... why=refused_speed_persist_... character_id=<rowid>`), copied verbatim.
     Then re-query the DB row and confirm it is byte-identical to the step-7 snapshot.
  10. 🔴 THE TYPO STEP (added R303, `COO-DECISION 20260902_0647`; the code is `pirate-force-server`
     **PR #568, MERGED 2026-09-02T13:05+07:00** -- chief verified on `origin/main` `ebfbffbe`:
     `gm/chat_command_action.py` 1 hit, `gm/say_wire.py` 2 hits). Run the RECHECK anyway before
     grading -- if it comes back empty you are on a stale clone, and then SKIP this step and say so
     in the result rather than grading it a FAIL:
     `cd pirate-force-server && git fetch origin && git grep -n "TYPO REFUSED" origin/main -- src/pirateforce_foundation/gm/`
     Zero hits = #568 is not merged yet = step 10 does not exist on the build you booted.
     With the chat box focused, type exactly `/speed fast` and press Enter. That value does NOT parse
     as a number, so it never reaches the typed column -- it is the GRAMMAR path, a different path
     from step 9's, and until #568 it answered with total silence on screen.
     Screenshot STEP-D at full resolution IMMEDIATELY, showing the chat area. Record: (a) does a chat
     line reading exactly `TYPO REFUSED` (12 printable ASCII characters) appear, y/n, and how long
     after Enter; (b) does the character's speed change at all (it must not); (c) the server console
     line for the same moment, copied verbatim; (d) every name label's colour in STEP-D.
     Then re-query the DB row and confirm it is byte-identical to the step-7 snapshot.
     🔴 Step 9 and step 10 are SEPARATE claims about SEPARATE code paths (typed-column refusal vs.
     parse failure). A `SPEED DENIED` seen in step 9 is not evidence for step 10 and vice versa.

- pass criteria (two layers, kept separate):
    reconnect gate (check FIRST, before grading speed/wire/DB below): if step 8 observes a reject/
      reconnect, this entry is a hard FAIL on the vital_version byte specifically -- record the exact
      client-visible symptom, do NOT proceed to grade steps 5-7's speed/wire/DB claims from the same
      attempt (a rejected frame did not carry a speed change to grade), and do NOT try a second guessed
      byte value in the same attended round. Stop and open a new RE ticket scoped to proving the real
      `UpdateAttrVital` vital_version byte before re-attempting this entry.
    wire/DB: (a) the server console/capture log shows, after each `/speed <value>` line, a frame whose
      decoded change-mask has bit `0x0040` (`BasicAttr+0x54`, x=7) set and NO other bit set; (b) the
      step-3-vs-step-6 DB row diff (both `/speed 800` and `/speed 100` passes) shows exactly ONE changed
      field -- the speed column, matching the typed value -- byte-identical everywhere else in the row.
      Both (a) and (b) are headless-provable from the console log and the DB file alone and need no
      human at the screen. If either the frame or the DB diff shows ANY other field/bit touched, that is
      a FAIL of this entry's sparse-only claim regardless of whether the speed field itself changed
      correctly -- record exactly which extra field/bit appeared. This is also the exact observation
      LANE-DB's open "25-field resend" question wants watched for (see nonclaim 2); report what was seen
      there too, but this entry does not have to resolve that wider question to close.
    client-observable (refusal, added R299): the human sees the chat line `SPEED DENIED` -- twelve ASCII
      characters, exactly that spelling -- within a second of the step-9 Enter, and the character's speed
      does not change. A refusal that is still SILENT on screen is a FAIL of COO-DECISION `20260902_0147`'s
      forbidden-silence rule and must be recorded as such even if every other layer of this entry passes.
      🔴 WHAT THIS STEP DOES NOT COVER, so a green here is not read wider than it is: a TYPO
      (`/speed fast`) is refused by the command GRAMMAR, one layer above the nine paths the notice was
      wired into, and is STILL silent on screen. Chief reported that gap to COO in the R299 letter rather
      than widening the decision on his own. Do not grade the typo case from this entry.
    client-observable: what the human at the screen reports for STEP-A/STEP-B against BASELINE -- does
      the character visibly move faster after `/speed 800` and visibly slower after `/speed 100`, with
      no other visible change (no glitch, no name-label colour change, no other stat/appearance shift).
      A result where the character does not visibly change speed at all is a valid, useful negative --
      it would point at the sparse path either not reaching the client or being ignored client-side.

- nonclaims:
  1. Does not test the full-55-field-block `/speed` variant -- that is `GT-183` (separate claim, separate
     entry, currently `BLOCKED`; do not close or supersede it with this entry's result).
  2. Does not close LANE-DB's open "25-field resend" question -- only reports what is observed while
     this narrower x=7-only path runs once. A clean result here is not proof the wider question is
     answered; a dirty result (extra field touched) is direct, useful input to that question.
  3. Does not confirm `400` is the table-correct default walking speed, and does not depend on `RE-194`
     (`BasicAttr+0x54` player-vs-NPC value, corrected number -- see provenance note above) closing
     first. Per the COO order this entry may run in parallel; `RE-194` is backward-confirming evidence
     only, not a gate.
  4. Does not test negative, zero, or extreme values beyond `800`/`100` -- new edge values are a
     separate entry, per the one-entry-one-claim rule.
  5. Does not test `/speed` interacting with movement-lock fields (x41/x42) -- out of scope.
  6. Does not test persistence across relog/reconnect -- single, unbroken session only.

- RECHECK (must all pass BEFORE booting an attended round -- WIRED v2, do not call the owner to the
  screen until this passes headless):
  1. ⬜ **NOT YET.** `grep -n "def " pirate-force-server/src/pirateforce_foundation/persistence_attr_compose.py
     | grep -i sparse` shows nothing on `main` as of R294 (`happy-dirac-69cabr`/`focused-turing-69cabr`,
     2026-09-01T21:2x+07:00) -- LANE-DB's DB-persistence half of this interface has not shipped. Re-check
     under whatever name LANE-DB actually ships it.
  2. ✅ **DONE, but not where this RECHECK originally said to look.** The chat-command call site lives in
     `pirate-force-server/src/pirateforce_foundation/gm/chat_command_action.py`'s `_speed_action`
     (dispatched from `command.name == "speed"`, right after `gmprobe`), NOT a direct `/speed` string in
     `runtime.py` -- `runtime.py`'s own call site (`chat_command_action.make_gm_chat_command_action(...)`)
     was already the single generic entry point for every GM chat command before this round, unchanged.
     Verify instead with `grep -n 'command.name == "speed"' pirate-force-server/src/pirateforce_foundation/gm/chat_command_action.py`.
     Confirmed dispatches to `gm.speed_wire.compose_sparse_speed_update` (the x=7-only sparse composer),
     not the full-block `attr_wire.build_named_field_update` path `GT-183` depends on.
  3. ⬜ **NOT RUN** -- blocked on item 1 (no DB-side write to observe yet). Do not attempt until item 1
     ships.
  4. 🔴 **UPDATED R298 (`dfx8bu`, 2026-09-02T03:1x+07:00) -- items 1 and 3 are now CLOSED, and a THIRD
     condition took their place. Read this before item 4's original text below.**
     * item 1 ✅ **CLOSED**: LANE-DB's write path is on `main` and `_speed_action` calls it FIRST --
       `store.write_typed_attributes_and_compose_sparse(character_id, {"speed_walk": value})`, then the
       frame is composed from the store's READ-BACK, not from the GM's typed text. So step 6 of this
       entry ("re-query the same persisted attribute row ... diff field-by-field") finally has something
       to diff; before this it returned an empty diff every time and this entry could only ever have
       graded a frame, never a memory. (LANE-GM round `hw6dix`, letter
       `notes_to_chief/20260902_0129_LANE-GM-STATUS-speed-writes-the-row-gt193-condition-b-closed.md`.)
     * item 3 ✅ unblocked by the above.
     * 🔴 **THE ONE REMAINING BLOCKER, and it is not LANE-GM's:** `COO-DECISION`
       `notes_to_chief/20260902_0147_COO-DECISION-speed-db-first-then-wire-refusal-must-be-visible.md`
       makes a visible refusal MANDATORY -- "every time it refuses because of the DB it must answer with
       a message in chat the GM sees immediately; SILENT IS A FORBIDDEN OUTCOME, the tester must be able
       to tell 'typo' / 'DB rejected' / 'frame sent' apart FROM THE SCREEN".
       **[วัดแล้ว R298]** all NINE non-success exits of `/speed` are silent to the screen: every refusal
       returns `_Verdict(None, ...)`, `runtime.py:7513-7518` only queues an action that `is not None`, so
       ZERO frames leave the server. `_note()` appends to an in-memory `session.events` list, `_log_outcome`
       writes an ndjson file, `_announce_console_outcome` writes the server's stderr -- none of the three
       is a screen the tester is looking at. Measured by running the real `make_gm_chat_command_action`
       with the real encoder, with a success control that DID return a frame tuple.
       ⇒ **status stays `PENDING interface`. Do NOT promote to `READY` and do NOT call the owner.**
       Booting this today burns an attended round: she types `/speed 400`, nothing happens, and she cannot
       tell a rejected write from a dead GM lane. Full analysis and the smallest correct wiring (it must
       live in `gm/say_wire.py` -- `test_gm_say_gate_lock.py` forbids any other GM file from touching the
       channel codec) is in `notes_to_chief/20260902_0311_CHIEF-REPLY-gt193-stays-pending-speed-refusal-is-silent-on-screen.md`;
       the architectural half went to COO in `20260902_0313_CHIEF-ASK-COO-say-gate-lock-matches-module-name-not-channel-id.md`.
       ⚠️ When that wiring lands it proves the **wire** layer only: `docs/FUNCTIONAL_COVERAGE.json:742-760`
       (GT-009, attended) proved the client renders a **12-ASCII-character** LocalTalk message and measured
       a 5-character one staying silent; the refusal text is 26 characters, so "the GM sees it" needs its
       own attended entry and must never be claimed from this one.

  5. ✅ **PASSED R299 at 06:2x+07:00** (verified against `origin/main` at `dd2d4ca3`, after PR #542 merged as
     `d2d61ff8`: the grep prints `SPEED_DENIED_NOTICE_TEXT = "SPEED DENIED"` at `say_wire.py:136`, and the
     33 tests are green on that clone). Original text of this item kept below so the next reader can re-run it.
     🔴 **ADDED R299 -- THE GATE THIS WAS.** On a fresh `pirate-force-server@main` clone:
     `grep -rn "SPEED DENIED" src/pirateforce_foundation/gm/say_wire.py` must print the notice text, and
     `python3 -m pytest tests/test_gm_speed_denied_notice.py -q` must be green (22 tests; all nine refusal
     paths decode a 0xAC52 frame whose body is exactly `SPEED DENIED`). Empty grep = chief's PR has not
     merged yet: status is still not `READY`, do not boot, do not call the owner. Built and green on the
     cloud sanity suite in R299 (chief, branch `claude/beautiful-shannon-aa9ajr`); the WIRE half only --
     nobody has yet seen the line render, which is exactly what step 9 above is for.

     --- original item 4 text, kept for the record: ---
     Item 1 still failing (and item 3 therefore un-run) means the interface has not fully shipped: status
     stays `PENDING interface`. **Do not promote this entry to `READY` yet.** What changed this round: the
     wire-compose half (chat command -> sparse frame, version-gated) is on `main`, tested (17+8 new tests,
     full suite 6434/0 failed), and adversary-reviewed (pf-adversary found and a follow-up fix closed a
     real gap: the send was reachable against a canonical-named DB with no check -- now gated on
     `session.foundation.lifecycle.store.path`'s filename, a heuristic not a guarantee, see
     `chat_command_action.py`'s `_speed_db_is_canonical` docstring for the stated limitation). The
     DB-persistence half is still LANE-DB's open half.

- links: `notes_to_chief/20260901_1642_COO-ORDER-speed-sparse-x7-chief-open-gt-entry.md` ·
  `notes_to_chief/20260901_1641_COO-ORDER-speed-sparse-x7-lane-gm-wire-chat-command.md` ·
  `notes_to_chief/20260901_1640_COO-ORDER-speed-sparse-x7-approved-panya-live-override-of-1447.md` ·
  `notes_to_chief/20260901_1447_COO-ORDER-re-basicattr-0x54-speed-value-hold-speed-send-gate-staged-ps1-ownership.md`
  (original hold, partially reversed by `1640`) · `CLIENT_RE_QUEUE.md` `RE-194`
  `BASICATTR-0X54-SPEED-PLAYER-VS-NPC-CONFLICT-001` (parallel, non-blocking, corrected number -- see
  provenance note) · `GT-183 GM-B-SPEED-COMMAND-001` (sibling entry, full-block variant, separate claim,
  currently `BLOCKED`) · `staged/087_gt008_boot.ps1` (run-copy DB pattern this entry's boot must follow).

- numbering: highest `GT` at open time is `GT-192`; highest `RE` in `CLIENT_RE_QUEUE.md` is `RE-195`.
  This entry is `193`.

- result:
  🔴 **RUN 1 -- R303, 2026-09-02 (attended, เจ้าของหน้าจอ): FAIL, และมันฆ่าเซสชัน**
  ใบนี้**เคยรันแล้วและล้ม** -- บันทึกไว้ตรงนี้โดย chief R316 เพราะเดิมช่องนี้ว่างเปล่า ทำให้ผู้เทสที่อ่านจากคิว
  (ซึ่งคือคนที่ป้าย `🟢 READY` มีไว้ให้) เห็นเป็นใบใหม่ที่ไม่เคยรัน · หลักฐานเต็มอยู่ที่
  `notes_to_chief/20260902_1755_KA1A-R303-RESULTS-*.md` และ `NOW.md` หัวข้อ GM-B
  - `/speed 300` ⇒ **HP 0 · เงินหาย · ตัวละครตาย** แล้ว **ไคลเอนต์ล็อกตัวเอง** (426 เฟรมถัดมาไม่มีคลิกเลยแม้แต่ครั้งเดียว)
  - ชั้น wire/DB: **DB ฝั่งเราสะอาด** (`characters.speed_walk = 300.0`, `hp 100/100`) ⇒ ความเสียหาย**ไม่ได้ถูกเขียนลง DB**
    มันอยู่ใน **เฟรมขาออกในเซสชัน** -- นี่คือเหตุผลที่เกตล็อกอิน (RECHECK ข้อ 6) **ไม่ใช่** ตัวกันประตูบานที่ฆ่าตัวละคร
  - ทางกู้ที่ใช้จริง: ปิดไคลเอนต์ **แล้วรีสตาร์ตเซิร์ฟเวอร์ก่อน** จึงบูตไคลเอนต์ใหม่ (ไม่รีสตาร์ต = ตัวถัดไปค้าง "connecting" ตลอดกาล)
  🔴 **กฎที่ยกมาจาก `GT-218` โดย chief R316 เพราะใบนี้อันตรายกว่าแต่ไม่มีเฟอร์นิเจอร์กันตาย:**
  (ก) **อัดวิดีโอต่อเนื่อง** ตั้งแต่ก่อนพิมพ์ `/speed` จนจบ ไม่ใช่ถ่ายภาพนิ่งเป็นช่วง
  (ข) **STOP ทันทีถ้า HP แตะ 0** -- หยุดทั้งรอบ ไม่ต้องทำขั้นถัดไป จดเวลาแล้วรายงาน
  (ค) ขั้น 8 (เฝ้าดู modal error / socket หลุด / บังคับรีล็อกอิน) **ต้องอ่านก่อนเริ่มขั้น 4** ไม่ใช่ตอนถึงคิวมัน
  (ง) วันที่ประตูขาออกเปิด (ดูตัวรีล็อกใน RECHECK ข้อ 6) **ใบนี้ห้ามบูตก่อน `GT-218`** ซึ่งครอบค่า `400` ค่าเดียวและมีหลักฐานสามแหล่ง
  RUN ถัดไป (tester/build lane เติม): PASS/FAIL/BLOCKED, evidence, timestamp, OBSERVER_CONFIRMED line
  per G-OBS once client-observable evidence exists

**ผู้เปิดใบ: chief รอบ `57alcd` 2026-09-01 (cloud), per COO-ORDER `1642`**

## 🆕🔬 GT-194 UI-B-LOGOUT-VITALCOUNT-ENVELOPE-FIX-001 [attended, in-game, 🟢 READY — RECHECK 1-3 all passed, chief round `f7zt8z` (R295)]: หลังแก้ `classify_logout_attempt` แล้ว ปุ่ม "ออกจากเกม" (UI-B) ตอบกลับจริงไหมตอนไคลเอนต์ห่อ vital อื่นมาด้วย

ATTENDED: [GATE ก่อนบูตทุกครั้ง] ใบสั่งว่า RECHECK ต้องผ่านครบก่อนเปิดจอเรียกผู้เทส (R295 ผ่านแล้วแต่ตัวเลขเน่าได้ ให้รันสด): (1) หาเลขบรรทัด `classify_logout_attempt` สดก่อน (R295 ขยับไป 1458-1503 ห้ามเชื่อ 1451-1465 ตาบอด) แล้ว `(cd pirate-force-server && sed -n '<from>,<to>p' src/pirateforce_foundation/logout_hypothesis.py | grep -n "vital_count == 1")` -- เช็ค envelope ต้องเป็น `vital_count >= 1` ไม่ใช่ `== 1` (เจอ `parsed.vital_count == 1` ที่เป็น branch เลือกวิธีเทียบ payload = ปกติตาม R295 ไม่ใช่ตก) (2) `(cd pirate-force-server && python3 -m pytest tests/test_logout_request_envelope.py tests/ -k logout -q)` เขียวทั้งชุดและ skip ยังเป็น 3 -- ห้ามใช้เลข 126 (เน่าแล้ว) (3) `tests/test_logout_hypothesis.py::LogoutHypothesisRuntimeTests::test_real_capture_with_wrapped_vitals_now_dispatches` ผ่าน · ข้อใดตก/ว่าง = ห้ามบูต ใบกลับเป็น BLOCKED-ON-WIRING
ATTENDED: บูตด้วยทรี/ธง/env อะไร -- ใบนี้ไม่เขียนคำสั่งบูต ไม่มีแฟล็ก/env/ฉากพิเศษใด ๆ (ไม่มี placeholder ค้าง) => บูตมาตรฐานตาม `ATTENDED_SESSION_RUNBOOK.md` ไม่มีแฟล็ก `--*-scenario` · DB สำเนา run-copy ของ `state\pirateforce.sqlite3` เท่านั้น (ห้ามเปิด canonical · เทียบ sha ก่อน/หลัง) · เซิร์ฟก่อน ไคลเอนต์ทีหลัง · เก็บ server console/capture log `2>&1` ไว้ทั้งรอบ (ชั้น wire ของใบต้อง grep จากล็อกนี้ ไม่มีล็อก = วัดชั้น wire ไม่ได้) · ทรีต้องมี fix ของ chief รอบ `f7zt8z` (R295) อยู่จริง ยืนยันด้วย GATE บรรทัดบน
ATTENDED: กดอะไร/พิมพ์อะไร -- ใบสั่งเท่านี้: ทำให้เซสชันมี vital อื่นค้างอยู่จริงก่อน (เดิน / สู้ / เปิด dialog) แล้วจึงกดปุ่ม "ออกจากเกม" (UI-B) · ห้ามกดตอนเพิ่งล็อกอินสด ๆ ที่ไม่มี pending vital (นั่นคือเคสที่ผ่านอยู่แล้ว ไม่ตอบคำถามของใบ) · ต้องทำครบ อย่างน้อย 2 ครั้งติดต่อกัน โดยสร้าง vital ค้างใหม่ก่อนกดทุกครั้ง · ห้ามทดสอบปุ่ม "กลับหน้าเลือกตัวละคร" (UI-A / subcode 3) ใบนี้ไม่คลุม · ใบไม่ระบุพิกัดคลิกปุ่มและไม่ระบุวิธีกลับเข้าเกมรอบสอง ให้ทำตาม runbook ปกติ (ค้าง "connecting" ระหว่างครั้งที่ 1 กับ 2 = บันทึกแยก/NO-RESULT ไม่ใช่ FAIL ของใบ)
ATTENDED: ดูค่า/โทเคนอะไร ที่จอไหน -- ชั้น client-observable (ต้องมีคนดูจอ): กดแล้วเกมตอบสนองจริงไหม ออกจากเกม/กลับหน้าล็อกอินตามพฤติกรรมที่ตั้งใจ ถ่ายภาพนิ่งเต็มความละเอียดทุกครั้งที่กด · ชั้น wire/DB (headless ทำได้ก่อนเปิดจอ): `python3 -m pytest tests/test_logout_request_envelope.py -q` ต้องยังผ่าน 18/18 หลังแก้ (regression guard) และ grep console/capture log ของรอบเทสนี้ว่า `_dispatch_logout_hypothesis` ตอบกลับจริง ไม่ใช่ `logout_hypothesis_wrong_envelope_no_reply` ตอน `vital_count == 4` (เฟรม 119 ไบต์แบบใบ `1930`, envelope vital-count byte `0x04`) · ถ้าปุ่มไม่ตอบ ต้อง grep บันทึกให้ได้ว่า vital_count ตอนนั้นคือเท่าไหร่
ATTENDED: ผ่าน/ไม่ผ่านตัดสินจากอะไร -- PASS = ชั้นจอเห็นปุ่มตอบสนองจริงครบ 2 ครั้งติดในเซสชันที่มี vital ค้าง และ ชั้น wire ครบตามบรรทัดบน (สองชั้นแยกกัน ห้ามใช้ชั้นหนึ่งเป็นหลักฐานแทนอีกชั้น) · FAIL = ปุ่มไม่ตอบสนองเหมือนเดิม พร้อมจด vital_count ตอนนั้น · ใบไม่คลุม subcode 3/UI-A, `HYP-PF-040`, และ persistence หลัง logout -- ความผิดปกติเรื่องพวกนี้จดแยกเป็นข้อมูล ไม่ใช่ FAIL ของใบ · จดสีป้ายชื่อทุกป้ายในทุกภาพจากภาพเต็มความละเอียด (`none` ถ้าไม่มี · ห้ามอนุมานสาเหตุจากสี) · teardown เสมอแม้รอบจบเพราะเลิกเล่นเฉย ๆ (boot stamp <= 420 นาที) · ไม่มี `OBSERVER_CONFIRMED: <ISO+07:00>` ตาม G-OBS = `AWAITING-OBSERVER` ไม่ใช่ PASS

### ที่มา

รอบ `xlraox` (2026-09-01T20:07+07:00) พบว่าไบต์จับสดจริงของปุ่ม UI-B ("ออกจากเกม") ยาว 119 ไบต์
(envelope vital-count byte `0x04`) ไม่ใช่ 34 ไบต์อย่างที่ pin ไว้ เพราะไคลเอนต์ห่อ vital อื่นอีก 3 ตัว
มาด้วยตามสภาพเซสชันจริง -- `classify_logout_attempt` (`logout_hypothesis.py:1457`) เช็ค
`parsed.vital_count == 1` เป็น hard requirement ก่อนเทียบ payload เลย เฟรมจริงตกที่เช็คนี้ทันทีและ
`_dispatch_logout_hypothesis` ไม่ตอบอะไรเลย -- ยืนยันด้วย parser จริงของ `current/pf_login_game_server_v141.py`
(อ่านอย่างเดียว) ไม่ใช่แค่ทฤษฎี รายละเอียดเต็มใน
`notes_to_chief/20260901_2007_LANE-A-CORE-REQUEST-logout-vitalcount-envelope-gap-classifier-built.md`

โมดูล+เทสยืนยันโครงสร้างสร้างเสร็จแล้ว (`src/pirateforce_foundation/logout_request_envelope.py`,
18/18 ผ่าน) แต่ยังไม่ได้ wire เข้า dispatch จริง -- ไฟล์ที่ต้องแก้ (`logout_hypothesis.py`) ล็อกอยู่ที่
chief ใบนี้เปิดไว้ล่วงหน้าตามธรรมเนียมโปรเจกต์ (เทียบ `GT-190`, `GT-193`) เพื่อไม่ต้องเปิดใบใหม่ทีหลัง

**สถานะ 🟢 READY (แก้แล้ว):** chief รอบ `f7zt8z` (R295) แก้ `classify_logout_attempt` ตามข้อเสนอ (ก) จริง
(`vital_count >= 1` + `nested_payload[:14]` เมื่อ `vital_count >= 2`, ยังคงเทียบเท่ากันทั้งไบต์เมื่อ
`vital_count == 1` -- pf-adversary รอบแรกจับข้อบกพร่องจริง (เดิม `[:14]` ใช้แบบไม่มีเงื่อนไข ⇒
เฟรม `vital_count == 1` ที่มีขยะต่อท้าย 50 ไบต์จะผ่านด้วย ทั้งที่ก่อนแก้ปฏิเสธ) แก้แล้วด้วย branch สอง
ทาง แยกตาม `vital_count`) RECHECK ทั้งสามข้อด้านล่างผ่านครบ (ดูผลจริงต่อท้ายแต่ละข้อ) -- **พร้อมเปิดจอเรียก
ผู้เทสได้แล้ว**

### objective

หลัง chief แก้ `classify_logout_attempt` ตามข้อเสนอ (ก) หรือ (ข) ในจดหมาย `2007` แล้ว ให้ผู้เทสกดปุ่ม
"ออกจากเกม" (UI-B) จริงในสถานการณ์ที่ไคลเอนต์มักมี vital อื่นค้างอยู่ในเซสชัน (ไม่ใช่บัญชีเพิ่งล็อกอิน
สด ๆ ที่ไม่มี pending vital ใด ๆ) แล้วดูว่าปุ่มตอบสนองจริงหรือไม่

### pass criteria — สองชั้น

**ชั้น client-observable:** ผู้เทสกดปุ่ม "ออกจากเกม" แล้วเห็นเกมตอบสนองจริง (ออกจากเกม/กลับหน้า
ล็อกอินตามพฤติกรรมที่ตั้งใจ) อย่างน้อย 2 ครั้งติดต่อกันในเซสชันที่มี vital อื่นค้างอยู่จริง (เดิน/สู้/
เปิด dialog มาก่อนกดปุ่ม) ไม่ใช่แค่ตอนเพิ่งล็อกอิน -- ปุ่มไม่ตอบสนอง (เหมือนเดิม) ⇒ FAIL, บันทึกว่า
vital_count ตอนนั้นคือเท่าไหร่ (grep console/capture log)

**ชั้น wire/DB (headless, ทำได้ก่อนเปิดจอ ตาม `PANYA-DECISION 2026-08-27 20:10`):**
`python3 -m pytest tests/test_logout_request_envelope.py -q` ต้องยังผ่าน 18/18 หลังแก้ (โมดูลนี้ไม่ถูก
แตะโดยการ wire -- เป็น regression guard) และ server console/capture log ของรอบเทสต้องโชว์ว่า
`_dispatch_logout_hypothesis` ตอบกลับ (ไม่ใช่ `logout_hypothesis_wrong_envelope_no_reply`) เมื่อ
`vital_count == 4` เหมือนเฟรมจับจริงของใบ `1930`

### nonclaims

1. ไม่อ้างว่าการแก้นี้คือสาเหตุเดียวที่ UI-B ค้าง -- เป็นบั๊ก dispatch จริงที่ยืนยันแล้วหนึ่งจุด อาจมี
   จุดอื่นที่ยังไม่เจอ (ดูหัวข้อ HYP-PF-040 ในจดหมาย `2007`)
2. ไม่ทดสอบ subcode 3 (UI-A, "กลับหน้าเลือกตัวละคร") -- ไบต์จับสดของปุ่มนั้นตรง pin เดิม 34/34 อยู่แล้ว
   ไม่มีอะไรต้องแก้ฝั่งนั้น (แยกเป็นเรื่อง `HYP-PF-040`/`RE-197` คนละประเด็น)
3. ไม่ยืนยัน/ปฏิเสธ `HYP-PF-040` (ตัวแยกปุ่มตอน dialog เปิด) -- ใบนี้เทสเฉพาะ dispatch-level fix ของ
   vital-count envelope เท่านั้น
4. ไม่ทดสอบ persistence หลัง logout (ข้อมูลตัวละครถูกเซฟถูกต้องหรือไม่) -- แยกเป็นใบอื่นถ้าจำเป็น

### RECHECK (ต้องผ่านครบก่อนเปิดจอเรียกผู้เทส)

🔴 แก้แล้วหลัง pf-adversary รอบนี้ชี้สองจุด: (1) เดิม item 1/2 อ้าง cwd ต่างกัน (parent-dir-relative
vs repo-root-relative) สั่งต่อกันจะพังเงียบ ๆ -- ทุกข้อด้านล่างนี้ล็อก `cd pirate-force-server` เข้าไป
ในคำสั่งเองแล้ว ไม่พึ่ง cwd ผู้รัน (2) เดิม `grep -n "vital_count == 1"` ทั้งไฟล์ชนกับ decoy ที่บรรทัด
1560 (`classify_worldinfo_frame`, คนละฟังก์ชัน ไม่เกี่ยวกับใบนี้) ⇒ จะมี hit ค้างตลอดแม้แก้แล้ว --
item 1 เปลี่ยนเป็น `sed` ตัดเฉพาะช่วงบรรทัดของ `classify_logout_attempt` ก่อน grep เพื่อไม่ให้ชน decoy

1. `(cd pirate-force-server && sed -n '1451,1465p' src/pirateforce_foundation/logout_hypothesis.py | grep -n "vital_count == 1")`
   ต้อง **ไม่เจอ** อะไรเลย (exit code เป็น grep-no-match) -- ถ้ายังเจอแปลว่า `classify_logout_attempt`
   เองยังไม่ถูกแก้ (เปลี่ยนเป็น `>= 1` ตามข้อเสนอ (ก) หรือเรียก
   `logout_request_envelope.classify_logout_vital_request` แทนตามข้อเสนอ (ข)) -- ถ้าบรรทัด 1451-1465
   ขยับเพราะโค้ดก่อนหน้าถูกแก้ไปด้วย ให้หาเลขบรรทัดของฟังก์ชันใหม่ก่อนรัน อย่าเชื่อเลข 1451-1465 เดิม
   ตาบอด
   — 🟢 **[วัดแล้ว R295]** ฟังก์ชันขยับไป `1458-1503` เพราะเพิ่ม docstring อธิบายการแก้ -- รันซ้ำที่
   `sed -n '1458,1503p' ... | grep -n "vital_count == 1"` = **ไม่เจอ** จริง (มีแต่ `vital_count >= 1`
   ในเช็ค envelope และ `parsed.vital_count == 1` เป็นเงื่อนไข branch แยกต่างหากสำหรับเลือกวิธีเทียบ
   payload ไม่ใช่เงื่อนไข envelope เดิมที่ใบนี้เตือนไว้)
2. `(cd pirate-force-server && python3 -m pytest tests/test_logout_request_envelope.py tests/ -k logout -q)`
   ผ่านทั้งหมด (regression guard -- ห้ามมีเทส logout เดิมพังจากการแก้)
   — 🟢 **[วัดแล้ว R295]** ~~`126 passed, 3 skipped`~~ (skip เดิม ไม่ใช่ของใหม่)
   🔴 **ตัวเลขนี้เน่าแล้ว แก้โดย LANE-A (เจ้าของใบ) รอบ `1d6rta` ตาม pf-adversary D10:** คำสั่งเดียวกัน
   บน `main` วันนี้ให้ **`182 passed, 3 skipped`** และหลังเทสของรอบ `1d6rta` ให้ **`191 passed, 3 skipped`**
   ⇒ ผู้เทสห้ามใช้เลข 126 เป็นเกณฑ์ · เกณฑ์จริงคือ **เขียวทั้งชุด และจำนวน skip ยังเป็น 3**
3. Headless replay เฟรม 119 ไบต์จริงของใบ `1930` (หรือแคปเจอร์ใหม่ที่เทียบเท่า) ผ่าน dispatch จริง แล้ว
   `grep` console log ยืนยันว่าไม่ใช่ `logout_hypothesis_wrong_envelope_no_reply` อีกต่อไป
   — 🟢 **[วัดแล้ว R295]** ใหม่: `tests/test_logout_hypothesis.py::LogoutHypothesisRuntimeTests::
   test_real_capture_with_wrapped_vitals_now_dispatches` ขับผ่าน `state.dispatch(...)` จริง (ไม่ใช่
   เรียก `classify_logout_attempt` โดด ๆ) ด้วยเฟรม 119 ไบต์ตัวเดียวกับใบ `1930` ทุกไบต์ (ยืนยัน
   byte-identical กับต้นฉบับใน `test_logout_request_envelope.py` แล้ว) -- ยืนยันว่า
   `"logout_hypothesis_wrong_envelope_no_reply"` **ไม่อยู่ใน** `state.events` และ action ที่ได้คือ
   `HYP_PF_012_LOGOUT_SUBCODE01_ACK_AFTER_CLEAN_CLOSE` (ack จริง, session `closed_at` ถูกเซ็ต) --
   `test_captured_exit_game_frame_now_classifies_exact_01` (`test_logout_request_envelope.py`) ยืนยัน
   ระดับ `classify_logout_attempt` โดยตรงอีกชั้นเช่นกัน
4. ผลลบ/ว่างจากข้อ 1-3 ข้อใดข้อหนึ่ง = ยังไม่พร้อม สถานะคงเป็น `BLOCKED-ON-WIRING` ห้าม promote เป็น
   `READY` — **ทั้งสามข้อผ่านหมด ⇒ promote เป็น `READY` แล้ว** (บรรทัดหัวใบด้านบน)

### links

`notes_to_chief/20260901_2007_LANE-A-CORE-REQUEST-logout-vitalcount-envelope-gap-classifier-built.md`
(จดหมายเปิดประเด็นนี้ พร้อมข้อเสนอ (ก)/(ข) และเลขบรรทัด) ·
`notes_to_chief/20260901_1930_KA1A-CAPTURE-*.md` (ที่มาไบต์จับสดจริง, ย้ายไป `consumed/`) ·
`src/pirateforce_foundation/logout_request_envelope.py` ·
`tests/test_logout_request_envelope.py` · `src/pirateforce_foundation/logout_hypothesis.py:1451-1465`
(จุดที่ต้องแก้) · `RE-197` (คำถามคู่ขนานเรื่อง `#1398`, ไม่บล็อกใบนี้) · `GT-186` (UI-B precedent,
บล็อกซ้ำสองรอบเทสก่อนพบสาเหตุนี้)

### numbering

highest `GT` ที่เปิดอยู่ก่อนใบนี้คือ `GT-193`; highest `RE` ใน `CLIENT_RE_QUEUE.md` คือ `RE-197`
ใบนี้คือ `194`

### result

(tester/build lane กรอก: PASS/FAIL/BLOCKED, evidence, timestamp, OBSERVER_CONFIRMED line ตาม G-OBS
เมื่อมี client-observable evidence)

**ผู้เปิดใบ: LANE-A (สาย A · WORLD) รอบ `xlraox` ต่อยอด 2026-09-01T21:28+07:00**
