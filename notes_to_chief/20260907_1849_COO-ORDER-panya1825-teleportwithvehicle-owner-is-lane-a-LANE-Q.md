[จาก: COO รอบ 1849 | ตาม PANYA-DECISION `20260907_1825` (ka1-A) | 2026-09-07T18:49+07:00]
ADDRESSEE: LANE-Q
cc: LANE-A · Panya

# แก้แผนที่: `Player.TeleportWithVehicle` เจ้าของ = LANE-A · เลิกสถานะ "cross-lane" ลอย ๆ

## ตัดสินอะไร
เจ้าของเคาะ `1825` ข้อ 2: ขาออกทั้งเส้นของ `Player.TeleportWithVehicle` เป็นของ **LANE-A คนเดียว** · หน้าที่ของคุณคือ **binding ใน script_host ตามที่ A ขอ** ไม่ใช่เจ้าของพฤติกรรม
ใน `docs/LUA_HOST_API_MAP.tsv` แถวนี้เขียนว่า "cross-lane w/ LANE-A" ⇒ เปลี่ยนเป็นเจ้าของเดี่ยว = `LANE-A` (คอลัมน์ owner) · สถานะ STUB/wire คงตามความจริงวันนี้ ห้ามเปลี่ยนตาม

## ที่ยังไม่ใช่ของคุณและยังไม่ใช่ของใคร
`Trigger.TriggerShowMessage` / `Player.OpenUI` — แถวพวกนี้รอผลใบ RE "หน้าต่างรายงานกัปตัน" (A เขียนเนื้อใบรอบนี้ · K ออกเลข) · **ห้ามเดาเจ้าของหรือเดาเฟรม** (กฎ `1910`) · เมื่อผล RE ออก ผมจะตั้งเจ้าของในรอบที่เห็นผล

## โทเคน
`grep TeleportWithVehicle docs/LUA_HOST_API_MAP.tsv` ต้องเห็น `LANE-A` และไม่เห็นคำว่า cross-lane ภายใน 2 รอบของคุณ · งานนี้เล็ก ห้ามให้มันแทรกคิว `Lv`/ครึ่งเขียนของคุณ

-- COO
