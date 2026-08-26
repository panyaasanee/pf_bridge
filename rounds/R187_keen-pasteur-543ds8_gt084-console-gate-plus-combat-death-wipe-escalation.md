# R187 (session `keen-pasteur-543ds8` / `optimistic-mccarthy-543ds8`) — 2026-08-27 ~08:53-09:30 (+07:00)

## บริบทตอนเริ่มรอบ

รอบก่อนหน้า (R186) จบด้วย WIRED เดิม = 10/10 — เลขนั้นถูกถอนไปแล้วโดย `ATTENDED-URGENT` (03:00) และ
`COO-DECISION-WIRED-v2` (03:45): นิยาม "wired" เดิม (import/เรียกอะไรก็ได้) ผ่านได้แม้เลนไม่ส่งอะไรออกสายจริง
COO สั่งเป็นงานอันดับหนึ่งของรอบนี้: ต่อ `field_mobs.build_field_mob_population` เข้าเส้นบูตจริง ยืนยันด้วยบูต
headless + grep คอนโซล ก่อนงานอื่นทุกอย่าง

## ① สิ่งที่พบ — สมมติฐานตั้งต้นผิด: field-mob hostile bodies ถูกต่อสายไว้แล้วจริง เพียงแค่มองไม่เห็นบนคอนโซล

ตรวจสด `runtime.py` พบว่า `mob_death.full_roster_override` + `_apply_mob_death_census_override` ต่อเข้า
arrival census ไว้ถูกต้องแล้วตั้งแต่ commit `3036b03` (26 ส.ค.) — **ไม่ใช่ `build_field_mob_population` ที่ COO
สั่งให้ต่อ** (ฟังก์ชันนั้นยังไม่ถูกเรียกจากไหนเลยจริง แต่เป็นเส้นทางคนละเส้นที่ถูกแทนที่ด้วย full_roster_override
ไปแล้ว ไม่ใช่ของที่ต้องต่อเพิ่ม) วัดสดยืนยัน: census 115/115 ไม่หด · 13/13 identity ตรง · เฟรม hostile
byte-exact เทียบกับ `field_mobs.hostile_actor_entry` โดยตรง · **หนึ่ง** `make_runtime_remote_actors` call
เดียวสำหรับ arrival composition (ไม่ใช่สอง — จุดนี้คือจุดที่จะกลายเป็น world-wipe ถ้าทำผิด)

`GT-084`'s "0 hostile frames" (`20260827_0205_GT084-NO-RESULT-*.md`) คือช่องว่างการมองเห็น: grep หา
`FIELD_MOB`/`HOSTILE` ซึ่งไม่เคยมีอยู่จริงบน production path — ไม่ใช่หลักฐานว่าไบต์ไม่ออก สาย B วินิจฉัยเรื่อง
นี้เองที่ 08:10 (`rounds/B_20260827_0805_*.md`) และขอ wiring หนึ่งบรรทัดจาก chief (ไฟล์ของ chief เอง สายอื่นแตะ
ไม่ได้)

## ② สิ่งที่ทำ — เติมบรรทัดคอนโซลเดียวที่สาย B ขอ

`pirate-force-server` commit `dd5c785` (branch `claude/optimistic-mccarthy-543ds8`):
- `runtime.py:4899-4924` (+26 บรรทัด): `print(mob_death.describe_roster_override_coverage(mob_death_override,
  generation.actor_identities)[0])` ต่อท้ายบล็อก `_apply_mob_death_census_override` เดิม วางไว้**นอก** `if`
  เจตนา — override ว่างเปล่าต้องพิมพ์ `matched=0/0` ไม่ใช่เงียบ
- `tests/test_world_census_wiring.py` (+282 บรรทัด, 6 เทสใหม่): pin จำนวนประชากรไม่หด, 13 identity ถูก
  override เป็นเฟรม hostile byte-exact จริง, มีเรียก `make_runtime_remote_actors` ครั้งเดียว (ไม่ใช่สอง —
  mutation test ยืนยันว่าถ้าใครแอบต่อ field-mob เป็น sender ที่สอง เทสจะจับได้)
- เทสรวม: **3227 → 3233 ผ่าน** (0 regression) · บูต headless ยืนยันสด: ก่อนแก้ไม่มีบรรทัดคอนโซลนี้เลย (ผลลบ
  เดิมของ `GT-084` reproduce ได้จริง) หลังแก้พิมพ์ `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13
  missing=none` ทุกครั้งที่ census ประกอบสำเร็จ
- ผ่าน `pf-adversary` ก่อน commit — ไม่พบข้อบกพร่องที่บล็อก มีข้อสังเกตเดียวว่า print ไม่มี verbosity gate
  (ตั้งใจ ตรงตามที่ COO สั่งไว้)

`GAME_TEST_QUEUE.md`: เติมอัปเดตใต้ `GT-084` บอก grep token ที่ถูกต้องคือ `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE`
ไม่ใช่ `FIELD_MOB`/`HOSTILE` กันไม่ให้รอบ attended ถัดไปอ่านผลผิดซ้ำ

`AGENTS.md`: เพิ่มหัวข้อ WIRED v2 + กฎด่านคอนโซลก่อนเรียกเจ้าของ (cascade จาก `COO-DECISION 03:45` ข้อ 3)

## ③ สิ่งที่พบเพิ่ม — ยกระดับเป็น CHIEF-URGENT: `mob_combat`/`mob_death` ยังไม่ compose แบบเดียวกับ arrival

`mob_combat.py:989` (`bar_frames`) และ `mob_death.py:902` (`death_frames`) ส่ง `make_runtime_remote_actors`
แบบ **หนึ่งรายการเดี่ยว ไม่มีเงื่อนไข** บนบูตไร้แฟล็ก (`runtime.py:3828-3835`) — ไม่ผ่านจุด compose ที่ arrival
เพิ่งพิสูจน์ว่าใช้ได้ `RE-092` (ปิดแล้ว) ยืนยัน collection นี้เป็น replace-by-omission จริง ⇒ ถ้าเป็นเซแมนติก
เดียวกัน **ทุกหมัด/ทุกการตายจะล้าง registry 115-actor ทั้งก้อน** เขียน `notes_to_chief/20260827_0920_
CHIEF-URGENT-*.md` เสนอเป็น `CORE-REQUEST` ถัดไปของสาย B ไม่ได้ขอบล็อก `GT-084` (ริเดอร์ `OW1`-`OW3` เดิมทำ
หน้าที่สังเกตอยู่แล้ว) แต่เสนอว่าการแก้จริงควรมาก่อน M4 (29 ส.ค.)

## ④ กล่องจดหมาย

Panya ถามตรง (`0140`) ว่าทำไม RE-073/083/086/087/088 ยังไม่ปิดหัวใบ — ตรวจแล้วพบว่า R185 (`h53n8f`) ปิดหัวใบ
ทั้งห้าไปแล้วจริงก่อนรอบนี้เริ่ม (แค่สต๊อบ `.CONSUMED.txt` ของสามใบหายไปเพราะ naming drift) เขียนสต๊อบ backfill
ให้ครบ (`consumed/20260827_0140_*`, `0115_*`, `0056_*`) พร้อม `Action taken:` ตามที่ขอ พบ naming drift สามแบบ
ขนานกันในธรรมเนียม `.CONSUMED.txt` (`CHIEF-CLOSE-mailbox-stub-naming-drift-*.md`) — ปิดกลุ่มที่เหลือด้วย
precedent เดียวกับ `COO-DECISION 2146`/`CHIEF-CLOSE-148` ไม่ backfill ทีละใบ (ต้นทุนสูงกว่าประโยชน์)

## WIRED = 12/13 นับ import โดยตรง (v1, ล้าสมัยแล้ว) · WIRED v2 (ตัวที่นับจริง) ยังไม่วัดซ้ำทั้งกระดาน รอบนี้ยืนยัน
เฉพาะ `field_mobs`/`mob_death` census composition ว่าส่งเฟรมจริง (ผ่าน v2) — เลนอื่นยังต้องยืนยันแยก

## ค้างสำหรับรอบถัดไป

- `CORE-REQUEST` ใหม่ (สาย B): compose `mob_combat.bar_frames`/`mob_death.death_frames` เข้า full census
  เดียวกับ arrival แทน one-entry แยก (ดู ③) — ก่อน M4
- วัด WIRED v2 ให้ครบทั้ง 10-13 เลน ไม่ใช่แค่ field_mobs/mob_death ที่ยืนยันรอบนี้
- `docs/HYPOTHESIS_LEDGER.json`/`FUNCTIONAL_COVERAGE.json` P132 name-length inconsistency ที่ pf-adversary
  ชี้ (byte delta +3 ไม่ใช่ +5 สำหรับ P132) — เอกสารเล็กน้อย ไม่กระทบความถูกต้อง ให้สาย B แก้เมื่อสะดวก
- เครื่องมือ `tools/pf_consume_note.py` (เสนอ กันข naming drift ของสต๊อบ) — backlog ของสาย E เอง ไม่เร่งด่วน

## ไฟล์ที่แตะ

`pirate-force-server`: `src/pirateforce_foundation/runtime.py` (+26), `tests/test_world_census_wiring.py` (+282)
`pf_bridge`: `AGENTS.md` (+17), `GAME_TEST_QUEUE.md` (+1 block), `notes_to_chief/*` (2 chief notes + 3 backfilled
stubs), `rounds/R187_*.md` (ไฟล์นี้), `CHIEF_CONTINUATION.md` (ดัชนีบรรทัดเดียว)

## สิ่งที่ยังไม่ได้พิสูจน์

ผล client-observable ของ hostile bodies (สีแดง/ไม่แดง) ยังไม่มีใครเห็น — รอ `GT-084` attended จริง ยืนยันแค่
ชั้น wire/DB รอบนี้ ตามกฎหลักฐานสองชั้น
