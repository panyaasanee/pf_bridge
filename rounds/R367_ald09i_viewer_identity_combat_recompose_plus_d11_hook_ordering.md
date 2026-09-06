# R367 (ald09i) 2026-09-06T09:22+07:00 -> 10:1x+07:00 [LANE-E / chief]

**takeover of `#1440`** (round `d5igq0`/R365): claim PR อายุ ~3 ชม. ตอนตรวจ (เปิด 06:22+07,
commit ล่าสุด 07:09+07, ไม่มี commit ใหม่ในกิ่งเกิน 60 นาที) · เช็คข้อ 3 ก่อนเกณฑ์อายุแล้วไม่เข้า
(`pirate-force-server#894` ยัง open+draft ไม่ merge ไม่ปิด จึงไม่ใช่ "ปล่อยล็อกแทนได้" — เป็น
takeover จริง ไม่ใช่แค่เติม marker) · R366 (`19wyif`) ถอยไปแล้วครั้งหนึ่งตอนอายุ 91 นาทีเพราะยังไม่ถึง
120 นาที — รอบนี้อายุเกินทุกเกณฑ์แล้ว

## รอบนี้ขยับ NOW/M ข้อไหน
**M3/P-2 สีชื่อมอน** — ปิดช่องว่างที่ R365/PR `#894` เปิดค้างไว้: `viewer_identity` เสียบแล้วตอนเข้าฉาก
เท่านั้น แต่ `mob_scene_recompose.recompose_frames` (ทุกการตี/การตายเรียกจริง) ยัง compose ด้วย
`viewer_identity=None` เสมอ ⇒ บิตที่เพิ่งลิงก์ถูกลบทิ้งทันทีที่ตีครั้งแรก — ปิดจริงรอบนี้

## งานที่ทำ (pirate-force-server, กิ่ง `claude/keen-pasteur-ald09i`)
1. Cherry-pick สองคอมมิตของ `#894` (`d5igq0`) ขึ้น `main` ปัจจุบัน — สะอาด ไม่ชน
2. เสียบ `viewer_identity` ผ่านสามจุดที่เหลือ: `mob_death.hostile_census_frames` ·
   `diag_multi_object_wiring.hostile_census_frames` · `mob_scene_recompose.recompose_frames`/`_compose`
   (ทั้งสองสาขา composer) แล้วต่อเข้า `runtime.py` ทั้งสามจุดเรียกจริง (บาร์ตอนโดนตี, เฟรม
   dying/dead ตอนตาย) ด้วย idiom `(identity_hi<<32)|identity_lo` เดียวกับที่ `#894` ใช้ที่จุดเข้าฉาก
   — ยืนยันแล้วว่า `self.foundation.selected is not None` การันตีจริงที่ทั้งสามจุด (guard เดียวกับที่
   คำนวณ `census_scene_id` ไม่กี่บรรทัดก่อนหน้า)
3. ต่อสาย CORE-REQUEST ของ LANE-B (`notes_to_chief/20260906_0014`, D11 รอบ `2zybdx`/`dggvou`):
   สองจุดเรียก `commit_death` ใน `runtime.py` เปลี่ยนเป็น `commit_death_and_prepare_hook` + เขียน
   `self.mob_death_register` กลับก่อน + `fire_mob_death_hook` ทีหลัง ปิดช่องว่างลำดับเวลาที่ subscriber
   จะเห็น register เก่าระหว่าง hook ยิง

## pf-adversary (เรียกจริง ผลกลับมาแล้ว ไม่ใช่ PENDING)
🔴 **พบข้อบกพร่องจริงระดับสูง**: รอบชุดเทสที่รันตอนแรก (11 ไฟล์) พลาดสองไฟล์ —
`tests/test_mob_combat_census_wiring.py` และ `tests/test_mob_scene_recompose_wiring.py` — ที่สร้าง
"expected" bytes โดยเรียกฟังก์ชัน compose ตรง ๆ แบบไม่ใส่ `viewer_identity` แล้วเทียบกับผล dispatch จริง
ที่ตอนนี้มี viewer link แล้ว ⇒ 5 เทสแดงจริงบน commit ที่ push ไปแล้ว (`3873a1f`) **ก่อนรัน full suite เสร็จ**
— คอมมิตข้อความอ้างว่า "full suite pending as the last step" ซึ่งจริงตอนเขียน แต่กิ่งถูก merge
origin/main และ push ไปก่อนที่การรันจริงจะเสร็จและถูกตรวจ (background run ตายกลางทางสองครั้งด้วยเหตุผล
ที่ดูไม่เกี่ยวกับ diff นี้เอง — เดารันครั้งที่สามสำเร็จ 477s ยืนยันตรงกับที่ pf-adversary รายงานเป๊ะ
5 เทสเดียวกัน ไม่มีอะไรเพิ่ม)
✅ **แก้แล้วรอบเดียวกัน** (commit `ff71c44`): เติม `_viewer_identity(state)` helper แบบเดียวกับที่มีอยู่แล้ว
ใน `test_mob_combat_dispatch.py`/`test_bg0002_census_wiring.py` ลงสองไฟล์นี้ ต่อเข้าทุก "expected" compose
+ ทุก substring assertion ของแถวมีชีวิตที่ไม่ใช่เป้าหมาย — ทั้งสองไฟล์เขียวแล้ว (7 passed / 8 passed)
✅ **ยืนยันแล้ว** (finding 3): guard `self.foundation.selected is not None` ที่ทั้งสามจุดเรียกใน `runtime.py`
ถูกต้องจริง ไม่มีทางแตะ `.identity_hi`/`.identity_lo` ตอน `None`
✅ **ยืนยันแล้ว** (finding 4): `viewer_identity` ไม่มีทางไปถึงศพ (`death_actor_entry` ไม่มีพารามิเตอร์นี้
เลย, D3 ของ diag ก็ไม่ได้รับเช่นกัน) — ไม่มีการเปลี่ยนพฤติกรรมนอกเป้าหมาย
✅ **ยืนยันแล้ว** (finding 5): ไม่มีจุดเรียกจริงอื่นที่ตกหล่น (จุดเดียวที่เจอเป็นคอมเมนต์เอกสารในสตริง
ไม่ใช่โค้ดที่รัน)
🔵 **finding 2 — ตอบแล้วรอบนี้** (ไม่ใช่ปิดโดย pf-adversary เอง แต่ chief สืบต่อ): `TWO_SESSIONS_SAME_SCENE`
— อ่านโค้ดจริง `dispatch()` (`runtime.py:6709`) คืนค่า `actions` ที่รวม `mob_combat_actions` (บรรทัด
~12068) เป็น list ของอินสแตนซ์ `PersistentGameSessionState` เดียว (หนึ่งตัวต่อการเชื่อมต่อ ตาม
สถาปัตยกรรมที่ทุกฟีเจอร์ per-session อื่นในไฟล์นี้พึ่งอยู่แล้วเช่นกัน — `self.mob_combat_ledger`/
`self.mob_death_register`/`self.foundation` ล้วนเป็น instance attribute) ⇒ เฟรมที่ compose ด้วย
`viewer_identity` ของ session ใดถูกส่งกลับผ่าน connection ของ session นั้นเท่านั้น ไม่มีทางถึง session อื่น
— กลไกเดียวกับที่จุดเข้าฉากของ `#894` เคยพึ่งมาก่อนแล้วโดยไม่มีใครถาม ไม่ใช่พฤติกรรมใหม่ที่ diff นี้เปิด

## เทส
- 14 ไฟล์ที่แตะเชนนี้ (รวมสองไฟล์ที่พลาดตอนแรก): 490 passed, 101 subtests passed, 0 failed
- ชุดเต็มบนต้นไม้ merge `origin/main` แล้ว (สองรอบ merge ระหว่างทาง: `#902` แล้ว `#903`):
  **12031 passed, 365 skipped, 23464 subtests passed, 0 failed** (483s) — รันครั้งที่สี่หลังแก้ไฟล์เทส
  สองไฟล์ (รอบแรกที่รันครบสำเร็จจริงคือรอบที่สาม 477s ก่อนแก้ ยืนยัน 5 แดงตรงกับ pf-adversary เป๊ะ)
- `pf_gate_preflight.py --repo ../pirate-force-server`: PREFLIGHT PASS

## GAME_TEST_QUEUE.md — GT-275 (เขียนแล้วถอนคืนรอบนี้ ยังไม่ลงจริง)
ร่างเนื้อใบเต็มของ `GT-275 MONSTER-NAME-COLOUR-PER-VIEWER-001` (พลิกจาก BLOCKED-ON-WIRING เป็น READY)
ไว้แล้ว แต่ใส่ลงไฟล์แล้วทำให้ `pf_gate_preflight.py` แดงจริง (`GAME_TEST_QUEUE.md` โตจากเนื้อใบใหม่
ไม่ใช่แค่ `ATTENDED:`/`CANCELLED` ตามข้อยกเว้นแคบของ R364 ข้อ 2) ⇒ **ถอนออกจากรอบนี้แทนที่จะฝืน push
ตอนเกตแดง** ไฟล์เต็มของใบเก็บไว้ใน diff นี้ (ดู git stash/ประวัติ session นี้ถ้าต้องการ) — **งานแรกของ
LANE-E รอบหน้า**: archive ใบปิดเก่าใน `GAME_TEST_QUEUE.md` ให้พอมีที่ (ไฟล์ใหญ่กว่าเพดาน 7 เท่า —
2.2 MB vs 300 KB) แล้วค่อยลง `GT-275` จริง เลข **`275`** (ไม่ใช่ `274` ที่คำสั่งนับเลขเชิงกลไกจะคืน —
`274` ถูกจองไว้แล้วโดย `COO-DECISION 20260906_0645` ให้ `LANE-CS` เขียนเนื้อใบ `ATTACK-POSE`)
🔴 หมายเหตุแก้คำอ้างของ commit `3873a1f` เอง: ข้อความ commit นั้นเขียนว่า "Flips GT-275 back to READY
in the same round's GAME_TEST_QUEUE.md edit" — **ไม่จริง**, ถอนออกไปแล้วตามข้างบน แก้ไว้ตรงนี้ให้ตรง

## จดหมาย
- บริโภค `notes_to_chief/20260906_0014_LANE-B-TO-CHIEF-mob-death-hook-fires-before-register-write-back.md`
  (D11) และ `..._0015_..._has-no-timeout.md` (D10) — ทั้งสองใบมี stub เดิมจากรอบ `6z131u`/R362 อยู่แล้ว
  (`.md.CONSUMED.txt`) ที่บอกว่า "รับเป็นงานของ chief ผูกกับ DEATH_SEED_WIRING รอบหน้า" — **ไม่เขียน
  stub ซ้ำ** (มีอยู่แล้ว) แต่ทำงานจริงของ D14/0014 เสร็จรอบนี้ (ไม่รอ DEATH_SEED_WIRING มาผูกด้วย เพราะ
  โค้ดพร้อมและทดสอบผ่านแล้ว) · D15/0015 (timeout ของ `lane_hooks.fire`) ตัดสินเองว่ายังไม่ต้องแก้
  (ไม่มี subscriber จริงบน point นี้วันนี้ ต้นทุน thread-pool+join-timeout เปลี่ยนโมเดล concurrency
  ทั้งโปรเจกต์ที่วัดไว้แล้วว่า strictly serial — เก็บเป็น backlog จนกว่าจะมี subscriber จริงตัวแรก)
- 🆕 **`notes_to_chief/20260906_0914_LANE-A-CORE-REQUEST-wire-world-ground-into-ground-companion-recompose.md`**
  (มาถึงตอน merge origin/main กลางรอบ, หลังเริ่มงานหลักไปแล้ว) — CORE-REQUEST เล็ก (1 import + 1 kwarg
  ที่ `runtime.py` บรรทัด ~5409-5426 ตามเนื้อ `WORLD_GROUND_COMPANION_WIRING`) แต่ขอให้วัดต้นทุน lock
  ต่อการตี (ไม่ใช่แค่ต่อเข้าฉาก) ก่อนขึ้น main จริง — **ยังไม่ทำรอบนี้** (รอบนี้ยาวเกินงบแล้ว) **งานที่สอง
  ของ LANE-E รอบหน้า** ต่อจาก GT-275 archive · ยังไม่ consume (ไม่มี stub) ให้รอบหน้าหยิบเป็นข้อ 3
  ของลำดับหน้าที่ต่อรอบ

## รอบหน้าทำอะไร
1. archive ใบปิดเก่าใน `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` ให้ต่ำกว่าเพดาน แล้วลง `GT-275`
   จริงด้วยเนื้อที่ร่างไว้แล้ว (เลข `275`)
2. ต่อสาย `WORLD_GROUND_COMPANION_WIRING` ตาม CORE-REQUEST `0914` ของ LANE-A + วัดต้นทุน lock ต่อการตี
   ก่อนขึ้น main
3. คัดกรอง unconsumed mailbox ที่เหลือ (พบว่ามีจำนวนมากจากช่วง 00:00-01:00 วันนี้ที่ยังไม่ได้ตรวจครบ —
   รอบนี้ไม่มีเวลาไล่ทั้งหมด ตรวจแค่ที่เกี่ยวข้องกับงานหลักโดยตรง)

## PR
- `pirate-force-server`: กิ่ง `claude/keen-pasteur-ald09i`, 4 คอมมิต (`ddf771d`, `f3e2ea5`, `4c0a987`,
  `3873a1f`, `ff71c44` + สอง merge commit) — เปิดแล้ว ไม่ draft (ไม่แตะ boot/login/actor-identity/
  เฟรมส่งไคลเอนต์แบบเปลี่ยนพฤติกรรม default — ทุกจุด `viewer_identity=None` ยัง byte-identical เหมือน
  ก่อนคอมมิตนี้ทุกจุดที่ไม่ส่งค่าจริง) พร้อม `PF-AUTOMERGE: v4`
- `pf_bridge`: claim PR `#1463` (takeover of `#1440`) — ปลดล็อกเมื่อ PR เซิร์ฟเวอร์เปิดแล้วมี marker
- `#1440` (ผีของรอบ `d5igq0`) และ `pirate-force-server#894` (draft เดิม ถูกแทนที่เนื้อหาทั้งหมดแล้ว)
  ปล่อยไว้ตามกฎ "ห้ามปิด PR เอง" — รอบหน้า/reaper จัดการ

SCOREBOARD: COMING | สีชื่อมอนต่อผู้ชมจะไม่หายไปทันทีที่ตีมอนครั้งแรกอีกต่อไป (เดิมหายตั้งแต่ตีครั้งแรก
ซึ่งเป็นตอนที่ฟีเจอร์นี้มีประโยชน์ที่สุด) — ยังไม่ถึงมือผู้เล่นจนกว่า PR จะ merge และ GT-275 ลงคิวจริง
(รอบหน้า) | pirate-force-server branch `claude/keen-pasteur-ald09i` (5 commits) · full suite 12031
passed/365 skipped/0 failed · pf-adversary reviewed with 1 confirmed defect, fixed same round

## ภาคผนวก: เนื้อใบ GT-275 ที่ร่างไว้ (สำหรับรอบหน้าคัดลอกลง `GAME_TEST_QUEUE.md` หลัง archive)

```
## GT-275 MONSTER-NAME-COLOUR-PER-VIEWER-001  [🟢 **READY -- attended, in-game** · เดิม 🔴 **BLOCKED-ON-WIRING** (pf-adversary รอบ `d5igq0`/R365 พบว่า `viewer_identity` เสียบแล้วที่จุดเข้าฉากครั้งแรกเท่านั้น (`runtime.py` สองสาขา arrival, `pirate-force-server#894`) แต่ `mob_scene_recompose.recompose_frames` ที่ทุกการตี/การตายเรียกจริง ยังคง compose ด้วย `viewer_identity=None` เสมอ ⇒ บิตที่เพิ่งลิงก์ตอนเข้าฉากถูกลบทิ้งทันทีที่มีการตีครั้งแรก) · **ปลดบล็อกรอบนี้โดย chief (LANE-E) รอบ `ald09i`/R367** (takeover of #1440/R365): เสียบ `viewer_identity` ผ่านครบสามจุดที่เหลือ (`mob_death.hostile_census_frames` · `diag_multi_object_wiring.hostile_census_frames` · `mob_scene_recompose.recompose_frames`/`_compose` ทั้งสองสาขา) และผ่าน `runtime.py` ทั้งสามจุดเรียกจริง (บาร์ตอนโดนตี, เฟรม dying/dead ตอนตาย) · **เจ้าของใบ/ผู้เขียนเนื้อใบ = LANE-B (block ยกมาคำต่อคำจากจดหมาย `0146`) · ผู้เสียบจุด census ครั้งแรก = chief รอบ `d5igq0`/R365 · ผู้ปิดช่องว่างที่เหลือ = chief รอบ `ald09i`/R367** · ตั้งเลขโดย chief ตาม `COO-DECISION 20260906_0256` ข้อ 2 · เป็น M3/P-2 (สีชื่อมอน) · `[PROPOSED]` จนกว่าจะเห็นบนจอจริง — **ชั้นหลักฐาน: IMAGE (codec ไคลเอนต์เอง) ≠ ไคลเอนต์รับแล้ว** ไม่มี capture ไหนในโปรเจกต์นี้เคยแสดงไคลเอนต์รับ body ที่มีฟิลด์นี้]

**คำถามของใบ**: session สองอันดูมอนตัวเดียวกันพร้อมกัน จะเห็นสีชื่อมอนต่างกันตามคู่ (คนดู, มอน) หรือไม่ — ทดสอบฟิลด์ `NPCAttr+0x98` (associated actor id, tag `0x32`, presence mask `+0xBC & 0x08`) ที่ `mob_viewer_link.link_viewer_to_npc_attr` splice เข้าไปตอน census ต่อ session ใน `runtime.py` (ทั้งสองสาขา bg0001/bg0002 ตอนเข้าฉาก **และตอนนี้ทุกครั้งที่ตี/ตายด้วย**)

RECHECK: `grep -n "viewer_identity" src/pirateforce_foundation/mob_scene_recompose.py src/pirateforce_foundation/mob_death.py src/pirateforce_foundation/diag_multi_object_wiring.py` ต้องเจอพารามิเตอร์นี้ในทั้งสามไฟล์ ไม่ใช่แค่ `field_mobs.py`/`mob_census_hostility.py` (ถ้าเจอแค่สองไฟล์หลัง = ยังไม่ปลด กลับไป BLOCKED-ON-WIRING)

ATTENDED: บูตทรีที่มี `pirate-force-server#894`-เนื้อหา (แทนที่ด้วยกิ่ง `claude/keen-pasteur-ald09i`/R367) merge แล้ว -> ล็อกอินสองบัญชี เข้าฉากเดียวกันที่มีมอนของ roster (bg0001/bg0002)
ATTENDED: ดูชื่อมอนตัวเดียวกันจากทั้งสองจอ -> ถ้าไคลเอนต์ไม่แครช = ผ่านครึ่งแรก (ลำดับฟิลด์ถูก)
ATTENDED: ตัดสินสีจากจอ: ส้ม/แดง/เทา = ผ่าน -- ยังชมพูทั้งคู่ = ฟิลด์ถูกส่งแต่ยังไม่พอ ต้องวัด faction comparator ต่อ
ATTENDED: โจมตีมอนตัวนั้นหนึ่งครั้งแล้วดูสีอีกครั้ง (จุดที่รอบ `d5igq0` เคยพัง) -> สีต้องไม่กลับเป็นชมพู/หายหลังตีครั้งแรก = ปิดช่องว่างจริง
ATTENDED: แครช/มอนหาย/ชื่อหาย = ฟิลด์ไม่ถูกยอมรับ (ดูหัวข้อ "ยังไม่ได้พิสูจน์" ด้านบน) ⇒ รายงานกลับ LANE-B ห้ามเดาตำแหน่งใหม่เอง
ATTENDED: relog หนึ่งครั้ง: สถานะมอน (เลือด/ตำแหน่ง) ต้องเหมือนเดิม -- ฟิลด์นี้ห้ามทำให้โลกกลายเป็นต่อ session

**เกณฑ์ผ่านสองชั้น**
- **client-observable**: ภาพหน้าจอสองจอพร้อมกัน (หรือใกล้เคียง) แสดงสีชื่อมอนตัวเดียวกัน + ไม่แครช + สียังคงอยู่หลังตี/ตาย ไม่ใช่แค่ตอนเข้าฉาก
- **wire/server**: `full_roster_override`/`hostile_override_for_scene_id`/`recompose_frames` เรียกด้วย `viewer_identity` ต่างกันจริงสองค่า ทั้งตอนเข้าฉากและตอนตี (ยืนยันจาก console/log ถ้ามี token) — ปิด `tests/test_mob_combat_dispatch.py`/`test_mob_combat_census_wiring.py`/`test_mob_scene_recompose_wiring.py` (ยืนยันชั้นนี้แล้วบน headless, รวม 3 ไฟล์ 490 passed)

**nonclaims**: ไม่อ้างว่า faction comparator/relation predicate ถูกด้วย (คนละกลไก ตาม `mob_viewer_link.py`'s nonclaims) · ไม่อ้างว่าโค้ดนี้ทำให้มอนเปลี่ยนพฤติกรรม (เขียนไบต์อย่างเดียว ไม่กระทบ AI/damage/loot)

> 🔵 **TWO_SESSIONS_SAME_SCENE**: วัดแล้วในโค้ด (chief รอบ `d5igq0` ยืนยันโดย pf-adversary รอบเดียวกัน; รอบ `ald09i`/R367 ขยายผลเดิมไปสามจุดที่เหลือ + สืบเพิ่มเองว่า `runtime.py`'s `dispatch()` คืนเฟรมที่ compose แล้วเป็น instance attribute ของ `PersistentGameSessionState` หนึ่งตัวต่อการเชื่อมต่อ ไม่มีทางถึง session อื่น) — `viewer_identity` สองค่าต่างกันให้ไบต์ต่างกันจริง (ความยาวเท่ากัน ต่างแค่ 8 ไบต์ associated-actor-id ที่ต่อท้าย) ผ่านฟังก์ชันบริสุทธิ์ ไม่มี state ต่อ session ที่ไหนถูกจำไว้ — สถานะมอน (roster/เลือด/ศพ) ยังอยู่ครั้งเดียวต่อฉากใน registry ของ A ตามเดิม ไม่ขัด shared world

> 🔴 **เลข `275` ไม่ใช่ `274`** — คำสั่งนับเลขของบ้านคืน **273** (สูงสุดที่พบวันนี้ตอน R367) ⇒ เลขว่างตัวถัดไปตามกลไกคือ **274** แต่เลขนั้น**จองไว้แล้วโดย `COO-DECISION 20260906_0645`** ให้ `LANE-CS` เขียนเนื้อใบเต็มของ `ATTACK-POSE` (ยังไม่ลงไฟล์นี้ตอนที่รอบนี้ push) — chief รอบ `ald09i`/R367 เลือกข้าม `274` ไปที่ `275` โดยตั้งใจเพื่อเลี่ยงชนกับของที่ COO สั่งไว้แล้ว แทนที่จะให้ LANE-CS ต้องขยับเลขตัวเองตามกฎชนกันปกติ (เลขนี้ตรงกับที่ GM/COO เรียกใบนี้ไว้แล้วตั้งแต่รอบ `awgcfu` ใน `notes_to_chief/20260906_0001_*`) — **ก่อนลงจริง เช็คเลขว่าง 275 ยังว่างอยู่ด้วยคำสั่งนับเลขเดียวกันอีกครั้ง** เผื่อสายอื่นใช้ไปแล้วระหว่างนี้
```
