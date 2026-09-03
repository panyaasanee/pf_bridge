[ถึง: chief · LANE-A · LANE-B · COO | จาก: Codex static RE | 2026-09-01T04:43:54+07:00]

# CHECKPOINT: GM / monster color / ground drop

## สถานะที่ต้องถือเป็น authoritative ตอนนี้

- ACTIVE 1: `GM_BUTTON`
- ACTIVE 2: `MONSTER_COLOR`
- ACTIVE 3: `GROUND_DROP`
- PAUSED: P0-7 presentation, P0-5 combat lifecycle และ backlog อื่น จนกว่าเจ้าของสั่งเปลี่ยนหรือสามเรื่อง active ได้ checkpoint
- Main Attr generation ยัง `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae`; field-status changes = **0**; semantic `UNKNOWN` ยัง **42/490 = 8.57%**; scope `UNKNOWN` ยัง **210**

## ผลที่ปิดได้

1. **GM:** DATA ยืนยัน `GMUI.project -> GMUI_1` และ `GMUI_1.model` มี root `GMUI_1`, child `GMUI_BASIC`; IMAGE ปิด bounded loader boundary. `GMUI_1` เป็น **PROPOSED compatible binding** ไม่ใช่ original DLL return. ต้องผ่าน runtime acceptance: button opens panel → intended tab reachable → clean shutdown
2. **Monster color:** IMAGE ปิด RuntimeRes actor-entry qword → actor type 4 → `CNetNPC` → signed identity gate → canonical selector; DATA ปิด palette 56–63. Positive identity ข้าม style 60/61/62/63 ทั้งกลุ่ม. Current five-file comparisonใช้ positive IDs แต่ไม่ใช่ producer censusครบและไม่ใช่ original policy; ห้ามเดา negative IDหรือแก้ V141
3. **Ground drop:** IMAGE ปิด RuntimeRes → TerrainThingPool → `DropThingModule_Client`: NULL clear; non-NULL count0 preserve; nonempty authoritative update/create/omission removal; มี range removal. CAPTURE ยืนยันเพียง `MOB_LOOT_DROP` log 3 ครั้ง ไม่เปิด payload/mask/delivery/decode/memory/screen. `FightingDrop` เป็น false leadเฉพาะ typed pathนี้

## Current-code conflicts เรียงตามผลกระทบ

1. **สูงมาก — color:** selected producers ใช้ positive identities จึงไป positive family; แก้แต่ `n_OFFESIVE`/bit ไม่พอ และเดา ID เสี่ยงชน registry/reference
2. **สูงมาก — drop:** ledger/kill compositionมีแล้ว แต่ expiry/pickup/remove ยังไม่มี total-order event publisherที่พิสูจน์; ordinary keepaliveควร non-NULL count0, full live setเฉพาะ state-change event; ห้าม second ledger/timer full-resend/V141 edit
3. **สูง — GM:** bindingยังไม่ผ่าน panel/tab/shutdown runtime acceptance; ห้ามยก `GMUI_BASIC` เป็น plugin identityโดยฟันธง

## Final standalone artifacts

- GM: `pf_bridge/external/pf_rederive_gm_plugin_gate.py` 54,640 B `c991e68db9a5105b0e9532688d702dcbf447215114a0774d7d35080b837c1100`; `PF_GM_PLUGIN_GATE.tsv` 17,569 B `790cb0f2e4f4dc9277226cb569ebaadca2e2eaf11ba59d87a8919e612f5cbffd`; `PF_GM_PLUGIN_GATE.md` 10,877 B `a3018a03778633ea1ee8e44038c9ecac93ff562f17453d57157da79468fe5d27`
- Color: `pf_bridge/external/pf_rederive_monster_color_gate.py` 79,217 B `bc76197ad4c382e9bf9d736d7f69063ef0b95d714ba94838c8f58109169ece70`; TSV 40,636 B `c094f9f4ff6e39648ecffb2f0c8d8edf9b3338c94860afdd264f3c32d599552f`; MD 12,770 B `99f59a2d84281690f6f2b04df68eeda7ab23df0183da0200ebaca2c0507abf4d`; pair marker 528 B `e960ba51784a16bb044c8d9c96511a1af2eaab3b23c5901ce5792bf318826deb`; independent adversarial `ACCEPT`
- Drop: `pf_bridge/external/pf_rederive_ground_drop_lifetime.py` 63,321 B `04cce5cb44670f76a12de78af608bd53ec52ed166266470e7d7b45ef8bed9761`; TSV 24,410 B `abe383f09e67088180dd0a723a7ddbebe95dd0ee5638d18778f02c11b3ece600`; MD 8,267 B `1c22c50b7ed0e13d555225cd8dca87c0f9414ebdaefd329a932a9a11a2f167c8`

ทั้งสาม checker publish/`--check` PASS; IMAGE ก่อน/หลังคง 14,759,424 B SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`. ทุก TSV rowมี source เดียว: GM IMAGE13/DATA2, color IMAGE38/DATA8, drop IMAGE17/CAPTURE3

## Canonical report และการส่งมอบ

- รายงาน: `C:\Users\Panya\Desktop\Pirate Force\Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md` — 121,484 B; SHA-256 `8170fa3a1cd42d62be8bb0deca9ac94000b255829026b59e6403754fc97f27ca`; independent report review `ACCEPT`
- pre-edit snapshot: `C:\Users\Panya\Desktop\Pirate Force\audit_history\Pirate_Force_Codex_Audit_Recommendations.b96e420c2902_20260901_0420.md` — 109,411 B; SHA-256 `a34bfc728c7f6c3e77bd2fb2667c692dcd4c3e1be748e16e74a96e545f5f9c97`
- รายงานคง `CHECKPOINT / PROVISIONAL` และ `RELEASED TO TEAM 2026-09-01 (เจ้าของเคาะ)`; ไม่ใช่คำสั่งแก้ระบบ
- External artifacts เป็น local-only/Git-ignored; Claude บนเครื่องเดียวกันอ่านได้ แต่ clone อื่นต้องรอ owner-approved packaging/ingest

ระหว่างรอบ Claude ผู้ถือ lease แก้ `runtime.py` เวลา 04:26. Checkers หยุด fail-closed; Codexวัดใหม่และ refreshเฉพาะ current-code pins จากนั้น re-check/re-reviewผ่าน. Codexไม่ได้แก้ ServerProject, Git, workflow, queue หรือ runtime และไม่ได้รัน GameClient/server
