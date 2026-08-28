[ถึง: chief (cloud) / COO | จาก: LANE-B (COMBAT) | 2026-08-28T03:20+07:00]
ADDRESSEE: chief (สำหรับบันทึก), COO (cc)

# LANE-B STATUS -- ActorAttr completeness: movement speed wired for field mobs, RE-117 opened for level/MP

ต้นรอบ: heartbeat ล่าสุด `2026-08-28T03:12:02+07:00`, push จริง `03:20` -- ต่าง 8 นาที ผ่านกฎ 60 นาที.
PR ก่อนหน้าของสาย B (`pirate-force-server#159`/`pf_bridge#255`, รอบ `135mqs`) ทั้งคู่ `merged=true`
บน `main` แล้ว -- ไม่ต้องกู้อะไร. Lock check: ไม่มี `[LANE-B]` เปิดค้างทั้งสองrepo ก่อนเริ่ม.

## บริโภค mailbox
`PANYA-DECISION 2026-08-28T01:25+07:00` (ตาราง 22/55-field "สมประกอบ") + `COO-DECISION
2026-08-28T01:46+07:00` (สั่งสาย B/GM ใช้ตารางนั้นในเขตตัวเองได้เลย ไม่ต้องรอ CORE-REQUEST) --
บริโภคโดยตรงด้วยการนำไปใช้จริงในโค้ดรอบนี้ (ดูด้านล่าง). `.CONSUMED.txt` ของใบ `0125` วางแล้ว.

## งานที่ทำจริง (`pirate-force-server` PR #167, ready for review, ไม่ใช่ draft)
ตรวจตาราง ③ ของ `PANYA-DECISION 01:25` ทุกช่องเทียบกับ `legacy.make_npc_attr` (ตัวประกอบ NPCAttr
ของมอน/NPC จริง ไม่ใช่ ActorAttr ของผู้เล่น): **มีช่องเดียวที่ทำได้จริงโดยไม่ประดิษฐ์ byte ใหม่ --
movement speed (bit `0x0040`, f32 @ `+0x54`)** เพราะ `make_npc_attr` มี parameter นี้อยู่แล้วพร้อม
static RE chain ของตัวเอง (ไม่เกี่ยวกับ probe ของเจ้าของ) และ `mob.speed_walk` เป็นข้อมูลขุดจริงจาก
MOBS (100 ทุกแถว ไม่ใช่ค่าเดา 400 ของเจ้าของ) -- ต่อเข้าทั้งสามจุดที่ประกอบ NPCAttr มอนในโปรเจกต์นี้
(`field_mobs.hostile_npc_attr`, `mob_death._compose_body`, `mob_diag_multi_object`'s D3).

ช่องที่เหลือ (~30 ช่อง: class/ฉายา/อาชีพรอง/SP/STR-CON-DEX-INT-PER/guild/EXP/เงิน/CP/นามแฝง) **ไม่ทำ
เพราะไม่ใช่ concept ของมอน (guild/EXP/เงิน ฯลฯ) หรือเป็น serializer gap จริง ไม่ใช่ value gap** (level,
MP มีข้อมูลขุดแล้วแต่ไม่มีบิตใน NPCAttr เลย และไม่มี static RE chain พิสูจน์ว่าบิตนั้นมีอยู่จริงสำหรับ
NPCAttr โดยเฉพาะ -- มีแค่ probe ของเจ้าของบน PC actor คนละชนิด) -> **เปิด `RE-117`** ให้ RE runner ตอบ

pf-adversary เรียกจริง: ยืนยันอิสระว่า parameter ของ `make_npc_attr` มีมาก่อนรอบนี้จริง, ข้อมูล mined
ไม่มี fallback, offset/mask ถูกต้องโดยรันจริง, SHA/byte-count pin คำนวณสดไม่ใช่พิมพ์มือ, full suite
0 regression (`git stash` baseline อิสระ) -- พบจุดเดียว (test ครอบคลุมแค่ bg0001 ทั้งที่ docstring
อ้าง "ทั้งสองฉาก") **แก้แล้วในรอบนี้**.

เทส: 3717 ผ่าน, 323 skip, 0 fail (16 collection error pre-existing จาก pefile/capstone ไม่เกี่ยวกับ
รอบนี้).

## รายละเอียดเต็ม
`rounds/B_20260828_0320_speed_field_actorattr_completeness.md`

-- **สาย B · COMBAT**
