# CODEX CHECKPOINT — P0-4 ROLE DECISION (SECOND NO-DELTA)

เวลา: 2026-09-01 20:02 +07:00

สถานะ: `CHECKPOINT / PROVISIONAL`  
รายงานเปิดให้ทีมอ่านแล้วตามคำสั่งเจ้าของ แต่เอกสารนี้ไม่ใช่คำสั่งแก้ ServerProject

## 1. ผลรอบนี้

- เพิ่ม `PF_ACTOR_RELATION_INTERACTION_GRAPH` 42 แถว ทุกแถว `source=IMAGE`
- เพิ่ม `PF_MONSTER_ROLE_DATA_CONTROLS` 21 แถว ทุกแถว `source=DATA`
- ไม่คัดลอกแถวเดิมจาก main Attr generationมานับใหม่ และไม่ผสม IMAGE/DATAในแถวเดียว
- IMAGE graphแบ่ง 31 direct E8 callsitesเป็น talk/interact 4, target presentation 3, enemy target/state 10, color/style 3 และ unresolved 11
- คำตัดสินของ artifact: `BOUNDED_STATIC_GRAPH / ORIGINAL_POLICY_OPEN`

## 2. คำตอบ P0-4

1. ยังไม่พบ actor-factory caseหรือ fieldเดียวที่พิสูจน์ว่า objectเป็น monster, NPC หรือ training dummy. Clientใช้หลายแกนร่วมกัน: identity/role, interaction, relation/target, action, presentation, deathและ drop.
2. Client-local talk/interact pathแยกจาก enemy-target/action-related pathsได้ใน bounded graph แต่ universal attack admissionและ original-server assignment policyยัง `OPEN`.
3. MOBS ID 916 มี exact ASCII DATA label `Training Iron Man`. ข้อนี้แก้เฉพาะ blocker phraseเก่าที่ว่าไม่มี training label; ค่า rank/combat/offensive/aggro/usage/capability/dropและ nonclaimอื่นยังคงเดิม. Labelไม่พิสูจน์ runtime class, attackabilityหรือ damage behavior.

## 3. กฎกันจมและลำดับต่อไป

Main Attr generationยังเป็น `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae` และรอบนี้มี:

- field semantic-status change: 0
- field scope-status change: 0
- UNKNOWN change: 0

นี่เป็น P0-4 checkpointติดต่อกันครั้งที่สองที่ field/status/scopeไม่เปลี่ยน จึงใช้ GOAL_MASTER:

`P0-4_PAUSED_BY_ANTI_STALL / ORIGINAL_POLICY_OPEN`

Active static-RE laneถัดไปคือ P0-5 combat/death/animation. การตัดสินนี้ไม่เปลี่ยน owner implementation prioritiesของ Claude: GM button, monster name color และ ground-drop.

## 4. P0-5 delta shortlist

ไม่ rederive `PF_COMBAT_LIFECYCLE` 34 แถวเดิม. ไล่เฉพาะ:

1. `GSCN_RunTimeProtocolRes` actor-entry carrier
2. dying/dead predicate split
3. dead task/model-ready gate
4. `TargetIsDead` ไป actual target release
5. ActorAttr `+0x198` / NPCAttr `+0xA8` target-ID writersและ zeroing
6. target-panel HP/name refresh order
7. TerrainThingPool live-set/clear และ death-to-loot edge
8. CHitResult เทียบ HP arrival
9. `CFightMsgVital` lead
10. `PickupTerrainThing` post-loot boundary

ตัด `TargetVital` no-op, direct-negative `UpdateAttrVital`, character-select `DeleteActorVital`, EMPTY `DropThingModule_Client` และ name-only `FightingDrop*` ออกจาก deltaจนกว่าจะมีหลักฐานเพิ่ม.

## 5. หลักฐาน runtime ใหม่ — แยกชั้น

LOCK_GAME รอบ GT-192 ถูกปล่อยที่ 19:52. ผู้ทดสอบยืนยันว่า replacementส่ง level/HPต่างกันตาม actorและ clientแสดง HPตรงสาย แต่ทุก actorแสดง `LV 1`, ชื่อเขียวและ nameplateแบบ NPC. นี่เป็น `CLIENT-OBSERVED RESULT` ที่ช่วย localizeว่า recordถูก clientอ่านเพียงบางส่วน; ไม่ใช่ IMAGE/DATA factและยังไม่ระบุ fieldหรือ original-server policy.

## 6. Frozen artifacts

### IMAGE

- generator: `pf_rederive_actor_relation_interaction_graph.py` — 89,606 B — `8d1b5c1964a54c5849de001f715e877a86d3598d887adc18d0170dd87ad64d1e`
- TSV: 104,190 B — `0192050fab1df86346a8aac069a3f0f3fbe90620589879a89890461780e812ad`
- Markdown: 7,102 B — `47c3afea68093b329271323d750781c03808fff7178ab391c1c5834a89213ecd`
- pair: 556 B — `8fd30ceab78c865f973a98bfc63f4a9182627fd148208ac906174ff2f7476c48`
- generation: `b62f9c3a72e42177f4e2991fd91a1515e6e70450c610e338c1bf7c85c603a71f`

### DATA

- generator: `pf_rederive_monster_role_data_controls.py` — 78,358 B — `e878040fcc2317a9ae208de9cecd3e9df6f055421fc3eb6a901cabef5e8b7603`
- TSV: 45,536 B — `72a5e6ece07f8ca64f710617a8c95b976895be62fb1ddb5677f4ee6ee371348f`
- Markdown: 7,838 B — `c73e337235cc29d785c3ac7fa6f717490fc4d31663e54abedfaef6786d3c559e`
- pair: 739 B — `b27a8f8a74399c74fd21f313c7fa9940b78fef94103e91483e46e2924377233d`
- pair ID: `2f1e5b1e09032421f993999d7c2ed6d83d1c5d119f8ba75e77f814a403ddde5d`
- metrics: `d032c714a5eb9401744d6df02bccde34ad7705122e84b62f1115386413855435`

## 7. Top conflicts / blockers

1. Original-server role assignment/admission policyยังไม่มี original producerหรือ eligible S2C.
2. IMAGE graphมี unresolved direct callers 11 จุด; ไม่เดาชื่อจากบริบท.
3. ID916 lexical labelไม่พิสูจน์ attackability, autonomous AI, damageหรือ drop.
4. Talk pathแยกจาก attack-related pathได้ แต่ mixed-role admissionยังไม่ปิด.
5. Death-to-loot edgeและ actual target releaseเป็น P0-5/P0-6 blockers.

## 8. Integrity / delivery

- Root `--check` และ `--self-test` ผ่าน; frozen hashes/sizes/mtimesไม่เปลี่ยน.
- Adversarial audit re-derived pair generations, 42 IMAGE claim/evidence digests, 31 E8 targets, 45 prior-reference triplets, DATA usage cells 72 ช่องและ pins 95 จุด: PASS.
- IMAGEก่อน/หลัง: 14,759,424 B / SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- Working copiesใต้ `external/*` ถูก ignore/untracked แต่ทั้งแปดไฟล์มี byte-identical tracked mirrorใต้ `notes_to_chief/reference_codex_attr` ที่ pf_bridge commit `89c16e29ddca4502e81575a0aa86949cf80b5d79`.
- Authority: 15,708 B / `f3f1a8eddae03e9976c1926be69e034631bec0cd2912b56b39a452715f581f57`.
- Canonical report: 167,305 B / `ee6de975053e45ae4215ca38c34d7e9b05532ec844f40b637f3ebb67177d04bd`.
- รายงานก่อนแก้มี permanent byte-identical snapshotอยู่แล้ว: `audit_history/Pirate_Force_Codex_Audit_Recommendations.b96e420c2902_20260901_1124.byka1B.md` / `48948f235046d6dc509c6dc84588ed77025035eee01600420e2a56d4a62d4a44` จึงไม่สร้าง duplicate snapshot.
- ไม่แก้ ServerProject, ไม่รัน tests/server/client/GameClient/dump/capture, ไม่แตะ Git/workflow/queue/leaseหรือ frozen V141.
