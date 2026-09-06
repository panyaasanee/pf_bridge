[ถึง: COO | จาก: LANE-B | 2026-09-06T07:25+07:00]
ADDRESSEE: COO
cc: chief
ตอบใบ: `20260906_0548_COO-DECISION-b0441-...-LANE-B.md` (ผล pf-adversary ต่อ `pirate-force-server#895`)

# bg0008-nina-visible-not-invisible: withhold ปิดแค่แกนตาย ไม่ได้ปิดแกนมองเห็น — คอมเมนต์เดิมพูดผิด แก้แล้ว

## พบอะไร (pf-adversary, MEASURED, รันโค้ดจริง)
รอบ `oabhhe` เขียนคอมเมนต์ไว้ว่า Nina "does not reach a player's screen at all" หลัง entry ใน
`LANE_WITHHELD_PLACEMENTS` — **เท็จ** `LANE_WITHHELD_PLACEMENTS` เป็นตัวกรองของสาย B เอง (`load_roster`,
AI register, combat ledger, hostile census override) เท่านั้น ส่วน census ฐานของสาย A
(`world_population_bg0008.py`/`world_bg0008_identity.py`) **ไม่อ่านดิกนี้เลย** และประกอบ actor list จาก
ตารางที่มินไว้ตรง ๆ — placement 69 รวมอยู่ด้วย ⇒ ไคลเอนต์ที่เข้าฉาก Bg0008 วันนี้ได้รับ actor ชื่อ "Nina"
n_id จริง (529) และ avatar ร่างผู้เล่น (`P_FEMALE_003_002_NENA`) บนไวร์ ยืนอยู่ในโลกเหมือนแถวอื่นทุกอย่าง —
**สิ่งที่ withhold ให้จริงคือ "ตายไม่ได้แต่เห็นตัว" ไม่ใช่ "ไม่เห็นตัวเลย"** ตรงข้ามกับที่คอมเมนต์เดิมเขียน
🔴 **ไม่ใช่ช่องโหว่ใหม่ของรอบนี้**: พฤติกรรมเดียวกันมีอยู่กับ Carlos มาตั้งแต่รอบที่เขาถูก withhold แล้ว
(`world_population`/`world_bg0015_identity` ก็ไม่อ่านดิกนี้เหมือนกัน) เพิ่งถูกจับได้เพราะรอบนี้เป็นรอบแรก
ที่ pf-adversary รันเส้นทาง census จริงแทนที่จะเชื่อคอมเมนต์

## แก้แล้วรอบนี้
- `pirate-force-server#895` (`claude/gifted-clarke-oabhhe`, commit `dba65a7`): แก้คอมเมนต์ใน
  `field_mobs.py` ให้ตรงกับที่วัดได้จริง (unkillable, not invisible) ก่อน PR นี้ merge — ยังไม่ merge ตอน
  เขียนใบนี้ จึงแก้ได้ทันไม่ต้องเปิดใบตามหลัง
- เทสที่แตะไฟล์นี้ (104 ผ่าน, 1055 subtests) รันซ้ำหลังแก้ ไม่มีอะไรพัง (ไม่มีเทสใด pin ข้อความคอมเมนต์เดิม)

## คำถามที่ยังไม่ตอบ ต้องให้ COO เคาะ
เหตุผลเดิมของ COO ที่ให้ withhold Carlos/Nina คือ "ไม่ออกใบฆ่าให้ของที่ไม่รู้จัก" ซึ่งอ่านได้ว่าเจตนาคือ
**ไม่เอาเนื้อหาที่ยังไม่รู้จักไปอยู่ตรงหน้าผู้เล่น** ไม่ใช่แค่ "ห้ามฆ่า" — ถ้าอ่านแบบนั้นถูก การที่ Nina (และ
Carlos) ยังยืนโชว์ตัวเต็มชื่อ/avatar อยู่ในโลกทุกวันนี้ (ทั้งคู่ ไม่ใช่แค่ Nina) **ไม่ได้ปิดสิ่งที่ COO
ตั้งใจปิด** [สมมติของสาย B - รอ COO ยืนยัน] LANE-B อ่านว่า "unkillable" คือขอบเขตที่ COO อนุมัติจริง
(withhold = คำสั่งของ LANE-B เอง ไม่ใช่ owner refusal — ดูคอมเมนต์ `OWNER_REFUSED_PLACEMENTS` ข้างบนดิก
เดียวกัน) และ "invisible" เป็นแค่คำอธิบายเกินจริงของ LANE-B เอง ไม่ใช่คำสั่งที่ COO เคยให้ — แต่ไม่แน่ใจ
พอที่จะปิดคำถามเองโดยไม่ถาม เพราะถ้าอ่านผิด Carlos/Nina ทั้งคู่ต้องถอดออกจากโลกทันที ไม่ใช่แค่จากใบฆ่า
ทางเลือก: (ก) ยืนตามที่เป็นอยู่ — unkillable พอแล้ว ไม่ต้องแก้การมองเห็น (ข) LANE-A ต้องเพิ่มการอ่าน
`LANE_WITHHELD_PLACEMENTS`/`LANE_WITHHELD_REASON` เข้า census ฐานด้วย เพื่อให้ withhold ปิดทั้งสองแกนจริง
(ค) ทิ้งไว้จนกว่าใบ RE/content "924+529 คืออะไร" (ที่ chief ต้องตั้งเลขตาม `0545` อยู่แล้ว) ตอบ แล้วค่อย
ตัดสินทีเดียวทั้งสองแกน — LANE-B เอนไปทาง (ค) เพราะไม่ใช่ตัวบล็อกผู้เล่นวันนี้ (P-2/GT ยังปิดอยู่ดี) แต่ไม่
ใช่คนตัดสิน

## งานสำรอง (adversary item 4, PROCESS_GATES.md §25)
ไฟล์รอบ `oabhhe` (merge แล้ว) ไม่มีบรรทัด `TWO_SESSIONS_SAME_SCENE:` ทั้งที่ PR แตะ roster registration —
ของจริงคือ **ถูก** (HOSTILE_PLACEMENTS เป็นข้อมูลระดับโมดูล process-wide เหมือนทุกฉากก่อนหน้า ไม่ใช่ต่อ
session/connection · DeathRegister คีย์ด้วย (scene, actor_identity) อยู่แล้ว ไม่แตะรอบนี้) แต่บรรทัดหาย
ไปจากไฟล์รอบเดิมจริง — บันทึกไว้ในไฟล์รอบนี้แทน (ดูด้านล่าง) รับว่าเป็นความผิดพลาดของรอบ `oabhhe` เอง

-- LANE-B
