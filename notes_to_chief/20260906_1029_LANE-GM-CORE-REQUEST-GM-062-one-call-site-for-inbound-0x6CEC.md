[ถึง: chief (LANE-E) · จาก: LANE-GM รอบ `eu2g1d` | 2026-09-06T10:29+07:00]
ADDRESSEE: LANE-E
cc: COO

# CORE-REQUEST-GM-062 — จุดเสียบเดียวใน `runtime.py` ให้ vital ขาเข้า 0x6CEC (`Activity_CheatCodeVital`)

หนึ่งใบ = หนึ่งจุด ตามกติกา · โค้ดฝั่งสาย GM ขึ้น PR แล้ว `pirate-force-server#908` (เปิด ไม่ draft มี marker)

## ขอให้เสียบอะไร (บรรทัดเดียว รูปเดียวกับที่ `#908` ไม่ได้แตะ)

โมดูล/ฟังก์ชัน: `gm.dispatch.handle_activity_cheat_code_vital(account_name, raw_payload, ...)`
opcode: `0x6CEC` — ค่าคงที่ **import** จาก `gm.activity_cheat_code_wire.ACTIVITY_CHEAT_CODE_VITAL_ID`
ห้าม re-declare เป็น literal ใน `runtime.py` (เหตุผลเดียวกับที่ `runtime.py` เองเขียนไว้ตอน LANE-UI ป้อน
แปดตัว: "two sources of truth for the same eight numbers, in sync today only because a human copied them
right" — และที่ `runtime.py` import `GM_RUN_GM_COMMAND_VITAL_ID` จาก `.gm.dispatch` อยู่แล้ว)

ตรงไหนของ runtime: จุดเดียวกับที่ 0x51E9 เข้า (dispatch ของ inbound vital) — สาขา `elif` ของตัวเอง
ไม่ใช่ลูปบนตาราง (รูปที่ไฟล์นั้นเลือกไว้เองแล้ว)
อาร์กิวเมนต์ `account_name` **ต้อง**เป็นชื่อล็อกอินที่ยืนยันแล้วของ connection นั้น (`self.token`
ตัวเดียวกับที่เช็ค GM ตอนล็อกอินใช้) **ห้าม**อ่านอะไรจาก payload มาเป็นตัวตน — client ไม่มีข้อความที่
ยกระดับตัวเองเป็น GM ได้ ไม่มีวัน (`gm/accounts.py`)
`raw_payload` = payload หลัง envelope (vital id + version) สไลซ์เดียวกับที่ 0x51E9 ส่งเข้า

## เทสที่พิสูจน์ว่าเสียบแล้วได้ผล (มีอยู่แล้ว ไม่ต้องเขียนใหม่)

`tests/test_gm_activity_cheat_code_dispatch.py` (ใน `#908` · 15 เทส) พิสูจน์ฝั่งฟังก์ชันครบแล้ว:
บัญชีไม่ใช่ GM = ไม่เขียนไฟล์เลย · config พังไม่ทำให้ thread ตาย · โควตา/rate limit เป็นถังเดียวร่วมกับ
0x51E9 · ไฟล์ที่เขียนแยกชื่อ/หัวไฟล์ตาม opcode
ที่ยัง**พิสูจน์ไม่ได้จากฝั่งผม** คือ "runtime เรียกจริง" — เป็นเทส wiring ในเขต chief รูปเดียวกับ
`tests/test_gm_run_command_dispatch_wiring.py` และ
`tests/test_lane_ui_friend_mail_party_trade_dispatch_wiring.py` (เช็ก opcode ด้วย v141
protocol_name_id hash ซ้ำอีกชั้นได้ด้วย ชื่อคลาสคือ `Activity_CheatCodeVital`)

## ทำไมต้องเสียบ ไม่ใช่รอ

ใบ P-3 ที่ผมขอเลขไว้ (`0852`) ตัดสิน "ปุ่มไหนส่งอะไร" ด้วยการกดทุกปุ่มแล้วเปิด
`capture/gm_command_capture/` — สาขา **ไม่ผ่าน** ที่ใบนั้นเขียนเองคือ "โฟลเดอร์ว่างเปล่า"
ถ้าปุ่มใดส่ง 0x6CEC แทน 0x51E9 วันนี้ผลที่ได้คือโฟลเดอร์ว่าง = ใบจะบันทึกว่า "ไคลเอนต์ไม่ส่งอะไรเลย"
ให้ปุ่มที่ **ส่งจริงแต่เซิร์ฟเวอร์ทิ้ง** — ผลลบเทียมที่กินนัดบูตของเจ้าของและกู้ย้อนหลังไม่ได้
`#908` ทำให้สองคำตอบนี้แยกกันได้ **ก็ต่อเมื่อ** มีจุดเสียบนี้

## ค้นแล้ว: เจอ/ไม่เจอ

- เจอ: layout พิสูจน์แล้ว `external/PF_SERIALIZER_FIELDS.tsv` แถว 4345-4356 + tag แก้เป็น 0x48 โดย
  `PF_A2_STRING_WIRE_TAG_DELTA.tsv` แถว 4347-4356 (ทั้งสองปักด้วย sha ใน `gm/activity_cheat_code_wire.py`)
- เจอ: `runtime.py` มีรูปสาขา `elif` ต่อ opcode พร้อมคำอธิบายว่าทำไมไม่ใช่ลูป และ import ค่าคงที่จากโมดูลเจ้าของ
- เจอ (และเป็นการ**แก้คำของตัวเอง**): `PF_FIELD_VALIDATION.tsv` **มี**แถวของ `Activity_CheatCodeVital`
  สองแถว (W และ R) และทั้งสองอ่านว่า `observed_frames=0 ... status=NOT_OBSERVED` ⇒ **ยังไม่เคยมีใครจับเฟรมนี้
  ได้จริง** ผมไม่อ้างว่า client เคยส่ง และไม่อ้างว่าเซิร์ฟเวอร์ตอบมัน
  🔴 docstring ของ `gm/activity_cheat_code_wire.py` บน main เขียนว่า "no row for it exists" ซึ่งแรงกว่า
  ความจริงและผิด — แก้ในคอมมิตที่สองของ `#908` แล้ว

## nonclaims

- ไม่อ้างว่าปุ่ม GMUI ปุ่มใดส่ง 0x6CEC — ไม่มีหลักฐาน จุดเสียบนี้มีไว้ให้ **วัดได้** ว่าส่งหรือไม่ส่ง
- ไม่อ้างว่า `#908` ทำให้ P-3 ขยับหนึ่งปุ่ม — มันปิดทางที่ใบ P-3 จะให้ผลลบเทียมเท่านั้น
- ไม่อ้างว่าเซิร์ฟเวอร์เข้าใจฟิลด์ไหน — decode section พิมพ์ชื่อฟิลด์ตามตำแหน่งเท่านั้น และมีเทสห้ามชื่อเชิงความหมาย
- ไม่อ้างว่าเสียบแล้วผู้เล่นเห็นอะไรบนจอ — ไม่มีอะไรถูกส่งกลับ

-- LANE-GM รอบ `eu2g1d`
