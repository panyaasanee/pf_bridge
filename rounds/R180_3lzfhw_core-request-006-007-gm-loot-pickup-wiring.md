# R180 (3lzfhw) — 2026-08-26 ~19:0x-20:0x (+07:00)

## สรุปหนึ่งย่อหน้า

ตาม v6.1 หัวข้อ 17 ข้อ 3 (ต่อสาย CORE-REQUEST ก่อนงานอื่นทุกอย่างในรอบ): ต่อสาย `CORE-REQUEST-006`
(GM state after login) เต็มใบ และ `CORE-REQUEST-007` ที่เหลือ (`mob_loot`/`mob_pickup`) เท่าที่
`MOB_LOOT_WIRING`/`MOB_PICKUP_WIRING` อนุญาตให้ทำตอนนี้ (ไม่แตะ step 3 ของ pickup ที่ยังไม่ปลอดภัย) —
ใช้ `pf-builder` เขียน `runtime.py` ตามคำสั่งเดินสายที่แต่ละโมดูลเขียนไว้เองแล้ว จากนั้น `pf-adversary`
บังคับก่อน commit พบข้อบกพร่องจริงหนึ่งข้อระดับ **HIGH** (ไม่ใช่แค่เอกสาร) — แก้แล้วก่อน push ทั้งหมด
`WIRED` (นิยาม ก, COO-DECISION `20260826_1743`) ขยับ **7/10 → 9/10** (เหลือ `world_scene_density`
เป็นเลนเดียวที่ยังไม่ต่อสาย)

## ① สิ่งที่ทำ — `pirate-force-server`

`pirate-force-server@<push ตอนจบ>` (branch `claude/optimistic-mccarthy-3lzfhw`, PR รอ merge):

- `runtime.py` (+198 บรรทัด จาก `pf-builder`, +แก้ 2 จุดจาก `pf-adversary` finding):
  - **CORE-REQUEST-006**: หลัง `world_scene_entry.resolve_entry()` สำเร็จ (จุดเดียวกับที่
    `CORE-REQUEST-003` ต่อ) เรียก `is_gm_account(self.token)` (`self.token` คือ login name ที่มีอยู่แล้ว
    ไม่ใช่ฟิลด์ใหม่) แล้วถ้าเป็น GM ประกอบ `make_gm_update_state_frame(legacy, 1, 0, 0, 0)` ต่อท้าย
    action list — ค่าฟิลด์ทั้งสี่ `[ASSUMED - awaiting RE]` ตามที่จดหมาย GM ขอไว้ (ยังไม่รู้ความหมายจริง
    รอ `CORE-REQUEST-GM-001`)
  - **CORE-REQUEST-007 ที่เหลือ**: `mob_loot` — หนึ่ง `DropLedgerCell` + หนึ่ง `random.Random()` ของ
    เซิร์ฟเวอร์เองต่อเซสชัน หลัง `mob_death.commit_death()` สำเร็จ roll หนึ่งครั้ง retry `loot_a_kill` บน
    `ledger_generation_moved`/`ledger_stale` (roll เดิม ไม่ roll ซ้ำ ตามกฎของ `commit_drops` เอง) ไม่
    retry บน `mob_already_looted` ส่งทุกเฟรมของ `drop_frames()` ต่อท้ายเฟรมตาย แล้ว prune ทันทีผ่าน
    `cell.take()` (ยังไม่มีทาง pickup อ่านคืน — ห้ามใช้ timer/`refresh_frames()` ตามคำตัดสิน COO ที่อ้าง
    ในโมดูลเอง) · `mob_pickup` — หนึ่ง `BagCellRegistry()` ต่อเซิร์ฟเวอร์ (สร้างครั้งเดียวใน
    `make_state_class` แบบเดียวกับ `scene_entry_registry`) `claim()` ที่ character-select (ใช้
    `BackpackState` ที่ `select_and_start` โหลดไว้แล้ว ไม่อ่าน DB ซ้ำ) `release()` ใน
    `close_connection()` เสมอ — **ไม่ต่อสายฝั่ง "รับคำขอ pickup"** (step 1-4 ของ `MOB_PICKUP_WIRING`)
    เพราะยังไม่มี vital id ที่รู้จริงสำหรับ pickup request บนไวร์ (ยืนยันด้วย adversary: 0 hit ของ
    `PickupClaim`/`commit_pickup` ใน `runtime.py`)
- `tests/test_mob_combat_dispatch.py`: สองเทสเดิม (`test_a_killing_blow_sends_announce_then_death_frames_in_order`,
  `test_world_census_override_reflects_a_committed_kill`) แก้จาก exact-match บนทั้งลิสต์ เป็นตรวจสาม
  ตัวแรกแบบ exact + ยอมรับ `MOB_LOOT_DROP` ต่อท้ายได้ (ไฟล์นี้พิสูจน์ลำดับ combat/death ไม่ใช่ loot —
  `test_mob_loot.py` คุมสัญญา roll/encode อยู่แล้ว) — สาเหตุคือ `roll_drops` ตอนนี้รันบน
  `random.Random()` จริงไม่ seed ต่อเซสชัน ทำให้จำนวนเฟรม loot ไม่คงที่ (ยืนยันด้วยรัน 5 ครั้งก่อน/หลัง
  แก้ ไม่มีเทสแดงอีก)
- `tests/test_gm_dispatch.py` (ใหม่ 4 เทส): headless ผ่าน `make_state_class` จริง พิสูจน์ (ก) บูตไม่มี
  config → ไม่มีเฟรม GM (ข) account ไม่อยู่ในลิสต์ → ไม่มีเฟรม (ค) account อยู่ในลิสต์ → ได้เฟรมตรงกับ
  `make_gm_update_state_frame` (ง) **finding ของ adversary**: config เสีย (`gm_accounts` เป็น string
  ไม่ใช่ list) → ไม่ crash ทั้ง listener แค่ refuse ด้วยชื่อ event แล้ว login คนนั้นไปต่อได้ปกติ

## ② `pf-adversary` finding และการแก้ (ก่อน push ทั้งหมด)

**HIGH — `is_gm_account()` ไม่มี guard ทำให้ dispatcher ทั้งตัวล้มได้จากการพิมพ์ผิดในไฟล์ config เดียว**:
`gm/accounts.py` ตั้งใจ raise `ValueError` เมื่อ `config/gm_accounts.json` มี `gm_accounts` ที่ไม่ใช่ list
(ป้องกัน typo แปลงเป็น "ไม่มีใครเป็น GM" แบบเงียบ) — แต่ `runtime.py` เรียกฟังก์ชันนี้แบบไม่มี
`try/except` ทุกครั้งที่มี `START_GAME_REQ` (ทุกผู้เล่น ไม่ใช่แค่ GM) จุดเดียวที่ exception ลอยไปถึงคือ
`current/pf_login_game_server_v141.py` listener loop ที่ดัก catch ไว้แค่ error ระดับ socket
(`ConnectionResetError`/`OSError` ฯลฯ) ไม่ใช่ `ValueError` — จะทำให้ **thread listener เกมทั้งตัวตาย
เงียบ ๆ** จากการพิมพ์ผิดใน config ไฟล์เดียว ไม่ใช่แค่ล็อกอินของคนที่พิมพ์ผิด (`pf-adversary` reproduce
จริงด้วยสคริปต์แยกก่อนรายงาน) — **แก้แล้ว**: ห่อการเรียกด้วย `try/except (ValueError, OSError)` แปลง
เป็น refuse-by-name (`gm_account_lookup_failed_<ExceptionType>`) แทนการปล่อยให้ crash · เพิ่มเทส
regression กัน (ดูข้อ ① ข้อ (ง) ด้านบน)

**LOW (ระบุแล้ว แก้ด้วย)**: guard `self.foundation.backpack is not None` ก่อน claim bag cell เป็นเงื่อนไข
ที่ไม่มีวันเป็นเท็จจริง (backpack ถูก set เสมอหลัง `select_and_start` สำเร็จ) — ลบเงื่อนไขที่ตายแล้วออก
ตามกฎ "ชื่อ refusal ที่เกิดไม่ได้คือคำโกหก" ที่ `mob_loot.py` ประกาศไว้เอง

**ยืนยันแล้วไม่ใช่บั๊ก** (adversary ตรวจแล้วปฏิเสธ): reconnect-ก่อน-`close_connection`
(reproduce จริง → ได้ refusal ชื่อ `mob_pickup_claim_refused_bag_already_claimed` ไม่ crash ไม่เงียบ) ·
โค้ดใหม่รันก่อน `self.foundation.selected` ถูกตั้งไม่ได้ (อยู่ใน `if not load_only:` หลัง
`select_and_start`/`resolve_entry` สำเร็จเท่านั้น) · retry loop livelock (ตรวจแล้ว unreachable วันนี้
เหมือน pattern เดิมของ `mob_combat`/`mob_ai_control`) · ค่า placeholder GM ติดป้าย `[ASSUMED]` ชัดเจน
พอไม่ให้อ่านผิดเป็นค่าที่พิสูจน์แล้ว

**MEDIUM ที่แก้ด้วยการเพิ่มเทส ไม่ใช่แก้โค้ด**: ไม่มีเทสระดับ dispatcher ที่พิสูจน์ path สำเร็จ/ล้มเหลว
ของ GM มาก่อนเลย (เทสเดิมทั้งหมดไม่มี `config/gm_accounts.json` เลยไม่เคยวิ่งผ่าน branch `is_gm_account
is True` หรือ branch ที่ config เสีย) — เพิ่ม `tests/test_gm_dispatch.py` ตามข้อ ① ด้านบน

**LOW ที่รับทราบแล้วไม่แก้รอบนี้ (เขียนไว้ในโค้ดแล้ว ไม่ซ่อน)**: `mob_loot_cell` เป็น per-session ไม่ใช่
per-scene ตามที่ `MOB_LOOT_WIRING` เขียนตัวหนังสือ (แต่ตรงกับ pattern เดิมของ `mob_combat_ledger`/
`mob_death_register`/`mob_ai_register` ที่ COO เคยยอมรับแล้วว่า per-session ปลอดภัยเพราะ
`game_listener` เสิร์ฟทีละ connection) — adversary เปิดคำถามไว้ว่าโมเดล concurrency ของโปรเจกต์นี้เป็น
"ทีละคนตลอดกาล" โดยเจตนา หรือเป็นแค่สภาพของ harness วันนี้ ยังไม่มีใครตอบ ไม่บล็อกอะไรตอนนี้

## ③ สวีตเต็ม

ก่อนแก้: `3044 passed, 198 skipped` (จาก `pf-builder`, มี 2 เทสแดงไม่คงที่จาก `roll_drops` unseeded)
หลังแก้ครบ (ติดตั้ง `capstone`/`pefile`/`pytest` สดในคอนเทนเนอร์นี้ก่อน เหมือนทุกรอบ cloud): **`3203
passed, 327 skipped, 4986 subtests passed, 0 failed`** เขียว(cloud sanity) — รันซ้ำ 3 รอบเฉพาะไฟล์ที่
แตะ loot/pickup/GM ยืนยันไม่มีเทสไม่คงที่อีก

## ④ `pf_bridge`

- บริโภคจดหมาย 11 ใบใน `notes_to_chief/` (6 ใบ `1730/1731/1732/1735/1746/1750` ถูก R179 บริโภคไปแล้ว
  ก่อนรอบนี้เริ่ม — พบตอนจะ commit ว่า stub ที่ผมวางผิดที่ (`notes_to_chief/*.CONSUMED.txt` แทนที่จะเป็น
  `notes_to_chief/consumed/*.CONSUMED.txt`) แก้ตำแหน่งให้ตรงธรรมเนียม R179 ก่อน commit จริง ไม่ทับของ
  เดิม; เหลือ 5 ใบใหม่จริงที่บริโภครอบนี้: `1741`/`1743`/`1755`/`1811`/`1839`)
- `.gitattributes` ของ `pirate-force-server` (`*.tsv text eol=lf`) และ `RE-092` (คำถาม world-wipe ของ
  `LANE-B-URGENT`) **ทำไปแล้วโดย R179 ก่อนรอบนี้เริ่ม** — ตรวจซ้ำแล้วไม่ต้องทำอะไรเพิ่ม
- เติมริเดอร์ `RIDER-084-A` ท้ายใบ `GT-084` (`GAME_TEST_QUEUE.md`, ผ่าน `pf-queue-author`) สั่งผู้เทสให้
  สังเกต/บันทึกนักแสดงอื่นบนจอก่อน-หลังทุกหมัด/เฟรมตาย ไม่ใช่แค่หลอด HP เป้าหมาย — ไม่แก้ P1-P5/objective/
  pass criteria เดิมแม้แต่ตัวอักษรเดียว อ้าง `RE-092` เป็นที่มา ไม่ตัดสิน PASS/FAIL ของ `GT-084` เอง
- เขียน `notes_to_chief/20260826_1900_CHIEF-ASK-COO-GT-084-world-wipe-risk-not-delaying.md` — ตัดสินใจ
  เองว่าไม่ชะลอ `GT-084` (เหตุผลในจดหมาย) COO แก้ได้ทันทีถ้าเห็นต่าง ไม่บล็อกอะไร

## ⑤ `WIRED`

**นิยาม (ก) ยืนยันด้วย COO-DECISION `20260826_1743`**: `6/10` → (R179) `7/10` (`combat_aggro`) →
(รอบนี้) **`9/10`** — เพิ่ม `combat_loot` (`mob_loot`) และ `combat_pickup` (`mob_pickup`, เฉพาะ
claim/release — ยังไม่มี inbound request path แต่โมดูลของเลนต่อเข้า `runtime.py` แล้วจริงตามนิยาม)
เลนเดียวที่เหลือ: `world_scene_density` — ไม่มี `CORE-REQUEST` ค้างจากสาย A สำหรับเลนนี้ ณ ตอนเขียน
รอบนี้ (ตรวจ `notes_to_chief/` แล้ว)

## ⑤.5 `LANE-B-REQUEST` (`full_roster_override`) — ลองแล้ว revert แล้ว ไม่ push

ระหว่างรอบ `main` ของ `pirate-force-server` ขยับ (`pirate-force-server#70` merge, `full_roster_override`
เข้ามาจริง) พร้อมจดหมายขอสลับหนึ่งบรรทัดที่ `runtime.py:4819` (`corpse_override` →
`full_roster_override`) — ลองสลับตามที่ขอ รันสวีตเต็มก่อน push แล้วเจอ **12 เทสแดง** ใน
`tests/test_world_census_wiring.py` (census บนบูตปริยายที่ยังไม่มีใครถูกตีเลยก็เปลี่ยนไบต์แล้ว เพราะ
`full_roster_override` ไม่เคยคืนค่าว่างต่างจาก `corpse_override` ที่คืนว่างเมื่อ ledger/register ยังสด)
— คำอ้าง "byte-identical กับพาธเดิม" ในจดหมายขอ ถูกแค่ระดับ per-identity ไม่ใช่ระดับ census โดยรวม
**revert กลับเป็น `corpse_override()` ก่อน push** (ไม่มีการสลับนี้ในสิ่งที่ push ไปจริง) เขียนตอบกลับ
พร้อมหลักฐาน: `notes_to_chief/20260826_2015_CHIEF-REPLY-LANE-B-full_roster_override-not-byte-identical-at-integration.md`

## ⑥ ค้าง

- `RE-092` ยังเปิดอยู่ (ต้อง RE runner บนสะพาน)
- `CORE-REQUEST-GM-001` (ความหมายฟิลด์ GM state) ยังเปิดอยู่ — ค่า placeholder `1,0,0,0` ยังไม่พิสูจน์
- `mob_loot`/`mob_pickup` inbound pickup request ยังไม่มีทางไป (รอ vital id จริงจาก RE)
- คำถาม concurrency model ที่ adversary เปิดไว้ (ข้อ ②) — ไม่บล็อก ไม่ต้องตอบด่วน
- `RE-082` amend (`RE-077` T5 + `GT-046` span pin) ค้างมา 4 รอบแล้ว (R177/178/179/180 ตั้งใจไม่รีบทำ) —
  ยังไม่สูงพอเทียบกับ CORE-REQUEST ที่เป็นลำดับแรกของ v6.1
- `CHIEF_CONTINUATION.md` 67,759 ไบต์ ยังไม่ถึงเพดาน archive
