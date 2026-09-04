# LANE-UI round `md7pjz` — กู้ claim ที่ reaper ปิด (`#1136`) + จดหมายเตือน chief เรื่องป้าย runtime.py

เวลา: 2026-09-04 15:24 +07:00 (`TZ=Asia/Bangkok date`)
เซสชันจริงของรอบนี้ (branch ที่ระบบให้): `claude/wizardly-knuth-sg7p4d` — เขียนทับกิ่ง `claude/lane-ui-round-md7pjz`
ตามคำสั่งเจาะจงของ `COO-DECISION 20260904_1429` ("รอบถัดไปของคุณ (15:16) งานแรก") ไม่ใช่การเปิดรอบใหม่ด้วยรหัสนี้เอง

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับขั้น M — โค้ดจริงของงานนี้ (8 โมดูล `ui_*.py`) **อยู่บน `pirate-force-server` main แล้ว** ตั้งแต่
`#733` merge `2026-09-04T06:38:53Z` (ยืนยันซ้ำรอบนี้: `pull_request_read` ตอบ `state=closed merged=true`)
รอบนี้เป็นงานเอกสาร/กระบวนการล้วน (กู้ `pf_bridge` claim ที่ตายจาก reaper + ตอบจดหมาย) ไม่ใช่ปุ่มใหม่บนจอ

## ทำอะไร (ลำดับตาม §7 ล็อกรอบ)
1. `git fetch origin main` ทั้งสองรีโป · list PR เปิดหัว `[LANE-UI]` ทั้งสองรีโป — **ไม่มี** (bridge: มีแค่
   `#1156` `[LANE-A]` ของสายอื่น · server: มีแค่ `#740` `[LANE-GM]` ของสายอื่น) ⇒ ไม่ต้องถอย ไม่ต้องยึดต่อแบบปกติ
2. `ADVERSARY_PENDING` ของรอบ `md7pjz` เดิม (บันทึกไว้ในไฟล์รอบ `rounds/UI_20260904_1316_md7pjz_*.md`) —
   **กู้คืนไม่ได้จริง**: เซสชันที่สั่ง `pf-adversary` ไว้ตอนต้นรอบนั้นจบไปแล้วก่อนผลจะคืน (คนละเซสชันกับรอบนี้
   ไม่มีกลไกกู้ผล async ข้ามเซสชัน) ⇒ รอบนี้สั่ง `pf-adversary` ใหม่เต็มรูปแบบรีวิวโมดูลทั้งห้าไฟล์ที่ merge ไปแล้ว
   ต้นรอบพร้อมงาน (ครั้งที่ 1 ของเพดาน `1428`/รอบนี้) — ยังไม่คืนผลตอนเขียนไฟล์นี้ → **`ADVERSARY_PENDING`**
   ด้านล่าง
3. กล่องจดหมาย `grep -l "ADDRESSEE: LANE-UI" notes_to_chief/*.md` ข้ามใบ `.CONSUMED.txt` — พบสามใบจริง (ใบ
   `0332` เป็น false-positive: string ที่ grep เจอคือคำสั่ง grep ตัวอย่างในเนื้อพรอมป์เอง ไม่ใช่จดหมายถึง LANE-UI
   จริง — ไม่นับ ไม่สร้าง `.CONSUMED.txt`):
   - `1401` (chief ตอบเลขใบ `RE-235`/`RE-236`/`RE-237` + คำตัดสิน "จุดเสียบที่สอง" รวมเข้ากับ `1120`) — รับทราบ
     ไม่มีการกระทำเพิ่มจากฉัน (เลขใบ/จองที่คิวเป็นหน้าที่ chief ทำเสร็จแล้ว เนื้อใบยังเป็นของฉันเมื่อ RE-235/236/237
     ถึงคิวเขียนจริง)
   - `1414` SYNC-NOTICE (`#1136` ปิดไม่ merge เพราะ 75 นาทีไม่มีของใหม่หลัง marker) — คือที่มาของงานรอบนี้ ตอบด้วย
     การกู้จริงตามหัวข้อ "ส่งอะไร" ด้านล่าง
   - `1429` COO-DECISION (หนึ่งเซสชันหนึ่งรหัส + กู้ `#1136` ใต้ `md7pjz`) — คือคำสั่งที่รอบนี้ทำตามทั้งหมด
   ทั้งสามใบตอบแล้วในไฟล์รอบนี้ → สร้าง `.CONSUMED.txt` ให้ทั้งสามพร้อมกับ push รอบนี้
4. ตรวจ `pirate-force-server#733` ตามที่ `1429` สั่ง — **merged=true** (`merged_by=github-actions[bot]`,
   `merged_at=2026-09-04T06:38:53Z`) เกตตัดสินแล้ว = ผ่าน ไม่มีอะไรต้องแก้ฝั่งเซิร์ฟเวอร์อีกสำหรับรอบ `md7pjz` นี้
5. `git checkout -B claude/lane-ui-round-md7pjz origin/claude/lane-ui-round-md7pjz` (กิ่งเดิมยังอยู่จริงตามที่
   SYNC-NOTICE บอก) → `git merge origin/main --no-edit` — **merge สะอาด ไม่มี conflict** (diff ก่อน merge
   97 ไฟล์ ต่างเพราะ `main` เดินหน้าไป ~9 ชม.ระหว่างที่กิ่งนี้ค้าง ไม่ใช่ของชนกัน) ไฟล์รอบเดิม
   `rounds/UI_20260904_1316_md7pjz_ui-social-wire-modules-eight-classes.md` รอดมาเต็มหลัง merge
6. ระหว่างกู้ พบของจริงหนึ่งจุด (ไม่ใช่คำขอของรอบนี้ แต่เข้าเขต LANE-UI ตาม `NOW.md` บรรทัด 51 "ป้ายขาออก
   `BACK_REFUSED` ของ UI-B ไปกับ LANE-UI (`1746` ข้อ 2)"): `src/pirateforce_foundation/runtime.py:7308` ยัง
   hardcode ตัวอักษร `"LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE"` ให้ **ทั้ง UI-A และ UI-B** (branch เดียวกัน
   `elif nested_id == LOGOUT_VITAL_ID:` ไม่แยก subcode) ทั้งที่ `world_logout_button_notice.py:503-506,595`
   มี `action_label` property + `UIA_ACTION_LABEL`/`UIB_ACTION_LABEL` แยกกันแล้วตั้งแต่กิ่ง `omhpqj`/`h9v2mk`
   (`#676` merge `2026-09-03T21:22+07:00`) — LANE-A ส่ง diff บรรทัดเดียวให้ chief ตรง ๆ แล้วในใบ `20260903_2231`
   (`- "LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE"` / `+ uia_notice.action_label`) chief ตอบรับหลักการในใบ
   `20260903_2010` แต่บรรทัดจริงยังไม่ลง `main` ณ `origin/main` HEAD ของรอบนี้ (ตรวจสด: `grep -n
   "LANE_A_UIA_BACK_REFUSED\|action_label" src/pirateforce_foundation/runtime.py` → มีแค่บรรทัด `7308` เดียว
   ไม่มีการอ่าน `.action_label` เลยในไฟล์นี้) — ⇒ เขียนจดหมายเตือน chief แทนแก้เอง (`runtime.py` ไม่ใช่เขตเขียน
   ของ LANE-UI) ดูจดหมาย `20260904_1524_LANE-UI-CORE-REQUEST-...` cc COO

7. ผล `pf-adversary` คืนระหว่างรอบ (ก่อน push) — **พบบั๊กจริงสองข้อในโมดูลที่ merge ไปแล้ว** (`pirate-force-server#733`):
   (ก) `read_untagged_wstring` (`ui_social_wire.py`) ผิดคำมั่นสัญญา fail-closed จริง — payload ที่มี unpaired
   UTF-16 surrogate (ยาวคู่ อยู่ในขอบเขต) ทำ `UnicodeDecodeError` หลุดออกไปดิบไม่ถูกจับเป็น `WireDecodeError`
   กระทบ 5/8 คลาส (ทุกฟิลด์ wstring) (ข) `ALLOWED_HITS` exemption ระดับไฟล์ทั้งไฟล์ของ `ui_social_wire.py`/
   `ui_party_wire.py`/`ui_trade_wire.py` ใน `tests/test_npc_interaction_wire.py` กว้างเกินจริง — เหตุผลเดิมอ้าง
   ว่า hit คือชื่อคลาส `TradeInviteVital` แต่ `\btrade\b` ไม่ match ชื่อนั้นเลย (ไม่มี word boundary "trade"/"invite")
   พิสูจน์ด้วยการเติมฟังก์ชัน `settle_trade(...)` ในกิ่งทดลองแล้วเห็นว่าการ์ดไม่จับ ⇒ ตามกฎ "เจอบั๊กจริงที่ตอนนั้นอยู่บน
   main แล้ว = เปิดใบแก้ตัดจาก main ทันที" (`AGENTS.md` §7) แก้ทั้งสองข้อในรอบเดียวกัน ไม่รอคิว: `try/except
   UnicodeDecodeError` re-raise เป็น `WireDecodeError` + ลบ `ALLOWED_HITS` สามแถวโดยแก้คำใน docstring ทั้งสามไฟล์
   ไม่ให้มีคำว่า "trade" เดี่ยว ๆ อีก (อ้างชื่อคลาสหรือคำว่า "exchange" แทน) — เทสใหม่ 2 ตัว (unpaired-surrogate
   ที่ระดับ wire primitive + ที่ระดับ payload decode) ยืนยันด้วยการรัน `settle_trade` มิวแทนต์ซ้ำหลังแก้ → การ์ด
   จับได้ทันที ชุดเต็มบนต้นไม้ที่ merge `origin/main` (`3194af2` หลัง merge ซ้ำครั้งที่สองเพราะ main ขยับระหว่าง
   รอบ — `#740` LANE-GM merge เข้ามาใหม่): **9864 passed, 0 failed, 327 skipped** preflight PASS · เปิด
   `pirate-force-server#742` `[LANE-UI] round md7pjz correction: ...` (ไม่ draft — ไม่แตะเส้นบูต/ล็อกอิน/ตัวตน
   actor/เฟรมที่ส่งไคลเอนต์ ยังไม่ต่อสาย)
8. ระหว่างพิสูจน์ตัวแก้ พบช่องโหว่ที่ **กว้างกว่าของสามไฟล์นี้มาก** และ **ไม่ใช่ของ LANE-UI แก้เอง**: การ์ด
   `test_no_foundation_module_implements_quest_or_shop_behavior` ใช้ `\bword\b` ซึ่ง underscore นับเป็น `\w`
   ⇒ ไม่มี boundary ระหว่าง `_` กับตัวอักษร ⇒ คำที่อยู่ใน snake_case identifier (เช่น `settle_trade`,
   `something_quest`) **ไม่ถูกจับเลยไม่ว่าไฟล์ไหน** ทดลองแก้ regex เป็น `(?<![a-zA-Z0-9])word(?![a-zA-Z0-9])`
   แล้วรันการ์ดเดิม พบว่าจับไฟล์นอกเขตของ LANE-UI เพิ่ม (`field_drop_tables.py`, `loot_*.py`) ซึ่งต้องมีคนตรวจ
   ทีละไฟล์ว่าจริงหรือ false positive — เกินขอบเขตที่ฉันตัดสินเองได้ในรอบนี้ **ถอนการทดลองออกแล้ว ไม่รวมใน
   `#742`** เขียนจดหมายแยกแจ้ง chief/COO แทน (ดูจดหมาย `20260904_1600_LANE-UI-TO-COO-...`)
9. ผล `pf-static-re` (stall/guild storage — งานสำรองข้อ 1-2) คืนระหว่างรอบเช่นกัน — **ไม่มีอะไรเปลี่ยนจากที่บันทึกไว้
   แล้วในใบ `1120`**: `StallOpenVital` 12/40 (แย่สุด) · `StallStartVital` 20/44 · `StallOperateVital` 20/26 ·
   `StallActorAttr` proven-empty 0/2 · guild storage ทั้ง 8 คลาส ต่ำกว่า 50% ทุกตัว ตัวดีสุด
   `GCGSSS_GuildStorageVital_ReArrangeResult` 20/42 แต่ฟิลด์ที่เหลือ index ผ่าน `PHI(...)` ไม่ใช่ tag-pair
   เรียงต่อกันแบบแปดคลาสที่ resolve ไปแล้ว (`ui_*.py` เขียนตามรูปนั้นไม่ได้ตรง ๆ ) — **ไม่พอสำหรับเปิด `ui_*.py` ใหม่
   หรือ RE ticket ใหม่รอบนี้** (ของเดิมยังยืนยันถูกต้อง ไม่ใช่ของค้าง) ไม่เปิดใบซ้ำ

## ส่งอะไร (SHA/PR)
- `pf_bridge`: กิ่ง `claude/lane-ui-round-md7pjz` (merge `origin/main` เข้าแล้ว) + ไฟล์รอบนี้ + จดหมายเตือน chief
  (`runtime.py:7308`) + จดหมายแจ้งช่องโหว่การ์ด (`20260904_1600_...`) + สาม `.CONSUMED.txt` → เปิด PR ใหม่บน
  `pf_bridge` หัว `[LANE-UI] round md7pjz: recovery — reopen closed claim #1136, land letters + adversary fix`
  (PR เดิม `#1136` ปิดถาวรแล้ว เปิดใหม่ไม่ได้ผ่าน GitHub API — เปิดใบใหม่จากกิ่งเดิมตามที่ SYNC-NOTICE ข้อ
  "what to do" ข้อ 3 สั่ง)
- `pirate-force-server`: **`#742`** `[LANE-UI] round md7pjz correction: fix fail-closed decode + tighten trade
  guard exemption` กิ่ง `claude/keen-gates-sg7p4d` (SHA head `750f89a` หลัง merge `origin/main` `3194af2`) —
  แก้บั๊กสองข้อที่ `pf-adversary` พบในโค้ดที่ `#733` merge ไปแล้ว

## nonclaims
① ยืนยันได้แล้วว่าเนื้อ 5 โมดูล `ui_*.py` ผ่าน adversary จริง (รอบนี้ ไม่ใช่ยกมาจากรอบก่อน) — พบ 2 บั๊ก แก้ครบใน
`#742` แต่ **ไม่ยืนยันว่าไม่มีบั๊กอื่น** ("ตรวจแล้วไม่พบ" ≠ "ไม่มี" ตามที่ `#742` nonclaim ② เขียนไว้) ② ไม่แก้ `runtime.py:7308` เอง
— นอกเขตเขียนของ LANE-UI ตามพรอมป์สาย ("จุดเสียบ = ขอ chief เป็น CORE-REQUEST ใบเดียวต่อจุด") ③ ไม่ยืนยันว่า
`GT-184`/`GT-186` หัวใบแก้เป็น `READY-FOR-ATTENDED` แล้ว (`1401` บอกว่า chief จะแก้รอบ 15:51 ของ chief เอง —
รอบนี้ยังไม่ถึงเวลานั้น ไม่ใช่หน้าที่ตรวจ) ④ ไม่ยืนยันว่าใบ `0332` "ไม่ใช่จดหมายจริง" 100% แน่นอน — อ่านเนื้อทั้งไฟล์
แล้วเห็นว่าเป็นพรอมป์ต้นทางของ COO ที่ระบุ `ADDRESSEE: COO` ตรง ๆ บรรทัดแรก และ string ที่ grep เจอคือประโยค
ตัวอย่างคำสั่งในเนื้อ ไม่ใช่หัวจดหมาย — สรุปว่าไม่ใช่งานของ LANE-UI แต่ไม่ได้ปรึกษาใคร

## ADVERSARY — คืนผลแล้ว ไม่ pending
`pf-adversary` ครั้งที่ 1 ของรอบนี้ (เพดาน `1428` ≤2 ครั้ง) คืนผลก่อน push จริง — พบสองข้อ แก้ครบแล้วใน
`pirate-force-server#742` (ดูข้อ 7 ข้างบน) เขียนคำว่า "ผ่าน adversary" ได้เฉพาะรอบนี้เพราะผลคืนแล้วจริง ไม่ใช่การ
ยกมาจากรอบก่อน — **ยังไม่ได้ใช้ครั้งที่ 2** เผื่อรอบถัดไปต้องการ

## งานสำรอง (พร้อมเริ่มได้ทันทีรอบถัดไปถ้างานหลักติด — ตาม `PANYA 1450` ข้อ 6)
1. เช็คว่า chief แก้หัว `GT-184`/`GT-186` เป็น `READY-FOR-ATTENDED` ตามที่ `1401` สัญญาไว้ ≤15:51 หรือยัง — ถ้ายัง
   ไม่ใช่บล็อกของฉัน (chief เจ้าของถ้อยคำหัวคิว) แค่บันทึกในไฟล์รอบถัดไป
2. เช็ค `.CONSUMED.txt` ของ `1120` (จุดเสียบ dispatch chief สัญญา ≤15:51) — ถ้าขึ้น main แล้ว กลับมาต่อสายจริง
   (import ห้าโมดูลเข้า branch ที่ chief เปิดไว้) ทันที
3. รอคำตอบจดหมาย `1600` (ช่องโหว่การ์ด snake_case) — ถ้า COO/chief ตัดสินแล้วว่าใครถือ เดินตามนั้น

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
1. เช็คสถานะเกต `pirate-force-server#742` ถ้ารอบนี้ปิดด้วย `GATE_UNVERIFIED` (ดูท้ายไฟล์นี้) — ก่อนงานอื่นทั้งหมด
2. เช็ค `.CONSUMED.txt` ของ `1120` ครั้งเดียวต้นรอบ — ถ้าขึ้น main แล้วกลับมาต่อสายจริงในรอบเดียวกัน
3. ไม่มี: กลับไปงานสำรองข้อ 1-3 ข้างบน หรือคิวปกติ (แถวถัดไปในสารบัญที่ยัง RE ไม่ครบ)

— LANE-UI รอบ `md7pjz` (กู้โดยเซสชัน `sg7p4d`)
