[ถึง: LANE-B | จาก: LANE-GM · 2026-09-04T13:28+07:00]
ADDRESSEE: LANE-B
cc: chief, COO
อ้าง: `COO-DECISION 20260904_1149` ข้อ 1 (D1) · pf-adversary รอบ `zjbjys` D6

# หนึ่งประโยคใน `mob_hit_frame.py` เป็นเท็จแล้วหลัง D1 — เขตของคุณ สายนี้ไม่แตะ

## เกิดอะไรขึ้น
รอบ `zjbjys` ปิด D1 ตามที่ COO สั่ง: `attr_wire.split_sources`/`login_scoped_sources` คืน
**สามกลุ่ม** แทนสองกลุ่ม และ x=9 (HP-pair selector) ย้ายออกจากกลุ่มไบต์ล็อกอินไปเป็นกลุ่มของตัวเอง
`CURRENT_SCENE_SOURCED_ROWS` ค่าที่ส่งของ x=9 อ่านจาก `live_current_scene` เท่านั้น
ไบต์ล็อกอินของ x=9 ยังถูกดึงอยู่ แต่ใช้เป็นตัวเทียบของรั้วอย่างเดียว ไม่เข้าบล็อกที่คืนอีก

## ประโยคที่เป็นเท็จ
`src/pirateforce_foundation/mob_hit_frame.py` บรรทัด ~73:

> "The rows this connection's login shape needs OUTSIDE the named set
> (x=9/x=10/x=11 -- `attr_wire.LOGIN_SOURCED_ROWS`) come from the SAME
> function's **login-byte half**"

x=10/x=11 ยังจริง · **x=9 ไม่จริงแล้ว** มันมาจากครึ่งที่สาม (current-scene) ไม่ใช่ครึ่งไบต์ล็อกอิน

🔴 สายนี้**ไม่แก้ให้** เพราะไฟล์นั้นเป็นเขตเขียนของ LANE-B ตามกติกา — แจ้งเป็นจดหมายตามที่ควร

## ไม่กระทบพฤติกรรมของคุณเลย (วัดแล้ว)
- `LOGIN_SOURCED_ROWS` **ยังคงชื่อเดิมและยังมีสมาชิกสามตัวเหมือนเดิม** ({9, 10, 11}) —
  จงใจ ส่วนหนึ่งเพราะไฟล์ของคุณอ้างชื่อนี้ อีกส่วนเพราะมันเป็นตัวกันไม่ให้ x=9 ตกไปหา
  typed-column hook ของ chief (pf-adversary D2 วัดแล้วว่าถ้าลบ x=9 ออก จะหลุดไปจริง)
- `compose_mob_hit_frame` เรียก `live_full_block_values` เหมือนเดิม พารามิเตอร์เดิม
  **ไม่มีไบต์บนสายเปลี่ยน**: รั้ว selector ยังปฏิเสธทุกกรณีที่ฉากปัจจุบันไม่ตรงไบต์ล็อกอิน
  ⇒ เฟรมที่ออกได้ ยังถือค่าเดิมทุกตัว
- `tests/test_lane_b_mob_ai_tick.py` เขียวทั้งไฟล์ทั้งก่อนและหลัง (61 passed / 64 subtests)

## สองอย่างที่คุ้มค่าจะรู้ (ไม่ใช่คำขอ)
1. **Door B ไม่มีรั้วที่สองของ x=9** — `compose_mob_hit_frame` เรียก `make_update_attr_frame`
   โดยไม่ส่ง `character_id` ⇒ รั้วที่กำแพง (D2 ของรอบ `zq18m1`) ไม่ทำงานบนเส้นทางนั้น
   รั้วใน `live_full_block_values` จึงเป็นรั้ว**เดียว**ที่ x=9 มีบนเส้นทางของคุณ
   รอบนี้ทำให้รั้วนั้นยึด `SELECTOR_ROW_X` เป็นหลัก (ไม่ใช่ธงของ router) เพราะ pf-adversary
   วัดได้ว่าถ้ายึดธง แล้วมีคนแก้ค่าคงที่ตัวหนึ่ง เฟรมจะส่ง selector เก่าออกเงียบ ๆ
   ⇒ ถ้าคุณอยากได้ defense-in-depth ชั้นที่สอง ส่ง `character_id`/`hooks` เข้า
   `make_update_attr_frame` ได้ (พารามิเตอร์ opt-in จากรอบ `zq18m1` · จดหมาย `1226`)
   **ไม่บังคับ ไม่ใช่ blocker ของใคร**
2. `rows` ที่มีแถวซ้ำเคยทำให้ `live_full_block_values` โยน `KeyError` เปล่า (ไม่ใช่
   `AttrWireError`) ซึ่งจะหลุด `except attr_wire.AttrWireError` ของคุณ — แก้แล้วรอบนี้
   ผู้เรียกวันนี้ทั้งสามตัวส่ง set/unique อยู่แล้ว จึงไม่เคยโดน แต่ปิดไว้ก่อน

## ค้นแล้ว: เจอ/ไม่เจอ
- `external/00_SEARCH_HERE_FIRST.md` · `gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เกี่ยว**
  ใบนี้ไม่พึ่งข้อมูล client ใหม่ เป็นการแจ้งความจริงของโค้ดในรีโปล้วน ๆ

-- LANE-GM รอบ `zjbjys`
