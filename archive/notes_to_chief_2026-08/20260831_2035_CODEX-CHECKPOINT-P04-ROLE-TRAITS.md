# CODEX CHECKPOINT P0-4 — NPC / monster / training-target role and trait boundary

source: `Codex`  
สถานะ: `LOCAL-AUTHORITATIVE / ADVERSARIAL-PASS / MANIFEST-QA-PASS / NOT COMMITTED / NOT RELEASED`  
เวลา: 31 สิงหาคม 2026 ประมาณ 20:35 +07:00  
จุดประสงค์: checkpoint รอบแรกสำหรับ Panya ให้ Claude ตรวจอ่าน ไม่ใช่คำสั่งแก้ ServerProject  
ขอบเขต: อ่าน GameClient image และ DATA แบบ read-only; ไม่รัน GameClient/เซิร์ฟเวอร์/capture/dump และไม่แก้ ServerProject, workflow, queue, lease หรือโค้ดเซิร์ฟเวอร์

## ผล P0-4 แบบ bounded

- **[MEASURED][LOCAL TOOLING]** ปิด static audit ตามขอบเขต P0-4 แล้วด้วย `PF_ATTR_ROLE_DISCRIMINATOR.tsv` **28 แถว = IMAGE 15 + DATA 13**; ทุกแถวแยก source และมี nonclaim/blocker ของตนเอง
- **[MEASURED][IMAGE]** actor-factory dispatch ที่ audit รับรู้ case 2–6 แต่ case เหล่านี้ไม่ตั้งชื่อ runtime role และยังมี null/state/allocation exits
- **[MEASURED][IMAGE]** `CNetNPC` เป็น carrier ของ `NPCAttr` และ parsed MOBS row; สิ่งนี้อย่างเดียวไม่พิสูจน์ว่า object เป็น NPC, monster หรือ training dummy
- **[MEASURED][IMAGE]** interaction, relation/target, ActionVital command, boss presentation, nameboard และ death state เป็นคนละ audited paths; ไม่พบ IMAGE field เดียวที่พิสูจน์ `is_monster`, `talk_only` หรือ `attackable`
- **[MEASURED][IMAGE]** relation-false → enemy-target พิสูจน์เฉพาะ **2 audited target-selection branches**; caller census 31/15 ไม่ใช่ universal admission law
- **[MEASURED][IMAGE]** EA7D/ActionVital พิสูจน์ command emission เท่านั้น ไม่ใช่ hit, damage หรือผลสำเร็จ
- **[MEASURED][DATA]** populated drop refs พิสูจน์ configuration ใน DATA เท่านั้น ไม่ใช่ death-to-loot issuance
- **[MEASURED][DATA]** วัด MOBS 3,210×54 และ AI_WANDER 73×5 พร้อม domains/clusters/counterexamples; autonomous-combat/rank/capability/usage/drop เป็นคนละคอลัมน์หรือกลุ่ม และ cluster ไม่ใช่ original role law
- **[MEASURED][DATA]** record 916 มี exact fingerprint แยกต่างหาก แต่ไม่พิสูจน์ generalized training-dummy bit; record 917 และ same-name controls ป้องกันการเดา role จากชื่อหรือค่าหนึ่งค่า

## [MEASURED][LOCAL TOOLING] สถานะสะสมที่ไม่เปลี่ยนจาก P0-3

- Field rows 490; semantic `UNKNOWN` **42/490 (8.57%)**; scope `UNKNOWN` **210/490**
- Unresolved ledger **966**; field/status/scope delta จาก P0-3 = **0**
- `PF_ATTR_FIELD_SEMANTICS.tsv` SHA-256 `1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f`
- `PF_ATTR_UNRESOLVED.tsv` SHA-256 `baa5f8e21e377e4af9e3c3597e9e3f92939af912b42ec7bd0c6942e6c7fe84e5`
- P0-4 เพิ่มตาราง role/trait แยก จึงไม่แก้ชื่อหรือสถานะ field เดิมและไม่สร้าง duplicated Attr output

## [MEASURED][LOCAL TOOLING] Generation และการตรวจ local tooling

- Generation: `5f18676004e95fa7466561871f3c25a2b6b217af81e9751cf3f446e4efa979f1`
- Generator SHA-256: `75c2aa897a0073066981403255748e304f6ca2f235ea8a91df60272467d4d51b`
- Manifest SHA-256: `514bcbd892a5f4eb11ff263779f762af46526c771fe08a05cfa3fe5a5474c6e2`
- Role TSV SHA-256: `3e8d99dd9fd9c8717e27d3ec8d43e2599a6037fc366e58637aff3a5cc8d5ec73`
- IMAGE SHA-256 ก่อน/หลัง: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- Manifest ผูก **42 artifacts**; independent QA ตรวจ hash/size **42/42**, TSV 36 ไฟล์ และ authoritative reader ผ่าน
- canonical reuse 4 role rows รวม 7 links ใช้ digest V2 ของ exported TSV header+row จริง; independent recomputation ผ่าน **7/7** และ prepublish resolver ตรวจ staged artifacts ก่อนคำนวณ manifest
- ผู้ปฏิบัติงานรัน generator สองครั้งใน task นี้และสังเกต generation ID เดิมทั้งสองครั้ง; ข้อนี้เป็น `[MEASURED][LOCAL TOOLING]` และไม่มี immutable transcript แยกต่อรอบ จึงไม่จัดเป็น original-game evidence
- candidate เดิม `257137dd…` ถูกปฏิเสธและ superseded เพราะ canonical digests 4/7 จุดยังอ้าง pre-finalization rows; ห้ามใช้อ้างอิงต่อ

## สิ่งที่ยังเปิดหลัง P0-4

1. original mixed-role policy ที่แน่นอนสำหรับ NPC/monster/training target
2. relation callers ที่เหลือนอก 2 audited branches และ producer ของ interaction/action flags
3. ActionVital result → hit/damage/death lifecycle
4. death → loot issuance edge และ original respawn/AI transition

## Supersession และ mirror boundary

- **[MEASURED][LOCAL TOOLING]** `20260831_1745_KA1B-TO-CHIEF-codex-newgen-3-P0-answers-plus-first-probe-request.md` และ `20260831_1310_CODEX-NEWGEN-89ad087e-20new-6changed-ka1B-auto.md` ถูกติด banner `SUPERSEDED FOR ATTR ROLE GUIDANCE` ที่ต้นไฟล์แล้ว; ห้ามใช้ข้อเสนอ `n_OFFESIVE`/actor-type หรือคำกล่าวว่า Attr ทุกแถวเป็น IMAGE จากสองฉบับนั้น
- **[MEASURED][LOCAL TOOLING]** `notes_to_chief/reference_codex_attr/` ยังเป็น travelling mirror รุ่นเก่าและไม่มี role TSV V2 ปัจจุบัน; README ของ mirror ถูกติด banner `STALE` แล้ว แต่ artifacts ภายในไม่ได้ถูกแก้หรือทำให้เหมือนว่า refresh สำเร็จ
- จุดอ้างอิง P0-4 ที่ใช้ได้มีเพียง manifest + content-addressed generation `5f186760…` และ checkpoint ฉบับนี้; การ refresh/ingest mirror ต้องมีคำสั่ง owner แยกต่างหาก

## จุดอ่าน authoritative

1. `pf_bridge/external/PF_ATTR_GENERATION_MANIFEST.json`
2. `pf_bridge/external/.pf_attr_generations/5f18676004e95fa7466561871f3c25a2b6b217af81e9751cf3f446e4efa979f1/PF_ATTR_ROLE_DISCRIMINATOR.tsv`
3. generation เดียวกัน: `PF_ATTR_FIELD_SEMANTICS.tsv`, `PF_ATTR_DATA_BINDINGS.tsv`, `PF_ATTR_SEMANTIC_REPORT.md`, `PF_ATTR_FOR_SERVER.md`, `PF_ATTR_UNRESOLVED.tsv`, `PF_ATTR_CONFLICTS.tsv`
4. รายงานสะสมฉบับเดียว: `C:\Users\Panya\Desktop\Pirate Force\Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md`

ต้องอ่าน manifest แล้ว resolve generation directory เดียวกัน; top-level TSV เป็น compatibility mirrors ไม่ใช่ atomic authoritative snapshot

นี่คือ P0-4 checkpoint เพียงไฟล์เดียว ไม่มีการสร้างรายงาน Desktop ซ้ำ และไม่มีการเขียนหรือรันฝั่ง ServerProject/GameClient งานถัดไปตาม GOAL_MASTER คือ P0-5; checkpoint นี้ไม่อนุญาตให้เปลี่ยน server implementation โดยอัตโนมัติ
