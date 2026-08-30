ADDRESSEE: สาย GM · cc: COO, เจ้าของ
ประเภท: CHIEF-REPLY ตอบ CORE-REQUEST-GM-043 (ใบ `20260831_0321`)

# ตัดสิน: ทางเลือก A -- คำสั่งแชท `/gmprobe <variant_id>`

เหตุผล:

1. **ทำครั้งเดียวจบ** (หลักดีไซน์ข้อ 4) -- กะ1-A ยิง variant ไหนก็ได้ตามต้องการระหว่างเซสชันจริง ไม่ต้องนั่งจับ
   เวลาแบบทางเลือก B ซึ่งใช้ได้ครั้งเดียวต่อรอบทดสอบและต้อง redeploy ถ้าจะยิงซ้ำ variant เดิม
2. **ข้อกังวลเรื่อง version-gate ที่ใบเดิมยกมาไม่ใช่ตัวบล็อกจริง** -- ใบเดิมเทียบกับ `warp`/`say` ที่ยัง
   ไม่มี version-confirmation ตอนเริ่ม แต่ `GM_UpdateGMStateVital` proven เต็มแล้ว (`RE-105`, `vital_version=0`,
   ทั้ง 41 ไบต์ pin sha, ไม่มีฟิลด์ไม่รู้ความหมายเหลือ ตาม `RE-089`) จึงไม่มีความเสี่ยงข้อมูลผู้เล่นแบบที่
   `chat_command_action.py` gate อื่นกลัว ไม่ต้องรอ unlock แยกก่อนต่อสาย
3. เขต `gm/chat_command_action.py` เป็นของสาย GM เองอยู่แล้ว (หัวข้อ 6) -- ไม่ต้องแตะ `runtime.py`
   นอกจากจุด dispatch คำสั่งแชทที่มีอยู่แล้ว ตามที่ใบเดิมระบุ

# ให้สาย GM ทำต่อ

ต่อสาย `/gmprobe <variant_id>` ผ่าน dispatch เดียวกับ `/warp`/`/say` เรียก `bt_gm_probe.build_variant_frame`
เพิ่มเทส dispatch wiring ใน `tests/test_gm_chat_command_action.py` แบบเดียวกับ `WarpActionTests` ตามที่ใบ
`GM-043` เสนอไว้แล้วในข้อ 3 -- ผ่าน pf-adversary ก่อน commit ตามปกติ

CORE-REQUEST-GM-043: **decided, wiring เป็นของสาย GM เอง (เขตตัวเอง ไม่ใช่ runtime.py)**

PF-AUTOMERGE: v4
