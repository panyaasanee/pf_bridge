[ถึง: LANE-DB | ADDRESSEE: LANE-DB | cc: chief, สาย GM, เจ้าของ | จาก: COO | 2026-09-01T11:01+07:00]
[อ้าง: ใบ `20260901_1059` (คำตัดสินเจ้าของ) · ใบ `20260901_1100` (charter ของสายนี้)]

# COO-ORDER — งานแรกของสาย: `/speed` ใช้ได้จริงตอนเทส

## สั่งอะไร

ทำ `/speed <ตัวคูณ>` ให้ผู้เทส attended ใช้ได้จริง — เดินเร็วขึ้นเห็นด้วยตา — เป็น use case แรกที่
บังคับให้ท่อ typed-attr ทั้งเส้นเกิดจริง (DB -> compose -> ส่ง -> client apply) ตามคำสั่งเจ้าของ

## ข้อเท็จจริงตั้งต้น (วัดมาแล้ว อย่าเสียรอบวัดซ้ำโดยไม่มีเหตุ)

- ฟิลด์เป้าหมายพิสูจน์แล้ว: `BasicAttr@0x54` float32 default 400.0 =
  `MOBS.n_SPEED_WALK_to_initial_visual_horizontal_locomotion_scalar` และ
  `FightAttr_run_speed_formula_input` (gate `+0x70 & 0x0040`) — ดู
  `notes_to_chief/reference_codex_attr/PF_ATTR_FIELD_SEMANTICS.tsv`
- `gm/attr_wire.py` มี `build_named_field_update` ที่ fail-closed (ไม่มี seed = ส่งไม่ได้) —
  `GM-044`: ไม่มีแหล่งบล็อกดิบ live · `RE-172`: ไม่มีแหล่งอื่น — **แต่ DB เก็บ `avatar_wire` /
  `actor_wire` ของตัวละครทุกตัวตั้งแต่ตอนสร้างอยู่แล้ว** (ตาราง `characters`) = ฐานบล็อกดิบ
  per-character มีอยู่จริง
- แนวที่ให้ลองก่อน: base = บล็อบ creation ของตัวละครตัวเอง + overlay เฉพาะฟิลด์ typed ที่รู้จัก
  ⇒ ฟิลด์ไม่รู้จักคงค่าเดิมของตัวละครเอง ไม่มีการเดาเป็นศูนย์ (ข้อห้ามของเจ้าของ ใบ `1059`)
  — ต้องให้ pf-adversary ตรวจว่า claim bulk-copy client `0x464F30` ทำให้แนวนี้ปลอดภัยจริงก่อนส่งจริง

## เกณฑ์ผ่าน

1. wire/DB: ส่ง attr update แล้วค่า speed เปลี่ยนตามสั่ง ฟิลด์อื่นทุกไบต์เท่าเดิม (พิสูจน์ด้วย diff)
2. client-observable: ผู้เทส attended เห็นเดินเร็วขึ้นจริง (เข้าคิว GT entry ผ่าน chief)
3. fail-closed คงอยู่: ตัวละครไม่มีบล็อบ creation = ไม่ส่ง
4. ค่า speed ที่ตั้ง persist ข้าม logout/login (ลง typed column ตัวแรกของสาย)
5. จุดเสียบ chat command: ประสานสาย GM (`gm/chat_command.py`) — ขอผ่านจดหมาย อย่าแก้ไฟล์ของสายอื่นเอง

## กำหนดเมื่อไร

- รอบแรก (11:01): อ่าน charter + สำรวจโค้ดจริง + แผนลง `rounds/DB_*`
- PR โค้ดแรกภายในรอบ 14:01 วันนี้ · `/speed` พร้อมเข้าคิวเทส attended ภายใน 2026-09-02 12:00
- ติดอะไร เขียนใบถึง COO ทันที อย่ารอข้ามรอบ

— COO
