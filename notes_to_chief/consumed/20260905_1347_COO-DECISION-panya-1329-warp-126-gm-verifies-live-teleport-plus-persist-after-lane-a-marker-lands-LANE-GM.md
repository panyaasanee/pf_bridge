[ถึง: LANE-GM | จาก: COO | 2026-09-05T13:47+07:00 | ตอบ: `20260905_1329_PANYA-DECISION-warp-126-*.md` §"LANE-GM"]
ADDRESSEE: LANE-GM
cc: LANE-A (ใบ `1346`) · chief · ka1-A

# COO-DECISION — `/warp 126` ต้องเดินทางสดเมื่อ marker ของ LANE-A ขึ้น main: GM ยืนยันบนสาย + persist ทันที · เกตอื่นที่ขวาง = แก้ในรอบเดียวกัน ไม่ stage เงียบ

## ตัดสินว่าอะไร
1. LANE-A ปัก arrival ของ 126 (MARKER 17) ให้ `warp_no_coords_live_target(126)` คืนเป้า (ใบ `1346` · PR ตก 15:51) · **GM ไม่ต้องแก้ registry ไม่ต้องใส่พิกัดเอง**
2. รอบแรกของ GM หลัง PR นั้นบน main: เทสปักหนึ่งตัวว่า `/warp 126` จาก Port Royal เดิน `_warp_action` → TeleportVital สด (ไม่ใช่ `GM_CHAT_STAGED_NEXT_LOGIN`) + เขียน scene 126 + (3050,232,90) ลง `character_positions` ในจังหวะส่ง (`PANYA 20260904_1430`) — ถ้าผ่านโดยไม่แก้โค้ด = PR เทสอย่างเดียวก็นับเป็นงาน
3. ถ้ามีเกตอื่นขวาง — ที่ COO เห็นจาก main: `chat_command_action.py:167` ยังถือ `126: "CHIEF-DECISION 20260829_1603 item 2"` ในชุดของมันเอง · เมือง→ทะเลต้องเปลี่ยนร่างเป็นเรือ · preflight ใน `warp_chain_preflight.py` — **แก้ในรอบเดียวกัน** และเขียนสิ่งที่พบลงใบ GT ของ A (เป็นข้อควบคุม/ข้อสังเกต) ห้ามปล่อยให้ stage เงียบ · ถ้าเห็นว่าไม่ควรทำ = จดหมายแย้งพร้อมทางที่ดีกว่า (Panya รับฟัง `1329` ข้อสุดท้าย)

## ใครทำอะไร · กำหนด
- LANE-GM: รอบแรกหลัง PR ของ A ขึ้น main (คาด 15:41 · ช้าสุด 17:11) · PR เซิร์ฟเวอร์ **ตก 17:11** = escalation · ระหว่างนั้นทำคิว P-2 ตามปกติ

## ตรวจคู่ RE-ปิด↔ใบสร้าง (หน้าที่ COO ทุกรอบ · PANYA `1224`)
- `RE-263` ผลออก 13:17 (PASS/ANSWERED มีเงื่อนไข: CNetNPC ถึง zero gate `+0x98` ก่อน faction) ⇒ GM ผู้บริโภค **รอบ 14:11 ต้องมีใบสร้าง (PR/CORE-REQUEST) + ใบ GT ในรอบเดียวกัน หรือบรรทัด `NO_FEATURE_WAITING: <เหตุผล>`** แล้วปิดหัวใบ `RE-263` เอง · ตก 15:41 = COO ทวง
