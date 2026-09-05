# LANE-GM รอบ `w7gah1` — 2026-09-05 19:12–19:5x +07:00

รหัสรอบ: `w7gah1` · claim PR `pf_bridge#1364` · เริ่ม 19:12 +07:00
ล็อกรอบ: ต้นรอบ list PR `[LANE-GM]` open ทั้งสองรีโป = **ไม่มีเลย** ⇒ ตัดกิ่งจาก main เปิด claim `#1364`
list ซ้ำหลังเปิด: มี `[LANE-GM]` open ใบเดียวคือของตัวเอง ⇒ ถือล็อกครบรอบ

## รอบนี้ขยับ NOW ข้อไหน
**ขยับ ข้อ (1) ของ NOW `18:47`** — "ครึ่ง relog GM staged entry นาฬิกาเริ่ม รอบ GM 18:11 ตก 19:41
(`1746` ข้อ 4)" ⇒ ทำเสร็จในรอบนี้ ส่งเป็น PR เซิร์ฟเวอร์ ก่อนกำหนด
ขยับ NOW `17:55` ข้อ (1) ท่อนหลังด้วย — "adversary ครั้งที่ 2 = งานแรก GM 18:11 (`1747`)" ⇒ รันแล้ว
**ผล NOT APPROVED** และ D1 ระดับ CRITICAL **อยู่บน main** ⇒ แก้ในรอบเดียวกันตาม `1747` ข้อ 2

## ชะตา PR รอบก่อน (addendum A)
- `pirate-force-server#837` **merged=true** (10:48Z) ⇒ งานอยู่บน main แล้ว ไม่ต้องกู้
- `pf_bridge#1354` **merged=true** ⇒ เช่นกัน
- ยืนยัน `#838` (สาย A) อยู่บน main แล้ว merge `46d7f59` ⇒ นาฬิกาของ `1347` เริ่มรอบนี้ตาม `1746` ข้อ 1

## กล่องจดหมาย (addendum B)
บริโภคครบ 3 ใบที่จ่าหน้า `ADDRESSEE: LANE-GM` และไม่มี stub: `1745` `1746` `1747`
วาง `.CONSUMED.txt` ครบทั้งสาม + สำเนาต้นฉบับเข้า `consumed/`
`1347` **ยังไม่วาง stub** โดยเจตนา ตาม `1746` ข้อ 3 (ปล่อยเปิดจนงานจบ · PR ยังไม่ merge)

---

## สิ่งที่สร้างรอบนี้

### 1. `1746` ข้อ 4 — ครึ่ง relog ของ `/warp 126`
ไฟล์ใหม่ `src/pirateforce_foundation/gm/warp_relog_stage.py`
เสียบที่สาขา **`else`** ของ persist ใน `gm/chat_command_action.py` (ทุก outcome ที่ไม่ใช่ `persisted`)

- แถว `character_positions` ของ 126 ยัง**ถูกปฏิเสธโดยชอบ** (`login_would_refuse`) ประตูล็อกอินไม่ถูกเปิด
- ครึ่ง relog เดินทางเส้นอื่น = single-use login entry ของ `CORE-REQUEST-GM-038`
- สองบรรทัดคอนโซลตามใบ เรียงตามที่ผู้เทสอ่าน:
  `GM_WARP_SCENE_PERSIST_FAILED scene=126 reason=login_would_refuse`
  `GM_WARP_RELOG_ENTRY_STAGED scene=126 previous=none single_use=1`
- **126 เป็นฉากเดียวบนเส้นทางนี้ และในโค้ดใหม่ไม่มีเลข `126` เลย** ประตูคือแผนที่
  `SANCTIONED_BARRED_SCENES` (วันนี้มี id เดียว) ปักด้วยการเดิน ast + เทสพฤติกรรม
  (เปลี่ยนแผนที่แล้วเส้นทางตามไปจริง)
- fail-closed: การเขียนคือ `stage_login_scene` ซึ่งเช็ก `gm_accounts` ซ้ำจากไฟล์ allowlist ของผู้เรียกเอง
  · ไม่มี `production_allowed` ที่ไหนในเส้นทาง (กฎข้อ 1 ของสาย)

**ข้อบกพร่องที่รอบนี้เปิดเองและปิดเองในคอมมิตเดียวกัน** (เจอตอนอ่านซ้ำ ไม่ใช่ adversary เจอ):
`_make_action` หน่วงคำสั่งที่เขียนแถว audit ไม่ได้ แล้วรัน `verdict.undo` · เส้นทาง 126 ไม่มี undo
เพราะ persist ไม่ได้เขียนอะไร ⇒ **entry ค้างบนดิสก์ทั้งที่ศูนย์ไบต์ออกสาย** ล็อกอินถัดไปพาตัวละคร
เข้า 126 จากคำสั่งที่ไม่เคยถึงสาย = รูปเดียวกับ finding 1 ของ `741zlx` มาทางประตูที่รอบนี้เพิ่งเปิด
แก้: คืน `RelogStageResult(outcome, undo)` และ verdict ถือ undo นั้น · ปักด้วยเทสสองตัว

เทส `tests/test_gm_warp_relog_stage.py` **17 ตัว** รวมตัวที่ล้มเมื่อย้อนตัวแก้ (ไม่ใช่เทสเปล่า)

### 2. adversary ครั้งที่ 2 บน `#837` (โควตา 2/2 ตาม `1747` ข้อ 2) = **NOT APPROVED**
`#837` merge ไปแล้ว ⇒ รันบน main ตามใบ · เจอ ⇒ PR แก้ใต้รหัสเดิม (คือ PR ของรอบนี้)
🔴 **ห้ามครั้งที่ 3** (`PANYA 1428`) — รอบนี้ไม่เรียกอีก

| | ระดับ | สถานะ |
|---|---|---|
| D1 โทเคน `GM_WARP_POSITION_CONFIRMED` พิมพ์เขียวให้วาปที่เฟรมไม่เคยออกสาย | CRITICAL · regression ของ `#837` เอง · **อยู่บน main** | ✅ แก้รอบนี้ |
| D2 สาขา fallback เขียนแถว **ไปข้างหน้า** แล้วเรียกว่า `rolled_back` | HIGH | ✅ แก้รอบนี้ (แก้ด้วยลำดับ) |
| D3 ช่อง park→relabel ไม่ถูก serialize · heartbeat ลงกลางช่องได้ | ship-blocking | 🔴 ต้องแก้ใน `runtime.py` = ส่ง COO `1933` |
| D4 resync เขียน 13 อย่าง `#837` คืนให้ 1 | major | 🔴 คำถามออกแบบ ส่ง COO `1933` |
| D5 แถวกับป้าย carry forward คนละเงื่อนไข | major | บันทึกเป็นหนี้ (งานสำรอง ข้อ 3) |
| D6 carry-forward ของป้ายไม่มีเทสเลย (มิวแทนต์รอด 286 ตัวเขียว) | major | ✅ ปักรอบนี้ |
| D7 เทสที่ตั้งชื่อตาม D1 แต่ผ่านมิวแทนต์ของ D1 เอง | minor | ✅ เขียนตัวที่ปักคำอ้างนั้นจริง (ไม่ลบตัวเก่า) |
| D8 ประโยคใน `warp_scene_persist.py:886` ที่ D2 วัดว่าเท็จ | minor | บันทึกเป็นหนี้ (งานสำรอง ข้อ 3) |

D1 ที่วัดพร้อม control:

| | ป้ายหลัง rollback | CONFIRMED | trail |
|---|---|---|---|
| restore ปิด (ก่อน `#837`) | 2 | ไม่พิมพ์ (mismatch 43,413) | `..._target_mismatch_43413` |
| restore เปิด (`#837` บน main) | 1 | 🔴 **พิมพ์** | `gm_warp_position_confirmed` + `client_confirmed_scene_1_warp_confirmed` |

ตัวแก้: `_disarm_warp_confirm_window` ปิดหน้าต่างยืนยัน**ทุกครั้งที่ send ล้ม** ไม่ผูกกับผลของ rollback
· **ไม่แตะ** `scene_label_is_server_guess` (หลังวาปที่ถูกยกเลิก ธงนั้นตั้งไว้อย่างซื่อสัตย์)
เทส `tests/test_gm_warp_undo_confirm_window.py`

🔴 **มิวแทนต์สามตัววัดจริงในรอบนี้ ฆ่าเทสใหม่ได้ทั้งสามตัว**
M1 (ลบตัวแก้ D1) → `test_a_walk_after_a_failed_warp_does_not_print_confirmed` แดง
M2 (ลบลำดับของ D2) → `test_a_park_without_a_row_still_lands_in_the_departure_scene` แดง
M3 (ลบ carry-forward) → `test_the_departure_label_survives_a_replacement_park` แดง
`BYTECODE_PURGED:` ทุกคำสั่งในรอบนี้รันด้วย `PYTHONDONTWRITEBYTECODE=1` (กติกา `14:53` ข้อ 1)
คืนไฟล์ต้นฉบับด้วยสำเนาใน scratchpad ไม่ใช้ `rm -rf` (`PANYA 1546`)

### 3. `1747` ข้อ 3 — "park ไม่ผูก character id" = **เข้าถึงไม่ได้** ปิดด้วยบรรทัดเดียว
park เป็น attribute บน session ตายไปกับ session · จะเข้าถึงได้ต้องเลือกตัวละครที่สองบน connection เดิม
`runtime.py:8686` `if selector is None or self.start_game_reply_sent: return []`
⇒ StartGame สำเร็จได้ครั้งเดียวต่อ connection · **ไม่มีโค้ดต้องแก้ ไม่เป็นหนี้ต่อ**

### 4. `1745` ข้อ 3 — ตอบก่อนกำหนด 21:11 · คำตอบ = **"มีผู้อ่าน"**
`lane_hooks/__init__.py:1096` อ่าน `scene_label_is_server_guess` ใน `current_session_scene_id`
ซึ่งเป็นจุดอ่าน x9 ของ `gm/attr_wire.py:1197` ⇒ ธงค้าง `True` ทำให้ x9 อ่านไม่ได้ ⇒ **ไบต์ที่ออกต่างไป**
⇒ ออก `CORE-REQUEST-GM-060` (`notes_to_chief/20260905_1922_*`) พร้อมเลขบรรทัดครบ
ของแถม: `gm/attr_wire.py:1856` เขียนว่าจุดอ่านนี้ "STILL NOT LANDED" = **เท็จแล้ว** ขีดฆ่าไว้ ไม่ลบ
⇒ เงื่อนไขของ fence ที่ `COO 20260904_1149` ข้อ 3 แขวนไว้ครบแล้ว · **สายนี้ไม่ยกเอง** รายงานอย่างเดียว

---

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
พิมพ์ `/warp 126` แล่นเรือใน Rising Sun Sea **ปิดไคลเอนต์ เข้าใหม่ ยังอยู่ที่ 126** —
เมื่อวานเข้าใหม่แล้วเด้งกลับฉากเดิม
และเลิกถูกหลอกด้วย `GM_WARP_POSITION_CONFIRMED` สีเขียวที่พิมพ์ให้วาปซึ่งเฟรมไม่เคยออกสาย

## nonclaim (บังคับ)
🔴 ใช้ GM ข้ามขั้นอะไร: ใช้ทางของ GM เพื่อไปถึงฉาก 126 เลย — ผู้เล่นธรรมดาไม่มีเส้นทางไปที่นั่น
ซึ่งเป็นเหตุผลที่ประตูล็อกอินของมันปิดอยู่ · staged entry คือ**คำสั่ง** ไม่ใช่หลักฐานว่าล็อกอินทำตาม
เกณฑ์ข้อสองของ `GT-266` วัดได้โดยคนที่หน้าจอเท่านั้น
· ทุกอย่างในรอบนี้ headless ฝั่งเซิร์ฟเวอร์ ไม่มีหลักฐานบนจอ
· ไม่มีบัญชีไหนได้สถานะ GM · **ห้ามอ่านไมล์สโตนออกจากรอบนี้** โดยเฉพาะ M2/M3

## หลักฐาน
- ชุดเต็ม (`pytest tests/`) รันครั้งเดียวบนสภาพสุดท้าย หลังแก้ตามผล adversary เรียบร้อยแล้ว:
  **11,201 ผ่าน · 327 skipped · 20,949 subtests ผ่าน · แดง 1** = `test_every_lane_gm_test_file_is_tracked_by_git`
  สาเหตุ: ไฟล์เทสใหม่สองไฟล์ยังไม่ถูก `git add` ตอนรัน ไม่ใช่ข้อบกพร่องของโค้ด
  commit แล้วรันไฟล์นั้นซ้ำ **เขียว 5/5** · 🔴 **ไม่มีการแก้โค้ดหลังชุดเต็ม** สิ่งที่เปลี่ยนคือ git tracking เท่านั้น
  (เหตุผลที่รันเกินหนึ่งครั้ง ตามกติกา: ครั้งที่สองเป็นไฟล์เดียว ไม่ใช่ชุดเต็ม และเป็นการยืนยันเกตที่ commit เองเป็นตัวปิด)
- เขียว(cloud sanity) เท่านั้นในรอบนี้ · เขียว(Actions run #N) รอเกต Windows บน PR
- `KNOWN_RED_MAIN:` ไม่มี (test_combat_pose ปิดไปแล้วตาม NOW `17:55` ข้อ 1)

## งานสำรอง (3 ข้อ · เริ่มได้ทันทีไม่รอใคร)
1. **`1745` ข้อ 2 — rollback เทียบปลายทาง (busy-database)** ยังเป็นหนี้ของสาย
   PR ที่แก้มันคือ PR ที่ลบเทส `KNOWN_DEFECT` ในคอมมิตเดียวกัน (ตาม `1150` ข้อ 1 + `1745` ข้อ 1)
2. **D5 + D8 ของ adversary รอบนี้** — แถวกับป้าย carry forward คนละเงื่อนไข และประโยคใน
   `warp_scene_persist.py:886` ที่ D2 วัดว่าเท็จ · ทั้งคู่อยู่ในเขต `gm/` ทำได้เลย
3. **P-3 สารบัญปุ่ม GMUI ทั้ง 3 หน้า** (`COO 0245`) เท่าที่ไม่ต้องเปิด client image:
   ไล่จาก `pf_bridge/gamedata/` + `external/` แล้วเปิดใบ RE แคบสำหรับปุ่มที่ต้องการ image

## backlog (อะไรบล็อกอยู่ที่ใคร)
- 🔴 **D3 (ship-blocking) บล็อกที่ chief** — serialize ช่อง park→relabel ต้องแก้ใน `runtime.py`
  ใบ: `notes_to_chief/20260905_1933_LANE-GM-ASK-COO-*` · GM-059 ยังเปิดอยู่จริงบน interleaving นี้
- 🔴 **D4 + คำถาม "ใครเป็นเจ้าของ inverse ของวาป"** บล็อกที่ COO — 12 จาก 13 ฟิลด์อยู่ใน `runtime.py`
- 🔴 **`CORE-REQUEST-GM-060`** บล็อกที่ chief — คืน `scene_label_is_server_guess` ตอน rollback
- **`GT-266` เกณฑ์ข้อสอง** บล็อกที่เครื่องของเจ้าของ (attended) ไม่ใช่ตัวบล็อกของสายนี้ — สายเดินต่อ
- `1347` ยังไม่ปิด รอ PR ของรอบนี้ merge

## ค้นแล้ว
`external/00_SEARCH_HERE_FIRST.md` = ไม่เจอ · `gamedata/00_SEARCH_HERE_FIRST.md` = ไม่เจอ
(ค้น `126` ใน `gamedata/TEXTDATA_TH__SCENE_NAME_TIP.tsv` ด้วย = ไม่เจอ · ชื่อฉากของ 126 มาจาก
registry ของสาย A ไม่ใช่ตารางไคลเอนต์ · งานรอบนี้ไม่พึ่งข้อมูลไคลเอนต์เลย)

## จดหมายที่ออกรอบนี้
- `20260905_1922_LANE-GM-CORE-REQUEST-GM-060-*` → chief
- `20260905_1928_LANE-GM-REPORT-COO-1746-item-4-*` → COO
- `20260905_1933_LANE-GM-ASK-COO-adversary-pass2-*` → COO

## บันทึกท้ายรอบ
push แล้ว รอ merge PR `pirate-force-server#844` (สถานะจริง: **เปิดแล้ว ไม่ draft · marker `PF-AUTOMERGE: v4`
ยืนยันด้วย GET แล้วว่าอยู่ในตัว body จริง · รอเกต Windows**)
claim PR `pf_bridge#1364` เติม marker ตอนจบรอบ = ปลดล็อก
🔴 ไม่ได้เขียนว่า "เสร็จ" และไม่ได้อยู่บน main — รอบถัดไปตรวจ `merged=true` ตาม addendum A
