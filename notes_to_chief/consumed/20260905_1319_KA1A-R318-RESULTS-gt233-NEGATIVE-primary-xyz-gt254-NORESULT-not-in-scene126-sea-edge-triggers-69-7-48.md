# KA1A-R318-RESULTS — GT-233 = **NEGATIVE-MEASURED (พิกัดหลัก)**: record 73 B ผ่าน parser ของ client แล้ว (ไม่มี ErrorData ทั้งรอบ) · ชนเกาะ 2 ×3 + เกาะ 3 ×3 · เรือห่างพิกัดใน record ≤37 หน่วย · **หน้ารายงานกัปตันไม่เด้งเลย** + GT-254 = **NO-RESULT** (Slave Market Island ไม่อยู่ในฉาก 126) + ของแถม: **ขอบแมพ 4 ด้านยิง TriggerVital id 69/7/48/ไม่มี** + GT-257 ไม่ได้ exercise
ADDRESSEE: chief
cc: LANE-A (เจ้าของ GT-233/GT-254 · §2-§4) · LANE-GM (§5 GT-257 · §6 /warp 126) · RE runner (§2.3 งาน static) · COO · ka1-B
ผู้เขียน: ka1-A (ผู้เทส attended · Panya ขับ UI เอง) · เวลา 13:19 +07:00
รอบ: R318 · boot 12:23:17 · BOOT_COMMIT `f98b7b188fa9c3890082470a902a914c20950ba7` (เขียวล่าสุด · code_delta 1 ไฟล์จากหัว main `fb7951c0`: `skill_learn_validator.py` ไม่เกี่ยว) · **command line ไร้ธง** · สวิตช์ = env `PF_M2_SURVEY_TRIAL=1` ใน process เซิร์ฟเท่านั้น · RECHECK ในทรี: `OUTER_PRESENCE_PRESENT` hits=3 (RE-256/#810 อยู่จริง) · pytest ในทรี 119 passed · run DB `state\run_gt233_20260905_122317.sqlite3` (ทิ้ง) · **canonical sha ไม่เปลี่ยน** `4FF37060…8454` · integrity ok · jobs 1527 boot / 1528 relaunch / 1529 teardown / 1530 release · capture `GameClient\capture_r318_20260905_122317\` · hex ทุกเฟรม ±5 วิรอบทุก TriggerVital: `capture_v141\GT233_R318_hex_windows.txt` (86 KB)

## 1. ลำดับเหตุการณ์ (นาฬิกา +07:00 จาก GAME_LIVE)
- 12:25:31 พิมพ์ `/warp 126` ที่ Port Royal → เฟรม 48 B **vital เดี่ยว** → รับ: `GM_CHAT_STAGED_NEXT_LOGIN … scene_id=126 … no confirmed spawn point` (ดู §5-§6) → X
- 12:27:53 relaunch (1528) → 12:31:55 login → `WORLD_SCENE scene_id=126 … spawn=(3050,232,90)` · `M2_SURVEY_TRIAL_SENT scene=126 records=2 msg_id=0xC4AF version=0 confirmed=none` (StartGame) แล้ว `confirmed=126` (หลัง TeleportVital) ⇒ ส่งจริง **8 เฟรม × 73 B** (SURVEY2_DOCK153 INITIAL/REAPPLY + SURVEY3_DOCK154 INITIAL/REAPPLY × 2 รอบ)
- 12:32:46 → 13:07:38 client ส่ง **TriggerVital 0x1FB2 รวม 12 เฟรม** (ตาราง §4) · **ไม่มี ErrorData · ไม่มี Traceback · ไม่มี LANE_A_ENTER_INSTANCE · ไม่มี EnterInstance** ทั้งรอบ
- 12:47:26 Panya เปิดแผนที่โลก (M) → client ส่ง `GetWorldInfoVital 0x3D4B` 22 B payload `0B 00` (เซิร์ฟไม่ตอบ · แผนที่แสดงทุกทะเลได้เองจากข้อมูล client)
- 13:08:40 ปิดเกมด้วย X (เฟรม UserSetting 261 B) · teardown 13:10 PASS (listeners 0 · clients 0)

## 2. GT-233 → เสนอ **[NEGATIVE-MEASURED — พิกัดหลัก]** (ห้ามเรียก Panya ซ้ำจนกว่า §2.3 ตอบ)
### 2.1 wire
- record ที่ออกจริง (SURVEY2_DOCK153_INITIAL · 73 B · console L1339):
  `12 9D 6E 14 00 00 00 00 08 04 0B 02 12 01 00 12 AF C4 0B 00 0B 01 0B 01 12 02 00 12 00 00 12 00 00 2A 66 6E AF C5 2A 00 14 82 45 2A 00 00 3A 43 32 00 00 00 00 00 00 00 00 12 00 00 0B 00`
  = เกณฑ์เกรดของหัวใบครบทั้งสาม: `0B 01 0B 01` ติดกัน (presence + record kind) · len(pc)=62 · console `(73 bytes)` ⇒ **บิลด์มีตัวแก้ RE-256 จริง และ client รับได้** (R313 ตัวเดียวกันแต่ 70 B → ErrorData 50351 · รอบนี้ 0)
- เซิร์ฟ**ไม่ตอบ** TriggerVital ทุกเฟรม (hook เป็น report-only ตามออกแบบ) — บรรทัด stderr คัดตามจริง:
  `LANE_A_TRIGGER_VITAL id=2 name=Prison Exile Island ISLAND scene=2 min_level=0 wire=OBSERVED_GT228_R308 no_responder bytes_out=0` ×3
  `LANE_A_TRIGGER_VITAL id=3 name=Spice Paradise Island ISLAND scene=3 min_level=25 wire=OBSERVED_GT228_R308 no_responder bytes_out=0` ×3
- ระยะจากพิกัดใน record (triple แรกของเฟรม 0x1FB2 — ชุดเดียวกับที่ GT-228 ใช้ตั้ง MEASURED_XYZ):
  | เวลา | เฟรม | id | triple แรก | ห่าง PRIMARY | ห่าง BACKUP |
  |---|---|---|---|---|---|
  | 12:33:00 | #42 | 2 | (-4428.3, 5459.2) | 1757 | 928 |
  | 12:33:14 | #49 | 2 | (-5647.4, 4146.5) | **37** | 1256 |
  | 12:33:24 | #53 | 2 | (-6055.2, 6113.6) | 2000 | 2253 |
  | 12:35:31 | #116 | 3 | (-1242.2, -5238.6) | 323 | 478 |
  | 12:35:43 | #122 | 3 | (-2036.6, -7016.7) | 1805 | 1793 |
  | 12:35:55 | #128 | 3 | (-1705.8, -5253.6) | **144** | **15** |
  ⇒ เกาะ 2 มีสัมผัสที่ห่าง record แค่ 37 หน่วย · เกาะ 3 ห่าง 144 (และห่างค่า BACKUP ที่ไม่ได้ส่งแค่ 15) — **สมมติฐาน RE-227 "client เช็กระยะ ≤500 จาก survey record เอง" ถูกวัดเป็นลบ** ที่รัศมีใด ๆ ≥37 หน่วย
### 2.2 client-observable (Panya · OBSERVER_CONFIRMED 2026-09-05T12:48+07:00)
- ชน Prison Exile Island 3 ครั้ง + Spice Paradise Island 3 ครั้ง: **"ไม่มีหน้าต่างอะไรเด้ง"** ทั้งสองเกาะ · ไม่มีข้อความปฏิเสธ · ไม่มี dialog error · client ไม่ปิดตัว · HUD `HP -1/1` ขณะเป็นเรือเหมือน R313 (สังเกตการณ์) · ภาพเกาะ 2 ตอน 12:33:32 ในแชท
### 2.3 อ่านผล + ทางต่อ (static ก่อน ไม่ใช่บูตซ้ำ)
1. **บวก**: layout ของ RE-256 ถูก — `NavigationEx_AddSurveyDataVtial` ผ่าน parser ของ client แล้ว (ปิดข้อสงสัย 50351 ได้)
2. **ลบ**: record + ระยะ ≤37 หน่วย **ไม่เปิดหน้ารายงานกัปตัน** ⇒ กลไก "client เปิดเอง" ไม่พอหรือผิด · สองทางที่ยังไม่ถูกตัด: (ก) **เซิร์ฟเดิมเป็นคนตอบเฟรม 0x1FB2** ด้วยเฟรมสั่งเปิดหน้ารายงาน — §4 ให้น้ำหนักทางนี้: ขอบทะเลใช้เฟรมเดียวกัน (id ต่างกัน) และบนเซิร์ฟเดิมผลคือ**เปลี่ยนฉาก** ซึ่ง client ทำเองไม่ได้ ⇒ เซิร์ฟเดิมต้องตอบ 0x1FB2 อยู่แล้วอย่างน้อยหนึ่งแบบ (ข) เนื้อ record "อ่านออก" แต่ความหมายไม่ใช่ (u16 2/3 · ช่องศูนย์ 3 ช่อง · u64 0) หรือ AddSurveyData ไม่ใช่ตัวเปิดหน้านี้เลย (อาจเป็นข้อมูลรายการ "สำรวจ" ในแผนที่)
3. **พิกัดสำรอง (STOP rule ของใบ)**: ทำไม่ได้บนบิลด์นี้ — `MEASURED_XYZ_BACKUP` "read by no function in this module today" (ไม่มีสวิตช์ · ka1-A ห้ามแตะ src) · และจากตาราง §2.1 ระยะไม่น่าใช่ตัวแปร ⇒ ถ้า LANE-A ยังต้องการปิดทางนี้ เสนอ env `PF_M2_SURVEY_XYZ=primary|backup|both` (`both` = 4 records ในบูตเดียว) — **ห้ามเรียก Panya เพื่อบูต backup อย่างเดียว**
4. งาน static ที่ควรทำก่อนบูตครั้งถัดไป (RE runner/LANE-A): (ก) ในไบนารี client หา UI หน้า "รายงานกัปตัน เรือเทียบท่า" (string table → UI id → caller) แล้วไล่ว่า**อะไรสั่งเปิด** — handler ของ vital ไหน หรือ Lua ตัวไหน (ข) handler ของ `NavigationEx_AddSurveyDataVtial` เก็บลงที่ไหน ใครอ่าน (ค) ตารางทริกเกอร์ของฉาก 126 ใน `gamedata\scene\` — index 2/3/7/35/48/57/69 คืออะไร (§4)

## 3. GT-254 (Slave Market Island · เกาะ 155) → **[NO-RESULT: ไม่พบเกาะ — ไม่อยู่ในฉาก 126]**
- P-A ผ่าน (GT-233 จบ · ยังอยู่ 126 · client มีชีวิต · capture เขียนอยู่) · P-B: `LANE_HOOK_REGISTERED` ไม่อยู่ใน stderr ที่เก็บได้ (พิมพ์ตอน import ก่อน tee) แต่ `LANE_A_TRIGGER_VITAL` 12 บรรทัดพิสูจน์ว่า hook ยิงจริง · ขั้น 1-6 **ไม่ได้ทำ**
- เหตุ (ภาพแผนที่โลกจาก Panya 12:47 · ส่งในแชท): ฉาก 126 "Atlantic Ocean: Rising Sun Sea" มีเฉพาะ **Prison Exile Island · Port Royal · Spice Paradise Island** · **Slave Market Island + Evil Port อยู่ "Atlantic Ocean: Dark Fog Sea"** (= ฉาก 304 ตาม `gm_scene_name_tip.tsv`) · ทะเลอื่น: Taboo Sea (127) Ocean Walled City/Voodoo Island · Pale Silver Sea (305) Silver Harbour · Bermuda Sea (128) Death City Sea/Hell Volcanic Island
- **ข้อเท็จจริงเกม (Panya · เซิร์ฟเดิม)**: "ย้ายไปแมพทะเลที่อยู่ติดกัน ต้องแล่นเรือไปชนขอบแมพด้านนั้น" — ไม่มี NPC/วาป · แผนที่ของ 126 มีลูกศรขอบ**ตะวันตก** (→ Dark Fog Sea) และ**ใต้** (→ Pale Silver Sea ตาม Panya) · ไม่มีลูกศรเหนือ/ตะวันออก
- ⇒ ใบ GT-254 ตั้งอยู่บนสมมติฐานผิด (แถว 155 `BG0004` อยู่ทะเลของฉาก 304) · ต้องมี **กลไกข้ามขอบทะเล** ก่อน (§4) แล้วออกใบใหม่ · ไม่ใช่ความผิดของ GT-233 (เกรดแยกตามใบ)

## 4. ของแถม (ไม่มีใบ · Panya สั่งเก็บเองบนบูตเดียวกัน · capture-only ไม่แตะเซิร์ฟ): **ขอบแมพ 4 ด้าน**
| เวลา | เฟรม | ด้าน/ที่ | id (tag 0x0F) | triple แรก | TargetPos (= HUD) | ชื่อใน dock table (hook) |
|---|---|---|---|---|---|---|
| 12:32:46 | #36 | ใกล้จุดเกิด | **35** | (-739.4, 3257.2) | (-891.1, 3621.4) | Thorn Flower PROP |
| 12:59:47 | #840 | **ขอบใต้** (→ Pale Silver Sea) | **69** | (-892.5, -8383.7) | (-896.6, -8573.8) | Ground Site Entrance PROP |
| 13:02:52 | #932 | ระหว่างทางไปตะวันตก | **57** | (-4511.3, -6278.9) | (-4756.7, -5973.8) | Black Charm Demon Flower PROP |
| 13:03:04 | #938 | **ขอบตะวันตก** (→ Dark Fog Sea) | **7** | (-8093.2, -2850.8) | (-8273.4, -2621.3) | Viper Wicket PROP |
| 13:06:09 | #1030 | ขอบตะวันตก ครั้ง 2 (ถอยแล้วชนใหม่) | **7** | (-8087.2, 627.6) | (-8322.9, 547.4) | Viper Wicket PROP |
| 13:07:38 | #1074 | **ขอบเหนือ** | **48** | (-2393.2, 6413.0) | (-2321.8, 6525.3) | Captive Cage PROP |
| 13:07:40-13:08:40 | — | **ขอบตะวันออก** (Panya ชน 1 ครั้ง) | **ไม่มีเฟรม 0x1FB2** (เช็ค hex ดิบ `12 B2 1F` = 0 ในช่วงนี้) | — | — | — |
- hex เต็ม 4 เฟรมขอบ (ต่างจากเฟรมเกาะเฉพาะ u16 หลัง `0F` และ float):
  #840 `12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 45 00 0B 04 2A F4 20 5F C4 2A B4 FE 02 C6 2A 00 00 3A 43 12 90 2A 0B 00 2A 39 26 60 C4 2A 47 F7 05 C6 2A 00 00 AC 42 2A 54 D2 CB 3F 0B 01 0B 00`
  #938 `… 0F 07 00 0B 04 2A 83 E9 FC C5 2A F7 2C 32 C5 2A 00 00 3A 43 12 90 2A 0B 00 2A 98 45 01 C6 2A F9 D4 23 C5 2A 00 00 AC 42 2A 29 80 81 40 0B 01 0B 00`
  #1030 `… 0F 07 00 0B 04 2A 88 B9 FC C5 2A C4 E8 1C 44 2A 00 00 3A 43 12 90 2A 0B 00 2A B7 0B 02 C6 2A A7 D8 08 44 2A 00 00 AC 42 2A A6 10 34 40 0B 01 0B 00`
  #1074 `… 0F 30 00 0B 04 2A A5 93 15 C5 2A A3 67 C8 45 2A 00 00 3A 43 12 90 2A 0B 00 2A ED 1C 11 C5 2A 36 EA CB 45 2A 00 00 AC 42 2A EF EC A8 40 0B 01 0B 00`
- สิ่งที่วัดได้: (1) **ขอบตะวันตก = เส้น X ≈ -8090 ยิง id 7 ซ้ำได้ 2/2** ที่ Y ต่างกัน 3,478 หน่วย · ขอบใต้ Y ≈ -8384 = id 69 · ขอบเหนือ Y ≈ +6413 = id 48 · ตะวันออกเงียบ (สอดคล้องแผนที่ไม่มีลูกศรตะวันออก — แต่เหนือก็ไม่มีลูกศรและยังยิง 48 ⇒ 48 อาจไม่ใช่ทางออก nonclaim) (2) **triple แรกของ 0x1FB2 ไม่ใช่ตำแหน่งเรือ** — TargetPos (triple สอง) ตรงกับ HUD เป๊ะ (#128 TargetPos (-1466.8,-5368.3) = แผนที่ `X:-1,466 Y:-5,368`) ส่วน triple แรกห่างเรือ ~260-300 หน่วยและเปลี่ยนทุกครั้ง ⇒ น่าจะเป็น**จุดสัมผัส**บน trigger volume (ตอบคำถามค้างของ R308 บางส่วน · nonclaim ว่าเป็นอะไรแน่) (3) id บนสายไม่ตรงเลขฉากปลายทาง (304/305) และไม่ตรง `trigger_tip_th.tsv` (284 "เดินทางสู่ Atlantic-Dark Fog Sea [Lv.30]" · 285/287 Pale Silver Sea [Lv.100]/[Lv.80] · 288/289 "มุ่งหน้าไป…") ⇒ namespace ที่สาม — ชื่อ PROP ที่ hook พิมพ์สำหรับ 7/35/48/57/69 **ห้ามเชื่อ** (หัวใบ hook เขียนเองว่าสอง namespace อาจไม่ใช่อันเดียวกัน)
- เสนอ (LANE-A · COO ตัดสิน): (ก) static: ผูก id 2/3/7/35/48/57/69 กับตารางทริกเกอร์ของฉาก 126 ใน `gamedata\scene\` (ต้นทางจริงของ tag 0x0F) (ข) เปิดใบสร้าง **"ข้ามขอบทะเล"**: เซิร์ฟตอบ 0x1FB2 id 7 → เปลี่ยนฉากไป 304 (Dark Fog Sea) และ id 69 → 305 — ต้องใช้ตัวส่ง "เปลี่ยนฉากสด" ตัวเดียวกับที่ `/warp` สด ต้องการ (LANE-GM · GT-258) ⇒ งานร่วม A+GM (ค) เมื่อ (ข) มี GT-254 ออกใหม่ได้ในฉาก 304 · และ M2 เทียบท่าน่าจะเป็นตระกูลเดียวกัน: เซิร์ฟตอบ id 2/3 ด้วยเฟรมเปิดหน้ารายงาน (ยังไม่รู้ opcode — §2.3 ข้อ 4ก)

## 5. GT-257 (chat 2-vital) → **ไม่ได้ exercise รอบนี้** (ยัง READY พ่วงบูตหน้า)
- เฟรม `/warp 126` 12:25:31 มาแบบ vital เดี่ยว 48 B (Panya พิมพ์หลังอยู่ในแมพนานแล้ว) · `TAIL_UNDECLARED_BODY`=0 · `LANE_GM_CHAT_TAIL`=0 · เงื่อนไขกระตุ้น = พิมพ์คำสั่งทันทีหลังเข้าแมพขณะ client flush UserSetting (R313) — ผู้เทสรอบหน้าต้องพิมพ์**ทันที**หลังเข้าแมพ

## 6. /warp 126 ยัง staged (LANE-GM/LANE-A)
- `GM_CHAT_STAGED_NEXT_LOGIN account='localtest' command=warp scene_id=126 coordinates=none basis=server_believed_scene next='this scene has no confirmed spawn point…'` — ทำงานถูกตามบิลด์ แต่เจ้าของต้องการ**วาปสดไป 126** · คำสั่ง Panya จะมาเป็นจดหมาย PANYA-DECISION แยก (จุดเกิด 126 = client MARKER n_ID 17 (3050,232,90) ที่ `WORLD_SCENE` ใช้อยู่แล้ว)

## nonclaims
- ไม่ตัดสินว่าทำไมหน้ารายงานไม่เด้ง (2.3 ข้อ 2 เป็นสมมติฐานสองทาง) · ไม่ตัดสินรัศมี <37 หน่วย · ไม่ตัดสินความหมายของ triple แรก · ไม่ตัดสินว่า 48 เป็นทางออกเหนือ · ขอบตะวันออก: ยืนยันจากคำ Panya + ไม่มีเฟรมในช่วง 60 วิก่อนปิดเท่านั้น (ไม่มีภาพ) · ไม่ได้ทดสอบพิกัด BACKUP (ไม่มีสวิตช์) · GT-254 ไม่ได้เดินขั้นใด · แผนที่โลกอ่านจากภาพ Panya ไม่ใช่จาก wire

## บทเรียนเครื่องมือ
- teardown EVID `ErrorData = 2` ของรอบนี้คือ token `errordata_if_rejected=50351` ใน `M2_SURVEY_TRIAL_SENT` (grep ไม่แยกตัวพิมพ์) ไม่ใช่ error จริง — template ควร grep `ErrorData=` ตัวพิมพ์ตรง
- ใบที่ตั้งบน "เกาะ X อยู่ในฉาก Y" ต้องเช็คแผนที่โลกของ client ก่อน (ภาพ M ของ Panya ตอบได้ใน 1 นาที) — ประหยัดรอบ attended
- ใบ piggyback ที่ต้องพึ่งการเดินเรือ ควรใส่ "พิกัด/ทิศของเป้า" ให้ผู้เทส — R318 ใช้แผนที่ M แทน (deviation จาก "หมุนกล้องล้วน" ของ GT-254 ขั้น 2 · ไม่กระทบ hex ตอนชน)

-- ka1-A
