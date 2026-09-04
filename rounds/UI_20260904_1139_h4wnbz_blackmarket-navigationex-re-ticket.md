# LANE-UI round h4wnbz — RE ticket for black-market family + ship-window survey opcodes

เวลา: 2026-09-04 11:39 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ NOW/M ข้อไหนรอบนี้ — เป็นใบ RE (คำขอ dynamic capture) ไม่ใช่โค้ด ตามกติกาภารกิจ ("ไม่รู้รูปเฟรมตอบ ⇒
ออกใบ RE ห้ามเดา opcode แล้วส่งไบต์ออก") ปิดสองแถวสุดท้ายของสารบัญ 15 แถวที่ยังไม่มีใบ RE (ตลาดมืด/หน้าต่างเรือ)
เหลือแค่แถวมินิแมปที่ยังไม่ทำ (ยังไม่มีข้อมูลพอเปิดใบ)

## ทำอะไร
1. `git fetch origin main` · ยืนยันรอบก่อน (`qk4t9x` #1115) merge แล้วจริง · ไม่มีใบ `[LANE-UI]` เปิดค้าง
2. รอบก่อนไม่มี `ADVERSARY_PENDING` ค้าง — verification pass ของ `qk4t9x` คืนผลแล้ว **สะอาด ไม่มี defect ยืนยัน**
   (มีข้อสังเกตระดับ low-confidence หนึ่งจุดเรื่องการแยกมิติ STATIC/PROVEN ที่ agent เองบอกว่าไม่ใช่ข้อผิดพลาดจริง
   — ไม่เปิดรอบแก้เพิ่ม)
3. ใช้วิธีเช็คใหม่ (อ่านเนื้อ `.CONSUMED.txt` ตรง ๆ ไม่ใช่แค่เช็คว่าไฟล์มีอยู่) ตรวจ `0453`/`0621` ซ้ำ — เนื้อหา
   เหมือนเดิม (รับหลักการ ยังคิวอยู่) ไม่มีอัปเดตใหม่ · เช็ค `runtime.py`/`vital_walk.py` ตรง ๆ ยืนยันว่ายังไม่มี
   โค้ดลงจริงสำหรับ TARGET_VITAL/CHOOSE_NPC/TradeCmdVital/8 คลาสของใบ `1120` เลย (0 hit ทุกตัว) — ไม่มีโค้ดใหม่
   ให้ทำต่อรอบนี้ กลับไปทำคิว RE ตามเดิม
4. `pf-static-re` (ทำเองในรอบนี้ ไม่ใช้ agent แยก เพราะการค้นครั้งนี้ตรงไปตรงมา): grep
   `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` หา "blackmarket"/"requestsurvey" — ว่างทั้งคู่ (สามรอบติดที่
   ยืนยันแล้ว: `c2a7nc`/`p7m2wq`/`h4wnbz`) · พบข้อเท็จจริงใหม่ที่ยังไม่เคยเขียนไว้ที่ไหน: ไฟล์นี้มีแค่ 327/519
   คลาส (นับด้วย `awk`/`wc -l` เอง) ⇒ "ไม่อยู่ในไฟล์" ≠ "ไม่มี opcode จริง" แค่ "ไม่เคยเจอเป็นสตริงในรอบ R38"
   · นับฟิลด์ resolved ต่อคลาสจาก `PF_SERIALIZER_FIELDS.tsv` เอง (grep ตรง ๆ ทีละคลาส ไม่เชื่อเลขเก่า) — พบว่า
   5/7 คลาสตลาดมืด + `NavigationEx_RequestSurveyVtial` ฟิลด์ resolved ครบแล้ว รอแค่ opcode
5. **กันสับสนสำคัญ**: `NavigationEx_RequestSurveyVtial` (แถว "หน้าต่างเรือ" ของสารบัญฉัน) คนละคลาสกับ
   `NavigationEx_AddSurveyDataVtial`/`NavigationEx_EnterInstanceVital` (กลไก M2 เทียบท่าเกาะของ LANE-A/chief) —
   ชื่อคล้ายกันมากจึงเขียนย้ำไว้หัวจดหมายชัดเจน ไม่ให้เข้าใจผิดว่าแตะเขต M2
6. เขียนจดหมาย `ADDRESSEE: chief`
   `notes_to_chief/20260904_1137_LANE-UI-RE-TICKET-black-market-and-ship-survey-window-opcodes-not-in-r38-
   registry.md` (5,711 อักขระ / 11,182 ไบต์ — ต่ำกว่าเพดาน 12,000 อักขระ)
7. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานเขียนจดหมาย — รีวิวตัวเลข grep/field count ทุกตัว + เช็คว่าไม่ซ้ำใบเดิม +
   เช็คว่าคนละคลาสกับ M2 จริง + เช็คคำอ้าง RE-086/RE-087 จาก archive ตรง ๆ — ผลยังไม่คืนตอน push
   ⇒ **`ADVERSARY_PENDING pf_bridge#1118`**

## ส่งอะไร (SHA/PR)
- `pf_bridge` PR `#1118` (`[LANE-UI] round h4wnbz: claim` → เติมไฟล์รอบนี้ + จดหมาย RE) กิ่ง
  `claude/lane-ui-round-h4wnbz`
- ไม่มี PR เซิร์ฟเวอร์ · ไม่แตะโค้ดเลย · เปิด RE-ticket ใหม่ 1 ใบ (ยังไม่มีเลข — รอ chief ตั้ง)

## nonclaims
① ไม่ยืนยันว่า `GSCN_BlackMarketSearchMyItem` (EMPTY ทั้งคู่) ยังใช้งานจริงหรือเป็น dead code
② ไม่ตัดสินว่า chief ควร re-run string-extraction ให้ครอบคลุม 519 คลาสหรือไม่ — เสนอเป็นทางเลือกเฉย ๆ
③ caller/verb ของทุกคลาสยังไม่รู้ ต่อให้มี opcode ก็ยังไม่รู้พฤติกรรมจริง ④ ไม่ได้เปิดใบมินิแมป — GT evidence ที่
เจอ (`GT-043`/`045`/`063`/`080`) เป็นแค่ minimap เป็น landmark ภาพ ไม่ใช่ click-to-travel ⑤ ไม่มีไบต์ออกไปไคลเอนต์
เครื่องไหนเลยรอบนี้ ไม่แตะโค้ด

## ADVERSARY_PENDING
`pf_bridge#1118` — pf-adversary รีวิวจดหมาย `20260904_1137_LANE-UI-RE-TICKET-*` เริ่มต้นรอบพร้อมงาน ยังไม่คืนผล
ตอน push · ห้ามเขียนว่า "ผ่าน adversary" จนกว่าจะมีผลจริง · รอบถัดไปของ LANE-UI หยิบผลเป็นงานแรกก่อน claim ใหม่

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
- หยิบผล `pf-adversary` ก่อน (ADVERSARY_PENDING ข้างบน)
- ใช้วิธีเช็ค `.CONSUMED.txt` เนื้อหาตรง ๆ ตรวจสามคำขอ (`0453`/`0621`/`1120`) ว่ามีอัปเดตไหม — ถ้ามีโค้ดลง main
  จริงให้ข้ามไปเขียน `ui_*.py` ทันที สูงกว่าคิว RE letter
- แถวเดียวที่เหลือของสารบัญ 15 แถวที่ยังไม่ทำอะไรเลย: **มินิแมป** (ยังไม่รู้แม้แต่ชื่อ class) — ต้องค้นกว้างกว่า
  opcode-matching ปกติ (ลองหาใน UI element names/texture names แทน)

— LANE-UI รอบ `h4wnbz`
