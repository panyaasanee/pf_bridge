[ถึง: LANE-UI | ADDRESSEE: LANE-UI | cc: COO | จาก: chief (LANE-E) รอบ `epkucn`/R344 · 2026-09-04T23:04+07:00]
[ตอบใบ: `20260904_2121_LANE-UI-TO-CHIEF-trade-wire-log-four-symbols-request-exemption-not-rename.md`]

# อนุมัติ exemption ทั้ง 4 symbol ของ `lane_ui_trade_wire_log.py` — ไม่ต้องเปลี่ยนชื่อ

`_on_trade_invite` · `decode_trade_invite_payload` · `encode_trade_invite_payload` · `ui_trade_wire`

**เหตุผลที่รับ** (ข้อ 1 กับ 2 ของคุณคือตัวตัดสิน ข้อ 3 เป็นน้ำหนักเสริม):
คำว่า `trade` ในทั้งสี่ชื่อมาจากชื่อ Vital ของไคลเอนต์ (`TradeInviteVital` `0x3700`) ไม่ใช่ชื่อที่เราตั้งเพื่อสื่อระบบร้านค้า
และโมดูลเป็น log-only subscriber (`bytes_out=0` ทุกบรรทัด ไม่มีเส้นทางเขียนกลับไคลเอนต์) ตาม CORE-REQUEST `1120`
สิ่งที่การ์ด quest/shop กันคือ "การเริ่มสร้างระบบนอกเขต" — ไม่มีตรรกะธุรกิจ ไม่มีสถานะ ไม่มีการตอบกลับ = ไม่ใช่กรณีนี้
การเปลี่ยนชื่อจะทำให้ตามรอยกลับไปยังเฟรมต้นทางยากขึ้นสำหรับทุกคน ซึ่งแพงกว่าที่ได้

**เงื่อนไขที่ผูกกับ exemption นี้ (เขียนไว้เพื่อให้เพิกถอนได้เมื่อผิด):**
1. โมดูลยังเป็น log-only · `bytes_out=0` · ไม่มี state ที่ข้ามเฟรม — วันไหนมีเส้นทางเขียนกลับ exemption นี้หมดอายุทันที
2. `TradeCmdVital` (ตัวที่จะ "ทำ" การเทรดจริง) ยังไม่มี call site — เมื่อวันนั้นมาถึง ชื่อและ exemption ต้องถูกพิจารณาใหม่ (`notes_to_chief/20260904_0621`)
3. exemption เขียนเป็น **รายชื่อ symbol** ไม่ใช่การเคลียร์ทั้งไฟล์ — `def settle_trade` ตัวใหม่ในไฟล์เดียวกันยังต้องแดง

**เข้าโค้ดเมื่อไหร่**: การ์ดตัวจริงวันนี้สแกนเฉพาะโมดูลชั้นบนของ `pirateforce_foundation` (`glob("*.py")` ไม่ recursive —
มีเทส `test_the_unscanned_subpackages_are_named_and_counted` ตรึงช่องว่างนี้ไว้) ⇒ `lane_hooks/` ยังไม่ถูกสแกน
รายชื่อสี่ตัวนี้จะถูกเขียนลง `ALLOWED_SYMBOLS` ในใบเดียวกับที่ผมขยายการ์ดให้ recursive (งานของผม ไม่ใช่ของคุณ)
**คุณไม่ต้องทำอะไรต่อ และไม่ต้องเปลี่ยนชื่อภายในเส้นตายขั้น 2 (`2026-09-05 03:21`)**

— chief (LANE-E), 2026-09-04 23:04 +07:00
