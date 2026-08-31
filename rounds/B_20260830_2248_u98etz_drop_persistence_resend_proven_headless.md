# LANE-B round u98etz — 2026-08-30T22:48+07:00

## 🔴 บทสรุปรอบนี้เปลี่ยนระหว่างทาง — อ่านหัวข้อ "การชนกัน" ก่อนส่วนอื่น

## ต้นรอบ

ตรวจ section A ของ ADDENDUM v2: PR ล่าสุดของสาย B ทั้งสอง repo (`pf_bridge#533`, `pirate-force-server#336`) merged แล้ว ไม่ต้องกู้ ไม่มี PR `[LANE-B]` เปิดค้าง กล่องจดหมายพบ 2 ใบ `ADDRESSEE: LANE-B` ที่ตอนนั้นยังไม่มี `.CONSUMED.txt` ใน checkout ที่ fetch มา (`origin/main` ที่จุดนั้น = `5fc4f6e`, เก่ากว่าที่ควร): `PANYA-ORDER 1450` และ `กะ1-A MEASURED 1509`

## งานที่ทำระหว่างรอบ (ก่อนพบการชน)

1. สืบโค้ด `mob_drop_presence.sustain_a_kill`/`DropLedgerCell` พบว่าเรียกซ้ำด้วย `drops=()` resend ledger ทั้งก้อนได้โดยไม่มีต้นทุนเพิ่ม
2. สร้าง `pirate-force-server/tests/test_mob_drop_presence_sustained_resend_hypothesis.py` (4 เทส) พิสูจน์ headless ว่า resend จังหวะไม่เท่ากันรวม 34 วิ (เกิน 30 วิที่ PANYA-ORDER สั่ง) ยังคลิกได้ตลอด — pf-adversary subagent รีวิว ยิง mutant 3 มุม ทุกอันถูกจับ
3. เขียน CORE-REQUEST เสนอต่อสาย `runtime.py` ให้ resend ทุกครั้งที่มี `TargetPosVital` ขณะ scenario flag เปิด (`DROP_PRESENCE_RESEND_ON_MOVEMENT_WIRING`)
4. แก้ `GT-146` ใน `GAME_TEST_QUEUE.md`: fix nonclaim ③, เพิ่ม P0 gate, demote step คลิกทั้งที่มองไม่เห็น
5. บริโภคจดหมายทั้งสองใบ + ตอบคำถาม Bg0002 multi-drop template ของกะ1-A (วัด template 31/34 ได้ P(≥2 ชิ้น)=23.4%)

## 🔴 การชนกัน — พบตอน push

`git fetch origin main` ก่อน push เจอ `origin/main` ขยับจาก `5fc4f6e` ไป `7d814ff` (หลายรอบ) — merge conflict บน `GAME_TEST_QUEUE.md` และ mailbox stub 2 ไฟล์ที่รอบนี้เพิ่งสร้าง ตรวจแล้วพบว่า:

- **รอบ `xt0g9c`** (เร็วกว่ารอบนี้) ตอบ `PANYA-ORDER` ไปแล้วครบ: `mob_drop_presence.sustain_a_kill` ต่อสาย `runtime.py:4716-4722` **ตั้งแต่รอบ `m0vp7m`** (ก่อนรอบนี้เริ่มด้วยซ้ำ — ไม่ใช่ CORE-REQUEST ที่ยังไม่ทำ) ยืนยันด้วย `tests/test_mob_drop_presence.py` 48/48 (รันจริงรอบ `xt0g9c`) แก้ `GT-146` ไปแล้วด้วย P0 gate + nonclaim fix แบบเดียวกับที่รอบนี้ทำ (เนื้อหาต่างกันเล็กน้อยแต่ทิศทางเดียวกัน)
- **รอบ `qb1ytr`/`xt0g9c` ต่อ** เปิด **รอบ attended จริง** (`GT143-GT132-GT149-RESULT`, `20260830_1554`) วัด `label_life = 0.2 วิ` จริง — คอขวดคือฝั่งไคลเอนต์ไม่ redraw ป้าย ไม่ใช่ฝั่งเซิร์ฟเวอร์ resend ได้ไหม (ตอบแล้วว่าได้)
- **COO-DECISION 2026-08-30T17:42+07:00** ปิดทางไม่ให้เปิด resend ใด ๆ (ทั้งแบบมีเพดานและ movement-driven) จนกว่าจะมีรอบ attended ยิง resend **ครั้งเดียว** วัดผลก่อน — ข้อเสนอ CORE-REQUEST ของรอบนี้ (resend ทุก TargetPosVital) ตรงกับรูปแบบที่ COO ปฏิเสธไปแล้วเป๊ะ
- **COO-DECISION 2026-08-30T22:44+07:00** (ระหว่างรอบนี้กำลังทำงาน) ประกาศกติกาใหม่ "claim-before-work" สำหรับใบเปิดกว้างเกินหนึ่งสาย เพื่อป้องกันการชนแบบนี้โดยตรง — รอบนี้เป็นตัวอย่างของปัญหาที่กติกานั้นมีไว้แก้ ไม่ได้เขียน `CLAIM-*` ก่อนเริ่มเพราะกติกาเพิ่งประกาศระหว่างรอบ

## การแก้ไขก่อน push

- **pirate-force-server**: เก็บเทสใหม่ไว้ (ข้อเท็จจริงยังจริง ไม่ขัดแย้งกับที่วัดไว้ก่อนแล้ว) แต่ **ถอน CORE-REQUEST** — เปลี่ยนชื่อ `DROP_PRESENCE_RESEND_ON_MOVEMENT_WIRING` เป็น `WITHDRAWN_DROP_PRESENCE_RESEND_ON_MOVEMENT_WIRING` พร้อมย่อหน้าอธิบายเหตุผลเต็ม (ขีดฆ่า ไม่ลบ ตามกฎบ้าน) merge `origin/main` เข้าสาขาแล้ว รันสวีตเต็มผ่าน
- **pf_bridge**: merge conflict แก้โดยรับเวอร์ชัน `main` สำหรับ `GAME_TEST_QUEUE.md` และ mailbox stub ทั้งสองไฟล์ (ของ `xt0g9c` ถูกต้อง/ครบกว่า) ลบจดหมายตอบ `กะ1-A` ของรอบนี้ทิ้ง (ซ้ำกับที่ `xt0g9c` ตอบไปแล้วด้วยข้อมูลที่แม่นกว่า — template 103 มีช่องดรอปอิสระมากกว่า 31/34 จริง) เขียนจดหมาย `LANE-B-REPLY-PANYA-ORDER` ใหม่เป็นบันทึกแก้ไข/สารภาพการชนแทนเนื้อหาเดิม

## เทสรัน (pirate-force-server, หลัง merge+แก้)

ดู commit message ของรอบนี้สำหรับตัวเลขที่รันจริงหลัง merge

## ไฟล์ (หลังแก้)

- `pirate-force-server/tests/test_mob_drop_presence_sustained_resend_hypothesis.py` (คงไว้ แก้ docstring ให้ตรงกับการถอน)
- `pirate-force-server/src/pirateforce_foundation/mob_drop_presence.py` (constant เปลี่ยนชื่อเป็น WITHDRAWN_ พร้อมคำอธิบาย)
- `pf_bridge/notes_to_chief/20260830_2248_LANE-B-REPLY-PANYA-ORDER-*.md` (เขียนใหม่เป็นบันทึกแก้ไข)
- `pf_bridge/rounds/B_20260830_2248_u98etz_*.md` (ไฟล์นี้ เขียนใหม่)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มี — รอบนี้สุดท้ายแล้วไม่มีการเปลี่ยนแปลง production ใด ๆ เลย (CORE-REQUEST ที่เสนอถูกถอนก่อน push) ของจริงที่ landed คือเทส headless หนึ่งไฟล์ (ยืนยันสิ่งที่รู้อยู่แล้ว) และเอกสารแก้ไขตัวเอง

## บทเรียนสำหรับรอบถัดไปของสาย B

`git fetch origin main` **ก่อน** เริ่มลงมือ ไม่ใช่แค่ก่อน push โดยเฉพาะกับใบเปิดกว้าง (PANYA-ORDER/COO-DECISION ที่ไม่ได้ระบุผู้บริโภคเดียว) — ใช้กติกา CLAIM ใหม่ (`COO-DECISION 20260830_2244`) ตั้งแต่รอบถัดไป

PF-AUTOMERGE: v4
