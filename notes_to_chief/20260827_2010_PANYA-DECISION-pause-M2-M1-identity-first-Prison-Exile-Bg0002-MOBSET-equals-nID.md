# PANYA-DECISION 2026-08-27 20:10 +07:00 — พัก M2 · ทำ M1 "true identity spawns" ให้สำเร็จก่อน · เริ่มที่เกาะคุก (Prison Exile, scene 2 / Bg0002) — และไฟล์ placement ของเกาะคุกบอก identity ตรง ๆ

จาก Panya (เคาะในแชทของกะ1-A 19:5x — เขียนแทนโดยกะ1-A) — ถึง chief, COO, **สาย A (เจ้าของ M1 · ADDRESSEE: LANE-A)**, สาย B (มอน 27-35 · ADDRESSEE: LANE-B), RE runner (ADDRESSEE: RE), cc สาย GM, กะ1-B

## คำเคาะ (คำของเจ้าของ)
"สิ่งที่หวังจริงตอนนี้คือ true identity spawns · พัก M2 ออกไปก่อนได้เลย ทำ M1 ให้สำเร็จให้ได้เสียที ตอนนี้มีหลักฐานมากขึ้นเยอะแล้ว — บล็อก Port Royal (156+) และ 1-35 ของเกาะคุก แทบแน่ใจแล้วว่ามี NPC และมอนไหนบ้าง · ถ้า Port Royal ยังยากไป ตั้งความหวังที่เกาะคุกก่อนเป็นที่แรก"

⇒ มีผลทันที: (1) **M2 พัก** — งานฉาก 17/ปลายทาง 126/ออปชัน 3205/vehicle-bind หยุดหลัง PR ที่เปิดอยู่ merge · ยกเว้น **บั๊ก persistence (COO 1746 ข้อ 1) ต้องแก้** เพราะเส้นทางเข้าเกาะคุกข้างล่างพึ่ง persistence เดียวกัน (2) **M1 = ลำดับหนึ่งของทุกสาย** (3) **เป้าแรกของ M1 = เกาะคุก** ("M1-P") · Port Royal ทำคู่ขนานในชั้น RE/ข้อมูล ไม่ใช่ชั้นบูต

## สิ่งที่กะ1-A พบตอนตรวจข้อมูล (20:0x) — [สมมติฐานแข็ง ต้องให้สาย A ยืนยันครบทุก anchor ก่อนใช้]
`pf_bridge/gamedata/scene/Bg0002/Bg0002.placements.tsv` (106 placements, จาก GameClient\Data\Scene\Save\Bg0002\Bg0002.npc) ตั้งชื่อ placement เป็น **`MOBSET_NN MM`** (NN = ชุด, MM = ตัวที่) — ต่างจาก bg0001 ที่ใช้ `Mob_Set_NN` เรียงตาม index (1-113) ซึ่งพิสูจน์แล้วว่าไม่ใช่ identity
หลักฐานว่า **NN ของ Bg0002 = MOBS n_ID**:
1. ชุด 1-35 มีครบทุกเลข = ขนาดบล็อกเกาะคุกพอดี · ชุด **1-26 มีตัวเดียว** ทุกชุด = NPC (MOBS 1-26: n_AI_COMBAT 0, EXP 0) · ชุด **27-35 มีหลายตัว** (27 ×4, 28 ×6, 29 ×7, 30 ×11, 31 ×3, 32 ×3, 33 ×9, 34 ×6, 35 ×3) = มอน (MOBS 27-35: n_AI_COMBAT 100-352, f_RATIO_EXP 1.0, 35 = Fighting Fish Sergeant BOSS) — โครงตรงกันแบบไม่บังเอิญ
2. anchor ของเจ้าของ: **Veronica 14** HUD (3,825 / 12,447) ↔ `MOBSET_14 01` = (−3598, 12550, 1845) — ตรงหลัง sign-flip แกน X (ต่าง 227/103 หน่วย = ระยะที่เธอยืนห่าง) · **Legend Jack 6 + Men 7 (×2) + Mountain Deer 27** ในคลิปยืนกลุ่มเดียวกัน ↔ `MOBSET_06 01` (−8020,14586) · `MOBSET_07 01/02` (−8607,14735)/(−7542,14951) · `MOBSET_27 02` (−8637,13720) — อยู่ในรัศมี ~1,000 หน่วยจริง และ "Men" มี 2 ตัวพอดี
3. ชุด 36-41 มีตัวเดียว = n_ID 36 Columbus (Marine Transport Station) 37 Port transportation 38 Reyna 39 Mo Yuzi 40 Carle 41 Martin — `MOBSET_36 01` (29414,22476) อยู่ใกล้ `MOBSET_01 01` Navy Transfer (26078,20389) = ท่าเรือ ⇒ ตรงคำแก้ของเจ้าของ 1040 ว่า NPC วาร์ปของเกาะคุกคือ Columbus รุ่นเกาะ (ไม่ใช่ Navy Transfer) และบอกว่าบล็อกเกาะคุกจริงคือ **1-41** ไม่ใช่ 1-35 · ชุด 101-104 (5 placements) ยังไม่รู้ — ห้ามเดา
4. n_ID 31 = Tornado Eagle อยู่ในบล็อกนี้ (ชุด 31 ×3) — นกที่เราเอาไปวางในเมืองคือมอนของเกาะคุกจริง

## งาน M1-P (เรียงตามลำดับ · เพดาน: headless proof ภายในพรุ่งนี้เช้า แล้วเรียกเจ้าของนั่ง 1 รอบ)
1. **สาย A** — roster_bg0002: ทุก placement → n_ID = NN (1-41), name/title จาก MOBS_TIP, body/preset/lv จาก MOBS, ตัวที่ MM = instance · ตรวจ anchor ทั้ง 7 จากใบ 1020 (Navy Transfer 1 ประตูท่า · Sebastian 2 + Goliaon · Pike 5 ในคอกไม้ · Legend Jack 6/Men 7/Deer 27 · Veronica 14 HUD) ด้วย transform sign-flip เดียวกันทุกจุด — ต้องตรงทุก anchor ถึงประกาศว่า NN = n_ID · ชุด 101-104 ติดป้าย UNKNOWN ไม่วาง · เขียน WORLD_CENSUS ของ scene 2 ผ่าน path production (census composer เดิม, scene id 2)
2. **chief/สาย A** — ทางเข้าเกาะคุก**ไร้แฟล็ก**: ใช้ path persistence ที่มีอยู่ (`WORLD_SCENE_LIVENESS decision=honour reason=home_row stored_scene=…`) — run DB สำเนาที่ตำแหน่งของ Arena01 ถูกตั้งเป็น scene_id=2 ที่จุดปลอดภัยใกล้ท่า (แถว `MOBSET_01` (26078,20389,1735) หรือจุดที่ SCENE-001 เคยเรนเดอร์) · serializer รับ scene 1/2 อยู่แล้ว (comment ใน runtime) · **ห้ามใช้ `--*-scenario`** · แก้บั๊ก persistence (บันทึก scene_id ผิด) พร้อมกัน — ถ้าเข้าทางนี้ไม่ได้จริง ค่อยถอยไป login-scene override (CORE-REQUEST-017) เป็นทางสำรอง
3. **สาย B** — มอน 27-35 ในสำมะโน scene 2 ใช้คู่ faction (1,6) เดิม + widen death scope ให้ครอบ bg0002 (guard `assert_single_scene_tables` ต้องขยาย ไม่ใช่ปิด) — **ไม่ใช่เกณฑ์ผ่านของ M1-P** (M1 = identity + ตำแหน่ง) แต่ต้องไม่ทำให้บูตล้ม · DIAG-001 (ใบ 1855) ใช้มอนจากบล็อกนี้ได้เลย (27 Mountain Deer / 30 Desert Eagle / 33 Sediment Wolf — ทุกตัว n_AI_COMBAT > 0, EXP 1.0)
4. **headless proof ก่อนเรียกเจ้าของ**: บูตไร้แฟล็ก + run DB ข้อ 2 → คอนโซล `WORLD_SCENE scene_id=2 model=BG0002` + `WORLD_CENSUS assembled=N/N` (N = 101 ถ้าตัด 101-104) + บรรทัดต่อ actor `n_ID name title @xyz` → ค่อยเขียนใบ GT-M1P (≤ 8 KB) ให้กะ1-A brief เจ้าของ: เดินจากท่า → Navy Transfer 1 / Columbus 36 → Sebastian 2 → Pike 5 → Legend Jack 6 + Men 7 + Deer 27 → Veronica 14 (HUD 3,825/12,447) — เจ้าของยืนยันชื่อ/ตำแหน่ง = เกณฑ์ผ่านของ M1-P
5. **RE runner (คู่ขนาน สำหรับ Port Royal)**: เปิดใบ "หน้าต่างแผนที่ในเกม (M) รายการ 'ค้นหาตัวละครในฉาก' + ปุ่ม GO! อ่านรายชื่อ/ตำแหน่ง NPC จากไหน — packet หรือตารางไคลเอนต์" (เสนอไว้ในใบ 1240 §① แต่ยังไม่มีใครเปิด) · ถ้าเป็นตารางไคลเอนต์ = คำตอบ placement→identity ของ Port Royal ทั้งเมือง
6. **สาย A (หลัง M1-P)**: Port Royal ด้วยแลนด์มาร์กจากคลิป (ใบ 1240 §③) + ผลข้อ 5

## ห้าม
- ห้ามอ้าง "NN = n_ID" เป็นข้อเท็จจริงจนกว่า anchor ครบ 7 · ห้าม brute-force วางทีละตัวให้เจ้าของดู (กฎ 04:5x) · ห้ามใช้ v141 source_name เป็นตัวตน · ห้ามเรียกเจ้าของก่อน headless proof ข้อ 4

— จาก Panya (เขียนแทนโดย attended session "กะ1-A") · ADDRESSEE: LANE-A, LANE-B, RE, chief
