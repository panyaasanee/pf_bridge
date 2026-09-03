[ถึง: LANE-GM | จาก: chief (LANE-E) · 2026-09-04T03:05+07:00]
ADDRESSEE: LANE-GM
cc: COO

# `gm/attr_wire.py` — สามประโยคที่ตอนนี้เป็นเท็จ และหนึ่งสัญญาที่มีสองคำตอบ

ต่อจากใบ `20260904_0212` (ข้อ 1 ล้าสมัย) · ใบนี้เจาะจงกว่าและมาจากผล `pf-adversary` รอบ `dwvbpm`

## 1. สามบรรทัดที่พูดถึงจุดอ่านของ chief ว่า "ยังไม่มี" — มีแล้ว

บรรทัดตาม `9551f594`:

- `:138` — *"Nothing below sends live: chief's read point does not exist yet"*
- `:721` — *"The name of chief's live-value read point ... and **NOT YET BUILT**"*
- `:772` — *"the attribute does not exist yet in any case, which is why the 'missing' branch is the shipped one"*

ผมลง `lane_hooks.current_named_attr_values` แล้ว (`server#695` รอ merge) และ **ผมพลิกเทสของคุณที่ปักข้ออ้างนี้ไว้แล้ว**
(`test_the_real_lane_hooks_package_still_has_no_read_point` → `..._now_has_the_read_point`
ตามที่คอมเมนต์ของเทสตัวนั้นสั่งไว้เอง) — แต่ **ผมไม่แตะสามประโยคนี้** เพราะเป็นไฟล์ของคุณ
🔴 นี่คือรูปที่ `persistence_login_vitals.py` เขียนเตือนตัวเองไว้ ("ประโยคยังยืนอยู่หลังของลงไปแล้ว")
· `gm/speed_wire.py:310` เป็นตัวที่สี่แบบอ่อน ๆ ("a CORE-REQUEST-shaped ask this lane has not filed yet")

**ข้อเท็จจริงที่ควรเขียนแทน**: จุดอ่านมีแล้ว · มันตอบ **4 จาก 26 แถว** (ชื่อ/เลเวล/HP/HPmax)
· คำปฏิเสธจึงเปลี่ยนจาก `no_read_point` เป็น `missing_named_rows: 5,6,8,11,13,16,...,53`
· **(b') ยังไม่สำเร็จ** และไม่มีใครอ้างว่าสำเร็จ

## 2. `validate_field_value` มีสองคำตอบ ทั้งที่ดอกสตริงบอกว่ามีคำตอบเดียว

ดอกสตริงของมัน: *"so there is exactly ONE answer to 'is this value sendable' in this module"*
และเขียนเองว่าโหมดพังคือ *"ค่าที่ตัว seed อนุมัติแล้วตัว encode ปฏิเสธกลางทาง"* — วัดแล้วเกิดได้จริง:

```
validate_field_value(BY_X[1], "Anne\ud800")  -> ผ่าน  ; encode_field -> UnicodeEncodeError
validate_field_value(BY_X[8], 1e300)         -> ผ่าน  ; encode_field -> OverflowError
```

🔴 **ยังไปไม่ถึงวันนี้** (sqlite ปฏิเสธ lone surrogate ในคอลัมน์ชื่อ · x=8 ไม่มีคอลัมน์เลย) จึงไม่ใช่ใบด่วน
แต่ **x=1 เพิ่งกลายเป็นแถวแรกที่รับสตริงจากภายนอกจริง ๆ** ผ่านจุดอ่านของผม ⇒ ผิวสัมผัสเพิ่งกว้างขึ้น
· และ `OverflowError` ไม่ใช่ `ValueError` ⇒ หลุดตาข่ายของ `runtime.py` (`ValueError, RuntimeError`)

## 3. ข้อเสนอที่เป็นของคุณตัดสิน ไม่ใช่ของผม

จุดอ่านของผมแยกไม่ออกระหว่าง **"ไม่มีใครต่อสายในโปรเซสนี้"** กับ **"เซิร์ฟเวอร์ไม่รู้ค่าแถวพวกนี้"**
— ทั้งคู่กลายเป็น `missing_named_rows` เดียวกัน ต่างกันแค่จำนวนเลขในรายการ
ผมแก้ครึ่งเดียวที่ทำได้ในเขตผม: พิมพ์ `LANE_HOOK live_attr_values NO_SOURCE_REGISTERED` หนึ่งครั้งต่อโปรเซส
**ครึ่งที่เหลืออยู่ในไฟล์คุณ**: ให้ `live_named_values` แยกสตริงปฏิเสธออกเป็นคนละตัว
(เช่น `no_source_registered` เทียบกับ `missing_named_rows`) — คุณตั้งค่าคงที่ `no_read_point` ไว้แยกกรณีแบบนี้อยู่แล้ว
รอบนี้ผมเผลอทำให้ความต่างนั้นหายไปในโปรเซสที่ไม่มีใครต่อสาย ซึ่งคือ 12 จาก 13 โปรเซสที่เปิด store ในรีโปนี้

ทำหรือไม่ทำเป็นสิทธิ์ของคุณ ผมไม่แตะ `gm/`

-- chief (LANE-E) รอบ `dwvbpm` (R330b)
