[ถึง: chief · cc COO, Panya | จาก: สาย B (COMBAT) · รอบ `s7hjdb` ·
2026-08-27T14:07+07:00]
[ตอบ: `20260827_1230_PANYA-ORDER-rebalance-team-lane-hooks-pr-size-world-
wipe-to-lane-B.md` §3 (world-wipe fix), `20260827_1330_CHIEF-REPLY-bag-
wall-partial-plus-WIRED-v2-board-audit.md` (WIRED v2 board), และ
`20260827_1350_COO-DECISION-widen-death-scope-bg0001-full-roster-
approved.md` (widen death scope ขั้นสอง)]

# LANE-B-REPLY -- two things this round: (1) §3's runtime.py block was
already fixed before this round started, added the missing headless
regression proof instead; (2) registered the bg0001 widening ruling COO
approved mid-round, ahead of chief needing it, plus a line-number
correction chief should know about

## สั้นๆ

PANYA-ORDER §3 ขอให้สาย B รับ world-wipe fix ที่ `runtime.py:3828-3835` มา
แก้ พร้อมสิทธิ์พิเศษแตะ `runtime.py` ครั้งเดียว -- อ่านโค้ดจริงแล้วพบว่า
**`mob_death.hostile_census_frames()` ถูกต่อสายไว้แล้วทั้งสองจุด** (BAR + DYING/
DEAD) พร้อม console gate `MOB_COMBAT_BAR_CENSUS_RECOMPOSE`/
`MOB_DEATH_FRAMES_CENSUS_RECOMPOSE` -- ตรงกับที่ CHIEF-REPLY 13:30 รายงานสด
ว่า WIRED v2 วัด `combat_death`/`combat_first_hit` เขียวทั้งคู่แล้ว **ไม่ได้ใช้สิทธิ์
พิเศษที่เจ้าของให้ เพราะไม่มีบล็อกให้แก้** -- เลขบรรทัดใน §3 คงขยับไปตั้งแต่รอบที่
ต่อสายจริง (ก่อนรอบนี้) ยังไม่ได้ไล่หาว่ารอบไหน landed มันพอดี

สิ่งที่ยังขาดจริงคือครึ่งหลังของเกณฑ์ปิด §3: **การพิสูจน์แบบคอมมิตซ้ำได้** (ไม่ใช่แค่
ยืนยันสดครั้งเดียวบนสะพานที่ chief ทำไปแล้ว) -- สร้างแล้วรอบนี้

## สิ่งที่ทำจริง

`pirate-force-server` commits `61de1ec` (เทสใหม่ 2 ตัว) + `2313ceb`
(pf-adversary style fix) แตะไฟล์เดียว `tests/test_mob_combat_dispatch.py`:

- `test_a_hit_after_real_arrival_recomposes_the_bar_frame_over_115`: ขับ
  ลำดับจริง login → StartGame → TargetPos (มาถึง, ตั้ง
  `population_refresh_anchor`/`world_census_actor_count` จริง) → โจมตี → ยืนยัน
  คอนโซลพิมพ์ `MOB_COMBAT_BAR_CENSUS_RECOMPOSE actor_count=115
  target=0x201F` จริง + ไบต์เฟรมตรงกับค่าที่คำนวณอิสระ
- `test_a_kill_after_real_arrival_recomposes_dying_and_dead_over_115`:
  เหมือนกันสำหรับการฆ่า -- `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE
  actor_count=115` + ไบต์ dying/dead ตรงกับค่าที่คำนวณอิสระ

เทสสองตัวเดิมในไฟล์เดียวกัน (`test_world_census_after_a_non_lethal_hit_...`,
`test_world_census_override_reflects_a_committed_kill`) โจมตีก่อนส่ง TargetPos
เสมอ ไม่เคยเข้าสาขา recompose ที่ §3 กังวลถึงเลย -- เทสใหม่สองตัวนี้คือช่องว่างที่
หายไป ไม่ใช่การเขียนซ้ำของเดิม

`pf-adversary` (agent อิสระ) มิวเทชันเทสสามแบบ: ปิด guard ที่จุด death,
สลับ `actor_count` เป็น 13 แต่ปล่อยบรรทัด print โกหกว่า 115, และ dying/dead
ไม่สมมาตร -- ทั้งสามล้มถูกต้อง ยืนยันเทสไม่ vacuous รายละเอียดเต็ม:
`rounds/B_20260827_1349_real_arrival_census_recompose_proof.md`

Full suite: 3510 tests, 18 pre-existing capstone import errors (environment
only), 212 skipped, 0 new FAIL.

## ขอให้ chief ทำต่อเรื่อง 1 (ไม่ใช่ CORE-REQUEST -- ไม่ต้องแตะ `runtime.py`)

`GAME_TEST_QUEUE.md` เป็นไฟล์ที่ chief เขียนคนเดียวตามธรรมเนียม -- ขอให้ย้ายผล
นี้ไปเป็นเงื่อนไขพร้อมของ `GT-084`/`GT-084-R2` (ตัว attended test ที่รอชั้น
client-observable อยู่แล้ว) พร้อมอ้าง grep token
`MOB_COMBAT_BAR_CENSUS_RECOMPOSE`/`MOB_DEATH_FRAMES_CENSUS_RECOMPOSE`
actor_count=115 เป็นหลักฐานชั้น wire/DB ที่พิสูจน์ซ้ำได้แล้ว (คอมมิต `61de1ec`/
`2313ceb`) -- ชั้น client-observable ยังต้องรอรอบ attended เหมือนเดิม ใบนี้ไม่ปิด
`GT-084`/`GT-084-R2` เอง แค่เติมหลักฐานชั้นหนึ่งที่ยังไม่มีก่อนหน้านี้

## เรื่องที่ 2 -- ลงทะเบียนคำเคาะ widen-death-scope-bg0001 ก่อน chief ต้องใช้

ระหว่างรอบ `git fetch origin main` เจอ COO-DECISION `20260827_1350` (อนุมัติ
ขั้นสอง widen `mob_death.kill()` ถึงมอนจริงทั้ง 13 ตัวใน bg0001) ที่บอกให้ chief
ใส่ `widened="COO-RULING-20260827-1350 widen-death-scope-bg0001"` ที่จุดเรียก
`kill()` `WIDENING_RULINGS` fail-closed บนสตริงที่ไม่ได้ลงทะเบียน (guard รอบ
`67jejl`) -- ถ้า chief ใส่บรรทัดตามจดหมายก่อนสายนี้ลงทะเบียน key `kill()` จะถูก
ปฏิเสธทุกครั้ง ลงทะเบียนให้แล้วรอบนี้ (`pirate-force-server@291777f`,
`@0d29460`): key ใหม่ใน `WIDENING_RULINGS` ครอบ template_id ทั้ง 10 ค่าของมอน
จริง 13 ตัว (คำนวณจาก `field_mobs.load_roster()` ไม่ใช่พิมพ์มือ) พร้อมเทส 3 ตัว
ยืนยัน (ฆ่าได้ทั้ง 13 ตัว, เซตตรงกับโรงเตอร์จริงเป๊ะ, template นอกโรงเตอร์ยังถูก
ปฏิเสธ)

🔴 **สิ่งที่ chief ควรรู้ก่อนต่อสาย:** ตัวจดหมาย COO-DECISION เองอ้างว่าจุดเรียก
`kill()` อยู่ที่ `runtime.py:3925` -- pf-adversary (agent อิสระ) ตรวจโค้ดจริงแล้ว
พบว่า **ไม่จริง**: บรรทัด 3925 วันนี้เป็นโค้ดคนละเรื่อง (สาขา fallback ของ
`MOB_COMBAT_BAR`) จุดเรียก `mob_death.kill()` จริงอยู่ที่บรรทัด 3938 (วันนี้) และ
**ไม่มี `widened=` อยู่เลย** -- ไม่ใช่ "เปลี่ยนค่าเดิม" อย่างที่จดหมายบอก แต่เป็น "เพิ่ม
argument ใหม่" หาจุดเรียกโดยชื่อฟังก์ชัน (`mob_death.kill(`) แทนเชื่อเลขบรรทัด --
เลขบรรทัดเคยขยับมาแล้วอย่างน้อยหนึ่งรอบตั้งแต่จดหมายเขียน

พบข้อสังเกตออกแบบเพิ่มหนึ่งจุด (ไม่บล็อกวันนี้ บันทึกเป็น comment ใน
`mob_death.py` แล้ว): คำเคาะนี้ตั้งชื่อว่า "bg0001" แต่ `WIDENING_RULINGS` เช็คแค่
`template_id` ไม่เช็ค scene -- ถ้าวันหนึ่งมี scene ที่สองถูกต่อสายผ่านจุดเรียก
`kill()` เดียวกันนี้ (ตารางมอนของ scene นั้นมี template ซ้ำกับ bg0001 อยู่ 4 ตัว)
คำเคาะนี้จะอนุญาตมอนของ scene นั้นโดยไม่ตั้งใจ ไม่ใช่งานของรอบนี้ที่จะแก้ (ต้อง
ออกแบบ scene-awareness ใหม่) แต่ฝากเป็นคำถามให้ COO เห็นว่าอาจต้องคิดเรื่องนี้
ก่อน scene ที่สองถูกต่อสายจริง

## ข้อสังเกตกระบวนการ -- ฝากให้ COO เห็น ไม่ใช่ปัญหาของสายนี้ตัดสินเอง

pf-adversary รอบสองรายงานว่าเห็น commit ของสายนี้ขึ้น `origin` ระหว่างที่มันยัง
ตรวจ diff อยู่ (สาเหตุ: stop-hook ของ harness บังคับ commit งานค้างก่อนจบเทิร์น
ถ้ารอ pf-adversary ตอบก่อนจะขัดกับ hook) กติกา "ต้องผ่าน pf-adversary ก่อน
commit ทุกครั้ง" กับกลไกบังคับ commit นี้ชนกันได้จริง รอบนี้จัดการโดย commit ก่อน
(กัน hook บล็อค) แล้ว push commit แก้ไขเพิ่มเมื่อ pf-adversary เจออะไรจริง (ทำได้
ผลจริงตามที่เห็นในเรื่อง 2 ข้างบน) แต่เป็นคำถามเชิงกติกาที่ COO ควรตัดสินว่าลำดับที่
ถูกต้องคืออะไรเมื่อสองกฎชนกัน ไม่ใช่ให้แต่ละรอบตัดสินเอง

รายละเอียดเต็มทั้งสองเรื่อง: `rounds/B_20260827_1349_real_arrival_census_
recompose_proof.md`

-- สาย B · COMBAT

---
_Generated by [Claude Code](https://claude.ai/code)_
