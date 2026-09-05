# KA1A-R316-RESULTS — GT-242 = **PASS สองชั้น** (ประกาศของพื้นซ้ำ items=2 หลัง reply รหัสผ่านสอง · ของอยู่บนจอ) + ข้อค้นพบ 4 ข้อให้ LANE-B + คำตัดสิน Panya 1057 (shared world)
ADDRESSEE: chief
cc: LANE-B (เจ้าของใบ/ผู้บริโภคผล) · LANE-A (census recompose) · COO · ka1-B
ผู้เขียน: ka1-A (ผู้เทส attended · Panya ขับ UI เอง) · เวลา 2026-09-05 11:02 +07:00
รอบ: R316 · boot 10:32:18-10:58:26 · BOOT_COMMIT `987edc553d05a09c30b1a360063946d0d0a9ceaf` (= หัว main ขณะนั้น) · **เซิร์ฟ command line ไร้ธง** (second-password mode = required ค่าเริ่มต้น) · client เปิดด้วย `-SecondPasswordMode bypass` ตามใบ · run DB `state\run_gt242_20260905_103218.sqlite3` ต่อจาก run DB ของ R315 (Panya อยู่เกาะคุกจุดเดิม) · **canonical sha ไม่เปลี่ยน** `4FF37060…8454` · jobs 1521 boot / 1522 teardown / 1522b release · capture `GameClient\capture_r316_20260905_103218\`

## ลำดับเหตุการณ์ (สองเซสชันใน server เดียว)
**เซสชัน 1 (login 10:34:37)** — ตามขั้นของใบ:
- 10:35:03 ขั้น 3 negative control: เปิดกระเป๋าตอนพื้นว่าง → `[G< #14] CheckSecondPwdVital 64 B` → `MOB_GROUND_WORLD_REMEMBERED scene='' new=0` → **`GROUND_REANNOUNCE_AFTER_SECOND_PWD_REFUSED scene=None reason=refused_cell_has_no_scene_to_publish`** → `[G>] V110_CHECK_SECOND_PASSWORD_OK 44 B` · ภาพ S0 `20260905_103523.png` (กระเป๋าเปิด พื้นว่าง)
- ฆ่า Fighting Fish Sergeant 0x2051 → `MOB_LOOT_DROPS_CENSUS … items=2200401:x1@0x100000` · `MOB_DROP_PRESENCE live=1 announced=1 declared_lifetime=120.0s` · ภาพ S1 `103600.png`
- ตีตัวที่สอง 0x203B นัดแรก → `MOB_COMBAT_BAR_CENSUS_RECOMPOSE actor_count=97` → **Panya เห็นของตัวแรกหายจากพื้น** → ตัวสองตาย → `MOB_LOOT_DROPS_CENSUS … 2200601 … ` · `MOB_DROP_PRESENCE live=2 announced=1 carried=1` → **ของทั้งสองชิ้นกลับมาโผล่** · ภาพ S2/S3 `103606.png` + ภาพในแชท 10:4x (Shield / Guard Hammer บนพื้น กระเป๋าเปิดและปิด)
- Panya เปิด/ปิดกระเป๋ารัว ๆ หลายครั้ง → **client ไม่ส่ง CheckSecondPwdVital อีกเลย** (เฟรมเดียวต่อเซสชัน) → ของไม่หาย · ของยังอยู่บนจอเกิน 2 นาที (เกิน declared_lifetime 120 s)
**เซสชัน 2 (relogin 10:46:27 — ka1-A สั่งทำใหม่เพื่อให้ "เปิดกระเป๋าครั้งแรก" เกิดตอนมีของ)**:
- ฆ่า Sergeant 0x2051 → `MOB_LOOT_DROPS_CENSUS … drops=2 items=2400046:x1@0x100000,2204801:x1@0x100001` · `MOB_DROP_PRESENCE live=2 announced=2`
- 10:47:15 **เปิดกระเป๋าครั้งแรกของเซสชัน** → `[G< #31] CheckSecondPwdVital 64 B` → **`GROUND_REANNOUNCE_AFTER_SECOND_PWD scene='Bg0002' items=2`** → `[G>] V110_CHECK_SECOND_PASSWORD_OK 44 B` → Panya: "ของไม่หาย ตอนเปิดครั้งแรกไอเท็มกระพริบไว ๆ ทีหนึ่งแต่ไม่หาย" · ภาพ `104708.png` (กระเป๋าเปิด ของ Blood/Exile crystal อยู่บนพื้น)
- หลังจากนั้น: `MOB_PICKUP_REQUEST_DECODED object_ref=0x00100000` → `MOB_PICKUP_REQUEST_REFUSED reason=drop_already_taken` → `MOB_PICKUP_GROUND_EXPIRY_HELD_SCENE_EMPTY expired=2 rows_left=0` (Panya คลิกเก็บของ — เซิร์ฟบอกถูกเก็บแล้ว/หมดอายุ · ไม่ใช่เป้าใบนี้ จดไว้)
- `/warp 1` → `GM_WARP_SCENE_PERSISTED scene=1` → X · teardown สะอาด (listeners 0 · integrity ok · canonical ไม่เปลี่ยน)

## ผล GT-242 → เสนอ **[PASS]** (OBSERVER_CONFIRMED 2026-09-05T10:50+07:00)
- wire (2-ใหม่)(3): CheckSecondPwd 64 B + reply 44 B และ **บรรทัด `GROUND_REANNOUNCE_AFTER_SECOND_PWD scene='Bg0002' items=2` ทันทีก่อน reply** ✓ · (4) `oldest_left` หลังขั้น 5: ไม่มีบรรทัด MOB_DROP_PRESENCE ใหม่หลัง reply (ไม่ได้ฆ่าเพิ่ม) — ตามใบ = NO-RESULT ข้อ (4) เท่านั้น แต่ (1)-(3),(5) ครบ · (6) negative control: **ไม่ใช่ "ไม่มีบรรทัด/items=0" แต่เป็น `_REFUSED reason=refused_cell_has_no_scene_to_publish`** = finding ข้อ ก
- client (7)(8)(9): ของอยู่ก่อนเปิด / ตอนเปิด (กระพริบ 1 ที) / หลังปิด ✓ · (10) สีป้ายมอนชมพูทุกตัว, ป้ายของบนพื้นสีส้ม/แดงเข้ม (Shield, Guard Hammer, Blood/Exile crystal) — จดสีอย่างเดียว · (11) dist ไม่ได้วัด → `UNMEASURED_DIST: 4/4`

## ข้อค้นพบให้ LANE-B (เรียงตามผลกระทบ)
ก. **client ส่ง CheckSecondPwdVital ครั้งเดียวต่อเซสชัน** (ครั้งแรกที่เปิดกระเป๋า) — ลำดับขั้นของใบ (negative control ก่อน) จึงใช้เฟรมเดียวนั้นทิ้ง ⇒ รอบแรกของวันนี้ hook ไม่เคยได้ทำงานกับของจริง · ใบรุ่นถัดไป: negative control ต้องอยู่คนละเซสชัน · และ **การล้างพื้นใน R309 น่าจะเกิดเฉพาะ "เปิดกระเป๋าครั้งแรก"** (nonclaim: ไม่ได้รันซ้ำแบบไม่มี fix)
ข. ตอนพื้นว่าง hook ตอบ `_REFUSED reason=refused_cell_has_no_scene_to_publish` (`MOB_GROUND_WORLD_REMEMBERED scene=''`) — ไม่มีผลบนจอ แต่เป็น REFUSED ในเคสปกติ ควรเป็น `items=0`
ค. **เฟรม `MOB_COMBAT_BAR_CENSUS_RECOMPOSE` ตอนตีมอนตัวใหม่ ไม่มีของพื้น → client ลบของตัวเก่า** จนกว่าจะมี `MOB_LOOT_DROPS_CENSUS` ครั้งถัดไป (carried=1) — บั๊กคนละตัวกับกระเป๋า เห็นชัดบนจอ (Panya สังเกตเอง) · เข้าข่ายกติกาใหม่ PANYA-DECISION 1057 ข้อ 2 (เฟรมจากการกระทำเดียวห้ามลบโลกทั้งฉาก)
ง. ของบนพื้นอยู่เกิน 120 วิบนจอ (client ไม่บังคับอายุเอง) แต่ฝั่งเซิร์ฟถือว่าหมดอายุ (`EXPIRY_HELD … expired=2`) → คลิกเก็บถูกปฏิเสธ `drop_already_taken` = สถานะจอกับเซิร์ฟไม่ตรงกัน

## nonclaims
- ไม่ตัดสินว่า 0x4B98 เป็น action เดียวที่ล้างพื้น · ไม่ได้รันคู่ควบคุมแบบไม่มี fix · ไม่ตัดสินรูป reply 44 B · ไม่แตะสาเหตุสีป้าย · ไม่พิสูจน์การเก็บของหลังปิดกระเป๋า
- ทางเบี่ยง (relogin เพื่อให้เปิดกระเป๋าครั้งแรกตอนมีของ) เป็นคำสั่งของ ka1-A ระหว่างรอบ Panya ทำตาม — ไม่ใช่ขั้นในใบ

-- ka1-A
