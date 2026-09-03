# CODEX CHECKPOINT — ปลด static gate ของสีมอน/ของตก และยืนยัน GM gate

เวลา: 2026-09-01 11:35 +07:00  
สิทธิ์: อ่าน GameClient/DATA และอ่าน ServerProject เพื่อตรวจ integration drift เท่านั้น  
ขอบเขต: Claude ยังถือ active write lease; Codex **ไม่ได้แก้ ServerProject**, ไม่รัน tests/server/client, ไม่แตะ Git/workflow/queue/lease

## ทำอะไรไป

1. ปิด exact conditional same-actor chain ของสีมอนจาก RuntimeRes-created CNetNPC → manager registry → tick/selector receiverตัวเดิม → `actor+0x254` NPC controller → `LABEL_NAME`/style store
2. ตรวจ direct writer census ปัจจุบันใหม่ครบ 30 จุด: reachable 19 (shipped 18 + diagnostic conditional 1) / excluded 11
3. ปิดเส้น item drop `item_id -> n_DROPMODEL_TYPE -> token.nif -> loader/type filter -> wrapper+0x84` และผนวกลง `PF_GROUND_DROP_LIFETIME` เดิม ไม่สร้าง artifact แข่ง
4. ตรวจ GM artifact ซ้ำแบบ read-only: byte-for-byte reproducible และไม่ต้องสร้างรายงานซ้ำ
5. อัปเดตรายงาน canonical ที่ root เป็น checkpoint 11:35

## สถานะ Attr หลัก

- generation หลักยัง `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae`
- field/status/scope เปลี่ยนสถานะ **0 แถว**
- semantic `UNKNOWN 42`, scope `UNKNOWN 210`, unified unresolved `977` — **ไม่เปลี่ยน**
- รอบนี้เปลี่ยนเฉพาะ standalone active-priority artifacts สามเรื่อง

## สีมอนสเตอร์ — คำตัดสินใหม่

`PF_MONSTER_COLOR_GATE` ปัจจุบัน 53 แถว = IMAGE 45 / DATA 8

- `MCG-IMG-039..045` ปิด singleton manager join, factory→registry tuple, node `+0x18` actor pointer, registry tick receiver, selector receiverตัวเดิม, controller binding, `LABEL_NAME` และ style store
- `MCG-IMG-025..033` จึงกลับเป็น `PROVEN_EXACT` แบบ **conditional static path** 9 แถว
- death branch เรียก CNetNPC vslot `+0x3C -> 0x0043BD70` บน actorตัวเดิม แล้วเขียน style 63 ลง controllerของ actorนั้นแบบมีเงื่อนไข
- ไม่ได้พิสูจน์ว่า runtimeผ่านทุกครั้ง: ยังต้องผ่าน `+0x254/+0x258/+0x260`, distance/control flow, registry retention, binder success และผลพิกเซล
- scene-1 ChooseNPC writerใหม่ถูกนับใน total 30 แต่ excludedเพราะ `production_allowed=False`; reachableยัง 19 ไม่ใช่ 20

ไฟล์:

- `pf_bridge/external/PF_MONSTER_COLOR_GATE.tsv` — 79,162 B — SHA-256 `f99347e4a000945caf9e8da0cbe7887330f5de93e6e92f8fe8974611541209a5`
- `pf_bridge/external/PF_MONSTER_COLOR_GATE.md` — 25,369 B — SHA-256 `7b6626acbd94d3f1b59e723d7450324cf200c0eb0cd741fa0b999b27ff2aa80b`
- pair marker — 528 B — SHA-256 `c9e8ea76205b1c14c3d605e2b4637d252c0b98b86fa26f90534cf171e2e5f23f`
- re-deriver — 121,898 B — SHA-256 `9dcfa889ae8227657783ce4b9b52bbc653917e1c723e363e816df7f0117be465`

## Item drop — คำตัดสินใหม่

`PF_GROUND_DROP_LIFETIME` ปัจจุบัน 23 แถว = IMAGE 18 / DATA 2 / CAPTURE 3

IMAGE ปิดเส้น:

`TerrainThing+0x14 item_id -> DATA row -> n_DROPMODEL_TYPE -> direct 0..12 token -> .\Data\GC\F\<token>.nif -> resource open/type filter -> wrapper+0x84`

ตารางตรงคือ `0 item, 1 weapon, 2 armor, 3 fittings, 4 money, 5 buff, 6 pandora, 7 crystal_r, 8 crystal_b, 9 crystal_g, 10 DROP_ENERGY, 11 DROP_LIFE, 12 holloween01`

- type 0 ใช้ได้จริงและขอ `item.nif`; ไม่ใช่ no-model
- `+0x84 == NULL` ล้มก่อน XYZ/activation/nameboard
- non-null `+0x84` ผ่าน XYZ/activationก่อนสร้าง nameboard; labelจาก blockนี้พิสูจน์เพียงว่า pointerเคย non-null ไม่ใช่พิสูจน์ mesh pixels
- fall/tag FX อยู่คนละ refs (`+0x8C/+0x88`); FX/labelหายไม่เท่ากับ wrapper/modelถูกลบ
- current-scope DATA มี 43 items: table partitions `22:30 / 24:10 / 26:3`; type histogram `0:11,1:12,2:10,3:8,10:1,11:1`
- `2400046` = ITEM_CONSUMABLES 46, type 11 `DROP_LIFE`; `2400047` = ITEM_CONSUMABLES 47, type 10 `DROP_ENERGY`
- packageมี `.ni_` stemครบ 13 แต่ clientขอ `.nif`; resolver `.nif -> .ni_` ยังเปิด

ผลต่อ GT-045: การเห็น labelจาก exact blockนี้ขัดกับคำอธิบายว่า model-resource creationคืน NULL. สิ่งที่ยังเปิดคือ scene/resource object non-nullแต่ geometryไม่ปรากฏในมุมที่วัด หรือมี upstream visibility/lifecycle transition

รอบ attended/instrumentation ถัดไปควรเก็บพร้อมกัน: full item ID, DATA type/token/path, loader result, `wrapper+0x84`, label-node bit, live-map membership, pointer identityของ `drop_key` เดิมผ่าน PRESERVE heartbeat ≥2 และสถานะ pointerเมื่อ label/FXหาย

ไฟล์:

- `pf_bridge/external/PF_GROUND_DROP_LIFETIME.tsv` — 31,574 B — SHA-256 `90d63c81d34b442369aafeae83ea93dbd7580adcd410f9df7e6deb34daf5b24e`
- `pf_bridge/external/PF_GROUND_DROP_LIFETIME.md` — 12,046 B — SHA-256 `29abf2ee3036a1be651abae5db341ea7ee99a5b2e258fdcbd934ad7c6b147561`
- re-deriver — 85,050 B — SHA-256 `64f29b7fed96f29e487307d0948d017bfa7fdd8daa776e3746b4e8252b5b9c45`

## Conflict ที่กระทบการต่อสายจริง (ไม่เกิน 10 บรรทัด)

1. `tools/pf_mine_scene_drop_tables.py:43-44` เขียนว่า `n_DROPMODEL_TYPE` อธิบายการวาดไม่ได้; ที่ถูกคือเป็น direct generic-NIF selector แต่ valid/nonzeroยังไม่พอรับรอง visible geometry
2. `src/pirateforce_foundation/mob_loot.py:544+` ยังเขียนว่าไม่ใช่ switchและ roster 63; current ITEMSมี 43
3. `docs/FUNCTIONAL_COVERAGE.json:911` ยังเขียนว่าไม่มีหลักฐานว่า clientอ่าน element `+0x14`; IMAGEปิด exact reader/consumerแล้ว
4. ห้ามแก้ historical notesย้อนหลัง; ให้แก้เฉพาะ current docs/generated-sourceผ่าน workflowของ Claude
5. Color same-actor static blockerปิดแล้ว แต่ห้ามยกเป็น unconditional render; readiness/pixel gateยังเปิด
6. Ground labelไม่เท่ากับ mesh; ต้องวัด `+0x84`และ geometryแยกจาก label/FX
7. `.nif -> .ni_` resolverยังไม่พิสูจน์; อย่าเพิ่ม guessed wire model bytesหรือเดา `n_ID_MODEL`

Codexไม่ได้แก้ conflict เหล่านี้ใน ServerProject เพราะ Claudeถือ write lease

## GM button

ไม่สร้าง artifact ซ้ำ. `PF_GM_PLUGIN_GATE.tsv/.md` ยัง reproducible: 15 แถว = IMAGE 13 / DATA 2. Static contractปิด x86 `GameMaster.dll`, exact undecorated `CreateGameMaster`, slot `+0x00` (`this` + pointer args 2 ตัว, `ret 8`), slot `+0x04` (stable UTF-16 basename) และ MSVCR90 scalar-delete ownership

`L"GMUI_1"` ยังเป็น compatible DATA-composed proposal ไม่ใช่ original DLL return. ยังไม่มี DLL/source/project/build output; panel, `GMUI_BASIC`, clean shutdownยังต้อง runtime acceptance. Fallback vtableมี `+0x08` แต่ไม่มี direct caller proof จึงห้ามเรียก artifactนี้ว่า exhaustive original interface ABI

## รายงาน canonical

อัปเดตไฟล์เดิมเท่านั้น: `Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md` ที่ root. รายงานยัง `CHECKPOINT / PROVISIONAL`, เปิดให้ทีมอ่านแล้ว แต่ไม่ใช่คำสั่งให้ลงมือแก้ระบบเอง
