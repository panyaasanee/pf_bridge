[LANE-B (COMBAT) · round `2pnu4l` · 2026-08-28T04:5x+07:00 · ADDRESSEE: chief (สำหรับบันทึก), COO (cc)]

# STATUS: RE-117 บริโภคแล้ว -- level wired เข้า NPCAttr wire ของมอนสนาม, MP ยังไม่แตะ

## สรุป

`RE-117` (static, ปิดโดย RE runner 04:14) พิสูจน์ว่า NPCAttr ใช้ BasicAttr bit `0x0002` (level,
+0x5E, u16 tag `0x12`) และ `0x0010`/`0x0020` (MP cur/max) ชุดเดียวกับ PC ActorAttr จริง (ผ่าน
common serializer `0x004656F0`) -- ไม่ใช่แค่ PC-only บิตอย่างที่เคยสงสัยไว้ตอนเปิดใบรอบ `gi7bxs`

รอบนี้ (`pirate-force-server`) wire **level** เข้า `field_mobs.hostile_npc_attr` (splice บน
output ของ `legacy.make_npc_attr` -- ไม่แตะไฟล์ของ chief) และแก้ `mob_death.py`'s independent
composer (`_compose_body`/`_timer_offset`) ให้ตรงกัน ค่าใช้ `mob.level` ที่ขุดจาก MOBS อยู่แล้ว
เสมอ (แนวทางเดียวกับที่ `movement_speed` ถูกต่อสายไปแล้วรอบก่อน ตาม COO-DECISION
2026-08-28T01:46+07:00)

**MP cur/max ไม่แตะ** -- RE-117 เองบอกชัดว่าไม่มีตาราง MP สำหรับมอน/NPC ในข้อมูลที่ขุดมาถึงตอนนี้
(`MOBS`/`STANDARD_MOB` ไม่มีคอลัมน์นี้) การประดิษฐ์ค่าขึ้นมาจะขัดกฎหลักฐานสองชั้นตรง ๆ -- ถ้า COO/
เจ้าของต้องการ MP บนมอน ต้องมีแหล่งข้อมูลใหม่ก่อน (ใบขอแยกได้ถ้าต้องการ ยังไม่เปิดเองเพราะไม่มี
สัญญาณว่าเป็นของที่ต้องการตอนนี้)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มี -- RE-117 เองพิสูจน์แค่ wire surface ไม่ใช่ UI consumer ยังไม่มีหลักฐานว่า client แสดง level
ของมอนที่ target panel/HUD จากบิตนี้ ถ้ามีรอบ attended ที่เห็นอะไรเปลี่ยน (เช่น level โผล่ที่ target
panel) นั่นคือของใหม่ที่ต้องเปิดใบ GT แยก

## เทส

Full suite `pirate-force-server`: 3724 passed, 323 skipped, 0 failures (ติดตั้ง capstone/pefile
ในแซนด์บ็อกซ์รอบนี้เลยไม่มี collection error 16-17 ตัวที่รอบก่อน ๆ รายงานไว้) pin document 3 ไฟล์
(`scenarios/field_mobs_hostile_001.json`, `combat_death_001.json`, `combat_first_hit_001.json`)
regenerate สดจากโค้ดจริง ไม่มีจุดไหนพิมพ์ค่าเอง

## Addendum v2 ข้อ A/B/G ตรวจแล้ว

- ข้อ A: `pf_bridge#266`/`pirate-force-server#167` (รอบก่อน) `merged=true` ทั้งคู่ -- ไม่ต้องกู้
- ข้อ B: `RE-117` เป็นใบเดียวที่ค้างของสาย B -- บริโภคแล้วตามข้างต้น backfill stub ของ
  `PANYA-DECISION-pause-M2` (เนื้อหาถูกทำผ่าน M1-P ไปแล้ว ไม่มีอะไรใหม่ต้องทำ)
- ข้อ G (world-wipe fix): **เก่าไปแล้วตั้งแต่รอบ `wcpm2h` (22:36)** -- แก้จริงตั้งแต่ R188
  (`CORE-REQUEST-008`), `GT-084-R2` วิ่งไปแล้วจริง (ผล `notes_to_chief/20260827_1620_*.md`) ไม่ใช่
  งานค้างของสาย B อีกต่อไป (บันทึกซ้ำไว้กันรอบถัดไปไล่บรรทัดผิด)

รอบก่อนหน้า (`xfgdv1`) เปิด `CORE-REQUEST` ให้ chief ต่อสาย `check_attack_cadence` เข้า
`runtime.py` (spam-click fix ที่สร้างเสร็จแล้วแต่ไม่เคยถูกเรียก) -- ตรวจแล้ว **chief ต่อสายแล้วจริง**
รอบ R205 (`GAME_TEST_QUEUE.md` GT-084 UPDATE 04:1x) ไม่มีอะไรให้สาย B ทำเพิ่มจากจดหมายนั้น

-- สาย B · COMBAT
