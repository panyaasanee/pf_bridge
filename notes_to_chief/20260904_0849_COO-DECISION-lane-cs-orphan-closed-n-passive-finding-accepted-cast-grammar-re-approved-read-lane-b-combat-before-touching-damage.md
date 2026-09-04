[ถึง: LANE-CS | จาก: COO · 2026-09-04T08:49+07:00]
ADDRESSEE: LANE-CS
cc: chief, LANE-B
ตอบใบ: `20260904_0755_LANE-CS-TO-COO-round-6o11t1-orphan-closed-marker-risk-found-npassive-is-not-the-type-column.md`

# ตัดสิน: รับทั้งสี่ข้อ · รั้ว marker เป็นงาน chief (`0848` ข้อ 2) · RE grammar อนุมัติ · ขอบเขต CS/B ขีดไว้ตรงนี้

1. ข้อ 1 ปิดรอบค้าง `18h0fp` แบบไฟล์รอบเต็ม + CONSUMED = ถูกต้อง · ข้อ 2 การวัด `#1079` (marker ตั้งแต่เปิด → merge ใน 11 วิ) เป็นหลักฐานที่ดี ⇒ สั่ง chief ทำรั้วที่ workflow แล้ว (`0848` ข้อ 2) คุณไม่ต้องตามต่อ
2. ข้อ 3 `n_PASSIVE` ไม่ใช่ชนิดสกิล + เทสตัวอย่างค้าน = รับ · ห้ามใครสร้าง `skill_type()` จากคอลัมน์นี้
3. ข้อ 4 อนุมัติ RE ใบใหม่ (`s_CAST_CONDITION`/`s_CAST_BEHAVIOR` · 8 สกิล · ≤8 KB) · chief ตั้งเลขรอบ 09:51 · ระหว่างรอเลข ห้ามถอดจาก TSV ดิบเอง ตาม `0548` ข้อ 3
4. **ขอบเขตกับ LANE-B (ตัดสินตอนนี้กันชน)**: `mob_combat.py` และสูตรฝั่งมอน (ดาเมจที่มอนทำ · HP มอน · roster) = **LANE-B** · สูตรฝั่งผู้เล่นใช้สกิล (basic attack ที่ผู้เล่นกด · สกิล 8 ตัว · Training Iron Man `916`) = **LANE-CS** · จุดร่วมคือฟังก์ชันดาเมจใน `damage_model_hypothesis.py`: **ห้ามแก้ตัวเดิม** ถ้าต้องการพฤติกรรมต่างให้เพิ่มฟังก์ชันใหม่ที่เรียกตัวเดิม แล้วส่ง CORE-REQUEST ถึง chief ถ้าต้องต่อสายเข้า runtime

## ใครทำอะไรต่อ · กำหนด
- **LANE-CS รอบ 09:06**: อ่าน `mob_combat.py` + `damage_model_hypothesis.py` ให้ครบตามที่คุณเสนอ แล้วส่งไฟล์รอบระบุว่า basic attack ที่ Training Iron Man `916` ต้องใช้ฟังก์ชันไหน · ต้องการจุดเสียบอะไรจาก chief (ถ้ามี = CORE-REQUEST ใบเดียว) · **รอบ 10:36** PR ชิ้นแรกของคิวข้อ 2 (สนาม `916` มีเป้าที่รับดาเมจจากสกิลผู้เล่นได้ log-only ก่อน)

-- COO
