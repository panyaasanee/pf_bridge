[ถึง: COO (สะพาน, attended) · cc: Panya | จาก: chief cloud (cc) · รอบ R172 · branch `claude/modest-tesla-lh44g4`]

# 9 ใบที่ค้าง `expired_pending_decision` — หนึ่งหน้า แถวละสามบรรทัด ตามที่สั่ง

เวลา: `2026-08-26T00:15+07:00` · ตอบคำสั่ง `COO-CHARTER-01` ⑤ ข้อ 1
ที่มาของข้อมูล: `pirate-force-server/docs/HYPOTHESIS_LEDGER.json` (เลขบรรทัดกำกับท้ายตาราง)

🔴 **ก่อนอ่านตาราง — รูปแบบเดียวที่ทั้ง 9 ใบมีร่วมกัน ผมเขียนไว้ตรงนี้เพราะมันคือคำตอบจริง:**
> **ทุกใบเป็น *composition ของเรา* ที่ต่อของที่พิสูจน์แยกกันสองชิ้นเข้าด้วยกัน แล้วขาดชิ้นเดียวกันหมดคือ *หลักฐานว่าเซิร์ฟเวอร์ต้นฉบับทำแบบนั้นจริง*** — ซึ่ง **กู้ไม่ได้ตลอดกาล** (เซิร์ฟเวอร์ต้นฉบับปิดไปแล้วและไม่เคยถูก publish)
> ⇒ ทางเลือก "เดินต่อด้วย original traffic" ที่เขียนไว้ในทุกแถว **ในทางปฏิบัติแปลว่า "ไม่มีวันเดินต่อ"**
> ⇒ **ผมเสนอให้เคาะทั้ง 9 ใบด้วยคำตัดสินเดียวกัน: ปิดเป็น harness/transport claim ที่ `production_allowed=false` ถาวร** แล้วเลิกนับมันเป็นของค้าง

| ใบ | สามบรรทัด |
|---|---|
| **HYP-PF-003** | **ถาม:** q3020 op1 → action 6 `OpenAcceptUI` และ op2 → action 1 `Accept_Run` เป็นลำดับที่เซิร์ฟเวอร์จริงส่งหรือไม่<br>**สถานะจริง:** ต่อ client request ordering เข้ากับ action consumer ที่พิสูจน์แยกกัน · ขาด response linkage ของ q3020 ทั้งชุด · frozen V134–V141<br>**ทางเลือก:** ปิดเป็น harness-only claim / เดินต่อด้วย original q3020 traffic *(กู้ไม่ได้)* / ยกเลิก |
| **HYP-PF-004** | **ถาม:** q3020 `Var2=1` + empty 12-byte RuntimeReq เป็น trigger จริงของ MARKER1 TeleportCheck prompt หรือไม่<br>**สถานะจริง:** ต่อ q3020 (data-backed) เข้ากับ prompt ที่พิสูจน์แยกกัน · ไม่มีหลักฐานว่าเซิร์ฟเวอร์จริงเชื่อมสองอันนี้ · frozen V136–V141<br>**ทางเลือก:** ปิดเป็น transport-only prompt / เดินต่อด้วย producer ที่ระบุ trigger+marker+value *(กู้ไม่ได้)* / ยกเลิก |
| **HYP-PF-005** | **ถาม:** หลัง MARKER1 confirm ต้องส่ง TeleportVital v4 ไป scene 1/seq 0 XYZ `(-10322,-755,671)` โดย field อื่นเป็น 0 หรือไม่<br>**สถานะจริง:** พิกัดมาจาก MARKER1 data + wire shape ของ consumer จริง · แต่ field policy ของเซิร์ฟเวอร์จริงไม่มี · frozen V137–V141<br>**ทางเลือก:** ปิดเป็น transport composition เฉพาะจุดหมายนี้ / เดินต่อด้วย producer ที่พิสูจน์ envelope/version/scene/coords *(กู้ไม่ได้)* / ยกเลิก |
| **HYP-PF-006** | **ถาม:** MARKER1 nearest-20 snapshot + P86 target/choose/facing/default-conversation เป็นพฤติกรรมปลายทางที่ถูกหรือไม่<br>**สถานะจริง:** ประกอบจาก frozen placement rows + snapshot ordering เดิม · ไม่มี destination snapshot ของเซิร์ฟเวอร์จริง · frozen V138–V141<br>**ทางเลือก:** ปิดเป็น destination/interaction harness / เดินต่อด้วย traffic ที่พิสูจน์ membership+ordering+identity *(กู้ไม่ได้)* / ยกเลิก |
| **HYP-PF-007** | **ถาม:** direct Scene2 load ใช้ `scene_seq 0` และ `heading 0` ได้หรือไม่ (direction 8 ยัง unmapped)<br>**สถานะจริง:** Grade D transport default รอบ marker position ที่ exact · ขาด mapping direction-8→heading และ producer ของ scene sequence · frozen SCENE-001–006<br>**ทางเลือก:** ปิดเป็น load-harness default / **🎯 เดินต่อด้วย static mapping ได้จริง — ใบนี้ต่างจากอีก 8 ใบ** / ยกเลิก |
| **DIAG-PF-001** | **ถาม:** P60 ใช้ BasicAttr mask `0x070D` กับ HP 3857/3857 (จาก local level-27 data) เป็นค่า diagnostic ได้หรือไม่<br>**สถานะจริง:** runtime พิสูจน์แค่ liveness/target-selection ไม่ได้พิสูจน์ spawn policy · ไม่มี HP policy/scaling ของจริง · frozen SCENE-003–012<br>**ทางเลือก:** ปิดเป็น diagnostic value (ห้าม persist/scale) / เดินต่อด้วย spawn traffic จริง *(กู้ไม่ได้)* / ยกเลิก |
| **GEO-PF-002** | **ถาม:** วางผู้เล่นห่างจาก MOBS34/P60 ที่ `+100X/+50Y` ระนาบ Z เดียวกัน เป็น geometry ที่ยอมรับได้หรือไม่<br>**สถานะจริง:** พิกัด P60 มีหลักฐาน แต่ offset ผู้เล่นเป็น synthetic · `authentic=false` · frozen SCENE-002–006<br>**ทางเลือก:** ปิดเป็น synthetic test geometry (ห้าม publish เป็น world data) / เดินต่อด้วยหลักฐาน co-location จริง *(กู้ไม่ได้)* / ยกเลิก |
| **GEO-PF-003** | **ถาม:** ย้าย P60 ไปพิกัด P144/Jessica แล้ววางผู้เล่นที่ V74 `(0,0,931)` heading 0 เป็น harness ที่ยอมรับได้หรือไม่<br>**สถานะจริง:** พิกัดต้นทางแต่ละตัวมีหลักฐาน แต่การรวมเป็น synthetic · ไม่มี P60 placement จริงใน scene 1 · `authentic=false`<br>**ทางเลือก:** ปิดเป็น camera-visibility harness / เดินต่อด้วย authentic scene-1 placement *(กู้ไม่ได้)* / ยกเลิก |
| **GEO-PF-004** | **ถาม:** pin player `Y=-2830.045166015625`, heading 0 ให้ P0 อยู่ที่ `+100X/+50Y` สัมพัทธ์ ใช้ได้หรือไม่<br>**สถานะจริง:** legacy synthetic geometry รอบ P0 placement ที่ authentic · ไม่มี player location/heading จริงของบทสนทนานี้ · frozen V135–V141<br>**ทางเลือก:** ปิดเป็น P0 conversation reachability harness / เดินต่อด้วยหลักฐาน co-location จริง *(กู้ไม่ได้)* / ยกเลิก |

## สิ่งที่ผมขอให้คุณเคาะ — สองบรรทัด

1. 🔴 **8 ใบ (ทุกใบยกเว้น `HYP-PF-007`): ปิดเป็น harness/transport claim ถาวร `production_allowed=false`** — เพราะเงื่อนไขที่จะปลดมันคือหลักฐานที่ไม่มีวันมี · **ถ้าเห็นด้วย ผมเดินแก้ ledger ให้ในรอบถัดไปทันที ไม่ต้องตอบยาว ตอบว่า "เอาตามที่เสนอ" พอ**
2. 🎯 **`HYP-PF-007` แยกออกมา — มันไม่ตันเหมือนอีก 8 ใบ** สิ่งที่มันขาดคือ **static mapping ของ direction-8 → heading** ซึ่ง **สาย C ขุดจากอิมเมจได้จริง** · และมัน **บล็อก `BUILD-002`/M2 โดยตรง** (ฉากที่สองต้องรู้ seq/heading ตอนโหลด)
   ⇒ **ผมเสนอให้ยก `HYP-PF-007` ขึ้นเป็นใบของสาย C ที่บล็อก M2 แทนที่จะเป็นใบค้าง** — นี่คือใบเดียวใน 9 ใบที่มี BUILD_IMPACT จริง

## nonclaims
- ผม **ไม่ได้แก้ ledger ในรอบนี้** — ตารางนี้เป็นข้อเสนอ ไม่ใช่การเปลี่ยนสถานะ
- ตัวเลข `tracked_versions` ของทุกใบ **ถึงหรือเกินเพดาน `max_versions: 5`** และทุกใบมี `extension_approval_ref: null`
- บรรทัด "กู้ไม่ได้ตลอดกาล" อ้างจากคำยืนยันของเจ้าของ 2026-08-18 (เซิร์ฟเวอร์ต้นฉบับปิดและไม่เคยถูก publish) **ไม่ใช่สิ่งที่ผมวัดเอง**
