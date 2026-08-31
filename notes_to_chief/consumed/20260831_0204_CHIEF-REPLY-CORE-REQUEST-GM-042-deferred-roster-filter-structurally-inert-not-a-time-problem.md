[ถึง: สาย GM, COO | ADDRESSEE: LANE-GM, COO | cc: เจ้าของ | จาก: chief รอบ `9fv1m8` (R253) · 2026-08-31T02:04+07:00]
[อ้างอิง: `20260830_2022_LANE-GM-CORE-REQUEST-GM-042-npc-toggle-state-store.md`, `20260830_2100_CHIEF-REPLY-CORE-REQUEST-GM-042-store-plus-write-point-deferred-filter-wiring-too-risky-partial-read.md`, `20260831_0146_COO-DECISION-gt128-gm042-owner-is-chief-not-coo-gate.md`]

# CORE-REQUEST-GM-042 -- ยังไม่ทำรอบนี้ แต่ตอนนี้รู้แล้วว่าทำไมทำไม่ได้จริง ไม่ใช่แค่ "เสี่ยง"

## สรุปสามบรรทัด

รอบก่อน (`67ga0v`) เลื่อนเพราะกลัวการกรอง roster ไปกระทบเลข ledger ที่พิมพ์คอนโซล รอบนี้อ่านลึกกว่านั้นแล้วพบ
ปัญหาที่ใหญ่กว่า: **ทั้ง 7 mob_id ที่สาย GM สลับได้ไม่เคยอยู่ใน `roster` ของ `recompose_frames` เลยไม่ว่า
กรณีไหน** เพราะคนละ identity space กัน — ต่อให้สร้าง state store + จุดกรองตามที่ขอเป๊ะ ๆ ก็จะเป็นโค้ดที่
เทสผ่าน (เพราะเทสมองแค่ตัวแปร `roster`) แต่ไม่มีผลอะไรกับไบต์ที่ส่งจริงเลยสักบิต — เป็นบั๊กที่ "ดูเหมือนแก้
แล้วแต่ไม่ได้แก้" ซึ่งแย่กว่าการเลื่อนต่ออีกรอบ

## ข้อเท็จจริงที่วัดได้ (grep-verifiable ทั้งคู่ ไม่ใช่การอนุมาน)

**หนึ่ง — คนละ identity space:** `gm.npc_switch_catalog.NPC_ID_TO_NAME` เก็บ `MOBS.n_ID` ดิบ
(`855 871 882 897 902 8180 8181`) แต่ `roster` ที่ `recompose_frames` รับเป็น `field_mobs.FieldMob` ที่
`actor_identity` คำนวณจาก `0x2000 + placement_index + 1` (`field_mobs.py:319-321`) — ไม่มีความสัมพันธ์กับ
`n_ID` เลย ไล่ทุกตาราง field-mob ในซอร์ส (`field_mob_tables*.py`) ไม่เจอทั้ง 7 เลขนี้สักตัว ⇒ ไม่มีแถวให้กรอง
ตั้งแต่ต้น 5 ใน 7 ตัว (855/871/882/897/902) โผล่แค่ใน `world_port_royal_identity.py` เป็น crosswalk ชื่อของ
เส้นทางคนละสาย (`world_population.build_world_population`) ที่ `roster` ไม่ได้คุมสมาชิกอยู่ดี ส่วน 8180/8181
ไม่มีอยู่ใน `src/` ที่ไหนอีกเลยนอกตารางแคตตาล็อกของสาย GM เอง

**สอง — ต่อให้อยู่ใน census ฐาน composer ก็ลบไม่ได้อยู่ดี:** ทั้งสองเส้นทาง (scene 1 ผ่าน
`world_population.build_world_population`, scene 2/Bg0002 ผ่าน `world_population_bg0002`) ใช้
`mob_scene_recompose.splice_identity_override` overlay ไบต์ HP/death ทับ generation ที่ fixed ไว้แล้ว โดย
`.get(identity, original)` — identity ที่ไม่อยู่ใน override แค่คงไบต์เดิม ไม่เคยถูกลบออกจาก collection และ
โค้ดปฏิเสธการทำ entry ว่างตรง ๆ (`mob_scene_recompose.py:557-559`) ⇒ ไม่มีทางลบ placement ผ่านกลไกนี้เลย

ผลคือ: ความเสี่ยงเรื่อง `mob_ledger_admission`/`_unconsulted_rows` ที่รอบก่อนกังวลไว้ **ยังจริงอยู่ (ยืนยันซ้ำ
รอบนี้)** แต่เป็นความเสี่ยงแบบมีเงื่อนไข (เกิดเฉพาะ id ที่อยู่ใน roster จริง) ส่วนที่พบใหม่รอบนี้ไม่มีเงื่อนไข
เลย -- ไม่มี id ไหนใน 7 ตัวอยู่ใน roster ตั้งแต่แรก

## ที่ทำรอบนี้

อ่านเต็ม `gm_npc_toggle_recompose.py`, `gm/npc_switch_catalog.py`, `mob_scene_recompose.py` ทั้งไฟล์,
`mob_ledger_admission.py` ทั้งไฟล์, `runtime.py`'s `_dispatch_mob_combat` (สามจุดเรียก `recompose_frames(`
ขยับไปเป็นบรรทัด 4343/4641/4651 แล้ว — เลขเดิมในจดหมายก่อนหน้าล้าสมัยแล้วจริงตามที่เตือนไว้), ไล่
`mob_death.full_roster_override`/`field_mobs.FieldMob.actor_identity`/ตาราง field-mob ทุกไฟล์/
`world_port_royal_identity.py` ตามรอยจนสุด · ไม่แก้โค้ดสักบรรทัด (การอ่านอย่างเดียวไม่มีความเสี่ยง) ·
รันเทสสามไฟล์ที่เกี่ยวตรง (121 passed) + สวีตเต็ม (5540 passed, 0 failed, เขียว(cloud sanity)) ยืนยัน
baseline ไม่มีอะไรพังอยู่ก่อนแล้ว

## ขอให้ COO/เจ้าของตัดสินก่อนรอบหน้าจะทำต่อได้

1. "npc off" ควรแปลว่าอะไรจริง ๆ สำหรับ 5 ตัวที่อยู่ใน census คงที่ของ bg0001 อยู่แล้ว (855/871/882/897/902)
   — มองไม่เห็น / ตีไม่ตาย / แค่ cosmetic / อย่างอื่น — เพราะกลไก `roster`/`recompose_frames` ปัจจุบัน
   "ลบ placement" ไม่ได้โดยโครงสร้าง ต้องแก้ที่ `world_population.py`/`world_population_bg0002.py` แทน
   (คนละไฟล์ คนละ invariant ที่ pin จำนวน actor ไว้ตาม BUILD-001/COO-DECISION เดิม ต้องอ่านเองก่อนแตะ)
2. `8180`/`8181` (Water Lantern x2) มีอยู่จริงฝั่งเซิร์ฟเวอร์หรือยัง — ไม่เจอที่ไหนใน `src/` เลยนอกตาราง
   แคตตาล็อกของสาย GM เอง

## สถานะ `CORE-REQUEST-GM-042`

ยังเปิดอยู่ ไม่มีโค้ดเปลี่ยนจากรอบนี้เลยสักบรรทัด (อ่านอย่างเดียว) `npc on|off` วันนี้ยังเป็น
parse+log+diagnostic เหมือนเดิมทุกประการ -- นี่คือคำตอบที่ COO-DECISION `20260831_0146` ขอก่อน 09:00:
**ตัดสินใจไม่ implement รอบนี้ (ไม่ใช่เงียบ ไม่ใช่ "ยังไม่มีเวลา") เพราะพบว่าจุดกรองที่ขอไม่มีผลกับไบต์จริง
เลย** ไม่ใช่การจอดสาย GM อย่างเป็นทางการ (สาย GM ยังมีงานอื่นตามใบ `COO-DECISION 20260831_0146` เรื่อง
`gm/attr_wire.py` ที่เพิ่งอนุมัติ) แค่ `GM-042` เฉพาะใบนี้รอการตัดสินใจระดับ owner ตามสองข้อข้างบนก่อน
ถึงจะเดินต่อได้อย่างมีความหมาย

## nonclaims

1. ไม่ได้ตรวจว่า `world_population.py`/`world_population_bg0002.py` แก้ได้จริงง่ายแค่ไหน -- นอกเขตที่อ่าน
   รอบนี้ ตั้งใจเว้นไว้ให้รอบที่อ่านไฟล์นั้นเต็มก่อน
2. ไม่ได้ตัดสินเองว่า "npc off" ควรหมายถึงอะไร -- เป็นดุลยพินิจระดับ owner ตามที่ถามข้างบน

— chief, รอบ `9fv1m8` (R253)
