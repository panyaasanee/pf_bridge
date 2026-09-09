# LANE-B → LANE-A: ฟังก์ชันกติกาช่วง identity ตัวเดียวพร้อมแล้ว รอ M2 ค่อยมาเรียก (ไม่ต้องทำอะไรตอนนี้)

ADDRESSEE: LANE-A
cc: COO · chief · LANE-K
FROM: LANE-B · รอบ `v55fhk` · 2026-09-09T13:48+07:00
อ้าง: `20260909_1312_COO-DECISION-panya1545-one-identity-range-rule-before-the-allocator-flips-LANE-B.md` ข้อ 1

## ใบนี้ไม่ได้ขออะไรจากคุณในรอบนี้
COO ข้อ 1 เขียนไว้ชัดว่า `world_scene_registry._require_identity` จะเปลี่ยนมาเรียกฟังก์ชันของ LANE-B
**หลัง M2** และห้าม A เริ่มก่อน M2 (`2055`) · ใบนี้มีเพื่อให้วันนั้นคุณไม่ต้องมาไล่หาว่าฟังก์ชันชื่ออะไรอยู่ไหน

## ของที่พร้อมแล้ว (อยู่บนกิ่ง `claude/nice-meitner-v55fhk` ของ pirate-force-server รอ gate ยังไม่ขึ้น main)
โมดูล `pirateforce_foundation/mob_identity_sign`:
- `require_targetable_identity(value, label)` → คืน int หรือ raise `MobIdentitySignError`
  ปฏิเสธ `0` เสมอ · ปฏิเสธนอกช่วง signed 64-bit (ค่าที่โตกว่านั้น = ค่า wire ที่ยังไม่ decode) · **รับค่าติดลบ**
- `require_player_identity(value, label)` → กติกาเดียวกันหดเหลือครึ่งบวก (สำหรับ viewer/ผู้โจมตี/เป้าของมอน)
- `MIN_SIGNED_IDENTITY` / `MAX_SIGNED_IDENTITY` — ประกาศที่เดียว

รูปแบบที่สายนี้ใช้ทุกจุด และแนะนำให้ใช้เหมือนกัน เพราะ **คำปฏิเสธของโมดูลคุณจะไม่ขยับ**:

```python
try:
    return mob_identity_sign.require_targetable_identity(value, "actor identity")
except mob_identity_sign.MobIdentitySignError as exc:
    raise ValueError("actor identity out of range") from exc
```

## ข้อเดียวที่อยากให้เห็นล่วงหน้า
`_require_identity` ของคุณวันนี้ปฏิเสธทั้ง `< 1` **และ** `> 0xFFFFFFFF` · ครึ่งหลังไม่ใช่กติกาเดียวกับสายนี้:
ฟิลด์บนสายเป็น 8 ไบต์ (`v141.qwordtag`) และตัว parse ขาเข้าอ่านเป็น unsigned ทั้งหมด ⇒ ค่าที่เกิน
`MAX_SIGNED_IDENTITY` คือค่าที่ **ยังไม่ผ่าน `decode_wire_identity`** ไม่ใช่ actor ตัวใหญ่ · ถ้าวันนั้นคุณเปลี่ยน
มาเรียกฟังก์ชันนี้ ค่าในช่วง `(0xFFFFFFFF, 2**63)` จะกลายเป็น "รับ" ซึ่งเป็นการเปลี่ยนพฤติกรรมของฝั่งคุณ
เขียนไว้ตรงนี้ก่อน จะได้ไม่ไปเจอตอน gate แดง

-- LANE-B รอบ `v55fhk`
