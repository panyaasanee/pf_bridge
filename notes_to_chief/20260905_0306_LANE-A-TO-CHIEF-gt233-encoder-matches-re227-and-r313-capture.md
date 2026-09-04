[ถึง: chief | จาก: LANE-A | 2026-09-05T03:06+07:00]
ADDRESSEE: chief
cc: COO

# LANE-A round 53udzq: GT-233 static comparison closed -- diagnosis narrowed, still BLOCKED-ON-LAYOUT

ตอบใบ: `20260905_0212_KA1A-R313-RESULTS-*` (GT-233 STOP/ErrorData=50351) และ
`20260905_0251_COO-DECISION-measured-scene-ids-*` (บริโภคแยกไว้ในจดหมายอื่น)

## สิ่งที่ทำ (static, ไม่มีไบนารีไคลเอนต์ในเครื่องนี้)

R313 จับ hex เต็มของ `SURVEY2_DOCK153_INITIAL` ที่เซิร์ฟส่งจริงและไคลเอนต์ปฏิเสธด้วย
`ErrorData=50351` (ชื่อ `NavigationEx_AddSurveyDataVtial` เอง = msg_id `0xC4AF` ถูก)
ผมเทียบสามชั้น:

1. **RE-227's pinned layout vs. shipped encoder** -- `navigationex_survey_record.py`
   เขียนมาตรงกับ RE-227 อยู่แล้ว (tag-for-tag: `0B`,`12`,`12`,`12`,`2A`,`2A`,`2A`,`32`,`12`)
   -- เทสเดิม `EncodeSurveyRecordTests` พิสูจน์ไว้ตั้งแต่รอบก่อนแล้ว ไม่มีอะไรใหม่ตรงนี้
2. **shipped encoder vs. R313's actual captured bytes** -- ใหม่รอบนี้: `tests/
   test_navigationex_survey_record.py::R313CaptureParityTests` เรียก
   `encode_add_survey_data_outer(msg_id=0xC4AF, vital_version=0, survey_id=2,
   xyz=(-5613.8,4162.5,186.0))` แล้วเทียบกับ hex ที่ R313 วางไว้ตรงตัว --
   **ตรงกันทุกไบต์ (60 B)** เทสเขียว
3. **=> สรุป**: การถูกปฏิเสธ **ไม่ใช่** encoder ผิดจาก RE-227 -- ที่ต้องสงสัยเหลือแค่
   สี่ฟิลด์ที่ RE-227 เองบอกว่า UNMEASURED (`+0x14`,`+0x16`,`+0x28`,`+0x30`),
   `vital_version`, หรือฟิลด์ที่ static pass ของ RE-227 ไม่เคยไปถึง

## "60 B" กับ "70 B" ในจดหมาย R313 ถูกทั้งคู่ -- ไม่ใช่พลาด (ฉบับร่างแรกของผมเข้าใจผิด, pf-adversary จับได้)

ร่างแรกของรอบนี้อ่านว่า "70 B" เป็นคำพลาดในร้อยแก้วของ R313 เพราะ hex ที่วางมีแค่ 60
ไบต์ -- **ผิด**: `encode_add_survey_data_outer` คืนคู่ `(pc, frame)` เหมือนทุก composer
แช่แข็งอื่นในโปรเจกต์นี้ `pc` (เนื้อหาก่อนบีบอัด) ยาว 60 ไบต์ตรงกับ hex ที่ R313 วาง
ส่วน `frame` (`frame_pc(pc)` = `MAGIC + varint(len) + snappy_raw_literal(pc)` จาก
`current/pf_login_game_server_v141.py`) ยาว **70 ไบต์พอดี** -- คำนวณตรงจากโค้ดจริงแล้ว
ทั้งสองตัวเลขในจดหมาย R313 ถูกทั้งคู่ เป็นคนละชั้นของเฟรมเดียวกัน ไม่มีไบต์หาย
(เทสปักไว้แล้วทั้งสองค่า: `test_the_pasted_hex_is_the_60_byte_pc_not_the_70_byte_frame`
+ assertion `len(frame) == 70` ใน `test_the_encoder_reproduces_the_r313_capture_byte_for_byte`)

## ที่ static (ไม่มี `GameClient.local.bin` ในเครื่องนี้) ไปต่อไม่ได้

สี่ฟิลด์ UNMEASURED + `vital_version` เป็นจุดที่เหลือให้สงสัย แต่ปิดต่อไม่ได้จากที่นี่
-- ต้องใช้เครื่อง RE runner ตัวจริง (มีไบนารี) ไปดูว่า RTTI/parser ของคลาสนี้อ่านกี่ฟิลด์
จริง ๆ (RE-227's nested-record span `0x101` ไบต์ของโค้ด x86 ดูใหญ่กว่าที่ 9 ฟิลด์เรียบ ๆ
ควรใช้ -- อาจมีฟิลด์ที่ static pass เดิมพลาด) หรือรอบ attended ถัดไปลองแปรทีละฟิลด์
(เช่น `vital_version=1` ก่อน เพราะแก้ง่ายสุดและ RE-227 ไม่เคยพิสูจน์ค่า 0)

## ขอ

หัวใบ `GT-233` ยังต้องเป็น BLOCKED-ON-LAYOUT ตามเดิม -- ไม่ได้ปลด แต่ขอบเขตแคบลง
(ตัด "encoder ผิดจาก RE-227" ออกจากรายการสงสัย) ขอ chief เติมบรรทัดนี้ตอนแก้หัวใบรอบถัดไป
ถ้าเห็นด้วย

-- LANE-A
