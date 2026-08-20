# ORD-001 แกะ flag word 16 บิตของ hit result ให้ครบทุกบิต

- **objective (claim เดียว):** ในโครง hit-result entry (32 ไบต์ต่อเป้าหมาย) ฟิลด์ `result flag word`
  ขนาด 16 บิต — **แต่ละบิตควบคุมพฤติกรรม/การแสดงผลอะไรของ client และบิตไหนที่ client ไม่อ่านเลย**
  ตอบด้วยหลักฐานระดับไบต์ต่อบิต ไม่ใช่การเดาจากชื่อ

- **ทำไมงานนี้สำคัญ:** Panya อนุมัติแล้วให้ทีม **ออกแบบสูตรความเสียหายของเราเอง** และ
  DAMAGE-MODEL-001 (รอบ 83) สรุปว่าสิ่งที่ server ต้องส่งต่อเป้าหมายคือ
  **i32 มีเครื่องหมาย 1 ตัว + flag word 1 ตัว** ⇒ ครึ่งหนึ่งของ contract ยังไม่มีใครรู้ความหมายทีละบิต

- **inputs (อ่านอย่างเดียวทั้งหมด):**
  - `GameClient\GameClient.local.bin`
  - `reports\` ฉบับของ DAMAGE-MODEL-001 (รอบ 83) — มี 235 byte-exact guards ของโครงเฟรมอยู่แล้ว
  - `tools\` เครื่องมือ static ที่มีอยู่ ใช้เป็นแบบอย่างสไตล์โค้ดได้

- **known answers (ต้อง reproduce ให้ตรงก่อนเชื่ออย่างอื่น):**
  1. เฟรม hit result = หัว 5 ฟิลด์ แล้วตามด้วย array ของ entry ขนาด **32 ไบต์**
  2. ตัวเลขความเสียหายที่ลอยบนจอ = **i32 มีเครื่องหมาย ที่ offset +8 ของ entry** ผ่าน abs() แล้วพิมพ์แบบ integer
     (client **ไม่มีสูตรคำนวณใด ๆ** ไม่ scale ไม่ลบเลือดเอง)
  3. เฟรม missile variant **ใช้ array entry โครงเดียวกัน**
  4. รายการที่รอบ 83 ระบุว่า flag word เกี่ยวข้อง: blocking · knockback · resource readouts ·
     critical · overkill — **แต่ยังไม่มีใครระบุว่าเป็นบิตที่เท่าไรของแต่ละอย่าง**
  ⇒ ถ้าเครื่องมือของคุณ reproduce 4 ข้อนี้ไม่ตรง **ให้หยุดและรายงาน** อย่าเดินต่อ

- **method constraints:**
  - เครื่องมือสุดท้ายต้องรัน **ด้วย standard library ล้วน** (เครื่องที่ตรวจไม่มี disassembler)
  - จับ opcode/เทียบไบต์ตรง ๆ ได้ · ถ้าใช้ตัวช่วยภายนอกระหว่างสำรวจ **ห้ามให้ผลสุดท้ายขึ้นกับมัน**
  - 🔴 **ห้ามสรุปผลลบจากการกวาดที่หยุดกลางทาง** — ต้องรายงานช่วงที่อยู่ที่กวาดจริง
  - พิมพ์เฉพาะอักขระที่ cp874 รับได้

- **deliverables:**
  - `tools\pf_hitresult_flagword_static.py` — เครื่องมือ + guards ต่อบิต (stdlib only)
  - `tests\test_hitresult_flagword_static.py` — เรียกเครื่องมือจริง + **trap test** (แก้ไบต์ให้ผิดแล้วต้องแดง)
  - `reports\PF_HITRESULT_FLAGWORD_STATIC_<วันที่>.md` — ตารางบิต 0–15 ทีละบิต:
    `บิต | ที่อยู่ที่อ่านบิตนี้ | ทำอะไร | ชั้นหลักฐาน (static/inference) | ถ้าไม่ถูกอ่านเลยให้เขียนว่าไม่ถูกอ่าน`
  - `reports\PF_HITRESULT_FLAGWORD_STATIC_<วันที่>.bits.json` — ตารางเดียวกันแบบเครื่องอ่าน
    (รายงานต้อง derive ตัวเลขจากไฟล์นี้ ไม่ใช่พิมพ์มือ)

- **acceptance:**
  - `py -3 -m pytest tests\test_hitresult_flagword_static.py -q` เขียว รวม trap test
  - `py -3 -m pytest -q` (ชุดเต็ม) เขียว
  - `py -3 tools\pf_hitresult_flagword_static.py` รันจบด้วย exit 0 และพิมพ์จำนวน guard ที่รัน/ที่แดง
  - `git check-ignore` ทุกไฟล์ใหม่ → **ต้องไม่ถูก ignore** (โปรเจกต์นี้ ignore ไฟล์ tools/reports ใหม่โดยปริยาย
    ต้องเพิ่มใน allowlist ของ `.gitignore` ⇒ **บอกไว้ใน HANDBACK ว่าคุณแตะ .gitignore** เพราะ chief
    ต้องรัน seam test ก่อน merge)

- **forbidden (เพิ่มจากรายการกลาง):** ห้ามแก้ `src/` · ห้ามเขียน encoder ของ hit result
  (การ implement เป็นงานของ chief) · ห้ามเปิด hypothesis

- **report format:** objective / method + ขอบเขตที่กวาดจริง / ตารางบิต / สิ่งที่ขัดกับที่เคยเชื่อ /
  **nonclaims** (อย่างน้อยต้องมี: ไม่ได้พิสูจน์ว่า server ต้นฉบับใช้บิตเหล่านี้อย่างไร) /
  ข้อเสนอต่อ chief
