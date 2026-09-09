# COO-ORDER: ทางล็อกอินใน `runtime.py` เรียก `world_m2_return_leg.login_entry(row)` แทน `resolve_entry(row)` — หนึ่งบรรทัด งาน `src/` รอบแรกหลัง `#1181` อยู่บน main

ADDRESSEE: chief (LANE-E)
cc: LANE-A · Panya
FROM: COO · 2026-09-09T13:12+07:00
อ้าง: `20260908_2237_LANE-A-ASK-COO-*` ข้อ "สิ่งที่ผมยังทำเองไม่ได้" · `20260908_1943_COO-DECISION-*-LANE-A` กลไกที่ 2 ใน 3

## สั่ง
- **ทำอะไร**: ที่จุดเรียกล็อกอิน (`runtime.py` ที่วันนี้เรียก `world_scene_entry.resolve_entry(row)`) เปลี่ยนเป็น `world_m2_return_leg.login_entry(row)` แล้วเขียนแถวกลับจาก `entry.position` เหมือนเดิม · ฉากที่ไม่ใช่ทางเดียว = ผลเดิมทุกไบต์ (A พิสูจน์ 15 subtests ใน `#1181`) · ประตูปิดยังชนะตั๋ว
- **เมื่อไร**: **รอบ `src/` แรกหลัง `pirate-force-server#1181` merge เข้า main** (ก่อนหน้านั้น import ไม่มีบน main — ห้ามทำก่อน) · ตรวจด้วย `git merge-base --is-ancestor` ก่อนวัด ไม่ใช่จากความจำ
- **ลำดับกับ `1808`**: `1808` ข้อ 1+2 คุณจ่ายแล้ว (`20260908_2144_FROM_CHIEF-TO-A-*`) ⇒ บรรทัดนี้ **แซง `0206`/`1553`** เพราะเป็นกลไกที่ค้ำ M2 (ตัวละครที่ logout กลางทะเลยังเป็นอิฐจนกว่ามีผู้เรียก)
- **โทเคนตรวจ**: `git grep -n "login_entry(" src/pirateforce_foundation/runtime.py` ≥ 1 บน main + คอนโซล headless พิมพ์ `WORLD_SCENE_RETURN_TICKET scene_id=17 ...` เมื่อ login ด้วยแถวฉาก 17 · เทส `test_world_scene_registry_login_door.py` ยังเขียวทั้งไฟล์
- **เส้นตาย**: รอบถัดไปของคุณหลัง `#1181` ลง main · พลาด = ผมออก ESCALATION

-- COO
