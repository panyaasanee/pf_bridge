[ถึง: chief · cc: COO · Panya | จาก: LANE-GM (pirate-force-server session_01FAtR1ZPrzFWzaRgKKxENSe) · 2026-08-26T17:31+07:00]

ตอบ: `20260826_1630_PANYA-ORDER-open-Lane-GM-plus-attended-recon-GM-packets-already-in-client-registry.md` ส่วน ④/⑤ (เปิดเลน LANE-GM รอบแรก)

# CORE-REQUEST-006 (เสนอ · รอ chief เขียนแถวลงทะเบียน `CHIEF_CONTINUATION.md`) — ส่ง GM_UpdateGMStateVital หลัง login สำเร็จ ให้บัญชีใน gm_accounts

## เลขที่เสนอ
ทะเบียนล่าสุดใน `CHIEF_CONTINUATION.md` ณ ตอนเขียนใบนี้อยู่ที่ 001–005 (สาย A: 001-004 · สาย B: 005) — เลขถัดไปที่ว่างคือ **006** ขอเสนอเลขนี้ให้ CORE-REQUEST แรกของ LANE-GM ตามกติกา `COO-DECISION-CORE-REQUEST-numbering-is-one-counter-owned-by-chief` (หนึ่งตัวนับรวมทุกสาย ไม่ใช่ `GM-001`) — งานภายในของสาย GM เองยังเรียก "GM-001" ตามลำดับงานในใบ 1630 ต่อไป (คนละเลขกับ CORE-REQUEST ที่นี่ อย่าสับสน)

## ① โมดูล
`src/pirateforce_foundation/gm/state_wire.py` (ฟังก์ชัน `make_gm_update_state_frame`) + `src/pirateforce_foundation/gm/accounts.py` (ฟังก์ชัน `is_gm_account`) — ทั้งสองอยู่บน `main` ของ `pirate-force-server` แล้วหลัง PR รอบนี้ merge

## ② ฟังก์ชันที่ต้องเรียก
```python
from pirateforce_foundation.gm.accounts import is_gm_account
from pirateforce_foundation.gm.state_wire import make_gm_update_state_frame

if is_gm_account(login_name):
    pc, frame = make_gm_update_state_frame(
        legacy, vital_version, field_0x0b_first, field_0x0b_second, field_0x14
    )
    # ส่ง frame ให้ connection นี้
```
🔴 `vital_version` และสามฟิลด์ (`field_0x0b_first` / `field_0x0b_second` / `field_0x14`) **ยังไม่รู้ค่าที่ถูกต้อง** — layout ของ tag/offset พิสูจน์แล้ว (pin sha `03b18673...033c661` ใน `PF_SERIALIZER_FIELDS.tsv`) แต่ความหมายของค่ายังไม่รู้ (ดู RE-request ข้อ ③ ด้านล่าง) จนกว่าจะรู้ ขอให้ chief เลือกค่าเริ่มต้นที่ปลอดภัยที่สุดเอง (เช่น `1, 0, 0`) แล้วติดป้าย `[สมมติ - รอ RE]` ในจุดที่ wiring หรือรอ RE-request ตอบก่อนต่อสายจริงก็ได้ ไม่บล็อกกัน

## ③ ตรงไหนของ runtime
หลัง login สำเร็จ (จุดเดียวกับที่ CORE-REQUEST-003 ของสาย A ต่อ `world_scene_entry.resolve_entry` เข้า — หลัง character select/start ยืนยัน connection แล้ว) ก่อนส่ง frame แรกของฉาก — ส่งเป็น runtime vital เพิ่มเติมหนึ่งใบ ไม่แทนที่อะไรเดิม

## ④ เทสที่พิสูจน์
- `tests/test_gm_accounts.py` (9 เทส) — allowlist ค่าเริ่มต้นว่าง, match ตรงตัว, บัญชีนอกรายการไม่ได้อะไร
- `tests/test_gm_state_wire.py` (8 เทส) — payload ตรงตาม tag/offset ที่พิสูจน์แล้ว, ปฏิเสธค่านอกช่วง
- สวีตเต็ม 3264 เทส รันแล้วก่อนส่งใบนี้ ไม่มี regression จากรอบนี้ (18 error เดิมเป็น `ModuleNotFoundError: capstone/pefile/pytest` ที่ cloud container ไม่มี — ไม่เกี่ยวกับรอบนี้)

## ⑤ ค้นแล้ว
ค้นชุดส่งมอบ `external/` แล้ว: เจอ (`PF_PROTOCOL_REGISTRY.tsv` แถว `GM_UpdateGMStateVital`, `PF_SERIALIZER_FIELDS.tsv` 6 แถว tag/offset) · ค้น `gamedata/` แล้ว: ไม่เกี่ยวกับใบนี้โดยตรง (ใบนี้เป็นเรื่อง wire ไม่ใช่ตารางข้อมูล)

## ⑥ nonclaim
ใบนี้ไม่ได้อ้างว่า client แสดงผลอะไรเมื่อได้รับ frame นี้ — นั่นคือสิ่งที่ probe attended (แนบท้ายคิว `GAME_TEST_QUEUE.md`) ต้องยืนยันหลัง merge เท่านั้น
