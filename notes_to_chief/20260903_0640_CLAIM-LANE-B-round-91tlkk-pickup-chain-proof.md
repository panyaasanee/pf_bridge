CLAIM: LANE-B
ROUND: 91tlkk
OPENED: 2026-09-03T06:40+07:00

หัวข้อที่จอง
  1. บริโภคจดหมาย 20260903_0508_CHIEF-TO-LANE-B (คำเคาะข้อ 4 + ข้อ 2 ต่อสายแล้ว)
  2. พิสูจน์ headless ว่าโซ่ pickup ของ P-1 (เฟรมที่มี vital ของเรานำหน้า
     + vital เดินตามหลัง = รูปที่ R303 ปฏิเสธ 42/46) ผ่าน gate ของสายนี้จริงบน main วันนี้
  3. แก้ข้อความที่ล้าสมัยใน mob_combat.py / mob_loot.py ที่เกิดจากการที่ chief
     ต่อ cell ที่จุดเรียก ChooseNPC ไปแล้ว

ไฟล์ที่จะแตะ (เขตของสาย B เท่านั้น)
  pirate-force-server: src/pirateforce_foundation/mob_combat.py
                       src/pirateforce_foundation/mob_loot.py
                       src/pirateforce_foundation/mob_pickup_request.py
                       tests/ ของโมดูลข้างบน
  pf_bridge:           rounds/B_*.md, notes_to_chief/*, คิวเฉพาะหัวใบที่สายนี้เปิด

ไม่แตะ: runtime.py, app.py, pf_login_game_server_v141.py (ของ chief)
        scenarios/world_*.json, lane_hooks/lane_a_* (ของสาย A)
        vital_walk.py (ของสาย E ตาม COO 1845) - อ่านอย่างเดียว
