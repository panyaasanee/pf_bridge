R337, LANE-E session `9vec2s`
start: 2026-09-04T12:23+07:00

# ขยับ NOW ข้อไหน

`NOW.md` "งานด่วนตอนนี้" ข้อ `1151` สั่งตรงถึง chief: PR เดียวรอบ 12:51 สองจุดอ่าน (GM-054 +
หนี้ `0216`) + บรรทัด `GT-224`. ทำครบตามนั้น และต่อ CORE-REQUEST ของ LANE-B/LANE-A ที่ค้างอยู่
ตามลำดับ §17 ข้อ 3 (ต่อสาย A/B/GM ก่อนงานอื่น) ในรอบเดียวกัน — ไม่ขยับบันไดไมล์สโตน M2-M6 เอง
(ไม่มีของใหม่ให้ M2 เกาะ 2/3 หรือ M3-M4 ในรอบนี้ นอกจากสิ่งที่ระบุไว้ข้างล่างว่ากระทบ GT-224/M4)

# ล็อกรอบ

`git fetch` แล้ว list ทั้งสอง repo: ไม่มี `[LANE-E]` open PR อื่น → claim ทันที (`pf_bridge#1130`)
list ซ้ำ: ไม่มีคู่แข่งอายุมากกว่า → ผ่าน. ตรวจชะตา R335: server `#722` merged=true, pf_bridge
`#1095` (claim `2vfbtf`) closed unmerged 11:42 โดย Panya แต่งานจริง (`d1bd2005`) landed บน main
ผ่านทางอื่นแล้ว (ยืนยันด้วย `git merge-base --is-ancestor`) — ตรงกับที่ NOW.md `1151` ข้อ 2 บันทึกไว้
ไม่มีอะไรต้องกู้.

🔴 **แก้ผิดพลาดของตัวเองกลางรอบ**: ครั้งแรกสร้าง claim บนกิ่งชื่อเอง (`claude/e-round-9vec2s`)
ผิดกฎ — harness กำหนด branch `claude/cool-johnson-9vec2s` ไว้แล้ว ย้าย commit ไปกิ่งที่ถูกก่อนเปิด PR
กิ่งผิดถูกทิ้งไว้เฉย ๆ (ไม่มี PR เปิดค้าง ไม่ต้องเก็บกวาด)

# ทำอะไรไปบ้าง (pirate-force-server, 8 ไฟล์เนื้อหา + 5 ไฟล์เทส)

## 1. GM-054 — `lane_hooks.current_session_scene_id(character_id)`

สัญญาตาม `COO-DECISION 20260904_1151`: อ่าน `session.client_confirmed_scene` เมื่อ
`scene_label_is_server_guess` เป็นเท็จ · ไม่รู้/เป็น guess = raise `NoConfirmedScene`
(ห้าม `foundation.selected.position.scene_id` เด็ดขาด — field นั้นถูก `_gm_warp_resync_selected_scene`
เขียนทับเป็นปลายทาง warp ก่อนไคลเอนต์ยืนยัน)

ปัญหาที่ต้องแก้เพิ่มจากที่ใบขอ: ฟังก์ชันรับ `character_id` แต่ scene fields เป็น per-session
(in-memory) ไม่ใช่ per-DB — ไม่มี character_id→session registry อยู่ก่อน ⇒ สร้างใหม่:
`lane_hooks._LIVE_SESSION_BY_CHARACTER` (`weakref.WeakValueDictionary`) + `register_live_session
(character_id, session)` เรียกจาก `runtime.py`'s `START_GAME_REQ` handler ทันทีหลัง
`select_and_start` สำเร็จ. Weak ref เพื่อให้ connection ปิด = ตอบ "ไม่รู้" อัตโนมัติ ไม่ใช่ค่าค้าง

🔴 **pf-adversary รอบแรกจับได้จริง**: จุดลงทะเบียนอยู่ก่อนบรรทัด `start_game_reply_sent = True`
ราว 880 บรรทัด และมีทางที่ `select_and_start` สำเร็จแต่ถูกปฏิเสธลึกกว่านั้น (`SceneEntryRefused`)
โดยไม่ latch reply — ไคลเอนต์ retry คนละตัวละครบน **connection เดิม** ได้ ⇒ ตัวละครเก่าจะค้างชี้ไปที่
session เดียวกับตัวละครใหม่ ตอบฉากผิดตัว. แก้: `register_live_session` evict ตัวเอง
(compare-and-delete: ลบ entry เก่าเฉพาะถ้ายังชี้ไปที่ session ตัวเองจริง กัน race กับ session อื่นที่
เพิ่งได้ตัวละครนั้นไปครองจริง) + เทสสองใบใหม่ปักพฤติกรรมทั้งสองทิศ

## 2. หนี้ `COO-DECISION 20260904_0216` — `lane_hooks.current_login_attr_bytes`

pf-static-re วัดจริง (ไม่เดา): `attr_wire.unnamed_field_x()` (28 แถว) ตัดกับ
`login_mask.login_field_x()` (สิ่งที่ login ประกอบจริงวันนี้) ได้ **แค่ 2 แถว**: x=7 (speed, จาก
`login_speed.resolve_for_character`) กับ x=10 (`scene_seq`, จาก `store.get_character(cid).position
.scene_seq`) — อีก 26 แถวไม่มี login-time source เลยจริง ๆ (โครงสร้าง ไม่ใช่ช่องว่างการค้นหา)
สร้างโมดูลใหม่ `live_login_attr_bytes.py` มิเรอร์ `live_named_attr_values.py` เป๊ะ (source-registration
pattern เดียวกัน, never-raises, ประกาศ console เมื่อไม่มี source) + จุดอ่าน `current_login_attr_bytes`
ใน `lane_hooks` + ผูกใน `app.py` (จุดเดียวกับ named-attr source, ตรวจด้วย AST test แบบเดียวกัน)

ผลลัพธ์: `attr_wire.live_login_bytes` เปลี่ยนจาก refuse 28 แถวเหลือ refuse 26 แถว — **ไม่ได้ปลด
(b'') ให้ส่งได้** (ยังขาดอีก 26) แต่เป็นความคืบหน้าจริงแบบเดียวกับจุดอ่าน named-values เดิม
`tests/test_gm_attr_wire.py`'s canary (`..._still_has_no_login_read_point`) พลิกเป็นบวกตามแบบที่
`current_named_attr_values` เคยทำมาก่อน

## 3. CORE-REQUEST LANE-B `20260904_1134` — `actor_identities` เข้า announced membership

`lane_hooks.SceneCensusResult.actor_identities` มีอยู่แล้ว (`COO-DECISION 20260903_2247`) และ
`lane_a_scene_census.compose` ก็ใส่ค่าอยู่แล้ว — ช่องโหว่คือ `runtime.py`'s lane-census commit
(บรรทัดที่เคย comment ว่า "JUDGMENT CALL... lane_hooks is not in this round's scope") ทิ้งมันแล้ว
ส่ง `()` ตรง ๆ ให้ `mob_combat_membership.build_membership`. แก้เป็นอ่าน `composed.actor_identities`
(coerce เป็น `int` ในเน็ตเดียวกับฟิลด์อื่น) แล้วส่งจริง

**วัดสด (ไม่ใช่แค่แก้แล้วเดา)**: รันฉาก 14 ผ่าน dispatcher จริงก่อน/หลังแก้ — ก่อนแก้ได้
`mob_combat_target_not_announced_no_reply`, หลังแก้ **ไม่มี** event นั้นเลย (ไม่มี mob_combat_
event ใดเลย เพราะแพ็กเก็ตที่ใช้ทดสอบเป็น action code 0 "wield" ไม่ใช่ strike — ผ่านรั้ว announced
แล้วไม่มีอะไรให้รายงานต่อ ไม่ใช่ผลลบ) ⇒ `tests/test_mob_combat_bg0015_gates.py` สองใบพัง
(`test_a_real_swing_in_scene_14_now_answers_not_announced`,
`test_bg0015_registration_is_now_real_not_simulated`) — **ตามที่คอมเมนต์ของมันเองบอกไว้ว่าจะพัง**
เขียนใหม่ตามพฤติกรรมจริง ไม่ลบ (ชื่อ+docstring ระบุว่าอัปเดตรอบไหน เหตุผลอะไร)

แก้ comment เท็จที่ `runtime.py` (บรรทัดใกล้กัน) ที่ยังเขียนว่า "`mob_scene_recompose` has no
composer for a lane scene yet" — เท็จตั้งแต่ `#727` (ฉาก 5 มี `COMPOSER_BG0005` แล้ว ฉาก 14 มีมา
ตั้งแต่ `n4pv7k`) ตามที่ LANE-B ขอ (ใบเดียวกัน หัวข้อเล็กกว่า)

**Nonclaim ตามใบเดิม**: ไม่อ้างว่าฉาก 5/14 ตีได้จริงแล้ว — RE-157 cadence gate/AI register/aggro
ไม่ถูกแตะรอบนี้ นี่แค่ปิดช่องที่ทำให้ roster สมบูรณ์แค่ไหนก็ยังตีไม่ได้เพราะ membership ว่างเสมอ

## 4. CORE-REQUEST LANE-A `20260903_1641` ข้อ 1 — สองแถวความยาวคลิก

`vital_walk.body_length_table` เพิ่ม `_click_body_lengths(legacy)` (lazy import
`world_click_vitals.body_lengths` — lazy เพราะ `world_click_vitals` import `vital_walk` กลับอยู่
แล้ว, วงกลมถ้า import ตรง ๆ) เมิร์จเข้า table เดียวกับ pickup id. ผล: เฟรมที่มี `TargetVital`/
`ChooseNPC` เดินได้ทั้งเฟรมแล้ว (ก่อนหน้านี้ id ที่ไม่มีความยาวประกาศหยุดทั้งเฟรม ไม่ใช่แค่ vital นั้น
⇒ ตำแหน่งที่แนบมากับคลิกหายไปด้วย — รูปเดียวกับ R303) วัดผ่าน dispatcher จริง:
`VITAL_WALK_PROMOTED` ขึ้น ตำแหน่งขยับตามเฟรม ไม่ใช่ค้างที่เดิม

`tests/test_world_click_vitals.py` สามใบใน `DispatchTodayTests` พังตามที่คอมเมนต์บอกไว้ว่าจะพัง
(เขียนดักไว้ล่วงหน้าโดย LANE-A) แก้เป็นเกณฑ์ใหม่ + `NothingCallsThisYetTests` เพิ่มข้อยกเว้นแคบ
(เฉพาะ `body_lengths` ชื่อเดียว มีเทสใหม่ปักไว้ว่าห้ามกว้างกว่านี้) เพราะ `vital_walk.py` เป็นผู้เรียก
ที่ผ่านรีวิวแล้วหนึ่งราย ไม่ใช่การเปิดทางกว้าง — ข้อ 2 ของใบเดิม (`runtime.py`'s click gate อ่าน
`nested_id` ตัวแรกอย่างเดียว) **ไม่ได้ทำ** ตามที่ใบระบุไว้ว่า "ทางเลือก ไม่บังคับรอบเดียวกัน"

## 5. GT-224 — บรรทัดตาม `COO 1047` ข้อ 4

เพิ่มสองบรรทัด 🔴🆕 ในหัวใบ (`GAME_TEST_QUEUE.md`): (ก) หลัง `/warp` ต้องรีล็อกอินก่อนเข้าตี
ตามที่สั่ง (ข) เพิ่มเอง — เกณฑ์เดิม "ฉาก 3/4/5/14/278 ต้องได้ `mobs=0`" อาจไม่ตรงแล้วสำหรับฉาก 5/14
เพราะตอนนี้มีตารางมอนจริง (`#727`, และฉาก 14 มีมาก่อนแล้ว) — ไม่ได้แก้เกณฑ์เอง (ไม่มีเครื่องวัด
`mobs=` สดในมือ) แค่เตือนผู้เทสให้เช็ก `field_mobs._SCENE_TABLE_MODULES` ก่อนตัดสิน

## GM-053 — เลื่อน มีเหตุผล

จุดประกอบ login block (`legacy_bridge.py`'s `LegacyProjector.start_game`) เป็น **singleton ต่อ
โปรเซส** ไม่ใช่ต่อคอนเนกชัน (คอมเมนต์ของมันเองเตือนเรื่องนี้ไว้แล้วสำหรับ speed) — ใบขอให้บันทึก
mask ลง session แต่จุดที่ระบุไม่มี session ให้อ้าง ต้องแก้ signature ของ `start_game()` หรือย้ายจุด
บันทึกไปที่ `session.py`'s `select_and_start` ซึ่งกระทบจุดเรียก 4 จุดใน `runtime.py` ทั้งคู่ — ไม่ใช่
"ห้าบรรทัด" แบบใบขอบอก ต้องมีรอบแยกวัดผลกระทบให้ครบ เขียนตอบ LANE-GM แล้ว
(`notes_to_chief/20260904_1307_CHIEF-TO-LANE-GM-*.md`) ตั้งเลขรอบถัดไปให้ตัวเอง

## CORE-REQUEST อื่นที่ยังไม่แตะ (LANE-DB `0542`, LANE-CS `1041`, LANE-UI `1120`)

ไม่อยู่ในลำดับบังคับก่อน (§17 ข้อ 3 ระบุ A/B/GM) รอบนี้เต็มแล้วจากสี่ใบข้างบน — ยกไปรอบหน้า
ไม่ใช่ปฏิเสธ

# pf-adversary

สองรอบแยก ทั้งคู่ผลคืนและแก้ครบ**ก่อน** push จริง (ไม่ต้องติด ADVERSARY_PENDING ในที่สุด แม้จะ
สั่งไว้ตามกฎ `0903_2345` เผื่อผลมาไม่ทัน):
- **รอบ 1** (GM-054 + session registry): พบ defect จริงหนึ่งข้อ — `register_live_session` ไม่มี
  eviction เมื่อ connection เดิมถูกปฏิเสธกลางทางแล้ว retry ด้วยตัวละครอื่น จะตอบฉากผิดตัวละคร
  แก้ด้วย compare-and-delete eviction ก่อน commit แรก
- **รอบ 2** (actor_identities + login-bytes + click-vitals): สองข้อ
  (ก) eviction ของรอบ 1 เองไม่ thread-safe — โปรเจกต์รันหนึ่งเทรดต่อคอนเนกชันจริง การ
      check-then-delete สองขั้นตอนแยกกันมีช่องให้ thread อื่นแทรกได้ (จำลองสำเร็จ: thread ที่ลง
      ทะเบียนตัวละครใหม่ถูก thread เก่าลบทิ้งเพราะเช็กค้างไว้ก่อนหน้า) แก้ด้วย `_LIVE_SESSION_LOCK`
      ครอบทั้งลำดับ + เทสพิสูจน์ mutual exclusion จริง (ไม่ใช่แค่จำลอง interleaving เฉพาะเจาะจง)
  (ข) เทส AST guard ของ `vital_walk.py`'s exemption จับได้แค่รูป `from .X import Y` — พิสูจน์ได้ว่า
      รูป `from . import X as _x; _x.attr` หลบผ่านได้เงียบ ๆ แก้เป็นตัวช่วยใหม่
      `_click_vitals_names_referenced` ที่ตามรอย whole-module import + attribute access +
      ธง sentinel สำหรับ opaque import — ยืนยันแล้วว่า mutation เดิมที่หลบผ่านได้ ตอนนี้แดง
ทั้งสองผลลง commit ที่สองก่อน push จริง — push #1 (ยัง"ไม่ผ่าน adversary รอบ 2") ไม่เคยเกิดขึ้น
จริง (คอมมิตทั้งสองถูก push พร้อมกันหลังผลรอบ 2 คืน)

# ชุดเต็ม (commit สุดท้าย, merge main แล้ว)

`git fetch origin main` แล้ว merge เข้ากิ่งก่อนรัน (main ขยับระหว่างรอบ: `#729`/`#730` เข้ามา,
auto-merge สะอาด ไม่มี conflict) — `pytest tests -q -rs` (48 modules excluded ตรงพิน) =
**8828 passed, 4 skipped** (skip เดิมทั้งสี่ ไม่มีใหม่) · `skip_census` = **PASS** (excluded=48) ·
`tools/verify_hypothesis_ledger.py` = **PASS entries=50** · `test_tree_is_cp874_safe.py` ผ่าน
🔴 หมายเหตุ: นี่คือ **cloud sanity** ไม่ใช่ gate เต็มบนสะพาน — ไม่มี `py -3`/Windows/มือทดสอบจริง

# สถานะ WIRED

WIRED = จำนวนโมดูลเลนที่ import จริง / production_allowed lanes — ไม่เปลี่ยนจากรอบก่อน (ไม่มีโมดูล
lane_hooks ใหม่ที่ registrer ตัวเองรอบนี้ — งานรอบนี้ทั้งหมดอยู่ในไฟล์ของ chief เอง
`lane_hooks/__init__.py`, `runtime.py`, `app.py`, `vital_walk.py`, `legacy_bridge.py` ไม่ใช่โมดูล
`lane_<x>_*.py` ใหม่)

# สถานะ push

push แล้ว รอ merge `pirate-force-server#734` — pf-adversary ทั้งสองรอบผ่านและแก้ครบก่อน push
(ไม่มี ADVERSARY_PENDING ค้าง) · เกตยังไม่ตัดสิน ณ ตอนเขียนบรรทัดนี้ ห้ามเขียนว่า "อยู่บน main"
จนกว่ารอบถัดไปเห็น merged=true (หัวข้อ 2 ข้อ 7)

-- chief รอบ `9vec2s`
