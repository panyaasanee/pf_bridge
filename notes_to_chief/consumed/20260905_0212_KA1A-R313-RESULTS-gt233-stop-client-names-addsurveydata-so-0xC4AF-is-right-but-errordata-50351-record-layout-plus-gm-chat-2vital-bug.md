# KA1A-R313-RESULTS — GT-233 = STOP/NEGATIVE-MEASURED: client รู้จักชื่อ NavigationEx_AddSurveyDataVtial (msg_id 0xC4AF ถูก) แต่ถอดเนื้อ record ไม่ผ่าน ErrorData=50351 → dialog error ก่อนได้ชนเกาะ · + บั๊ก GM chat 2-vital
ADDRESSEE: chief
cc: LANE-A (เจ้าของใบ/ผู้บริโภคผล) · LANE-GM (บั๊กแชท 2 vital) · COO · ka1-B
ผู้เขียน: ka1-A (ผู้เทส attended · Panya ขับ UI เอง) · เวลา 2026-09-05 02:12 +07:00 (ประมาณ)
รอบ: R313 · boot 01:59:59-02:09:57 · BOOT_COMMIT `c055dbc6e9c211828cce3ac609878532c40d57ac` (เขียวล่าสุด · ต่างจากหัว main `2a71c0a5` 2 ไฟล์: `legacy_bridge.py`, `persistence_scene_field_patch.py` — ไม่เกี่ยว M2) · **command line ไร้ธง** · สวิตช์ = env `PF_M2_SURVEY_TRIAL=1` ใน process เซิร์ฟเท่านั้น (job 1510 ตั้งก่อน Start-Process แล้วลบทิ้ง) · run DB `state\run_gt233_20260905_015959.sqlite3` (ทิ้ง) · **canonical sha ไม่เปลี่ยน** `4FF37060…8454` · jobs 1510 boot / 1511,1511b relaunch / 1512 teardown / 1513 release · capture `GameClient\capture_r313_20260905_015959\` · pytest ในทรี 101 passed (test_m2_survey_trial, test_navigationex_survey_record, test_world_m2_provisioning_trial, test_world_m2_survey_plan)

## 1. ลำดับเหตุการณ์
- 02:01 login Arena01 ฉาก 1 → พิมพ์ `/warp 126` ครั้งแรก 02:01:58 **ไม่ถูกรับ** (ดู §3) → พิมพ์ซ้ำ 02:04:34 รับ: `LANE_GM_CHAT_ACTION warp route=action` + `GM_CHAT_STAGED_NEXT_LOGIN … scene_id=126 … next login staged` → X
- 02:06 relaunch (1511b) → login → `WORLD_SCENE scene_id=126 … name=Atlantis … sent_before=NO` · `WORLD_SCENE_RELOCATED … used=(3050,232,90)` · census 37 actors
- `M2_SURVEY_TRIAL_SENT scene=126 records=2 msg_id=0xC4AF version=0 confirmed=none guess=0` (ตอน StartGame) แล้ว `… confirmed=126 guess=0` อีกครั้งหลัง TeleportVital ⇒ ส่งจริง **8 เฟรม** (SURVEY2_DOCK153 INITIAL/REAPPLY + SURVEY3_DOCK154 INITIAL/REAPPLY × 2 รอบ) ทุกเฟรม 70 B late ≤31 ms
- ~02:07:20 (ก่อน Panya ขยับเรือไปชนอะไร · เธออยู่ที่ X:3,088 Y:271 ใกล้จุดเกิด) **client เด้ง dialog Error**:
  `網路 VitalData 讀取失敗 --- NavigationEx_AddSurveyDataVtial ErrorData=50351, 請洽程式設計人員`
  ("อ่าน VitalData จากเครือข่ายล้มเหลว — NavigationEx_AddSurveyDataVtial ErrorData=50351 กรุณาติดต่อโปรแกรมเมอร์") · ภาพ `GameClient\Data\ScreenShot\20260905_0207xx.png` (ส่งในแชทแล้ว) · STOP ตามกติกาใบ · Panya กด OK แล้วปิดเกม 02:09
- ไม่ได้ชนเกาะ · ไม่มี TriggerVital 0x1FB2 · ไม่มี EnterInstance · ไม่มี LANE_A_ENTER_INSTANCE (ตามคาด — ยังไม่ถึงขั้นนั้น)

## 2. ผล GT-233 → เสนอ **[STOP / NEGATIVE-MEASURED — ห้ามบูตซ้ำจนแก้ layout]**
### wire/DB
- เฟรม AddSurveyData ออกจากเซิร์ฟจริง (hex เต็ม SURVEY2_DOCK153_INITIAL 70 B · console บรรทัด 4168):
  `12 9D 6E 14 00 00 00 00 08 04 0B 02 12 01 00 12 AF C4 0B 00 0B 01 12 02 00 12 00 00 12 00 00 2A 66 6E AF C5 2A 00 14 82 45 2A 00 00 3A 43 32 00 00 00 00 00 00 00 00 12 00 00 0B 00`
  = envelope v4 · vital `0xC4AF` · `0B 00` (vital_version 0) · `0B 01` · u16 2 · u16 0 · u16 0 · f32 -5613.8 · f32 4162.5 · f32 186.0 · u64 0 · u16 0 · `0B 00` (change mask)
  SURVEY3 ต่างเฉพาะ u16 3 + XYZ (-1563.5, -5275.1, 186.0) — พิกัดชุดหลัก (rx152/rx433) ตาม COO 1345
- ไม่มี Traceback/TypeError ฝั่งเซิร์ฟ (ตัวบล็อก `player_scene_id` ของ #763 ผ่านจริง) · integrity ok · FK 0 · canonical ไม่เปลี่ยน
### client-observable (Panya · OBSERVER_CONFIRMED 2026-09-05T02:08+07:00)
- dialog Error ข้อความข้างบน เด้งกลางจอไม่กี่วินาทีหลังเข้าทะเล · HUD ขึ้น `HP -1 /1` ขณะเป็นเรือ (สังเกตการณ์ — ไม่รู้ว่าเกี่ยวหรือเป็นของเดิม) · ไม่มีหน้ารายงานกัปตัน (ยังไม่ได้ชน)
### อ่านผล (แยกชั้น)
1. **บวก**: client แปลง msg_id `0xC4AF` เป็นชื่อ `NavigationEx_AddSurveyDataVtial` ในข้อความ error เอง ⇒ **เลข id ถูก** (hash typo-included พิสูจน์บนจอแล้ว) — ตัดข้อสงสัย "id ผิด" ทิ้งได้
2. **ลบ**: เนื้อ record ไม่ตรงที่ client คาด → `ErrorData=50351` (คนละรหัสกับ `28317` = envelope ขาด `0B 00`) ⇒ ปัญหาอยู่ที่ **layout ฟิลด์ใน record / vital_version** ไม่ใช่ envelope และไม่ใช่ XYZ (client ยังไม่ทันดูพิกัด)
3. เสนอทางถัดไป **static ก่อน attended**: client เอ่ยชื่อคลาสเอง ⇒ RTTI `.?AVNavigationEx_AddSurveyDataVtial@@` + reader ของมันหาได้ตรง ๆ ในไบนารี (RE runner/LANE-A: ไล่ parser ของคลาสนี้ให้ได้ลำดับ tag/ชนิดฟิลด์ที่มันอ่าน แล้วเทียบกับ 70 B ข้างบน) · ถ้าจะลอง `vital_version` อื่นก่อน (ใบบอกให้แปรก่อนสงสัยกลไก) ควรทำ**หลัง**รู้ layout — ไม่งั้นเสียรอบ attended ทีละค่า · ไม่ควรเรียก Panya จนกว่า record ผ่าน parser ของ client (เกณฑ์ปลด: static พิสูจน์ layout หรือ RE-234 ทางสำรอง)

## 3. บั๊ก LANE-GM: คำสั่งแชทที่มาแบบ 2 vital ในเฟรมเดียวถูกทิ้ง
- 02:01:58 client ส่ง frame #8 171 B = vital `0xAC52` (แชท `/warp 126`, UTF-16) **+ vital `0x0F01` UserSetting_UpdateServerSettingVital ต่อท้ายในเฟรมเดียว** → `LANE_GM_CHAT_TAIL reason=tail_unknown_vital_id tail_vitals=0 ids=none chat_bytes=none payload_bytes=151 vital_count=unavailable` → คำสั่ง**ไม่ถูกทำ** (DB ยังฉาก 1 · ไม่มี GM_CHAT_STAGED)
- 02:04:34 พิมพ์ซ้ำ (รอ ~5 วิหลังเข้าแมพ) เฟรม 48 B เดี่ยว → รับปกติ
- เกิดเมื่อพิมพ์ทันทีหลังเข้าแมพขณะ client กำลัง flush การบันทึกค่า UI (เฟรม UserSetting ออกทุกครั้งที่เปิด/ปิดหน้าต่าง — เห็นซ้ำใน R312) · ผลกระทบ: ผู้เล่น/ผู้เทสพิมพ์คำสั่งแล้ว "เงียบ" โดยไม่มีข้อความบอก · เสนอ LANE-GM ให้ตัวอ่านแชทวนทุก nested vital (parser เราเอง `DISPATCH_NESTED_VITALS … parse_outer decodes the first nested vital only`) — จุดเดียวกับที่ทำให้ R312 เห็น CLearnSkillVital ผิดเป็น "เฟรมเดี่ยว"
- hex #8: `12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 52 AC 0B 00 48 00 00 00 00 48 12 00 00 00 2F 00 77 00 61 00 72 00 70 00 20 00 31 00 32 00 36 00 12 01 0F 0B 00 0B 01 0B FF 32 00×8 26 FF FF FF FF 0B 19 0B 00 0B 00 05 01 32 00×8 26 01 00 00 00 0B 0C 0B 0C 0B 0C 0B 03 08 01 2A E3 64 30 3F 2A 5E AE 5E 3F 0B 02 0B 04 0B 00 32 6F 00×7 0B 04 0B 01 32 6E 00×7 08 02 2A E3 64 30 3F 2A FF 04 53 3F 0B 00 08 03 2A E3 64 30 3F 2A A0 5B 47 3F 0B 00 0B 00`

## nonclaims
- ไม่ตัดสินว่าฟิลด์ไหนใน record ผิด · ไม่ตัดสินว่า vital_version 0 ผิด · ไม่ตัดสินว่า client ปิดตัวเองหลัง OK (Panya กด OK แล้วปิดเอง — ไม่ได้รอดู)
- ไม่ได้ทดสอบพิกัดสำรอง (ไม่ถึงขั้น) · ไม่ได้ชนเกาะ · RE-227 ไม่ถูกหักล้าง (client ไม่เคยได้ record ที่อ่านออก)
- `HP -1 /1` บนเรือ: สังเกตการณ์อย่างเดียว ไม่เทียบกับ R308

## บทเรียนเครื่องมือ
- ใบ GT-233 อ้าง token `[G>] M2_SURVEY_TRIAL_SURVEY2_DOCK153_INITIAL` — token สร้างจาก f-string จึง grep ในซอร์สไม่เจอ (0 hit) แต่มีจริงบน console (1506/1510 informational เท่านั้น ไม่ abort)
- job relaunch แบบรอ GameClient=0 สูงสุด 40 วิ (1511) ใช้ได้ดี ไม่ต้องวางซ้ำ
- ผู้เทสควร**รอ ~5 วิหลังเข้าแมพก่อนพิมพ์คำสั่ง GM** จนกว่า LANE-GM แก้ §3

-- ka1-A
