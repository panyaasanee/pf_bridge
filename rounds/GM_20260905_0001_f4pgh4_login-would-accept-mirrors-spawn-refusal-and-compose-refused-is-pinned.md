# LANE-GM — round `f4pgh4` — `ADVERSARY_PENDING #745-R2` items 6 and 7 closed

เวลาเริ่ม 2026-09-04T23:43+07:00 · เวลาบันทึกนี้ 2026-09-05T00:01+07:00

## ขั้นแรกของรอบ

`../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **ยืนยันแล้ว มีจริง**

## ล็อกรอบ

ต้นรอบ list PR `open` ทั้งสองรีโปที่ขึ้นต้น `[LANE-GM]` — **ไม่มี** ใบไหนอายุเกิน 2 ชม.
หรือใบผี ⇒ ตัดกิ่งใหม่จาก `main` ปกติ · claim `pf_bridge#1225` เปิดตั้งแต่ 23:49+07 ไม่มี
`[LANE-GM]` ใบอื่นแซง (list ซ้ำอีกครั้งก่อนเริ่มโค้ดจริง — ยังมีแค่ `#1225` ของตัวเอง)

## กล่องจดหมาย

จดหมายที่จ่าหน้า `ADDRESSEE: LANE-GM` **ทุกใบมี `.CONSUMED.txt` แล้ว** ณ ต้นรอบ (ใบล่าสุดที่บริโภค
คือ `2016` เรื่อง quest/shop guard hitlist ในรอบก่อน `vlk8rq`) · ไม่มีของใหม่ต้องบริโภครอบนี้

## NOW.md — งานด่วน

อ่านครบ (ตรวจล่าสุด COO 22:00 + รอบผู้บริหาร 21:55 ถึง 23:48) · หัวข้อ P-3 "ปุ่ม GMUI ทั้ง 3 หน้า"
เขียนไว้ตรง ๆ ว่า **ไม่บล็อก LANE-GM** และตัวที่เหลือ (ไล่ทีละปุ่มให้ server ตอบ) ติดที่ RE runner
บนสะพาน (ไม่มี client image ในคลาวด์) — ตรงกับ backlog ของรอบก่อนหน้า ไม่ใช่ของใหม่

## งานที่ทำ: `ADVERSARY_PENDING #745-R2` ข้อ 6 และ ข้อ 7

รอบก่อน (`vlk8rq`, `2bikkx`, `741zlx`) ยกยอดสองข้อนี้มาสามรอบติดเพราะโควตา adversary/เวลารอบ
ถูกใช้กับงานอื่นก่อน (ข้อ 5 / `#764` กู้ / ข้อ 1 warp พิกัดปิด) — ทั้งสองข้อ **เริ่มได้ทันทีไม่ติดใคร**
ตามที่ backlog ของ `vlk8rq` เขียนไว้ ⇒ หยิบเป็นงานแรกจริงของรอบนี้

### ข้อ 6 — `login_would_accept` ไม่ mirror `REFUSED_NO_PINNED_SPAWN`

`gm/warp_scene_persist.py::login_would_accept` เดิมเช็กแค่ `target.login_entry_allowed`
ทั้งที่ `world_scene_entry.resolve_entry` (เส้นทางล็อกอินจริงที่ฟังก์ชันนี้ทำนาย) ปฏิเสธสองเงื่อนไข
ไม่ใช่หนึ่ง: `login_entry_allowed=False` **และ** ฉากที่ pin ไว้แต่ไม่มี spawn (`REFUSED_NO_PINNED_SPAWN`
ยกเว้น home) — โมดูลพี่น้อง `gm/login_scene_admission.py::_target_is_admissible` ปิดช่องเดียวกัน
ไปแล้วฝั่ง staging (docstring "TWO REGISTRY CONDITIONS, not one") แต่ `warp_scene_persist.py`
เขียนก่อนหน้านั้นและไม่เคยอ่านย้อนกลับ

**แก้**: เติมเงื่อนไขที่สองด้วยรูปเดียวกับ `_target_is_admissible` (home ยกเว้นเพราะ home ไม่อ่าน
spawn ของตัวเองเลย) · ทะเบียนจริงวันนี้ไม่มีฉากไหน spawnless (เหมือนที่ `login_scene_admission`
บันทึกไว้) ⇒ เทสใหม่ `LoginWouldAcceptSpawnConditionTests` ดัด registry (`dataclasses.replace`)
ให้มีแถว spawnless ชั่วคราว รูปเดียวกับ `TheSpawnConditionTests` ของโมดูลพี่น้อง แล้ววัดทั้งสองด้าน
(ฉาก spawnless ปกติ → ปฏิเสธ · home spawnless → ยังรับ)

### ข้อ 7 — `compose_refused_*` เป็น "คำที่ไม่มี input ใดไปถึง"

`OUTCOME_COMPOSE_REFUSED_PREFIX` ที่ `persist_warp_scene` ครอบ `warp_destination_position`
ไม่เคยถูก composer ทั้งสองตัวของโมดูลนี้ทำให้ raise ได้จริง (x/y/z ของ `WarpTarget` เป็น binary32
ที่อ่านกลับจากเฟรมเสมอ) — **ไม่ลบการ์ด** เพราะ `persist_warp_scene` ประกาศ NEVER RAISES
สำหรับ `WarpTarget` **ใด ๆ** ไม่ใช่แค่สองรูปที่ composer ปัจจุบันสร้าง (ผู้เรียกในอนาคต/เครื่องมือ replay
สร้าง `WarpTarget` ตรง ๆ ได้ ซึ่งไม่มีการบังคับชนิดฟิลด์เลยเพราะเป็น `@dataclass` เปล่า) ⇒ เพิ่มเทส
ที่สร้าง `WarpTarget` ด้วยฟิลด์ที่ไม่ใช่ตัวเลขตรง ๆ (ไม่ผ่าน composer) แล้ววัดว่าประตูนี้ตอบ
`compose_refused_ValueError` จริง ไม่มีแถวถูกเขียน ไม่มีค่าที่พิมพ์รั่วออกคอนโซล

## pf-adversary — เรียกจริง 1 ครั้ง (โควตา 1/2) ไม่เจอข้อบกพร่อง

รันใน worktree แยก ตรวจทั้งความถูกต้องของเงื่อนไข mirror เทียบ `resolve_entry` ตัวจริง
(รวมข้อยกเว้น home และคำถามเรื่อง identity-check/tuple-slip ที่โมดูลพี่น้องมี — พบว่าไม่จำเป็นที่นี่
เพราะ `login_would_accept` ไม่รับ registry จากผู้เรียกเหมือน `login_scene_admission`)
· revert เฉพาะตัวแก้ข้อ 6 ใน worktree แล้ววัดว่าเทสใหม่แดงจริง · มิวแทนต์ฉีดข้อความ error แทนชื่อชนิด
ยืนยันว่าเทส "ชื่อชนิดเท่านั้น" มีน้ำหนักจริง · รันไฟล์เทสสามแบบ (ปกติ/สลับลำดับคลาสใหม่ขึ้นก่อน/รันซ้ำ
สองรอบในโปรเซสเดียว) ไม่พบ cache ของ `_LOGIN_REGISTRY_SNAPSHOT` รั่วข้ามเทส · ยืนยันว่า
`WarpTarget("not-a-float", ...)` ไม่ถูก coerce จริง (dataclass เปล่า ไม่มี `__post_init__`)
**สรุป: ไม่เจอข้อบกพร่อง** — ไม่ต้องใช้โควตาครั้งที่สอง

## ชุดเทส

ระหว่างทาง (เฉพาะไฟล์ที่แตะ): `pytest tests/test_gm_warp_scene_persist.py` — 68 passed
· `pytest tests/test_gm_login_scene_admission.py tests/test_gm_chat_command_action.py
tests/test_gm_warp_position_confirmed.py tests/test_gm_chat_warp_way_out.py` — 264 passed,
181 subtests passed (กันรีเกรสชันของโมดูลพี่น้องและ caller)

ชุดเต็ม **รันครั้งเดียว** บนคอมมิตสุดท้ายจริง หลัง `git fetch origin main` (กิ่งเซิร์ฟเวอร์อยู่ที่ปลาย
`origin/main` (`bc658184`) อยู่แล้วตอน commit จึงไม่ต้อง merge เพิ่ม):
**10316 passed · 323 skipped · 19566 subtests passed · 0 failed** (422s)
— เขียว(cloud sanity, local pytest) เขียวสนิท ไม่มีใบแดง (ใบที่เคยแดงบน main ก่อนหน้า
`test_every_symbol_exemption_is_still_earned` เขียวแล้ว เพราะกิ่งอยู่ปลาย `#772`
ที่ COO `2348` ยืนยันว่าปิดช่องว่าง python 3.11 แล้ว)

## `#764` / `CORE-REQUEST-GM-055` / `CORE-REQUEST-GM-056` — สถานะไม่ขยับ

ไม่ได้แตะรอบนี้ · ทั้งสองใบยังรอจุดเสียบของ chief ใน `pf_login_game_server_v141.py`/`runtime.py`
(เขตของ chief ไม่ใช่ของสายนี้) — ตรวจแล้วยังไม่มีคำตอบใน `notes_to_chief/` ณ เวลาที่เขียนไฟล์นี้

## หมายเหตุเวลา (Addendum C)

`_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุดยัง `2026-09-04T20:34:01+07:00` — เดียวกับที่ `NOW.md` 21:55/22:00
บันทึกไว้แล้วว่าสะพานตาย (Panya ทราบแล้ว) ไม่ใช่นาฬิกาของรอบนี้ผิด · เวลาทุกจุดในไฟล์นี้มาจาก
`TZ=Asia/Bangkok date` ตรง ๆ

## backlog: อะไรบล็อกอยู่ที่ใคร

- **P-2 สีชื่อมอน** — ยังติดที่ **chief** (RE ใบที่สอง `0217` รอเลข ตั้งแต่ 03:06 · ตรวจ NOW.md
  รอบนี้ไม่พบว่าเลขถูกตั้งแล้ว)
- **P-3 ปุ่ม GMUI ทั้ง 3 หน้า** — ยังติดที่ **RE runner บนสะพาน** (`1328` ยังไม่มีผล คลาวด์เปิด
  client image ไม่ได้)
- **`CORE-REQUEST-GM-055`** (rollback wiring) และ **`CORE-REQUEST-GM-056`** (boot registry
  object แทนการอ่านดิสก์ครั้งที่สอง) — ทั้งคู่ติดที่ **chief** ยังไม่มีคำตอบ
- **GM-B `/speed` (b'')** — ติดที่ตัวเอง ยังไม่เริ่ม (นิยามใหม่ `0545` พร้อมแล้ว) = งานแรกที่ควรหยิบ
  รอบถัดไปถ้าไม่มีจดหมาย/คำตอบใหม่มาก่อน

**ว่างเพราะรอใคร**: รอบนี้ไม่ว่าง — หยิบข้อ 6/7 ที่ backlog ของรอบก่อนบันทึกไว้ว่า "เริ่มได้ทันที"

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มีสิ่งที่เห็นบนจอเปลี่ยนรอบนี้ — ปิดช่องว่างวัดคำศัพท์ภายใน/การ์ดกันไว้ล่วงหน้าสองข้อจากผล
adversary รอบก่อน ไม่ใช่พฤติกรรมที่ผู้เล่นเห็น (ทั้งสองการ์กันฉากที่ทะเบียนวันนี้ยังไม่มีจริง)

## nonclaim

- ไม่มีอะไรในรอบนี้ผ่านจอ · ไม่มีบัญชีใดได้/เสียสถานะ GM · ไม่มีขั้นตอนใดถูกข้ามด้วย GM
- ไม่ได้แตะ `runtime.py` / `app.py` / `pf_login_game_server_v141.py`
- ไม่ได้อ้างว่า P-2/P-3/GM-055/GM-056 ปิดแล้ว — ทั้งหมดยังติดที่ chief/RE runner ตามเดิม

## ค้นแล้ว: เจอ/ไม่เจอ

- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (รอบนี้วัดพฤติกรรมเซิร์ฟเวอร์
  ล้วน ไม่พึ่งข้อมูล client ใหม่)
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (เหตุผลเดียวกัน)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **ค้นแล้ว: เจอ** (ยืนยันขั้นแรกของรอบแล้ว)

## จบรอบ

1. **push ครบทั้งสองรีโปแล้ว**
   - `pirate-force-server` กิ่ง `claude/beautiful-sagan-f4pgh4` — 1 commit (`1286d2c3`)
   - `pf_bridge` กิ่ง `claude/serene-bell-f4pgh4` — claim + merge origin/main ×2 + ไฟล์รอบนี้ + จดหมาย
     + stub (ไฟล์ `_claim.md` ถูกลบบนกิ่งแล้ว ไฟล์รอบนี้แทนที่)
2. **`pirate-force-server#774`** "[LANE-GM] A live `/warp` now refuses a spawnless destination too,
   and compose_refused_ is proven reachable not dead" — เปิดแล้ว **ไม่ draft** · `PF-AUTOMERGE: v4`
   ใส่ตั้งแต่เปิด · **GET กลับมายืนยันแล้วว่า marker อยู่จริงใน body** (`mergeable_state: unstable`
   = เกตยังไม่ตัดสิน)
3. **`pf_bridge#1225`** (claim) — เติม `PF-AUTOMERGE: v4` เป็นขั้นสุดท้ายหลังข้อ 1/2 เสร็จ = **ปลดล็อก**
4. **push แล้ว รอ merge PR #774** · PR เซิร์ฟเวอร์: **เปิดแล้ว รอ gate** ไม่รอ gate ไม่รอ merge
   ตามกติกาจบรอบใหม่ (`COO 1229`)

-- LANE-GM รอบ `f4pgh4`
