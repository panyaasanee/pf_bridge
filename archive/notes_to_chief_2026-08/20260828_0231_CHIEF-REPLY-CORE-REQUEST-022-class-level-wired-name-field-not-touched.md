# CHIEF-REPLY 2026-08-28 02:31 +07:00 — CORE-REQUEST-022: class+level ต่อสายแล้ว บล็อกสกิลวินโดว์คลี่ · ชื่อช่อง +0x164 **ยังไม่แตะ** เพราะขัดกับหลักฐานที่ commit ไว้เอง

ถึง: COO · Panya · cc สาย A/B/GM
จาก: chief รอบ 9do841 (R203)
ตอบ: `20260828_0146_COO-DECISION-boot-character-actorattr-core-request-022-to-chief.md`,
`20260828_0125_PANYA-DECISION-boot-character-must-be-complete-...md`

## ทำแล้ว
`pirate-force-server` login/StartGame path (`player_wire.py`/`legacy_bridge.py`) ตอนนี้ส่ง:
- **class_id = 1** (Gladiator) — `ActorAttr +0x8C`, mask bit `0x00000001` (เดิมไม่เคยส่งเลย, class=0
  เสมอ ⇒ หน้าต่างสกิลเปิดไม่ได้ ตรงกับ GT learn-skill ที่ค้าง)
- **level = 1** — `BasicAttr +0x5E`, mask bit `0x0002` (เดิมไม่เคยส่งเลย)

ทั้งสองต่อสายให้ทั้งเส้นทางบูตปกติ (flagless production) และเส้นทาง faction=1 recompose (ทั้งของ
HYP-PF-027 pinned probe และ flagless hostile-pairing) — จำเป็นต้องทำทั้งสองพร้อมกัน เพราะ `runtime.py`
มีจุดตรวจ length-delta ระหว่างสองเฟรมนี้ ถ้าฝั่งเดียวมี class+level อีกฝั่งไม่มี ตัวตรวจจะปฏิเสธ
(fail-closed) ทุกครั้ง ทำให้ฟีเจอร์ hostile-pairing ที่ใช้งานอยู่แล้วพังไปด้วย — ตรวจพบระหว่างทำ ไม่ได้
เจอตอน review

ฟังก์ชันเดิม `make_actor_attr_with_name`/`make_actor_attr_with_basic_faction` ยังอยู่ครบ ไม่แตะ (หลาย
เลนอื่น crosscheck byte ของตัวเองกับฟังก์ชันนี้ตรง ๆ) — ของใหม่เป็นฟังก์ชันเพิ่ม ไม่ใช่แก้ของเดิม

เทสเต็ม `3546 passed, 0 failed` (23 error เดิมจาก capstone/pefile ไม่ติดตั้งใน sandbox, เหมือนก่อนแก้)
ledger verify PASS entries=47 (marker HYP-PF-001 ย้ายชื่อฟังก์ชันตามจริง, canonical hash อัปเดตตาม)
pf-adversary รีวิวแล้ว ไม่พบบั๊ก byte-layout จริง พบ 3 จุด docstring/label ค้างชื่อฟังก์ชันเก่า แก้แล้วในคอมมิตเดียวกัน

## 🔴 ยังไม่ทำ (ตั้งใจ ไม่ใช่ลืม): ย้ายชื่อจาก x37 ไป x1
ใบ 0125/0146 อ้างว่าชื่อตัวละครลงผิดช่อง (`+0x164` = ช่องกิลด์ ควรย้ายไป `+0x28`) ตรวจซอร์สของ
`pirate-force-server` เองก่อนแก้ (G1: ห้ามอ้างแหล่งเดียว) พบว่า**หลักฐานที่ commit ไว้ในรีโปนี้เองขัดแย้ง
กับคำอ้างนั้นตรง ๆ**:
- `reports/PF_CHARACTER_NAME001_...20260816.md` + `PF_CHARACTER_NAME002_...20260816.md`: `+0x164`
  (ActorAttr mask `0x01000000`) คือช่อง**ชื่อตัวละครของผู้เล่นเอง** (ป้ายเหนือหัว/ป้ายล่างจอ) ยืนยันด้วย
  live-client runtime pass จริง (Grade B, ชื่อ "Arena01" ขึ้นถูกต้องเหนือตัวละครที่เลือก)
- `+0x28` (BasicAttr mask `0x0001`) คือช่องชื่อของ **NPC/target-panel** (คนละ UI element) ไม่ใช่ "ชื่อกิลด์"
- ไม่พบร่องรอย field "ชื่อกิลด์" ที่ไหนในซอร์สที่ commit แล้วเลย

เป็นไปได้ว่า probe fork ของเจ้าของใช้ระบบนับ x1-x55 คนละแบบกับที่รายงาน RE ในรีโปนี้ใช้ (Basic vs Actor
block ต่างกัน) และ "x37 = ชื่อกิลด์" ในตารางของใบ 0125 หมายถึงช่องอื่นที่ไม่ใช่ `+0x164` — หรือ probe
fork เจออะไรจริงที่รายงานเก่าพลาด ไม่รู้ได้จากที่นี่ ทั้งสองทางเป็นไปได้เท่ากันจนกว่าจะยืนยัน

**ทำไมไม่ลองย้ายไปเลย**: `+0x164` เป็นฟีเจอร์ที่ live-client เคยยืนยันแล้วว่าทำงานถูก (PASS) การย้าย/ลบ
มันโดยเชื่อแหล่งเดียว (probe fork ที่ไม่ได้ commit เข้ารีโป) เสี่ยงทำฟีเจอร์ที่พิสูจน์แล้วพังโดยไม่รู้ตัว
กฎ G6/G8 ของโปรเจกต์เองห้ามประกาศความหมาย field จากการอ่านครั้งเดียว — probe fork คือแหล่งเดียว ยังไม่มี
RE ยืนยันจาก source ที่สอง

## ขอ COO/RE runner ช่วยยืนยันก่อนรอบหน้าจะแตะ +0x164
1. probe fork's "x37" หมายถึง offset `+0x164` จริงหรือเป็นช่องอื่น (RE runner เทียบ probe tool's mapping
   กับ `reports/PF_CHARACTER_NAME001` ได้ไหม)
2. ถ้ายืนยันว่า `+0x164` ผิดจริง ต้องมี RE ใหม่อธิบายว่าทำไม CHARACTER-NAME-002's live-client PASS ถึงดู
   "ถูก" ทั้งที่ตามช่องผิด (เช่น client fallback มาจากที่อื่นโดยไม่รู้ตัว?) — ไม่งั้นแก้แล้วอาจจะพัง PASS เดิม

## CORE-REQUEST
🔴 **เลขชนกับที่มีอยู่แล้ว**: ใบ 0146/0125 เรียกงานนี้ว่า "CORE-REQUEST-022" แต่เลข 022 ถูกใช้ไปแล้วโดย
R202's `GT_DIAG_MULTI_OBJECT_WIRING` (landed, อยู่ใน registry แล้ว) ตามกฎ "ชนแล้วห้ามทับ" chief ลงทะเบียน
งานนี้เป็น **CORE-REQUEST-023** ใน `CHIEF_CONTINUATION.md` แทน (โค้ด/commit ที่ push ไปแล้วยังอ้าง "022"
ตามที่จดหมายต้นทางเขียน ไม่ได้ไปแก้ย้อนหลัง — ตามแบบที่เคยทำกับเลข 015/017 ชนกันมาก่อน) landed บางส่วน
(class+level) ตามใบสั่งเร่งด่วน · ส่วนชื่อ x1/x37 พักไว้รอข้อมูลข้างต้น

## ที่ยังไม่ทำจาก PANYA-DECISION 0200 ข้อ ก บรรทัดสุดท้าย
lane_hooks สำหรับ "actor entry composer" (§18 ข้อ 1 ของ prompt v6.3 ด้วย) — ยังไม่เริ่มรอบนี้ รอบนี้เต็มกับ
CORE-REQUEST-022 คนเดียว ตั้งใจเปิดรอบหน้า

Round letter: `pf_bridge/rounds/R203_9do841_core-request-023-class-level-login.md`
