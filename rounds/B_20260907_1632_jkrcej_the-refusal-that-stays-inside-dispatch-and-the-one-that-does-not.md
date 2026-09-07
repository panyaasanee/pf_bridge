# LANE-B รอบ `jkrcej` — คำปฏิเสธที่อยู่ในบ้าน กับคำปฏิเสธที่เดินออกจากบ้าน · วัดทั้งสองตัวแล้ว

รหัสรอบ: `jkrcej` · เริ่ม 2026-09-07T16:32+07:00 · claim `pf_bridge#1744` (ไม่ใช่ takeover)
กิ่ง: `claude/sharp-bardeen-jkrcej` (สะพาน) · `claude/magical-albattani-jkrcej` (เซิร์ฟเวอร์)

## รอบนี้ขยับ NOW/M ข้อไหน
- **NOW "งานด่วนตอนนี้ · M4 · LANE-B (`1541`) งานแรก"** — ขยับ**จนจบ**: "วัดว่า `MobDeathContractError`
  นอกคำสั่งคลายสแต็กออกจากเธรดฟังไหม" · คำตอบวัดได้แล้ว **ทั้งสองครึ่ง** และครึ่งที่แย่กว่าไม่ใช่ครึ่งที่ถูกถาม
- **NOW "รอ Panya ติ๊ก · death scope `bg0002`"** — **ไม่ขยับโดยตั้งใจ** (ห้ามพลิกจนกว่าติ๊ก) แต่รอบนี้
  ถอดความเสี่ยงข้อหนึ่งที่แขวนอยู่กับการติ๊กนั้นออก: ถ้าติ๊กมาแล้วมีมอนที่ไม่มีใบคุ้ม ผู้เล่นจะเห็น
  "ตีไม่ตาย" ไม่ใช่ "โลกว่าง" — และตอนนี้มีเทสปักไว้แล้ว ไม่ใช่ความเชื่อ
- **M4 "ตีได้ตายได้"** — ยังไม่มีอะไรใหม่บนจอ พูดตรง ๆ · รอบนี้ปักพื้นที่ที่ M4 จะยืน

## กล่องจดหมายที่บริโภครอบนี้
1. `20260907_1541_COO-DECISION-b1520-hold-the-flip-measure-the-raise-LANE-B.md` — **คำสั่งหลักของรอบ** ทำครบข้อ 5
2. `20260907_1616_SYNC-NOTICE-pirate-force-server-pr1043-closed-never-merged.md` — **ใช้จริง** (ดูหัวข้อกู้งาน)
3. `20260907_1441_COO-DECISION-panya1349-gt178-owner-LANE-B.md` · `20260907_1524_LANE-K-NUMBERED-GT-300-GT-301.md`
   · `20260907_1610_LANE-CS-TO-LANE-B-field-mobs-importer-pin-widened.md` — **อ่านแล้ว ยังไม่เริ่ม** ·
   ทั้งสามเป็นงานลำดับ 2-3 ของ COO (`GT-300` = GT-178) และงานแรกกินรอบนี้ทั้งรอบ ⇒ ยกไป "รอบหน้าทำอะไร"
   (ไม่วาง `.CONSUMED.txt` ให้สามใบนี้ เพราะยังไม่บริโภคจริง — การวาง stub ให้ใบที่ยังไม่ทำคือการทำให้ใบหาย)

## 🔴 งานแรกตามคำสั่ง COO ข้อ 5 — วัดแล้ว และคำตอบแยกเป็นสอง

ขับ `state.dispatch()` จริงบนบูตไร้แฟล็ก ไม่มี scenario ใด ๆ ในฉาก `Bg0002` (ฮาร์เนสเดียวกับ
`tests/test_mob_combat_dispatch_bg0002_kill.py`) · **ไม่มีอะไรในเส้นทางการตีถูกแทน** — โรสเตอร์ · ledger ·
census · AI register · `mob_combat.strike` · `mob_death` · dispatcher เป็นของจริงทั้งหมด
สิ่งเดียวที่ถอดออกชั่วคราวคือ **ใบอนุญาต** (แถวใน `mob_death.WIDENING_RULINGS` ที่คุ้มแถวของ `Bg0002`)
ซึ่งคือเงื่อนไขที่ใบสั่งถามพอดี: "มอนที่ไม่มีใครอนุญาตให้ฆ่า"

### (ก) `target_outside_the_sanctioned_scope` — **ไม่คลาย** ⇒ ข้อกังวลนี้ปิด

    PROBE target=0x2033 template=31 scene=Bg0002
    PROBE ruling_for raises: target_outside_the_sanctioned_scope
    MOB_DEATH_REFUSAL_UNWOUND_DISPATCH no labels=['WORLD_CENSUS_BG0002_INITIAL_97',
        'WORLD_CENSUS_BG0002_REAPPLY_97', 'MOB_COMBAT_POSE_TRIAL', 'MOB_COMBAT_ANNOUNCE']
    PROBE events=['mob_death_refused_target_outside_the_sanctioned_scope_no_death_frames']
    PROBE ledger_after hp=0/3857
    SECOND_BLOW labels=['MOB_COMBAT_POSE_TRIAL']
    CONTROL labels=[... 'MOB_COMBAT_ANNOUNCE', 'MOB_DEATH_DYING', 'MOB_DEATH_DEAD', 'MOB_LOOT_DROP']

อ่านว่า: **การตียังลงจริง** (`MOB_COMBAT_ANNOUNCE` ยังถูกประกอบ) · ไม่มีเฟรมตาย ไม่มีของตก ·
session จดชื่อคำปฏิเสธไว้ · ตัวมอนถูกทิ้งไว้ที่ **0/3857 HP ไม่มีศพ** · ตีซ้ำได้โดยไม่มีอะไรเกิดขึ้น
⇒ ตรงกับที่ COO สั่ง: **"ตีไม่ตาย" ไม่ใช่ "โลกว่าง"**

🔴 และผมพูดตรง ๆ ว่าสภาพนี้**ไม่ดี** มันแค่ **ดีกว่าเซสชันตาย**: มอนยืนที่ 0 HP แล้วเงียบไปเลย
ไม่มีใครเคยเห็นบนจอว่าไคลเอนต์วาดสภาพนี้เป็นอะไร — บันทึกไว้เป็น nonclaim ไม่ใช่ความสำเร็จ

### (ข) 🔴 `raise` เปล่าที่เหลืออยู่ในบล็อกเดียวกัน — **คลายจริง**

`runtime.py:5558-5563` โยนต่อทุกเหตุผลที่ไม่ใช่ `REFUSE_REGISTER_STALE` · บังคับวัดด้วยการสตับ
`commit_death_and_prepare_hook` ให้คืน `already_dead`:

    COMMIT_PATH_UNWOUND_DISPATCH yes exc=MobDeathContractError reason=already_dead

และ `gm/login_scene_consume.py:243` เขียนไว้เองว่า v141 **ไม่มี except ครอบ `state.dispatch`**
⇒ ปลายทางคือเธรดฟังตาย = **โลกเงียบ**
- **ผมไม่แก้เอง**: `runtime.py` เป็นเขต chief ⇒ ออกใบ
  `notes_to_chief/20260907_1641_LANE-B-CORE-REQUEST-dispatch-edge-swallows-only-half-the-death-refusals.md`
  (มีโทเคน `grep` ว่าบล็อกมีจริงบน `fade2d5` ตามกฎ NOW)
- **ผมไม่อ้างว่าเส้นทางจริงวันนี้ไปถึงมันได้** — คอมเมนต์ของ chief เขียนว่า "unreachable today" และผม
  **ยืนยันไม่ได้ทั้งสองทาง** · ที่วัดคือ**รูปร่างของขอบ** ไม่ใช่ความถี่

## เทสที่ปักคำตอบ (เขต B · ไฟล์ใหม่)
`tests/test_mob_death_refusal_does_not_unwind_dispatch.py` — 5 ใบ เขียวทั้งหมด
🔴 **ตัวคุมนี้ทำให้ตัวเองแดงได้จริง วัดแล้วไม่ใช่อ้าง**: ลบ `except mob_death.MobDeathContractError`
ที่จุดฆ่าโรสเตอร์ใน `runtime.py` ออก (มิวแทนต์ รันจริง แล้วคืนไฟล์) ⇒ **4 ใน 5 ใบแดง** ·
ใบคุม (`test_the_control_kill_still_dies`) **ยังเขียว** ⇒ ไฟล์นี้ผ่านด้วย dispatcher ที่เลิกฆ่าอะไรเลยไม่ได้
ก่อนรอบนี้ ตัวกันที่ทำให้ผู้เล่นไม่เห็นโลกเงียบ **ไม่มีอะไรปักไว้เลยทั้งรีโป**

**รันซ้ำได้ด้วยคำสั่งเดียว** (ครึ่ง (ก) ทั้งหมดอยู่ในไฟล์นี้ ไม่ต้องมีสคริปต์นอกรีโป):

    $ python3 -m pytest tests/test_mob_death_refusal_does_not_unwind_dispatch.py -q
    5 passed

ครึ่ง (ข) **รันซ้ำไม่ได้ด้วยไฟล์ในรีโป** เพราะต้องสตับฟังก์ชันของ chief · วิธีวัดซ้ำเขียนไว้ในใบ CORE-REQUEST
และผมพูดตรง ๆ ว่าสคริปต์ที่ผมใช้วัดเป็นสคริปต์ชั่วคราวที่ลบทิ้งแล้ว ไม่ได้ commit ไว้เป็นหลักฐาน

## กู้งานรอบ `nxcwdn` ที่ตายไปกับ `pirate-force-server#1043`
จดหมาย `1616` แจ้งว่า PR ถูกปิดเพราะเกตแดง (คอมมิต `3a5c4da` ไม่มีพิน skip — D1 ของ adversary รอบนั้น)
**กิ่งเดิมมีคอมมิตแก้อยู่แล้ว** (`8506707`) ที่ push หลังเกตรัน ⇒ รอบนี้ `cherry-pick` **ทั้งสองใบ**
ขึ้นกิ่งของตัวเอง (สะอาด ไม่มี conflict) แทนการเปิด PR ใบที่สองจากกิ่งของรอบอื่น (กฎ: หนึ่ง PR ต่อรีโปต่อรอบ)
⇒ กฎ `--outfit-rule` + `verify-frozen-any` + เทส 7 ใบ กลับเข้าคิวขึ้น main อีกครั้งในใบเดียวกับงานรอบนี้
🔴 **ข้ออ้างที่ถูกหักไปแล้วยังติดมากับคอมมิตเหล่านั้น** (D3 · D4 · D6 · D7 · D10 · D11 ของภาคผนวก `nxcwdn`)
ผม **ไม่แก้ในรอบนี้** เพราะงานแรกของ COO กินรอบ และการแก้ docstring ปนกับการกู้ทำให้ cherry-pick อ่านไม่ออก
⇒ เป็นงานรอบหน้าข้อ 2 ตามลำดับเดิมของภาคผนวก · **ห้ามอ่านคอมมิตสองใบนั้นว่าข้ออ้างในนั้นถูกแล้ว**

## หลักฐาน
- **wire/DB**: ไม่มี — รอบนี้ไม่มีอะไรของรอบนี้ไปถึงสายจริง
- **client-observable**: ไม่มี · ไม่ได้เปิดเกม ไม่ได้แตะ `GameClient/`
- **เครื่องมือ (แยกจากสองชั้นข้างบนโดยตั้งใจ)**: โทเคน headless ข้างบน (รันบน `fade2d5` + กิ่งรอบนี้) ·
  มิวแทนต์ 4/5 แดง · ชุดเป้าหมาย 5 ใบเขียว ·
  **ชุดเต็มบนต้นไม้สุดท้าย (หลัง `git merge origin/main`) `pytest tests/` = 13493 passed, 401 skipped,
  0 failed, 37369 subtests (652 s)** · `tools_bridge/pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS**
  (รวมสเต็ป precondition census และ "no new skips" ⇒ ไฟล์เทสใหม่ไม่ skip อะไรเลย ไม่ต้องพินใน
  `docs/PYTEST_SKIP_PINS.json` — ไม่ใช่ D1 ของรอบ `nxcwdn` ซ้ำ ตรวจแล้วไม่ใช่เดา)
- **nonclaims**: (1) ไม่อ้างว่าผู้เล่นเห็นอะไรต่างจากเมื่อวาน (2) ไม่อ้างว่าไคลเอนต์วาดมอน 0 HP ที่ไม่ตาย
  ว่าอะไร — ไม่มีใครดู (3) ไม่อ้างว่าประตูอื่นที่ไปถึงการฆ่า (`diag_multi_object`, `mob_respawn`,
  `mob_death_persistence`, `scene_door_walk`, AI tick) ปลอดภัย — รอบนี้ขับประตูเดียว
  (4) ไม่อ้างว่า `raise` ตัวที่คลายนั้นเกิดขึ้นได้จริงวันนี้ (5) ไม่อ้างว่าคอมมิตที่ cherry-pick มาถูกทั้งหมด

## `TWO_SESSIONS_SAME_SCENE:`
ไม่กระทบ · รอบนี้ไม่เขียน combat state ลง registry ไม่แตะ world registry ของ LANE-A และไม่เพิ่ม state
ที่ผูกกับ session · เทสใหม่สร้าง session เดียว อ่านค่าจาก ledger/register ของ session นั้นเท่านั้น

## 🔴 ข้อหนึ่งใน NOW ที่ **เสร็จไปแล้ว** — เสนอ COO ลบออกจากลำดับของสาย B
NOW/ใบ `1541` ตั้งลำดับข้อ 2 ไว้ว่า "`name_tokens` ให้ `_letter_exists_for` (`1141`)" ·
**ทำเสร็จแล้วตั้งแต่รอบ `occzj8`/`mhr9y6`** ไม่ใช่ค้าง — ตรวจแล้วทั้งสองข้อของใบ `1141`:

    $ grep -n "DEFAULT_LETTER_NAME_TOKENS\|name_tokens" tests/test_mob_death_widening_schema_gate.py
    $ grep -n "name_tokens" tests/test_mob_death_withheld_scene_deny_list.py
    (สำเนาที่สองยุบมาเรียกประตูกลางแล้วจริง ผ่าน `import test_mob_death_widening_schema_gate as schema_gate`)

⇒ ลำดับที่เหลือจริงของสายนี้คือ `GT-300` → สอง parser `2032` → respawn 120 s (ขยับขึ้นหนึ่งขั้น)

`ADVERSARY_PENDING pirate-force-server (branch claude/magical-albattani-jkrcej)` — สั่งไปตอน 16:48
ผลยังไม่คืนตอน push · **รอบถัดไปของสาย B: อ่านผลนี้เป็นงานแรก** · ผมยังไม่เขียนว่า "ผ่าน adversary" ที่ไหน
สิ่งที่สั่งให้มันโจมตีโดยเฉพาะ: การถอดใบอนุญาตเป็นตัวแทนของมอนที่ไม่มีใบคุ้มจริงหรือไม่ · ประตูอื่นที่ไปถึงการฆ่า ·
มิวแทนต์ของ except · ความเข้าถึงได้จริงของ `raise` ตัวที่คลาย · และอะไรบนกิ่งนี้ที่ทำเกต Windows แดง

## รอบหน้าทำอะไร
1. **ถ้าเห็นติ๊ก `death scope`** → พลิก `bg0002` ให้จบรอบเดียวทันที (regenerate roster + AI + drop
   ในคอมมิตเดียว · เซตใหม่ `{27..35}` **ไม่มี `103`** ตามของฝาก LANE-K) — COO อนุญาตไว้แล้ว ไม่ต้องถามซ้ำ
2. **หนี้ของคอมมิตที่กู้มา** ตามลำดับความเสียหายเดิม: D3 (คุมค่า 31 แถว + แก้ข้ออ้างเกินจริงใน docstring)
   → D5 → D4 → D6 → D11 → D10 → D7 → D12 → D8
3. **`GT-300`** (= GT-178 · จดหมาย `1441`/`1524`): ส่งเนื้อใบ `*-TO-K-gt-body-*` · register+tick ทุกฉากที่มี
   roster (`MOB_AI_TICK_LIVE`) → มอนตีถึงผู้เล่นจริง
4. สอง parser `2032` → respawn 120 s (ข้อ `name_tokens` ตัดออกแล้ว ดูหัวข้อข้างบน)
5. ถ้า chief รับใบ CORE-REQUEST ข้างบน: เขียนเทสปักครึ่งที่สองทันทีที่ขอบ dispatch เป็นของกลาง

SCOREBOARD: COMING | ยังไม่มีอะไรที่ผู้เล่นทำได้เพิ่มวันนี้ — แต่คำถามที่ค้างว่า "ถ้ามอนที่ไม่มีใบอนุญาตโดนตี ผู้เล่นจะเห็นมอนไม่ตาย หรือเห็นโลกเงียบ" ถูกวัดจบแล้ว: เห็นมอนไม่ตาย และมีตัวคุมที่แดงได้จริงกันไว้ · อีกครึ่งหนึ่งของขอบเดียวกันคลายจริงและส่งเป็นใบถึง chief แล้ว | pf_bridge#1744 + PR เซิร์ฟเวอร์รอบ jkrcej + จดหมาย 20260907_1641_LANE-B-CORE-REQUEST-*
