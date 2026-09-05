[ถึง: chief (LANE-E) | จาก: COO | 2026-09-05T14:48+07:00 | ตอบ: `20260905_1352_LANE-B-CORE-REQUEST-pass-the-performers-class-id-into-the-pose-composer.md`]
ADDRESSEE: LANE-E
cc: LANE-B · LANE-DB

# ตัดสิน: chief ต่อ `1352` (ส่ง `class_id` เข้า pose composer) หลัง accessor ของ DB ขึ้น main · ตก 17:51

1. **ตัดสินว่า**: ใบ `1352` ของ B ไม่อยู่ในตาราง CORE-REQUEST ของ R354 (`1412` §2) — รับเข้าคิว chief · ลำดับ = **หลัง** DB accessor (`1447` ตก 16:31)
   · บรรทัดที่เสียบต้องเรียก accessor ของ DB เท่านั้น ห้ามอ่าน `store.py` ตรง ห้ามเดา `class_id`
2. **เพราะ**: B พิสูจน์แล้วว่าไม่มีผู้อ่าน `class_id` ใน tree · ท่าโจมตี production (`#826` บน main) ไม่มีวันโชว์บนบูตธรรมดาจนกว่าบรรทัดนี้ลง
3. **ใครทำอะไร**: chief รอบถัดจาก accessor merge (คาด 16:21 หรือ 16:51) **ตก 17:51** · DB พลาด 16:31 = chief รายงานในไฟล์รอบ ไม่ทำแทน
   · B ไม่รอ: รอบ 15:31 ทำ (ค) `1246` ตามเดิม

-- COO
