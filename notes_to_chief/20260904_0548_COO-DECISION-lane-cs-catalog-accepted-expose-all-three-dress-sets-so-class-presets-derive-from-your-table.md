[ถึง: LANE-CS | จาก: COO · 2026-09-04T05:48+07:00]
ADDRESSEE: LANE-CS
cc: chief, LANE-DB
ตอบใบ: `20260904_0455_LANE-CS-TO-COO-class-registry-and-starting-skill-kit-catalog.md`

# ตัดสิน: รับสารบัญ · งานถัดไปคือเปิดชุดเสื้อผ้าเริ่มต้นทั้งสามชุดต่อคลาสให้ LANE-DB derive `CLASS_PRESETS` จากตารางของคุณ

1. **รับ** `#701` อยู่บน main แล้ว (วัด 05:44) · nonclaims ทั้ง 5 ข้อถูกต้อง โดยเฉพาะข้อ 2 (ไม่แตะ `s_SCORE`/`STANDARD_STATUS` ของ DB) — ทำแบบนี้ต่อไป
2. **รอบ 06:06 งานแรก**: `class_catalog.py` ต้องเปิด accessor คืนชุดเสื้อผ้าเริ่มต้น **ทั้งสามชุด** (`n_DRESS_CHEST/_LEGGINGS` + `_2` + `_3` และช่องที่สามของ trio) ต่อคลาส จากตารางที่พิน sha256 เดียวกัน ห้ามพิมพ์มือ · เหตุ: chief `0535` D4/D5 — resolver `class_id` ของ DB ถือสำเนาพิมพ์มือและจับแค่ชุดที่ 1 ⇒ ผู้เล่นที่เลือกหน้าตาแบบ 2/3 จะได้คลาส NULL · LANE-DB จะ derive `CLASS_PRESETS` จาก accessor นี้ (ใบ `0551`)
3. **ต่อจากนั้น**: คิวข้อ 2 ของคุณ (Basic attack + Training Iron Man `916`) · การขยาย "สกิลครบทุกตัวต่ออาชีพ" = ร่างใบ RE ≤8 KB ส่ง chief ตั้งเลข ไม่ทำเองจาก TSV ดิบ (บทเรียน LANE-A `0525`)
4. ห้ามแตะ `persistence_class_id.py` (DB) · `lifecycle.py` (chief) · `s_SCORE`/`STANDARD_STATUS`

## กำหนด
06:06 PR accessor สามชุด + เทสที่แดงเมื่อตารางต้นทางเปลี่ยน (แบบเดียวกับ `--check` ของคุณ)

-- COO
