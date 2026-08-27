# M1-P RESULT 2026-08-28 01:50 +07:00 — **PASS: เจ้าของยืนยัน "NPC และมอนสเตอร์เหมือนเมื่อก่อนจนน่าตกใจ ทุกตัวแทบถูกต้องหมดและควรอยู่ที่นี่"** — M1 true identity สำเร็จครั้งแรกที่เกาะคุก · พร้อมช่องว่าง 6 ข้อ + เบาะแสใหญ่: หน้าต่างแผนที่ (M) ของ client รู้จัก NPC ทุกตัวทุกฉากอยู่แล้ว

ถึง: สาย A (เจ้าของ M1 · ADDRESSEE: LANE-A) · chief (ADDRESSEE: chief) · สาย B (ADDRESSEE: LANE-B) · RE runner (ADDRESSEE: RE) · COO · cc สาย GM, กะ1-B
จาก: attended session "กะ1-A" (Panya ขับ UI เอง ตามกติกา brief → "ทราบ" → บูต) · OBSERVER_CONFIRMED: 2026-08-28T00:3x-00:5x+07:00 (คำเจ้าของ + ภาพในเกม 2 ใบ + วิดีโอเต็มรอบ)

## สถานะที่ควรเป็น
- **M1-P = PASS (claim: NPC/มอนบนเกาะคุกเป็นตัวจริงตามตำแหน่งจริง — เจ้าของตัดสิน)** · สมมติฐาน "Bg0002 MOBSET_NN = MOBS n_ID" **ยืนยันโดยเจ้าของทั้งฉาก** ไม่ใช่แค่ 2/7 anchor อีกต่อไป — สาย A ปิดหัวใบ/ประกาศได้
- ยังไม่ใช่ "M1 ปิด" ทั้งก้อน: Port Royal ยังไม่ทำ (ดู §เบาะแสใหญ่) และมีช่องว่าง 6 ข้อที่เจ้าของชี้ (ล่าง) — เปิดเป็น M1-P2 (polish) แยกจาก identity ที่ผ่านแล้ว

## บูต (jobs 1311 hold+resolve · 1312 boot_video · 1313 teardown_video กดโดยเจ้าของ 00:53 · release 1314)
- BOOT_COMMIT **6406a05** = main HEAD (เขียวของตัวเอง run 33095719949) · ไร้แฟล็ก · code delta 0 · ด่าน: grep 4/4 + `tests/test_bg0002_census_wiring.py` 8 passed ผ่าน dispatcher จริง
- **seed**: run DB สำเนา `run_m1p_20260828_002659` แถว Arena01 `scene_id 1→2, (26905,21185,1680)` (SEED_OK) · canonical 4FF37060… ไม่เปลี่ยน · teardown PASS (listeners 0, clients 0, ffmpeg 0)
- วิดีโอ: evidence_video\1312_m1p_FULLROUND_20260828_002704.mkv · ภาพเจ้าของ: evidence_screens\M1P_ingame_20260828_*.png + M1P_mapwindow_PrisonExile_*.png · คอนโซล: GameClient\capture_m1p_20260828_002659\server_console_live.out.txt

## ชั้น wire (คอนโซล)
- L163 `WORLD_SCENE scene_id=2 model=BG0002 name=Prison_Exile_Island spawn=(26905,21185,1680) population=bg0002_roster` · `WORLD_SCENE_LIVENESS decision=honour reason=accepted_before_this_process stored_scene=2` · L165 `PLAYER_FACTION basic_faction=1` ⇒ ทางเข้าไร้แฟล็กผ่าน persistence ใช้ได้จริง (ไม่ต้องมี GM/override)
- L265 `WORLD_CENSUS assembled=97/97 wire=97 … source=bg0002_full_roster unresolved=9` · L363 `[G>] WORLD_CENSUS_BG0002_INITIAL_97 (17754 bytes)` · L1474 REAPPLY · รายตัว n_ID=1..41 ตรงตาราง (3 Navy soldier ×13, 27 กวาง ×4, 28 ×6, 29 ×7, 30 ×11, 31 นก ×3, 32 ×3, 33 ×9, 34 ×6, 35 ×3) · unresolved 9 = n_ID 37 (Port transportation — MOBS ไม่มีแถว 37?) + ชุด 101/102/103×5/104
- 🔴 **จังหวะส่งสำมะโน**: census ถูกส่งหลัง `TargetPosVital` ใบแรกของ client (L260 → L264-265) ไม่ใช่ตอน StartGame/arrival — ตรงกับที่เจ้าของเห็นข้อ 1 ทุกประการ
- เซสชัน ~694 heartbeat (~26 นาที) ไม่มี traceback · client ปิดปกติ

## ชั้น client-observable — คำเจ้าของ (คำต่อคำโดยสรุป)
**"npc และ monster เหมือนเมื่อก่อนจนน่าตกใจ! ทุกตัวคือแทบจะถูกต้องหมดและมันควรจะอยู่ที่นี่"** — Pike (Unemployed Sailor), Mountain Deer, Drunk wolf pirates, Mo Yuzi (Naval Communications Bureau) ในเต็นท์ทหารเรือ ฯลฯ ถูกที่ทั้งหมด
ช่องว่างที่เจ้าของชี้ (ทุกข้อ = งาน M1-P2):
1. **เข้าฉากแล้วไม่มีอะไรเกิดขึ้นจนกว่าจะกด Q/E/A/S/D/W หนึ่งครั้ง** (เซิร์ฟเวอร์เดิมมี NPC ทันที) — ฝั่งสาย: census รอ TargetPosVital ใบแรก ⇒ **แก้ให้ส่งตอน arrival** (หลัง StartGame/teleport เสร็จ ไม่ต้องรอผู้เล่นขยับ) — chief/สาย A
2. **ทุกตัวขยับ/หายใจจริง แต่หันหน้าทิศเดียวกันหมด** ไม่เป็นธรรมชาติ — เราไม่ส่ง heading; placement มี field ทิศ (f32_3/4/5 ตัวไหน — สาย A/B ตรวจ + `CONSTDATA_TH__MARKER.n_DIRTECTION` เป็นตัวอย่างค่า) — สาย A
3. **ชื่อทุกตัวสีเขียว** (ทั้ง NPC และมอน) — กฎเจ้าของ: **NPC ต้องเหลืองเท่านั้น · มอนต้อง ส้ม/แดง/เทาเมื่อตาย** (ชมพูแบบรอบนกก็ผิด) — RE-109 + DIAG-001 (GT-114) เป็นทางไป · ข้อมูลใหม่: entry แบบเดียวกันให้สีเขียวทั้ง NPC และมอน ⇒ ฟิลด์ที่เราส่งเหมือนกันหมดคือตัวการ
4. **มอนเกิดถูกชนิดแต่ความหนาแน่นน้อย** — เจ้าของเชื่อว่ามีกลไก "จำนวนต่อกลุ่ม" และ "ตัวเล็ก-ตัวใหญ่ไม่เท่ากันในโมเดลเดียวกัน" — ตรงกับที่สาย B วัดไว้ว่า placement `u16_1 ≈ จำนวนตั้งใจ 78%` ⇒ spawn N ตัวต่อ placement + ฟิลด์ scale (f32?) — สาย B/A
5. **NPC เควสหาย**: "Mirage Reel" ควรยืนข้าง Mo Yuzi (แมว) แต่ไม่ถูก render — MOBS_TIP มี "Mirage reel" หลาย n_ID (151, 230-238, 245, 485, 487, 718-727, 752, 866) ต้องหาว่าตัวไหนของฉาก 2 และอยู่ใน placement ชุดไหน (ชุด 101-104? หรือไม่มีใน .npc = spawn จากเควส) — สาย A + RE
6. **Pike ชื่อ/title ต่ำจนทับโมเดล** เพราะของจริง Pike อยู่ท่า "นอนร่อแร่" บนพื้นตลอด · NPC บางตัวมีท่าเดินไปมาเป็นเอกลักษณ์ — ฟิลด์ pose/idle-animation ต่อ NPC (MOBS มี n_AI_WANDER 1/2/16 — เบาะแส) — เจ้าของให้เป็นเบาะแส จะแปะภาพเซิร์ฟเวอร์เดิมเทียบให้
7. (จากรอบ ad-hoc ของกะ1-B คืนนี้) เจ้าของกับกะ1-B **ลองใส่ค่า Attr ที่ยังไม่รู้ความหมายให้ตัวละคร → สถานะตัวละครสมบูรณ์ขึ้น (มีอาชีพ เปิดหน้าต่างสกิล K ได้ ฯลฯ)** ⇒ เจ้าของสรุปว่า "คอขวดทุกวันนี้ (ตีมอนไม่ได้ NPC/มอนแสดงแปลก) มาจากเราใส่ค่าให้ actor ไม่ครบ" — ดูใบเคาะทิศทาง 0200

## เบาะแสใหญ่ (เจ้าของชี้ ผู้ช่วยยืนยันจากภาพ)
**หน้าต่างแผนที่ในเกม (กด M)** แสดง: แผนที่ฉากพร้อมชื่อโซน (Guard Encampment, North Seaside, Battlefield, Exile Encampment, East/South Seaside) + ไอคอนรับเควส + **รายชื่อ NPC ของฉาก** (เกาะคุก: Navy Transfer, Warden Sebastian, Drunken Captain Legend Jack, Witch Servant Edmund, Madman Captain Baboza, Prison Gourmet Paul, The Shipbuilding Thin … = n_ID 1,2,6,8,9,12,18 ตามลำดับ = NPC ที่มีเควส) + ปุ่ม **GO!** เดินอัตโนมัติไปหา · รายการนี้มี "Mirage Reel" ที่เรา**ไม่ได้ส่ง** ⇒ รายชื่อมาจากฝั่ง client (ตาราง/ไฟล์) ไม่ใช่จากสำมะโนของเรา · Port Royal ก็มี (156-163…) · แผนที่โลก "Atlantic Ocean: Rising Sun Sea" มีเกาะคุก/Port Royal/Spice + รายชื่อเรือ (Santa Maria, Merchant marine Trade Ship ×3)
⇒ คำเจ้าของ: "npc ทุกตัวในแต่ละแมพมีข้อมูลใน client หมดแล้ว ต้องใช้ให้เกิดประโยชน์" — งานในใบ 0200

## nonclaims
- [ไม่อ้าง] ว่า 9 unresolved เป็น "ไม่มีในเกมเดิม" — 37/101-104 ต้องตรวจ · [ไม่อ้าง] ว่า GO! ใช้ตำแหน่งจากตาราง client จนกว่า RE/probe จะพิสูจน์ (อาจเป็น packet จากเซิร์ฟเวอร์เดิม) · [ไม่อ้าง] สาเหตุสีเขียว/ทิศเดียวกัน — ฟิลด์ต้องวัด

## หลักฐาน
คอนโซล L163-165, 255-366, 1474 · outbox\1311_m1p_hold_and_resolve.utf8.txt (pytest 8 passed) · outbox\1312_m1p_boot_video.utf8.txt (SEED_BEFORE/AFTER) · outbox\1313_m1p_teardown_video.out.txt (PASS) · evidence_screens\M1P_* + REF_OURS_mapwindow_* / REF_OURS_worldmap_* (จากรอบ ad-hoc กะ1-B 22:57-23:00) · LOCK_GAME release 1314
