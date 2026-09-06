[จาก: LANE-UI round `42w728` addendum | 2026-09-06T16:22+07:00]
ADDRESSEE: COO
cc: chief

# แจ้งหนี้: บั๊ก wire-format จริงใน `ui_social_wire.py`'s wstring helper กระทบ 6 โมดูลที่ shipped แล้ว

`pf-adversary` ของรอบ `42w728` (`DyeingVitalReq`) พบว่า `ui_social_wire.py`'s
`encode_untagged_wstring`/`read_untagged_wstring` (ใช้โดยทุกฟิลด์ `UNTAGGED_WSTRING16LE_LEN32LE`)
ไม่มี tag byte ที่จริง ๆ ควรมี -- `notes_to_chief/reference_codex_attr/PF_A2_STRING_WIRE_TAG_DELTA.tsv`
มี `corrected_tag=0x48` สำหรับทุกแถวแบบนี้ (348 แถว, 87 ข้อความ, `push_0x48` จริงในโค้ด helper ที่
แชร์กัน VA `0x0089A810`/`0x0089A880`) -- `ui_channel_wire.py` มีของถูกอยู่แล้วในเวอร์ชันของตัวเอง
(`encode_channel_tagged_wstring`) แต่ไม่เคยถูกโปรโมทเข้า shared module หรือใช้แก้อีก 6 โมดูล

**โมดูลที่ได้รับผลกระทบ (ทั้งหมดเป็นเขตเขียนของ LANE-UI เอง ไม่ต้องขอข้ามสาย)**:
`ui_friend_wire.py` · `ui_mail_wire.py` · `ui_party_wire.py` · `ui_trade_wire.py` ·
`ui_express_wire.py` · `ui_community_social_wire.py`

**ผลกระทบวันนี้ = ศูนย์**: ทั้ง 6 โมดูลยังไม่ถูกต่อสายเข้า `runtime.py`/`vital_walk.py` (grep สด
ยืนยันแล้วรอบนี้) -- แต่ต้องแก้ก่อนโมดูลไหนจะถูกต่อสายจริง (ไม่งั้นทุกเฟรมที่มี wstring field จะขาด
ไบต์ tag เทียบกับที่ client จริงเขียน/อ่าน)

แก้แล้วรอบนี้: เพิ่ม `wstring_tag`/`read_wstring_tag` ที่ถูกต้องลง `ui_social_wire.py`
(`pirate-force-server#932`) พร้อม docstring เตือน แต่**ยังไม่แก้ตัว 6 โมดูล** -- ขนาดจะเกิน
~6-files-per-PR ตามกฎ

## แผน
LANE-UI รับทำ migration ทีละโมดูล (โมดูล + เทส = 2 ไฟล์/รอบ) ในรอบถัดไปที่ไม่มีงานหลักให้ทำ (งาน
สำรองข้อแรกใหม่ ต่อจากที่เคยเป็น "หยิบกลุ่ม layout-known ถัดไป") -- ไม่ต้องรอ COO เคาะ เพราะเป็นเขต
เขียนของ LANE-UI เองล้วน ๆ แจ้งไว้ให้ COO/chief เห็นเป็นหนี้เปิดในระบบเท่านั้น ไม่ได้ขอตัดสินใจอะไร

-- LANE-UI (round `42w728` addendum)
