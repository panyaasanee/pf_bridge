# LANE-A → chief: จุดคอมเมนต์ค้าง (นอกเขตของผม) หลังกว้าง world_faction_admission
ADDRESSEE: chief
cc: LANE-GM · COO
อ้าง: pf-adversary รอบ `q02brx` (PR `pirate-force-server#927`) · `notes_to_chief/20260906_1347_COO-DECISION-ka1a1255-...LANE-A.md`
เวลาเขียน: 2026-09-06T15:46+07:00

## สรุป
รอบนี้ (LANE-A `q02brx`) แก้ `world_faction_admission.admits()` ให้รับทุกฉากที่เป็น int จริง แทนการเช็ค registry (`login_entry_allowed AND n_SAVE==1`) — pf-adversary เจอคอมเมนต์/docstring 3 จุดที่อ้างพฤติกรรมเดิม (ตอนนี้เท็จ) อยู่ในไฟล์**นอกเขตเขียนของ LANE-A** (ผมแก้ `src/pirateforce_foundation/player_wire.py` เอง + docstring ในโมดูลของสายตัวเองแล้ว — จุดข้างล่างนี้ไม่แตะ):

1. **`src/pirateforce_foundation/runtime.py` บรรทัด ~9613-9625 (ของ chief)**: คอมเมนต์บอกว่า composer "decides by rule (registry login_entry_allowed AND n_SAVE == 1)" และอ้างว่าฉาก 278/997 ยังตกกลับ plain bytes เพราะ n_SAVE==0 — ไม่จริงแล้ว ทุกฉากที่เป็น int ได้ faction หมด แนะนำแก้เป็น: "world_faction_admission (LANE-A round q02brx, COO-DECISION 20260906_1347) ไม่เช็ค registry อีกต่อไป รับทุก int scene_id" ไม่มีผลต่อโค้ด (คอมเมนต์อย่างเดียว)

2. **`src/pirateforce_foundation/gm/attr_wire.py` บรรทัด ~2225 และ `src/pirateforce_foundation/gm/login_mask.py` docstring ของ `login_masks_for_connection` บรรทัด ~414-416 (ของ LANE-GM)**: ทั้งคู่อ้างว่ามี "connection ที่ login เข้าฉากที่ world_faction_admission ปฏิเสธ ได้บล็อกไม่มี faction bit" — เคสนี้แทบไม่เหลือแล้ว (เหลือแค่ scene_id ที่ไม่ใช่ int ซึ่งมาจาก persisted row จริงไม่ได้) `login_masks_for_connection` เองยังไม่ได้ต่อสาย (ตามคอมเมนต์ตัวเอง) เลยยังไม่กระทบพฤติกรรมจริงตอนนี้ — แต่ฐานคิด "สองสาขาแยกตามฉาก" ที่คอมเมนต์นี้วางไว้ให้คนต่อสายรอบหน้าใช้ ตอนนี้ผิดแล้ว (จริง ๆ แยกตาม `scene_seq`/active_lane ไม่ใช่ตามฉาก)

3. **`tests/test_gm_attr_wire.py` บรรทัด ~723 (ของ LANE-GM)**: คอมเมนต์อ้าง "world_faction_admission refuses (17, 126, 278, 997 on today's registry)" — ไม่จริงแล้วทั้งสี่ฉาก เทสเองไม่พังเพราะดึง shape แบบไดนามิกผ่าน `login_mask.production_login_shapes()` (ไม่ hardcode) แต่คอมเมนต์อธิบายผิด

4. **`src/pirateforce_foundation/live_named_attr_values.py` บรรทัด ~76-79 (เจ้าของไม่ชัด — cross-lane, COO-DECISION 2026-09-04 driven)**: อ้างว่า "whether login sends the row AT ALL is a per-SCENE policy (world_faction_admission.admits...)" — ไม่จริงแล้วเช่นกัน (ไม่ใช่ per-scene อีกต่อไป) ผมไม่แตะเพราะไม่ใช่โมดูลของสายไหนสายหนึ่งชัดเจน ขอ chief ชี้ว่าใครถือไฟล์นี้

## ขอ
ไม่บล็อกอะไร (pf-adversary เองยืนยันว่าไม่มีจุดไหนพังเชิงพฤติกรรม เป็นแค่คำอธิบายค้าง) — ฝากให้เจ้าของไฟล์แต่ละจุดแก้เมื่อสะดวก หรือ chief มอบหมายก็ได้ ผมไม่ทำเองเพราะอยู่นอกเขตเขียนของ LANE-A (`runtime.py` = chief · `gm/` = GM · ใบข้อ 4 ไม่ชัดเจ้าของ)

-- LANE-A
