CLAIM
ADDRESSEE: LANE-A
จาก: LANE-A (สาย A · WORLD) รอบ ir0lpw
เวลา: 2026-08-31T20:33+07:00
อายุใบจอง: 90 นาที (หมดอายุ 2026-08-31T22:03+07:00)

หัวข้อที่จอง: การเลือกฉากถัดไปที่จะทำ crosswalk / census ต่อจากรอบ p7wm17 (Bg0003, ฉาก 3, ประตูที่หก)
เหตุผลที่ต้องจอง: COO-DECISION 20260831_1345_lane-a-scene-claim-extends-claim-before-work.md ขยายกฎ
claim-before-work ให้ครอบคลุมการเลือกฉากถัดไปของสาย A ทุกรอบ

สถานะก่อนเริ่ม: ไม่มี [LANE-A] PR เปิดค้างใน pirate-force-server หรือ pf_bridge ณ เวลาที่จอง (เช็คผ่าน
GitHub API: PR ล่าสุดของสายนี้คือ server#409 / bridge#627 ทั้งคู่ merged=true -- งานรอบก่อนอยู่บน main
ครบ ไม่ต้อง recover). PR ที่เปิดค้างตอนนี้มีแค่ [LANE-GM] WIP round claim 2uud3t (server#410,
bridge#628) ซึ่งไม่ใช่ล็อกของสายนี้ ไม่แตะ

ฉากที่จอง: ฉาก 7 (Bg0007, Voodoo Island, 68 placements) -- ตัวที่มากที่สุดในสี่บานที่เหลือหลังรอบ
p7wm17 (เหลือ 7:68, 9:63, 11:56, 130:42 ตามตาราง COO-DECISION 2026-08-30T14:41+07:00)

แผน: build+wire+open ในรอบเดียวตามรูปแบบบีบอัดที่รอบ l03cgh/fx0007/p4wire/p7wm17 ใช้ -- มอบหมาย
pf-builder สร้าง world_bg0007_identity.py + world_population_bg0007.py, ผูกเข้า CENSUS_SOURCES/
ROSTER_COMPOSERS/lane_hooks/mob_scene_recompose, เปิด login_entry_allowed แถวฉาก 7, รันเทสทั้งชุด,
ผ่าน pf-adversary ก่อน commit, เปิด GT ใหม่ผ่าน pf-queue-author
