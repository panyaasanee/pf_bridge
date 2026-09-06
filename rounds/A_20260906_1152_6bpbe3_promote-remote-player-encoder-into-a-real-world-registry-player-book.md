round 6bpbe3
start 2026-09-06T11:52+07:00
claim (not a takeover)

LANE-A · mailbox at round start: one letter addressed to LANE-A without a
`.CONSUMED.txt` sibling -- `20260906_1147_COO-DECISION-a1038-...-LANE-A.md`
(COO answering `1038`: no further action on GT-079/GT-080, "รอบหน้ากลับไปงานหลัก
M2 / remote_player_hypothesis.py promotion / RE-270"). Consumed this round, stub
attached to this commit. That letter's own instruction is source-of-truth #2
this round.

## 1. อะไรขยับ (NOW.md / M ข้อไหน)

**M2 ไม่ขยับ** และตรงกับที่ `NOW.md` บอกไว้แล้ว: ตัวบล็อกโค้ดคือ 0, `GT-233` ค้างที่
เครื่องเจ้าของ ไม่ใช่ของสายนี้ทำ · `RE-270` เป็นของ RE runner ขนานไป ไม่ใช่งานโค้ดของ
LANE-A รอบนี้

รอบนี้ขยับ `docs/PROMOTION_BACKLOG.md` แถวที่สองของ LANE-A แทน: `remote_player_hypothesis.py`
(REMOTE-PLAYER-ENCODER-001) ตามที่จดหมาย `1147` สั่งตรง ๆ ว่า "รอบหน้ากลับไปงานหลัก"

## 2. งานที่ทำ

### สิ่งที่พบก่อนเขียนโค้ด

`remote_player_hypothesis.py` (1723 บรรทัด) เป็น research probe ของตัวเอง (เขียนไว้เองใน
docstring): สามตัวตนสังเคราะห์ A/B/C รวม NEGATIVE_CONTROL ที่จงใจผิดคลาส เพื่อทดสอบ
สมมติฐานเรื่อง actor-factory dispatch บน actor_type 2 (CNetActor) การปลด `production_allowed`
ของไฟล์นี้ตรง ๆ เท่ากับส่ง probe ออกไปเป็นของจริง ซึ่งขัดกับกฎบ้าน (ห้ามส่ง probe lane)
⇒ "โปรโมต" รอบนี้แปลว่า: ดึงความรู้ที่ probe พิสูจน์แล้ว (มาสก์ BasicAttr 0x030D · ActorAttr
mask 0 + extra-group byte 1 · MovementAttr 0xFF) มาสร้างของจริงคนละไฟล์ ไม่แตะ probe เดิม

### โค้ดที่เพิ่ม (`pirate-force-server#919`)

- `world_scene_registry.py` -- ทะเบียนโลกที่ LANE-A ถือแชร์อยู่แล้ว (มอน/ศพ/ของพื้น) เพิ่ม
  เล่มที่สี่: `PlayerVital` (`note_player`/`forget_player`/`remembered_players`) เข้ากติกา
  shared-singleton เดียวกับสามเล่มเดิม (`PANYA-DECISION 20260905_1057`/`1140`)
- `world_remote_player_actor.py` (ใหม่ `production_allowed=True`) -- ประกอบ actor_type-2
  entry จริงของผู้เล่นคนอื่นทุกคนในทะเบียนของฉากนั้น (กรองตัวเองออก) ใช้ตัวเข้ารหัสที่
  freeze แล้วใน `population.py` ซ้ำ ไม่ยืมกลไก unlock/allowlist ของ probe เลย (มีเทสปัก
  ไว้ตรง ๆ)
- re-pin census ตัวสร้าง actor entry (`tools/pf_runtimeres_actor_entry_static.py` + เทส +
  รายงาน) สำหรับ 1 builder ใหม่ + 1 call site ใหม่

### pf-adversary -- สั่งหลังโค้ดพร้อม (agent ไม่มี Agent tool เรียกเอง) ผลคืนแล้ว ไม่ใช่ PENDING

พบ 2 ข้อ CONFIRMED แก้ในรอบเดียวกัน (commit `3012ce7`, `4adc2fa`, `4eaebb2`):
1. เพดานจำนวนฉาก (`scenes=N`) เช็คแยกทีละเล่ม (`len(self._players)` กับ `len(self._scenes)`
   คนละตัว) ⇒ กระบวนการจำฉากได้จริงถึง 2 เท่าของเพดานที่เอกสารอ้าง (ฉากที่มีแต่มอนกับฉาก
   ที่มีแต่ผู้เล่นนับแยกกัน) แก้ด้วย `_scene_count()` (union ของสองเล่ม) ใช้ทั้งสองประตูเขียน
   + `scenes()` เทสตามรอยสถานการณ์เดียวกับที่ adversary ใช้จับ 3 เทสใหม่
2. import ตาย 7 ตัวใน `world_remote_player_actor.py` (`BASIC_BIT_*` หก + `RUNTIME_PROTOCOL_RES_ID`)
   ไม่มีใครอ้างถึงหลังบรรทัด import เลย ⇒ ลบ
ข้อ 3 (ไม่บล็อก เพราะยังไม่มีใครเรียกโค้ดจริง): `note_player` ไม่มีประตูอัปเดตบางส่วนแบบ
`note_position`/`note_balance` ของเล่มมอน ⇒ จดไว้ใน `PLAYER_PRESENCE_WIRING` ให้คนต่อสาย
call site 2 อ่านให้ถูกก่อนเรียก

### สถานะจริง -- ไม่ใช่ SHIPPED

adversary ยืนยัน: ยังไม่มีใครเรียก `register_player_presence`/`compose_other_live_players_frame`
จากเส้นคำขอจริงเลย -- `runtime.py` เป็นของ chief ไม่แตะ ⇒ บนบูตปกติวันนี้โมดูลนี้เป็นโค้ด
จริง มีเทส ไม่มีแฟล็ก แต่ไม่มีผู้เรียก (ไม่ใช่ probe แต่ก็ยังไปไม่ถึงผู้เล่น) เขียน CORE-REQUEST
สามจุด (`runtime.py` START_GAME_REQ / `_vital_walk_promote_target_pos` / arrival path) ไว้ใน
body ของ `#919` ให้ chief แทนจดหมายแยก (LANE-A.md: "ต้องการเดินสาย เขียนบรรทัดเดียวใน PR body")

## 3. เทส/เกต

- ไฟล์ที่แตะ: `test_world_scene_registry.py` + `test_world_remote_player_actor.py` +
  `test_runtimeres_actor_entry_static.py` -- 93 passed, 19 skipped, 0 failed
- ชุดเต็มบนต้นไม้สุดท้าย (merge `origin/main` 154f0f1 เข้าแล้ว): `pytest tests -q` ->
  **12252 passed, 369 skipped, 0 failed**
- `tools/verify_hypothesis_ledger.py` PASS (entries=50) · `tools/verify_functional_coverage.py`
  PASS (domains=8) -- รันเพราะ merge เอา `docs/FUNCTIONAL_COVERAGE.json` มาด้วย ไม่มี drift
- `pf_gate_preflight.py --repo` PASS · `--pr-body ... --pr-stage final` PASS (marker บรรทัด
  เดียว ไม่มีที่อื่นพูดถึงโทเคน)

## 4. จดหมายรอบนี้

**บริโภค**: `20260906_1147_...-LANE-A.md` (ADDRESSEE: LANE-A) -- ตอบใบ `1038` ว่าไม่ต้องทำ
อะไรกับ GT-079/GT-080 อีก รอบหน้ากลับงานหลัก ⇒ ทำตามตรง ๆ stub แนบมาพร้อมรอบนี้
**เปิดใหม่**: ไม่มี -- CORE-REQUEST ไปที่ PR body ของ `#919` แทนจดหมายแยกตามกฎ LANE-A.md

## 5. ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่เห็นอะไรต่าง และไม่แต่งให้มี** -- ของที่พร้อมคือโค้ดจริงไม่มีแฟล็กที่ประกอบผู้เล่น
คนที่สองแบบ actor_type 2 จริง (ชื่อ+HP+ตำแหน่ง) จากทะเบียนโลกที่แชร์ข้ามเซสชันแล้ว รอ chief
ต่อสาย 3 จุดใน `runtime.py` เท่านั้น

## 6. รอบหน้าทำอะไร

1. ถ้า chief ต่อสาย `PLAYER_PRESENCE_WIRING` แล้ว: เปิดใบ GT "สองเซสชันในฉากเดียวกันเห็น
   ตัวละครของกันและกัน (ชื่อ+HP+ตำแหน่ง)" ทันทีในรอบเดียวกับที่ตรวจว่าต่อสายจริง (ไม่ใช่แค่
   ชื่อฟังก์ชันถูกเรียก)
2. ถ้ายังไม่ต่อสาย: กลับไปดู `docs/PROMOTION_BACKLOG.md` แถวถัดไปของ LANE-A
   (`move_authority_hypothesis.py` หรือ `logout_dialog_open_hypothesis.py`) หรือ
   `lane_a_choose_npc_scene1.py` ข้อ 6/7 ที่รอบ `6dvcer` ทิ้งไว้
3. ข้อ 3 ของ adversary รอบนี้ (ไม่มีประตูอัปเดตบางส่วนของ `note_player`) -- ถ้า call site 2
   ใกล้ต่อสายจริง ให้เพิ่ม `note_player_position` ก่อน ไม่ใช่หลัง

## 7. กำหนดเวลา

เริ่ม 11:52 · pf-builder subagent ทำโค้ด+เทสหลัก (ไม่มี Agent tool ของตัวเอง เรียก
pf-adversary ไม่ได้ตรงจึงสั่งจากรอบนี้เองทันทีที่โค้ดพร้อม) · adversary คืนผลก่อน push
(ไม่ใช่ PENDING) แก้ 2 ข้อ CONFIRMED ในรอบเดียวกัน · `origin/main` ขยับระหว่างรอบ
(`4e64b7d` -> `154f0f1`) merge เข้าแล้วรันชุดเต็มซ้ำเป็น commit สุดท้ายจริงก่อน push

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรต่างบนจอ -- โค้ดที่ประกอบผู้เล่นคนที่สองจริง (actor_type 2 ชื่อ+HP+ตำแหน่ง) จากทะเบียนโลกที่แชร์ข้ามเซสชันแล้วพร้อมทำงานทันทีไม่มีแฟล็ก รอ chief ต่อสาย runtime.py 3 จุด | pirate-force-server#919 (7 files, 12252/12252 tests pass on merged tree, pf-adversary 2 confirmed findings fixed in-PR) · pf_bridge round 6bpbe3 claim #1476
