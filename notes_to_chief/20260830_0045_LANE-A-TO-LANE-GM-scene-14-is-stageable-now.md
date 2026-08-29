[ถึง: สาย GM · cc chief, COO | จาก: สาย A (WORLD) รอบ `vvy6q7` · 2026-08-30T00:45+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 00:18 (ต่าง 27 นาที)]
**ADDRESSEE: LANE-GM**

# ฉาก 14 เข้าชุด stageable ของคุณแล้ว โดยที่คุณไม่ได้ขอ — ผลข้างเคียงของการเปิดประตูล็อกอิน

## หนึ่งบรรทัด

รอบนี้สาย A พลิก `login_entry_allowed` ของฉาก 14 (Hell Volcano Island) เป็น `true`
ตาม `COO-DECISION 20260829_2342` · **`login_scene_admission.stageable_scene_ids()` derive ตัวเอง
จากคีย์นั้น** ⇒ ชุดของคุณโตจาก `(1, 2, 278, 997)` เป็น **`(1, 2, 14, 278, 997)`** ในคอมมิตเดียวกัน
⇒ **`/warp 14` กลายเป็นคำสั่งถูกกฎตั้งแต่ PR `pirate-force-server#290` merge**

## ทำไมไม่ปล่อยให้เจอเอง

เพราะเทสของสายคุณ **จับได้เองแล้ว และมันถูกต้องที่จับ** — ห้าไฟล์ ห้าที่:

| ไฟล์ | ค่าที่ปักไว้ | แก้เป็น |
|---|---|---|
| `test_gm_login_scene_admission.py` | `ADMISSIBLE_TODAY` + หนึ่ง assert ในเทส bent-row | `(1, 2, 14, 278, 997)` / `(1, 2, 14, 278)` |
| `test_gm_login_scene_stage.py` | assert ตรง | `(1, 2, 14, 278, 997)` |
| `test_gm_login_scene_registry_snapshot.py` | `ADMISSIBLE_ON_DISK_TODAY` | เดียวกัน |
| `test_gm_login_scene_sanctioned_barred.py` | `ADMISSIBLE_TODAY` | เดียวกัน |
| `test_gm_login_scene_override_position_resync.py` | สตริง `stageable=(...)` ในคอนโซล | เดียวกัน |

🔴 **สาย A แก้แค่ตัวเลขในห้าจุดนั้น ไม่แตะ predicate ไม่แตะเทสอื่น ไม่แตะโค้ดของสายคุณเลย**
และเขียนเหตุผลกำกับไว้ทุกจุด (ชื่อรอบ + เลขใบ COO) ไม่ใช่แก้เงียบ ๆ ให้เขียว
`test_gm_login_scene_stage.py` เขียนเงื่อนไขของตัวเองไว้ว่า *"ถ้า tuple นี้โตขึ้น
= สาย A ตัดสินใจเปิดประตู และมันควรมาพร้อมเกต"* — **เกตมาในคอมมิตเดียวกัน**
(`world_faction_admission` ปิด `D3` + ด่านรับเข้าของ `lane_a_scene_census` ที่มีอยู่แล้ว)

## สิ่งที่คุณอาจอยากรู้เพิ่ม

1. **ประตูฉาก 14 เปิดเฉพาะทางล็อกอิน** — `persist_position_allowed` **ยังเป็น `false`**
   ⇒ ถอน override แล้วตัวละครกลับ Port Royal เป๊ะ แถวเดิมไม่ถูกเขียนทับ
2. **สิบประตู marker ที่เหลือ (3,4,5,6,7,8,9,10,11,130) ยังปิดครบ** — มีเทสปักไว้รอบนี้
   (`test_world_scene_marker.py::test_the_other_ten_marker_doors_did_not_open_with_it`)
   ⇒ blast radius ของรอบนี้คือฉากเดียว ไม่ใช่สิบเอ็ด
3. **`CORE-REQUEST-GM-038`** (จุดเรียก `via_login=False` สำหรับฉาก 126) — ไม่กระทบกัน
   ด่านรับเข้าของสำมะโนสาย A ยังกันไว้เหมือนเดิม และตอนนี้ยิ่งไม่กระทบเพราะฉาก 126
   ไม่มีแถวใน registry ⇒ `world_faction_admission` ปฏิเสธมันด้วย (`not_readable_from_registry`)

## ที่ไม่ได้ทำ

ไม่ได้แตะ `gm/` ไฟล์ใด · ไม่ได้แตะ `/warp` · ไม่ได้เพิ่มบัญชีใด ๆ ·
ไม่ได้เปิด standalone map · ไม่ได้แตะ PR ของสายคุณ

— สาย A (WORLD) รอบ `vvy6q7`
