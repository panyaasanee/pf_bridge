# LANE-B (COMBAT) รอบ `ltuevf` — 2026-09-05T12:16+07:00 → 12:29+07:00

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่มีอะไรบนจอ (P-2 ยังปิดประตูตี GT ทุกฉาก) แต่ log/console
ของบูตแรกของทุกเซสชันจะไม่พิมพ์ `_REFUSED reason=refused_cell_has_no_scene_to_publish` ตอนเปิดกระเป๋า
บนพื้นว่างอีกต่อไป (จุดที่ R316 เพิ่งเห็นเป็นบรรทัดแรกของทุกเซสชัน) — เมื่อ chief เดินสาย `scene=` ตามที่ขอไว้
ข้างล่าง มันจะพิมพ์ `GROUND_REANNOUNCE_AFTER_SECOND_PWD scene=<n> items=0` แทน ซึ่งเป็นคำตอบเดียวกับที่
เคสมีของบนพื้นได้อยู่แล้ว แค่ตอนพื้นยังไม่เคยมีของก็ตอบแบบเดียวกัน ไม่ใช่ REFUSED

## TWO_SESSIONS_SAME_SCENE
ไม่กระทบ — งานรอบนี้เป็น console-token/reporting fix ที่ชั้น wire composition ของ session เดียว
(`reannounce_ground`/`sustain_a_kill`) ไม่แตะสถาปัตยกรรมโลกร่วม และไม่แตะทะเบียนของพื้นข้าม session
(`COO-DECISION 20260905_1152` เพิ่งย้ายเจ้าของทะเบียนของพื้นข้าม session ไป LANE-A — B ยังเป็นผู้เขียน
ตอนของตกและยังเป็นเจ้าของ "ประกอบเฟรมอะไรให้ฉากที่ cell รู้จัก" ซึ่งเป็นชั้นที่รอบนี้แก้ ไม่ทับกัน)

---

## 1. ADVERSARY_PENDING `#814` (r6isy5) — resolved: no defect found

รีวิวโค้ดที่ merge จริงบน main (`e2647900`) ตามที่ COO สั่งเป็นงานแรกของรอบ:

- `field_mob_tables_bg0004.py`: ตรวจ HOSTILE_PLACEMENTS 7 แถว/5 template (94,97,103,246,519) ตรงกับที่
  `mob_death.py` ใช้ตั้งใบฆ่า, ตรวจ WITHDRAWN/UNRESOLVED/COMBAT_AI_AT_RANK_ZERO ครบตามที่ docstring อ้าง
- `field_mobs.py` (`BG0004_SCENE`, `_SCENE_TABLE_MODULES`): ลงทะเบียนถูกคีย์ (`'bg0004'`), คอมเมนต์อธิบาย
  การชนกับ template 103 ของ Bg0002 ตรงกับสิ่งที่ `mob_death.WIDENING_RULING_SCENES` ทำจริง
- `mob_scene_recompose.py` (`COMPOSER_BG0004`, `_build_bg0004`, `NON_DELEGATED_COMPOSER_KINDS`): รูปแบบ
  เดียวกับ bg0002/bg0003/bg0005 เป๊ะ, `_build_bg0004.serves_scene_id` ผูกถูกต้อง (คุมโดย
  `assert_every_non_delegated_kind_has_a_builder` ที่ pf-adversary รอบก่อนบังคับให้เช็ค `serves_scene_id`
  ไม่ใช่แค่ key set)
- `mob_death.py` ใบฆ่าฉาก 4 ห้า template: `WIDENING_RULINGS`/`WIDENING_RULING_SCENES` ทั้งสองมีคู่กันครบ
  (ไม่มีใบไหนไม่มีการผูก scene) · การชนสามทาง (`0x2046` ในฉาก 3/4/5) ถูกกันด้วย scene tie ที่ `kill()`
  บรรทัด 2311-2312 เช็คจริง (อ่านโค้ดยืนยันแล้ว ไม่ใช่แค่อ่านคอมเมนต์)

วิธีที่ยืนยัน: อ่านซอร์สทั้งสี่ไฟล์ตามจุดที่ COO ระบุ + รัน
`tests/test_field_mob_tables_bg0004.py tests/test_mob_death_wired_widening.py tests/test_field_mobs.py
tests/test_mob_loot.py tests/test_mob_death_persistence.py tests/test_mob_stat_fabrication_guard.py
tests/test_mob_combat_bg0015_gates.py tests/test_gm_identity_registry_census.py tests/test_scene_door_walk.py
tests/test_field_mob_tables_bg0005.py` → **425 passed, 1197 subtests passed**

**ADVERSARY_PENDING (r6isy5) resolved: no defect found, verified by reading the four named modules against
the round's own claims (composer registration shape, scene-tie coverage, cross-scene collision guard) and
running the ten test files the round itself flagged as adversary-relevant.**

## 2. ข้อ 3(ข) — พื้นว่างตอบ `_REFUSED` → `GROUND_REANNOUNCE_AFTER_SECOND_PWD ... items=0`

**ไฟล์ที่แก้**: `src/pirateforce_foundation/mob_drop_presence.py`, `tests/test_mob_drop_presence_ground_reannounce.py`
(pirate-force-server, กิ่ง `claude/magical-hawking-ltuevf`)

`reannounce_ground(cell, legacy, scene=None)` มีจุดที่ทำให้ REFUSED ผิดเคสอยู่สองจุด, แก้ทั้งคู่:

1. **การเช็คก่อนเรียก `sustain_a_kill`**: เดิม `cell_scene is None` ถูกนับรวมเป็น "scene disagrees" (refuse
   ทันทีก่อนถึง `sustain_a_kill` เลย) — แก้ให้ `cell_scene is None` (cell ยังไม่เคยรู้จักฉากใด ๆ) ไม่ใช่
   "ไม่ตรงกัน" ปล่อยให้ตกไปที่ `sustain_a_kill` ตามปกติ ส่วน cell ที่ **มี** ฉากอยู่แล้วแต่ไม่ตรงกับที่
   caller ส่งมา ยังถูก refuse เหมือนเดิมทุกประการ
2. **สาขา `step.refused`**: เมื่อ `step.state == REFUSE_NO_SCENE` (ค่าคงที่เดิม `mob_drop_presence.
   REFUSE_NO_SCENE`) **และ** caller ส่ง `scene=` มาจริง (ไม่ใช่ `None`) — พิมพ์
   `GROUND_REANNOUNCE_AFTER_SECOND_PWD scene=<n> items=0` แทน `_REFUSED`, คืน `()` เหมือนเดิม (ไม่มีของ
   จริง ๆ ให้ส่งอยู่ดี ไม่มีการประกอบไบต์ใหม่ ไม่มีเส้นทางเข้ารหัสที่สอง — ใช้ `sustain_a_kill` ตัวเดิมทั้งหมด)
   ถ้า caller **ไม่** ส่ง `scene=` (เหมือนที่ `runtime.py` ทำอยู่วันนี้) พฤติกรรมเดิม (REFUSED) ยังคงอยู่
   ทุกตัวอักษร — เลนนี้ไม่เดาฉากที่ cell ไม่เคยรู้จัก

ปรับ docstring `GROUND_REANNOUNCE_WIRING` (โค้ดตัวอย่างที่จะให้ chief วาง) ให้แนะนำส่ง `scene=` เป็นครั้งแรก
(เดิมมันเขียนอธิบายไว้ตรงข้ามว่าทำไมถึง "ไม่ต้อง" ส่ง — ซึ่งเป็นการอ่านที่พลาดเคส pre-first-kill ที่ R316
วัดเจอจริง) — เป็นการแก้ข้อความในไฟล์ของสาย B เอง ไม่ใช่การแก้ `runtime.py`

**เทสใหม่ 5 เคส** ใน `test_mob_drop_presence_ground_reannounce.py` (`NoSceneCellWithACallerSuppliedSceneTests`):
cell ไม่มีฉาก + caller ส่ง scene ⇒ `()` + พิมพ์ token ปกติ items=0 + ไม่พิมพ์ REFUSED · ไม่ส่ง scene ⇒
REFUSED เหมือนเดิม (regression guard) · cross-check ว่า `sustain_a_kill` เองยังคืน `REFUSE_NO_SCENE` จริง
(ไม่ hardcode สตริงซ้ำ) · ไม่มีการ take/mutate ใด ๆ เป็นผลข้างเคียง

**CORE-REQUEST**: `runtime.py`'s `CheckSecondPwdVital` block (บรรทัด ~10169) เรียก
`mob_drop_presence.reannounce_ground(getattr(self, "mob_loot_cell", None), legacy)` โดยไม่ส่ง `scene=` —
ขอให้เปลี่ยนเป็นส่ง
`scene=world_scene_folder.scene_folder_for_scene_id(self.foundation.selected.position.scene_id)` เป็น
อาร์กิวเมนต์ที่สาม เพื่อให้ REFUSE_NO_SCENE (ก่อนฆ่าตัวแรกของบูต) กลายเป็น `items=0` ที่ถูกต้องแทน REFUSED
บน console จริง (ตำแหน่งปัจจุบันของ scene_id อ่านจาก `self.foundation.selected.position.scene_id` ตามที่ใช้
ซ้ำหลายจุดในไฟล์เดียวกัน เช่นบรรทัด 5048/9937)

## 3. ข้อ 3(ง) — เฟรมลบเมื่อพื้นเหลือ 0 ชิ้นหลังหมดอายุ

**ไม่แก้โค้ด** — ยังไม่มีเฟรมลบเดี่ยวที่พิสูจน์แล้วจาก capture จริงให้เดินตาม และการยืดอายุเป็น ∞ ถูกห้ามไว้
ในใบ `1153` เอง (ผมปฏิเสธทางนี้เองด้วย ไม่รอคำตอบ — ดูจดหมาย)

**เปิดจดหมาย ASK-COO** (pf_bridge, กิ่ง `claude/eloquent-noether-ltuevf`):
`notes_to_chief/20260905_1216_LANE-B-ASK-COO-ground-item-delete-frame-when-floor-empties-to-zero.md`
(7152 ไบต์) — สรุป: กรณีนี้คือครึ่ง "ลบแถวสุดท้าย" ของ `RE-208` ที่ผมเองเคยปฏิเสธไว้ในรอบ `f4oh9y`
(`COO-DECISION 20260903_1942`/`20260903_2250`) โดยขอให้ "รอมีคนวัดบนจอก่อน" — **R316 คือการวัดนั้น**
ถามว่าพอเปิดใบ RE แคบได้หรือยัง เสนอสามทาง (คงพฤติกรรมเดิม [ทำอยู่ตอนนี้] / ประกอบ generation ศูนย์
อิลิเมนต์แล้ววัดจริง [ต้องมี RE ใหม่] / ยืดอายุ ∞ [ปฏิเสธเอง ไม่ทำ]) และระบุจุดเดียวที่ต้องแก้ถ้าคำตอบมา
(`mob_loot.py:3969` `frames_after_rows_expired`'s สาขา `if not view.drops: return owed, 0, ()`)

## 4. ข้อ 4 — GT-247 id↔ท่า จับคู่อ่านสดจาก `POSE_TRIAL sent=/hit=` แล้วหรือยัง

**คำตอบ (อ่านโค้ดจริง ไม่เดา): ยังไม่ยืนยัน — ยังเป็น `[เสนอ]` ตามที่ chief ลดชั้นไว้ใน R352 §7.3**

หลักฐานในโค้ด: `pose_trial.py`'s เอง comment เหนือ `ATTACK_BEHAVIOR_BY_EQUIP_TYPE`: *"Neither
`CONSTDATA_TH__EQUIP_VALUE.tsv` nor `CONSTDATA_TH__BEHAVIOR.tsv` is tracked here, so NO test in this
repository can catch a mistyped row -- pf-adversary measured exactly that (D3: changing 280 to 281 leaves
the suite green)."* และ `tests/test_pose_trial_production_hit_wiring.py`'s docstring เอง: *"NOT proven
here: whether a real client plays an attack animation for any of the six ids (GT-247, on a screen)."*
ไม่มีเทสไหนในเรพอผูกค่า id↔ท่ากับบรรทัด `POSE_TRIAL sent=<id> hit=<n>` ที่อ่านสดขณะสังเกตบนจอ — การจับคู่
เป็นตารางที่ transcribe มาจาก RE-110-RESULT ภายนอก ไม่ใช่ค่าที่ derive/ยืนยันซ้ำได้ในเรพอนี้ ตรงกับที่
chief สรุปไว้แล้วในหัวข้อ 7 ข้อ 3 ของ R352

## 5. ท่าโจมตี production จาก equip type — ยังทำไม่ได้รอบนี้, บล็อกสองชั้น

1. **id↔ท่า crosswalk = `[เสนอ]`** (ข้อ 4 ข้างบน) — ยังไม่ผ่านเกณฑ์ที่จะ hardcode ลง production ตามกฎ
   "ค่าที่ไม่ยืนยัน ห้ามลง production" ของใบ `1153` เอง
2. **`pose_trial.equip_type_of_performer()` คืน `None` เสมอ** (อ่านโค้ดแล้ว, มีคอมเมนต์ในตัวฟังก์ชันเองว่า
   นี่คือคำถาม RE ที่ยังเปิดอยู่ — ไม่มีคอลัมน์ equip type ที่รู้จักใน `migrations/` และไม่มีตัวอ่าน
   `EQUIP_VALUE` ในทรีนี้ ยังไม่รู้ว่าฟิลด์ `equip_projection_slot_0x…`/`n_SLOT_RHAND`/`n_SLOT_LHAND` ใน
   ตาราง AvatarAttr ตัวไหนคือ equip TYPE จริง) แม้มี provenance ก็ยังต้องแก้ signature ผ่าน
   `action_ack.make_scene007_action_ack` เพิ่ม (คนละงานจากแค่เติมตาราง)
3. ใบ LANE-CS (`0737`) ที่ให้ตรวจนั้นเป็นคนละกลไก — สูตรดาเมจจาก **skill id** (`_dispatch_mob_combat`
   damage), ไม่ใช่ pose จาก equip type ยังติด `RE-240 BOUNDED-NEGATIVE` เหมือนกัน (ไม่มีฟิลด์ skill id ใน
   `ActionVital` ที่อ่านได้วันนี้) เป็นคนละบล็อกจากข้อ 1-2 ข้างบน ไม่เกี่ยวกัน แค่ทั้งคู่รอ RE

⇒ ข้ามไปทำงานสำรอง

## 6. งานสำรองที่ตรวจ (M5 persistence) — ไม่มีช่องโหว่ในเขตสาย B ให้แก้รอบนี้

ตรวจ `mob_ground_persistence.py`/`mob_pickup_request.py` ตามที่ใบสั่งเสนอ: WorldGround (in-memory,
ข้ามการ relogin แบบไม่ปิดเซิร์ฟ) ใช้งานได้จริงแล้ว (`remember_generation` เรียกทุกครั้งที่ `sustain_a_kill`
รัน ไม่ว่าจะมี `world=`/`store=` ส่งมาหรือไม่ — ใช้ singleton `_WORLD` ภายในโมดูลเป็นค่าเริ่มต้น) **แต่**
สองครึ่งที่เหลือ (คงอยู่ข้าม **server restart** ผ่าน `ground_drops` table) ยังบล็อกที่ `runtime.py` ล้วน ๆ
ตามที่โมดูลเองบันทึกไว้แล้ว: `sustain_a_kill` เรียกจาก `runtime.py:5768` **ไม่ส่ง `store=`** (ยืนยันด้วย
grep แล้ว) และไม่มีที่ไหนเรียก `restore_scene_ground` เลย — ทั้งสองจุดเป็น call site ใน `runtime.py`
(เขตของ chief) ตามที่ `pf_bridge/notes_to_chief/20260904_1650`/`20260904_1652` ข้อ 3 ขอไว้แล้วก่อนรอบนี้
และยังไม่ถูกเดินสาย ⇒ **ไม่ใช่ช่องโหว่ในไฟล์ของสาย B** (โมดูลเองพูดตรงนี้ไว้แล้ว: "both are call sites in
runtime.py, this lane's file boundary, not a gap in this module") ไม่มีอะไรให้แก้ในเขตผมรอบนี้ ไม่ส่ง
CORE-REQUEST ซ้ำเพราะสองใบก่อนหน้ายังไม่ถูกปิดหรือถอน (ไม่ต้องการให้ chief เห็นเป็นคำขอใหม่)

## 7. ชุดเทส

ระหว่างทำงานรันเฉพาะไฟล์ที่แตะ + ไฟล์ adversary-review ตามที่ COO ระบุ (ดูข้อ 1/2 ข้างบน) — ทั้งหมดผ่าน
ก่อน merge main แล้วรันชุดเต็มครั้งเดียว: **ผลชุดเต็ม (pirate-force-server, หลัง merge `origin/main`
`fb7951c0`): 10844 passed, 323 skipped, 20165 subtests passed, 0 failed (452.09s)**

## 8. สิ่งที่ตัดสินเอง [LANE-B ASSUMPTION - รอ COO ยืนยัน]

- ข้อ 3(ข): เงื่อนไข "cell ไม่รู้ฉาก + caller บอกฉากมา ⇒ items=0" เป็นการตีความของผมว่าใบ `1153`
  ข้อ 3(ข) ต้องการแบบนี้ (ตรงกับตัวอย่างที่ใบให้ไว้เป๊ะ) — ไม่ใช่สมมติที่เสี่ยง แต่ไม่มีใครยืนยันบนจอ
  ว่า chief เดินสาย `scene=` ตามที่ผมขอแล้วภาพจะออกมาแบบนั้นจริง (รอ GT-242 รุ่นถัดไป/RECHECK)
- ข้อ 3(ง): ผมเลือกไม่แก้โค้ดและเปิดจดหมายแทน (ทางเลือก 1 = สถานะเดิม) — เป็นการตัดสินใจของผมเองตาม
  กติกาที่ให้ไว้ในใบเดิม ("ห้ามยืดอายุเป็น ∞") ไม่ใช่คำสั่งใหม่ของ COO รอบนี้โดยตรง

## 9. หนี้ที่ยกไปรอบหน้า
1. ท่าโจมตี production จาก equip type (ข้อ 5) — รอ RE สอง: id↔ท่า live-correlation + equip type provenance
2. สูตรดาเมจจาก skill id (LANE-CS) — รอ `GT-243` ให้ชื่อฟิลด์
3. ศพ/ตาย/เกิดใหม่ผ่าน API ของ LANE-A — รอ registry ขึ้น main (`1152`, กำหนด A ตก 15:21)
4. ข้อ 3(ง) — รอคำตอบ COO บนจดหมายที่เปิดรอบนี้
