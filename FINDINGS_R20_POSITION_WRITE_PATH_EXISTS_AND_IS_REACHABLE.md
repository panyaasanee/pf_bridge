# FINDINGS R20 — เส้นทางเขียนตำแหน่งมีอยู่จริง active และเฟรมของ client จริงผ่านมันได้ 100%

รอบ: idle round ครั้งที่ 20 · 2026-08-17 11:11–11:2x ICT
ผู้เขียน: Claude (Cowork, scheduled task `pirate-force-chief-continue`)
ขอบเขต: **ไม่เปิด GameClient ไม่แตะ UI ไม่บูต server ไม่เปิด socket** — static analysis
+ offline corpus audit + รัน unit test ที่มีอยู่แล้วในรีโป
repo: **read-only 100%** (เขียนเฉพาะใน `pf_bridge\`)

---

## 0. คำถามของรอบ และทำไมถึงถามตอนนี้

รอบ 19 วัด `persistence` เป็นครั้งแรกใน 19 รอบ แล้วพบว่า **6 ใน 7 ตารางไม่เคยถูกเขียนเลย**
โดยเฉพาะ `character_positions` และเขียน nonclaim ที่ถูกต้องกำกับไว้เองว่า:

> replay หยุดที่ `TeleportVital` และ **ไม่เคยส่ง `TargetPosVital`** ดังนั้นข้อสรุปที่ถูกคือ
> *"เส้นทางเข้าเกมอย่างเดียวไม่เขียนตำแหน่ง"* ไม่ใช่ *"ตำแหน่งไม่เคยถูกบันทึก"*

รอบ 19 เสนอ **ข้อ 16** = ขออนุญาตส่ง `TargetPosVital` เพื่อปิดคำถามนี้ แล้วหยุดรอคำตัดสิน
เพราะการส่ง vital ชนิดที่ไม่เคยส่ง = แตะพื้นผิวใหม่ของโปรโตคอล

**รอบนี้ปิดคำถามเดียวกันโดยไม่ส่งเฟรมใหม่แม้แต่เฟรมเดียว** — ด้วยการถามว่า
*"ถ้าเฟรม `TargetPosVital` ของ **client จริง** ที่นอนอยู่ใน capture มาถึง server จริง
server จะเขียน DB หรือไม่"* แล้วตอบด้วย **parser ของ server เอง** เป็น oracle

---

## 1. FACTS (เกรด A)

### A1 — เส้นทางเขียนตำแหน่งมีอยู่ครบ และ **active ในโหมดที่ Panya จะเทสจริง**

โซ่การเรียกเต็ม ตรวจจากซอร์สที่ commit อยู่:

```
v141.py:7455-7457   pc = snappy_raw_decompress(comp) ; parsed = parse_outer(pc)
runtime.py:487      durable_target = legacy.parse_v141_refresh_target_pos(parsed)
runtime.py:638-645  if scene_load_scenario is None
                       and durable_target is not None
                       and self.foundation.selected is not None:
                           self._checkpoint_exact_target(durable_target)
runtime.py:290-299  candidate = Position(sel.scene_id, sel.scene_seq, x, y, z, heading)
                    if candidate != selected.position:
                        self.foundation.checkpoint(candidate)
session.py:91-95    self.lifecycle.checkpoint(self.session_id, self.selected, position)
lifecycle.py:59-60  self.store.save_position(session_id, character.id, position)
store.py:209-217    UPDATE character_positions SET scene_id,scene_seq,x,y,z,heading,updated_at
                    WHERE character_id=? AND EXISTS (SELECT 1 FROM sessions
                          WHERE id=? AND selected_character_id=? AND closed_at IS NULL)
```

**ไม่มีเงื่อนไข `runtime_ack_sent` / `teleport_sent` บนเส้นนี้** (ต่างจากเลนอื่นในไฟล์เดียวกัน)

### A2 — เงื่อนไขแรก `scene_load_scenario is None` **เป็นจริงเสมอ** ในทุก boot ที่ใช้จริง

`tools/run_foundation_visible.ps1:22-27` ส่งให้ `pirateforce_foundation.app` แค่สามตัว:

```
--db <path>   --capture-root <path>   --second-password-mode <mode>
```

**ไม่มี `--scene-load-scenario` ไม่มี `--population-scenario`** → `app.py:54-60` ให้ทั้งคู่เป็น `None`
→ ไม่เข้าเลน `_dispatch_object_population_target` (runtime.py:494) และไม่ใช้
`ReadOnlyFoundationSession` (ตัวที่ `raise PermissionError("scene-load milestone cannot checkpoint")`)
สคริปต์นี้คือตัวที่ PLAYBOOK และ job 040/041/042 ทุกตัวใช้บูต

### A3 — เฟรม `TargetPosVital` ของ client จริง **ผ่าน parser ครบ 435 จาก 435 = 100%**

เครื่องมือใหม่ `pf_bridge\replay\pf_targetpos_audit.py` เดินทั้ง `GameClient\`
630 capture log · **20,209 inbound frames** (ตรงกับตัวเลขของรอบ 16 เป๊ะ)

| รายการ | ค่า |
|---|---|
| เฟรมที่ `nested_id == TARGET_POS_VITAL` | **435** |
| **ผ่าน `parse_v141_refresh_target_pos`** | **435** |
| ถูกปฏิเสธ | **0** |
| ค่า `(x,y,z,heading)` ที่ไม่ซ้ำ | 312 |
| `moving` flag | `1` → 205 ครั้ง · `0` → 230 ครั้ง |

เฟรมทั้งหมดมาจาก **58 capture log ของ client จริง** (`GAME_20260815_*`, `GAME_20260816_*`)
— **ไม่มีเฟรมจาก replay ของเราเองปนเลย** (job รอบ 16–19 เขียน capture ลง `outbox\capture_r*`
และไม่เคยส่ง `TargetPosVital`) → ไม่มี circularity

### A4 — จำลองเงื่อนไข `candidate != selected.position` แล้ว: **จะเรียก `save_position()` 346 ครั้ง**

เดินตามลำดับ wire ในแต่ละ capture พร้อมติดตามตำแหน่งที่ server ถืออยู่:

| | |
|---|---|
| **จะเรียก `save_position()` (= UPDATE จริง)** | **346** |
| ข้ามเพราะตำแหน่งซ้ำกับค่าก่อนหน้า | 89 |

→ **VERDICT: WRITES REACHABLE**

### A5 — cross-check ที่ยืนยันว่า parser ครอบทุกไบต์ที่แปรผันจริง (หลักฐานที่แข็งที่สุดของรอบ)

| นับแบบ | ค่า |
|---|---|
| ไบต์ `pc` ทั้งเฟรมที่ไม่ซ้ำ | **315** ← ตรงกับที่ **รอบ 16** รายงานไว้เป๊ะ |
| `(x, y, z, heading, moving)` ที่ไม่ซ้ำ | **315** |
| `(x, y, z, heading)` ที่ไม่ซ้ำ | 312 |

**315 = 315** แปลว่า **ไม่มีไบต์ใดใน payload ของ `TargetPosVital` ที่แปรผันโดยที่ parser
มองไม่เห็น** — ฟิลด์ทั้งห้าที่ decode ได้ อธิบายความหลากหลายของไบต์ได้ครบถ้วน
(และส่วนต่าง 3 คือคู่ที่ตำแหน่งเดียวกันแต่ `moving` ต่างกัน)

### A6 — เส้นทางนี้มี unit test ครอบอยู่แล้ว และ **เขียวจริงวันนี้บน Windows `py -3`** (job 043)

`tests/test_foundation.py:124 test_real_v141_dispatch_lifecycle` สร้าง state **โดยไม่ใส่ scenario ใด ๆ**
(= โหมดเดียวกับ A2) แล้ว dispatch จริงตามลำดับ login → create → start → **TargetPos frame**
แล้ว assert ว่า `store.get_character(c.id).position == Position(1,0,-10001.25,-700.5,671.0,1.25)`
· และ assert เชิงลบต่อท้ายว่า `vital_count=2` **ไม่เขียน**

| test module | ผล |
|---|---|
| `test_real_v141_dispatch_lifecycle` | **OK** exit 0 |
| `test_exit_restart_load_position` | **OK** exit 0 |
| `test_new_session_revokes_stale_position_writer` | **OK** exit 0 |
| `test_position_rejects_nonfinite` | **OK** exit 0 |
| `tests.test_foundation` (13) | **OK** exit 0 |
| `tests.test_connection_lifecycle` (12) | **OK** exit 0 |
| `tests.test_session_row_persistence` (13) | **OK** exit 0 |
| `tests.test_startup_stale_lease_recovery` (15) | **OK** exit 0 |

รวม **53 tests เขียว** บน Windows `py -3` ที่ HEAD `eef51fa` + WIP ปัจจุบัน

### A7 — ตำแหน่งกลับมาหลัง restart จริง และถูกฉีดเข้าเฟรม `start_game`

`test_exit_restart_load_position` เปิด `SQLiteStore` **ตัวใหม่บนไฟล์เดิม** แล้ว
`select_and_start` → `c2.position == saved` **และ** `assertIn(f32tag(saved.x), pc)`
→ ไม่ใช่แค่ค่ากลับมาใน DB แต่ **เดินทางออกไปถึงไบต์ที่ส่งให้ client**

### A8 — audit ให้ผลเดียวกันทั้งสองแพลตฟอร์ม

Linux `python3` (sandbox) และ Windows `py -3` (job 043) ได้
`435 / 435 / 0 / 346 / WRITES REACHABLE` **เท่ากันทุกตัว**

---

## 2. NEGATIVES (เกรด A)

### N1 — การปิด connection **ไม่เขียนตำแหน่ง** และนี่คือคำอธิบายที่สมบูรณ์ของผลรอบ 19

`runtime.py:118,125-126` → `session.py:109 close_connection()` ซึ่ง docstring เขียนไว้เองว่า
*"Close this exact lease **without rewriting its last position**"*

`session.py:97 close(position)` ที่เขียนตำแหน่งตอนออก **ไม่ถูกเรียกจาก server เลย** — มีแต่ใน test
→ **ตำแหน่งถูกบันทึกระหว่างเล่นเป็นราย `TargetPos` เท่านั้น ไม่ใช่ตอนออก**
→ ดังนั้น "เข้าเกมแล้วออกโดยไม่เดิน" **ต้อง** ไม่เขียน `character_positions` — ซึ่งคือสิ่งที่รอบ 19 วัดได้พอดี
**ผลรอบ 19 ไม่ใช่อาการของบั๊ก แต่เป็นพฤติกรรมที่ออกแบบไว้ และตอนนี้อธิบายได้ทุกบรรทัด**

### N2 — parser รับเฉพาะรูป **singleton** เท่านั้น

`vital_count != 1` · `outer_mask != 0x02` · `nested_version != 0` · มีไบต์เหลือ ·
`derived_mask != 0` · ค่า non-finite → คืน `None` ทุกกรณี
แต่ **ในทางปฏิบัติไม่มีเฟรมของ client จริงสักเฟรมที่ตกเงื่อนไขเหล่านี้** (A3: reject = 0)
→ ความเข้มงวดนี้ **ไม่ใช่กำแพงสำหรับการเล่นปกติ**

---

## 3. INFERENCES

- **B1 (เกรด B)** — `GT-005` (เดินแล้วตำแหน่งอยู่ข้าม restart) **ผ่านได้ในชั้น wire/DB**
  ทั้งสี่ชิ้นส่วนพร้อม: code path (A1) · โหมด default ถูกต้อง (A2) · เฟรมจริงผ่าน parser (A3–A4)
  · เขียนแล้วโหลดกลับได้ (A7)
  ข้อจำกัด: ยังไม่มีการรัน end-to-end จริงบน server ที่บูตอยู่ **นี่คือสิ่งเดียวที่ยังขาด**
- **B2 (เกรด C)** — ถ้า `GT-005` FAIL จริงตอน Panya รัน สาเหตุที่เหลือน่าจะไม่ใช่ "ไม่มีฟีเจอร์"
  แต่เป็นชั้น client (client ไม่ส่ง `TargetPos` เพราะเดินไม่ได้/ไม่มีพื้น/UI ไม่ตอบ)
  หรือชั้น session (`EXISTS` guard ใน `store.py:215` ไม่ผ่านเพราะ lease ถูกแทนที่)
- **B3 (เกรด C)** — `_checkpoint_exact_target` **ไม่มี try/except** และ `save_position`
  `raise PermissionError` เมื่อ `rowcount != 1` → ถ้า lease ถูกแย่งระหว่างเล่น
  exception จะวิ่งขึ้นไปถึง dispatch loop **ยังไม่ได้ตรวจว่า socket loop จับมันไว้หรือไม่**
  (ไม่ตรวจในรอบนี้เพราะต้องบูต server = คนละคำถาม)

---

## 4. NONCLAIMS — สิ่งที่รอบนี้ **ไม่ได้** พิสูจน์

1. **ไม่ได้พิสูจน์ว่า server ที่รันอยู่จริงเขียน `character_positions` สำเร็จ** — ทั้งรอบไม่บูต server
   สิ่งที่พิสูจน์คือ *ทุกเงื่อนไขบนเส้นทางเป็นจริง* ไม่ใช่ *การรันจริงหนึ่งครั้งที่สำเร็จ*
2. ไม่ได้พิสูจน์ว่า **client จริงจะส่ง `TargetPos` เมื่อ Panya กดเดิน** — พิสูจน์แค่ว่า
   **เคยส่งมาแล้ว 435 ครั้ง** ในเซสชันของวันที่ 15–16 ส.ค.
3. ไม่ได้ตรวจว่า `scene_id`/`scene_seq` ที่ถูกบันทึกถูกต้องตามฉากที่ client อยู่จริง —
   `candidate` **ยืม `scene_id`/`scene_seq` เดิมจาก `selected.position`** แล้วเปลี่ยนแค่ x/y/z/heading
4. ไม่ได้ตรวจพฤติกรรมเมื่อ `EXISTS` guard ไม่ผ่าน (B3)
5. ไม่ได้ตรวจ 6 ตารางที่เหลือของรอบ 19 — รอบนี้แตะเฉพาะ `character_positions`
   (`character_backpacks*`, `characters`, `accounts`, `schema_migrations` ยังไม่มีคำตอบ)
6. ตัวเลข 346 คือ **ขอบบนของ capture ชุดนี้** ไม่ใช่คำทำนายว่าเซสชันใหม่จะเขียนกี่ครั้ง
7. การจำลองใน A4 เริ่มด้วยตำแหน่ง "ไม่ทราบ" → เฟรมแรกนับเป็น write เสมอ
   (เลือกทางที่อนุรักษ์นิยมสำหรับคำถาม *"เขียนได้ไหม"* แต่ทำให้ 346 สูงกว่าจริงได้สูงสุด 58 ครั้ง)
8. `pf_targetpos_audit.py` อ่าน block `DECOMPRESSED` ที่ **server เขียนเอง** — ถ้า block นั้น
   ไม่ตรงกับไบต์ที่รับจริง ผลจะพลอยผิดตาม (รอบ 16 ตรวจ roundtrip 20,209/20,209 ผ่านแล้ว)
9. เทสที่รันในรอบนี้เป็น **unit test** — เป็นหลักฐานของโค้ด ไม่ใช่ของ runtime จริง
   (กฎสองชั้นของรอบ 17: ห้ามอ้างชั้น wire/DB เป็นหลักฐานของชั้น client-observable)
10. ไม่ได้พิสูจน์ว่า **หน้าจอเกมจะแสดงตัวละครที่ตำแหน่งเดิม** หลัง restart — นั่นคือชั้น
    client-observable ที่ต้องมี Panya เสมอ

---

## 5. ผลต่อ **ข้อ 16** ที่รอบ 19 ตั้งไว้

รอบ 19 เสนอ: *"อนุญาตให้ chief ส่ง `TargetPosVital` ชั้น wire หลัง `runtime_ack` แล้ววัด
`character_positions` ~10 นาที"* โดยให้เหตุผลว่า **ถ้าไม่ทำ Panya จะแยกไม่ออกว่า
"ฟีเจอร์พัง" หรือ "เทสผิดขั้นตอน"**

**เหตุผลข้อนั้นอ่อนลงมากแล้ว** เพราะรอบนี้ตอบคำถาม *"ฟีเจอร์มีไหม"* ได้โดยไม่ต้องส่งอะไรเลย:
มีจริง · active ในโหมดที่จะใช้ · เฟรมจริงผ่าน 100% · มีเทสครอบและเขียว

| ทาง | เนื้อหา | ต้นทุน | ผลได้ |
|---|---|---|---|
| **ก** | อนุญาตส่ง `TargetPosVital` ชั้น wire (ข้อ 16 เดิม) | ~10 นาที + แตะพื้นผิวใหม่ | ได้ integration จริง ปิด nonclaim #1 |
| **ข** | **ไม่ต้องอนุญาต** — ถือว่ารอบนี้พอสำหรับตัดสินใจ แล้วให้ Panya รัน GT-005 ตรง ๆ | 0 | เร็วที่สุด แต่ nonclaim #1 ยังเปิด |
| **ค** | อนุญาตแบบแคบ: ส่งได้เฉพาะเฟรมที่ **ยกมาจาก capture ทั้งดุ้น** ไม่สังเคราะห์ใหม่ | ~10 นาที | ได้ integration โดยไม่สร้างไบต์ที่ client ไม่เคยส่ง |
| **ง** | รอ | 0 | — |

**chief เอนไปทาง ค** — ได้คำตอบ end-to-end เท่าทาง ก แต่ไม่มีการสังเคราะห์ไบต์ใหม่เลย
(เฟรมทั้ง 435 มีอยู่ในดิสก์แล้ว และ A5 พิสูจน์ว่าเรารู้ครบทุกไบต์ที่แปรผันในนั้น)
ถ้า Panya ไม่ตอบ chief จะ **ไม่ทำ** ทั้ง ก และ ค ตามกติกาเดิม

---

## 6. สิ่งที่ทำในรอบนี้

1. **`pf_bridge\replay\pf_targetpos_audit.py`** (ใหม่) — audit corpus แบบ offline
   ใช้ `parse_outer` + `parse_v141_refresh_target_pos` **ของ server เอง** เป็น oracle
   พร้อมตัวไล่เหตุผลการปฏิเสธทีละ clause · stdlib ล้วน · ไม่เปิด socket ไม่แตะ DB
2. **job 043** — รัน 53 unit test บน Windows `py -3` + รัน audit ซ้ำบน Windows + ตรวจ repo/DB
3. **ไฟล์นี้**
4. อัปเดต `GAME_TEST_QUEUE.md` — evidence ใต้ `GT-005` + ขั้นตอนที่แม่นขึ้น (ไม่เปลี่ยนสถานะ)

## 7. สิ่งที่ตั้งใจ **ไม่** ทำ

- **ไม่ส่ง `TargetPosVital`** (ข้อ 16 ยังรอ Panya) · **ไม่บูต server เลยทั้งรอบ**
- ไม่เขียน harness เต็มตัว (ข้อ 12) · ไม่แก้ `src/` (ข้อ 14) · ไม่ commit เครื่องมือเข้า repo
- ไม่เปิด GameClient ไม่แตะ UI (ขอบเขตที่ผู้ใช้สั่ง 2026-08-17)
- ไม่เปลี่ยนสถานะรายการใดในคิว · ไม่ enable task ผู้เทส · ไม่แก้ cron ตัวเอง

## 8. ยืนยันหลังทำงาน (job 043 บน Windows)

HEAD `eef51fa983dd6d2573fd8021eb0d21177069fa55` เท่าเดิม ·
dirty **6 ไฟล์ 187+/21− ครบรายไฟล์** · staged **0** · untracked **0** ·
`diff --check` exit **0** · **ไม่มี `index.lock`** ·
canonical DB **69,632B · mtime `2026-08-17 04:23:18.5714411` ·
sha `673F4BFB1C35EC390D6ED3B0C1FE3F581B20C6895ACE9183C86A5971BCCC9708` ไม่ขยับ** ·
**ไม่มี `-wal`/`-shm`** · ไม่บูต server จึงไม่มีสำเนา DB ให้ park ·
console worktree ไม่ได้แตะ (**23 รอบติด**)
