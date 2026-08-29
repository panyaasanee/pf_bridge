[ถึง: chief · cc: COO · Panya | จาก: LANE-GM (pirate-force-server session 8791h3) | 2026-08-27T15:24+07:00]

**เร่งด่วน — เฟรมเวอร์ชัน 1 นี้ฆ่าเซสชันเจ้าของไปแล้วหนึ่งครั้งจริง (`GT-101`, owner-observed)**

ตอบ: `notes_to_chief/20260827_1445_GT101-RESULT-client-rejects-0x5A19-version-1-error-23065-session-killed.md`
ข้อ 2 ("สาย GM: แก้ ... ห้ามเดา 3/4 ... จนกว่าจะพิน ห้ามใส่ชื่อบัญชีใดใน gm_accounts ที่เจ้าของจะบูตด้วย")

# CORE-REQUEST-016 (เสนอ · รอ chief เขียนแถวลงทะเบียน `CHIEF_CONTINUATION.md`) — guard การส่ง `GM_UPDATE_STATE_AFTER_LOGIN` จนกว่า `RE-105` จะพินเวอร์ชันที่ถูก

## เลขที่เสนอ
ทะเบียนล่าสุดที่พบใน `notes_to_chief/` มีถึง **CORE-REQUEST-014** (chief, M2 deadline risk) — เลขถัดไปที่ว่างคือ
**015** ใบนี้ขอจอง **016** เพราะ **CORE-REQUEST-015** ถูกใช้แล้วโดยใบพี่น้องรอบนี้ (login-scene-override wiring,
ดูใบแยก) เขียนพร้อมกัน สายเดียวกัน คนละจุดต่อ — grep ยืนยันก่อน push ทั้งสองใบว่าไม่ชนเลขกัน

## สิ่งที่พบ (ไม่ใช่ของใหม่ที่สร้างรอบนี้ — เป็นสิ่งที่ต้อง**หยุด**)
`runtime.py:4746` เรียก `make_gm_update_state_frame(legacy, 1, 0, 0, 0)` แบบไม่มีเงื่อนไข ทุกครั้งที่
`is_gm_account(self.token)` เป็นจริง — `1` คือ `vital_version` ที่ `gm/state_wire.py` เองติดป้ายไว้แล้วว่า
`[ASSUMED - awaiting RE]` ตั้งแต่รอบแรกของสายนี้ (ไม่เคยวัดจริง)

`GT-101` (attended, เจ้าของขับ UI เอง, `OBSERVER_CONFIRMED: 2026-08-27T14:39+07:00`) วัดผลจริงแล้ว: client
ปฏิเสธเฟรมนี้ด้วย modal error กลางจอ `網路 VitalData 版本不對 --- ErrorData=23065` (`23065` ฐานสิบ = `0x5A19`
= vital นี้เป๊ะ) แล้ว**หยุดประมวลผลสายทั้งหมด** (นับถอยหลัง 24/25/26 วินาทีบนจอ) จากนั้นปิด socket เอง
(`ConnectionResetError(10054)`) — เจ้าของต้องกด OK ปิดเกมทั้งที่แมพ Port Royal เรนเดอร์ครบข้างหลัง dialog

**ตอนนี้ config/gm_accounts.json ไม่ได้ commit อะไร (default = ไม่มีใครเป็น GM) จึงไม่มีอันตรายทันทีใน repo
เอง** — แต่ code path ที่ `runtime.py:4746` ยังไม่มี guard ใด ๆ กันการซ้ำรอย ถ้าใครเติมชื่อบัญชีจริงลง
`gm_accounts.json`/`PF_GM_ACCOUNTS_CONFIG` (ไม่ว่ารอบไหน สายไหน) ก่อน `RE-105` ปิด บัญชีนั้นจะเจอ error เดิมทันที
ที่ login

## ① โมดูล
ไม่มีโมดูลใหม่รอบนี้ — ขอแก้ที่ `runtime.py:4746` เอง (เขตของ chief) จุดเดียว

## ② สิ่งที่ขอให้ทำ
เพิ่ม guard ก่อนเรียก `make_gm_update_state_frame` ให้ default เป็น **ไม่ส่ง** จนกว่าจะมีค่าที่ `RE-105` พิน
เช่น (ข้อเสนอ ไม่บังคับรูปแบบ chief เลือกได้):
```python
# gm/state_wire.py -- proposed addition, NOT built this round (chief's call
# whether to add it there or gate purely at the call site in runtime.py)
GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED = None  # set only after RE-105 pins it
```
แล้วที่ `runtime.py:4746`:
```python
if is_gm and state_wire.GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED is not None:
    gm_pc, gm_frame = make_gm_update_state_frame(
        legacy, state_wire.GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED, 0, 0, 0,
    )
    gm_state_action = (
        "GM_UPDATE_STATE_AFTER_LOGIN", gm_pc, gm_frame, 0.0,
    )
# else: is_gm account logs in with no GM-state frame -- same as before this
# lane existed. Not sending is always safe; sending a wrong version kills
# the session (GT-101).
```
ทางเลือกอื่นที่ใช้ได้เหมือนกัน: comment เฟรมทั้งบล็อกออกตรง ๆ พร้อมอ้าง `GT-101`/`RE-105` จนกว่าจะพิน — ขอแค่ว่า
**ไม่มี account ไหนได้รับเฟรมเวอร์ชัน 1 อีก** จนกว่า `RE-105` จะปิด

## ③ ตรงไหนของ runtime
`runtime.py:4746` (ในบล็อก `if is_gm:` ปัจจุบัน หลัง `is_gm_account(self.token)` check, ก่อน
`CORE-REQUEST-007`/`MOB-PICKUP-001` comment block ที่ตามมา)

## ④ เทสที่พิสูจน์
เมื่อ chief แก้แล้ว ขอให้ยืนยัน (ไม่ใช่ของสาย GM ทำ เพราะแตะ `runtime.py`): บูต headless ด้วยบัญชี GM (ผ่าน
`PF_GM_ACCOUNTS_CONFIG` ชั่วคราว ไม่ commit) → grep คอนโซล → ไม่มี `[G>] GM_UPDATE_STATE_AFTER_LOGIN` พิมพ์เลย
จนกว่า guard จะถูกปลด — เทสนี้พิสูจน์ "ไม่ส่ง" ไม่ใช่ "ส่งถูก" (ยังไม่มีเวอร์ชันที่พิสูจน์แล้วให้เทสว่าส่งถูก)

## ⑤ ค้นแล้ว
ค้น `pf_bridge/external/00_SEARCH_HERE_FIRST.md`/`pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` แล้ว: ไม่มีตาราง
ไหนบอก vital_version ที่ถูกของ `0x5A19` — เป็นเหตุผลที่เปิด `RE-105` (static-on-bridge) แทนที่จะเดา ค้นใน
`pirate-force-server` เองด้วย: ไม่มี guard เดิมอยู่แล้วที่จุดนี้ (grep `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED`
= 0 hit ก่อนรอบนี้)

## ⑥ nonclaim
ใบนี้ไม่ได้อ้างว่าเวอร์ชันที่ถูกคือค่าไหน (ห้ามเดาตามคำสั่งเดิมของ `GT-101`) — แค่ขอให้หยุดส่งค่าที่วัดแล้วว่าผิด
จนกว่า `RE-105` จะปิดใบ ไม่กระทบ field semantics (สามฟิลด์ที่เหลือ) ที่ `RE-089` เคยพิสูจน์ไว้แล้ว
