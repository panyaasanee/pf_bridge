# CODEX CHECKPOINT — P0-6 ground-drop pickup closure

เวลา checkpoint: 2026-09-01 22:42 +07:00  
สถานะรายงาน: `CHECKPOINT / PROVISIONAL`  
คำตัดสิน: `P0-6_BOUNDED_CLIENT_KEY_TRANSPORT_CLOSED / ORIGINAL_PICKUP_REMOVAL_POLICY_OPEN`

## ผลที่ปิดได้

`PF_GROUND_DROP_PICKUP_CLOSURE` มี 15 แถวและแยก sourceต่อแถวชัดเจน: IMAGE 8 / CAPTURE 7; ไม่มีแถวผสมชั้นหลักฐานและไม่มี raw proprietary payloadถูกเขียนออกมา.

**[ORIGINAL EVIDENCE: IMAGE]** ปิด bounded client path ต่อไปนี้:

- typed `DropThingGameObj` gateก่อนสร้างคำขอ pickup;
- reconciliation key บน reached success path: `PickupTerrainThing+0x14 == TerrainThing+0x10`;
- logical discriminators `0x4543` nested, `0x6E6F` gameplay outer และ `0x453A` login outer; ไม่ยกค่าเหล่านี้เป็น top-level wire opcode;
- serialize → buffer rewrite → chunk ไม่เกิน `0x3FF8` → `WS2_32!send`;
- ไม่พบ direct local unregister/map eraseภายใน successful pickup-emission subspanที่ตรวจ. ข้อนี้เป็น bounded negative ไม่ใช่ whole-program absence.

## Capture census และเพดานคำตอบ

**[CAPTURE EVIDENCE]** corpusปัจจุบันมี 2,227 ไฟล์ / 699,015,496 ไบต์; manifest `b8284a566d9993f52540dea52e82896b0d8eb499b9aa83ceb74084a0e671db3c`.

- RuntimeRes R 15,288: bit08 absent 14,536; present/count-zero 0; present/nonempty 23; unresolved 729; truncated-derived-mask 3.
- C2S outer 65,610 = gameplay 64,979 + login 631.
- nested declared 15,350; exactly reached 14,615; fail-closed 735; `PickupTerrainThing` reached 0/14,615.
- 23 nonempty framesเป็น `PATH_CLASSIFIED_CAPTURE_V_PREFIX` ตามชื่อ pathเท่านั้น. ไม่มี authoritative server-provenance ledger จึงห้ามเรียกว่า originalหรือ replacement traffic.
- `0/14,615` ไม่ใช่ global absence: ยังมี 735 nested membersที่ fail closed และไม่มี original-qualified exchange.

**[CAPTURE EVIDENCE — parser coverage correction]** `PF_FIELD_VALIDATION` เดิม returnก่อน derived tailเมื่อ outer bit02 absent จึงไม่เห็น terrain-pool tailที่ artifactนี้ recoverได้ 23 เฟรมและยังเหลือ unresolved 729. นี่เป็น blind spotของ parserเดิม ไม่ใช่เหตุให้แก้ static field tableให้เข้ากับ capture.

## สิ่งที่ยังเปิด

- original accepted-pickup exchange;
- post-pickup omission/full-clear/remove carrierและ ordering;
- last-item all-clear;
- expiry duration/policy;
- authoritative original/replacement capture provenance;
- final socket literal mappingหลัง buffer rewrite;
- RuntimeRes tail 729 และ C2S nested 735 ที่ fail closed;
- shared scene ownershipและ production removal publisher.

`FightingDrop*` เป็น false leadเฉพาะ concrete typed carrierนี้ ไม่ใช่ global-unused claim. Count-zeroยังเป็น PRESERVE ไม่ใช่ CLEAR; ห้ามเดา removalจากค่า 0หรือจากชื่อ path.

## Integrity / adversarial review

- generation `82d3d4dc351e4c94314c40dafa664ece2619621b3f03a507a67bce045d2b145f`;
- claim set `0b24e08a365928d38d37c98063bbea2d2ce44c00e8096bb024e745ad0adcc13f`;
- `--check` PASS; `--self-test` PASS; fail-closed mutations 27;
- full-row structural templatesครอบคลุม CAPTURE rowsทุกคอลัมน์; adversarial mutate 238 ช่องและ accepted 0;
- แก้ provenance guardสามรอบ: ถอน path-derived REPLACEMENT/ORIGINAL claims, เปลี่ยน denylistเป็น structural templates และขยาย templateให้ครบทุก published CAPTURE column.

## Artifact pins

- `pf_rederive_ground_drop_pickup_closure.py` — 124,485 B — `f3eb92393fbaec884e596acc5cbafba02738328c1af39d875e0aca0beb310d9d`
- `PF_GROUND_DROP_PICKUP_CLOSURE.tsv` — 30,672 B — `1cf955edcff6f360735488c8a6e03a91435f1041ba642092f9193fd295348a1c`
- `PF_GROUND_DROP_PICKUP_CLOSURE.md` — 14,761 B — `52981a6ad0c505f5d62d2430d54f41e074ae43b26fbfe3b6521ed1d2dae39b8f`
- `PF_GROUND_DROP_PICKUP_CLOSURE.pair.json` — 4,074 B — `a2bdbcd29e5df9f3a2e37aefa68f41b0a7af2642be403c7471464163d1ec9f3e`

Externalทั้งสี่ไฟล์ตรง byte-for-byteกับ tracked mirrorใต้ `pf_bridge/notes_to_chief/reference_codex_attr` ที่ commit `621a7d7f56833db9f5d8f069d806cc3a4df09acd`. P0-5 mirrorถูก trackแล้วที่ commit `26bef6f9b45e514e9d4f600291477f40d423c697`; ข้อความเก่าที่เรียก P0-5 ว่า untrackedถูก supersede.

## Current ServerProject read-only audit

**[RECONSTRUCTED POLICY; ไม่ใช่ original-server evidence]** inspected clean HEAD `89632cb386f3b1d875e89b3465ed1def023eec32` เวลา 22:51 +07:00. หลัง checkpointเดิม `mob_loot.py` และ `mob_drop_presence.py` เปลี่ยนเพื่อ live-wire derived mask-`0x16` `n_DROPMODEL_TYPE` candidateและแก้ wide-frame trim cap. การเปลี่ยนนี้ไม่เพิ่ม scene term/reset, ไม่หยุด whole-live-ledger republish และไม่ต่อ production pickup/removal; urgent findingsเดิมจึงยังไม่ปิด. `runtime.py`, `mob_death.py`, `mob_scene_recompose.py`, `mob_pickup.py` และ frozen V141 blobไม่เปลี่ยน. Codexไม่ได้แก้ ServerProjectหรือรัน tests/server/client.

Machine-readable authority: `PF_CRITICAL_ARTIFACT_AUTHORITY.json` — 26,948 B — `5b5ae26626cf2534e6d432ae1c7443dfda061fad204a657fc07685909f6a79d5`.

Canonical report: `Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md` — 186,075 B — `79526d748fb7c0ee894a87c7ff0df0f2bfbfac0a40105575059989c354f00119` ณการอัปเดตก่อนสร้าง noteนี้. Pre-overwrite snapshot: `audit_history/Pirate_Force_Codex_Audit_Recommendations.b96e420c2902_20260901_2220.byka1B.md` — 178,171 B — `6d28c79ff5c58c6e74874ff72aaacff602e800d3325a82344a2d1b46460ef1bc`.

## Attr / next lane

Main Attr generationยัง `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae`; semantic UNKNOWN 42/490 และ scope UNKNOWN 210 ไม่เปลี่ยน เพราะ P0-6เป็น standalone delta ไม่ใช่ field-table rewrite.

Active Codex static laneย้ายไป P0-7 ตามลำดับ:

1. `f_SCALE +0x0C`: manager-identity-sensitive IMAGE censusจาก MOBS singleton `0x0040B560`, lookup `0x004A1C70`, CNetNPC MOBS pointer `+0x35C`; แยก false joinของ mapอีกตัวที่ `0x004A1E90`.
2. authored density: reuse DATA scene census 289 `.npc` files / 6,248 placements / 6,230 lexical Mob/Monster rows; อ้างได้เฉพาะ authored placement groups ไม่ใช่ live original density.
3. outfit/action/idle: ตาม MOBS `s_OUTFIT +0x108` ไป Avatar registry/active selection. ห้ามใช้ MOBS `+0x1C` (`s_PROPERTIES`), SceneFog `Action/@Actived` หรือ DIE=sleepเป็นทางลัด.

ทุก real P0-7 checkpointต้อง recompute comparator V2ทั้งสี่; no-change streakปัจจุบัน 0.
