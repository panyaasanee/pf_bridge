# FINDINGS R21 — เขียนกระเป๋าได้ครั้งเดียวจริง ๆ และ `dispatch` ไม่มีตาข่ายรับข้อยกเว้น

รอบที่ 21 · 2026-08-17 11:30–11:5x ICT · Chief Architect (Cowork scheduled task)
HEAD `eef51fa` · **ไม่บูต server ไม่เปิด socket ไม่เปิด GameClient ไม่แตะ UI ทั้งรอบ**
เขียนเฉพาะใน `pf_bridge\` · repo read-only 100%

---

## คำถามของรอบ

รอบ 20 ปิดท้ายด้วยรายการ probe แคบที่ทำได้โดยไม่ต้องขออำนาจใหม่ รอบนี้หยิบสองข้อแรก:

* **Q1** — 6 ตารางที่เหลือจากรอบ 19 มี code path เขียนไหม และ *เข้าถึงได้จากการเล่นปกติ* หรือไม่
  (ทำให้คำว่า "persistence" ระบุตารางได้ครบทั้ง 7 ตาราง ตามกฎที่รอบ 19 วางไว้)
* **Q2** — B3 ของรอบ 20: `save_position` raise `PermissionError` เมื่อ `rowcount != 1`
  แล้ว socket loop จับไว้ไหม

ทั้งสองข้อตอบได้ด้วยซอร์สที่ commit อยู่ + corpus ที่นอนบนดิสก์ ไม่ต้องส่งเฟรมใหม่แม้แต่เฟรมเดียว
(= ไม่แตะ **ข้อ 16** ที่ยังรอ Panya เคาะ)

---

## A — fact เกรด A (อ่านจากซอร์สที่ commit อยู่ / วัดจาก corpus จริง)

### A1 · แผนที่การเขียนครบทั้ง 7 ตาราง

| ตาราง | INSERT | UPDATE / DELETE | เข้าถึงได้บน boot มาตรฐาน |
|---|---|---|---|
| `accounts` | `store.py:128` `INSERT OR IGNORE` (ทุกครั้งที่ต่อ GAME) | **ไม่มีเลยทั้งโปรเจกต์** | ✅ แต่ **idempotent** — หลังแถวแรกเกิดแล้วไม่มีวันเปลี่ยนอีก |
| `schema_migrations` | `store.py:116` | `store.py:96` (checksum) | ⚙️ เฉพาะตอน migrate ตอนบูต |
| `sessions` | `store.py:144` | `136` / `152` / `157` / `206` | ✅ ทุก connection |
| `characters` | `store.py:181` (สร้างตัวละคร) | **ไม่มีเลย** — ไม่มี UPDATE ไม่มี DELETE ไม่มีการเขียน `deleted_at` ที่ไหนเลย | ✅ เฉพาะตอน **สร้าง** |
| `character_positions` | `store.py:184` (ตอนสร้าง) | `store.py:215` `save_position` | ✅ (รอบ 20 พิสูจน์แล้ว 435/435) |
| `character_backpacks` | `store.py:223` | `315` / `346` / `388` | ⚠️ ดู A2 |
| `character_backpack_items` | `store.py:228` | `297` / `306` / `337` / `374` | ⚠️ ดู A2 |

### A2 · บน boot มาตรฐาน มี mutator กระเป๋าเข้าถึงได้ **ตัวเดียว**

`tools\run_foundation_visible.ps1` ส่งแค่ `--db --capture-root --second-password-mode`
→ ทั้ง `item_move_capture_scenario` และ `item_move_hypothesis_scenario` เป็น `None`

```
runtime.py:478  if nested_id == ITEM_OPERATE_REQ_VITAL:
runtime.py:479      if item_move_capture_scenario is not None:      -> None ที่นี่
runtime.py:481      if item_move_hypothesis_scenario is not None:   -> None ที่นี่
runtime.py:483      candidate = parse_merge_candidate(...)
runtime.py:485      if candidate is not None: -> _dispatch_v111_persistent_merge
                    # candidate เป็น None -> ตกลงไปข้างล่าง ไม่ตอบ ไม่เขียน
```

* `move_backpack_item_to_free_slot` (M4 free-slot) ต้องมี `allow_hypothesized_item_move`
  ซึ่งเปิดจาก `--item-move-hypothesis-scenario` **เท่านั้น** ไม่งั้น `session.py:78` raise `PermissionError` ทันที
* `apply_v111_stack_merge` ต้องผ่าน `is_exact_merge_request` = **ไบต์ต้องเท่ากับ
  `V111_MERGE_REQUEST_PC` ทั้งดุ้น** (`inventory.py:277-287`)
* และ `store.py:294` บังคับ pre-state เป็น `INITIAL_BACKPACK` เป๊ะ
  → **เขียนได้ครั้งเดียวต่อชีวิตตัวละคร** ครั้งที่สองคืนค่า `None` = "replay" ไม่เขียน

### A3 · วัดกับเฟรมจริงของ client: **1 ใน 24**

เครื่องมือใหม่ `pf_bridge\replay\pf_itemoperate_audit.py` เดินทั้ง `GameClient\`
ใช้ `parse_outer` + `parse_item_operate_req` ของ server และ `parse_merge_candidate`
+ `is_exact_merge_request` ของ `inventory.py` **เป็น oracle**

```
files 630 · inbound 20,209        <- ตรงกับ corpus ของรอบ 20 เป๊ะ
ItemOperate-shaped : 24 · distinct pc : 12   <- ตรงกับตารางของรอบ 16 เป๊ะ
  EXACT_MERGE_WOULD_WRITE  : 1
  NOT_CANDIDATE_NO_WRITE   : 23   (22 ตกท่อเงียบ · 1 decode ไม่ได้)
writes บน boot มาตรฐาน (จำลอง pre-state one-shot) : 1
VERDICT: BACKPACK WRITES REACHABLE (exact V111 merge only)
```

รูปแบบ `(operation, value32, item_identity)` ที่ client ส่งจริง — ทุกตัว `operation=4`:

| fields | ครั้ง | | fields | ครั้ง |
|---|---|---|---|---|
| `(4, 2, 1)` | 4 | | `(4, 0, 3)` ← **ตัวที่เขียนได้** | 1 |
| `(4, 0, 1)` | 4 | | `(4, 8, 1)` | 1 |
| `(4, 2, 4)` | 3 | | `(4, 0, 2)` | 1 |
| `(4, 2, 2)` | 3 | | `(4, 1, 1)` | 1 |
| `(4, 9, 1)` | 2 | | `(4, 10, 1)` | 1 |
| `(4, 9, 2)` | 2 | | decode ไม่ได้ | 1 |

### A4 · gate จริงบน Windows `py -3` (job 044) ตรงกับ Linux ทุกตัวเลข

* audit ItemOperate: **630 / 20,209 / 24 / 12 / 1** เท่ากันเป๊ะทั้งสอง interpreter
* audit TargetPos ของรอบ 20 รันซ้ำ: **accepted 435 · rejected 0 · would-write 346** ไม่ขยับ
* เทสที่ครอบเส้นทางนี้ **46 ตัวเขียว exit 0**:
  `test_item_lifecycle` 8 · `test_item_move_capture` 8 · `test_item_move_hypothesis` 8
  · `test_delete_actor` 7 · `test_server_shutdown` 15

---

## N — ของใหม่ที่ไม่มีเอกสารไหนเคยบันทึก

### 🔴 N1 · `state.dispatch(parsed)` ไม่มี `except` ครอบ — และข้อยกเว้นจากมัน **ปิด server ทั้งตัว**

```
v141.py:7440   try:                     <- คู่กับ finally:7847 เท่านั้น ไม่มี except
v141.py:7558       actions = state.dispatch(parsed)
```

ข้อยกเว้นที่หลุดออกมาจะไหลออกจาก `game_listener` ไปถึง:

```
shutdown.py:267   except BaseException as error:
shutdown.py:268       controller.record_thread_failure(error)
shutdown.py:269       controller.request_stop("server thread failure")   <- ปิดทั้ง server
```

และภายใน `dispatch` **`_checkpoint_exact_target` เป็น DB write ทางเดียวที่ไม่มี `try/except` ครอบ**
(`runtime.py:290` เรียกจาก `315` และ `645`) — ต่างจากเลน `merge` (`164-174`) และเลน
`hypothesis` (`264-274`) ที่ดัก `Exception` แล้วตอบ "no reply" อย่างสุภาพทั้งคู่

> `store.py:216` → `raise PermissionError("stale or non-owning character session")`
> เมื่อ `rowcount != 1` = **เดินในเกมหนึ่งก้าวแล้ว server ดับทั้งตัว**

### 🟢 N2 · แต่ยังไม่มี trigger ที่เข้าถึงได้ในการเล่น client เดียว — และตัวที่กันไว้คือ "ข่าวร้าย" ของรอบ 18

เงื่อนไขเดียวที่ทำให้ `rowcount != 1` คือแถว `sessions` ของผู้เล่นถูกปิดหรือถูกแย่ง
ซึ่งเกิดจาก `open_session` เท่านั้น (`store.py:136` ปิด lease ทุกใบของ account เดียวกัน)
และ `open_session` ถูกเรียกเฉพาะตอน **รับ GAME connection ใหม่** (`FoundationSession.__init__`
→ `lifecycle.login`) — ซึ่ง **loop แบบ `accept()`+handle ในลูปเดียวของรอบ 18 กันไว้อยู่**

> ⭐ **ข้อจำกัดที่รอบ 18 รายงานว่าเป็นข่าวร้าย (server รับทีละตัว) กำลังทำหน้าที่เป็น
> interlock ที่กันบั๊กที่ร้ายแรงกว่าไม่ให้ยิงได้**
> → **มีผลตรงกับข้อ 14**: ถ้า Panya อนุมัติให้ทำ multi-client ต้องแก้ N1 (ดัก `PermissionError`)
> และนโยบาย lease ต่อ account **ก่อน** ไม่งั้นการปลดล็อกนี้จะเปิดทางให้ client ตัวที่สอง
> ทำให้ server ดับทั้งตัวตอนที่ client ตัวแรกขยับตัว

### 🔴 N3 · เส้นทาง "thread ตาย → ปิด server" **ไม่มีเทสครอบเลยสักตัว**

`git grep record_thread_failure -- src tests` เจอเฉพาะใน `src\...\shutdown.py` 3 บรรทัด
ไม่มีใน `tests\` เลย ทั้งที่ `test_server_shutdown` 15 ตัวเขียวหมด
(ส่วน `save_position` มีเทสระดับ store ครบ — `test_a_stale_lease_can_no_longer_write_a_position`)

### 🔴 N4 · ลบตัวละครไม่มีทางเปลี่ยน DB ได้

`delete_actor.py` เป็น **parser ล้วน** (docstring เขียนเองว่าไม่ dispatch ไม่ mutate)
และ `DELETE_ACTOR_VITAL` **ไม่ถูกอ้างถึงใน `runtime.py` หรือ dispatch ของ `v141.py` เลย**
บวกกับ A1 (ไม่มีคำสั่งเขียน `deleted_at` ที่ไหนในโปรเจกต์)
→ เทสใดที่คาดว่า "ลบตัวละครแล้วหายจาก DB" จะ FAIL เสมอ **และไม่ใช่บั๊ก**

---

## B — inference เกรด B (เหตุผลแน่น แต่ยังไม่ได้รันจริง)

* **B1** — GT-002 ตามที่เขียนในคิว (ลาก `identity1` slot2→slot10 ผ่าน UI) **จะไม่เขียน DB
  ถ้าบูตด้วยบรรทัดมาตรฐาน** ต้องบูตด้วย `--item-move-hypothesis-scenario` เท่านั้น
  → คิวต้องระบุ boot line ให้ชัด ไม่งั้นผลเทสจะตีความผิดแบบเดียวกับที่รอบ 19 เกือบพลาด
* **B2** — 23/24 เฟรมจริงที่ "ไม่ใช่ candidate" แปลว่า client ส่ง `ItemOperate` หลายชนิด
  ที่ server เงียบสนิทโดยตั้งใจ → ถ้า Panya ลากของในเกมแล้ว "ไม่มีอะไรเกิดขึ้น"
  นั่นคือพฤติกรรมที่ออกแบบไว้ ไม่ใช่อาการพัง
* **B3** — `accounts` ไม่มี UPDATE เลย แปลว่าไม่มีทางเปลี่ยนรหัส/ชื่อบัญชีผ่าน server ตัวนี้
  (สอดคล้องกับผลรอบ 19 ที่ตารางนี้ไม่ขยับ — เพราะแถวเดียวที่มีถูกสร้างไปนานแล้ว)

---

## ⚠️ nonclaims (สิ่งที่รอบนี้ **ไม่ได้** พิสูจน์)

1. ไม่ได้บูต server เลยทั้งรอบ — ทุกอย่างเป็นชั้นซอร์ส + corpus **ไม่ใช่การรันจริง**
2. ไม่ได้ส่ง `ItemOperateVitalReq` แม้แต่เฟรมเดียว (ข้อ 16 ยังรอ Panya)
3. ไม่ได้พิสูจน์ว่า **หน้าจอ client** แสดงอะไรตอนลากของแล้ว server เงียบ (ชั้น client-observable)
4. N1 พิสูจน์ว่า "ถ้า raise แล้ว server ดับ" **ไม่ได้พิสูจน์ว่ามันเคยเกิดขึ้นจริงสักครั้ง**
5. N2 เป็นการอ้างเรื่อง *ความเข้าถึงไม่ได้* — ยังไม่ได้ไล่ทุกเส้นทางที่อาจปิด session
   ระหว่างเล่น (เช่น เครื่องมือภายนอกที่แก้ DB ตรง ๆ ระหว่าง server ทำงานอยู่)
6. LOGIN listener: อ่านจาก `app.py` ว่า adapt เฉพาะ `game_listener` และ frozen login ไม่แตะ store
   — **ไม่ได้ยืนยันด้วยการรัน**
7. "one-shot per character" จำลองจาก pre-state ในโค้ด ไม่ได้เทียบกับ DB จริงหลายไฟล์
8. corpus 24 เฟรมเล็กมาก — ไม่ได้อ้างว่าครอบคลุมทุกการกระทำกับกระเป๋าที่ client ทำได้
9. ไม่ได้ตรวจ `character_backpacks.updated_at` ว่าขยับโดยไม่มีการเปลี่ยนไอเทมหรือไม่
10. ไม่ได้แตะ 6 ตารางในแง่ *runtime* — ยืนยันเฉพาะว่ามี/ไม่มีเส้นทางในโค้ด

---

## ข้อ 17 (ใหม่) — จะดัก `PermissionError` รอบ `dispatch` ไหม

| ทาง | ทำอะไร | ต้นทุน | ผลได้ | ความเสี่ยง |
|---|---|---|---|---|
| **ก** | ใส่ `try/except` รอบ `_checkpoint_exact_target` แบบเดียวกับเลน merge | ~10 บรรทัดใน `runtime.py` | เดินแล้วเซฟไม่ได้ ≠ server ดับ | แตะ `src/` = เข้าข่ายข้อ 14 |
| **ข** | ใส่ `except` ที่ frame loop ของ `v141.py` | แตะไฟล์ frozen | ครอบทุกเลน | ผิดหลัก "frozen V141" ที่ทั้งโปรเจกต์ยึด |
| **ค** | ไม่แก้อะไร แต่บันทึกเป็นเงื่อนไขบังคับของข้อ 14 | 0 | ไม่เพิ่มความเสี่ยงวันนี้ (N2) | ถ้าลืม จะระเบิดตอนทำ multi-client |
| **ง** | ไม่ทำและไม่บันทึก | 0 | — | — |

**chief เอนไปทาง ค** — เพราะ N2 บอกว่าวันนี้ยังยิงไม่ได้ และการแก้ `src/` โดยไม่มีคำตัดสิน
ผิดกติกาเดิมอยู่แล้ว แต่ **ต้องผูกไว้กับข้อ 14 ให้แน่น** ว่าเป็น *เงื่อนไขก่อน* ไม่ใช่งานตามหลัง

---

## เครื่องมือที่เพิ่มในรอบนี้ (อยู่ใน `pf_bridge\` ไม่ได้ commit เข้า repo)

* `pf_bridge\replay\pf_itemoperate_audit.py` — audit corpus แบบ offline สำหรับกระเป๋า
  รับ dir หรือไฟล์ · `--per-file` · `--json` · stdlib ล้วน ไม่เปิด socket ไม่แตะ DB
  ใช้ `inventory.py` เป็น oracle ได้สะอาดเพราะโมดูลนั้นไม่มี relative import
* `pf_bridge\inbox\044_r21_backpack_path_gate.ps1` (→ `done\`) — gate บน Windows `py -3`
  ไม่บูต server เลย ใช้เวลา **7 วินาที**
