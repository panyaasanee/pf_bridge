[ถึง: chief · cc: COO | จาก: LANE-GM (ร่างโดย pf-queue-author) · 2026-08-27T05:45+07:00]

# LANE-GM ร่างใบเทส attended ให้ chief ใส่คิว GAME_TEST_QUEUE.md (เลขจริงให้ chief เคาะ)

## หมายเหตุก่อนอ่าน
- ร่างนี้เขียนโดย `pf-queue-author` จากบริบท GM-001 (ดู `CORE-REQUEST-007` proposed, จดหมาย `20260827_0524`) — **ยังไม่มีเลขจริง** เขียนเป็น `GT-0NN` รอ chief grep เลขว่างถัดไปตอนใส่คิว (ตัวนับร่วมกับ `CLIENT_RE_QUEUE.md`; ที่ `main` วันนี้สูงสุดคือ `RE-083`/`GT-081` ⇒ ถ้ายังไม่มีใครจองก่อน ใบนี้ควรได้ `085` เพราะ LANE-GM เสนอ `RE-084` ไปแล้วในจดหมายแยก)
- แก้คำอ้างอิงของ `pf-queue-author`: จดหมาย `20260826_1630_PANYA-ORDER-open-Lane-GM-...md` **มีอยู่จริง** ที่ `pf_bridge/notes_to_chief/` (ทั้งฉบับ `.md` ที่ consumed แล้วในโฟลเดอร์ `consumed/` และสำเนาที่ไม่มีนามสกุล `.CONSUMED.txt`) — น่าจะเป็นเพราะ agent ที่ร่างใบนี้รันในบริบทที่ไม่เห็นไฟล์นั้น พิกัด **X 11,865 Y 6,147 (เมืองศูนย์กลาง ไม่ใช่ท่าเรือ)** มาจากจดหมายฉบับนั้นจริง ยืนยันแล้ว

## เนื้อใบ (พร้อมวางในคิว หลัง chief เติมเลขจริง)

```
## GT-0NN GM-STATE-LOGIN-VISUAL-001: หลัง GM account ที่อยู่ใน allowlist ล็อกอิน แล้วเซิร์ฟเวอร์ยิง GM_UpdateGMStateVital (0x5A19) ของตัวเอง — บนจอมีอะไรเปลี่ยนไหม  [BLOCKED-ON-WIRING — รอ CORE-REQUEST-007 merge เข้า main]
```
- objective: (claim เดียว) เมื่อบัญชี GM ที่อยู่ใน `gm_accounts` allowlist ล็อกอินสำเร็จ และเซิร์ฟเวอร์ส่ง `GM_UpdateGMStateVital` (vital id `0x5A19`, field_a=1/field_b=0/field_c=0 ตามค่า placeholder ปัจจุบันของ `gm/state_wire.py`) กลับให้ client ตัวเดียวกันโดยอัตโนมัติ — เกิดผลที่ *มองเห็นได้บนจอ* หรือไม่ (ไอคอน `bm_gm.tga` ใน chat balloon, UI element เฉพาะ GM, คำนำหน้าชื่อในแชท, หรืออะไรก็ตาม) ใบนี้ตอบแค่ "เห็นอะไรไหม" — ไม่ตอบว่าคำสั่ง GM ใด ๆ ทำงาน (นั่นคือ GM-002/GM-003 คนละใบ)
  - 🔴 คำทำนาย (เขียนก่อนบูต): field ทั้งสามเป็นค่าเดา (`[SMMUT_LANE_GM_ROR_RE]`) ⇒ คาดว่าจะไม่เห็นอะไรเปลี่ยนบนจอเลย — ถ้าคำทำนายถูก นี่คือ finding มีค่าเท่าผลบวก ไม่ใช่ความล้มเหลวของใบ

### PRECONDITION — BLOCKED-ON-WIRING · ยังบูตไม่ได้ ห้ามบูต
งานของ chief (CORE-REQUEST-007):
1. `runtime.py` หลัง login สำเร็จ เรียก `gm_accounts.is_gm(character.account_id, gm_allowlist)` แล้วถ้าจริง เรียก `gm_state_wire.for_gm_grant(legacy)` ห่อเป็น `GM_UpdateGMStateVital` ส่งให้ session นั้น
2. เลือก framing/vital helper (`make_runtime_vital` แบบ `character_list` หรือ `make_login_vital` แบบ `start_game`)
3. ตัดสิน path ของไฟล์ `gm_accounts` แล้วเติมลง server args ของใบนี้เป็นสตริงจริง พร้อมยืนยันว่ามีอย่างน้อยหนึ่ง account_id อยู่ใน allowlist ของสำเนา DB รอบนี้
4. 🔴 คอนโซลต้องพิมพ์ `GM_STATE_SEND account_id=<id> vital=0x5A19 field_a=<n> field_b=<n> field_c=<n> bytes=<n>` ตอนส่งจริง (ASCII, cp874-safe)
5. ค่าเริ่มต้นต้องยังเป็น "ไม่มีใครเป็น GM" — ผู้เทสยืนยันจากคอนโซลก่อนบูตจริง (ล็อกอินด้วยบัญชีทั่วไปก่อนหนึ่งครั้งถ้าเป็นไปได้ ต้องไม่เห็นบรรทัด `GM_STATE_SEND` เลย)
6. คนต่อสายเสร็จ กลับมาเติม server args เป็นสตริงจริง แล้วพลิกสถานะเป็น `PENDING`

- server args: (เติมไม่ได้จนกว่าจะต่อสาย)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt0NN.sqlite3 <CHIEF_FILLS_THIS_IN_AT_WIRING_TIME: gm_accounts path flag>
```
  client: `-SecondPasswordMode bypass` · ห้ามมี `--*-scenario` แม้แต่ตัวเดียว

- steps (ย่อ — เต็มอยู่ในเวอร์ชันร่างของ pf-queue-author แนบท้ายจดหมายนี้ถ้า chief ต้องการฉบับเต็มต่อคลิก):
  1. server ก่อน client เสมอ (ports 10188/10189 = 0 ก่อนเปิด client)
  2. อัดวิดีโอตั้งแต่ก่อนเข้าเกม
  3. ล็อกอินด้วยบัญชี GM ที่อยู่ใน allowlist → เข้าเกม → `T0` = เฟรมแรก HUD ครบ
  4. ยืนนิ่งที่จุดเกิด 15 วิ จดว่ามีอะไรวาบขึ้นทันทีหรือไม่
  5. เดินไป **เมืองศูนย์กลาง X 11,865 Y 6,147** (ไม่ใช่ท่าเรือ — เลี่ยงชนงานเลนอื่นแถวท่าเรือ)
  6. พิมพ์แชทสั้นหนึ่งบรรทัด (ห้ามพิมพ์คำสั่ง GM ใด ๆ — ใบนี้สังเกตเฉย ๆ) ดูคำนำหน้า/สีชื่อ
  7. ตรวจ UI ทุกมุมจอ + กวาดกล้องรอบตัว 4 ทิศ
  8. ภาพนิ่ง full-res ≥3 ใบ, จดสีป้ายชื่อทุกป้ายทีละภาพ (บังคับตามกฎ R163)
  9. teardown ปกติ, sha canonical ต้องตรง `CANON_SHA.txt` ทั้งก่อนหลัง

- pass criteria (สองชั้น ไม่มีข้อไหนเป็น "ตก" ฝั่ง client-observable):
  - wire/DB: `GM_STATE_SEND ...` ปรากฏเฉพาะบัญชี allowlist, เฟรม `0x5A19` ยาวตรงกับ span, ค่า offset ตรงกับที่ `for_gm_grant` ประกอบ
  - client-observable: บันทึกตามจริง เห็นอะไรเปลี่ยน = ผลบวก, ไม่เห็นอะไรเลย = ผลลบสมบูรณ์เท่ากัน (ตรงคำทำนาย)

- nonclaims:
  - ไม่ทดสอบคำสั่ง GM ใด ๆ (GM-002/003 คนละใบ)
  - GM ถึงสถานะที่เซิร์ฟเวอร์ตั้งใจส่งให้ ไม่ใช่หลักฐานว่าฟีเจอร์ GM ใช้งานได้
  - ไม่ยืนยันความหมายจริงของฟิลด์ +0x15/+0x18 (ของ RE-084)
  - ไม่ทดสอบเส้นทาง revoke

- result: (ผู้เทสกรอก)

## หมายเหตุปิดท้ายจาก LANE-GM
เต็มไปด้วยรายละเอียดต่อคลิกที่ `pf-queue-author` ร่างไว้ครบ (server args ฉบับเต็ม, การจับเวลา, เกณฑ์ NO-CRASH, teardown) — ตัดมาแค่โครงในจดหมายนี้เพื่อไม่ให้ยาวเกิน ถ้า chief ต้องการฉบับเต็มบอกได้ จะ paste ทั้งก้อนในจดหมายถัดไป

— LANE-GM
