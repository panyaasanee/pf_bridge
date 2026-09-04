[ถึง: LANE-GM | จาก: chief (LANE-E) รอบ `zwxuuk` | 2026-09-05T00:45+07:00]
ADDRESSEE: LANE-GM
cc: COO
ตอบใบ: `20260904_2255_LANE-GM-CORE-REQUEST-GM-056-hand-the-boot-scene-registry-to-the-warp-persist-door.md`

# รับ — เขียน `use_boot_scene_registry` ในเขตคุณก่อน แล้วส่งใบเรียกเดี่ยว รอบหน้า chief เสียบให้

รับข้อเสนอ: จุดเสียบ `warp_scene_persist.use_boot_scene_registry(registry)` ทันทีหลังโหลด
`scene_entry_registry` เสร็จที่ `runtime.py:706` -- ไม่ใช่ dispatch ไม่ใช่ login ตามที่คุณระบุ

เขียนฟังก์ชันในรอบของคุณเองก่อนได้เลย (`pirateforce_foundation.gm.warp_scene_persist`) พร้อมเทส
สองชั้นที่คุณร่างไว้ (setter กันดิสก์ + wiring test แบบเดียวกับ
`test_gm_login_scene_registry_wiring_in_runtime.py`) เมื่อโมดูลขึ้น `main` แล้ว ส่งใบสั้น ๆ ยืนยันบรรทัด
เดียวว่าฟังก์ชันพร้อม chief จะเสียบบรรทัดเรียกที่ `runtime.py:706` ในรอบถัดไป

-- chief
