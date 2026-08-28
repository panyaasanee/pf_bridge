# R208 (x6a85q) — CORE-REQUEST-023: movement speed wired · fabricated MP/stat values caught and rejected before push · RE-122 opened

2026-08-28T07:35+07:00

## สรุปสั้น

ต่อสาย CORE-REQUEST-023 ต่อจาก R203/R204 (class+level ต่อไปแล้ว): เพิ่ม **movement speed**
(`BasicAttr +0x54`, f32 tag `0x2A`, mask `0x0040`, ค่า `400.0`) เข้า login ActorAttr ของผู้เล่น
`pirate-force-server@dc2c521` (push แล้ว รอ merge PR #181) + companion `pf_bridge@cf52a60`
(push แล้ว รอ merge PR #280)

**เหตุการณ์สำคัญของรอบนี้ ไม่ใช่ speed field — คือการจับบั๊กก่อน push**: subagent ที่ผมมอบหมายให้ทำ
CORE-REQUEST-023 ทั้งก้อน (MP + 5 stat + speed) ส่งค่ากลับมาโดย **ประดิษฐ์ตัวเลข** MP current/max = 100/100
และ STR/CON/DEX/INT/PER = 10 ทุกตัว โดยไม่มีแหล่งข้อมูลจริงรองรับเลย ผมตรวจแหล่งก่อนเชื่อ (G1: ห้ามอ้างจาก
แหล่งเดียว) พบว่า:
- `reports/PF_JOB001_CHARCREATE_CLASS_STATIC_BOUNDARY_20260816.md`: ตาราง `CHARCREATE_CLASS` ไม่มีคอลัมน์
  stat score เลย (37 คอลัมน์ทั้งหมดเป็นไอคอน/equipment/skill string)
- `reports/PF_STATS_PROG001_..._20260818.md` §8.4: บอกตรง ๆ ว่าตัวเลขจริงต่อระดับ/อาชีพ "remain unknown"

ถอดค่าที่ประดิษฐ์ทั้งหมดออกก่อน push (เก็บแค่ตำแหน่ง wire ที่พิสูจน์แล้วไว้ในคอมเมนต์ ไม่เอาค่าออกไปด้วย)
เหลือแค่ speed=400 ที่มีหลักฐานรองรับจริง (ดูล่าง) เขียนเทสใหม่ที่ยืนยันด้วยว่า MP/stat bits **ไม่ถูกส่ง**
กันรอบหน้าเผลอเติมค่าประดิษฐ์กลับมาโดยไม่รู้ตัว แล้วเปิด `RE-122` (`pf_bridge/CLIENT_RE_QUEUE.md`) ให้ RE
runner หาค่าจริงแทน

## pf-adversary

เรียกจริงก่อน push — คำตัดสิน: ไม่พบบั๊กฟังก์ชัน พบจุดเดียวที่เป็นปัญหาจริง (evidence-labeling ไม่ใช่ bug):
docstring ที่ผมเขียนอ้างว่าค่า speed=400 มาจาก "เจ้าของเห็นเองบนจอจาก probe session" โดยไม่มี citation ที่
ตรวจสอบได้จากใน repo นี้เอง (จริงอยู่ว่าที่มาจริงคือ `PANYA-DECISION 20260828_0125` แถว ⑦ ซึ่งอยู่ใน pf_bridge
คนละ repo — adversary มองไม่เห็นจากฝั่ง server) — **adversary เจอหลักฐานที่แข็งกว่าเองด้วย**:
`reports/PF_RESCUE_AND_DEATH_ESCALATION_STATIC_20260819.md` บรรทัด ~281 ถอดรหัส ctor ของ `BasicAttr` เจอว่า
client เขียน `400.0f` ลง object offset `+0x54` (ช่องเดียวกับ speed) เองตั้งแต่สร้าง object ก่อนรับข้อมูลจาก
สายเลย — เป็นหลักฐาน static [MEASURED] ที่ยืนยันตัวเลขเดียวกับที่เจ้าของเห็นบนจอ (สองแหล่งอิสระตรงกัน)
แก้ docstring อ้างทั้งสองแหล่งให้ตรวจสอบได้ push commit แยก (`dc2c521`)

รายละเอียดครบ: ยืนยัน byte layout ด้วยมือ (mask `0x034E` ตรง), ยืนยัน `NPC_HOSTILE_PLAYER_FACTION_WIRE_DELTA`
invariant ยังจริงด้วยเทสจริง (ไม่ใช่ vacuous), grep ทั้ง repo หาจุดที่ crosscheck byte กับฟังก์ชันนี้ — ไม่มีจุด
ไหนพัง, ยืนยันว่าการถอด MP/stat ออกสะอาดจริง (ไม่มี bit ไหนหลุดค้าง), รัน full suite + ledger เองอิสระ ตรงกับที่
ผมอ้าง

## เทส

`tests/test_player_wire_probe_base1.py` เขียนใหม่ (ตัดส่วน MP/stat ออก, เพิ่มเทสยืนยันว่าไม่ถูกส่ง) +
`tests/test_player_name.py` ปรับ hardcoded layout ตาม · golden hash 3 คู่คีย์ (`foundation_v1.json`,
`item_lifecycle_v1.json` ×2) regenerate จากโค้ดจริง (สคริปต์ capture-and-diff ไม่ใช่พิมพ์ค่าเอง) · สวีตเต็ม
`3594 passed, 0 failed` (23 error เดิม capstone/pefile/tools ไม่ใช่ของใหม่ — ยืนยันด้วย `git stash -u` diff
โดย adversary เอง) เขียว(cloud sanity) · ledger verify PASS entries=47

## CORE-REQUEST

CORE-REQUEST-023: speed wired (ครั้งนี้) — class/level wired แล้ว (R203) — MP/5 stat ยังไม่ต่อ รอ RE-122

## เปิดใบให้สาย C

`RE-122 PLAYER-STANDARD-STATUS-AND-CHARCREATE-SCORE-VALUES-001` (`pf_bridge/CLIENT_RE_QUEUE.md`) — ขอค่า MP
current/max และ STR/CON/DEX/INT/PER จริงของ level 1 class 1 ตำแหน่ง wire ปิดแล้ว เหลือแค่ตัวเลข

## GAME_TEST_QUEUE

ไม่เปิดใบใหม่รอบนี้ — เหตุผล: หลักฐาน ctor-default ข้างต้นแปลว่า client เดินที่ speed 400 อยู่แล้วโดยดีฟอลต์
แม้เซิร์ฟเวอร์จะไม่เคยส่งฟิลด์นี้มาก่อนเลยก็ตาม การส่งค่าเดียวกันอย่างชัดเจนตอนนี้จึงเป็นความถูกต้อง/ความสมบูรณ์
ของ wire (ตรงตามที่ `PANYA-DECISION 0125` ต้องการ — "ครบสมบูรณ์ที่สุดเท่าที่รู้ ไม่ใช่ขั้นต่ำที่พอไม่พัง") แต่
**ไม่มีอะไรต่างบนจอให้ผู้เทสสังเกตได้จริงจากการเปลี่ยนนี้อย่างเดียว** (ก่อน/หลังน่าจะเดินเร็วเท่ากัน) การเปิดใบ
เทสแยกตอนนี้จะทดสอบสิ่งที่คาดว่าเหมือนเดิม ไม่ใช่ signal ใหม่จริง — รอจนกว่า RE-122 ปิดแล้วต่อ MP/stat ครบ
(ซึ่งน่าจะมีผลบนจอเห็นได้จริง เช่น หน้าต่างสถานะ K ไม่ว่างเปล่า) ค่อยเปิดใบรวมคราวเดียวสำหรับ "probe base 1
เต็มรูปแบบ"

## nonclaims

- speed value 400.0 [MEASURED] จาก ctor default + owner probe — ไม่ได้พิสูจน์ว่า server ต้อง override ค่านี้
  เสมอไปในอนาคต (ถ้าสูตร progression จริงบอกว่า speed ต่างกันตาม level/gear จะต้องกลับมาแก้)
- MP/5 stat wire position [MEASURED] (สองแหล่งสำหรับ MP, แหล่งเดียวสำหรับ 5 stat — RE-122 ควรหาแหล่งที่สอง
  ให้ 5 stat ด้วยถ้าเป็นไปได้)
- ชื่อตัวละคร x1/x37 ยังพักตามที่ R203 ตัดสินไว้ (ไม่แตะรอบนี้)
- lane_hooks สำหรับ actor-entry composer (§18 ข้อ 1 ของ prompt เดิม) ยังไม่ได้ตรวจสถานะจริงรอบนี้ — บันทึกไว้
  ใน registry ว่า R203 บอกว่า "ยังไม่เริ่ม" แต่ R195 (ก่อน R203) มีรอบชื่อ "lane-hooks-skeleton" แล้ว — ไม่ได้ตรวจ
  ว่าขัดแย้งกันจริงไหมรอบนี้ (นอกขอบเขต PR เดียวเรื่องเดียว)
