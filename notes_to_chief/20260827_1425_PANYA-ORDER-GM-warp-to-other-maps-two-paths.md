# PANYA-ORDER 2026-08-27 14:25 +07:00 — GM ต้อง "ไปแมพอื่นที่มี NPC/มอนสเตอร์" ให้ได้: เปิดสองทางพร้อมกัน

จาก Panya (เคาะในแชท attended 14:2x — ผู้ช่วยเขียนแทน) — ถึง สาย GM (เจ้าของงาน), chief (จุดเรียกใน runtime), สาย A/B (ข้อมูลฉาก/มอน), COO, RE runner

## สิ่งที่เจ้าของต้องการ (คำของเธอ)
"เทสเกมที่ตัวเองเป็น GM แล้ว ดูว่าหน้าตา UI ต่างไหม ทำอะไรได้มากกว่าเดิมไหม และอยากใช้ warp [ชื่อแมพ] ไปแมพอื่น ๆ ที่มี NPC หรือมอนสเตอร์ spawn อยู่ **ยังไม่ซีเรียสว่าต้องเป็นตัวที่ถูกต้อง**"

## ที่เป็นอยู่ (วัด 14:15 จาก main + docs/GM_LANE.md)
- GM state หลัง login ต่อสายแล้ว (CORE-REQUEST-006) — GT-101 กำลังรันโดยผู้เทสตอนนี้ด้วยบัญชีจริง `localtest` (ไม่ใช่ `attended_test` ที่ chief อนุมัติ — ชื่อนั้นเป็น fixture ไม่ใช่บัญชีที่ client ส่งจริง; ใช้ config แยกผ่าน PF_GM_ACCOUNTS_CONFIG ตามที่อนุมัติ)
- warp: `gm/warp_executor.py` ทำได้แค่ในฉากเดียวกัน (ForcePos) และยังไม่มีจุดเรียก (CORE-REQUEST-011 [บล็อก]) · ข้ามฉากต้อง TeleportVital ที่ RE-090 ทิ้งฟิลด์ไม่พิสูจน์หลายตัว · 0x51E9 ขาเข้าถูก capture อย่างเดียว ไม่ decode เป็น GmCommand · **วิธีเปิดหน้าต่าง GM ของ client ยังไม่รู้** (RE-091: editor แยก ไม่ใช่ prefix แชต)
⇒ วันนี้ GM ไปแมพอื่นไม่ได้ทุกทาง เจ้าของสั่งเปิดสองทางคู่กัน

## ทาง ก (เร็ว ให้เจ้าของเห็นแมพอื่นภายใน 1-2 รอบ): "GM login-scene override" — ไม่ต้องมี GM UI ไม่ต้องมี TeleportVital
- สาย GM: เพิ่ม config ต่อบัญชี GM `gm_login_scene: {"localtest": <scene_id>}` (ไฟล์เดียวกับ gm_accounts หรือไฟล์แยกผ่าน env เดิม) — บัญชี GM ที่ตั้งค่านี้ **login เข้าฉากนั้นตรง ๆ** ผ่านเส้นทาง START_GAME_RES เดิม (scene_id ที่ client รับได้จริงตอนนี้พิสูจน์แล้วแค่ 1 กับ 2 — เริ่มจาก **scene 2 Prison Exile Island** ซึ่งเคยเรนเดอร์ได้จริง SCENE-001) จุดเกิด = placement index 0 ของ `.npc` ฉากนั้น (ไม่ต้องถูก ขอให้ยืนบนพื้น)
- census ของฉากนั้น: ประกอบจาก placement ของ `Data\Scene\Save\bgXXXX\bgXXXX.npc` ด้วย parser เดิม `gamedata/pf_decode_lua_npc.py` (สาย A/B มีทางนี้อยู่แล้วสำหรับ bg0001) + roster hostile ของสาย B ถ้ามีสำหรับฉากนั้น (bg0015 มี) — **ตัวไม่ถูกก็ได้ ขอให้มีของยืนอยู่** ตามคำเจ้าของ · nonclaim ต้องเขียนว่าเป็น GM shortcut ไม่ใช่ M2
- chief: ต่อจุดเรียก 2 จุด (login scene override + census ของฉากตาม scene_id) — ถ้า lane_hooks ลง main ก่อน ให้สาย GM ต่อเองใน hook
- เกณฑ์ก่อนเรียกเจ้าของ: บูต headless ไร้แฟล็ก + env config → grep คอนโซล เห็น START_GAME_RES scene_id=<N> และ census ของฉาก N > 0 actor → ค่อยเปิดใบ GT ให้ผู้เทส (กฎ "พิสูจน์ headless ก่อนเรียกคน")
- เพดานเวลา: ใบแรกรอบถัดไปของสาย GM

## ทาง ข (ของจริง): warp ข้ามฉากจากในเกม
1. RE runner: เปิดใบ RE ใหม่ **"เปิดหน้าต่าง GM editor ของ client ยังไง"** — หา trigger ของ widget ที่ RE-091 พบ (คีย์ลัด/เมนู/เงื่อนไข GMModule_Client+0x18 ที่ 0x5A19 ตั้งค่า) — นี่คือประตูของทุกคำสั่ง GM จากในเกม
2. RE runner: เปิดใบ RE ใหม่ **TeleportVital semantics** (field_0x10/0x11/0x18/0x20/0x22 + TeleportAux) ด้วยวิธีที่ RE-090 เสนอ — ถ้า static ไม่พอ ให้ใช้ live capture ตอนเจ้าของเดินทางผ่าน Columbus ครั้งแรก (M2) เป็นตัวอย่างจริง
3. สาย GM: decode 0x51E9 → GmCommand (ปิดช่องที่ dispatch.py ยังไม่ทำ) และต่อ warp_executor ในฉากเดียวกันเป็นขั้นแรก (CORE-REQUEST-011 ปลดบล็อกเมื่อ 1 ปิด)
4. เมื่อ 1+2 ปิด: warp ข้ามฉากผ่าน TeleportVital

## สิ่งที่ห้าม (เดิม)
GM เฉพาะบัญชีใน gm_accounts (ตอนนี้ = `localtest` ผ่าน config แยกของผู้เทสเท่านั้น ห้าม commit) · client ยกตัวเองเป็น GM ไม่ได้ · ผลจาก GM ไม่ใช่หลักฐาน milestone

— จาก Panya (เขียนแทนโดย attended session "กะ1") · ADDRESSEE: LANE-GM (ทาง ก ข้อ 3-4), chief (จุดเรียก), RE runner (ทาง ข 1-2)
