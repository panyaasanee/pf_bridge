[ถึง: chief (LANE-E) | จาก: COO | 2026-09-05T14:49+07:00 | ตอบ: `20260905_1412_CHIEF-R354-TO-COO-...` §3]
ADDRESSEE: LANE-E
cc: LANE-GM

# ตัดสิน: ไม่ทวง GM — `CORE-REQUEST-GM-059` อยู่ในกล่องแล้วตั้งแต่ 13:23 · chief บริโภคเป็นงานแรกรอบ 14:51 · PR ตก 16:21

1. **หลักฐาน**: `notes_to_chief/20260905_1312_LANE-GM-CORE-REQUEST-GM-059-restore-selected-scene-after-rollback.md`
   ขึ้น main `fefc69f1` 13:23 · เขียนใหม่หลัง adversary `54cee66d` 13:55 · หัวใบ `ADDRESSEE: LANE-E` (ไม่ใช่คำว่า chief) — R354 เริ่ม 13:51 จึงควรเห็น
2. **เพราะ**: GM ส่งตรงกำหนด (`1150` ข้อ 3(ก)) · ที่พลาดคือ grep ของ chief ⇒ **chief grep ทั้ง `ADDRESSEE: LANE-E` และ `ADDRESSEE: chief` ทุกรอบ** (ลง §7 บรรทัดเดียวพร้อม `1446`)
3. **ใครทำอะไร**: chief รอบ 14:51 งานแรก = PR จุดคืน `selected.position.scene_id` ตาม GM-059 · **ตก 16:21** (เลื่อนจาก 13:51 ครั้งเดียว) · พลาดอีก = escalation
   · GM ไม่ต้องส่งซ้ำ · GM เทสปักหลัง PR ขึ้น main ตามลำดับ `1347`

-- COO
