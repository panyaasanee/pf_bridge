# DB round (`6ra2qv`) — 2026-09-03T15:05+07:00 to 15:26+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260903_1436_n32ch0_the-damage-door-gets-its-own-short-budget.md`
(รอบก่อนทำ `COO 1248` ข้อ 1-3 คอมมิตเดียว จงใจไม่แตะข้อ 4)

**บรรทัดเดียวของรอบนี้: `COO 1444` อนุมัติข้อ 1-3 + ระบุเงื่อนไขเริ่มข้อ 4 (`#653` ต้องเป็นบรรพบุรุษของ
`origin/main` บนโคลนที่ unshallow แล้ว) — วัดแล้วเป็น YES ⇒ ทำข้อ 4: pragma ที่ถูกปฏิเสธนับและพิมพ์บรรทัด
แทนบรรทัด `pass` เดิม ทั้งสองประตู คอมมิตเดียว, `pf-adversary` เจอคอมเมนต์อ้างเกินจริงหนึ่งจุด แก้แยกคอมมิต**

## NOW.md — รอบนี้ขยับข้อไหน

อ่าน `NOW.md` เป็นไฟล์แรกก่อนแตะอะไร (ฉบับ "ตรวจล่าสุด 2026-09-03 14:45 +07:00 โดย COO")
หัวข้อ "งานด่วนตอนนี้" ยังไม่ว่าง (P-0/P-1/P-2/P-3 บนสุด) ไม่มีข้อไหนอยู่ในเขตของ LANE-DB โดยตรงรอบนี้
เช่นเดียวกับรอบก่อน — งานของรอบนี้มาจากใบของ COO (`1444`) ที่ตอบใบรายงานของ LANE-DB เอง ไม่ใช่จาก NOW.md
โดยตรง

- **ไม่ขยับบรรทัดใดของ NOW.md โดยตรง** (ไฟล์นั้นเป็นของ Panya/COO เท่านั้น) — สิ่งที่ COO/chief อาจอยาก
  ขยับ: บรรทัด 47 ("ข้อที่ห้าของ DB ... คิวถัดของ DB = เสียบ seam") อ้างถึงงานที่ปิดไปแล้วหลายรอบก่อน
  ไม่เกี่ยวกับข้อ 4 นี้โดยตรง — ไม่มีคำใน NOW.md ฉบับที่อ่านพูดถึงข้อ 4 ตรง ๆ เลย (มันมาจากจดหมายเท่านั้น)
- **M4 ไม่ขยับ** เหมือนทุกรอบก่อนหน้า — `apply_hp_damage` ยังผู้เรียกศูนย์ ไม่มีอะไรเปลี่ยนที่จุดเรียก
  รอบนี้แตะเฉพาะภายในสองเมธอดที่มีอยู่แล้ว
- **P-0 · P-1 · P-2 · P-3 · GM-A · UI-A · UI-B** นอกเขตของสายนี้ ไม่แตะแม้ไฟล์เดียว
- 🔴 ไม่ปลดล็อกใดของ `/speed` ไม่แตะ `gm/` `speed_wire.py` `runtime.py` `app.py` `v141`
- 🔴 ไม่สร้าง `migrations/` ใหม่ และไม่แตะไฟล์ `.db` จริงแม้ไบต์เดียว (ไม่มี canonical DB บนคลาวด์)

## 1. ล็อกรอบ

- 15:05 list PR สถานะ open ทั้งสองรีโป หัวข้อขึ้นต้น `[LANE-DB]`
  - `pf_bridge`: ไม่มีใบเปิดเลย (มีของสายอื่นสี่ใบ: LANE-GM `#975`, LANE-A `#976`, LANE-B `#977`,
    LANE-E `#979` — ไม่ใช่ล็อกของผม ไม่แตะ)
  - `pirate-force-server`: ไม่มีใบเปิดเลย
  ⇒ ไม่มี `[LANE-DB]` open ทั้งสองรีโป ⇒ ล็อกว่าง ไม่ใช่ takeover
- ตัดกิ่งจาก `origin/main` ของ `pf_bridge` commit `rounds/DB_20260903_1505_6ra2qv_claim.md`
  push แล้วเปิด `#980 [LANE-DB] round 6ra2qv: claim` ไม่มี `PF-AUTOMERGE: v4` ใน body ตอนเปิด
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open มีใบเดียวคือ `#980` ของผมเอง (สายอื่นมี LANE-GM `#981` เพิ่มมา
  ระหว่างนั้น ไม่ใช่ของผม) ⇒ ไม่แพ้ ทำงานต่อ
- ก่อน push โค้ดฝั่งเซิร์ฟเวอร์: list ซ้ำอีกครั้ง (15:23) — `[LANE-DB]` open ยังมีแค่ `#980` ของผมเอง

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` แล้วหักใบที่มี `.CONSUMED.txt` คู่ ⇒ ค้างหนึ่งใบ:

| ใบ | ทำอะไรรอบนี้ |
|---|---|
| `20260903_1444_COO-DECISION-...-item-4-starts-only-after-653-is-an-ancestor-of-main.md` | งานหลักของรอบ (§3) |

สร้าง `.CONSUMED.txt` แล้ว · เขียนตอบหนึ่งใบถึง COO (`1526`)

## 3. ทำอะไร

### 3.1 วัดเงื่อนไขก่อนเริ่ม (`COO 1444` ข้อ 3)

โคลนนี้เป็น shallow ตอนต้นรอบ (`git rev-parse --is-shallow-repository` → `true`) — `git fetch
--unshallow origin` ก่อน แล้ว `git merge-base --is-ancestor 56ae1f55628807dcf578c1b6624f162add647071
origin/main` (SHA หัวกิ่งของ `#653` จาก GitHub API) → `YES` — ตอนนั้น `origin/main` คือ merge commit ของ
`#653` เอง (`a769503f`) ⇒ เริ่มข้อ 4 ได้

### 3.2 `COO 1248` ข้อ 4 — pragma ที่ถูกปฏิเสธนับและพิมพ์ (pirate-force-server, คอมมิตแรก)

`src/pirateforce_foundation/store.py`, สองจุดคอมมิตเดียว:
- ประตูฮีล (`_begin_immediate_under_contention`, บรรทัดเดิม ~1705-1710): `except sqlite3.Error: pass`
  → `_note_pragma_busy_timeout_refused("heal", ceiling)`
- ประตูดาเมจ (`_begin_immediate_for_damage`, บรรทัดเดิม ~1778-1788): เหมือนกัน →
  `_note_pragma_busy_timeout_refused("damage", DAMAGE_LOCK_BUSY_TIMEOUT_MS)` — ลบคอมเมนต์เดิมที่บอกว่า
  "ยังไม่แตะ เป็นคิวรอบถัดไป" ทิ้ง (ไม่จริงอีกต่อไป)
- ฟังก์ชันร่วมใหม่ `_note_pragma_busy_timeout_refused(door, requested_ms)` + ค่าคงที่
  `PRAGMA_BUSY_TIMEOUT_REFUSED_TOKEN = "PRAGMA_BUSY_TIMEOUT_REFUSED"` +
  `PRAGMA_BUSY_TIMEOUT_REFUSED_COUNT = 0` (module-level, process lifetime, ไม่ล็อกเธรด)
- **ไม่เปลี่ยน control flow ของทั้งสองจุด**: หลัง pragma ถูกปฏิเสธ ทั้งสองยังเดินต่อไปลอง
  `BEGIN IMMEDIATE` เหมือนเดิมทุกประการ — เพิ่มแค่การนับ+พิมพ์ก่อนตกลงไปที่ `try` ถัดไป

### 3.3 เทส (พ่วงคอมมิตแรก)

- `tests/test_persistence_vitals_heal.py`: ขยายเทสเดิม
  `test_a_pragma_a_connection_refuses_does_not_stop_the_heal` (เดิมวัดแค่ `begins == 1`) ให้วัดเพิ่ม:
  ตัวนับขึ้นพอดีหนึ่ง + stdout มี token/`door=heal`/`requested_ms=`
- `tests/test_persistence_vitals.py`: เทสใหม่
  `test_a_pragma_a_connection_refuses_does_not_stop_a_hit_and_is_counted` (คลาส
  `DamageDoorHasItsOwnShortBudgetTests`) — fake connection เล็ก ๆ ในเทสเอง วัดสามอย่างเดียวกันฝั่งดาเมจ

### 3.4 คอมมิตที่สอง — แก้คอมเมนต์อ้างเกินจริงที่ `pf-adversary` เจอ

ดู §5

## 4. หลักฐาน — สองชั้นแยกกัน

### 4.1 client-observable

🔴 **ศูนย์ รอบนี้ไม่มีหลักฐานชั้นนี้เลย** ไม่มีเฟรมถูกประกอบ ไม่มีอะไรถูกส่ง ไม่มีผู้เล่นเห็นอะไรต่างจาก
เมื่อวาน และไม่มีอะไรในรอบนี้เคยรันบน canonical DB ของเจ้าของ

### 4.2 wire-DB

**ก. เทสที่แตะ/เกี่ยวข้องโดยตรง** — `test_persistence_vitals.py` + `_heal` +
`test_login_vitals_revive_under_contention.py` + `test_persistence_login_vitals.py`:
`276 passed, 205 subtests passed` (วัดเองก่อนส่งตรวจ และ `pf-adversary` วัดซ้ำอิสระในเวิร์กทรีแยก
ได้ตัวเลขเดียวกัน)

**ข. มิวแทนต์ (โดย `pf-adversary` ในเวิร์กทรีแยก) — ห้าตัว จับได้ครบ**

| มิวแทนต์ | จับได้โดย |
|---|---|
| คืน `_note_pragma_busy_timeout_refused("heal", ceiling)` กลับเป็น `pass` | เทสฮีลปฏิเสธ (ตัวนับไม่ขึ้น) |
| คืนฝั่งดาเมจกลับเป็น `pass` เหมือนกัน | เทสดาเมจปฏิเสธเช่นกัน |
| ตัด token ออกจากรูปแบบบรรทัดพิมพ์ | ทั้งสองเทสปฏิเสธ (`assertIn(...TOKEN, printed)`) |
| สลับชื่อประตู (ฮีลพิมพ์ `door=damage`) | เทสฮีลปฏิเสธ (`assertIn("door=heal", printed)`) |
| มิวแทนต์ control-flow: `except: ...; continue` แทนที่จะตกลงไปที่ `try` ถัดไป | ลูปวนไม่รู้จบกับ
  fake connection ที่ปฏิเสธเสมอ (ต้อง `kill -9`) — จับได้โดย "ไม่จบ" ไม่ใช่ "แดง" — `pf-adversary`
  บันทึกว่าเป็นความเสี่ยงที่มีอยู่แล้วในรูปเดิมของ `while True` ไม่ใช่รอบนี้สร้างขึ้น และไม่มี
  pytest-timeout ในรีโป — รายงานไว้เป็นข้อสังเกตให้เจ้าของ CI ไม่ใช่งานของรอบนี้ |

**ค. ไม่มีอะไรของสายอื่นถูกแตะ** — diff มีสามฮังก์ (`store.py`: บรรทัดคงที่/ฟังก์ชันใหม่, ประตูฮีล,
ประตูดาเมจ) ไม่มีฮังก์ใดทับช่วงบรรทัดของ `connect`/`_apply_hp_transition`/`apply_hp_heal`/
`restore_hp_to_full` (ตรวจโดย `pf-adversary`)

**ง. ไม่มีชื่อชนกัน** — `grep -rln PRAGMA_BUSY_TIMEOUT_REFUSED` ทั่วรีโปเจอแค่ `store.py` +
สองไฟล์เทสใหม่ (`pf-adversary` วัด)

**จ. `apply_hp_damage` ยังผู้เรียกศูนย์** — ไม่มีจุดเรียกเปลี่ยน รอบนี้แตะแค่ภายในสองเมธอดที่มีอยู่แล้ว

## 5. ตรวจ pf-adversary — หนึ่งจุดจริง แก้แล้ว

ส่ง subagent ตรวจก่อนคอมมิตสุดท้าย (isolated worktree, ไม่แตะ live checkout) — วัดไฟล์ที่เกี่ยวข้องซ้ำ
อิสระ (276 passed, 205 subtests ตรงกัน) + ลองมิวแทนต์ห้าตัวเอง (ดู §4.2) — เจอจุดจริงหนึ่งจุด: คอมเมนต์
กำกับ `PRAGMA_BUSY_TIMEOUT_REFUSED_COUNT` ในร่างแรกอ้างว่า "เหมือนตัวนับ census ที่รีโปนี้มีอยู่แล้ว" —
`pf-adversary` grep `census counter` ทั่ว `src/` ไม่เจอตัวนับรูปนี้ที่ไหนอีก (มีแค่โมดูล
`identity_registry_census.py` ของสาย GM ซึ่งชื่อคล้ายกันแต่คนละเรื่อง) — คำอ้างไม่มีอะไรรองรับจริง แก้แล้ว
คอมมิตที่สอง เขียนคอมเมนต์ใหม่ตรงตามที่ตรวจได้จริง (ไม่ล็อกเธรด เพราะยังไม่เคยเห็นการปฏิเสธ pragma จริง
นอกเทสที่จงใจบังคับ ถ้าจะล็อกให้วัดของจริงก่อนตามกฎบ้านเดียวกับที่ `DAMAGE_LOCK_BUSY_TIMEOUT_MS` ใช้)

ไม่พบข้อบกพร่องอื่นที่บล็อกรอบนี้ ข้อสังเกตเดียวที่ไม่ใช่ข้อบกพร่องของรอบนี้: ลูปวนไม่รู้จบของ
`_begin_immediate_under_contention` เมื่อเจอ pragma ที่ปฏิเสธทุกครั้ง (มีมาก่อนรอบนี้ ไม่ใช่รอบนี้สร้าง)
— บันทึกไว้ใน §4.2 ไม่ใช่งานของ LANE-DB จะแก้เองนอกใบสั่ง

## 6. nonclaims

1. **M4 ไม่ขยับ** `apply_hp_damage` ยังผู้เรียกศูนย์ทั้งรีโป ไม่มีอะไรเปลี่ยนที่จุดเรียก
2. **ไม่มีอะไร client-observable** ในรอบนี้ ไม่มีเฟรม ไม่มีการส่ง
3. **ไม่เคยรันบน canonical DB ของเจ้าของ** ดาต้าเบสทุกตัวสร้างใน `TemporaryDirectory`
4. **`PRAGMA_BUSY_TIMEOUT_REFUSED_COUNT` ไม่ล็อกเธรด** — จงใจ ยังไม่เคยมีการปฏิเสธ pragma จริงนอกเทส
   ที่บังคับด้วยมือ การล็อกสำหรับสภาพที่ไม่เคยวัดจะเป็นการเปลี่ยนที่ไม่มีอะไรรองรับ (เหตุผลเดียวกับที่
   `DAMAGE_LOCK_BUSY_TIMEOUT_MS` เป็นเพดานไม่ใช่ผลวัด)
5. **ลูปวนไม่รู้จบของประตูฮีลเมื่อ pragma ปฏิเสธทุกครั้งเป็นความเสี่ยงที่มีอยู่แล้ว** ไม่ใช่รอบนี้สร้าง
   ไม่แก้เองนอกใบสั่ง (§5)
6. **ไม่ประกาศไมล์สโตนใด** และไม่แตะ `GAME_TEST_QUEUE.md`

## 7. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- ระหว่างทำงานรันเฉพาะสองไฟล์ที่แตะก่อน (`test_persistence_vitals.py`, `test_persistence_vitals_heal.py`)
  แล้วขยายเป็นสี่ไฟล์ที่เกี่ยวข้อง (พ่วง `_login_vitals` + `test_login_vitals_revive_under_contention.py`)
- ก่อน push: `git fetch origin main` (pirate-force-server) เจอ `#654` merge ใหม่ระหว่างรอบ (สาย GM,
  ไฟล์ `gm/name_color_gate.py`/`gm/say_wire.py` ไม่ทับกับไฟล์ของรอบนี้) → `git merge origin/main` เข้ากิ่ง
  ก่อน ไม่มี conflict
- **ชุดเต็มรันครั้งเดียวบนต้นไม้ที่ merge `origin/main` แล้วนั้น จริงๆ** (หลัง commit ที่สองแก้คอมเมนต์
  ของ pf-adversary แล้ว): `python -m pytest tests/ -q -rs` → `8773 passed, 323 skipped, 17360 subtests
  passed in 462.81s (0:07:42)` · `tools/pf_pytest_precondition_census.py --report <log>` →
  `RESULT: PASS` ทุก skip ยังถูกประกาศ ตั้งชื่อ และปักครบ
- 🔴 **ไม่มีไฟล์เทสใหม่และไม่ขยับตัวเลข skip แม้ตัวเดียว** (แก้ไฟล์เทสเดิมสองไฟล์เท่านั้น ไม่มีไฟล์ใหม่)
  ⇒ ไม่ต้องซ้อม `pytest_subset`/`skip_census` แยกในสภาพไม่มี `pf_bridge`
- **PR เซิร์ฟเวอร์ `#655` เปิดแล้ว มี `PF-AUTOMERGE: v4` — รอ gate Windows ยังไม่ขึ้น `main`
  ณ เวลาที่ push ใบนี้**
- claim PR `#980` ของ `pf_bridge`: เติม marker ตอนจบรอบ (หลังไฟล์รอบนี้ push แล้ว) ตามหัวข้อล็อกรอบ

## 8. รอบหน้าทำอะไร

`COO 1248`/`0951` ท้ายใบ: `COO 0951` — ของที่เก็บเข้ากระเป๋าแล้วต้องอยู่ครบหลังล็อกเอาต์–ล็อกอิน
(ขอบเขต: วัดว่าแถวที่ pickup เขียนไว้ถูกอ่านกลับตอนล็อกอินหรือไม่ ห้ามแตะ `runtime.py` ถ้าเส้นทางอ่าน
ไม่โหลดกระเป๋า = เขียนจดหมายรายงาน ห้ามแก้เอง)
