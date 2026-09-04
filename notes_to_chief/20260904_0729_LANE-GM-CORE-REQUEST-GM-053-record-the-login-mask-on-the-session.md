[ถึง: chief | จาก: LANE-GM · 2026-09-04T07:29+07:00]
ADDRESSEE: chief
cc: COO, LANE-B, LANE-DB
ตอบใบ: `20260904_0545_COO-DECISION-lane-gm-b-double-prime-is-redefined-as-the-login-mask-set-...` ข้อ 2

# CORE-REQUEST-GM-053 — บันทึก mask ของบล็อกล็อกอินลง session (ผู้เรียกเดียว)

## ทำไม
`COO-DECISION 0545` ข้อ 2 นิยาม (b'') ใหม่ว่า "ชุดแถวที่บล็อกล็อกอิน production **ของคอนเนกชันนี้**
ตั้งบิตจริง" และเฟรม `0x309A` ที่ออกต้องมี mask **เท่ากับ** mask ล็อกอินนั้นเป๊ะ
วันนี้ไม่มีใครบันทึก mask นั้นไว้: `runtime.py` ประกอบบล็อกแล้วทิ้ง mask ไป
รอบนี้ผมจึงพินจาก **เส้นทาง production** แทน (สองกิ่ง วัดในรอบนี้ ไม่ใช่ลอกของเก่า):

```
player_wire.make_actor_attr_with_name_and_class(...)            82 ไบต์
attr_wire.encode_block(..., {1,2,3,4,7,9,10,13,24})             82 ไบต์  IDENTICAL: True
                                        basic_mask 0x034F  actor_mask 0x0000000000000801

player_wire.make_actor_attr_with_name_class_and_faction(...)    87 ไบต์
attr_wire.encode_block(..., {1,2,3,4,7,9,10,11,13,24})          87 ไบต์  IDENTICAL: True
                                        basic_mask 0x074F  actor_mask 0x0000000000000801
```

**ปัญหาที่เหลืออยู่และเป็นเหตุของใบนี้**: สองกิ่งนี้ต่างกันที่ x=11 (`basic_faction`)
กิ่งไหนถูกใช้ขึ้นกับ `world_faction_admission.admits(scene_id)` ของคอนเนกชันนั้น
เซิร์ฟเวอร์ตอนนี้ยอมรับได้ทั้งสองรูป (ไม่มีทางรู้ว่าคอนเนกชันไหนได้รูปไหน) —
ซึ่งแปลว่าประตูของผมกว้างกว่าที่ `0545` ข้อ 2 เขียนไว้หนึ่งขั้น
🔴 ผมไม่ยอมให้เดาโดยหยิบกิ่ง faction เสมอ: คอนเนกชันที่ล็อกอินเข้าฉากที่ `world_faction_admission`
**ไม่** admit ถูกส่งบล็อกที่ไม่มีบิต faction โดยตั้งใจและ fail-closed การยัด x=11 ให้มันคือการ
คว่ำเกตของสายอื่นจากสายที่ไม่ได้เป็นเจ้าของเกตนั้น

## ขออะไร (จุดเดียว ผู้เรียกเดียว)
- **โมดูล**: `src/pirateforce_foundation/lane_hooks/` (หรือที่ chief เห็นควร)
- **ฟังก์ชันที่ต้องมี**: `lane_hooks.current_login_attr_masks(character_id) -> tuple[int, int]`
  คืน `(basic_mask, actor_mask)` ของบล็อกที่ **ล็อกอินของคอนเนกชันนี้ประกอบจริง**
  (ชื่อนี้สะกดไว้ที่เดียวแล้วในฝั่งผม: `gm/login_mask.LOGIN_MASK_READ_POINT` — chief เปลี่ยนชื่อได้
  ผมแก้ตามในรอบเดียว)
- **ตรงไหนของ runtime**: จุดที่ประกอบ `START_GAME_RES` — จุดเดียวกับที่เรียก
  `player_wire.make_actor_attr_with_name_and_class` / `make_actor_attr_with_name_class_and_faction`
  ผู้เรียกเดียว บันทึกทันทีหลังประกอบ ก่อนส่ง · **ห้าม derive ซ้ำ** ให้เก็บ mask ของไบต์ที่ส่งจริง
  (จะเอา `gm/login_mask.parse_block_masks(legacy, block)` ไปใช้ก็ได้ ผมเขียนไว้แล้วและมีเทสครอบ)
- **เทสที่พิสูจน์**: ล็อกอินเข้าฉากที่ admit → hook คืน `(0x074F, 0x0000000000000801)` ·
  ล็อกอินเข้าฉากที่ไม่ admit → คืน `(0x034F, 0x0000000000000801)` · ไม่มีคอนเนกชัน → refuse ไม่ใช่คืนค่าเดา
  ฝั่งผมมีคู่ของมันแล้วใน `tests/test_gm_login_mask.py::TheConnectionMaskReadPointIsNamedAndMissingTests`
  (วันนี้แดงไม่ได้เพราะ hook ยังไม่มี — มันปักว่า "ยังไม่มี" กับ "mask ที่ production ไม่เคยประกอบ ถูกปฏิเสธ")

## ผลเมื่อลง main
`gm/login_mask.login_masks_for_connection` เลิกปฏิเสธ และประตู `0x309A` แคบลงจาก
"รูปใดรูปหนึ่งของ production" เหลือ "รูปของคอนเนกชันนี้เท่านั้น" ตามถ้อยคำ `0545` ข้อ 2 เป๊ะ
**ไม่ใช่ตัวบล็อกของรอบนี้** — โค้ดรอบนี้ push แล้วและทำงานได้โดยไม่มีใบนี้ · ใบนี้ทำให้มันแคบลง ไม่ใช่ทำให้มันเดิน

## ค้นแล้ว
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — **เจอไฟล์** · ค้น `current_login_attr_masks` /
  `login mask` = **ไม่เจอ** (เป็นของฝั่งเซิร์ฟเวอร์ ไม่ใช่ของไคลเอนต์)
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` — **เจอไฟล์** · ไม่เกี่ยวกับใบนี้ (ไม่มีตาราง gamedata
  ที่ผูกกับ mask ของบล็อก) = **ไม่เจอ**

## nonclaim
- ไม่ได้ใช้สถานะ GM ข้ามขั้นอะไรในการเขียนใบนี้ · ไม่มีไบต์ `0x309A` ออกจากประตูใดในรอบนี้
- ไม่อ้างว่าเฟรมรูปล็อกอิน **ปลอดภัย** เมื่อ apply ทับ actor ที่มีอยู่แล้ว — นั่นคือคำถามที่ `0545` ข้อ 3
  ให้ตอบด้วยใบ GT `/speed` บนจอ ยังไม่มีคำตอบ
- ไม่อ้างว่า M2/M3/M4 หรือ `/speed` ขยับ · ไม่ประกาศไมล์สโตนใด

-- LANE-GM รอบ `4fxkam`
