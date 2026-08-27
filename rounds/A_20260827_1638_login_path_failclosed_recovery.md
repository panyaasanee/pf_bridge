# รอบ `A_lf7p3z` - สาย A - WORLD (`pf-builder`)

**เวลา:** 2026-08-27T16:38+07:00
**สาย:** A (WORLD)
**รอบ:** `lf7p3z`
**บริบท:** รอบกู้คืนงานของรอบ `0z3kjx` ที่ PR ปิดไปโดยไม่ merge (ดูหัวข้อ ② ก่อนอ่านอย่างอื่น)

---

## ① ประโยคบังคับของสาย: ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

> **`pirate-force-server`: ไม่มีอะไรเปลี่ยนบนจอเกมเลยสักบิต** — งานรอบนี้ทั้งหมดคือ fail-safe ชั้น foundation
> (`world_scene_entry.resolve_entry`) ที่ไม่มีอะไรเรียกด้วยพารามิเตอร์ใหม่ยกเว้นจุดเดียว
> (`columbus_quest_dispatch.resolve_columbus_arrival`, synthetic call ที่ไม่เคยอ่านแถวตัวละครจริงอยู่แล้ว)
> ส่วน `runtime.py`'s login call site เดิม (ที่มีอยู่แล้วจริงในโค้ดวันนี้ ไม่ใช่แผนอนาคต - ดูหัวข้อ ④) ไม่ถูก
> แตะเลยสักบรรทัด และยังคงพฤติกรรมเดิมทุกประการสำหรับทุกฉากที่มีอยู่ (1/2/278/997) ผลที่มองไม่เห็นบนจอ: ถ้าวันหนึ่ง
> แถวตัวละครใน DB มี `scene_id=17` ติดมา (วันนี้ยังไม่มีทางเขียนค่านั้นได้จริง) ตัวละครนั้นจะยัง refuse login แบบ
> เดิมที่เคยมีก่อนฉาก 17 จะมี spawn จริง แทนที่จะหลุดไปโผล่กลางทะเลที่ (0,0,0) โดยไม่ผ่าน dispatch ใดๆ
>
> **`pf_bridge`: เอกสารล้วน** ไม่มีโค้ด ไม่มีอะไรที่ผู้เล่นเห็น

---

## ② สิ่งที่เกิดขึ้นกับรอบก่อน (`0z3kjx`) - ทำไมรอบนี้ถึงมีอยู่

รอบ `0z3kjx` (บันทึกไว้ที่ `rounds/A_20260827_1544_scene17_provisional_spawn_decree_wired.md`, ซึ่งยังอยู่ใน
ประวัติ git ของ branch นี้) ทำงานจริงและมีค่า: ต่อสายพิกัดชั่วคราวฉาก 17 เข้า `world_scene_registry_001.json`
จริง และพบ+แก้ช่องโหว่ fail-safe ของ login path เอง (pf-adversary pass ภายนอกในรอบนั้น) — **แต่ PR ทั้งสองใบของ
รอบนั้น (pirate-force-server #127, pf_bridge #209) ปิดไปโดยไม่ merge** (`mergeable_state: dirty`) เกือบแน่นอน
เพราะ session ของรอบนั้นก็โดนบั๊กเดียวกับที่ผู้ใช้เตือนรอบนี้ไว้ตั้งแต่ต้น: **`git fetch origin main` ในแซนด์บ็อกซ์
นี้เคยคืน snapshot ของ `main` ที่เก่ากว่าจริง (พบครั้งหนึ่งเก่าเกินหนึ่งวันเต็ม) ทั้งที่คำสั่งรายงานว่าสำเร็จ** รอบ
`0z3kjx` เขียนโค้ดบน base ที่ล้าสมัยไปแล้ว พอ automerge workflow พยายาม land งานจริงจึงชนกันและถูก reaper ปิดทิ้ง
**นี่คือความเสี่ยงเชิง operational ที่ควรรู้ในวงกว้าง** (chief/COO) เพราะรูปแบบ "รอบสาย A merge ไม่ติด" นี้อาจไม่ใช่
เรื่องคุณภาพงาน แต่เป็นบั๊กของเครื่องมือ git fetch เอง - ผู้ใช้ (orchestrator) เจอปัญหาเดียวกันนี้ซ้ำกับ worktree ของ
รอบนี้เองด้วย (ดูหัวข้อ ③) ก่อนเริ่มงานจริง

**ของที่ superseded ไปแล้ว ไม่ต้องกู้คืน**: การต่อสาย spawn/ground ของฉาก 17 (`columbus_quest_dispatch.py`,
M2-no-vehicle dispatch) - chief cloud รอบ `e0daaa` (R194, PR #124, อยู่บน main แล้ว) ทำงานเทียบเท่า/ดีกว่าใน
ประเด็นเดียวกันไปแล้วอย่างอิสระ ตรวจโค้ดปัจจุบันแล้วยืนยัน: `scenarios/world_scene_registry_001.json`'s ฉาก 17 มี
`spawn={0,0,0}` พร้อม provenance `PROVISIONAL-OWNER-DECREE-20260827-1445` อยู่แล้วจริงบน main วันนี้ และ
`dispatch_columbus_quest3021()` ไม่ atomic-refuse อีกต่อไปแล้ว (M2-NO-VEHICLE-OWNER-20260827-1525) - สาย A ไม่แตะ
ส่วนนี้ซ้ำ

**ของที่ยังไม่ถูกกู้คืนจริงจนถึงรอบนี้**: ช่องโหว่ fail-safe ของ login path เอง - นี่คืองานหลักของรอบนี้ (ดูหัวข้อ
④)

## ③ base ของ worktree เอง stale เช่นกัน - แก้แล้วก่อนเริ่มงานจริง

worktree `pf_bridge` ของรอบนี้เช็คเอาต์ที่ commit `3733440` (sync จาก windows bridge วันที่ 2026-08-26 11:28 -
เก่ากว่าจริงเกินหนึ่งวัน) **ไม่มี** 3 คอมมิตของรอบ `0z3kjx` ที่ orchestrator บอกว่า rebase ไว้แล้วบน
`claude/quirky-planck-lf7p3z` (`0d77431`/`8deab4f`/`dad438e`) ทั้งที่คอมมิตเหล่านั้นมีอยู่จริงใน object database
เดียวกัน แก้โดย `git fetch /home/user/pf_bridge claude/quirky-planck-lf7p3z:refs/heads/quirky-planck-lf7p3z-real`
แล้ว `git checkout -B claude/quirky-planck-lf7p3z dad438e` - ตรวจแล้ว `git log --oneline -4` ตรงกับที่คาดไว้เป๊ะ
ทุกบรรทัด **ยังไม่ได้ commit อะไรก่อนแก้จุดนี้ จึงไม่มีอะไรต้อง rebase ซ้ำ** ฝั่ง `pirate-force-server` ตรวจแล้วว่า
`HEAD` ตรงกับ `0c8588845e63d70c3f08cfd6e808e1174858d8be` ที่ผู้ใช้ระบุไว้เป๊ะ (อ่านตรงจาก `.git/refs/heads/...`
ไม่ผ่าน `git` command เพราะ worktree isolation ห้ามเรียก `git` ข้ามไดเรกทอรีในแซนด์บ็อกซ์นี้)

## ④ งานหลักรอบนี้: login-path fail-closed gate (กู้คืนจากรอบ `0z3kjx` โดยเขียนใหม่บนโค้ดปัจจุบัน)

**พบจริง**: `world_scene_entry.resolve_entry()` คือฟังก์ชันเดียวกันเป๊ะที่ `runtime.py:4715` เรียกตอน login จริง
ทุกครั้ง (**ต่อสายแล้วจริงบน main วันนี้ ไม่ใช่แผนที่ยังไม่ได้ทำ** - docstring เดิมของโมดูลนี้ยังเขียนว่า "NOTHING
CALLS IT YET" ซึ่งล้าสมัยไปแล้ว บันทึกไว้เป็นข้อสังเกตในหัวข้อ ⑦ ไม่ได้แก้เองเพราะอยู่นอก scope ของรอบนี้)
ด้วย `self.foundation.selected.position` คือแถวที่ persist ไว้จริงของตัวละครนั้น ก่อนฉาก 17 จะมี spawn จริง
`resolve_entry()` refuse ฉาก 17 ให้ฟรีอยู่แล้ว (`REFUSED_NO_PINNED_SPAWN`) เพราะ `target.spawn is None` เสมอ
พอฉาก 17 มี `spawn={0,0,0}` จริงแล้ว (จาก R194) refusal ฟรีตัวนั้นหายไปด้วย - ไม่มีอะไรมาแทนที่ - หมายความว่า
ถ้าแถวตัวละครใน DB เคยมี `scene_id=17` (ไม่มี `CHECK` constraint ห้ามไว้เลย - `migrations/001_initial.sql:5`)
ตัวละครนั้นจะ login **สำเร็จ** และถูกวางกลางทะเลที่ (0,0,0) โดยข้าม `dispatch_columbus_quest3021`'s
vehicle-bind refusal ไปเลย เพราะ login path ไม่เคยเรียก dispatch function นั้น อ่านแค่ registry ผ่าน
`resolve_entry` เท่านั้น สถานการณ์นี้ยัง **latent** จริง (ยังไม่มีอะไรเขียน `scene_id=17` ลง DB ได้จริงวันนี้) แต่
เป็นการเอา fail-closed guarantee ของฉาก 17 ออกไปเงียบๆ โดยไม่มีใครตั้งใจ

**การแก้**: เพิ่มฟิลด์เสริม `login_entry_allowed` (bool, optional) บน destination ใน
`world_scene_registry_001.json` - default `True` เมื่อไม่ระบุ (ฉาก 1/2/278/997 ไม่เปลี่ยนพฤติกรรมเลยสักบิต -
มีเทสยืนยันตรงๆ) ฉาก 17 ตั้งเป็น `false` พร้อมคำอธิบายในฟิลด์ `table_row_differences.login_entry_allowed_because`
เพิ่มพารามิเตอร์ `via_login: bool = True` ใน `world_scene_entry.resolve_entry()` - ค่า default `True` คือ
"นี่คือ login path" และจะ raise `SceneEntryRefused(REFUSED_NOT_ALLOWED_AT_LOGIN, ...)` ถ้าฉากนั้น
`login_entry_allowed=False` **ไม่แตะ `runtime.py` เลยสักบรรทัด** เพราะ default ของ `via_login` ทำหน้าที่แทน -
`runtime.py:4715`'s call site เดิม (`resolve_entry(position, registry=...)`, ไม่ส่ง keyword ใหม่) ได้พฤติกรรม
fail-closed อัตโนมัติ `columbus_quest_dispatch.resolve_columbus_arrival()` (โมดูลของสาย A เอง) แก้ให้ส่ง
`via_login=False` explicit เพราะมันไม่ได้อ่านแถว persist ของตัวละครเลย (`synthetic_stored` สร้างใหม่ทุกครั้ง ไม่
เคยโหลดจาก DB)

โครงสร้างของ diff เดิมจากรอบ `0z3kjx` (เก็บไว้อ่านที่
`/tmp/claude-0/.../scratchpad/lost_fix_2f8530a.diff` โดยผู้ใช้) ใช้กลไก `ground_bound_waiver` ของ `_spawn()` ซึ่ง
**ไม่มีอยู่แล้วในโค้ดปัจจุบัน** (R194 เปลี่ยนกลไกนั้นเป็นการเช็ค prefix `PROVISIONAL-OWNER-DECREE` ของ
`spawn_provenance` โดยตรงใน `_within_ground()`/`_spawn()` แทน) - เขียนใหม่ทั้งหมดตามเจตนาเดิม ไม่ใช่ apply patch
ตรงๆ (cherry-pick ตรงจะชนแน่นอนตามที่ผู้ใช้เตือนไว้)

## ⑤ ของที่แตะจริงใน `pirate-force-server` (7 ไฟล์ ไม่แตะ `runtime.py`/`app.py`/`current/`)

| ไฟล์ | อะไร |
|---|---|
| `src/pirateforce_foundation/world_scene_travel.py` | เพิ่มค่าคงที่ `DEFAULT_LOGIN_ENTRY_ALLOWED = True`, ฟิลด์ `SceneDestination.login_entry_allowed`, helper `_require_bool`, ต่อสาย loader อ่าน/validate ฟิลด์เสริมจาก JSON |
| `src/pirateforce_foundation/world_scene_entry.py` | เพิ่มค่าคงที่ `REFUSED_NOT_ALLOWED_AT_LOGIN`, พารามิเตอร์ `via_login: bool = True` บน `resolve_entry()`, เช็คจริงก่อน `REFUSED_NO_PINNED_SPAWN` |
| `src/pirateforce_foundation/columbus_quest_dispatch.py` | `resolve_columbus_arrival()` ส่ง `via_login=False` explicit + docstring อธิบายกลไก |
| `scenarios/world_scene_registry_001.json` | ฉาก 17 (`n_id=17`) เพิ่ม `"login_entry_allowed": false` + คำอธิบายใน `table_row_differences.login_entry_allowed_because` |
| `tests/test_world_scene_entry.py` | +class `LoginEntryRestrictionTests` (8 เทสใหม่) + import `REFUSED_NOT_ALLOWED_AT_LOGIN` + แก้ 2 เทสเดิมใน `ProvisionalDecreeTests` ให้ส่ง `via_login=False` (เทสกลไก ground/decree ไม่ใช่เทส login gate) |
| `tests/test_world_scene_travel.py` | +3 เทสใหม่ (field parsing/default/non-bool refusal) + เพิ่ม assertion 1 บรรทัดในเทสเดิม |
| `tests/test_columbus_quest_dispatch.py` | +1 เทสใหม่ (`test_calls_resolve_entry_with_via_login_false`, ยืนยัน mock ว่าเรียกจริงด้วย keyword นี้ ไม่ใช่แค่ default) |

## ⑥ ตัวเลขที่วัดได้

- เทสกลุ่มเป้าหมาย (6 ไฟล์: `test_world_scene_entry` + `test_world_scene_travel` + `test_columbus_quest_dispatch`
  + `test_columbus_quest_dispatch_wiring` + `test_world_travel_gate` + `test_world_travel_gate_wiring`) =
  **246/246 ผ่าน, 102 subtests ผ่าน**
- เทสทั้งเรโป (`pytest`, `--continue-on-collection-errors`): **3305 เทสผ่าน, 198 skipped, 3573 subtests ผ่าน,
  23 collection errors** - ทั้ง 23 คือ `ModuleNotFoundError: No module named 'capstone'`/`'tools'` เดิมที่มีอยู่
  ก่อนรอบนี้ (ตรวจชื่อไฟล์ error ทั้งหมดแล้ว ไม่มีไฟล์ที่รอบนี้แตะสักไฟล์เดียว) - **0 FAIL จริง**
- เทสใหม่ที่เพิ่มรอบนี้: **12 เทส** (8 + 3 + 1 ตามตารางข้างบน)
- cp874-encodability: ตรวจทุกไฟล์ที่แตะใน `src/`/`tests/`/`scenarios/` ด้วย `.encode('cp874')` ผ่านหมดจริง
  (ตรวจเป็นสคริปต์ ไม่ใช่อ่านตาเปล่า)
- ยืนยันสด (headless script, ไม่ใช่เทส): แถวตัวละครสมมติที่ `scene_id=17` เรียก `resolve_entry(row, emit=...)`
  แบบ login call shape (ไม่ส่ง `via_login`) refuse จริงด้วย reason `scene_not_allowed_at_login`; เรียกซ้ำด้วย
  `via_login=False` สำเร็จจริงและพิมพ์ `SCENE_ENTRY scene=17 ... source=PROVISIONAL-OWNER-DECREE-20260827-1445`
  เหมือนเดิม; `columbus_quest_dispatch.resolve_columbus_arrival()` ยังสำเร็จเหมือนเดิมทุกประการ (ไม่มีอะไรใน
  behavior ของ M2 เปลี่ยนไป)

## ⑦ pf-adversary self-review pass (ไม่มี agent ให้เรียกในสภาพแวดล้อมนี้ - ทำเองแบบ adversarial)

ไม่มี tool สำหรับเรียก pf-adversary agent แยกในรอบนี้ (ไม่มี Task/agent-spawn tool ให้ใช้) ทำ self-review แบบ
adversarial แทน เช็คทีละข้อตามที่ผู้ใช้สั่ง:

1. **default fail-closed สำหรับทุกฉากเดิมจริงหรือไม่** - ตรวจแล้ว: `DEFAULT_LOGIN_ENTRY_ALLOWED = True` ใช้เมื่อ
   ไม่มีฟิลด์ในเดต้าคลาส และ `via_login` default `True` ทำให้เช็คทำงานเสมอเว้นแต่ผู้เรียกส่ง `False` ชัดเจน grep
   ทั้งเรโปยืนยัน **มีจุดเดียวเท่านั้น** ที่ส่ง `via_login=False` จริง
   (`columbus_quest_dispatch.py:291`) เทส `test_every_other_destination_defaults_login_entry_allowed_true` และ
   `test_login_restricted_scenes_other_than_17_are_unaffected` ยืนยันตรงๆ
2. **ฟิลด์ schema validate/reject junk values จริงหรือไม่** - `_require_bool` เช็ค `type(value) is not bool`
   ตรงๆ (เข้มกว่า truthy check) เทส `test_a_non_bool_login_entry_allowed_is_refused` ยืนยันด้วยค่า `1, "false",
   None, 0` ทุกตัว raise `ValueError` จริง และ `resolve_entry`'s เอง `type(via_login) is not bool` ก็เช็คเช่น
   เดียวกัน เทส `test_via_login_must_be_a_bool` ยืนยัน
3. **มีทางไหนที่ `via_login` default ผิดแล้วเปิดประตูเงียบๆ ไหม** - grep `resolve_entry(` ทั้งเรโป (ไม่นับเทส) พบ
   แค่ 2 จุด: `runtime.py:4715` (ไม่ส่ง `via_login` - ได้ default `True` = ปลอดภัย) กับ
   `columbus_quest_dispatch.py:290` (ส่ง `via_login=False` ชัดเจน เพราะ synthetic call เท่านั้น) ไม่มีจุดที่สาม
   **[พบและแก้เองระหว่างรัน targeted tests]**: เทสเดิม 2 ตัวใน `ProvisionalDecreeTests`
   (`test_a_row_far_outside_real_ground_but_near_the_decree_point_still_relocates`,
   `test_a_row_genuinely_far_from_the_decree_also_relocates_and_prints_the_token`) เรียก `resolve_entry` บนแถว
   สมมติของฉาก 17 แบบ login call shape (ไม่ส่ง `via_login`) เพื่อทดสอบกลไก ground/decree relocation - หลังเพิ่ม
   gate ใหม่ เทสทั้งสองพัง (ถูกต้องแล้ว - นี่คือพฤติกรรมที่เปลี่ยนจริงตามที่ตั้งใจ) แก้โดยเพิ่ม `via_login=False`
   ให้เทสทั้งสองพร้อม comment อธิบายว่าเทสกลุ่มนี้ทดสอบกลไก relocation ไม่ใช่ login gate (คนละเรื่องกัน) รันซ้ำ
   ผ่านหมดจริง ไม่ได้แค่แก้ให้เขียวเฉยๆ
4. **docstring เดิมล้าสมัย (พบ ไม่แก้ เพราะนอก scope)** - `world_scene_entry.py`'s module docstring ยังเขียนว่า
   "NOTHING CALLS IT YET" ทั้งที่ `runtime.py:4715` เรียกจริงแล้วตั้งแต่รอบก่อนๆ (ไม่ใช่รอบนี้) - ไม่แก้เพราะเป็น
   doc sweep ใหญ่กว่าที่รอบนี้ตั้งใจทำ บันทึกไว้ให้ chief/COO ทราบแทน
5. **`docs/FUNCTIONAL_COVERAGE.json`'s CORE-REQUEST-014 note (พบ ไม่แก้ เพราะนอก scope)** - note เดิมยังเขียนว่า
   `dispatch_columbus_quest3021` "ALWAYS refuses" ด้วย "two named, independent evidence gaps" ซึ่งล้าสมัยไปแล้ว
   ตั้งแต่ R194 (ไม่ atomic-refuse อีกต่อไป, M2-NO-VEHICLE) - stale ก่อนรอบนี้เริ่มด้วยซ้ำ ไม่ใช่ผลจากรอบนี้ ไม่แก้
   เพราะต้องอธิบาย M2-NO-VEHICLE ทั้งกลไกซึ่งไม่ใช่งานของสาย A รอบนี้ (เป็นงานของ chief cloud รอบ `e0daaa`)
   บันทึกไว้เป็นข้อสังเกตแทนการแก้เอง

## ⑧ BUILD-002 (ฉาก 278 เป็นเส้นทางออกเริ่มต้น) - ยืนยันซ้ำว่ายังบล็อกอยู่

`notes_to_chief/20260826_2147_COO-DECISION-BUILD-002-scene278-stays-blocked.md` ยังไม่มีคำสั่งใหม่มายกเลิก -
สาย A **ไม่ทำ** ตามคำสั่งเดิม และ **ไม่เปิด ASK-COO ซ้ำ** ตามที่จดหมายฉบับนั้นสั่งไว้ตรงๆ ไม่ให้ถามซ้ำ

## ⑨ ตรวจ mailbox - ไม่มีจดหมายจริงที่ค้าง

ไล่อ่าน `notes_to_chief/*.md` ที่มี timestamp หลัง `2026-08-27 15:44` (ตอนจบรอบ `0z3kjx`) ทั้งหมด: พบ 3 ฉบับที่ cc
สาย A (`20260827_1545_CHIEF-STATUS-M2-quest-gate-skip-*`, `20260827_1600_CHIEF-STATUS-M2-console-token-fix-*`,
`20260827_1600_CHIEF-ASK-COO-world-population-handoff-*`) **ทั้งหมดเป็น broadcast ของ chief ไปหา Panya/COO โดย
cc สาย A เฉยๆ ไม่มีข้อไหนสั่งงานสาย A โดยตรง** เนื้อหาคือความเสี่ยงของ M2 (client FSM gate, retry-once,
quest-gate-skip) ที่ chief พบระหว่างรอบ `e0daaa` เอง - ไม่เกี่ยวกับ scope ของรอบนี้ (login-path fix) และไม่มี
action item ให้สาย A ไม่พบจดหมายที่จ่าหน้าถึงสาย A โดยตรง (`ถึง: ... สาย A`) ที่ยังไม่มี `.CONSUMED.txt` คู่ในช่วง
เวลานี้เลย **ไม่เปิดงาน consumption ปลอมขึ้นมา**

## ⑩ CORE-REQUEST

none - ไม่ต้องแตะ `runtime.py`/`app.py` เลยรอบนี้ ยืนยันด้วยการ grep หา call site ทั้งหมดของ `resolve_entry`
ทั้งเรโปแล้ว (หัวข้อ ⑦ ข้อ 3) `runtime.py:4715`'s call site เดิมได้พฤติกรรม fail-closed อัตโนมัติจาก default ของ
`via_login` โดยไม่ต้องแก้บรรทัดเดียว

## ⑪ เปิดใบให้สาย C

none

## ⑫ nonclaims

- **ไม่ได้อ้างว่า M2 เปลี่ยนพฤติกรรม** - `dispatch_columbus_quest3021`/`resolve_columbus_arrival` ทำงานเหมือนเดิม
  ทุกประการ (ยืนยันด้วยเทส wiring end-to-end ผ่านหมด) รอบนี้แตะแค่ path ที่ยังไม่มีใครไปถึงได้จริงวันนี้ (persisted
  `scene_id=17` row)
- **ไม่ได้อ้างว่าบั๊กนี้เคย exploit ได้จริง** - latent เท่านั้น เพราะไม่มีทางเขียน `scene_id=17` ลง DB ได้จริงวันนี้
  (`dispatch_columbus_quest3021` ไม่เคย persist อะไรเลย)
- **ไม่ได้แก้ docstring ล้าสมัยหรือ `docs/FUNCTIONAL_COVERAGE.json`** - พบทั้งสองจุด บันทึกไว้ในหัวข้อ ⑦ แทนการแก้
  เอง เพราะนอก scope ของรอบนี้
- **ไม่ได้ implement BUILD-002** - ยังบล็อกตามคำสั่ง COO เดิม (หัวข้อ ⑧)
- **ไม่ได้เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB**
- **ไม่ได้แตะ** `runtime.py` · `app.py` · `current/pf_login_game_server_v141.py`
- **ไม่ได้ commit/push เอง** - รอ chief/orchestrator เป็นคน commit ตามธรรมเนียมของสายนี้

— สาย A · WORLD
