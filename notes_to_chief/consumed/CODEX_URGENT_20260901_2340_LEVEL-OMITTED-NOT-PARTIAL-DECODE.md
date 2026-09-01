[ถึง: chief / COO / Claude ผู้ถือสิทธิ์เขียน ServerProject · cc Panya | จาก: Codex static audit · 2026-09-01T23:40:32+07:00]

# CODEX URGENT — GT-192 LV 1 เกิดจาก census ปกติไม่ได้ส่ง level ไม่ใช่ client ถอด record ได้เพียงบางส่วน

## คำตัดสินที่ต้องแก้ทันที

- **[CLIENT-OBSERVED RESULT]** GT-192 เห็น HP ของแต่ละ actor ตรงกับค่าที่ replacement แสดงใน console แต่ทุกตัวขึ้น `LV 1`, ชื่อเขียว และป้ายแบบ NPC.
- **[RECONSTRUCTED POLICY — READ-ONLY CURRENT SOURCE]** ข้อความเดิมที่ว่า “replacement ส่ง level/HP ต่างกัน แต่ client apply record เพียงบางส่วน” ไม่ถูกต้องสำหรับ census ปกติ: console พิมพ์ level จาก roster DATA แต่ wire composer ปกติไม่ได้ encode level เลย. HP ถูก encode จึงแสดงถูก; LV 1 ไม่ใช่หลักฐานว่า client เมิน level ที่ส่งมา.
- ข้อนี้ supersede เฉพาะการวินิจฉัยใน `20260901_2002_CODEX-CHECKPOINT-P04-ROLE-DECISION-SECOND.md:55` และข้อความเดียวกันใน cumulative audit. ไม่ถอนผลที่เจ้าของเห็นบนจอ.

## จุดที่ผิดในโค้ดที่รันอยู่

- Frozen helper `current/pf_login_game_server_v141.py:1139-1195` (SHA-256 `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`) รับ `name/HP/speed/scene/seq` แต่ไม่มี parameter level. BasicAttr mask มี `0x0004|0x0008|0x0100|0x0200` และ optional `0x0001/0x0040`; ไม่มี bit `0x0002`. ลำดับ body จึงเป็น optional name -> HP current/max -> optional speed -> scene/seq โดยไม่มี level.
- Ordinary scene composers เรียก helper นี้ด้วยชื่อ/HP แต่ไม่ส่ง level: `world_population_bg0006.py:188-197` (SHA `26739708c69b3ad6fbeba47c307586d5fcaaa3f3ae647cd155974f0c2bbc72aa`), `world_population_bg0009.py:188-197` (SHA `3505923e3c8c42bda5beb4eaea81b2adb7bff76d588e58e2e0f5aca16cb8e4f1`) และ `world_population_bg0015.py:273-282` (SHA `2dcfe6f10779990d06b46b99d44912675ac2cd27d79625b9c880b794d119db7a`). Console line เป็น metadata คนละทาง ไม่ใช่หลักฐานว่า bytes level ถูกส่ง.

## หลักฐาน field ที่ใช้ต่อสายได้แล้ว

- **[ORIGINAL EVIDENCE: IMAGE]** RE-117 (`20260828_0414_RE-117-RESULT-NPCATTR-INHERITS-LEVEL-MP-BITS.md`) พิสูจน์ว่า NPCAttr serializer `0x00466EB0` เรียก BasicAttr serializer `0x004656F0` ก่อนเสมอ; level คือ BasicAttr mask bit `0x0002`, object `+0x5E`, `u16` tag `0x12`, W `0x00465736..0x0046574A`, R `0x00465870..0x00465884`.
- **[RECONSTRUCTED POLICY — SAFE REUSE]** `field_mobs.py:1564-1608,1668-1682` (SHA `a4fc6eaee6351d10e7bb44abb527db51966f217d474318a92078811bb79bb865`) มี splice ที่ guard แล้ว: เปิด bit `0x0002` และวาง `u16tag(0x12, mob.level)` หลัง optional name และก่อน HP ตามลำดับ mask.

## BUILD IMPACT / ข้อเสนอ

- **ทำได้ทันทีแบบ bounded:** สร้าง Foundation-owned additive helper/wrapper สำหรับ census ปกติให้ encode level ด้วยกฎเดียวกับ splice ที่พิสูจน์แล้ว. `current/pf_login_game_server_v141.py` เป็น frozen legacy ห้ามแก้ตรงนั้น. ทดสอบ focused codec/order + regression ก่อน attended round แล้ววัดว่าป้าย LV เปลี่ยนตาม actor จริง.
- **ห้ามเหมารวมไปแก้สี:** สีเขียว/ป้ายแบบ NPC เป็นคนละ boundary. Census ปัจจุบันใช้ actor type 4/CNetNPC และ synthetic positive qword; P0-2 พิสูจน์เพียง selector lanes แต่ยังไม่พิสูจน์ original identity assignment/lifecycle-safe negative domain. ห้ามสุ่ม negative ID, เปลี่ยน actor type, ใส่ faction อย่างเดียว หรือ hardcode FontStyleID.
- Scene 14 มี hostile subset ที่ใช้ `field_mobs.hostile_actor_entry` และส่ง level อยู่แล้ว; ก่อนแก้ generic path ต้องกัน double-field/double-mask สำหรับแถวนั้น.

`BUILD_IMPACT_LEVEL: SAFE_BOUNDED_IMPLEMENTATION_NOW`

`BUILD_IMPACT_COLOR: NOT_READY_FOR_POLICY_CHANGE`

## สิ่งที่ยังต้องพิสูจน์

1. IMAGE: ตาม BasicAttr `+0x5E` จาก CNetNPC/NPCAttr ไป formatter/UILabel เพื่อยืนยัน default/refresh behavior เพิ่มเติม (ไม่ใช่ blocker ต่อการ encode field ที่ RE-117 ปิดแล้ว).
2. IMAGE: audit same-qword lifecycle ครบ registry/target/action/death/remove/drop ก่อนใช้ signed-nonpositive identity lane เพื่อสี.
3. Original-server assignment policy ยังต้องการ source-separated original runtime/traffic evidence; replacement source ไม่ใช่หลักฐานของ server เดิม.

วิธีรอบนี้: อ่านอย่างเดียว; ไม่แก้ ServerProject/V141/queue/workflow/lease/Git, ไม่เปิด client/server และไม่อ่าน raw capture/dump bytes.
