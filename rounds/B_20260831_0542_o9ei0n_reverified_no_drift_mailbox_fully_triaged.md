# LANE-B (COMBAT) รอบ `o9ei0n` -- 2026-08-31T05:42+07:00 (scheduled, ไม่มีคนเฝ้าหน้าจอ)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** รอบนี้ไม่แตะ `src/` ในทั้งสอง repo -- ตรวจสดว่า backlog ของสาย B ทุกจุดยังบล็อกด้วย
เหตุผลที่มีคนตัดสินไปแล้ว (เหมือนที่รอบ `upf0xp` วัดไว้เมื่อ 3 ชั่วโมงก่อน) และกล่องจดหมายไม่มีใบ
ใหม่ที่จ่าหน้าถึงสาย B ค้างให้บริโภค -- บอกตรง ๆ แทนการแต่งงานขึ้นมาทำ

## ต้นรอบ -- ตรวจสถานะสด (ข้อ A)

- ไม่มี `mcp__github__*` tool จริงในชุดเครื่องมือของสาย B รอบนี้เช่นเดิม (ทดสอบ
  `list_pull_requests`/`get_pull_request`/`pull_request_read`/`search_pull_requests` ทั้งมี/ไม่มี
  prefix `mcp__github__` -- ทุกตัวตอบ "No such tool available") -- ใช้ `curl` + `$GITHUB_TOKEN`
  ยิง GitHub REST API ตรงแทนตลอดทั้งรอบ (list PRs, สร้าง PR)
- ตรวจ PR ปิดล่าสุดของสาย B (`pirate-force-server#360`) ผ่าน GitHub API ตรง: `merged=true` จริง --
  งานรอบก่อน (`jiy6lj`) อยู่บน `main` แล้ว ไม่มีอะไรต้อง cherry-pick
- ไม่มี PR เปิดค้างหัวข้อ `[LANE-B]` ในทั้งสอง repo ก่อนรอบนี้ (`GET /pulls?state=open` กรอง title --
  มีแค่ PR ของสาย GM #361 ที่ merge ไปแล้ว และไม่มี PR เปิดค้างเลยใน `pf_bridge`) ⇒ เปิด draft PR
  ใหม่ยึดล็อกก่อนเริ่มงาน (`pirate-force-server#363`)
- `local branch` ของรอบนี้ (`claude/tender-goldberg-o9ei0n`) อยู่หลัง `origin/main` หนึ่ง merge
  (PR #361 ของสาย GM, `label npc_switch_catalog`) -- ทำ `git merge --ff-only origin/main` ก่อน
  เริ่มงานใด ๆ (ไม่มี divergence ของตัวเอง จึง fast-forward ได้ตรง ๆ ไม่ต้อง rebase)

## กล่องจดหมาย -- grep `ADDRESSEE: LANE-B` ทุกไฟล์ใน `notes_to_chief/` (ข้อ B)

ไล่ทุกไฟล์ `.md` ที่ไม่มี `.CONSUMED.txt`/`consumed/...CONSUMED.txt` คู่กัน แล้วกรองเอาเฉพาะใบที่
`ADDRESSEE` เป็น `LANE-B` และ "จาก" ไม่ใช่สาย B เอง (ใบขาออกของสาย B เองไม่ต้อง stub ตัวเอง) --
**ไม่มีใบใหม่**. รายละเอียดที่ตรวจ:

- `20260829_1323_CHIEF-TO-LANE-B-identity-width-pin-and-normalize-*.md` (ใบที่ระบบสั่งงานอ้างถึง
  โดยตรงว่า "สาย B: RE-098" -- แต่เนื้อในจริงคือคำขอ identity-width pin/normalize) **มี stub อยู่
  แล้วทั้งสองรูปแบบ** (`consumed/...CONSUMED.txt` และ `...md.CONSUMED.txt`) -- ตรวจโค้ดจริงยืนยันว่า
  งานที่ขอ (เทสพิน + normalize `mob_loot._require_identity`/`mob_pickup._require_identity` ให้กว้าง
  เท่ากัน) **เสร็จไปแล้วจริงตั้งแต่รอบ `uq2lxw2` (2026-08-29T13:05+07:00)** -- ก่อนใบของ chief
  (2026-08-29T13:23+07:00) จะถูกส่งมาด้วยซ้ำ (จดหมายไขว้กัน): `mob_pickup.MAX_ACTOR_IDENTITY =
  mob_loot.MAX_IDENTITY` (binding ผ่าน AST, ไม่ใช่ literal คู่ขนาน) และ
  `tests/test_mob_pickup.py` มีเทสพินความกว้าง + เทส AST ยืนยันว่ายังผูกกันอยู่ (บรรทัด 1944-2042)
- `RE-098` เอง: ปิดและ consumed แล้วตั้งแต่ 2026-08-27 (`consumed/20260827_0710_RE-098-RESULT-*`)
  -- คำสั่งงานที่อ้างถึง RE-098 ในระบบสั่งงานของรอบนี้เป็นสถานะเก่ากว่ารอบปัจจุบันมาก (ค้างจาก
  ประมาณ R172) ไม่ใช่งานที่ยังต้องทำ
- `RE-067` (สีชื่อ) ที่ระบบสั่งงานบอกว่า "ยังเปิด เป็นของสาย RE" ก็ปิดไปแล้วเช่นกัน (archived
  2026-08-27, `CLIENT_RE_QUEUE.md:112`) -- `mob_census_hostility.py:33` อ้างผลปิดนี้อยู่แล้ว ไม่มี
  อะไรให้สาย B ทำเพิ่ม
- ใบเดียวที่ไม่มี stub ในกล่องคือใบ `ASK-COO`/`STATUS` ของสาย A/GM/chief เอง (~90 ใบ ตามที่ chief
  เพิ่งรายงานใน `20260831_0457_CHIEF-ASK-COO-mailbox-stub-bug-*.md`) ซึ่งเป็นของ COO/chief บริโภค
  ไม่ใช่ของสาย B ตามกติกาเดียวกับที่ใบนั้นเองอธิบายไว้

⇒ **ไม่มี `.CONSUMED.txt` ใหม่ที่ต้องวางรอบนี้** -- ทุกใบที่จ่าหน้าถึงสาย B มีคนบริโภคไปแล้วจริง

## ไล่ backlog ของสาย B ทั้งหมดซ้ำ -- ตรวจสดทีละจุด (ไม่ก็อปจดหมายเดิม)

```
BUILD-004 (M3 สนามมีมอนสเตอร์)
  field_mobs._SCENE_TABLE_MODULES = {bg0001, bg0002} เท่านั้น (field_mobs.py:475-478) -- LIVE
  default-on จริง ไม่มีแฟล็ก ใช้แถวจริงจาก MOBS ผ่าน field_mob_tables*.py
  scene 14 (Bg0015): COO-DECISION 2026-08-26T12:46+07:00 ยังไม่ถูกยกเลิก -- ไม่ใช่ของสาย B แก้

BUILD-005 (M4 ตีได้ ตายได้)
  mob_death.kill()      : runtime.py:4504 (WIRED, default-on)
  mob_loot.roll_drops() : runtime.py:4768 (WIRED)
  mob_census_wire_count : runtime.py:4457, :4742 (WIRED) -- world-wipe fix ยืนยันซ้ำ:
  tests/test_world_wipe_headless_proof.py = 7 passed, 2 subtests passed (ไม่ regress)

BUILD-006 (M5 เก็บของได้)
  grep -c mob_pickup_persist runtime.py = 0 (ยังไม่มีจุดเสียบที่สาม)
  บล็อกจริง: GT-146 PICKUP-CLICK-OPCODE-CAPTURE-001 ยังเป็น PENDING (attended, หัวคิว) --
  GAME_TEST_QUEUE.md:8200/:26 ยืนยันสถานะเดิม ไม่มี opcode มาให้ต่อสาย
  lane_hooks/ ยังไม่มี lane_b_*.py (มีแต่ lane_a_*.py x2, lane_gm_*.py x2) -- ไม่มีจุดเสียบ
  combat-specific ให้ผูกล่วงหน้าอยู่แล้ว

RE-157 job 1/2 wiring (trade/combat membership guard -> runtime.py call site)
  predicate ครบสองไฟล์แล้ว (trade_session_membership.py, mob_combat_membership.py) --
  การต่อสายเข้า runtime.py เป็นการตัดสินใจของ chief ที่เลื่อนไว้แล้ว ไม่ใช่ของสาย B บังคับเอง

mob_aggro M6
  RE-150 ปิด BOUNDED-NEGATIVE แล้ว ไม่มีสัญญาณใหม่ให้เริ่ม

GT-132/GT-149 (coalesced drop labels / label life)
  บล็อกจริงคือ label_life ซึ่ง COO-DECISION 20260830_1742 ยืนกฎเดิม "สาย B ไม่ต้องทำอะไรเพิ่ม"
  จนกว่าจะมีรอบ attended วัดส่งซ้ำครั้งเดียว
```

สแกน `_WIRING`/`STATUS: WIRED` constant ทุกตัวในโมดูลของสาย B (`mob_death.MOB_DEATH_WIRING`,
`mob_combat.MOB_COMBAT_WIRING`/`MOB_COMBAT_CADENCE_WIRING`, `mob_pickup.MOB_PICKUP_WIRING`,
`mob_ai_control.MOB_AI_CONTROL_WIRING`, `mob_loot.MOB_LOOT_WIRING`,
`mob_drop_presence.DROP_PRESENCE_WIRING`, `mob_scene_recompose.SCENE_RECOMPOSE_WIRING`,
`mob_diag_multi_object.GT_DIAG_MULTI_OBJECT_WIRING`) เทียบกับ call site จริงใน `runtime.py` --
ไม่มีตัวไหนดริฟท์ (สองตัวล่าสุดที่เคยดริฟท์ถูกปิดไปแล้วโดยรอบ `hpronz` และ `jiy6lj`)

## pf-adversary

ไม่มี Agent/Task tool ให้เรียก subagent `pf-adversary` ตรงในเซสชันของสาย B รอบนี้ (เหมือนรอบก่อน
หน้าทุกรอบที่บันทึกปัญหาเดียวกันไว้) -- ทำ self-review แทน: รันสวีตเต็มก่อนแตะไฟล์ใด ๆ, grep ซ้ำทุก
เลขบรรทัด/เลขไฟล์ที่อ้างข้างต้นสดจากซอร์ส (ไม่ก็อปจากจดหมายรอบก่อน), และไม่อ้างว่าตรวจ cp874 ของ
ไฟล์นี้ (`pf_bridge`/`notes_to_chief`/`rounds` อยู่นอก scope ของเกต cp874 ตาม hard limit เดิม)

## ตัวเลขที่วัดได้

```
ไฟล์ที่แตะ (pirate-force-server): 1
  - rounds/B_20260831_0542_o9ei0n_CLAIM.md (ใหม่, force-added เหมือน CLAIM ก่อนหน้าทุกไฟล์
    เพราะ .gitignore deny-all ที่ root ไม่มี allowlist entry ให้ rounds/)

ไฟล์ที่แตะ (pf_bridge): 2 (นับเฉพาะรอบนี้ ไม่รวมไฟล์นี้เอง)
  - notes_to_chief/20260831_0542_LANE-B-STATUS-reverified-no-drift-mailbox-fully-triaged.md (ใหม่)
  - rounds/B_20260831_0542_o9ei0n_reverified_no_drift_mailbox_fully_triaged.md (ไฟล์นี้, ใหม่)

สวีตเต็ม (pirate-force-server, ก่อนรอบนี้ = หลังรอบนี้ เพราะไม่แก้ src/):
  5658 passed, 327 skipped, 9758 subtests passed, 0 failed (133.94s)
  (มากกว่า 5645/9733 ที่รอบ jiy6lj บันทึกไว้ -- เพิ่มจาก PR #361 ของสาย GM ที่ merge เข้า main
  ระหว่างสองรอบนี้ ไม่ใช่ของสาย B)
tests/test_world_wipe_headless_proof.py: 7 passed, 2 subtests passed (ไม่ regress)
```

## ยังไม่ได้พิสูจน์

ว่า backlog ที่ตรวจว่า "บล็อก" รอบนี้จะยังบล็อกอยู่รอบหน้า -- ขึ้นกับผล `GT-146` (attended, ยังไม่
บูต) และ COO-DECISION ใหม่ถ้ามี ไม่ใช่สิ่งที่รอบนี้ยืนยันได้

## CORE-REQUEST

ไม่มี

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT) รอบ `o9ei0n`
