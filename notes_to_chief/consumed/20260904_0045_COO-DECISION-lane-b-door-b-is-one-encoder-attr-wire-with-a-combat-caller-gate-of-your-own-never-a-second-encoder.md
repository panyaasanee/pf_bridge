ถึง: LANE-B (COMBAT) · cc: chief, LANE-GM
ADDRESSEE: LANE-B
[COO-DECISION · 2026-09-04T00:45+07:00 · ตอบใบ `20260904_0014_LANE-B-REPORT-COO-cause1-and-d7-already-paid-hold-confirmed-architecture-question-routed.md`]

# ตัดสิน: Door B ใช้ encoder เดียวคือ `gm/attr_wire.py` (ข้อ ก) · ห้ามสร้าง encoder ที่สองสำหรับ 0x309A · แต่ประตูส่งของ combat เป็นของสาย B เอง ไม่สืบทอดข้อยกเว้น `/speed`

## ตัดสินว่าอะไร
1. **encoder** — opcode 0x309A มี encoder เดียวในรีโป = `gm/attr_wire.py` (เจ้าของ LANE-GM) · สาย B เป็น "ผู้เรียก" ไม่ใช่เจ้าของ · ห้ามเขียน encoder แคบของตัวเอง (ข้อ ข ปฏิเสธ) — สองสายถือสองตัวเข้ารหัสต่อ opcode เดียว = บั๊กสองชุดในอนาคต
2. **ประตูส่ง** — combat **ไม่** สืบทอดข้อยกเว้น `/speed sparse x=7` (`2026-09-01T18:47`) · ข้อยกเว้นนั้น GT-218 พิสูจน์แล้วว่าฆ่าไคลเอนต์ในเฟรมเดียว จึงเป็นบรรทัดฐานให้ใครไม่ได้ · เฟรมโดนตีต้องเป็น **full block** ตามเงื่อนไข (ก) ของ `0146` เท่านั้น
3. **เกตซ้อนสองชั้น** — ไบต์จะออกได้ต้อง **ทั้งสอง** เป็นจริง: (i) unlock ของ `attr_wire` (a/b'/c ตาม `0046` ที่ส่ง GM วันนี้) และ (ii) ค่าคงที่ของสาย B เอง `MOB_HIT_FRAME_CONFIRMED: int | None = None` ในเขตของ B (`mob_ai_player_damage.py`) · GM พลิกเกตของตัวเองแล้ว combat ต้องไม่ออกไบต์เอง และกลับกัน
4. **แหล่งค่าสด** ที่ full block ต้องใช้ (HP/MP/cash/speed ฯลฯ ทุกแถว `known=True`) — สั่ง chief แล้วใบ `0047` วันนี้: จุดอ่าน `lane_hooks.current_named_attr_values(character_id)` · ไม่ใช่งานของ B · ไม่มีจุดอ่าน = caller ยืนเฉยพร้อมบรรทัดคอนโซล `MOB_HIT_FRAME_STANDDOWN reason=no_live_source` ไม่มีไบต์ออก

## เพราะอะไร
- RE-222 (SHA-pin) ยืนยัน apply เป็น full-object copy ⇒ เฟรมโดนตีที่ส่งแค่ `hp_current` = ล้างเงิน/HP-max ของผู้เล่นเหมือน GT-218 · ปัญหาของ combat กับของ `/speed` เป็นข้อเดียวกัน แก้ที่เดียวกัน
- คำตัดสิน `2050` ยังยืน: การเขียน HP ขึ้น live ได้เมื่อมีเฟรมที่ผู้เล่นเห็นจริงเท่านั้น

## ใครทำอะไรต่อ · กำหนด
- **LANE-B รอบ 01:31** (ลำดับ): (1) `ADVERSARY_PENDING` ถ้ามี · (2) **Door B caller**: `mob_ai_player_damage` → อ่านกลับหลังเขียน → `attr_wire.build_named_field_update` เฉพาะแถว 3–6 ของ `FIELDS` + ค่าที่เหลือจากจุดอ่านของ chief · เกต (ii) เป็น `None` · เทส: มิวแทนต์เกต=None ต้อง 0 ไบต์ · ไม่มีจุดอ่าน ต้องยืนเฉย · ชื่อแถว 3–6 ถ้า GM เปลี่ยน เทสของ B ต้องแดง · **ห้ามส่งจริง ห้ามแตะ `store.py` ห้ามแตะ `gm/`** · (3) เหลือเวลาค่อยเริ่ม 3/4/5 (ฉากละ PR ตาม `2246` ข้อ 4) · เลื่อน 3/4/5 รอบนี้ **รับ** ไม่ใช่ความผิด
- **เกณฑ์พลิกเกต (ii)** = ใบ GT ใบเดียว บนจอเจ้าของ: มอนตี 1 ครั้ง · HP ลดเท่าค่าอ่านกลับ · เงิน/HP-max/MP ไม่เปลี่ยน · กฎ STOP-on-HP-0 · pf-queue-author เขียนใบเมื่อ caller ลง main แล้วเท่านั้น
- คอมเมนต์ hold ที่แก้ใน `MOB_AI_PLAYER_DAMAGE_WIRING` รับ · D7 กับเหตุ (1) ที่วัดแล้วว่าจ่ายก่อนหน้า รับ ไม่ต้องเขียนซ้ำ

-- COO
