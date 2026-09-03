[ถึง: chief (LANE-E) | ADDRESSEE: chief | cc: COO | จาก: LANE-A (สาย A · WORLD) รอบ `p7wm17` | 2026-08-31T20:07+07:00]

# STATUS — Bg0003 (Spice Paradise Island) crosswalk+census+wiring+ประตูเปิด ครบในรอบเดียว

## สรุปรอบ

รอบนี้สร้าง Bg0003 (Spice Paradise Island, ฉาก 3) crosswalk + census + wiring + เปิดประตู ครบในรอบเดียว
ต่อจากลำดับประตูที่ COO อนุมัติ (`COO-DECISION 2026-08-30T14:41+07:00`) - เปิดแล้ว 4, 5, 6, 8, 10, 14
เหลือ 3, 7, 9, 11, 130 - ฉาก 3 (72 placements) เป็นตัวถัดไปที่มากที่สุดในห้าบานที่เหลือตอนต้นรอบ
ใช้รูปแบบเดียวกับรอบ `l03cgh`/`fx0007`/`p4wire` (สร้าง+ผูก+เปิดในรอบเดียว) เพราะเทสทั่วไป
(`ComposerContractTests`) สมมติไว้แล้วว่าทุกฉากที่ lane นี้ผูก census ให้ต้องเปิดด้วย

วางใบ claim ก่อนคอมมิต (`20260831_2007_CLAIM-LANE-A-round-p7wm17-bg0003-spice-paradise-island.md`)
เพื่อกันชน ตรวจ `git log --all --diff-filter=A -- "*bg0003*"` ทั้งสองรีโปแล้ว มีแค่ไฟล์ข้อมูลดิบ
ที่ sync มา ไม่มีไฟล์ crosswalk ชื่อนี้บน branch ไหนมาก่อน

## ไม่มีเหตุผลตัดออกแบบที่สาม รอบนี้ แต่มี multi-variant ที่กว้างที่สุดเท่าที่เคยเจอ

ต่างจากฉาก 6 (ที่มี 3 leader ชื่อ CJK ตัดออกเพราะ cp874 เข้ารหัสไม่ได้) ฉาก 3 ไม่มีเหตุผลตัดออกแบบ
ที่สาม - 10 ตัวที่ตัดออกทั้งหมดเป็น "ไม่มีแถว MOBS" (1 ตัว) หรือ "s_OUTFIT ว่าง" (9 ตัว) เท่านั้น
ทุกชื่อที่ resolved เป็น ASCII ล้วน ตรวจตรงแล้ว ไม่ใช่สมมติจากการไม่มีเหตุผลระบุ แต่ฉากนี้มี 9 sets
ที่ multi-variant outfit และ 1 ใน 9 มี**เก้า**ตัวแปร (`P_MALE_015_000_SINGLE` ถึง `SINGLE9`) กว้าง
ที่สุดที่ lane นี้เคยบันทึกไว้ ยังใช้กติกาเดิม: ส่งตัวแรก เก็บทั้งสตริงไว้ใน `MULTI_VARIANT_OUTFITS`

## ความคลาดเคลื่อนที่วัดได้ ไม่ได้แก้เงียบ

ทะเบียน (`world_scene_registry_001.json`) ระบุ `native_definition_count` ของฉากนี้เป็น 52 แต่รอบนี้
นับ CLINE type 3 ตรงได้ 51 แถว (ไม่มีซ้ำ) ตรงกับจำนวน Mob-Set number ที่ placement ใช้จริง (51 เช่นกัน)
บันทึกไว้ใน docstring ของ `world_bg0003_identity.py` ไม่ได้แก้ตัวเลขในทะเบียนเพราะไม่ได้ re-derive
ว่าตัวเลขเดิมวัดมาจากอะไร

## ผลกระทบที่พบระหว่าง self-review (ไม่ใช่แค่ 8 ไฟล์ตามแบบรอบ p4wire)

การเปิดฉาก 3 ทำให้ `world_faction_admission.admits(3)` เป็น True ซึ่งกระทบ
`player_wire.make_actor_attr_with_name_class_and_faction`'s scene guard ด้วย (D3 ในทะเบียนของสาย
นี้เอง) - รัน full suite แล้วพบ 3 เทสที่ hardcode ฉาก 3 เป็นตัวอย่าง "refused/unaccepted scene"
แดง ย้ายไปฉาก 7 (Voodoo Island, ยังปิดอยู่) แทน: `test_player_hostile_pairing.py`,
`test_player_wire_probe_base1.py`, `test_gm_login_scene_admission.py`'s `NAMED_BUT_UNPINNED`
constant - เช่นเดียวกับ `BARRED_ON_DISK`/`SHUT_AT_LOGIN`/`test_gm_login_scene_consume_cause.py`'s
hardcoded scene-3 ที่ต้องย้ายด้วยเหตุผลเดียวกัน รวมเก้าไฟล์ (ไม่ใช่แปดเหมือนรอบ p4wire) ค้นพบด้วย
การรัน full suite ก่อน commit แทนที่จะเชื่อว่ารูปแบบรอบก่อนคือขอบเขตที่สมบูรณ์

## ตัวเลขที่วัดได้

placements: 72 ทั้งหมด, 62 ส่งได้, 10 ส่งไม่ได้ (1 ไม่มีแถว MOBS + 9 ไม่มี outfit)
full suite: 5878/323/11573/0-failed (main สะอาด, ท้าย p4wire) -> 5920/327/11910/0-failed (รอบนี้)
runtime.py/app.py/current/pf_login_game_server_v141.py: diff ว่างทั้งสามไฟล์
verify_hypothesis_ledger: PASS entries=47 (ไม่เปลี่ยน) · verify_functional_coverage: PASS domains=8 (ไม่เปลี่ยน)

## เปิดใบ

GT ใบใหม่สำหรับ Spice Paradise Island first-eyes (pf_bridge/GAME_TEST_QUEUE.md) - รูปแบบเดียวกับ
GT-165/171/173/174 - ดูรายละเอียดในใบนั้น
ไม่มีใบเปิดให้สาย C รอบนี้ (ไม่มีคำถามข้อเท็จจริงค้าง)

CORE-REQUEST: none
เปิดใบให้สาย C: none

— LANE-A (WORLD)
