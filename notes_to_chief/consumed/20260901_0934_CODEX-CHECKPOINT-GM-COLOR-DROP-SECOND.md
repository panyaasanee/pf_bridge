# CODEX CHECKPOINT — GM / MONSTER COLOR / GROUND DROP (SECOND)

ผู้รับ: Chief / COO / LANE-GM / LANE-B / attended-test owner  
ผู้ส่ง: OpenAI Codex  
เวลา: 2026-09-01 09:34 +07:00  
สถานะ: CHECKPOINT / PROVISIONAL / TEAM-READABLE

## สรุปสิ่งที่เพิ่มจาก checkpoint ก่อน

1. **Monster color:** ปิด current Foundation actor-type-4 direct-writer census แบบ fail-closed ได้ 29 definitions: เข้าถึงได้โดยไม่ใช้ scenario flag 19 จุด (18 default + 1 operator-conditional diagnostic; ไม่ active พร้อมกัน) และ excluded 10 จุด. ทุกจุดที่เข้าถึงได้ยังใช้ positive identity และยังไม่มี Foundation-owned seam ที่บังคับ identity เดียวกันทั้ง inbound/outbound lifecycle.
2. **GM button:** เพิ่ม implementation contract จาก IMAGE ให้ครบ exact undecorated export `CreateGameMaster`, x86 vtable slot `+0x00/+0x04`, calling convention/stack cleanup และ MSVCR90 scalar-delete allocator compatibility. `L"GMUI_1"` ยังเป็น PROPOSED compatible binding ไม่ใช่ original DLL return.
3. **Ground drop:** ตรวจ current code พบ heartbeat PRESERVE patch merged แล้ว แต่ยังไม่มี client-observed proof. `GT-188` ต้องแยก `model/object visible` ออกจาก `label visible`, ตาม object เดียวกัน และต้องมี PRESERVE heartbeat อย่างน้อยสองครั้งใน exact A→C interval.
4. **Attr:** main generation `b96e420c…` ไม่เปลี่ยน; field rows/status/scope/UNKNOWN เปลี่ยน **0 แถว** (`semantic UNKNOWN 42/490`, `scope UNKNOWN 210`).

## Top conflicts / จุดที่ทีมควรพิจารณา

1. Color identity ต้องเป็น bidirectional mapping: inbound `resolve_wire(W)->P` และทุก outbound actor/CHitResult/bar/death/recompose/drop/pickup reference ต้องใช้ `project_wire(P)->W`; เปลี่ยนเฉพาะ spawn จะ split identity.
2. Mapping ควรเป็น session+scene+generation-scoped bijection, collision-check กับ outgoing census ทั้งหมด และ invalidate เมื่อ scene/generation เปลี่ยน.
3. Orange→red→gray ยังเป็น staged hypothesis เพราะ IMAGE gates อื่นยังเปิด. STEP-A ไม่ส้มก่อนโจมตี = stop; matched-W CHitResult ไม่แดง = stop; gray ต้องตาม matched-W corpse + HP=0/timer<=0.
4. GM implementation ต้องมี slot `+0x00` ด้วย ไม่ใช่แค่ slotชื่อ `+0x04`; export decoration หรือ stack cleanup ผิดอาจ crash.
5. GM object ต้อง allocate ด้วย runtime ที่ compatible กับ MSVCR90 scalar delete; ห้ามคืน static/global interface objectและห้ามสมมติ modern UCRT heapว่าเข้ากัน.
6. `GT-188` false-green ได้หากป้ายค้างแต่ item modelไม่เคยวาด; STEP-A model/objectต้องเป็น precondition มิฉะนั้น NO-RESULT.
7. Long-term ground-drop lifecycle ยังขาด scene id, scene/connection clear, authoritative expiry, pickup/persistence order และ shared ownership; immediate PRESERVE patchไม่ได้ปิดประเด็นเหล่านี้.
8. Bg0002 ตัวเลข 17→12 เป็น production-configured source projection ไม่ใช่ live/player-observed roster; ห้ามยกเป็น runtime fact.

## ข้อพิจารณาสำหรับทีม (ไม่ใช่คำสั่งแก้)

- LANE-GM อาจใช้ ABI/allocator checklist ใน `PF_GM_PLUGIN_GATE.md` เป็น pre-build gate แล้วให้ attended testตัดสิน panel → `GMUI_BASIC` tab → clean shutdown.
- LANE-B อาจเลือก seam กลางเดียวสำหรับ identity projection; `AnnouncedActorMembership` เป็น existing candidate seam แต่ต้องผูก actual census generation/invalidation ก่อนใช้เป็น authority.
- attended-test owner ควรเพิ่มการสังเกต modelกับ labelแยกกันใน `GT-188`; หาก STEP-A ไม่มี model ให้บันทึก NO-RESULTแทน pass/failของ persistence.

## Artifact identity

- Canonical report: `C:\Users\Panya\Desktop\Pirate Force\Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md` — 124,585 B — SHA-256 `a016178cecf6383955e22f7a28605212f3acb9c2b38ab9142bffe6d690dacc70`
- GM TSV: 17,569 B — `790cb0f2e4f4dc9277226cb569ebaadca2e2eaf11ba59d87a8919e612f5cbffd`
- GM MD: 11,679 B — `d690640e512e5731b075d67f0334a0541816ec4450781337a19426f7d592537e`
- GM re-deriver: 55,442 B — `d634a21fa5d3ed80415392c59b9edb96b6220619b2d2668ae9d59b75f94b3cd1`
- Color TSV: 40,636 B — `c094f9f4ff6e39648ecffb2f0c8d8edf9b3338c94860afdd264f3c32d599552f`
- Color MD: 21,320 B — `210f740eb185116bdb217394bb3f11865d52922d14a9c5d487c99b88893e04c4`
- Color marker: 528 B — `f474d0958949b860bf38fabdcde6f65736d0f21317a6321db7b2810b9a3f7599`
- Color re-deriver: 101,216 B — `40d1ca22d10c2718e36c13a9bea6d5a25d3c5a96a4885e17a5be8c26230edff5`
- Drop TSV: 24,410 B — `abe383f09e67088180dd0a723a7ddbebe95dd0ee5638d18778f02c11b3ece600`
- Drop MD: 8,267 B — `1c22c50b7ed0e13d555225cd8dca87c0f9414ebdaefd329a932a9a11a2f167c8`
- Drop re-deriver: 63,321 B — `04cce5cb44670f76a12de78af608bd53ec52ed166266470e7d7b45ef8bed9761`

## Duplicate guard / provenance

Checkpoint นี้ไม่แทนที่และไม่คัดซ้ำเนื้อหาเต็มของ:

- `20260901_0344_CODEX-CORRECTION-GM-EVIDENCE-BOUNDARY.md`
- `CODEX_URGENT_20260901_0407_DROP-EVIDENCE-CORRECTION.md`
- `CODEX_URGENT_20260901_0419_MONSTER-COLOR-IDENTITY-GATE.md`

เพิ่มเฉพาะ exhaustive writer census, bidirectional mapping contract, GM allocator/slot0 guard และ `GT-188` false-green guard.

Codex อ่าน ServerProject แบบ read-onlyเพื่อ audit reconstructionตามสิทธิ์ แต่ไม่ได้แก้ ServerProject, รัน tests/server/client, แตะ Git/workflow/queue/lease หรือแก้ frozen V141. `GameClient.local.bin` ก่อน–หลังยัง size 14,759,424 และ SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`. ไม่มี proprietary raw byteถูกคัดลง artifact.
