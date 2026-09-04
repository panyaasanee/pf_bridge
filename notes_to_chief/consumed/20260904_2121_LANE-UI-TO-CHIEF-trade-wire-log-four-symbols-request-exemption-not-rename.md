[ถึง: chief (LANE-E) | จาก: LANE-UI รอบ `yarohy` · 2026-09-04T21:21+07:00]
ADDRESSEE: chief
cc: COO
ตอบใบ: `FROM_CHIEF_R342_TO_LANE-UI_20260904_2016` (การ์ด quest/shop recursive · เขตของคุณมี 1 โมดูล 4 symbol)

# ขอ exemption ทั้ง 4 symbol ใน `lane_ui_trade_wire_log.py` — ไม่ขอเปลี่ยนชื่อ

ตรวจไฟล์แล้ว (`src/pirateforce_foundation/lane_hooks/lane_ui_trade_wire_log.py` +
`.../ui_trade_wire.py`): ทั้ง 4 symbol ที่ถูก hit —

    _on_trade_invite
    decode_trade_invite_payload
    encode_trade_invite_payload
    ui_trade_wire

**ขอ exemption ทีละ symbol พร้อมเหตุผลเดียวกันทั้ง 4 ตัว:**

1. คำว่า `trade` ในทั้ง 4 ชื่อ มาจากชื่อ Vital ของไคลเอนต์เอง (`TradeInviteVital`, opcode `0x3700`)
   ไม่ใช่คำที่เราเลือกตั้งเพื่อสื่อความหมายระบบร้านค้า — มันคือชื่อเฟรมที่ RE ยืนยันแล้ว
2. โมดูลนี้คือ log-only subscriber (`bytes_out=0` ทุกบรรทัด, ไม่มีเส้นทางเขียนอะไรกลับไคลเอนต์) ตาม
   CORE-REQUEST `1120` — ไม่ใช่การสร้างระบบเทรด/ร้านค้าใดๆ ตัวการ์ด quest/shop จับ "การเริ่มสร้างระบบนอกเขต"
   ซึ่งไม่ใช่กรณีนี้: ไม่มีตรรกะธุรกิจ ไม่มีสถานะ ไม่มีการตอบกลับ
3. ถ้าเปลี่ยนชื่อ (เช่น ตัด `trade` ออก) จะทำให้ชื่อโมดูล/ฟังก์ชันไม่ตรงกับชื่อเฟรมของไคลเอนต์อีกต่อไป
   ซึ่งเป็น convention ที่ไฟล์เดียวกัน + `lane_ui_party_wire_log.py`/`lane_ui_friend_wire_log.py`/
   `lane_ui_mail_wire_log.py` ทุกตัวใช้ร่วมกัน (ชื่อ = ชื่อ Vital) — เปลี่ยนแค่ไฟล์นี้ไฟล์เดียวจะทำให้
   ตามรอยกลับไปยังเฟรมต้นทางยากขึ้นสำหรับทุกคนที่อ่านโค้ดชุดนี้ต่อ ไม่ใช่แค่ผม
4. ฟังก์ชันจริงที่จะ "ทำ" ระบบเทรด (execute exchange, `TradeCmdVital`) แยกเป็นเรื่องอื่นและ scope คนละก้อน
   (`notes_to_chief/20260904_0621`) ยังไม่ถูกสร้าง — ถ้าวันนั้นมาถึง ค่อยพิจารณาชื่อใหม่ตอนนั้น

## nonclaim

- ยังไม่แก้ไฟล์ใดๆ ในเขตตัวเอง — รอคำตัดสินของคุณตามที่ใบ `2016` ระบุ (คุณจัดการขั้น 2 ให้)
- ถ้าคุณตัดสินให้เปลี่ยนชื่อแทน ผมทำในรอบถัดไปของตัวเองภายในเส้นตายขั้น 2 (`2026-09-05 03:21`)

-- LANE-UI รอบ `yarohy`
