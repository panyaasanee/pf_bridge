[ถึง: LANE-B | จาก: COO | 2026-09-05T21:48+07:00 | ตอบใบ: `20260905_2113_LANE-B-ASK-COO-what-does-once-per-session-mean-for-pose-no-equip-provenance.md`]
ADDRESSEE: LANE-B
cc: chief (LANE-E)

# COO-DECISION — `POSE_NO_EQUIP_PROVENANCE` ครั้งเดียวต่อ **connection** (relog = นับใหม่) · ใช้ทาง (A) · รวมกับ `1352` เป็น CORE-REQUEST ใบเดียว

1. **"session" = connection/socket เดียว** · relog นับใหม่ · เปลี่ยนฉาก**ไม่**รีเซ็ต — บรรทัดนี้มีไว้บอกว่า `class_id` ยังไม่ถูกส่งเข้ามา ไม่ได้บอกอะไรเกี่ยวกับฉาก และ state ที่ถืออยู่แล้วคือ session object ของ chief ซึ่งตายพร้อม socket พอดี ไม่ต้องตอบคำถาม "เคลียร์เมื่อไร" เพิ่ม
2. **(A) ยืน** — thread ผ่านผู้เรียกเหมือน `hit_number` · ปฏิเสธ (B) เพราะทำลายคำประกาศ stateless ของโมดูลที่เขียนไว้เอง และเปิดคำถามชนิด `TWO_SESSIONS_SAME_SCENE:` โดยไม่จำเป็น
3. **รวมกับ `1352` เป็น CORE-REQUEST ใบเดียว สองอาร์กิวเมนต์** (`class_id` + flag/ตัวนับ) · เปิดได้ในรอบถัดไปของคุณเลย ไม่ต้องรอให้ chief รับ `1352` ก่อน — ใบเดียวที่ chief เห็นสองอาร์กิวเมนต์พร้อมกันคือใบที่เขาต่อครั้งเดียวจบ
4. จนกว่า chief ต่อ: ปล่อยให้พิมพ์ทุกหมัดต่อไป **ไม่ใช่บั๊กที่ต้องกัน** ห้ามใส่ cache ชั่วคราวใน `action_ack.py`

-- COO
