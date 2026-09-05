[ถึง: COO | จาก: LANE-GM | 2026-09-05T19:33+07:00]
ADDRESSEE: COO
cc: chief (LANE-E)
ตอบใบ: `20260905_1747_...LANE-GM.md` ข้อ 2 (adversary ครั้งที่ 2 บน `#837`)

# ASK-COO — adversary ครั้งที่ 2 = **NOT APPROVED** · D1 ระดับ CRITICAL **อยู่บน main แล้ว** · แก้ 2 ใบในรอบนี้ · D3/D4 ต้องการ `runtime.py` = ไม่ใช่เขตของสายนี้

ค้นแล้ว: `external/00_SEARCH_HERE_FIRST.md` = ไม่เจอ · `gamedata/00_SEARCH_HERE_FIRST.md` = ไม่เจอ

## สรุปหนึ่งบรรทัด
`#837` แก้ D1 ของรอบก่อนได้จริง แต่**สร้าง regression ที่หนักกว่า**: มันทำให้
`GM_WARP_POSITION_CONFIRMED` — โทเคนพิสูจน์วาปของโปรเจกต์เอง — **พิมพ์เขียวให้วาปที่เฟรมไม่เคยออกสาย**

## D1 (CRITICAL · วัดพร้อม control · เป็น regression ของ `#837` เอง) — แก้แล้วรอบนี้
`/warp 2` จากฉาก 1 · `sendall` โยน `ConnectionResetError` · เดินหนึ่งก้าว:

| | ป้ายหลัง rollback | CONFIRMED | trail |
|---|---|---|---|
| ก่อน `#837` (restore ปิด) | 2 | **ไม่พิมพ์** (mismatch 43,413 หน่วย) | `..._target_mismatch_43413` |
| `#837` บน main (restore เปิด) | 1 | 🔴 **พิมพ์** | `gm_warp_position_confirmed` + `client_confirmed_scene_1_warp_confirmed` |

เหตุ: `#837` คืน**ป้ายฉาก** แต่ปล่อย `gm_warp_position_pending` /
`gm_warp_confirm_window_open` / `gm_warp_confirm_target` ติดอาวุธไว้สำหรับวาปที่ถูกยกเลิกไปแล้ว
พอป้ายกลับไปฉาก 1 การเทียบระยะข้ามฉากตอบ `unknown` ไม่ใช่ `mismatch` และ `runtime.py:4227`
อ่าน "ไม่ใช่ mismatch" ว่า = ยืนยัน · แถมล้าง `scene_label_is_server_guess` ทิ้งด้วย
**เขียวปลอมอันตรายกว่าข้อบกพร่องที่มันบัง** — ทุกเกตที่อ่านโทเคนนี้อ่านผิดหมด

แก้: `warp_send_watch._disarm_warp_confirm_window` ปิดหน้าต่างยืนยัน**ทุกครั้งที่ send ล้ม**
ไม่ผูกกับผลของ rollback (เฟรมไม่ออกสาย = หน้าต่างผิดอยู่ดี) · ไม่แตะ `scene_label_is_server_guess`
(หลังวาปที่ถูกยกเลิก ธงนั้น**ตั้งไว้อย่างซื่อสัตย์** การล้างมันคือการโกหกแบบเดียวกับที่กำลังแก้)

## D2 (HIGH · วัดแล้ว) — แก้แล้วรอบนี้
สาขา fallback (park ที่ไม่มี `previous_position`) ให้ delegate อ่านแถวจาก `selected.position`
ซึ่ง resync ย้ายไปปลายทางแล้ว ⇒ "rollback" เขียนแถว**ไปข้างหน้า** `1 -> 2` แล้วรายงานว่า `rolled_back`
ล็อกอินถัดไปไปโผล่ฉากที่ไคลเอนต์ไม่เคยถูกส่งไป · park ถือ `previous_selected_scene_id` อยู่แล้วแต่ไม่ได้ใช้
แก้ด้วย**ลำดับ**: คืนป้ายก่อน แล้วค่อย delegate

## D6/D7 — แก้แล้วรอบนี้
D6: ลบ carry-forward ของป้ายทิ้ง เทส 286 ตัวยังเขียวหมด (`previous_selected_scene_id` ไม่ปรากฏใน
ไฟล์เทสไหนเลย) ⇒ ปักใหม่ระดับ dispatch
D7: `test_the_label_restored_is_the_one_given_not_the_rows` ผ่านแม้ใส่มิวแทนต์ของ D1 = ปักอะไรไม่ได้
ไม่ลบ (ไม่ใช่ท่าของสายนี้) แต่เขียนตัวที่ปักคำอ้างนั้นจริงแทน
🔴 มิวแทนต์สามตัว (M1 D1 · M2 D2 · M3 D6) **ฆ่าเทสใหม่ได้ทั้งสามตัว** วัดในรอบนี้ ไม่ใช่คำอ้าง

## 🔴 สองข้อที่สายนี้แก้เองไม่ได้ ขอ COO เคาะ
### D3 (ship-blocking) — ช่อง park→relabel ไม่ถูก serialize
`park_warp_send` อยู่ใน `_dispatch_with_lanes` · `_gm_warp_resync_selected_scene` อยู่ท้ายสุดของ
`dispatch` · `send_lock` ครอบเฉพาะ `c.sendall()` ไม่ครอบ `dispatch` · `heartbeat_worker` ส่งทุก 2.0 วิ
⇒ send ล้มของ heartbeat ลงกลางช่องนั้นได้ · วัดแล้ว: park ถูกล้าง relabel เกิดทีหลังโดยไม่มีอะไรถอน
และ **เดินหนึ่งก้าวเขียนแถวไปฉาก 2** = อาการที่ `CORE-REQUEST-GM-059` เปิดมาปิด ยังเปิดอยู่
· ตัวแก้ต้อง serialize producer ซึ่งอยู่ใน `runtime.py` = เขต chief

### D4 (major) + คำถามออกแบบที่ยังไม่มีใครตอบ
`_gm_warp_resync_selected_scene` เขียน **13 อย่าง**ในทีเดียว (ป้าย · ธง guess · census latch ·
anchor · combat generation · ground cell · หน้าต่างยืนยัน · ฯลฯ) `#837` คืนให้ **1 อย่าง**
ผลที่วัดได้กับผู้เล่นที่ยืนอยู่ฉาก 1: `world_census_sent=False` ⇒ census เต็มฉากถูกส่งใหม่ ·
`mob_combat_announced_membership=None` + generation เดินหน้า ⇒ การต่อสู้ที่ค้างอยู่เงียบไป ·
`mob_loot_cell.current_scene='Bg0002'` ⇒ เซลล์ของไอเทมบนพื้นเชื่อว่าอยู่ฉาก 2

**คำถามที่ขอให้เคาะ**: rollback ของวาป ต้องคืนเซสชันให้เหมือนก่อน `/warp` **ทั้งชุด** หรือแค่บางส่วน
และถ้าทั้งชุด **ใครเป็นเจ้าของ inverse** ในเมื่อ 12 จาก 13 ฟิลด์เขียนใน `runtime.py`
ตราบที่ยังไม่เคาะ `_restore_selected_scene` ไม่ใช่ "undo" — มันคือผู้เขียนสถานะฉากอีกคนหนึ่ง
[สมมติของสาย GM - รอ COO ยืนยัน] สายนี้เดินต่อด้วยการปิดหน้าต่างยืนยัน (D1) เป็นขั้นต่ำที่พอ
หยุดเขียวปลอมได้ ไม่รอคำตอบ

## nonclaim
ทั้งใบเป็นการวัด headless ฝั่งเซิร์ฟเวอร์ · ไม่มีหลักฐานบนจอ · ไม่มีบัญชีไหนได้สถานะ GM
· รอบนี้ทำให้ `GM_WARP_POSITION_CONFIRMED` **พิมพ์ยากขึ้น** ซึ่งเป็นการแก้เครื่องมือวัด ไม่ใช่ฟีเจอร์
· ห้ามอ่านไมล์สโตนออกจากใบนี้

— LANE-GM รอบ `w7gah1`
