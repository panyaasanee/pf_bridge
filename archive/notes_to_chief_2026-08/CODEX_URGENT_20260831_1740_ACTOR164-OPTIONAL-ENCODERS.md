# CODEX URGENT — ActorAttr +0x164 ในเส้น optional ยังเป็น character_name

สถานะ: พบความขัดแย้งกับโค้ดที่รันได้จริงจากการตรวจแบบอ่านอย่างเดียว; ยังไม่ได้แก้ ServerProject

## ผิดตรงไหน

- `src/pirateforce_foundation/player_wire.py:109-152` มี frozen class-less helper ที่ยังส่งชื่อผ่าน `ActorAttr +0x164`; optional stats path เรียก helper นี้เป็น byte-for-byte crosscheck ที่ `stats_progression_hypothesis.py:943-968,1007,2324`
- `src/pirateforce_foundation/stats_progression_hypothesis.py:303-310` นิยาม `character_name` ที่ `ActorAttr +0x164`
- `src/pirateforce_foundation/damage_hp_link_hypothesis.py:317-321` นิยาม `character_name` ที่ `ActorAttr +0x164`

production `LegacyProjector.start_game` ไม่ใช่จุดผิด: มันเรียก class+level encoder ที่ส่งชื่อใน `BasicAttr +0x28` แล้ว จุดข้างบนเป็น non-default frozen/optional components แต่ถูกเรียกจริงเมื่อเปิด lane ที่เกี่ยวข้อง

## หลักฐานต้นฉบับ

- IMAGE field key: `ActorAttr@0x164.var#W:b0x01000000`
- IMAGE evidence key: `3392ba8ca736f896a76fddf06a84ac2e8d99e6a21305b4b554eb00f74ecf6f9d`
- ผล: `ActorAttr +0x164` ป้อน `NameBoard_Player/LABEL_GUILD`; ชื่อตัวละครหลักมาจาก `BasicAttr +0x28`
- OPEN conflicts: `579ea549…`, `f82af72f…`, `6bc12549…`
- Local-authoritative generation: `59ea10c95c729bb1ee7c0c24c95daf0184f2a5884a3b7b3c29a5a24bf269fc73`

## ผลกระทบ

ถ้าแก้เพียง field table สองโมดูล แต่ไม่แก้ frozen helper/crosscheck เส้น optional จะยังบังคับ layout เก่า หรือ crosscheck จะล้ม หากเปิดใช้โดยไม่แก้ครบ ชื่อตัวละครอาจกลับไปอยู่บรรทัดกิลด์และทำให้ผลทดลอง nameboard ผิด

## ข้อเสนอหลังได้รับสิทธิ์แก้ server

แก้พร้อมกันทั้ง frozen helper/crosscheck, stats field table, HP-link field table และ baseline/tests ที่ตรึงไบต์เก่า โดยคง production class+level path ที่ถูกอยู่แล้วไว้ จากนั้น rerun audit และปิด conflict ทั้ง 3 รายการพร้อมกัน ห้ามแก้ทีละจุดแล้วประกาศว่าปิดแล้ว

