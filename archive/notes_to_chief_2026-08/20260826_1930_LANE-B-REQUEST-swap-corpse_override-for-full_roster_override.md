[ถึง: chief · cc: Panya | จาก: สาย B (COMBAT) · รอบ `4z0efc` · 2026-08-26T19:30+07:00]

# LANE-B-REQUEST — สลับหนึ่งบรรทัดที่ `runtime.py:4599` เพื่อเปิด `BUILD-004` (มอนสเตอร์แดง-ศัตรูจริง)

## ขอให้ทำอะไร

ที่จุดเดียวใน `runtime.py` (บรรทัด ~4599) ที่เรียก:

```python
mob_death_override = mob_death.corpse_override(
    legacy, field_mobs.load_roster(), self.mob_death_register,
    ledger=self.mob_combat_ledger,
)
```

สลับชื่อฟังก์ชันเป็น `mob_death.full_roster_override(...)` — **อาร์กิวเมนต์เดิมทุกตัว ไม่ต้อง
แก้อย่างอื่น**

## ทำไม

`corpse_override()` (ต่อสายแล้ว, COO ยอมรับแล้ว) จงใจคืนเฉพาะ identity ที่เปลี่ยนจาก census
default (ตายแล้ว/บาดเจ็บ) — มอนสเตอร์ที่ยังไม่โดนตีเลยยังส่งแบบเดิม (ไม่มีชื่อ ไม่เป็นศัตรู)
`full_roster_override()` (สร้างรอบนี้, `pirate-force-server` branch `claude/serene-darwin-4z0efc`,
commit `fbc9937`) เรียก `repopulation_entries()` ตัวเดียวกันแต่เก็บผลทั้งหมด — สำหรับ identity
ที่ `corpse_override()` คืนอยู่แล้ว สองฟังก์ชันคืนไบต์เหมือนกันทุกประการ (พิสูจน์ด้วยเทส 4 ตัวใน
`tests/test_mob_death.py`) ดังนั้นการสลับนี้ไม่เปลี่ยนพฤติกรรมที่มีอยู่แล้วแม้แต่ byte เดียว
สิ่งเดียวที่เปลี่ยนคือมอนสเตอร์ 13 ตัวที่ยังไม่โดนตีจะได้ร่างศัตรู+มีชื่อในการ build census ครั้ง
ถัดไป — ตรงตาม `BUILD-004` (กำหนด 28 ส.ค. 12:00)

## ไม่กระทบอะไร

- ไม่แตะ death-scope gate (`SANCTIONED_FIRST_TARGET_IDENTITY` 0x201F) — มอนสเตอร์นอกเหนือ P30
  จะเป็นศัตรูให้เห็นและรับดาเมจได้ แต่ยังตายจริงไม่ได้จนกว่าจะมี ruling ขยาย scope เหมือนเดิมทุก
  ประการ (นี่คือคำอ้างของ `BUILD-004` เท่านั้น ไม่ใช่ `BUILD-005`)
- ไม่มี migration ไม่มีการเขียน DB ใหม่ ไม่กระทบ `mob_loot`/`mob_pickup`

## หลักฐาน

`pirate-force-server` `claude/serene-darwin-4z0efc` commit `fbc9937` (PR `#70`) — เทสเต็ม
`3147 passed, 356 skipped, 0 failed` · `pf-adversary` รันก่อน commit (พบ 1 จุด: การอ้าง commit
ผิดในดอกสตริงแก้ไข แก้แล้วในคอมมิตที่ push) ดู `rounds/B_20260826_1930_field_mob_bodies_from_spawn.md`
สำหรับรายละเอียดเต็ม

-- **สาย B · COMBAT**
