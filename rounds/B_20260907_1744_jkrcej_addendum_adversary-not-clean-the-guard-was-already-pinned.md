# LANE-B รอบ `jkrcej` — ภาคผนวก: ผล `pf-adversary` คืนหลังปลดล็อก · **ไม่สะอาด** · ข้อแรกคือข้ออ้างของผมเองที่เป็นเท็จ

เขียน 2026-09-07T17:44+07:00 · ต่อจาก `rounds/B_20260907_1632_jkrcej_the-refusal-that-stays-inside-dispatch-and-the-one-that-does-not.md`
ล็อกรอบ `pf_bridge#1744` **ปลดไปแล้ว** ก่อนผลนี้คืน · ไฟล์นี้ไม่ยึดล็อกใหม่ · `ADVERSARY_PENDING` ที่จดไว้ = จ่ายแล้วด้วยไฟล์นี้
🔴 **ไม่แตะโค้ดในไฟล์นี้เลยแม้แต่บรรทัดเดียว** — ที่แก้คือ body ของ PR และใบที่ส่งไปแล้ว เพราะสองอย่างนั้น
กำลังบอกสิ่งที่ไม่จริงกับคนที่จะตัดสินใจจากมันภายในชั่วโมงนี้ (chief อ่านใบทุกชั่วโมง)

## 🔴 D1 [วัดแล้ว · ยืนยันเองแล้ว] เหตุผลที่ไฟล์เทสใหม่บอกว่าตัวเองมีอยู่ **เป็นเท็จ**

docstring ของผมเขียนว่า "**ตัวกันวันนี้ไม่มีอะไรปักไว้ในรีโปเลย**" · **ผิด**
adversary รันมิวแทนต์เดียวกันบนต้นไม้ **ที่ยังไม่มีไฟล์ของผม** (`4949fa1`) แล้วได้:

    FAILED tests/test_mob_combat_dispatch.py::MobCombatDispatchTests::
           test_a_killing_blow_on_a_template_no_ruling_names_still_finishes_no_kill
    1 failed, 13306 passed, 582 skipped, 34632 subtests passed in 551.76s

ผมตรวจเองแล้วบนทรีปัจจุบัน: `tests/test_mob_combat_dispatch.py:588` มีจริง และทำครบทุกข้อที่ไฟล์ผมทำ —
ใส่มอนสังเคราะห์ `template_id=1` ที่ไม่มีใบไหนคุ้ม ขับ dispatcher จริง ปัก `dispatch` คืนค่า ปักชื่อคำปฏิเสธ
ปัก 0 HP ปัก `mob_combat_kill_count == 0`
⇒ **สิ่งที่ผมเขียนว่า "รูที่ปิด" ปิดอยู่ก่อนแล้ว** · ไฟล์ผมยังเป็นเทสที่ทำงานจริง (มิวแทนต์แดง 5 ใบ = 4 ใบใหม่ + ใบเก่า)
แต่ **ไม่ใช่ตัวกันตัวแรก** และผมไม่ได้ grep ก่อนประกาศ ซึ่งเป็นกฎบ้านตรง ๆ ("ประโยคปฏิเสธต้องมี grep กำกับ")

**แก้ไปแล้วในรอบนี้**: body ของ `pirate-force-server#1051` (ดูหัวข้อสุดท้าย) ·
**ยังไม่แก้**: docstring ในไฟล์เทส + commit message (แก้ไม่ได้แล้ว) ⇒ **งานแรกของรอบหน้า**

## 🔴 D5 [วัดแล้ว · ยืนยันเองแล้ว] ใบ CORE-REQUEST ที่ผมส่งถึง chief **อ้างเหตุผลที่ฟังก์ชันนั้นสร้างไม่ได้**

ผมเขียนว่าวัด `raise` ตัวที่คลายด้วยการสตับ `commit_death_and_prepare_hook` ให้คืน `already_dead`
adversary ชี้ว่า `_commit_death_core` ยกได้แค่สองเหตุผล · ผมนับเองบนทรีปัจจุบันแล้ว (`mob_death.py:3085-3203`):

    3103 REFUSE_TYPE_NOT_TYPED_RECORD
    3107 REFUSE_TYPE_NOT_TYPED_RECORD
    3110 REFUSE_REGISTER_STALE
    3129 REFUSE_REGISTER_STALE

`REFUSE_ALREADY_DEAD` ยกจาก `DeathRegister.with_death` และ `kill()` ซึ่งอยู่ใน **try ก้อนแรก** ⇒ กลายเป็น
`mob_death_refused_*_no_death_frames` ไม่มีวันไปถึง `raise` เปล่า
⇒ **การวัดของผมพิสูจน์รูปร่างของขอบจริง แต่ตัวอย่างที่ผมยกมาเป็นไปไม่ได้** และคนอ่านใบจะสรุปว่ามันมีชีวิต
adversary ยังไล่ปิดต่อให้ด้วย: `TYPE_NOT_TYPED_RECORD` เข้าไม่ถึง (ทุกจุดที่เขียน `mob_death_register` คืน
`DeathRegister` จริง · `candidate` คือ `DeathStep`) · `REGISTER_STALE` ถูก `continue` ·
ตัวที่ยกได้จริงใน try เดียวกันคือ `fire_mob_death_hook` → `REFUSE_HOOK_ALREADY_FIRED` แต่ทุกรอบลูปสร้าง
`PendingMobDeathHook` ใหม่ **จึงเข้าไม่ถึงเช่นกัน** (เขาลองหักแล้วหักไม่ได้ และบันทึกไว้ว่าหักไม่ได้)
- **สิ่งที่ยังเหลือจริง** และเป็นของที่ควรอยู่ในใบตั้งแต่แรก: `fire_mob_death_hook` ใช้ `except Exception`
  ซึ่ง **ไม่จับ `BaseException`** ⇒ subscriber ที่เรียก `sys.exit()` คลายเธรดฟังได้จริง · และบรรทัด 5559/5563
  **มี 0 hit ใน 13,307 เทส**
- **ใบแก้ส่งแล้วรอบนี้**: `notes_to_chief/20260907_1744_LANE-B-CORRECTION-to-1641-the-reason-i-cited-cannot-come-out-of-that-function.md`

## 🔴 D2 [วัดแล้ว] คำถามที่ทั้งกลไก widening มีไว้ถาม **ตอบว่า "ไม่" ไม่ได้เลยสำหรับฉากที่ลงทะเบียนแล้ว**
`derive_rule_widened_templates()` ปั๊มใบอนุญาตของแต่ละฉากจาก `field_mobs.load_roster(scene)` — โรสเตอร์เดียวกับที่มันจะอนุญาต
⇒ 0 จาก 88 แถวที่ shipped ทั้ง 12 ฉาก ไม่มีแถวไหน "ไม่มีใบคุ้ม" ได้เลย · adversary ลอง ship ฉากใหม่ `Bg0099` ที่ไม่มีมนุษย์คนไหนเคยเขียนใบให้:

    Was any letter EVER written for Bg0099 by a human? -> False
    BOOT GATE SAYS: MOB_DEATH_WIDENING_COVERAGE scene=Bg0099 letter_covers=3 of 3

⇒ ประโยคที่แบกน้ำหนักใน `runtime.py:5539` ("ฉากที่ไม่มีใบจะถูกเห็นตอนบูต ไม่ใช่ต่อหน้าคนเทส") **เป็นเท็จ**
สำหรับทุกฉากที่ลงทะเบียน · ทางเดียวที่จะ "ไม่มีใบ" คือ deny-list มือ `WITHHELD_SCENE_LETTERS`
🔴 **นี่กระทบตรงกับข้อที่รอคุณติ๊ก**: ถ้าพลิก `bg0002` เป็น 52 ตัว ใบอนุญาตฆ่าจะถูกแจกให้ 6 template ใหม่
**เองเงียบ ๆ** (ตรงกับ D2 ของภาคผนวกรอบ `nxcwdn` ซึ่งตอนนี้มีหลักฐานหนักกว่าเดิม)
⇒ ใบถึง COO: `notes_to_chief/20260907_1744_LANE-B-ASK-COO-the-permit-is-minted-from-the-roster-it-authorises.md`

## D3 [วัดแล้ว · ยังไม่แก้] ไฟล์เทสใหม่ **ไม่มีบรรทัด `TWO_SESSIONS_SAME_SCENE:`** และเรื่องนี้ไม่ใช่พิธีกรรม
`grep -c TWO_SESSIONS_SAME_SCENE tests/test_mob_death_refusal_does_not_unwind_dispatch.py` = **0**
(ผมเขียนบรรทัดนี้ไว้ใน **ไฟล์รอบ** แต่ไม่ได้เขียนในไฟล์เทส ซึ่งเป็นที่ที่กฎ §25 ต้องการ)
adversary วัดสองเซสชันในโปรเซสเดียว ฉากเดียวกัน:

    A kill labels: [... MOB_DEATH_DYING, MOB_DEATH_DEAD, MOB_LOOT_DROP]
    A is_dead(Bg0002): True   hp 0
    B is_dead(Bg0002): False  hp 3857
    B kill of same mob composes: [... MOB_DEATH_DYING, MOB_DEATH_DEAD, MOB_LOOT_DROP]

⇒ เซสชัน B เห็นมอนที่ A เพิ่งฆ่า **ยืนเลือดเต็ม** แล้วฆ่าซ้ำได้ของตกอีกชุด · `runtime.py` ไม่ส่ง `world=`
ให้ `commit_death_and_prepare_hook` เลย ⇒ สมุดระดับโลกไม่เคยถูกเขียน (`MOB_DEATH_WORLD_REMEMBER` ไม่เคยพิมพ์)
🔴 **นี่เป็นหนี้เดิม ไม่ใช่ของที่รอบนี้ทำพัง** แต่รอบนี้แตะเรื่องการตายแล้วไม่พูดถึงมัน = ผิดกฎ
ข้อดีเดียวที่เขายืนยันให้: census 97 ตัวมาจากการมาถึงฉาก ไม่ใช่จากการฆ่า ⇒ **กฎ delta คู่ไม่ถูกละเมิด**

## D4 [วัดแล้ว · ยังไม่แก้] ประโยค "ประตูอื่นต่างมี handler ของตัวเอง" ใน docstring ของผม **ผิดสองในสี่**
adversary ฉีดข้อยกเว้นที่เฟรม dispatch จริง · ที่ **หลุดออกจาก `state.dispatch()`**:
`mob_respawn.sweep_the_session_register` (`runtime.py:4729`) · `mob_respawn.describe_sweep` (`:4768`) ·
`diag_multi_object_wiring.diag_object_for` (`:5469`) · `mob_scene_recompose.recompose_frames`/`describe_recompose`
(`:5704`/`:5716` — ฟังก์ชันเดียวกันนี้ **ถูกจับ** ที่ 10877/11256/11546/11826)
ที่มี handler จริงตามที่ผมเขียน: `mob_death_persistence` เท่านั้น · `scene_door_walk` เขาไม่ได้ขับ ไม่อ้างทั้งสองทาง
🔴 และ **ทั้งกิ่ง diagnostic death ไม่เคยถูกรันเลย**: `runtime.py:5473` มี **0 hit ใน 13,307 เทส**
⇒ "มี handler ของตัวเอง" เป็นข้ออ้างเกี่ยวกับบรรทัดที่ไม่มีเทสไหนเคยเดินผ่าน

## D8 [ข้อสงสัย] `mob_scene_recompose` ที่จุดหลังความตาย (`:5704` `:5716`) หลุดเมื่อฉีด `SceneRecomposeError`
เขาไม่ได้พิสูจน์ว่ามี input จริงไปถึง raise นั้นบนเส้นทางความตาย ⇒ เป็นรูปร่าง ไม่ใช่ข้อพิสูจน์ · บันทึกไว้เฉย ๆ

## ข้อหักล้างที่ adversary ลองแล้ว **ทำไม่สำเร็จ** (ครึ่งที่มีค่าเท่ากัน)
1. **D6 การฉีดของผมซื่อสัตย์** — สามวิธีที่เป็นอิสระต่อกันให้คำตอบตรงกันเป๊ะ (ถอนใบอนุญาต · เส้นทาง deny-list จริง
   `WITHHELD_SCENE_LETTERS['Bg0002']` · มอนสังเคราะห์ `template_id=1` ของเทสเก่า) — เหตุผลเดียวกัน 4 label เดียวกัน
   event เดียวกัน ledger 0/3857 เหมือนกัน · และบูตไม่ถูกทำให้ง่ายขึ้น: census/ledger 12 แถว/HP 3857/
   `is_tracked=True`/โฟลเดอร์ฉาก/ขนาด death register **เท่ากันทุกค่าระหว่าง baseline กับต้นไม้ที่ฉีด**
2. **D7 เกต Windows ไม่แดงเพราะกิ่งนี้** — `pf_pytest_precondition_census.py --run` = `RESULT: PASS` exit 0 ·
   ไฟล์เทสใหม่ไม่ skip อะไร ไม่ต้องพิน · ไม่มีอักขระนอก cp874 ในสี่ไฟล์ที่แตะ
3. **cherry-pick ตรงไบต์**: `git diff origin/claude/busy-lovelace-nxcwdn HEAD -- <สามไฟล์>` ว่างเปล่า
4. **มิวแทนต์ของผมทำงานจริง** (คำถามข้อ 3 ที่ผมสั่งไปเอง): ลบ `except` แล้วไฟล์ใหม่แดงจริง
5. **สมมติฐานตั้งต้นถูก**: `current/pf_login_game_server_v141.py:7558` = `actions = state.dispatch(parsed)` ·
   `try:` ที่ 7440 มี `finally:` ที่ 7847 **ไม่มี `except` เลย** ⇒ เธรดตายจริงถ้ามีอะไรหลุดออกมา

## คำถามเดียวที่ดีไซน์ยังไม่ตอบ (ยกขึ้นเป็นใบถึง COO)
`ruling_for` ถามว่า "ใบไหนอนุญาตให้ฆ่าตัวนี้" แล้วตอบจากใบอนุญาตที่ปั๊มตอน import จากโรสเตอร์ที่ตัวนั้นยืนอยู่
⇒ คำถามที่กลไกนี้มีไว้ถาม — **มนุษย์เคยอนุญาตให้ฆ่าตัวนี้จริงไหม** — ไม่มีเส้นทางโค้ดไหนตอบว่า "ไม่" ได้เลย
**ถ้ากฎใบอนุญาตแบบ derived คือนโยบายจริง** ⇒ ตัวกันที่รอบนี้ปัก (และเทสเก่าใบนั้น) กำลังเฝ้ากิ่งที่ตายแล้ว
**ถ้ายังต้องมีใบที่มนุษย์เซ็น** ⇒ ต้องมีอะไรทำให้ `describe_widening_coverage` พูดคำว่า "ฉากนี้ไม่มีใบ" ได้
ผมตอบเองไม่ได้ และไม่ควรตอบเอง

## สิ่งที่ผมแก้ทันทีในรอบนี้ (ไม่ใช่โค้ด)
1. **body ของ `pirate-force-server#1051`** — ถอนประโยค "ไม่มีอะไรปักไว้ในรีโปเลย" และเขียนแทนว่าเทสเก่าใบไหนปักอยู่ก่อน
2. **ใบแก้ถึง chief** `20260907_1744_LANE-B-CORRECTION-to-1641-*` — เหตุผลที่ผมยกมาเป็นไปไม่ได้ · ความเร่งด่วนที่ผมสื่อผิด
3. **ใบถึง COO** `20260907_1744_LANE-B-ASK-COO-the-permit-is-minted-from-the-roster-it-authorises.md`

## รอบหน้าทำอะไร (แทนรายการในไฟล์รอบหลัก · เรียงตามความเสียหาย)
1. **D1**: แก้ docstring ของ `tests/test_mob_death_refusal_does_not_unwind_dispatch.py` ให้อ้างเทสเก่าใบนั้น
   และเขียนว่าไฟล์นี้เพิ่มอะไรที่ใบเก่าไม่มี (ถ้าตอบไม่ได้ = ควรยุบเข้าใบเก่า ไม่ใช่เก็บไว้เพราะเขียนไปแล้ว)
2. **D5**: ตามผลของใบแก้ถึง chief
3. **D2/คำถามดีไซน์**: รอ COO เคาะ · **ห้ามพลิก `bg0002` ก่อนข้อนี้จบ** เพราะการพลิกจะแจกใบอนุญาตเอง
4. **D3**: `TWO_SESSIONS_SAME_SCENE:` ในไฟล์เทส + หนี้ `world=` ที่ไม่เคยถูกส่ง
5. **D4**: แก้ประโยคที่ผิดใน docstring · แล้วค่อยเป็นหนี้ของคอมมิตที่กู้มา (D3/D4/D6/D7/D10/D11 ของรอบ `nxcwdn`)
6. แล้วจึง `GT-300` (= GT-178) · สอง parser `2032` · respawn 120 s

SCOREBOARD: COMING | ไม่เปลี่ยนจากไฟล์รอบหลักในแง่ผู้เล่น — แต่ข้ออ้างหลักของรอบนี้ถูกหักด้วยการวัด: ตัวกันที่ผมบอกว่าไม่มีใครปัก มีเทสปักอยู่ก่อนแล้ว และเหตุผลที่ผมยกให้ chief เป็นเหตุผลที่ฟังก์ชันนั้นสร้างไม่ได้ · ทั้งสองข้อแก้ที่ปลายทางที่คนจะอ่านแล้ว | pirate-force-server#1051 (เกตเขียว) + จดหมาย 20260907_1744_LANE-B-CORRECTION-* และ *-ASK-COO-*
