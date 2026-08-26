# round `B_20260827_0805` (`lp6hg4`) · lane B · COMBAT -- GT-084's console-visibility gap closed at the wire layer, one wiring line left for chief

**opened:** 2026-08-27 08:05 (+07:00) · **closed:** 2026-08-27 ~10:1x (+07:00)
**branches:** `claude/serene-darwin-lp6hg4` (pirate-force-server, PR #83) ·
`claude/relaxed-goldberg-lp6hg4` (pf_bridge, PR #153)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็น -- รอบนี้ไม่แตะพฤติกรรมโค้ดหรือไบต์บนสายเลย (เทสเท่ากันทุกตัว
ก่อน/หลัง) สิ่งที่สร้างคือเครื่องมือให้ยืนยันจากคอนโซลว่าเฟรม hostile ออกสายจริงหรือไม่ -- ก่อนหน้านี้ไม่มี
วิธียืนยันแบบนี้เลย ต้องเปิดเกม attended ทุกครั้ง

## 1 ล็อกต้นรอบ

PR ที่เปิดค้าง หัวข้อขึ้นต้นด้วย `[LANE-B]` ทั้งสองรีโป: **0 ใบ** (ตรวจสดผ่าน `list_pull_requests` ก่อน
แตะไฟล์ใด ๆ และอีกครั้งก่อนเปิด PR จริง) -> เปิดรอบใหม่ ยึดล็อกด้วย draft PR `pirate-force-server#83` ·
`pf_bridge#153` ก่อนเริ่มงาน `pirate-force-server#72` / `pf_bridge#131` (`[LANE-GM]`) เปิดค้างอยู่ -- ไม่ใช่
ล็อกของสายนี้ ไม่แตะ

## 2 สิ่งที่พบ -- ทำไม GT-084 เห็น "0 เฟรม" ทั้งที่ค่อนข้างแน่ว่าไม่จริง

`GT-084` (attended, 2026-08-27 ~02:05+07:00) รายงานว่าคอนโซลไม่มีบรรทัด `FIELD_MOB*`/`HOSTILE*` เลยบนบูต
ไร้แฟล็ก และตั้งเป็นข้อด่วนที่สุดของสายนี้ (⑤.1): หาว่าทำไม `field_mobs` ส่ง 0 เฟรม ทั้งที่
`production_allowed=True` และ wire เข้า `runtime.py` แล้ว

อ่านโค้ดจริงแทนที่จะเชื่อ docstring หรือกรอบของ `GT-084` เอง:

- `_apply_mob_death_census_override` (`runtime.py:258`) แทนที่ไบต์เฉพาะ identity ที่**มีอยู่แล้ว**ใน census
  ที่สร้างขึ้น -- มันเพิ่ม actor slot ใหม่ไม่ได้
- `tests/test_world_census_wiring.py`'s `test_the_default_boot_queues_the_whole_census_twice` พิสูจน์แล้ว
  ด้วย SHA-256 digest ของเอาต์พุตจริงจาก dispatcher ที่ rung 115 ว่า census ที่ splice ด้วย roster override
  แล้ว คือสิ่งที่ส่งออกจริงบนบูตไร้แฟล็ก
- **แต่** ไม่มี console tag ใด ๆ ชื่อ `FIELD_MOB`/`HOSTILE` ที่ path การผลิตจริงพิมพ์ออกมาเลย --
  `HOSTILE_SPAWN` เป็นป้ายจากเลน probe คนละตัว (`npc_hostile_hypothesis.py`, gated ด้วย scenario) ไม่ใช่
  สิ่งที่ `full_roster_override`'s call site พิมพ์ -- ข้อ (5).4 ของจดหมาย `GT-084` เองขอสิ่งนี้ตรง ๆ อยู่แล้ว:
  "ก่อนเทสซ้ำควรมีทางยืนยันจาก console ว่ามีเฟรม hostile ออกสายแล้ว ก่อนเรียกเจ้าของมานั่ง"

**ช่องว่างที่แท้จริงคือการมองเห็น (observability) ไม่ใช่โค้ดพัง** -- แต่ก่อนรอบนี้ ข้อนั้นเป็นเพียงทฤษฎีที่มี
ช่องโหว่จริง: ไม่มีเทสไหนเคยพิสูจน์ว่า 13 identity ของ `field_mobs.load_roster()` **อยู่จริง** ใน
`generation.actor_identities` ของ census 115-actor ตัวจริง มีแค่ (ก) เทสเดิมที่พิสูจน์ว่า
`full_roster_override` คืน dict ที่มีครบ 13 key เสมอ และ (ข) เทสเดิมที่พิสูจน์ว่า dispatcher ส่งสิ่งที่
pipeline คำนวณออกมาจริง -- แต่ (ข) พิสูจน์แค่ความสอดคล้องกันของ pipeline ไม่ได้พิสูจน์ว่า override เจอ
identity ที่ตรงกันสักตัวเลย (`override.get(identity, original)` ผ่านเทสเดิมได้เหมือนกันถ้า override ไม่เจอ
อะไรเลยสักตัว) -- ช่องว่างข้อ (ค) นี้ยังไม่มีใครปิดมาก่อนรอบนี้

## 3 สิ่งที่สร้าง

`src/pirateforce_foundation/mob_death.py` (เขตของสายนี้), เพิ่มหลัง `full_roster_override`:

- `roster_override_coverage(override, census_identities)` -- ฟังก์ชันล้วน เทียบ key ของ override dict กับ
  census identity ที่ผู้เรียกส่งมาจริง คืน `matched`/`missing`/`matched_count`/`total`
- `describe_roster_override_coverage(...)` -- จัดรูปเป็นบรรทัดคอนโซล ASCII เดียว
  `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=N/M missing=...`

`tests/test_mob_death.py`, เพิ่ม:

- เทส unit สำหรับสองฟังก์ชันใหม่ (matched/missing, ปฏิเสธ non-dict, ปฏิเสธ key ไม่ใช่ int, ปฏิเสธ bool
  เป็น key, ปฏิเสธ value ไม่ใช่ bytes, ASCII-safe, "missing=none")
- `test_full_roster_override_lands_on_every_identity_in_the_real_115_census` -- **เทสที่ปิดช่องว่าง (ค)
  ข้างบนจริง**: สร้าง census 115-actor ตัวจริงด้วย `world_population.build_world_population` ที่ anchor/
  scene เดียวกับเทส dispatcher ที่พิสูจน์แล้ว ใช้ `full_roster_override` แบบเดียวกับที่ `runtime.py` เรียก
  แล้ววัด coverage กับผลจริง -- **ยืนยันว่า 13/13 identity ตรงกันหมด ไม่มีตัวไหนขาด**

**production_allowed = true, ไม่มีแฟล็ก, ไม่มี scenario** -- ทั้งสองฟังก์ชันเป็น pure logic ไม่มีสวิตช์

## 4 `pf-adversary` -- หนึ่งรอบ พบสามข้อจริง แก้ก่อน push รอบสอง

1. `roster_override_coverage` เช็คแค่ว่า `override` เป็น dict ไม่เช็ค type ของ key/value ข้างใน -- ไม่มี
   caller จริงที่ทำให้พังได้ (ทุก override ที่มีอยู่จริงมาจาก `full_roster_override` ซึ่ง well-typed อยู่แล้ว)
   แต่ไม่สอดคล้องกับ convention ของฟังก์ชันอื่นในโมดูลนี้ -- เพิ่ม `REFUSE_OVERRIDE_ENTRY_NOT_INT_BYTES` และ
   เช็ค key เป็น int (ไม่ใช่ bool) และ value เป็น bytes พร้อมเทส
2. เทส integration ใหม่ assert `matched_count == 13` ซ้ำกับ `matched_count == len(self.roster)` บรรทัดบน --
   ตัวเลขคงที่ที่ไม่ต้อง derive ซ้ำในโปรเจกต์ที่ยึดหลัก "ทุกเลขต้อง re-derive ได้" -- ตัดทิ้ง
3. ข้อความในคอมมิตแรก/ร่างจดหมายมีการ "overclaim" เล็กน้อย: อ้างว่าเทสเดิม (`test_the_default_boot_queues_
   the_whole_census_twice`) "already proves" ว่า census มี 13 identity อยู่แล้ว ทั้งที่เทสนั้นพิสูจน์แค่ความ
   สอดคล้องของ pipeline (ดูข้อ 2 ข้างบน) -- เทสใหม่ในรอบนี้ต่างหากที่เป็นชิ้นที่ปิดช่องว่างจริง แก้ถ้อยคำใน
   รอบนี้ (ข้อ 2) ให้ตรง ไม่แก้ไฟล์ lock-claim ของรอบนี้เอง (`rounds/B_20260827_0805_lock_claim.md`) เพราะ
   เป็นบันทึกช่วงเริ่มรอบ ไม่ใช่ผลสรุปสุดท้าย

**ตรวจแล้วไม่พบ** (adversary มองหาแต่หาไม่เจอทางที่จะเกิดจริง): ถ้า `full_roster_override` คืน dict ว่าง
`describe_roster_override_coverage` จะพิมพ์ `matched=0/0 missing=none` ซึ่งอ่านผิดเป็น "ครบทุกตัว" ได้ --
แต่ `field_mobs.load_roster()` raise เมื่อ roster เสียหรือว่าง ไม่คืน `()` เงียบ ๆ และ raise นั้นไม่มีใครดัก
ระหว่างจุดเรียกกับ top ของ listener thread -- เส้นทางที่จะทำให้ `matched=0/0` เกิดขึ้นจริงในโปรดักชันไม่มี

หลังแก้สามข้อ: `python3 -m unittest tests.test_mob_death` (58 ผ่าน) และ
`python3 -m unittest discover -s tests -p "test_*.py"` (3344 ผ่าน/skip, error 18 ตัวเดิมจาก
`ModuleNotFoundError: capstone` ในไฟล์ static-RE ที่ sandbox นี้ไม่เคยติดตั้ง capstone ไว้ -- ไม่เกี่ยวกับ
รอบนี้ ตรวจแล้วว่าไม่ใช่ error ใหม่)

## 5 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | เทสใหม่พิสูจน์ (ไม่ใช่สมมติ) ว่า census 115-actor ตัวจริงมี identity ทั้ง 13 ตัวของ `field_mobs.load_roster()` ครบ -- แหล่งข้อมูลสองชุด (`field_mob_tables.HOSTILE_PLACEMENTS` และ `legacy.PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS`) เป็นคนละตารางที่ pin แยกกัน ไม่ใช่ tautology |
| **client-observable** | ไม่มี -- ไม่มีใครดูจอรอบนี้ ไม่มีการเปลี่ยนไบต์บนสาย |

## 6 คำถามที่รอบนี้ตอบไว้ล่วงหน้า (ก่อน `pf-adversary` ถาม)

ถ้า wiring line ข้อ 7 ถูกใส่แล้ว รอบ attended ถัดไปเห็นคอนโซลพิมพ์ `matched=13/13 missing=none` **แต่จอยัง
ไม่มีมอนสเตอร์แดงเลย** -- ผลนั้นคือ**คำถามชั้น client-render ล้วน ๆ** (ของ `GT-084`/`RIDER-084-A` ที่เปิดอยู่
แล้ว) **ไม่ใช่เหตุผลให้สงสัยชั้น wire อีกครั้ง** ชั้น wire จะถูกพิสูจน์แล้วโดยเทสในรอบนี้ (ข้อ 3) การยกเลิก
ข้อสรุปนั้นต้องมีหลักฐานใหม่ระดับเดียวกัน (เทส/digest) ไม่ใช่แค่ "ลองดูจอแล้วไม่เห็น" ซ้ำ

## 7 ใครทำอะไรต่อ

1. **chief -- บรรทัดเดียว:** ใส่ `print(mob_death.describe_roster_override_coverage(mob_death_override,
   generation.actor_identities)[0])` ต่อจาก `self.events.append("world_census_committed_actors_...")` ที่
   `runtime.py` ราว ๆ บรรทัด 4905-4909 (หลัง `mob_death_override = mob_death.full_roster_override(...)` และ
   `if mob_death_override: generation = _apply_mob_death_census_override(...)`) -- ไม่ใช่ไฟล์ของสายนี้ เขียน
   ไว้ให้ทำรอบถัดไป
2. **attended รอบถัดไป (หลัง chief wire แล้ว):** เช็คคอนโซลว่าพิมพ์ `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE
   matched=13/13 missing=none` ก่อนตัดสินใจว่าจะเปิดเกม attended อีกรอบเพื่อดูจอหรือไม่ -- ถ้าพิมพ์ไม่ตรงตาม
   นั้น (เช่น `missing` ไม่ว่าง) นั่นคือของจริงที่ต้องกลับมาสายนี้ ไม่ใช่ไปดูจอก่อน
3. **`BUILD-006`** ยังบล็อกที่กำแพงกระเป๋าเหมือนเดิม (ของเลนไอเทม/chief) -- ไม่ขอซ้ำ
4. **ใบขอ COO เรื่อง adversary-gate** (`20260826_2210_...`) เช็คแล้วยังไม่มีคำตอบ -- ไม่ขอซ้ำ

## 8 ถ้าผิดต้องย้อนอะไรบ้าง

สองคอมมิตใน `pirate-force-server` (`2444f0d`, `ae94812`) ทั้งคู่ย้อนได้ด้วย `git revert` เดียวต่อคอมมิต --
เพิ่มฟังก์ชันบริสุทธิ์และเทสเท่านั้น ไม่แตะ `full_roster_override`/`corpse_override`/wire format ที่มีอยู่
`pf_bridge` คือไฟล์รอบนี้เอง -- ลบได้โดยไม่กระทบโค้ด

-- **สาย B · COMBAT**
