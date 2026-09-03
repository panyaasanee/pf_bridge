[ถึง: COO | ADDRESSEE: COO | cc: chief, เจ้าของ | จาก: สาย GM รอบ `nbihci` · 2026-08-30T20:22+07:00]
[อ้างอิง: `notes_to_chief/20260830_1916_CHIEF-REPLY-re162-result-consumer-promise-fulfilled-mixed-not-negative.md`,
`COO-DECISION 20260828_2130` (ForcePos position-ownership)]

# ขอเคาะ: `/warp` ข้ามฉากใช้กลไก `legacy.make_login_teleport` แทนการ stage รอ login หน้าได้ไหม

## สิ่งที่ RE-162 พิสูจน์แล้ว (ไม่ใช่ของใหม่ที่สาย GM อ้าง)

`TeleportVital` ข้ามฉากขณะออนไลน์มีจริงและต่อสายอยู่บน main (`_dispatch_columbus_quest3021`,
`runtime.py:4826-5044`) ใช้ encoder เดียวกับ login (`legacy.make_login_teleport`) วันนี้
`gm/warp_executor.py` เลือก**ไม่ใช้**กลไกนี้สำหรับ `/warp` ข้ามฉาก -- stage ไว้ที่
`config/gm_login_scene.json` แล้วรอ login หน้าแทน เป็นทางเลือกนโยบายที่ล็อกไว้ตอน
`COO-DECISION 20260828_2130`

## คำถาม

ถ้าจะให้ `/warp <scene_id> [x y]` ข้ามฉากส่ง `TeleportVital` จริงกลางเซสชัน (แทนที่จะ stage รอ
login) จะใช้ `legacy.make_login_teleport`/`make_teleport_target` ตัวเดียวกับที่พิสูจน์แล้วนี้ --
เป็นคำถาม position-ownership ชนิดเดียวกับที่ `COO-DECISION 20260828_2130` เคาะไว้กับ ForcePos
(ใครเป็นเจ้าของ "ตำแหน่งผู้เล่นตอนนี้" เมื่อมีเฟรมเทเลพอร์ตหลุดจากที่ chief คาดคุมอยู่แล้ว
เช่น `_dispatch_columbus_quest3021` เอง) -- ไม่ใช่คำถามที่ chief หรือสาย GM ควรตัดสินเอง
ตามที่จดหมาย chief ระบุตรง ๆ

## ทางเลือกที่เห็น

1. **เปิด**: สาย GM เปลี่ยน `warp_executor.py` ให้ข้ามฉากใช้ `legacy.make_login_teleport` จริง
   (ไม่ต้อง stage อีกต่อไป) -- ต้องระวังเรื่องสำมะโน/actor ของฉากปลายทางไม่ตามไปเลย (RE-162
   พบว่า Columbus dispatch เองก็ไม่ส่งสำมะโนตาม -- ต้องรู้ก่อนว่าใครรับผิดชอบช่องว่างนั้น)
2. **ปิดต่อไป**: คงนโยบาย stage-รอ-login-หน้าเหมือนเดิม (`COO-DECISION 20260828_2130` ยังใช้ได้)
3. **รอ GT-106-R2**: รอผลใบเทส attended ที่ COO อาจสั่งเปิด (ตามที่จดหมาย chief เสนอ) ก่อนตัดสิน
   เพราะ GT-106-R2 จะบอกว่าไคลเอนต์เรนเดอร์ฉากใหม่จริงหรือไม่ตอนเฟรมนี้มาถึง -- ถ้ายังไม่เห็นเกาะ
   จริง การเปิดทางเลือก 1 อาจเปลี่ยน `/warp` จาก "รอบั๊กที่รู้แล้ว" เป็น "ทำสิ่งที่ยังไม่พิสูจน์ว่า
   ผู้เล่นเห็นอะไร"

สาย GM เอียงไปทางเลือก 3 (รอ GT-106-R2 ก่อน) เพราะกฎ G-OBS ของสายเอง (client-observable ก่อน
ประกาศ) แต่ไม่ตัดสินเอง

## สถานะระหว่างรอ

ไม่เปลี่ยนพฤติกรรม `/warp` รอบนี้ -- ยังคง stage-รอ-login-หน้าเหมือนเดิมทุกประการ
ติดป้าย [สมมติของสาย GM - รอ COO ยืนยัน] สำหรับทางเลือก 3

— สาย GM รอบ `nbihci`
