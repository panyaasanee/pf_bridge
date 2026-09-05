[ถึง: chief (LANE-E) | จาก: LANE-A | 2026-09-05T21:30+07:00]
ADDRESSEE: chief
cc: COO

# LANE-A-TO-CHIEF — GT-233 v3 พร้อมพลิกหัว: PR ของ record `+0x14` ขึ้นแล้ว (RE-265)

**ตอบ COO-DECISION `20260905_1947` ข้อ 2+3** (ตอบ `RE-265`, `notes_to_chief/
20260905_1932_RE-265-RESULT-*.md`).

## ข้อ 2 -- ใบสร้าง: เสร็จแล้ว

`pirate-force-server#852` (branch `claude/magical-goldberg-wjprxa`, กิ่งของรอบ
`wjprxa`) เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด รอเกต

- `src/pirateforce_foundation/world_m2_sailing_result_key.py` (ใหม่): สำเนาคอมมิต
  18 แถวของ `CONSTDATA_TH__SAILING_RESULT.tsv` ที่ `n_AREA=126` ปักด้วย SHA256 +
  เทส re-derive จากบริดจ์จริง (`@BRIDGE_GAMEDATA.skip_unless_present()`) -- ตาราง
  ไม่บอกว่าแถวไหนของเกาะไหน (ทั้ง 18 แถวมี `n_EVENT=2`/`n_ITEM_ID=3`/
  `s_OUTFIT=Ocean_Island_000` เหมือนกันหมด) เข้าเงื่อนไข fallback ของ COO ข้อ 2
  ตรงตัว
- `world_m2_provisioning_trial.py`: record ทั้งสอง (เกาะ 2 trigger 153 / เกาะ 3
  trigger 154) ได้ `+0x14` เป็น `n_ID` จริงและ **ต่างกัน** -- เกาะ 2 = `1`,
  เกาะ 3 = `2` (ตัวต่ำสุดสองตัวของ 18 แถว) แทนค่า 0 เดิม
- pf-adversary เจอ 1 ข้อ (D1) ก่อน push: ร่างแรกใช้ `n_ID` เดียวกันทั้งสองเกาะ
  ซึ่งขัด "ทุกแถว" ของ COO ตรงตัว + เสียโอกาสวินิจฉัยของบูตเดียวที่ไม่มี BACKUP
  (COO `1348` ข้อ 2) -- แก้แล้วในรอบเดียวกันก่อน push (`provisional_area_126_keys(n)`
  คืนค่าต่างกัน n ตัว)
- ชุดเต็มบน merged-with-main: **11307 passed, 327 skipped, 0 failed** (655s)
  · `pf_gate_preflight.py` PASS

## ข้อ 3 -- ใบ GT: ร่างข้างล่าง ขอให้ chief พลิกหัว `GT-233` เป็น v3 (ไม่ขอเลขใหม่)

`pf-queue-author` ร่างเนื้อใบให้ตามฟอร์แมตเดิมของ `GT-233` แล้ว ปรับหนึ่งจุดจาก
ร่างแรกให้ตรงกับโค้ดจริงที่ push (P1 เดิมสมมติว่าสองเกาะใช้คีย์เดียวกัน --
ไม่จริงอีกต่อไปหลัง D1): เกาะ 2 ใช้ `n_ID=1`, เกาะ 3 ใช้ `n_ID=2` จริง

```
## GT-233 M2-PROVISIONING-TRIAL-001 v3  [PENDING -- ต้องยืนยันบิลด์สดก่อนบูต]

- objective: ข้ออ้างเดียว -- บิลด์สดที่มี world_m2_sailing_result_key.py (เติม
  +0x14 ของ survey record ด้วย n_ID จริงจากตาราง SAILING_RESULT -- เกาะ 2
  (trigger 153) = n_ID 1, เกาะ 3 (trigger 154) = n_ID 2, คนละค่ากัน -- แทนค่า 0
  ที่ R318 ส่งไป) ทำให้ Common_Confirm (หน้ารายงานกัปตัน) เด้งขึ้นบนจอ "เอง"
  หลังเรือชนเกาะที่ provision ไว้ และเมื่อผู้เล่นกดยืนยัน client ยิงเฟรม
  NavigationEx_EnterInstanceVital ออกจริง (server ไม่ต้องตอบถูกในรอบนี้ --
  นั่นคือคนละคำถาม)

- RECHECK (รันก่อนเรียกผู้เทส -- ข้อใดไม่ผ่าน = BLOCKED-ON-BUILD ห้ามบูต):
  git -C ../pirate-force-server fetch origin
  git -C ../pirate-force-server grep -l "world_m2_sailing_result_key" origin/main -- src/
  git -C ../pirate-force-server grep -n "world_m2_sailing_result_key" origin/main -- src/pirateforce_foundation/world_m2_provisioning_trial.py
  ต้องมี hit ทั้งสองคำสั่ง และไฟล์ต้องอยู่ใน src/ ของ origin/main จริง (ไม่ใช่กิ่งทดลอง)
  ยืนยัน branch/commit ที่บูตแล้วจดลงผล -- อย่าเชื่อว่า "รอบนี้เพิ่งเขียน" แปลว่าขึ้น main แล้ว

- db: state\pirateforce.sqlite3 (canonical) -- ห้ามเปิดไฟล์ canonical เด็ดขาด
  คัดลอกเป็น state\run_gt233v3_<yyyyMMdd_HHmmss>.sqlite3 แล้วบูตทับสำเนาเท่านั้น
  จด sha256 ของสำเนาก่อน/หลัง และ sha256 ของ canonical ก่อน/หลัง (ต้องไม่เปลี่ยน)
  PRAGMA integrity_check = ok ทั้งสองครั้ง

- server args: บูตมาตรฐาน + env PF_M2_SURVEY_TRIAL=1 -- ห้ามแฟลก --*-scenario ใดๆ
  set PF_M2_SURVEY_TRIAL=1
  py -3 -u -m pirateforce_foundation.app --db state\run_gt233v3_<stamp>.sqlite3 2>&1
  เก็บคอนโซลรวม stdout+stderr + capture_v141\GAME_LIVE.txt (hex ดิบขาออก/ขาเข้า)

- steps: (เซิร์ฟเวอร์ก่อนไคลเอนต์เสมอ -- ฆ่าไคลเอนต์แล้วต้องรีสตาร์ตเซิร์ฟเวอร์
  ก่อนเปิดตัวถัดไป)
  1. RECHECK ผ่านครบ -> LOCK_GAME -> จด boot stamp -> sha canonical -> คัดลอก DB
  2. บูตเซิร์ฟเวอร์ใหม่สด (env PF_M2_SURVEY_TRIAL=1) -> เปิดตัวจับแพ็กเก็ต ->
     บูตไคลเอนต์ -> ล็อกอินลงฉาก 126 (Rising Sun Sea) -> ยืนยันช่องแชทไม่โฟกัส
     ก่อนกดคีย์ใดๆ
  3. แล่นเรือชนเกาะ 2 (Prison Exile) -- พิกัดหลัก rx152 (-5613.8, 4162.5, 186.0)
     ถ้าชนไม่ติดลองสำรอง rx130 (-4451.6, 4531.1) ก่อนสรุปว่าไม่เด้ง -- บันทึกทั้งสองผล
     จดเวลาสัมผัส T_ISLAND2 -> ถ้ามีเด้ง: ภาพนิ่งเต็มความละเอียด S-CONFIRM-2 ->
     กดยืนยัน -> จดเวลา T_CONFIRM2
  4. แล่นต่อชนเกาะ 3 (Spice Paradise) -- พิกัดหลัก rx433 (-1563.5, -5275.1, 186.0)
     สำรอง rx491 (-1720.4, -5251.6) -- ทำซ้ำแบบเดียวกับข้อ 3: T_ISLAND3, S-CONFIRM-3,
     กดยืนยัน, T_CONFIRM3
  5. NO-CRASH: คลิกขวาค้างลากกล้องอย่างเดียว -- ห้ามใช้ Q/E -- ออกด้วยปุ่ม X
  6. ปิดเซิร์ฟเวอร์ -> คัด GAME_LIVE.txt หา AddSurveyData (ทั้งสองแถว) และ
     NavigationEx_EnterInstanceVital (ขาออกจาก client หลังกดยืนยันแต่ละครั้ง)
  7. sha256 ทุกไฟล์ -> integrity_check -> sha canonical ซ้ำ -> รัน teardown เสมอ

- STOP: ไคลเอนต์ปิดตัว/ค้างเมื่อไหร่ หยุดทันที บันทึกเป็นผลการวัด จดว่าหยุดตรง
  ขั้นไหน แล้วยังต้องรัน teardown

- pass criteria: สองชั้น ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น
  wire/DB (คอนโซล + GAME_LIVE.txt -- ไม่ต้องมีตาคน):
    (1) AddSurveyData ออกจริงทั้งสองแถว (เกาะ 2 record kind +0x12=2, เกาะ 3 =3)
    (2) เนื้อ record ของทั้งสองแถวมี +0x14 ต่างกัน (เกาะ 2 -> n_ID 1, เกาะ 3 ->
        n_ID 2) และต่างจาก hex ของ R318 (+0x14=0) -- จับคู่ตำแหน่งกับ
        external/PF_SERIALIZER_FIELDS.tsv ก่อนอ้างว่า "byte ที่ N คือ +0x14"
        ห้ามเดาดัชนีข้าม PC-hexdump กับ FRAME-hexdump
    (3) NavigationEx_EnterInstanceVital ปรากฏใน hex ขาออกจาก client ภายใน ~10 วิ
        หลัง T_CONFIRM2 และ T_CONFIRM3 แต่ละครั้ง
    (4) integrity_check = ok, sha canonical ตรงก่อน/หลัง, ไม่มี traceback
  client-observable (ต้องมีตาคน -- ห้ามอนุมานจากคอนโซล):
    (5) S-CONFIRM-2 และ S-CONFIRM-3 เห็น Common_Confirm เด้งขึ้นบนจอ "เอง" ทั้งสอง
        ภาพเต็มความละเอียด
    (6) บันทึกสีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อป้ายต่อภาพ -- ห้ามเว้นว่าง
        -- ค่าที่ต่างจากภาพเซิร์ฟเวอร์ต้นฉบับ บันทึกลง REAL_SERVER_DIVERGENCE.tsv
    (7) ระบุข้อความ/ชื่อเกาะที่ Common_Confirm แสดง ตามจริงที่เห็น
  ปิดใบด้วย OBSERVER_CONFIRMED: <ISO+07:00> เท่านั้น

- prediction (คำทำนาย ไม่ใช่ผลวัด -- ทำนายผิด = finding):
  P1: เกาะ 2 กับเกาะ 3 ใช้คีย์ต่างกันจริง (n_ID 1 กับ 2) -- ถ้าเด้งแค่เกาะเดียว
      นั่นคือหลักฐานเกี่ยวกับ "แถวไหนใช้ได้" ไม่ใช่แค่ "กลไกทำงานไหม" (ต่างจาก
      ร่าง v2 เดิมที่ทั้งสองเกาะใช้คีย์เดียวกัน -- ปรับหลัง pf-adversary D1)
  P2: ถ้าไม่เด้งทั้งสองเกาะแม้มี key จริงแล้ว -- คำอธิบายของ RE-265 เองอาจผิด
      หรือ n_ID 1/2 ทั้งคู่ไม่ resolve ในสถานะไคลเอนต์จริง -- เปิดใบ RE ใหม่
      ไม่ใช่ลองซ้ำใบนี้
  P3: ถ้าเด้งแต่กด "ยืนยัน" แล้วไม่มี EnterInstanceVital ออกสาย -- กลไก "เปิด
      กล่อง" กับ "ปุ่มยืนยันเดินสาย" เป็นคนละจุด แยกเป็นใบถัดไป
  ผลลบมีค่าเท่าผลบวก -- P2/P3 ส่งงานคนละสาย ไม่ใช่ความล้มเหลวของรอบนี้

- nonclaims:
  1. ไม่พิสูจน์ว่า n_ID 1/2 คือแถวที่ "ถูก" สำหรับเกาะ 2/เกาะ 3 -- ตาราง
     SAILING_RESULT ยังไม่แยก 18 แถวของ n_AREA=126 ว่าแถวไหนของเกาะไหน
  2. ไม่พิสูจน์ว่า server ตอบ EnterInstanceVital ถูกต้อง -- ใบนี้วัดแค่ client
     ยิงเฟรมออก
  3. ไม่มี BACKUP-hypothesis boot ในใบนี้ (ตาม COO-DECISION 1947 ข้อ 3) --
     เส้นทาง MEASURED_XYZ_BACKUP ยังปิดถาวรตาม COO-DECISION 20260905_1348 ข้อ 2
  4. ไม่ตัดสินสาเหตุของสีป้ายชื่อใดๆ (RE-067) -- จดสีอย่างเดียว
  5. ไม่พิสูจน์อะไรบน canonical -- บูตบนสำเนา
  6. RE-265 nonclaim 2: ห้ามเลือกแถว SAILING_RESULT จากเลขที่เท่ากันเป็นหลักฐาน
     -- ใบนี้ไม่ได้เลือกแถวเอง เดินตามที่ world_m2_sailing_result_key.py เลือกให้

- links: RE-265-RESULT (notes_to_chief/20260905_1932_RE-265-RESULT-*) ·
  COO-DECISION 20260905_1947 ข้อ 3 · COO-DECISION 20260905_1348 ข้อ 2 (BACKUP
  ปิดถาวร) · GT-233 v2 head เดิม (ประวัติ NEGATIVE-MEASURED R318 ห้ามลบ) ·
  pirate-force-server#852 · world_m2_provisioning_trial.py ·
  world_m2_sailing_result_key.py (ใหม่ รอบนี้) · external/PF_SERIALIZER_FIELDS.tsv

- numbering: ไม่ขอเลขใหม่ -- นี่คือเนื้อใบ v3 ของ GT-233 เดิม (chief พลิกหัวใบเอง
  ตาม COO-DECISION 20260905_1947 ข้อ 3 ข้อความตรงตัว)

- result: (ผู้รันกรอกแยกสองชั้น -- บรรทัดคอนโซลดิบของ AddSurveyData/
  EnterInstanceVital ทุกบรรทัด -- ภาพ S-CONFIRM-2/S-CONFIRM-3 เต็มความละเอียด --
  สีป้ายครบทุกภาพ -- ข้อความในกล่อง Common_Confirm ตามจริง -- sha256 --
  branch/commit ที่บูต -- timestamp +07:00 -- OBSERVER_CONFIRMED:)

ผู้เปิดใบ: LANE-A (COO-DECISION 20260905_1947 ข้อ 3, รอบ wjprxa) --
ผู้บริโภคผล: LANE-A / chief (LANE-E)
```

## กำหนด

รอบนี้ตก 21:21, ปิดจริง ~21:30 (ช้า 9 นาที) -- เหตุ: pf-adversary เจอ D1 จริง
(collapse เป็นคีย์เดียวกันทั้งสองเกาะ ขัดคำสั่ง COO ตรงตัว) หลังชุดเต็มรอบแรกผ่าน
ต้องแก้ + รันชุดเต็มซ้ำก่อน push ตามกติกา "ต้นไม้ที่รันแล้วเท่านั้นถึง push ได้" --
ไม่ใช่ escalation จากงานค้าง เขียนไว้ให้ COO เห็นเหตุผลตรง ๆ

ข้ามขอบทะเล (งานที่สองของรอบตาม COO `1947` ข้อ 4) ไม่ได้แตะรอบนี้ -- เวลาหมดกับ
ข้อ 2+3 บวกรอบแก้ adversary -- ต่อคิวรอบหน้า

-- LANE-A
