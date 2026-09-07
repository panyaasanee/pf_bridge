# R323D RESULTS (ka1-A attended · Panya ที่คีย์บอร์ด 21:5x–22:5x) — RE-305 ครึ่งสาย **จบ**: `ItemOperateVitalReq op=5` value32 = `1<<N` ตารางบิต 13 ช่องสวมใส่ครบ · GT-288 ชุด 1 **MEASURED**: สีชื่อ = ความสัมพันธ์ฝ่าย (s_ENEMY) เท่านั้น ไม่มีเหลือง/ส้ม

ADDRESSEE: LANE-K (พับผล + แก้ชุด 3 ของ GT-288) · cc: LANE-DB (เจ้าของ RE-305 / GT-272) · LANE-B (เจ้าของ GT-288) · COO · chief
ส่งทาง: สะพาน (เครื่องเจ้าของเปิด)
OBSERVER_CONFIRMED: 2026-09-07T22:2x+07:00 (Panya ลากไอเท็มลงช่องทีละช่อง 13 ช่อง แล้วสั่ง "จดตามฉัน" ลำดับช่อง) · 2026-09-07T22:4x+07:00 (Panya: ภาพหน้าจอแถวหุ่น 8 ตัว + สีทีละตัว)

## บูต (สองบูตในนัดเดียว · ทรีไร้ธง · run DB ตัดจาก canonical · canonical sha **ไม่เปลี่ยน** `4FF37060…A548454`)
- **บูต A (RE-305)** BOOT_COMMIT `e5ed9370` (resolver หัวเขียวล่าสุด) · ไม่มีธง ไม่มี env · jobs 1580 บูต / 1581 teardown · run DB `state/run_re305_20260907_214950.sqlite3` · capture `GameClient/capture_r323d_a_20260907_214950/` · ตัวละคร Arena01 (Gladiator LV60) มีดาบในกระเป๋า · ระหว่างรอบเธอไปตีมอนได้ของดรอป 1 ชิ้น (สร้อย 2205001) + มีกุญแจ (identity=1)
- **บูต B (GT-288 ชุด 1)** BOOT_COMMIT `3ff41aae` (main ณ ตอนบูต `52c5d56b` ไม่มี mainline run สำเร็จ · resolver ถอยไปหัวเขียวล่าสุด) · env `PF_NAME_COLOUR_SWEEP=1` (ใบต้องการ) · RECHECK pytest ผ่านบนทรีบูต · jobs 1582 / 1583 · run DB `run_gt288_20260907_224211` (ต่อจาก run_re305) · capture `capture_r323d_b_20260907_224211/` · **ตัวละคร Arena01 (เดิม) ไม่ใช่ตัวใหม่** — deviation จากใบ (ชุด 2 เมื่อค่ำใช้ตัวใหม่แล้ว ผลเหมือนกันด้าน login บนบก `basic_faction=1`)
- ปิดสะอาดทั้งสองบูต (`FINAL listeners=0 clients=0`) · release 1584 · ไม่มีเหตุการณ์ teardown ชน client (กติกาใหม่หลัง 19:33 ใช้ได้)

## RE-305 — ครึ่งสาย (client → server) **จบ** · ครึ่งเซิร์ฟเวอร์ (reply) ยังเปิด
### เฟรม (ทุกครั้ง 36 B · `[G< #n] IDs=[(0, 28271, 'GSCN_RunTimeProtocolReq'), (15, 19437, 'ItemOperateVitalReq')]` · server: `journaled and receives no reply` ตามโค้ดปัจจุบัน)
```
#207 (ดาบ→มือหลัก1)  12 6F 6E 14 00 00 00 00 08 00 0B 02 12 01 00 12  ED 4B 0B 00 0B 05 14 08 00 00 00 32 04 00 00 00  00 00 00 00
#967 (ของดรอป→หมวก)  12 6F 6E 14 00 00 00 00 08 00 0B 02 12 01 00 12  ED 4B 0B 00 0B 05 14 01 00 00 00 32 06 00 00 00  00 00 00 00
```
- หัว 20 ไบต์เหมือนกันทุกเฟรม (`12 ED 4B` = vital id 19437) · `0B 05` = operation 5 · `14 <u32 LE>` = value32 (บิตช่อง) · `32 <u64 LE>` = item identity (4 = ดาบ · 5 = สร้อยที่ดรอปมา · 1 = กุญแจ · 6 = ไอเท็มดรอปชิ้นที่สองที่เธอใช้ไล่ 13 ช่อง) — ตรงกับ `[MILESTONE] V123_EQUIP_FROM_BAG_REQUEST_CAPTURED_NO_REPLY operation=5 value32_mapped=… item_identity=…` ของเซิร์ฟเวอร์
### ตารางบิต 13 ช่อง (เฟรม #967–#985 ตรงกับลำดับที่เจ้าของไล่ลากทีละช่อง: "หมวก, เสื้อ, กางเกง, ถุงมือ, รองเท้า, สร้อย, กำไล, แหวน, ตรา, สมบัติ, Sword Soul, มือหลัก1, มือรอง1")
| ช่อง (คำเจ้าของ) | value32 | N (1<<N) |
|---|---|---|
| หมวก | 0x00000001 | 0 |
| เสื้อ | 0x00000002 | 1 |
| กางเกง | 0x00000004 | 2 |
| มือหลัก1 | 0x00000008 | 3 |
| มือรอง1 | 0x00000010 | 4 |
| ถุงมือ | 0x00000020 | 5 |
| รองเท้า | 0x00000040 | 6 |
| สร้อย | 0x00000080 | 7 |
| แหวน | 0x00000100 | 8 |
| ตรา | 0x00000200 | 9 |
| กำไล | 0x00000400 | 10 |
| Sword Soul | 0x00008000 | 15 |
| สมบัติ | 0x00010000 | 16 |
- บิต 11–14 ไม่ปรากฏ (ช่องที่ UI ไม่มีให้ลาก — น่าจะ มือหลัก2/มือรอง2/ฯลฯ ของชุดอาวุธสำรอง · **ไม่ยืนยัน**) · ยืนยันซ้ำจากรอบที่ไม่เรียง (#293–#306 ค่าเดียวกันครบ 13 ค่า) และจาก R321 (ดาบ→มือหลัก = 0x08)
### พฤติกรรม client ที่วัดได้
- **ลากเท่านั้นที่ส่งเฟรม** — ดับเบิลคลิกไอเท็ม และ Shift+คลิกขวา ส่ง 0 เฟรม (ต่างจากบันทึก R321 ที่ว่าดับเบิลคลิกก็ส่ง — R321 ตอนนั้นเธออาจลากโดยไม่รู้ตัว หรือดาบตอบสนองต่างจากไอเท็มดรอป · ไม่ตัดสิน)
- **client ไม่ตรวจชนิดไอเท็มกับช่อง**: ดาบ (identity 4) ลงได้ทุกช่องทั้ง 13 (#293–#306) · สร้อย (identity 5) ลง 2 ช่อง (#553 0x08 = มือหลัก1 · #554 0x80 = สร้อย) · กุญแจ (identity 1 ไม่ใช่ของสวมใส่) ลง 2 ช่อง (#619 0x08 · #620 0x80) · ของดรอปชิ้นที่สอง (identity 6) ลงครบ 13 ช่อง (#668 + #967–#985) — ส่งเหมือนกันหมดทุกชนิด ⇒ **เซิร์ฟเวอร์ต้องเป็นผู้ปฏิเสธ** (ตอบ error/เงียบ) ไม่งั้นกุญแจใส่หัวได้
- ชั้นจอ: ทุกครั้งไอเท็มเด้งกลับกระเป๋า ไม่มีข้อความ (server ไม่ตอบ) — ตรงกับ GT-272 ที่ยังค้าง "สวมแล้วต้องเห็นบนตัว"
### nonclaims
- ไม่อ้างว่าบิต 11–14 คืออะไร · ไม่อ้าง layout ของ reply (ยังไม่มีเฟรมตัวอย่างจากเซิร์ฟเวอร์เดิม — ครึ่งนี้เป็นงาน RE static/DB) · ไม่ได้ทดสอบถอด (unequip) และไม่ได้ทดสอบลากช่อง→ช่อง · การจับคู่ชื่อช่อง↔บิตอาศัยลำดับที่เจ้าของบอกปากเปล่า 13 ช่องกับ 13 เฟรมที่มาต่อกัน (#967–#985 ไม่มีเฟรมอื่นแทรก) — ถ้าเธอสลับลำดับ 1 คู่ ตารางจะสลับ 1 คู่ตาม; ค่า 0x08=มือหลัก1 และ 0x80=สร้อย ยืนยันอิสระจาก R321 และจากการลากสร้อยครั้งที่ 2
- BUILD_PROPOSED: ItemOperateVitalRes (server reply to op=5) | LANE-DB | on op=5 with value32 = 1<<N: validate item type vs slot N (reject key/necklace-on-weapon), persist equip in DB, and send the reply frame that makes the client draw the item on the body; token: owner drags sword to main1 and sees it on the character + DB row + a named [G>] frame · this closes GT-272 attended half
- BUILD_PROPOSED: equip slot constants | LANE-DB | ship the 13-slot bit table above as a named constant table (slot name -> bit) with a test that pins every value; token: test file on main

## GT-288 NAME-COLOUR-SWEEP-DUMMY-ROW-001 ชุด 1 (faction) — **MEASURED ทั้งสองชั้น**
### ชั้น wire
- `NAME_COLOUR_SWEEP_STANDING_REFUSAL allowed=False blockers=3` (ตามคาด) · **`NAME_COLOUR_SWEEP_ARMED actors=8 census_actors=108 wire=116 pc=21877 frame=21891`** · `[G>] WORLD_CENSUS_INITIAL_108_SWEEP_8 (21891 bytes)` ×1 + `REAPPLY` ×1 · login บนบก `basic_faction=1`
- หุ่น 8 ตัว (จากโค้ด `_faction_set`): N-BASE (ไม่มีบิต faction) · N-F07 · N-F12 · N-F999 · M-BASE (faction 6 = FIELD_MOB_FACTION) · M-F07 · M-F12 · M-F999 · ผู้เล่นฝ่าย 1 ซึ่ง `CONSTDATA_TH__FACTION` s_ENEMY = `6;11;12;17;18;26`
### ชั้นจอ (Panya · หุ่นเรียง −X ห่าง 150 · ไม่คลิก/ไม่ตี)
| ป้าย | faction | อยู่ใน s_ENEMY ของฝ่าย 1? | สีที่เห็น |
|---|---|---|---|
| N-BASE | — | ไม่ | **เขียว** |
| N-F07 | 7 | ไม่ | **เขียว** |
| N-F12 | 12 | ใช่ | **ชมพู** |
| N-F999 | 999 | ไม่ | **เขียว** |
| M-BASE | 6 | ใช่ | **ชมพู** |
| M-F07 | 7 | ไม่ | **เขียว** |
| M-F12 | 12 | ใช่ | **ชมพู** |
| M-F999 | 999 | ไม่ | **เขียว** |
- ทั้ง 8 ตัววาดขึ้นจอ มีป้ายชื่อ ร่างกายปกติ (ไม่มีอาการเปลือย/T-pose ของชุด 2)
### สิ่งที่ตารางบอก
- **สีชื่อของหุ่นทุกตัว = สูตร "ผู้เล่นต่างฝ่าย"**: faction อยู่ใน s_ENEMY ของผู้เล่น → ชมพู · ไม่อยู่/ไม่มี → เขียว · **ต้นแบบ NPC กับต้นแบบมอน ให้ผลเหมือนกันทุกค่า** ⇒ ฟิลด์ที่ต่างกันระหว่าง NPC(1) กับ มอน(916) ใน body **ไม่ใช่**ตัวเลือกสูตร และ faction ก็ไม่ใช่ (มันแค่เลือกเขียว/ชมพูภายในสูตรผู้เล่น)
- รวมกับชุด 2 (actor_type/สกิน ไม่มีผล): **client ยังมองหุ่นทุกตัวเป็น "ผู้เล่น"** — สีเหลือง(NPC)/ส้ม-แดง-เทา(มอน) ยังไม่เคยถูกเรียกใช้เลยในทุกชุด · ตรงกับห่วงโซ่เกตของ RE-222: **เกตแรกคือเครื่องหมายของ identity** (identity บวก → สูตรผู้เล่น · identity ≤ 0 → สายเช็ค NPC/มอน: ตาย→เทา · NPCAttr · identity ที่ผูกไว้ `+0x98/+0x9C` · scene lookup · ชนิด `CNetNPC` · behaviour predicate) — หุ่นทุกตัวของเราใช้ identity `0x2000+…` (บวก) จึงไม่มีทางหลุดจากสูตรผู้เล่น
### ข้อเสนอชุด 3 ใหม่ (แทนชุด 3 เดิม SPEC ONLY · K แก้ใบ · B เขียนโค้ด)
- **ชุด 3 = สวีปเครื่องหมาย identity**: N-BASE (ควบคุม) · **N-NEGID** (NPC body เดิม แต่ actor_identity เป็นค่าลบ/บิตสูง ตามที่ RE-222 ระบุว่าเป็นสาย non-player) · **M-NEGID** (มอน faction 6 + identity ลบ) · **M-NEGID-DEAD** (เหมือน M-NEGID + สถานะตาย ถ้า field มี) · ถ้า RE-222 ระบุ linked identity ที่ `+0x98/+0x9C` ให้เพิ่ม **N-LINK** (identity บวก แต่ช่อง +0x98/+0x9C ชี้ไปค่าลบ) · env `PF_NAME_COLOUR_SWEEP=3` · HEADLESS_PROOF แบบเดียวกับชุด 1/2 · เกณฑ์ผ่าน = ตัวใดตัวหนึ่ง **ไม่ใช่เขียว/ชมพู** (เหลือง/ส้ม/แดง/เทา หรือไม่มีป้าย) — แม้จะเป็นสีอะไรก็ตาม ถือว่าหลุดจากสูตรผู้เล่นแล้ว
- ความเสี่ยงที่ต้องเขียนในใบ: identity ลบอาจชนกับ identity ของ census/ผู้เล่น หรือทำ client crash — ให้ B พิสูจน์ในทรีก่อน (ไม่ชนตาราง placement) และให้ใบอนุญาต client crash เป็นผลลัพธ์ที่บันทึกได้
### nonclaims
- ไม่ได้วัดว่า "ชมพู" = ตีได้ (ใบห้ามคลิก) · ไม่ได้ทดสอบ faction ที่อยู่ใน s_ENEMY แต่ไม่ใช่ 6/12 (11/17/18/26) — สองค่าที่ทดสอบพอสรุปกฎ · ไม่ได้วัดว่าฝ่าย 999 มีแถวใน s_FRIEND ของใคร · ตารางสีต่อตัวรวบรวมจากคำเจ้าของในแชท (ภาพหน้าจอ 22:4x) — ka1-A เป็นผู้จับคู่ป้ายกับสี
- BUILD_PROPOSED: GT-288 set 3 identity-sign sweep | LANE-B | replace the SPEC-ONLY set 3 with N-NEGID / M-NEGID / M-NEGID-DEAD (+ N-LINK if RE-222 pins +0x98/+0x9C) under PF_NAME_COLOUR_SWEEP=3, same HEADLESS_PROOF shape; token: NAME_COLOUR_SWEEP_ARMED actors=4|5 on a flagless tree + placement-collision test green

## เก็บตก (แจ้งไว้ · ไม่ใช่ผลใบ)
- ทั้งคืน R323A–D = 4 นัด 11 บูต ตัวละคร Arena01 ทั้งหมดยกเว้น R323A/B (ตัวใหม่ "test") · ไม่มีการเขียน canonical
- คิวที่เหลือสำหรับนัดหน้า (รอ K ยืนยันสถานะ): GT-304 (คำตัดสินเกาะบนคอนโซล — ต้องรอ merge) · GT-291 · GT-288 ชุด 3 (หลัง B สร้าง) · GT-272 รอบ 2 (หลัง DB ทำ reply) · M2 attended เมื่อ A ต่อ `0x4477` (RE-303 ตอบแล้ว 21:50)

RESULT: RE-305 WIRE-HALF-DONE R323D 2026-09-07 22:3x (op=5 value32 = 1<<N · 13-slot bit table pinned to owner-stated slot order · drag only · client accepts any item on any slot · server reply half still open)
RESULT: GT-288 MEASURED R323D 2026-09-07 22:4x (set 1: 8 dummies drawn · colour = faction in player s_ENEMY → pink else green · NPC and mob prototypes identical · no yellow/orange/red/grey · wire actors=8 wire=116 SWEEP_8)
SCOREBOARD: NONE | ผู้เล่นยังสวมของไม่ได้และยังเห็นชื่อสีผิด แต่ตอนนี้รู้บิตของทุกช่องสวมใส่ (DB ทำ reply ได้เลย) และรู้ว่า faction/actor_type/สกินไม่ใช่ตัวเลือกสูตรสี — เหลือเครื่องหมาย identity เป็นผู้สมัครแรก | 20260907_2305_KA1A-R323D-RESULTS-*
