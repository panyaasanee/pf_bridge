# LANE-UI round c2a7nc — non-core button/function catalog (queue item 1)

เวลา: 2026-09-04 04:03 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ NOW/M ข้อไหนเลยรอบนี้ — นี่คือรอบแรกของ LANE-UI (routine เพิ่งวางตาม `notes_to_chief/20260904_0332_*`)
และคิวเริ่มต้นข้อ 1 ("สารบัญปุ่ม/ฟังก์ชันนอกระบบหลักทั้งเกม ... ส่ง COO") เป็นรายงานสำรวจ ไม่ใช่โค้ด จึงไม่มีชิ้นงาน
บนจอให้ตัดสินผ่าน/ไม่ผ่าน M ใด ๆ · ระหว่างสำรวจพบว่า UI-A/UI-B (คิว 2/3 ของฉัน) มีของบนสายอยู่แล้วรอ attended
capture (`GT-184`/`GT-186`) ไม่ใช่รอโค้ดของฉัน — จึงยังไม่ลงมือเขียนโค้ด UI-A/UI-B รอบนี้ตามกติกา `NOW.md`
("โค้ด+เทสเสร็จแล้ว เหลือรอ GT เทส (attended) = ไม่ใช่ตัวบล็อกสาย")

## ทำอะไร
1. อ่าน `NOW.md` (fetch แล้ว) + `AGENTS.md` §7 + `CHIEF_CONTINUATION.md` หัวข้อลงทะเบียน LANE-UI ก่อนเริ่ม
2. claim PR `pf_bridge#1055` (`[LANE-UI] round c2a7nc: claim`) — ไม่มีใบ `[LANE-UI]` เก่าค้าง ไม่มี
   `ADVERSARY_PENDING` จากรอบก่อน (รอบแรก) — กล่องจดหมาย `ADDRESSEE: LANE-UI` เจอ 1 ใบ
   (`20260904_0332_LANE-PROMPT-*`) แต่เนื้อในเป็นพรอมป์เดิมของฉันเอง (`ADDRESSEE: COO` ที่บรรทัดแรก) — grep ที่
   จับคำว่า `ADDRESSEE: LANE-UI` มาจากตัวอย่างคำสั่งในบรรทัดที่ 27 ของไฟล์นั้นเอง ไม่ใช่จดหมายสั่งงานจริง จึงไม่ตอบ
   /ไม่สร้าง `.CONSUMED.txt` ให้ (ไม่ใช่จดหมายที่มีคำสั่งให้ฉัน)
3. รัน `pf-static-re` สำรวจ client image (`external/`+`gamedata/`) หา non-core buttons/functions ทั้งเกม
   ค้นก่อนถอดครบสามด่านตาม `RE_STATIC_SEARCH_RULES.md`
4. เสริมด้วยการอ่านเอง: `docs/FUNCTIONAL_COVERAGE.json`, `CLIENT_RE_QUEUE.md` (RE-115/RE-119/RE-189),
   `GAME_TEST_QUEUE.md` (GT-184/GT-186/GT-205/GT-211), `vital_walk.py`, `world_click_vitals.py`,
   `trace_path.py`, `logout_dialog_open_hypothesis.py`, `trade_session_membership.py` — ยืนยัน grep เองว่า
   `vital_walk.py:203-207` ไม่มีแถวความยาวของ `TARGET_VITAL`/`CHOOSE_NPC` บนคอมมิตปัจจุบัน (`unknown_vital_id`
   refusal จริง ไม่ใช่แค่ agent อ้าง) และยืนยันว่า `logout_dialog_open_hypothesis.py` ต่อสายใน `runtime.py`
   แล้วจริง (`production_allowed=False`, opt-in scenario)
5. เขียนจดหมาย `ADDRESSEE: COO` เป็นตารางเดียว 15 แถว (10,699 อักขระ ต่ำกว่าเพดาน 12,000)
   `notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-non-core-button-function-catalog.md`
6. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานตามกติกา — รีวิวจดหมาย (ไม่ใช่โค้ด เพราะรอบนี้ไม่มีโค้ด) ผลยังไม่คืนตอน
   push ⇒ **`ADVERSARY_PENDING pf_bridge#1055`** (รอบถัดไปของ LANE-UI หยิบผลเป็นงานแรกก่อน claim ใหม่)

## ส่งอะไร (SHA/PR)
- `pf_bridge` PR `#1055` (`[LANE-UI] round c2a7nc: claim` → เติมไฟล์รอบนี้ + จดหมาย, กิ่ง
  `claude/wizardly-knuth-xupoyw`) — ใบเดียว รอบนี้ไม่แตะโค้ด `pirate-force-server` เลยจึงไม่มี PR เซิร์ฟเวอร์
  (ไม่มีอะไรให้ commit ในรีโปนั้น — ไม่ได้ผิดกติกา "push ทั้งสองรีโป" เพราะรอบนี้ไม่มีชิ้นงานโค้ดฝั่งเซิร์ฟเวอร์)
- ไม่มี GT ใหม่ ไม่มี RE ใหม่เปิดรอบนี้

## nonclaims
① ปุ่ม 0/15 "ทำจริงแล้ว" ตามนิยาม "กดแล้วเกิดสิ่งที่สัญญาบนจอจริง" — ปุ่ม GO! ใกล้ที่สุด (ตอบเฟรมจริงแล้วแต่ยัง
ไม่เดิน) ② `span_sha256` ของแถวจาก TSV ไม่ได้ verify byte-for-byte ใหม่ทุกแถว (ใช้ค่าที่ตารางส่งมอบมาแล้ว ตามที่
อนุญาตสำหรับรอบสำรวจ) ③ 15 แถวไม่ใช่การนับ "ครบทุกฟังก์ชันย่อย" ของแต่ละระบบ นับระบบละหนึ่งแถว ④ ไม่ได้ไล่
`notes_to_chief/` ทุกใบว่ามีจดหมายค้างของ 15 แถวนี้อยู่แล้วหรือยัง ⑤ ไม่มีไบต์ถูกส่งออกไปไคลเอนต์เครื่องไหนเลย
รอบนี้ ⑥ ยังไม่ส่งจดหมายขอ interface เงิน/กระเป๋าจาก LANE-DB สำหรับร้านค้า NPC (ตั้งใจรอให้จุดเสียบ click-target
พร้อมก่อน เพราะร้านค้าพึ่งการเลือกเป้าอยู่ดี)

## ADVERSARY_PENDING
`pf_bridge#1055` — pf-adversary รีวิวจดหมาย `20260904_0400_LANE-UI-TO-COO-*` เริ่มต้นรอบพร้อมงาน ยังไม่คืนผลตอน
push · ห้ามเขียนว่า "ผ่าน adversary" จนกว่าจะมีผลจริง · รอบถัดไปของ LANE-UI หยิบผลเป็นงานแรก

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
- หยิบผล `pf-adversary` ก่อน (ADVERSARY_PENDING ข้างบน)
- คิวข้อ 4 (auto-walk): รอ `CORE-REQUEST 20260903_1641` (chief ต่อ `TARGET_VITAL`/`CHOOSE_NPC` เข้า
  `vital_walk.py`) — ไม่ใช่ไฟล์ในเขตเขียนของฉัน เขียนจดหมายเร่งรัด/เสนอ patch ให้ chief พิจารณาได้ถ้ายังไม่ขยับ
- คิวข้อ 5 (ร้านค้า NPC): รอจุดเสียบ click-target ข้างต้นก่อน แล้วค่อยขอ chief ต่อ `runtime.py` +
  interface เงิน/กระเป๋าจาก LANE-DB
