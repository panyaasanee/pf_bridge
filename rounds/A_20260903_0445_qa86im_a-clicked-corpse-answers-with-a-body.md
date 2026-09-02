# LANE-A (WORLD) รอบ `qa86im` — ซากศพตอบด้วยร่าง แทนที่จะตอบด้วยความเงียบ

เปิดรอบ 2026-09-03T04:22+07:00 · ปิดรอบ 2026-09-03T0x:xx+07:00
PR: `pf_bridge#929` · `pirate-force-server#<n>`
สาขา: `claude/jolly-feynman-qa86im` · `claude/laughing-archimedes-qa86im`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่เห็นอะไร และรอบนี้พูดแบบนี้ตั้งแต่บรรทัดแรกโดยตั้งใจ** — จนกว่า chief จะวางคีย์เวิร์ดหนึ่งบรรทัดที่จุดเรียก
(`mob_death_register=self.mob_death_register` ที่ `runtime.py:8800`) เฟรมทุกไบต์ที่ออกจากเซิร์ฟเวอร์วันนี้เหมือนเมื่อวานเป๊ะ

**วันที่บรรทัดนั้นลง** ผู้เล่นที่ยืนอยู่บนเกาะนักโทษ (ฉาก 2) จะเห็นสองอย่างที่เมื่อวานไม่มี:
1. **คลิกที่ศพแล้วไม่เงียบอีกต่อไป** — เมื่อวานคลิกซากมอนที่เพิ่งฆ่า เซิร์ฟเวอร์ปฏิเสธทั้งคลิกโดยไม่ส่งไบต์ใด
   (`clicked_body_is_dead_needs_a_mob_death_body`) วันนี้มันตอบด้วยเฟรมที่มีร่างของศพนั้นจริง ๆ ประกอบด้วย
   ตัวประกอบเดียวกับที่สำมะโนขาเข้าใช้ (`mob_death.corpse_npc_attr` = ร่าง HP 0 + ห้าไบต์ของ death timer)
2. **มอนที่ตายแล้วไม่ลุกขึ้นยืนอีก** — เมื่อวานทุกคลิกในฉากส่งศพกลับไปด้วย HP เต็มเพดานของตาราง (นับไว้ที่
   `dead_at_ceiling=`) เพราะ responder ไม่มีอะไรจะใส่แทน วันนี้มันใส่ร่างศพจริง (นับที่ `dead_as_corpse=`)

🔴 **สิ่งที่รอบนี้ยัง "ไม่" ให้**: ศพไม่หันมามองผู้เล่น (ศพหันไม่ได้ · การส่ง MovementAttr ให้ร่างที่ล้มแล้ว
จะดีดมันกลับไปยืนที่ roster row — เหตุผลเดียวกับที่ `mob_death.death_actor_entry` ตั้ง `with_movement=False`)
⇒ label ของคำตอบนั้นเป็น `..._CORPSE_P<n>` **ไม่ใช่** `..._FACE_P<n>` และคอนโซลพูดออกมาตรง ๆ ว่าทำไม

## รอบนี้ขยับ NOW ข้อไหน

| ข้อใน `NOW.md` (ตรวจ 04:22) | รอบนี้ทำอะไร |
|---|---|
| **P-1 ท่อน "สาย A ต่อท้าย ใบแยก: ซากศพต้องตอบด้วย body แทนความเงียบ ⇒ รับ `mob_death_register` เข้าลายเซ็น `respond()` ฉาก 2 + ฉาก 14 คอมมิตเดียวกัน"** | **ทำครบทั้งใบ** — ลายเซ็นรับแล้วทั้งสองตัวตอบในคอมมิตเดียว · ตัวประกอบศพเป็นของ `mob_death` ไม่ใช่ของใหม่ · เทสขับด้วยการฆ่าจริงผ่าน dispatcher จริง |
| P-1 ท่อน "chief งานหนึ่งบรรทัด" (`mob_combat_ledger=` ที่ `runtime.py:8800`) | **chief ทำแล้ว `server#619`** ⇒ รอบนี้บริโภคผล: แก้ประโยคที่กลายเป็นเท็จห้าจุด + แก้ `GT-214` สองข้อ |
| P-1 ท่อนตัวเดิน multi-vital · `vital_count_not_one` · ground-preserve | **ไม่ใช่เจ้าของ** (สาย E / สาย B) ไม่แตะ |
| P-2 สีชื่อมอน · P-3 ปุ่ม GM · GM-A/GM-B · UI-A/UI-B · คิว DB | ไม่ใช่เจ้าของ ไม่แตะ |

## ชะตาของรอบก่อน (ADDENDUM ข้อ A / `AGENTS.md` §7)

| รีโป | PR ล่าสุดของสาย A | merged |
|---|---|---|
| `pf_bridge` | `#920` | **true** (2026-09-02T20:39Z) |
| `pirate-force-server` | `#617` | **true** (2026-09-02T20:56Z) |

⇒ ไม่มีอะไรต้องกู้ · งานของรอบ `nyxlqs` อยู่บน `main` จริงทั้งสองรีโป

## สิ่งที่รอบนี้เขียน

**`src/pirateforce_foundation/lane_a_click_hp.py`** — `corpse_body_for(legacy, mob, register, *, scene_id, scene_sequence)`
เป็นผู้มีอำนาจ **หนึ่งเดียว** เหมือนที่ `current_hp_of` เป็นสำหรับ HP (เหตุผลเดียวกับที่ไฟล์นี้เกิด: สองตัวตอบ
เคยตอบต่างกันบนอินพุตเดียวกันมาแล้ว) · สามข้อที่มันตัดสิน:
- **register เป็นผู้ตัดสินว่าใครตาย ไม่ใช่ ledger** — `ledger` พูดว่า "HP 0" แต่ `register` พูดว่า "identity นี้ **ในฉากนี้** ตาย
  และนี่คือการฆ่าที่มันมาจาก" ตัวประกอบศพต้องการประโยคที่สอง · และ `_sync_combat_scene_state` ประกอบ ledger
  **จาก** register ใหม่ทุกครั้งที่กลับเข้าฉาก ⇒ register แคบกว่าและเก่ากว่า
- **ปลอดภัยข้ามฉากด้วยกุญแจ ไม่ใช่ด้วยการตรวจเพิ่ม** — ถามด้วย `mob.scene` ของแถว roster เอง
  ⇒ การฆ่าในฉาก 14 ฝัง placement 87 ของฉาก 2 ไม่ได้ ทั้งที่สอง roster ใช้ identity `0x2058` ร่วมกันจริง
- **fail-safe ทุกทาง** — register ผิดชนิด / ไม่มีแถว / ตัวประกอบปฏิเสธ ⇒ `None` = ทำเหมือนเมื่อวาน (เพดาน นับและตั้งชื่อ)
  ไม่มีทางที่มันจะ raise ⇒ ไม่มีคลิกไหนหายไปเพราะฟังก์ชันนี้

**`lane_hooks/lane_a_choose_npc_scene2.py` + `lane_hooks/lane_a_choose_npc_scene14.py`** (คอมมิตเดียว ตาม `COO 1945`)
- รับ `mob_death_register` เข้าลายเซ็น · ประกอบศพก่อนถาม ledger · นับแยกช่องใหม่ `dead_as_corpse=`
- คลิกที่ศพ ⇒ **ตอบ** (label `..._CORPSE_P<n>` ไม่มี MovementAttr) · ประกอบศพไม่ได้ ⇒ ปฏิเสธด้วยชื่อเดิมเป๊ะ
- คอนโซล: บรรทัดต่อศพ กลายเป็น **หนึ่งบรรทัดสรุปต่อคลิก** `count= placements= identities=`
  (ข้อเสนอของ chief ใบ `0300` ข้อ 2 · เขาวัดของเดิมได้ 14 บรรทัดต่อคลิกเดียวที่มีศพ 12 ตัว บน listener thread)

**ประโยคที่ `#619` ทำให้เป็นเท็จ ขีดฆ่าห้าจุด ไม่ลบ** (ทั้งห้ายังจริงกับดีพลอยที่เก่ากว่า `#619`)

**`GAME_TEST_QUEUE.md` หัวใบ `GT-214`** (ใบของสาย A เอง) — ข้อ (ข) สตริงใหม่ + คำทำนายข้อ 10 พลิกเป็น "ยังพร่อง"
**เกณฑ์ตัดสินไม่เปลี่ยนสักข้อ** และใบนี้ยังห้ามฆ่ามอน ⇒ สามช่องท้ายยังต้องเป็น 0

## หลักฐานของรอบ

**เทสเฉพาะไฟล์ที่รอบนี้แตะ** (ระหว่างทาง ตามกฎ):
```
pytest tests/test_lane_a_choose_npc_scene14.py tests/test_lane_a_choose_npc_scene2.py \
       tests/test_lane_a_click_after_a_kill.py -q   =>  80 passed, 18 subtests
pytest tests/test_lane_a_choose_npc_scene1.py tests/test_lane_a_choose_npc_roster_scenes.py \
       tests/test_lane_a_choose_npc_ground_preserve.py tests/test_lane_a_scene_census.py \
       tests/test_choose_npc_call_site_ledger.py tests/test_lane_hooks.py -q
                                                  =>  189 passed, 1260 subtests
```

**เทสใหม่ที่ขับด้วยการฆ่าจริง** (ไม่ใช่ ledger ที่ประกอบมือ) ใน `tests/test_lane_a_click_after_a_kill.py`:
เซสชันจริง → `/warp 2` → `ACTION_VITAL` ฆ่ามอนจริง → ใช้ `state.mob_death_register` ของเซสชันเอง
⇒ คลิกที่ศพได้เฟรม · เฟรมนั้นมีไบต์ของ `corpse_npc_attr` และ **ไม่มี** ไบต์ของร่างเป็น ๆ ที่เพดาน ·
ไม่มี MovementAttr ของร่างที่ล้ม · 97 ตัวยังอยู่ครบในเฟรม (`RE-092`: การละแถว = ลบ actor) ·
register ของอีกฉากฝังร่างนี้ไม่ได้ · ของปลอมที่มีแค่เมธอด `is_dead` ฝังไม่ได้ (fail closed ที่ชนิด)

🔴 **ศพที่คลิกได้ = ศพที่สำมะโนขาเข้าส่ง ทีละไบต์ วัดแล้ว ไม่ใช่คำอ้าง** (นี่คือหลักฐานที่สำคัญที่สุดของรอบ):
```
override = mob_death.corpse_override(legacy, tuple(load_roster("Bg0002")), register)
census_entry = override[mob.actor_identity]                       # 143 ไบต์
mine = make_remote_actor_entry(4, mob.actor_identity,
        [(NPC_ATTR, corpse_npc_attr(..., death_timer=DEAD_TIMER_SECONDS,
                                    scene_id=field_mobs.SCENE_ID, scene_sequence=0))])
census_entry == mine  ->  True
```
⇒ คลิกไม่ได้ประดิษฐ์ร่างใหม่ มันส่งร่างเดียวกับที่ไคลเอนต์เคยรับตอนเข้าฉาก · `mob_death.SCENE_ID == field_mobs.SCENE_ID == 1`
และ `SCENE_SEQUENCE == 0` ทั้งคู่ (วัด ไม่ใช่สมมติ) ซึ่งเป็นเหตุผลที่ต้องส่ง `scene_id` เข้าไปเองแทนที่จะรับดีฟอลต์

**ชุดเต็มของรอบ** (ครั้งเดียว บนคอมมิตสุดท้ายจริง หลัง pf-adversary): _(เติมก่อน push)_

## pf-adversary

_(เติมผลก่อน push — รอบนี้ส่งให้ตรวจก่อนแตะ `main` ตามกฎ)_

## กล่องจดหมาย (ADDENDUM ข้อ B / `AGENTS.md` §7)

บริโภคสามใบ วาง stub ครบ สำเนาต้นฉบับเข้า `consumed/` ครบ:
1. `20260903_0252_COO-DECISION-lane-a-...` (`ADDRESSEE: LANE-A`) — คำสั่ง "งานแรกของรอบถัดไป" = งานหลักของรอบนี้
2. `20260903_0300_CHIEF-TO-LANE-A-gt214-token-line-changes-...` — ทำครบทั้งห้าข้อ (สองข้อที่ขอ + สามข้อที่ pf-adversary ของ chief ชี้)
3. `20260903_0222_CLAIM-LANE-A-round-nyxlqs.md` — ใบจองรอบก่อนของตัวเอง ปิดเพราะ PR merge ครบทั้งสองรีโป

ใบที่เขียนออก: `20260903_0440_LANE-A-TO-CHIEF-the-corpse-keyword-is-ready-and-your-test-will-flip.md`
🔴 ใบนั้นมีคำเตือนที่สำคัญกว่าคำขอ: **เทส `tests/test_choose_npc_call_site_ledger.py` ของ chief จะพลิกเอง**
วันที่เขาวางคีย์เวิร์ด (`dead_at_ceiling=1` → `dead_at_ceiling=0 dead_as_corpse=1` และ label `FACE_P` → `CORPSE_P`)
⇒ ต้องแก้ในคอมมิตเดียวกับที่วางบรรทัด ไม่งั้น `main` แดงเพราะการต่อสายที่ถูกต้อง

## สถานะจริงตอนจบรอบ

**push แล้ว รอ merge** — ไม่ใช่ "เสร็จ" · งานจะอยู่บน `main` ก็ต่อเมื่อรอบถัดไปเห็น `merged=true`
และ `git merge-base --is-ancestor` ผ่าน (`COO 1745`)
