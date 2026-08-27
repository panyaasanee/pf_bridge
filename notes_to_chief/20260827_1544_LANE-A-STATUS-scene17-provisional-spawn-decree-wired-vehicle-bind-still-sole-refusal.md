[ถึง: chief cloud · COO · cc Panya, RE runner | จาก: สาย A (WORLD) | 2026-08-27T15:44+07:00]
[ตอบ: `20260827_1445_PANYA-DECISION-scene17-provisional-arrival-xyz-0-0-0-owner-decree-ka1-B.md`]

# LANE-A STATUS - scene 17 provisional spawn decree wired (dispatch still refuses, one reason not two)

## สรุปสั้น

จดหมาย 14:45 ของเจ้าของ (พิกัดชั่วคราวฉาก 17 = (0,0,0), ป้าย `PROVISIONAL-OWNER-DECREE-20260827-1445`) ยังไม่
มีใครต่อสายเข้าโค้ดจริง (รอบ `kqrlhr`, 3 นาทีหลัง decree, consume ผล RE 6 ใบแต่ไม่ได้ต่อสายค่านี้) รอบนี้ต่อสาย
ให้จริง: `scenarios/world_scene_registry_001.json`'s ฉาก 17 มี `spawn` แล้ว (ไม่ใช่ `null` อีกต่อไป)
`columbus_quest_dispatch.resolve_columbus_arrival()` ไม่ raise `SceneEntryRefused` สำหรับฉาก 17 อีกต่อไป และ
พิมพ์ token คอนโซลตามที่จดหมายข้อ 2 สั่ง `dispatch_columbus_quest3021()` **ยัง refuse ทุกครั้งเหมือนเดิม**
(never-partially-applies ตามเดิม) แต่ตอนนี้เหตุผลเดียว (`no_re096_vehicle_row_evidence`) ไม่ใช่สองเหตุผล
รายละเอียดเต็มอยู่ใน `rounds/A_20260827_1544_scene17_provisional_spawn_decree_wired.md`

## ปัญหาจริงที่พบระหว่างต่อสาย (คุ้มค่าที่จะรู้ก่อนใช้ค่านี้ที่อื่น)

`world_scene_travel._spawn()` เช็คทุก spawn ที่ pin ไว้ว่าต้องอยู่ในขอบเขต `ground` ของฉากนั้น ฉาก 17 มี
`ground.z_min=746.04, z_max=1272.74` (วัดจริงจาก `Bg1001.placements.tsv`) - เขียน `spawn.z=0.0` ตรงๆ ตามคำสั่ง
เจ้าของจะทำให้ **ทั้ง `world_scene_registry_001.json` โหลดไม่ขึ้นเลย** (`load_scene_registry()` parse ทุก
destination รวดเดียว รวมฉาก 1/บ้าน) เพราะ cross-check เดิมไม่รู้จักข้อยกเว้นแบบ "เจ้าของสั่งเอง" แก้โดยเพิ่ม
ฟิลด์เสริม `spawn.ground_bound_waiver` (ข้อความอ้างอิงได้) ที่ทำให้ cross-check ข้ามเฉพาะแถวที่มีฟิลด์นี้ -
ทุกฉากอื่นยังถูกเช็คเหมือนเดิม 100% (มีเทสยืนยันทั้งสองทาง) นี่คือ landmine จริงที่ถ้าใครก๊อปพิกัด (0,0,0) ไปแปะ
ตรงๆ โดยไม่ผ่านฟิลด์นี้จะพังทั้งไฟล์ ไม่ใช่แค่ฉาก 17

## ของที่แตะใน `pirate-force-server` (6 ไฟล์ ไม่แตะ `runtime.py`/`app.py`/`current/`)

| ไฟล์ | อะไร |
|---|---|
| `scenarios/world_scene_registry_001.json` | ฉาก 17 `spawn` จาก `null` เป็น `{0,0,0}` + `ground_bound_waiver` อ้างอิงจดหมาย 1445 ตรงๆ |
| `src/pirateforce_foundation/world_scene_travel.py` | เพิ่มฟิลด์เสริม `ground_bound_waiver` ใน spawn schema, ข้าม ground cross-check เฉพาะแถวที่มีฟิลด์นี้ |
| `src/pirateforce_foundation/columbus_quest_dispatch.py` | `resolve_columbus_arrival()` ไม่ raise สำหรับฉาก 17 อีกต่อไป + พิมพ์ token คอนโซลตามจดหมาย 1445 ข้อ 2 |
| `tests/test_world_scene_travel.py` | +4 เทสใหม่ (waiver ผ่าน/ไม่ผ่าน/ว่างเปล่า/ฉากอื่นไม่ติด) + แก้ 1 เทสเดิม |
| `tests/test_columbus_quest_dispatch.py` | แก้ 2 เทส + เพิ่ม 2 เทสใหม่ |
| `tests/test_columbus_quest_dispatch_wiring.py` | แก้ 1 เทส end-to-end ผ่าน `runtime.make_state_class` จริง ยืนยันไม่ต้องแตะ `runtime.py` เลย |

## ตัวเลขที่วัดได้

- เทสกลุ่มเป้าหมาย (12 ไฟล์): **429/429 ผ่าน**
- เทสทั้งเรโป: **3543 เทส, error 18 ตัว (capstone ModuleNotFoundError เดิม, ไม่เกี่ยวกับรอบนี้), 0 FAIL**
- cp874-encodability: ทุกไฟล์ที่แตะใน `src/`/`tests/`/`scenarios/` ผ่านหมด
- ยืนยันสด (headless): console/events มีบรรทัด `WORLD_SCENE scene_id=17 ...`,
  `SCENE_ENTRY scene=17 xyz=0,0,0 source=PROVISIONAL-OWNER-DECREE-20260827-1445`,
  `columbus_quest3021_dispatch_refused_no_re096_vehicle_row_evidence` (1 ตัว ไม่ใช่ 2 เหมือนก่อนรอบนี้)

## ยังไม่ได้พิสูจน์ / รอมนุษย์

- ผู้เล่นยังไม่เห็นอะไรเปลี่ยนบนจอเกม - Columbus ยัง refuse ทุกครั้งจนกว่า `RE-096` จะปิดจริง หรือเจ้าของเคาะ
  คำถามที่ค้างอยู่ (จดหมาย 1510 ข้อ 4: M2 รับเข้าฉาก 17 แบบยังไม่เป็นเรือได้ไหม) **สาย A ไม่แตะคำถามนั้นเลย
  ไม่เปิดใบซ้ำ** dispatch ยัง atomic เหมือนเดิมทุกประการ
- พิกัด (0,0,0) ยังไม่พิสูจน์ว่าไคลเอนต์จะวางผู้เล่นบนผิวน้ำ/ในขอบแมพ (nonclaim จดหมาย 1445 ข้อ 4 คำต่อคำ)
- `RE-103` หัวใบใน `CLIENT_RE_QUEUE.md` ยังไม่ถูกปิด (ของ chief cloud รอบ `4txjyg`) - ธงเดิมยังยืน สาย A ไม่แตะ

## CORE-REQUEST

none

## เปิดใบให้สาย C

none

— สาย A · WORLD

---

## ADDENDUM 2026-08-27T~16:xx+07:00 - pf-adversary pass ภายนอก พบช่องว่างจริง 1 จุด แก้แล้ว

ผู้ใช้รัน pf-adversary จากภายนอกก่อน merge พบ **medium-severity 1 จุดจริง**: `resolve_columbus_arrival()` เรียก
`world_scene_entry.resolve_entry()` ซึ่งเป็นสายเดียวกับที่ `runtime.py`'s login path เรียกจริง (ด้วย `scene_id`
ที่ persist ไว้ในแถวตัวละคร) ก่อนรอบนี้ `resolve_entry()` refuse ฉาก 17 เสมอเพราะไม่มี spawn - login รวมอยู่ด้วย
พอรอบนี้เติม spawn `(0,0,0)` ให้ฉาก 17 การ refuse นั้นหายไปแบบไม่ตั้งใจ - **ถ้า** แถวตัวละครใน DB เคยมี
`scene_id=17` (ไม่มี CHECK constraint ห้าม, `migrations/001_initial.sql:5`) login ครั้งถัดไปจะสำเร็จและวาง
ผู้เล่นไว้กลางทะเลที่ `(0,0,0)` โดยข้าม vehicle-bind atomicity ของ `dispatch_columbus_quest3021` ไปเลย
(ปัจจุบัน latent - ยังไม่มีอะไรเขียน `scene_id=17` ลง DB จริง เพราะ dispatch ไม่เคยสำเร็จ)

**แก้แล้ว**: เพิ่ม `login_entry_allowed: false` บนฉาก 17 ใน registry (default `true` ทุกฉากอื่น ไม่เปลี่ยน
พฤติกรรม) และพารามิเตอร์ `via_login: bool = True` ใน `resolve_entry()` - default `True` คุ้มครอง login path
ของ `runtime.py` โดยไม่ต้องแตะไฟล์นั้นเลย (call site เดิมไม่ส่ง keyword ใหม่ = ได้ fail-closed อัตโนมัติ)
`resolve_columbus_arrival()` ส่ง `via_login=False` explicit เพราะไม่ได้อ่านแถว persist จริง เพิ่มเทส regression
8 ตัวใน `tests/test_world_scene_entry.py` (`LoginEntryRestrictionTests`) ที่พิสูจน์ตรง ๆ ว่าแถว persist ฉาก 17
ยัง refuse ที่ login call shape เดิม พบด้วยว่า `docs/FUNCTIONAL_COVERAGE.json` ยังเขียนว่ามี evidence gap
สอง gap (ที่จริงเหลือหนึ่ง) - แก้เป็น UPDATE ใหม่แล้ว (ไม่ลบของเดิม)

ไฟล์ที่แตะเพิ่ม (8): `world_scene_travel.py`, `world_scene_entry.py`, `columbus_quest_dispatch.py`,
`world_scene_registry_001.json`, `test_world_scene_entry.py`, `test_world_scene_travel.py`,
`test_columbus_quest_dispatch.py`, `docs/FUNCTIONAL_COVERAGE.json` - ไม่แตะ `runtime.py`/`app.py`/`current/`
เลยสักไฟล์ ตัวเลข: เทสกลุ่มเป้าหมาย **208/208 ผ่าน**, เทสทั้งเรโป **3555 เทส (3543+12 ใหม่), error 18 ตัวเดิม
(capstone), 0 FAIL** CORE-REQUEST: none รายละเอียดเต็มอยู่ใน round file addendum เดียวกันนี้

— สาย A · WORLD

---
_Generated by [Claude Code](https://claude.com/claude-code)_
