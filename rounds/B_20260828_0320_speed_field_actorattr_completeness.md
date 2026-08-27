[LANE-B (COMBAT) · round `gi7bxs` · 2026-08-28T03:20+07:00]

# ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
**ไม่มีอะไรบนจอวันนี้** -- นี่คือการปรับ byte ของ wire (BasicAttr movement-speed field) ที่พิสูจน์ผล
บนจอไม่ได้จนกว่าจะมี attended session ดูมอนสเตอร์เดินจริง การเดินของมอนสเตอร์ควรเหมือนเดิมทุกประการ
เพราะค่าที่ส่งตรงกับที่ client คำนวณเองจากตาราง MOBS อยู่แล้ว (ทุกแถวที่ขุดมาจนถึงตอนนี้เป็น 100)

# 0 ล็อกรอบ (ADDENDUM v2 ข้อ A)
`search_pull_requests is:open in:title [LANE-B]` = 0 ผลทั้งสอง repo ก่อนเริ่มรอบ. PR ล่าสุดของสาย B
คือ `pirate-force-server#159`/`pf_bridge#255` (รอบ `135mqs`/`y1fqrc`) -- ตรวจด้วย `pull_request_read`
เห็น `merged=true` ทั้งคู่บน `main` แล้ว -- งานรอบก่อนอยู่บน main ไม่ต้องกู้อะไรตามข้อ A

# 1 กล่องจดหมาย (ADDENDUM v2 ข้อ B)
กวาด `notes_to_chief/*.md` หาใบที่ addressed ถึง LANE-B และไม่มี `.CONSUMED.txt` คู่กัน (fallback เช็ค
ทั้งรูปแบบเก่า `.CONSUMED.txt` ตัด `.md` และรูปแบบใหม่เต็ม ตาม `COO-DECISION 0043`) พบใบสำคัญที่สุด:

- `20260828_0125_PANYA-DECISION-boot-character-must-be-complete-...md` (ถึงทุกสาย A/B/GM/RE) --
  ตาราง 22/55-field "สมประกอบ" ของ ActorAttr, และหลักการ "actor ทุกชนิดต้องส่ง attr ครบสมบูรณ์ที่สุด
  ไม่ใช่ขั้นต่ำที่พอไม่พัง" -- **บริโภคแล้วรอบนี้โดยตรง**: นำตาราง ③ มาใช้เป็นแนวทางประกอบ ActorAttr ของ
  field mob (ดูข้อ 2 ด้านล่าง) ตาม `COO-DECISION 2026-08-28T01:46+07:00`'s คำสั่งชัดเจนว่าสาย B/GM ไม่ต้อง
  รอ CORE-REQUEST ใหม่
- `20260828_0146_COO-DECISION-boot-character-actorattr-core-request-022-to-chief.md` (cc สาย A/B/GM) --
  เปิด CORE-REQUEST-022 ให้ chief แก้จุด login/StartGame ของผู้เล่น (ไม่ใช่ของสาย B) แต่ย้ำว่าสาย B/GM
  ใช้ตารางเดียวกันในเขตของตัวเองได้เลย -- ข้อความนี้คือสิ่งที่รอบนี้ทำจริง
- `20260828_0200_PANYA-DECISION-new-direction-...md` (ถึงทุกสาย) -- Attr completeness เป็นลำดับ 1 ของ
  ทุกสาย, GO! probe (ยกเลิกแล้วโดย ADDENDUM 02:35 ของใบเดียวกัน) -- มี `.CONSUMED.txt` ของอีกสาย (chief)
  อยู่แล้วที่ path นี้ (เนื้อหาเฉพาะของ chief); ไม่เขียนทับ เพราะกฎ ADDENDUM v2 ข้อ B ให้สิทธิ์แก้เฉพาะหัวใบ
  ที่สายตัวเองเปิด/เป็น addressee หลัก ไม่ใช่ overwrite ของสายอื่น -- รอบนี้บริโภคในทางปฏิบัติผ่านการนำ
  "Attr completeness เป็นแกนงาน" มาใช้จริงในโค้ด (ข้อ 2) แทน

**บริโภคแล้ว**: วาง `.CONSUMED.txt` ของใบ `0125` (ใหม่, สาย B) พร้อมสำเนาไป `consumed/`

# 2 ของที่เขียนจริงรอบนี้ (pirate-force-server, PR #167)
`COO-DECISION 2026-08-28T01:46+07:00` สั่งสาย B ให้ใช้ตาราง ③ ของ `PANYA-DECISION 01:25` เป็นแนวทาง
"ครบสมบูรณ์ที่สุด" เมื่อประกอบ ActorAttr ของ NPC/มอน -- ไม่ต้องรอ CORE-REQUEST ใหม่ ตรวจทุกช่องในตาราง
(55/22 ช่อง) เทียบกับ `legacy.make_npc_attr` (ตัวประกอบ NPCAttr จริง) แล้วพบว่า:

- **ช่องเดียวที่ทำได้จริงโดยไม่ประดิษฐ์ byte ใหม่: movement speed (x7, BasicAttr bit `0x0040`, f32 @
  `+0x54`).** `legacy.make_npc_attr` มี parameter นี้อยู่แล้ว พร้อม static RE chain ของตัวเอง (`0x45C103`
  อ่าน MOBS `n_SPEED_WALK`, `0x464960` setter, `0x45D2EA`/`0x484580` consumer) จากก่อนรอบนี้ -- ไม่เกี่ยวกับ
  probe ของเจ้าของเลย และ `mob.speed_walk` เป็นข้อมูลขุดจริงจาก MOBS (ทุกแถวที่ขุดแล้วในทั้ง bg0001/Bg0002
  เป็น 100 เสมอ ไม่ใช่ค่าเดา) -- ต่อสายเข้า `field_mobs.hostile_npc_attr`, `mob_death._compose_body`
  (และ `_timer_offset`'s offset math), `mob_diag_multi_object.alive_entry`'s D3 path ครบทั้งสามจุดที่ประกอบ
  NPCAttr ของมอนในโปรเจกต์นี้
- **ช่องอื่นทั้งหมด (~30 ช่อง) ไม่ทำ**: guild/EXP/เงิน/CP/นามแฝง เป็นแนวคิดผู้เล่นล้วน ไม่มีความหมายกับมอน ·
  class id/ฉายา/อาชีพรอง/SP/STR-CON-DEX-INT-PER (ทั้งบล็อก "Actor" b0-b41 ที่ตารางอ้างถึง) ไม่มีบิตใดเลย
  ใน NPCAttr ของโปรเจกต์นี้ · level (มีข้อมูลขุดแล้ว `mob.level`) และ MP cur/max ไม่มีบิตใน NPCAttr เช่นกัน
  **และไม่มี static RE chain พิสูจน์ว่าบิตเหล่านั้นมีอยู่จริงสำหรับ NPCAttr โดยเฉพาะ** -- มีแค่ probe ของ
  เจ้าของบน PC ActorAttr ซึ่งเป็น actor คนละชนิด การประดิษฐ์ splice จากตารางนั้นจะขัดกฎหลักฐานสองชั้น
  ของโปรเจกต์ -> **เปิด `RE-117`** (CLIENT_RE_QUEUE.md) ถามว่าบิต level/MP มีอยู่จริงสำหรับ NPCAttr หรือไม่

pf-adversary (เรียกจริงรอบนี้) ตรวจสอบอิสระ: `make_npc_attr`'s `movement_speed` มีอยู่ก่อนรอบนี้จริง
(ไม่ใช่โค้ดใหม่ที่แปะป้ายว่าเก่า) · `mob.speed_walk` ไม่มี silent fallback · ลำดับ ascending-mask-bit และ
offset ถูกต้อง (คำนวณด้วยมือ + รันจริง) · SHA256/byte-count ที่ pin ไว้คำนวณสดจาก byte จริง ไม่ใช่เลข
พิมพ์มือ · รันชุดเทสเต็มจาก `git stash` baseline อิสระ = 0 regression · พบจุดหนึ่ง (test ครอบคลุมแค่
bg0001 ทั้งที่ docstring อ้างว่า "ทั้งสองฉาก") -- **แก้แล้วในรอบนี้**: `tests/test_field_mobs.py` วน
loop ทั้ง bg0001 และ Bg0002 อย่างชัดเจน

# 3 pf-adversary
เรียกจริง (agent `pf-adversary`) -- ผลสรุปในข้อ 2 ด้านบน ไม่มี defect ที่ยังไม่แก้เหลืออยู่

# 4 หลักฐานสองชั้น
| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | `legacy.make_npc_attr`'s `movement_speed` parameter (RE เดิม 0x45C103/0x464960/0x45D2EA/0x484580) + `mob.speed_walk` มาจาก MOBS table ที่ขุดแล้ว (source digest ปักหมุดใน `field_mob_tables*.py`) |
| **client-observable** | ยังไม่มี -- ต้องรอ attended session ดูมอนสเตอร์เดินจริงในสนาม (ควรเหมือนเดิมทุกประการเพราะ 100 เป็นค่าเดิมที่ client คำนวณเองอยู่แล้ว) |

# 5 CORE-REQUEST
none -- COO-DECISION 2026-08-28T01:46+07:00 บอกชัดว่าสาย B ทำในเขตตัวเองได้เลย ไม่ต้องเปิดใบใหม่

# 6 เปิดใบให้สาย C
`RE-117` NPCATTR-LEVEL-MP-BIT-001 (CLIENT_RE_QUEUE.md) -- level (BasicAttr bit `0x0002`) และ MP cur/max
มีบิตจริงสำหรับ NPCAttr (ต่างจาก PC ActorAttr ที่ตารางเจ้าของพิสูจน์) หรือไม่ ที่ VA ไหน

# 7 เขตเขียนรอบนี้
`pirate-force-server` (PR #167): `src/pirateforce_foundation/field_mobs.py`, `mob_death.py`,
`mob_diag_multi_object.py` (ทั้งสามไฟล์เป็นโมดูลของสาย B เอง) · `tests/test_field_mobs.py`,
`test_mob_combat.py`, `test_mob_death.py`, `test_mob_diag_multi_object.py`, `test_npc_gait_wire.py`,
`test_world_census_wiring.py` · `scenarios/combat_death_001.json`, `combat_first_hit_001.json`,
`field_mobs_hostile_001.json` (pin re-derived จาก running code)
`pf_bridge`: ไฟล์นี้ (ใหม่), `CLIENT_RE_QUEUE.md` (เพิ่ม RE-117), `.CONSUMED.txt` ของใบ `0125` (ใหม่),
`notes_to_chief/consumed/20260828_0125_...md` (สำเนา), จดหมายสถานะ (ใหม่)
ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/`scenarios/world_*.json`

# 8 ถ้าผิดต้องย้อนอะไรบ้าง
`git revert` commit เดียวใน `pirate-force-server` (12 ไฟล์ อยู่ใน write zone ของสาย B ทั้งหมด ไม่มี
side effect นอกไฟล์เหล่านี้) -- ไม่มี schema/DB change, ไม่มี wire format ใหม่ (เป็น parameter ที่มีอยู่
แล้วในซีเรียลไลเซอร์เดิม) ย้อนได้ปลอดภัย 100%

-- **สาย B · COMBAT**
