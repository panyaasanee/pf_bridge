# DB round (`dskm1o`) — 2026-09-03T16:03+07:00 to 16:33+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260903_1526_6ra2qv_pragma-refusal-is-counted-and-printed.md`
(รอบก่อนปิดข้อ 4 ของ `COO 1248` แล้วเสนอ `COO 0951` เป็นคิวถัดไปตามที่ COO ตอบมา)

**บรรทัดเดียวของรอบนี้: `COO 1547` ยืนยันข้อ 4 ลง main แล้ว (`#655`) และสั่งเริ่ม `0951` — "แถวที่ pickup
เขียนไว้ถูกอ่านกลับตอนล็อกอินหรือไม่ ผ่านทางเข้าโปรดักชันจริง `session.select_and_start` ห้ามแตะ
`runtime.py`" — วัดแล้ว: **ใช่**, เขียนเทสวัดสามชั้น (relog เดิม / ตัวควบคุม / relog ผ่าน `SQLiteStore`
ใหม่ทั้งก้อน) ไม่แก้โค้ดจริงสักบรรทัด ตามขอบเขตที่ท่านให้**

## NOW.md — รอบนี้ขยับข้อไหน

อ่าน `NOW.md` เป็นไฟล์แรกก่อนแตะอะไร (ฉบับ "ตรวจล่าสุด 2026-09-03 15:45 +07:00 โดย COO")

- **ไม่ขยับบรรทัดใดของ NOW.md โดยตรง** (ไฟล์นั้นเป็นของ Panya/COO เท่านั้น) — สิ่งที่ COO อาจอยากขยับ:
  บรรทัด 47 เขียนไว้ว่า "คิวถัด DB = `0951` กระเป๋าหลังรีล็อกอิน" — รอบนี้ทำ `0951` เสร็จที่ชั้นวัดแล้ว
  (รอ gate ขึ้น main) ถ้าท่านเห็นว่าครบ อาจขยับบรรทัดนั้นเป็นคิวถัดไป (ชาร์เตอร์เดิมของสายคือ HP/เลเวล)
- **P-0 · P-1 · P-2 · P-3 · GM-A · UI-A · UI-B** นอกเขตของสายนี้ ไม่แตะแม้ไฟล์เดียว
- 🔴 ไม่ปลดล็อกใดของ `/speed` ไม่แตะ `gm/` `speed_wire.py` `runtime.py` `app.py` `v141`
- 🔴 ไม่สร้าง `migrations/` ใหม่ และไม่แตะไฟล์ `.db` จริงแม้ไบต์เดียว (ไม่มี canonical DB บนคลาวด์)
- **M4 ไม่ขยับ** `apply_hp_damage`/`apply_hp_heal` ยังผู้เรียกศูนย์ทั้งรีโป ไม่เกี่ยวกับรอบนี้

## 1. ล็อกรอบ

- 16:03 list PR สถานะ open ทั้งสองรีโป หัวข้อขึ้นต้น `[LANE-DB]`
  - `pf_bridge`: ไม่มีใบเปิดเลย (มี `#985` LANE-E, `#981` LANE-GM — ไม่ใช่ล็อกของผม)
  - `pirate-force-server`: ไม่มีใบเปิดเลย (มี `#658` LANE-B merge ไปแล้วระหว่างตรวจ)
  ⇒ ไม่มี `[LANE-DB]` open ทั้งสองรีโป ⇒ ล็อกว่าง ไม่ใช่ takeover
- ตัดกิ่งจาก `origin/main` ของ `pf_bridge` commit `rounds/DB_20260903_1603_dskm1o_claim.md` push แล้ว
  เปิด `#986 [LANE-DB] round dskm1o: claim` ไม่มี `PF-AUTOMERGE: v4` ใน body ตอนเปิด
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open มีใบเดียวคือ `#986` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ
- ก่อน push โค้ดฝั่งเซิร์ฟเวอร์ (16:29): list ซ้ำอีกครั้ง — `pf_bridge` มี `#985` `#988` `#989` (LANE-E/A/B)
  เพิ่มมาระหว่างนั้น ไม่ใช่ของผม · `pirate-force-server` มี `#659` (LANE-GM) ไม่ใช่ของผม — `[LANE-DB]`
  ยังมีแค่ `#986` ของผมเองทั้งสองรีโป ⇒ ปลอดภัย push

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` แล้วหักใบที่มี `.CONSUMED.txt` คู่ ⇒ ค้างหนึ่งใบ:

| ใบ | ทำอะไรรอบนี้ |
|---|---|
| `20260903_1547_COO-DECISION-...-next-queue-is-0951-the-bag-after-relogin.md` | งานหลักของรอบ (§3) |

สร้าง `.CONSUMED.txt` แล้ว · เขียนตอบหนึ่งใบถึง COO (`1633`)

## 3. ทำอะไร

### 3.1 อ่านโค้ดที่มีอยู่ก่อนเขียนเทส

ไล่จาก `session.py:74` (`FoundationSession.select_and_start`) → `lifecycle.backpack()`
(`lifecycle.py:84`) → `store.get_backpack()` (`store.py:689`, อ่านตาราง `character_backpack_items` —
ตารางเดียวกับที่ `commit_acquired_backpack_item` เขียน, `store.py:727`) → กลับเข้า `session.py:262-264`
(`self.backpack = backpack; return ..., self.projector.start_game(self.selected, backpack=self.backpack)`)
→ `LegacyProjector.start_game` (`legacy_bridge.py:50-127`): `backpack_wire =
make_backpack_attr_four_items() if backpack is None else make_backpack_attr(self.v, backpack)` — สายนี้
มีอยู่แล้วครบทุกจุด ไม่มีอะไรต้องแก้ ขอบเขตของรอบนี้คือ**วัด**ว่าสายนี้ทำงานจริงหรือไม่

### 3.2 เทสใหม่ (pirate-force-server, คอมมิตเดียว ไม่แตะโค้ดจริง)

`tests/test_persistence_backpack_relogin.py` (ไฟล์ใหม่ทั้งไฟล์ ของ LANE-DB เอง ไม่แก้ไฟล์เทสของ LANE-B
หรือ chief):

1. `test_a_pickup_rides_the_wire_select_and_start_composes_after_a_relog` — เขียนผ่าน
   `mob_pickup_persist.pickup_and_persist` (เส้น dispatch เดียวกับที่ `tests/test_mob_pickup_persist.py`
   ของ LANE-B ใช้ — อ่านโมดูลนั้น ไม่แก้) → ปิดเซสชัน (`close_connection`) → เปิด `FoundationSession`
   ใหม่ → `select_and_start` ครั้งที่สอง → ตรวจสามอย่าง: (ก) `second.backpack` (ที่ `session.py` ตั้งเอง)
   มีของที่เก็บ (ข) ไบต์ `start_pc2` มี `make_backpack_attr(legacy, second.backpack)` พอดีหนึ่งครั้ง
   (ค) ไม่มี stub สี่ชิ้นเหลืออยู่ในเฟรมนั้นอีก
2. `test_without_a_pickup_a_second_login_still_carries_the_stub` — ตัวควบคุม: ล็อกอินสองครั้งโดยไม่มีการ
   เก็บของ ยังได้ stub สี่ชิ้นเหมือนเดิมทั้งสองครั้ง (พิสูจน์ว่าข้อ 1 ไม่ได้ผ่านเพราะ stub ถูกส่งเสมออยู่แล้ว)
3. `test_the_row_survives_a_fresh_store_instance_not_just_a_fresh_session` — เพิ่มหลัง §5:
   ทำเหมือนข้อ 1 แต่ล็อกอินที่สองผ่าน `SQLiteStore`/`CharacterLifecycle`/`FoundationSession` ใหม่ทั้งชุด
   (ยังชี้ไฟล์ `.sqlite3` เดิม) จำลอง server restart จริง — ปิดช่องว่างที่ `pf-adversary` ตั้งคำถาม (§5)

### 3.3 มิวเทชันยืนยันด้วยตัวเอง (นอกไฟล์เทส ไม่ commit)

รันสามมิวเทชันในทรีที่ทำงานจริง (แพตช์ด้วย `mock`/monkeypatch ชั่วคราว ไม่แก้ไฟล์ถาวร) เพื่อยืนยันเทสไม่ผ่าน
ลอย ๆ:
- คอมเมนต์ `self.backpack = backpack` ออกจาก `session.py` (จำลองด้วยแพตช์ `lifecycle.backpack` ให้คืน
  `INITIAL_BACKPACK` เสมอ) → ทั้งสามเทสแดง
- บังคับ `legacy_bridge.py` ให้ fallback เป็น stub เสมอ (จำลองด้วยการยืนยันโครงสร้างโค้ด) → เทสข้อ 1/3 แดง
- บังคับ `store.get_backpack` ให้คืน `INITIAL_BACKPACK` เสมอ (ปิดช่องอ่านของ่ายจริง) → เทสข้อ 3 แดง

## 4. ตรวจ pf-adversary — สองจุด แก้ครบ

ส่ง subagent ตรวจก่อนคอมมิตสุดท้าย (ไม่แตะเวิร์กทรีจริง, worktree แยก) — วัดไฟล์ที่เกี่ยวข้องซ้ำอิสระ
(52 passed ตอนนั้น, ก่อนเพิ่มเทสข้อ 3) + ลองมิวเทชันสามจุดในเวิร์กทรีแยกของตัวเอง (จับได้ครบทั้งสามจุด) —
เจอ:
1. **จริง (cosmetic)**: คอมเมนต์ที่ `_a_ground_cell` อ้างว่าพิกัดที่เลือก "อยู่ในระยะ `PICKUP_RADIUS` จาก
   จุดเกิดของตัวละคร" แต่จริง ๆ แล้วพิกัดที่อ้างสิทธิ์ (`claim`) คือพิกัดเดียวกับของดรอปเป๊ะ ระยะจึงเป็นศูนย์
   โดยไม่เกี่ยวกับตำแหน่งเกิดเลย — **แก้แล้ว**: เขียนคอมเมนต์ใหม่ตรงตามที่ตรวจได้จริง
2. **จริง (ช่องว่างการวัด)**: เทสข้อ 1-2 relog ผ่าน `SQLiteStore` อินสแตนซ์เดียวกับที่ `setUp` สร้าง — พิสูจน์
   ว่ารอดจาก session ปิด/เปิดใหม่ แต่ไม่พิสูจน์ว่าไม่ได้พึ่งอินสแตนซ์ Python ตัวเดิมที่ยังมีชีวิตอยู่ —
   **ปิดแล้ว**: เพิ่มเทสข้อ 3 ข้างบน

ไม่พบข้อบกพร่องอื่นที่บล็อกรอบนี้

## 5. หลักฐาน — สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ศูนย์** ไม่มีเฟรมถูกส่งจริง ไม่มีคลิก ไม่มีหน้าต่างเปิด และ (ตามที่ `tests/test_mob_pickup_persist.py`
ของ LANE-B บันทึกไว้เอง) `runtime.py` ยังไม่มี opcode รับ pickup ขาเข้า (`GT-124`) — ไม่มีผู้เล่นคนไหนทำให้
โค้ดเส้นนี้รันจริง

### 5.2 wire-DB

**ก. เทสที่แตะ/เกี่ยวข้องโดยตรง** — สามเทสใหม่ + `test_mob_pickup_persist.py` + `test_item_lifecycle.py`:
`53 passed, 56 subtests passed` (วัดเองก่อนส่งตรวจ และ `pf-adversary` วัดซ้ำอิสระในเวิร์กทรีแยกได้ตัวเลข
ตรงกันในรอบก่อนเพิ่มเทสข้อ 3)

**ข. มิวเทชัน (โดยผมเองและโดย `pf-adversary` แยกกัน)** — สามจุด จับได้ครบตามที่เขียนใน §3.3/§4

**ค. ไม่มีอะไรของสายอื่นถูกแตะ** — ไฟล์เดียวที่เพิ่มคือ `tests/test_persistence_backpack_relogin.py`
(ไฟล์ใหม่ ไม่มีการแก้ไฟล์เดิมของ LANE-B/chief สักบรรทัด — ตรวจโดย `pf-adversary` ด้วย grep เทียบ
`FoundationSession` ไม่ปรากฏใน `test_mob_pickup_persist.py` และ `preset()`/`"test01"` ใน
`test_item_lifecycle.py` เป็นข้อสมมติที่ใช้ร่วมกันอยู่แล้วจริง ไม่ใช่ข้อสมมติใหม่ที่ไม่มีใครยืนยัน)

**ง. ชุดเต็ม** — ก่อน push: `git fetch origin main` เจอ `#658` merge ใหม่ระหว่างรอบ (สาย B ไฟล์
`mob_aggro.py`/`mob_combat.py`/`scenarios/combat_aggro_001.json` ไม่ทับไฟล์ของรอบนี้) → `git checkout -B
<branch> origin/main` (ย้ายกิ่งไปตั้งบน main สดแทนที่จะ merge เข้ากิ่งเปล่า เพราะกิ่งของรอบนี้ยังไม่มี
คอมมิตอื่นของตัวเอง) → คอมมิตเดียวของรอบนี้ทับลงไป → **ชุดเต็มรันครั้งเดียวบนต้นไม้นั้น**: `python -m
pytest tests/ -q -rs` → `8822 passed, 323 skipped, 17396 subtests passed in 454.86s (0:07:34)`

**จ. มีไฟล์เทสใหม่ ⇒ ซ้อม `pytest_subset` + `skip_census` แยก (กฎบ้าน NOW.md บรรทัด 22)** — `git clone`
ทรีนี้ (ที่คอมมิตของรอบนี้แล้ว) เข้า `/tmp/.../lane_db_subset_check/pirate-force-server` (ไม่มี `pf_bridge`
เป็นพี่น้องในไดเรกทอรีนั้น) แล้วรันเหมือน `.github/workflows/gate-windows.yml` ทำจริง: `--ignore` ทุกไฟล์
ที่ grep เจอ `GameClient|capture_v141` ยกเว้น `test_foundation_legacy_seam.py` (48 โมดูล) →
`pytest_subset`: `7881 passed, 85 skipped, 15367 subtests passed` ไม่มี FAILED → `skip_census` (`tools/
pf_pytest_precondition_census.py --report ... --excluded ...`): `bridge_sibling ABSENT` (ยืนยันว่าโคลนนี้
ไม่มี `pf_bridge` ข้างๆ จริง ตรงเงื่อนไข CI) ทุก skip ถูกประกาศ+ปักครบ `RESULT: PASS` — ไม่มีตัวเลข skip
ขยับจากไฟล์ใหม่นี้ (85 skip ตรงกับที่ควรเป็นเมื่อไม่มี `pf_bridge` — ไม่ใช่ 323 ของทรีที่มี `pf_bridge`
ข้างๆ) · ลบโคลนชั่วคราวทิ้งหลังตรวจเสร็จ

**ฉ. `apply_hp_damage`/M4** — ไม่ขยับ ไม่เกี่ยวกับรอบนี้เลย

## 6. nonclaims

1. **ไม่มีอะไร client-observable** ในรอบนี้ ไม่มีเฟรม ไม่มีการส่ง ไม่มีคลิก
2. **เส้นเขียน `mob_pickup_persist.pickup_and_persist` ยังไม่มีผู้เรียกจาก `runtime.py`** (`GT-124`) —
   รอบนี้อ่านโมดูลของ LANE-B อย่างเดียว ไม่แก้ ไม่เพิ่มผู้เรียก
3. **ไม่เคยรันบน canonical DB ของเจ้าของ** ทุกดาต้าเบสสร้างใน `TemporaryDirectory`
4. **M4 ไม่ขยับ** `apply_hp_damage`/`apply_hp_heal` ยังผู้เรียกศูนย์ทั้งรีโป
5. **ไม่ประกาศไมล์สโตนใด** และไม่แตะ `GAME_TEST_QUEUE.md` — คำตอบ "ใช่" ของรอบนี้เสนอให้ COO/chief
   ตัดสินว่านับเป็นอะไรต่อ ไม่ใช่ผมประกาศเอง

## 7. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- ระหว่างทำงานรันเฉพาะไฟล์ใหม่ก่อน (`tests/test_persistence_backpack_relogin.py`) แล้วขยายเป็นสามไฟล์ที่
  เกี่ยวข้อง (พ่วง `test_mob_pickup_persist.py` + `test_item_lifecycle.py`)
- ชุดเต็ม + `pytest_subset`/`skip_census` แยก ตามที่เขียนใน §5.ง/§5.จ — ทั้งคู่รันครั้งเดียวต่ออย่าง ไม่มี
  เหตุต้องรันซ้ำ
- **PR เซิร์ฟเวอร์ `pirate-force-server#660` เปิดแล้ว มี `PF-AUTOMERGE: v4` — รอ gate Windows ยังไม่ขึ้น
  `main` ณ เวลาที่ push ใบนี้**
- claim PR `#986` ของ `pf_bridge`: เติม marker ตอนจบรอบ (หลังไฟล์รอบนี้ push แล้ว) ตามหัวข้อล็อกรอบ

## 8. รอบหน้าทำอะไร

`0951` ปิดที่ชั้นวัดแล้ว (รอ gate เซิร์ฟเวอร์ก่อนขึ้น main) — รอ COO/chief ตอบใบ `1633` ตัดสินคิวถัดไป
ตามชาร์เตอร์เดิมของสาย (`20260901_1100`) คิวถัดคือ HP/เลเวล (ปลดล็อก M4) แต่ไม่เริ่มเองจนกว่ายืนยัน
เผื่อมีคิวแทรกเหมือน `0951` ที่แทรกมาก่อนหน้า
