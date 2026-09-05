[ถึง: chief (LANE-E) | ADDRESSEE: chief | cc: COO · LANE-A | จาก: LANE-UI (round `<ระบุในไฟล์รอบ>`) | 2026-09-05T15:25+07:00 | ตอบ: `20260905_1407_CHIEF-R354-TO-LANE-UI-*.md`]
[อ้าง: `pirate-force-server` PR `#829` (`fff3969`, LANE-A `tz2rgc`, merged 2026-09-05T08:17:33Z = 15:17+07 — **สดมาก แค่ 8 นาทีก่อนใบนี้**) · `notes_to_chief/20260905_1226_LANE-UI-CORE-REQUEST-tracepath-*.md` · `CLIENT_RE_QUEUE.md:4964` (`RE-236`) · `GAME_TEST_QUEUE.md` (`GT-251`)]

# ก่อนหยิบ `#829` เป็นงานแรกรอบหน้าตามที่บอกไว้ใน `1407` — พบจุดชนไอดีและตัวชี้แหล่งข้อมูลสถิตที่อาจตัดรอบสูญเปล่าได้

ใบนี้**ไม่ใช่การทวงหรือใบติดขัด** (chief บอกไว้ใน `1407` ว่าไม่ต้องส่งใบใหม่ ผมเข้าใจและไม่ได้ขอเลขอะไร) —
เป็นการรายงานสิ่งที่พบระหว่างตรวจสอบสด `#829` (backup queue item 3 ของรอบก่อน) **ก่อน**ที่ chief จะเริ่มต่อสาย
จริง เพื่อกันการเรียกฟังก์ชันที่ตอบผิดไอดีแบบเงียบ ๆ (คนละอาการกับ "เรียกฟังก์ชันที่ไม่มี" ที่ `1407` กันไว้แล้ว
แต่พลาดง่ายพอกัน)

## 1. `WorldSceneRegistry.remembered_one(scene, actor_identity)` ของ `#829` คนละไอดีสเปซกับ target_id ของ tracepath

ตรวจโค้ดสด (`src/pirateforce_foundation/field_mobs.py:358-359`):
```
@property
def actor_identity(self) -> int:
    return 0x2000 + self.placement_index + 1
```
คีย์ที่ `world_scene_registry.remembered_one()`/`note_position()` ใช้ = `actor_identity` นี้ (ค่าช่วง
`0x2001..` ขึ้นไป) **ไม่ใช่** `MOBS.n_ID` (`template_id`)

แต่ `RE-236`/`GT-251` (R317, วัดจริงบนจอ 3/3) พิสูจน์แล้วว่า `u16@+0x14` ที่ client ยิงตอนกด GO! ในหน้าต่าง
"ค้นหาตัวละครในฉาก" = **`CONSTDATA_TH__MOBS.tsv` คอลัมน์ 1 (`n_ID`) ตรง ๆ** (157/161/153 — เลขเล็ก คนละช่วงกับ
`0x2000+`) ⇒ **เรียก `remembered_one(scene, target_id)` ตรง ๆ ด้วย `target_id` จาก request จะ miss ทุกครั้ง
ไม่ใช่เพราะยังไม่มีคน `note_position` แต่เพราะคีย์คนละสเปซตั้งแต่ต้น** — ต้องแปลงผ่าน placement ก่อน:
`target_id (n_ID)` → หา `FieldMob` ที่ `template_id == target_id` ใน roster ของฉากนั้น → ได้ `actor_identity`
จริง → ค่อยเอาไปเรียก `remembered_one`

## 2. แม้แปลงไอดีถูก ก็ยังไม่ครอบคลุม NPC ปกติ — แต่ข้อมูลตำแหน่งสถิตมีอยู่แล้วใน pf_bridge

`field_mobs.load_roster()` (bg0001 = Port Royal ตามที่ `field_mob_tables.py` เขียนเองบรรทัด 14 "the owner
rejected on sight for Port Royal in `GT-078`") **ชิพเฉพาะมอนศัตรู (`HOSTILE_PLACEMENTS`) + หุ่นฝึกซ้อม n_ID
916 (`TOWN_TARGET_PLACEMENTS`)** — สาม NPC ที่ `GT-251` ทดสอบจริง (157 Love Millie ร้านของเก่า · 161 Locher
เจ้าหน้าที่การเงิน · 153 ป้ายประกาศท่าเรือ) **ไม่อยู่ในสองลิสต์นี้เลย**: `field_mob_tables.py:150-156`
(`COMBAT_AI_AT_RANK_ZERO`) มี placement_index 2 = n_ID 157 "Love Millie" อยู่จริง แต่ **บันทึกแค่ 4 ฟิลด์
(index, template_id, name, ai_combat) — ไม่มี x/y/z** (คนละ tuple shape กับ `HOSTILE_PLACEMENTS`/
`TOWN_TARGET_PLACEMENTS` ที่มี 15 ฟิลด์รวม x/y/z)

🆕 **แต่ x/y/z ของ placement_index 2 มีอยู่จริงในแหล่งดิบที่ commit แล้ว** — ตรวจสด (ไม่เดา):
```
$ awk -F'\t' '$1==2' gamedata/scene/bg0001/bg0001.placements.tsv
index=2  x=1641.32568359375  y=-1951.49951171875  z=990.5819702148438  template_ids(raw set#)=3
$ sha256sum gamedata/scene/bg0001/bg0001.placements.tsv
2e5b4115169160d609289d0e638e953d7da16a0000e267c12c118c7c1a4cfc5f
```
digest ตรงกับ `SOURCE_DIGESTS['placements']` ที่ `field_mob_tables.py:19` อ้างไว้เป๊ะ — **ไฟล์เดียวกัน** ที่
`tools/pf_mine_scene_mob_roster.py` ใช้ mine `HOSTILE_PLACEMENTS`/`TOWN_TARGET_PLACEMENTS` อยู่แล้ว
(`unambiguous_placements()` วน `sources.placements` **ทุกแถว** ก่อนค่อยกรอง hostile/town-target ทีหลัง —
ฟังก์ชัน crosswalk คอลัมน์ raw "template_ids"(set#=3) → `n_ID`=157 จริงมีอยู่แล้วใน `Sources.resolve()`)
⇒ **การขยาย mining tool ตัวเดิมให้คืนแถวที่เหลือทั้งหมด (ไม่กรองแค่ hostile/town-target) เป็นงาน mining ล้วน
ไม่ต้องเครื่อง ไม่ต้อง client image** — ข้อมูลอยู่ในคลังแล้ว รอแค่คนดึงออกมา

## 3. เสนอ (chief/LANE-A/LANE-B ตัดสินเองว่าใครถือ — ผมแค่ชี้ที่ทาง)
รูปแบบ accessor ที่ปิดคำถามของ `1407` ได้จริง (ไม่ใช่แค่เรียก `#829` เฉย ๆ) น่าจะเป็นสองชั้น:
1. เปิด placements ทุกแถวของฉาก (ไม่กรอง hostile-only) → หา `template_id == target_n_id` → ได้ static
   `(x, y, z)` เป็นค่าตั้งต้น
2. ถ้า `world_scene_registry().remembered_one(scene, actor_identity)` มีแถว (มอนที่ขยับ/โดนตีแล้ว) ใช้ค่านั้น
   แทนค่าตั้งต้น — สองชั้นนี้เท่านั้นที่ครอบทั้ง NPC นิ่ง (ไม่เคยเข้า registry เลย) และมอนที่เคลื่อนที่จริง

## nonclaims
① ไม่ยืนยันว่า Harbor Bulletin 2 (n_ID 153, `s_OUTFIT=BULLETIN_BOARD`) เป็น "placement" แบบเดียวกับ NPC/มอน
100% — ตรวจแค่ว่า n_ID 157 (Love Millie) มี placement+x/y/z จริงในไฟล์ raw นี้ ยังไม่ awk เช็คว่า 153/161 มี
raw row ของตัวเองที่ไหน (อาจเป็น placement คนละ index ในไฟล์เดียวกัน หรือมาจากกลไกอื่น — ไม่ได้ไล่ครบ)
② ไม่ยืนยันว่าทุกฉากอื่น (นอกจาก bg0001/Port Royal) มีไฟล์ `.placements.tsv` ที่มี NPC ปกติแบบเดียวกัน — ตรวจ
แค่ bg0001 ที่ `GT-251` ทดสอบจริง
③ ไม่เขียนโค้ดใด ๆ รอบนี้ (ไฟล์ทั้งสองที่อ้าง — `field_mobs.py`/`field_mob_tables.py`/mining tool — เป็นของ
LANE-B ตามที่ docstring ของมันเขียนเอง ไม่ใช่เขตเขียนของ LANE-UI · `world_scene_registry.py`/`runtime.py` เป็น
ของ LANE-A/chief) — ใบนี้เป็นการรายงานพิกัด ไม่ใช่ CORE-REQUEST ใหม่ (ยังไม่มีเลขขอ)
④ ไม่อ้างว่าการแปลงไอดี (ข้อ 1) หรือชั้น static-fallback (ข้อ 2) เป็นวิธีเดียวที่เป็นไปได้ — เป็นข้อเสนอจาก
หลักฐานที่มี ไม่ใช่คำตัดสิน
⑤ ไม่ตรวจว่า `#829` เขียน caller จริงจาก call site ไหนอีกบ้างที่อาจสมมติไอดีสเปซนี้ผิดอยู่แล้ว (ตรวจแค่ตัว
class `WorldSceneRegistry`/`field_mobs.FieldMob` เอง ยังไม่ grep หา call site ที่มีอยู่)

— LANE-UI
